# -*- coding: utf-8 -*-
########################################################################
# Ruijie
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Components' (e.g., BIOS, CPLD, FPGA, etc.) available in
# the platform
#
########################################################################

try:
    import time
    import sys
    from sonic_platform.util import read_sysfs, exec_os_cmd, NULL_VALUE
    from sonic_platform_base.component_base import ComponentBase
    from sonic_platform.logger import sonic_platform_logger
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

class Component(ComponentBase):
    """Ruijie Platform-specific Component class"""

    def __init__(self, comp_id, index=1):
        ComponentBase.__init__(self)
        self.logger = sonic_platform_logger()
        self.index = index
        self.comp_id = comp_id

    def get_name(self):
        """
        Retrieves the name of the component

        Returns:
            A string containing the name of the component
        """

        if self.comp_id == "fpga" or self.comp_id == "cpld":
            attr_path = "/sys/s3ip/{}/{}{}/alias".format(self.comp_id, self.comp_id, self.index)
            ret, tmp_value = read_sysfs(attr_path)
            if ret is True:
                return tmp_value
            self.logger.log_error("sysfs access failed. %s" % attr_path)
            return NULL_VALUE
        else:
            # bios, bmc
            return str(self.comp_id).upper()

    def get_description(self):
        """
        Retrieves the description of the component

        Returns:
            A string containing the description of the component
        """
        if self.comp_id == "fpga" or self.comp_id == "cpld":
            attr_path = "/sys/s3ip/{}/{}{}/type".format(self.comp_id, self.comp_id, self.index)
            ret, tmp_value = read_sysfs(attr_path)
            if ret is True:
                return tmp_value
            self.logger.log_error("sysfs access failed. %s" % attr_path)
            return NULL_VALUE
        else:
            # bios, bmc
            return str(self.comp_id).upper()

    def get_firmware_version(self):
        """
        Retrieves the firmware version of the component

        Returns:
            A string containing the firmware version of the component
        """

        if self.comp_id == "fpga" or self.comp_id == "cpld":
            attr_path = "/sys/s3ip/{}/{}{}/firmware_version".format(self.comp_id, self.comp_id, self.index)
            ret, tmp_value = read_sysfs(attr_path)
            if ret is True:
                return tmp_value
            self.logger.log_error("sysfs access failed. %s" % attr_path)
            return NULL_VALUE
        elif self.comp_id == "bios":
            command = "dmidecode -t 0 | grep Version | awk -F' ' '{print $2}'",
            status, output = exec_os_cmd(command)
            if status:
                self.logger.log_error("%s failed." % command)
                return NULL_VALUE
            output = output.strip('\n')
            return output
        elif self.comp_id == "bmc":
            command = "ipmitool mc info |grep \"Firmware Revision\" | awk -F' ' '{print $4}'",
            status, output = exec_os_cmd(command)
            if status:
                self.logger.log_error("%s failed." % command)
                return NULL_VALUE
            output = output.strip('\n')
            return output
        else:
            return NULL_VALUE
