try:
    import os
    import copy
    import re
    from module_util import ModuleUtil
    from sff8024 import *
    from sffcom import *
    from cmis_parsed_info import *
    from logger import logger
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

FW_IMG_TYPE_APP = "App"
FW_IMG_TYPE_DSP = "Dsp"
CDB_CMD_LEN = 8
CDB_CMD_PAGE = 0x9f
CDB_CMD_STATUS_PAGE = 0
CDB_CMD_STATUS_OFFSET = 37
CDB_CMD_CODE_OFFSET = 128
CDB_CMD_DATA_OFFSET = 130
CDB_CMD_TIME_INTER_S = 0.1
CDB_CMD_TIME_TIMEOUT_S = 10

CDB_LPL_MAX_WRITE_SIZE = 116
CDB_LPL_LEN_OFFSET = 132
CDB_LPL_REPLY_OFFSET = 136
CDB_CHK_CODE_OFFSET = 133

CDB_CMD_SUCCESS_STATUS = '01'

class ModuleCmis(object):

    DRV_TYPE = "optoe3"
    
    module_util = ModuleUtil.get_instance()

    @classmethod
    def get_instance(cls):
        if not hasattr(ModuleCmis, '_instance'):
            ModuleCmis._instance = ModuleCmis()

        return ModuleCmis._instance

    def read_eeprom(self, e2_key, page, offset, num_bytes):
        return self.module_util.read_eeprom_specific_bytes(e2_key, page, offset, num_bytes)
    
    def write_eeprom(self, e2_key, page, offset, write_buffer):
        return self.module_util.write_eeprom_specific_bytes(e2_key, page, offset, write_buffer)

    def get_transceiver_basic_info(self, e2_key):
        info_dict = self.module_util.parse_info(e2_key, parsed_basic_info)
        info_dict.update(self.module_util.parse_info(e2_key, parsed_adv_info))

        return info_dict

    def get_transceiver_imp_info(self, e2_key):
        info_dict = self.module_util.parse_multi_page_info(e2_key, parsed_imp_info)
        
        return info_dict

    def get_transceiver_dom_info(self, e2_key):
        info_dict = {}
        imp_info = self.get_transceiver_imp_info(e2_key)
        if not imp_info:
            return info_dict
        parsed_dict_tmp = copy.deepcopy(parsed_module_monitors_info)
        
        if not imp_info.get('TempMonitorImplemented'):
            parsed_dict_tmp['info']['ModuleTemperature']['valid'] = False
        if not imp_info.get('VoltMonitorImplemented'):
            parsed_dict_tmp['info']['SupplyVoltage']['valid'] = False
        
        info_dict.update(self.module_util.parse_info(e2_key, parsed_dict_tmp))
        
        parsed_dict_tmp = copy.deepcopy(parsed_lane_monitors_info)
        
        lane_max = int(self.get_transceiver_basic_info(e2_key)['MediaLaneCount'])
        for key in parsed_dict_tmp['info']:
            if re.match(r'.*x.*Power.*', key):
                lane = int("".join(list(filter(str.isdigit, key))))
                if lane > lane_max:
                    parsed_dict_tmp['info'][key]['valid'] = False
        
        if not imp_info.get('TxPowerMonitorImplemented'):
            for key in parsed_dict_tmp['info']:
                if re.match(r'.*Tx.*Power.*', key):
                    parsed_dict_tmp['info'][key]['valid'] = False
        if not imp_info.get('RxPowerMonitorImplemented'):
            for key in parsed_dict_tmp['info']:
                if re.match(r'.*Rx.*Power.*', key):
                    parsed_dict_tmp['info'][key]['valid'] = False
        
        info_dict.update(self.module_util.parse_info(e2_key, parsed_dict_tmp))
        
        return info_dict

    def get_transceiver_dom_alarm_info(self, e2_key):
        info_dict = {}
        imp_info = self.get_transceiver_imp_info(e2_key)
        if not imp_info:
            return info_dict
        parsed_dict_tmp = copy.deepcopy(parsed_dom_monitors_interrupt_info)
        
        if not imp_info.get('TempMonitorImplemented'):
            for key in parsed_dict_tmp['info']:
                if re.match(r'.*Temp.*', key):
                    parsed_dict_tmp['info'][key]['valid'] = False
        if not imp_info.get('VoltMonitorImplemented'):
            for key in parsed_dict_tmp['info']:
                if re.match(r'.*Vcc.*', key):
                    parsed_dict_tmp['info'][key]['valid'] = False
        
        info_dict.update(self.module_util.parse_info(e2_key, parsed_dict_tmp))
        
        parsed_dict_tmp = copy.deepcopy(parsed_dom_chnl_monitors_interrupt_info)
        
        lane_max = int(self.get_transceiver_basic_info(e2_key)['MediaLaneCount'])
        for key in parsed_dict_tmp['info']:
            if re.match(r'.*x.*Power.*', key) or re.match(r'.*LOS', key):
                lane = int("".join(list(filter(str.isdigit, key))))
                if lane > lane_max:
                    parsed_dict_tmp['info'][key]['valid'] = False
        
        if not imp_info.get('TxPowerMonitorImplemented'):
            for key in parsed_dict_tmp['info']:
                if re.match(r'.*Tx.*Power.*', key):
                    parsed_dict_tmp['info'][key]['valid'] = False
        if not imp_info.get('RxPowerMonitorImplemented'):
            for key in parsed_dict_tmp['info']:
                if re.match(r'.*Rx.*Power.*', key):
                    parsed_dict_tmp['info'][key]['valid'] = False
        if not imp_info.get('RxLOSImplemented'):
            for key in parsed_dict_tmp['info']:
                if re.match(r'.*Rx.*LOS.*', key):
                    parsed_dict_tmp['info'][key]['valid'] = False
        
        info_dict.update(self.module_util.parse_info(e2_key, parsed_dict_tmp))
        
        return info_dict

    def set_transceiver_loopback(self, e2_key, side, dir, enable):
        imp_info = self.get_transceiver_imp_info(e2_key)
        if not imp_info:
            return False
        
        page = parsed_diag1_info['page']
        offset_p = 0
        key_str = ''
        if side:
            key_str += 'Host'
        else:
            key_str += 'Media'
        if dir:
            key_str += 'Tx'
        else:
            key_str += 'Rx'
        
        key_str += 'Loopback'
        key_str_imp = key_str + 'Implemented'
        
        if not imp_info.get(key_str_imp):
            logger.warning("%s not Implemented!" % key_str_imp)
            return False
        
        offset_p = parsed_diag1_info['info'][key_str]['offset']
        data = 0
        if enable:
            data = 0xff
        
        return self.write_eeprom(e2_key, page, offset_p, data)

    def get_transceiver_vdm_parameter_info(self, e2_key):
        info_dict = {}
        vdm_id = 0
        
        imp_info = self.get_transceiver_imp_info(e2_key)
        if not imp_info:
            return info_dict
        if not imp_info.get('VDMImplemented'):
            logger.warning("VDM not Implemented!")
            return info_dict
        
        info_dict_tmp = self.module_util.parse_info(e2_key, parsed_vdm_group1_conf_info)['VDMGroupConfig']
        for key in info_dict_tmp:
            vdm_id = key + 1
            info_dict[vdm_id] = {}
            for key2 in info_dict_tmp[key]:
                if key2 == 'Threshold ID':
                    info_dict[vdm_id][key2] = info_dict_tmp[key][key2] + 1
                    continue
                info_dict[vdm_id][key2] = info_dict_tmp[key][key2]
        
        info_dict_tmp = self.module_util.parse_info(e2_key, parsed_vdm_group2_conf_info)['VDMGroupConfig']
        for key in info_dict_tmp:
            vdm_id = key + 65
            info_dict[vdm_id] = {}
            for key2 in info_dict_tmp[key]:
                if key2 == 'Threshold ID':
                    info_dict[vdm_id][key2] = info_dict_tmp[key][key2] + 17
                    continue
                info_dict[vdm_id][key2] = info_dict_tmp[key][key2]
        
        info_dict_tmp = self.module_util.parse_info(e2_key, parsed_vdm_group3_conf_info)['VDMGroupConfig']
        for key in info_dict_tmp:
            vdm_id = key + 129
            info_dict[vdm_id] = {}
            for key2 in info_dict_tmp[key]:
                if key2 == 'Threshold ID':
                    info_dict[vdm_id][key2] = info_dict_tmp[key][key2] + 33
                    continue
                info_dict[vdm_id][key2] = info_dict_tmp[key][key2]
        
        info_dict_tmp = self.module_util.parse_info(e2_key, parsed_vdm_group4_conf_info)['VDMGroupConfig']
        for key in info_dict_tmp:
            vdm_id = key + 193
            info_dict[vdm_id] = {}
            for key2 in info_dict_tmp[key]:
                if key2 == 'Threshold ID':
                    info_dict[vdm_id][key2] = info_dict_tmp[key][key2] + 49
                    continue
                info_dict[vdm_id][key2] = info_dict_tmp[key][key2]
        
        return info_dict

    def _get_target_vdm_id_type_info(self, e2_key, target_types):
        info_dict = {}
        vdm_parameter_info = self.get_transceiver_vdm_parameter_info(e2_key)
        for type in target_types:
            for vdm_id in vdm_parameter_info:
                if vdm_parameter_info[vdm_id]['Type'] == cmis_vdm_conf_type_info.get(type):
                    info_dict[vdm_id] = type
                    break
        
        return info_dict
    
    def _get_group_ids(self, vdm_ids):
        group_ids = {}
        for i in range(1, 5):
            group_ids[i] = []
        
        for vdm_id in vdm_ids:
            if vdm_id >= 1 and vdm_id <= 64:
                group_ids[1].append(vdm_id)
            elif vdm_id >= 65 and vdm_id <= 128:
                group_ids[2].append(vdm_id)
            elif vdm_id >= 129 and vdm_id <= 192:
                group_ids[3].append(vdm_id)
            elif vdm_id >= 193 and vdm_id <= 256:
                group_ids[4].append(vdm_id)
        
        return group_ids

    def get_vdm_supported_type_info(self, e2_key):
        info_dict = {}
        vdm_parameter_info = self.get_transceiver_vdm_parameter_info(e2_key)
        for vdm_id in vdm_parameter_info:
            info_dict[vdm_id] = vdm_parameter_info[vdm_id]['Type']
        
        return info_dict

    def get_vdm_real_time_info(self, e2_key, target_types):
        info_dict = {}
        
        vdm_id_type_info = self._get_target_vdm_id_type_info(e2_key, target_types)
        group_ids = self._get_group_ids(vdm_id_type_info.keys())
        
        for group_id in group_ids:
            if not group_ids[group_id]:
                continue
            
            group_data_raw_info = {}
            if group_id == 1:
                group_data_raw_info = self.module_util.parse_info(e2_key, parsed_vdm_group1_val_info)['VDMGroupVal']
            elif group_id == 2:
                group_data_raw_info = self.module_util.parse_info(e2_key, parsed_vdm_group2_val_info)['VDMGroupVal']
            elif group_id == 3:
                group_data_raw_info = self.module_util.parse_info(e2_key, parsed_vdm_group3_val_info)['VDMGroupVal']
            elif group_id == 4:
                group_data_raw_info = self.module_util.parse_info(e2_key, parsed_vdm_group4_val_info)['VDMGroupVal']

            data_raw_index = 0
            for vdm_id in group_ids[group_id]:
                data_raw_index = (vdm_id - 1) % 64
                data_raw = group_data_raw_info[data_raw_index]
                
                vdm_type = vdm_id_type_info[vdm_id]
                info_dict[cmis_vdm_conf_type_info.get(vdm_type)] = calc_vdm_val(vdm_type, data_raw)

        return info_dict

    def get_vdm_basic_current_info(self, e2_key):
        target_types = cust_target_vdm_basic_cur_type
        return self.get_vdm_real_time_info(e2_key, target_types)

    def get_vdm_basic_stat_info(self, e2_key):
        target_types = cust_target_vdm_basic_stat_type
        return self.get_vdm_real_time_info(e2_key, target_types)

    def get_vdm_basic_alarm_info(self, e2_key):
        info_dict = {}
        
        target_types = cust_target_vdm_basic_alarm_type
        vdm_id_type_info = self._get_target_vdm_id_type_info(e2_key, target_types)
        data_info = self.module_util.parse_info(e2_key, parsed_vdm_alarm_info)['VDMAlarmVal']
        for vdm_id in vdm_id_type_info.keys():
            vdm_type = vdm_id_type_info[vdm_id]
            info_dict[cmis_vdm_conf_type_info.get(vdm_type)] = {}
            for key in data_info[vdm_id]:
                info_dict[cmis_vdm_conf_type_info.get(vdm_type)][key] = data_info[vdm_id][key]

        return info_dict

    def _jduge_is_400ZR(self, e2_key):
        basic_info = self.get_transceiver_basic_info(e2_key)
        ret = False
        if basic_info.get('MediaInterface') == sm_media_interface.get('3e') or \
                basic_info.get('MediaInterface') == sm_media_interface.get('3f'):
            ret = True
        
        return ret

    def get_vdm_datapath_current_info(self, e2_key):
        info_dict = {}
        
        if not self._jduge_is_400ZR(e2_key):
            logger.warning("not 400ZR, not Support!")
            return {}
        
        target_types = cust_target_vdm_datapath_cur_type
        info_dict.update(self.get_vdm_real_time_info(e2_key, target_types))
        
        return info_dict

    def get_vdm_datapath_stat_info(self, e2_key):
        info_dict = {}
        
        if not self._jduge_is_400ZR(e2_key):
            logger.warning("not 400ZR, not Support!")
            return {}
        
        parsed_dict_tmp = parsed_media_lane_link_performance_monitoring
        info_dict.update(self.module_util.parse_info(e2_key, parsed_dict_tmp))
        
        parsed_dict_tmp = parsed_media_lane_fec_performance_monitoring
        info_dict.update(self.module_util.parse_info(e2_key, parsed_dict_tmp))
        
        parsed_dict_tmp = parsed_host_interface_performance_monitoring
        info_dict.update(self.module_util.parse_info(e2_key, parsed_dict_tmp))
        
        return info_dict
    
    def get_vdm_datapath_alarm_info(self, e2_key):
        info_dict = {}
        
        if not self._jduge_is_400ZR(e2_key):
            logger.warning("not 400ZR, not Support!")
            return {}
        
        parsed_dict_tmp = parsed_media_lane_flags
        info_dict.update(self.module_util.parse_info(e2_key, parsed_dict_tmp))
        
        parsed_dict_tmp = parsed_host_interface_flags
        info_dict.update(self.module_util.parse_info(e2_key, parsed_dict_tmp))
        
        return info_dict

    def get_datapath_configure_info(self, e2_key):
        info_dict = {}
        
        if not self._jduge_is_400ZR(e2_key):
            logger.warning("not 400ZR, not Support!")
            return {}
        
        parsed_dict_tmp = parsed_host_interface_conf
        info_dict.update(self.module_util.parse_info(e2_key, parsed_dict_tmp))
        
        parsed_dict_tmp = parsed_media_lane_prov
        info_dict.update(self.module_util.parse_info(e2_key, parsed_dict_tmp))
        
        return info_dict

    def set_lf_insertion_on_ld(self, e2_key, side, ena):
        page = 0
        offset = 0
        bit = 0
        
        if not self._jduge_is_400ZR(e2_key):
            logger.warning("not 400ZR, not Support!")
            return False
        
        if side:
            page = parsed_host_interface_conf['page']
            offset = parsed_host_interface_conf['info']['HostLfInsertionOnLdEnable']['offset']
            bit = parsed_host_interface_conf['info']['HostLfInsertionOnLdEnable']['bit']
        else:
            page = parsed_media_lane_prov['page']
            offset = parsed_media_lane_prov['info']['MediaLfInsertionOnLdEnable']['offset']
            bit = parsed_media_lane_prov['info']['MediaLfInsertionOnLdEnable']['bit']
        
        data = 0
        ret, data_raw = self.read_eeprom(e2_key, page, offset, 1)
        if not ret:
            logger.error("read eeprom fail")
            return False
        
        data_ori = int(data_raw[0], 16)
        if ena:
            data = data_ori | (1 << bit)
        else:
            data = data_ori & (~(1 << bit))
        
        return self.write_eeprom(e2_key, page, offset, data)

