#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import re
import subprocess
import click
import socket
import struct
import fcntl
import time
import array
import syslog
from faclib.all import *
import json

SYSLOG_IDENTIFIER = "facinit"

RETURN_KEY1 = "code"
RETURN_KEY2 = "msg"

syslog_debug = 0
# ========================== Syslog wrappers ==========================


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


def stop():
    pass


def test_bmc_channel():
    '''测试BMC通路'''
    ip = TESTCASE.get('BMC').get('ip')
    port = TESTCASE.get('BMC').get('port')
    msg = ''
    returncode = False
    import socket
    try:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(10)
        sk.connect((ip, port))
        returncode = True
    except Exception as e:
        msg = '到BMC通路失败,请确认[%s]' % str(e)
        returncode = False
    finally:
        sk.close()
    return returncode, msg


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


def io_wr(reg_addr, reg_data):
    '''io写'''
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
        ret = os.write(fd, chr(regdata))
        return True
    except ValueError as e:
        print(e)
        return False
    except Exception as e:
        print(e)
        return False
    finally:
        os.close(fd)
    return False


def test_bmc_isrunning():
    bmcstatus = TESTCASE.get('bmcstatus', None)
    bmcrunning = bmcstatus.get('bmc_running', None)
    presentbit = bmcrunning.get('presentbit', None)
    gettype = bmcrunning.get('gettype', None)
    bmc_reset = bmcstatus.get('bmc_reset', None)
    reset_gettype = bmc_reset.get('gettype', None)

    for i in range(0, 2):
        if gettype == "io":
            ret = io_rd(bmcrunning.get('io_addr'))
        elif gettype == "i2c":
            log, ret = rji2cget(bmcrunning.get('bus', None), bmcrunning.get('devno', None),
                                bmcrunning.get('addr', None))
        else:
            pass
        val_t = (int(ret, 16) & (1 << presentbit)) >> presentbit
        if val_t == 0:
            click.echo('BMC处于复位状态，正在解复位')
            if reset_gettype == "io":
                ind = io_wr(bmc_reset.get('io_addr'), bmc_reset.get('value'))
            elif reset_gettype == "i2c":
                ind, log = rji2cset(bmc_reset.get('bus', None), bmc_reset.get('devno', None),
                                    bmc_reset.get('addr', None), bmc_reset.get('value', None))
            if ind == True:
                continue
        else:
            click.echo('BMC处于运行状态')
            return True
    raise Exception('BMC解复位失败')


def test_bmc_checkusb0():
    for i in range(0, 60):
        ret, log = test_bmc_channel()
        if ret == True:
            click.echo('BMC通路正常')
            return True
        else:
            click.echo('等待网络通路连接 %d' % (i + 1))
            time.sleep(3)
    raise Exception('bmc fac服务创建失败')


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


def getRealUrl(case, param=None):
    http = TESTCASE.get('BMC').get('requesthttp')
    realurl = ""
    if param is None:
        realurl = "%scase=%s" % (http, case)
    else:
        realurl = "%scase=%s&param=%s" % (http, case, param)
    return realurl


def test_bmc_func(func, param=None, timeout=80):
    if param is None:
        ret = HttpRest().Get(getRealUrl(func), timeout)
    else:
        ret = HttpRest().Get(getRealUrl(func, json.dumps(param)), timeout)
    return ret


def startFanctrol():
    if STARTMODULE['fancontrol'] == 1:
        cmd = "nohup fancontrol.py start >/dev/null 2>&1 &"
        rets = getPid("fancontrol.py")
        if len(rets) == 0:
            os.system(cmd)


def stopFanctrol():
    '''关闭风扇定时服务'''
    if STARTMODULE['fancontrol'] == 1:
        rets = getPid("fancontrol.py")  #
        for ret in rets:
            cmd = "kill " + ret
            os.system(cmd)
        return True


def test_stop_fanctrol():
    stopFanctrol()
    return True, ""


def test_start_fanctrol():
    startFanctrol()
    return True, ""


def test_bmc_i2c_open():
    switch_ctrol = TESTCASE.get("switchcontrol", None)
    if switch_ctrol is None:
        return True, ""
    if switch_ctrol.get('needopen') != 0:
        test_stop_fanctrol()
        time.sleep(1)
        for item in switch_ctrol.get('switchctrl', []):
            if item.get('gettype') == 'io':
                addr = item.get('io_addr')
                val = item.get('switchbmc')
                io_wr(addr, val)
            else:
                # maybe i2c
                pass
    return True, ""


def test_bmc_i2c_close():
    switch_ctrol = TESTCASE.get("switchcontrol", None)
    if switch_ctrol is None:
        return True, ""
    if switch_ctrol.get('needopen') != 0:
        for item in switch_ctrol.get('switchctrl', []):
            if item.get('gettype') == 'io':
                addr = item.get('io_addr')
                val = item.get('switchcpu')
                io_wr(addr, val)
            else:
                pass
    test_start_fanctrol()
    return True, ""


def rj_os_system(cmd):
    status, output = subprocess.getstatusoutput(cmd)
    return status, output


def test_bmc_get_product():
    case = 'bmc_get_productinfo'
    ret = test_bmc_func(case)
    if ret.get('code') == 0:
        click.echo('bmc产品名称为:[%s]' % ret.get('msg', ''))
        return True
    else:
        click.echo("获取失败[%s]" % ret.get('msg', ''))
        return False


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


def test_bmc_check_i2c():
    bmcstatus = TESTCASE.get('bmcstatus', {})
    busendbus = bmcstatus.get('bmc_i2c_endbusname', '')
    param = {}
    param['endbus'] = busendbus
    func = 'check_i2c_bus'
    for i in range(10):
        ret = test_bmc_func(func, param)
        time.sleep(2)
        if ret.get('code') >= 0:
            return True
    return False


def test_bmc_reboot():
    func = 'bmc_reboot'
    ret = test_bmc_func(func, timeout=5)
    print(ret)


def fac_sensors_kill():
    cmdstr = "docker exec pmon  ps -ef | grep sensord | grep -v grep | cut -c 9-15 | xargs docker exec pmon kill -s 9"
    try:
        os.system(cmdstr)
    except BaseException:
        pass


def test_sonic_led_soc():
    productcpldconf = TESTCASE.get('productfromcpld')
    productloca = productcpldconf.get('location')
    bus = productloca.get('bus')
    devno = productloca.get('devno')
    addr = productloca.get('addr')

    cpldchange = productcpldconf.get('cpldchange')
    command = productcpldconf.get('commands')
    checkcommand = productcpldconf.get('checkcommand')
    product_file = productcpldconf.get('product_file')

    click.echo('>>>>led 固件加载')
    ret, ind = rji2cget(bus, devno, addr)
    if ret == True:
        name = cpldchange.get(ind)
        fpath = os.path.dirname(product_file)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        with open(product_file, 'w') as fd:
            fd.write(name)
        click.echo("cpld对应的码流产品:%s" % name)
        ret, ind2 = rj_os_system(checkcommand)
        if ret == 0:
            click.echo('替换固件前:%s' % ind2)
        comm = command.get(name)

        click.echo("执行替换")
        # print comm
        ret, ind3 = rj_os_system(comm)
        if ret == 0:
            click.echo(ind3)
        ret, ind4 = rj_os_system(checkcommand)
        if ret == 0:
            click.echo('替换固件后:%s' % ind4)


def bmcinit():
    ''' check bmc is on'''
    test_bmc_i2c_open()
    try:
        for i in range(1, 4):
            click.echo('>>>>查看BMC是否处于复位状态')
            if test_bmc_isrunning() == False:   # bmc是否在运行
                click.echo("解复位失败，请确认!")
            click.echo('>>>>校验网络通路...')
            test_bmc_checkusb0()
            click.echo('>>>>获取BMC产品名称')
            test_bmc_get_product()
            click.echo('>>>>校验BMC端I2C-BUS是否生成正常')
            if test_bmc_check_i2c() == False:
                click.echo('重启bmc...')
                test_bmc_reboot()
                time.sleep(3)
            else:
                click.echo('facinit完成, 可以执行下一步骤')
                break
    except Exception as e:
        click.echo(str(e))
    finally:
        test_bmc_i2c_close()


def sonicinit(rebootsonic=False):
    if rebootsonic == True:
        click.echo('重启sonic...')
        os.system('reboot -f')
    else:
        pass


def facinit(rebootsonic=False):
    '''
    （码流点灯控制 ?)
    关闭sensor
    判断BMC有没有起来 (是否被拉住)
        解除BMC复位（权限给BMC 关闭风扇）
    判断USB通路是否正常
    获取BMC产品信息
        (最多2次)for 判断BMC是否正常 (I2C有没有创建成功)
            重启BMC
    权限切回sonic， 打开调速
    sonic重启
    '''
    log_info("测试开始")
    check_cpld_version()
    if FACTESTMODULE.get("firmware_check", 0) == 1:  # 固件检测
        firmware_check()
    if FACTESTMODULE.get("ledsoc", 0) == 1:  # sensord后台进程
        test_sonic_led_soc()
    if FACTESTMODULE.get("sensord", 0) == 1:  # sensord后台进程
        fac_sensors_kill()
    if FACTESTMODULE.get("fancontrol_stop", 0) == 1:  # sensord后台进程
        test_stop_fanctrol()
    if FACTESTMODULE.get('bmcinit', 0) == 1:
        bmcinit()
        sonicinit(rebootsonic)

# 不论大小比较字符串


def astrcmp(str1, str2):
    return str1.lower() == str2.lower()


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


def check_cpld_version():
    items = TESTCASE.get("CHECK_CPLD_CARDID", None)
    ind = ""
    val = ""
    ret = ""
    if items is None:
        return
    click.echo("请选择产品：")
    count = 0
    for item in items:
        count += 1
        click.echo("    %d.%s" % (count, item.get("name", "error")))
    click.echo("    q.退出")
    while True:
        choose = getch("    请选择:")
        click.echo(" %s" % choose)
        choose = choose.lstrip().lower()
        if astrcmp(choose, "q"):
            quit()
        elif len(choose) == 0:
            continue
        elif ord("1") <= ord(choose) and ord(choose) <= ord(str(count)):
            chose_number = int(choose)
            name = items[chose_number - 1].get("name", None)
            compare = items[chose_number - 1].get("compare", None)
            gettype = items[chose_number - 1].get("type", "i2c")
            if gettype == "i2c":
                bus = items[chose_number - 1].get("bus", None)
                devno = items[chose_number - 1].get("devno", None)
                addr = items[chose_number - 1].get("addr", None)
                ind, val = rji2cget(bus, devno, addr)
            elif gettype == "io":
                io_addr = items[chose_number - 1].get("io_addr")
                ret = io_rd(io_addr)
                val = ret
            else:
                pass
            if ind is False or ret is None:
                click.echo("    CPLD-板卡id获取失败")
            else:
                if compare == int(val, 16):
                    click.echo("    CPLD-板卡id：0x%x     PASS" % compare)
                    click.echo("    当前产品CPLD为%s" % name)
                    click.echo("    Test Result: Pass")
                    return True
                else:
                    click.echo("    CPLD-板卡id匹配失败")
                    click.echo("    Test Result: fail")
        else:
            click.echo("       输入无效,请重新输入")


@click.group()
def main():
    '''device operator'''
    pass


@main.command()
def init():
    facinit(rebootsonic=True)


@main.command()
def start():
    facinit()


@main.command()
def stop():
    pass


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
    # 电源在线检测
    RET = psu_check()
    if RET[RETURN_KEY1] < 0:
        log_error("psu check fail.\n%s" % RET[RETURN_KEY2])
        click.echo("psu check fail.\n%s" % RET[RETURN_KEY2])
        is_ok = False

    # 风扇在位检测
    RET = fan_check()
    if RET[RETURN_KEY1] < 0:
        log_error("fan check fail.\n%s" % RET[RETURN_KEY2])
        click.echo("fan check fail.\n%s" % RET[RETURN_KEY2])
        is_ok = False

    if is_ok is False:
        pass


def root_check():
    if os.geteuid() != 0:
        click.echo("请在Root权限下执行！")
        sys.exit(1)


if __name__ == '__main__':
    root_check()
    main()
