# -*- coding: utf-8 -*-
########################################################################
# Ruijie
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Thermals' information which are available in the platform
#
########################################################################

try:
    import os
    import time
    import glob
    import sys
    from sonic_platform.util import read_sysfs, NULL_VALUE
    from sonic_platform.logger import sonic_platform_logger
    from sonic_platform_base.thermal_base import ThermalBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

class Thermal(ThermalBase):

    def __init__(self, index):
        self.logger = sonic_platform_logger()
        self.temperature_list = []
        self.index = index

    def get_name(self):
        """
        Retrieves the name of the thermal

        Returns:
            string: The name of the thermal
        """
        attr_path = "/sys/s3ip/temp_sensor/temp{}/alias".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return tmp_value
        self.logger.log_error("sysfs access failed. %s" % attr_path)
        return NULL_VALUE

    def get_presence(self):
        """
        Retrieves the presence of the thermal

        Returns:
            bool: True if thermal is present, False if not
        """
        return True

    def get_status(self):
        """
        Retrieves the operational status of the thermal

        Returns:
            A boolean value, True if thermal is operating properly,
            False if not
        """
        temp = self.get_temperature()
        high = self.get_high_critical_threshold()
        low = self.get_low_critical_threshold()
        if temp >= high or temp <= low :
            self.logger.log_error("temp%d is out of range. temp = %f, low=%f, high=%f" % (self.index, temp, low, high))
            return False

        return True

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
        return False

    def get_temperature(self):
        """
        Retrieves current temperature reading from thermal

        Returns:
            A float number of current temperature in Celsius up to nearest thousandth
            of one degree Celsius, e.g. 30.1
        """
        attr_path = "/sys/s3ip/temp_sensor/temp{}/value".format(self.index)
        ret, value = read_sysfs(attr_path)
        if ret is False:
            self.logger.log_error("sysfs access failed. %s" % attr_path)
            value = 0
        if (len(self.temperature_list) >= 1000):
            del self.temperature_list[0]
        self.temperature_list.append(float(value)/1000)
        return round(float(value)/1000, 1)

    def get_high_critical_threshold(self):
        """
        Retrieves the high critical threshold temperature of thermal

        Returns:
            A float number, the high critical threshold temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.1
        """
        attr_path = "/sys/s3ip/temp_sensor/temp{}/max".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return round(float(tmp_value)/1000, 1)
        self.logger.log_error("sysfs access failed. %s" % attr_path)

        return 0.0

    def get_low_critical_threshold(self):
        """
        Retrieves the low critical threshold temperature of thermal

        Returns:
            A float number, the low critical threshold temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.1
        """
        attr_path = "/sys/s3ip/temp_sensor/temp{}/min".format(self.index)
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return round(float(tmp_value)/1000, 1)
        self.logger.log_error("sysfs access failed. %s" % attr_path)

        return -10.0

    def get_minimum_recorded(self):
        """
        Retrieves the minimum recorded temperature of thermal

        Returns:
            A float number, the minimum recorded temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.1
        """
        if len(self.temperature_list) == 0:
            self.get_temperature()
        return round(float(min(self.temperature_list)), 1)

    def get_maximum_recorded(self):
        """
        Retrieves the maximum recorded temperature of thermal

        Returns:
            A float number, the maximum recorded temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.1
        """
        if len(self.temperature_list) == 0:
            self.get_temperature()
        return round(float(max(self.temperature_list)), 1)
    
    def get_high_threshold(self):
        """
        Retrieves the high threshold temperature of thermal

        Returns:
            A float number, the high threshold temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        return self.get_high_critical_threshold()

    def get_low_threshold(self):
        """
        Retrieves the low threshold temperature of thermal

        Returns:
            A float number, the low threshold temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        return self.get_low_critical_threshold()
