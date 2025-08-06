#ifndef _RG_MODULE_H_
#define _RG_MODULE_H_

#include "switch_driver.h"

typedef enum dfd_rv_s {
    DFD_RV_OK               = 0,
    DFD_RV_INIT_ERR         = 1,
    DFD_RV_SLOT_INVALID     = 2,
    DFD_RV_MODE_INVALID     = 3,
    DFD_RV_MODE_NOTSUPPORT  = 4,
    DFD_RV_TYPE_ERR         = 5,
    DFD_RV_DEV_NOTSUPPORT   = 6,
    DFD_RV_DEV_FAIL         = 7,
    DFD_RV_INDEX_INVALID    = 8,
    DFD_RV_NO_INTF          = 9,
    DFD_RV_NO_NODE          = 10,
    DFD_RV_NODE_FAIL        = 11,
    DFD_RV_INVALID_VALUE    = 12,
    DFD_RV_NO_MEMORY        = 13,
} dfd_rv_t;

typedef enum status_mem_e {
    STATUS_ABSENT  = 0,
    STATUS_OK      = 1,
    STATUS_NOT_OK  = 2,
    STATUS_MEM_END = 3,
} status_mem_t;

typedef enum dfd_psu_knos_status_e {
    FAULT = 0,
    NORMAL = 1,
} dfd_psu_knos_status_t;

/* psu PMBUS */
typedef enum psu_sensors_type_e {
    PSU_SENSOR_NONE    = 0,
    PSU_IN_VOL         = 1,
    PSU_IN_CURR        = 2,
    PSU_IN_POWER       = 3,
    PSU_OUT_VOL        = 4,
    PSU_OUT_CURR       = 5,
    PSU_OUT_POWER      = 6,
    PSU_FAN_SPEED      = 7,
    PSU_OUT_MAX_POWERE = 8,
    PSU_OUT_STATUS     = 9,
    PSU_IN_STATUS      = 10,
    PSU_IN_TYPE        = 11,
    PSU_FAN_RATIO      = 12,
} psu_sensors_type_t;

/* Watchdog类型 */
typedef enum rg_wdt_type_e {
    RG_WDT_TYPE_NAME         = 0,     /* watchdog identify */
    RG_WDT_TYPE_STATE        = 1,     /* watchdog state */
    RG_WDT_TYPE_TIMELEFT     = 2,     /* watchdog timeleft */
    RG_WDT_TYPE_TIMEOUT      = 3,     /* watchdog timeout */
    RG_WDT_TYPE_ENABLE       = 4,     /* watchdog enable */
    RG_WDT_TYPE_RESET        = 5,     /* watchdog reset */
} rg_wdt_type_t;

typedef enum dfd_dev_info_type_e {
    DFD_DEV_INFO_TYPE_MAC               = 1,
    DFD_DEV_INFO_TYPE_NAME              = 2,
    DFD_DEV_INFO_TYPE_SN                = 3,
    DFD_DEV_INFO_TYPE_PWR_CONS          = 4,
    DFD_DEV_INFO_TYPE_HW_INFO           = 5,
    DFD_DEV_INFO_TYPE_DEV_TYPE          = 6,
    DFD_DEV_INFO_TYPE_PART_NAME         = 7,
    DFD_DEV_INFO_TYPE_PART_NUMBER       = 8,  /* part number */
    DFD_DEV_INFO_TYPE_FAN_DIRECTION     = 9,
    DFD_DEV_INFO_TYPE_MAX_OUTPUT_POWRER = 10, /* max_output_power */
    DFD_DEV_INFO_TYPE_SPEED_MAX = 11,
    DFD_DEV_INFO_TYPE_SPEED_MIN = 12,
    DFD_DEV_INFO_TYPE_ASSET_TAG = 13,
    DFD_DEV_INFO_TYPE_OUT_VOL_MAX = 14,
    DFD_DEV_INFO_TYPE_OUT_VOL_MIN = 15,
} dfd_dev_tlv_type_t;

/* 主设备类型 */
typedef enum rg_main_dev_type_e {
    RG_MAIN_DEV_MAINBOARD = 0,      /* 主板 */
    RG_MAIN_DEV_FAN       = 1,      /* 风扇 */
    RG_MAIN_DEV_PSU       = 2,      /* 电源 */
    RG_MAIN_DEV_SFF       = 3,      /* 光模块 */
    RG_MAIN_DEV_CPLD      = 4,      /* CPLD */
    RG_MAIN_DEV_SLOT      = 5,      /* 子卡 */
} rg_main_dev_type_t;

/* 次设备类型 */
typedef enum rg_minor_dev_type_e {
    RG_MINOR_DEV_NONE  = 0,    /* None */
    RG_MINOR_DEV_TEMP  = 1,    /* 温度*/
    RG_MINOR_DEV_IN    = 2,    /* 电压 */
    RG_MINOR_DEV_CURR  = 3,    /* 电流 */
    RG_MINOR_DEV_POWER = 4,    /* 功率 */
    RG_MINOR_DEV_MOTOR = 5,    /* 马达 */
    RG_MINOR_DEV_PSU   = 6,    /* 电源型号 */
    RG_MINOR_DEV_FAN   = 7,    /* 风扇型号 */
    RG_MINOR_DEV_CPLD  = 8,    /* CPLD */
    RG_MINOR_DEV_FPGA  = 9,    /* FPGA */
} rg_minor_dev_type_t;

/* SENSORS属性类型 */
typedef enum rg_sensor_type_e {
    RG_SENSOR_INPUT       = 0,     /* 传感器值 */
    RG_SENSOR_ALIAS       = 1,     /* 传感器别称 */
    RG_SENSOR_TYPE        = 2,     /* 传感器类型*/
    RG_SENSOR_MAX         = 3,     /* 传感器最大值 */
    RG_SENSOR_MAX_HYST    = 4,     /* 传感器回滞值 */
    RG_SENSOR_MIN         = 5,     /* 传感器最小值 */
    RG_SENSOR_CRIT        = 6,     /* 传感器crit值 */
    RG_SENSOR_RANGE       = 7,     /* 传感器误差值 */
    RG_SENSOR_NOMINAL_VAL = 8,     /* 传感器标称值 */
    RG_SENSOR_HIGH        = 9,     /* 传感器高值 */
    RG_SENSOR_LOW         = 10,    /* 传感器低值 */
} rg_sensor_type_t;

/* sff cpld属性类型 */
typedef enum rg_sff_cpld_attr_e {
    RG_SFF_POWER_ON      = 0x01,
    RG_SFF_TX_FAULT,
    RG_SFF_TX_DIS,
    RG_SFF_PRESENT_RESERVED,
    RG_SFF_RX_LOS,
    RG_SFF_RESET,
    RG_SFF_LPMODE,
    RG_SFF_MODULE_PRESENT,
    RG_SFF_INTERRUPT,
} rg_sff_cpld_attr_t;

/* LED灯类型 */
typedef enum rg_led_e {
    RG_SYS_LED_FRONT   = 0,      /* 前面板SYS灯 */
    RG_SYS_LED_REAR    = 1,      /* 后面板SYS灯 */
    RG_BMC_LED_FRONT   = 2,      /* 前面板BMC灯 */
    RG_BMC_LED_REAR    = 3,      /* 后面板BMC灯 */
    RG_FAN_LED_FRONT   = 4,      /* 前面板风扇灯 */
    RG_FAN_LED_REAR    = 5,      /* 后面板风扇灯 */
    RG_PSU_LED_FRONT   = 6,      /* 前面板电源灯 */
    RG_PSU_LED_REAR    = 7,      /* 后面板电源灯 */
    RG_ID_LED_FRONT    = 8,      /* 前面板定位灯 */
    RG_ID_LED_REAR     = 9,      /* 后面板定位灯 */
    RG_FAN_LED_MODULE  = 10,     /* 风扇模块灯 */
    RG_PSU_LED_MODULE  = 11,     /* 电源模块灯 */
    RG_SLOT_LED_MODULE = 12,     /* 子卡状态灯 */
} rg_led_t;

extern int g_dfd_dbg_level;
extern int g_dfd_fan_dbg_level;
extern int g_dfd_fru_dbg_level;
extern int g_dfd_eeprom_dbg_level;
extern int g_dfd_cpld_dbg_level;
extern int g_dfd_fpga_dbg_level;
extern int g_dfd_sysled_dbg_level;
extern int g_dfd_slot_dbg_level;
extern int g_dfd_sensor_dbg_level;
extern int g_dfd_psu_dbg_level;
extern int g_dfd_sff_dbg_level;
extern int g_dfd_watchdog_dbg_level;

#define RG_MIN(a, b)   ((a) < (b) ? (a) : (b))
#define RG_MAX(a, b)   ((a) > (b) ? (a) : (b))

#define DBG_DEBUG(level, fmt, arg...) do { \
    if (g_dfd_dbg_level & level) { \
        if(level >= DBG_ERROR) { \
            printk(KERN_ERR "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } else { \
            printk(KERN_INFO "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } \
    } \
} while (0)

#define DFD_FAN_DEBUG(level, fmt, arg...) do { \
    if (g_dfd_fan_dbg_level & level) { \
        if(level >= DBG_ERROR) { \
            printk(KERN_ERR "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } else { \
            printk(KERN_INFO "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } \
    } \
} while (0)

#define DBG_FRU_DEBUG(level, fmt, arg...) do { \
    if (g_dfd_fru_dbg_level & level) { \
        if(level >= DBG_ERROR) { \
            printk(KERN_ERR "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } else { \
            printk(KERN_INFO "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } \
    } \
} while (0)

#define DBG_EEPROM_DEBUG(level, fmt, arg...) do { \
    if (g_dfd_eeprom_dbg_level & level) { \
        if(level >= DBG_ERROR) { \
            printk(KERN_ERR "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } else { \
            printk(KERN_INFO "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } \
    } \
} while (0)

#define DBG_CPLD_DEBUG(level, fmt, arg...) do { \
    if (g_dfd_cpld_dbg_level & level) { \
        if(level >= DBG_ERROR) { \
            printk(KERN_ERR "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } else { \
            printk(KERN_INFO "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } \
    } \
} while (0)

#define DBG_FPGA_DEBUG(level, fmt, arg...) do { \
    if (g_dfd_fpga_dbg_level & level) { \
        if(level >= DBG_ERROR) { \
            printk(KERN_ERR "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } else { \
            printk(KERN_INFO "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } \
    } \
} while (0)

#define DBG_SYSLED_DEBUG(level, fmt, arg...) do { \
    if (g_dfd_sysled_dbg_level & level) { \
        if(level >= DBG_ERROR) { \
            printk(KERN_ERR "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } else { \
            printk(KERN_INFO "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } \
    } \
} while (0)

#define DFD_SLOT_DEBUG(level, fmt, arg...) do { \
    if (g_dfd_slot_dbg_level & level) { \
        if(level >= DBG_ERROR) { \
            printk(KERN_ERR "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } else { \
            printk(KERN_INFO "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } \
    } \
} while (0)

#define DFD_SENSOR_DEBUG(level, fmt, arg...) do { \
    if (g_dfd_sensor_dbg_level & level) { \
        if(level >= DBG_ERROR) { \
            printk(KERN_ERR "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } else { \
            printk(KERN_INFO "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } \
    } \
} while (0)

#define DFD_PSU_DEBUG(level, fmt, arg...) do { \
    if (g_dfd_psu_dbg_level & level) { \
        if(level >= DBG_ERROR) { \
            printk(KERN_ERR "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } else { \
            printk(KERN_INFO "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } \
    } \
} while (0)

#define DFD_SFF_DEBUG(level, fmt, arg...) do { \
    if (g_dfd_sff_dbg_level & level) { \
        if(level >= DBG_ERROR) { \
            printk(KERN_ERR "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } else { \
            printk(KERN_INFO "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } \
    } \
} while (0)

#define DFD_WDT_DEBUG(level, fmt, arg...) do { \
    if (g_dfd_watchdog_dbg_level & level) { \
        if(level >= DBG_ERROR) { \
            printk(KERN_ERR "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } else { \
            printk(KERN_INFO "[DBG-%d]:<%s, %d>:"fmt, level, __FUNCTION__, __LINE__, ##arg); \
        } \
    } \
} while (0)

/**
 * rg_dev_cfg_init - dfd模块初始化
 *
 * @returns: <0失败，否则成功
 */
int32_t rg_dev_cfg_init(void);

/**
 * rg_dev_cfg_exit - dfd模块退出
 *
 * @returns: void
 */

void rg_dev_cfg_exit(void);

/**
 * dfd_get_dev_number - 获取设备数量
 * @main_dev_id:主设备号
 * @minor_dev_id:次设备号
 * @returns: <0失败，否则返回设备数量
 */
int dfd_get_dev_number(unsigned int main_dev_id, unsigned int minor_dev_id);
#endif  /* _RG_MODULE_H_ */
