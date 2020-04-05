# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/15
Revision: 1.0.0
Description: Description
"""
from define.define_redis_key import *
from define.define_web_redis_key import *
from model.model_redis import getInst
from public import public_func
from server.factorys.tornadoFactory import baseFactory


class MatchOperate(object):
    State_None = 0  # 无状态(大厅状态)
    State_Enroll = 1  # 报完名,等待(大厅状态)
    State_WaitJoinRoom = 2  # 比赛满足,等待玩家进入房间(大厅状态)
    State_ReadyStart = 3  # 游戏已接管,等待比赛开始(倒计时)(游戏状态)
    State_Matching = 4  # 比赛进行中(游戏状态)
    State_Balance = 5  # 比赛结束,结算中(游戏状态)

    State_Ending = 10  # 比赛完美结束
    State_Dismissing = 11  # 比赛正在被解散
    State_Have_Dismiss = 12  # 比赛已解散

    @classmethod
    def existMatchGame(cls, self, gameId, *args, **kwargs):
        if isinstance(self, baseFactory):
            factory = self
        else:
            factory = self.factory
        matchInfoMap = factory.matchMgrMap
        if gameId and gameId not in matchInfoMap:
            return False, {'msg': '赛事错误, 没有该游戏的相关赛事', 'gameId': gameId, 'code': -1}
        return True, {}

    @classmethod
    def existMatchGameMatchId(cls, self, gameId, matchId, *args, **kwargs):
        if isinstance(self, baseFactory):
            factory = self
        else:
            factory = self.factory
        matchMgrMap = factory.matchMgrMap
        if gameId not in matchMgrMap:
            return False, {'msg': '赛事错误, 没有该游戏的相关赛事', 'gameId': gameId, 'matchId': matchId, 'code': -1}
        elif matchId not in matchMgrMap[gameId]:
            return False, {'msg': '赛事错误, 该游戏不存在所报名的赛事', 'gameId': gameId, 'matchId': matchId, 'code': -1}
        return True, {}

    @classmethod
    def getServerList(cls, self, gameId: int, *args, **kwargs):
        redis = getInst()
        serverList = redis.lrange(FORMAT_GAME_SERVICE_SET % gameId, 0, -1)
        return True, dict(serverList=serverList)

    @classmethod
    def getUserMatchEnrollInfo(cls, self, uid: int, *args, **kwargs):
        redis = getInst()
        Match_UserEnroll_Key = Key_Match_UserEnroll % uid
        Match_UserEnrollInfo = redis.hgetall(Match_UserEnroll_Key)
        Match_UserEnrollInfo = public_func.dictParseValue(parserObj={
            'gameId': {'type': int},
            'matchId': {'type': int},
            'state': {'type': int},
            'port': {'type': int},
            'fullTime': {'type': int},
        }, onlyParseKey=False, **Match_UserEnrollInfo)
        return True, dict(enrollInfo=Match_UserEnrollInfo)

    @classmethod
    def userEnroll_cancel(cls, self, gameId: int, matchId: int, uid: int, *args, **kwargs):
        if isinstance(self, baseFactory):
            factory = self
        else:
            factory = self.factory
        matchMgr = factory.getMatchMgr(gameId=gameId, matchId=matchId)
        if not matchMgr:
            return False, {'msg': '赛事不存在', 'code': -1, 'gameId': gameId, 'matchId': matchId}
        elif matchMgr.userEnroll_cancel(uid=uid):
            return True, {'msg': '取消比赛报名成功', 'gameId': gameId, 'matchId': matchId, 'code': 0}
        else:
            return False, {'msg': '取消比赛报名失败', 'code': -1, 'gameId': gameId, 'matchId': matchId}
