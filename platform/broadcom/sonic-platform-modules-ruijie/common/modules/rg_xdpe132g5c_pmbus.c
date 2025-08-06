/*
 * xdpe132g5c_pumbus_drv.c
 *
 * Hardware monitoring driver for Infineon Multi-phase Digital VR Controllers
 * through xdpe132g5c PMBUS address.
 *
 * History
 *  [Version]                [Date]                    [Description]
 *   *  v1.0                2021-09-17                  Initial version
 */

#include <linux/err.h>
#include <linux/i2c.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/hwmon-sysfs.h>
#include <linux/string.h>
#include <linux/sysfs.h>
#include <linux/delay.h>
#include <linux/mutex.h>
#include "rg_pmbus.h"

typedef enum {
    DBG_START,
    DBG_VERBOSE,
    DBG_KEY,
    DBG_WARN,
    DBG_ERROR,
    DBG_END,
} dbg_level_t;

static int debuglevel = 0;
module_param(debuglevel, int, S_IRUGO);

#define DBG_DEBUG(fmt, arg...)  do { \
    if ( debuglevel > DBG_START && debuglevel < DBG_ERROR) { \
          printk(KERN_INFO "[DEBUG]:<%s, %d>:"fmt, __FUNCTION__, __LINE__, ##arg); \
    } else if ( debuglevel >= DBG_ERROR ) {   \
        printk(KERN_ERR "[DEBUG]:<%s, %d>:"fmt, __FUNCTION__, __LINE__, ##arg); \
    } else {    } \
} while (0)

#define DBG_ERROR(fmt, arg...)  do { \
     if ( debuglevel > DBG_START) {  \
        printk(KERN_ERR "[ERROR]:<%s, %d>:"fmt, __FUNCTION__, __LINE__, ##arg); \
       } \
} while (0)

#define BUF_SIZE                    (256)
#define XDPE132G5C_PAGE_NUM         (2)

struct pmbus_data {
	struct device *dev;
	struct device *hwmon_dev;

	u32 flags;		/* from platform data */

	int exponent[PMBUS_PAGES];
				/* linear mode: exponent for output voltages */

	const struct pmbus_driver_info *info;

	int max_attributes;
	int num_attributes;
	struct attribute_group group;
	const struct attribute_group *groups[2];
	struct dentry *debugfs;		/* debugfs device directory */

	struct pmbus_sensor *sensors;

	struct mutex update_lock;
	bool valid;
	unsigned long last_updated;	/* in jiffies */

	/*
	 * A single status register covers multiple attributes,
	 * so we keep them all together.
	 */
	u16 status[PB_NUM_STATUS_REG];

	bool has_status_word;		/* device uses STATUS_WORD register */
	int (*read_status)(struct i2c_client *client, int page);

	u8 currpage;
};

static ssize_t set_xdpe132g5c_avs(struct device *dev, struct device_attribute *da, const char *buf,
                                    size_t count)
{
    int ret;
    unsigned long val;
    struct sensor_device_attribute *attr = to_sensor_dev_attr(da);
    struct i2c_client *client = to_i2c_client(dev);
    struct pmbus_data *data;

    data = i2c_get_clientdata(client);
    ret = kstrtoul(buf, 16, &val);
    if (ret){
        return ret;
    }
    mutex_lock(&data->update_lock);
    /* set value */
    ret = rg_pmbus_write_word_data(client, attr->index, PMBUS_VOUT_COMMAND, val);
    if (ret < 0) {
        DBG_ERROR("set pmbus_vout_command fail\n");
        goto finish_set;
    }
finish_set:
    rg_pmbus_clear_faults(client);
    mutex_unlock(&data->update_lock);
    return (ret < 0) ? ret : count;

}

static ssize_t show_xdpe132g5c_avs(struct device *dev, struct device_attribute *da, char *buf)
{
    int val;
    struct sensor_device_attribute *attr = to_sensor_dev_attr(da);
    struct i2c_client *client = to_i2c_client(dev);
    struct pmbus_data *data;

    data = i2c_get_clientdata(client);
    mutex_lock(&data->update_lock);
    val = rg_pmbus_read_word_data(client, attr->index, PMBUS_VOUT_COMMAND);
    if (val < 0) {
        DBG_ERROR("fail val = %d\n", val);
        goto finish_show;
    }
finish_show:
    rg_pmbus_clear_faults(client);
    mutex_unlock(&data->update_lock);
    return snprintf(buf, BUF_SIZE, "0x%04x\n", val);
}

static SENSOR_DEVICE_ATTR(avs0_vout_command, S_IRUGO | S_IWUSR, show_xdpe132g5c_avs, set_xdpe132g5c_avs, 0);
static SENSOR_DEVICE_ATTR(avs1_vout_command, S_IRUGO | S_IWUSR, show_xdpe132g5c_avs, set_xdpe132g5c_avs, 1);

static struct attribute *xdpe132g5c_sysfs_attrs[] = {
    &sensor_dev_attr_avs0_vout_command.dev_attr.attr,
    &sensor_dev_attr_avs1_vout_command.dev_attr.attr,
    NULL,
};

static const struct attribute_group xdpe132g5c_sysfs_attrs_group = {
    .attrs = xdpe132g5c_sysfs_attrs,
};

static struct pmbus_driver_info xdpe132g5c_info = {
    .pages = XDPE132G5C_PAGE_NUM,
    .format[PSC_VOLTAGE_IN] = linear,
    .format[PSC_VOLTAGE_OUT] = linear,
    .format[PSC_TEMPERATURE] = linear,
    .format[PSC_CURRENT_IN] = linear,
    .format[PSC_CURRENT_OUT] = linear,
    .format[PSC_POWER] = linear,
    .func[0] = PMBUS_HAVE_VIN | PMBUS_HAVE_IIN | PMBUS_HAVE_PIN
        | PMBUS_HAVE_STATUS_INPUT | PMBUS_HAVE_TEMP
        | PMBUS_HAVE_STATUS_TEMP
        | PMBUS_HAVE_VOUT | PMBUS_HAVE_STATUS_VOUT
        | PMBUS_HAVE_IOUT | PMBUS_HAVE_STATUS_IOUT | PMBUS_HAVE_POUT,
    .func[1] = PMBUS_HAVE_VIN | PMBUS_HAVE_IIN | PMBUS_HAVE_PIN
        | PMBUS_HAVE_STATUS_INPUT
        | PMBUS_HAVE_VOUT | PMBUS_HAVE_STATUS_VOUT
        | PMBUS_HAVE_IOUT | PMBUS_HAVE_STATUS_IOUT | PMBUS_HAVE_POUT,
};

static int xdpe132g5c_probe(struct i2c_client *client,
             const struct i2c_device_id *id)
{
    int status;
    struct pmbus_driver_info *info;

	info = devm_kmemdup(&client->dev, &xdpe132g5c_info, sizeof(*info), GFP_KERNEL);
	if (!info){
        return -ENOMEM;
    }

    status = rg_pmbus_do_probe(client, id, info);
    if (status != 0) {
        DBG_ERROR("pmbus probe error %d\n", status);
        return status;
    }

    status = sysfs_create_group(&client->dev.kobj, &xdpe132g5c_sysfs_attrs_group);
    if (status != 0) {
        DBG_ERROR("sysfs_create_group error %d\n", status);
        return status;
    }

    return status;
}

static int xdpe132g5c_remove(struct i2c_client *client)
{
    int ret;

    sysfs_remove_group(&client->dev.kobj, &xdpe132g5c_sysfs_attrs_group);
    ret = rg_pmbus_do_remove(client);
    if (ret != 0){
        DBG_ERROR("fail remove xdpe132g5c %d\n", ret);
    }
    return ret;
}

static const struct i2c_device_id xdpe132g5c_id[] = {
    {"rg_xdpe132g5c_pmbus", 0},
    {}
};

MODULE_DEVICE_TABLE(i2c, xdpe132g5c_id);

static const struct of_device_id __maybe_unused xdpe132g5c_of_match[] = {
    {.compatible = "infineon,rg_xdpe132g5c_pmbus"},
    {}
};
MODULE_DEVICE_TABLE(of, xdpe132g5c_of_match);

static struct i2c_driver xdpe132g5c_driver = {
    .driver = {
        .name = "rg_xdpe132g5c_pmbus",
        .of_match_table = of_match_ptr(xdpe132g5c_of_match),
    },
    .probe = xdpe132g5c_probe,
    .remove = xdpe132g5c_remove,
    .id_table = xdpe132g5c_id,
};

module_i2c_driver(xdpe132g5c_driver);

MODULE_AUTHOR("rd <rd@ruijie.com>");
MODULE_DESCRIPTION("PMBus driver for Infineon XDPE132 family");
MODULE_LICENSE("GPL");
