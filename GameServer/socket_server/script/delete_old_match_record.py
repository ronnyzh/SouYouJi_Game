# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/12/4
Revision: 1.0.0
Description: Description
"""
from model.model_redis import getInst
from define.define_redis_key import *

redis = getInst()

for _key in redis.scan_iter(Key_Match_matchNumber_Hesh % '*', 10):
    if redis.ttl(_key) == -1:
        print(_key)
        redis.expire(_key, 60)
