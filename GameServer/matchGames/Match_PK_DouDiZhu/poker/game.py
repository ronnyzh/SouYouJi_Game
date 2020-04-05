# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: game logic
"""

from common.common_game import CommonGame
from common import poker_pb2
from common.consts import *
import fightTheLandlord_poker_pb2
from common.card_define import *
from common.log import *
from common.protocols.poker_consts import *

from player import Player
from deal import *
from consts import *
import private_mahjong_pb2
import copy
import random
from common.pb_utils import *
from twisted.internet.threads import deferToThread
from publicCommon.public_game import PublicGame
from publicCommon.time_config import *
from matchCommon.match_game import MatchGame

HAVE_WILD_CARD = 0
NO_SHUFFLE = 1


class Game(MatchGame):
    def __init__(self, *args, **kwargs):
        self.cardList = []
        super(Game, self).__init__(*args, **kwargs)
        self.firstCallSide = -1

    def resetSetData(self):
        '''
        每局数据初始化
        '''
        super(Game, self).resetSetData()
        self.baseScore = 1
        self.multiple = 1
        self.wildCardList = []
        self.holeCards = []
        self.isLandlordWin = False
        self.isSpring = False
        self.isBeSpring = False
        self.bombCount = 0
        self.isAfterDeal = False
        self.isAfterLandlord = False
        # 抢地主列表
        self.robLandlordList = []
        self.firstRobSide = -1
        self.gameStage = 0
        self.noCallSide = []
        self.noRobSide = []
        self.callScoreList = []
        self.curSelectedMaxScore = 0
        self.curMaxSide = -1
        self.resetCurCallingData()

        self.curCallingNum = 0
        # 全部人不叫次数
        self.curAllNotCallCount = 0
        self.maxAllNotCallCount = 3  # 最大流局次数,达到将会随机庄 如果是0则是无限次

    def resetCurCallingData(self):
        self.curCallingSide = -1
        self.curCallingType = -1

    def resetDealData(self):
        self.isAfterDeal = False
        self.gameStage = 0
        self.noCallSide = []
        self.callScoreList = []
        self.curSelectedMaxScore = 0
        self.curMaxSide = -1
        self.resetCurCallingData()
        self.dealMgr.resetCards()
        for player in self.getPlayers():
            player.isCalledLandlord = False
            player.callData = 0
            player.handleMgr.resetDataPerGame()

    def initByRuleParams(self, ruleParams):
        """
        初始化游戏设置参数
        """
        self.gameType = HAPPY_DDZ  # 经典斗地主 HAPPY_DDZ #欢乐斗地主CLASSICAL_DDZ
        self.callType = CALL_LANDLORD  # 叫分 CALL_LANDLORD #叫地主
        self.maxBombCount = THREE_BOMB  # 炸弹上限
        self.haveWildCard = False  # 是否有癞子
        self.noShuffle = False  # 是否不洗牌
        self.banInteraction = False  # 禁用互动功能
        self.ban3to2 = False  # 禁用3带2
        self.ban4to2 = False  # 禁用4带2

        params = eval(ruleParams)
        log(u'[initByRuleParams] params[%s] ruleParams[%s]' % (params, ruleParams), LOG_LEVEL_RELEASE)
        self.ruleDescs = []

        switch = params[0]

        self.gameType = switch
        if switch == HAPPY_DDZ:
            self.ruleDescs.append('欢乐斗地主')
            self.ruleDescs.append('叫地主')
            self.callType = CALL_LANDLORD
        else:
            if switch == CLASSICAL_DDZ:
                self.ruleDescs.append('经典斗地主')
            self.ruleDescs.append('叫分')
            self.callType = CALL_SCORE

        self.players = [None] * self.maxPlayerCount
        self.ruleDescs.append("%s人" % (self.maxPlayerCount))

        switch = int(params[1])
        self.maxBombCount = switch + 3
        if switch == THREE_BOMB:
            self.ruleDescs.append('3炸')
        elif switch == FOUR_BOMB:
            self.ruleDescs.append('4炸')
        elif switch == FIVE_BOMB:
            self.ruleDescs.append('5炸')

        canChooseList = []
        for num in canChooseList:
            if num == 2:
                self.ban3to2 = True
                self.ruleDescs.append(u"禁用牌型三带二")
            elif num == 3:
                self.ban4to2 = True
                self.ruleDescs.append(u"禁用牌型四带二")
            else:
                if num == HAVE_WILD_CARD:
                    self.haveWildCard = True
                    self.ruleDescs.append('有癞子')
                else:
                    self.noShuffle = True
                    self.ruleDescs.append('不洗牌')

        self.extendStr = '%s,%s,%s,%s,%s' % (self.gameType, self.callType, self.maxBombCount,
                                             self.haveWildCard, self.noShuffle)

        super(Game, self).initByRuleParams(ruleParams)

    def getMaxPlayerCount(self):
        """
        返回房间最大玩家数，上层可重写
        """
        return 3

    def doAfterDeal(self):
        """
        发牌后操作
        """
        self.isAfterDeal = True
        self.cardList = []

        self.gameStage = CALLING
        side = OWNNER_SIDE
        if self.lastWinSide != -1:
            side = self.lastWinSide
        self.firstCallSide = side
        self.logger(u'[doAfterDeal] firstCallSide[%s]' % (self.firstCallSide))
        self.callLandlord(self.firstCallSide, self.callType)

    def dealClassicalFirstCall(self):
        """
        处理经典斗地主叫地主/叫分的流程
        """
        side = OWNNER_SIDE
        self.logger(u'[dealClassicalFirstCall] callType[%s]' % (self.callType))
        if self.lastWinSide != -1:
            side = self.lastWinSide
        self.firstCallSide = side
        self.logger(u'[dealClassicalFirstCall] firstCallSide[%s]' % (self.firstCallSide))
        self.callLandlord(self.firstCallSide, self.callType)

    def calcBalance(self, player):
        """
        每小局结算算分接口
        """
        leftCards = player.handleMgr.getCards()
        self.addCardList(leftCards)
        self.logger(u'[calcBalance] player[%s] isLandlord[%s]' % (player.chair, player.isLandlord))
        if player.isLandlord:
            self.logger(u'[calcBalance] [%s] baseScore[%s] multiple[%s]' %
                        (player.account, self.baseScore, self.multiple))
            deltaScore = self.baseScore * self.multiple

            if self.isLandlordWin:
                for other in self.getPlayers((player,)):
                    other.curGameScore -= deltaScore
                    player.curGameScore += deltaScore
            else:
                for other in self.getPlayers((player,)):
                    other.curGameScore += deltaScore
                    player.curGameScore -= deltaScore

    def fillBalanceData(self, player, balanceData):
        """
        客户端显示规则根据发送的balanceData.descs组装每条play的结算信息字串
        如：海南麻将
        player.getBalanceDescs()返回类似：
        ['缺门','掐张']这样的结算描述给客户端组装显示
        将输赢分数/玩家手牌信息 填充到score/cards字段
        ['#chow1#a1,a2,a3']
        """

        balanceData.descs.extend(player.getBalanceDescs())
        balanceData.score = player.curGameScore
        balanceData.cards.extend(player.handleMgr.getBalanceCards())
        balanceData.isWin = False
        if self.isGameEnd and ((self.isLandlordWin and player.isLandlord) or
                               not (self.isLandlordWin or player.isLandlord)):
            balanceData.isWin = True

    def fillTotalBalanceData(self, player, balanceData):
        """
        客户端显示规则根据发送的balanceData.descs组装每条play的结算信息字串
        如：海南麻将
        player.getBalanceDescs()返回类似：
        ['无噶','点炮','庄闲','1连庄']这样的结算描述给客户端组装显示
        将输赢分数/玩家手牌信息 填充到score/cards字段
        ['#chow1#a1,a2,a3']
        """
        balanceData.score = player.totalGameScore
        balanceData.descs.extend(player.packTotalBalanceDatas())

    def getDealManager(self):
        """
        返回发牌器
        """
        return DealMange(self)

    def getRobot(self):
        """
        获得使用的玩家类，用于设置掉线后放置玩家的拷贝
        """
        return Player()

    def getSaveSendAllProtoList(self):
        """
        获得需要保存回放的sendAll的协议列表
        """
        return ['S_C_RobLandlordResult', 'S_C_RobLandlord', 'S_C_ScoreData']

    def getResetProtoList(self):
        return ['S_C_DealCards', 'S_C_RobLandlord', 'S_C_RobLandlordResult', 'S_C_ScoreData']

    def setGMType2ValidCmdJudge(self):
        # GM类型到相应判断命令是否有效的方法的映射
        super(Game, self).setGMType2ValidCmdJudge()
        self.validGMCommand[GET_HOLE_CARDS] = self.validGetHoleCards
        self.validGMCommand[GET_WILD_CARDS] = self.validGetWildCards

    def validGetHoleCards(self, player, data):
        """
        检验GM命令是否有效
        """
        data = reCards.findall(data)
        log(u'valid data[%s] poolCards[%s]' % (data, self.dealMgr.poolCards), LOG_LEVEL_RELEASE)
        for card in data:
            if card not in self.dealMgr.poolCards:
                self.sendGMError(player, ERR_MSG['cardErr'])
                return False
        return True

    def validGetWildCards(self, player, data):
        """
        检验GM命令是否有效
        """
        return self.validGetHoleCards(player, data)

    def getCanChooseScore(self, mustBeLandlord=False):
        start = self.curSelectedMaxScore + 1
        self.logger(u'[getCanChooseScore] curSelectedMaxScore => %s' % self.curSelectedMaxScore)
        end = 4
        if mustBeLandlord:
            start = end - 1
            self.logger(u'[getCanChooseScore] mustBeLandlord')
        if start > end:
            return []
        _list = range(start, end)
        self.logger(u'[getCanChooseScore] _list => %s' % _list)
        return _list

    def onRobLandlordTimeOut(self, side, callType, operate, callingNum):
        if side != self.curCallingSide:
            return
        if self.curCallingNum != callingNum:
            return
        player = self.players[side]
        player.mustBeLandlord = False
        self.onRobLandlord(player, callType, operate)

    def onRobLandlord(self, player, callType, operate):
        self.logger(u'[onRobLandlord] player[%s] gameType[%s] callType[%s] operate[%s]'
                    % (player.chair, self.gameType, callType, operate))
        if self.holeCards:
            self.logger(u'[onRobLandlord] holeCards is set')
            return

        if player.mustBeLandlord:

            if player.isLandlord:
                if self.gameStage == ACTIONING:  # 倒计还没结束时，玩家已做了操作，待倒计结束时执行该操作将被直接返回
                    return

            if not self.haveWildCard and self.gameType == CLASSICAL_DDZ:
                if self.curCallingType == CALL_SCORE:
                    chooseScore = self.getCanChooseScore(mustBeLandlord=True)
                    operate = chooseScore[-1]
                    callType = CALL_SCORE
                else:
                    operate = 1
                    callType = CALL_LANDLORD

        if operate == NO_CALL and callType != ROB_LANDLORD and callType != CALL_SCORE:
            self.sendRobResult(player, callType, operate)
            if len(self.noCallSide) == self.maxPlayerCount:
                self.doDrawn()  # 流局
            else:
                side = self.getNextValidSide(player.chair)
                self.callLandlord(side, callType)
            return

        if operate > NO_CALL:
            self.robLandlordList.append(player.chair)

        if self.gameType == CLASSICAL_DDZ:
            if callType == CALL_LANDLORD or operate == 3:
                self.doLandlord(player, callType, operate)
                return
            # 叫分
            self.sendRobResult(player, callType, operate)
            if len(self.noCallSide) == self.maxPlayerCount:
                self.doDrawn()  # 流局
                return
            if operate > self.curSelectedMaxScore:
                self.curSelectedMaxScore = operate
                self.curMaxSide = player.chair
            self.logger(u'[onRobLandlord] callScoreList => %s' % (self.callScoreList))
            if len(self.callScoreList) == self.maxPlayerCount:
                self.doLandlord(self.players[self.curMaxSide], callType, self.curSelectedMaxScore)
                return

            side = self.getNextValidSide(player.chair)
            self.callLandlord(side, callType)
            return

        if callType == CALL_LANDLORD and self.gameType != CLASSICAL_DDZ:
            side = self.getNextValidSide(player.chair)

            if side == player.chair:
                self.doLandlord(player, callType, operate)
                return
            self.sendRobResult(player, callType, operate)
            self.firstRobSide = side
            self.gameStage = ROBING
            self.callLandlord(side, ROB_LANDLORD)
            return

        if callType == ROB_LANDLORD:
            if operate == CALL:
                self.multiple *= 2
            side = self.getNextValidSide(player.chair)
            if side == self.robLandlordList[-1] or side == self.firstRobSide:
                self.doLandlord(player, callType, operate)
                return
            self.sendRobResult(player, callType, operate)
            self.callLandlord(side, ROB_LANDLORD)

    def sendRobResult(self, player, callType, operate, isConfirmLandlord=False):

        if callType == ROB_LANDLORD:
            player.isRobedLandlord = True
            player.robData = operate
            if operate == NO_CALL:
                self.noRobSide.append(player.chair)
        elif callType in [CALL_LANDLORD, CALL_SCORE]:
            player.isCalledLandlord = True
            player.callData = operate
            self.callScoreList.append(player.chair)
            if operate == NO_CALL:
                self.noCallSide.append(player.chair)

        resp = fightTheLandlord_poker_pb2.S_C_RobLandlordResult()
        resp.side = player.chair
        resp.choseType = callType
        resp.operate = operate
        resp.isConfirmLandlord = isConfirmLandlord
        if isConfirmLandlord:
            self.fillLandlordData(resp.landlordData)
        self.sendAll(resp)

        if callType == ROB_LANDLORD and operate == CALL:
            scoreResp = self.packScoreData(player)
            self.sendAll(scoreResp)

    def getNextValidSide(self, side):
        tryCount = self.maxPlayerCount
        while True:
            tryCount -= 1
            side = self.getNextSide(side)
            if side not in self.noCallSide:
                break
            assert tryCount
        return side

    def doLandlord(self, player, callType, operate):
        # 避免重复当地主

        self.logger(u'[doLandlord] callType[%s] operate[%s]' % (callType, operate))

        if self.gameType == CLASSICAL_DDZ and callType == CALL_SCORE:
            self.baseScore = operate
        if self.haveWildCard:
            wildCard = self.dealMgr.getWildCard()
            self.wildCardList.append(wildCard)
            for _player in self.players:
                _player.handleMgr.setWildCard(self.wildCardList)

        landlordSide = self.robLandlordList[-1]
        player_ = self.players[landlordSide]
        if player_.isLandlord:
            return

        self.dealerSide = player_.chair
        self.holeCards = self.dealMgr.getHoleCards()
        player_.handleMgr._addCards(self.holeCards)
        player_.handleMgr.doSortMyCards()
        player_.isLandlord = True
        self.sendRobResult(player, callType, operate, True)
        self.doAfterLandlord()

    def doAfterLandlord(self):
        self.isAfterLandlord = True
        curPlayer = self.players[self.dealerSide]
        self.logger(u'[doAfterLandlord] curPlayer[%s]' % (curPlayer))
        self.gameStage = ACTIONING
        self.doSendAllowActions(curPlayer)
        self.resetCurCallingData()

    def autoDoAction(self, player, action, actionCards, num):
        self.logger(u'[autoDoAction] player[%s] action[%s] actionCards[%s]' % (player.chair, action, actionCards))
        self.onDoAction(player, action, actionCards, num)

    def fillOpenHandData(self, resp):
        """
        处理明牌数据
        """
        for player in self.players:
            if player.isOpenHand:
                playerHandData = resp.playerHandData.add()
                playerHandData.side = player.chair
                playerHandData.handCards.extend(player.handleMgr.cards)
        self.logger(u'[fillOpenHandData] resp[%s]' % (resp))
        return resp

    def doBeforeBalance(self, isEndGame=False):
        """
        结算前重写逻辑
        """
        self.logger(u'doBeforeBalance setSpring')
        if self.isGameEnd:
            self.setSpring()

    def setSpring(self):
        isSpring = True
        for player in self.players:
            if player.isLandlord and len(player.handleMgr.discardCards) == 1:
                self.isBeSpring = True
                self.multiple *= 2
            if not player.isLandlord and player.handleMgr.discardCards:
                isSpring = False
        if isSpring:
            self.isSpring = True
            self.multiple *= 2

    def packScoreData(self, player, isBomb=False):
        """
        处理score数据
        """
        resp = fightTheLandlord_poker_pb2.S_C_ScoreData()
        resp.baseScore = self.baseScore
        resp.multiple = self.multiple
        resp.isBomb = isBomb
        if isBomb:
            resp.playerBombData.side = player.chair
            resp.playerBombData.bombCount = player.bombCount
        self.logger(u'[packScoreData] resp[%s]' % (resp))
        return resp

    def fillRobLandlord(self, resp):
        """
        """
        resp.side = self.curCallingSide
        resp.choseType = self.curCallingType
        if self.callType == 1:
            resp.canChooseScore.extend(self.getCanChooseScore())
            if self.players[resp.side].mustBeLandlord:
                resp.canChooseScore.extend(self.getCanChooseScore(True))
        self.logger(u'[fillRobLandlord] resp[%s]' % (resp))
        return resp

    def fillLandlordData(self, resp):
        """
        """
        dealerSide = self.dealerSide
        if self.dealerSide < 0:
            dealerSide = 100
        resp.landlordSide = dealerSide
        holeCards = ','.join(self.holeCards)
        resp.holeCards = holeCards
        resp.baseScore = self.baseScore
        resp.multiple = self.multiple
        resp.wildCard.extend(self.wildCardList)
        self.logger(u'[fillLandlordData] resp[%s]' % (resp))
        return resp

    def dealBombData(self, player):
        player.bombCount += 1
        self.bombCount += 1
        if self.bombCount <= self.maxBombCount:
            self.multiple *= 2

        resp = self.packScoreData(player, True)
        self.sendAll(resp)

    def fillCommonData(self, resp):
        commonData = resp.gameCommonDatas.add()
        commonData.datas.extend(self.getCommonData())
        commonData.extendData.extend(self.getCommonExtendData())

    def getCommonExtendData(self):
        if self.isSpring:
            return [1]
        if self.isBeSpring:
            return [2]
        return []

    def getCommonData(self):
        descs = []

        desc = ('底分:%s' % (self.baseScore)).decode('utf-8')
        descs.append(desc)

        # desc = ('叫地主:x%s'%(self.callLandlordCount)).decode('utf-8')
        # descs.append(desc)

        # if self.bombCount:
        desc = ('炸弹:x%s' % (self.bombCount)).decode('utf-8')
        descs.append(desc)

        if self.isSpring:
            desc = '春天:x1'.decode('utf-8')
            descs.append(desc)
        if self.isBeSpring:
            desc = '反春天:x1'.decode('utf-8')
            descs.append(desc)

        desc = ('总倍数:x%s' % (self.multiple)).decode('utf-8')
        descs.append(desc)

        return descs

    def isCanEndGame(self, curPlayer):
        """
        是否结束游戏，上层根据具体条件重写
        """
        if not curPlayer.handleMgr.getCards():
            if curPlayer.isLandlord:
                self.isLandlordWin = True
            return True
        return False

    def addCardList(self, cards):

        b = set(self.cardList)
        c = set(cards)
        cards = list(c - (b & c))
        self.cardList.extend(cards)
        self.logger(u'[addCardList] cards[%s] cardList[%s]' % (cards, self.cardList))

    def setPlayerCopy(self, robot, player):
        """
        设置拷贝了玩家数据的机器人
        """
        super(Game, self).setPlayerCopy(robot, player)

        robot.totalBombCount = player.totalBombCount
        robot.gameScores = player.gameScores
        robot.callLandlordCount = player.callLandlordCount

        robot.isLandlord = player.isLandlord
        robot.isOpenHand = player.isOpenHand
        robot.bombCount = player.bombCount
        robot.isRobedLandlord = player.isRobedLandlord
        robot.robData = player.robData
        robot.isCalledLandlord = player.isCalledLandlord
        robot.callData = player.callData
        robot.isAutoDiscard = player.isAutoDiscard

        robot.mustBeLandlord = player.mustBeLandlord
        robot.needCallScore = player.needCallScore

    def onJoinGame(self, player, resp, isSendMsg=True):
        """
        加入游戏
        """
        super(Game, self).onJoinGame(player, resp, isSendMsg=True)

        # 通知禁用互动功能
        if self.banInteraction:
            resp = private_mahjong_pb2.S_C_BanInteraction()
            resp.result = True
            self.sendOne(player, resp)

    def doSendAllowActions_midway(self, curPlayer):
        autoDiscard = curPlayer.handleMgr.isDisRocket(self.lastDiscard)
        if not autoDiscard:
            if curPlayer.isAutoDiscard:
                leftCards = curPlayer.handleMgr.getAutoDiscard()
                obj_timer = self.timerMgr.getTimer(
                    callback=self.onSpecialAutoAction,
                    overTime=getTime_Action_special(),
                    params=(curPlayer.chair, self.actionNum, DISCARD, leftCards, curPlayer.isproxy),
                    note='[%s]打双鬼,可直接出完所有牌' % (curPlayer.nickname)
                )
                self.timerMgr.add_Timer(obj_timer, 1)
            elif curPlayer.isproxy:
                super(Game, self).doSendAllowActions_midway(curPlayer)
        else:
            if curPlayer.isproxy:
                super(Game, self).doSendAllowActions_midway(curPlayer)
            elif not curPlayer.isAutoDiscard:
                obj_timer = self.timerMgr.getTimer(
                    callback=self.onSpecialAutoAction,
                    overTime=getTime_Action_special(),
                    params=(curPlayer.chair, self.actionNum, PASS, '', curPlayer.isproxy),
                    note='[%s]打双鬼,直接PASS' % (curPlayer.nickname)
                )
                self.timerMgr.add_Timer(obj_timer, 1)

    def onSpecialAutoAction(self, chair, actionNum, action=PASS, actionCards='', Auto=True):
        if not self.checkStage(GAMING):
            return
        player = self.players[chair]
        if not self.checkCounter(player):
            return
        if actionNum != self.actionNum:
            return
        if not self.lastDiscard:
            return
        self.onDoAction(player, action, actionCards, self.actionNum, Auto=Auto)

    def checkCurAction(self, player, actionNum):
        chair = player.chair
        if not self.checkStage(GAMING):
            return False
        player = self.players[chair]
        if not self.checkCounter(player):
            return False
        if actionNum != self.actionNum:
            return False
        return True

    def onAutoActionTimeOut(self, chair, actionNum, Auto=True):
        player = self.players[chair]
        if not self.checkCurAction(player, actionNum):
            return
        self.defaultActionDo(chair, actionNum, Auto=Auto)

    def onAutoActionProxy(self, chair, actionNum, Auto=True):
        player = self.players[chair]
        if not player.isproxy:
            return
        self.defaultActionDo(chair, actionNum, Auto=Auto)

    def defaultActionDo(self, chair, actionNum, Auto=True):
        player = self.players[chair]
        if not self.checkCurAction(player, actionNum):
            return
        if not self.lastDiscard:
            self.onDoAction(player, DISCARD, [player.handleMgr.getSmallestCards()], self.actionNum, Auto=True)
        else:
            self.onDoAction(player, PASS, '', self.actionNum, Auto=Auto)

    def checkCounter(self, player):
        """
        """
        if isinstance(self.countPlayerSides, (list, tuple, set)):
            if player.chair not in self.countPlayerSides:
                self.logger(u'[check counter][error]error counter[%s] need counter[%s].' %
                            (player.chair, self.countPlayerSides))
                return False
        else:
            if player.chair != self.countPlayerSides:
                self.logger(u'[check counter][error]error counter[%s] need counter[%s].' %
                            (player.chair, self.countPlayerSides))
                return False
        return True

    def callLandlord(self, side, type):
        """
        type==0:叫地主
        type==1:叫分
        type==2:抢地主
        """
        self.curPlayerSide = side
        self.curCallingSide = side
        self.curCallingType = type

        self.logger(u'[callLandlord] curCallingSide[%s] curCallingType[%s]' %
                    (self.curCallingSide, self.curCallingType))

        player = self.players[side]
        resp = fightTheLandlord_poker_pb2.S_C_RobLandlord()
        resp.side = self.curCallingSide
        resp.choseType = self.curCallingType
        self.sendExclude((player,), resp)
        self.curCallingNum += 1

        if not self.haveWildCard and self.gameType == CLASSICAL_DDZ:
            player = self.players[self.curCallingSide]
            if player.handleMgr.mustBeLandLord():
                player.mustBeLandlord = True
                if self.curCallingType == CALL_SCORE:
                    chooseScore = self.getCanChooseScore(mustBeLandlord=True)
                    resp.canChooseScore.extend([chooseScore[-1]])
                    obj_timer = self.timerMgr.getTimer(
                        callback=self.onRobLandlordTimeOut,
                        overTime=getTime_RobLandlord_Must(),
                        params=(player.chair, self.curCallingType, chooseScore[-1], self.curCallingNum),
                        note='[%s]双鬼4个2必需抢' % (player.nickname))
                    self.timerMgr.add_Timer(obj_timer, 1)
                else:
                    obj_timer = self.timerMgr.getTimer(
                        callback=self.onRobLandlordTimeOut,
                        overTime=getTime_RobLandlord_Must(),
                        params=(player.chair, self.curCallingType, 1, self.curCallingNum),
                        note='[%s]双鬼4个2必需抢' % (player.nickname))
                    self.timerMgr.add_Timer(obj_timer, 1)
            else:
                if self.callType == CALL_SCORE:
                    resp.canChooseScore.extend(self.getCanChooseScore())
        else:
            if self.callType == CALL_SCORE:
                resp.canChooseScore.extend(self.getCanChooseScore())
        self.sendOne(player, resp)
        self.logger(u'[callLandlord] resp => %s' % (resp))

        if self.callType == CALL_SCORE:
            operate = resp.canChooseScore[0]
        else:
            operate = 0

        obj_timer = self.timerMgr.getTimer(
            callback=self.onRobLandlordTimeOut,
            overTime=getTime_RobLandlord(),
            params=(player.chair, self.curCallingType, 0, self.curCallingNum),
            note='全局抢庄,不抢[%s]' % (player.nickname))
        self.timerMgr.add_Timer(obj_timer, 0)

    def CountdownCallbackFunc(self):
        return [self.onRobLandlordTimeOut]

    def doDrawn(self):
        self.curAllNotCallCount += 1
        log(u'[doDrawn]', LOG_LEVEL_RELEASE)
        self.logger(u'[doDrawn] curAllNotCallCount[%s]' % (self.curAllNotCallCount))

        if self.maxAllNotCallCount and self.curAllNotCallCount >= self.maxAllNotCallCount:
            luckyBoy = random.choice(self.getPlayers())

            self.robLandlordList.append(luckyBoy.chair)
            if self.callType == CLASSICAL_DDZ:
                self.curSelectedMaxScore = 1
                self.curMaxSide = luckyBoy.chair
                self.doLandlord(luckyBoy, self.curCallingType, self.curSelectedMaxScore)
            else:
                self.doLandlord(luckyBoy, self.curCallingType, 1)
        else:
            self.resetDealData()
            self.doResetReplayData()
            self.deal(True)
