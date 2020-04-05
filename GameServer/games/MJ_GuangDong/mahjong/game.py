# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: game logic
"""

from common.common_game import CommonGame
from common.card_define import *
from common.log import *
from common.protocols.mahjong_consts import *
from common import mahjong_pb2
from player import Player
from deal import DealManager
import guangdong_mahjong_pb2
from common.consts import ERR_MSG
import copy
from common.pb_utils import *
import random
from publicCommon.public_game import PublicGame

import re


# class Game(CommonGame):
class Game(PublicGame):
    def __init__(self, server, ruleParams, needInit=True, roomId=0):
        self.gameplayers = 4
        super(Game, self).__init__(server, ruleParams, needInit=needInit, roomId=0)
        self.isSendReadyHand = True
        self.beforeHuSide = -1

    def resetSetData(self):
        '''每局数据初始化'''
        self.isTianDiHu = True
        # 记录action的玩家（多个同级响应时）[chair,chair] #add
        self.actionplayers = []
        self.WinHorseTiles = []
        self.HorseList = []
        self.isselfkong = False
        super(Game, self).resetSetData()

    def initByRuleParams(self, ruleParams):
        '''初始化房間參數'''
        params = eval(ruleParams)
        self.logger(u'[initByRuleParams] params is {}'.format(params))
        self.isCanChiHu = False  # 能否吃胡
        self.isHasGhost = None  # 是否有鬼
        self.HorseCount = 0  # 奖马数量
        self.buyhorse = False  # 买马
        self.gethorse = False  # 抓马
        self.isFollowHorse = False  # 马跟底分
        self.isHorseKong = False  # 马跟杠
        self.canBeKongHu = False  # 是否可抢杠胡
        self.isBaoKongHu = False  # 杠爆全包
        self.isBaoBeKongHu = False  # 抢杠全包
        self.isFanHu = 0  # 几番起胡
        self.HuTypeList = []  # 能胡牌的牌型
        self.HuScore = [1]  # 胡牌的翻数列表
        self.HorseFan = 0  # 马最高跟翻
        self.ghostzhong = False  # 鬼牌算位置

        self.huType_ThirteenOrphans = False
        self.huType_BigFourHu = False
        self.huType_SmallFourHu = False
        self.huType_BigThreeHu = False
        self.huType_SmallThreeHu = False
        self.huType_SuperSevenPairHu = False

        if params[0][0] == 0:
            self.ruleDescs.append("无鬼")
            if 0 in params[0][1]:
                self.huType_ThirteenOrphans = True
                self.ruleDescs.append("十三幺")
            if 1 in params[0][1]:
                self.huType_BigFourHu = True
                self.ruleDescs.append("大四喜")
            if 2 in params[0][1]:
                self.huType_SmallFourHu = True
                self.ruleDescs.append("小四喜")
            if 3 in params[0][1]:
                self.huType_BigThreeHu = True
                self.ruleDescs.append("大三元")
            if 4 in params[0][1]:
                self.huType_SmallThreeHu = True
                self.ruleDescs.append("小三元")
            if 5 in params[0][1]:
                self.huType_SuperSevenPairHu = True
                self.ruleDescs.append("豪华七对")

        elif params[0][0] == 1:
            self.isHasGhost = 'Random'
            self.ruleDescs.append("随机鬼")
        # 是否可吃胡
        self.isCanChiHu = False
        # 可抢杠胡
        self.canBeKongHu = True
        # 杠爆全包
        self.isBaoKongHu = True  # 杠爆全包
        # 抢杠全包
        self.isBaoBeKongHu = True  # 抢杠全包
        #############买马#############################
        self.buyhorse = True
        if params[1] == 1:
            self.HorseCount = 2
            self.ruleDescs.append("买2码")
        elif params[1] == 2:
            self.HorseCount = 4
            self.ruleDescs.append("买4码")
        elif params[1] == 3:
            self.HorseCount = 6
            self.ruleDescs.append("买6码")
        elif params[1] == 4:
            self.HorseCount = 8
            self.ruleDescs.append("买8码")
        else:
            self.buyhorse = False
            self.ruleDescs.append("不买码")

        self.logger(u'[initByRuleParams] ruleDescs is {}'.format(self.ruleDescs))
        super(Game, self).initByRuleParams(ruleParams)

    def onSetStart(self, player):
        """
        开始游戏（每小局开始）
        """
        if not self.checkStage(GAME_READY):
            return
        if player.chair != OWNNER_SIDE:
            log(u'[on set start][error]error chair[%s].' % (player.chair), LOG_LEVEL_RELEASE)
            return

        self.doBeforeSetStart()
        self.stage = WAIT_ROLL
        self.curGameCount += 1
        self.startLock = True

        resp = mahjong_pb2.S_C_SetStart()
        dicePoints = self.getDicePoint()

        if self.dealer:
            oldDealerSide = self.dealer.chair
        else:
            oldDealerSide = -1
        log(u'[on set start] oldDealerSide[%s] lastHuSide[%s]' % (oldDealerSide, self.lastHuSide),
            LOG_LEVEL_RELEASE)
        if self.curGameCount == 1:
            dealerSide = OWNNER_SIDE
        else:
            # 上局流局
            if self.lastHuSide == -1:
                dealerSide = oldDealerSide
            elif self.lastHuSide == oldDealerSide:
                dealerSide = oldDealerSide
            else:
                if oldDealerSide == 0:
                    dealerSide = self.maxPlayerCount - 1
                else:
                    dealerSide = (oldDealerSide - 1) % self.maxPlayerCount
        if dealerSide == -1:
            log(u'[onSetStart][error] dealerSide false [%s]' % (dealerSide), LOG_LEVEL_RELEASE)
            dealerSide = 0

        self.dealer = self.players[dealerSide]
        self.lastHuSide = -1
        if self.dealer.chair == oldDealerSide:
            self.dealerCount += 1
        else:
            self.dealerCount = 0

        resp.dealer = dealerSide
        resp.dealerCount = self.dealerCount

        resp.dicePoints.extend(dicePoints)
        resp.timestamp = self.server.getTimestamp()

        self.sendAll(resp)
        log(u'[on set start]room[%s] dealer[%s] dealerCount[%s].' % (self.roomId, dealerSide, self.dealerCount),
            LOG_LEVEL_RELEASE)
        self.doAfterSetStart()

    def nextProc(self, curPlayer, isDrawTile=False):
        """
        打牌或摸牌后根据是否存在操作决定下一个流程
        """
        if not isDrawTile and curPlayer != self.dealer or curPlayer != self.dealer and isDrawTile:
            self.isTianDiHu = False
        self.actionplayers = []
        super(Game, self).nextProc(curPlayer, isDrawTile)

    def getAllowActions4Discard(self, curPlayer, player):
        '''出牌時允許的操作'''
        actions = [PONG, OTHERS_KONG, HU]

        # 无牌可摸的情况下，可能需要将杠排除到允许actions之外
        if self.dealMgr.isDraw():
            if not self.canKong4NotTile():
                actions.remove(OTHERS_KONG)

        if not self.isCanChiHu:
            actions.remove(HU)

        if self.lastDiscard == self.players[0].handleMgr.ghost and HU in actions:
            actions.remove(HU)

        if self.lastDiscard in self.players[0].handleMgr.ghostList and HU in actions:
            actions.remove(HU)

        return actions

    def getRobot(self):
        """
        获得使用的玩家类，用于设置掉线后放置玩家的拷贝
        """
        return Player()

    def getSpecialTile(self):
        '''处理鬼牌'''

        # 获取鬼牌
        if self.isHasGhost == 'White':  # 白板做鬼
            specialTile = 'd5'
            self.specialTile = specialTile
        elif self.isHasGhost == 'Random':  # 随机鬼
            specialTile = self.setGhost()
        elif self.isHasGhost == 'DoubleGhost':
            specialTile = self.setGhost(isdouble=True)
        else:
            specialTile = None

        self.logger(u'specialTile %s' % (specialTile))

        return specialTile

    def setGhost(self, isdouble=False):
        """
        定鬼牌
        """
        # HONOR_TILES 风牌、箭刻牌
        # ALL_TILES  所有万筒条
        self.logger(u"Setting ghost")
        tmpghost = random.choice(self.dealMgr.tiles)
        if self.dealMgr.getGhost4GM:
            tmpghost = self.dealMgr.getGhost4GM[0]
            self.logger(u'[getGhost4GM] specialTile %s' % (tmpghost))
        if not isdouble:
            self.dealMgr.tiles.remove(tmpghost)  # 从牌堆中移除这张牌
        if isdouble:
            onetile = self.getNextTile(tmpghost)
            twotile = self.getNextTile(onetile)
            self.specialTile = ','.join([tmpghost, onetile, twotile])
            return [onetile, twotile]
        else:
            ghostTile = self.getNextTile(tmpghost)
            self.specialTile = ','.join([tmpghost, ghostTile])  # 'a2,a3'
            return ghostTile

    def getNextTile(self, tile):
        character = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9']
        dot = ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9']
        bamboo = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9']
        dragon = ['d1', 'd9', 'd5']
        wind = ['e1', 'e4', 'e6', 'e9']
        group = [character, dot, bamboo, dragon, wind]
        ghost = None
        for _iter in group:
            if tile in _iter:
                index = _iter.index(tile)
                if index == (len(_iter) - 1):
                    ghost = _iter[0]
                else:
                    ghost = _iter[index + 1]
                break
        return ghost

    def getHorseTiles(self, side=-1):
        '''获取该玩家可中码的列表'''
        horselist = []
        horsetype = ['a', 'b', 'c']

        horse = [['e1', 'd1'],
                 ['e4', 'd9'],
                 ['e6', 'd5'],
                 ['e9']]
        number = [[1, 5, 9],
                  [2, 6],
                  [3, 7],
                  [4, 8], ]

        if self.gameplayers == 3:
            horse = [['e1', ],
                     ['e4', 'd1'],
                     ['e9', 'd5']]
            number = [[1, 5, 9],
                      [2, 6],
                      [4, 8], ]

        if self.gameplayers == 2:
            horse = [['e1'],
                     ['e6', 'd9'], ]
            number = [[1, 5, 9],
                      [3, 7], ]

        if side == -1:
            return []
        else:
            for h in horsetype:
                for n in number[side]:
                    horselist.append('%s%s' % (h, n))
            horselist.extend(horse[side])
            return horselist

    def getWinhorsetile(self, side=-1, horsetiles=None):
        '''返回码堆中中码的列表'''
        tmphorse = self.getHorseTiles(side)
        self.logger(u'[gethorsetile] horselist is [%s]' % (horsetiles))
        self.logger(u'[gethorsetile] tmphorse is [%s]' % (tmphorse))
        if self.ghostzhong:  # 鬼牌算中牌
            for ghost in self.players[0].handleMgr.ghostList:
                if ghost not in tmphorse:
                    tmphorse.append(ghost)
            self.logger(u'[gethorsetile] [ghostzhong] horselist is [%s]' % (horsetiles))
            self.logger(u'[gethorsetile] [ghostzhong] tmphorse is [%s]' % (tmphorse))
        WinHorse = []
        for h in horsetiles:
            if h in tmphorse:
                WinHorse.append(h)
        return WinHorse

    def setGMType2ValidCmdJudge(self):
        """
         GM类型到相应判断命令是否有效的方法的映射
        """
        GET_TILE = 1
        GET_HAND_TILES = 2
        GET_DEALER = 3
        GET_GHOST = 4
        self.validGMCommand = {
            GET_TILE: self.validGetTile,
            GET_HAND_TILES: self.validGetHandTiles,
            GET_DEALER: self.validGetDealer,
            GET_GHOST: self.validGetGhost,
        }

    def validGetGhost(self, player, data):
        """
        检验GM命令是否有效
        """
        data = re.findall('\D\d', data)
        if data[0] not in self.dealMgr.tiles:
            self.sendGMError(player, ERR_MSG['tileErr'])
            return False
        return True

    def setSpecialTile(self, specialTile):
        """
        设置特殊牌，若self.specialTileIsGhost()为True则自动设置鬼牌
        """
        if self.specialTile and self.specialTileIsGhost():
            for player in self.getPlayers():
                player.handleMgr.setGhost(specialTile)

    def setPlayerCopy(self, robot, player):
        super(Game, self).setPlayerCopy(robot, player)
        robot.totalHuCount = player.totalHuCount

    def getMaxPlayerCount(self):
        """
        返回房间最大玩家数，上层可重写
        """
        return self.gameplayers

    def getDealManager(self):
        """
        返回发牌器
        """
        return DealManager(self)

    def canGrabKongHu(self):
        """
        是否允许抢杠胡
        """
        return self.canBeKongHu

    def dealSelfKong(self, action, player):
        if self.canGrabKongHu():
            log(u'[dealSelfKong] try grabkongHu.', LOG_LEVEL_RELEASE)
            if not player.handleMgr.kongTiles:
                return
            tile = player.handleMgr.kongTiles[-1]
            existCanHu = False
            self.resetCurAction()
            for _player in self.getPlayers((player,)):
                _player.handleMgr.setTmpTile(tile, _player.chair)
                self.isselfkong = True
                actionNtiles = _player.handleMgr.getGrabKongHu()
                self.isselfkong = False
                _player.handleMgr.setTmpTile(None)
                self.addCurAction(_player, actionNtiles)
                if actionNtiles:
                    existCanHu = True
            if existCanHu:
                self.lastOperateSide = player.chair
                self.beGrabKongHuPlayer = self.players[player.chair]
                self.nextProc(player)
                return
        self.drawTile(player)

    def setWinHorse(self, player, horsetiles, isset=False):
        '''设置中码的牌'''
        hside = player.chair
        if hside >= self.dealer.chair:
            bside = hside - self.dealer.chair
        else:
            bside = self.gameplayers - self.dealer.chair + hside
        if isset:
            player.WinHorse = self.getWinhorsetile(bside, horsetiles)
        return self.getWinhorsetile(bside, horsetiles)

    def doBeforeBalance(self, isEndGame=False):
        """
        胡牌结算
        """
        if isEndGame:
            return
        self.logger(u'[doBeforeBalance]')
        self.logger(u'actionplayers is {}'.format(self.actionplayers))
        if self.lastHuSide < 0:
            self.logger(u'nobody hu or isDrawn')
            return False

        horsetiles = []
        if self.HorseCount:
            HorseCount = copy.deepcopy(self.HorseCount)
            horsetiles = self.dealMgr.tiles[:HorseCount]
            self.HorseList.extend(horsetiles)

        self.logger(u'[doBeforeBalance] lastHuSide is {}'.format(self.lastHuSide))
        self.logger(u'[doBeforeBalance] actionplayers is {}'.format(self.actionplayers))
        self.logger(u'[doBeforeBalance] beGrabKongHuPlayer is {}'.format(self.beGrabKongHuPlayer))
        self.logger(u'[doBeforeBalance] lastDiscardSide is {}'.format(self.lastDiscardSide))
        self.logger(u'[doBeforeBalance] beGrabKongHuPlayer is {}'.format(self.beGrabKongHuPlayer))

        HuPlayer = self.players[self.lastHuSide]
        huRate = HuPlayer.handleMgr.getHuScore()  # 获取胡牌分数
        # HuPlayer.huDescs.append(u'名堂分(%s)'%huRate)
        self.logger(u'[doBeforeBalance] huRate is %s' % huRate)
        self.setWinHorse(HuPlayer, horsetiles, isset=True)  # 算中马(赢的那个人)

        self.WinHorseTiles.extend(HuPlayer.WinHorse)  # 中马列表
        # self.compute_hu(HuPlayer, huRate, horsetiles)

        self.logger(u'[doBeforeBalance]')
        if HuPlayer.handleMgr.lastTile:  # 自摸
            self.logger(u'[doBeforeBalance] beGrabKongHuPlayer selfhu')
            HuPlayer.huDescs.append(u'自摸')
            if HuPlayer.handleMgr.BeKongFlower:
                beHuPlayer = self.players[HuPlayer.handleMgr.BeKongFlower]
                beHuPlayer.huDescs.append(u'放杠爆全包')
                score = huRate * (1 + len(HuPlayer.WinHorse)) * 3
                HuPlayer.curGameScore += score
                beHuPlayer.curGameScore -= score
            else:
                for other in self.getPlayers((HuPlayer,)):
                    score = huRate * (1 + len(HuPlayer.WinHorse))
                    HuPlayer.curGameScore += score
                    other.curGameScore -= score
        elif self.beGrabKongHuPlayer:  # 抢杠胡
            beHuPlayer = self.beGrabKongHuPlayer
            # HuPlayer.huDescs.append(u'抢杠胡')
            beHuPlayer.huDescs.append(u'被抢杠胡全包')
            score = huRate * (1 + len(HuPlayer.WinHorse)) * 3
            HuPlayer.curGameScore += score
            beHuPlayer.curGameScore -= score

        if self.HorseCount:
            HuPlayer.huDescs.append(u'中码X%d' % (len(self.WinHorseTiles)))
            resp = guangdong_mahjong_pb2.S_C_RunHorse()
            resp.Horsetiles.extend(self.HorseList)
            resp.WinHorse.extend(self.WinHorseTiles)
            log(u'[S_C_RunHorse]resp is %s' % (resp), LOG_LEVEL_RELEASE)
            self.sendAll(resp)

    def calcBalance(self, player):
        """
        每小局结算算分接口
        """
        if len(player.handleMgr.selfKongTiles):
            player.huDescs.append(u'碰杠X%s' % len(player.handleMgr.selfKongTiles))
        if len(player.handleMgr.concealedKongTiles):
            player.huDescs.append(u'暗杠X%s' % len(player.handleMgr.concealedKongTiles))
        if len(player.handleMgr.othersKongTiles):
            player.huDescs.append(u'接杠X%s' % len(player.handleMgr.othersKongTiles))
        if len(player.handleMgr.beKongTiles):
            player.huDescs.append(u'放杠X%s' % len(player.handleMgr.beKongTiles))

        for other in self.getPlayers((player,)):
            player.curGameScore += len(player.handleMgr.selfKongTiles) * 1
            other.curGameScore -= len(player.handleMgr.selfKongTiles) * 1
            player.curGameScore += len(player.handleMgr.concealedKongTiles) * 2
            other.curGameScore -= len(player.handleMgr.concealedKongTiles) * 2

        for BeKonger in player.handleMgr.othersKongTiles:
            player.curGameScore += 3
            self.players[BeKonger[0]].curGameScore -= 3

    def fillBalanceData(self, player, balanceData):
        '''小局结算'''
        beHuPlayer, _, _ = player.handleMgr.getHuData()
        balanceData.descs.extend(player.getBalanceDescs())
        self.logger(u'{} balance desc is {}'.format(player.nickname, balanceData.descs))
        balanceData.score = player.curGameScore
        balanceData.tiles.extend(player.handleMgr.getBalanceTiles())
        balanceData.tiles.extend(self.getHorseTilesData(player))
        self.logger(u'{} hand tiles {}'.format(player.nickname, balanceData.tiles))
        balanceData.isHu = False
        if beHuPlayer >= 0:
            balanceData.isHu = True

    def fillTotalBalanceData(self, player, balanceData):
        '''大局结算'''
        balanceData.score = player.totalGameScore
        balanceData.descs.extend(player.packTotalBalanceDatas())

    def getSaveSendAllProtoList(self):
        """
        获得需要保存回放的sendAll的协议列表
        """
        return ['S_C_RunHorse']

    def getSaveSendOneProtoList(self):
        """
        获得需要保存回放的sendOne的协议列表
        只保存当前行动玩家的，比如S_C_DrawTiles只会保存发给摸牌的那个人的那条，不会保存发给别人的那条
        """
        return []

    def getHorseTilesData(self, player):  # 奖马信息
        balanceTiles = []
        if player == self.players[self.lastHuSide]:
            balanceTiles.append(','.join(self.WinHorseTiles))
        else:
            balanceTiles.append('')
        balanceTiles.append(','.join(self.HorseList))
        return balanceTiles
