#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import subprocess
import os
import re


class pktutil:
    def pkt_os_util(self, cmd):
        status, output = subprocess.getstatusoutput(cmd)
        return status, output

    def __init__(self):
        self.__check_pktgen_driver()  # check driver

    def getpktversion(self):
        cmd = "cat /proc/net/pktgen/pgctrl"
        status, log = self.pkt_os_util(cmd)
        return log

    def __checkroot():
        if os.geteuid() != 0:
            raise Exception("please use root operate!")

    def __check_pktgen_driver(self):
        cmd = "lsmod | grep pktgen"
        status, log = self.pkt_os_util(cmd)
        if status != 0 or len(log) < 1:
            cmd = "modprobe pktgen"
            ret, output = subprocess.getstatusoutput(cmd)

    def get_frame_count(self, iface='eth0'):
        u''' get current iface tx  rx packet '''
        txcmd = "ifconfig %s |grep -E 'TX packets'" % iface
        rxcmd = "ifconfig %s |grep -E 'RX packets'" % iface
        ret, txlog = self.pkt_os_util(txcmd)
        ret, rxlog = self.pkt_os_util(rxcmd)
        tx = re.findall(r"\d+\.?\d*", txlog)[0]
        rx = re.findall(r"\d+\.?\d*", rxlog)[0]
        return int(rx), int(tx)

    def __sendpkt(self, iface, count, size, dst_mac):
        if os.path.exists("/proc/net/pktgen/%s" % iface) != True:
            cmd = "echo \"add_device %s\" > /proc/net/pktgen/kpktgend_0" % iface
            ret, output = self.pkt_os_util(cmd)
            if(ret != 0):
                raise Exception(str(output))
        cmd = "echo \"pkt_size %d\" > /proc/net/pktgen/%s" % (size, iface)
        ret, output = self.pkt_os_util(cmd)
        if(ret != 0):
            raise Exception(str(output))
        cmd = "echo \"delay  %d\" > /proc/net/pktgen/%s" % (100000, iface)
        ret, output = self.pkt_os_util(cmd)
        if(ret != 0):
            raise Exception(str(output))
        cmd = "echo \"count %d\" > /proc/net/pktgen/%s" % (count, iface)
        ret, output = self.pkt_os_util(cmd)
        if(ret != 0):
            raise Exception(str(output))
        cmd = "echo \"dst_mac %s\" > /proc/net/pktgen/%s" % (dst_mac, iface)
        ret, output = self.pkt_os_util(cmd)
        if(ret != 0):
            raise Exception(str(output))
        cmd = "echo \"start\" > /proc/net/pktgen/pgctrl"
        ret, output = self.pkt_os_util(cmd)
        if(ret != 0):
            raise Exception(str(output))
        cmd = "cat /proc/net/pktgen/%s" % iface
        ret, output = self.pkt_os_util(cmd)
        if(ret != 0):
            raise Exception(str(output))
        return True, output

    def sendpacket(self, iface, count, size=64, dst_mac="ff:ff:ff:ff:ff:ff"):
        return self.__sendpkt(iface, count, size, dst_mac)
