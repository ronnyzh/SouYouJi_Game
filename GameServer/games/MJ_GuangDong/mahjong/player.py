# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: Player peer
"""

from handle import Handel
from common.common_player import CommonPlayer
from publicCommon.public_player import PublicPlayer


class Player(PublicPlayer):
    def __init__(self):
        super(Player, self).__init__()
        # 结算相关数据
        self.totalHuCount = 0

    def resetPerGame(self):
        super(Player, self).resetPerGame()
        self.WinHorse = []
        self.huDescs = []

    def getBalanceDescs(self):
        return self.huDescs

    def getHandleMgr(self):  # 玩家手牌管理器
        return Handel(self)

    def getHuData(self):
        side, _, _ = self.handleMgr.getHuData()
        player = self.game.players[side]
        return player

    def upTotalUserData(self):
        self.totalGameScore += self.curGameScore  # 分数
        self.totalKongCount += len(self.handleMgr.getKongTiles())  # 明杠
        self.totalConcealedKongCount += len(self.handleMgr.getConcealedKongTiles())  # 暗杠
        huSide = self.handleMgr.getHuData()[0]
        if huSide >= 0:
            self.totalHuCount += 1
            if huSide == self.chair:
                self.totalSelfHuCount += 1  # 自摸
            else:
                self.totalOtherHuCount += 1  # 吃炮
                self.game.players[huSide].totalGiveHuCount += 1  # 点炮

    def packTotalBalanceDatas(self):
        totalBalanceDatas = []
        data = '自摸次数:%s' % (self.totalSelfHuCount)
        data = data.decode('utf-8')
        totalBalanceDatas.append(data)
        data = '胡牌次数:%s' % (self.totalHuCount)
        data = data.decode('utf-8')
        totalBalanceDatas.append(data)
        data = '点炮次数:%s' % (self.totalGiveHuCount)
        data = data.decode('utf-8')
        totalBalanceDatas.append(data)
        data = '明杠次数:%s' % (self.totalKongCount)
        data = data.decode('utf-8')
        totalBalanceDatas.append(data)
        data = '暗杠次数:%s' % (self.totalConcealedKongCount)
        data = data.decode('utf-8')
        totalBalanceDatas.append(data)
        return totalBalanceDatas
