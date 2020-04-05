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
from common.card_define import *
from common.log import *
import hainan_mahjong_pb2
from publicCommon.public_player import PublicPlayer

class Player(PublicPlayer):
    def __init__(self):
        super(Player, self).__init__()
        self.gaHisList = []
        # 总结算数据
        self.totalGameScore = 0
        self.totalKongCount = 0
        self.totalConcealedKongCount = 0
        self.totalHuCount = 0
        self.totalSelfHuCount = 0

    def __str__(self):
        return '(%s curScore[%s])' % (self.account, self.curGameScore)

    def resetPerGame(self):
        super(Player, self).resetPerGame()
        self.flower4HuFlag = False
        # self.flower8HuFlag = None
        self.flowerSet = []
        self.flowerHuRate = 0
        self.curGameScore = 0
        # 是否为庄
        self.isDealer = False
        # 连庄次数
        self.dealerCount = 0
        # 杠牌对象，如果是-1则为暗杠
        self.kongPlayers = []
        # 是否被包杠
        self.isKeptKong = False
        # 是否被包胡
        self.isKeptDiscard = False
        # 被包胡玩家
        self.keptHuPlayer = None
        # 是否包牌标志
        self.isWrapTile = False
        # 首张被跟
        self.beFollowFirstTile = False
        self.huDescs = []
        self.ChowPongHis = {0: 0, 1: 0, 2: 0, 3: 0}
        self.beChowPongHis = {0: 0, 1: 0, 2: 0, 3: 0}
        self.ga = -1
        self.lastSelfOp = -1
        self.isGrabKongHu = False
        self.threeTiles = []
        self.fourTiles = []

    def getBalanceDescs(self):
        descs = []
        if self.ga > 0:
            desc = '%s噶' % (self.ga)
            desc = desc.decode('utf-8')
            descs.append(desc)
        else:
            desc = '无噶'
            desc = desc.decode('utf-8')
            descs.append(desc)
        if self.flowerHuRate:
            desc = '花胡x%s' % (self.flowerHuRate)
            desc = desc.decode('utf-8')
            descs.append(desc)
        if self.kongPlayers:
            cancealKongCount = self.kongPlayers.count(-1)
            if cancealKongCount:
                desc = '暗杠x%s' % (cancealKongCount)
                desc = desc.decode('utf-8')
                descs.append(desc)
            kongCount = len(self.kongPlayers) - cancealKongCount
            if kongCount:
                desc = '明杠x%s' % (kongCount)
                desc = desc.decode('utf-8')
                descs.append(desc)
        bekongCount = len(self.handleMgr.getBeKongTiles())
        if bekongCount:
            desc = '放杠x%s' % (bekongCount)
            desc = desc.decode('utf-8')
            descs.append(desc)
        if self.isKeptDiscard:
            otherDesc = '海底包牌 '.decode('utf-8')
            if otherDesc not in self.huDescs:
                desc = '出牌被包'
                desc = desc.decode('utf-8')
                descs.append(desc)
        if self.keptHuPlayer:
            desc = '包牌'
            desc = desc.decode('utf-8')
            descs.append(desc)
        if self.game.isDealerNidle and self.isDealer:
            desc = '庄闲'
            desc = desc.decode('utf-8')
            descs.append(desc)
        if self.game.isContinueDealer and self.isDealer and self.dealerCount:
            desc = '连庄x%s' % (self.dealerCount)
            desc = desc.decode('utf-8')
            descs.append(desc)
        flowerCount = len(self.handleMgr.getFlowerTiles())
        if flowerCount > 0:
            desc = '补花x%s' % (flowerCount)
            desc = desc.decode('utf-8')
            descs.append(desc)
        descs.extend(self.huDescs)
        return descs

    def getHandleMgr(self):  # 玩家手牌管理器
        return Handel(self)

    def doAction(self, action, actionTiles):
        super(Player, self).doAction(action, actionTiles)
        log(u'[try player do action]action[%s] actionTiles[%s]' % (action, actionTiles), LOG_LEVEL_RELEASE)

        if action == HU:
            side, _, _ = self.handleMgr.getHuData()
            for _side, times in self.ChowPongHis.items():
                if times == 3 and side == _side:
                    self.threeTiles.append(_side)
                    self.game.dealSurroundData(_side)
                if times == 4 and (side == _side or side == self.chair):
                    self.fourTiles.append(_side)
                    self.game.dealSurroundData(_side)

            for _side, times in self.beChowPongHis.items():
                if times == 3 and side == _side:
                    self.threeTiles.append(_side)
                    self.game.dealSurroundData(_side)
                if times == 4 and (side == _side or side == self.chair):
                    self.fourTiles.append(_side)
                    self.game.dealSurroundData(_side)

        if action == OTHERS_KONG and (self.handleMgr.tmpSide == self.game.dealer.chair) \
                and (self.game.isFirstTile):
            # 是否被包杠
            self.isKeptKong = True
            resp = hainan_mahjong_pb2.S_C_Be_Kong()
            resp.side = self.game.dealer.chair
            self.game.sendAll(resp)

        if action == CONCEALED_KONG:
            log(u'[try player do action]CONCEALED_KONG', LOG_LEVEL_RELEASE)
            self.kongPlayers.append(-1)
            self.lastSelfOp = CONCEALED_KONG

        elif action in [OTHERS_KONG, SELF_KONG]:
            log(u'[try player do action]OTHERS_KONG or SELF_KONG', LOG_LEVEL_RELEASE)
            self.lastSelfOp = action
            if self.handleMgr.lastTile:
                log(u'[try player do action]SELF_KONG', LOG_LEVEL_RELEASE)
                self.kongPlayers.append(self.chair)
            else:
                log(u'[try player do action]OTHERS_KONG', LOG_LEVEL_RELEASE)
                self.kongPlayers.append(self.handleMgr.tmpSide)

        if action in [CHOW, PONG]:
            # 如果玩家碰吃需要记录是否三道,四道牌
            chair, data = self.handleMgr.action2balanceTiels[action][-1].split(";")
            chair = int(chair)
            self.ChowPongHis[chair] += 1
            bePlayer = self.game.players[chair]
            bePlayer.beChowPongHis[self.chair] += 1
            for side, time in self.ChowPongHis.items():
                print "[side,time]:", side, time, self.ChowPongHis
                if int(time) >= 3:
                    log(u'[try sendHandleTiles] side[%s] beSide[%s] time[%s]' % (side, self.chair, time),
                        LOG_LEVEL_RELEASE)
                    resp = hainan_mahjong_pb2.S_C_Be_Handle_Tiles()
                    resp.nums = int(time)
                    resp.discardSide = side
                    resp.actionSide = self.chair
                    self.game.sendAll(resp)

    def getHuData(self):
        if self.beFollowFirstTile:
            desc = '首张被跟'.decode('utf-8')
            self.huDescs.append(desc)
        if self.isKeptKong:
            desc = '首张被杠'.decode('utf-8')
            self.game.dealer.huDescs.append(desc)

        side, _, _ = self.handleMgr.getHuData()
        if side < 0:
            return None, None
        player = self.game.players[side]
        huRate = 1
        log(u'[getHuData] side[%s] selfChair[%s] beFollowFirstTile[%s] isKeptKong[%s] isGrabKongHu[%s] account[%s]' % (
        side, self.chair, self.beFollowFirstTile, self.isKeptKong, self.isGrabKongHu, self.account), LOG_LEVEL_RELEASE)
        if player == self:
            if not self.handleMgr.isDiscard:
                huRate *= 3
                if player is self.game.dealer:
                    desc = '天胡'.decode('utf-8')
                    self.huDescs.append(desc)
                else:
                    desc = '地胡'.decode('utf-8')
                    self.huDescs.append(desc)
            else:
                if self.lastSelfOp in [OTHERS_KONG, SELF_KONG, CONCEALED_KONG]:
                    huRate *= 3
                    desc = "杠上开花".decode('utf-8')
                elif self.lastSelfOp == 10:
                    huRate *= 3
                    desc = "花上开花".decode('utf-8')
                else:
                    huRate *= 2
                    desc = '自摸'.decode('utf-8')
                self.huDescs.append(desc)
        else:
            if self.isGrabKongHu:
                desc = '抢杠胡'.decode('utf-8')
                self.huDescs.append(desc)
            else:
                desc = '接炮'.decode('utf-8')
                self.huDescs.append(desc)
            otherDesc = '点炮'.decode('utf-8')
            player.huDescs.append(otherDesc)
            if player.game.beginWrap and player.game.isPackAll:
                otherDesc = '海底包牌 '.decode('utf-8')
                player.isKeptDiscard = True
                player.huDescs.append(otherDesc)
        if self.handleMgr.isThirteenOrphans():
            huRate *= 13
            desc = '十三幺'.decode('utf-8')
            self.huDescs.append(desc)
        else:
            if self.handleMgr.isSuperSevenPair():
                huRate *= 3
                desc = '豪华七对'.decode('utf-8')
                self.huDescs.append(desc)
            elif self.handleMgr.isSevenPair():
                huRate *= 2
                desc = '七小对'.decode('utf-8')
                self.huDescs.append(desc)
            elif self.handleMgr.isAllPong():
                huRate *= 2
                desc = '碰碰胡'.decode('utf-8')
                self.huDescs.append(desc)
            else:
                desc = '平胡'.decode('utf-8')
                self.huDescs.append(desc)
            if self.handleMgr.isOneColour():
                huRate *= 2
                desc = '清一色'.decode('utf-8')
                self.huDescs.append(desc)
            if self.threeTiles:
                otherDesc = '三道包牌'.decode('utf-8')
                wrapPlayer = self.game.players[self.threeTiles[0]]
                wrapPlayer.huDescs.append(otherDesc)
            if self.fourTiles:
                otherDesc = '四道包牌'.decode('utf-8')
                for side in self.fourTiles:
                    wrapPlayer = self.game.players[side]
                    wrapPlayer.huDescs.append(otherDesc)
        log(u'[player get HuData]account[%s] huDescs[%s] huRate[%s]' % (self.account, self.huDescs, huRate),
            LOG_LEVEL_RELEASE)
        return player, huRate

    def upTotalUserData(self):
        log(u'[up total user data]account[%s] totalGameScore[%s] curGameScore[%s]' \
            % (self.account, self.totalGameScore, self.curGameScore), LOG_LEVEL_RELEASE)
        self.totalGameScore += self.curGameScore
        self.totalKongCount += len(self.handleMgr.getKongTiles())
        self.totalConcealedKongCount += len(self.handleMgr.getConcealedKongTiles())
        huSide = self.handleMgr.getHuData()[0]
        if huSide >= 0:
            self.totalHuCount += 1
            if huSide == self.chair:
                self.totalSelfHuCount += 1

    def packTotalBalanceDatas(self):
        totalBalanceDatas = []
        data = '明杠次数:%s' % (self.totalKongCount)
        data = data.decode('utf-8')
        totalBalanceDatas.append(data)
        data = '暗杠次数:%s' % (self.totalConcealedKongCount)
        data = data.decode('utf-8')
        totalBalanceDatas.append(data)
        data = '胡牌次数:%s' % (self.totalHuCount)
        data = data.decode('utf-8')
        totalBalanceDatas.append(data)
        data = '自摸次数:%s' % (self.totalSelfHuCount)
        data = data.decode('utf-8')
        totalBalanceDatas.append(data)
        return totalBalanceDatas
