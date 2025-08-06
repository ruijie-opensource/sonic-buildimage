/*
 * Copyright(C) 2001-2012 Ruijie Network. All rights reserved.
 */
/*
 * rg_eeprom_driver.c
 * Original Author: sonic_rd@ruijie.com.cn 2020-02-17
 *
 * eeprom相关属性读写函数
 * History
 *  [Version]        [Author]                   [Date]            [Description]
 *   *  v1.0    sonic_rd@ruijie.com.cn         2020-02-17          Initial version
 */

#include <linux/module.h>

#include "./include/rg_module.h"
#include "./include/dfd_cfg.h"
#include "./include/dfd_cfg_adapter.h"
#include "./include/dfd_tlveeprom.h"

int g_dfd_eeprom_dbg_level = 0;
module_param(g_dfd_eeprom_dbg_level, int, S_IRUGO | S_IWUSR);

/**
 * dfd_get_eeprom_size - 获取eeprom的数据大小
 * @e2_type: 区分E2类型，包括整机、电源、风扇、模块E2
 * @index: E2的编号
 * return: 成功: 返回eeprom的数据大小
 *       : 失败: 返回负值
 */
int dfd_get_eeprom_size(int e2_type, int index)
{
    int key;
    int *p_eeprom_size;

    /* 获取eeprom大小 */
    key = DFD_CFG_KEY(DFD_CFG_ITEM_EEPROM_SIZE, e2_type, index);

    p_eeprom_size = dfd_ko_cfg_get_item(key);
    if (p_eeprom_size == NULL) {
        DBG_EEPROM_DEBUG(DBG_ERROR, "get eeprom size error. key:0x%x\n", key);
        return -DFD_RV_DEV_NOTSUPPORT;
    }

    return *p_eeprom_size;
}

/**
 * dfd_read_eeprom_data - 读取eeprom数据
 * @e2_type: 区分E2类型，包括整机、电源、风扇、模块E2
 * @index: E2的编号
 * @buf: eeprom数据接收buf
 * @offset: 读取的偏移地址
 * @count：读取的长度
 * return: 成功：返回填充buf的长度
 *       ：失败：返回负值
 */
ssize_t dfd_read_eeprom_data(int e2_type, int index, char *buf, loff_t offset, size_t count)
{
    int key;
    ssize_t rd_len;
    char *eeprom_path;

    if (buf == NULL || offset < 0 || count <= 0) {
        DBG_EEPROM_DEBUG(DBG_ERROR, "params error, offset: 0x%llx, rd_count: %lu.\n",
            offset, count);
        return -DFD_RV_INVALID_VALUE;
    }

    /* 获取eeprom读取路径 */
    key = DFD_CFG_KEY(DFD_CFG_ITEM_EEPROM_PATH, e2_type, index);
    eeprom_path = dfd_ko_cfg_get_item(key);
    if (eeprom_path == NULL) {
        DBG_EEPROM_DEBUG(DBG_ERROR, "get eeprom path error, e2_type: %d, index: %d, key: 0x%08x\n",
            e2_type, index, key);
        return -DFD_RV_DEV_NOTSUPPORT;
    }

    DBG_EEPROM_DEBUG(DBG_VERBOSE, "e2_type: %d, index: %d, path: %s, offset: 0x%llx, \
        rd_count: %lu\n", e2_type, index, eeprom_path, offset, count);

    memset(buf, 0, count);
    rd_len = dfd_ko_read_file(eeprom_path, offset, buf, count);
    if (rd_len < 0) {
        DBG_EEPROM_DEBUG(DBG_ERROR, "read eeprom data failed, loc: %s, offset: 0x%llx, \
        rd_count: %lu, ret: %ld,\n", eeprom_path, offset, count, rd_len);
    } else {
        DBG_EEPROM_DEBUG(DBG_VERBOSE, "read eeprom data success, loc: %s, offset: 0x%llx, \
            rd_count: %lu, rd_len: %ld,\n", eeprom_path, offset, count, rd_len);
    }

    return rd_len;
}

/**
 * dfd_write_eeprom_data - 写eeprom数据
 * @e2_type: 区分E2类型，包括整机、电源、风扇、模块E2
 * @index: E2的编号
 * @buf: eeprom数据buf
 * @offset: 写入的偏移地址
 * @count：写入的长度
 * return: 成功：返回写入的数据长度
 *       ：失败：返回负值
 */
ssize_t dfd_write_eeprom_data(int e2_type, int index, char *buf, loff_t offset, size_t count)
{
    int key;
    ssize_t wr_len;
    char *eeprom_path;

    if (buf == NULL || offset < 0 || count <= 0) {
        DBG_EEPROM_DEBUG(DBG_ERROR, "params error, offset: 0x%llx, count: %lu.\n", offset, count);
        return -DFD_RV_INVALID_VALUE;
    }

    /* 获取eeprom读取路径 */
    key = DFD_CFG_KEY(DFD_CFG_ITEM_EEPROM_PATH, e2_type, index);
    eeprom_path = dfd_ko_cfg_get_item(key);
    if (eeprom_path == NULL) {
        DBG_EEPROM_DEBUG(DBG_ERROR, "get eeprom path error, e2_type: %d, index: %d, key: 0x%08x\n",
            e2_type, index, key);
        return -DFD_RV_DEV_NOTSUPPORT;
    }

    DBG_EEPROM_DEBUG(DBG_VERBOSE, "e2_type: %d, index: %d, path: %s, offset: 0x%llx, \
        wr_count: %lu.\n", e2_type, index, eeprom_path, offset, count);

    wr_len = dfd_ko_write_file(eeprom_path, offset, buf, count);
    if (wr_len < 0) {
        DBG_EEPROM_DEBUG(DBG_ERROR, "write eeprom data failed, loc:%s, offset: 0x%llx, \
            wr_count: %lu, ret: %ld.\n", eeprom_path, offset, count, wr_len);
    } else {
        DBG_EEPROM_DEBUG(DBG_VERBOSE, "write eeprom data success, loc:%s, offset: 0x%llx, \
            wr_count: %lu, wr_len: %ld.\n", eeprom_path, offset, count, wr_len);
    }

    return wr_len;
}