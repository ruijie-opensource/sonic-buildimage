/*
 * isl68137.c Hardware monitoring driver for Intersil ISL68137
 *
 * Copyright (c) 2017
 *
 */

#include <linux/err.h>
#include <linux/hwmon-sysfs.h>
#include <linux/i2c.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/string.h>
#include <linux/sysfs.h>
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
module_param(debuglevel, int, S_IRUGO | S_IWUSR);

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

#define WRITE_PROTECT_CLOSE         (0x00)
#define WRITE_PROTECT_OPEN          (0x40)
#define WRITE_PROTECT               (0x10)
#define ISL68127_PAGE_NUM           (2)

static ssize_t set_isl68137_avs(struct device *dev, struct device_attribute *da, const char *buf, size_t
count)
{
    int err, rv;
    unsigned long val;
    struct sensor_device_attribute *attr = to_sensor_dev_attr(da);
    struct i2c_client *client = to_i2c_client(dev);

    err = kstrtoul(buf, 16, &val);
    if (err){
        return err;
    }

    /* 关闭写保护 */
    rv = rg_pmbus_write_byte_data(client, attr->index, WRITE_PROTECT, WRITE_PROTECT_CLOSE);
    if (rv < 0) {
        DBG_ERROR("close write_protect_cloes fail\n");
		return rv;
    }
    /* 设置数值 */
    rv = rg_pmbus_write_word_data(client, attr->index, PMBUS_VOUT_COMMAND, val);
    if (rv < 0) {
        DBG_ERROR("set pmbus_vout_command fail\n");
		return rv;
    }
    /* 打开写保护 */
    rv = rg_pmbus_write_byte_data(client, attr->index, WRITE_PROTECT, WRITE_PROTECT_OPEN);
    if (rv < 0) {
        DBG_ERROR("open write_protect_cloes fail\n");
		return rv;
    }
    return count;

}

static ssize_t show_isl68137_avs(struct device *dev, struct device_attribute *da, char *buf)
{
    int val;
    struct sensor_device_attribute *attr = to_sensor_dev_attr(da);
    struct i2c_client *client = to_i2c_client(dev);

    val = rg_pmbus_read_word_data(client, attr->index, PMBUS_VOUT_COMMAND);
    if (val < 0) {
        DBG_ERROR("fail val = %d\n", val);
        return 0;
    }

    DBG_DEBUG("buf_tmp = %d\n", val);
    return sprintf(buf, "0x%04x\n", val);

}

static SENSOR_DEVICE_ATTR(avs0_vout_command, S_IRUGO | S_IWUSR, show_isl68137_avs, set_isl68137_avs, 0);
static SENSOR_DEVICE_ATTR(avs1_vout_command, S_IRUGO | S_IWUSR, show_isl68137_avs, set_isl68137_avs, 1);

static struct attribute *isl68137_sysfs_attrs[] = {
    &sensor_dev_attr_avs0_vout_command.dev_attr.attr,
    &sensor_dev_attr_avs1_vout_command.dev_attr.attr,
    NULL,
};

static const struct attribute_group isl68137_sysfs_attrs_group = {
    .attrs = isl68137_sysfs_attrs,
};

static struct pmbus_driver_info isl68137_info = {
    .pages = ISL68127_PAGE_NUM,
    .format[PSC_VOLTAGE_IN] = direct,
    .format[PSC_VOLTAGE_OUT] = direct,
    .format[PSC_CURRENT_IN] = direct,
    .format[PSC_CURRENT_OUT] = direct,
    .format[PSC_POWER] = direct,
    .format[PSC_TEMPERATURE] = direct,
    .m[PSC_VOLTAGE_IN] = 1,
    .b[PSC_VOLTAGE_IN] = 0,
    .R[PSC_VOLTAGE_IN] = 3,
    .m[PSC_VOLTAGE_OUT] = 1,
    .b[PSC_VOLTAGE_OUT] = 0,
    .R[PSC_VOLTAGE_OUT] = 3,
    .m[PSC_CURRENT_IN] = 1,
    .b[PSC_CURRENT_IN] = 0,
    .R[PSC_CURRENT_IN] = 2,
    .m[PSC_CURRENT_OUT] = 1,
    .b[PSC_CURRENT_OUT] = 0,
    .R[PSC_CURRENT_OUT] = 1,
    .m[PSC_POWER] = 1,
    .b[PSC_POWER] = 0,
    .R[PSC_POWER] = 0,
    .m[PSC_TEMPERATURE] = 1,
    .b[PSC_TEMPERATURE] = 0,
    .R[PSC_TEMPERATURE] = 0,
    .func[0] = PMBUS_HAVE_VIN | PMBUS_HAVE_IIN | PMBUS_HAVE_PIN
        | PMBUS_HAVE_STATUS_INPUT | PMBUS_HAVE_TEMP | PMBUS_HAVE_TEMP2
        | PMBUS_HAVE_TEMP3 | PMBUS_HAVE_STATUS_TEMP
        | PMBUS_HAVE_VOUT | PMBUS_HAVE_STATUS_VOUT
        | PMBUS_HAVE_IOUT | PMBUS_HAVE_STATUS_IOUT | PMBUS_HAVE_POUT,
    .func[1] = PMBUS_HAVE_VOUT | PMBUS_HAVE_STATUS_VOUT
        | PMBUS_HAVE_IOUT | PMBUS_HAVE_STATUS_IOUT | PMBUS_HAVE_POUT,

};

static int isl68137_probe(struct i2c_client *client,
              const struct i2c_device_id *id)
{
    int status;
    struct pmbus_driver_info *info;

	info = devm_kmemdup(&client->dev, &isl68137_info, sizeof(*info), GFP_KERNEL);
	if (!info){
        return -ENOMEM;
    }

    status = rg_pmbus_do_probe(client, id, info);
    if (status != 0) {
        DBG_ERROR("pmbus_do_probe ret = %d\n", status);
        return -1;
    }
    status = sysfs_create_group(&client->dev.kobj, &isl68137_sysfs_attrs_group);
    if (status != 0) {
        DBG_ERROR("sysfs_create_group error\n");
        return -1;
    }
    return 0;
}

static const struct i2c_device_id isl68137_id[] = {
    {"rg_isl68137", 0},
    {}
};

static int isl68137_remove(struct i2c_client *client)
{
    sysfs_remove_group(&client->dev.kobj, &isl68137_sysfs_attrs_group);
    return 0;
}

MODULE_DEVICE_TABLE(i2c, isl68137_id);

/* This is the driver that will be inserted */
static struct i2c_driver isl68137_driver = {
    .driver = {
           .name = "rg_isl68137",
           },
    .probe = isl68137_probe,
    .remove = isl68137_remove,
    .id_table = isl68137_id,
};

module_i2c_driver(isl68137_driver);

MODULE_AUTHOR("sonic_rd <sonic_rd@ruijie.com.cn>");
MODULE_DESCRIPTION("PMBus driver for Intersil ISL68137");
MODULE_LICENSE("GPL");
