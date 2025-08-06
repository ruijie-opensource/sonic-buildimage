#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/sysfs.h>
#include <linux/slab.h>
#include <linux/stat.h>
#include <linux/uaccess.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/i2c.h>
#include <linux/i2c-mux.h>
#include <linux/version.h>
#if LINUX_VERSION_CODE < KERNEL_VERSION(4,19,152)
#include <linux/i2c-mux-gpio.h>
#else
#include <linux/platform_data/i2c-mux-gpio.h>
#endif
#include <linux/platform_device.h>
#include <linux/delay.h>
#include <linux/i2c-smbus.h>
#include <linux/string.h>
#include "ruijie.h"

#define PLATFORM_I2C_RETRY_TIMES    3

s32 platform_i2c_smbus_read_byte_data(const struct i2c_client *client, u8 command)
{
    int i;
    s32 ret;

    ret = -1;
    for (i = 0; i < PLATFORM_I2C_RETRY_TIMES; i++) {
       if ((ret = i2c_smbus_read_byte_data(client, command) ) >= 0 )
            break;
    }
    return ret;

}
EXPORT_SYMBOL(platform_i2c_smbus_read_byte_data);

s32 platform_i2c_smbus_read_i2c_block_data(const struct i2c_client *client,
                u8 command, u8 length, u8 *values)
{
    int i;
    s32 ret;

    ret = -1;
    for (i = 0; i < PLATFORM_I2C_RETRY_TIMES; i++) {
       if ((ret = i2c_smbus_read_i2c_block_data(client, command, length, values) ) >= 0 )
            break;
    }
    return ret;
}
EXPORT_SYMBOL(platform_i2c_smbus_read_i2c_block_data);

s32 platform_i2c_smbus_read_word_data(const struct i2c_client *client, u8 command)
{
    int i;
    s32 ret;

    ret = -1;
    for (i = 0; i < PLATFORM_I2C_RETRY_TIMES; i++) {
       if ((ret = i2c_smbus_read_word_data(client, command) ) >= 0 )
            break;
    }
    return ret;
}
EXPORT_SYMBOL(platform_i2c_smbus_read_word_data);

static int __init ruijie_platform_init(void)
{
    return 0;
}

static void __exit ruijie_platform_exit(void)
{

}

module_init(ruijie_platform_init);
module_exit(ruijie_platform_exit);

MODULE_DESCRIPTION("ruijie Platform Support");
MODULE_AUTHOR("sonic_rd <sonic_rd@ruijie.com.cn>");
MODULE_LICENSE("GPL");
