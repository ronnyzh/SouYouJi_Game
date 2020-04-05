# -*- coding:utf-8 -*-
# !/usr/bin/python

"""
     荣誉场数据模型

"""
import random
import copy
import json
import traceback
from .honor_db_define import *
from server_common.web_db_define import *


def getNeedHonorDefault(redis,gameid):
    redis = redis
    if redis.exists(HONOR_ROOM_THRESHOLD % gameid):
        threshold_min = int(redis.hget(HONOR_ROOM_THRESHOLD % gameid, 'threshold_min') or 0)
    elif redis.exists(HONOR_ROOM_THRESHOLD % 'default'):
        threshold_min = int(redis.hget(HONOR_ROOM_THRESHOLD % 'default', 'threshold_min') or 0)
    else:
        threshold_min = 1000
    return threshold_min

def getSetting(redis,gameid='default',reverse=False):
    if redis.exists(HONOR_ROOM_INFOS % gameid):
        RoomInfos = redis.get(HONOR_ROOM_INFOS % gameid)
    else:
        RoomInfos = redis.get(HONOR_ROOM_INFOS % 'default')
    try:
        json_str = json.loads(RoomInfos)
    except:
        traceback.print_exc()
        return []
    else:
        RoomInfos = json_str
        print u'[getSetting] RoomInfos %s' % str(RoomInfos).replace('u\'', '\'').decode("unicode-escape")
        if reverse:
            RoomInfos.reverse()
        return RoomInfos

def getAccountCanJoinPlayId(redis, account, gameid='default'):
    user_table = redis.get(FORMAT_ACCOUNT2USER_TABLE % account)
    honor = int(redis.hget(user_table, 'honor') or 0)
    print u'[FilterCanJoinRoom] account[%s] honor[%s]' % (account, honor)
    # 获取可加入的场次ID
    canJoinPlayIdList = []
    for _setting in getSetting(redis,gameid,reverse=True):
        if not _setting['id']:
            continue
        _playid = _setting['id']
        if len(_setting['need']) == 2:
            min_need, max_need = _setting['need']
        else:
            min_need = _setting['need'][0]
            max_need = 0
        if min_need and honor < min_need:
            continue
        if max_need and honor > max_need:
            continue
        canJoinPlayIdList.append(_playid)
    return canJoinPlayIdList

def FilterCanJoinRoom(redis,account,gameid):
    '''
    找出玩家可加入的房间
    :param account: 玩家账号
    :return: Game类,房间号,场次ID
    思路:
    1.通过玩家荣誉值找到匹配的所有场次信息
    2.查找匹配的场次信息对应房间的人员情况,记录非空房
    3-1.如果2有找到,从人多到人少找出房间,返回
    3-2.如果2没找到,找到匹配场次中的最高场次,如果有空房,则进入,若无,则创建
    '''
    canJoinPlayIdDict = {}
    _roomid = None
    _game = None
    _playid = None
    canJoinPlayIdList = getAccountCanJoinPlayId(redis,account,gameid)
    for _PlayId in canJoinPlayIdList:
        honor_can_join_rooms_key = HONOR_CAN_JOIN_ROOM_HASH % (gameid, _playid)
        if redis.exists(honor_can_join_rooms_key):
            rooms_lenPlayer = redis.hgetall(honor_can_join_rooms_key)
            for _room, _lenPlayer in rooms_lenPlayer.iteritems():
                if not _lenPlayer:
                    continue
                canJoinPlayIdDict.setdefault(_lenPlayer, [])
                canJoinPlayIdDict[_lenPlayer].append(_room)
    print u'[FilterCanJoinRoom] 可加入的非空房List为 %s' % (canJoinPlayIdList)
    print u'[FilterCanJoinRoom] 可加入的非空房Dict为 %s' % (canJoinPlayIdDict)
    if canJoinPlayIdDict:
        for _lenPlayer in sorted(canJoinPlayIdDict.keys(), reverse=True):
            _roomid = random.choice(canJoinPlayIdDict[_lenPlayer])
    if not _game:
        # 不存在可加入的房间(非空)
        # 进入最大匹配的房间
        max_playid = max(canJoinPlayIdList)
        roomids = list(redis.smembers(GOLD_CAN_JOIN_ROOM_SET % (self.ID, max_playid)))
        canJoinRoomList = roomids
        if roomids:
            _roomid = random.choice(canJoinRoomList)
    print u'[FilterCanJoinRoom] _roomid[%s]' % (_roomid)
    return _roomid
