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


def getip(ethname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15]))[20:24])
        s.close()
        return ip
    except BaseException:
        return None


def check_linked(ifname):
    """check hw(eth0) net physics conection"""
    buff = array.array('i', [0x0000000a, 0x00000000])
    addr, length = buff.buffer_info()
    arg = struct.pack("Pi", addr, length)
    data = (ifname + '\0' * 16)[:16] + arg

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    SIOCETHTOOL = 0x8946
    try:
        fcntl.ioctl(sock.fileno(), SIOCETHTOOL, data)
    except IOError as e:
        print("check eth0 lined failed , and error is ", str(e))
        sock.close()
        return False
    sock.close()

    return bool(buff.tolist()[1])


def getlink(ethname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8946, struct.pack('256s', ethname[:15]))[20:24])
        s.close()
        return ip
    except BaseException:
        return None


ip = "1.1.1.1"
cmdup = "ifconfig usb0 up"
cmd = "ifconfig usb0 %s netmask 255.255.255.0" % ip


def rj_os_system(cmd):
    status, output = subprocess.getstatusoutput(cmd)
    return status, output


def configusb0network():
    log_debug("config usb0 network ing")
    intindex = 0
    while check_linked('usb0') == False:
        rj_os_system(cmdup)
        intindex += 1
        if intindex >= 5:
            log_debug("set usb0 up failed")
            return

    if getip('usb0') == ip:

        return
    else:
        rj_os_system(cmd)
        log_debug("set usb0 ip ")


def stop():
    pass


def run(interval):
    index = 0
    while True:
        try:
            configusb0network()
            time.sleep(interval)
        except Exception as e:
            print(e)


@click.group()
def main():
    '''device operator'''
    pass


@main.command()
def start():
    run(10)


@main.command()
def stop():
    pass


if __name__ == '__main__':
    main()
