#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    大厅广播调度进程
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

def do_clearContainBrocast():
    """
    重启时清除维护广播
    """
    system_contain_bro = redis.lrange(HALL_BRO_CONTAIN_ALL_LIST%(0),0,-1)
    fish_system_bro  = redis.lrange(FISH_BRO_CONTAIN_ALL_LIST%(0),0,-1)
    agent_contain_bro  = redis.lrange(HALL_BRO_CONTAIN_ALL_LIST%(2),0,-1)
    play_set           = redis.smembers(HALL_BRO_PLAY_SET)
    if not system_contain_bro:
        system_contain_bro = []
    if not agent_contain_bro:
        agent_contain_bro = []

    system_contain_bro,agent_contain_bro,fish_system_bro = list(system_contain_bro),list(agent_contain_bro),list(fish_system_bro)
    system_contain_bro.extend(agent_contain_bro)
    system_contain_bro.extend(fish_system_bro)

    for bro in system_contain_bro:
        if bro in play_set:
            redis.srem(HALL_BRO_PLAY_SET,bro)
            print '[try do_clearContainBrocast] broadId[%s] is remove..'%(bro)

try:
    print '[%s] broadManager is running..'%(datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S"))
    do_clearContainBrocast()
    while True:
        nowTime = time.time()
        nowDate = datetime.now()
        borads = redis.lrange(HALL_BRO_LIST,0,-1)
        borads_fish = redis.lrange(FISH_BRO_LIST,0,-1)
        borads,borads_fish = list(borads),list(borads_fish)
        borads.extend(borads_fish)
        print '[%s][try getBrocast] borads[%s]'%(datetime.strftime(nowDate,"%Y-%m-%d %H:%M:%S"),borads)
        out_set = redis.smembers(HALL_BRO_OUT_SET)
        play_set = redis.smembers(HALL_BRO_PLAY_SET)
        for borad in borads:
            if borad in out_set:
                continue
            if borad in play_set:
                print '[%s][try Brocast] borads[%s] is boradding....'%(datetime.strftime(nowDate,"%Y-%m-%d %H:%M:%S"),borad)
            broad_table = HALL_BRO_TABLE%(borad)
            boradInfo = redis.hgetall(broad_table)
            start_date = datetime.strptime(boradInfo['start_date'],'%Y-%m-%d %H:%M')
            end_date = None
            if boradInfo['end_date']:
                end_date   = datetime.strptime(boradInfo['end_date'],'%Y-%m-%d %H:%M')

            if start_date > nowDate:#未到开始时间
                continue

            if end_date and end_date<=nowDate:
                #播放时间已结束
                if borad not in out_set:
                    redis.hset(broad_table,'status',2)
                    redis.srem(HALL_BRO_PLAY_SET,borad)
                    redis.sadd(HALL_BRO_OUT_SET,borad)
                    print '[%s] broadId[%s] is endding.'%(datetime.strftime(nowDate,"%Y-%m-%d %H:%M:%S"),borad)
                continue

            if start_date <= nowDate:
                if borad not in play_set:
                    redis.hset(broad_table,'status',1)
                    redis.sadd(HALL_BRO_PLAY_SET,borad)
                    print '[%s] broadId[%s] is ready broading.'%(datetime.strftime(nowDate,"%Y-%m-%d %H:%M:%S"),borad)
                continue

        elapseTime = time.time() - nowTime
        sleepTime = max(SLEEP_SECS - elapseTime,0)

        time.sleep(sleepTime)

except Exception, e:
        print "[checkGroup][EXCEPT][TRACE] MatchServer is quit by Except! reason[%s]"%(e)
