#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    协议方法
"""

import re
import time
from web_db_define import *
from datetime import datetime, date
from common.log import *

def tryCloseServer(redis,gameId):
    """
    尝试关闭游戏服务
    """

    protocolStr = HEAD_SERVICE_PROTOCOL_GAME_CLOSE
    #通知游戏服务器关服
    sendProtocol2GameService(redis, gameId, protocolStr)

def waitServer(redis,gameId, isStartup):
    """
    等待频道关闭
    """
    count = 600
    while count > 0:
        isLaunch = redis.lrange(FORMAT_GAME_SERVICE_SET%(gameId),0,-1)
        if isStartup == bool(isLaunch):
            return True
        count -= 1
        time.sleep(0.5)
    return False

def serviceNoticeMemberRefresh(redis, account, excludeServiceTag = None):
    """
    """
    pass

def serviceNoticeKickMember(redis, account):
    """
        通知服务端踢出玩家协议
    """
    pass


def sendProtocol2GameService(redis, gameId, protocolStr, serviceFind = None):
    """
        发送协议给游戏服务器
    """
    #assert gameId in GAME_IDS
    serverList = redis.lrange(FORMAT_GAME_SERVICE_SET%(gameId), 0, -1)
    for serverTable in serverList:
        if serviceFind and serverTable.find(serviceFind) == -1:
            continue
        print serverTable
        _, _, _, currency, ip, port = serverTable.split(':')
        print FORMAT_SERVICE_PROTOCOL_TABLE%(gameId, '%s:%s:%s'%(currency, ip, port)), protocolStr
        redis.rpush(FORMAT_SERVICE_PROTOCOL_TABLE%(gameId, '%s:%s:%s'%(currency, ip, port)), protocolStr)

def sendProtocol2AllGameService(redis, protocolStr,game="MAHJONG"):
    """
        发送协议给所有游戏服务器
    """
    if game == "MAHJONG":
        gameIds = redis.lrange(GAME_LIST,0,-1)
    elif game == "FISH":
        gameIds = redis.lrange(FISH_ROOM_LIST,0,-1)
    else:
        gameIds = []
        
    for gameId in gameIds:
        isRunning = isGameServiceRunning(redis,gameId)
        if isRunning:
            sendProtocol2GameService(redis, gameId, protocolStr)


def isGameServiceRunning(redis, gameId):
    return bool(redis.lrange(FORMAT_GAME_SERVICE_SET%(gameId), 0, -1))
