#ifndef __DFD_CFG_FILE_H__
#define __DFD_CFG_FILE_H__

#include <linux/types.h>

/* 返回值 */
#define KFILE_RV_OK             (0)
#define KFILE_RV_INPUT_ERR      (-1)    /* 入参错误 */
#define KFILE_RV_STAT_FAIL      (-2)    /* 获取文件属性失败 */
#define KFILE_RV_OPEN_FAIL      (-3)    /* 打开文件失败 */
#define KFILE_RV_MALLOC_FAIL    (-4)    /* 申请内存失败 */
#define KFILE_RV_RD_FAIL        (-5)    /* 读取失败 */
#define KFILE_RV_ADDR_ERR       (-6)    /* 地址错误 */
#define KFILE_RV_WR_FAIL        (-7)    /* 地址错误 */

/* 是否为换行符 */
#define IS_CR(c)  ((c) == '\n')

/* 文件操作控制结构 */
typedef struct kfile_ctrl_s {
    int32_t size;       /* 文件大小 */
    int32_t pos;        /* 当前位置 */
    char *buf;          /* 文件缓存区 */
} kfile_ctrl_t;

/*
 * 打开文件
 * @fname: 文件名
 * @kfile_ctrl: 文件控制变量
 *
 * @returns: 0成功，其他失败
 */
int kfile_open(char *fname, kfile_ctrl_t *kfile_ctrl);

/*
 * 关闭文件
 * @kfile_ctrl: 文件控制变量
 */
void kfile_close(kfile_ctrl_t *kfile_ctrl);

/*
 * 关闭文件
 * @kfile_ctrl: 文件控制变量
 *
 * @returns: >=0成功，其他失败
 */
int kfile_gets(char *buf, int buf_size, kfile_ctrl_t *kfile_ctrl);

/*
 * 读数据
 * @buf: buf缓存区
 * @buf_size: buf大小
 * @kfile_ctrl: 文件控制变量
 *
 * @returns: >=0成功，其他失败
 */
int kfile_read(int32_t addr, char *buf, int buf_size, kfile_ctrl_t *kfile_ctrl);

/*
 * 读数据
 * @buf: buf缓存区
 * @buf_size: buf大小
 * @kfile_ctrl: 文件控制变量
 *
 * @returns: >=0成功，其他失败
 */
int kfile_iterate_dir(const char *dir_path, const char *obj_name, char *match_name, int len);

#if 0
/*
 * 写数据
 * @fname: 文件名
 * @addr: 写入文件的偏移地址
 * @buf: 写入数据
 * @buf_size: 数据大小
 *
 * @returns: >=0成功，其他失败
 */
int kfile_write(char *fpath, int32_t addr, char *buf, int buf_size);
#endif
#endif /* __DFD_CFG_FILE_H__ */
