/*
 * Copyright(C) 2022 Ruijie Network. All rights reserved.
 * rg_ssd_power.c
 * Original Author: sonic_rd@ruijie.com.cn 2022-02-22
 *
 * This driver is used to power off/on SSD.
 *
 * History
 *  [Version]        [Author]                   [Date]            [Description]
 *   *  v1.0    sonic_rd@ruijie.com.cn         2022-02-22          Initial version
 */

#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/string.h>
#include <linux/mm.h>
#include <linux/of_platform.h>
#include <linux/delay.h>
#include <linux/slab.h>
#include <linux/kallsyms.h>
#include <linux/fs.h>
#include <asm/uaccess.h>
#include <linux/device.h>
#include <linux/platform_device.h>
#include <linux/kprobes.h>
#include "rg_ssd_power.h"

#define PROXY_NAME "rg-ssd-power"

#define SSD_POWER_MAX_NUM       (8)

#define SYMBOL_I2C_DEV_MODE     (1)   /* 通过I2C接口访问逻辑器件寄存器 */
#define FILE_MODE               (2)   /* 通过文件方式访问逻辑器件寄存器 */
#define SYMBOL_PCIE_DEV_MODE    (3)   /* 通过PCIe接口访问逻辑器件寄存器 */
#define SYMBOL_IO_DEV_MODE      (4)   /* 通过IO接口访问逻辑器件寄存器 */

typedef struct {
    uint32_t port_id;
    const char *file_name;
    uint32_t addr;
    uint32_t power_on;
    uint32_t power_off;
    uint32_t power_mask;
    uint32_t power_on_delay;
    uint32_t power_off_delay;
    uint32_t reg_access_mode;
    struct device *dev;
} ssd_power_node_t;

static ssd_power_node_t *g_ssd_power_n[SSD_POWER_MAX_NUM];


static int g_ssd_power_debug = 0;
static int g_ssd_power_error = 0;

module_param(g_ssd_power_debug, int, S_IRUGO | S_IWUSR);
module_param(g_ssd_power_error, int, S_IRUGO | S_IWUSR);


#define SSD_POWER_DEBUG(fmt, args...) do {                                        \
    if (g_ssd_power_debug) { \
        printk(KERN_DEBUG "[SSD_POWER][DEBUG][func:%s line:%d]\n"fmt, __func__, __LINE__, ## args); \
    } \
} while (0)

#define SSD_POWER_ERROR(fmt, args...) do {                                        \
    if (g_ssd_power_error) { \
        printk(KERN_ERR "[SSD_POWER][ERR][func:%s line:%d]\n"fmt, __func__, __LINE__, ## args); \
    } \
} while (0)

typedef int (*ata_power_reset_func_t)(unsigned int);
typedef int (*p_reg_ata_ssd_power_reset)(ata_power_reset_func_t power_reset_handle);
typedef int (*p_unreg_ata_ssd_power_reset)(void);
p_reg_ata_ssd_power_reset g_p_reg_ata_ssd_power_reset = NULL;
p_unreg_ata_ssd_power_reset g_p_unreg_ata_ssd_power_reset = NULL;

static int noop_pre(struct kprobe *p, struct pt_regs *regs) { return 0; }
static struct kprobe kp = {   
	.symbol_name = "kallsyms_lookup_name",  
};
unsigned long (*kallsyms_lookup_name_fun)(const char *name) = NULL;


extern int i2c_device_func_write(const char *path, uint32_t offset, uint8_t *buf, size_t count);
extern int i2c_device_func_read(const char *path, uint32_t offset, uint8_t *buf, size_t count);
extern int pcie_device_func_read(const char *path, uint32_t offset, uint8_t *buf, size_t count);
extern int pcie_device_func_write(const char *path, uint32_t offset, uint8_t *buf, size_t count);
extern int io_device_func_read(const char *path, uint32_t offset, uint8_t *buf, size_t count);
extern int io_device_func_write(const char *path, uint32_t offset, uint8_t *buf, size_t count);

/* 调用kprobe找到kallsyms_lookup_name的地址位置 */
static int find_kallsyms_lookup_name(void)
{ 
    int ret = -1;

	kp.pre_handler = noop_pre;
	ret = register_kprobe(&kp);
    if (ret < 0) {  
	    SSD_POWER_ERROR("register_kprobe failed, error:%d\n", ret); 
        return ret; 
	}
	SSD_POWER_DEBUG("kallsyms_lookup_name addr: %p\n", kp.addr); 
	kallsyms_lookup_name_fun = (void*)kp.addr; 
	unregister_kprobe(&kp);
    
	return ret;
}

static int rg_dev_file_read(const char *path, uint32_t pos, uint8_t *val, size_t size)
{
    int ret;
    struct file *filp;
    loff_t tmp_pos;

    filp = filp_open(path, O_RDONLY, 0);
    if (IS_ERR(filp)) {
        SSD_POWER_ERROR("read open failed errno = %ld\r\n", -PTR_ERR(filp));
        filp = NULL;
        goto exit;
    }
    ret = 0;
    tmp_pos = (loff_t)pos;
    ret = kernel_read(filp, val, size, &tmp_pos);
    if (ret < 0) {
        SSD_POWER_ERROR("read kernel_read failed, ret=%d\r\n", ret);
        goto exit;
    }
    filp_close(filp, NULL);

    return ret;

exit:
    if (filp != NULL) {
        filp_close(filp, NULL);
    }

    return -1;
}

static int rg_dev_file_write(const char *path, uint32_t pos, uint8_t *val, size_t size)
{
    int ret;
    struct file *filp;
    loff_t tmp_pos;

    filp = filp_open(path, O_RDWR, 777);
    if (IS_ERR(filp)) {
        SSD_POWER_ERROR("write open failed errno = %ld\r\n", -PTR_ERR(filp));
        filp = NULL;
        goto exit;
    }
    ret = 0;
    tmp_pos = (loff_t)pos;
    ret = kernel_write(filp, (void*)val, size, &tmp_pos);
    if (ret < 0) {
        SSD_POWER_ERROR("write kernel_write failed, ret=%d\r\n", ret);
        goto exit;
    }
    vfs_fsync(filp, 1);
    filp_close(filp, NULL);

    return ret;

exit:
    if (filp != NULL) {
        filp_close(filp, NULL);
    }

    return -1;
}

static int rg_logic_reg_write(ssd_power_node_t *node, uint32_t pos, uint8_t *val, size_t size)
{
    int ret;

    switch (node->reg_access_mode) {
    case SYMBOL_I2C_DEV_MODE:        /* 使用i2c设备器件驱动模式 */
        ret = i2c_device_func_write(node->file_name, pos, val, size);
        break;
    case FILE_MODE:                  /* 文件访问模式 */
        ret = rg_dev_file_write(node->file_name, pos, val, size);
        break;
    case SYMBOL_PCIE_DEV_MODE:       /* 使用pcie设备器件驱动模式 */
        ret = pcie_device_func_write(node->file_name, pos, val, size);
        break;
    case SYMBOL_IO_DEV_MODE:         /* 使用io设备器件驱动模式 */
        ret = io_device_func_write(node->file_name, pos, val, size);
        break;
    default:
        SSD_POWER_ERROR("error mode %u, write %s addr: 0x%x, failed.\n",
            node->reg_access_mode, node->file_name, pos);
        return -EINVAL;
    }

    return ret;
}

static int rg_logic_reg_read(ssd_power_node_t *node, uint32_t pos, uint8_t *val, size_t size)
{
    int ret;

    switch (node->reg_access_mode) {
    case SYMBOL_I2C_DEV_MODE:        /* 使用i2c设备器件驱动模式 */
        ret = i2c_device_func_read(node->file_name, pos, val, size);
        break;
    case FILE_MODE:                  /* 文件访问模式 */
        ret = rg_dev_file_read(node->file_name, pos, val, size);
        break;
    case SYMBOL_PCIE_DEV_MODE:       /* 使用pcie设备器件驱动模式 */
        ret = pcie_device_func_read(node->file_name, pos, val, size);
        break;
    case SYMBOL_IO_DEV_MODE:         /* 使用io设备器件驱动模式 */
        ret = io_device_func_read(node->file_name, pos, val, size);
        break;
    default:
        SSD_POWER_ERROR("error mode %u, read %s addr: 0x%x failed.\n",
            node->reg_access_mode, node->file_name, pos);
        return -EINVAL;
    }

    return ret;
}


static int rg_ssd_power_ctrl(ssd_power_node_t *node, int on)
{
    uint8_t power_ops;
    int ret;

    /* read origin register value */
    ret = rg_logic_reg_read(node, node->addr, &power_ops, 1);
    if (ret < 0) {
        SSD_POWER_ERROR("read %s, addr: 0x%x failed, ret: %d\n", node->file_name,
            node->addr, ret);
        return -EIO;
    }
    SSD_POWER_DEBUG("read %s addr 0x%x success, value: 0x%x\n",
        node->file_name, node->addr, power_ops);

    /* modify register value to ssd power control */
    power_ops &= ~(node->power_mask);
    if (on == 0) {
        power_ops |= node->power_off;
    } else {
        power_ops |= node->power_on;
    }

    /* write back to register */
    ret = rg_logic_reg_write(node, node->addr, &power_ops, 1);
    if (ret < 0) {
        SSD_POWER_ERROR("write %s, addr: 0x%x failed, ret: %d write value: 0x%x\n",
            node->file_name, node->addr, ret, power_ops);
        return -EIO;
    }
    SSD_POWER_DEBUG("write %s addr 0x%x value: 0x%x success\n",
        node->file_name, node->addr, power_ops);
    if ((on == 0) && (node->power_off_delay != 0)) {
        msleep(node->power_off_delay);
    } else if ((on != 0) && (node->power_on_delay != 0)) {
        msleep(node->power_on_delay);
    }

    return 0;
}

static int rg_ssd_power_reset(unsigned int port_id)
{
    ssd_power_node_t *node;
    int ret;

    if (port_id >= SSD_POWER_MAX_NUM) {
        printk(KERN_ERR "Invalid param, port_id[%u] greater than the maximum value %d, power reset failed.\n",
            port_id, SSD_POWER_MAX_NUM);
        return -EINVAL;
    }

    if (g_ssd_power_n[port_id] == NULL) {
        printk(KERN_ERR "SSD%u power reset node is NULL, power reset failed.\n", port_id);
        return -EINVAL;
    }

    node = g_ssd_power_n[port_id];

    dev_dbg(node->dev, "SSD%u power reset start\n", port_id);
    ret = rg_ssd_power_ctrl(node, 0);
    if (ret != 0) {
        dev_err(node->dev, "SSD%u power off failed, ret: %d\n", port_id, ret);
        return ret;
    }

    ret = rg_ssd_power_ctrl(node, 1);
    if (ret != 0) {
        dev_err(node->dev, "SSD%u power on failed, ret: %d\n", port_id, ret);
        return ret;
    }
    dev_info(node->dev, "SSD%u power reset success\n", port_id);
    return 0;
}

static void rg_ssd_power_node_destroy(void)
{
    int i;

    for (i = 0; i < SSD_POWER_MAX_NUM; i++) {
        if (g_ssd_power_n[i] != NULL) {
            g_ssd_power_n[i] = NULL;
        }
    }
    return;
}

static int rg_ssd_power_config_init(ssd_power_node_t *node)
{
    int ret;
    struct device *dev;
    ssd_power_device_t *ssd_power_device;

    dev = node->dev;
    if (dev->of_node) {
        ret = 0;
        ret += of_property_read_u32(node->dev->of_node, "port_id", &node->port_id);
        ret += of_property_read_u32(node->dev->of_node, "addr", &node->addr);
        ret += of_property_read_u32(node->dev->of_node, "power_on", &node->power_on);
        ret += of_property_read_u32(node->dev->of_node, "power_off", &node->power_off);
        ret += of_property_read_u32(node->dev->of_node, "power_mask", &node->power_mask);
        ret += of_property_read_u32(node->dev->of_node, "power_on_delay", &node->power_on_delay);
        ret += of_property_read_u32(node->dev->of_node, "power_off_delay", &node->power_off_delay);
        ret += of_property_read_string(node->dev->of_node, "file_name", &node->file_name);
        ret += of_property_read_u32(node->dev->of_node, "reg_access_mode", &node->reg_access_mode);
        if (ret != 0) {
            SSD_POWER_ERROR("get ssd power control dts config error, ret: %d\n", ret);
            return -ENXIO;
        }
    } else {
        if (dev->platform_data == NULL) {
            SSD_POWER_ERROR("Failed to priv platform data \n");
            return -ENXIO;
        }
        ssd_power_device = node->dev->platform_data;
        node->port_id = ssd_power_device->port_id;
        node->addr = ssd_power_device->addr;
        node->power_on = ssd_power_device->power_on;
        node->power_off = ssd_power_device->power_off;
        node->power_mask = ssd_power_device->power_mask;
        node->power_on_delay = ssd_power_device->power_on_delay;
        node->power_off_delay = ssd_power_device->power_off_delay;
        node->file_name = ssd_power_device->file_name;
        node->reg_access_mode = ssd_power_device->reg_access_mode;
        ret = 0;
    }
    SSD_POWER_DEBUG("rg_ssd_power_config_init success");
    return ret;
}

static int rg_ssd_power_probe(struct platform_device *pdev)
{
    ssd_power_node_t *ssd_power;
    int ret;
    uint32_t port_id;

    SSD_POWER_DEBUG("rg_ssd_power_init\n");

    ssd_power = devm_kzalloc(&pdev->dev, sizeof(ssd_power_node_t), GFP_KERNEL);
    if (!ssd_power) {
        dev_err(&pdev->dev, "devm_kzalloc error.\n");
        return -ENOMEM;
    }

    platform_set_drvdata(pdev, ssd_power);
    ssd_power->dev = &pdev->dev;

    ret = rg_ssd_power_config_init(ssd_power);
    if (ret !=0) {
        dev_err(ssd_power->dev, "Failed to get ssd power control dts config, ret: %d\n", ret);
        return -ENXIO;
    }

    port_id = ssd_power->port_id;
    if (port_id >= SSD_POWER_MAX_NUM) {
        dev_err(ssd_power->dev, "Port id %u, beyond the limit.\n", ssd_power->port_id);
        return -EINVAL;
    }
    g_ssd_power_n[port_id] = ssd_power;

    dev_info(ssd_power->dev, "Register ssd%u power control using mode %u with %s offset address 0x%x power off delay %u ms, power on delay %u ms success.\n",
        ssd_power->port_id, ssd_power->reg_access_mode, ssd_power->file_name, ssd_power->addr, ssd_power->power_off_delay, ssd_power->power_on_delay);
    return 0;
}

static int rg_ssd_power_remove(struct platform_device *pdev)
{
    ssd_power_node_t *ssd_power;
    uint32_t port_id;

    ssd_power = platform_get_drvdata(pdev);
    port_id = ssd_power->port_id;
    g_ssd_power_n[port_id] = NULL;
    dev_info(ssd_power->dev, "Remove ssd%u power control success.\n", ssd_power->port_id);
    platform_set_drvdata(pdev, NULL);
    return 0;
}

static const struct of_device_id rg_ssd_power_driver_of_match[] = {
    { .compatible = "ruijie,rg-ssd-power" },
    { },
};
MODULE_DEVICE_TABLE(of, rg_ssd_power_driver_of_match);

static struct platform_driver rg_ssd_power_driver = {
    .probe      = rg_ssd_power_probe,
    .remove     = rg_ssd_power_remove,
    .driver     = {
        .owner  = THIS_MODULE,
        .name   = PROXY_NAME,
        .of_match_table = rg_ssd_power_driver_of_match,
    },
};

static int libata_reset_ksyms_look_up(void)
{
    int ret;
    unsigned long sym_reg_ata_ssd_power_reset_addr;
    unsigned long sym_unreg_ata_ssd_power_reset_addr;

    ret = find_kallsyms_lookup_name();
    if (ret < 0) {
        SSD_POWER_ERROR("find kallsyms_lookup_name failed\n");
        return ret;
    }

    sym_reg_ata_ssd_power_reset_addr = (unsigned long)kallsyms_lookup_name_fun("reg_ata_ssd_power_reset");
    if (!sym_reg_ata_ssd_power_reset_addr) {
        printk(KERN_ERR "Failed to find symbol reg_ata_ssd_power_reset.\n");
        return -ENOSYS;
    }

    sym_unreg_ata_ssd_power_reset_addr = (unsigned long)kallsyms_lookup_name_fun("unreg_ata_ssd_power_reset");
    if (!sym_unreg_ata_ssd_power_reset_addr) {
        printk(KERN_ERR "Failed to find symbol unreg_ata_ssd_power_reset.\n");
        return -ENOSYS;
    }

    g_p_reg_ata_ssd_power_reset = (p_reg_ata_ssd_power_reset)sym_reg_ata_ssd_power_reset_addr;
    g_p_unreg_ata_ssd_power_reset = (p_unreg_ata_ssd_power_reset)sym_unreg_ata_ssd_power_reset_addr;
    return 0;
}

static int __init rg_ssd_power_init(void)
{
    int i, ret;

    ret = libata_reset_ksyms_look_up();
    if (ret < 0) {
        printk(KERN_ERR "rg_ssd_power_init failed.\n");
        return ret;
    }

    for (i = 0; i < SSD_POWER_MAX_NUM; i++) {
        g_ssd_power_n[i] = NULL;
    }

    ret = g_p_reg_ata_ssd_power_reset(rg_ssd_power_reset);
    if (unlikely(ret != 0)) {
        printk(KERN_ERR "Failed to register ssd power control hook, ret: %d\n", ret);
        return ret;
    }

    return platform_driver_register(&rg_ssd_power_driver);
}

static void __exit rg_ssd_power_exit(void)
{
    rg_ssd_power_node_destroy();
    platform_driver_unregister(&rg_ssd_power_driver);
    (void)g_p_unreg_ata_ssd_power_reset();
    g_p_reg_ata_ssd_power_reset = NULL;
    g_p_unreg_ata_ssd_power_reset = NULL;
    printk(KERN_INFO "SSD power conrtol driver exit success.\n");
}

module_init(rg_ssd_power_init);
module_exit(rg_ssd_power_exit);

MODULE_DESCRIPTION("ssd power control driver");
MODULE_LICENSE("GPL");
MODULE_AUTHOR("sonic_rd <sonic_rd@ruijie.com.cn>");
