#ifndef __RG_SPI_OCORES_H__
#define __RG_SPI_OCORES_H__

#define SPI_OCORES_DEV_NAME_MAX_LEN (64)

typedef struct spi_ocores_device_s {
    uint32_t bus_num;           /* spi bus号 */
    uint32_t big_endian;        /* 1大端模式, 0小端模式 */
    char dev_name[SPI_OCORES_DEV_NAME_MAX_LEN];
    uint32_t reg_access_mode;   /* spi ocore 寄存器的访问方式 */
    uint32_t dev_base;          /* spi ocore 寄存器基址 */
    uint32_t reg_shift;
    uint32_t reg_io_width;
    uint32_t clock_frequency;   /* spi控制器主时钟频率 */
    uint32_t num_chipselect;    /* spi控制器支持的cs数 */
    int device_flag;            /* 设备生成标记，0：成功，-1：失败 */
} spi_ocores_device_t;

#endif