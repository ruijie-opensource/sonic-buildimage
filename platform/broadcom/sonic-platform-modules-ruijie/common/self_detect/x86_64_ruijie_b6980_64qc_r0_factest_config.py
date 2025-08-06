#!/usr/bin/python
# -*- coding: UTF-8 -*-
from collections import OrderedDict

RUIJIE_CARDID = 0x00004077
RUIJIE_PRODUCTNAME = "B6980-64QC"
RUIJIE_PART_NUMBER = "RJ0000001"
RUIJIE_LABEL_REVISION = "R01"
RUIJIE_ONIE_VERSION = "2023.02"
RUIJIE_MAC_SIZE = 3
RUIJIE_MANUF_NAME = "Ruijie"
RUIJIE_MANUF_COUNTRY = "CN"
RUIJIE_VENDOR_NAME = "Ruijie"
RUIJIE_DIAG_VERSION = "0.1.0.15"
RUIJIE_SERVICE_TAG = "www.ruijie.com"

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
        {"io_addr": 0x722, "val": 0x02, "gettype": "io"},
        {"io_addr": 0x960, "val": 0xf7, "gettype": "io"},
    ],
    "switch_slave": [
        {"io_addr": 0x722, "val": 0x02, "gettype": "io"},
        {"io_addr": 0x722, "val": 0x01, "gettype": "io"},
        {"io_addr": 0x960, "val": 0xf7, "gettype": "io"},
    ],
}

CPU_CPLD_TEST = [
]


CPU_FPGA_TEST = [
    {"test_name": "MAC FPGA upgrade test", "cmd": "firmware_upgrade fpga test fpga0"},
]

FRULISTS = {
    "fans": [
        {"name": "FAN1", "bus": 95, "loc": 0x50},
        {"name": "FAN2", "bus": 104, "loc": 0x50},
        {"name": "FAN3", "bus": 96, "loc": 0x50},
        {"name": "FAN4", "bus": 105, "loc": 0x50},
        {"name": "FAN5", "bus": 97, "loc": 0x50},
        {"name": "FAN6", "bus": 106, "loc": 0x50},
        {"name": "FAN7", "bus": 98, "loc": 0x50},
        {"name": "FAN8", "bus": 107, "loc": 0x50},
    ],
    "psus": [
        {"name": "PSU1", "bus": 83, "loc": 0x50},
        {"name": "PSU2", "bus": 84, "loc": 0x50},
        {"name": "PSU3", "bus": 86, "loc": 0x50},
        {"name": "PSU4", "bus": 85, "loc": 0x50},
    ]
}

DCDC_LIST = [
    {"Sensor": "MAC_VDD3.3V_standby", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/128-005b/hwmon/hwmon*/in1_input", "Address": "dc-i2c-128-5b"},
    {"Sensor": "MAC_VDD12V_A", "CriticalLow": 10200, "CriticalHigh": 13800, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/128-005b/hwmon/hwmon*/in2_input", "Address": "dc-i2c-128-5b"},
    {"Sensor": "MAC_VDD1.0V_FPGA", "CriticalLow": 850, "CriticalHigh": 1150, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/128-005b/hwmon/hwmon*/in3_input", "Address": "dc-i2c-128-5b"},
    {"Sensor": "MAC_VDD1.8V_FPGA", "CriticalLow": 1530, "CriticalHigh": 2070, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/128-005b/hwmon/hwmon*/in4_input", "Address": "dc-i2c-128-5b"},
    {"Sensor": "MAC_VDD1.2V_FPGA", "CriticalLow": 1020, "CriticalHigh": 1380, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/128-005b/hwmon/hwmon*/in5_input", "Address": "dc-i2c-128-5b"},
    {"Sensor": "MAC_VDD3.3V", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/128-005b/hwmon/hwmon*/in6_input", "Address": "dc-i2c-128-5b"},
    {"Sensor": "MAC_VDD5V_CLK_MCU", "CriticalLow": 4250, "CriticalHigh": 5750, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/128-005b/hwmon/hwmon*/in7_input", "Address": "dc-i2c-128-5b"},
    {"Sensor": "MAC_VDD3.3V_MAC ", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/128-005b/hwmon/hwmon*/in8_input", "Address": "dc-i2c-128-5b"},
    {"Sensor": "MAC_VDDO1.8V", "CriticalLow": 1530, "CriticalHigh": 2070, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/128-005b/hwmon/hwmon*/in9_input", "Address": "dc-i2c-128-5b"},
    {"Sensor": "MAC_VDDO1.2V", "CriticalLow": 1020, "CriticalHigh": 1380, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/128-005b/hwmon/hwmon*/in10_input", "Address": "dc-i2c-128-5b"},
    {"Sensor": "MAC_VDD_CORE", "CriticalLow": 680, "CriticalHigh": 980, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/128-005b/hwmon/hwmon*/in11_input", "Address": "dc-i2c-128-5b"},
    {"Sensor": "MAC_VDD3.3_CLK", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/128-005b/hwmon/hwmon*/in12_input", "Address": "dc-i2c-128-5b"},
    {"Sensor": "MAC_VDD_ANALOG", "CriticalLow": 655, "CriticalHigh": 885, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/128-005b/hwmon/hwmon*/in13_input", "Address": "dc-i2c-128-5b"},
    {"Sensor": "MAC_VDD1.2V_MAC_A", "CriticalLow": 1020, "CriticalHigh": 1380, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/128-005b/hwmon/hwmon*/in14_input", "Address": "dc-i2c-128-5b"},
    {"Sensor": "QMAC_AVDD1.8V", "CriticalLow": 1530, "CriticalHigh": 2070, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/128-005b/hwmon/hwmon*/in15_input", "Address": "dc-i2c-128-5b"},
    {"Sensor": "MAC_VDD_ANALOG2", "CriticalLow": 655, "CriticalHigh": 885, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/128-005b/hwmon/hwmon*/in16_input", "Address": "dc-i2c-128-5b"},
    {"Sensor": "MAC_VDD12V_B", "CriticalLow": 10200, "CriticalHigh": 13800, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in1_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "MAC_VDD5.0V", "CriticalLow": 4250, "CriticalHigh": 5750, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in2_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "MAC_QSFPDD_VDD3.3V_A", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in3_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "MAC_QSFPDD_VDD3.3V_B", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in4_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "MAC_QSFPDD_VDD3.3V_C", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in5_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "MAC_QSFPDD_VDD3.3V_D", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in6_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "MAC_QSFPDD_VDD3.3V_E", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in7_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "MAC_QSFPDD_VDD3.3V_F", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in8_input", "Address": "dc-i2c-129-5b"},
    {"Sensor": "PORT_VDD1.0V_FPGA", "CriticalLow": 850, "CriticalHigh": 1150, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/130-005b/hwmon/hwmon*/in1_input", "Address": "dc-i2c-130-5b"},
    {"Sensor": "PORT_VDD1.8V_FPGA", "CriticalLow": 1530, "CriticalHigh": 2070, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/130-005b/hwmon/hwmon*/in2_input", "Address": "dc-i2c-130-5b"},
    {"Sensor": "PORT_VDD1.2V_FPGA", "CriticalLow": 1020, "CriticalHigh": 1380, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/130-005b/hwmon/hwmon*/in3_input", "Address": "dc-i2c-130-5b"},
    {"Sensor": "PORT_VDD3.3V", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/130-005b/hwmon/hwmon*/in4_input", "Address": "dc-i2c-130-5b"},
    {"Sensor": "PORT_VDD12V", "CriticalLow": 10200, "CriticalHigh": 13800, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/130-005b/hwmon/hwmon*/in5_input", "Address": "dc-i2c-130-5b"},
    {"Sensor": "PORT_VDD3.3V_standby", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/130-005b/hwmon/hwmon*/in6_input", "Address": "dc-i2c-130-5b"},
    {"Sensor": "PORT_QSFPDD_VDD3.3V_A", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/130-005b/hwmon/hwmon*/in7_input", "Address": "dc-i2c-130-5b"},
    {"Sensor": "PORT_QSFPDD_VDD3.3V_B", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/130-005b/hwmon/hwmon*/in8_input", "Address": "dc-i2c-130-5b"},
    {"Sensor": "PORT_QSFPDD_VDD3.3V_C", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/130-005b/hwmon/hwmon*/in9_input", "Address": "dc-i2c-130-5b"},
    {"Sensor": "PORT_QSFPDD_VDD3.3V_D", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/130-005b/hwmon/hwmon*/in10_input", "Address": "dc-i2c-130-5b"},
    {"Sensor": "PORT_QSFPDD_VDD3.3V_E", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/130-005b/hwmon/hwmon*/in11_input", "Address": "dc-i2c-130-5b"},
    {"Sensor": "PORT_QSFPDD_VDD3.3V_F", "CriticalLow": 2805, "CriticalHigh": 3795, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/130-005b/hwmon/hwmon*/in12_input", "Address": "dc-i2c-130-5b"},
    {"Sensor": "MAC_VDD1.2V_MAC_B", "CriticalLow": 1020, "CriticalHigh": 1380, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/131-0067/hwmon/hwmon*/in3_input", "Address": "dc-i2c-131-67"},
    {"Sensor": "CPU_VDD12V","CriticalLow": 10200,"CriticalHigh": 13800,"gettype": "sysfs","Unit": "mV",
        "location": "/sys/bus/i2c/devices/77-005b/hwmon/hwmon*/in1_input","Address": "dc-i2c-77-5b"},
    {"Sensor": "CPU_VDD3.3V","CriticalLow": 2805,"CriticalHigh": 3795,"gettype": "sysfs","Unit": "mV",
        "location": "/sys/bus/i2c/devices/77-005b/hwmon/hwmon*/in2_input","Address": "dc-i2c-77-5b"},
    {"Sensor": "CPU_SSD_VDD3.3V","CriticalLow": 2805,"CriticalHigh": 3795,"gettype": "sysfs","Unit": "mV",
        "location": "/sys/bus/i2c/devices/77-005b/hwmon/hwmon*/in3_input","Address": "dc-i2c-77-5b"},
    {"Sensor": "CPU_P1V05_V","CriticalLow": 882,"CriticalHigh": 1232,"gettype": "sysfs","Unit": "mV",
        "location": "/sys/bus/i2c/devices/78-0067/hwmon/hwmon*/in4_input","Address": "dc-i2c-78-67"},
    {"Sensor": "CPU_VCCIN_V", "CriticalLow": 1368, "CriticalHigh": 2244, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/78-0067/hwmon/hwmon*/in3_input", "Address": "dc-i2c-78-67"},
    {"Sensor": "CPU_VCCD_V", "CriticalLow": 990, "CriticalHigh": 1452, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/78-006c/hwmon/hwmon*/in3_input", "Address": "dc-i2c-78-6c"},
    {"Sensor": "CPU_VCCSCSUS_V", "CriticalLow": 855, "CriticalHigh": 1265, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/78-006c/hwmon/hwmon*/in4_input", "Address": "dc-i2c-78-6c"},
    {"Sensor": "CPU_P5V_AUX_V", "CriticalLow": 3852, "CriticalHigh": 6347, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/78-0043/hwmon/hwmon*/in1_input", "Address": "dc-i2c-78-43"},
    {"Sensor": "CPU_P3V3_STBY_V", "CriticalLow": 2682, "CriticalHigh": 4004, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/78-0043/hwmon/hwmon*/in2_input", "Address": "dc-i2c-78-43"},
    {"Sensor": "CPU_P1V7_VCCSCFUSESUS_V", "CriticalLow": 1377, "CriticalHigh": 2057, "gettype": "sysfs", "Unit": "mV",
        "location": "/sys/bus/i2c/devices/78-0043/hwmon/hwmon*/in3_input", "Address": "dc-i2c-78-43"},
]

FRUS_STATUS = {
    "fans": [
        {"name": "   FAN1 present status:", "bus": 92, "loc": 0x0d, "presentloc": 0x30, 'presentbit': 0,
         'childfans': [
                {"name": "front motor status", "statusloc": 0x31, 'statusbit': 0},
                {"name": "rear motor status", "statusloc": 0x34, 'statusbit': 0}
         ]},
        {"name": "    FAN2 present status:", "bus": 101, "loc": 0x0d, "presentloc": 0x30, 'presentbit': 0,
            'childfans': [
                {"name": "front motor status", "statusloc": 0x31, 'statusbit': 0},
                {"name": "rear motor status", "statusloc": 0x34, 'statusbit': 0}
            ]},
        {"name": "    FAN3 present status:", "bus": 92, "loc": 0x0d, "presentloc": 0x30, 'presentbit': 1,
            'childfans': [
                {"name": "front motor status", "statusloc": 0x31, 'statusbit': 1},
                {"name": "rear motor status", "statusloc": 0x34, 'statusbit': 1}
            ]},
        {"name": "    FAN4 present status:", "bus": 101, "loc": 0x0d, "presentloc": 0x30, 'presentbit': 1,
            'childfans': [
                {"name": "front motor status", "statusloc": 0x31, 'statusbit': 1},
                {"name": "rear motor status", "statusloc": 0x34, 'statusbit': 1}
            ]},
        {"name": "    FAN5 present status:", "bus": 92, "loc": 0x0d, "presentloc": 0x30, 'presentbit': 2,
            'childfans': [
                {"name": "front motor status", "statusloc": 0x31, 'statusbit': 2},
                {"name": "rear motor status", "statusloc": 0x34, 'statusbit': 2}
         ]},
        {"name": "    FAN6 present status:", "bus": 101, "loc": 0x0d, "presentloc": 0x30, 'presentbit': 2,
            'childfans': [
                {"name": "front motor status", "statusloc": 0x31, 'statusbit': 2},
                {"name": "rear motor status", "statusloc": 0x34, 'statusbit': 2}
         ]},
        {"name": "    FAN7 present status:", "bus": 92, "loc": 0x0d, "presentloc": 0x30, 'presentbit': 3,
            'childfans': [
                {"name": "front motor status", "statusloc": 0x31, 'statusbit': 3},
                {"name": "rear motor status", "statusloc": 0x34, 'statusbit': 3}
         ]},
        {"name": "    FAN8 present status:", "bus": 101, "loc": 0x0d, "presentloc": 0x30, 'presentbit': 3,
            'childfans': [
                {"name": "front motor status", "statusloc": 0x31, 'statusbit': 3},
                {"name": "rear motor status", "statusloc": 0x34, 'statusbit': 3}
         ]},
    ],
    "psus": [
        {"name": "psu1", "io_addr": 0x91c, "gettype": "io", 'presentbit': 0, 'statusbit': 1, 'alertbit': 2},
        {"name": "psu2", "io_addr": 0x91c, "gettype": "io", 'presentbit': 4, 'statusbit': 5, 'alertbit': 6},
        {"name": "psu3", "io_addr": 0x91d, "gettype": "io", 'presentbit': 4, 'statusbit': 5, 'alertbit': 6},
        {"name": "psu4", "io_addr": 0x91d, "gettype": "io", 'presentbit': 0, 'statusbit': 1, 'alertbit': 2},
    ],
    "psupmbus": [
        {"name": "psu1", "values":
            [
                {"location": "/sys/bus/i2c/devices/83-0058/hwmon/*/curr1_input",
                    "displayname": "Input Current", 'name': 'iin', 'unit': 'A', 'min': 0.01, 'max': 7.2},
                {"location": "/sys/bus/i2c/devices/83-0058/hwmon/*/in1_input",
                    "displayname": "Input voltage", 'name': 'vin', 'unit': 'V', 'min': 180, 'max': 300},
                {"location": "/sys/bus/i2c/devices/83-0058/hwmon/*/in2_input",
                    "displayname": "Output voltage", 'name': 'vout1', 'unit': 'V', 'min': 11.4, 'max': 12.6},
                {"location": "/sys/bus/i2c/devices/83-0058/hwmon/*/curr2_input",
                    "displayname": "Output Current", 'name': 'iout1', 'unit': 'A', 'min': 1, 'max': 45},
                {"location": "/sys/bus/i2c/devices/83-0058/hwmon/*/temp1_input",
                    "displayname": "PSU Temperature", 'name': 'temp1', 'unit': 'C', 'min': -20, 'max': 65},
                {"location": "/sys/bus/i2c/devices/83-0058/hwmon/*/fan1_input",
                    "displayname": "PSU Fan Speed", 'name': 'fan1', 'unit': 'RPM', 'min': 500, 'max': 32000},
                {"location": "/sys/bus/i2c/devices/83-0058/hwmon/*/power1_input",
                 "displayname": "Input Power", 'name': 'pin', 'unit': 'W', 'min': 10, 'max': 550},
                {"location": "/sys/bus/i2c/devices/83-0058/hwmon/*/power2_input",
                 "displayname": "Output Power", 'name': 'pout1', 'unit': 'W', 'min': 10, 'max': 550},
            ]
         },
        {"name": "psu2", "values":
            [
                {"location": "/sys/bus/i2c/devices/84-0058/hwmon/*/curr1_input",
                    "displayname": "Input Current", 'name': 'iin', 'unit': 'A', 'min': 0.01, 'max': 7.2},
                {"location": "/sys/bus/i2c/devices/84-0058/hwmon/*/in1_input",
                    "displayname": "Input voltage", 'name': 'vin', 'unit': 'V', 'min': 180, 'max': 300},
                {"location": "/sys/bus/i2c/devices/84-0058/hwmon/*/in2_input",
                    "displayname": "Output voltage", 'name': 'vout1', 'unit': 'V', 'min': 11.4, 'max': 12.6},
                {"location": "/sys/bus/i2c/devices/84-0058/hwmon/*/curr2_input",
                    "displayname": "Output Current", 'name': 'iout1', 'unit': 'A', 'min': 1, 'max': 45},
                {"location": "/sys/bus/i2c/devices/84-0058/hwmon/*/temp1_input",
                    "displayname": "PSU Temperature", 'name': 'temp1', 'unit': 'C', 'min': -20, 'max': 65},
                {"location": "/sys/bus/i2c/devices/84-0058/hwmon/*/fan1_input",
                    "displayname": "PSU Fan Speed", 'name': 'fan1', 'unit': 'RPM', 'min': 500, 'max': 32000},
                {"location": "/sys/bus/i2c/devices/84-0058/hwmon/*/power1_input",
                    "displayname": "Input Power", 'name': 'pin', 'unit': 'W', 'min': 10, 'max': 550},
                {"location": "/sys/bus/i2c/devices/84-0058/hwmon/*/power2_input",
                 "displayname": "Output Power", 'name': 'pout1', 'unit': 'W', 'min': 10, 'max': 550},
            ]
         },
        {"name": "psu3", "values":
            [
                {"location": "/sys/bus/i2c/devices/86-0058/hwmon/*/curr1_input",
                    "displayname": "Input Current", 'name': 'iin', 'unit': 'A', 'min': 0.01, 'max': 7.2},
                {"location": "/sys/bus/i2c/devices/86-0058/hwmon/*/in1_input",
                    "displayname": "Input voltage", 'name': 'vin', 'unit': 'V', 'min': 180, 'max': 300},
                {"location": "/sys/bus/i2c/devices/86-0058/hwmon/*/in2_input",
                    "displayname": "Output voltage", 'name': 'vout1', 'unit': 'V', 'min': 11.4, 'max': 12.6},
                {"location": "/sys/bus/i2c/devices/86-0058/hwmon/*/curr2_input",
                    "displayname": "Output Current", 'name': 'iout1', 'unit': 'A', 'min': 1, 'max': 45},
                {"location": "/sys/bus/i2c/devices/86-0058/hwmon/*/temp1_input",
                    "displayname": "PSU Temperature", 'name': 'temp1', 'unit': 'C', 'min': -20, 'max': 65},
                {"location": "/sys/bus/i2c/devices/86-0058/hwmon/*/fan1_input",
                    "displayname": "PSU Fan Speed", 'name': 'fan1', 'unit': 'RPM', 'min': 500, 'max': 32000},
                {"location": "/sys/bus/i2c/devices/86-0058/hwmon/*/power1_input",
                    "displayname": "Input Power", 'name': 'pin', 'unit': 'W', 'min': 10, 'max': 550},
                {"location": "/sys/bus/i2c/devices/86-0058/hwmon/*/power2_input",
                 "displayname": "Output Power", 'name': 'pout1', 'unit': 'W', 'min': 10, 'max': 550},
            ]
         },
        {"name": "psu4", "values":
            [
                {"location": "/sys/bus/i2c/devices/85-0058/hwmon/*/curr1_input",
                    "displayname": "Input Current", 'name': 'iin', 'unit': 'A', 'min': 0.01, 'max': 7.2},
                {"location": "/sys/bus/i2c/devices/85-0058/hwmon/*/in1_input",
                    "displayname": "Input voltage", 'name': 'vin', 'unit': 'V', 'min': 180, 'max': 300},
                {"location": "/sys/bus/i2c/devices/85-0058/hwmon/*/in2_input",
                    "displayname": "Output voltage", 'name': 'vout1', 'unit': 'V', 'min': 11.4, 'max': 12.6},
                {"location": "/sys/bus/i2c/devices/85-0058/hwmon/*/curr2_input",
                    "displayname": "Output Current", 'name': 'iout1', 'unit': 'A', 'min': 1, 'max': 45},
                {"location": "/sys/bus/i2c/devices/85-0058/hwmon/*/temp1_input",
                    "displayname": "PSU Temperature", 'name': 'temp1', 'unit': 'C', 'min': -20, 'max': 65},
                {"location": "/sys/bus/i2c/devices/85-0058/hwmon/*/fan1_input",
                    "displayname": "PSU Fan Speed", 'name': 'fan1', 'unit': 'RPM', 'min': 500, 'max': 32000},
                {"location": "/sys/bus/i2c/devices/85-0058/hwmon/*/power1_input",
                    "displayname": "Input Power", 'name': 'pin', 'unit': 'W', 'min': 10, 'max': 550},
                {"location": "/sys/bus/i2c/devices/85-0058/hwmon/*/power2_input",
                 "displayname": "Output Power", 'name': 'pout1', 'unit': 'W', 'min': 10, 'max': 550},
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

BIOS_STATUS = {'gettype': 'io', 'io_addr': 0x0727, 'bitmask': 0x01}
BIOS_STATUS_DECODE = {1: 'master', 0: 'slave'}

FPGA_VERSION_INFO = [
    {"name": "version", "pcibus": 8, "slot": 0, "fn": 0, "bar": 0, "offset": 0, "gettype": "pci"},
    {"name": "date", "pcibus": 8, "slot": 0, "fn": 0, "bar": 0, "offset": 4, "gettype": "pci"},
    {"name": "golden version", "pcibus": 8, "slot": 0, "fn": 0, "bar": 0, "offset": 12, "gettype": "pci"},
]

# 内存条丝印
MEM_SLOTS = ["J14", "", "J12", ""]

FAN_PROTECT = [
    {"bus": 92, "devno": 0x0d, "addr": 0x19, "open": 0x00, "close": 0xff},
    {"bus": 101, "devno": 0x0d, "addr": 0x19, "open": 0x00, "close": 0xff},
]
rg_eeprom = "1-0056/eeprom"
E2_LOC = {"bus": 1, "devno": 0x56}
E2_PROTECT = {"io_addr": 0x941, "gettype": "io", "open": 0xfe, "close": 0xff}

CPLDVERSIONS = [
    {"io_addr": 0x0700, "name": "CPU_CPLD", "gettype": "io"},
    {"io_addr": 0x0900, "name": "BASE_CPLD", "gettype": "io"},
    {"bus": 109, "devno": 0x1d, "name": "MAC_CPLDA"},
    {"bus": 110, "devno": 0x2d, "name": "MAC_CPLDB"},
    {"bus": 111, "devno": 0x3d, "name": "PORT_CPLDA"},
    {"bus": 112, "devno": 0x4d, "name": "PORT_CPLDB"},
    {"bus": 92, "devno": 0x0d, "name": "FAN_CPLDA"},
    {"bus": 101, "devno": 0x0d, "name": "FAN_CPLDB"}
]


TEMPS_DEFINE = {
    "boards": [
        {"location": "/sys/bus/i2c/devices/79-004b/hwmon/*/temp1_input", "displayname": "INLET_TEMP_0x4b"},
        {"location": "/sys/bus/i2c/devices/117-004b/hwmon/*/temp1_input", "displayname": "MAC_TEMP_0x4b"},
        {"location": "/sys/bus/i2c/devices/118-004f/hwmon/*/temp1_input", "displayname": "MAC_TEMP_0x4f"},
        {"location": "/sys/bus/i2c/devices/93-0048/hwmon/*/temp1_input", "displayname": "OUTLET_TEMP1_0x48"},
        {"location": "/sys/bus/i2c/devices/94-0049/hwmon/*/temp1_input", "displayname": "OUTLET_TEMP1_0x49"},
        {"location": "/sys/bus/i2c/devices/102-0048/hwmon/*/temp1_input", "displayname": "OUTLET_TEMP2_0x48"},
        {"location": "/sys/bus/i2c/devices/103-0049/hwmon/*/temp1_input", "displayname": "OUTLET_TEMP2_0x49"},
    ],
    "cpu": '/sys/class/hwmon/hwmon0',
    "mac": [
        {"location": "/sys/bus/i2c/devices/122-0044/hwmon/hwmon*/temp1_input", "displayname": "MAC_DIE_0"},
        {"location": "/sys/bus/i2c/devices/122-0044/hwmon/hwmon*/temp2_input", "displayname": "MAC_DIE_1"},
        {"location": "/sys/bus/i2c/devices/122-0044/hwmon/hwmon*/temp3_input", "displayname": "MAC_DIE_2"},
        {"location": "/sys/bus/i2c/devices/122-0044/hwmon/hwmon*/temp4_input", "displayname": "MAC_DIE_3"},
        {"location": "/sys/bus/i2c/devices/122-0044/hwmon/hwmon*/temp5_input", "displayname": "MAC_DIE_4"},
        {"location": "/sys/bus/i2c/devices/122-0044/hwmon/hwmon*/temp6_input", "displayname": "MAC_DIE_5"},
        {"location": "/sys/bus/i2c/devices/122-0044/hwmon/hwmon*/temp7_input", "displayname": "MAC_DIE_6"},
        {"location": "/sys/bus/i2c/devices/122-0044/hwmon/hwmon*/temp8_input", "displayname": "MAC_DIE_7"},
        {"location": "/sys/bus/i2c/devices/122-0044/hwmon/hwmon*/temp9_input", "displayname": "MAC_DIE_8"},
        {"location": "/sys/bus/i2c/devices/122-0044/hwmon/hwmon*/temp10_input", "displayname": "MAC_DIE_9"},
        {"location": "/sys/bus/i2c/devices/122-0044/hwmon/hwmon*/temp11_input", "displayname": "MAC_DIE_10"},
        {"location": "/sys/bus/i2c/devices/122-0044/hwmon/hwmon*/temp12_input", "displayname": "MAC_DIE_11"},
        {"location": "/sys/bus/i2c/devices/122-0044/hwmon/hwmon*/temp13_input", "displayname": "MAC_DIE_12"},
        {"location": "/sys/bus/i2c/devices/122-0044/hwmon/hwmon*/temp14_input", "displayname": "MAC_DIE_13"},
        {"location": "/sys/bus/i2c/devices/122-0044/hwmon/hwmon*/temp15_input", "displayname": "MAC_DIE_14"},
    ],
}

PSU_MODEL_MAP = {
    "GW-CRPS1300D": "RG-PA1200-F",
    "DPS-1300AB-6 S": "RG-PA1200-F",
}

OPTOE_PORT_MAP = {
    "port_num": 64,
    "optoe_start_bus": 133,
}

ECC_CMD = [
    {"cmd" : "/usr/local/bin/dfd_debug phymem_rd 4 0x8ffa2104 16", "keyword" : ["0x8ffa2100", "0x8ffa2110"], "check_len" : 16},
    {"cmd" : "/usr/local/bin/dfd_debug phymem_rd 4 0x8ffa3104 16", "keyword" : ["0x8ffa3100", "0x8ffa3110"], "check_len" : 16},
]

FACTESTMODULE = {
    "bmc_diag": 0,
    "mgmttest": 1,
    "bmcsetmac": 0,
    "sysinfo_showhw": 1,  # 默认为1
    "sensord": 1,
    "fancontrol_stop": 0,
    "firmware_check": 1,
    "fpga_show": 1,
    "bmcinit": 1,
    "show_device_mac": 1,
    #"show_config_ver": 1,
    "eeprom_pn_sn_show": 1,
}

I2C_SCAN_LIST = [
    {"addr": 0x56, "name": "ONIE TLV E2(1-0x56)", "bus": 1},
    {"addr": 0x57, "name": "CPU E2(1-0x57)", "bus": 1},
    {"addr": 0x5b, "name": "CPU UCD90160(77-0x5b)", "bus": 77},
    {"addr": 0x43, "name": "CPU INA3221(78-0x43)", "bus": 78},
    {"addr": 0x67, "name": "CPU TPS53622RSBT/VCCIN/P1V05(78-0x67)", "bus": 78},
    {"addr": 0x6C, "name": "CPU TPS53622RSBT/P1V2_VDDQ(78-0x6c)", "bus": 78},
    {"addr": 0x4b, "name": "CPU LM75_0(79-0x4b)", "bus": 79},
    {"addr": 0x50, "name": "PSU1(PMBUS)(83-0x50)", "bus": 83},
    {"addr": 0x58, "name": "PSU1(FRU EEPROM)(83-0x58)", "bus": 83},
    {"addr": 0x50, "name": "PSU2(PMBUS)(84-0x50)", "bus": 84},
    {"addr": 0x58, "name": "PSU2(FRU EEPROM)(84-0x58)", "bus": 84},
    {"addr": 0x50, "name": "PSU3(PMBUS)(86-0x50)", "bus": 86},
    {"addr": 0x58, "name": "PSU3(FRU EEPROM)(86-0x58)", "bus": 86},
    {"addr": 0x50, "name": "PSU4(PMBUS)(85-0x50)", "bus": 85},
    {"addr": 0x58, "name": "PSU4(FRU EEPROM)(85-0x58)", "bus": 85},
    {"addr": 0x0D, "name": "FAN CPLD_1(92-0x0d)", "bus": 92},
    {"addr": 0x48, "name": "FAN LM75_1_0(93-0x48)", "bus": 93},
    {"addr": 0x49, "name": "FAN LM75_1_1(94-0x49)", "bus": 94},
    {"addr": 0x50, "name": "FAN FAN1(95-0x50)", "bus": 95},
    {"addr": 0x50, "name": "FAN FAN3(96-0x50)", "bus": 96},
    {"addr": 0x50, "name": "FAN FAN5(97-0x50)", "bus": 97},
    {"addr": 0x50, "name": "FAN FAN7(98-0x50)", "bus": 98},
    {"addr": 0x0D, "name": "FAN CPLD_2(101-0x0d)", "bus": 101},
    {"addr": 0x48, "name": "FAN LM75_2_0(102-0x48)", "bus": 102},
    {"addr": 0x49, "name": "FAN LM75_2_1(103-0x49)", "bus":103},
    {"addr": 0x50, "name": "FAN FAN2(104-0x50)", "bus": 104},
    {"addr": 0x50, "name": "FAN FAN4(105-0x50)", "bus": 105},
    {"addr": 0x50, "name": "FAN FAN6(106-0x50)", "bus": 106},
    {"addr": 0x50, "name": "FAN FAN8(107-0x50)", "bus": 107},
    {"addr": 0x1d, "name": "MAC CPLDA(109-0x1d)", "bus": 109},
    {"addr": 0x2d, "name": "MAC CPLDB(110-0x2d)", "bus": 110},
    {"addr": 0x3d, "name": "PORT CPLDA(111-0x3d)", "bus": 111},
    {"addr": 0x4d, "name": "PORT CPLDB(112-0x4d)", "bus": 112},
    {"addr": 0x4B, "name": "MAC LM75_0(117-0x4b)", "bus": 117},
    {"addr": 0x4F, "name": "MAC LM75_1(118-0x4f)", "bus": 118},
    {"addr": 0x4C, "name": "MAC TMP411ADGKT_0(119-0x4c)", "bus": 119},
    {"addr": 0x4C, "name": "MAC TMP411ADGKT_1(120-0x4c)", "bus": 120},
    {"addr": 0x44, "name": "MAC BSC_TH4(122-0x44)", "bus": 122},
    {"addr": 0x40, "name": "MAC_CORE(PMBUS)(126-0x40)", "bus": 126},
    {"addr": 0x10, "name": "MAC_CORE(I2C)(126-0x10)", "bus": 126},
    {"addr": 0x40, "name": "MAC_ANALOG(PMBUS)(127-0x40)", "bus": 127},
    {"addr": 0x10, "name": "MAC_ANALOG(I2C)(127-0x10)", "bus": 127},
    {"addr": 0x5b, "name": "MAC UCD90160_A(128-0x5b)", "bus": 128},
    {"addr": 0x5b, "name": "MAC UCD90160_B(129-0x5b)", "bus": 129},
    {"addr": 0x5b, "name": "PORT UCD90160(130-0x5b)", "bus": 130},
    {"addr": 0x67, "name": "MAC TPS53622(131-0x67)", "bus":131},
]

LED_NEW = {
    "fanleds": {
        "attrs": OrderedDict([("灭", 0x00), ("黄灯亮", 0x06), ("绿灯亮", 0x04), ("红灯亮", 0x02), ]),
        "name": "FAN1/2/3/4/5/6灯",
        "device": [
            {"bus": 4, "addr": 0x3d, "reg": 0x41},
            {"bus": 4, "addr": 0x3d, "reg": 0x40},
            {"bus": 4, "addr": 0x3d, "reg": 0x3f},
            {"bus": 4, "addr": 0x3d, "reg": 0x3e},
            {"bus": 4, "addr": 0x3d, "reg": 0x3d},
            {"bus": 4, "addr": 0x3d, "reg": 0x3c},
        ]
    },
    "sysleds": {
        "attrs": OrderedDict([("灭", 0x00), ("黄灯亮", 0x06), ("红灯亮", 0x02), ("绿灯亮", 0x04), ]),
        "name": "系统LED测试(SYS,BMC,PSU,FAN)",
        "device": [
            {"bus": 2, "addr": 0x2d, "reg": 0x47},
            {"bus": 2, "addr": 0x2d, "reg": 0x4a},
            {"bus": 2, "addr": 0x2d, "reg": 0x49},
        ]
    },
    "portleds_r": {
        "attrs": OrderedDict([("红灯亮", 0xff), ("恢复", 0x00), ]),
        "name": "端口灯红灯测试",
        "device": [
            {"bus": 2, "addr": 0x1d, "reg": 0x3c},
            {"bus": 2, "addr": 0x1d, "reg": 0x3d},
            {"bus": 2, "addr": 0x1d, "reg": 0x3e},
            {"bus": 2, "addr": 0x1d, "reg": 0x3f},
            {"bus": 2, "addr": 0x2d, "reg": 0x3b},
            {"bus": 2, "addr": 0x2d, "reg": 0x3c},
            {"bus": 2, "addr": 0x2d, "reg": 0x3d},
            {"bus": 2, "addr": 0x2d, "reg": 0x3e},
        ]
    },
}

FAN_LOWRATIO = 40
FAN_MIDRATIO = 60
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
    "mgmt_kt_ports": {"eth1": 38, "eth2": 78},  # 内部管理口对应的unit_port
    "prbs_port_range": "1-37,40-74",  # 面板口unit_port范围(不包含mgmt口和loopback口)
    "extphy_device": 0,  # 是否是有外部phy的设备(是 : 1, 不是 : 0)
    "prbs_ber": 1.0e-6,  # prbs测试允许的误码率
    "prbs_time": 120,  # prbs测试时间 (通常为120s/180s)
    "prbs_ber_dict": {
        1: "1.00E-06",
        2: "1.00E-06",
        3: "1.00E-06",
        4: "1.00E-06",
        5: "1.00E-06",
        6: "1.00E-06",
        7: "1.00E-06",
        8: "1.00E-06",
        9: "1.00E-06",
        10: "1.00E-06",
        11: "1.00E-06",
        12: "1.00E-06",
        13: "1.00E-06",
        14: "1.00E-06",
        15: "1.00E-06",
        16: "1.00E-06",
        17: "1.00E-06",
        18: "1.00E-06",
        19: "1.00E-06",
        20: "1.00E-06",
        21: "1.00E-06",
        22: "1.00E-06",
        23: "1.00E-06",
        24: "1.00E-06",
        25: "1.00E-06",
        26: "1.00E-06",
        27: "1.00E-06",
        28: "1.00E-06",
        29: "1.00E-06",
        30: "1.00E-06",
        31: "1.00E-06",
        32: "1.00E-06",
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
    {"pci_addr": "00:00.0", "dev_id": "8086:6f00"},
    {"pci_addr": "00:01.0", "dev_id": "8086:6f02"},
    {"pci_addr": "00:01.1", "dev_id": "8086:6f03"},
    {"pci_addr": "00:02.0", "dev_id": "8086:6f04"},
    {"pci_addr": "00:02.2", "dev_id": "8086:6f06"},
    {"pci_addr": "00:02.3", "dev_id": "8086:6f07"},
    {"pci_addr": "00:03.0", "dev_id": "8086:6f08"},
    {"pci_addr": "00:03.1", "dev_id": "8086:6f09"},
    {"pci_addr": "00:03.2", "dev_id": "8086:6f0a"},
    {"pci_addr": "00:03.3", "dev_id": "8086:6f0b"},
    {"pci_addr": "00:04.0", "dev_id": "8086:6f20"},
    {"pci_addr": "00:04.1", "dev_id": "8086:6f21"},
    {"pci_addr": "00:04.2", "dev_id": "8086:6f22"},
    {"pci_addr": "00:04.3", "dev_id": "8086:6f23"},
    {"pci_addr": "00:04.4", "dev_id": "8086:6f24"},
    {"pci_addr": "00:04.5", "dev_id": "8086:6f25"},
    {"pci_addr": "00:04.6", "dev_id": "8086:6f26"},
    {"pci_addr": "00:04.7", "dev_id": "8086:6f27"},
    {"pci_addr": "00:05.0", "dev_id": "8086:6f28"},
    {"pci_addr": "00:05.1", "dev_id": "8086:6f29"},
    {"pci_addr": "00:05.2", "dev_id": "8086:6f2a"},
    {"pci_addr": "00:05.4", "dev_id": "8086:6f2c"},
    {"pci_addr": "00:14.0", "dev_id": "8086:8c31"},
    {"pci_addr": "00:16.0", "dev_id": "8086:8c3a", "ignore": 1},
    {"pci_addr": "00:16.1", "dev_id": "8086:8c3b", "ignore": 1},
    {"pci_addr": "00:1d.0", "dev_id": "8086:8c26"},
    {"pci_addr": "00:1f.0", "dev_id": "8086:8c54"},
    {"pci_addr": "00:1f.2", "dev_id": "8086:8c02"},
    {"pci_addr": "00:1f.3", "dev_id": "8086:8c22"},
    {"pci_addr": "04:00.0", "dev_id": "8086:15ab"},
    {"pci_addr": "04:00.1", "dev_id": "8086:15ab"},
    {"pci_addr": "05:00.0", "dev_id": "8086:15ab"},
    {"pci_addr": "05:00.1", "dev_id": "8086:15ab"},
    {"pci_addr": "06:00.0", "dev_id": "14e4:b990"},
    {"pci_addr": "07:00.0", "dev_id": "8086:1533"},
    {"pci_addr": "08:00.0", "dev_id": "10ee:7011"},
    {"pci_addr": "ff:0b.0", "dev_id": "8086:6f81"},
    {"pci_addr": "ff:0b.1", "dev_id": "8086:6f36"},
    {"pci_addr": "ff:0b.2", "dev_id": "8086:6f37"},
    {"pci_addr": "ff:0b.3", "dev_id": "8086:6f76"},
    {"pci_addr": "ff:0c.0", "dev_id": "8086:6fe0"},
    {"pci_addr": "ff:0c.1", "dev_id": "8086:6fe1"},
    {"pci_addr": "ff:0c.2", "dev_id": "8086:6fe2"},
    {"pci_addr": "ff:0c.3", "dev_id": "8086:6fe3"},
    {"pci_addr": "ff:0f.0", "dev_id": "8086:6ff8"},
    {"pci_addr": "ff:0f.4", "dev_id": "8086:6ffc"},
    {"pci_addr": "ff:0f.5", "dev_id": "8086:6ffd"},
    {"pci_addr": "ff:0f.6", "dev_id": "8086:6ffe"},
    {"pci_addr": "ff:10.0", "dev_id": "8086:6f1d"},
    {"pci_addr": "ff:10.1", "dev_id": "8086:6f34"},
    {"pci_addr": "ff:10.5", "dev_id": "8086:6f1e"},
    {"pci_addr": "ff:10.6", "dev_id": "8086:6f7d"},
    {"pci_addr": "ff:10.7", "dev_id": "8086:6f1f"},
    {"pci_addr": "ff:12.0", "dev_id": "8086:6fa0"},
    {"pci_addr": "ff:12.1", "dev_id": "8086:6f30"},
    {"pci_addr": "ff:13.0", "dev_id": "8086:6fa8"},
    {"pci_addr": "ff:13.1", "dev_id": "8086:6f71"},
    {"pci_addr": "ff:13.2", "dev_id": "8086:6faa"},
    {"pci_addr": "ff:13.3", "dev_id": "8086:6fab"},
    {"pci_addr": "ff:13.4", "dev_id": "8086:6fac"},
    {"pci_addr": "ff:13.5", "dev_id": "8086:6fad"},
    {"pci_addr": "ff:13.6", "dev_id": "8086:6fae"},
    {"pci_addr": "ff:13.7", "dev_id": "8086:6faf"},
    {"pci_addr": "ff:14.0", "dev_id": "8086:6fb0"},
    {"pci_addr": "ff:14.1", "dev_id": "8086:6fb1"},
    {"pci_addr": "ff:14.2", "dev_id": "8086:6fb2"},
    {"pci_addr": "ff:14.3", "dev_id": "8086:6fb3"},
    {"pci_addr": "ff:14.4", "dev_id": "8086:6fbc"},
    {"pci_addr": "ff:14.5", "dev_id": "8086:6fbd"},
    {"pci_addr": "ff:14.6", "dev_id": "8086:6fbe"},
    {"pci_addr": "ff:14.7", "dev_id": "8086:6fbf"},
    {"pci_addr": "ff:15.0", "dev_id": "8086:6fb4"},
    {"pci_addr": "ff:15.1", "dev_id": "8086:6fb5"},
    {"pci_addr": "ff:15.2", "dev_id": "8086:6fb6"},
    {"pci_addr": "ff:15.3", "dev_id": "8086:6fb7"},
    {"pci_addr": "ff:1e.0", "dev_id": "8086:6f98"},
    {"pci_addr": "ff:1e.1", "dev_id": "8086:6f99"},
    {"pci_addr": "ff:1e.2", "dev_id": "8086:6f9a"},
    {"pci_addr": "ff:1e.3", "dev_id": "8086:6fc0"},
    {"pci_addr": "ff:1e.4", "dev_id": "8086:6f9c"},
    {"pci_addr": "ff:1f.0", "dev_id": "8086:6f88"},
    {"pci_addr": "ff:1f.2", "dev_id": "8086:6f8a"},
]

PCIe_SPEED_ITEM = [
    {"dev_desc": "I210", "PCIe_name": "I210", },
    {"dev_desc": "MAC", "PCIe_name": "Broadcom", },
    {"dev_desc": "FPGA", "PCIe_name": "Xilinx", },
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

# test menu
MENU_ID_ROOT = 0
MENU_ID_SIGNLE_TEST = 1
MENU_ID_DEVICE_REST = 6
MENU_ID_CPU_TEST = 11
MENU_ID_BMC_TEST = 12
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
MENU_ID_CONFIG = 7
MENU_ID_SETMAC = 71
MENU_ID_FIRMWARE = 72
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
test_fan_status_item = {"name": "FAN status test", "deal": "test_fan_status"}
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
    test_sys_part_item, #sdk version
    test_temp_item, #mac temp other temp
    test_dcdc_item,
    test_fan_eeprom_item,
    test_fan_status_item,
    test_fan_speed_item,
    test_psu_eeprom_item,
    test_power_status_item,
    test_power_pmbus_item,
    test_sff_present_status_item, # 光模块在位和状态检测
    test_rtc_date_item,
    test_ssd_smart_item,
    test_ssd_smart_attr_item,
    test_ssd_smart_health_item,
    test_sata_abnormal_item,
    test_pcie_scan_item, #带宽检测
    test_i2c_item,
    test_cpld_item,
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
   # "onie_build_date":"2023-11-01T03:17+0000",
    "bios_vendor":"American Megatrends Inc.",
    "bios_version":"5.14(3CNHU022)",
    "bios_release_date":"01/19/2022",
    "cpld_check":{
        "CPU_CPLD":"15210511",
        "BASE_CPLD":"10210813",
        "MAC_CPLDA":"10210806",
        "MAC_CPLDB":"10210806",
        "PORT_CPLDA":"10210806",
        "PORT_CPLDB":"10210806",
        "FAN_CPLDA":"10210806",
        "FAN_CPLDB":"10210806",
    },
    "fpga_check":{
        "version":"0x7a500810",
    },
    #"sdk_version":"sdk-6.5.28 built 20231212 (Tue Dec 12 15:03:59 2023)",
    "PCIe FW loader version":"2.10",
    "PCIe FW version":"D000_05",
    "PCIe FW loader built date":"20210311",
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
   # "switch_cpld_gpio": SwitchCpldGpio,
    "sdkcmdversion": 0,  # 0bcmcmd  1bcmcmdb
    #"SetEnv5387": SetEnv5387,
    "FanLowLevel": FAN_LOWRATIO,
    "FanHighLevel": FAN_HIGHRATIO,
    "open_fpga_i2c_access": open_fpga_i2c_access,
    "smi_access": SMI_ACCESS,
    "ssd_slot_num": 2,
    "temps": TEMPS_DEFINE,
    "BIOS_TEST": BIOS_TEST,
    "frustatus": FRUS_STATUS,
    'setmacsnlen': SETMAC_SN_LEN,
    'psu_model_map': PSU_MODEL_MAP,
    'optoe_port_map': OPTOE_PORT_MAP,
    "dcdcsensor": DCDC_LIST,
    "frustatusdecode": FRUS_STATUS_DECODE,
    "biosstatus": BIOS_STATUS,
    "biosstatusdecode": BIOS_STATUS_DECODE,
    "FPGA_INFO": FPGA_VERSION_INFO,
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
        {"name": "BASE_CPLD", "io_addr": 0x0900, "addr": 0x55, "gettype": "io", "testval": [0x55, 0xaa]},
        {"name": "FAN_CPLDA", "bus": 92, "devno": 0x0d, "addr": 0xaa, "testval": [0x55, 0xaa]},
        {"name": "FAN_CPLDA", "bus": 101, "devno": 0x0d, "addr": 0xaa, "testval": [0x55, 0xaa]},
        {"name": "MAC_CPLDA", "bus": 109, "devno": 0x1d, "addr": 0xaa, "testval": [0x55, 0xaa]},
        {"name": "MAC_CPLDB", "bus": 110, "devno": 0x2d, "addr": 0xaa, "testval": [0x55, 0xaa]},
        {"name": "PORT_CPLDA", "bus": 111, "devno": 0x3d, "addr": 0xaa, "testval": [0x55, 0xaa]},
        {"name": "PORT_CPLDB", "bus": 112, "devno": 0x4d, "addr": 0xaa, "testval": [0x55, 0xaa]},
    ],
    "FPGATEST": [
        {"name": "MAC FPGA", "path": "/dev/fpga0", "offset": 0x8, "gettype": "devfile", "value": [0x55, 0xaa, 0x5a, 0xa5], "read_len":4},
        {"name": "PORT FPGA", "path": "/dev/fpga1", "offset": 0x8, "gettype": "devfile", "value": [0x55, 0xaa, 0x5a, 0xa5], "read_len":4}
    ],
    "LED_NEWS": LED_NEW,
    "I2CSCAN": I2C_SCAN_LIST,
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
    "VERSIONTEST": [
        {"name": "MAC VR PSU:", "bus": 126, "devno": 0x10, "addr": 0x76},
    ],
    "EthernetNum": 32,
    "Ethernet_LIST": ['Ethernet0', 'Ethernet4', 'Ethernet8', 'Ethernet12', 'Ethernet16', 'Ethernet20', 'Ethernet24', 'Ethernet28',
                       'Ethernet32', 'Ethernet36', 'Ethernet40', 'Ethernet44', 'Ethernet48', 'Ethernet52', 'Ethernet56', 'Ethernet60',
                       'Ethernet64', 'Ethernet68', 'Ethernet72', 'Ethernet76', 'Ethernet80', 'Ethernet84', 'Ethernet88', 'Ethernet92', 
                       'Ethernet96', 'Ethernet100', 'Ethernet108', 'Ethernet116', 'Ethernet124', 'Ethernet132', 'Ethernet140', 'Ethernet148'],
}

alltest = []
looptest = []
