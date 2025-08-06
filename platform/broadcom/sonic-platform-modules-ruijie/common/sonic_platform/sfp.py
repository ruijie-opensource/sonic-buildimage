# -*- coding: UTF-8 -*-
#############################################################################
# Ruijie
#
# Module contains an implementation of SONiC Platform Base API and
# provides the platform information
#
#############################################################################
import sys
import time
import syslog
import traceback

try:
    import os
    from sonic_platform_base.sonic_xcvr.sfp_optoe_base import SfpOptoeBase

except ImportError as e:
    raise ImportError (str(e) + "- required module not found")

LOG_DEBUG_LEVEL  = 1
LOG_WARNING_LEVEL  = 2
LOG_ERROR_LEVEL  = 3

EEPROM_RETRY = 5
EEPROM_RETRY_BREAK_SEC = 0.2

SYSFS_VAL_IS_PRESENT = 1
SYSFS_VAL_IS_RESET = 1
SYSFS_VAL_IS_LPMODE = 1

class Sfp(SfpOptoeBase):

    QSFP_DEVICE_TYPE = 1
    SFP_DEVICE_TYPE  = 2
    CMIS_DEVICE_TYPE = 3

    def __init__(self, index):
        SfpOptoeBase.__init__(self)
        self._port_id = index
        self._optoe_type = None
        self.log_level = 1
        self.sfp_type = None
        # self._set_log_level(self._get_config("sfp_log_level"))

    def get_eeprom_path(self):
        return self._get_config("eeprom_path") % self._port_id or None

    def read_eeprom(self, offset, num_bytes):
        eeprom_path = self.get_eeprom_path()
        if eeprom_path is None:
            self._log_error("eeprom_path is None")
            return False
        try:
            for i in range(EEPROM_RETRY):
                with open(eeprom_path, mode='rb', buffering=0) as f:
                    f.seek(offset)
                    result = f.read(num_bytes)
                    if len(result) < num_bytes:
                        result = result[::-1].zfill(num_bytes)[::-1]
                    if result is not None:
                        return bytearray(result)
                    time.sleep(EEPROM_RETRY_BREAK_SEC)
                    continue

        except Exception as err:
            print(traceback.format_exc())

        return None

    def write_eeprom(self, offset, num_bytes, write_buffer):
        eeprom_path = self.get_eeprom_path()
        if eeprom_path is None:
            self._log_error("eeprom_path is None")
            return False
        try:
            for i in range(EEPROM_RETRY):
                with open(eeprom_path, "wb+") as eeprom:
                    eeprom.seek(offset)
                    ret = eeprom.write(write_buffer[0:num_bytes])
                time.sleep(0.01)
                if ret is False:
                    time.sleep(EEPROM_RETRY_BREAK_SEC)
                    continue
                break
        except Exception as e:
            self._log_error(traceback.format_exc(e))
            return False
        return True

    def get_presence(self):
        try:
            presence_sysfs_path = self._get_config("presence_path") % self._port_id
            ret, result = self._read_sysfs(presence_sysfs_path)
            if ret is False:
                return False
            return result == SYSFS_VAL_IS_PRESENT
        except Exception as err:
            self._log_error(traceback.format_exc(err))

        return False

    def get_transceiver_info(self):
        # temporary solution for a SONiC community bug
        transceiver_info = super().get_transceiver_info()
        try:
            if transceiver_info["vendor_rev"] is not None:
                transceiver_info["hardware_rev"] = transceiver_info["vendor_rev"]
            return transceiver_info
        except Exception as e:
            print(traceback.format_exc())

    def get_reset_status(self):
        if not self.get_presence():
            return False

        if self.sfp_type is None:
            self.refresh_xcvr_api()

        if self.sfp_type == 'SFP':
            self._log_warning('SFP does not support reset')
            return False

        try:
            reset_sysfs_path = self._get_config("reset_path") % self._port_id
            ret, result = self._read_sysfs(reset_sysfs_path)
            if ret is False:
                return False
            return result == SYSFS_VAL_IS_RESET
        except Exception as err:
            self._log_error(traceback.format_exc(err))
        return False

    def reset(self):
        if self.get_presence() is False:
            return False

        if self.sfp_type is None:
            self.refresh_xcvr_api()

        if self.sfp_type == 'SFP':
            self._log_warning('SFP does not support reset')
            return False

        self._log_debug('port_num:%d resetting...' % self._port_id)
        ret = self._set_reset(True)
        if ret:
            time.sleep(0.5)
            ret = self._set_reset(False)

        return ret

    def get_lpmode(self):
        if not self.get_presence():
            return False

        if self.sfp_type is None:
            self.refresh_xcvr_api()

        if self.sfp_type == 'SFP':
            self._log_warning('SFP does not support lpmode')
            return False

        try:
            lpmode_sysfs_path = self._get_config("lpmode_path") % self._port_id
            ret, result = self._read_sysfs(lpmode_sysfs_path)
            if ret is False:
                return False
            return result == SYSFS_VAL_IS_LPMODE
        except Exception as err:
            self._log_error(traceback.format_exc(err))

        return False

    def set_lpmode(self, lpmode):
        if not self.get_presence():
            return False

        if self.sfp_type is None or self._xcvr_api is None:
            self.refresh_xcvr_api()

        if self.sfp_type == 'QSFP_DD':
            return SfpOptoeBase.set_lpmode(self, lpmode)
        elif self.sfp_type == 'QSFP':
            if lpmode:
                return self._xcvr_api.set_power_override(True, lpmode)
            else:
                return self._xcvr_api.set_power_override(False, lpmode)
        else:
            self._log_warning('SFP does not support lpmode')
            return False

    def get_rx_los(self):
        """
        Retrieves the RX LOS (lost-of-signal) status of SFP
        Returns:
            A Boolean, True if SFP has RX LOS, False if not.
            Note : RX LOS status is latched until a call to get_rx_los or a reset.
        """
        if not self.get_presence():
            return False

        if self.sfp_type is None:
            self.refresh_xcvr_api()

        try:
            sysfs_path = self._get_config("rx_los_path") % self._port_id
            ret, result = self._read_sysfs(sysfs_path)
            if ret is False:
                return False
            return result
        except Exception as err:
            self._log_error(traceback.format_exc(err))

        return False

    def get_tx_fault(self):
        """
        Retrieves the TX fault status of SFP
        Returns:
            A Boolean, True if SFP has TX fault, False if not
            Note : TX fault status is lached until a call to get_tx_fault or a reset.
        """
        if not self.get_presence():
            return False

        if self.sfp_type is None:
            self.refresh_xcvr_api()

        try:
            sysfs_path = self._get_config("tx_fault_path") % self._port_id
            ret, result = self._read_sysfs(sysfs_path)
            if ret is False:
                return False
            return result
        except Exception as err:
            self._log_error(traceback.format_exc(err))

        return False

    def get_tx_disable(self):
        """
        Retrieves the tx_disable status of this SFP

        Returns:
            A Boolean, True if tx_disable is enabled, False if disabled
        """
        if not self.get_presence():
            return False

        if self.sfp_type is None:
            self.refresh_xcvr_api()

        try:
            sysfs_path = self._get_config("tx_dis_path") % self._port_id
            ret, result = self._read_sysfs(sysfs_path)
            if ret is False:
                return False
            return result
        except Exception as err:
            self._log_error(traceback.format_exc(err))

        return False

    def tx_disable(self, tx_disable):
        """
        Disable SFP TX for all channels

        Args:
            tx_disable : A Boolean, True to enable tx_disable mode, False to disable
                         tx_disable mode.

        Returns:
            A boolean, True if tx_disable is set successfully, False if not
        """
        if self.get_presence() is False:
            return False

        if self.sfp_type is None:
            self.refresh_xcvr_api()

        self._log_debug('port_num:%d set tx_diable...' % self._port_id)
        return self._set_tx_disable(tx_disable)

    def set_optoe_write_max(self, write_max):
        """
        This func is declared and implemented by SONiC but we're not supported
        so override it as NotImplemented
        """
        self._log_debug("set_optoe_write_max NotImplemented")
        pass

    def refresh_xcvr_api(self):
        """
        Updates the XcvrApi associated with this SFP
        """
        self._xcvr_api = self._xcvr_api_factory.create_xcvr_api()

        self.class_name = self._xcvr_api.__class__.__name__
        self._get_device_type(self.class_name)
        if self._optoe_type is not None:
            self._set_optoe_type(self._optoe_type)


#################### inner api ####################

    def _get_device_type(self, class_name):
        if (class_name == 'CmisApi'):
            self._optoe_type = self.CMIS_DEVICE_TYPE
            self.sfp_type = 'QSFP_DD'
        elif (class_name == 'Sff8472Api'):
            self._optoe_type = self.SFP_DEVICE_TYPE
            self.sfp_type = 'SFP'
        elif (class_name == 'Sff8636Api') or (class_name == 'Sff8436Api'):
            self._optoe_type = self.QSFP_DEVICE_TYPE
            self.sfp_type = 'QSFP'
        else:
            self._log_error("get_device_type error, class_name not supported:%s" % class_name)
            self._optoe_type = None
            self.sfp_type = None

    def _set_optoe_type(self, optoe_type):
        optoe_sysfs_path = self._get_config("optoe_path") % self._port_id
        try:
            with open(optoe_sysfs_path, "r+") as sysfs_file:
                sysfs_file_val = sysfs_file.read(-1)
                if int(sysfs_file_val) != optoe_type:
                    dc_str = "%s" % str(optoe_type)
                    sysfs_file.write(dc_str)
        except Exception as err:
            self._log_error(traceback.format_exc())
            return False
        return True

    def _set_reset(self, reset):
        try:
            reset_sysfs_path = self._get_config("reset_path") % self._port_id
            ret, result = self._read_sysfs(reset_sysfs_path)
            if ret is False:
                return False
            if reset:
                result = SYSFS_VAL_IS_RESET
            else:
                result = 0

            ret = self._write_sysfs(reset_sysfs_path, result)
            if ret is False:
                return False
        except Exception as err:
            self._log_error(traceback.format_exc())
            return False
        return True

    def _set_tx_disable(self, disable):
        try:
            sysfs_path = self._get_config("tx_dis_path") % self._port_id
            ret, result = self._read_sysfs(sysfs_path)
            if ret is False:
                return False
            if disable:
                result = 1
            else:
                result = 0

            ret = self._write_sysfs(sysfs_path, result)
            if ret is False:
                return False
        except Exception as err:
            self._log_error(traceback.format_exc())
            return False
        return True

    def _read_sysfs(self, sysfs_path):
        val = 0
        if sysfs_path is None:
            self._log_error("sysfs_path is None")
            return False, 0

        try:
            with open(sysfs_path, "rb") as data:
                sysfs_data = data.read(2)
                if sysfs_data != "":
                    val = int(sysfs_data, 16)
        except Exception as err:
            self._log_error(traceback.format_exc(err))
            return False, 0

        return True, val

    def _write_sysfs(self, sysfs_path, val):
        if sysfs_path is None:
            self._log_error("sysfs_path is None")
            return False

        try:
            with open(sysfs_path, "r+") as data:
                data.seek(0)
                sres = hex(val)[2:]
                data.write(sres)
        except Exception as err:
            self._log_error(traceback.format_exc(err))
            return False

        self._log_debug("write sysfs_path:%s success, val:%d" % (sysfs_path, val))
        return True

    def _get_config(self, key=None, default_val=None):
        config = {
            "sfp_log_level": 1,
            "presence_path": "/sys/s3ip/transceiver/eth%d/present",
            "eeprom_path": "/sys/s3ip/transceiver/eth%d/eeprom",
            "lpmode_path": "/sys/s3ip/transceiver/eth%d/low_power_mode",
            "reset_path": "/sys/s3ip/transceiver/eth%d/reset",
            "tx_dis_path": "/sys/s3ip/transceiver/eth%d/tx_disable",
            "rx_los_path": "/sys/s3ip/transceiver/eth%d/rx_los",
            "tx_fault_path": "/sys/s3ip/transceiver/eth%d/tx_fault",
            "optoe_path": "/sys/s3ip/transceiver/eth%d/optoe_type",
        }
        return config.get(key, default_val)

    ####### SfpLog class #####

    def _set_log_level(self, level):
        if (level == LOG_DEBUG_LEVEL
            or level == LOG_ERROR_LEVEL):
            self.log_level = level
        else:
            self.log_error("unavailable loglevel:%d" % level)

    def _log_debug(self, msg):
        if self.log_level <= LOG_DEBUG_LEVEL:
            try:
                syslog.openlog("Sfp")
                syslog.syslog(syslog.LOG_DEBUG, msg)
                syslog.closelog()

            except Exception as e:
                msg = traceback.format_exc(e)

    def _log_warning(self, msg):
        if self.log_level <= LOG_WARNING_LEVEL:
            try:
                syslog.openlog("Sfp")
                syslog.syslog(syslog.LOG_WARNING, msg)
                syslog.closelog()

            except Exception as e:
                msg = traceback.format_exc(e)
                print("Exception_info:\n%s" % msg)

    def _log_error(self, msg):
        if self.log_level <= LOG_ERROR_LEVEL:
            try:
                syslog.openlog("Sfp")
                syslog.syslog(syslog.LOG_ERR, msg)
                syslog.closelog()

            except Exception as e:
                msg = traceback.format_exc(e)
                print("Exception_info:\n%s" % msg)

