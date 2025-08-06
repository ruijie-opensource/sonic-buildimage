'''
e2_bus_id:
    continues >> key: start bus id, val: port range
    single >> key: bus id, val: port
'''
sff_conf = {
    "port_first_index": 1,
    "qsfp_dd_ports": "1-64",
    "ports_num": 64,
    "present_val": 0,
    "presence_cpld_info": {
        "dev_id": {
            4: {
                "offset": {
                    0x71: "49-50, 53-54, 57-58, 61-62",
                },
            },
            5: {
                "offset": {
                    0x73: "1-2, 5-6, 9-10, 13-14",
                    0x74: "17-18, 21-22, 25-26, 29-30",
                    0x75: "33-34, 37-38, 41-42, 45-46",
                },
            },
            6: {
                "offset": {
                    0x72: "3-4, 7-8, 11-12, 15-16",
                    0x73: "20, 23-24, 27-28, 31-32",
                },
            },
            7: {
                "offset": {
                    0x73: "19, 35-36, 39-40, 43-44, 47",
                    0x74: "48, 51-52, 55-56, 59-60, 63",
                    0x75: "64",
                },
            },
        },
    },
}
