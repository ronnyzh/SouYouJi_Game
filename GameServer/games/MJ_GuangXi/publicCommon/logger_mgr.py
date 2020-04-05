# coding:utf-8

import logging
import logging.handlers

t_fmt = '%(asctime)s - %(message)s'


class close_log(object):
    def info(self, *args, **kwargs):
        pass

    def error(self, *args, **kwargs):
        pass


def getLogger(label, backupCount=5, maxBytes=1024 * 8192, fmt=t_fmt):
    LOG_FILE = 'log/%s.log' % (label)
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=maxBytes, backupCount=backupCount)
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger = logging.getLogger(label)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


g_logger = getLogger('game')
e_logger = getLogger('error')
s_logger = getLogger('server')
