/*
 * Copyright(C) 2001-2012 Ruijie Network. All rights reserved.
 */
/*
 * rg_psu_driver.c
 * Original Author: sonic_rd@ruijie.com.cn 2020-02-17
 *
 * 电源相关属性读写函数
 * History
 *  [Version]        [Author]                   [Date]            [Description]
 *   *  v1.0    sonic_rd@ruijie.com.cn         2020-02-17          Initial version
 */

#include <linux/module.h>
#include <linux/slab.h>

#include "./include/rg_module.h"
#include "./include/dfd_cfg.h"
#include "./include/dfd_cfg_adapter.h"
#include "./include/dfd_cfg_info.h"
#include "./include/dfd_frueeprom.h"

#define PSU_SIZE                         (256)
#define RG_GET_PSU_PMBUS_BUS(addr)       (((addr) >> 24) & 0xff)
#define RG_GET_PSU_PMBUS_ADDR(addr)      (((addr) >> 8) & 0xffff)
#define RG_GET_PSU_PMBUS_OFFSET(addr)    ((addr) & 0xff)

typedef enum dfd_psu_pmbus_type_e {
    DFD_PSU_PMBUS_TYPE_AC      = 1,
    DFD_PSU_PMBUS_TYPE_DC      = 2,
} dfd_psu_pmbus_type_t;

typedef enum dfd_psu_sysfs_type_e {
    DFD_PSU_SYSFS_TYPE_DC      = 0,
    DFD_PSU_SYSFS_TYPE_AC      = 1,
} dfd_psu_sysfs_type_t;

typedef enum dfd_psu_status_e {
    DFD_PSU_PRESENT_STATUS  = 0,
    DFD_PSU_OUTPUT_STATUS   = 1,
    DFD_PSU_ALERT_STATUS    = 2,
    DFD_PSU_INPUT_STATUS    = 3,
} dfd_psu_status_t;

typedef enum dfd_psu_alarm_e{
    DFD_PSU_NOT_OK        = 0,
    DFD_PSU_OK        = 1,
} dfd_psu_alarm_t;

enum knos_alarm{
    PSU_TERMAL_ERROR    = 0x1,
    PSU_FAN_ERROR       = 0x2,
    PSU_VOL_ERROR       = 0x4,
};

/* PMBUS STATUS WORD decode */
#define PSU_STATUS_WORD_CML             (1 << 1)
#define PSU_STATUS_WORD_TEMPERATURE     (1 << 2)
#define PSU_STATUS_WORD_VIN_UV          (1 << 3)
#define PSU_STATUS_WORD_IOUT_OC         (1 << 4)
#define PSU_STATUS_WORD_VOUT_OV         (1 << 5)
#define PSU_STATUS_WORD_OFF             (1 << 6)
#define PSU_STATUS_WORD_BUSY            (1 << 7)
#define PSU_STATUS_WORD_FANS            (1 << 10)
#define PSU_STATUS_WORD_POWER_GOOD      (1 << 11)
#define PSU_STATUS_WORD_INPUT           (1 << 13)
#define PSU_STATUS_WORD_IOUT            (1 << 14)
#define PSU_STATUS_WORD_VOUT            (1 << 15)

#define PSU_VOLTAGE_ERR_OFFSET          (PSU_STATUS_WORD_VOUT | PSU_STATUS_WORD_IOUT | \
                                         PSU_STATUS_WORD_INPUT | PSU_STATUS_WORD_POWER_GOOD| \
                                         PSU_STATUS_WORD_OFF | PSU_STATUS_WORD_VOUT_OV| \
                                         PSU_STATUS_WORD_IOUT_OC | PSU_STATUS_WORD_VIN_UV)

int g_dfd_psu_dbg_level = 0;
module_param(g_dfd_psu_dbg_level, int, S_IRUGO | S_IWUSR);

static char *dfd_get_psu_sysfs_name(void)
{
    int key;
    char *sysfs_name;

    /* string类型配置项 */
    key = DFD_CFG_KEY(DFD_CFG_ITEM_PSU_SYSFS_NAME, 0, 0);
    sysfs_name = dfd_ko_cfg_get_item(key);
    if (sysfs_name == NULL) {
        DFD_PSU_DEBUG(DBG_VERBOSE, "key=0x%08x, sysfs_name is NULL, use default way.\n", key);
    } else {
        DFD_PSU_DEBUG(DBG_VERBOSE, "sysfs_name: %s.\n", sysfs_name);
    }
    return sysfs_name;
}

static void dfd_psu_del_no_print_string(char *buf)
{
    int i, len;

    len = strlen(buf);
    /* 剔除非字符 */
    for (i = 0; i < len; i++) {
        if ((buf[i] < 0x21) || (buf[i] > 0x7E)) {
            buf[i] = '\0';
            break;
        }
    }
    return ;
}


/**
 * dfd_get_psu_present_status - 获取电源在位状态
 * @index: 电源的编号,从1开始
 * return: 0：不在位
 *         1：在位
 *       : 负值 - 读取失败
 */
static int dfd_get_psu_present_status(unsigned int psu_index)
{
    int present_key, present_status;
    int ret;

    /* 获取在位状态 */
    present_key = DFD_CFG_KEY(DFD_CFG_ITEM_PSU_STATUS, psu_index, DFD_PSU_PRESENT_STATUS);
    ret = dfd_info_get_int(present_key, &present_status, NULL);
    if (ret  < 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "dfd_get_psu_status error. psu_index: %u, ret: %d\n",
            psu_index, ret);
        return ret;
    }

    return present_status;
}

/**
 * dfd_get_psu_present_status_str - 获取电源状态
 * @index: 电源的编号,从1开始
 * return: 成功:状态字符串长度
 *       : 负值 - 读取失败
 */
ssize_t dfd_get_psu_present_status_str(unsigned int psu_index, char *buf, size_t count)
{
    int ret;
    if (buf == NULL) {
        DFD_PSU_DEBUG(DBG_ERROR, "params error.psu_index: %u.",psu_index);
        return -EINVAL;
    }
    if (count <= 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "buf size error, count: %lu, psu index: %u\n",
            count, psu_index);
        return -EINVAL;
    }

    ret = dfd_get_psu_present_status(psu_index);
    if (ret < 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "get psu status error, ret: %d, psu_index: %u\n", ret, psu_index);
        return -EIO;
    }
    memset(buf, 0, count);
    return (ssize_t)snprintf(buf, count, "%d\n", ret);
}


/**
 * dfd_get_psu_status_pmbus_str - 获取电源pmbus寄存器上的值
 * @index: 电源的编号,从1开始
 * return: 成功:状态字符串长度
 *       : 负值 - 读取失败
 */
ssize_t dfd_get_psu_status_pmbus_str(unsigned int psu_index, char *buf, size_t count)
{
    int ret, key;
    int pmbus_data;

    if (buf == NULL) {
        DFD_PSU_DEBUG(DBG_ERROR, "buf is NULL, psu index: %u\n", psu_index);
        return -EINVAL;
    }
    if (count <= 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "buf size error, count: %lu, psu index: %u\n", count, psu_index);
        return -EINVAL;
    }

    /* 从电源的pmbus寄存器获取状态 */
    key = DFD_CFG_KEY(DFD_CFG_ITEM_PSU_PMBUS_REG, psu_index, PSU_SENSOR_NONE);
    ret = dfd_info_get_int(key, &pmbus_data, NULL);
    if (ret == -DFD_RV_DEV_NOTSUPPORT) {
        DFD_PSU_DEBUG(DBG_WARN, "get psu%u pmbus status info don't support\n", psu_index);
        return snprintf(buf, count, "%s\n", SWITCH_DEV_NO_SUPPORT);
    } else if (ret < 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "get psu%u pmbus status info failed, key: 0x%x, ret: %d\n", psu_index, key, ret);
        return -EIO;
    }

    DFD_PSU_DEBUG(DBG_VERBOSE, "psu_index: %u, pmbus_data = 0x%x \n", psu_index, pmbus_data);

    memset(buf, 0, count);
    return (ssize_t)snprintf(buf, count, "%d\n", pmbus_data);
}

/**
 * dfd_get_psu_fan_speed_max_str - 获取电源转速最大值
 * @index: 电源的编号,从1开始
 * return: 成功:电源转速最大值
 *       : 负值 - 读取失败
 */
static int dfd_get_psu_fan_speed_max_str(int power_type, char *psu_buf, int buf_len)
{
    int key, value;
    int *speed_max;

    key = DFD_CFG_KEY(DFD_CFG_ITEM_FAN_SPEED_MAX, power_type, 0);
    speed_max = dfd_ko_cfg_get_item(key);
    if (speed_max == NULL) {
        DFD_PSU_DEBUG(DBG_ERROR, "config error, get psu speed max error, key: 0x%x\n", key);
        return -DFD_RV_DEV_NOTSUPPORT;
    }
    value = *speed_max;
    memset(psu_buf, 0, buf_len);
    snprintf(psu_buf, buf_len, "%d", value);
    DFD_PSU_DEBUG(DBG_VERBOSE, "psu speed max match ok, speed_max: %d\n", value);
    return DFD_RV_OK;
}

/**
 * dfd_get_psu_fan_speed_max_str - 获取电源转速最小值
 * @index: 电源的编号,从1开始
 * return: 成功:电源转速最小值
 *       : 负值 - 读取失败
 */
static int dfd_get_psu_fan_speed_min_str(int power_type, char *psu_buf, int buf_len)
{
    int key, value;
    int *speed_min;

    key = DFD_CFG_KEY(DFD_CFG_ITEM_FAN_SPEED_MIN, power_type, 0);
    speed_min = dfd_ko_cfg_get_item(key);
    if (speed_min == NULL) {
        DFD_PSU_DEBUG(DBG_ERROR, "config error, get psu speed min error, key: 0x%x\n", key);
        return -DFD_RV_DEV_NOTSUPPORT;
    }
    value = *speed_min;
    memset(psu_buf, 0, buf_len);
    snprintf(psu_buf, buf_len, "%d", value);
    DFD_PSU_DEBUG(DBG_VERBOSE, "psu speed min match ok, speed_min: %d\n", value);
    return DFD_RV_OK;
}

/**
 * dfd_get_psu_out_vol_max_str - 获取电源输入电压最大值
 * @index: 电源的编号,从1开始
 * return: 成功:电源输入电压最大值
 *       : 负值 - 读取失败
 */
static int dfd_get_psu_out_vol_max_str(int power_type, char *psu_buf, int buf_len)
{
    int key, value;
    int *out_vol_max;

    key = DFD_CFG_KEY(DFD_CFG_ITEM_PSU_OUT_VOL_MAX, power_type, 0);
    out_vol_max = dfd_ko_cfg_get_item(key);
    if (out_vol_max == NULL) {
        DFD_PSU_DEBUG(DBG_ERROR, "config error, get psu out_vol max error, key: 0x%x\n", key);
        return -DFD_RV_DEV_NOTSUPPORT;
    }
    value = *out_vol_max;
    memset(psu_buf, 0, buf_len);
    snprintf(psu_buf, buf_len, "%d", value);
    DFD_PSU_DEBUG(DBG_VERBOSE, "psu out_vol max match ok, out_vol_max: %d\n", value);
    return DFD_RV_OK;
}

/**
 * dfd_get_psu_out_vol_max_str - 获取电源输入电压最小值
 * @index: 电源的编号,从1开始
 * return: 成功:电源输入电压最小值
 *       : 负值 - 读取失败
 */
static int dfd_get_psu_out_vol_min_str(int power_type, char *psu_buf, int buf_len)
{
    int key, value;
    int *out_vol_min;

    key = DFD_CFG_KEY(DFD_CFG_ITEM_PSU_OUT_VOL_MIN, power_type, 0);
    out_vol_min = dfd_ko_cfg_get_item(key);
    if (out_vol_min == NULL) {
        DFD_PSU_DEBUG(DBG_ERROR, "config error, get psu out_vol min error, key: 0x%x\n", key);
        return -DFD_RV_DEV_NOTSUPPORT;
    }
    value = *out_vol_min;
    memset(psu_buf, 0, buf_len);
    snprintf(psu_buf, buf_len, "%d", value);
    DFD_PSU_DEBUG(DBG_VERBOSE, "psu out_vol min match ok, out_vol_min: %d\n", value);
    return DFD_RV_OK;
}

/**
 * dfd_get_psu_out_status_str - 获取输出电源状态
 * @index: 电源的编号,从1开始
 * return: 成功:状态字符串长度
 *       : 负值 - 读取失败
 */
ssize_t dfd_get_psu_out_status_str(unsigned int psu_index, char *buf, size_t count)
{
    int ret, key;
    int pmbus_data;
    int output_status;

    if (buf == NULL) {
        DFD_PSU_DEBUG(DBG_ERROR, "buf is NULL, psu index: %u\n", psu_index);
        return -EINVAL;
    }
    if (count <= 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "buf size error, count: %lu, psu index: %u\n", count, psu_index);
        return -EINVAL;
    }

    /* 从电源的pmbus寄存器获取状态 */
    key = DFD_CFG_KEY(DFD_CFG_ITEM_PSU_PMBUS_REG, psu_index, PSU_OUT_STATUS);
    ret = dfd_info_get_int(key, &pmbus_data, NULL);
    if (ret == -DFD_RV_DEV_NOTSUPPORT) {
        DFD_PSU_DEBUG(DBG_WARN, "get psu%u pmbus status info don't support\n", psu_index);
        return snprintf(buf, count, "%s\n", SWITCH_DEV_NO_SUPPORT);
    } else if (ret < 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "get psu%u pmbus status info failed, key: 0x%x, ret: %d\n", psu_index, key, ret);
        return -EIO;
    }

    output_status = DFD_PSU_OK;
    if (pmbus_data & (PSU_STATUS_WORD_INPUT | PSU_STATUS_WORD_OFF | PSU_STATUS_WORD_POWER_GOOD)) {
        /* no power的判断逻辑与百度sysfs的逻辑一致 */
        output_status = DFD_PSU_NOT_OK;
    }
    DFD_PSU_DEBUG(DBG_VERBOSE, "psu_index: %u, pmbus_data = 0x%x \n", psu_index, pmbus_data);

    memset(buf, 0, count);
    return (ssize_t)snprintf(buf, count, "%d\n", output_status);
}

/**
 * dfd_psu_product_name_decode - 电源名称转换
 * @power_type: 电源类型
 * @psu_buf: 电源名称缓冲区
 * @buf_len: psu_buf长度
 * return: 成功：0
 *       ：失败：返回负值
 */
static int dfd_psu_product_name_decode(int power_type, char *psu_buf, int buf_len)
{
    int key;
    char *p_decode_name;

    key = DFD_CFG_KEY(DFD_CFG_ITEM_DECODE_POWER_NAME, power_type, 0);
    p_decode_name = dfd_ko_cfg_get_item(key);
    if (p_decode_name == NULL) {
        DFD_PSU_DEBUG(DBG_ERROR, "config error, get psu decode name error, key: 0x%x\n", key);
        return -DFD_RV_DEV_NOTSUPPORT;
    }
    memset(psu_buf, 0, buf_len);
    strncpy(psu_buf, p_decode_name, buf_len - 1);
    DFD_PSU_DEBUG(DBG_VERBOSE, "psu name match ok, display psu name: %s\n", psu_buf);
    return DFD_RV_OK;
}

/**
 * dfd_psu_fan_direction_decode - 电源风道类型转换
 * @power_type: 电源类型
 * @psu_buf: 电源名称缓冲区
 * @buf_len: psu_buf长度
 * return: 成功：0
 *       ：失败：返回负值
 */
static int dfd_psu_fan_direction_decode(int power_type, char *psu_buf, int buf_len)
{
    int key;
    char *p_decode_direction;

    key = DFD_CFG_KEY(DFD_CFG_ITEM_DECODE_POWER_FAN_DIR, power_type, 0);
    p_decode_direction = dfd_ko_cfg_get_item(key);
    if (p_decode_direction == NULL) {
        DFD_PSU_DEBUG(DBG_ERROR, "config error, get psu decode direction error, key: 0x%x\n", key);
        return -DFD_RV_DEV_NOTSUPPORT;
    }
    memset(psu_buf, 0, buf_len);
    snprintf(psu_buf, buf_len, "%d", *p_decode_direction);
    DFD_PSU_DEBUG(DBG_VERBOSE, "psu%u fan direction match ok, display psu direction: %s\n",
        power_type, psu_buf);
    return DFD_RV_OK;
}

/**
 * dfd_psu_max_output_power - 电源额定功率
 * @power_type: 电源类型
 * @psu_buf: 数据缓冲区
 * @buf_len: psu_buf长度
 * return: 成功：0
 *       ：失败：返回负值
 */
static int dfd_psu_max_output_power(int power_type, char *psu_buf, int buf_len)
{
    int key, value;
    int *p_power_max_output_power;

    key = DFD_CFG_KEY(DFD_CFG_ITEM_POWER_RSUPPLY, power_type, 0);
    p_power_max_output_power = dfd_ko_cfg_get_item(key);
    if (p_power_max_output_power == NULL) {
        DFD_PSU_DEBUG(DBG_ERROR, "config error, get psu input type error, key: 0x%x\n", key);
        return -DFD_RV_DEV_NOTSUPPORT;
    }
    value = *p_power_max_output_power;
    memset(psu_buf, 0, buf_len);
    snprintf(psu_buf, buf_len, "%d", value);
    DFD_PSU_DEBUG(DBG_VERBOSE, "psu name %s match max output power %d\n", psu_buf, value);
    return DFD_RV_OK;
}

static int dfd_get_psu_type(unsigned int psu_index, dfd_i2c_dev_t *i2c_dev, int *power_type,
               const char *sysfs_name)
{
    int rv;
    char psu_buf[PSU_SIZE];

    rv = dfd_get_fru_data(i2c_dev->bus, i2c_dev->addr, DFD_DEV_INFO_TYPE_PART_NUMBER, psu_buf,
             PSU_SIZE, sysfs_name);
    if (rv < 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "get psu type from eeprom read failed, rv: %d\n", rv);
        return -DFD_RV_DEV_FAIL;
    }

    DFD_PSU_DEBUG(DBG_VERBOSE, "%s\n", psu_buf);
    dfd_psu_del_no_print_string(psu_buf);

    DFD_PSU_DEBUG(DBG_VERBOSE, "dfd_psu_product_name_decode get psu name %s\n", psu_buf);
    rv = dfd_ko_cfg_get_power_type_by_name((char *)psu_buf, power_type);
    if (rv < 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "get power type by name[%s] fail, rv: %d\n", psu_buf, rv);
        return -DFD_RV_NO_NODE;
    }

    DFD_PSU_DEBUG(DBG_VERBOSE, "get psu[%u] bus[%d] addr[0x%x] return power_type[0x%x]\n",
            psu_index, i2c_dev->bus, i2c_dev->addr, *power_type);
    return DFD_RV_OK;
}

/**
 * dfd_get_psu_info - 获取电源信息
 * @index: 电源的编号,从1开始
 * @cmd: 电源信息类型,电源名称:2, 电源序列号:3,电源硬件版本号:5
 * @buf: 接收buf
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_psu_info(unsigned int psu_index, uint8_t cmd, char *buf, size_t count)
{
    int key, rv;
    char psu_buf[PSU_SIZE];
    dfd_i2c_dev_t *i2c_dev;
    int power_type;
    const char *sysfs_name;

    if (buf == NULL) {
        DFD_PSU_DEBUG(DBG_ERROR, "buf is NULL, psu index: %u, cmd: 0x%x\n", psu_index, cmd);
        return -EINVAL;
    }
    if (count <= 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "buf size error, count: %lu, psu index: %u, cmd: 0x%x\n",
            count, psu_index, cmd);
        return -EINVAL;
    }

    memset(buf, 0, count);
    memset(psu_buf, 0, PSU_SIZE);
    key = DFD_CFG_KEY(DFD_CFG_ITEM_OTHER_I2C_DEV, RG_MAIN_DEV_PSU, psu_index);
    i2c_dev = dfd_ko_cfg_get_item(key);
    if (i2c_dev == NULL) {
        DFD_PSU_DEBUG(DBG_ERROR, "psu i2c dev config error, key: 0x%08x\n", key);
        return (ssize_t)snprintf(buf, count, "%s\n", SWITCH_DEV_NO_SUPPORT);
    }
    sysfs_name = dfd_get_psu_sysfs_name();
    /* 电源E2产品名称转换 */
    if (cmd == DFD_DEV_INFO_TYPE_PART_NAME) {
        rv = dfd_get_psu_type(psu_index, i2c_dev, &power_type, sysfs_name);
        if (rv < 0) {
            DFD_PSU_DEBUG(DBG_ERROR, "psu get type error, rv: %d\n", rv);
            return -EIO;
        }
        rv = dfd_psu_product_name_decode(power_type, psu_buf, PSU_SIZE);
        if (rv < 0) {
            DFD_PSU_DEBUG(DBG_ERROR, "psu name decode error, power_type[0x%x] rv: %d\n",
                power_type, rv);
        }
    } else if (cmd == DFD_DEV_INFO_TYPE_FAN_DIRECTION) {
        rv = dfd_get_psu_type(psu_index, i2c_dev, &power_type, sysfs_name);
        if (rv < 0) {
            DFD_PSU_DEBUG(DBG_ERROR, "psu get type error, rv: %d\n", rv);
            return -EIO;
        }
        rv = dfd_psu_fan_direction_decode(power_type, psu_buf, PSU_SIZE);
        if (rv < 0) {
            DFD_PSU_DEBUG(DBG_ERROR, "psu input type decode error, power_type[0x%x] rv: %d\n",
                power_type, rv);
            return -EIO;
        }
    } else if (cmd == DFD_DEV_INFO_TYPE_MAX_OUTPUT_POWRER) {
        rv = dfd_get_psu_type(psu_index, i2c_dev, &power_type, sysfs_name);
        if (rv < 0) {
            DFD_PSU_DEBUG(DBG_ERROR, "psu get type error, rv:%d\n", rv);
            return -EIO;
        }
        rv = dfd_psu_max_output_power(power_type, psu_buf, PSU_SIZE);
        if (rv < 0) {
            DFD_PSU_DEBUG(DBG_ERROR, "psu max ouput power error, power_type[0x%x] rv: %d\n",
                power_type, rv);
            return -EIO;
        }
    } else if (cmd == DFD_DEV_INFO_TYPE_SPEED_MAX) {
        rv = dfd_get_psu_type(psu_index, i2c_dev, &power_type, sysfs_name);
        if (rv < 0) {
            DFD_PSU_DEBUG(DBG_ERROR, "psu get type error, rv:%d\n", rv);
            return -EIO;
        }
        rv = dfd_get_psu_fan_speed_max_str(power_type, psu_buf, PSU_SIZE);
        if (rv < 0) {
            DFD_PSU_DEBUG(DBG_ERROR, "psu fan speed max error, power_type[0x%x] rv: %d\n",
                power_type, rv);
            return -EIO;
        }
    } else if (cmd == DFD_DEV_INFO_TYPE_SPEED_MIN) {
        rv = dfd_get_psu_type(psu_index, i2c_dev, &power_type, sysfs_name);
        if (rv < 0) {
            DFD_PSU_DEBUG(DBG_ERROR, "psu get type error, rv:%d\n", rv);
            return -EIO;
        }
        rv = dfd_get_psu_fan_speed_min_str(power_type, psu_buf, PSU_SIZE);
        if (rv < 0) {
            DFD_PSU_DEBUG(DBG_ERROR, "psu fan speed min error, power_type[0x%x] rv: %d\n",
                power_type, rv);
            return -EIO;
        }
    } else if (cmd == DFD_DEV_INFO_TYPE_OUT_VOL_MAX) {
        rv = dfd_get_psu_type(psu_index, i2c_dev, &power_type, sysfs_name);
        if (rv < 0) {
            DFD_PSU_DEBUG(DBG_ERROR, "psu get type error, rv:%d\n", rv);
            return -EIO;
        }
        rv = dfd_get_psu_out_vol_max_str(power_type, psu_buf, PSU_SIZE);
        if (rv < 0) {
            DFD_PSU_DEBUG(DBG_ERROR, "psu fan out_vol max error, power_type[0x%x] rv: %d\n",
                power_type, rv);
            return -EIO;
        }
    } else if (cmd == DFD_DEV_INFO_TYPE_OUT_VOL_MIN) {
        rv = dfd_get_psu_type(psu_index, i2c_dev, &power_type, sysfs_name);
        if (rv < 0) {
            DFD_PSU_DEBUG(DBG_ERROR, "psu get type error, rv:%d\n", rv);
            return -EIO;
        }
        rv = dfd_get_psu_out_vol_min_str(power_type, psu_buf, PSU_SIZE);
        if (rv < 0) {
            DFD_PSU_DEBUG(DBG_ERROR, "psu fan out_vol min error, power_type[0x%x] rv: %d\n",
                power_type, rv);
            return -EIO;
        }
    } else {
        rv = dfd_get_fru_data(i2c_dev->bus, i2c_dev->addr, cmd, psu_buf, PSU_SIZE, sysfs_name);
        if (rv < 0) {
            DFD_PSU_DEBUG(DBG_ERROR, "psu eeprom read failed, rv: %d\n", rv);
            return -EIO;
        }
    }
    snprintf(buf, count, "%s\n", psu_buf);
    return strlen(buf);
}

/**
 * dfd_get_psu_input_type - 获取电源输入类型
 * @index: 电源的编号,从1开始
 * @buf: 接收buf
 * return: 成功：返回buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_psu_input_type(unsigned int psu_index, char *buf, size_t count)
{
    int ret;
    int data, key;

    if (buf == NULL) {
        DFD_PSU_DEBUG(DBG_ERROR, "buf is NULL, psu index: %u\n", psu_index);
        return -EINVAL;
    }
    if (count <= 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "buf size error, count: %lu, psu index: %u\n", count, psu_index);
        return -EINVAL;
    }

    key = DFD_CFG_KEY(DFD_CFG_ITEM_PSU_PMBUS_REG, psu_index, PSU_IN_TYPE);
    ret = dfd_info_get_int(key, &data, NULL);
    if (ret == -DFD_RV_DEV_NOTSUPPORT) {
        DFD_PSU_DEBUG(DBG_WARN, "get psu%u pmbus status info don't support\n", psu_index);
        return snprintf(buf, count, "%s\n", SWITCH_DEV_NO_SUPPORT);
    } else if (ret < 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "get psu%u pmbus status info failed, key: 0x%x, ret: %d\n", psu_index, key, ret);
        return -EIO;
    }

    DFD_PSU_DEBUG(DBG_VERBOSE, "psu_index: %u, pmbus_data = 0x%x \n", psu_index, data);

    if (data == DFD_PSU_PMBUS_TYPE_AC) {
        return snprintf(buf, count, "%d\n", DFD_PSU_SYSFS_TYPE_AC);
    } else if (data == DFD_PSU_PMBUS_TYPE_DC) {
        return snprintf(buf, count, "%d\n", DFD_PSU_SYSFS_TYPE_DC);
    } else {
        DFD_PSU_DEBUG(DBG_WARN, "get psu%u input type data[%u] unknow, ret: %d\n",
                psu_index, data, ret);
        return snprintf(buf, count, "%s\n", SWITCH_DEV_NO_SUPPORT);
    }

    DFD_PSU_DEBUG(DBG_ERROR, "get psu%u pmbus type data[%u] unknow, ret: %d\n",
        psu_index, data, ret);
    return -EIO;
}

/**
 * dfd_get_psu_in_status_str - 获取输入电源状态
 * @index: 电源的编号,从1开始
 * return: 成功:状态字符串长度
 *       : 负值 - 读取失败
 */
ssize_t dfd_get_psu_in_status_str(unsigned int psu_index, char *buf, size_t count)
{
    int ret, key;
    int pmbus_data;
    int input_status;

    if (buf == NULL) {
        DFD_PSU_DEBUG(DBG_ERROR, "buf is NULL, psu index: %u\n", psu_index);
        return -EINVAL;
    }
    if (count <= 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "buf size error, count: %lu, psu index: %u\n", count, psu_index);
        return -EINVAL;
    }

    key = DFD_CFG_KEY(DFD_CFG_ITEM_PSU_PMBUS_REG, psu_index, PSU_IN_STATUS);
    ret = dfd_info_get_int(key, &pmbus_data, NULL);
    if (ret == -DFD_RV_DEV_NOTSUPPORT) {
        DFD_PSU_DEBUG(DBG_WARN, "get psu%u pmbus status info don't support\n", psu_index);
        return snprintf(buf, count, "%s\n", SWITCH_DEV_NO_SUPPORT);
    } else if (ret < 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "get psu%u pmbus status info failed, key: 0x%x, ret: %d\n", psu_index, key, ret);
        return -EIO;
    }

    input_status = DFD_PSU_OK;
    if (pmbus_data & PSU_STATUS_WORD_INPUT) {
        /* no power的判断逻辑，按意见只判断bit13 */
        DFD_PSU_DEBUG(DBG_VERBOSE, "psu_index: %u, no power, pmbus_data = 0x%x \n", psu_index, pmbus_data);
        input_status = DFD_PSU_NOT_OK;
    }
    DFD_PSU_DEBUG(DBG_VERBOSE, "psu_index: %u, pmbus_data = 0x%x \n", psu_index, pmbus_data);

    memset(buf, 0, count);
    return (ssize_t)snprintf(buf, count, "%d\n", input_status);
}

ssize_t dfd_get_psu_output_status(unsigned int psu_index)
{
    int ret, output_key, output_status;

    output_key = DFD_CFG_KEY(DFD_CFG_ITEM_PSU_STATUS, psu_index, DFD_PSU_OUTPUT_STATUS);
    ret = dfd_info_get_int(output_key, &output_status, NULL);
    if (ret < 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "dfd_get_psu_output_status error. psu_index:%d, ret:%d\n",
            psu_index, ret);
        return ret;
    }

    DFD_PSU_DEBUG(DBG_VERBOSE, "dfd_get_psu_output_status success. psu_index:%d, status:%d\n",
        psu_index, output_status);
    return output_status;
}

ssize_t dfd_get_psu_alert_status(unsigned int psu_index)
{
    int ret, alert_key, alert_status;

    alert_key = DFD_CFG_KEY(DFD_CFG_ITEM_PSU_STATUS, psu_index, DFD_PSU_ALERT_STATUS);
    ret = dfd_info_get_int(alert_key, &alert_status, NULL);
    if (ret < 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "dfd_get_psu_alert_status error. psu_index:%d, ret:%d\n",
            psu_index, ret);
        return ret;
    }

    DFD_PSU_DEBUG(DBG_VERBOSE, "dfd_get_psu_alert_status success. psu_index:%d, status:%d\n",
        psu_index, alert_status);
    return alert_status;
}

ssize_t dfd_get_psu_alarm_status(unsigned int psu_index, char *buf, size_t count)
{
    int ret, key;
    int pmbus_data;
    int alarm;

    if (buf == NULL) {
        DFD_PSU_DEBUG(DBG_ERROR, "buf is NULL, psu index: %u\n", psu_index);
        return -EINVAL;
    }
    if (count <= 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "buf size error, count: %lu, psu index: %u\n", count, psu_index);
        return -EINVAL;
    }

    /* PMBUS STATUS WORD (0x79) */
    key = DFD_CFG_KEY(DFD_CFG_ITEM_PSU_PMBUS_REG, psu_index, PSU_OUT_STATUS);
    ret = dfd_info_get_int(key, &pmbus_data, NULL);
    if (ret == -DFD_RV_DEV_NOTSUPPORT) {
        DFD_PSU_DEBUG(DBG_WARN, "get psu%u pmbus status info don't support\n", psu_index);
        return snprintf(buf, count, "%s\n", SWITCH_DEV_NO_SUPPORT);
    } else if (ret < 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "get psu%u pmbus status info failed, key: 0x%x, ret: %d\n", psu_index, key, ret);
        return -EIO;
    }

    alarm = 0;
    if (pmbus_data & PSU_STATUS_WORD_TEMPERATURE) {
        DFD_PSU_DEBUG(DBG_VERBOSE, "psu%d PSU_TERMAL_ERROR, pmbus_data = 0x%x \n", psu_index, pmbus_data);
        alarm |= PSU_TERMAL_ERROR;
    }

    if (pmbus_data & PSU_STATUS_WORD_FANS) {
        DFD_PSU_DEBUG(DBG_VERBOSE, "psu%d PSU_FAN_ERROR, pmbus_data = 0x%x \n", psu_index, pmbus_data);
        alarm |= PSU_FAN_ERROR;
    }

    if (pmbus_data & PSU_VOLTAGE_ERR_OFFSET) {
        DFD_PSU_DEBUG(DBG_VERBOSE, "psu%d PSU_VOL_ERROR, pmbus_data = 0x%x \n", psu_index, pmbus_data);
        alarm |= PSU_VOL_ERROR;
    }
    DFD_PSU_DEBUG(DBG_VERBOSE, "psu_index: %u, pmbus_data = 0x%x \n", psu_index, pmbus_data);

    memset(buf, 0, count);
    return (ssize_t)snprintf(buf, count, "%d\n", alarm);
}


/**
 * dfd_get_psu_fan_ratio_str - 获取风扇目标转率
 * @index: 电源的编号,从1开始
 * return: 成功:状态字符串长度
 *       : 负值 - 读取失败
 */
ssize_t dfd_get_psu_fan_ratio_str(unsigned int psu_index, char *buf, size_t count)
{
    int ret, key;
    int pmbus_data;

    if (buf == NULL) {
        DFD_PSU_DEBUG(DBG_ERROR, "buf is NULL, psu index: %u\n", psu_index);
        return -EINVAL;
    }
    if (count <= 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "buf size error, count: %lu, psu index: %u\n", count, psu_index);
        return -EINVAL;
    }

    /* 从电源的pmbus寄存器获取状态 */
    key = DFD_CFG_KEY(DFD_CFG_ITEM_PSU_PMBUS_REG, psu_index, PSU_FAN_RATIO);
    ret = dfd_info_get_int(key, &pmbus_data, NULL);
    if (ret == -DFD_RV_DEV_NOTSUPPORT) {
        DFD_PSU_DEBUG(DBG_WARN, "get psu%u pmbus fan ratio don't support\n", psu_index);
        return snprintf(buf, count, "%s\n", SWITCH_DEV_NO_SUPPORT);
    } else if (ret < 0) {
        DFD_PSU_DEBUG(DBG_ERROR, "get psu%u pmbus fan ratio info failed, key: 0x%x, ret: %d\n", psu_index, key, ret);
        return -EIO;
    }

    memset(buf, 0, count);
    return (ssize_t)snprintf(buf, count, "%d\n", pmbus_data);
}
