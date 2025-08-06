/*
 * rg_psu.c - A driver for control rg_psu base on rg_psu.c
 *
 * Copyright (c) 2018 sonic_rd <sonic_rd@ruijie.com.cn>
 *
 */

#include <linux/module.h>
#include <linux/init.h>
#include <linux/slab.h>
#include <linux/jiffies.h>
#include <linux/i2c.h>
#include <linux/hwmon.h>
#include <linux/hwmon-sysfs.h>
#include <linux/err.h>
#include <linux/mutex.h>
#include "ruijie.h"

#define MAGIC_PSU_RATE              0xA7
#define MAGIC_PSU_OUT_CURRENT       0x8C
#define MAGIC_PSU_OUT_VOLTAGE       0x8B
#define MAGIC_PSU_IN_VOLTAGE        0x88
#define MAGIC_PSU_IN_CURRENT        0x89
#define MAGIC_PSU_TEMP              0x8D
#define MAGIC_PSU_TYPE              0x25
#define MAGIC_PSU_SN                0x38
#define MAGIC_PSU_HW                0x35
#define MAGIC_PSU_VENDOR            0x0C
#define PSU_SIZE 256

struct psu_data {
    struct i2c_client   *client;
	struct device		*hwmon_dev;
    struct mutex        update_lock;
    char            valid;       /* !=0 if registers are valid */
    unsigned long       last_updated;    /* In jiffies */
    u8          data[PSU_SIZE]; /* Register value */
};

int debuglevel = 0;
module_param(debuglevel, int, S_IRUGO | S_IWUSR);

static ssize_t show_psu_sysfs_value(struct device *dev, struct device_attribute *da, char *buf);
static ssize_t show_sysfs_15_value(struct device *dev, struct device_attribute *da, char *buf);
static ssize_t show_sysfs_13_value(struct device *dev, struct device_attribute *da, char *buf);
static ssize_t show_sysfs_7_value(struct device *dev, struct device_attribute *da, char *buf);
static ssize_t show_psu_value(struct device *dev, struct device_attribute *da, char *buf);
static ssize_t show_psu_e2_sysfs_value(struct device *dev, struct device_attribute *da, char *buf);

static SENSOR_DEVICE_ATTR(psu_rate, S_IRUGO, show_psu_sysfs_value, NULL, MAGIC_PSU_RATE);
static SENSOR_DEVICE_ATTR(psu_out_current, S_IRUGO, show_psu_sysfs_value, NULL, MAGIC_PSU_OUT_CURRENT);
static SENSOR_DEVICE_ATTR(psu_out_voltage, S_IRUGO, show_psu_sysfs_value, NULL, MAGIC_PSU_OUT_VOLTAGE);
static SENSOR_DEVICE_ATTR(psu_in_voltage, S_IRUGO, show_psu_sysfs_value, NULL, MAGIC_PSU_IN_VOLTAGE);
static SENSOR_DEVICE_ATTR(psu_in_current, S_IRUGO, show_psu_sysfs_value, NULL, MAGIC_PSU_IN_CURRENT);
static SENSOR_DEVICE_ATTR(psu_temp, S_IRUGO, show_psu_sysfs_value, NULL, MAGIC_PSU_TEMP);
static SENSOR_DEVICE_ATTR(psu_type, S_IRUGO, show_sysfs_15_value, NULL, MAGIC_PSU_TYPE);
static SENSOR_DEVICE_ATTR(psu_sn, S_IRUGO, show_sysfs_13_value, NULL, MAGIC_PSU_SN);
static SENSOR_DEVICE_ATTR(psu_vendor, S_IRUGO, show_sysfs_7_value, NULL, MAGIC_PSU_VENDOR);
static SENSOR_DEVICE_ATTR(psu_hw, S_IRUGO, show_psu_value, NULL, MAGIC_PSU_HW);
static SENSOR_DEVICE_ATTR(psu_eeprom, S_IRUGO, show_psu_e2_sysfs_value, NULL, 0);

static struct attribute *psu_pmbus_sysfs_attrs[] = {
    &sensor_dev_attr_psu_rate.dev_attr.attr,
    &sensor_dev_attr_psu_out_current.dev_attr.attr,
    &sensor_dev_attr_psu_out_voltage.dev_attr.attr,
    &sensor_dev_attr_psu_in_voltage.dev_attr.attr,
    &sensor_dev_attr_psu_in_current.dev_attr.attr,
    &sensor_dev_attr_psu_temp.dev_attr.attr,
    NULL
};

static struct attribute *psu_fru_sysfs_attrs[] = {
    &sensor_dev_attr_psu_type.dev_attr.attr,
    &sensor_dev_attr_psu_sn.dev_attr.attr,
    &sensor_dev_attr_psu_vendor.dev_attr.attr,
    &sensor_dev_attr_psu_hw.dev_attr.attr,
    &sensor_dev_attr_psu_eeprom.dev_attr.attr,
    NULL
};

static const struct attribute_group psu_pmbus_sysfs_attrs_group = {
    .attrs = psu_pmbus_sysfs_attrs,
};

static const struct attribute_group psu_fru_sysfs_attrs_group = {
    .attrs = psu_fru_sysfs_attrs,
};

static ssize_t show_psu_value(struct device *dev, struct device_attribute *da, char *buf)
{
    struct sensor_device_attribute *attr = to_sensor_dev_attr(da);
    struct i2c_client *client = to_i2c_client(dev);
    struct psu_data *data = i2c_get_clientdata(client);
    int ret;
    char psu_buf[PSU_SIZE];
    memset(psu_buf, 0, PSU_SIZE);
    mutex_lock(&data->update_lock);
    ret = platform_i2c_smbus_read_i2c_block_data(client, attr->index, 2, psu_buf);
    if (ret < 0) {
		DBG_ERROR("Failed to read psu \n");
	}
    DBG_DEBUG("cpld reg pos:0x%x value:0x%02x\n",  attr->index, data->data[0]);
    mutex_unlock(&data->update_lock);
    return snprintf(buf, PSU_SIZE, "%s\n", psu_buf);
}

static int linear_to_value(short reg, bool v_out)
{
    short exponent;
    int mantissa;
    long val;

    if (v_out) {
        exponent = -9;
        mantissa = (uint16_t)reg;
    } else {
        exponent = reg >> 11;
        mantissa = ((short)((reg & 0x7ff) << 5)) >> 5;
    }
    val = mantissa;
    val = val * 1000L;
    if (exponent >= 0) {
        val <<= exponent;
    }else{
        val >>= -exponent;
    }

    return val;
}

static ssize_t show_psu_sysfs_value(struct device *dev, struct device_attribute *da, char *buf)
{
    struct sensor_device_attribute *attr = to_sensor_dev_attr(da);
    struct i2c_client *client = to_i2c_client(dev);
    struct psu_data *data = i2c_get_clientdata(client);
    int ret;
    u8  smbud_buf[PSU_SIZE];
    uint16_t value;
    int result;

    ret = -1;
    memset(smbud_buf, 0, PSU_SIZE);
    mutex_lock(&data->update_lock);
    DBG_DEBUG("ret:%d", ret);
    ret = platform_i2c_smbus_read_i2c_block_data(client, attr->index, 2, smbud_buf);
    if (ret < 0) {
		DBG_ERROR("Failed to read psu \n");
	}
    value = smbud_buf[1];
    value = value << 8;
    value |= smbud_buf[0];

    if (attr->index == 0x8b) {
        result = linear_to_value(value, true);
    } else {
        result = linear_to_value(value, false);
    }
    mutex_unlock(&data->update_lock);
    return snprintf(buf, PSU_SIZE,  "%d\n", result);
}

static ssize_t show_sysfs_15_value(struct device *dev, struct device_attribute *da, char *buf)
{
    struct sensor_device_attribute *attr = to_sensor_dev_attr(da);
    struct i2c_client *client = to_i2c_client(dev);
    struct psu_data *data = i2c_get_clientdata(client);
    int ret;
    u8  smbud_buf[PSU_SIZE];

    memset(smbud_buf, 0, PSU_SIZE);
    mutex_lock(&data->update_lock);
    ret = platform_i2c_smbus_read_i2c_block_data(client, attr->index, 15, smbud_buf);
    if (ret < 0) {
        DBG_ERROR("Failed to read psu \n");
    }
    mutex_unlock(&data->update_lock);
    return snprintf(buf, PSU_SIZE, "%s\n", smbud_buf);
}

static ssize_t show_sysfs_13_value(struct device *dev, struct device_attribute *da, char *buf)
{
    struct sensor_device_attribute *attr = to_sensor_dev_attr(da);
    struct i2c_client *client = to_i2c_client(dev);
    struct psu_data *data = i2c_get_clientdata(client);
    int ret;
    u8  smbud_buf[PSU_SIZE];

    memset(smbud_buf, 0, PSU_SIZE);
    mutex_lock(&data->update_lock);
    ret = platform_i2c_smbus_read_i2c_block_data(client, attr->index, 13, smbud_buf);
    if (ret < 0) {
        DBG_ERROR("Failed to read psu \n");
    }
    mutex_unlock(&data->update_lock);
    return snprintf(buf, PSU_SIZE, "%s\n", smbud_buf);
}

static ssize_t show_sysfs_7_value(struct device *dev, struct device_attribute *da, char *buf)
{
    struct sensor_device_attribute *attr = to_sensor_dev_attr(da);
    struct i2c_client *client = to_i2c_client(dev);
    struct psu_data *data = i2c_get_clientdata(client);
    int ret;
    u8  smbud_buf[PSU_SIZE];

    memset(smbud_buf, 0, PSU_SIZE);
    mutex_lock(&data->update_lock);
    ret = platform_i2c_smbus_read_i2c_block_data(client, attr->index, 7, smbud_buf);
    if (ret < 0) {
        DBG_ERROR("Failed to read psu \n");
    }
    mutex_unlock(&data->update_lock);
    return snprintf(buf, PSU_SIZE, "%s\n", smbud_buf);
}

/*
 * read psu eeprom 256byes and send the data to sysfs node
 */
static ssize_t show_psu_e2_sysfs_value(struct device *dev, struct device_attribute *da, char *buf)
{
    struct i2c_client *client = to_i2c_client(dev);
    struct psu_data *data = i2c_get_clientdata(client);
    int i;

    mutex_lock(&data->update_lock);
    if (i2c_check_functionality(client->adapter, I2C_FUNC_SMBUS_READ_I2C_BLOCK)) {
        /* support block read */
        for (i = 0; i < PSU_SIZE; i += 32) {
                if (platform_i2c_smbus_read_i2c_block_data(client, i, 32, data->data + i) != 32) {
                    goto exit;
                }
            }
    } else {
        /* support word read */
        for (i = 0; i < PSU_SIZE; i += 2) {
            int word = platform_i2c_smbus_read_word_data(client, i);
            if (word < 0) {
                goto exit;
            }
            data->data[i] = word & 0xff;
            data->data[i + 1] = word >> 8;
        }
    }
    memcpy(buf, &data->data[0], PSU_SIZE);
exit:
    DBG_DEBUG("read times:%d", i);
	mutex_unlock(&data->update_lock);
    return PSU_SIZE;
}

#if 0
static int psu_detect(struct i2c_client *new_client, struct i2c_board_info *info)
{
    struct i2c_adapter *adapter = new_client->adapter;
    int conf;

    if (!i2c_check_functionality(adapter, I2C_FUNC_SMBUS_BYTE_DATA |
                     I2C_FUNC_SMBUS_WORD_DATA))
        return -ENODEV;
    conf = platform_i2c_smbus_read_byte_data(new_client, 0);
    if (!conf)
        return -ENODEV;

    return 0;
}
#endif

static int psu_probe(struct i2c_client *client, const struct i2c_device_id *id)
{
    struct psu_data *data;
    int status;

	status = -1;
    data = devm_kzalloc(&client->dev, sizeof(struct psu_data), GFP_KERNEL);
    if (!data)
        return -ENOMEM;

    data->client = client;
    i2c_set_clientdata(client, data);
    mutex_init(&data->update_lock);

    switch (client->addr) {
        case 0x50:
        case 0x53:
            status = sysfs_create_group(&client->dev.kobj, &psu_fru_sysfs_attrs_group);
            if (status !=0) {
                DBG_ERROR("%s %d sysfs_create_group err\n", __func__, __LINE__);
            }
            break;
        case 0x58:
        case 0x5b:
            status = sysfs_create_group(&client->dev.kobj, &psu_pmbus_sysfs_attrs_group);
            if (status !=0) {
                DBG_ERROR("%s %d sysfs_create_group err\n", __func__, __LINE__);
                break;
            }
            break;
        default:
            break;

    }

    return status;
}

static int psu_remove(struct i2c_client *client)
{
    switch (client->addr) {
        case 0x50:
        case 0x53:
            sysfs_remove_group(&client->dev.kobj, &psu_fru_sysfs_attrs_group);
            break;
        case 0x58:
        case 0x5b:
            sysfs_remove_group(&client->dev.kobj, &psu_pmbus_sysfs_attrs_group);
            break;
        default:
            break;
    }
    return 0;
}

static const struct i2c_device_id psu_id[] = {
    { "rg_psu", 0 },
    {}
};
MODULE_DEVICE_TABLE(i2c, psu_id);

static struct i2c_driver rg_psu_driver = {
    .class      = I2C_CLASS_HWMON,
    .driver = {
        .name   = "rg_psu",
    },
    .probe      = psu_probe,
    .remove     = psu_remove,
    .id_table   = psu_id,
};

module_i2c_driver(rg_psu_driver);

MODULE_AUTHOR("sonic_rd <sonic_rd@ruijie.com.cn>");
MODULE_DESCRIPTION("ruijie CPLD driver");
MODULE_LICENSE("GPL");
