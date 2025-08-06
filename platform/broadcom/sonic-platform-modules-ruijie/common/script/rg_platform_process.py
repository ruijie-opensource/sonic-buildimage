#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import click
import os
import subprocess
import time
import mmap
from ruijieconfig import *
from ruijieutil import rjpciwr

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


def write_sysfs_value(reg_name, value):
    u'''写sysfs文件'''
    retval = 'ERR'
    mb_reg_file = "/sys/bus/i2c/devices/" + reg_name
    if (not os.path.isfile(mb_reg_file)):
        print(mb_reg_file, 'not found !')
        return False
    try:
        with open(mb_reg_file, 'w') as fd:
            fd.write(value)
    except Exception as error:
        return False
    return True


def getPid(name):
    ret = []
    for dirname in os.listdir('/proc'):
        if dirname == 'curproc':
            continue
        try:
            with open('/proc/{}/cmdline'.format(dirname), mode='r') as fd:
                content = fd.read()
        except Exception:
            continue
        if name in content:
            ret.append(dirname)
    return ret


def startAvscontrol():
    if STARTMODULE.get('avscontrol', 0) == 1:
        cmd = "nohup avscontrol.py start >/dev/null 2>&1 &"
        rets = getPid("avscontrol.py")
        if len(rets) == 0:
            os.system(cmd)


def startAvscontrol_sysfs():
    if STARTMODULE.get('avscontrol_sysfs', 0) == 1:
        cmd = "nohup avscontrol_sysfs.py start >/dev/null 2>&1 &"
        rets = getPid("avscontrol_sysfs.py")
        if len(rets) == 0:
            os.system(cmd)


def startxdpe_avscontrol():
    if STARTMODULE.get('xdpe_avscontrol', 0) == 1:
        cmd = "nohup xdpe_avscontrol.py start >/dev/null 2>&1 &"
        rets = getPid("xdpe_avscontrol.py")
        if len(rets) == 0:
            os.system(cmd)


def startFanctrol():
    if STARTMODULE.get('fancontrol', 0) == 1:
        cmd = "nohup fancontrol.py start >/dev/null 2>&1 &"
        rets = getPid("fancontrol.py")
        if len(rets) == 0:
            os.system(cmd)


def starthal_fanctrl():
    if STARTMODULE.get('hal_fanctrl', 0) == 1:
        cmd = "nohup hal_fanctrl.py start >/dev/null 2>&1 &"
        rets = getPid("hal_fanctrl.py")
        if len(rets) == 0:
            os.system(cmd)


def starthal_ledctrl():
    if STARTMODULE.get('hal_ledctrl', 0) == 1:
        cmd = "nohup hal_ledctrl.py start >/dev/null 2>&1 &"
        rets = getPid("hal_ledctrl.py")
        if len(rets) == 0:
            os.system(cmd)


def startDevmonitor():
    if STARTMODULE.get('dev_monitor', 0) == 1:
        cmd = "nohup dev_monitor.py start >/dev/null 2>&1 &"
        rets = getPid("dev_monitor.py")
        if len(rets) == 0:
            os.system(cmd)


def startSlotmonitor():
    if STARTMODULE.get('slot_monitor', 0) == 1:
        cmd = "nohup slot_monitor.py start >/dev/null 2>&1 &"
        rets = getPid("slot_monitor.py")
        if len(rets) == 0:
            os.system(cmd)


def startIntelligentmonitor():
    if STARTMODULE.get('intelligent_monitor', 0) == 1:
        cmd = "nohup intelligent_monitor.py >/dev/null 2>&1 &"
        rets = getPid("intelligent_monitor.py")
        if len(rets) == 0:
            os.system(cmd)


def startSignalmonitor():
    if STARTMODULE.get('signal_monitor', 0) == 1:
        cmd = "nohup signal_monitor.py start >/dev/null 2>&1 &"
        rets = getPid("signal_monitor.py")
        if len(rets) == 0:
            os.system(cmd)


def startSff_temp_polling():
    if STARTMODULE.get('sff_temp_polling', 0) == 1:
        cmd = "nohup sfp_highest_temperatue.py >/dev/null 2>&1 &"
        rets = getPid("sfp_highest_temperatue.py")
        if len(rets) == 0:
            os.system(cmd)


def startRebootCause():
    if STARTMODULE.get('reboot_cause', 0) == 1:
        cmd = "nohup reboot_cause.py >/dev/null 2>&1 &"
        rets = getPid("reboot_cause.py")
        if len(rets) == 0:
            os.system(cmd)


def startPMON_sys():
    if STARTMODULE.get('rg_pmon_syslog', 0) == 1:
        cmd = "nohup rg_pmon_syslog.py >/dev/null 2>&1 &"
        rets = getPid("rg_pmon_syslog.py")
        if len(rets) == 0:
            os.system(cmd)


def startSff_polling():
    if STARTMODULE.get('sff_polling', 0) == 1:
        cmd = "nohup sff_polling.py start > /dev/null 2>&1 &"
        rets = getPid("sff_polling.py")
        if len(rets) == 0:
            os.system(cmd)


def startGenerate_product_name():
    if STARTMODULE.get('product_name', 0) == 1:
        cmd = "nohup product_name.py > /dev/null 2>&1 &"
        rets = getPid("product_name.py")
        if len(rets) == 0:
            os.system(cmd)


def stopAvscontrol():
    if STARTMODULE.get('avscontrol', 0) == 1:
        rets = getPid("avscontrol.py")
        for ret in rets:
            cmd = "kill " + ret
            os.system(cmd)
        return True


def stopAvscontrol_sysfs():
    if STARTMODULE.get('avscontrol_sysfs', 0) == 1:
        rets = getPid("avscontrol_sysfs.py")
        for ret in rets:
            cmd = "kill " + ret
            os.system(cmd)
        return True


def stopxdpe_avscontrol():
    if STARTMODULE.get('xdpe_avscontrol', 0) == 1:
        rets = getPid("xdpe_avscontrol.py")
        for ret in rets:
            cmd = "kill " + ret
            os.system(cmd)
        return True


def stopFanctrol():
    u'''关闭风扇定时服务'''
    if STARTMODULE.get('fancontrol', 0) == 1:
        rets = getPid("fancontrol.py")  #
        for ret in rets:
            cmd = "kill " + ret
            os.system(cmd)
        return True


def stophal_fanctrl():
    if STARTMODULE.get('hal_fanctrl', 0) == 1:
        rets = getPid("hal_fanctrl.py")
        for ret in rets:
            cmd = "kill " + ret
            os.system(cmd)
        return True


def stophal_ledctrl():
    if STARTMODULE.get('hal_ledctrl', 0) == 1:
        rets = getPid("hal_ledctrl.py")
        for ret in rets:
            cmd = "kill " + ret
            os.system(cmd)
        return True


def stopDevmonitor():
    u'''关闭风扇定时服务'''
    if STARTMODULE.get('dev_monitor', 0) == 1:
        rets = getPid("dev_monitor.py")  #
        for ret in rets:
            cmd = "kill " + ret
            os.system(cmd)
        return True


def stopSlotmonitor():
    u'''关闭slot定时服务'''
    if STARTMODULE.get('slot_monitor', 0) == 1:
        rets = getPid("slot_monitor.py")  #
        for ret in rets:
            cmd = "kill " + ret
            os.system(cmd)
        return True


def stopIntelligentmonitor():
    if STARTMODULE.get('intelligent_monitor', 0) == 1:
        rets = getPid("intelligent_monitor.py")
        for ret in rets:
            cmd = "kill " + ret
            os.system(cmd)
        return True


def stopSignalmonitor():
    if STARTMODULE.get('signal_monitor', 0) == 1:
        rets = getPid("signal_monitor.py")  #
        for ret in rets:
            cmd = "kill " + ret
            os.system(cmd)
        return True


def stopSff_temp_polling():
    if STARTMODULE.get('sff_temp_polling', 0) == 1:
        rets = getPid("sfp_highest_temperatue.py")
        for ret in rets:
            cmd = "kill " + ret
            os.system(cmd)
        return True


def stopPMON_sys():
    if STARTMODULE.get('rg_pmon_syslog', 0) == 1:
        rets = getPid("rg_pmon_syslog.py")
        for ret in rets:
            cmd = "kill " + ret
            os.system(cmd)
        return True


def stopRebootCause():
    if STARTMODULE.get('reboot_cause', 0) == 1:
        rets = getPid("reboot_cause.py")
        for ret in rets:
            cmd = "kill " + ret
            os.system(cmd)
        return True


def stopSff_polling():
    if STARTMODULE.get('sff_polling', 0) == 1:
        rets = getPid("sff_polling.py")
        for ret in rets:
            cmd = "kill " + ret
            os.system(cmd)
        return True


def stopGenerate_product_name():
    if STARTMODULE.get('product_name', 0) == 1:
        rets = getPid("product_name.py")
        for ret in rets:
            cmd = "kill " + ret
            os.system(cmd)
        return True


def otherinit():
    for index in GLOBALINITPARAM:
        write_sysfs_value(index["loc"], index["value"])

    for index in GLOBALINITCOMMAND:
        log_os_system(index)


def otherinit_pre():
    for index in GLOBALINITPARAM_PRE:
        write_sysfs_value(index["loc"], index["value"])

    for index in GLOBALINITCOMMAND_PRE:
        log_os_system(index)


def unload_apps():
    u'''卸载设备和驱动'''
    stopSff_polling()  # 停止模块polling进程
    stopPMON_sys()  # 停止pmon sys进程
    stopSignalmonitor()  # 停止信号监控
    stopIntelligentmonitor()  # 停止智能监控
    stopSlotmonitor()  # 停止子卡热插拔监控服务
    stopDevmonitor()  # 停止可拔插设备驱动监控
    stopAvscontrol()  # 停止MAC调压进程
    stopAvscontrol_sysfs()  # 停止MAC调压进程
    stopxdpe_avscontrol()  # 停止XDPE MAC调压进程
    stophal_ledctrl()  # 停止LED控制服务
    stophal_fanctrl()  # 停止风扇控制服务
    stopFanctrol()  # 停止风扇控制服务
    stopSff_temp_polling()  # 停止光模块温度polling进程
    stopRebootCause()  # 停止reboot cause监控进程
    stopGenerate_product_name() # 停止生成产品名称进程


def MacLedSet(data):
    '''write pci register'''
    pcibus = MAC_LED_RESET.get("pcibus")
    slot = MAC_LED_RESET.get("slot")
    fn = MAC_LED_RESET.get("fn")
    bar = MAC_LED_RESET.get("bar")
    offset = MAC_LED_RESET.get("offset")
    val = MAC_LED_RESET.get(data, None)
    if val is None:
        click.echo("%%RG_PLATFORM_PROCESS-INIT: MacLedSet wrong input")
        return
    rjpciwr(pcibus, slot, fn, bar, offset, val)


def load_apps():
    u'''加载应用'''
    otherinit_pre()
    startGenerate_product_name()  # 打开生成产品名称进程
    startRebootCause()  # 打开reboot cause监控进程
    startSff_temp_polling()  # 打开光模块温度polling进程
    startFanctrol()  # 打开风扇
    starthal_fanctrl()  # 打开hal风扇控制
    starthal_ledctrl()  # 打开hal LED控制
    startxdpe_avscontrol()  # XPDE AVS调压
    startAvscontrol_sysfs()  # avs调压
    startAvscontrol()  # avs调压
    startDevmonitor()  # 可插拔设备驱动监控
    startSlotmonitor()  # 线卡插拔初始化监控
    startIntelligentmonitor()  # 打开智能监控
    startSignalmonitor()  # 打开信号监控
    startPMON_sys()  # 打开pmon sys进程
    startSff_polling()  # 打开模块polling进程
    otherinit()        # 其他初始化 光模块初始化
    if STARTMODULE.get("macledreset", 0) == 1:
        MacLedSet("reset")


@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
def main():
    '''device operator'''
    pass


@main.command()
def start():
    '''load process '''
    load_apps()


@main.command()
def stop():
    '''stop process '''
    unload_apps()


@main.command()
def restart():
    '''restart process'''
    unload_apps()
    load_apps()


if __name__ == '__main__':
    u'''process init operation'''
    main()
