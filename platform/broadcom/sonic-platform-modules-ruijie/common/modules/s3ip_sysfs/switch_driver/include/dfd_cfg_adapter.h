#ifndef __DFD_CFG_ADAPTER_H__
#define __DFD_CFG_ADAPTER_H__

#define DFD_KO_CPLD_I2C_RETRY_SLEEP            (10)  /* ms */
#define DFD_KO_CPLD_I2C_RETRY_TIMES            (50 / DFD_KO_CPLD_I2C_RETRY_SLEEP)

#define DFD_KO_CPLD_GET_SLOT(addr)             ((addr >> 24) & 0xff)
#define DFD_KO_CPLD_GET_ID(addr)               ((addr >> 16) & 0xff)
#define DFD_KO_CPLD_GET_INDEX(addr)            (addr & 0xffff)
#define DFD_KO_CPLD_MODE_I2C_STRING            "i2c"
#define DFD_KO_CPLD_MODE_LPC_STRING            "lpc"

#define DFD_KO_OTHER_I2C_GET_MAIN_ID(addr)     ((addr >> 24) & 0xff)
#define DFD_KO_OTHER_I2C_GET_INDEX(addr)       ((addr >> 16) & 0xff)
#define DFD_KO_OTHER_I2C_GET_OFFSET(addr)      (addr & 0xffff)
#define DFD_SYSFS_PATH_MAX_LEN                 (64)

typedef struct dfd_i2c_dev_s {
    int bus;        /* bus号 */
    int addr;       /* 总线地址 */
} dfd_i2c_dev_t;

/* dfd_i2c_dev_t成员宏 */
typedef enum dfd_i2c_dev_mem_s {
    DFD_I2C_DEV_MEM_BUS,
    DFD_I2C_DEV_MEM_ADDR,
    DFD_I2C_DEV_MEM_END
} dfd_i2c_dev_mem_t;

typedef enum cpld_mode_e {
    DFD_CPLD_MODE_I2C,     /* I2C总线 */
    DFD_CPLD_MODE_LPC,      /*LPC总线*/
} cpld_mode_t;

/* i2c访问模式 */
typedef enum i2c_mode_e {
    DFD_I2C_MODE_NORMAL_I2C,    /* I2C总线 */
    DFD_I2C_MODE_SMBUS,         /* SMBUS总线 */
} i2c_mode_t;

/* 全局变量 */
extern char *g_dfd_i2c_dev_mem_str[DFD_I2C_DEV_MEM_END];      /* dfd_i2c_dev_t成员字符串 */

/**
 * dfd_ko_cpld_read - cpld读操作
 * @addr: 偏移地址
 * @buf: 数据
 *
 * @returns: <0失败，其他成功
 */
int32_t dfd_ko_cpld_read(int32_t addr, uint8_t *buf);

/**
 * dfd_ko_cpld_write - cpld 写操作
 * @addr: 地址
 * @data: 数据
 *
 * @returns: <0失败，其他成功
 */
int32_t dfd_ko_cpld_write(int32_t addr, uint8_t val);

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
int32_t dfd_ko_i2c_read(int bus, int addr, int offset, uint8_t *buf, uint32_t size, const char *sysfs_name);

/**
 * dfd_ko_i2c_write - I2C 写操作
 * @bus: I2C通道
 * @addr: I2C设备地址
 * @offset：寄存器偏移
 * @buf：写缓冲区
 * @size：写入长度
 * @returns: <0失败，其他成功
 */
int32_t dfd_ko_i2c_write(int bus, int addr, int offset, uint8_t *buf, uint32_t size);

/**
 * dfd_ko_read_file - 文件读操作
 * @fpath: 文件路径
 * @addr: 地址
 * @val: 数据
 * @read_bytes: 长度
 *
 * @returns: <0失败，其他成功
 */
int32_t dfd_ko_read_file(char *fpath, int32_t addr, uint8_t *val, int32_t read_bytes);

/**
 * dfd_ko_write_file - 文件写操作
 * @fpath: 文件路径
 * @addr: 地址
 * @val: 数据
 * @write_bytes: 长度
 *
 * @returns: <0失败，其他成功
 */
int32_t dfd_ko_write_file(char *fpath, int32_t addr, uint8_t *val, int32_t write_bytes);

/**
 * dfd_ko_other_i2c_dev_read - other_i2c读操作
 * @addr: 地址
 * @val: 数据
 * @read_len: 长度
 *
 * @returns: <0失败，其他成功
 */
int32_t dfd_ko_other_i2c_dev_read(int32_t addr, uint8_t *value, int32_t read_len);
#endif /* __DFD_CFG_ADAPTER_H__ */
