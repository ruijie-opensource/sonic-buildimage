#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import signal
import time
import threading 
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
from tabulate import tabulate
from faclib.all import *
import pexpect

from rjutil.baseutil import get_machine_info
from rjutil.baseutil import get_platform_info

MAILBOX_DIR = "/sys/bus/i2c/devices/"        # sysfs 顶层目录


def getdeviceplatform():
    x = get_platform_info(get_machine_info())
    if x != None:
        filepath = "/usr/share/sonic/device/" + x
    return filepath

platform = get_platform_info(get_machine_info())                   #platform 获取平台信息       x86_64-ruijie_b6520-64cq-r0
platformpath = getdeviceplatform()                                 #platformpath获取可映射docker目录    /usr/share/sonic/device/x86_64-ruijie_b6520-64cq-r0
grtd_productfile = (platform + "_fwupdate_config").replace("-","_")
configfile_pre   =  "/usr/local/bin/"                              #py放的目录
import sys
sys.path.append(platformpath)
sys.path.append(configfile_pre)

global  module_product
if os.path.exists(configfile_pre + grtd_productfile + ".py"):
    module_product  = __import__(grtd_productfile, globals(), locals(), [], -1)
else:
    print("不存在配置文件，退出")
    exit(-1)


def get_var(name):
    global  module_product
    var_name = "module_product." + name
    try :
        var_value = eval(var_name)
    except:
        var_value = None
    return var_value

menuList      = get_var("menuList")
STARTMENUID   = get_var("STARTMENUID")
TESTCASE      = get_var("TESTCASE")
CPLDVERSIONS    = get_var("CPLDVERSIONS")


 

SYSLOG_IDENTIFIER = "FWUPDATE"
OPENBMC_PASSWORD = "0penBmc"
g_info_tmp = ""
syslog_debug = 0
#信号处理： 不处理ctrl + N    
def sigint_handler(signum, frame):
    RJPRINT("\n\n不接收ctrl+c退出")

signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGHUP, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)

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

def test_tbd():
    RJPRINT("待实现")
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    return RET

def test_not_support():
    RJPRINT("该产品不支持此功能")
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    return RET

def quit():
    sys.exit(0)

def RJPRINTLINE(x):
    '''保留函数,后续适配3.x'''
    print(x, end=' ')

def RJPRINT(x,newline = True):
    '''保留函数,后续适配3.x'''
    if newline == True:
        print(x)
    else:
        print(x, end=' ')

def RJPRINTERR(str):
    print(("\033[0;31m%s\033[0m" % str))

def getRealUrl(case, param=None):
    http = TESTCASE.get('BMC').get('requesthttp')
    realurl = ""
    if param is None:
        realurl = "%scase=%s" %(http, case)
    else:
        realurl = "%scase=%s&param=%s"% (http, case, param)
    return realurl

def test_bmc_func(func,param=None,timeout=80):
    if param is None:
        ret = HttpRest().Get(getRealUrl(func),timeout)
    else:
        ret = HttpRest().Get(getRealUrl(func,json.dumps(param)),timeout)
    return ret

def test_bmc_channel():
    '''测试BMC通路'''
    ip = TESTCASE.get('BMC').get('ip')
    port = TESTCASE.get('BMC').get('port')
    msg = ''
    returncode = False
    import socket
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(5)
    try:
      sk.connect((ip,port))
      returncode =  True
    except Exception:
      msg = '到BMC通路失败,请确认'
      returncode = False
    sk.close()
    return returncode, msg

def test_bmc_testcase(param_t):
    ret = test_bmc_func(param_t)
    RJPRINT(ret.get(RETURN_KEY2))
    return ret


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
        log_error(e)
        sys.exit(-1)


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
        RJPRINT(e)
        RJPRINT("error\n\n")
    finally:
        if funcafter is not None:
            log_debug("    测试项后置:%s " % (funcafter))
            for i in range(0, 3):
                if funcafter() == True:
                    break
                else:
                   continue
    return RET

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

#菜单打印
#  printMenu
#  param: list_t  菜单项列表
#         id      菜单id
#
def printMenu(list_t, id):
    while True:
        try:
            printList(list_t, id)
            test = "请选择:"
            str= getch(test)
            RJPRINT(" %s" % str)
            log_debug("选择:%s" % str)
            str = str.lstrip().lower()
            if str == "q":
                if id == STARTMENUID:  #顶层目录，无路可退
                    quit()
                else:
                    break
            if str not in listindex:
                log_debug("%s 不在菜单项中" % str);
                RJPRINT("\n\n")
                continue
            else:
                RJPRINT("=======================> %s <======================="%list_t[listindex.index(str)][MENUITEMNAME])
                log_debug("选择的测试项为:%s id:%d" % (list_t[listindex.index(str)][MENUITEMNAME], id))
                
                RET = dealchoosefunc(list_t[listindex.index(str)])
                if RET == None:
                    RJPRINT("\n\n")
                    continue
                RJPRINT(" ")
                if RET[RETURN_KEY1] == 0:
                    RJPRINT("Test Result: Pass")
                    log_debug("菜单测试结果:" + SUCCESS_TIPS)
                elif RET[RETURN_KEY1] == 1:
                    pass
                else:
                    RJPRINT("Test Result: Fail")
                    log_debug("[%s]测试结果:" % list_t[listindex.index(str)][MENUITEMNAME] + 'error')
                RJPRINT("\n\n")
        except IndexError as d:
            RJPRINT("\n\n非法输入\n\n")
        except Exception as e:
            RJPRINT(e)
            #log_debug(e)
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

#根据id获取菜单
def startMenu(id):
    list,code = getMenuFromList(menuList, id)
    if code == False:
        log_error("错误的文件结构")
        RJPRINT("无此菜单，请确认")
        sys.exit(1)
    log_debug("根据ID获取到相应的菜单列表")
    printMenu(list, id)

# 开始
def start():
    global STARTMENUID
    if STARTMENUID is None:
        STARTMENUID = 0
    startMenu(STARTMENUID)

def usb0_init():
    '''配置USB0的IP'''
    usbip = TESTCASE.get("SONIC",{}).get("ip","1.1.1.1")
    cmd = "ifconfig usb0 %s netmask 255.255.255.0" % usbip
    ret,log = log_os_system(cmd, 0)
    if ret or "ERROR" in log:
        return False
    return True

def fac_init_check_ipmi():
    if not os.path.exists("/dev/ipmi0"):
        ret, log = log_os_system("rmmod ipmi_watchdog; rmmod ipmi_si; modprobe ipmi_msghandler; modprobe ipmi_si trydefaults=1 tryacpi=1;modprobe ipmi_devintf", 0)
        if not os.path.exists("/dev/ipmi0"):
            msg ="     无/dev/ipmi0设备,请检查"
            RJPRINT(msg)
            return False
    return True

# ====================================     
# 执行shell命令
# ====================================
def log_os_system(cmd, show):
    status, output = subprocess.getstatusoutput(cmd)
    if status:
        log_error('Failed :'+cmd)
        if show:
            RJPRINT('Failed :'+ cmd)
    return  status, output

def root_check():
    if os.geteuid() != 0:
        click.echo("请在Root权限下执行！")
        sys.exit(1)

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

def password_command(cmd, password, exec_timeout=30):

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
                msg = '与BMC连接超时'
                continue
            # 没有 public key
            if i == 1:
                child.sendline ('yes')
                i = child.expect([pexpect.TIMEOUT, 'password: '],timeout=30)
                if i == 0: # Timeout
                    msg = '与BMC连接超时'
                    continue
                if i == 1:#走到下面输入密码的逻辑
                    i = 2
            if i == 2: #输入密码
                child.sendline (password)
                i = child.expect([pexpect.EOF, pexpect.TIMEOUT], exec_timeout)
                if i == 0:
                    return True,child.before
                if i == 1:
                    msg = str(child.before)+"\nBMC执行命令超时"
                    return False,msg
            if i == 3: #BMC 拒绝连接
                msg =  '连接BMC失败'
                continue
            if i == 4:
                msg = child.before
        except Exception as e:
            msg = str(child.before)+"\n连接BMC失败"

    return False,msg

def getfilevalue(location):
    try:
        with open(location, 'r') as fd:
            value = fd.read()
        return True, value.strip()
    except Exception as e:
        return False, "error"

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

def mount_usb(print_cached = False):
    totalerr = 0
    errmsg = ""
    usb_mount_file = "/tmp/usb"
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    ret , info = getusbinfo();
    if ret == False:
        RJPRINT("读取USB信息失败")
        RET[RETURN_KEY1] = -1
        return RET

    print_clean()
    RET["already_mount"] = False
    RET["mount_dir"] = None

    usb_dev = info["id"]
    cmd = "fdisk -l |grep '%s'|grep 'Disk' -v|sort -k4 |tail -n1|awk '{print $1;}'"%usb_dev
    ret, usb_disk = log_os_system(cmd,0)
    cmd = "df -h 2>/dev/null|grep " + usb_disk
    ret, usb_already_mount_file = log_os_system(cmd,0)

    if "/" in usb_already_mount_file:
        RET["already_mount"] = True
        RET["mount_dir"] = re.split("\s+",usb_already_mount_file)[-1]
        return RET 

    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    if not os.path.exists(usb_mount_file):
        ret, log = log_os_system("mkdir %s && mount  %s %s"%(usb_mount_file, usb_disk, usb_mount_file), 0)
    else:
         ret, log = log_os_system("mount  %s %s"%(usb_disk, usb_mount_file), 0)
    if ret != 0 or len(log) > 0:
        print_temp(log,print_cached)
        print_temp("挂载U盘   FAILED",print_cached)
        RET[RETURN_KEY1] = -1
        return RET
    RET["mount_dir"] = usb_mount_file
    return  RET

def bin_pre_process(image_to_upgrade_rerules,remote = False,bin_dir = None):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    if bin_dir == None:
        RET = mount_usb()
        if RET[RETURN_KEY1] == -1:
           return RET
        bin_dir = RET["mount_dir"]

    image_to_use = None
    cmd = "ls %s |grep -E '%s'"%(bin_dir,image_to_upgrade_rerules)

    ret, image_msg = log_os_system(cmd,0)
    if ret != 0 and len(image_msg) != 0:
        print("执行指令 %s 出错:%s"%(cmd,image_msg))
        RET[RETURN_KEY1] = -2
        return RET
    if len(image_msg) == 0:
        print("没有找到符合命名规则(%s)的升级文件"%image_to_upgrade_rerules)
        RET[RETURN_KEY1] = -3
        return RET

    image_list = image_msg.split("\n")
    image_to_use = sorted(image_list,reverse=True)[0]

    image_list_len = len(image_list)
    if image_list_len != 1:
        print("检测到多个升级文件，选择升级最新版本")
    print("升级文件:%s"%image_to_use)
    RET["bin_dir"] = bin_dir
    RET["image_to_use"] = image_to_use
    if remote:
        bmcip = TESTCASE.get("BMC",{}).get("ip","1.1.1.2")
        cmd = 'scp -r %s/%s root@%s:/tmp'%(bin_dir,image_to_use,bmcip)
        ret, log = password_command(cmd,OPENBMC_PASSWORD,200)
        if ret and "100%" in log:
            RET["bin_name"] = "/tmp/"+image_to_use
            return RET
        else:
            print(log)
            print("传输bin文件失败")
            RET[RETURN_KEY1] = -4
            return RET
    else:
        RET["bin_name"] = bin_dir+'/'+image_to_use
        return RET

def test_bmc_image_update(bmc_info):
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    if makesure("升级BMC将导致BMC重启，是否继续？[Yes/No]：",True,echo = True):
        RET = bin_pre_process(TESTCASE["UPGRADE_CASE"]["bmc_regexp"],False)
        if RET[RETURN_KEY1] == -1:
            return RET
        cmd = "cp %s /tmp/image-bmc"%(RET["bin_name"])
        ret, image_msg = log_os_system(cmd,0)
        if ret != 0 and len(image_msg) != 0:
            RJPRINT("执行指令 %s 出错:%s"%(cmd,image_msg))
            RET[RETURN_KEY1] = -1
            return RET
        cmd = "which upgrade-bmc-bios.sh"
        ret, log = log_os_system(cmd,0)
        if ret or len(log) == 0:
            RJPRINT("未找到BMC升级脚本")
            RET[RETURN_KEY1] = -1
            return RET
        cmdstr="%s upgrade bmc /tmp/image-bmc %s erase" % (log,bmc_info)
        RJPRINT("BMC升级中，请等待...")
        successtips="succeeded to upgrade"
        log_debug(cmdstr)
        #os.system(cmdstr)
        ret1, status = log_os_system(cmdstr,0)
        log_debug(status)
        if ret1 == 0 and successtips in status:
            RJPRINT("BMC 升级成功,等待BMC重启...")
        else:
            RJPRINT("BMC 升级失败!")
            RET[RETURN_KEY1] = -1
            return RET
        # 升级BMC会重启BMC，需要重新配置X86端 USB0 IP
        # time.sleep(90) 改成先重启再升级，无需等待.
        ret_t = usb0_init()
        timeout = TESTCASE.get("SONIC",{}).get("timeout",120)
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
    else:
        RJPRINT("已撤销")
        RET[RETURN_KEY1] = 1
    return RET

def test_bmc_update_bcm5387():
    RET = {RETURN_KEY1 : 0 ,RETURN_KEY2 : ""}
    if makesure("确认升级BCM5387？[Yes/No]：",True,echo = True):
        tmp = TESTCASE.get("UPGRADE_CASE",{}).get("bcm5387", None)
        if tmp == None:
            RJPRINT("无BCM5387升级配置")
            RET[RETURN_KEY1] = 1
            return RET
        upgrade_file = tmp.get("upgrade_file", None)
        if upgrade_file == None:
            RJPRINT("无BCM5387升级文件信息")
            RET[RETURN_KEY1] = 1
            return RET
        RET = bin_pre_process(upgrade_file,True)
        if RET[RETURN_KEY1] == -1:
            return RET
        bcm5387 = RET["bin_name"]
        func = 'bmc_log_os_system'
        url = tmp.get("url", None)
        if url == None:
            RJPRINT("无BCM5387升级路径")
            RET[RETURN_KEY1] = 1
            return RET
        cmd = "cat %s > /sys/bus/spi/devices/%s/eeprom " % (bcm5387, url)
        log_debug(cmd)
        ret = test_bmc_func(func, cmd)
        if ret.get(RETURN_KEY1) != 0:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "BCM5387升级失败\nmessage:%s" % (ret.get(RETURN_KEY2))
        else:
            RJPRINT("BCM5387升级成功")
    else:
        RJPRINT("已撤销")
        RET[RETURN_KEY1] = 1
    return RET

def io_wr(reg_addr, reg_data):
    '''io写'''
    try:
        regdata  = 0
        regaddr  = 0
        if type(reg_addr) == int:
            regaddr = reg_addr
        else:
            regaddr = int(reg_addr, 16)
        if type(reg_data) == int:
            regdata = reg_data
        else:
            regdata = int(reg_data, 16)
        devfile = "/dev/port"
        fd = os.open(devfile, os.O_RDWR|os.O_CREAT)
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

def bios_force_switch(bios_info, cpu = False):
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

    if cpu == False:
        ret = test_bmc_func(func,switch_mod)
        return ret
    else:
        test_bios_swtch(switch_mod)
    return RET

def bios_update(bios_info):
    recovery_flag = False
    if bios_info == "master":
        RET = bin_pre_process(TESTCASE["UPGRADE_CASE"]["master_bios_regexp"], False)
    elif bios_info == "slave" and "slave_bios_regexp" in TESTCASE["UPGRADE_CASE"]:#主备BIOS烧片不同
        RET = bin_pre_process(TESTCASE["UPGRADE_CASE"]["slave_bios_regexp"], False)
    else:
        RET = bin_pre_process(TESTCASE["UPGRADE_CASE"]["master_bios_regexp"], False)
    if RET[RETURN_KEY1] == -1:
        return -1
    bios_image = RET["bin_name"]

    #切换升级通路
    log = get_bios_info()
    if log not in bios_info:
        bios_force_switch(bios_info, True)
        recovery_flag = True

    cmd = TESTCASE["UPGRADE_CASE"]["bios_clean_cmd"]
    RJPRINT("BIOS FLASH 擦除中...")
    ret, log = log_os_system(cmd, 0)
    if ret or "error" in log or "complete" not in log:
        RJPRINT("BIOS FLASH 擦除失败")
        if recovery_flag:
            bios_force_switch(log, True)
        return -1

    cmdstr = "dd if=%s of=/dev/mtd0 bs=1M count=8 skip=8 seek=8" % (bios_image)
    RJPRINT("BIOS升级中，请等待...")
    successtips = "8388608 bytes"
    log_debug(cmdstr)
    ret1, status = log_os_system(cmdstr, 0)
    log_debug(status)
    if recovery_flag:
        bios_force_switch(log, True)
    if ret1 == 0 and successtips in status:
        return 0
    else:
        RJPRINT("BIOS 升级失败!")
        return -1


def test_bios_image_update_new(bios_info):
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    ret = 0
    RJPRINT("请先确认BIOS配置中BIOS LOCK与 HOST Flash Lock-Down为Disabled状态!")
    if makesure("确认升级BIOS？[Yes/No]：",True,echo = True):
        if bios_info == "both":
            ret = bios_update("master")
            ret += bios_update("slave")
        else:
            ret = bios_update(bios_info)
        if ret == 0:
            RJPRINT("BIOS 升级成功,需要从主/备 BIOS启动，获取更新后的BIOS版本")
        else:
            RJPRINT("BIOS 升级失败!")
            RET[RETURN_KEY1] = -1
    else:
        RJPRINT("已撤销")
        RET[RETURN_KEY1] = 1
    return RET

def test_bmc_image_update_master():
    return test_bmc_image_update("master")

def test_bmc_image_update_slave():
    return test_bmc_image_update("slave")

def test_bmc_image_update_both():
    return test_bmc_image_update("both")

def test_bios_image_update(bios_info):
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    if makesure("确认升级BIOS？[Yes/No]：",True,echo = True):
        RET = bin_pre_process(TESTCASE["UPGRADE_CASE"]["bios_regexp"],False)
        if RET[RETURN_KEY1] == -1:
            return RET
        bios_image = RET["bin_name"]
        cmd = "which upgrade-bmc-bios.sh"
        ret, log = log_os_system(cmd,0)
        if ret or len(log) == 0:
            RJPRINT("未找到BIOS升级脚本")
            RET[RETURN_KEY1] = -1
            return RET
        cmdstr="%s upgrade bios %s %s" % (log,bios_image,bios_info)
        RJPRINT("BIOS升级中，请等待...")
        successtips="upgrade success"
        log_debug(cmdstr)
        #os.system(cmdstr)
        ret1, status = log_os_system(cmdstr,0)
        log_debug(status)
        if ret1 == 0 and successtips in status:
            if bios_info == "master":
                RJPRINT("主BIOS 升级成功,需要从主BIOS启动，获取更新后的BIOS版本")
            elif bios_info == "slave":
                RJPRINT("备BIOS 升级成功,需要从备BIOS启动，获取更新后的BIOS版本")
            else:
                RJPRINT("主备BIOS 升级成功,需要主备BIOS切换一次，获取更新后的BIOS版本")
        else:
            RJPRINT("BIOS 升级失败!")
            RET[RETURN_KEY1] = -1
    else:
        RJPRINT("已撤销")
        RET[RETURN_KEY1] = 1
    return RET

def test_bios_image_update_by_cpu():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    if makesure("确认升级BIOS？[Yes/No]：",True,echo = True):
        RET = bin_pre_process(TESTCASE["UPGRADE_CASE"]["bios_regexp"],False)
        if RET[RETURN_KEY1] == -1:
            return RET
        bios_image = RET["bin_name"]
        RET = bin_pre_process(TESTCASE["BIOS_UPDATE_TOOL"],False)
        if RET[RETURN_KEY1] == -1:
            return RET
        bios_afulnx = RET["bin_name"]

        cmd_mod = "chmod 755 %s" % bios_afulnx
        ret, log = log_os_system(cmd_mod,0)
        if ret != 0:
            return {RETURN_KEY1: -1, RETURN_KEY2: log}

        cmd="%s %s /P /B /N /L /K"%(bios_afulnx,bios_image)
        RJPRINT("BIOS升级中，请等待...")
        successtips="Verifying RomHole Block ..... done"
        log_debug(cmd)
        ret1, status = log_os_system(cmd,0)
        log_debug(status)
        if ret1 == 0 and successtips in status:
            RJPRINT("BIOS 升级成功,需要系统重启，获取更新后的BIOS版本")
        else:
            RJPRINT("BIOS 升级失败!")
            RET[RETURN_KEY1] = -1
    else:
        RJPRINT("已撤销")
        RET[RETURN_KEY1] = 1
    return RET

def test_bios_image_update_master():
    return test_bios_image_update("master")

def test_bios_image_update_slave():
    return test_bios_image_update("slave")

def test_bios_image_update_both():
    return test_bios_image_update("both")

def test_update_fpga_image(remote = False):
    RET = {RETURN_KEY1 : 0 ,RETURN_KEY2 : ""}
    if makesure("确认升级FPGA？[Yes/No]：",True,echo = True):
        fpga_package=TESTCASE.get("UPGRADE_CASE",{}).get("fpga_regexp")
        if fpga_package == None:
            RJPRINT("无FPGA升级配置信息")
            RET[RETURN_KEY1] = 1
            return RET
        if isinstance(fpga_package, dict):
            fpath = fpga_package.get("file")
            if not os.path.exists(fpath):
                RJPRINT("产品识别文件:%s, 不存在，请先执行facinit" % fpath)
                RET[RETURN_KEY1] = -1
                return RET
            with open(fpath,'r') as fd:
                ret = fd.read()
            fpga_package = fpga_package.get(ret)
        for item in fpga_package:
            RJPRINT("================= %s ===============" % item.get("name"))
            tmp_fpga_regexp = item.get("image")
            RJPRINT("查找规则(%s)的文件" % tmp_fpga_regexp)
            RET_BIN = bin_pre_process(tmp_fpga_regexp,remote)
            if RET_BIN[RETURN_KEY1] == -1:  #未插入U盘或者U盘挂载异常
                RET[RETURN_KEY1] = -1
                return RET
            if RET_BIN[RETURN_KEY1] < 0:
                RET[RETURN_KEY1] = -1
                continue
            upgrade_name=RET_BIN["bin_name"]
            slotlist = item.get("slot")
            chipname = item.get("chip", "fpga")
            successtips="upgrade succeeded!"
            for slot in slotlist:
                if item.get("displayname") is not None:
                    message = item.get("displayname") % slot
                else:
                    message = item.get("name")
                RJPRINT("%s 升级中，请等待..." % message)
                if remote == False:     # X86端升级fpga
                    cmdstr = "upgrade.py cold %s 0"%(upgrade_name)
                    log_debug(cmdstr)
                    ret1, status = log_os_system(cmdstr,0)
                    log_debug(status)
                    if ret1 == 0 and successtips in status:
                        RJPRINT("%s 升级成功!" % message)
                    else:
                        RJPRINT("%s 升级失败!" % message)
                        RET[RETURN_KEY1] = -1
                else:   #BMC端升级
                    params = {}
                    params["slot"] = slot
                    params["image"] = upgrade_name
                    ret_t = test_bmc_func("test_bmc_update_fpga_image",params,600)
                    log_debug(ret_t[RETURN_KEY2])
                    if ret_t[RETURN_KEY1] == -2:
                        RJPRINT("未找到升级工具")
                        RET[RETURN_KEY1] = ret_t[RETURN_KEY1]
                        RET[RETURN_KEY2] = ret_t[RETURN_KEY2]
                        return RET
                    if ret_t[RETURN_KEY1] == 0:
                        RJPRINT("%s 升级成功!" % message)
                    else:
                        RJPRINT("%s 升级失败!" % message)
                        RET[RETURN_KEY1] = -1
    else:
        RJPRINT("已撤销")
        RET[RETURN_KEY1] = 1
    return RET

def send_commands(commands, in_x86 = True):
    func = 'bmc_log_os_system'
    for command in commands:
        cmd = command.get("cmd")
        sleep_time = command.get("sleep", 0)
        if in_x86:
            ret, msg = log_os_system(cmd, 0)
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
    ret, val = send_commands(commands, flag)
    if ret:
        return True, ""
    else:
        return False, ""

def test_open_bmc_gpio():
    return test_open_gpio(False)

def test_close_bmc_gpio():
    return test_close_gpio(False)

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

def test_update_cpld_image(remote = False):
    RET = {RETURN_KEY1 : 0 ,RETURN_KEY2 : ""}
    if makesure("确认升级CPLD？[Yes/No]：",True,echo = True):
        cpld_package=TESTCASE.get("UPGRADE_CASE",{}).get("cpld_regexp")
        if cpld_package == None:
            RJPRINT("无CPLD升级配置信息")
            RET[RETURN_KEY1] = 1
            return RET
        if isinstance(cpld_package, dict):
            fpath = cpld_package.get("file")
            if not os.path.exists(fpath):
                RJPRINT("产品识别文件:%s, 不存在，请先执行facinit" % fpath)
                RET[RETURN_KEY1] = -1
                return RET
            with open(fpath,'r') as fd:
                ret = fd.read()
            cpld_package = cpld_package.get(ret)
        for item in cpld_package:
            RJPRINT("================= %s ===============" % item.get("name"))
            tmp_cpld_regexp = item.get("image")
            RJPRINT("查找规则(%s)的文件" % tmp_cpld_regexp)
            RET_BIN = bin_pre_process(tmp_cpld_regexp,remote)
            if RET_BIN[RETURN_KEY1] == -1:  #未插入U盘或者U盘挂载异常
                RET[RETURN_KEY1] = -1
                return RET
            if RET_BIN[RETURN_KEY1] < 0:
                RET[RETURN_KEY1] = -1
                continue
            upgrade_name=RET_BIN["bin_name"]
            slotlist = item.get("slot")
            successtips="upgrade succeeded!"
            for slot in slotlist:
                if item.get("displayname") is not None:
                    message = item.get("displayname") % slot
                else:
                    message = item.get("name")
                RJPRINT("%s 升级中，请等待..." % message)
                if remote == False:     # X86端升级CPLD
                    cmdstr = "upgrade.py cold %s 0"%(upgrade_name)
                    log_debug(cmdstr)
                    ret1, status = log_os_system(cmdstr,0)
                    log_debug(status)
                    if ret1 == 0 and successtips in status:
                        RJPRINT("%s 升级成功!" % message)
                    else:
                        RJPRINT("%s 升级失败!" % message)
                        RET[RETURN_KEY1] = -1
                else:   #BMC端升级
                    params = {}
                    params["slot"] = slot
                    params["image"] = upgrade_name
                    ret_t = test_bmc_func("test_bmc_update_cpld_image",params,600)
                    log_debug(ret_t[RETURN_KEY2])
                    if ret_t[RETURN_KEY1] == -2:
                        RJPRINT("未找到升级工具")
                        RET[RETURN_KEY1] = ret_t[RETURN_KEY1]
                        RET[RETURN_KEY2] = ret_t[RETURN_KEY2]
                        return RET
                    if ret_t[RETURN_KEY1] == 0:
                        RJPRINT("%s 升级成功!" % message)
                    else:
                        RJPRINT("%s 升级失败!" % message)
                        RET[RETURN_KEY1] = -1
    else:
        RJPRINT("已撤销")
        RET[RETURN_KEY1] = 1
    return RET


def test_cpu_update_cpld_image():
    return test_update_cpld_image(remote=False)

def test_bmc_update_cpld_image():
    return test_update_cpld_image(remote=True)

def rji2cget(bus, devno, address):
    command_line = "i2cget -f -y %d 0x%02x 0x%02x " % (bus, devno, address)
    retrytime = 6
    ret_t = ""
    for i in range(retrytime):
        ret, ret_t = log_os_system(command_line,0)
        if ret == 0:
            return True, ret_t
        time.sleep(0.1)
    return False, ret_t

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

def test_bios_force_switch(bios_info):
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
        ret = test_bmc_func(func,switch_mod)
        return ret
    else:
        RJPRINT("已撤销")
        RET[RETURN_KEY1] = 1
    return RET

def test_bios_force_switch_slave():
    return test_bios_force_switch("slave")

def test_bios_force_switch_master():
    return test_bios_force_switch("master")

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
        RJPRINT("已成功执行切换操作")
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
    else:
        RJPRINT("已撤销")
        RET[RETURN_KEY1] = 1
    return RET

def test_bmc_image_force_switch_master():
    return test_bmc_image_force_switch("master")

def test_bmc_image_force_switch_slave():
    return test_bmc_image_force_switch("slave")

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

def test_bios_version():
    RET = test_bios_flash()
    RJPRINT("%-21s： %s" % ('主BIOS版本',"%s"%(RET["master"])))
    RJPRINT("%-21s： %s" % ('备BIOS版本',"%s"%(RET["slave"])))
    log = get_bios_info()
    RJPRINT("%-20s： %s" % ('当前BIOS',"%s"%(log)))
    return RET

def io_rd(reg_addr, len =1):
    '''io读'''
    try: 
        regaddr = 0
        if type(reg_addr) == int:
            regaddr = reg_addr
        else:
            regaddr = int(reg_addr, 16)
        devfile = "/dev/port"
        fd = os.open(devfile, os.O_RDWR|os.O_CREAT)
        os.lseek(fd, regaddr, os.SEEK_SET)
        str = os.read(fd, len)
        return "".join(["%02x"% ord(item) for item in str])
    except ValueError: 
        return None
    except Exception as e:
        print(e)
        return None
    finally:
        os.close(fd)
    return None

def get_cpld_version():
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
        if gettype == "io":
            for i in range(4):
                ret = io_rd(io_addr + i)
                if ret == None:
                    t = False
                    break;
                data += chr(int(ret,16))
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
    return totalerr,result

def test_cpld_version():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    ind, val  = get_cpld_version()
    for item in val:
        formatstr = "  %-20s： %s%s"
        RJPRINT(formatstr%(item[0],item[2],item[1]))
    RET[RETURN_KEY1] = ind
    return RET

## 固件升级主程序
if __name__ == '__main__':
    root_check()
    #fac_init_check_ipmi()
    usb0_init()
    log_info("固件升级主程序")
    start()
