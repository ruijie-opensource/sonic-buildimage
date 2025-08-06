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

SYSLOG_IDENTIFIER = "us0-network"
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


def stopusb0config():
    rets = getPid("usb0networkconfig.py")
    for ret in rets:
        cmd = "kill " + ret
        os.system(cmd)
    return True


def startusb0config():
    cmd = "nohup usb0networkconfig.py start >/dev/null 2>&1 &"
    rets = getPid("usb0networkconfig.py")
    if len(rets) == 0:
        os.system(cmd)


@click.group()
def main():
    '''device operator'''
    pass


@main.command()
def start():
    startusb0config()


@main.command()
def stop():
    stopusb0config()


if __name__ == '__main__':
    main()
