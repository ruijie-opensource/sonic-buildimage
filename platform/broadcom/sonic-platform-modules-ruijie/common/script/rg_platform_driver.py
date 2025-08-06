#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import click
import os
import subprocess
import time
import mmap
from ruijieconfig import *

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


def log_os_system(cmd):
    u'''执行shell命令'''
    status, output = subprocess.getstatusoutput(cmd)
    if status:
        print(output)
    return status, output

def platform_process_file_check():
    # WARM_UPGRADE_STARTED_FLAG is used as warm_upgrade.py process start flag
    if os.path.exists(WARM_UPGRADE_STARTED_FLAG):
        os.remove(WARM_UPGRADE_STARTED_FLAG)

    # WARM_UPG_FLAG is used as port related service judgment flag
    if os.path.exists(WARM_UPG_FLAG):
        os.remove(WARM_UPG_FLAG)


def startCommon_operation():
    platform_process_file_check()

def check_driver():
    u'''判断是否存在rg开头的驱动'''
    status, output = log_os_system("lsmod | grep rg | wc -l")
    # 系统执行错误
    if status:
        return False
    if output.isdigit() and int(output) > 0:
        return True
    else:
        return False


def removeDev(bus, loc):
    cmd = "echo  0x%02x > /sys/bus/i2c/devices/i2c-%d/delete_device" % (loc, bus)
    devpath = "/sys/bus/i2c/devices/%d-%04x" % (bus, loc)
    if os.path.exists(devpath):
        log_os_system(cmd)


def addDev(name, bus, loc):
    if name == "lm75":
        time.sleep(0.1)
    pdevpath = "/sys/bus/i2c/devices/i2c-%d/" % (bus)
    for i in range(1, 100):  # 等待母bus生成，最多等待10s
        if os.path.exists(pdevpath) == True:
            break
        time.sleep(0.1)
        if i % 10 == 0:
            click.echo("%%RG_PLATFORM_DRIVER-INIT: %s not found, wait 0.1 second ! i %d " % (pdevpath, i))

    cmd = "echo  %s 0x%02x > /sys/bus/i2c/devices/i2c-%d/new_device" % (name, loc, bus)
    devpath = "/sys/bus/i2c/devices/%d-%04x" % (bus, loc)
    if os.path.exists(devpath) == False:
        os.system(cmd)


def removeOPTOE(name, startbus, endbus):
    for bus in range(endbus, startbus - 1, -1):
        removeDev(bus, 0x50)


def addOPTOE(name, startbus, endbus):
    for bus in range(startbus, endbus + 1):
        addDev(name, bus, 0x50)


def removeoptoes():
    optoes = GLOBALCONFIG["OPTOE"]
    for index in range(len(optoes) - 1, -1, -1):
        removeOPTOE(optoes[index]["name"], optoes[index]["startbus"], optoes[index]["endbus"])


def addoptoes():
    optoes = GLOBALCONFIG["OPTOE"]
    for index in range(0, len(optoes)):
        addOPTOE(optoes[index]["name"], optoes[index]["startbus"], optoes[index]["endbus"])


def removedevs():
    devs = GLOBALCONFIG["DEVS"]
    for index in range(len(devs) - 1, -1, -1):
        removeDev(devs[index]["bus"], devs[index]["loc"])


def adddevs():
    devs = GLOBALCONFIG["DEVS"]
    for dev in range(0, devs.__len__()):
        addDev(devs[dev]["name"], devs[dev]["bus"], devs[dev]["loc"])


def checksignaldriver(name):
    modisexistcmd = "lsmod | grep -w %s | wc -l" % name
    status, output = log_os_system(modisexistcmd)
    # 系统执行错误
    if status:
        click.echo("%%RG_PLATFORM_DRIVER-INIT: modisexistcmd exec error: %s" % output)
        return False
    if output.isdigit() and int(output) > 0:
        return True
    else:
        return False


def adddriver(name, delay):
    cmd = "modprobe %s" % name
    if delay != 0:
        time.sleep(delay)
    if checksignaldriver(name) != True:
        log_os_system(cmd)


def removedriver(name, delay, removeable=1):
    realname = name.lstrip().split(" ")[0]
    cmd = "rmmod -f %s" % realname
    if delay != 0:
        time.sleep(delay)
    if checksignaldriver(realname) and removeable:
        log_os_system(cmd)


def removedrivers():
    u'''卸载所有驱动'''
    if GLOBALCONFIG is None:
        click.echo("%%RG_PLATFORM_DRIVER-INIT: load global config failed.")
        return
    drivers = GLOBALCONFIG.get("DRIVERLISTS", None)
    if drivers is None:
        click.echo("%%RG_PLATFORM_DRIVER-INIT: load driver list failed.")
        return
    for index in range(len(drivers) - 1, -1, -1):
        delay = 0
        name = ""
        removeable = drivers[index].get("removable", 1)
        if isinstance(drivers[index], dict) and "delay" in drivers[index]:
            name = drivers[index].get("name")
            delay = drivers[index]["delay"]
        else:
            name = drivers[index]
        removedriver(name, delay, removeable)


def adddrivers():
    u'''添加驱动'''
    if GLOBALCONFIG is None:
        click.echo("%%RG_PLATFORM_DRIVER-INIT: load global config failed.")
        return
    drivers = GLOBALCONFIG.get("DRIVERLISTS", None)
    if drivers is None:
        click.echo("%%RG_PLATFORM_DRIVER-INIT: load driver list failed.")
        return
    for index in range(0, len(drivers)):
        delay = 0
        name = ""
        if isinstance(drivers[index], dict) and "delay" in drivers[index]:
            name = drivers[index].get("name")
            delay = drivers[index]["delay"]
        else:
            name = drivers[index]
        adddriver(name, delay)


def blacklist_driver_remove():
    u'''卸载配置文件中位于BLACKLIST_DRIVERS列表中的驱动'''
    if GLOBALCONFIG is None:
        click.echo("%%RG_PLATFORM_DRIVER-INIT: load global config failed.")
        return
    blacklist_drivers = GLOBALCONFIG.get("BLACKLIST_DRIVERS", [])
    for index in range(len(blacklist_drivers)):
        delay = 0
        name = ""
        if isinstance(blacklist_drivers[index], dict) and "delay" in blacklist_drivers[index]:
            name = blacklist_drivers[index].get("name")
            delay = blacklist_drivers[index]["delay"]
        else:
            name = blacklist_drivers[index]
        removedriver(name, delay)


def unload_driver():
    u'''卸载设备和驱动'''
    removeoptoes()    # 卸载OPTOE
    removedevs()    # 卸载其他设备
    removedrivers()  # 卸载驱动


def reload_driver():
    u'''重新加载设备和驱动'''
    removedevs()    # 卸载其他设备
    removedrivers()  # 卸载驱动
    time.sleep(1)
    adddrivers()
    adddevs()


def i2c_check(bus, retrytime=6):
    try:
        i2cpath = "/sys/bus/i2c/devices/" + bus
        while retrytime and not os.path.exists(i2cpath):
            click.echo("%%RG_PLATFORM_DRIVER-HA: i2c bus abnormal, last bus %s is not exist." % i2cpath)
            reload_driver()
            retrytime -= 1
            time.sleep(1)
    except Exception as e:
        click.echo("%%RG_PLATFORM_DRIVER-HA: %s" % str(e))
    return


def load_driver():
    u'''加载设备和驱动'''
    startCommon_operation() # 通用公共操作
    adddrivers()
    adddevs()
    addoptoes()      # 添加OPTOE


@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
def main():
    '''device operator'''
    pass


@main.command()
def start():
    '''load drivers and device '''
    blacklist_driver_remove()
    if check_driver():
        unload_driver()
    load_driver()


@main.command()
def stop():
    '''stop drivers device '''
    unload_driver()


@main.command()
def restart():
    '''restart drivers and device'''
    unload_driver()
    load_driver()


if __name__ == '__main__':
    u'''platform drivers and device init operation'''
    main()
