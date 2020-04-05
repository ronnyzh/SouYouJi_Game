#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    商品自动续期脚本
"""
import sys
sys.path.insert(0, './server_common')
sys.path.insert(0, './mahjong')
from web_db_define import FISH_SHARE_NOT_TAKE_SETS,FISH_FIRST_SHARE_PER_DAY_SET,FISH_SHARE_TAKE_SETS
from datetime import datetime
import time
from common import log_util
import redis
import hashlib

def getInst(dbNum):
    global redisdb
    redisdb = redis.ConnectionPool(host="127.0.0.1", port=6379, db='1', password='')
    return redis.Redis(connection_pool=redisdb)

if __name__ == '__main__':
    redis = getInst(1)
    pipe  = redis.pipeline()

    log_util.debug('[date] share table clearing............')
    clear_tables = [FISH_SHARE_NOT_TAKE_SETS,FISH_FIRST_SHARE_PER_DAY_SET,FISH_SHARE_TAKE_SETS]
    for clear_table in clear_tables:
        log_util.debug('clear table[%s]'%(clear_table))
        pipe.delete(clear_table)

    pipe.execute()
    print 'Done......'
