#ifndef __DFD_CFG_H__
#define __DFD_CFG_H__

#include <linux/list.h>

#define DFD_KO_FILE_NAME_DIR       "/etc/s3ip_sysfs_cfg/ko/file_name/"       /* 库配置文件名称目录 */
#define DFD_KO_CFG_FILE_DIR        "/etc/s3ip_sysfs_cfg/ko/cfg_file/"        /* 库配置文件目录 */
#define DFD_PUB_CARDTYPE_FILE      "/sys/module/ruijie_common/parameters/dfd_my_type"

#define DFD_CFG_CMDLINE_MAX_LEN (256)   /* 配置命令行最大长度 */
#define DFD_CFG_NAME_MAX_LEN    (256)   /* 配置名称最大长度 */
#define DFD_CFG_VALUE_MAX_LEN   (256)   /* 配置值最大长度 */
#define DFD_CFG_STR_MAX_LEN     (64)    /* 字符串配置最大长度 */
#define DFD_CFG_CPLD_NUM_MAX    (16)    /* cpld最大数目 */
#define DFD_PRODUCT_ID_LENGTH   (8)
#define DFD_PID_BUF_LEN         (32)
#define DFD_TEMP_NAME_BUF_LEN   (32)

#define DFD_CFG_EMPTY_VALUE     (-1)    /* 空配置数值 */
#define DFD_CFG_INVALID_VALUE   (0)     /* 配置非法值 */

/* 配置项二叉树key值 */
#define DFD_CFG_KEY(item, index1, index2) \
    ((((item) & 0xff) << 24) | (((index1) & 0xffff) << 8) | ((index2) & 0xff))
#define DFD_CFG_ITEM_ID(key)    (((key) >> 24) & 0xff)
#define DFD_CFG_INDEX1(key)     (((key) >> 8) & 0xffff)
#define DFD_CFG_INDEX2(key)     ((key)& 0xff)

/* 索引值范围 */
#define INDEX_NOT_EXIST     (-1)
#define INDEX1_MAX           (0xffff)
#define INDEX2_MAX           (0xff)

#define DFD_CFG_ITEM_ALL \
    DFD_CFG_ITEM(DFD_CFG_ITEM_NONE, "none", INDEX_NOT_EXIST, INDEX_NOT_EXIST)                       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_DEV_NUM, "dev_num", INDEX1_MAX, INDEX2_MAX)                 \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FAN_THRESHOLD, "fan_threshold", INDEX1_MAX, INDEX2_MAX)   \
    DFD_CFG_ITEM(DFD_CFG_ITEM_LED_STATUS_DECODE, "led_status_decode", INDEX1_MAX, INDEX2_MAX)   \
    DFD_CFG_ITEM(DFD_CFG_ITEM_CPLD_LPC_DEV, "cpld_lpc_dev", INDEX1_MAX, DFD_CFG_CPLD_NUM_MAX)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FAN_TYPE_NUM, "fan_type_num", INDEX1_MAX, INDEX_NOT_EXIST)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_EEPROM_SIZE, "eeprom_size", INDEX1_MAX, INDEX2_MAX)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_DECODE_POWER_FAN_DIR, "decode_power_fan_dir", INDEX1_MAX, INDEX_NOT_EXIST)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_WATCHDOG_ID, "watchdog_id", INDEX1_MAX, INDEX_NOT_EXIST)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_POWER_RSUPPLY, "power_rate_supply", INDEX1_MAX, INDEX_NOT_EXIST)           \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FAN_DIRECTION, "fan_direction", INDEX1_MAX, INDEX2_MAX)   \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FAN_SPEED_MAX, "fan_speed_max", INDEX1_MAX, INDEX_NOT_EXIST)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FAN_SPEED_MIN, "fan_speed_min", INDEX1_MAX, INDEX_NOT_EXIST)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_PSU_OUT_VOL_MAX, "psu_out_vol_max", INDEX1_MAX, INDEX_NOT_EXIST)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_PSU_OUT_VOL_MIN, "psu_out_vol_min", INDEX1_MAX, INDEX_NOT_EXIST)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_INT_END, "end_int", INDEX_NOT_EXIST, INDEX_NOT_EXIST)                 \
                                                                                                    \
    DFD_CFG_ITEM(DFD_CFG_ITEM_CPLD_MODE, "mode_cpld", INDEX1_MAX, DFD_CFG_CPLD_NUM_MAX)                 \
    DFD_CFG_ITEM(DFD_CFG_ITEM_CPLD_NAME, "cpld_name", INDEX1_MAX, INDEX2_MAX)              \
    DFD_CFG_ITEM(DFD_CFG_ITEM_CPLD_TYPE, "cpld_type", INDEX1_MAX, INDEX2_MAX)              \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FPGA_NAME, "fpga_name", INDEX1_MAX, INDEX2_MAX)              \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FPGA_TYPE, "fpga_type", INDEX1_MAX, INDEX2_MAX)              \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FPGA_MODEL_DECODE, "fpga_model_decode", INDEX1_MAX, INDEX_NOT_EXIST)   \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FAN_E2_MODE, "fan_e2_mode", INDEX_NOT_EXIST, INDEX_NOT_EXIST)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FAN_SYSFS_NAME, "fan_sysfs_name", INDEX_NOT_EXIST, INDEX_NOT_EXIST)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_POWER_NAME, "power_name", INDEX1_MAX, INDEX2_MAX)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FAN_NAME, "fan_name", INDEX1_MAX, INDEX2_MAX)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_DECODE_POWER_NAME, "decode_power_name", INDEX1_MAX, INDEX_NOT_EXIST)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_DECODE_FAN_NAME, "decode_fan_name", INDEX1_MAX, INDEX_NOT_EXIST)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_EEPROM_PATH, "eeprom_path", INDEX1_MAX, INDEX2_MAX)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_WATCHDOG_NAME, "watchdog_name", INDEX1_MAX, INDEX2_MAX)              \
    DFD_CFG_ITEM(DFD_CFG_ITEM_PSU_SYSFS_NAME, "psu_sysfs_name", INDEX_NOT_EXIST, INDEX_NOT_EXIST)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_SLOT_SYSFS_NAME, "slot_sysfs_name", INDEX_NOT_EXIST, INDEX_NOT_EXIST)       \
    DFD_CFG_ITEM(DFD_CFG_ITEM_STRING_END, "end_string", INDEX_NOT_EXIST, INDEX_NOT_EXIST)           \
                                                                                                    \
    DFD_CFG_ITEM(DFD_CFG_ITEM_CPLD_I2C_DEV, "cpld_i2c_dev", INDEX1_MAX, INDEX2_MAX)           \
    DFD_CFG_ITEM(DFD_CFG_ITEM_OTHER_I2C_DEV, "other_i2c_dev", INDEX1_MAX, INDEX2_MAX)         \
    DFD_CFG_ITEM(DFD_CFG_ITEM_I2C_DEV_END, "end_i2c_dev", INDEX_NOT_EXIST, INDEX_NOT_EXIST)         \
                                                                                                    \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FAN_ROLL_STATUS, "fan_roll_status", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FAN_SPEED, "fan_speed", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FAN_RATIO, "fan_ratio", INDEX1_MAX, INDEX_NOT_EXIST)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_LED_STATUS, "led_status", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_CPLD_VERSION, "cpld_version", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_CPLD_HW_VERSION, "cpld_hw_version", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_CPLD_TEST_REG, "cpld_test_reg", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_CPLD_RAW, "cpld_raw", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_DEV_PRESENT_STATUS, "dev_present_status", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_PSU_STATUS, "psu_status", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_HWMON_TEMP, "hwmon_temp", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_HWMON_IN, "hwmon_in", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_HWMON_CURR, "hwmon_curr", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_HWMON_PSU, "hwmon_psu", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_SFF_OPTOE_TYPE, "sff_optoe_type", INDEX1_MAX, INDEX_NOT_EXIST)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_HWMON_POWER, "hwmon_power", INDEX1_MAX, INDEX2_MAX) \
    DFD_CFG_ITEM(DFD_CFG_ITEM_SFF_CPLD_REG, "sff_cpld_reg", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FPGA_VERSION, "fpga_version", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FPGA_TEST_REG, "fpga_test_reg", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_FPGA_MODEL_REG, "fpga_model_reg", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_PSU_PMBUS_REG, "psu_pmbus_reg", INDEX1_MAX, INDEX2_MAX)  \
    DFD_CFG_ITEM(DFD_CFG_ITEM_WATCHDOG_DEV, "watchdog_dev", INDEX1_MAX, INDEX2_MAX)              \
    DFD_CFG_ITEM(DFD_CFG_ITEM_INFO_CTRL_END, "end_info_ctrl", INDEX_NOT_EXIST, INDEX_NOT_EXIST)     \
    DFD_CFG_ITEM(DFD_CFG_ITEM_POWER_STATUS, "power_status", INDEX1_MAX, INDEX2_MAX)  \

/* 配置项id枚举定义 */
#ifdef DFD_CFG_ITEM
#undef DFD_CFG_ITEM
#endif
#define DFD_CFG_ITEM(_id, _name, _index_min, _index_max)    _id,
typedef enum dfd_cfg_item_id_s {
    DFD_CFG_ITEM_ALL
} dfd_cfg_item_id_t;

#define DFD_CFG_ITEM_IS_INT(item_id) \
    (((item_id) > DFD_CFG_ITEM_NONE) && ((item_id) < DFD_CFG_ITEM_INT_END))

#define DFD_CFG_ITEM_IS_STRING(item_id) \
    (((item_id) > DFD_CFG_ITEM_INT_END) && ((item_id) < DFD_CFG_ITEM_STRING_END))

#define DFD_CFG_ITEM_IS_I2C_DEV(item_id) \
    (((item_id) > DFD_CFG_ITEM_STRING_END) && ((item_id) < DFD_CFG_ITEM_I2C_DEV_END))

#define DFD_CFG_ITEM_IS_INFO_CTRL(item_id) \
    (((item_id) > DFD_CFG_ITEM_I2C_DEV_END) && ((item_id) < DFD_CFG_ITEM_INFO_CTRL_END))

/* 索引值范围结构 */
typedef struct index_range_s {
    int index1_max;             /* 一级索引值最大值 */
    int index2_max;             /* 二级索引值最大值 */
} index_range_t;

/* 寄存器值转换节点 */
typedef struct val_convert_node_s {
    struct list_head lst;
    int int_val;                        /* 整型值 */
    char str_val[DFD_CFG_STR_MAX_LEN];  /* 字符串值 */
    int index1;                         /* 索引值1 */
    int index2;                         /* 索引值2 */
} val_convert_node_t;

/**
 * dfd_ko_cfg_get_item - 获取配置项
 * @key: 节点key
 *
 * @returns: NULL配置项不存在，其他成功
 */
void *dfd_ko_cfg_get_item(int key);

/**
 * dfd_ko_cfg_show_item - 显示配置项
 * @key: 节点key
 */
void dfd_ko_cfg_show_item(int key);

/**
 * dfd_dev_cfg_init - 模块初始化
 *
 * @returns: <0失败，否则成功
 */
int32_t dfd_dev_cfg_init(void);

/**
 * dfd_dev_cfg_exit - 模块退出
 *
 * @returns: void
 */
void dfd_dev_cfg_exit(void);

/* 剔除空格和回车换行 */
void dfd_ko_cfg_del_space_lf_cr(char *str);

/**
 * dfd_ko_cfg_get_fan_direction_by_name - 通过风扇名称获取风道类型
 * @fan_name: 风扇名称
 * @fan_direction: 风道类型
 *
 * @returns: 0成功，否则失败
 */
int dfd_ko_cfg_get_fan_direction_by_name(char *fan_name, int *fan_direction);

/**
 * dfd_ko_cfg_get_power_type_by_name - 通过电源名称获取电源类型
 * @power_name: 电源名称
 * @power_type: 电源类型
 * @returns: 0成功，否则失败
 */
int dfd_ko_cfg_get_power_type_by_name(char *power_name, int *power_type);

/**
 * dfd_ko_cfg_get_led_status_decode2_by_regval - 反查led状态的寄存器值
 * @regval: 定义的led值
 * @index1: led类型
 * @*value: 获取led状态的寄存器值
 * @returns: 0成功，否则失败
 */
int dfd_ko_cfg_get_led_status_decode2_by_regval(int regval, int index1, int *value);

/**
 * dfd_ko_cfg_get_fan_direction_by_name - 通过风扇名称获取风扇类型
 * @fan_name: 风扇名称
 * @fan_type: 风扇类型
 * @sub_type: 风扇子类型
 *
 * @returns: 0成功，否则失败
 */
int dfd_ko_cfg_get_fan_type_by_name(char *fan_name, int *fan_type, int *sub_type);

#endif /* __DFD_CFG_H__ */
