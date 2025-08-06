# coding:utf-8


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
            "pwm_min": 0x80,
            "pwm_max": 0xff,
            "a": 0.369,
            "b": -15.657,
            "c": 289,
            "tin_min": 25,
        },
    },

    "pid": {
        "CPU_TEMP": {
            "name": "CPU_TEMP",
            "flag": 1,
            "type": "duty",
            "pwm_min": 0x80,
            "pwm_max": 0xff,
            "Kp": 1,
            "Ki": 1,
            "Kd": 0.3,
            "target": 80,
            "value": [None, None, None],
        },
        "SWITCH_TEMP": {
            "name": "SWITCH_TEMP",
            "flag": 1,
            "type": "duty",
            "pwm_min": 0x80,
            "pwm_max": 0xff,
            "Kp": 1.5,
            "Ki": 1,
            "Kd": 0.3,
            "target": 90,
            "value": [None, None, None],
        },
        "OUTLET_TEMP": {
            "name": "OUTLET_TEMP",
            "flag": 1,
            "type": "duty",
            "pwm_min": 0x80,
            "pwm_max": 0xff,
            "Kp": 2,
            "Ki": 0.4,
            "Kd": 0.3,
            "target": 65,
            "value": [None, None, None],
        },
        "BOARD_TEMP": {
            "name": "BOARD_TEMP",
            "flag": 0,
            "type": "duty",
            "pwm_min": 0x80,
            "pwm_max": 0xff,
            "Kp": 2,
            "Ki": 0.4,
            "Kd": 0.3,
            "target": 65,
            "value": [None, None, None],
        },
        "SFF_TEMP": {
            "name": "SFF_TEMP",
            "flag": 1,
            "type": "duty",
            "pwm_min": 0x80,
            "pwm_max": 0xff,
            "Kp": 0.1,
            "Ki": 0.4,
            "Kd": 0,
            "target": 62,
            "value": [None, None, None],
        },
    },

    "temps_threshold": {
        "SWITCH_TEMP": {"name": "SWITCH_TEMP", "warning": 100, "critical": 105, "invalid": -100000, "error": -99999},
        "INLET_TEMP": {"name": "INLET_TEMP", "warning": 40, "critical": 50, "fix": -3},
        "BOARD_TEMP": {"name": "BOARD_TEMP", "warning": 70, "critical": 75},
        "OUTLET_TEMP": {"name": "OUTLET_TEMP", "warning": 70, "critical": 75},
        "CPU_TEMP": {"name": "CPU_TEMP", "warning": 100, "critical": 102},
        "SFF_TEMP": {"name": "SFF_TEMP", "warning": 999, "critical": 1000, "ignore_threshold": 1, "invalid": -10000, "error": -9999},
    },

    "fancontrol_para": {
        "interval": 5,
        "fan_status_interval": 0.5,
        "max_pwm": 0xff,
        "min_pwm": 0x80,
        "abnormal_pwm": 0xff,
        "warning_pwm": 0xff,
        "temp_invalid_pid_pwm": 0x80,
        "temp_error_pid_pwm": 0x80,
        "temp_fail_num": 3,
        "check_temp_fail": [
            {"temp_name": "INLET_TEMP"},
            {"temp_name": "SWITCH_TEMP"},
            {"temp_name": "CPU_TEMP"},
        ],
        "temp_warning_num": 3,  # temp over warning 3 times continuously
        "temp_critical_num": 3,  # temp over critical 3 times continuously
        "temp_warning_countdown": 60,  # 5 min warning speed after not warning
        "temp_critical_countdown": 60,  # 5 min full speed after not critical
        "rotor_error_count": 2,  # fan rotor error 2 times continuously
        "inlet_mac_diff": 999,
        "check_crit_reboot_flag": 1,
        "check_crit_reboot_num": 3,
        "check_crit_sleep_time": 20,
        "psu_absent_fullspeed_num": 0xFF,  # 系统全速转-psu不在位数目--关闭psu不在位全速转功能
        "fan_absent_fullspeed_num": 1,  # 系统全速转-fan不在位数目
        "rotor_error_fullspeed_num": 1,  # 系统全速转-马达失效数目
        "psu_fan_control": 1,  # 开启psu风扇控制功能
        "fan_plug_in_default_countdown": 0,  # no use
        "fan_plug_in_pwm": 0x80,  # fan plug in pwd
        "deal_fan_error": 1,  # 处理风扇异常
        "deal_fan_error_conf": {
            "countdown": 2,     # max time:(2-1)*调速周期
            "FAN1": [
                {"name": "FAN1", "pwm": 0xff},
                {"name": "FAN2", "pwm": 0x80},
                {"name": "FAN3", "pwm": 0x80},
                {"name": "FAN4", "pwm": 0x80},
                {"name": "FAN5", "pwm": 0x80},
                {"name": "FAN6", "pwm": 0x80},
            ],
            "FAN2": [
                {"name": "FAN1", "pwm": 0x80},
                {"name": "FAN2", "pwm": 0xff},
                {"name": "FAN3", "pwm": 0x80},
                {"name": "FAN4", "pwm": 0x80},
                {"name": "FAN5", "pwm": 0x80},
                {"name": "FAN6", "pwm": 0x80},
            ],
            "FAN3": [
                {"name": "FAN1", "pwm": 0x80},
                {"name": "FAN2", "pwm": 0x80},
                {"name": "FAN3", "pwm": 0xff},
                {"name": "FAN4", "pwm": 0x80},
                {"name": "FAN5", "pwm": 0x80},
                {"name": "FAN6", "pwm": 0x80},
            ],
            "FAN4": [
                {"name": "FAN1", "pwm": 0x80},
                {"name": "FAN2", "pwm": 0x80},
                {"name": "FAN3", "pwm": 0x80},
                {"name": "FAN4", "pwm": 0xff},
                {"name": "FAN5", "pwm": 0x80},
                {"name": "FAN6", "pwm": 0x80},
            ],
            "FAN5": [
                {"name": "FAN1", "pwm": 0x80},
                {"name": "FAN2", "pwm": 0x80},
                {"name": "FAN3", "pwm": 0x80},
                {"name": "FAN4", "pwm": 0x80},
                {"name": "FAN5", "pwm": 0xff},
                {"name": "FAN6", "pwm": 0x80},
            ],
            "FAN6": [
                {"name": "FAN1", "pwm": 0x80},
                {"name": "FAN2", "pwm": 0x80},
                {"name": "FAN3", "pwm": 0x80},
                {"name": "FAN4", "pwm": 0x80},
                {"name": "FAN5", "pwm": 0x80},
                {"name": "FAN6", "pwm": 0xff},
            ],
        },
    },

    "ledcontrol_para": {
        "interval": 5,
        "checkpsu": 0,  # sys灯需要检测psu状态
        "checkfan": 0,  # sys灯需要检测fan状态
        "psu_yellow_num": 1,
        "fan_yellow_num": 1,
        "board_sys_led": [
            {"led_name": "FRONT_SYS_LED"},
        ],
        "board_psu_led": [
            {"led_name": "FRONT_PSU_LED"},
        ],
        "board_fan_led": [
            {"led_name": "FRONT_FAN_LED"},
        ],
    },
    "otp_reboot_judge_file": {
        "otp_switch_reboot_judge_file": "/etc/.otp_switch_reboot_flag",
        "otp_other_reboot_judge_file": "/etc/.otp_other_reboot_flag",
    },
    "intelligent_monitor_para": {
        "interval": 60,
    },
    "dcdc": {
        "VDD5V_CLK_MCU": {
            "recode_file":"/sys/switch/sensor/in0/in_alarm",
            "format": "int(%s * 1000)",
        },
        "VDD3.3_CLK": {
            "recode_file":"/sys/switch/sensor/in1/in_alarm",
            "format": "int(%s * 1000)",
        },
        "VDD1.0V": {
            "recode_file":"/sys/switch/sensor/in2/in_alarm",
            "format": "int(%s * 1000)",
        },
        "VDD1.8V": {
            "recode_file":"/sys/switch/sensor/in3/in_alarm",
            "format": "int(%s * 1000)",
        },
        "VDD3.3V_A": {
            "recode_file":"/sys/switch/sensor/in4/in_alarm",
            "format": "int(%s * 1000)",
        },
        "VDD1.2V": {
            "recode_file":"/sys/switch/sensor/in5/in_alarm",
            "format": "int(%s * 1000)",
        },
        "VDD_CORE": {
            "recode_file":"/sys/switch/sensor/in6/in_alarm",
            "format": "int(%s * 1000)",
        },
        "ANALOG0.75V": {
            "recode_file":"/sys/switch/sensor/in7/in_alarm",
            "format": "int(%s * 1000)",
        },
        "MAC_VDD1.2V": {
            "recode_file":"/sys/switch/sensor/in8/in_alarm",
            "format": "int(%s * 1000)",
        },
        "VDDO1.8V": {
            "recode_file":"/sys/switch/sensor/in9/in_alarm",
            "format": "int(%s * 1000)",
        },
        "MAC_ANA1.2V": {
            "recode_file":"/sys/switch/sensor/in10/in_alarm",
            "format": "int(%s * 1000)",
        },
        "MAC_ANA1.8V": {
            "recode_file":"/sys/switch/sensor/in11/in_alarm",
            "format": "int(%s * 1000)",
        },
        "QSFP56_VDD3.3V_A": {
            "recode_file":"/sys/switch/sensor/in12/in_alarm",
            "format": "int(%s * 1000)",
        },
        "QSFP56_VDD3.3V_B": {
            "recode_file":"/sys/switch/sensor/in13/in_alarm",
            "format": "int(%s * 1000)",
        },
        "QSFPDD_VDD3.3V_A": {
            "recode_file":"/sys/switch/sensor/in14/in_alarm",
            "format": "int(%s * 1000)",
        },
        "QSFPDD_VDD3.3V_B": {
            "recode_file":"/sys/switch/sensor/in15/in_alarm",
            "format": "int(%s * 1000)",
        },
        "VDD5.0V": {
            "recode_file":"/sys/switch/sensor/in16/in_alarm",
            "format": "int(%s * 1000)",
        },
        "SW_VDD1.2V": {
            "recode_file":"/sys/switch/sensor/in17/in_alarm",
            "format": "int(%s * 1000)",
        },
        "VDD2.5V": {
            "recode_file":"/sys/switch/sensor/in18/in_alarm",
            "format": "int(%s * 1000)",
        },
        "VDD3.3V_B": {
            "recode_file":"/sys/switch/sensor/in19/in_alarm",
            "format": "int(%s * 1000)",
        },
        "P1V7_VCCSCFUSESUS_V": {
            "recode_file":"/sys/switch/sensor/in20/in_alarm",
            "format": "int(%s * 1000)",
        },
        "VDD12V": {
            "recode_file":"/sys/switch/sensor/in21/in_alarm",
            "format": "int(%s * 1000)",
        },
        "VDD3.3_STBY": {
            "recode_file":"/sys/switch/sensor/in22/in_alarm",
            "format": "int(%s * 1000)",
        },
        "SSD_VDD3.3V": {
            "recode_file":"/sys/switch/sensor/in23/in_alarm",
            "format": "int(%s * 1000)",
        },
        "VCCIN_V": {
            "recode_file":"/sys/switch/sensor/in24/in_alarm",
            "format": "int(%s * 1000)",
        },
        "P1V05_V": {
            "recode_file":"/sys/switch/sensor/in25/in_alarm",
            "format": "int(%s * 1000)",
        },
        "VCCD_V": {
            "recode_file":"/sys/switch/sensor/in26/in_alarm",
            "format": "int(%s * 1000)",
        },
        "VCCSCSUS_V": {
            "recode_file":"/sys/switch/sensor/in27/in_alarm",
            "format": "int(%s * 1000)",
        },
        "P5V_AUX_V": {
            "recode_file":"/sys/switch/sensor/in28/in_alarm",
            "format": "int(%s * 1000)",
        },
        "P3V3_STBY_V": {
            "recode_file":"/sys/switch/sensor/in29/in_alarm",
            "format": "int(%s * 1000)",
        },
    },
}
