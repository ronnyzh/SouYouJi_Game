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

IP = '192.168.50.2'
PORT = '9797'

if __name__ == '__main__':
    redis = getInst()
    ipKey = Key_Server_Order % ('%s:%s' % (IP, PORT))
    redis.lpush(ipKey, 'closeServer')
