#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    竞技比赛场模型
"""
from web_db_define import *
from admin  import access_module
from config.config import *
from common.log import *
import random
from datetime import datetime
import time
import os
import json
# --------------------------------  后台页面相关 -----------------------------------------------------


# 竞技场开关
PARTY_SWITCH = "party:comp:switch" # 0 关 1 开
# 竞技场开启时间
PARTY_TIME = "party:time"

def is_party_comp_open(redis):
    """
    获取竞技场开关
    :param redis: 
    :return: 
    """
    if not redis.exists(PARTY_SWITCH):
        return 0
    return int(redis.get(PARTY_SWITCH))

def set_party_comp(redis,switch):
    """
    竞技场开关
    :param redis: 
    switch: 0 关 1 开
    :return: 
    """
    return redis.set(PARTY_SWITCH,switch)

def modify_party_time(redis,timeList):
    """
    修改竞技场开启时间
    :param timeList:
    :return:
    """

    return redis.set(PARTY_TIME, timeList)

def get_party_time(redis):
    """
    获得竞技场开启时间
    """
    res = eval(redis.get(PARTY_TIME))
    log_debug("*****************获得竞技场开启时间:{0}-{1}".format(type(res),res))

    return res

def is_party_time(redis):
    """
    判断是否竞技场开启时间
    :param redis:
    :return:
    """
    lists = get_party_time(redis)
    dateNow = time.strftime('%Y-%m-%d {0}')
    nowTime = time.time()
    for timeList in lists:
        start = time.mktime(time.strptime(dateNow.format(timeList[0]),'%Y-%m-%d %H:%M:%S'))
        end = time.mktime(time.strptime(dateNow.format( timeList[1] or timeList[0]),'%Y-%m-%d %H:%M:%S'))
        if(nowTime >= start and nowTime <= end):
            return True
    return False

#  ----------------------------------------------   金币场      -----------------------------------------------
# 金币场配置
PARTY_GOLD_GAME_LIST = [
    {'id':0, 'title':'新手场', 'need':[2000,150000], 'baseScore':500, 'cost':600, 'gameid':'1', 'gameName':'贵溪麻将', 'maxMultiples':'2048倍'},
    {'id':1, 'title':'普通场', 'need':[20000,750000], 'baseScore':1500, 'cost':1500, 'gameid':'1', 'gameName':'贵溪麻将', 'maxMultiples':'2048倍'},
    {'id':2, 'title':'中级场', 'need':[30000], 'baseScore':3000, 'cost':4000, 'gameid':'1', 'gameName':'贵溪麻将', 'maxMultiples':'2048倍'},
    {'id':3, 'title':'高级场', 'need':[80000], 'baseScore':10000, 'cost':8000, 'gameid':'1', 'gameName':'贵溪麻将', 'maxMultiples':'2048倍'},
    {'id':4, 'title':'土豪场', 'need':[200000], 'baseScore':20000, 'cost':16000, 'gameid':'1', 'gameName':'贵溪麻将', 'maxMultiples':'2048倍'},
    {'id':5, 'title':'至尊场', 'need':[600000], 'baseScore':72000, 'cost':30000, 'gameid':'1', 'gameName':'贵溪麻将', 'maxMultiples':'2048倍'}
]

def get_GoldGameList(redis):
    """
    获取金币场场次
    """
    return PARTY_GOLD_GAME_LIST


"""
    金币场服务协议
"""
FORMAT_GOLD_SERVICE_PROTOCOL_TABLE = "goldservice:protocols"
FORMAT_GOLD_SERVICE_STATUS = "goldservice:status"

"""
    协议结果返回 
    partyservice:result:uuid
"""
RESULT_GOLD_SERVICE_PROTOCOL = "goldservice:result:%s"


def isGoldServiceOpening(redis):
    """
        查询金币场服务程序是否在线
    """
    if redis.exists(FORMAT_GOLD_SERVICE_STATUS):
        return True
    return False


def sendProtocol2GoldService(redis,protostr):
    """
        发送消息给partyService
        失败则为服务没启动或者异常
    """
    if not isGoldServiceOpening(redis):
        return
    redis.rpush(FORMAT_GOLD_SERVICE_PROTOCOL_TABLE, protostr)
    return True


def getProtocolFromGoldServiceResult(redis,_uuid,timeout=5):
    while timeout > 0:
        key = RESULT_GOLD_SERVICE_PROTOCOL % _uuid
        if redis.exists(key):
            return json.loads(redis.get(key))
        time.sleep(0.1)
        timeout = timeout - 0.1



"""
    竞技场协议
"""
FORMAT_PARTY_SERVICE_PROTOCOL_TABLE = "partyservice:protocols"
FORMAT_PARTY_SERVICE_STATUS = "partyservice:status"

"""
    协议结果返回 
    partyservice:result:uuid
"""
RESULT_PARTY_SERVICE_PROTOCOL = "partyservice:result:%s"


def isPartyServiceOpening(redis):
    """
        查询竞技场服务程序是否在线
    """
    if redis.exists(FORMAT_PARTY_SERVICE_STATUS):
        return True
    return False


def sendProtocol2OnePartyService(redis, protostr):
    """
        发送消息给partyService
        失败则为服务没启动或者异常
    """
    if not isPartyServiceOpening(redis):
        return
    redis.rpush(FORMAT_PARTY_SERVICE_PROTOCOL_TABLE, protostr)
    return True


def getProtocolFromPartyServiceResult(redis,_uuid,timeout=5):
    while timeout > 0:
        key = RESULT_PARTY_SERVICE_PROTOCOL % _uuid
        if redis.exists(key):
            return json.loads(redis.get(key))
        time.sleep(0.1)
        timeout = timeout - 0.1


#  ----------------------------------------------   福利系统      -----------------------------------------------
def do_PlayerCoin(redis, action, uid, account, coinNum, source):
    date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

    coinTotal = redis.get(USER4COIN % uid)
    coinTotal = int(coinTotal) if coinTotal else 0
    pipe = redis.pipeline()

    if not action:
        return False

    # 增加金币
    if action == "add":
        pipe.incrby(USER4COIN % uid, int(coinNum))
        coinChange = "+{0}".format(coinNum)
        coinTotal += coinNum
        res = coinNum
    # 修改金币
    if action == "to":
        pipe.set(USER4COIN % uid, int(coinNum))
        coinChange = int(coinNum) - coinTotal
        coinChange = "+{0}".format(coinChange) if coinChange > 0 else str(coinChange)
        res = coinChange
        coinTotal = int(coinNum)


    # 记录
    info = {'source': source, 'date': date, 'account':account, 'coinChange': coinChange, 'coinTotal': coinTotal}
    pipe.lpush(RECORD4USER_COIN % uid, json.dumps(info))
    pipe.execute()

    return True

def do_PlayerWelfareSign(redis, uid, account):
    """签到接口"""
    timestamp = time.mktime(time.localtime())
    key = WELFARE_USER_SIGN % (uid)
    # 检查最后一次签到
    lastInfo = redis.lindex(key,0)
    isSign = True
    if not lastInfo :
        isSign = False
    else:
        lastInfo = json.loads(lastInfo)
        lastTimestamp = lastInfo.get("timestamp","")
        if not time.strftime('%Y-%m-%d',time.localtime(lastTimestamp)) \
                == time.strftime('%Y-%m-%d',time.localtime(timestamp)):
            isSign = False

    if isSign:
        return False
    else:
        coinNum = random.randint(100,2000)
        res = do_PlayerCoin(redis, "add", uid, account, coinNum, "签到获得")
        if not res :
            log_debug("--------[error]do_PlayerWelfareSign coinNum:{0} account:{1}".format(coinNum,account))
            return {'code': 1, 'msg': '增加金币失败'}

        info = {'timestamp': timestamp, 'uid': uid, 'coinNum': coinNum}
        redis.lpush(key, json.dumps(info))

        return res

def do_PlayerWelfareInsurance(redis, uid, account):
    """低保接口"""
    timestamp = time.mktime(time.localtime())
    key = WELFARE_USER_INSURANCE % (uid)
    # 低保配置
    SIGN_MAX = 2        #每日领取次数
    SIGN_LINE = 2000    #低保线
    SIGN_COINNUM = 2000 #每次赠送金币数

    # 检查玩家金币数
    playerCoin = redis.get(USER4COIN % uid)
    playerCoin = playerCoin if playerCoin else 0
    if int(playerCoin) >= SIGN_LINE:
        return {'code':1,'msg':'未达到低保线无法领取'}

    # 检查最后一次低保
    lastInfo = redis.lindex(key,0)
    if not lastInfo:
        isSign = False
        isTimesOverflow = False
    else:
        lastInfo = json.loads(lastInfo)
        lastTimestamp = lastInfo.get("timestamp", "")
        isSameDate = time.strftime('%Y-%m-%d',time.localtime(lastTimestamp)) == time.strftime('%Y-%m-%d',time.localtime(timestamp))
        isSign = isSameDate
        isTimesOverflow = isSameDate and int(lastInfo.get("signTimes")) >= SIGN_MAX


    if isSign and isTimesOverflow:
        return {'code':1,'msg':'已经领取了 {0} 次'.format(SIGN_MAX)}
    else:
        coinNum = SIGN_COINNUM
        res = do_PlayerCoin(redis, "add", uid, account, coinNum, "低保获得")

        if not res :
            log_debug("--------[error]do_PlayerWelfareInsurance coinNum:{0} account:{1}".format(coinNum,account))
            return {'code': 1, 'msg': '增加金币失败'}

        signTimes = int(lastInfo.get("signTimes")) + 1 if lastInfo else 1
        info = {'timestamp': timestamp, 'uid': uid, 'coinNum': coinNum, 'signTimes': signTimes}

        redis.lpush(key, json.dumps(info))

        return {'code':0,'msg':'领取低保成功'}

def get_PlayerWelfareInfo(redis, account):
    """获取玩家签到、低保"""
    date = time.strftime('%Y-%m-%d',time.localtime())
    key = WELFARE_USER_SIGN % (account)
    res = redis.get(key)
    if not res :
        res = 0
    return res