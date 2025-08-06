# -*- coding: utf-8 -*-
########################################################################
# Ruijie
#
# Module contains an implementation of SONiC Platform Base API and
# provides the PSUs' information which are available in the platform
#
########################################################################
try:
    import os
    import time
    import sys
    from sonic_platform.util import read_sysfs, NULL_VALUE
    from sonic_platform.logger import sonic_platform_logger
    from sonic_platform_base.psu_base import PsuBase
    from sonic_platform.fan import Fan
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

class Psu(PsuBase):
    """Ruijie Platform-specific PSU class"""

    def __init__(self, index):
        PsuBase.__init__(self)
        self.logger = sonic_platform_logger()
        self._fan_list = []
        self._thermal_list = []
        self.index = index
        self.fan1_index = 1
        self.name = "PSU" + str(index)

        self._fan_list.append(Fan(self.fan1_index, psu_fan = True, psu_index = index, psu_obj = self))

    def get_name(self):
        """
        Retrieves the name of the device

        Returns:
            string: The name of the device
        """
        return "Psu{}".format(self.index)

    def get_presence(self):
        """
        Retrieves the presence of the Power Supply Unit (PSU)

        Returns:
            bool: True if PSU is present, False if not
        """
        attr_path = "/sys/s3ip/psu/psu{}/present".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            if int(tmp_value) == 0:
                return False
            else:
                return True
        self.logger.log_error("sysfs access failed. %s" % attr_path)
        return False
    
    def get_direction(self):
        """
        Retrieves the fan airflow direction
        Returns:
            A string, either FAN_DIRECTION_INTAKE or FAN_DIRECTION_EXHAUST
            depending on fan direction

        Notes:
            - Forward/Exhaust : Air flows from Port side to Fan side.
            - Reverse/Intake  : Air flows from Fan side to Port side.
        """
        attr_path = "/sys/s3ip/psu/psu{}/fan_direction".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return int(tmp_value)
        self.logger.log_error("sysfs access failed. %s" % attr_path)
        return NULL_VALUE

    def get_model(self):
        """
        Retrieves the part number of the PSU

        Returns:
            string: Part number of PSU
        """
        attr_path = "/sys/s3ip/psu/psu{}/model_name".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return tmp_value
        self.logger.log_error("sysfs access failed. %s" % attr_path)
        return NULL_VALUE

    def get_serial(self):
        """
        Retrieves the serial number of the PSU

        Returns:
            string: Serial number of PSU
        """
        attr_path = "/sys/s3ip/psu/psu{}/serial_number".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return tmp_value
        self.logger.log_error("sysfs access failed. %s" % attr_path)
        return NULL_VALUE

    def get_speed_rpm(self):
        """
        Retrieves the speed (eg. 7840) of the PSU

        Returns:
             An integer: speed of PSU's fan
        """
        attr_path = "/sys/s3ip/psu/psu{}/fan_speed".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return int(tmp_value)
        self.logger.log_error("sysfs access failed. %s" % attr_path)
        return 0
    
    def get_speed_rpm_max(self):
        """
 
        Retrieves the max fan speed of the PSU

        Returns:
            integer
       
        """
        attr_path = "/sys/s3ip/psu/psu{}/fan_speed_max".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return int(tmp_value)
        self.logger.log_error("sysfs access failed. %s" % attr_path)
        return 0

    def get_speed_rpm_min(self):
        """
 
        Retrieves the min fan speed of the PSU

        Returns:
            integer
       
        """
        attr_path = "/sys/s3ip/psu/psu{}/fan_speed_min".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return int(tmp_value)
        self.logger.log_error("sysfs access failed. %s" % attr_path)
        return 0

    def get_status(self):
        """
        Retrieves the operational status of the PSU

        Returns:
            bool: True if PSU is operating properly, False if not
        """
        attr_path_out_status = "/sys/s3ip/psu/psu{}/out_status".format(self.index)
        attr_path_in_status = "/sys/s3ip/psu/psu{}/in_status".format(self.index)
        #0:不正常
        #1:正常
        ret1, out_status = read_sysfs(attr_path_out_status)
        if ret1 is False:
            self.logger.log_error("sysfs access failed. %s" % attr_path_out_status)
            return False

        ret2, in_status = read_sysfs(attr_path_in_status)
        if ret2 is False:
            self.logger.log_error("sysfs access failed. %s" % attr_path_in_status)
            return False
        
        if int(out_status) == 1 and int(in_status) == 1:
            return True
        else:
            self.logger.log_debug("psu%d get_status. in_stauts=%s, out_status=%s" % (self.index, out_status, in_status))
            return False

    def get_psu_status_fr_pmbus(self):
        """
        Retrieves the status of the PSU from pmbus

        Returns:
            integer
        """
        attr_path_pmbus_status = "/sys/s3ip/psu/psu{}/status_fr_pmbus".format(self.index)
        ret, pmbus_status = read_sysfs(attr_path_pmbus_status)
        if ret is False:
            self.logger.log_error("sysfs access failed. %s" % attr_path_pmbus_status)
            return NULL_VALUE
        
        pmbus_status = int(pmbus_status)
        if ((pmbus_status & 0xff) == 0xff or (pmbus_status & 0xff00) == 0xff00):
            self.logger.log_error("psu%d get_psu_status_fr_pmbus. pmbus stauts=%s. value is 0xff" % (self.index, pmbus_status))
            return NULL_VALUE

        self.logger.log_debug("psu%d get_psu_status_fr_pmbus. pmbus stauts=%s" % (self.index, pmbus_status))
        return pmbus_status
 
    def get_position_in_parent(self):
        """
        Retrieves 1-based relative physical position in parent device. If the agent cannot determine the parent-relative position
        for some reason, or if the associated value of entPhysicalContainedIn is '0', then the value '-1' is returned
        Returns:
            integer: The 1-based relative physical position in parent device or -1 if cannot determine the position
        """
        return -1

    def is_replaceable(self):
        """
        Indicate whether this device is replaceable.
        Returns:
            bool: True if it is replaceable.
        """
        return True

    def get_voltage(self):
        """
        Retrieves current PSU voltage output

        Returns:
            A float number, the output voltage in volts,
            e.g. 12.1
        """
        attr_path = "/sys/s3ip/psu/psu{}/out_vol".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return round(float(tmp_value)/1000, 1)
        self.logger.log_error("sysfs access failed. %s" % attr_path)

        return 0.0

    def get_current(self):
        """
        Retrieves present electric current supplied by PSU

        Returns:
            A float number, electric current in amperes,
            e.g. 15.4
        """
        attr_path = "/sys/s3ip/psu/psu{}/out_curr".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return round(float(tmp_value)/1000, 1)
        self.logger.log_error("sysfs access failed. %s" % attr_path)

        return 0.0

    def get_power(self):
        """
        Retrieves current energy supplied by PSU

        Returns:
            A float number, the power in watts,
            e.g. 302.6
        """
        attr_path = "/sys/s3ip/psu/psu{}/out_power".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return round(float(tmp_value)/1000000, 1)
        self.logger.log_error("sysfs access failed. %s" % attr_path)

        return 0.0

    def get_powergood_status(self):
        """
        Retrieves the powergood status of PSU

        Returns:
            A boolean, True if PSU has stablized its output voltages and
            passed all its internal self-tests, False if not.
        """
        return self.get_status()

    def get_input_voltage(self):
        """
        Get the input voltage of the PSU

        Returns:
            A float number, the input voltage in volts,
        """
        attr_path = "/sys/s3ip/psu/psu{}/in_vol".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return round(float(tmp_value)/1000, 1)
        self.logger.log_error("sysfs access failed. %s" % attr_path)

        return 0.0

    def get_input_current(self):
        """
        Get the input electric current of the PSU

        Returns:
            A float number, the input current in amperes, e.g 220.3
        """
        attr_path = "/sys/s3ip/psu/psu{}/in_curr".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return round(float(tmp_value)/1000, 1)
        self.logger.log_error("sysfs access failed. %s" % attr_path)

        return 0.0

    def get_input_power(self):
        """
        Get the input current energy of the PSU

        Returns:
            A float number, the input power in watts, e.g. 302.6
        """
        attr_path = "/sys/s3ip/psu/psu{}/in_power".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return round(float(tmp_value)/1000000, 1)
        self.logger.log_error("sysfs access failed. %s" % attr_path)

        return 0.0

    def get_revision(self):
        """
        Retrieves the hardware revision of the device

        Returns:
            string: Revision value of device
        """
        attr_path = "/sys/s3ip/psu/psu{}/hardware_version".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return tmp_value
        self.logger.log_error("sysfs access failed. %s" % attr_path)

        return NULL_VALUE

    def get_vendor(self):
        """
        Retrieves the vendor name of the psu

        Returns:
            string: Vendor name of psu
        """
        return "Ruijie"

    def get_maximum_supplied_power(self):
        """
        Retrieves the maximum supplied power by PSU

        Returns:
            A float number, the maximum power output in Watts.
            e.g. 1200.1
        """
        attr_path = "/sys/s3ip/psu/psu{}/out_max_power".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return round(float(tmp_value)/1000000, 1)
        self.logger.log_error("sysfs access failed. %s" % attr_path)

        return 0.0

    def get_temperature(self):
        """
        Retrieves current temperature reading from PSU

        Returns:
            A float number of current temperature in Celsius up to nearest thousandth
            of one degree Celsius, e.g. 30.125
        """
        attr_path = "/sys/s3ip/psu/psu{}/temp1/value".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return round(float(tmp_value)/1000, 1)
        self.logger.log_error("sysfs access failed. %s" % attr_path)

        return 0.0

    def get_temperature_high_threshold(self):
        """
        Retrieves the high threshold temperature of PSU

        Returns:
            A float number, the high threshold temperature of PSU in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        attr_path = "/sys/s3ip/psu/psu{}/temp1/max".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return round(float(tmp_value)/1000, 1)
        self.logger.log_error("sysfs access failed. %s" % attr_path)

        return 0.0
    
    def get_status_led(self):
        """
        Gets the state of the PSU status LED

        Returns:
            A string, one of the predefined STATUS_LED_COLOR_* strings.
        """
        PSU_STATUS_UNNORMAL = 0
        if not self.get_presence():
            return "N/A"
        in_status_path = "/sys/s3ip/psu/psu{}/in_status".format(self.index)
        out_status_path = "/sys/s3ip/psu/psu{}/out_status".format(self.index)
        ret, in_status_value = read_sysfs(in_status_path)
        if ret is False:
            self.logger.log_error("sysfs access failed. %s" % in_status_path)
            return self.STATUS_LED_COLOR_RED
        ret, out_status_value = read_sysfs(out_status_path)
        if ret is False:
            self.logger.log_error("sysfs access failed. %s" % out_status_path)
            return self.STATUS_LED_COLOR_RED
        
        if (int(out_status_value) == PSU_STATUS_UNNORMAL) or (int(in_status_value) == PSU_STATUS_UNNORMAL):
            return self.STATUS_LED_COLOR_RED
        return self.STATUS_LED_COLOR_GREEN
    
    def get_voltage_high_threshold(self):
        """
        Retrieves the high threshold PSU voltage output

        Returns:
            A float number, the high threshold output voltage in volts,
            e.g. 12.1
        """
        attr_path = "/sys/s3ip/psu/psu{}/out_vol_max".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return round(float(tmp_value)/1000, 1)
        self.logger.log_error("sysfs access failed. %s" % attr_path)
        return 0

    def get_voltage_low_threshold(self):
        """
        Retrieves the low threshold PSU voltage output

        Returns:
            A float number, the low threshold output voltage in volts,
            e.g. 12.1
        """
        attr_path = "/sys/s3ip/psu/psu{}/out_vol_min".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return round(float(tmp_value)/1000, 1)
        self.logger.log_error("sysfs access failed. %s" % attr_path)
        return 0

    def get_speed_tolerance(self):
        """
        Retrieves the speed tolerance of the psu fan
        Returns:
            An integer, the percentage of variance from target speed which is
        considered tolerable
        """

        return NULL_VALUE
    
    def get_target_speed(self):
        """
        Retrieves the target (expected) speed of the psu fan
        Returns:
            An integer, the percentage of full fan speed, in the range 0 (off)
                 to 100 (full speed)
        """
        attr_path = "/sys/s3ip/psu/psu{}/fan_ratio".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return int(tmp_value)
        self.logger.log_error("sysfs access failed. %s" % attr_path)
        return 0
