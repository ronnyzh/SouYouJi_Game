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
from player import Player
from deal import DealMange
from common import mahjong_pb2
import hainan_mahjong_pb2
from matchCommon.match_game import MatchGame
from publicCommon.time_config import *
import copy

isValidFreeUpGa = [0, 1, 2, 3, 5]


class Game(MatchGame):
    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
        self.gaList = [None] * self.maxPlayerCount
        self.beginWrap = False  # 是否开始包
        self.firstDiscardSide = []
        self.isFirstCircle = True
        self.isFirstTile = True
        self.orderNum = -1

    def onGa(self, player, gaNum):
        """
        玩家上噶
        """

        if gaNum in isValidFreeUpGa:
            player.ga = gaNum
            player.gaHisList.append(gaNum)
        else:
            print gaNum, isValidFreeUpGa

        self.sendGaBrocast(player, gaNum)

        allSelect = True
        for player in self.players:
            if int(player.ga) == -1:
                log(u'[try Ga][Info] player[%s] ga[%s]' % (player.account, player.ga), LOG_LEVEL_RELEASE)
                allSelect = False

        log(u'[try Ga][info] allSelect[%s]' % (allSelect), LOG_LEVEL_RELEASE)

        if allSelect:
            # 所有玩家选噶后开始游戏
            self.onSetStart(self.players[OWNNER_SIDE])

    def getAllowGa(self, gaNum):
        """
        获取玩家可选的噶
        """

        if self.isFreeUpGa:
            return isValidFreeUpGa

        if self.isUpGa:
            if int(gaNum) >= 3:
                isValidUpGa = [0, 1, 2, 3, 5]
            else:
                isValidUpGa = [0, 1, 2, 3]

            return [ga for ga in isValidUpGa if ga >= gaNum]

    def beWrapLeaveTile(self):
        # 被包剩下的牌张数
        return 19

    def getDealer(self, dicePoints):
        """
        返回庄家座位号
        根据骰子点数确定庄家(可重写，未必与点数相关)
        """
        dealer = self.dealer
        if dealer:
            oldDealerSide = dealer.chair
        else:
            oldDealerSide = -1
        dealerSide = self.dealMgr.getDealerByGM()
        if dealerSide != -1:
            side = dealerSide
        if self.curGameCount == 1:
            side = OWNNER_SIDE
        elif dealer and (oldDealerSide == self.lastHuSide or self.lastHuSide == -1):
            side = oldDealerSide
        else:
            side = (oldDealerSide + 1) % self.maxPlayerCount
        if side == OWNNER_SIDE and not (dealer and (oldDealerSide == self.lastHuSide or self.lastHuSide == -1)):
            self.orderNum += 1

        return side

    def nextProc(self, curPlayer, isDrawTile=False):
        """
        打牌或摸牌后根据是否存在操作决定下一个流程
        """
        log(u'[next proc] curPlayer[%s] isDrawTile[%s].' % (curPlayer.nickname, isDrawTile), LOG_LEVEL_RELEASE)
        if self.curActioningPlayers:
            self.ActionMS = self.actionCounterMs
            self.ActionStartTime = self.server.getTimestamp()
            for player in self.curActioningPlayers:
                if player.isproxy:
                    obj_timer = self.timerMgr.getTimer(callback=self.onAutoActionProxy, overTime=getTime_Action_Proxy(),
                                                       params=(player.chair,),
                                                       note='玩家(%s)设置托管action定时器' % (player.nickname))
                    self.timerMgr.add_Timer(obj_timer, 1)
                    player.Timer = obj_timer

            obj_timer = self.timerMgr.getTimer(callback=self.onDoActionTimeout, overTime=getTime_Action(),
                                               note='全部自动aciton定时器')
            self.timerMgr.add_Timer(obj_timer, 0)
        else:
            if isDrawTile:
                self.dealDrawTile(curPlayer)
                return
            nexter = self.getNexter(curPlayer)
            if not nexter:
                self.balance()
            else:
                if not self.firstDiscardSide:
                    self.firstDiscardSide.append(curPlayer.chair)
                self.dealFirstBeFollow(curPlayer)
                self.drawTile(nexter)

    def dealFirstBeFollow(self, discardPlayer):
        if self.firstDiscardSide and self.isFirstCircle:
            firstDiscardSide = self.firstDiscardSide[0]
            lastDiscardSide = (firstDiscardSide + 3) % self.maxPlayerCount
            if lastDiscardSide == discardPlayer.chair:
                self.isFirstCircle = False
                firstDiscardTile = discardPlayer.handleMgr.discardTiles[0]
                isKeptDiscard = True
                for player in self.players:
                    discardTile = player.handleMgr.discardTiles
                    if (not discardTile) or (discardTile and discardTile[0] != firstDiscardTile):
                        isKeptDiscard = False
                if self.maxPlayerCount in (2, 3):
                    isKeptDiscard = False
                if isKeptDiscard:
                    # 发送首牌被跟协议
                    resp = hainan_mahjong_pb2.S_C_Be_Follow()
                    resp.side = firstDiscardSide
                    self.sendAll(resp)
                    beKeptPlayer = self.players[firstDiscardSide]
                    beKeptPlayer.beFollowFirstTile = True

    def onDiscard(self, player, tile):
        """
        玩家出牌
        """
        if tile in FLOWER_TILES:
            log(u'[onDiscard] player[%s] 不能打花牌' % (player.nickname), LOG_LEVEL_RELEASE)
            return

        if self.isFirstTile and self.dealer.chair != player.chair:
            self.isFirstTile = False
        if self.dealMgr.hasAnyTiles() == self.beWrapLeaveTile():
            # 牌山剩多少张是开始包的时候开始包
            self.beginWrap = True

        player.lastSelfOp = -1
        super(Game, self).onDiscard(player, tile)

    def resetSetData(self):
        '''
        每局数据初始化
        '''
        super(Game, self).resetSetData()
        self.firstDiscardSide = []
        self.isFirstCircle = True
        self.isFirstTile = True

    def doAfterGameStart(self):
        """
        游戏开始后做的操作
        """
        if self.isUpGa or self.isFreeUpGa:
            self.sendGaInfo2Client()
        else:
            super(Game, self).doAfterGameStart()

    def canGrabKongHu(self):
        return True

    def sendGaBrocast(self, player, gaNum):
        """
        发送噶数据给客户端
        """
        reqGaInfo = hainan_mahjong_pb2.S_C_Ga_Choose()
        data = reqGaInfo.data.add()
        data.side = player.chair
        data.ga = gaNum
        reqGaInfo.result = True
        reqGaInfo.reason = ''
        log(u'[try sendGaInfo] player[%s] ga[%s] side[%s]' % (player.account, gaNum, player.chair), LOG_LEVEL_RELEASE)

        self.sendAll(reqGaInfo)

    def sendAllGaBrocast(self):
        """
        """
        reqGaInfo = hainan_mahjong_pb2.S_C_Ga_Choose()
        for player in self.players:
            if int(player.ga) == -1:
                continue
            data = reqGaInfo.data.add()
            data.side = player.chair
            data.ga = player.ga
            reqGaInfo.result = False
            reqGaInfo.reason = ''
            log(u'[try sendAllGaBrocast] player[%s] ga[%s] side[%s]' % (player.account, player.ga, player.chair),
                LOG_LEVEL_RELEASE)

        if reqGaInfo.data:
            self.sendAll(reqGaInfo)

    def sendGaInfo2Client(self):
        """
        发送噶协给客户端
        """
        resp = hainan_mahjong_pb2.S_C_GaData()

        for player in self.players:
            if int(player.ga) == -1:
                sendResp = copy.deepcopy(resp)
                gaData = self.getAllowGa(player.gaHisList[-1] if player.gaHisList else -1)
                print '[gaData]', gaData
                sendResp.canGetGa.extend(gaData)
                self.sendOne(player, sendResp)

        obj_timer = self.timerMgr.getTimer(callback=self.onSelectGaTimeOut, overTime=getTime_Action(),
                                           note='全部自动选噶定时器')
        self.timerMgr.add_Timer(obj_timer, 0)

    def onSelectGaTimeOut(self):
        for _player in self.getPlayers():
            if int(_player.ga) == -1:
                self.onGa(_player, isValidFreeUpGa[0])

    def initByRuleParams(self, ruleParams):
        """
        初始化游戏设置参数
        """

        self.isDealerNidle = False  # 庄闲
        self.isContinueDealer = False  # 是否连庄
        self.isUpGa = False  # 是否上噶
        self.isValidStream = False  # 流局得分是否有效
        self.isFlowerHu = False  # 是否四花胡
        self.isFreeUpGa = False  # 是否自由上噶
        self.isCheatProof = False  # 是否防勾脚
        self.isOrder = False
        self.isPackAll = False

        params = eval(ruleParams)
        self.ruleDescs = []
        # self.gameTotalCount = int(params[-2]) * 8 #游戏总局数
        self.ruleDescs.append("海南棋牌")
        # self.ruleDescs.append("%s局"%(self.gameTotalCount))
        self.hasFan = not bool(params[0])  # 有番无番
        self.ruleDescs.append("%s" % ("有番" if self.hasFan else "-无番"))
        for num in xrange(9):
            if num in params[1]:
                if num == 0:
                    self.isDealerNidle = True
                    self.ruleDescs.append("庄闲")
                elif num == 1:
                    self.isContinueDealer = True
                    self.ruleDescs.append("连庄")
                elif num == 2:
                    self.isUpGa = True
                    self.ruleDescs.append("上噶")
                elif num == 3:
                    self.isValidStream = True
                    self.ruleDescs.append("流局算分")
                elif num == 4:
                    self.isFlowerHu = True
                    self.ruleDescs.append("花胡")
                elif num == 5:
                    self.isFreeUpGa = True
                    if "上噶" in self.ruleDescs:
                        self.ruleDescs.remove("上噶")
                    self.ruleDescs.append("自由上噶")
                elif num == 6:
                    self.isCheatProof = True
                    self.ruleDescs.append("防勾脚")
                elif num == 7:
                    self.isPackAll = True
                    self.ruleDescs.append("海底包牌")
                elif num == 8:
                    self.isOrder = True
                    self.ruleDescs.append("叫令")

        # self.maxPlayerCount = 2 + params[2]
        self.maxPlayerCount = 4
        self.players = [None] * self.maxPlayerCount
        self.ruleDescs.append("%s人" % (self.maxPlayerCount))

        super(Game, self).initByRuleParams(ruleParams)

    def doAfterSetStart(self):
        self.setSpecialTiles()
        if self.isOrder:
            resp = hainan_mahjong_pb2.S_C_Order()
            resp.orderNum = self.orderNum
            self.sendAll(resp)
        super(Game, self).doAfterSetStart()

    def setSpecialTiles(self):
        """
        设置玩家番的标志
        """
        if self.dealer:
            dealerSide = self.dealer.chair
        else:
            dealerSide = OWNNER_SIDE
        for index in xrange(self.maxPlayerCount):
            side = (dealerSide + index) % self.maxPlayerCount
            self.players[side].handleMgr.setFlower(FLOWER_FLOWER_TILES[index])
            self.players[side].handleMgr.setWind(WIND_TILES[index])
            self.players[side].handleMgr.setSeason(FLOWER_SEASON_TILES[index])

    def doBeforeBalance(self, isEndGame=False):
        if self.dealer:
            self.dealer.isDealer = True
            self.dealer.dealerCount = self.dealerCount

    def dealSurroundData(self, beSurroundSide):
        resp = hainan_mahjong_pb2.S_C_Be_Surround()
        resp.side = beSurroundSide
        self.sendAll(resp)

    def doGrabKongHu(self, huPlayer, beGrabPlayer):
        """
        抢杠胡重写
        """
        if not huPlayer.handleMgr.canHu():
            # 如果胡牌玩家无番则被抢杠玩家包胡
            beGrabPlayer.keptHuPlayer = True
        huPlayer.isGrabKongHu = True
        beKongSide = beGrabPlayer.kongPlayers[-1]
        beGrabPlayer.kongPlayers.remove(beKongSide)

        super(Game, self).doGrabKongHu(huPlayer, beGrabPlayer)

    def calcBalance(self, player):
        """
        每小局结算算分接口
        """
        if not self.isValidStream and self.lastHuSide == -1:
            return
        # 获得玩家胡牌参数：点炮玩家,胡牌倍率
        beHuPlayer, huRate = player.getHuData()
        if beHuPlayer is player:
            beHuPlayer = 0

        """
        该玩家杠数据格式：
        [(beKongPlayer, KONG), (None, CANCEAL_KONG)]
        """
        beKongSides = copy.deepcopy(player.kongPlayers)
        log('player before calcBalance[%s] getBeHuPlayer[%s] huRate[%s] beKongSides[%s]' % (
            player, beHuPlayer, huRate, beKongSides), LOG_LEVEL_RELEASE)

        if player.isKeptKong:
            beKongSides = beKongSides[1:]
            for other in self.getPlayers((player,)):
                otherGaScore = other.ga if other.ga >= 0 else 0
                playerGaScore = player.ga if player.ga >= 0 else 0
                baseScore = self.baseScore
                dealerScore = 0
                if player.isDealer or other.isDealer:
                    if self.isContinueDealer:
                        dealerScore = self.dealerCount
                        log('[calc balance]kong:isContinueDealerp[%s]' % (dealerScore), LOG_LEVEL_RELEASE)
                    if self.isDealerNidle:
                        dealerScore += 1
                        log('[calc balance]kong:isDealerNidle[%s]' % (dealerScore), LOG_LEVEL_RELEASE)

                kongRate = 1
                deltaScore = (otherGaScore + playerGaScore + baseScore + dealerScore) * kongRate

                self.dealer.curGameScore -= deltaScore
                player.curGameScore += deltaScore

        for other in self.getPlayers((player,)):
            # 起始分根据点炮与否会略有不同
            otherGaScore = other.ga if other.ga >= 0 else 0
            playerGaScore = player.ga if player.ga >= 0 else 0
            baseScore = self.baseScore
            dealerScore = 0
            if player.isDealer or other.isDealer:
                if self.isContinueDealer:
                    dealerScore = self.dealerCount
                    log('[calc balance]hu:isContinueDealerp[%s]' % (dealerScore), LOG_LEVEL_RELEASE)
                if self.isDealerNidle:
                    dealerScore += 1
                    log('[calc balance]hu:isDealerNidle[%s]' % (dealerScore), LOG_LEVEL_RELEASE)

            if player.flowerHuRate:
                deltaScore = (otherGaScore + playerGaScore + baseScore + dealerScore) * player.flowerHuRate
                other.curGameScore -= deltaScore
                player.curGameScore += deltaScore

            if player.threeTiles or player.fourTiles:
                beHuScore = 0
                if beHuPlayer and beHuPlayer.chair == other.chair:
                    beHuScore = 1
                deltaScore = (otherGaScore + playerGaScore + baseScore + dealerScore) * huRate + beHuScore
                if player.threeTiles:
                    payPlayer = self.players[player.threeTiles[0]]
                    payPlayer.curGameScore -= deltaScore
                    player.curGameScore += deltaScore
                elif player.fourTiles:
                    for side in player.fourTiles:
                        payPlayer = self.players[side]
                        payPlayer.curGameScore -= deltaScore
                        player.curGameScore += deltaScore
            elif beHuPlayer:
                beHuScore = 0
                if other is beHuPlayer:
                    # baseScore = baseScore + 1
                    beHuScore = 1
                deltaScore = (otherGaScore + playerGaScore + baseScore + dealerScore) * huRate + beHuScore
                if (isinstance(beHuPlayer, Player) and self.isCheatProof) or \
                        beHuPlayer.isKeptDiscard or \
                        (beHuPlayer.keptHuPlayer and not player.handleMgr.isCheckHu()) or \
                        beHuPlayer.isWrapTile:
                    # 如果是防勾脚或者是玩家被包或抢杠胡,点炮玩家当老板
                    beHuPlayer.curGameScore -= deltaScore
                else:
                    other.curGameScore -= deltaScore
                player.curGameScore += deltaScore
            elif beHuPlayer == 0:
                deltaScore = (otherGaScore + playerGaScore + baseScore + dealerScore) * huRate
                other.curGameScore -= deltaScore
                player.curGameScore += deltaScore

            if beKongSides:
                log('kong calcBalance[%s] beKongSides[%s] isKeptKong[%s]' % (player, beKongSides, player.isKeptKong),
                    LOG_LEVEL_RELEASE)
                oneHandScore = (otherGaScore + playerGaScore + baseScore + dealerScore)
                for beKongSide in beKongSides:
                    if beKongSide == -1:
                        kongRate = 2
                    else:
                        kongRate = 1
                    deltaScore = oneHandScore * kongRate

                    if self.isCheatProof and beKongSide != -1 and beKongSide != player.chair:
                        self.players[beKongSide].curGameScore -= deltaScore
                    else:
                        other.curGameScore -= deltaScore
                    player.curGameScore += deltaScore
            if player.beFollowFirstTile:
                deltaScore = (otherGaScore + playerGaScore + baseScore + dealerScore)
                other.curGameScore += deltaScore
                player.curGameScore -= deltaScore

        log('player after calcBalance[%s]' % (player), LOG_LEVEL_RELEASE)

    def fillBalanceData(self, player, balanceData):
        """
        客户端显示规则根据发送的balanceData.descs组装每条play的结算信息字串
        如：海南麻将
        player.getBalanceDescs()返回类似：
        ['无噶','点炮','庄闲','1连庄']这样的结算描述给客户端组装显示
        将输赢分数/玩家手牌信息 填充到score/tiles字段
        ['#chow1#a1,a2,a3']
        """
        # 获得玩家胡牌参数：点炮玩家,胡牌倍率
        beHuPlayer, _, _ = player.handleMgr.getHuData()

        balanceData.descs.extend(player.getBalanceDescs())
        balanceData.score = player.curGameScore
        balanceData.tiles.extend(player.handleMgr.getBalanceTiles())
        balanceData.isHu = False
        if beHuPlayer >= 0:
            balanceData.isHu = True

    def fillTotalBalanceData(self, player, balanceData):
        """
        客户端显示规则根据发送的balanceData.descs组装每条play的结算信息字串
        如：海南麻将
        player.getBalanceDescs()返回类似：
        ['无噶','点炮','庄闲','1连庄']这样的结算描述给客户端组装显示
        将输赢分数/玩家手牌信息 填充到score/tiles字段
        ['#chow1#a1,a2,a3']
        """
        balanceData.score = player.totalGameScore
        balanceData.descs.extend(player.packTotalBalanceDatas())

    def doAfterDrawTile(self, drawPlayer):
        """
        海南麻将摸牌之后都要判断是否存在花胡
        """
        flowerTiles = set(drawPlayer.handleMgr.getFlowerTiles())
        if len(flowerTiles) == 8:
            drawPlayer.flowerHuRate = 2
            drawPlayer.flower4HuFlag = False
        else:
            if self.isFlowerHu:
                if drawPlayer.handleMgr.is4FlowerHu():
                    drawPlayer.flowerHuRate = 1
                # if FLOWER_FLOWER_TILES_SET <= flowerTiles:
                # drawPlayer.flowerHuRate = 1
            else:
                if len(flowerTiles) == 7:
                    drawPlayer.flowerHuRate = 1

        log(u'[try flowerHu] player[%s] flowerTiles[%s] flowerHuRate[%s]' % (
            drawPlayer.account, flowerTiles, drawPlayer.flowerHuRate), LOG_LEVEL_RELEASE)
        if drawPlayer.flowerHuRate and drawPlayer.flowerSet != flowerTiles and not drawPlayer.flower4HuFlag:
            resp = hainan_mahjong_pb2.S_C_Flower_Hu()
            resp.side = drawPlayer.chair
            resp.rate = drawPlayer.flowerHuRate
            self.sendAll(resp)

        if self.isFlowerHu:
            if drawPlayer.handleMgr.is4FlowerHu():
                drawPlayer.flower4HuFlag = True
        drawPlayer.flowerSet = flowerTiles
        super(Game, self).doAfterDrawTile(drawPlayer)

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

    def setPlayerCopy(self, robot, player):
        """
        设置拷贝了玩家数据的机器人
        """
        super(Game, self).setPlayerCopy(robot, player)
        robot.ga = player.ga
        robot.gaHisList = player.gaHisList
        robot.flower4HuFlag = player.flower4HuFlag
        robot.flowerSet = player.flowerSet

        robot.flowerHuRate = player.flowerHuRate
        robot.curGameScore = player.curGameScore
        robot.isDealer = player.isDealer
        robot.dealerCount = player.dealerCount
        robot.kongPlayers = player.kongPlayers
        robot.isKeptKong = player.isKeptKong
        robot.isKeptDiscard = player.isKeptDiscard
        robot.keptHuPlayer = player.keptHuPlayer
        robot.isWrapTile = player.isWrapTile
        robot.beFollowFirstTile = player.beFollowFirstTile
        robot.huDescs = player.huDescs
        robot.ChowPongHis = player.ChowPongHis
        robot.beChowPongHis = player.beChowPongHis
        robot.lastSelfOp = player.lastSelfOp
        robot.isGrabKongHu = player.isGrabKongHu
        robot.threeTiles = player.threeTiles
        robot.fourTiles = player.fourTiles

        robot.totalGameScore = player.totalGameScore
        robot.totalKongCount = player.totalKongCount
        robot.totalConcealedKongCount = player.totalConcealedKongCount
        robot.totalHuCount = player.totalHuCount
        robot.totalSelfHuCount = player.totalSelfHuCount

    def getMaxPlayerCount(self):
        """
        返回房间最大玩家数，上层可重写
        """
        return 4

    def drawTile(self, player):
        """
        某玩家摸牌
        """
        # 无牌可摸了，应该结算流局
        if self.dealMgr.isDraw():
            self.balance(isDrawn=True)
            return

        self.beGrabKongHuPlayer = None
        # 摸牌前刷新行动玩家为摸牌玩家，用于记录回放
        self.countPlayerSides = [player.chair]

        resp = mahjong_pb2.S_C_DrawTiles()
        resp.timestamp = self.server.getTimestamp()
        resp.side = player.chair
        otherPlayerResp = copy.deepcopy(resp)
        playerFloweCount = len(player.handleMgr.getFlowerTiles())
        self.onDrawTile(player, resp.tiles)
        self.curPlayerSide = player.chair
        if len(player.handleMgr.getFlowerTiles()) != playerFloweCount:
            player.lastSelfOp = 10

        # 自己的发完手牌，其它人需要mask掉
        self.sendOne(player, resp)
        for drawData in resp.tiles:
            inOuts = otherPlayerResp.tiles.add()
            inTiles = [''] * len(drawData.inTiles)
            inOuts.inTiles.extend(inTiles)
            inOuts.outTiles.extend(drawData.outTiles)
        for _player in self.getPlayers((player,)):
            self.sendOne(_player, otherPlayerResp)

        # 摸牌之后需要生成操作或由上层重写的流程
        self.doAfterDrawTile(player)

    def getSaveSendAllProtoList(self):
        """
        获得需要保存回放的sendAll的协议列表
        """
        return ['S_C_Flower_Hu', 'S_C_Be_Handle_Tiles', 'S_C_Be_Follow', 'S_C_Be_Kong', 'S_C_Be_Surround', 'S_C_Order']

    def getSaveSendOneProtoList(self):
        """
        获得需要保存回放的sendOne的协议列表
        只保存当前行动玩家的，比如S_C_DrawTiles只会保存发给摸牌的那个人的那条，不会保存发给别人的那条
        """
        return []

    def onDiscardTimeout(self, chair):
        """
            超时打牌即进入托管状态
        """
        player = self.players[chair]
        if not self.checkCounter(player):
            return
        if len(player.handleMgr.tiles) % 3 != 2:
            log(u'[onDiscardTimeout][error]tiles[%s] len error.' % (player.handleMgr.tiles), LOG_LEVEL_RELEASE)
            return
        player.isproxy = True
        self.sendProxy(player)
        tile = player.handleMgr.getLastTile()
        if not tile:
            tile = player.handleMgr.tiles[-1]
        if tile in FLOWER_TILES:
            for _index in xrange(1, len(player.handleMgr.tiles) + 1):
                tile = player.handleMgr.tiles[-_index]
                if tile not in FLOWER_TILES:
                    break
        self.onDiscard(player, tile)

    def onAutoDiscardProxy(self, chair):
        """
            托管自动打牌
        """
        player = self.players[chair]
        if not player.isproxy:
            return
        tile = player.handleMgr.getLastTile()
        if not tile:
            tile = player.handleMgr.tiles[-1]
        if tile in FLOWER_TILES:
            for _index in xrange(1, len(player.handleMgr.tiles) + 1):
                tile = player.handleMgr.tiles[-_index]
                if tile not in FLOWER_TILES:
                    break
        self.onDiscard(player, tile)

    def CountdownCallbackFunc(self):
        return [self.onDiscardTimeout, self.onDoActionTimeout, self.onSelectGaTimeOut]
