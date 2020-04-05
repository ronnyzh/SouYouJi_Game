#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    审核公会进程
"""

import sys
sys.path.insert(0, 'server_common')
sys.path.insert(0, 'mahjong')
from web_db_define import *
from datetime import datetime
import time
from admin import access_module
import redis
import hashlib

def getInst(dbNum):
    global redisdb
    redisdb = redis.ConnectionPool(host="192.168.0.99", port=6379, db='1', password='')
    return redis.Redis(connection_pool=redisdb)


redis = getInst(1)

#进程执行心跳
SLEEP_SECS = 5.0
#倒计时结算
DISCOUNT_TIME = 60 * 3

AGENT_IDS = ['113388']

try:
    print 'check is monitor...'
    while True:
        nowTime = time.time()
        nowDate = datetime.now()
        for agentId in AGENT_IDS:
            memberIds = redis.lrange(JOIN_GROUP_LIST%(agentId),0,-1)
            pipe = redis.pipeline()
            for memberId in memberIds:
                if int(memberId) <= 0:
                    continue 
                print memberId
                status = redis.get(JOIN_GROUP_RESULT%(memberId)).split(':')[1]
                if int(status) == 0:
                    status = 1
                    pipe.set(JOIN_GROUP_RESULT%(memberId),"%s:%s"%(agentId,status))
                    pipe.sadd(FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE%(agentId), memberId)
                    pipe.hset(FORMAT_USER_TABLE%(memberId),'parentAg',agentId)
                    pipe.lrem(JOIN_GROUP_LIST%(agentId),memberId)
                    pipe.execute()
                    print 'memberId[%s] check success.'%(memberId)

        elapseTime = time.time() - nowTime
        sleepTime = max(SLEEP_SECS - elapseTime,0)

        time.sleep(sleepTime)

except Exception, e:
        print "[checkGroup][EXCEPT][TRACE] MatchServer is quit by Except! reason[%s]"%(e)
