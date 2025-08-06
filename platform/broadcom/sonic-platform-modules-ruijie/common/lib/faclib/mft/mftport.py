#!/usr/bin/python3
# -*- coding: UTF-8 -*-
u'''生测PORT组件'''
import time
import os
import re
import io
import logging
import syslog
import subprocess
import collections
import json
import collections
import traceback
import abc
import sys
import click
import copy
import yaml
import threading
from scapy.all import *
import datetime

from sfputil.main import *
from faclib.config.facconfig import *

SYSLOG_IDENTIFIER = "PORT"
SAI_PROFILE = "sai.profile"
SAI_PROFILE_PREDIX = "SAI_INIT_CONFIG_FILE=/usr/share/sonic/hwsku/"
CONFIG_DB_JSON_PATH = "/etc/sonic/config_db.json"
MACHINE_FILE = "/host/machine.conf"
MACHINE_PLATFORM_PREDIX = "onie_platform="

LOG_DEBUG_LEVEL = 1
LOG_INFO_LEVEL = 2
LOG_WARNING_LEVEL = 3
LOG_ERROR_LEVEL = 4

LANE_MAX = 4
PACKETS_COUNT = 10000
PACKETS_SIZE = 64
PACKETS_DST_MAC = "ff:ff:ff:ff:ff:ff"
PORT_TEST_VLAN = 4048
KR_VLAN = 4080
PRBS_BER_DEFAULT = 1.0e-8
PRBS_TIME_DEFAULT = 120
PRBS_WAIT_TIME = 10

# True: 同时将log打印出来(默认False)
log_also_print_to_console = False
# True: 同时将cmd打印出来(默认False)
cmd_also_print_to_console = False
# True: 同时将cmd执行结果打印出来(默认False)
cmd_output_also_print_to_console = False
# True: 测试失败时将整个测试流程的log打印到控制台(默认True)
port_log_info_print_to_console = False
# True: 开启输入重定向  cmd + < /dev/null(默认True)
sdk_cmd_redirect_console = True

# 生测Port相关配置, 从配置文件中获取
global_port_config = {
    "hsdk_device": 1,  # bcmcmdb 设备
    "mgmt_kt_ports": {},
    "prbs_port_range": "",
    "extphy_device": 0,
    "prbs_ber": PRBS_BER_DEFAULT,
    "prbs_time": PRBS_TIME_DEFAULT,
    "prbs_ber_dict": None,  # 设备单个端口对应的误码率
    "port_frame_test_retrynum": 1,  # 端口收发帧重试次数(内部重试)
    "port_brcst_test_retrynum": 1,  # 端口广播测试重试次数(内部重试)
    "port_prbs_test_retrynum": 1,  # 端口PRBS测试重试次数(内部重试)
    "port_kr_test_retrynum": 1,  # 内部管理口测试重试次数(内部重试)
    "port_frame_del_time": 10,  # 端口收发帧恢复测试环境等待时间(s)
    "port_brcst_del_time": 10,  # 端口广播测试恢复测试环境等待时间(s)
    "port_prbs_del_time": 10,  # 端口PRBS测试恢复测试环境等待时间(s)
    "port_kr_del_time": 10,  # 内部管理口测试恢复测试环境等待时间(s)
    "port_log_level": LOG_ERROR_LEVEL,  # PORT组件log级别
    "flag": False  # 是否已经载入port配置
}

global_port_log_info = "port_log_info:\n"
global_prbs_info = ""
global_onie_platform = ""
global_unit_port_list = []

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class AliasedGroup(click.Group):
    u'''命令别名'''

    def get_command(self, ctx, cmd_name):
        u'''获取命令'''
        get_rv = click.Group.get_command(self, ctx, cmd_name)
        if get_rv is not None:
            return get_rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if matches:
            if len(matches) == 1:
                return click.Group.get_command(self, ctx, matches[0])
            ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))
        return None


def singleton(cls):
    u'''单例'''

    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


def log_info_gather_fun(log_content):
    u'''测试过程的log收集'''

    global global_port_log_info
    global_port_log_info = global_port_log_info + "\n" + log_content


def prbs_info_gather_fun(prbs_content, clear=False):
    u'''prbs测试过程的信息收集'''

    global global_prbs_info
    if clear == True:
        global_prbs_info = prbs_content
    else:
        global_prbs_info = global_prbs_info + "\n" + prbs_content


def log_debug(msg):
    u'''debug日志'''

    funcName = sys._getframe().f_back.f_code.co_name  # 获取调用函数名
    lineNumber = sys._getframe().f_back.f_lineno     # 获取行号
    dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 含微秒的日期时间
    info_str = dt_ms + "| DEBUG PORT: " + funcName + ": " + str(lineNumber)
    log_info_gather = "%-40s| %s" % (info_str, str(msg))
    log_info_gather_fun(log_info_gather)
    if global_port_config["port_log_level"] <= LOG_DEBUG_LEVEL:
        try:
            syslog.openlog(SYSLOG_IDENTIFIER)
            syslog.syslog(syslog.LOG_DEBUG, msg)
            syslog.closelog()

            if log_also_print_to_console:
                click.echo(log_info_gather)
        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)


def log_info(msg):
    u'''info日志'''

    funcName = sys._getframe().f_back.f_code.co_name  # 获取调用函数名
    lineNumber = sys._getframe().f_back.f_lineno     # 获取行号
    dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 含微秒的日期时间
    info_str = dt_ms + "| INFO PORT: " + funcName + ": " + str(lineNumber)
    log_info_gather = "%-40s| %s" % (info_str, str(msg))
    log_info_gather_fun(log_info_gather)
    if global_port_config["port_log_level"] <= LOG_INFO_LEVEL:
        try:
            syslog.openlog(SYSLOG_IDENTIFIER)
            syslog.syslog(syslog.LOG_INFO, msg)
            syslog.closelog()

            if log_also_print_to_console:
                click.echo(log_info_gather)
        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)


def log_warning(msg):
    u'''warning日志'''

    funcName = sys._getframe().f_back.f_code.co_name  # 获取调用函数名
    lineNumber = sys._getframe().f_back.f_lineno     # 获取行号
    dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 含微秒的日期时间
    info_str = dt_ms + "| WARNING PORT: " + funcName + ": " + str(lineNumber)
    log_info_gather = "%-40s| %s" % (info_str, str(msg))
    log_info_gather_fun(log_info_gather)
    if global_port_config["port_log_level"] <= LOG_WARNING_LEVEL:
        try:
            syslog.openlog(SYSLOG_IDENTIFIER)
            syslog.syslog(syslog.LOG_WARNING, msg)
            syslog.closelog()

            if log_also_print_to_console:
                click.echo(log_info_gather)
        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)


def log_error(msg):
    u'''error日志'''

    funcName = sys._getframe().f_back.f_code.co_name  # 获取调用函数名
    lineNumber = sys._getframe().f_back.f_lineno     # 获取行号
    dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')  # 含微秒的日期时间
    info_str = dt_ms + "| ERROR PORT: " + funcName + ": " + str(lineNumber)
    log_info_gather = "%-40s| %s" % (info_str, str(msg))
    log_info_gather_fun(log_info_gather)
    if global_port_config["port_log_level"] <= LOG_ERROR_LEVEL:
        try:
            syslog.openlog(SYSLOG_IDENTIFIER)
            syslog.syslog(syslog.LOG_ERR, msg)
            syslog.closelog()

            if log_also_print_to_console:
                click.echo(log_info_gather)
        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)


def sdkcmdb_os_system(cmd):
    with bcmcmdb_lock:
        status, output = subprocess.getstatusoutput(cmd)
    return status, output


def port_getstatusoutput_one_time(cmd, time_sleep=0):
    u'''获取命令的执行结果一次'''

    if hsdk_check():
        ret, output = sdkcmdb_os_system(cmd)
    else:
        ret, output = subprocess.getstatusoutput(cmd)

    t = int(time_sleep)
    if cmd_also_print_to_console:
        log_debug(cmd)
    if cmd_output_also_print_to_console:
        log_debug(output)
    if t != 0:
        log_debug("time sleep: %ds" % t)
        time.sleep(t)
    if ret == 0:
        if (re.search('hsdk msg connect fail', output.strip())):
            return -1, output
        return ret, output
    else:
        output_content = "cmd: %s execution fail, output:%s" % (cmd, output)
        return_output_content = output_content.replace("\"", "'")
        log_error("%s" % output_content)
        return ret, "%s" % return_output_content


def port_checkstatusoutput(output):
    if (re.search('cmicx_sbusdma_error', output.strip())):
        return False
    return True


def port_getstatusoutput(cmd, time_sleep=0):
    u'''获取命令的执行结果'''

    ret = -1
    output = ""
    retry_time = 0
    for i in range(3):
        retry_time = i + 1
        ret, output = port_getstatusoutput_one_time(cmd, time_sleep)
        if ret != 0:
            break
        if port_checkstatusoutput(output) is False:
            log_error("[%d] cmd:%s output:%s\n port_checkstatusoutput fail" % (retry_time, cmd, output))
            if "tx" in cmd and "DestMac" in cmd:
                log_debug("cmd: %s not need retry" % (cmd))
                break
            time.sleep(5)
            continue
        break
    return ret, output


def get_sdk_cmd(cmd, time_out=0, grep=""):
    u'''对传入的cmd进行组合, 返回sdk_cmd'''

    cmd_str = ""
    sdk_cmd = ""
    t = int(time_out)
    if (hsdk_check()):
        sdk_cmd = "bcmcmdb "
    else:
        sdk_cmd = "bcmcmd "
    if t != 0:
        cmd_str = sdk_cmd + "-t %d \"" % t
    else:
        cmd_str = sdk_cmd + "\""
    if sdk_cmd_redirect_console == True:
        cmd_str = cmd_str + str(cmd) + "\" < /dev/null"
    else:
        cmd_str = cmd_str + str(cmd) + "\""
    if grep != "":
        cmd_str += " | grep \"%s\"" % str(grep)
    return cmd_str

###################### HSDK Class ######################


class PortHsdkClass():
    u'''PortHsdkClass类主要用于存储端口在不同层级的别名及相关信息'''

    def __init__(self, **kwargs):

        lport = kwargs.get("lport", 0)
        bcm_port = kwargs.get("bcm_port", "")
        interface = kwargs.get("interface", "")
        unit_port = kwargs.get("unit_port", 0)
        phy_port = kwargs.get("phy_port", 0)
        prbs_ber = kwargs.get("prbs_ber", PRBS_BER_DEFAULT)

        self._lport = lport
        self._interface = interface
        self._bcm_port = bcm_port
        self._unit_port = unit_port
        self._phy_port = phy_port
        self._prbs_ber = prbs_ber

    @property
    def lport(self):
        u'''返回lport'''

        return self._lport

    @property
    def interface(self):
        u'''返回interface'''

        return self._interface

    @property
    def bcm_port(self):
        u'''返回bcm_port'''

        return self._bcm_port

    @property
    def unit_port(self):
        u'''返回unit_port'''

        return self._unit_port

    @property
    def phy_port(self):
        u'''返回phy_port'''

        return self._phy_port

    @property
    def prbs_ber(self):
        u'''返回prbs_ber'''

        return self._prbs_ber

    def set_lport(self, lport):
        u'''设置lport'''

        self._lport = lport

    def set_interface(self, interface):
        u'''设置interface'''

        self._interface = interface

    def set_bcm_port(self, bcm_port):
        u'''设置bcm_port'''

        self._bcm_port = bcm_port

    def set_unit_port(self, unit_port):
        u'''设置unit_port'''

        self._unit_port = unit_port

    def set_phy_port(self, phy_port):
        u'''设置phy_port'''

        self._phy_port = phy_port

    def set_prbs_ber(self, prbs_ber):
        u'''设置prbs_ber'''

        self._prbs_ber = prbs_ber


class PortHsdkUtil():
    u'''Port工具类'''

    @staticmethod
    def get_config_bcm_path():
        u'''返回config_bcm的地址'''

        config_bcm_path = ""
        try:
            (platform, hwsku) = get_platform_and_hwsku()
            platform_path = "/".join([PLATFORM_ROOT_PATH, platform])
            hwsku_path = "/".join([platform_path, hwsku])
            saiprofile_path = "/".join([hwsku_path, SAI_PROFILE])
            with open(saiprofile_path, "r") as saiprofile_f:
                for line in saiprofile_f:
                    if re.search('%s(.*?)$' % SAI_PROFILE_PREDIX, line):
                        config_bcm = re.findall(r"%s(.*?)$" % SAI_PROFILE_PREDIX, line)[0]
                        config_bcm_path = "/".join([hwsku_path, config_bcm])
        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)

        return config_bcm_path

    @staticmethod
    def get_port_config_path():
        u'''返回port_config的地址'''

        port_config_path = get_path_to_port_config_file()
        return port_config_path

    @staticmethod
    def get_onie_platform():
        u'''获取onie_platform'''

        log_debug("获取onie_platform")
        with open(MACHINE_FILE, "r") as machine_f:
            for line in machine_f:
                if(re.search('%s(.*?)$' % MACHINE_PLATFORM_PREDIX, line)):
                    onie_platform = re.findall(r"%s(.*?)$" % MACHINE_PLATFORM_PREDIX, line)[0]
                    global global_onie_platform
                    global_onie_platform = onie_platform
                    log_debug("onie_platform:%s" % global_onie_platform)
                    return onie_platform
        return None

    class ReUtil():
        u'''正则工具类'''

        @staticmethod
        def is_port_id_line(line):
            u'''判断是否port_id行'''

            if re.search('_PORT_ID:(.*?)$', line.strip()):
                return False
            elif re.search(r'PORT_ID: \[', line.strip()):
                return False
            elif re.search('PORT_ID:(.*?)$', line.strip()):
                return True
            return False

        @staticmethod
        def is_pc_phys_port_id_line(line):
            u'''判断是否pc_phys_phy_port_id行'''

            if re.search('PC_PHYS_PORT_ID:(.*?)$', line.strip()):
                return True
            return False

        @staticmethod
        def yaml_getre_unit_port(line):
            return int(re.findall(r"PORT_ID:(.*?)$", line.strip())[0])

        @staticmethod
        def yaml_getre_phy_port(line):
            return int(re.findall(r"PC_PHYS_PORT_ID:(.*?)$", line.strip())[0])

        @staticmethod
        def getre_port_status(output):
            u'''解析返回结果，获取端口up/down状态'''
            lines = output.split("\n")

            if len(lines) > 3:
                if re.search("up", lines[3]):
                    return True, "up"
                elif re.search("!ena", lines[3]):
                    return True, "!ena"
                elif re.search("down", lines[3]):
                    return True, "down"
                else:
                    return False, output
            else:
                return False, output

        @staticmethod
        def is_unit_port_line(line, unit_port):
            u'''判断是否存该unit_port的line'''

            if (re.search(r"^.*?\(.*?\)", line) and
                    int(re.findall(r"^.*?\((.*?)\)", line)[0].strip()) == unit_port):
                return True
            return False

        @staticmethod
        def getre_output_bcm_port(output):
            u'''解析返回结果，获取bcm_port/mgmt_bcm_port'''

            return re.findall(r"^(.*?)\(.*?\)", output)[0].strip()

        @staticmethod
        def getre_output_packets_count(line):
            u'''解析返回结果，获取收/发包数量'''
            if (len(line.split())) > 2:
                return int(re.sub('[,]', '', line.split()[2].strip("+-")))
            else:
                return 0

        @staticmethod
        def getre_output_unit_port(output):
            u'''解析返回结果，获取unit_port'''

            return int((output.split(')')[0]).split('(')[1])

        @staticmethod
        def getre_output_speed(line):
            u'''解析返回结果，获取speed'''

            if (len(line.split())) > 4:
                speed = (line.split("FD"))[0].split()[-1]
                if "G" in speed:
                    return speed
            return None

        @staticmethod
        def getre_output_rx_packets(line):
            u'''解析返回结果，获取内部管理口rx_packets'''

            rx_packets = 0
            if (len(line.split())) > 2:
                rx_packets = int(line.split()[2])

            return rx_packets


class PortHsdkTest():
    u'''PortHsdkTest父类'''

    device_port_list = []
    bcm_ports = []
    ifconig_rx_packet_dict = {"old_packet": {}, "new_packet": {}}
    prbs_port_range = None
    standard_ber_val = None
    prbs_time = None
    kr_thread = None

    def __init__(self):
        if global_onie_platform == "":
            PortHsdkUtil.get_onie_platform()
        self.get_factest_port_config()
        if len(self.device_port_list) == 0:
            self._config_yaml_file = io.open(PortHsdkUtil.get_config_bcm_path(), 'r', encoding="utf-8")
            self._port_config_file = open(PortHsdkUtil.get_port_config_path(), 'r+')
            self.__parse_port_config()
            self.__parse_yaml_data()
            self.__get_prbs_ber()
            self.__get_global_bcmports()
            self._config_yaml_file.flush()
            self._port_config_file.flush()
            self._config_yaml_file.close()
            self._port_config_file.close()
        if self.prbs_time is None:
            self.prbs_time = global_port_config.get("prbs_time", PRBS_TIME_DEFAULT)
        if self.standard_ber_val is None:
            self.standard_ber_val = global_port_config.get("prbs_ber", PRBS_BER_DEFAULT)

    @abc.abstractmethod
    def init_test(self):
        u'''抽象方法,待继承'''

        return None

    @abc.abstractmethod
    def start_test(self, **kwargs):
        u'''抽象方法,待继承'''

        return None

    @abc.abstractmethod
    def check_test(self, **kwargs):
        u'''抽象方法,待继承'''

        return None

    @abc.abstractmethod
    def del_test(self):
        u'''抽象方法,待继承'''

        return None

    def __parse_port_config(self):
        u'''解析port_config, 获取lport, interface, phy_port'''

        log_debug("解析port_config")
        lport_num = 0
        for line in self._port_config_file:
            line.strip()
            if len(line.split()) > 0 and re.search("Eth", line.split()[0]):
                lport_num = lport_num + 1
                phy_port_t = int(line.split()[1].split(',')[0])
                self.device_port_list.append(PortHsdkClass(lport=lport_num,
                                                           interface=line.split()[0],
                                                           phy_port=phy_port_t))

    def __parse_yaml_data(self):
        u'''解析yaml中port_id、phy_port_id行的配置'''

        log_debug("解析yaml")
        unit_port = 0
        phy_port = 0
        curr_line_num = 0
        port_id_line = 0
        phy_port_id_line = 0
        reutil = PortHsdkUtil.ReUtil()
        for line in self._config_yaml_file:
            curr_line_num = curr_line_num + 1
            if reutil.is_port_id_line(line):
                port_id_line = curr_line_num
                unit_port = reutil.yaml_getre_unit_port(line)
            if (curr_line_num == (port_id_line + 2)):
                if reutil.is_pc_phys_port_id_line(line):
                    phy_port_id_line = curr_line_num
                    phy_port = reutil.yaml_getre_phy_port(line)
                    for port_obj in self.device_port_list:
                        if port_obj.phy_port == phy_port:
                            port_obj.set_unit_port(unit_port)
                            break

    def __get_prbs_ber(self):
        u'''获取单个端口误码率'''

        log_debug("获取prbs_ber")
        prbs_ber = PRBS_BER_DEFAULT
        for port_obj in self.device_port_list:
            if global_port_config.get("prbs_ber_dict", None):
                prbs_ber = global_port_config["prbs_ber_dict"].get(port_obj.lport, PRBS_BER_DEFAULT)
            else:
                prbs_ber = global_port_config.get("prbs_ber", PRBS_BER_DEFAULT)
            port_obj.set_prbs_ber(prbs_ber)

    def __get_global_bcmports(self):
        u'''获取ps返回结果中的bcm_port, unit_port部分'''

        cmd = get_sdk_cmd("ps")
        ret, output = port_getstatusoutput(cmd)
        lines = output.split("\n")
        if ret == 0:
            for line in lines:
                if (re.search(r'(.*?)\((.*?)$', line.strip())):
                    unit_port = PortHsdkUtil.ReUtil.getre_output_unit_port(line)
                    bcm_port = PortHsdkUtil.ReUtil.getre_output_bcm_port(line)
                    for port_obj in self.device_port_list:
                        if port_obj.unit_port == unit_port:
                            port_obj.set_bcm_port(bcm_port)
                            break
            for port_obj in self.device_port_list:
                self.bcm_ports.append(str(port_obj.bcm_port))
            log_debug("bcm_ports:%s" % self.bcm_ports)

    def get_port_status(self, port):
        u'''获取端口up/down情况, 返回up/down/!ena'''

        # 获取bcm_port
        cmd = get_sdk_cmd("ps %s" % self.device_port_list[port - 1].bcm_port)
        ret, output = port_getstatusoutput(cmd)

        if ret == 0:
            return PortHsdkUtil.ReUtil.getre_port_status(output)
        return False, output

    @classmethod
    def clear_port_packets(cls):
        u'''清除SDK 统计的报文'''

        # 调用SDK指令清除port_packets
        # 清除报文统计数据
        cmd = get_sdk_cmd("clear c")
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, output

        log_debug("clear_port_packets success")
        return True, output

    def start_send_port_packets(self, port, count, size, dst_mac):
        u'''调用SDK指令进行发包'''

        # 使用tx指令发包
        cmd = get_sdk_cmd("tx %d VLantag=4048 PortBitMap=%s Length=%d DestMac=%s"
                          % (count, self.device_port_list[port - 1].bcm_port, size, dst_mac))
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, output
        return True, output

    def vlan_config(self, vlan):
        u'''测试vlan配置'''

        # 清除之前配置的vlan
        ret, output = self.vlan_config_clear()
        if ret is False:
            log_warning("vlan_config fail, output:%s" % output)
            return False, "vlan_config fail, output:%s" % output

        # 遍历所有端口配置vlan
        for i in range(len(self.device_port_list)):
            bcm_port = self.device_port_list[i].bcm_port
            if i == 0:
                # 配置vlan 第一个端口用create, 后面的用add
                cmd = get_sdk_cmd("vlan create %d PortBitMap=%s UntagBitMap=%s" % (vlan,
                                                                                   bcm_port,
                                                                                   bcm_port))
            else:
                cmd = get_sdk_cmd("vlan add %d PortBitMap=%s UntagBitMap=%s" % (vlan,
                                                                                bcm_port,
                                                                                bcm_port))
            ret, output = port_getstatusoutput(cmd)
            if ret != 0:
                log_warning("vlan_config vlan create or add fail, output:%s" % output)
                return False, "vlan_config vlan create or add fail, output:%s" % output

            # 配置pvlan
            cmd = get_sdk_cmd("pvlan set %s %d" % (bcm_port, vlan))
            ret, output = port_getstatusoutput(cmd)
            if ret != 0:
                log_warning("vlan_config pvlan set fail, output:%s" % output)
                return False, "vlan_config pvlan set fail, output:%s" % output

        log_debug("vlan_config success")
        return True, "vlan_config success"

    @classmethod
    def vlan_config_clear(cls):
        u'''端口测试vlan环境恢复'''

        cmd = get_sdk_cmd("vlan clear")
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            log_warning("vlan_config_clear fail, output:%s" % output)
            return False, "vlan_config_clear fail, output:%s" % output

        log_debug("vlan_config_clear success")
        return True, "vlan_config_clear success"

    def get_mgmt_bcmport_one_time(self, mgmt_eth):
        u'''获取内部管理口一次'''

        try:
            cmd = get_sdk_cmd("ps")
            ret, output = port_getstatusoutput(cmd)
            lines = output.split("\n")
            if ret == 0:
                unit_port = global_port_config["mgmt_kt_ports"][mgmt_eth]
                for line in lines:
                    line.strip()
                    if PortHsdkUtil.ReUtil.is_unit_port_line(line, unit_port):
                        bcmport = PortHsdkUtil.ReUtil.getre_output_bcm_port(line)
                        return bcmport
        except Exception as except_result:
            msg = traceback.format_exc()
            log_error("Exception_info:\n%s" % msg)
        return None

    def get_mgmt_bcmport(self, mgmt_eth):
        u'''获取内部管理口'''

        retry_time = 0
        mgmt_bcmport = None
        for i in range(3):
            retry_time = i + 1
            mgmt_bcmport = self.get_mgmt_bcmport_one_time(mgmt_eth)
            if mgmt_bcmport is not None:
                break
            time.sleep(5)
        log_debug("[%d] %s bcmport: %s" % (retry_time, mgmt_eth, mgmt_bcmport))
        return mgmt_bcmport

    def set_all_mgmt_enable(self, enable):
        u'''控制所有内部管理口的使能'''

        # 对所有内部管理口进行操作，设置en=0/1
        # enable = 1 up down
        # enable = 0 !ena
        cmd = None
        try:
            cmd = get_sdk_cmd("port %s en=%d" % (",".join(self.get_mgmt_bcmport(item)
                                                          for item
                                                          in global_port_config["mgmt_kt_ports"]), enable))
        except Exception as except_result:
            msg = traceback.format_exc()
            log_error("Exception_info:\n%s" % msg)
            return False, "set_all_mgmt_enable:%d fail, output:%s" % (enable, msg)
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            log_warning("set_all_mgmt_enable:%d fail, output:%s" % (enable, output))
            return False, "set_all_mgmt_enable:%d fail, output:%s" % (enable, output)

        log_debug("set_all_mgmt_enable:%d success" % enable)
        return True, "set_all_mgmt_enable:%d success" % enable

    def port_stp_config(self, enable):
        u'''生成树协议配置'''

        if enable == 1:
            log_debug("开启STP")
            cmd = get_sdk_cmd("stg stp 1 all forward")
            ret, output = port_getstatusoutput(cmd)
            if ret == 0:
                # 关掉多配置的内部管理口生成树协议
                cmd = get_sdk_cmd("stg stp 1 %s disable" % (",".join(self.get_mgmt_bcmport(item)
                                                                     for item
                                                                     in global_port_config["mgmt_kt_ports"])))
                ret, output = port_getstatusoutput(cmd)
        else:
            log_debug("关闭STP")
            cmd = get_sdk_cmd("stg stp 1 all disable")
            ret, output = port_getstatusoutput(cmd)

        if ret != 0:
            return False, "port_stp_config fail, output:%s" % output
        return True, "port_stp_config success"

    def get_unit_port_list(self, port_list):
        u'''获取up端口的unit_port列表'''

        self.set_global_unit_port_list_null()
        for port in port_list:
            unit_port = self.device_port_list[port - 1].unit_port
            global global_unit_port_list
            global_unit_port_list.append(unit_port)
        log_debug("unit_port_list:%s" % global_unit_port_list)

    @classmethod
    def get_min_max_unit_port(cls):
        u'''获取unit_port列表里最小和最大的unit_port'''

        min_unit_port = 1
        max_unit_port = 1
        if len(global_unit_port_list) > 0:
            min_unit_port = int(min(global_unit_port_list))
            max_unit_port = int(max(global_unit_port_list))
        log_debug("min_unit_port = %d max_unit_port = %d" % (min_unit_port, max_unit_port))
        return min_unit_port, max_unit_port

    def get_prbs_port_range(self):
        u'''获取面板口unit_port范围(不包含mgmt口和loopback口)'''

        self.prbs_port_range = global_port_config.get("prbs_port_range", None)
        if self.prbs_port_range is None:
            min_unit_port, max_unit_port = self.get_min_max_unit_port()
            self.prbs_port_range = "%s-%s" % (str(min_unit_port), str(max_unit_port))

    @classmethod
    def set_global_unit_port_list_null(cls):
        global global_unit_port_list
        global_unit_port_list = []

    def get_factest_port_config_flag(self):
        return global_port_config["flag"]

    def get_factest_port_config(self):
        if self.get_factest_port_config_flag() is False:
            if TESTCASE:
                mft_portconfig = {}
                if TESTCASE.get("mft_port", {}):
                    mft_portconfig = copy.deepcopy(TESTCASE.get("mft_port", {}))
                port_config = {
                    "hsdk_device": 1,
                    "mgmt_kt_ports": {},
                    "prbs_port_range": "",
                    "extphy_device": 0,
                    "prbs_ber": PRBS_BER_DEFAULT,
                    "prbs_time": PRBS_TIME_DEFAULT,
                    "port_frame_test_retrynum": 1,  # 端口收发帧重试次数(内部重试)
                    "port_brcst_test_retrynum": 1,  # 端口广播测试重试次数(内部重试)
                    "port_prbs_test_retrynum": 1,  # 端口PRBS测试重试次数(内部重试)
                    "port_kr_test_retrynum": 1,  # 内部管理口测试重试次数(内部重试)
                    "port_frame_del_time": 10,  # 端口收发帧恢复测试环境等待时间(s)
                    "port_brcst_del_time": 10,  # 端口广播测试恢复测试环境等待时间(s)
                    "port_prbs_del_time": 10,  # 端口PRBS测试恢复测试环境等待时间(s)
                    "port_kr_del_time": 10,  # 内部管理口测试恢复测试环境等待时间(s)
                    "port_log_level": LOG_ERROR_LEVEL,  # PORT组件log级别
                    "flag": False
                }
                try:
                    port_config["mgmt_kt_ports"] = copy.deepcopy(mft_portconfig["mgmt_kt_ports"])
                    log_debug("mgmt_kt_ports: %s" % port_config["mgmt_kt_ports"])

                    port_config["prbs_port_range"] = mft_portconfig.get("prbs_port_range", None)
                    log_debug("prbs_port_range: %s" % port_config["prbs_port_range"])

                    port_config["hsdk_device"] = mft_portconfig["hsdk_device"]
                    log_debug("hsdk_device: %s" % port_config["hsdk_device"])

                    port_config["extphy_device"] = mft_portconfig["extphy_device"]
                    log_debug("extphy_device: %s" % port_config["extphy_device"])

                    port_config["prbs_ber"] = mft_portconfig["prbs_ber"]
                    log_debug("prbs_ber: %s" % port_config["prbs_ber"])

                    port_config["prbs_time"] = mft_portconfig["prbs_time"]
                    log_debug("prbs_time: %s" % port_config["prbs_time"])

                    if mft_portconfig.get("prbs_ber_dict", None):
                        port_config["prbs_ber_dict"] = copy.deepcopy(mft_portconfig["prbs_ber_dict"])
                        log_debug("prbs_ber_dict: %s" % port_config["prbs_ber_dict"])

                    port_config["port_frame_test_retrynum"] = mft_portconfig["port_frame_test_retrynum"]
                    log_debug("port_frame_test_retrynum: %s" % port_config["port_frame_test_retrynum"])

                    port_config["port_brcst_test_retrynum"] = mft_portconfig["port_brcst_test_retrynum"]
                    log_debug("port_brcst_test_retrynum: %s" % port_config["port_brcst_test_retrynum"])

                    port_config["port_prbs_test_retrynum"] = mft_portconfig["port_prbs_test_retrynum"]
                    log_debug("port_prbs_test_retrynum: %s" % port_config["port_prbs_test_retrynum"])

                    port_config["port_kr_test_retrynum"] = mft_portconfig["port_kr_test_retrynum"]
                    log_debug("port_kr_test_retrynum: %s" % port_config["port_kr_test_retrynum"])

                    port_config["port_frame_del_time"] = mft_portconfig["port_frame_del_time"]
                    log_debug("port_frame_del_time: %s" % port_config["port_frame_del_time"])

                    port_config["port_brcst_del_time"] = mft_portconfig["port_brcst_del_time"]
                    log_debug("port_brcst_del_time: %s" % port_config["port_brcst_del_time"])

                    port_config["port_prbs_del_time"] = mft_portconfig["port_prbs_del_time"]
                    log_debug("port_prbs_del_time: %s" % port_config["port_prbs_del_time"])

                    port_config["port_kr_del_time"] = mft_portconfig["port_kr_del_time"]
                    log_debug("port_kr_del_time: %s" % port_config["port_kr_del_time"])

                    port_config["port_log_level"] = mft_portconfig["port_log_level"]
                    log_debug("port_log_level: %s" % port_config["port_log_level"])
                except Exception as except_result:
                    msg = traceback.format_exc()
                    print("Exception_info:\n%s" % msg)

                port_config["flag"] = True
                global global_port_config
                global_port_config = copy.deepcopy(port_config)
                log_debug("global_port_config: %s" % global_port_config)
            else:
                print("TESTCASE: %s" % TESTCASE)


@singleton
class PortHsdkFrameTest(PortHsdkTest):
    u'''端口收发帧'''

    def init_test(self):
        u'''端口收发帧测试初始化'''

        log_debug("init_test")
        ret, output = self.clear_port_packets()
        if ret is False:
            log_error("clear_port_packets fail, output:%s" % output)
            return False, "clear_port_packets fail, output:%s" % output

        ret, output = self.cpu_create()
        if ret is False:
            log_error("cpu_create fail, output:%s" % output)
            return False, "cpu_create fail, output:%s" % output

        ret, output = self.port_stp_config(1)
        if ret is False:
            log_error("port_stp_config fail, output:%s" % output)
            return False, "port_stp_config fail, output:%s" % output

        ret, output = self.vlan_config(PORT_TEST_VLAN)
        if ret is False:
            log_error("vlan_config fail, output:%s" % output)
            return False, "vlan_config fail, output:%s" % output

        cmd = get_sdk_cmd("counter on")
        ret, output = port_getstatusoutput(cmd)

        log_debug("init_test success")
        return True, "init_test success"

    def start_test(self, **kwargs):
        u'''端口收发帧测试开始'''

        port = kwargs["port"]
        count = kwargs.get("count", PACKETS_COUNT)
        size = kwargs.get("size", PACKETS_SIZE)
        dst_mac = kwargs.get("dst_mac", PACKETS_DST_MAC)

        log_debug("start_test")
        return self.start_send_port_packets(port, count, size, dst_mac)

    def check_test(self, **kwargs):
        u'''端口收发帧测试结果获取'''

        port = kwargs["port"]
        count = kwargs.get("count", PACKETS_COUNT)
        direc = kwargs.get("direc", "tx")

        log_debug("check_test")
        return self.check_port_packets(port, count, direc)

    def del_test(self):
        u'''端口收发帧测试环境恢复'''

        log_debug("del_test")
        ret, output = self.vlan_config_clear()
        if ret is False:
            log_error("vlan_config_clear fail, output:%s" % output)
            return False, output

        ret, output = self.cpu_destroy()
        if ret is False:
            log_error("cpu_destroy fail,%s" % output)
            return False, "cpu_destroy fail,%s" % output

        ret, output = self.port_stp_config(0)
        if ret is False:
            log_error("port_stp_config fail, output:%s" % output)
            return False, output

        log_debug("del_test success")
        return True, "cpu_destroy success"

    def check_port_packets(self, port, count, direc="tx"):
        u'''检查端口收发帧测试结果'''
        # 提取具体端口的统计结果。如果端口接收到的数目与发送数目相同，
        # 则返回该端口成功，否则则返回该端口失败及失败原因。

        if direc == "tx":
            return self.check_port_packets_tx(port, count)
        if direc == "rx":
            return self.check_port_packets_rx(port, count)

        return False, "check_port_packets_fail"

    def check_port_packets_tx(self, port, count):
        u'''direc == "tx"'''

        # 查看报文收发统计数据
        count_pkt = 0
        count_1518 = 0
        result_str = ""
        bcm_port = self.device_port_list[port - 1].bcm_port
        log_debug("bcm_port:%s direc:tx" % bcm_port)

        cmd = get_sdk_cmd("counter on")
        ret, output = port_getstatusoutput(cmd)
        cmd = get_sdk_cmd("show c %s" % bcm_port)
        ret, output = port_getstatusoutput(cmd)
        lines = output.split("\n")
        if ret == 0:
            for line in lines:
                if (re.search('XLMIB_TPKT(.*?)$', line.strip())):
                    count_pkt = PortHsdkUtil.ReUtil.getre_output_packets_count(line)
                elif (re.search('XLMIB_T1518(.*?)$', line.strip())):
                    count_1518 = PortHsdkUtil.ReUtil.getre_output_packets_count(line)
        else:
            return False, output

        log_debug("count:%d" % count)
        log_debug("count_pkt:%d" % count_pkt)
        log_debug("count_1518:%d" % count_1518)
        result_str += "count:%d\n" % count
        result_str += "count_pkt:%d\n" % count_pkt
        result_str += "count_1518:%d\n" % count_1518

        if (count_pkt == 0 or count_1518 == 0):
            result_str += "output:%s\n" % output
            log_warning("output:%s" % output)
        if (count == count_pkt and count == count_1518):
            log_debug("check_port_packets tx success")
            return True, result_str

        log_warning("check_port_packets_tx_fail, output:%s" % output)
        return False, result_str

    def check_port_packets_rx(self, port, count):
        u'''direc == "rx"'''

        # 查看报文收发统计数据
        count_pkt = 0
        count_1518 = 0
        result_str = ""
        bcm_port = self.device_port_list[port - 1].bcm_port
        log_debug("bcm_port:%s direc:rx" % bcm_port)

        cmd = get_sdk_cmd("counter on")
        ret, output = port_getstatusoutput(cmd)
        cmd = get_sdk_cmd("show c %s" % bcm_port)
        ret, output = port_getstatusoutput(cmd)
        if ret == 0:
            lines = output.split("\n")
            for line in lines:
                if (re.search('XLMIB_RPKT(.*?)$', line.strip())):
                    count_pkt = PortHsdkUtil.ReUtil.getre_output_packets_count(line)
                elif (re.search('XLMIB_R1518(.*?)$', line.strip())):
                    count_1518 = PortHsdkUtil.ReUtil.getre_output_packets_count(line)
        else:
            return False, output

        log_debug("count:%d" % count)
        log_debug("count_pkt:%d" % count_pkt)
        log_debug("count_1518:%d" % count_1518)
        result_str += "count:%d\n" % count
        result_str += "count_pkt:%d\n" % count_pkt
        result_str += "count_1518:%d\n" % count_1518

        if (count_pkt == 0 or count_1518 == 0):
            result_str += "output:%s\n" % output
            log_warning("output:%s" % output)
        if (count == count_pkt and count == count_1518):
            log_debug("check_port_packets rx success")
            return True, result_str

        log_warning("check_port_packets_rx_fail, output:%s" % output)
        return False, result_str

    def cpu_create(self):
        u'''调用cpu_create.cint'''

        cmd = get_sdk_cmd("cint /usr/share/sonic/device/%s/cpu_create.cint" % global_onie_platform)
        ret, output = port_getstatusoutput(cmd)
        if(ret != 0):
            return False, output

        log_debug("cpu_create success")
        return True, output

    def cpu_destroy(self):
        u'''调用cpu_destroy.cint'''

        cmd = get_sdk_cmd("cint /usr/share/sonic/device/%s/cpu_destroy.cint" % global_onie_platform)
        ret, output = port_getstatusoutput(cmd)
        if(ret != 0):
            return False, output

        log_debug("cpu_destroy success")
        return True, output


@singleton
class PortHsdkBrcstTest(PortHsdkTest):
    u'''端口广播'''

    def init_test(self):
        u'''端口广播测试初始化'''

        ret, output = self.clear_port_packets()
        if ret is False:
            log_error("clear_port_packets fail, output:%s" % output)
            return False, "clear_port_packets fail, output:%s" % output

        ret, output = self.port_stp_config(1)
        if ret is False:
            log_error("port_stp_config fail, output:%s" % output)
            return False, "port_stp_config fail, output:%s" % output

        ret, output = self.vlan_config(PORT_TEST_VLAN)
        if ret is False:
            log_error("vlan_config fail, output:%s" % output)
            return False, "vlan_config fail, output:%s" % output

        cmd = get_sdk_cmd("counter on")
        ret, output = port_getstatusoutput(cmd)

        log_debug("init_test success")
        return True, "init_test success"

    def start_test(self, **kwargs):
        u'''端口广播测试开始'''

        port = kwargs["port"]
        count = kwargs["count"]
        size = kwargs.get("size", PACKETS_SIZE)
        dst_mac = kwargs.get("dst_mac", PACKETS_DST_MAC)

        log_debug("start_test")
        return self.start_send_port_packets(port, count, size, dst_mac)

    def check_test(self, **kwargs):
        u'''端口广播测试结果获取'''

        port = kwargs["port"]

        log_debug("check_test")
        return self.get_port_fcs_status(port)

    def del_test(self):
        u'''端口广播测试环境恢复'''

        log_debug("del_test")
        ret, output = self.vlan_config_clear()
        if ret is False:
            log_error("vlan_config_clear fail, output:%s" % output)
            return False, output

        ret, output = self.stop_send_port_packets()
        if ret is False:
            log_error("stop_send_port_packets fail, output:%s" % output)
            return False, output

        ret, output = self.port_stp_config(0)
        if ret is False:
            log_error("port_stp_config fail, output:%s" % output)
            return False, output

        return True, "del_test success"

    def get_port_fcs_status(self, port):
        u'''检查端口广播测试结果'''

        tfcs = 0
        rfcs = 0
        result_str = ""
        # 查看报文收发统计数据
        bcm_port = self.device_port_list[port - 1].bcm_port
        cmd = get_sdk_cmd("counter on")
        ret, output = port_getstatusoutput(cmd)
        cmd = get_sdk_cmd("show c %s" % bcm_port)
        ret, output = port_getstatusoutput(cmd)
        if ret == 0:
            lines = output.split("\n")
            for line in lines:
                if (re.search('XLMIB_TFCS(.*?)$', line.strip())):
                    tfcs = PortHsdkUtil.ReUtil.getre_output_packets_count(line)
                    log_warning("tfcs: %d" % tfcs)
                elif (re.search('XLMIB_RFCS(.*?)$', line.strip())):
                    rfcs = PortHsdkUtil.ReUtil.getre_output_packets_count(line)
                    log_warning("rfcs: %d" % rfcs)

            result_str += "tfcs:%d\n" % tfcs
            result_str += "rfcs:%d\n" % rfcs

            if (tfcs == 0 and rfcs == 0):
                ret, output = self.get_port_fcs_status_f(bcm_port, lines)
                if ret is True:
                    return True, result_str
                else:
                    result_str += output
            return False, result_str
        else:
            return False, output

    def stop_send_port_packets(self):
        u'''端口广播测试停止发包'''

        # 对xe，ce进行操作，设置en=0/1 -> 修改成 all
        # enable = 1 up down
        # enable = 0 !ena
        cmd = get_sdk_cmd("port all en=0")
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, output
        time.sleep(5)

        cmd = get_sdk_cmd("port all en=1")
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, output

        ret, output = self.set_all_mgmt_enable(0)
        if ret is False:
            log_error("stop_send_port_packets fail, output:%s" % output)
            return False, "stop_send_port_packets fail, output:%s" % output

        time.sleep(5)

        log_debug("stop_send_port_packets success")
        return True, "stop_send_port_packets success"

    def get_port_fcs_status_f(self, bcm_port, lines):
        u'''检查端口广播测试结果,检测端口是否有收发包'''

        tpkt = 0
        rpkt = 0
        # 查看报文收发统计数据
        for line in lines:
            if (re.search('XLMIB_TPKT(.*?)$', line.strip())):
                tpkt = PortHsdkUtil.ReUtil.getre_output_packets_count(line)
                log_debug("%s tpkt: %d" % (bcm_port, tpkt))

            elif (re.search('XLMIB_RPKT(.*?)$', line.strip())):
                rpkt = PortHsdkUtil.ReUtil.getre_output_packets_count(line)
                log_debug("%s rpkt: %d" % (bcm_port, rpkt))

        if tpkt > 0 and rpkt > 0:
            log_debug("%s get_port_fcs_status_f success" % bcm_port)
            return True, "%s get_port_fcs_status_f success" % bcm_port
        else:
            log_error("%s get_port_fcs_status_f fail, tpkt:%d rpkt:%d" % (bcm_port, rpkt, tpkt))
            return False, "%s get_port_fcs_status_f fail, tpkt:%d rpkt:%d" % (bcm_port, rpkt, tpkt)


class PortHsdkPrbsTest(PortHsdkTest):
    u'''端口PRBS父类'''

    def init_test(self):
        u'''待继承'''

        return None

    def start_test(self, **kwargs):
        u'''待继承'''

        return None

    def check_test(self, **kwargs):
        u'''待继承'''

        return None

    def del_test(self):
        u'''待继承'''

        return None


@singleton
class PortHsdkPrbsExtPhyTest(PortHsdkPrbsTest):
    u'''ExtPhy prbs'''

    def init_test(self):
        u'''端口ExtPhy prbs测试初始化'''

        log_debug("init_test")
        return self.clear_port_prbs()

    def start_test(self, **kwargs):
        u'''端口ExtPhy prbs测试开始'''

        test_type = kwargs["test_type"]

        log_debug("start_test")
        return self.start_port_prbs(test_type)

    def check_test(self, **kwargs):
        u'''端口ExtPhy prbs测试结果获取'''

        test_type = kwargs["test_type"]
        upports = kwargs["uprt"]
        result_dict = kwargs["r_dict"]

        log_debug("check_test")
        return self.get_port_prbs_ext_result(test_type=test_type,
                                             uprt=upports,
                                             r_dict=result_dict)

    def del_test(self):
        u'''端口ExtPhy prbs测试环境恢复'''

        log_debug("del_test")
        return self.clear_port_prbs()

    def start_port_prbs(self, test_type):
        u'''ExtPhy prbs测试结果获取'''

        if test_type == "prbs_mac":
            return self.start_port_prbs_mac()

        if test_type == "prbs_sys":
            return self.start_port_prbs_sys()

        if test_type == "prbs_line":
            return self.start_port_prbs_line()

        log_warning("start_port_prbs fail, test_type=%s" % str(test_type))
        return False, "start_port_prbs fail, test_type=%s" % str(test_type)

    def start_port_prbs_mac(self):
        u'''开始mac_sys端prbs测试,获取mac端prbs结果'''

        # 配置mac端的PRBS，默认配置为PRBS31
        cmd = get_sdk_cmd("dsh -c 'phy diag %s prbs set p=3'" % self.prbs_port_range)
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, "start_port_prbs_mac fail %s" % output

        # 配置sys端的PRBS，默认配置为PRBS31
        cmd = get_sdk_cmd("dsh -c 'phy control %s setprbs lnside=1 p=5'" % self.prbs_port_range)
        ret, output = port_getstatusoutput(cmd, time_sleep=5)
        if ret != 0:
            return False, "start_port_prbs_mac fail %s" % output

        cmd = get_sdk_cmd("dsh -c 'phy diag %s prbs get'" % self.prbs_port_range)
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, "start_port_prbs_mac fail %s" % output

        cmd = get_sdk_cmd("dsh -c 'phy diag %s prbsstat start interval=%d'" % (self.prbs_port_range, self.prbs_time))
        ret, output = port_getstatusoutput(cmd, time_sleep=(self.prbs_time + PRBS_WAIT_TIME))
        if ret != 0:
            return False, "start_port_prbs_mac fail %s" % output

        return True, "start_port_prbs_mac success"

    def start_port_prbs_sys(self):
        u'''开始mac_sys端prbs测试,获取sys端prbs结果'''

        # 配置mac端的PRBS，默认配置为PRBS31
        cmd = get_sdk_cmd("dsh -c 'phy diag %s prbs set p=3'" % self.prbs_port_range)
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, "start_port_prbs_sys fail %s" % output

        # 配置sys端的PRBS，默认配置为PRBS31
        cmd = get_sdk_cmd("dsh -c 'phy control %s setprbs lnside=1 p=5'" % self.prbs_port_range)
        ret, output = port_getstatusoutput(cmd, time_sleep=5)
        if ret != 0:
            return False, "start_port_prbs_sys fail %s" % output

        # 新封装的获取prbs测试结果的命令里面包含了get, 所以这里不需要get

        return True, "start_port_prbs_sys success"

    def start_port_prbs_line(self):
        u'''开始line端prbs测试,获取line端prbs结果'''

        # 配置line端的PRBS，默认配置为PRBS31
        cmd = get_sdk_cmd("dsh -c 'phy control %s setprbs lnside=0 p=5'" % self.prbs_port_range)
        ret, output = port_getstatusoutput(cmd, time_sleep=5)
        if ret != 0:
            return False, "start_port_prbs_line fail %s" % output

        # 新封装的获取prbs测试结果的命令里面包含了get, 所以这里不需要get

        return True, "start_port_prbs_line success"

    def get_port_prbs_ext_result(self, **kwargs):
        u'''ExtPhy prbs测试结果获取'''
        test_type = kwargs["test_type"]
        upports = kwargs["uprt"]
        result_dict = kwargs["r_dict"]

        if test_type == "prbs_mac":
            return self.get_prbs_mac_result(upports, result_dict)

        if test_type == "prbs_sys":
            return self.get_prbs_sys_result(upports, result_dict)

        if test_type == "prbs_line":
            return self.get_prbs_line_result(upports, result_dict)

        log_warning("get_port_prbs_ext_result fail, test_type=%s" % str(test_type))
        return False, "get_port_prbs_ext_result fail, test_type=%s" % str(test_type)

    def get_prbs_mac_result(self, upports, result_dict):
        u'''获取mac端prbsstat_ber'''
        result_dict["successports"] = []
        result_dict["errorports"] = []

        cmd = get_sdk_cmd("dsh -c 'phy diag %s prbsstat ber'" % self.prbs_port_range)
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            other_info = result_dict.get("other_info", "")
            result_dict["other_info"] = other_info + output
            return False, result_dict

        lines = output.split("\n")
        for port in upports:
            prbs_ber_flag = 0
            prbs_ber_test_fail = 0
            output_content = ""
            lport = self.device_port_list[port - 1].lport
            unit_port = self.device_port_list[port - 1].unit_port
            bcm_port = self.device_port_list[port - 1].bcm_port
            self.standard_ber_val = self.device_port_list[port - 1].prbs_ber
            output_content_port_info = "port:%-3d %s(%d)" % (lport, bcm_port, unit_port)
            for line in lines:
                if (re.search('.*].*e', line.strip())):
                    line_unit_port = int(line.split('[')[0])
                    if unit_port == line_unit_port:
                        prbs_ber_flag = 1
                        lane_num = int((line.split(']')[0]).split('[')[1])
                        prbs_ber = line.split(' ')[-1]
                        if (float(prbs_ber) > float(self.standard_ber_val)):
                            prbs_ber_test_fail = 1
                            output_content = output_content + \
                                "%-20s Lane[%d] prbs_ber:%s > %s, test fail\n" % (
                                    output_content_port_info, lane_num, prbs_ber, self.standard_ber_val)
                            prbs_info_gather_fun(
                                "%-20s Lane[%d] prbs_ber:%s > %s, test fail" %
                                (output_content_port_info, lane_num, prbs_ber, self.standard_ber_val))
                            log_error("%-20s lane:%d, prbs_ber:%s > %s, test fail" %
                                      (output_content_port_info, lane_num, prbs_ber, self.standard_ber_val))
                        else:
                            prbs_info_gather_fun(
                                "%-20s Lane[%d] prbs_ber:%s <= %s, test success" %
                                (output_content_port_info, lane_num, prbs_ber, self.standard_ber_val))
                            log_debug(
                                "%-20s lane:%d, prbs_ber:%s <= %s, test success" %
                                (output_content_port_info, lane_num, prbs_ber, self.standard_ber_val))
                elif (re.search('Nolock', line.strip()) or re.search('LossOfLock', line.strip())):
                    line_unit_port = int(line.split('[')[0])
                    if unit_port == line_unit_port:
                        prbs_ber_flag = 1
                        prbs_ber_test_fail = 1
                        lane_num = int((line.split(']')[0]).split('[')[1])
                        lock_info = line.split(' ')[-1]

                        prbs_info_gather_fun(
                            "%-20s Lane[%d] %s, test fail" %
                            (output_content_port_info, lane_num, lock_info))
                        output_content = output_content + \
                            "%-20s Lane[%d] %s, test fail\n" % (output_content_port_info, lane_num, lock_info)
                        log_error("%-20s lane:%d, %s, test fail" % (output_content_port_info, lane_num, lock_info))
            if prbs_ber_flag == 1 and prbs_ber_test_fail == 0:
                result_dict["successports"].append(port)
            elif prbs_ber_flag == 1 and prbs_ber_test_fail == 1:
                result_dict["errorports"].append(port)
                result_dict["port_info_dict"][port]["log"] = output_content
            else:
                result_dict["errorports"].append(port)
                prbs_info_gather_fun("%-20s get prbs_ber fail, output:\n%s" % (output_content_port_info, output))
                result_dict["port_info_dict"][port]["log"] = "%-20s get prbs_ber fail, output:%s" % (
                    output_content_port_info, output)
                log_error("%-20s get prbs_ber fail, output:%s" % (output_content_port_info, output))
            prbs_info_gather_fun("")

        if len(result_dict["errorports"]) > 0:
            return False, result_dict
        return True, result_dict

    def get_prbs_sys_result(self, upports, result_dict):
        u'''获取sys端prbsstat_ber'''
        result_dict["successports"] = []
        result_dict["errorports"] = []

        # 新封装的获取prbs测试结果的命令里面包含了等待时间，无需额外等待
        cmd = get_sdk_cmd("dsh -c 'phy control %s calprbs lnside=1 time=%d'" %
                          (self.prbs_port_range, self.prbs_time), time_out=300, grep="] Ber")
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            other_info = result_dict.get("other_info", "")
            result_dict["other_info"] = other_info + output
            return False, result_dict

        lines = output.split("\n")
        for port in upports:
            prbs_ber_flag = 0
            prbs_ber_test_fail = 0
            output_content = ""
            lport = self.device_port_list[port - 1].lport
            unit_port = self.device_port_list[port - 1].unit_port
            bcm_port = self.device_port_list[port - 1].bcm_port
            self.standard_ber_val = self.device_port_list[port - 1].prbs_ber
            output_content_port_info = "port:%-3d %s(%d)" % (lport, bcm_port, unit_port)
            for line in lines:
                if (re.search('.*] Ber', line.strip())):
                    line_unit_port = int((line.split('Lane')[0]).split('Port')[1])
                    if unit_port == line_unit_port:
                        prbs_ber_flag = 1
                        lane_num = int((line.split(']')[0]).split('[')[1])
                        prbs_ber = line.split('Ber')[1]
                        if (float(prbs_ber) > float(self.standard_ber_val)):
                            prbs_ber_test_fail = 1
                            output_content = output_content + \
                                "%-20s Lane[%d] prbs_ber:%s > %s, test fail\n" % (
                                    output_content_port_info, lane_num, prbs_ber, self.standard_ber_val)
                            prbs_info_gather_fun(
                                "%-20s Lane[%d] prbs_ber:%s > %s, test fail" %
                                (output_content_port_info, lane_num, prbs_ber, self.standard_ber_val))
                            log_error("%-20s lane:%d, prbs_ber:%s > %s, test fail" %
                                      (output_content_port_info, lane_num, prbs_ber, self.standard_ber_val))
                        else:
                            prbs_info_gather_fun(
                                "%-20s Lane[%d] prbs_ber:%s <= %s, test success" %
                                (output_content_port_info, lane_num, prbs_ber, self.standard_ber_val))
                            log_debug(
                                "%-20s lane:%d, prbs_ber:%s <= %s, test success" %
                                (output_content_port_info, lane_num, prbs_ber, self.standard_ber_val))
                elif (re.search('Nolock', line.strip()) or re.search('LossOfLock', line.strip())):
                    line_unit_port = int((line.split('Lane')[0]).split('Port')[1])
                    if unit_port == line_unit_port:
                        prbs_ber_flag = 1
                        prbs_ber_test_fail = 1
                        lane_num = int((line.split(']')[0]).split('[')[1])
                        lock_info = line.split(']')[1]

                        prbs_info_gather_fun(
                            "%-20s Lane[%d] %s, test fail" %
                            (output_content_port_info, lane_num, lock_info))
                        output_content = output_content + \
                            "%-20s Lane[%d] %s, test fail\n" % (output_content_port_info, lane_num, lock_info)
                        log_error("%-20s lane:%d, %s, test fail" % (output_content_port_info, lane_num, lock_info))
            if prbs_ber_flag == 1 and prbs_ber_test_fail == 0:
                result_dict["successports"].append(port)
            elif prbs_ber_flag == 1 and prbs_ber_test_fail == 1:
                result_dict["errorports"].append(port)
                result_dict["port_info_dict"][port]["log"] = output_content
            else:
                result_dict["errorports"].append(port)
                prbs_info_gather_fun("%-20s get prbs_ber fail, output:\n%s" % (output_content_port_info, output))
                result_dict["port_info_dict"][port]["log"] = "%-20s get prbs_ber fail, output:%s" % (
                    output_content_port_info, output)
                log_error("%-20s get prbs_ber fail, output:%s" % (output_content_port_info, output))
            prbs_info_gather_fun("")

        if len(result_dict["errorports"]) > 0:
            return False, result_dict
        return True, result_dict

    def get_prbs_line_result(self, upports, result_dict):
        u'''获取line端prbsstat_ber'''
        result_dict["successports"] = []
        result_dict["errorports"] = []

        # 新封装的获取prbs测试结果的命令里面包含了等待，无需额外等待
        cmd = get_sdk_cmd("dsh -c 'phy control %s calprbs lnside=0 time=%d'" %
                          (self.prbs_port_range, self.prbs_time), time_out=300, grep="] Ber")
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            other_info = result_dict.get("other_info", "")
            result_dict["other_info"] = other_info + output
            return False, result_dict

        lines = output.split("\n")
        for port in upports:
            prbs_ber_flag = 0
            prbs_ber_test_fail = 0
            output_content = ""
            lport = self.device_port_list[port - 1].lport
            unit_port = self.device_port_list[port - 1].unit_port
            bcm_port = self.device_port_list[port - 1].bcm_port
            self.standard_ber_val = self.device_port_list[port - 1].prbs_ber
            output_content_port_info = "port:%-3d %s(%d)" % (lport, bcm_port, unit_port)
            for line in lines:
                if (re.search('.*] Ber', line.strip())):
                    line_unit_port = int((line.split('Lane')[0]).split('Port')[1])
                    if unit_port == line_unit_port:
                        prbs_ber_flag = 1
                        lane_num = int((line.split(']')[0]).split('[')[1])
                        prbs_ber = line.split('Ber')[1]
                        if (float(prbs_ber) > float(self.standard_ber_val)):
                            prbs_ber_test_fail = 1
                            output_content = output_content + \
                                "%-20s Lane[%d] prbs_ber:%s > %s, test fail\n" % (
                                    output_content_port_info, lane_num, prbs_ber, self.standard_ber_val)
                            prbs_info_gather_fun(
                                "%-20s Lane[%d] prbs_ber:%s > %s, test fail" %
                                (output_content_port_info, lane_num, prbs_ber, self.standard_ber_val))
                            log_error("%-20s lane:%d, prbs_ber:%s > %s, test fail" %
                                      (output_content_port_info, lane_num, prbs_ber, self.standard_ber_val))
                        else:
                            prbs_info_gather_fun(
                                "%-20s Lane[%d] prbs_ber:%s <= %s, test success" %
                                (output_content_port_info, lane_num, prbs_ber, self.standard_ber_val))
                            log_debug(
                                "%-20s lane:%d, prbs_ber:%s <= %s, test success" %
                                (output_content_port_info, lane_num, prbs_ber, self.standard_ber_val))
                elif (re.search('Nolock', line.strip()) or re.search('LossOfLock', line.strip())):
                    prbs_ber_flag = 1
                    prbs_ber_test_fail = 1
                    lane_num = int((line.split(']')[0]).split('[')[1])
                    lock_info = line.split(']')[1]

                    prbs_info_gather_fun(
                        "%-20s Lane[%d] %s, test fail" %
                        (output_content_port_info, lane_num, lock_info))
                    output_content = output_content + \
                        "%-20s Lane[%d] %s, test fail\n" % (output_content_port_info, lane_num, lock_info)
                    log_error("%-20s lane:%d, %s, test fail" % (output_content_port_info, lane_num, lock_info))
            if prbs_ber_flag == 1 and prbs_ber_test_fail == 0:
                result_dict["successports"].append(port)
            elif prbs_ber_flag == 1 and prbs_ber_test_fail == 1:
                result_dict["errorports"].append(port)
                result_dict["port_info_dict"][port]["log"] = output_content
            else:
                result_dict["errorports"].append(port)
                prbs_info_gather_fun("%-20s get prbs_ber fail, output:\n%s" % (output_content_port_info, output))
                result_dict["port_info_dict"][port]["log"] = "%-20s get prbs_ber fail, output:%s" % (
                    output_content_port_info, output)
                log_error("%-20s get prbs_ber fail, output:%s" % (output_content_port_info, output))
            prbs_info_gather_fun("")

        if len(result_dict["errorports"]) > 0:
            return False, result_dict
        return True, result_dict

    def clear_port_prbs(self):
        u'''clear_port_prbs'''

        cmd = get_sdk_cmd("dsh -c 'phy diag %s prbs clear'" % (self.prbs_port_range))
        ret, output = port_getstatusoutput(cmd, time_sleep=3)
        if ret is False or "fail" in output:
            log_error("mac prbs clear fail, output:%s" % output)
            return False, "mac prbs clear fail, output:%s" % output

        cmd = get_sdk_cmd("dsh -c 'phy control %s clearprbs lnside=1'" % (self.prbs_port_range))
        ret, output = port_getstatusoutput(cmd, time_sleep=3)
        if ret is False or "fail" in output:
            log_error("sys prbs clear fail, output:%s" % output)
            return False, "sys prbs clear fail, output:%s" % output

        cmd = get_sdk_cmd("dsh -c 'phy control %s clearprbs lnside=0'" % (self.prbs_port_range))
        ret, output = port_getstatusoutput(cmd, time_sleep=3)
        if ret is False or "fail" in output:
            log_error("line prbs clear fail, output:%s" % output)
            return False, "line prbs clear fail, output:%s" % output

        log_debug("clear_port_prbs success")
        return True, "clear_port_prbs success"


@singleton
class PortHsdkPrbsIntPhyTest(PortHsdkPrbsTest):
    u'''IntPhy prbs'''

    def init_test(self):
        u'''端口内部PHY PRBS测试初始化'''

        pass

    def start_test(self, **kwargs):
        u'''端口内部PHY PRBS测试开始'''

        log_debug("start_test")
        return self.set_port_prbs(1)

    def check_test(self, **kwargs):
        u'''端口内部PHY PRBS测试结果获取'''

        port = kwargs["port"]

        log_debug("check_test")
        return self.get_port_prbs_int_result(port)

    def del_test(self):
        u'''端口内部PHY PRBS测试环境恢复'''

        log_debug("del_test")
        return self.reset_port_prbs()

    def set_port_prbs(self, enable):
        u'''设置端口prbs, 并开始测试'''

        if enable == 1:
            cmd = get_sdk_cmd("dsh -c 'phy diag %s prbs set p=3'" % self.prbs_port_range)
            ret, output = port_getstatusoutput(cmd)
            if(ret != 0):
                return False, output
            cmd = get_sdk_cmd("dsh -c 'phy diag %s prbs get'" % self.prbs_port_range)
            ret, output = port_getstatusoutput(cmd)
            if(ret != 0):
                return False, output
            cmd = get_sdk_cmd(
                "dsh -c 'phy diag %s prbsstat start interval=%d'" %
                (self.prbs_port_range, self.prbs_time))
            ret, output = port_getstatusoutput(cmd, time_sleep=(self.prbs_time + PRBS_WAIT_TIME))
            if(ret != 0):
                return False, output
            cmd = get_sdk_cmd("dsh -c 'phy diag %s prbsstat ber'" % self.prbs_port_range)
            ret, output = port_getstatusoutput(cmd, time_sleep=5)
            if(ret != 0):
                return False, output
            return True, output
        else:
            cmd = get_sdk_cmd("dsh -c 'phy diag %s prbs clear'" % self.prbs_port_range)
            ret, output = port_getstatusoutput(cmd)
            if(ret != 0):
                return False, output
            return True, output

    def get_port_prbs_int_result(self, port):
        u'''获取端口PRBS测试结果'''

        prbs_ber_flag = 0
        prbs_ber_test_fail = 0
        output_content = ""
        dsc_info = ""
        lport = self.device_port_list[port - 1].lport
        bcm_port = self.device_port_list[port - 1].bcm_port
        unit_port = self.device_port_list[port - 1].unit_port
        self.standard_ber_val = self.device_port_list[port - 1].prbs_ber
        output_content_port_info = "port:%-3d %s(%d)" % (lport, bcm_port, unit_port)

        cmd = get_sdk_cmd("dsh -c 'phy diag %d prbsstat ber'" % unit_port)
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, output
        log_debug(output)

        lines = output.split("\n")
        for line in lines:
            if (re.search('.*].*e', line.strip())):
                prbs_ber_flag = 1  # 返回内容中包含有prbs_ber信息
                lane_num = int((line.split(']')[0]).split('[')[1])
                prbs_ber = line.split(' ')[-1]
                if (float(prbs_ber) > float(self.standard_ber_val)):
                    prbs_ber_test_fail = 1
                    prbs_info_gather_fun(
                        "%-20s Lane[%d] prbs_ber:%s > %s, test fail" %
                        (output_content_port_info, lane_num, prbs_ber, self.standard_ber_val))
                    output_content = output_content + \
                        "%-20s Lane[%d] prbs_ber:%s > %s, test fail\n" % (
                            output_content_port_info, lane_num, prbs_ber, self.standard_ber_val)
                    log_error("%-20s lane:%d, prbs_ber:%s > %s, test fail" %
                              (output_content_port_info, lane_num, prbs_ber, self.standard_ber_val))
                else:
                    prbs_info_gather_fun(
                        "%-20s Lane[%d] prbs_ber:%s <= %s, test success" %
                        (output_content_port_info, lane_num, prbs_ber, self.standard_ber_val))
                    log_debug("%-20s lane:%d, prbs_ber:%s <= %s, test success" %
                              (output_content_port_info, lane_num, prbs_ber, self.standard_ber_val))
            elif (re.search('Nolock', line.strip()) or re.search('LossOfLock', line.strip())):
                prbs_ber_test_fail = 1
                lane_num = int((line.split(']')[0]).split('[')[1])
                lock_info = line.split(' ')[-1]

                prbs_info_gather_fun("%-20s Lane[%d] %s, test fail" % (output_content_port_info, lane_num, lock_info))
                output_content = output_content + \
                    "%-20s Lane[%d] %s, test fail\n" % (output_content_port_info, lane_num, lock_info)
                log_error("%-20s lane:%d, %s, test fail" % (output_content_port_info, lane_num, lock_info))
        if prbs_ber_flag == 1 and prbs_ber_test_fail == 0:
            prbs_info_gather_fun("")
            return True, output
        elif prbs_ber_flag == 1 and prbs_ber_test_fail == 1:
            prbs_info_gather_fun("")
            dsc_info = self.get_port_int_dsc_info(port)
            output_content = output_content + dsc_info
            log_error(dsc_info)
            return False, output_content
        else:
            prbs_info_gather_fun("%-20s get prbs_ber fail, output:\n%s" % (output_content_port_info, output))
            prbs_info_gather_fun("")
            dsc_info = self.get_port_int_dsc_info(port)
            log_error("%-20s get prbs_ber fail, output:%s" % (output_content_port_info, output))
            log_error(dsc_info)
            return False, "%-20s get prbs_ber fail, output:%s" % (output_content_port_info, output)

    def get_port_int_dsc_info(self, port):
        u'''获取内部phy端口dsc信息'''
        unit_port = self.device_port_list[port - 1].unit_port

        cmd = get_sdk_cmd("dsh -c 'phy diag %d dsc'" % unit_port)
        ret, output = port_getstatusoutput(cmd)
        dsc_info = "\ndsc_info:\n\n" + output + "\n"

        return dsc_info

    def reset_port_prbs(self):
        u'''重置端口prbs'''

        ret, output = self.set_port_prbs(0)
        if ret:
            time.sleep(10)
            log_debug("reset_port_prbs success")
            return True, "reset_port_prbs success"
        else:
            log_error("reset_port_prbs fail, output:%s" % output)
            return False, "reset_port_prbs fail, output:%s" % output


@singleton
class PortHsdkKrTest(PortHsdkTest):
    u'''内部管理口收发包'''

    def init_test(self):
        '''内部管理口测试初始化'''
        log_debug("init_test")
        self.install_pktgen_mode()
        ret, output = self.set_mgmt_antoneg_on()
        if ret is False:
            log_error("set_mgmt_antoneg_on fail, output:%s" % output)
            return False, "set_mgmt_antoneg_on fail, output:%s" % output

        ret, output = self.set_all_mgmt_enable(1)
        if ret is False:
            log_error("set_all_mgmt_enable fail, output:%s" % output)
            return False, "set_all_mgmt_enable fail, output:%s" % output

        ret, output = self.clear_all_mgmt_packets()
        if ret is False:
            log_error("clear_all_mgmt_packets fail, output:%s" % output)
            return False, "clear_all_mgmt_packets fail, output:%s" % output

        cmd = get_sdk_cmd("counter on")
        ret, output = port_getstatusoutput(cmd)

        log_debug("init_test success")
        return True, "init_test success"

    def start_test(self, **kwargs):
        u'''内部管理口测试开始'''

        mgmt_eth = kwargs["mgmt_eth"]
        count = kwargs.get("count", PACKETS_COUNT)
        size = kwargs.get("size", PACKETS_SIZE)
        dst_mac = kwargs.get("dst_mac", PACKETS_DST_MAC)
        vlan = kwargs.get("vlan", KR_VLAN)

        log_debug("start_test")
        return self.kr_start_send_port_packets(mgmt_eth=mgmt_eth, count=count, size=size,
                                               dst_mac=dst_mac, vlan=vlan)

    def check_test(self, **kwargs):
        u'''内部管理口测试结果获取'''

        mgmt_eth = kwargs["mgmt_eth"]
        count = kwargs.get("count", PACKETS_COUNT)

        log_debug("check_test")
        ret, output_cpu = self.check_port_packets(mgmt_eth, count)
        if ret is False:
            return ret, output_cpu

        ret, output_mac = self.check_port_mac_packets(mgmt_eth, count)
        output = output_cpu + output_mac
        return ret, output

    def del_test(self):
        u'''内部管理口测试环境恢复'''

        log_debug("del_test")
        ret, output = self.set_all_mgmt_enable(0)
        if ret is False:
            log_error("set_all_mgmt_enable fail, output:%s" % output)
            return False, "set_all_mgmt_enable fail, output:%s" % output

        ret, output = self.clear_all_mgmt_packets()
        if ret is False:
            log_error("clear_all_mgmt_packets fail, output:%s" % output)
            return False, "clear_all_mgmt_packets fail, output:%s" % output

        return True, "del_test success"

    def kr_start_send_port_packets(self, **kwargs):
        u'''开始发包'''

        mgmt_eth = kwargs["mgmt_eth"]
        count = kwargs.get("count", PACKETS_COUNT)
        size = kwargs.get("size", PACKETS_SIZE)
        dst_mac = kwargs.get("dst_mac", PACKETS_DST_MAC)
        vlan = kwargs.get("vlan", KR_VLAN)

        mgmt_bcmport = self.get_mgmt_bcmport(mgmt_eth)
        if mgmt_bcmport is None:
            return False, "kr_start_send_port_packets fail, get_mgmt_bcmport:%s None" % mgmt_eth

        ret, output = self.kr_vlan_config(vlan, mgmt_bcmport)
        if ret is False:
            return False, "kr_start_send_port_packets fail, output:%s" % output

        ret, output = self.kr_pktgen_config(mgmt_eth=mgmt_eth,
                                            count=count,
                                            size=size,
                                            dst_mac=dst_mac,
                                            vlan=vlan,
                                            mgmt_bcmport=mgmt_bcmport)
        if ret is False:
            return False, "kr_start_send_port_packets fail, output:%s" % output

        ret, output = self.kr_pktgen_start(mgmt_eth, vlan, mgmt_bcmport)
        if ret is False:
            return False, "kr_start_send_port_packets fail, output:%s" % output

        ret, output = self.kr_mac_start(mgmt_eth=mgmt_eth,
                                        count=count,
                                        size=size,
                                        dst_mac=dst_mac,
                                        mgmt_bcmport=mgmt_bcmport)
        if ret is False:
            return False, "kr_mac_start fail, output:%s" % output

        log_debug("start_send_port_packets success")
        return True, "start_send_port_packets success"

    def set_mgmt_antoneg_on(self):
        u'''调用mgmt.cint, 打开内部管理口的自协商'''

        cmd = get_sdk_cmd("cint /usr/share/sonic/device/%s/mgmt.cint" % global_onie_platform)
        ret, output = port_getstatusoutput(cmd)
        if(ret != 0):
            log_error("set_mgmt_antoneg_on fail, output:%s" % output)
            return False, "set_mgmt_antoneg_on fail, output:%s" % output

        log_debug("set_mgmt_antoneg_on success")
        return True, output

    def get_kr_port_status(self, eth):
        u'''获取kr口up/down情况'''

        # 获取bcm_port
        cmd = get_sdk_cmd("ps %s" % self.get_mgmt_bcmport(eth))
        ret, output = port_getstatusoutput(cmd)

        if ret == 0:
            return PortHsdkUtil.ReUtil.getre_port_status(output)
        return False, output

    def get_kr_unit_port_by_bcm(self, eth, bcm_port):
        u'''获取unit_port'''

        unit_port = None
        cmd = get_sdk_cmd("ps %s" % bcm_port)
        ret, output = port_getstatusoutput(cmd)

        lines = output.split("\n")
        if ret == 0:
            for line in lines:
                if (re.search(r'(.*?)\((.*?)$', line.strip())):
                    unit_port = PortHsdkUtil.ReUtil.getre_output_unit_port(line)
            log_debug(
                "port:%s bcm_port:%s unit_port:%s, get_kr_unit_port_by_bcm success" %
                (eth, bcm_port, str(unit_port)))
            return True, unit_port

        log_error("port:%s bcm_port:%s, get_unit_port_by_bcm fail, output:%s" % (eth, bcm_port, output))
        return False, 0

    def check_mgmt_speed_is_10G(self, eth, bcm_port):
        u'''验证内部管理口速率是否是10G'''

        cmd = get_sdk_cmd("ps %s" % bcm_port)
        ret, output = port_getstatusoutput(cmd)
        lines = output.split("\n")
        mgmt_speed = None
        if ret == 0:
            for line in lines:
                if (re.search(r'(.*?)\((.*?)$', line.strip())):
                    mgmt_speed = PortHsdkUtil.ReUtil.getre_output_speed(line)
        if mgmt_speed == "10G":
            log_debug("port:%s bcm_port:%s speed:%s, check_mgmt_speed_is_10G success" % (eth, bcm_port, mgmt_speed))
            return True, "port:%s bcm_port:%s speed:%s, check_mgmt_speed_is_10G success" % (eth, bcm_port, mgmt_speed)
        else:
            log_error(
                "port:%s bcm_port:%s speed:%s, check_mgmt_speed_is_10G fail, output:%s" %
                (eth, bcm_port, mgmt_speed, output))
            return False, "port:%s bcm_port:%s speed:%s, check_mgmt_speed_is_10G fail, output:%s" % (
                eth, bcm_port, mgmt_speed, output)

    def get_mgmt_ifconig_rx_packet(slef, eth, bcm_port):
        u'''验证内部管理口ifconfig的rx_packet'''

        cmd = "ifconfig %s" % eth
        ret, output = port_getstatusoutput(cmd)
        log_debug(output)
        lines = output.split("\n")
        rx_packets = 0
        for line in lines:
            if (re.search('RX packets(.*?)$', line.strip())):
                rx_packets = PortHsdkUtil.ReUtil.getre_output_rx_packets(line)
                log_debug(
                    "port:%s bcm_port:%s rx_packets:%d, get_mgmt_ifconig_rx_packet success" %
                    (eth, bcm_port, rx_packets))
                return rx_packets

        log_error("port:%s bcm_port:%s rx_packets:%d, get_mgmt_ifconig_rx_packet fail" % (eth, bcm_port, rx_packets))
        return rx_packets

    def check_port_packets(self, mgmt_eth, count=PACKETS_COUNT):
        u'''内部管理口测试结果获取'''

        kr_count_pkt = 0
        pktgen_count_pkt = 0
        result_str = ""
        # 获取pktgen发包结果
        cmd = "cat /proc/net/pktgen/%s" % mgmt_eth
        ret, output = port_getstatusoutput(cmd)
        log_debug(output)
        lines = output.split("\n")
        for line in lines:
            if (re.search('Result(.*?)$', line.strip())):
                pktgen_count_pkt = int((line.split("usec,"))[1].split("(")[0])
                log_debug("pktgen_count_pkt:%d" % pktgen_count_pkt)
        if (pktgen_count_pkt != 0):
            result_str += "pktgen_count_pkt:%d\n" % pktgen_count_pkt
        else:
            result_str += (output + "\n")
        # 获取show c结果
        cmd = get_sdk_cmd("counter on")
        ret, output = port_getstatusoutput(cmd)
        cmd = get_sdk_cmd("show c %s" % self.get_mgmt_bcmport(mgmt_eth))
        ret, output = port_getstatusoutput(cmd)
        log_debug(output)
        lines = output.split("\n")
        for line in lines:
            if (re.search('XLMIB_RPOK(.*?)$', line.strip())):
                kr_count_pkt = PortHsdkUtil.ReUtil.getre_output_packets_count(line)
                log_debug("kr_count_pkt:%d" % kr_count_pkt)
                result_str += "kr_count_pkt:%d\n" % kr_count_pkt
                if (pktgen_count_pkt == kr_count_pkt):
                    return True, result_str
                else:
                    result_str += "pktgen_count_pkt != kr_count_pkt\n"
                    return False, result_str
        result_str += "kr_count_pkt:%d\n" % kr_count_pkt
        result_str += "%s, output:\n%s" % (cmd, output)
        return False, result_str

    def check_port_mac_packets(self, mgmt_eth, count=PACKETS_COUNT):
        u'''内部管理口mac侧发包，测试结果获取'''

        old_packet = int(self.ifconig_rx_packet_dict["old_packet"][mgmt_eth])
        new_packet = int(self.ifconig_rx_packet_dict["new_packet"][mgmt_eth])
        ifconig_rx_packet = new_packet - old_packet

        log_debug("ifconig_old_rx_packet:%d" % old_packet)
        log_debug("ifconig_new_rx_packet:%d" % new_packet)
        log_debug("ifconig_rx_packet:%d" % ifconig_rx_packet)
        result_str = "ifconig_old_rx_packet:%d ifconig_new_rx_packet:%d" % (old_packet, new_packet)
        if (ifconig_rx_packet == PACKETS_COUNT):
            return True, result_str
        return False, result_str

    def clear_all_mgmt_packets(self):
        u'''清除内部管理口port_packets'''

        cmd = get_sdk_cmd("clear c %s" % (",".join(self.get_mgmt_bcmport(item)
                                                   for item
                                                   in global_port_config["mgmt_kt_ports"])))
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            log_warning("clear_all_mgmt_packets fail, output:%s" % output)
            return False, "clear_all_mgmt_packets fail, output:%s" % output

        log_debug("clear_all_mgmt_packets success")
        return True, "clear_all_mgmt_packets success"

    @classmethod
    def install_pktgen_mode(cls):
        u'''查询当前系统是否加载了pktgen模块，如果没有则载入pktgen模块'''

        cmd = "lsmod | grep pktgen"
        ret, output = port_getstatusoutput(cmd)
        if not output or ret != 0:
            log_debug("载入pktgen模块")
            cmd = "modprobe pktgen"
            ret, output = port_getstatusoutput(cmd)
        eth_list = sorted(global_port_config["mgmt_kt_ports"].keys())
        for eth in eth_list:
            cmd = "ls /proc/net/pktgen/%s" % eth
            ret, output = port_getstatusoutput(cmd)
            if "cannot" in output:
                cmd = "ifconfig %s up" % eth
                ret, output = port_getstatusoutput(cmd, time_sleep=1)
                cmd = "echo \"add_device %s\" > /proc/net/pktgen/kpktgend_0" % eth
                ret, output = port_getstatusoutput(cmd)
        time.sleep(3)

    @classmethod
    def kr_vlan_config(cls, vlan, mgmt_bcmport):
        u'''内部管理口发包前配置vlan'''

        time.sleep(1)
        cmd = get_sdk_cmd("vlan destroy %d" % vlan)
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, output
        cmd = get_sdk_cmd("vlan create %d PortBitMap=%s UntagBitMap=%s" % (vlan,
                                                                           mgmt_bcmport,
                                                                           mgmt_bcmport))
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, output
        cmd = get_sdk_cmd("pvlan set %s %d" % (mgmt_bcmport, vlan))
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, output

        return True, "kr_vlan_config success"

    @classmethod
    def kr_pktgen_config(cls, **kwargs):
        u'''内部管理口发包前配置pktgen参数'''

        mgmt_eth = kwargs["mgmt_eth"]
        size = kwargs["size"]
        count = kwargs["count"]
        dst_mac = kwargs["dst_mac"]
        vlan = kwargs["vlan"]
        mgmt_bcmport = kwargs["mgmt_bcmport"]

        cmd = "echo \"pkt_size %d\" > /proc/net/pktgen/%s" % (size, mgmt_eth)
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, output
        cmd = "echo \"count %d\" > /proc/net/pktgen/%s" % (count, mgmt_eth)
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, output
        cmd = "echo \"dst_mac %s\" > /proc/net/pktgen/%s" % (dst_mac, mgmt_eth)
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, output
        cmd = "echo \"vlan_id %s\" > /proc/net/pktgen/%s" % (vlan, mgmt_eth)
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, output

        cmd = get_sdk_cmd("clear c %s" % mgmt_bcmport)
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, output

        return True, "kr_pktgen_config success"

    @classmethod
    def kr_pktgen_start(cls, mgmt_eth, vlan, mgmt_bcmport):
        u'''内部管理口使用pktgen开始发包'''

        # 开始pktgen发包，sleep 5s
        cmd = "echo \"start\" > /proc/net/pktgen/pgctrl"
        ret, output = port_getstatusoutput(cmd, time_sleep=5)
        if ret != 0:
            return False, output

        # 停止pktgen发包
        cmd = "echo \"stop\" > /proc/net/pktgen/pgctrl"
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, output

        # 发包完，将对应的内部管理口从vlan中移除
        cmd = get_sdk_cmd("vlan remove %d PortBitMap=%s" % (vlan, mgmt_bcmport))
        ret, output = port_getstatusoutput(cmd)
        if ret != 0:
            return False, output

        return True, "start_send_port_packets_t success"

    def kr_mac_start(self, **kwargs):
        u'''内部管理口mac侧开始发包'''

        mgmt_eth = kwargs["mgmt_eth"]
        size = kwargs["size"]
        count = kwargs["count"]
        dst_mac = kwargs["dst_mac"]
        mgmt_bcmport = kwargs["mgmt_bcmport"]

        # 发包前，获取上一次ifconfig的rx_packet
        self.ifconig_rx_packet_dict["old_packet"].update(
            {mgmt_eth: self.get_mgmt_ifconig_rx_packet(mgmt_eth, mgmt_bcmport)})

        self.sniff_kr_thread(mgmt_eth)

        cmd = get_sdk_cmd("tx %d PortBitMap=%s Length=%d DestMac=%s" % (count, mgmt_bcmport, size, dst_mac))
        ret, output = port_getstatusoutput(cmd, time_sleep=5)
        if ret != 0:
            log_error("kr_mac_start fail, output:%s" % output)
            return False, "kr_mac_start fail, output:%s" % output

        self.ifconig_rx_packet_dict["new_packet"].update(
            {mgmt_eth: self.get_mgmt_ifconig_rx_packet(mgmt_eth, mgmt_bcmport)})

        return True, "kr_mac_start success"

    def sniff_kr_thread(self, mgmt_eth):
        self.kr_thread = threading.Thread(target=self.sniff_kr, args=(mgmt_eth,))
        self.kr_thread.setDaemon(True)
        self.kr_thread.start()
        time.sleep(1)

    def sniff_kr(self, mgmt_eth):
        dpkt = sniff(iface=mgmt_eth, timeout=10)


class PortScene():
    u'''接口类'''

    @staticmethod
    def port_frame_test(port_list=[], redirect=True):
        u'''端口收发帧测试'''

        log_debug("开始端口收发帧测试")
        pft = PortHsdkFrameTest()
        psf = PortScnFn()
        frmnm = PACKETS_COUNT
        port_list = copy.deepcopy(port_list)  # 防止传入为对象时，对传入对象进行操作
        cycle_num = global_port_config["port_frame_test_retrynum"]  # 循环次数
        del_sleep_time = global_port_config["port_frame_del_time"]  # 恢复测试环境等待时间
        psf.sdk_cmd_redirect_judge(redirect)
        log_debug("端口收发帧重试次数为%d次" % cycle_num)

        for c_i in range(cycle_num):
            log_debug("端口收发帧第%d次测试" % (c_i + 1))
            global global_port_log_info
            global_port_log_info = "port_log_info:\n"

            upports = []
            successports = []
            updownerrorports = []
            errorports = []
            result_dict = {}
            ret_t = 0
            try:
                ret_t, result_dict, upports, updownerrorports = psf.get_port_status_f(f_obj=pft, port_list=port_list)
                log_debug("up_port:" + ", ".join(str(index) for index in upports))
                if ret_t < 0 or len(upports) == 0:
                    if (ret_t < 0):
                        other_info = result_dict.get("other_info", "")
                        result_dict["other_info"] = other_info + "get_port_status_f ret_t < 0\n"
                        log_error("get_port_status_f ret_t < 0")
                    else:
                        other_info = result_dict.get("other_info", "")
                        result_dict["other_info"] = other_info + "get_port_status_f len(upports) == 0\n"
                        log_error("get_port_status_f len(upports) == 0")
                else:
                    ret, result = pft.init_test()
                    if ret is False:
                        other_info = result_dict.get("other_info", "")
                        result_dict["other_info"] = other_info + "init_test fail, result:%s\n" % result
                        log_error("init_test fail, result:%s" % result)
                        continue  # 开始整个测试项重试
                    ret_t, result_dict = psf.frame_start_f(f_obj=pft,
                                                           ret_t=ret_t,
                                                           uprt=upports,
                                                           frmnm=frmnm,
                                                           r_dict=result_dict)
                    time.sleep(5)
                    ret_t, result_dict, successports, errorports = psf.frame_check_f(f_obj=pft,
                                                                                     ret_t=ret_t,
                                                                                     uprt=upports,
                                                                                     frmnm=frmnm,
                                                                                     r_dict=result_dict)
            except Exception as except_result:
                msg = traceback.format_exc()
                print("Exception_info:\n%s" % msg)
                ret_t = -999
                continue
            finally:
                ret, result = pft.del_test()
                if ret is False:
                    log_error("del_test fail, result:%s" % result)
                time.sleep(del_sleep_time)
                ret_t, result_dict = psf.compare_start_end_ports(f_obj=pft,
                                                                 ret_t=ret_t,
                                                                 uprt=upports,
                                                                 r_dict=result_dict,
                                                                 port_list=port_list)
            result_dict["successports"] = successports
            result_dict["updownerrorports"] = updownerrorports
            result_dict["errorports"] = errorports
            if len(updownerrorports) > 0:
                ret_t -= 1
            if ret_t < 0:
                continue
            break

        return psf.test_return(ret_t=ret_t, result_dict=result_dict, test_type="frame")

    @staticmethod
    def port_brcst_test(port_list=[], redirect=True):
        u'''端口广播测试'''

        log_debug("开始端口广播测试")
        pbt = PortHsdkBrcstTest()
        psf = PortScnFn()
        psf.sdk_cmd_redirect_judge(redirect)
        port_list = copy.deepcopy(port_list)  # 防止传入为对象时，对传入对象进行操作
        cycle_num = global_port_config["port_brcst_test_retrynum"]  # 循环次数
        del_sleep_time = global_port_config["port_brcst_del_time"]  # 恢复测试环境等待时间
        log_debug("端口广播重试次数为%d次" % cycle_num)

        for c_i in range(cycle_num):
            log_debug("端口广播帧第%d次测试" % (c_i + 1))
            global global_port_log_info
            global_port_log_info = "port_log_info:\n"

            upports = []
            successports = []
            updownerrorports = []
            errorports = []
            result_dict = {}
            ret_t = 0
            try:
                ret_t, result_dict, upports, updownerrorports = psf.get_port_status_f(f_obj=pbt, port_list=port_list)
                log_debug("up_port:" + ", ".join(str(index) for index in upports))
                if ret_t < 0 or len(upports) == 0:
                    if (ret_t < 0):
                        other_info = result_dict.get("other_info", "")
                        result_dict["other_info"] = other_info + "get_port_status_f ret_t < 0\n"
                        log_error("get_port_status_f ret_t < 0")
                    else:
                        other_info = result_dict.get("other_info", "")
                        result_dict["other_info"] = other_info + "get_port_status_f len(upports) == 0\n"
                        log_error("get_port_status_f len(upports) == 0")
                else:
                    ret, result = pbt.init_test()
                    if ret is False:
                        other_info = result_dict.get("other_info", "")
                        result_dict["other_info"] = other_info + "init_test fail, result:%s\n" % result
                        log_error("init_test fail, result:%s" % result)
                        continue
                    # 通过第一个up的端口发广播包
                    port = upports[0]
                    ret, output = pbt.start_test(port=port, count=PACKETS_COUNT)
                    if ret is True:
                        time.sleep(10)  # 端口广播测试等待泛洪时间 10s
                        ret_t, result_dict, successports, errorports = psf.brcst_check_f(f_obj=pbt,
                                                                                         ret_t=ret_t,
                                                                                         uprt=upports,
                                                                                         r_dict=result_dict)
                    else:
                        ret_t -= 1
                        log_error("port %d:sending packet , output:%s" % (port, output))
                        output_info = result_dict["port_info_dict"][port]["output"]
                        result_dict["port_info_dict"][port]["output"] = output_info + \
                            "port %d:sending packet , output:%s" % (port, output)

            except Exception as except_result:
                msg = traceback.format_exc()
                print("Exception_info:\n%s" % msg)
                ret_t = -999
                continue
            finally:
                # 关闭广播，恢复环境
                ret, result = pbt.del_test()
                if ret is False:
                    log_error("del_test fail, result:%s" % result)
                time.sleep(del_sleep_time)
                ret_t, result_dict = psf.compare_start_end_ports(f_obj=pbt,
                                                                 ret_t=ret_t,
                                                                 uprt=upports,
                                                                 r_dict=result_dict,
                                                                 port_list=port_list)
            result_dict["successports"] = successports
            result_dict["updownerrorports"] = updownerrorports
            result_dict["errorports"] = errorports
            if len(updownerrorports) > 0:
                ret_t -= 1
            if ret_t < 0:
                continue
            break

        return psf.test_return(ret_t=ret_t, result_dict=result_dict, test_type="brcst")

    def port_prbs_test(self, port_list=[], test_type="", redirect=True):
        u'''端口PRBS测试'''

        # 初始化生测配置，防止有外部phy设备，第一个测试项为prbs时，生测配置没有初始化，调用了内部phy prbs接口
        ppipt = PortHsdkPrbsIntPhyTest()
        if global_port_config.get("extphy_device", 0) == 1:  # 有外部phy
            log_debug("PortHsdkPrbsExtPhyTest")
            return self.test_port_prbs_extphy(port_list=port_list, test_type=test_type, redirect=redirect)
        # 没有外部phy
        log_debug("PortHsdkPrbsIntPhyTest")
        return self.test_port_prbs_intphy(port_list=port_list, test_type=test_type, redirect=redirect)

    @staticmethod
    def port_kr_test(port_list=[], redirect=True):
        u'''内部管理口收发包测试'''

        log_debug("开始内部管理口收发包测试")
        pkt = PortHsdkKrTest()
        psf = PortScnFn()
        packetcount = PACKETS_COUNT
        port_list = copy.deepcopy(port_list)  # 防止传入为对象时，对传入对象进行操作
        cycle_num = global_port_config["port_kr_test_retrynum"]  # 循环次数
        del_sleep_time = global_port_config["port_kr_del_time"]  # 恢复测试环境等待时间
        psf.sdk_cmd_redirect_judge(redirect)
        log_debug("内部管理口收发包重试次数为%d次" % cycle_num)

        for c_i in range(cycle_num):
            log_debug("内部管理口收发包第%d次测试" % (c_i + 1))
            global global_port_log_info
            global_port_log_info = "port_log_info:\n"

            upports = []
            successports = []
            updownerrorports = []
            errorports = []
            result_dict = {}
            ret_t = 0
            try:
                ret, result = pkt.init_test()
                if ret is False:
                    ret_t = -1
                    other_info = result_dict.get("other_info", "")
                    result_dict["other_info"] = other_info + "init_test fail, result:%s\n" % result
                    log_error("init_test fail, result:%s" % result)
                ret_t, result_dict, upports, updownerrorports = psf.get_port_status_f(
                    f_obj=pkt, kr_test=True, port_list=port_list)
                log_debug("up_port:" + ", ".join(str(index) for index in upports))
                if ret_t < 0 or len(upports) == 0:
                    if (ret_t < 0):
                        other_info = result_dict.get("other_info", "")
                        result_dict["other_info"] = other_info + "get_port_status_f ret_t < 0\n"
                        log_error("get_port_status_f ret_t < 0")
                    else:
                        other_info = result_dict.get("other_info", "")
                        result_dict["other_info"] = other_info + "get_port_status_f len(upports) == 0\n"
                        log_error("get_port_status_f len(upports) == 0")
                else:
                    for eth in upports:
                        log_debug("内部管理口:%s 正在发包" % eth)
                        ret, output = pkt.start_test(mgmt_eth=eth, count=packetcount, vlan=2000)
                        if ret is False:
                            errorports.append(eth)
                            output_info = result_dict["port_info_dict"][eth]["log"]
                            result_dict["port_info_dict"][eth]["log"] = output_info + \
                                "port_kr_test start_test fail, output:%s" % output
                            log_warning("port_kr_test start_test fail, output:%s" % output)
                        else:
                            time.sleep(4)
                            ret, output = pkt.check_test(mgmt_eth=eth, count=packetcount)
                            if ret:
                                successports.append(eth)
                            else:
                                ret_t = -1
                                errorports.append(eth)
                                output_info = result_dict["port_info_dict"][eth]["log"]
                                result_dict["port_info_dict"][eth]["log"] = output_info + \
                                    "port_kr_test check_test fail, output:%s" % output
                                log_error("%s check_test fail, output:%s" % (eth, output))
            except Exception as except_result:
                msg = traceback.format_exc()
                print("Exception_info:\n%s" % msg)
                ret_t = -999
                continue
            finally:
                ret_t, result_dict = psf.compare_start_end_ports(f_obj=pkt,
                                                                 ret_t=ret_t,
                                                                 uprt=upports,
                                                                 r_dict=result_dict,
                                                                 kr_test=True,
                                                                 port_list=port_list)
                ret, result = pkt.del_test()
                if ret is False:
                    log_error("del_test fail, result:%s" % result)
                time.sleep(del_sleep_time)
            result_dict["successports"] = successports
            result_dict["updownerrorports"] = updownerrorports
            result_dict["errorports"] = errorports
            if len(updownerrorports) > 0:
                ret_t -= 1
            if ret_t < 0:
                continue
            break

        return psf.test_return(ret_t=ret_t, result_dict=result_dict, test_type="kr")

    @staticmethod
    def test_port_prbs_extphy(port_list=[], test_type="", redirect=True):
        u'''ExtPhy prbs测试'''

        log_debug("开始ExtPhy prbs测试")
        if (test_type != ""):
            log_debug("test_type: %s" % test_type)
        else:
            log_debug("test_type: prbs_mac、prbs_sys、prbs_line")

        psf = PortScnFn()
        psf.sdk_cmd_redirect_judge(redirect)
        ppept = PortHsdkPrbsExtPhyTest()
        port_list = copy.deepcopy(port_list)  # 防止传入为对象时，对传入对象进行操作
        cycle_num = global_port_config["port_prbs_test_retrynum"]  # 循环次数
        del_sleep_time = global_port_config["port_prbs_del_time"]  # 恢复测试环境等待时间
        log_debug("ExtPhy prbs重试次数为%d次" % cycle_num)

        for c_i in range(cycle_num):
            log_debug("ExtPhy prbs第%d次测试" % (c_i + 1))
            global global_port_log_info
            global_port_log_info = "port_log_info:\n"

            upports = []
            updownerrorports = []
            result_dict = {}
            # 保持指向同一对象
            prbs_mac_result_dict = result_dict
            prbs_sys_result_dict = result_dict
            prbs_line_result_dict = result_dict
            prbs_all_result_dict = {
                "prbs_mac_result_dict": prbs_mac_result_dict,
                "prbs_sys_result_dict": prbs_sys_result_dict,
                "prbs_line_result_dict": prbs_line_result_dict
            }
            ret_t = 0
            try:
                ret_t, result_dict, upports, updownerrorports = psf.get_port_status_f(f_obj=ppept, port_list=port_list)
                result_dict["updownerrorports"] = updownerrorports
                log_debug("up_port:" + ", ".join(str(index) for index in upports))
                if ret_t < 0 or len(upports) == 0:
                    if (ret_t < 0):
                        other_info = result_dict.get("other_info", "")
                        result_dict["other_info"] = other_info + "get_port_status_f ret_t < 0\n"
                        log_error("get_port_status_f ret_t < 0")
                    else:
                        other_info = result_dict.get("other_info", "")
                        result_dict["other_info"] = other_info + "get_port_status_f len(upports) == 0\n"
                        log_error("get_port_status_f len(upports) == 0")
                else:
                    ret_t, prbs_all_result_dict = psf.prbs_mac_sys_line_start_check(f_obj=ppept,
                                                                                    ret_t=ret_t,
                                                                                    uprt=upports,
                                                                                    udeprt=updownerrorports,
                                                                                    test_type=test_type,
                                                                                    r_dict=result_dict)
            except Exception as except_result:
                msg = traceback.format_exc()
                print("Exception_info:\n%s" % msg)
                ret_t = -999
                continue
            finally:
                ret, result = ppept.del_test()
                if ret is False:
                    log_error("del_test fail, result:%s" % result)
                time.sleep(del_sleep_time)
                ret_t, result_dict = psf.compare_start_end_ports(f_obj=ppept,
                                                                 ret_t=ret_t,
                                                                 uprt=upports,
                                                                 r_dict=result_dict,
                                                                 port_list=port_list)
                prbs_all_result_dict = psf.prbs_ext_result_dict_dispose(r_dict=result_dict,
                                                                        test_type=test_type,
                                                                        prbs_all_r_dict=prbs_all_result_dict)
            if len(updownerrorports) > 0:
                ret_t -= 1
            if ret_t < 0:
                continue
            break
        return PortScnFn.test_return(ret_t=ret_t, prbs_all_result_dict=prbs_all_result_dict, test_type=test_type)

    @staticmethod
    def test_port_prbs_intphy(port_list=[], test_type="", redirect=True):
        u'''IntPhy prbs测试'''

        log_debug("开始IntPhy prbs测试")
        ppipt = PortHsdkPrbsIntPhyTest()
        psf = PortScnFn()
        psf.sdk_cmd_redirect_judge(redirect)
        port_list = copy.deepcopy(port_list)  # 防止传入为对象时，对传入对象进行操作
        cycle_num = global_port_config["port_prbs_test_retrynum"]  # 循环次数
        del_sleep_time = global_port_config["port_prbs_del_time"]  # 恢复测试环境等待时间
        log_debug("IntPhy prbs重试次数为%d次" % cycle_num)

        for c_i in range(cycle_num):
            log_debug("IntPhy prbs第%d次测试" % (c_i + 1))
            global global_port_log_info
            global_port_log_info = "port_log_info:\n"
            prbs_info_gather_fun("prbs_mac_test", clear=True)

            upports = []
            successports = []
            updownerrorports = []
            errorports = []
            result_dict = {}
            prbs_all_result_dict = {}
            ret_t = 0
            try:
                ret_t, result_dict, upports, updownerrorports = psf.get_port_status_f(f_obj=ppipt, port_list=port_list)
                log_debug("up_port:" + ", ".join(str(index) for index in upports))
                if ret_t < 0 or len(upports) == 0:
                    if (ret_t < 0):
                        other_info = result_dict.get("other_info", "")
                        result_dict["other_info"] = other_info + "get_port_status_f ret_t < 0\n"
                        log_error("get_port_status_f ret_t < 0")
                    else:
                        other_info = result_dict.get("other_info", "")
                        result_dict["other_info"] = other_info + "get_port_status_f len(upports) == 0\n"
                        log_error("get_port_status_f len(upports) == 0")
                else:
                    ret_t, result_dict = psf.prbs_int_start_f(
                        f_obj=ppipt, ret_t=ret_t, uprt=upports, r_dict=result_dict)
                    ret_t, result_dict, successports, errorports = psf.prbs_int_check_f(f_obj=ppipt,
                                                                                        ret_t=ret_t,
                                                                                        uprt=upports,
                                                                                        r_dict=result_dict)
            except Exception as except_result:
                msg = traceback.format_exc()
                print("Exception_info:\n%s" % msg)
                ret_t = -999
                continue
            finally:
                ret, result = ppipt.del_test()
                if ret is False:
                    log_error("del_test fail, result:%s" % result)
                time.sleep(del_sleep_time)
                ret_t, result_dict = psf.compare_start_end_ports(f_obj=ppipt,
                                                                 ret_t=ret_t,
                                                                 uprt=upports,
                                                                 r_dict=result_dict,
                                                                 port_list=port_list)
            result_dict["successports"] = successports
            result_dict["updownerrorports"] = updownerrorports
            result_dict["errorports"] = errorports
            if len(updownerrorports) > 0:
                ret_t -= 1
            if ret_t < 0:
                continue
            break
        prbs_all_result_dict["prbs_mac_result_dict"] = copy.deepcopy(result_dict)
        prbs_all_result_dict["prbs_mac_result_dict"]["prbs_info"] = global_prbs_info
        prbs_all_result_dict["prbs_sys_result_dict"] = {}
        prbs_all_result_dict["prbs_line_result_dict"] = {}
        prbs_all_result_dict["prbs_mac_result_dict"]["test_type"] = "prbs_mac"
        if ret_t < 0:
            prbs_all_result_dict["prbs_mac_result_dict"]["test_result"] = False
        else:
            prbs_all_result_dict["prbs_mac_result_dict"]["test_result"] = True
        return psf.test_return(ret_t=ret_t, prbs_all_result_dict=prbs_all_result_dict, test_type="prbs_mac")


class PortScnFn():
    u'''PortScene函数'''

    @staticmethod
    def get_port_status_f(**kwargs):
        u'''获取端口状态'''

        ret_t = 0
        upports = []
        updownerrorports = []
        result_dict = {"port_info_dict": {}, "other_info": "", "test_result": False,
                       "updownerrorports": [], "errorports": [], "successports": []}
        f_obj = kwargs["f_obj"]
        kr_test_flag = kwargs.get("kr_test", False)
        port_list = kwargs.get("port_list", [])

        log_debug("开始获取端口状态")
        try:
            if kr_test_flag is False:
                # 传入port_list=[] 或 不传入port_list, 测试全部端口
                # 传入port_list=[7,8,9,10], 测试面板口7, 8, 9, 10
                log_debug("bcm_port数量:%d" % len(f_obj.device_port_list))
                if len(port_list) == 0:
                    for i in range(len(f_obj.device_port_list)):
                        port_list.append(i + 1)

                if isinstance(port_list[0], int):
                    log_debug("port_list %s" % port_list)
                else:
                    other_info = result_dict.get("other_info", "")
                    result_dict["other_info"] = other_info + "not find port in port_list:%s\n" % port_list
                    log_error("not find port in port_list:%s " % port_list)
                    ret_t -= 1
                    port_list = []

                # 针对port_list初始化result_dict
                for port in port_list:
                    result_dict["port_info_dict"][port] = {
                        "port_info": "",
                        "status": "",
                        "log": ""}
                for port in port_list:
                    # 获取port_info，加入result_dict["port_info_dict"][port]["port_info"]
                    bcm_port = f_obj.device_port_list[port - 1].bcm_port
                    unit_port = f_obj.device_port_list[port - 1].unit_port
                    port_info = "port:%-3d %s(%d)" % (port, bcm_port, unit_port)
                    result_dict["port_info_dict"][port]["port_info"] = port_info

                    # 获取端口状态，加入result_dict["port_info_dict"][port]["status"]、加入对应的端口状态列表
                    ret, output = f_obj.get_port_status(port)
                    if ret is True:
                        if output == "up":
                            upports.append(port)
                            result_dict["port_info_dict"][port]["status"] = "up"
                            log_debug("%-18s:up" % port_info)
                        elif output == "down":
                            updownerrorports.append(port)
                            result_dict["port_info_dict"][port]["status"] = "down"
                            log_warning("%-18s:down" % port_info)
                        elif output == "!ena":
                            updownerrorports.append(port)
                            result_dict["port_info_dict"][port]["status"] = "!ena"
                            log_warning("%-18s:!ena" % port_info)
                        else:
                            updownerrorports.append(port)
                            result_dict["port_info_dict"][port]["status"] = "NA"
                            log_warning("%-18s:NA, output:%s" % (port_info, output))
                    else:
                        ret_t -= 1
                        result_dict["port_info_dict"][port]["status"] = "NA"
                        result_dict["port_info_dict"][port]["log"] = "get_port_status abnormal, output:%s\n" % output
                        other_info = result_dict.get("other_info", "")
                        result_dict["other_info"] = other_info + "get_port_status abnormal, output:%s\n" % output
                        log_error("%-18s:get_port_status abnormal, output:%s" % (port_info, output))
                        break
            else:  # kr测试: 获取的是eth口对应的bcm_port
                # 传入port_list=[] 或 不传入port_list, 测试全部内部管理口
                # 传入port_list=['eth1'], 测试内部管理口eth1
                # 内部管理口额外判断:速率是否是10G
                if len(port_list) == 0:
                    eth_list = sorted(global_port_config["mgmt_kt_ports"].keys())
                else:
                    eth_list = sorted(port_list)

                if isinstance(eth_list[0], int):
                    other_info = result_dict.get("other_info", "")
                    result_dict["other_info"] = other_info + "not find ethX in eth_list:%s\n" % eth_list
                    log_error("not find ethX in eth_list:%s " % eth_list)
                    ret_t -= 1
                    eth_list = []
                else:
                    log_debug("eth_list %s" % eth_list)

                # 针对eth_list初始化result_dict
                for eth in eth_list:
                    result_dict["port_info_dict"][eth] = {
                        "port_info": "",
                        "status": "",
                        "log": ""}
                for eth in eth_list:
                    # 获取port_info，加入result_dict["port_info_dict"][eth]["port_info"]
                    bcm_port = f_obj.get_mgmt_bcmport(eth)
                    ret, unit_port = f_obj.get_kr_unit_port_by_bcm(eth, bcm_port)
                    port_info = "port:%s %s(%s)" % (eth, bcm_port, str(unit_port))
                    result_dict["port_info_dict"][eth]["port_info"] = port_info

                    # 获取端口速率，判断是否是10G
                    ret, output = f_obj.check_mgmt_speed_is_10G(eth, bcm_port)
                    if ret is False:
                        ret_t -= 1
                        result_dict["port_info_dict"][eth]["log"] = "%s\n" % output
                        other_info = result_dict.get("other_info", "")
                        result_dict["other_info"] = other_info + "%s\n" % output
                        break
                    # 获取端口状态，加入result_dict["port_info_dict"][eth]["status"]、加入对应的端口状态列表
                    ret, output = f_obj.get_kr_port_status(eth)  # 获取管理口对应的bcm_port端口状态
                    if ret is True:
                        if output == "up":
                            upports.append(eth)
                            result_dict["port_info_dict"][eth]["status"] = "up"
                            log_debug("%-18s:up" % port_info)
                        elif output == "down":
                            updownerrorports.append(eth)
                            result_dict["port_info_dict"][eth]["status"] = "down"
                            log_warning("%-18s:down" % port_info)
                        elif output == "!ena":
                            updownerrorports.append(eth)
                            result_dict["port_info_dict"][eth]["status"] = "!ena"
                            log_warning("%-18s:!ena" % port_info)
                        else:
                            updownerrorports.append(eth)
                            result_dict["port_info_dict"][eth]["status"] = "NA"
                            log_warning("%-18s:NA, output:%s" % (port_info, output))
                    else:
                        ret_t -= 1
                        result_dict["port_info_dict"][eth]["status"] = "NA"
                        result_dict["port_info_dict"][eth]["log"] = "get_port_status abnormal, output:%s\n" % output
                        other_info = result_dict.get("other_info", "")
                        result_dict["other_info"] = other_info + "get_port_status abnormal, output:%s\n" % output
                        log_error("%-18s:get_port_status abnormal" % port_info)
                        break
        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)
            ret_t = -999
            return ret_t, result_dict, upports, updownerrorports
        return ret_t, result_dict, upports, updownerrorports

    @staticmethod
    def compare_start_end_ports(**kwargs):
        u'''对比开始和结束测试项时的端口up情况'''

        f_obj = kwargs["f_obj"]
        ret_t = kwargs["ret_t"]
        upports = kwargs["uprt"]
        kr_test_flag = kwargs.get("kr_test", False)
        port_list = kwargs.get("port_list", [])
        result_dict = kwargs["r_dict"]

        try:
            # 上面的测试都成功的时候，才会继续对比开始和结束测试项时的端口up情况
            if ret_t == 0:
                if kr_test_flag is False:
                    s_ret_t, _, s_upports, _ = PortScnFn.get_port_status_f(f_obj=f_obj, port_list=port_list)
                else:
                    # kr测试时 是获取eth口
                    s_ret_t, _, s_upports, _ = PortScnFn.get_port_status_f(
                        f_obj=f_obj, port_list=port_list, kr_test=kr_test_flag)
                if s_ret_t == 0:
                    if upports != s_upports:
                        ret_t -= 1
                        temp_log = "first_uplist != second_uplist\nfirst_uplist:%s\nsecond_uplist:%s\n" % (
                            upports, s_upports)
                        other_info = result_dict.get("other_info", "")
                        result_dict["other_info"] = other_info + temp_log
                        log_error(temp_log)
                    else:
                        log_debug("两次端口up状态相同")
                else:
                    ret_t -= 1
                    other_info = result_dict.get("other_info", "")
                    result_dict["other_info"] = other_info + "test end:get_port_status abnormal"
                    log_warning("test end:get_port_status abnormal")
        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)
            ret_t = -999
            return ret_t, result_dict
        return ret_t, result_dict

    @staticmethod
    def frame_start_f(**kwargs):
        u'''端口收发帧发包'''

        f_obj = kwargs["f_obj"]
        ret_t = kwargs["ret_t"]
        upports = kwargs["uprt"]
        framenum = kwargs["frmnm"]
        result_dict = kwargs["r_dict"]

        try:
            for port in upports:
                bcm_port = f_obj.device_port_list[port - 1].bcm_port
                unit_port = f_obj.device_port_list[port - 1].unit_port
                port_info = "port:%d %s(%d)" % (port, bcm_port, unit_port)
                log_debug("%-18s:sending packet" % port_info)

                ret, output = f_obj.start_test(port=port, count=framenum, size=1024)
                if ret is False:
                    ret_t -= 1
                    output_info = result_dict["port_info_dict"][port]["log"]
                    result_dict["port_info_dict"][port]["log"] = output_info + \
                        "sending packet fail, output:%s\n" % output
                    other_info = result_dict.get("other_info", "")
                    result_dict["other_info"] = other_info + "sending packet fail, output:%s\n" % output
                    log_warning("%-18s:sending packet fail, output:%s" % (port_info, output))
        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)
            ret_t = -999
            return ret_t, result_dict
        return ret_t, result_dict

    @staticmethod
    def frame_check_f(**kwargs):
        u'''端口收发帧结果检测'''

        successport = []
        errorport = []

        f_obj = kwargs["f_obj"]
        ret_t = kwargs["ret_t"]
        upports = kwargs["uprt"]
        framenum = kwargs["frmnm"]
        result_dict = kwargs["r_dict"]

        try:
            # 针对upports的端口做验证
            for port in upports:
                bcm_port = f_obj.device_port_list[port - 1].bcm_port
                unit_port = f_obj.device_port_list[port - 1].unit_port
                port_info = "port:%d %s(%d)" % (port, bcm_port, unit_port)

                ret, output = f_obj.check_test(port=port, count=framenum, direc="rx")
                if ret is True:
                    successport.append(port)
                    log_debug("%-18s:test success" % port_info)
                else:
                    ret_t -= 1
                    errorport.append(port)
                    output_info = result_dict["port_info_dict"][port]["log"]
                    result_dict["port_info_dict"][port]["log"] = output_info + "frame_check_f fail, output:%s" % output
                    log_warning("%-18s:test fail, output:%s" % (port_info, output))
        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)
            ret_t = -999
            return ret_t, result_dict, successport, errorport
        return ret_t, result_dict, successport, errorport

    @staticmethod
    def brcst_check_f(**kwargs):
        u'''端口广播结果检测'''

        successport = []
        errorport = []

        f_obj = kwargs["f_obj"]
        ret_t = kwargs["ret_t"]
        upports = kwargs["uprt"]
        result_dict = kwargs["r_dict"]

        try:
            for port in upports:
                bcm_port = f_obj.device_port_list[port - 1].bcm_port
                unit_port = f_obj.device_port_list[port - 1].unit_port
                port_info = "port:%d %s(%d)" % (port, bcm_port, unit_port)

                ret, output = f_obj.check_test(port=port)
                if ret is True:
                    successport.append(port)
                    log_debug("%-18s:test success" % port_info)
                else:
                    ret_t -= 1
                    errorport.append(port)
                    output_info = result_dict["port_info_dict"][port]["log"]
                    result_dict["port_info_dict"][port]["log"] = output_info + \
                        "brcst_check_f fail, output:%s\n" % output
                    log_warning("%-18s:test fail, output:%s" % (port_info, output))
        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)
            ret_t = -999
            return ret_t, result_dict, successport, errorport
        return ret_t, result_dict, successport, errorport

    @staticmethod
    def prbs_prepare_test(**kwargs):
        u'''ExtPhy prbs 准备测试环境'''

        f_obj = kwargs["f_obj"]
        upports = kwargs["uprt"]
        try:
            # 因为每次传入的upports可能不同，需要重新获取
            f_obj.get_unit_port_list(upports)
            f_obj.get_prbs_port_range()
            # 测试的是3侧的, 所以每一侧的测试前，需要重新清除一下prbs
            ret, output = f_obj.init_test()
            if ret is False:
                log_warning("prbs_prepare_test fail, output:%s" % output)
                return False, "prbs_prepare_test fail, output:%s\n" % output

        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)
            return False, "Exception_info:\n%s" % msg
        return True, "prbs_prepare_test success"

    @staticmethod
    def prbs_mac_sys_line_start_check(**kwargs):
        u'''ExtPhy prbs mac、sys、line端检测'''

        psf = PortScnFn()

        f_obj = kwargs["f_obj"]
        ret_t = kwargs["ret_t"]
        upports = kwargs["uprt"]
        test_type = kwargs["test_type"]
        result_dict = kwargs["r_dict"]
        prbs_all_result_dict = {
            "prbs_mac_result_dict": {},
            "prbs_sys_result_dict": {},
            "prbs_line_result_dict": {}
        }
        mac_flag = False
        sys_flag = False
        line_flag = False
        all_flag = False
        try:
            if test_type == "prbs_mac":
                mac_flag = True
            elif test_type == "prbs_sys":
                sys_flag = True
            elif test_type == "prbs_line":
                line_flag = True
            else:
                all_flag = True
            # MAC端
            if mac_flag or all_flag:
                prbs_info_gather_fun("prbs_mac_test", clear=True)
                log_debug("====================prbs_mac_test")
                prbs_mac_result_dict = copy.deepcopy(result_dict)
                ret_t, prbs_mac_result_dict = psf.prbs_mac_sys_line_result(f_obj=f_obj,
                                                                           ret_t=ret_t,
                                                                           uprt=upports,
                                                                           r_dict=prbs_mac_result_dict,
                                                                           test_type="prbs_mac")

                prbs_all_result_dict["prbs_mac_result_dict"] = copy.deepcopy(prbs_mac_result_dict)
                prbs_all_result_dict["prbs_mac_result_dict"]["prbs_info"] = global_prbs_info
            # SYS端
            if sys_flag or all_flag:
                prbs_info_gather_fun("prbs_sys_test", clear=True)
                log_debug("====================prbs_sys_test")
                prbs_sys_result_dict = copy.deepcopy(result_dict)
                ret_t, prbs_sys_result_dict = psf.prbs_mac_sys_line_result(f_obj=f_obj,
                                                                           ret_t=ret_t,
                                                                           uprt=upports,
                                                                           r_dict=prbs_sys_result_dict,
                                                                           test_type="prbs_sys")
                prbs_all_result_dict["prbs_sys_result_dict"] = copy.deepcopy(prbs_sys_result_dict)
                prbs_all_result_dict["prbs_sys_result_dict"]["prbs_info"] = global_prbs_info
            # Line端
            if line_flag or all_flag:
                prbs_info_gather_fun("prbs_line_test", clear=True)
                log_debug("====================prbs_line_test")
                prbs_line_result_dict = copy.deepcopy(result_dict)
                ret_t, prbs_line_result_dict = psf.prbs_mac_sys_line_result(f_obj=f_obj,
                                                                            ret_t=ret_t,
                                                                            uprt=upports,
                                                                            r_dict=prbs_line_result_dict,
                                                                            test_type="prbs_line")

                prbs_all_result_dict["prbs_line_result_dict"] = copy.deepcopy(prbs_line_result_dict)
                prbs_all_result_dict["prbs_line_result_dict"]["prbs_info"] = global_prbs_info
        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)
            ret_t = -999
            return ret_t, prbs_all_result_dict
        return ret_t, prbs_all_result_dict

    @staticmethod
    def prbs_mac_sys_line_result(**kwargs):
        u'''ExtPhy prbs mac、sys、line端开始测试, 并检测测试结果'''

        psf = PortScnFn()

        f_obj = kwargs["f_obj"]
        ret_t = kwargs["ret_t"]
        upports = kwargs["uprt"]
        result_dict = kwargs["r_dict"]
        test_type = kwargs["test_type"]

        try:
            ret, output = psf.prbs_prepare_test(f_obj=f_obj, uprt=upports)
            if ret is False:
                ret_t -= 1
                other_info = result_dict.get("other_info", "")
                result_dict["other_info"] = other_info + "output:%s\n" % output
                log_error("prbs_mac_sys_line_result fail, output:%s\n")
                return ret_t, result_dict
            ret, output = f_obj.start_port_prbs(test_type)
            if ret is False:
                ret_t -= 1
                other_info = result_dict.get("other_info", "")
                result_dict["other_info"] = other_info + "output:%s\n" % output
                log_error("prbs_mac_sys_line_result fail, output:%s\n")
                return ret_t, result_dict
            ret_t, result_dict = psf.prbs_mac_sys_line_check(f_obj=f_obj,
                                                             ret_t=ret_t,
                                                             uprt=upports,
                                                             r_dict=result_dict,
                                                             test_type=test_type)
        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)
            ret_t = -999
            return ret_t, result_dict
        return ret_t, result_dict

    @staticmethod
    def prbs_mac_sys_line_check(**kwargs):
        u'''ExtPhy prbs mac、sys、line端检测'''

        f_obj = kwargs["f_obj"]
        ret_t = kwargs["ret_t"]
        upports = kwargs["uprt"]
        result_dict = kwargs["r_dict"]
        test_type = kwargs["test_type"]

        try:
            ret, result_dict = f_obj.check_test(test_type=test_type,
                                                uprt=upports,
                                                r_dict=result_dict)
            result_dict["test_type"] = test_type
            if ret:
                result_dict["test_result"] = True
                log_debug("======================%s_test check success\n" % test_type)
            else:
                ret_t -= 1
                result_dict["test_result"] = False
                log_warning("======================%s_test check fail\n" % test_type)
        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)
            ret_t = -999
            return ret_t, result_dict
        return ret_t, result_dict

    @staticmethod
    def prbs_ext_result_dict_dispose(**kwargs):
        u'''ExtPhy 返回结果字典处理'''

        result_dict = kwargs["r_dict"]
        test_type = kwargs["test_type"]
        prbs_all_result_dict = kwargs["prbs_all_r_dict"]

        try:
            # 防止测试过程中，忽然出现异常，导致字典部分 key没有赋值
            if (test_type == "prbs_mac"):
                if prbs_all_result_dict["prbs_mac_result_dict"] == {}:
                    prbs_all_result_dict["prbs_mac_result_dict"] = copy.deepcopy(result_dict)
                prbs_all_result_dict["prbs_mac_result_dict"]["test_type"] = "prbs_mac"
                result_dict_other_info = result_dict.get("other_info", "")
                prbs_all_result_dict_other_info = prbs_all_result_dict["prbs_mac_result_dict"].get("other_info", "")
                prbs_all_result_dict["prbs_mac_result_dict"]["other_info"] = result_dict_other_info + \
                    prbs_all_result_dict_other_info
            elif (test_type == "prbs_sys"):
                if prbs_all_result_dict["prbs_sys_result_dict"] == {}:
                    prbs_all_result_dict["prbs_sys_result_dict"] = copy.deepcopy(result_dict)
                prbs_all_result_dict["prbs_sys_result_dict"]["test_type"] = "prbs_sys"
                result_dict_other_info = result_dict.get("other_info", "")
                prbs_all_result_dict_other_info = prbs_all_result_dict["prbs_sys_result_dict"].get("other_info", "")
                prbs_all_result_dict["prbs_sys_result_dict"]["other_info"] = result_dict_other_info + \
                    prbs_all_result_dict_other_info
            elif (test_type == "prbs_line"):
                if prbs_all_result_dict["prbs_line_result_dict"] == {}:
                    prbs_all_result_dict["prbs_line_result_dict"] = copy.deepcopy(result_dict)
                prbs_all_result_dict["prbs_line_result_dict"]["test_type"] = "prbs_line"
                result_dict_other_info = result_dict.get("other_info", "")
                prbs_all_result_dict_other_info = prbs_all_result_dict["prbs_line_result_dict"].get("other_info", "")
                prbs_all_result_dict["prbs_line_result_dict"]["other_info"] = result_dict_other_info + \
                    prbs_all_result_dict_other_info
            else:
                if prbs_all_result_dict["prbs_mac_result_dict"] == {}:
                    prbs_all_result_dict["prbs_mac_result_dict"] = copy.deepcopy(result_dict)
                if prbs_all_result_dict["prbs_sys_result_dict"] == {}:
                    prbs_all_result_dict["prbs_sys_result_dict"] = copy.deepcopy(result_dict)
                if prbs_all_result_dict["prbs_line_result_dict"] == {}:
                    prbs_all_result_dict["prbs_line_result_dict"] = copy.deepcopy(result_dict)

                prbs_all_result_dict["prbs_mac_result_dict"]["test_type"] = "prbs_mac"
                prbs_all_result_dict["prbs_sys_result_dict"]["test_type"] = "prbs_sys"
                prbs_all_result_dict["prbs_line_result_dict"]["test_type"] = "prbs_line"

                result_dict_other_info = result_dict.get("other_info", "")
                prbs_all_result_dict_other_info = prbs_all_result_dict["prbs_mac_result_dict"].get("other_info", "")
                prbs_all_result_dict["prbs_mac_result_dict"]["other_info"] = result_dict_other_info + \
                    prbs_all_result_dict_other_info

                result_dict_other_info = result_dict.get("other_info", "")
                prbs_all_result_dict_other_info = prbs_all_result_dict["prbs_sys_result_dict"].get("other_info", "")
                prbs_all_result_dict["prbs_sys_result_dict"]["other_info"] = result_dict_other_info + \
                    prbs_all_result_dict_other_info

                result_dict_other_info = result_dict.get("other_info", "")
                prbs_all_result_dict_other_info = prbs_all_result_dict["prbs_line_result_dict"].get("other_info", "")
                prbs_all_result_dict["prbs_line_result_dict"]["other_info"] = result_dict_other_info + \
                    prbs_all_result_dict_other_info
        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)
            return prbs_all_result_dict
        return prbs_all_result_dict

    @staticmethod
    def prbs_int_start_f(**kwargs):
        u'''IntPhy prbs 测试'''

        f_obj = kwargs["f_obj"]
        ret_t = kwargs["ret_t"]
        upports = kwargs["uprt"]
        result_dict = kwargs["r_dict"]

        try:
            # 因为每次传入的upports可能不同，需要重新获取
            f_obj.get_unit_port_list(upports)
            f_obj.get_prbs_port_range()
            ret, output = f_obj.start_test()
            if ret is False:
                other_info = result_dict.get("other_info", "")
                result_dict["other_info"] = other_info + "prbs_int_start_f fail, output:%s\n" % output
                log_error("prbs_int_start_f fail, output:%s" % output)
        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)
            ret_t = -999
            return ret_t, result_dict
        return ret_t, result_dict

    @staticmethod
    def prbs_int_check_f(**kwargs):
        u'''IntPhy prbs 结果检测'''

        successport = []
        errorport = []

        f_obj = kwargs["f_obj"]
        ret_t = kwargs["ret_t"]
        upports = kwargs["uprt"]
        result_dict = kwargs["r_dict"]

        try:
            for port in upports:
                bcm_port = f_obj.device_port_list[port - 1].bcm_port
                unit_port = f_obj.device_port_list[port - 1].unit_port
                port_info = "port:%d %s(%d)" % (port, bcm_port, unit_port)
                ret, output = f_obj.check_test(port=port)
                if ret is True:
                    successport.append(port)
                    log_debug("%-18s:prbs check success" % port_info)
                else:
                    ret_t -= 1
                    errorport.append(port)
                    output_info = result_dict["port_info_dict"][port]["log"]
                    result_dict["port_info_dict"][port]["log"] = output_info + \
                        "prbs_int_check_f fail\noutput:%s" % output
                    log_error("%-18s:prbs check fail\noutput:%s" % (port_info, output))
        except Exception as except_result:
            msg = traceback.format_exc()
            print("Exception_info:\n%s" % msg)
            ret_t = -999
            return ret_t, result_dict, successport, errorport
        return ret_t, result_dict, successport, errorport

    @staticmethod
    def sdk_cmd_redirect_judge(redirect):
        u'''判断当前是否开启了输入重定向，再按照传入的redirect进行设置'''

        if redirect == False and sdk_cmd_redirect_console == True:
            PortLog.set_sdk_cmd_redirect_console(False)
        elif redirect == True and sdk_cmd_redirect_console == False:
            PortLog.set_sdk_cmd_redirect_console(True)

    @staticmethod
    def test_return(**kwargs):
        u'''测试用例返回结果判断'''
        ret_t = kwargs["ret_t"]
        test_type = kwargs.get("test_type", "")
        result_dict = kwargs.get("result_dict", {})
        prbs_all_result_dict = kwargs.get("prbs_all_result_dict", {})
        return_dict = {}
        errorports_flag = False  # errorports > 0 为True

        if prbs_all_result_dict:
            # 有外部phy的prbs测试返回字典因为有3侧的结果，所以进行单独的判断
            # test_type、test_result的赋值 放在对某一侧的测试结果进行检测的时候
            return_dict = copy.deepcopy(prbs_all_result_dict)
            if "errorports" in return_dict["prbs_mac_result_dict"]:
                if (len(return_dict["prbs_mac_result_dict"]["errorports"])) > 0:
                    errorports_flag = True
            elif "errorports" in return_dict["prbs_sys_result_dict"]:
                if (len(return_dict["prbs_sys_result_dict"]["errorports"])) > 0:
                    errorports_flag = True
            elif "errorports" in return_dict["prbs_line_result_dict"]:
                if (len(return_dict["prbs_line_result_dict"]["errorports"])) > 0:
                    errorports_flag = True
            else:
                errorports_flag = False
        else:
            return_dict = copy.deepcopy(result_dict)
            return_dict["test_type"] = test_type
            if ret_t < 0:
                return_dict["test_result"] = False
            else:
                return_dict["test_result"] = True

            if "errorports" in return_dict:
                if (len(return_dict["errorports"])) > 0:
                    errorports_flag = True
                    return_dict["test_result"] = False
        if ret_t < 0:
            if port_log_info_print_to_console and errorports_flag:
                # 开启了控制宏: 测试失败时将整个测试流程的log打印到控制台 且 errorports > 0
                print(global_port_log_info)
            return return_dict
        return return_dict


class PortLog():
    u'''port log宏控制类'''

    @classmethod
    def get_log_also_print_to_console(cls):
        u'''获取控制宏: 同时将log打印出来'''

        log_debug("get_log_also_print_to_console: %r" % log_also_print_to_console)
        return log_also_print_to_console

    @staticmethod
    def set_log_also_print_to_console(console_val):
        u'''设置控制宏: 同时将log打印出来'''

        global log_also_print_to_console
        log_also_print_to_console = console_val
        log_debug("set_log_also_print_to_console: %r" % log_also_print_to_console)

    @classmethod
    def get_cmd_also_print_to_console(cls):
        u'''获取控制宏: 同时将cmd打印出来'''

        log_debug("get_cmd_also_print_to_console: %r" % cmd_also_print_to_console)
        return cmd_also_print_to_console

    @staticmethod
    def set_cmd_also_print_to_console(console_val):
        u'''设置控制宏: 同时将cmd执行结果打印出来'''

        global cmd_also_print_to_console
        cmd_also_print_to_console = console_val
        log_debug("set_cmd_also_print_to_console: %r" % cmd_also_print_to_console)

    @classmethod
    def get_cmd_output_also_print_to_console(cls):
        u'''获取控制宏: 同时将cmd执行结果打印出来'''

        log_debug("get_cmd_output_also_print_to_console: %r" % cmd_output_also_print_to_console)
        return cmd_output_also_print_to_console

    @staticmethod
    def set_cmd_output_also_print_to_console(console_val):
        u'''设置控制宏: 同时将cmd执行结果打印出来'''

        global cmd_output_also_print_to_console
        cmd_output_also_print_to_console = console_val
        log_debug("set_cmd_output_also_print_to_console: %r" % cmd_output_also_print_to_console)

    @classmethod
    def get_port_log_info_print_to_console(cls):
        u'''获取控制宏: 测试失败时将整个测试流程的log打印到控制台'''

        log_debug("get_port_log_info_print_to_console: %r" % port_log_info_print_to_console)
        return port_log_info_print_to_console

    @staticmethod
    def set_port_log_info_print_to_console(console_val):
        u'''设置控制宏: 测试失败时将整个测试流程的log打印到控制台'''

        global port_log_info_print_to_console
        port_log_info_print_to_console = console_val
        log_debug("set_port_log_info_print_to_console: %r" % port_log_info_print_to_console)

    @classmethod
    def get_sdk_cmd_redirect_console(cls):
        u'''获取控制宏: 开启输入重定向  cmd + < /dev/null'''

        log_debug("get_sdk_cmd_redirect_console: %r" % sdk_cmd_redirect_console)
        return sdk_cmd_redirect_console

    @staticmethod
    def set_sdk_cmd_redirect_console(console_val):
        u'''设置控制宏: 开启输入重定向  cmd + < /dev/null'''

        global sdk_cmd_redirect_console
        sdk_cmd_redirect_console = console_val
        log_debug("set_sdk_cmd_redirect_console: %r" % sdk_cmd_redirect_console)


def hsdk_check():
    if global_port_config.get("flag", False) is False:
        pt = PortHsdkTest()
    if global_port_config.get("hsdk_device", 0) == 1:
        return True
    else:
        return False


@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
def main():
    u'''main'''

    return None


if __name__ == '__main__':
    main()
