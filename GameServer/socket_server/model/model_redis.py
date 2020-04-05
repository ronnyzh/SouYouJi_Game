# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/15
Revision: 1.0.0
Description: Description
"""

from functools import wraps
import redis
from configs import CONFIGS

redisdb = None


def getInst(dbNum=None, redis_config=CONFIGS['redis'], decode_responses=True):
    global redisdb
    if not dbNum:
        dbNum = redis_config['dbNum']
    redisdb = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'], db=dbNum,
                                   password=redis_config['password'], decode_responses=decode_responses)
    redisData = redis.Redis(connection_pool=redisdb)
    return redisData


def wraps_getRedis(func):
    @wraps(object)
    def main(*args, **kwargs):
        redis = kwargs.get('redis')
        if not redis:
            redis = getInst()
        kwargs['redis'] = redis
        return func(*args, **kwargs)

    return main
