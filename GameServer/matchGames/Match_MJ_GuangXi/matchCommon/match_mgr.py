# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/17
Revision: 1.0.0
Description: Description
"""
import time
import traceback
import copy
import random
import json
from datetime import datetime
from pprint import pprint, pformat

from common import consts
from publicCommon import logger_mgr, timer
from .match_db_define import *
from .define_mysql_key import *
from .match_record import *
import redis_instance
import match_pb2
from .match_consts import *
from .sqlFormat import *

isMahjong = False
try:
    from common import mahjong_pb2
except:
    from common import baseProto_pb2, poker_pb2
else:
    baseProto_pb2 = mahjong_pb2
    poker_pb2 = mahjong_pb2
    isMahjong = True

m_logger = logger_mgr.getLogger('matchServer')


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


class enum_balanceType(object):
    none = 0
    wait = 1  # 等待下局
    rise = 2  # 晋级
    eliminate = 3  # 淘汰
    rank = 4  # 赛事已结算


class MatchMgr(object):
    '''比赛管理器'''

    def __init__(self, server, matchNumber, uidsList, gameId, matchId, matchInfo, *args, **kwargs):
        self.server = server
        # 每个房间的人数
        self.gameIdMap = {}
        self.curRoundNum = 0
        self.curRotation = 0
        self.curRotationRoundNum = 0
        self.roundGameMap = {}
        self.curRoundRooms = []
        self.curRoundRooms_balance = []
        self.curRoundRooms_notBalance = []
        # 玩家
        self.userIds = []
        self.curUserIds = []
        self.curPlayerNum = 0
        self.maxPlayerCount = self.server.getMaxPlayerCount()

        self.matchNumber = matchNumber
        self.matchInitTime = int(matchNumber.split('-')[-1])
        self.matchEndTime = 0
        self.matchDate = datetime.fromtimestamp(self.matchInitTime / 1000).strftime("%Y-%m-%d %H:%M:%S")
        self.gameId = gameId
        self.matchId = matchId
        self.matchInfo = matchInfo
        self.initData(**matchInfo)

        self.tryCreateGame()

        self.matchState = MatchOperate.State_None
        self.timerMgr = timer.TimersMgr(self)

        assert len(set(uidsList)) == self.maxPlayerNum
        self.matchRecordMgr = MatchRecordMgr(self)
        self.joinUsersByUid(uidsList)

        self.Match_EnrollUsers_Key = Key_Match_EnrollUsers_Zset % (self.gameId, self.matchId)
        self.Match_Game_MatchInfo_Key = Key_Match_Game_MatchInfo_Hesh % (self.gameId, self.matchId)
        self.Match_matchNumber_Key = Key_Match_matchNumber_Hesh % (self.matchNumber)
        self.Match_Gaming_matchNumber_Key = Key_Match_GameId_matchNumber_Gameing_Set % (self.gameId)
        self.Match_EndBalance_matchNumber_Key = Key_Match_GameId_matchNumber_EndBalance_Set % (self.gameId)

        self.BalanceDatas = {}
        self.dismissStartTime = 0
        self.dismissReason = ''
        # 比赛最大时长,如果因为BUG导致赛事超时,就会解散
        self.matchOvertime = 1000 * 60 * 60

        self.total_award_num = 0

        self.sql_save_match_recode_start()

    def __str__(self):
        return u'[%s] curRotation[%s] curRoundNum[%s] userIds => %s gameIdMap => %s' % \
               (self.matchNumber, self.curRotation, self.curRoundNum, self.userIds, self.gameIdMap)

    def getRedis(self, dbNum=1):
        redis = redis_instance.getInst(dbNum=dbNum)
        return redis

    def initData(self, title, rule, play_num, rewardList, roundNums, roundPlayers, fee, feetype, matchtype, **kwargs):
        self.title = title
        self.introduce = rule
        self.maxPlayerNum = int(play_num)
        self.matchType = int(matchtype)
        self.rewardList = rewardList
        self.fee = abs(int(fee))
        self.feeType = int(feetype)
        self.setRewardList()
        self.roundNums = list(map(int, roundNums.split(',')))
        self.roundPlayers = list(map(int, roundPlayers.split(',')))
        self.maxRoundNum = self.roundNums[-1]
        self.checkRoundPlayersAndNums()

    def tryCreateGame(self):
        rule = str(self.server.getMatchRoomRule())
        _game = self.server.getGameModule(self, rule, curRoundNum=0, matchMgr=self, describe=u'测试房间')
        del _game

    def setRewardList(self):
        self.rewardMgr = {}
        rewardList = json.loads(self.rewardList)
        for _reward_ in rewardList:
            rank = int(_reward_.get('rank', 0))
            self.rewardMgr[rank] = dict(
                rank=rank,
                field=_reward_.get('field', '未知').decode('utf-8'),
                currency_type=int(_reward_.get('currency_type', 0)),
                currency_count=int(_reward_.get('currency_count', 0)),
            )
        self.logger(u'[setRewardList] %s' % (pformat(self.rewardMgr)))

    def checkRoundPlayersAndNums(self):
        assert len(self.roundNums) == len(set(self.roundNums))
        assert len(self.roundPlayers) == len(set(self.roundPlayers))
        assert self.roundNums == sorted(self.roundNums)
        assert self.roundPlayers == sorted(self.roundPlayers, reverse=True)
        assert not filter(lambda x: x % self.maxPlayerCount != 0, self.roundPlayers)
        assert self.roundPlayers[0] < self.maxPlayerNum

    def logger(self, msg, level='info'):
        m_logger.info(u'[MatchMgr][%s][%s:%s] %s' % (self.matchNumber, self.curRotation, self.curRoundNum, msg))

    def onTick(self, timestamp):
        self.timerMgr.check_timer()
        if timestamp - self.matchInitTime >= self.matchOvertime:
            self.dismiss(reason=u'赛事超时')

    def setCurUserIds(self, curUserIds):
        if self.curUserIds == curUserIds:
            return
        self.curUserIds = curUserIds
        self.curPlayerNum = len(self.curUserIds)
        self.setCurPlayerNum()

    def setCurPlayerNum(self):
        redis = self.getRedis()
        self.saveRedisMatch({'curPlayerNum': self.curPlayerNum})

    def setMatchState(self, matchState):
        self.matchState = matchState
        self.saveRedisMatch({'matchState': self.matchState})
        self.redis_save_userEnrollInfo(state=self.matchState)

    def checkMatchState(self, matchState):
        return self.matchState == matchState

    def joinList(self, listData, isSorted=False):
        data = map(str, listData)
        if isSorted:
            data = sorted(listData)
        return ','.join('%s' % _data for _data in data)

    def redis_save_match(self):
        redis = self.getRedis()
        self.saveRedisMatch({
            'serviceTag': self.server.serviceTag,
            'matchNumber': self.matchNumber,
            'matchInfo': json.dumps(self.matchInfo),
            'userIds': self.joinList(self.userIds, isSorted=True),
            'roundNums': self.joinList(self.roundNums),
            'roundPlayers': self.joinList(self.roundPlayers),
            'maxRoundNum': self.maxRoundNum,
            'matchState': self.matchState,
        })
        redis.sadd(self.Match_Gaming_matchNumber_Key, self.Match_matchNumber_Key)

    def setCurAttrToRedis(self):
        self.saveRedisMatch({
            'curRoundRooms_notBalance': self.joinList(self.curRoundRooms_notBalance),
            'curRoundRooms_balance': self.joinList(self.curRoundRooms_balance),
            'curRoundNum': self.curRoundNum,
            'curRotation': self.curRotation,
            'curRotationRoundNum': self.curRotationRoundNum,
            'curUserIds': self.joinList(self.curUserIds, isSorted=True),
            'curPlayerNum': self.curPlayerNum,
            'matchState': self.matchState,
            'BalanceDatas': json.dumps(self.BalanceDatas),
        })

    def saveRedisMatch(self, datas):
        redis = self.getRedis()
        redis.hmset(self.Match_matchNumber_Key, datas)
        redis.expire(self.Match_matchNumber_Key, 60 * 60 * 6)

    def redis_save_userEnrollInfo(self, **enrollInfo):
        redis = self.getRedis()
        for uid in self.userIds:
            Match_UserEnroll_Key = Key_Match_UserEnroll % uid
            userEnroll = redis.hgetall(Match_UserEnroll_Key)
            if userEnroll.get('matchNumber', None) == self.matchNumber:
                redis.hmset(Match_UserEnroll_Key, enrollInfo)

    def redis_delete_userEnrollInfo(self, userIds, msg=u''):
        if isinstance(userIds, (int, str)):
            userIds = [userIds]
        redis = self.getRedis()
        for uid in userIds:
            Match_UserEnroll_Key = Key_Match_UserEnroll % uid
            userEnroll = redis.hgetall(Match_UserEnroll_Key)
            if userEnroll.get('matchNumber', None) == self.matchNumber:
                redis.delete(Match_UserEnroll_Key)
                self.logger(u'[redis_delete_userEnrollInfo] [%s] 清理报名信息[%s]' % (msg, uid))

    def readyStart(self):
        self.logger(u'[readyStart]  已设置开始倒计时时间')
        self.redis_save_match()
        self.redis_save_userEnrollInfo(matchNumber=self.matchNumber)
        self.setMatchState(MatchOperate.State_ReadyStart)
        self.matchStart()

    def matchStart(self):
        self.nextRound(self.userIds, nextRotation=True)

    def saveDatas(self, game):
        self.BalanceDatas.setdefault(self.curRoundNum, {})
        if isMahjong:
            datas = game.mahjong_getSaveDatas()
        else:
            datas = game.poker_getSaveDatas()
        self.BalanceDatas[self.curRoundNum][game.gameNumber] = datas
        self.logger(u'[MatchMgr-saveDatas] %s' % (pformat(self.BalanceDatas)))
        self.setCurAttrToRedis()

    def gameBalanceing(self, game, isDrawn):
        try:
            try:
                self.curRoundRooms_notBalance.remove(game.roomId)
                self.curRoundRooms_balance.append(game.roomId)
                self.sendAllcurRoundRoomDatas()
            except:
                traceback.print_exc()

            for _player in game.getPlayers():
                userRecordMgr = self.getUserRecordMgr(_player.uid)
                userRecordMgr.saveRoundRecord(game, _player, isDrawn)

            self.matchRecordMgr.sortAndUpdateRank()
            # 推送到除当前所有比赛,比赛的排名信息
            resp = self.getMatchRanks()
            self.sendAllGamePlayers(resp=resp, excludeGames=(game,))
            # 推送到除当前所有比赛,比赛和房间的排名信息
            game.getRoomRanks(resp=resp)
            game.sendAll(resp)

            self.logger(u'[gameBalanceing] S_C_RankInfo => %s' % (resp))
            self.saveDatas(game)
        except:
            traceback.print_exc()

    def gameAfterBalance(self, game):
        self.logger(u'[gameAfterBalance]  房间[%s] 已经结算完毕' % (game.roomId))
        isAllEnding = True
        for _game in self.getCurRoundGame().itervalues():
            if not _game.isEnding:
                isAllEnding = False
                break
        if isAllEnding:
            self.logger(u'[gameAfterBalance]  全部房间已结算完毕')
            obj_timer = self.timerMgr.getTimer(callback=self.waitNextRound, overTime=5 * 1000,
                                               note=u'设置赛事下轮赛事倒计时时间')
            self.timerMgr.add_Timer(obj_timer, 0)
        return isAllEnding

    def getCurRoundRoomDatas(self):
        resp = match_pb2.S_C_curRoundRoomDatas()
        resp.totalCount = len(self.curRoundRooms)
        resp.notBalanceCount = len(self.curRoundRooms_notBalance)
        resp.balanceCount = len(self.curRoundRooms_balance)
        return resp

    def sendAllcurRoundRoomDatas(self, excludeGames=()):
        resp = self.getCurRoundRoomDatas()
        self.sendAllGamePlayers(resp=resp, excludeGames=excludeGames)

    def getRotationDatas(self):
        resp = match_pb2.S_C_RotationDatas()
        curRotation = 0
        lastPlayerNum = self.maxPlayerNum
        lastRoundNum = 0
        for roundNum, playerNum in zip(self.roundNums, self.roundPlayers):
            curRotation += 1

            respDatas = resp.RotationDatas.add()
            respDatas.rotation = curRotation
            respDatas.type = 0
            respDatas.totalPlayerNum = lastPlayerNum
            respDatas.targetPlayerNum = playerNum
            respDatas.targetRound = roundNum - lastRoundNum

            lastPlayerNum = playerNum
            lastRoundNum = roundNum

        resp.RotationDatas[-1].type = 1
        return resp

    def waitNextRound(self):
        self.logger(u'[waitNextRound]')

        obj_timer = self.timerMgr.getTimer(callback=self.removeCurRoundGame, overTime=10 * 1000,
                                           note=u'设置赛事下轮赛事开始倒计时时间')
        self.timerMgr.add_Timer(obj_timer, 0)

    def sendNotice(self, txt, isSendAll=False):
        noticeProto = baseProto_pb2.S_C_Notice()
        noticeProto.repeatTimes = 2
        noticeProto.repeatInterval = 0
        noticeProto.id = 0
        noticeProto.txt = txt
        if isSendAll:
            self.sendAllGamePlayers(resp=noticeProto)
        return noticeProto

    def getCurRoundGame(self):
        if self.curRoundNum not in self.roundGameMap:
            return {}
        return self.roundGameMap[self.curRoundNum]

    def joinUsersByUid(self, uidsList):
        for uid in uidsList:
            if uid not in self.userIds:
                self.userIds.append(uid)
                self.matchRecordMgr.addUserRecored(uid=uid)
            else:
                self.logger(u'[joinUsersByUid]  uid[%s]重复添加' % uid)

    def getUserRecordMgr(self, uid):
        uid = int(uid)
        if uid in self.matchRecordMgr.usersRecordsMap:
            return self.matchRecordMgr.usersRecordsMap[uid]
        # if uid in self.matchRecordMgr.usersRecordsMap_old:
        return self.matchRecordMgr.usersRecordsMap_old[uid]

    def removeCurRoundGame(self):
        matchIsEnd = False
        if self.curRoundNum >= self.maxRoundNum:
            matchIsEnd = True
        if not matchIsEnd:
            isEliminate = False
            loserUids = []
            if self.curRoundNum in self.roundNums:
                playerNums = self.roundPlayers[self.roundNums.index(self.curRoundNum)]
                playerIds_Old = self.matchRecordMgr.usersRecordsMap.keys()
                loserUids = self.matchRecordMgr.eliminate(playerNums)
                winnerUids = self.matchRecordMgr.usersRecordsMap.keys()
                self.logger(u'[removeCurRoundGame] playerIds_Old => %s' % (playerIds_Old))
                self.logger(u'[removeCurRoundGame] loserUids => %s' % (loserUids))
                self.logger(u'[removeCurRoundGame] winnerUids => %s' % (winnerUids))
                isEliminate = True
            else:
                winnerUids = self.curUserIds

            for _game in self.getCurRoundGame().itervalues():
                for _player in _game.getPlayers():
                    userRecordMgr = self.getUserRecordMgr(_player.uid)
                    B_resp = match_pb2.S_C_RoundBalance()

                    if isEliminate:
                        if userRecordMgr.__isLose__():
                            B_resp.balanceType = enum_balanceType.eliminate
                            B_resp.balanceRank = userRecordMgr.rank
                        else:
                            B_resp.balanceType = enum_balanceType.rise
                    else:
                        B_resp.balanceType = enum_balanceType.wait
                    _game.sendOne(_player, B_resp)

                self.allPlayersExitAndRemoveGame(game=_game, isEliminate=isEliminate)
            if loserUids:
                self.redis_delete_userEnrollInfo(loserUids, msg=u'[被淘汰]')

            self.nextRound(playerIds=winnerUids, nextRotation=isEliminate)
        else:
            self.setMatchState(MatchOperate.State_Balance)

            resp = self.getMatchRanks()
            self.sendAllGamePlayers(resp=resp)

            for _rank, _rewardData in self.rewardMgr.items():
                try:
                    userRecordMgr = self.matchRecordMgr.getUserRecordByRank(_rank)
                    assert userRecordMgr.rank == _rank
                    currency_type = _rewardData['currency_type']
                    currency_count = _rewardData['currency_count']
                    userRecordMgr.setReward(rewardId=currency_type, rewardNum=currency_count)
                    self.server.send_mail(**dict(
                        uids_list=userRecordMgr.uid,
                        title=u'比赛场获奖领取通知',
                        body=u'恭喜您在%s（%s）中获得了第%s名获得%s×%s。请尽快领取\n%s' %
                             (self.title, self.matchDate, _rank, Define_Currency.getCurrencyChinese(currency_type),
                              currency_count, self.matchNumber),
                        enclosure_id=currency_type,
                        enclosure_num=currency_count,
                        emailType=Email_Type.matchAward,
                    ))
                    self.total_award_num += currency_count
                except:
                    traceback.print_exc()

            for _game in self.getCurRoundGame().itervalues():
                for _player in _game.getPlayers():
                    userRecordMgr = self.getUserRecordMgr(_player.uid)
                    B_resp = match_pb2.S_C_RoundBalance()
                    B_resp.balanceType = enum_balanceType.rank
                    B_resp.balanceRank = userRecordMgr.rank
                    B_resp.rewardId = userRecordMgr.reward[0]
                    B_resp.rewardNum = userRecordMgr.reward[1]
                    _game.sendOne(_player, B_resp)

            for _game in self.getCurRoundGame().itervalues():
                self.allPlayersExitAndRemoveGame(game=_game, isDrop=True)
            self.sendNotice(txt=u'当前赛事已结束,查看积分榜后可自行离开', isSendAll=True)
            self.logger(u'[removeCurRoundGame]  比赛完美结束')
            self.setMatchState(MatchOperate.State_Ending)
            self.matchEnding(commit=True)

    def allPlayersExitAndRemoveGame(self, game, isDrop=False, msg_resp=None, isEliminate=False):
        if game.roomId not in self.server.globalCtrl.num2game:
            return
        redis = self.getRedis()
        resp = baseProto_pb2.S_C_ExitRoomResult()
        resp.result = True
        for player in game.getPlayers():
            side = player.chair
            game.players[side] = None
            game.playerCount -= 1
            # 该情况下不记录重连信息，无法重连
            self.server.tryRmExitPlayerData(player, game)
            player.chair = consts.SIDE_UNKNOWN
            player.game = None
            self.server.userDBOnExitGame(player, game, isDrop=isDrop)
            if isDrop:
                game.sendOne(player, resp)
            if msg_resp:
                game.sendOne(player, msg_resp)

        game.removeRoom()

    def nextRound(self, playerIds, nextRotation=False):
        if len(playerIds) % self.maxPlayerCount != 0:
            self.logger(u'[createGroupRooom]  分配完毕')
            return
        self.setCurUserIds(playerIds)
        if nextRotation:
            self.curRotation += 1
            self.curRotationRoundNum = 0
        self.curRoundNum += 1
        self.curRotationRoundNum += 1
        self.curRoundRooms = []
        self.curRoundRooms_balance = []
        self.curRoundRooms_notBalance = []
        self.createGroupRooom(playerIds)
        self.setCurAttrToRedis()

    def createGroupRooom(self, playerIds):
        userIds = copy.deepcopy(playerIds)
        random.shuffle(userIds)

        describe = u'第%s轮次比赛' % (self.curRoundNum)
        if self.curRoundNum in self.roundNums:
            if self.curRoundNum == self.roundNums[-1]:
                describe = u'最终赛事'
            else:
                playerNums = self.roundPlayers[self.roundNums.index(self.curRoundNum)]
                describe = u'%s强晋级淘汰赛' % (playerNums)

        redis = self.getRedis()
        while userIds:
            _game = self.server.oncreateNewMatchRoom(curRoundNum=self.curRoundNum, matchMgr=self, describe=describe)
            _roomId = _game.roomId
            _needRefreshPlayers_ = []

            self.gameIdMap[_roomId] = _game
            self.curRoundRooms.append(_roomId)
            self.curRoundRooms_notBalance.append(_roomId)
            self.roundGameMap.setdefault(self.curRoundNum, {})
            self.roundGameMap[self.curRoundNum][_roomId] = self.gameIdMap[_game.roomId]

            curUserIds = userIds[:self.maxPlayerCount]
            del userIds[:self.maxPlayerCount]
            for uid in curUserIds:
                _needRefreshPlayer_ = self.server.createNewPlayerInGame(game=_game, uid=uid, matchMgr=self)
                if _needRefreshPlayer_:
                    _needRefreshPlayers_.append(_needRefreshPlayer_)

                redis.hset(Key_Match_PlayingUser, uid, _game.gameNumber)

            resp = match_pb2.S_C_Need_To_Refresh()
            resp.refreshType = 2
            for _needRefreshPlayer_ in _needRefreshPlayers_:
                self.server.sendOne(_needRefreshPlayer_, resp)

        self.logger(u'[createGroupRooom]  分配完毕')
        if self.curRoundNum == 1:
            overTime = 20 * 1000
            self.saveRedisMatch({'FirstGameStartTimeStamp': int(time.time() * 1000 + overTime)})
        else:
            overTime = 20 * 1000
        obj_timer = self.timerMgr.getTimer(callback=self.roundAllStart, overTime=overTime,
                                           note=u'设置全部房间开始倒计时')
        self.timerMgr.add_Timer(obj_timer, 0)

    def roundAllStart(self):
        if self.checkMatchState(MatchOperate.State_ReadyStart):
            self.setMatchState(MatchOperate.State_Matching)
        self.logger(u'[roundAllStart]  全部房间开始')
        for _game in self.getCurRoundGame().itervalues():
            _game.onGameStart(_game.players[0])

    def getTimerNum(self):
        return self.matchNumber

    def dismiss(self, reason=u''):
        '''解散当前比赛'''
        self.logger(u'[dismiss] reason[%s]' % reason)
        if self.checkMatchState(MatchOperate.State_Ending):
            self.logger(u'[dismiss] 比赛已完美结束')
            return
        if self.checkMatchState(MatchOperate.State_Dismissing):
            self.logger(u'[dismiss] 比赛正在解散中')
            return
        if self.checkMatchState(MatchOperate.State_Have_Dismiss):
            self.logger(u'[dismiss] 比赛已解散')
            return

        self.dismissStartTime = int(time.time() * 1000)
        self.dismissReason = reason

        try:
            if reason:
                self.sendNotice(txt=u'当前比赛即将中断取消，取消原因:%s。' % reason, isSendAll=True)
            else:
                self.sendNotice(txt=u'当前比赛即将中断取消，取消原因请稍后留意公告。', isSendAll=True)
        except:
            traceback.print_exc()

        self.logger(u'[dismiss] 已设置解散比赛倒计时时间')
        obj_timer = self.timerMgr.getTimer(callback=self.dismissTimeOut, overTime=15 * 1000, note=u'设置解散比赛倒计时时间')
        self.timerMgr.add_Timer(obj_timer, 0)
        self.setMatchState(MatchOperate.State_Dismissing)

    def dismissTimeOut(self):
        if not self.checkMatchState(MatchOperate.State_Dismissing):
            return
        for _game in self.getCurRoundGame().itervalues():
            try:
                _game.endGame()
            except:
                traceback.print_exc()
        self.logger(u'[dismissTimeOut] 比赛已经解散')
        self.setMatchState(MatchOperate.State_Have_Dismiss)
        self.matchEnding()

    def getMatchRanks(self, resp=None):
        if not resp:
            resp = match_pb2.S_C_RankInfo()

        for userRecordMgr in self.matchRecordMgr.curRecordRank:
            matchRankResp = resp.matchRanks.add()
            matchRankResp.side = -1
            matchRankResp.uid = userRecordMgr.uid
            matchRankResp.nickname = userRecordMgr.nickname
            matchRankResp.headImgUrl = userRecordMgr.headImgUrl
            matchRankResp.rank = userRecordMgr.rank
            matchRankResp.integralTotal = userRecordMgr.integralTotal
            matchRankResp.integralHistory.extend(userRecordMgr.integralHistory)
        return resp

    def sendAllGamePlayers(self, resp, excludeGames=()):
        for _game in self.getCurRoundGame().itervalues():
            if _game in excludeGames:
                continue
            _game.sendAll(resp)

    def matchEnding(self, commit=False):
        '''
        赛事结束
        :param commit:是否正常结束
        :return:
        '''
        self.matchEndTime = int(time.time() * 1000)
        try:
            self.sql_save_match_recode_end()
            self.sql_save_match_player()
        except:
            traceback.print_exc()
        try:
            if not commit:
                self.server.matchFailReturnFee(**dict(
                    userIds=self.userIds,
                    matchNumber=self.matchNumber,
                    feeType=self.feeType,
                    fee=self.fee,
                    dismissReason=self.dismissReason
                ))
            self.redis_delete_userEnrollInfo(self.userIds, msg=u'matchEnding调用')
        except:
            traceback.print_exc()
        try:
            redis = self.getRedis()
            pipe = redis.pipeline()
            pipe.srem(self.Match_Gaming_matchNumber_Key, self.Match_matchNumber_Key)
            pipe.sadd(self.Match_EndBalance_matchNumber_Key, self.Match_matchNumber_Key)
            pipe.execute()
        except:
            traceback.print_exc()

        if self.matchNumber in self.server.matchMgrMap:
            del self.server.matchMgrMap[self.matchNumber]
        self.logger(u'[matchEnding]  比赛已解散,移除')

    def sql_save_match_recode_start(self):
        saveData = {
            'game_id': self.gameId,
            'match_id': self.matchId,
            'match_number': self.matchNumber,
            'user_ids': self.joinList(self.userIds, isSorted=True),
            'serviceTag': '%s:%s' % (self.server.ip, self.server.port),
            'fee_type': self.feeType,
            'total_fee': self.fee * self.maxPlayerNum,
            'total_num': self.maxPlayerNum,
            'match_Info': json.dumps(self.matchInfo),
            'start_time': self.matchInitTime / 1000,
        }

        sql_data = json.dumps({
            'tableName': Table_match_record,
            'method': SQL_Method.INSERT,
            'data': saveData,
        })

        if self.server.mysql_twisted.check_pool():
            saveData['create_time'] = int(time.time())
            sql, args = FormatSql_Insert(**dict(
                tableName=Table_match_record,
                datasDict=saveData,
            )).getSqlStrAndArgs()
            d = self.server.mysql_twisted.insert(sql, args)
            d.addErrback(self.sql_excute_fail, sql_data=sql_data)
        else:
            redis = self.getRedis()
            redis.rpush(Key_Match_Mysql_Jobs, sql_data)

    def sql_save_match_recode_end(self):
        saveData = {
            'match_number': self.matchNumber,
            'fee_type': self.feeType,
            'total_award_type': self.matchType,
            'total_award_num': self.total_award_num,
            'end_time': self.matchEndTime / 1000,
            'dismissReason': self.dismissReason,
            'matchState': self.matchState,
            'balance_datas': json.dumps(self.BalanceDatas),
        }

        sql_data = json.dumps({
            'tableName': Table_match_record,
            'method': SQL_Method.UPDATE,
            'data': saveData,
        })

        if self.server.mysql_twisted.check_pool():
            saveData['update_time'] = int(time.time())
            sql, args = FormatSql_Update(**dict(
                tableName=Table_match_record,
                datasDict=saveData,
                whereParams={
                    'data': {'match_number': self.matchNumber},
                },
            )).getSqlStrAndArgs()
            d = self.server.mysql_twisted.update(sql, args)
            d.addCallbacks(callback=self.sql_excute_update_suc, callbackKeywords={'sql_data': sql_data},
                           errback=self.sql_excute_fail, errbackKeywords={'sql_data': sql_data})
        else:
            redis = self.getRedis()
            redis.rpush(Key_Match_Mysql_Jobs, sql_data)

    def sql_excute_update_suc(self, rowcount, sql_data, *args, **kwargs):
        if not rowcount:
            self.logger(u'[sql_excute_update_suc] 更新0条数据,需要当作失败处理' % (sql_data))
            self.logger(u'[sql_excute_update_suc] sql_data => %s' % (sql_data))
            redis = self.getRedis()
            redis.rpush(Key_Match_Mysql_Jobs, sql_data)

    def sql_excute_fail(self, failure, sql_data, *args, **kwargs):
        self.logger(u'[sql_excute_fail] %s' % (failure.getErrorMessage()))
        self.logger(u'[sql_excute_fail] sql_data => %s' % (sql_data))
        redis = self.getRedis()
        redis.rpush(Key_Match_Mysql_Jobs, sql_data)

    def sql_save_match_player(self):
        baseData = {
            'tableName': Table_match_player,
            'method': SQL_Method.INSERT,
            'data': {
                'game_id': self.gameId,
                'match_id': self.matchId,
                'match_number': self.matchNumber,
                'fee_type': self.feeType,
                'fee': self.fee,
            },
        }

        useMysql = False
        if self.server.mysql_twisted.check_pool():
            useMysql = True

        for _uid, userRecordMgr in self.matchRecordMgr.itemAllRecords():
            data = baseData.copy()
            data['data'].update({
                'user_id': _uid,
                'score': userRecordMgr.integralTotal,
                'rank': userRecordMgr.rank,
                'reward_type': userRecordMgr.reward[0],
                'reward_fee': userRecordMgr.reward[1],
            })
            if useMysql:
                sql, args = FormatSql_Insert(**dict(
                    tableName=Table_match_player,
                    datasDict={
                        'game_id': self.gameId,
                        'match_id': self.matchId,
                        'match_number': self.matchNumber,
                        'fee_type': self.feeType,
                        'fee': self.fee,
                        'user_id': _uid,
                        'score': userRecordMgr.integralTotal,
                        'rank': userRecordMgr.rank,
                        'reward_type': userRecordMgr.reward[0],
                        'reward_fee': userRecordMgr.reward[1],
                        'create_time': int(time.time()),
                    },
                )).getSqlStrAndArgs()
                d = self.server.mysql_twisted.insert(sql, args)
                d.addErrback(self.sql_excute_fail, sql_data=json.dumps(data))
            else:
                redis = self.getRedis()
                redis.rpush(Key_Match_Mysql_Jobs, json.dumps(data))
