# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/29
Revision: 1.0.0
Description: Description
"""
from common.common_db_define import *
import redis_instance


class MatchRecordMgr(object):
    def __init__(self, matchMgr, *args, **kwargs):
        self.matchMgr = matchMgr
        self.usersRecordsMap = {}
        self.usersRecordsMap_old = {}

        self.curRecordRank = []
        self.curRecordRank_old = []

    def itemAllRecords(self):
        '''迭代器'''
        for _uid, userRecordMgr in self.usersRecordsMap.iteritems():
            yield _uid, userRecordMgr
        for _uid, userRecordMgr in self.usersRecordsMap_old.iteritems():
            yield _uid, userRecordMgr

    def logger(self, *args, **kwargs):
        self.matchMgr.logger(*args, **kwargs)

    def getUserRecordByRank(self, rank):
        if rank <= len(self.curRecordRank):
            return self.curRecordRank[rank - 1]
        offsetRank = rank - len(self.curRecordRank)
        return self.curRecordRank_old[offsetRank - 1]

    def addUserRecored(self, uid):
        self.usersRecordsMap[uid] = UserRecordMgr(matchRecordMgr=self, uid=uid)
        self.curRecordRank.append(self.usersRecordsMap[uid])

    def sortAndUpdateRank(self):
        def sortFunc(a, b):
            '''
            如果第一个参数小于第二个参数，返回一个负数；
            如果第一个参数等于第二个参数，返回零；
            如果第一个参数大于第二个参数，返回一个正数
            '''
            # 积分越多,排序越前
            if a.integralTotal < b.integralTotal:
                return -1
            elif a.integralTotal > b.integralTotal:
                return 1
            # 结算时间越早,排序越前
            if a.lastBalanceTime < b.lastBalanceTime:
                return 1
            elif a.lastBalanceTime > b.lastBalanceTime:
                return -1
            # chair越小,排序越前
            if a.lastBalanceChair < b.lastBalanceChair:
                return 1
            elif a.lastBalanceTime > b.lastBalanceTime:
                return -1
            # uid越小,排序越前
            if a.uid < b.uid:
                return 1
            elif a.uid > b.uid:
                return -1
            else:
                assert False

        self.curRecordRank = sorted(self.curRecordRank, cmp=sortFunc, reverse=True)
        for index, usersRecords in enumerate(self.curRecordRank):
            usersRecords.rank = index + 1
            self.logger(u'[sortAndUpdateRank] %s' % (usersRecords))

    def eliminate(self, maxRank):
        losers = self.curRecordRank[maxRank:]
        loserUids = []
        self.curRecordRank_old = losers + self.curRecordRank_old
        self.curRecordRank = self.curRecordRank[:maxRank]
        for usersRecords in losers:
            usersRecords.setLose()
            self.usersRecordsMap_old[usersRecords.uid] = self.usersRecordsMap[usersRecords.uid]
            del self.usersRecordsMap[usersRecords.uid]
            loserUids.append(usersRecords.uid)
        return loserUids


class UserRecordMgr(object):
    def __init__(self, matchRecordMgr, uid, *args, **kwargs):
        self.matchRecordMgr = matchRecordMgr

        self.uid = uid
        self.integralTotal = 0  # 积分
        self.integralHistory = []  # 积分历史
        self.roundNumHistory = []  # 比赛轮次编号历史
        self.rank = 0  # 排名

        self.lastBalanceTime = 0
        self.lastBalanceChair = 0
        self.initData()

        self.lose = False
        self.reward = tuple([0, 0])  # 奖励

    def setLose(self):
        self.lose = True

    def __isLose__(self):
        return self.lose

    def initData(self):
        redis = redis_instance.getInst()
        self.userInfo = redis.hgetall(FORMAT_USER_TABLE % self.uid)

        self.account = self.userInfo['account'].decode('utf-8')
        self.nickname = self.userInfo['nickname'].decode('utf-8')
        self.headImgUrl = self.userInfo['headImgUrl']

    def __str__(self):
        return '{UserRecordMgr} [%s]  积分 %s=[%s] Chair[%s] Time[%s]' % \
               (self.uid, self.integralHistory, self.integralTotal, self.lastBalanceChair,
                self.lastBalanceTime)

    def saveRoundRecord(self, game, player, isDrawn):
        integral = player.curGameScore
        # if isDrawn:
        #     integral = -(game.maxPlayerCount - player.chair) * 1

        self.integralHistory.append(integral)
        self.integralTotal = sum(self.integralHistory)
        self.roundNumHistory.append(game.gameNumber)

        self.lastBalanceTime = game.setEndTime
        self.lastBalanceChair = player.chair

        self.logger(u'[saveRoundRecord] %s' % self.__str__())

    def logger(self, *args, **kwargs):
        self.matchRecordMgr.logger(*args, **kwargs)

    def setReward(self, rewardId, rewardNum):
        self.reward = tuple([rewardId, rewardNum])
