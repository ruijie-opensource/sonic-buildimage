/*
 * Copyright(C) 2001-2012 Ruijie Network. All rights reserved.
 */
/*
 * rg_sff_driver.c
 * Original Author: sonic_rd@ruijie.com.cn 2020-02-17
 *
 * sff相关属性读写函数
 * History
 *  [Version]        [Author]                   [Date]            [Description]
 *   *  v1.0    sonic_rd@ruijie.com.cn         2020-02-17          Initial version
 */

#include <linux/module.h>

#include "./include/rg_module.h"
#include "./include/dfd_cfg.h"
#include "./include/dfd_cfg_info.h"
#include "./include/dfd_cfg_adapter.h"

int g_dfd_sff_dbg_level = 0;
module_param(g_dfd_sff_dbg_level, int, S_IRUGO | S_IWUSR);

/**
 * dfd_set_sff_cpld_info - 设置光模块CPLD寄存器状态
 * @sff_index: 光模块编号，从1开始
 * @cpld_reg_type: 光模块CPLD寄存器类型
 * @value: 写入寄存器的值
 * return: 成功：0
 *       ：失败：返回负值
 */
int dfd_set_sff_cpld_info(unsigned int sff_index, int cpld_reg_type, int value)
{
    int key, ret;

    if ((value != 0) && (value != 1)) {
        DFD_SFF_DEBUG(DBG_ERROR, "sff%u cpld reg type %d, can't set invalid value: %d\n",
            sff_index, cpld_reg_type, value);
        return -DFD_RV_INVALID_VALUE;
    }
    key = DFD_CFG_KEY(DFD_CFG_ITEM_SFF_CPLD_REG, sff_index, cpld_reg_type);
    ret = dfd_info_set_int(key, value);
    if (ret < 0) {
        DFD_SFF_DEBUG(DBG_ERROR, "set sff%u cpld reg type %d error, key: 0x%x, ret: %d.\n",
            sff_index, cpld_reg_type, key, ret);
        return ret;
    }

    return DFD_RV_OK;
}

/**
 * dfd_get_sff_cpld_info - 获取光模块CPLD寄存器状态
 * @sff_index: 光模块编号，从1开始
 * @cpld_reg_type: 光模块CPLD寄存器类型
 * @buf: 光模块E2信息接收buf
 * @count：buf长度
 * return: 成功：返回填充buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_get_sff_cpld_info(unsigned int sff_index, int cpld_reg_type, char *buf, size_t count)
{
    int key, ret, value;

    if (buf == NULL) {
        DFD_SFF_DEBUG(DBG_ERROR, "param error, buf is NULL. sff_index: %u, cpld_reg_type: %d\n",
            sff_index, cpld_reg_type);
        return -DFD_RV_INVALID_VALUE;
    }
    if (count <= 0) {
        DFD_SFF_DEBUG(DBG_ERROR, "buf size error, count: %lu, sff index: %u, cpld_reg_type: %d\n",
            count, sff_index, cpld_reg_type);
        return -DFD_RV_INVALID_VALUE;
    }
    memset(buf, 0 , count);
    key = DFD_CFG_KEY(DFD_CFG_ITEM_SFF_CPLD_REG, sff_index, cpld_reg_type);
    ret = dfd_info_get_int(key, &value, NULL);
    if (ret < 0) {
        DFD_SFF_DEBUG(DBG_ERROR, "get sff%u cpld reg type %d error, key: 0x%x, ret: %d\n",
            sff_index, cpld_reg_type, key, ret);
        if (ret == -DFD_RV_DEV_NOTSUPPORT) {
            return (ssize_t)snprintf(buf, count, "%s\n", SWITCH_DEV_NO_SUPPORT);
        }
        return ret;
    }
    return (ssize_t)snprintf(buf, count, "%d\n", value);
}


/**
 * dfd_get_eth_optoe_type - 获取光模块optoe类型
 * @sff_index: 光模块编号，从1开始
 * @optoe_type: 光模块optoe类型
 * return: 成功：0
 *       ：失败：返回负值
 */
int dfd_get_eth_optoe_type(unsigned int sff_index, int *optoe_type)
{
    int key, ret, value;

    key = DFD_CFG_KEY(DFD_CFG_ITEM_SFF_OPTOE_TYPE, sff_index, 0);
    ret = dfd_info_get_int(key, &value, NULL);
    if (ret < 0) {
        DFD_SFF_DEBUG(DBG_ERROR, "get sff optoe type error, key:0x%x,ret:%d.\n", key, ret);
        return ret;
    }

    /* assic int to int */
    *optoe_type = value - '0';
    return ret;
}

/**
 * dfd_set_eth_optoe_type - 设置光模块optoe类型
 * @sff_index: 光模块编号，从1开始
 * @optoe_type: 光模块optoe类型
 * return: 成功：0
 *       ：失败：返回负值
 */
int dfd_set_eth_optoe_type(unsigned int sff_index, int optoe_type)
{
    int key, ret, value;

    /* int to assic int */
    value = optoe_type + '0';
    key = DFD_CFG_KEY(DFD_CFG_ITEM_SFF_OPTOE_TYPE, sff_index, 0);
    ret = dfd_info_set_int(key, value);
    if (ret < 0) {
        DFD_SFF_DEBUG(DBG_ERROR, "set sff optoe type error, key:0x%x,ret:%d.\n", key, ret);
        return ret;
    }

    return ret;
}
