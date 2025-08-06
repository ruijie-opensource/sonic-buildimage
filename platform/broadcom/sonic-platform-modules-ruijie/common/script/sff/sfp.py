try:
    import sys
    sys.path.append("/usr/local/bin/")
    import os
    import time
    import json
    import collections
    from module_cmis import ModuleCmis
    from logger import logger
    from module_util import ModuleUtil
    from platform_intf import *
    from sonic_platform.sff_conf import sff_conf
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

SFP_TYPE = "SFP"
QSFP_TYPE = "QSFP"
QSFP_DD_TYPE = "QSFP_DD" # CMIS
OSFP_TYPE = "OSFP"

OPTOE1_TYPE = 1
OPTOE2_TYPE = 2
OPTOE3_TYPE = 3

# parse like 'A', 'A-B', 'A, A-B' ... , support port_first_index = 0/1
def _get_config_range_int(range_str):
    if not range_str:
        return []

    int_range_strs = range_str.split(',')
    range_res = []
    for int_range_str in int_range_strs:
        if '-' in int_range_str:
            if sff_conf.get('port_first_index', 1):
                range_s = int(int_range_str.split('-')[0])
                range_e = int(int_range_str.split('-')[1]) + 1
            else:
                range_s = int(int_range_str.split('-')[0]) - 1
                range_e = int(int_range_str.split('-')[1])
        else:
            if sff_conf.get('port_first_index', 1):
                range_s = int(int_range_str)
                range_e = int(int_range_str) + 1
            else:
                range_s = int(int_range_str) - 1
                range_e = int(int_range_str)
        
        #range_res = range_res + range(range_s, range_e)
        range_res = range_res + [x for x in range(range_s, range_e)]

    return range_res

class Sfp(object):
    eeprom_obj = None
    module_util = None
    
    port_num = -1
    port_valid = False
    
    presence_dev_id = -1
    presence_offset = 0
    presence_bit = 0
    
    # for xcvrd, not to change var name
    sfp_type = ""
    
    def __init__(self, index):
        if not self._init_port_info(index):
            return
        
        # TODO update driver type. may better form detected thread
        self.module_util = ModuleUtil.get_instance()
        if self.get_presence():
            if not self.module_util.judge_is_cmis(self.port_e2_key):
                logger.error("current sfp_type is not CMIS!")
                return
            else:
                self.module_util.set_optoe_driver(self.port_e2_key, OPTOE3_TYPE)
                self.sfp_type = QSFP_DD_TYPE
                self.eeprom_obj = ModuleCmis.get_instance()

    def _get_conf_cpld_info(self, cpld_info):
        if not not cpld_info:
            dev_info = cpld_info.get('dev_id')
            if not not dev_info:
                for dev_id in dev_info:
                    offset_info = dev_info[dev_id].get('offset')
                    if not not offset_info:
                        for offset in offset_info:
                            ports = _get_config_range_int(offset_info[offset])
                            if self.port_num in ports:
                                return True, dev_id, offset, ports.index(self.port_num)
        
        return False, None, None, None

    def _init_port_info(self, index):
        self.port_num = index
        
        if sff_conf.get('port_first_index', 1):
            self.port_e2_key = index
        else:
            self.port_e2_key = index + 1
        
        self.port_valid = False
        if sff_conf.get('port_first_index', 1):
            if self.port_num in range(1, sff_conf.get('ports_num', 0) + 1):
                self.port_valid = True
        else:
            if self.port_num in range(0, sff_conf.get('ports_num', 0)):
                self.port_valid = True
        if not self.port_valid:
            logger.error("port num %d invalid" % self.port_num)
            return False
        
        presence_cpld_info = sff_conf.get('presence_cpld_info')
        ret, dev_id, offset, offset_bit = self._get_conf_cpld_info(presence_cpld_info)
        if ret:
            self.presence_dev_id = dev_id
            self.presence_offset = offset
            self.presence_bit = offset_bit
        
        return True

    def get_presence(self):
        if not self.port_valid or self.presence_dev_id < 0:
            return False
        
        ret, info = platform_reg_read(0, self.presence_dev_id, self.presence_offset, 1)
        if not ret:
            logger.error("platform_reg_read fail:%s" % info)
            return False
        
        # get target bit val
        flag_on = 0
        if info[0] & (1 << self.presence_bit):
            flag_on = 1
        
        ret = False
        # 1-present
        if sff_conf.get('present_val', 0):
            if flag_on:
                ret =  True
        else:
            if not flag_on:
                ret =  True
        
        return ret

    def get_transceiver_basic_info(self):
        if not self.get_presence():
            logger.warning("Module not present!")
            return None
        if not self.eeprom_obj:
            logger.error("Current Module type not support!")
            return None
        
        return self.eeprom_obj.get_transceiver_basic_info(self.port_e2_key)

    def get_transceiver_imp_info(self):
        if not self.get_presence():
            logger.warning("Module not present!")
            return None
        if not self.eeprom_obj:
            logger.error("Current Module type not support!")
            return None
        
        return self.eeprom_obj.get_transceiver_imp_info(self.port_e2_key)

    def get_transceiver_dom_info(self):
        if not self.get_presence():
            logger.warning("Module not present!")
            return None
        if not self.eeprom_obj:
            logger.error("Current Module type not support!")
            return None

        return self.eeprom_obj.get_transceiver_dom_info(self.port_e2_key)

    def set_transceiver_loopback(self, side, dir, enable):
        if not self.get_presence():
            logger.warning("Module not present!")
            return False
        if not self.eeprom_obj:
            logger.error("Current Module type not support!")
            return None
        
        if self.sfp_type == QSFP_DD_TYPE:
            return self.eeprom_obj.set_transceiver_loopback(self.port_e2_key, side, dir, enable)
        else:
            return False

    def get_transceiver_dom_alarm_info(self):
        if not self.get_presence():
            logger.warning("Module not present!")
            return None
        if not self.eeprom_obj:
            logger.error("Current Module type not support!")
            return None
        
        return self.eeprom_obj.get_transceiver_dom_alarm_info(self.port_e2_key)

    def get_vdm_basic_current_info(self):
        if not self.get_presence():
            logger.warning("Module not present!")
            return False
        if not self.eeprom_obj:
            logger.error("Current Module type not support!")
            return None
        
        if self.sfp_type == QSFP_DD_TYPE:
            return self.eeprom_obj.get_vdm_basic_current_info(self.port_e2_key)
        else:
            return False

    def get_vdm_supported_type_info(self):
        if not self.get_presence():
            logger.warning("Module not present!")
            return False
        if not self.eeprom_obj:
            logger.error("Current Module type not support!")
            return None
        
        if self.sfp_type == QSFP_DD_TYPE:
            return self.eeprom_obj.get_vdm_supported_type_info(self.port_e2_key)
        else:
            return False

    def get_vdm_basic_stat_info(self):
        if not self.get_presence():
            logger.warning("Module not present!")
            return False
        if not self.eeprom_obj:
            logger.error("Current Module type not support!")
            return None
        
        if self.sfp_type == QSFP_DD_TYPE:
            return self.eeprom_obj.get_vdm_basic_stat_info(self.port_e2_key)
        else:
            return False

    def get_vdm_basic_alarm_info(self):
        if not self.get_presence():
            logger.warning("Module not present!")
            return False
        if not self.eeprom_obj:
            logger.error("Current Module type not support!")
            return None
        
        if self.sfp_type == QSFP_DD_TYPE:
            return self.eeprom_obj.get_vdm_basic_alarm_info(self.port_e2_key)
        else:
            return False

    def get_vdm_datapath_current_info(self):
        if not self.get_presence():
            logger.warning("Module not present!")
            return False
        if not self.eeprom_obj:
            logger.error("Current Module type not support!")
            return None
        
        if self.sfp_type == QSFP_DD_TYPE:
            return self.eeprom_obj.get_vdm_datapath_current_info(self.port_e2_key)
        else:
            return False

    def get_vdm_datapath_stat_info(self):
        if not self.get_presence():
            logger.warning("Module not present!")
            return False
        if not self.eeprom_obj:
            logger.error("Current Module type not support!")
            return None
        
        if self.sfp_type == QSFP_DD_TYPE:
            return self.eeprom_obj.get_vdm_datapath_stat_info(self.port_e2_key)
        else:
            return False

    def get_vdm_datapath_alarm_info(self):
        if not self.get_presence():
            logger.warning("Module not present!")
            return False
        if not self.eeprom_obj:
            logger.error("Current Module type not support!")
            return None
        
        if self.sfp_type == QSFP_DD_TYPE:
            return self.eeprom_obj.get_vdm_datapath_alarm_info(self.port_e2_key)
        else:
            return False

    def get_datapath_configure_info(self):
        if not self.get_presence():
            logger.warning("Module not present!")
            return None
        if not self.eeprom_obj:
            logger.error("Current Module type not support!")
            return None
        
        if self.sfp_type == QSFP_DD_TYPE:
            return self.eeprom_obj.get_datapath_configure_info(self.port_e2_key)
        else:
            return False

    def set_lf_insertion_on_ld(self, side, ena):
        if not self.get_presence():
            logger.warning("Module not present!")
            return None
        
        if not self.eeprom_obj:
            logger.error("Current Module type not support!")
            return None
        
        if self.sfp_type == QSFP_DD_TYPE:
            return self.eeprom_obj.set_lf_insertion_on_ld(self.port_e2_key, side, ena)
        else:
            return False

    def read_eeprom_info(self, page, page_offset, num_bytes):
        if not self.get_presence():
            logger.warning("Module not present!")
            return False, []
        
        return self.module_util.read_eeprom_specific_bytes(self.port_e2_key, page, page_offset, num_bytes)
    
    def write_eeprom_info(self, page, page_offset, val):
        if not self.get_presence():
            logger.warning("Module not present!")
            return False
        
        return self.module_util.write_eeprom_specific_bytes(self.port_e2_key, page, page_offset, val)

