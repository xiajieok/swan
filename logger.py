#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/8/16 10:40
# @Author  : Medivh

import functools
import logging
import logging.handlers
import os

LOG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs', 'logger.log')
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=10)
fmt = '[%(levelname)s]: %(asctime)s - %(filename)s - %(funcName)s - %(threadName)s - %(message)s'

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger('logger')
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        logging.info('call %s():' % func.__name__)
        return func(*args, **kw)

    return wrapper

