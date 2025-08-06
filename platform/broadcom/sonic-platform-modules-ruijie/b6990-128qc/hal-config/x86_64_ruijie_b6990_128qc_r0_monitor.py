#coding:utf-8


monitor = {
    "openloop": {
        "linear": {
            "name": "linear",
            "flag": 0,
            "pwm_min": 0x80,
            "pwm_max": 0xff,
            "K": 11,
            "tin_min": 38,
        },
        "curve": {
            "name": "curve",
            "flag": 1,
            "pwm_min": 0x66,
            "pwm_max": 0xff,
            "a": 0.04,
            "b": 4.416,
            "c": -62,
            "tin_min": 25,
        },
    },

    "pid": {
        "CPU_TEMP": {
            "name": "CPU_TEMP",
            "flag": 1,
            "type": "duty",
            "pwm_min": 0x66,
            "pwm_max": 0xff,
            "Kp": 1.5,
            "Ki": 0.3,
            "Kd": 0.3,
            "target": 80,
            "value": [None, None, None],
        },
        "SWITCH_TEMP": {
            "name": "SWITCH_TEMP",
            "flag": 1,
            "type": "duty",
            "pwm_min": 0x66,
            "pwm_max": 0xff,
            "Kp": 0.5,
            "Ki": 0.3,
            "Kd": 0.3,
            "target": 80,
            "value": [None, None, None],
        },
        "OUTLET_TEMP": {
            "name": "OUTLET_TEMP",
            "flag": 1,
            "type": "duty",
            "pwm_min": 0x66,
            "pwm_max": 0xff,
            "Kp": 2,
            "Ki": 0.4,
            "Kd": 0.3,
            "target": 65,
            "value": [None, None, None],
        },
        "BOARD_TEMP": {
            "name": "BOARD_TEMP",
            "flag": 1,
            "type": "duty",
            "pwm_min": 0x66,
            "pwm_max": 0xff,
            "Kp": 2,
            "Ki": 0.4,
            "Kd": 0.3,
            "target": 80,
            "value": [None, None, None],
        },
        "MOS_TEMP": {
            "name": "MOS_TEMP",
            "flag": 1,
            "type": "duty",
            "pwm_min": 0x66,
            "pwm_max": 0xff,
            "Kp": 1,
            "Ki": 0.1,
            "Kd": 0.3,
            "target": 95,
            "value": [None, None, None],
        },
        "SFF_TEMP": {
            "name": "SFF_TEMP",
            "flag": 1,
            "type": "duty",
            "pwm_min": 0x66,
            "pwm_max": 0xff,
            "Kp": 0.1,
            "Ki": 0.2,
            "Kd": 0,
            "target": 62,
            "value": [None, None, None],
        },
    },

    "temps_threshold": {
        "SWITCH_TEMP": {"name": "SWITCH_TEMP", "warning": 100, "critical": 105, "invalid": -100000, "error": -99999},
        "INLET_TEMP": {"name": "INLET_TEMP", "warning": 50, "critical": 55, "fix":-1},
        "OUTLET_TEMP": {"name": "OUTLET_TEMP", "warning": 70, "critical": 75},
        "CPU_TEMP": {"name": "CPU_TEMP", "warning": 90, "critical": 95},
        "BOARD_TEMP": {"name": "BOARD_TEMP", "warning": 85, "critical": 90},
        "MOS_TEMP": {"name": "MOS_TEMP", "warning": 110, "critical": 125},
        "SFF_TEMP": {"name": "SFF_TEMP", "warning": 999, "critical": 1000, "ignore_threshold": 1, "invalid":-10000, "error":-9999},
    },

    "fancontrol_para": {
        "interval": 5,
        "fan_air_flow_monitor": 0,
        "max_pwm": 0xff,
        "min_pwm": 0x66,
        "abnormal_pwm": 0xff,
        "warning_pwm": 0xff,
        "temp_invalid_pid_pwm": 0x66,
        "temp_error_pid_pwm": 0x66,
        "temp_fail_num": 3,
        "check_temp_fail" : [
            {"temp_name" : "INLET_TEMP"},
            {"temp_name" : "SWITCH_TEMP"},
            {"temp_name" : "CPU_TEMP"},
            {"temp_name": "BOARD_TEMP"},
            {"temp_name": "MOS_TEMP"},
        ],
        "temp_warning_num": 3,  # temp over warning 3 times continuously
        "temp_critical_num": 3,  # temp over critical 3 times continuously
        "temp_warning_countdown": 60,  # 5 min warning speed after not warning
        "temp_critical_countdown": 60,  # 5 min full speed after not critical
        "rotor_error_count": 6,  # fan rotor error 6 times continuously
        "inlet_mac_diff": 999,
        "check_crit_reboot_flag": 1,
        "check_crit_reboot_cmd": "i2cset -f -y 89 0x3d 0x15 0 & /sbin/reboot",
        "check_crit_reboot_num": 3,
        "check_crit_sleep_time": 20,
        "psu_absent_fullspeed_num": 0xFF, # 系统全速转-psu不在位数目--关闭psu不在位全速转功能
        "fan_absent_fullspeed_num": 3,  # 系统全速转-fan不在位数目
        "rotor_error_fullspeed_num": 5,  # 系统全速转-马达失效数目
    },

    "ledcontrol_para": {
        "interval": 5,
        "checkpsu": 1, # sys灯需要检测psu状态
        "checkfan": 1, # sys灯需要检测fan状态
        "psu_yellow_num": 1,
        "fan_yellow_num": 1,
        "board_sys_led" : [
            {"led_name" : "FRONT_SYS_LED"},
        ],
        "board_psu_led" : [
            {"led_name" : "FRONT_PSU_LED"},
        ],
        "board_fan_led" : [
            {"led_name" : "FRONT_FAN_LED"},
        ],
        "psu_air_flow_monitor": 0,
        "fan_air_flow_monitor": 0,
    },

    "intelligent_monitor_para": {
        "interval": 60,
    },

    "dcdc_monitor_whitelist": {             #not monitor when checkbit equal okval
        "UPORT_XDPE_QSFP112_VDD3.3V_A_V": {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x32, "checkbit": 1, "okval": 0, "read_len": 1},
        "UPORT_XDPE_QSFP112_VDD3.3V_B_V": {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x32, "checkbit": 0, "okval": 0, "read_len": 1},
        "DPORT_XDPE_QSFP112_VDD3.3V_A_V": {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x32, "checkbit": 1, "okval": 0, "read_len": 1},
        "DPORT_XDPE_QSFP112_VDD3.3V_B_V": {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x32, "checkbit": 0, "okval": 0, "read_len": 1},
        "MAC_XDPE_QSFP112_VDD3.3V_A_V": {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x36, "checkbit": 0, "okval": 0, "read_len": 1},
        "MAC_XDPE_QSFP112_VDD3.3V_B_V": {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x36, "checkbit": 1, "okval": 0, "read_len": 1},
        "MAC_XDPE_QSFP112_VDD3.3V_C_V": {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x36, "checkbit": 2, "okval": 0, "read_len": 1},
        "MAC_XDPE_QSFP112_VDD3.3V_D_V": {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x36, "checkbit": 3, "okval": 0, "read_len": 1},
    },
}
