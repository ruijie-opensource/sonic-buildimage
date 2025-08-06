#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
import click
import os
import time
import platform
import syslog
import traceback
import json
import subprocess
import signal
import threading
import importlib.machinery
from ruijieutil import *
from ruijieconfig import *

TEST_DEBUG_FILE = "/etc/.test_debug_flag"
TESTDEBUG = 1
debuglevel = 0
SIGNAL_TEST_TIMES = 500

SERVICES_LIST = [
    {
        'stop_service':{"cmd":"systemctl stop rg_platform_process.service", "gettype":"cmd"},
        'start_service':{"cmd":"systemctl start rg_platform_process.service", "gettype":"cmd"},
    },
]

CONFIG_FILE_LIST = ["/usr/local/bin/", "/usr/local/lib/python3.7/dist-packages/config/"]

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

def debug_init():
    global debuglevel
    if os.path.exists(TEST_DEBUG_FILE):
        debuglevel = debuglevel | TESTDEBUG
    else:
        debuglevel = debuglevel & ~(TESTDEBUG)

def testinfo(s):
    syslog.openlog("TEST", syslog.LOG_PID)
    syslog.syslog(syslog.LOG_INFO, s)

def testerror(s):
    #s = s.decode('utf-8').encode('gb2312')
    syslog.openlog("TEST",syslog.LOG_PID)
    syslog.syslog(syslog.LOG_ERR,s)

def testdebuglog(s):
    #s = s.decode('utf-8').encode('gb2312')
    if TESTDEBUG & debuglevel:
        syslog.openlog("TEST",syslog.LOG_PID)
        syslog.syslog(syslog.LOG_DEBUG,s)

def thread_handle(device_config):
    for i in range(SIGNAL_TEST_TIMES):
        dev_name = device_config.get('name', None)
        ret, val = get_value(device_config)
        if ret is True:
            testdebuglog('%s access success' % dev_name)
            continue
        else:
            testerror("%s access failed, log:%s" % (dev_name, val))
            break

class BasePlatform():
    CONFIG_NAME = 'I2C_SCAN_LIST'
    __i2c_dev_list = []
    def __init__(self):
        platform = (getplatform_name()).replace("-", "_")
        for configfile_path in CONFIG_FILE_LIST:
            configfile = (configfile_path + platform + "_i2c_dev_list.py")
            if os.path.exists(configfile):
                real_path = configfile
                break
        config = importlib.machinery.SourceFileLoader(self.CONFIG_NAME, real_path).load_module()
        self.__i2c_dev_list = config.I2C_SCAN_LIST

    def signal_thread_main(self):
        try:
            if len(self.__i2c_dev_list) == 0:
                print("not find i2c dev list config")
                return

            #stop service
            for service_config in SERVICES_LIST:
                stop_service = service_config.get('stop_service', None)
                if stop_service is not None:
                    ret, val = set_value(stop_service)
                    if ret is True:
                        testdebuglog('%s start success' % stop_service)
                        service_config.update({'stop_flag':1})
                    else:
                        testerror("%s start failed, log:%s" % (stop_service, val))

            testdebuglog('all service start success')

            #start accessing device
            loop = 0
            while True:
                loop = loop + 1
                log = "round %d is begin" % loop
                cmd = "echo '%s' > /dev/ttyS0" % log
                subprocess.getstatusoutput(cmd)
                testinfo(log)
                for device_config in self.__i2c_dev_list:
                    if device_config is not None:
                        for i in range(SIGNAL_TEST_TIMES):
                            dev_name = device_config.get('name', None)
                            ret, val = get_value(device_config)
                            if ret is True:
                                testdebuglog('%s access success' % dev_name)
                                continue
                            else:
                                testerror("%s access failed, log:%s" % (dev_name, val))
                                break
                log = "round %d is completed" % loop
                cmd = "echo '%s' > /dev/ttyS0" % log
                subprocess.getstatusoutput(cmd)
                testinfo(log)
        except Exception as e:
            log = "An exception occurred, exception log:%s" % str(e)
            testerror(log)
            return
        finally:
            for service_config in SERVICES_LIST:
                if service_config.get("stop_flag", 0) == 1:
                    start_service = service_config.get('start_service', None)
                    if start_service is not None:
                        set_value(start_service)
            return

    def mul_thread_main(self):
        try:
            if len(self.__i2c_dev_list) == 0:
                print("not find i2c dev list config")
                return

            #start accessing device
            while True:
                for device_config in self.__i2c_dev_list:
                    if device_config is not None:
                        t = threading.Thread(target=thread_handle, args=(device_config,))
                        t.start()
            return
        except Exception as e:
            log = "An exception occurred, exception log:%s" % str(e)
            testerror(log)
            return

@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
def main():
    '''test script'''

#signal_thread test
@main.command()
def signal_thread():
    '''signal_thread'''
    platform = BasePlatform()
    platform.signal_thread_main()

# mul_thread test
@main.command()
def mul_thread():
    '''mul_thread'''
    platform = BasePlatform()
    platform.mul_thread_main()

if __name__ == '__main__':
    debug_init()
    main()
