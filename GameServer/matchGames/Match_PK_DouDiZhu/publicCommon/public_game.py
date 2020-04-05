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
from common.pb_utils import *
from common.protocols.poker_consts import *
from common import poker_pb2, baseProto_pb2
from publicCommon import common_pb2
from .configs import *
from .time_config import *
import timer
from publicCommon.logger_mgr import g_logger, e_logger

import copy
import traceback


class PublicGame(CommonGame):
    def __init__(self, server, ruleParams, needInit=True, roomId=0):
        self.timerMgr = self.getTimer()
        super(PublicGame, self).__init__(server, ruleParams, needInit=needInit, roomId=roomId)

    def logger(self, str, level='info'):
        try:
            if level == 'info':
                g_logger.info(u'[%s] %s' % (self.roomId, str))
            elif level == 'error':
                e_logger.info(u'[%s] %s' % (self.roomId, str))
            else:
                print(u'[%s] %s' % (self.roomId, str))
        except:
            traceback.print_exc()
            print(u'[Room:%s] %s' % (self.roomId, str))

    def resetSetData(self):
        super(PublicGame, self).resetSetData()
        self.timerMgr.reset_timer()

    def getTimer(self):
        return timer.TimersMgr(self)

    def onTick(self, timestamp):
        self.timerMgr.check_timer()
        super(PublicGame, self).onTick(timestamp)

    def getMainTimerMs(self):
        '''主计时器的剩余时间'''
        if not self.timerMgr:
            return 0
        if not self.timerMgr.timer:
            return 0
        remain = self.timerMgr.timer.get_SurplusMS()
        if remain < 0:
            return 0
        return remain

    def getCountdownTime(self, player=None):
        if self.stage in [WAIT_START, GAME_READY]:
            return 99
        timer = self.timerMgr.timer
        if not timer:
            return 15
        callback = timer.callback
        interval = timer.get_SurplusMS()
        interval = interval if interval > 0 else 0
        if callback in self.CountdownCallbackFunc():
            return interval
        return 15

    def CountdownCallbackFunc(self):
        return [self.onAutoActionTimeOut, self.onDoActionTimeout]

    def getReadyPlayers(self, excludePlayers=()):
        return [player for player in self.players if (player and player not in excludePlayers and player.isReady)]

    def checkallready(self):
        if len(self.getReadyPlayers()) == self.maxPlayerCount:
            return True
        else:
            return False

    def DoReadyStart(self, player, result):
        if not self.checkStage(WAIT_START) or not isOpenReadyStart:
            return
        player.isReady = result
        resp = common_pb2.S_C_PlayerReadyResult()
        _player = resp.PlayerResult.add()
        _player.side = player.chair
        _player.result = result
        self.sendAll(resp)
        self.logger(u'[DoReadyStart] 玩家[%s][%s] 选择了 [%s] resp[%s]' % (player.nickname, player.chair, result, resp))
        self.logger(u'[DoReadyStart] 准备的玩家[%s]' % ([_player.chair for _player in self.getReadyPlayers()]))
        if self.checkallready():
            self.onGameStart(self.players[OWNNER_SIDE])

    def setPlayerCopy(self, robot, player):
        super(PublicGame, self).setPlayerCopy(robot, player)
        robot.isReady = player.isReady
        robot.isproxy = player.isproxy
        robot.Timer = player.Timer

    def onJoinGame(self, player, resp, isSendMsg=True):
        super(PublicGame, self).onJoinGame(player, resp, isSendMsg)
        if player.game.stage == WAIT_START and isOpenReadyStart:
            self.sendAllPlayerReadyResult(sendPlayer=player)

    def sendAllPlayerReadyResult(self, sendPlayer=None):
        ready_resp = common_pb2.S_C_PlayerReadyResult()
        for _player in self.getPlayers():
            player_info = ready_resp.PlayerResult.add()
            player_info.side = _player.chair
            player_info.result = _player.isReady
        if sendPlayer:
            self.sendOne(sendPlayer, ready_resp)
            self.logger(u"[sendAllPlayerReadyResult] nickname[%s] room[%s] ready_resp[%s]" %
                        (sendPlayer.nickname, self.roomId, ready_resp))
        else:
            self.logger(u"[sendAllPlayerReadyResult] room[%s] ready_resp[%s]" % (self.roomId, ready_resp))
            self.sendAll(ready_resp)

    def balance(self, isEndGame=False, isSave=True):
        """
        结算并结束游戏
        """
        log(u'[on balance]room[%s] curGameCount[%s] gameTotalCount[%s] isEndGame[%s] isSave[%s].' \
            % (self.roomId, self.curGameCount, self.gameTotalCount, isEndGame, isSave), LOG_LEVEL_RELEASE)
        self.doBeforeBalance(isEndGame)
        if not self.setEndTime:
            self.setEndTime = self.server.getTimestamp()
        if not self.gameEndTime:
            self.gameEndTime = self.server.getTimestamp()

        if not self.isUseRoomCards and self.curGameCount == 1 and not self.isDebug and not self.isParty and isSave:
            self.server.useRoomCards(self)

        # 检测局数是否直接结束全部
        if self.curGameCount + 1 > self.gameTotalCount:
            log(u'[on balance]room[%s] curGameCount[%s] > gameTotalCount[%s].' \
                % (self.roomId, self.curGameCount, self.gameTotalCount), LOG_LEVEL_RELEASE)
            isEndGame = True

        # 打包小局数据
        resp = poker_pb2.S_C_Balance()
        resp.isNormalEndGame = self.isGameEnd
        if isSave:
            for player in self.getPlayers():
                self.calcBalance(player)

        if self.stage != GAME_READY:
            self.fillCommonData(resp)
        for player in self.getPlayers():
            if self.stage != GAME_READY:  # 局间不显示单局结算数据
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
        log(u'[on balance] resp[%s]' % (resp), LOG_LEVEL_RELEASE)
        self.sendAll(resp)

        # 每局数据存盘
        if isSave:
            self.server.savePlayerBalanceData(self, resp.setUserDatas)
            saveResp = poker_pb2.S_C_RefreshData()
            saveResp.result = True
            self.server.tryRefresh(self, player, saveResp)
            self.replayRefreshData = saveResp.SerializeToString()
            self.isSaveGameData = True
            self.gamePlayedCount += 1
        if isEndGame:
            if self.isSaveGameData:
                # 总数据存盘
                log(u'[on balance]room[%s] save all data.' % (self.roomId), LOG_LEVEL_RELEASE)
                self.server.savePlayerTotalBalanceData(self, resp.gameUserDatas)
            self.removeRoom()
        else:
            # 切换下一局
            self.resetSetData()
            self.isEnding = True
            self.stage = GAME_READY
            # self.onSetStart(self.players[OWNNER_SIDE])
            self.setCounter([self.dealerSide], self.balanceCounterMs, self.onGameStartTimeout)

    ####托管部分####
    def sendProxy(self, player):
        """
            发送托管状态
        """
        resp = common_pb2.S_C_Proxy()
        data = resp.data.add()
        data.side = player.chair
        data.isproxy = player.isproxy
        self.sendAll(resp)

    def sendProxyBro(self, player=None):
        """
            发送托管状态 广播
        """
        resp = common_pb2.S_C_Proxy()
        for _player in self.players:
            if not _player:
                continue
            data = resp.data.add()
            data.side = _player.chair
            data.isproxy = _player.isproxy
        if player:
            self.sendOne(player, resp)
            return
        self.sendAll(resp)

    def onProxy(self, player, isproxy):
        """
            托管
        """
        if self.stage in [WAIT_START, GAME_READY]:
            log(u'onProxy 当前游戏还没开始 {}'.format(self.stage), LOG_LEVEL_RELEASE)
            return
        log('onProxy', LOG_LEVEL_RELEASE)
        if isproxy == 0 and not player.isproxy:
            log(u'onProxy 玩家{}不在托管状态，不能取消'.format(player.chair), LOG_LEVEL_RELEASE)
            self.sendProxy(player)
            return
        elif isproxy == 1 and player.isproxy:
            log(u'onProxy 玩家{}已经是托管状态'.format(player.chair), LOG_LEVEL_RELEASE)
            self.sendProxy(player)
            return
        else:
            if isproxy:
                player.isproxy = True
            else:
                player.isproxy = False
        self.sendProxy(player)
        self.afterOnProxy(player)

    def afterOnProxy(self, player):
        """ 托管处理 """
        if not self.checkCounter(player):
            return

        if player.isproxy:
            obj_timer = self.timerMgr.getTimer(callback=self.onAutoActionProxy, overTime=getTime_Action_Proxy(),
                                               params=(player.chair, self.actionNum)
                                               , note='玩家(%s)设置托管action定时器' % (player.nickname))
            self.timerMgr.add_Timer(obj_timer, 1)
            player.Timer = obj_timer
        else:
            if player.Timer:
                self.timerMgr.del_timer(player.Timer, 1)
                player.Timer = None

    def doSendAllowActions(self, curPlayer):
        log(u'[doSendAllowActions] curPlayer[%s]' % (curPlayer.chair), LOG_LEVEL_RELEASE)
        super(PublicGame, self).doSendAllowActions(curPlayer=curPlayer)
        self.doSendAllowActions_midway(curPlayer)
        self.doSendAllowActions_finally(curPlayer)

    def doSendAllowActions_midway(self, curPlayer):
        if curPlayer.isproxy:
            obj_timer = self.timerMgr.getTimer(callback=self.onAutoActionProxy, overTime=getTime_Action_Proxy(),
                                               params=(curPlayer.chair, self.actionNum),
                                               note='[%s]托管自动操作' % (curPlayer.nickname))
            self.timerMgr.add_Timer(obj_timer, 1)

    def doSendAllowActions_finally(self, curPlayer):
        self.ActionMS = self.actionCounterMs
        self.ActionStartTime = self.server.getTimestamp()
        self.logger(u'[doSendAllowActions] 玩家[%s][%s]自动打牌' % (curPlayer.nickname, curPlayer.chair))
        obj_timer = self.timerMgr.getTimer(callback=self.onAutoActionTimeOut, overTime=getTime_Action(),
                                           params=(curPlayer.chair, self.actionNum),
                                           note='全局(%s)正常打牌' % (curPlayer.nickname))
        self.timerMgr.add_Timer(obj_timer, 0)

    def onAutoActionTimeOut(self, chair, actionNum):
        pass

    def onAutoActionProxy(self, chair, actionNum):
        '''Action超时处理(托管)'''
        pass

    def doBeforeBalance(self, isEndGame=False):
        if isEndGame:
            return
        pass

    def getBalanceCounterMs(self):
        """
        结算倒计时(毫秒)，需要则重写
        """
        return 15 * 1000

    def onDoAction(self, player, action, actionCards, num, Auto=False):
        """
        玩家操作
        """
        if not self.checkStage(GAMING):
            return

        side = player.chair
        if side != self.curActioningSide:
            log(u'[onDoAction][error]side[%s] is not curActioningSide[%s].' % (side, self.curActioningSide),
                LOG_LEVEL_RELEASE)
            return

        if num != self.actionNum:
            log(u'[onDoAction][error]error num[%s] for side[%s] player[%s], actionNum[%s].' \
                % (num, side, player.nickname, self.actionNum), LOG_LEVEL_RELEASE)
            return

        if Auto and not player.isproxy:
            player.isproxy = True
            self.sendProxy(player)
        elif not Auto and player.isproxy:
            self.onProxy(player, 0)

        self.doCurAction(player, action, actionCards)

    def getTimerNum(self):
        return self.roomId

    def getPlayersName(self, players):
        return ','.join([p.nickname for p in players])

    def sendOne(self, player, protocol_obj):
        name = protocol_obj.__class__.__name__
        self.logger(u'[sendOne] nickname[%s] =>[%s] %s' % (player.nickname, name, protocol_obj))
        if player.chair not in self.exitPlayers:
            self.server.sendOne(player, protocol_obj)
        self.saveSendData(protocol_obj, peer=player)

    def sendExclude(self, excludePlayers, protocol_obj):
        name = protocol_obj.__class__.__name__
        self.logger(u'[sendExclude] excludePlayers[%s] =>[%s] %s' %
                    (self.getPlayersName(excludePlayers), name, protocol_obj))
        self.server.send(self.getOnlinePlayers(excludePlayers), protocol_obj)

    def sendAll(self, protocol_obj):
        name = protocol_obj.__class__.__name__
        self.logger(u'[sendAll] =>[%s] %s' % (name, protocol_obj))
        self.server.send(self.getOnlinePlayers(), protocol_obj)
        self.saveSendData(protocol_obj)
