/*
 * Copyright(C) 2001-2012 Ruijie Network. All rights reserved.
 */
/*
 * rg_module.c
 * Original Author: sonic_rd@ruijie.com.cn 2020-02-17
 *
 * dfd内核代码，DM无关代码抽出
 *
 * History
 *  [Version]        [Author]                   [Date]            [Description]
 *   *  v1.0    sonic_rd@ruijie.com.cn         2020-02-17          Initial version
 *   *  v1.1    sonic_rd@ruijie.com.cn         2021-08-26          S3IP sysfs
 */
#include <linux/module.h>

#include "./include/rg_module.h"
#include "./include/dfd_cfg.h"

int g_dfd_dbg_level = 0;   /* 调试开关级别 */
module_param(g_dfd_dbg_level, int, S_IRUGO | S_IWUSR);

/**
 * rg_dev_cfg_init - dfd模块初始化
 *
 * @returns: <0失败，否则成功
 */
int32_t rg_dev_cfg_init(void)
{
    return dfd_dev_cfg_init();
}

/**
 * rg_dev_cfg_exit - dfd模块退出
 *
 * @returns: void
 */

void rg_dev_cfg_exit(void)
{
    dfd_dev_cfg_exit();
    return;
}

/**
 * dfd_get_dev_number - 获取设备数量
 * @main_dev_id:主设备号
 * @minor_dev_id:次设备号
 * @returns: <0失败，否则返回设备数量
 */
int dfd_get_dev_number(unsigned int main_dev_id, unsigned int minor_dev_id)
{
    int key,dev_num;
    int *p_dev_num;

    key = DFD_CFG_KEY(DFD_CFG_ITEM_DEV_NUM, main_dev_id, minor_dev_id);
    p_dev_num = dfd_ko_cfg_get_item(key);
    if (p_dev_num == NULL) {
        DBG_DEBUG(DBG_ERROR, "get device number failed, key:0x%x\n",key);
        return -DFD_RV_DEV_NOTSUPPORT;
    }
    dev_num = *p_dev_num;
    DBG_DEBUG(DBG_VERBOSE, "get device number ok, number:%d\n",dev_num);
    return dev_num;
}
