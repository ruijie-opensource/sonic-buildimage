# -*- coding: utf-8 -*-
########################################################################
# Ruijie
#
# class for Logging used by sonic_platform
#
########################################################################


import os
import sys
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = "/var/log/ruijie/bsp/"
LOG_FILE =  LOG_DIR + "sonic_platform.log"

debuglevel = 0

def Singleton(cls):
    _instance = {}
 
    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
 
    return _singleton

@Singleton
class sonic_platform_logger(object):
    def __init__(self):
        return

    def log_error(self, s):
        return

    def log_info(self, s):
        return

    def log_debug(self, s):
        return
