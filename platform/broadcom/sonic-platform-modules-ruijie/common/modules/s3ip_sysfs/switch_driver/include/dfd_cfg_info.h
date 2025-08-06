#ifndef __DFD_CFG_INFO_H__
#define __DFD_CFG_INFO_H__

#include <linux/types.h>

/* num buf格式数据转换成数值函数指针 */
typedef int (*info_num_buf_to_value_f)(uint8_t *num_buf, int buf_len, int *num_val);

/* num buf格式数据转换成数值函数指针 */
typedef int (*info_buf_to_buf_f)(uint8_t *buf, int buf_len, uint8_t *buf_new, int *buf_len_new);

/* 信息格式判断宏 */
#define IS_INFO_FRMT_BIT(frmt)      ((frmt) == INFO_FRMT_BIT)
#define IS_INFO_FRMT_BYTE(frmt)     (((frmt) == INFO_FRMT_BYTE) || ((frmt) == INFO_FRMT_NUM_BYTES))
#define IS_INFO_FRMT_NUM_STR(frmt)  ((frmt) == INFO_FRMT_NUM_STR)
#define IS_INFO_FRMT_NUM_BUF(frmt)  ((frmt) == INFO_FRMT_NUM_BUF)
#define IS_INFO_FRMT_BUF(frmt)      ((frmt) == INFO_FRMT_BUF)

/* INT信息长度合法性判断 */
#define INFO_INT_MAX_LEN            (32)
#define INFO_INT_LEN_VALAID(len)    (((len) > 0) && ((len) < INFO_INT_MAX_LEN))

/* buf信息长度合法性判断 */
#define INFO_BUF_MAX_LEN            (128)
#define INFO_BUF_LEN_VALAID(len)    (((len) > 0) && ((len) < INFO_BUF_MAX_LEN))

/* 信息位偏移数合法性判断 */
#define INFO_BIT_OFFSET_VALID(bit_offset)   (((bit_offset) >= 0) && ((bit_offset) < 8))

/* 信息控制模式 */
typedef enum info_ctrl_mode_e {
    INFO_CTRL_MODE_NONE,
    INFO_CTRL_MODE_CFG,      /* 配置模式 */
    INFO_CTRL_MODE_CONS,     /* 常量模式 */
    INFO_CTRL_MODE_TLV,      /* TLV模式 */
    INFO_CTRL_MODE_SRT_CONS, /* 字符串常量*/
    INFO_CTRL_MODE_END
} info_ctrl_mode_t;

/* 信息格式 */
typedef enum info_frmt_e {
    INFO_FRMT_NONE,
    INFO_FRMT_BIT,          /* 单个或多个位，不超过8位 */
    INFO_FRMT_BYTE,         /* 单个字节 */
    INFO_FRMT_NUM_BYTES,    /* 多个字节数值，不超过sizeof(int) */
    INFO_FRMT_NUM_STR,      /* 字符串数值 */
    INFO_FRMT_NUM_BUF,      /* 字符串数值 */
    INFO_FRMT_BUF,          /* 多个字节 */
    INFO_FRMT_END
} info_frmt_t;

/* 信息源 */
typedef enum info_src_e {
    INFO_SRC_NONE,
    INFO_SRC_CPLD,          /* CPLD设备 */
    INFO_SRC_FPGA,          /* FPGA设备 */
    INFO_SRC_OTHER_I2C,     /* 其他i2c设备 */
    INFO_SRC_FILE,          /* 文件 */
    INFO_SRC_END
} info_src_t;

/* 信息极性 */
typedef enum info_pola_e {
    INFO_POLA_NONE,
    INFO_POLA_POSI,         /* 正极性 位值1有效 数值高字节保存在来源的低地址空间 */
    INFO_POLA_NEGA,         /* 负极性 位值0有效 数值高字节保存在来源的高地址空间 */
    INFO_POLA_END
} info_pola_t;

/* 信息控制结构体 */
#define INFO_FPATH_MAX_LEN     (128)  /* 文件来源信息路径最大长度 */
#define INFO_STR_CONS_MAX_LEN  (64)   /* 字符串常量最大长度 */
typedef struct info_ctrl_s {
    info_ctrl_mode_t mode;          /* 模式 */
    int32_t int_cons;               /* 暂时只支持int类型 */
    info_src_t src;                 /* 源 */
    info_frmt_t frmt;               /* 格式 */
    info_pola_t pola;               /* 极性 */
    char fpath[INFO_FPATH_MAX_LEN]; /* 文件路径，只针对文件来源信息 */
    int32_t addr;                   /* 地址 */
    int32_t len;                    /* 长度，位长度或字节长度 */
    int32_t bit_offset;             /* 地址内位偏移数 */
    char str_cons[INFO_STR_CONS_MAX_LEN]; /* 字符串常量 */
    int32_t int_extra1;             /* int类型预留 */
    int32_t int_extra2;
} info_ctrl_t;

/* info_ctrl_t成员宏 */
typedef enum info_ctrl_mem_s {
    INFO_CTRL_MEM_MODE,
    INFO_CTRL_MEM_INT_CONS,
    INFO_CTRL_MEM_SRC,
    INFO_CTRL_MEM_FRMT,
    INFO_CTRL_MEM_POLA,
    INFO_CTRL_MEM_FPATH,
    INFO_CTRL_MEM_ADDR,
    INFO_CTRL_MEM_LEN,
    INFO_CTRL_MEM_BIT_OFFSET,
    INFO_CTRL_MEM_STR_CONS,
    INFO_CTRL_MEM_INT_EXTRA1,
    INFO_CTRL_MEM_INT_EXTRA2,
    INFO_CTRL_MEM_END
} info_ctrl_mem_t;

/* sensor 数据格式 */
typedef enum sensor_format_mem_s {
    LINEAR11 = 1,
    LINEAR16,
    TMP464,
    MAC_TH5
} sensor_format_mem_t;

/* hwmon数据格式转换 */
typedef int (*info_hwmon_buf_f)(uint8_t *buf, int buf_len, uint8_t *buf_new, int *buf_len_new,
                info_ctrl_t *info_ctrl, int coefficient, int addend);

/* 全局变量 */
extern char *g_info_ctrl_mem_str[INFO_CTRL_MEM_END];  /* info_ctrl_t成员字符串 */
extern char *g_info_src_str[INFO_SRC_END];            /* info_src_t枚举字符串 */
extern char *g_info_frmt_str[INFO_FRMT_END];          /* info_frmt_t枚举字符串 */
extern char *g_info_pola_str[INFO_POLA_END];          /* info_pola_t枚举字符串 */
extern char *g_info_ctrl_mode_str[INFO_CTRL_MODE_END];/* info_ctrl_mode_t枚举字符串 */

/**
 * dfd_info_get_int - 获取int类型信息
 * @key: 配置项搜索关键字
 * @ret: int类型信息
 * @pfun: num buf类型数据转换函数
 *
 * @returns: 0成功，<0失败
 */
int dfd_info_get_int(int key, int *ret, info_num_buf_to_value_f pfun);

/**
 * dfd_info_get_buf - 获取buf型信息
 * @key: 配置项搜索关键字
 * @buf: 信息buf
 * @buf_len: buf长度，长度需要不小于info_ctrl->len
 * @pfun: 数据转换函数指针
 *
 * @returns: <0失败，其他成功
 */
int dfd_info_get_buf(int key, uint8_t *buf, int buf_len, info_buf_to_buf_f pfun);

/**
 * dfd_info_set_int - 设置int类型信息
 * @key: 配置项搜索关键字
 * @val: int类型信息
 *
 * @returns: 0成功，<0失败
 */
int dfd_info_set_int(int key, int val);

/**
 * dfd_info_get_sensor - 获取sensors数值
 * @key: HWMON配置对应的key
 * @buf：结果存放
 * @buf_len: buf长度
 *
 * @returns: <0失败，其他成功
 */
int dfd_info_get_sensor(uint32_t key, char *buf, int buf_len, info_hwmon_buf_f pfun);

/**
 * @buf：输入和结果存放
 *
 */
void dfd_info_del_no_print_string(char *buf);
#endif /* __DFD_CFG_INFO_H__ */
