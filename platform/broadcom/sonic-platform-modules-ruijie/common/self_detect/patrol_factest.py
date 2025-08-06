#!/usr/bin/python
# -*- coding: UTF-8 -*-
from faclib.all import *
import os
import sys
import signal
import time
import threading
import xml.etree.ElementTree as ET
import hashlib
import subprocess
import re
import datetime
import syslog
import fcntl
import logging
import subprocess
import json
import unicodedata
import tty
import glob
import mmap
from tabulate import tabulate
import traceback
from datetime import datetime
try:
    import pexpect
except:
    pass
from common_config import *
from platform_util import *
try:
    import platform_manufacturer
except Exception as e:
    pass

PYTHON_VERSION = sys.version_info.major

SCRIPT_VERSION = 20230404

RETURN_KEY3 = "code2" #测试项是否失败标识
MAILBOX_DIR = "/sys/bus/i2c/devices/"  # sysfs 顶层目录
PORTS_DIR = "/sys/class/net/"
#from scapy.all import sendp, Ether, ARP
# from monitor import status
import configparser

GRTD_BROADCAST_RETRY_SLEEP_TIME  = 3
G_BMCIP = None
OPENBMC_PASSWORD = "0penBmc"
BMC_DIAG_CONF_FILE_PATH = "/tmp/factest/bmc_factest/"
BMC_PATH = "PATH=/usr/sbin/:/bin/:/usr/bin/:/sbin/:/usr/local/bin"

Inspection_START_TIME = None

'''
from ruijieutil import *
import grtd_test as gt
from tabulate import tabulate
from faclib.rest import HttpRest

fan_check           = gt.fan_check
get_sysfs_value     = gt.get_sysfs_value
test_port           = gt.test_port
test_port_prbs      = gt.test_port_prbs
test_port_portframe = gt.test_port_portframe
stopFanctrol        = gt.stopFanctrol
startFanctrol       = gt.startFanctrol
test_ports_prbs_new = gt.test_ports_prbs_new
'''
# ===================================================================
# 测试项:内存ECC检测
# ===================================================================
def test_ddr_ecc():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2:""}

    ecc_cmd = TESTCASE.get("ECC_CMD", None)
    if ecc_cmd is None:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "获取ECC_CMD配置错误"
        RJPRINT([RETURN_KEY2])
        return RET
    for item in ecc_cmd:
        cmd = item.get("cmd", None)
        keyword = item.get("keyword", None)
        check_len = item.get("check_len", None)
        ret, log = log_os_system(cmd, 0)
        if ret != 0 or len(log) == 0:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "[%s]命令执行出错 : %s" % (cmd, log)
            RJPRINT("%s" % RET[RETURN_KEY2])
            return RET

        total_len = 0
        for key in keyword:
            result = re.findall('%s\s+.*' % key, log)
            if len(result) > 0:
                line = result[-1]
                RJPRINT("%s" % line)
                total_len += line.replace(key, '').count('00')
            else:
                RJPRINT("%s" % log)
        if total_len != check_len:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "命令[%s]执行结果：预期\'00\'个数为%d, 实际个数为%d" % (cmd, check_len, total_len)
            RJPRINT(RET[RETURN_KEY2])
        RJPRINT("")
    return RET

def test_check_syslog(error_log_list=[]):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    error_log_list = list(set(error_log_list))
    cmd='zgrep -m 10 "{}" -na /var/log/syslog*'.format('\|'.join(error_log_list))
    ret,log = log_cmd_raise(cmd,regexp="(^\s*$)",status_ignore=True,ei="找到以上异常log")
    if ret is False:
        RET[RETURN_KEY1] = -1
    else:
        RET[RETURN_KEY2] = "无异常log"
        RJPRINT(RET[RETURN_KEY2])
    return RET

def test_mac_ecc():
    error_log_list = [
        "A parity error occurs",
        "An ECC error occurs",
        "ECC exception repair failed",
        "ECC has many exceptions and cannot be repaired. Please restart the device",
        "ECC exception has been fixed",
    ]
    return test_check_syslog(error_log_list)

# ===================================================================
# 测试项:CPU中断测试
# ===================================================================
def test_cpu_irq():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}

    for test_item in TESTCASE.get("IRQ_TEST", None):
        RJPRINT("")
        data1 = 0
        data2 = 0
        cmd = test_item.get("GetIrq", None)
        ret, val = log_os_system(cmd, True)
        if ret or len(val) == 0:
            RET[RETURN_KEY1] -= 1
        else:
            data1 = int(val,16)

        commands = test_item.get("SetBaseIrq", None)
        ret, val = send_commands(commands, True)
        if ret == False:
            RET[RETURN_KEY1] -= 1
            RJPRINT("%s : FAIL" % (test_item["test_name"]))
            continue

        ret, val = log_os_system(cmd, True)
        if ret or len(val) == 0:
            RET[RETURN_KEY1] -= 1
        else:
            data2 = int(val,16)
        if data2 > data1:
            RJPRINT("%s : PASS" % (test_item["test_name"]))
        commands = test_item.get("ClearBaseIrq", None)
        ret, val = send_commands(commands, True)
        if ret == False:
            RET[RETURN_KEY1] -= 1

    return RET

def port_present_check():
    pass_list = []
    failed_list = []
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    ret, log = log_os_system("show interfaces transceiver presence | grep -a -E '^Ethernet'", 0)
    if "Traceback" in log:
        RJPRINT( "在位检测失败，请确认光模块是否在位")
    else:
        log,times = re.subn("Ethernet\d{1,3}\s*","",log)
        if len(log) == 0:
            RET[RETURN_KEY1] = -1
            return RET
        dev_list = log.split("\n")
        i = 1
        for dev in dev_list:
            if "Not present" in dev:
                failed_list.append(i)
            else:
                pass_list.append(i)
            i += 1
        if len(failed_list) > 0:        #有失败端口则打印
            RJPRINT( "光模块在位情况：")
            port_totalprint(pass_list, "OK")
            port_totalprint(failed_list, "failed")
        if ret or "FAILED" in log:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = log
    if ret or "Not" in log or "Unknown" in log:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = log
    return RET

def mask_i2c_set(cfg_list, set_val_num):
    RET = {RETURN_KEY1:0, RETURN_KEY2:""}
    for cfg_item in cfg_list:
        bus = cfg_item.get("bus", None)
        addr = cfg_item.get("addr", None)
        reg = cfg_item.get("reg", None)
        set_val_x = "set_val_%d" % set_val_num
        set_val = cfg_item.get(set_val_x, None)
        if bus is None or addr is None or reg is None or set_val is None:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "mask i2c param get failed"
            return RET
        log_debug("mask get i2c param, bus:%d, addr:0x%x, reg:0x%x, set_val:0x%x"
            % (bus, addr, reg, set_val))

        ret, log = rji2cset(bus, addr, reg, set_val)
        if ret == False:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] += "mask i2cset failed.bus:%d, addr:0x%x, reg:0x%x, set_val:0x%x, log:%s\n" % (bus, addr, reg, set_val, log)
        time.sleep(0.1)
    return RET

def rangei2cset_and_i2ccheck(set_list, check_list, val_num):
    RET = {RETURN_KEY1:0, RETURN_KEY2:"", "failed":[], "success":[]}
    startbus = set_list.get("startbus", None)
    endbus = set_list.get("endbus", None)
    startportnum = set_list.get("startportnum", None)
    addr = set_list.get("addr", None)
    reg = set_list.get("reg", None)
    set_val_x = "set_val_%d" % val_num
    set_val = set_list.get(set_val_x, None)
    if startbus is None or endbus is None or startportnum is None or addr is None or reg is None or set_val is None:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "port %s i2c param get failed" % startportnum
        return RET
    log_debug("get rangebus i2c param, startbus:%d, endbus:%d, startportnum:%d, addr:0x%x, reg:0x%x, set_val:0x%x"
        % (startbus,  endbus, startportnum, addr, reg, set_val))

    for bus in range(startbus, endbus + 1):
        ret, log = rji2cset(bus, addr, reg, set_val)
        if ret == False:
            port_num = bus - startbus + startportnum
            RET["failed"].append(port_num)
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] += "port %d i2cset failed.bus:%d, addr:0x%x, reg:0x%x, set_val:0x%x, log:%s\n"  % (port_num, bus, addr, reg, set_val, log)
        time.sleep(0.1)
    time.sleep(5)
    for cfg_item in check_list:
        bus = cfg_item.get("bus", None)
        addr = cfg_item.get("addr", None)
        reg = cfg_item.get("reg", None)
        check_bit = cfg_item.get("check_bit", None)
        port_num = cfg_item.get("port_num", None)
        ok_val_x = "ok_val_%d" % val_num
        ok_val = cfg_item.get(ok_val_x, None)
        if bus is None or addr is None or reg is None or ok_val is None:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "status check port %s get i2c param failed" % port_num
            return RET
        log_debug("status check get i2c param, bus:%d, addr:0x%x, reg:0x%x, check_bit:%d, port_num:%d, ok_val:%d"
            % (bus, addr, reg, check_bit, port_num, ok_val))

        if port_num in RET["failed"]:
            continue

        time.sleep(0.1)
        ret, val = rji2cget(bus, addr, reg)
        if ret == False:
            RET["failed"].append(port_num)
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] += "status check i2cget port %d failed. bus:%d, addr:0x%x, reg:0x%x\n" % (port_num, bus, addr, reg)
            continue

        val_t = (int(val, 16) & (1 << check_bit)) >> check_bit
        if val_t != ok_val:
            RET[RETURN_KEY1] = -1
            RET["failed"].append(port_num)
            RET[RETURN_KEY2] += "port %d status check error. bus:%d, addr:0x%x, reg:0x%x\n" % (port_num, bus, addr, reg)
        else:
            RET["success"].append(port_num)
    return RET

def rangei2cset_and_i2ccheck_new(set_list, check_list, val_num):
    RET = {RETURN_KEY1:0, RETURN_KEY2:"", "failed":[], "success":[]}
    for set_list_num in set_list:
        startbus = set_list_num.get("startbus", None)
        endbus = set_list_num.get("endbus", None)
        startportnum = set_list_num.get("startportnum", None)
        addr = set_list_num.get("addr", None)
        reg = set_list_num.get("reg", None)
        set_bit = set_list_num.get("set_bit", None)
        set_val_x = "set_val_%d" % val_num
        set_val = set_list_num.get(set_val_x, None)
        if startbus is None or endbus is None or startportnum is None or addr is None or reg is None or set_bit is None or set_val is None:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "port %s i2c param get failed" % startportnum
            return RET
        log_debug("get rangebus i2c param, startbus:%d, endbus:%d, startportnum:%d, addr:0x%x, reg:0x%x, set_bit:%d, set_val:0x%x"
            % (startbus,  endbus, startportnum, addr, reg, set_bit, set_val))

        for bus in range(startbus, endbus + 1):
            port_num = bus - startbus + startportnum
            ret, val = rji2cget(bus, addr, reg)
            if ret == False:
                RET["failed"].append(port_num)
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] += "port %d i2cset failed. bus:%d, addr:0x%x, reg:0x%x\n" % (port_num, bus, addr, reg)
                continue
            set_val_t = int(val, 16) & (~(1 << set_bit))
            set_val_t |= set_val << set_bit
            ret, log = rji2cset(bus, addr, reg, set_val_t)
            if ret == False:
                RET["failed"].append(port_num)
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] += "port %d i2cset failed.bus:%d, addr:0x%x, reg:0x%x, set_val:0x%x, log:%s\n"  % (port_num, bus, addr, reg, set_val_t, log)
            time.sleep(0.1)
    time.sleep(1)
    for cfg_item in check_list:
        bus = cfg_item.get("bus", None)
        addr = cfg_item.get("addr", None)
        reg = cfg_item.get("reg", None)
        check_bit = cfg_item.get("check_bit", None)
        port_num = cfg_item.get("port_num", None)
        ok_val_x = "ok_val_%d" % val_num
        ok_val = cfg_item.get(ok_val_x, None)
        if bus is None or addr is None or reg is None or ok_val is None:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "status check port %s get i2c param failed" % port_num
            return RET
        log_debug("status check get i2c param, bus:%d, addr:0x%x, reg:0x%x, check_bit:%d, port_num:%d, ok_val:%d"
            % (bus, addr, reg, check_bit, port_num, ok_val))
        if port_num in RET["failed"]:
            continue
        time.sleep(0.1)
        ret, val = rji2cget(bus, addr, reg)
        if ret == False:
            RET["failed"].append(port_num)
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] += "status check i2cget port %d failed. bus:%d, addr:0x%x, reg:0x%x\n" % (port_num, bus, addr, reg)
            continue
        val_t = (int(val, 16) & (1 << check_bit)) >> check_bit
        if val_t != ok_val:
            RET[RETURN_KEY1] = -1
            RET["failed"].append(port_num)
            RET[RETURN_KEY2] += "port %d status check error. bus:%d, addr:0x%x, reg:0x%x\n" % (port_num, bus, addr, reg)
        else:
            RET["success"].append(port_num)
    return RET

def test_lssignal_int():
    RET = {RETURN_KEY1:0, RETURN_KEY2:""}
    RET = port_present_check()
    if RET[RETURN_KEY1] != 0:
        RJPRINT( "测试失败，请确保所有光模块在位后再重新测试")
        return RET
    LSSIGNAL_INT = TESTCASE.get("LSSIGNAL_INT", None)
    for int_item in LSSIGNAL_INT:
        type = int_item.get("type", None)
        mask_item = int_item.get("mask_list", None)
        loopback_item = int_item.get("loopback_list", None)
        status_item = int_item.get("status_list", None)
        if type is None or mask_item is None or loopback_item is None or status_item is None:
            log_debug("type:%s, mask_item:%s, loopback_item:%s, status_item:%s"
                % (type, mask_item, loopback_item, status_item))
            RJPRINT( "测试失败，相关配置文件缺失，请确认后再重新测试")
            RET[RETURN_KEY1] = -1
            return RET

        RET1_1 = mask_i2c_set(mask_item, 1);    #屏蔽中断
        if RET1_1[RETURN_KEY1] == 0:
            RET2_1 = rangei2cset_and_i2ccheck(loopback_item, status_item, 1);   #光模块设置val1并检测状态
            RJPRINT( "******************* %s光模块int引脚输出低电平测试 *******************" % type)
            port_totalprint(RET2_1["success"], "成功端口：          ")
            port_totalprint(RET2_1["failed"], "失败端口：          ")
            if len(RET2_1["failed"]) > 0:
                errmes = print_port_sn(RET2_1["failed"], "ErroMes")
                RJPRINT( "%s" % errmes)

            if RET2_1[RETURN_KEY1] != 0:
                RJPRINT( "################################################ " )
                RJPRINT( " %s光模块int引脚输出低电平测试失败, log:\n%s " % (type, RET2_1[RETURN_KEY2]))
                RJPRINT( "################################################ ")

            RET2_2 = rangei2cset_and_i2ccheck(loopback_item, status_item, 2);   #光模块设置val2并检测状态
            RJPRINT( "******************* %s光模块int引脚输出高电平测试 *******************" % type)
            port_totalprint(RET2_2["success"], "成功端口：          ")
            port_totalprint(RET2_2["failed"], "失败端口：          ")
            if len(RET2_2["failed"]) > 0:
                errmes = print_port_sn(RET2_2["failed"], "ErroMes")
                RJPRINT( "%s" % errmes)

            if RET2_2[RETURN_KEY1] != 0:
                RJPRINT( "################################################ " )
                RJPRINT( " %s光模块int引脚输出高电平测试失败, log:\n%s " % (type, RET2_2[RETURN_KEY2]))
                RJPRINT( "################################################ ")
        else:
            RJPRINT( "################################################ " )
            RJPRINT( " %s光模块中断屏蔽失败, log:\n%s " % (type, RET1_1[RETURN_KEY2]))
            RJPRINT( "################################################ ")
        RET1_2 = mask_i2c_set(mask_item, 2);     #恢复中断
        if RET1_2[RETURN_KEY1] != 0:
            RJPRINT( "################################################ " )
            RJPRINT( " %s光模块中断恢复失败, log:\n%s " % (type, RET1_2[RETURN_KEY2]))
            RJPRINT( "################################################ ")
        if RET1_1[RETURN_KEY1] != 0 or RET1_2[RETURN_KEY1] != 0 or RET2_1[RETURN_KEY1] != 0 or RET2_2[RETURN_KEY1] != 0:
            RET[RETURN_KEY1] = -1
            log_debug("############ %s光模块测试Failed ############" % type)
    return RET

def test_lssignal_access(param):
    RET = {RETURN_KEY1:0, RETURN_KEY2:""}
    RET = port_present_check();
    if RET[RETURN_KEY1] != 0:
        RJPRINT( "测试失败，请确保所有光模块在位后再重新测试")
        return RET
    LSSIGNAL_ACCESS = TESTCASE.get(param, None)
    for item in LSSIGNAL_ACCESS:
        type = item.get("type", None)
        mask_item = item.get("mask_list", None)
        access_item = item.get("access_list", None)
        if type is None or  mask_item is None or  access_item is None:
            log_debug("type:%s, mask_item:%s, access_item:%s" % (type, mask_item, access_item))
            RJPRINT( "测试失败，相关配置文件缺失，请确认后再重新测试")
            RET[RETURN_KEY1] = -1
            return RET

        startbus = access_item.get("startbus", None)
        endbus = access_item.get("endbus", None)
        addr = access_item.get("addr", None)
        reg = access_item.get("reg", None)
        startportnum = access_item.get("startportnum", None)
        if startbus is None or endbus is None or addr is None or reg is None or startportnum is None:
            RJPRINT( "测试失败，相关配置参数缺失，请确认后再重新测试")
            RET[RETURN_KEY1] = -1
            return RET
        log_debug("lssignal access get param. startbus:%d, endbus:%d addr:0x%x, reg:0x%x, startportnum:%d"
            % (startbus, endbus, addr, reg, startportnum))

        RJPRINT("******************* %s光模块访问屏蔽测试 *******************" % type)
        RECODE = {"failed":[], "success":[]}
        RET1 = mask_i2c_set(mask_item, 1);      #关闭访问通道，无法访问光模块
        time.sleep(5)
        if RET1[RETURN_KEY1] == 0:
            for bus in range(startbus, endbus + 1):
                port_num = bus - startbus + startportnum
                ret, val = rji2cget(bus,addr,reg)
                if ret != False:
                    RET[RETURN_KEY1] = -1
                    RECODE["failed"].append(port_num)
                else:
                    RECODE["success"].append(port_num)
                time.sleep(0.1)
            port_totalprint(RECODE["success"], "成功端口：          ")
            port_totalprint(RECODE["failed"], "失败端口：          ")
            if len(RECODE["failed"]) > 0:
                errmes = print_port_sn(RECODE["failed"], "ErroMes")
                RJPRINT( "%s" % errmes)
        else:
            RJPRINT( "################################################ " )
            RJPRINT( " %s光模块访问屏蔽设置失败, log:\n%s " % (type, RET1[RETURN_KEY2]))
            RJPRINT( "################################################ ")
        RJPRINT("******************* %s光模块访问测试 *******************" % type)
        RECODE = {"failed":[], "success":[]}
        RET2 = mask_i2c_set(mask_item, 2);      #开启访问通道，正常访问
        time.sleep(5)
        if RET2[RETURN_KEY1] == 0:
            for bus in range(startbus, endbus + 1):
                port_num = bus - startbus + startportnum
                ret, val = rji2cget(bus, addr, reg)
                if ret == False:
                    RET[RETURN_KEY1] = -1
                    RECODE["failed"].append(port_num)
                else:
                    RECODE["success"].append(port_num)
                time.sleep(0.1)
            port_totalprint(RECODE["success"], "成功端口：          ")
            port_totalprint(RECODE["failed"], "失败端口：          ")
            if len(RECODE["failed"]) > 0:
                errmes = print_port_sn(RECODE["failed"], "ErroMes")
                RJPRINT( "%s" % errmes)
        else:
            RJPRINT( "################################################ " )
            RJPRINT( " %s光模块访问设置失败, log:\n%s " % (type, RET2[RETURN_KEY2]))
            RJPRINT( "################################################ ")

        if RET1[RETURN_KEY1] != 0 or RET2[RETURN_KEY1] != 0:
            RET[RETURN_KEY1] = -1
            log_debug("############ %s光模块测试Failed ############" % type)
    return RET

def test_lssignal_lpmode():
    RET = {RETURN_KEY1:0, RETURN_KEY2:""}
    RET = port_present_check();
    if RET[RETURN_KEY1] != 0:
        RJPRINT( "测试失败，请确保所有光模块在位后再重新测试")
        return RET
    LSSIGNAL_LPMODE = TESTCASE.get("LSSIGNAL_LPMODE", None)
    for item in LSSIGNAL_LPMODE:
        type = item.get("type", None)
        mask_item = item.get("mask_list", None)
        check_list = item.get("check_list", None)
        if type is None or  mask_item is None or  check_list is None:
            log_debug("type:%s, mask_item:%s, check_list:%s" % (type, mask_item, check_list))
            RJPRINT( "测试失败，相关配置文件缺失，请确认后再重新测试")
            RET[RETURN_KEY1] = -1
            return RET

        startbus = check_list.get("startbus", None)
        endbus = check_list.get("endbus", None)
        addr = check_list.get("addr", None)
        reg = check_list.get("reg", None)
        check_bit = check_list.get("check_bit", None)
        ok_val_1 = check_list.get("ok_val_1", None)
        ok_val_2 = check_list.get("ok_val_2", None)
        startportnum = check_list.get("startportnum", None)
        if startbus is None or endbus is None or addr is None or reg is None or check_bit is None or ok_val_1 is None or ok_val_2 is None or startportnum is None:
            RJPRINT( "测试失败，相关配置参数缺失，请确认后再重新测试")
            RET[RETURN_KEY1] = -1
            return RET
        log_debug("lssignal access get param. startbus:%d, endbus:%d addr:0x%x, reg:0x%x, check_bit:%d, ok_val_1:%d, ok_val_2:%d, startportnum:%d"
            % (startbus, endbus, addr, reg, check_bit, ok_val_1, ok_val_2, startportnum))

        RJPRINT("******************* %s光模块lpmode拉高测试 *******************" % type)
        RECODE = {"failed":[], "success":[]}
        RET1 = mask_i2c_set(mask_item, 1);
        time.sleep(5)
        if RET1[RETURN_KEY1] == 0:
            for bus in range(startbus, endbus + 1):
                port_num = bus - startbus + startportnum
                ret, val = rji2cget(bus, addr, reg)
                if ret == False:
                    RET[RETURN_KEY1] = -1
                    RECODE["failed"].append(port_num)
                    log_debug("i2cget failed. bus:%d, addr:0x%x, reg:0x%x" %(bus, addr, reg))
                else:
                    val_t = (int(val,16) & (1 << check_bit)) >> check_bit
                    if val_t != ok_val_1:
                        RET[RETURN_KEY1] = -1
                        RECODE["failed"].append(port_num)
                    else:
                        RECODE["success"].append(port_num)
                time.sleep(0.1)
            port_totalprint(RECODE["success"], "成功端口：          ")
            port_totalprint(RECODE["failed"], "失败端口：          ")
            if len(RECODE["failed"]) > 0:
                errmes = print_port_sn(RECODE["failed"], "ErroMes")
                RJPRINT( "%s" % errmes)
        else:
            RJPRINT( "################################################ " )
            RJPRINT( " %s光模块lpmode拉高设置失败, log:\n%s " % (type, RET1[RETURN_KEY2]))
            RJPRINT( "################################################ ")
        RJPRINT("******************* %s光模块lpmode拉低测试 *******************" % type)
        RECODE = {"failed":[], "success":[]}
        RET2 = mask_i2c_set(mask_item, 2);
        time.sleep(5)
        if RET2[RETURN_KEY1] == 0:
            for bus in range(startbus, endbus + 1):
                port_num = bus - startbus + startportnum
                ret, val = rji2cget(bus, addr, reg)
                if ret == False:
                    RET[RETURN_KEY1] = -1
                    RECODE["failed"].append(port_num)
                    log_debug("i2cget failed. bus:%d, addr:0x%x, reg:0x%x" %(bus, addr, reg))
                else:
                    val_t = (int(val,16) & (1 << check_bit)) >> check_bit
                    if val_t != ok_val_2:
                        RET[RETURN_KEY1] = -1
                        RECODE["failed"].append(port_num)
                    else:
                        RECODE["success"].append(port_num)
                time.sleep(0.1)
            port_totalprint(RECODE["success"], "成功端口：          ")
            port_totalprint(RECODE["failed"], "失败端口：          ")
            if len(RECODE["failed"]) > 0:
                errmes = print_port_sn(RECODE["failed"], "ErroMes")
                RJPRINT( "%s" % errmes)
        else:
            RJPRINT( "################################################ " )
            RJPRINT( " %s光模块lpmode拉低设置失败, log:\n%s " % (type, RET2[RETURN_KEY2]))
            RJPRINT( "################################################ ")

        if RET1[RETURN_KEY1] != 0 or RET2[RETURN_KEY1] != 0:
            RET[RETURN_KEY1] = -1
            log_debug("############ %s光模块测试Failed ############" % type)
    return RET

def test_lssignal_vcc(param):
    RET = {RETURN_KEY1:0, RETURN_KEY2:""}
    failed_list = []
    RET = port_present_check();
    if RET[RETURN_KEY1] != 0:
        RJPRINT( "测试失败，请确保所有光模块在位后再重新测试")
        return RET
    LSSIGNAL_VCC = TESTCASE.get(param, None)
    for vcc_item in LSSIGNAL_VCC:
        type = vcc_item.get("type", None)
        threshold_item = vcc_item.get("threshold_list", None)
        if type is None or  threshold_item is None:
            log_debug("type:%s, loopback_item:%s" % (type, threshold_item))
            RJPRINT( "测试失败，相关配置文件缺失，请确认后再重新测试")
            RET[RETURN_KEY1] = -1
            return RET

        startbus = threshold_item.get("startbus", None)
        endbus = threshold_item.get("endbus", None)
        addr = threshold_item.get("addr", None)
        reg1 = threshold_item.get("reg1", None)
        reg2 = threshold_item.get("reg2", None)
        min = threshold_item.get("min", None)
        max = threshold_item.get("max", None)
        startportnum = threshold_item.get("startportnum", None)
        if startbus is None or endbus is None or addr is None or reg1 is None or reg2 is None or min is None or max is None or startportnum is None:
            RJPRINT( "测试失败，相关配置参数缺失，请确认后再重新测试")
            RET[RETURN_KEY1] = -1
            return RET
        log_debug("lssignal vcc get param. startbus:%d, endbus:%d addr:0x%x, reg1:0x%x, reg2:0x%x"
            % (startbus, endbus, addr, reg1, reg2))
        log_debug("lssignal vcc get param. min:%d, endbus:%d, startportnum:%d"
            % (min, max, startportnum))

        RJPRINT( "******************* %s光模块 *******************" % type)
        for bus in range(startbus, endbus + 1):
            time.sleep(0.1)
            port_num = bus - startbus + startportnum
            ret1, val1 = rji2cget(bus, addr, reg1)
            if ret1 == False:
                RET[RETURN_KEY1] = -1
                failed_list.append(port_num)
                RJPRINT( "\n############# error: port %d: i2cget failed.bus:%d, addr:0x%x, reg:0x%x#############\n" % (port_num, bus, addr, reg1))
                continue
            time.sleep(0.1)
            ret2, val2 = rji2cget(bus, addr, reg2)
            if ret2 == False:
                RET[RETURN_KEY1] = -1
                failed_list.append(port_num)
                RJPRINT( "\n############# error: port %d: i2cget failed.bus:%d, addr:0x%x, reg:0x%x#############\n" % (port_num, bus, addr, reg2))
                continue

            val = int(val1, 16) * 0x0100 + int(val2, 16)
            val = val / 10    #光模块寄存器单位0.1mV, 除10转换为mV便于显示
            if val < min or val > max:
                RET[RETURN_KEY1] = -1
                failed_list.append(port_num)
                RJPRINT( "\n############# error: port %d: %dmV(min:%dmV, max:%dmV)   FAILED#############\n" % (port_num, val, min, max))
            else:
                RJPRINT( "port %d : %dmV (min:%dmV, max:%dmV)     PASS" % (port_num, val, min, max))
    if len(failed_list) > 0:
        errmes = print_port_sn(failed_list, "ErroMes")
        RJPRINT( "%s" % errmes)
    return RET

def upper_input(tips):
    sys.stdout.write(tips)
    sys.stdout.flush()
    passwd = []
    while True:
        ch = getrawch().upper()
        if ch == "\r" or ch == "\n":
          print()
          tmp =  "".join(passwd)
          ret_t = tmp.strip().strip(b'\x00'.decode())
          return str(ret_t)
        elif ch == '\b' or ord(ch) == 127:
            if passwd:
                del passwd[-1]
                sys.stdout.write('\b \b')
        else:
          sys.stdout.write(ch)
          passwd.append(ch)

def getrawch():
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ch

TLV_INFO_ID_STRING = "TlvInfo\x00"
TLV_INFO_VERSION = 0x01
TLV_INFO_LENGTH = 0x00
TLV_INFO_LENGTH_VALUE = 0xba


def getTLV_BODY(type, productname):
    x = []
    temp_t = ""
    if type == TLV_CODE_MAC_BASE:
        arr = productname.split(':')
        for tt in arr:
            temp_t += chr(int(tt, 16))
    elif type == TLV_CODE_DEVICE_VERSION:
        temp_t = chr(productname)
    elif type == TLV_CODE_MAC_SIZE:
        temp_t = chr(productname >> 8) + chr(productname & 0x00ff)
    else:
        temp_t = productname
    x.append(chr(type))
    x.append(chr(len(temp_t)))
    for i in temp_t:
        x.append(i)
    return x

def _crc32(v):
    return '0x%08x' % (binascii.crc32(v) & 0xffffffff)  # 取crc32的八位数据 %x返回16进制


def util_setmac(eth, mac):
    rulefile = "/etc/udev/rules.d/70-persistent-net.rules"
    if isValidMac(mac) == False:
        return False, "MAC非法"
    cmd = "ethtool -e %s | grep 0x0010 | awk '{print \"0x\"$13$12$15$14}'" % eth
    ret, log = rj_os_system(cmd)
    log_debug(log)
    magic = ""
    if ret == 0 and len(log):
        magic = log
    macs = mac.upper().split(":")

    # 暂时把本地的ETH0改为setmac后的值
    ifconfigcmd = "ifconfig %s hw ether %s" % (eth,mac)
    log_debug(ifconfigcmd)
    ret, status = rj_os_system(ifconfigcmd)
    if ret:
        raise SETMACException("软件设置网卡MAC出错")
    if ret:
        return False
    index = 0
    for item in macs:
        cmd = "ethtool -E %s magic %s offset %d value 0x%s" % (
            eth, magic, index, item)
        log_debug(cmd)
        index += 1
        ret, log = rj_os_system(cmd)
        if ret != 0:
            raise SETMACException("设置硬件网卡MAC出错")
            return False
    # 取设置后的返回值
    cmd_t = "ethtool -e %s offset 0 length 6" % eth
    ret, log = rj_os_system(cmd_t)
    m = re.split(':', log)[-1].strip().upper()
    mac_result = m.upper().split(" ")

    for ind, s in enumerate(macs):
        if s != mac_result[ind]:
            RJPRINTERR("MAC比较出错")
    if os.path.exists(rulefile):
        os.remove(rulefile)  # 删除文件
    print("MGMT MAC【%s】" % mac)
    return True

def test_bmc_i2c_open():
    switch_ctrol = TESTCASE.get("switchcontrol",None)
    if switch_ctrol is None:
        return True, ""
    if switch_ctrol.get('needopen') != 0:
        test_stop_fanctrol()
        time.sleep(1)
        for item in switch_ctrol.get('switchctrl',[]):
            if item.get('gettype') == 'io':
                addr = item.get('io_addr')
                val = item.get('switchbmc')
                io_wr(addr, val)
            else:
            # maybe i2c
                pass
    return True,""

def test_bmc_i2c_close():
    switch_ctrol = TESTCASE.get("switchcontrol",None)
    if switch_ctrol is None:
        return True, ""
    if switch_ctrol.get('needopen') != 0:
        for item in switch_ctrol.get('switchctrl',[]):
            if item.get('gettype') == 'io':
                addr = item.get('io_addr')
                val = item.get('switchcpu')
                io_wr(addr, val)
            else:
                # maybe i2c
                pass
    test_start_fanctrol()
    return True,""

def writeToBMCEEprom(rst_arr, loc, ep_param):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    params = {}
    try:
        params["value"] = []
        params["loc"] = loc
        params.update(ep_param)
        for item in rst_arr: # item是字符，转换为ASCII
            params["value"].append(ord(item))
        func = "test_bmc_write_eeprom"
        RET = test_bmc_func(func,params)
        if RET[RETURN_KEY1] < 0:
            return RET
    except Exception as e:
        RET[RETURN_KEY2] = str(e)
        RET[RETURN_KEY1] = -1
    return RET

def sync_bmc_tlv_e2(rst_arr):
    tmp = TESTCASE.get('bmctlve2sync')
    if "BMC_access" in tmp and tmp.get("BMC_access") == 1: #BMC_access为1时，在BMC端同步做E2同步
        loc = tmp.get('BMC_E2_LOC')
        ep_param = tmp.get('BMC_E2_PROTECT')
        writeToBMCEEprom(rst_arr, loc, ep_param)
        return
    e2_protect = tmp.get('BMC_E2_PROTECT',None)
    if e2_protect is not None:
        dealtype = e2_protect.get('gettype', None)
        if dealtype is None:
            rji2cset(e2_protect["bus"], e2_protect["devno"],
                     e2_protect["addr"], e2_protect["open"])
        elif dealtype == "io":
            io_wr(e2_protect["io_addr"], e2_protect["open"])
    index = 0
    e2_loc = tmp.get('BMC_E2_LOC',None)
    if e2_loc is not None:
        for item in rst_arr:
            rji2cset(e2_loc["bus"], e2_loc["devno"], index, ord(item))
            index += 1

    if e2_protect is not None:
        if dealtype is None:
            rji2cset(e2_protect["bus"], e2_protect["devno"],
                     e2_protect["addr"], e2_protect["close"])
        elif dealtype == "io":
            io_wr(e2_protect["io_addr"], e2_protect["close"])

def writeToEEprom(rst_arr):
    dealtype = E2_PROTECT.get('gettype',None)
    if dealtype is None:
        rji2cset(E2_PROTECT["bus"], E2_PROTECT["devno"],
                 E2_PROTECT["addr"], E2_PROTECT["open"])
    elif dealtype == "io":
        io_wr(E2_PROTECT["io_addr"], E2_PROTECT["open"])
    index = 0
    for item in rst_arr:
        rji2cset(E2_LOC["bus"], E2_LOC["devno"], index, ord(item))
        index += 1
    if 'bmctlve2sync' in TESTCASE:
        sync_bmc_tlv_e2(rst_arr)
        func = 'bmc_log_os_system'
        cmd = "systemctl restart read-uboot-mac.service"  # 修改BMC eth0 MAC
        ret = test_bmc_func(func, cmd)
        if ret[RETURN_KEY1] != 0:
            RJPRINT("set BMC eth0 fail")
    if dealtype is None:
        rji2cset(E2_PROTECT["bus"], E2_PROTECT["devno"],
                 E2_PROTECT["addr"], E2_PROTECT["close"])
    elif dealtype == "io":
        io_wr(E2_PROTECT["io_addr"], E2_PROTECT["close"])
    # 最后处理系统驱动
    #os.system("rmmod at24 ")
    #os.system("modprobe at24 ")
    os.system("rm -f /var/cache/sonic/decode-syseeprom/syseeprom_cache")


def changeTypeValue(_value, type1, tips, example):
    if type1 == TLV_CODE_PRODUCT_NAME:
        while True:
            print("请确认 (1)前后进风/(2)后前进风:", end=' ')
            option = input()
            if option == "1":
                _value[type1] = example + "-F-RJ"
                print("确认该产品为前后进风设备,产品名称:%s"%_value[type1])
                break
            elif option == "2":
                _value[type1] = example + "-R-RJ"
                print("确认该产品为后前进风设备,产品名称:%s"%_value[type1])
                break
            else:
                print("输入错误,请认真核对")
        return True
    print("请输入【%s】如(%s):" % (tips, example), end=' ')
    if type1 == TLV_CODE_MAC_BASE:
        name = upper_input("")
        if len(name) != 12:
            raise SETMACException("MAC地址长度不对(12位),请认真核对")
            return False
        release_mac = ""
        for i in range(len(name) / 2):
            if i == 0:
                release_mac += name[i * 2:i * 2 + 2]
            else:
                release_mac += ":" + name[i * 2:i * 2 + 2]
        if isValidMac(release_mac) == True:
            _value[type1] = release_mac
        else:
            raise SETMACException("MAC地址非法,请认真核对")
            return False
    elif type1 == TLV_CODE_DEVICE_VERSION:
        name = upper_input("")
        if not name.isdigit():
            raise SETMACException("版本号非数字,请认真核对")
        elif int(name) > 255:
            raise SETMACException("版本号超出范围(0-255),请认真核对")
        else:
            _value[type1] = int(name)
    elif type1 == TLV_CODE_MAC_SIZE:
        name = upper_input("")
        if name.isdigit():
            _value[type1] = int(name, 16)
        else:
            raise SETMACException("版本号非数字,请认真核对")
    elif type1 == TLV_CODE_SERIAL_NUMBER:
        name = upper_input("")
        board_sn_len = TESTCASE.get('setmacsnlen', {}).get("board", BOARD_SN_LEN_DEF)
        if name.isalnum() == False:
            raise SETMACException("序列号非法字符串,请认真核对")
        elif len(name) != board_sn_len:
            raise SETMACException("序列号长度不对(" + str(board_sn_len) + "位),请认真核对")
        else:
            _value[type1] = name
    elif type1 == TLV_CODE_PART_NUMBER:
        name = upper_input("")
        if name.isalnum() == False:
            raise SETMACException("Part Number为非法字符串,请认真核对")
        elif len(name) > 16:
            raise SETMACException("Part Number长度不对(不允许超过16位),请认真核对")
        else:
            _value[type1] = name
    elif type1 == TLV_CODE_LABEL_REVISION:
        name = upper_input("")
        if name.isalnum() == False:
            raise SETMACException("Label Revision为非法字符串,请认真核对")
        elif name != "BN" and name != "RMA":
            raise SETMACException("Label Revision输入错误,请输入BN或RMA")
        else:
            _value[type1] = name
    elif type1 == TLV_CODE_ONIE_VERSION:
        name = upper_input("")
        if len(name) > 16:
            raise SETMACException("ONIE版本号长度不允许超过16位,请认真核对")
        else:
            _value[type1] = name
    elif type1 == TLV_CODE_MANUF_NAME:
        name = input("")
        if name.isalnum() == False:
            raise SETMACException("生产商名称为非法字符串,请认真核对")
        elif len(name) > 16:
            raise SETMACException("生产商名称长度不对,超过(16个字符),请认真核对")
        else:
            _value[type1] = name
    elif type1 == TLV_CODE_SERVICE_TAG:
        name = input("")
        if name.isalnum() == False:
            raise SETMACException("服务标签为非法字符串,请认真核对")
        elif len(name) > 16:
            raise SETMACException("服务标签长度不允许超过16位,请认真核对")
        else:
            _value[type1] = name
    elif type1 == TLV_CODE_VENDOR_EXT:
        name = upper_input("")
        _value[type1] = name
    else:
        name = upper_input("")
        _value[type1] = name
    return True



class SETMACException(Exception):
    def __init__(self, param='错误', errno="-1"):
        err = "setmac出错[%s]: %s" % (errno, param)
        Exception.__init__(self, err)
        self.param = param
        self.errno = errno
def getPid(name):
    ret = []
    for dirname in os.listdir('/proc'):
        if dirname == 'curproc':
            continue
        try:
            with open('/proc/{}/cmdline'.format(dirname), mode='rb') as fd:
                content = fd.read()
        except Exception:
            continue
        if name in content:
            ret.append(dirname)
    return ret

def getsysmeminfo_detail():
    ret, log = rj_os_system("which dmidecode ")
    if ret != 0 or len(log) <= 0:
        error = "cmd find dmidecode"
        return False, error
    cmd = log + " -t 17 | grep  -A21 \"Memory Device\""  # 17
    # 先获取总数
    ret1, log1 = rj_os_system(cmd)
    if ret != 0 or len(log1) <= 0:
        return False, "command[%s] execution error" % cmd
    result_t = log1.split("--")
    mem_rets = []
    for item in result_t:
        its = item.replace("\t", "").strip().split("\n")
        ret = {}
        for it in its:
            if ":" in it:
                key = it.split(":")[0].lstrip()
                value = it.split(":")[1].lstrip()
                ret[key] = value
        mem_rets.append(ret)
    return True, mem_rets





def getsysbios():
    return getDmiSysByType(0)

def getDmiSysByType(type_t):
    ret, log = rj_os_system("which dmidecode ")
    if ret != 0 or len(log) <= 0:
        error = "cmd find dmidecode"
        return False, error
    cmd = log + " -t %s" % type_t
    # 先获取总数
    ret1, log1 = rj_os_system(cmd)
    if ret != 0 or len(log1) <= 0:
        return False, "command[%s] execution error" % cmd
    its = log1.replace("\t", "").strip().split("\n")
    ret = {}
    for it in its:
        if ":" in it:
            key = it.split(":")[0].strip()
            value = it.split(":")[1].strip()
            ret[key] = value
    return True, ret



def gethwsys():
    return getDmiSysByType(1)

TLV_CODE_PRODUCT_NAME = 0x21
TLV_CODE_PART_NUMBER = 0x22
TLV_CODE_SERIAL_NUMBER = 0x23
TLV_CODE_MAC_BASE = 0x24
TLV_CODE_MANUF_DATE = 0x25
TLV_CODE_DEVICE_VERSION = 0x26
TLV_CODE_LABEL_REVISION = 0x27
TLV_CODE_PLATFORM_NAME = 0x28
TLV_CODE_ONIE_VERSION = 0x29
TLV_CODE_MAC_SIZE = 0x2A
TLV_CODE_MANUF_NAME = 0x2B
TLV_CODE_MANUF_COUNTRY = 0x2C
TLV_CODE_VENDOR_NAME = 0x2D
TLV_CODE_DIAG_VERSION = 0x2E
TLV_CODE_SERVICE_TAG = 0x2F
TLV_CODE_VENDOR_EXT = 0xFD
TLV_CODE_CRC_32 = 0xFE
_TLV_DISPLAY_VENDOR_EXT = 1
TLV_CODE_RJ_CARID = 0x01
_TLV_INFO_HDR_LEN = 11



def decoder(s, t):
    if ord(t[0]) == TLV_CODE_PRODUCT_NAME:
        name = "Product Name"
        value = str(t[2:2 + ord(t[1])])
    elif ord(t[0]) == TLV_CODE_PART_NUMBER:
        name = "Part Number"
        value = t[2:2 + ord(t[1])]
    elif ord(t[0]) == TLV_CODE_SERIAL_NUMBER:
        name = "Serial Number"
        value = t[2:2 + ord(t[1])]
    elif ord(t[0]) == TLV_CODE_MAC_BASE:
        name = "Base MAC Address"
        value = ":".join([binascii.b2a_hex(T) for T in t[2:8]]).upper()
    elif ord(t[0]) == TLV_CODE_MANUF_DATE:
        name = "Manufacture Date"
        value = t[2:2 + ord(t[1])]
    elif ord(t[0]) == TLV_CODE_DEVICE_VERSION:
        name = "Device Version"
        value = str(ord(t[2]))
    elif ord(t[0]) == TLV_CODE_LABEL_REVISION:
        name = "Label Revision"
        value = t[2:2 + ord(t[1])]
    elif ord(t[0]) == TLV_CODE_PLATFORM_NAME:
        name = "Platform Name"
        value = t[2:2 + ord(t[1])]
    elif ord(t[0]) == TLV_CODE_ONIE_VERSION:
        name = "ONIE Version"
        value = t[2:2 + ord(t[1])]
    elif ord(t[0]) == TLV_CODE_MAC_SIZE:
        name = "MAC Addresses"
        value = str((ord(t[2]) << 8) | ord(t[3]))
    elif ord(t[0]) == TLV_CODE_MANUF_NAME:
        name = "Manufacturer"
        value = t[2:2 + ord(t[1])]
    elif ord(t[0]) == TLV_CODE_MANUF_COUNTRY:
        name = "Manufacture Country"
        value = t[2:2 + ord(t[1])]
    elif ord(t[0]) == TLV_CODE_VENDOR_NAME:
        name = "Vendor Name"
        value = t[2:2 + ord(t[1])]
    elif ord(t[0]) == TLV_CODE_DIAG_VERSION:
        name = "Diag Version"
        value = t[2:2 + ord(t[1])]
    elif ord(t[0]) == TLV_CODE_SERVICE_TAG:
        name = "Service Tag"
        value = t[2:2 + ord(t[1])]
    elif ord(t[0]) == TLV_CODE_VENDOR_EXT:
        name = "Vendor Extension"
        value = ""
        if _TLV_DISPLAY_VENDOR_EXT:
            value = t[2:2 + ord(t[1])]
    elif ord(t[0]) == TLV_CODE_CRC_32 and len(t) == 6:
        name = "CRC-32"
        value = "0x%08X" % (((ord(t[2]) << 24) | (
            ord(t[3]) << 16) | (ord(t[4]) << 8) | ord(t[5])),)
    elif ord(t[0]) == TLV_CODE_RJ_CARID:
        name = "rj_cardid"
        value = ""
        for c in t[2:2 + ord(t[1])]:
            value += "%02X" % (ord(c),)
    else:
        name = "Unknown"
        value = ""
        for c in t[2:2 + ord(t[1])]:
            value += "0x%02X " % (ord(c),)
    return {"name": name, "code": ord(t[0]), "value": value}


def wide_chars(s):
    if isinstance(s, str):
        s = s.encode().decode('utf-8')
    return sum(unicodedata.east_asian_width(x) in ('F', 'W') for x in s)


grtdlog_dir= "/var/grtd"
grtdlog_name = grtdlog_dir +"/grtdtest.log"
kjlogmaxshow = 10


def get_pmc_register(reg_name):
    retval = 'ERR'
    if reg_name[0:4] == "/rif" or reg_name[0:4] == "/ma1" or reg_name[0:4] == "/eth":
        mb_reg_file = PORTS_DIR + reg_name
    else:
        mb_reg_file = MAILBOX_DIR + reg_name
    if (not os.path.isfile(mb_reg_file)):
        print(mb_reg_file,  'not found !')
        return retval
    try:
        if (not os.path.isfile(mb_reg_file)):
            print(mb_reg_file,  'not found !')
            return retval
        with open(mb_reg_file, 'r') as fd:
            retval = fd.read()
    except Exception as error:
        log_error("Unable to open " + mb_reg_file + "file !")
    retval = retval.rstrip('\r\n')
    retval = retval.lstrip(" ")
    #log_debug(retval)
    return retval


def get_sysfs_value(location):
    pos_t = str(location)
    name = get_pmc_register(pos_t)
    return name

def rj_os_system(cmd):
    status, output = subprocess.getstatusoutput(cmd)
    return status, output


def get_cpu_info():
    cmd = "cat /proc/cpuinfo |grep processor -A18"  # 17

    ret, log1 = rj_os_system(cmd)
    if ret != 0 or len(log1) <= 0:
        return False, "命令执行出错[%s]" % cmd
    result_t = log1.split("--")
    mem_rets = []
    for item in result_t:
        its = item.replace("\t", "").strip().split("\n")
        ret = {}
        for it in its:
            if ":" in it:
                key = it.split(":")[0].lstrip()
                value = it.split(":")[1].lstrip()
                ret[key] = value
        mem_rets.append(ret)
    return True, mem_rets


def getch(msg):
    ret = ""
    fd = sys.stdin.fileno()
    old_ttyinfo = termios.tcgetattr(fd)
    new_ttyinfo = old_ttyinfo[:]
    new_ttyinfo[3] &= ~termios.ICANON
    new_ttyinfo[3] &= ~termios.ECHO
    sys.stdout.write(msg)
    sys.stdout.flush()
    try:
        termios.tcsetattr(fd, termios.TCSANOW, new_ttyinfo)
        ret = os.read(fd, 1)
    finally:
        # print "try to setting"
        termios.tcsetattr(fd, termios.TCSANOW, old_ttyinfo)
    return ret

def root_check():
    if os.geteuid() != 0:
        click.echo("请在Root权限下执行！")
        sys.exit(1)

SYSLOG_IDENTIFIER = "FACTEST"

g_info_tmp = ""
def print_temp(str,cache = True):
    if cache:
        global g_info_tmp
        g_info_tmp += str+"\n"
    else:
        print(str)

def print_temp_flush():
    global g_info_tmp
    if g_info_tmp != "":
       print(g_info_tmp)
    g_info_tmp = ""

def print_clean():
    global g_info_tmp
    g_info_tmp = ""

syslog_debug = 0
def log_info(msg, also_print_to_console=False):
    if syslog_debug == 1:
        syslog.openlog(SYSLOG_IDENTIFIER)
        syslog.syslog(syslog.LOG_INFO, msg)
        syslog.closelog()
    if also_print_to_console:
        click.echo(msg)


def log_debug(msg, also_print_to_console=False):
    try:
        if syslog_debug == 1:
            syslog.openlog(SYSLOG_IDENTIFIER)
            syslog.syslog(syslog.LOG_DEBUG, msg)
            syslog.closelog()

        if also_print_to_console:
            click.echo(msg)
    except Exception as e:
        pass


def log_warning(msg, also_print_to_console=False):
    if syslog_debug == 1:
        syslog.openlog(SYSLOG_IDENTIFIER)
        syslog.syslog(syslog.LOG_DEBUG, msg)
        syslog.closelog()

    if also_print_to_console:
        click.echo(msg)


def log_error(msg, also_print_to_console=False):
    if syslog_debug == 1:
        syslog.openlog(SYSLOG_IDENTIFIER)
        syslog.syslog(syslog.LOG_DEBUG, msg)
        syslog.closelog()

    if also_print_to_console:
        click.echo(msg)

LOGERROR = False
DEBUG = False
KAOJILOGPATH = "/var/grtd/"
KAOJILOGFILE = KAOJILOGPATH + "kjlog.log"
KAOJISTATUS = 1
ISKAOJI = 0
# CONFIG_NAME = "apptest.xml"
RTC_WAIT_TIME                   = 3
RTC_THRESHOLD_LOWER             = 3
RTC_THRESHOLD_UPPER             = 5


kj_result =[]

nosetrtc = 1

DIAGTEST = False
SAVE_STDOUT = None
INSP_RESULT = ""

def keep_message(RET, x, newline = True):
    if newline == True:
        RET[RETURN_KEY2] += (str)(x) + "\n"
    else:
        RET[RETURN_KEY2] += (str)(x)

def RJPRINTLINE(x):
    '''保留函数,后续适配3.x'''
    print(x, end=' ')

def RJPRINT(x,newline = True):
    '''保留函数,后续适配3.x'''
    if newline == True:
        print(x)
    else:
        print(x, end=' ')

def force_abort_cpu_stress():
    log_os_system("ps -ef | grep \"%s\" | grep -v grep | awk '{print $2}' | xargs kill -9 " % CpuStressCmd, 0)

def quit():
    force_abort_cpu_stress()
    force_abort_ddr_stress()
    sys.exit(0)

def test_sys_halt():
    log_os_system("sync", 0)
    log_os_system("halt -f", 0)

def test_sys_reload():
    log_os_system("sync", 0)
    log_os_system("reboot -f", 0)

def powercycle_conf_check(conf):
    if (
        conf.get("addr") is None
        or conf.get("gettype") is None
        or conf.get("value") is None
    ):
        return False
    return True

def powercycle_process(addr, val):
    # poweroff
    return io_wr(addr, val)

def check_yes_no(msg):
    ret = input("{}[Yes/no]：".format(msg))
    if astrcmp(ret, "y") or astrcmp(ret, "ye") or astrcmp(ret, "yes") or astrcmp(ret, ""):
        return True
    else:
        return False

def test_powercycle():
    """
    整机 powercycle
    """
    RET = {RETURN_KEY1: -1,  RETURN_KEY2: ""}
    conf = TESTCASE.get("POWERCYCLE")
    if conf is None:
        RET[RETURN_KEY1] = -2
        RET[RETURN_KEY2] = "没有配置文件"
        return RET
    if not powercycle_conf_check(conf):
        RET[RETURN_KEY1] = -3
        RET[RETURN_KEY2] = "配置文件校验失败"
        return RET

    if not check_yes_no("确认是否执行整机 powercycle"):
        RET[RETURN_KEY1] = -4
        RET[RETURN_KEY2] = "取消操作"
        return RET

    ret = powercycle_process(conf.get("addr"), conf.get("value"))
    if ret:
        RET[RETURN_KEY1] = 0
        RET[RETURN_KEY2] = "执行成功"
    else:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "执行失败"

    return RET

def getInputValue(title, tips):
    print("请输入【%s】如(%s):" % (title, tips), end=' ')
    name = input()
    return name

# Backport Python 3.4's regular expression "fullmatch()" to Python 2
def fullmatch(regex, string, flags=0):
    """Emulate python-3.4 re.fullmatch()."""
    return re.match("(?:" + regex + r")\Z", string, flags=flags)

def test_set_rtc():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    time = getInputValue("RTC时间","20180816 11:43:22")
    ret = fullmatch("[0-9]{8} [0-9]{2}:[0-9]{2}:[0-9]{2}", time)
    if ret:
        cmd = "date -s '%s' &&hwclock --systohc" % time
        ret, log = rj_os_system(cmd)
    else:
        RET[RETURN_KEY1] = -1
        RJPRINT("输入错误")
        return RET
    if ret != 0:
        RJPRINTERR("\n\n!!!.设置RTC时间失败\n\n")
        return {RETURN_KEY1 : -1, RETURN_KEY2 : []}
    systimecmd = "date -R"
    ret , log = rj_os_system(systimecmd)
    RJPRINT("当前时间: %s" % log)
    return RET

#菜单打印 菜单项带前面数字提示符
def printList(_list, id):
    try:
        RJPRINT("****************************************")
        for index in range(len(_list)):
            RJPRINT(formatStringLevel1 %( listindex[index] , _list[index]["name"]))
        if id != STARTMENUID:
            RJPRINT("q.返回上一层")
        else:
            RJPRINT("q.退出")
        RJPRINT("****************************************")
    except Exception as e:
        log_error(str(e))
        sys.exit(-1)

def analy_port_result(val_dit):
    tmp = ""
    for key, val in list(val_dit.items()):
        if len(val) != 0:
            if key == "prbs_info":
                tmp += "%s\n%s"%(key, val)
            elif key == "other_info":
                tmp += "port %s\n%s"%(key, val)
            elif key == "port_info_dict":
                tmp += "port %s:\n%s" % (key, val)
            else:
                tmp += print_to_str(val, key)
    return tmp

def test_kr_new():
    RET = {RETURN_KEY1 : -1,  RETURN_KEY2 : ""}
    packetcount = 10000
    subprocess_case.print_result("packets %d\n" % packetcount)
    obj = PortTestCall(port_list_val=[], redirect = True)
    ret, val_dit = obj.port_kr_test()
    if ret:
        RET[RETURN_KEY1] = 0
    for key, val in list(val_dit.items()):
        if len(val) != 0:
            if key == "other_info":
                subprocess_case.print_result("port %s\n%s"%(key, val))
            elif key == "port_info_dict":
                subprocess_case.print_result("port %s:\n%s" % (key, val))
            else:
                subprocess_case.print_result("%-20s%s\n"%(key, " ".join("%-3s"%str(x) for x in val)))
    return RET

def test_kr():
    RET = {RETURN_KEY1 : -1,  RETURN_KEY2 : ""}
    packetcount = 10000
    RJPRINT("packets %d" % packetcount)

    returnstr = ''
    ind = False

    for i in range(0 , 3):
        returnstr = ''
        try:
            pk = PortKrTest()
            error = 0
            errmsg = ""
            for i in [1,2]:
                eth = "eth%d"%i
                xe_port = pk.get_mgmt_bcmport(eth)
                cmd = "bcmcmd \"port %s en=1\"" % xe_port
                ret, output = rj_os_system(cmd)
                if(ret != 0):
                    log_debug("cmd %s fail, output %s" % (cmd, output))
                pk.clear_port_packets()
                time.sleep(1)
                ret, result = pk.start_send_port_packets(eth, count=packetcount, vlan = 2000)
                time.sleep(4)
                ret, log = pk.check_port_packets(eth, count=packetcount)
                if ret:
                    returnstr += "%s : PASS \n" % eth
                else:
                    error -= 1
                    returnstr += "%s : FAILED  reason[%s] \n" % (eth, str(log))
            for i in [1,2]:
                eth = "eth%d"%i
                xe_port = pk.get_mgmt_bcmport(eth)
                cmd = "bcmcmd \"port %s en=0\"" % xe_port
                ret, output = rj_os_system(cmd)
                if(ret != 0):
                    log_debug("cmd %s fail, output %s" % (cmd, output))
            if error < 0:
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] = returnstr
                continue
            else:
                RET[RETURN_KEY1] = 0
                RET[RETURN_KEY2] = returnstr
                break
        except Exception as e:
            RET[RETURN_KEY1] = -999
            RET[RETURN_KEY2] = returnstr
    RJPRINT(RET[RETURN_KEY2])
    return  RET


def getBMCIP():
    global G_BMCIP
    if G_BMCIP is not None:
        return True, G_BMCIP
    bmc_usb_ip = TESTCASE.get("bmc_usb_ip", None)
    if bmc_usb_ip is not None:
        return True, bmc_usb_ip    #x86与BMC端的usb0 ip需要外部脚本配置
    cmd = "ipmitool lan print |grep 'IP Address'|awk 'NR==2'"
    ret, log = rj_os_system(cmd)
    if ret != 0 or len(log) == 0:
        msg = "cmd: %s exec error, log: %s" % (cmd, log)
        log_debug(msg)
        return False, msg
    split_list = (log).strip().split(":")
    if len(split_list) != 2:
        msg = "cmd: %s split error, log: %s" % (cmd, log)
        log_debug(msg)
        return False, msg
    G_BMCIP = split_list[1].strip()
    return True, G_BMCIP


def password_command_tmp(cmd, password, exec_timeout=30):

    newkey = 'continue connecting'
    log_os_system("rm -rf ~/.ssh", 0)
    msg = ""
    try_times = 3
    try_times_conter = try_times
    while try_times_conter:
        child = pexpect.spawn(cmd)
        if try_times != try_times_conter:
            time.sleep(5)
        try_times_conter -= 1
        try:
            i = child.expect([pexpect.TIMEOUT, newkey, 'password: ',"refused",pexpect.EOF],timeout=30)
            # 如果登录超时，打印出错信息，并退出.
            if i == 0: # Timeout
                msg = 'Connection to BMC timed out'
                continue
            # 没有 public key
            if i == 1:
                child.sendline ('yes')
                i = child.expect([pexpect.TIMEOUT, 'password: '],timeout=30)
                if i == 0: # Timeout
                    msg = 'Connection to BMC timed out'
                    continue
                if i == 1:#走到下面输入密码的逻辑
                    i = 2
            if i == 2: #输入密码
                child.sendline (password)
                i = child.expect([pexpect.EOF, pexpect.TIMEOUT], exec_timeout)
                if i == 0:
                    return True,child.before
                if i == 1:
                    msg = str(typeTostr(child.before))+"\nBMC execution command timed out"
                    return False,msg
            if i == 3: #BMC 拒绝连接
                msg =  'Failed to connect to BMC'
                continue
            if i == 4:
                msg = child.before
        except Exception as e:
            msg = str(typeTostr(child.before))+"\nFailed to connect to BMC"

    return False,msg


def password_command(cmd, password, exec_timeout=30):
    ret, log = password_command_tmp(cmd, password, exec_timeout)
    log = typeTostr(log)
    return ret, log


def scpFileToBMC(src, dst):
    ret, bmcip = getBMCIP()
    if ret is False:
        msg = "get bmcip faled, log:%s" % bmcip
        return ret, msg
    cmd = 'scp -r %s root@%s:%s' % (src, bmcip, dst)
    log_debug('scp file to bmc, cmd: %s' % cmd)
    ret, log = password_command(cmd,OPENBMC_PASSWORD)
    if ret and "100%" in log:
        log_debug("scp file to bmc success, src: %s, dts:%s" % (src, dst))
        return True, ""
    log_debug("scp file to bmc failed, src: %s, dts:%s, log: %s" % (src, dst, log))
    return False, log


def sshExecBMCCmd(cmd):
    ret, bmcip = getBMCIP()
    if ret is False:
        msg = "get bmcip faled, log:%s" % bmcip
        return ret, msg
    cmd = "ssh root@%s \"%s\"" % (bmcip, cmd)
    log_debug('ssh exec bmc command, cmd: %s' % cmd)
    status, log = password_command(cmd, OPENBMC_PASSWORD)
    if not status :
        log_debug("cmd: %s exec error, log: %s" % (cmd, log))
        return False, log
    log_debug("cmd: %s exec success, log: %s" % (cmd, log))
    return True, log


def test_all_check(path, test_items):
    # 执行diagtestall中的巡检项
    # 将结果汇总，统一存入一个自定义命名格式的文件中
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : "", "log":"", RETURN_KEY3: 0}
    sum_fail_cont = 0
    sum_pass_info_tmp = ""
    sum_fail_info_tmp = ""

    if path is None or len(test_items) == 0:
        RET[RETURN_KEY1] = -1
        RJPRINT("file path or inspection parameter is NULL")
        return RET
    # 执行diagtestall中的巡检项，并将测试结果汇总
    for item in test_items:
        try:
            RJPRINT("")
            RJPRINT("=" * 12 + item[MENUITEMNAME] + "=" *12)
            ret = dealchoosefunc(item)
            formatstr = "======%%-%ds ======:%%-10s\n"%((40+wide_chars(item[MENUITEMNAME])))
            if ret[RETURN_KEY1] == 0 or ret[RETURN_KEY1] == 1:
                sum_pass_info_tmp += formatstr%(item[MENUITEMNAME], "PASS")
                RJPRINT("[%s]Test result: " % item[MENUITEMNAME] + 'PASS')
                log_debug("[%s]Test result: " % item[MENUITEMNAME] + SUCCESS_TIPS)
            else:
                sum_fail_cont =  sum_fail_cont + 1
                sum_fail_info_tmp += formatstr%(item[MENUITEMNAME], "FAIL")
                RJPRINT("[%s]Test result: " % item[MENUITEMNAME] + 'FAIL')
                log_debug("[%s]Test result: " % item[MENUITEMNAME] + 'error')
        except Exception as e:
            RET[RETURN_KEY1] = -1
            RJPRINT("Inspection test item raise exception, msg: %s" % str(e))
            return RET
    if sum_fail_cont > 0:
        RET[RETURN_KEY3] = -1
    RJPRINT("\n")
    log = "\n\n"
    if sum_fail_cont:
        RJPRINT("There are test failure items")
        log += "There are test failure items\n"
    else:
        RJPRINT("All inspection items passed")
        log += "All inspection items passed\n"
    RJPRINT("\n")
    log += "\n\n"

    try:
        end_time = time.time()
        work_time = end_time - Inspection_START_TIME
        RJPRINT("Inspection Device: %s" % RUIJIE_PRODUCTNAME)
        log += "Inspection Device: %s\n" % (RUIJIE_PRODUCTNAME)
        RJPRINT("Inspection Execution Time: %ss\n" % (str(work_time)))
        log += "Inspection Execution Time: %ss\n\n" % (str(work_time))
        RJPRINT("Inspection Script Version: %s\n" % (SCRIPT_VERSION))
        log += "Inspection Script Version: %s\n\n" % (SCRIPT_VERSION)
        RJPRINT("Inspection PASS Items: \n%s" % (sum_pass_info_tmp))
        log += "Inspection PASS Items: \n%s\n" % (sum_pass_info_tmp)
        RJPRINT("Inspection Failed Items: \n%s" % (sum_fail_info_tmp))
        log += "Inspection Failed Items: \n%s\n" % (sum_fail_info_tmp)
    except Exception as e:
        RET[RETURN_KEY1] = -1
        RJPRINT("Failed to generate inspection report")
        log += "Failed to generate inspection report\n"

    # 返回自定义文件名供上层保存巡检结果，自定义命名格式：TLV_PN + TLV_SN + 时间 + 失败个数.txt
    try:
        sn = getsyseeprombyId(TLV_CODE_SERIAL_NUMBER).get('value')
        pn = getsyseeprombyId(TLV_CODE_PRODUCT_NAME).get('value')
        now_time = time.strftime('%m%d%H%M')
        save_path = path + "/" + pn + "_" + sn + "_" + now_time + "_" + str(sum_fail_cont) + "F" +".txt"
        save_path = save_path.replace(" ","")
        RET[RETURN_KEY2] = save_path
    except Exception as e:
        RET[RETURN_KEY1] = -1
        RJPRINT("Failed to generate inspection file name, msg: %s" % str(e))
        log += "Failed to generate inspection file name, msg: %s\n" % str(e)

    RET["log"] = log
    return RET


def test_all_tmp(test_items):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    global INSP_RESULT
    totalerr = 0
    sum_pass_info_tmp = ""
    sum_fail_info_tmp = ""
    sum_fail_cont = 0
    sum_pass_cont = 0
    time1 = time.time();
    timeArraystart  = time.localtime(time1)
    test_start_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArraystart)

    for item in test_items:
        RJPRINT("")
        RJPRINT("=" * 12 + item[MENUITEMNAME] + "=" *12)
        RET = dealchoosefunc(item)
        RJPRINT("\n")
        formatstr = "======%%-%ds ======:%%-10s\n"%((40+wide_chars(item["name"])))
        if RET[RETURN_KEY1] == 0:
            RJPRINT("[%s]测试结果:" % item[MENUITEMNAME] + 'PASS')
            log_debug("[%s]测试结果:" % item[MENUITEMNAME] + SUCCESS_TIPS)
            sum_pass_cont += 1
            sum_pass_info_tmp += formatstr%(item["name"], "PASS")
        elif RET[RETURN_KEY1] == 1:
            pass
        else:
            totalerr -= 1
            RJPRINT("[%s]测试结果:" % item[MENUITEMNAME] + 'FAIL')
            log_debug("[%s]测试结果:" % item[MENUITEMNAME] + 'error')
            sum_fail_cont += 1
            sum_fail_info_tmp += formatstr%(item["name"], "FAIL")

    time2 = time.time();
    timeArraystart  = time.localtime(time2)
    test_end_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArraystart)

    RJPRINT("\n汇总：")
    RJPRINT(sum_pass_info_tmp)
    RJPRINT(sum_fail_info_tmp)
    RJPRINT("测试开始时间：%s"% test_start_time)
    RJPRINT("测试结束时间：%s"% test_end_time)
    RJPRINT("总共测试项数：%d"%(sum_pass_cont+sum_fail_cont))
    RJPRINT("PASS测试项数：%d"%sum_pass_cont)
    RJPRINT("FAIL测试项数：%d"%sum_fail_cont)
    sn = getsyseeprombyId(TLV_CODE_SERIAL_NUMBER).get('value')
    RJPRINTLINE(" 产品序列号 : %s," % sn)
    if (sum_fail_cont > 0):
        RJPRINT("Test Result: FAIL")
        INSP_RESULT = "FAIL"
    else:
        RJPRINT("Test Result: PASS")
        INSP_RESULT = "PASS"
    return {RETURN_KEY1 : 1,  RETURN_KEY2 : ""}


def test_all():
    return test_all_tmp(alltest)

def test_diag_all():
    return test_all_tmp(diagtestall)

def test_insp_led_ctl(led_list):
    for item in led_list:
        bus = item["bus"]
        loc = item["loc"]
        reg = item["reg"]
        val = item["val"]
        rji2cset(bus,loc,reg,val)

class Logger(object):
    def __init__(self, fileN="/tmp/out.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

    def close(self):
        self.log.close()



def test_stdout_redirect():
    global SAVE_STDOUT
    SAVE_STDOUT = sys.stdout    # 保存标准输出流
    sys.stdout = Logger()  # 输出重定向

def test_stdout_resume():
    global SAVE_STDOUT
    if SAVE_STDOUT is not None:
        sys.stdout.close()
        sys.stdout = SAVE_STDOUT
        SAVE_STDOUT = None


def test_save_insp_result(dst,src = '/tmp/out.log'):
    '''保存巡检结果'''
    global INSP_RESULT
    if not os.path.exists(src):
        return False
    time1 = time.time();
    timeArraystart  = time.localtime(time1)
    test_start_time = time.strftime("%Y-%m-%d-%H-%M-%S", timeArraystart)
    sn = getsyseeprombyId(TLV_CODE_SERIAL_NUMBER).get('value')
    file_name = "%s_%s_%s.log" % (test_start_time,sn,INSP_RESULT)
    if not os.path.exists(dst):
        os.makedirs(dst)
    cmd = "mv %s %s/%s" % (src,dst,file_name)
    status, output = rj_os_system(cmd)
    if status:
        return False
    return True

def test_inspection_pre():
    '''巡检前道工序'''
    # 生测通路检查
    ret, msg = test_bmc_channel()
    if ret == False:
        return ret, msg
    inspection_conf = TESTCASE.get("inspection_config",None)
    if inspection_conf is None:
        return True, ''
    # 挂载U盘 将巡检结果保存到U盘里，待实现
    if inspection_conf.get("mount_usb",0) == 1:
        pass
    led_init_list = inspection_conf.get("led_init",[])
    test_insp_led_ctl(led_init_list)
    test_stdout_redirect()   # 输出定向到控制台和文件
    return True, ''

def test_inspection_after():
    '''巡检后道工序'''
    global INSP_RESULT
    inspection_conf = TESTCASE.get("inspection_config",None)
    if inspection_conf is None:
        return True
    # 恢复标准输出
    test_stdout_resume()
    # 保存巡检结果
    dst_path = inspection_conf.get("log_path")
    test_save_insp_result(dst_path)
    # 卸载U盘 待实现
    if inspection_conf.get("mount_usb",0) == 1:
        pass
    # 点灯提示
    if INSP_RESULT == "PASS":   # 巡检OK
        func = inspection_conf.get("bmc_led_ctl",None)
        if func is not None:    # BMC端点灯
            url_path = getRealUrl(func)
            cmd = "curl -m 3 %s" % url_path
            rj_os_system(cmd)
        else:
            pass
        if inspection_conf.get('halt_flag',0) == 1:    # 关机
            stopFanctrol()
            fac_sensors_kill()
            test_sys_halt()
        return True
    led_alarm = inspection_conf.get("led_alarm",[]) # 巡检失败，点灯告警
    test_insp_led_ctl(led_alarm)
    return True


def test_kr_pre():
    return True,""

def test_kr_after():
    return True,""

# 菜单： 单项测试
def test_signal(id):
    startMenu(id)

def dealfunc(func):
    msg = ""
    for i in range(0, 3):
        ret, msg = func()
        if ret == True:
            return True
        else:
           continue
    raise Exception(msg)
    return False


def dealchoosefunc(list):
    '''真正菜单处理项'''
    RET = ERROR_RETURN
    funcbefore = None
    functest  = None
    funcafter = None
    param_tt = None
    param_val = None
    funcbeforestr = list.get(ITEMBEFORE, None)
    functeststr = list.get(MENUITEMDEAL, None)
    funcafterstr = list.get(ITEMAFTER, None)
    param_tt = list.get(CHILDID, None)
    param_val = list.get('param', None)

    if funcbeforestr is not None:
        funcbefore = eval(funcbeforestr)
    if functeststr is not None:
        functest = eval(functeststr)
    if funcafterstr is not None:
        funcafter = eval(funcafterstr)
    try:
        if funcbefore is not None:
            log_debug("    测试项前置:%s " % (funcbefore))
            dealfunc(funcbefore)
        if functest is not None:
            log_debug("    测试项    :%s " % (functest))
            if param_tt is not None:
                RET = functest(param_tt)
            else:
                if param_val is not None:
                    RET = functest(param_val)
                else:
                    RET = functest()
        else:
            raise Exception("fun test is none")
    except Exception as e:
        msg = traceback.format_exc()
        log_error(msg)
        RJPRINT(msg)
        RJPRINT("error\n\n")
    finally:
        if funcafter is not None:
            log_debug("    测试项后置:%s " % (funcafter))
            for i in range(0, 3):
                ret, _ = funcafter()
                if ret == True:
                    break
                elif i == 2:
                    log_debug("    测试项后置:%s run fail 3 times" % (funcafter))
    return RET


#菜单打印
#  printMenu
#  param: list_t  菜单项列表
#         id      菜单id
#
def printMenu(list_t, id):
    global nosetrtc
    while True:
        try:
            printList(list_t, id)
            test = "请选择:"
            ch = getch(test)
            RJPRINT(" %s" % ch)
            log_debug("选择:%s" % ch)
            ch = ch.lstrip().lower()
            if PYTHON_VERSION >= 3:
                ch = byteTostr(ch)
            if ch == "q":
                if id == STARTMENUID:  #顶层目录，无路可退
                    log_debug("wait subprocess exit")
                    subprocess_case.shutdown_bgtest()
                    quit()
                else:
                    break
            if ch not in listindex:
                log_debug("%s 不在菜单项中" % ch);
                RJPRINT("\n\n")
                continue
            else:
                RJPRINT("=======================> %s <======================="%list_t[listindex.index(ch)][MENUITEMNAME])
                log_debug("选择的测试项为:%s id:%d" % (list_t[listindex.index(ch)][MENUITEMNAME], id))

                if list_t[listindex.index(ch)].get('lock', False) and (subprocess_case.is_running()
                    or subprocess_case.is_stopping()):#后台执行时，部分测试项不可入。
                    RJPRINT("后台测试中 %s 不可执行" % list_t[listindex.index(ch)][MENUITEMNAME]);
                    RJPRINT("\n\n")
                    continue
                RET = dealchoosefunc(list_t[listindex.index(ch)])
                if RET == None:
                    RJPRINT("\n\n")
                    continue
                RJPRINT(" ")
                if RET[RETURN_KEY1] == 0:
                    RJPRINT("Test Result: PASS")
                    log_debug("菜单测试结果:" + SUCCESS_TIPS)
                elif RET[RETURN_KEY1] == 1:
                    pass
                else:
                    RJPRINT("Test Result: FAIL")
                    log_debug("[%s]测试结果:" % list_t[listindex.index(ch)][MENUITEMNAME] + 'error')
                    if isinstance(RET[RETURN_KEY2], str) and len(RET[RETURN_KEY2]) !=0:
                        log_debug("RET[RETURN_KEY2]:%s" % RET[RETURN_KEY2])

                RJPRINT("\n\n")
        except IndexError as d:
            RJPRINT("\n\n非法输入\n\n")
        except Exception as e:
            RJPRINT(e)
            RJPRINTERR("\n\n 异常\n\n" )

def getMenuFromList(list, id):
    for key in list:
        if key[MENUID] == id:
            return key[MENUVALUE],True
    return 0, False

def getParentIdMenuFromList(list, id):
    for key in list:
        if key[MENUID] == id:
            return key[MENUPARENT],True
    return -1, False

def getDriverFromGlobal(name):
    for key in testdriver:
        if key["name"] == name:
            return key,True
    return "-1", False

def i2ccheckValue(ret1 , ret2, type):
    if type == 1 and ret1 == ret2:
        return True
    elif type == 2 and ret1 == "SUCCESS":
        return True
    else:
        return False

def test_i2c_scan(scan_list):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    errtotal = 0
    errmsg  = ""
    for i2cdev in scan_list:
        STATE = "FAILED"
        formatstr = "    %%-%ds %%-10s"%((40+wide_chars(i2cdev['name'])))

        before_cmd = i2cdev.get("before_cmd", None)
        if before_cmd is not None:
            rj_os_system(before_cmd)

        type = i2cdev.get("gettype", None)
        if type == "I2C_32":
            ret, log = rji2cget_32bit(i2cdev["bus"], i2cdev["addr"], "0x00 0x00 0x00 0x00")
        else:
            ret, log = rji2cget(i2cdev["bus"], i2cdev["addr"], 0)
        if ret == False or "Error" in log:
            STATE = "FAILED"
            errtotal -= 1
            errmsg = "%s %s\n" % (errmsg,formatstr%(i2cdev['name'],log))
        else:
           STATE = "PASS"
        RJPRINT(formatstr%(i2cdev['name'],STATE))

        after_cmd = i2cdev.get("after_cmd", None)
        if after_cmd is not None:
            rj_os_system(after_cmd)

    if errtotal < 0:
      RET[RETURN_KEY1] = errtotal
    RET[RETURN_KEY2] = errmsg
    return RET

def test_i2c_before():
    commands = TESTCASE.get("I2C_TEST", None).get("i2c_test_bef_cmd",None)
    ret, val = send_commands(commands, True)
    if ret:
        return True, ""
    else:
        return False, ""

def test_i2c_after():
    commands = TESTCASE.get("I2C_TEST", None).get("i2c_test_aft_cmd",None)
    ret, val = send_commands(commands, True)
    if ret:
        return True, ""
    else:
        return False, ""

def test_i2c_new():
    return test_i2c_scan(TESTCASE["I2CSCAN"])

def test_diag_i2c():
    return test_i2c_scan(TESTCASE["DIAGI2CSCAN"])


# 菜单：测试i2c
def test_i2c():
    RET = {RETURN_KEY1 : -1, RETURN_KEY2 : []}
    result_key = 0
    for i2c in TESTCASE["I2C"]:
        testerror ={}
        RJPRINT("测试项[%s] " % i2c["name"])
        log_debug("测试项[%s] " %i2c["name"])
        testerror["name"] = i2c["name"]
        caseerror =[]
        if "cases" not in i2c:
            RJPRINT("没有测试项")
            log_debug("没有测试项")
            continue
        for case in i2c["cases"]:
            ###获取调用的命令
            cmd_t = case["cmd"].lstrip()
            cmd = cmd_t[0 : cmd_t.index(" ")]
            ret_t, log = log_os_system("which " + cmd, 0)
            if len(log):
                cmd = "cmd find "
            else:
                result_key -= 1
                caseerror.append({"name":case["name"] ,"error":"cmd not find"})
                continue
            ret_t, log = log_os_system(case["cmd"], 0)
            if ret_t or ("Error" in log ):
                status = "[FAILED]"
                result_key -= 1
                caseerror.append({"name":case["name"] ,"error":log})
                log_debug("case: %s   [%s]  %s" % (case["name"] , case["cmd"],"fail"))
            else:
                value = " "
                if "value" not in case:
                    value = " "
                else:
                    value = case["value"]
                if i2ccheckValue(log, value, case["deal_type"]):
                    status = "[ok]"
                    log_debug("case: %s   [%s]  %s" % (case["name"] , case["cmd"],"ok"))
                else:
                    status = "[FAILED]"
                    log_debug("case: %s   [%s]  %s" % (case["name"] , case["cmd"],"fail"))
                    result_key -= 1
                    caseerror.append({"name":case["name"] ,"error": log})
            formatstr = "    %%-%ds %%-10s"%((40+wide_chars(case["name"])))
            RJPRINT(formatstr%(case["name"],status))
            testerror['errmsg'] = caseerror
        RET[RETURN_KEY2].append(testerror)
    if result_key <= 0:
        RET[RETURN_KEY1] = result_key
    #log_debug(RET)
    return RET

#不论大小比较字符串
def astrcmp(str1,str2):
    return str1.lower()==str2.lower()

def makesure(info, default = True ,echo = False):
    while True:
        print(info, end=' ')
        if echo:
            str = input()
        else:
            str = get_raw_input()
        if astrcmp(str, ""):
            return default
        if astrcmp(str, "y") or astrcmp(str, "ye") or astrcmp(str, "yes"):
            return True
        elif astrcmp(str, "n") or astrcmp(str, "no"):
            return False
        else:
            RJPRINT("输入无效,请重新输入，")

#led check输入确认
def get_led_inputcheck():
    err = 0;
    str = input("确认状态灯是否正确切换[Yes/no]：")
    if astrcmp(str, "y") or astrcmp(str, "ye") or astrcmp(str, "yes") or astrcmp(str, ""):
        return True
    else:
        return False

def test_mgmtled():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    lb_with_Plug = TESTCASE.get('mgmt').get('100M')
    resetphy  = TESTCASE.get('mgmt').get('clear')
    lenon = TESTCASE.get("mgmt",{}).get("ledon",None)
    ledoff = TESTCASE.get("mgmt",{}).get("ledoff",None)
    ind = 0
    try:
        ret = test_bmc_func(resetphy.get('case'), resetphy.get('param'))
        if ret is None:
            raise Exception('初始phy失败')
        ret = test_bmc_func(lb_with_Plug.get('case'), lb_with_Plug.get('param'))
        if ret is None:
            raise Exception('设置100回环失败')
        time.sleep(0.5)
        key = "(link灯：橙色)"
        if makesure("确认切换到%s（Yes/No):"%key ,echo = 1) == True:
            ret = test_bmc_func(resetphy.get('case'), resetphy.get('param'))
            time.sleep(0.5)
        else:
            ind = -1
        cmd = lenon.get("cmd",None)
        func = lenon.get("bmc_interface",None)
        ret = test_bmc_func(func,cmd)
        key = "(link灯：绿 、act灯：绿)"
        if makesure("确认切换到%s（Yes/No):"%key ,echo = 1) == True:
            ret = test_bmc_func(resetphy.get('case'), resetphy.get('param'))
            time.sleep(0.5)
        else:
            ind = -2
        key = "(link灯：灭 、act灯：灭)"
        cmd = ledoff.get("cmd",None)
        func = ledoff.get("bmc_interface",None)
        ret = test_bmc_func(func,cmd)
        if makesure("确认切换到%s（Yes/No):"%key ,echo = 1) == True:
            ret = test_bmc_func(resetphy.get('case'), resetphy.get('param'))
            time.sleep(0.5)
        else:
            ind = -3
    except Exception as e:
        ind = -999
        RET[RETURN_KEY2] = str(e)
        print(str(e))
    finally:
        ret = test_bmc_func(resetphy.get('case'), resetphy.get('param'))
        time.sleep(0.5)
    RET[RETURN_KEY1] = ind
    return RET


def test_led_new():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    led_param = TESTCASE["LED_NEWS"]
    total_err = 0
    rest_status = 0

    for item_keys in sorted(led_param.keys()):
        item_led = led_param.get(item_keys)
        try:
            ''' 新加逻辑,在端口点灯前先判断是否需要关闭前置寄存器 '''
            led_control = item_led.get('LED_CONTROL', None)
            if led_control is not None:
                ind = led_control.get("open", 0)
                if ind == 1:
                    regs  = led_control.get("regs", [])
                    for item in regs:
                        rji2cset(item["bus"], item["devno"], item["addr"], item["open"])
                else:
                    pass
            else:
                pass

            attrs = item_led.get('attrs')
            device = item_led.get('device')
            RJPRINT(item_led.get('name'))

            for key, val in list(attrs.items()):
                for item in device:
                    gettype = item.get("gettype",'i2c')
                    if gettype == 'i2c': #i2c
                        bmc_cmd = item.get("bmc_command", 0)
                        if bmc_cmd == 1:
                            func = 'bmc_log_os_system'
                            cmd = "i2cset -f -y %d 0x%02x 0x%02x 0x%02x" % (item.get('bus'),item.get('addr'),item.get('reg'), val)
                            ret = test_bmc_func(func, cmd)
                        else:
                            rji2cset(item.get('bus'),item.get('addr'),item.get('reg'), val)
                    elif gettype == 'io':
                        io_wr(item.get('io_addr'), val)
                    elif gettype == 'cmd':
                        cmd = item.get('cmd') % val
                        rj_os_system(cmd)
                    elif gettype == 'pcie':
                        pcibus = item.get('pcibus')
                        slot = item.get('slot')
                        bar = item.get('bar')
                        fn = item.get('fn')
                        offset = item.get('offset')
                        rjpciwr(pcibus, slot, fn, bar, offset, val)
                    elif gettype == 'restful':
                        returncode, msg = test_bmc_channel()
                        if returncode == False:
                            total_err -= 1
                            rest_status = -1
                            RJPRINT(msg)
                            break
                        func = item.get('func')
                        param = item.get('param')
                        param['value'] = val
                        ret = test_bmc_func(func,param)
                if rest_status < 0:
                    rest_status = 0
                    break
                if makesure("确认切换到%s（Yes/No):"%key ,echo = 1) == True:
                    continue
                else:
                    total_err -=1
        except Exception as e:
                total_err = -999
                RET[RETURN_KEY2] = str(e)
        finally:
            ''' 新加逻辑,在端口点灯后先判断是否需要关闭前置寄存器 '''
            led_control = item_led.get('LED_CONTROL', None)
            if led_control is not None:
                ind = led_control.get("open", 0)
                if ind == 1:
                    regs  = led_control.get("regs", [])
                    for item in regs:
                        rji2cset(item["bus"], item["devno"], item["addr"], item["close"])
                else:
                    pass
            else:
                pass


    RET[RETURN_KEY1] = total_err
    # 取前后
    return RET

#系统灯测试
def test_led():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    try:
        stopFanctrol()
        for led in TESTCASE["LED"]:
            RJPRINT("测试项: %s" % led["name"])
            if "cases" not in led:
                RJPRINT("没有测试项")
                continue
            for case in led["cases"]:
                RJPRINT(case["name"])
                ###获取调用的命令
                if "cmd" in list(case.keys()):
                    cmd_t = case["cmd"].lstrip()
                    cmd = cmd_t[0 : cmd_t.index(" ")]
                    ret, log = log_os_system("which " + cmd, 0)
                    if len(log):
                        cmd = "cmd find "
                    else:
                        RET[RETURN_KEY2] = "no " + cmd +" found"
                        log_debug(RET[RETURN_KEY2])
                        RJPRINT(RET[RETURN_KEY2])
                        RET[RETURN_KEY1] = -1
                        return RET
                    log_debug(case["cmd"])
                    ret, log = log_os_system(case["cmd"], 0)
                    if ret or ("Error" in log ):
                        RJPRINT("[ERROR]")
                        totalerr -= 1
                    else:
                        if get_led_inputcheck():
                           RJPRINT("[PASS]")
                        else:
                           RJPRINT("[FAIL]")
                           totalerr -= 1
                elif "deal_bmc_led" in list(case.keys()):
                    returncode, msg = test_bmc_channel()
                    if returncode == False:
                        totalerr -= 1
                        RJPRINT(msg)
                        continue
                    func = case["deal_bmc_led"]
                    param = case["param"]
                    ret = test_bmc_func(func,param)
                    if ret[RETURN_KEY1] != 0:
                        RJPRINT("[ERROR]")
                        totalerr -= 1
                    else:
                        if get_led_inputcheck():
                           RJPRINT("[PASS]")
                        else:
                           RJPRINT("[FAIL]")
                           totalerr -= 1
    except Exception as e:
        RJPRINT(e)
        totalerr -= 1
    finally:
        startFanctrol()
    RET[RETURN_KEY1] = totalerr
    return RET


#设置debug等级
def test_setdebug():
    global DEBUG
    DEBUG = not DEBUG
    if DEBUG == False:
        RJPRINT("调试开关关闭")
    else:
        RJPRINT("调试开关打开")
    return SUCCESS_RETURN

#根据id获取菜单
def startMenu(id):
    list,code = getMenuFromList(menuList, id)
    if code == False:
        log_error("错误的文件结构")
        RJPRINT("无此菜单，请确认")
        sys.exit(1)
    log_debug("根据ID获取到相应的菜单列表")
    printMenu(list, id)

def keyboardTest():
    while True:
        log_debug("123")

def startThread():
    thread = threading.Thread(target=keyboardTest)
    thread.setDaemon(True)
    thread.start()

def rji2cset(bus, devno, address, byte):
    command_line = "i2cset -f -y %d 0x%02x 0x%02x 0x%02x" % (
        bus, devno, address, byte)
    retrytime = 6
    ret_t = ""
    for i in range(retrytime):
        ret, ret_t = rj_os_system(command_line)
        if ret == 0:
            return True, ret_t
    return False, ret_t

def rjpcird(pcibus, slot, fn, resource, offset):
    '''read pci register'''
    if offset % 4 != 0:
        return "ERR offset: %d not 4 bytes align"
    filename = "/sys/bus/pci/devices/0000:%02x:%02x.%x/resource%d" % (int(pcibus), int(slot), int(fn), int(resource))
    with open(filename, "r+") as file:
        size = os.path.getsize(filename)
        data = mmap.mmap(file.fileno(), size)
        result = data[offset: offset + 4]
        s = result[::-1]
        val = 0
        for value in s:
            val = val << 8 | value
        data.close()
    return "0x%08x" % val


def inttostr(vl,len): # 将int 转为字符串 如 0x3030 = 00
    if type(vl) != int:
        raise Exception(" type error")
    index = 0
    ret_t = ""
    while index < len:
        ret = 0xff & (vl >> index * 8)
        ret_t += chr(ret)
        index += 1;
    return ret_t

def rjpciwr(pcibus, slot, fn, resource, offset):
    '''write pci register'''
    ret = inttobytes(data, 4)
    filename = "/sys/bus/pci/devices/0000:%02x:%02x.%x/resource%d" % (int(pcibus), int(slot), int(fn), int(resource))
    with open(filename, "r+") as file:
        size = os.path.getsize(filename)
        data = mmap.mmap(file.fileno(), size)
        data[offset: offset + 4] = ret
        result = data[offset: offset + 4]
        s = result[::-1]
        val = 0
        for value in s:
            val = val << 8 | value
        data.close()


# 开始
def start():
    #menuid =  if vars().has_key('STARTMENUID') else 0
    #print menuid
    #print STARTMENUID
    global STARTMENUID
    if STARTMENUID is None:
        STARTMENUID = 0
    startMenu(STARTMENUID)

def test_cpu_stress_show():
    ret, log = log_os_system("top -bi -n2 -d 0.2 | grep '%Cpu(s)' | tail -n1", 0)
    if ret:
        print("获取CPU信息失败")
    else:
        value , times = re.subn("[\S\s]*,\s*([\.\d]+)\sid[\S\s]*","\g<1>", log)
        if times != 1:
            print(log)
            print("获取CPU利用率失败")
        else:
            print("当前cpu利用率为%.1f%%"%(100 - float(value)))
    return {RETURN_KEY1 : 1, RETURN_KEY2 : ""}

CpuStressCmd = TESTCASE.get("CpuStressCmd", "stress -c 4")
def process_cpu_stress_test(interval):
    #print("The time is {0}".format(time.ctime()))
    #产生4个进程，每个进程都反复不停的计算由rand ()产生随机数的平方根
    cmd = CpuStressCmd
    ret, log = log_os_system(cmd, 0)

def test_cpu_stress():
    RET = {RETURN_KEY1 : 1, RETURN_KEY2 : "已启动后台执行"}

    ret, log = rj_os_system("ps -ef | grep \"%s\"| grep -v grep" % CpuStressCmd)
    if ret == 0:
        RJPRINT(RET[RETURN_KEY2])
        return RET
    ret, log = log_os_system("which stress", 0)
    if len(log):
        p = multiprocessing.Process(target = process_cpu_stress_test, args = (3,))
        p.daemon = True
        p.start()
    else:
        RET[RETURN_KEY2] = "no stress cmd"
    RJPRINT(RET[RETURN_KEY2])
    return RET


# 获取内存信息
def memory_stat():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    mem = {}
    f = open("/proc/meminfo")
    lines = f.readlines()
    f.close()
    resultval = []
    for line in lines:
        if len(line) < 2: continue
        name = line.split(':')[0]
        var = line.split(':')[1].split()[0]
        mem[name] = int(var)
    mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
    if 0 < mem['MemUsed'] < mem['MemTotal']:
        statusmsg = "OK"
    else:
        statusmsg = 'Not OK'
        RET[RETURN_KEY1] = -1
    resultval.append(["%s%s"%(mem['MemUsed'], 'kB'), "%s%s"%(mem['MemTotal'], 'kB'), statusmsg])

    #打印
    header = ['MemUsed','MemTotal', 'State']
    result = tabulate(resultval, header, tablefmt='simple')
    RJPRINT(result)
    return RET

def get_sdk_version():
    return SdkCmdCase.get_sdk_version()


def get_cpu_message():
    cpu_ret = getDmiSysByType("processor")
    return cpu_ret

def get_phypcie_version():
    return SdkCmdCase.get_phypcie_version()

def show_cpu_info():
    totalerr = 0
    msg = ""
    cmd = "cat /proc/cpuinfo "
    ret, log = log_os_system(cmd, 0)
    if ret != 0 or len(log) <= 0:
        msg = "command [%s] execution error, msg: %s" % (cmd,log)
        RJPRINT(msg)
        return -1, msg
    for line in log.strip().split("\n"):
        RJPRINT("    %s" % line)
    return totalerr, msg

def show_ddr_info():
    cmd = "cat /proc/meminfo"
    ret, log = log_os_system(cmd, 0)
    if ret != 0 or len(log) <= 0:
        msg = "command [%s] execution error, msg: %s" % (cmd,log)
        RJPRINT(msg)
        return -1, msg
    for line in log.strip().split("\n"):
        RJPRINT("    %s" % line)
    return 0, ""


def get_sonic_version():

    tmp_t ={}
    try:
        with open("/etc/sonic/sonic_version.yml") as fd:
            version = fd.read()
        for line in version.strip().split("\n"):
            if ":" not in line:
                continue
            RJPRINT("    %s" % line)
            ver_list = line.split(":")
            tmp_t[ver_list[0].strip()] = ver_list[1].strip()
        sonic_version_check = TESTCASE.get('dev_info').get('sonic_version')
        if sonic_version_check is not None:
            if tmp_t.get("build_version") != sonic_version_check.strip():
                RJPRINT("    SONiC version detection failed, device version: %s, expected version: %s" % (tmp_t.get("build_version"), sonic_version_check.strip()))
                return False
        return True
    except Exception as e:
        RJPRINT(traceback.format_exc())
        return False

def show_version():
    cmd = "show version"

    ret, log1 = log_os_system(cmd, 0)
    if ret != 0 or len(log1) <= 0:
        return -1, "command [%s] execution error, msg: %s" % (cmd, log1)
    else:
        log1 = log1.splitlines()
        for line in log1:
            if "Error" in line:
                RJPRINT("    " + line + "errmsg: %s" % line)
            else:
                RJPRINT("    " + line)
    return 0, "command[%s]" % cmd

def getFormatHead(HEAD):
    len_t = len(HEAD)
    formatstr = "    "
    headtip = formatstr
    septips = formatstr
    for i in range(len_t):
        formatstr += "%-20s "
        headtip += "%%-%ds "%(20+wide_chars(HEAD[i]))
        septips +="%-20s "
        headtip = headtip % HEAD[i]
        septips = septips % ("-"*20)
    print(headtip)
    print(septips)
    return formatstr


def rji2cgetWord(bus, devno, address):
    command_line = "i2cget -f -y %d 0x%02x 0x%02x w" % (bus, devno, address)
    retrytime = 3
    ret_t = ""
    for i in range(retrytime):
        ret, ret_t = rj_os_system(command_line)
        if ret == 0:
            return True, ret_t
    return False, ret_t


def rji2cget(bus, devno, address):
    command_line = "i2cget -f -y %d 0x%02x 0x%02x " % (bus, devno, address)
    retrytime = 6
    ret_t = ""
    for i in range(retrytime):
        ret, ret_t = rj_os_system(command_line)
        if ret == 0:
            return True, ret_t
        time.sleep(0.1)
    return False, ret_t

def rji2cget_32bit(bus, devno, address): #address = "0x00 0x00 0x00 0x00"
    dfd_debug_path = TESTCASE.get("dfd_debug_path", None)
    if dfd_debug_path == None:
        command_line = "dfd_debug i2c_gen_rd %d 0x%02x 4 %s 4" % (bus, devno, address)
    else:
        command_line = "%s i2c_gen_rd %d 0x%02x 4 %s 4" % (dfd_debug_path, bus, devno, address)
    retrytime = 6
    ret_t = ""
    for i in range(retrytime):
        ret, ret_t = rj_os_system(command_line)
        if ret == 0:
            return True, ret_t
        time.sleep(0.1)
    return False, ret_t


def get_mgmt_version(is_onl=False):
    ip_netns_exec = TESTCASE.get("ip_netns_exec", 1)
    tmp_t ={}
    if is_onl is True:
        mgmt = "ma1"
    else:
        mgmt = "eth0"
    if ip_netns_exec == 1:
        cmd = "ip netns exec mgmt ethtool -i %s" % mgmt
    else:
        cmd = "ethtool -i %s" % mgmt
    valstr = ""
    ret , log = rj_os_system(cmd)
    if ret != 0:
        return False
    else:
        version_temp = log.split('\n')
        for line in version_temp:
            RJPRINT("    %s" % line.strip())
            if ":" in line:
                ver_list = line.strip().split(":")
                tmp_t[ver_list[0].strip()] = ver_list[1].strip()
    i2c_version_check = TESTCASE.get('dev_info').get('I210_FW_version')
    if i2c_version_check is not None:
        if tmp_t.get("firmware-version") != i2c_version_check.strip():
            RJPRINT("    I210 firmware-version detection failed, device version: %s, expected version: %s" % (tmp_t.get("firmware-version"), i2c_version_check.strip()))
            return False
    return True


def get_harddisk_info(sddev):
    ret = {}
    cmd = "smartctl -i /dev/%s |grep Device -A13" % sddev
    ret1, log1 = rj_os_system(cmd)
    if ret1 != 0 or len(log1) <= 0:
        return False, "command[%s] execution error" % cmd
    its = log1.replace("\t", "").strip().split("\n")
    for it in its:
        if ":" in it:
            key = it.split(":", 1)[0].lstrip()
            value = it.split(":", 1)[1].lstrip()
            ret[key] = value
    return True, ret

def show_harddisk_info():
    RET = {RETURN_KEY1 : -1, RETURN_KEY2 : ""}
    cmd = "ls -l /sys/block/sda"
    ind = None
    val = None
    ret, output = log_os_system(cmd, 0)
    sata_key, times = re.subn(".*/(ata.)/*","\g<1>",output.lower())
    ret, log = log_os_system("which smartctl", 0)
    if len(log):
        ind, val =get_harddisk_info("sda")
    else:
        RET[RETURN_KEY2] = "no smartctl cmd"
        return RET
    #print val
    valtemp = "    Serial Number    : {Serial Number}\n"\
              "    Device Model     : {Device Model}\n"\
              "    SATA Version     : {SATA Version is}\n"\
              "    User Capacity    : {User Capacity}\n"\
              "    Firmware Version : {Firmware Version}\n"

    s = valtemp.format(**val)
    if TESTCASE.get("ssd_slot_num", 1) == 2:
        if sata_key[0:4] == "ata1" :
            RJPRINT("  SATA slot          : 1")
            RJPRINT(s)
            RJPRINT("  SATA slot          : 2 (Not present)")
        else:
            RJPRINT("  SATA slot          : 1 (Not present)")

            RJPRINT("  SATA slot          : 2")
            RJPRINT(s)
    else:
        RJPRINT(s)
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    return RET

def get_cpld_version():
    #header = ["名称","日期","版本"]
    #formatstr = getFormatHead(header)
    result = []
    totalerr = 0
    for cpld in CPLDVERSIONS:
        dict = {}
        gettype = cpld.get("gettype",None)
        bus = cpld.get("bus",None)
        devno = cpld.get("devno",None)
        url = cpld.get("url",None)
        io_addr = cpld.get("io_addr",None)
        data = ""
        t = True
        ret = None
        if gettype == "lpc":
            for i in range(4):
                ret = lpc_cpld_rd(i)
                if ret == None:
                    t = False
                    break;
                data += chr(int(ret,16))
        elif gettype == "io":
            for i in range(4):
                ret = io_rd(io_addr + i)
                if ret == None:
                    t = False
                    break;
                data += chr(int(ret,16))
        elif gettype == "restful":
            ret = cpld_version_restful(url)
            if ret == None:
                continue
            data_1 = ret.replace("\""," ").strip().split(" ")
            for item in data_1:
                data += chr(int(item,16))
        else:
            for i in range(4):
                ind, ret = rji2cget(bus, devno, i)
                if ind == False:
                    t = False
                    break;
                data += chr(int(ret,16))
        if data == "":
            totalerr -= 1
            result.append([ cpld.get('name',None),"NA","NA" ])
        else:
            result.append([ cpld.get('name',None),"%02x%02x%02x" %  (ord(data[1]) ,ord(data[2]) ,ord(data[3])),"%02x" %  (ord(data[0]))])
    #for item in result:
    #    formatstr = "    %%-%ds %%-20s %%-20s "%((20+wide_chars(item[0])))
    #    print (formatstr%(item[0],item[1],item[2]))
    return totalerr,result

def show_81724_version():
    ret, log = SdkCmdCase.show_81724_version()
    RJPRINT("    %s" % log)
    return ret

def show_fpga_version():
    RJPRINT("")
    RJPRINT("%s " % "FPGA Version")
    fpgastatus = TESTCASE.get("FPGA_INFO", None)
    fpga_version_check = TESTCASE.get('dev_info').get('fpga_check').get('version', None)
    fpga_version_check = fpga_version_check.replace("\x00", "").strip()
    totalerr = 0
    for item in fpgastatus:
        if item.get("gettype",None) == 'pci':
            pcibus = item.get("pcibus",None)
            slot = item.get("slot",None)
            fn = item.get("fn",None)
            bar = item.get("bar",None)
            offset = item.get("offset",None)
            ret = rjpcird(pcibus, slot, fn, bar, offset)
            ret = ret.replace("\x00", "").strip()
            if ret is None:
                totalerr = -1
                RJPRINT("\tget %s failed: fpga"% item.get("name", "error para"))
                continue
            else:
                if item.get("name", None) == "version":
                    ret = ret.replace("\x00", "").strip()
                    if fpga_version_check == ret:
                        RJPRINT("    %-20s: %s" % (item.get("name", "error para"), ret))
                    else:
                        totalerr = -1
                        RJPRINT("    %-20s: FPGA version detection failed, device version: %s, expected version: %s" %
                            (item.get("name", "error para"), ret, fpga_version_check))
        else:
            pass
    RJPRINT("")
    return totalerr

def show_mul_fpga_version():
    totalerr = 0
    RJPRINT("")
    RJPRINT("FPGA Version")
    fpga_check = TESTCASE.get('dev_info').get('fpga_check', {})
    for fpga_show in TESTCASE.get("MUL_FPGA_INFO", None):
        fpga_name = fpga_show.get('fpga_name', None)
        fpga_version_check = fpga_check.get(fpga_name, None)
        fpga_version_check = fpga_version_check.replace("\x00", "").strip()
        #RJPRINT("%s" % (fpga_show.get('fpga_name')))
        for item in fpga_show.get('value'):
            if item.get("gettype",None) == 'pci':
                pcibus = item.get("pcibus",None)
                slot = item.get("slot",None)
                fn = item.get("fn",None)
                bar = item.get("bar",None)
                offset = item.get("offset",None)
                ret = rjpcird(pcibus, slot, fn, bar, offset)
                if ret is None:
                    totalerr = -1
                    RJPRINT("\tget %s failed: fpga"% item.get("name", "error para"))
                    continue
                else:
                    if item.get("name", None) == "version":
                        ret = ret.replace("\x00", "").strip()
                        if fpga_version_check == ret:
                            RJPRINT("    %-20s: %s" % (item.get("name", "error para"), ret))
                        else:
                            RJPRINT("    %-20s: FPGA version detection failed, device version: %s, expected version:%s" %
                                (item.get("name", "error para"), ret, fpga_version_check))
            else:
                pass
    return totalerr

def devfileread_fpga_version():
    totalerr = 0
    fpga_check = TESTCASE.get('dev_info').get('fpga_check', {})
    for fpga_show in TESTCASE.get("DEVFILEREAD_FPGA_INFO", None):
        RJPRINT("")
        fpga_name = fpga_show.get('fpga_name')
        RJPRINT("%s" % fpga_name)
        fpga_version_check = fpga_check.get(fpga_name, None)
        fpga_version_check = fpga_version_check.replace("\x00", "").strip()
        for item in fpga_show.get('value'):
            path = item.get("path",None)
            offset = item.get("offset",None)
            len = item.get("len",None)
            bit_width = item.get("bit_width",None)
            version_str = platform_manufacturer.devfileread(path, offset, len, bit_width)
            if version_str is None:
                totalerr = -1
                RJPRINT("\tget %s failed: fpga"% item.get("name", "error para"))
                continue
            else:
                if item.get("name", None) == "version":
                    ret = version_str.replace("\x00", "").strip()
                    if fpga_version_check == ret:
                        RJPRINT("    %-20s: %s" % (item.get("name", "error para"), ret))
                    else:
                        RJPRINT("    %-20s: FPGA version detection failed, device version: %s, expected version: %s" %
                            (item.get("name", "error para"), ret, fpga_version_check))
    return totalerr

def check_cpu_mac(is_onl=False):
    #    print "CPU,BMC,TLV,FRU的MAC和录入的MAC进行比较"
    log1 = getsyseeprombyId(TLV_CODE_MAC_BASE).get('value')
    # cmd="ifconfig eth0 |grep HWaddr |awk '{print $5}'"
    if is_onl is True:
        mgmt = "ma1"
    else:
        mgmt = "eth0"
    cmd = "ifconfig %s" % mgmt
    ret, log2 = log_os_system(cmd, 0)
    if ret != 0:
        log_debug("\n ifconfig %s failed" % mgmt)
        return {RETURN_KEY1: -1, RETURN_KEY2: "ifconfig %s failed" % mgmt}
    str_eth_tmp = re.subn('[\r\n\t]', ' ', log2.lower())
    cpu_mac = re.sub(".*(([0-9a-fA-F]{2,2}:){5,5}[0-9a-fA-F]{2,2}).*", "\g<1>", str_eth_tmp[0])
    if len(cpu_mac) != 17:
        log_debug("Failed to get CPU MAC address")
        return {RETURN_KEY1: -1, RETURN_KEY2: "Failed to get CPU MAC address"}
    log_debug("cpu_mac = %s, e2_mac = %s" % (cpu_mac.lower(), log1.lower()))
    if cpu_mac.lower() == log1.lower():
        return {RETURN_KEY1: 0, RETURN_KEY2: cpu_mac.lower()}
    else:
        log_debug("CPU MAC address:%s is not equal to ONIE E2 MAC address: %s" % (cpu_mac.lower(), log1.lower()))
        return {RETURN_KEY1: -1, RETURN_KEY2: "CPU MAC address:%s is not equal to ONIE E2 MAC address: %s" % (cpu_mac.lower(), log1.lower())}

def show_bmc_mac():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    ret, msg = test_bmc_channel()
    if ret == False:
        log_debug("show_bmc_mac bmc channel error:%s" % msg)
        RET[RETURN_KEY1] = -1
        return RET

    cmd = "ifconfig eth0 |grep HWaddr |awk '{print $5}'"
    func = 'bmc_log_os_system'
    ret = test_bmc_func(func,cmd)
    if ret.get(RETURN_KEY1) == -1 or len(ret.get(RETURN_KEY2)) == 0:
        RET[RETURN_KEY1] = -1
        log_debug("Failed to get BMC MAC address\nmessage:%s" % (ret.get(RETURN_KEY2)))
    else:
        RET = ret
        log_debug("BMC MAC Get Success")
    return RET

def add_mac_num(list_mac,n):
    str_mac_lower=list(list_mac.lower())
    for j in range(int(n)):
        add_n=1
        for i in range(17):
            if str_mac_lower[16-i] ==':':
                continue
            else:
               if add_n==1:
                   if str_mac_lower[16-i]=='f':
                       str_mac_lower[16-i]='0'
                   elif str_mac_lower[16-i]=='9':
                       str_mac_lower[16-i]='a'
                       add_n=0
                   else:
                       int_mac=ord(str_mac_lower[16-i])+1
                       str_mac_lower[16-i]=chr(int_mac)
                       add_n=0
               else:
                   break
    return ''.join(str_mac_lower)

def show_device_mac(is_onl=False):
    global BMC_DIAG_FLAG
    RJPRINT("%s " % "MAC address:")
    RET = {RETURN_KEY1: 0, RETURN_KEY2: ""}

    RET = check_cpu_mac(is_onl)
    result = 0
    if RET[RETURN_KEY1] < 0:
        RJPRINT("    CPU: fail %s" % RET[RETURN_KEY2])
        result = -1
    else:
        RJPRINT("    CPU: %s" % RET[RETURN_KEY2])
    if BMC_DIAG_FLAG == 1:
        if FACTESTMODULE.get("bmc_present", 0) == 1 or bmc_presence_check():
            bmc_right_macaddr = add_mac_num(RET[RETURN_KEY2], 2)
            RET = show_bmc_mac()
            if RET[RETURN_KEY1] < 0:
                RJPRINT("    BMC：fail %s" % RET[RETURN_KEY2])
                result = -1
            elif RET[RETURN_KEY2].lower() != bmc_right_macaddr.lower():
                result = -1
                RJPRINT("    BMC: %s" % RET[RETURN_KEY2].lower())
                RJPRINT("    Failed! BMC MAC address is not equal to CPU MAC address + 2")
            else:
                RJPRINT("    BMC: %s" % RET[RETURN_KEY2].lower())
    RJPRINT("")
    return result

# 系统信息获取依赖bcmcmdb的单独测试项（phypcie版本、SDK版本）
def test_sysinfo_part():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    errmsg = ""

    waitForSDK()

    if FACTESTMODULE.get("sdk_ver", 1) == 1:
        RJPRINT("%s"% "SDK Version:")
        sdk_version = get_sdk_version()
        if sdk_version is False:
            totalerr -= 1
            RJPRINT("    %s"% "fetch failed")
        else:
            sdk_version_check = TESTCASE.get('dev_info').get('sdk_version', None)
            if sdk_version_check is None:
                RJPRINT("    %s"% sdk_version)
            else:
                sdk_version_check = sdk_version_check.replace("\x00", "").strip()
                if sdk_version_check == sdk_version.replace("\x00", "").strip():
                    RJPRINT("    %s"% sdk_version)
                else:
                    totalerr -= 1
                    RJPRINT("    SDK version mismatch")
                    RJPRINT("    device version: %s" % sdk_version)
                    RJPRINT("    expected version: %s" % sdk_version_check)
        RJPRINT("")


    if FACTESTMODULE.get("mac_pcie", 1) == 1:
        RJPRINT("PCIE:")
        loader, version, build_date = get_phypcie_version()
        if loader is None or version is None:
            RJPRINT("Failed to get PCIE firmware version")
            totalerr += -1

        loader = loader.replace("\x00", "").strip()
        version = version.replace("\x00", "").strip()

        loader_check = TESTCASE.get('dev_info').get('PCIe FW loader version', None)
        if loader_check is not None:
            loader_check = loader_check.replace("\x00", "").strip()
            if loader_check == loader:
                RJPRINT("    PCIe FW loader version: %s" % loader_check)
            else:
                RJPRINT("    PCIe FW loader version detection failed, device version: %s, expected version: %s" %(loader, loader_check))
                totalerr += -1
        else:
            RJPRINT("    PCIe FW loader version: %s" % loader)

        version_check = TESTCASE.get('dev_info').get('PCIe FW version', None)
        if version_check is not None:
            version_check = version_check.replace("\x00", "").strip()
            if version_check == version:
                RJPRINT("    PCIe FW version: %s" % version_check)
            else:
                RJPRINT("    PCIe FW version detection failed, device version: %s, expected version: %s" %(version, version_check))
                totalerr += -1
        else:
             RJPRINT("    PCIe FW version: %s" % version)

        build_date_check = TESTCASE.get('dev_info').get('PCIe FW loader built date', None)
        if build_date_check is not None:
            build_date_check = build_date_check.replace("\x00", "").strip()
            build_date = build_date.replace("\x00", "").strip()
            if build_date_check == build_date:
                RJPRINT("    PCIe FW loader built date: %s" % build_date_check)
            else:
                RJPRINT("    PCIe FW loader built date detection failed, device version: %s, expected version: %s" %(build_date, build_date_check))
                totalerr += -1

    if FACTESTMODULE.get("81724firmware", 0) == 1:
        RJPRINT("%s "% "81724 Version")
        totalerr += show_81724_version()
    RJPRINT("")

    if totalerr <= 0:
        RET[RETURN_KEY1] += totalerr
        RET[RETURN_KEY2] += errmsg

    return RET



def get_onl_onie_version():
    onie_version_check = TESTCASE.get('dev_info').get('onie_version', None)

    ret, log = rj_os_system("show version |grep ONIE")
    if ret != 0 or len(log) == 0:
        error = "ONIE版本获取失败, ret:%s, log: %s " % (ret, log)
        return False, error

    onie_split_list = log.strip().split(":")
    if len(onie_split_list) != 2:
        error = "ONIE版本获取失败, log: %s " % (log)
        return False, error

    onie_version = onie_split_list[1].strip()
    if onie_version_check is not None:
        onie_version_check = onie_version_check.replace("\x00", "").strip()
        if onie_version != onie_version_check:
            log = "onie_version校验失败.设备版本:%s, 期望版本:%s" % (onie_version, onie_version_check)
            return False, log
    return True, "%s" % (onie_version)


def get_onl_version():
    onl_version_check = TESTCASE.get('dev_info').get('onl_version', None)

    ret, log = rj_os_system("show version |grep \"ONL version\"")
    if ret != 0 or len(log) == 0:
        error = "ONL版本获取失败, ret:%s, log: %s " % (ret, log)
        return False, error

    onl_split_list = log.strip().split(":")
    if len(onl_split_list) != 2:
        error = "ONL版本获取失败, log: %s " % (log)
        return False, error

    onl_version = onl_split_list[1].strip()
    if onl_version_check is not None:
        onl_version_check = onl_version_check.replace("\x00", "").strip()
        if onl_version != onl_version_check:
            log = "ONL版本校验失败.设备版本:%s, 期望版本:%s" % (onl_version, onl_version_check)
            return False, log
    return True, "%s" % (onl_version)


def test_sdr_list():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    cmd = "ipmitool sdr list"

    ret, log1 = log_os_system(cmd, 0)
    RJPRINT(log1)
    if ret != 0 or len(log1) <= 0:
        RET[RETURN_KEY2] = "命令执行出错[%s]" % cmd
        RET[RETURN_KEY1] = -1
    else:
        log1 = log1.splitlines()
        RET[RETURN_KEY2] = "检测错误的有："
        for line in log1:
            tmp = line.split("|")
            if tmp[2].strip() != "ok":
                RET[RETURN_KEY2] = RET[RETURN_KEY2] + " " + tmp[0].strip()
                RET[RETURN_KEY1] -= 1
        if RET[RETURN_KEY1] < 0:
            RJPRINT("")
            RJPRINT(RET[RETURN_KEY2] + "    FAILED")
            RJPRINT("")
    return RET

def get_onie_full_version():
    return_msg = ""
    onie_version_check = TESTCASE.get('dev_info').get('onie_version')
    onie_build_date_check = TESTCASE.get('dev_info').get('onie_build_date')
    onie_sub_version_check = TESTCASE.get('dev_info').get('onie_sub_version', None)

    machine_vars = get_config_file('/host/machine.conf')
    onie_version = machine_vars.get("onie_version", None).replace("\x00", "").strip()
    onie_build_date = machine_vars.get("onie_build_date", None).replace("\x00", "").strip()


    if onie_version is None or onie_build_date is None:
        log = "Failed to get onie_version: %s, onie_build_date: %s" % (onie_version, onie_build_date)
        log_debug(log)
        return False, log

    if onie_version_check is not None and onie_version != onie_version_check.replace("\x00", "").strip():
        log = "ONIE version detection failed, device version: %s, expected version: %s" % (onie_version, onie_version_check.replace("\x00", "").strip())
        log_debug(log)
        return False, log

    if onie_build_date_check is not None and onie_build_date != onie_build_date_check.replace("\x00", "").strip():
        log = "ONIE build date detection failed, device version: %s, expected version: %s" % (onie_build_date, onie_build_date_check.replace("\x00", "").strip())
        log_debug(log)
        return False, log

    return_msg = "onie_version: %s\n    onie_build_date:%s" % (onie_version, onie_build_date)

    onie_sub_version = ""
    if onie_sub_version_check is not None:
        onie_sub_version_check = onie_sub_version_check.replace("\x00", "").strip()
        onie_sub_version = machine_vars.get("onie_sub_version", None)
        onie_sub_version = onie_sub_version.replace("\x00", "").strip()
        if onie_sub_version != onie_sub_version_check:
            log = "ONIE sub version detection failed, device version: %s, expected version: %s" % (onie_sub_version, onie_sub_version_check)
            log_debug(log)
            return False, log
        return_msg += "\n    onie_sub_version: %s" % onie_sub_version
    return True, "%s" % return_msg

def get_bios_version():
    vendor_cmd = "dmidecode -t bios |grep Vendor |cut -d : -f 2"
    version_cmd = "dmidecode -t bios |grep Version |cut -d : -f 2"
    release_cmd = "dmidecode -t bios |grep Release | cut -d : -f 2"
    vendor_check = TESTCASE.get('dev_info').get('bios_vendor', None).replace("\x00", "").strip()
    version_check = TESTCASE.get('dev_info').get('bios_version', None).replace("\x00", "").strip()
    #release_check = TESTCASE.get('dev_info').get('bios_release_date', None).replace("\x00", "").strip()

    ret1, log1 = rj_os_system(vendor_cmd)
    if ret1 != 0:
        return False, "    vendor get failed"
    ret2, log2 = rj_os_system(version_cmd)
    if ret2 != 0:
        return False, "    version get failed"
    ret3, log3 = rj_os_system(release_cmd)
    if ret3 != 0:
        return False, "    release date get failed"

    #if vendor_check is None or version_check is None or release_check is None:
    if vendor_check is None or version_check is None :
        return False, "    bios check info get failed"

    log1 = log1.replace("\x00", "").strip()
    log2 = log2.replace("\x00", "").strip()
    log3 = log3.replace("\x00", "").strip()

    '''
    if log1 != vendor_check or log2 != version_check or log3 != release_check:
        log_debug("log1:%s, vendor_check:%s, log2:%s, version_check:%s, log3:%s, release_check:%s" %
            (log1, vendor_check, log2, version_check, log3, release_check))
        return False, "      设备的BIOS版本与配置文件不匹配,设备的BIOS版本：\n      %-21s： %s\n      %-21s： %s\n      %-21s： %s\n"% ("vendor", log1, "version", log2, "release_date", log3)
    '''

    if log1 != vendor_check or log2 != version_check:
        log_debug("log1:%s, vendor_check:%s, log2:%s, version_check:%s, log3:%s" %
            (log1, vendor_check, log2, version_check, log3))
        return False, "    BIOS version detection failed\n    Device version: \n        %-21s: %s\n        %-21s: %s\n    Desired version:\n        %-21s: %s\n        %-21s: %s\n"% ("vendor", log1, "version", log2, "vendor", vendor_check, "version", version_check)

    log = "    %-21s: %s\n    %-21s: %s\n" % ("vendor", vendor_check, "version", version_check)
    return True, log


def get_bfn_sde_version(cmd):
    ret, log = log_os_system(cmd, 0)
    if ret != 0 or len(log) == 0:
        RJPRINT("命令执行出错[%s]" % cmd)
        return None
    lines = log.splitlines()
    for line in lines:
        if "bf-syslibs:" in line:
            tmp = line.split(":", 1)
            return tmp[1].strip()
    RJPRINT(log)
    return None


def get_bfn_phypcie_version(cmd):
    ret, log = log_os_system(cmd, 0)
    if ret != 0 or len(log) == 0:
        RJPRINT("命令执行出错[%s]" % cmd)
        return None
    lines = log.splitlines()
    for line in lines:
        if "__device_select__misc_regs__spi_idcode" in line:
            tmp = line.strip().split(":")
            return tmp[1].strip()
    return None


# 系统信息获取依赖bfcmd的单独测试项（phypcie版本、SDE版本）
def test_bfn_sysinfo_part():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    errmsg = ""

    sde_ver_cmd = TESTCASE.get("BFN_SDE_VER", None)
    if sde_ver_cmd is not None:
        sde_ver = get_bfn_sde_version(sde_ver_cmd)
        if sde_ver is None:
            RJPRINT("SDE版本获取异常")
            totalerr -= 1
        else:
            sde_ver_check = TESTCASE.get('dev_info').get("sde_version")
            if sde_ver_check is None:
                RJPRINT("%-20s： %s"% ("SDE版本", sde_ver))
            else:
                sde_ver_check = sde_ver_check.strip()
                if sde_ver != sde_ver_check:
                    RJPRINT("SDE版本不匹配: 设备版本:%s, 期望版本:%s" %(sde_ver, sde_ver_check))
                    totalerr -= 1
                else:
                    RJPRINT("%-20s： %s"% ("SDE版本", sde_ver))
        RJPRINT("")

    pcie_ver_cmd = TESTCASE.get("BFN_PCIE_VER", None)
    if pcie_ver_cmd is not None:
        pcie_ver = get_bfn_phypcie_version(pcie_ver_cmd)
        if pcie_ver is None:
            RJPRINT("PCIE 固件版本获取异常")
            totalerr += -1
        else:
            pcie_fw_check = TESTCASE.get('dev_info').get("PCIe FW version")
            if pcie_fw_check is None:
                RJPRINT("%-20s： %s"% ("PCIE固件版本", pcie_ver))
            else:
                pcie_fw_check = pcie_fw_check.strip()
                if pcie_ver != pcie_fw_check:
                    RJPRINT("PCIE固件版本不匹配: 设备版本:%s, 期望版本:%s" %(pcie_ver, pcie_fw_check))
                    totalerr -= 1
                else:
                    RJPRINT("%-20s： %s"% ("PCIE固件版本", pcie_ver))
    RJPRINT("")

    if totalerr <= 0:
        RET[RETURN_KEY1] += totalerr
        RET[RETURN_KEY2] += errmsg
    return RET

# 系统信息获取
def test_onl_sysinfo():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    errmsg = ""
    totalerr = 0

    onie_version_check = TESTCASE.get("onie_version_check", 1)
    if onie_version_check == 1:
        RJPRINT("%s"% "ONIE版本")
        ret, onie_full_version = get_onl_onie_version()
        if ret is False:
            totalerr -= 1
            RJPRINT("      %s"% "获取失败")
            RJPRINT("              %s"% onie_full_version)
        else:
            RJPRINT("      %s"% onie_full_version)
        RJPRINT("")

    RJPRINT("%s"% "ONL版本")
    ret, onl_version = get_onl_version()
    if ret is False:
        totalerr -= 1
        RJPRINT("      %s"% onl_version)
    else:
        RJPRINT("      %s"% onl_version)
    RJPRINT("")

    RJPRINT("%s"% "BIOS版本:")
    ret, log = get_bios_version()
    if ret is False:
        totalerr -= 1
    RJPRINT("%s" % log)

    log_debug("正在获取软件版本信息")
    RJPRINT("%s "% "CPU")
    ret , biosmsg = get_cpu_message()
    if ret == True:
        #RJPRINT("      供应商       : %s" % (biosmsg["Manufacturer"]))
        RJPRINT("      版本         : %s" % (biosmsg["Version"]))
        RJPRINT("      Core Count   : %s" % (biosmsg["Core Count"]))
        RJPRINT("      Thread Count : %s" % (biosmsg["Thread Count"]))
    else:
        totalerr -= 1
    RJPRINT("")
    if FACTESTMODULE.get("show_device_mac", 0) == 1:
        totalerr += show_device_mac(True)

    RJPRINT("%s "% "I210版本")
    mgmt_version = get_mgmt_version(True)
    if mgmt_version is False:
        totalerr -= 1
    RJPRINT("")

    RJPRINT("%s "% "SATA")
    show_harddisk_info()

    RJPRINT("")
    log_debug("正在获内存信息")
    #print "%s "% "内存"
    RJPRINT("%s "% "内存条:")
    ret ,log  = getsysmeminfo_detail()
    if ret == True:
        for item in log:
            if(len(MEM_SLOTS) == len(log)):
                RJPRINT("      槽位【%s】/【%s】" % (item["Locator"], MEM_SLOTS[log.index(item)]))
            else:
                RJPRINT("      槽位【%s】" % (item["Locator"]))
            RJPRINT("         序列号: %s" % (item["Serial Number"]))
            RJPRINT("         容量  : %s" % (item["Size"]))
            RJPRINT("         速度  : %s" % (item["Speed"]))
    else:
        totalerr -= 1

    if FACTESTMODULE.get("sysinfo_showhw", 1) == 1:
        RJPRINT("")
        RJPRINT("%s "% "硬件系统")
        ret ,sysmsg = gethwsys()
        if ret == True:
            RJPRINT("      产品名称      : %s" % (sysmsg["Product Name"]))
            RJPRINT("      版本          : %s" % (sysmsg["Version"]))
            RJPRINT("      序列号        : %s" % (sysmsg["Serial Number"]))
            RJPRINT("      产商          : %s" % (sysmsg["Manufacturer"]))
            RJPRINT("      SKU           : %s" % (sysmsg["SKU Number"]))
            RJPRINT("      UUID          : %s" % (sysmsg["UUID"]))
            RJPRINT("      Family        : %s" % (sysmsg["Family"]))
            RJPRINT("      Wake-up Type  : %s" % (sysmsg["Wake-up Type"]))
        else:
            totalerr -= 1
    else:
        pass

    RJPRINT("")
    RJPRINT("%s "% "CPLD版本检测")
    ind, val  = get_cpld_version()
    for item in val:
        cpld_check = TESTCASE.get('dev_info').get('cpld_check', {})
        item[1] = item[1].replace("\x00", "").strip()
        item[2] = item[2].replace("\x00", "").strip()
        cpld_check[item[0]] = cpld_check[item[0]].replace("\x00", "").strip()
        if cpld_check[item[0]] == "%s%s" % (item[2],item[1]):
            RJPRINT("  %-20s： %s%s" %(item[0],item[2],item[1]))
        else:
            RJPRINT("  %-20s： CPLD版本不匹配. 设备版本:%s%s, 期望版本:%s" %(item[0], item[2], item[1], cpld_check[item[0]]))
            totalerr -= 1

    if FACTESTMODULE.get("fpga_show", 0) == 1:
        totalerr += show_fpga_version()

    if FACTESTMODULE.get("mul_fpga_show", 0) == 1:
        totalerr += show_mul_fpga_version()

    if FACTESTMODULE.get("devfileread_fpga_show", 0) == 1:
        totalerr += devfileread_fpga_version()

    #版本检测
    vals = TESTCASE.get("VERSIONTEST",None)
    if vals is not None :
        for item in vals:
            RJPRINT("")
            RJPRINT("%s " % (item.get('name')))
            ret,ind1 = rji2cgetWord(item.get('bus'), item.get('devno'), item.get('addr'))
            if ret == True:
                RJPRINT("  version            :  %s" % (ind1))
            else:
                totalerr -= 1

    #UCD90160版本检测
    vals = TESTCASE.get("UCD90160_VER",None)
    if vals is not None :
        for item in vals:
            chr_list = []
            chr_str = ""
            RJPRINT("")
            RJPRINT("%s " % (item.get('name')))
            cmd = item.get('cmd')
            ret, log = log_os_system(cmd, 0)
            if ret:
                RJPRINT("获取UCD90160版本失败")
                totalerr -= 1
            log = log.replace("\n", " ").strip()
            log = ' '.join(log.split())
            chr_list = log.split()
            for item in chr_list:
                if item.startswith("0x"):
                    continue
                chr_str += chr(int(item,16))
            RJPRINT("  version            :  %s" % (chr_str))

    if FACTESTMODULE.get("show_config_ver", 0) == 1:
        RJPRINT("")
        RJPRINT("配置文件版本号       :  %s" % TESTCASE.get("RUIJIE_CONFIG_VERSION"))

    bmc_version_check = TESTCASE.get('dev_info').get('bmc_version', None)
    if bmc_version_check is not None :
        RJPRINT("")
        RJPRINT("BMC版本：")
        #BMC检测
        bmc_version_check = bmc_version_check.replace("\x00", "").strip()
        ret, log = subprocess.getstatusoutput("ipmitool mc info |grep \"Firmware Revision\"|cut -d : -f 2")
        if ret:
            RJPRINT("        读取BMC版本失败")
            totalerr -= 1
        else:
            log = log.replace("\x00", "").strip()
            if bmc_version_check == log:
                RJPRINT("        %s" % bmc_version_check)
            else:
                RJPRINT("        读取到的BMC版本和配置文件不一致。设备版本:%s, 期望版本:%s" % (log, bmc_version_check))
                totalerr -= 1

    bcm5387_version_check = TESTCASE.get('dev_info').get('bcm5387_version', None)
    if bcm5387_version_check is not None :
        RJPRINT("")
        RJPRINT("CPU-BMC-SWITCH版本md5值：")
        #5387检测
        bcm5387_version_check = bcm5387_version_check.replace("\x00", "").strip()
        get_bcm5387_version_init_cmd = TESTCASE.get('get_bcm5387_version_init_cmd', [])
        for cmd in get_bcm5387_version_init_cmd:
            subprocess.getstatusoutput(cmd)
            time.sleep(0.1)
        get_bcm5387_version_cmd = TESTCASE.get('get_bcm5387_version_cmd', None)
        if get_bcm5387_version_cmd is None:
            ret, log = subprocess.getstatusoutput("platform_manufacturer.py |grep -A 3 \"CPU-BMC-SWITCH\"|grep \"Hardware Version\"|cut -d : -f 2")
            time.sleep(0.1)
        else:
            ret, log = subprocess.getstatusoutput(get_bcm5387_version_cmd)
            time.sleep(0.1)
        get_bcm5387_version_finish_cmd = TESTCASE.get('get_bcm5387_version_finish_cmd', [])
        for cmd in get_bcm5387_version_finish_cmd:
            subprocess.getstatusoutput(cmd)
            time.sleep(0.1)
        if ret:
            RJPRINT("        读取CPU-BMC-SWITCH版本失败")
            totalerr -= 1
        else:
            log = log.replace("\x00", "").strip()
            if bcm5387_version_check == log:
                RJPRINT("        %s" % bcm5387_version_check)
            else:
                RJPRINT("        CPU-BMC-SWITCH版本校验失败.设备版本:%s, 期望版本:%s" % (log, bcm5387_version_check))
                totalerr -= 1

    RJPRINT("")
    if totalerr <= 0:
        RET[RETURN_KEY1] += totalerr
        RET[RETURN_KEY2] += errmsg

    return RET


def ctc_command(cmd_list, exec_timeout=60):
    result_str=""
    cmd_iter = iter(cmd_list)
    child = pexpect.spawn("docker exec -it syncd ctc_shell")
    expect_words = "CTC_CLI\\(ctc-sdk\\)#"
    cmd_kill = "killall ctc_shell"
    try:
        while True:
            i = child.expect([pexpect.TIMEOUT,expect_words,pexpect.EOF],timeout=exec_timeout)
            if "CTC_CLI\#" not in expect_words:
                result_str += typeTostr(child.before)
            try:
                cmd = next(cmd_iter)
            except StopIteration:
                #延时1秒是为了保证第二个exit顺利退出，否则压力测试容易出现异常
                time.sleep(1)
                return True,result_str

            if i == 0: # Timeout
                return False, "执行命令超时,code:{}\n {}".format(i,typeTostr(child.before))
            if i == 1:
                if "exit" in cmd:
                    expect_words = "CTC_CLI\#"
                elif cmd == "inter":
                    expect_words = "\rCTC_CLI\\(ctc-internal\\)# \r\n\r\rCTC_CLI\\(ctc-internal\\)#"
                elif cmd == "dk":
                    expect_words = "\rCTC_CLI\\(ctc-dkits\\)# \r\n\r\rCTC_CLI\\(ctc-dkits\\)#"
                elif cmd == "sdk" or expect_words == "CTC_CLI\\(ctc-sdk\\)#":
                    expect_words = "\rCTC_CLI\\(ctc-sdk\\)# \r\n\r\rCTC_CLI\\(ctc-sdk\\)#"
                else:
                    expect_words = expect_words
                child.sendline( cmd + "\n")
                time.sleep(0.1)
            else:
                return False, "执行命令出错,code:{}\n {}".format(i,typeTostr(child.before))
    finally:
        child.close(force=True)
        ret, log = log_os_system(cmd_kill, 0)


# 系统信息获取依赖ctccmd的单独测试项(SDK版本)
def test_ctc_sysinfo_part():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    RJPRINT("SDK Information")
    sdk_cmd_list =  ["show version","exit","exit"]
    ret, log = ctc_command(sdk_cmd_list)

    if ret is False or len(log) == 0:
        RET[RETURN_KEY1] = -1
        RJPRINT("Failed to get SDK version")
    else:
        RJPRINT(log)
        #版本信息一致检查
        config_sdk_version = TESTCASE.get('dev_info').get('sdk_version')
        if config_sdk_version != None:
            check_sdk_version = re.findall("SDK\s*(\S+)\s*",log)[0]
            if len(check_sdk_version) > 0 and check_sdk_version.strip()==config_sdk_version.strip():
                RJPRINT("    SDK Version check: PASS")
            else:
                RJPRINT("    SDK Version check: FAILED, device version: %s, expected version: %s"%(check_sdk_version, config_sdk_version))
                RET[RETURN_KEY1] = -1

    return RET

def get_uboot_version():
    uboot_ver = "N/A"
    cmd = "sudo fw_printenv ver"
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    raw_data, err = p.communicate()
    raw_data = byteTostr(raw_data)
    err = byteTostr(err)
    if err == '' and raw_data != '':
        uboot_ver = re.findall("\w+\.\w+\.\w+\s+\(.*\)", raw_data)[0]
    return str(uboot_ver)

def get_current_uboot():
    """
        # Get booting uboot image of current running host OS
        # @return a string, "master" or "slave"
    """
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}

    uboot_conf = TESTCASE.get("UBOOT_STATUS")
    if uboot_conf is None:
        return False, "UBOOT_STATUS config not found"
    ret, value = get_value(uboot_conf)
    if ret is False or value is None:
        return False, "get uboot status failed, msg: %s" % value
    mask = uboot_conf.get("mask", 0xff)
    val = value & mask
    if val not in uboot_conf:
        return False, "unknow uboot status: %s" % value
    return True, uboot_conf[val]

def check_uboot_ver():
    totalerr = 0
    uboot_ver = get_uboot_version()
    status, uboot_status = get_current_uboot()
    if uboot_ver == "N/A":
        totalerr -= 1
        RJPRINT("    %s"% "Failed to get Uboot Version")
    if status is False:
        totalerr -= 1
        RJPRINT("    %s"% "Failed to get Uboot status")
    if totalerr < 0:
        return totalerr

    uboot_ver_check = TESTCASE.get('dev_info').get('uboot_version')
    if uboot_ver_check is not None and uboot_ver != uboot_ver_check:
        RJPRINT("    Uboot version detection failed, device version: %s, expected version: %s" % (uboot_ver, uboot_ver_check))
        return -1
    RJPRINT("    %s(%s)" % (uboot_ver, uboot_status))
    return 0

# ctc系统信息获取
def test_ctc_sysinfo():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    errmsg = ""
    totalerr = 0

    onie_version_check = TESTCASE.get("onie_version_check", 1)
    if onie_version_check == 1:
        log_debug("Obtaining ONIE Version")
        RJPRINT("%s"% "ONIE Version:")
        ret, onie_full_version = get_onie_full_version()
        if ret is False:
            totalerr -= 1
            RJPRINT("    %s"% onie_full_version)
        else:
            RJPRINT("    %s"% onie_full_version)
        RJPRINT("")

    log_debug("Obtaining SONiC Version")
    show_version_flag = TESTCASE.get("show_version", 1)
    if show_version_flag == 1:
        RJPRINT("%s"% "SONiC Version:")
        ret, log = show_version()
        if ret:
            totalerr -= 1
        RJPRINT("")
    else:
        RJPRINT("%s"% "SONiC Version:")
        ret = get_sonic_version()
        if ret is False:
            totalerr -= 1
        RJPRINT("")

    log_debug("Obtaining CPU information")
    RJPRINT("%s "% "CPU Information:")
    ret, log = show_cpu_info()
    if ret:
        totalerr -= 1
    RJPRINT("")

    if FACTESTMODULE.get("show_device_mac", 0) == 1:
        log_debug("Obtaining device mac")
        totalerr += show_device_mac()

    RJPRINT("")
    log_debug("Obtaining DDR information")
    RJPRINT("%s "% "DDR Information:")
    ret, log = show_ddr_info()
    if ret:
        totalerr -= 1

    RJPRINT("")
    RJPRINT("%s "% "CPLD Version")
    log_debug("Obtaining CPLD Version")
    ind, val  = get_cpld_version()
    for item in val:
        cpld_check = TESTCASE.get('dev_info').get('cpld_check', {})
        item[1] = item[1].replace("\x00", "").strip() # date
        item[2] = item[2].replace("\x00", "").strip() # version
        cpld_check[item[0]] = cpld_check[item[0]].replace("\x00", "").strip() # name
        if cpld_check[item[0]] == "%s%s" % (item[2],item[1]):
            RJPRINT("    %-20s: %s%s" %(item[0],item[2],item[1]))
        else:
            RJPRINT("    %-20s: CPLD version detection failed, device version: %s%s, expected version: %s" %(item[0], item[2], item[1], cpld_check[item[0]]))
            totalerr -= 1

    # 海外只能获取CPU端的uboot版本(fw_printenv获取)，无法获取BMC端的uboot版本
    # i2cget -f -y 2 0x0d 0x12读取CPLD(bit1: 0: 主uboot启动 1:备uboot启动)
    RJPRINT("")
    RJPRINT("%s "% "Uboot Version")
    ret = check_uboot_ver()
    if ret:
        totalerr -= 1
    RJPRINT("")

    # 8367
    # 待补充

    RJPRINT("")
    if totalerr < 0:
        RET[RETURN_KEY1] += totalerr
        RET[RETURN_KEY2] += errmsg


    return RET


# 系统信息获取
def test_sysinfo():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    errmsg = ""
    totalerr = 0

    onie_version_check = TESTCASE.get("onie_version_check", 1)
    if onie_version_check == 1:
        log_debug("Obtaining ONIE Version")
        RJPRINT("%s"% "ONIE Version:")
        ret, onie_full_version = get_onie_full_version()
        if ret is False:
            totalerr -= 1
            RJPRINT("    %s"% onie_full_version)
        else:
            RJPRINT("    %s"% onie_full_version)
        RJPRINT("")

    log_debug("Obtaining SONiC Version")
    show_version_flag = TESTCASE.get("show_version", 1)
    if show_version_flag == 1:
        RJPRINT("%s"% "SONiC Version:")
        ret, log = show_version()
        if ret:
            totalerr -= 1
        RJPRINT("")
    else:
        RJPRINT("%s"% "SONiC Version:")
        sonic_version = get_sonic_version()
        if sonic_version is False:
            totalerr -= 1
        RJPRINT("")

    log_debug("Obtaining BIOS Version")
    RJPRINT("%s"% "BIOS Version:")
    ret, log = get_bios_version()
    if ret is False:
        totalerr -= 1
    RJPRINT("%s" % log)

    RJPRINT("%s"% "Current BIOS flash")
    bios_info = get_bios_info()
    if bios_info is None:
        totalerr -= 1
        RJPRINT("      %s"% "Failed to get current BIOS flash")
    else:
        RJPRINT("      %s"% bios_info)
    RJPRINT("")


    log_debug("Obtaining CPU information")
    RJPRINT("%s "% "CPU Information:")
    ret , biosmsg = get_cpu_message()
    if ret == True:
        RJPRINT("    Model        : %s" % (biosmsg["Version"]))
        RJPRINT("    Core Count   : %s" % (biosmsg["Core Count"]))
        RJPRINT("    Thread Count : %s" % (biosmsg["Thread Count"]))
    else:
        totalerr -= 1
    RJPRINT("")
    if FACTESTMODULE.get("show_device_mac", 0) == 1:
        log_debug("Obtaining device mac")
        totalerr += show_device_mac()

    log_debug("Obtaining I210 Version")
    RJPRINT("%s "% "I210 Version:")
    mgmt_version = get_mgmt_version()
    if mgmt_version is False:
        totalerr -= 1
    RJPRINT("")

    log_debug("Obtaining SATA information")
    RJPRINT("%s "% "SATA")
    show_harddisk_info()

    RJPRINT("")
    log_debug("Obtaining DDR information")
    RJPRINT("%s "% "DDR:")
    ret ,log  = getsysmeminfo_detail()
    if ret == True:
        for item in log:
            if(MEM_SLOTS is not None and len(MEM_SLOTS) == len(log)):
                RJPRINT("  slot[%s]/[%s]" % (item["Locator"], MEM_SLOTS[log.index(item)]))
            else:
                RJPRINT("  slot[%s]" % (item["Locator"]))
            RJPRINT("    Serial Number: %s" % (item["Serial Number"]))
            RJPRINT("    Size         : %s" % (item["Size"]))
            RJPRINT("    Speed        : %s" % (item["Speed"]))
    else:
        totalerr -= 1

    if FACTESTMODULE.get("sysinfo_showhw", 1) == 1:
        RJPRINT("")
        RJPRINT("%s "% "Hardware system")
        log_debug("Obtaining hardware system information")
        ret ,sysmsg = gethwsys()
        if ret == True:
            RJPRINT("      Product Name  : %s" % (sysmsg["Product Name"]))
            RJPRINT("      Version       : %s" % (sysmsg["Version"]))
            RJPRINT("      Serial Number : %s" % (sysmsg["Serial Number"]))
            RJPRINT("      Manufacturer  : %s" % (sysmsg["Manufacturer"]))
            RJPRINT("      SKU Number    : %s" % (sysmsg["SKU Number"]))
            RJPRINT("      UUID          : %s" % (sysmsg["UUID"]))
            RJPRINT("      Family        : %s" % (sysmsg["Family"]))
            RJPRINT("      Wake-up Type  : %s" % (sysmsg["Wake-up Type"]))
        else:
            totalerr -= 1
    else:
        pass

    RJPRINT("")
    RJPRINT("%s "% "CPLD Version")
    log_debug("Obtaining CPLD Version")
    ind, val  = get_cpld_version()
    for item in val:
        cpld_check = TESTCASE.get('dev_info').get('cpld_check', {})
        if len(cpld_check) == 0:
            RJPRINT("skip CPLD version detection")
            break
        item[1] = item[1].replace("\x00", "").strip() # date
        item[2] = item[2].replace("\x00", "").strip() # version
        cpld_version_tmp = []
        if isinstance(cpld_check[item[0]], list):
            for cpld_version in cpld_check[item[0]]:
                cpld_version_tmp.append(cpld_version.replace("\x00", "").strip())
        else:
            cpld_version_tmp.append(cpld_check[item[0]].replace("\x00", "").strip())

        # cpld_check[item[0]] = cpld_check[item[0]].replace("\x00", "").strip() # name
        # if cpld_check[item[0]] == "%s%s" % (item[2],item[1]):
        if "%s%s" % (item[2],item[1]) in cpld_version_tmp:
            RJPRINT("    %-20s: %s%s" %(item[0],item[2],item[1]))
        else:
            RJPRINT("    %-20s: CPLD version detection failed, device version: %s%s, expected version: %s" %(item[0], item[2], item[1], cpld_version_tmp))
            totalerr -= 1

    if FACTESTMODULE.get("fpga_show", 0) == 1:
        totalerr += show_fpga_version()

    if FACTESTMODULE.get("mul_fpga_show", 0) == 1:
        totalerr += show_mul_fpga_version()

    if FACTESTMODULE.get("devfileread_fpga_show", 0) == 1:
        totalerr += devfileread_fpga_version()

    vals = TESTCASE.get("VERSIONTEST",None)
    if vals is not None :
        for item in vals:
            RJPRINT("")
            RJPRINT("%s " % (item.get('name')))
            ret,ind1 = rji2cgetWord(item.get('bus'), item.get('devno'), item.get('addr'))
            if ret == True:
                RJPRINT("    version          : %s" % (ind1))
            else:
                totalerr -= 1

    # UCD90160 version detection
    vals = TESTCASE.get("UCD90160_VER",None)
    if vals is not None :
        for item in vals:
            chr_list = []
            chr_str = ""
            RJPRINT("")
            RJPRINT("%s " % (item.get('name')))
            cmd = item.get('cmd')
            ret, log = log_os_system(cmd, 0)
            if ret:
                RJPRINT("Failed to get UCD90160 version")
                totalerr -= 1
            chr_list = log.split()
            for i in range(len(chr_list)):
                chr_str += chr(int(chr_list[i],16))
            RJPRINT("    version          : %s" % (chr_str))

    if FACTESTMODULE.get("show_config_ver", 0) == 1:
        RJPRINT("")
        RJPRINT("Inspection configuration file version:  %s" % TESTCASE.get("RUIJIE_CONFIG_VERSION"))

    bmc_version_check = TESTCASE.get('dev_info').get('bmc_version', None)
    if bmc_version_check is not None :
        RJPRINT("")
        RJPRINT("BMC Version:")
        # BMC
        bmc_version_check = bmc_version_check.replace("\x00", "").strip()
        ret, log = subprocess.getstatusoutput("ipmitool mc info |grep \"Firmware Revision\"|cut -d : -f 2")
        if ret:
            RJPRINT("    Failed to get BMC version")
            totalerr -= 1
        else:
            log = log.replace("\x00", "").strip()
            if bmc_version_check == log:
                RJPRINT("    %s" % bmc_version_check)
            else:
                RJPRINT("    BMC version detection failed, device version: %s, expected version: %s" % (log, bmc_version_check))
                totalerr -= 1

    bcm5387_version_check = TESTCASE.get('dev_info').get('bcm5387_version', None)
    if bcm5387_version_check is not None :
        RJPRINT("")
        RJPRINT("CPU-BMC-SWITCH md5sum: ")
        #5387检测
        bcm5387_version_check = bcm5387_version_check.replace("\x00", "").strip()
        get_bcm5387_version_init_cmd = TESTCASE.get('get_bcm5387_version_init_cmd', [])
        for cmd in get_bcm5387_version_init_cmd:
            subprocess.getstatusoutput(cmd)
            time.sleep(0.1)
        get_bcm5387_version_cmd = TESTCASE.get('get_bcm5387_version_cmd', None)
        if get_bcm5387_version_cmd is None:
            ret, log = subprocess.getstatusoutput("platform_manufacturer.py |grep -A 3 \"CPU-BMC-SWITCH\"|grep \"Hardware Version\"|cut -d : -f 2")
            time.sleep(0.1)
        else:
            ret, log = subprocess.getstatusoutput(get_bcm5387_version_cmd)
            time.sleep(0.1)
        get_bcm5387_version_finish_cmd = TESTCASE.get('get_bcm5387_version_finish_cmd', [])
        for cmd in get_bcm5387_version_finish_cmd:
            subprocess.getstatusoutput(cmd)
            time.sleep(0.1)
        if ret:
            RJPRINT("    Failed to get CPU-BMC-SWITCH version")
            totalerr -= 1
        else:
            log = log.replace("\x00", "").strip().replace(" ", "")
            if bcm5387_version_check == log:
                RJPRINT("    %s" % bcm5387_version_check)
            else:
                RJPRINT("    CPU-BMC-SWITCH version detection failed, device version: %s, expected version: %s" % (log, bcm5387_version_check))
                totalerr -= 1

    RJPRINT("")
    if totalerr < 0:
        RET[RETURN_KEY1] += totalerr
        RET[RETURN_KEY2] += errmsg

    return RET

def test_diag_sysinfo():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    errmsg = ""
    totalerr = 0

    RJPRINT("%s"% "ONIE版本")
    ret, onie_full_version = get_onie_full_version()
    if ret is False:
        totalerr -= 1
        RJPRINT("      %s"% "获取失败")
        RJPRINT("              %s"% onie_full_version)
    else:
        RJPRINT("      %s" % onie_full_version)
    RJPRINT("")

    RJPRINT("%s"% "SONiC版本")
    sonic_version = get_sonic_version()
    if sonic_version is False:
        totalerr -= 1
    RJPRINT("")

    '''
    RJPRINT("%s"% "SDK版本")
    sdk_version = get_sdk_version()
    if sdk_version is False:
        totalerr -= 1
        RJPRINT("      %s"% "获取失败")
    else:
        sdk_version_check = TESTCASE.get('dev_info').get('sdk_version', None)
        sdk_version_check = sdk_version_check.replace("\x00", "").strip()
        if sdk_version_check == sdk_version.replace("\x00", "").strip():
            RJPRINT("      %s"% sdk_version)
        else:
            totalerr -= 1
            RJPRINT("      SDK版本不匹配")
            RJPRINT("      设备版本:%s" % sdk_version)
            RJPRINT("      期望版本:%s" % sdk_version_check)
    RJPRINT("")
    '''

    RJPRINT("%s"% "BIOS版本:")
    ret, log = get_bios_version()
    if ret is False:
        totalerr -= 1
    RJPRINT("%s" % log)

    RJPRINT("%s"% "当前所在BIOS")
    bios_info = get_bios_info()
    if bios_info is None:
        totalerr -= 1
        RJPRINT("      %s"% "获取失败")
    else:
        RJPRINT("      %s"% bios_info)
    RJPRINT("")

    log_debug("正在获取软件版本信息")
    RJPRINT("%s "% "CPU")
    ret , biosmsg = get_cpu_message()
    if ret == True:
        #RJPRINT("      供应商       : %s" % (biosmsg["Manufacturer"]))
        RJPRINT("      版本         : %s" % (biosmsg["Version"]))
        RJPRINT("      Core Count   : %s" % (biosmsg["Core Count"]))
        RJPRINT("      Thread Count : %s" % (biosmsg["Thread Count"]))
    else:
        totalerr -= 1
    RJPRINT("")

    if FACTESTMODULE.get("mac_pcie", 1) == 1:
        RJPRINT("%s "% "PCIE")
        loader, version, build_date = get_phypcie_version()
        if loader is None or version is None:
            RJPRINT("PCIE 固件版本获取异常")
            totalerr += -1

        loader_check = TESTCASE.get('dev_info').get('PCIe FW loader version', None)
        loader_check = loader_check.replace("\x00", "").strip()
        version_check = TESTCASE.get('dev_info').get('PCIe FW version', None)
        version_check = version_check.replace("\x00", "").strip()
        build_date_check = TESTCASE.get('dev_info').get('PCIe FW loader built date', None)

        loader = loader.replace("\x00", "").strip()
        version = version.replace("\x00", "").strip()
        if loader_check == loader:
            RJPRINT("      PCIe FW loader version:%s" % loader_check)
        else:
            RJPRINT("      PCIe FW loader version不匹配: 设备版本:%s, 期望版本:%s" %(loader, loader_check))
            totalerr += -1
        if version_check == version:
            RJPRINT("      PCIe FW version:%s" % version_check)
        else:
            RJPRINT("      PCIe FW version不匹配: 设备版本:%s, 期望版本:%s" %(version, version_check))
            totalerr += -1

        if build_date_check is not None:
            build_date_check = build_date_check.replace("\x00", "").strip()
            build_date = build_date.replace("\x00", "").strip()
            if build_date_check == build_date:
                RJPRINT("      PCIe FW loader built date:%s" % build_date_check)
            else:
                RJPRINT("      PCIe FW loader built date不匹配: 设备版本:%s, 期望版本:%s" %(build_date, build_date_check))
                totalerr += -1

    RJPRINT("")

    if FACTESTMODULE.get("81724firmware", 0) == 1:
        RJPRINT("%s "% "81724版本")
        show_81724_version()
    RJPRINT("")

    RJPRINT("%s "% "I210版本")
    mgmt_version = get_mgmt_version()
    if mgmt_version is False:
        totalerr -= 1
    RJPRINT("")

    RJPRINT("%s "% "SATA")
    show_harddisk_info()

    RJPRINT("")
    log_debug("正在获内存信息")
    #print "%s "% "内存"
    RJPRINT("%s "% "内存条:")
    ret ,log  = getsysmeminfo_detail()
    if ret == True:
        for item in log:
            if(len(MEM_SLOTS) == len(log)):
                RJPRINT("      槽位【%s】/【%s】" % (item["Locator"], MEM_SLOTS[log.index(item)]))
            else:
                RJPRINT("      槽位【%s】" % (item["Locator"]))
            RJPRINT("         序列号: %s" % (item["Serial Number"]))
            RJPRINT("         容量  : %s" % (item["Size"]))
            RJPRINT("         速度  : %s" % (item["Speed"]))
    else:
        totalerr -= 1

    if FACTESTMODULE.get("sysinfo_showhw", 1) == 1:
        RJPRINT("")
        RJPRINT("%s "% "硬件系统")
        ret ,sysmsg = gethwsys()
        if ret == True:
            RJPRINT("      产品名称      : %s" % (sysmsg["Product Name"]))
            RJPRINT("      版本          : %s" % (sysmsg["Version"]))
            RJPRINT("      序列号        : %s" % (sysmsg["Serial Number"]))
            RJPRINT("      产商          : %s" % (sysmsg["Manufacturer"]))
            RJPRINT("      SKU           : %s" % (sysmsg["SKU Number"]))
            RJPRINT("      UUID          : %s" % (sysmsg["UUID"]))
            RJPRINT("      Family        : %s" % (sysmsg["Family"]))
            RJPRINT("      Wake-up Type  : %s" % (sysmsg["Wake-up Type"]))
        else:
            totalerr -= 1
    else:
        pass

    RJPRINT("")
    RJPRINT("%s "% "CPLD版本检测")
    ind, val  = get_cpld_version()
    for item in val:
        cpld_check = TESTCASE.get('dev_info').get('cpld_check', {})
        item[1] = item[1].replace("\x00", "").strip()
        item[2] = item[2].replace("\x00", "").strip()
        cpld_check[item[0]] = cpld_check[item[0]].replace("\x00", "").strip()
        if cpld_check[item[0]] == "%s%s" % (item[2],item[1]):
            RJPRINT("  %-20s： %s%s" %(item[0],item[2],item[1]))
        else:
            RJPRINT("  %-20s： CPLD版本不匹配. 设备版本:%s%s, 期望版本:%s" %(item[0], item[2], item[1], cpld_check[item[0]]))
            totalerr -= 1

    bmc_version_check = TESTCASE.get('dev_info').get('bmc_version', None)
    if bmc_version_check is not None :
        RJPRINT("")
        RJPRINT("BMC版本：")
        #BMC检测
        bmc_version_check = bmc_version_check.replace("\x00", "").strip()
        ret, log = subprocess.getstatusoutput("ipmitool mc info |grep \"Firmware Revision\"|cut -d : -f 2")
        if ret:
            RJPRINT("         读取BMC版本失败")
            totalerr -= 1
        else:
            log = log.replace("\x00", "").strip()
            if bmc_version_check == log:
                RJPRINT("         %s" % bmc_version_check)
            else:
                RJPRINT("         读取到的BMC版本和配置文件不一致。设备版本:%s, 期望版本:%s" % (log, bmc_version_check))
                totalerr -= 1

    bcm5387_version_check = TESTCASE.get('dev_info').get('bcm5387_version', None)
    if bcm5387_version_check is not None :
        RJPRINT("")
        RJPRINT("5387版本md5值：")
        #5387检测
        bcm5387_version_check = bcm5387_version_check.replace("\x00", "").strip()
        ret, log = subprocess.getstatusoutput("platform_manufacturer.py |grep -A 3 \"CPU-BMC-SWITCH\"|grep \"Hardware Version\"|cut -d : -f 2")
        if ret:
            RJPRINT("         读取5387版本失败")
            totalerr -= 1
        else:
            log = log.replace("\x00", "").strip()
            if bcm5387_version_check == log:
                RJPRINT("         %s" % bcm5387_version_check)
            else:
                RJPRINT("         读取到的5387版本和配置文件不一致。设备版本:%s, 期望版本:%s" % (log, bcm5387_version_check))
                totalerr -= 1

    RJPRINT("")
    if totalerr <= 0:
        RET[RETURN_KEY1] += totalerr
        RET[RETURN_KEY2] += errmsg

    return RET

def rtc_date_test():
    RET = ERROR_RETURN
    cmd = "hwclock | cut -d . -f 1"
    ret, log = rj_os_system(cmd)
    if ret:
        log_error("command:%s. run fail.log:%s" % (cmd, log))
        RET = {RETURN_KEY1: -1 , RETURN_KEY2 : "Error:RTC test failed"}
        return RET
    RJPRINT("RTC  time: %s" % log)
    time1 = time.mktime(time.strptime(log, '%Y-%m-%d %H:%M:%S'))
    my_log("time1 time stamp: %s" % time1)
    # 获取当前系统时间
    cmd_now = "date +'%Y-%m-%d %H:%M:%S'"
    ret, log = rj_os_system(cmd_now)
    if ret:
        log_error("command:%s. run fail.log:%s" % (cmd_now, log))
        RET = {RETURN_KEY1: -1 , RETURN_KEY2 : "Error:RTC test failed"}
        return RET
    RJPRINT("date time: %s" % log)
    time2 = time.mktime(time.strptime(log, '%Y-%m-%d %H:%M:%S'))
    my_log("time2 time stamp: %s" % time2)

    timeCompare = abs(time2 - time1)
    my_log("time difference:" + str(timeCompare))
    if timeCompare > RTC_THRESHOLD_LOWER:
        RJPRINT("begin RTC set date time\n")
        cmd = "hwclock -s"
        ret, log = rj_os_system(cmd)
        if ret:
            RET = {RETURN_KEY1: -1 , RETURN_KEY2 : "Error:RTC set date time failed"}
        else:
            RJPRINT("RTC reset date time OK,RTC test success\n")
            RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    else:
        RJPRINT("RTC test success")
        RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    return RET
# ====================================
# 测试项:RTC
# ====================================
def test_rtc():
    RET = ERROR_RETURN
    cmd = "hwclock | cut -d . -f 1"
    ret, log = rj_os_system(cmd)
    if ret:
        log_error("command:%s. run fail.log:%s" % (cmd, log))
        RET = {RETURN_KEY1: -1 , RETURN_KEY2 : "Error:RTC test failed"}
        return RET
    RJPRINT("Starting time: %s" % log)
    time1 = time.mktime(time.strptime(log, '%Y-%m-%d %H:%M:%S'))
    my_log("time1 time stamp: %s" % time1)

    time.sleep(RTC_WAIT_TIME)

    cmd = "hwclock | cut -d . -f 1"
    ret, log = rj_os_system(cmd)
    if ret:
        log_error("command:%s. run fail.log:%s" % (cmd, log))
        RET = {RETURN_KEY1: -1 , RETURN_KEY2 : "Error:RTC test failed"}
        return RET
    RJPRINT("Ending time  : %s" % log)
    time2 = time.mktime(time.strptime(log, '%Y-%m-%d %H:%M:%S'))
    my_log("time2 time stamp: %s" % time2)

    timeCompare =  time2 - time1
    my_log("time difference:" + str(timeCompare))
    if timeCompare < RTC_THRESHOLD_LOWER or timeCompare > RTC_THRESHOLD_UPPER:
        log_debug("RTC test failed")
        RET = {RETURN_KEY1: -1 , RETURN_KEY2 : "Error:RTCtest failed"}
    else:
        log_debug("RTC test success")
        RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    return RET

# ====================================
# 执行shell命令
# ====================================
def get_sys_execute(str):
    #function 1
    result = os.popen(str)
    res = result.read()
    for line in res.splitlines():
        RJPRINT(line)
    '''
    #function 2
    output = commands.getstatusoutput(str)
    print  output


    #function 3
    p = subprocess.Popen('ps aux',shell=True,stdout=subprocess.PIPE)
    out,err = p.communicate()
    for line in out.splitlines():
       print line
    '''
#mylog
def my_log(txt):
    if DEBUG == True:
        RJPRINT("[RUIJIE]:",)
        RJPRINT(txt)
    return
# ====================================
# 执行shell命令
# ====================================
def log_os_system(cmd, show):
    my_log ('         Run :'+ cmd)
    status, output = subprocess.getstatusoutput(cmd)
    my_log (" with result :" + str(status))
    my_log ("      output :" + output)
    if status:
        log_error('Failed :'+cmd)
        if show:
            RJPRINT('Failed :'+ cmd)
    return  status, output
# ====================================
# 拷机初始化
# ====================================
def kj_init():
    global KAOJILOGFILE
    time1 = time.time()
    timeArraystart = time.localtime(time1)
    otherStyleTime = time.strftime("%Y%m%d_%H%M", timeArraystart)
    KAOJILOGFILE = "/var/grtd/kjlog_%s.log" % otherStyleTime
    log_debug("创建的拷机日志:" + KAOJILOGFILE)
    file = open(KAOJILOGFILE,'w')
    file.close()

# ====================================
# 拷机结果保存
# ====================================
def KJERSULT(log):
    global KAOJILOGFILE
    strval = json.dumps(log, ensure_ascii = False,indent=4)
    with open(KAOJILOGFILE, 'w') as f:
        f.write(strval)

# ====================================
# 拷机错误数组中是否存在该测试项
# ====================================
def kj_isexit(name, result):
    for item in result:
        #log_debug(item)
        if name == item["name"]:
#            log_debug(name + " in result")
            return True
    return False

# ====================================
# 返回错误数组中存在的测试项信息
# ====================================
def kj_find_result(name , result):
    for item in result:
        if name == item["name"]:
#            log_debug(name + "exist")
            return item
    return None


# ====================================
# 拷机测试
# ====================================
def test_loop():
    global kj_result
    global KAOJISTATUS
    global ISKAOJI
    kj_result = []
    real_kj_result ={"starttime":"","endtime":"","result":[] ,"loop":0}
    KAOJISTATUS = 1
    kj_init()
    #创建拷机文件
    loop = 1
    isloopprint = True
    try:
        time1 = time.time();
        timeArraystart = time.localtime(time1)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArraystart)
        real_kj_result["starttime"] = otherStyleTime
        while True:
            ISKAOJI = 1
            time1 = time.time();
            timetemp_t = time.localtime(time1)
            casestarttime = time.strftime("%Y-%m-%d %H:%M:%S", timetemp_t)
            RJPRINT("\n==================> 生测第%d轮拷机测试开始 <===================" %loop)
            log_debug("==========生测第%d轮拷机测试开始(%s)============" % (loop, casestarttime))
            for item in looptest:
                kj_itemresult = {"name":"test", "loop":[], "error":[]}
                RJPRINT("\n\n %s" % item[MENUITEMNAME])
                RJPRINT("=" * 60)
                log_debug(" ")
                log_debug("==========%s 开始============" % item[MENUITEMNAME])
                RET = dealchoosefunc(item) #eval(item[MENUITEMDEAL])()
                #log_debug(RET)
                if RET[RETURN_KEY1] != 0:
                    RJPRINT("[%s]测试结果:" % item[MENUITEMNAME] + 'FAIL')
                    val_tmp = RET[RETURN_KEY2]
                    if kj_isexit(item[MENUITEMNAME], kj_result):
                        it = kj_find_result(item[MENUITEMNAME], kj_result)
                        #log_debug(it)
                        it["loop"].append(loop)
                        it["error"].append(val_tmp)
                    else:
                        kj_itemresult["name"] = item[MENUITEMNAME]
                        kj_itemresult["loop"].append(loop)
                        kj_itemresult["error"].append(val_tmp)
                        kj_result.append(kj_itemresult)
                else:
                    RJPRINT("[%s]测试结果:" % item[MENUITEMNAME] + 'PASS')
                log_debug("==========%s 结束============" % item[MENUITEMNAME])
            time2 = time.time();
            timeArrayend = time.localtime(time2)
            otherStyleTime1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArrayend)
            real_kj_result["endtime"] = otherStyleTime1
            real_kj_result["result"] = kj_result
            real_kj_result["loop"] = loop
            #写文件
            KJERSULT(real_kj_result)
            RJPRINT("\n==================> 生测第%d轮拷机测试结束 <===================\n" %loop)
            log_debug("==========生测第%d轮拷机测试结束(%s)============" % (loop,otherStyleTime1))
            loop += 1
            #isloopprint = True
            #time.sleep(5)
            if KAOJISTATUS == 0:
                break
        ISKAOJI = 0
    except Exception as e:
        RJPRINT(e)
        log_error(str(e))
    return {RETURN_KEY1 : 1,  RETURN_KEY2 : ""}

def file_name(file_dir):
    L=[]
    for dirpath, dirnames, filenames in os.walk(file_dir):
        for file in filenames :
            if file.startswith("kjlog"):
                L.append(os.path.join(dirpath, file))
    datas =sorted(L,reverse=True)
    return datas


def readKjLog(filename):
    str1 =""
    try:
        with open(filename, 'r') as f:
             str1 = f.read()
        if str1 == "":
            raise Exception("文件内容为空")
        val_t = eval(str1)
        ret = val_t["result"]
        RJPRINT("=====================================拷机结果=========================================================")
        RJPRINT("开始时间: %s  \r\n结束时间: %s  \r\n总轮数  :【%d】"% (val_t["starttime"], val_t["endtime"], val_t["loop"]))

        if len(ret) > 0:
            RJPRINT(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>失败测试项:")
        else:
            RJPRINT("本次拷机无失败测试项")
        for item in ret:
            RJPRINT("%s  【%s】 "% ("测试项:", item["name"]))
            loopstr = ""
            for loop in item["loop"]:
                loopstr += " %d " % loop
            RJPRINT("失败的轮数:   %s" % loopstr),
            for loop in item["loop"]:
                RJPRINT("第【%d】轮数错误:" % loop)
                index = item["loop"].index(loop)
                errmsg = item["error"][index]
                if isinstance(errmsg, list):
                    for test in errmsg:
                        RJPRINT("   %s :  " % test["name"])
                        for case_ret  in test["errmsg"]:
                            RJPRINT("           {name}   {error}".format(**case_ret) )
                elif isinstance(errmsg, str):
                    RJPRINT("{0} \n{1}".format(item["name"] , errmsg))
                RJPRINT("\n")
    except Exception as e:
        RJPRINTERR(str(e))

    RJPRINT("\n\n\n\n")
# ====================================
# 拷机日志数组选择
# ====================================
def printKJList():
    readtips = True
    L = file_name(KAOJILOGPATH)
    if len(L) <= 0:
        RJPRINT("\n\n没有拷机日志\n\n");
        return
    while(readtips):
        index = 0
        for x in L:
            RJPRINT("%d. %s"%(index, os.path.basename(x)))
            index += 1
            if (index >= kjlogmaxshow):
                break
        RJPRINT("q. %s"%("返回上一层"))
        test = "请选择:"
        str= getch(test)
        RJPRINT(" %s" % str)
        if str.isalnum() == False:
            RJPRINT("")
            continue
        #log_debug("选择:%s" % str)
        str = str.lstrip().lower()
        if str == "q":
            readtips = False
        elif (int(str) >= 0 and  int(str) <= index):
            readKjLog(L[int(str)])
        else:
            log_debug("异常输入项")

# ==================================================
# 拷机结果删除
# ==================================================
def test_loop_delete():
    L = file_name(KAOJILOGPATH)
    if len(L) <=0:
        RJPRINT("没有拷机记录")
        return {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    for file in L:
        os.remove(file)    #删除文件
    return {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}

# ====================================
# 拷机结果查看
# ====================================
def test_loop_read():
    printKJList();
    return {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}

def getRealUrl(case, param=None):
    ret, bmcip = getBMCIP()
    http = TESTCASE.get('BMC').get('requesthttp') % (bmcip)
    realurl = ""
    if param is None:
        realurl = "%scase=%s" %(http, case)
    else:
        realurl = "%scase=%s&param=%s"% (http, case, param)
    return realurl

def test_bmc_func(func,param=None):
    if param is None:
        ret = HttpRest().Get(getRealUrl(func))
    else:
        ret = HttpRest().Get(getRealUrl(func,json.dumps(param)))
    return ret

def test_bmc_testcase(param_t):
    ret = test_bmc_func(param_t)
    RJPRINT(ret.get(RETURN_KEY2))
    return ret

def uploadfile(filename):
    http = TESTCASE.get('BMC').get('uploadfilehttp')
    return HttpRest().uploadfile(http, filename)

def test_cpld_new():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    ermsg = ""
    #dealtype = E2_PROTECT.get('gettype',None)
    vals = TESTCASE["CPLDTEST"]
    #vals = "123"
    if type(vals) == list:
        for item in vals:
            try:
                dealtype = item.get('gettype',None)
                if dealtype is not None and dealtype == "io":
                    for wr_tmp in item.get('testval'):
                        io_wr(item.get('io_addr') + item.get('addr'), wr_tmp)
                        rets = io_rd(item.get('io_addr') + item.get('addr'))
                        val = int(rets, 16)
                        if item.get("invert", 0) == 1:
                            val = ~val & 0xff
                        if val ==  wr_tmp:
                            RJPRINT("%s\t\t0x%02x  %s" % (item.get('name'), wr_tmp, 'OK'))
                        else:
                            totalerr -= 1
                            ermsg = "%s %-30s  io_addr: 0x%0x addr:0x%02x  val:0x%02x rd:0x%02x \n" % (ermsg, item.get('name'),item.get('io_addr'), item.get('addr'),wr_tmp, val)
                else:
                    for wr_tmp1 in item.get('testval'):
                        rji2cset(item.get('bus'), item.get('devno'),item.get('addr'),wr_tmp1)
                        ret,ind = rji2cget(item.get('bus'), item.get('devno'),item.get('addr'))
                        val = int(ind, 16)
                        if item.get("invert", 0) == 1:
                            val = ~val & 0xff
                        if wr_tmp1 == val:
                            RJPRINT("%s\t\t0x%02x  %s" % (item.get('name'), wr_tmp1, 'OK'))
                        else:
                            totalerr -= 1
                            ermsg = "%s %-30s bus:%3d devno:0x%02x addr:0x%02x 0x%02x rd:0x%02x \n" % (ermsg, item.get('name'),item.get('bus'), item.get('devno'),item.get('addr'), wr_tmp1, val)
            except Exception as e:
                log_debug(str(e))
                ermsg = "%-30s        %s" % (item.get('name'), 'FAIL')
                totalerr -= 1
                continue
    else:
        totalerr -= 1
        ermsg  = 'Parameter error'
    if totalerr < 0:
        RJPRINTERR("\nerrmsg:")
        RJPRINTERR(ermsg)
    RET[RETURN_KEY1] = totalerr
    RET[RETURN_KEY2] = ermsg
    return RET

def test_fpga_new():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    ermsg = ""
    vals = TESTCASE["FPGATEST"]
    if type(vals) == list:
        for item in vals:
            try:
                dealtype = item.get('gettype',None)
                if dealtype is not None and dealtype == "devfile":
                 # record check val
                    check_val = item.get("value", None)
                    # write value
                    ret, log = set_value(item)
                    if ret == False:
                        ermsg = " fpga write value: %s failed \n" % (check_val)
                    # read value
                    ret, val = get_value(item)
                    if ret == False:
                        ermsg = " fpga read failed ,val: %s\n" % (val)
                    # compare write and read val
                    if val == check_val:
                        RJPRINT("%-18s  %s  %s" % (item.get('name'), check_val, 'PASS'))
                else:
                    for wr_tmp1 in item.get('value'):
                        rji2cset(item.get('bus'), item.get('devno'),item.get('addr'),wr_tmp1)
                        ret,ind = rji2cget(item.get('bus'), item.get('devno'),item.get('addr'))
                        if wr_tmp1 == int(ind, 16):
                            RJPRINT("%-30s  0x%02x  %s" % (item.get('name'), wr_tmp1, 'PASS'))
                        else:
                            totalerr -= 1
                            ermsg = "%s %-30s bus:%3d devno:0x%02x addr:0x%02x 0x%02x rd:%s \n" % (ermsg, item.get('name'),item.get('bus'), item.get('devno'),item.get('addr'), wr_tmp1, ind)
            except Exception as e:
                log_debug(str(e))
                ermsg = "%-30s        %s" % (item.get('name'), 'FAIL')
                totalerr -= 1
                continue
    else:
        totalerr -= 1
        ermsg  = 'Parameter error'
    if totalerr < 0:
        RJPRINTERR("\nerrmsg:")
        RJPRINTERR(ermsg)
    RET[RETURN_KEY1] = totalerr
    RET[RETURN_KEY2] = ermsg
    return RET

# ====================================
# 测试项:servcie服务测试
# ====================================
def test_service_status_check():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    ermsg = ""
    commands = TESTCASE["SERVICE_STATUS_CHECK"]
    for command in commands:
        cmd = command.get("cmd")
        sleep_time = command.get("sleep", 0)
        check_col = command.get("check_col", 1)
        check_str = command.get("check", "enable")
        ret, msg = rj_os_system(cmd)
        if sleep_time != 0:
            time.sleep(sleep_time)
        if ret != 0:
            log_debug("failed %s" % cmd)
            totalerr -= 1
            ermsg += ("failed %s" % cmd)
            continue
        msg_lines = msg.splitlines()
        for msg_line in msg_lines:
            msg_list = msg_line.split()
            service_name = msg_list[0]
            service_state = msg_list[check_col]
            if service_state == check_str:
                RJPRINT("%-40s  %-10s  %s" % (service_name, service_state, 'OK'))
            else:
                totalerr -= 1
                ermsg += ("failed %s state %s" %(service_name, service_state))
                RJPRINT("%-40s  %-10s  %s" % (service_name, service_state, 'Failed'))
    RET[RETURN_KEY1] = totalerr
    RET[RETURN_KEY2] = ermsg
    return RET

# ====================================
# cpld测试
# ====================================
def test_cpld():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    for cpld in TESTCASE["CPLD"]:
        RJPRINT("测试项: %s" % cpld["name"])
        if "cases" not in cpld:
            RJPRINT("没有测试项")
            continue
        for case in cpld["cases"]:
            RJPRINTLINE(case["name"])
            ###获取调用的命令
            cmd_t = case["cmd"].lstrip()
            cmd = cmd_t[0 : cmd_t.index(" ")]
            ret, log = log_os_system("which " + cmd, 0)
            if len(log):
                cmd = "cmd find "
            else:
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] = "no" + cmd +" found"
                return RET
            log_debug(case["cmd"])
            ret, log = log_os_system(case["cmd"], 0)
            log_debug(log)
            if ret or ("Error" in log ):
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] = log
                RJPRINT("[FAIL]")
            else:
                RJPRINT("[PASS]")
    return RET

def flip_reg_val_from_mid(reg_val):
    tmp_val = reg_val.replace("0x", "").replace("0X", "")
    len_val = len(tmp_val)
    mid = len_val / 2
    result = ''
    cache = ''
    for i, val in enumerate(tmp_val):
        if i < mid:
            cache += tmp_val[i]
        else:
            result += tmp_val[i]
    result += cache
    return result
def get_cur_val(monitor_chip):
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : []}
    resultval = []
    calu = monitor_chip.get("curcal",None)
    if calu is None:
        RET[RETURN_KEY2] = 'no current formula'
        return RET
    board_cur = monitor_chip.get('current',None)
    if board_cur is None:
        RET[RETURN_KEY2] = 'no current reg info'
        return RET
    chip_name = monitor_chip.get('cur_chip_name','')
    for slot in list(board_cur.keys()):
        slot_tmp = board_cur.get(slot)
        for i2c_para in slot_tmp:
            resistance = i2c_para.get("resistance")
            name = i2c_para.get("name")
            ret, curval = rji2cget(i2c_para["bus"], i2c_para["devno"], i2c_para["addr"], 16)
            if ret == False:
                RET[RETURN_KEY1] = -1000
                RET[RETURN_KEY2] += '%s fail' % name
                resultval.append([("%s_%s" % (slot, name)), 'read fail', ' ', ' ', 'Not OK'])
                continue
            curval = flip_reg_val_from_mid(curval)
            curval_int = int(curval,16)
            if i2c_para.get("abs", 0) == 1:
                curval_int = c_int16_to_abs(curval_int)
            result = calu % (curval_int, resistance)
            val_tmp = eval(result)
            if i2c_para['min'] <= val_tmp <= i2c_para['max']:
                resultval.append([("%s_%s" % (slot, name)), val_tmp, i2c_para['min'], i2c_para['max'], 'OK'])
            else:
                resultval.append([("%s_%s" % (slot, name)), val_tmp, i2c_para['min'], i2c_para['max'], 'Not OK'])
                RET[RETURN_KEY1] -= 1
    header = [ 'Sensor %s Current' % chip_name,  'Value', 'LowThd', 'HighThd' ,'State']
    result_fmt = tabulate(resultval, header, tablefmt='simple')
    RJPRINT(result_fmt)
    RJPRINT('\n')
    return RET
def get_vol_val(monitor_chip):
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : []}
    resultval = []
    calu = monitor_chip.get("volcal",None)
    if calu is None:
        RET[RETURN_KEY2] = 'no vol formula'
        return RET
    board_vol = monitor_chip.get('voltage',None)
    if board_vol is None:
        RET[RETURN_KEY2] = 'no vol reg info'
        return RET
    chip_name = monitor_chip.get('vol_chip_name','')
    for slot in list(board_vol.keys()):
        slot_tmp = board_vol.get(slot)
        for i2c_para in slot_tmp:
            name = i2c_para.get("name")
            ret, volval = rji2cget(i2c_para["bus"], i2c_para["devno"], i2c_para["addr"], 16)
            if ret == False:
                RET[RETURN_KEY1] = -1000
                RET[RETURN_KEY2] += '%s fail' % name
                resultval.append([("%s_%s"%(slot,name)), 'read fail', i2c_para['min'], i2c_para['max'], 'Not OK'])
                continue
            volval = flip_reg_val_from_mid(volval)
            result = calu % (volval)
            val_tmp = eval(result)
            if i2c_para['min'] <= val_tmp <= i2c_para['max']:
                resultval.append([("%s_%s"%(slot,name)), val_tmp, i2c_para['min'], i2c_para['max'], 'OK'])
            else:
                RET[RETURN_KEY2] = '%s vol out of range' % name
                resultval.append([("%s_%s"%(slot,name)), val_tmp, i2c_para['min'], i2c_para['max'], 'Not OK'])
                RET[RETURN_KEY1] -= 1
    header = [ 'Sensor %s Vol' % chip_name,  'Value', 'LowThd', 'HighThd' ,'State' ]
    result_fmt = tabulate(resultval, header, tablefmt='simple')
    RJPRINT(result_fmt)
    RJPRINT('\n')
    return RET
def get_power_chip_info(monitor_chip):
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : []}
    resultval = []
    power_info = monitor_chip.get('power_info',None)
    if power_info is None:
        RET[RETURN_KEY2] = 'no power_info config'
        return RET
    chip_name = monitor_chip.get('power_chip_name','')
    for slot_name, slot_infos in list(power_info.items()):
        for reg_info in slot_infos:
            name = reg_info['name']
            formula = reg_info['formula']
            rji2cset(reg_info["bus"], reg_info["devno"], reg_info["page_reg"], reg_info["page"])
            ret, tmp = rji2cget(reg_info["bus"], reg_info["devno"], reg_info["addr"], 16)
            if ret == False:
                RET[RETURN_KEY1] = -1000
                RET[RETURN_KEY2] += '%s fail' % name
                resultval.append([("%s_%s"%(slot_name,name)), 'read fail', reg_info["min"], reg_info["max"], 'Not OK'])
                continue
            result = formula % (tmp)
            val_tmp = eval(result)
            if reg_info['min'] <= val_tmp <= reg_info['max']:
                resultval.append([("%s_%s"%(slot_name,name)), val_tmp, reg_info["min"], reg_info["max"], 'OK'])
            else:
                resultval.append([("%s_%s"%(slot_name,name)), val_tmp, reg_info["min"], reg_info["max"], 'Not OK'])
                RET[RETURN_KEY1] -= 1
    header = [ 'Sensor %s' % chip_name,  'Value', 'LowThd', 'HighThd' ,'State' ]
    result_fmt = tabulate(resultval, header, tablefmt='simple')
    RJPRINT(result_fmt)
    RJPRINT('\n')
    return RET
def test_monitor_chip():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : []}
    monitor_chip = TESTCASE.get("monitor_chip",None)
    if monitor_chip is None:
        RET[RETURN_KEY2].append(' no support test')
        return RET
    ret = get_cur_val(monitor_chip)
    if ret[RETURN_KEY1]:
        RET[RETURN_KEY1] += -1001
        RET[RETURN_KEY2].append(' cur test:' + msg)
    ret = get_vol_val(monitor_chip)
    if ret[RETURN_KEY1]:
        RET[RETURN_KEY1] += -1002
        RET[RETURN_KEY2].append(' vol test:' + msg)
    ret = get_power_chip_info(monitor_chip)
    if ret[RETURN_KEY1]:
        RET[RETURN_KEY1] += -1003
        RET[RETURN_KEY2].append(' power test:' + msg)
    return RET

def test_voltage_getValue(item_r):
    gettype = item_r.get('gettype')
    len = item_r.get('len')
    address = item_r.get('io_addr')
    calcuvol = item_r.get('formula')
    min = item_r.get('minThread')
    max = item_r.get('maxThread')
    name = item_r.get('name')
    bus = item_r.get('bus')
    devno = item_r.get('devno')
    offset = item_r.get('addr')
    select = item_r.get('select')
    slectvalue = item_r.get('slectvalue')
    val = None
    if gettype == 'pagei2c':
        rji2cset(bus,devno, select, slectvalue)
        ret, ind = rji2cget(bus,devno, offset)
        if ret == False:
            val = None
        else:
            val =  ind.replace("0x","").replace("0X","")
    elif gettype == 'pagei2cword':
        rji2cset(bus,devno, select, slectvalue)
        ret, ind = rji2cgetWord(bus,devno, offset)
        if ret == False:
            val = None
        else:
            val =  ind.replace("0x","").replace("0X","")
    elif gettype == 'io':
        val = io_rd(address, len)
        val = "%0x" %(int(val, 16) >> 4)
    elif gettype == 'i2c':
        i2ctmp = ''
        for i in range(0,len):
            ret, ind = rji2cget(bus,devno, offset+i)
            if ret == False:
                i2ctmp = None
                break
            i2ctmp += ind.replace("0x","").replace("0X","")
        if i2ctmp == None:
            val = None
        else:
            val = "%0x" %(int(i2ctmp, 16) >> 4)
    return val


def test_voltage():
    RET =  {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    errmsg =""
    resultval = []

    voldef = TESTCASE.get("voltagesensors",None)
    if voldef is None:
        RET[RETURN_KEY1] = -999
        RET[RETURN_KEY2] = 'config error'
        return RET

    #找出参考值
    calu = voldef.get("voltagecal",None)
    if calu is None:
        RET[RETURN_KEY1] = -997
        RET[RETURN_KEY2] = 'config error'
        return RET

    boardtemps = voldef.get('voltages',None)
    if boardtemps is None:
        RET[RETURN_KEY1] = -998
        RET[RETURN_KEY2] = 'config error'
        return RET
    try:
        for key in list(boardtemps.keys()):
            voltage_tmp = boardtemps.get(key)
            reference = None
            referenceitem = None

            for item in voltage_tmp:
                if item.get('reference',0)==1:
                    referenceitem = item
            if referenceitem is None:
                totalerr -= 1
                errmsg += "%s not find config\n" % key
                RJPRINT(errmsg)
                continue

            val = test_voltage_getValue(referenceitem)
            if val is None:
                totalerr -= 1
                errmsg += "%s read reference error\n" % key
                RJPRINT(errmsg)
                continue
            result = calu % val
            reference = eval(result)


            if type(val) == str:
                log_debug(" %s reference name:%s val type:0x%s  val:%f"% (key, referenceitem.get('name'),val, reference))
            if reference is None:
                totalerr -= 1
                errmsg += "%s reference cal error\n" % key
            else:
                for item_r in voltage_tmp:
                    val_calc = test_voltage_getValue(item_r)
                    gettype = item_r.get('gettype')
                    calcuvol = item_r.get('formula')
                    min = item_r.get('minThread')
                    max = item_r.get('maxThread')
                    name = item_r.get('name')
                    statusmsg = 'N/A'

                    if val_calc is None:
                        totalerr -= 1
                        resultval.append([("%s_%s"%(key,name)),'N/A' , min, max, statusmsg])
                        continue
                    if gettype == 'pagei2c':
                        pagei2c_tmp = calcuvol %(val_calc, val_calc)
                        val_tmp = eval(pagei2c_tmp)
                    if gettype == 'pagei2cword':
                        pagei2c_tmp = calcuvol %(val_calc)
                        val_tmp = eval(pagei2c_tmp)
                    elif gettype == 'io' or gettype == 'i2c':
                        result_curr_tmp = calu % val_calc
                        result_curr = eval(result_curr_tmp)
                        result = calcuvol % (result_curr, reference)
                        val_tmp = eval(result)
                    if min < val_tmp <max:
                        statusmsg = 'OK'
                    else:
                        totalerr -= 1
                        statusmsg = 'Not OK'
                    log_debug("%s_%s val:%f  threadsold[%f, %f]"%(key, name, val_tmp,min, max))
                    resultval.append([("%s_%s"%(key,name)),val_tmp , min, max, statusmsg])
    except Exception as e:
        totalerr = -1001
        import traceback
        msg = traceback.format_exc() # 方式1
        print (msg)

    header = [ 'Sensor',  'Value', 'LowThd', 'HighThd' ,'State' ]
    result = tabulate(resultval, header, tablefmt='simple')
    RJPRINT(result)
    if totalerr < 0:
        errmsg += str(result)

    RET[RETURN_KEY1] = totalerr
    RET[RETURN_KEY2] = errmsg
    return RET

def test_phy_recover():
    RET =  {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    ret, log = rj_os_system("docker exec -it syncd cat /tmp/repair")
    if ret != 0 or len(log) <= 0 :
        return RET
    RJPRINT("")
    RJPRINT("槽位         端口      修复温度")
    RJPRINT("-------    -------  -----------")
    logic_ports = PortTest().logic_ports
    alias = TESTCASE.get('port_alias', None)
    logs = log.splitlines()
    for line in logs:
        if "temperature" in line:
            ret = re.findall(r'port_start:\[(\d+)\]', line)
            port_num1 = re.findall(r'/(\d+)', alias.get(logic_ports.index((int)(ret[0]))+1,None))
            ret = re.findall(r'port_end:\[(\d+)\]', line)
            port_num2 = re.findall(r'/(\d+)', alias.get(logic_ports.index((int)(ret[0]))+1,None))
            lost_num = re.findall(r'\d+', alias.get(logic_ports.index((int)(ret[0]))+1,None))
            temp_num = ((float)(re.findall(r'temperature:\[(.*?)\]', line)[0]))/1000.0
            port_msg = "%s-%s"%(port_num1[0], port_num2[0])
            keep_message(RET, ("SLOT%-6s%8s%13.1f" % (lost_num[0],port_msg, temp_num )))
    RJPRINT(RET[RETURN_KEY2])
    return RET

def test_bfn_mac_temp():
    RET =  {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    max_temp = -50
    total_temp = 0
    count = 0

    temp_def = TESTCASE.get("temps",None)
    if temp_def is None:
        RET[RETURN_KEY1] = -999
        RET[RETURN_KEY2] = 'config error'
        RJPRINT(RET[RETURN_KEY2])
        return RET
    mactemps = temp_def.get('bfn_mac_temp',None)
    if mactemps is None:
        RET[RETURN_KEY1] = -998
        RET[RETURN_KEY2] = 'config error'
        RJPRINT(RET[RETURN_KEY2])
        return RET

    ret, log = log_os_system(mactemps, 0)
    if ret != 0 or len(log) == 0:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "命令执行出错[%s]" % mactemps
        RJPRINT(RET[RETURN_KEY2])
        return RET

    lines = log.splitlines()
    for line in lines:
        if "TEMP" in line:
            count += 1
            tmp = line.strip().split()
            name = tmp[1]
            cur_temp = int(tmp[4])
            total_temp += cur_temp
            if cur_temp > max_temp:
                max_temp = cur_temp
            RJPRINT("  %-15s : %0.2f C" % (name, cur_temp))
    RJPRINT("  %-15s : %0.2f C" % ("最高温度", max_temp))
    RJPRINT("  %-15s : %0.2f C" % ("平均温度", (total_temp / count)))
    return RET

def test_mac_temp():
    RET =  {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    errmsg = ""
    temp_def = TESTCASE.get("temps",None)
    RJPRINT("%s "% "MAC温度")
    if temp_def is None:
        RET[RETURN_KEY1] = -999
        RET[RETURN_KEY2] = 'config error'
        return RET

    mactemps = temp_def.get('mac_temp',None)
    if mactemps is not None:
        for item in mactemps:
            retval = ""
            rval = None
            name = item.get('displayname')
            location = item.get('location')
            try:
                locations = glob.glob(location)
                with open(locations[0], 'r') as fd1:
                    retval = fd1.read()
                rval = float(retval)/1000
                if rval >= 0:
                    formatlenstr = "  %%-%ds: %%.2f %%s" % (11+wide_chars(name))
                    RJPRINT(formatlenstr %(name, rval, 'C'))
                else:
                    RJPRINT("  %s: 读出温度为负值，温度异常" %(name))
                    totalerr -= 1
            except Exception as e:
                totalerr -= 1
                errmsg = " %s %s" % (errmsg, str(e))
                formatlenstr2 = "  %%-%ds: %%s" % (11+wide_chars(name))
                RJPRINT(formatlenstr2 %(name, 'NA'))

    ret, aver_temp = SdkCmdCase.show_aver_mac_temp()
    if ret is False:
        totalerr -= 1
        errmsg += "[获取MAC平均温度出错]"
        RJPRINT("平均温度[FAILED]")
    else:
        if aver_temp >= 0:
            RJPRINT("  %s : %0.2f %s" % ("平均温度  ", aver_temp, "C"))
        else:
            RJPRINT("  平均温度 : 读出平均温度为负值，温度异常")
            totalerr -= 1

    ret, max_temp = SdkCmdCase.show_max_mac_temp()
    if ret is False:
        totalerr -= 1
        errmsg += "[获取MAC最高温度出错]"
        RJPRINT("最高温度 [FAILED]")
    else:
        if aver_temp >= 0:
            RJPRINT("  %s : %0.2f %s" % ("最高温度  ", max_temp, "C"))
            if max_temp > 95:
                totalerr -= 1
                errmsg += "[获取MAC最高温度超过95度]"
                RJPRINT("")
                RJPRINT("最高温度超过95度 [FAILED]")
        else:
            RJPRINT("  最高温度 : 读出最高温度为负值，温度异常")
            totalerr -= 1
    RET[RETURN_KEY1] = totalerr
    RET[RETURN_KEY2] = errmsg
    return RET

def test_tempinfo_new():
    '''温度检测 19/05/10'''
    RET =  {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    errmsg = ""
    resultval = []

    temp_def = TESTCASE.get("temps",None)
    if temp_def is None:
        RET[RETURN_KEY1] = -999
        RET[RETURN_KEY2] = 'config error'
        return RET

    boardtemps = temp_def.get('boards',None)
    if boardtemps is None:
        RET[RETURN_KEY1] = -998
        RET[RETURN_KEY2] = 'config error'
        return RET

    for item in boardtemps:
        retval = ""
        rval = None
        name = item.get('displayname')
        location = item.get('location')
        min = item.get("min", 0)
        max = item.get("max", 70)
        try:
            locations = glob.glob(location)
            with open(locations[0], 'r') as fd1:
                retval = fd1.read()
            rval = float(retval)/1000
            if min < rval < max:
                statusmsg = 'OK'
            else:
                RJPRINT("  %s: The temperature is out of range, abnormal" % name)
                totalerr -= 1
                statusmsg = 'Not OK'
        except Exception as e:
            totalerr -= 1
            errmsg = " %s %s" % (errmsg, str(e))
            formatlenstr2 = "  %%-%ds: %%s" % (25+wide_chars(name))
            RJPRINT(formatlenstr2 %(name, 'NA'))
        resultval.append([name, "%s %s"%(rval, 'C'), "%s %s"%(min, 'C'), "%s %s"%(max, 'C'), statusmsg])
    header = ['Board temperature', 'Value', 'LowTemp', 'HighTemp', 'State']
    result = tabulate(resultval, header, tablefmt='simple')
    RJPRINT(result)
    RJPRINT("")
    location = temp_def.get('cpu',None)
    L=[]
    cpuval = []
    for dirpath, dirnames, filenames in os.walk(location):
        for file in filenames :
            if file.endswith("input"):
                L.append(os.path.join(dirpath, file))
        L =sorted(L,reverse=False)

    for i in range(len(L)):
        nameloc = "%s/temp%d_label"%(location,i+1)
        valloc  = "%s/temp%d_input"%(location,i+1)
        min = temp_def.get('cpu_temp_min',10)
        max = temp_def.get('cpu_temp_max',100)
        #print nameloc
        with open(nameloc, 'r') as fd1:
            retval2 = fd1.read()
        with open(valloc, 'r') as fd2:
            retval3 = fd2.read()
            rval = float(retval3)/1000
            if min < rval < max:
                statusmsg = 'OK'
            else:
                RJPRINT("  %s: The temperature is out of range, abnormal" % retval2.strip())
                totalerr -= 1
                statusmsg = 'NOT OK'
        cpuval.append([retval2.strip(), "%s %s"%(rval, 'C'), "%s %s"%(min, 'C'), "%s %s"%(max, 'C'), statusmsg])
    header = ['CPU temperature', 'Value', 'LowTemp', 'HighTemp', 'State']
    result = tabulate(cpuval, header, tablefmt='simple')
    RJPRINT(result)

    mactemps = temp_def.get('mac', None)
    macval = []
    if mactemps is not None:
        RJPRINT("")
        for item in mactemps:
            retval = ""
            rval = None
            name = item.get('displayname')
            location = item.get('location')
            min = temp_def.get('mac_temp_min',10)
            max = temp_def.get('mac_temp_max',100)
            try:
                locations = glob.glob(location)
                with open(locations[0], 'r') as fd1:
                    retval = fd1.read()
                rval = float(retval)/1000
                if min < rval < max:
                    statusmsg = 'OK'
                else:
                    statusmsg = 'NOT OK'
                    RJPRINT("  %s: The temperature is out of range, it's abnormal" % name)
                    totalerr -= 1
            except Exception as e:
                totalerr -= 1
                errmsg = " %s %s" % (errmsg, str(e))
                formatlenstr2 = "  %%-%ds: %%s" % (25+wide_chars(name))
                RJPRINT(formatlenstr2 %(name, 'NA'))
            macval.append([name, "%s %s"%(rval, 'C'), "%s %s"%(min, 'C'), "%s %s"%(max, 'C'), statusmsg])
        header = ['MAC temperature', 'Value', 'LowTemp', 'HighTemp', 'State']
        result = tabulate(macval, header, tablefmt='simple')
        RJPRINT(result)


    RET[RETURN_KEY1] = totalerr
    RET[RETURN_KEY2] = errmsg
    return RET

# ====================================
# 电源状态检测
# ====================================
def test_power():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    RET1 = sysinfo_show_psumsg()
    RET[RETURN_KEY1] += RET1[RETURN_KEY1]
    RET[RETURN_KEY2] += RET1[RETURN_KEY2]
    return RET


def test_i2c_stress():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    totalerr = 0
    test_times = 10
    for i in range(0, test_times):
       print("\n\n第 %d/%d 次测试"%(i+1, test_times))
       RET1 = test_i2c_new()
       #print_temp_flush()
       totalerr += RET1[RETURN_KEY1]
       RET[RETURN_KEY2] += RET1[RETURN_KEY2]
    if totalerr < 0:
       RET[RETURN_KEY1] = -1
    return RET

def i2cget_python(bus, devno, address):
    ret_t = ""
    ret, ret_t = osutil.rji2cget_python(bus, devno, address)
    if ret:
        return True, ret_t
    return False, ret_t

def test_i2c_stress_new():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    errtotal = 0
    test_times = TESTCASE.get("i2c_test_times", 100)
    keep_str = ""
    scan_list = TESTCASE["I2CSCAN"]
    errmsg = ""
    for i2cdev in scan_list:
        tmp_count = 0
        err_flag = False
        for i in range(0, test_times + 1):
            formatstr = "    %%-%ds %%-10s\n" % ((40 + wide_chars(i2cdev['name'])))
            type = i2cdev.get("gettype", None)
            if i == 0:
                keep_str += formatstr % (i2cdev['name'], "PASS")
                continue
            if type == "I2C_32":
                ret, log = rji2cget_32bit(i2cdev["bus"], i2cdev["addr"], "0x00")
            else:
                ret, log = i2cget_python(i2cdev["bus"], i2cdev["addr"], 0)
            if ret == False:
                tmp = formatstr % (i2cdev['name'], "PASS")
                replace_str = formatstr % (i2cdev['name'], "FAILED")
                keep_str = keep_str.replace(tmp, replace_str)
                errmsg = "%s %s\n" % (errmsg, i2cdev['name'])
                err_flag = True
            if err_flag:
                tmp_count += 1
        if errtotal < tmp_count:
            errtotal = tmp_count
    RJPRINT(keep_str)
    RJPRINT("\n\nI2C %d次压力测试" % test_times)
    RJPRINT("PASS TIMES：%d" % (test_times - errtotal))
    RJPRINT("FAILED TIMES：%d" % errtotal)
    if errtotal != 0:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = errmsg
    return RET

def test_get_psu_fru():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    errmsg = ""
    psus =  FRULISTS.get('psus')
    for psu in psus:
        try:
            RJPRINT("===============%s ================getmessage" % psu.get('name'))
            eeprom = I2CUTIL.dumpValueByI2c(psu.get('bus'), psu.get('loc'))
            if eeprom is None:
                raise Exception("%s:wrong value" % psu.get('name'))
            fru = ipmifru()
            fru.decodeBin(eeprom)

            if fru.boardInfoArea is not None:
                RJPRINT("=================board=================")
                RJPRINT(fru.boardInfoArea)
            if fru.productInfoArea is not None:
                RJPRINT("=================product=================")
                # 进行可能存在的电源型号映射
                psuModleName_Dict = TESTCASE.get('psu_model_map', None)
                if psuModleName_Dict is not None:
                    for psu_name in list(psuModleName_Dict.keys()):
                        if psu_name in fru.productInfoArea.productPartModelName:
                            fru.productInfoArea.productName = psuModleName_Dict[psu_name]
                            psu_match = True
                            break
                RJPRINT(fru.productInfoArea)
        except Exception as e:
            RJPRINT(str(e))
            totalerr -=1
            errmsg = " %s %s %s \n" %(errmsg, psu.get('name'), str(e))

    RET[RETURN_KEY1] = totalerr
    RET[RETURN_KEY2] = errmsg
    return  RET

def fan_check1(fans, levelpolicy, errt_t):
    try:
        stopFanctrol()
        ret_t = 0
        for level in levelpolicy["level"]:
            testerror = {}
            ind = levelpolicy["level"].index(level)
            lowspeed = levelpolicy["low_speed"][ind]
            highspeed = levelpolicy["high_speed"][ind]
            strtmp = "风扇转速等级: 【%s】 写入cpld值:0x%02x  阈值: [%d , %d]"% (levelpolicy["tips"][ind], level,lowspeed,highspeed)
            RJPRINT(strtmp)
            log_debug(strtmp)
            for item in fans:
                loc = item.get('location')
                write_sysfs_value(loc, "0x%02x"% level )
                ret_val = get_sysfs_value(loc)
                log_debug("写入的值为%s" % ret_val)
            time.sleep(13)
            caseerror = []
            for item_fan in fans:
                testind = 0
                RJPRINT(item_fan.get('name'))
                for fanstatus in item_fan["childfans"]:
                    nowspeed = test_fan_speed_average(fanstatus["location"])
                    if nowspeed != -1:
                        log_debug("%s (now: %d low:%d high:%d)"% (fanstatus["name"], nowspeed ,lowspeed,highspeed))
                        speedmsg = "(%d)"% ( nowspeed)
                        if lowspeed < nowspeed and highspeed > nowspeed:
                            RJPRINT("    %s %s : %s"%(fanstatus["name"],speedmsg, "[PASS]"))
                        else:
                            RJPRINT("    %s %s : %s"%(fanstatus["name"],speedmsg, "[FAILED]"))
                            caseerror.append({"name": ("%s %s" %(item_fan.get('name'),fanstatus["name"])) ,"error":"不在转速范围内 [nowspeed: %d low_speed:%d high:%d]" % ( nowspeed ,lowspeed,highspeed)})
                            ret_t -= 1
                            testind -= 1
                    else:
                        RJPRINT("    %s : %s"%(fanstatus["name"], "[FAILED]"))
                        caseerror.append({"name": ("%s %s" %(item_fan.get('name'),fanstatus["name"])) ,"error":"获取转速为空"})
                        ret_t -= 1
                        testind -= 1
                if len(caseerror) > 0:
                    testerror["name"] = "转速等级:[%s]0x%02x "% (levelpolicy["tips"][ind], level)
                    testerror['errmsg'] = caseerror
            if testind < 0:
                errt_t.append(testerror)
    except Exception as e:
        print(e)
        log_error(e.message)
        return False
    finally:
        startFanctrol()
    if ret_t < 0:
        return ret_t
    return ret_t

def write_sysfs_value(reg_name, value):
    retval = 'ERR'
    fileLoc = MAILBOX_DIR + reg_name
    try:
        if not os.path.isfile(fileLoc):
            print(fileLoc,  'not found !')
            return False
        with open(fileLoc, 'w') as fd:
            fd.write(value)
    except Exception as error:
        log_error("Unable to open " + fileLoc + "file !")
        return False
    return True


def get_config_file(filename):
    if not os.path.isfile(filename):
        return ""
    machine_vars = {}
    with open(filename) as machine_file:
        for line in machine_file:
            tokens = line.split('=')
            if len(tokens) < 2:
                continue
            machine_vars[tokens[0]] = tokens[1].strip()
    return machine_vars

def getonieversion():
    if not os.path.isfile('/host/machine.conf'):
        return ""
    machine_vars = {}
    with open('/host/machine.conf') as machine_file:
        for line in machine_file:
            tokens = line.split('=')
            if len(tokens) < 2:
                continue
            machine_vars[tokens[0]] = tokens[1].strip()
    return machine_vars.get("onie_version")


def fac_board_setmac():
    _value = {}

    try:
        onie = onie_tlv()
        # 默认赋值
        _value[onie.TLV_CODE_VENDOR_EXT] = generate_ext(RUIJIE_CARDID)  # 生成锐捷特有的id
        _value[onie.TLV_CODE_PRODUCT_NAME] = RUIJIE_PRODUCTNAME
        _value[onie.TLV_CODE_PART_NUMBER]    = RUIJIE_PART_NUMBER
        _value[onie.TLV_CODE_LABEL_REVISION] = RUIJIE_LABEL_REVISION
        _value[onie.TLV_CODE_PLATFORM_NAME]  = platform
        _value[onie.TLV_CODE_ONIE_VERSION]   = getonieversion()
        _value[onie.TLV_CODE_MAC_SIZE]       = RUIJIE_MAC_SIZE
        _value[onie.TLV_CODE_MANUF_NAME]     = RUIJIE_MANUF_NAME
        _value[onie.TLV_CODE_MANUF_COUNTRY]  = RUIJIE_MANUF_COUNTRY
        _value[onie.TLV_CODE_VENDOR_NAME]    = RUIJIE_VENDOR_NAME
        _value[onie.TLV_CODE_DIAG_VERSION]   = RUIJIE_DIAG_VERSION
        _value[onie.TLV_CODE_SERVICE_TAG]    = RUIJIE_SERVICE_TAG
        if 0x00004052 == RUIJIE_CARDID:
            _value[TLV_CODE_PRODUCT_NAME] = RUIJIE_PRODUCTNAME + "-RJ"
        elif 0x00004051 == RUIJIE_CARDID or 0x00004050 == RUIJIE_CARDID:
            changeTypeValue(_value, TLV_CODE_PRODUCT_NAME,
                        "产品名称",RUIJIE_PRODUCTNAME)
        sample = "0000000000000"
        board_sn_len = TESTCASE.get('setmacsnlen', {}).get("board", BOARD_SN_LEN_DEF)
        sample = sample.ljust(board_sn_len, '0')
        changeTypeValue(_value, TLV_CODE_SERIAL_NUMBER,
                        "SN", sample)  # 添加序列号
        changeTypeValue(_value, TLV_CODE_DEVICE_VERSION,
                        "硬件版本号", "101")  # 硬件版本号
        changeTypeValue(_value, TLV_CODE_MAC_BASE,
                        "MAC地址", "58696cfb2108")  # MAC地址
        if FACTESTMODULE.get("setmac_extend", 0) == 1:      # setmac扩展以下五个字段
            changeTypeValue(_value, TLV_CODE_PART_NUMBER,
                            "Part Number", RUIJIE_PART_NUMBER)  # 添加Part Number
            changeTypeValue(_value, TLV_CODE_LABEL_REVISION,
                            "Label Revision", "BN/RMA")  # Label Revision
            changeTypeValue(_value, TLV_CODE_ONIE_VERSION,
                            "ONIE Version", RUIJIE_ONIE_VERSION)  # ONIE Version
            changeTypeValue(_value, TLV_CODE_MANUF_NAME,
                            "Manufacturer", RUIJIE_MANUF_NAME)  # 产商名称
            changeTypeValue(_value, TLV_CODE_SERVICE_TAG,
                            "Service Tag", RUIJIE_SERVICE_TAG)  # 服务编号
        _value[TLV_CODE_MANUF_DATE] = time.strftime(
            '%m/%d/%Y %H:%M:%S', time.localtime())  # 自动添加setmac时间
        rst, ret = onie.generate_value(_value)
        if util_setmac("eth0", _value[TLV_CODE_MAC_BASE]) == True:  # 设置网卡IP
            writeToEEprom(rst)  # 写值到e2中
        else:
            return False
    except SETMACException as e:
        #print e
        RJPRINTERR("\n\n%s\n\n" % e)
        return False
    except ValueError as e:
        return False
    return True

def generate_ext(cardid):
    s = "%08x" % cardid
    ret = ""
    for t in range(0, 4):
        ret += chr(int(s[2 * t:2 * t + 2], 16))
    ret = chr(0x01) + chr(len(ret)) + ret
    return ret


def test_stop_fanctrol():
    stopFanctrol()
    return True,""

def test_start_fanctrol():
    startFanctrol()
    return True,""

def test_power_pmbus_msg():
    '''获取电源PMBUS信息'''
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    errmsg = ""
    frustatus = TESTCASE.get("frustatus",None)
    if frustatus is None:
        RET[RETURN_KEY1] = -999
        RET[RETURN_KEY2] = 'config error'
        return RET

    psu_pmbus = frustatus.get('psupmbus', None)
    if psu_pmbus is None:
        RET[RETURN_KEY1] = -998
        RET[RETURN_KEY2] = 'config error'
        return RET

    for item in psu_pmbus:
        print(item.get('name'))
        loc = item.get('values')
        for lo in loc:
            retval = ""
            rval = None
            name = lo.get('displayname')
            unit = lo.get('unit')
            location = lo.get('location')
            min_value = lo.get('min',-999999)
            max_value = lo.get('max',999999)
            try:
                locations = glob.glob(location)
                with open(locations[0], 'r') as fd1:
                    retval = fd1.read()
                if unit == 'A' or unit == 'V' or unit == 'C':
                    rval = float(retval)/1000
                elif unit == 'W':
                    rval = float(retval)/1000/1000
                else:
                    rval = float(retval)
                if rval >= max_value or rval <= min_value:
                    totalerr -= 1
                RJPRINT("  %-20s: %.2f %s" %(name, rval, unit))
            except Exception as e:
                totalerr -= 1
                errmsg = " %s %s" % (errmsg, str(e))
                RJPRINT("  %-20s: error" %(name))
    RET[RETURN_KEY1] = totalerr
    RET[RETURN_KEY2] = errmsg
    return RET


def test_power_pmbus_msg_by_model():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    errmsg = ""
    frustatus = TESTCASE.get("frustatus",None)
    if frustatus is None:
        RET[RETURN_KEY1] = -999
        RET[RETURN_KEY2] = 'config error'
        return RET

    psu_pmbus = frustatus.get('psupmbus', None)
    if psu_pmbus is None:
        RET[RETURN_KEY1] = -998
        RET[RETURN_KEY2] = 'config error'
        return RET

    for item in psu_pmbus:
        print(item.get('name'))
        bus = item.get('bus')
        addr = item.get('addr')
        eeprom = I2CUTIL.dumpValueByI2c(bus, addr)
        if eeprom is None:
            totalerr -= 1
            errmsg += "Failed to read pus eeprom, bus: %d, addr: 0x%x\n" % (bus, addr)
            RJPRINT(errmsg)
            continue
        fru = ipmifru()
        fru.decodeBin(eeprom)
        psu_model = fru.productInfoArea.productPartModelName.strip()
        if psu_model not in item:
            loc = item.get('others')
        else:
            loc = item.get(psu_model)
        for lo in loc:
            retval = ""
            rval = None
            name = lo.get('displayname')
            unit = lo.get('unit')
            location = lo.get('location')
            min_value = lo.get('min',-999999)
            max_value = lo.get('max',999999)
            try:
                locations = glob.glob(location)
                with open(locations[0], 'r') as fd1:
                    retval = fd1.read()
                if unit == 'A' or unit == 'V' or unit == 'C':
                    rval = float(retval)/1000
                elif unit == 'W':
                    rval = float(retval)/1000/1000
                else:
                    rval = float(retval)
                if rval >= max_value or rval <= min_value:
                    totalerr -= 1
                RJPRINT("  %-20s: %.2f %s" %(name, rval, unit))
            except Exception as e:
                totalerr -= 1
                errmsg += " %s" % str(e)
                RJPRINT("  %-20s: error" %(name))
    RET[RETURN_KEY1] = totalerr
    RET[RETURN_KEY2] = errmsg
    return RET


    eeprom = I2CUTIL.dumpValueByI2c(psu.get('bus'), psu.get('loc'))
    if eeprom is None:
        raise Exception("%s:wrong value" % psu.get('name'))
    fru = ipmifru()
    fru.decodeBin(eeprom)


def test_power_status():
    '''测试电源状态'''
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    fanstatusdecode = TESTCASE.get("frustatusdecode",None)
    fanstatus = TESTCASE.get("frustatus",None)
    errmsg = ""

    if fanstatus is None or fanstatusdecode is None:
        RET[RETURN_KEY1] = -999
        RET[RETURN_KEY2] = 'config error'
        return RET

    psu_conf = fanstatus.get('psus', None)
    if psu_conf is None:
        RET[RETURN_KEY1] = -998
        RET[RETURN_KEY2] = 'config error'
        return RET

    psupresent = fanstatusdecode.get('psupresent')
    psuoutput = fanstatusdecode.get('psuoutput')
    psualert = fanstatusdecode.get('psualert')

    for item_fan in psu_conf:
        retval = None
        gettype = item_fan.get('gettype',None)
        statusbit = item_fan.get('statusbit')
        presentbit = item_fan.get('presentbit')
        alertbit = item_fan.get('alertbit')
        if gettype is not None and gettype == "io":
            io_addr = item_fan.get('io_addr')
            val = io_rd(io_addr)
            if val is not None:
                retval = val
            else:
                totalerr -=1
                errmsg = " %s  %s" % (errmsg, "lpc read failed")
                pass
        else:
            i2c_addr = item_fan.get('i2c_addr')
            bus = i2c_addr['bus']
            devno = i2c_addr['devno']
            reg_offset = i2c_addr['reg_offset']
            ind, val = rji2cget(bus, devno,reg_offset)
            if ind == True:
                retval = val
            else:
                totalerr -=1
                errmsg = " %s  %s" % (errmsg, "i2c read failed")
                pass
        if retval is None:
            continue
        val_t = (int(retval,16) & (1<< presentbit)) >> presentbit
        val_status = (int(retval,16) & (1<< statusbit)) >> statusbit
        val_alert = (int(retval,16) & (1<< alertbit)) >> alertbit
        msg = "%s \n" \
              "    Presence: %s\n"\
              "    Output  : %s \n"\
              "    Alert   : %s \n"% (item_fan.get('name'),psupresent.get(val_t),psuoutput.get(val_status),psualert.get(val_alert))
        RJPRINT(msg)
        if val_t != psupresent.get('okval') or val_status != psuoutput.get('okval') or val_alert != psualert.get('okval'):
            errmsg += msg
            totalerr -=1
        else:
            pass

    RET[RETURN_KEY1] = totalerr
    RET[RETURN_KEY2] = errmsg
    return RET

def test_fan_speed_average(loc,read_cnt=5,critical_speed=None):
    speedlist = []
    max_cnt = read_cnt + 5    # 冗余5次
    for i in range(0,max_cnt):
        real_value = get_pmc_register(loc)
        if real_value.isdigit():
            speedlist.append(int(real_value))
        else:
            log_debug("fan speed read error,times:%d,loc:%s"%(i,loc))
        if len(speedlist) == read_cnt:
            break
        time.sleep(0.01)
    if len(speedlist) == read_cnt:
        log_debug("风扇转速排序前: %s" % speedlist)
        speedlist.sort()
        log_debug("风扇转速排序后: %s" % speedlist)
        if critical_speed is not None and speedlist[read_cnt-1] >= critical_speed:
            return speedlist[read_cnt-1]
        return speedlist[int((read_cnt -1)/2)]    # 取中值
    return -1

def test_ctc_fan_speed():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    fan_speed_conf = TESTCASE.get("CTC_FAN_SPEED_CONF")
    if fan_speed_conf is None:
        RET[RETURN_KEY1] = -999
        RET[RETURN_KEY2] = 'config error'
        return RET
    for item in fan_speed_conf:
        RJPRINT(item.get("name"))
        for child in item.get("child", []):
            childname = child.get("name")
            gettype = child.get("gettype")
            if gettype != "i2c":
                RJPRINT("    %s unsupport gettype:%s" % (childname, gettype))
                totalerr -= 1
                continue
            bus = child.get("bus")
            loc = child.get("loc")
            offset = child.get("offset")
            ind, val = rji2cget(bus, loc,offset)
            if ind is False:
                RJPRINT("    %s get speed failed, log:%s" % (childname, val))
                totalerr -= 1
                continue
            calc_format = child.get("format")
            speed = eval(calc_format % val)
            max = child.get("max")
            min = child.get("min")
            if speed > max or speed < min:
                totalerr -= 1
                RJPRINT("    %s (%s) not in [%d, %d] failed" % (childname, speed, min, max))
            else:
                RJPRINT("    %s (%s)"%(childname,  speed))
    RET[RETURN_KEY1] = totalerr
    return RET

def test_fan_speed():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    ret_t = 0
    errmsg =""

    low_speed = fanlevel.get('low_speed')[0] if 'low_speed' in fanlevel else None
    high_speed = fanlevel.get('high_speed')[2] if 'high_speed' in fanlevel else None
    for item_fan in fanloc:
        RJPRINT(item_fan.get('name'))
        for fanstatus in item_fan["childfans"]:
            if 'low_speed' in fanstatus:
                low_speed = fanstatus.get('low_speed')[0]
                high_speed = fanstatus.get('high_speed')[2]
            nowspeed = test_fan_speed_average(fanstatus["location"])
            if nowspeed == -1:
                RJPRINT("    %s : %s"%(fanstatus["name"], "[FAILED]"))
                ret_t -= 1
                continue
            if nowspeed not in list(range(low_speed, high_speed)):
                ret_t -= 1
                speedmsg = "(%d) not in [%d, %d] failed"% ( nowspeed, low_speed, high_speed)
                errmsg = " %s %s %s\n" % (errmsg, fanstatus["name"],speedmsg)
            else:
                speedmsg = "(%d)"% (nowspeed)
            RJPRINT("    %s %s"%(fanstatus["name"],speedmsg))
    RET[RETURN_KEY1] = ret_t
    RET[RETURN_KEY2] = errmsg
    return RET

def test_M6510_fan_speed():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    fanspeedcheck = TESTCASE.get("fanspeedcheck",None)
    printmsg = ""
    speedmsg = ""
    errmsg = ""

    if fanspeedcheck is None:
        RET[RETURN_KEY1] = -999
        RET[RETURN_KEY2] = 'config error'
        return RET

    low_speed = fanspeedcheck.get("low_speed")
    high_speed = fanspeedcheck.get("high_speed")
    critical_speed = fanspeedcheck.get("critical_speed")
    fanloc = fanspeedcheck.get("fanloc")
    speed_read_times = fanspeedcheck.get("speed_read_times")
    retry = fanspeedcheck.get("retry")          # 重试次数

    for item_fan in fanloc:
        try:
            fan_name = item_fan.get('name')
            retry_cnt = 0
            while retry_cnt < retry:          # 按照每个风扇来重试
                nowspeed = test_fan_speed_average(item_fan["speed_loc"],speed_read_times,critical_speed)
                log_debug("%s speed:%d retry:%d" % (fan_name,nowspeed,retry_cnt))
                if nowspeed == -1 or nowspeed >= critical_speed:
                    speedmsg = "%s (%d) not in [%d, %d] failed"% (fan_name, nowspeed, low_speed, high_speed)
                    totalerr -= 1
                    break
                if nowspeed <= high_speed and nowspeed >= low_speed:
                    speedmsg = "%s (%d)"% (fan_name, nowspeed)
                    break
                speedmsg = "%s (%d) not in [%d, %d] failed"% (fan_name, nowspeed, low_speed, high_speed)
                retry_cnt += 1
            RJPRINT("    %s"% speedmsg)
            if retry_cnt == retry:
                totalerr -= 1
                errmsg += (speedmsg + "\n")
        except Exception as e:
            totalerr -= 1
            errmsg += (srt(e) + "\n")
    RET[RETURN_KEY1] = totalerr
    RET[RETURN_KEY2] = errmsg
    return RET

def cat_file_value(url):
    cmd = "cat %s" % url
    ret, log = rj_os_system(cmd)
    if ret:
        log_error("command:%s. run fail.log:%s" % (cmd, log))
        return False, log
    return True, log

def get_rotor_status(url):# url /sys/rg_plat/fan/fan1/motor0
    rotor_status = {}
    ret, log = cat_file_value("%s/status" % url)
    if ret is False:
        rotor_status.update({"status": -999})
        return False, rotor_status
    if log == "1":
        rotor_status.update({"status": True})
    else:
        rotor_status.update({"status": False})
    return True, rotor_status

def get_rotor_speed(url):# url /sys/rg_plat/fan/fan1/motor0
    rotor_speed = {}
    ret, log = cat_file_value("%s/speed" % url)
    if ret is False:
        return False, rotor_speed
    tmp = int(log)
    rotor_speed.update({"speed": tmp})
    return True, rotor_speed

def get_rotor_ratio(url):# url /sys/rg_plat/fan/fan1/motor0
    rotor_ratio = {}
    ret, log = cat_file_value("%s/ratio" % url)
    if ret is False:
        rotor_ratio.update({"ratio": -999})
        return False, rotor_ratio
    tmp = int(log)
    rotor_ratio.update({"ratio": tmp})
    return True, rotor_ratio

def get_rotor_info(rotor_url): #rotor_url = /sys/rg_plat/fan/fan1/motor0
    rotor = {}
    errflag = True
    ret, rotor_status = get_rotor_status(rotor_url)
    if ret is False:
        log_error("get_rotor_status fail rotor_url = %s" % rotor_url)
        errflag = False
    ret, rotor_speed = get_rotor_speed(rotor_url)
    if ret is False:
        log_error("get_rotor_speed fail rotor_url = %s" % rotor_url)
        errflag = False
    ret, rotor_ratio = get_rotor_ratio(rotor_url)
    if ret is False:
        log_error("get_rotor_ratio fail rotor_url = %s" % rotor_url)
        errflag = False
    rotor.update(rotor_status)
    rotor.update(rotor_speed)
    rotor.update(rotor_ratio)
    return errflag, rotor

def get_fan_info(fan_url): #fan_url = /sys/rg_plat/fan/fan1
    fan = {}
    err_flag = True
    tmp = 0

    ret, log = cat_file_value("%s/present" % fan_url)
    if ret is False:
        fan.update({"present": -999})
        return False, fan

    if log == "1":
        fan.update({"present": True})
    else:
        fan.update({"present": False})
        return True, fan

    ret, log = cat_file_value("%s/num_motors" % fan_url)
    if ret is False:
        fan.update({"num_motors": -999})
        err_flag = False
    else:
        try:
            tmp = int(log)
            fan.update({"num_motors": tmp})
        except Exception as e:
            return False, fan

    for i in range(tmp):
        name = "motor%d" % i
        rotor_url = fan_url + "/" +  name
        ret, rotor = get_rotor_info(rotor_url)
        if ret is False:
            log_error("get rotor info fail %s" % rotor_url)
            err_flag = False
            continue
        fan.update({name: rotor})
    if err_flag is False:
        return False, fan
    return True, fan

def set_rotor_ratio(url, ratio):
    cmd = "echo %d > %s" % (ratio, url)
    ret, log = rj_os_system(cmd)
    if ret:
        return False, log
    return True, log

def set_fans_ratio(ratio):
    ret, fans = get_fans_info("/sys/wb_plat/fan")
    fansnum = fans.get("num_fans")
    if fansnum is None:
        log_error("风扇个数获取失败")
        return False
    totalerr = 0
    for i in range(fansnum):
        fanname = "fan%d" % (i+1)
        fan_dit = fans.get(fanname)
        if fan_dit.get("present") is False:
            totalerr = -1
            log_error("设置转速失败， 风扇%d在位状态 ABSENT"% (i + 1))
            continue
        morotsnum = fan_dit.get("num_motors")
        for i in range(morotsnum):
            name = "motor%d" % i
            url = "/sys/wb_plat/fan/%s/%s/ratio" % (fanname, name)
            ret, log = set_rotor_ratio(url, ratio)
            if ret is False:
                log_error("set ratio fail where=%s" % url)
                totalerr = -1
    if totalerr < 0:
        return False
    return True

def get_fans_info(fans_url): #fans_url = /sys/rg_plat/fan/
    fans = {}
    ret, log = cat_file_value("%s/num_fans" % fans_url)
    if ret is False:
        fans.update({"num_fans": -999})
        return False, fans
    try:
        tmp = int(log)
    except Exception as e:
        return False, fans
    fans.update({"num_fans": tmp})
    err_flag = True
    for i in range(tmp):
        name = "fan%d" % (i + 1)
        fan_url = fans_url + "/" +  name
        ret, rotor = get_fan_info(fan_url)
        if ret is False:
            log_error("get_fan_info fail %s" % fan_url)
            err_flag = False
            continue
        fans.update({name: rotor})
    if err_flag is False:
        return False, fans
    return True, fans

def test_fan_status_standard_sysfs():
    RET = {RETURN_KEY1: 0, RETURN_KEY2: ""}
    try:
        ret, fans = get_fans_info("/sys/rg_plat/fan")
        fansnum = fans.get("num_fans", None)
        if fansnum is None:
            RET[RETURN_KEY1] = -1
            RJPRINT("风扇个数获取失败")
            return RET
        totalerr = 0
        for i in range(fansnum):
            name = "fan%d" % (i + 1)
            fan_dit = fans.get(name)
            if fan_dit.get("present") is False:
                totalerr = -1
                RJPRINT("    风扇%d在位状态 ABSENT"% (i + 1))
                continue
            else:
                RJPRINT("    风扇%d在位状态 PRESENT" % (i + 1))
            morotsnum = fan_dit.get("num_motors")
            for i in range(morotsnum):
                name = "motor%d" % i
                morot_dit = fan_dit.get(name)
                if morot_dit.get("status") is False:
                    RJPRINT("    马达%d STALL" % (i + 1))
                    totalerr = -1
                else:
                    RJPRINT("    马达%d ROLL" % (i + 1))
        RET[RETURN_KEY1] = totalerr
    except Exception as e:
        msg = traceback.format_exc()
        RJPRINT(msg)
    return RET

def test_fan_speed_standard_sysfs():
    RET = {RETURN_KEY1: 0, RETURN_KEY2: ""}
    try:
        ret, fans = get_fans_info("/sys/rg_plat/fan")
        fansnum = fans.get("num_fans", None)
        if fansnum is None:
            RET[RETURN_KEY1] = -1
            RJPRINT("Failed to get fan number")
            return RET
        FANS_THRESHOLD = TESTCASE.get("FANS_THRESHOLD")
        FanLowLevel  = TESTCASE.get("FanLowLevel")
        FanHighLevel = TESTCASE.get("FanHighLevel")
        totalerr = 0
        for i in range(fansnum):
            name = "fan%d" % (i + 1)
            log_debug("test_fan_speed_by_sysfs %s" % name)
            FAN_THRESHOLD = FANS_THRESHOLD.get(name)
            low_threshold = FAN_THRESHOLD.get(FanLowLevel)
            high_threshold = FAN_THRESHOLD.get(FanHighLevel)
            fan_dit = fans.get(name)
            if fan_dit.get("present") is False:
                totalerr = -1
                RJPRINT("FAN%d : %s" % ((i + 1), "[FAILED]"))
                continue
            RJPRINT("FAN%d" % (i + 1))
            morotsnum = fan_dit.get("num_motors")
            for i in range(morotsnum):
                name = "motor%d" % i
                morotlow = low_threshold.get(name).get("low")
                morothigh = high_threshold.get(name).get("high")
                log_debug("test_fan_speed_by_sysfs %s morotlow：%d, morothigh:%d" % (name, morotlow, morothigh))
                morot_dit = fan_dit.get(name)
                nowspeed = morot_dit.get("speed")
                if morotlow < nowspeed and morothigh > nowspeed:
                    speedmsg = "(%d)" % (nowspeed)
                else:
                    totalerr -= 1
                    speedmsg = "(%d) not in [%d, %d] failed" % (nowspeed, morotlow, morothigh)
                RJPRINT("    motor%d %s" % (i, speedmsg))
        RET[RETURN_KEY1] = totalerr
    except Exception as e:
        msg = traceback.format_exc()
        RJPRINT(msg)
    return RET

def test_fan_ratio_standard_sysfs(param=None):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    try:
        totalerr = 0
        if param is None:
            RET[RETURN_KEY1] = -999
            RET[RETURN_KEY2] = 'param err'
            return RET
        param_t = json.loads(param)
        sleeptime = param_t.get('sleep', None)
        ratio = param_t.get('ratio', 0)

        if sleeptime is None or isinstance(sleeptime,int) == False:
            RET[RETURN_KEY1] = -998
            RET[RETURN_KEY2] = 'sleeptime param err'
            return RET

        if ratio == 0:
            RET[RETURN_KEY1] = -997
            RET[RETURN_KEY2] = 'ratio err'
            return RET

        RJPRINT("设置风扇转速等级: %d" % ratio)
        ret = set_fans_ratio(ratio) #设置转速比率
        if ret < 0:
            totalerr = -1
            RJPRINT("转速设置失败")
        time.sleep(sleeptime)
        ret, fans = get_fans_info("/sys/wb_plat/fan")
        FANS_THRESHOLD = TESTCASE.get("FANS_THRESHOLD")
        fansnum = fans.get("num_fans", None)
        if fansnum is None:
            RET[RETURN_KEY1] = -1
            RJPRINT("风扇个数获取失败")
            return RET
        for i in range(fansnum):
            name = "fan%d" % (i+1)
            fan_dit = fans.get(name)
            FAN_THRESHOLD = FANS_THRESHOLD.get(name).get(ratio, None)
            if fan_dit.get("present") is False:
                totalerr = -1
                RJPRINT("风扇%d不在位" % (i+1))
                continue
            if FAN_THRESHOLD is None:
                totalerr = -1
                RJPRINT("   阈值获取失败")
                continue
            RJPRINT("风扇%d" % (i+1))
            morotsnum = fan_dit.get("num_motors")
            for i in range(morotsnum):
                name = "motor%d" % i
                morotlow = FAN_THRESHOLD.get(name).get("low")
                morothigh = FAN_THRESHOLD.get(name).get("high")
                log_debug("test_fan_speed_by_sysfs %s morotlow：%d, morothigh:%d" % (name, morotlow, morothigh))
                morot_dit = fan_dit.get(name)
                nowspeed = morot_dit.get("speed")
                if nowspeed not in list(range(morotlow, morothigh)):
                    totalerr -= 1
                    RJPRINT("    马达%d （%d） : %s  阈值: [%d , %d]" % (i,nowspeed, "[FAILED]", morotlow, morothigh))
                else:
                    RJPRINT("    马达%d （%d） : %s  阈值: [%d , %d]" % (i,nowspeed, "[PASS]", morotlow, morothigh))
        RET[RETURN_KEY1] = totalerr
    except Exception as e:
        msg = traceback.format_exc()
        RJPRINT(msg)
    return RET

def test_fan_status():
    '''测试风扇状态 在线和转动'''
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    fanstatusdecode = TESTCASE.get("frustatusdecode",None)
    fanstatus = TESTCASE.get("frustatus",None)

    if fanstatus is None or fanstatusdecode is None:
        RET[RETURN_KEY1] = -999
        RET[RETURN_KEY2] = 'config error'
        return RET

    fans_conf = fanstatus.get('fans', None)
    if fans_conf is None:
        RET[RETURN_KEY1] = -998
        RET[RETURN_KEY2] = 'config error'
        return RET

    fanpresent = fanstatusdecode.get('fanpresent')
    fanroll = fanstatusdecode.get('fanroll')

    for item_fan in fans_conf:
        RJPRINTLINE(item_fan.get('name'))
        presentbus = item_fan.get('bus')
        presentaddr = item_fan.get('presentloc')
        presentbit = item_fan.get('presentbit')
        loc      = item_fan.get('loc')
        childs   = item_fan.get('childfans')
        ind, val = rji2cget(presentbus, loc,presentaddr)
        if ind == True:
            val_t = (int(val,16) & (1<< presentbit)) >> presentbit
            RJPRINT(fanpresent.get(val_t))
            if val_t != fanpresent.get('okval'):
                totalerr -=1
            else:
                pass
        else:
            totalerr -=1
            RJPRINT("Failed to get present status")

        for child in childs:
            RJPRINTLINE("    %s" % child.get('name'))
            statusloc  = child.get('statusloc', None)
            statusbit  = child.get('statusbit', None)
            ind, val = rji2cget(presentbus, loc, statusloc)
            if ind == True:
                val_t = (int(val,16) & (1<< statusbit)) >> statusbit
                RJPRINT(fanroll.get(val_t))
                if val_t != fanroll.get('okval'):
                    totalerr -=1
                else:
                    pass
            else:
                totalerr -=1
                RJPRINT("Failed to get status")
    RET[RETURN_KEY1] = totalerr
    return RET


def test_fan_speed_new(param=None):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    try:
        ret_t = 0
        if param is None:
            RET[RETURN_KEY1] = -999
            RET[RETURN_KEY2] = 'param err'
            return RET
        param_t = json.loads(param)
        speedval  = param_t.get('levelval', None)
        lowspeed  = param_t.get('low', None)
        highspeed = param_t.get('high', None)
        sleeptime = param_t.get('sleep', None)
        threshold = param_t.get('threshold', 0)

        if sleeptime is None or isinstance(sleeptime,int) == False:
            RET[RETURN_KEY1] = -998
            RET[RETURN_KEY2] = 'sleeptime param err'
            return RET

        # if speedval is None or lowspeed is None or highspeed is None:
        #     RET[RETURN_KEY1] = -998
        #     RET[RETURN_KEY2] = 'speedval/lowspeed/highspeed param err'
        #     return RET
        if lowspeed is not None:
            strtmp = "写入cpld值:0x%02x  阈值: [%d , %d]"% (speedval, lowspeed, highspeed)
            RJPRINT(strtmp)
            log_debug(strtmp)

        for item in fanloc:
            loc = item.get('location')
            write_sysfs_value(loc, "0x%02x"% speedval )
            ret_val = get_sysfs_value(loc)
            log_debug("写入的值为%s" % ret_val)
        time.sleep(sleeptime)

        caseerror = ""
        for item_fan in fanloc:
            RJPRINT(item_fan.get('name'))
            for fanstatus in item_fan["childfans"]:
                real_value = get_pmc_register(fanstatus["location"])
                if "low_speed" in fanstatus:
                    lowspeed = fanstatus.get("low_speed")[threshold]
                    highspeed = fanstatus.get("high_speed")[threshold]
                    strtmp = "写入cpld值:0x%02x  阈值: [%d , %d]" % (speedval, lowspeed, highspeed)
                    RJPRINT(strtmp)
                if real_value.isdigit():
                    nowspeed = int(real_value)
                    log_debug("%s (now: %d low:%d high:%d)"% (fanstatus["name"], nowspeed ,lowspeed,highspeed))
                    speedmsg = "(%d)"% ( nowspeed)
                    if lowspeed < nowspeed and highspeed > nowspeed:
                        RJPRINT("    %s %s : %s"%(fanstatus["name"],speedmsg, "[PASS]"))
                    else:
                        RJPRINT("    %s %s : %s"%(fanstatus["name"],speedmsg, "[FAILED]"))
                        caseerror += "name:%s %s 不在转速范围内 [nowspeed: %d low_speed:%d high:%d] \n" % (item_fan.get('name'),fanstatus["name"], nowspeed ,lowspeed,highspeed)
                        ret_t -= 1
                else:
                    RJPRINT("    %s : %s"%(fanstatus["name"], "[FAILED]"))
                    caseerror +=  "name: %s %s  获取转速为空 \n" % (item_fan.get('name'),fanstatus["name"])
                    ret_t -= 1
        RET[RETURN_KEY1] = ret_t
        RET[RETURN_KEY2] = caseerror
    except Exception as e:
        RET[RETURN_KEY1] = -9999
        RET[RETURN_KEY2] = str(e)
        RJPRINT(str(e))
    return RET

# ====================================
# 风扇状态检测
# ====================================
def test_fan():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    log = []
    #sysinfo_showfanmsg_ind = factest_module.get('sysinfo_showfanmsg', 1)
    #if sysinfo_showfanmsg_ind == 1:
    #    log_debug("正在获取风扇信息")
    #    RJPRINT('%s '% "风扇状态获取")
    #    totalfanstatus = []
    #    status.checkFan(totalfanstatus)
    #    for fanstatus in totalfanstatus:
    #        RJPRINT('%s%s: %s'%    (fanstatus["id"], "状态  ", fanstatus["errmsg"]))
    #    RJPRINT('')

    RJPRINT('%s '% "风扇转速设置")
    ret = fan_check1(fanloc, fanlevel, log)
    if ret == 0:
        RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    else:
        RET[RETURN_KEY1] = ret
        RET[RETURN_KEY2] = log
    return RET


def M6510_check(fanlevelcheck):
    RET = {"status" : "", "printmsg":"","errmsg" : ""}
    errcnt = 0
    failcnt = 0
    printmsg = ""
    speedmsg = ""
    errmsg = ""

    fanlevel = fanlevelcheck.get("fanlevel")
    level_loc = fanlevelcheck.get("level_loc")
    fanloc = fanlevelcheck.get("fanloc")
    critical_speed = fanlevelcheck.get("critical_speed")
    sleep_time = fanlevelcheck.get("sleep")
    speed_read_times = fanlevelcheck.get("speed_read_times")

    try:
        for level in fanlevel:
            tips = level.get("tips")
            fan_level = level.get("level")
            lowspeed = level.get("low_speed")
            highspeed = level.get("high_speed")
            strtmp = "风扇转速等级: 【%s】 写入cpld值:0x%02x  阈值: [%d , %d]\n"% (tips, fan_level,lowspeed,highspeed)
            log_debug(strtmp)
            errmsg += strtmp
            printmsg += strtmp

            write_sysfs_value(level_loc, "0x%02x"% fan_level )
            ret_val = get_sysfs_value(level_loc)
            log_debug("写入的值为%s" % ret_val)
            time.sleep(sleep_time)

            for fan_item in fanloc:
                name = fan_item.get("name")
                speed_loc = fan_item.get("speed_loc")
                nowspeed = test_fan_speed_average(speed_loc,speed_read_times,critical_speed)
                speedmsg = "(%d)"% ( nowspeed)
                log_debug("%s (now: %d low:%d high:%d)"% (name, nowspeed ,lowspeed,highspeed))
                if nowspeed != -1 and nowspeed < critical_speed:
                    if nowspeed >= lowspeed and nowspeed <= highspeed:
                        strtmp = "    %s %s : %s\n"%(name,speedmsg, "[PASS]")
                    else:
                        strtmp = "    %s %s : %s\n"%(name,speedmsg, "[FAILED]")
                        errmsg += "%s 不在转速范围内 [nowspeed: %d low_speed:%d high:%d]\n" % (name,nowspeed ,lowspeed,highspeed)
                        failcnt -= 1
                else:
                    strtmp = "    %s %s : %s" % (name,speedmsg, "[FAILED]")
                    errmsg += "%s 不在转速范围内 [nowspeed: %d low_speed:%d high:%d]\n" % (name,nowspeed ,lowspeed,highspeed)
                    errcnt -= 1
                printmsg += strtmp
        RET["printmsg"] = printmsg
        RET["errmsg"] = errmsg
        if errcnt < 0:
            RET["status"] = "error"
        elif failcnt < 0:
            RET["status"] = "fail"
        else:
            RET["status"] = "pass"
    except Exception as e:
        RET["status"] = "fail"
        RET["printmsg"] = str(e)
        RET["errmsg"] = str(e)
        log_error(e.message)
    return RET

# ====================================
# M6510风扇状态检测
# ====================================
def test_M6510_fan():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    fanlevelcheck = TESTCASE.get("fanlevelcheck",None)
    printmsg = ""
    speedmsg = ""
    errmsg = ""

    if fanlevelcheck is None:
        RET[RETURN_KEY1] = -999
        RET[RETURN_KEY2] = 'config error'
        return RET
    retry = fanlevelcheck.get("retry")          # 重试次数

    RJPRINT('%s '% "风扇转速设置")
    for i in range(retry):
        try:
            ret = M6510_check(fanlevelcheck)
            if ret.get("status") == "pass":
                RET[RETURN_KEY1] = 0
                break
            elif ret.get("status") == "error":
                RET[RETURN_KEY1] = -1
                break
            else :
                RET[RETURN_KEY1] = -1
        except Exception as e:
            log = traceback.format_exc()
            log_error(log)
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = log
    RJPRINT(ret.get("printmsg"))
    RET[RETURN_KEY2] = ret.get("errmsg")
    return RET


# ====================================
# CPU内存测试
# ====================================
def test_cpumemoryinfo():
    RET = ERROR_RETURN
    cmd = ""
    ret, log = log_os_system("which memtester", 0)
    if len(log):
        cmd = "memtester "
    else:
        RET[RETURN_KEY2] = "no memtester cmd"
        return RET
    for case in TESTCASE["MEMTORY"]["cases"]:
        RJPRINT("测试项: %s" %case["name"])
        log_debug("case: %s   [%s]" % (case["name"] , case["cmd"]))
        os.system(case["cmd"])
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    return RET

ddr_test_result_file = "/tmp/ddr_test_result"
thread_test_ddr = None;

def test_ddr_stress_with_result():
    test_ddr_stress()
    print_temp("后台执行测试，等待100s", False)
    time.sleep(100)
    return test_ddr_stress_result()

def stop_docker():
    file_name = '/tmp/.docker_stop_over'
    if os.path.exists(file_name) is False:
        RJPRINT("请稍等")
        timeout = 300
        while timeout > 0:
            try:
                ret, log = rj_os_system("systemctl is-active snmp.service") #启动完成才能正常关闭
                if ret == 0 and "active" in log: #docker启动完毕
                    ret, log = rj_os_system("systemctl stop snmp.timer") #关闭自启
                    time.sleep(3)
                    ret1, log1 = rj_os_system("docker stop snmp swss syncd dhcp_relay radv") #关闭后续启动的无用docker
                    if ret == 0 and ret1 == 0:
                        open(file_name, "w") #用于判断是否已关闭过docker
                        return True, ""
                    else:
                        log_error("log:%s,log1:%s" % (log, log1))
                        break
                else:
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    timeout -= 1
                    time.sleep(1)
            except Exception as e:
                log_debug(str(e))
                continue
        RJPRINT("stop docker fail")
        return False, ""
    else:
        return True, ""

def test_ddr_stress():
    global thread_test_ddr
    RET = {RETURN_KEY1 : 1, RETURN_KEY2 : ""}
    ret, log = log_os_system("which stressapptest", 0)
    if len(log):
        if thread_test_ddr != None:
            RET[RETURN_KEY2] = "已有DDR后台执行任务，请首先查看测试结果或终止上次测试任务"
            RJPRINT(RET[RETURN_KEY2])
            return RET
        RET[RETURN_KEY2] = "已启动后台执行"
        cmd = "free -m|grep Mem"
        ret, log = rj_os_system(cmd)
        if "Mem" not in log:
            RJPRINT("Memory info get fail.log=%s, cmd=%s" % (log, cmd))
            RET[RETURN_KEY1] = -1
            return RET
        tmp = log.split()
        mem_test_size = int(tmp[1]) - int(tmp[2]) - 600 # tmp[1]total,tmp[2] used,200 reserve
        '''
             total       used       free     shared    buffers     cached
Mem:          7896       1247       6649         58        188        343
        '''
        cmd = "stressapptest -M %d -m 1 -s 3600" % mem_test_size
        with open(ddr_test_result_file, "w+") as f:
            #thread_test_ddr = subprocess.Popen("stressapptest -M 512 -m 1 -s 86400",shell=True,stdout=subprocess.PIPE)
            thread_test_ddr = subprocess.Popen(cmd, shell=True, stdout=f)
    else:
        RET[RETURN_KEY2] = "no stressapptest cmd"
    RJPRINT(RET[RETURN_KEY2])
    return RET


def test_ddr_stress_stop():
    RET = {RETURN_KEY1 : 1, RETURN_KEY2 : ""}
    global thread_test_ddr
    if thread_test_ddr == None:
        RET[RETURN_KEY2] = "未启动后台测试"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    if not makesure("强行结束将无法查看结果，是否继续？[Yes/No]：",echo = True):
        RET[RETURN_KEY2] = "已撤销"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    thread_test_ddr.terminate()

    cmd = "kill -9 %d"%(thread_test_ddr.pid + 1)
    #不管输出
    ret, log = log_os_system(cmd, 0)
    RET[RETURN_KEY2] = "该后台测试已被终止"
    thread_test_ddr = None
    RJPRINT(RET[RETURN_KEY2])
    return RET

def force_abort_ddr_stress():
    log_os_system("ps -ef | grep stressapptest | grep -v grep | awk '{print $2}' | xargs kill -9 ", 0)

def test_ddr_stress_result():
    global thread_test_ddr
    RET = {RETURN_KEY1 : 1, RETURN_KEY2 : ""}
    if thread_test_ddr == None:
       RJPRINT("未启动后台测试，没有测试结果")
       return RET

    ret, log = log_os_system("ps -ef | grep stressapptest | grep -v grep | awk '{print $2}'", 0)
    if len(log):
        RJPRINT("测试还未结束，测试时长60mins, 请稍后查看结果")
        return RET
    thread_test_ddr = None
    bufferSize = 50000
    input = ""
    resuult = ""

    try:
       file = os.open(ddr_test_result_file, os.O_RDONLY | os.O_NONBLOCK);
       input = os.read(file, bufferSize);
       resuult = input
       os.close(file)
    except OSError as err:
        if err.errno == 11:#为空，小概率到这里
            resuult = "没有数据"
            os.close(file)

    if "Status: PASS"  not in resuult:
        RET[RETURN_KEY1] = -1
    else:
        RET[RETURN_KEY1] = 0
    RET[RETURN_KEY2] = resuult
    RJPRINT(RET[RETURN_KEY2])
    return RET

# ====================================
# 硬盘测试
# ====================================
def test_hard():
    RET = ERROR_RETURN
    cmd = ""
    ret, log = log_os_system("which smartctl", 0)
    if len(log):
        cmd = "smartctl "
    else:
        RET[RETURN_KEY2] = "no smartctl cmd"
        return RET
    for case in TESTCASE["SMARTCTLCMDS"]["cases"]:
        RJPRINT("测试项: %s" %case["name"])
        log_debug("case: %s   [%s]" % (case["name"] , case["cmd"]))
        os.system(case["cmd"])
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    return RET

# ====================================
# 设置日志等级
# ====================================
def test_log_setlevel(name):
    logger = logging.getLogger()    # initialize logging class
    logger.setLevel(levelNames[name])  # default log level

def test_log_critical():
    test_log_setlevel("CRITICAL")
def test_log_debug():
    test_log_setlevel("DEBUG")
def test_log_error():
    test_log_setlevel("ERROR")
def test_log_info():
    test_log_setlevel("INFO")
def test_log_notset():
    test_log_setlevel("NOTSET")
def test_log_warning():
    test_log_setlevel("WARNING")

#日志输出等级菜单
def test_loginfolevel():
    logger = logging.getLogger()    # initialize logging class
    RJPRINT("当前调试等级为:  %s" % levelNames[logger.level])
    startMenu(3)

#信号处理： 不处理ctrl + N
def sigint_handler(signum, frame):
    global KAOJISTATUS
    KAOJISTATUS = 0
    if ISKAOJI == 1:
        RJPRINT("\n\nAlready input ctrl+c, please wait for the end of this round of execution")
    else:
        RJPRINT("\n\nExit without receiving ctrl+c")

signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGHUP, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)

#配置
def test_config():
    if load_CONFIG() == False:
        sys.exit(1)

# ====================================
# 测试项:校验文件MD5
# ====================================
def checkFileMD5(filename):
     if not os.path.isfile(filename):
         return
     myhash = hashlib.md5()
     f = file(filename,'rb')
     while True:
         b = f.read(8096)
         if not b :
             break
         myhash.update(b)
     f.close()
     return myhash.hexdigest()

def test_portbroadcast_new():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    obj = PortTestCall(port_list_val=[], redirect = True)
    ret, val_dit = obj.port_brcst_test()
    if ret is False:
        RET[RETURN_KEY1] = -1
    tmp = analy_port_result(val_dit)
    subprocess_case.print_result(tmp)
    return RET

# ====================================
# 测试项:端口广播
# ====================================
def test_portbroadcast():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    for i in range(3):
        try:
            ret, log = test_port()
            if ret:
                RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : log}
                break
            else :
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] = log
        except Exception as e:
            log = traceback.format_exc()
            log_error(log)
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = log
    RJPRINT(log)
    return RET

def test_prbs_new1():
    RET = {RETURN_KEY1: 0, RETURN_KEY2: ""}
    obj = PortTestCall(port_list_val=[], redirect = True)
    ret, val_dit = obj.port_prbs_test()
    if ret is False:
        RET[RETURN_KEY1] = -1
    tmp = analy_port_result(val_dit)
    subprocess_case.print_result(tmp)
    return RET
# ====================================
# 测试项:prbs
# ====================================
def test_prbs():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    for i in range(3):
        try:
            ret, log = test_port_prbs()
            if ret:
                RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : log}
                break
            else :
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] = log
        except Exception as e:
            log = traceback.format_exc()
            log_error(log)
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = log
    RJPRINT(log)
    return RET

def test_prbs_new():
    '''prbs新方法测试 add 20190411'''
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    ret, log = test_ports_prbs_new()
    if ret:
        RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    else :
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = log
    return RET

def test_bmc_channel():
    '''测试BMC通路'''
    ret, bmcip = getBMCIP()
    if ret is False:
        msg = "get bmcip faled, log:%s" % bmcip
        return ret, msg
    port = TESTCASE.get('BMC').get('port')
    msg = ''
    returncode = False
    import socket
    try:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(5)
        sk.connect((bmcip,port))
        returncode =  True
    except Exception as e:
        msg = 'BMC channel failed. ip:%s, port:%s \n Exception:%s' % (str(e), bmcip, port)
        returncode = False
    finally:
        sk.close()
    return returncode, msg

# ===================================================================
# 测试项:加载CPU端GPIO模拟MDIO驱动，disable BMC端的MDIO
# ===================================================================
def test_modprobe_cpu_gpio_mdio():
    ret, msg = test_bmc_channel()
    if ret is False:
        return ret, msg
    func = 'bmc_log_os_system'
    cmd = "devmem 0x1e6e2090 32 0x087f0009" #disable bmc mdio
    ret = test_bmc_func(func,cmd)
    if ret[RETURN_KEY1] != 0:
        return ret, msg + " disable bmc mdio fail"
    return True, ''

# ===================================================================
# 测试项:卸载CPU端GPIO模拟MDIO驱动，enable BMC端的MDIO
# ===================================================================
def test_rmmod_cpu_gpio_mdio():
    ret, msg = test_bmc_channel()
    if ret is False:
        return ret, msg
    func = 'bmc_log_os_system'
    cmd = "devmem 0x1e6e2090 32 0x087F000D" #enable bmc mdio
    ret = test_bmc_func(func,cmd)
    if ret[RETURN_KEY1] != 0:
        return False, msg + " enable bmc mdio fail"
    return True, ''

# ===================================================================
# 测试项:CPU端MDIO测试
# ===================================================================
def test_cpu_gpio_mdio():
        RET = {RETURN_KEY1: 0, RETURN_KEY2: ""}
        errtotal = 0
        MDIO_dev_dict = TESTCASE.get("PHY_MDIO_DEV", None)
        if MDIO_dev_dict is None:
            MDIO_dev_dict = {
                "MGMT-54616": ["18"],
                "5387      ": ["00", "01", "02", "03", "04", "05", "06", "07"],
            }

        for dev in list(MDIO_dev_dict.keys()):
            check_log = ""
            dev_errtotal = 0
            for i in MDIO_dev_dict[dev]:
                cmd = "hw_test.bin mdiodev_rd 1 %s 2|grep 0x2|awk '{print $4}'" % i
                ret, log = log_os_system(cmd, 0)
                if ret or log == "0xffff" or log == "0":
                    check_log += i + ": FAILD (%s)\n" % log
                    dev_errtotal -= 1
                else:
                    check_log += i + ": PASS\n"
            errtotal += dev_errtotal
            if dev_errtotal < 0:
                RJPRINT(dev + " : FAILED")
                RJPRINT(check_log)  # 打印详细的错误信息
            else:
                RJPRINT(dev + " : PASS (%s)" % log)

        if errtotal < 0:
            RET[RETURN_KEY1] = -1
        return RET

# ===================================================================
# 测试项:CPU端5387-eeprom-MD5查看
# ===================================================================
def test_cpu_5387_md5(param):
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    cmd = param.get("cmd", None)
    ret, log = log_os_system(cmd, 0)
    devname = param.get("devname", None)
    if devname is not None:
        RJPRINT(devname + log)
    else:
        RJPRINT(log)
    if ret or len(log) == 0:
        RET[RETURN_KEY1] = -1
    else:
        RET[RETURN_KEY1] = 0
        RET[RETURN_KEY2] = log
    return RET

# ===================================================================
# 测试项:CPU端MDIO压力测试
# ===================================================================
def cpu_test_MDIO_stress():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 :""}
    totalerr = 0
    test_times = 10
    for i in range(0, test_times):
       log_debug("\n\n第 %d/%d 次测试"%(i+1, test_times))
       RET1 = test_cpu_gpio_mdio()
       totalerr += RET1[RETURN_KEY1]
    if totalerr < 0:
       RET[RETURN_KEY1] = -1
    return RET

def test_portframe_new():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    obj = PortTestCall(port_list_val=[], redirect = True)
    ret, val_dit = obj.port_frame_test()
    if ret is False:
        RET[RETURN_KEY1] = -1
    tmp = analy_port_result(val_dit)
    subprocess_case.print_result(tmp)
    return RET

# ====================================
# 测试项:端口收发帧
# ====================================
def test_portframe():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    for i in range(3):
        try:
            ret, log = test_port_portframe()
            if ret:
                RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : log}
                break
            else :
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] = log
        except Exception as e:
            log = traceback.format_exc()
            log_error(log)
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = log
    RJPRINT(log)
    return RET


def get_raw_input():
    ret=""
    fd=sys.stdin.fileno()
    old_ttyinfo=termios.tcgetattr(fd)
    new_ttyinfo=old_ttyinfo[:]
    new_ttyinfo[3] &= ~termios.ICANON
    new_ttyinfo[3] &= ~termios.ECHO
    try:
        termios.tcsetattr(fd,termios.TCSANOW,new_ttyinfo)
        ret=input("")
    except Exception as e:
        print(e)
    finally:
        termios.tcsetattr(fd,termios.TCSANOW,old_ttyinfo)
    return ret


def test_port_portframe():
    '''端口收发帧'''
    framenum = 10000
    porttest = PortTest()
    len_t = len(porttest.bcm_ports)
    upports = []
    ret_t = 0
    errt_t = []
    testerror ={}
    caseerror=[]
    testerror["name"] = "端口收发帧"
    successport=[]
    updownerrport=[]
    errorport = []
    try:
        #全部设值UP端口PRBS
        for i in range(len_t):
            status = porttest.get_port_status(i + 1)
            if status == "up":
                upports.append(i + 1)
            else:
                updownerrport.append(i+1)
        if len(updownerrport) > 0:
            ret_t -= 1
            pass
        else:
            porttest.init_port_cpu()
            porttest.clear_port_packets()
            for i in range(len(porttest.bcm_ports)):
                if (i + 1) in upports :
                    porttest.start_send_port_packets(i + 1, framenum, 1024)
                    log_debug("%d:正在发包"%(i+1))
            time.sleep(5)
            for i in range(len(porttest.bcm_ports)):
                if (i + 1) in upports :
                    ret, log = porttest.check_port_packets(i + 1, framenum, "rx")
                    log_debug(ret)
                    if ret == True:
                        successport.append(i + 1)
                    else:
                        errorport.append(i + 1)
                        ret_t -= 1
                        caseerror.append({"name":"端口%d"%(i + 1), "error":"端口收发帧失败"})
                        log_debug(log)
                else:
                    ret_t -= 1
                    caseerror.append({"name":"端口%d"%(i + 1), "error":"up/down状态异常"})
                    updownerrport.append(i+1)
    except Exception as e:
        msg = traceback.format_exc()
        log_error(msg)
        ret_t  = -1
        return False , msg
    finally:
        porttest.reset_port_cpu()
    result_str = ''
    result_str += print_to_str(successport, "OK")
    result_str += print_to_str(updownerrport, "up/down error")
    result_str += print_to_str(errorport, "failed")
    testerror['errmsg'] = caseerror
    errt_t.append(testerror)
    if ret_t < 0:
        return False , result_str
    return True , result_str


def test_ports_prbs_new():
    '''端口prbs'''

    result_t = []
    testerror1 = {}
    testerror1["name"] = "PRBS测试(phy到mac)"
    testerror2 = {}
    testerror2["name"] = "PRBS测试(mac到phy)"
    testerror3 = {}
    testerror3["name"] = "PRBS测试(phy到line)"
    retrytime = 0
    total_err = 0
    pr = None
    val_ber  = TESTCASE.get("PRBS").get("prbsber", None) # 1.0e-8
    totalretrys = TESTCASE.get("PRBS").get("retrytimes", None) # 1.0e-8
    #print val_ber
    macprbsresult = {"success":[], "error":[]}
    sysprbsresult = {"success":[], "error":[]}
    lineprbsresult = {"success":[], "error":[]}

    if val_ber is not None:
        pr = PortPrbsTest(val_ber)
    else:
        pr = PortPrbsTest()
    for i in range(len(pr.bcm_ports)):
        macprbsresult.get('error').append((i+1))
        sysprbsresult.get('error').append((i+1))
        lineprbsresult.get('error').append((i+1))

    while len(macprbsresult.get('error'))> 0 or  len(sysprbsresult.get('error')) > 0 or len(lineprbsresult.get('error'))> 0:
        if retrytime >= totalretrys:
            break
        else:
            ret,log = pr.clear_port_prbs()
            if ret == False:
                raise Exception("prbs清除 %s" % log)
            ret, log = pr.init_port_prbs()
            if  ret == False:
                raise Exception("prbs初始化失败 %s" % log)

            caseerror=[]
            for i in range(len(pr.bcm_ports)):
                ret, result = pr.get_port_prbs_result("mac", i + 1)
                if ret == True:
                    if (i+1) in macprbsresult.get('error'):
                        macprbsresult.get('error').remove((i+1))
                        macprbsresult.get('success').append((i+1))
                else:
                    if retrytime == (totalretrys -1):
                        total_err -= 1
                        caseerror.append({"name":"端口%03d"%(i + 1), "error":str(result)})
                        log_debug("mac 端口%03d error:%s" % ((i + 1), str(result)))
            if retrytime == (totalretrys -1):
                testerror1['errmsg'] = caseerror


            caseerror=[]
            for i in range(len(pr.bcm_ports)):
                ret, result = pr.get_port_prbs_result("sys", i + 1)
                if ret == True:
                    if (i+1) in sysprbsresult.get('error'):
                        sysprbsresult.get('error').remove((i+1))
                        sysprbsresult.get('success').append((i+1))
                else:
                    if retrytime == (totalretrys -1):
                        total_err -= 1
                        caseerror.append({"name":"端口%03d"%(i + 1), "error":str(result)})
                        log_debug("sys 端口%03d error:%s" % ((i + 1), str(result)))
            if retrytime == (totalretrys -1):
                testerror2['errmsg'] = caseerror


            caseerror=[]
            for i in range(len(pr.bcm_ports)):
                ret, result = pr.get_port_prbs_result("line", i + 1)
                if ret == True:
                    if (i+1) in lineprbsresult.get('error'):
                        lineprbsresult.get('error').remove((i+1))
                        lineprbsresult.get('success').append((i+1))
                else:
                    if retrytime == (totalretrys -1):
                        total_err -= 1
                        caseerror.append({"name":"端口%03d"%(i + 1), "error":str(result)})
                        log_debug("line 端口%03d error:%s" % ((i + 1), str(result)))
            if retrytime == (totalretrys -1):
                testerror3['errmsg'] = caseerror

            ret,log = pr.clear_port_prbs()
            if ret == False:
                raise Exception("prbs清除 %s" % log)
            time.sleep(10)

            if retrytime == (totalretrys -1):
                result_t.append(testerror1)
                result_t.append(testerror2)
                result_t.append(testerror3)
        retrytime += 1

    if len(macprbsresult.get('error')) == 0:
        RJPRINT("mac  prbs测试结果: PASS")
    else:
        RJPRINT("mac  prbs测试结果: FAIL")
        port_totalprint(macprbsresult.get('error'),"failed")

    if len(sysprbsresult.get('error')) == 0:
        RJPRINT("sys  prbs测试结果: PASS")
    else:
        RJPRINT("sys  prbs测试结果: FAIL")
        port_totalprint(sysprbsresult.get('error'),"failed")

    if len(lineprbsresult.get('error')) == 0:
        RJPRINT("line prbs测试结果: PASS")
    else:
        RJPRINT("line prbs测试结果: FAIL")
        port_totalprint(lineprbsresult.get('error'),"failed")

    if total_err < 0:
        return False , result_t
    return True ,""

# 端口prbs
def test_port_prbs():
    ret_t = 0
    #取端口
    porttest = PortTest()
    len_t = len(porttest.bcm_ports)
    errmsg = []
    upports = []
    successport=[]
    updownerrport=[]
    errorport = []
    try:
        #获取端口UP/DOWN状态
        for i in range(len_t):
            status = porttest.get_port_status(i + 1)
            if status == "up":
                upports.append(i + 1)
            else:
                updownerrport.append(i+1)
        log_debug(",".join(str(index) for index in upports))
        if len(updownerrport) > 0:
            ret_t -= 1
            pass
        else:
            porttest.init_port_prbs()
            for i in range(len_t):
                porttest.set_port_prbs(i + 1, 1)
            time.sleep(5)
            #取值
            for i in range(len_t):
                log_debug("端口prbs校验:%d"% (i + 1))
                ret  = porttest.get_port_prbs_result(i + 1)
                if ret == 0:
                    successport.append(i + 1)
                else:
                    errorport.append(i + 1)
                    ret_t -= 1
            #全部设值UP端口PRBS
    except Exception as e:
        msg = traceback.format_exc()
        log_error(msg)
        ret_t  = -1
        return False , msg
    finally:
        for i in range(len_t):
            porttest.set_port_prbs(i + 1, 0)
        porttest.reset_port_prbs()
        time.sleep(5)
    result_str = ''
    result_str += print_to_str(successport, "OK")
    result_str += print_to_str(updownerrport, "up/down error")
    result_str += print_to_str(errorport, "failed")
    if ret_t < 0:
        return False , result_str
    return True ,result_str


# 端口广播测试
def test_port():
    #errt_t = []
    ret_t = 0
    porttest = PortTest()
    # 取端口
    len_t = len(porttest.bcm_ports)

    successport=[]
    updownerrport=[]
    errorport = []
    upports = []
    try:
        #获取端口UP/DOWN状态
        for i in range(len_t):
            status = porttest.get_port_status(i + 1)
            if status == "up":
                upports.append(i + 1)
            else:
                updownerrport.append(i+1)
        if len(updownerrport) > 0:
            ret_t -= 1
            pass
        else:
            #所有端口都要up才进行测试，通过第一个端口发广播包
            log_debug("发送广播报文...")
            ret = porttest.start_send_port_packets(1, 10000)
            ###等待时间
            time.sleep(GRTD_BROADCAST_RETRY_SLEEP_TIME)
            log_debug("等待结果......")
            for i in range(len_t):
                ret , fcs = porttest.get_port_fcs_status(i + 1)
                if ret == True and fcs[0] == 0 and fcs[1] == 0:
                    successport.append(i + 1)
                else:
                    ret_t -= 1
                    errorport.append(i + 1)
                    log_debug("error: 端口%d  发送校验：%d  接收校验 %d" %( (i + 1), fcs[0], fcs[1]) )
    except Exception as e:
        msg = traceback.format_exc()
        log_error(msg)
        ret_t  = -1
        return False , msg
    finally:
        #关闭广播
        sta = porttest.stop_send_port_packets()
        time.sleep(5)
    result_str = ''
    result_str += print_to_str(successport, "OK")
    result_str += print_to_str(updownerrport, "up/down error")
    result_str += print_to_str(errorport, "failed")
    if ret_t < 0:
        return False , result_str
    return True ,result_str

def startFanctrol():
    if STARTMODULE['fancontrol'] == 1:
        cmd = "nohup fancontrol.py start >/dev/null 2>&1 &"
        rets = getPid("fancontrol.py")
        if len(rets) == 0:
            os.system(cmd)
    if "hal_fanctrl" in STARTMODULE and STARTMODULE['hal_fanctrl'] ==1:
        cmd = "nohup hal_fanctrl.py start >/dev/null 2>&1 &"
        rets = getPid("hal_fanctrl.py")
        if len(rets) == 0:
            os.system(cmd)

def startProcess(process_name, delay = 3):
    rets = getPid(process_name)
    if len(rets) == 0:
        os.system("supervisorctl start %s" % process_name)
    time.sleep(delay)
    rets = getPid(process_name)
    if len(rets) != 0:
        return True
    else:
        return False

def start_sfp_highest_temperatue():
    ret = startProcess("sfp_highest_temperatue", 0)
    if ret:
        return True, "start sfp_highest_temperatue succeed"
    else:
        return False, "start sfp_highest_temperatue fail"

def stop_sfp_highest_temperatue():
    ret = stopProcess("sfp_highest_temperatue")
    if ret:
        return True, "stop sfp_highest_temperatue succeed"
    else:
        return False, "stop sfp_highest_temperatue fail"

def start_hal_ledctrl():
    ret = startProcess("hal_ledctrl.py", 0)
    if ret:
        return True, "start hal_ledctrl succeed"
    else:
        return False, "start hal_ledctrl fail"

def getUsbLocation():
    dir = "/sys/block/"
    spect = "sd"
    usbpath = ""
    result = searchDirByName(spect, dir)
    if len(result) <= 0:
        return False
    for item in result:
        with open(os.path.join(item, "removable"), 'r') as fd:
            value = fd.read()
            if value.strip() == "1":  # 表示找到U盘
                usbpath = item
                break
    if usbpath == "":  # 没找到U盘
        log_debug("no usb found")
        return False, usbpath
    return True, usbpath

def searchDirByName(name, dir):
    result = []
    try:
        files = os.listdir(dir)
        for file in files:
            if name in file:
                result.append(os.path.join(dir, file))
    except Exception as e:
        pass
    return result



def getusbinfo():
    ret, path = getUsbLocation()
    if ret == False:
        return False, "not usb exists"
    str = os.path.join(path, "size")
    ret, value = getfilevalue(str)
    if ret == True:
        return True, {"id": os.path.basename(path), "size": float(value) * 512 / 1024 / 1024 / 1024}
    else:
        return False, "Err"


def stopFanctrol():
    '''关闭风扇定时服务'''
    if STARTMODULE['fancontrol'] == 1:
        rets = getPid("fancontrol.py")  #
        for ret in rets:
            cmd = "kill "+ ret
            os.system(cmd)
        time.sleep(3)
        return True
    if "hal_fanctrl" in STARTMODULE and STARTMODULE['hal_fanctrl'] ==1:
        rets = getPid("hal_fanctrl.py")  #
        for ret in rets:
            cmd = "kill "+ ret
            os.system(cmd)
        time.sleep(3)
        return True

def stopProcess(process_name, delay=3):
    os.system("supervisorctl stop %s" % process_name)
    time.sleep(delay)
    rets = getPid(process_name)
    if len(rets) == 0:
        return True
    else:
        return False

def stop_hal_ledctrl():
    ret = stopProcess("hal_ledctrl.py")
    if ret:
        return True, "stop hal_ledctrl succeed"
    else:
        return False, "stop hal_ledctrl fail"


# ====================================
# 测试项:CPLD版本检验
# ====================================
def test_cpldversion():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    ret, log = log_os_system("which grtd_test.py", 0)
    if len(log):
        cmd = "cmd find "
    else:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "    [FAILED]:no grtd_test.py found"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    ret, log = log_os_system("grtd_test.py sys cpld_version", 0)
    log_debug(log)
    if ret or ("Error" in log ):
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = log
        RJPRINT("    [FAILED]:CPLD版本读取失败")
    else:
        RJPRINT(log)
    return RET


def test_cpu_stress_stop():
    RET = {RETURN_KEY1 : 1, RETURN_KEY2 : ""}
    ret, log = rj_os_system("ps -ef | grep \"%s\"| grep -v grep" % CpuStressCmd)
    if ret == 0:
        ret, log = log_os_system("ps -ef | grep \"%s\" | grep -v grep | awk '{print $2}' | xargs kill -9 " % CpuStressCmd, 0)
        if ret or len(log):
            RET[RETURN_KEY2] = "取消压力测试异常:%s"%log
        else:
             RET[RETURN_KEY2] = "该后台测试已被终止"
    else:
        RET[RETURN_KEY2] = "未启动后台测试"
    RJPRINT(RET[RETURN_KEY2])
    return RET

# ====================================
# 测试项:BMC FRU/TLV E2PROM信息获取测试
# ====================================
def test_show_bmc_fru_eeprom():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    try:
        tmp = TESTCASE.get('bmce2loc')
        loc = tmp.get("fru",None)
        ret = test_get_bmc_eeprom(loc)
        if ret[RETURN_KEY1] < 0 :
            RJPRINT("读取BMC-FRU-E2失败")
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = ret[RETURN_KEY2]
            return RET
        eeprom = ret[RETURN_KEY2]
        bmcfru = ipmifru()
        bmcfru.decodeBin(eeprom)
        RJPRINT(bmcfru.boardInfoArea)
    except Exception as e:
        RJPRINT(str(e))
        RET[RETURN_KEY1] -= 1
        RET[RETURN_KEY2] = str(e)
    return RET

def test_show_bmc_tlv_eeprom():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    eeprom = ""
    totalerr = 0
    params = {}
    try:
        tmp = TESTCASE.get('bmce2loc')
        loc = tmp.get("tlv",None)
        ret = test_get_bmc_eeprom(loc)
        if ret[RETURN_KEY1] < 0:
            RJPRINT("读取BMC-TLV-E2失败")
            RET[RETURN_KEY1] = -1
            return RET
        eeprom = ret[RETURN_KEY2]
        onietlv = onie_tlv()
        rets    = onietlv.decode(eeprom)
        RJPRINT("%-20s %-5s %-5s  %-20s" % ("TLV name","Code","lens","Value"))
        for item in rets:
            if item["code"] == 0xfd:
                RJPRINT("%-20s 0x%-02X   %-5s" % (item["name"],item["code"],item["lens"]))
            else:
                RJPRINT("%-20s 0x%-02X   %-5s %-20s" % (item["name"],item["code"],item["lens"],item["value"]))
        RJPRINT("")
    except Exception as e:
        RJPRINT(str(e))
        totalerr -= 1
    if totalerr < 0:
        RET[RETURN_KEY1] = -1
    return RET

def test_get_bmc_eeprom(loc):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    params = {}
    eeprom = ""
    params["loc"]  = loc
    func = "test_bmc_read_eeprom"
    try:
        ret = test_bmc_func(func,params)
        if ret[RETURN_KEY1] < 0:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = ret[RETURN_KEY2]
            return RET
        value = ret.get("value","")
        for i in value:
            eeprom += chr(i)
        RET[RETURN_KEY2] = eeprom
    except Exception as e:
        RET[RETURN_KEY1] -= 1
        RET[RETURN_KEY2] = str(e)
    return RET


# ====================================
# 测试项:USB测试
# ====================================
def test_usb():
    ret , info = getusbinfo();
    if ret == True:
        RJPRINT("%s %s"%("-"*6,"-"*20))
        RJPRINT("{id}    {size}G".format(**info))
        return {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    else:
        log_debug(info)
        RJPRINT("读取USB信息失败")
    return {RETURN_KEY1 : -1,  RETURN_KEY2 : "读取USB信息失败"}



def test_usb2(test_times = 1):
    totalerr = 0
    errmsg = ""
    RET = test_usb()
    if RET[RETURN_KEY1] == -1:
       return RET
    #print_clean()#防止打印test_usb的内容
    ret,info = getusbinfo()
    usb_dev = info["id"]
    cmd = "fdisk -l |grep '%s'|grep 'Disk' -v|sort -k4 |tail -n1|awk '{print $1;}'"%usb_dev
    ret, usb_disk = log_os_system(cmd,0)
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    #生成测试文件
    ret, log = log_os_system("dd if=/dev/random of=/tmp/file.txt bs=1M count=10", 0)
    ret, log = log_os_system("mkdir /tmp/usb_stress_test && mount  %s /tmp/usb_stress_test/"%usb_disk, 0)
    if ret != 0 or len(log) > 0:
        RJPRINT(log)
        RJPRINT("挂载U盘   FAILED")
        totalerr -= 1
    else:
        for i in range(0, test_times):
            if test_times != 1:
                RJPRINT("\n\n第 %d/%d 次测试"%(i+1, test_times))

            cmd = 'cp -rf /tmp/file.txt /tmp/usb_stress_test/file.txt'
            ret, log = log_os_system(cmd,0)
            if ret != 0 or len(log) > 0:
                RJPRINT( log)
                RJPRINT( "拷贝文件   FAILED")
                totalerr -= 1
            else:
                RJPRINT( "拷贝文件   PASS")

            cmd = 'diff /tmp/file.txt /tmp/usb_stress_test/file.txt'
            ret, log = log_os_system(cmd,0)
            if ret != 0 or len(log) > 0:
                RJPRINT( "校验文件   FAILED")
                totalerr -= 1
            else:
                RJPRINT( "校验文件   PASS")

            cmd = 'rm -rf /tmp/usb_stress_test/file.txt'
            ret, log = log_os_system(cmd,0)
            if ret != 0 or len(log) > 0:
                RJPRINT( log)
                RJPRINT( "删除文件   FAILED")
                totalerr -= 1
            else:
                RJPRINT( "删除文件   PASS")

    ret, log = log_os_system("umount /tmp/usb_stress_test", 0)
    ret, log = log_os_system("rm /tmp/usb_stress_test -r", 0)
    ret, log = log_os_system("rm /tmp/file.txt", 0)
    if totalerr < 0:
        RET[RETURN_KEY1] = -1
    return RET

def test_usb_stress():
    return test_usb2(10)


def test_bmc_setmac():
    while bmc_setmac() == False:
        pass
    return {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}

def test_e2_setmac():
    ret = fac_board_setmac()
    if ret == True:
        return {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    else:
        RJPRINT("E2SETMAC失败")
    return {RETURN_KEY1 : -1,  RETURN_KEY2 : "E2SETMAC失败"}

# ====================================
# 测试项:风扇setmac
# ====================================
def test_fan_setmac():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    try:
        stopFanctrol()
        if(fac_fans_setmac() == False):
            totalerr -= 1
    except Exception as e:
        RJPRINTERR(e)
        totalerr -= 1
    finally:
        startFanctrol()
    RET[RETURN_KEY1] = totalerr
    return RET

pidfile = 0
############################################################################################
##  文件锁
############################################################################################
def ApplicationInstance():
    global pidfile
    pidfile = open(os.path.realpath(__file__), "r")
    try:
        fcntl.flock(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB) #创建一个排他锁,并且所被锁住其他进程不会阻塞
    except:
        RJPRINT("已有一个程序在运行...."  )
        sys.exit(1)

def fac_init_setmac():
    if getsyseeprombyId(TLV_CODE_PRODUCT_NAME) == None or getsyseeprombyId(TLV_CODE_SERIAL_NUMBER) == None or\
       getsyseeprombyId(TLV_CODE_MAC_BASE) == None or getsyseeprombyId(TLV_CODE_DEVICE_VERSION) == None :
        log_debug("需要重新setmac")
        return False
    return True

def fac_sensors_kill():
    cmd = "docker exec pmon  ps -ef | grep sensord | grep -v grep"
    cmdstr = "docker exec pmon  ps -ef | grep sensord | grep -v grep | cut -c 9-15 | xargs docker exec pmon kill -s 9"
    try:
        log_debug("正在停止sensord服务")
        ret, status = rj_os_system(cmd)
        if ret != 0:
            log_debug("sensord服务未启动")
            return
        ret, status = rj_os_system(cmdstr)
        if ret != 0:
            RJPRINT("停止sensord服务异常，请确认")
    except:
        pass

def test_mac_memtest():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    for test_item in TESTCASE.get("MAC_MEMTEST_TEST", None):
        test_name = test_item.get("test_name", None)
        RJPRINT("%s:" % test_name)

        commands = test_item.get("commands", None)
        for command in commands:
            cmd = command.get("cmd")
            sleep_time = command.get("sleep", 0)
            ret, msg = rj_os_system(cmd)
            if sleep_time != 0:
                time.sleep(sleep_time)
        #由于每个项执行时间太久，回显超时，单独判断无意义直接PASS
        RJPRINT("    %s：pass" % (test_name))
        judge = test_item.get("judge", None)
        if judge is not None:
            cmd = "bcmcmdb \"dsh -c 'tl pt'\" |grep TOTAL"
            ret, log = log_os_system(cmd, True)
            if ret != 0 or ("0" not in log):
                cmd = "bcmcmdb \"dsh -c 'tl pt'\" "
                ret, log = rj_os_system(cmd)
                RJPRINT("    %s" % (log))
                RET[RETURN_KEY1] -= 1
    RJPRINT("")
    RJPRINT("测试完成，请重启设备")
    return RET

def test_avs_set(param):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    for test_item in TESTCASE.get(param, None):
        test_name = test_item.get("test_name", None)
        RJPRINT("%s" % test_name)

        avs_file = test_item.get("location", None)
        with open(avs_file, 'r') as fd:
            val = fd.read()
        avs = int(val, 16)*1000/4096
        RJPRINT("    初始电压为%s, 转化十进制为%dmv" % (val,avs))
        mul = test_item.get("mul", None)
        avs_high = avs*mul
        RJPRINT("    调压后为%dmV" % avs_high)
        #设置电压
        commands = test_item.get("switch_page", None)
        ret, val = send_commands(commands, True)
        if ret == False:
            RJPRINT("%s：设置电压switch_page失败" % (test_item["avs_name"]))
            continue
        set_cmd = test_item.get("set_vol", None)
        set_avs = set_cmd % (avs_high*4096/1000)
        ret, val = log_os_system(set_avs, True)
        if ret == 0:
            time.sleep(1)
            get_cmd = test_item.get("get_vol", None)
            ret, val = log_os_system(get_cmd, True)
            RJPRINT("    调压成功，调整后电压十六进制为%s" % val)
        commands = test_item.get("recover_page", None)
        ret, val = send_commands(commands, True)
        if ret == False:
           RJPRINT("%s：设置电压recover_page失败" % (test_item["avs_name"]))
        RJPRINT("")
    return RET

def test_avs_set_normal():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    for test_item in TESTCASE.get("MAC_AVS_INIT_LIST", None):
        avs_name = test_item.get("avs_name", None)
        RJPRINT("恢复%s" % avs_name)

        avs_file = test_item.get("location", None)
        with open(avs_file, 'r') as fd:
            nor_avs = fd.read()
        avs = int(nor_avs, 16)*1000/4096
        RJPRINT("    初始电压为%s, 转化十进制为%dmv" % (nor_avs,avs))
        #设置电压
        commands = test_item.get("switch_page", None)
        ret, val = send_commands(commands, True)
        if ret == False:
            RJPRINT("恢复%s：switch_page失败" % (test_item["avs_name"]))
            continue
        set_cmd = test_item.get("set_vol", None)
        set_avs = set_cmd % nor_avs
        ret, val = log_os_system(set_avs, True)
        if ret == 0:
            time.sleep(1)
            get_cmd = test_item.get("get_vol", None)
            ret, val = log_os_system(get_cmd, True)
            RJPRINT("    调压成功，恢复后电压十六进制为%s" % val)
        commands = test_item.get("recover_page", None)
        ret, val = send_commands(commands, True)
        if ret == False:
           RJPRINT("恢复%s：recover_page失败" % (test_item["avs_name"]))
        RJPRINT("")
    return RET

def mac_avs_init():
    for avs_item in TESTCASE.get("MAC_AVS_INIT_LIST", None):
        avs_file = avs_item.get("location", None)
        cmd = "ls %s" % avs_file
        ret, val = log_os_system(cmd, False)
        if ret or "No such file" in val:
            cmd = "touch %s" % avs_file
            log_os_system(cmd, 0)
            #获取初始电压
            commands = avs_item.get("switch_page", None)
            ret, val = send_commands(commands, True)
            if ret == False:
                RJPRINT("%s获取初始电压switch_page失败" % (avs_item["avs_name"]))
                cmd = "rm %s" % avs_file
                log_os_system(cmd, 0)
                continue
            command = avs_item.get("get_vol", None)
            ret, val = log_os_system(command, True)
            if ret == 0:
                with open(avs_file, 'w') as f:
                    f.write(val)
            else:
                RJPRINT("%s获取初始电压失败" % (avs_item["avs_name"]))
                cmd = "rm %s" % avs_file
                log_os_system(cmd, 0)
            commands = avs_item.get("recover_page", None)
            ret, val = send_commands(commands, True)
            if ret == False:
               RJPRINT("%s获取初始电压recover_page失败" % (avs_item["avs_name"]))

def fac_init():
    global DIAGTEST
    firmware_check()         # 固件检测
    if DIAGTEST is False: # 由ATE自行进入菜单setMac,保持一致性
        fac_setmac_check()   # setmac检查
    waitForSDK()             # 等待SDK
    closeProtocol()          # 关闭协议
    if FACTESTMODULE.get("sensord", 0) == 1: # sensord后台进程
        fac_sensors_kill()
    if FACTESTMODULE.get("firmware_init", 0) == 1: # 固件初始化
        fac_firmware_init()
    if FACTESTMODULE.get("usb0_config", 0) == 1 and bmc_presence_check(): # USB0 IP配置
        ret_t = usb0_init()
        if ret_t is False:
            RJPRINT("配置SONIC端USB网口失败，请手动配置")
    if FACTESTMODULE.get("mac_avs_init", 0) == 1: # MAC电压默认值初始化
        mac_avs_init()
    if bmc_presence_check():
        ret_t = False
        for i in range(0, 60):
            ret, log = test_bmc_channel()
            if ret is False:
                time.sleep(1)
            else:
                ret_t = True
                break
        if ret_t is False:
            RJPRINT("到BMC通路失败，请确认！")
    if bmc_presence_check() and TESTCASE.get("ETH0_IP", None) is not None:
        x86_start_iperf3_server()
        bmc_start_iperf3_server()
    RJPRINT("")
def fac_init_check_ipmi():
    if not os.path.exists("/dev/ipmi0"):
        ret, log = log_os_system("rmmod ipmi_watchdog; rmmod ipmi_si; modprobe ipmi_msghandler; modprobe ipmi_si trydefaults=1 tryacpi=1;modprobe ipmi_devintf", 0)
        if not os.path.exists("/dev/ipmi0"):
            msg ="     无/dev/ipmi0设备,请检查"
            RJPRINT(msg)
            return False
    return True

def fac_setmac_check():
    # 板卡ID检测
    if fac_init_cardidcheck() == False:
        RJPRINTERR("\n\n板卡ID检测失败，请确认!\n\n")
        sys.exit(-1);

    # setmac检测
    if fac_init_setmac() is False:
        RJPRINT("未检测到SETMAC信息, 请先进入系统配置执行E2SETMAC")

def io_rd(reg_addr, read_len=1):
    try:
        regaddr = 0
        if isinstance(reg_addr, int):
            regaddr = reg_addr
        else:
            regaddr = int(reg_addr, 16)
        devfile = "/dev/port"
        fd = os.open(devfile, os.O_RDWR | os.O_CREAT)
        os.lseek(fd, regaddr, os.SEEK_SET)
        val = os.read(fd, read_len)
        return "".join(["%02x" % item for item in val])
    except ValueError:
        return None
    except Exception as e:
        print(e)
        return None
    finally:
        os.close(fd)


def io_wr(reg_addr, reg_data):
    try:
        regdata = 0
        regaddr = 0
        if isinstance(reg_addr, int):
            regaddr = reg_addr
        else:
            regaddr = int(reg_addr, 16)
        if isinstance(reg_data, int):
            regdata = reg_data
        else:
            regdata = int(reg_data, 16)
        devfile = "/dev/port"
        fd = os.open(devfile, os.O_RDWR | os.O_CREAT)
        os.lseek(fd, regaddr, os.SEEK_SET)
        os.write(fd, regdata.to_bytes(1, 'little'))
        return True
    except ValueError as e:
        print(e)
        return False
    except Exception as e:
        print(e)
        return False
    finally:
        os.close(fd)


def getBMCMAC():
    cmd = "ipmitool lan print 1 | grep 'MAC Address'"
    ret , status = rj_os_system(cmd)
    if ret == 0:
        return status[status.index(":") + 1:len(status)].strip().upper()
    else:
        RJPRINTERR("获取BMC MAC失败[%s]" % status)
        return None

def checkkallsyms(name):
    symsisexistcmd = "cat /proc/kallsyms | grep %s | wc -l" % name
    status, output = log_os_system(symsisexistcmd, 0)
    #系统执行错误
    if status:
        return False
    if output.isdigit() and int(output) > 0:    #符号存在
        return True
    else:
        return False

def checksignaldriver(name):
    modisexistcmd = "lsmod | grep %s | wc -l" % name
    status, output = log_os_system(modisexistcmd, 0)
    #系统执行错误
    if status:
        return False
    if output.isdigit() and int(output) > 0:
        return True
    else:
        return False

def adddriver(name, delay):
    cmd = "modprobe %s" % name
    if checksignaldriver(name) != True:
        log_os_system(cmd, 0)
        if delay != 0:
            time.sleep(delay)
            log_debug('%s sleep %d second!' %(name,delay))

def removedriver(name, delay):
    realname = name.lstrip().split(" ")[0];
    cmd = "rmmod -f %s" % realname
    if checksignaldriver(realname):
        log_os_system(cmd, 0)
        if delay != 0:
            time.sleep(delay)
            log_debug('%s sleep %d second!' %(name,delay))
'''
#管理口速率切换测试中，发送包方式选择
def test_mgmt_packet_send(issonic = True,packet_count = 2000):
    if issonic:
        sendp(Ether(dst='FF:FF:FF:FF:FF:FF',src='00:00:00:00:00:03')/ARP(op=1), iface='eth0', count=packet_count)
    else:
        cmd = "ssh root@240.1.1.1 'export %s && ftg100_tool tx %d'"%(BMC_PATH,packet_count)
        ret, log = password_command(cmd,OPENBMC_PASSWORD)
        if "packet" not in log:
            raise Exception,"发送数据包出错:\n"+log
        time.sleep(3)
'''

def print_to_str(arr, tips):
    return_str = ''
    alias = TESTCASE.get('port_alias',None)
    if len(arr) <= 0:
        return_str += "\n"
        return return_str
    return_str += "%-20s" % tips
    for index in range(len(arr)):
        if alias is not None:
            return_str += ("%s" % alias.get(arr[index],"unkowned"))
        else:
            return_str += ("%03d" % arr[index])
        return_str +=(" ")  #加个空格
        if (index + 1) % 8 == 0:
            return_str += "\n"
            return_str += (" " * 20)
    return_str += "\n"
    return return_str

def port_totalprint(arr, tips):
    '''按照格式打印输出(还要附带转码)'''
    alias = TESTCASE.get('port_alias',None)
    if len(arr) <= 0:
        return
    RJPRINTLINE("%-20s" % tips)
    for index in range(len(arr)):
        if alias is not None:
            RJPRINTLINE("%s" % alias.get(arr[index],"unkowned"))
        else:
            RJPRINTLINE("%03d" % arr[index])
        if (index + 1) % 8 == 0:
            RJPRINT("")
            RJPRINTLINE(" " * 20)
    RJPRINT("")

def getmgmtrx():
    mgmtrxloc = "/eth0/statistics/rx_packets"
    value_t = get_pmc_register(mgmtrxloc)
    return int(value_t,10)


# ==============================================
# MGMT网口测试
# ==============================================
def test_mgmt_speed(speed , bmctest ):
    MGMT_LPBK_CMD  = ("ethtool -s eth0 speed %d duplex full autoneg on" % speed)    # MGMT自环网口设置命令
    MGMT_LINK_CHK_CMD  = "mii-tool eth0"    # MGMT网口自环头连接成功判断命令
    LINK_CHK_KEY = "link ok"    # MGMT网口自环头连接成功log判定关键字
    MGMT_LPBK_1000M_EN_CMD  = "echo 1 > /sys/class/lpbk_1000m/enable"    # 使能MGMT自环网口配置:1000M
    MGMT_LPBK_1000M_DIS_CMD = "echo 0 > /sys/class/lpbk_1000m/enable"    # 关闭MGMT自环网口配置:1000M
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    try:
        PACKET_NUM = TESTCASE.get('mgmt').get("packetcount")
        retrytimes = TESTCASE.get('mgmt').get("retrytimes",5)
        # MGMT:自环网口设置
        if speed == 1000:
            ret, log = log_os_system(MGMT_LPBK_1000M_EN_CMD, 0)
            if ret != 0:
                RJPRINT("1000m: %s 命令运行错误   [FAIL]" % MGMT_LPBK_1000M_EN_CMD)
                RET = {RETURN_KEY1 : -1, RETURN_KEY2 : "Error: 1000M自环网口设置命令出错\n"}
                return RET
        else:
            ret, log = log_os_system(MGMT_LPBK_CMD, 0)
            if ret != 0:
                RJPRINT("%dM: %s 命令运行错误   [FAIL]" % (speed,MGMT_LPBK_CMD))
                RET = {RETURN_KEY1 : -1, RETURN_KEY2 : ("Error: %dM自环网口设置命令出错\n" % speed)}
                return RET
        # MGMT网口自环头连接成功判断
        time.sleep(1)
        for i in range(10):
            ret, log = log_os_system(MGMT_LINK_CHK_CMD, 0)
            if ret != 0:
                RJPRINT("%dM: %s 命令运行错误   [FAIL]" % (speed,MGMT_LINK_CHK_CMD))
                RET = {RETURN_KEY1 : -1, RETURN_KEY2 : ("Error: %dM自环头连接成功命令出错\n" % speed)}
                return RET
            if LINK_CHK_KEY not in log:
                time.sleep(1)
                continue
            # MGMT自环头连接 up 成功,开始发包,获取端口收发信息
            RJPRINT("MGMT测试 speed:%dM" % speed)
            # X86端收发包测试
            for i in range(retrytimes):
                message = ''
                totalerr = 0
                RXstart,TXstart = get_frame_count()
                test_mgmt_packet_send(packet_count = PACKET_NUM)
                RXend,TXend = get_frame_count()
                Tx_total = TXend - TXstart
                Rx_total = RXend - RXstart
                if Rx_total >= PACKET_NUM:    # 要考虑可能有其它进程往MGMT网口发包
                    message += "X86端确认: MGMT网口测试  [OK]\n"
                else:
                    totalerr -= 1
                    message += "X86端确认: [FAIL](packets=%d Tx_total=%d Rx_total=%d)\n" % (PACKET_NUM, Tx_total, Rx_total)
                # BMC端收发包测试
                if bmctest == True:
                    ret, log = bmc_test_mgmt_speed()
                    totalerr += ret
                    message += log
                RET[RETURN_KEY2] += message
                if totalerr == 0:
                    RJPRINT(message)
                    return RET
            RJPRINT(message)
            RET[RETURN_KEY1] = -1
            return RET
        RJPRINT("%dM: MGMT自环头连接 up 失败  [FAIL]" % speed)
        RET = {RETURN_KEY1 : -1, RETURN_KEY2 : ("FAIL: %dM自环头连接 up 失败\n" % speed)}
    except Exception as e:
        RJPRINT(str(e))
        RET[RETURN_KEY1] = -1
    finally:
        if speed == 1000:
            log_os_system(MGMT_LPBK_1000M_DIS_CMD, 0)
    return RET

def bmc_test_mgmt_speed():
    # BMC端收发包测试
    totalerr = 0
    message = ''
    bmccheck = TESTCASE.get('mgmt').get("bmccheck")
    try:
        ret = test_bmc_func(bmccheck.get('case'), bmccheck.get('param'))
        if ret.get(RETURN_KEY1) == 0:
            message += "BMC端确认: MGMT网口测试  [OK]"
        else:
            totalerr -= 1
            message += "BMC端确认: [FAIL]%s \n" % ret.get(RETURN_KEY2)

    except Exception as e:
        message += str(e) + "\n"
        totalerr -= 1
    finally:
        return totalerr, message

def test_mgmt_loopback_new_noconfirm():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    ret_t = test_mgmt_loop_new_real('10M')
    RET[RETURN_KEY1] += ret_t.get(RETURN_KEY1)
    RET[RETURN_KEY2] += ret_t.get(RETURN_KEY2)

    ret_t = test_mgmt_loop_new_real('100M')
    RET[RETURN_KEY1] += ret_t.get(RETURN_KEY1)
    RET[RETURN_KEY2] += ret_t.get(RETURN_KEY2)

    ret_t = test_mgmt_loop_new_real('1000M')
    RET[RETURN_KEY1] += ret_t.get(RETURN_KEY1)
    RET[RETURN_KEY2] += ret_t.get(RETURN_KEY2)
    return RET

def test_mgmt_loopback_new():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    ret = makesure("  !!!请确保登入的是串口终端!!!  自环工装是否插入[Yes/no]：", echo = 1)
    if ret != True:
        RET = {RETURN_KEY1 : -1, RETURN_KEY2 : "FAIL"}
        return RET

    return test_mgmt_loopback_new_noconfirm()

def test_mgmt_packet_send(iface1='eth0', packet_count = 2000):
    sendp(Ether(dst='FF:FF:FF:FF:FF:FF',src='00:00:00:00:00:03')/ARP(op=1), iface=iface1, count=packet_count,verbose=0)

def test_check_cpu_loopback(iface, packet_count, pktthread):
    RXstart,TXstart = get_frame_count(iface)
    test_mgmt_packet_send(iface1 = iface, packet_count = packet_count) #先发包
    RXend,TXend = get_frame_count(iface)
    Tx_total = TXend - TXstart
    Rx_total = RXend - RXstart
    log_debug("发送帧计数：%d，接收帧计数：%d"%(Tx_total,Rx_total))
    packet_rate = float(Rx_total)/float(Tx_total)
    if Rx_total >= packet_count  and Tx_total >= packet_count and packet_rate >= pktthread:
         return True,""
    return False, "发送帧计数：%d，接收帧计数：%d"%(Tx_total,Rx_total)


def get_frame_count(iface ='eth0'):
    txcmd = "ifconfig %s |grep -E 'TX packets'" % iface
    rxcmd = "ifconfig %s |grep -E 'RX packets'" % iface
    ret, txlog = log_os_system(txcmd, 0)
    ret, rxlog = log_os_system(rxcmd, 0)
    tx = re.findall(r"\d+\.?\d*",txlog)[0]
    rx = re.findall(r"\d+\.?\d*",rxlog)[0]
    return int(rx), int(tx)

def test_mgmt_loop_new_real(speed):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    http = TESTCASE.get('mgmt').get(speed)
    http2 = TESTCASE.get('mgmt').get('clear')
    bcmcheckk = TESTCASE.get('mgmt').get('bmccheck')
    iface = TESTCASE.get('mgmt').get('iface')
    pk_count = TESTCASE.get('mgmt').get('packetcount')
    pktthread = TESTCASE.get('mgmt').get('pktpassthread')
    retrytimes = TESTCASE.get('mgmt').get('retrytimes', 1)

    RJPRINT("MGMT测试 speed:%s" % speed)
    RJPRINT("----------------------")
    for i in range(retrytimes):
        totalerr = 0
        errmsg = ""
        printmsg = ""
        try:
            ret = test_bmc_func(http2.get('case'),http2.get('param'))
            if ret is None:
                raise Exception('SONiC reset失败')
            if ret.get(RETURN_KEY1) != 0:
                totalerr += ret.get(RETURN_KEY1)
                errmsg  += ret.get(RETURN_KEY2)
                printmsg += errmsg + ' \n'
            time.sleep(0.5)
            ret = test_bmc_func(http.get('case'),http.get('param'))
            if ret is None:
                raise Exception('SONiC设置回环失败')
            time.sleep(0.5)
            if ret.get(RETURN_KEY1) != 0:
                totalerr += ret.get(RETURN_KEY1)
                errmsg  += ret.get(RETURN_KEY2)
                printmsg += errmsg + ' \n'
            else:
                val_check, errmsg = test_check_cpu_loopback(iface, pk_count, pktthread)
                printmsg += "SONiC端确认:"
                if val_check == True:
                    printmsg += " [ok] \n"
                else:
                    printmsg += "[failed] %s \n" % errmsg
                    if i  < (retrytimes -1):
                        continue
                printmsg += "BMC端确认:"
                ret = test_bmc_func(bcmcheckk.get('case'),bcmcheckk.get('param'))
                if ret is None:
                    raise Exception('BMC端确认失败')
                if ret.get(RETURN_KEY1) == 0:
                    printmsg +="[ok] \n"
                else:
                    totalerr += ret.get(RETURN_KEY1)
                    errmsg  += ret.get(RETURN_KEY2)
                    printmsg += "[failed] %s \n" % ret.get(RETURN_KEY2)
                    if i  < (retrytimes -1):
                        continue
        except Exception as e:
            totalerr = -998
            RET[RETURN_KEY1] = -999
            RET[RETURN_KEY2] += str(e)
            printmsg += str(e) + ' \n'
        finally:
            ret = test_bmc_func(http2.get('case'),http2.get('param'))
            time.sleep(0.5)
        if totalerr >=0:
            break
    RJPRINT(printmsg)
    RET[RETURN_KEY1] = totalerr
    RET[RETURN_KEY2] = errmsg
    return RET

# ==============================================
# MGMT网口测试
# ==============================================
def test_mgmt():
    bmctest = True
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}

    #MGMT 自环工装插入确认
    ret = makesure("  !!!请确保登入的是串口终端!!!  自环工装是否插入[Yes/no]：", echo = 1)
    if ret != True:
        RET = {RETURN_KEY1 : -1, RETURN_KEY2 : "FAIL"}
        return RET
    if "mgmttest" in FACTESTMODULE and FACTESTMODULE['mgmttest'] == 1:
        if checkkallsyms("phy_backup_data") != True:
            removedriver("igb",1)
            adddriver("igb",2)
            log_os_system("ifconfig eth0 up", 0)
        adddriver("lpbk_1000m",1)
    status, msg = test_bmc_channel()
    if status == False:
        RJPRINT("到BMC通路异常，无法测试BMC端NCSI通路")
        RET[RETURN_KEY1] -= 1
        bmctest = False
    ret_t = test_mgmt_speed(10 , bmctest)
    RET[RETURN_KEY1] += ret_t.get(RETURN_KEY1)
    RET[RETURN_KEY2] += ret_t.get(RETURN_KEY2)

    ret_t = test_mgmt_speed(100 , bmctest)
    RET[RETURN_KEY1] += ret_t.get(RETURN_KEY1)
    RET[RETURN_KEY2] += ret_t.get(RETURN_KEY2)

    ret_t = test_mgmt_speed(1000 , bmctest)
    RET[RETURN_KEY1] += ret_t.get(RETURN_KEY1)
    RET[RETURN_KEY2] += ret_t.get(RETURN_KEY2)

    time.sleep(5)
    return RET


# ==============================================
# MGMT网口拷机测试
# ==============================================
def test_mgmt_loop():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    bmctest = True
    if "mgmttest" in FACTESTMODULE and FACTESTMODULE['mgmttest'] == 1:
        if checkkallsyms("phy_backup_data") != True:
            removedriver("igb",1)
            adddriver("igb",2)
            log_os_system("ifconfig eth0 up", 0)
        adddriver("lpbk_1000m",1)
    if bmc_presence_check():
        status, msg = test_bmc_channel()
        if status == False:
            RJPRINT("到BMC通路异常，无法测试BMC端NCSI通路")
            RET[RETURN_KEY1] -= 1
            bmctest = False
    else:
        bmctest = False
    ret_t = test_mgmt_speed(10 , bmctest)
    RET[RETURN_KEY1] += ret_t.get(RETURN_KEY1)
    RET[RETURN_KEY2] += ret_t.get(RETURN_KEY2)

    ret_t = test_mgmt_speed(100 , bmctest)
    RET[RETURN_KEY1] += ret_t.get(RETURN_KEY1)
    RET[RETURN_KEY2] += ret_t.get(RETURN_KEY2)

    ret_t = test_mgmt_speed(1000 , bmctest)
    RET[RETURN_KEY1] += ret_t.get(RETURN_KEY1)
    RET[RETURN_KEY2] += ret_t.get(RETURN_KEY2)

    time.sleep(5)
    return RET



def diff_pcie():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    ret, log = log_os_system("lspci -n", 0)
    pci_list = log.split("\n")
    if len(pci_list) != len(PCIe_DEV_LIST):
        RET[RETURN_KEY2] = "Error: PCIe devices is not equal, lspci device number: %d, configuration file device number: %d\n" % (len(pci_list),len(PCIe_DEV_LIST))
        log_debug("Error: PCIe devices is not equal, lspci device number: %d, configuration file device number: %d\n" % (len(pci_list),len(PCIe_DEV_LIST)))
    pci_dict = {}
    for pci in pci_list:
        pci_item = pci.split(" ")
        pci_dict[pci_item[0]] = pci_item[2]
    try:
        for dev in PCIe_DEV_LIST:
            if dev["pci_addr"] not in pci_dict:
                RET[RETURN_KEY2] += "Error: PCIe device not found. PCIe addr = %s,device ID = %s\n" % (dev["pci_addr"],dev["dev_id"])
                log_debug("Error: PCIe device not found. PCIe addr = %s,device ID = %s\n" % (dev["pci_addr"],dev["dev_id"]))
                if dev.get("ignore",0) == 1:    # 规避百度BIOS切换导致2个设备扫不到
                    pass
                else:
                    RET[RETURN_KEY1] -= 1
            elif dev["dev_id"] != pci_dict[dev["pci_addr"]]:
                RET[RETURN_KEY1] -= 1
                RET[RETURN_KEY2] += "Error: PCIe device ID is not equal. PCIe addr: %s, configuration file device ID: %s, lspci device ID: %s\n"% (dev["pci_addr"],dev["dev_id"],pci_dict[dev["pci_addr"]])
                log_debug("Error: PCIe device ID is not equal. PCIe addr: %s, configuration file device ID: %s, lspci device ID: %s\n"% (dev["pci_addr"],dev["dev_id"],pci_dict[dev["pci_addr"]]))
                del pci_dict[dev["pci_addr"]]
            else:
                del pci_dict[dev["pci_addr"]]
        for pci_addr, dev_id in sorted(pci_dict.items()):
            RET[RETURN_KEY1] -= 1
            RET[RETURN_KEY2] += "Error: The PCIe device scanned by lspci is not in the configuration file.PCIe addr = %s,device ID = %s\n" % (pci_addr, dev_id)
            log_debug("Error: The PCIe device scanned by lspci is not in the configuration file.PCIe addr = %s,device ID = %s\n" % (pci_addr, dev_id))
    except Exception as e:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = str(e)
        log_debug(str(e))

    return RET

def check_pcie_speed():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    errmsg = ""
    try:
        for pci in PCIe_SPEED_ITEM:
            ret, log = log_os_system("lspci|grep %s"%pci["PCIe_name"], 0)
            if pci["PCIe_name"] in log:
                result_t = log.split(" ")
                vvcmd = "lspci -s %s -vvv | grep LnkSta | grep Width" % result_t[0]
                ret2, log2 = log_os_system(vvcmd, 0)
                filted_list = re.findall(r".*(speed.*, width.*).*",log2.lower())
                if len(filted_list) > 0 :
                    value_list = filted_list[0].split(",")
                    checklist = pci.get("check",None)
                    if checklist is None:
                        RJPRINT("%-10s (%-13s, %s): PASS"%(pci["dev_desc"], value_list[0], value_list[1]))
                    else:
                        realdata = {"speed":"","width":""}
                        realdata["speed"] = value_list[0].strip().split(" ")[1].strip()
                        realdata["width"] = value_list[1].strip().split(" ")[1].strip()
                        for key,value in list(checklist.items()):
                            if realdata[key] != value:
                                totalerr -= 1
                                errmsg += "%s %s check error,correct value is :%s\n" %(pci["dev_desc"],key,value)
                        if totalerr < 0:
                            RET[RETURN_KEY1] = -1
                            RJPRINT("%-10s (%-13s, %s): FAILED"%(pci["dev_desc"], value_list[0], value_list[1]))
                            RJPRINT(errmsg)
                            errmsg = ""
                            totalerr = 0
                        else:
                            RJPRINT("%-10s (%-13s, %s): PASS"%(pci["dev_desc"], value_list[0], value_list[1]))
                else:
                    RJPRINT("%-10s : PASS"%pci["dev_desc"])
            else:
                RJPRINT("%-10s : FAILED"%pci["dev_desc"])
                RET[RETURN_KEY2] += "%-10s : FAILED"%pci["dev_desc"]
                RET[RETURN_KEY1] = -1
    except Exception as e:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = str(e)
        log_debug(str(e))

    return RET


def pci_scan():
#   check diff
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    RET1 = diff_pcie()
    if RET1[RETURN_KEY1] != 0:
        RET[RETURN_KEY1] += RET1[RETURN_KEY1]
        RET[RETURN_KEY2] += RET1[RETURN_KEY2]
        RJPRINT("PCIe        devices scan             : FAILED")
        RJPRINT("failed reason: %s" % RET[RETURN_KEY2])
    else:
        RJPRINT("PCIe        devices scan             : PASS")

    RET1 = check_pcie_speed()
    if RET1[RETURN_KEY1] != 0:
        RET[RETURN_KEY1] += RET1[RETURN_KEY1]
        RET[RETURN_KEY2] += RET1[RETURN_KEY2]

    return RET

def test_cpu_gpio():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    firmware_upgrade_path = TESTCASE.get('firmware_upgrade_path', None)
    if firmware_upgrade_path is None:
        ret, log = log_os_system("which firmware_upgrade", 0)
        if len(log):
            ret, log = log_os_system("firmware_upgrade cpld test", 0)
            RJPRINT(log)
            if "PASS" not in log:
                RET[RETURN_KEY2] = log
                RET[RETURN_KEY1] = -1
    else:
        cmd = "%s cpld test" % firmware_upgrade_path
        ret, log = log_os_system(cmd, 0)
        RJPRINT(log)
        if "PASS" not in log:
            RET[RETURN_KEY2] = log
            RET[RETURN_KEY1] = -1
    return RET

def test_cpld_gpio():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    upgrade_py_path = TESTCASE.get('upgrade_py_path', None)
    slot_num = TESTCASE.get('slot_num', 0)
    if upgrade_py_path is None:
        ret, log = log_os_system("which upgrade.py", 0)
        if len(log):
            for slot in range(0, slot_num + 1):
                cmd = "upgrade.py test cpld %s" % slot
                ret, log = log_os_system(cmd, 0)
                RJPRINT(log)
                if "succeeded" not in log:
                    RET[RETURN_KEY1] = -1
        else:
            test_open_gpio()
            RET = test_cpu_gpio()
            test_close_gpio()
    else:
        for slot in range(0, slot_num + 1):
            cmd = "%s test cpld %s" % (upgrade_py_path, slot)
            ret, log = log_os_system(cmd, 0)
            RJPRINT(log)
            if "succeeded" not in log:
                RET[RETURN_KEY1] = -1
    return RET

def test_bmc_cpld_gpio(param_t):
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    cmd = ""
    for gpiotest in TESTCASE.get("BMC_CPLD_TEST", None):
        test_ret = 0
        RJPRINT("")
        commands = gpiotest.get("open_gpio", None)
        ret, val = send_commands(commands, False)
        if ret == False:
            RET[RETURN_KEY1] = -1
            test_ret = -1
            RJPRINT("%s : FAIL" % (gpiotest["test_name"]))
            continue

        ret = test_bmc_func(param_t)
        RJPRINT(ret.get(RETURN_KEY2))
        if ret.get(RETURN_KEY1) != 0:
            RET[RETURN_KEY1] = -1
            test_ret = -1
            RJPRINT("%s : FAIL" % (gpiotest["test_name"]))
            continue

        commands = gpiotest.get("close_gpio", None)
        ret, val = send_commands(commands, False)
        if ret == False:
            RET[RETURN_KEY1] = -1
            test_ret = -1

        if test_ret == 0:
            RJPRINT("%s : PASS" % (gpiotest["test_name"]))
        else:
            RJPRINT("%s : FAIL" % (gpiotest["test_name"]))
    return RET

def test_fpga():
    errmsg = ""
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    cmd = ""
    ret, log = log_os_system("which firmware_upgrade", 0)
    if len(log):
        cmd = "firmware_upgrade fpga test fpga0"
    else:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "no firmware_upgrade cmd find"
        RJPRINT("no firmware_upgrade cmd find")
        return RET

    ret, log = log_os_system(cmd, 0)
    RJPRINT(log)
    if "PASS" not in log:
        RET[RETURN_KEY2] = log
        RET[RETURN_KEY1] = -1
    return RET

def test_mul_fpga():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    upgrade_py_path = TESTCASE.get('upgrade_py_path', None)
    if upgrade_py_path is None:
        cmd = ""
        ret, log = log_os_system("which upgrade.py", 0)
        if len(log):
            cmd = "upgrade.py test fpga 0"
            ret, log = log_os_system(cmd, 0)
            if len(log):
                RJPRINT(log)
                if "succeeded" not in log:
                    RET[RETURN_KEY2] = log
                    RET[RETURN_KEY1] = -1
            else:
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] = "exec upgrade.py test fpga 0 failed"
                RJPRINT("exec upgrade.py test fpga 0 failed")
        else:
            RET = test_fpga()
    else:
        cmd = "%s test fpga 0" % upgrade_py_path
        ret, log = log_os_system(cmd, 0)
        RJPRINT(log)
        if "succeeded" not in log:
            RET[RETURN_KEY2] = log
            RET[RETURN_KEY1] = -1
    return RET

def test_mul_fpga_mtd():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    cmd = ""
    for gpiotest in TESTCASE.get("CPU_FPGA_MTD_TEST", None):
        test_ret = 0
        RJPRINT("")
        commands = gpiotest.get("open_gpio", None)
        ret, val = send_commands(commands, True)
        if ret == False:
            RET[RETURN_KEY1] = -1
            test_ret = -1
            RJPRINT("%s : FAIL" % (gpiotest["test_name"]))
            continue

        ret, log = log_os_system("cat /proc/mtd", 0)
        if "spi" not in log:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "Open gpio fail"
            test_ret = -1
            RJPRINT("Open gpio fail")

        commands = gpiotest.get("close_gpio", None)
        ret, val = send_commands(commands, True)
        if ret == False:
            RET[RETURN_KEY1] = -1
            test_ret = -1

        if test_ret == 0:
            RJPRINT("%s : PASS" % (gpiotest["test_name"]))
        else:
            RJPRINT("%s : FAIL" % (gpiotest["test_name"]))
    return RET

def test_e2_protect():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    cmd = ""
    for e2test in TESTCASE.get("E2TEST", None):
        test_ret = 0
        #打开写保护开关，该测试项无需测试关闭的情况，因为关闭写保护在SET E2PROM信息时会测试到
        e2_pro = e2test.get('e2_protect',{})
        dealtype = e2_pro.get('gettype',None)
        if dealtype is None:
            rji2cset(e2_pro["bus"], e2_pro["devno"], e2_pro["addr"], e2_pro["close"])
        elif dealtype == "io":
            io_wr(e2_pro["io_addr"], e2_pro["close"])
        RJPRINT("")
        #打开写保护开关情况下，无法写值到E2PROM
        for e2prom in e2test.get("e2prom", None):
            rji2cset(e2prom["bus"], e2prom["devno"], e2prom["addr"], e2prom["testval"])
            time.sleep(0.1)
            ret, val = rji2cget(e2prom["bus"], e2prom["devno"], e2prom["addr"])
            if int(val,16) == e2prom["testval"]:
                RET[RETURN_KEY2] = val
                RET[RETURN_KEY1] = -1
                test_ret = -1
        if test_ret == 0:
            RJPRINT("%s : PASS" % (e2test.get('test_name')))
        else:
            RJPRINT("%s : FAIL" % (e2test.get('test_name')))

    return RET

def test_e2_write_protect():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    #MAC E2写保护寄存器测试
    ret, log = rj_os_system("dfd_debug i2c_wr 2 0x1d 0x49 0xfe")
    ret, log = rj_os_system("dfd_debug i2c_wr 78 0x57 0xff 0x00")
    time.sleep(0.1)
    ret, log = rji2cget(78, 0x57, 0xff)
    if "0x00" not in log:
        RET[RETURN_KEY2] = log
        RET[RETURN_KEY1] = -1
        RJPRINT("MAC E2写保护寄存器测试 : FAIL")
        return RET
    ret, log = rj_os_system("dfd_debug i2c_wr 78 0x57 0xff 0xaa")
    time.sleep(0.1)
    ret, log = rji2cget(78, 0x57, 0xff)
    if "0xaa" not in log:
        RET[RETURN_KEY2] = log
        RET[RETURN_KEY1] = -1
        RJPRINT("MAC E2写保护寄存器测试 : FAIL")
        return RET
    ret, log = rj_os_system("dfd_debug i2c_wr 2 0x1d 0x49 0xff")
    ret, log = rj_os_system("dfd_debug i2c_wr 78 0x57 0xff 0x00")
    time.sleep(0.1)
    ret, log = rji2cget(78, 0x57, 0xff)
    if "0x00" in log:
        RET[RETURN_KEY2] = log
        RET[RETURN_KEY1] = -1
        RJPRINT("MAC E2写保护寄存器测试 : FAIL")
        return RET
    RJPRINT("MAC E2写保护寄存器测试 : OK")

    #CPU底板E2写保护测试
    ret, log = rj_os_system("dfd_debug io_wr 0x941 0xfc")
    ret, log = rj_os_system("dfd_debug i2c_wr 1 0x56 0xff 0x00")
    ret, log = rj_os_system("dfd_debug i2c_wr 1 0x57 0xff 0x00")
    time.sleep(0.1)
    ret, log = rji2cget(1, 0x56, 0xff)
    if "0x00" not in log:
        RET[RETURN_KEY2] = log
        RET[RETURN_KEY1] = -1
        RJPRINT("CPU底板E2写保护寄存器测试  : FAIL")
        return RET
    ret, log = rji2cget(1, 0x57, 0xff)
    if "0x00" not in log:
        RET[RETURN_KEY2] = log
        RET[RETURN_KEY1] = -1
        RJPRINT("CPU底板E2写保护寄存器测试  : FAIL")
        return RET
    ret, log = rj_os_system("dfd_debug i2c_wr 1 0x56 0xff 0xaa")
    ret, log = rj_os_system("dfd_debug i2c_wr 1 0x57 0xff 0xaa")
    time.sleep(0.1)
    ret, log = rji2cget(1, 0x56, 0xff)
    if "0xaa" not in log:
        RET[RETURN_KEY2] = log
        RET[RETURN_KEY1] = -1
        RJPRINT("CPU底板E2写保护寄存器测试  : FAIL")
        return RET
    ret, log = rji2cget(1, 0x57, 0xff)
    if "0xaa" not in log:
        RET[RETURN_KEY2] = log
        RET[RETURN_KEY1] = -1
        RJPRINT("CPU底板E2写保护寄存器测试  : FAIL")
        return RET
    ret, log = rj_os_system("dfd_debug io_wr 0x941 0xff")
    ret, log = rj_os_system("dfd_debug i2c_wr 1 0x56 0xff 0x00")
    ret, log = rj_os_system("dfd_debug i2c_wr 1 0x57 0xff 0x00")
    time.sleep(0.1)
    ret, log = rji2cget(1, 0x56, 0xff)
    if "0x00" in log:
        RET[RETURN_KEY2] = log
        RET[RETURN_KEY1] = -1
        RJPRINT("CPU底板E2写保护寄存器测试  : FAIL")
        return RET
        ret, log = rji2cget(1, 0x57, 0xff)
    if "0x00" in log:
        RET[RETURN_KEY2] = log
        RET[RETURN_KEY1] = -1
        RJPRINT("CPU底板E2写保护寄存器测试  : FAIL")
        return RET
    RJPRINT("CPU底板E2写保护寄存器测试 : OK")

    #FAN板E2写保护寄存器测试
    ret, log = rj_os_system("dfd_debug i2c_wr 4 0x3d 0x31 0xfe")
    ret, log = rj_os_system("dfd_debug i2c_wr 77 0x56 0xff 0x00")
    time.sleep(0.1)
    ret, log = rji2cget(77, 0x56, 0xff)
    if "0x00" not in log:
        RET[RETURN_KEY2] = log
        RET[RETURN_KEY1] = -1
        RJPRINT("FAN板E2写保护寄存器测试 : FAIL")
        return RET
    ret, log = rj_os_system("dfd_debug i2c_wr 77 0x56 0xff 0xaa")
    time.sleep(0.1)
    ret, log = rji2cget(77, 0x56, 0xff)
    if "0xaa" not in log:
        RET[RETURN_KEY2] = log
        RET[RETURN_KEY1] = -1
        RJPRINT("FAN板E2写保护寄存器测试 : FAIL")
        return RET
    ret, log = rj_os_system("dfd_debug i2c_wr 4 0x3d 0x31 0xff")
    ret, log = rj_os_system("dfd_debug i2c_wr 77 0x56 0xff 0x00")
    time.sleep(0.1)
    ret, log = rji2cget(77, 0x56, 0xff)
    if "0x00" in log:
        RET[RETURN_KEY2] = log
        RET[RETURN_KEY1] = -1
        RJPRINT("FAN板E2写保护寄存器测试 : FAIL")
        return RET
    RJPRINT("FAN板E2写保护寄存器测试 : OK")
    return RET

def test_loopback_module():
    pass_list = []
    failed_list = []
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    #光模块电压测试测试
    RJPRINT("光模块电压测试：")
    i = 1
    #BUS 6~53为100G口
    for bus in range(6, 54):
        ret1, val1 = rji2cget(bus, 0x50, 0x10)
        ret2, val2 = rji2cget(bus, 0x50, 0x11)
        #电压的合法范围在3135mV到3500mV，转换成对应的16进制进行判断
        if ret1 == True and ret2 == True:
            vcc = int(val1,16) * 0x0100 + int(val2,16)
            if vcc > 0x7A76 and vcc < 0x88b8:
                pass_list.append(i)
            else:
                failed_list.append(i)
        else:
            failed_list.append(i)
        i += 1
    #BUS 54~61为400G口
    for bus in range(54, 62):
        ret1, val1 = rji2cget(bus, 0x50, 0x10)
        ret2, val2 = rji2cget(bus, 0x50, 0x11)
        ret3, val3 = rji2cget(bus, 0x50, 0x18)
        ret4, val4 = rji2cget(bus, 0x50, 0x19)
        ret5, val5 = rji2cget(bus, 0x50, 0x16)
        ret6, val6 = rji2cget(bus, 0x50, 0x17)
        #电压的合法范围在3135mV到3500mV，转换成对应的16进制进行判断
        if (ret1 == True and ret2 == True) and (ret3 == True and ret4 == True) and (ret5 == True and ret6 == True):
            vcc1 = int(val1,16) * 0x0100 + int(val2,16)
            vcctx = int(val3,16) * 0x0100 + int(val4,16)
            vccrx = int(val5,16) * 0x0100 + int(val6,16)
            if (vcc1 > 0x7A76 and vcc1 < 0x88b8) and (vcctx > 0x7A76 and vcctx < 0x88b8) and (vccrx > 0x7A76 and vccrx < 0x88b8):
                pass_list.append(i)
            else:
                failed_list.append(i)
        else:
            failed_list.append(i)
        i += 1
    if len(pass_list) > 0:
        port_totalprint(pass_list, "成功端口：          ")
    if len(failed_list) >0:
        port_totalprint(failed_list, "失败端口：          ")
        RET[RETURN_KEY1] = -1

    #100G LPWn/PRSn信号信号测试：
    pass_list2 = []
    failed_list2 = []
    RJPRINT("")
    RJPRINT("100G LPWn/PRSn信号信号测试：")
    rji2cset(2, 0x1d, 0x37, 0xff)
    rji2cset(2, 0x2d, 0x33, 0xff)
    rji2cset(2, 0x2d, 0x34, 0xff)
    rji2cset(2, 0x3d, 0x33, 0xff)
    rji2cset(2, 0x3d, 0x34, 0xff)
    rji2cset(2, 0x3d, 0x35, 0xff)
    rji2cset(2, 0x3d, 0x36, 0xff)
    time.sleep(0.1)
    i = 1
    #BUS 6~53为100G口
    for bus in range(6, 54):
        #LPWn信号测试
        ret1, val1 = rji2cget(bus, 0x50, 0x03)
        if ret1 == True:
            lpwn = int(val1,16)
            lpmode = (lpwn & (1<< 2)) >> 2
            if lpmode == 1 :
                pass_list2.append(i)
            else:
                failed_list2.append(i)
                log_error("LOOPBACK LPMODE SET FAIL  PORT:%d, GETVALUE:%s bus：%d addr:0x50 offset:0x03" % (i, val1, bus))
                ret1, val1 = rji2cget(bus, 0x50, 0x03) # S6580 loopback 硬件BUG，此处为规避处理，详见BUG ID 690648
                log_error("LOOPBACK LPMODE SET FAIL  PORT:%d, GETVALUE:%s bus：%d addr:0x50 offset:0x03" % (i, val1, bus))
                ret1, val1 = rji2cget(bus, 0x50, 0x03)
                log_error("LOOPBACK LPMODE SET FAIL  PORT:%d, GETVALUE:%s bus：%d addr:0x50 offset:0x03" % (i, val1, bus))
                ret1, val1 = rji2cget(bus, 0x50, 0x03)
                log_error("LOOPBACK LPMODE SET FAIL  PORT:%d, GETVALUE:%s bus：%d addr:0x50 offset:0x03" % (i, val1, bus))
        else:
            failed_list2.append(i)
        i += 1
    if len(pass_list2) > 0:
        port_totalprint(pass_list2, "成功端口：          ")
    if len(failed_list2) >0:
        port_totalprint(failed_list2, "失败端口：          ")
        RET[RETURN_KEY1] = -1
    #PRSN信号测试，判断是否全部在位
    ret_prsn = True
    ret1, val1 = rji2cget(2, 0x1d, 0x31)
    if ret1 == True:
        prsn = int(val1,16)
        if prsn != 0x00:
            ret_prsn = False
    else:
        ret_prsn = False
    ret2, val2 = rji2cget(2, 0x1d, 0x30)
    if ret2 == True:
        prsn = int(val2,16)
        if prsn != 0x00:
            ret_prsn = False
    else:
        ret_prsn = False
    ret3, val3 = rji2cget(2, 0x2d, 0x30)
    if ret3 == True:
        prsn = int(val3,16)
        if prsn != 0x00:
            ret_prsn = False
    else:
        ret_prsn = False
    ret4, val4 = rji2cget(2, 0x2d, 0x31)
    if ret4 == True:
        prsn = int(val4,16)
        if prsn != 0x00:
            ret_prsn = False
    else:
        ret_prsn = False
    ret5, val5 = rji2cget(2, 0x2d, 0x32)
    if ret5 == True:
        prsn = int(val5,16)
        if prsn != 0xf8:
            ret_prsn = False
    else:
        ret_prsn = False
    ret6, val6 = rji2cget(2, 0x3d, 0x30)
    if ret6 == True:
        prsn = int(val6,16)
        if prsn != 0x00:
            ret_prsn = False
    else:
        ret_prsn = False
    ret7, val7 = rji2cget(2, 0x3d, 0x31)
    if ret7 == True:
        prsn = int(val7,16)
        if prsn != 0x00:
            ret_prsn = False
    else:
        ret_prsn = False
    ret8, val8 = rji2cget(2, 0x3d, 0x32)
    if ret8 == True:
        prsn = int(val8,16)
        if prsn != 0xe0:
            ret_prsn = False
    else:
        ret_prsn = False

    if ret_prsn == True:
        RJPRINT("100G PRSN信号是否全部在位： 是")
    else:
        RJPRINT("100G PRSN信号是否全部在位： 否")
        RET[RETURN_KEY1] = -1

    #100G INt/RSTn信号测试，当前存在中断问题，代码先注释提交：
    """ pass_list3 = []
    failed_list3 = []
    RJPRINT("")
    RJPRINT("100G INt/RSTn信号测试：")
    ret_int  = True
    ret1, val1 = rji2cget(2, 0x1d, 0x14)
    if (ret1 == False) or (int(val1,16) != 0xff):
        ret_int = False
    ret2, val2 = rji2cget(2, 0x2d, 0x12)
    if (ret2 == False) or (int(val2,16) != 0xff):
        ret_int = False
    ret3, val3 = rji2cget(2, 0x2d, 0x13)
    if (ret3 == False) or (int(val3,16) != 0xff):
        ret_int = False
    ret4, val4 = rji2cget(2, 0x2d, 0x14)
    if (ret4 == False) or (int(val4,16) != 0xff):
        ret_int = False
    ret5, val5 = rji2cget(2, 0x3d, 0x12)
    if (ret5 == False) or (int(val5,16) != 0xff):
        ret_int = False
    ret6, val6 = rji2cget(2, 0x3d, 0x13)
    if (ret6 == False) or (int(val6,16) != 0xff):
        ret_int = False
    ret7, val7 = rji2cget(2, 0x3d, 0x14)
    if (ret7 == False) or (int(val7,16) != 0xff):
        ret_int = False
    if ret_int == True:
        RJPRINT("100G 光模块是否无中断信号电平： 是")
    else:
        RJPRINT("100G 光模块是否无中断信号电平： 否")
        RET[RETURN_KEY1] = -1
    #RSTn信号测试, 复位信号写0
    i = 1
    for bus in range(6, 53):
        rji2cset(2, 0x1d, 0x21, 0x00)
        rji2cset(2, 0x2d, 0x20 ,0x00)
        rji2cset(2, 0x2d, 0x21, 0x00)
        rji2cset(2, 0x3d, 0x21, 0x00)
        rji2cset(2, 0x3d, 0x22, 0x00)
        rji2cset(2, 0x3d, 0x23, 0x00)
        rji2cset(2, 0x3d, 0x24, 0x00)
        time.sleep(1)
        ret1, val1 = rji2cget(bus, 0x50, 0x00)
        if ret1 == True:
            failed_list3.append(i)
            i += 1
            continue
        rji2cset(2, 0x1d, 0x21, 0xff)
        rji2cset(2, 0x2d, 0x20 ,0xff)
        rji2cset(2, 0x2d, 0x21, 0xff)
        rji2cset(2, 0x3d, 0x21, 0xff)
        rji2cset(2, 0x3d, 0x22, 0xff)
        rji2cset(2, 0x3d, 0x23, 0xff)
        rji2cset(2, 0x3d, 0x24, 0xff)
        time.sleep(1)
        ret1, val1 = rji2cget(bus, 0x50, 0x00)
        if ret1 == True:
            pass_list3.append(i)
        else:
            failed_list3.append(i)
        i += 1
    #完成信号测试后，统一恢复
    rji2cset(2, 0x1d, 0x21, 0xff)
    rji2cset(2, 0x2d, 0x20 ,0xff)
    rji2cset(2, 0x2d, 0x21, 0xff)
    rji2cset(2, 0x3d, 0x21, 0xff)
    rji2cset(2, 0x3d, 0x22, 0xff)
    rji2cset(2, 0x3d, 0x23, 0xff)
    rji2cset(2, 0x3d, 0x24, 0xff)
    if len(pass_list3) > 0:
        port_totalprint(pass_list3, "成功端口：          ")
    if len(failed_list3) >0:
        port_totalprint(failed_list3, "失败端口：          ")
        RET[RETURN_KEY1] = -1

    #400G INTL信号测试：
    pass_list4 = []
    failed_list4 = []
    RJPRINT("")
    RJPRINT("400G INTL信号测试：")"""

    #400G RESETL Signal信号测试：
    pass_list5 = []
    failed_list5 = []
    RJPRINT("")
    RJPRINT("400G RESETL Signal信号测试：")
    i = 49
    for bus in range(54, 62):
        rji2cset(2, 0x1d, 0x22, 0x00)
        time.sleep(0.1)
        ret1, val1 = rji2cget(bus, 0x50, 0x00)
        if ret1 == True:
            failed_list5.append(i)
            i += 1
            continue
        rji2cset(2, 0x1d, 0x22, 0xff)
        time.sleep(0.1)
        ret1, val1 = rji2cget(bus, 0x50, 0x00)
        if ret1 == True:
            pass_list5.append(i)
        else:
            failed_list5.append(i)
        i += 1
    #完成信号测试后，统一恢复
    rji2cset(2, 0x1d, 0x22, 0xff)
    if len(pass_list5) > 0:
        port_totalprint(pass_list5, "成功端口：          ")
    if len(failed_list5) >0:
        port_totalprint(failed_list5, "失败端口：          ")
        RET[RETURN_KEY1] = -1

    #400G MODSELL信号测试：
    pass_list6 = []
    failed_list6 = []
    RJPRINT("")
    RJPRINT("400G MODSELL信号测试：")
    i = 49
    for bus in range(54, 62):
        rji2cset(2, 0x1d, 0x35, 0xff)
        time.sleep(0.1)
        ret1, val1 = rji2cget(bus, 0x50, 0x00)
        if ret1 == True:
            failed_list6.append(i)
            i += 1
            continue
        rji2cset(2, 0x1d, 0x35, 0x00)
        time.sleep(0.1)
        ret1, val1 = rji2cget(bus, 0x50, 0x00)
        if ret1 == True:
            pass_list6.append(i)
        else:
            failed_list6.append(i)
        i += 1
    #完成信号测试后，统一恢复
    rji2cset(2, 0x1d, 0x35, 0x00)
    if len(pass_list6) > 0:
        port_totalprint(pass_list6, "成功端口：          ")
    if len(failed_list6) >0:
        port_totalprint(failed_list6, "失败端口：          ")
        RET[RETURN_KEY1] = -1

    #400G LPMODE信号测试：
    pass_list7 = []
    failed_list7 = []
    RJPRINT("")
    RJPRINT("400G LPMODE信号测试：")
    rji2cset(2, 0x1d, 0x38, 0xff)
    time.sleep(0.1)
    i = 49
    for bus in range(54, 62):
        ret1, val1 = rji2cget(bus, 0x50, 0x12)
        if ret1 == True:
            lpmode = (int(val1,16) & (1<< 3)) >> 3
            if lpmode == 1 :
                pass_list7.append(i)
            else:
                failed_list7.append(i)
        else:
            failed_list7.append(i)
        i += 1
    if len(pass_list6) > 0:
        port_totalprint(pass_list7, "成功端口：          ")
    if len(failed_list6) >0:
        port_totalprint(failed_list7, "失败端口：          ")
        RET[RETURN_KEY1] = -1

    #400G  MODPRSL信号测试：
    RJPRINT("")
    ret1, val1 = rji2cget(2, 0x1d, 0x31)
    if (ret1 == True) and (int(val1,16) == 0x00):
        RJPRINT("400G MODPRSL信号是否全部在位： 是")
    else:
        RJPRINT("400G MODPRSL信号是否全部在位： 否")
        RET[RETURN_KEY1] = -1

    return RET

def bmc_get_sensor_info():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    cmd = ""
    ret, log = log_os_system("ipmitool sdr list", 0)
    RET[RETURN_KEY2] = log
    RJPRINT(log)
    if "disabled" in log or "failed"in log:
        RET[RETURN_KEY1] = -1
    return RET

def test_bmc_image_force_switch(bmc_info):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    RET = test_bmc_func("bmc_get_flash")
    status = False
    timeout = TESTCASE.get("SONIC",{}).get("timeout",120)
    if RET[RETURN_KEY1]:
        RJPRINT(RET[RETURN_KEY2])
        return RET
    if bmc_info in RET[RETURN_KEY2]:
        RJPRINT("已是%s，无需切换"%bmc_info)
        RET[RETURN_KEY1] = 0
        return RET
    if makesure("切换会导致BMC重启，是否继续？[Yes/No]：",False,echo = True):
        RJPRINT("执行切换中，请等待约90s...")
        path = getRealUrl("bmc_test_switch")
        cmd = "curl -m 90 %s" % path
        ret, log =log_os_system(cmd, 0)
        if "timed out" not in log:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "强制切换BMC失败"
            return RET
        #BMC切换之后会导致X86端的USB0 IP丢失，需要重新配置
        ret_t = usb0_init()
        while timeout > 0:
            if ret_t == False:
                ret_t = usb0_init()
            status,msg = test_bmc_channel()
            if status == True:
                break
            time.sleep(2)
            timeout -= 2
        if timeout < 0:
            RJPRINT(msg)
            RET[RETURN_KEY1] = -1
            return RET
        RET = test_bmc_func("bmc_get_flash")
        if bmc_info in RET[RETURN_KEY2]:
            RJPRINT("已成功执行切换操作")
        else:
            RJPRINT("BMC切换失败，请检测主备BMC系统是否在位")
            RET[RETURN_KEY1] = -1
            return RET
    else:
        print("已撤销")
        RET[RETURN_KEY1] = -1
    return RET

def test_bmc_image_force_switch_master():
    return test_bmc_image_force_switch("master")

def test_bmc_image_force_switch_slave():
    return test_bmc_image_force_switch("slave")

def generate_value(_t):
    ret = []
    for i in TLV_INFO_ID_STRING:
        ret.append(i)
    ret.append(chr(TLV_INFO_VERSION))
    ret.append(chr(TLV_INFO_LENGTH))
    ret.append(chr(TLV_INFO_LENGTH_VALUE))

    total_len = 0
    for key in _t:
        x = getTLV_BODY(key, _t[key])
        ret += x
        total_len += len(x)
    ret[10] = chr(total_len + 6)

    ret.append(chr(0xFE))
    ret.append(chr(0x04))
    s = _crc32(''.join(ret))
    for t in range(0, 4):
        ret.append(chr(int(s[2 * t + 2:2 * t + 4], 16)))
    totallen = len(ret)
    if (totallen < 256):
        for left_t in range(0, 256 - totallen):
            ret.append(chr(0x00))
    return (ret, True)



def isValidMac(mac):
    if re.match(r"^\s*([0-9a-fA-F]{2,2}:){5,5}[0-9a-fA-F]{2,2}\s*$", mac):
        return True
    return False

def RJPRINTERR(str):
    print(("\033[0;31m%s\033[0m" % str))


def test_bmc_ddr_stress_stop():
    RET = {RETURN_KEY1 : 1, RETURN_KEY2 : ""}
    if not makesure("强行结束将无法查看结果，是否继续？[Yes/No]：",echo = True):
        RET[RETURN_KEY2] = "已撤销"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    RET = test_bmc_func("bmc_test_ddr_stress_stop_by_sonic")
    RJPRINT(RET[RETURN_KEY2])
    return RET

def test_bmc_emmc_stress_stop():
    RET = {RETURN_KEY1 : 1, RETURN_KEY2 : ""}
    if not makesure("强行结束将无法查看结果，是否继续？[Yes/No]：",echo = True):
        RET[RETURN_KEY2] = "已撤销"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    RET = test_bmc_func("bmc_test_emmc_stress_stop")
    RJPRINT(RET[RETURN_KEY2])
    return RET

def bmc_test_ddr_stress_with_result():
    RET = {RETURN_KEY1 : 1, RETURN_KEY2 : ""}
    RET = test_bmc_func("bmc_test_ddr_stress")
    RJPRINT(RET[RETURN_KEY2])
    if "已启动后台执行" not in RET[RETURN_KEY2]:
        return RET
    RJPRINT("后台执行测试，等待100s")
    time.sleep(100)
    RET = test_bmc_func("bmc_test_ddr_stress_result")
    RJPRINT(RET[RETURN_KEY2])
    return RET

def get_fane2_sysfs(bus, loc):
    rg_fan_e2 = "%d-%04x/fan" % (bus, loc)
    eeprom = get_sysfs_value(rg_fan_e2)
    return eeprom

#定义序列号长度的默认值
FAN_SN_LEN_DEF = 13
BOARD_SN_LEN_DEF = 13

def checkfansninput(fan_sn, fansntemp):
    if fan_sn in fansntemp:
        RJPRINTERR("存在相同序列号，请重新输入！")
        return False
    if fan_sn.isalnum() == False:
        RJPRINTERR("序列号非法字符串，请重新输入！")
        return False
    fan_sn_len = TESTCASE.get('setmacsnlen', {}).get("fan", FAN_SN_LEN_DEF)
    if(len(fan_sn) != fan_sn_len):
        RJPRINTERR("序列号长度错误(" + fan_sn_len + "位)，请重新输入！")
        return False
    return True

# 判断输入的硬件版本号
def checkfanhwinput(hw):
    if len(hw) != 4:
        RJPRINTERR("硬件版本号长度不正确,请重新输入！")
        return False
    if hw.find(".") != 1:
        RJPRINTERR("硬件版本号不正确,请重新输入！")
        return False
    return True

def util_show_fanse2(fans):
    formatstr = "%-8s  %-20s  %-20s  %-20s"
    print(formatstr % ("id", "名称", "硬件版本号", "序列号"))
    formatstr = "%-8s  %-18s  %-15s  %-15s"
    print(formatstr % ("------", "------------", "-----------", "---------------"))
    formatstr = "%-10s  %-18s  %-15s  %-15s"
    for fan in fans:
        # print fan.dstatus
        if fan.dstatus < 0:
            print("%-8s" % ("风扇%d" % (fans.index(fan) + 1)), end=' ')
            RJPRINTERR("  解析e2出错")
        else:
            print(formatstr % ("风扇%d" % (fans.index(fan) + 1), fan.typename.replace(chr(0x00), ""),
                               fan.typehwinfo.replace(chr(0x00), ""), fan.typesn.replace(chr(0x00), "")))

def fac_fan_setmac(item):

    I2CUTIL.openFanE2Protect()
    I2CUTIL.writeToFanE2(item.fanbus, item.fanloc, item.generate_fan_value())
    I2CUTIL.closeFanE2Protect()

    pass


def fac_fans_setmac_tlv(ret):
    if len(ret) <=0:
        return None
    fans = []
    fansntemp = []
    for index in range(len(ret)):
        item = ret[index]
        log_debug(item)
        eeprom = get_fane2_sysfs(item["bus"], item["loc"])
        fane2 = fan_tlv()
        fane2.decode(eeprom)
        fane2.fanbus = item["bus"]
        fane2.fanloc = item["loc"]
        log_debug("decode eeprom success")

        print("风扇【%d】-【%s】setmac" % ((index + 1), FANS_DEF[fane2.typedevtype]))
        while True:
            print("请输入[%s如(0000000000000)]:" % "序列号", end=' ')
            fan_sn = input()
            if checkfansninput(fan_sn, fansntemp) == False:
                continue
            fansntemp.append(fan_sn)
            fan_sn = fan_sn + chr(0x00)
            fane2.typesn = fan_sn
            break
        while True:
            print("请输入[%s如(1.00)]:" % "硬件版本号", end=' ')
            hwinfo = input()
            if checkfanhwinput(hwinfo) == False:
                continue
            fan_hwinfo = hwinfo + chr(0x00)
            fane2.typehwinfo = fan_hwinfo
            break
        log_debug(fane2.typedevtype)
        fane2.typename = FANS_DEF[fane2.typedevtype] + chr(0x00)
        fans.append(fane2)
        print("\n")
    print("\n*******************************\n")

    util_show_fanse2(fans)
    if makesure("确认是否输入正确（Yes/No):",echo = 1) == True:
        for fan in fans:
            log_debug("ouput fan")
            fac_fan_setmac(fan)
    else:
        print("setmac退出")
        return False

def fac_fans_show_tlv(ret):
    totalerr = 0
    fans =  ret
    for fan in fans:
        try:
            RJPRINT("===============fan%d ================getmessage" % (fans.index(fan)+1))
            #判断风扇是否在位
            fanstatus = TESTCASE.get("frustatus",None)
            fanstatusdecode = TESTCASE.get("frustatusdecode",None)
            fanpresent = fanstatusdecode.get('fanpresent')
            fans_conf = fanstatus.get('fans', None)
            item_fan = fans_conf[fans.index(fan)]
            presentbus = item_fan.get('bus')
            presentaddr = item_fan.get('presentloc')
            presentbit = item_fan.get('presentbit')
            loc      = item_fan.get('loc')
            ind, val = rji2cget(presentbus, loc,presentaddr)
            if ind == True:
                val_t = (int(val,16) & (1<< presentbit)) >> presentbit
                if val_t != fanpresent.get('okval'):#风扇不在位
                    formatstr = "fan%%-%dd:ABSENT"%((17+wide_chars("fan")))
                    RJPRINT(formatstr%(fans.index(fan)+1))
                    totalerr -= 1
                    continue
                else:
                    eeprom = I2CUTIL.dumpValueByI2c(fan.get('bus'), fan.get('loc'))
                    tlv = fan_tlv()
                    rets = tlv.decode(eeprom)
                    if len(rets) == 0:
                        totalerr -= 1
                        RJPRINT("fan E2 read error, please set fan E2 !")
                        continue
                    for item in rets:
                        formatstr = "%%-%ds:%%-20s"%((20+wide_chars(item["name"])))
                        RJPRINT(formatstr%(item["name"],item["value"]))
            else:
                totalerr -= 1
                RJPRINT("get fan present fail!")
        except Exception as e:
            RJPRINT(str(e))
            totalerr -= 1
    if totalerr < 0:
        return False
    return True



def fac_fans_show_fru(ret):
    fans =  ret
    totalerr = 0
    for fan in fans:
        try:
            RJPRINT("===============%s ================getmessage" % fan.get('name'))
            ret, binval_bytes = dev_file_read(I2CUTIL.getE2File(fan.get('bus'), fan.get('loc')), 0, 256)
            if ret is False:
                RJPRINT("%s getmessage failed: %s" % (fan.get('name'), binval_bytes))
                totalerr -= 1
                continue
            eeprom = byteTostr(binval_bytes)
            fru = ipmifru()
            fru.decodeBin(eeprom)
            e2_decode = fan.get('e2_decode')
            if e2_decode is not None:
                fru_eeprom_decode(fru, e2_decode)

            RJPRINT("=================board=================")
            RJPRINT(fru.boardInfoArea)
            RJPRINT("=================product=================")
            RJPRINT(fru.productInfoArea)
        except Exception as e:
            totalerr -= 1
    if totalerr <0:
        return False
    return True

def getfilevalue(location):
    try:
        with open(location, 'r') as fd:
            value = fd.read()
        return True, value.strip()
    except Exception as e:
        return False, "error"

def test_psu_eeprom():
    return test_get_psu_fru()

def test_tlv_eeprom(is_onl = False):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    errmsg = ""
    totalerr = 0
    flag = 0

    if is_onl is False:
        RJPRINT("%s "% "show platform syseeprom information:")
        ret, log = log_os_system("show platform syseeprom", 0)
        RJPRINT(log)
        if ret or "TlvInfo" not in log:
            RET[RETURN_KEY1] = -1
            totalerr -= 1
            RJPRINT("Failed to get system TLV-E2 information")

    RJPRINT("")
    RJPRINT("%s "% "Hardware TLV E2 information:")
    rets = get_sys_eeprom()
    if len(rets) == 0:
        RET[RETURN_KEY1] = -1
        totalerr -= 1
        RJPRINT("Failed to parse hardware TLV-E2 information")
        return RET
    for item in rets:
        if item["code"] == TLV_CODE_PRODUCT_NAME :
            RJPRINT("    %-20s : %s "%("Product Name", item["value"]))
            flag = flag + 1
        if item["code"] == TLV_CODE_DEVICE_VERSION :
            RJPRINT("    %-20s : %s "%("Device Version", item["value"]))
            flag = flag + 1
        if item["code"] == TLV_CODE_SERIAL_NUMBER :
            RJPRINT("    %-20s : %s "%("Serial Number", item["value"]))
            flag = flag + 1
        if item["code"] == TLV_CODE_MAC_BASE :
            RJPRINT("    %-20s : %s "%("MAC Address", item["value"]))
            flag = flag + 1
        if item["code"] == TLV_CODE_PLATFORM_NAME :
            RJPRINT("    %-20s : %s "%("Platform Name", item["value"]))
            flag = flag + 1
        if item["code"] == TLV_CODE_ONIE_VERSION :
            RJPRINT("    %-20s : %s "%("ONIE Version", item["value"]))
            flag = flag + 1
    if flag != 6:
        RET[RETURN_KEY1] = -1
        totalerr -= 1
        RJPRINT("Parsing hardware TLV-E2 information is incomplete")
    RJPRINT("")

    return RET

def test_fan_eeprom():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    try:
        if (fans_eeprom_show() == False):
            totalerr -= 1
    except Exception as e:
        RJPRINTERR(e)
        totalerr -= 1
    RET[RETURN_KEY1] = totalerr
    return RET

def fans_eeprom_show():
    ret =  I2CUTIL.getvaluefromdevice("rg_fan")
    if ret is not None and len(ret) > 0:
        return fac_fans_show_tlv(ret)
    fans =  FRULISTS.get('fans', None)
    if fans is not None and len(fans)>0:
        return fac_fans_show_fru(fans)
    return False

def fac_fan_setmac_fru(ret):
    fans =  ret
    fanfrus = {}
    newfrus = {}
    #getmsg
    try:
        for fan in fans:
            RJPRINT("===============%s ================getmessage" % fan.get('name'))
            eeprom = getsysvalue(I2CUTIL.getE2File(fan.get('bus'), fan.get('loc')))
            if eeprom is None:
                raise Exception("错误")
            fru = ipmifru()
            fru.decodeBin(eeprom)
            fanfrus[fan.get('name')] = fru
    except Exception as e:
        RJPRINT(str(e))
        return False

    #setmsg
    for fan in fans:
        RJPRINT("===============%s ================setmac" % fan.get('name'))
        fruold = fanfrus.get(fan.get('name'))
        newfru = getInputSetmac(fruold)
        newfru.recalcute()
        newfrus[fan.get('name')] = newfru

    #writemsg
    for fan in fans:
        RJPRINT("===============%s ================writeToE2" % fan.get('name'))
        ret_t = newfrus.get(fan.get('name'))
        I2CUTIL.openFanE2Protect()
        #I2CUTIL.writeToFanE2(fan.get('bus'), fan.get('loc'), ret_t.bindata)
        I2CUTIL.writeToFanE2File(fan.get('bus'), fan.get('loc'), ret_t.bindata)
        I2CUTIL.closeFanE2Protect()

    #check
    try:
        for fan in fans:
            RJPRINT("===============%s ================getmessage" % fan.get('name'))
            eeprom = getsysvalue(I2CUTIL.getE2File(fan.get('bus'), fan.get('loc')))
            fru = ipmifru()
            fru.decodeBin(eeprom)

            RJPRINT("=================board=================")
            RJPRINT(fru.boardInfoArea)
            RJPRINT("=================product=================")
            RJPRINT(fru.productInfoArea)
    except Exception as e:
        RJPRINT(str(e))
        return False
    return True

def fac_fans_setmac():
    ret =  I2CUTIL.getvaluefromdevice("rg_fan")
    if ret is not None and len(ret) > 0:
        return fac_fans_setmac_tlv(ret)
    fans =  FRULISTS.get('fans', None)
    if fans is not None and len(fans)>0:
        return fac_fan_setmac_fru(fans)
    return False


def getinputsetmac_slot():
    slot_info = {}
    slot_sn = upper_input("产品序列号:")
    if len(slot_sn) != 13:
        raise Exception("序列号长度不对")
    checkinputproduct(slot_sn)
    hw_version = upper_input("硬件版本号:(如1.00)")
    slot_info["slot_sn"] = slot_sn
    slot_info["hw_version"] = hw_version
    return slot_info

def test_tlv_slot_eeprom():

    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    slots =  FRULISTS.get('slots_tlv', [])
    for slot in slots:
        try:
            RJPRINT("===============%s ================getmessage" % slot.get('name'))
            eeprom = I2CUTIL.dumpValueByI2c(slot.get('bus'), slot.get('loc'))
            if eeprom is None:
                raise Exception("错误")
            slote2 = fan_tlv()
            slote2.decode(eeprom)
            RJPRINT(slote2)
        except Exception as e:
            RJPRINT(str(e))
            RET[RETURN_KEY1] -= 1
            RET[RETURN_KEY2] = str(e)

    return RET

def test_fru_slot_eeprom():

    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    slots =  FRULISTS.get('slots_fru', [])
    for slot in slots:
        try:
            RJPRINT("===============%s ================getmessage" % slot.get('name'))
            eeprom = I2CUTIL.dumpValueByI2c(slot.get('bus'), slot.get('loc'))
            if eeprom is None:
                raise Exception("错误")
            slote2 = ipmifru()
            slote2.decodeBin(eeprom)
            RJPRINT(slote2.boardInfoArea)
        except Exception as e:
            RJPRINT(str(e))
            RET[RETURN_KEY1] -= 1
            RET[RETURN_KEY2] = str(e)

    return RET

def fac_tlv_slots_setmac(old_eeprom,setmac_info):
    '''tlv格式子卡setmac'''
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    slots_tlv =  FRULISTS.get('slots_tlv', [])
    protect = TESTCASE.get('tlv_slots_E2protect',[])

    try:
        for item in protect:
            rji2cset(item["bus"], item["devno"], item["addr"], item["open"])
        for slot in slots_tlv:
            try:
                slote2 = old_eeprom.get(slot.get('name'))
                slot_info = setmac_info.get(slot.get('name'))
                slote2.typesn = slot_info.get("slot_sn") + chr(0x00)
                slote2.typehwinfo = slot_info.get("hw_version") + chr(0x00)

                RJPRINT("===============tlv_%s ================writeToE2" % slot.get('name'))
                I2CUTIL.writeToE2(slot.get('bus'), slot.get('loc'), slote2.generate_fan_value())

                RJPRINT("===============tlv_%s ================showmessage" % slot.get('name'))
                eeprom_new = I2CUTIL.dumpValueByI2c(slot.get('bus'), slot.get('loc'))
                if eeprom_new is None:
                    raise Exception("错误")
                slote2.decode(eeprom_new)
                RJPRINT(slote2)
            except Exception as e:
                RJPRINT(str(e))
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] = str(e)
    except Exception as e:
        RJPRINT(str(e))
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = str(e)
    finally:
        for item in protect:
            rji2cset(item["bus"], item["devno"], item["addr"], item["close"])

    return RET


def fac_fru_slots_setmac(old_eeprom,setmac_info):
    '''fru格式子卡setmac'''
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    slots_fru =  FRULISTS.get('slots_fru', [])
    protect = TESTCASE.get('fru_slots_E2protect',[])

    try:
        for item in protect:
            rji2cset(item["bus"], item["devno"], item["addr"], item["open"])

        for slot in slots_fru:
            try:
                slote2 = old_eeprom.get(slot.get('name'))
                slot_info = setmac_info.get(slot.get('name'))
                slote2.boardInfoArea.boardSerialNumber = slot_info.get("slot_sn")
                slote2.boardInfoArea.boardextra1 = slot_info.get("hw_version")
                slote2.recalcute()
                # writemsg
                RJPRINT("===============fru_%s ================writeToE2" % slot.get('name'))
                I2CUTIL.writeToE2(slot.get('bus'), slot.get('loc'), slote2.bindata)

                RJPRINT("===============fru_%s ================showmessage" % slot.get('name'))
                eeprom_new = I2CUTIL.dumpValueByI2c(slot.get('bus'), slot.get('loc'))
                if eeprom_new is None:
                    raise Exception("错误")
                slote2.decodeBin(eeprom_new)
                RJPRINT(slote2.boardInfoArea)
            except Exception as e:
                RJPRINT(str(e))
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] = str(e)
    except Exception as e:
        RJPRINT(str(e))
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = str(e)
    finally:
        for item in protect:
            rji2cset(item["bus"], item["devno"], item["addr"], item["close"])

    return RET


def fac_slots_setmac():
    """子卡setmac"""
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    setmac_info = {}
    tlv_setmac_flag = FACTESTMODULE.get('tlv_slotsetmac',0)
    fru_setmac_flag = FACTESTMODULE.get('fru_slotsetmac',0)
    if tlv_setmac_flag == 0 and fru_setmac_flag == 0:
        RJPRINT("=============== 无子卡E2 SETMAC信息！================")
        return RET

    slots_tlv =  FRULISTS.get('slots_tlv', [])
    slots_fru =  FRULISTS.get('slots_fru', [])

    if tlv_setmac_flag == 1 and len(slots_tlv) == 0 or fru_setmac_flag == 1 and len(slots_fru) == 0:
        RET[RETURN_KEY1] -= 1
    if tlv_setmac_flag == fru_setmac_flag and len(slots_tlv) != len(slots_fru):
        RET[RETURN_KEY1] -= 1
    if RET[RETURN_KEY1] < 0 :
        RJPRINT("===============子卡E2 SETMAC错误，请检查配置文件! ========" )
        RJPRINT("===============tlv_setmac_flag:%d,length:%d ================" %(tlv_setmac_flag,len(slots_tlv)))
        RJPRINT("===============fru_setmac_flag:%d,length:%d ================" %(fru_setmac_flag,len(slots_fru)))
        return RET


    tlv_old_eeprom = {}
    fru_old_eeprom = {}
    if tlv_setmac_flag == 1:
        for slot in slots_tlv:
            try:
                RJPRINT("===============tlv_%s ================getmessage" % slot.get('name'))
                eeprom = I2CUTIL.dumpValueByI2c(slot.get('bus'), slot.get('loc'))
                if eeprom is None:
                    raise Exception("错误")
                slote2 = fan_tlv()
                slote2.decode(eeprom)
                tlv_old_eeprom[slot.get('name')] = slote2
            except Exception as e:
                 RJPRINT(str(e))
                 RET[RETURN_KEY1] = -1
                 RET[RETURN_KEY2] = str(e)

    if fru_setmac_flag == 1:
        for slot in slots_fru:
            try:
                RJPRINT("===============fru_%s ================getmessage" % slot.get('name'))
                eeprom = I2CUTIL.dumpValueByI2c(slot.get('bus'), slot.get('loc'))
                if eeprom is None:
                    raise Exception("错误")
                slote2 = ipmifru()
                slote2.decodeBin(eeprom)
                fru_old_eeprom[slot.get('name')] = slote2
            except Exception as e:
                 RJPRINT(str(e))
                 RET[RETURN_KEY1] = -1
                 RET[RETURN_KEY2] = str(e)
    if RET[RETURN_KEY1] < 0 :
        RJPRINT("=============== 请确认原始烧片是否正常! ================" )
        return RET

    if tlv_setmac_flag == 1:
        for slot in slots_tlv:
            RJPRINT("=============== %s ================setmac" % slot.get('name'))
            slot_info = getinputsetmac_slot()
            setmac_info[slot.get('name')] = slot_info
    else:
        for slot in slots_fru:
            RJPRINT("=============== %s ================setmac" % slot.get('name'))
            slot_info = getinputsetmac_slot()
            setmac_info[slot.get('name')] = slot_info

    #tlv slot setmac
    if tlv_setmac_flag == 1:
        ret_t = fac_tlv_slots_setmac(tlv_old_eeprom,setmac_info)
        RET[RETURN_KEY1] += ret_t.get(RETURN_KEY1)
        RET[RETURN_KEY2] += ret_t.get(RETURN_KEY2)
    #fru slot setmac
    if fru_setmac_flag == 1:
        ret_t = fac_fru_slots_setmac(fru_old_eeprom,setmac_info)
        RET[RETURN_KEY1] += ret_t.get(RETURN_KEY1)
        RET[RETURN_KEY2] += ret_t.get(RETURN_KEY2)
    return RET

def checkinput(b):
    if b.isdigit() == False:
        raise Exception("非法数字")
    if int(b) > 0xff or int(b) < 0:
        raise Exception("不在区间内")

def checkinputproduct(b):
    if b.isalnum() ==False:
        raise Exception("非法字符串")


# 风扇SETMAC
def getInputSetmac(val):
    bia = val.boardInfoArea
    pia = val.productInfoArea
    # 有些产品非默认长度
    fan_sn_len = TESTCASE.get('setmacsnlen', {}).get("fan", FAN_SN_LEN_DEF)
    sample = "0000000000000"
    sample = sample.ljust(fan_sn_len, '0')
    if bia != None:
        a = upper_input("请输入[板卡区]产品序列号，如(%s):" % sample)
        if len(a) != fan_sn_len:
            raise Exception("序列号长度不对(" + str(fan_sn_len) + "位),请认真核对")
        checkinputproduct(a)
        bia.boardSerialNumber = a
        b = upper_input("[板卡区]产品版本号:(从1-255)")
        checkinput(b)
        #b = "%0x" % int(b)
        bia.boardextra1 = b.upper()
        if FACTESTMODULE.get("setmac_extend", 0) == 1:     # 风扇setmac扩展boardManufacturer字段
            c = upper_input("[板卡区]产品生产商:(不超过16个字符)")
            if len(c) > 16:
                raise Exception("生产商名称长度不对,超过(16个字符),请认真核对")
            checkinputproduct(c)
            bia.boardManufacturer = c
    if pia != None:
        a = upper_input("[产品区]产品序列号，如(%s):" % sample)
        if len(a) != fan_sn_len:
            raise Exception("序列号长度不对(" + str(fan_sn_len) + "位),请认真核对")
        checkinputproduct(a)
        pia.productSerialNumber = a
        b = upper_input("[产品区]产品版本号:(从1-255)")
        checkinput(b)
        #b = "%0x" % int(b)
        pia.productVersion = b.upper()
        if FACTESTMODULE.get("setmac_extend", 0) == 1:     # 风扇setmac扩展productManufacturer字段
            c = upper_input("[产品区]产品生产商:(不超过16个字符)")
            if len(c) > 16:
                raise Exception("生产商名称长度不对,超过(16个字符),请认真核对")
            checkinputproduct(c)
            pia.productManufacturer = c
    return val



class I2CUTIL():
    @staticmethod
    def getvaluefromdevice(name):
        ret = []
        if DEVICE == None:
            return None
        for item in DEVICE:
            if item["name"] == name:
                ret.append(item)
        return ret

    @staticmethod
    def openFanE2Protect():
        if FAN_PROTECT is None or len(FAN_PROTECT) <= 0:
            return
        if type(FAN_PROTECT) == list: #expand 20190429
            for item in FAN_PROTECT:
                rji2cset(item["bus"], item["devno"],
                         item["addr"], item["open"])
        elif type(FAN_PROTECT) == dict:
            rji2cset(FAN_PROTECT["bus"], FAN_PROTECT["devno"],
                     FAN_PROTECT["addr"], FAN_PROTECT["open"])
        else:
            return

    @staticmethod
    def closeFanE2Protect():
        if FAN_PROTECT is None or len(FAN_PROTECT) <= 0:
            return
        if type(FAN_PROTECT) == list: #expand 20190429
            for item in FAN_PROTECT:
                rji2cset(item["bus"], item["devno"],
                         item["addr"], item["close"])
        elif type(FAN_PROTECT) == dict:
            rji2cset(FAN_PROTECT["bus"], FAN_PROTECT["devno"],
                     FAN_PROTECT["addr"], FAN_PROTECT["close"])
        else:
            return

    @staticmethod
    def writeToFanE2(bus, loc, rst_arr):
        index = 0
        for item in rst_arr:
            rji2cset(bus, loc, index, ord(item))
            index += 1

    @staticmethod
    def writeToFanE2File(bus, loc, _value):
        filename = "/sys/bus/i2c/devices/%d-00%02x/eeprom" % (bus, loc)
        file = open(filename, 'wb')
        for x in _value:
            file.write(str(x))
        file.close()

    @staticmethod
    def writeToE2(bus, loc, rst_arr):
        index = 0
        for item in rst_arr:
            rji2cset(bus, loc, index, ord(item))
            index += 1

    @staticmethod
    def getE2File(bus, loc):
        return "/sys/bus/i2c/devices/%d-00%02x/eeprom" % (bus, loc)

    @staticmethod
    def dumpValueByI2c(bus, loc):
        str = ""
        for i in range(256):
            ret,val = rji2cget(bus, loc, i)
            if ret is False:
                log_error("Read bus[%d] loc[0x%x] offset[0x%x] failed." % (bus, loc, i))
                return None
            str += chr(int(val, 16))
        return str

def getsysvalue(location):
    retval = None
    mb_reg_file = location
    try:
        if (not os.path.isfile(mb_reg_file)):
            print(mb_reg_file,  'not found !')
            return retval
        with open(mb_reg_file, 'r') as fd:
            retval = fd.read()
        return byteTostr(retval)
    except Exception as error:
        log_error("Unable to open " + mb_reg_file + "file !")
    retval = retval.rstrip('\r\n')
    retval = retval.lstrip(" ")
    #log_debug(retval)
    return retval

def waitForDocker(need_restart=False):
    time_cnt = 0
    while True:
        try:
            ret, status = rj_os_system("docker ps |wc -l")
            if ret == 0 and int(status) >= 9:
                break
            else:
                sys.stdout.write(".")
                sys.stdout.flush()
                time_cnt = time_cnt + 1
                time.sleep(1)
                if (need_restart == True):
                    if (time_cnt >= 120 and time_cnt%10 == 0):
                        if (time_cnt >= 180):
                            restartDockerService(True)
                        else:
                            restartDockerService()
        except Exception as e:
            continue

def waitForSDK():
    timeout = 300
    while timeout > 0:
        try:
            ret, status = SdkCmdCase.test_sdk()
            if ret != 0 :
                sys.stdout.write(".")
                sys.stdout.flush()
                timeout -= 1
                time.sleep(1)
            else:
                break
        except Exception as e:
            log_debug(str(e))
            continue

def fac_init_cardidcheck():
    rest = getsyseeprombyId(TLV_CODE_RJ_CARID)  # 判断cardId是否相同
    if rest == None:
        print("需要烧写bin文件")
        return False
    else:
        rest_v = rest['value']
        value = int(rest_v, 16)
        if value == RUIJIE_CARDID:
            log_debug("板卡ID检测通过")
        else:
            log_debug("板卡ID有误")
            return False
    return True

def get_sys_eeprom():
    onietlv = onie_tlv()
    ret, binval_bytes = dev_file_read(MAILBOX_DIR + rg_eeprom, 0, 256)
    if ret is False:
        print("eeprom read error, eeprom path: %s, msg: %s" % (MAILBOX_DIR + rg_eeprom, binval_bytes))
        return []
    binval = byteTostr(binval_bytes)
    return onietlv.decode(binval)


def getsyseeprombyId(id):  # 根据ID获取系统系统
    ret = get_sys_eeprom()
    for item in ret:
        if item["code"] == id:
            return item
    return None

def test_tbd():
    RJPRINT("待实现")
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    return RET

def test_pass():
    RJPRINT("")
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    return RET

def set_port_mac_lb():
    ret = SdkCmdCase.set_port_mac_lb()
    if ret is False:
        RJPRINT("FAILED")
        return False, "配置回环失败"
    time.sleep(6)
    return True, ""

def cancel_port_mac_lb():
    ret = SdkCmdCase.cancel_port_mac_lb()
    if ret is False:
        RJPRINT("取消配置回环失败")
        return False, "取消配置回环失败"
    time.sleep(6)
    return True, ""

def test_PCIe_stress():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    ''' old code backup'''
    '''
    totalerr = 0
    test_times = 3
    try:
        for i in range(0, test_times):
           RJPRINT("\n\n第 %d/%d 次测试"%(i+1, test_times))
           RET1 = test_portframe()
           totalerr += RET1[RETURN_KEY1]
           RET[RETURN_KEY2] += str(RET1[RETURN_KEY2])
    except Exception as e:
        totalerr = -999
        RET[RETURN_KEY2] = str(e)
    if totalerr < 0:
       RET[RETURN_KEY1] = -1
    return RET
    '''
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    for i in range(3):
        if "mft_port" in TESTCASE:
            log = ""
            obj = PortTestCall(port_list_val=[], redirect=True)
            ret, val_dit = obj.port_frame_test()
            log = analy_port_result(val_dit)
        else:
            ret, log = test_port_portframe()
        if ret is False:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = log
            break
    RJPRINT(log)
    return RET

def test_PCIe_mac_stress():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    pcie_stress_cmd = TESTCASE.get("PCIE_STRESS_CMD", None)
    if pcie_stress_cmd == None :
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "获取pcie_stree_cmd配置错误"
        RJPRINT("%s" % RET[RETURN_KEY2])
        return False,""
    for i in range(0, 10):
        for item in pcie_stress_cmd:
            cmd_name = item["cmd_name"]
            delay = item.get("delay",0)
            ignore = item.get("ignore",0)
            if cmd_name is None:
                    RET[RETURN_KEY2] = "获取命令字为空"
                    RJPRINT("%s" % RET[RETURN_KEY2])
                    return False,""
            retrytimes = 3
            while retrytimes > 0:
                ret, log = log_os_system(cmd_name, 0)
                if ret :
                    RJPRINT("FAILED")
                    RET[RETURN_KEY1] = -1
                    RET[RETURN_KEY2]= "PCIE 无数据活动"
                    RJPRINT("%s" % RET[RETURN_KEY2])
                    return RET
                log_debug("log:%s" % log)
                if ignore == 1:    # 是否指令继续往下处理
                    time.sleep(delay)
                    break

                for line in log.splitlines():
                    pcie_speed = line.split()
                    for j in range(len(pcie_speed)):
                        if item["flag"] in pcie_speed[j]:
                            p = re.compile(r'[(](.*?)[)]', re.S)
                            a=re.findall(p, pcie_speed[j])
                            if (len(a) > 0) and (int(a[0]) > 0) :
                                RJPRINT("PCIE 第%d min 监控带宽为%f Gbps" % (i+1,(float(a[0])*8*9000)/(10*1024*1024*1024)))
                                retrytimes = 0
                            else :
                                if retrytimes == 1 :
                                    RET[RETURN_KEY1] = -1
                                    RET[RETURN_KEY2]="PCIE 无数据活动"
                retrytimes = retrytimes-1
                if retrytimes==0 :
                    RET[RETURN_KEY1] = -1
                    RET[RETURN_KEY2]="PCIE 无数据活动"
                    RJPRINT("第%d min PCIE 无数据活动" % (i+1))
                time.sleep(delay)
        time.sleep(60)
    if RET[RETURN_KEY1] < 0 :
        return RET
    if TESTCASE.get("AER_NOCHECK", 0) == 1:
        return RET
    return test_pcie_aer_stress_with_result()

def test_PCIe_huge_stress():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    cmd_name="bcmcmd \"show c\" | grep MC_PERQ_BYTE"
    RJPRINT("MAC PCIE 高带宽数据收发连续测试10 min")
    for i in range(0, 10):
        retrytimes = 3
        while retrytimes > 0:
            ret, log = log_os_system(cmd_name, 0)
            if ret :
                    RJPRINT("FAILED")
                    RET[RETURN_KEY1] = -1
                    RET[RETURN_KEY2]="PCIE 无数据活动"
                    RJPRINT("%s" % RET[RETURN_KEY2])
                    return RET
            for line in log.splitlines():
                pcie_speed = line.split()
                for j in range(len(pcie_speed)):
                    if "(0).cpu0" in pcie_speed[j]:
                        if len(pcie_speed) >= 5:
                            if pcie_speed[4] != None :
                                speed=re.sub("\D", "", pcie_speed[4])
                                RJPRINT("PCIE 第%d min 监控带宽为%ld bps" % (i+1,int(speed)*8))
                                retrytimes = 0
                            else :
                                if retrytimes == 1 :
                                    RET[RETURN_KEY1] = -1
                                    RET[RETURN_KEY2]="PCIE 无数据活动"
                                    RJPRINT("第%d min PCIE 无数据活动" % (i+1))
                        else :
                            if retrytimes == 1 :
                                RET[RETURN_KEY1] = -1
                                RET[RETURN_KEY2]="PCIE 无数据活动"
                                RJPRINT("第%d min PCIE 无数据活动" % (i+1))
            retrytimes = retrytimes-1
            if retrytimes==0 :
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2]="PCIE 无数据活动"
                RJPRINT("第%d min PCIE 无数据活动" % (i+1))
            time.sleep(1)
        time.sleep(60)
    if RET[RETURN_KEY1] < 0 :
        return RET

    return test_pcie_aer_stress_with_result()

def set_port_huge_mac_lb():
    RET = {RETURN_KEY1 : True, RETURN_KEY2 : ""}
    pcie_pre_cmd = TESTCASE.get("PCIE_PRE_CMD", None)
    if pcie_pre_cmd == None :
        RET[RETURN_KEY2] = "获取pcie_pre_cmd配置错误"
        RJPRINT("%s" % RET[RETURN_KEY2])
        return False,""
    for item in pcie_pre_cmd:
        cmd_name = item["cmd_name"]
        if cmd_name is None:
            RET[RETURN_KEY2] = "获取命令字为空"
            RJPRINT("%s" % RET[RETURN_KEY2])
            return False,""
        log_debug("cmd:%s" % cmd_name)
        ret, log = log_os_system(cmd_name, 0)
        if ret :
            RJPRINT("FAILED")
            RET[RETURN_KEY2]="设置命令%s失败" %cmd_name
            RJPRINT("%s" % RET[RETURN_KEY2])
            return False,""
        time.sleep(1)
    time.sleep(10)
    return True,""

def cancel_port_huge_mac_lb():
    RET = {RETURN_KEY1 : True, RETURN_KEY2 : ""}
    pcie_after_cmd = TESTCASE.get("PCIE_AFTER_CMD", None)
    if pcie_after_cmd == None :
        RET[RETURN_KEY2] = "获取pcie_after_cmd配置错误"
        RJPRINT("%s" % RET[RETURN_KEY2])
        return False,""
    for item in pcie_after_cmd:
        cmd_name = item["cmd_name"]
        if cmd_name is None:
            RET[RETURN_KEY2] = "获取命令字为空"
            RJPRINT("%s" % RET[RETURN_KEY2])
            return False,""
        log_debug("cmd:%s" % cmd_name)
        ret, log = log_os_system(cmd_name, 0)
        if ret :
            RJPRINT("FAILED")
            RET[RETURN_KEY2]="设置命令%s失败" %cmd_name
            RJPRINT("%s" % RET[RETURN_KEY2])
            return RET
        time.sleep(1)
    time.sleep(10)
    return True,""

pcie_crorrect_err_dectect = False
pcie_uncrorrect_err_dectect = False
def analyz_pcie_err_stat(log_enable):
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    if not os.access('/sys/kernel/debug/pcieaer/err_stat',os.R_OK):
        RJPRINT("err_stat文件不存在，请确认是否加载AER驱动程序")
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "err_stat文件不存在"
        return RET
    cmd = "cat /sys/kernel/debug/pcieaer/err_stat | grep ')' "
    ret_cmd, log = log_os_system(cmd, 0)
    cmd_name = "cat /sys/kernel/debug/pcieaer/err_stat | grep ']' "
    ret_name, log_name = log_os_system(cmd_name, 0)
    if ret_cmd != 0 or ret_name != 0 :
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "no all pcie err stat"
        return RET;
    for line_name in log_name.splitlines():
        err_name =re.sub("\\[.*?\\]", "", line_name)
        tmp = err_name.split()
        if len(tmp) == 8:
            correct_name=tmp
        elif len(tmp) == 17:
            uncorrect_name=tmp

    for line in log.splitlines():
        #a =re.sub(u"\\(.*?\\)", "", line)
        err_num = line.split()
        for i in range(1,len(err_num)):
            if int(err_num[i]) > 0:
                if len(err_num) == 9:
                    global pcie_crorrect_err_dectect
                    pcie_crorrect_err_dectect=True
                    log_debug("pci id %s correct err detect  %s:%s" % (err_num[0],correct_name[i-1],err_num[i]))
                    if log_enable == True:
                        RJPRINT("pci id %s correct err detect  %s:%s" % (err_num[0],correct_name[i-1],err_num[i]))
                elif len(err_num) == 18:
                    global pcie_uncrorrect_err_dectect
                    pcie_uncrorrect_err_dectect=True
                    log_debug("pci id %s uncorrect err detect %s:%s" % (err_num[0],uncorrect_name[i-1],err_num[i]))
                    if log_enable == True:
                        RJPRINT("pci id %s uncorrect err detect %s:%s" % (err_num[0],uncorrect_name[i-1],err_num[i]))
    return RET

def test_pci_aer_pre():
    ret, log = log_os_system("lsmod | grep pcieaer", 0)
    if not log or ret != 0:
        log_debug("载入pcieaer模块")
        ret, log = log_os_system("modprobe pcieaer", 0)
    return True,""

def test_pcie_aer_stress_show():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    log_debug("查看PCIe错误检测结果")
    global pcie_crorrect_err_dectect
    global pcie_uncrorrect_err_dectect
    test_pci_aer_pre()
    analyz_pcie_err_stat(False)
    if pcie_crorrect_err_dectect == False and pcie_uncrorrect_err_dectect == False :
        RJPRINT("未发现pcie错误")
    else :
        RJPRINT("检测到pcie_aer 错误")
        analyz_pcie_err_stat(True)
        RET[RETURN_KEY1]=-1
        RET[RETURN_KEY2]="检测到pcie_aer 错误"
    return RET

def test_pcie_aer_stress_with_result():
    return test_pcie_aer_stress_show()

def test_iio_pcie_aer_result():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : "No PCIE AER errors detected"}
    total_err = 0
    result = ""
    pcie_aer = TESTCASE.get("PCIE_AER", None)
    if pcie_aer is None :
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "Get PCIE_AER configuration error"
        RJPRINT("%s" % RET[RETURN_KEY2])
        return RET
    for pcie_aer_item in pcie_aer:
        pci_addr = pcie_aer_item.get("pci_addr", None)
        aer_file = pcie_aer_item.get("aer_file", None)
        if pci_addr is None or aer_file is None:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "Get PCIE_AER configuration error"
            RJPRINT("%s" % RET[RETURN_KEY2])
            return RET
        result += "%s:\n" % pci_addr
        for aer_file_item in aer_file:
            name = aer_file_item.get("name", None)
            location = aer_file_item.get("location", None)
            cmd = "cat %s" % location
            ret, log = log_os_system(cmd, 0)
            if ret != 0 or len(log) == 0:
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] = log
                RJPRINT("%s" % RET[RETURN_KEY2])
                return RET
            result += "\t%s:\n" % name
            lines = log.splitlines()
            for line in lines:
                result += "\t\t%s\n" % line
                value = line.split(" ")[-1]
                if int(value) > 0:
                    total_err -= 1
            result += "\n"
    RJPRINT(result)
    if total_err < 0:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "PCIE AER error detected"
    RJPRINT("%s" % RET[RETURN_KEY2])
    return RET
def test_opt_module_present():
    pass_list = []
    failed_list = []
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    empty_str = "      "
    ret, log = log_os_system("show interfaces transceiver presence", 0)
    if "Traceback" in log or len(log) == 0:
        RJPRINT( "在位检测失败，请确认光模块是否在位")
    else:
        dev_list = log.split("\n")
        i = 1
        for dev in dev_list:
            if "Not present" in dev:
                failed_list.append(i)
            elif "Present" in dev:
                pass_list.append(i)
            else:
                log_error(dev)
                continue
            i += 1
        if len(pass_list) > 0:
            port_totalprint(pass_list, "OK")
        if len(failed_list) >0:
            port_totalprint(failed_list, "failed")
        if ret or "FAILED" in log:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = log
    if ret or "Not" in log or "Unknown" in log:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = log
    return RET

def test_cpu_i2c_stress():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : []}
    totalerr = 0
    test_times = 10
    for i in range(0, test_times):
       RJPRINT("\n\nCPU端第 %d/%d 次测试"%(i+1, test_times))
       RET1 = test_i2c()
       totalerr += RET1[RETURN_KEY1]
    if totalerr < 0:
       RET[RETURN_KEY1] = -1
    return RET

def test_bmc_testcase_new(func, param_t=None, timeout = 600):
    if param_t is None:
        ret = HttpRest().Get(getRealUrl(func), timeout=timeout)
    else:
        ret = HttpRest().Get(getRealUrl(func, json.dumps(param_t)), timeout=timeout)
    RJPRINT(ret.get(RETURN_KEY2))
    return ret

def test_bmc_i2c_stress():
    totalerr = 0
    try:
        test_bmc_i2c_open()
        RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
        test_times = 10
        returncode, msg = test_bmc_channel()
        if returncode == False:
            RJPRINT(msg)
            return {RETURN_KEY1 : -1, RETURN_KEY2 : msg}
        RET1 = test_bmc_testcase_new("bmc_test_i2c_stress")
        RET[RETURN_KEY2] += RET1[RETURN_KEY2]
        totalerr += RET1[RETURN_KEY1]
    except Exception as e:
        RJPRINT(str(e))
    finally:
        test_bmc_i2c_close()
    if totalerr < 0:
       RET[RETURN_KEY1] = -1
    return RET

def complement_to_binary(data):
    if data > 127:
        data ^= 0xff
        data += 1
        data = -data
        return data
    else:
        return data

def get_ssd_smart_info():
    cmd = "smartctl --all /dev/sda"
    ret, log = log_os_system("which smartctl", 0)
    if len(log):
        ret1, log1 = log_os_system(cmd, 0)
        if len(log1) <= 0:
            RJPRINT("command[%s] execution error" % cmd)
            return -1, "command[%s] execution error" % cmd
        return 0, log1
    else:
        return -1, "no smartctl cmd"

def test_ssd_smart_info():
    '''SSD Smart属性打印'''
    RET = {RETURN_KEY1 : -1, RETURN_KEY2 : ""}
    ret, smart_info = get_ssd_smart_info()
    if ret != 0 or len(smart_info) == 0:
        RET[RETURN_KEY2] = "Failed to get SSD Smart information"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    RJPRINT(smart_info)
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    return RET

def test_ssd_smart_attrs():
    '''SSD Smart属性阈值检测'''
    RET = {RETURN_KEY1 : -1, RETURN_KEY2 : ""}
    ssd = None
    model = ""
    attr_found = False
    total_err = 0
    ret, smart_info = get_ssd_smart_info()
    if ret != 0 or len(smart_info) == 0:
        RET[RETURN_KEY2] = "Failed to get SSD Smart information"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    lines = smart_info.replace("\t", "").strip().split("\n")
    for line in lines:
        if line.startswith("Device Model:"):
            model = line.split(":")[1].strip()
            for ssd_item in SSD_ATTR_LIST:
                if ssd_item["model"] in model:
                    ssd = ssd_item
                    break
            if ssd is None:
                RET[RETURN_KEY2] = "Unknown SSD model: %s" % model
                RJPRINT(RET[RETURN_KEY2])
                return RET
        if not attr_found and "ATTRIBUTE_NAME" in line:
            attr_found = True
            continue
        if attr_found:
            if "0x0" in line and "-" in line:
                attr = ' '.join(line.split()).split(' ')
                if not attr[0].isdigit() or not attr[9].isdigit():
                    continue
                attr_id = int(attr[0])
                attr_value = int(attr[9])
                for attr_item in ssd["attrs"]:
                    if attr_item["id"] == attr_id:
                        if attr_item["attr_name"] == "Bad block increase number":
                            pass
                        elif attr_item["attr_name"] == "Write failures times":
                            pass
                        elif attr_item["attr_name"] == "Erase failed test":
                            pass
                        elif attr_item["attr_name"] == "Remaining life":
                            attr_value = int(attr[3])
                            RJPRINT("%s : %d%%" % (attr_item["attr_name"], attr_value))
                            if attr_value < attr_item["life"]:
                                total_err -= 1
                                RJPRINT("The remaining life of the SSD is insufficient: %d%%" % attr_value)
                        elif attr_item["attr_name"] == "PLP capacity":
                            pass
                        elif attr_item["attr_name"] == "SATA CRC":
                            RJPRINT("%s : %d" % (attr_item["attr_name"], attr_value))
                            if attr_item.get("ignore", 1) == 1:
                                continue
                            if attr_value > attr_item["critical"]:
                                total_err -= 1
                                RJPRINT("The attribute value of SATA CRC[%d] is more than the critical value: %d" % (attr_value, attr_item["critical"]))
                            elif attr_value > attr_item["warning"]:
                                log_warning("The attribute value of SATA CRC[%d] is more than the warning value: %d" % (attr_value, attr_item["warning"]))
                        elif attr_item["attr_name"] == "SATA spin down":
                            RJPRINT("%s : %d" % (attr_item["attr_name"], attr_value))
                            if attr_item.get("ignore", 0) == 1:
                                continue
                            if attr_value > attr_item["critical"]:
                                total_err -= 1
                                RJPRINT("The attribute value of SATA spin down[%d] is more than the critical value: %d" % (attr_value, attr_item["critical"]))
                            elif attr_value > attr_item["warning"]:
                                log_warning("The attribute value of SATA spin down[%d] is more than the warning value: %d" % (attr_value, attr_item["warning"]))
                        elif attr_item["attr_name"] == "E2E error":
                            RJPRINT("%s : %d" % (attr_item["attr_name"], attr_value))
                            if attr_value > attr_item["critical"]:
                                total_err -= 1
                                RJPRINT("The attribute value of E2E error[%d] is more than the critical value: %d" % (attr_value, attr_item["critical"]))
                            elif attr_value > attr_item["warning"]:
                                log_warning("The attribute value of E2E error[%d] is more than the warning value: %d" % (attr_value, attr_item["warning"]))
                        elif attr_item["attr_name"] == "Temperature":
                            if attr_item.get("convert", False):
                                attr_value = complement_to_binary(attr_value)
                            RJPRINT("%s : %d" % (attr_item["attr_name"], attr_value))
                            if attr_item.get("ignore", 1) == 1:
                                continue
                            if attr_value <= attr_item["min"] or attr_value >= attr_item["max"]:
                                total_err -= 1
                                RJPRINT("The temperature of the SSD is abnormal, current temperature is: %d" % attr_value)
                        else:
                            pass
            else:
                break
    if len(model):
        RET[RETURN_KEY1] = total_err
    else:
        RET[RETURN_KEY2] = "SSD model not found"
        RJPRINT(RET[RETURN_KEY2])
    return RET

def test_ssd_health():
    '''SSD Smart健康状态检测'''
    RET = {RETURN_KEY1 : -1, RETURN_KEY2 : ""}
    cmd = "smartctl -H /dev/sda"
    ret, log = log_os_system("which smartctl", 0)
    if len(log):
        ret1, log1 = log_os_system(cmd, 0)
        if len(log1) <= 0:
            RJPRINT("command[%s] execution error" % cmd)
            return -1, "command[%s] execution error" % cmd
        RJPRINT(log1)
        if "PASSED" in log1:
            RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
            return RET
        else:
            RET[RETURN_KEY2] = "SSD health status is abnormal"
            RJPRINT(RET[RETURN_KEY2])
            return RET
    else:
        RET[RETURN_KEY2] = "no smartctl cmd"
        return RET

def test_sata_abnormal():
    '''SATA接口异常拦截'''
    RET = {RETURN_KEY1 : -1, RETURN_KEY2 : ""}
    cmd = "dmesg"
    ret, log = log_os_system(cmd, 0)
    if len(log):
        if "SError" in log:
            RET[RETURN_KEY2] = "SATA interface SError exception"
            RJPRINT(RET[RETURN_KEY2])
        else:
            RET[RETURN_KEY1] = 0
            RJPRINT("SATA interface has no SError log")
    else:
        RET[RETURN_KEY2] = "command[%s] execution error" % cmd
        RJPRINT(RET[RETURN_KEY2])
    return RET

ssd_test_status = 0  # 0 undo 1 doing
ssd_status = 0 # 0 undo 1 doing 2 done 3 stopping
def test_ssd_stress():
    RET = {RETURN_KEY1 : 1, RETURN_KEY2 : "已启动后台执行"}
    cmd = "smartctl -t long  /dev/sda"
    global ssd_test_status
    global ssd_status
    if ssd_status == 1:
        RET[RETURN_KEY2] = "已存在后台ssd测试"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    if ssd_test_status ==  1:
        RET[RETURN_KEY2] = "存在FIO性能测试任务，请等FIO性能测试结束并查看测试结果后再执行SSD压力测试"
        RJPRINT(RET[RETURN_KEY2])
        return RET

    ret, log = log_os_system("which smartctl", 0)
    if len(log):
        # smartctl 自带后台检测
        # 需要通过smartctl -l selftest  /dev/sda 查看
        tmp_str01 = "Please wait "
        tmp_str02 = " minutes"
        # 停止可能的已存在的smartctl测试，避免获取执行时间失败
        log_os_system("smartctl -X /dev/sda", 0)
        ret, log = log_os_system(cmd, 0)
        if len(log):
            RJPRINT(log)
            try:
                index_start = log.find(tmp_str01) + len(tmp_str01)
                index_end = log.find(tmp_str02)
                run_time = log[index_start: index_end].strip(" ").strip("\n")
                run_time = int(run_time) * 60
                ssd_test_status = 1
                ssd_status = 1
            except  Exception as e:
                ret, log = log_os_system("smartctl -X /dev/sda", 0)
                if("Self-testing aborted!" in log):
                    RJPRINT("获取测试执行时间错误，SSD压力测试已停止")
                else:
                    RJPRINT("获取测试执行时间错误，且停止SSD压力测试失败！")
                RET[RETURN_KEY2] = "get smartctl run_time fail"
                RET[RETURN_KEY1] = -1
    else:
        RJPRINT("设备缺少smartctl工具，无法执行测试项")
        RET[RETURN_KEY2] = "no smartctl cmd"
        RET[RETURN_KEY1] = -1
    if(RET[RETURN_KEY1] == 1):
        RJPRINT(RET[RETURN_KEY2])
    return RET

def test_ssd_short_stress():
    RET = {RETURN_KEY1 : 1, RETURN_KEY2 : "已启动后台执行"}
    cmd = "smartctl -t short  /dev/sda"
    global ssd_test_status
    global ssd_status
    if ssd_status == 1:
        RET[RETURN_KEY2] = "已存在后台ssd测试"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    if ssd_test_status ==  1:
        RET[RETURN_KEY2] = "存在FIO性能测试任务，请等FIO性能测试结束并查看测试结果后再执行SSD压力测试"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    ret, log = log_os_system("which smartctl", 0)
    if len(log):
        tmp_str01 = "Please wait "
        tmp_str02 = " minutes"
        log_os_system("smartctl -X /dev/sda", 0)
        ret, log = log_os_system(cmd, 0)
        if len(log):
            RJPRINT(log)
            try:
                index_start = log.find(tmp_str01) + len(tmp_str01)
                index_end = log.find(tmp_str02)
                run_time = log[index_start: index_end].strip(" ").strip("\n")
                run_time = int(run_time) * 60
                ssd_test_status = 1
                ssd_status = 1
            except  Exception as e:
                ret, log = log_os_system("smartctl -X /dev/sda", 0)
                if("Self-testing aborted!" in log):
                    RJPRINT("获取测试执行时间错误，SSD压力测试已停止")
                else:
                    RJPRINT("获取测试执行时间错误，且停止SSD压力测试失败！")
                RET[RETURN_KEY2] = "get smartctl run_time fail"
                RET[RETURN_KEY1] = -1
    else:
        RJPRINT("设备缺少smartctl工具，无法执行测试项")
        RET[RETURN_KEY2] = "no smartctl cmd"
        RET[RETURN_KEY1] = -1
    if(RET[RETURN_KEY1] == 1):
        RJPRINT(RET[RETURN_KEY2])
    return RET

def abort_ssd_stress():
    global ssd_test_status
    global ssd_status
    RET = {RETURN_KEY1 : 1,  RETURN_KEY2 : ""}
    cmd = "smartctl -X /dev/sda"

    ret, log = log_os_system("which smartctl", 0)
    if len(log):
        # smartctl 自带后台检测
        # 需要通过smartctl -l selftest  /dev/sda 查看
        if(ssd_status == 1):
            os.system(cmd)
            ssd_test_status = 0
            ssd_status = 3
            time.sleep(1)
            RET[RETURN_KEY2] = "该后台测试已被终止"
        else:
            RET[RETURN_KEY2] = "无后台测试在运行"
    else:
        RET[RETURN_KEY2] = "no smartctl cmd"
    RJPRINT(RET[RETURN_KEY2])
    return RET

def force_abort_ssd_stress():
    log_os_system("smartctl -X /dev/sda", 0)

def get_ssd_stress_result():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    global ssd_test_status
    global ssd_status
    if ssd_status == 0:
        RET = {RETURN_KEY1: 1, RETURN_KEY2: "未执行后台ssd测试"}
        RJPRINT(RET[RETURN_KEY2])
        return RET
    ret, log = log_os_system("which smartctl", 0)
    if len(log):
        cmd = "smartctl -c /dev/sda"
        ret, log = rj_os_system(cmd)
        if len(log):
            if "Self-test routine in progress..." in log:
                RET = {RETURN_KEY1: 1, RETURN_KEY2: "后台ssd测试还未结束，请稍等"}
                RJPRINT(RET[RETURN_KEY2])
                return RET
            elif "The self-test routine was aborted" in log:
                ssd_test_status = 0
                ssd_status = 3
                RET = {RETURN_KEY1: 1, RETURN_KEY2: "后台ssd测试未完成被强制终止"}
                RJPRINT(RET[RETURN_KEY2])
                return RET
            else:
                ssd_test_status = 0
                ssd_status = 2
        else:
            RET[RETURN_KEY1] = -1;
            RET[RETURN_KEY2] = "命令执行出错[%s]" % cmd
            RJPRINT(RET[RETURN_KEY2])
            return RET

        cmd = "smartctl -l selftest /dev/sda"
        ret, logout = rj_os_system(cmd)
        tmpval = ''
        for line in logout.splitlines():
            if "# 1" in line:
                tmpval = line
                break
        if tmpval == '' or 'Completed without error' not in tmpval:
            RJPRINT(logout)
            RET[RETURN_KEY1] =  -1
            RET[RETURN_KEY2] =  logout
        else:
            RJPRINT(tmpval)
            RET[RETURN_KEY1] = 0
    else:
        RET[RETURN_KEY2] = "no smartctl cmd"
    ssd_status = 0
    # RJPRINT(RET[RETURN_KEY2])
    return RET

fio_test_file = "/tmp/fio_test"
fio_test_thread = None
fio_test_status = 0      # 0 undo 1 doing 2 done 3 stopping 4 error
fio_test_result = ""
def process_fio_test(param):
    global fio_test_status
    global fio_test_result
    fio_test_result = ""
    ssd_fio = TESTCASE.get("SSD_FIO", None)
    if ssd_fio == None :
        RJPRINT("获取SSD_FIO配置错误")
        return
    ssd_fio_case = ssd_fio.get(param, None)
    if ssd_fio_case == None :
        RJPRINT("找不到指定的FIO配置")
        return
    for fio_item in ssd_fio_case:
        rw = fio_item.get("rw", None)
        bs = fio_item.get("bs", None)
        rwmixwrite = fio_item.get("rwmixwrite", None)
        iodepth = fio_item.get("iodepth", None)
        size = fio_item.get("size", None)
        name = fio_item.get("name", None)
        verify = fio_item.get("verify", None)
        do_verify = fio_item.get("do_verify", None)
        cmd = "fio -rw=%s -bs=%s -rwmixwrite=%d -iodepth=%d -size=%s -verify=%s -do_verify=%d -verify_fatal=1 -verify_state_save=0 -name=%s -filename=%s" % (rw, bs, rwmixwrite, iodepth, size, verify, do_verify, name, fio_test_file)
        ret, log = log_os_system(cmd, 0)
        if fio_test_status != 1 :
            if os.path.exists(fio_test_file) :
                os.remove(fio_test_file)
            return
        if ret != 0 :
            fio_test_status = 4
            fio_test_result = log
            if os.path.exists(fio_test_file) :
                os.remove(fio_test_file)
            return
        fio_test_result += name + " :\n"
        index = log.find("read", 0)
        if index != -1:
            fio_test_result += "\tRead : "
            iops_index = log.find("iops=", index)
            if iops_index == -1:
                iops_index = log.find("IOPS=", index)
            if iops_index != -1:
                iops = log[iops_index : log.find(",", iops_index)]
                fio_test_result += iops + "\n"
        index = log.find("write", 0)
        if index != -1:
            fio_test_result += "\tWrite : "
            iops_index = log.find("iops=", index)
            if iops_index == -1:
                iops_index = log.find("IOPS=", index)
            if iops_index != -1:
                iops = log[iops_index : log.find(",", iops_index)]
                fio_test_result += iops + "\n"
    if os.path.exists(fio_test_file) :
        os.remove(fio_test_file)
    fio_test_status = 2
def test_fio(param):
    RET = {RETURN_KEY1 : 1, RETURN_KEY2 : ""}
    global ssd_test_status
    global fio_test_thread
    global fio_test_status
    if fio_test_status == 1:
        RET[RETURN_KEY2] = "已有FIO后台执行任务，请首先查看测试结果或终止上次测试任务"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    if ssd_test_status ==  1:
        RET[RETURN_KEY2] = "存在SSD后台压力测试任务，请等SSD后台压力测试结束并查看测试结果后再执行FIO性能测试"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    ret, log = log_os_system("which fio", 0)
    if len(log):
        ssd_test_status = 1
        fio_test_status = 1
        fio_test_thread = threading.Thread(target=process_fio_test, args=(param,))
        fio_test_thread.setDaemon(True)
        fio_test_thread.start()
        RET[RETURN_KEY2] = "已启动后台执行"
    else:
        RET[RETURN_KEY2] = "no fio cmd"
    RJPRINT(RET[RETURN_KEY2])
    return RET
def test_fio_stop():
    RET = {RETURN_KEY1 : 1, RETURN_KEY2 : ""}
    global ssd_test_status
    global fio_test_thread
    global fio_test_status
    if fio_test_status != 1:
        RET[RETURN_KEY2] = "未启动后台测试"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    if not makesure("强行结束将无法查看结果，是否继续？[Yes/No]：",echo = True):
        RET[RETURN_KEY2] = "已撤销"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    ssd_test_status = 0
    fio_test_status = 3
    ret, log = log_os_system("ps -ef | grep fio | grep -v grep | awk '{print $2}' | xargs kill -9", 0)
    if fio_test_thread != None :
        fio_test_thread.join()
        fio_test_thread = None
    RET[RETURN_KEY2] = "该后台测试已被终止"
    RJPRINT(RET[RETURN_KEY2])
    return RET
def force_abort_fio():
    cmd = "ps -ef | grep fio | grep -v grep | awk '{print $2}' | xargs kill -9 && rm -rf %s" % fio_test_file
    log_os_system(cmd, 0)
def get_fio_result():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    global ssd_test_status
    global fio_test_thread
    global fio_test_status
    global fio_test_result

    if fio_test_status == 0 or fio_test_status == 3:
        RET = {RETURN_KEY1: 1, RETURN_KEY2: "未启动后台测试，没有测试结果"}
        RJPRINT(RET[RETURN_KEY2])
        return RET
    elif fio_test_status == 1:
        RET = {RETURN_KEY1: 1, RETURN_KEY2: "后台FIO性能校验测试还未结束，请稍等"}
        RJPRINT(RET[RETURN_KEY2])
        return RET
    elif fio_test_status == 4 :
        ssd_test_status = 0
        fio_test_status = 0
        RET = {RETURN_KEY1: -1, RETURN_KEY2: fio_test_result}
        RJPRINT(RET[RETURN_KEY2])
        return RET

    RET[RETURN_KEY2] = fio_test_result
    RJPRINT(RET[RETURN_KEY2])
    ssd_test_status = 0
    fio_test_thread = None
    fio_test_status = 0
    fio_test_result = ""
    return RET
def test_kr_stress():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    totalerr = 0
    test_times = 10
    for i in range(0, test_times):
        print("\n\n第 %d/%d 次测试"%(i+1, test_times))
        if "mft_port" in TESTCASE:
            RET1 = test_kr_new()
        else:
            RET1 = test_kr()
        print_temp_flush()
        totalerr += RET1[RETURN_KEY1]
        RET[RETURN_KEY2] += RET1[RETURN_KEY2]
    if totalerr < 0:
       RET[RETURN_KEY1] = -1
    return RET

def test_subprocess_run():
    RET = {RETURN_KEY1 : 1,  RETURN_KEY2 : "开始子进程后台测试"}
    if subprocess_case.is_running() or subprocess_case.is_stopping():
        RET[RETURN_KEY2] = "已存在后台测试"
        RJPRINT(RET[RETURN_KEY2])
    else:
        subprocess_case.start_run_bgtest()
    return RET

def test_subprocess_stop():
    RET = {RETURN_KEY1: 1, RETURN_KEY2: "结束子进程后台测试"}
    if subprocess_case.is_running():
        subprocess_case.shutdown_bgtest()
    else:
        RJPRINT("未进行后台测试")
        #退出
    return RET

def test_subprocess_result():
    RET = {RETURN_KEY1: 1, RETURN_KEY2: "查看子进程后台测试结果"}
    if subprocess_case.is_undo():
        res = subprocess_case.get_all_message()
        if res == "":
            RJPRINT("未执行后台测试")
            return RET
        else:
            RJPRINT(res)
        if "FAIL" in res:
            RET[RETURN_KEY1] = -1
        else:
            RET[RETURN_KEY1] = 0
    else:
        RJPRINT("后台测试正在运行，请稍后查看")
    return RET

class setPortLog():
    log_also_print_to_console = None
    cmd_also_print_to_console = None
    cmd_output_also_print_to_console = None
    port_log_info_print_to_console = None
    sdk_cmd_redirect_console = None
    def __init__(self):
        self.log_also_print_to_console = PortLog.get_log_also_print_to_console()
        self.cmd_also_print_to_console = PortLog.get_cmd_also_print_to_console()
        self.cmd_output_also_print_to_console = PortLog.get_cmd_output_also_print_to_console()
        self.port_log_info_print_to_console = PortLog.get_port_log_info_print_to_console()
        self.sdk_cmd_redirect_console = PortLog.get_sdk_cmd_redirect_console
    def all_print_close(self):
        PortLog.set_log_also_print_to_console(False)
        PortLog.set_cmd_also_print_to_console(False)
        PortLog.set_cmd_output_also_print_to_console(False)
        PortLog.set_port_log_info_print_to_console(False)
        PortLog.set_sdk_cmd_redirect_console(False)
    def all_print_open(self):
        PortLog.set_log_also_print_to_console(True)
        PortLog.set_cmd_also_print_to_console(True)
        PortLog.set_cmd_output_also_print_to_console(True)
        PortLog.set_port_log_info_print_to_console(True)
        PortLog.set_sdk_cmd_redirect_console(True)
    def all_print_reset(self):
        PortLog.set_cmd_output_also_print_to_console(self.cmd_output_also_print_to_console)
        PortLog.set_port_log_info_print_to_console(self.port_log_info_print_to_console)
        PortLog.set_sdk_cmd_redirect_console(self.sdk_cmd_redirect_console)
        PortLog.set_log_also_print_to_console(self.log_also_print_to_console)
        PortLog.set_cmd_also_print_to_console(self.cmd_also_print_to_console)
class BackgroundOperation(setPortLog):
    UNDO             = 0 # 未执行后台测试项
    DOING            = 1 # 正在后台运行测试项
    STOPPING         = 2 # 正在关闭后台测试项
    StatusFlag       = None # 子进程当前状态
    lock             = None #  共享内存锁
    message          = None #  存放测试log
    bgmenulist       = None #  后台测试的菜单列表
    subprocess_obj   = None #  子进程

    def __init__(self):
        self.lock = multiprocessing.Lock()
        self.StatusFlag = multiprocessing.Value('i', self.UNDO) #初始undo
        self.message = multiprocessing.Queue()
        self.bgmenulist = TESTCASE.get("BackgroundMenuList", None)

    @staticmethod
    def paren_proce_status(): #子进程开个线程判断父进程是否异常退出(被1号进程接管),异常退出则跟着退出
        while True:
            log_debug("subprocess ppid %d" % os.getppid())
            if os.getppid() == 1:
                log_debug("parent process  aborted, kill subprocess self")
                cmd = "kill -9 %d" % os.getpid()
                os.system(cmd)
            time.sleep(1)
    def subprocess_real(self):
        RET = {RETURN_KEY1: -1, RETURN_KEY2: ""}
        thread_tmp = threading.Thread(target=BackgroundOperation.paren_proce_status)
        thread_tmp.setDaemon(True)
        thread_tmp.start()
        self.get_all_message()  # 清空queue
        data = self.bgmenulist
        self.all_print_close()
        try:
            totalresult = ""
            if data is None:
                self.put_message("获取后台测试用例错误")
                self.turn_undo()
                return RET
            for item in data:  # todo 考虑测试项前置后置项
                if self.is_stopping():
                    formatstr = "======%%-%ds 因用户终止未执行\n" % ((40 + wide_chars(item[MENUITEMNAME])))
                    totalresult += formatstr % item[MENUITEMNAME]
                    continue
                self.put_message(item[MENUITEMNAME])
                RET = eval(item[MENUITEMDEAL])()
                if RET[RETURN_KEY1] == 0:
                    self.put_message("Test Result: " + SUCCESS_TIPS + '\n\n')
                    formatstr = "======%%-%ds Test Result: %s\n" % ((40 + wide_chars(item[MENUITEMNAME])), SUCCESS_TIPS)
                    totalresult += formatstr % (item[MENUITEMNAME])
                elif RET[RETURN_KEY1] == 1:
                    pass
                elif RET[RETURN_KEY1] == -1:
                    self.put_message("Test Result: FAIL" + '\n\n')
                    formatstr = "======%%-%ds Test Result: FAIL\n" % ((40 + wide_chars(item[MENUITEMNAME])))
                    totalresult += formatstr % item[MENUITEMNAME]
                self.put_message("==============================================================")
            self.put_message(totalresult)
        except Exception as e:
            msg = traceback.format_exc()
            self.put_message(msg)
            self.turn_undo()
        self.turn_undo()
        self.all_print_reset()
        return RET

    def start_run_bgtest(self):
        self.turn_doing()
        self.subprocess_obj = multiprocessing.Process(target=self.subprocess_real)
        self.subprocess_obj.daemon = True
        self.subprocess_obj.start()
        print("已开始后台测试，部分测试项不可访问")

    def put_message(self, str, newline = True):
        if newline:
            self.message.put(str + '\n')
        else:
            self.message.put(str)

    def get_message(self):
        return self.message.get()

    def get_all_message(self):
        tmp = ""
        while not self.message.empty():
            tmp += self.get_message()
        return tmp

    def turn_doing(self):
        with self.lock:
            self.StatusFlag.value = self.DOING

    def turn_undo(self):
        with self.lock:
            self.StatusFlag.value = self.UNDO

    def turn_stoping(self):
        with self.lock:
            self.StatusFlag.value = self.STOPPING

    def is_running(self):
        with self.lock:
            if self.StatusFlag.value == self.DOING:
                return True
            else:
                return False

    def is_undo(self):
        with self.lock:
            if self.StatusFlag.value == self.UNDO:
                return True
            else:
                return False

    def is_stopping(self):
        with self.lock:
            if self.StatusFlag.value == self.STOPPING:
                return True
            else:
                return False

    def print_bgtest_name(self, newline =True):#打印需要后台运行的测试项
        tmp = ""
        for item in self.bgmenulist:
            tmp += item[MENUITEMNAME]
            if newline:
                tmp += "\n"
        return tmp

    def print_result(self, str):
        if self.is_undo():
            print(str)
        else:
            self.put_message(str)

    def shutdown_bgtest(self):
        with self.lock:
            if self.StatusFlag.value == self.DOING:
                print("正在等待后台进程结束，请稍等")
                self.StatusFlag.value = self.STOPPING
        while self.is_stopping():
            print(".", end=' ')
            sys.stdout.flush()
            time.sleep(2)

subprocess_case = BackgroundOperation()

def print_menulist_before_choose():
    RJPRINT("以下测试项将进入后台测试：")
    RJPRINT(subprocess_case.print_bgtest_name())
    return True, ''

def test_opt_module_e2_read():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    pass_list = []
    failed_list = []
    dev_list1 = []
    dev_list2 = []
    dev_list3 = []
    dev_list4 = []
    dev_list5 = []
    empty_str = "      "
    temp_id = 0

    ret, log = log_os_system("show interfaces transceiver eeprom", 0)
    if ret:
        RET[RETURN_KEY1] = -1
        RJPRINT("获取光模块信息失败")
        return RET
    dev_list1 = log.split("\n")

    # get e2_info and opt_module_name
    for i in range(len(dev_list1)):
        ret = ''.join(re.findall('EEPROM detected', dev_list1[i]))
        if ret:
            dev_list2.append(ret)
        ret = ''.join(re.findall('Vendor.*Name:.*', dev_list1[i]))
        if ret:
            dev_list3.append(ret)
        if FACTESTMODULE.get("eeprom_pn_sn_show", 0) == 1:
            ret = ''.join(re.findall('PN:.*', dev_list1[i]))
            if ret:
                dev_list4.append(ret)
            else:
                ret = ''.join(re.findall('Part Number:.*', dev_list1[i]))
                if ret:
                    dev_list4.append(ret)
            ret = ''.join(re.findall('SN:.*', dev_list1[i]))
            if ret:
                dev_list5.append(ret)
                RJPRINT("%03d : %s          %s "%(temp_id + 1, dev_list4[temp_id], dev_list5[temp_id]))
                temp_id = temp_id + 1
            else:
                ret = ''.join(re.findall('Serial Number:.*', dev_list1[i]))
                if ret:
                    dev_list5.append(ret)
                    RJPRINT("%03d : %s          %s "%(temp_id + 1, dev_list4[temp_id], dev_list5[temp_id]))
                    temp_id = temp_id + 1

    RJPRINT("")
    len_opt_e2 = len(dev_list2)
    len_opt_name = len(dev_list3)
    if len_opt_e2 != len_opt_name or len_opt_e2 == 0 or len_opt_name == 0:
        RET[RETURN_KEY1] = -1
        RJPRINT("光模块E2信息或名称信息获取个数，不正确或不相等")
        RJPRINT("光模块E2信息获取个数：%s" %(len_opt_e2))
        RJPRINT("光模块名称信息获取个数：%s" %(len_opt_name))
        RJPRINT("%s" %(log))
        return RET


    # filter e2_info and opt_module_name
    for i in range(len_opt_e2):
        dev_list2[i], times = re.subn("SFP EEPROM detected","PASS",dev_list2[i])
        dev_list2[i], times = re.subn("SFP EEPROM not detected","FAILED",dev_list2[i])
        dev_list2[i], times = re.subn("Ethernet\d{1,3}:","",dev_list2[i])
        dev_list2[i], times = re.subn(" ","",dev_list2[i])

        dev_list3[i], times = re.subn("Vendor.*Name:","",dev_list3[i])
        dev_list3[i], times = re.subn("\\t","",dev_list3[i])
        dev_list3[i], times = re.subn(" ","",dev_list3[i])
        dev_list3[i] = dev_list3[i].strip('\x00')

    # print e2_info and opt_module_name as pass or fail
    for i in range(len_opt_e2):
        if len(dev_list2[i]) == 0 or "FAILED" in dev_list2[i]:
            failed_list.append(i+1)
        elif len(dev_list3[i]) == 0:
            failed_list.append(i+1)
        else:
            pass_list.append(i+1)
    if len(pass_list) >0:
        port_totalprint(pass_list, "OK")
    if len(failed_list) > 0:
        port_totalprint(failed_list, "failed")
        tmpstr = '\nFAILED:\n'
        tmpstr += empty_str
        for i in range(len(failed_list)):
            tmpstr +="%-5s"% failed_list[i]
            if((i + 1) %8 == 0):
                tmpstr +="\n"
                tmpstr += empty_str
        tmpstr += ""
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = tmpstr
        RJPRINT("%s" %(log))
        return RET

    return RET

def get_port_num():
    port_optoe_dict = TESTCASE.get("optoe_port_map", None)
    port_num = port_optoe_dict.get("port_num", 0)
    if port_num <= 0:
        msg = "OPTOE_PORT_MAP port_num config error, port_num: %d!" % port_num
        return False, msg
    return True, port_num

def get_port_path(port):
    port_optoe_dict = TESTCASE.get("optoe_port_map", None)
    port_num = port_optoe_dict.get("port_num", 0)
    if port_num <= 0:
        msg = "OPTOE_PORT_MAP port_num config error, port_num: %d!" % port_num
        return False, msg

    if port <= 0 or port > port_num:
        msg = "port out of range !"
        return False, msg

    port_bus_map = port_optoe_dict.get("port_bus_map")
    optoe_start_bus = port_optoe_dict.get("optoe_start_bus", 0)
    if port_bus_map is None: # get port bus by optoe_start_bus
        if optoe_start_bus <= 0:
            msg = "OPTOE_PORT_MAP optoe_start_bus config error, optoe_start_bus: %d" % optoe_start_bus
            return False, msg
        port_bus = port + optoe_start_bus - 1
    else: # get port bus by port_bus_map
        port_bus = port_bus_map.get(port)
        if port_bus is None:
            msg = "port %d don't has i2c bus" % port
            return False, msg
        if not isinstance(port_bus, int) or port_bus < 0:
            msg = "port %d i2c bus config error, port_bus: %s " % port_bus
            return False, msg
    return True, port_bus

def test_sff_present_status():
    pass_list = []
    failed_list = []
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    empty_str = "      "
    ret, port_num = get_port_num()
    if ret is False:
        RJPRINT("msg: %s, exit test_sff_present_status" % port_num)
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = port_num
        return RET

    for index in range(port_num):
        i = index + 1
        sff_present_loc = "/sys/s3ip/transceiver/eth%d/present" % i
        sff_present_conf = {"gettype": "sysfs", "loc": sff_present_loc}
        ret, present = get_value(sff_present_conf)
        if ret is False:
            RJPRINT("msg: %s, get %s failed" % (present, sff_present_loc))
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = present
            return RET
        if not present:
            ret, bus = get_port_path(i)
            if ret == False:
                RJPRINT( "Ethernet%d Not present,i2c bus address get error " % (i))
            if isinstance(bus, int):
                ret, val = rji2cget(bus, 0x50, 0x1)
                if ret == True:
                    RJPRINT( "Ethernet%-20d Not present,but eeprom read ok, Fail " % (i))
                    failed_list.append(i)
                else:
                    RJPRINT( "Ethernet%-20d Not present,eeprom NA, PASS " % (i))
                    pass_list.append(i)
            else:
                failed_list.append(i)
        else:
            ret1, bus1 = get_port_path(i)
            if ret1 == False:
                RJPRINT( "Ethernet%d Present,i2c bus address get error " % (i))
            if isinstance(bus1, int):
                ret1, val1 = rji2cget(bus1, 0x50, 0x1)
                if ret1 == True:
                    RJPRINT( "Ethernet%-20d Present,eeprom read OK, PASS " % (i))
                    pass_list.append(i)
                else:
                    RJPRINT( "Ethernet%-20d Present,eeprom NA , Fail" % (i))
                    failed_list.append(i)
            else:
                failed_list.append(i)

    if len(pass_list) > 0:
        port_totalprint(pass_list, "OK")
    if len(failed_list) >0:
        port_totalprint(failed_list, "failed")
    return RET

def test_lpc():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    errmsg = ''

    items = []
    for item in CPLDVERSIONS:
        if item.get("gettype", None) == 'io':
            items.append(item)

    if len(items) > 0:
        RJPRINT("LPC read/write CPLD test:")

    for it in items:
        addr = it.get('io_addr')
        name = it.get('name')
        testaddr = 0
        RJPRINT(name)
        if name == 'X86_CPLD' or name == 'CPU板CPLD' or name == 'CPU_CPLD':
            testaddr = addr + 0x05
        elif name == 'BASE_CPLD' or name == 'BASE板CPLD':
            testaddr = addr + 0x55
        else:
            testaddr = addr +  0xaa
        for wr_byte in [0x5a,0xa5]:
            ret = io_wr(testaddr, wr_byte)
            ret = io_rd(testaddr)
            if wr_byte != int(ret,16):
                totalerr -= 1
                msg = "    Write value: 0x%x, Read back value: 0x%x"%(wr_byte, int(ret,16))
                RJPRINT(msg)
                RJPRINT("    FAILED")
                errmsg += "%s %s \n" % (errmsg, msg)
            else:
                msg = "    Write value: 0x%x, Read back value: 0x%x"%(wr_byte, int(ret,16))
                RJPRINT(msg)
                RJPRINT("    PASS")
        RJPRINT("")
    lpc_item = TESTCASE.get("LPC",[])
    for item in lpc_item:
        RJPRINT("LPC read/write %s test:"%item['name'])
        addr = item.get('addr')
        for wr_byte in [0x5a,0xa5]:
            ret = io_wr(addr, wr_byte)
            ret = io_rd(addr)
            if wr_byte != int(ret,16):
                totalerr -= 1
                msg = "    Write value: 0x%x, Read back value: 0x%x"%(wr_byte, int(ret,16))
                RJPRINT(msg)
                RJPRINT("    FAIL")
                errmsg += "%s %s \n" % (errmsg, msg)
            else:
                msg = "    Write value: 0x%x, Read back value: 0x%x"%(wr_byte, int(ret,16))
                RJPRINT(msg)
                RJPRINT("    PASS")
        RJPRINT("")
    if FACTESTMODULE.get("bmc_present", 0) == 1 or bmc_presence_check():
        ret, log = lpc_test_bmc()
        totalerr += ret
        errmsg += log

    RET[RETURN_KEY1] = totalerr
    RET[RETURN_KEY2] = errmsg
    return RET

def lpc_test_bmc():
    totalerr = 0
    Silicon_Revision = 0x1E6E207C # Silicon Revision ID Register
    ret, val = LPCTool().read_bmc_reg_32(Silicon_Revision)
    RJPRINT("LPC读写BMC测试:")
    if ret is False or "ffffffff" == val:
        RJPRINT("    FAILED")
        totalerr -= 1
    else:
        RJPRINT("    PASS")
    return totalerr, val

def test_MDIO_stress():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 :""}
    totalerr = 0
    test_times = 10
    for i in range(0, test_times):
       RJPRINT("\n\n第 %d/%d 次测试"%(i+1, test_times))
       func = "bmc_test_MDIO"
       RET1 = test_bmc_testcase(func)
       totalerr += RET1[RETURN_KEY1]
    if totalerr < 0:
       RET[RETURN_KEY1] = -1
    return RET

def test_lpc_stress():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    totalerr = 0
    test_times = 10
    for i in range(0, test_times):
       RJPRINT("\n\n第 %d/%d 次测试"%(i+1, test_times))
       RET1 = test_lpc()
       #print_temp_flush()
       totalerr += RET1[RETURN_KEY1]
       RET[RETURN_KEY2] += RET1[RETURN_KEY2]
    if totalerr < 0:
       RET[RETURN_KEY1] = -1
    return RET

def lpc_test_cpld(retry_times = 1):
    items = []
    totalerr = 0
    for item in CPLDVERSIONS:
        if item.get("gettype", None) == 'io':
            items.append(item)
    if len(items) > 0:
        RJPRINT("LPC读写CPLD测试:")
    for i in range(0, retry_times):
        err_flag = False
        for it in items:
            keep_str = ""
            addr = it.get('io_addr')
            name = it.get('name')
            if i == 0:
                it.update({'info': ""})
                it['info'] += "    写入5a，读出5a\n    PASS\n"
                it['info'] += "    写入a5，读出a5\n    PASS\n"
            if name == 'X86_CPLD' or name == 'CPU板CPLD':
                testaddr = addr + 0x05
            elif name == 'BASE_CPLD' or name == 'BASE板CPLD':
                testaddr = addr + 0x55
            else:
                testaddr = addr +  0xaa
            for wr_byte in [0x5a,0xa5]:
                io_wr(testaddr, wr_byte)
                ret = io_rd(testaddr)
                if wr_byte != int(ret,16):
                    keep_str += "    写入%x，读出%x\n"%(wr_byte, int(ret,16))
                    keep_str += "    FAILED"
                    keep_str += "\r\n"
                    err_flag = True
            if keep_str != "":
                it['info'] = keep_str
        if err_flag:
            totalerr += 1
    for it in items:
        RJPRINT(it.get('name'))
        RJPRINT(it['info'])
    return totalerr

def lpc_test_cpu_cpld(retry_times = 1):
    totalerr = 0
    lpc_item = list(TESTCASE.get("LPC",[]))
    for i in range(0, retry_times):
        err_flag = False
        for item in lpc_item:
            addr = item.get('addr')
            keep_str = ""
            if i == 0:
                item.update({'info':""})
                item['info'] += "    写入5a，读出5a\n    PASS\n"
                item['info'] += "    写入a5，读出a5\n    PASS\n"
            for wr_byte in [0x5a, 0xa5]:
                io_wr(addr, wr_byte)
                ret = io_rd(addr)
                if wr_byte != int(ret, 16):
                    keep_str += "    写入%x，读出%x\n" % (wr_byte, int(ret, 16))
                    keep_str += "    FAILED"
                    keep_str += "\r\n"
                    err_flag = True
            if keep_str != "":
                item['info'] = keep_str
        if err_flag:
            totalerr +=1
    for item in lpc_item:
        RJPRINT("LPC读写%s测试:" % item['name'])
        RJPRINT(item['info'])
    return totalerr

def lpc_test_bmc_new(retry_times = 1):
    lcptool = LPCTool()
    Silicon_Revision = 0x1E6E207C  # Silicon Revision ID Register\
    totalerr = 0
    if bmc_presence_check() is False:
        return totalerr

    keep_str = ""
    keep_str += "LPC读写BMC测试:\n"
    keep_str += "    PASS\n"
    for i in range(0, retry_times):
        ret, val = lcptool.read_bmc_reg_32(Silicon_Revision)
        if ret is False or "ffffffff" == val:
            keep_str = ""
            keep_str += "LPC读写BMC测试:\n"
            keep_str += "    FAILED\n"
            totalerr += 1
    RJPRINT(keep_str)
    return totalerr

def test_lpc_stress_new():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    test_times = TESTCASE.get("lpc_test_times", 100)
    err1 = lpc_test_cpld(test_times)
    err2 = lpc_test_cpu_cpld(test_times)
    err3 = lpc_test_bmc_new(test_times)
    totalerr = err2
    if err1 > err2:
        totalerr = err1
    if totalerr < err3:
        totalerr = err3
    RJPRINT("LPC %d次压力测试" % test_times)
    RJPRINT("PASS TIMES：%d" % (test_times - totalerr))
    RJPRINT("FAILED TIMES：%d" % totalerr)
    if totalerr != 0:
        RET[RETURN_KEY1] = -1
    return RET

def createbmcMac(cpumac , num = 2):
    cpumacvalue = int(cpumac.replace(":",""),16)
    bmcmacvalue = cpumacvalue + 2

    len = 6
    s =[''] * len
    for i in range(len):
        tmpval = bmcmacvalue & 0xff
        s[len - i - 1] = "%02x" % tmpval
        bmcmacvalue = bmcmacvalue >> 8

    bmcmac = ":".join(s)
    return  bmcmac.upper()

def ipmi_set_mac(mac):
    if fac_init_check_ipmi() == True:
        macs = mac.split(":")
        cmdinit = "ipmitool raw 0x0c 0x01 0x01 0xc2 0x00"
        cmdset = "ipmitool raw 0x0c 0x01 0x01 0x05"
        for ind in range(len(macs)):
            cmdset += " 0x%02x" % int(macs[ind], 16)
        rj_os_system(cmdinit)
        ret, status = rj_os_system(cmdset)
        if ret:
            RJPRINTERR("\n\n%s\n\n" % status)
            return False
        return True
    else:
        return False

def test_bios_flash():
    '''通过读取主备BIOS版本来验证'''
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : "","master":"","slave":""}
    file_path = TESTCASE.get("BIOS_INFO",None)
    if file_path == None:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "No BIOS flash test case."
        return RET
    try:
        with open(file_path, 'r') as fd:
            log = fd.read().strip()
        #RJPRINT(log)
        if "master" not in log.lower() or "slave" not in log.lower():
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "No master/slave BIOS version!"
            return RET
        version = log.split("\n",1)
        for version_item in version:
            bios_version = version_item.split(":",1)
            if len(bios_version) != 2 or len(bios_version[1].strip()) == 0:
                RET[RETURN_KEY1] -= 1
                if "master" in bios_version[0]:
                    RET[RETURN_KEY2] += "master BIOS version read error!\n"
                else:
                    RET[RETURN_KEY2] += "slave BIOS version read error!\n"
                continue
            if "master" in bios_version[0]:
                RET["master"] = bios_version[1].strip()
            else:
                RET["slave"] = bios_version[1].strip()
    except Exception as error:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = str(error)
    return RET

def get_bios_info():
    biosstatusdecode = TESTCASE.get("biosstatusdecode",None)
    biosstatus = TESTCASE.get("biosstatus",None)

    if biosstatus is None or biosstatusdecode is None:
        return None

    if biosstatus["gettype"] == "i2c":
        bus = biosstatus["bus"]
        loc = biosstatus["loc"]
        reg = biosstatus["reg"]
        ind, val = rji2cget(bus, loc,reg)
        if ind == False:
            val = None
    else:
        io_addr = biosstatus.get('io_addr')
        val = io_rd(io_addr)
    if val is not None:
        bitmask = biosstatus["bitmask"]
        val_t = int(val,16) & bitmask
        if val_t not in list(biosstatusdecode.keys()):
            return None
        return biosstatusdecode.get(val_t,None)
    return None

def test_bios_force_switch(bios_info, cpu = False):
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    log = get_bios_info()

    if log == None:
        RET[RETURN_KEY1] = -1
        RJPRINT("获取BIOS信息失败")
        return RET
    elif bios_info in log:
        RJPRINT("已是%s，无需切换"%bios_info,False)
        RET[RETURN_KEY1] = 0
        return RET

    if bios_info == "master":
        switch_mod = 0
    else:
        switch_mod = 1

    if makesure("切换BIOS会导致X86重启，是否继续？[Yes/No]：",True,echo = True):
        func = "test_bmc_bios_switch"
        if cpu == False:
            ret = test_bmc_func(func,switch_mod)
            return ret
        else:
            test_bios_swtch(switch_mod)
    else:
        print("已撤销")
        RET[RETURN_KEY1] = -1
    return RET

def test_bios_force_switch_slave():
    return test_bios_force_switch("slave")

def test_bios_force_switch_master():
    return test_bios_force_switch("master")

def test_cpu_bios_force_switch_slave():
    return test_bios_force_switch("slave", True)

def test_cpu_bios_force_switch_master():
    return test_bios_force_switch("master", True)

def test_bmc_command(param):
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    cmd = param.get("cmd",None)
    func = param.get("bmc_interface",None)
    if cmd == None or func == None:
        RET[RETURN_KEY1] = -88
        RET[RETURN_KEY2] = "获取配置文件错误"
    else:
        ret = test_bmc_func(func,cmd)
        if ret.get(RETURN_KEY1) == -1 or len(ret.get(RETURN_KEY2)) == 0:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "获取固件版本号 测试失败\nmessage:%s" % (ret.get(RETURN_KEY2))
        else:
            RET[RETURN_KEY1] = 0
            RET[RETURN_KEY2] = ret.get(RETURN_KEY2)
    RJPRINT(RET[RETURN_KEY2])
    return RET

def test_bmc_5387MD5():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    cmd = TESTCASE.get("eeprom5387_bmc",{}).get("cmd",None)
    func = TESTCASE.get("eeprom5387_bmc",{}).get("bmc_interface",None)
    if cmd == None or func == None:
        RET[RETURN_KEY1] = -88
        RET[RETURN_KEY2] = "获取配置文件错误"
    else:
        ret = test_bmc_func(func,cmd)
        if ret.get(RETURN_KEY1) == -1 or len(ret.get(RETURN_KEY2)) == 0:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "获取固件版本号 测试失败\nmessage:%s" % (ret.get(RETURN_KEY2))
        else:
            RET[RETURN_KEY1] = 0
            RET[RETURN_KEY2] = ret.get(RETURN_KEY2)
    RJPRINT(RET[RETURN_KEY2])
    return RET

def test_bios_swtch(switch_mod):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    #切换BIOS
    BIOS_TEST = TESTCASE.get("BIOS_TEST", None)
    if BIOS_TEST is None:
        RET = {RETURN_KEY1: -1, RETURN_KEY2: "no find config"}
        return RET
    if switch_mod == 0:    #切换至主BIOS
        switch_oplist = BIOS_TEST.get("switch_master",[])
    elif switch_mod == 1:    #切换至备份BIOS
        switch_oplist = BIOS_TEST.get("switch_slave",[])
    else:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "switch_mod error!"
        return RET
    for switch_opitem in switch_oplist:
        type = switch_opitem.get("gettype", "i2c")
        if type == "i2c":
            bus = switch_opitem["bus"]
            loc = switch_opitem["loc"]
            reg = switch_opitem["reg"]
            val = switch_opitem["val"]
            ret,log = rji2cset(bus,loc,reg,val)
            if ret == False:
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] = "switch i2c write failed!"
                return RET
        elif type == "io":
            io_addr = switch_opitem["io_addr"]
            val = switch_opitem["val"]
            ret = io_wr(io_addr, val)
            if ret == False:
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] = "switch i2c write failed!"
                return RET
        elif type == "func":
            funcname = eval(switch_opitem["funcname"])
            ret, msg = funcname()
            if ret is False:
                RET[RETURN_KEY1] = -1
                log_debug("switch bios func fail %s" % switch_opitem["funcname"])
                return RET
    return RET

def readsysfs(location):
    try:
        locations = glob.glob(location)
        with open(locations[0], 'r') as fd1:
            val = fd1.read()
    except Exception as e:
        return False, (str(e)+" location[%s]" % location)
    return True, val

def test_dcdc():
    RET = {RETURN_KEY1: 0, RETURN_KEY2: ""}
    totalerr = 0
    errmsg = ""
    resultval = []

    items = TESTCASE.get("dcdcsensor", None)
    if items is None:
        RET[RETURN_KEY1] = -999
        RET[RETURN_KEY2] = 'config error'
        return RET

    #get dcdcsensor value
    for item in items:
        Sensor = item.get('Sensor', None)
        Address = item.get('Address', None)
        min = item.get('CriticalLow', None)
        max = item.get('CriticalHigh', None)
        Unit = item.get('Unit', "")
        format = item.get("format", None)
        gettype = item.get("gettype", None)
        io_addr = item.get("io_addr", None)
        len = item.get("len", None)
        if gettype == "sysfs":
            location = item.get("location", "error_url")
            ret,ind = readsysfs(location)
        elif gettype == "pagei2cword":
            bus = item.get('bus')
            devno = item.get('devno')
            offset = item.get('addr')
            select = item.get('select')
            slectvalue = item.get('slectvalue')
            rji2cset(bus, devno, select, slectvalue)
            ret, ind = rji2cgetWord(bus, devno, offset)
            if ret == False:
                val = None
            else:
                val = ind.replace("0x", "").replace("0X", "")
        elif gettype == 'io':
            val = io_rd(io_addr, len)
            val = "%s" % (int(val, 16) >> 4) #
        elif gettype == 'i2c':
            bus = item.get('bus')
            devno = item.get('devno')
            offset = item.get('addr')
            i2ctmp = ''
            for i in range(0,len):
                ret, ind = rji2cget(bus,devno, offset+i)
                if ret == False:
                    i2ctmp = None
                    break
                i2ctmp += ind.replace("0x","").replace("0X","")
            if i2ctmp == None:
                val = None
            else:
                val = "%s" %(int(i2ctmp, 16) >> 4)

        if ret == True:
            if gettype == "sysfs":
                val = ind.replace("\n", "")
            if format is not None:
                tmp = format % val
                val_tmp = eval(tmp)
            else:
                val_tmp = int(val, 10)
            if min < val_tmp < max:
                statusmsg = "OK"
            else:
                totalerr -= 1
                statusmsg = 'Not OK'
        else:
            totalerr -= 1
            statusmsg = 'Not OK'
            val_tmp = "fail "
            Unit = ""
            log_debug("get dcdc value fail %s" % Sensor)
        resultval.append([Sensor, Address, statusmsg, "%s%s"%(val_tmp, Unit), "%s%s"%(min, Unit), "%s%s"%(max, Unit)])

    #打印
    header = ['Sensor', 'Address', 'State', 'Value', 'CriticalLow', 'CriticalHigh']
    result = tabulate(resultval, header, tablefmt='simple')
    RJPRINT(result)
    if totalerr < 0:
        errmsg += str(result)

    RET[RETURN_KEY1] = totalerr
    RET[RETURN_KEY2] = errmsg
    return RET

def test_bmc_sol():
    '''CPU和BMC之间的串口（SOL）测试'''
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    cur_time = time.time();
    timeArray = time.localtime(cur_time)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    teststr = 'SOL test,current time:%s' % otherStyleTime
    cmd = "echo '%s' > /dev/ttyS0" % teststr
    log_os_system(cmd,0)
    time.sleep(1)

    func = 'bmc_log_os_system'
    cmd = "cat /var/log/obmc-console.log | grep '%s'" % teststr
    ret = test_bmc_func(func,cmd)
    if ret.get(RETURN_KEY1) == -1 or len(ret.get(RETURN_KEY2)) == 0:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "SOL 测试失败\nmessage:%s" % (ret.get(RETURN_KEY2))
    else:
        RET[RETURN_KEY1] = 0
        RET[RETURN_KEY2] = "SOL 测试成功"
    RJPRINT(RET[RETURN_KEY2])
    return RET

def print_register(value):
    index = 0
    lineStr = ""
    RJPRINT("        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f")
    for val in value:
        if index % 32 == 0 :
            if len(lineStr) != 0 :
                RJPRINT(lineStr)
            lineStr = "%04x: " % (index / 2)
        if index % 2 == 0 :
            lineStr += " "
        lineStr += val
        index += 1
    RJPRINT(lineStr)
    RJPRINT("\n")
def test_bmc_emmc_register():
    '''eMMC寄存器值读取'''
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    func = 'bmc_log_os_system'
    totalerr = 0
    emmc_register = TESTCASE.get("EMMC_REGISTER", None)
    if emmc_register == None :
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "获取eMMC寄存器配置错误"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    for item in emmc_register:
        name = item.get('name')
        location = item.get('location')
        RJPRINT("%s : " % name)
        cmd = "cat %s" % location
        ret = test_bmc_func(func, cmd)
        if ret.get(RETURN_KEY1) == -1 or len(ret.get(RETURN_KEY2)) == 0:
            totalerr -= 1
            RJPRINT("eMMC寄存器值%s读取失败 : %s" % (name, ret.get(RETURN_KEY2)))
        else:
            val = ret.get(RETURN_KEY2)
            print_register(val)
    RET[RETURN_KEY1] = totalerr
    return RET
def test_bmc_emmc_life():
    '''eMMC寿命检测'''
    RET = {RETURN_KEY1 : -1,  RETURN_KEY2 : ""}
    func = 'bmc_log_os_system'
    emmc_register = TESTCASE.get("EMMC_REGISTER", None)
    if emmc_register == None :
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "获取eMMC寄存器配置错误"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    for item in emmc_register:
        name = item.get('name')
        if name == "EXT_CSD":
            location = item.get('location')
            cmd = "cat %s" % location
            ret = test_bmc_func(func, cmd)
            if ret.get(RETURN_KEY1) == -1 or len(ret.get(RETURN_KEY2)) == 0:
                RET[RETURN_KEY2] = "eMMC寄存器值%s读取失败 : %s" % (name, ret.get(RETURN_KEY2))
                RJPRINT(RET[RETURN_KEY2])
                return RET
            else:
                val = ret.get(RETURN_KEY2)
                val_268 = val[268*2 : 269*2]
                if len(val_268) != 2:
                    RET[RETURN_KEY2] = "EXT_CSD寄存器第268字节读取失败"
                    RJPRINT(RET[RETURN_KEY2])
                    return RET
                val_268_t = int(val_268, 16)
                RJPRINT("EXT_CSD byte 268 = 0x%x, 预期值 = 0x01" % val_268_t)
                if val_268_t == 0:
                    RET[RETURN_KEY2] = "检测到未定义寿命值"
                    RJPRINT(RET[RETURN_KEY2])
                if val_268_t > 1:
                    RET[RETURN_KEY2] = "eMMC已使用寿命超过10%"
                    RJPRINT(RET[RETURN_KEY2])
                else:
                    RET[RETURN_KEY2] = "eMMC寿命正常"
                    RJPRINT(RET[RETURN_KEY2])
                    RET[RETURN_KEY1] = 0
                return RET
    RET[RETURN_KEY2] = "未找到eMMC寄存器EXT_CSD的配置"
    RJPRINT(RET[RETURN_KEY2])
    return RET
def release_bmc_cached_memory():
    RET = test_bmc_func("bmc_release_cached_memory")
    if RET <= 0:
        return False, ""
    return True, ""
emmc_fio_test_file = "/data/fio_test"
def test_bmc_emmc_rw(param):
    '''eMMC读写检测'''
    RET = {RETURN_KEY1 : -1,  RETURN_KEY2 : ""}
    func = 'bmc_log_os_system'
    emmc_fio = TESTCASE.get("EMMC_FIO", None)
    if emmc_fio == None :
        RET[RETURN_KEY2] = "获取eMMC FIO配置错误"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    emmc_fio_case = emmc_fio.get(param, None)
    if emmc_fio_case == None :
        RET[RETURN_KEY2] = "找不到指定的eMMC FIO配置"
        RJPRINT(RET[RETURN_KEY2])
        return RET
    for item in emmc_fio_case:
        rw = item.get("rw", None)
        bs = item.get("bs", None)
        rwmixwrite = item.get("rwmixwrite", None)
        iodepth = item.get("iodepth", None)
        size = item.get("size", None)
        name = item.get("name", None)
        verify = item.get("verify", None)
        do_verify = item.get("do_verify", None)
        cmd = "fio -rw=%s -bs=%s -rwmixwrite=%d -iodepth=%d -size=%s -verify=%s -do_verify=%d -verify_fatal=1 -verify_state_save=0 -name=%s -filename=%s" % (rw, bs, rwmixwrite, iodepth, size, verify, do_verify, name, emmc_fio_test_file)
        ret = test_bmc_func(func, cmd)
        if ret.get(RETURN_KEY1) == -1 or len(ret.get(RETURN_KEY2)) == 0:
            RET[RETURN_KEY2] = "%s 失败: %s" % (name, ret.get(RETURN_KEY2))
            RJPRINT(RET[RETURN_KEY2])
            cmd = "rm %s" % emmc_fio_test_file
            ret = test_bmc_func(func, cmd)
            return RET
        else:
            result = name + " :\n"
            log = ret.get(RETURN_KEY2)
            index = log.find("read", 0)
            if index != -1:
                result += "\tRead : "
                iops_index = log.find("iops=", index)
                if iops_index == -1:
                    iops_index = log.find("IOPS=", index)
                if iops_index != -1:
                    iops = log[iops_index : log.find(",", iops_index)]
                    result += iops + "\n"
            index = log.find("write", 0)
            if index != -1:
                result += "\tWrite : "
                iops_index = log.find("iops=", index)
                if iops_index == -1:
                    iops_index = log.find("IOPS=", index)
                if iops_index != -1:
                    iops = log[iops_index : log.find(",", iops_index)]
                    result += iops + "\n"
            RJPRINT(result)
    cmd = "rm %s" % emmc_fio_test_file
    ret = test_bmc_func(func, cmd)
    RET[RETURN_KEY1] = 0
    return RET

def fac_check_eth_mac():
    '''判断I210和MAC能否扫到'''
    totalerr = 0
    errmsg = ""
    for pci in PCIe_SPEED_ITEM:
        try:
            status, output = log_os_system("lspci|grep %s | wc -l"%pci["PCIe_name"], 0)
            if output.isdigit() and int(output) == 0:
                totalerr -= 1
                RJPRINT("%s can't find!" % pci["PCIe_name"])
        except Exception as error:
             totalerr -= 1
             errmsg = str(error)
             RJPRINT("errmsg")
    if totalerr < 0:
        quit()

def cpld_init():
    '''写CPLD寄存器进行CPLD初始化'''
    items = TESTCASE.get("init_param",{}).get("CPLD",None)
    if items == None:
        return True
    try:
        for item in items:
            if item.get("gettype") == "i2c":
                bus = item["bus"]
                loc = item["loc"]
                reg = item["reg"]
                val = item["val"]
                ret, log = rji2cset(bus, loc, reg, val)
                if ret == False:
                    RJPRINT("Write cpld falied,bus:%d,loc:0x%2x,reg:0x%2x,value:0x%2x" %(bus,loc,reg,val))
                    return False
            else:
                pass
    except Exception as error:
        errmsg = str(error)
        RJPRINT("errmsg")
        return False
    return True

def usb0_init():
    '''配置USB0的IP'''
    usbip = TESTCASE.get("SONIC",{}).get("ip","1.1.1.1")
    cmd = "ifconfig usb0 %s netmask 255.255.255.0" % usbip
    ret,log = log_os_system(cmd, 0)
    if ret or "ERROR" in log:
        return False
    return True

class IniRdwr():
    path = '/tmp/.status.ini'
    config = None
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.path)

    def check_section(self, section):
        return self.config.has_section(section)

    def check_option(self, section, option):
        return self.config.has_option(section, option)

    def rd_ini_option(self, section, option, type = "str"):
        self.config.read(self.path)
        if self.check_option(section, option) is False:
            return False, 'no section or option in %s' % self.path
        if type == 'int':
            value = self.config.getint(section, option)
        elif type == 'bool':
            value = self.config.getboolean(section, option)
        elif type == "float":
            value = self.config.getfloat(section, option)
        elif type == "str":
            value = self.config.get(section, option)
        else:
            return False, 'error para'
        return True, value

    def wr_ini_option(self, section, option, value):
        if self.check_section(section) is False:
            self.config.add_section(section)
        self.config.set(section, option, value)
        with open(self.path, "w") as f:
            self.config.write(f)
        return True, "success"

def bmc_presence_check():
    obj = IniRdwr()
    ret, val = obj.rd_ini_option("bmc", "bmc_present", "bool")
    if ret and val:
        return True
    else:
        return False

def psu_check():
    '''电源防呆检测'''
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    errmsg = ""
    psus =  FRULISTS.get('psus',[])
    psucheckitem = TESTCASE.get("firmware_check",{}).get("psus",None)

    if psucheckitem == None: #无电源检测项
        return True
    psutypes = psucheckitem.get("psutype")
    for psu in psus:
        psuscheck = False
        try:
            eeprom = I2CUTIL.dumpValueByI2c(psu.get('bus'), psu.get('loc'))
            if eeprom is None:
                continue
            fru = ipmifru()
            fru.decodeBin(eeprom)
            realtype = fru.productInfoArea.productPartModelName.strip()
            for type in psutypes:
                if type in realtype:   #匹配成功
                    psuscheck = True
                    break
            if psuscheck == False:
                RJPRINT("%s 电源类型不匹配，请检查!" % psu.get("name"))
                totalerr -= 1
        except Exception as e:
            errmsg = " %s %s %s \n" %(errmsg, psu.get('name'), str(e))
            continue

    if totalerr < 0:
        RJPRINT("检测错误，无法启动生测程序!请使用以下型号电源进行测试:")
        for type in psutypes:
            RJPRINT(type)
        quit()
    return  True

def fac_check_rtc():
    try:
        time1 = time.time();
        timeArraystart = time.localtime(time1)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArraystart)
        log_debug("当前时间:%s" % otherStyleTime)
        time_t = otherStyleTime.split("-")
        time_year = int(time_t[0].strip())
        log_debug("当前时间:%d年" % time_year)
        if time_year <= 2000:
            RJPRINT("当前时间:%s,请先进入系统配置,设置RTC" % otherStyleTime)
    except Exception as e:
        log_debug(str(e))
        pass

class LPCTool():
    reg_addr = None
    reg_data = None

    def __init__(self, reg_addr = 0x4E, reg_data = 0x4F):
        self.reg_addr = reg_addr
        self.reg_data = reg_data
        self.disable_sio_val = 0xAA
        self.enable_sio_val = 0xA5
        self.siorx_07 = 0x07
        self.siord_30 = 0x30
        self.ldu_0d_val = 0x0D # 选择LDU 0D（iLPC2AHB-LPC转AHB总线桥）
        self.siord_F8 = 0xF8
        self.check_sio_length = 0x03
        self.length_4_bytes = 0x2
        self.retrytime = 1 # 判断非4字节后，重新设置的次数
        self.port_addr = "/dev/port"

    def dis_ilpc2ahb(self):
        try:
            # disabled ilpc2ahb
            self.seek_addr(self.siord_30)
            self.port_write(self.reg_data, 0x00)
            # dis_superio
            self.seek_addr(self.disable_sio_val)
        except Exception as error:
            RJPRINT("dis_ilpc2ahb fail:" + str(error))

    def get_reg(self, reg):
        self.seek_addr(reg)
        return self.port_read(self.reg_data)

    def set_reg(self, reg, val):
        self.seek_addr(reg)
        return self.port_write(self.reg_data, val)

    def en_ilpc2ahb(self):
        try:
            # dis_superio
            self.seek_addr(self.disable_sio_val)
            # en_superio
            self.seek_addr(self.enable_sio_val)
            self.seek_addr(self.enable_sio_val)
            # enable bmc ilpc2ahb
            self.set_reg(self.siorx_07, self.ldu_0d_val)
            self.set_reg(self.siord_30, 0x01)

            for i in range(self.retrytime + 1):
                tmp = self.get_reg(self.siord_F8)
                val = int(tmp, 16)
                if val & self.check_sio_length == self.length_4_bytes:
                    return True, val
                if i == self.retrytime:
                    break
                val = val & 0xfc | self.length_4_bytes  # 设置4字节长度,bit0,bit1位置(10)
                self.set_reg(self.siord_F8, val)
            return False, val
        except Exception as error:
            RJPRINT("en_ilpc2ahb fail:" + str(error))
            return False, None

    def port_read(self, offset, size=1):
        try:
            ret = None
            fd = os.open(self.port_addr, os.O_RDWR|os.O_CREAT)
            os.lseek(fd, offset, os.SEEK_SET)
            ret = os.read(fd, size)
        except ValueError:
            return None
        except Exception as e:
            print(e)
            return None
        finally:
            os.close(fd)
        return "".join(["{:02x}".format(ord(item)) for item in ret])

    def port_write(self, offset, val):
        if isinstance(val, int):
            val = chr(val)
        try:
            fd = os.open(self.port_addr, os.O_RDWR|os.O_CREAT)
            os.lseek(fd, offset, os.SEEK_SET)
            ret = os.write(fd, val)
        except ValueError:
            return None
        except Exception as e:
            print(e)
            return None
        finally:
            os.close(fd)

    def write_32bit_val(self, addr):
        address_base = 0xF0 # reg for access address
        for i in range(4):
            self.seek_addr(address_base + i)
            bit = 32 - (i + 1) * 8
            self.port_write(self.reg_data, addr >> bit & 0xFF)

    def seek_addr(self, addr):
        self.port_write(self.reg_addr, addr)

    def read_bmc_reg_32(self, addr):
        try:
            value_address_base = 0xF4 # reg for value address
            ret, _ = self.en_ilpc2ahb()
            if ret is False:
                return ret, ""
            self.write_32bit_val(addr)
            self.seek_addr(0xFE)
            ret = self.port_read(self.reg_data)
            val = ""
            for i in range(4):
                self.seek_addr(value_address_base + i)
                val += self.port_read(self.reg_data)
            self.dis_ilpc2ahb()
        except Exception as error:
            RJPRINT("read_bmc_reg_32 fail:" + str(error))
            return False, ""
        return True, val

def send_commands(commands, in_x86 = True):
    func = 'bmc_log_os_system'
    for command in commands:
        cmd = command.get("cmd")
        sleep_time = command.get("sleep", 0)
        if in_x86:
            ret, msg = rj_os_system(cmd)
        else:
            tmp = test_bmc_func(func, cmd) # todo 命令全部发送 循环在BMC端做
            ret = tmp.get(RETURN_KEY1)
            msg = tmp.get(RETURN_KEY2)
            log_debug(msg)
        if sleep_time != 0:
            time.sleep(sleep_time)
        if ret != 0:
            log_debug("failed %s" % cmd)
            return False, cmd
        else:
            log_debug("succeed %s" % cmd)
    return True, "success"

def test_open_gpio(flag = True):# True CPU gpio; False BMC gpio
    if flag:
        commands = TESTCASE.get("switch_cpld_gpio",{}).get("cpu_open_gpio",None)
    else:
        commands = TESTCASE.get("switch_cpld_gpio", {}).get("bmc_open_gpio", None)
    if commands is None:
        return True, ""
    ret, val = send_commands(commands, flag)
    if ret:
        return True, ""
    else:
        return False, ""

def test_close_gpio(flag = True):# True CPU gpio; False BMC gpio
    if flag:
        commands = TESTCASE.get("switch_cpld_gpio",{}).get("cpu_close_gpio",None)
    else:
        commands = TESTCASE.get("switch_cpld_gpio", {}).get("bmc_close_gpio", None)
    if commands is None:
        return True, ""
    ret, val = send_commands(commands, flag)
    if ret:
        return True, ""
    else:
        return False, ""

def test_setenv_5387():
    commands = TESTCASE.get("SetEnv5387", {}).get("SetEnv", None)
    ret, val = send_commands(commands, False)
    if ret:
        return True, ""
    else:
        return False, ""

def test_cleanenv_5387():
    commands = TESTCASE.get("SetEnv5387", {}).get("ClearEnv", None)
    ret, val = send_commands(commands, False)
    if ret:
        return True, ""
    else:
        return False, ""

def test_setcpuenv_5387():
    commands = TESTCASE.get("SetEnv5387", {}).get("SetCpuEnv", None)
    ret, val = send_commands(commands, True)
    if ret:
        return True, ""
    else:
        return False, ""

def test_cleancpuenv_5387():
    commands = TESTCASE.get("SetEnv5387", {}).get("ClearCpuEnv", None)
    ret, val = send_commands(commands, True)
    if ret:
        return True, ""
    else:
        return False, ""

def test_setenv_lssignal():
    commands = TESTCASE.get("SetEnvLssignal", {}).get("SetEnv", None)
    ret, val = send_commands(commands, True)
    if ret:
        return True, ""
    else:
        return False, ""

def test_cleanenv_lssignal():
    commands = TESTCASE.get("SetEnvLssignal", {}).get("ClearEnv", None)
    ret, val = send_commands(commands, True)
    if ret:
        return True, ""
    else:
        return False, ""

def open_smi_access(whichone = "x86"):
    global BMC_DIAG_FLAG
    commands = TESTCASE.get("smi_access")
    if whichone == "x86":
        opencmd = subprocess.get("CPU").get("open")
        ret, val = send_commands(opencmd)
        if BMC_DIAG_FLAG == 1:
            closecmd = subprocess.get("BMC").get("close")
            ret1, val1 = send_commands(closecmd, False)
        else:
            ret1 = True
    elif whichone == "bmc":
        opencmd = subprocess.get("BMC").get("open")
        ret, val = send_commands(opencmd, False)
        closecmd = subprocess.get("CPU").get("close")
        ret1, val1 = send_commands(closecmd)
    else:
        return False, ""

    if ret and ret1:
        return True, ""
    else:
        return False, ""

def open_bmc_smi_access():
    ret, msg = test_bmc_channel()
    if ret is False:
        return ret, msg
    return open_smi_access("bmc")

def test_lssignal_init():
    LSSIGNAL_ACCESS = TESTCASE.get("LSSIGNAL_RESET", None)
    for item in LSSIGNAL_ACCESS:
        type = item.get("type", None)
        mask_item = item.get("mask_list", None)
        access_item = item.get("access_list", None)
        if type is None or  mask_item is None or  access_item is None:
            return

        startbus = access_item.get("startbus", None)
        endbus = access_item.get("endbus", None)
        addr = access_item.get("addr", None)
        reg = access_item.get("reg", None)
        startportnum = access_item.get("startportnum", None)
        if startbus is None or endbus is None or addr is None or reg is None or startportnum is None:
            return
        log_debug("lssignal access get param. startbus:%d, endbus:%d addr:0x%x, reg:0x%x, startportnum:%d"
            % (startbus, endbus, addr, reg, startportnum))

        RET1 = mask_i2c_set(mask_item, 1);      #关闭访问通道，无法访问光模块
        time.sleep(5)

        RET2 = mask_i2c_set(mask_item, 2);      #开启访问通道，正常访问
        time.sleep(5)
    return

lssignal_init_status = 0
def open_fpga_i2c_access():
    commands = TESTCASE.get("open_fpga_i2c_access")
    ret, val = send_commands(commands)
    if ret is False:
        RJPRINT("open_fpga_i2c_access fail:%s" % val)
    commands1 = TESTCASE.get("open_bmc_fpga_i2c_access", None)
    ret1 = True
    if commands1 is not None:
        ret1, val1 = send_commands(commands1, False)
        if ret1 is False:
            RJPRINT("open_bmc_fpga_i2c_access fail:%s" % val1)
    #进入生测前，需要判断是否进行lssignal初始化，此项为临时解决自环模块端口挂住问题
    #进入生测后，lssignal初始化仅需执行一次
    global lssignal_init_status
    if FACTESTMODULE.get("lssignalinit", 0) == 1 and lssignal_init_status == 0:
        test_setenv_lssignal()
        test_lssignal_init()
        test_cleanenv_lssignal()
        lssignal_init_status = 1
    if ret and ret1:
        return True, ""
    else:
        return False, ""


def bmc_fpag_i2_access(open_flag):
    if open_flag is True:
        commands1 = TESTCASE.get("open_bmc_fpga_i2c_access", None)
        flag_str = "open"
    else:
        commands1 = TESTCASE.get("close_bmc_fpga_i2c_access", None)
        flag_str = "close"
    ret1 = True
    if commands1 is not None:
        ret1, val1 = send_commands(commands1, False)
        if ret1 is False:
            RJPRINT("bmc fpga i2c access %s fail:%s" % (flag_str, val1))


def test_open_cpu_gpio():
    global BMC_DIAG_FLAG
    if BMC_DIAG_FLAG == 1:
        ret, val = test_close_gpio(False) #关闭BMC权限
        if ret is False:
            log_error("Unable to close bmc gpio access")
            return ret, val
    return test_open_gpio() #开启x86权限

def test_open_bmc_gpio():
    ret, val = test_close_gpio() #关闭X86权限
    if ret is False:
        log_error("Unable to close cpu gpio access")
        return ret, val
    return test_open_gpio(False) #开启BMC权限

def test_close_bmc_gpio():
    return test_close_gpio(False)

def fac_check_bmc_status():
    try:
        lpctool = LPCTool()
        ret, val = lpctool.en_ilpc2ahb()
        obj = IniRdwr()
        if ret is False and val == "ff":
            cmd = "ifconfig usb0"
            ret, msg = rj_os_system(cmd)
            if ret != 0:
                obj.wr_ini_option("bmc","bmc_present","False")
            else:
                obj.wr_ini_option("bmc", "bmc_present", "True")
        elif ret is True:
            obj.wr_ini_option("bmc","bmc_present","True")
    except Exception as e:
        RJPRINT(str(e))
    finally:
        lpctool.dis_ilpc2ahb()

# ===================================================================
# 测试项:AVS状态检测
# ===================================================================
def test_vas(param):
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    RJPRINT("")
    cmd = param.get("cmd", None)
    ret, log = log_os_system(cmd, 0)
    if ret or len(log) == 0:
        RET[RETURN_KEY1] -= 1
    else:
        RJPRINT("MAC VID value : %s" % log)
        RET[RETURN_KEY1] = 0
    items = TESTCASE.get("CORE_VOL_TEST", None)
    if items is not None:
        commands = items.get("switch_page", None)
        ret, val = send_commands(commands, True)
        cmd = items.get("get_vol", None)
        ret, log = log_os_system(cmd, True)
        if ret or len(log) == 0:
            RET[RETURN_KEY1] -= 1
        else:
            RJPRINT("Core电压  : %fV" % ((float)(int(log, 16))/4096.0))
        commands = items.get("recover_page", None)
        ret, val = send_commands(commands, True)
    return RET

# ===================================================================
# 测试项:端口DSC异常检测
# ===================================================================
def test_opt_module_dsg():
    pass_list = []
    failed_list = []
    port_list = []
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    empty_str = "      "

    port_list = TESTCASE.get("DSC_PORT_LIST",None)
    for i in range(len(port_list)):
        ret, log = log_os_system("bcmcmd \"dsh -c 'phy diag %s dsc'\" | grep veye_margin_limit_fail " % port_list[i], 0)
        if len(log) and "veye_margin_limit_fail = 0x1" in log:
            failed_list.append(i+1)
        else:
            pass_list.append(i+1)

    if len(pass_list) > 0:
        port_totalprint(pass_list, "OK")
    if len(failed_list) > 0:
        port_totalprint(failed_list, "failed")
        tmpstr = '\nFAILED:\n'
        tmpstr += empty_str
        for i in range(len(failed_list)):
            tmpstr +="%-5s"% failed_list[i]
            if((i + 1) %8 == 0):
                tmpstr +="\n"
                tmpstr += empty_str
        tmpstr += ""
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = tmpstr
        return RET

    return RET

# LED status check
def test_led_status_check():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    ret_msg = ""
    led_list = TESTCASE.get("LED_STATUS_CHECK")
    if led_list is None:
        RET[RETURN_KEY1] = 1
        RET[RETURN_KEY2] = "LED status check config not found"
        return RET

    for led_conf in led_list:
        color = "N/A"
        name = led_conf.get('name')
        led_value_conf = led_conf.get('led')
        okval = led_conf.get('okval')
        led_attrs = led_conf.get('led_attrs')
        mask = led_attrs.get('mask', 0xff)
        formatstr = "    %%-%ds %%-20s %%-4s"%((20+wide_chars(name)))
        ret, value = get_value(led_value_conf)
        if ret is False or value is None:
            color = value
            status = "FAIL"
            totalerr -= 1
        else:
            ledval = int(value) & mask
            if ledval != okval:
                status = "FAIL"
                totalerr -= 1
            else:
                status = "PASS"
            for key, val in led_attrs.items():
                if (ledval == val) and (key != "mask"):
                    color = key.upper()
                    break
        RJPRINT(formatstr % (name, color, status))
    RET[RETURN_KEY1] = totalerr
    return RET

def set_onie_value(params):
    onie = params.get("onie")
    field = params.get("field")
    config_value = params.get("config_value")
    for index, onie_item in enumerate(onie):
        if onie_item.get("name") == field:
            if "value" in onie_item.keys():
                onie[index]["value"] = config_value


def onie_eeprom_decode(onie, e2_decode):
    for e2_decode_item in e2_decode:
        field = e2_decode_item.get("field")
        decode_type = e2_decode_item.get("decode_type")
        if decode_type == 'func':
            params = {
                "onie": onie,
                "field": field
            }
            func_name = e2_decode_item.get("func_name")
            if func_name is not None:
                run_func(func_name, params)
        elif decode_type == 'config':
            config_value = e2_decode_item.get("config_value")
            if config_value is not None:
                params = {
                    "onie": onie,
                    "field": field,
                    "config_value": config_value
                }
                set_onie_value(params)
        else:
            RJPRINT("unsupport decode type")
            continue


def onie_eeprom_show(eeprom, e2_decode=None):
    ret = 0
    msg = ""
    try:
        onietlv = ot.onie_tlv()
        rets = onietlv.decode(eeprom)
        if e2_decode is not None:
            onie_eeprom_decode(rets, e2_decode)
        RJPRINT("%-20s %-5s %-5s  %-20s" % ("TLV name", "Code", "lens", "Value"))
        for item in rets:
            if item["code"] == 0xfd:
                RJPRINT("%-20s 0x%-02X   %-5s" % (item["name"], item["code"], item["lens"]))
            else:
                RJPRINT("%-20s 0x%-02X   %-5s %-20s" % (item["name"], item["code"], item["lens"], item["value"]))
    except Exception as e:
        ret = -1
        msg = traceback.format_exc()
    return ret, msg

def set_fantlv_value(params):
    fantlv_dict = params.get("fantlv")
    field = params.get("field")
    config_value = params.get("config_value")
    for index, fantlv_item in enumerate(fantlv_dict):
        if fantlv_item.get("name") == field:
            if "value" in fantlv_item.keys():
                fantlv_dict[index]["value"] = config_value


def fantlv_eeprom_decode(fantlv_dict, e2_decode):
    for e2_decode_item in e2_decode:
        field = e2_decode_item.get("field")
        decode_type = e2_decode_item.get("decode_type")
        if decode_type == 'func':
            params = {
                "fantlv": fantlv_dict,
                "field": field
            }
            func_name = e2_decode_item.get("func_name")
            if func_name is not None:
                run_func(func_name, params)
        elif decode_type == 'config':
            config_value = e2_decode_item.get("config_value")
            if config_value is not None:
                params = {
                    "fantlv": fantlv_dict,
                    "field": field,
                    "config_value": config_value
                }
                set_fantlv_value(params)
        else:
            RJPRINT("unsupport decode type")
            continue


def fantlv_eeprom_show(eeprom, e2_decode=None):
    ret = 0
    msg = ""
    try:
        tlv = fan_tlv()
        rets = tlv.decode(eeprom)
        if len(rets) == 0:
            ret = -1
            msg = "fan tlv eeprom info error!"
            return ret, msg
        if e2_decode is not None:
            fantlv_eeprom_decode(rets, e2_decode)
        RJPRINT("%-15s %-5s %-5s  %-20s" % ("TLV name", "Code", "lens", "Value"))
        for item in rets:
            RJPRINT("%-15s 0x%-02X   %-5s %-20s" % (item["name"], item["code"], item["lens"], item["value"]))
    except Exception as e:
        ret = -1
        msg = traceback.format_exc()
    return ret, msg


def run_func(funcname, params):
    try:
        eval(funcname)(params)
    except Exception as e:
        print(str(e))


def decode_mac(encodedata):
    if encodedata is None:
        return None
    ret = ":".join("%02x" % ord(data) for data in encodedata)
    return ret.upper()


def fru_decode_mac(params):
    ipmi_fru = params.get("fru")
    area = params.get("area")
    field = params.get("field")
    area_info = getattr(ipmi_fru, area, None)
    if area_info is not None:
        raw_mac = getattr(area_info, field, None)
        decoded_mac = decode_mac(raw_mac)
        ipmi_fru.setValue(area, field, decoded_mac)


def decode_mac_number(encodedata):
    if encodedata is None:
        return None
    return (ord(encodedata[0]) << 8) | (ord(encodedata[1]) & 0x00ff)


def fru_decode_mac_number(params):
    ipmi_fru = params.get("fru")
    area = params.get("area")
    field = params.get("field")
    area_info = getattr(ipmi_fru, area, None)
    if area_info is not None:
        raw_mac_number = getattr(area_info, field, None)
        mac_number = decode_mac_number(raw_mac_number)
        ipmi_fru.setValue(area, field, mac_number)


def fru_decode_hw(params):
    ipmi_fru = params.get("fru")
    area = params.get("area")
    field = params.get("field")
    area_info = getattr(ipmi_fru, area, None)
    if area_info is not None:
        raw_hw = getattr(area_info, field, None)
        decode_hw = str(int(raw_hw, 16))
        ipmi_fru.setValue(area, field, decode_hw)


def set_fru_value(params):
    ipmi_fru = params.get("fru")
    area = params.get("area")
    field = params.get("field")
    config_value = params.get("config_value")
    ipmi_fru.setValue(area, field, config_value)


def fru_eeprom_decode(ipmi_fru, e2_decode):
    for e2_decode_item in e2_decode:
        area = e2_decode_item.get("area")
        field = e2_decode_item.get("field")
        decode_type = e2_decode_item.get("decode_type")
        if decode_type == 'func':
            params = {
                "fru": ipmi_fru,
                "area": area,
                "field": field
            }
            func_name = e2_decode_item.get("func_name")
            if func_name is not None:
                run_func(func_name, params)
        elif decode_type == 'config':
            config_value = e2_decode_item.get("config_value")
            if config_value is not None:
                params = {
                    "fru": ipmi_fru,
                    "area": area,
                    "field": field,
                    "config_value": config_value
                }
                set_fru_value(params)
        else:
            RJPRINT("unsupport decode type")
            continue


def fru_eeprom_show(eeprom, e2_decode=None):
    ret = 0
    msg = ""
    try:
        ipmi_fru = ipmifru()
        ipmi_fru.decodeBin(eeprom)
        if e2_decode is not None:
            fru_eeprom_decode(ipmi_fru, e2_decode)
        RJPRINT("=================board=================")
        RJPRINT(ipmi_fru.boardInfoArea)
        RJPRINT("=================product=================")
        RJPRINT(ipmi_fru.productInfoArea)
    except Exception as e:
        ret = -1
        msg = traceback.format_exc()
    return ret, msg


def wedge_eeprom_show(eeprom, e2_decode =None):
    ret = 0
    msg = ""
    try:
        wedge_e2 = Wedge()
        wedge_e2.decode(eeprom)
        RJPRINT(wedge_e2)
    except Exception as e:
        ret = -1
        msg = traceback.format_exc()
    return ret, msg


def test_board_eeprom():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    ret_msg = ""
    board_e2_conf = TESTCASE.get("BOARD_E2_CONF")
    if board_e2_conf is None:
        RET[RETURN_KEY1] = 1
        RET[RETURN_KEY2] = "Board eeprom config not found"
        return RET
    for e2_conf in board_e2_conf:
        try:
            name = e2_conf.get("name")
            RJPRINT("===============%s ================getmessage" % name)
            e2_type = e2_conf.get("e2_type")
            gettype = e2_conf.get("gettype")
            e2_decode = e2_conf.get("e2_decode")
            if e2_type not in ("onie_tlv", "fru", "fantlv", "wedge"):
                RJPRINT("%s unsupport e2_type: %s" % (name, e2_type))
                totalerr -= 1
                continue
            if gettype not in ("sysfs", "i2c"):
                RJPRINT("%s unsupport gettype: %s" % (name, gettype))
                totalerr -= 1
                continue
            if gettype == "sysfs":
                e2_path = e2_conf.get("e2_path")
                e2_size = e2_conf.get("e2_size", 256)
                e2_decode = e2_conf.get("e2_decode")
                ret, binval_bytes = dev_file_read(e2_path, 0, e2_size)
                if ret is False:
                    RJPRINT("%s read error, eeprom path: %s, msg: %s" % (name, e2_path, binval_bytes))
                    totalerr -= 1
                    continue
                binval = byteTostr(binval_bytes)
            else:
                e2_bus = e2_conf.get("bus")
                e2_loc = e2_conf.get("loc")
                binval = I2CUTIL.dumpValueByI2c(e2_bus, e2_loc)
            if e2_type == "onie_tlv":
                ret, msg = onie_eeprom_show(binval, e2_decode)
            elif e2_type == "fru":
                ret, msg = fru_eeprom_show(binval, e2_decode)
            elif e2_type == "fantlv":
                ret, msg = fantlv_eeprom_show(binval, e2_decode)
            else:
                ret, msg = wedge_eeprom_show(binval, e2_decode)
            if ret < 0:
                totalerr -= 1
                RJPRINT(msg)
        except Exception as e:
            totalerr -= 1
            msg = traceback.format_exc()
            RJPRINT(msg)
    RET[RETURN_KEY1] = totalerr
    return RET

#EMMC信息显示
def show_emmc_info():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    cmd = "fdisk -l"
    cap_threshoud = {"high":9000,"low":7000}
    ret, log1 = log_os_system(cmd, 0)
    if ret != 0 or len(log1) <= 0:
        msg = ("command[%s] execution error: %s" % (cmd, log1))
        RJPRINT(msg)
        RET[RETURN_KEY2] =msg
        RET[RETURN_KEY1] = -1
    else:
        data = re.findall(".*/dev/mmcblk0:\s+(\d*\.?\d+)\s+GiB.*",log1)
        if len(data) != 1:
            msg = ("Failed to get capacity information")
            RJPRINT(msg)
            RET[RETURN_KEY2] = msg
            RET[RETURN_KEY1] = -1
        else:
            msg = ("EMMC  capacity: %s G"%(data[0]))
            RJPRINT(msg)
            RET[RETURN_KEY2] = msg
            RET[RETURN_KEY1] = 0
    return RET


def test_emmc_status_check():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    ret ,log  = log_os_system("df -h | grep 'Mounted on\|/host'", 0)
    if ret == 0:
        RJPRINT(log)
        for line in log.splitlines():
            rows = line.split()
            if "Filesystem" in line:
                continue
            elif "/host" in line and (float(rows[4].strip("%")) > float(50)):
                RJPRINT("\n /host partition usage exceeds 50%")
                RET[RETURN_KEY1] = -1
    return RET


def reboot_system():
    ret, msg = rj_os_system("reboot -f")
    if ret == 0:
        return True, msg
    return False, msg

def firmware_check():
    # 电源防呆检测
    psu_check()
    # I210和mac检测
    fac_check_eth_mac()
    # RTC检测
    fac_check_rtc()
    # BMC在位检测
    fac_check_bmc_status()

def fac_firmware_init():
    cpld_init()

def test_bmc_ip():
    ret, bmcip = getBMCIP()
    if ret is False:
        msg = "get bmcip faled, log:%s" % bmcip
        return False, msg
    for i in range(0, 3):
        ret, msg = rj_os_system("ping -c 5 -w 5 %s > /dev/null" % bmcip)
        if ret == 0:
            return True, ""
    return False, msg

def bmc_diag_init():
    #openTxEth0()
    ret, log = test_bmc_ip()
    if ret is False:
        return False, "BMC IP not available"
    rj_os_system("chmod -R 777 %s" % BMC_DIAG_CONF_FILE_PATH)
    ret, log = scpFileToBMC(BMC_DIAG_CONF_FILE_PATH, "/tmp/")
    if ret is False:
        return False, "Failed to copy file to BMC"
    bcm_diag_service_cmd = "nohup python -u /tmp/bmc_factest/facserver.py > /dev/null 2>&1 &"
    cmd = "export %s &&%s" % (BMC_PATH, bcm_diag_service_cmd)
    ret, log = sshExecBMCCmd(cmd)
    if ret is False:
        return False, "BMC run facserver failed"
    ret_t = False
    time.sleep(10)
    for i in range(0, 10):
        ret, log = test_bmc_channel()
        if ret is False:
            time.sleep(1)
        else:
            ret_t = True
            break
    if ret_t is False:
        log_debug("test_bmc_channel timeout log: %s" % log)
        return False, log
    bmc_fpag_i2_access(True)

    return True, ""

def bmc_diag_exit():
    bmc_fpag_i2_access(False)
    sshExecBMCCmd("ps | grep facserver | grep -v grep | awk '{print $1}' | xargs kill -9")
    sshExecBMCCmd("rm -rf /tmp/bmc_factest")

def factest_check(argv):
    global Inspection_START_TIME
    Inspection_START_TIME = time.time()

    global BMC_DIAG_FLAG
    BMC_DIAG_FLAG = 0
    if len(argv) == 2 and argv[1] == 'diag':
        DIAGTEST = True
        bmcmac = getBMCMAC()
        RJPRINT("BMC MAC【%s】" % bmcmac)
    elif (len(argv) == 2 or len(argv) == 3) and (argv[1] == 'diagusb' or argv[1] == 'diagmanual'):
        if FACTESTMODULE.get("bmc_diag", 0) == 0 or (len(argv) == 3 and argv[2] == 'ignorebmc'):
            BMC_DIAG_FLAG = 0
        else :
            BMC_DIAG_FLAG = 1

        if BMC_DIAG_FLAG == 1:
            for i in range(0, 10):
                ret, log = bmc_diag_init()
                if ret is True:
                    log_debug("bmc_diag_init success, retry: %d" % i)
                    break
                log_debug("bmc_diag_init failed, retry: %d, msg: %s" % (i, log))
            if i >= 9:
                RJPRINT("x86-BMC channel check is abnormal")
                sys.exit(0)

        save_path = "/tmp/factestdiag"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        tmp_file = save_path + "/" +"tmp_save.txt"
        try:
            file = open(tmp_file,'w')
        except Exception as e:
            RJPRINT("open %s failed, msg: %s" % (tmp_file, str(e)))
            if BMC_DIAG_FLAG == 1:
                bmc_diag_exit()
            sys.exit(1)

        # 保存将结果打印到屏幕的旧sys.stdout配置，复原前RJPRINT将打印结果到指定file中
        oldstdout = sys.stdout
        sys.stdout = file

        if argv[1] == 'diagusb':
            diag_list = diagtestall
        else:
            diag_list = diag_manual

        # 执行巡检并保存数据到指定路径
        if BMC_DIAG_FLAG == 1:
            diag_list.extend(diagtestbmcall)
        ret = test_all_check(save_path, diag_list)
        # 复原sys.stdout配置，将缓存文件按照指定格式重命名
        file.close()
        sys.stdout = oldstdout
        fd = os.open(tmp_file, os.O_RDWR|os.O_CREAT)
        os.lseek(fd, 0, os.SEEK_SET)
        rd_str = os.read(fd, 100000).decode('utf-8')
        if isinstance(rd_str, bytes):
            rd_str = byteTostr(rd_str)
        RJPRINT("%s" % rd_str)
        #RJPRINT("%s" % ret["log"])
        if ret[RETURN_KEY1] == 0 and len(ret[RETURN_KEY2]) != 0:
            try:
                save_file = ret[RETURN_KEY2]
                os.system("mv %s %s" % (tmp_file, save_file))
                os.system("sync")
            except Exception as e:
                RJPRINT("Write inspection result failed, msg: %s" % str(e))
            RJPRINT("Inspection completed")
        else:
            RJPRINT("Execution of inspection failed")

        if BMC_DIAG_FLAG == 1:
            bmc_diag_exit()

        if ret[RETURN_KEY3] == 0:
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        pass

## 生产测试主程序
if __name__ == '__main__':
    # ApplicationInstance()
    #print sys.getdefaultencoding()
    #print sys.getfilesystemencoding()
    #import locale
    #print locale.getdefaultlocale()
    root_check()
    factest_check(sys.argv)
    #start()
