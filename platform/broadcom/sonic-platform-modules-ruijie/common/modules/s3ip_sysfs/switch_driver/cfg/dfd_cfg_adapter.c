/*
 * Copyright(C) 2015 Ruijie Network. All rights reserved.
 */
/*
 * dfd_cfg_adapter.c
 * Original Author:  sonic_rd@ruijie.com.cn 2020-02-17
 *
 * dfd内核模块产品适配
 *
 */

#include <linux/fs.h>
#include <linux/slab.h>
#include <asm/unistd.h>
#include <asm/uaccess.h>
#include <linux/types.h>
#include <linux/delay.h>
#include <linux/i2c.h>

#include "../include/rg_module.h"
#include "../include/dfd_cfg_file.h"
#include "../include/dfd_cfg.h"
#include "../include/dfd_cfg_adapter.h"

/* dfd_i2c_dev_t成员字符串 */
char *g_dfd_i2c_dev_mem_str[DFD_I2C_DEV_MEM_END] = {
    ".bus",
    ".addr",
};

static dfd_i2c_dev_t* dfd_ko_get_cpld_i2c_dev(int sub_slot, int cpld_id)
{
    int key;
    dfd_i2c_dev_t *i2c_dev;

    /* 读取配置值 */
    key = DFD_CFG_KEY(DFD_CFG_ITEM_CPLD_I2C_DEV, sub_slot, cpld_id);
    i2c_dev = dfd_ko_cfg_get_item(key);
    if (i2c_dev == NULL) {
        DBG_DEBUG(DBG_ERROR, "get cpld[%d] i2c dev config fail, key=0x%08x\n", cpld_id, key);
        return NULL;
    }

    return i2c_dev;
}

static int dfd_ko_i2c_block_read(int bus, int addr, int offset, uint8_t *buf, uint32_t size)
{
    struct file *fp;
    struct i2c_client client;
    int i;
    int rv = 0;
    char i2c_path[32];

    memset(i2c_path, 0, 32);
    snprintf(i2c_path, sizeof(i2c_path), "/dev/i2c-%d", bus);

    fp = filp_open(i2c_path, O_RDWR, S_IRUSR | S_IWUSR);
    if (IS_ERR(fp)) {
        DBG_DEBUG(DBG_ERROR, "i2c open fail.\n");
        return -1;
    }
    memcpy(&client, fp->private_data, sizeof(struct i2c_client));
    client.addr = addr;

    if (i2c_check_functionality(client.adapter, I2C_FUNC_SMBUS_READ_I2C_BLOCK)) {
        for (i = 0; i < size; i += 32) {
                rv = i2c_smbus_read_i2c_block_data(&client, offset + i, RG_MIN(32, size-i), buf + i);
                if (rv < 0) {
                    DBG_DEBUG(DBG_ERROR, "i2c_block read failed, rv = %d\n", rv);
                    rv = -DFD_RV_DEV_FAIL;
                    goto out;
                }
                if (rv != 32) {
                    break;
                }
        }
        rv = DFD_RV_OK;
    } else {
        rv = -DFD_RV_DEV_NOTSUPPORT;
    }

out:
    filp_close(fp, NULL);
    return rv;
}

static int32_t dfd_ko_i2c_smbus_transfer(int read_write, int bus, int addr, int offset, uint8_t *buf, uint32_t size)
{
    int rv;
    struct i2c_adapter *i2c_adap;
    union i2c_smbus_data data;

    i2c_adap = i2c_get_adapter(bus);
    if (i2c_adap == NULL) {
        DBG_DEBUG(DBG_ERROR, "get i2c bus[%d] adapter fail\n", bus);
        return -DFD_RV_DEV_FAIL;
    }

    /* 操作i2c */
    if (read_write == I2C_SMBUS_WRITE) {
        data.byte = *buf;
    } else {
        data.byte = 0;
    }
    rv = i2c_smbus_xfer(i2c_adap, addr, 0, read_write, offset, I2C_SMBUS_BYTE_DATA, &data);
    if (rv < 0) {
        DBG_DEBUG(DBG_ERROR, "i2c dev[bus=%d addr=0x%x offset=0x%x size=%d rw=%d] transfer fail, rv=%d\n",
            bus, addr, offset, size, read_write, rv);
        rv = -DFD_RV_DEV_FAIL;
    } else {
        DBG_DEBUG(DBG_VERBOSE, "i2c dev[bus=%d addr=0x%x offset=0x%x size=%d rw=%d] transfer success\n",
            bus, addr, offset, size, read_write);
        rv = DFD_RV_OK;
    }

    if (read_write == I2C_SMBUS_READ) {
        if (rv == DFD_RV_OK) {
            *buf = data.byte;
        } else {
            *buf = 0;
        }
    }

    i2c_put_adapter(i2c_adap);
    return rv;
}

static int32_t dfd_ko_i2c_read_bulk_data(int bus, int addr, int offset, uint8_t *buf, uint32_t size)
{
    int i, rv;
    for (i = 0; i < DFD_KO_CPLD_I2C_RETRY_TIMES; i++) {
        rv = dfd_ko_i2c_block_read(bus, addr, offset, buf, size);
        if (rv < 0) {
            DBG_DEBUG(DBG_ERROR, "[%d] read[offset=0x%x] fail, rv %d\r\n", i, addr, rv);
            msleep(DFD_KO_CPLD_I2C_RETRY_SLEEP);
        } else {
            DBG_DEBUG(DBG_VERBOSE, "[%d] read[offset=0x%x] success\r\n",
                i, addr);
            break;
        }
    }
    return rv;
}

static int32_t dfd_ko_i2c_read_data(int bus, int addr, int offset, uint8_t *buf, uint32_t size)
{
    int i, rv;
    for (i = 0; i < DFD_KO_CPLD_I2C_RETRY_TIMES; i++) {
        rv = dfd_ko_i2c_smbus_transfer(I2C_SMBUS_READ, bus, addr, offset, buf, size);
        if (rv < 0) {
            DBG_DEBUG(DBG_ERROR, "[%d]cpld read[offset=0x%x] fail, rv %d\n", i, addr, rv);
            msleep(DFD_KO_CPLD_I2C_RETRY_SLEEP);
        } else {
            DBG_DEBUG(DBG_VERBOSE, "[%d]cpld read[offset=0x%x] success, value=0x%x\n",
                i, addr, *buf);
            break;
        }
    }
    return rv;
}

static int32_t dfd_ko_i2c_write_data(int bus, int addr, int offset, uint8_t data, uint32_t size)
{
    int i, rv;
    for (i = 0; i < DFD_KO_CPLD_I2C_RETRY_TIMES; i++) {
        rv = dfd_ko_i2c_smbus_transfer(I2C_SMBUS_WRITE, bus, addr, offset, &data, size);
        if (rv < 0) {
            DBG_DEBUG(DBG_ERROR, "[%d]cpld write[offset=0x%x] fail, rv=%d\n", i, addr, rv);
            msleep(DFD_KO_CPLD_I2C_RETRY_SLEEP);
        } else {
            DBG_DEBUG(DBG_VERBOSE, "[%d]cpld write[offset=0x%x, data=%d] success\n", i, addr, data);
            break;
        }
    }

    return rv;
}

/**
 * dfd_ko_cpld_i2c_read - cpld读操作
 * @offset: 偏移地址
 * @buf: 数据
 *
 * @returns: <0失败，其他成功
 */
static int32_t dfd_ko_cpld_i2c_read(int32_t addr, uint8_t *buf)
{
    int rv;
    int sub_slot, cpld_id, cpld_addr;
    dfd_i2c_dev_t *i2c_dev;

    if (buf == NULL) {
        DBG_DEBUG(DBG_ERROR, "input arguments error\n");
        return -DFD_RV_INDEX_INVALID;
    }

    /* 获取i2c设备bus addr */
    sub_slot = DFD_KO_CPLD_GET_SLOT(addr);
    cpld_id = DFD_KO_CPLD_GET_ID(addr);
    cpld_addr = DFD_KO_CPLD_GET_INDEX(addr);

    i2c_dev = dfd_ko_get_cpld_i2c_dev(sub_slot, cpld_id);
    if (i2c_dev == NULL) {
        return -DFD_RV_DEV_NOTSUPPORT;
    }
    rv = dfd_ko_i2c_read_data(i2c_dev->bus, i2c_dev->addr, cpld_addr, buf, sizeof(uint8_t));

    return rv;
}

/**
 * dfd_ko_cpld_i2c_write - cpld写操作
 * @offset: 偏移地址
 * @data: 数据
 *
 * @returns: <0失败，其他成功
 */
static int32_t dfd_ko_cpld_i2c_write(int32_t addr, uint8_t data)
{
    int rv;
    int sub_slot, cpld_id, cpld_addr;
    dfd_i2c_dev_t *i2c_dev;

    /* 获取i2c设备bus addr */
    sub_slot = DFD_KO_CPLD_GET_SLOT(addr);
    cpld_id = DFD_KO_CPLD_GET_ID(addr);
    cpld_addr = DFD_KO_CPLD_GET_INDEX(addr);

    i2c_dev = dfd_ko_get_cpld_i2c_dev(sub_slot, cpld_id);
    if (i2c_dev == NULL) {
        return -DFD_RV_DEV_NOTSUPPORT;
    }

    rv = dfd_ko_i2c_write_data(i2c_dev->bus, i2c_dev->addr, cpld_addr, data, sizeof(uint8_t));

    return rv;
}

/**
 * dfd_ko_cpld_io_read - cpld io空间读操作
 * @addr: 地址
 * @buf: 数据
 *
 * @returns: <0失败，其他成功
 */
static int32_t dfd_ko_cpld_io_read(int32_t addr, uint8_t *buf)
{
    int cpld_id, sub_slot, offset;
    int key;
    int *tmp;
    uint16_t io_port;

    sub_slot = DFD_KO_CPLD_GET_SLOT(addr);
    cpld_id = DFD_KO_CPLD_GET_ID(addr);
    offset = DFD_KO_CPLD_GET_INDEX(addr);

    /* int类型配置项 */
    key = DFD_CFG_KEY(DFD_CFG_ITEM_CPLD_LPC_DEV, sub_slot, cpld_id);
    tmp = dfd_ko_cfg_get_item(key);
    if (tmp == NULL) {
        DBG_DEBUG(DBG_ERROR,"get cpld io base config fail, key=0x%08x\n", key);
        return -DFD_RV_DEV_NOTSUPPORT;
    }

    io_port = (u16)(*tmp) + offset;
    *buf = inb(io_port);
    DBG_DEBUG(DBG_VERBOSE, "read cpld io port addr 0x%x, data 0x%x\n", io_port, *buf);

    return DFD_RV_OK;

}

/**
 * dfd_ko_cpld_io_write - cpld io空间写操作
 * @addr: 地址
 * @data: 数据
 *
 * @returns: <0失败，其他成功
 */
static int32_t dfd_ko_cpld_io_write(int32_t addr, uint8_t data)
{
    int cpld_id, sub_slot, offset;
    int key;
    int *tmp;
    uint16_t io_port;

    sub_slot = DFD_KO_CPLD_GET_SLOT(addr);
    cpld_id = DFD_KO_CPLD_GET_ID(addr);
    offset = DFD_KO_CPLD_GET_INDEX(addr);

    /* int类型配置项 */
    key = DFD_CFG_KEY(DFD_CFG_ITEM_CPLD_LPC_DEV, sub_slot, cpld_id);
    tmp = dfd_ko_cfg_get_item(key);
    if (tmp == NULL) {
        DBG_DEBUG(DBG_ERROR, "get cpld io base config fail, key=0x%08x\n", key);
        return -1;
    }

    io_port = (u16)(*tmp) + offset;
    DBG_DEBUG(DBG_VERBOSE, "write cpld io port addr 0x%x, data 0x%x\n", io_port, data);
    outb(data, (u16)io_port);

    return DFD_RV_OK;
}

static int dfd_cfg_get_cpld_mode(int sub_slot, int cpld_id, int *mode)
{
    int key;
    char *name;

    if (mode == NULL) {
        DBG_DEBUG(DBG_ERROR, "input arguments error\n");
        return -DFD_RV_TYPE_ERR;
    }

    /* string类型配置项 */
    key = DFD_CFG_KEY(DFD_CFG_ITEM_CPLD_MODE, sub_slot, cpld_id);
    name = dfd_ko_cfg_get_item(key);
    if (name == NULL) {
        DBG_DEBUG(DBG_ERROR, "get cpld[%d] mode info ctrl fail, key=0x%08x\n", cpld_id, key);
        return -DFD_RV_DEV_NOTSUPPORT;
    }

    DBG_DEBUG(DBG_VERBOSE, "cpld_id %d mode_name %s.\n", cpld_id, name);
    if (!strncmp(name, DFD_KO_CPLD_MODE_I2C_STRING, strlen(DFD_KO_CPLD_MODE_I2C_STRING))) {
        *mode = DFD_CPLD_MODE_I2C;
    } else if (!strncmp(name, DFD_KO_CPLD_MODE_LPC_STRING, strlen(DFD_KO_CPLD_MODE_LPC_STRING))) {
        *mode = DFD_CPLD_MODE_LPC;
    } else {
        /* 缺省返回I2C模式 */
        *mode = DFD_CPLD_MODE_I2C;
    }

    DBG_DEBUG(DBG_VERBOSE, "cpld_id %d mode %d.\n", cpld_id, *mode);
    return 0;
}

/**
 * dfd_ko_cpld_read - cpld读操作,只读一个字节
 * @offset: 偏移地址
 * @buf: 数据
 *
 * @returns: <0失败，其他成功
 */
int32_t dfd_ko_cpld_read(int32_t addr, uint8_t *buf)
{
    int ret;
    int sub_slot, cpld_id;
    int cpld_mode;

    sub_slot = DFD_KO_CPLD_GET_SLOT(addr);
    cpld_id = DFD_KO_CPLD_GET_ID(addr);
    /* cpld模式，有I2C和LPC，其他暂不支持 */
    ret = dfd_cfg_get_cpld_mode(sub_slot, cpld_id, &cpld_mode);
    if (ret) {
        DBG_DEBUG(DBG_WARN, "drv_get_cpld_mode sub_slot %d cpldid %d faile, set default i2c mode.\n", sub_slot, cpld_id);
        cpld_mode = DFD_CPLD_MODE_I2C;
    }

    if (cpld_mode == DFD_CPLD_MODE_I2C) {
        ret = dfd_ko_cpld_i2c_read(addr, buf);
    } else if (cpld_mode == DFD_CPLD_MODE_LPC) {
        ret = dfd_ko_cpld_io_read(addr, buf);
    } else {
        DBG_DEBUG(DBG_ERROR, "cpld_mode %d invalid.\n", cpld_mode);
        ret = -DFD_RV_DEV_NOTSUPPORT;
    }

    DBG_DEBUG(DBG_VERBOSE, "addr 0x%x val 0x%x ret %d\n", addr, *buf, ret);
    return ret;
}

/**
 * dfd_ko_cpld_write - cpld写操作 写一个字节
 * @offset: 偏移地址
 * @data: 数据
 *
 * @returns: <0失败，其他成功
 */
int32_t dfd_ko_cpld_write(int32_t addr, uint8_t val)
{
    int ret;
    int sub_slot, cpld_id, cpld_mode;

    sub_slot = DFD_KO_CPLD_GET_SLOT(addr);
    cpld_id = DFD_KO_CPLD_GET_ID(addr);

    ret = dfd_cfg_get_cpld_mode(sub_slot, cpld_id, &cpld_mode);
    if (ret) {
        DBG_DEBUG(DBG_ERROR, "drv_get_cpld_mode sub_slot %d cpldid %d faile, set default local_bus mode.\n", sub_slot, cpld_id);
        cpld_mode = DFD_CPLD_MODE_I2C;
    }

    if (cpld_mode == DFD_CPLD_MODE_I2C) {
        ret = dfd_ko_cpld_i2c_write(addr, val);
    } else if (cpld_mode == DFD_CPLD_MODE_LPC) {
        ret = dfd_ko_cpld_io_write(addr, val);
    } else {
        DBG_DEBUG(DBG_ERROR, "cpld_mode %d invalid.\n", cpld_mode);
        ret = -DFD_RV_MODE_INVALID;
    }

    DBG_DEBUG(DBG_VERBOSE, "addr 0x%x val 0x%x ret %d\n", addr, val, ret);
    return ret;
}

/**
 * dfd_ko_i2c_read_tmp - I2C 读操作
 * @bus: I2C通道
 * @addr: I2C设备地址
 * @offset：寄存器偏移
 * @buf：读缓冲区
 * @size：读数据长度
 * @returns: <0失败，其他成功
 */
static int32_t dfd_ko_i2c_read_tmp(int bus, int addr, int offset, uint8_t *buf, uint32_t size)
{
    int i, rv;

    for (i = 0; i < size; i++) {
        rv = dfd_ko_i2c_read_data(bus, addr, offset, &buf[i], sizeof(uint8_t));
        if (rv < 0) {
            DBG_DEBUG(DBG_ERROR, "dfd_ko_i2c_read_data[bus=%d addr=0x%x offset=0x%x]fail, rv=%d\n",
                bus, addr, offset, rv);
            return rv;
        }
        offset++;
    }

    return size;
}

/**
 * dfd_ko_i2c_write - I2C 写操作
 * @bus: I2C通道
 * @addr: I2C设备地址
 * @offset：寄存器偏移
 * @buf：写缓冲区
 * @size：写入长度
 * @returns: <0失败，其他成功
 */
int32_t dfd_ko_i2c_write(int bus, int addr, int offset, uint8_t *buf, uint32_t size)
{
    int i, rv;

    for (i = 0; i < size; i++) {
        rv = dfd_ko_i2c_write_data(bus, addr, offset, buf[i], sizeof(uint8_t));
        if (rv < 0) {
            DBG_DEBUG(DBG_ERROR, "dfd_ko_i2c_write[bus=%d addr=0x%x offset=0x%x]fail, rv=%d\n",
                bus, addr, offset, rv);
            return rv;
        }
        offset++;
    }

    return size;

}

/**
 * dfd_ko_read_file - 文件读操作
 * @fpath: 文件路径
 * @addr: 地址
 * @val: 数据
 * @read_bytes: 长度
 *
 * @returns: <0失败，其他成功
 */
int32_t dfd_ko_read_file(char *fpath, int32_t addr, uint8_t *val, int32_t read_bytes)
{
    int32_t ret;
    struct file *filp;
    loff_t pos;

    if ((fpath == NULL) || (val == NULL) || (addr < 0) || (read_bytes < 0)) {
        DBG_DEBUG(DBG_ERROR, "input arguments error, addr=%d read_bytes=%d\n", addr, read_bytes);
        return -DFD_RV_INDEX_INVALID;
    }

    /* 打开文件 */
    filp = filp_open(fpath, O_RDONLY, 0);
    if (IS_ERR(filp)){
        DBG_DEBUG(DBG_ERROR, "open file[%s] fail\n", fpath);
        return -DFD_RV_DEV_FAIL;
    }
    /* 定位文件 */
    pos = addr;
    ret = kernel_read(filp, val, read_bytes, &pos);
    if (ret < 0) {
        DBG_DEBUG(DBG_ERROR, "kernel_read failed, path=%s, addr=%d, size=%d, ret=%d\n", fpath, addr, read_bytes, ret);
        ret = -DFD_RV_DEV_FAIL;
    }
    filp_close(filp, NULL);
    return ret;
}

/**
 * dfd_ko_other_i2c_dev_read - other_i2c读操作
 * @addr: 地址
 * @val: 数据
 * @read_len: 长度
 *
 * @returns: <0失败，其他成功
 */
int32_t dfd_ko_other_i2c_dev_read(int32_t addr, uint8_t *value, int32_t read_len)
{
    int rv;
    int key, e2p_main_id, e2p_index, e2p_addr;
    dfd_i2c_dev_t *i2c_dev;

    if ((value == NULL) || (read_len <= 0)) {
        DBG_DEBUG(DBG_ERROR, "input arguments error, read_len=%d\r\n", read_len);
        return -1;    
    }

    e2p_main_id = DFD_KO_OTHER_I2C_GET_MAIN_ID(addr);
    e2p_index = DFD_KO_OTHER_I2C_GET_INDEX(addr);
    e2p_addr = DFD_KO_OTHER_I2C_GET_OFFSET(addr);

    key = DFD_CFG_KEY(DFD_CFG_ITEM_OTHER_I2C_DEV, e2p_main_id, e2p_index);
    i2c_dev = dfd_ko_cfg_get_item(key);
    if (i2c_dev == NULL) {
        DBG_DEBUG(DBG_ERROR, "psu i2c dev config error, key=0x%08x\r\n", key);
        return -DFD_RV_NODE_FAIL;
    }

    rv = dfd_ko_i2c_read_bulk_data(i2c_dev->bus, i2c_dev->addr, e2p_addr, value, read_len);
    DBG_DEBUG(DBG_VERBOSE, "dfd_ko_other_i2c_dev_read, value[0] = 0x%x\n", value[0]);
    DBG_DEBUG(DBG_VERBOSE, "dfd_ko_other_i2c_dev_read, value[1] = 0x%x\n", value[1]);
    return rv;
}

/**
 * dfd_ko_i2c_read - I2C 读操作
 * @bus: I2C通道
 * @addr: I2C设备地址
 * @offset：寄存器偏移
 * @buf：读缓冲区
 * @size：读数据长度
 * @sysfs_name：sysfs属性名称
 * @returns: <0失败，其他成功
 */
int32_t dfd_ko_i2c_read(int bus, int addr, int offset, uint8_t *buf, uint32_t size, const char *sysfs_name)
{
    int rv;
    char sysfs_path[DFD_SYSFS_PATH_MAX_LEN];

    if (buf == NULL) {
        DBG_DEBUG(DBG_ERROR, "params error, buf is NULL.\n");
        return -DFD_RV_INVALID_VALUE;
    }

    if (sysfs_name == NULL) {   /* 通过i2c的方式读取 */
        DBG_DEBUG(DBG_VERBOSE, "using i2c_smbus_xfer, bus:%d, addr:0x%x, offset:0x%x, read size:%d.\n",
            bus, addr, offset, size);
        rv = dfd_ko_i2c_read_tmp(bus, addr, offset, buf, size);
    } else {    /* 通过sysfs读取 */
        memset(sysfs_path, 0, sizeof(sysfs_path));
        snprintf(sysfs_path, sizeof(sysfs_path), "/sys/bus/i2c/devices/%d-%04x/%s",
            bus, addr, sysfs_name);
        DBG_DEBUG(DBG_VERBOSE, "using sysfs, sysfs_path:%s, offset:0x%x, read size:%d.\n",
            sysfs_path, offset, size);
        rv = dfd_ko_read_file(sysfs_path, offset, buf, size);
    }

    if (rv < 0) {
        DBG_DEBUG(DBG_ERROR, "dfd_ko_i2c_read failed.\n");
    } else {
        DBG_DEBUG(DBG_VERBOSE, "dfd_ko_i2c_read success.\n");
    }

    return rv;
}

/**
 * dfd_ko_write_file - 文件写操作
 * @fpath: 文件路径
 * @addr: 地址
 * @val: 数据
 * @write_bytes: 长度
 *
 * @returns: <0失败，其他成功
 */
int32_t dfd_ko_write_file(char *fpath, int32_t addr, uint8_t *val, int32_t write_bytes)
{
    int32_t ret;
    struct file *filp;
    loff_t pos;

    if ((fpath == NULL) || (val == NULL) || (addr < 0) || (write_bytes <= 0)) {
        DBG_DEBUG(DBG_ERROR, "input arguments error, addr=%d write_bytes=%d\n", addr, write_bytes);
        return -DFD_RV_INDEX_INVALID;
    }

    /* 打开文件 */
    filp = filp_open(fpath, O_WRONLY, 0);
    if (IS_ERR(filp)) {
        DBG_DEBUG(DBG_ERROR, "open file[%s] fail\n", fpath);
        return -DFD_RV_DEV_FAIL;
    }
    /* 定位文件 */
    pos = addr;
    ret = kernel_write(filp, val, write_bytes, &pos);
    if (ret < 0) {
        DBG_DEBUG(DBG_ERROR,"kernel_write failed, path=%s, addr=%d, size=%d, ret=%d\n", fpath, addr, write_bytes, ret);
        ret = -DFD_RV_DEV_FAIL;
    }

    filp_close(filp, NULL);
    return ret;
}
