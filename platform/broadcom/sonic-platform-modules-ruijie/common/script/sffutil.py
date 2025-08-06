#!/usr/bin/python3
try:
    import click
    import json
    import collections
    import sys
    sys.path.append("/usr/local/bin/sff/")
    from sffcom import *
    from sfp import Sfp
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

class BasedIntParamType(click.ParamType):
    name = "integer"

    def convert(self, value, param, ctx):
        try:
            if value[:2].lower() == "0x":
                return int(value[2:], 16)
            elif value[:1] == "0":
                return int(value, 8)
            return int(value, 10)
        except Exception as err:
            print("invalid int str")

BASED_INT = BasedIntParamType()

TAB_STR = "    "
def get_sorted_dict(info_dict):
    sorted_keys = sorted(info_dict.keys())
    buty_dict = collections.OrderedDict()
    for key in sorted_keys:
        if type(info_dict[key]) == dict:
            buty_dict[key] = get_sorted_dict(info_dict[key])
        else:
            buty_dict[key] = info_dict[key]
    
    return buty_dict

def dump_ordered_dict(info_dict, levels):
    for key in info_dict:
        if isinstance(info_dict[key], collections.OrderedDict):
            print(TAB_STR * levels + str(key) + ":")
            levels += 1
            dump_ordered_dict(info_dict[key], levels)
            levels -= 1
        else:
            print(TAB_STR * levels +  str(key) + ": " + str(info_dict[key]))


def dump_buty_dict(info_dict):
    if not info_dict:
        print(TAB_STR + 'N/A')
        return
    
    buty_dict = get_sorted_dict(info_dict)
    dump_ordered_dict(buty_dict, 1)

@click.group()
def sff():
    ''' Module Diag '''
    pass

@sff.group()
def eeprom():
    ''' EEPROM Diag '''
    pass

@sff.group()
def show():
    ''' Show Diag '''
    pass

@sff.group()
def set():
    ''' Set Diag '''
    pass

@eeprom.command()
@click.argument('port_num', required=True, type=BASED_INT)
@click.argument('page', required=True, type=BASED_INT)
@click.argument('offset', required=True, type=BASED_INT)
@click.argument('size', required=True, type=BASED_INT)
def read(port_num, page, offset, size):
    tsfp = Sfp(port_num)
    
    if offset < 128 and page != 0:
        print("Page or Offset invalid")
        return False
    ret, data = tsfp.read_eeprom_info(page, offset, size)
    if ret:
        print("Module:%d Page:0x%x Offset:%d Size:%d EEPROM Read Success, Info:" % (port_num, page, offset, size))
        for i in range(0, len(data)):
            print(str(data[i]) + ' ', end = '')
            if ((i + 1) % 16 == 0):
                print('')
        print('')
    else:
        print("Module:%d Page:0x%x Offset:%d Size:%d EEPROM Read Fail" % (port_num, page, offset, size))

@eeprom.command()
@click.argument('port_num', required=True, type=BASED_INT)
@click.argument('page', required=True, type=BASED_INT)
@click.argument('offset', required=True, type=BASED_INT)
@click.argument('val', required=True, type=BASED_INT)
def write(port_num, page, offset, val):
    tsfp = Sfp(port_num)
    
    ret = 'Success'
    if not tsfp.write_eeprom_info(page, offset, val):
        ret = 'Fail'
    print("Module:%d Page:0x%x Offset:%d Val:0x%x EEPROM  Write %s" % (port_num, page, offset, val, ret))

@show.command()
@click.argument('port_num', required=True, type=BASED_INT)
def presence(port_num):
    tsfp = Sfp(port_num)
    
    print("Module:%d Present:%s" % (port_num, tsfp.get_presence()))

@show.command()
@click.argument('port_num', required=True, type=BASED_INT)
def basic_info(port_num):
    tsfp = Sfp(port_num)
    
    print("Module:%d Basic Info:" % (port_num))
    dump_buty_dict(tsfp.get_transceiver_basic_info())

@show.command()
@click.argument('port_num', required=True, type=BASED_INT)
def impl_info(port_num):
    tsfp = Sfp(port_num)
    
    print("Module:%d Implemented Info:" % (port_num))
    dump_buty_dict(tsfp.get_transceiver_imp_info())

@show.command()
@click.argument('port_num', required=True, type=BASED_INT)
def ddm_cur_info(port_num):
    tsfp = Sfp(port_num)
    
    print("Module:%d DDM Cur Info:" % (port_num))
    dump_buty_dict(tsfp.get_transceiver_dom_info())

@show.command()
@click.argument('port_num', required=True, type=BASED_INT)
def ddm_alarm_info(port_num):
    tsfp = Sfp(port_num)
    
    print("Module:%d DDM Alarm Info:" % (port_num))
    dump_buty_dict(tsfp.get_transceiver_dom_alarm_info())

@show.command()
@click.argument('port_num', required=True, type=BASED_INT)
def vdm_basic_cur_info(port_num):
    tsfp = Sfp(port_num)
    
    print("Module:%d VDM Basic Cur Info:" % (port_num))
    dump_buty_dict(tsfp.get_vdm_basic_current_info())

@show.command()
@click.argument('port_num', required=True, type=BASED_INT)
def vdm_basic_stat_info(port_num):
    tsfp = Sfp(port_num)
    
    print("Module:%d VDM Basic Stat Info:" % (port_num))
    dump_buty_dict(tsfp.get_vdm_basic_stat_info())

@show.command()
@click.argument('port_num', required=True, type=BASED_INT)
def vdm_basic_alarm_info(port_num):
    tsfp = Sfp(port_num)
    
    print("Module:%d VDM Basic Alarm Info:" % (port_num))
    dump_buty_dict(tsfp.get_vdm_basic_alarm_info())

@show.command()
@click.argument('port_num', required=True, type=BASED_INT)
def vdm_supported_type_info(port_num):
    tsfp = Sfp(port_num)
    
    print("Module:%d VDM Supported Type Info:" % (port_num))
    dump_buty_dict(tsfp.get_vdm_supported_type_info())

@show.command()
@click.argument('port_num', required=True, type=BASED_INT)
def vdm_datapath_cur_info(port_num):
    tsfp = Sfp(port_num)
    
    print("Module:%d VDM Datapath Cur Info:" % (port_num))
    dump_buty_dict(tsfp.get_vdm_datapath_current_info())

@show.command()
@click.argument('port_num', required=True, type=BASED_INT)
def vdm_datapath_stat_info(port_num):
    tsfp = Sfp(port_num)
    
    print("Module:%d VDM Datapath Stat Info:" % (port_num))
    dump_buty_dict(tsfp.get_vdm_datapath_stat_info())

@show.command()
@click.argument('port_num', required=True, type=BASED_INT)
def vdm_datapath_alarm_info(port_num):
    tsfp = Sfp(port_num)
    
    print("Module:%d VDM Datapath Alarm Info:" % (port_num))
    dump_buty_dict(tsfp.get_vdm_datapath_alarm_info())

@set.command()
@click.argument('port_num', required=True, type=BASED_INT)
@click.argument('side', required=True, type=bool)
@click.argument('dir', required=True, type=bool)
@click.argument('ena', required=True, type=bool)
def loopback(port_num, side, dir, ena):
    tsfp = Sfp(port_num)
    
    ret = 'Success'
    if not tsfp.set_transceiver_loopback(side, dir, ena):
        ret = 'Fail'
    print("Module:%d Side:%s Dir:%s Enable:%s Set Loopback %s" % (port_num, ['MediaSide', 'HostSide'][side], ['Rx', 'Tx'][dir], ena, ret))

@show.command()
@click.argument('port_num', required=True, type=BASED_INT)
def datapath_conf_info(port_num):
    tsfp = Sfp(port_num)
    
    print("Module:%d Ctrl Info:" % (port_num))
    dump_buty_dict(tsfp.get_datapath_configure_info())

@set.command()
@click.argument('port_num', required=True, type=BASED_INT)
@click.argument('side', required=True, type=bool)
@click.argument('ena', required=True, type=bool)
def lf_insert_on_ld(port_num, side, ena):
    tsfp = Sfp(port_num)
    
    ret = 'Success'
    if not tsfp.set_lf_insertion_on_ld(side, ena):
        ret = 'Fail'
    print("Module:%d Side:%s Enable:%s Set LfInsertionOnLd %s" % (port_num, ['MediaSide', 'HostSide'][side], ena, ret))


sff()
