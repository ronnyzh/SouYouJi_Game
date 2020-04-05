# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: Player peer
"""

from handle import Handel
from common.card_define import *
from common.log import *

from publicCommon.public_player import PublicPlayer
from matchCommon.match_player import MatchPlayer

class Player(MatchPlayer):

    def resetPerGame(self):
        super(Player, self).resetPerGame()
        self.curGameScore = 0
        self.kongPlayers = []  # 杠牌对象，如果是-1则为暗杠
        self.huDescs = []
        self.ChowPongHis = {0: 0, 1: 0, 2: 0, 3: 0}

        self.lastAction = -1
        self.actionBefore = -1
        self.trueLastAction = -1
        self.isFreeze = False
        self.colorSet = None  # 定缺
        self.changingTiles = []
        self.ckScore = 0
        self.isSelfHU = False
        self.isOtherHu = False
        self.beenHuCount = 0

    def loadDB(self, playerTable, isInit=True, account=None):
        super(Player, self).loadDB(playerTable, isInit, account)
        self.nickname = self.nickname.decode('utf-8')

    def doAction(self, action, actionTiles):
        super(Player, self).doAction(action, actionTiles)
        if action == HU:
            return
        self.trueLastAction = action
        self.actionBefore = self.lastAction
        self.lastAction = action

    def getBalanceDescs(self):
        return self.huDescs

    def getHandleMgr(self):  # 玩家手牌管理器
        return Handel(self)

    def getHuData(self):
        side, _, _ = self.handleMgr.getHuData()
        if side < 0:
            return None, None
        player = self.game.players[side]
        name, rate = self.handleMgr.checkRate()
        self.huDescs.extend(name)
        # if player == self and self.trueLastAction == OTHERS_KONG:
        if player == self and self.trueLastAction in [OTHERS_KONG, SELF_KONG, CONCEALED_KONG]:
            '''杠上开花'''
            rate += 1
            if self.game.bt2 == 0 and self.trueLastAction == OTHERS_KONG:
                '''算点炮'''
                self.isOtherHu = True
                desc = '接炮'.decode('utf-8')
                self.huDescs.append(desc)
                side = self.handleMgr.othersKongTiles[-1][0]
                player = self.game.players[side]
                self.handleMgr.huData[0] = side
                player.beenHuCount += 1
                desc = '放炮'.decode('utf-8')
                player.huDescs.append(desc)
            else:
                '''算自摸'''
                self.isSelfHU = True
            desc = '杠上开花'.decode('utf-8')
            self.huDescs.append(desc)
            '''扫底'''
            if self.handleMgr.isHaiDi():
                desc = '扫底胡'.decode('utf-8')
                self.huDescs.append(desc)
                rate += 1
        elif player == self:
            '''自摸'''
            desc = '自摸'.decode('utf-8')
            self.huDescs.append(desc)
            self.isSelfHU = True
            '''天胡'''
            if self.game.tdHU and player == self.game.dealer and not self.handleMgr.isDiscard:
                desc = '天胡'.decode('utf-8')
                self.huDescs.append(desc)
                rate += 3
            '''自摸加番'''
            if self.game.bt == 1:
                rate += 1
            '''扫底'''
            if self.handleMgr.isHaiDi():
                desc = '扫底胡'.decode('utf-8')
                self.huDescs.append(desc)
                rate += 1
        else:
            '''抢杠/点炮'''
            self.isOtherHu = True
            player.beenHuCount += 1
            desc = '放炮'.decode('utf-8')
            player.huDescs.append(desc)
            '''地胡'''
            if self.game.tdHU and player == self.game.dealer:
                flag = [i for i in self.game.getPlayers((player,)) if i.handleMgr.isDiscard]
                if not flag:
                    rate += 5
                    desc = '地胡'.decode('utf-8')
                    self.huDescs.append(desc)
            if player == self.game.beGrabKongHuPlayer:
                '''抢杠'''
                rate += 1
                desc = '抢杠胡'.decode('utf-8')
                self.huDescs.append(desc)
            elif player.trueLastAction == OTHERS_KONG or player.trueLastAction == CONCEALED_KONG \
                    or player.trueLastAction == SELF_KONG:
                rate += 1
                desc = '杠上炮'.decode('utf-8')
                self.huDescs.append(desc)
            else:
                desc = '接炮'.decode('utf-8')
                self.huDescs.append(desc)
            '''海底炮'''
            if self.handleMgr.isHaiDi():
                desc = '海底炮'.decode('utf-8')
                self.huDescs.append(desc)
                rate += 1
        self.logger(u'[getHuData] huDescs[%s] rate[%s] fans[%s]' % (','.join(self.huDescs), rate, self.game.fans))
        rate = self.game.fans if rate > self.game.fans else rate
        return player, rate

    def upTotalUserData(self):
        self.totalKongCount += len(self.handleMgr.getKongTiles())
        self.totalConcealedKongCount += len(self.handleMgr.getConcealedKongTiles())
        self.totalBeKongCount += len(self.handleMgr.getBeKongTiles())
        huSide = self.handleMgr.getHuData()[0]
        if huSide >= 0:
            if huSide == self.chair:
                self.totalSelfHuCount += 1
            else:
                self.totalOtherHuCount += 1
                self.game.players[huSide].totalGiveHuCount += 1

    def packTotalBalanceDatas(self):
        totalBalanceDatas = []
        data = '自摸次数:%s' % (self.totalSelfHuCount)
        data = data.decode('utf-8')
        totalBalanceDatas.append(data)
        data = '胡牌次数:%s' % (self.totalSelfHuCount + self.totalOtherHuCount)
        data = data.decode('utf-8')
        totalBalanceDatas.append(data)
        data = '明杠次数:%s' % (self.totalKongCount)
        data = data.decode('utf-8')
        totalBalanceDatas.append(data)
        data = '暗杠次数:%s' % (self.totalConcealedKongCount)
        data = data.decode('utf-8')
        totalBalanceDatas.append(data)

        return totalBalanceDatas

    def getMyColorSetTiles(self):
        return [_tile for _tile in self.handleMgr.tiles if getTileType(_tile) == self.colorSet]
