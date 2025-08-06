#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from ruijiecommon import *

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
    "rg_pmon_syslog":1,
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
                            "path": "/dev/cpld4",
                            "offset": 0x34,
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
                            "name": "81-0058 file check",
                            "judge_file": "/sys/bus/i2c/devices/81-0058/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "81-0058 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/81-0058/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "81-0058 delete_device",
                            "cmd": "echo 0x58 > /sys/bus/i2c/devices/i2c-81/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "81-0058 new_device",
                            "cmd": "echo rg_fsp1200 0x58 > /sys/bus/i2c/devices/i2c-81/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "psu1frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "81-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/81-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "81-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/81-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "81-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-81/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "81-0050 new_device",
                            "cmd": "echo 24c02 0x50 > /sys/bus/i2c/devices/i2c-81/new_device",
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
                            "path": "/dev/cpld4",
                            "offset": 0x34,
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
                            "name": "82-0058 file check",
                            "judge_file": "/sys/bus/i2c/devices/82-0058/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "82-0058 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/82-0058/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "82-0058 delete_device",
                            "cmd": "echo 0x58 > /sys/bus/i2c/devices/i2c-82/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "82-0058 new_device",
                            "cmd": "echo rg_fsp1200 0x58 > /sys/bus/i2c/devices/i2c-82/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "psu2frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "82-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/82-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "82-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/82-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "82-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-82/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "82-0050 new_device",
                            "cmd": "echo 24c02 0x50 > /sys/bus/i2c/devices/i2c-82/new_device",
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
                            "path": "/dev/cpld6",
                            "offset": 0x37,
                            "read_len": 1
                        },
                        "rd_bit": 5,
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
                            "name": "75-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/75-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "75-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/75-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "75-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-75/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "75-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-75/new_device",
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
                            "path": "/dev/cpld6",
                            "offset": 0x37,
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
                    "id": "fan2frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "74-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/74-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "74-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/74-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "74-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-74/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "74-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-74/new_device",
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
                            "path": "/dev/cpld6",
                            "offset": 0x37,
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
                    "id": "fan3frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "73-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/73-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "73-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/73-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "73-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-73/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "73-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-73/new_device",
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
                            "path": "/dev/cpld6",
                            "offset": 0x37,
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
                    "id": "fan4frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "72-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/72-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "72-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/72-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "72-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-72/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "72-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-72/new_device",
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
                            "path": "/dev/cpld6",
                            "offset": 0x37,
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
                    "id": "fan5frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "71-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/71-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "71-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/71-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "71-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-71/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "71-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-71/new_device",
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
                            "path": "/dev/cpld6",
                            "offset": 0x37,
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
                    "id": "fan6frue2",
                    "stop_monitor_condition": [
                        {
                            "name": "70-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/70-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "70-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/70-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "70-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-70/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "70-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-70/new_device",
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
                            "name": "76-0048 file check",
                            "judge_file": "/sys/bus/i2c/devices/76-0048/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "76-0048 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/79-0048/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "76-0048 delete_device",
                            "cmd": "echo 0x48 > /sys/bus/i2c/devices/i2c-76/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "76-0048 new_device",
                            "cmd": "echo rg_lm75 0x48 > /sys/bus/i2c/devices/i2c-76/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_2",
                    "stop_monitor_condition": [
                        {
                            "name": "76-0049 file check",
                            "judge_file": "/sys/bus/i2c/devices/76-0049/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "76-0049 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/76-0049/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "76-0049 delete_device",
                            "cmd": "echo 0x49 > /sys/bus/i2c/devices/i2c-76/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "76-0049 new_device",
                            "cmd": "echo rg_lm75 0x49 > /sys/bus/i2c/devices/i2c-76/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_3",
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
                    "id": "lm75_4",
                    "stop_monitor_condition": [
                        {
                            "name": "80-004e file check",
                            "judge_file": "/sys/bus/i2c/devices/80-004e/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "80-004e file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/80-004e/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "80-004e delete_device",
                            "cmd": "echo 0x4e > /sys/bus/i2c/devices/i2c-80/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "80-004e new_device",
                            "cmd": "echo rg_lm75 0x4e > /sys/bus/i2c/devices/i2c-80/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_5",
                    "stop_monitor_condition": [
                        {
                            "name": "80-004f file check",
                            "judge_file": "/sys/bus/i2c/devices/80-004f/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "80-004f file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/80-004f/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "80-004f delete_device",
                            "cmd": "echo 0x4f > /sys/bus/i2c/devices/i2c-80/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "80-004f new_device",
                            "cmd": "echo rg_lm75 0x4f > /sys/bus/i2c/devices/i2c-80/new_device",
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
                            "name": "64-005b file check",
                            "judge_file": "/sys/bus/i2c/devices/64-005b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "64-005b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/64-005b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "64-005b delete_device",
                            "cmd": "echo 0x5b > /sys/bus/i2c/devices/i2c-64/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "64-005b new_device",
                            "cmd": "echo rg_ucd90160 0x5b > /sys/bus/i2c/devices/i2c-64/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "ucd90160_2",
                    "stop_monitor_condition": [
                        {
                            "name": "85-005b file check",
                            "judge_file": "/sys/bus/i2c/devices/85-005b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "85-005b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/85-005b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "85-005b delete_device",
                            "cmd": "echo 0x5b > /sys/bus/i2c/devices/i2c-85/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "85-005b new_device",
                            "cmd": "echo rg_ucd90160 0x5b > /sys/bus/i2c/devices/i2c-85/new_device",
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
                            "name": "65-0043 file check",
                            "judge_file": "/sys/bus/i2c/devices/65-0043/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "65-0043 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/65-0043/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "65-0043 delete_device",
                            "cmd": "echo 0x43 > /sys/bus/i2c/devices/i2c-65/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "65-0043 new_device",
                            "cmd": "echo rg_ina3221 0x43 > /sys/bus/i2c/devices/i2c-65/new_device",
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
                            "name": "65-0067 file check",
                            "judge_file": "/sys/bus/i2c/devices/65-0067/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "65-0067 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/65-0067/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "65-0067 delete_device",
                            "cmd": "echo 0x67 > /sys/bus/i2c/devices/i2c-65/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "65-0067 new_device",
                            "cmd": "echo rg_tps53622 0x67 > /sys/bus/i2c/devices/i2c-65/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "tps53622_2",
                    "stop_monitor_condition": [
                        {
                            "name": "65-006c file check",
                            "judge_file": "/sys/bus/i2c/devices/65-006c/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "65-006c file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/65-006c/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "65-006c delete_device",
                            "cmd": "echo 0x6c > /sys/bus/i2c/devices/i2c-65/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "65-006c new_device",
                            "cmd": "echo rg_tps53622 0x6c > /sys/bus/i2c/devices/i2c-65/new_device",
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
                            "name": "84-0044 file check",
                            "judge_file": "/sys/bus/i2c/devices/84-0044/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "84-0044 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/84-0044/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "84-0044 delete_device",
                            "cmd": "echo 0x44 > /sys/bus/i2c/devices/i2c-84/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "84-0044 new_device",
                            "cmd": "echo rg_mac_bsc_td4 0x44 > /sys/bus/i2c/devices/i2c-84/new_device",
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
                            "name": "79-004c file check",
                            "judge_file": "/sys/bus/i2c/devices/79-004c/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "79-004c file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/79-004c/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "79-004c delete_device",
                            "cmd": "echo 0x4c > /sys/bus/i2c/devices/i2c-79/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "79-004c new_device",
                            "cmd": "echo rg_tmp411 0x4c > /sys/bus/i2c/devices/i2c-79/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "tmp411_2",
                    "stop_monitor_condition": [
                        {
                            "name": "80-004c file check",
                            "judge_file": "/sys/bus/i2c/devices/80-004c/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "80-004c file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/80-004c/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "80-004c delete_device",
                            "cmd": "echo 0x4c > /sys/bus/i2c/devices/i2c-80/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "80-004c new_device",
                            "cmd": "echo rg_tmp411 0x4c > /sys/bus/i2c/devices/i2c-80/new_device",
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
        "config": "LCMXO3LF-2100C-5BG256C",
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
        "config": "CONNECT_CPLDA",
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
        "config": "MACA_CPLD",
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
        "config": "MACB_CPLD",
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
        "config": "FAN_CPLD",
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
        "config": "MACC_CPLD",
        "arrt_index": 3,
    },
    "cpld6_version": {
        "key": "Firmware Version",
        "parent": "cpld6",
        "reg": {"loc": "/dev/cpld7", "offset": 0, "len": 4, "gettype": "devfile_ascii"},
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
    "fpga_model": {
        "parent": "fpga",
        "config": "XC7A50T-2FGG484I",
        "key": "Device Model",
        "arrt_index": 1,
    },
    "fpga_vendor": {
        "parent": "fpga",
        "config": "XILINX",
        "key": "Vendor",
        "arrt_index": 2,
    },
    "fpga_desc": {
        "parent": "fpga",
        "config": "NA",
        "key": "Description",
        "arrt_index": 3,
    },
    "fpga_hw_version": {
        "parent": "fpga",
        "config": "NA",
        "key": "Hardware Version",
        "arrt_index": 4,
    },
    "fpga_fw_version": {
        "parent": "fpga",
        "devfile": {"loc": "/dev/fpga0", "offset": 0, "len": 4,"bit_width":4 },
        "key": "Firmware Version",
        "arrt_index": 5,
    },
    "fpga_date": {
        "parent": "fpga",
        "devfile": {"loc": "/dev/fpga0", "offset": 4, "len": 4, "bit_width":4 },
        "key": "Build Date",
        "arrt_index": 6,
    },
    "others": {
        "key": "OTHERS",
    },

    "5387": {
    "parent": "others",
    "key": "CPU-BMC-SWITCH",
    "arrt_index": 1,
    },
    "5387_model": {
        "parent": "5387",
        "config": "BCM5387",
        "key": "Device Model",
        "arrt_index": 1,
    },
    "5387_vendor": {
        "parent": "5387",
        "config": "Broadcom",
        "key": "Vendor",
        "arrt_index": 2,
    },
    "5387_hw_version": {
        "parent": "5387",
        "key": "Hardware Version",
        "func": {
            "funcname": "get_bcm5387_version",
            "params": {
                "before": [
                    {"gettype": "cmd", "cmd": "echo 50 > /sys/class/gpio/export"},
                    {"gettype": "cmd", "cmd": "echo out > /sys/class/gpio/gpio50/direction"},
                    {"gettype": "cmd", "cmd": "echo 1 > /sys/class/gpio/gpio50/value"},
                    {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4d, "value":0xfe},  # enable 5387 
                ],
                "get_version": "md5sum /sys/bus/spi/devices/spi0.0/eeprom | awk '{print $1}'",
                "after": [
                    {"gettype": "cmd", "cmd": "echo 0 > /sys/class/gpio/gpio50/value"},
                    {"gettype": "cmd", "cmd": "echo 50 > /sys/class/gpio/unexport"},
                ],
                "finally": [
                    {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4d, "value":0xff}, # close 5387
                ],
            },
        },
        "arrt_index": 3,
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
    0x72: 0.90000,
    0x73: 0.89375,
    0x74: 0.88750,
    0x75: 0.88125,
    0x76: 0.87500,
    0x77: 0.86875,
    0x78: 0.86250,
    0x79: 0.85625,
    0x7a: 0.85000,
    0x7b: 0.84375,
    0x7c: 0.83750,
    0x7d: 0.83125,
    0x7e: 0.82500,
    0x7f: 0.81875,
    0x80: 0.81250,
    0x81: 0.80625,
    0x82: 0.80000,
    0x83: 0.79375,
    0x84: 0.78750,
    0x85: 0.78125,
    0x86: 0.77500,
    0x87: 0.76875,
    0x88: 0.76250,
    0x89: 0.75625,
    0x8A: 0.75000,
    0x8B: 0.74375,
    0x8C: 0.73750,
    0x8D: 0.73125,
    0x8E: 0.72500,
}

AVS_VOUT_MODE_PARAM = {
    0x18: 256,        # 2^8
    0x17: 512,        # 2^9
    0x16: 1024,       # 2^10
    0x15: 2048,       # 2^11
    0x14: 4096,       # 2^12
}
MAC_DEFAULT_PARAM = {
    "type": 1,                       # type 1表示 不在范围内用默认 / 0表示不在范围内不调
    "default": 0x82,                  # 配合type使用
    "bus": 83,                        # AVSI2C总线地址
    "devno": 0x5b,                    # AVS地址
    "loopaddr": 0xff,                 # AVS loop地址
    "loop": 0x06,                     # AVS loop值
    "vout_cmd_addr": 0x42,            # AVS调压地址
    "vout_mode_addr": 0x40,           # AVS调压地址
    "sdktype": 0,                    # type 0表示 不需要移位 / 1 表示需要移位
    "macregloc": 24,                 # 移位操作
    "mask": 0xff,                    # 移位后掩码
    "rov_source": 0,                  # rov_source 0表示从cpld获取rov值 / 1表示从sdk获取rov值
    "cpld_avs": {"bus": 2, "loc": 0x2d, "offset": 0x46, "gettype": "i2c"},
    "set_avs": {"loc": "/sys/bus/i2c/devices/83-005b/avs_vout", "gettype": "sysfs", "formula": "int((%f)*1000000)"},
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
    {"name": "ruijie_common dfd_my_type=0x40ca", "delay": 0},
    {"name": "rg_fpga_pcie", "delay": 0},
    {"name": "rg_pcie_dev", "delay": 0},
    {"name": "rg_pcie_dev_device", "delay": 0},
    {"name": "rg_lpc_drv", "delay": 0},
    {"name": "rg_lpc_drv_device", "delay": 0},
    {"name": "rg_io_dev", "delay": 0},
    {"name": "rg_io_dev_device", "delay": 0},
    {"name": "rg_i2c_dev", "delay": 0},
    {"name": "rg_fpga_i2c_bus_drv", "delay": 0},
    {"name": "rg_fpga_i2c_bus_device", "delay": 0},
    {"name": "rg_i2c_dev_device", "delay": 0},
    {"name": "rg_fpga_pca954x_drv", "delay": 0},
    {"name": "rg_fpga_pca954x_device", "delay": 0},
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
    {"name": "rg_xdpe132g5c", "delay": 0},
    {"name": "rg_spi_gpio_device", "delay":0},
    {"name": "rg_eeprom_93xx46", "delay": 0},
    {"name": "rg_ssd_power", "delay": 0},
    {"name": "rg_ssd_power_device", "delay": 0},
    {"name": "firmware_driver_cpld", "delay":0},
    {"name": "firmware_driver_ispvme", "delay":0},
    {"name": "firmware_driver_sysfs", "delay":0},
    {"name": "rg_firmware_upgrade_device", "delay":0},

    {"name": "rg_plat_dfd", "delay": 0},
    {"name": "rg_plat_switch", "delay": 0},
    {"name": "rg_plat_fan", "delay": 0},
    {"name": "rg_plat_psu", "delay": 0},
    {"name": "rg_plat_sff", "delay": 0},
    {"name": "rg_plat_sensor", "delay": 0},
    {"name": "hw_test", "delay": 0},
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
    {"name": "rg_mac_bsc_td4", "bus": 84, "loc": 0x44},
    # 风扇
    {"name": "24c64", "bus": 70, "loc": 0x50},
    {"name": "24c64", "bus": 71, "loc": 0x50},
    {"name": "24c64", "bus": 72, "loc": 0x50},
    {"name": "24c64", "bus": 73, "loc": 0x50},
    {"name": "24c64", "bus": 74, "loc": 0x50},
    {"name": "24c64", "bus": 75, "loc": 0x50},
    # 电源
    {"name": "24c02", "bus": 81, "loc": 0x50},
    {"name": "rg_fsp1200", "bus": 81, "loc": 0x58},
    {"name": "24c02", "bus": 82, "loc": 0x50},
    {"name": "rg_fsp1200", "bus": 82, "loc": 0x58},
    # 温度
    {"name": "rg_lm75", "bus": 76, "loc": 0x48},
    {"name": "rg_lm75", "bus": 76, "loc": 0x49},
    {"name": "rg_lm75", "bus": 79, "loc": 0x4b},
    {"name": "rg_tmp411", "bus": 79, "loc": 0x4c},
    {"name": "rg_tmp411", "bus": 80, "loc": 0x4c},
    {"name": "rg_lm75", "bus": 80, "loc": 0x4e},
    {"name": "rg_lm75", "bus": 80, "loc": 0x4f},
    # dcdc
    {"name": "rg_ucd90160", "bus": 64, "loc": 0x5b},
    {"name": "rg_ucd90160", "bus": 85, "loc": 0x5b},
    {"name": "rg_ina3221", "bus": 65, "loc": 0x43},
    {"name": "rg_tps53622", "bus": 65, "loc": 0x67},
    {"name": "rg_tps53622", "bus": 65, "loc": 0x6c},
    #avs
    {"name": "rg_xdpe132g5c", "bus": 83, "loc": 0x5b},
]

OPTOE = [
    {"name": "rg_optoe3", "startbus": 6, "endbus": 61},
]

REBOOT_CTRL_PARAM = {
    "cpu": {"io_addr": 0x920, "rst_val": 0xfe, "rst_delay": 0, "gettype": "io"},
    "mac": {"bus": 2, "loc": 0x1d, "offset": 0x20, "rst_val": 0xfd, "rst_delay": 0, "gettype": "i2c"},
    "phy": {"io_addr": 0x923, "rst_val": 0xef, "rst_delay": 1, "unlock_rst_val": 0xff, "unlock_rst_delay": 1, "gettype": "io"},
}

REBOOT_CAUSE_PARA = {
    "reboot_cause_list": [
        {
            "name": "cold_reboot",
            "monitor_point": {"gettype": "io", "io_addr": 0x988, "okval": 0},
            "record": [
                {"record_type": "file", "mode": "cover", "log": "Power Loss, ",
                    "path": "/etc/.reboot/.previous-reboot-cause.txt"},
                {"record_type": "file", "mode": "add", "log": "Power Loss, ", 
                    "path": "/etc/.reboot/.history-reboot-cause.txt"}
            ]
        },
        {
            "name": "wdt_reboot",
            "monitor_point": {"gettype": "io", "io_addr": 0x987, "okval": 0, "compare_mode":"great"},
            "record": [
                {"record_type": "file", "mode": "cover", "log": "Watchdog reboot, ",
                    "path": "/etc/.reboot/.previous-reboot-cause.txt"},
                {"record_type": "file", "mode": "add", "log": "Watchdog reboot, ",
                    "path": "/etc/.reboot/.history-reboot-cause.txt"}
            ],
            "finish_operation": [
                {"gettype": "io", "io_addr": 0x986, "value": 0x01},
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
    "i2cset -f -y 2 0x2d 0x4c 0xff",
    "i2cset -f -y 2 0x2d 0x4d 0xff",
    "i2cset -f -y 2 0x2d 0x35 0xff",
    "i2cset -f -y 2 0x2d 0x36 0xff",
    "i2cset -f -y 2 0x1d 0x39 0xff",
    "i2cset -f -y 2 0x1d 0x3a 0xff",
    "i2cset -f -y 2 0x1d 0x3b 0xff",
    "i2cset -f -y 2 0x3d 0x38 0xff",
    "i2cset -f -y 2 0x3d 0x39 0xff",
    "i2cset -f -y 2 0x3d 0x3a 0xff",
    "i2cset -f -y 2 0x3d 0x3b 0xff",
    # 光模块解复位
    "i2cset -f -y 2 0x1d 0x21 0xff",
    "i2cset -f -y 2 0x1d 0x22 0xff",
    "i2cset -f -y 2 0x2d 0x20 0xff",
    "i2cset -f -y 2 0x2d 0x21 0xff",
    "i2cset -f -y 2 0x3d 0x21 0xff",
    "i2cset -f -y 2 0x3d 0x22 0xff",
    "i2cset -f -y 2 0x3d 0x23 0xff",
    "i2cset -f -y 2 0x3d 0x24 0xff",
    # 使能码流点灯
    "i2cset -f -y 2 0x2d 0x3a 0xff",
    "i2cset -f -y 2 0x1d 0x3c 0xff"
]

WARM_UPGRADE_PARAM = {
    "slot0": {
        "VME": {
            "chain1": [
                {"name": "CPU_CPLD",
                    "refresh_file_judge_flag": 1,
                    "refresh_file": "/etc/.cpld_refresh/b6580_48cq8qc_refresh_cpu_cpld_header.vme",
                    "init_cmd": [
                        {"cmd": "echo 50 > /sys/class/gpio/export", "gettype": "cmd"},
                        {"cmd": "echo out > /sys/class/gpio/gpio50/direction", "gettype": "cmd", "delay": 0.1},
                        {"cmd": "echo 0 > /sys/class/gpio/gpio50/value", "gettype": "cmd"},
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
                        {"cmd": "echo 1 > /sys/class/gpio/gpio50/value", "gettype": "cmd"},
                        {"cmd": "echo 50 > /sys/class/gpio/unexport", "gettype": "cmd"},
                    ],
                 },

                {"name": "CONNECT_CPLD",
                    "refresh_file_judge_flag": 1,
                    "refresh_file": "/etc/.cpld_refresh/b6580_48cq8qc_refresh_cpu_base_header.vme",
                    "init_cmd": [
                        {"cmd": "echo 50 > /sys/class/gpio/export", "gettype": "cmd"},
                        {"cmd": "echo out > /sys/class/gpio/gpio50/direction", "gettype": "cmd", "delay": 0.1},
                        {"cmd": "echo 0 > /sys/class/gpio/gpio50/value", "gettype": "cmd"},
                        {"bus": 2, "loc": 0x1d, "offset": 0xce, "value": 0xff, "gettype": "i2c"},
                        {"io_addr": 0x9cc, "value": 0, "gettype": "io"},
                    ],
                    "rw_recover_reg": [
                        {"io_addr": 0x9aa, "value": None, "gettype": "io"},
                        {"io_addr": 0x955, "value": None, "gettype": "io"},
                        {"io_addr": 0x911, "value": None, "gettype": "io"},
                        {"io_addr": 0x920, "value": None, "gettype": "io"},
                        {"io_addr": 0x921, "value": None, "gettype": "io"},
                        {"io_addr": 0x922, "value": None, "gettype": "io"},
                        {"io_addr": 0x923, "value": None, "gettype": "io"},
                        {"io_addr": 0x924, "value": None, "gettype": "io"},
                        {"io_addr": 0x930, "value": None, "gettype": "io"},
                        {"io_addr": 0x932, "value": None, "gettype": "io"},
                        {"io_addr": 0x933, "value": None, "gettype": "io"},
                        {"io_addr": 0x934, "value": None, "gettype": "io"},
                        {"io_addr": 0x937, "value": None, "gettype": "io"},
                        {"io_addr": 0x938, "value": None, "gettype": "io"},
                        {"io_addr": 0x939, "value": None, "gettype": "io"},
                        {"io_addr": 0x93a, "value": None, "gettype": "io"},
                        {"io_addr": 0x941, "value": None, "gettype": "io"},
                        {"io_addr": 0x942, "value": None, "gettype": "io"},
                        {"io_addr": 0x947, "value": None, "gettype": "io"},
                        {"io_addr": 0x948, "value": None, "gettype": "io"},
                        {"io_addr": 0x949, "value": None, "gettype": "io"},
                        {"io_addr": 0x94d, "value": None, "gettype": "io"},
                        {"io_addr": 0x94e, "value": None, "gettype": "io"},
                        {"io_addr": 0x950, "value": None, "gettype": "io"},
                        {"io_addr": 0x9cd, "value": None, "gettype": "io"},
                        {"io_addr": 0x9ce, "value": None, "gettype": "io"},
                    ],
                    "save_set_reg": [
                        {"io_addr": 0x94f, "value": None, "set_value": 0, "save_value": None, "gettype": "io"},
                    ],
                    "after_upgrade_delay": 1,
                    "after_upgrade_delay_timeout": 30,
                    "refresh_finish_flag_check": {"io_addr": 0x9cb, "value": 0x5a, "gettype": "io"},
                    "access_check_reg": {"io_addr": 0x9aa, "value": 0x5a, "gettype": "io"},
                    "finish_cmd": [
                        {"bus": 2, "loc": 0x1d, "offset": 0xce, "value": 0, "gettype": "i2c"},
                        {"cmd": "echo 1 > /sys/class/gpio/gpio50/value", "gettype": "cmd"},
                        {"cmd": "echo 50 > /sys/class/gpio/unexport", "gettype": "cmd"},
                    ],
                 },

                {"name": "MACA_CPLD",
                    "refresh_file_judge_flag": 1,
                    "refresh_file": "/etc/.cpld_refresh/b6580_48cq8qc_refresh_mac_cplda_header.vme",
                    "init_cmd": [
                        {"file": WARM_UPG_FLAG, "gettype": "creat_file"},
                        {"cmd": "echo 50 > /sys/class/gpio/export", "gettype": "cmd"},
                        {"cmd": "echo out > /sys/class/gpio/gpio50/direction", "gettype": "cmd", "delay": 0.1},
                        {"cmd": "echo 0 > /sys/class/gpio/gpio50/value", "gettype": "cmd"},
                        {"io_addr": 0x9cd, "value": 0xff, "gettype": "io"},
                        {"bus": 2, "loc": 0x1d, "offset": 0xcc, "value": 0, "gettype": "i2c"},
                    ],
                    "rw_recover_reg": [
                        {"bus": 2, "loc": 0x1d, "offset": 0xaa, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x55, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x11, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x13, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x16, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x17, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x18, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x19, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x1a, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x1b, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x1e, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x1f, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x20, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x21, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x22, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x35, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x37, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x38, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x39, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x3a, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x3b, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x3c, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x49, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0x4d, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0xcd, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x1d, "offset": 0xce, "value": None, "gettype": "i2c"},
                    ],
                    "after_upgrade_delay": 1,
                    "after_upgrade_delay_timeout": 30,
                    "refresh_finish_flag_check": {"bus": 2, "loc": 0x1d, "offset": 0xcb, "value": 0x5a, "gettype": "i2c"},
                    "access_check_reg": {"bus": 2, "loc": 0x1d, "offset": 0xaa, "value": 0x5a, "gettype": "i2c"},
                    "finish_cmd": [
                        {"io_addr": 0x9cd, "value": 0, "gettype": "io"},
                        {"cmd": "echo 1 > /sys/class/gpio/gpio50/value", "gettype": "cmd"},
                        {"cmd": "echo 50 > /sys/class/gpio/unexport", "gettype": "cmd"},
                        {"file": WARM_UPG_FLAG, "gettype": "remove_file"},
                    ],
                 },

                {"name": "MACB_CPLD",
                    "refresh_file_judge_flag": 1,
                    "refresh_file": "/etc/.cpld_refresh/b6580_48cq8qc_refresh_mac_cpldb_header.vme",
                    "init_cmd": [
                        {"file": WARM_UPG_FLAG, "gettype": "creat_file"},
                        {"cmd": "echo 50 > /sys/class/gpio/export", "gettype": "cmd"},
                        {"cmd": "echo out > /sys/class/gpio/gpio50/direction", "gettype": "cmd", "delay": 0.1},
                        {"cmd": "echo 0 > /sys/class/gpio/gpio50/value", "gettype": "cmd"},
                        {"io_addr": 0x9ce, "value": 0xff, "gettype": "io"},
                        {"bus": 2, "loc": 0x2d, "offset": 0xcc, "value": 0, "gettype": "i2c"},
                    ],
                    "rw_recover_reg": [
                        {"bus": 2, "loc": 0x2d, "offset": 0xaa, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x55, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x11, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x15, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x16, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x17, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x18, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x19, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x1a, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x1b, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x1c, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x1d, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x20, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x21, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x33, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x34, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x35, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x36, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x3a, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x47, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x48, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x49, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x4a, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x4b, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x4c, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x4d, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x2d, "offset": 0x51, "value": None, "gettype": "i2c"},
                    ],
                    "after_upgrade_delay": 1,
                    "after_upgrade_delay_timeout": 30,
                    "refresh_finish_flag_check": {"bus": 2, "loc": 0x1d, "offset": 0xcb, "value": 0x5a, "gettype": "i2c"},
                    "access_check_reg": {"bus": 2, "loc": 0x2d, "offset": 0xaa, "value": 0x5a, "gettype": "i2c"},
                    "finish_cmd": [
                        {"io_addr": 0x9ce, "value": 0, "gettype": "io"},
                        {"cmd": "echo 1 > /sys/class/gpio/gpio50/value", "gettype": "cmd"},
                        {"cmd": "echo 50 > /sys/class/gpio/unexport", "gettype": "cmd"},
                        {"file": WARM_UPG_FLAG, "gettype": "remove_file"},
                        {"cmd": "ipmitool raw 0x32 0x03 0x01", "gettype": "cmd", "ignore_result": 1},
                    ],
                 },

                {"name": "MACC_CPLD",
                    "refresh_file_judge_flag": 1,
                    "refresh_file": "/etc/.cpld_refresh/b6580_48cq8qc_refresh_mac_cpldc_header.vme",
                    "init_cmd": [
                        {"file": WARM_UPG_FLAG, "gettype": "creat_file"},
                        {"cmd": "echo 50 > /sys/class/gpio/export", "gettype": "cmd"},
                        {"cmd": "echo out > /sys/class/gpio/gpio50/direction", "gettype": "cmd", "delay": 0.1},
                        {"cmd": "echo 0 > /sys/class/gpio/gpio50/value", "gettype": "cmd"},
                        {"bus": 2, "loc": 0x1d, "offset": 0xcd, "value": 0xff, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0xcc, "value": 0, "gettype": "i2c"},
                    ],
                    "rw_recover_reg": [
                        {"bus": 2, "loc": 0x3d, "offset": 0xaa, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x55, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x11, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x15, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x16, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x17, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x18, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x19, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x1a, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x1b, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x1c, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x1d, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x21, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x22, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x23, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x24, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x33, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x34, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x35, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x36, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x38, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x39, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x3a, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x3b, "value": None, "gettype": "i2c"},
                        {"bus": 2, "loc": 0x3d, "offset": 0x3c, "value": None, "gettype": "i2c"},
                    ],
                    "after_upgrade_delay": 1,
                    "after_upgrade_delay_timeout": 30,
                    "refresh_finish_flag_check": {"bus": 2, "loc": 0x3d, "offset": 0xcb, "value": 0x5a, "gettype": "i2c"},
                    "access_check_reg": {"bus": 2, "loc": 0x3d, "offset": 0xaa, "value": 0x5a, "gettype": "i2c"},
                    "finish_cmd": [
                        {"bus": 2, "loc": 0x1d, "offset": 0xcd, "value": 0, "gettype": "i2c"},
                        {"cmd": "echo 1 > /sys/class/gpio/gpio50/value", "gettype": "cmd"},
                        {"cmd": "echo 50 > /sys/class/gpio/unexport", "gettype": "cmd"},
                        {"file": WARM_UPG_FLAG, "gettype": "remove_file"},
                    ],
                 },

                {"name": "FAN_CPLD",
                    "refresh_file_judge_flag": 1,
                    "refresh_file": "/etc/.cpld_refresh/b6580_48cq8qc_refresh_fan_header.vme",
                    "init_cmd": [
                        {"cmd": "echo 50 > /sys/class/gpio/export", "gettype": "cmd"},
                        {"cmd": "echo out > /sys/class/gpio/gpio50/direction", "gettype": "cmd", "delay": 0.1},
                        {"cmd": "echo 0 > /sys/class/gpio/gpio50/value", "gettype": "cmd"},
                    ],
                    "finish_cmd": [
                        {"cmd": "echo 1 > /sys/class/gpio/gpio50/value", "gettype": "cmd"},
                        {"cmd": "echo 50 > /sys/class/gpio/unexport", "gettype": "cmd"},
                    ],
                    "rw_recover_reg": [],
                    "after_upgrade_delay": 1,
                    "after_upgrade_delay_timeout": 30,
                    "access_check_reg": {"bus": 4, "loc": 0x3d, "offset": 0xaa, "value": 0x5a, "gettype": "i2c"},
                 },
            ],
        },

        "SPI-LOGIC-DEV": {
            "chain1": [
                {"name": "FPGA",
                    "init_cmd": [
                        {"file": WARM_UPG_FLAG, "gettype": "creat_file"},
                        {"io_addr": 0xb4d, "value": 0xfe, "gettype": "io"},
                    ],
                    "after_upgrade_delay": 10,
                    "after_upgrade_delay_timeout": 180,
                    "refresh_finish_flag_check": {"io_addr": 0xb4d, "value": 0xff, "gettype": "io"},
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
    "devtype": 0x40ca,

    "slot0": {
        "subtype": 0,
        "VME": {
            "chain1": {
                "name": "CPLD",
                "is_support_warm_upg": 1,
                 "init_cmd": [
                    {"cmd": "echo 50 > /sys/class/gpio/export", "gettype": "cmd"},
                    {"cmd": "echo out > /sys/class/gpio/gpio50/direction", "gettype": "cmd", "delay": 0.1},
                    {"cmd": "echo 0 > /sys/class/gpio/gpio50/value", "gettype": "cmd"},
                ],
                "finish_cmd": [
                    {"cmd": "echo 1 > /sys/class/gpio/gpio50/value", "gettype": "cmd"},
                    {"cmd": "echo 50 > /sys/class/gpio/unexport", "gettype": "cmd", "delay": 0.1},
                ],
            },
        },

        "SPI-LOGIC-DEV": {
            "chain1": {
                "name": "FPGA",
                "is_support_warm_upg": 1,
            },
        },

        "SYSFS": {
            "chain2": {
                "name": "BCM5387",
                "is_support_warm_upg": 0,
                "init_cmd": [
                    {"cmd": "modprobe rg_spi_gpio", "gettype": "cmd"},
                    {"cmd": "modprobe rg_spi_93xx46 spi_bus_num=0 spi_cs_gpio=6", "gettype": "cmd", "delay": 0.1},
                ],
                "finish_cmd": [
                    {"cmd": "rmmod rg_spi_93xx46 spi_bus_num=0 spi_cs_gpio=6", "gettype": "cmd"},
                    {"cmd": "rmmod rg_spi_gpio", "gettype": "cmd", "delay": 0.1},
                ],
            },
        },

        "MTD": {
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
                {"chain": 1, "file": "/etc/.upgrade_test/b6580-48_fpga_test_0_1_header.bin", "display_name": "FPGA"},
            ],
            "cpld": [
                {"chain": 1, "file": "/etc/.upgrade_test/b6580-48_cpld_test_0_1_header.vme", "display_name": "CPLD"},
            ],
        },
    },
}

PLATFORM_E2_CONF = {
    "fan": [
        {"name": "fan1", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/75-0050/eeprom"},
        {"name": "fan2", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/74-0050/eeprom"},
        {"name": "fan3", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/73-0050/eeprom"},
        {"name": "fan4", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/72-0050/eeprom"},
        {"name": "fan5", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/71-0050/eeprom"},
        {"name": "fan6", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/70-0050/eeprom"},
    ],
    "psu": [
        {"name": "psu1", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/81-0050/eeprom"},
        {"name": "psu2", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/82-0050/eeprom"},
    ],
    "syseeprom": [
        {"name": "syseeprom", "e2_type": "onie_tlv", "e2_path": "/sys/bus/i2c/devices/1-0056/eeprom"},
    ],
}

