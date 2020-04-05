# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: Player peer
"""

from common.common_player import CommonPlayer
from handle import Handel
from publicCommon.public_player import PublicPlayer
from matchCommon.match_player import MatchPlayer


class Player(MatchPlayer):
    def __init__(self):
        super(Player, self).__init__()
        # 结算相关数据
        self.resetPerGame()
        self.totalBombCount = 0
        self.gameScores = []
        self.callLandlordCount = 0

    def __str__(self):
        return '(%s curScore[%s])' % (self.account, self.curGameScore)

    def resetPerGame(self):
        super(Player, self).resetPerGame()
        # 是否为地主
        self.isLandlord = False
        # 是否明牌
        self.isOpenHand = False
        self.bombCount = 0
        self.isCalledLandlord = False
        self.callData = 0
        self.isRobedLandlord = False
        self.robData = 0
        self.isAutoDiscard = False
        self.mustBeLandlord = False
        self.needCallScore = 0

    def getBalanceDescs(self):
        descs = []

        # 剩余牌张数
        leftCards = self.handleMgr.getCards()
        _len = len(leftCards)
        desc = ('%s' % (_len)).decode('utf-8')
        descs.append(desc)

        # 炸弹个数
        desc = ('%s' % (self.bombCount)).decode('utf-8')
        descs.append(desc)

        return descs

    def getHandleMgr(self):  # 玩家手牌管理器
        return Handel(self)

    def upTotalUserData(self):
        self.gameScores.append(self.curGameScore)
        self.totalGameScore += self.curGameScore
        self.totalBombCount += self.bombCount
        if self.game.isGameEnd and \
                ((self.isLandlord and self.game.isLandlordWin) or \
                 not (self.isLandlord or self.game.isLandlordWin)):
            self.totalWinCount += 1

    def packTotalBalanceDatas(self):
        totalBalanceDatas = []
        data = ('单局最高:%s' % (max(self.gameScores))).decode('utf-8')
        # data = data.decode('utf-8')
        totalBalanceDatas.append(data)
        data = ('炸弹个数:%s' % (self.totalBombCount)).decode('utf-8')
        totalBalanceDatas.append(data)
        data = ('胜利局数:%s' % (self.totalWinCount)).decode('utf-8')
        totalBalanceDatas.append(data)
        return totalBalanceDatas
