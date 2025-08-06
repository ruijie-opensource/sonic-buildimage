#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import re
from faclib.factool.rgutil import *

class SdkCmdBase():
    port_enable_cmd = None
    port_disable_cmd = None
    get_sdk_version_cmd = None
    get_phypcie_version_cmd = None
    show_81724_version_cmd = None
    test_sdk_cmd = None
    set_port_mac_lb_cmd = None
    cancel_port_mac_lb_cmd = None
    show_mac_temp_cmd = None

    def log_debug(msg, also_print_to_console=False):  # todo 单独一个log类，加入调用函数和具体行号以及时间戳
        try:
            funcName = sys._getframe().f_back.f_code.co_name  # 获取调用函数名
            lineNumber = sys._getframe().f_back.f_lineno  # 获取行号
            time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 含微秒的日期时间
            info_str = time_now + funcName + ": " + str(lineNumber)
            log_msg = "%-40s| %s" % (info_str, str(msg))
            syslog.openlog("SDKCMD")
            syslog.syslog(syslog.LOG_DEBUG, log_msg)
            syslog.closelog()

            if also_print_to_console:
                click.echo(msg)
        except Exception as e:
            pass

    def sdkcmd_os_system(self, cmd):
        log_debug(cmd)
        status, output = subprocess.getstatusoutput(cmd)
        return status, output

    def get_sdk_version(self):
        ret, log = self.sdkcmd_os_system(self.get_sdk_version_cmd)
        if ret:
            return False
        else:
            version_temp = re.subn("(      \r\n)|(   \r\n\r\r\ndrivshell>)|(version\r\r)", "", log)[0]
            version_clean = re.subn("\n", "\n\t", version_temp)[0]
            return version_clean

    def get_phypcie_version(self):
        ret1, loader = self.sdkcmd_os_system("%s|grep \'PCIe FW loader version\'|cut -d : -f 2" % self.get_phypcie_version_cmd)
        ret2, version = self.sdkcmd_os_system("%s|grep \'PCIe FW version\'|cut -d : -f 2" % self.get_phypcie_version_cmd)
        ret3, loader_built = self.sdkcmd_os_system("%s|grep \'PCIe FW loader built date\'|cut -d : -f 2" % self.get_phypcie_version_cmd)
        return loader, version, loader_built

    def test_sdk(self):
        ret, log = self.sdkcmd_os_system(self.test_sdk_cmd)
        return ret, log

    def set_port_mac_lb(self):
        bmc_cmd = "port all en=1 lb=mac"
        ret, log = self.sdkcmd_os_system(self.set_port_mac_lb_cmd)
        if ret or bmc_cmd not in log:
            log_debug("set_port_mac_lb fail %s" % log)
            return False
        return True

    def cancel_port_mac_lb(self):
        bmc_cmd = "port all lb=none"
        ret, log = self.sdkcmd_os_system(self.cancel_port_mac_lb_cmd)
        if ret or bmc_cmd not in log:
            log_debug("cancel_port_mac_lb fail %s" % log)
            return False
        return True


class SdkCmdb(SdkCmdBase):
    # bcmcmdb
    bcmcmdb_lock = None  # 共享内存锁

    def __init__(self, lock):
        self.bcmcmdb_lock = lock
        self.get_sdk_version_cmd = "bcmcmdb 'version' < /dev/null | grep Release"
        self.get_phypcie_version_cmd = 'bcmcmdb -t 5 \"dsh -c \'PCIEphy fwinfo\'\" < /dev/null |grep PCIe'
        self.test_sdk_cmd = "bcmcmdb -t 5 ps < /dev/null"
        self.set_port_mac_lb_cmd = "bcmcmdb \"port all en=1 lb=mac\" < /dev/null"
        self.cancel_port_mac_lb_cmd = "bcmcmdb \"port all lb=none\" < /dev/null"
        self.show_mac_temp_cmd = "bcmcmdb \"dsh -c 'hmon temperature'\" |sed -n '6,14p'"  # 当前未计算sensor9 等sdk更新后修订

    def sdkcmd_os_system(self, cmd):
        log_debug(cmd)
        with self.bcmcmdb_lock:
            status, output = subprocess.getstatusoutput(cmd)
        return status, output

    def show_max_mac_temp(self):
        ret, log = self.sdkcmd_os_system(self.show_mac_temp_cmd)
        if ret:
            return False, None
        else:
            logs = log.splitlines()
            max_temp = 0
            for line in logs:
                tmp = line.split("\t\t")
                a = float(tmp[3])
                if a > max_temp:
                    max_temp = a
            return True, max_temp

    def show_aver_mac_temp(self):
        ret, log = self.sdkcmd_os_system(self.show_mac_temp_cmd)
        if ret:
            return False, None
        else:
            logs = log.splitlines()
            temp_total = 0
            for line in logs:
                tmp = line.split("\t\t")
                a = float(tmp[3])
                temp_total += float(tmp[1])
            aver_temp = temp_total / (len(logs))
            return True, aver_temp


class SdkCmdscd(SdkCmdBase):
    # bcmcmdscd
    bcmcmdb_lock = None  # 共享内存锁

    def __init__(self, lock):
        self.bcmcmdb_lock = lock
        self.get_sdk_version_cmd = "scdcmd 'version' < /dev/null | grep Release | cut -d : -f 2-4"
        self.get_phypcie_version_cmd = 'scdcmd -t 5 \"dsh -c \'PCIEphy fwinfo\'\" < /dev/null |grep PCIe'
        self.test_sdk_cmd = "scdcmd -t 5 ps < /dev/null"
        self.set_port_mac_lb_cmd = "scdcmd \"port all en=1 lb=mac\" < /dev/null"
        self.cancel_port_mac_lb_cmd = "scdcmd \"port all lb=none\" < /dev/null"
        self.show_mac_temp_cmd = "scdcmd \"dsh -c 'hmon temperature'\" |sed -n '6,14p'"  # 当前未计算sensor9 等sdk更新后修订

    def sdkcmd_os_system(self, cmd):
        log_debug(cmd)
        with self.bcmcmdb_lock:
            status, output = subprocess.getstatusoutput(cmd)
        return status, output

    def show_max_mac_temp(self):
        ret, log = self.sdkcmd_os_system(self.show_mac_temp_cmd)
        if ret:
            return False, None
        else:
            logs = log.splitlines()
            max_temp = 0
            for line in logs:
                tmp = line.split("\t\t")
                a = float(tmp[3])
                if a > max_temp:
                    max_temp = a
            return True, max_temp

    def show_aver_mac_temp(self):
        ret, log = self.sdkcmd_os_system(self.show_mac_temp_cmd)
        if ret:
            return False, None
        else:
            logs = log.splitlines()
            temp_total = 0
            for line in logs:
                tmp = line.split("\t\t")
                a = float(tmp[3])
                temp_total += float(tmp[1])
            aver_temp = temp_total / (len(logs))
            return True, aver_temp


class SdkCmd(SdkCmdBase):
    def __init__(self):
        self.port_enable_cmd = "bcmcmd \"port %s en=1\""
        self.port_disable_cmd = "bcmcmd \"port %s en=0\""
        self.get_sdk_version_cmd = "bcmcmd 'version' < /dev/null | grep Release |cut -d : -f 2-4"
        self.get_phypcie_version_cmd = TESTCASE.get("get_phypcie_version_cmd", None)
        self.show_81724_version_cmd = 'bcmcmd "phy control  ce fw_get" < /dev/null'
        self.show_mac_temp_cmd = TESTCASE.get("show_mac_temp_cmd", None)
        self.test_sdk_cmd = "bcmcmd -t 1 ps < /dev/null"
        self.set_port_mac_lb_cmd = "bcmcmd \"port all en=1 lb=mac\" < /dev/null"
        self.cancel_port_mac_lb_cmd = "bcmcmd \"port all lb=none\" < /dev/null"

    def port_enable(self):
        ret, log = self.sdkcmd_os_system(self.port_enable_cmd)
        return ret, log

    def port_disable(self):
        ret, log = self.sdkcmd_os_system(self.port_disable_cmd)
        return ret, log

    def show_81724_version(self):
        version = None
        ret, log = self.sdkcmd_os_system(self.show_81724_version_cmd)
        if ret == 0:
            for line in log.splitlines():
                if "fw_version" in line:
                    if "success" not in line:
                        return False, "success get fail"
                    else:
                        versiontmp = re.findall(r"fw_version=(.+?) ", line)[0]
                        if version is None:
                            version = versiontmp
                        else:
                            if version != versiontmp:
                                return False, "81724 version error %s != %s" % (versiontmp, version)
                else:
                    pass
        else:
            return False, "%s cmd fail" % self.show_81724_version_cmd
        return True, version

    def show_max_mac_temp(self):
        ret, log = self.sdkcmd_os_system(self.show_mac_temp_cmd)
        if ret:
            return False, None
        else:
            logs = log.splitlines()
            max_temp = 0
            for line in logs:
                tmp = line.split("\t\t")
                a = float(tmp[3])
                if a > max_temp:
                    max_temp = a
            return True, max_temp

    def show_aver_mac_temp(self):
        ret, log = self.sdkcmd_os_system(self.show_mac_temp_cmd)
        if ret:
            return False, None
        else:
            logs = log.splitlines()
            temp_total = 0
            for line in logs:
                tmp = line.split("\t\t")
                a = float(tmp[3])
                temp_total += float(tmp[1])
            aver_temp = temp_total / (len(logs))
            return True, aver_temp


def TestSdkCmd():
    # cmd列表顺序需与定义的sdkcmd对应
    cmdlist = ["bcmcmd -t 1 ps < /dev/null", "bcmcmdb -t 5 ps < /dev/null", "scdcmd -t 5 ps < /dev/null"]
    i = 0
    for cmd in cmdlist:
        ret, log = subprocess.getstatusoutput(cmd)
        if ret == 0:
            return i
        i += 1
    return 0


def SdkCmdChoose():
    version = TESTCASE.get("sdkcmdversion", 0)  # 0bcmcmd  1bcmcmdb
    if version == -1:
        #探测sdk cmd
        version = TestSdkCmd()

    if version == 1:
        log_debug("return SdkCmdb")
        return SdkCmdb(bcmcmdb_lock)
    elif version == 2:
        log_debug("return SdkCmdscd")
        return SdkCmdscd(bcmcmdb_lock)
    else:
        log_debug("return SdkCmd")
        return SdkCmd()


SdkCmdCase = SdkCmdChoose()  # 避免多次初始化
