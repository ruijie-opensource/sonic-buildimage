#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from ruijiecommon import *
PCA9548START = -1
PCA9548BUSEND = -2

# 启机模块
STARTMODULE = {
    "fancontrol": 0,
    "avscontrol": 0,
    "xdpe_avscontrol": 1,
    "avscontrol_restful": 0,
    "dev_monitor": 1,
    "hal_fanctrl": 1,
    "hal_ledctrl": 1,
    "intelligent_monitor": 1,
    "sff_temp_polling": 1,
    "rg_pmon_syslog": 1,
    "reboot_cause": 1,
}

DEV_MONITOR_PARAM = {
    "dev_monitor_interval": 5,
    "status_monitor_interval": 0.5,
    "device": [
        {
            "name": "psu1",
            "monitor_point": [
                [
                    {
                        "name": "psu1 present check",
                        "rd_config": {
                            "gettype": "devfile",
                            "path": "/dev/cpld1",
                            "offset": 0x1c,
                            "read_len": 1
                        },
                        "rd_bit": 0,
                        "okval": 0,
                        "gettype": "bit_rd"
                    }
                ]
            ],
            "subdevice": [
                {
                    "id": "psu1pmbus",
                    "stop_monitor_condition": [
                        {
                            "name": "83-0058 file check",
                            "judge_file": "/sys/bus/i2c/devices/83-0058/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "83-0058 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/83-0058/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "83-0058 delete_device",
                            "cmd": "echo 0x58 > /sys/bus/i2c/devices/i2c-83/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "83-0058 new_device",
                            "cmd": "echo rg_fsp1200 0x58 > /sys/bus/i2c/devices/i2c-83/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "psu1frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "83-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/83-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "83-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/83-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "83-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-83/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "83-0050 new_device",
                            "cmd": "echo 24c02 0x50 > /sys/bus/i2c/devices/i2c-83/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                }
            ]
        },
        {
            "name": "psu2",
            "monitor_point": [
                [
                    {
                        "name": "psu2 present check",
                        "rd_config": {
                            "gettype": "devfile",
                            "path": "/dev/cpld1",
                            "offset": 0x1c,
                            "read_len": 1
                        },
                        "rd_bit": 4,
                        "okval": 0,
                        "gettype": "bit_rd"
                    }
                ]
            ],
            "subdevice": [
                {
                    "id": "psu2pmbus",
                    "stop_monitor_condition": [
                        {
                            "name": "84-0058 file check",
                            "judge_file": "/sys/bus/i2c/devices/84-0058/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "84-0058 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/84-0058/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "84-0058 delete_device",
                            "cmd": "echo 0x58 > /sys/bus/i2c/devices/i2c-84/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "84-0058 new_device",
                            "cmd": "echo rg_fsp1200 0x58 > /sys/bus/i2c/devices/i2c-84/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "psu2frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "84-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/84-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "84-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/84-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "84-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-84/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "84-0050 new_device",
                            "cmd": "echo 24c02 0x50 > /sys/bus/i2c/devices/i2c-84/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                }
            ]
        },
        {
            "name": "psu3",
            "monitor_point": [
                [
                    {
                        "name": "psu3 present check",
                        "rd_config": {
                            "gettype": "devfile",
                            "path": "/dev/cpld1",
                            "offset": 0x1d,
                            "read_len": 1
                        },
                        "rd_bit": 4,
                        "okval": 0,
                        "gettype": "bit_rd"
                    }
                ]
            ],
            "subdevice": [
                {
                    "id": "psu3pmbus",
                    "stop_monitor_condition": [
                        {
                            "name": "86-0058 file check",
                            "judge_file": "/sys/bus/i2c/devices/86-0058/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "86-0058 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/86-0058/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "86-0058 delete_device",
                            "cmd": "echo 0x58 > /sys/bus/i2c/devices/i2c-86/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "86-0058 new_device",
                            "cmd": "echo rg_fsp1200 0x58 > /sys/bus/i2c/devices/i2c-86/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "psu3frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "86-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/86-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "86-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/86-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "86-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-86/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "86-0050 new_device",
                            "cmd": "echo 24c02 0x50 > /sys/bus/i2c/devices/i2c-86/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                }
            ]
        },
        {
            "name": "psu4",
            "monitor_point": [
                [
                    {
                        "name": "psu4 present check",
                        "rd_config": {
                            "gettype": "devfile",
                            "path": "/dev/cpld1",
                            "offset": 0x1d,
                            "read_len": 1
                        },
                        "rd_bit": 0,
                        "okval": 0,
                        "gettype": "bit_rd"
                    }
                ]
            ],
            "subdevice": [
                {
                    "id": "psu4pmbus",
                    "stop_monitor_condition": [
                        {
                            "name": "85-0058 file check",
                            "judge_file": "/sys/bus/i2c/devices/85-0058/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "85-0058 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/85-0058/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "85-0058 delete_device",
                            "cmd": "echo 0x58 > /sys/bus/i2c/devices/i2c-85/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "85-0058 new_device",
                            "cmd": "echo rg_fsp1200 0x58 > /sys/bus/i2c/devices/i2c-85/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "psu4frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "85-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/85-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "85-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/85-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "85-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-85/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "85-0050 new_device",
                            "cmd": "echo 24c02 0x50 > /sys/bus/i2c/devices/i2c-85/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                }
            ]
        },
        {
            "name": "fan1",
            "monitor_point": [
                [
                    {
                        "name": "fan1 present check",
                        "rd_config": {
                            "gettype": "devfile",
                            "path": "/dev/cpld8",
                            "offset": 0x30,
                            "read_len": 1
                        },
                        "rd_bit": 0,
                        "okval": 0,
                        "gettype": "bit_rd"
                    }
                ]
            ],
            "subdevice": [
                {
                    "id": "fan1frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "95-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/95-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "95-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/95-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "95-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-95/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "95-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-95/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                }
            ]
        },
        {
            "name": "fan2",
            "monitor_point": [
                [
                    {
                        "name": "fan2 present check",
                        "rd_config": {
                            "gettype": "devfile",
                            "path": "/dev/cpld9",
                            "offset": 0x30,
                            "read_len": 1
                        },
                        "rd_bit": 0,
                        "okval": 0,
                        "gettype": "bit_rd"
                    }
                ]
            ],
            "subdevice": [
                {
                    "id": "fan2frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "104-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/104-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "104-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/104-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "104-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-104/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "104-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-104/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                }
            ]
        },
        {
            "name": "fan3",
            "monitor_point": [
                [
                    {
                        "name": "fan3 present check",
                        "rd_config": {
                            "gettype": "devfile",
                            "path": "/dev/cpld8",
                            "offset": 0x30,
                            "read_len": 1
                        },
                        "rd_bit": 1,
                        "okval": 0,
                        "gettype": "bit_rd"
                    }
                ]
            ],
            "subdevice": [
                {
                    "id": "fan3frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "96-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/96-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "96-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/96-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "96-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-96/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "96-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-96/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                }
            ]
        },
        {
            "name": "fan4",
            "monitor_point": [
                [
                    {
                        "name": "fan4 present check",
                        "rd_config": {
                            "gettype": "devfile",
                            "path": "/dev/cpld9",
                            "offset": 0x30,
                            "read_len": 1
                        },
                        "rd_bit": 1,
                        "okval": 0,
                        "gettype": "bit_rd"
                    }
                ]
            ],
            "subdevice": [
                {
                    "id": "fan4frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "105-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/105-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "105-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/105-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "105-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-105/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "105-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-105/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                }
            ]
        },
        {
            "name": "fan5",
            "monitor_point": [
                [
                    {
                        "name": "fan5 present check",
                        "rd_config": {
                            "gettype": "devfile",
                            "path": "/dev/cpld8",
                            "offset": 0x30,
                            "read_len": 1
                        },
                        "rd_bit": 2,
                        "okval": 0,
                        "gettype": "bit_rd"
                    }
                ]
            ],
            "subdevice": [
                {
                    "id": "fan5frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "97-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/97-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "97-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/97-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "97-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-97/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "97-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-97/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                }
            ]
        },
        {
            "name": "fan6",
            "monitor_point": [
                [
                    {
                        "name": "fan6 present check",
                        "rd_config": {
                            "gettype": "devfile",
                            "path": "/dev/cpld9",
                            "offset": 0x30,
                            "read_len": 1
                        },
                        "rd_bit": 2,
                        "okval": 0,
                        "gettype": "bit_rd"
                    }
                ]
            ],
            "subdevice": [
                {
                    "id": "fan6frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "106-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/106-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "106-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/106-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "106-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-106/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "106-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-106/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                }
            ]
        },
        {
            "name": "fan7",
            "monitor_point": [
                [
                    {
                        "name": "fan7 present check",
                        "rd_config": {
                            "gettype": "devfile",
                            "path": "/dev/cpld8",
                            "offset": 0x30,
                            "read_len": 1
                        },
                        "rd_bit": 3,
                        "okval": 0,
                        "gettype": "bit_rd"
                    }
                ]
            ],
            "subdevice": [
                {
                    "id": "fan7frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "98-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/98-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "98-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/98-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "98-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-98/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "98-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-98/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                }
            ]
        },
        {
            "name": "fan8",
            "monitor_point": [
                [
                    {
                        "name": "fan8 present check",
                        "rd_config": {
                            "gettype": "devfile",
                            "path": "/dev/cpld9",
                            "offset": 0x30,
                            "read_len": 1
                        },
                        "rd_bit": 3,
                        "okval": 0,
                        "gettype": "bit_rd"
                    }
                ]
            ],
            "subdevice": [
                {
                    "id": "fan8frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "107-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/107-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "107-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/107-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "107-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-107/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "107-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-107/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                }
            ]
        },
        {
            "name": "eeprom",
            "subdevice": [
                {
                    "id": "eeprom_1",
                    "stop_monitor_condition": [
                        {
                            "name": "1-0056 file check",
                            "judge_file": "/sys/bus/i2c/devices/1-0056/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "1-0056 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/1-0056/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "1-0056 delete_device",
                            "cmd": "echo 0x56 > /sys/bus/i2c/devices/i2c-1/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "1-0056 new_device",
                            "cmd": "echo 24c02 0x56 > /sys/bus/i2c/devices/i2c-1/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                }
            ]
        },
        {
            "name": "lm75",
            "subdevice": [
                {
                    "id": "lm75_1",
                    "stop_monitor_condition": [
                        {
                            "name": "79-004b file check",
                            "judge_file": "/sys/bus/i2c/devices/79-004b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "79-004b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/79-004b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "79-004b delete_device",
                            "cmd": "echo 0x4b > /sys/bus/i2c/devices/i2c-79/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "79-004b new_device",
                            "cmd": "echo rg_lm75 0x4b > /sys/bus/i2c/devices/i2c-79/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_2",
                    "stop_monitor_condition": [
                        {
                            "name": "93-0048 file check",
                            "judge_file": "/sys/bus/i2c/devices/93-0048/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "93-0048 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/93-0048/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "93-0048 delete_device",
                            "cmd": "echo 0x48 > /sys/bus/i2c/devices/i2c-93/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "93-0048 new_device",
                            "cmd": "echo rg_lm75 0x48 > /sys/bus/i2c/devices/i2c-93/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_3",
                    "stop_monitor_condition": [
                        {
                            "name": "94-0049 file check",
                            "judge_file": "/sys/bus/i2c/devices/94-0049/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "94-0049 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/94-0049/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "94-0049 delete_device",
                            "cmd": "echo 0x49 > /sys/bus/i2c/devices/i2c-94/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "94-0049 new_device",
                            "cmd": "echo rg_lm75 0x49 > /sys/bus/i2c/devices/i2c-94/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_4",
                    "stop_monitor_condition": [
                        {
                            "name": "102-0048 file check",
                            "judge_file": "/sys/bus/i2c/devices/102-0048/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "102-0048 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/102-0048/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "102-0048 delete_device",
                            "cmd": "echo 0x48 > /sys/bus/i2c/devices/i2c-102/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "102-0048 new_device",
                            "cmd": "echo rg_lm75 0x48 > /sys/bus/i2c/devices/i2c-102/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_5",
                    "stop_monitor_condition": [
                        {
                            "name": "103-0049 file check",
                            "judge_file": "/sys/bus/i2c/devices/103-0049/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "103-0049 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/103-0049/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "103-0049 delete_device",
                            "cmd": "echo 0x49 > /sys/bus/i2c/devices/i2c-103/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "103-0049 new_device",
                            "cmd": "echo rg_lm75 0x49 > /sys/bus/i2c/devices/i2c-103/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_6",
                    "stop_monitor_condition": [
                        {
                            "name": "117-004b file check",
                            "judge_file": "/sys/bus/i2c/devices/117-004b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "117-004b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/117-004b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "117-004b delete_device",
                            "cmd": "echo 0x4b > /sys/bus/i2c/devices/i2c-117/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "117-004b new_device",
                            "cmd": "echo rg_lm75 0x4b > /sys/bus/i2c/devices/i2c-117/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_7",
                    "stop_monitor_condition": [
                        {
                            "name": "118-004f file check",
                            "judge_file": "/sys/bus/i2c/devices/118-004f/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "118-004f file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/118-004f/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "118-004f delete_device",
                            "cmd": "echo 0x4f > /sys/bus/i2c/devices/i2c-118/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "118-004f new_device",
                            "cmd": "echo rg_lm75 0x4f > /sys/bus/i2c/devices/i2c-118/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_8",
                    "stop_monitor_condition": [
                        {
                            "name": "198-004b file check",
                            "judge_file": "/sys/bus/i2c/devices/198-004b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "198-004b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/198-004b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "198-004b delete_device",
                            "cmd": "echo 0x4b > /sys/bus/i2c/devices/i2c-198/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "198-004b new_device",
                            "cmd": "echo rg_lm75 0x4b > /sys/bus/i2c/devices/i2c-198/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
            ]
        },
        {
            "name": "ucd90160",
            "subdevice": [
                {
                    "id": "ucd90160_1",
                    "stop_monitor_condition": [
                        {
                            "name": "77-005b file check",
                            "judge_file": "/sys/bus/i2c/devices/77-005b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "77-005b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/77-005b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "77-005b delete_device",
                            "cmd": "echo 0x5b > /sys/bus/i2c/devices/i2c-77/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "77-005b new_device",
                            "cmd": "echo rg_ucd90160 0x5b > /sys/bus/i2c/devices/i2c-77/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "ucd90160_2",
                    "stop_monitor_condition": [
                        {
                            "name": "128-005b file check",
                            "judge_file": "/sys/bus/i2c/devices/128-005b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "128-005b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/128-005b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "128-005b delete_device",
                            "cmd": "echo 0x5b > /sys/bus/i2c/devices/i2c-128/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "128-005b new_device",
                            "cmd": "echo rg_ucd90160 0x5b > /sys/bus/i2c/devices/i2c-128/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "ucd90160_3",
                    "stop_monitor_condition": [
                        {
                            "name": "129-005b file check",
                            "judge_file": "/sys/bus/i2c/devices/129-005b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "129-005b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/129-005b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "129-005b delete_device",
                            "cmd": "echo 0x5b > /sys/bus/i2c/devices/i2c-129/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "129-005b new_device",
                            "cmd": "echo rg_ucd90160 0x5b > /sys/bus/i2c/devices/i2c-129/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "ucd90160_4",
                    "stop_monitor_condition": [
                        {
                            "name": "130-005b file check",
                            "judge_file": "/sys/bus/i2c/devices/130-005b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "130-005b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/130-005b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "130-005b delete_device",
                            "cmd": "echo 0x5b > /sys/bus/i2c/devices/i2c-130/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "130-005b new_device",
                            "cmd": "echo rg_ucd90160 0x5b > /sys/bus/i2c/devices/i2c-130/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
            ]
        },
        {
            "name": "ina3221",
            "subdevice": [
                {
                    "id": "ina3221_1",
                    "stop_monitor_condition": [
                        {
                            "name": "78-0043 file check",
                            "judge_file": "/sys/bus/i2c/devices/78-0043/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "78-0043 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/78-0043/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "78-0043 delete_device",
                            "cmd": "echo 0x43 > /sys/bus/i2c/devices/i2c-78/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "78-0043 new_device",
                            "cmd": "echo rg_ina3221 0x43 > /sys/bus/i2c/devices/i2c-78/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
            ]
        },
        {
            "name": "tps53622",
            "subdevice": [
                {
                    "id": "tps53622_1",
                    "stop_monitor_condition": [
                        {
                            "name": "131-0067 file check",
                            "judge_file": "/sys/bus/i2c/devices/131-0067/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "131-0067 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/131-0067/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "131-0067 delete_device",
                            "cmd": "echo 0x67 > /sys/bus/i2c/devices/i2c-131/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "131-0067 new_device",
                            "cmd": "echo rg_tps53622 0x67 > /sys/bus/i2c/devices/i2c-131/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "tps53622_2",
                    "stop_monitor_condition": [
                        {
                            "name": "78-0067 file check",
                            "judge_file": "/sys/bus/i2c/devices/78-0067/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "78-0067 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/78-0067/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "78-0067 delete_device",
                            "cmd": "echo 0x67 > /sys/bus/i2c/devices/i2c-78/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "78-0067 new_device",
                            "cmd": "echo rg_tps53622 0x67 > /sys/bus/i2c/devices/i2c-78/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "tps53622_3",
                    "stop_monitor_condition": [
                        {
                            "name": "78-006c file check",
                            "judge_file": "/sys/bus/i2c/devices/78-006c/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "78-006c file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/78-006c/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "78-006c delete_device",
                            "cmd": "echo 0x6c > /sys/bus/i2c/devices/i2c-78/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "78-0067 new_device",
                            "cmd": "echo rg_tps53622 0x6c > /sys/bus/i2c/devices/i2c-78/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
            ]
        },
        {
            "name": "mac_bsc",
            "subdevice": [
                {
                    "id": "mac_bsc_1",
                    "stop_monitor_condition": [
                        {
                            "name": "122-0044 file check",
                            "judge_file": "/sys/bus/i2c/devices/122-0044/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "122-0044 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/122-0044/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "122-0044 delete_device",
                            "cmd": "echo 0x44 > /sys/bus/i2c/devices/i2c-122/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "122-0044 new_device",
                            "cmd": "echo rg_mac_bsc_th4 0x44 > /sys/bus/i2c/devices/i2c-122/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
            ]
        },
        {
            "name": "tmp411",
            "subdevice": [
                {
                    "id": "tmp411_1",
                    "stop_monitor_condition": [
                        {
                            "name": "119-004c file check",
                            "judge_file": "/sys/bus/i2c/devices/119-004c/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "119-004c file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/119-004c/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "119-004c delete_device",
                            "cmd": "echo 0x4c > /sys/bus/i2c/devices/i2c-119/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "119-004c new_device",
                            "cmd": "echo rg_tmp411 0x4c > /sys/bus/i2c/devices/i2c-119/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "tmp411_2",
                    "stop_monitor_condition": [
                        {
                            "name": "120-004c file check",
                            "judge_file": "/sys/bus/i2c/devices/120-004c/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "120-004c file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/120-004c/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "120-004c delete_device",
                            "cmd": "echo 0x4c > /sys/bus/i2c/devices/i2c-120/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "120-004c new_device",
                            "cmd": "echo rg_tmp411 0x4c > /sys/bus/i2c/devices/i2c-120/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                }
            ]
        }
    ]
}

CPLDVERSIONS = []
MANUINFO_CONF = {
    "bios": {
        "key": "BIOS",
        "head": True,
        "next": "bmc"
    },
    "bios_vendor": {
        "parent": "bios",
        "key": "Vendor",
        "cmd": "dmidecode -t 0 |grep Vendor",
        "pattern": r".*Vendor",
        "separator": ":",
        "arrt_index": 1,
    },
    "bios_version": {
        "parent": "bios",
        "key": "Version",
        "cmd": "dmidecode -t 0 |grep Version",
        "pattern": r".*Version",
        "separator": ":",
        "arrt_index": 2,
    },
    "bios_date": {
        "parent": "bios",
        "key": "Release Date",
        "cmd": "dmidecode -t 0 |grep Release",
        "pattern": r".*Release Date",
        "separator": ":",
        "arrt_index": 3,
    },

    "bmc": {
        "key": "BMC",
        "next": "onie"
    },

    "onie": {
        "key": "ONIE",
        "next": "cpu"
    },
    "onie_date": {
        "parent": "onie",
        "key": "Build Date",
        "file": "/host/machine.conf",
        "pattern": r"^onie_build_date",
        "separator": "=",
        "arrt_index": 1,
    },
    "onie_version": {
        "parent": "onie",
        "key": "Version",
        "file": "/host/machine.conf",
        "pattern": r"^onie_version",
        "separator": "=",
        "arrt_index": 2,
    },

    "cpu": {
        "key": "CPU",
        "next": "ssd"
    },
    "cpu_vendor": {
        "parent": "cpu",
        "key": "Vendor",
        "cmd": "dmidecode --type processor |grep Manufacturer",
        "pattern": r".*Manufacturer",
        "separator": ":",
        "arrt_index": 1,
    },
    "cpu_model": {
        "parent": "cpu",
        "key": "Device Model",
        "cmd": "dmidecode --type processor | grep Version",
        "pattern": r".*Version",
        "separator": ":",
        "arrt_index": 2,
    },
    "cpu_core": {
        "parent": "cpu",
        "key": "Core Count",
        "cmd": "dmidecode --type processor | grep \"Core Count\"",
        "pattern": r".*Core Count",
        "separator": ":",
        "arrt_index": 3,
    },
    "cpu_thread": {
        "parent": "cpu",
        "key": "Thread Count",
        "cmd": "dmidecode --type processor | grep \"Thread Count\"",
        "pattern": r".*Thread Count",
        "separator": ":",
        "arrt_index": 4,
    },

    "ssd": {
        "key": "SSD",
        "next": "cpld"
    },
    "ssd_model": {
        "parent": "ssd",
        "key": "Device Model",
        "cmd": "smartctl -i /dev/sda |grep \"Device Model\"",
        "pattern": r".*Device Model",
        "separator": ":",
        "arrt_index": 1,
    },
    "ssd_fw": {
        "parent": "ssd",
        "key": "Firmware Version",
        "cmd": "smartctl -i /dev/sda |grep \"Firmware Version\"",
        "pattern": r".*Firmware Version",
        "separator": ":",
        "arrt_index": 2,
    },
    "ssd_user_cap": {
        "parent": "ssd",
        "key": "User Capacity",
        "cmd": "smartctl -i /dev/sda |grep \"User Capacity\"",
        "pattern": r".*User Capacity",
        "separator": ":",
        "arrt_index": 3,
    },

    "cpld": {
        "key": "CPLD",
        "next": "psu"
    },

    "cpld1": {
        "key": "CPLD1",
        "parent": "cpld",
        "arrt_index": 1,
    },
    "cpld1_model": {
        "key": "Device Model",
        "parent": "cpld1",
        "config": "LCMXO3LF-2100C-5BG256C",
        "arrt_index": 1,
    },
    "cpld1_vender": {
        "key": "Vendor",
        "parent": "cpld1",
        "config": "LATTICE",
        "arrt_index": 2,
    },
    "cpld1_desc": {
        "key": "Description",
        "parent": "cpld1",
        "config": "CPU_CPLD",
        "arrt_index": 3,
    },
    "cpld1_version": {
        "key": "Firmware Version",
        "parent": "cpld1",
        "reg": {"loc": "/dev/cpld0", "offset": 0, "len": 4, "gettype": "devfile_ascii"},
        "callback": "cpld_format",
        "arrt_index": 4,
    },

    "cpld2": {
        "key": "CPLD2",
        "parent": "cpld",
        "arrt_index": 2,
    },
    "cpld2_model": {
        "key": "Device Model",
        "parent": "cpld2",
        "config": "LCMXO3LF-2100C-5BG324C",
        "arrt_index": 1,
    },
    "cpld2_vender": {
        "key": "Vendor",
        "parent": "cpld2",
        "config": "LATTICE",
        "arrt_index": 2,
    },
    "cpld2_desc": {
        "key": "Description",
        "parent": "cpld2",
        "config": "CONNECT_CPLD",
        "arrt_index": 3,
    },
    "cpld2_version": {
        "key": "Firmware Version",
        "parent": "cpld2",
        "reg": {"loc": "/dev/cpld1", "offset": 0, "len": 4, "gettype": "devfile_ascii"},
        "callback": "cpld_format",
        "arrt_index": 4,
    },

    "cpld3": {
        "key": "CPLD3",
        "parent": "cpld",
        "arrt_index": 3,
    },
    "cpld3_model": {
        "key": "Device Model",
        "parent": "cpld3",
        "config": "LCMXO3LF-2100C-5BG256C",
        "arrt_index": 1,
    },
    "cpld3_vender": {
        "key": "Vendor",
        "parent": "cpld3",
        "config": "LATTICE",
        "arrt_index": 2,
    },
    "cpld3_desc": {
        "key": "Description",
        "parent": "cpld3",
        "config": "MAC_CPLD_1",
        "arrt_index": 3,
    },
    "cpld3_version": {
        "key": "Firmware Version",
        "parent": "cpld3",
        "reg": {"loc": "/dev/cpld4", "offset": 0, "len": 4, "gettype": "devfile_ascii"},
        "callback": "cpld_format",
        "arrt_index": 4,
    },

    "cpld4": {
        "key": "CPLD4",
        "parent": "cpld",
        "arrt_index": 4,
    },
    "cpld4_model": {
        "key": "Device Model",
        "parent": "cpld4",
        "config": "LCMXO3LF-2100C-5BG256C",
        "arrt_index": 1,
    },
    "cpld4_vender": {
        "key": "Vendor",
        "parent": "cpld4",
        "config": "LATTICE",
        "arrt_index": 2,
    },
    "cpld4_desc": {
        "key": "Description",
        "parent": "cpld4",
        "config": "MAC_CPLD_2",
        "arrt_index": 3,
    },
    "cpld4_version": {
        "key": "Firmware Version",
        "parent": "cpld4",
        "reg": {"loc": "/dev/cpld5", "offset": 0, "len": 4, "gettype": "devfile_ascii"},
        "callback": "cpld_format",
        "arrt_index": 4,
    },

    "cpld5": {
        "key": "CPLD5",
        "parent": "cpld",
        "arrt_index": 5,
    },
    "cpld5_model": {
        "key": "Device Model",
        "parent": "cpld5",
        "config": "LCMXO3LF-2100C-5BG256C",
        "arrt_index": 1,
    },
    "cpld5_vender": {
        "key": "Vendor",
        "parent": "cpld5",
        "config": "LATTICE",
        "arrt_index": 2,
    },
    "cpld5_desc": {
        "key": "Description",
        "parent": "cpld5",
        "config": "PORT_CPLD_1",
        "arrt_index": 3,
    },
    "cpld5_version": {
        "key": "Firmware Version",
        "parent": "cpld5",
        "reg": {"loc": "/dev/cpld6", "offset": 0, "len": 4, "gettype": "devfile_ascii"},
        "callback": "cpld_format",
        "arrt_index": 4,
    },

    "cpld6": {
        "key": "CPLD6",
        "parent": "cpld",
        "arrt_index": 6,
    },
    "cpld6_model": {
        "key": "Device Model",
        "parent": "cpld6",
        "config": "LCMXO3LF-2100C-5BG256C",
        "arrt_index": 1,
    },
    "cpld6_vender": {
        "key": "Vendor",
        "parent": "cpld6",
        "config": "LATTICE",
        "arrt_index": 2,
    },
    "cpld6_desc": {
        "key": "Description",
        "parent": "cpld6",
        "config": "PORT_CPLD_2",
        "arrt_index": 3,
    },
    "cpld6_version": {
        "key": "Firmware Version",
        "parent": "cpld6",
        "reg": {"loc": "/dev/cpld7", "offset": 0, "len": 4, "gettype": "devfile_ascii"},
        "callback": "cpld_format",
        "arrt_index": 4,
    },

    "cpld7": {
        "key": "CPLD7",
        "parent": "cpld",
        "arrt_index": 7,
    },
    "cpld7_model": {
        "key": "Device Model",
        "parent": "cpld7",
        "config": "LCMXO3LF-2100C-5BG256C",
        "arrt_index": 1,
    },
    "cpld7_vender": {
        "key": "Vendor",
        "parent": "cpld7",
        "config": "LATTICE",
        "arrt_index": 2,
    },
    "cpld7_desc": {
        "key": "Description",
        "parent": "cpld7",
        "config": "FAN_CPLD_1",
        "arrt_index": 3,
    },
    "cpld7_version": {
        "key": "Firmware Version",
        "parent": "cpld7",
        "reg": {"loc": "/dev/cpld8", "offset": 0, "len": 4, "gettype": "devfile_ascii"},
        "callback": "cpld_format",
        "arrt_index": 4,
    },

    "cpld8": {
        "key": "CPLD8",
        "parent": "cpld",
        "arrt_index": 8,
    },
    "cpld8_model": {
        "key": "Device Model",
        "parent": "cpld8",
        "config": "LCMXO3LF-2100C-5BG256C",
        "arrt_index": 1,
    },
    "cpld8_vender": {
        "key": "Vendor",
        "parent": "cpld8",
        "config": "LATTICE",
        "arrt_index": 2,
    },
    "cpld8_desc": {
        "key": "Description",
        "parent": "cpld8",
        "config": "FAN_CPLD_2",
        "arrt_index": 3,
    },
    "cpld8_version": {
        "key": "Firmware Version",
        "parent": "cpld8",
        "reg": {"loc": "/dev/cpld9", "offset": 0, "len": 4, "gettype": "devfile_ascii"},
        "callback": "cpld_format",
        "arrt_index": 4,
    },

    "psu": {
        "key": "PSU",
        "next": "fan"
    },

    "psu1": {
        "parent": "psu",
        "key": "PSU1",
        "arrt_index": 1,
    },
    "psu1_hw_version": {
        "key": "Hardware Version",
        "parent": "psu1",
        "extra": {
            "funcname": "getPsu",
            "id": "psu1",
            "key": "hw_version"
        },
        "arrt_index": 1,
    },
    "psu1_fw_version": {
        "key": "Firmware Version",
        "parent": "psu1",
        "config": "NA",
        "arrt_index": 2,
    },

    "psu2": {
        "parent": "psu",
        "key": "PSU2",
        "arrt_index": 2,
    },
    "psu2_hw_version": {
        "key": "Hardware Version",
        "parent": "psu2",
        "extra": {
            "funcname": "getPsu",
            "id": "psu2",
            "key": "hw_version"
        },
        "arrt_index": 1,
    },
    "psu2_fw_version": {
        "key": "Firmware Version",
        "parent": "psu2",
        "config": "NA",
        "arrt_index": 2,
    },
    "psu3": {
        "parent": "psu",
        "key": "PSU3",
        "arrt_index": 3,
    },
    "psu3_hw_version": {
        "key": "Hardware Version",
        "parent": "psu3",
        "extra": {
            "funcname": "getPsu",
            "id": "psu3",
            "key": "hw_version"
        },
        "arrt_index": 1,
    },
    "psu3_fw_version": {
        "key": "Firmware Version",
        "parent": "psu3",
        "config": "NA",
        "arrt_index": 2,
    },

    "psu4": {
        "parent": "psu",
        "key": "PSU4",
        "arrt_index": 4,
    },
    "psu4_hw_version": {
        "key": "Hardware Version",
        "parent": "psu4",
        "extra": {
            "funcname": "getPsu",
            "id": "psu4",
            "key": "hw_version"
        },
        "arrt_index": 1,
    },
    "psu4_fw_version": {
        "key": "Firmware Version",
        "parent": "psu4",
        "config": "NA",
        "arrt_index": 2,
    },

    "fan": {
        "key": "FAN",
        "next": "i210"
    },

    "fan1": {
        "key": "FAN1",
        "parent": "fan",
        "arrt_index": 1,
    },
    "fan1_hw_version": {
        "key": "Hardware Version",
        "parent": "fan1",
        "extra": {
            "funcname": "checkFan",
            "id": "fan1",
            "key": "hw_version"
        },
        "arrt_index": 1,
    },
    "fan1_fw_version": {
        "key": "Firmware Version",
        "parent": "fan1",
        "config": "NA",
        "arrt_index": 2,
    },

    "fan2": {
        "key": "FAN2",
        "parent": "fan",
        "arrt_index": 2,
    },
    "fan2_hw_version": {
        "key": "Hardware Version",
        "parent": "fan2",
        "extra": {
            "funcname": "checkFan",
            "id": "fan2",
            "key": "hw_version"
        },
        "arrt_index": 1,
    },
    "fan2_fw_version": {
        "key": "Firmware Version",
        "parent": "fan2",
        "config": "NA",
        "arrt_index": 2,
    },

    "fan3": {
        "key": "FAN3",
        "parent": "fan",
        "arrt_index": 3,
    },
    "fan3_hw_version": {
        "key": "Hardware Version",
        "parent": "fan3",
        "extra": {
            "funcname": "checkFan",
            "id": "fan3",
            "key": "hw_version"
        },
        "arrt_index": 1,
    },
    "fan3_fw_version": {
        "key": "Firmware Version",
        "parent": "fan3",
        "config": "NA",
        "arrt_index": 2,
    },

    "fan4": {
        "key": "FAN4",
        "parent": "fan",
        "arrt_index": 4,
    },
    "fan4_hw_version": {
        "key": "Hardware Version",
        "parent": "fan4",
        "extra": {
            "funcname": "checkFan",
            "id": "fan4",
            "key": "hw_version"
        },
        "arrt_index": 1,
    },
    "fan4_fw_version": {
        "key": "Firmware Version",
        "parent": "fan4",
        "config": "NA",
        "arrt_index": 2,
    },

    "fan5": {
        "key": "FAN5",
        "parent": "fan",
        "arrt_index": 5,
    },
    "fan5_hw_version": {
        "key": "Hardware Version",
        "parent": "fan5",
        "extra": {
            "funcname": "checkFan",
            "id": "fan5",
            "key": "hw_version"
        },
        "arrt_index": 1,
    },
    "fan5_fw_version": {
        "key": "Firmware Version",
        "parent": "fan5",
        "config": "NA",
        "arrt_index": 2,
    },

    "fan6": {
        "key": "FAN6",
        "parent": "fan",
        "arrt_index": 6,
    },
    "fan6_hw_version": {
        "key": "Hardware Version",
        "parent": "fan6",
        "extra": {
            "funcname": "checkFan",
            "id": "fan6",
            "key": "hw_version"
        },
        "arrt_index": 1,
    },
    "fan6_fw_version": {
        "key": "Firmware Version",
        "parent": "fan6",
        "config": "NA",
        "arrt_index": 2,
    },

    "fan7": {
        "key": "FAN7",
        "parent": "fan",
        "arrt_index": 7,
    },
    "fan7_hw_version": {
        "key": "Hardware Version",
        "parent": "fan7",
        "extra": {
            "funcname": "checkFan",
            "id": "fan7",
            "key": "hw_version"
        },
        "arrt_index": 1,
    },
    "fan7_fw_version": {
        "key": "Firmware Version",
        "parent": "fan7",
        "config": "NA",
        "arrt_index": 2,
    },

    "fan8": {
        "key": "FAN8",
        "parent": "fan",
        "arrt_index": 8,
    },
    "fan8_hw_version": {
        "key": "Hardware Version",
        "parent": "fan8",
        "extra": {
            "funcname": "checkFan",
            "id": "fan8",
            "key": "hw_version"
        },
        "arrt_index": 1,
    },
    "fan8_fw_version": {
        "key": "Firmware Version",
        "parent": "fan8",
        "config": "NA",
        "arrt_index": 2,
    },

    "i210": {
        "key": "NIC",
        "next": "fpga"
    },
    "i210_model": {
        "parent": "i210",
        "config": "NA",
        "key": "Device Model",
        "arrt_index": 1,
    },
    "i210_vendor": {
        "parent": "i210",
        "config": "INTEL",
        "key": "Vendor",
        "arrt_index": 2,
    },
    "i210_version": {
        "parent": "i210",
        "cmd": "sudo ethtool -i eth0",
        "pattern": r"firmware-version",
        "separator": ":",
        "key": "Firmware Version",
        "arrt_index": 3,
    },

    "fpga": {
        "key": "FPGA",
        "next": "others"
    },

    "fpga1": {
        "key": "FPGA1",
        "parent": "fpga",
        "arrt_index": 1,
    },
    "fpga1_model": {
        "parent": "fpga1",
        "config": "XC7A50T-2FGG484I",
        "key": "Device Model",
        "arrt_index": 1,
    },
    "fpga1_vender": {
        "parent": "fpga1",
        "config": "XILINX",
        "key": "Vendor",
        "arrt_index": 2,
    },
    "fpga1_desc": {
        "key": "Description",
        "parent": "fpga1",
        "config": "MAC_FPGA",
        "arrt_index": 3,
    },
    "fpga1_hw_version": {
        "parent": "fpga1",
        "config": "NA",
        "key": "Hardware Version",
        "arrt_index": 4,
    },
    "fpga1_fw_version": {
        "parent": "fpga1",
        "devfile": {"loc": "/dev/fpga0", "offset": 0, "len": 4,"bit_width":4 },
        "key": "Firmware Version",
        "arrt_index": 5,
    },
    "fpga1_date": {
        "parent": "fpga1",
        "devfile": {"loc": "/dev/fpga0", "offset": 4, "len": 4, "bit_width":4 },
        "key": "Build Date",
        "arrt_index": 6,
    },

    "fpga2": {
        "key": "FPGA2",
        "parent": "fpga",
        "arrt_index": 2,
    },
    "fpga2_model": {
        "parent": "fpga2",
        "config": "XC7A50T-2FGG484I",
        "key": "Device Model",
        "arrt_index": 1,
    },
    "fpga2_vender": {
        "parent": "fpga2",
        "config": "XILINX",
        "key": "Vendor",
        "arrt_index": 2,
    },
    "fpga2_desc": {
        "key": "Description",
        "parent": "fpga2",
        "config": "PORT_FPGA",
        "arrt_index": 3,
    },
    "fpga2_hw_version": {
        "parent": "fpga2",
        "config": "NA",
        "key": "Hardware Version",
        "arrt_index": 4,
    },
    "fpga2_fw_version": {
        "parent": "fpga2",
        "devfile": {"loc": "/dev/fpga1", "offset": 0, "len": 4,"bit_width":4 },
        "key": "Firmware Version",
        "arrt_index": 5,
    },
    "fpga2_date": {
        "parent": "fpga2",
        "devfile": {"loc": "/dev/fpga1", "offset": 4, "len": 4, "bit_width":4 },
        "key": "Build Date",
        "arrt_index": 6,
    },

    "others": {
        "key": "OTHERS",
    },
}

PMON_SYSLOG_STATUS = {
    "polling_time": 3,
    "sffs": {
        "present": {"path": ["/sys/rg_plat/sff/*/present"], "ABSENT": 0},
        "nochangedmsgflag": 0,
        "nochangedmsgtime": 60,
        "noprintfirsttimeflag": 1,
        "alias": {
            "sff1": "Ethernet1",
            "sff2": "Ethernet2",
            "sff3": "Ethernet3",
            "sff4": "Ethernet4",
            "sff5": "Ethernet5",
            "sff6": "Ethernet6",
            "sff7": "Ethernet7",
            "sff8": "Ethernet8",
            "sff9": "Ethernet9",
            "sff10": "Ethernet10",
            "sff11": "Ethernet11",
            "sff12": "Ethernet12",
            "sff13": "Ethernet13",
            "sff14": "Ethernet14",
            "sff15": "Ethernet15",
            "sff16": "Ethernet16",
            "sff17": "Ethernet17",
            "sff18": "Ethernet18",
            "sff19": "Ethernet19",
            "sff20": "Ethernet20",
            "sff21": "Ethernet21",
            "sff22": "Ethernet22",
            "sff23": "Ethernet23",
            "sff24": "Ethernet24",
            "sff25": "Ethernet25",
            "sff26": "Ethernet26",
            "sff27": "Ethernet27",
            "sff28": "Ethernet28",
            "sff29": "Ethernet29",
            "sff30": "Ethernet30",
            "sff31": "Ethernet31",
            "sff32": "Ethernet32",
            "sff33": "Ethernet33",
            "sff34": "Ethernet34",
            "sff35": "Ethernet35",
            "sff36": "Ethernet36",
            "sff37": "Ethernet37",
            "sff38": "Ethernet38",
            "sff39": "Ethernet39",
            "sff40": "Ethernet40",
            "sff41": "Ethernet41",
            "sff42": "Ethernet42",
            "sff43": "Ethernet43",
            "sff44": "Ethernet44",
            "sff45": "Ethernet45",
            "sff46": "Ethernet46",
            "sff47": "Ethernet47",
            "sff48": "Ethernet48",
            "sff49": "Ethernet49",
            "sff50": "Ethernet50",
            "sff51": "Ethernet51",
            "sff52": "Ethernet52",
            "sff53": "Ethernet53",
            "sff54": "Ethernet54",
            "sff55": "Ethernet55",
            "sff56": "Ethernet56",
            "sff57": "Ethernet57",
            "sff58": "Ethernet58",
            "sff59": "Ethernet59",
            "sff60": "Ethernet60",
            "sff61": "Ethernet61",
            "sff62": "Ethernet62",
            "sff63": "Ethernet63",
            "sff64": "Ethernet64",
        }
    },
    "fans": {
        "present": {"path": ["/sys/rg_plat/fan/*/present"], "ABSENT": 0},
        "status": [
            {"path": "/sys/rg_plat/fan/%s/motor0/status", 'okval': 1},
            {"path": "/sys/rg_plat/fan/%s/motor1/status", 'okval': 1},
        ],
        "nochangedmsgflag": 1,
        "nochangedmsgtime": 60,
        "noprintfirsttimeflag": 0,
    },
    "psus": {
        "present": {"path": ["/sys/rg_plat/psu/*/present"], "ABSENT": 0},
        "status": [
            {"path": "/sys/rg_plat/psu/%s/output", "okval": 1},
            {"path": "/sys/rg_plat/psu/%s/alert", "okval": 0},
        ],
        "nochangedmsgflag": 1,
        "nochangedmsgtime": 60,
        "noprintfirsttimeflag": 0,
    }
}

#####################MAC调压参数####################################
MAC_AVS_PARAM = {
    0x7e: 0.90090,
    0x82: 0.87820,
    0x86: 0.85640,
    0x8A: 0.83370,
    0x8E: 0.80960,
}

AVS_VOUT_MODE_PARAM = {
    0x18: 256,        # 2^8
    0x17: 512,        # 2^9
    0x16: 1024,       # 2^10
    0x15: 2048,       # 2^11
    0x14: 4096,       # 2^12
}
MAC_DEFAULT_PARAM = {
    "type": 0,                       # type 1表示 不在范围内用默认 / 0表示不在范围内不调
    "default": 0x82,                  # 配合type使用
    "bus": 126,                        # AVSI2C总线地址
    "devno": 0x10,                    # AVS地址
    "loopaddr": 0xff,                 # AVS loop地址
    "loop": 0x06,                     # AVS loop值
    "vout_cmd_addr": 0x42,            # AVS调压地址
    "vout_mode_addr": 0x40,           # AVS调压地址
    "sdktype": 0,                    # type 0表示 不需要移位 / 1 表示需要移位
    "macregloc": 24,                 # 移位操作
    "mask": 0xff,                    # 移位后掩码
    "rov_source": 0,                  # rov_source 0表示从cpld获取rov值 / 1表示从sdk获取rov值
    "cpld_avs": {"bus": 109, "loc": 0x1d, "offset": 0x24, "gettype": "i2c"},
}
#####################MAC调压参数####################################

# 驱动列表
##
BLACKLIST_DRIVERS = [
    {"name": "i2c_i801", "delay": 0},
]

DRIVERLISTS = [
    {"name": "rg_i2c_i801", "delay": 1},
    {"name": "rg_gpio_d1500", "delay": 0},
    {"name": "i2c_dev", "delay": 0},
    {"name": "rg_i2c_algo_bit", "delay": 0},
    {"name": "rg_i2c_gpio", "delay": 0},
    {"name": "i2c_mux", "delay": 0},
    {"name": "rg_gpio_device", "delay": 0},
    {"name": "rg_i2c_gpio_device gpio_sda=17 gpio_scl=1 gpio_udelay=2", "delay": 0},
    {"name": "ruijie_common dfd_my_type=0x4077", "delay": 0},
    {"name": "rg_fpga_pcie", "delay": 0},
    {"name": "rg_pcie_dev", "delay": 0},
    {"name": "rg_pcie_dev_device", "delay": 0},
    {"name": "rg_io_dev", "delay": 0},
    {"name": "rg_i2c_dev", "delay": 0},
    {"name": "rg_spi_ocores", "delay": 0},
    {"name": "rg_spi_ocores_device", "delay": 0},
    {"name": "rg_spi_dev", "delay": 0},
    {"name": "rg_spi_dev_device", "delay": 0},
    {"name": "rg_lpc_drv", "delay": 0},
    {"name": "rg_lpc_drv_device", "delay": 0},
    {"name": "rg_io_dev_device", "delay": 0},
    {"name": "rg_fpga_i2c_bus_drv", "delay": 0},
    {"name": "rg_fpga_i2c_bus_device", "delay": 0},
    {"name": "rg_i2c_mux_pca9641", "delay": 0},
    {"name": "rg_i2c_mux_pca954x", "delay": 0},
    {"name": "rg_i2c_mux_pca954x_device", "delay": 0},
    {"name": "rg_fpga_pca954x_drv", "delay": 0},
    {"name": "rg_fpga_pca954x_device", "delay": 0},
    {"name": "rg_i2c_dev_device", "delay": 0},
    {"name": "rg_wdt", "delay": 0},
    {"name": "rg_wdt_device", "delay": 0},
    {"name": "rg_lm75", "delay": 0},
    {"name": "rg_tmp401", "delay": 0},
    {"name": "rg_optoe", "delay": 0},
    {"name": "at24", "delay": 0},
    {"name": "rg_mac_bsc", "delay": 0},
    {"name": "rg_pmbus_core", "delay": 0},
    {"name": "rg_csu550", "delay": 0},
    {"name": "rg_ina3221", "delay": 0},
    {"name": "rg_tps53622", "delay": 0},
    {"name": "rg_ucd9000", "delay": 0},
    {"name": "rg_ssd_power", "delay": 0},
    {"name": "rg_ssd_power_device", "delay": 0},
    {"name": "firmware_driver_cpld", "delay": 0},
    {"name": "firmware_driver_ispvme", "delay": 0},
    {"name": "firmware_driver_sysfs", "delay": 0},
    {"name": "rg_firmware_upgrade_device", "delay": 0},
    {"name": "hw_test", "delay": 0},
    {"name": "rg_plat_dfd", "delay": 0},
    {"name": "rg_plat_switch", "delay": 0},
    {"name": "rg_plat_fan", "delay": 0},
    {"name": "rg_plat_psu", "delay": 0},
    {"name": "rg_plat_sff", "delay": 0},
    {"name": "rg_plat_sensor", "delay": 0},
    #s3ip
    {"name": "s3ip_sysfs", "delay": 0},
    {"name": "rg_switch_driver", "delay": 0},
    {"name": "syseeprom_device_driver", "delay": 0},
    {"name": "fan_device_driver", "delay": 0},
    {"name": "fpga_device_driver", "delay": 0},
    {"name": "cpld_device_driver", "delay": 0},
    {"name": "sysled_device_driver", "delay": 0},
    {"name": "psu_device_driver", "delay": 0},
    {"name": "transceiver_device_driver", "delay": 0},
    {"name": "temp_sensor_device_driver", "delay": 0},
    {"name": "watchdog_device_driver", "delay": 0},
    {"name": "vol_sensor_device_driver", "delay": 0},
]

DEVICE = [
    {"name": "24c02", "bus": 1, "loc": 0x56},
    {"name": "rg_mac_bsc_th4", "bus": 122, "loc": 0x44},
    # 风扇
    {"name": "24c64", "bus": 95, "loc": 0x50},
    {"name": "24c64", "bus": 96, "loc": 0x50},
    {"name": "24c64", "bus": 97, "loc": 0x50},
    {"name": "24c64", "bus": 98, "loc": 0x50},
    {"name": "24c64", "bus": 104, "loc": 0x50},
    {"name": "24c64", "bus": 105, "loc": 0x50},
    {"name": "24c64", "bus": 106, "loc": 0x50},
    {"name": "24c64", "bus": 107, "loc": 0x50},
    # 电源
    {"name": "24c02", "bus": 83, "loc": 0x50},
    {"name": "rg_fsp1200", "bus": 83, "loc": 0x58},
    {"name": "24c02", "bus": 84, "loc": 0x50},
    {"name": "rg_fsp1200", "bus": 84, "loc": 0x58},
    {"name": "24c02", "bus": 86, "loc": 0x50},
    {"name": "rg_fsp1200", "bus": 86, "loc": 0x58},
    {"name": "24c02", "bus": 85, "loc": 0x50},
    {"name": "rg_fsp1200", "bus": 85, "loc": 0x58},
    # 温度
    {"name": "rg_lm75", "bus": 79, "loc": 0x4b},
    {"name": "rg_lm75", "bus": 93, "loc": 0x48},
    {"name": "rg_lm75", "bus": 94, "loc": 0x49},
    {"name": "rg_lm75", "bus": 102, "loc": 0x48},
    {"name": "rg_lm75", "bus": 103, "loc": 0x49},
    {"name": "rg_lm75", "bus": 117, "loc": 0x4b},
    {"name": "rg_lm75", "bus": 118, "loc": 0x4f},
    {"name": "rg_tmp411", "bus": 119, "loc": 0x4c},
    {"name": "rg_tmp411", "bus": 120, "loc": 0x4c},
    {"name": "rg_lm75", "bus": 198, "loc": 0x4b},
    # dcdc
    {"name": "rg_ucd90160", "bus": 77, "loc": 0x5b},
    {"name": "rg_ina3221", "bus": 78, "loc": 0x43},
    {"name": "rg_tps53622", "bus": 78, "loc": 0x67},
    {"name": "rg_tps53622", "bus": 78, "loc": 0x6C},
    {"name": "rg_ucd90160", "bus": 128, "loc": 0x5b},
    {"name": "rg_ucd90160", "bus": 129, "loc": 0x5b},
    {"name": "rg_ucd90160", "bus": 130, "loc": 0x5b},
    {"name": "rg_tps53622", "bus": 131, "loc": 0x67},
]

OPTOE = [
    {"name": "rg_optoe3", "startbus": 133, "endbus": 196},
]

REBOOT_CTRL_PARAM = {
    "cpu": {"io_addr": 0x920, "rst_val": 0xfe, "rst_delay": 0, "gettype": "io"},
    "mac": {"bus": 109, "loc": 0x1d, "offset": 0x11, "rst_val": 0xfd, "rst_delay": 0, "gettype": "i2c"},
    "phy": {"io_addr": 0x921, "rst_val": 0xef, "rst_delay": 1, "unlock_rst_val": 0xff, "unlock_rst_delay": 1, "gettype": "io"},
}

REBOOT_CAUSE_PARA = {
    "reboot_cause_list": [
        {
            "name": "cold_reboot",
            "monitor_point": {"gettype": "io", "io_addr": 0x926, "okval": 0},
            "record": [
                {"record_type": "file", "mode": "cover", "log": "Power Loss, ",
                    "path": "/etc/.reboot/.previous-reboot-cause.txt"},
                {"record_type": "file", "mode": "add", "log": "Power Loss, ", 
                    "path": "/etc/.reboot/.history-reboot-cause.txt"}
            ]
        },
        {
            "name": "wdt_reboot",
            "monitor_point": {"gettype": "io", "io_addr": 0x929, "okval": 0, "compare_mode":"great"},
            "record": [
                {"record_type": "file", "mode": "cover", "log": "Watchdog reboot, ",
                    "path": "/etc/.reboot/.previous-reboot-cause.txt"},
                {"record_type": "file", "mode": "add", "log": "Watchdog reboot, ",
                    "path": "/etc/.reboot/.history-reboot-cause.txt"}
            ],
            "finish_operation": [
                {"gettype": "io", "io_addr": 0x929, "value": 0x00},
            ]
        },
        {
            "name": "otp_switch_reboot",
            "monitor_point": {"gettype": "file_exist", "judge_file": "/etc/.otp_switch_reboot_flag", "okval":True},
            "record": [
                {"record_type": "file", "mode": "cover", "log": "Thermal Overload: ASIC, ",
                    "path": "/etc/.reboot/.previous-reboot-cause.txt"},
                {"record_type": "file", "mode": "add", "log": "Thermal Overload: ASIC, ", 
                    "path": "/etc/.reboot/.history-reboot-cause.txt"}
            ],
            "finish_operation": [
                {"gettype": "cmd", "cmd": "rm -rf /etc/.otp_switch_reboot_flag"},
            ]
        },
        {
            "name": "otp_other_reboot",
            "monitor_point": {"gettype": "file_exist", "judge_file": "/etc/.otp_other_reboot_flag", "okval":True},
            "record": [
                {"record_type": "file", "mode": "cover", "log": "Thermal Overload: Other, ",
                    "path": "/etc/.reboot/.previous-reboot-cause.txt"},
                {"record_type": "file", "mode": "add", "log": "Thermal Overload: Other, ", 
                    "path": "/etc/.reboot/.history-reboot-cause.txt"}
            ],
            "finish_operation": [
                {"gettype": "cmd", "cmd": "rm -rf /etc/.otp_other_reboot_flag"},
            ]
        },
    ],
    "other_reboot_cause_record": [
        {"record_type": "file", "mode": "cover", "log": "Other, ", "path": "/etc/.reboot/.previous-reboot-cause.txt"},
        {"record_type": "file", "mode": "add", "log": "Other, ", "path": "/etc/.reboot/.history-reboot-cause.txt"}
    ],
}

INIT_PARAM = []

INIT_COMMAND = [
    # 光模块上电
    "dfd_debug io_wr 0x939 0x01",
    "i2cset -f -y 109 0x1d 0x73 0xff",
    "i2cset -f -y 110 0x2d 0x79 0xff",
    "i2cset -f -y 110 0x2d 0x7a 0xff",
    "i2cset -f -y 110 0x2d 0x7b 0xff",
    "i2cset -f -y 111 0x3d 0x76 0xff",
    "i2cset -f -y 111 0x3d 0x77 0xff",
    "i2cset -f -y 112 0x4d 0x79 0xff",
    "i2cset -f -y 112 0x4d 0x7a 0xff",
    "i2cset -f -y 112 0x4d 0x7b 0xff",

    # 使能码流点灯
    "i2cset -f -y 109 0x1d 0xc4 0x1",
    "i2cset -f -y 110 0x2d 0xcc 0x1",
    "i2cset -f -y 111 0x3d 0xc8 0x1",
    "i2cset -f -y 112 0x4d 0xc9 0x1",
]

WARM_UPGRADE_PARAM = {
    "slot0": {
        "VME": {
            "chain1": [
                {"name": "CONNECT_CPLD",
                    "refresh_file_judge_flag": 1,
                    "refresh_file": "/etc/.cpld_refresh/b6980_64qc_refresh_base_cpld_header.vme",
                    "init_cmd": [
                        {"bus": 109, "loc": 0x1d, "offset": 0x1c, "value": 0xff, "gettype": "i2c"},
                        {"io_addr": 0x993, "value": 0, "gettype": "io"},
                    ],
                    "rw_recover_reg": [
                        {"io_addr": 0x911, "value": None, "gettype": "io"},
                        {"io_addr": 0x912, "value": None, "gettype": "io"},
                        {"io_addr": 0x913, "value": None, "gettype": "io"},
                        {"io_addr": 0x914, "value": None, "gettype": "io"},
                        {"io_addr": 0x915, "value": None, "gettype": "io"},
                        {"io_addr": 0x918, "value": None, "gettype": "io"},
                        {"io_addr": 0x919, "value": None, "gettype": "io"},
                        {"io_addr": 0x91a, "value": None, "gettype": "io"},
                        {"io_addr": 0x91b, "value": None, "gettype": "io"},
                        {"io_addr": 0x921, "value": None, "gettype": "io"},
                        {"io_addr": 0x922, "value": None, "gettype": "io"},
                        {"io_addr": 0x923, "value": None, "gettype": "io"},
                        {"io_addr": 0x924, "value": None, "gettype": "io"},
                        {"io_addr": 0x925, "value": None, "gettype": "io"},
                        {"io_addr": 0x928, "value": None, "gettype": "io"},
                        {"io_addr": 0x929, "value": None, "gettype": "io"},
                        {"io_addr": 0x932, "value": None, "gettype": "io"},
                        {"io_addr": 0x933, "value": None, "gettype": "io"},
                        {"io_addr": 0x934, "value": None, "gettype": "io"},
                        {"io_addr": 0x938, "value": None, "gettype": "io"},
                        {"io_addr": 0x939, "value": None, "gettype": "io"},
                        {"io_addr": 0x93a, "value": None, "gettype": "io"},
                        {"io_addr": 0x93b, "value": None, "gettype": "io"},
                        {"io_addr": 0x941, "value": None, "gettype": "io"},
                        {"io_addr": 0x942, "value": None, "gettype": "io"},
                        {"io_addr": 0x949, "value": None, "gettype": "io"},
                        {"io_addr": 0x94d, "value": None, "gettype": "io"},
                        {"io_addr": 0x952, "value": None, "gettype": "io"},
                        {"io_addr": 0x955, "value": None, "gettype": "io"},
                        {"io_addr": 0x972, "value": None, "gettype": "io"},
                        {"io_addr": 0x973, "value": None, "gettype": "io"},
                        {"io_addr": 0x990, "value": None, "gettype": "io"},
                        {"io_addr": 0x991, "value": None, "gettype": "io"},
                        {"io_addr": 0x993, "value": None, "gettype": "io"},
                    ],
                    "save_set_reg": [
                        {"io_addr": 0x927, "value": None, "set_value": 0, "save_value": None, "gettype": "io"},
                    ],
                    "after_upgrade_delay": 30,
                    "after_upgrade_delay_timeout": 60,
                    "refresh_finish_flag_check": {"io_addr": 0x993, "value": 0x01, "gettype": "io"},
                    "access_check_reg": {"io_addr": 0x955, "value": 0x5a, "gettype": "io"},
                    "finish_cmd": [
                        {"bus": 109, "loc": 0x1d, "offset": 0x1c, "value": 0, "gettype": "i2c"},
                    ],
                 },
            ],

            "chain2": [
                {"name": "FAN_CPLD_1",
                    "refresh_file_judge_flag": 1,
                    "refresh_file": "/etc/.cpld_refresh/b6980_64qc_refresh_fana_cpld_header.vme",
                    "rw_recover_reg": [],
                    "after_upgrade_delay": 1,
                    "after_upgrade_delay_timeout": 30,
                    "access_check_reg": {"bus": 92, "loc": 0x0d, "offset": 0xaa, "value": 0x5a, "gettype": "i2c"},
                 },
            ],

            "chain3": [
                {"name": "FAN_CPLD_2",
                    "refresh_file_judge_flag": 1,
                    "refresh_file": "/etc/.cpld_refresh/b6980_64qc_refresh_fanb_cpld_header.vme",
                    "rw_recover_reg": [],
                    "after_upgrade_delay": 1,
                    "after_upgrade_delay_timeout": 30,
                    "access_check_reg": {"bus": 101, "loc": 0x0d, "offset": 0xaa, "value": 0x5a, "gettype": "i2c"},
                 },
            ],

            "chain4": [
                {"name": "MAC_CPLD_1",
                    "refresh_file_judge_flag": 1,
                    "refresh_file": "/etc/.cpld_refresh/b6980_64qc_refresh_mac_cplda_header.vme",
                    "init_cmd": [
                        {"file": WARM_UPG_FLAG, "gettype": "creat_file"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x13, "value": 0xff, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x18, "value": 0x00, "gettype": "i2c"},
                    ],
                    "rw_recover_reg": [
                        {"bus": 109, "loc": 0x1d, "offset": 0x11, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x12, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x13, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x16, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x18, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x1a, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x1b, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x1c, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x21, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x23, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x51, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x52, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x54, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x56, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x57, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x58, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x59, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x5a, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x70, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x72, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x73, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0xaa, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0xc0, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0xc1, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0xc2, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0xc3, "value": None, "gettype": "i2c"},
                        {"bus": 109, "loc": 0x1d, "offset": 0xc4, "value": None, "gettype": "i2c"},
                    ],
                    "after_upgrade_delay": 1,
                    "after_upgrade_delay_timeout": 30,
                    "refresh_finish_flag_check": {"bus": 109, "loc": 0x1d, "offset": 0x18, "value": 0x01, "gettype": "i2c"},
                    "access_check_reg": {"bus": 109, "loc": 0x1d, "offset": 0xaa, "value": 0x5a, "gettype": "i2c"},
                    "finish_cmd": [
                        {"bus": 110, "loc": 0x2d, "offset": 0x13, "value": 0, "gettype": "i2c"},
                        {"file": WARM_UPG_FLAG, "gettype": "remove_file"},
                    ],
                 },

                {"name": "MAC_CPLD_2",
                    "refresh_file_judge_flag": 1,
                    "refresh_file": "/etc/.cpld_refresh/b6980_64qc_refresh_mac_cpldb_header.vme",
                    "init_cmd": [
                        {"file": WARM_UPG_FLAG, "gettype": "creat_file"},
                        {"bus": 109, "loc": 0x1d, "offset": 0x1b, "value": 0xff, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x11, "value": 0x00, "gettype": "i2c"},
                    ],
                    "rw_recover_reg": [
                        {"bus": 110, "loc": 0x2d, "offset": 0x11, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x13, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x52, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x53, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x54, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x56, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x57, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x58, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x59, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x5a, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x5b, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x5c, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x5d, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x5e, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x70, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x71, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x72, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x76, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x77, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x78, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x79, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x7a, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0x7b, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0xaa, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0xc0, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0xc1, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0xc2, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0xc3, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0xc4, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0xc5, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0xc6, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0xc7, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0xc8, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0xc9, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0xca, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0xcb, "value": None, "gettype": "i2c"},
                        {"bus": 110, "loc": 0x2d, "offset": 0xcc, "value": None, "gettype": "i2c"},
                    ],
                    "after_upgrade_delay": 1,
                    "after_upgrade_delay_timeout": 30,
                    "refresh_finish_flag_check": {"bus": 110, "loc": 0x2d, "offset": 0x11, "value": 0x01, "gettype": "i2c"},
                    "access_check_reg": {"bus": 110, "loc": 0x2d, "offset": 0xaa, "value": 0x5a, "gettype": "i2c"},
                    "finish_cmd": [
                        {"bus": 109, "loc": 0x1d, "offset": 0x1b, "value": 0, "gettype": "i2c"},
                        {"file": WARM_UPG_FLAG, "gettype": "remove_file"},
                    ],
                 },
            ],

            "chain5": [
                {"name": "PORT_CPLD_1",
                    "refresh_file_judge_flag": 1,
                    "refresh_file": "/etc/.cpld_refresh/b6980_64qc_refresh_port_cplda_header.vme",
                    "init_cmd": [
                        {"file": WARM_UPG_FLAG, "gettype": "creat_file"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x13, "value": 0xff, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x18, "value": 0x00, "gettype": "i2c"},
                    ],
                    "rw_recover_reg": [
                        {"bus": 111, "loc": 0x3d, "offset": 0x11, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x13, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x14, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x15, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x16, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x18, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x1a, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x1b, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x21, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x51, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x53, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x54, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x56, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x57, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x58, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x59, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x5a, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x5b, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x5c, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x70, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x71, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x74, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x75, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x76, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x77, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0xaa, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0xc0, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0xc1, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0xc2, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0xc3, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0xc4, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0xc5, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0xc6, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0xc7, "value": None, "gettype": "i2c"},
                        {"bus": 111, "loc": 0x3d, "offset": 0xc8, "value": None, "gettype": "i2c"},
                    ],
                    "after_upgrade_delay": 1,
                    "after_upgrade_delay_timeout": 30,
                    "refresh_finish_flag_check": {"bus": 111, "loc": 0x3d, "offset": 0x18, "value": 0x01, "gettype": "i2c"},
                    "access_check_reg": {"bus": 111, "loc": 0x3d, "offset": 0xaa, "value": 0x5a, "gettype": "i2c"},
                    "finish_cmd": [
                        {"bus": 112, "loc": 0x4d, "offset": 0x13, "value": 0, "gettype": "i2c"},
                        {"file": WARM_UPG_FLAG, "gettype": "remove_file"},
                    ],
                 },

                {"name": "PORT_CPLD_2",
                    "refresh_file_judge_flag": 1,
                    "refresh_file": "/etc/.cpld_refresh/b6980_64qc_refresh_port_cpldb_header.vme",
                    "init_cmd": [
                        {"file": WARM_UPG_FLAG, "gettype": "creat_file"},
                        {"bus": 111, "loc": 0x3d, "offset": 0x1b, "value": 0xff, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x11, "value": 0x00, "gettype": "i2c"},
                    ],
                    "rw_recover_reg": [
                        {"bus": 112, "loc": 0x4d, "offset": 0x11, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x13, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x50, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x52, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x53, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x54, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x55, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x56, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x57, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x58, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x59, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x5a, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x5b, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x5c, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x5d, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x5e, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x70, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x71, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x72, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x76, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x77, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x78, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x79, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x7a, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0x7b, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0xaa, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0xc0, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0xc1, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0xc2, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0xc3, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0xc4, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0xc5, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0xc6, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0xc7, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0xc8, "value": None, "gettype": "i2c"},
                        {"bus": 112, "loc": 0x4d, "offset": 0xc9, "value": None, "gettype": "i2c"},

                    ],
                    "after_upgrade_delay": 1,
                    "after_upgrade_delay_timeout": 30,
                    "refresh_finish_flag_check": {"bus": 112, "loc": 0x4d, "offset": 0x11, "value": 0x01, "gettype": "i2c"},
                    "access_check_reg": {"bus": 112, "loc": 0x4d, "offset": 0xaa, "value": 0x5a, "gettype": "i2c"},
                    "finish_cmd": [
                        {"bus": 111, "loc": 0x3d, "offset": 0x1b, "value": 0, "gettype": "i2c"},
                        {"file": WARM_UPG_FLAG, "gettype": "remove_file"},
                    ],
                 },
            ],

            "chain6": [
                {"name": "CPU_CPLD",
                    "refresh_file_judge_flag": 1,
                    "refresh_file": "/etc/.cpld_refresh/b6980_64qc_refresh_cpu_cpld_header.vme",
                    "init_cmd": [
                        {"cmd": "echo 7 > /sys/class/gpio/export", "gettype": "cmd"},
                        {"cmd": "echo out > /sys/class/gpio/gpio7/direction", "gettype": "cmd"},
                        {"cmd": "echo 1 > /sys/class/gpio/gpio7/value", "gettype": "cmd"},
                        {"io_addr": 0x7cc, "value": 0, "gettype": "io"},
                    ],
                    "rw_recover_reg": [
                        {"io_addr": 0x705, "value": None, "gettype": "io"},
                        {"io_addr": 0x713, "value": None, "gettype": "io"},
                        {"io_addr": 0x715, "value": None, "gettype": "io"},
                        {"io_addr": 0x721, "value": None, "gettype": "io"},
                        {"io_addr": 0x722, "value": None, "gettype": "io"},
                        {"io_addr": 0x772, "value": None, "gettype": "io"},
                        {"io_addr": 0x774, "value": None, "gettype": "io"},
                        {"io_addr": 0x776, "value": None, "gettype": "io"},
                        {"io_addr": 0x778, "value": None, "gettype": "io"},
                        {"io_addr": 0x77a, "value": None, "gettype": "io"},
                        {"io_addr": 0x77c, "value": None, "gettype": "io"},
                        {"io_addr": 0x780, "value": None, "gettype": "io"},
                    ],
                    "after_upgrade_delay": 1,
                    "after_upgrade_delay_timeout": 30,
                    "access_check_reg": {"io_addr": 0x705, "value": 0x5a, "gettype": "io"},
                    "finish_cmd": [
                        {"io_addr": 0x7cc, "value": 0xff, "gettype": "io"},
                        {"cmd": "echo 0 > /sys/class/gpio/gpio7/value", "gettype": "cmd"},
                        {"cmd": "echo 7 > /sys/class/gpio/unexport", "gettype": "cmd"},
                    ],
                 },
            ],
        },

        "MTD": {
            "chain1": [
                {"name": "MAC_FPGA",
                    "init_cmd": [
                        {"file": WARM_UPG_FLAG, "gettype": "creat_file"},
                        {"bus": 58, "loc": 0x1c, "offset": 0x23, "value": 0x00, "gettype": "i2c"},
                        {"bus": 58, "loc": 0x1c, "offset": 0x23, "value": 0x01, "gettype": "i2c", "delay": 0.1},
                    ],
                    "after_upgrade_delay": 10,
                    "after_upgrade_delay_timeout": 180,
                    "refresh_finish_flag_check": {"bus": 58, "loc": 0x1c, "offset": 0x23, "value": 0x07, "gettype": "i2c"},
                    "access_check_reg": {
                        "path": "/dev/fpga0", "offset": 0x8, "value": [0x55, 0xaa, 0x5a, 0xa5], "read_len":4, "gettype":"devfile",
                        "polling_cmd":[
                            {"cmd": "rmmod rg_fpga_pcie", "gettype": "cmd"},
                            {"cmd": "modprobe rg_fpga_pcie", "gettype": "cmd", "delay": 0.1},
                        ],
                        "polling_delay": 0.1
                    },
                    "finish_cmd": [
                        {"file": WARM_UPG_FLAG, "gettype": "remove_file"},
                    ],
                 },
            ],
            "chain2": [
                {"name": "PORT_FPGA",
                    "init_cmd": [
                        {"file": WARM_UPG_FLAG, "gettype": "creat_file"},
                        {"bus": 66, "loc": 0x3c, "offset": 0x21, "value": 0x00, "gettype": "i2c"},
                        {"bus": 66, "loc": 0x3c, "offset": 0x21, "value": 0x01, "gettype": "i2c", "delay": 0.1},
                    ],
                    "after_upgrade_delay": 10,
                    "after_upgrade_delay_timeout": 180,
                    "refresh_finish_flag_check": {"bus": 66, "loc": 0x3c, "offset": 0x21, "value": 0x07, "gettype": "i2c"},
                    "access_check_reg": {
                        "path": "/dev/fpga1", "offset": 0x8, "value": [0x55, 0xaa, 0x5a, 0xa5], "read_len":4, "gettype":"devfile",
                        "polling_cmd":[
                            {"cmd": "rmmod rg_fpga_pcie", "gettype": "cmd"},
                            {"cmd": "modprobe rg_fpga_pcie", "gettype": "cmd", "delay": 0.1},
                        ],
                        "polling_delay": 0.1
                    },
                    "finish_cmd": [
                        {"file": WARM_UPG_FLAG, "gettype": "remove_file"},
                    ],
                 },
            ],
        },
    },
    "stop_services_cmd": [
        "rg_platform_process.py stop",
    ],
    "start_services_cmd": [
        "rg_platform_process.py start",
    ],
}

UPGRADE_SUMMARY = {
    "devtype": 0x4077,

    "slot0": {
        "subtype": 0,
        "VME": {
            "chain1": {
                "name": "BASE_CPLD",
                "is_support_warm_upg": 1,
            },
            "chain2": {
                "name": "FANA_CPLD",
                "is_support_warm_upg": 1,
            },
            "chain3": {
                "name": "FANB_CPLD",
                "is_support_warm_upg": 1,
            },
            "chain4": {
                "name": "MAC_CPLD",
                "is_support_warm_upg": 1,
            },
            "chain5": {
                "name": "PORT_CPLD",
                "is_support_warm_upg": 1,
            },
            "chain6": {
                "name": "CPU_CPLD",
                "is_support_warm_upg": 1,
            },
        },

        "MTD": {
            "chain1": {
                "name": "MAC_FPGA",
                "is_support_warm_upg": 1,
                "init_cmd": [
                    {"cmd": "echo 48 > /sys/class/gpio/export", "gettype": "cmd"},
                    {"cmd": "echo out > /sys/class/gpio/gpio48/direction", "gettype": "cmd", "delay": 0.1},
                    {"cmd": "echo 1 > /sys/class/gpio/gpio48/value", "gettype": "cmd"},
                    {"io_addr": 0x991, "value": 0x2, "gettype": "io"},
                    {"io_addr": 0x990, "value": 0xe, "gettype": "io"},
                    {"cmd": "modprobe rg_spi_gpio", "gettype": "cmd"},
                    {"cmd": "modprobe rg_spi_gpio_device sck=65 miso=32 mosi=67 cs=6 bus=0", "gettype": "cmd"},
                    {"cmd": "modprobe rg_spi_nor_device spi_bus_num=0", "gettype": "cmd", "delay": 0.1},
                ],
                "finish_cmd": [
                    {"cmd": "rmmod rg_spi_nor_device", "gettype": "cmd"},
                    {"cmd": "rmmod rg_spi_gpio_device", "gettype": "cmd", "delay": 0.1},
                    {"cmd": "rmmod rg_spi_gpio", "gettype": "cmd", "delay": 0.1},
                    {"cmd": "echo 0 > /sys/class/gpio/gpio48/value", "gettype": "cmd"},
                    {"cmd": "echo 48 > /sys/class/gpio/unexport", "gettype": "cmd", "delay": 0.1},
                    {"io_addr": 0x990, "value": 0x0f, "gettype": "io"},
                    {"io_addr": 0x991, "value": 0x0, "gettype": "io"},
                ],
            },
            "chain2": {
                "name": "PORT_FPGA",
                "is_support_warm_upg": 1,
                "init_cmd": [
                    {"cmd": "echo 48 > /sys/class/gpio/export", "gettype": "cmd"},
                    {"cmd": "echo out > /sys/class/gpio/gpio48/direction", "gettype": "cmd", "delay": 0.1},
                    {"cmd": "echo 1 > /sys/class/gpio/gpio48/value", "gettype": "cmd"},
                    {"io_addr": 0x991, "value": 0x3, "gettype": "io"},
                    {"io_addr": 0x990, "value": 0xb, "gettype": "io"},
                    {"cmd": "modprobe rg_spi_gpio", "gettype": "cmd"},
                    {"cmd": "modprobe rg_spi_gpio_device sck=65 miso=32 mosi=67 cs=6 bus=0", "gettype": "cmd"},
                    {"cmd": "modprobe rg_spi_nor_device spi_bus_num=0", "gettype": "cmd", "delay": 0.1},
                ],
                "finish_cmd": [
                    {"cmd": "rmmod rg_spi_nor_device", "gettype": "cmd"},
                    {"cmd": "rmmod rg_spi_gpio_device", "gettype": "cmd", "delay": 0.1},
                    {"cmd": "rmmod rg_spi_gpio", "gettype": "cmd", "delay": 0.1},
                    {"cmd": "echo 0 > /sys/class/gpio/gpio48/value", "gettype": "cmd"},
                    {"cmd": "echo 48 > /sys/class/gpio/unexport", "gettype": "cmd", "delay": 0.1},
                    {"io_addr": 0x990, "value": 0x0f, "gettype": "io"},
                    {"io_addr": 0x991, "value": 0x0, "gettype": "io"},
                ],
            },
            "chain3": {
                "name": "BIOS",
                "is_support_warm_upg": 0,
                "init_cmd": [
                    {"io_addr": 0x722, "value": 0x02, "gettype": "io"},
                    {"cmd": "modprobe intel_spi_platform writeable=1", "gettype": "cmd"},
                ],
                 "finish_cmd": [
                     {"io_addr": 0x722, "value": 0x02, "gettype": "io"},
                     {"cmd": "rmmod intel_spi_platform", "gettype": "cmd"},
                ],
            },
        },
        "TEST": {
            "fpga": [
                {"chain": 1, "file": "/etc/.upgrade_test/b6980_fpga_test_0_1_header.bin", "display_name": "MAC_FPGA"},
                {"chain": 2, "file": "/etc/.upgrade_test/b6980_fpga_test_0_2_header.bin", "display_name": "PORT_FPGA"},
            ],
            "cpld": [
                {"chain": 1, "file": "/etc/.upgrade_test/b6980_cpld_test_0_1_header.vme", "display_name": "BASE_CPLD"},
                {"chain": 2, "file": "/etc/.upgrade_test/b6980_cpld_test_0_2_header.vme", "display_name": "FANA_CPLD"},
                {"chain": 3, "file": "/etc/.upgrade_test/b6980_cpld_test_0_3_header.vme", "display_name": "FANB_CPLD"},
                {"chain": 4, "file": "/etc/.upgrade_test/b6980_cpld_test_0_4_header.vme", "display_name": "MAC_CPLD"},
                {"chain": 5, "file": "/etc/.upgrade_test/b6980_cpld_test_0_5_header.vme", "display_name": "PORT_CPLD"},
                {"chain": 6, "file": "/etc/.upgrade_test/b6980_cpld_test_0_6_header.vme", "display_name": "CPU_CPLD"},
            ],
        },
    },
}

PLATFORM_E2_CONF = {
    "fan": [
        {"name": "fan1", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/95-0050/eeprom"},
        {"name": "fan2", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/104-0050/eeprom"},
        {"name": "fan3", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/96-0050/eeprom"},
        {"name": "fan4", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/105-0050/eeprom"},
        {"name": "fan5", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/97-0050/eeprom"},
        {"name": "fan6", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/106-0050/eeprom"},
        {"name": "fan7", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/98-0050/eeprom"},
        {"name": "fan8", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/107-0050/eeprom"},
    ],
    "psu": [
        {"name": "psu1", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/83-0050/eeprom"},
        {"name": "psu2", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/84-0050/eeprom"},
        {"name": "psu3", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/86-0050/eeprom"},
        {"name": "psu4", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/85-0050/eeprom"},
    ],
    "syseeprom": [
        {"name": "syseeprom", "e2_type": "onie_tlv", "e2_path": "/sys/bus/i2c/devices/1-0056/eeprom"},
    ],
}
