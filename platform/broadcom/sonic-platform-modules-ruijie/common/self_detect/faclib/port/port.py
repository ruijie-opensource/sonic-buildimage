#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import os
import re
import logging
import syslog
import subprocess
import subprocess
from . import portutil
import click
try:
    from sonic_platform import get_machine_info
    from sonic_platform import get_platform_info
except BaseException:
    from sonic_device_util import get_machine_info
    from sonic_device_util import get_platform_info

MACHINE_FILE = "/host/machine.conf"
MACHINE_PLATFORM_PREDIX = "onie_platform="
SYSLOG_IDENTIFIER = "PORT"


global_mgmt_kr_ports = {
    "x86_64-ruijie_b6510-48vs8cq-r0": {"eth1": 66, "eth2": 130},
    "x86_64-ruijie_b6510-32cq-r0": {"eth1": 66, "eth2": 130},
    "x86_64-ruijie_b6520-64cq-r0": {"eth1": 66, "eth2": 100},
    "x86_64-ruijie_b6920-4c-r0": {"eth1": 38, "eth2": 118},
    "x86_64-tencent_tcs81-100f-r0": {"eth1": 66, "eth2": 130},
    "x86_64-tencent_tcs82-100f-r0": {"eth1": 66, "eth2": 130},
    "x86_64-tencent_tcs83-100f-r0": {"eth1": 38, "eth2": 118}
}


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


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton

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
        print(e)
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


class PortKrTest(object):

    def __init__(self):
        self.__install_pktgen_mode()

    def __get_onie_platform(self):
        with open(MACHINE_FILE, "r") as machine_f:
            for line in machine_f:
                if(re.search('%s(.*?)$' % MACHINE_PLATFORM_PREDIX, line)):
                    onie_platform = re.findall(r"%s(.*?)$" % MACHINE_PLATFORM_PREDIX, line)[0]
                    return onie_platform
        return None

    def __install_pktgen_mode(self):
        cmd = "lsmod | grep pktgen"
        ret, output = subprocess.getstatusoutput(cmd)
        if(not output):
            cmd = "modprobe pktgen"
            ret, output = subprocess.getstatusoutput(cmd)
        cmd = "ls /proc/net/pktgen/eth1"
        ret, output = subprocess.getstatusoutput(cmd)
        if("cannot" in output):
            cmd = "ifconfig eth1 up"
            ret, output = subprocess.getstatusoutput(cmd)
            time.sleep(1)
            cmd = "echo \"add_device eth1\" > /proc/net/pktgen/kpktgend_0"
            ret, output = subprocess.getstatusoutput(cmd)
        cmd = "ls /proc/net/pktgen/eth2"
        ret, output = subprocess.getstatusoutput(cmd)
        if("cannot" in output):
            cmd = "ifconfig eth2 up"
            ret, output = subprocess.getstatusoutput(cmd)
            time.sleep(1)
            cmd = "echo \"add_device eth2\" > /proc/net/pktgen/kpktgend_0"
            ret, output = subprocess.getstatusoutput(cmd)
        time.sleep(3)

    def get_mgmt_bcmport(self, port):
        cmd = "bcmcmd ps"
        ret, output = subprocess.getstatusoutput(cmd)
        lines = output.split("\n")
        logic_port = global_mgmt_kr_ports[self.__get_onie_platform()][port]
        for line in lines:
            line.strip()
            if re.search(r"^.*?\(.*?\)", line) and int(re.findall(r"^.*?\((.*?)\)",
                                                                  line)[0].strip()) == logic_port:
                return re.findall(r"^(.*?)\(.*?\)", line)[0].strip()
        return None

    def start_send_port_packets(self, port, count=10000, size=64, dst_mac="ff:ff:ff:ff:ff:ff", vlan=4080):
        bcm_port = self.get_mgmt_bcmport(port)
        time.sleep(1)
        cmd = "bcmcmd \"vlan destroy %d\"" % vlan
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = "bcmcmd \"vlan create %d PortBitMap=%s UntagBitMap=%s\"" % (vlan, bcm_port, bcm_port)
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = "bcmcmd \"pvlan set %s %d\"" % (bcm_port, vlan)
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output

        cmd = "echo \"pkt_size %d\" > /proc/net/pktgen/%s" % (size, port)
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = "echo \"count %d\" > /proc/net/pktgen/%s" % (count, port)
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = "echo \"dst_mac %s\" > /proc/net/pktgen/%s" % (dst_mac, port)
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = "echo \"vlan_id %s\" > /proc/net/pktgen/%s" % (vlan, port)
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = "bcmcmd \"clear c %s\"" % bcm_port
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output

        cmd = "echo \"start\" > /proc/net/pktgen/pgctrl"
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        time.sleep(2)
        cmd = "echo \"stop\" > /proc/net/pktgen/pgctrl"
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = "bcmcmd \"vlan remove %d PortBitMap=%s\"" % (vlan, bcm_port)
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = "cat /proc/net/pktgen/%s" % port
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output

        return True, output

    def clear_port_packets(self):
        for port in global_mgmt_kr_ports[self.__get_onie_platform()]:
            cmd = "bcmcmd \"clear c %s\"" % self.get_mgmt_bcmport(port)
            ret, output = subprocess.getstatusoutput(cmd)
            if(ret != 0):
                return False, output
        return True, output

    def check_port_packets(self, port, count=10000):
        cmd = "bcmcmd \"show c XLMIB_RPOK.%s\"" % self.get_mgmt_bcmport(port)
        ret, output = subprocess.getstatusoutput(cmd)
        # print output
        lines = output.split("\n")
        if(lines[1].strip()):
            if (count == int(re.sub('[,]', '', lines[1].split()[2].strip("+-")))):
                return True, lines[1].split()[2]
            else:
                return False, lines[1].split()[2]
        return False, "fail"


@Singleton
class PortTest(object):
    __mode = 0

    interfaces = []
    porttabfile = " "
    bcm_ports = []
    logic_ports = []

    def __init__(self, mode="sdk"):
        self.__install_pktgen_mode()
        self.__get_global_interfaces()
        self.__get_global_bcmports()
        if(mode == "sonic"):
            self.__mode = 1
        else:
            self.__mode = 0

    def __install_pktgen_mode(self):
        cmd = "lsmod | grep pktgen"
        ret, output = subprocess.getstatusoutput(cmd)
        lines = output.split("\n")
        if(not lines):
            cmd = "modprobe pktgen"
            ret, output = subprocess.getstatusoutput(cmd)

    def __get_global_interfaces(self):
        if(len(self.interfaces)):
            #print("inited interfaces")
            pass
        else:
            cmd = "show interfaces status"
            ret, output = subprocess.getstatusoutput(cmd)
            lines = output.split("\n")
            for line in lines:
                line.strip()
                if(len(line.split()) and re.search("Ethernet[0-9]+", line.split()[0])):
                    self.interfaces.append(line.split()[0])

    def __get_global_bcmports(self):
        if(len(self.bcm_ports)):
            pass
        else:
            pu = portutil.PortUtil()
            cmd = "bcmcmd ps"
            ret, output = subprocess.getstatusoutput(cmd)
            lines = output.split("\n")
            for port in pu.device_port_list:
                for line in lines:
                    line.strip()
                    if re.search(r"^.*?\(.*?\)", line) and int(re.findall(r"^.*?\((.*?)\)", line)
                                                               [0].strip()) == port.logic_port:
                        self.bcm_ports.append(re.findall(r"^(.*?)\(.*?\)", line)[0].strip())
                        self.logic_ports.append(port.logic_port)
                        break
            log_debug(' '.join(str(i) for i in self.bcm_ports))

    def __get_port_status_by_sonic(self, port):
        cmd = "show int status %s" % self.interfaces[port - 1]
        ret, output = subprocess.getstatusoutput(cmd)
        lines = output.split("\n")
        return lines[-2].split()[5]

    def __get_port_status_by_sdk(self, port):
        cmd = "bcmcmd \"ps %s\"" % self.bcm_ports[port - 1]
        ret, output = subprocess.getstatusoutput(cmd)
        lines = output.split("\n")
        if(re.search("up", lines[3])):
            return "up"
        elif(re.search("!ena", lines[3])):
            return "!ena"
        else:
            return "down"

    def __get_unit_port_by_bcm(self, port):
        cmd = "bcmcmd \"ps %s\"" % self.bcm_ports[port - 1]
        ret, output = subprocess.getstatusoutput(cmd)
        lines = output.split("\n")
        unit_port = int(re.findall(r"%s\((.*?)\)" % self.bcm_ports[port - 1], lines[3])[0].strip())
        return unit_port

    def __start_send_port_packets_by_sonic(self, port, count, size=64, dst_mac="ff:ff:ff:ff:ff:ff"):
        cmd = "echo \"add_device %s\" > /proc/net/pktgen/kpktgend_0" % self.interfaces[port - 1]
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = "echo \"pkt_size %d\" > /proc/net/pktgen/%s" % (size, self.interfaces[port - 1])
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = "echo \"count %d\" > /proc/net/pktgen/%s" % (count, self.interfaces[port - 1])
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = "echo \"dst_mac %s\" > /proc/net/pktgen/%s" % (dst_mac, self.interfaces[port - 1])
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = "echo \"start\" > /proc/net/pktgen/pgctrl"
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = "cat /proc/net/pktgen/%s" % self.interfaces[port - 1]
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        return True, output

    def __start_send_port_packets_by_sdk(self, port, count, size=64, dst_mac="ff:ff:ff:ff:ff:ff"):
        cmd = "bcmcmd \"pbmp %s\"" % self.bcm_ports[port - 1]
        ret, output = subprocess.getstatusoutput(cmd)
        lines = output.split("\n")
        pbmp = re.findall("0x[0-9]+", lines[1].strip())[0]
        cmd = "bcmcmd \"tx %d VLantag=1 TXUnit=0 PortBitMap=%s Length=%d DestMac=%s\"" % (count, pbmp, size, dst_mac)
        ret, output = subprocess.getstatusoutput(cmd)
        log_debug(output)
        if(ret != 0):
            return False, output
        return True, output

    def __clear_port_packets_by_sonic(self):
        cmd = "show interfaces counters -c"
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        return True, output

    def __clear_port_packets_by_sdk(self):
        cmd = "bcmcmd \"clear c\""
        ret, output = subprocess.getstatusoutput(cmd)
        log_debug(output)
        if(ret != 0):
            return False, output
        return True, output

    def __check_port_packets_by_sonic(self, port, count, direc="tx"):
        cmd = "show interfaces counters"
        ret, output = subprocess.getstatusoutput(cmd)
        lines = output.split("\n")
        for line in lines:
            line.strip()
            if(len(line.split()) and re.search("Ethernet[0-9]+", line.split()[0])):
                if(self.interfaces[port - 1] == line.split()[0]):
                    if(direc == "tx"):
                        if(count == int(re.sub('[,]', '', line.split()[9]))):
                            return True, line.split()[9]
                        else:
                            #print("packets num = %s" % int(re.sub('[,]', '', line.split()[9])))
                            return False, line.split()[9]
                    elif(direc == "rx"):
                        if(count == int(re.sub('[,]', '', line.split()[2]))):
                            return True, line.split()[9]
                        else:
                            #print("packets num = %s" % int(re.sub('[,]', '', line.split()[2])))
                            return False, line.split()[9]
        return False, "fail"

    def __check_port_packets_by_sdk(self, port, count, direc="tx"):
        if(direc == "tx"):
            cmd = "bcmcmd \"show c CLMIB_TPOK\""
            ret, output = subprocess.getstatusoutput(cmd)
            if re.search(r"failed", output):
                showpkt = "CDMIB_TPKT"
                show1518 = "CDMIB_T1518"
            else:
                showpkt = "CLMIB_TPKT"
                show1518 = "CLMIB_T1518"
            cmd = "bcmcmd \"show c %s.%s\"" % (showpkt, self.bcm_ports[port - 1])
            ret, output = subprocess.getstatusoutput(cmd)
            lines = output.split("\n")
            count_pkt = int(re.sub('[,]', '', lines[1].split()[2].strip("+-")))
            log_debug(' '.join(str(s) for s in lines))
            cmd = "bcmcmd \"show c %s.%s\"" % (show1518, self.bcm_ports[port - 1])
            ret, output = subprocess.getstatusoutput(cmd)
            lines = output.split("\n")
            count_1518 = int(re.sub('[,]', '', lines[1].split()[2].strip("+-")))
            log_debug(' '.join(str(s) for s in lines))
            if(lines[1].strip()):
                if(count == count_pkt or count == count_1518):
                    return True, lines[1].split()[2]
                else:
                    return False, lines[1].split()[2]
        elif(direc == "rx"):
            cmd = "bcmcmd \"show c CLMIB_RPOK\""
            ret, output = subprocess.getstatusoutput(cmd)
            if re.search(r"failed", output):
                showpkt = "CDMIB_RPKT"
                show1518 = "CDMIB_R1518"
            else:
                showpkt = "CLMIB_RPKT"
                show1518 = "CLMIB_R1518"
            cmd = "bcmcmd \"show c %s.%s\"" % (showpkt, self.bcm_ports[port - 1])
            ret, output = subprocess.getstatusoutput(cmd)
            lines = output.split("\n")
            count_pkt = int(re.sub('[,]', '', lines[1].split()[2].strip("+-")))
            log_debug(' '.join(str(s) for s in lines))
            cmd = "bcmcmd \"show c %s.%s\"" % (show1518, self.bcm_ports[port - 1])
            ret, output = subprocess.getstatusoutput(cmd)
            lines = output.split("\n")
            count_1518 = int(re.sub('[,]', '', lines[1].split()[2].strip("+-")))
            log_debug(' '.join(str(s) for s in lines))
            if(lines[1].strip()):
                if(count == count_pkt or count == count_1518):
                    return True, lines[1].split()[2]
                else:
                    return False, lines[1].split()[2]
        return False, "fail"

    ################################################################################################

    def get_port_status(self, port):
        if(self.__mode == 0):
            return self.__get_port_status_by_sdk(port)
        elif(self.__mode == 1):
            return self.__get_port_status_by_sonic(port)

    def get_port_fcs_status(self, port):
        tfcs = 0
        rfcs = 0
        cmd = "bcmcmd \"show c CLMIB_TPOK\""
        ret, output = subprocess.getstatusoutput(cmd)
        if re.search(r"failed", output):
            showc = "CDMIB_TFCS"
        else:
            showc = "CLMIB_TFCS"
        cmd = "bcmcmd \"show c %s.%s\"" % (showc, self.bcm_ports[port - 1])
        ret, output = subprocess.getstatusoutput(cmd)
        lines = output.split("\n")
        if lines[1].strip():
            tfcs = int(re.sub('[,]', '', lines[1].split()[2]))
        cmd = "bcmcmd \"show c CLMIB_RPOK\""
        ret, output = subprocess.getstatusoutput(cmd)
        if re.search(r"failed", output):
            showc = "CDMIB_RFCS"
        else:
            showc = "CLMIB_RFCS"
        cmd = "bcmcmd \"show c %s.%s\"" % (showc, self.bcm_ports[port - 1])
        ret, output = subprocess.getstatusoutput(cmd)
        lines = output.split("\n")
        if lines[1].strip():
            rfcs = int(re.sub('[,]', '', lines[1].split()[2]))
        if(tfcs == 0 and rfcs == 0):
            return True, (tfcs, rfcs)
        # print "port = %d, tfcs = %d rfcs = %d" % (port, tfcs, tfcs)
        return False, (tfcs, rfcs)

    def start_send_port_packets(self, port, count, size=64, dst_mac="ff:ff:ff:ff:ff:ff"):
        if(self.__mode == 0):
            return self.__start_send_port_packets_by_sdk(port, count, size, dst_mac)
        elif(self.__mode == 1):
            return self.__start_send_port_packets_by_sonic(port, count, size, dst_mac)
        return False, "fail"

    def stop_send_port_packets(self):
        cmd = "bcmcmd \"port xe,ce en=0\""
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        time.sleep(2)
        cmd = "bcmcmd \"port xe,ce en=1\""
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        time.sleep(30)
        return True, output

    def clear_port_packets(self):
        if(self.__mode == 0):
            return self.__clear_port_packets_by_sdk()
        elif(self.__mode == 1):
            return self.__clear_port_packets_by_sonic()
        return False, "fail"

    def check_port_packets(self, port, count, direc="tx"):
        if(self.__mode == 0):
            return self.__check_port_packets_by_sdk(port, count, direc)
        elif(self.__mode == 1):
            return self.__check_port_packets_by_sonic(port, count, direc)
        return False, "fail"

    def init_port_cpu(self):
        cmd = "bcmcmd \"cint /usr/share/sonic/platform/cpu.cint\""
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        return True, output

    def reset_port_cpu(self):
        cmd = "bcmcmd \"cint;\r\n bcm_field_entry_destroy(0, 2048);\r\n bcm_field_group_destroy(0, 5);\r\n exit;\""
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        return True, output

    def init_port_prbs(self):
        cmd = "bcmcmd \"cint /usr/share/sonic/platform/prbs.cint\""
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        return True, output

    def reset_port_prbs(self):
        time.sleep(1)

    def set_port_prbs(self, port, enable):
        unit_port = self.__get_unit_port_by_bcm(port)
        cmd = "bcmcmd \"cint;\r\n set_port_prbs(%d, %d);\r\n exit;\"" % (unit_port, enable)
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        return True, output

    def get_port_prbs_result(self, port):
        unit_port = self.__get_unit_port_by_bcm(port)
        cmd = "bcmcmd \"cint;\r\n print get_port_prbs_result(%d);\r\n exit;\"" % unit_port
        ret, output = subprocess.getstatusoutput(cmd)
        time.sleep(1)
        cmd = "bcmcmd \"cint;\r\n print get_port_prbs_result(%d);\r\n exit;\"" % unit_port
        ret, output = subprocess.getstatusoutput(cmd)
        lines = output.split("\n")
        status = int(re.findall(" = (.*?) ", lines[-5])[0])
        return status


@Singleton
class PortPrbsTest(object):
    mac_output = []
    sys_output = []
    line_output = []
    bcm_ports = []
    standard = 0

    def __init__(self, standard=1.0e-10):
        self.standard = standard
        self.__get_global_bcmports()

    def __get_global_bcmports(self):
        if(len(self.bcm_ports)):
            pass
        else:
            pu = portutil.PortUtil()
            cmd = "bcmcmd ps"
            ret, output = subprocess.getstatusoutput(cmd)
            lines = output.split("\n")
            for port in pu.device_port_list:
                for line in lines:
                    line.strip()
                    if re.search(r"^.*?\(.*?\)", line) and int(re.findall(r"^.*?\((.*?)\)", line)
                                                               [0].strip()) == port.logic_port:
                        self.bcm_ports.append(re.findall(r"^(.*?)\(.*?\)", line)[0].strip())
                        break

    def _get_mac_side_prbsstat_ber(self, port):
        results = []
        i = 0
        for line in self.mac_output:
            if ((self.bcm_ports[port - 1] + "[0]") in line) or ((self.bcm_ports[port - 1] + "[1]") in line):
                results.append(line)
                i = i + 1
        for result in results:
            i = i - 1
            ex = "[0-9]{0,}[.][0-9]{0,}[e][+][0-9]{0,}|[0-9]{0,}[.][0-9]{0,}[e][-][0-9]{0,}"
            ber = (re.search(ex, result))
            if (ber is not None):
                if (float(ber.group()) > float(self.standard)):
                    return False, results
                elif(i == 0):
                    return True, results
        return False, results

    def _get_sys_side_prbsstat_ber(self, port):
        results = []
        icount = 2
        ex = "[0-9]+$"
        num = (re.search(ex, self.bcm_ports[port - 1])).group()
        num = int(num) * 2 + 1
        results.append(self.sys_output[num])
        results.append(self.sys_output[num + 1])
        for result in results:
            icount = icount - 1
            ex = "[0-9]{0,}[.][0-9]{0,}[e][+][0-9]{0,}|[0-9]{0,}[.][0-9]{0,}[e][-][0-9]{0,}"
            ber = re.search(ex, result)
            if(ber is not None):
                if(float(ber.group()) > float(self.standard)):
                    return False, results
                elif(icount == 0):
                    return True, results
        return False, results

    def _get_line_side_prbsstat_ber(self, port):
        results = []
        icount = 4
        ex = "[0-9]+$"
        num = (re.search(ex, self.bcm_ports[port - 1])).group()
        num = int(num) * 4 + 1
        results.append(self.line_output[num])
        results.append(self.line_output[num + 1])
        results.append(self.line_output[num + 2])
        results.append(self.line_output[num + 3])
        for result in results:
            icount = icount - 1
            ex = "[0-9]{0,}[.][0-9]{0,}[e][+][0-9]{0,}|[0-9]{0,}[.][0-9]{0,}[e][-][0-9]{0,}"
            ber = re.search(ex, result)
            if(ber is not None):
                if(float(ber.group()) > float(self.standard)):
                    return False, results
                elif(icount == 0):
                    return True, results
        return False, results

    def init_port_prbs(self):
        cmd = 'bcmcmd "phy diag ce prbs set p=3"'
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        time.sleep(5)
        cmd = 'bcmcmd "phy control ce prbs lnside=1 p=5"'
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0 or "fail" in output):
            return False, output
        time.sleep(5)
        cmd = 'bcmcmd "phy control ce prbs lnside=0 p=5"'
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0 or "fail" in output):
            return False, output
        time.sleep(5)
        cmd = 'bcmcmd "phy diag ce prbs get"'
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = 'bcmcmd "phy diag ce prbs get"'
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = 'bcmcmd "phy diag ce prbsstat start i=120"'
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = 'bcmcmd "phy control ce prbs lnside=1"'
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        cmd = 'bcmcmd "phy control ce prbs lnside=0"'
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0):
            return False, output
        time.sleep(120)
        cmd = 'bcmcmd "phy control ce prbs lnside=1 time=120 cal=1"'
        ret, output = subprocess.getstatusoutput(cmd)
        self.sys_output = output.split("\r\n")
        if(ret != 0 or "fail" in output):
            return False, output
        cmd = 'bcmcmd "phy control ce prbs lnside=0 time=120 cal=1"'
        ret, output = subprocess.getstatusoutput(cmd)
        self.line_output = output.split("\r\n")
        if(ret != 0 or "fail" in output):
            return False, output
        time.sleep(30)
        cmd = 'bcmcmd "phy diag ce prbsstat ber"'
        ret, output = subprocess.getstatusoutput(cmd)
        self.mac_output = output.split("\r\n")
        if(ret != 0 or "unlock" in output or "fail" in output):
            return False, output
        return True, output

    def clear_port_prbs(self):
        cmd = 'bcmcmd "phy diag ce prbs clear"'
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0 or "fail" in output):
            cmd = 'bcmcmd "phy diag ce prbs clear"'
            ret, output = subprocess.getstatusoutput(cmd)
        time.sleep(5)
        cmd = 'bcmcmd "phy control ce prbs lnside=1 clear=1"'
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0 or "fail" in output):
            cmd = 'bcmcmd "phy control ce prbs lnside=1 clear=1"'
            ret, output = subprocess.getstatusoutput(cmd)
        time.sleep(5)
        cmd = 'bcmcmd "phy control ce prbs lnside=0 clear=1"'
        ret, output = subprocess.getstatusoutput(cmd)
        if(ret != 0 or "fail" in output):
            cmd = 'bcmcmd "phy control ce prbs lnside=0 clear=1"'
            ret, output = subprocess.getstatusoutput(cmd)
        time.sleep(5)
        return True, output

    def get_port_prbs_result(self, flag, port):
        if (flag == "mac"):
            ret, output = self._get_mac_side_prbsstat_ber(port)
            return ret, output
        elif (flag == "sys"):
            ret, output = self._get_sys_side_prbsstat_ber(port)
            return ret, output
        elif (flag == "line"):
            ret, output = self._get_line_side_prbsstat_ber(port)
            return ret, output
        else:
            return False, "fail"


@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
def main():
    '''device operator'''
    pass


@main.command()
def test():
    pk = PortKrTest()
    pk.clear_port_packets()
    ret, result = pk.start_send_port_packets("eth1", vlan=2001)
    # print ret
    # print result
    ret, result = pk.check_port_packets("eth1")
    print(ret)
    print(result)
    pk.clear_port_packets()
    ret, result = pk.start_send_port_packets("eth2", vlan=2002)
    # print ret
    # print result
    ret, result = pk.check_port_packets("eth2")
    print(ret)
    print(result)
    pk.clear_port_packets()


if __name__ == '__main__':
    main()


'''
portts = PortTest()


portts.init_port_prbs()
for i in range(64):
    portts.set_port_prbs((i+1),1)
    #portts.set_port_prbs(2,1)

time.sleep(5)

for i in range(64):
    print portts.get_port_prbs_result((i+1))
    #print portts.get_port_prbs_result(2)

for i in range(64):
    portts.set_port_prbs((i+1),0)


#status = get_port_status(i + 1)
'''
