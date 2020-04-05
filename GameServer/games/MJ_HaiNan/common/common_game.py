#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Author: $Author$
@Date: $Date$
@version: $Revision$

Description: Describe module function
"""

from common.gameobject import GameObject
from common import consts
from common.consts import ERR_MSG
from common.log import log, LOG_LEVEL_RELEASE
from common_player import CommonPlayer
from common.deal_manage import *

from common.protocols.mahjong_consts import *
from common_db_define import *
from card_define import *

import mahjong_pb2
import replay4proto_pb2
from pb_utils import *
import random
import time
from datetime import datetime
import copy
import redis_instance
import re
import statics


WAIT_BACK_TIME = 15*1000 + consts.LAG_MS
WAIT_DISSOLVE_TIME = 3 * 60 * 1000 #等待解散时间
GAME_NOT_START_END_TIME = 6 * 60 * 60 * 1000
PUBLIC_ROOM_GAME_NOT_START_END_TIME = 6 * 60 * 60 * 1000
OTHER_TYPE_GAME_NOT_START_END_TIME = 6 * 60 * 60 * 1000

SAVE_SEND_ALL_PROTO_LIST = ['S_C_Discard', 'S_C_DoAction', 'S_C_RollDice', 'S_C_SetStart']
SAVE_SEND_ONE_PROTO_LIST = ['S_C_DrawTiles']
SAVE_SEND_PROC_PROTO_LIST = ['S_C_DealTiles']
SAVE_SEND_END_PROTO = 'S_C_Balance'

PING_INTERVAL_TICK = 25*1000


class CommonGame(GameObject):
    """
    """
    def __init__(self, server, ruleParams, needInit = True, roomId = 0):
        """
        """
        self.server = server
        self.roomId = roomId
        self.roomName = ''
        self.parentAg = None
        # 是否允许相同IP玩家进入房间
        self.allowSameIpNotInto = False

        self.ruleParams = ruleParams
        self.playerCount = 0
        self.maxPlayerCount = self.getMaxPlayerCount()
        self.curGameCount = 0
        self.gameTotalCount = self.getGameTotalCount()
        self.gamePlayedCount = 0
        self.players = [None]*self.maxPlayerCount
        self.side2gps = {}
        self.dealer = None
        self.controlPlayerSide = -1 #调试模式时可能指定由一个人控制四个人
        self.dealerCount = 0
        self.specialTile = None
        self.isDebug = False
        self.isParty = False
        self.ownner = ''
        self.otherRoomTable = ''
        self.isUseRoomCards = False
        self.needRoomCards = 1
        self.baseScore = 1 #基本分
        self.isSendReadyHand = False
        self.isHidden = False
        #倒计时回调及毫秒
        self.__resetCounter()
        self.resetCurAction()
        self.maxDiceCount = self.getMaxDiceCount()
        self.stage = WAIT_START #游戏状态
        self.exitPlayers = [] #掉线玩家的位置列表
        self.countPlayerSides = []
        self.ready2NextGameSides = []

        #倒计时毫秒数
        self.discardCounterMs = self.getDiscardCounterMs()
        self.diceCounterMs = self.getDiceCounterMs()
        self.actionCounterMs = self.getActionCounterMs()
        self.balanceCounterMs = self.getBalanceCounterMs()
        self.dissovedCounterMs = 0
        self.dissoved4GameNotStartMs = 0

        #解散
        self.dissolvePlayerSide = -1
        self.dissolve = [None] * self.maxPlayerCount
        self.isSaveGameData = False
        self.isEnding = False

        #回放
        self.replayRefreshData = None
        self.saveSendAllProtoList = copy.deepcopy(SAVE_SEND_ALL_PROTO_LIST)
        self.saveSendAllProtoList.extend(self.getSaveSendAllProtoList())
        self.saveSendOneProtoList = copy.deepcopy(SAVE_SEND_ONE_PROTO_LIST)
        self.saveSendOneProtoList.extend(self.getSaveSendOneProtoList())
        self.oldBalanceData = None

        self.lastHuSide = -1 #记录上次胡牌的size
        self.actionNum = 0

        #时间记录
        self.gameStartTime = 0
        self.gameEndTime = 0

        self.ruleDescs = []
        if needInit:
            self.initByRuleParams(ruleParams)
        
        #发牌器
        self.dealMgr = self.getDealManager()
        self.setGMType2ValidCmdJudge()

        self.resetSetData()

        self.initDoActionDict()

#++++++++++++++++++++ 响应消息回调 ++++++++++++++++++++


    def onGameStart(self, player):
        """
        开始游戏（房主点击或自动开始）
        """
        if player.chair != OWNNER_SIDE:
            log(u'[on game start][error]error chair[%s].'%(player.chair), LOG_LEVEL_RELEASE)
            return

        if self.getEmptyChair() != consts.SIDE_UNKNOWN: #满人
            log(u'[on game start][error]room is not full, empty chair[%s].'%(self.getEmptyChair()), LOG_LEVEL_RELEASE)
            resp = mahjong_pb2.S_C_GameStartResult()
            resp.result = False
            errMsg = '房间未满，无法开始'.decode('utf-8')
            resp.reason = errMsg
            self.sendOne(player, resp)
            return

        if self.stage != WAIT_START and not self.isEnding:
            log(u'[on game start][error]can not start, stage[%s], isEnding[%s].'%(self.stage, self.isEnding), LOG_LEVEL_RELEASE)
            return

        if not self.setStartTime:
            self.setStartTime = self.server.getTimestamp()
        if not self.gameStartTime:
            self.gameStartTime = self.server.getTimestamp()
            # 数据统计
            statics.dig_game_start(self)

        self.dissoved4GameNotStartMs = 0
        self.ready2NextGameSides = []
        self.isEnding = False
        self.stage = GAME_READY

        resp = mahjong_pb2.S_C_GameStartResult()
        resp.result = True
        self.sendOne(player, resp)


        self.doBeforeGameStart()
        self.doAfterGameStart()

    def onSetStart(self, player):
        """
        开始游戏（每小局开始）
        """
        if not self.checkStage(GAME_READY):
            return

        if player.chair != OWNNER_SIDE:
            log(u'[on set start][error]error chair[%s].'%(player.chair), LOG_LEVEL_RELEASE)
            return

        self.doBeforeSetStart()
        self.stage = WAIT_ROLL
        self.curGameCount += 1
        self.startLock = True

        resp = mahjong_pb2.S_C_SetStart()
        dicePoints = self.getDicePoint()
        dealerSide = self.getDealer(dicePoints)
        if self.dealer:
            oldDealerSide = self.dealer.chair
        else:
            oldDealerSide = -1
        self.dealer = self.players[dealerSide]
        self.lastHuSide =  -1
        if self.dealer.chair == oldDealerSide:
            self.dealerCount += 1
        else:
            self.dealerCount = 0

        resp.dealer = dealerSide
        resp.dealerCount = self.dealerCount

        resp.dicePoints.extend(dicePoints)
        resp.timestamp = self.server.getTimestamp()

        self.sendAll(resp)

        log(u'[on set start]room[%s] dealer[%s] dealerCount[%s].'%(self.roomId, dealerSide, self.dealerCount), LOG_LEVEL_RELEASE)

        self.doAfterSetStart()

    def onRollDice(self, player):
        """
        庄家打骰，系统发牌
        """
        if not self.checkStage(WAIT_ROLL):
            return

        if not self.checkCounter(player):
            return

        self.doBeforeRollDice()
        self.stage = GAMING
        self.rollLock = True

        resp = mahjong_pb2.S_C_RollDice()
        resp.dicePoints.extend(self.getDicePoint())
        self.sendAll(resp)

        self.doAfterRollDice()

    def onDiscard(self, player, tile):
        """
        玩家出牌
        """
        if not self.checkStage(GAMING):
            return

        if not self.checkCounter(player):
            return

        #检测有无此牌
        if not player.handleMgr.checkTile(tile):
            log(u'[try play tile][error]tile[%s] not in handleMgr[%s].'%(tile, player.handleMgr.tiles), LOG_LEVEL_RELEASE)
            return

        if len(player.handleMgr.tiles) % 3 != 2:
            log(u'[try play tile][error]tiles[%s] len error.'%(player.handleMgr.tiles), LOG_LEVEL_RELEASE)
            return

        log(u'[try play tile]player[%s] tiles[%s].'%(player.nickname, player.handleMgr.tiles), LOG_LEVEL_RELEASE)
        self.discard(player, tile)

    def onDoAction(self, player, action, actionTiles, num):
        """
        玩家操作(吃碰杠胡)
        """
        if not self.checkStage(GAMING):
            return

        if not self.checkCounter(player):
            return

        if not self.doCurAction(player, action, actionTiles, num):
            return

    def onReadyHand(self, player):
        """
        返回听牌列表
        """
        readyHands = player.getReadyHands(self.dealMgr.getTryReadyHandTiles())
        log(u'[get ready hands]room[%s] nickname[%s] readyHands[%s].'%(self.roomId, player.nickname, readyHands), LOG_LEVEL_RELEASE)

        resp = mahjong_pb2.S_C_ReadyHand()
        resp.tile.extend(readyHands)
        self.sendOne(player, resp)

        self.doAfterReadyHand(player)
    def onReadyHandFancy(self, player,onetile):
        """
        返回听牌列表
        """
        if onetile in player.handleMgr.tiles:
                readyHands = player.handleMgr.getReadyHandsFancy(self.dealMgr.getTryReadyHandTiles(),onetile)
                log(u'[get ready hand fancy s]room[%s] nickname[%s] readyHands[%s].'%(self.roomId, player.nickname, readyHands), LOG_LEVEL_RELEASE)
        
                resp = mahjong_pb2.S_C_ReadyHand()
                resp.tile.extend(readyHands)
                alltiles=copy.deepcopy(player.handleMgr.tiles)
                alltiles.remove(onetile)
                resp.myTiles.extend(alltiles)
                self.sendOne(player, resp)
    def onDissolveRoom(self, player):
        """
        玩家发起解散
        """
        if self.dissolvePlayerSide >= 0:
            log(u'[try dissolve game][error]side[%s] is dissolveing.'%(self.dissolvePlayerSide), LOG_LEVEL_RELEASE)
            return

        #非房主不能解散
        # if player.chair != OWNNER_SIDE:
            # log(u'[try dissolve game][error]nickname[%s] is not game master.'%(player.nickname), LOG_LEVEL_RELEASE)
            # return

        if self.stage == WAIT_START:
            log(u'[try dissolve game][error]error stage.', LOG_LEVEL_RELEASE)
            return

        self.dissolvePlayerSide = player.chair
        self.dissolve[player.chair] = True
        self.dissovedCounterMs = self.server.getTimestamp() + self.getDissolvedCounterMs()
        log(u'[try dissolve game]nickname[%s] room[%s].'%(player.nickname, self.roomId), LOG_LEVEL_RELEASE)
        # if self.maxPlayerCount <= 2:
            # self.dissovedCounterMs = 0
            # resp = mahjong_pb2.S_C_DissolveVoteResult()
            # resp.result = True
            # self.sendAll(resp)
            # self.dissolve = [None] * self.maxPlayerCount
            # self.dissolvePlayerSide = -1
            # log(u'[try dissolve vote]room[%s] dissolve succed for player count[%s].'%(self.roomId, self.maxPlayerCount), LOG_LEVEL_RELEASE)
            # self.endGame()
        # else:
        self.sendDissolveResult(player)

    def onDissolveVote(self, player, result):
        """
        解散投票
        """

        if self.dissolvePlayerSide < 0:
            log(u'[try dissolve vote][error]no one want to dissolve game.', LOG_LEVEL_RELEASE)
            return

        side = player.chair
        if self.dissolve[side] != None:
            log(u'[try dissolve vote][error]nickname[%s] is voted.'%(player.nickname), LOG_LEVEL_RELEASE)
            return

        self.dissolve[side] = result
        if self.dissolve.count(True) >= self.getDissolveSuccedNeedPlayerCount() or\
                self.dissolve.count(False) > self.getDissolveFailNeedPlayerCount():
            self.dissovedCounterMs = 0
            resp = mahjong_pb2.S_C_DissolveVoteResult()
            resp.result = result
            self.sendAll(resp)
            self.dissolve = [None] * self.maxPlayerCount
            self.dissolvePlayerSide = -1
            if result:
                log(u'[try dissolve vote]room[%s] dissolve succed.'%(self.roomId), LOG_LEVEL_RELEASE)
                self.endGame()
            else:
                log(u'[try dissolve vote]room[%s] dissolve failed.'%(self.roomId), LOG_LEVEL_RELEASE)
            return
        #依旧解散中，告知投票结果
        self.sendDissolveResult(player)

    def onReady2NextGame(self, player):
        """
        快速关闭结算页面，所有玩家都做了此操作后，马上开始下一小局
        """
        if not self.isEnding:
            log(u'[ready next]room[%s] game is not end.'%(self.roomId), LOG_LEVEL_RELEASE)
            return

        side = player.chair
        if side not in self.ready2NextGameSides:
            self.ready2NextGameSides.append(side)
        if len(self.ready2NextGameSides) >= self.maxPlayerCount:
            log(u'[ready next]room[%s] all ready.'%(self.roomId), LOG_LEVEL_RELEASE)
            self.ready2NextGameSides = []
            #马上开始下一局
            self.__resetCounter()
            self.onGameStart(self.players[OWNNER_SIDE])

    def onSetGps(self, player, gpsValue):
        """
        设置gps
        """
        self.side2gps[player.chair]=gpsValue

        resp = mahjong_pb2.S_C_Gps()
        for side, gps in self.side2gps.items():            
            gpsData = resp.gpsDatas.add()
            gpsData.chair = side
            gpsData.gpsValue = gps
        self.sendAll(resp)

    def onJoinGame(self, player, resp, isSendMsg = True):
        """
        加入游戏
        """
        chair = self.getEmptyChair()
        assert chair != consts.SIDE_UNKNOWN
        player.chair = chair
        player.game = self

        self.server.savePlayerGameData(player, self.roomId)
        if not self.parentAg: #房间绑定代理商
            self.parentAg = player.parentAg
        self.playerCount += 1
        self.players[chair] = player

        joinResponse = mahjong_pb2.S_C_JoinRoom()
        joinResponse.info.headImgUrl = player.headImgUrl
        joinResponse.isFull = False
        pbPlayerInfo(joinResponse.info, self, player.chair)

        pbRoomInfo(resp.myInfo.roomInfo, self.server, self)
        pbPlayerInfo(resp.myInfo.selfInfo, self, player.chair, isNeedMyData = True)
        for p in self.players:
            if not p:
                continue
            _playerInfo = resp.myInfo.roomInfo.playerList.add()
            pbPlayerInfo(_playerInfo, self, p.chair)

        if self.getEmptyChair() == consts.SIDE_UNKNOWN: #满人
            joinResponse.isFull = True

            #打包全员初始数据保存回放
            saveResp = mahjong_pb2.S_C_RefreshData()
            saveResp.result = True
            self.server.tryRefresh(self, player, saveResp)
            self.replayRefreshData = saveResp.SerializeToString()
            self.doAfterRoomFull()

        if isSendMsg:
            self.sendOne(player, resp)
            self.sendExclude((player,), joinResponse)
            self.server.sendOthersOnlineState(player)

        self.server.userDBOnJoinGame(player, self)

    def onExitGame(self, player, sendMessage = True, byPlayer = False, isEndGame = False):
        """
        退出游戏
        """
        if not player or not player.game or player.game != self:
            return

        isOwnnerEnd = False #房主提前退出导致的游戏结束
        isDrop = False #是否断开玩家，只有离开当前game时才为true
        side = player.chair

        if (byPlayer and self.stage == WAIT_START) or isEndGame: #未开始前客户端主动退出，或者游戏结束
            isDrop = True
            log(u'[on exit]nickname[%s] is exit room[%s] in wait time.'%(player.nickname, self.roomId), LOG_LEVEL_RELEASE)
            if sendMessage:
                exitResp = mahjong_pb2.S_C_ExitRoom()
                exitResp.info.side = side
                exitResp.info.nickname = player.nickname
                self.sendExclude((player,), exitResp)
            self.players[side] = None
            self.playerCount -= 1
            #该情况下不记录重连信息，无法重连
            self.server.tryRmExitPlayerData(player, self)
            if not isEndGame and side == OWNNER_SIDE and not self.ownner: #开始前庄家退出T出全员解散
                log(u'[try dissolve game]game is not start and master[%s] is exit.'%(player.nickname), LOG_LEVEL_RELEASE)
                isOwnnerEnd = True
        else: #游戏中退出，需要记录重连信息
            log(u'[on exit]nickname[%s] is exit room[%s] in game time.'%(player.nickname, self.roomId), LOG_LEVEL_RELEASE)
            self.exitPlayers.append(side)
            robot = self.getRobot()
            self.setPlayerCopy(robot, player)
            self.server.saveExitPlayer(player, self)

            #发送离线状态
            # self.onLeaveGame(robot.chair)
            robot.isOnline = False
            _resp = mahjong_pb2.S_C_OnlineState()
            _resp.changeSide = player.chair
            _resp.isOnline = player.isOnline
            self.sendExclude((player,), _resp)

        player.chair = consts.SIDE_UNKNOWN
        player.game = None

        self.server.userDBOnExitGame(player, self, isDrop)

        if side == self.controlPlayerSide:
            for otherPlayer in self.getPlayers((robot,)):
                self.onExitGame(otherPlayer, sendMessage = False)
        if byPlayer and self.stage == WAIT_START:
            resp = mahjong_pb2.S_C_ExitRoomResult()
            resp.result = True
            self.sendOne(player, resp)
        if isOwnnerEnd:
            self.endGame(isNotStart = True)

    def setGMType2ValidCmdJudge(self):
        """
         GM类型到相应判断命令是否有效的方法的映射
        """
        self.validGMCommand = {
            GET_TILE         :  self.validGetTile,
            GET_HAND_TILES   :  self.validGetHandTiles,
            GET_DEALER       :  self.validGetDealer,
        }

    def sendGMError(self, player, errMsg):
        """
        """
        resp = mahjong_pb2.S_C_GMControl()
        resp.result = False
        resp.reason = errMsg
        self.sendOne(player, resp)
        
    def validGetTile(self, player, data):
        """
        检验GM命令是否有效
        """
        data = re.findall('\D\d', data)
        for tile in data:
            if tile not in self.dealMgr.tiles:
                log(u'valid data[%s] tile[%s] tiles[%s]'%(data, tile, self.dealMgr.tiles),LOG_LEVEL_RELEASE)
                self.sendGMError(player, ERR_MSG['tileErr'])
                return False
        # if data not in self.dealMgr.tiles:
            # self.sendGMError(player, ERR_MSG['tileErr'])
            # return False
        return True
        
    def validGetDealer(self, player, data):
        """
        检验GM命令是否有效
        """
        data = int(data)
        if data >= len(self.players) or data < 0:
            self.sendGMError(player, ERR_MSG['sideErr'])
            return False
        return True
            
    def validGetHandTiles(self, player, data):
        """
        检验GM命令是否有效
        """
        # data = re.findall('\D\d', data)
        if len(data)/2.0 > self.dealMgr.setting['HAND_TILES_COUNT']:
            self.sendGMError(player, ERR_MSG['lenErr'])
            return False
        # for tile in data:
            # if tile not in self.dealMgr.tiles:
                # log(u'valid data[%s] tile[%s] tiles[%s]'%(data, tile, self.dealMgr.tiles))
                # self.sendGMError(player, ERR_MSG['tileErr'])
                # return False
        return self.validGetTile(player, data)
        
    def onGMControl(self, player, type, data):
        """
        """
        if not self.dealMgr.ctrlTypes.has_key(type):
            self.sendGMError(player, ERR_MSG['typeErr'])
            log(u'[try control]control failed, nickname[%s] type[%s] data[%s].'%(player.nickname, type, data), LOG_LEVEL_RELEASE)
            return
            
        validCommand = self.validGMCommand[type](player, data)
        if not validCommand:
            log(u'[try control]control failed, nickname[%s] type[%s] data[%s].'%(player.nickname, type, data), LOG_LEVEL_RELEASE)
            return

        self.dealMgr.ctrlTypes[type](player.chair, data)

        resp = mahjong_pb2.S_C_GMControl()
        resp.result = True
        resp.reason = ''
        self.sendOne(player, resp)
        log(u'[try control]control succeed, nickname[%s] type[%s] data[%s].'%(player.nickname, type, data), LOG_LEVEL_RELEASE)

    def onTalk(self, emoticons, side, voiceNum, duration): #发表情和语音
        log(u'[player talk]room[%s] side[%s] talk[%s] [%s] [%s].'%(self.roomId, side, emoticons, voiceNum, duration), LOG_LEVEL_RELEASE)
        resp = mahjong_pb2.S_C_Talk()
        resp.talkSide = side
        if emoticons:
            resp.emoticons = emoticons
        if voiceNum:
            resp.voice = voiceNum
        if duration:
            resp.duration = duration
        # self.sendExclude((self.players[side],), resp)
        self.sendAll(resp)

#++++++++++++++++++++ 响应消息回调 end ++++++++++++++++++++

#++++++++++++++++++++ 麻将工具函数 ++++++++++++++++++++

    def discard(self, discardPlayer, tile):
        """
        出牌
        """
        discardPlayer.handleMgr.discard(tile)
        resp = mahjong_pb2.S_C_Discard()
        resp.tile= tile
        resp.side = discardPlayer.chair
        resp.timestamp = self.server.getTimestamp()
        log(u'[on discard]room[%s] nickname[%s] tile[%s] handle[%s].'\
            %(self.roomId, discardPlayer.nickname, tile, discardPlayer.handleMgr.tiles), LOG_LEVEL_RELEASE)
        self.sendAll(resp)

        self.lastDiscard = tile
        self.lastDiscardSide = discardPlayer.chair
        self.doAfterDiscard(discardPlayer, tile)

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

        self.nextProc(discardPlayer)

    def drawTile(self, player):
        """
        某玩家摸牌
        """
        #无牌可摸了，应该结算流局
        if self.dealMgr.isDraw():
            self.balance(isDrawn = True)
            return

        self.beGrabKongHuPlayer = None
        #摸牌前刷新行动玩家为摸牌玩家，用于记录回放
        self.countPlayerSides = [player.chair]
        
        resp = mahjong_pb2.S_C_DrawTiles()
        resp.timestamp = self.server.getTimestamp()
        resp.side = player.chair
        otherPlayerResp = copy.deepcopy(resp)
        self.onDrawTile(player, resp.tiles)
        self.curPlayerSide = player.chair

        #自己的发完手牌，其它人需要mask掉
        self.sendOne(player, resp)
        for drawData in resp.tiles:
            inOuts = otherPlayerResp.tiles.add()
            inTiles= [''] * len(drawData.inTiles)
            inOuts.inTiles.extend(inTiles)
            inOuts.outTiles.extend(drawData.outTiles)
        for _player in self.getPlayers((player,)):
            self.sendOne(_player, otherPlayerResp)

        #摸牌之后需要生成操作或由上层重写的流程
        self.doAfterDrawTile(player)

    def deal(self):
        """
        发牌处理
        """
        resp = mahjong_pb2.S_C_DealTiles()
        specialTile = self.getSpecialTile()
        self.setSpecialTile(specialTile)
        #存在特殊牌才写入该字段
        if self.specialTile:
            resp.specialTile = self.specialTile
        resp.timestamp = self.server.getTimestamp()

        #发牌
        self.dealMgr.deal()
        eachTiles = self.dealMgr.getEachTiles()
        for player, handleTiles in zip(self.getPlayers(), eachTiles):
            log(u'[try deal]room[%s] nickname[%s] handleTiles%s.'%(self.roomId, player.nickname, handleTiles), LOG_LEVEL_RELEASE)
            player.setHandleTiles(handleTiles)
            #客户端的牌值为逗号分隔的字串
            playerResp = copy.deepcopy(resp)
            playerResp.tiles.extend(handleTiles)
            self.sendOne(player, playerResp)

        self.doAfterDeal()

    def balance(self, isDrawn = False, isEndGame = False, isSave = True, needSpecitile = True):
        """
        结算并结束游戏
        """
        log(u'[on balance]room[%s] curGameCount[%s] gameTotalCount[%s] isDrawn[%s] isEndGame[%s] isSave[%s].'\
                %(self.roomId, self.curGameCount, self.gameTotalCount, isDrawn, isEndGame, isSave), LOG_LEVEL_RELEASE)
        self.doBeforeBalance()
        if not self.setEndTime:
            self.setEndTime = self.server.getTimestamp()
        if not self.gameEndTime:
            self.gameEndTime = self.server.getTimestamp()

        if not self.isUseRoomCards and self.curGameCount == 1 and not self.isDebug and not self.isParty and isSave:
            self.server.useRoomCards(self)

        #检测局数是否直接结束全部
        if self.curGameCount + 1 > self.gameTotalCount:
            log(u'[on balance]room[%s] curGameCount[%s] > gameTotalCount[%s].'%(self.roomId, self.curGameCount, self.gameTotalCount), LOG_LEVEL_RELEASE)
            isEndGame = True

        #打包小局数据
        resp = mahjong_pb2.S_C_Balance()
        resp.isDrawn = isDrawn
        if needSpecitile and self.specialTile:
            resp.ghostTile = self.specialTile
        if isSave:
            for player in self.getPlayers():
                self.calcBalance(player)

        for player in self.getPlayers():
            if self.stage != GAME_READY: #局间不显示单局结算数据
                userData = resp.setUserDatas.add()
                pbBalanceData(player, userData)
                self.fillBalanceData(player, userData)
                player.upTotalUserData()
            if isEndGame:
                totalUserData = resp.gameUserDatas.add()
                pbBalanceData(player, totalUserData)
                self.fillTotalBalanceData(player, totalUserData)
                totalUserData.roomSetting = self.ruleDescs
        self.oldBalanceData = copy.deepcopy(resp)
        self.sendAll(resp)

        #每局数据存盘
        if isSave:
            self.server.savePlayerBalanceData(self, resp.setUserDatas)
            saveResp = mahjong_pb2.S_C_RefreshData()
            saveResp.result = True
            self.server.tryRefresh(self, player, saveResp)
            self.replayRefreshData = saveResp.SerializeToString()
            self.isSaveGameData = True
            self.gamePlayedCount += 1
        if isEndGame:
            if self.isSaveGameData:
                #总数据存盘
                log(u'[on balance]room[%s] save all data.'%(self.roomId), LOG_LEVEL_RELEASE)
                self.server.savePlayerTotalBalanceData(self, resp.gameUserDatas)
            self.removeRoom()
        else:
            #切换下一局
            self.resetSetData()
            self.isEnding = True
            self.stage = GAME_READY
            # self.onSetStart(self.players[OWNNER_SIDE])
            self.setCounter([self.dealer.chair], self.balanceCounterMs, self.onGameStartTimeout)

    def removeRoom(self):
        statics.dig_game_end(self)
        for player in self.getPlayers():
            self.onExitGame(player, isEndGame = True, sendMessage = False)
        if self.playerCount <= 0: #房间无人则移除房间
            log(u'[try end game] nobody in room[%s].'%(self.roomId), LOG_LEVEL_RELEASE)
            self.server.onRemoveGame(self)
        else:
            log(u'[try end game][error]player in room[%s], players[%s], playerCount[%s]'%(self.roomId, self.getPlayers(), self.playerCount), LOG_LEVEL_RELEASE)

    def resetSetData(self):
        '''
        每局数据初始化
        '''
        self.setStartTime = 0
        self.setEndTime = 0
        for player in self.getPlayers():
            player.resetPerGame()

        #回放
        self.replayData = []
        self.replayinitTilesData = []

        self.dicePoints = []
        self.lastDiscard = ''
        self.lastDiscardSide = -1
        self.curPlayerSide = 0
        self.lastOperateSide = -1
        self.beGrabKongHuPlayer = None

        self.dealMgr.resetTiles()

    def endGame(self, isNotStart = False):
        """
        结束游戏（主动解散房间）
        """
        #发送报表
        if isNotStart:
            for player in self.getOnlinePlayers((self.players[OWNNER_SIDE],)):
                try:
                    messsageStr = '房主退出，游戏解散'.decode('utf-8')
                    player.drop(messsageStr, type = 2)
                except Exception as e:
                    print 'drop error e:%s'%(e)
                    print 'drop nickname%s'%(player.nickname)
            self.removeRoom()
        else:
            self.balance(isEndGame = True, isSave = False)

    def nextProc(self, curPlayer, isDrawTile = False):
        """
        打牌或摸牌后根据是否存在操作决定下一个流程
        """
        log(u'[next proc] curPlayer[%s] isDrawTile[%s].'%(curPlayer.nickname, isDrawTile), LOG_LEVEL_RELEASE)
        if self.curActioningPlayers:
            playerSides = self.getPlayers2sides(self.curActioningPlayers)
            self.setCounter(playerSides, self.actionCounterMs, self.onDoActionTimeout)
        else:
            if isDrawTile:
                self.dealDrawTile(curPlayer)
                # self.curPlayerSide = curPlayer.chair
                # self.setCounter([curPlayer.chair], self.discardCounterMs, self.onDiscardTimeout, [curPlayer.chair])
                return
            nexter = self.getNexter(curPlayer)
            if not nexter:
                self.balance()
            else:
                self.drawTile(nexter)

    def dealDrawTile(self, curPlayer):
        self.curPlayerSide = curPlayer.chair
        self.setCounter([curPlayer.chair], self.discardCounterMs, self.onDiscardTimeout, [curPlayer.chair])

    def resetCurAction(self):
        """
        curActions = (chow, pong, hu)
        curAction2PlayerNtiles = {
            hu : {player1.chair : ['a1,a3', 'a3,a4'], 
                    player2.chair : [...]
                    },
            pong : {player1.chair : ['b2', 'a3,a4']},
            chow : {player1.chair : ['a1,a3', 'a3,a4']},
        }
        curActioningPlayers = (player1, player2)
        curActionedPlayerDatas = {
            player1.chair : (hu, ['a1,a3'])
            player2.chair : (chow, ['a1,a3'])
        }
        """
        self.curActions = []
        self.curAction2PlayerNtiles = {}
        self.curActioningPlayers = []
        self.curActionedPlayerDatas = {}
        self.curHighestAction = 0
        self.grabKongTile = ''
        self.side2ActionNum = {}

    def addCurAction(self, player, actionNtiles):
        """
        """
        if actionNtiles:
            if player.chair not in self.countPlayerSides:
                self.countPlayerSides.append(player.chair)
            # self.countPlayerSides = [player.chair]
            self.curActions.extend(actionNtiles.keys())
            #优化排序,最后一个action为最高优先级
            self.curActions.sort()
            self.curActioningPlayers.append(player)
            resp = mahjong_pb2.S_C_AllowAction()
            self.actionNum += 1
            self.side2ActionNum[player.chair] = self.actionNum
            resp.num = self.actionNum
            for action, tiles in actionNtiles.iteritems():
                log(u'[try add cur action]room[%s] nickname[%s] action[%s] tiles[%s].'%(self.roomId, player.nickname, action, tiles), LOG_LEVEL_RELEASE)
                if action not in self.curAction2PlayerNtiles:
                    self.curAction2PlayerNtiles[action] = {}
                chair = player.chair
                if chair not in self.curAction2PlayerNtiles[action]:
                    self.curAction2PlayerNtiles[action][chair] = tiles
                    if NOT_GET not in self.curAction2PlayerNtiles:
                        self.curAction2PlayerNtiles[NOT_GET] = {}
                    self.curAction2PlayerNtiles[NOT_GET][chair] = []

                actionObj = resp.actions.add()
                actionObj.action = action
                actionObj.tiles.extend(tiles)
            self.sendOne(player, resp)

    def doCurAction(self, player, action, actionTiles, num):
        """
        """
        if action != NOT_GET and action not in self.curActions:
            log(u'[try do curAction][error]action[%s] not in curActions[%s].'%(action, self.curActions), LOG_LEVEL_RELEASE)
            return False

        if player not in self.curActioningPlayers:
            log(u'[try do curAction][error]player[%s] not in curActioningPlayers.'%(player.nickname), LOG_LEVEL_RELEASE)
            return False

        side = player.chair
        if side not in self.curAction2PlayerNtiles[action]:
            log(u'[try do curAction][error]side[%s] not in curAction2PlayerNtiles[%s].'\
                    %(side, self.curAction2PlayerNtiles[action]), LOG_LEVEL_RELEASE)
            return False

        if side not in self.side2ActionNum or num != self.side2ActionNum[side]:
            log(u'[try do curAction][error]error num[%s] for side[%s] player[%s], side2ActionNum[%s].'\
                    %(num, side, player.nickname, self.side2ActionNum), LOG_LEVEL_RELEASE)
            return False

        allowActionTiles = self.curAction2PlayerNtiles[action][side]

        #判断操作的麻将是否在允许集合中
        if action and actionTiles not in allowActionTiles:
            log(u'[try do curAction][error]actionTiles[%s] not in allowActionTiles[%s].'%(actionTiles, allowActionTiles), LOG_LEVEL_RELEASE)
            return False

        for _action in self.curAction2PlayerNtiles:
            if side in self.curAction2PlayerNtiles[_action]:
                del self.curAction2PlayerNtiles[_action][side]
                if _action in self.curActions:
                    self.curActions.remove(_action)
        log(u'[doCurAction]curAction2PlayerNtiles[%s] curActions[%s] num[%s].'\
            %(self.curAction2PlayerNtiles, self.curActions, num), LOG_LEVEL_RELEASE)
        self.curActionedPlayerDatas[side] = (action, actionTiles)
        existHigherAction = False
        if action >= self.curHighestAction:
            if self.highestActionIsHu() and self.curHighestAction == HU:
                pass
            else:
                self.curHighestAction = action

        #是否存在当前确认操作的一样或更高的优先级
        if self.curActions:
            highestAction = self.curActions[-1]
        else:
            highestAction = 0
        if self.highestActionIsHu() and HU in self.curActions:
            highestAction = HU
        #规则不允许一炮多响的话，即不存在同一优先级的等待，同一优先级只取最高的
        if self.canHuMoreThanOne():
            existHigherAction = self.curHighestAction <= highestAction
        else:
            existHigherAction = self.curHighestAction < highestAction #是否存在更高级的action
            if not existHigherAction:
                if self.curHighestAction != action: #是否存在还未执行最高级action的玩家
                    existHigherAction = bool(self.curAction2PlayerNtiles[self.curHighestAction])
                else:#是否同级里面存在更高优先级的顺位
                    existHigherAction = self.existHigherSide(player, action)
            #清理
            if not existHigherAction:
                for _side in self.curActionedPlayerDatas.keys()[:]:
                    if self.curActionedPlayerDatas[_side][0] != self.curHighestAction or\
                            self.existHigherSide4End(_side, self.curHighestAction):
                        del self.curActionedPlayerDatas[_side]
        existHigherAction = existHigherAction and self.curAction2PlayerNtiles[highestAction]
        log(u'[doCurAction]existHigherAction[%s] curActions[%s].'\
                    %(existHigherAction, self.curActions), LOG_LEVEL_RELEASE)

        #最高优先的操作者>1的话，即为一炮多响
        topActionPlayerCount = 0
        doActionPlayer = player
        curHighestAction = NOT_GET
        if not existHigherAction:
            log(u'[doCurAction]curActionedPlayerDatas[%s].'\
                    %(self.curActionedPlayerDatas), LOG_LEVEL_RELEASE)
            for chair, actionNtiles in self.curActionedPlayerDatas.iteritems():
                _action, tiles = actionNtiles
                if self.curHighestAction == _action:
                    if not _action:
                        continue
                    curHighestAction = _action
                    doActionPlayer = self.players[chair]
                    resp = mahjong_pb2.S_C_DoAction()
                    resp.side = chair
                    if _action == CONCEALED_KONG:
                        copyResp = copy.deepcopy(resp)
                    actionObj = resp.action.add()
                    actionObj.action = _action
                    if doActionPlayer.handleMgr.tmpSide >=0:
                        actionObj.beActionSide = doActionPlayer.handleMgr.tmpSide

                    tileList = tiles.split(',')
                    tileList = doActionPlayer.handleMgr.packActionTiles(_action, tileList)

                    if _action == HU:
                        if self.beGrabKongHuPlayer:
                            self.grabKongTile = tileList[-1]
                            self.doGrabKongHu(doActionPlayer, self.beGrabKongHuPlayer)
                        handTiles = self.getHuTileList(doActionPlayer, tileList)
                        actionObj.tiles.extend(handTiles)
                    actionObj.tiles.extend(tileList)

                    #暗杠不显示给其他玩家
                    if _action == CONCEALED_KONG:
                        self.sendOne(doActionPlayer, resp)
                        tileList = self.getTileList(doActionPlayer, tileList[-1])
                        actionObj2 = copyResp.action.add()
                        actionObj2.action = _action
                        actionObj2.tiles.extend(tileList)
                        self.sendExclude((doActionPlayer,), copyResp)
                    else:
                        self.sendAll(resp)
                    log(u'[try do cur action]room[%s] player[%s] action[%s] handle[%s].'\
                            %(self.roomId, doActionPlayer.nickname, _action, doActionPlayer.handleMgr.tiles), LOG_LEVEL_RELEASE)

                    doActionPlayer.doAction(_action, tiles.split(','))

                    topActionPlayerCount += 1
            self.resetCurAction()

            if topActionPlayerCount > 1:
                self.doHuMoreThanOne()

            self.doAfterDoCurAction(curHighestAction, doActionPlayer)

        return True

    def highestActionIsHu(self):
        """
        最高级的action是否是胡，用于增加新action的时候使用
        """
        return True

    def existHigherSide(self, player, action):
        """
        不能一炮多响时，判断是否存在更高优先级的边
        """
        sides = self.curAction2PlayerNtiles[action].keys()
        log(u'[existHigherSide] sides[%s].'%(sides), LOG_LEVEL_RELEASE)
        discardSide = self.lastOperateSide
        myPriority = self._getPriority4Side(discardSide, player.chair)
        log(u'[existHigherSide] sides[%s] myPriority[%s] discardSide[%s].'\
            %(sides, myPriority, discardSide), LOG_LEVEL_RELEASE)
        for _side in sides:
            if self._getPriority4Side(discardSide, _side) > myPriority:
                return True
        return False

    def existHigherSide4End(self, side, action):
        """
        action执行结束，用于判断是否最高级action中的最优先side
        """
        sides = self.curActionedPlayerDatas.keys()
        for _side in sides[:]:
            if self.curActionedPlayerDatas[_side][0] != action:
                sides.remove(_side)
        log(u'[existHigherSide4End] sides[%s].'%(sides), LOG_LEVEL_RELEASE)
        discardSide = self.lastOperateSide
        myPriority = self._getPriority4Side(discardSide, side)
        log(u'[existHigherSide4End] sides[%s] myPriority[%s] discardSide[%s].'\
            %(sides, myPriority, discardSide), LOG_LEVEL_RELEASE)
        for _side in sides:
            if self._getPriority4Side(discardSide, _side) > myPriority:
                return True
        return False

    def getTileList(self, player, kongTile):
        return ['','','','']

    def getHuTileList(self, player, tileList):
        handTiles = copy.deepcopy(player.handleMgr.getTiles())
        #未doaction所以需要移除
        if player.handleMgr.tmpSide == -1:
            handTiles.remove(tileList[0])
        return handTiles

    def _getPriority4Side(self, discardSide, side):
        """
        不能一炮多响时，获取边的优先级
        """
        return (discardSide - side)%self.maxPlayerCount

    def doHuMoreThanOne(self):
        pass

    def getNexter(self, curPlayer):
        """
        返回curPlayer的下一家
        """
        return self.players[(curPlayer.chair+1)%self.maxPlayerCount]

    def getPlayerAllowActionsByDiscard(self, curPlayer, player):
        """
        根据当前出牌玩家得到某玩家允许的操作列表
        """
        nexter = self.getNexter(curPlayer)
        if player is nexter:
            return self.ruleAllowActions
        else:
            return self.ruleAllowActions[:]

    def sendDissolveResult(self, player):
        """
        发送解散投票结果
        """
        resp = mahjong_pb2.S_C_DissolveVote()
        for otherPlayer in self.getPlayers():
            voteData = resp.vote.add()
            side = otherPlayer.chair
            if self.dissolve[side] != None:
                voteData.result = self.dissolve[side]
            voteData.nickname = otherPlayer.nickname
        resp.nickname =  self.players[self.dissolvePlayerSide].nickname
        resp.dissolveSide = self.dissolvePlayerSide
        resp.waitTime = max(int((self.dissovedCounterMs - self.server.getTimestamp()) / 1000), 0)
        self.sendAll(resp)

    def setPlayerCopy(self, robot, player):
        """
        设置拷贝了玩家数据的机器人
        """
        robot.game = self
        robot.handleMgr = player.handleMgr
        robot.handleMgr.player = robot
        robot.account = player.account
        robot.nickname = player.nickname
        robot.chair = player.chair
        robot.ip = player.ip
        robot.region = player.region
        robot.sex = player.sex
        robot.headImgUrl = player.headImgUrl
        robot.uid = player.uid
        robot.lastOnlineState = player.lastOnlineState
        robot.isOnline = player.isOnline

        robot.totalGameScore = player.totalGameScore
        robot.totalKongCount = player.totalKongCount
        robot.totalConcealedKongCount = player.totalConcealedKongCount
        robot.totalBeKongCount = player.totalBeKongCount
        robot.totalGiveHuCount = player.totalGiveHuCount
        robot.totalOtherHuCount = player.totalOtherHuCount
        robot.totalSelfHuCount = player.totalSelfHuCount

        robot.curGameScore = player.curGameScore

        if player.controlPlayer != player:
            robot.controlPlayer = player.controlPlayer
        if self.dealer == player:
            self.dealer = robot
        self.players[player.chair] = robot
        if player in self.curActioningPlayers:
            self.curActioningPlayers.remove(player)
            self.curActioningPlayers.append(robot)
        if self.beGrabKongHuPlayer is player:
            self.beGrabKongHuPlayer = robot

#++++++++++++++++++++ 通用麻将工具函数 end ++++++++++++++++++++

#++++++++++++++++++++ 通用房间服务工具 ++++++++++++++++++++
    def sendOne(self, player, protocol_obj):
        if player.chair not in self.exitPlayers:
            log(u'[try send]account[%s]'%(player.nickname), LOG_LEVEL_RELEASE)
            self.server.sendOne(player, protocol_obj)
        self.saveSendData(protocol_obj, peer = player)

    def sendExclude(self, excludePlayers, protocol_obj):
        log(u'[try send]game[%s] exit player %s'%(self.roomId, self.exitPlayers), LOG_LEVEL_RELEASE)
        self.server.send(self.getOnlinePlayers(excludePlayers), protocol_obj)
        # self.server.send([p for p in self.__getPlayers() if p not in excludePlayers], protocol_obj)

    def sendAll(self, protocol_obj):
        log(u'[try send]game[%s] exit player %s'%(self.roomId, self.exitPlayers), LOG_LEVEL_RELEASE)
        self.server.send(self.getOnlinePlayers(), protocol_obj)
        self.saveSendData(protocol_obj)

    def saveSendData(self, protocol_obj, peer = None): #保存发包
        name = protocol_obj.__class__.__name__
        code = self.server.senderMgr._cmds[name].msg_code
        data = protocol_obj.SerializeToString()

        saveResp = replay4proto_pb2.ActionData()
        saveResp.msgCode = code
        saveResp.replayMessage = data
        saveResp.timestamp = self.server.getTimestamp()

        if name in self.saveSendAllProtoList:
            self.replayData.append(saveResp)
        elif name == SAVE_SEND_END_PROTO:
            protoCopy = copy.deepcopy(protocol_obj)
            protoLen = len(protoCopy.gameUserDatas)
            for index in xrange(protoLen):
                protoCopy.gameUserDatas.remove(protoCopy.gameUserDatas[protoLen - 1 - index])
            saveResp.replayMessage = protoCopy.SerializeToString()
            self.replayData.append(saveResp)
        elif peer and name in SAVE_SEND_PROC_PROTO_LIST:
            if not self.replayinitTilesData: #标记发牌时间
                self.replayData.append(saveResp)
            resp = replay4proto_pb2.TilesData()
            resp.side = peer.chair
            resp.tiles = data
            self.replayinitTilesData.append(resp)
        elif peer and name in self.saveSendOneProtoList and (peer.chair in self.countPlayerSides):
            self.replayData.append(saveResp)

    def getEmptyChair(self):
        """
        return an empty side range[0:maxPlayerCount-1]
        return -1 for full
        """
        for chair, player in enumerate(self.players):
            if not player:
                return chair

        return consts.SIDE_UNKNOWN

    def getOnlinePlayers(self, excludePlayers=()):
        return [player for player in self.players if (player and player not in excludePlayers and player.chair not in self.exitPlayers)]

    def getPlayers(self, excludePlayers=()):
        return [player for player in self.players if (player and player not in excludePlayers)]

    def getPlayers2sides(self, players = ()):
        sides = []
        for player in players:
            sides.append(player.chair)
        return sides

    def setCounter(self, countPlayers, timeMs, timeoutCallback, params = ()):
        """
        设置当前计时器及超时回调
        """
        log(u'[set counter]countPlayers[%s] timeMs[%s] timeoutCallback[%s] params[%s].'\
                    %(countPlayers, timeMs, timeoutCallback.__name__, params), LOG_LEVEL_RELEASE)
        self.countPlayerSides = countPlayers
        self.countStartTime = self.server.getTimestamp()
        self.counterMs = timeMs
        self.counterCallback = timeoutCallback
        self.counterParams = params

    def doCounter(self, timestamp):
        """
        倒计时处理
        """
        if self.counterCallback and timestamp - self.countStartTime > self.counterMs:
            countStartTime = self.countStartTime
            log(u'[do counter]room[%s] counterCallback[%s] counterParams[%s].'\
                    %(self.roomId, self.counterCallback.__name__, self.counterParams), LOG_LEVEL_RELEASE)
            self.counterCallback(*self.counterParams)
            #倒计时变更则增加了新计时器，不重置
            if countStartTime == self.countStartTime:
                self.__resetCounter()

    def __resetCounter(self):
        """
        重置倒计时
        """
        self.counterCallback = None
        self.countStartTime = 0
        self.counterMs = None
        self.counterParams = None
        # self.dealer = None

    def checkCounter(self, player):
        """
        """
        if player.chair not in self.countPlayerSides:
            log(u'[check counter][error]error counter[%s] need counter[%s].'%(player.chair, self.countPlayerSides), LOG_LEVEL_RELEASE)
            return False
        return True

    def checkStage(self, stage):
        """
        """
        if self.stage != stage:
            log(u'[check stage][error]error stage[%s] need stage[%s].'%(self.stage, stage), LOG_LEVEL_RELEASE)
            return False
        return True

    def onTick(self, timestamp):
        """
        房间服务心跳
        """
        #倒计时及回调触发
        self.doCounter(timestamp)
        self.dealPing(timestamp)

        if self.dissovedCounterMs and timestamp > self.dissovedCounterMs:
            self.onDissolveVoteTimeout()
            self.dissovedCounterMs = 0

        if self.stage == WAIT_START and not self.ownner:
            if self.players[OWNNER_SIDE] and self.players[OWNNER_SIDE].isOnline == False:
                if not self.dissoved4GameNotStartMs:
                    self.dissoved4GameNotStartMs = self.server.getTimestamp()
                waitingTime = PUBLIC_ROOM_GAME_NOT_START_END_TIME
                if self.isHidden:
                    waitingTime = GAME_NOT_START_END_TIME
                if self.server.getTimestamp() - self.dissoved4GameNotStartMs > waitingTime:
                    if OWNNER_SIDE not in self.exitPlayers:
                        messsageStr = '长时间未开始游戏，房间已自动解散'.decode('utf-8')
                        self.players[OWNNER_SIDE].drop(messsageStr, type = 2)
                    log(u'[on tick]room[%s] ownner leave game too long.'%(self.roomId), LOG_LEVEL_RELEASE)
                    self.endGame(isNotStart = True)
            else:
                self.dissoved4GameNotStartMs = 0
        elif self.ownner:
            if self.playerCount == 0:
                waitingTime = PUBLIC_ROOM_GAME_NOT_START_END_TIME
                if self.isHidden:
                    waitingTime = OTHER_TYPE_GAME_NOT_START_END_TIME
                if not self.dissoved4GameNotStartMs:
                    self.dissoved4GameNotStartMs = self.server.getTimestamp()
                    self.server.saveOtherRoomEndTime(self, self.dissoved4GameNotStartMs + waitingTime)
                if self.server.getTimestamp() - self.dissoved4GameNotStartMs > waitingTime:
                    log(u'[on tick]room[%s] nobody too long.'%(self.roomId), LOG_LEVEL_RELEASE)
                    self.server.removeOtherGameData(self)
                    self.endGame(isNotStart = True)
            else:
                self.dissoved4GameNotStartMs = 0

    def dealPing(self, timestamp):
        """
        """
        for player in self.players:
            if not player:
                continue
            #log(u'[dealPing start] account[%s] isOnline[%s] lastOnlineState[%s]'%(player.nickname, player.isOnline,player.lastOnlineState), LOG_LEVEL_RELEASE)
            if timestamp - player.lastPingTimestamp > PING_INTERVAL_TICK:
                player.isOnline = False
            if player.isOnline != player.lastOnlineState:
                resp = mahjong_pb2.S_C_OnlineState()
                resp.changeSide = player.chair
                resp.isOnline = player.isOnline
                self.sendExclude((player,), resp)
                player.lastOnlineState = player.isOnline
                #log(u'[dealPing] side[%s] isOnline[%s]'%(resp.changeSide, resp.isOnline), LOG_LEVEL_RELEASE)

#++++++++++++++++++++ 通用房间服务工具 end ++++++++++++++++++++

#++++++++++++++++++++ 房间服务可重写接口 ++++++++++++++++++++

    def getDiscardCounterMs(self):
        """
        出牌倒计时(毫秒)，需要则重写
        """
        return WAIT_BACK_TIME

    def getDiceCounterMs(self):
        """
        打骰倒计时(毫秒)，需要则重写
        """
        return 1

    def getActionCounterMs(self):
        """
        吃碰杠胡倒计时(毫秒)，需要则重写
        """
        return WAIT_BACK_TIME

    def getBalanceCounterMs(self):
        """
        结算倒计时(毫秒)，需要则重写
        """
        return WAIT_BACK_TIME

    def getDissolvedCounterMs(self):
        """
        解散倒计时(毫秒)，需要则重写
        """
        return 5 * 60 * 1000

    def getMaxPlayerCount(self):
        """
        返回房间最大玩家数，上层可重写
        """
        return 4

    def getGameTotalCount(self):
        """
        返回默认最大小局数
        """
        return 8

    def getMaxDiceCount(self):
        """
        返回骰子数，上层可重写
        """
        return 2

    def getDissolveSuccedNeedPlayerCount(self):
        """
        同意人数满足，解散成功
        """
        return self.maxPlayerCount - self.getDissolveFailNeedPlayerCount()

    def getDissolveFailNeedPlayerCount(self):
        """
        不同意人数满足，解散失败
        默认值为房间人数减去解散成功需要的人数
        """
        return max(self.maxPlayerCount / 2 + self.maxPlayerCount % 2 - 1, 1)

    def initByRuleParams(self, ruleParams):
        """
        Abstract interface for parse rule parameters
        """
        params = eval(ruleParams)

        totalCount = int(params[-3])
        if totalCount:
            self.gameTotalCount = totalCount
            self.ruleDescs.append("%s局"%(self.gameTotalCount))

        self.needRoomCards = int(params[-2])
        self.baseScore = max(int(params[-1]), 1)
        self.ruleDescs.append("底分%s"%(self.baseScore))

        self.ruleDescs = "-".join(self.ruleDescs).decode('utf-8')

        log(u'[get gameRules]room[%s] ruleParams[%s] ruleTxt[%s]'%(self.roomId, params, self.ruleDescs),LOG_LEVEL_RELEASE)

    def getDicePoint(self):
        """
        返回骰子点数列表
        获得随机的打骰子点数
        """
        self.dicePoints = [random.randint(1, 6) for i in xrange(self.maxDiceCount)]
        return self.dicePoints

    def getDealer(self, dicePoints):
        """
        返回庄家座位号
        根据骰子点数确定庄家(可重写，未必与点数相关)
        """
        if self.curGameCount == 1:
            dealerSide = OWNNER_SIDE
        else:
            dealerSide = self.dealMgr.getDealerByGM()
            if dealerSide == -1:
                dealerSide = (sum(dicePoints)/4)%self.maxPlayerCount
        return dealerSide

    def getSpecialTile(self):
        """
        返回每小局游戏会一张特殊牌(一般为类似鬼牌这样的变牌标识)
        返回None则表示本局无特殊牌
        """
        return None

    def getDealManager(self):
        """
        返回发牌器
        """
        return DealMgr(self)

    def getRobot(self):
        """
        获得使用的玩家类，用于设置掉线后放置玩家的拷贝
        """
        return CommonPlayer()

    def getSaveSendAllProtoList(self):
        """
        获得需要保存回放的sendAll的协议列表
        """
        return []

    def getSaveSendOneProtoList(self):
        """
        获得需要保存回放的sendOne的协议列表
        只保存当前行动玩家的，比如S_C_DrawTiles只会保存发给摸牌的那个人的那条，不会保存发给别人的那条
        """
        return []

    def getActionedTiles(self, resp, side, curPlayerSide):
        """
        返回玩家已有操作的数据抽象，用于重连刷新
        """
        action2balanceTiels = self.players[side].handleMgr.action2balanceTiels
        getBalanceTiles = self.players[side].handleMgr.getBalanceTiles()

        data = resp.add()
        data.tiles.extend(self.players[side].handleMgr.getDiscardTiles()) #出过的牌的列表

        tiles2NumList = copy.deepcopy(self.players[side].handleMgr.tiles2NumList)

        data = resp.add()
        chowTiles = copy.deepcopy(action2balanceTiels[CHOW])
        for index, tiles in enumerate(chowTiles):
            chowTiles[index] = tiles + ';%s'%(tiles2NumList[tiles][0])
            tiles2NumList[tiles].remove(tiles2NumList[tiles][0])
        data.tiles.extend(chowTiles) #吃过的牌的列表

        data = resp.add()
        pongTiles = copy.deepcopy(action2balanceTiels[PONG])
        for index, tiles in enumerate(pongTiles):
            pongTiles[index] = tiles + ';%s'%(tiles2NumList[tiles][0])
            tiles2NumList[tiles].remove(tiles2NumList[tiles][0])
        data.tiles.extend(pongTiles) #碰过的牌的列表

        data = resp.add()
        kongTiles = copy.deepcopy(action2balanceTiels[OTHERS_KONG])
        kongTiles.extend(self.players[side].handleMgr.selfKongSideNTile)
        for index, tiles in enumerate(kongTiles):
            kongTiles[index] = tiles + ';%s'%(tiles2NumList[tiles][0])
            tiles2NumList[tiles].remove(tiles2NumList[tiles][0])
        data.tiles.extend(kongTiles) #杠过的牌的列表

        data = resp.add()
        if side != curPlayerSide:
            tileList = copy.deepcopy(action2balanceTiels[CONCEALED_KONG])
            for index, tiles in enumerate(tileList):
                tileSide, tileData = tiles.split(';')
                tileData = self.getTileList(self.players[side], tileData.split(',')[-1])
                tileData = ','.join(tileData)
                tileSideNData = '%s;%s'%(tileSide, tileData)
                tileList[index] = tileSideNData + ';%s'%(tiles2NumList[tiles][0])
                tiles2NumList[tiles].remove(tiles2NumList[tiles][0])
        else:
            tileList = copy.deepcopy(action2balanceTiels[CONCEALED_KONG])
            for index, tiles in enumerate(tileList):
                tileList[index] = tiles + ';%s'%(tiles2NumList[tiles][0])
                tiles2NumList[tiles].remove(tiles2NumList[tiles][0])
        data.tiles.extend(tileList) #暗杠过的牌的列表

        data = resp.add()
        data.tiles.extend(self.players[side].handleMgr.getFlowerTiles()) #补过的花的列表

        data = resp.add()
        if side != curPlayerSide:
            tiles = [''] * len(self.players[side].handleMgr.getTiles())
        else:
            tiles = copy.deepcopy(self.players[side].handleMgr.getTiles())
            lastTile = self.players[side].handleMgr.lastTile
            if lastTile and lastTile in tiles:
                tiles.remove(lastTile)
                tiles.append(lastTile)
        data.tiles.extend(tiles) #手牌列表

        return resp

    def setSpecialTile(self, specialTile):
        """
        设置特殊牌，若self.specialTileIsGhost()为True则自动设置鬼牌
        """
        self.specialTile = specialTile

        if self.specialTile and self.specialTileIsGhost():
            for player in self.getPlayers():
                player.handleMgr.setGhost(specialTile)

    def doAfterRoomFull(self):
        """
        人满后操作
        """
        pass

    def doBeforeRollDice(self):
        """
        """
        pass

    def doAfterRollDice(self):
        """
        """
        self.deal()

    def doBeforeGameStart(self):
        """
        """
        pass

    def doAfterGameStart(self):
        """
        """
        self.onSetStart(self.players[OWNNER_SIDE])
        # self.setCounter([OWNNER_SIDE], self.balanceCounterMs, self.onSetStart, [self.players[OWNNER_SIDE]])

    def doBeforeSetStart(self):
        """
        """
        pass

    def doAfterSetStart(self):
        """
        """
        # self.setCounter([self.dealer.chair], self.diceCounterMs, self.onDiceTimeout)
        self.server.saveSetStartData(self)
        self.countPlayerSides = [self.dealer.chair]
        self.onRollDice(self.dealer)

    def doAfterDeal(self):
        """
        """
        self.drawTile(self.dealer)
        
    def doAfterDrawTile(self, drawPlayer):
        """
        {
            chow:['a1,a3', 'a3,a4'],
            pong:['b2'],
            kong:['b2','b3'],
            cancelKong:['b2', 'b3'],
            hu:['b2', 'b3'],
        }
        """

        actionNtiles = drawPlayer.handleMgr.getAllowActionNTiles(self.getAllowActions4Draw())
        self.resetCurAction()
        self.addCurAction(drawPlayer, actionNtiles)

        self.nextProc(drawPlayer, True)

    def onDrawTile(self, player, drawData):
        """
        
        """
        #inOuts.in.append(self.dealMgr.getTile())

        tiles = None
        while 1:
            flowerTiles = player.handleMgr.getFlowerList()
            drawCount = player.handleMgr.getNeedTileCount()
            try:
                tiles = [self.dealMgr.getTile(player.chair) for i in xrange(drawCount)]
            except:
                tiles = self.dealMgr.tiles
            if not tiles and not flowerTiles:
                log(u'[try draw tile]room[%s] account[%s] draw end drawCount[%s].'%(self.roomId, player.nickname, drawCount), LOG_LEVEL_RELEASE)
                break
            player.handleMgr.doAddTiles(tiles)

            inOuts = drawData.add()
            inOuts.inTiles.extend(tiles)
            inOuts.outTiles.extend(flowerTiles)
            log(u'[try draw tile]room[%s] account[%s] inTiles%s inOuts%s tiles%s.'\
                    %(self.roomId, player.nickname, tiles, flowerTiles, player.handleMgr.getTiles()), LOG_LEVEL_RELEASE)

    def initDoActionDict(self):
        """
        """
        self.doActionDict = {
            HU                :      self.dealHu,
            CHOW              :      self.dealChow,
            PONG              :      self.dealPong,
            OTHERS_KONG       :      self.dealOthersKong,
            SELF_KONG         :      self.dealSelfKong,
            CONCEALED_KONG    :      self.dealConcealedKong,
            NOT_GET           :      self.dealNotGet,
        }
        
    def dealHu(self, action, player):
        if self.endGameWhenHu():
            self.lastHuSide = player.chair
            self.balance()
            return
        self.nextProc(player)

    def dealChow(self, action, player):
        self.nextProc(player, True)

    def dealPong(self, action, player):
        self.nextProc(player, True)

    def dealOthersKong(self, action, player):
        self.drawTile(player)
        
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
    
    def dealConcealedKong(self, action, player):
        self.drawTile(player)
    
    def dealNotGet(self, action, player):
        if self.beGrabKongHuPlayer:
            self.countPlayerSides = [self.beGrabKongHuPlayer.chair]
            self.drawTile(self.beGrabKongHuPlayer)
            return
        if player.handleMgr.lastTile:
            self.nextProc(player, True)
            return

        self.nextProc(self.players[self.lastDiscardSide])

    def doAfterDoCurAction(self, curHighestAction, doActionPlayer):
        log(u'[doAfterDoCurAction] room[%s] action[%s] doActionPlayer[%s].'\
        %(self.roomId, curHighestAction, doActionPlayer), LOG_LEVEL_RELEASE)

        self.doActionDict[curHighestAction](curHighestAction, doActionPlayer)

    def doAfterReadyHand(self, player):
        """
        听牌后操作
        """
        pass

    def onDiceTimeout(self):
        """
        """
        dealer = self.players[self.countPlayerSides[0]]
        self.onRollDice(dealer)

    def onDoActionTimeout(self):
        """
        """
        return
        # for side in self.countPlayerSides:
            # player = self.players[side]
            # self.onDoAction(player, NOT_GET, [])

    def onDiscardTimeout(self, player):
        """
        """
        return
        self.onDiscard(player, player.handleMgr.getLastTile())

    def onDissolveVoteTimeout(self):
        """
        """
        for player in self.getPlayers():
            self.onDissolveVote(player, True)

    def onGameStartTimeout(self):
        """
        """
        self.onGameStart(self.players[OWNNER_SIDE])

    def getAllowActions4Draw(self):
        """
        返回游戏规则在摸牌时允许的麻将操作tuple
        """
        actions = [SELF_KONG, CONCEALED_KONG, HU]
        #无牌可摸的情况下，可能需要将杠排除到允许actions之外
        if self.dealMgr.isDraw():
            if not self.canKong4NotTile():
                actions.remove(SELF_KONG)
                actions.remove(CONCEALED_KONG)
        return actions

    def getAllowActions4Discard(self, curPlayer, player):
        """
        返回游戏规则在别人出牌时允许的麻将操作tuple
        """
        actions = [CHOW, PONG, OTHERS_KONG, HU]
        #无牌可摸的情况下，可能需要将杠排除到允许actions之外
        if self.dealMgr.isDraw():
            if not self.canKong4NotTile():
                actions.remove(OTHERS_KONG)

        nexter = self.getNexter(curPlayer)
        if nexter is not player:
            actions.remove(CHOW)

        return actions

    def getPartyRoomRule(self):
        """
        娱乐模式规则
        """
        return []

    def canKong4NotTile(self):
        """
        规则定义，无牌可摸后是否仍允许杠
        """
        return False

    def canHuMoreThanOne(self):
        """
        是否允许一炮多响
        """
        return False

    def canGrabKongHu(self):
        """
        是否允许抢杠胡
        """
        return False

    def doGrabKongHu(self, huPlayer, beGrabPlayer):
        """
        抢杠胡的操作
        """
        log('[doGrabKongHu_1] huPlayer[%s] beGrabPlayer[%s]'%(huPlayer.nickname, beGrabPlayer),LOG_LEVEL_RELEASE)
        huPlayer.handleMgr.isGrabKongSide = beGrabPlayer.chair
        kongTile = self.grabKongTile

        selfKongTiles = beGrabPlayer.handleMgr.selfKongTiles
        pongTiles = beGrabPlayer.handleMgr.pongTiles
        kongTiles = beGrabPlayer.handleMgr.kongTiles
        action2balanceTiels = beGrabPlayer.handleMgr.action2balanceTiels
        selfKongSideNTile = beGrabPlayer.handleMgr.selfKongSideNTile

        bePongSide = beGrabPlayer.handleMgr.pongTile2Side[kongTile]
        beKongPlayer = self.players[bePongSide]
        beKongTiles = beKongPlayer.handleMgr.beKongTiles

        log('[doGrabKongHu_2] selfKongTiles[%s] pongTiles[%s] kongTiles[%s] action2balanceTiels[%s] beKongTiles[%s] selfKongSideNTile[%s]'%(selfKongTiles, pongTiles, kongTiles, action2balanceTiels, beKongTiles, selfKongSideNTile),LOG_LEVEL_RELEASE)

        if kongTile not in pongTiles:
            pongTiles.append(kongTile)
        if kongTile in selfKongTiles:
            selfKongTiles.remove(kongTile)
        if kongTile in kongTiles:
            kongTiles.remove(kongTile)

        _tiles = [kongTile]
        pongTilesData = self._dealTilesData(bePongSide, _tiles, beGrabPlayer, PONG)
        kongTilesData = self._dealTilesData(beGrabPlayer.chair, _tiles, beGrabPlayer, SELF_KONG)
        selfTilesData = self._dealTilesData(bePongSide, _tiles, beGrabPlayer, SELF_KONG)
        if pongTilesData not in action2balanceTiels[PONG]:
            action2balanceTiels[PONG].append(pongTilesData)
        if kongTilesData in action2balanceTiels[SELF_KONG]:
            action2balanceTiels[SELF_KONG].remove(kongTilesData)
        if selfTilesData in selfKongSideNTile:
            selfKongSideNTile.remove(selfTilesData)

        if kongTile in beKongTiles:
            beKongTiles.remove(kongTile)

        log('[doGrabKongHu_3] selfKongTiles[%s] pongTiles[%s] kongTiles[%s] action2balanceTiels[%s] beKongTiles[%s] selfKongSideNTile[%s]'%(selfKongTiles, pongTiles, kongTiles, action2balanceTiels, beKongTiles, selfKongSideNTile),LOG_LEVEL_RELEASE)

    def _dealTilesData(self, side, tileList, player, action):
        tiles = player.handleMgr.packActionTiles(action, tileList)
        tileData = ','.join(tiles)
        tilesData = '%s;%s'%(side, tileData)
        return tilesData

    def specialTileIsGhost(self):
        """
        是否特殊牌就是鬼牌
        """
        return True

    def doHuMoreThanOn(self):
        """
        一炮多响时需要做的处理
        """
        pass

    def endGameWhenHu(self):
        """
        胡牌是否即刻结束并结算游戏
        """
        return True

    def fillBalanceData(self, player, balanceData):
        """
        填充玩家小局结算数据，详见mahjong.proto中BalanceData中的
        desc
        score
        times
        tiles
        """
        balanceData.descs.extend([])
        balanceData.score = 0
        balanceData.tiles.extend([])
        balanceData.isHu = False

    def fillTotalBalanceData(self, player, balanceData):
        """
        填充玩家总结算数据，详见mahjong.proto中BalanceData中的
        score
        times
        """
        balanceData.score = 0
        balanceData.descs.extend([])

    def calcBalance(self, player):
        """
        每小局结算算分接口
        """
        pass

    def doBeforeBalance(self):
        """
        结算前重写逻辑
        """
        pass

#++++++++++++++++++++ 房间服务可重写接口 end ++++++++++++++++++++
