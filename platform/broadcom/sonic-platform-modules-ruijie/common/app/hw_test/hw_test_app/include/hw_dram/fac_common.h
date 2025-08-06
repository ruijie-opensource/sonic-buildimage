/*
 * Copyright(C) 2013 Ruijie Network. All rights reserved. 
 */
/*
 * common.h 
 * Original Author:  sonic_rd@ruijie.com.cn, 2013-9-25 
 *
 * factroy generial handle of factory test.
 */

#ifndef _FAC_AC_COMMON_H_
#define _FAC_AC_COMMON_H_

#define FAC_TEST_OK                  0
#define FAC_TEST_FAIL                1
#define GRTD_LOG_DEBUG               2
#define GRTD_LOG_ERR                 1
#define GRTD_LOG_NONE                0
#define FAC_MEM_SIZE_BUF_LEN         1024               /* 保存内存大小的长度 */
#define FAC_MEM_TEST_SIZE            (1024*1024*32)     /* 内存测试大小 */
#define FAC_MEM_AUTOTEST_SIZE        (1024*1024*2048ULL) /* 内存测试大小 */
#define FAC_MEM_MAX_SIZE             (1024*1024*4096ULL) /* 内存测试大小 */
#define FAC_MEM_TEST_PAGESIZE        8192           /* 内存测试的pagesize */
#define FAC_FILENAME_LEN             128            /* 设备文件名长度 */
#define FAC_FILE_LINE_LEN            128            /* 文件每行的长度 */
#define FAC_FILE_SIZE_LEN            16             /* 文件中表示大小的长度 */
#define GRTD_SDRAM_ECC_ERR           1              /* ECC校验错误 */
#define GRTD_SDRAM_WR_ERR            2              /* 读写操作错误 */
#define GRTD_SDRAM_GET_MEM_SIZE_ERR  3              /* 获取内存容量错误 */
#define GRTD_SDRAM_UNKNOW_ERR        4              /* 其他未知错误 */

extern int platform_fac_dbg;
/* 生产测试模块跟踪调试信息 */
#define FAC_LOG_DBG(dbg, fmt, arg...)                       \
    do {                                                    \
        if (dbg <= platform_fac_dbg) {                      \
            printf("[FACTORY <%s>:<%d>] " fmt,          \
                 __FUNCTION__, __LINE__, ##arg); \
        }                                                   \
    } while (0)

#endif /* _FAC_AC_COMMON_H_ */
