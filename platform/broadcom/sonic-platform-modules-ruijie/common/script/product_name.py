#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import syslog
from ruijieconfig import *
from rjutil.baseutil import get_machine_info
from rjutil.baseutil import get_onie_machine

BOARD_ID_PATH = "/sys/module/ruijie_common/parameters/dfd_my_type"
PRODUCT_DEBUG_FILE = "/etc/.product_debug_flag"
PRODUCT_RESULT_FILE = "/tmp/.productname"

PRODUCTERROR = 1
PRODUCTDEBUG = 2

debuglevel = 0


def product_info(s):
    syslog.openlog("PRODUCT", syslog.LOG_PID)
    syslog.syslog(syslog.LOG_INFO, s)


def product_error(s):
    syslog.openlog("PRODUCT", syslog.LOG_PID)
    syslog.syslog(syslog.LOG_ERR, s)


def product_debug(s):
    if PRODUCTDEBUG & debuglevel:
        syslog.openlog("PRODUCT", syslog.LOG_PID)
        syslog.syslog(syslog.LOG_DEBUG, s)

def product_debug_error(s):
    if PRODUCTERROR & debuglevel:
        syslog.openlog("PRODUCT", syslog.LOG_PID)
        syslog.syslog(syslog.LOG_ERR, s)


def debug_init():
    global debuglevel
    try:
        with open(PRODUCT_DEBUG_FILE, "r") as fd:
            value = fd.read()
        debuglevel = int(value)
    except Exception as e:
        debuglevel = 0

################################## 各产品自定义接口存放区 begin ###################################

'''tcs84读取MAC芯片ID区分产品'''
def get_td4_mac_id(loc):
    if not os.path.exists(loc):
        msg = "mac id path: %s, not exists" % loc
        product_error(msg)
        return False, msg
    with open(loc) as fd:
        id_str = fd.read().strip()
    id = "0x%x" % (int(id_str, 10))
    return True, id

################################## 各产品自定义接口存放区 end #####################################

def get_func_value(funcname, params = None):
    try:
        if params is not None:
            status, ret = eval(funcname)(params)
        else:
            status, ret = eval(funcname)
        return status, ret
    except Exception as e:
        product_error(str(e))
    return False, str(e)


def get_product_name_default():
    onie_machine = get_onie_machine(get_machine_info())
    if onie_machine is not None:
        ret = onie_machine.strip().split("_", 1)
        if len(ret) != 2:
            product_error("unknow onie machine: %s" % onie_machine)
            return None
        product_name = ret[1]
        product_debug("get product name: %s success" % product_name)
        return product_name
    product_error("onie machine is None, can't get product name")
    return None


def get_board_id_default():
    if not os.path.exists(BOARD_ID_PATH):
        product_error("board id path: %s, not exists" % BOARD_ID_PATH)
        return None
    with open(BOARD_ID_PATH) as fd:
        id_str = fd.read().strip()
    return "0x%x" % (int(id_str, 10))


def deal_method(method):
    try:
        gettype = method.get("gettype")
        if gettype == "config": # 通过配置文件获取
            result = method.get("value")
            product_debug("get info use config value: %s" % result)
            return True, result

        if gettype == "func": # 通过自定义函数获取
            funcname = method.get("funcname")
            params = method.get("params")
            status, ret = get_func_value(funcname, params)
            if status is False:
                product_error("get info func: %s, params: %s failed, ret: %s" %
                    (funcname, params, ret))
                return status, ret
            decode_val = method.get("decode")
            if decode_val is not None:
                result = decode_val.get(ret)
            else:
                result = ret
            product_debug("get info func: %s, params: %s, ret: %s, result: %s" %
                (funcname, params, ret, result))
            return True, result
        msg = "unsupport get info method: %s " % gettype
        product_error(msg)
        return False, msg
    except Exception as e:
        return False, str(e)


def get_product_name():
    # 获取产品名称
    get_product_name_method = PRODUCT_NAME_CONF.get("get_product_name_method")
    if get_product_name_method is None: # 采用默认的方法获取产品名称
        product_name = get_product_name_default()
        product_debug("get product name use default method, product name: %s" % (product_name))
        return product_name

    status, ret = deal_method(get_product_name_method)
    if status is False:
        product_error("get product name faield, msg: %s" % ret)
        return None
    product_debug("get product name success, product name: %s" % (ret))
    return ret


def get_board_id():
    # 获取板卡ID
    get_board_id_method = PRODUCT_NAME_CONF.get("get_board_id_method")
    if get_board_id_method is None: # 采用默认的方法获取板卡ID
        board_id = get_board_id_default()
        product_debug("get board id use default method, board id: %s" % (board_id))
        return board_id

    status, ret = deal_method(get_board_id_method)
    if status is False:
        product_error("get board id faield, msg: %s" % ret)
        return None
    product_debug("get board id success, board id: %s" % (ret))
    return ret


def save_product_name():
    # 获取产品名称
    product_name = get_product_name()
    board_id = get_board_id()
    name = "%s_%s\n" % (product_name, board_id)
    product_info("save product name: %s" % name)
    with open(PRODUCT_RESULT_FILE, "w") as fd:
        fd.write(name)


if __name__ == '__main__':
    debug_init()
    product_debug("enter main")
    save_product_name()
