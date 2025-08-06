#ifndef __RG_SPI_DEV_H__
#define __RG_SPI_DEV_H__
#include <linux/string.h>

#define SPI_DEV_NAME_MAX_LEN (64)
#define mem_clear(data, size) memset((data), 0, (size))
typedef struct spi_dev_device_s {
    char spi_dev_name[SPI_DEV_NAME_MAX_LEN];    /* 设备名称 */
    uint32_t data_bus_width;                    /* 设备的数据位宽 */
    uint32_t addr_bus_width;                    /* 设备的地址位宽 */
    uint32_t per_rd_len;                        /* 每次读取长度限制 */
    uint32_t per_wr_len;                        /* 每次写入长度限制 */
    uint32_t spi_len;
} spi_dev_device_t;

#endif