#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
import click
import os
import subprocess
import time
import syslog
import traceback
from  ruijieutil import * 

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

def avswarninglog(s):
    #s = s.decode('utf-8').encode('gb2312')
    syslog.openlog("AVSCONTROL",syslog.LOG_PID)
    syslog.syslog(syslog.LOG_WARNING,s)

def avscriticallog(s):
    #s = s.decode('utf-8').encode('gb2312')
    syslog.openlog("AVSCONTROL",syslog.LOG_PID)
    syslog.syslog(syslog.LOG_CRIT,s)

def avserror(s):
    #s = s.decode('utf-8').encode('gb2312')
    syslog.openlog("AVSCONTROL",syslog.LOG_PID)
    syslog.syslog(syslog.LOG_ERR,s)

def avsinfo(s):
    syslog.openlog("AVSCONTROL",syslog.LOG_PID)
    syslog.syslog(syslog.LOG_INFO,s)

def log_os_system(cmd):
    u'''shell commond'''
    status, output = subprocess.getstatusoutput(cmd)
    if status:
        print(output)
    return  status, output

def readsysfs(location):
    try:
        locations = glob.glob(location)
        with open(locations[0], 'rb') as fd1:
            retval = fd1.read()
        retval = retval.rstrip('\r\n')
        retval = retval.lstrip(" ")
    except Exception as e:
        return False, (str(e)+" location[%s]" % location)
    return True, retval

def writesysfs(location, value):
    try:
        if not os.path.isfile(location):
            print(location, 'not found !')
            return False, ("location[%s] not found !" % location)
        with open(location, 'w') as fd1:
            fd1.write(value)
    except Exception as e:
        return False, (str(e)+" location[%s]" % location)
    return True, ("set location[%s] %s success !" % (location, value))

def rji2cget(bus, devno, address):
    command_line = "i2cget -f -y %d 0x%02x 0x%02x " % (bus, devno, address)
    retrytime = 6
    ret_t = ""
    for i in range(retrytime):
        ret, ret_t = log_os_system(command_line)
        if ret == 0:
            return True, ret_t
        time.sleep(0.1)
    return False, ret_t

def rji2cset(bus, devno, address, byte):
    command_line = "i2cset -f -y %d 0x%02x 0x%02x 0x%02x" % (
        bus, devno, address, byte)
    retrytime = 6
    ret_t = ""
    for i in range(retrytime):
        ret, ret_t = log_os_system(command_line)
        if ret == 0:
            return True, ret_t
    return False, ret_t

def get_value(config):
    way = config.get("gettype")
    if way == 'sysfs':
        return readsysfs(config.get("loc"))
    elif way == "i2c":
        bus = config.get("bus")
        addr = config.get("loc")
        offset = config.get("offset")
        ret, val = rji2cget(bus, addr, offset)
        if ret == True:
            value = int(val,16)
        else:
            value = val
        return ret, value
    elif way == "io":
        io_addr = config.get("io_addr")
        ret = io_rd(io_addr)
        if ret != None:
            value = int(ret, 16)
        else:
            ret = False
            value = None
        return ret, value
    return False, None

def set_value(config, value):
    way = config.get("gettype")
    if way == 'sysfs':
        loc = config.get("loc")
        return writesysfs(loc, "0x%x" % value)
    elif way == "i2c":
        bus = config.get("bus")
        addr = config.get("loc")
        offset = config.get("offset")
        return rji2cset(bus, addr, offset, value)
    return False, None

def get_dcdc_value(cpld_value):
    for key in MAC_AVS_SYSFS_PARAM:
        if key == cpld_value:
            dcdc_value = MAC_AVS_SYSFS_PARAM[key]
            return True, dcdc_value
    return False, None

def get_rov_value_cpld():
    cpld_avs_config = MAC_AVS_SYSFS_DEFAULT_PARAM["cpld_avs"]
    return get_value(cpld_avs_config)

def get_rov_value_sdk():
    name = MAC_AVS_SYSFS_DEFAULT_PARAM["sdkreg"]
    ret, status = getSdkReg(name)
    if ret == False:
        return False, None
    status = strtoint(status)
    # shift operation
    if MAC_AVS_SYSFS_DEFAULT_PARAM["sdktype"] != 0:
        status = (
            status >> MAC_AVS_SYSFS_DEFAULT_PARAM["macregloc"]) & MAC_AVS_SYSFS_DEFAULT_PARAM["mask"]
    macavs = status
    return True, macavs

def doAvsCtrol():
    default_type = MAC_AVS_SYSFS_DEFAULT_PARAM["type"]
    dcdc_value_default = MAC_AVS_SYSFS_DEFAULT_PARAM["default"]
    rov_source = MAC_AVS_SYSFS_DEFAULT_PARAM["rov_source"]
    set_avs_config = MAC_AVS_SYSFS_DEFAULT_PARAM["set_avs"]
    if rov_source == 0:
        ret, rov_value = get_rov_value_cpld() #get rov from cpld reg
    else:
        ret, rov_value = get_rov_value_sdk() #get rov from sdk reg
    if ret == False:
        return False, "get rov_value failed"
    ret, value = get_dcdc_value(rov_value)
    if ret == True:
        dcdc_value = value
    else:
        if default_type == 0:
            return False, "get dcdc_value failed"
        dcdc_value = dcdc_value_default
    return set_value(set_avs_config, dcdc_value)

def run():
    try:
        #wait 30s for device steady
        time.sleep(30)
        ret, value = doAvsCtrol()
        if ret == True:
            avsinfo("%%AVSCONTROL success")
        else:
            avserror("%%AVSCONTROL failed")
            avserror("%s" % value)
    except Exception as e:
        traceback.print_exc()
        print(e)

@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
def main():
    '''device operator'''
    pass

@main.command()
def start():
    '''start AVS control'''
    avsinfo("%%AVSCONTROL start")
    run()

if __name__ == '__main__':
    main()