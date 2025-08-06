#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  ruijiecommon import *

#启机模块
STARTMODULE  =  {
                "xdpe_avscontrol": 1,
                "dev_monitor": 1,
                "hal_fanctrl":1,
                "hal_ledctrl":1,
                "intelligent_monitor":1,
                "sff_temp_polling":1,
                "rg_pmon_syslog":1,
                "reboot_cause":1,
                "plugins_init":0,
                "product_name": 1,
            }

## 驱动列表
##
BLACKLIST_DRIVERS = [
    {"name": "i2c_i801", "delay": 0},
    {"name": "i2c_ismt", "delay": 0},
]

DRIVERLISTS = [
        {"name": "rg_i2c_i801", "delay": 0},
        {"name": "i2c_dev", "delay": 0},
        {"name": "i2c_gpio", "delay":0},
        {"name": "i2c_mux", "delay":0},
        {"name": "rg_i2c_mux_pca9641", "delay": 0},
        {"name": "rg_i2c_mux_pca954x", "delay": 0},
        {"name": "rg_fpga_pcie", "delay": 0},
        {"name": "rg_pcie_dev", "delay": 0},
        {"name": "rg_io_dev", "delay": 0},
        {"name": "rg_i2c_dev", "delay": 0},
        {"name": "rg_fpga_i2c_bus_drv", "delay": 0},
        {"name": "rg_fpga_pca954x_drv", "delay": 0},
        {"name": "mdio_bitbang", "delay": 0},
        {"name": "rg_mdio_gpio", "delay": 0},
        {"name": "ipmi_si", "delay": 0},
        {"name": "rg_wdt", "delay": 0},
        {"name": "intel_spi writeable=on", "delay": 0},
        {"name": "intel_spi_pci", "delay": 0},

        {"name": "rg_i2c_gpio_d1700_device", "delay":0},
        {"name": "rg_pcie_dev_device", "delay": 0},
        {"name": "rg_io_dev_device", "delay": 0},
        {"name": "rg_fpga_i2c_bus_device", "delay": 0},
        {"name": "rg_fpga_pca954x_device", "delay": 0},
        {"name": "rg_i2c_dev_device", "delay": 0},
        {"name": "rg_wdt_device", "delay": 0},
        {"name": "rg_mdio_gpio_device", "delay": 0},
        {"name": "rg_i2c_mux_pca954x_device", "delay": 0},
        {"name": "rg_spi_gpio_d1700_device mosi=54 miso=52", "delay":0},

        {"name": "ruijie_common dfd_my_type_i2c_bus=1 dfd_my_type_i2c_addr=0x56", "delay": 1},

        {"name": "rg_eeprom_93xx46", "delay": 0},
        {"name": "rg_lm75", "delay":0},
        {"name": "rg_tmp401", "delay":0},
        {"name": "rg_optoe", "delay": 0},
        {"name": "at24", "delay": 0},
        {"name": "rg_mac_bsc", "delay": 0},
        {"name": "rg_pmbus_core", "delay":0},
        {"name": "rg_csu550", "delay": 0},
        {"name": "rg_ina3221", "delay": 0},
        {"name": "rg_tps53622", "delay": 0},
        {"name": "rg_ucd9000", "delay": 0},
        {"name": "rg_xdpe132g5c_pmbus", "delay": 0},
        {"name": "ice", "delay": 0},
        {"name": "rg_ssd_power", "delay": 0},
        {"name": "rg_ssd_power_device", "delay": 0},

        {"name": "firmware_driver_cpld", "delay": 0},
        {"name": "firmware_driver_ispvme", "delay": 0},
        {"name": "firmware_driver_sysfs", "delay": 0},
        {"name": "rg_firmware_upgrade_device", "delay": 0},

        {"name": "hw_test", "delay":0},
        {"name": "rg_plat_dfd", "delay":0},
        {"name": "rg_plat_switch", "delay":0},
        {"name": "rg_plat_fan", "delay":0},
        {"name": "rg_plat_psu", "delay":0},
        {"name": "rg_plat_sff", "delay":0},
        {"name": "rg_plat_sensor", "delay": 0},

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
        {"name": "curr_sensor_device_driver", "delay": 0},
]

DEVICE = [
        # GPIO-I2C
        {"name": "24c02", "bus":1, "loc":0x56 },
        # UP port board
        {"name": "rg_ucd90160", "bus": 64, "loc": 0x5b},
        {"name": "rg_lm75", "bus": 65, "loc": 0x4b},
        # MAC board
        {"name": "rg_ucd90160", "bus": 79, "loc": 0x5b},
        {"name": "rg_ucd90160", "bus": 80, "loc": 0x5b},
        # PSU
        {"name": "24c02", "bus":95, "loc":0x50},
        {"name": "rg_fsp1200","bus":95, "loc":0x58 },
        {"name": "24c02", "bus":96, "loc": 0x50},
        {"name": "rg_fsp1200","bus":96, "loc":0x58 },
        {"name": "24c02", "bus":97, "loc":0x50},
        {"name": "rg_fsp1200","bus":97, "loc":0x58 },
        {"name": "24c02", "bus":98, "loc": 0x50},
        {"name": "rg_fsp1200","bus":98, "loc":0x58 },
        # FAN
        {"name": "24c64","bus":106,"loc":0x50 },
        {"name": "24c64","bus":107,"loc":0x50 },
        {"name": "24c64","bus":108,"loc":0x50 },
        {"name": "24c64","bus":105,"loc":0x50 },
        {"name": "24c64","bus":114,"loc":0x50 },
        {"name": "24c64","bus":115,"loc":0x50 },
        {"name": "24c64","bus":116,"loc":0x50 },
        {"name": "24c64","bus":113,"loc":0x50 },
        # fan temp
        {"name": "rg_lm75", "bus": 104, "loc": 0x4b},
        {"name": "rg_lm75", "bus": 112, "loc": 0x4b},
        # base temp
        {"name": "rg_lm75", "bus": 123, "loc": 0x4b},
        {"name": "rg_lm75", "bus": 124, "loc": 0x4b},
        {"name": "rg_lm75", "bus": 71, "loc": 0x4b},
        {"name": "rg_lm75", "bus": 72, "loc": 0x4f},
        # should be ct7318
        #{"name": "rg_tmp411", "bus": 73, "loc": 0x4c},
        #{"name": "rg_tmp411", "bus": 74, "loc": 0x4c},
        # base dcdc
        {"name": "rg_ucd90160", "bus": 121, "loc": 0x5b},
        {"name": "rg_ucd90160", "bus": 122, "loc": 0x5f},
        # DOWN port board
        {"name": "rg_ucd90160", "bus": 129, "loc": 0x5b},
        {"name": "rg_lm75", "bus": 130, "loc": 0x4b},
        # xdpe avs
        {"name": "rg_xdpe12284", "bus": 66, "loc": 0x70},
        {"name": "rg_xdpe132g5c_pmbus", "bus": 81, "loc": 0x40},
        {"name": "rg_xdpe132g5c_pmbus", "bus": 82, "loc": 0x4d},
        {"name": "rg_xdpe132g5c_pmbus", "bus": 83, "loc": 0x4d},
        {"name": "rg_xdpe12284", "bus": 84, "loc": 0x70},
        {"name": "rg_xdpe12284", "bus": 85, "loc": 0x70},
        {"name": "rg_xdpe12284", "bus": 131, "loc": 0x70},
        {"name": "rg_xdpe12284", "bus": 122, "loc": 0x70},
        {"name": "rg_xdpe12284", "bus": 122, "loc": 0x6e},
        {"name": "rg_xdpe12284", "bus": 122, "loc": 0x5e},
        {"name": "rg_xdpe12284", "bus": 122, "loc": 0x68},
]

OPTOE = [
        {"name": "rg_optoe3", "startbus": 140, "endbus": 267},
]

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
                            "path": "/dev/cpld6",
                            "offset": 0x64,
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
                    "id": "psu1pmbus",
                    "stop_monitor_condition": [
                        {
                            "name": "23-0058 file check",
                            "judge_file": "/sys/bus/i2c/devices/95-0058/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "95-0058 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/95-0058/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "95-0058 delete_device",
                            "cmd": "echo 0x58 > /sys/bus/i2c/devices/i2c-95/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "95-0058 new_device",
                            "cmd": "echo rg_fsp1200 0x58 > /sys/bus/i2c/devices/i2c-95/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "psu1frue2",
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
                            "cmd": "echo 24c02 0x50 > /sys/bus/i2c/devices/i2c-95/new_device",
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
                            "path": "/dev/cpld6",
                            "offset": 0x64,
                            "read_len": 1
                        },
                        "rd_bit": 6,
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
                            "name": "96-0058 file check",
                            "judge_file": "/sys/bus/i2c/devices/96-0058/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "96-0058 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/96-0058/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "96-0058 delete_device",
                            "cmd": "echo 0x58 > /sys/bus/i2c/devices/i2c-96/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "96-0058 new_device",
                            "cmd": "echo rg_fsp1200 0x58 > /sys/bus/i2c/devices/i2c-96/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "psu2frue2",
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
                            "cmd": "echo 24c02 0x50 > /sys/bus/i2c/devices/i2c-96/new_device",
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
                            "path": "/dev/cpld6",
                            "offset": 0x65,
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
                    "id": "psu3pmbus",
                    "stop_monitor_condition": [
                        {
                            "name": "97-0058 file check",
                            "judge_file": "/sys/bus/i2c/devices/97-0058/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "97-0058 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/97-0058/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "97-0058 delete_device",
                            "cmd": "echo 0x58 > /sys/bus/i2c/devices/i2c-97/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "97-0058 new_device",
                            "cmd": "echo rg_fsp1200 0x58 > /sys/bus/i2c/devices/i2c-97/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "psu3frue2",
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
                            "cmd": "echo 24c02 0x50 > /sys/bus/i2c/devices/i2c-97/new_device",
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
                            "path": "/dev/cpld6",
                            "offset": 0x65,
                            "read_len": 1
                        },
                        "rd_bit": 6,
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
                            "name": "98-0058 file check",
                            "judge_file": "/sys/bus/i2c/devices/98-0058/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "98-0058 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/98-0058/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "98-0058 delete_device",
                            "cmd": "echo 0x58 > /sys/bus/i2c/devices/i2c-98/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "98-0058 new_device",
                            "cmd": "echo rg_fsp1200 0x58 > /sys/bus/i2c/devices/i2c-98/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "psu4frue2",
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
                            "cmd": "echo 24c02 0x50 > /sys/bus/i2c/devices/i2c-98/new_device",
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
                            "path": "/dev/cpld3",
                            "offset": 0x5b,
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
            "name": "fan2",
            "monitor_point": [
                [
                    {
                        "name": "fan2 present check",
                        "rd_config": {
                            "gettype": "devfile",
                            "path": "/dev/cpld7",
                            "offset": 0x5b,
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
                            "name": "113-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/113-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "113-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/113-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "113-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-113/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "113-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-113/new_device",
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
                            "path": "/dev/cpld3",
                            "offset": 0x5b,
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
            "name": "fan4",
            "monitor_point": [
                [
                    {
                        "name": "fan4 present check",
                        "rd_config": {
                            "gettype": "devfile",
                            "path": "/dev/cpld7",
                            "offset": 0x5b,
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
                            "name": "114-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/114-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "114-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/114-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "114-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-114/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "114-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-114/new_device",
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
                            "path": "/dev/cpld3",
                            "offset": 0x5b,
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
            "name": "fan6",
            "monitor_point": [
                [
                    {
                        "name": "fan6 present check",
                        "rd_config": {
                            "gettype": "devfile",
                            "path": "/dev/cpld7",
                            "offset": 0x5b,
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
                            "name": "115-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/115-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "115-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/115-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "115-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-115/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "115-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-115/new_device",
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
                            "path": "/dev/cpld3",
                            "offset": 0x5b,
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
                            "name": "108-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/108-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "108-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/108-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "108-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-108/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "108-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-108/new_device",
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
                            "path": "/dev/cpld7",
                            "offset": 0x5b,
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
                            "name": "116-0050 file check",
                            "judge_file": "/sys/bus/i2c/devices/116-0050/eeprom",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "116-0050 file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/116-0050/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "116-0050 delete_device",
                            "cmd": "echo 0x50 > /sys/bus/i2c/devices/i2c-116/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "116-0050 new_device",
                            "cmd": "echo 24c64 0x50 > /sys/bus/i2c/devices/i2c-116/new_device",
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
                            "name": "65-004b file check",
                            "judge_file": "/sys/bus/i2c/devices/65-004b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "65-004b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/65-004b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "65-004b delete_device",
                            "cmd": "echo 0x4b > /sys/bus/i2c/devices/i2c-65/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "65-004b new_device",
                            "cmd": "echo rg_lm75 0x4b > /sys/bus/i2c/devices/i2c-65/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_2",
                    "stop_monitor_condition": [
                        {
                            "name": "104-004b file check",
                            "judge_file": "/sys/bus/i2c/devices/104-004b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "104-004b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/104-004b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "104-004b delete_device",
                            "cmd": "echo 0x4b > /sys/bus/i2c/devices/i2c-104/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "104-004b new_device",
                            "cmd": "echo rg_lm75 0x4b > /sys/bus/i2c/devices/i2c-104/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_3",
                    "stop_monitor_condition": [
                        {
                            "name": "112-004b file check",
                            "judge_file": "/sys/bus/i2c/devices/112-004b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "112-004b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/112-004b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "112-004b delete_device",
                            "cmd": "echo 0x4b > /sys/bus/i2c/devices/i2c-112/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "112-004b new_device",
                            "cmd": "echo rg_lm75 0x4b > /sys/bus/i2c/devices/i2c-112/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_4",
                    "stop_monitor_condition": [
                        {
                            "name": "123-004b file check",
                            "judge_file": "/sys/bus/i2c/devices/123-004b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "123-004b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/123-004b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "123-004b delete_device",
                            "cmd": "echo 0x4b > /sys/bus/i2c/devices/i2c-123/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "123-004b new_device",
                            "cmd": "echo rg_lm75 0x4b > /sys/bus/i2c/devices/i2c-123/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_5",
                    "stop_monitor_condition": [
                        {
                            "name": "124-004b file check",
                            "judge_file": "/sys/bus/i2c/devices/124-004b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "124-004b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/124-004b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "124-004b delete_device",
                            "cmd": "echo 0x4b > /sys/bus/i2c/devices/i2c-124/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "124-004b new_device",
                            "cmd": "echo rg_lm75 0x4b > /sys/bus/i2c/devices/i2c-124/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_6",
                    "stop_monitor_condition": [
                        {
                            "name": "71-004b file check",
                            "judge_file": "/sys/bus/i2c/devices/71-004b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "71-004b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/71-004b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "71-004b delete_device",
                            "cmd": "echo 0x4b > /sys/bus/i2c/devices/i2c-71/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "71-004b new_device",
                            "cmd": "echo rg_lm75 0x4b > /sys/bus/i2c/devices/i2c-71/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_7",
                    "stop_monitor_condition": [
                        {
                            "name": "72-004f file check",
                            "judge_file": "/sys/bus/i2c/devices/72-004f/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "72-004f file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/72-004f/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "72-004f delete_device",
                            "cmd": "echo 0x4f > /sys/bus/i2c/devices/i2c-72/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "72-004f new_device",
                            "cmd": "echo rg_lm75 0x4f > /sys/bus/i2c/devices/i2c-72/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "lm75_8",
                    "stop_monitor_condition": [
                        {
                            "name": "130-004b file check",
                            "judge_file": "/sys/bus/i2c/devices/130-004b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "130-004b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/130-004b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "130-004b delete_device",
                            "cmd": "echo 0x4b > /sys/bus/i2c/devices/i2c-130/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "130-004b new_device",
                            "cmd": "echo rg_lm75 0x4b > /sys/bus/i2c/devices/i2c-130/new_device",
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
                            "name": "79-005b file check",
                            "judge_file": "/sys/bus/i2c/devices/79-005b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "79-005b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/79-005b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "79-005b delete_device",
                            "cmd": "echo 0x5b > /sys/bus/i2c/devices/i2c-79/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "79-005b new_device",
                            "cmd": "echo rg_ucd90160 0x5b > /sys/bus/i2c/devices/i2c-79/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "ucd90160_3",
                    "stop_monitor_condition": [
                        {
                            "name": "80-005b file check",
                            "judge_file": "/sys/bus/i2c/devices/80-005b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "80-005b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/80-005b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "80-005b delete_device",
                            "cmd": "echo 0x5b > /sys/bus/i2c/devices/i2c-80/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "80-005b new_device",
                            "cmd": "echo rg_ucd90160 0x5b > /sys/bus/i2c/devices/i2c-80/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "ucd90160_4",
                    "stop_monitor_condition": [
                        {
                            "name": "121-005b file check",
                            "judge_file": "/sys/bus/i2c/devices/121-005b/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "121-005b file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/121-005b/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "121-005b delete_device",
                            "cmd": "echo 0x5b > /sys/bus/i2c/devices/i2c-121/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "121-005b new_device",
                            "cmd": "echo rg_ucd90160 0x5b > /sys/bus/i2c/devices/i2c-121/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "ucd90160_5",
                    "stop_monitor_condition": [
                        {
                            "name": "122-005f file check",
                            "judge_file": "/sys/bus/i2c/devices/122-005f/hwmon",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action_check": [
                        {
                            "name": "122-005f file pre_action_check",
                            "judge_file": "/sys/bus/i2c/devices/122-005f/",
                            "okval": 1,
                            "gettype": "file_check"
                        }
                    ],
                    "pre_action": [
                        {
                            "name": "122-005f delete_device",
                            "cmd": "echo 0x5f > /sys/bus/i2c/devices/i2c-122/delete_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ],
                    "action": [
                        {
                            "name": "122-005f new_device",
                            "cmd": "echo rg_ucd90160 0x5f > /sys/bus/i2c/devices/i2c-122/new_device",
                            "gettype": "cmd",
                            "delay": 0.1
                        }
                    ]
                },
                {
                    "id": "ucd90160_5",
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
            ]
        },
    ]
}

#####################MAC调压参数####################################
MAC_AVS_PARAM = {
    0x92: 0xBF4,
    0x90: 0xC29,
    0x8e: 0xC56,
    0x8c: 0xC8B,
    0x8a: 0xCBD,
    0x88: 0xCEA,
    0x86: 0xD14,
    0x84: 0xD44,
    0x82: 0xD71
}

AVS_VOUT_MODE_PARAM ={
    0x18:256,        # 2^8
    0x17:512,        # 2^9
    0x16:1024,       # 2^10
    0x15:2048,       # 2^11
    0x14:4096,       # 2^12
}
MAC_DEFAULT_PARAM = {
  "type": 0,                       # type 1表示 不在范围内用默认 / 0表示不在范围内不调
  "default":0x82,                  # 配合type使用
  "bus":81,                        # AVSI2C总线地址
  "devno":0x40,                    # AVS地址
  "loopaddr":0xff,                 # AVS loop地址
  "loop":0x06,                     # AVS loop值
  "vout_cmd_addr":0x42,            # AVS调压地址
  "vout_mode_addr":0x40,           # AVS调压地址
  "sdktype": 0,                    # type 0表示 不需要移位 / 1 表示需要移位
  "macregloc":24 ,                 # 移位操作
  "mask": 0xff,                    # 移位后掩码
  "rov_source":0,                  # rov_source 0表示从cpld获取rov值 / 1表示从sdk获取rov值
  "cpld_avs":{"path": "/dev/cpld4", "offset": 0x30, "read_len": 1, "gettype":"devfile"},
  "set_avs": {"loc": "/sys/bus/i2c/devices/81-0040/avs0_vout_command", "gettype": "sysfs",  "formula": "hex(%d)"},
}
#####################MAC调压参数####################################

# 拉起进程的前置操作
INIT_PARAM_PRE = [
]

INIT_COMMAND = [
    # 开启X86监控BMC串口
    "dfd_debug sysfs_data_wr /dev/cpld1 0x41 0x01",
    # 光模块上电
    "dfd_debug sysfs_data_wr /dev/cpld2 0x32 0x0f",
    "dfd_debug sysfs_data_wr /dev/cpld6 0x36 0x0f",
    "dfd_debug sysfs_data_wr /dev/cpld8 0x32 0x0f",
    # 使能码流点灯
    "dfd_debug sysfs_data_wr /dev/cpld2 0xef 0x01",
    "dfd_debug sysfs_data_wr /dev/cpld4 0xef 0x01",
    "dfd_debug sysfs_data_wr /dev/cpld5 0xef 0x01",
    "dfd_debug sysfs_data_wr /dev/cpld8 0xef 0x01",
]

REBOOT_CTRL_PARAM = {
    "cpu": {"path":"/dev/cpld1", "offset":0x17, "rst_val":0xfd, "rst_delay":0, "gettype":"devfile"},
    "phy": {"path":"/dev/cpld1", "offset":0x18, "rst_val":0xe, "rst_delay":0, "gettype":"devfile"},
    "power": {"path":"/dev/cpld6", "offset":0x32, "rst_val":0x1, "rst_delay":0, "gettype":"devfile"},
    "mac": [
                {"gettype": "cmd", "cmd": "setpci -s 14:02.0 0x50.W=0x0050", "rst_delay":0.1},
                {"path":"/dev/cpld4", "offset":0x16, "rst_val":0x0, "rst_delay":1, "gettype":"devfile"},
                {"gettype": "cmd", "cmd": "setpci -s 14:02.0 0x50.W=0x0060", "rst_delay":0.1},
            ],
}

REBOOT_CAUSE_PARA = {
    "reboot_cause_list": [
        {
            "name": "cold_reboot",
            "monitor_point": {"gettype":"devfile", "path":"/dev/cpld1", "offset":0x1d, "read_len":1, "okval":0x09},
            "record": [
                {"record_type":"file", "mode":"cover", "log":"Power Loss, ", "path":"/etc/.reboot/.previous-reboot-cause.txt"},
                {"record_type": "file", "mode": "add", "log": "Power Loss, ", "path": "/etc/.reboot/.history-reboot-cause.txt"}
            ]
        },
        {
            "name": "watchdog_reboot",
            "monitor_point": {"gettype":"devfile", "path":"/dev/cpld1", "offset":0x1d, "read_len":1, "okval":0x05},
            "record": [
                {"record_type":"file", "mode":"cover", "log":"Watchdog reboot, ", "path":"/etc/.reboot/.previous-reboot-cause.txt"},
                {"record_type": "file", "mode": "add", "log": "Watchdog reboot, ", "path": "/etc/.reboot/.history-reboot-cause.txt"}
            ],
        },
        {
            "name": "bmc_reboot",
            "monitor_point": {"gettype":"devfile", "path":"/dev/cpld1", "offset":0x1d, "read_len":1, "okval":0x06},
            "record": [
                {"record_type":"file", "mode":"cover", "log":"BMC reboot, ", "path":"/etc/.reboot/.previous-reboot-cause.txt"},
                {"record_type": "file", "mode": "add", "log": "BMC reboot, ", "path": "/etc/.reboot/.history-reboot-cause.txt"}
            ],
        },
        {
            "name": "bmc_powerdown",
            "monitor_point": {"gettype":"devfile", "path":"/dev/cpld1", "offset":0x1d, "read_len":1, "okval":0x01},
            "record": [
                {"record_type":"file", "mode":"cover", "log":"BMC powerdown, ", "path":"/etc/.reboot/.previous-reboot-cause.txt"},
                {"record_type": "file", "mode": "add", "log": "BMC powerdown, ", "path": "/etc/.reboot/.history-reboot-cause.txt"}
            ],
        },
        {
            "name": "cpu_reboot",
            "monitor_point": {"gettype":"devfile", "path":"/dev/cpld1", "offset":0x1d, "read_len":1, "okval":[0x03, 0x04]},
            "record": [
                {"record_type":"file", "mode":"cover", "log":"CPU reboot, ", "path":"/etc/.reboot/.previous-reboot-cause.txt"},
                {"record_type": "file", "mode": "add", "log": "CPU reboot, ", "path": "/etc/.reboot/.history-reboot-cause.txt"}
            ],
        },
        {
            "name": "cpu_powerdown",
            "monitor_point": {"gettype":"devfile", "path":"/dev/cpld1", "offset":0x1d, "read_len":1, "okval":[0x02, 0x07, 0x0a]},
            "record": [
                {"record_type":"file", "mode":"cover", "log":"CPU powerdown, ", "path":"/etc/.reboot/.previous-reboot-cause.txt"},
                {"record_type": "file", "mode": "add", "log": "CPU powerdown, ", "path": "/etc/.reboot/.history-reboot-cause.txt"}
            ],
        },
        {
            "name": "otp_reboot",
            "monitor_point": {"gettype": "file_exist", "judge_file": "/etc/.otp_reboot_flag", "okval":True},
            "record": [
                {"record_type":"file", "mode":"cover", "log":"Thermal Overload: ASIC, ", "path":"/etc/.reboot/.previous-reboot-cause.txt"},
                {"record_type": "file", "mode": "add", "log": "Thermal Overload: ASIC, ", "path": "/etc/.reboot/.history-reboot-cause.txt"}
            ],
            "finish_operation": [
                {"gettype": "cmd", "cmd": "rm -rf /etc/.otp_reboot_flag"},
            ]
        },
    ],
    "other_reboot_cause_record": [
        {
            "record_type": "file",
            "mode": "cover",
            "log": "User issued 'reboot' command or other reasons, ",
            "path": "/etc/.reboot/.previous-reboot-cause.txt"
        },
        {
            "record_type": "file",
            "mode": "add",
            "log": "User issued 'reboot' command or other reasons, ",
            "path": "/etc/.reboot/.history-reboot-cause.txt",
            "file_max_size":1*1024*1024
        }
    ]
}

PLATFORM_E2_CONF = {
    "fan": [
        {"name": "fan1", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/105-0050/eeprom"},
        {"name": "fan2", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/113-0050/eeprom"},
        {"name": "fan3", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/106-0050/eeprom"},
        {"name": "fan4", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/114-0050/eeprom"},
        {"name": "fan5", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/107-0050/eeprom"},
        {"name": "fan6", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/115-0050/eeprom"},
        {"name": "fan7", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/108-0050/eeprom"},
        {"name": "fan8", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/116-0050/eeprom"},
    ],
    "psu": [
        {"name": "psu1", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/95-0050/eeprom"},
        {"name": "psu2", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/96-0050/eeprom"},
        {"name": "psu3", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/97-0050/eeprom"},
        {"name": "psu4", "e2_type": "fru", "e2_path": "/sys/bus/i2c/devices/98-0050/eeprom"},
    ],
    "syseeprom": [
        {"name": "syseeprom", "e2_type": "onie_tlv", "e2_path": "/sys/bus/i2c/devices/1-0056/eeprom"},
    ],
}

UPGRADE_SUMMARY = {
    "devtype":0x409f,

    "slot0":{
        "subtype":0,
        "VME":{
            "chain1":{
                "name":"BASE_CPLD",
                "is_support_warm_upg":1,
            },
            "chain2":{
                "name":"MAC_CPLD_A/B",
                "is_support_warm_upg":1,
            },
            "chain3":{
                "name":"MAC_CPLD_C",
                "is_support_warm_upg":1,
            },
            "chain4":{
                "name":"UPORT_CPLD",
                "is_support_warm_upg":1,
            },
            "chain5":{
                "name":"DPORT_CPLD",
                "is_support_warm_upg":1,
            },
            "chain6":{
                "name":"UFCB_CPLD",
                "is_support_warm_upg":1,
            },
            "chain7":{
                "name":"DFCB_CPLD",
                "is_support_warm_upg":1,
            },
            "chain8":{
                "name":"CPU_CPLD",
                "is_support_warm_upg":1,
            },
        },

        "SPI-LOGIC-DEV":{
            "chain1":{
                "name":"UPORT_FPGA",
                "is_support_warm_upg":1,
            },
            "chain2":{
                "name":"MAC_FPGA",
                "is_support_warm_upg":1,
            },
            "chain3":{
                "name":"DPORT_FPGA",
                "is_support_warm_upg":1,
            },
        },

        "SYSFS":{
            "chain4":{
                "name":"BCM5387",
                "is_support_warm_upg":0,
                "init_cmd":[
                    {"cmd":"modprobe rg_spi_gpio", "gettype":"cmd"},
                    {"cmd":"modprobe rg_spi_93xx46", "gettype":"cmd", "delay":0.1},
                ],
                "finish_cmd":[
                    {"cmd":"rmmod rg_spi_93xx46", "gettype":"cmd"},
                    {"cmd":"rmmod rg_spi_gpio", "gettype":"cmd", "delay":0.1},
                ],
            },
        },

        "MTD": {
            "chain8": {
                "name": "BIOS",
                "filesizecheck": 20480,  # bios check file size, Unit: K
                "is_support_warm_upg": 0,
            },
        },

        "TEST":{
            "fpga":[
                {
                    "chain": 1,
                    "file": "/etc/.upgrade_test/b6990_uport_fpga_test_header.bin",
                    "display_name": "UPORT_FPGA",
                },
                {
                    "chain": 2,
                    "file": "/etc/.upgrade_test/b6990_mac_fpga_test_header.bin",
                    "display_name": "MAC_FPGA",
                },
                {
                    "chain": 3,
                    "file": "/etc/.upgrade_test/b6990_dport_fpga_test_header.bin",
                    "display_name": "DPORT_FPGA",
                },
            ],
            "cpld":[
                {"chain":1, "file":"/etc/.upgrade_test/b6990_base_cpld_test_header.vme", "display_name":"BASE_CPLD"},
                {"chain":2, "file":"/etc/.upgrade_test/b6990_mac_cpld_ab_test_header.vme", "display_name":"MAC_CPLD_A/B"},
                {"chain":3, "file":"/etc/.upgrade_test/b6990_mac_cpld_c_test_header.vme", "display_name":"MAC_CPLD_C"},
                {"chain":4, "file":"/etc/.upgrade_test/b6990_uport_cpld_test_header.vme", "display_name":"UPORT_CPLD"},
                {"chain":5, "file":"/etc/.upgrade_test/b6990_dport_cpld_test_header.vme", "display_name":"DPORT_CPLD"},
                {"chain":6, "file":"/etc/.upgrade_test/b6990_ufan_cpld_test_header.vme", "display_name":"UFCB_CPLD"},
                {"chain":7, "file":"/etc/.upgrade_test/b6990_dfan_cpld_test_header.vme", "display_name":"DFCB_CPLD"},
                {"chain":8, "file":"/etc/.upgrade_test/b6990_cpu_cpld_test_header.vme", "display_name":"CPU_CPLD"},
            ],
        },
    },

    "BMC": {
        "name": "BMC",
        "init_cmd":[
            # 关闭BMC堆栈狗
            {"cmd": "ipmitool raw 0x32 0x03 0x02", "gettype": "cmd", "ignore_result": 1},
            # BMC LED喂狗超时时间设置为最大
            {"cmd": "platform_ipmi.py 'i2cset -f -y 14 0x1b 0x41 0xff'", "gettype": "cmd", "ignore_result": 1},
            # BMC灯设置为绿闪
            {"cmd": "platform_ipmi.py 'i2cset -f -y 14 0x1b 0x0b 0x03'", "gettype": "cmd", "ignore_result": 1},
        ],
        "finish_cmd": [ ],
    },
}

WARM_UPGRADE_PARAM = {
    "slot0": {
        "VME":{
            "chain1":[
                {   "name":"BASE_CPLD",
                    "refresh_file_judge_flag":1,
                    "refresh_file":"/etc/.cpld_refresh/mgmt_transfer_header.vme",
                    "init_cmd":[
                       {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0xcb, "value": [0x01], "delay": 0.1},
                       {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x3b, "value": [0x00], "delay": 0.1},
                       {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x36, "value": [0x2c], "delay": 0.1}, #bmc_ready
                    ],
                    "rw_recover_reg":[
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x11, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x16, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x17, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x19, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x1b, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x1c, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x21, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x23, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x24, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x25, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x2b, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x2c, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x2d, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x31, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x32, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x33, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x36, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x38, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x39, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x3d, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x3e, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x3f, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x40, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x41, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x43, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x44, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x45, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x46, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x49, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4b, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4c, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4d, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4e, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4f, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x51, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x53, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xb1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xb4, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xb6, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xb7, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xb8, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xbc, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xba, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xc3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xc5, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xc6, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xc7, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xc8, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xc9, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xca, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xcb, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xd0, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xd2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xd3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xd4, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xd5, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xd8, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xe0, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xe2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xf1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xf2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xf3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xf4, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xf5, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xfb, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xfc, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xfd, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xff, "read_len": 1, "value": None, "delay": 0.1},

                    ],
                    "after_upgrade_delay":30,
                    "after_upgrade_delay_timeout":60,
                    "access_check_reg":{"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x55, "read_len": 1, "value": 0x0, "okval": 0xff},
                    "finish_cmd":[
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x3b, "value": [0x03], "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0xcb, "value": [0x00], "delay": 0.1},
                    ],
                },
            ],
            "chain2":[
                {   "name":"MAC_CPLD_A/B",
                    "refresh_file_judge_flag":1,
                    "refresh_file":"/etc/.cpld_refresh/MAC_CPLDA_B_transfer_header.vme",
                    "init_cmd": [
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4c, "value": [0x03], "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x28, "value": [0x00], "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x28, "value": [0x00], "delay": 0.1},
                    ],
                    "rw_recover_reg":[
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x23, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x24, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x25, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x27, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x35, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x56, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x57, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x5d, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x5e, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x5f, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x63, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x64, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x65, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x70, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x71, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x72, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x76, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x77, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x78, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xd0, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xd1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xd2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xd3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xd4, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xe0, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xe1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xe2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xe3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xe4, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xef, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xf1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xf2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xf3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xf4, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xf5, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xfb, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xfc, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xfd, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0xff, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x59, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x5a, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x5b, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x5c, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x5d, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x5e, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x66, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x67, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x68, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x69, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x6a, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x6b, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x70, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x71, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x72, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x73, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x74, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x75, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x80, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x81, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x82, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x83, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x84, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x85, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xd0, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xd1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xd2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xd3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xd4, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xd5, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xd6, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xd7, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xd8, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xd9, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xda, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xe0, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xe1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xe2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xe3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xe4, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xe5, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xe6, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xe7, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xe8, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xe9, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xea, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xef, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xf1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xf2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xf3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xf4, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xf5, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xfb, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xfc, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xfd, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0xff, "read_len": 1, "value": None, "delay": 0.1},
                    ],
                    "after_upgrade_delay":1,
                    "after_upgrade_delay_timeout":30,
                    "access_check_reg": {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x55, "read_len": 1, "value": 0x0, "okval": 0xff},
                    "finish_cmd": [
                        {"gettype": "devfile", "path": "/dev/cpld5", "offset": 0x28, "value": [0x01], "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld4", "offset": 0x28, "value": [0x01], "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4c, "value": [0x00], "delay": 0.1},
                    ],
                },
            ],
            "chain3":[
                {   "name":"MAC_CPLD_C",
                    "refresh_file_judge_flag":1,
                    "refresh_file":"/etc/.cpld_refresh/MAC_CPLDC_transfer_header.vme",
                    "init_cmd": [
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4c, "value": [0x04], "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x46, "value": [0x00], "delay": 0.1},
                    ],
                    "rw_recover_reg":[
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x13, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x16, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x17, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x18, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x19, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x1a, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x21, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x32, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x34, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x35, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x36, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x37, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x49, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x4a, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x4b, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x52, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x59, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x62, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x63, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0xf1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0xf2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0xf3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0xf4, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0xf5, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0xfb, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0xfc, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0xfd, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0xff, "read_len": 1, "value": None, "delay": 0.1},
                    ],
                    "after_upgrade_delay":1,
                    "after_upgrade_delay_timeout":30,
                    "access_check_reg": {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x55, "read_len": 1, "value": 0x0, "okval": 0xff},
                    "finish_cmd": [
                        {"gettype": "devfile", "path": "/dev/cpld6", "offset": 0x46, "value": [0x01], "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4c, "value": [0x00], "delay": 0.1},
                    ],
                },
            ],
            "chain4":[
                {   "name":"UPORT_CPLD",
                    "refresh_file_judge_flag":1,
                    "refresh_file":"/etc/.cpld_refresh/Uport_transfer_header.vme",
                    "init_cmd": [
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4c, "value": [0x08], "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x23, "value": [0x00], "delay": 0.1},
                    ],
                    "rw_recover_reg":[
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x14, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x15, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x16, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x21, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x31, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x32, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x51, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x53, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x5a, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x5b, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x5c, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x5d, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x64, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x65, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x66, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x67, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x70, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x71, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x72, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x73, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x78, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x79, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x7a, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x7b, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xd0, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xd1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xd2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xd3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xd4, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xd5, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xd6, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xd7, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xd8, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xd9, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xda, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xdb, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xdc, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xdd, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xde, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xdf, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xd5, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xef, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xf1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xf2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xf3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xf4, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xf5, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xfb, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xfc, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xfd, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0xff, "read_len": 1, "value": None, "delay": 0.1},
                    ],
                    "after_upgrade_delay":1,
                    "after_upgrade_delay_timeout":30,
                    "access_check_reg": {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x55, "read_len": 1, "value": 0x0, "okval": 0xff},
                    "finish_cmd": [
                        {"gettype": "devfile", "path": "/dev/cpld2", "offset": 0x23, "value": [0x01], "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4c, "value": [0x00], "delay": 0.1},
                    ],
                },
            ],
            "chain5":[
                {   "name":"DPORT_CPLD",
                    "refresh_file_judge_flag":1,
                    "refresh_file":"/etc/.cpld_refresh/Dport_transfer_header.vme",
                    "init_cmd": [
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4c, "value": [0x10], "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x23, "value": [0x00], "delay": 0.1},
                    ],
                    "rw_recover_reg":[
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x14, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x15, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x16, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x21, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x31, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x32, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x51, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x53, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x5a, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x5b, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x5c, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x5d, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x64, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x65, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x66, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x67, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x70, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x71, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x72, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x73, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x78, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x79, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x7a, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x7b, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xd0, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xd1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xd2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xd3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xd4, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xd5, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xd6, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xd7, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xd8, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xd9, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xda, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xdb, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xdc, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xdd, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xde, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xdf, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xd5, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xef, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xf1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xf2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xf3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xf4, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xf5, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xfb, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xfc, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xfd, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0xff, "read_len": 1, "value": None, "delay": 0.1},
                    ],
                    "after_upgrade_delay":1,
                    "after_upgrade_delay_timeout":30,
                    "access_check_reg": {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x55, "read_len": 1, "value": 0x0, "okval": 0xff},
                    "finish_cmd": [
                        {"gettype": "devfile", "path": "/dev/cpld8", "offset": 0x23, "value": [0x01], "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4c, "value": [0x00], "delay": 0.1},
                    ],
                },
            ],
            "chain6":[
                {   "name":"UFCB_CPLD",
                    "refresh_file_judge_flag":1,
                    "refresh_file":"/etc/.cpld_refresh/Ufan_transfer_header.vme",
                    "init_cmd": [
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4c, "value": [0x20], "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0x40, "value": [0x00], "delay": 0.1},
                    ],
                    "rw_recover_reg":[
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0x20, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0x22, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0x31, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0x51, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0x53, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0x56, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0x58, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0x90, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0x91, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0x92, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0x93, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0xd0, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0xd1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0xd2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0xd3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0xf1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0xf2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0xf3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0xf4, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0xf5, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0xfb, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0xfc, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0xfd, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0xff, "read_len": 1, "value": None, "delay": 0.1},
                    ],
                    "after_upgrade_delay":1,
                    "after_upgrade_delay_timeout":30,
                    "access_check_reg": {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0x55, "read_len": 1, "value": 0x0, "okval": 0xff},
                    "finish_cmd": [
                        {"gettype": "devfile", "path": "/dev/cpld3", "offset": 0x40, "value": [0x01], "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4c, "value": [0x00], "delay": 0.1},
                    ],
                },
            ],
            "chain7":[
                {   "name":"DFCB_CPLD",
                    "refresh_file_judge_flag":1,
                    "refresh_file":"/etc/.cpld_refresh/Dfan_transfer_header.vme",
                    "init_cmd": [
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4c, "value": [0x40], "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0x40, "value": [0x00], "delay": 0.1},
                    ],
                    "rw_recover_reg":[
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0x20, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0x22, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0x31, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0x51, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0x53, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0x56, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0x58, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0x90, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0x91, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0x92, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0x93, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0xd0, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0xd1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0xd2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0xd3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0xf1, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0xf2, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0xf3, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0xf4, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0xf5, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0xfb, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0xfc, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0xfd, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0xff, "read_len": 1, "value": None, "delay": 0.1},
                    ],
                    "after_upgrade_delay":1,
                    "after_upgrade_delay_timeout":30,
                    "access_check_reg": {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0x55, "read_len": 1, "value": 0x0, "okval": 0xff},
                    "finish_cmd": [
                        {"gettype": "devfile", "path": "/dev/cpld7", "offset": 0x40, "value": [0x01], "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x4c, "value": [0x00], "delay": 0.1},
                    ],
                },
            ],
            "chain8":[
                {   "name":"CPU_CPLD",
                    "refresh_file_judge_flag":1,
                    "refresh_file":"/etc/.cpld_refresh/cpu_transfer_header.vme",
                    "init_cmd": [
                        {"gettype": "cmd", "cmd": "echo 497 > /sys/class/gpio/export"},
                        {"gettype": "cmd", "cmd": "echo high > /sys/class/gpio/gpio497/direction"},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0xcc, "value": [0x00], "delay": 0.1},
                    ],
                    "rw_recover_reg":[
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x17, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x41, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x51, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x52, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x53, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x54, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x60, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x61, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x62, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x74, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x81, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x82, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x83, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x84, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x85, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x86, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x87, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x88, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x89, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x8a, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x83, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x84, "read_len": 1, "value": None, "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0xcb, "read_len": 1, "value": None, "delay": 0.1},
                    ],
                    "after_upgrade_delay":1,
                    "after_upgrade_delay_timeout":30,
                    "access_check_reg": {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0xa, "read_len": 1, "value": 0x0, "okval": 0xff},
                    "finish_cmd": [
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0xcc, "value": [0x01], "delay": 0.1},
                        {"gettype": "devfile", "path": "/dev/cpld0", "offset": 0x21, "value": [0x01], "delay": 0.1},
                        {"gettype": "cmd", "cmd": "echo 0 > /sys/class/gpio/gpio497/value"},
                        {"gettype": "cmd", "cmd": "echo 497 > /sys/class/gpio/unexport"},
                    ],
                },
            ],
        },
        "SPI-LOGIC-DEV":{
            "chain1":[
                {   "name":"UPORT_FPGA",
                    "init_cmd":[
                        {"file":WARM_UPG_FLAG, "gettype":"creat_file"},
                        {"cmd": "setpci -s 00:10.0 0x50.W=0x0050", "gettype": "cmd"}, # link_disable
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xc8, "value":0x00},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xc8, "value":0x01, "delay": 1},
                    ],
                    "after_upgrade_delay":10,
                    "after_upgrade_delay_timeout":10,
                    "refresh_finish_flag_check": {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x64, "value":0x01, "read_len": 1},
                    "access_check_reg":{
                        "path":"/dev/fpga0", "offset":0x8, "value":[0x55, 0xaa, 0x5a, 0xa5], "read_len":4, "gettype":"devfile",
                        "polling_cmd":[
                            {"cmd": "setpci -s 00:10.0 0x50.W=0x0060", "gettype": "cmd", "delay":1}, # retrain_link
                            {"cmd": "setpci -s 00:10.0 0x52.w", "gettype": "cmd", "okval": 0x12, "timeout": 10, "mask": 0xff},# check link status
                            {"cmd":"rmmod rg_fpga_pcie", "gettype":"cmd"},
                            {"cmd":"modprobe rg_fpga_pcie", "gettype":"cmd", "delay":2},
                        ],
                        "polling_delay":0.1
                    },
                    "finish_cmd":[
                        {"cmd": "setpci -s 00:10.0 0x50.W=0x0060", "gettype": "cmd"}, # retrain_link
                        {"file":WARM_UPG_FLAG, "gettype":"remove_file"},
                    ],
                },
            ],
            "chain2": [
                {"name": "MAC_FPGA",
                    "init_cmd": [
                        {"file":WARM_UPG_FLAG, "gettype":"creat_file"},
                        {"cmd": "setpci -s 00:12.0 0x50.W=0x0050", "gettype": "cmd"}, # link_disable
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xc6, "value":0x00},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xc6, "value":0x01, "delay": 1},
                    ],
                    "after_upgrade_delay": 10,
                    "after_upgrade_delay_timeout": 10,
                    "refresh_finish_flag_check":{"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x63, "value":0x01, "read_len": 1},
                    "access_check_reg": {
                        "path": "/dev/fpga1", "offset": 0x8, "value": [0x55, 0xaa, 0x5a, 0xa5], "read_len":4, "gettype":"devfile",
                        "polling_cmd":[
                            {"cmd": "setpci -s 00:12.0 0x50.W=0x0060", "gettype": "cmd", "delay":1}, # retrain_link
                            {"cmd": "setpci -s 00:12.0 0x52.w", "gettype": "cmd", "okval": 0x12, "timeout": 10, "mask": 0xff},# check link status
                            {"cmd": "rmmod rg_fpga_pcie", "gettype": "cmd", "delay": 0.1},
                            {"cmd": "modprobe rg_fpga_pcie", "gettype": "cmd", "delay": 2},
                        ],
                        "polling_delay": 0.1
                    },
                    "finish_cmd": [
                        {"cmd": "setpci -s 00:12.0 0x50.W=0x0060", "gettype": "cmd"}, # retrain_link
                        {"file":WARM_UPG_FLAG, "gettype":"remove_file"},
                    ],
                },
            ],
            "chain3":[
                {   "name":"DPORT_FPGA",
                    "init_cmd":[
                        {"file":WARM_UPG_FLAG, "gettype":"creat_file"},
                        {"cmd": "setpci -s 00:11.0 0x50.W=0x0050", "gettype": "cmd"}, # link_disable
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xca, "value":0x00},
                        {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0xca, "value":0x01, "delay": 1},
                    ],
                    "after_upgrade_delay":10,
                    "after_upgrade_delay_timeout":10,
                    "refresh_finish_flag_check": {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x62, "value":0x01, "read_len": 1},
                    "access_check_reg":{
                        "path":"/dev/fpga2", "offset":0x8, "value":[0x55, 0xaa, 0x5a, 0xa5], "read_len":4, "gettype":"devfile",
                        "polling_cmd":[
                            {"cmd": "setpci -s 00:11.0 0x50.W=0x0060", "gettype": "cmd", "delay":1}, # retrain_link
                            {"cmd": "setpci -s 00:11.0 0x52.w", "gettype": "cmd", "okval": 0x12, "timeout": 10, "mask": 0xff},# check link status
                            {"cmd":"rmmod rg_fpga_pcie", "gettype":"cmd"},
                            {"cmd":"modprobe rg_fpga_pcie", "gettype":"cmd", "delay":2},
                        ],
                        "polling_delay":0.1
                    },
                    "finish_cmd":[
                        {"cmd": "setpci -s 00:11.0 0x50.W=0x0060", "gettype": "cmd"}, # retrain_link
                        {"file":WARM_UPG_FLAG, "gettype":"remove_file"},
                    ],
                },
            ],
        },
    },
    "stop_services_cmd":[
        "systemctl stop rg_platform_process.service",
    ],
    "start_services_cmd":[
        "systemctl start rg_platform_process.service",
    ],
}

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
        "arrt_index" : 1,
    },
    "bios_version": {
        "parent": "bios",
        "key": "Version",
        "cmd": "dmidecode -t 0 |grep Version",
        "pattern": r".*Version",
        "separator": ":",
        "arrt_index" : 2,
    },
    "bios_date": {
        "parent": "bios",
        "key": "Release Date",
        "cmd": "dmidecode -t 0 |grep Release",
        "pattern": r".*Release Date",
        "separator": ":",
        "arrt_index" : 3,
    },

    "bmc": {
        "key": "BMC",
        "next": "onie"
    },
    "bmc_version": {
        "parent": "bmc",
        "key": "Version",
        "cmd": "ipmitool mc info |grep \"Firmware Revision\"",
        "pattern": r".*Firmware Revision",
        "separator": ":",
        "arrt_index" : 1,
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
        "arrt_index" : 1,
    },
    "onie_version": {
        "parent": "onie",
        "key": "Version",
        "file": "/host/machine.conf",
        "pattern": r"^onie_version",
        "separator": "=",
        "arrt_index" : 2,
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
        "arrt_index" : 1,
    },
    "cpu_model": {
        "parent": "cpu",
        "key": "Device Model",
        "cmd": "dmidecode --type processor | grep Version",
        "pattern": r".*Version",
        "separator": ":",
        "arrt_index" : 2,
    },
    "cpu_core": {
        "parent": "cpu",
        "key": "Core Count",
        "cmd": "dmidecode --type processor | grep \"Core Count\"",
        "pattern": r".*Core Count",
        "separator": ":",
        "arrt_index" : 3,
    },
    "cpu_thread": {
        "parent": "cpu",
        "key": "Thread Count",
        "cmd": "dmidecode --type processor | grep \"Thread Count\"",
        "pattern": r".*Thread Count",
        "separator": ":",
        "arrt_index" : 4,
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
        "arrt_index" : 1,
    },
    "ssd_fw": {
        "parent": "ssd",
        "key": "Firmware Version",
        "cmd": "smartctl -i /dev/sda |grep \"Firmware Version\"",
        "pattern": r".*Firmware Version",
        "separator": ":",
        "arrt_index" : 2,
    },
    "ssd_user_cap": {
        "parent": "ssd",
        "key": "User Capacity",
        "cmd": "smartctl -i /dev/sda |grep \"User Capacity\"",
        "pattern": r".*User Capacity",
        "separator": ":",
        "arrt_index" : 3,
    },

    "cpld": {
        "key": "CPLD",
        "next": "i210"
    },

    "cpld1": {
        "key": "CPLD1",
        "parent": "cpld",
        "arrt_index" : 1,
    },
    "cpld1_model": {
        "key": "Device Model",
        "parent": "cpld1",
        "config" : "LCMXO3LF-2100C-5BG256C",
        "arrt_index" : 1,
    },
    "cpld1_vender": {
        "key": "Vendor",
        "parent": "cpld1",
        "config" : "LATTICE",
        "arrt_index" : 2,
    },
    "cpld1_desc": {
        "key": "Description",
        "parent": "cpld1",
        "config" : "CPU_CPLD",
        "arrt_index" : 3,
    },
    "cpld1_version": {
        "key": "Firmware Version",
        "parent": "cpld1",
        "reg": {
            "loc": "/dev/port",
            "offset": 0xa00,
            "size": 4
        },
        "callback": "cpld_format",
        "arrt_index" : 4,
    },

    "cpld2": {
        "key": "CPLD2",
        "parent": "cpld",
        "arrt_index" : 2,
    },
    "cpld2_model": {
        "key": "Device Model",
        "parent": "cpld2",
        "config" : "LCMXO3LF-4300C-6BG324I",
        "arrt_index" : 1,
    },
    "cpld2_vender": {
        "key": "Vendor",
        "parent": "cpld2",
        "config" : "LATTICE",
        "arrt_index" : 2,
    },
    "cpld2_desc": {
        "key": "Description",
        "parent": "cpld2",
        "config" : "BASE_CPLD",
        "arrt_index" : 3,
    },
    "cpld2_version": {
        "key": "Firmware Version",
        "parent": "cpld2",
        "reg": {
            "loc": "/dev/port",
            "offset": 0x900,
            "size": 4
        },
        "callback": "cpld_format",
        "arrt_index" : 4,
    },

    "cpld3": {
        "key": "CPLD3",
        "parent": "cpld",
        "arrt_index" : 3,
    },
    "cpld3_model": {
        "key": "Device Model",
        "parent": "cpld3",
        "config" : "LCMXO3LF-4300C-6BG324I",
        "arrt_index" : 1,
    },
    "cpld3_vender": {
        "key": "Vendor",
        "parent": "cpld3",
        "config" : "LATTICE",
        "arrt_index" : 2,
    },
    "cpld3_desc": {
        "key": "Description",
        "parent": "cpld3",
        "config" : "UPORT_CPLD",
        "arrt_index" : 3,
    },
    "cpld3_version": {
        "key": "Firmware Version",
        "parent": "cpld3",
        "i2c": {
            "bus": "62",
            "loc": "0x3d",
            "offset": 0,
            "size": 4
        },
        "callback": "cpld_format",
        "arrt_index" : 4,
    },

    "cpld4": {
        "key": "CPLD4",
        "parent": "cpld",
        "arrt_index" : 4,
    },
    "cpld4_model": {
        "key": "Device Model",
        "parent": "cpld4",
        "config" : "LCMXO3LF-2100C-5BG256C",
        "arrt_index" : 1,
    },
    "cpld4_vender": {
        "key": "Vendor",
        "parent": "cpld4",
        "config" : "LATTICE",
        "arrt_index" : 2,
    },
    "cpld4_desc": {
        "key": "Description",
        "parent": "cpld4",
        "config" : "UFCB_CPLD",
        "arrt_index" : 3,
    },
    "cpld4_version": {
        "key": "Firmware Version",
        "parent": "cpld4",
        "i2c": {
            "bus": "103",
            "loc": "0x0d",
            "offset": 0,
            "size": 4
        },
        "callback": "cpld_format",
        "arrt_index" : 4,
    },

    "cpld5": {
        "key": "CPLD5",
        "parent": "cpld",
        "arrt_index" : 5,
    },
    "cpld5_model": {
        "key": "Device Model",
        "parent": "cpld5",
        "config" : "LCMXO3LF-4300C-6BG256C",
        "arrt_index" : 1,
    },
    "cpld5_vender": {
        "key": "Vendor",
        "parent": "cpld5",
        "config" : "LATTICE",
        "arrt_index" : 2,
    },
    "cpld5_desc": {
        "key": "Description",
        "parent": "cpld5",
        "config" : "MAC_CPLDA",
        "arrt_index" : 3,
    },
    "cpld5_version": {
        "key": "Firmware Version",
        "parent": "cpld5",
        "i2c": {
            "bus": "87",
            "loc": "0x1d",
            "offset": 0,
            "size": 4
        },
        "callback": "cpld_format",
        "arrt_index" : 4,
    },

    "cpld6": {
        "key": "CPLD6",
        "parent": "cpld",
        "arrt_index" : 6,
    },
    "cpld6_model": {
        "key": "Device Model",
        "parent": "cpld6",
        "config" : "LCMXO3LF-4300C-6BG324I",
        "arrt_index" : 1,
    },
    "cpld6_vender": {
        "key": "Vendor",
        "parent": "cpld6",
        "config" : "LATTICE",
        "arrt_index" : 2,
    },
    "cpld6_desc": {
        "key": "Description",
        "parent": "cpld6",
        "config" : "MAC_CPLDB",
        "arrt_index" : 3,
    },
    "cpld6_version": {
        "key": "Firmware Version",
        "parent": "cpld6",
        "i2c": {
            "bus": "88",
            "loc": "0x2d",
            "offset": 0,
            "size": 4
        },
        "callback": "cpld_format",
        "arrt_index" : 4,
    },

    "cpld7": {
        "key": "CPLD7",
        "parent": "cpld",
        "arrt_index" : 7,
    },
    "cpld7_model": {
        "key": "Device Model",
        "parent": "cpld7",
        "config" : "LCMXO3LF-4300C-6BG324I",
        "arrt_index" : 1,
    },
    "cpld7_vender": {
        "key": "Vendor",
        "parent": "cpld7",
        "config" : "LATTICE",
        "arrt_index" : 2,
    },
    "cpld7_desc": {
        "key": "Description",
        "parent": "cpld7",
        "config" : "MAC_CPLDC",
        "arrt_index" : 3,
    },
    "cpld7_version": {
        "key": "Firmware Version",
        "parent": "cpld7",
        "i2c": {
            "bus": "89",
            "loc": "0x3d",
            "offset": 0,
            "size": 4
        },
        "callback": "cpld_format",
        "arrt_index" : 4,
    },

    "cpld8": {
        "key": "CPLD8",
        "parent": "cpld",
        "arrt_index" : 8,
    },
    "cpld8_model": {
        "key": "Device Model",
        "parent": "cpld8",
        "config" : "LCMXO3LF-2100C-5BG324I",
        "arrt_index" : 1,
    },
    "cpld8_vender": {
        "key": "Vendor",
        "parent": "cpld8",
        "config" : "LATTICE",
        "arrt_index" : 2,
    },
    "cpld8_desc": {
        "key": "Description",
        "parent": "cpld8",
        "config" : "DFCB_CPLD",
        "arrt_index" : 3,
    },
    "cpld8_version": {
        "key": "Firmware Version",
        "parent": "cpld8",
        "i2c": {
            "bus": "111",
            "loc": "0x0d",
            "offset": 0,
            "size": 4
        },
        "callback": "cpld_format",
        "arrt_index" : 4,
    },

    "cpld9": {
        "key": "CPLD9",
        "parent": "cpld",
        "arrt_index" : 9,
    },
    "cpld9_model": {
        "key": "Device Model",
        "parent": "cpld9",
        "config" : "LCMXO3LF-4300C-6BG324I",
        "arrt_index" : 1,
    },
    "cpld9_vender": {
        "key": "Vendor",
        "parent": "cpld9",
        "config" : "LATTICE",
        "arrt_index" : 2,
    },
    "cpld9_desc": {
        "key": "Description",
        "parent": "cpld9",
        "config" : "DPORT_CPLD",
        "arrt_index" : 3,
    },
    "cpld9_version": {
        "key": "Firmware Version",
        "parent": "cpld9",
        "i2c": {
            "bus": "127",
            "loc": "0x3d",
            "offset": 0,
            "size": 4
        },
        "callback": "cpld_format",
        "arrt_index" : 4,
    },

    "i210": {
        "key": "NIC",
        "next": "fpga"
    },
    "i210_model": {
        "parent": "i210",
        "config": "NA",
        "key": "Device Model",
        "arrt_index" : 1,
    },
    "i210_vendor": {
        "parent": "i210",
        "config": "INTEL",
        "key": "Vendor",
        "arrt_index" : 2,
    },
    "i210_version": {
        "parent": "i210",
        "cmd": "sudo ethtool -i eth0",
        "pattern": r"firmware-version",
        "separator": ":",
        "key": "Firmware Version",
        "arrt_index" : 3,
    },

    "fpga": {
        "key": "FPGA",
        "next": "others"
    },

    "fpga1": {
        "key": "FPGA1",
        "parent": "fpga",
        "arrt_index" : 1,
    },
    "fpga1_model": {
        "parent": "fpga1",
        "devfile": {
            "loc": "/dev/fpga0",
            "offset":0x98,
            "len":4,
            "bit_width":4
        },
        "decode": {
            "0x00000050": "XC7A50T-2FGG484I",
            "0x00000100": "XC7A100T-2FGG484I",
            "0x00000000": "XC7A100T-2FGG484I"
        },
        "key": "Device Model",
        "arrt_index" : 1,
    },
    "fpga1_vender": {
        "parent": "fpga1",
        "config" : "XILINX",
        "key": "Vendor",
        "arrt_index" : 2,
    },
    "fpga1_desc": {
        "key": "Description",
        "parent": "fpga1",
        "config" : "UPORT_FPGA",
        "arrt_index" : 3,
    },
    "fpga1_hw_version": {
        "parent": "fpga1",
        "config" : "NA",
        "key": "Hardware Version",
        "arrt_index" : 4,
    },
    "fpga1_fw_version": {
        "parent": "fpga1",
        "devfile": {
            "loc": "/dev/fpga0",
            "offset":0x0,
            "len":4,
            "bit_width":4
        },
        "key": "Firmware Version",
        "arrt_index" : 5,
    },

    "fpga2": {
        "key": "FPGA2",
        "parent": "fpga",
        "arrt_index" : 2,
    },
    "fpga2_model": {
        "parent": "fpga2",
        "devfile": {
            "loc": "/dev/fpga1",
            "offset":0xb0,
            "len":4,
            "bit_width":4
        },
        "decode": {
            "0x00000050": "XC7A50T-2FGG484I",
            "0x00000100": "XC7A100T-2FGG484I",
            "0x00000000": "XC7A100T-2FGG484I"
        },
        "key": "Device Model",
        "arrt_index" : 1,
    },
    "fpga2_vender": {
        "parent": "fpga2",
        "config" : "XILINX",
        "key": "Vendor",
        "arrt_index" : 2,
    },
    "fpga2_desc": {
        "key": "Description",
        "parent": "fpga2",
        "config" : "MAC_FPGA",
        "arrt_index" : 3,
    },
    "fpga2_hw_version": {
        "parent": "fpga2",
        "config" : "NA",
        "key": "Hardware Version",
        "arrt_index" : 4,
    },
    "fpga2_fw_version": {
        "parent": "fpga2",
        "devfile": {
            "loc": "/dev/fpga1",
            "offset":0x0,
            "len":4,
            "bit_width":4
        },
        "key": "Firmware Version",
        "arrt_index" : 5,
    },

    "fpga3": {
        "key": "FPGA3",
        "parent": "fpga",
        "arrt_index" : 3,
    },
    "fpga3_model": {
        "parent": "fpga3",
        "devfile": {
            "loc": "/dev/fpga2",
            "offset":0x98,
            "len":4,
            "bit_width":4
        },
        "decode": {
            "0x00000050": "XC7A50T-2FGG484I",
            "0x00000100": "XC7A100T-2FGG484I",
            "0x00000000": "XC7A100T-2FGG484I"
        },
        "key": "Device Model",
        "arrt_index" : 1,
    },
    "fpga3_vender": {
        "parent": "fpga3",
        "config" : "XILINX",
        "key": "Vendor",
        "arrt_index" : 2,
    },
    "fpga3_desc": {
        "key": "Description",
        "parent": "fpga3",
        "config" : "DPORT_FPGA",
        "arrt_index" : 3,
    },
    "fpga3_hw_version": {
        "parent": "fpga3",
        "config" : "NA",
        "key": "Hardware Version",
        "arrt_index" : 4,
    },
    "fpga3_fw_version": {
        "parent": "fpga3",
        "devfile": {
            "loc": "/dev/fpga2",
            "offset":0x0,
            "len":4,
            "bit_width":4
        },
        "key": "Firmware Version",
        "arrt_index" : 5,
    },

    "others": {
        "key": "OTHERS",
    },
    "5387": {
        "parent": "others",
        "key": "CPU-BMC-SWITCH",
        "arrt_index" : 1,
    },
    "5387_model": {
        "parent": "5387",
        "config": "BCM53134O",
        "key": "Device Model",
        "arrt_index" : 1,
    },
    "5387_vendor": {
        "parent": "5387",
        "config": "Broadcom",
        "key": "Vendor",
        "arrt_index" : 2,
    },
    "5387_hw_version": {
        "parent": "5387",
        "key": "Hardware Version",
        "func": {
            "funcname": "get_bcm5387_version",
            "params" : {
                "before": [
                    # OE拉高
                    {"gettype": "cmd", "cmd": "echo 323 > /sys/class/gpio/export"},
                    {"gettype": "cmd", "cmd": "echo high > /sys/class/gpio/gpio323/direction"},
                    # SEL1拉高
                    {"gettype": "cmd", "cmd": "echo 324 > /sys/class/gpio/export"},
                    {"gettype": "cmd", "cmd": "echo high > /sys/class/gpio/gpio324/direction"},
                    # 使能
                    {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x3d, "value":0x00},
                    # 选择53134升级
                    {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x45, "value":0x01},
                    # 使能53134通路
                    {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x46, "value":0x06},
                ],
                "get_version" : "md5sum /sys/bus/spi/devices/spi0.0/eeprom | awk '{print $1}'",
                "after": [
                    {"gettype": "cmd", "cmd": "echo 0 > /sys/class/gpio/gpio324/value"},
                    {"gettype": "cmd", "cmd": "echo 324 > /sys/class/gpio/unexport"},
                    {"gettype": "cmd", "cmd": "echo 0 > /sys/class/gpio/gpio323/value"},
                    {"gettype": "cmd", "cmd": "echo 323 > /sys/class/gpio/unexport"},
                ],
                "finally": [
                    {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x46, "value":0x00},
                    {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x45, "value":0x00},
                    {"gettype": "devfile", "path": "/dev/cpld1", "offset": 0x3d, "value":0x01},
                ],
            },
        },
        "arrt_index" : 3,
    },
}

PMON_SYSLOG_STATUS = {
    "polling_time": 3,
    "sffs": {
        "present": {"path": ["/sys/s3ip/transceiver/*/present"], "ABSENT":0},
        "nochangedmsgflag": 0,
        "nochangedmsgtime": 60,
        "noprintfirsttimeflag": 1,
        "alias": {
            "eth1": "Eth1",
            "eth2": "Eth2",
            "eth3": "Eth3",
            "eth4": "Eth4",
            "eth5": "Eth5",
            "eth6": "Eth6",
            "eth7": "Eth7",
            "eth8": "Eth8",
            "eth9": "Eth9",
            "eth10": "Eth10",
            "eth11": "Eth11",
            "eth12": "Eth12",
            "eth13": "Eth13",
            "eth14": "Eth14",
            "eth15": "Eth15",
            "eth16": "Eth16",
            "eth17": "Eth17",
            "eth18": "Eth18",
            "eth19": "Eth19",
            "eth20": "Eth20",
            "eth21": "Eth21",
            "eth22": "Eth22",
            "eth23": "Eth23",
            "eth24": "Eth24",
            "eth25": "Eth25",
            "eth26": "Eth26",
            "eth27": "Eth27",
            "eth28": "Eth28",
            "eth29": "Eth29",
            "eth30": "Eth30",
            "eth31": "Eth31",
            "eth32": "Eth32",
            "eth33": "Eth33",
            "eth34": "Eth34",
            "eth35": "Eth35",
            "eth36": "Eth36",
            "eth37": "Eth37",
            "eth38": "Eth38",
            "eth39": "Eth39",
            "eth40": "Eth40",
            "eth41": "Eth41",
            "eth42": "Eth42",
            "eth43": "Eth43",
            "eth44": "Eth44",
            "eth45": "Eth45",
            "eth46": "Eth46",
            "eth47": "Eth47",
            "eth48": "Eth48",
            "eth49": "Eth49",
            "eth50": "Eth50",
            "eth51": "Eth51",
            "eth52": "Eth52",
            "eth53": "Eth53",
            "eth54": "Eth54",
            "eth55": "Eth55",
            "eth56": "Eth56",
            "eth57": "Eth57",
            "eth58": "Eth58",
            "eth59": "Eth59",
            "eth60": "Eth60",
            "eth61": "Eth61",
            "eth62": "Eth62",
            "eth63": "Eth63",
            "eth64": "Eth64",
            "eth65": "Eth65",
            "eth66": "Eth66",
            "eth67": "Eth67",
            "eth68": "Eth68",
            "eth69": "Eth69",
            "eth70": "Eth70",
            "eth71": "Eth71",
            "eth72": "Eth72",
            "eth73": "Eth73",
            "eth74": "Eth74",
            "eth75": "Eth75",
            "eth76": "Eth76",
            "eth77": "Eth77",
            "eth78": "Eth78",
            "eth79": "Eth79",
            "eth80": "Eth80",
            "eth81": "Eth81",
            "eth82": "Eth82",
            "eth83": "Eth83",
            "eth84": "Eth84",
            "eth85": "Eth85",
            "eth86": "Eth86",
            "eth87": "Eth87",
            "eth88": "Eth88",
            "eth89": "Eth89",
            "eth90": "Eth90",
            "eth91": "Eth91",
            "eth92": "Eth92",
            "eth93": "Eth93",
            "eth94": "Eth94",
            "eth95": "Eth95",
            "eth96": "Eth96",
            "eth97": "Eth97",
            "eth98": "Eth98",
            "eth99": "Eth99",
            "eth100": "Eth100",
            "eth101": "Eth101",
            "eth102": "Eth102",
            "eth103": "Eth103",
            "eth104": "Eth104",
            "eth105": "Eth105",
            "eth106": "Eth106",
            "eth107": "Eth107",
            "eth108": "Eth108",
            "eth109": "Eth109",
            "eth110": "Eth110",
            "eth111": "Eth111",
            "eth112": "Eth112",
            "eth113": "Eth113",
            "eth114": "Eth114",
            "eth115": "Eth115",
            "eth116": "Eth116",
            "eth117": "Eth117",
            "eth118": "Eth118",
            "eth119": "Eth119",
            "eth120": "Eth120",
            "eth121": "Eth121",
            "eth122": "Eth122",
            "eth123": "Eth123",
            "eth124": "Eth124",
            "eth125": "Eth125",
            "eth126": "Eth126",
            "eth127": "Eth127",
            "eth128": "Eth128",
        }
    },
    "fans": {
        "present": {"path": ["/sys/s3ip/fan/*/status"], "ABSENT":0},
        "status": [
            {"path": "/sys/s3ip/fan/%s/status", 'okval': 1},
        ],
        "nochangedmsgflag": 1,
        "nochangedmsgtime": 60,
        "noprintfirsttimeflag": 0
    },
    "psus": {
        "present" : {"path": ["/sys/s3ip/psu/*/present"], "ABSENT":0},
        "status" : [
            {"path": "/sys/s3ip/psu/%s/out_status", "okval":1},
        ],
        "nochangedmsgflag": 1,
        "nochangedmsgtime": 60,
        "noprintfirsttimeflag": 0
    },
    "temps": {
        "temps_list":[
            {"name":"MGMT_AIR_INLET_1", "input_path":["/sys/bus/i2c/devices/123-004b/hwmon/hwmon*/temp1_input"], "input_accuracy":1000, "warning":50, "critical":55},
            {"name":"MGMT_AIR_INLET_2", "input_path":["/sys/bus/i2c/devices/124-004b/hwmon/hwmon*/temp1_input"], "input_accuracy":1000, "warning":50, "critical":55},
            {"name":"UPORT_AIR_INLET", "input_path":["/sys/bus/i2c/devices/65-004b/hwmon/hwmon*/temp1_input"], "input_accuracy":1000, "warning":75, "critical":80},
            {"name":"DPORT_AIR_INLET", "input_path":["/sys/bus/i2c/devices/130-004b/hwmon/hwmon*/temp1_input"], "input_accuracy":1000, "warning":75, "critical":80},
            {"name":"MAC_AIR_INLET_1", "input_path":["/sys/bus/i2c/devices/71-004b/hwmon/hwmon*/temp1_input"], "input_accuracy":1000, "warning":75, "critical":80},
            {"name":"MAC_AIR_INLET_2", "input_path":["/sys/bus/i2c/devices/72-004f/hwmon/hwmon*/temp1_input"], "input_accuracy":1000, "warning":75, "critical":80},
            {"name":"UPORT_FAN_AIR_OUTLET", "input_path":["/sys/bus/i2c/devices/104-004b/hwmon/hwmon*/temp1_input"], "input_accuracy":1000, "warning":70, "critical":75},
            {"name":"DPORT_FAN_AIR_OUTLET", "input_path":["/sys/bus/i2c/devices/112-004b/hwmon/hwmon*/temp1_input"], "input_accuracy":1000, "warning":70, "critical":75},
            {"name":"CPU_TEMP", "input_path":"/sys/bus/platform/devices/coretemp.0/hwmon/hwmon*/temp1_input", "input_accuracy":1000, "warning":100, "critical":102},
            {"name":"MAC_TEMP_MAX", "input_path":"/sys/s3ip/temp_sensor/temp15/value", "input_accuracy":1000, "warning":100, "critical":105},
            {"name":"MAC_TEMP_MIN", "input_path":"/sys/s3ip/temp_sensor/temp14/value", "input_accuracy":1000, "warning":100, "critical":105},
        ],
        "over_temps_polling_seconds": 60,
    },
}
