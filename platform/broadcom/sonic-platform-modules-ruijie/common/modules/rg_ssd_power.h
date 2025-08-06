#ifndef __RG_SSD_POWER_H__
#define __RG_SSD_POWER_H__

typedef int (*ata_power_reset_func_t)(unsigned int);

#define SSD_POWER_NAME_MAX_LEN (64)

typedef struct {
    uint32_t port_id;
    char file_name[SSD_POWER_NAME_MAX_LEN];
    uint32_t addr;
    uint32_t power_on;
    uint32_t power_off;
    uint32_t power_mask;
    uint32_t power_on_delay;
    uint32_t power_off_delay;
    uint32_t reg_access_mode;
    int device_flag;            /* 设备生成标记，0：成功，-1：失败 */
} ssd_power_device_t;

#endif /* __RG_SSD_POWER_H__ */
