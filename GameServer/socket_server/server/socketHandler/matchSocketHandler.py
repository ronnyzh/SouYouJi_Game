# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/22
Revision: 1.0.0
Description: Description
"""
import traceback

from tornado.escape import json_decode

from define.define_consts import *
from define.define_web_redis_key import *
from define.define_redis_key import *
from model.model_redis import getInst
from proto import hall_match_pb2
from public.public_func import *
from public.public_tornado import BaseWebSocketHandler
from server.operate import UserOperate, MatchOperate


class MatchSocketHandler(BaseWebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(MatchSocketHandler, self).__init__(*args, **kwargs)
        self.sid = ''
        self.uid = 0

        self.readyJoinIgnoreTime = 0
        self.connectTime = None
        self.hexId = str(hex(id(self)))[2:]

        self.isNeedAutoPush = True

        self.userInfo = {}
        self.account = ''
        self.nickname = ''
        self.headImgUrl = ''

    def __str__(self):
        return '[Socket][%s] [uid:%s]' % (self.hexId, self.uid)

    def __detailed_str__(self):
        return '[Socket][%s][%s] [sid:%s] [uid:%s]' % (self.hexId, self.connectTime, self.sid, self.uid)

    def getRedis(self, dbNum=1):
        return getInst(dbNum=dbNum)

    def loadUserData(self):
        redis = self.getRedis()
        self.userInfo = redis.hgetall(FORMAT_USER_TABLE % self.uid)
        self.account = self.userInfo['account']
        self.nickname = self.userInfo['nickname']
        self.headImgUrl = self.userInfo['headImgUrl']

    def checkSid(self, sid):
        flag, cb_data = UserOperate.checkSid(self=self, sid=sid)
        self.sid = sid
        if not flag:
            actionType = Disconnected_actionType.relogin
            if cb_data.get('code', 0) == -4:
                actionType = Disconnected_actionType.disconnect
            self.close(code=1000, reason=cb_data.get('msg', u'未知'), actionType=actionType)
            return False
        self.uid = int(cb_data['uid'])
        self.loadUserData()
        return True

    def open(self, sid, *args, **kwargs):
        self.log('[open] sid=>%s' % sid)
        super(MatchSocketHandler, self).open(*args, **kwargs)
        if self.checkSid(sid):
            self.factory.addSocket(self)

    def close(self, code: int = None, reason: str = None, isSendResp: bool = True,
              actionType: Disconnected_actionType = Disconnected_actionType.disconnect) -> None:
        if isSendResp:
            sendResp = hall_match_pb2.S_C_Disconnected()
            sendResp.reason = reason or u'未知'
            sendResp.actionType = actionType
            sendResp.webSockCode = code or 1000
            self.factory.sendOne(self, sendResp)
        super(MatchSocketHandler, self).close(code=code, reason=reason)

    def on_close(self):
        if self.isConnect:
            self.factory.removeSocket(self)
        super(MatchSocketHandler, self).on_close()

    def on_message(self, message):
        try:
            self.factory.resolveMsg(self, message)
        except:
            traceback.print_exc()
            for tb in traceback.format_exc().splitlines():
                self.log(u'[ERROR][User-on_message] %s' % (tb), level='error')

    def sendMessage(self, message, binary=True):
        self.write_message(message, binary)

    def user_OnTick(self, timeStamp: int) -> None:
        redis = self.getRedis()

        flag, cb_data = UserOperate.checkSid(self=self, sid=self.sid)
        if not flag:
            actionType = Disconnected_actionType.relogin
            if cb_data.get('code', 0) == -4:
                actionType = Disconnected_actionType.disconnect
            self.close(code=1000, reason=cb_data.get('msg', u'未知'), actionType=actionType)
        else:
            if timeStamp > self.readyJoinIgnoreTime:
                self.push_user_match_readyJoin(redis, timeStamp)
                self.readyJoinIgnoreTime = 0

    def push_user_match_readyJoin(self, redis, timeStamp: int) -> None:
        _, cb_data = MatchOperate.getUserMatchEnrollInfo(self=self, uid=self.uid)
        enrollInfo = cb_data.get('enrollInfo', {})
        if not enrollInfo:
            return
        state = enrollInfo['state']
        if MatchOperate.State_ReadyStart <= state < MatchOperate.State_Ending:
            isAutoJoin = False
            if state > MatchOperate.State_ReadyStart:
                isAutoJoin = True
            else:
                matchNumber = enrollInfo['matchNumber']
                startTime = int(redis.hget(Key_Match_matchNumber_Hesh % (matchNumber), 'FirstGameStartTimeStamp') or 0)
                if 0 <= (startTime - timeStamp) <= 5 * 1000:
                    isAutoJoin = True
            sendResp = hall_match_pb2.S_C_match_readyJoin_tips()
            sendResp.isPush = True
            self.factory.setKey_enrollInfo(resp=sendResp, enrollInfo=enrollInfo)
            self.factory.setKey_matchJoinInfo(resp=sendResp, **enrollInfo, isAutoJoin=isAutoJoin)
            self.factory.sendOne(self, sendResp)
