#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import syslog
import click
from ruijieconfig import *

SFF_POLLING_DEBUG_FILE = "/etc/.sff_polling_debug_flag"
SFF_POLLING_DEBUG = 1
SFF_POLLING_ERROR = 2
debuglevel = 0
SFF_TYPE_UNKNOWN = "UNKNOWN"

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


def sff_polling_debug(s):
    if SFF_POLLING_DEBUG & debuglevel:
        syslog.openlog("SFF_POLLING_DEBUG", syslog.LOG_PID)
        syslog.syslog(syslog.LOG_DEBUG, s)


def sff_polling_error(s):
    if SFF_POLLING_ERROR & debuglevel:
        syslog.openlog("SFF_POLLING_ERROR", syslog.LOG_PID)
        syslog.syslog(syslog.LOG_ERR, s)


def debug_init():
    global debuglevel

    try:
        with open(SFF_POLLING_DEBUG_FILE, "r") as fd:
            value = fd.read()
        debuglevel = int(value)
    except Exception as e:
        debuglevel = 0
    return


def dev_file_write(path, offset, buf):
    # 写设备文件
    # @path: 文件路径
    # @offset: 文件的偏移地址
    # @buf: 写入的数据
    # 返回值：
    #     成功: 返回True, 写入的长度
    #     失败: 返回False, 失败信息
    msg = ""
    value = ""
    fd = -1

    if not os.path.exists(path):
        msg = path + " not found !"
        return False, msg

    sff_polling_debug("dev_file_write path:%s, offset:0x%x, value: %s" % (path, offset, buf))

    try:
        for item in buf:
            value += chr(item)
        fd = os.open(path, os.O_WRONLY)
        os.lseek(fd, offset, os.SEEK_SET)
        ret = os.write(fd, value)
    except Exception as e:
        msg = str(e)
        return False, msg
    finally:
        if fd > 0:
            os.close(fd)

    return True, ret


def dev_file_read(path, offset, len):
    # 读设备文件
    # @path: 文件路径
    # @offset: 文件的偏移地址
    # @len: 读取的长度
    # 返回值：
    #     成功: 返回True, value
    #     失败: 返回False, 失败信息
    value = []
    msg = ""
    ret = ""
    fd = -1

    if not os.path.exists(path):
        msg = path + " not found !"
        return False, msg

    try:
        fd = os.open(path, os.O_RDONLY)
        os.lseek(fd, offset, os.SEEK_SET)
        ret = os.read(fd, len)
        for item in ret:
            value.append(ord(item))
    except Exception as e:
        msg = str(e)
        return False, msg
    finally:
        if fd > 0:
            os.close(fd)

    sff_polling_debug("dev_file_read path:%s, offset:0x%x, len:%d, value: %s" % (path, offset, len, value))
    return True, value


class SffPolling(object):

    def __init__(self, config, index, sffid):
        self.__sff_id = sffid  # 模块id 1 ~ 总的模块个数
        self.__logic_dev_loc = config["logic_dev_loc"]   # polling的逻辑器件路径
        self.__reg_base_addr = config["base_addr"] + (index * config["range"])  # 每个模块polling配置的基址
        self.__sff_type_conf = config["sff_type"]        # 模块类型获取的路径
        self.__pre_sff_type = SFF_TYPE_UNKNOWN           # 模块类型初始化为UNKNOWN

    @property
    def sff_id(self):
        return self.__sff_id

    @property
    def logic_dev_loc(self):
        return self.__logic_dev_loc

    @property
    def reg_base_addr(self):
        return self.__reg_base_addr

    @property
    def sff_type_conf(self):
        return self.__sff_type_conf

    @property
    def pre_sff_type(self):
        return self.__pre_sff_type

    @pre_sff_type.setter
    def pre_sff_type(self, value):
        self.__pre_sff_type = value

    @property
    def sff_type(self):
        # 读sysfs获取模块类型,读失败或模块类型不支持,返回"UNKNOWN"
        sff_type_loc = self.sff_type_conf["loc"] % self.sff_id
        mask = self.sff_type_conf.get("mask", 0xff)

        if not os.path.exists(sff_type_loc):
            sff_polling_error("sff%d type loc: %s not found" % (self.sff_id, sff_type_loc))
            return SFF_TYPE_UNKNOWN
        try:
            with open(sff_type_loc, "r") as fd:
                value = fd.read()
            sff_type_value = int(value, 16) & mask
            sff_type = self.sff_type_conf.get(sff_type_value, SFF_TYPE_UNKNOWN)
            sff_polling_debug(
                "sff%d type loc:%s, value:%s, type:%s" %
                (self.sff_id, sff_type_loc, sff_type_value, sff_type))
            return sff_type
        except Exception as e:
            sff_polling_error("sff%d get type error: %s" % (self.sff_id, str(e)))
        return SFF_TYPE_UNKNOWN

    def set_sff_polling_reg(self, conf_item):
        # 设置每个模块的polling参数
        reg_desc = conf_item["reg_desc"]
        offset = self.reg_base_addr + conf_item["offset"]
        value = conf_item["value"]
        status, msg = dev_file_write(self.logic_dev_loc, offset, value)
        if status is False:
            sff_polling_error("sff%d set %s failed, loc:%s, offset:0x%x, value:%s, err msg:%s"
                              % (self.sff_id, reg_desc, self.logic_dev_loc, offset, value, msg))
            return False
        sff_polling_debug("sff%d set %s success, loc:%s, offset:0x%x, value:%s"
                          % (self.sff_id, reg_desc, self.logic_dev_loc, offset, value))
        return True

    def check_sff_polling_enable(self):
        # 读 polling_cfg_en 判断是否启动polling
        polling_cfg_en = SFF_POLLING_CONF["polling_cfg_en"]
        offset = self.reg_base_addr + polling_cfg_en["offset"]
        mask = polling_cfg_en["mask"]
        polling_cfg_en_val = polling_cfg_en["enable"]
        status, value = dev_file_read(self.logic_dev_loc, offset, 1)
        if status is False:
            sff_polling_error(
                "sff%d get polling_cfg_en status failed, loc:%s, offset:0x%x" %
                (self.sff_id, self.logic_dev_loc, offset))
            return -1
        if (value[0] & mask) == polling_cfg_en_val:
            sff_polling_debug("sff%d already start polling" % self.sff_id)
            return True
        sff_polling_debug("sff%d not start polling" % self.sff_id)
        return False

    def start_sff_polling(self):
        try:
            # 读模块类型
            sff_type = self.sff_type
            if sff_type == SFF_TYPE_UNKNOWN:
                sff_polling_debug("sff%d type unknown do nothing" % self.sff_id)
                return
            # 判断是否启动polling
            polling_en_status = self.check_sff_polling_enable()
            # 模块类型未改变且已经启动polling
            if sff_type == self.pre_sff_type and polling_en_status is True:
                sff_polling_debug(
                    "sff%d type %s not change, and already start polling, do nothing" %
                    (self.sff_id, sff_type))
                return
            # 模块类型改变或未启动polling, 重新配置
            sff_polling_debug(
                "sff%d type change from %s to %s, start to set polling config" %
                (self.sff_id, self.pre_sff_type, sff_type))
            sff_conf_list = SFF_POLLING_CONF[sff_type]
            for item in sff_conf_list:
                status = self.set_sff_polling_reg(item)
                if status is False:
                    sff_polling_error("sff%d start polling failed." % self.sff_id)
                    return
            sff_polling_debug("sff%d start polling success." % self.sff_id)
            self.pre_sff_type = sff_type  # 更新模块类型
        except Exception as e:
            sff_polling_error("sff%d start polling error, msg: %s" % (self.sff_id, str(e)))
        return


def run(interval, sff_list):
    while True:
        debug_init()
        for obj in sff_list:
            obj.start_sff_polling()
        time.sleep(interval)


@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
def main():
    pass


@main.command()
def start():
    '''start sff polling process'''

    sff_list = []
    for item in SFF_POLLING_CONF["device"]:
        index = 0
        start_port = item["start_port"]
        end_port = item["end_port"]
        for sff_id in range(start_port, end_port + 1):
            obj = SffPolling(item, index, sff_id)  # index为每个模块在对应逻辑器件内的偏移, sff_id为模块的id, 1 ~ 总的模块个数
            sff_list.append(obj)
            index += 1

    interval = SFF_POLLING_CONF.get("polling", 3)
    run(interval, sff_list)


if __name__ == '__main__':
    main()
