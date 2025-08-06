#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import subprocess
import click
import time

from faclib.all import *

RETURN_KEY1 = "code"
RETURN_KEY2 = "msg"


def rj_os_system(cmd):
    status, output = subprocess.getstatusoutput(cmd)
    return status, output


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


def io_rd(reg_addr, len=1):
    '''io读'''
    try:
        regaddr = 0
        if isinstance(reg_addr, int):
            regaddr = reg_addr
        else:
            regaddr = int(reg_addr, 16)
        devfile = "/dev/port"
        fd = os.open(devfile, os.O_RDWR | os.O_CREAT)
        os.lseek(fd, regaddr, os.SEEK_SET)
        str1 = os.read(fd, len)
        return "".join(["%02x" % ord(item) for item in str1])
    except ValueError:
        return None
    except Exception as e:
        print(e)
        return None
    finally:
        os.close(fd)
    return None


def write_sysfs_value(fileLoc, value):
    try:
        with open(fileLoc, 'w') as fd:
            fd.write(value)
    except Exception as error:
        print(("Unable to open " + fileLoc + "file !"))
        return False
    return True


def psu_check():
    RET = {RETURN_KEY1: 0, RETURN_KEY2: ""}
    fanstatusdecode = TESTCASE.get("frustatusdecode", None)
    fanstatus = TESTCASE.get("frustatus", None)

    if fanstatus is None or fanstatusdecode is None:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = 'config no find'
        return RET

    psu_conf = fanstatus.get('psus', None)
    if psu_conf is None:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = 'config error'
        return RET

    psupresent = fanstatusdecode.get('psupresent')
    psu_num = 0
    for item_fan in psu_conf:
        retval = None
        psu_num = psu_num + 1
        gettype = item_fan.get('gettype', None)
        presentbit = item_fan.get('presentbit')
        if gettype is not None and gettype == "io":
            io_addr = item_fan.get('io_addr')
            val = io_rd(io_addr)
            if val is not None:
                retval = val
            else:
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] += "  PSU%d 获取失败\n" % psu_num
        else:
            i2c_addr = item_fan.get('i2c_addr')
            bus = i2c_addr['bus']
            devno = i2c_addr['devno']
            reg_offset = i2c_addr['reg_offset']
            ind, val = rji2cget(bus, devno, reg_offset)
            if ind is True:
                retval = val
            else:
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] += "  PSU%d 获取失败\n" % psu_num
        val_t = (int(retval, 16) & (1 << presentbit)) >> presentbit
        if val_t != psupresent.get('okval'):
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] += "  PSU%d 不在位\n" % psu_num
        else:
            RET[RETURN_KEY2] += "  PSU%d 在位\n" % psu_num

    return RET


def fan_check():
    RET = {RETURN_KEY1: 0, RETURN_KEY2: ""}
    fanstatusdecode = TESTCASE.get("frustatusdecode", None)
    fanstatus = TESTCASE.get("frustatus", None)

    if fanstatus is None or fanstatusdecode is None:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = 'config no find'
        return RET

    fans_conf = fanstatus.get('fans', None)
    if fans_conf is None:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = 'config error'
        return RET

    fanpresent = fanstatusdecode.get('fanpresent')
    fan_num = 0
    for item_fan in fans_conf:
        fan_num = fan_num + 1
        presentbus = item_fan.get('bus')
        presentaddr = item_fan.get('presentloc')
        presentbit = item_fan.get('presentbit')
        loc = item_fan.get('loc')
        ind, val = rji2cget(presentbus, loc, presentaddr)
        if ind is True:
            val_t = (int(val, 16) & (1 << presentbit)) >> presentbit
            if val_t != fanpresent.get('okval'):
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] += ("  风扇%d不在位\n") % fan_num
            else:
                RET[RETURN_KEY2] += ("  风扇%d在位\n") % fan_num
        else:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] += ("  风扇%d获取失败\n") % fan_num
    return RET


def firmware_check():
    is_ok = True
    url = "/dev/ttyS0"
    # 电源在线检测
    RET = psu_check()
    if RET[RETURN_KEY1] < 0:
        write_sysfs_value(url, "psu check fail.\n%s" % RET[RETURN_KEY2])
        is_ok = False

    # 风扇在位检测
    RET = fan_check()
    if RET[RETURN_KEY1] < 0:
        write_sysfs_value(url, "fan check fail.\n%s" % RET[RETURN_KEY2])
        is_ok = False

    if is_ok is False:
        pass


@click.group()
def main():
    '''device operator'''
    pass


@main.command()
def start():
    '''stat devmonitor '''
    if FACTESTMODULE.get("firmware_check", 0) == 1:  # 固件检测
        firmware_check()


@main.command()
def stop():
    pass


if __name__ == '__main__':
    main()
