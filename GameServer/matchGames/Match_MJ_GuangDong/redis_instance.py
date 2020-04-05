# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Pipo
Date: $Date$
Revision: $Revision$

Description: Redis
"""
import redis
from configs import CONFIGS

redisdb = None


def getInst(dbNum=CONFIGS['redis']['db']):
    global redisdb
    redisdb = redis.ConnectionPool(
        host=CONFIGS['redis']['host'],
        port=CONFIGS['redis']['port'],
        db=dbNum,
        password=CONFIGS['redis']['password']
    )
    redisData = redis.Redis(connection_pool=redisdb)
    return redisData
