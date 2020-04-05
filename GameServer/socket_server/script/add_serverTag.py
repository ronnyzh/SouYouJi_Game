# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/11/16
Revision: 1.0.0
Description: Description
"""
import time
import random
from model.model_redis import getInst
from define.define_redis_key import *

redis = getInst()

while True:
    time.sleep(5)
    serverTag = '192.168.50.2:%s' % (random.randint(9700, 9999))
    redis.sadd(Key_Server_Set, serverTag)
    print('新增',serverTag)