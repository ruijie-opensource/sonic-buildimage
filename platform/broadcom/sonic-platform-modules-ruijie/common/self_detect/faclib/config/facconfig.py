#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import subprocess
import time
#try:
#    from sonic_platform import get_machine_info
#    from sonic_platform import get_platform_info
#except BaseException:
#    from sonic_device_util import get_machine_info
#    from sonic_device_util import get_platform_info
import binascii
import termios
import multiprocessing

PRODUCT_RESULT_FILE = "/etc/.productname"
DFD_MY_TYPE_PATH = "/sys/module/ruijie_common/parameters/dfd_my_type"


def get_machine_info():
    if not os.path.isfile('/host/machine.conf'):
        return None
    machine_vars = {}
    with open('/host/machine.conf') as machine_file:
        for line in machine_file:
            tokens = line.split('=')
            if len(tokens) < 2:
                continue
            machine_vars[tokens[0]] = tokens[1].strip()
    return machine_vars


def get_platform_info(machine_info):
    if machine_info is not None:
        if 'onie_platform' in machine_info:
            return machine_info['onie_platform']
        elif 'aboot_platform' in machine_info:
            return machine_info['aboot_platform']
    return ""


def get_onie_machine(machine_info):
    if machine_info is not None:
        if 'onie_machine' in machine_info:
            return machine_info['onie_machine']
    return None


def get_board_id_from_file():
    if not os.path.isfile(PRODUCT_RESULT_FILE):
        return "NA"
    with open(PRODUCT_RESULT_FILE, 'r') as fd:
        ret = fd.read().strip()
        return ret

def get_dfd_my_type():
    if not os.path.isfile(DFD_MY_TYPE_PATH):
        return "NA"
    with open(DFD_MY_TYPE_PATH, 'r') as fd:
        ret = fd.read().strip()
        return str(hex(int(ret, 10)))

def get_onl_platform():
    # Determine the current platform name.
    platform = None

    # running ONL proper
    if platform is None and os.path.exists("/etc/onl/platform"):
        with open("/etc/onl/platform", 'r') as f:
            platform=f.read().strip()

    # in the middle of an ONL install
    if platform is None and os.path.exists("/etc/onl/installer.conf"):
        with open("/etc/onl/installer.conf") as f:
            lines = f.readlines(False)
            lines = [x for x in lines if x.startswith('onie_platform')]
            if lines:
                platform = lines[0].partition('=')[2].strip()

    # running ONIE
    if platform is None and os.path.exists("/bin/onie-sysinfo"):
        try:
            platform = subprocess.check_output(('/bin/onie-sysinfo', '-p',)).strip()
        except subprocess.CalledProcessError as what:
            for line in (what.output or "").splitlines():
                sys.stderr.write(">>> %s\n" % line)
            sys.stderr.write("onie-sysinfo failed with code %d\n" % what.returncode)
            platform = None

    # running ONL loader, with access to ONIE
    if platform is None and os.path.exists("/usr/bin/onie-shell"):
        try:
            platform = subprocess.check_output(('/usr/bin/onie-shell', '-c', "onie-sysinfo -p",)).strip()
        except subprocess.CalledProcessError as what:
            for line in (what.output or "").splitlines():
                sys.stderr.write(">>> %s\n" % line)
            sys.stderr.write("onie-sysinfo (onie-shell) failed with code %d\n" % what.returncode)
            platform = None

    # legacy ONIE environment (including parsable shell in machine.conf)
    if platform is None and os.path.exists("/etc/machine.conf"):
        cmd = "IFS=; . /tmp/machine.conf; set | egrep ^onie_platform="
        buf = subprocess.check_output(cmd)
        if buf:
            platform = buf.partition('=')[2].strip()
            if platform.startswith('"') or platform.startswith("'"):
                platform = ast.literal_eval(platform)
    return platform


def getbiosproductname():
    ret, val = subprocess.getstatusoutput("dmidecode -s system-product-name")
    tmp = val.lower().replace('-', '_')
    if ret != 0 or len(val) <= 0:
        return "N/A"
    else:
        return tmp


def get_mac_id(loc):
    try:
        if not os.path.exists(loc):
            msg = "mac id path: %s, not exists" % loc
            return False, msg
        with open(loc) as fd:
            id_str = fd.read().strip()
        id = int(id_str, 10)
        return True, id
    except Exception as e:
        return False, "get_mac_id Exception"


def getdeviceplatform():
    x = get_platform_info(get_machine_info())
    filepath = None
    if x is not None:
        filepath = "/usr/share/sonic/device/" + x
    return filepath


def get_board_id(machine_info):
    if machine_info is not None:
        if 'onie_board_id' in machine_info:
            return machine_info['onie_board_id'].lower()
    return "NA"


def get_mac_platform():
    ret, id = get_mac_id("/sys/module/rg_mac_bsc/parameters/mac_pcie_id")
    if ret is False:
        return ""
    if id == 0xb780:
        return "x86_64_tencent_tcs8400_r0"
    elif id == 0xb788:
        return "x86_64_tencent_tcs8410_r0"
    else:
        return ""

bios_platform = getbiosproductname()
bios_board_id_name = get_board_id_from_file()
bios_grtd_productfile = (bios_platform + "_factest_config").replace("-", "_")
bios_platform_configfile = (bios_board_id_name + "_factest_config").replace("-", "_") # platfrom + board_id
bios_card_type_configfile = (bios_platform  + "_" +  get_dfd_my_type() + "_factest_config").replace("-", "_") # platfrom + board_id

onl_platform = get_onl_platform()
if onl_platform is not None:
    onl_configfile = (onl_platform + "_factest_config").replace("-", "_")
else:
    onl_configfile = ""

mac_platform = get_mac_platform()
platform = get_platform_info(get_machine_info())  # platform         获取平台信息             x86_64-ruijie_b6520-64cq-r0
board_id = get_board_id(get_machine_info())
platformpath = getdeviceplatform()  # platformpath     获取可映射docker目录    /usr/share/sonic/device/x86_64-ruijie_b6520-64cq-r0
grtd_productfile = (platform + "_factest_config").replace("-", "_")
mac_platform_configfile = (mac_platform + "_" + board_id + "_factest_config").replace("-", "_")
platform_configfile = (platform + "_" + board_id + "_factest_config").replace("-", "_") # platfrom + board_id
configfile_pre = "/usr/local/bin/self_detect/"  # py放的目录， 暂时用/usr/local/bin 后续修订
sys.path.append(platformpath)
sys.path.append(configfile_pre)
sys.path.append("/usr/local/bin/")
sys.path.append("/usr/local/bin/ruijie/")

global module_product
if os.path.exists(configfile_pre + mac_platform_configfile + ".py"):
    module_product = __import__(mac_platform_configfile, globals(), locals(), [], 0)
elif os.path.exists(configfile_pre + platform_configfile + ".py"):
    module_product = __import__(platform_configfile, globals(), locals(), [], 0)
elif os.path.exists(configfile_pre + grtd_productfile + ".py"):
    module_product = __import__(grtd_productfile, globals(), locals(), [], 0)
elif os.path.exists(configfile_pre + bios_card_type_configfile + ".py"):
    module_product = __import__(bios_card_type_configfile, globals(), locals(), [], 0)
elif os.path.exists(configfile_pre + bios_platform_configfile + ".py"):
    module_product = __import__(bios_platform_configfile, globals(), locals(), [], 0)
elif os.path.exists(configfile_pre + bios_grtd_productfile + ".py"):
    module_product = __import__(bios_grtd_productfile, globals(), locals(), [], 0)
elif os.path.exists(configfile_pre + onl_configfile + ".py"):
    module_product = __import__(onl_configfile, globals(), locals(), [], 0)
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
RUIJIE_PRODUCTNAME_RUIJIE = module_product.RUIJIE_PRODUCTNAME if hasattr(module_product, 'RUIJIE_PRODUCTNAME_RUIJIE') else None
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
diag_manual = module_product.diag_manual if hasattr(module_product, 'diag_manual') else None
diagtestbmcall = module_product.diagtestbmcall if hasattr(module_product, 'diagtestbmcall') else None
CPLDVERSIONS = module_product.CPLDVERSIONS
