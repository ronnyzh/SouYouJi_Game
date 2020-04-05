# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/25
Revision: 1.0.0
Description: Description
"""
import random
import time
import traceback
from typing import *
import copy

from redis import Redis

from define.define_consts import *
from define.define_redis_key import *
from define.define_web_redis_key import *
from model.model_redis import getInst, wraps_getRedis
from public.public_func import *
from server.operate.matchOperate import MatchOperate
from server.operate.userOperate import UserOperate
from proto import hall_match_pb2
from server.focusHandler.matchFocusHandler import MatchFocusHandler


class MatchMgr(object):

    def __init__(self, factory, gameid, id, title, play_num, rule, display, enroll_status, fee, feetype, rewardList,
                 gamename, matchtype, enrollNum=0, *args, **kwargs):
        self.factory = factory
        self.gameId = int(gameid)
        self.matchId = int(id)
        self.gameName = gamename
        self.title = title
        self.introduce = rule
        self.maxNum = int(play_num)
        self.fee = abs(int(fee))
        self.feeType = int(feetype)
        self.matchType = int(matchtype)

        self.display = int(display)  # 1:可见,0:不可见
        self.enroll_status = int(enroll_status)  # 1:可报名,0:不报名
        self.rewardList = rewardList
        self.enrollUids = []
        self.enrollNum = int(enrollNum)
        self.matchInfo = {}

        self.Match_EnrollUsers_Key = Key_Match_EnrollUsers_Zset % (self.gameId, self.matchId)
        self.Match_Game_MatchInfo_Key = Key_Match_Game_MatchInfo_Hesh % (self.gameId, self.matchId)
        self.updataEnroll()
        self.resetMatchInfo()

    def __str__(self) -> str:
        return '[%s-%s] title[%s] introduce[%s]' % (self.gameId, self.matchId, self.title, self.introduce)

    def log(self, msg: str = '', level: str = 'info') -> None:
        try:
            msg = '[MatchMgr][%s-%s] %s' % (self.gameId, self.matchId, msg)
            self.factory.log(msg=msg, level=level)
        except:
            traceback.print_exc()

    def resetMatchInfo(self) -> None:
        self.matchInfo = dict(
            gameId=self.gameId,
            matchId=self.matchId,
            gameName=self.gameName,
            title=self.title,
            introduce=self.introduce,
            maxNum=self.maxNum,
            fee=self.fee,
            feeType=self.feeType,
            matchType=self.matchType,
            display=self.display,
            enroll_status=self.enroll_status,
            rewardList=self.rewardList,
            enrollNum=self.enrollNum,
        )

    def updateMatchInfo(self, dateDict: dict) -> None:
        self.matchInfo.update(dateDict)

    def getMatchInfo(self):
        return {}

    @wraps_getRedis
    def getNowEnrollNum(self, redis: Redis):
        return redis.zcard(self.Match_EnrollUsers_Key)

    @wraps_getRedis
    def getNowEnrollList(self, redis: Redis, start: int = 0, end: int = -1) -> List[str]:
        return list(redis.zrange(self.Match_EnrollUsers_Key, start, end))

    @wraps_getRedis
    def updataEnroll(self, redis: Redis, needPush: bool = False) -> None:
        self.enrollUids = listStrToInt(self.getNowEnrollList(redis=redis), isSorted=True)
        hasDifference = False
        if self.enrollNum != len(self.enrollUids):
            # 检查是否有差异
            hasDifference = True
        self.enrollNum = len(self.enrollUids)
        self.updateMatchInfo({'enrollNum': self.enrollNum})
        self.factory.update_redisMatchInfo_enrollNum(gameId=self.gameId, matchId=self.matchId, enrollNum=self.enrollNum)
        if needPush and hasDifference:
            pass

    def getTheBestServerTable(self, serverList: Union[list, set, tuple]) -> str:
        redis = getInst()
        tmpServerList = []
        for _serverTable_ in serverList:
            _, _, _, currency, ip, port = _serverTable_.split(':')
            serverInfo = redis.hgetall(Key_Match_ServerInfo % (self.gameId, ip, port))
            thisServerDict = {
                'serverTable': _serverTable_,
                'curMatchNum': int(serverInfo.get('curMatchNum', 0)),
                'curPlayerNum': int(serverInfo.get('curPlayerNum', 0)),
            }
            thisServerDict['weight'] = thisServerDict['curMatchNum'] * thisServerDict['curPlayerNum']
            tmpServerList.append(thisServerDict)
        tmpServerList = sorted(tmpServerList, key=lambda x: x['weight'])
        serverTable = tmpServerList[0]['serverTable']
        return serverTable

    def onCheck(self, serverList: Union[list, set, tuple], timeStamp: int) -> None:
        redis = getInst()
        self.updataEnroll(redis=redis, needPush=True)

        if self.enrollNum >= self.maxNum:
            # 人数已满

            # serverTable = random.choice(serverList)
            serverTable = self.getTheBestServerTable(serverList)
            matchNumber = self.getMatchNumber(timeStamp=timeStamp)
            _, _, _, currency, ip, port = serverTable.split(':')
            saveData = {
                'ip': ip,
                'port': port,
                'matchNumber': matchNumber,
                'fullTime': timeStamp,
                'fullDate': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeStamp / 1000)),
                'state': MatchOperate.State_WaitJoinRoom,
            }
            enrollUsers = listStrToInt(redis.zrange(self.Match_EnrollUsers_Key, 0, self.maxNum - 1), isSorted=True)
            redis.zremrangebyrank(self.Match_EnrollUsers_Key, 0, self.maxNum - 1)
            self.log('[满人] %s' % enrollUsers)

            for uid in enrollUsers:
                Match_UserEnroll_Key = Key_Match_UserEnroll % uid
                redis.hmset(Match_UserEnroll_Key, saveData)
            self.factory.createMatch(gameId=self.gameId, matchNumber=matchNumber, uidsList=enrollUsers,
                                     saveData=saveData)
        else:
            self.log('[未满人] %s > %s => %s' % (self.maxNum, self.enrollNum, self.enrollUids))

    def getMatchNumber(self, timeStamp: int) -> str:
        return '%s-%s-%s' % (self.gameId, self.matchId, timeStamp)

    def userEnroll_do(self, uid: Union[str, int]) -> Tuple[bool, dict]:
        if self.enroll_status != CanEnrollStatus:
            return False, {'msg': '当前不可报名', 'code': -1}
        try:
            changeTrade = {}
            redis = getInst()
            if self.fee:
                if self.feeType == Define_Currency.Currency_roomCard:
                    flag, roomCard = UserOperate.lostRoomCard(self=self, uid=uid, number=self.fee)
                    if not flag:
                        return False, {'msg': '报名费用不足', 'code': -1}
                    changeTrade['curNumber'] = roomCard
                changeTrade['tradeType'] = self.feeType
                changeTrade['changeNumber'] = -self.fee

            Match_UserEnroll_Key = Key_Match_UserEnroll % uid
            pipe = redis.pipeline()
            enrollInfo = {
                'gameId': self.gameId,
                'matchId': self.matchId,
                'state': MatchOperate.State_Enroll,
                'feeType': self.feeType,
                'fee': self.fee,
            }
            pipe.hmset(Match_UserEnroll_Key, enrollInfo)
            pipe.zadd(self.Match_EnrollUsers_Key, {uid: int(time.time() * 1000)})
            pipe.execute()
        except Exception as err:
            traceback.print_exc()
            for tb in traceback.format_exc().splitlines():
                self.log(u'[ERROR][MatchMgr-userEnroll_do] %s' % (tb), level='error')
            return False, {'msg': '发生错误[%s]' % (err), 'code': -1}
        else:
            self.updataEnroll(redis=redis, needPush=True)
            return True, {'enrollInfo': enrollInfo, 'changeTrade': changeTrade, 'code': 0}

    def userEnroll_cancel(self, uid: Union[str, int]) -> Tuple[bool, dict]:
        try:
            changeTrade = {}
            redis = getInst()
            if self.fee:
                if self.feeType == Define_Currency.Currency_roomCard:
                    flag, roomCard = UserOperate.addRoomCard(self=self, uid=uid, number=self.fee)
                    changeTrade['curNumber'] = roomCard
                changeTrade['tradeType'] = self.feeType
                changeTrade['changeNumber'] = self.fee

            Match_UserEnroll_Key = Key_Match_UserEnroll % uid
            pipe = redis.pipeline()
            pipe.delete(Match_UserEnroll_Key)
            pipe.zrem(self.Match_EnrollUsers_Key, uid)
            pipe.execute()
        except Exception as err:
            traceback.print_exc()
            for tb in traceback.format_exc().splitlines():
                self.log(u'[ERROR][MatchMgr-userEnroll_cancel] %s' % (tb), level='error')
            return False, {'msg': '发生错误[%s]' % (err), 'code': -1}
        else:
            self.updataEnroll(redis=redis, needPush=True)
            return True, {'changeTrade': changeTrade, 'code': 0}

    @wraps_getRedis
    def getEnrollUsers(self, redis: Redis) -> dict:
        usersData = {'users': {}, 'count': 0}
        enrollUids = listStrToInt(redis.zrange(self.Match_EnrollUsers_Key, 0, -1), isSorted=True)
        userKeys = ['nickname', 'account']
        for _uid in enrollUids:
            userInfo = redis.hmget(FORMAT_USER_TABLE % _uid, *userKeys)
            usersData['users'][_uid] = {}
            for index, key in enumerate(userKeys):
                usersData['users'][_uid][key] = userInfo[index]
        usersData['count'] = len(enrollUids)
        return usersData

    @wraps_getRedis
    def cancelAllEnrollUsers(self, redis: Redis) -> Dict:
        '''
        取消该赛事所有报名
        :param redis:
        :param isGiveBack: 是否返还报名费
        :return:
        '''
        enrollUids = listStrToInt(redis.zrange(self.Match_EnrollUsers_Key, 0, -1), isSorted=True)
        httpCallBackDatas = {'success': {}, 'fail': {}}
        sendResp = hall_match_pb2.S_C_match_enroll_cancel()
        sendResp.gameId = self.gameId
        sendResp.matchId = self.matchId
        sendResp.isPush = True
        sendResp.msg = '举办方取消了%s的赛事报名' % (self.title)
        for uid in enrollUids:
            flag, cb_data = self.userEnroll_cancel(uid=uid)
            if flag:
                httpCallBackDatas['success'][uid] = cb_data.copy()
            else:
                httpCallBackDatas['fail'][uid] = cb_data.copy()

            if uid in self.factory.uidSocketMgrs:
                copySendResp = copy.deepcopy(sendResp)
                socket = self.factory.uidSocketMgrs[uid]
                changeTrade = cb_data.get('changeTrade', {})
                if changeTrade:
                    self.factory.setKey_changeTrade(copySendResp, changeTrade)
                self.factory.sendOne(socket, copySendResp)
            MatchFocusHandler.send_mail(
                uids_list=uid, title='比赛场取消报名须知',
                body='十分抱歉,举办方取消了%s的赛事报名,报名费用已实时返还,请留意。\n%s-%s' % (self.title, self.gameId, self.matchId),
                emailType=Email_Type.notice)
        return httpCallBackDatas
