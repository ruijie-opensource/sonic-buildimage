# -*- coding: utf-8 -*-
########################################################################
# Ruijie
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Fans' information which are available in the platform.
#
########################################################################

try:
    import time
    import sys
    from sonic_platform.util import read_sysfs, write_sysfs, NULL_VALUE
    from sonic_platform.logger import sonic_platform_logger
    from sonic_platform_base.fan_base import FanBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

class Fan(FanBase):
    """Ruijie Platform-specific Fan class"""

    def __init__(self, index, psu_fan=False, psu_index=0, psu_obj=None):
        self.logger = sonic_platform_logger()
        self.index = index
        self.psu_index = psu_index
        self.is_psu_fan = psu_fan

        if not self.is_psu_fan:
            self.name = "FAN" + str(index)
        else:
            self.name = "PSU" + str(psu_index)
            self.psu = psu_obj

    def get_name(self):
        """
        Retrieves the fan name
        Returns:
            string: The name of the device
        """
        if not self.is_psu_fan:
            return "Fan {}".format(self.index)
        else:
            return "Psu {} Fan {}".format(self.psu_index, self.index)

    def get_model(self):
        """
        Retrieves the part number of the FAN
        Returns:
            string: Part number of FAN
        """
        if not self.is_psu_fan:
            attr_path = "/sys/s3ip/fan/fan{}/model_name".format(self.index)
            ret, tmp_value = read_sysfs(attr_path)
            if ret is True:
                return tmp_value
            self.logger.log_error("sysfs access failed. %s" % attr_path)
            return NULL_VALUE
        else:
            return NULL_VALUE

    def get_serial(self):
        """
        Retrieves the serial number of the FAN
        Returns:
            string: Serial number of FAN
        """
        if not self.is_psu_fan:
            attr_path = "/sys/s3ip/fan/fan{}/serial_number".format(self.index)
            ret, tmp_value = read_sysfs(attr_path)
            if ret is True:
                return tmp_value
            self.logger.log_error("sysfs access failed. %s" % attr_path)
            return NULL_VALUE
        else:
            return NULL_VALUE

    def get_presence(self):
        """
        Retrieves the presence of the FAN
        Returns:
            bool: True if fan is present, False if not
        """
        if not self.is_psu_fan:
            attr_path = "/sys/s3ip/fan/fan{}/status".format(self.index)
        elif self.psu:
            return self.psu.get_presence()
        else:
            return False
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            if int(tmp_value) == 0:
                return False
            else:
                return True
        self.logger.log_error("sysfs access failed. %s" % attr_path)
        return False

    def get_status_one(self):
        """
        Retrieves the operational status of the FAN
        Returns:
            bool: True if FAN is operating properly, False if not
        """
        if not self.is_psu_fan:
            speed_rpm = self.get_speed_rpm()
            tolerance = self.get_speed_tolerance()
            target_rpm = self.get_target_speed_rpm()
            if (abs(speed_rpm - target_rpm) / target_rpm > tolerance):
                return False
            return True
        else:
            speed_rpm = self.psu.get_speed_rpm()
            speed_rpm_max = self.psu.get_speed_rpm_max()
            speed_rpm_min = self.psu.get_speed_rpm_min()
            if speed_rpm == 0:
                return False
            elif speed_rpm < speed_rpm_min or speed_rpm > speed_rpm_max:
                return False
            return True

    def get_status(self):
        """
        Retrieves the operational status of the FAN
        Returns:
            bool: True if FAN is operating properly, False if not
        """
        if not self.get_presence():
            return False

        max_try = 7
        retry_delay = 1  # max total delay = retry times * retry_delay

        while max_try > 0:
            status = True
            status = self.get_status_one()
            if not status:
                max_try -= 1
                if max_try <= 0:
                    self.logger.log_error("fan%d speed is out of range of tolerance. max_try = %d" % (self.index, max_try))
                    break
                time.sleep(retry_delay)
            else:
                break

        return status

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

    def get_direction(self):
        """
        Retrieves the fan airflow direction
        Returns:
            A string, either FAN_DIRECTION_INTAKE or FAN_DIRECTION_EXHAUST
            depending on fan direction

        Notes:
            - Forward/Exhaust : Air flows from Fan side to Port side.
            - Reverse/Intake  : Air flows from Port side to Fan side.
        """
        if not self.is_psu_fan:
            attr_path = "/sys/s3ip/fan/fan{}/direction".format(self.index)
            ret, tmp_value = read_sysfs(attr_path)
            if ret is True:
                #0：F2B，前向风道
                #1：B2F，后向风道
                if int(tmp_value) == 1:
                    return self.FAN_DIRECTION_EXHAUST
                else:
                    return self.FAN_DIRECTION_INTAKE
            self.logger.log_error("sysfs access failed. %s" % attr_path)
            return NULL_VALUE
        elif self.psu:
            tmp_value = self.psu.get_direction()
            if tmp_value == 1:
                return self.FAN_DIRECTION_EXHAUST
            elif tmp_value == NULL_VALUE:
                return NULL_VALUE
            else:
                return self.FAN_DIRECTION_INTAKE
        else:
            return NULL_VALUE

    def get_motor_num(self):
        """
        Retrieves the motor num of fan
        Returns:
            An integer
        """
        if not self.is_psu_fan:
            attr_path = "/sys/s3ip/fan/fan{}/motor_number".format(self.index)
            ret, tmp_value = read_sysfs(attr_path)
            if ret is True:
                return int(tmp_value)
            self.logger.log_error("sysfs access failed. %s" % attr_path)
            return 0
        else:
            return 1

    def get_speed_rpm(self, motor=1):
        """
        Retrieves the speed of motor
        Returns:
            An integer
        """
        if not self.is_psu_fan:
            attr_path = "/sys/s3ip/fan/fan{}/motor{}/speed".format(self.index, motor)
        elif self.psu:
            return self.psu.get_speed_rpm()
        else:
            return False
        ret, tmp_value = read_sysfs(attr_path)
        if ret is True:
            return int(tmp_value)
        self.logger.log_error("sysfs access failed. %s" % attr_path)
        return 0
    
    def get_speed_rpm_max(self, motor=1):
        """
        Retrieves the max speed of motor
        Returns:
            An integer
        """
        if not self.is_psu_fan:
            attr_path = "/sys/s3ip/fan/fan{}/motor{}/speed_max".format(self.index, motor)
            ret, tmp_value = read_sysfs(attr_path)
            if ret is True:
                return int(tmp_value)
            self.logger.log_error("sysfs access failed. %s" % attr_path)
            return 0
        elif self.psu:
            return self.psu.get_speed_rpm_max()
        else:
            return False

    def get_speed(self, motor=1):
        """
        Retrieves the speed of fan as a percentage of full speed

        Returns:
            An integer, the percentage of full fan speed, in the range 0 (off)
                 to 100 (full speed)
        """
        try:
            if not self.is_psu_fan:
                value = self.get_speed_rpm(motor)
                max = self.get_speed_rpm_max(motor)
            elif self.psu:
                value = self.psu.get_speed_rpm()
                max = self.psu.get_speed_rpm_max()
            else:
                return 0
            if max == 0:
                return 0
            pwm = value * 100 / max
            if pwm > 100:
                pwm = 100
            elif pwm < 0:
                pwm = 0
        except BaseException:
            return 0
        return int(pwm)

    def get_speed_tolerance(self, motor=1):
        """
        Retrieves the speed tolerance of the fan
        Returns:
            An integer, the percentage of variance from target speed which is
        considered tolerable
        """
        return 30

    def set_speed(self, speed):
        """
        Set fan speed to expected value
        Args:
            speed: An integer, the percentage of full fan speed to set fan to,
                   in the range 0 (off) to 100 (full speed)
        Returns:
            bool: True if set success, False if fail.
        """
        if not self.is_psu_fan:
            attr_path = "/sys/s3ip/fan/fan{}/ratio".format(self.index)
            ret, msg = write_sysfs(attr_path, str(speed))
            if ret is True:
                return True
            self.logger.log_error("sysfs access failed. %s" % attr_path)
            return False
        else:
            raise NotImplementedError

    def color_map(self):
        s3ip_fanled_color_map = {
            0: self.STATUS_LED_COLOR_OFF, #dark
            1: self.STATUS_LED_COLOR_GREEN, #green
            2: self.STATUS_LED_COLOR_AMBER, #yellow
            3: self.STATUS_LED_COLOR_RED, #red
            #4: #blue
            5: self.STATUS_LED_COLOR_GREEN,#green_flash 
            6: self.STATUS_LED_COLOR_AMBER,#yellow_flash
            7: self.STATUS_LED_COLOR_RED,#red_flash
            #8: #blue_flash
        }
        
        return s3ip_fanled_color_map

    def get_status_led(self):
        """
        Gets the state of the Fan status LED

        Returns:
            A string, one of the predefined STATUS_LED_COLOR_* strings.
        """
        if not self.is_psu_fan:
            s3ip_fanled_color_map = self.color_map()

            attr_path = "/sys/s3ip/fan/fan{}/led_status".format(self.index)
            ret, tmp_value = read_sysfs(attr_path)
            if ret is True:
                return s3ip_fanled_color_map[int(tmp_value)]
            self.logger.log_error("sysfs access failed. %s" % attr_path)
            return NULL_VALUE
        else:
            return NULL_VALUE
        
    def set_status_led(self, color):
        """
        Sets the state of the fan module status LED

        Args:
            color: A string representing the color with which to set the
                   fan module status LED

        Returns:
            bool: True if status LED state is set successfully, False if not
        """
        s3ip_sysled_color_map = self.color_map()
        s3ip_color = [key for key, value in s3ip_sysled_color_map.items() if value == color]
        
        if len(s3ip_color) != 0:
            attr_path = "/sys/s3ip/fan/fan{}/led_status".format(self.index)
            s3ip_color.sort()
            ret, tmp_value = write_sysfs(attr_path, str(s3ip_color[0]))
            if ret is True:
                return True
            self.logger.log_error("sysfs access failed. %s。 value set: %d" % (attr_path, s3ip_color[0]))
            return False

        self.logger.log_error("color %s is not supported." % color)
        return False


    def get_target_speed(self):
        """
        Retrieves the target (expected) speed of the fan
        Returns:
            An integer, the percentage of full fan speed, in the range 0 (off)
                 to 100 (full speed)
        """
        if not self.is_psu_fan:
            attr_path = "/sys/s3ip/fan/fan{}/ratio".format(self.index)
            ret, tmp_value = read_sysfs(attr_path)
            if ret is True:
                return int(tmp_value)
            self.logger.log_error("sysfs access failed. %s" % attr_path)
            return 0
        elif self.psu:
            return self.psu.get_target_speed()
        else:
            raise NotImplementedError

    def get_target_speed_rpm(self, motor=1):
        """
        Retrieves the target (expected) speed of the fan
        Returns:
            An integer, the rpm value of motor
        """
        if not self.is_psu_fan:
            attr_path = "/sys/s3ip/fan/fan{}/motor{}/speed_target".format(self.index, motor)
            ret, tmp_value = read_sysfs(attr_path)
            if ret is True:
                return int(tmp_value)
            self.logger.log_error("sysfs access failed. %s" % attr_path)
            return 0
        else:
            return NULL_VALUE

    def get_revision(self):
        """
        Retrieves the hardware revision of the device

        Returns:
            string: Revision value of device
        """
        if not self.is_psu_fan:
            attr_path = "/sys/s3ip/fan/fan{}/hardware_version".format(self.index)
            ret, tmp_value = read_sysfs(attr_path)
            if ret is True:
                return tmp_value
            self.logger.log_error("sysfs access failed. %s" % attr_path)
            return NULL_VALUE
        else:
            return NULL_VALUE

