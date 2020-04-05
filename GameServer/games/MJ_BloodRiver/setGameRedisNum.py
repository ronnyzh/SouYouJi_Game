# -*- coding:utf-8 -*-
"""
设置gameid对应的的数据库编号
"""

from common.common_db_define import *
import redis_instance

GAME_ID = 341
IP = '172.18.176.198'
PORT = '6381'
DB_NUM = 9
PASSWD = '168joyvick'

redis = redis_instance.getInst(1)
redis.hmset(GAME2REDIS%(GAME_ID), {'ip':IP, 'port':PORT, 'num':DB_NUM, 'passwd':PASSWD})
for key in redis.keys(GAME2REDIS%('*')):
    print key
    print redis.hgetall(key)