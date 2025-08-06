#!/usr/bin/python
# -*- coding: UTF-8 -*-
from collections import OrderedDict

RUIJIE_CARDID = 0x0000409F
RUIJIE_PRODUCTNAME = "B6990-128QC"
RUIJIE_PART_NUMBER = "01013202"
RUIJIE_LABEL_REVISION = "BN"
RUIJIE_ONIE_VERSION = "2018.02"
RUIJIE_MAC_SIZE = 3
RUIJIE_MANUF_NAME = "Ruijie"
RUIJIE_MANUF_COUNTRY = "CN"
RUIJIE_VENDOR_NAME = "Ruijie"
RUIJIE_DIAG_VERSION = "0.1.0.15"
RUIJIE_SERVICE_TAG = "www.ruijie.com.cn"

# 启机模块
STARTMODULE = {
    "hal_fanctrl": 1,
    "xdpe_avscontrol": 1,
    "hal_ledctrl": 1,
    "avscontrol": 1,
    "dev_monitor": 1,
    "pmon_syslog": 1,
    "tty_console": 1,
    "macledreset": 1,
    "sff_temp_polling": 1,
    "generate_airflow": 1,
    "reboot_cause": 1,
}

fanlevel = {
    "tips": ["低", "中", "高"],
    "level": [102, 150, 255],
}
fanlevel = fanlevel

BIOS_TEST = {
    "switch_master": [
        {"io_addr": 0x9C3, "val": 0x00, "gettype": "io"},
    ],
    "switch_slave": [
        {"io_addr": 0x9C3, "val": 0x01, "gettype": "io"},
    ],
}

CPU_CPLD_TEST = [
    {"test_name": "底板CPLD在线升级通路测试",
     "open_gpio": [
         {"cmd": "echo 39 > /sys/class/gpio/export", "sleep": 0.1},
         {"cmd": "echo out > /sys/class/gpio/gpio39/direction"},
         {"cmd": "echo 1 > /sys/class/gpio/gpio39/value"},
     ],
     "close_gpio": [
         {"cmd": "echo 0 > /sys/class/gpio/gpio39/value"},
         {"cmd": "echo 39 > /sys/class/gpio/unexport"},
     ],
     },
    {"test_name": "CPU CPLD在线升级通路测试",
     "open_gpio": [
         {"cmd": "echo 50 > /sys/class/gpio/export", "sleep": 0.1},
         {"cmd": "echo out > /sys/class/gpio/gpio50/direction"},
         {"cmd": "echo 1 > /sys/class/gpio/gpio50/value"},
         {"cmd": "echo 48 > /sys/class/gpio/export", "sleep": 0.1},
         {"cmd": "echo out > /sys/class/gpio/gpio48/direction"},
         {"cmd": "echo 1 > /sys/class/gpio/gpio48/value"},
         {"cmd": "dfd_debug io_wr 0x918 0x01"},
     ],
     "close_gpio": [
         {"cmd": "dfd_debug io_wr 0x918 0x00"},
         {"cmd": "echo 0 > /sys/class/gpio/gpio48/value"},
         {"cmd": "echo 48 > /sys/class/gpio/unexport"},
         {"cmd": "echo 0 > /sys/class/gpio/gpio50/value"},
         {"cmd": "echo 50 > /sys/class/gpio/unexport"},
     ],
     },
    {"test_name": "上FAN板CPLD在线升级通路测试",
     "open_gpio": [
         {"cmd": "echo 50 > /sys/class/gpio/export", "sleep": 0.1},
         {"cmd": "echo out > /sys/class/gpio/gpio50/direction"},
         {"cmd": "echo 1 > /sys/class/gpio/gpio50/value"},
         {"cmd": "echo 48 > /sys/class/gpio/export", "sleep": 0.1},
         {"cmd": "echo out > /sys/class/gpio/gpio48/direction"},
         {"cmd": "echo 1 > /sys/class/gpio/gpio48/value"},
         {"cmd": "dfd_debug io_wr 0x918 0x04"},
     ],
     "close_gpio": [
         {"cmd": "dfd_debug io_wr 0x918 0x00"},
         {"cmd": "echo 0 > /sys/class/gpio/gpio48/value"},
         {"cmd": "echo 48 > /sys/class/gpio/unexport"},
         {"cmd": "echo 0 > /sys/class/gpio/gpio50/value"},
         {"cmd": "echo 50 > /sys/class/gpio/unexport"},
     ],
     },
    {"test_name": "下FAN板CPLD在线升级通路测试",
     "open_gpio": [
         {"cmd": "echo 50 > /sys/class/gpio/export", "sleep": 0.1},
         {"cmd": "echo out > /sys/class/gpio/gpio50/direction"},
         {"cmd": "echo 1 > /sys/class/gpio/gpio50/value"},
         {"cmd": "echo 48 > /sys/class/gpio/export", "sleep": 0.1},
         {"cmd": "echo out > /sys/class/gpio/gpio48/direction"},
         {"cmd": "echo 1 > /sys/class/gpio/gpio48/value"},
         {"cmd": "dfd_debug io_wr 0x918 0x05"},
     ],
     "close_gpio": [
         {"cmd": "dfd_debug io_wr 0x918 0x00"},
         {"cmd": "echo 0 > /sys/class/gpio/gpio48/value"},
         {"cmd": "echo 48 > /sys/class/gpio/unexport"},
         {"cmd": "echo 0 > /sys/class/gpio/gpio50/value"},
         {"cmd": "echo 50 > /sys/class/gpio/unexport"},
     ],
     },
    {"test_name": "MAC板CPLD在线升级通路测试",
     "open_gpio": [
         {"cmd": "echo 50 > /sys/class/gpio/export", "sleep": 0.1},
         {"cmd": "echo out > /sys/class/gpio/gpio50/direction"},
         {"cmd": "echo 1 > /sys/class/gpio/gpio50/value"},
         {"cmd": "echo 48 > /sys/class/gpio/export", "sleep": 0.1},
         {"cmd": "echo out > /sys/class/gpio/gpio48/direction"},
         {"cmd": "echo 1 > /sys/class/gpio/gpio48/value"},
         {"cmd": "dfd_debug io_wr 0x918 0x02"},
         {"cmd": "dfd_debug io_wr 0x946 0x3d"},
     ],
     "close_gpio": [
         {"cmd": "dfd_debug io_wr 0x918 0x00"},
         {"cmd": "dfd_debug io_wr 0x946 0x3f"},
         {"cmd": "echo 0 > /sys/class/gpio/gpio48/value"},
         {"cmd": "echo 48 > /sys/class/gpio/unexport"},
         {"cmd": "echo 0 > /sys/class/gpio/gpio50/value"},
         {"cmd": "echo 50 > /sys/class/gpio/unexport"},
     ],
     },
    {"test_name": "UPORT板CPLD在线升级通路测试",
     "open_gpio": [
         {"cmd": "echo 50 > /sys/class/gpio/export", "sleep": 0.1},
         {"cmd": "echo out > /sys/class/gpio/gpio50/direction"},
         {"cmd": "echo 1 > /sys/class/gpio/gpio50/value"},
         {"cmd": "echo 48 > /sys/class/gpio/export", "sleep": 0.1},
         {"cmd": "echo out > /sys/class/gpio/gpio48/direction"},
         {"cmd": "echo 1 > /sys/class/gpio/gpio48/value"},
         {"cmd": "dfd_debug io_wr 0x918 0x07"},
         {"cmd": "dfd_debug io_wr 0x946 0x1f"},
     ],
     "close_gpio": [
         {"cmd": "dfd_debug io_wr 0x946 0x3f"},
         {"cmd": "dfd_debug io_wr 0x918 0x00"},
         {"cmd": "echo 0 > /sys/class/gpio/gpio48/value"},
         {"cmd": "echo 48 > /sys/class/gpio/unexport"},
         {"cmd": "echo 0 > /sys/class/gpio/gpio50/value"},
         {"cmd": "echo 50 > /sys/class/gpio/unexport"},
     ],
     },
    {"test_name": "DPORT板CPLD在线升级通路测试",
     "open_gpio": [
         {"cmd": "echo 50 > /sys/class/gpio/export", "sleep": 0.1},
         {"cmd": "echo out > /sys/class/gpio/gpio50/direction"},
         {"cmd": "echo 1 > /sys/class/gpio/gpio50/value"},
         {"cmd": "echo 48 > /sys/class/gpio/export", "sleep": 0.1},
         {"cmd": "echo out > /sys/class/gpio/gpio48/direction"},
         {"cmd": "echo 1 > /sys/class/gpio/gpio48/value"},
         {"cmd": "dfd_debug io_wr 0x918 0x03"},
         {"cmd": "dfd_debug io_wr 0x946 0x37"},
     ],
     "close_gpio": [
         {"cmd": "dfd_debug io_wr 0x946 0x3f"},
         {"cmd": "dfd_debug io_wr 0x918 0x00"},
         {"cmd": "echo 0 > /sys/class/gpio/gpio48/value"},
         {"cmd": "echo 48 > /sys/class/gpio/unexport"},
         {"cmd": "echo 0 > /sys/class/gpio/gpio50/value"},
         {"cmd": "echo 50 > /sys/class/gpio/unexport"},
     ],
     },
]


CPU_FPGA_TEST = [
    {"test_name": "MAC FPGA upgrade test", "cmd": "firmware_upgrade fpga test fpga0"},
]

SwitchCpldGpio = {
    "cpu_open_gpio": [
        {"cmd": "echo 50 > /sys/class/gpio/export", "sleep": 0.1},
        {"cmd": "echo out > /sys/class/gpio/gpio50/direction"},
        {"cmd": "echo 1 > /sys/class/gpio/gpio50/value"},
        {"cmd": "echo 48 > /sys/class/gpio/export", "sleep": 0.1},
        {"cmd": "echo out > /sys/class/gpio/gpio48/direction"},
        {"cmd": "echo 1 > /sys/class/gpio/gpio48/value"},
        {"cmd": "dfd_debug io_wr 0x918 1"},
    ],
    "cpu_close_gpio": [
        {"cmd": "dfd_debug io_wr 0x918 0"},
        {"cmd": "echo 0 > /sys/class/gpio/gpio48/value"},
        {"cmd": "echo 48 > /sys/class/gpio/unexport"},
        {"cmd": "echo 0 > /sys/class/gpio/gpio50/value"},
        {"cmd": "echo 50 > /sys/class/gpio/unexport"},
    ],
    "bmc_open_gpio": [
        {"cmd": "echo 392 > /sys/class/gpio/export", "sleep": 0.1},
        {"cmd": "echo out > /sys/class/gpio/gpio392/direction"},
        {"cmd": "echo 0 > /sys/class/gpio/gpio392/value"},
        {"cmd": "echo 392 > /sys/class/gpio/unexport"},
    ],
    "bmc_close_gpio": [
        {"cmd": "echo 392 > /sys/class/gpio/export", "sleep": 0.1},
        {"cmd": "echo out > /sys/class/gpio/gpio392/direction"},
        {"cmd": "echo 1 > /sys/class/gpio/gpio392/value"},
        {"cmd": "echo 392 > /sys/class/gpio/unexport"},
    ],
}

SetEnv5387 = {
    "SetEnv": [
        {"cmd": "modprobe rg_spi_93xx46", "sleep": 0.2},
        {"cmd": "i2cset -f -y 0 0x3b 0x3d 0x0", "sleep": 0.1},
        {"cmd": "i2cset -f -y 0 0x3b 0x46 0x6"},
        {"cmd": "i2cset -f -y 0 0x3b 0x45 0x2"},
        {"cmd": "i2cset -f -y 0 0x3b 0x42 0x0"},
        {"cmd": "echo 901 > /sys/class/gpio/export", "sleep": 0.1},
        {"cmd": "echo out > /sys/class/gpio/gpio901/direction", "sleep": 0.1},
        {"cmd": "echo 0 > /sys/class/gpio/gpio901/value", "sleep": 0.1},
    ],
    "ClearEnv": [
        {"cmd": "echo 1 > /sys/class/gpio/gpio901/value"},
        {"cmd": "echo 901 > /sys/class/gpio/unexport"},
    ],
    "SetCpuEnv": [
        {"cmd": "modprobe rg_spi_gpio", "sleep": 0.2},
        {"cmd": "modprobe rg_spi_93xx46", "sleep": 0.2},
        {"cmd": "echo 10051 > /sys/class/gpio/export", "sleep": 0.1},
        {"cmd": "echo high > /sys/class/gpio/gpio10051/direction", "sleep": 0.1},
        {"cmd": "echo 10052 > /sys/class/gpio/export", "sleep": 0.1},
        {"cmd": "echo high > /sys/class/gpio/gpio10052/direction", "sleep": 0.1},
        {"cmd": "dfd_debug io_wr 0x93d 0"},
        {"cmd": "dfd_debug io_wr 0x946 6"},
        {"cmd": "dfd_debug io_wr 0x945 1"},
    ],
    "ClearCpuEnv": [
        {"cmd": "echo 0 > /sys/class/gpio/gpio10052/value"},
        {"cmd": "echo 10052 > /sys/class/gpio/unexport"},
        {"cmd": "echo 0 > /sys/class/gpio/gpio10051/value"},
        {"cmd": "echo 10051 > /sys/class/gpio/unexport"},
        {"cmd": "dfd_debug io_wr 0x945 0x3"},
        {"cmd": "dfd_debug io_wr 0x946 0x0"},
        {"cmd": "dfd_debug io_wr 0x93d 1"},
        {"cmd": "rmmod rg_spi_93xx46"},
        {"cmd": "rmmod rg_spi_gpio"},
    ],
}
FRULISTS = {
    "fans": [
        {"name": "FAN板FAN1", "bus": 105, "loc": 0x50},
        {"name": "FAN板FAN2", "bus": 113, "loc": 0x50},
        {"name": "FAN板FAN3", "bus": 106, "loc": 0x50},
        {"name": "FAN板FAN4", "bus": 114, "loc": 0x50},
        {"name": "FAN板FAN5", "bus": 107, "loc": 0x50},
        {"name": "FAN板FAN6", "bus": 115, "loc": 0x50},
        {"name": "FAN板FAN7", "bus": 108, "loc": 0x50},
        {"name": "FAN板FAN8", "bus": 116, "loc": 0x50},
    ],
    "psus": [
        {"loc": 0x50, "bus": 95, "name": "PSU1"},
        {"loc": 0x50, "bus": 96, "name": "PSU2"},
        {"loc": 0x50, "bus": 97, "name": "PSU3"},
        {"loc": 0x50, "bus": 98, "name": "PSU4"},
    ]
}

DCDC_LIST = [
    {"Sensor": "MGMT_VDD12V", "CriticalLow": 10800, "CriticalHigh": 13200, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in1_input", "Address": "dc-i2c-121-5b"},
    {"Sensor": "MGMT_VDD3.3_STBY", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in2_input", "Address": "dc-i2c-121-5b"},
    {"Sensor": "MGMT_VDD5V_USB", "CriticalLow": 4500, "CriticalHigh": 5500, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in3_input", "Address": "dc-i2c-121-5b"},
    {"Sensor": "MGMT_PHY_VDD1V0", "CriticalLow": 900, "CriticalHigh": 1100, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in4_input", "Address": "dc-i2c-121-5b"},
    {"Sensor": "MGMT_VDD3.3V", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in5_input", "Address": "dc-i2c-121-5b"},
    {"Sensor": "MGMT_PHY_VDD1V8", "CriticalLow": 1620, "CriticalHigh": 1980, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in6_input", "Address": "dc-i2c-121-5b"},
    {"Sensor": "MGMT_VDD3.3_CLK", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in7_input", "Address": "dc-i2c-121-5b"},
    {"Sensor": "MGMT_VDD2.5V", "CriticalLow": 2250, "CriticalHigh": 2750, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in8_input", "Address": "dc-i2c-121-5b"},
    {"Sensor": "MGMT_SSD1_VDD3.3V", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in9_input", "Address": "dc-i2c-121-5b"},
    {"Sensor": "MGMT_SSD2_VDD3.3V", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in10_input", "Address": "dc-i2c-121-5b"},
    {"Sensor": "MGMT_VDD3V8_CLK", "CriticalLow": 3420, "CriticalHigh": 4180, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in11_input", "Address": "dc-i2c-121-5b"},
    {"Sensor": "UPORT_VDD12V", "CriticalLow": 10800, "CriticalHigh": 13200, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in1_input", "Address": "dc-i2c-64-5b"},
    {"Sensor": "UPORT_VDD3.3V_standby", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in2_input", "Address": "dc-i2c-64-5b"},
    {"Sensor": "UPORT_VDD1.0V_FPGA", "CriticalLow": 900, "CriticalHigh": 1100, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in3_input", "Address": "dc-i2c-64-5b"},
    {"Sensor": "UPORT_VDD1.8V_FPGA", "CriticalLow": 1620, "CriticalHigh": 1980, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in4_input", "Address": "dc-i2c-64-5b"},
    {"Sensor": "UPORT_VDD1.2V_FPGA", "CriticalLow": 1080, "CriticalHigh": 1320, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in5_input", "Address": "dc-i2c-64-5b"},
    {"Sensor": "UPORT_VDD3.3V", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in6_input", "Address": "dc-i2c-64-5b"},
    {"Sensor": "UPORT_VDD5V_VR", "CriticalLow": 4500, "CriticalHigh": 5500, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in7_input", "Address": "dc-i2c-64-5b"},
    {"Sensor": "UPORT_QSFP112_VDD3.3V_A", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in8_input", "Address": "dc-i2c-64-5b"},
    {"Sensor": "UPORT_QSFP112_VDD3.3V_B", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in9_input", "Address": "dc-i2c-64-5b"},
    {"Sensor": "UPORT_XDPE_QSFP112_VDD3.3V_A_V", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/66-0070/hwmon/hwmon*/in3_input", "Address": "dc-i2c-66-70", "format": "int(int('%s', 10)*1.5)"},
    {"Sensor": "UPORT_XDPE_QSFP112_VDD3.3V_A_C", "CriticalLow": -5000, "CriticalHigh": 60900, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/66-0070/hwmon/hwmon*/curr3_input", "Address": "dc-i2c-66-70"},
    {"Sensor": "UPORT_XDPE_QSFP112_VDD3.3V_B_V", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/66-0070/hwmon/hwmon*/in4_input", "Address": "dc-i2c-66-70", "format": "int(int('%s', 10)*1.5)"},
    {"Sensor": "UPORT_XDPE_QSFP112_VDD3.3V_B_C", "CriticalLow": -5000, "CriticalHigh": 63800, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/66-0070/hwmon/hwmon*/curr4_input", "Address": "dc-i2c-66-70"},
    {"Sensor": "MAC_XDPE_VDD_CORE_V", "CriticalLow": 720, "CriticalHigh": 880, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/81-0040/hwmon/hwmon*/in3_input", "Address": "dc-i2c-81-40"},
    {"Sensor": "MAC_XDPE_VDD_CORE_C", "CriticalLow": -1000, "CriticalHigh": 909700, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/81-0040/hwmon/hwmon*/curr3_input", "Address": "dc-i2c-81-40"},
    {"Sensor": "MAC_XDPE_VDD0_9V_ANLG0_V", "CriticalLow": 810, "CriticalHigh": 990, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/82-004d/hwmon/hwmon*/in3_input", "Address": "dc-i2c-82-4d"},
    {"Sensor": "MAC_XDPE_VDD0_9V_ANLG0_C", "CriticalLow": -1000, "CriticalHigh": 77737, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/82-004d/hwmon/hwmon*/curr3_input", "Address": "dc-i2c-82-4d"},
    {"Sensor": "MAC_XDPE_VDD0_75V_ANLG0_V", "CriticalLow": 675, "CriticalHigh": 825, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/82-004d/hwmon/hwmon*/in4_input", "Address": "dc-i2c-82-4d"},
    {"Sensor": "MAC_XDPE_VDD0_75V_ANLG0_C", "CriticalLow": -1000, "CriticalHigh": 38825.6, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/82-004d/hwmon/hwmon*/curr4_input", "Address": "dc-i2c-82-4d"},
    {"Sensor": "MAC_XDPE_VDD0_9V_ANLG1_V", "CriticalLow": 810, "CriticalHigh": 990, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/83-004d/hwmon/hwmon*/in3_input", "Address": "dc-i2c-83-4d"},
    {"Sensor": "MAC_XDPE_VDD0_9V_ANLG1_C", "CriticalLow": -1000, "CriticalHigh": 77737, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/83-004d/hwmon/hwmon*/curr3_input", "Address": "dc-i2c-83-4d"},
    {"Sensor": "MAC_XDPE_VDD0_75V_ANLG1_V", "CriticalLow": 675, "CriticalHigh": 825, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/83-004d/hwmon/hwmon*/in4_input", "Address": "dc-i2c-83-4d"},
    {"Sensor": "MAC_XDPE_VDD0_75V_ANLG1_C", "CriticalLow": -1000, "CriticalHigh": 38825.6, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/83-004d/hwmon/hwmon*/curr4_input", "Address": "dc-i2c-83-4d"},
    {"Sensor": "MAC_XDPE_QSFP112_VDD3.3V_A_V", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/84-0070/hwmon/hwmon*/in3_input", "Address": "dc-i2c-84-70", "format": "int(int('%s', 10)*1.5)"},
    {"Sensor": "MAC_XDPE_QSFP112_VDD3.3V_A_C", "CriticalLow": -5000, "CriticalHigh": 88000, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/84-0070/hwmon/hwmon*/curr3_input", "Address": "dc-i2c-84-70"},
    {"Sensor": "MAC_XDPE_QSFP112_VDD3.3V_B_V", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/84-0070/hwmon/hwmon*/in4_input", "Address": "dc-i2c-84-70", "format": "int(int('%s', 10)*1.5)"},
    {"Sensor": "MAC_XDPE_QSFP112_VDD3.3V_B_C", "CriticalLow": -5000, "CriticalHigh": 88000, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/84-0070/hwmon/hwmon*/curr4_input", "Address": "dc-i2c-84-70"},
    {"Sensor": "MAC_XDPE_QSFP112_VDD3.3V_C_V", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/85-0070/hwmon/hwmon*/in3_input", "Address": "dc-i2c-85-70", "format": "int(int('%s', 10)*1.5)"},
    {"Sensor": "MAC_XDPE_QSFP112_VDD3.3V_C_C", "CriticalLow": -5000, "CriticalHigh": 88000, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/85-0070/hwmon/hwmon*/curr3_input", "Address": "dc-i2c-85-70"},
    {"Sensor": "MAC_XDPE_QSFP112_VDD3.3V_D_V", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/85-0070/hwmon/hwmon*/in4_input", "Address": "dc-i2c-85-70", "format": "int(int('%s', 10)*1.5)"},
    {"Sensor": "MAC_XDPE_QSFP112_VDD3.3V_D_C", "CriticalLow": -5000, "CriticalHigh": 88000, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/85-0070/hwmon/hwmon*/curr4_input", "Address": "dc-i2c-85-70"},
    {"Sensor": "MAC_VDD12V", "CriticalLow": 10800, "CriticalHigh": 13200, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in1_input", "Address": "dc-i2c-79-5b"},
    {"Sensor": "MAC_VDD1.8_CLK", "CriticalLow": 1620, "CriticalHigh": 1980, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in2_input", "Address": "dc-i2c-79-5b"},
    {"Sensor": "MAC_VDD3.3_CLK", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in3_input", "Address": "dc-i2c-79-5b"},
    {"Sensor": "MAC_VDD1.0V_FPGA", "CriticalLow": 900, "CriticalHigh": 1100, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in4_input", "Address": "dc-i2c-79-5b"},
    {"Sensor": "MAC_VDD1.8V_FPGA", "CriticalLow": 1620, "CriticalHigh": 1980, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in5_input", "Address": "dc-i2c-79-5b"},
    {"Sensor": "MAC_VDD1.2V_FPGA", "CriticalLow": 1080, "CriticalHigh": 1320, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in6_input", "Address": "dc-i2c-79-5b"},
    {"Sensor": "MAC_VDD3.3V", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in7_input", "Address": "dc-i2c-79-5b"},
    {"Sensor": "MAC_VDDO1.2V", "CriticalLow": 1080, "CriticalHigh": 1320, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in8_input", "Address": "dc-i2c-79-5b"},
    {"Sensor": "MAC_VDDO1.8V", "CriticalLow": 1620, "CriticalHigh": 1980, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in9_input", "Address": "dc-i2c-79-5b"},
    {"Sensor": "MAC_VDD_CORE", "CriticalLow": 720, "CriticalHigh": 900, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in10_input", "Address": "dc-i2c-79-5b"},
    {"Sensor": "MAC_VDDA1.5V", "CriticalLow": 1350, "CriticalHigh": 1650, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in11_input", "Address": "dc-i2c-79-5b"},
    {"Sensor": "MAC_VDD0_9V_ANLG0", "CriticalLow": 810, "CriticalHigh": 1080, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in12_input", "Address": "dc-i2c-79-5b"},
    {"Sensor": "MAC_VDD0_9V_ANLG1", "CriticalLow": 810, "CriticalHigh": 1080, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in13_input", "Address": "dc-i2c-79-5b"},
    {"Sensor": "MAC_VDD0_75V_ANLG0", "CriticalLow": 675, "CriticalHigh": 900, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in14_input", "Address": "dc-i2c-79-5b"},
    {"Sensor": "MAC_VDD0_75V_ANLG1", "CriticalLow": 675, "CriticalHigh": 900, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in15_input", "Address": "dc-i2c-79-5b"},
    {"Sensor": "MAC_VDD0.8V", "CriticalLow": 720, "CriticalHigh": 880, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in16_input", "Address": "dc-i2c-79-5b"},
    {"Sensor": "MAC_VDD12V", "CriticalLow": 10800, "CriticalHigh": 13200, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in1_input", "Address": "dc-i2c-80-5b"},
    {"Sensor": "MAC_VDD3.3V_standby", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in2_input", "Address": "dc-i2c-80-5b"},
    {"Sensor": "MAC_VDD3V8_CLK", "CriticalLow": 3420, "CriticalHigh": 4180, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in3_input", "Address": "dc-i2c-80-5b"},
    {"Sensor": "MAC_VDD5V_VR", "CriticalLow": 4500, "CriticalHigh": 5500, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in4_input", "Address": "dc-i2c-80-5b"},
    {"Sensor": "MAC_VDD1.5V", "CriticalLow": 1350, "CriticalHigh": 1650, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in5_input", "Address": "dc-i2c-80-5b"},
    {"Sensor": "MAC_VDD1_2V", "CriticalLow": 1080, "CriticalHigh": 1320, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in6_input", "Address": "dc-i2c-80-5b"},
    {"Sensor": "MAC_VDD_PLL0", "CriticalLow": 810, "CriticalHigh": 990, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in7_input", "Address": "dc-i2c-80-5b"},
    {"Sensor": "MAC_VDD_PLL1", "CriticalLow": 810, "CriticalHigh": 990, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in8_input", "Address": "dc-i2c-80-5b"},
    {"Sensor": "MAC_VDD_PLL2", "CriticalLow": 810, "CriticalHigh": 990, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in9_input", "Address": "dc-i2c-80-5b"},
    {"Sensor": "MAC_VDD_PLL3", "CriticalLow": 810, "CriticalHigh": 990, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in10_input", "Address": "dc-i2c-80-5b"},
    {"Sensor": "MAC_QSFP112_VDD3.3V_A", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in11_input", "Address": "dc-i2c-80-5b"},
    {"Sensor": "MAC_QSFP112_VDD3.3V_B", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in12_input", "Address": "dc-i2c-80-5b"},
    {"Sensor": "MAC_QSFP112_VDD3.3V_C", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in13_input", "Address": "dc-i2c-80-5b"},
    {"Sensor": "MAC_QSFP112_VDD3.3V_D", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in14_input", "Address": "dc-i2c-80-5b"},
    {"Sensor": "DPORT_XDPE_QSFP112_VDD3.3V_A_V", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/131-0070/hwmon/hwmon*/in3_input", "Address": "dc-i2c-131-70", "format": "int(int('%s', 10)*1.5)"},
    {"Sensor": "DPORT_XDPE_QSFP112_VDD3.3V_A_C", "CriticalLow": -5000, "CriticalHigh": 88000, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/131-0070/hwmon/hwmon*/curr3_input", "Address": "dc-i2c-131-70"},
    {"Sensor": "DPORT_XDPE_QSFP112_VDD3.3V_B_V", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/131-0070/hwmon/hwmon*/in4_input", "Address": "dc-i2c-131-70", "format": "int(int('%s', 10)*1.5)"},
    {"Sensor": "DPORT_XDPE_QSFP112_VDD3.3V_B_C", "CriticalLow": -5000, "CriticalHigh": 88000, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/131-0070/hwmon/hwmon*/curr4_input", "Address": "dc-i2c-131-70"},
    {"Sensor": "DPORT_VDD12V", "CriticalLow": 10800, "CriticalHigh": 13200, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in1_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "DPORT_VDD3.3V_standby", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in2_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "DPORT_VDD1.0V_FPGA", "CriticalLow": 900, "CriticalHigh": 1100, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in3_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "DPORT_VDD1.8V_FPGA", "CriticalLow": 1620, "CriticalHigh": 1980, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in4_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "DPORT_VDD1.2V_FPGA", "CriticalLow": 1080, "CriticalHigh": 1320, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in5_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "DPORT_VDD3.3V", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in6_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "DPORT_VDD5V_VR", "CriticalLow": 4500, "CriticalHigh": 5500, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in7_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "DPORT_QSFP112_VDD3.3V_A", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in8_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "DPORT_QSFP112_VDD3.3V_B", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in9_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "CPU_P1V05", "CriticalLow": 954, "CriticalHigh": 1160, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in1_input", "Address": "dc-i2c-122-5f"},
    {"Sensor": "CPU_VCCIN", "CriticalLow": 1350, "CriticalHigh": 2200, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in2_input", "Address": "dc-i2c-122-5f"},
    {"Sensor": "CPU_P1V2_VDDQ", "CriticalLow": 1120, "CriticalHigh": 1280, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in3_input", "Address": "dc-i2c-122-5f"},
    {"Sensor": "CPU_P1V8", "CriticalLow": 1690, "CriticalHigh": 1910, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in4_input", "Address": "dc-i2c-122-5f"},
    {"Sensor": "CPU_P0V6_VTT", "CriticalLow": 558, "CriticalHigh": 682, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in5_input", "Address": "dc-i2c-122-5f"},
    {"Sensor": "CPU_VNN_PCH", "CriticalLow": 540, "CriticalHigh": 1320, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in6_input", "Address": "dc-i2c-122-5f"},
    {"Sensor": "CPU_VNN_NAC", "CriticalLow": 540, "CriticalHigh": 1320, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in7_input", "Address": "dc-i2c-122-5f"},
    {"Sensor": "CPU_P2V5_VPP", "CriticalLow": 2250, "CriticalHigh": 2750, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in8_input", "Address": "dc-i2c-122-5f"},
    {"Sensor": "CPU_VCC_ANA", "CriticalLow": 900, "CriticalHigh": 1100, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in9_input", "Address": "dc-i2c-122-5f"},
    {"Sensor": "CPU_P3V3_STBY", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in10_input", "Address": "dc-i2c-122-5f"},
    {"Sensor": "CPU_P5V_AUX", "CriticalLow": 4000, "CriticalHigh": 5750, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in11_input", "Address": "dc-i2c-122-5f"},
    {"Sensor": "CPU_P1V8_AUX_NAC", "CriticalLow": 1690, "CriticalHigh": 1910, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in12_input", "Address": "dc-i2c-122-5f"},
    {"Sensor": "CPU_P3V3_AUX", "CriticalLow": 2970, "CriticalHigh": 3630, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in13_input", "Address": "dc-i2c-122-5f"},
    {"Sensor": "CPU_V1P80_EMMC_OUT", "CriticalLow": 1690, "CriticalHigh": 1910, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in14_input", "Address": "dc-i2c-122-5f"},
    {"Sensor": "CPU_V3P3_EMMC_OUT", "CriticalLow": 3100, "CriticalHigh": 3500, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in15_input", "Address": "dc-i2c-122-5f"},
    {"Sensor": "CPU_XDPE_VCCIN_V", "CriticalLow": 1350, "CriticalHigh": 2200, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-0070/hwmon/hwmon*/in3_input", "Address": "dc-i2c-122-70"},
    {"Sensor": "CPU_XDPE_P1V8_V", "CriticalLow": 1690, "CriticalHigh": 1910, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-0070/hwmon/hwmon*/in4_input", "Address": "dc-i2c-122-70"},
    {"Sensor": "CPU_XDPE_VCCIN_C", "CriticalLow": -3100, "CriticalHigh": 147000, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/122-0070/hwmon/hwmon*/curr3_input", "Address": "dc-i2c-122-70"},
    {"Sensor": "CPU_XDPE_P1V8_C", "CriticalLow": -3100, "CriticalHigh": 2300, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/122-0070/hwmon/hwmon*/curr4_input", "Address": "dc-i2c-122-70"},
    {"Sensor": "CPU_XDPE_P1V05_V", "CriticalLow": 954, "CriticalHigh": 1160, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-006e/hwmon/hwmon*/in3_input", "Address": "dc-i2c-122-6e"},
    {"Sensor": "CPU_XDPE_VNN_PCH_V", "CriticalLow": 540, "CriticalHigh": 1320, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-006e/hwmon/hwmon*/in4_input", "Address": "dc-i2c-122-6e"},
    {"Sensor": "CPU_XDPE_P1V05_C", "CriticalLow": -3100, "CriticalHigh": 14300, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/122-006e/hwmon/hwmon*/curr3_input", "Address": "dc-i2c-122-6e"},
    {"Sensor": "CPU_XDPE_VNN_PCH_C", "CriticalLow": -3100, "CriticalHigh": 7400, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/122-006e/hwmon/hwmon*/curr4_input", "Address": "dc-i2c-122-6e"},
    {"Sensor": "CPU_XDPE_P1V2_VDDQ_V", "CriticalLow": 1120, "CriticalHigh": 1280, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-005e/hwmon/hwmon*/in3_input", "Address": "dc-i2c-122-5e"},
    {"Sensor": "CPU_XDPE_P1V2_VDDQ_C", "CriticalLow": -3100, "CriticalHigh": 19000, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/122-005e/hwmon/hwmon*/curr3_input", "Address": "dc-i2c-122-5e"},
    {"Sensor": "CPU_XDPE_VNN_NAC_V", "CriticalLow": 540, "CriticalHigh": 1320, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-0068/hwmon/hwmon*/in3_input", "Address": "dc-i2c-122-68"},
    {"Sensor": "CPU_XDPE_VCC_ANA_V", "CriticalLow": 900, "CriticalHigh": 1100, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/122-0068/hwmon/hwmon*/in4_input", "Address": "dc-i2c-122-68"},
    {"Sensor": "CPU_XDPE_VNN_NAC_C", "CriticalLow": -3100, "CriticalHigh": 22000, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/122-0068/hwmon/hwmon*/curr3_input", "Address": "dc-i2c-122-68"},
    {"Sensor": "CPU_XDPE_VCC_ANA_C", "CriticalLow": -3100, "CriticalHigh": 2210, "gettype": "sysfs", "Unit": "mA",
        "location": "/sys/bus/i2c/devices/122-0068/hwmon/hwmon*/curr4_input", "Address": "dc-i2c-122-68"},
]


FRUS_STATUS = {
    "psus": [
        {"name": "psu1", "i2c_addr": {"bus": 89, "devno": 0x3d, "reg_offset": 0x64}, "gettype": "i2c", 'presentbit': 2, 'statusbit': 1, 'alertbit': 0},
        {"name": "psu2", "i2c_addr": {"bus": 89, "devno": 0x3d, "reg_offset": 0x64}, "gettype": "i2c", 'presentbit': 6, 'statusbit': 5, 'alertbit': 4},
        {"name": "psu3", "i2c_addr": {"bus": 89, "devno": 0x3d, "reg_offset": 0x65}, "gettype": "i2c", 'presentbit': 2, 'statusbit': 1, 'alertbit': 0},
        {"name": "psu4", "i2c_addr": {"bus": 89, "devno": 0x3d, "reg_offset": 0x65}, "gettype": "i2c", 'presentbit': 6, 'statusbit': 5, 'alertbit': 4},
    ],
    "psupmbus": [
        {"name": "psu1", "values":
            [
                {"location": "/sys/bus/i2c/devices/95-0058/hwmon/*/curr1_input",
                    "displayname": "输入电流", 'name': 'iin', 'unit': 'A', 'min': 0, 'max': 10},
                {"location": "/sys/bus/i2c/devices/95-0058/hwmon/*/in1_input",
                    "displayname": "输入电压", 'name': 'vin', 'unit': 'V', 'min': 180, 'max': 300},
                {"location": "/sys/bus/i2c/devices/95-0058/hwmon/*/in2_input",
                    "displayname": "输出电压", 'name': 'vout1', 'unit': 'V', 'min': 11.4, 'max': 12.6},
                {"location": "/sys/bus/i2c/devices/95-0058/hwmon/*/curr2_input",
                    "displayname": "输出电流", 'name': 'iout1', 'unit': 'A', 'min': 0, 'max': 134.1},
                {"location": "/sys/bus/i2c/devices/95-0058/hwmon/*/temp1_input",
                    "displayname": "电源温度", 'name': 'temp1', 'unit': 'C', 'min': -20, 'max': 65},
                {"location": "/sys/bus/i2c/devices/95-0058/hwmon/*/fan1_input",
                    "displayname": "风扇转速", 'name': 'fan1', 'unit': 'RPM', 'min': 500, 'max': 32000},
                {"location": "/sys/bus/i2c/devices/95-0058/hwmon/*/power1_input",
                 "displayname": "输入功率", 'name': 'pin', 'unit': 'W', 'min': 0, 'max': 2500},
                {"location": "/sys/bus/i2c/devices/95-0058/hwmon/*/power2_input",
                 "displayname": "输出功率", 'name': 'pout1', 'unit': 'W', 'min': 0, 'max': 1600},
            ]
         },
        {"name": "psu2", "values":
            [
                {"location": "/sys/bus/i2c/devices/96-0058/hwmon/*/curr1_input",
                    "displayname": "输入电流", 'name': 'iin', 'unit': 'A', 'min': 0, 'max': 10},
                {"location": "/sys/bus/i2c/devices/96-0058/hwmon/*/in1_input",
                    "displayname": "输入电压", 'name': 'vin', 'unit': 'V', 'min': 180, 'max': 300},
                {"location": "/sys/bus/i2c/devices/96-0058/hwmon/*/in2_input",
                    "displayname": "输出电压", 'name': 'vout1', 'unit': 'V', 'min': 11.4, 'max': 12.6},
                {"location": "/sys/bus/i2c/devices/96-0058/hwmon/*/curr2_input",
                    "displayname": "输出电流", 'name': 'iout1', 'unit': 'A', 'min': 0, 'max': 134.1},
                {"location": "/sys/bus/i2c/devices/96-0058/hwmon/*/temp1_input",
                    "displayname": "电源温度", 'name': 'temp1', 'unit': 'C', 'min': -20, 'max': 65},
                {"location": "/sys/bus/i2c/devices/96-0058/hwmon/*/fan1_input",
                    "displayname": "风扇转速", 'name': 'fan1', 'unit': 'RPM', 'min': 500, 'max': 32000},
                {"location": "/sys/bus/i2c/devices/96-0058/hwmon/*/power1_input",
                    "displayname": "输入功率", 'name': 'pin', 'unit': 'W', 'min': 0, 'max': 2500},
                {"location": "/sys/bus/i2c/devices/96-0058/hwmon/*/power2_input",
                 "displayname": "输出功率", 'name': 'pout1', 'unit': 'W', 'min': 0, 'max': 1600},
            ]
         },
        {"name": "psu3", "values":
            [
                {"location": "/sys/bus/i2c/devices/97-0058/hwmon/*/curr1_input",
                    "displayname": "输入电流", 'name': 'iin', 'unit': 'A', 'min': 0, 'max': 10},
                {"location": "/sys/bus/i2c/devices/97-0058/hwmon/*/in1_input",
                    "displayname": "输入电压", 'name': 'vin', 'unit': 'V', 'min': 180, 'max': 300},
                {"location": "/sys/bus/i2c/devices/97-0058/hwmon/*/in2_input",
                    "displayname": "输出电压", 'name': 'vout1', 'unit': 'V', 'min': 11.4, 'max': 12.6},
                {"location": "/sys/bus/i2c/devices/97-0058/hwmon/*/curr2_input",
                    "displayname": "输出电流", 'name': 'iout1', 'unit': 'A', 'min': 0, 'max': 134.1},
                {"location": "/sys/bus/i2c/devices/97-0058/hwmon/*/temp1_input",
                    "displayname": "电源温度", 'name': 'temp1', 'unit': 'C', 'min': -20, 'max': 65},
                {"location": "/sys/bus/i2c/devices/97-0058/hwmon/*/fan1_input",
                    "displayname": "风扇转速", 'name': 'fan1', 'unit': 'RPM', 'min': 500, 'max': 32000},
                {"location": "/sys/bus/i2c/devices/97-0058/hwmon/*/power1_input",
                    "displayname": "输入功率", 'name': 'pin', 'unit': 'W', 'min': 0, 'max': 2500},
                {"location": "/sys/bus/i2c/devices/97-0058/hwmon/*/power2_input",
                 "displayname": "输出功率", 'name': 'pout1', 'unit': 'W', 'min': 0, 'max': 1600},
            ]
         },
        {"name": "psu4", "values":
            [
                {"location": "/sys/bus/i2c/devices/98-0058/hwmon/*/curr1_input",
                    "displayname": "输入电流", 'name': 'iin', 'unit': 'A', 'min': 0, 'max': 10},
                {"location": "/sys/bus/i2c/devices/98-0058/hwmon/*/in1_input",
                    "displayname": "输入电压", 'name': 'vin', 'unit': 'V', 'min': 180, 'max': 300},
                {"location": "/sys/bus/i2c/devices/98-0058/hwmon/*/in2_input",
                    "displayname": "输出电压", 'name': 'vout1', 'unit': 'V', 'min': 11.4, 'max': 12.6},
                {"location": "/sys/bus/i2c/devices/98-0058/hwmon/*/curr2_input",
                    "displayname": "输出电流", 'name': 'iout1', 'unit': 'A', 'min': 0, 'max': 134.1},
                {"location": "/sys/bus/i2c/devices/98-0058/hwmon/*/temp1_input",
                    "displayname": "电源温度", 'name': 'temp1', 'unit': 'C', 'min': -20, 'max': 65},
                {"location": "/sys/bus/i2c/devices/98-0058/hwmon/*/fan1_input",
                    "displayname": "风扇转速", 'name': 'fan1', 'unit': 'RPM', 'min': 500, 'max': 32000},
                {"location": "/sys/bus/i2c/devices/98-0058/hwmon/*/power1_input",
                    "displayname": "输入功率", 'name': 'pin', 'unit': 'W', 'min': 0, 'max': 2500},
                {"location": "/sys/bus/i2c/devices/98-0058/hwmon/*/power2_input",
                 "displayname": "输出功率", 'name': 'pout1', 'unit': 'W', 'min': 0, 'max': 1600},
            ]
         },
    ]
}

FRUS_STATUS_DECODE = {
    'fanpresent': {0: 'PRESENT', 1: 'ABSENT', 'okval': 0},
    'fanroll': {0: 'STALL', 1: 'ROLL', 'okval': 1},
    'psupresent': {0: 'PRESENT', 1: 'ABSENT', 'okval': 0},
    'psuoutput': {0: 'FAULT', 1: 'NORMAL', 'okval': 1},
    'psualert': {0: 'FAULT', 1: 'NORMAL', 'okval': 1},
}

BIOS_STATUS = {'gettype': 'io', 'io_addr': 0x09C2, 'bitmask': 0x01}
BIOS_STATUS_DECODE = {1: 'master', 0: 'slave'}

MUL_FPGA_VERSION_INFO = [
    {
        "fpga_name": "MAC FPGA版本检测",
        "value": [
            {"name": "version", "pcibus": 6, "slot": 0, "fn": 0, "bar": 0, "offset": 0, "gettype": "pci"},
            {"name": "date", "pcibus": 6, "slot": 0, "fn": 0, "bar": 0, "offset": 4, "gettype": "pci"},
            {"name": "golden version", "pcibus": 6, "slot": 0, "fn": 0, "bar": 0, "offset": 12, "gettype": "pci"},
        ],
    },
    {
        "fpga_name": "UPORT FPGA版本检测",
        "value": [
            {"name": "version", "pcibus": 4, "slot": 0, "fn": 0, "bar": 0, "offset": 0, "gettype": "pci"},
            {"name": "date", "pcibus": 4, "slot": 0, "fn": 0, "bar": 0, "offset": 4, "gettype": "pci"},
            {"name": "golden version", "pcibus": 4, "slot": 0, "fn": 0, "bar": 0, "offset": 12, "gettype": "pci"},
        ],
    },
    {
        "fpga_name": "DPORT FPGA版本检测",
        "value": [
            {"name": "version", "pcibus": 5, "slot": 0, "fn": 0, "bar": 0, "offset": 0, "gettype": "pci"},
            {"name": "date", "pcibus": 5, "slot": 0, "fn": 0, "bar": 0, "offset": 4, "gettype": "pci"},
            {"name": "golden version", "pcibus": 5, "slot": 0, "fn": 0, "bar": 0, "offset": 12, "gettype": "pci"},
        ],
    },
]

# 内存条丝印
MEM_SLOTS = ["J1", "", "J2", ""]

FAN_PROTECT = [
    {"bus": 103, "devno": 0x0d, "addr": 0x20, "open": 0x00, "close": 0x0f},
    {"bus": 111, "devno": 0x0d, "addr": 0x20, "open": 0x00, "close": 0x0f},
]
rg_eeprom = "1-0056/eeprom"
E2_LOC = {"bus": 1, "devno": 0x56}
E2_PROTECT = {"bus": 87, "devno": 0x1d, "addr": 0x25, "open": 0x1f, "close": 0x3f}

CPLDVERSIONS = [
    {"io_addr": 0x0a00, "name": "CPU_CPLD", "gettype": "io"},
    {"io_addr": 0x0900, "name": "BASE_CPLD ", "gettype": "io"},
    {"bus": 87, "devno": 0x1D, "name": "MAC_CPLDA"},
    {"bus": 88, "devno": 0x2D, "name": "MAC_CPLDB"},
    {"bus": 89, "devno": 0x3D, "name": "MAC_CPLDC"},
    {"bus": 62, "devno": 0x3D, "name": "UPORT_CPLD"},
    {"bus": 127, "devno": 0x3D, "name": "DPORT_CPLD"},
    {"bus": 103, "devno": 0x0D, "name": "UFCB_CPLD"},
    {"bus": 111, "devno": 0x0D, "name": "DFCB_CPLD"},
]

BMC_TLV_E2_SYNC = {
    "BMC_access": 1,
    "BMC_E2_LOC": "/sys/bus/i2c/devices/2-0057/eeprom",
    "BMC_E2_PROTECT": {"ep_bus": 82, "ep_loc": 0x1d, "ep_addr": 0x25, "ep_open": 0x00, "ep_close": 0xff},
}

BMC_E2_LOC = {
    "fru": "/sys/bus/i2c/devices/2-0053/eeprom",
    "tlv": "/sys/bus/i2c/devices/2-0057/eeprom",
}

TEMPS_DEFINE = {
    "boards": [
        {"location": "/sys/bus/i2c/devices/65-004b/hwmon/*/temp1_input", "displayname": "UPORT_AIR_INLET", "max": 80, "min": 0},
        {"location": "/sys/bus/i2c/devices/71-004b/hwmon/*/temp1_input", "displayname": "MAC_AIR_INLET_1", "max": 80, "min": 0},
        {"location": "/sys/bus/i2c/devices/72-004f/hwmon/*/temp1_input", "displayname": "MAC_AIR_INLET_2", "max": 80, "min": 0},
        {"location": "/sys/bus/i2c/devices/130-004b/hwmon/*/temp1_input", "displayname": "DPORT_AIR_INLET", "max": 80, "min": 0},
        {"location": "/sys/bus/i2c/devices/104-004b/hwmon/*/temp1_input", "displayname": "UPORT_FAN_AIR_OUTLET", "max": 75, "min": -30},
        {"location": "/sys/bus/i2c/devices/112-004b/hwmon/*/temp1_input", "displayname": "DPORT_FAN_AIR_OUTLET", "max": 75, "min": -30},
        {"location": "/sys/bus/i2c/devices/123-004b/hwmon/*/temp1_input", "displayname": "MGMT_AIR_INLET_1", "max": 55, "min": -30},
        {"location": "/sys/bus/i2c/devices/124-004b/hwmon/*/temp1_input", "displayname": "MGMT_AIR_INLET_2", "max": 55, "min": -30},
    ],
    "cpu": '/sys/bus/platform/devices/coretemp.0/hwmon/hwmon1',
    "cpu_temp_max": 102,
    "cpu_temp_min": -30,
    "mac_temp_cpld": "cat /sys/rg_plat/sensor/temp1/temp_input",
    "mac_temp_max": 105,
    "mac_temp_min": -30,
}

PSU_MODEL_MAP = {
    "GW-CRPS1300D": "PA1300I-F",
    "DPS-1300AB-6 S": "PA1300I-F",
}

OPTOE_PORT_MAP = {
    "port_num": 128,
    "optoe_start_bus": 140,
}

# ECC_CMD = [
#     {"cmd": "dfd_debug phymem_rd 4 0x8ffa2104 16", "keyword": ["0x8ffa2100", "0x8ffa2110"], "check_len": 16},
#     {"cmd": "dfd_debug phymem_rd 4 0x8ffa3104 16", "keyword": ["0x8ffa3100", "0x8ffa3110"], "check_len": 16},
# ]

ECC_CMD = [
    {"cmd": "dfd_debug phymem_rd 4 0xfb923430 8", "keyword": ["0xfb923430"], "check_len": 8},
]

FACTESTMODULE = {
    "bmc_diag": 0,
    "mgmttest": 1,
    "bmcsetmac": 0,
    "sysinfo_showhw": 1,  # 默认为1
    "sensord": 1,
    "fancontrol_stop": 0,
    "firmware_check": 1,
    "mul_fpga_show": 1,
    "bmcinit": 1,
    "show_device_mac": 1,
    #"show_config_ver": 1,
    "eeprom_pn_sn_show": 1,
}

I2C_SCAN_LIST = [
    #{"addr": 0x56, "name": "CPU扣板EEPROM（U29）", "bus": 0},
    {"addr": 0x56, "name": "MAC板整机EEPROM1（U148）", "bus": 1},
    {"addr": 0x57, "name": "MAC板整机EEPROM2（U149）", "bus": 1},
    {"addr": 0x3C, "name": "MAC板CPLDC（U146）", "bus": 132},
    {"addr": 0x1C, "name": "MAC板CPLDA（U15）", "bus": 133},
    {"addr": 0x2C, "name": "MAC板CPLDB（U109）", "bus": 134},
    {"addr": 0x36, "name": "MAC板FPGA（U95）", "bus": 135},
    {"addr": 0x3C, "name": "上端口板CPLD（U8）", "bus": 136},
    {"addr": 0x36, "name": "上端口板FPGA（U5）", "bus": 137},
    {"addr": 0x3C, "name": "下端口板CPLD（U8）", "bus": 138},
    {"addr": 0x36, "name": "下端口板FPGA（U5）", "bus": 139},
    {"addr": 0x3D, "name": "上端口板CPLD（U8）", "bus": 62},
    {"addr": 0x57, "name": "上端口板EEPROM（U10）", "bus": 63},
    {"addr": 0x5B, "name": "上端口板UCD90160（U23）", "bus": 64},
    {"addr": 0x4B, "name": "上端口板CT75（U11）", "bus": 65},
    {"addr": 0x70, "name": "上端口板XDPE12284C（U26）", "bus": 66},
    {"addr": 0x50, "name": "PSU1(FRU EEPROM)", "bus": 95},
    {"addr": 0x58, "name": "PSU1(PMBUS)", "bus": 95},
    {"addr": 0x50, "name": "PSU2(FRU EEPROM)", "bus": 96},
    {"addr": 0x58, "name": "PSU2(PMBUS)", "bus": 96},
    {"addr": 0x50, "name": "PSU3(FRU EEPROM)", "bus": 97},
    {"addr": 0x58, "name": "PSU3(PMBUS)", "bus": 97},
    {"addr": 0x50, "name": "PSU4(FRU EEPROM)", "bus": 98},
    {"addr": 0x58, "name": "PSU4(PMBUS)", "bus": 98},
    {"addr": 0x0D, "name": "FAN板CPLD（U13）", "bus": 103},
    {"addr": 0x4B, "name": "FAN板CT75_0（U21）", "bus": 104},
    {"addr": 0x50, "name": "FAN板FAN_0（fan1）", "bus": 105},
    {"addr": 0x50, "name": "FAN板FAN_1（fan3）", "bus": 106},
    {"addr": 0x50, "name": "FAN板FAN_2（fan5）", "bus": 107},
    {"addr": 0x50, "name": "FAN板FAN_3（fan7）", "bus": 108},
    {"addr": 0x0D, "name": "FAN板CPLD（U13）", "bus": 111},
    {"addr": 0x4B, "name": "FAN板CT75_0（U21）", "bus": 112},
    {"addr": 0x50, "name": "FAN板FAN_0（fan2）", "bus": 113},
    {"addr": 0x50, "name": "FAN板FAN_1（fan4）", "bus": 114},
    {"addr": 0x50, "name": "FAN板FAN_2（fan6）", "bus": 115},
    {"addr": 0x50, "name": "FAN板FAN_3（fan8）", "bus": 116},
    {"addr": 0x57, "name": "MGMT板EEPROM（U22）", "bus": 119},
    {"addr": 0x3D, "name": "MGMT板CPLD（U13）", "bus": 120},
    {"addr": 0x5B, "name": "MGMT板UCD90160（U37）", "bus": 121},
    {"addr": 0X5F, "name": "CPU扣板UCD90160（U15）", "bus": 122},
    #{"addr": 0X09, "name": "CPU扣板RC32504（U28）", "bus": 122},
    {"addr": 0X70, "name": "CPU扣板VR电源1（U1）", "bus": 122},
    {"addr": 0X6E, "name": "CPU扣板VR电源2（U17）", "bus": 122},
    {"addr": 0X5E, "name": "CPU扣板VR电源3（U20）", "bus": 122},
    {"addr": 0X68, "name": "CPU扣板VR电源4（U23）", "bus": 122},
    {"addr": 0x4B, "name": "MGMT板CT75_0（U23）", "bus": 123},
    {"addr": 0x4B, "name": "MGMT板CT75_1（U24）", "bus": 124},
    {"addr": 0x4B, "name": "MAC板CT75_0（U103）", "bus": 71},
    {"addr": 0x4F, "name": "MAC板CT75_1（U104）", "bus": 72},
    {"addr": 0x4C, "name": "MAC板TMP411ADGKT_0（U101）", "bus": 73},
    {"addr": 0x4C, "name": "MAC板TMP411ADGKT_1（U102）", "bus": 74},
    {"addr": 0x44, "name": "MAC芯片（U92）", "bus": 75},
    {"addr": 0x5B, "name": "MAC板UCD90160（U48）", "bus": 79},
    {"addr": 0x5B, "name": "MAC板UCD90160B（U48）", "bus": 80},
    {"addr": 0x40, "name": "XDPE132G5D_28+0", "bus": 81},
    #{"addr": 0x28, "name": "XDPE132G5D_28+0", "bus": 81},
    {"addr": 0x4D, "name": "XDPE132G5D_3+2", "bus": 82},
    #{"addr": 0x35, "name": "XDPE132G5D_3+2", "bus": 82},
    {"addr": 0x4D, "name": "XDPE132G5D_3+2", "bus": 83},
    #{"addr": 0x35, "name": "XDPE132G5D_3+2", "bus": 83},
    {"addr": 0x70, "name": "XDPE12284C_3+3", "bus": 84},
    {"addr": 0x70, "name": "XDPE12284C_3+3", "bus": 85},
    {"addr": 0x1D, "name": "MAC板CPLDA（U15）", "bus": 87},
    {"addr": 0x2D, "name": "MAC板CPLDB（U109）", "bus": 88},
    {"addr": 0x3D, "name": "MAC板CPLDC（U146）", "bus": 89},
    {"addr": 0x57, "name": "MAC板EEPROM（U100）", "bus": 91},
    #{"addr": 0x58, "name": "MAC板RC32312 EEPROM（U118）", "bus": 92},
    {"addr": 0x3D, "name": "下端口板CPLD（U8）", "bus": 127},
    {"addr": 0x57, "name": "下端口板EEPROM（U10）", "bus": 128},
    {"addr": 0x5B, "name": "下端口板UCD90160（U23）", "bus": 129},
    {"addr": 0x4B, "name": "下端口板CT75（U11）", "bus": 130},
    {"addr": 0x70, "name": "下端口板XDPE12284C（U26）", "bus": 131},
]

LED_NEW = {
    "fanleds": {
        "attrs": OrderedDict([("灭", 0x00), ("红灯亮", 0x02), ("绿灯亮", 0x04), ]),
        "name": "风扇1/2/3/4/5/6/7/8灯",
        "device": [
            {"bus": 103, "addr": 0x0d, "reg": 0xd0},
            {"bus": 111, "addr": 0x0d, "reg": 0xd0},
            {"bus": 103, "addr": 0x0d, "reg": 0xd1},
            {"bus": 111, "addr": 0x0d, "reg": 0xd1},
            {"bus": 103, "addr": 0x0d, "reg": 0xd2},
            {"bus": 111, "addr": 0x0d, "reg": 0xd2},
            {"bus": 103, "addr": 0x0d, "reg": 0xd3},
            {"bus": 111, "addr": 0x0d, "reg": 0xd3},
        ]
    },
    "sysleds": {
        "attrs": OrderedDict([("灭", 0x00), ("黄灯亮", 0x06), ("红灯亮", 0x02), ("绿灯亮", 0x04), ]),
        "name": "系统LED测试(SYS,BMC,PSU,FAN)",
        "device": [
            {"bus": 120, "addr": 0x3d, "reg": 0xd2},
            {"bus": 120, "addr": 0x3d, "reg": 0xd5},
            {"bus": 120, "addr": 0x3d, "reg": 0xd3},
            {"bus": 120, "addr": 0x3d, "reg": 0xd4},
        ]
    },
    "uidleds":{ 
        "attrs":OrderedDict([("蓝灯亮",0x03), ("灭",0x02),]),
        "name":"UID灯测试",
        "device":[
            {"bus":120,"addr":0x3d,"reg":0xd0},
        ]
    },
    "portleds": {
        "attrs": OrderedDict([("灭", 0x3f), ("绿灯亮", 0x24), ("红灯亮", 0x12), ("恢复", 0x00), ]),
        "name": "端口灯测试",
        "device": [
            {"bus": 87, "addr": 0x1d, "reg": 0xd0},
            {"bus": 87, "addr": 0x1d, "reg": 0xd1},
            {"bus": 87, "addr": 0x1d, "reg": 0xd2},
            {"bus": 87, "addr": 0x1d, "reg": 0xd3},
            {"bus": 87, "addr": 0x1d, "reg": 0xd4},
            {"bus": 87, "addr": 0x1d, "reg": 0xe0},
            {"bus": 87, "addr": 0x1d, "reg": 0xe1},
            {"bus": 87, "addr": 0x1d, "reg": 0xe2},
            {"bus": 87, "addr": 0x1d, "reg": 0xe3},
            {"bus": 87, "addr": 0x1d, "reg": 0xe4},
            {"bus": 88, "addr": 0x2d, "reg": 0xd0},
            {"bus": 88, "addr": 0x2d, "reg": 0xd1},
            {"bus": 88, "addr": 0x2d, "reg": 0xd2},
            {"bus": 88, "addr": 0x2d, "reg": 0xd3},
            {"bus": 88, "addr": 0x2d, "reg": 0xd4},
            {"bus": 88, "addr": 0x2d, "reg": 0xd5},
            {"bus": 88, "addr": 0x2d, "reg": 0xd6},
            {"bus": 88, "addr": 0x2d, "reg": 0xd7},
            {"bus": 88, "addr": 0x2d, "reg": 0xd8},
            {"bus": 88, "addr": 0x2d, "reg": 0xd9},
            {"bus": 88, "addr": 0x2d, "reg": 0xda},
            {"bus": 88, "addr": 0x2d, "reg": 0xe0},
            {"bus": 88, "addr": 0x2d, "reg": 0xe1},
            {"bus": 88, "addr": 0x2d, "reg": 0xe2},
            {"bus": 88, "addr": 0x2d, "reg": 0xe3},
            {"bus": 88, "addr": 0x2d, "reg": 0xe4},
            {"bus": 88, "addr": 0x2d, "reg": 0xe5},
            {"bus": 88, "addr": 0x2d, "reg": 0xe6},
            {"bus": 88, "addr": 0x2d, "reg": 0xe7},
            {"bus": 88, "addr": 0x2d, "reg": 0xe8},
            {"bus": 88, "addr": 0x2d, "reg": 0xe9},
            {"bus": 88, "addr": 0x2d, "reg": 0xea},
            {"bus": 62, "addr": 0x3d, "reg": 0xd0, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 62, "addr": 0x3d, "reg": 0xd1, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 62, "addr": 0x3d, "reg": 0xd2, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 62, "addr": 0x3d, "reg": 0xd3, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 62, "addr": 0x3d, "reg": 0xd4, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 62, "addr": 0x3d, "reg": 0xd5, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 62, "addr": 0x3d, "reg": 0xd6, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 62, "addr": 0x3d, "reg": 0xd7, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 62, "addr": 0x3d, "reg": 0xd8, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 62, "addr": 0x3d, "reg": 0xd9, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 62, "addr": 0x3d, "reg": 0xda, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 62, "addr": 0x3d, "reg": 0xdb, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 62, "addr": 0x3d, "reg": 0xdc, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 62, "addr": 0x3d, "reg": 0xdd, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 62, "addr": 0x3d, "reg": 0xde, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 62, "addr": 0x3d, "reg": 0xdf, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 127, "addr": 0x3d, "reg": 0xd0, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 127, "addr": 0x3d, "reg": 0xd1, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 127, "addr": 0x3d, "reg": 0xd2, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 127, "addr": 0x3d, "reg": 0xd3, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 127, "addr": 0x3d, "reg": 0xd4, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 127, "addr": 0x3d, "reg": 0xd5, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 127, "addr": 0x3d, "reg": 0xd6, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 127, "addr": 0x3d, "reg": 0xd7, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 127, "addr": 0x3d, "reg": 0xd8, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 127, "addr": 0x3d, "reg": 0xd9, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 127, "addr": 0x3d, "reg": 0xda, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 127, "addr": 0x3d, "reg": 0xdb, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 127, "addr": 0x3d, "reg": 0xdc, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 127, "addr": 0x3d, "reg": 0xdd, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 127, "addr": 0x3d, "reg": 0xde, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
            {"bus": 127, "addr": 0x3d, "reg": 0xdf, "attrs": OrderedDict([("灭", 0x77), ("绿灯亮", 0x44), ("红灯亮", 0x22), ("恢复", 0x00), ]),},
        ]
    },
}

FAN_LOWRATIO = 20
FAN_MIDRATIO = 50
FAN_HIGHRATIO = 100

FAN_THRESHOLD = {
    FAN_LOWRATIO: {"motor0": {"low": 1950, "high": 2850}, "motor1": {"low": 1650, "high": 2550}},
    FAN_MIDRATIO: {"motor0": {"low": 5400, "high": 6600}, "motor1": {"low": 4680, "high": 5720}},
    FAN_HIGHRATIO: {"motor0": {"low": 11070, "high": 13530}, "motor1": {"low": 9630, "high": 11770}}
}

FANS_THRESHOLD = {
    "fan1": FAN_THRESHOLD,
    "fan2": FAN_THRESHOLD,
    "fan3": FAN_THRESHOLD,
    "fan4": FAN_THRESHOLD,
    "fan5": FAN_THRESHOLD,
    "fan6": FAN_THRESHOLD,
    "fan7": FAN_THRESHOLD,
    "fan8": FAN_THRESHOLD,
}

MFT_PORTCONFIG = {
    "hsdk_device": 1,  # 是否是Hsdk设备(是 : 1, 不是 : 0)
    "mgmt_kt_ports": {"eth1":76, "eth2":164, "eth3":274, "eth4":186},  # 内部管理口对应的unit_port
    # 面板口unit_port范围(不包含mgmt口和loopback口)
    "prbs_port_range": "1-75,77-163,165-185,187-273,275-347",
    "extphy_device": 0,  # 是否是有外部phy的设备(是 : 1, 不是 : 0)
    "prbs_ber": 1.0e-7,  # prbs测试允许的误码率
    "prbs_time": 120,  # prbs测试时间 (通常为120s/180s)
    "prbs_ber_dict": {
        1: "1.00E-07",
        2: "1.00E-07",
        3: "1.00E-07",
        4: "1.00E-07",
        5: "1.00E-07",
        6: "1.00E-07",
        7: "1.00E-07",
        8: "1.00E-07",
        9: "1.00E-07",
        10: "1.00E-07",
        11: "1.00E-07",
        12: "1.00E-07",
        13: "1.00E-07",
        14: "1.00E-07",
        15: "1.00E-07",
        16: "1.00E-07",
        17: "1.00E-07",
        18: "1.00E-07",
        19: "1.00E-07",
        20: "1.00E-07",
        21: "1.00E-07",
        22: "1.00E-07",
        23: "1.00E-07",
        24: "1.00E-07",
        25: "1.00E-07",
        26: "1.00E-07",
        27: "1.00E-07",
        28: "1.00E-07",
        29: "1.00E-07",
        30: "1.00E-07",
        31: "1.00E-07",
        32: "1.00E-07",
        33: "1.00E-07",
        34: "1.00E-07",
        35: "1.00E-07",
        36: "1.00E-07",
        37: "1.00E-07",
        38: "1.00E-07",
        39: "1.00E-07",
        40: "1.00E-07",
        41: "1.00E-07",
        42: "1.00E-07",
        43: "1.00E-07",
        44: "1.00E-07",
        45: "1.00E-07",
        46: "1.00E-07",
        47: "1.00E-07",
        48: "1.00E-07",
        49: "1.00E-07",
        50: "1.00E-07",
        51: "1.00E-07",
        52: "1.00E-07",
        53: "1.00E-07",
        54: "1.00E-07",
        55: "1.00E-07",
        56: "1.00E-07",
        57: "1.00E-07",
        58: "1.00E-07",
        59: "1.00E-07",
        60: "1.00E-07",
        61: "1.00E-07",
        62: "1.00E-07",
        63: "1.00E-07",
        64: "1.00E-07",
        65: "1.00E-07",
        66: "1.00E-07",
        67: "1.00E-07",
        68: "1.00E-07",
        69: "1.00E-07",
        70: "1.00E-07",
        71: "1.00E-07",
        72: "1.00E-07",
        73: "1.00E-07",
        74: "1.00E-07",
        75: "1.00E-07",
        76: "1.00E-07",
        77: "1.00E-07",
        78: "1.00E-07",
        79: "1.00E-07",
        80: "1.00E-07",
        81: "1.00E-07",
        82: "1.00E-07",
        83: "1.00E-07",
        84: "1.00E-07",
        85: "1.00E-07",
        86: "1.00E-07",
        87: "1.00E-07",
        88: "1.00E-07",
        89: "1.00E-07",
        90: "1.00E-07",
        91: "1.00E-07",
        92: "1.00E-07",
        93: "1.00E-07",
        94: "1.00E-07",
        95: "1.00E-07",
        96: "1.00E-07",
        97: "1.00E-07",
        98: "1.00E-07",
        99: "1.00E-07",
        100: "1.00E-07",
        101: "1.00E-07",
        102: "1.00E-07",
        103: "1.00E-07",
        104: "1.00E-07",
        105: "1.00E-07",
        106: "1.00E-07",
        107: "1.00E-07",
        108: "1.00E-07",
        109: "1.00E-07",
        110: "1.00E-07",
        111: "1.00E-07",
        112: "1.00E-07",
        113: "1.00E-07",
        114: "1.00E-07",
        115: "1.00E-07",
        116: "1.00E-07",
        117: "1.00E-07",
        118: "1.00E-07",
        119: "1.00E-07",
        120: "1.00E-07",
        121: "1.00E-07",
        122: "1.00E-07",
        123: "1.00E-07",
        124: "1.00E-07",
        125: "1.00E-07",
        126: "1.00E-07",
        127: "1.00E-07",
        128: "1.00E-07",
    },  # 设备单个端口对应的误码率
    "port_frame_test_retrynum": 1,  # 端口收发帧重试次数(内部重试)
    "port_brcst_test_retrynum": 1,  # 端口广播测试重试次数(内部重试)
    "port_prbs_test_retrynum": 1,  # 端口PRBS测试重试次数(内部重试)
    "port_kr_test_retrynum": 1,  # 内部管理口测试重试次数(内部重试)
    "port_frame_del_time": 10,  # 端口收发帧恢复测试环境等待时间(s)
    "port_brcst_del_time": 10,  # 端口广播测试恢复测试环境等待时间(s)
    "port_prbs_del_time": 10,  # 端口PRBS测试恢复测试环境等待时间(s)
    "port_kr_del_time": 10,  # 内部管理口测试恢复测试环境等待时间(s)
    "port_log_level": 1,  # PORT组件log级别(DEBUG : 1, INFO : 2, WARNING : 3, ERROR : 4)
}

PCIe_DEV_LIST = [
    {"pci_addr": "00:00.0", "dev_id": "8086:09a2"},
    {"pci_addr": "00:00.1", "dev_id": "8086:09a4"},
    {"pci_addr": "00:00.2", "dev_id": "8086:09a3"},
    {"pci_addr": "00:00.3", "dev_id": "8086:09a5"},
    {"pci_addr": "00:00.4", "dev_id": "8086:0998"},
    {"pci_addr": "00:01.0", "dev_id": "8086:0b00"},
    {"pci_addr": "00:01.1", "dev_id": "8086:0b00"},
    {"pci_addr": "00:01.2", "dev_id": "8086:0b00"},
    {"pci_addr": "00:01.3", "dev_id": "8086:0b00"},
    {"pci_addr": "00:01.4", "dev_id": "8086:0b00"},
    {"pci_addr": "00:01.5", "dev_id": "8086:0b00"},
    {"pci_addr": "00:01.6", "dev_id": "8086:0b00"},
    {"pci_addr": "00:01.7", "dev_id": "8086:0b00"},
    {"pci_addr": "00:02.0", "dev_id": "8086:09a6"},
    {"pci_addr": "00:02.1", "dev_id": "8086:09a7"},
    {"pci_addr": "00:02.4", "dev_id": "8086:3456"},
    {"pci_addr": "00:06.0", "dev_id": "8086:18da"},
    {"pci_addr": "00:09.0", "dev_id": "8086:18a4"},
    {"pci_addr": "00:0b.0", "dev_id": "8086:18a6"},
    {"pci_addr": "00:0e.0", "dev_id": "8086:18f2"},
    {"pci_addr": "00:0f.0", "dev_id": "8086:18ac"},
    {"pci_addr": "00:10.0", "dev_id": "8086:18a8"},
    {"pci_addr": "00:11.0", "dev_id": "8086:18a9"},
    {"pci_addr": "00:12.0", "dev_id": "8086:18aa"},
    {"pci_addr": "00:13.0", "dev_id": "8086:18ab"},
    {"pci_addr": "00:14.0", "dev_id": "8086:18ad"},
    {"pci_addr": "00:15.0", "dev_id": "8086:18ae"},
    {"pci_addr": "00:18.0", "dev_id": "8086:18d3"},
    {"pci_addr": "00:18.1", "dev_id": "8086:18d4"},
    {"pci_addr": "00:18.4", "dev_id": "8086:18d6"},
    {"pci_addr": "00:1a.0", "dev_id": "8086:18d8"},
    {"pci_addr": "00:1a.1", "dev_id": "8086:18d8"},
    {"pci_addr": "00:1a.2", "dev_id": "8086:18d8"},
    {"pci_addr": "00:1a.3", "dev_id": "8086:18d9"},
    {"pci_addr": "00:1c.0", "dev_id": "8086:18db"},
    {"pci_addr": "00:1d.0", "dev_id": "8086:0998"},
    {"pci_addr": "00:1e.0", "dev_id": "8086:18d0"},
    {"pci_addr": "00:1f.0", "dev_id": "8086:18dc"},
    {"pci_addr": "00:1f.4", "dev_id": "8086:18df"},
    {"pci_addr": "00:1f.5", "dev_id": "8086:18e0"},
    {"pci_addr": "00:1f.7", "dev_id": "8086:18e1"},
    {"pci_addr": "01:00.0", "dev_id": "8086:18ee"},
    {"pci_addr": "04:00.0", "dev_id": "10ee:7011"},
    {"pci_addr": "05:00.0", "dev_id": "10ee:7011"},
    {"pci_addr": "06:00.0", "dev_id": "10ee:7011"},
    {"pci_addr": "08:00.0", "dev_id": "8086:1533"},
    {"pci_addr": "14:00.0", "dev_id": "8086:09a2"},
    {"pci_addr": "14:00.1", "dev_id": "8086:09a4"},
    {"pci_addr": "14:00.2", "dev_id": "8086:09a3"},
    {"pci_addr": "14:00.3", "dev_id": "8086:09a5"},
    {"pci_addr": "14:00.4", "dev_id": "8086:0998"},
    {"pci_addr": "14:02.0", "dev_id": "8086:347a"},
    {"pci_addr": "15:00.0", "dev_id": "14e4:f900"},
    {"pci_addr": "f3:00.0", "dev_id": "8086:09a2"},
    {"pci_addr": "f3:00.1", "dev_id": "8086:09a4"},
    {"pci_addr": "f3:00.2", "dev_id": "8086:09a3"},
    {"pci_addr": "f3:00.3", "dev_id": "8086:09a5"},
    {"pci_addr": "f3:00.4", "dev_id": "8086:0998"},
    {"pci_addr": "f3:04.0", "dev_id": "8086:18d1"},
    {"pci_addr": "f4:00.0", "dev_id": "8086:124c"},
    {"pci_addr": "f4:00.1", "dev_id": "8086:124c"},
    {"pci_addr": "f4:00.2", "dev_id": "8086:124c"},
    {"pci_addr": "f4:00.3", "dev_id": "8086:124c"},
    {"pci_addr": "f4:00.4", "dev_id": "8086:124c"},
    {"pci_addr": "fe:00.0", "dev_id": "8086:3450"},
    {"pci_addr": "fe:00.1", "dev_id": "8086:3451"},
    {"pci_addr": "fe:00.2", "dev_id": "8086:3452"},
    {"pci_addr": "fe:00.3", "dev_id": "8086:0998"},
    {"pci_addr": "fe:00.5", "dev_id": "8086:3455"},
    {"pci_addr": "fe:0b.0", "dev_id": "8086:3448"},
    {"pci_addr": "fe:0b.1", "dev_id": "8086:3448"},
    {"pci_addr": "fe:0b.2", "dev_id": "8086:344b"},
    {"pci_addr": "fe:0c.0", "dev_id": "8086:344a"},
    {"pci_addr": "fe:1a.0", "dev_id": "8086:2880"},
    {"pci_addr": "ff:00.0", "dev_id": "8086:344c"},
    {"pci_addr": "ff:00.1", "dev_id": "8086:344c"},
    {"pci_addr": "ff:00.2", "dev_id": "8086:344c"},
    {"pci_addr": "ff:00.3", "dev_id": "8086:344c"},
    {"pci_addr": "ff:00.4", "dev_id": "8086:344c"},
    {"pci_addr": "ff:00.5", "dev_id": "8086:344c"},
    {"pci_addr": "ff:0a.0", "dev_id": "8086:344d"},
    {"pci_addr": "ff:0a.1", "dev_id": "8086:344d"},
    {"pci_addr": "ff:0a.2", "dev_id": "8086:344d"},
    {"pci_addr": "ff:0a.3", "dev_id": "8086:344d"},
    {"pci_addr": "ff:0a.4", "dev_id": "8086:344d"},
    {"pci_addr": "ff:0a.5", "dev_id": "8086:344d"},
    {"pci_addr": "ff:1d.0", "dev_id": "8086:344f"},
    {"pci_addr": "ff:1d.1", "dev_id": "8086:3457"},
    {"pci_addr": "ff:1e.0", "dev_id": "8086:3458"},
    {"pci_addr": "ff:1e.1", "dev_id": "8086:3459"},
    {"pci_addr": "ff:1e.2", "dev_id": "8086:345a"},
    {"pci_addr": "ff:1e.3", "dev_id": "8086:345b"},
    {"pci_addr": "ff:1e.4", "dev_id": "8086:345c"},
    {"pci_addr": "ff:1e.5", "dev_id": "8086:345d"},
    {"pci_addr": "ff:1e.6", "dev_id": "8086:345e"},
    {"pci_addr": "ff:1e.7", "dev_id": "8086:345f"},
]

PCIe_SPEED_ITEM = [
    {"dev_desc": "I210", "PCIe_name": "I210", "check": {"speed": "2.5gt/s", "width" : "x1"}},
    {"dev_desc": "MAC", "PCIe_name": "Broadcom", "check": {"speed": "8gt/s", "width" : "x4"}},
    {"dev_desc": "MAC_FPGA", "PCIe_name": "06:00.0", "check": {"speed": "5gt/s", "width" : "x1"}},
    {"dev_desc": "UPORT_FPGA", "PCIe_name": "04:00.0", "check": {"speed": "5gt/s", "width" : "x1"}},
    {"dev_desc": "DPORT_FPGA", "PCIe_name": "05:00.0", "check": {"speed": "5gt/s", "width" : "x1"}},
]

# 测试项菜单
MENU_ID_ROOT = 0
MENU_ID_SIGNLE_TEST = 1
MENU_ID_DEVICE_REST = 6
MENU_ID_CPU_TEST = 11
MENU_ID_SYSINFO_TEST = 111
MENU_ID_SSDINFO_TEST = 112
MENU_ID_BMC_TEST = 12
MENU_ID_EMMC_TEST = 121
MENU_ID_EEPROM_TEST = 13
MENU_ID_TEMP_TEST = 14
MENU_ID_LED = 15
MENU_ID_FAN_TEST = 16
MENU_ID_FAN_SPEED_TEST = 161
MENU_ID_PSU_TEST = 17
MENU_ID_STRESS_TEST = 18
MENU_ID_DDR_TEST = 181
MENU_ID_DDR_CPU_TEST = 1811
MENU_ID_DDR_BMC_TEST = 1812
MENU_ID_SSD_TEST = 182
MENU_ID_I2C_STRESS_TEST = 183
MENU_ID_CPU_STRESS_TEST = 185
MENU_ID_BMC_EMMC_STRESS = 189
MENU_ID_TEMP_TEST = 19
MENU_ID_CONFIG = 7
MENU_ID_SETMAC = 71
MENU_ID_FIRMWARE = 72
MENU_ID_BGFUN_TEST = 8
MENU_ID_LSSIGNAL_TEST = 1119

STARTMENUID = MENU_ID_ROOT

#### Single test####
################### CPU test items###############
test_cpu_item = {"name": "CPU test items", "deal": "startMenu", "childid": MENU_ID_CPU_TEST}
test_sys_item = {"name": "Product information test", "deal": "test_sysinfo"}
test_sys_part_item = {"name": "SDK version test", "deal": "test_sysinfo_part"}
test_rtc_item = {"name": "RTC test", "deal": "test_rtc"}
test_rtc_date_item = {"name": "RTC DATE test", "deal": "rtc_date_test"}
test_i2c_item = {"name": "I2C test", "deal": "test_i2c_new"}
test_cpld_item = {"name": "CPLD test", "deal": "test_cpld_new"}
test_fpga_item = {"name": "FPGA test", "deal": "test_fpga_new"}
test_pcie_scan_item = {"name": "PCIe device scan test", "deal": "pci_scan"}
test_cpu_gpio_item = {"name": "CPU CPLD upgrade test", "deal": "test_cpld_gpio"}
test_cpu_fpga_upgrade_item = {"name": "CPU FPGA upgrade test", "deal": "test_mul_fpga"}
test_lpc_item = {"name": "LPC test", "deal": "test_lpc"}
test_dcdc_item = {"name": "DC/DC test", "deal": "test_dcdc"}
test_portframe_item = {"name": "port test", "deal": "test_portframe"}
test_usb_item = {"name": "USB test", "deal": "test_usb"}
test_prbs_item = {"name": "PRBS test", "deal": "test_prbs"}
test_portbroadcast_item = {"name": "port broadcast ", "deal": "test_portbroadcast"}
test_kr_item = {"name": "KR test", "deal": "test_kr", 'before': 'test_kr_pre', 'after': 'test_kr_after'}
test_op_module_status_item = {"name": "Optical module presence detection", "deal": "test_opt_module_present"}
test_sff_present_status_item = {"name": "SFF present and status check", "deal": "test_sff_present_status"}
test_op_module_eeprom_read_item = {
    "name": "Optical module EEPROM information reading",
    "deal": "test_opt_module_e2_read"}
test_bios_flash_item = {"name": "BIOS flash test", "deal": "test_bios_flash"}
test_cpu_gpio_mdio_item = {
    "name": "CPU MDIO test",
    "deal": "test_cpu_gpio_mdio",
    'before': 'test_modprobe_cpu_gpio_mdio',
    'after': 'test_rmmod_cpu_gpio_mdio'}


################### BMC test items###############
test_bmc_item = {
    "name": "BMC test items",
    'before': 'test_bmc_channel',
    "deal": "startMenu",
    "childid": MENU_ID_BMC_TEST}

test_bmc_cpu_info_item = {
    "name": "BMC CPU information display",
    "deal": "test_bmc_testcase",
    "param": "bmc_get_cpu_info"}
test_bmc_ddr_info_item = {
    "name": "BMC DDR information display",
    "deal": "test_bmc_testcase",
    "param": "bmc_get_ddr_info"}
test_bmc_gpio_item = {"name": "BMC CPLD upgrade test", "deal": "test_bmc_testcase", "param": "bmc_test_cpu_gpio"}
test_bmc_peci_item = {"name": "BMC PECI test", "deal": "test_bmc_testcase", "param": "bmc_test_peci"}
test_bmc_sensor_item = {"name": "BMC sensor test", "deal": "test_bmc_testcase", "param": "bmc_get_sensor_info"}
test_bmc_i2c_scan_item = {
    "name": "BMC I2C test",
    "deal": "test_bmc_testcase",
    "param": "bmc_test_i2c_scan",
    "before": "test_stop_fanctrol",
    "after": "test_start_fanctrol"}
test_bmc_cpld_item = {
    "name": "BMC CPLD test",
    "deal": "test_bmc_testcase",
    "param": "bmc_cpld_check",
    "before": "test_stop_fanctrol",
    "after": "test_start_fanctrol"}
test_bmc_sol_item = {"name": "BMC monitoring CPU serial port test", "deal": "test_bmc_sol"}
test_bmc_emmc_info_item = {
    "name": "BMC eMMC information display",
    "deal": "test_bmc_testcase",
    "param": "bmc_get_emmc_info"}
test_bmc_version_item = {"name": "BMC version display", "deal": "test_bmc_testcase", "param": "bmc_get_version"}
test_bmc_mdio_item = {"name": "BMC MDIO test", "deal": "test_bmc_testcase", "param": "bmc_test_MDIO"}
test_bmc_force_switch_slave_item = {"name": "Switch slave BMC image test", "deal": "test_bmc_image_force_switch_slave"}
test_bmc_force_switch_master_item = {
    "name": "Switch master BMC image test",
    "deal": "test_bmc_image_force_switch_master"}
test_bmc_5387md5_item = {
    "name": "5387-eeprom-MD5SUM",
    "deal": "test_bmc_command",
    "param": {
        'cmd': 'md5sum /sys/bus/spi/devices/spi0.0/eeprom',
        'bmc_interface': 'bmc_log_os_system'}}
test_bmc_frueeprom_md5_item = {
    "name": "bmcfru-eeprom-MD5SUM",
    "deal": "test_bmc_command",
    "param": {
        'cmd': 'md5sum /sys/bus/i2c/devices/2-0053/eeprom',
        'bmc_interface': 'bmc_log_os_system'}}
test_bmc_mgmt_item = {"name": "BMC MGMT test", "deal": "test_tbd"}

################### eeprom###############
test_eeproms_item = {"name": "EEPROM information reading", "deal": "startMenu", "childid": MENU_ID_EEPROM_TEST}
test_tlv_eeprom_item = {"name": "TLV-EEPROM test", "deal": "test_tlv_eeprom"}
test_fan_eeprom_item = {"name": "FAN EEPROM test", "deal": "test_fan_eeprom"}
test_psu_eeprom_item = {"name": "PSU EEPROM test", "deal": "test_psu_eeprom"}

test_temp_ancestor_item = {"name": "temp test", "deal": "startMenu", "childid": MENU_ID_TEMP_TEST}
test_temp_item = {"name": "Temperature test", "deal": "test_tempinfo_new"}
test_mac_temp_item = {"name": "MAC temp test", "deal": "test_mac_temp"}
################## LED test##############
test_led_item = {"name": "LED test", "deal": "startMenu", "childid": MENU_ID_LED}
test_sysled_item = {
    "name": "LED test",
    "deal": "test_led_new",
    'before': 'test_stop_fanctrol',
    'after': 'test_start_fanctrol'}
test_mgmtled_item = {"name": "MGMT LED test", 'before': 'test_bmc_channel', "deal": "test_mgmtled"}
################### FAN test###############
test_fan_items = {"name": "Fan test", "deal": "startMenu", "childid": MENU_ID_FAN_TEST}
test_fan_status_item = {"name": "FAN status test", "deal": "test_fan_status_standard_sysfs"}
test_fan_speed_item = {"name": "FAN speed test", "deal": "test_fan_speed_standard_sysfs"}
test_fan_item = {"name": "FAN speed detection", "deal": "startMenu", "childid": MENU_ID_FAN_SPEED_TEST}
test_fan_low_item = {
    "name": "Fan low speed detection",
    "deal": "test_fan_ratio_standard_sysfs",
    'param': '{"ratio":%d,"sleep":13}' % FAN_LOWRATIO,
    'before': 'test_stop_fanctrol',
    'after': 'test_start_fanctrol'}
test_fan_middle_item = {
    "name": "Fan medium speed detection",
    "deal": "test_fan_ratio_standard_sysfs",
    'param': '{"ratio":%d,"sleep":13}' % FAN_MIDRATIO,
    'before': 'test_stop_fanctrol',
    'after': 'test_start_fanctrol'}
test_fan_high_item = {
    "name": "Fan high speed detection",
    "deal": "test_fan_ratio_standard_sysfs",
    'param': '{"ratio":%d,"sleep":13}' % FAN_HIGHRATIO,
    'before': 'test_stop_fanctrol',
    'after': 'test_start_fanctrol'}

################# PSU status detection#############
test_power_item = {"name": "PSU test", "deal": "startMenu", "childid": MENU_ID_PSU_TEST}
test_power_status_item = {"name": "PSU status test", "deal": "test_power_status"}
test_power_pmbus_item = {"name": "PSU PMBus test", "deal": "test_power_pmbus_msg"}

################### stress test###############
test_stress_item = {"name": "Stress test", "deal": "startMenu", "childid": MENU_ID_STRESS_TEST}
test_ddr_stress_test_item = {"name": "DDR stress test(CPU&BMC)", "deal": "startMenu", "childid": MENU_ID_DDR_TEST}
test_ssd_stress_test_item = {"name": "SSD stress test", "deal": "startMenu", "childid": MENU_ID_SSD_TEST}
test_i2c_stress_test_item = {
    "name": "I2C stress test(CPU&BMC)",
    "deal": "startMenu",
    "childid": MENU_ID_I2C_STRESS_TEST}
test_kr_stress_test_item = {"name": "KR stress test", "deal": "test_kr_stress"}
test_cpu_stress_test_item = {"name": "CPU stress test", "deal": "startMenu", "childid": MENU_ID_CPU_STRESS_TEST}
test_pcie_stress_test_item = {
    "name": "PCIe stress test",
    "deal": "test_PCIe_stress",
    "before": "set_port_mac_lb",
    "after": "cancel_port_mac_lb"}
test_lpc_stress_test_item = {"name": "LPC stress test", "deal": "test_lpc_stress"}
test_emmc_stress_test_item = {"name": "eMMC stress test", "deal": "startMenu", "childid": MENU_ID_BMC_EMMC_STRESS}
test_usb_stress_test_item = {"name": "USB stress test", "deal": "test_usb_stress"}
test_MDIO_stress_test_item = {"name": "MDIO stress test", "deal": "test_MDIO_stress"}
test_cpu_MDIO_stress_test_item = {
    "name": "CPU MDIO stress test",
    "deal": "cpu_test_MDIO_stress",
    'before': 'test_modprobe_cpu_gpio_mdio',
    'after': 'test_rmmod_cpu_gpio_mdio'}

# emmc stress test
test_emmc_stress_test_item_start_item = {
    "name": "Start background test",
    "deal": "test_bmc_testcase",
    "param": "bmc_test_emmc_stress"}
test_emmc_stress_test_item_stop_item = {"name": "Terminate background test", "deal": "test_bmc_emmc_stress_stop"}
test_emmc_stress_test_item_result_item = {
    "name": "View test results",
    "deal": "test_bmc_testcase",
    "param": "bmc_test_emmc_stress_result"}

# DDR stress test
test_cpu_ddr_item = {"name": "CPU DDR test", "deal": "startMenu", "childid": MENU_ID_DDR_CPU_TEST}
test_cpu_test_ddr_stress_item = {"name": "Start CPU DDR background test", "deal": "test_ddr_stress"}
test_cpu_stop_ddr_stress_item = {"name": "Terminate CPU DDR background test", "deal": "test_ddr_stress_stop"}
test_cpu_get_ddr_stress_result_item = {"name": "View CPU DDR test results", "deal": "test_ddr_stress_result"}
test_cpu_ddr_stress_with_result_item = {"name": "CPU DDR background test", "deal": "test_ddr_stress_with_result"}

test_bmc_ddr_item = {
    "name": "BMC DDR test",
    'before': 'test_bmc_channel',
    "deal": "startMenu",
    "childid": MENU_ID_DDR_BMC_TEST}
test_bmc_test_ddr_stress_item = {
    "name": "Start BMC DDR background test",
    "deal": "test_bmc_testcase",
    "param": "bmc_test_ddr_stress"}
test_bmc_stop_ddr_stress_item = {"name": "Terminate BMC DDR background test", "deal": "test_bmc_ddr_stress_stop"}
test_bmc_get_ddr_stress_result_item = {
    "name": "View BMC DDR test results",
    "deal": "test_bmc_testcase",
    "param": "bmc_test_ddr_stress_result"}
test_bmc_ddr_stress_with_result_item = {"name": "BMC DDR test", "deal": "bmc_test_ddr_stress_with_result"}


################### SSD###############
test_ssd_smart_item = {"name": "SSD Smart information test", "deal": "test_ssd_smart_info"}
test_ssd_smart_attr_item = {"name": "SSD Smart attribute test", "deal": "test_ssd_smart_attrs"}
test_ssd_smart_health_item = {"name": "SSD health status test", "deal": "test_ssd_health"}
test_sata_abnormal_item = {"name": "SATA interface abnormal test", "deal": "test_sata_abnormal"}

test_ddr_ecc_item = {"name": "DDR ECC test", "deal": "test_ddr_ecc"}
test_drr_used_item = {"name": "DDR USED test", "deal": "memory_stat"}
test_get_pcie_aer_result_item  = {"name":"MAC PCIe AER test", "deal" :"test_iio_pcie_aer_result"}
test_led_status_item  = {"name":"LED status test", "deal" :"test_led_status_check"}

###################服务状态检测###############
# service
test_pre_service_item = {"name": "巡检前服务状态检测", "deal": "test_service_status_check"}
test_service_item = {"name": "巡检后服务状态检测", "deal": "test_service_status_check"}

diagtestbmcall = [
    test_bmc_cpu_info_item,
    test_bmc_ddr_info_item,
    test_bmc_peci_item,
    test_bmc_i2c_scan_item,
    test_bmc_cpld_item,
    test_bmc_emmc_info_item,
    test_bmc_gpio_item,
    test_bmc_sol_item,
    test_bmc_version_item,
    test_bmc_mdio_item,
    test_bmc_5387md5_item,
]

diagtestall = [
    #test_pre_service_item,
    test_tlv_eeprom_item,
    test_sys_item,
    # test_sys_part_item, #sdk version
    test_temp_item, #mac temp other temp
    test_dcdc_item,
    test_fan_eeprom_item,
    test_fan_status_item,
    test_fan_speed_item,
    test_psu_eeprom_item,
    test_power_status_item,
    test_power_pmbus_item,
    test_sff_present_status_item, # 光模块在位和状态检测
    # test_rtc_date_item,
    test_ssd_smart_item,
    test_ssd_smart_attr_item,
    test_ssd_smart_health_item,
    test_sata_abnormal_item,
    test_pcie_scan_item, #带宽检测
    test_i2c_item,
    # test_cpld_item,
    test_fpga_item,
    test_ddr_ecc_item,
    test_drr_used_item,
    test_cpu_gpio_item,
    test_cpu_fpga_upgrade_item,
]

BackgroundMenuList = [
    test_portframe_item,
    test_prbs_item,
    test_portbroadcast_item,
    test_kr_item,
]

SMI_ACCESS = {
    "CPU": {
        "open": [{"cmd": "dfd_debug io_wr 0x952 0xfe"}],
        "close": [{"cmd": "dfd_debug io_wr 0x952 0xff"}],
    },
    "BMC": {
        "open": [{"cmd": "i2cset -f -y 6 0x3d 0x53 0xfe"}],
        "close": [{"cmd": "i2cset -f -y 6 0x3d 0x53 0xff"}],
    },
}

open_fpga_i2c_access = [
    {"cmd": "dfd_debug io_wr 0x951 0xfe"},
]
open_bmc_fpga_i2c_access = [
    {"cmd": "i2ctransfer -f -y 0 w8@0x70 0 0 0 0x9c 0 0 0 0x3"},
    {"cmd": "i2ctransfer -f -y 1 w8@0x70 0 0 0 0xa0 0 0 0 0x1"},
    {"cmd": "i2ctransfer -f -y 4 w8@0x70 0 0 0 0xa4 0 0 0 0x1"},
    {"cmd": "i2ctransfer -f -y 5 w8@0x70 0 0 0 0xa8 0 0 0 0x1"},
]
SETMAC_SN_LEN = {
    "board": 16,
    "fan": 16,
}

PSU_MODEL_MAP = {
    "DPS-1300AB-6": "PSA1300CRPS-F",
    "GW-CRPS1300D": "PSA1300CRPS-F",
}

LSSIGNAL_INT = [
    {
        "type": "200G",
        "mask_list": [
            {"bus": 2, "addr": 0x2d, "reg": 0x14, "set_val_1": 0x00, "set_val_2": 0xff},
            {"bus": 2, "addr": 0x2d, "reg": 0x15, "set_val_1": 0x00, "set_val_2": 0xff},
            {"bus": 2, "addr": 0x1d, "reg": 0x14, "set_val_1": 0x00, "set_val_2": 0xff},
        ],
        "loopback_list": {"startbus": 6, "endbus": 61, "startportnum": 1, "addr": 0x50, "reg": 0x1d, "set_val_1": 0x04, "set_val_2": 0x06},
        "status_list": [
            {"bus": 2, "addr": 0x2d, "reg": 0x12, "check_bit": 0, "ok_val_1": 0, "ok_val_2": 1, "port_num": 1},
            {"bus": 2, "addr": 0x2d, "reg": 0x12, "check_bit": 1, "ok_val_1": 0, "ok_val_2": 1, "port_num": 2},
            {"bus": 2, "addr": 0x2d, "reg": 0x12, "check_bit": 2, "ok_val_1": 0, "ok_val_2": 1, "port_num": 3},
            {"bus": 2, "addr": 0x2d, "reg": 0x12, "check_bit": 3, "ok_val_1": 0, "ok_val_2": 1, "port_num": 4},
            {"bus": 2, "addr": 0x2d, "reg": 0x12, "check_bit": 4, "ok_val_1": 0, "ok_val_2": 1, "port_num": 5},
            {"bus": 2, "addr": 0x2d, "reg": 0x12, "check_bit": 5, "ok_val_1": 0, "ok_val_2": 1, "port_num": 6},
            {"bus": 2, "addr": 0x2d, "reg": 0x12, "check_bit": 6, "ok_val_1": 0, "ok_val_2": 1, "port_num": 7},
            {"bus": 2, "addr": 0x2d, "reg": 0x12, "check_bit": 7, "ok_val_1": 0, "ok_val_2": 1, "port_num": 8},
            {"bus": 2, "addr": 0x2d, "reg": 0x13, "check_bit": 0, "ok_val_1": 0, "ok_val_2": 1, "port_num": 9},
            {"bus": 2, "addr": 0x2d, "reg": 0x13, "check_bit": 1, "ok_val_1": 0, "ok_val_2": 1, "port_num": 10},
            {"bus": 2, "addr": 0x2d, "reg": 0x13, "check_bit": 2, "ok_val_1": 0, "ok_val_2": 1, "port_num": 11},
            {"bus": 2, "addr": 0x2d, "reg": 0x13, "check_bit": 3, "ok_val_1": 0, "ok_val_2": 1, "port_num": 12},
            {"bus": 2, "addr": 0x2d, "reg": 0x13, "check_bit": 4, "ok_val_1": 0, "ok_val_2": 1, "port_num": 13},
            {"bus": 2, "addr": 0x2d, "reg": 0x13, "check_bit": 5, "ok_val_1": 0, "ok_val_2": 1, "port_num": 14},
            {"bus": 2, "addr": 0x2d, "reg": 0x13, "check_bit": 6, "ok_val_1": 0, "ok_val_2": 1, "port_num": 15},
            {"bus": 2, "addr": 0x2d, "reg": 0x13, "check_bit": 7, "ok_val_1": 0, "ok_val_2": 1, "port_num": 16},
            {"bus": 2, "addr": 0x1d, "reg": 0x12, "check_bit": 0, "ok_val_1": 0, "ok_val_2": 1, "port_num": 17},
            {"bus": 2, "addr": 0x1d, "reg": 0x12, "check_bit": 1, "ok_val_1": 0, "ok_val_2": 1, "port_num": 18},
            {"bus": 2, "addr": 0x1d, "reg": 0x12, "check_bit": 2, "ok_val_1": 0, "ok_val_2": 1, "port_num": 19},
            {"bus": 2, "addr": 0x1d, "reg": 0x12, "check_bit": 3, "ok_val_1": 0, "ok_val_2": 1, "port_num": 20},
            {"bus": 2, "addr": 0x1d, "reg": 0x12, "check_bit": 4, "ok_val_1": 0, "ok_val_2": 1, "port_num": 21},
            {"bus": 2, "addr": 0x1d, "reg": 0x12, "check_bit": 5, "ok_val_1": 0, "ok_val_2": 1, "port_num": 22},
            {"bus": 2, "addr": 0x1d, "reg": 0x12, "check_bit": 6, "ok_val_1": 0, "ok_val_2": 1, "port_num": 23},
            {"bus": 2, "addr": 0x1d, "reg": 0x12, "check_bit": 7, "ok_val_1": 0, "ok_val_2": 1, "port_num": 24},
        ],
    },
]

LSSIGNAL_RESET = [
    {
        "type": "200G",
        "mask_list": [
            {"bus": 2, "addr": 0x2d, "reg": 0x22, "set_val_1": 0x00, "set_val_2": 0xff},
            {"bus": 2, "addr": 0x2d, "reg": 0x23, "set_val_1": 0x00, "set_val_2": 0xff},
            {"bus": 2, "addr": 0x1d, "reg": 0x21, "set_val_1": 0x00, "set_val_2": 0xff},
        ],
        "access_list": {"startbus": 46, "endbus": 69, "addr": 0x50, "reg": 0x00, "startportnum": 1},
    },
    {
        "type": "400G",
        "mask_list": [
            {"bus": 2, "addr": 0x1d, "reg": 0x22, "set_val_1": 0x00, "set_val_2": 0xff},
        ],
        "access_list": {"startbus": 70, "endbus": 77, "addr": 0x50, "reg": 0x00, "startportnum": 25},
    },
]

LSSIGNAL_LPMODE = [
    {
        "type": "200G",
        "mask_list": [
            {"bus": 2, "addr": 0x2d, "reg": 0x32, "set_val_1": 0xff, "set_val_2": 0x00},
            {"bus": 2, "addr": 0x2d, "reg": 0x33, "set_val_1": 0xff, "set_val_2": 0x00},
            {"bus": 2, "addr": 0x1d, "reg": 0x37, "set_val_1": 0xff, "set_val_2": 0x00},
        ],
        "check_list": {"startbus": 46, "endbus": 69, "addr": 0x50, "reg": 0x1c, "check_bit": 3, "ok_val_1": 1, "ok_val_2": 0, "startportnum": 1},
    },
    {
        "type": "400G",
        "mask_list": [
            {"bus": 2, "addr": 0x1d, "reg": 0x38, "set_val_1": 0xff, "set_val_2": 0x00},
        ],
        "check_list": {"startbus": 70, "endbus": 77, "addr": 0x50, "reg": 0x12, "check_bit": 3, "ok_val_1": 1, "ok_val_2": 0, "startportnum": 25},
    },
]

LSSIGNAL_MODSEL = [
    {
        "type": "200G",
        "mask_list": [
            {"bus": 2, "addr": 0x2d, "reg": 0x30, "set_val_1": 0xff, "set_val_2": 0x00},
            {"bus": 2, "addr": 0x2d, "reg": 0x31, "set_val_1": 0xff, "set_val_2": 0x00},
            {"bus": 2, "addr": 0x1d, "reg": 0x35, "set_val_1": 0xff, "set_val_2": 0x00},

        ],
        "access_list": {"startbus": 46, "endbus": 69, "addr": 0x50, "reg": 0x00, "startportnum": 1},
    },
    {
        "type": "400G",
        "mask_list": [
            {"bus": 2, "addr": 0x1d, "reg": 0x36, "set_val_1": 0xff, "set_val_2": 0x00},
        ],
        "access_list": {"startbus": 70, "endbus": 77, "addr": 0x50, "reg": 0x00, "startportnum": 25},
    },
]

LSSIGNAL_VCC = [
    {
        "type": "200G",
        "threshold_list": {"startbus": 46, "endbus": 69, "addr": 0x50, "reg1": 0x1a, "reg2": 0x1b, "min": 3135, "max": 3600, "startportnum": 1},
    },
    {
        "type": "400G",
        "threshold_list": {"startbus": 70, "endbus": 77, "addr": 0x50, "reg1": 0x10, "reg2": 0x11, "min": 3135, "max": 3600, "startportnum": 25},
    },
]

LSSIGNAL_VCCR = [
    {
        "type": "200G",
        "threshold_list": {"startbus": 46, "endbus": 69, "addr": 0x50, "reg1": 0x20, "reg2": 0x21, "min": 3135, "max": 3600, "startportnum": 1},

    },
    {
        "type": "400G",
        "threshold_list": {"startbus": 70, "endbus": 77, "addr": 0x50, "reg1": 0x18, "reg2": 0x19, "min": 3135, "max": 3600, "startportnum": 25},

    },
]

LSSIGNAL_VCCT = [
    {
        "type": "200G",
        "threshold_list": {"startbus": 46, "endbus": 69, "addr": 0x50, "reg1": 0x22, "reg2": 0x23, "min": 3135, "max": 3600, "startportnum": 1},

    },
    {
        "type": "400G",
        "threshold_list": {"startbus": 70, "endbus": 77, "addr": 0x50, "reg1": 0x16, "reg2": 0x17, "min": 3135, "max": 3600, "startportnum": 25},

    },
]

EMMC_REGISTER = [
 {"name" : "OCR", "location": "/sys/class/mmc_host/mmc0/mmc0\:0001/ocr"},
    {"name" : "CID", "location": "/sys/class/mmc_host/mmc0/mmc0\:0001/cid"},
    {"name" : "CSD", "location": "/sys/class/mmc_host/mmc0/mmc0\:0001/csd"},
    {"name" : "EXT_CSD", "location" : "/sys/kernel/debug/mmc0/mmc0\:0001/ext_csd"},
]

DEV_INFO = {
    "onie_version":"2023.02",
    "onie_build_date":"2023-09-18T02:54+0000",
    #"onie_sub_version":"1.0.1",
    "bios_vendor":"American Megatrends International, LLC.",
    "bios_version":"5.28(1AZHA4818)",
    "bios_release_date":"09/27/2023",
    # "cpld_check":{
    #     "CPU_CPLD":["24240313", "09230619"],
    #     "BASE_CPLD ":["23240318", "01231107"],
    #     "MAC_CPLDA":["10231031"],
    #     "MAC_CPLDB":["06231122", "05231030"],
    #     "MAC_CPLDC":["12240219", "01231109"],
    #     "UPORT_CPLD":["10231207", "01231109"],
    #     "DPORT_CPLD":["10231207", "01231109"],
    #     "UFCB_CPLD":["13231207", "01231023"],
    #     "DFCB_CPLD":["13231207", "01231023"],
    # },
    "fpga_check":{
        "MAC FPGA版本检测":"0x7a642305",
        "UPORT FPGA版本检测":"0x7a322406",
        "DPORT FPGA版本检测":"0x7a322406",
    },
    "sdk_version":"sdk-6.5.28 built 20231108 (Wed Nov  8 05:07:45 2023)",
    "PCIe FW loader version":"2.11",
    "PCIe FW version":"0000_00",
    "PCIe FW loader built date":"20221103",
  #"bmc_version":"2.21",
    # "bcm5387_version":"b7b48c9cefb51a5dfa2b85436b5c8c43",
}
EMMC_FIO = {
    "randrw" : [
        {
            "name": "randrw_4k", "rw": "randrw", "bs": "4k", "rwmixwrite": 50, "iodepth": 32, "size": "10M", "verify" : "md5", "do_verify": 1
        },
        {
            "name": "randrw_8k", "rw": "randrw", "bs": "8k", "rwmixwrite": 50, "iodepth": 32, "size": "10M", "verify" : "md5", "do_verify": 1
        },
        {
            "name": "randrw_16k", "rw": "randrw", "bs": "16k", "rwmixwrite": 50, "iodepth": 32, "size": "10M", "verify" : "md5", "do_verify": 1
        },
    ],
    "rw" : [
        {
            "name": "rw_4k", "rw": "rw", "bs": "4k", "rwmixwrite": 50, "iodepth": 32, "size": "10M", "verify" : "md5", "do_verify": 1
        },
        {
            "name": "rw_8k", "rw": "rw", "bs": "8k", "rwmixwrite": 50, "iodepth": 32, "size": "10M", "verify" : "md5", "do_verify": 1
        },
        {
            "name": "rw_16k", "rw": "rw", "bs": "16k", "rwmixwrite": 50, "iodepth": 32, "size": "10M", "verify" : "md5", "do_verify": 1
        },
    ]
}

SSD_FIO = {
    "randrw" : [
        {
            "name": "randrw_4k", "rw": "randrw", "bs": "4k", "rwmixwrite": 50, "iodepth": 32, "size": "5G", "verify" : "md5", "do_verify": 1
        },
        {
            "name": "randrw_8k", "rw": "randrw", "bs": "8k", "rwmixwrite": 50, "iodepth": 32, "size": "5G", "verify" : "md5", "do_verify": 1
        },
        {
            "name": "randrw_16k", "rw": "randrw", "bs": "16k", "rwmixwrite": 50, "iodepth": 32, "size": "5G", "verify" : "md5", "do_verify": 1
        },
    ],
    "rw" : [
        {
            "name": "rw_4k", "rw": "rw", "bs": "4k", "rwmixwrite": 50, "iodepth": 32, "size": "5G", "verify" : "md5", "do_verify": 1
        },
        {
            "name": "rw_8k", "rw": "rw", "bs": "8k", "rwmixwrite": 50, "iodepth": 32, "size": "5G", "verify" : "md5", "do_verify": 1
        },
        {
            "name": "rw_16k", "rw": "rw", "bs": "16k", "rwmixwrite": 50, "iodepth": 32, "size": "5G", "verify" : "md5", "do_verify": 1
        },
    ]
}

SSD_LIST = [
    {
        "model": "SSDSCKKB240G8",
        "attrs": [
            {"attr_name": "坏块增加数", "id": 0x05},
            {"attr_name": "写失败次数", "id": 0xab},
            {"attr_name": "擦失败测试", "id": 0xac},
            {"attr_name": "剩余寿命", "id": 0xe9, "life" : 95},
            {"attr_name": "PLP容量", "id": 0xaf},
            {"attr_name": "SATA CRC", "id": 0xc7, "warning": 1, "critical": 2},
            {"attr_name": "SATA降速", "id": 0xb7, "warning": 1, "critical": 2},
            {"attr_name": "E2E错误", "id": 0xb8, "warning": 1, "critical": 2},
            {"attr_name": "温度", "id": 0xbe, "min": -50, "max": 70}, #低温合法性不设下限，暂用-50度，实际测试不会达到。
        ],
    },
    {
        "model": "SSDSCKKB480GZ",
		"attrs": [
			{"attr_name": "坏块增加数", "id": 0x05},
			{"attr_name": "写失败次数", "id": 0xab},
			{"attr_name": "擦失败测试", "id": 0xac},
			{"attr_name": "剩余寿命", "id": 0xe9, "life" : 95},
			{"attr_name": "PLP容量", "id": 0xaf},
			{"attr_name": "SATA CRC", "id": 0xc7, "warning": 1, "critical": 2},
			{"attr_name": "SATA降速", "id": 0xb7, "warning": 1, "critical": 2},
			{"attr_name": "E2E错误", "id": 0xb8, "warning": 1, "critical": 2},
			{"attr_name": "温度", "id": 0xbe, "min": -50, "max": 70}, #低温合法性不设下限，暂用-50度，实际测试不会达到。
		],
	},
    {
        "model": "AF2MA31DTDLT240A",
        "attrs": [
            {"attr_name": "坏块增加数", "id": 0x05},
            {"attr_name": "写失败次数", "id": 0xab},
            {"attr_name": "擦失败测试", "id": 0xac},
            {"attr_name": "剩余寿命", "id": 0xca, "life" : 95},
            {"attr_name": "PLP容量", "id": 0xaf},
            {"attr_name": "SATA CRC", "id": 0xc7, "warning": 1, "critical": 2},
            {"attr_name": "SATA降速", "id": 0xb7, "warning": 1, "critical": 2},
            {"attr_name": "E2E错误", "id": 0xb8, "warning": 1, "critical": 2},
            {"attr_name": "温度", "id": 0xc2, "min": -50, "max": 70},
        ],
    },
    {
        "model": "ER2-GD240",
        "attrs": [
            {"attr_name": "坏块增加数", "id": 0x05},
            {"attr_name": "写失败次数", "id": 0xab},
            {"attr_name": "擦失败测试", "id": 0xac},
            {"attr_name": "剩余寿命", "id": 0xca, "life" : 95},
            {"attr_name": "PLP容量", "id": 0xe5},
            {"attr_name": "SATA CRC", "id": 0xc7, "warning": 1, "critical": 2},
            {"attr_name": "SATA降速", "id": 0xb7, "warning": 1, "critical": 2},
            {"attr_name": "E2E错误", "id": 0xb8, "warning": 1, "critical": 2},
            {"attr_name": "温度", "id": 0xbe, "min": -50, "max": 70},
        ],
    },
    {
		"model": "ER2-GD480",
		"attrs": [
			{"attr_name": "坏块增加数", "id": 0x05},
			{"attr_name": "写失败次数", "id": 0xab},
			{"attr_name": "擦失败测试", "id": 0xac},
			{"attr_name": "剩余寿命", "id": 0xca, "life" : 95},
			{"attr_name": "PLP容量", "id": 0xe5},
			{"attr_name": "SATA CRC", "id": 0xc7, "warning": 1, "critical": 2},
			{"attr_name": "SATA降速", "id": 0xb7, "warning": 1, "critical": 2},
			{"attr_name": "E2E错误", "id": 0xb8, "warning": 1, "critical": 2},
			{"attr_name": "温度", "id": 0xbe, "min": -50, "max": 70},
		],
	},
    {
        "model": "MD619GXCIDE6",
        "attrs": [
            {"attr_name": "坏块增加数", "id": 0x05},
            {"attr_name": "写失败次数", "id": 0xf6},
            {"attr_name": "擦失败测试", "id": 0xf7},
            {"attr_name": "剩余寿命", "id": 0xa9, "life" : 95},
            {"attr_name": "SATA CRC", "id": 0xc7, "warning": 1, "critical": 2},
            {"attr_name": "温度", "id": 0xc2, "min": -50, "max": 70},
        ],
    },
    {
        "model": "MZNLH240HBJQ-00005",
        "attrs": [
            {"attr_name": "坏块增加数", "id": 0x05},
            {"attr_name": "写失败次数", "id": 0xb5},
            {"attr_name": "擦失败测试", "id": 0xb6},
            {"attr_name": "剩余寿命", "id": 0xf5, "life" : 95},
            {"attr_name": "SATA CRC", "id": 0xc7, "warning": 1, "critical": 2},
            {"attr_name": "SATA降速", "id": 0xf3, "warning": 1, "critical": 2},
            {"attr_name": "E2E错误", "id": 0xb8, "warning": 1, "critical": 2},
            {"attr_name": "温度", "id": 0xbe, "min": -100, "max": 70},
        ],
    },
    {
        "model": "MZNLH480HBLR-00005",
		"attrs": [
			{"attr_name": "坏块增加数", "id": 0x05},
			{"attr_name": "写失败次数", "id": 0xb5},
			{"attr_name": "擦失败测试", "id": 0xb6},
			{"attr_name": "剩余寿命", "id": 0xf5, "life" : 95},
			{"attr_name": "SATA CRC", "id": 0xc7, "warning": 1, "critical": 2},
            {"attr_name": "SATA降速", "id": 0xf3, "warning": 1, "critical": 2},
			{"attr_name": "E2E错误", "id": 0xb8, "warning": 1, "critical": 2},
			{"attr_name": "温度", "id": 0xbe, "min": -100, "max": 70},
		],
	},
]
PCIE_STRESS_CMD = [
    {"cmd_name":"bcmcmdb \"dsh -c 'set CMIC_CMC0_PKTDMA_CH1_PKT_COUNT_RXPKTr 0'\"", "delay": 10, "ignore": 1},
    {"cmd_name":"bcmcmdb \"dsh -c 'get CMIC_CMC0_PKTDMA_CH1_PKT_COUNT_RXPKTr'\"", "delay": 1, "flag":"COUNT="},
]

PCIE_PRE_CMD = [
    {"cmd_name":"bcmcmdb \"stg stp 1 cd forward\""},
    {"cmd_name":"bcmcmdb \"vlan create 2\""},
    {"cmd_name":"bcmcmdb \"vlan add 2 PortBitMap=cd0-cd1,cpu UntagBitMap=cd0-cd1\""},
    {"cmd_name":"bcmcmdb \"pvlan set cd0-cd1 2\""},
    {"cmd_name":"bcmcmdb \"tx 100 pbm=cd0 length=9000 untagged=yes sm=0x001122334455 dm=0xffffffffffff\""},
]
PCIE_AFTER_CMD= [
    {"cmd_name":"bcmcmdb \"vlan destroy 2\""},
    {"cmd_name":"bcmcmdb \"pvlan set cd0 1\""},
    {"cmd_name":"bcmcmdb \"pvlan set cd1 1\""},
]

MGMT_LOOPBACK = {
    '10'  :  "pseudo_phy_test.py wr 0x00 0x59 0 0 0 0x000B &&\
              pseudo_phy_test.py wr 0x11 0x00 0 0 0 0x0100 &&\
              pseudo_phy_test.py wr 0x11 0x30 0 0 0 0x8400",
    '100' : "pseudo_phy_test.py wr 0x00 0x59 0 0 0 0x000B &&\
             pseudo_phy_test.py wr 0x11 0x00 0 0 0 0x2100 &&\
             pseudo_phy_test.py wr 0x11 0x30 0 0 0 0x8400 ",
    '1000': "pseudo_phy_test.py wr 0x11 0x12 0 0 0 0x1800 &&\
             pseudo_phy_test.py wr 0x11 0x00 0 0 0 0x0040 &&\
             pseudo_phy_test.py wr 0x11 0x30 0 0 0 0x8400 &&\
             pseudo_phy_test.py wr 0x00 0x59 0 0 0 0x004B ",
    'check' : 'pseudo_phy_test.py rd 0x11 0x02 && pseudo_phy_test.py rd 0x11 0x02',
    'clear' : "pseudo_phy_test.py wr 0x00 0x59 0 0 0 0x000B && pseudo_phy_test.py wr 0x11 0x00 0 0 0 0x9140",
}

PTU_CMD = [
    {
        "model": "D-1527",
        "cmd" : [
            {"name": "cd /usr/local/bin/d1527 && chmod 777 * && ./BroadwellPTU_Rev2.0 -core0x07 -P80 -Lic=yes  >/dev/null &","num":0x00},
            {"name": "cd /usr/local/bin/d1527 && chmod 777 * && ./BroadwellPTU_Rev2.0 -core0x0B -P80 -Lic=yes  >/dev/null &","num":0x01},
            {"name": "cd /usr/local/bin/d1527 && chmod 777 * && ./BroadwellPTU_Rev2.0 -core0x0D -P80 -Lic=yes  >/dev/null &","num":0x02},
            {"name": "cd /usr/local/bin/d1527 && chmod 777 * && ./BroadwellPTU_Rev2.0 -core0x0E -P80 -Lic=yes  >/dev/null &","num":0x03},
        ],
    },
    {
        "model": "D-1627",
        "cmd" : [
            {"name": "cd /usr/local/bin/d1627 && chmod 777 * && ./HewittLakePTU_Rev0.7 -core0x07 -P80 -Lic=yes  >/dev/null &","num":0x00},
            {"name": "cd /usr/local/bin/d1627 && chmod 777 * && ./HewittLakePTU_Rev0.7 -core0x0B -P80 -Lic=yes  >/dev/null &","num":0x01},
            {"name": "cd /usr/local/bin/d1627 && chmod 777 * && ./HewittLakePTU_Rev0.7 -core0x0D -P80 -Lic=yes  >/dev/null &","num":0x02},
            {"name": "cd /usr/local/bin/d1627 && chmod 777 * && ./HewittLakePTU_Rev0.7 -core0x0E -P80 -Lic=yes  >/dev/null &","num":0x03},
        ],
    },
]


TESTCASE = {
    "ip_netns_exec": 0,
    "get_phypcie_version_cmd":"bcmcmd \"dsh -c 'pciephy fwinfo'\" |grep PCIe", #mac芯片固件版本信息
    "show_mac_temp_cmd":"bcmcmd \"dsh -c 'hmon temperature'\" |sed -n '6,14p'",
    "dev_info":DEV_INFO,
    "mft_port": MFT_PORTCONFIG,
    "FANS_THRESHOLD": FANS_THRESHOLD,
    "BackgroundMenuList": BackgroundMenuList,
    "switch_cpld_gpio": SwitchCpldGpio,
    "sdkcmdversion": 0,  # 0bcmcmd  1bcmcmdb
    "SetEnv5387": SetEnv5387,
    "FanLowLevel": FAN_LOWRATIO,
    "FanHighLevel": FAN_HIGHRATIO,
    "open_fpga_i2c_access": open_fpga_i2c_access,
    #"open_bmc_fpga_i2c_access": open_bmc_fpga_i2c_access,
    "smi_access": SMI_ACCESS,
    "ssd_slot_num": 2,
    "temps": TEMPS_DEFINE,
    "BIOS_TEST": BIOS_TEST,
    "frustatus": FRUS_STATUS,
    #'bmctlve2sync': BMC_TLV_E2_SYNC,
    #'bmce2loc': BMC_E2_LOC,
    'setmacsnlen': SETMAC_SN_LEN,
    'psu_model_map': PSU_MODEL_MAP,
    "dcdcsensor": DCDC_LIST,
    "frustatusdecode": FRUS_STATUS_DECODE,
    "biosstatus": BIOS_STATUS,
    "biosstatusdecode": BIOS_STATUS_DECODE,
    "MUL_FPGA_INFO": MUL_FPGA_VERSION_INFO,
    "LSSIGNAL_INT": LSSIGNAL_INT,
    "LSSIGNAL_RESET": LSSIGNAL_RESET,
    "LSSIGNAL_LPMODE": LSSIGNAL_LPMODE,
    "LSSIGNAL_MODSEL": LSSIGNAL_MODSEL,
    "LSSIGNAL_VCC": LSSIGNAL_VCC,
    "LSSIGNAL_VCCR": LSSIGNAL_VCCR,
    "LSSIGNAL_VCCT": LSSIGNAL_VCCT,
    "EMMC_REGISTER": EMMC_REGISTER,
    "EMMC_FIO": EMMC_FIO,
    "SSD_LIST": SSD_LIST,
    "SSD_FIO": SSD_FIO,
    "PCIE_STRESS_CMD": PCIE_STRESS_CMD,
    "PCIE_PRE_CMD": PCIE_PRE_CMD,
    "PCIE_AFTER_CMD": PCIE_AFTER_CMD,
    "AER_NOCHECK": 1,
    "MGMT_LOOPBACK": MGMT_LOOPBACK,
    "MGMT_LOOPBACK_SET": 1,
    #"BMCSwitchTime": 150,
    "PTU_CMD": PTU_CMD,
    "PTU_TEST": 1,
    "ECC_CMD": ECC_CMD,
    "BIOS_INFO": "/host/sonic/bios_info",
    "BMC": {
        'port': 8084,
        'requesthttp': 'http://%s:8084/factest/getmsg?'
    },
    "SONIC": {
        'ip': '1.1.1.1'
    },
    "CPLDTEST": [
        {"name": "CPU_CPLD", "io_addr": 0x0a00, "addr": 0x0a, "gettype": "io", "testval": [0x55, 0xaa, 0x00, 0xff], "invert": 1},
        {"name": "BASE_CPLD ", "io_addr": 0x0900, "addr": 0x55, "gettype": "io", "testval": [0x55, 0xaa, 0x00, 0xff], "invert": 1},
        {"name": "MAC_CPLDA", "bus": 87, "devno": 0x1D, "addr": 0x55, "testval": [0x55, 0xaa, 0x00, 0xff], "invert": 1},
        {"name": "MAC_CPLDB", "bus": 88, "devno": 0x2D, "addr": 0x55, "testval": [0x55, 0xaa, 0x00, 0xff], "invert": 1},
        {"name": "MAC_CPLDC", "bus": 89, "devno": 0x3D, "addr": 0x55, "testval": [0x55, 0xaa, 0x00, 0xff], "invert": 1},
        {"name": "UPORT_CPLD", "bus": 62, "devno": 0x3D, "addr": 0x55, "testval": [0x55, 0xaa, 0x00, 0xff], "invert": 1},
        {"name": "DPORT_CPLD", "bus": 127, "devno": 0x3D, "addr": 0x55, "testval": [0x55, 0xaa, 0x00, 0xff], "invert": 1},
        {"name": "UFCB_CPLD", "bus": 103, "devno": 0x0D, "addr": 0x55, "testval": [0x55, 0xaa, 0x00, 0xff], "invert": 1},
        {"name": "DFCB_CPLD", "bus": 111, "devno": 0x0D, "addr": 0x55, "testval": [0x55, 0xaa, 0x00, 0xff], "invert": 1},
    ],
    "FPGATEST": [
        {"name": "MAC_FPGA", "path": "/dev/fpga1", "offset": 0x8, "gettype": "devfile", "value": [0x55, 0xaa, 0x5a, 0xa5], "read_len":4},
        {"name": "UPORT_FPGA", "path": "/dev/fpga0", "offset": 0x8, "gettype": "devfile", "value": [0x55, 0xaa, 0x5a, 0xa5], "read_len":4},
        {"name": "DPORT_FPGA", "path": "/dev/fpga2", "offset": 0x8, "gettype": "devfile", "value": [0x55, 0xaa, 0x5a, 0xa5], "read_len":4},
        ],
    "LED_NEWS": LED_NEW,
    "I2CSCAN": I2C_SCAN_LIST,
    'optoe_port_map': OPTOE_PORT_MAP,
    'mgmt': {
        'retrytimes': 5,
        '10M': {'case': 'bmc_set_loopback', 'param': {'speed': "10"}},
        '100M': {'case': 'bmc_set_loopback', 'param': {'speed': "100"}},
        '1000M': {'case': 'bmc_set_loopback', 'param': {'speed': "1000"}},
        'clear': {'case': 'bmc_reset_loopback', 'param': {'speed': "clear"}},
        'bmccheck': {'case': 'bmc_check_loopback', 'param': {'packetcount': 2000, 'iface': 'eth0', 'pktpassthread': 0.8}},
        'packetcount': 2000,
        'iface': 'eth0',
        'pktpassthread': 0.8,
        'ledon': {'bmc_interface': 'bmc_log_os_system', "cmd": "echo 0x0010 > /sys/bus/mdio_bus/devices/1e680000.ethernet--1:18/hw_test10"},
        'ledoff': {'bmc_interface': 'bmc_log_os_system', "cmd": "echo 0x0004 > /sys/bus/mdio_bus/devices/1e680000.ethernet--1:18/hw_test10"},
    },
    # "VERSIONTEST": [
    #     {"name": "MAC VR PSU:", "bus": 83, "devno": 0x5b, "addr": 0x76},
    # ],
    # "UCD90160_VER": [
    #     {"name": "Base UCD90160:", "cmd": "i2ctransfer -f -y 64 w1@0x5b 0x9b r9"},
    #     {"name": "MAC UCD90160:", "cmd": "i2ctransfer -f -y 85 w1@0x5b 0x9b r9"},
    # ],
    "EthernetNum": 32,
    "Ethernet_LIST": ['Ethernet0', 'Ethernet4', 'Ethernet8', 'Ethernet12', 'Ethernet16', 'Ethernet20', 'Ethernet24', 'Ethernet28',
                       'Ethernet32', 'Ethernet36', 'Ethernet40', 'Ethernet44', 'Ethernet48', 'Ethernet52', 'Ethernet56', 'Ethernet60',
                       'Ethernet64', 'Ethernet68', 'Ethernet72', 'Ethernet76', 'Ethernet80', 'Ethernet84', 'Ethernet88', 'Ethernet92', 
                       'Ethernet96', 'Ethernet100', 'Ethernet108', 'Ethernet116', 'Ethernet124', 'Ethernet132', 'Ethernet140', 'Ethernet148'],
    #"KR_EYE_CMD": "bcmcmdb \"dsh -c 'phy diag 38 dsc'\" ",
    #"PHY_MDIO_DEV": {
    #    "53134O    ": ["00", "01", "02", "03", "04"],
    #},
}

alltest = []
looptest = []
