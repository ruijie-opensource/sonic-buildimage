#ifndef __RG_PLATFORM_I2C_DEV_H__
#define __RG_PLATFORM_I2C_DEV_H__

#define I2C_DEV_NAME_MAX_LEN (64)

typedef struct platform_i2c_dev_device_s {
    uint32_t i2c_bus;                       /* i2c bus号 */
    uint32_t i2c_addr;                      /* i2c设备地址 */
    char i2c_name[I2C_DEV_NAME_MAX_LEN];    /* 设备名称 */
    uint32_t data_bus_width;                /* 数据位宽 */
    uint32_t addr_bus_width;                /* 地址位宽 */
    uint32_t per_rd_len;                    /* 每次读取长度限制 */
    uint32_t per_wr_len;                    /* 每次写入长度限制 */
    int device_flag;                        /* 设备生成标记，0：成功，-1：失败 */
} platform_i2c_dev_device_t;

#endif
