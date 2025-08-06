'''
e2_bus_id:
    continues >> key: start bus id, val: port range
    single >> key: bus id, val: port
'''
sff_conf = {
    "port_first_index": 1,
    "qsfp_dd_ports": "1-56",
    "ports_num": 56,
    "present_val": 0,
    "presence_cpld_info": {
        "dev_id": {
            4: {
                "offset": {
                    0x30: "41-48",
                    0x31: "49-56",
                },
            },
            5: {
                "offset": {
                    0x30: "1-8",
                    0x31: "9-13, 15, 22, 24",
                    0x32: "31-32, 35",
                },
            },
            7: {
                "offset": {
                    0x30: "14, 16-21, 23",
                    0x31: "25-30, 33-34",
                    0x32: "36-40",
                },
            },
        },
    },
}
