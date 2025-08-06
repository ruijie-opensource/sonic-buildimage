# coding:utf-8


monitor = {
    "openloop": {
        "linear": {
            "name": "linear",
            "flag": 1,
            "pwm_min": 0x80,
            "pwm_max": 0xff,
            "K": 11,
            "tin_min": 38,
        },
        "curve": {
            "name": "curve",
            "flag": 0,
            "pwm_min": 0x80,
            "pwm_max": 0xff,
            "a": 0.183,
            "b": -6.88,
            "c": 120,
            "tin_min": 25,
        },
    },

    "pid": {
        "CPU_TEMP": {
            "name": "CPU_TEMP",
            "flag": 0,
            "type": "duty",
            "pwm_min": 0x80,
            "pwm_max": 0xff,
            "Kp": 1.5,
            "Ki": 1,
            "Kd": 0.3,
            "target": 90,
            "value": [None, None, None],
        },
        "SWITCH_TEMP": {
            "name": "SWITCH_TEMP",
            "flag": 0,
            "type": "duty",
            "pwm_min": 0x80,
            "pwm_max": 0xff,
            "Kp": 1.5,
            "Ki": 1,
            "Kd": 0.3,
            "target": 90,
            "value": [None, None, None],
        },
    },

    "temps_threshold": {
        "SWITCH_TEMP": {"name": "SWITCH_TEMP", "warning": 100, "critical": 105},
        "INLET_TEMP": {"name": "INLET_TEMP", "warning": 70, "critical": 80},
        "BOARD_TEMP": {"name": "BOARD_TEMP", "warning": 85, "critical": 90},
        "OUTLET_TEMP": {"name": "OUTLET_TEMP", "warning": 85, "critical": 90},
        "CPU_TEMP": {"name": "CPU_TEMP", "warning": 85, "critical": 100},
    },

    "fancontrol_para": {
        "interval": 60,
        "max_pwm": 0xff,
        "min_pwm": 0x80,
        "abnormal_pwm": 0xbb,
        "temp_fail_num": 3,
        "check_temp_fail": [
            {"temp_name": "INLET_TEMP"},
        ],
        "inlet_mac_diff": 50,
        "check_crit_reboot_num": 3,
        "check_crit_sleep_time": 20,
        "psu_absent_fullspeed_num": 1,  # 系统全速转-psu不在位数目
        "fan_absent_fullspeed_num": 1,  # 系统全速转-fan不在位数目
        "rotor_error_fullspeed_num": 1,  # 系统全速转-马达失效数目
    },

    "ledcontrol_para": {
        "interval": 10,
        "checkpsu": 0,  # sys灯需要检测psu状态
        "checkfan": 0,  # sys灯需要检测fan状态
        "psu_yellow_num": 1,
        "fan_yellow_num": 1,
        "board_sys_led": [
            {"led_name": "FRONT_SYS_LED"},
            {"led_name": "BACK_SYS_LED"},
        ],
        "board_psu_led": [
            {"led_name": "FRONT_PSU_LED"},
        ],
        "board_fan_led": [
            {"led_name": "FRONT_FAN_LED"},
        ],
    },
}
