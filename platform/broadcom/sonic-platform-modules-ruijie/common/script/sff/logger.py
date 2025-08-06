# -*- coding: utf-8 -*-

import logging


def _init_logger():
    formatter = logging.Formatter(
        "[sfflog] %(asctime)s %(levelname)s %(filename)s[%(funcName)s][%(lineno)s]: %(message)s"
    )
    handler = logging.FileHandler("/var/log/syslog")
    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    logger.addHandler(ch)
    
    return logger


logger = _init_logger()
