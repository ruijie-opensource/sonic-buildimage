try:
    import sys
    sys.path.append("/usr/local/bin")
    import os
    import time
    import collections
    from math import log10
    import binascii
    from sff8024 import *
    from sffcom import *
    from ctypes import create_string_buffer
    from logger import logger
    from platform_intf import *
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

def get_bits_val(data, bits):
    retval = 0
    try:
        off_right = 0
        for i in range(0, 8):
            if bits & (1 << i):
                off_right = i
                break
        retval = (data & bits) >> off_right
    except Exception as err:
        logger.error(str(err))
    
    return retval

def convert_hex_to_string(data_raw):
    try:
        res_str = ''
        for val in data_raw:
            res_str += val
        return str.strip(binascii.unhexlify(res_str).decode())
    except Exception as err:
        return str(err)

def convert_date_to_string(data_raw):
    try:
        year_offset  = 0
        month_offset = 2
        day_offset   = 4
        lot_offset   = 6

        date = convert_hex_to_string(data_raw)
        retval = "20"+ date[year_offset : year_offset + 2] + "-" + \
                date[month_offset : month_offset + 2] + "-" + \
                date[day_offset : day_offset + 2] + " " + \
                date[lot_offset : lot_offset + 2]
        return retval
    except Exception as err:
        return str(err)

def convert_lsb_first_data_to_long(data_raw):
    val = 0
    try:
        for i in range(0, len(data_raw)):
            val |= int(data_raw[i], 16) << (8 * i)
        
    except Exception as err:
        logger.error(str(err))
    
    return val

def convert_msb_first_data_to_long(data_raw):
    val = 0
    try:
        data_raw.reverse()
        for i in range(0, len(data_raw)):
            val |= int(data_raw[i], 16) << (8 * i)
    except Exception as err:
        logger.error(str(err))
    
    return val

def twos_comp(num, bits):
    try:
        if ((num & (1 << (bits - 1))) != 0):
            num = num - (1 << bits)
        return num
    except:
        return 0

def mw_to_dbm(mW):
    if mW == 0:
        return float("-inf")
    elif mW < 0:
        return float("NaN")
    return 10. * log10(mW)

def test_bit(n, bitpos):
    try:
        mask = 1 << bitpos
        if (n & mask) == 0:
            return False
        else:
            return True
    except:
        return False

def calc_temperature(data_raw):
    retval = 'N/A'
    try:
        msb = int(data_raw[0], 16)
        lsb = int(data_raw[1], 16)
        result = (msb << 8) | (lsb & 0xff)
        result = twos_comp(result, 16)
        
        result = float(result / 256.0)
        retval = '%.4f' %result + 'C'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_voltage(data_raw):
    retval = 'N/A'
    try:
        msb = int(data_raw[0], 16)
        lsb = int(data_raw[1], 16)
        result = (msb << 8) | (lsb & 0xff)
        
        result = float(result * 0.0001)
        retval = '%.4f' %result + 'Volts'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_power(data_raw):
    retval = 'N/A'
    try:
        msb = int(data_raw[0], 16)
        lsb = int(data_raw[1], 16)
        result = (msb << 8) | (lsb & 0xff)
        
        result = float(result * 0.0001)
        retval = "%.4f%s" % (mw_to_dbm(result), "dBm")
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_bias(data_raw):
    retval = 'N/A'
    try:
        msb = int(data_raw[0], 16)
        lsb = int(data_raw[1], 16)
        result = (msb << 8) | (lsb & 0xff)
        
        result = float(result * 0.002)
        retval = '%.4f' % result + 'mA'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_media_id(data_raw):
    retval = 'N/A'
    try:
        media_type = type_of_media_interface.get(data_raw[0])
        if media_type == 'Undefined' or not media_type:
            return retval
        
        if data_raw[0] == '01': 
            retval = nm_850_media_interface.get(data_raw[2])
        elif data_raw[0] == '02': 
            retval = sm_media_interface.get(data_raw[2])
        elif data_raw[0] == '03': 
            retval = passive_copper_media_interface.get(data_raw[2])
        elif data_raw[0] == '04': 
            retval = active_cable_media_interface.get(data_raw[2])
        elif data_raw[0] == '05': 
            retval = base_t_media_interface.get(data_raw[2])
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_cmis_power_class(data_raw):
    retval = 'N/A'
    try: 
        class_data = int(data_raw[0], 16)
        power_data = int(data_raw[1], 16)
        data_high3 = (class_data & 0xe0) >> 5
        
        class_str = ext_type_of_transceiver.get(str(data_high3))
        power = power_data * 0.25
        power_str = ' (%d W max. )' % power
        retval = class_str + power_str
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_cmis_loopback(data_raw):
    retval = 'N/A'
    try: 
        data = int(data_raw[0], 16)
        if data == 0xff:
            retval = 'True'
        else:
            retval = 'False'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_ber_f16(data_raw):
    retval = 'N/A'
    try:
        # from cmis-Table 8-98 Encoding for BER/FERC
        msb = int(data_raw[1], 16)
        lsb = int(data_raw[0], 16)
        
        exponent = (lsb & 0xf8) >> 3
        mantissa = msb | ((lsb & 0x07) << 8)
        retval = mantissa * (10 ** (exponent - 24))
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_laser_age(data_raw):
    retval = 'N/A'
    try:
        msb = int(data_raw[0], 16)
        lsb = int(data_raw[1], 16)
        
        result = (msb << 8) | (lsb & 0xff)
        retval = str(result) + '%'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_laser_frequency_error(data_raw):
    retval = 'N/A'
    try:
        msb = int(data_raw[0], 16)
        lsb = int(data_raw[1], 16)
        
        result = (msb << 8) | (lsb & 0xff)
        retval = str(result * 10) + 'MHZ'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_vdm_config(data_raw):
    retval = 'N/A'
    try:
        retval = {}
        for i in range(0, 64):
            msb = int(data_raw[i*2], 16)
            lsb = int(data_raw[i*2+1], 16)
            type = cmis_vdm_conf_type_info.get(lsb, 'N/A')
            threshold_id = (msb & 0xf0) >> 4
            dsc_raw = msb & 0x0f
            dsc = cmis_vdm_conf_lane_info.get(dsc_raw, 'N/A')
            
            if type == 'N/A':
                continue
            retval[i] = {}
            retval[i]['Type'] = type
            retval[i]['Threshold ID'] = threshold_id
            retval[i]['Dsc'] = dsc
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_vdm_val_raw(data_raw):
    retval = 'N/A'
    try:
        retval = {}
        for i in range(0, 64):
            data = data_raw[i*2 : i*2+2]
            
            retval[i] = data
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_vdm_alarm_raw(data_raw):
    retval = 'N/A'
    try:
        retval = {}
        for i in range(0, 128):
            retval[i*2+1] = {}
            retval[i*2+2] = {}
            for j in range(1, 3):
                dict_tmp = retval[i*2+j]
                dict_tmp['HighAlarm'] = 'False'
                dict_tmp['LowAlarm'] = 'False'
                dict_tmp['HighWarning'] = 'False'
                dict_tmp['LowWarning'] = 'False'
            data = int(data_raw[i], 16)
            if data & 0x1:
                retval[i*2+1]['HighAlarm'] = 'True'
            if data & 0x2:
                retval[i*2+1]['LowAlarm'] = 'True'
            if data & 0x4:
                retval[i*2+1]['HighWarning'] = 'True'
            if data & 0x8:
                retval[i*2+1]['LowWarning'] = 'True'
            if data & 0x10:
                retval[i*2+2]['HighAlarm'] = 'True'
            if data & 0x20:
                retval[i*2+2]['LowAlarm'] = 'True'
            if data & 0x40:
                retval[i*2+2]['HighWarning'] = 'True'
            if data & 0x80:
                retval[i*2+2]['LowWarning'] = 'True'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_vdm_val(type, data_raw):
    if not type or type == 'N/A':
        return 'N/A'
    
    if type == 1:
        return calc_laser_age(data_raw)
    elif type == 2:
        return calc_tec_current(data_raw)
    elif type == 3:
        return calc_laser_frequency_error(data_raw)
    elif type == 4:
        return calc_temperature(data_raw)
    elif type in range(5, 9):
        return calc_snr(data_raw)
    elif type in range(9, 25):
        return calc_ber_f16(data_raw)
    elif type in range(128, 134):
        return calc_modulator_bias(data_raw)
    elif type in range(134, 136):
        return calc_cd(data_raw)
    elif type == 136:
        return calc_dgd(data_raw)
    elif type == 137:
        return calc_sopmd(data_raw)
    elif type == 138:
        return calc_pdl(data_raw)
    elif type == range(139, 141):
        return calc_snr(data_raw)
    elif type == 141:
        return calc_cfo(data_raw)
    elif type == 142:
        return calc_evmmodem(data_raw)
    elif type == range(143, 146):
        return calc_vdm_power(data_raw)
    elif type == 146:
        return calc_sopcr(data_raw)
    elif type == 147:
        return calc_mer(data_raw)
    else:
        return 'N/A'

def calc_cmis_cdb_support(data_raw):
    retval = 'N/A'
    try:
        if int(data_raw[0], 16) >> 6 != 0:
            retval = 'True'
        else:
            retval = 'False'
    except Exception as err:
        logger.error(str(err))
    
    return retval


##########
def calc_modulator_bias(data_raw):
    retval = 'N/A'
    try:
        result = convert_msb_first_data_to_long(data_raw)
        result *= 100.0 / 65535
        retval = '%.4f' % result + ' %'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_cd(data_raw):
    retval = 'N/A'
    try:
        result = convert_msb_first_data_to_long(data_raw)
        result = twos_comp(result, len(data_raw) * 8)
        retval = '%d' % result + ' ps/nm'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_dgd(data_raw):
    retval = 'N/A'
    try:
        result = convert_msb_first_data_to_long(data_raw)
        result *= 0.01
        retval = '%.2f' % result + ' ps'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_sopmd(data_raw):
    retval = 'N/A'
    try:
        result = convert_msb_first_data_to_long(data_raw)
        result *= 0.01 * 0.01
        retval = '%.4f' % result + ' ps^2'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_pdl(data_raw):
    retval = 'N/A'
    try:
        result = convert_msb_first_data_to_long(data_raw)
        result *= 0.01
        retval = '%.2f' % result + ' dB'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_snr(data_raw):
    retval = 'N/A'
    try:
        result = convert_msb_first_data_to_long(data_raw)
        result *= 0.01
        retval = '%.2f' % result + ' dB'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_cfo(data_raw):
    retval = 'N/A'
    try:
        result = convert_msb_first_data_to_long(data_raw)
        result = twos_comp(result, len(data_raw) * 8)
        retval = '%d' % result + ' MHz'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_evmmodem(data_raw):
    retval = 'N/A'
    try:
        result = convert_msb_first_data_to_long(data_raw)
        result *= 100 / 65535.0
        retval = '%.4f' % result + ' %'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_vdm_power(data_raw):
    retval = 'N/A'
    try:
        result = convert_msb_first_data_to_long(data_raw)
        result = twos_comp(result, len(data_raw) * 8)
        result *= 0.01
        retval = '%.4f' % result + ' dBm'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_sopcr(data_raw):
    retval = 'N/A'
    try:
        result = convert_msb_first_data_to_long(data_raw)
        retval = '%d' % result + ' krads/s'
    except Exception as err:
        logger.error(str(err))
    
    return retval

def calc_mer(data_raw):
    retval = 'N/A'
    try:
        result = convert_msb_first_data_to_long(data_raw)
        result *= 0.01
        retval = '%2f' % result + ' dB'
    except Exception as err:
        logger.error(str(err))
    
    return retval


########################################################

OPTOE1_TYPE = 1
OPTOE2_TYPE = 2
OPTOE3_TYPE = 3

class ModuleUtil():

    I2C_MAX_ATTEMPT = 3
    
    @classmethod
    def get_instance(cls):
        if not hasattr(ModuleUtil, '_instance'):
            ModuleUtil._instance = ModuleUtil()
        return ModuleUtil._instance

    def _get_absolute_offset(self, page, offset):
        if page == 0x0 or offset < 128:
            return offset
        
        return page * 128 + offset

    def read_eeprom_specific_bytes(self, e2_key, page, offset_p, num_bytes):
        eeprom_raw = []
        attempts = 0
        while attempts < self.I2C_MAX_ATTEMPT:
            offset = self._get_absolute_offset(page, offset_p)
            ret, info = platform_sfp_read(e2_key, offset, num_bytes)
            if ret:
                if not info:
                    logger.info("%d %d %d %d read abnormal, may invalid read" %(e2_key, page, offset_p, num_bytes))
                    break
                
                for n in range(0, num_bytes):
                    eeprom_raw.append(hex(info[n])[2:].zfill(2))
                break
            else:
                attempts += 1
                time.sleep(0.05)
                logger.error("platform_sfp_read fail:%s" % info)
        
        ret = True
        if len(eeprom_raw) != num_bytes:
            ret = False
        return ret, eeprom_raw

    # write_buffer: int list or int val
    def write_eeprom_specific_bytes(self, e2_key, page, offset_p, write_buffer):
        #todo 一次最多写32byte数据
        val_list = []
        if isinstance(write_buffer, list):
            val_list = write_buffer
        else:
            val_list.append(write_buffer)
        
        offset = self._get_absolute_offset(page, offset_p)
        ret, info = platform_sfp_write(e2_key, offset, val_list)
        time.sleep(0.01)
        
        if ret:
            return True
        else:
            logger.error("%d %d %d %s platform_sfp_write fail:%s" % (e2_key, page, offset_p, str(write_buffer), info))
            return False

    def parse_info(self, e2_key, dict_info):
        info_dict = {}
        if not dict_info:
            return info_dict
        
        try:
            offset_min = 0xff
            offset_max = 0
            for key in dict_info['info']:
                obj = dict_info['info'][key]
                if not obj.get('valid'):
                    continue
                cur_offset_min = obj['offset']
                cur_offset_max = obj['offset'] + obj.get('size', 1)
                if cur_offset_min < offset_min:
                    offset_min = cur_offset_min
                if cur_offset_max > offset_max:
                    offset_max = cur_offset_max
            
            offset_total = offset_min
            size_total = offset_max - offset_min
            if size_total < 0:
                return info_dict
            
            ret, data_raw_total = self.read_eeprom_specific_bytes(e2_key, dict_info['page'], offset_total, size_total)
            if not ret:
                logger.error("read fail")
                return info_dict
            
            for key in dict_info['info']:
                obj = dict_info['info'][key]
                type = obj.get('type')
                if not obj.get('valid') or not type:
                    continue
                
                info_dict[key] = 'N/A'
                start = obj['offset'] - offset_total
                end = start + obj.get('size', 1)
                data_raw = data_raw_total[start : end]
                
                if type == 'enum':
                    info_dict[key] = obj['decode'].get(data_raw[0], 'N/A')
                elif type == 'func':
                    info_dict[key] = obj['decode'](data_raw)
                elif type == 'str':
                    info_dict[key] = convert_hex_to_string(data_raw)
                elif type == 'hex':
                    info_dict[key] = '-'.join(data_raw[0 : len(data_raw)])
                elif type == 'date':
                    info_dict[key] = convert_date_to_string(data_raw)
                elif type == 'int':
                    info_dict[key] = int(data_raw[0], 16)
                elif type == 'bit':
                    data = int(data_raw[0], 16)
                    bitpos = obj['bit']
                    bitval = test_bit(data, bitpos)
                    info_dict[key] = [False, True][bitval]
                elif type == 'long_lsb_first':
                    info_dict[key] = convert_lsb_first_data_to_long(data_raw)
                elif type == 'enum_bits':
                    val = get_bits_val(int(data_raw[0], 16), obj['bits'])
                    info_dict[key] = obj['decode'].get(val, 'N/A')
                elif type == 'int_bits':
                    val = get_bits_val(int(data_raw[0], 16), obj['bits'])
                    info_dict[key] = val
                else:
                    logger.error("unsupport type: %s" % type)
        except Exception as err:
            logger.error(str(err))
        
        return info_dict

    def parse_multi_page_info(self, e2_key, dict_info):
        info_dict = {}
        if not dict_info:
            return info_dict
        try:
            for page in dict_info['page']:
                dict_target = {}
                dict_target['page'] = page
                dict_target['info'] = dict_info['page'][page]['info']
                info_dict.update(self.parse_info(e2_key, dict_target))
        except Exception as err:
            logger.error(str(err))
        
        return info_dict

    def judge_is_cmis(self, e2_key):
        try:
            ret = False
            rv, data_raw = self.read_eeprom_specific_bytes(e2_key, 0, 128, 1)
            if not rv:
                return False
            
            # TODO only 1e? from baidu doc
            if data_raw[0] == '1e' or data_raw[0] == '18':
                ret = True
        except Exception as err:
            logger.error(str(err))
        
        return ret

    def set_optoe_driver(self, e2_key, optoe_type):
        if optoe_type < 1 or optoe_type > 3:
            logger.error("invalid  optoe_type:%d" % optoe_type)
            return False
        
        ret, info = platform_get_optoe_type(e2_key)
        if not ret:
            logger.error("platform_get_optoe_type fail:%s" % info)
            return False
        
        if info == optoe_type:
            return True
        
        ret, info = platform_set_optoe_type(e2_key, optoe_type)
        if not ret:
            logger.error("platform_set_optoe_type fail:%s" % info)
            return False
        else:
            logger.info("optoe driver change to: optoe%d" % optoe_type)
            return True



