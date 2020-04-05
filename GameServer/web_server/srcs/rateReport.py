#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    DB初始化
"""

import sys
sys.path.insert(0, 'server_common')
sys.path.insert(0, 'mahjong')
from web_db_define import *
from datetime import datetime,time
from admin import access_module
import redis
import hashlib

def getInst(dbNum):
    global redisdb
    redisdb = redis.ConnectionPool(host="192.168.0.99", port=6379, db='1', password='')
    return redis.Redis(connection_pool=redisdb)


redis = getInst(1)

#初始化管理账号
curTime = datetime.now()
pipe = redis.pipeline()

# id


"""
    配置代理名称和钻石
    代理名称            ：       钻石数
"""

curTime = datetime.now()
date = curTime.strftime("%Y-%m-%d")

def countRateOfAgent(redis,agentId,roomcardNumber,unitPrice,lowerRate=0):
        curTime = datetime.now()
        date = curTime.strftime("%Y-%m-%d")
        parentTable = AGENT_TABLE%(agentId)
        parentType,parentrate,parentId = redis.hmget(parentTable,('type','shareRate','parent_id'))
        if not parentrate:
            AGENT_RATE_TABLE = AGENT_COMPAY_RATE_DATE % (agentId,date)
        else:
            AGENT_RATE_TABLE =AGENT_RATE_DATE%(agentId,parentrate,unitPrice,date)
        redis.hincrby(AGENT_RATE_TABLE,'number',amount=roomcardNumber)
        redis.hset(AGENT_RATE_TABLE,'unitPrice',unitPrice)
        redis.hset(AGENT_RATE_TABLE,'rate',parentrate)
        if parentType == '1':
            RemainPrice = float(unitPrice) - float(lowerRate)
            if RemainPrice > 0:
                redis.hincrbyfloat(AGENT_RATE_TABLE, 'rateTotal', amount=RemainPrice * roomcardNumber)
        else:
            remainPrice = float(unitPrice) -  float(lowerRate)
            if remainPrice <= 0:
                countRateOfAgent(redis,parentId,roomcardNumber,unitPrice,lowerRate)
            else:
                parent1Type, parent1Rate = redis.hmget( AGENT_TABLE % (parentId), ('type', 'shareRate'))
                if parent1Type !='1':
                    if parentrate > parent1Rate:
                        parentrate = parent1Rate
                firstRemainPrice = float(unitPrice) - float(parentrate)
                if firstRemainPrice <=0:
                    Rate = float(unitPrice) - float(lowerRate)
                    redis.hincrbyfloat(AGENT_RATE_TABLE,'rateTotal',amount=Rate*roomcardNumber)
                    redis.hincrbyfloat(AGENT_RATE_TABLE, 'meAndNextTotal', amount=float(unitPrice) * roomcardNumber)
                    countRateOfAgent(redis,parentId,roomcardNumber,unitPrice,parentrate)
                else :
                    Rate = float(parentrate) - float(lowerRate)
                    redis.hincrbyfloat(AGENT_RATE_TABLE,'rateTotal',amount=Rate*roomcardNumber)
                    redis.hincrbyfloat(AGENT_RATE_TABLE, 'meAndNextTotal', amount=float(parentrate) * roomcardNumber)
                    redis.hincrbyfloat(AGENT_RATE_TABLE, 'superRateTotal', amount=firstRemainPrice*roomcardNumber)
                    countRateOfAgent(redis,parentId,roomcardNumber,unitPrice,parentrate)
agentId = '134253'
number = '10'
AgentTable = AGENT_TABLE%(agentId)
unitPrice,parentId=redis.hmget(AgentTable,'unitPrice','parent_id')
if not unitPrice:
    Agent1Table = AGENT_TABLE%(parentId)
    unitPrice,parentId=redis.hmget(Agent1Table,'unitPrice','parent_id')
print 'unitPrice',unitPrice
print 'agentId',agentId
if unitPrice:
    countRateOfAgent(redis,agentId,int(number),unitPrice)

    print 'success'
else :
    print 'not unitPrice'
# AgentTable = AGENT_TABLE%(agentId)
# parentId = redis.hget(AgentTable,'parent_id')

# AGENT_RATE_TABLE =AGENT_RATE_DATE%('157027',1,price,date)
# AGENT_RATE_TABLE1 = AGENT_RATE_DATE%('343474',3,5,date)
# AGENT_RATE_TABLE2 = AGENT_COMPAY_RATE_DATE%('585328',date)
# print redis.hgetall(AGENT_RATE_TABLE)
# print redis.hgetall(AGENT_RATE_TABLE1)
# print redis.hgetall(AGENT_RATE_TABLE2)

