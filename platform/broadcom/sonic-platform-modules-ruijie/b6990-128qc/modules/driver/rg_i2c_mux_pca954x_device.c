#include <linux/module.h>
#include <linux/io.h>
#include <linux/i2c.h>
#include <linux/device.h>
#include <linux/delay.h>
#include <linux/platform_device.h>

#include <rg_i2c_mux_pca954x.h>

static int g_rg_i2c_mux_pca954x_device_debug = 0;
static int g_rg_i2c_mux_pca954x_device_error = 0;

module_param(g_rg_i2c_mux_pca954x_device_debug, int, S_IRUGO | S_IWUSR);
module_param(g_rg_i2c_mux_pca954x_device_error, int, S_IRUGO | S_IWUSR);

#define RG_I2C_MUX_PCA954X_DEVICE_DEBUG_VERBOSE(fmt, args...) do {                                        \
    if (g_rg_i2c_mux_pca954x_device_debug) { \
        printk(KERN_INFO "[RG_I2C_MUX_PCA954X_DEVICE][VER][func:%s line:%d]\r\n"fmt, __func__, __LINE__, ## args); \
    } \
} while (0)

#define RG_I2C_MUX_PCA954X_DEVICE_DEBUG_ERROR(fmt, args...) do {                                        \
    if (g_rg_i2c_mux_pca954x_device_error) { \
        printk(KERN_ERR "[RG_I2C_MUX_PCA954X_DEVICE][ERR][func:%s line:%d]\r\n"fmt, __func__, __LINE__, ## args); \
    } \
} while (0)

static i2c_mux_pca954x_device_t i2c_mux_pca954x_device_data0 = {
    .i2c_bus                        = 1,
    .i2c_addr                       = 0x70,
    .probe_disable                  = 1,
    .select_chan_check              = 1,
    .close_chan_force_reset         = 1,
    .pca9548_base_nr                = 132, /* 132~139 */
    .pca9548_reset_type             = PCA9548_RESET_IO,
    .rst_delay_b                    = 0,
    .rst_delay                      = 1000,
    .rst_delay_a                    = 1000,
    .attr = {
        .io_attr.io_addr          = 0x919,
        .io_attr.mask             = 0x40,
        .io_attr.reset_on         = 0x00,
        .io_attr.reset_off        = 0x40,
    },
};

struct i2c_board_info i2c_mux_pca954x_device_info[] = {
    {
        .type = "rg_pca9548",
        .platform_data = &i2c_mux_pca954x_device_data0,
    },
};

static int __init rg_i2c_mux_pca954x_device_init(void)
{
    int i;
    struct i2c_adapter *adap;
    struct i2c_client *client;
    i2c_mux_pca954x_device_t *i2c_mux_pca954x_device_data;

    RG_I2C_MUX_PCA954X_DEVICE_DEBUG_VERBOSE("enter!\n");
    for (i = 0; i < ARRAY_SIZE(i2c_mux_pca954x_device_info); i++) {
        i2c_mux_pca954x_device_data = i2c_mux_pca954x_device_info[i].platform_data;
        i2c_mux_pca954x_device_info[i].addr = i2c_mux_pca954x_device_data->i2c_addr;
        adap = i2c_get_adapter(i2c_mux_pca954x_device_data->i2c_bus);
        if (adap == NULL) {
            i2c_mux_pca954x_device_data->client = NULL;
            printk(KERN_ERR "get i2c bus %d adapter fail.\n", i2c_mux_pca954x_device_data->i2c_bus);
            continue;
        }
        client = i2c_new_client_device(adap, &i2c_mux_pca954x_device_info[i]);
        if (!client) {
            i2c_mux_pca954x_device_data->client = NULL;
            printk(KERN_ERR "Failed to register pca954x device %d at bus %d!\n",
                i2c_mux_pca954x_device_data->i2c_addr, i2c_mux_pca954x_device_data->i2c_bus);
        } else {
            i2c_mux_pca954x_device_data->client = client;
        }
        i2c_put_adapter(adap);
    }
    return 0;
}

static void __exit rg_i2c_mux_pca954x_device_exit(void)
{
    int i;
    i2c_mux_pca954x_device_t *i2c_mux_pca954x_device_data;

    RG_I2C_MUX_PCA954X_DEVICE_DEBUG_VERBOSE("enter!\n");
    for (i = ARRAY_SIZE(i2c_mux_pca954x_device_info) - 1; i >= 0; i--) {
        i2c_mux_pca954x_device_data = i2c_mux_pca954x_device_info[i].platform_data;
        if (i2c_mux_pca954x_device_data->client) {
            i2c_unregister_device(i2c_mux_pca954x_device_data->client);
            i2c_mux_pca954x_device_data->client = NULL;
        }
    }
}

module_init(rg_i2c_mux_pca954x_device_init);
module_exit(rg_i2c_mux_pca954x_device_exit);
MODULE_DESCRIPTION("RG I2C MUX PCA954X Devices");
MODULE_LICENSE("GPL");
MODULE_AUTHOR("sonic_rd@ruijie.com.cn");
