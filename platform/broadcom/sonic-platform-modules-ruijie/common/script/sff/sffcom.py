cmis_prbs_pattern_info = {
    0 : 'PRBS-31Q',
    1 : 'PRBS-31',
    2 : 'PRBS-23Q',
    3 : 'PRBS-23',
    4 : 'PRBS-15Q',
    5 : 'PRBS-15',
    6 : 'PRBS-13Q',
    7 : 'PRBS-13',
    8 : 'PRBS-9Q',
    9 : 'PRBS-9',
    10 : 'PRBS-7Q',
    11 : 'PRBS-7',
    12 : 'SSPRQ',
}

cust_target_vdm_basic_cur_type = [1, 2, 3, 4, 15, 16, 23, 24]
cust_target_vdm_basic_alarm_type = [4, 15, 16]
cust_target_vdm_basic_stat_type = range(9, 15)

cust_target_vdm_datapath_cur_type = range(128, 148)
cust_target_vdm_datapath_alarm_type = [141]

cmis_vdm_conf_type_info = {
    1  : 'Laser Age',
    2  : 'TEC Current',
    3  : 'Laser Frequency Error',
    4  : 'Laser Temperature',
    5  : 'eSNR Media Input',
    6  : 'eSNR Host Input',
    7  : 'PAM4 Level Transition Parameter (LTP) Media Input',
    8  : 'PAM4 Level Transition Parameter (LTP) Host Input',
    9  : 'Pre-FEC BER Minimum Media Input (data-path)',
    10 : 'Pre-FEC BER Minimum Host Input',
    11 : 'Pre-FEC BER Maximum Media Input',
    12 : 'Pre-FEC BER Maximum Host Input',
    13 : 'Pre-FEC BER Average Media Input',
    14 : 'Pre-FEC BER Average Host Input',
    15 : 'Pre-FEC BER Current Value Media Input',
    16 : 'Pre-FEC BER Current Value Host Input',
    17 : 'Errored Frames Minimum Media Input',
    18 : 'Errored Frames Minimum Host Input',
    19 : 'Errored Frames Maximum Media Input',
    20 : 'Errored Frames Minimum Host Input',
    21 : 'Errored Frames Average Media Input',
    22 : 'Errored Frames Average Host Input',
    23 : 'Errored Frames Current Value Media Input',
    24 : 'Errored Frames Current Value Host Input',
    # oif datapath
    128 : 'Modulator Bias X/I',
    129 : 'Modulator Bias X/Q',
    130 : 'Modulator Bias Y/I',
    131 : 'Modulator Bias Y/Q',
    132 : 'Modulator Bias X_Phase',
    133 : 'Modulator Bias Y_Phase',
    134 : 'CD – high granularity, short link',
    135 : 'CD – low granularity, long link',
    136 : 'DGD',
    137 : 'SOPMD',
    138 : 'PDL',
    139 : 'OSNR',
    140 : 'eSNR',
    141 : 'CFO',
    142 : 'EVM_modem',
    143 : 'Tx Power',
    144 : 'Rx Total',
    145 : 'Rx Signal',
    146 : 'SOP ROC',
    147 : 'MER',
}

cmis_vdm_conf_lane_info = {
    0: 'Lane 1 or data path starting on lane 1',
    1: 'Lane 2 or data path on lane 2',
    2: 'Lane 3 or data path on lane 3',
    3: 'Lane 4 or single-host-lane data path on lane 4',
    4: 'Lane 5 or single-host-lane data path on lane 5',
    5: 'Lane 6 or single-host-lane data path on lane 6',
    6: 'Lane 7 or single-host-lane data path on lane 7',
    7: 'Lane 8 or single-host-lane data path on lane 8',
    15: 'Module',
}

rxamp_codes_info = {
    0: '100-400 mV',
    1: '300-600 mV',
    2: '400-800 mV',
    3: '600-1200 mV',
}

txeq_codes_info = {
    0 : 'No Eq',
    1 : '1 dB',
    2 : '2 dB',
    3 : '3 dB',
    4 : '4 dB',
    5 : '5 dB',
    6 : '6 dB',
    7 : '7 dB',
    8 : '8 dB',
    9 : '9 dB',
    10: '10 dB',
}

rxemp_codes_info = {
    0 : 'No Emphasis',
    1 : '1 dB',
    2 : '2 dB',
    3 : '3 dB',
    4 : '4 dB',
    5 : '5 dB',
    6 : '6 dB',
    7 : '7 dB',
}

pre_rxeq_codes_info = {
    0 : 'No Equalization',
    1 : '0.5 dB',
    2 : '1 dB',
    3 : '1.5 dB',
    4 : '2 dB',
    5 : '2.5 dB',
    6 : '3 dB',
    7 : '3.5 dB',
}

post_rxeq_codes_info = {
    0 : 'No Equalization',
    1 : '1 dB',
    2 : '2 dB',
    3 : '3 dB',
    4 : '4 dB',
    5 : '5 dB',
    6 : '6 dB',
    7 : '7 dB',
}