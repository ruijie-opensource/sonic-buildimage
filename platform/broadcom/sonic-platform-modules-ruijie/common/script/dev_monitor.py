#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
import os
import time
import traceback
import logging
from ruijieconfig import *
from platform_util import *
from logging.handlers import RotatingFileHandler

DEVMONITOR_DEBUG_FILE = "/etc/.devmonitor_debug_flag"
LOG_DIR = "/var/log/ruijie/bsp/"
LOG_FILE = LOG_DIR + "/dev_monitor.log"

STATUS_OK = 1
STATUS_NOT_OK = 0

CONDITION_CHECK_OK = 1
CONDITION_CHECK_NOT_OK = 0
CONDITION_CHECK_ALL = 0xff

FLAG_SET = 1
FLAG_CLEAR = 0

FAIL_RETRY_TIMES = 3

debuglevel = 0


def dev_monitor_log_init():
    global dev_logger
    if not os.path.exists(LOG_DIR):
        os.system("mkdir -p %s" % LOG_DIR)
        os.system("sync")
    dev_logger = logging.getLogger(__name__)
    dev_logger.setLevel(logging.DEBUG)
    dev_handler = RotatingFileHandler(filename = LOG_FILE, maxBytes = 1*1024*1024, backupCount = 1)
    dev_handler.setFormatter(logging.Formatter('%(asctime)s, %(filename)s, %(levelname)s, %(message)s'))
    dev_handler.setLevel(logging.DEBUG)
    dev_logger.addHandler(dev_handler)


def dev_monitor_debug_init():
    global debuglevel
    if os.path.exists(DEVMONITOR_DEBUG_FILE):
        debuglevel = 1
    else:
        debuglevel = 0


def deverror(s):
    #s = s.decode('utf-8').encode('gb2312')
    dev_logger.error("LINE:%s, %s" % (sys._getframe(1).f_lineno, s))


def devinfo(s):
    #s = s.decode('utf-8').encode('gb2312')
    dev_logger.info("LINE:%s, %s" % (sys._getframe(1).f_lineno, s))


def devdebuglog(s):
    #s = s.decode('utf-8').encode('gb2312')
    if debuglevel == 1:
        dev_logger.debug("LINE:%s, %s" % (sys._getframe(1).f_lineno, s))


class Monitoring(object):
    def __init__(self, config):
        self.each_dev_config = config

    def do_action(self):
        self.id = self.each_dev_config.get('id', None)
        self.stop_monitor_condition = self.each_dev_config.get('stop_monitor_condition', [])
        self.disposable_action = self.each_dev_config.get('disposable_action', [])
        self.pre_action_check = self.each_dev_config.get('pre_action_check', [])
        self.pre_action = self.each_dev_config.get('pre_action', [])
        self.action_list = self.each_dev_config.get('action', [])
        self.func_call = self.each_dev_config.get('func_call', [])
        self.support_type = self.each_dev_config.get('support_type', None)
        self.get_card_type = self.each_dev_config.get("get_card_type", None)

        try:
            if len(self.stop_monitor_condition) == 0:
                # 无"停止监控条件"项，则进行后续监控动作
                devdebuglog("%s doesn't have stop_monitor_condition" % (self.id))
            else:
                # 有"停止监控条件"项
                tmp = 0
                for stop_config in self.stop_monitor_condition:
                    name = stop_config.get("name", None)
                    ret, log = check_value(stop_config)
                    if ret is not True:
                        deverror("stop %s monitor point is not ok, doing monitor." % (name))
                        tmp = -1
                        break
                    if log == CHECK_VALUE_OK:
                        devdebuglog("stop %s monitor point check ok" % (name))
                    else:
                        devdebuglog("stop %s monitor point check not ok" % (name))
                        tmp = -1
                        break
                # 全部项都check ok，则直接退出不动作
                if tmp == 0:
                    devdebuglog("stop %s all monitor condition is ok, no action" % self.id)
                    return True

            if self.get_card_type is not None and self.support_type is not None:
                # 板卡支持校验，支持的板卡才进行后续动作
                ret, log = get_value(self.get_card_type)
                if ret is False:
                    deverror("self.id:%s card_type get failed. log: %s" % (self.id, log))
                    return False
                card_type = log

                if isinstance(self.support_type, int):
                    if self.support_type != card_type:
                        devdebuglog("self.id:%s does not support board card 0x%x" % (self.id, card_type))
                        return True
                elif isinstance(self.support_type, list):
                    if card_type not in self.support_type:
                        msg = "card_type:%s not match support_type_list:%s" % (card_type, self.support_type)
                        devdebuglog(msg)
                        return True
                else:
                    return False, ("self.support_type:%s is not int or list type" % (self.support_type))

            # 进行pre_check动作
            tmp = 0
            for pre_action_check in self.pre_action_check:
                name = pre_action_check.get("name", None)
                ret, log = check_value(pre_action_check)
                if ret is not True:
                    deverror("%s pre check not ok." % (name))
                    tmp = -1
                else:
                    if log == CHECK_VALUE_OK:
                        devdebuglog("%s pre check ok " % (name))
                    else:
                        devdebuglog("%s pre check not ok " % (name))
                        tmp = -1

            # pre_check通过，则进行相应动作
            if tmp == 0:
                for pre_action in self.pre_action:
                    name = pre_action.get("name", None)
                    ret, log = set_value(pre_action)
                    if ret is False:
                        deverror("action %s excute failed. ret:%s, log:%s"
                                 % (name, ret, log))
                    else:
                        devinfo("pre_action %s doing success" % (name))

            tmp = 0
            # disposable_action 是某些动作只需执行一次
            for disposable_action in self.disposable_action:
                name = disposable_action.get("name", None)
                if disposable_action.get("action_flag", 0) == 0:
                    devdebuglog("disposable %s will do disposable_action" % (name))
                    ret, log = set_value(disposable_action)
                    if ret is False:
                        deverror("disposable %s excute failed. ret:%s, log:%s."
                                 % (name, ret, log))
                        tmp = -1
                    else:
                        # action finish flag set 1
                        devinfo("disposable %s doing success" % (name))
                        disposable_action["action_flag"] = 1

            # 进行action动作
            for action_config in self.action_list:
                name = action_config.get("name", None)
                ret, log = set_value(action_config)
                if ret is False:
                    deverror("action %s excute failed. ret:%s, log:%s"
                             % (name, ret, log))
                    tmp = -1
                else:
                    devinfo("action %s doing success" % (name))

            # 调用函数
            for func_call in self.func_call:
                name = func_call.get("name", None)
                func = func_call.get("func")
                param = func_call.get("param")
                ret = eval(func)(eval(param))
                if ret is False:
                    deverror("func_call %s excute failed. func:%s param:%s" % (name, func, param))
                    tmp = -1
                else:
                    devinfo("func_call %s doing %s success" % (name, func_call))

            # 各停止监控项与预期判断
            for stop_config in self.stop_monitor_condition:
                name = stop_config.get("name", None)
                ret, log = check_value(stop_config)
                if ret is not True:
                    deverror("stop %s result check failed. ret:%s, log:%s"
                             % (name, ret, log))
                    tmp = -1
                else:
                    if log == CHECK_VALUE_OK:
                        devdebuglog("stop %s check ok " % (name))
                    else:
                        devdebuglog("stop %s check not ok " % (name))
                        tmp = -1

            if tmp == 0:
                devinfo("do action %s all device mount success" % self.id)
                return True
            return False
        except Exception as e:
            deverror("do action exception, log:%s" % str(e))
            return False


class Intelligent_Monitor(Monitoring):
    def __init__(self):
        self.dev_config_list = []
        self.monitor_config = DEV_MONITOR_PARAM.copy()
        self.init_delay = self.monitor_config.get('init_delay', 0)
        self.ready_timeout = self.monitor_config.get('ready_timeout', 0)
        self.timeout_action_list = self.monitor_config.get('timeout_action', [])
        self.dev_ready_check_list = self.monitor_config.get('dev_ready_check', [])
        self.status_monitor_interval = self.monitor_config.get("status_monitor_interval", 0)
        self.dev_monitor_interval = self.monitor_config.get("dev_monitor_interval", 5)
        self.device_list = self.monitor_config.get("device", [])

    def recovery_option(self, config):
        name = config.get('name', None)
        subdevice_list = config.get('subdevice', [])
        recovery_fail_cnt = config.get('recovery_fail_cnt', 0)

        try:
            if len(subdevice_list) == 0:
                devdebuglog("recovery option is not configured, do nothing")
                config['recovery_flag'] = FLAG_CLEAR
                return

            # 赋初值
            if recovery_fail_cnt == 0:
                config['recovery_fail_cnt'] = 0

            # 对于失败次数上限进行重试，失败超过重试次数不再重试
            if recovery_fail_cnt >= FAIL_RETRY_TIMES:
                config['recovery_fail_cnt'] = 0
                config['recovery_flag'] = FLAG_CLEAR
                deverror("%s recovery fail cnt:%s, not retry" % (name, recovery_fail_cnt))
                return

            # 进行recovery动作，将subdevice_list中的每个动作定义成一个类对象
            self.dev_config_list = []
            for sub_config in subdevice_list:
                config_instance = Monitoring(sub_config)
                self.dev_config_list.append(config_instance)

            # 对dev_config_list中的所有项进行动作，全部成功则认为成功
            tmp = 0
            for dev in self.dev_config_list:
                ret = dev.do_action()
                if ret is False:
                    deverror("%s dev do action failed" % (name))
                    tmp = -1
            if tmp == 0:
                # 全部动作成功则清空recovery_flag和recovery_fail_cnt
                config['recovery_flag'] = FLAG_CLEAR
                config['recovery_fail_cnt'] = 0
                devinfo("recovery option %s all success" % name)
            else:
                config['recovery_fail_cnt'] += 1

        except Exception as e:
            deverror("recovery option exception, log:%s" % str(e))
        return

    def leave_option(self, config):
        name = config.get('name', None)
        leave_option_list = config.get("leave_option", [])
        leave_fail_cnt = config.get('leave_fail_cnt', 0)

        try:
            if len(leave_option_list) == 0:
                devdebuglog("leave option is not configured, do nothing")
                config['leave_flag'] = FLAG_CLEAR
                return

            # 赋初值
            if leave_fail_cnt == 0:
                config['leave_fail_cnt'] = 0

            # 对于失败次数上限进行重试，失败超过重试次数不再重试
            if leave_fail_cnt >= FAIL_RETRY_TIMES:
                config['leave_fail_cnt'] = 0
                config['leave_flag'] = FLAG_CLEAR
                deverror("%s leave fail cnt:%s, not retry" % (name, leave_fail_cnt))
                return

            tmp = 0
            for leave_option_config in leave_option_list:
                name = leave_option_config.get("name", None)
                ret, log = set_value(leave_option_config)
                if ret is False:
                    tmp = -1
                    deverror("leave option %s set failed. log:%s" % (name, log))
                else:
                    devinfo("leave option %s doing success." % (name))

            if tmp == 0:
                # 全部动作成功则清空leave_flag和leave_fail_cnt
                config['leave_flag'] = FLAG_CLEAR
                config['leave_fail_cnt'] = 0
                devdebuglog("leave option all action success")
            else:
                config['leave_fail_cnt'] += 1

        except Exception as e:
            log = "leave option exception, log:%s" % str(e)
            deverror(log)
        return

    def do_monitor(self):
        for config in self.device_list:
            try:
                leave_flag = config.get('leave_flag', FLAG_CLEAR)
                recovery_flag = config.get('recovery_flag', FLAG_CLEAR)

                # FLAG_SET置上则进行leave动作
                if leave_flag == FLAG_SET:
                    self.leave_option(config)

                # FLAG_SET置上则进行recovery动作
                if recovery_flag == FLAG_SET:
                    self.recovery_option(config)

            except Exception as e:
                deverror("do monitor exception, log:%s" % str(e))
        return

    def update_monitor_list_status(self, each_monitor_list, each_dev_last_status):
        try:
            # 对于未定义each_monitor_list的监控项，直接返回失败
            if len(each_monitor_list) == 0:
                deverror("lack of each_dev_monitor_list")
                return False, "lack of each_monitor_list"

            # each_monitor_point_config为每个监控列表中的每个监控项
            # 某一项监控失败直接return false
            for each_monitor_point_config in each_monitor_list:
                name = each_monitor_point_config.get("name", None)
                # monitor_condition表示特定情况下才进行监控,
                # 1表示上次状态为OK时才进行check_value，
                # 0表示上次状态为NOT OK时才进行check_value，
                # 其余值表示任何时刻都进行check_value
                monitor_condition = each_monitor_point_config.get("monitor_condition", CONDITION_CHECK_ALL)
                if monitor_condition == CONDITION_CHECK_OK and each_dev_last_status != STATUS_OK:
                    devdebuglog("last status isn't ok, %s skip check" % (name))
                    continue

                if monitor_condition == CONDITION_CHECK_NOT_OK and each_dev_last_status != STATUS_NOT_OK:
                    devdebuglog("last status isn't not ok, %s skip check" % (name))
                    continue

                ret, val = check_value(each_monitor_point_config)
                if ret is not True:
                    log = "monitor config %s check failed. log:%s" % (name, val)
                    deverror(log)
                    return False, log
                elif val != CHECK_VALUE_OK:
                    devdebuglog("monitor config %s check not ok" % (name))
                    return True, CHECK_VALUE_NOT_OK
                else:
                    devdebuglog("monitor config %s check ok" % (name))

            return True, CHECK_VALUE_OK
        except Exception as e:
            log = "update monitor list status exception, log:%s" % str(e)
            deverror(log)
            return False, log

    def update_each_dev_status(self, each_dev_monitor_list, each_dev_last_status):
        try:
            # 对于未定义each_dev_monitor_list的设备，直接进行后续的do_monitor动作逻辑
            if len(each_dev_monitor_list) == 0:
                devdebuglog("has no each_dev_monitor_list")
                return True, CHECK_VALUE_OK

            # each_dev_monitor_list中其中某个list是check ok，就认为此设备check ok
            tmp = 0
            for each_monitor_list in each_dev_monitor_list:
                ret, val = self.update_monitor_list_status(each_monitor_list, each_dev_last_status)
                if ret is True and val == CHECK_VALUE_OK:
                    return ret, val
                if ret is False:
                    tmp = -1
                    continue

            # check not ok
            # 返回值不存在check failed的情况，最终返回True, check not ok，否则返回False
            if tmp == 0:
                return True, CHECK_VALUE_NOT_OK
            return False, "each_monitor_list has mistake"

        except Exception as e:
            log = "update each dev status exception, log:%s" % str(e)
            deverror(log)
            return False, log

    def update_dev_status(self):
        try:
            # 对需要监控的device_list中的每种设备进行遍历
            for each_dev_config in self.device_list:
                name = each_dev_config.get('name', None)
                each_dev_monitor_list = each_dev_config.get("monitor_point", [])
                # 每个dev的上次状态
                each_dev_last_status = each_dev_config.get("last_status", STATUS_NOT_OK)

                # 遍历各dev的监控列表，ret是True表示dev的此次状态是ok，反之为not ok
                # recovery表示恢复(not ok -> ok），如子卡插入，如cpld寄存器恢复为就绪值，
                # leave表示recovery的相反含义(ok -> not ok)
                ret, val = self.update_each_dev_status(each_dev_monitor_list, each_dev_last_status)
                if ret is True and val == CHECK_VALUE_OK:
                    # 本次状态是ok，更新状态
                    each_dev_config['last_status'] = STATUS_OK
                    # 本次状态是ok，不允许leave动作
                    each_dev_config['leave_flag'] = FLAG_CLEAR
                    if each_dev_last_status == STATUS_NOT_OK:
                        # not ok -> ok，置上recovery标志
                        devinfo("dev %s status from not ok change to ok." % (name))
                        each_dev_config['recovery_flag'] = FLAG_SET
                else:
                    # check失败和check not ok走相同处理, check失败多一条error打印
                    if ret is not True:
                        deverror("dev %s check val failed, log:%s" % (name, val))
                    # 本次状态是not ok，更新状态
                    each_dev_config['last_status'] = STATUS_NOT_OK
                    # 本次状态是not ok，不允许recovery动作
                    each_dev_config['recovery_flag'] = FLAG_CLEAR
                    if each_dev_last_status == STATUS_OK:
                        # ok -> not ok，置上leave标志
                        devinfo("dev %s status from ok change to not ok." % (name))
                        each_dev_config['leave_flag'] = FLAG_SET
        except Exception as e:
            deverror("update dev status exception, log:%s" % str(e))
            return

    def dev_ready_check(self, check_list):
        try:
            # 未定义要校验的项，直接返回true
            if len(check_list) == 0:
                log = 'dev ready check list is None, not checking'
                devdebuglog(log)
                return True, log

            # 对于check_list中的each_check_list进行校验，全部成功才最终返回true
            for each_check_list in check_list:
                # 每个校验项要求进行配置
                if len(each_check_list) == 0:
                    log = 'dev ready check each check list is None, config error'
                    deverror(log)
                    return False, log

                # 对于each_check_list中的each_check_config进行校验，全部成功才最终返回true
                tmp = 0
                for each_check_config in each_check_list:
                    name = each_check_config.get('name', None)
                    ret, val = check_value(each_check_config)
                    if ret is False:
                        deverror("dev ready check %s check failed." % (name))
                        deverror("error log: %s" % val)
                        tmp = -1
                        break
                    if val != CHECK_VALUE_OK:
                        log = 'dev ready check %s check not ok' % name
                        devdebuglog(log)
                        tmp = -1
                        break
                    else:
                        devdebuglog('dev ready check %s check ok' % name)
                if tmp == 0:
                    log = 'dev ready check all check ok. \n list:%s' % each_check_list
                    devdebuglog(log)
                    return True, log
            log = 'dev ready check not all check ok. \n list:%s' % check_list
            devdebuglog(log)
            return False, log
        except Exception as e:
            log = "dev ready check exception, log:%s" % str(e)
            deverror(log)
            return False, log

    def wait_dev_ready(self):
        start_time = time.time()
        while True:
            try:
                dev_monitor_debug_init()
                if self.ready_timeout > 0 and time.time() - start_time >= self.ready_timeout:
                    #等待设备状态就绪超时，进行相应的timeout action
                    deverror("wait dev ready check is timeout.")
                    for timeout_action_config in self.timeout_action_list:
                        name = timeout_action_config.get('name', None)
                        ret, log = set_value(timeout_action_config)
                        if ret is False:
                            deverror("wait dev ready %s timeout action set failed. log:%s" %(name, log))
                        else:
                            devinfo("wait dev ready %s timeout action set success." % name)
                    return

                # 进行设备状态校验
                ret, log = self.dev_ready_check(self.dev_ready_check_list)
                if ret is False:
                    devdebuglog('dev ready check not ok, log:%s' % log)
                    time.sleep(self.dev_monitor_interval)
                    continue

                devdebuglog('wait dev ready all dev ready')
                return
            except Exception as e:
                traceback.print_exc()
                deverror("wait dev ready exception, log:%s" % str(e))
                exit(-1)

    def run(self):
        dev_monitor_log_init()
        dev_monitor_debug_init()
        # init_delay用于那些拉起进程时需要延迟一段时间再进入检测逻辑的场景
        if self.init_delay > 0:
            devdebuglog("run init_delay is %d, doing delay" % self.init_delay)
            time.sleep(self.init_delay)

        # wait_dev_ready用于那些需检测到某些状态就绪后再进入检测逻辑的场景
        self.wait_dev_ready()

        # 设置起始时间
        start_time = time.time()
        while True:
            try:
                dev_monitor_debug_init()
                # dev_monitor_interval表示动作周期，status_monitor_interval表示快速检测状态，
                # 例如用于子卡热拔插功能，可能最终卡插入5s才进行相应动作，但是每0.5s检测一次是否有卡插入，
                # 防止拔插周期在5s内场景出现时异常
                if self.status_monitor_interval > 0 and self.status_monitor_interval < self.dev_monitor_interval:
                    if time.time() - start_time >= self.dev_monitor_interval:
                        # 到达dev_monitor_interval动作周期，进入动作逻辑
                        self.update_dev_status()
                        self.do_monitor()
                        start_time = time.time()
                    else:
                        # 每status_monitor_interval周期更新一次设备状态
                        self.update_dev_status()
                        time.sleep(self.status_monitor_interval)
                else:
                    # 未定义快速检测机制，则每dev_monitor_interval周期，进行一次状态检测和动作
                    self.update_dev_status()
                    self.do_monitor()
                    time.sleep(self.dev_monitor_interval)
            except Exception as e:
                traceback.print_exc()
                deverror("run exception, log:%s" % str(e))
                exit(-1)


if __name__ == '__main__':
    dev_monitor = Intelligent_Monitor()
    dev_monitor.run()
