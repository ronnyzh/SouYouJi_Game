# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/15
Revision: 1.0.0
Description: Description
"""

import json
import traceback

from define.define_consts import *
from define.define_web_redis_key import *
from model.model_event import *
from model.model_redis import *
from public.public_tornado import *
from public.public_func import *
from server.focusHandler.matchFocusHandler import MatchFocusHandler
from server.operate import MatchOperate


def verifyMatchNumber(key, value, *args, **kwargs):
    try:
        gameId, matchId, _ = value.split('-')
        return True
    except:
        traceback.print_exc()
    return False


class MatchHandler_dismiss(BaseRequestHandler):
    '''解散正在比赛的赛事'''

    @EventClass.befor(BaseRequestHandler.parseArgs, parserObj={
        'matchNumber': {'type': str, 'required': True, 'notEmpty': True, 'verifyFunc': verifyMatchNumber},
    })
    @EventClass.befor(BaseRequestHandler.checkSid)
    @record_http_request
    def post(self, matchNumber: str, *args, **kwargs):
        gameId, matchId, _ = matchNumber.split('-')
        redis = getInst()
        if not bool(redis.lrange(FORMAT_GAME_SERVICE_SET % (gameId), 0, -1)):
            self.finish({'msg': '服务器未开启', 'code': -1})
            return
        dismissMatchKey = "dismissMatch|%s|" % (matchNumber)
        self.factory.sendProtocol2GameService(gameId=gameId, protocolStr=dismissMatchKey)
        self.finish({'msg': '发送成功', 'code': 0})


class PingHandler(BaseRequestHandler):
    @record_http_request
    def get(self):
        self.finish({'msg': '成功', 'code': 0})

    post = get


class MatchHandler_enrollUsers(BaseRequestHandler):
    '''赛事已报名玩家'''

    @EventClass.befor(BaseRequestHandler.parseArgs, parserObj={
        'gameId': {'type': int, 'required': True, 'notEmpty': False},
        'matchId': {'type': int, 'required': True, 'notEmpty': False},
    })
    @record_http_request
    def get(self, gameId: int, matchId: int, *args, **kwargs):
        matchMgr = self.getMatchMgr(gameId=gameId, matchId=matchId)
        usersData = matchMgr.getEnrollUsers()
        self.finish({'msg': '获取成功', 'code': 0, 'data': usersData})

    @EventClass.befor(BaseRequestHandler.parseArgs, parserObj={
        'gameId': {'type': int, 'required': True, 'notEmpty': False},
        'matchId': {'type': int, 'required': True, 'notEmpty': False},
    })
    @record_http_request
    def delete(self, gameId: int, matchId: int, *args, **kwargs):
        '''删除赛事已报名玩家'''
        matchMgr = self.getMatchMgr(gameId=gameId, matchId=matchId)
        httpCallBackDatas = matchMgr.cancelAllEnrollUsers()
        self.finish({'msg': '删除成功', 'code': 0, 'data': httpCallBackDatas})


class MatchHandler_matchList(BaseRequestHandler):

    @EventClass.befor(BaseRequestHandler.checkSid)
    def get(self, sid: str, uid: int, *args, **kwargs):
        self.render('matchList.html', sid=sid, uid=uid, gameIdMap=gameIdMap, json=json)


class MatchHandler_infoList(BaseRequestHandler):

    @EventClass.befor(BaseRequestHandler.parseArgs, parserObj={
        'gameId': {'type': int, 'required': False, 'notEmpty': False},
        'matchId': {'type': int, 'required': False, 'notEmpty': False},
    })
    @EventClass.befor(BaseRequestHandler.checkSid)
    @record_http_request
    def post(self, uid: int, gameId: int, matchId: int, *args, **kwargs):
        flag, cb_data = MatchFocusHandler.infoList(self=self, uid=uid, gameId=gameId, matchId=matchId)
        self.finish(cb_data)


class MatchHandler_infoList_get(BaseRequestHandler):
    post = MatchHandler_infoList.get


class MatchHandler_enroll(BaseRequestHandler):

    @EventClass.befor(BaseRequestHandler.checkSid)
    @EventClass.befor(MatchOperate.getUserMatchEnrollInfo)
    @record_http_request
    def get(self, enrollInfo: dict, *args, **kwargs):
        if not enrollInfo:
            self.finish({'msg': '当前无已报名的赛事', 'code': 0})
        else:
            self.finish({'msg': '获取成功', 'data': enrollInfo, 'code': 0})

    @EventClass.befor(BaseRequestHandler.parseArgs, parserObj={
        'gameId': {'type': int, 'required': True},
        'matchId': {'type': int, 'required': True}
    })
    @EventClass.befor(BaseRequestHandler.checkSid)
    @EventClass.befor(MatchOperate.existMatchGameMatchId)
    @EventClass.befor(MatchOperate.getUserMatchEnrollInfo)
    @record_http_request
    def post(self, uid: int, gameId: int, matchId: int, enrollInfo: dict, *args, **kwargs):
        if enrollInfo:
            self.finish({'msg': '报名失败, 您当前已存在报名了的赛事, 不可同时报名多场比赛', 'data': {'enrollInfo': enrollInfo},
                         'code': -1, 'gameId': gameId, 'matchId': matchId})
            return
        matchMgr = self.getMatchMgr(gameId=gameId, matchId=matchId)
        if matchMgr.enroll_status != CanEnrollStatus:
            self.finish({'msg': '报名失败, 当前不可报名', 'code': -1, 'gameId': gameId, 'matchId': matchId})
        else:
            flag, cb_data = matchMgr.userEnroll_do(uid=uid)
            if not flag:
                self.finish({'msg': cb_data.get('msg', '报名失败, 请稍后重试'), 'code': -1, 'gameId': gameId,
                             'matchId': matchId})
            else:
                enrollInfo = cb_data.get('enrollInfo', {})
                changeTrade = cb_data.get('changeTrade', {})
                self.finish({'msg': '报名成功', 'data': {'enrollInfo': enrollInfo, 'changeTrade': changeTrade}, 'code': 0,
                             'gameId': gameId, 'matchId': matchId})

    @EventClass.befor(BaseRequestHandler.parseArgs, parserObj={
        'gameId': {'type': int, 'required': True},
        'matchId': {'type': int, 'required': True}
    })
    @EventClass.befor(BaseRequestHandler.checkSid)
    @EventClass.befor(MatchOperate.existMatchGameMatchId)
    @EventClass.befor(MatchOperate.getUserMatchEnrollInfo)
    @record_http_request
    def delete(self, uid: int, gameId: int, matchId: int, enrollInfo: dict, *args, **kwargs):
        if not enrollInfo:
            self.finish({'msg': '当前无已报名的赛事', 'code': -1, 'gameId': gameId, 'matchId': matchId})
        elif int(enrollInfo['state']) != MatchOperate.State_Enroll:
            self.finish({'msg': '你有正在进行的比赛,不能取消,请尽快加入比赛', 'data': enrollInfo, 'code': -1,
                         'gameId': gameId, 'matchId': matchId})
        elif int(enrollInfo['gameId']) != gameId or int(enrollInfo['matchId']) != matchId:
            self.finish({'msg': '所需取消报名的比赛并未报名,无需取消,存在其他已报名赛事', 'data': enrollInfo, 'code': -1,
                         'gameId': gameId, 'matchId': matchId})
        else:
            flag, cb_data = MatchOperate.userEnroll_cancel(self, gameId=gameId, matchId=matchId, uid=uid)
            self.finish(cb_data)


class MatchHandler_enroll_get(BaseRequestHandler):
    post = MatchHandler_enroll.get


class MatchHandler_enroll_post(BaseRequestHandler):
    post = MatchHandler_enroll.post


class MatchHandler_enroll_delete(BaseRequestHandler):
    post = MatchHandler_enroll.delete
