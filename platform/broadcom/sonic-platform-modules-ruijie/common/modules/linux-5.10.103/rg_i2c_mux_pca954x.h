#ifndef __RG_I2C_MUX_PCA954X_H__
#define __RG_I2C_MUX_PCA954X_H__

typedef enum pca9548_reset_type_s {
    PCA9548_RESET_NONE = 0,     /* 不需要9548复位 */
    PCA9548_RESET_I2C = 1,      /* 通过I2C接口复位9548 */
    PCA9548_RESET_GPIO = 2,     /* 通过GPIO复位9548 */
    PCA9548_RESET_IO = 3,       /* 通过io接口复位9548 */
    PCA9548_RESET_FILE = 4,     /* 通过文件接口复位9548 */
} pca9548_reset_type_t;

typedef struct i2c_attr_s {
    uint32_t i2c_bus;
    uint32_t i2c_addr;
    uint32_t reg_offset;
    uint32_t mask;
    uint32_t reset_on;
    uint32_t reset_off;
} i2c_attr_t;

typedef struct io_attr_s {
    uint32_t io_addr;
    uint32_t mask;
    uint32_t reset_on;
    uint32_t reset_off;
} io_attr_t;

typedef struct file_attr_s {
    const char *dev_name;
    uint32_t offset;
    uint32_t mask;
    uint32_t reset_on;
    uint32_t reset_off;
} file_attr_t;

typedef struct gpio_attr_s {
    int gpio_init;
    uint32_t gpio;
    uint32_t reset_on;
    uint32_t reset_off;
} gpio_attr_t;

typedef struct i2c_mux_pca954x_device_s {
    struct i2c_client *client;
    uint32_t i2c_bus;                       /* i2c bus号 */
    uint32_t i2c_addr;                      /* i2c设备地址 */
    uint32_t pca9548_base_nr;               /* base bus号 */
    uint32_t pca9548_reset_type;            /* 数据位宽 */
    uint32_t rst_delay_b;                   /* delay time before reset(us) */
    uint32_t rst_delay;                     /* reset time(us) */
    uint32_t rst_delay_a;                   /* delay time after reset(us) */
    bool probe_disable;                     /* bus默认生成 0:不默认 1:默认生成 */
    bool select_chan_check;                 /* 开启通道时检查 0:不检查 1:检查 */
    bool close_chan_force_reset;            /* 关闭通道时复位 0:不复位 1:复位 */
    union {
        i2c_attr_t i2c_attr;
        gpio_attr_t gpio_attr;
        io_attr_t io_attr;
        file_attr_t file_attr;
    } attr;
} i2c_mux_pca954x_device_t;

#endif