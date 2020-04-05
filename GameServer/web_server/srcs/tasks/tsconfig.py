#-*- coding:utf-8 -*-
#!/usr/bin/env python

"""
    config & global value
"""
from __future__ import absolute_import
import sys
sys.path.insert(0, '../server_common')
import redis
import yaml
import time
import logging
import json
from datetime import datetime
redisdb = None

logger = None

with open('config/config.yaml') as f:
    config = yaml.load(f)

def get_inst():
    """ 
        redis连接
        建议跟web server相同ip  dbnum不同
    """
    global redisdb
    if not redisdb:
        host = config['redis']['host']
        port = config['redis']['port']
        db = config['redis']['db']
        pwd = config['redis']['password']
        redisdb = redis.ConnectionPool(host=host, port=port, db=db, password=pwd)
    return redis.Redis(connection_pool=redisdb)


def get_pub_inst():
    """ 
        获取公用数据库连接
    """
    config_file = '../conf_release.json'
    with open(config_file) as f:
        _cnofig = json.load(f)
    host = _cnofig['redis']['host']
    port = _cnofig['redis']['port']
    db = _cnofig['redis']['database']
    pwd = "168joyvick"
    redisdb = redis.ConnectionPool(host=host, port=port, db=db, password=pwd)
    return redis.Redis(connection_pool=redisdb)



def str2timestamp(str):
    return time.mktime(datetime.strptime(str,'%Y-%m-%d').timetuple())


def str2timestamp2(str):
    """ 
        时间字符串转换为时间戳
        时间字符串格式为 %Y-%m-%d %H:%M:%S
    """
    return time.mktime(datetime.strptime(str, '%Y-%m-%d %H:%M:%S').timetuple())


def init_log(name='my', level=logging.DEBUG):
    global logger
    if logger:
        return
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # sh = logging.StreamHandler()
    fh = logging.FileHandler('logs/%s.log' % name)
    formatter = logging.Formatter('%(asctime)s -%(filename)s-L%(lineno)d-%(name)s: %(message)s')
    # sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    # logger.addHandler(sh)
    logger.addHandler(fh)
    logging.debug("current log level is : %s", logging.getLevelName(logger.getEffectiveLevel()))
    return logger


def _get():
    global logger
    if not logger:
        logger = init_log()
    return logger


def log_debug(message):
    _get().log(logging.DEBUG, message)