/*
 * Copyright(C) 2001-2015s Ruijie Network. All rights reserved.
 */
/*
 * dfd_cfg_file.c
 * Original Author: sonic_rd@ruijie.com.cn 2020-02-17
 *
 * 内核模块文件操作，一次性将文件读取到内存中操作，不支持多线程操作
 *
 * History
 *  [Version]        [Author]                   [Date]            [Description]
 *     v1.0    sonic_rd@ruijie.com.cn         2020-02-17        Initial version
 *
 */

#include <asm/unistd.h>
#include <asm/uaccess.h>
#include <linux/stat.h>
#include <linux/slab.h>
#include <linux/fs.h>
#include <linux/mm.h>
#include <linux/types.h>
#include <linux/module.h>
#include <linux/kernel.h>

#include "../include/dfd_cfg_file.h"
#include "../include/rg_module.h"

struct getdents_callback {
    struct dir_context ctx;
    const char *obj_name;    /* 待匹配的名称 */
    char *match_name;        /* 匹配的结果 */
    int dir_len;             /* 目录名称长度 */
    int found;               /* 配置标志 */
};

/*
 * 打开文件
 * @fname: 文件名
 * @kfile_ctrl: 文件控制变量
 *
 * @returns: 0成功，其他失败
 */
int kfile_open(char *fname, kfile_ctrl_t *kfile_ctrl)
{
    int ret;
    struct file *filp;
    loff_t pos;

    if ((fname == NULL) || (kfile_ctrl == NULL)) {
        return KFILE_RV_INPUT_ERR;
    }

    /* 打开文件 */
    filp = filp_open(fname, O_RDONLY, 0);
    if (IS_ERR(filp)){
        return KFILE_RV_OPEN_FAIL;
    }

    kfile_ctrl->size = filp->f_inode->i_size;

    /* 申请文件大小的内存 */
    kfile_ctrl->buf = kmalloc(kfile_ctrl->size, GFP_KERNEL);
    if (kfile_ctrl->buf == NULL) {
        ret = KFILE_RV_MALLOC_FAIL;
        goto close_fp;
    }
    memset(kfile_ctrl->buf, 0, kfile_ctrl->size);
    /* 读取文件内容 */
    pos = 0;
    ret = kernel_read(filp, kfile_ctrl->buf, kfile_ctrl->size, &pos);
    if (ret < 0) {
        ret = KFILE_RV_RD_FAIL;
        goto free_buf;
    }
    /* 置当前位置 */
    kfile_ctrl->pos = 0;

    ret = KFILE_RV_OK;
    goto close_fp;

free_buf:
    kfree(kfile_ctrl->buf);
    kfile_ctrl->buf = NULL;

close_fp:
    filp_close(filp, NULL);
    return ret;
}

/*
 * 关闭文件
 * @kfile_ctrl: 文件控制变量
 */
void kfile_close(kfile_ctrl_t *kfile_ctrl)
{
    if (kfile_ctrl == NULL) {
        return;
    }

    /* 置文件大小为0，释放内存 */
    kfile_ctrl->size = 0;
    kfile_ctrl->pos = 0;
    if (kfile_ctrl->buf) {
        kfree(kfile_ctrl->buf);
        kfile_ctrl->buf = NULL;
    }
}

/*
 * 获取一行
 * @buf: buf缓存区
 * @buf_size: buf大小
 * @kfile_ctrl: 文件控制变量
 *
 * @returns: >=0成功，其他失败
 */
int kfile_gets(char *buf, int buf_size, kfile_ctrl_t *kfile_ctrl)
{
    int i;
    int has_cr = 0;

    if ((buf == NULL) || (buf_size <= 0) || (kfile_ctrl == NULL) || (kfile_ctrl->buf == NULL)
            || (kfile_ctrl->size <= 0)) {
        return KFILE_RV_INPUT_ERR;
    }

    /* 先将buf清零 */
    memset(buf, 0, buf_size);
    for (i = 0; i < buf_size; i++) {
        /* 已经到文件尾 */
        if (kfile_ctrl->pos >= kfile_ctrl->size) {
            break;
        }

        /* 上一个数据为换行符，一行已经复制完毕 */
        if (has_cr) {
            break;
        }

        /* 搜索到换行符 */
        if (IS_CR(kfile_ctrl->buf[kfile_ctrl->pos])) {
            has_cr = 1;
        }

        /* 复制数据 */
        buf[i] = kfile_ctrl->buf[kfile_ctrl->pos];
        kfile_ctrl->pos++;
    }

    return i;
}

/*
 * 读数据
 * @buf: buf缓存区
 * @buf_size: buf大小
 * @kfile_ctrl: 文件控制变量
 *
 * @returns: >=0成功，其他失败
 */
int kfile_read(int32_t addr, char *buf, int buf_size, kfile_ctrl_t *kfile_ctrl)
{
    int i;

    if ((buf == NULL) || (buf_size <= 0) || (kfile_ctrl == NULL) || (kfile_ctrl->buf == NULL)
            || (kfile_ctrl->size <= 0)) {
        return KFILE_RV_INPUT_ERR;
    }

    /* 地址检查 */
    if ((addr < 0) || (addr >= kfile_ctrl->size)) {
        return KFILE_RV_ADDR_ERR;
    }

    /* 先将buf清零 */
    memset(buf, 0, buf_size);

    kfile_ctrl->pos = addr;
    for (i = 0; i < buf_size; i++) {
        /* 已经到文件尾 */
        if (kfile_ctrl->pos >= kfile_ctrl->size) {
            break;
        }

        /* 复制数据 */
        buf[i] = kfile_ctrl->buf[kfile_ctrl->pos];
        kfile_ctrl->pos++;
    }

    return i;
}

static int kfile_filldir_one(struct dir_context *ctx, const char * name, int len,
            loff_t pos, u64 ino, unsigned int d_type)
{
    struct getdents_callback *buf ;
    int result;
    buf = container_of(ctx, struct getdents_callback, ctx);
    result = 0;
    if (strncmp(buf->obj_name, name, strlen(buf->obj_name)) == 0) {
        if (buf->dir_len < len) {
            DBG_DEBUG(DBG_ERROR, "match ok. dir name:%s, but buf_len %d small than dir len %d.\n",
                name, buf->dir_len, len);
            buf->found = 0;
            return -1;
        }
        memset(buf->match_name, 0 , buf->dir_len);
        memcpy(buf->match_name, name, len);
        buf->found = 1;
        result = -1;
    }
    return result;
}

/*
 * 读数据
 * @buf: buf缓存区
 * @buf_size: buf大小
 * @kfile_ctrl: 文件控制变量
 *
 * @returns: >=0成功，其他失败
 */
int kfile_iterate_dir(const char *dir_path, const char *obj_name, char *match_name, int len)
{
    int ret;
    struct file *dir;
    struct getdents_callback buffer = {
        .ctx.actor = kfile_filldir_one,
    };

    if(!dir_path || !obj_name || !match_name) {
        DBG_DEBUG(DBG_ERROR, "params error. \n");
        return KFILE_RV_INPUT_ERR;
    }
    buffer.obj_name = obj_name;
    buffer.match_name = match_name;
    buffer.dir_len = len;
    buffer.found = 0;
    /* 打开文件夹 */
    dir = filp_open(dir_path, O_RDONLY, 0);
    if (IS_ERR(dir)) {
        DBG_DEBUG(DBG_ERROR, "filp_open error, dir path:%s\n", dir_path);
        return KFILE_RV_OPEN_FAIL;
    }
    ret = iterate_dir(dir, &buffer.ctx);
    if (buffer.found) {
        DBG_DEBUG(DBG_VERBOSE, "match ok, dir name:%s\n", match_name);
        filp_close(dir, NULL);
        return DFD_RV_OK;
    }
    filp_close(dir, NULL);
    return -DFD_RV_NODE_FAIL;
}

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
int kfile_write(char *fpath, int32_t addr, char *buf, int buf_size)
{
    int ret = KFILE_RV_OK;
    struct file *filp;
    int wlen;

    if ((fpath == NULL) || (buf == NULL) || (buf_size <= 0)) {
        return KFILE_RV_INPUT_ERR;
    }

    /* 地址检查 */
    if (addr < 0) {
        return KFILE_RV_ADDR_ERR;
    }

    /* 打开文件 */
    filp = filp_open(fpath, O_RDWR, 0);
    if (IS_ERR(filp)){
        return KFILE_RV_OPEN_FAIL;
    }

    filp->f_op->llseek(filp,0,0);
    filp->f_pos = addr;
    /* 写文件内容 */
    wlen = filp->f_op->write(filp, buf, buf_size, &(filp->f_pos));
    if (wlen < 0) {
        ret = KFILE_RV_WR_FAIL;
    }

    filp->f_op->llseek(filp,0,0);
    filp_close(filp, NULL);

    return ret;
}
#endif
