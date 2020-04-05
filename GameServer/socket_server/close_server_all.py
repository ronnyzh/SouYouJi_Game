# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/11/15
Revision: 1.0.0
Description: Description
"""
from model.model_redis import getInst
from define.define_redis_key import *

if __name__ == '__main__':
    redis = getInst()
    pipe = redis.pipeline()
    hallServerSet = redis.smembers(Key_Server_Set)
    for serverTag in hallServerSet:
        ipKey = Key_Server_Order % serverTag
        pipe.lpush(ipKey, 'closeServer')
    pipe.execute()
