#coding:utf-8

"""
   配置说明
    首层目录表示 含有设备的类型：
            psus
            leds
            temps
            fans
            cards
            sensors
    第二层为列表[] 表示器件的组合 不区分先后顺序
            {
                e2loc : 表示带e2类型的
                pmbus : 表示PMBUS
            }
"""

psu_fan_airflow = {
    "F2B": ["DPS-1600AB-53 B", "GW-CRPS1600D2"],
    "B2F": ["DPS-1600AB-11 C", "CRPS1600D3R"]
}

psu_display_name = {
    "RG-PA1600II-F": ["DPS-1600AB-53 B", "GW-CRPS1600D2"],
    "RG-PA1600II-R": ["DPS-1600AB-11 C", "CRPS1600D3R"]
}

fanairflow = {
    "F2B": ["M2EFAN II-F"],
}

fan_display_name = {
    "M2EFAN II-F": ["M2EFAN II-F"],
}

psutypedecode = {
    0x00: 'N/A',
    0x01: 'AC',
    0x02: 'DC',
}

class Unit:
    Temperature = "C"
    Voltage = "V"
    Current = "A"
    Power =  "W"
    Speed = "RPM"

class threshold:
    PSU_TEMP_MIN = -10 * 1000
    PSU_TEMP_MAX = 60 * 1000

    PSU_FAN_SPEED_MIN = 2000
    PSU_FAN_SPEED_MAX = 18000

    PSU_OUTPUT_VOLTAGE_MIN = 11.4 * 1000
    PSU_OUTPUT_VOLTAGE_MAX = 12.6 * 1000

    PSU_AC_INPUT_VOLTAGE_MIN = 180 * 1000
    PSU_AC_INPUT_VOLTAGE_MAX = 264 * 1000

    PSU_DC_INPUT_VOLTAGE_MIN = 180 * 1000
    PSU_DC_INPUT_VOLTAGE_MAX = 300 * 1000

    ERR_VALUE = -9999999

    PSU_OUTPUT_POWER_MIN = 0 * 1000 * 1000
    PSU_OUTPUT_POWER_MAX = 1600 * 1000 * 1000

    PSU_INPUT_POWER_MIN = 0 * 1000 * 1000
    PSU_INPUT_POWER_MAX = 2500 * 1000 * 1000

    PSU_OUTPUT_CURRENT_MIN = 0 * 1000
    PSU_OUTPUT_CURRENT_MAX = 134.1 * 1000

    PSU_INPUT_CURRENT_MIN = 0 * 1000
    PSU_INPUT_CURRENT_MAX = 10 * 1000

    FAN_SPEED_MAX = 13000
    FAN_SPEED_MIN = 2000

devices = {
    "onie_e2": [
        {
            "name": "ONIE_E2",
            "e2loc": {"loc": "/sys/bus/i2c/devices/1-0056/eeprom", "way": "sysfs"},
        },
    ],
    "psus": [
        {
            "e2loc": {"bus": 95, "addr": 0x50,  "way":"i2c"},
            "pmbusloc": {"bus": 95, "addr": 0x58,  "way":"i2c"},
            "present" : {"loc":"/sys/rg_plat/psu/psu1/present","way":"sysfs", "mask": 0x01, "okval": 1},
            "name": "PSU1",
            "airflow" :psu_fan_airflow,
            "psu_display_name": psu_display_name,
            "TempStatus":{"bus": 95, "addr": 0x58,  "offset":0x79, "way":"i2cword", "mask": 0x0004},
            "Temperature": {
                           "value": {"loc":"/sys/bus/i2c/devices/i2c-95/95-0058/hwmon/hwmon*/temp1_input","way":"sysfs"},
                           "Min": threshold.PSU_TEMP_MIN,
                           "Max": threshold.PSU_TEMP_MAX,
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                          },
            "FanStatus":{"bus": 95, "addr": 0x58,  "offset":0x79, "way":"i2cword", "mask": 0x0400},
            "FanSpeed" : {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-95/95-0058/hwmon/hwmon*/fan1_input","way":"sysfs"},
                         "Min": threshold.PSU_FAN_SPEED_MIN,
                         "Max": threshold.PSU_FAN_SPEED_MAX,
                         "Unit": Unit.Speed
                          },
            "InputsStatus":{"bus": 95, "addr": 0x58,  "offset":0x79, "way":"i2cword", "mask": 0x2000},
            "InputsType":{"bus": 95, "addr": 0x58,  "offset":0x80, "way":"i2c", 'psutypedecode':psutypedecode},
            "InputsVoltage": {
                            'AC': {
                                "value":{"loc":"/sys/bus/i2c/devices/i2c-95/95-0058/hwmon/hwmon*/in1_input","way":"sysfs"},
                                "Min": threshold.PSU_AC_INPUT_VOLTAGE_MIN ,
                                "Max": threshold.PSU_AC_INPUT_VOLTAGE_MAX,
                                "Unit": Unit.Voltage,
                                "format":"float(float(%s)/1000)"

                            },
                            'DC': {
                                "value":{"loc":"/sys/bus/i2c/devices/i2c-95/95-0058/hwmon/hwmon*/in1_input","way":"sysfs"},
                                "Min": threshold.PSU_DC_INPUT_VOLTAGE_MIN ,
                                "Max": threshold.PSU_DC_INPUT_VOLTAGE_MAX,
                                "Unit": Unit.Voltage,
                                "format":"float(float(%s)/1000)"
                            },
                            'other': {
                                "value":{"loc":"/sys/bus/i2c/devices/i2c-95/95-0058/hwmon/hwmon*/in1_input","way":"sysfs"},
                                "Min": threshold.ERR_VALUE,
                                "Max": threshold.ERR_VALUE,
                                "Unit": Unit.Voltage,
                                "format":"float(float(%s)/1000)"
                            }
                        },
            "InputsCurrent":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-95/95-0058/hwmon/hwmon*/curr1_input","way":"sysfs"},
                         "Min": threshold.PSU_INPUT_CURRENT_MIN,
                         "Max": threshold.PSU_INPUT_CURRENT_MAX,
                         "Unit": Unit.Current,
                         "format":"float(float(%s)/1000)"
                          },
            "InputsPower":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-95/95-0058/hwmon/hwmon*/power1_input","way":"sysfs"},
                         "Min": threshold.PSU_INPUT_POWER_MIN,
                         "Max": threshold.PSU_INPUT_POWER_MAX,
                         "Unit": Unit.Power,
                         "format":"float(float(%s)/1000000)"
                          },
            "OutputsStatus":{"bus": 95, "addr": 0x58,  "offset":0x79, "way":"i2cword", "mask": 0x8800},
            "OutputsVoltage":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-95/95-0058/hwmon/hwmon*/in2_input","way":"sysfs"},
                         "Min": threshold.PSU_OUTPUT_VOLTAGE_MIN,
                         "Max": threshold.PSU_OUTPUT_VOLTAGE_MAX,
                         "Unit": Unit.Voltage,
                         "format":"float(float(%s)/1000)"
                          },
            "OutputsCurrent":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-95/95-0058/hwmon/hwmon*/curr2_input","way":"sysfs"},
                         "Min": threshold.PSU_OUTPUT_CURRENT_MIN,
                         "Max": threshold.PSU_OUTPUT_CURRENT_MAX,
                         "Unit": Unit.Current,
                         "format":"float(float(%s)/1000)"
                          },
            "OutputsPower":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-95/95-0058/hwmon/hwmon*/power2_input","way":"sysfs"},
                         "Min": threshold.PSU_OUTPUT_POWER_MIN,
                         "Max": threshold.PSU_OUTPUT_POWER_MAX,
                         "Unit": Unit.Power,
                         "format":"float(float(%s)/1000000)"
                          },
        },
        {
            "e2loc": {"bus": 96, "addr": 0x50,  "way":"i2c"},
            "pmbusloc": {"bus": 96, "addr": 0x58,  "way":"i2c"},
            "present" : {"loc":"/sys/rg_plat/psu/psu2/present","way":"sysfs", "mask": 0x01, "okval": 1},
            "name": "PSU2",
            "airflow" :psu_fan_airflow,
            "psu_display_name": psu_display_name,
            "TempStatus":{"bus": 96, "addr": 0x58,  "offset":0x79, "way":"i2cword", "mask": 0x0004},
            "Temperature": {
                           "value": {"loc":"/sys/bus/i2c/devices/i2c-96/96-0058/hwmon/hwmon*/temp1_input","way":"sysfs"},
                           "Min": threshold.PSU_TEMP_MIN,
                           "Max": threshold.PSU_TEMP_MAX,
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                          },
            "FanStatus":{"bus": 96, "addr": 0x58,  "offset":0x79, "way":"i2cword", "mask": 0x0400},
            "FanSpeed" : {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-96/96-0058/hwmon/hwmon*/fan1_input","way":"sysfs"},
                         "Min": threshold.PSU_FAN_SPEED_MIN,
                         "Max": threshold.PSU_FAN_SPEED_MAX,
                         "Unit": Unit.Speed
                          },
            "InputsStatus":{"bus": 96, "addr": 0x58,  "offset":0x79, "way":"i2cword", "mask": 0x2000},
            "InputsType":{"bus": 96, "addr": 0x58,  "offset":0x80, "way":"i2c", 'psutypedecode':psutypedecode},
            "InputsVoltage": {
                            'AC': {
                                "value":{"loc":"/sys/bus/i2c/devices/i2c-96/96-0058/hwmon/hwmon*/in1_input","way":"sysfs"},
                                "Min": threshold.PSU_AC_INPUT_VOLTAGE_MIN ,
                                "Max": threshold.PSU_AC_INPUT_VOLTAGE_MAX,
                                "Unit": Unit.Voltage,
                                "format":"float(float(%s)/1000)"

                            },
                            'DC': {
                                "value":{"loc":"/sys/bus/i2c/devices/i2c-96/96-0058/hwmon/hwmon*/in1_input","way":"sysfs"},
                                "Min": threshold.PSU_DC_INPUT_VOLTAGE_MIN ,
                                "Max": threshold.PSU_DC_INPUT_VOLTAGE_MAX,
                                "Unit": Unit.Voltage,
                                "format":"float(float(%s)/1000)"
                            },
                            'other': {
                                "value":{"loc":"/sys/bus/i2c/devices/i2c-96/96-0058/hwmon/hwmon*/in1_input","way":"sysfs"},
                                "Min": threshold.ERR_VALUE,
                                "Max": threshold.ERR_VALUE,
                                "Unit": Unit.Voltage,
                                "format":"float(float(%s)/1000)"
                            }
                        },
            "InputsCurrent":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-96/96-0058/hwmon/hwmon*/curr1_input","way":"sysfs"},
                         "Min": threshold.PSU_INPUT_CURRENT_MIN,
                         "Max": threshold.PSU_INPUT_CURRENT_MAX,
                         "Unit": Unit.Current,
                         "format":"float(float(%s)/1000)"
                          },
            "InputsPower":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-96/96-0058/hwmon/hwmon*/power1_input","way":"sysfs"},
                         "Min": threshold.PSU_INPUT_POWER_MIN,
                         "Max": threshold.PSU_INPUT_POWER_MAX,
                         "Unit": Unit.Power,
                         "format":"float(float(%s)/1000000)"
                          },
            "OutputsStatus":{"bus": 96, "addr": 0x58,  "offset":0x79, "way":"i2cword", "mask": 0x8800},
            "OutputsVoltage":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-96/96-0058/hwmon/hwmon*/in2_input","way":"sysfs"},
                         "Min": threshold.PSU_OUTPUT_VOLTAGE_MIN,
                         "Max": threshold.PSU_OUTPUT_VOLTAGE_MAX,
                         "Unit": Unit.Voltage,
                         "format":"float(float(%s)/1000)"
                          },
            "OutputsCurrent":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-96/96-0058/hwmon/hwmon*/curr2_input","way":"sysfs"},
                         "Min": threshold.PSU_OUTPUT_CURRENT_MIN,
                         "Max": threshold.PSU_OUTPUT_CURRENT_MAX,
                         "Unit": Unit.Current,
                         "format":"float(float(%s)/1000)"
                          },
            "OutputsPower":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-96/96-0058/hwmon/hwmon*/power2_input","way":"sysfs"},
                         "Min": threshold.PSU_OUTPUT_POWER_MIN,
                         "Max": threshold.PSU_OUTPUT_POWER_MAX,
                         "Unit": Unit.Power,
                         "format":"float(float(%s)/1000000)"
                          },
        },
        {
            "e2loc": {"bus": 97, "addr": 0x50,  "way":"i2c"},
            "pmbusloc": {"bus": 97, "addr": 0x58,  "way":"i2c"},
            "present" : {"loc":"/sys/rg_plat/psu/psu3/present","way":"sysfs", "mask": 0x01, "okval": 1},
            "name": "PSU3",
            "airflow" :psu_fan_airflow,
            "psu_display_name": psu_display_name,
            "TempStatus":{"bus": 97, "addr": 0x58,  "offset":0x79, "way":"i2cword", "mask": 0x0004},
            "Temperature": {
                           "value": {"loc":"/sys/bus/i2c/devices/i2c-97/97-0058/hwmon/hwmon*/temp1_input","way":"sysfs"},
                           "Min": threshold.PSU_TEMP_MIN,
                           "Max": threshold.PSU_TEMP_MAX,
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                          },
            "FanStatus":{"bus": 97, "addr": 0x58,  "offset":0x79, "way":"i2cword", "mask": 0x0400},
            "FanSpeed" : {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-97/97-0058/hwmon/hwmon*/fan1_input","way":"sysfs"},
                         "Min": threshold.PSU_FAN_SPEED_MIN,
                         "Max": threshold.PSU_FAN_SPEED_MAX,
                         "Unit": Unit.Speed
                          },
            "InputsStatus":{"bus": 97, "addr": 0x58,  "offset":0x79, "way":"i2cword", "mask": 0x2000},
            "InputsType":{"bus": 97, "addr": 0x58,  "offset":0x80, "way":"i2c", 'psutypedecode':psutypedecode},
            "InputsVoltage": {
                            'AC': {
                                "value":{"loc":"/sys/bus/i2c/devices/i2c-97/97-0058/hwmon/hwmon*/in1_input","way":"sysfs"},
                                "Min": threshold.PSU_AC_INPUT_VOLTAGE_MIN ,
                                "Max": threshold.PSU_AC_INPUT_VOLTAGE_MAX,
                                "Unit": Unit.Voltage,
                                "format":"float(float(%s)/1000)"

                            },
                            'DC': {
                                "value":{"loc":"/sys/bus/i2c/devices/i2c-97/97-0058/hwmon/hwmon*/in1_input","way":"sysfs"},
                                "Min": threshold.PSU_DC_INPUT_VOLTAGE_MIN ,
                                "Max": threshold.PSU_DC_INPUT_VOLTAGE_MAX,
                                "Unit": Unit.Voltage,
                                "format":"float(float(%s)/1000)"
                            },
                            'other': {
                                "value":{"loc":"/sys/bus/i2c/devices/i2c-97/97-0058/hwmon/hwmon*/in1_input","way":"sysfs"},
                                "Min": threshold.ERR_VALUE,
                                "Max": threshold.ERR_VALUE,
                                "Unit": Unit.Voltage,
                                "format":"float(float(%s)/1000)"
                            }
                        },
            "InputsCurrent":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-97/97-0058/hwmon/hwmon*/curr1_input","way":"sysfs"},
                         "Min": threshold.PSU_INPUT_CURRENT_MIN,
                         "Max": threshold.PSU_INPUT_CURRENT_MAX,
                         "Unit": Unit.Current,
                         "format":"float(float(%s)/1000)"
                          },
            "InputsPower":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-97/97-0058/hwmon/hwmon*/power1_input","way":"sysfs"},
                         "Min": threshold.PSU_INPUT_POWER_MIN,
                         "Max": threshold.PSU_INPUT_POWER_MAX,
                         "Unit": Unit.Power,
                         "format":"float(float(%s)/1000000)"
                          },
            "OutputsStatus":{"bus": 97, "addr": 0x58,  "offset":0x79, "way":"i2cword", "mask": 0x8800},
            "OutputsVoltage":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-97/97-0058/hwmon/hwmon*/in2_input","way":"sysfs"},
                         "Min": threshold.PSU_OUTPUT_VOLTAGE_MIN,
                         "Max": threshold.PSU_OUTPUT_VOLTAGE_MAX,
                         "Unit": Unit.Voltage,
                         "format":"float(float(%s)/1000)"
                          },
            "OutputsCurrent":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-97/97-0058/hwmon/hwmon*/curr2_input","way":"sysfs"},
                         "Min": threshold.PSU_OUTPUT_CURRENT_MIN,
                         "Max": threshold.PSU_OUTPUT_CURRENT_MAX,
                         "Unit": Unit.Current,
                         "format":"float(float(%s)/1000)"
                          },
            "OutputsPower":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-97/97-0058/hwmon/hwmon*/power2_input","way":"sysfs"},
                         "Min": threshold.PSU_OUTPUT_POWER_MIN,
                         "Max": threshold.PSU_OUTPUT_POWER_MAX,
                         "Unit": Unit.Power,
                         "format":"float(float(%s)/1000000)"
                          },
        },
        {
            "e2loc": {"bus": 98, "addr": 0x50,  "way":"i2c"},
            "pmbusloc": {"bus": 98, "addr": 0x58,  "way":"i2c"},
            "present" : {"loc":"/sys/rg_plat/psu/psu4/present","way":"sysfs", "mask": 0x01, "okval": 1},
            "name": "PSU4",
            "airflow" :psu_fan_airflow,
            "psu_display_name": psu_display_name,
            "TempStatus":{"bus": 98, "addr": 0x58,  "offset":0x79, "way":"i2cword", "mask": 0x0004},
            "Temperature": {
                           "value": {"loc":"/sys/bus/i2c/devices/i2c-98/98-0058/hwmon/hwmon*/temp1_input","way":"sysfs"},
                           "Min": threshold.PSU_TEMP_MIN,
                           "Max": threshold.PSU_TEMP_MAX,
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                          },
            "FanStatus":{"bus": 98, "addr": 0x58,  "offset":0x79, "way":"i2cword", "mask": 0x0400},
            "FanSpeed" : {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-98/98-0058/hwmon/hwmon*/fan1_input","way":"sysfs"},
                         "Min": threshold.PSU_FAN_SPEED_MIN,
                         "Max": threshold.PSU_FAN_SPEED_MAX,
                         "Unit": Unit.Speed
                          },
            "InputsStatus":{"bus": 98, "addr": 0x58,  "offset":0x79, "way":"i2cword", "mask": 0x2000},
            "InputsType":{"bus": 98, "addr": 0x58,  "offset":0x80, "way":"i2c", 'psutypedecode':psutypedecode},
            "InputsVoltage": {
                            'AC': {
                                "value":{"loc":"/sys/bus/i2c/devices/i2c-98/98-0058/hwmon/hwmon*/in1_input","way":"sysfs"},
                                "Min": threshold.PSU_AC_INPUT_VOLTAGE_MIN ,
                                "Max": threshold.PSU_AC_INPUT_VOLTAGE_MAX,
                                "Unit": Unit.Voltage,
                                "format":"float(float(%s)/1000)"

                            },
                            'DC': {
                                "value":{"loc":"/sys/bus/i2c/devices/i2c-98/98-0058/hwmon/hwmon*/in1_input","way":"sysfs"},
                                "Min": threshold.PSU_DC_INPUT_VOLTAGE_MIN ,
                                "Max": threshold.PSU_DC_INPUT_VOLTAGE_MAX,
                                "Unit": Unit.Voltage,
                                "format":"float(float(%s)/1000)"
                            },
                            'other': {
                                "value":{"loc":"/sys/bus/i2c/devices/i2c-98/98-0058/hwmon/hwmon*/in1_input","way":"sysfs"},
                                "Min": threshold.ERR_VALUE,
                                "Max": threshold.ERR_VALUE,
                                "Unit": Unit.Voltage,
                                "format":"float(float(%s)/1000)"
                            }
                        },
            "InputsCurrent":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-98/98-0058/hwmon/hwmon*/curr1_input","way":"sysfs"},
                         "Min": threshold.PSU_INPUT_CURRENT_MIN,
                         "Max": threshold.PSU_INPUT_CURRENT_MAX,
                         "Unit": Unit.Current,
                         "format":"float(float(%s)/1000)"
                          },
            "InputsPower":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-98/98-0058/hwmon/hwmon*/power1_input","way":"sysfs"},
                         "Min": threshold.PSU_INPUT_POWER_MIN,
                         "Max": threshold.PSU_INPUT_POWER_MAX,
                         "Unit": Unit.Power,
                         "format":"float(float(%s)/1000000)"
                          },
            "OutputsStatus":{"bus": 98, "addr": 0x58,  "offset":0x79, "way":"i2cword", "mask": 0x8800},
            "OutputsVoltage":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-98/98-0058/hwmon/hwmon*/in2_input","way":"sysfs"},
                         "Min": threshold.PSU_OUTPUT_VOLTAGE_MIN,
                         "Max": threshold.PSU_OUTPUT_VOLTAGE_MAX,
                         "Unit": Unit.Voltage,
                         "format":"float(float(%s)/1000)"
                          },
            "OutputsCurrent":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-98/98-0058/hwmon/hwmon*/curr2_input","way":"sysfs"},
                         "Min": threshold.PSU_OUTPUT_CURRENT_MIN,
                         "Max": threshold.PSU_OUTPUT_CURRENT_MAX,
                         "Unit": Unit.Current,
                         "format":"float(float(%s)/1000)"
                          },
            "OutputsPower":
                    {
                         "value":{"loc":"/sys/bus/i2c/devices/i2c-98/98-0058/hwmon/hwmon*/power2_input","way":"sysfs"},
                         "Min": threshold.PSU_OUTPUT_POWER_MIN,
                         "Max": threshold.PSU_OUTPUT_POWER_MAX,
                         "Unit": Unit.Power,
                         "format":"float(float(%s)/1000000)"
                          },
        }
    ],
    "temps":[
        {
            "name": "SWITCH_TEMP",
            "Temperature": {
                           "value": {"loc":"/sys/rg_plat/sensor/temp1/temp_input","way":"sysfs"},
                           "Min": -30000,
                           "Max": 105000,
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
           }
        },
        {
            "name": "INLET_TEMP",
            "Temperature": {
                           "value": [
                                {"loc":"/sys/bus/i2c/devices/123-004b/hwmon/hwmon*/temp1_input","way":"sysfs"},
                                {"loc":"/sys/bus/i2c/devices/124-004b/hwmon/hwmon*/temp1_input","way":"sysfs"},
                            ],
                           "Min": -30000,
                           "Max": 55000,
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                }
        },
        {
            "name": "OUTLET_TEMP",
            "Temperature": {
                           "value": [
                                {"loc":"/sys/bus/i2c/devices/104-004b/hwmon/hwmon*/temp1_input","way":"sysfs"},
                                {"loc":"/sys/bus/i2c/devices/112-004b/hwmon/hwmon*/temp1_input","way":"sysfs"},
                            ],
                           "Min": -30000,
                           "Max": 75000,
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                }
        },
        {
            "name": "CPU_TEMP",
            "Temperature": {
                           "value": {"loc":"/sys/bus/platform/devices/coretemp.0/hwmon/hwmon*/temp1_input","way":"sysfs"},
                           "Min": -30000,
                           "Max": 102000,
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                }
        },
        {
            "name": "SFF_TEMP",
            "Temperature": {
                           "value": {"loc":"/tmp/highest_sff_temp","way":"sysfs", "flock_path": "/tmp/highest_sff_temp"},
                           "Min": -15000,
                           "Max": 100000,
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                }
        },
        {
            "name": "MGMT_AIR_INLET_1",
            "Temperature": {
                           "value": {"loc":"/sys/bus/i2c/devices/123-004b/hwmon/*/temp1_input","way":"sysfs"},
                           "Max": {"loc":"/sys/bus/i2c/devices/123-004b/hwmon/*/temp1_max","way":"sysfs"},
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                }
        },
        {
            "name": "MGMT_AIR_INLET_2",
            "Temperature": {
                           "value": {"loc":"/sys/bus/i2c/devices/124-004b/hwmon/*/temp1_input","way":"sysfs"},
                           "Max": {"loc":"/sys/bus/i2c/devices/124-004b/hwmon/*/temp1_max","way":"sysfs"},
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                }
        },
        {
            "name": "UPORT_AIR_INLET",
            "Temperature": {
                           "value": {"loc":"/sys/bus/i2c/devices/65-004b/hwmon/*/temp1_input","way":"sysfs"},
                           "Max": {"loc":"/sys/bus/i2c/devices/65-004b/hwmon/*/temp1_max","way":"sysfs"},
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                }
        },
        {
            "name": "DPORT_AIR_INLET",
            "Temperature": {
                           "value": {"loc":"/sys/bus/i2c/devices/130-004b/hwmon/*/temp1_input","way":"sysfs"},
                           "Max": {"loc":"/sys/bus/i2c/devices/130-004b/hwmon/*/temp1_max","way":"sysfs"},
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                }
        },
        {
            "name": "MAC_AIR_INLET_1",
            "Temperature": {
                           "value": {"loc":"/sys/bus/i2c/devices/71-004b/hwmon/*/temp1_input","way":"sysfs"},
                           "Max": {"loc":"/sys/bus/i2c/devices/71-004b/hwmon/*/temp1_max","way":"sysfs"},
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                }
        },
        {
            "name": "MAC_AIR_INLET_2",
            "Temperature": {
                           "value": {"loc":"/sys/bus/i2c/devices/72-004f/hwmon/*/temp1_input","way":"sysfs"},
                           "Max": {"loc":"/sys/bus/i2c/devices/72-004f/hwmon/*/temp1_max","way":"sysfs"},
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                }
        },
        {
            "name": "UPORT_FAN_AIR_OUTLET",
            "Temperature": {
                           "value": {"loc":"/sys/bus/i2c/devices/104-004b/hwmon/*/temp1_input","way":"sysfs"},
                           "Max": {"loc":"/sys/bus/i2c/devices/104-004b/hwmon/*/temp1_max","way":"sysfs"},
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                }
        },
        {
            "name": "DPORT_FAN_AIR_OUTLET",
            "Temperature": {
                           "value": {"loc":"/sys/bus/i2c/devices/112-004b/hwmon/*/temp1_input","way":"sysfs"},
                           "Max": {"loc":"/sys/bus/i2c/devices/112-004b/hwmon/*/temp1_max","way":"sysfs"},
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                }
        },
        {
            "name": "BOARD_TEMP",
            "Temperature": {
                           "value": [
                                {"loc":"/sys/bus/i2c/devices/72-004f/hwmon/hwmon*/temp1_input", "way":"sysfs"},
                                {},
                            ],
                           "Min":-30000,
                           "Max": 75000,
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                }
        },
        {
            "name": "MOS_TEMP",
            "Temperature": {
                           "value": [
                                {"loc":"/sys/bus/i2c/devices/81-0040/hwmon/hwmon*/temp1_input", "way":"sysfs"},
                                {},
                            ],
                           "Min":-30000,
                           "Max": 125000,
                           "Unit": Unit.Temperature,
                           "format":"float(float(%s)/1000)"
                }
        },
    ],
    "leds": [
        {
            "name": "FRONT_SYS_LED",
            "led": {"loc": "/dev/cpld1", "offset":0xd2, "way":"devfile", "len": 1},
            "led_attrs" : {
                           "green":0x04, "red":0x02, "yellow":0x06, "default":0x04,
                           "flash":0xff, "light":0xff, "off": 0, "mask":0xff
                          },
        },
        {
            "name": "FRONT_PSU_LED",
            "led": {"loc": "/dev/cpld1", "offset":0xd3, "way":"devfile", "len": 1},
            "led_attrs" : {
                           "green":0x04, "red":0x02, "yellow":0x06, "default":0x04,
                           "flash":0xff, "light":0xff, "off": 0, "mask":0xff
                          },
        },
        {
            "name": "FRONT_FAN_LED",
            "led": {"loc": "/dev/cpld1", "offset":0xd4, "way":"devfile", "len": 1},
            "led_attrs" : {
                           "green":0x04, "red":0x02, "yellow":0x06, "default":0x04,
                           "flash":0xff, "light":0xff, "off": 0, "mask":0xff
                          },
        },
    ],
    "fans": [
        {
            "name": "FAN1",
            "airflow" : fanairflow,
            "fan_display_name": fan_display_name,
            "e2loc": {'loc': '/sys/bus/i2c/devices/i2c-105/105-0050/eeprom', 'offset': 0, 'len': 256, 'way': 'devfile'},
            "present" : {"loc":"/sys/rg_plat/fan/fan1/present","way":"sysfs", "mask": 0x01, "okval": 1},
            "SpeedMin" : threshold.FAN_SPEED_MIN,
            "SpeedMax" : threshold.FAN_SPEED_MAX,
            "led": {"bus": 103, "addr": 0x0d,  "offset":0xd0, "way":"i2c"},
            "led_attrs" : {
                           "green":0x04, "red":0x02, "yellow":0x06, "default":0x04,
                           "flash":0xff, "light":0xff, "off": 0, "mask":0xff
                          },
            "Rotor": {
                        "Rotor1_config": {  "name": "Rotor1",
                                            "Set_speed" : {"bus": 103, "addr": 0x0d,  "offset":0x90, "way":"i2c"},
                                            "Running": {"loc":"/sys/rg_plat/fan/fan1/motor0/status","way":"sysfs", "mask": 0x01, "is_runing": 1},
                                            "HwAlarm": {"loc":"/sys/rg_plat/fan/fan1/motor0/status","way":"sysfs", "mask": 0x01, "no_alarm": 1},
                                            "SpeedMin": threshold.FAN_SPEED_MIN,
                                            "SpeedMax": threshold.FAN_SPEED_MAX,
                                            "Speed": {
                                                        "value": {"loc": "/sys/rg_plat/fan/fan1/motor0/speed", "way": "sysfs"},
                                                        "Min": threshold.FAN_SPEED_MIN,
                                                        "Max": threshold.FAN_SPEED_MAX,
                                                        "Unit": Unit.Speed,
                                                    },
                                           },
                        "Rotor2_config": {
                                            "name": "Rotor2",
                                            "Set_speed" : {"bus": 103, "addr": 0x0d,  "offset":0x90, "way":"i2c"},
                                            "Running": {"loc":"/sys/rg_plat/fan/fan1/motor1/status","way":"sysfs", "mask": 0x01, "is_runing": 1},
                                            "HwAlarm": {"loc":"/sys/rg_plat/fan/fan1/motor1/status","way":"sysfs", "mask": 0x01, "no_alarm": 1},
                                            "SpeedMin": threshold.FAN_SPEED_MIN,
                                            "SpeedMax": threshold.FAN_SPEED_MAX,
                                            "Speed": {
                                                        "value": {"loc": "/sys/rg_plat/fan/fan1/motor1/speed", "way": "sysfs"},
                                                        "Min": threshold.FAN_SPEED_MIN,
                                                        "Max": threshold.FAN_SPEED_MAX,
                                                        "Unit": Unit.Speed,
                                                    },
                                           },
                },
        },
        {
            "name": "FAN2",
            "airflow" : fanairflow,
            "fan_display_name": fan_display_name,
            "e2loc": {'loc': '/sys/bus/i2c/devices/i2c-113/113-0050/eeprom', 'offset': 0, 'len': 256, 'way': 'devfile'},
            "present" : {"loc":"/sys/rg_plat/fan/fan2/present","way":"sysfs", "mask": 0x01, "okval": 1},
            "SpeedMin" : threshold.FAN_SPEED_MIN,
            "SpeedMax" : threshold.FAN_SPEED_MAX,
            "led": {"bus": 111, "addr": 0x0d,  "offset":0xd0, "way":"i2c"},
            "led_attrs" : {
                           "green":0x04, "red":0x02, "yellow":0x06, "default":0x04,
                           "flash":0xff, "light":0xff, "off": 0, "mask":0xff
                          },
            "Rotor": {
                        "Rotor1_config": {  "name": "Rotor1",
                                            "Set_speed" : {"bus": 111, "addr": 0x0d,  "offset":0x90, "way":"i2c"},
                                            "Running": {"loc":"/sys/rg_plat/fan/fan2/motor0/status","way":"sysfs", "mask": 0x01, "is_runing": 1},
                                            "HwAlarm": {"loc":"/sys/rg_plat/fan/fan2/motor0/status","way":"sysfs", "mask": 0x01, "no_alarm": 1},
                                            "SpeedMin": threshold.FAN_SPEED_MIN,
                                            "SpeedMax": threshold.FAN_SPEED_MAX,
                                            "Speed": {
                                                        "value": {"loc": "/sys/rg_plat/fan/fan2/motor0/speed", "way": "sysfs"},
                                                        "Min": threshold.FAN_SPEED_MIN,
                                                        "Max": threshold.FAN_SPEED_MAX,
                                                        "Unit": Unit.Speed,
                                                    },
                                           },
                        "Rotor2_config": {
                                            "name": "Rotor2",
                                            "Set_speed" : {"bus": 111, "addr": 0x0d,  "offset":0x90, "way":"i2c"},
                                            "Running": {"loc":"/sys/rg_plat/fan/fan2/motor1/status","way":"sysfs", "mask": 0x01, "is_runing": 1},
                                            "HwAlarm": {"loc":"/sys/rg_plat/fan/fan2/motor1/status","way":"sysfs", "mask": 0x01, "no_alarm": 1},
                                            "SpeedMin": threshold.FAN_SPEED_MIN,
                                            "SpeedMax": threshold.FAN_SPEED_MAX,
                                            "Speed": {
                                                        "value": {"loc": "/sys/rg_plat/fan/fan2/motor1/speed", "way": "sysfs"},
                                                        "Min": threshold.FAN_SPEED_MIN,
                                                        "Max": threshold.FAN_SPEED_MAX,
                                                        "Unit": Unit.Speed,
                                                    },
                                           },
                },
        },
        {
            "name": "FAN3",
            "airflow" : fanairflow,
            "fan_display_name": fan_display_name,
            "e2loc": {'loc': '/sys/bus/i2c/devices/i2c-106/106-0050/eeprom', 'offset': 0, 'len': 256, 'way': 'devfile'},
            "present" : {"loc":"/sys/rg_plat/fan/fan3/present","way":"sysfs", "mask": 0x01, "okval": 1},
            "SpeedMin" : threshold.FAN_SPEED_MIN,
            "SpeedMax" : threshold.FAN_SPEED_MAX,
            "led": {"bus": 103, "addr": 0x0d,  "offset":0xd1, "way":"i2c"},
            "led_attrs" : {
                           "green":0x04, "red":0x02, "yellow":0x06, "default":0x04,
                           "flash":0xff, "light":0xff, "off": 0, "mask":0xff
                          },
            "Rotor": {
                        "Rotor1_config": {  "name": "Rotor1",
                                            "Set_speed" : {"bus": 103, "addr": 0x0d,  "offset":0x91, "way":"i2c"},
                                            "Running": {"loc":"/sys/rg_plat/fan/fan3/motor0/status","way":"sysfs", "mask": 0x01, "is_runing": 1},
                                            "HwAlarm": {"loc":"/sys/rg_plat/fan/fan3/motor0/status","way":"sysfs", "mask": 0x01, "no_alarm": 1},
                                            "SpeedMin": threshold.FAN_SPEED_MIN,
                                            "SpeedMax": threshold.FAN_SPEED_MAX,
                                            "Speed": {
                                                        "value": {"loc": "/sys/rg_plat/fan/fan3/motor0/speed", "way": "sysfs"},
                                                        "Min": threshold.FAN_SPEED_MIN,
                                                        "Max": threshold.FAN_SPEED_MAX,
                                                        "Unit": Unit.Speed,
                                                    },
                                           },
                        "Rotor2_config": {
                                            "name": "Rotor2",
                                            "Set_speed" : {"bus": 103, "addr": 0x0d,  "offset":0x91, "way":"i2c"},
                                            "Running": {"loc":"/sys/rg_plat/fan/fan3/motor1/status","way":"sysfs", "mask": 0x01, "is_runing": 1},
                                            "HwAlarm": {"loc":"/sys/rg_plat/fan/fan3/motor1/status","way":"sysfs", "mask": 0x01, "no_alarm": 1},
                                            "SpeedMin": threshold.FAN_SPEED_MIN,
                                            "SpeedMax": threshold.FAN_SPEED_MAX,
                                            "Speed": {
                                                        "value": {"loc": "/sys/rg_plat/fan/fan3/motor1/speed", "way": "sysfs"},
                                                        "Min": threshold.FAN_SPEED_MIN,
                                                        "Max": threshold.FAN_SPEED_MAX,
                                                        "Unit": Unit.Speed,
                                                    },
                                           },
                },
        },
        {
            "name": "FAN4",
            "airflow" : fanairflow,
            "fan_display_name": fan_display_name,
            "e2loc": {'loc': '/sys/bus/i2c/devices/i2c-114/114-0050/eeprom', 'offset': 0, 'len': 256, 'way': 'devfile'},
            "present" : {"loc":"/sys/rg_plat/fan/fan4/present","way":"sysfs", "mask": 0x01, "okval": 1},
            "SpeedMin" : threshold.FAN_SPEED_MIN,
            "SpeedMax" : threshold.FAN_SPEED_MAX,
            "led": {"bus": 111, "addr": 0x0d,  "offset":0xd1, "way":"i2c"},
            "led_attrs" : {
                           "green":0x04, "red":0x02, "yellow":0x06, "default":0x04,
                           "flash":0xff, "light":0xff, "off": 0, "mask":0xff
                          },
            "Rotor": {
                        "Rotor1_config": {  "name": "Rotor1",
                                            "Set_speed" : {"bus": 111, "addr": 0x0d,  "offset":0x91, "way":"i2c"},
                                            "Running": {"loc":"/sys/rg_plat/fan/fan4/motor0/status","way":"sysfs", "mask": 0x01, "is_runing": 1},
                                            "HwAlarm": {"loc":"/sys/rg_plat/fan/fan4/motor0/status","way":"sysfs", "mask": 0x01, "no_alarm": 1},
                                            "SpeedMin": threshold.FAN_SPEED_MIN,
                                            "SpeedMax": threshold.FAN_SPEED_MAX,
                                            "Speed": {
                                                        "value": {"loc": "/sys/rg_plat/fan/fan4/motor0/speed", "way": "sysfs"},
                                                        "Min": threshold.FAN_SPEED_MIN,
                                                        "Max": threshold.FAN_SPEED_MAX,
                                                        "Unit": Unit.Speed,
                                                    },
                                           },
                        "Rotor2_config": {
                                            "name": "Rotor2",
                                            "Set_speed" : {"bus": 111, "addr": 0x0d,  "offset":0x91, "way":"i2c"},
                                            "Running": {"loc":"/sys/rg_plat/fan/fan4/motor1/status","way":"sysfs", "mask": 0x01, "is_runing": 1},
                                            "HwAlarm": {"loc":"/sys/rg_plat/fan/fan4/motor1/status","way":"sysfs", "mask": 0x01, "no_alarm": 1},
                                            "SpeedMin": threshold.FAN_SPEED_MIN,
                                            "SpeedMax": threshold.FAN_SPEED_MAX,
                                            "Speed": {
                                                        "value": {"loc": "/sys/rg_plat/fan/fan4/motor1/speed", "way": "sysfs"},
                                                        "Min": threshold.FAN_SPEED_MIN,
                                                        "Max": threshold.FAN_SPEED_MAX,
                                                        "Unit": Unit.Speed,
                                                    },
                                           },
                },
        },
        {
            "name": "FAN5",
            "airflow" : fanairflow,
            "fan_display_name": fan_display_name,
            "e2loc": {'loc': '/sys/bus/i2c/devices/i2c-107/107-0050/eeprom', 'offset': 0, 'len': 256, 'way': 'devfile'},
            "present" : {"loc":"/sys/rg_plat/fan/fan5/present","way":"sysfs", "mask": 0x01, "okval": 1},
            "SpeedMin" : threshold.FAN_SPEED_MIN,
            "SpeedMax" : threshold.FAN_SPEED_MAX,
            "led": {"bus": 103, "addr": 0x0d,  "offset":0xd2, "way":"i2c"},
            "led_attrs" : {
                           "green":0x04, "red":0x02, "yellow":0x06, "default":0x04,
                           "flash":0xff, "light":0xff, "off": 0, "mask":0xff
                          },
            "Rotor": {
                        "Rotor1_config": {  "name": "Rotor1",
                                            "Set_speed" : {"bus": 103, "addr": 0x0d,  "offset":0x92, "way":"i2c"},
                                            "Running": {"loc":"/sys/rg_plat/fan/fan5/motor0/status","way":"sysfs", "mask": 0x01, "is_runing": 1},
                                            "HwAlarm": {"loc":"/sys/rg_plat/fan/fan5/motor0/status","way":"sysfs", "mask": 0x01, "no_alarm": 1},
                                            "SpeedMin": threshold.FAN_SPEED_MIN,
                                            "SpeedMax": threshold.FAN_SPEED_MAX,
                                            "Speed": {
                                                        "value": {"loc": "/sys/rg_plat/fan/fan5/motor0/speed", "way": "sysfs"},
                                                        "Min": threshold.FAN_SPEED_MIN,
                                                        "Max": threshold.FAN_SPEED_MAX,
                                                        "Unit": Unit.Speed,
                                                    },
                                           },
                        "Rotor2_config": {
                                            "name": "Rotor2",
                                            "Set_speed" : {"bus": 103, "addr": 0x0d,  "offset":0x92, "way":"i2c"},
                                            "Running": {"loc":"/sys/rg_plat/fan/fan5/motor1/status","way":"sysfs", "mask": 0x01, "is_runing": 1},
                                            "HwAlarm": {"loc":"/sys/rg_plat/fan/fan5/motor1/status","way":"sysfs", "mask": 0x01, "no_alarm": 1},
                                            "SpeedMin": threshold.FAN_SPEED_MIN,
                                            "SpeedMax": threshold.FAN_SPEED_MAX,
                                            "Speed": {
                                                        "value": {"loc": "/sys/rg_plat/fan/fan5/motor1/speed", "way": "sysfs"},
                                                        "Min": threshold.FAN_SPEED_MIN,
                                                        "Max": threshold.FAN_SPEED_MAX,
                                                        "Unit": Unit.Speed,
                                                    },
                                           },
                },
        },
        {
            "name": "FAN6",
            "airflow" : fanairflow,
            "fan_display_name": fan_display_name,
            "e2loc": {'loc': '/sys/bus/i2c/devices/i2c-115/115-0050/eeprom', 'offset': 0, 'len': 256, 'way': 'devfile'},
            "present" : {"loc":"/sys/rg_plat/fan/fan6/present","way":"sysfs", "mask": 0x01, "okval": 1},
            "SpeedMin" : threshold.FAN_SPEED_MIN,
            "SpeedMax" : threshold.FAN_SPEED_MAX,
            "led": {"bus": 111, "addr": 0x0d,  "offset":0xd2, "way":"i2c"},
            "led_attrs" : {
                           "green":0x04, "red":0x02, "yellow":0x06, "default":0x04,
                           "flash":0xff, "light":0xff, "off": 0, "mask":0xff
                          },
            "Rotor": {
                        "Rotor1_config": {  "name": "Rotor1",
                                            "Set_speed" : {"bus": 111, "addr": 0x0d,  "offset":0x92, "way":"i2c"},
                                            "Running": {"loc":"/sys/rg_plat/fan/fan6/motor0/status","way":"sysfs", "mask": 0x01, "is_runing": 1},
                                            "HwAlarm": {"loc":"/sys/rg_plat/fan/fan6/motor0/status","way":"sysfs", "mask": 0x01, "no_alarm": 1},
                                            "SpeedMin": threshold.FAN_SPEED_MIN,
                                            "SpeedMax": threshold.FAN_SPEED_MAX,
                                            "Speed": {
                                                        "value": {"loc": "/sys/rg_plat/fan/fan6/motor0/speed", "way": "sysfs"},
                                                        "Min": threshold.FAN_SPEED_MIN,
                                                        "Max": threshold.FAN_SPEED_MAX,
                                                        "Unit": Unit.Speed,
                                                    },
                                           },
                        "Rotor2_config": {
                                            "name": "Rotor2",
                                            "Set_speed" : {"bus": 111, "addr": 0x0d,  "offset":0x92, "way":"i2c"},
                                            "Running": {"loc":"/sys/rg_plat/fan/fan6/motor1/status","way":"sysfs", "mask": 0x01, "is_runing": 1},
                                            "HwAlarm": {"loc":"/sys/rg_plat/fan/fan6/motor1/status","way":"sysfs", "mask": 0x01, "no_alarm": 1},
                                            "SpeedMin": threshold.FAN_SPEED_MIN,
                                            "SpeedMax": threshold.FAN_SPEED_MAX,
                                            "Speed": {
                                                        "value": {"loc": "/sys/rg_plat/fan/fan6/motor1/speed", "way": "sysfs"},
                                                        "Min": threshold.FAN_SPEED_MIN,
                                                        "Max": threshold.FAN_SPEED_MAX,
                                                        "Unit": Unit.Speed,
                                                    },
                                           },
                },
        },
        {
            "name": "FAN7",
            "airflow" : fanairflow,
            "fan_display_name": fan_display_name,
            "e2loc": {'loc': '/sys/bus/i2c/devices/i2c-108/108-0050/eeprom', 'offset': 0, 'len': 256, 'way': 'devfile'},
            "present" : {"loc":"/sys/rg_plat/fan/fan7/present","way":"sysfs", "mask": 0x01, "okval": 1},
            "SpeedMin" : threshold.FAN_SPEED_MIN,
            "SpeedMax" : threshold.FAN_SPEED_MAX,
            "led": {"bus": 103, "addr": 0x0d,  "offset":0xd3, "way":"i2c"},
            "led_attrs" : {
                           "green":0x04, "red":0x02, "yellow":0x06, "default":0x04,
                           "flash":0xff, "light":0xff, "off": 0, "mask":0xff
                          },
            "Rotor": {
                        "Rotor1_config": {  "name": "Rotor1",
                                            "Set_speed" : {"bus": 103, "addr": 0x0d,  "offset":0x93, "way":"i2c"},
                                            "Running": {"loc":"/sys/rg_plat/fan/fan7/motor0/status","way":"sysfs", "mask": 0x01, "is_runing": 1},
                                            "HwAlarm": {"loc":"/sys/rg_plat/fan/fan7/motor0/status","way":"sysfs", "mask": 0x01, "no_alarm": 1},
                                            "SpeedMin": threshold.FAN_SPEED_MIN,
                                            "SpeedMax": threshold.FAN_SPEED_MAX,
                                            "Speed": {
                                                        "value": {"loc": "/sys/rg_plat/fan/fan7/motor0/speed", "way": "sysfs"},
                                                        "Min": threshold.FAN_SPEED_MIN,
                                                        "Max": threshold.FAN_SPEED_MAX,
                                                        "Unit": Unit.Speed,
                                                    },
                                           },
                        "Rotor2_config": {
                                            "name": "Rotor2",
                                            "Set_speed" : {"bus": 103, "addr": 0x0d,  "offset":0x93, "way":"i2c"},
                                            "Running": {"loc":"/sys/rg_plat/fan/fan7/motor1/status","way":"sysfs", "mask": 0x01, "is_runing": 1},
                                            "HwAlarm": {"loc":"/sys/rg_plat/fan/fan7/motor1/status","way":"sysfs", "mask": 0x01, "no_alarm": 1},
                                            "SpeedMin": threshold.FAN_SPEED_MIN,
                                            "SpeedMax": threshold.FAN_SPEED_MAX,
                                            "Speed": {
                                                        "value": {"loc": "/sys/rg_plat/fan/fan7/motor1/speed", "way": "sysfs"},
                                                        "Min": threshold.FAN_SPEED_MIN,
                                                        "Max": threshold.FAN_SPEED_MAX,
                                                        "Unit": Unit.Speed,
                                                    },
                                           },
                },
        },
        {
            "name": "FAN8",
            "airflow" : fanairflow,
            "fan_display_name": fan_display_name,
            "e2loc": {'loc': '/sys/bus/i2c/devices/i2c-116/116-0050/eeprom', 'offset': 0, 'len': 256, 'way': 'devfile'},
            "present" : {"loc":"/sys/rg_plat/fan/fan8/present","way":"sysfs", "mask": 0x01, "okval": 1},
            "SpeedMin" : threshold.FAN_SPEED_MIN,
            "SpeedMax" : threshold.FAN_SPEED_MAX,
            "led": {"bus": 111, "addr": 0x0d,  "offset":0xd3, "way":"i2c"},
            "led_attrs" : {
                           "green":0x04, "red":0x02, "yellow":0x06, "default":0x04,
                           "flash":0xff, "light":0xff, "off": 0, "mask":0xff
                          },
            "Rotor": {
                        "Rotor1_config": {  "name": "Rotor1",
                                            "Set_speed" : {"bus": 111, "addr": 0x0d,  "offset":0x93, "way":"i2c"},
                                            "Running": {"loc":"/sys/rg_plat/fan/fan8/motor0/status","way":"sysfs", "mask": 0x01, "is_runing": 1},
                                            "HwAlarm": {"loc":"/sys/rg_plat/fan/fan8/motor0/status","way":"sysfs", "mask": 0x01, "no_alarm": 1},
                                            "SpeedMin": threshold.FAN_SPEED_MIN,
                                            "SpeedMax": threshold.FAN_SPEED_MAX,
                                            "Speed": {
                                                        "value": {"loc": "/sys/rg_plat/fan/fan8/motor0/speed", "way": "sysfs"},
                                                        "Min": threshold.FAN_SPEED_MIN,
                                                        "Max": threshold.FAN_SPEED_MAX,
                                                        "Unit": Unit.Speed,
                                                    },
                                           },
                        "Rotor2_config": {
                                            "name": "Rotor2",
                                            "Set_speed" : {"bus": 111, "addr": 0x0d,  "offset":0x93, "way":"i2c"},
                                            "Running": {"loc":"/sys/rg_plat/fan/fan8/motor1/status","way":"sysfs", "mask": 0x01, "is_runing": 1},
                                            "HwAlarm": {"loc":"/sys/rg_plat/fan/fan8/motor1/status","way":"sysfs", "mask": 0x01, "no_alarm": 1},
                                            "SpeedMin": threshold.FAN_SPEED_MIN,
                                            "SpeedMax": threshold.FAN_SPEED_MAX,
                                            "Speed": {
                                                        "value": {"loc": "/sys/rg_plat/fan/fan8/motor1/speed", "way": "sysfs"},
                                                        "Min": threshold.FAN_SPEED_MIN,
                                                        "Max": threshold.FAN_SPEED_MAX,
                                                        "Unit": Unit.Speed,
                                                    },
                                           },
                },
        },
    ],
    "dcdc": [
        {
            "name": "MAC_VDD12V_01",
            "dcdc_id": "DCDC1",
            "Min": 10800,
            "value": {
                "loc": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in1_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 13200,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD1.8_CLK",
            "dcdc_id": "DCDC2",
            "Min": 1620,
            "value": {
                "loc": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in2_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1980,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD3.3_CLK",
            "dcdc_id": "DCDC3",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD1.0V_FPGA",
            "dcdc_id": "DCDC4",
            "Min": 900,
            "value": {
                "loc": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1100,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD1.8V_FPGA",
            "dcdc_id": "DCDC5",
            "Min": 1620,
            "value": {
                "loc": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in5_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1980,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD1.2V_FPGA",
            "dcdc_id": "DCDC6",
            "Min": 1080,
            "value": {
                "loc": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in6_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1320,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD3.3V",
            "dcdc_id": "DCDC7",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in7_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDDO1.2V",
            "dcdc_id": "DCDC8",
            "Min": 1080,
            "value": {
                "loc": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in8_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1320,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDDO1.8V",
            "dcdc_id": "DCDC9",
            "Min": 1620,
            "value": {
                "loc": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in9_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1980,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD_CORE",
            "dcdc_id": "DCDC10",
            "Min": 720,
            "value": {
                "loc": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in10_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 900,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDDA1.5V",
            "dcdc_id": "DCDC11",
            "Min": 1350,
            "value": {
                "loc": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in11_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1650,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD0_9V_ANLG0",
            "dcdc_id": "DCDC12",
            "Min": 810,
            "value": {
                "loc": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in12_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1080,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD0_9V_ANLG1",
            "dcdc_id": "DCDC13",
            "Min": 810,
            "value": {
                "loc": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in13_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1080,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD0_75V_ANLG0",
            "dcdc_id": "DCDC14",
            "Min": 675,
            "value": {
                "loc": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in14_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 900,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD0_75V_ANLG1",
            "dcdc_id": "DCDC15",
            "Min": 675,
            "value": {
                "loc": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in15_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 900,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD0.8V",
            "dcdc_id": "DCDC16",
            "Min": 720,
            "value": {
                "loc": "/sys/bus/i2c/devices/79-005b/hwmon/hwmon*/in16_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 880,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD12V_02",
            "dcdc_id": "DCDC17",
            "Min": 10800,
            "value": {
                "loc": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in1_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 13200,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD3.3V_standby",
            "dcdc_id": "DCDC18",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in2_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD3V8_CLK",
            "dcdc_id": "DCDC19",
            "Min": 3420,
            "value": {
                "loc": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 4180,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD5V_VR",
            "dcdc_id": "DCDC20",
            "Min": 4500,
            "value": {
                "loc": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 5500,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD1.5V",
            "dcdc_id": "DCDC21",
            "Min": 1350,
            "value": {
                "loc": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in5_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1650,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD1_2V",
            "dcdc_id": "DCDC22",
            "Min": 1080,
            "value": {
                "loc": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in6_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1320,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD_PLL0",
            "dcdc_id": "DCDC23",
            "Min": 810,
            "value": {
                "loc": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in7_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 990,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD_PLL1",
            "dcdc_id": "DCDC24",
            "Min": 810,
            "value": {
                "loc": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in8_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 990,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD_PLL2",
            "dcdc_id": "DCDC25",
            "Min": 810,
            "value": {
                "loc": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in9_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 990,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_VDD_PLL3",
            "dcdc_id": "DCDC26",
            "Min": 810,
            "value": {
                "loc": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in10_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 990,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_QSFP112_VDD3.3V_A",
            "dcdc_id": "DCDC27",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in11_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_QSFP112_VDD3.3V_B",
            "dcdc_id": "DCDC28",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in12_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_QSFP112_VDD3.3V_C",
            "dcdc_id": "DCDC29",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in13_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_QSFP112_VDD3.3V_D",
            "dcdc_id": "DCDC30",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/80-005b/hwmon/hwmon*/in14_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_XDPE_VDD_CORE_V",
            "dcdc_id": "DCDC31",
            "Min": 720,
            "value": {
                "loc": "/sys/bus/i2c/devices/81-0040/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 880,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_XDPE_VDD0_9V_ANLG0_V",
            "dcdc_id": "DCDC32",
            "Min": 810,
            "value": {
                "loc": "/sys/bus/i2c/devices/82-004d/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 990,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_XDPE_VDD0_75V_ANLG0_V",
            "dcdc_id": "DCDC33",
            "Min": 675,
            "value": {
                "loc": "/sys/bus/i2c/devices/82-004d/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 825,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_XDPE_VDD0_9V_ANLG1_V",
            "dcdc_id": "DCDC34",
            "Min": 810,
            "value": {
                "loc": "/sys/bus/i2c/devices/83-004d/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 990,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_XDPE_VDD0_75V_ANLG1_V",
            "dcdc_id": "DCDC35",
            "Min": 675,
            "value": {
                "loc": "/sys/bus/i2c/devices/83-004d/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 825,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_XDPE_QSFP112_VDD3.3V_A_V",
            "dcdc_id": "DCDC36",
            "Min": 1980,
            "value": {
                "loc": "/sys/bus/i2c/devices/84-0070/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 2420,
            "format": "float(float(%s)*1.5/1000)",
        },
        {
            "name": "MAC_XDPE_QSFP112_VDD3.3V_B_V",
            "dcdc_id": "DCDC37",
            "Min": 1980,
            "value": {
                "loc": "/sys/bus/i2c/devices/84-0070/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 2420,
            "format": "float(float(%s)*1.5/1000)",
        },
        {
            "name": "MAC_XDPE_QSFP112_VDD3.3V_C_V",
            "dcdc_id": "DCDC38",
            "Min": 1980,
            "value": {
                "loc": "/sys/bus/i2c/devices/85-0070/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 2420,
            "format": "float(float(%s)*1.5/1000)",
        },
        {
            "name": "MAC_XDPE_QSFP112_VDD3.3V_D_V",
            "dcdc_id": "DCDC39",
            "Min": 1980,
            "value": {
                "loc": "/sys/bus/i2c/devices/85-0070/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 2420,
            "format": "float(float(%s)*1.5/1000)",
        },
        {
            "name": "MAC_XDPE_VDD_CORE_C",
            "dcdc_id": "DCDC40",
            "Min": -1000,
            "value": {
                "loc": "/sys/bus/i2c/devices/81-0040/hwmon/hwmon*/curr3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 909700,
            "format": "float(float(%s)/1000)*2",
        },
        {
            "name": "MAC_XDPE_VDD0_9V_ANLG0_C",
            "dcdc_id": "DCDC41",
            "Min": -1000,
            "value": {
                "loc": "/sys/bus/i2c/devices/82-004d/hwmon/hwmon*/curr3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 77737,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_XDPE_VDD0_75V_ANLG0_C",
            "dcdc_id": "DCDC42",
            "Min": -1000,
            "value": {
                "loc": "/sys/bus/i2c/devices/82-004d/hwmon/hwmon*/curr4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 38825,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_XDPE_VDD0_9V_ANLG1_C",
            "dcdc_id": "DCDC43",
            "Min": -1000,
            "value": {
                "loc": "/sys/bus/i2c/devices/83-004d/hwmon/hwmon*/curr3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 77737,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_XDPE_VDD0_75V_ANLG1_C",
            "dcdc_id": "DCDC44",
            "Min": -1000,
            "value": {
                "loc": "/sys/bus/i2c/devices/83-004d/hwmon/hwmon*/curr4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 38825,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_XDPE_QSFP112_VDD3.3V_A_C",
            "dcdc_id": "DCDC45",
            "Min": -5000,
            "value": {
                "loc": "/sys/bus/i2c/devices/84-0070/hwmon/hwmon*/curr3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 88000,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_XDPE_QSFP112_VDD3.3V_B_C",
            "dcdc_id": "DCDC46",
            "Min": -5000,
            "value": {
                "loc": "/sys/bus/i2c/devices/84-0070/hwmon/hwmon*/curr4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 88000,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_XDPE_QSFP112_VDD3.3V_C_C",
            "dcdc_id": "DCDC47",
            "Min": -5000,
            "value": {
                "loc": "/sys/bus/i2c/devices/85-0070/hwmon/hwmon*/curr3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 88000,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MAC_XDPE_QSFP112_VDD3.3V_D_C",
            "dcdc_id": "DCDC48",
            "Min": -5000,
            "value": {
                "loc": "/sys/bus/i2c/devices/85-0070/hwmon/hwmon*/curr4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 88000,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MGMT_VDD12V",
            "dcdc_id": "DCDC49",
            "Min": 10800,
            "value": {
                "loc": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in1_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 13200,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MGMT_VDD3.3_STBY",
            "dcdc_id": "DCDC50",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in2_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MGMT_VDD5V_USB",
            "dcdc_id": "DCDC51",
            "Min": 4500,
            "value": {
                "loc": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 5500,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MGMT_PHY_VDD1V0",
            "dcdc_id": "DCDC52",
            "Min": 900,
            "value": {
                "loc": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1100,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MGMT_VDD3.3V",
            "dcdc_id": "DCDC53",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in5_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MGMT_PHY_VDD1V8",
            "dcdc_id": "DCDC54",
            "Min": 1620,
            "value": {
                "loc": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in6_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1980,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MGMT_VDD3.3_CLK",
            "dcdc_id": "DCDC55",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in7_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MGMT_VDD2.5V",
            "dcdc_id": "DCDC56",
            "Min": 2250,
            "value": {
                "loc": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in8_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 2750,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MGMT_SSD1_VDD3.3V",
            "dcdc_id": "DCDC57",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in9_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MGMT_SSD2_VDD3.3V",
            "dcdc_id": "DCDC58",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in10_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "MGMT_VDD3V8_CLK",
            "dcdc_id": "DCDC59",
            "Min": 3420,
            "value": {
                "loc": "/sys/bus/i2c/devices/121-005b/hwmon/hwmon*/in11_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 4180,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_P1V05",
            "dcdc_id": "DCDC60",
            "Min": 954,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in1_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1160,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_VCCIN",
            "dcdc_id": "DCDC61",
            "Min": 1350,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in2_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 2200,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_P1V2_VDDQ",
            "dcdc_id": "DCDC62",
            "Min": 1120,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1280,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_P1V8",
            "dcdc_id": "DCDC63",
            "Min": 1690,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1910,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_P0V6_VTT",
            "dcdc_id": "DCDC64",
            "Min": 558,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in5_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 682,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_VNN_PCH",
            "dcdc_id": "DCDC65",
            "Min": 540,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in6_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1320,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_VNN_NAC",
            "dcdc_id": "DCDC66",
            "Min": 540,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in7_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1320,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_P2V5_VPP",
            "dcdc_id": "DCDC67",
            "Min": 2250,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in8_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 2750,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_VCC_ANA",
            "dcdc_id": "DCDC68",
            "Min": 900,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in9_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1100,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_P3V3_STBY",
            "dcdc_id": "DCDC69",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in10_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_P5V_AUX",
            "dcdc_id": "DCDC70",
            "Min": 4000,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in11_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 5750,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_P1V8_AUX_NAC",
            "dcdc_id": "DCDC71",
            "Min": 1690,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in12_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1910,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_P3V3_AUX",
            "dcdc_id": "DCDC72",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in13_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_V1P80_EMMC_OUT",
            "dcdc_id": "DCDC73",
            "Min": 1690,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in14_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1910,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_V3P3_EMMC_OUT",
            "dcdc_id": "DCDC74",
            "Min": 3100,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005f/hwmon/hwmon*/in15_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3500,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_XDPE_VCCIN_V",
            "dcdc_id": "DCDC75",
            "Min": 1350,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-0070/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 2200,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_XDPE_P1V8_V",
            "dcdc_id": "DCDC76",
            "Min": 1690,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-0070/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1910,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_XDPE_P1V05_V",
            "dcdc_id": "DCDC77",
            "Min": 954,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-006e/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1160,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_XDPE_VNN_PCH_V",
            "dcdc_id": "DCDC78",
            "Min": 540,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-006e/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1320,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_XDPE_P1V2_VDDQ_V",
            "dcdc_id": "DCDC79",
            "Min": 1120,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005e/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1280,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_XDPE_VNN_NAC_V",
            "dcdc_id": "DCDC80",
            "Min": 540,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-0068/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1320,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_XDPE_VCC_ANA_V",
            "dcdc_id": "DCDC81",
            "Min": 900,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-0068/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1100,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_XDPE_VCCIN_C",
            "dcdc_id": "DCDC82",
            "Min": -3100,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-0070/hwmon/hwmon*/curr3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 147000,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_XDPE_P1V8_C",
            "dcdc_id": "DCDC83",
            "Min": -3100,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-0070/hwmon/hwmon*/curr4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 2300,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_XDPE_P1V05_C",
            "dcdc_id": "DCDC84",
            "Min": -3100,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-006e/hwmon/hwmon*/curr3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 14300,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_XDPE_VNN_PCH_C",
            "dcdc_id": "DCDC85",
            "Min": -3100,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-006e/hwmon/hwmon*/curr4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 7400,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_XDPE_P1V2_VDDQ_C",
            "dcdc_id": "DCDC86",
            "Min": -3100,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-005e/hwmon/hwmon*/curr3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 19000,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_XDPE_VNN_NAC_C",
            "dcdc_id": "DCDC87",
            "Min": -3100,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-0068/hwmon/hwmon*/curr3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 22000,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "CPU_XDPE_VCC_ANA_C",
            "dcdc_id": "DCDC88",
            "Min": -3100,
            "value": {
                "loc": "/sys/bus/i2c/devices/122-0068/hwmon/hwmon*/curr4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 2210,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "UPORT_VDD12V",
            "dcdc_id": "DCDC89",
            "Min": 10800,
            "value": {
                "loc": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in1_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 13200,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "UPORT_VDD3.3V_standby",
            "dcdc_id": "DCDC90",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in2_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "UPORT_VDD1.0V_FPGA",
            "dcdc_id": "DCDC91",
            "Min": 900,
            "value": {
                "loc": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1100,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "UPORT_VDD1.8V_FPGA",
            "dcdc_id": "DCDC92",
            "Min": 1620,
            "value": {
                "loc": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1980,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "UPORT_VDD1.2V_FPGA",
            "dcdc_id": "DCDC93",
            "Min": 1080,
            "value": {
                "loc": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in5_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1320,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "UPORT_VDD3.3V",
            "dcdc_id": "DCDC94",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in6_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "UPORT_VDD5V_VR",
            "dcdc_id": "DCDC95",
            "Min": 4500,
            "value": {
                "loc": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in7_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 5500,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "UPORT_QSFP112_VDD3.3V_A",
            "dcdc_id": "DCDC96",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in8_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "UPORT_QSFP112_VDD3.3V_B",
            "dcdc_id": "DCDC97",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/64-005b/hwmon/hwmon*/in9_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "UPORT_XDPE_QSFP112_VDD3.3V_A_V",
            "dcdc_id": "DCDC98",
            "Min": 1980,
            "value": {
                "loc": "/sys/bus/i2c/devices/66-0070/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 2420,
            "format": "float(float(%s)*1.5/1000)",
        },
        {
            "name": "UPORT_XDPE_QSFP112_VDD3.3V_B_V",
            "dcdc_id": "DCDC99",
            "Min": 1980,
            "value": {
                "loc": "/sys/bus/i2c/devices/66-0070/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 2420,
            "format": "float(float(%s)*1.5/1000)",
        },
        {
            "name": "UPORT_XDPE_QSFP112_VDD3.3V_A_C",
            "dcdc_id": "DCDC100",
            "Min": -5000,
            "value": {
                "loc": "/sys/bus/i2c/devices/66-0070/hwmon/hwmon*/curr3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 60900,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "UPORT_XDPE_QSFP112_VDD3.3V_B_C",
            "dcdc_id": "DCDC101",
            "Min": -5000,
            "value": {
                "loc": "/sys/bus/i2c/devices/66-0070/hwmon/hwmon*/curr4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 63800,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "DPORT_VDD12V",
            "dcdc_id": "DCDC102",
            "Min": 10800,
            "value": {
                "loc": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in1_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 13200,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "DPORT_VDD3.3V_standby",
            "dcdc_id": "DCDC103",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in2_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "DPORT_VDD1.0V_FPGA",
            "dcdc_id": "DCDC104",
            "Min": 900,
            "value": {
                "loc": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1100,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "DPORT_VDD1.8V_FPGA",
            "dcdc_id": "DCDC105",
            "Min": 1620,
            "value": {
                "loc": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1980,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "DPORT_VDD1.2V_FPGA",
            "dcdc_id": "DCDC106",
            "Min": 1080,
            "value": {
                "loc": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in5_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 1320,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "DPORT_VDD3.3V",
            "dcdc_id": "DCDC107",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in6_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "DPORT_VDD5V_VR",
            "dcdc_id": "DCDC108",
            "Min": 4500,
            "value": {
                "loc": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in7_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 5500,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "DPORT_QSFP112_VDD3.3V_A",
            "dcdc_id": "DCDC109",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in8_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "DPORT_QSFP112_VDD3.3V_B",
            "dcdc_id": "DCDC110",
            "Min": 2970,
            "value": {
                "loc": "/sys/bus/i2c/devices/129-005b/hwmon/hwmon*/in9_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 3630,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "DPORT_XDPE_QSFP112_VDD3.3V_A_V",
            "dcdc_id": "DCDC111",
            "Min": 1980,
            "value": {
                "loc": "/sys/bus/i2c/devices/131-0070/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 2420,
            "format": "float(float(%s)*1.5/1000)",
        },
        {
            "name": "DPORT_XDPE_QSFP112_VDD3.3V_B_V",
            "dcdc_id": "DCDC112",
            "Min": 1980,
            "value": {
                "loc": "/sys/bus/i2c/devices/131-0070/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "V",
            "Max": 2420,
            "format": "float(float(%s)*1.5/1000)",
        },
        {
            "name": "DPORT_XDPE_QSFP112_VDD3.3V_A_C",
            "dcdc_id": "DCDC113",
            "Min": -5000,
            "value": {
                "loc": "/sys/bus/i2c/devices/131-0070/hwmon/hwmon*/curr3_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 88000,
            "format": "float(float(%s)/1000)",
        },
        {
            "name": "DPORT_XDPE_QSFP112_VDD3.3V_B_C",
            "dcdc_id": "DCDC114",
            "Min": -5000,
            "value": {
                "loc": "/sys/bus/i2c/devices/131-0070/hwmon/hwmon*/curr4_input",
                "way": "sysfs",
            },
            "read_times": 11,
            "Unit": "A",
            "Max": 88000,
            "format": "float(float(%s)/1000)",
        },
    ],
}
