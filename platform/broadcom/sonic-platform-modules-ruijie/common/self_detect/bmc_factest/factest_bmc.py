#!/usr/bin/python
# -*- coding: UTF-8 -*-
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
import socket
import fcntl,struct
import json
import struct
import base64
import os, errno
import glob
import unicodedata


def wide_chars(s):
    if isinstance(s, str):
        s = s.encode().decode('utf-8')
    return sum(unicodedata.east_asian_width(x) in ('F', 'W') for x in s)


def get_device_branch():
    ret_t, log = subprocess.getstatusoutput("fw_printenv productname")
    if ret_t == 0 :
        val_t = log.split("=")
        return val_t[1]
    else:
        return "NA"

def get_board_id():
    ret_t, log = subprocess.getstatusoutput("fw_printenv board_id")
    if ret_t == 0 :
        val_t = log.split("=")
        return val_t[1]
    else:
        return "NA"

def get_productname():
    productname = "NA"
    if os.path.isfile('/etc/device/productname'):
        with open("/etc/device/productname") as fd:
            productname = fd.read().strip()
    return productname


Device_branch = get_device_branch()
board_id = get_board_id()
productname = get_productname()

grtd_productfile = ("BMC_ruijie_"+Device_branch+ "_rj_r0_config").replace("-","_")
grtd_board_id_productfile = ("BMC_ruijie_"+Device_branch+ "_rj_"+board_id+"_r0_config").replace("-","_")
grtd_product_productfile = ("BMC_ruijie_"+productname+ "_rj_r0_config").replace("-","_")

common_productfile = "ruijiecommon"

configfile_pre   =  "/usr/sbin/"
import sys
sys.path.append(configfile_pre)
configfile_pre = '/tmp/bmc_factest/'


############################################################################################
global  module_product
if os.path.exists(configfile_pre + grtd_board_id_productfile + ".py"):
    module_product  = __import__(grtd_board_id_productfile, globals(), locals(), [], 0)
elif os.path.exists(configfile_pre + grtd_productfile + ".py"):
    module_product  = __import__(grtd_productfile, globals(), locals(), [], 0)
elif os.path.exists(configfile_pre + grtd_product_productfile + ".py"):
    module_product  = __import__(grtd_product_productfile, globals(), locals(), [], 0)
elif os.path.exists(configfile_pre + common_productfile + ".py"):
    module_product  = __import__(common_productfile, globals(), locals(), [], 0)
else:
    print("config file not found")
    exit(-1)

def get_var(name, default = None):
    global  module_product
    var_name = "module_product." + name
    try :
        var_value = eval(var_name)
    except:
        var_value = default
    return var_value

menuList      = get_var("menuList")
CPU_ID        = get_var("CPU_ID")
DCDC_DEVICE   = get_var("DCDC_DEVICE")
PSU_INFO      = get_var("PSU_INFO")
I2C_SCAN_LIST = get_var("I2C_SCAN_LIST")
LED_INFO      = get_var("LED_INFO")
FAN_SPEED     = get_var("FAN_SPEED")
E2_DEV        = get_var("E2_DEV")
FAN_PROTECT   = get_var("FAN_PROTECT")
CPLD_TEST     = get_var("CPLD_TEST")
FPGA_TEST     = get_var("FPGA_TEST")
MGMT_LOOPBACK = get_var("MGMT_LOOPBACK")
BIOS_TEST     = get_var("BIOS_TEST")
BMC_USB0      = get_var("BMC_USB0")
BMC_SENSOR    = get_var("BMC_SENSOR")
INSP_LED_CTL  = get_var("INSP_LED_CTL")
I2C_SCAN_TIMES  = get_var("I2C_SCAN_TIMES")
MDIO_DEV_DICT  = get_var("MDIO_DEV_DICT")
TEMPS_LIST = get_var("TEMPS_LIST")
PSU_PMBUS_LIST = get_var("PSU_PMBUS_LIST")
TESTCASE = get_var("TESTCASE", {})


import argparse
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-o","--operations",type=str,
    choices=["bmc_get_cpu_info",
             "bmc_get_ddr_info",
             "bmc_get_emmc_info",
             "bmc_test_emmc_stress",
             "bmc_test_emmc_stress_result",
             "bmc_test_emmc_stress_stop",
             "bmc_test_ddr_stress",
             "bmc_test_ddr_stress_result",
             "bmc_test_ddr_stress_stop",
             "bmc_get_dcdc_info",
             "bmc_test_peci",
             "bmc_test_peci_new",
             "bmc_test_SML0",
             "bmc_test_MDIO",
             "bmc_test_get_fan_present",
             "bmc_test_get_fan_speed",
             "bmc_test_set_fan_speed_high_without_reset",
             "bmc_test_set_fan_speed_reset",
             "bmc_test_set_fan_speed_high",
             "bmc_test_set_fan_speed_middle",
             "bmc_test_set_fan_speed_low",
             "bmc_test_get_psu_rfu_info",
             "bmc_test_get_psu_info",
             "bmc_test_get_psu_present",
             "bmc_test_i2c_scan",
             "bmc_test_i2c_stress",
             "bmc_set_led",
             "bmc_led_control",
             "bmc_test_cpu_gpio",
             "bmc_get_e2_show_list",
             "bmc_get_e2_set_list",
             "bmc_get_e2_bin",
             "bmc_write_e2_bin",
             "bmc_cpld_check",
             "bmc_fpga_check",
             ],
    help="给restful 调用")
parser.add_argument("-pid","--processid",type=str,help = "要杀死的进程ID")
parser.add_argument("-led","--ledtype",type=str,help = "需要设置的led的类型")
parser.add_argument("-ledattr","--ledattribute",type=str,help = "需要设置的led的属性")
parser.add_argument("-action","--action",type=str,help = "需要执行的动作")
parser.add_argument("-json","--json_str",type=str,help = "json 参数")
args = parser.parse_args()
#import inspect
#import ctypes

#on_appengine = os.environ.get('SERVER_SOFTWARE','').startswith('Development')
#if on_appengine and os.name == 'nt':
#    os.name = None
#import msvcrt
log_debug_flag = 0
def log_debug(a):
   if log_debug_flag == 1:
       print(a)

def log_error(a):
   if log_debug_flag == 1:
       print(a)
#几个压力测试项 后台运行需要
#import multiprocessing

grtdlog_dir= "/var/grtd"
grtdlog_name = grtdlog_dir +"/grtdtest.log"
kjlogmaxshow = 10
if not os.path.exists(grtdlog_dir):
    os.makedirs(grtdlog_dir)

SYSLOG_IDENTIFIER = "FACTEST"


LOGERROR = False
DEBUG = False
KAOJILOGPATH = "/var/grtd/"
KAOJILOGFILE = KAOJILOGPATH + "kjlog.log"
KAOJISTATUS = 1
ISKAOJI = 0
# CONFIG_NAME = "apptest.xml"
RTC_WAIT_TIME                   = 3
RTC_THRESHOLD_LOWER             = 3
RTC_THRESHOLD_UPPER             = 4
SUCCESS_TIPS                    = "PASS"

RETURN_KEY1       = "code"
RETURN_KEY2       = "msg"
#后台执行项 返回暂时 采用执行函数的返回，不直接打印pass
KT_K_BG_SUCCESS = 1
KT_K_BG_FAILD = -1
#RETURN_KEY1 : -1 表示有一个失败项 0 表示没有失败项  1用来指示后台运行成功
ERROR_RETURN      = {RETURN_KEY1 : -1, RETURN_KEY2 : "init error"}
SUCCESS_RETURN    = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
#顺利执行返回

SUCCESS_RETURN_EXCECUTE_OFFLINE = {RETURN_KEY1 : KT_K_BG_SUCCESS, RETURN_KEY2 : "已启动后台执行"}
SUCCESS_RETURN_EXCECUTE_OFFLINE_END = {RETURN_KEY1 : KT_K_BG_SUCCESS, RETURN_KEY2 : "结束测试"}
ERROR_RETURN_DETAIL  = {RETURN_KEY1 : -1, RETURN_KEY2 : []}

kj_result =[]
MENUID     = "menuid"
MENUPARENT = "parentid"
MENUVALUE  =  "value"
CHILDID    = "childid"
MENUITEMNAME = "name"
MENUITEMDEAL = "deal"
GOBACK  = "goBack"
GOQUIT  = "quit"

listindex=['1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','g','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
formatStringLevel1 = "%s.%s"
SYSINFOTIPS_FORMAT = "%30s : %s"
nosetrtc = 1

#发给sonic时，必须保持一定的格式，不能随便print
#在本地显示时，直接打印出来不会显得太卡顿
g_info_tmp_for_sonic = ""
def print_choose(str):
    global g_info_tmp_for_sonic
    g_info_tmp_for_sonic += str+"\n"
    print(str)

def print_sonic(RET):
    global g_info_tmp_for_sonic
    if g_info_tmp_for_sonic != "":
       RET[RETURN_KEY2] = g_info_tmp_for_sonic
    #print RET
    g_info_tmp_for_sonic = ""

#def ApplicationInstance():
#    global pidfile
#    pidfile = open(os.path.realpath(__file__), "r")
#    try:
#        fcntl.flock(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB) #创建一个排他锁,并且所被锁住其他进程不会阻塞
#    except:
#        print "已有一个程序在运行...."
#        sys.exit(1)

def RJPRINT(x):
    if LOGERROR:
        print(x)
    else:
        print(x)
def bmc_get_productinfo():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    RET[RETURN_KEY2] = Device_branch
    return RET

def check_i2c_bus(param):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    val_t = json.loads(param)
    bus = val_t.get('endbus',None)
    cmdstr = ""

    i2cpath = "/sys/bus/i2c/devices/" + bus
    if  os.path.exists(i2cpath):
        RET[RETURN_KEY1] = 0
        RET[RETURN_KEY2] = 'bus有找到对应的'
    else:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = '未找到对应的BUS'
    return RET


def bmc_reboot():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    log_os_system("sync", 0)
    log_os_system("reboot -f", 0)
    return RET

def get_sysfs_value(reg_name):
    mb_reg_file =  reg_name
    str = ""
    if (not os.path.isfile(mb_reg_file)):
        str =  mb_reg_file + 'not found !'
        return False, str
    try:
        with open(mb_reg_file, 'r') as fd:
            retval = fd.read()
    except Exception as error:
        str = "Unable to open " + mb_reg_file + "file !"
        return False, str
    retval = retval.rstrip('\r\n')
    retval = retval.lstrip(" ")
    return True, retval

def write_sysfs_value(reg_name, value):
    fileLoc = reg_name
    try:
        if not os.path.isfile(fileLoc):
            print(fileLoc,  'not found !')
            return False , "%s not found! " % fileLoc
        with open(fileLoc, 'w') as fd:
            fd.write(value)
    except Exception as error:
        return False , 'Unable to open %s  file' % fileLoc
    return True,""

def rji2cget(bus, devno, address):
    command_line = "i2cget -f -y %d 0x%02x 0x%02x " % (bus, devno, address)
    retrytime = 6
    ret_t = ""
    for i in range(retrytime):
        ret, ret_t = log_os_system(command_line,0)
        if ret == 0:
            return ret, ret_t
        time.sleep(0.1)
    return ret, ret_t

def rji2cget_32bit(bus, devno, address): #address = "0x00 0x00 0x00 0x00"
    command_line = "i2ctransfer -f -y %d w4@0x%02x %s r4 " % (bus, devno, address)
    retrytime = 6
    ret_t = ""
    for i in range(retrytime):
        ret, ret_t = log_os_system(command_line,0)
        if ret == 0:
            return ret, ret_t
        time.sleep(0.1)
    return ret, ret_t

def rji2cset(bus, devno, address, byte):
    command_line = "i2cset -f -y %d 0x%02x 0x%02x 0x%02x" % (
        bus, devno, address, byte)
    retrytime = 6
    ret_t = ""
    for i in range(retrytime):
        ret, ret_t = log_os_system(command_line,0)
        if ret == 0:
            return ret, ret_t
        time.sleep(0.1)
    return ret, ret_t

def rji2cget32(bus, devno, address):
    command_line = "i2cget -f -y %d 0x%02x %d i" % (
        bus, devno,address)
    retrytime = 6
    ret_t = ""
    for i in range(retrytime):
        ret, ret_t = log_os_system(command_line,0)
        if ret == 0:
            return ret, ret_t
        time.sleep(0.1)
    return ret, ret_t

def quit():
    sys.exit(0)

def test_tbd():
    print("待实现")
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    if args.operations != None:
       print(RET)
    return RET

def test_sys_reload():
    log_os_system("sync", 0)
    log_os_system("reboot", 0)


#菜单打印 菜单项带前面数字提示符
def printList(_list, id):
    try:
        RJPRINT("****************************************")
        for index in range(len(_list)):
            print(formatStringLevel1 %( listindex[index] , _list[index]["name"]))
        if id != 0:
            RJPRINT("q.返回上一层")
        else:
            RJPRINT("q.退出")

        RJPRINT("****************************************")
    except Exception as e:
        log_error(e)
        sys.exit(-1)

def test_all():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    for item in alltest:
        print("")
        print("=" * 12 + item[MENUITEMNAME] + "=" *12)
        RET = eval(item[MENUITEMDEAL])()
    return RET

#菜单打印
#  printMenu
#  param: list_t  菜单项列表
#         id      菜单id
#  当前菜单处理，目前该实现应该是叶子菜单项
#
def printMenu(list_t, id):
    global nosetrtc
    while True:
        try:
            printList(list_t, id)
            test = "请选择:"
            try:
               str = input(test)
            except Exception as ex:
               continue
            #bmc 中暂时不支持
            #str= getch(test)

            log_debug("选择:%s" % str)
            str = str.lstrip().lower()
            if str == "q":
                break#eval("goBack")(id)
            if str not in listindex:
                log_debug("%s 不在菜单项中" % str);
                RJPRINT("\n\n")
                continue;
            else:
                print("=======================> %s <======================="%list_t[listindex.index(str)][MENUITEMNAME])
                log_debug("选择的测试项为:%s id:%d" % (list_t[listindex.index(str)][MENUITEMNAME], id))

                if CHILDID in list_t[listindex.index(str)]:
                    childid = list_t[listindex.index(str)][CHILDID]
                    RET = eval(list_t[listindex.index(str)][MENUITEMDEAL])(childid)
                else:
                    RET = eval(list_t[listindex.index(str)][MENUITEMDEAL])()

                if RET == None:
                   RJPRINT("\n\n")
                   continue

                if RET[RETURN_KEY1] == 0:
                    RJPRINT(RET[RETURN_KEY2])
                    RJPRINT("Test Result: Pass")
                    log_debug("菜单测试结果:" + SUCCESS_TIPS)
                elif RET[RETURN_KEY1] == 1:
                    RJPRINT(RET[RETURN_KEY2])
                else:
                    RJPRINT("Test Result: Fail")
                    log_debug("[%s]测试结果:" % list_t[listindex.index(str)][MENUITEMNAME] + 'error')
                    #log_debug(RET[RETURN_KEY2])
           # print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                RJPRINT("\n\n")
        except IndexError as d:
            print("\n\n非法输入\n\n")
        except Exception as e:
            print(e)
            #log_debug(e)
            #RJPRINTERR("\n\n 异常\n\n" )

def getMenuFromList(list, id):
    for key in list:
        if key[MENUID] == id:
            return key[MENUVALUE],True
    return 0, False

def getParentIdMenuFromList(list, id):
    for key in list:
        if key[MENUID] == id and MENUPARENT in key:
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


# 菜单： 单项测试
def test_signal(id):
    startMenu(id)

#不论大小比较字符串
def astrcmp(str1,str2):
    return str1.lower()==str2.lower()

#led check输入确认
def get_led_inputcheck(LED,STATE):
    err = 0;
    while True:
        print("%s是否切换为%s[Yes/No]："%(LED,STATE), end=' ')
        str = input("")
        if astrcmp(str, "y") or astrcmp(str, "ye") or astrcmp(str, "yes") or astrcmp(str, ""):
            return True
        elif astrcmp(str, "n") or astrcmp(str, "no"):
            return False


# 菜单：系统配置
def test_sysconfig(id):
    startMenu(id)

#设置debug等级
def test_setdebug():
    global DEBUG
    DEBUG = not DEBUG
    return  {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}

#根据id获取菜单
def startMenu(id):
    list,code = getMenuFromList(menuList, id)
    if code == False:
        log_error("错误的文件结构")
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

#开始
def start():
    startMenu(0)

#menu调用
def goBack(id):
    log_debug(str(id))
    parentid,code = getParentIdMenuFromList(menuList, id)
    if code == False:
        log_error("无父结点")
        sys.exit(1)
    list,code = getMenuFromList(menuList, parentid)
    if code == False:
        log_error("错误的文件结构")
        sys.exit(1)
    startMenu(parentid)


# ====================================
# 执行shell命令
# ====================================
def get_sys_execute(str):
    #function 1
    result = os.popen(str)
    res = result.read()
    for line in res.splitlines():
        print(line)
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
        print("[RUIJIE]:", end=' ')
        print(txt)
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
            print(('Failed :'+ cmd))
    return  status, output
# ====================================
# 拷机初始化
# ====================================
def kj_init():
    global KAOJILOGFILE
    time1 = time.time();
    timeArraystart = time.localtime(time1)
    otherStyleTime = time.strftime("%m-%d_%H.%M", timeArraystart)
    KAOJILOGFILE = "/var/grtd/kjlog_%s.log" % otherStyleTime
    log_debug("创建的拷机日志:" + KAOJILOGFILE)

    file = open(KAOJILOGFILE,'w')
    file.close()

# ====================================
# 拷机结果保存
# ====================================
def KJERSULT(log):
    global KAOJILOGFILE
    with open(KAOJILOGFILE, 'w') as f:
         print(log, file=f)
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
            for item in looptest:
                kj_itemresult = {"name":"test", "loop":[], "error":[]}
                print("\n\n",item[MENUITEMNAME])
                print("=" * 60)
                log_debug(" ")
                log_debug("==========%s 开始============" % item[MENUITEMNAME])
                RET = eval(item[MENUITEMDEAL])()
                #log_debug(RET)
                if RET[RETURN_KEY1] != 0:
                    if kj_isexit(item[MENUITEMNAME], kj_result):
                        it = kj_find_result(item[MENUITEMNAME], kj_result)
                        #log_debug(it)
                        it["loop"].append(loop)
                        it["error"].append(RET[RETURN_KEY2])
                    else:
                        kj_itemresult["name"] = item[MENUITEMNAME]
                        kj_itemresult["loop"].append(loop)
                        kj_itemresult["error"].append(RET[RETURN_KEY2])
                        #log_debug(kj_itemresult)
                        kj_result.append(kj_itemresult)
                log_debug("==========%s 结束============" % item[MENUITEMNAME])
            time2 = time.time();
            timeArrayend = time.localtime(time2)
            otherStyleTime1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArrayend)
            real_kj_result["endtime"] = otherStyleTime1
            real_kj_result["result"] = kj_result
            real_kj_result["loop"] = loop
            #写文件
            KJERSULT(real_kj_result)
            loop += 1
            #isloopprint = True
            #time.sleep(5)
            if KAOJISTATUS == 0:
                break;
        ISKAOJI = 0
    except Exception as e:
        print(e)
        log_error(e)
    return {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}

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
    with open(filename, 'r') as f:
         str1 = f.read()
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
            print("第【%d】轮数错误:" % loop)
            index = item["loop"].index(loop)
            errmsg = item["error"][index]
            if isinstance(errmsg, list):
                for test in errmsg:
                    RJPRINT("   %s :  " % test["name"])
                    for case_ret  in test["errmsg"]:
                        RJPRINT("           {name}   {error}".format(**case_ret) )
            elif isinstance(errmsg, str):
                RJPRINT("{0}   {1}".format(item["name"] , errmsg))
            RJPRINT("\n")
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
            print("%d. %s"%(index, os.path.basename(x)))
            index += 1
            if (index >= kjlogmaxshow):
                break
        print("q. %s"%("返回上一层"))
        test = "请选择:"
        str= getch(test)
        print(" %s" % str)
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
    print("当前调试等级为:  %s" % levelNames[logger.level])
    startMenu(3)

#信号处理： 不处理ctrl + N
def sigint_handler(signum, frame):
    global KAOJISTATUS
    KAOJISTATUS = 0
    if ISKAOJI == 1:
        print("\n\n已经输入ctrl+c 请等待本轮执行结束")
    else:
        print("\n\n不接收ctrl+c退出")


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



pidfile = 0
############################################################################################
##  文件锁
############################################################################################
def ApplicationInstance():
    global pidfile
    #pidfile = open(os.path.realpath(__file__), "r")
    pidfile = open("/tmp/single_bmc", "a")
    try:
        fcntl.flock(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB) #创建一个排他锁,并且所被锁住其他进程不会阻塞
    except:
        if args.operations != None:
            print({RETURN_KEY1 : -1,  RETURN_KEY2 : "已有一个程序在运行...."})
        else:
            print("启动失败，请确确认:\r\n\
                   1、是否已有另一个diag_bmc进程在本设备上运行？\r\n\
                   2、是否已有diag进程在sonic端运行？\r\n\
                   3、是否sonic端的diag进程被强行kill？如果是，请重新启动diag并正常退出。\r\n")
        sys.exit(1)

def unlockInstance():
    global pidfile
    fcntl.flock(pidfile,fcntl.LOCK_UN)
def fac_init_setmac():
    if getsyseeprombyId(TLV_CODE_PRODUCT_NAME) == None or getsyseeprombyId(TLV_CODE_SERIAL_NUMBER) == None or\
       getsyseeprombyId(TLV_CODE_MAC_BASE) == None or getsyseeprombyId(TLV_CODE_DEVICE_VERSION) == None :
        log_debug("需要重新setmac")
        return False
    return True

thread_test_ddr = None;
thread_test_emmc = None;
def background_test_stress(thread_hander, test_result_file, cmd):
    RET = {RETURN_KEY1 : KT_K_BG_SUCCESS, RETURN_KEY2 : ""}
    ret, log = log_os_system("which stressapptest", 0)

    if len(log):
        if thread_hander != None:#对于sonic 调用来说，这个条件永远不成立，所以判断逻辑放在sonic端
            RET[RETURN_KEY2] = "后台已有该执行任务，请首先查看测试结果或终止上次测试任务"
        else:
            RET[RETURN_KEY2] = "已启动后台执行"
            with open(test_result_file, "w+") as f:
                thread_hander = subprocess.Popen(cmd, shell=True, stdout=f)
    else:
        RET[RETURN_KEY2] = "no stressapptest cmd"
    #if args.operations != None:

    #  print {"RET":RET,"pid":(thread_hander.pid)}
    return thread_hander,RET

def stop_makesure():
    while True:
        print("强行结束将无法查看结果，是否继续？[Yes/No]：", end=' ')
        str = input("")
        if astrcmp(str, "y") or astrcmp(str, "ye") or astrcmp(str, "yes") or astrcmp(str, ""):
            return True
        elif astrcmp(str, "n") or astrcmp(str, "no"):
            return False


def background_test_stress_stop(thread_hander, pid = -1,is_sonic = 0):
    RET = {RETURN_KEY1 : KT_K_BG_SUCCESS, RETURN_KEY2 : ""}
    #if args.operations == None: #本地运行
    if thread_hander == None:
        RET[RETURN_KEY2] = "未启动后台测试"
        #if args.operations != None:
        #   print_sonic(RET)
        return thread_hander,RET
    #if stop_makesure():强制执行，后续可能需要增加确认
        #该方法并不能杀死
    #if not is_sonic:
    #    if not stop_makesure():
    #        return thread_hander,{RETURN_KEY1 : 1, RETURN_KEY2 : "已撤销"}
    thread_hander.terminate()

    cmd = "kill -9 %d"%(thread_hander.pid + 1)
    #else:#由sonic 下发
    #    cmd = "kill -9 %d"%(pid)
    #不管输出
    ret, log = log_os_system(cmd, 0)
    RET[RETURN_KEY2] = "该后台测试已被终止"
    thread_hander = None
    #if args.operations != None:
    #   print_sonic(RET)
    return thread_hander, RET

def background_test_stress_result(thread_hander, test_result_file, pid = -1):
    RET = {RETURN_KEY1 : 1, RETURN_KEY2 :""}

    #if args.operations == None: #本地运行
    if thread_hander == None:
       #print "未启动后台测试，没有测试结果"
       print_sonic(RET)
       RET[RETURN_KEY2] = "未启动后台测试，没有测试结果"
       return thread_hander, RET
    pid = thread_hander.pid

    ret = thread_hander.poll()
    if ret != 0:
        #if args.operations != None: #本地运行
        RET[RETURN_KEY1] = 1
        RET[RETURN_KEY2] = "测试还未结束，测试时长1mins, 请稍后查看结果"
        print_sonic(RET)
        return thread_hander, RET

    time.sleep(3)
    bufferSize = 5000
    input = ""
    resuult = ""

    try:
       file = os.open(test_result_file, os.O_RDONLY | os.O_NONBLOCK);
       input = os.read(file, bufferSize);
       resuult = input
       os.close(file)
    except OSError as err:
        resuult = "测试结果为空，请重新执行该测试项"
        os.close(file)
    if "Status: PASS"  not in resuult:
        RET[RETURN_KEY1] = -1
    else:
        RET[RETURN_KEY1] = 0
    RET[RETURN_KEY2] = resuult
    thread_hander = None;
    #if args.operations != None:
    #   print_sonic(RET)
    return thread_hander, RET


ddr_test_result_file = "/tmp/ddr_test_result"
emmc_test_result_file = "/tmp/emmc_test_result"

def bmc_test_ddr_stress():
    global thread_test_ddr
    cmd = "stressapptest -M 100 -s 60"
    global ddr_test_result_file
    test_result_file = ddr_test_result_file
    thread_test_ddr, ret =  background_test_stress(thread_test_ddr, test_result_file, cmd)
    return ret

def bmc_test_ddr_stress_stop( pid = -1 ):
    global thread_test_ddr
    test_result_file = ddr_test_result_file
    thread_test_ddr, ret = background_test_stress_stop(thread_test_ddr, int(pid))
    return ret

def bmc_test_ddr_stress_stop_by_sonic( pid = -1 ):
    global thread_test_ddr
    test_result_file = ddr_test_result_file
    thread_test_ddr, ret = background_test_stress_stop(thread_test_ddr, int(pid),1)
    return ret


def bmc_test_ddr_stress_result( pid = -1 ):
    global thread_test_ddr
    global ddr_test_result_file
    test_result_file = ddr_test_result_file
    thread_test_ddr, ret = background_test_stress_result(thread_test_ddr, test_result_file, int(pid) )
    return ret

def bmc_test_emmc_stress():
    global thread_test_emmc
    test_result_file = emmc_test_result_file
    cmd = "stressapptest -f /data/data1 -f /data/data2 --filesize 20m --read-block-size 1024 -M 100M"
    thread_test_emmc, ret =  background_test_stress(thread_test_emmc, test_result_file, cmd)
    return ret

def bmc_test_emmc_stress_stop( pid = -1 ):
    global thread_test_emmc
    test_result_file = emmc_test_result_file
    thread_test_emmc, ret = background_test_stress_stop(thread_test_emmc, int(pid))
    return ret
def bmc_test_emmc_stress_result( pid = -1 ):
    global thread_test_emmc
    test_result_file = emmc_test_result_file
    thread_test_emmc, ret = background_test_stress_result(thread_test_emmc, test_result_file, int(pid))
    return ret

def bmc_get_cpu_info():

    RET = {RETURN_KEY1 : -1, RETURN_KEY2 : ""}
    cmd = "cat /proc/cpuinfo | grep 'Revision\|Serial' -v"

    ret, log1 = log_os_system(cmd, 0)
    if ret != 0 or len(log1) <= 0:
        RET[RETURN_KEY2] = "command[%s] execution error: %s" % (cmd, log1)
        RET[RETURN_KEY1] = -1
    else:
        RET[RETURN_KEY2] = log1
        RET[RETURN_KEY1] = 0
    if args.operations != None:
        print_sonic(RET)
    return RET

def bmc_get_ddr_info():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    cmd = "cat /proc/meminfo "

    ret, log1 = log_os_system(cmd, 0)
    if ret != 0 or len(log1) <= 0:
        RET[RETURN_KEY2] = "command[%s] execution error: %s" % (cmd, log1)
        RET[RETURN_KEY1] = -1
    else:
        RET[RETURN_KEY2] = log1
        RET[RETURN_KEY1] = 0
    if args.operations != None:
        print_sonic(RET)
    return RET

def facebookbmc_get_emmc_info():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    cmd = "fdisk -l"
    cap_threshoud = {"high":9000,"low":7000}
    ret, log1 = log_os_system(cmd, 0)
    if ret != 0 or len(log1) <= 0:
        print_choose("command[%s] execution error: %s" % (cmd, log1))
        RET[RETURN_KEY1] = -1
    else:
        data = re.findall(".*/dev/mmcblk0:\s+(\d*\.?\d+)\s+GiB.*",log1)
        if len(data) != 1:
            print_choose("Failed to get capacity information")
            RET[RETURN_KEY1] = -1
        else:
            msg = ("EMMC  capacity: %s G"%(data[0]))
            print_choose(msg)
            RET[RETURN_KEY1] = 0

    print_sonic(RET)
    return RET


def bmc_get_emmc_info():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    cmd = "fdisk -l"
    cap_threshoud = {"high":9000,"low":7000}

    ret, log1 = log_os_system(cmd, 0)
    if ret != 0 or len(log1) <= 0:
        RET[RETURN_KEY2] = "command[%s] execution error: %s" % (cmd, log1)
        RET[RETURN_KEY1] = -1
    else:
        data = re.findall(".*/dev/mmcblk0:\s+(\d+)\s+MB.*",log1)
        print(data)
        if len(data) != 1:
            RET[RETURN_KEY2] = "Failed to get capacity information"
            RET[RETURN_KEY1] = -1
        else:
            cap = int(data[0])
            RET[RETURN_KEY2] = "EMMC capacity: %d MB"%(cap)
            if cap in range(cap_threshoud["low"], cap_threshoud["high"]):
                RET[RETURN_KEY1] = 0
            else:
                RET[RETURN_KEY1] = -1

    if args.operations != None:
       print_sonic(RET)
    return RET

def bmc_test_emmc_check_occupancy_rate():
    errtotal = 0
    sign = "%"
    RET = {RETURN_KEY1 : -1, RETURN_KEY2 : ""}
    cmd1 = "df |grep '/dev/mmcblk*' | awk 'NR==1{print}' | awk '{print $3}'"
    cmd2 = "df |grep '/dev/mmcblk*' | awk 'NR==1{print}' | awk '{print $2}'"
    cmd3 = "df |grep '/dev/mmcblk*' | awk 'NR==2{print}' | awk '{print $3}'"
    cmd4 = "df |grep '/dev/mmcblk*' | awk 'NR==2{print}' | awk '{print $2}'"
    cmd5 = "df |grep '/dev/mmcblk*' | grep '/var' | awk '{print $3}'"
    cmd6 = "df |grep '/dev/mmcblk*' | grep '/var' | awk '{print $2}'"

    ret1, emmc1_used = log_os_system(cmd1, 0)
    if ret1 != 0 or len(emmc1_used) <= 0:
        print_choose("command[%s] execution error: %s" % (cmd1, emmc1_used))
        errtotal -= 1

    ret2, emmc1_total = log_os_system(cmd2, 0)
    if ret2 != 0 or len(emmc1_total) <= 0:
        print_choose("command[%s] execution error: %s" % (cmd2, emmc1_used))
        errtotal -= 1

    ret3, emmc2_used = log_os_system(cmd3, 0)
    if ret3 != 0:
        print_choose("command[%s] execution error: %s" % (cmd4, emmc2_used))
        errtotal -= 1

    ret4, emmc2_total = log_os_system(cmd4, 0)
    if ret4 != 0:
        print_choose("command[%s] execution error: %s" % (cmd4, emmc2_total))
        errtotal -= 1

    ret5, var_log_used = log_os_system(cmd5, 0)
    if ret5 != 0 or len(var_log_used) <= 0:
        print_choose("command[%s] execution error: %s" % (cmd5, var_log_used))
        errtotal -= 1

    ret6, var_log_total = log_os_system(cmd6, 0)
    if ret6 != 0 or len(var_log_total) <= 0:
        print_choose("command[%s] execution error: %s" % (cmd6, var_log_total))
        errtotal -= 1

    if errtotal < 0:
        RET[RETURN_KEY1] = -1
    else:
        if len(emmc2_used) <= 0:
            emmc_used_total = float(emmc1_used) / float(emmc1_total) * 100
        else:
            emmc_used_total = (float(emmc1_used) + float(emmc2_used)) / (float(emmc1_total) + float(emmc2_total)) * 100
        var_log_used_total = float(var_log_used) / float(var_log_total) * 100
        print_choose("emmc     usage: %.1f%s"%(emmc_used_total, sign))
        print_choose("/var/log usage: %.1f%s"%(var_log_used_total, sign ))
        if emmc_used_total > 40 or var_log_used_total > 40:
            print_choose("There are items that use more than 40%")
            RET[RETURN_KEY1] = -1
        else:
            RET[RETURN_KEY1] = 0
    print_sonic(RET)
    return RET


#暂时先写死 hwmon 的index
#def find_hwmon_index():
#    cmd = "ls /sys/class/hwmon/ -l"
#    dic_rt = {};
#    ret, log1 = log_os_system(cmd, 0)
#    print log1
#    if ret == 0 and len(log1):
#        log1 = log1.lstrip()
#        arr = log1.split("\n")
#        for arri in arr:
#           print arri
#           line_temp = re.search("(\d+)\-00(\d\w)/hwmon\/hwmon(\d+)",arri)
#           print "@@@"
#           if line_temp is None:
#              continue
#           bus = line_temp.group(1)
#           addr = line_temp.group(2)
#           index = int(line_temp.group(3))
#           dic_rt[index] = {"bus":bus,"addr":addr}
#        print dic_rt
#        return dic_rt
#    return None

def get_dcdc_1_info(dev):
    #先确认正确的地址
    cmd = "cat /sys/class/hwmon/*/%s"%(dev["file"])

    ret, log = log_os_system(cmd, 0)
    if "can't open" in log:
        return -1;
    else:
        return int(log)

def readsysfs(location):
    try:
        locations = glob.glob(location)
        with open(locations[0], 'r') as fd1:
            val = fd1.read()
    except Exception as e:
        return False, (str(e)+" location[%s]" % location)
    return True, val

def rji2cgetWord(bus, devno, address):
    command_line = "i2cget -f -y %d 0x%02x 0x%02x w" % (bus, devno, address)
    retrytime = 3
    ret_t = ""
    for i in range(retrytime):
        ret, ret_t = log_os_system(command_line, 0)
        if ret == 0:
            return True, ret_t
    return False, ret_t

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


def bmc_get_psu_pmbus_info():
    RET = {RETURN_KEY1: 0, RETURN_KEY2: ""}
    totalerr = 0
    errmsg = ""
    resultval = []
    val_dict = {}

    items = PSU_PMBUS_LIST
    if items is None:
        RET[RETURN_KEY1] = -999
        RET[RETURN_KEY2] = 'config error'
        return RET

    header = ['Sensor', 'State', 'Value', 'LowThd', 'HighThd']
    line = ['-----------------', '-------', '---------', '-------------', '--------------']
    formatstr = "    %-20s %-10s %-10s %-20s %-20s"
    print_choose(formatstr%(header[0], header[1], header[2], header[3], header[4]))
    print_choose(formatstr%(line[0], line[1], line[2], line[3], line[4]))

    #get dcdcsensor value
    for item in items:
        Sensor = item.get('Sensor', None)
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
        elif gettype == "calc_power":
            voltage = val_dict.get(item['voltage'])
            current = val_dict.get(item['current'])
            if voltage is None or current is None:
                ret = False
            else:
                ret = True
                val = float(voltage) * float(current)
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
                min = eval(format % min)
                max = eval(format % max)
            else:
                val_tmp = int(val, 10)
            if min < val_tmp < max:
                statusmsg = "OK"
            else:
                totalerr -= 1
                statusmsg = 'Not OK'
            val_dict[Sensor] = val_tmp
        else:
            totalerr -= 1
            statusmsg = 'Not OK'
            val_tmp = "fail "
            Unit = ""
            log_debug("get psu value fail %s" % Sensor)
        print_choose(formatstr % (Sensor, statusmsg, "%s%s"%(val_tmp, Unit), "%s%s"%(min, Unit), "%s%s"%(max, Unit)))
        #resultval.append([Sensor, Address, statusmsg, "%s%s"%(val_tmp, Unit), "%s%s"%(min, Unit), "%s%s"%(max, Unit)])

    #打印
    #header = ['Sensor', 'Address', 'State', 'Value', 'CriticalLow', 'CriticalHigh']
    #result = tabulate(resultval, header, tablefmt='simple')
    #RJPRINT(result)

    RET[RETURN_KEY1] = totalerr
    print_sonic(RET)
    return RET



    '''
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    totalerr = 0
    #hwmon_info = find_hwmon_index();

    #if hwmon_info == None:
    #    RET[RETURN_KEY2] = "No hwmon file"
    #    return RET
    rt_str = ""
    for dev in DCDC_DEVICE:

           value = get_dcdc_1_info(dev)
           if value == -1:
               result = "读取失败"
               totalerr -= 1
           else :
                if "curr" in dev["file"]:
                   result = "%-10d%-10s"%(value," mA")
                else :
                   result = "%-10d%-10s"%(value," mV")
           rt_str = "%-40s%s"%(dev["name"],result)
           print_choose(rt_str)

    if totalerr < 0:
        RET[RETURN_KEY1] = -1
    if args.operations != None:
       print_sonic(RET)
    return RET
    '''


def bmc_get_temp_info():
    RET = {RETURN_KEY1: 0, RETURN_KEY2: ""}
    totalerr = 0
    errmsg = ""
    resultval = []

    items = TEMPS_LIST
    if items is None:
        RET[RETURN_KEY1] = -999
        RET[RETURN_KEY2] = 'config error'
        return RET

    header = ['Sensor', 'InputName', 'State', 'Value', 'LowThd', 'HighThd']
    line = ['-----------------','-------------', '-------', '---------', '---------', '---------']
    formatstr = "    %-20s %-15s %-10s %-10s %-10s %-10s"
    print_choose(formatstr%(header[0], header[1], header[2], header[3], header[4], header[5]))
    print_choose(formatstr%(line[0], line[1], line[2], line[3], line[4], line[5]))

    #get dcdcsensor value
    for item in items:
        Sensor = item.get('Sensor', None)
        InputName = item.get('InputName', None)
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
                min = eval(format % min)
                max = eval(format % max)
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
            log_debug("get temp value fail %s" % Sensor)
        print_choose(formatstr % (Sensor, InputName, statusmsg, "%s%s"%(val_tmp, Unit), "%s%s"%(min, Unit), "%s%s"%(max, Unit)))
        #resultval.append([Sensor, Address, statusmsg, "%s%s"%(val_tmp, Unit), "%s%s"%(min, Unit), "%s%s"%(max, Unit)])

    #打印
    #header = ['Sensor', 'Address', 'State', 'Value', 'CriticalLow', 'CriticalHigh']
    #result = tabulate(resultval, header, tablefmt='simple')
    #RJPRINT(result)

    RET[RETURN_KEY1] = totalerr
    print_sonic(RET)
    return RET



    '''
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    totalerr = 0
    #hwmon_info = find_hwmon_index();

    #if hwmon_info == None:
    #    RET[RETURN_KEY2] = "No hwmon file"
    #    return RET
    rt_str = ""
    for dev in DCDC_DEVICE:

           value = get_dcdc_1_info(dev)
           if value == -1:
               result = "读取失败"
               totalerr -= 1
           else :
                if "curr" in dev["file"]:
                   result = "%-10d%-10s"%(value," mA")
                else :
                   result = "%-10d%-10s"%(value," mV")
           rt_str = "%-40s%s"%(dev["name"],result)
           print_choose(rt_str)

    if totalerr < 0:
        RET[RETURN_KEY1] = -1
    if args.operations != None:
       print_sonic(RET)
    return RET
    '''


def bmc_get_dcdc_info():
    RET = {RETURN_KEY1: 0, RETURN_KEY2: ""}
    totalerr = 0
    errmsg = ""
    resultval = []

    items = DCDC_DEVICE
    if items is None:
        RET[RETURN_KEY1] = -999
        RET[RETURN_KEY2] = 'config error'
        return RET

    header = ['Sensor', 'Address', 'State', 'Value', 'CriticalLow', 'CriticalHigh']
    line = ['-----------------','-----------', '-------', '---------', '-------------', '--------------']
    formatstr = "    %-20s %-15s %-10s %-10s %-20s %-20s"
    print_choose(formatstr%(header[0], header[1], header[2], header[3], header[4], header[5]))
    print_choose(formatstr%(line[0], line[1], line[2], line[3], line[4], line[5]))

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
                min = eval(format % min)
                max = eval(format % max)
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
        print_choose(formatstr % (Sensor, Address, statusmsg, "%s%s"%(val_tmp, Unit), "%s%s"%(min, Unit), "%s%s"%(max, Unit)))
        #resultval.append([Sensor, Address, statusmsg, "%s%s"%(val_tmp, Unit), "%s%s"%(min, Unit), "%s%s"%(max, Unit)])

    #打印
    #header = ['Sensor', 'Address', 'State', 'Value', 'CriticalLow', 'CriticalHigh']
    #result = tabulate(resultval, header, tablefmt='simple')
    #RJPRINT(result)

    RET[RETURN_KEY1] = totalerr
    print_sonic(RET)
    return RET



    '''
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    totalerr = 0
    #hwmon_info = find_hwmon_index();

    #if hwmon_info == None:
    #    RET[RETURN_KEY2] = "No hwmon file"
    #    return RET
    rt_str = ""
    for dev in DCDC_DEVICE:

           value = get_dcdc_1_info(dev)
           if value == -1:
               result = "读取失败"
               totalerr -= 1
           else :
                if "curr" in dev["file"]:
                   result = "%-10d%-10s"%(value," mA")
                else :
                   result = "%-10d%-10s"%(value," mV")
           rt_str = "%-40s%s"%(dev["name"],result)
           print_choose(rt_str)

    if totalerr < 0:
        RET[RETURN_KEY1] = -1
    if args.operations != None:
       print_sonic(RET)
    return RET
    '''

def bmc_test_peci():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    ret, log = log_os_system("dfd_debug peci_pkgcfg_rd 0 0", 0)
    if ret or "63 06 05 00" not in log:
        RET[RETURN_KEY2] = "通过PECI访问CPU失败, %s"%log
        RET[RETURN_KEY1] = -1
    else:
        RET[RETURN_KEY2] =  "通过PECI访问CPU成功"

    if args.operations != None:
        print_sonic(RET)
    return RET

def bmc_test_peci_new():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    ret, log = log_os_system("dfd_debug peci_pkgcfg_rd 0 0", 0)
    if ret or CPU_ID not in log:
        RET[RETURN_KEY2] = "通过PECI访问CPU失败, %s"%log
        RET[RETURN_KEY1] = -1
    else:
        RET[RETURN_KEY2] =  "通过PECI访问CPU成功"

    if args.operations != None:
        print_sonic(RET)
    return RET

def bmc_test_SML0():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    ret, log = rji2cget(1,0x16,0)

    if "Error: Read failed" in log:
        RET[RETURN_KEY2] = "SML0 测试失败"
        RET[RETURN_KEY1] = -1;
    else:
       RET[RETURN_KEY2] = "SML0 测试成功,读到寄存器0x00的值为%s"%log
    if args.operations != None:
        print_sonic(RET)
    return RET

def bmc_reset_loopback(param):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    val_t = json.loads(param)
    speed = val_t.get('speed',None)
    cmdstr = ""
    #print speed
    if speed is not None:
        cmdstr = MGMT_LOOPBACK.get(speed)
    #print cmdstr
    ret, log = log_os_system(cmdstr, 0)
    if ret != 0:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = '重置设备失败%s' % speed
        return RET
    time.sleep(1)
    return RET

def get_frame_count(iface ='eth0'):
    txcmd = "ifconfig %s |grep -E 'TX packets'" % iface
    rxcmd = "ifconfig %s |grep -E 'RX packets'" % iface
    ret, txlog = log_os_system(txcmd, 0)
    ret, rxlog = log_os_system(rxcmd, 0)
    tx = re.findall(r"\d+\.?\d*",txlog)[0]
    rx = re.findall(r"\d+\.?\d*",rxlog)[0]
    return int(rx), int(tx)

def bmc_check_loopback(param):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    val_t = json.loads(param)
    packetcount = val_t.get('packetcount',None)
    iface = val_t.get('iface',None)
    pktthread = val_t.get('pktpassthread',None)
    cmdstr = "ftg100_tool tx %d" % packetcount
    RXstart,TXstart = get_frame_count()

    ret, log = log_os_system(cmdstr, 0)
    if ret !=0:
        totalerr -= 1
        RET[RETURN_KEY1] = totalerr
        RET[RETURN_KEY2] = '发包失败%s' % log
        return RET
    RXend,TXend = get_frame_count()

    Tx_total = TXend - TXstart
    Rx_total = RXend - RXstart
    if Tx_total ==0:
        totalerr -= 1
        RET[RETURN_KEY2] = '计算包错误%s  Rx_total:%d  Tx_total:%d' % (log,Rx_total,Tx_total)
    packet_rate = float(Rx_total)/float(Tx_total)
    if packet_rate >= pktthread:
         return RET
    else:
        totalerr -= 1
        RET[RETURN_KEY1] = totalerr
        RET[RETURN_KEY2] = '计算包错误%s  Rx_total:%d  Tx_total:%d' % (log,Rx_total,Tx_total)
    return RET

def bmc_set_loopback(param):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    print(param)
    totalerr = 0
    val_t = json.loads(param)
    speed = val_t.get('speed',None)
    cmdstr = ""

    if speed is not None:
        cmdstr = MGMT_LOOPBACK.get(speed)
    ret, log = log_os_system(cmdstr, 0)
    if ret != 0:
        print(log)
        totalerr -= 1
        RET[RETURN_KEY1] = totalerr
        RET[RETURN_KEY2] = '设置%s回环失败%d' % (speed, totalerr)
        return RET
    time.sleep(2)
    check_str = MGMT_LOOPBACK.get('check')
    #get_sysfs_value(check_str)
    ret , log = log_os_system(check_str, 0)
    if ret != 0 or log[-1] != 'd':
        totalerr -= 1
        RET[RETURN_KEY1] = totalerr
        RET[RETURN_KEY2] = '设置%s回环失败%d' % (speed, totalerr)
        return RET
    return RET

def bmc_test_MDIO():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    errtotal = 0

    MDIO_dev_dict = {
        "BMC-54616 ":["11"],
        "MGMT-54616":["18"],
        "5387      ":["00","01","02","03","04","05","06","07"],
    }
    if MDIO_DEV_DICT is not None:
        MDIO_dev_dict = MDIO_DEV_DICT

    for dev in list(MDIO_dev_dict.keys()):
        check_log = ""
        dev_errtotal = 0
        for i in MDIO_dev_dict[dev]:
            cmd = "cat /sys/bus/mdio_bus/devices/1e680000.ethernet--1\:%s/hw_test02" % i
            ret, log = log_os_system(cmd, 0)
            if ret or "0xffff" in log or "0x   0" in log:
                check_log =  i + ": FAILD\n"
                dev_errtotal -= 1
            else:
                check_log = i + ": PASS\n"
        errtotal += dev_errtotal
        if dev_errtotal < 0:
            print_choose(dev + " : FAILED")
            print_choose(check_log) #打印详细的错误信息
        else:
            print_choose(dev + " : PASS")

    if errtotal < 0:
      RET[RETURN_KEY1] = -1;
    print_sonic(RET)
    return RET

def bmc_test_MDIO_stress():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 :""}
    totalerr = 0
    test_times = 10
    for i in range(0, test_times):
       print_choose("\n\n第 %d/%d 次测试"%(i+1, test_times))
       RET1 = bmc_test_MDIO()
       totalerr += RET1[RETURN_KEY1]
    if totalerr < 0:
       RET[RETURN_KEY1] = -1
    print_sonic(RET)
    return RET

def bmc_test_get_fan_present():
    errtotal = 0
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    ret, log = log_os_system("cat /sys/bus/i2c/devices/8-000d/hwmon/hwmon*/fan_present", 0)
    if ret or "can't open" in log:
       RET[RETURN_KEY1] = -1
       print_choose( "读取在位信息失败")
       print_sonic(RET)
       return RET
    fan_present = int(log, 16)
    for i in range(0,5):
        if i == 4 and "as13-32h" != Device_branch:
           continue
        if (fan_present & (1 << i)):
            print_choose("风扇%d"%(i+1) + ":不在位")
            errtotal -= 1
        else:
            print_choose("风扇%d"%(i+1) + ":在位")

    if errtotal < 0:
      RET[RETURN_KEY1] = -1;
    if args.operations != None:
        print_sonic(RET)
    return RET

def bmc_test_get_fan_speed():
    errtotal = 0
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    ret, log = log_os_system("cat /sys/bus/i2c/devices/8-000d/hwmon/hwmon*/fan_present", 0)
    if ret or "can't open" in log:
       RET[RETURN_KEY1] = -1
       print_choose("读取在位信息失败")
       print_sonic(RET)
       return RET
    fan_present = int(log, 16)

    for i in range(0,5):
        if i == 4 and "as13-32h" != Device_branch:
           continue
        if (fan_present & (1 << i)):
            print_choose("风扇%d"%(i+1) + ":不在位")
            errtotal -= 1
            continue
        else:
            cmd1 = "cat /sys/bus/i2c/devices/8-000d/hwmon/hwmon*/fan%d1_input"%(i+1)
            cmd2 = "cat /sys/bus/i2c/devices/8-000d/hwmon/hwmon*/fan%d2_input"%(i+1)
            ret, log = log_os_system(cmd1, 0)
            if ret or "can't open" in log:
               print_choose("风扇%d-子风扇1"%(i+1) +":读取转速信息失败")
               errtotal -= 1
            else :
                print_choose("风扇%d-子风扇1"%(i+1) +":%sRPM"%log)

            ret, log = log_os_system(cmd2, 0)
            if ret or "can't open" in log:
               print_choose("风扇%d-子风扇2"%(i+1) +":读取转速信息失败")
               errtotal -= 1
            else :
                print_choose("风扇%d-子风扇2"%(i+1) +":%sRPM"%log)

    if errtotal < 0:
      RET[RETURN_KEY1] = -1;
    print_sonic(RET)
    return RET

def bmc_test_set_fan_speed( level , finlreset = True):
    errtotal = 0
    no_fan_present = False
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    ret, log = log_os_system("cat /sys/bus/i2c/devices/8-000d/hwmon/hwmon*/fan_present", 0)
    if ret or "can't open" in log:
       RET[RETURN_KEY1] = -1
       print_choose("读取在位信息失败")
       print_sonic(RET)
       return RET
    fan_present = int(log, 16)
    print_choose("设置风扇转速")

    try:
        rji2cset(FAN_SPEED["bus"], 0x0d, 0x51, 0) #关闭风扇狗
        log_os_system("systemctl stop dev-monitor",0)#kill dev_monitor

        for i in range(0,5):
            if  "as13-32h" != Device_branch:
                if (fan_present & (0x0f)) == 0x0f:
                    no_fan_present = True
                if i == 4 :
                    continue
            else:
                if (fan_present & (0x1f)) == 0x1f:
                    no_fan_present = True

            if (fan_present & (1 << i)):
                print_choose("    风扇%d"%(i+1) + ":不在位")
                errtotal -= 1
                continue
            else:
                fan_level = FAN_SPEED["speedlevel"][level]
                fan_dev = FAN_SPEED["device"][i]
                ret, log = rji2cset(FAN_SPEED["bus"], FAN_SPEED["addr"], fan_dev["reg"],fan_level["value"])

                if ret or "can't open" in log:
                   print_choose("    风扇%d:设置转速等级失败"%(i+1))
                   errtotal -= 1
                else :
                    print_choose("    风扇%d 设置转速等级为 %s"%((i+1),fan_level["value"]))

        if no_fan_present:
            pass
        else:
            time.sleep(FAN_SPEED["waittime"])#等待风扇到达设置速度
            print_choose("读取风扇转速")
            for i in range(0,5):
                if i == 4 and "as13-32h" != Device_branch:
                   continue
                if (fan_present & (1 << i)):
                    print_choose("    风扇%d"%(i+1) + ":不在位")
                    errtotal -= 1
                    continue
                else:
                    cmd1 = "cat /sys/bus/i2c/devices/8-000d/hwmon/hwmon*/fan%d1_input"%(i+1)
                    cmd2 = "cat /sys/bus/i2c/devices/8-000d/hwmon/hwmon*/fan%d2_input"%(i+1)
                    ret, log = log_os_system(cmd1, 0)
                    if ret or "can't open" in log:
                       print_choose("    风扇%d-子风扇1"%(i+1) +":读取转速信息失败")
                       errtotal -= 1
                    else :
                        if (int(log) < fan_level["low_threshhold"] or int(log) > fan_level["high_threshhold"] ):
                            print_choose("    风扇%d-子风扇1"%(i+1) +":%sRPM,不在正常阈值范围内"%log)
                            errtotal -= 1
                        else:
                            print_choose("    风扇%d-子风扇1"%(i+1) +":%sRPM"%log)

                    ret, log = log_os_system(cmd2, 0)
                    if ret or "can't open" in log:
                       print_choose("    风扇%d-子风扇2"%(i+1) +":读取转速信息失败")
                       errtotal -= 1
                    else :
                        if (int(log) < fan_level["low_threshhold"] or int(log) > fan_level["high_threshhold"] ):
                            print_choose("    风扇%d-子风扇2"%(i+1) +":%sRPM,不在正常阈值范围内"%log)
                            errtotal -= 1
                        else:
                            print_choose("    风扇%d-子风扇2"%(i+1) +":%sRPM"%log)
    except Exception as e:
        errtotal -= 1
        RET[RETURN_KEY2] = e
    finally:
        if (finlreset == True):
            log_os_system("systemctl start dev-monitor",0)
            rji2cset(FAN_SPEED["bus"], 0x0d, 0x51, 1) #开启风扇狗
    if errtotal < 0:
      RET[RETURN_KEY1] = -1;
    print_sonic(RET)
    return RET

def bmc_test_set_fan_speed_high_without_reset():
    return bmc_test_set_fan_speed("high", False)

def bmc_test_set_fan_speed_reset():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    log_os_system("systemctl restart dev-monitor",0)
    rji2cset(FAN_SPEED["bus"], 0x0d, 0x51, 1) #开启风扇狗
    print_sonic(RET)
    return RET

def bmc_test_set_fan_speed_high():
    return bmc_test_set_fan_speed("high")

def bmc_test_set_fan_speed_middle():
    return bmc_test_set_fan_speed("middle")

def bmc_test_set_fan_speed_low():
    return bmc_test_set_fan_speed("low")
'''
def bmc_test_get_psu_rfu_info():
   RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
   PSUs =  PSU_INFO[Device_branch]
   errtotal = 0
   i = 0;

   cmd = "cat /sys/class/hwmon/hwmon*/psu_status*"
   ret, log_present = log_os_system(cmd, 0)
   if ret or "Error" in log_present:
       print_choose("读取PSU在位信息失败")
       RET[RETURN_KEY1] = -1;
       print_sonic(RET)
       return RET
   log_present, times = re.subn("(\d{2})\n?\r?(\d{2})", "\g<2>\g<1>", log_present)
   psu_status = int(log_present, 16)

   for psu in PSUs:
        try:
            i += 1
            print_choose("\nPSU%d:"%(i))
            psu_present = 1 << (i-1)*4
            if psu_status & psu_present:
                print_choose("不在位")
                errtotal -= 1
                continue

            filename = "/sys/bus/i2c/devices/%d-00%x/eeprom"%(psu["bus"],psu["e2addr"])
            ret = E2Util.decodeBinName(filename)
            head = ["key","value"]
            if ret!= None:
                for key,values in ret.productInfoArea.todict().items():
                    print_choose( "%-25s: %s "% (key,values) )
            else:
               print_choose("读取e2信息失败")
               errtotal -= 1
        except E2Exception as e:
            errtotal -= 1
            print_choose(e.message)


   if errtotal < 0:
      RET[RETURN_KEY1] = -1;
   if args.operations != None:
        print_sonic(RET)
   return RET
'''
def bmc_test_get_psu_info():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    PSUs =  PSU_INFO[Device_branch]
    errtotal = 0
    i = 0;
    dic_k = {"curr2_input":"输入电流",
             "curr1_input":"输出电流",
             "in2_input":"输入电压",
             "in1_input":"输出电压",
             "power1_input":"输出功率",
             "power2_input":"输入功率",
            }

    cmd = "cat /sys/class/hwmon/hwmon*/psu_status*"
    ret, log_present = log_os_system(cmd, 0)
    if ret or "Error" in log_present:
        print_choose("读取PSU在位信息失败")
        RET[RETURN_KEY1] = -1;
        print_sonic(RET)
        return RET
    log_present, times = re.subn("(\d{2})\n?\r?(\d{2})", "\g<2>\g<1>", log_present)
    psu_status = int(log_present, 16)

    for psu in PSUs:
        i += 1
        print_choose("PSU%d"%(i) +":")
        psu_present = 1 << (i-1)*4
        if psu_status & psu_present:
            print_choose("不在位")
            errtotal -= 1
            continue

        for attr_key in psu["attrs"]:
            cmd = "cat /sys/bus/i2c/devices/%d-00%x/hwmon/hwmon*/%s"%(psu["bus"],psu["addr"],attr_key)
            ret, log = log_os_system(cmd, 0)
            if ret or "can't open" in log:
               print_choose("读取信息失败")
               errtotal -= 1
            else:
               print_choose("%-20s %-10s %-10s"%(dic_k[attr_key],log,psu["attrs"][attr_key]))

    if errtotal < 0:
        RET[RETURN_KEY1] = -1;
    if args.operations != None:
        print_sonic(RET)
    return RET

def bmc_test_get_psu_present():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    PSUs =  PSU_INFO[Device_branch]
    errtotal = 0
    i = 0;
    cmd = "cat /sys/class/hwmon/hwmon*/psu_status*"
    ret, log = log_os_system(cmd, 0)
    if ret or "Error" in log:
        print_choose("读取PSU在位信息失败")
        errtotal -= 1
    else:
        log, times = re.subn("(\d{2})\n?\r?(\d{2})", "\g<2>\g<1>", log)
        for psu in PSUs:
            i += 1
            psu_present = 1 << (i-1)*4
            psu_status = int(log, 16)
            if psu_status & psu_present:
                print_choose("PSU%d"%(i) +": 不在位")
                errtotal -= 1
            else:
                print_choose("PSU%d"%(i) +": 在位")
    if errtotal < 0:
        RET[RETURN_KEY1] = -1;
    if args.operations != None:
         print_sonic(RET)
    return RET

def bmc_test_i2c_scan():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    #PSUs =  PSU_INFO[Device_branch]
    errtotal = 0
    for i2cdev in I2C_SCAN_LIST:
        STATE = "FAILED"
        type = i2cdev.get("gettype", None)
        if type == "I2C_32":
            ret, log = rji2cget_32bit(i2cdev["bus"], i2cdev["addr"], "0x00 0x00 0x00 0x00")
        else:
            ret, log = rji2cget(i2cdev["bus"], i2cdev["addr"], 0)
        if ret or "Error" in log:
            STATE = "FAILED"
            errtotal -= 1
        else:
            STATE = "PASS"
        formatstr = "    %%-%ds %%-10s"%((40+wide_chars(i2cdev['name'])))
        print_choose(formatstr%(i2cdev['name'],STATE))
    if errtotal < 0:
        RET[RETURN_KEY1] = -1
    print_sonic(RET)
    return RET

def bmc_test_i2c_stress():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    #PSUs =  PSU_INFO[Device_branch]
    keep_str = ""
    scan_list = I2C_SCAN_LIST
    if I2C_SCAN_TIMES is None:
        test_times = 100
    else:
        test_times = I2C_SCAN_TIMES.get("test_times", 100)
    errtotal = 0
    for i in range(0, test_times +1):
        err_flag = False
        for i2cdev in scan_list:
            if i == 0:
                formatstr = "    %%-%ds %%-10s\n" % ((40 + wide_chars(i2cdev['name'])))
                keep_str += formatstr%(i2cdev['name'], "PASS")
                continue
            type = i2cdev.get("gettype", None)
            if type == "I2C_32":
                ret, log = rji2cget_32bit(i2cdev["bus"], i2cdev["addr"], "0x00 0x00 0x00 0x00")
            else:
                ret, log = rji2cget(i2cdev["bus"], i2cdev["addr"], 0)
            if ret:
                formatstr = "    %%-%ds %%-10s\n" % ((40 + wide_chars(i2cdev['name'])))
                tmp = formatstr%(i2cdev['name'], "PASS")
                replace_str = formatstr%(i2cdev['name'], "FAILED")
                keep_str = keep_str.replace(tmp, replace_str)
                err_flag = True
        if err_flag:
            errtotal += 1
    keep_str += "BMC端I2C %d次压力测试\n" % test_times
    keep_str += "PASS TIMES：%d\n" % (test_times - errtotal)
    keep_str += "FAILED TIMES：%d\n" % errtotal
    if errtotal != 0:
        RET[RETURN_KEY1] = -1;
    print_choose(keep_str)
    print_sonic(RET)
    return RET

def led_test(LED_TYPE):
    LED_2_TEST = LED_INFO[LED_TYPE]
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    errtotal = 0
    for attr_key in LED_2_TEST["attrs"]:
        RET = bmc_set_led(LED_TYPE, attr_key)
        if RET[RETURN_KEY1] == -1:
            errtotal = -1
            break
        else:
            if get_led_inputcheck(LED_2_TEST["name"],attr_key):
                print("yes")
            else:
                print("no")
                errtotal -= 1
    if errtotal < 0:
        RET[RETURN_KEY1] = -1;
    if args.operations != None:
        print_sonic(RET)
    return RET

def bmc_led_control(ctrl):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    errtotal = 0
    if "start" in ctrl:
        cmd = "systemctl start dev-monitor"
        ret, log = log_os_system(cmd, 0)
        rji2cset(FAN_SPEED["bus"], 0x0d, 0x51, 1) #开启风扇狗
    else:
        rji2cset(FAN_SPEED["bus"], 0x0d, 0x51, 0) #关闭风扇狗
        cmd = "systemctl stop dev-monitor"
        ret, log = log_os_system(cmd, 0)
    if errtotal < 0:
        RET[RETURN_KEY1] = -1
    if args.operations != None:
        print_sonic(RET)
    return RET

def bmc_set_led(LED_TYPE, led_state):
    LED_2_TEST = LED_INFO[LED_TYPE]
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    errtotal = 0
    for led in LED_2_TEST["device"]:
        #128面板 风扇灯 补丁
        if "128" in Device_branch and LED_2_TEST["bus"] == 0 and LED_2_TEST["addr"] == 0x0d and led["reg"] == 0x74:
            ret, log = rji2cset(8, 0x0d, 0x40, LED_2_TEST["attrs"][led_state])
        else:
            ret, log = rji2cset(LED_2_TEST["bus"],LED_2_TEST["addr"],led["reg"],LED_2_TEST["attrs"][led_state])
        if ret or "can't open" in log:
           print_choose("设置失败       FAILD")
           errtotal -= 1
    if errtotal < 0:
        RET[RETURN_KEY1] = -1;
    if args.operations != None:
        print_sonic(RET)
    return RET

def bmc_test_cpu_gpio():
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    cmd = ""
    ret, log = log_os_system("which firmware_upgrade_ispvme", 0)
    if len(log):
        cmd = "firmware_upgrade_ispvme cpld test"
    else:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "no firmware_upgrade_ispvme cmd"
        print_sonic(RET)
        return RET

    ret, log = log_os_system(cmd, 0)
    if "PASS" not in log:
        RET[RETURN_KEY2] = log
        RET[RETURN_KEY1] = -1
    print_sonic(RET)
    return RET

def bmc_test_sysled():
   return led_test("sysleds")
def bmc_test_fanled():
   return led_test("fanleds")
def bmc_test_locationled():
   return led_test("location_led")
def bmc_test_bmcled():
   return led_test("bmc_led")

def bmc_test_led(param):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    dict_param = json.loads(param)
    bus = dict_param["bus"]
    dev_addr = dict_param["dev_addr"]
    reg_offset = dict_param["reg_offset"]
    value = dict_param["value"]
    ret,log = rji2cset(bus, dev_addr, reg_offset, value)
    if ret or "can't open" in log:
       RET[RETURN_KEY1] = -1
       RET[RETURN_KEY2] = "设置失败       FAILD"
    return RET

def bmc_get_e2_show_list():
    e2_dict = {}
    for e2 in list(E2_DEV.keys()):
        e2_dict[e2] = len(E2_DEV[e2]["list"])
    print(e2_dict)

def bmc_get_e2_set_list():
    e2_dict = {}
    for e2 in list(E2_DEV.keys()):
        if E2_DEV[e2]["canreset"]:
            e2_dict[e2] = len(E2_DEV[e2]["list"])
    print(e2_dict)

def e2_para_check(json_str):

    ret = {"status":"err","ret_info":"none"}
    try:
        if isinstance(json_str,str):
            req_json = eval(json_str)
        else:
            req_json = json_str
    except Exception as e:
        ret["ret_info"] = "invalid json %s"%(json_str)
        return ret

    e2type = req_json.get("e2type")
    index = req_json.get("index")
    if e2type == None or index == None:
        ret["ret_info"] = "invalid json"
        return ret
    if e2type not in E2_DEV:
        ret["ret_info"] = "invalid e2 type"
        return ret
    if index > ( len(E2_DEV[e2type]["list"]) - 1 ):
        ret["ret_info"] = "invalid e2 index"
        return ret
    ret["status"] = "ok"
    return ret

def bmc_write_e2_bin(json_str):
    json_str_list = eval(json_str)

    json_str = json_str_list[0]
    ret = e2_para_check(json_str)
    if ret["status"] == "err":
        print(ret)
        return

    req_json = json_str
    e2type = req_json.get("e2type")
    index = req_json.get("index")
    index_current=index
    bin_base64 = req_json.get("bin")
    bin = base64.b64decode(bin_base64)
    if not E2_DEV[e2type]["canreset"]:
        ret["ret_info"] = "%s can not be set"%(e2type)
        ret["status"] = "err"
        print(ret)
        return

    if bin == None or len(bin) != 256:
        ret["ret_info"] = "invalid bin"
        ret["status"] = "err"
        print(ret)
        return

    #bin_for_write ,times = re.subn("(\x00)+$","\x00",bin)
    bin_for_write = bin

    if("E2_FAN" == e2type):
        ret1,log = rji2cset(FAN_PROTECT["bus"], FAN_PROTECT["devno"],
                    FAN_PROTECT["addr"], FAN_PROTECT["open"])
        if ret1 or "Error" in log:
            ret["ret_info"] = "open fan e2 protect failed :%s"%(log)
            ret["status"] = "err"
            print(ret)
            return
    bus = E2_DEV[e2type]["list"][index]["bus"]
    addr = E2_DEV[e2type]["list"][index]["addr"]

    index = 0
    for item in bin_for_write:
        ret1,log = rji2cset(bus, addr, index, ord(item))
        if ret1 or "Error" in log:
            ret["ret_info"] = "write e2 failed :%s"%(log)
            ret["status"] = "err"
            print(ret)
            return
        index += 1

    if("E2_FAN" == e2type):
        ret1,log = rji2cset(FAN_PROTECT["bus"], FAN_PROTECT["devno"],
                    FAN_PROTECT["addr"], FAN_PROTECT["close"])
        if ret1 or "Error" in log:
            ret["ret_info"] = "close fan e2 protect failed :%s"%(log)
            ret["status"] = "err"
            print(ret)
            return

    if("E2_FAN"==e2type or "E2_PSU"==e2type or "E2_CARD"==e2type):
        cmd_reserv=E2_DEV[e2type]["restartserv"]%(index_current+1)
#        print cmd_reserv
        ret2,log=log_os_system(cmd_reserv,0)
        if ret2 !=0:
            ret["status"]="err"
            ret["ret_info"]="systemctl restart service failed"
            print(ret)
            return
    else:
        cmd_reserv=E2_DEV[e2type]["restartserv"]
#        print cmd_reserv
        ret2,log=log_os_system(cmd_reserv,0)
        if ret2 !=0:
            ret["status"]="err"
            ret["ret_info"]="systemctl restart service failed"
            print(ret)
            return
    ret["status"] = "ok"
    print(ret)
    return

def bmc_get_e2_bin(json_str):
    ret = e2_para_check(json_str)
    if ret["status"] == "err":
        print(ret)
        return

    req_json = eval(json_str)
    e2type = req_json.get("e2type")
    index = req_json.get("index")

    bus = E2_DEV[e2type]["list"][index]["bus"]
    addr = E2_DEV[e2type]["list"][index]["addr"]
    filename = "/sys/bus/i2c/devices/%d-00%02x/eeprom"%(bus,addr)
    retval = None
    try:
            #with open(filename, 'rb') as fd:
            #    retval = fd.read()
            #    #print retval
            #    ret["status"] = "ok"
            #    ret["ret_info"] = retval
            #    print ret
        list_reg = []

        for i in range(0,8) :
            ret1,log = rji2cget32(bus, addr, i*32)
            if ret1 or "Error" in log:
                ret["ret_info"] = "read e2 failed :%s"%(log)
                ret["status"] == "err"
                print(ret)
                return
            else:
                log,times = re.subn("32: ","",log)
                if times == 0:
                    ret["ret_info"] = "read e2 failed :%s"%(log)
                    ret["status"] == "err"
                    print(ret)
                    return
                else:
                    list_reg += log.split(" ")

        bin = chr(int(list_reg[0],16))

        for reg in list_reg[1:]:
            bin += chr(int(reg,16))
        ret["status"] = "ok"
        ret["ret_info"] = bin
        print(ret)

    except Exception as e:
        print(e)
        ret["status"] = "err"
        ret["ret_info"] = "get e2 failed "
        print(ret)
        return

def bmc_cpld_check():
    totalerr = 0
    result = ""
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    for cpld in CPLD_TEST:
        print_choose("%s read/write test:"%cpld["name"])
        for wr_byte in [0x5a,0xa5]:
            ret, log = rji2cset(cpld["bus"],cpld["addr"], cpld["test_reg"],wr_byte)
            if ret or "can't open" in log:
                RET[RETURN_KEY1] = -1
                print_choose(log)
            else:
                ret, log = rji2cget(cpld["bus"],cpld["addr"], cpld["test_reg"])
                if ret:
                    RET[RETURN_KEY1] = -1
                    print_choose(log)
                    continue
                rd_val = int(log,16)
                if wr_byte != rd_val:
                    RET[RETURN_KEY1] = -1
                    msg = "    Write value: 0x%x, Read back value: 0x%x"%(wr_byte, rd_val)
                    print_choose(msg)
                    print_choose("    FAILED")
                else:
                    msg = "    Write value: 0x%x, Read back value: 0x%x"%(wr_byte, rd_val)
                    print_choose(msg)
                    print_choose("    PASS")
        print_choose("\r\n")

    print_sonic(RET)
    return RET

def bmc_fpga_check():
    totalerr = 0
    result = ""
    RET = {RETURN_KEY1 : 0, RETURN_KEY2 : ""}
    for fpga in FPGA_TEST:
        print_choose("%s 读写测试:"%fpga["name"])
        for wr_byte in [0x5a,0xa5]:
            ret, log = rji2cset(fpga["bus"],fpga["addr"], fpga["test_reg"],wr_byte)
            if ret or "can't open" in log:
               RET[RETURN_KEY1] = -1
               print_choose(log)
            else:
               ret, log = rji2cget(fpga["bus"],fpga["addr"], fpga["test_reg"])
               str_get=log.replace('0x','')
               if "%x"%wr_byte not in log.lower():
                   RET[RETURN_KEY1] = -1
                   msg = "    写入%x，读出%s"%(wr_byte, str_get)
                   print_choose(msg)
                   print_choose("    FAILED")
               else:
                   msg = "    写入%x，读出%s"%(wr_byte, str_get)
                   print_choose(msg)
                   print_choose("    PASS")

    print_sonic(RET)
    return RET

def bmc_test_sol():

    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    cmd = "cat /var/log/obmc-console.log | grep SONiC |tail -n 10"
    ret, log = log_os_system(cmd, 0)
    log,time = re.subn("\x1b\S+","\n",log)
    if ret or len(log) == 0:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "SOL 测试失败:请确认BMC是否单独重启过"
    else:
        RET[RETURN_KEY1] = 0
        RET[RETURN_KEY2] = "SOL 测试成功,bmc通过SOL获得的sonic相关信息【展示部分信息】:\n%s" % log
    return RET

def bmc_log_os_system(param):
    '''BMC执行X86端发过来的shell命令'''
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    cmd = json.loads(param)
    ret, log = log_os_system(cmd, 0)
    if ret:
        RET[RETURN_KEY1] = -1
    else:
        RET[RETURN_KEY1] = 0
    RET[RETURN_KEY2] = log
    return RET

def bmc_get_version():

    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    cmd = "cat /etc/os-release "
    ret, log = log_os_system(cmd, 0)
    cmd1 = "bmc.sh view_flash"
    ret1, log1 = log_os_system(cmd1, 0)
    if  ret or len(log) == 0:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "获取BMC版本失败"
    else:
        RET[RETURN_KEY1] = 0
        RET[RETURN_KEY2] = "当前BMC为:%s\n%s" % (log1,log)
    return RET

def facebookbmc_get_version():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    tmp_t ={}
    cmd = "cat /etc/os-release"
    ret, log = log_os_system(cmd, 0)
    if  ret or len(log) == 0:
        print_choose("Failed to get BMC version")
        RET[RETURN_KEY1] = -1
        print_sonic(RET)
        return RET

    cmd1 = "boot_info.sh bmc"
    ret1, log1 = log_os_system(cmd1, 0)
    if  ret1 or len(log1) == 0:
        print_choose("Failed to get BMC flash status")
        RET[RETURN_KEY1] = -1
        print_sonic(RET)
        return RET

    if "Master" in log1:
        current_flash = "Master"
    else:
        current_flash = "Slave"
    RET[RETURN_KEY1] = 0
    print_choose("    Current BMC flash: %s" % current_flash)
    for line in log.strip().split("\n"):
        print_choose("    %s" % line)
        ver_list = line.split("=")
        tmp_t[ver_list[0]] = ver_list[1]
    bmc_version_check = TESTCASE.get('dev_info').get('bmc_version')
    if bmc_version_check is not None:
        if tmp_t.get("VERSION_ID") != bmc_version_check.strip():
            print_choose("    BMC version detection failed, device version: %s, expected version: %s" % (tmp_t.get("VERSION_ID"), bmc_version_check.strip()))
            RET[RETURN_KEY1] = -1
    print_sonic(RET)
    return RET


def bmc_get_flash():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    cmd = "bmc.sh view_flash"
    ret, log = log_os_system(cmd, 0)
    if ret or len(log) == 0:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "获取主备BMC状态失败,请检查BMC端bmc.sh view_flash是否正常"
    else:
        RET[RETURN_KEY1] = 0
        RET[RETURN_KEY2] = log
    return RET

def bmc_test_switch():

    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    cmd = "switch_bmc.sh"
    ret, log = log_os_system(cmd, 0)
    if  ret or len(log) == 0:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "主备BMC切换失败"
    else:
        RET[RETURN_KEY1] = 0
        RET[RETURN_KEY2] = log
    return RET

def CMD_dispatch():
    if args.operations == None:
        ApplicationInstance()
        start()
    elif args.json_str != None:
        eval(args.operations)(args.json_str)
    elif args.processid != None:
        eval(args.operations)(args.processid)
    elif args.ledattribute!= None and args.ledtype != None:
        eval(args.operations)(args.ledtype, args.ledattribute)
    elif args.action != None:
        eval(args.operations)(args.action)
    else:
        eval(args.operations)()

def test_bios_swtch(switch_mod):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    #切换BIOS
    if switch_mod == 0:    #切换至主BIOS
        switch_oplist = BIOS_TEST.get("switch_master",[])
    elif switch_mod == 1:    #切换至备份BIOS
        switch_oplist = BIOS_TEST.get("switch_slave",[])
    else:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "switch_mod error!"
        return RET
    for switch_opitem in switch_oplist:
        bus = switch_opitem["bus"]
        loc = switch_opitem["loc"]
        reg = switch_opitem["reg"]
        val = switch_opitem["val"]
        ret,log = rji2cset(bus,loc,reg,val)
        if ret or "can't open" in log:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "switch i2c write failed!"
            return RET
    return RET

def test_bmc_poweron_cpu():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    items = BIOS_TEST.get("cycle",{}).get("poweron",None)
    if items is None:
       RET[RETURN_KEY1] = -1
       RET[RETURN_KEY2] = "No poweron test case !"
    for item in items:
        bus = item["bus"]
        loc = item["loc"]
        reg = item["reg"]
        val = item["val"]
        ret,log = rji2cset(bus,loc,reg,val)
        if ret or "can't open" in log:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "Write i2c to poweron cpu failed!"
            return RET
    return RET

def test_bmc_poweroff_cpu():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    items = BIOS_TEST.get("cycle",{}).get("poweroff",None)
    if items is None:
       RET[RETURN_KEY1] = -1
       RET[RETURN_KEY2] = "No powerff test case !"
       return RET
    for item in items:
        bus = item["bus"]
        loc = item["loc"]
        reg = item["reg"]
        val = item["val"]
        ret,log = rji2cset(bus,loc,reg,val)
        if ret or "can't open" in log:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "Write i2c to poweroff cpu failed!"
            return RET
    return RET

def test_bmc_cycle_cpu():
    RET = test_bmc_poweroff_cpu()
    if RET[RETURN_KEY1] < 0:
        return RET
    time.sleep(BIOS_TEST.get("cycle",{}).get("sleep",3))
    RET = test_bmc_poweron_cpu()
    return RET

def test_bmc_reset_cpu():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    reboot_oplist = BIOS_TEST.get("reboot",[])
    for reboot_opitem in reboot_oplist:
        bus = reboot_opitem["bus"]
        loc = reboot_opitem["loc"]
        reg = reboot_opitem["reg"]
        val = reboot_opitem["val"]
        ret,log = rji2cset(bus,loc,reg,val)
        if ret or "can't open" in log:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "Write i2c to reset cpu failed!"
            return RET
    return RET

def test_config_usb0():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    #配置USB0
    ip = BMC_USB0.get("ip","1.1.1.2")
    netmask = BMC_USB0.get("netmask","255.255.255.0")
    cmd = "ifconfig usb0 %s netmask %s" % (ip,netmask)
    ret,log = log_os_system(cmd, 0)
    if ret :
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = "config usb0 failed!"
    return RET

def test_bmc_bios_switch(param):
    switch_mod = json.loads(param)
    #切换BIOS
    RET = test_bios_swtch(switch_mod)
    if RET[RETURN_KEY1] < 0 :
        return RET
    #重启X86
    RET = test_bmc_reset_cpu()
    if RET[RETURN_KEY1] < 0 :
        return RET
    time.sleep(60)
    #配置USB0
    RET = test_config_usb0()
    return RET


def bmc_get_sensor_info():
    '''获取BMC端各传感器信息'''
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    totalerr = 0
    errmsg = ""

    for item in BMC_SENSOR:
        name = item.get('name')
        unit = item.get('unit')
        location = item.get('location')
        try:
            locations = glob.glob(location)
            with open(locations[0], 'r') as fd1:
                retval = fd1.read()
            rval = float(retval)/1000
            RET[RETURN_KEY2] += ("  %-20s: %.2f %s\n" %(name, rval, unit))
        except Exception as e:
            totalerr -= 1
            errmsg = " %s %s" % (errmsg, str(e))
            RET[RETURN_KEY2]("  %-20s: error\n" %(name))
    RET[RETURN_KEY1] = totalerr
    return RET

def dumpValueByI2c(bus, loc):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : "", "value":[]}
    value = []
    for i in range(256):
        ret,val = rji2cget(bus, loc, i)
        if ret or "Error" in val:
           RET[RETURN_KEY1] = -1
           RET[RETURN_KEY2] = "Read E2 failed.bus:%d,loc=0x%x,addr=0x%x" % (bus, loc ,i)
           return RET
        value.append(int(val, 16))
    RET["value"] = value
    return RET

def test_bmc_read_eeprom(param):
    '''BMC端读取整片E2的内容'''
    index = 0
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : "", "value":[]}
    try:
        params = json.loads(param)
        loc = params["loc"]
        value_list = []
        ret,value = get_sysfs_value(loc)
        if ret == False:
            RET[RETURN_KEY1] = -1
            RET[RETURN_KEY2] = "read bmc fru eeprom error.loc:%s" % loc
        else:
            for i in value:
                value_list.append(ord(i))
            RET["value"] = value_list
    except Exception as e:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = str(e)
    return RET

def test_bmc_write_eeprom(param):
    '''BMC端写整片E2的内容'''
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    try:
        params = json.loads(param)
        loc = params.get("loc",None)
        ep_bus = params.get("ep_bus",None)
        ep_loc = params.get("ep_loc",None)
        ep_addr = params.get("ep_addr",None)
        ep_open = params.get("ep_open",None)
        ep_close = params.get("ep_close",None)
        rst_arr = params.get("value",[])
        eeprom = ""
        # 关闭写保护
        if ep_bus is not None:
            ret, log = rji2cset(ep_bus, ep_loc, ep_addr, ep_open)
            if ret or "can't open" in log:
                RET[RETURN_KEY1] = -1
                RET[RETURN_KEY2] = "Open BMC E2 protect failed!"
                return RET
        for i in rst_arr:
            eeprom += chr(i)
        for i in range(6):
            ret,log = write_sysfs_value(loc, eeprom)
            if ret == False:
                continue
            else:
                break
            time.sleep(1)
        RET[RETURN_KEY1] = ret
        RET[RETURN_KEY2] = log
    except Exception as e:
        RET[RETURN_KEY1] = -1
        RET[RETURN_KEY2] = str(e)
    finally:
        # 重新打开写保护
        if ep_bus is not None:
            ret, log = rji2cset(ep_bus, ep_loc, ep_addr, ep_close)
        else:
            pass
    return RET

def test_bmc_update_cpld_image(param):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    successtips="CPLD UPGRADE PASS!"
    dict_param = json.loads(param)
    slot =  dict_param["slot"]
    upgrade_name = dict_param["image"]
    ret, log = log_os_system("which firmware_upgrade_ispvme",0)
    if ret != 0 or len(log) <= 0:
        RJPRINT("未找到升级工具")
        return {RETURN_KEY1:-2, RETURN_KEY2:"Error, can't find firmware_upgrade_ispvme"}
    cmdstr = "%s %s cpld %d cpld"%(log,upgrade_name,slot)
    ret1, status = log_os_system(cmdstr,0)
    if ret1 == 0 and successtips in status:
        RET[RETURN_KEY1] = 0
    else:
        RET[RETURN_KEY1] = -1
    RET[RETURN_KEY2] = status
    return RET

def test_insp_bmc_control_led(led_conf):
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    sleep_time = led_conf.get("sleep",None)
    led_items = led_conf.get("led_ctl",[])
    if sleep_time is not None:
        time.sleep(sleep_time)
    for item in led_items:
        bus = item["bus"]
        loc = item["loc"]
        reg = item["reg"]
        val = item["val"]
        rji2cset(bus,loc,reg,val)
    return RET

def test_insp_bmc_control_led_pre():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    led_conf = INSP_LED_CTL.get("pre",None)
    if led_conf is None:
        return RET
    return test_insp_bmc_control_led(led_conf)

def test_insp_bmc_control_led_aft():
    RET = {RETURN_KEY1 : 0,  RETURN_KEY2 : ""}
    led_conf = INSP_LED_CTL.get("aft",None)
    if led_conf is None:
        return RET
    return test_insp_bmc_control_led(led_conf)

## 生产测试主程序
if __name__ == '__main__':
    #log_info("生产测试主程序")
  CMD_dispatch()
  unlockInstance();


