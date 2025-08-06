#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
import click
import os
import subprocess
import time
from ruijieutil import *
import syslog
from monitor import status
import traceback
try:
    from rest.rest import BMCMessage
except BaseException:
    pass

AVS_DEBUG_FILE = "/etc/.avs_debug_flag"

AVSDEDEBUG = 1

debuglevel = 0

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
    if os.path.exists(AVS_DEBUG_FILE):
        debuglevel = debuglevel | AVSDEDEBUG
    else:
        debuglevel = debuglevel & ~(AVSDEDEBUG)


def avswarninglog(s):
    syslog.openlog("AVSCONTROL", syslog.LOG_PID)
    syslog.syslog(syslog.LOG_WARNING, s)


def avscriticallog(s):
    syslog.openlog("AVSCONTROL", syslog.LOG_PID)
    syslog.syslog(syslog.LOG_CRIT, s)


def avserror(s):
    syslog.openlog("AVSCONTROL", syslog.LOG_PID)
    syslog.syslog(syslog.LOG_ERR, s)


def avsinfo(s):
    syslog.openlog("AVSCONTROL", syslog.LOG_PID)
    syslog.syslog(syslog.LOG_INFO, s)


def avsdebuglog(s):
    if AVSDEDEBUG & debuglevel:
        syslog.openlog("AVSCONTROL", syslog.LOG_PID)
        syslog.syslog(syslog.LOG_DEBUG, s)


def doAvsCtrol():
    index = 0
    url = "/xyz/openbmc_project/hostchannel/attr/MacRov"
    while True:
        if "avscontrol_restful" in STARTMODULE and STARTMODULE['avscontrol_restful'] == 1:
            try:
                macrov_value = -1
                get_macrov_value = getattr(BMCMessage(), "get_macrov_value", None)
                if callable(get_macrov_value):
                    macrov_value = int(get_macrov_value())
                else:
                    macrov_value = int(BMCMessage().getBmcValue(url))
                if macrov_value >= 0:
                    break
            except Exception as e:
                time.sleep(2)
                continue
        else:
            if AVSUTIL.mac_adj():
                break

        index += 1
        if index >= 10:
            avserror("%%DEV_MONITOR-AVS: MAC Voltage adjust failed.")
            exit(-1)
    avsinfo("%%AVSCONTROL success")
    time.sleep(5)
    exit(0)


def run(interval):
    while True:
        try:
            if waitForDocker(timeout=0) == True:
                time.sleep(10)  # docker起来再等10s
                doAvsCtrol()
            avsdebuglog("DEV_MONITOR-AVS: waitting sdk start-up.")
            time.sleep(interval)
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
    debug_init()
    interval = 5
    run(interval)


# device_i2c operation
if __name__ == '__main__':
    main()
