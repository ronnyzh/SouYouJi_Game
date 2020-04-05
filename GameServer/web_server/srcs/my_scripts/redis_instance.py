# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Pipo
Date: $Date$
Revision: $Revision$

Description: Redis
"""
import redis
import sys
sys.path.insert(0, '..')

from configs import CONFIGS

redisConfig = CONFIGS['redis']

redisdb = None


def getInst(dbNum=1):
    global redisdb
    redisdb = redis.ConnectionPool(host=redisConfig['host'], port=redisConfig['port'], db=dbNum,
                                   password=redisConfig['password'])
    redisdb4Read = redis.ConnectionPool(host=redisConfig['host'], port=redisConfig['port'], db=dbNum,
                                        password=redisConfig['password'])  # 读库地址
    redisData = redis.Redis(connection_pool=redisdb)
    redisData.connection_read_pool = redisdb4Read
    return redisData
