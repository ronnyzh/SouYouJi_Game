# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/23
Revision: 1.0.0
Description: Description
"""
import traceback

from define.define_web_redis_key import *
from model.model_redis import getInst


class UserOperate(object):

    @classmethod
    def checkSid(cls, self, sid, uid='', *args, **kwargs):
        redis = getInst()
        if uid:
            verfiySid = None
        elif sid:
            SessionTable = FORMAT_USER_HALL_SESSION % (sid)
            if not redis.exists(SessionTable):
                return False, {'code': -3, 'msg': 'sid超时', 'osid': sid}
            account, uid = redis.hmget(SessionTable, ('account', 'uid'))
            verfiySid = redis.get(FORMAT_USER_PLATFORM_SESSION % (uid))
        else:
            return False, {'code': -3, 'msg': 'sid不能为空'}
        if verfiySid and sid != verfiySid:
            return False, {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
        if redis.exists(FORMAT_USER_TABLE % uid):
            return True, dict(sid=sid, uid=int(uid))
        return False, {'code': -5, 'msg': '该用户不存在', 'osid': sid}

    @classmethod
    def getRoomCard(cls, self, uid):
        redis = getInst()
        parentAg = redis.hget(FORMAT_USER_TABLE % uid, 'parentAg')
        roomCards = redis.get(USER4AGENT_CARD % (parentAg, uid))
        if roomCards and int(roomCards) > 0:
            roomCards = int(roomCards)
        else:
            roomCards = 0
        return roomCards

    @classmethod
    def lostRoomCard(cls, self, uid, number):
        number = abs(number)
        redis = getInst()
        parentAg = redis.hget(FORMAT_USER_TABLE % uid, 'parentAg')
        roomCards = redis.incrby(USER4AGENT_CARD % (parentAg, uid), -number)
        if roomCards < 0:
            roomCards = redis.incrby(USER4AGENT_CARD % (parentAg, uid), number)
            return False, roomCards
        return True, roomCards

    @classmethod
    def addRoomCard(cls, self, uid, number):
        try:
            number = abs(number)
            redis = getInst()
            parentAg = redis.hget(FORMAT_USER_TABLE % uid, 'parentAg')
            roomCards = redis.incrby(USER4AGENT_CARD % (parentAg, uid), number)
            return True, roomCards
        except:
            traceback.print_exc()
            return False, 0
