#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import os
import time
import binascii
import termios
import multiprocessing
from platform_util import *


def getdeviceplatform():
    x = getplatform_name()
    if x is not None:
        filepath = "/usr/share/sonic/device/" + x
    return filepath


platform = getplatform_name()  # platform         获取平台信息             x86_64-ruijie_{device_name}-r0
platformpath = getdeviceplatform()  # platformpath     获取可映射docker目录    /usr/share/sonic/device/x86_64-ruijie_{device_name}-r0
grtd_productfile = (platform + "_factest_config").replace("-", "_")
configfile_pre = "/usr/local/bin/"  # py放的目录， 暂时用/usr/local/bin 后续修订
sys.path.append(platformpath)
sys.path.append(configfile_pre)

global module_product
if os.path.exists(configfile_pre + grtd_productfile + ".py"):
    module_product = __import__(grtd_productfile, globals(), locals(), [], 0)
else:
    print("不存在配置文件，退出")
    exit(-1)

bcmcmdb_lock = multiprocessing.Lock()  # bcmcmdb命令加锁
TESTCASE = module_product.TESTCASE if hasattr(module_product, 'TESTCASE') else None
menuList = module_product.menuList if hasattr(module_product, 'menuList') else None
E2_LOC = module_product.E2_LOC if hasattr(module_product, 'E2_LOC') else None
rg_eeprom = "%d-%04x/eeprom" % (E2_LOC["bus"], E2_LOC["devno"])
RUIJIE_CARDID = module_product.RUIJIE_CARDID if hasattr(module_product, 'RUIJIE_CARDID') else None
FACTESTMODULE = module_product.FACTESTMODULE if hasattr(module_product, 'FACTESTMODULE') else None
alltest = module_product.alltest if hasattr(module_product, 'alltest') else None
looptest = module_product.looptest if hasattr(module_product, 'looptest') else None
factest_module = module_product.factest_module if hasattr(module_product, 'factest_module') else None
MEM_SLOTS = module_product.MEM_SLOTS if hasattr(module_product, 'MEM_SLOTS') else None
PCIe_DEV_LIST = module_product.PCIe_DEV_LIST if hasattr(module_product, 'PCIe_DEV_LIST') else None
PCIe_SPEED_ITEM = module_product.PCIe_SPEED_ITEM if hasattr(module_product, 'PCIe_SPEED_ITEM') else None
TEMPIDCHANGE = module_product.TEMPIDCHANGE if hasattr(module_product, 'TEMPIDCHANGE') else None
fanloc = module_product.fanloc if hasattr(module_product, 'fanloc') else None
fanlevel = module_product.fanlevel if hasattr(module_product, 'fanlevel') else None
STARTMODULE = module_product.STARTMODULE if hasattr(module_product, 'STARTMODULE') else None
RUIJIE_CARDID = module_product.RUIJIE_CARDID if hasattr(module_product, 'RUIJIE_CARDID') else None
RUIJIE_PRODUCTNAME = module_product.RUIJIE_PRODUCTNAME if hasattr(module_product, 'RUIJIE_PRODUCTNAME') else None
RUIJIE_PART_NUMBER = module_product.RUIJIE_PART_NUMBER if hasattr(module_product, 'RUIJIE_PART_NUMBER') else None
RUIJIE_LABEL_REVISION = module_product.RUIJIE_LABEL_REVISION if hasattr(
    module_product, 'RUIJIE_LABEL_REVISION') else None
RUIJIE_ONIE_VERSION = module_product.RUIJIE_ONIE_VERSION if hasattr(module_product, 'RUIJIE_ONIE_VERSION') else None
RUIJIE_MAC_SIZE = module_product.RUIJIE_MAC_SIZE if hasattr(module_product, 'RUIJIE_MAC_SIZE') else None
RUIJIE_MANUF_NAME = module_product.RUIJIE_MANUF_NAME if hasattr(module_product, 'RUIJIE_MANUF_NAME') else None
RUIJIE_MANUF_COUNTRY = module_product.RUIJIE_MANUF_COUNTRY if hasattr(module_product, 'RUIJIE_MANUF_COUNTRY') else None
RUIJIE_VENDOR_NAME = module_product.RUIJIE_VENDOR_NAME if hasattr(module_product, 'RUIJIE_VENDOR_NAME') else None
RUIJIE_DIAG_VERSION = module_product.RUIJIE_DIAG_VERSION if hasattr(module_product, 'RUIJIE_DIAG_VERSION') else None
RUIJIE_SERVICE_TAG = module_product.RUIJIE_SERVICE_TAG if hasattr(module_product, 'RUIJIE_SERVICE_TAG') else None
STARTMENUID = module_product.STARTMENUID if hasattr(module_product, 'STARTMENUID') else None
E2_PROTECT = module_product.E2_PROTECT if hasattr(module_product, 'E2_PROTECT') else None
DEVICE = module_product.DEVICE if hasattr(module_product, 'DEVICE') else None
FRULISTS = module_product.FRULISTS if hasattr(module_product, 'FRULISTS') else None
FANS_DEF = module_product.FANS_DEF if hasattr(module_product, 'FANS_DEF') else None
FAN_PROTECT = module_product.FAN_PROTECT if hasattr(module_product, 'FAN_PROTECT') else None
diagtestall = module_product.diagtestall if hasattr(module_product, 'diagtestall') else None
CPLDVERSIONS = module_product.CPLDVERSIONS
