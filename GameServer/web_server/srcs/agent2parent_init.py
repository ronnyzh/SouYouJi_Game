#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    所有代理的上级代理做一个映射脚本
"""

import sys
sys.path.insert(0, 'server_common')
sys.path.insert(0, 'mahjong')
from web_db_define import *
from datetime import datetime,time
from config.config import *
import redis
import hashlib


serverList = [
        'http://127.0.0.1:9798',
        'http://192.168.0.18:9797',
        'http://192.168.0.155:9797'
]

def getInst(dbNum):
    global redisdb
    redisdb = redis.ConnectionPool(host="127.0.0.1", port=6379, db='1', password='')
    return redis.Redis(connection_pool=redisdb)


redis = getInst(1)


agentIDs = redis.smembers(AGENT_ID_TABLE)
for agent in agentIDs:
    parentId = redis.hget(AGENT_TABLE%(agent),'parent_id')
    if not redis.exists(AGENT2PARENT%(agent)):
        redis.set(AGENT2PARENT%(agent),parentId)
        print 'set AGENT2PARENT[%s] success.'%(agent)
    else :
        print 'set AGENT2PARENT[%s] exists.'%(agent)





