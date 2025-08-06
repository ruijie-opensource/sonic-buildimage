/**
 * Copyright(C) 2010 Ruijie Network. All rights reserved.
 */
/*
 * octeon_cpld_drv.h
 * Original Author : sonic_rd@ruijie.com.cn, 2012-07-06
 *
 * octeon Dram 驱动头文件
 *
 * History
 *    v1.0    sonic_rd@ruijie.com.cn  2012-07-06  Initial version.
 */

#ifndef _LINUX_DRAM_DRIVER_H
#define _LINUX_DRAM_DRIVER_H

#include <linux/types.h>
typedef unsigned int u32;

struct phydev_user_info {
    int phy_index;    /* 表示要操作第几个phydev */
    u32 regnum;       /* 寄存器地址 */
    u32 regval;       /* 寄存器值 */
};

#define CMD_PHY_LIST                        _IOR('P', 0, struct phydev_user_info)
#define CMD_PHY_READ                        _IOR('P', 1, struct phydev_user_info)
#define CMD_PHY_WRITE                       _IOR('P', 2, struct phydev_user_info)

struct mdio_dev_user_info {
    int mdio_index;    /* 表示要操作第几个mdio dev */
    int phyaddr;       /* phy设备地址 */
    u32 regnum;        /* 寄存器地址 */
    u32 regval;        /* 寄存器值 */
};

#define CMD_MDIO_LIST                        _IOR('M', 0, struct mdio_dev_user_info)
#define CMD_MDIO_READ                        _IOR('M', 1, struct mdio_dev_user_info)
#define CMD_MDIO_WRITE                       _IOR('M', 2, struct mdio_dev_user_info)

#endif
