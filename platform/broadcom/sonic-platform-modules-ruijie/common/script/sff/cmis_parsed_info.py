try:
    from module_util import *
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


parsed_basic_info = {
    'page': 0x0,
    'info': {
        'FWRevActive': {
            'valid': True,
            'offset': 39,
            'size': 2,
            'type': 'hex',
        },
        'MediaType': {
            'valid': True,
            'offset': 85,
            'type': 'enum',
            'decode': type_of_media_interface,
        },
        'MediaInterface': {
            'valid': True,
            'offset': 85,
            'size': 3,
            'type': 'func',
            'decode': calc_media_id,
        },
        'HostElectricalInterface': {
            'valid': True,
            'offset': 86,
            'size': 1,
            'type': 'enum',
            'decode': host_electrical_interface,
        },
        'MediaLaneCount': {
            'valid': True,
            'offset': 88,
            'bits': 0xf,
            'type': 'int_bits',
        },
        'HostLaneCount': {
            'valid': True,
            'offset': 88,
            'bits': 0xf0,
            'type': 'int_bits',
        },
        'Identifier': {
            'valid': True,
            'offset': 128,
            'type': 'enum',
            'decode': type_of_transceiver,
        },
        'VendorName': {
            'valid': True,
            'offset': 129,
            'size': 16,
            'type': 'str',
        },
        'VendorOUI': {
            'valid': True,
            'offset': 145,
            'size': 3,
            'type': 'hex',
        },
        'VendorPN': {
            'valid': True,
            'offset': 148,
            'size': 16,
            'type': 'str',
        },
        'VendorRev': {
            'valid': True,
            'offset': 164,
            'size': 2,
            'type': 'str',
        },
        'VendorSN': {
            'valid': True,
            'offset': 166,
            'size': 16,
            'type': 'str',
        },
        'VendorDateCode(YYYY-MM-DD Lot)': {
            'valid': True,
            'offset': 182,
            'size': 8,
            'type': 'date',
        },
        'PowerClass': {
            'valid': True,
            'offset': 200,
             'size': 2,
             'type': 'func',
             'decode': calc_cmis_power_class,
        },
        'ConnectorType': {
            'valid': True,
            'offset': 203,
            'type': 'enum',
            'decode': connector_dict,
        },
    },
}

parsed_adv_info = {
    'page': 0x1,
    'info': {
        'HardwareRev': {
            'valid': True,
            'offset': 130,
            'size': 2,
            'type': 'str',
        },
    },
}

parsed_imp_info = {
    'page': {
        0x1: {
            'info': {
                'VDMImplemented': {
                    'valid': True,
                    'offset': 142,
                    'type': 'bit',
                    'bit': 6,
                },
                'RxLOSImplemented': {
                    'valid': True,
                    'offset': 158,
                    'type': 'bit',
                    'bit': 1,
                },
                'TempMonitorImplemented': {
                    'valid': True,
                    'offset': 159,
                    'type': 'bit',
                    'bit': 0,
                },
                'VoltMonitorImplemented': {
                    'valid': True,
                    'offset': 159,
                    'type': 'bit',
                    'bit': 1,
                },
                'TxPowerMonitorImplemented': {
                    'valid': True,
                    'offset': 160,
                    'type': 'bit',
                    'bit': 1,
                },
                'RxPowerMonitorImplemented': {
                    'valid': True,
                    'offset': 160,
                    'type': 'bit',
                    'bit': 2,
                },
                'CDBImplemented': {
                    'valid': True,
                    'offset': 163,
                    'type': 'func',
                    'decode': calc_cmis_cdb_support,
                },
            },
        },
        0x13: {
            'info': {
                'MediaTxLoopbackImplemented': {
                    'valid' : True,
                    'offset': 128,
                    'type': 'bit',
                    'bit': 0,
                },
                'MediaRxLoopbackImplemented': {
                    'valid' : True,
                    'offset': 128,
                    'type': 'bit',
                    'bit': 1,
                },
                'HostRxLoopbackImplemented': {
                    'valid' : True,
                    'offset': 128,
                    'type': 'bit',
                    'bit': 2,
                },
                'HostTxLoopbackImplemented': {
                    'valid' : True,
                    'offset': 128,
                    'type': 'bit',
                    'bit': 3,
                },
                'SimultaneousLoopbackImplemented': {
                    'valid' : True,
                    'offset': 128,
                    'type': 'bit',
                    'bit': 6,
                },
            },
        },
    },
}

parsed_module_monitors_info = {
    'page': 0x0,
    'info': {
        'ModuleTemperature': {
            'valid': True,
            'offset': 14,
            'size': 2,
            'type': 'func',
            'decode': calc_temperature,
        },
        'SupplyVoltage': {
            'valid': True,
            'offset': 16,
            'size': 2,
            'type': 'func',
            'decode': calc_voltage,
        },
    },
}

parsed_lane_monitors_info = {
    'page': 0x11,
    'info': {
        'Tx1Power': {
            'valid': True,
            'offset': 154,
             'size': 2,
             'type': 'func',
             'decode': calc_power,
        },
        'Tx2Power': {
            'valid': True,
            'offset': 156,
             'size': 2,
             'type': 'func',
             'decode': calc_power,
        },
        'Tx3Power': {
            'valid': True,
            'offset': 158,
             'size': 2,
             'type': 'func',
             'decode': calc_power,
        },
        'Tx4Power': {
            'valid': True,
            'offset': 160,
             'size': 2,
             'type': 'func',
             'decode': calc_power,
        },
        'Tx5Power': {
            'valid': True,
            'offset': 162,
             'size': 2,
             'type': 'func',
             'decode': calc_power,
        },
        'Tx6Power': {
            'valid': True,
            'offset': 164,
             'size': 2,
             'type': 'func',
             'decode': calc_power,
        },
        'Tx7Power': {
            'valid': True,
            'offset': 166,
             'size': 2,
             'type': 'func',
             'decode': calc_power,
        },
        'Tx8Power': {
            'valid': True,
            'offset': 168,
             'size': 2,
             'type': 'func',
             'decode': calc_power,
        },
        'Rx1Power': {
            'valid': True,
            'offset': 186,
             'size': 2,
             'type': 'func',
             'decode': calc_power,
        },
        'Rx2Power': {
            'valid': True,
            'offset': 188,
             'size': 2,
             'type': 'func',
             'decode': calc_power,
        },
        'Rx3Power': {
            'valid': True,
            'offset': 190,
             'size': 2,
             'type': 'func',
             'decode': calc_power,
        },
        'Rx4Power': {
            'valid': True,
            'offset': 192,
             'size': 2,
             'type': 'func',
             'decode': calc_power,
        },
        'Rx5Power': {
            'valid': True,
            'offset': 194,
             'size': 2,
             'type': 'func',
             'decode': calc_power,
        },
        'Rx6Power': {
            'valid': True,
            'offset': 196,
             'size': 2,
             'type': 'func',
             'decode': calc_power,
        },
        'Rx7Power': {
            'valid': True,
            'offset': 198,
             'size': 2,
             'type': 'func',
             'decode': calc_power,
        },
        'Rx8Power': {
            'valid': True,
            'offset': 200,
             'size': 2,
             'type': 'func',
             'decode': calc_power,
        },
    },
}

parsed_dom_monitors_interrupt_info = {
    'page': 0x0,
    'info': {
        'TempLowWarning': {
            'valid': True,
            'offset':9,
            'type': 'bit',
            'bit': 3,
        },
        'TempHighWarning': {
            'valid': True,
            'offset':9,
            'type': 'bit',
            'bit': 2,
        },
        'TempLowAlarm': {
            'valid': True,
            'offset':9,
            'type': 'bit',
            'bit': 1,
        },
        'TempHighAlarm': {
            'valid': True,
            'offset':9,
            'type': 'bit',
            'bit': 0,
        },
        'VccLowWarning': {
            'valid': True,
            'offset':9,
            'type': 'bit',
            'bit': 7,
        },
        'VccHighWarning': {
            'valid': True,
            'offset':9,
            'type': 'bit',
            'bit': 6,
        },
        'VccLowAlarm': {
            'valid': True,
            'offset':9,
            'type': 'bit',
            'bit': 5,
        },
        'VccHighAlarm': {
            'valid': True,
            'offset':9,
            'type': 'bit',
            'bit': 4,
        },
    },
}

parsed_dom_chnl_monitors_interrupt_info = {
    'page': 0x11,
    'info': {
        'Tx1PowerHighAlarm': {
            'valid': True,
            'offset':139,
            'type': 'bit',
            'bit': 0,
        },
        'Tx2PowerHighAlarm': {
            'valid': True,
            'offset':139,
            'type': 'bit',
            'bit': 1,
        },
        'Tx3PowerHighAlarm': {
            'valid': True,
            'offset':139,
            'type': 'bit',
            'bit': 2,
        },
        'Tx4PowerHighAlarm': {
            'valid': True,
            'offset':139,
            'type': 'bit',
            'bit': 3,
        },
        'Tx5PowerHighAlarm': {
            'valid': True,
            'offset':139,
            'type': 'bit',
            'bit': 4,
        },
        'Tx6PowerHighAlarm': {
            'valid': True,
            'offset':139,
            'type': 'bit',
            'bit': 5,
        },
        'Tx7PowerHighAlarm': {
            'valid': True,
            'offset':139,
            'type': 'bit',
            'bit': 6,
        },
        'Tx8PowerHighAlarm': {
            'valid': True,
            'offset':139,
            'type': 'bit',
            'bit': 7,
        },
        'Tx1PowerLowAlarm': {
            'valid': True,
            'offset':140,
            'type': 'bit',
            'bit': 0,
        },
        'Tx2PowerLowAlarm': {
            'valid': True,
            'offset':140,
            'type': 'bit',
            'bit': 1,
        },
        'Tx3PowerLowAlarm': {
            'valid': True,
            'offset':140,
            'type': 'bit',
            'bit': 2,
        },
        'Tx4PowerLowAlarm': {
            'valid': True,
            'offset':140,
            'type': 'bit',
            'bit': 3,
        },
        'Tx5PowerLowAlarm': {
            'valid': True,
            'offset':140,
            'type': 'bit',
            'bit': 4,
        },
        'Tx6PowerLowAlarm': {
            'valid': True,
            'offset':140,
            'type': 'bit',
            'bit': 5,
        },
        'Tx7PowerLowAlarm': {
            'valid': True,
            'offset':140,
            'type': 'bit',
            'bit': 6,
        },
        'Tx8PowerLowAlarm': {
            'valid': True,
            'offset':140,
            'type': 'bit',
            'bit': 7,
        },
        'Tx1PowerHighWarning': {
            'valid': True,
            'offset':141,
            'type': 'bit',
            'bit': 0,
        },
        'Tx2PowerHighWarning': {
            'valid': True,
            'offset':141,
            'type': 'bit',
            'bit': 1,
        },
        'Tx3PowerHighWarning': {
            'valid': True,
            'offset':141,
            'type': 'bit',
            'bit': 2,
        },
        'Tx4PowerHighWarning': {
            'valid': True,
            'offset':141,
            'type': 'bit',
            'bit': 3,
        },
        'Tx5PowerHighWarning': {
            'valid': True,
            'offset':141,
            'type': 'bit',
            'bit': 4,
        },
        'Tx6PowerHighWarning': {
            'valid': True,
            'offset':141,
            'type': 'bit',
            'bit': 5,
        },
        'Tx7PowerHighWarning': {
            'valid': True,
            'offset':141,
            'type': 'bit',
            'bit': 6,
        },
        'Tx8PowerHighWarning': {
            'valid': True,
            'offset':141,
            'type': 'bit',
            'bit': 7,
        },
        'Tx1PowerLowWarning': {
            'valid': True,
            'offset':142,
            'type': 'bit',
            'bit': 0,
        },
        'Tx2PowerLowWarning': {
            'valid': True,
            'offset':142,
            'type': 'bit',
            'bit': 1,
        },
        'Tx3PowerLowWarning': {
            'valid': True,
            'offset':142,
            'type': 'bit',
            'bit': 2,
        },
        'Tx4PowerLowWarning': {
            'valid': True,
            'offset':142,
            'type': 'bit',
            'bit': 3,
        },
        'Tx5PowerLowWarning': {
            'valid': True,
            'offset':142,
            'type': 'bit',
            'bit': 4,
        },
        'Tx6PowerLowWarning': {
            'valid': True,
            'offset':142,
            'type': 'bit',
            'bit': 5,
        },
        'Tx7PowerLowWarning': {
            'valid': True,
            'offset':142,
            'type': 'bit',
            'bit': 6,
        },
        'Tx8PowerLowWarning': {
            'valid': True,
            'offset':142,
            'type': 'bit',
            'bit': 7,
        },
        'Rx1LOS': {
            'valid': True,
            'offset':147,
            'type': 'bit',
            'bit': 0,
        },
        'Rx2LOS': {
            'valid': True,
            'offset':147,
            'type': 'bit',
            'bit': 1,
        },
        'Rx3LOS': {
            'valid': True,
            'offset':147,
            'type': 'bit',
            'bit': 2,
        },
        'Rx4LOS': {
            'valid': True,
            'offset':147,
            'type': 'bit',
            'bit': 3,
        },
        'Rx5LOS': {
            'valid': True,
            'offset':147,
            'type': 'bit',
            'bit': 4,
        },
        'Rx6LOS': {
            'valid': True,
            'offset':147,
            'type': 'bit',
            'bit': 5,
        },
        'Rx7LOS': {
            'valid': True,
            'offset':147,
            'type': 'bit',
            'bit': 6,
        },
        'Rx8LOS': {
            'valid': True,
            'offset':147,
            'type': 'bit',
            'bit': 7,
        },
        'Rx1PowerHighAlarm': {
            'valid': True,
            'offset':149,
            'type': 'bit',
            'bit': 0,
        },
        'Rx2PowerHighAlarm': {
            'valid': True,
            'offset':149,
            'type': 'bit',
            'bit': 1,
        },
        'Rx3PowerHighAlarm': {
            'valid': True,
            'offset':149,
            'type': 'bit',
            'bit': 2,
        },
        'Rx4PowerHighAlarm': {
            'valid': True,
            'offset':149,
            'type': 'bit',
            'bit': 3,
        },
        'Rx5PowerHighAlarm': {
            'valid': True,
            'offset':149,
            'type': 'bit',
            'bit': 4,
        },
        'Rx6PowerHighAlarm': {
            'valid': True,
            'offset':149,
            'type': 'bit',
            'bit': 5,
        },
        'Rx7PowerHighAlarm': {
            'valid': True,
            'offset':149,
            'type': 'bit',
            'bit': 6,
        },
        'Rx8PowerHighAlarm': {
            'valid': True,
            'offset':149,
            'type': 'bit',
            'bit': 7,
        },
        'Rx1PowerLowAlarm': {
            'valid': True,
            'offset':150,
            'type': 'bit',
            'bit': 0,
        },
        'Rx2PowerLowAlarm': {
            'valid': True,
            'offset':150,
            'type': 'bit',
            'bit': 1,
        },
        'Rx3PowerLowAlarm': {
            'valid': True,
            'offset':150,
            'type': 'bit',
            'bit': 2,
        },
        'Rx4PowerLowAlarm': {
            'valid': True,
            'offset':150,
            'type': 'bit',
            'bit': 3,
        },
        'Rx5PowerLowAlarm': {
            'valid': True,
            'offset':150,
            'type': 'bit',
            'bit': 4,
        },
        'Rx6PowerLowAlarm': {
            'valid': True,
            'offset':150,
            'type': 'bit',
            'bit': 5,
        },
        'Rx7PowerLowAlarm': {
            'valid': True,
            'offset':150,
            'type': 'bit',
            'bit': 6,
        },
        'Rx8PowerLowAlarm': {
            'valid': True,
            'offset':150,
            'type': 'bit',
            'bit': 7,
        },
        'Rx1PowerHighWarning': {
            'valid': True,
            'offset':151,
            'type': 'bit',
            'bit': 0,
        },
        'Rx2PowerHighWarning': {
            'valid': True,
            'offset':151,
            'type': 'bit',
            'bit': 1,
        },
        'Rx3PowerHighWarning': {
            'valid': True,
            'offset':151,
            'type': 'bit',
            'bit': 2,
        },
        'Rx4PowerHighWarning': {
            'valid': True,
            'offset':151,
            'type': 'bit',
            'bit': 3,
        },
        'Rx5PowerHighWarning': {
            'valid': True,
            'offset':151,
            'type': 'bit',
            'bit': 4,
        },
        'Rx6PowerHighWarning': {
            'valid': True,
            'offset':151,
            'type': 'bit',
            'bit': 5,
        },
        'Rx7PowerHighWarning': {
            'valid': True,
            'offset':151,
            'type': 'bit',
            'bit': 6,
        },
        'Rx8PowerHighWarning': {
            'valid': True,
            'offset':151,
            'type': 'bit',
            'bit': 7,
        },
        'Rx1PowerLowWarning': {
            'valid': True,
            'offset':152,
            'type': 'bit',
            'bit': 0,
        },
        'Rx2PowerLowWarning': {
            'valid': True,
            'offset':152,
            'type': 'bit',
            'bit': 1,
        },
        'Rx3PowerLowWarning': {
            'valid': True,
            'offset':152,
            'type': 'bit',
            'bit': 2,
        },
        'Rx4PowerLowWarning': {
            'valid': True,
            'offset':152,
            'type': 'bit',
            'bit': 3,
        },
        'Rx5PowerLowWarning': {
            'valid': True,
            'offset':152,
            'type': 'bit',
            'bit': 4,
        },
        'Rx6PowerLowWarning': {
            'valid': True,
            'offset':152,
            'type': 'bit',
            'bit': 5,
        },
        'Rx7PowerLowWarning': {
            'valid': True,
            'offset':152,
            'type': 'bit',
            'bit': 6,
        },
        'Rx8PowerLowWarning': {
            'valid': True,
            'offset':152,
            'type': 'bit',
            'bit': 7,
        },
    },
}

parsed_diag1_info = {
    'page': 0x13,
    'info': {
        'MediaTxLoopback': {
            'valid': True,
            'offset': 180,
            'type': 'func',
            'decode': calc_cmis_loopback,
        },
        'MediaRxLoopback': {
            'valid': True,
            'offset': 181,
            'type': 'func',
            'decode': calc_cmis_loopback,
        },
        'HostRxLoopback': {
            'valid': True,
            'offset': 182,
            'type': 'func',
            'decode': calc_cmis_loopback,
        },
        'HostTxLoopback': {
            'valid': True,
            'offset': 183,
            'type': 'func',
            'decode': calc_cmis_loopback,
        },
    },
}

parsed_vdm_group1_conf_info = {
    'page': 0x20,
    'info': {
        'VDMGroupConfig': {
            'valid': True,
            'offset': 128,
            'size': 128,
            'type': 'func',
            'decode': calc_vdm_config,
        },
    },
}

parsed_vdm_group2_conf_info = {
    'page': 0x21,
    'info': {
        'VDMGroupConfig': {
            'valid': True,
            'offset': 128,
            'size': 128,
            'type': 'func',
            'decode': calc_vdm_config,
        },
    },
}

parsed_vdm_group3_conf_info = {
    'page': 0x22,
    'info': {
        'VDMGroupConfig': {
            'valid': True,
            'offset': 128,
            'size': 128,
            'type': 'func',
            'decode': calc_vdm_config,
        },
    },
}

parsed_vdm_group4_conf_info = {
    'page': 0x23,
    'info': {
        'VDMGroupConfig': {
            'valid': True,
            'offset': 128,
            'size': 128,
            'type': 'func',
            'decode': calc_vdm_config,
        },
    },
}

parsed_vdm_group1_val_info = {
    'page': 0x24,
    'info': {
        'VDMGroupVal': {
            'valid': True,
            'offset': 128,
            'size': 128,
            'type': 'func',
            'decode': calc_vdm_val_raw,
        },
    },
}

parsed_vdm_group2_val_info = {
    'page': 0x25,
    'info': {
        'VDMGroupVal': {
            'valid': True,
            'offset': 128,
            'size': 128,
            'type': 'func',
            'decode': calc_vdm_val_raw,
        },
    },
}

parsed_vdm_group3_val_info = {
    'page': 0x26,
    'info': {
        'VDMGroupVal': {
            'valid': True,
            'offset': 128,
            'size': 128,
            'type': 'func',
            'decode': calc_vdm_val_raw,
        },
    },
}

parsed_vdm_group4_val_info = {
    'page': 0x27,
    'info': {
        'VDMGroupVal': {
            'valid': True,
            'offset': 128,
            'size': 128,
            'type': 'func',
            'decode': calc_vdm_val_raw,
        },
    },
}

parsed_vdm_alarm_info = {
    'page': 0x2c,
    'info': {
        'VDMAlarmVal': {
            'valid': True,
            'offset': 128,
            'size': 128,
            'type': 'func',
            'decode': calc_vdm_alarm_raw,
        },
    },
}

parsed_media_lane_link_performance_monitoring = {
    'page': 0x35,
    'info': {
        'RxAvgCd': {
            'valid': True,
            'offset': 128,
            'size': 4,
            'type': 'func',
            'decode': calc_cd,
        },
        'RxMinCd': {
            'valid': True,
            'offset': 132,
            'size': 4,
            'type': 'func',
            'decode': calc_cd,
        },
        'RxMaxCd': {
            'valid': True,
            'offset': 136,
            'size': 4,
            'type': 'func',
            'decode': calc_cd,
        },
        'RxAvgDgd': {
            'valid': True,
            'offset': 140,
            'size': 2,
            'type': 'func',
            'decode': calc_dgd,
        },
        'RxMinDgd': {
            'valid': True,
            'offset': 142,
            'size': 2,
            'type': 'func',
            'decode': calc_dgd,
        },
        'RxMaxDgd': {
            'valid': True,
            'offset': 144,
            'size': 2,
            'type': 'func',
            'decode': calc_dgd,
        },
        'RxAvgSopmd': {
            'valid': True,
            'offset': 146,
            'size': 2,
            'type': 'func',
            'decode': calc_sopmd,
        },
        'RxMinSopmd': {
            'valid': True,
            'offset': 148,
            'size': 2,
            'type': 'func',
            'decode': calc_sopmd,
        },
        'RxMaxSopmd': {
            'valid': True,
            'offset': 150,
            'size': 2,
            'type': 'func',
            'decode': calc_sopmd,
        },
        'RxAvgPdl': {
            'valid': True,
            'offset': 152,
            'size': 2,
            'type': 'func',
            'decode': calc_pdl,
        },
        'RxMinPdl': {
            'valid': True,
            'offset': 154,
            'size': 2,
            'type': 'func',
            'decode': calc_pdl,
        },
        'RxMaxPdl': {
            'valid': True,
            'offset': 156,
            'size': 2,
            'type': 'func',
            'decode': calc_pdl,
        },
        'RxAvgOsnr': {
            'valid': True,
            'offset': 158,
            'size': 2,
            'type': 'func',
            'decode': calc_snr,
        },
        'RxMinOsnr': {
            'valid': True,
            'offset': 160,
            'size': 2,
            'type': 'func',
            'decode': calc_snr,
        },
        'RxMaxOsnr': {
            'valid': True,
            'offset': 162,
            'size': 2,
            'type': 'func',
            'decode': calc_snr,
        },
        'RxAvgEsnr': {
            'valid': True,
            'offset': 164,
            'size': 2,
            'type': 'func',
            'decode': calc_snr,
        },
        'RxMinEsnr': {
            'valid': True,
            'offset': 166,
            'size': 2,
            'type': 'func',
            'decode': calc_snr,
        },
        'RxMaxEsnr': {
            'valid': True,
            'offset': 168,
            'size': 2,
            'type': 'func',
            'decode': calc_snr,
        },
        'RxAvgCfo': {
            'valid': True,
            'offset': 170,
            'size': 2,
            'type': 'func',
            'decode': calc_cfo,
        },
        'RxMinCfo': {
            'valid': True,
            'offset': 172,
            'size': 2,
            'type': 'func',
            'decode': calc_cfo,
        },
        'RxMaxCfo': {
            'valid': True,
            'offset': 174,
            'size': 2,
            'type': 'func',
            'decode': calc_cfo,
        },
        'RxAvgEvmModem': {
            'valid': True,
            'offset': 176,
            'size': 2,
            'type': 'func',
            'decode': calc_evmmodem,
        },
        'RxMinEvmModem': {
            'valid': True,
            'offset': 178,
            'size': 2,
            'type': 'func',
            'decode': calc_evmmodem,
        },
        'RxMaxEvmModem': {
            'valid': True,
            'offset': 180,
            'size': 2,
            'type': 'func',
            'decode': calc_evmmodem,
        },
        'TxAvgPower': {
            'valid': True,
            'offset': 182,
            'size': 2,
            'type': 'func',
            'decode': calc_vdm_power,
        },
        'TxMinPower': {
            'valid': True,
            'offset': 184,
            'size': 2,
            'type': 'func',
            'decode': calc_vdm_power,
        },
        'TxMaxPower': {
            'valid': True,
            'offset': 186,
            'size': 2,
            'type': 'func',
            'decode': calc_vdm_power,
        },
        'RxAvgPower': {
            'valid': True,
            'offset': 188,
            'size': 2,
            'type': 'func',
            'decode': calc_vdm_power,
        },
        'RxMinPower': {
            'valid': True,
            'offset': 190,
            'size': 2,
            'type': 'func',
            'decode': calc_vdm_power,
        },
        'RxMaxPower': {
            'valid': True,
            'offset': 192,
            'size': 2,
            'type': 'func',
            'decode': calc_vdm_power,
        },
        'RxAvgSigPower': {
            'valid': True,
            'offset': 194,
            'size': 2,
            'type': 'func',
            'decode': calc_vdm_power,
        },
        'RxMinSigPower': {
            'valid': True,
            'offset': 196,
            'size': 2,
            'type': 'func',
            'decode': calc_vdm_power,
        },
        'RxMaxSigPower': {
            'valid': True,
            'offset': 198,
            'size': 2,
            'type': 'func',
            'decode': calc_vdm_power,
        },
        'RxAvgSopcr': {
            'valid': True,
            'offset': 200,
            'size': 2,
            'type': 'func',
            'decode': calc_sopcr,
        },
        'RxMinSopcr': {
            'valid': True,
            'offset': 202,
            'size': 2,
            'type': 'func',
            'decode': calc_sopcr,
        },
        'RxMaxSopcr': {
            'valid': True,
            'offset': 204,
            'size': 2,
            'type': 'func',
            'decode': calc_sopcr,
        },
        'RxAvgMer': {
            'valid': True,
            'offset': 206,
            'size': 2,
            'type': 'func',
            'decode': calc_mer,
        },
        'RxMinMer': {
            'valid': True,
            'offset': 208,
            'size': 2,
            'type': 'func',
            'decode': calc_mer,
        },
        'RxMaxMer': {
            'valid': True,
            'offset': 210,
            'size': 2,
            'type': 'func',
            'decode': calc_mer,
        },
    },
}

parsed_media_lane_fec_performance_monitoring = {
    'page': 0x34,
    'info': {
        'MediaRxCorrBits': {
            'valid': True,
            'offset': 144,
            'size': 8,
            'type': 'func',
            'decode': convert_msb_first_data_to_long,
        },
        'MediaRxMinCorrBits': {
            'valid': True,
            'offset': 152,
            'size': 8,
            'type': 'func',
            'decode': convert_msb_first_data_to_long,
        },
        'MediaRxMaxCorrBits': {
            'valid': True,
            'offset': 160,
            'size': 8,
            'type': 'func',
            'decode': convert_msb_first_data_to_long,
        },
        'MediaRxFramesUncorrErr': {
            'valid': True,
            'offset': 176,
            'size': 4,
            'type': 'func',
            'decode': convert_msb_first_data_to_long,
        },
        'MediaRxMinFramesUncorrErr': {
            'valid': True,
            'offset': 180,
            'size': 4,
            'type': 'func',
            'decode': convert_msb_first_data_to_long,
        },
        'MediaRxMaxFramesUncorrErr': {
            'valid': True,
            'offset': 184,
            'size': 4,
            'type': 'func',
            'decode': convert_msb_first_data_to_long,
        },
    },
}

parsed_host_interface_performance_monitoring = {
    'page': 0x3A,
    'info': {
        'HostRxCorrBits': {
            'valid': True,
            'offset': 144,
            'size': 8,
            'type': 'func',
            'decode': convert_msb_first_data_to_long,
        },
        'HostRxMinCorrBits': {
            'valid': True,
            'offset': 152,
            'size': 8,
            'type': 'func',
            'decode': convert_msb_first_data_to_long,
        },
        'HostRxMaxCorrBits': {
            'valid': True,
            'offset': 160,
            'size': 8,
            'type': 'func',
            'decode': convert_msb_first_data_to_long,
        },
        'HostRxFramesUncorrErr': {
            'valid': True,
            'offset': 176,
            'size': 4,
            'type': 'func',
            'decode': convert_msb_first_data_to_long,
        },
        'HostRxMinFramesUncorrErr': {
            'valid': True,
            'offset': 180,
            'size': 4,
            'type': 'func',
            'decode': convert_msb_first_data_to_long,
        },
        'HostRxMaxFramesUncorrErr': {
            'valid': True,
            'offset': 184,
            'size': 4,
            'type': 'func',
            'decode': convert_msb_first_data_to_long,
        },
    },
}

parsed_media_lane_flags = {
    'page': 0x33,
    'info': {
        'MediaRxLolFifoAlarm': {
            'valid': True,
            'offset':130,
            'type': 'bit',
            'bit': 0,
        },
        'MediaRxLolDeskewAlarm': {
            'valid': True,
            'offset':130,
            'type': 'bit',
            'bit': 1,
        },
        'MediaRxOoaAlarm': {
            'valid': True,
            'offset':130,
            'type': 'bit',
            'bit': 2,
        },
        'MediaRxLoaAlarm': {
            'valid': True,
            'offset':130,
            'type': 'bit',
            'bit': 3,
        },
        'MediaRxLolCdAlarm': {
            'valid': True,
            'offset':130,
            'type': 'bit',
            'bit': 4,
        },
        'MediaRxLolDemodAlarm': {
            'valid': True,
            'offset':130,
            'type': 'bit',
            'bit': 5,
        },
        'MediaRxFddAlarm': {
            'valid': True,
            'offset':132,
            'type': 'bit',
            'bit': 0,
        },
        'MediaRxFedAlarm': {
            'valid': True,
            'offset':132,
            'type': 'bit',
            'bit': 1,
        },
        'MediaRPFAlarm': {
            'valid': True,
            'offset':133,
            'type': 'bit',
            'bit': 0,
        },
        'MediaLDAlarm': {
            'valid': True,
            'offset':133,
            'type': 'bit',
            'bit': 1,
        },
        'MediaRDAlarm': {
            'valid': True,
            'offset':133,
            'type': 'bit',
            'bit': 2,
        },
    },
}

parsed_host_interface_flags = {
    'page': 0x3B,
    'info': {
        'HostRxFddAlarm': {
            'valid': True,
            'offset':192,
            'type': 'bit',
            'bit': 0,
        },
        'HostRxFedAlarm': {
            'valid': True,
            'offset':192,
            'type': 'bit',
            'bit': 1,
        },
    },
}

parsed_host_interface_conf = {
    'page': 0x38,
    'info': {
        'HostLfInsertionOnLdEnable': {
            'valid': True,
            'offset':136,
            'type': 'bit',
            'bit': 2,
        },
    },
}

parsed_media_lane_prov = {
    'page': 0x31,
    'info': {
        'MediaLfInsertionOnLdEnable': {
            'valid': True,
            'offset':128,
            'type': 'bit',
            'bit': 1,
        },
    },
}

