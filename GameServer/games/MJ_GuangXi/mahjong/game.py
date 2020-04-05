# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: game logic
"""

from common.common_game import CommonGame
import common.mahjong_pb2
from common.card_define import *
from common.log import *
from common.protocols.mahjong_consts import *
from common import mahjong_pb2
from player import Player
from deal import DealManager
import guangxi_mahjong_pb2
import copy
from common.pb_utils import *
import random
from collections import Counter
import traceback

from publicCommon.public_game import PublicGame



class Game(PublicGame):

    def __init__(self, server, ruleParams, needInit=True, roomId=0):
        super(Game, self).__init__(server, ruleParams, needInit, roomId)
        self.gameplayers = self.maxPlayerCount
        self.actionPlayers = []

    def resetSetData(self):
        self.huNumber = 0
        self.WinHorseTiles = []
        self.horseList = []

        super(Game, self).resetSetData()

    def getDealManager(self):
        """
        返回发牌器
        """
        return DealManager(self)

    def initByRuleParams(self, ruleParams):
        '''初始化房間參數'''
        params = eval(ruleParams)
        self.logger(u'[initByRuleParams] params is {}'.format(params))

        self.catchHourseCount_SelfHu = 0
        self.catchHourseCount_OtherHu = 0
        # 是否可吃胡
        self.isCanChiHu = False
        # 吃胡是否计算门清
        self.chiHuCountClean = False
        # 死双
        self.doubleDie = False

        if params[0] == 1:
            self.isCanChiHu = True
            self.ruleDescs.append("点炮胡牌")
        else:
            self.ruleDescs.append("自摸胡牌")

        self.catchHourseType = params[1]
        if params[1] == 1:
            self.ruleDescs.append("胡牌抓码")
        elif params[1] == 2:
            self.ruleDescs.append("吃胡码减半")
        else:
            self.ruleDescs.append("自摸抓码")

        if params[2] == 0:
            self.catchHourseCount_SelfHu = 2
            self.catchHourseCount_OtherHu = 2
            self.ruleDescs.append("抓2码")
        elif params[2] == 1:
            self.catchHourseCount_SelfHu = 4
            self.catchHourseCount_OtherHu = 4
            self.ruleDescs.append("抓4码")
        elif params[2] == 2:
            self.catchHourseCount_SelfHu = 6
            self.catchHourseCount_OtherHu = 6
            self.ruleDescs.append("抓6码")
        elif params[2] == 3:
            self.catchHourseCount_SelfHu = 8
            self.catchHourseCount_OtherHu = 8
            self.ruleDescs.append("抓8码")
        else:
            self.ruleDescs.append("不抓码")

        if self.catchHourseType == 0:
            self.catchHourseCount_OtherHu = 0
        elif self.catchHourseType == 2:
            self.catchHourseCount_OtherHu /= 2

        if 0 in params[3]:
            self.doubleDie = True
            self.ruleDescs.append("死双")
        if 1 in params[3]:
            self.ruleDescs.append("吃炮带门清")
            self.chiHuCountClean = True

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
            dealerSide = -1
            if self.lastHuSide == -1:
                dealerSide = oldDealerSide
            else:
                if self.actionPlayers:
                    if oldDealerSide in self.actionPlayers:
                        dealerSide = oldDealerSide
                elif self.lastHuSide == oldDealerSide:
                    dealerSide = oldDealerSide
            if dealerSide == -1:
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
        self.actionPlayers = []
        self.doAfterSetStart()

    def getAllowActions4Discard(self, curPlayer, player):
        """
        返回游戏规则在别人出牌时允许的麻将操作tuple
        """
        actions = [PONG, OTHERS_KONG, HU]
        # 无牌可摸的情况下，可能需要将杠排除到允许actions之外
        if self.dealMgr.isDraw():
            if not self.canKong4NotTile():
                actions.remove(OTHERS_KONG)
        if self.dealMgr.hasAnyTiles() - self.dealMgr.setting['INVALID_TILES_COUNT'] <= 1:
            if OTHERS_KONG in actions:
                actions.remove(OTHERS_KONG)

        if not self.isCanChiHu:
            actions.remove(HU)
        return actions

    def getAllowActions4Draw(self):
        """
        返回游戏规则在摸牌时允许的麻将操作tuple
        """
        actions = [SELF_KONG, CONCEALED_KONG, HU]
        # 无牌可摸的情况下，可能需要将杠排除到允许actions之外
        if self.dealMgr.isDraw():
            if not self.canKong4NotTile():
                actions.remove(SELF_KONG)
                actions.remove(CONCEALED_KONG)
        if self.dealMgr.hasAnyTiles() - self.dealMgr.setting['INVALID_TILES_COUNT'] <= 1:
            if SELF_KONG in actions:
                actions.remove(SELF_KONG)
            if CONCEALED_KONG in actions:
                actions.remove(CONCEALED_KONG)
        return actions

    def doAfterDrawTile(self, drawPlayer):
        drawPlayer.handleMgr.isCanHu = True
        super(Game, self).doAfterDrawTile(drawPlayer)

    def canGrabKongHu(self):
        """
        是否允许抢杠胡
        """
        return True

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
                actionNtiles = _player.handleMgr.getGrabKongHu()
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

    def setPlayerCopy(self, robot, player):
        super(Game, self).setPlayerCopy(robot, player)
        robot.totalHuCount = player.totalHuCount
        robot.huDescs = player.huDescs
        robot.lastAction = player.lastAction
        robot.actionBefore = player.actionBefore
        robot.horseTiles = player.horseTiles
        robot.winHorse = player.winHorse

    def getRobot(self):
        """
        获得使用的玩家类，用于设置掉线后放置玩家的拷贝
        """
        return Player()

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
        WinHorse = []
        for h in horsetiles:
            if h in tmphorse:
                WinHorse.append(h)
        return WinHorse

    def setWinHorse(self, player, horsetiles, isset=False):
        '''设置中码的牌'''
        hside = player.chair
        if hside >= self.dealer.chair:
            bside = hside - self.dealer.chair
        else:
            bside = self.gameplayers - self.dealer.chair + hside

        winHourseTile = self.getWinhorsetile(bside, horsetiles)
        if isset:
            player.WinHorse = winHourseTile
        return winHourseTile

    def fillBalanceData(self, player, balanceData):
        '''小局结算'''
        beHuPlayer, _, _ = player.handleMgr.getHuData()
        balanceData.descs.extend(player.getBalanceDescs())
        self.logger(u'{} balance desc is {}'.format(player.nickname, balanceData.descs))
        balanceData.score = player.curGameScore
        balanceData.tiles.extend(player.handleMgr.getBalanceTiles())
        self.logger(u'{} hand tiles {}'.format(player.nickname, balanceData.tiles))
        balanceData.isHu = False
        if beHuPlayer >= 0:
            balanceData.isHu = True
            balanceData.tiles.append(",".join(player.winHorse))
        else:
            balanceData.tiles.append("")
        balanceData.tiles.append(",".join(self.horseList))

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

    def getMaxPlayerCount(self):
        """
        返回房间最大玩家数，上层可重写
        """
        return 4

    def canHuMoreThanOne(self):
        """
        是否允许一炮多响
        """
        return True

    def doHuMoreThanOne(self, actionPlayers=None):
        """
        一炮多响时需要做的处理
        """
        self.logger(u"[doHuMoreThanOn] lastDiiscardSide [%s]" % (self.lastDiscardSide))
        self.huNumber += 1
        self.hudealer = self.players[self.lastDiscardSide]

        if len(actionPlayers) < 2:
            return False
        self.isHuMoreThanOne = True
        self.actionPlayers.extend(actionPlayers)

    def doAfterDiscard(self, discardPlayer, tile):
        self.resetCurAction()
        for player in self.getPlayers((discardPlayer,)):
            player.handleMgr.setTmpTile(tile, discardPlayer.chair)
            actionNtiles = player.handleMgr.getAllowActionNTiles(self.getAllowActions4Discard(discardPlayer, player))
            player.handleMgr.setTmpTile(None)
            self.addCurAction(player, actionNtiles)
        self.lastOperateSide = discardPlayer.chair

        if self.isSendReadyHand:
            self.onReadyHand(discardPlayer)

        if not self.curActioningPlayers:
            self.resetLastDiscardKongHistory(msg='[doAfterDiscard]')

        self.nextProc(discardPlayer)

    def nextProc(self, curPlayer, isDrawTile=False):
        """
        打牌或摸牌后根据是否存在操作决定下一个流程
        """
        self.actionPlayers = []
        super(Game, self).nextProc(curPlayer, isDrawTile)

    def resetLastDiscardKongHistory(self, msg='未知'):
        if self.lastDiscardSide < 0:
            return
        discardPlayer = self.players[self.lastDiscardSide]
        self.logger(u'[resetLastDiscardKongHistory] 清理 %s msg=> %s 原来 => %s' %
                    (discardPlayer.__str__(), msg, discardPlayer.handleMgr.alwaysKongs))
        discardPlayer.handleMgr.alwaysKongs = []

    def doAfterDoCurAction(self, curHighestAction, doActionPlayer):
        log(u'[doAfterDoCurAction] room[%s] action[%s] doActionPlayer[%s].' \
            % (self.roomId, curHighestAction, doActionPlayer), LOG_LEVEL_RELEASE)

        if curHighestAction in [PONG, OTHERS_KONG]:
            self.resetLastDiscardKongHistory(msg='[doAfterDoCurAction] %s' % (curHighestAction))

            if doActionPlayer.handleMgr.threeBiSide == -1:
                self.logger(u'[doAfterDoCurAction] %s 3笔状态 => %s' %
                            (doActionPlayer.__str__(), doActionPlayer.handleMgr.threeBi))
                for _side, _time in Counter(doActionPlayer.handleMgr.threeBi).items():
                    if _time >= 3:
                        doActionPlayer.handleMgr.threeBiSide = _side
                        self.players[_side].handleMgr.fengHu = True
                        self.logger(u'[doAfterDoCurAction] %s 被封胡' % (self.players[_side].__str__()))

        self.doActionDict[curHighestAction](curHighestAction, doActionPlayer)

    def dealNotGet(self, action, player):
        if self.beGrabKongHuPlayer:
            self.countPlayerSides = [self.beGrabKongHuPlayer.chair]
            self.drawTile(self.beGrabKongHuPlayer)
            return
        if player.handleMgr.lastTile:
            self.nextProc(player, True)
            return
        self.resetLastDiscardKongHistory(msg='[dealNotGet]')
        self.nextProc(self.players[self.lastDiscardSide])

    def doBeforeBalance(self, isEndGame=False):
        """
        胡牌结算
        """
        if isEndGame:
            return
        self.logger(u'[doBeforeBalance]')
        self.logger(u'[doBeforeBalance] actionPlayers is {}'.format(self.actionPlayers))
        self.logger(u'[doBeforeBalance] lastHuSide is {}'.format(self.lastHuSide))
        self.logger(u'[doBeforeBalance] beGrabKongHuPlayer is {}'.format(self.beGrabKongHuPlayer))
        self.logger(u'[doBeforeBalance] lastDiscardSide is {}'.format(self.lastDiscardSide))
        if self.lastHuSide < 0:
            self.logger(u'nobody hu or isDrawn')
            return False

        for _player in self.getPlayers():
            self.logger(u'[doBeforeBalance] %s alwaysKongs[%s]' % (_player.__str__(), _player.handleMgr.alwaysKongs))

        if self.beGrabKongHuPlayer:
            horseCount = self.catchHourseCount_SelfHu
        elif not self.actionPlayers:
            __HuPlayer__ = self.players[self.lastHuSide]
            if __HuPlayer__.handleMgr.lastTile:  # 自摸
                horseCount = self.catchHourseCount_SelfHu
            else:
                horseCount = self.catchHourseCount_OtherHu
        else:
            horseCount = self.catchHourseCount_OtherHu

        if horseCount:
            horsetiles = self.dealMgr.tiles[:horseCount]
            self.horseList.extend(horsetiles)
            resp = guangxi_mahjong_pb2.S_C_RunHorse()
            resp.Horsetiles.extend(self.horseList)
            self.sendAll(resp)

        if self.actionPlayers:  # 一炮多响
            double = 1
            if self.beGrabKongHuPlayer:
                beHuPlayer = self.beGrabKongHuPlayer
                double = (self.maxPlayerCount - 1)
                self.logger(u'[doBeforeBalance] beGrabKongHuPlayer MoreHu')
            else:
                beHuPlayer = self.players[self.lastDiscardSide]
                self.logger(u'[doBeforeBalance] MoreHu')

            beHuPlayer.huDescs.append(u'放炮')
            for _huside in self.actionPlayers:
                HuPlayer = self.players[_huside]
                HuPlayer.huDescs.append(u'接炮')
                # 算中马
                self.setWinHorse(HuPlayer, self.horseList, isset=True)
                HuPlayer.huDescs.append(u'中码X%s' % (len(HuPlayer.WinHorse)))
                try:
                    descList, totalScore = HuPlayer.handleMgr.getHuScore()
                    HuPlayer.huDescs.extend(descList)
                    totalScore = totalScore * (1 + len(HuPlayer.WinHorse))

                    HuPlayer.curGameScore += totalScore * double
                    beHuPlayer.curGameScore -= totalScore * double

                    if HuPlayer.handleMgr.threeBiSide >= 0:
                        threeBiBePlayer = self.players[HuPlayer.handleMgr.threeBiSide]
                        threeLoseScore = totalScore * 2 if self.doubleDie else 1
                        HuPlayer.curGameScore += threeLoseScore
                        threeBiBePlayer.curGameScore -= threeLoseScore
                        if '三笔' not in threeBiBePlayer.huDescs:
                            threeBiBePlayer.huDescs.append(u'三笔')
                        # threeBiBePlayer.huDescs.append(u'被三笔,额外支出%s' % (threeLoseScore))
                except:
                    traceback.print_exc()
        else:
            HuPlayer = self.players[self.lastHuSide]
            try:
                descList, totalScore = HuPlayer.handleMgr.getHuScore()
                HuPlayer.huDescs.extend(descList)
            except:
                descList, totalScore = [], 0
                traceback.print_exc()
            # 算中马
            self.setWinHorse(HuPlayer, self.horseList, isset=True)
            HuPlayer.huDescs.append(u'中码X%s' % (len(HuPlayer.WinHorse)))

            totalScore = totalScore * (1 + len(HuPlayer.WinHorse))

            if HuPlayer.handleMgr.lastTile:  # 自摸
                self.logger(u'[doBeforeBalance] selfhu')

                if HuPlayer.handleMgr.threeBiSide >= 0:
                    threeBiBePlayer = self.players[HuPlayer.handleMgr.threeBiSide]
                    threeLoseScore = totalScore * (self.maxPlayerCount - 1 + 2 if self.doubleDie else 0)
                    HuPlayer.curGameScore += threeLoseScore
                    threeBiBePlayer.curGameScore -= threeLoseScore
                    if '三笔' not in threeBiBePlayer.huDescs:
                        threeBiBePlayer.huDescs.append(u'三笔')

                elif HuPlayer.handleMgr.alwaysKongs and HuPlayer.handleMgr.alwaysKongs[0] <= 3:
                    # 连杠杠上开花：根据第一个杠来决定由谁支付
                    BaoPlayer = self.players[HuPlayer.handleMgr.alwaysKongs[0]]
                    HuPlayer.curGameScore += totalScore * (self.maxPlayerCount - 1)
                    BaoPlayer.curGameScore -= totalScore * (self.maxPlayerCount - 1)
                else:
                    for _loser in self.getPlayers(excludePlayers=(HuPlayer,)):
                        HuPlayer.curGameScore += totalScore
                        _loser.curGameScore -= totalScore
            else:
                double = 1
                if self.beGrabKongHuPlayer:  # 抢杠胡
                    beHuPlayer = self.beGrabKongHuPlayer
                    double = (self.maxPlayerCount - 1)
                    # HuPlayer.huDescs.append(u'抢杠胡')
                    beHuPlayer.huDescs.append(u'放杠被胡')
                    self.logger(u'doBeforeBalance qiangganghu')
                else:  # 普通吃胡
                    self.logger(u'doBeforeBalance public-Hu')
                    beHuPlayer = self.players[self.lastDiscardSide]
                    HuPlayer.huDescs.append(u'接炮')
                    beHuPlayer.huDescs.append(u'放炮')

                HuPlayer.curGameScore += totalScore * double
                beHuPlayer.curGameScore -= totalScore * double

                if HuPlayer.handleMgr.threeBiSide >= 0:
                    threeBiBePlayer = self.players[HuPlayer.handleMgr.threeBiSide]
                    threeLoseScore = totalScore * 2 if self.doubleDie else 1
                    HuPlayer.curGameScore += threeLoseScore
                    threeBiBePlayer.curGameScore -= threeLoseScore
                    if '三笔' not in threeBiBePlayer.huDescs:
                        threeBiBePlayer.huDescs.append(u'三笔')
                    # threeBiBePlayer.huDescs.append(u'被三笔,额外支出%s' % (threeLoseScore))
