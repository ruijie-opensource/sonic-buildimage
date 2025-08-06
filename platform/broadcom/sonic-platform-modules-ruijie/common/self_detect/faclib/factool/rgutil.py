#!/usr/bin/python
# -*- coding: UTF-8 -*-
import traceback
from faclib.config.facconfig import *

try:
    from faclib.mft.mftport import PortScene
except:
    pass

from collections import OrderedDict

from os.path import exists
from functools import wraps
from faclib.wbutil.smbus import SMBus
import subprocess
import time

SUCCESS_TIPS = "PASS"

RETURN_KEY1 = "code"
RETURN_KEY2 = "msg"
ERROR_RETURN = {RETURN_KEY1: -1, RETURN_KEY2: "init error"}
SUCCESS_RETURN = {RETURN_KEY1: 0, RETURN_KEY2: ""}
ERROR_RETURN_DETAIL = {RETURN_KEY1: -1, RETURN_KEY2: []}

MENUID = "menuid"
MENUPARENT = "parentid"
MENUVALUE = "value"
CHILDID = "childid"
MENUITEMNAME = "name"
MENUITEMDEAL = "deal"
GOBACK = "goBack"
GOQUIT = "quit"
ITEMBEFORE = 'before'
ITEMAFTER = 'after'

listindex = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
             'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
formatStringLevel1 = "%s.%s"
SYSINFOTIPS_FORMAT = "%30s : %s"

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


class PortTestCall():
    '''调用接口'''
    port_obj = None
    test_type = None
    port_list_val = None
    redirect = None
    port_map = None
    analy_ret = None

    def __init__(self, port_list_val=[], redirect=True, test_type="prbs_mac", port_map=False, analy_ret=True):
        self.port_obj = PortScene()
        self.test_type = test_type
        self.port_list_val = port_list_val
        self.redirect = redirect
        self.port_map = port_map
        self.analy_ret = analy_ret

    def port_frame_test(self):
        log_debug("port_frame_test param port_list_val=%s redirect=%s" %
                  (self.port_list_val, self.redirect))
        ret = self.port_obj.port_frame_test(self.port_list_val, self.redirect)
        if self.analy_ret:
            return self.analy_result(ret)
        else:
            return ret

    def port_brcst_test(self):
        log_debug("port_brcst_test param port_list_val=%s redirect=%s" %
                  (self.port_list_val, self.redirect))
        ret = self.port_obj.port_brcst_test(self.port_list_val, self.redirect)
        if self.analy_ret:
            return self.analy_result(ret)
        else:
            return self.ret

    def port_kr_test(self):
        log_debug("port_kr_test param port_list_val=%s redirect=%s" %
                  (self.port_list_val, self.redirect))
        ret = self.port_obj.port_kr_test(self.port_list_val, self.redirect)
        if self.analy_ret:
            return self.analy_result(ret)
        else:
            return self.ret

    def port_prbs_test(self):
        log_debug("port_prbs_test param port_list_val=%s test_type=%s redirect=%s" %
                  (self.port_list_val, self.test_type, self.redirect))
        ret = self.port_obj.port_prbs_test(self.port_list_val, self.test_type, self.redirect)
        if self.analy_ret and self.test_type == "prbs_mac":
            return self.analy_result(ret.get("prbs_mac_result_dict"))
        elif self.analy_ret:
            # 分次解析三个字典
            pass
        else:
            return self.ret

    def port_map_func(self):
        pass

    def analy_result(self, val):
        ret_dic = OrderedDict()
        ret = True
        if val is None:
            return False, {}
        # 解析解析
        if self.port_map:
            self.port_map_func()
        err_log = ""
        ret_dic['OK'] = val.get('successports', [])
        ret_dic['failed'] = val.get('errorports', [])
        ret_dic['updownerro'] = val.get('updownerrorports', [])
        ret_dic['prbs_info'] = val.get('prbs_info', "")

        if len(ret_dic['failed']) != 0 or len(ret_dic['updownerro']) != 0 or \
                len(ret_dic['OK']) == 0:
            ret = False
            log_debug("port error result port_info_dict:%s other_info:%s" % (val.get('port_info_dict', ""),
                                                                             val.get('other_info', "")))
            ret_dic['other_info'] = val.get('other_info', "")
            ret_dic['prbs_info'] = val.get('prbs_info', "")
            tmp = val.get('port_info_dict')
            for k, v in list(tmp.items()):
                log = v.get('log', "")
                if log != "":
                    err_log += "port%s：%s\n\n" % (k, log)
            ret_dic['port_info_dict'] = err_log

        return ret, ret_dic


def sysfs_rd(path):
    if not exists(path):
        raise IOError("file {} not exists".format(path))
    try:
        with open(path, 'r') as fd:
            return fd.read()
    except Exception as e:
        print((e.message))


def i2c_read(bus, devno, address):
    command_line = "i2cget -f -y %d 0x%02x 0x%02x " % (bus, devno, address)
    ret, ret_t = rj_os_system(command_line)
    if ret == 0:
        return True, ret_t
    return False, ret_t


def rj_os_system(cmd):
    status, output = subprocess.getstatusoutput(cmd)
    return status, output


def retry(maxretry=6, delay=0.01):
    '''
        maxretry:  max retry times
        delay   :  interval after last retry
    '''
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            time_retry = maxretry
            time_delay = delay
            result_msg = ""
            while time_retry:
                try:
                    val, result_msg = f(*args, **kwargs)
                    if val is False:
                        time_retry -= 1
                        time.sleep(time_delay)
                        continue
                    else:
                        return val, result_msg
                except Exception as e:
                    time_retry -= 1
                    result_msg = str(e)
                    time.sleep(time_delay)
            return False, "max time retry last errmsg is {}".format(result_msg)
        return wrapper
    return decorator


class osutil(object):
    """
       osutil
    """

    @staticmethod
    @retry(maxretry=6)
    def rji2cget_python(bus, addr, reg):
        with SMBus(bus) as y:
            val, ind = y.read_byte_data(addr, reg, True)
        return val, ind

    @staticmethod
    @retry(maxretry=6)
    def rji2cset_python(bus, addr, reg, value):
        with SMBus(bus) as y:
            val, ind = y.write_byte_data(addr, reg, value, True)
        return val, ind

    @staticmethod
    @retry(maxretry=6)
    def rji2cgetword_python(bus, addr, reg):
        with SMBus(bus) as y:
            val, ind = y.read_word_data(addr, reg, True)
        return val, ind

    @staticmethod
    @retry(maxretry=6)
    def rji2csetword_python(bus, addr, reg, value):
        with SMBus(bus) as y:
            val, ind = y.write_word_data(addr, reg, value, True)
        return val, ind

    @staticmethod
    @retry(maxretry=6)
    def rji2csetwordpec_python(bus, addr, reg, value):
        with SMBus(bus) as y:
            val, ind = y.write_word_data_pec(addr, reg, value, True)
        return val, ind

    @staticmethod
    @retry(maxretry=6)
    def rji2cset_byte_pec_python(bus, addr, reg, value):
        with SMBus(bus) as y:
            val, ind = y.write_byte_data_pec(addr, reg, value, True)
        return val, ind

    @staticmethod
    def command(cmdstr):
        retcode, output = subprocess.getstatusoutput(cmdstr)
        return retcode, output

    @staticmethod
    def geti2cword_i2ctool(bus, addr, offset):
        command_line = "i2cget -f -y %d 0x%02x 0x%02x  wp" % (bus, addr, offset)
        retrytime = 6
        ret_t = ""
        for i in range(retrytime):
            ret, ret_t = osutil.command(command_line)
            if ret == 0:
                return True, int(ret_t, 16)
            time.sleep(0.1)
        return False, ret_t

    @staticmethod
    def seti2cword_i2ctool(bus, addr, offset, val):
        command_line = "i2cset -f -y %d 0x%02x 0x%0x 0x%04x wp" % (bus, addr, offset, val)
        retrytime = 6
        ret_t = ""
        for i in range(retrytime):
            ret, ret_t = osutil.command(command_line)
            if ret == 0:
                return True, ret_t
            time.sleep(0.1)
        return False, ret_t

    @staticmethod
    def rji2cget_i2ctool(bus, devno, address):
        command_line = "i2cget -f -y %d 0x%02x 0x%02x " % (bus, devno, address)
        retrytime = 6
        ret_t = ""
        for i in range(retrytime):
            ret, ret_t = osutil.command(command_line)
            if ret == 0:
                return True, int(ret_t, 16)
            time.sleep(0.1)
        return False, ret_t

    @staticmethod
    def rji2cset_i2ctool(bus, devno, address, byte):
        command_line = "i2cset -f -y %d 0x%02x 0x%02x 0x%02x" % (
            bus, devno, address, byte)
        retrytime = 6
        ret_t = ""
        for i in range(retrytime):
            ret, ret_t = osutil.command(command_line)
            if ret == 0:
                return True, ret_t
        return False, ret_t

    @staticmethod
    def geti2cword(bus, addr, offset):
        return osutil.rji2cgetword_python(bus, addr, offset)

    @staticmethod
    def seti2cword(bus, addr, offset, val):
        return osutil.rji2csetword_python(bus, addr, offset, val)

    @staticmethod
    def seti2cwordpec(bus, addr, offset, val):
        return osutil.rji2csetwordpec_python(bus, addr, offset, val)

    @staticmethod
    def seti2c_byte_pec(bus, addr, offset, val):
        return osutil.rji2cset_byte_pec_python(bus, addr, offset, val)

    @staticmethod
    def rji2cget(bus, devno, address):
        return osutil.rji2cget_python(bus, devno, address)

    @staticmethod
    def rji2cset(bus, devno, address, byte):
        return osutil.rji2cset_python(bus, devno, address, byte)

    @staticmethod
    def byteTostr(val):
        strtmp = ''
        for i in range(len(val)):
            strtmp += chr(val[i])
        return strtmp

    @staticmethod
    def readsysfs(location):
        try:
            locations = glob.glob(location)
            with open(locations[0], 'rb') as fd1:
                retval = fd1.read()
            retval = retval.rstrip('\r\n')
            retval = retval.lstrip(" ")
        except Exception as e:
            return False, (str(e) + " location[%s]" % location)
        return True, retval

    @staticmethod
    def writesysfs(location, value):
        try:
            if not os.path.isfile(location):
                print((location, 'not found !'))
                return False, ("location[%s] not found !" % location)
            with open(location, 'w') as fd1:
                fd1.write(value)
        except Exception as e:
            return False, (str(e) + " location[%s]" % location)
        return True, ("set location[%s] %s success !" % (location, value))

    @staticmethod
    def getdevmem(addr, digit, mask):
        command_line = "devmem 0x%02x %d" % (addr, digit)
        retrytime = 6
        ret_t = ""
        for i in range(retrytime):
            ret, ret_t = osutil.command(command_line)
            if ret == 0:
                if mask is not None:
                    ret_t = str(int(ret_t, 16) & mask)
            return True, ret_t
        return False, ret_t

    @staticmethod
    def rj_os_system(cmd):
        status, output = subprocess.getstatusoutput(cmd)
        return status, output

    @staticmethod
    def getsdkreg(reg):
        try:
            cmd = "bcmcmd -t 1 'getr %s ' < /dev/null" % reg
            ret, result = osutil.rj_os_system(cmd)
            result_t = result.strip().replace("\r", "").replace("\n", "")
            if ret != 0 or "Error:" in result_t:
                return False, result
            patt = r"%s.(.*):(.*)>drivshell" % reg
            rt = re.findall(patt, result_t, re.S)
            test = re.findall("=(.*)", rt[0][0])[0]
        except Exception as e:
            return False, 'get sdk register error'
        return True, test

    @staticmethod
    def getmactemp():
        try:
            result = {}
            # waitForDocker()
            # need to exec twice
            ret, log = osutil.rj_os_system("bcmcmd -t 1 \"show temp\" < /dev/null")
            ret, log = osutil.rj_os_system("bcmcmd -t 1 \"show temp\" < /dev/null")
            if ret:
                return False, result
            else:
                logs = log.splitlines()
                for line in logs:
                    if "average" in line:
                        b = re.findall(r'\d+.\d+', line)
                        result["average"] = b[0]
                    elif "maximum" in line:
                        b = re.findall(r'\d+.\d+', line)
                        result["maximum"] = b[0]
        except Exception as e:
            return False, str(e)
        return True, result
