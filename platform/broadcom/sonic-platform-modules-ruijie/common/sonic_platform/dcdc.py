# -*- coding: utf-8 -*-
########################################################################
# Ruijie
#
# Module contains an implementation of SONiC Platform Base API and
# provides the DCDC' information which are available in the platform
#
########################################################################
try:
    from sonic_platform.util import read_sysfs, exec_os_cmd, NULL_VALUE
    from sonic_platform.logger import sonic_platform_logger
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")
try:
    from sonic_platform_base.dcdc_base import DcdcBase
except ImportError as e:
    class DcdcBase:
        pass

class Dcdc(DcdcBase):

    def __init__(self, dcdc_id):
        self.logger = sonic_platform_logger()
        self.dcdc_id = str(dcdc_id)
        self.dcdc_dict = {}

    def get_name(self):
        """
        Retrieves the name of the sensor

        Returns:
            string: The name of the sensor
        """
        return self.dcdc_id

    def ipmi_get_sensor(self):
        """
        Retrieves value reading from sensor
        Returns:
            bool: The status of the command
        """
        command = "ipmitool sensor get {}".format(self.dcdc_id)
        status, output = exec_os_cmd(command)
        if status:
            self.logger.log_error("%s failed." % command)
            return False
        dcdc_info = output.splitlines()
        """
            the result of ipmi command. eg:
                Locating sensor record...
                Sensor ID              : VDD_5V (0x53)
                 Entity ID             : 0.0
                 Sensor Type (Threshold)  : Voltage
                 Sensor Reading        : 5.100 (+/- 0) Volts
                 Status                : ok
                 Lower Non-Recoverable : na
                 Lower Critical        : 4.600
                 Lower Non-Critical    : 4.900
                 Upper Non-Critical    : 5.400
                 Upper Critical        : 5.700
                 Upper Non-Recoverable : na
                 Positive Hysteresis   : Unspecified
                 Negative Hysteresis   : Unspecified
        """
        for index in range(1, len(dcdc_info)):
            item = dcdc_info[index]
            
            if len(str(item).split(":")) >= 2: # need key:vaule pair
                item_key =  str(item).split(":")[0].strip()
                if len(item_key) > 0:
                    self.dcdc_dict[item_key] = str(item).split(":")[1].strip()

        return True

    def get_status(self):
        """
        Retrieves the status of the sensor
        Returns:
            bool: The status of the sensor
        """
        dcdc_info = self.ipmi_get_sensor()
        
        if self.dcdc_dict.get("Status", "nr") != "ok":
            self.logger.log_error("dcdc status false. dcdc info = %s " % str(self.dcdc_dict))
            return False
        return True