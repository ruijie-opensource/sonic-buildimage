#!/usr/bin/python
# -*- coding: UTF-8 -*-

SSD_ATTR_LIST = [
    {
        "model": "SSDSCKKB240G8",
        "attrs": [
            {"attr_name": "Bad block increase number", "id": 0x05},
            {"attr_name": "Write failures times", "id": 0xab},
            {"attr_name": "Erase failed test", "id": 0xac},
            {"attr_name": "Remaining life", "id": 0xe9, "life" : 95},
            {"attr_name": "PLP capacity", "id": 0xaf},
            {"attr_name": "SATA CRC", "id": 0xc7, "warning": 1, "critical": 2},
            {"attr_name": "SATA spin down", "id": 0xb7, "warning": 1, "critical": 2},
            {"attr_name": "E2E error", "id": 0xb8, "warning": 1, "critical": 2},
            {"attr_name": "Temperature", "id": 0xbe, "min": -20, "max": 70},
        ],
    },
    {
        "model": "SSDSCKKB480GZ",
        "attrs": [
            {"attr_name": "Bad block increase number", "id": 0x05},
            {"attr_name": "Write failures times", "id": 0xab},
            {"attr_name": "Erase failed test", "id": 0xac},
            {"attr_name": "Remaining life", "id": 0xe9, "life" : 95},
            {"attr_name": "PLP capacity", "id": 0xaf},
            {"attr_name": "SATA CRC", "id": 0xc7, "warning": 1, "critical": 2},
            {"attr_name": "SATA spin down", "id": 0xb7, "warning": 1, "critical": 2},
            {"attr_name": "E2E error", "id": 0xb8, "warning": 1, "critical": 2},
            {"attr_name": "Temperature", "id": 0xbe, "min": -20, "max": 70},
        ],
    },
    {
        "model": "AF2MA31DTDLT240A",
        "attrs": [
            {"attr_name": "Bad block increase number", "id": 0x05},
            {"attr_name": "Write failures times", "id": 0xab},
            {"attr_name": "Erase failed test", "id": 0xac},
            {"attr_name": "Remaining life", "id": 0xca, "life" : 95},
            {"attr_name": "PLP capacity", "id": 0xaf},
            {"attr_name": "SATA CRC", "id": 0xc7, "warning": 1, "critical": 2},
            {"attr_name": "SATA spin down", "id": 0xb7, "warning": 1, "critical": 2},
            {"attr_name": "E2E error", "id": 0xb8, "warning": 1, "critical": 2},
            {"attr_name": "Temperature", "id": 0xc2, "min": -20, "max": 70},
        ],
    },
    {
        "model": "ER2-GD240",
        "attrs": [
            {"attr_name": "Bad block increase number", "id": 0x05},
            {"attr_name": "Write failures times", "id": 0xab},
            {"attr_name": "Erase failed test", "id": 0xac},
            {"attr_name": "Remaining life", "id": 0xca, "life" : 95},
            {"attr_name": "PLP capacity", "id": 0xe5},
            {"attr_name": "SATA CRC", "id": 0xc7, "warning": 1, "critical": 2},
            {"attr_name": "SATA spin down", "id": 0xb7, "warning": 1, "critical": 2},
            {"attr_name": "E2E error", "id": 0xb8, "warning": 1, "critical": 2},
            {"attr_name": "Temperature", "id": 0xbe, "min": -20, "max": 70},
        ],
    },
    {
        "model": "ER2-GD480",
        "attrs": [
            {"attr_name": "Bad block increase number", "id": 0x05},
            {"attr_name": "Write failures times", "id": 0xab},
            {"attr_name": "Erase failed test", "id": 0xac},
            {"attr_name": "Remaining life", "id": 0xca, "life" : 95},
            {"attr_name": "PLP capacity", "id": 0xe5},
            {"attr_name": "SATA CRC", "id": 0xc7, "warning": 1, "critical": 2},
            {"attr_name": "SATA spin down", "id": 0xb7, "warning": 1, "critical": 2},
            {"attr_name": "E2E error", "id": 0xb8, "warning": 1, "critical": 2},
            {"attr_name": "Temperature", "id": 0xbe, "min": -20, "max": 70},
        ],
    },
    {
        "model": "SM619GXC DES",
        "attrs": [
            {"attr_name": "Bad block increase number", "id": 0x05},
            {"attr_name": "Write failures times", "id": 0xf6},
            {"attr_name": "Erase failed test", "id": 0xf7},
            {"attr_name": "Remaining life", "id": 0xa9, "life" : 95},
            {"attr_name": "SATA CRC", "id": 0xc7, "warning": 1, "critical": 2},
            {"attr_name": "Temperature", "id": 0xc2, "min": -20, "max": 70, "convert": True},
        ],
    },
    {
        "model": "MZNLH240HBJQ-00005",
        "attrs": [
            {"attr_name": "Bad block increase number", "id": 0x05},
            {"attr_name": "Write failures times", "id": 0xb5},
            {"attr_name": "Erase failed test", "id": 0xb6},
            {"attr_name": "Remaining life", "id": 0xf5, "life" : 95},
            {"attr_name": "SATA CRC", "id": 0xc7, "warning": 1, "critical": 2},
            {"attr_name": "SATA spin down", "id": 0xf3, "warning": 1, "critical": 2, "ignore": 1},
            {"attr_name": "E2E error", "id": 0xb8, "warning": 1, "critical": 2},
            {"attr_name": "Temperature", "id": 0xbe, "min": -20, "max": 70},
        ],
    },
    {
        "model": "MZNLH480HBLR-00005",
        "attrs": [
            {"attr_name": "Bad block increase number", "id": 0x05},
            {"attr_name": "Write failures times", "id": 0xb5},
            {"attr_name": "Erase failed test", "id": 0xb6},
            {"attr_name": "Remaining life", "id": 0xf5, "life" : 95},
            {"attr_name": "SATA CRC", "id": 0xc7, "warning": 1, "critical": 2},
            {"attr_name": "SATA spin down", "id": 0xf3, "warning": 1, "critical": 2, "ignore": 1},
            {"attr_name": "E2E error", "id": 0xb8, "warning": 1, "critical": 2},
            {"attr_name": "Temperature", "id": 0xbe, "min": -20, "max": 70},
        ],
    },
    {
        "model": "ADATA_IM2S3134N-064GM",
        "attrs": [
            {"attr_name": "Bad block increase number", "id": 0xa9},
            {"attr_name": "Erase failed test", "id": 0xad},
            {"attr_name": "Remaining life", "id": 0xe7, "life" : 95},
        ],
    },
]

