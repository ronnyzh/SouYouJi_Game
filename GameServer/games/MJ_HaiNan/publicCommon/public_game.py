# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: game logic
"""

from common.common_game import CommonGame, PING_INTERVAL_TICK
from common.card_define import *
from common.log import *
from common.pb_utils import *
from common.protocols.mahjong_consts import *
from common import mahjong_pb2
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
        return [self.onDiscardTimeout, self.onDoActionTimeout]

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

    def doCurAction(self, player, action, actionTiles, num, Auto=False):
        if action != NOT_GET and action not in self.curActions:
            log(u'[try do curAction][error]action[%s] not in curActions[%s].' % (action, self.curActions),
                LOG_LEVEL_RELEASE)
            return False

        if player not in self.curActioningPlayers:
            log(u'[try do curAction][error]player[%s] not in curActioningPlayers.' % (player.nickname),
                LOG_LEVEL_RELEASE)
            return False

        side = player.chair
        if side not in self.curAction2PlayerNtiles[action]:
            log(u'[try do curAction][error]side[%s] not in curAction2PlayerNtiles[%s].' \
                % (side, self.curAction2PlayerNtiles[action]), LOG_LEVEL_RELEASE)
            return False

        if side not in self.side2ActionNum or num != self.side2ActionNum[side]:
            log(u'[try do curAction][error]error num[%s] for side[%s] player[%s], side2ActionNum[%s].' \
                % (num, side, player.nickname, self.side2ActionNum), LOG_LEVEL_RELEASE)
            return False

        allowActionTiles = self.curAction2PlayerNtiles[action][side]

        # 判断操作的麻将是否在允许集合中
        if action and actionTiles not in allowActionTiles:
            log(u'[try do curAction][error]actionTiles[%s] not in allowActionTiles[%s].' % (
                actionTiles, allowActionTiles), LOG_LEVEL_RELEASE)
            return False

        if not Auto and player.isproxy:
            self.onProxy(player, 0)

        for _action in self.curAction2PlayerNtiles:
            if side in self.curAction2PlayerNtiles[_action]:
                del self.curAction2PlayerNtiles[_action][side]
                if _action in self.curActions:
                    self.curActions.remove(_action)
        log(u'[doCurAction]curAction2PlayerNtiles[%s] curActions[%s] num[%s].' \
            % (self.curAction2PlayerNtiles, self.curActions, num), LOG_LEVEL_RELEASE)
        self.curActionedPlayerDatas[side] = (action, actionTiles)
        existHigherAction = False
        if action >= self.curHighestAction:
            if self.highestActionIsHu() and self.curHighestAction == HU:
                pass
            else:
                self.curHighestAction = action

        # 是否存在当前确认操作的一样或更高的优先级
        if self.curActions:
            highestAction = self.curActions[-1]
        else:
            highestAction = 0
        if self.highestActionIsHu() and HU in self.curActions:
            highestAction = HU
        # 规则不允许一炮多响的话，即不存在同一优先级的等待，同一优先级只取最高的
        if self.canHuMoreThanOne():
            existHigherAction = self.curHighestAction <= highestAction
        else:
            existHigherAction = self.curHighestAction < highestAction  # 是否存在更高级的action
            if not existHigherAction:
                if self.curHighestAction != action:  # 是否存在还未执行最高级action的玩家
                    existHigherAction = bool(self.curAction2PlayerNtiles[self.curHighestAction])
                else:  # 是否同级里面存在更高优先级的顺位
                    existHigherAction = self.existHigherSide(player, action)
            # 清理
            if not existHigherAction:
                for _side in self.curActionedPlayerDatas.keys()[:]:
                    if self.curActionedPlayerDatas[_side][0] != self.curHighestAction or \
                            self.existHigherSide4End(_side, self.curHighestAction):
                        del self.curActionedPlayerDatas[_side]
        existHigherAction = existHigherAction and self.curAction2PlayerNtiles[highestAction]
        log(u'[doCurAction]existHigherAction[%s] curActions[%s].' \
            % (existHigherAction, self.curActions), LOG_LEVEL_RELEASE)

        # 最高优先的操作者>1的话，即为一炮多响
        topActionPlayerCount = 0
        doActionPlayer = player
        curHighestAction = NOT_GET
        ActionPlayers = []  # 记录action的对象
        if not existHigherAction:
            log(u'[doCurAction]curActionedPlayerDatas[%s].' \
                % (self.curActionedPlayerDatas), LOG_LEVEL_RELEASE)
            for chair, actionNtiles in self.curActionedPlayerDatas.iteritems():
                _action, tiles = actionNtiles
                if self.curHighestAction == _action:
                    curHighestAction = _action
                    doActionPlayer = self.players[chair]
                    if not _action:
                        resp = mahjong_pb2.S_C_DoAction()
                        resp.side = chair
                        actionObj = resp.action.add()
                        actionObj.action = NOT_GET
                        if doActionPlayer.handleMgr.tmpSide >= 0:
                            actionObj.beActionSide = doActionPlayer.handleMgr.tmpSide
                        self.sendOne(doActionPlayer, resp)
                        continue
                    resp = mahjong_pb2.S_C_DoAction()
                    resp.side = chair
                    if _action == CONCEALED_KONG:
                        copyResp = copy.deepcopy(resp)
                    actionObj = resp.action.add()
                    actionObj.action = _action
                    if doActionPlayer.handleMgr.tmpSide >= 0:
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

                    # 暗杠不显示给其他玩家
                    if _action == CONCEALED_KONG and False:
                        self.sendOne(doActionPlayer, resp)
                        tileList = self.getTileList(doActionPlayer, tileList[-1])
                        actionObj2 = copyResp.action.add()
                        actionObj2.action = _action
                        actionObj2.tiles.extend(tileList)
                        self.sendExclude((doActionPlayer,), copyResp)
                    else:
                        self.sendAll(resp)
                    log(u'[try do cur action]room[%s] player[%s] action[%s] handle[%s].' \
                        % (self.roomId, doActionPlayer.nickname, _action, doActionPlayer.handleMgr.tiles),
                        LOG_LEVEL_RELEASE)

                    doActionPlayer.doAction(_action, tiles.split(','))

                    topActionPlayerCount += 1
                    ActionPlayers.append(chair)
            self.resetCurAction()

            if topActionPlayerCount > 1 and len(ActionPlayers) > 1:
                self.doHuMoreThanOne(ActionPlayers)

            self.doAfterDoCurAction(curHighestAction, doActionPlayer)

        return True

    def balance(self, isDrawn=False, isEndGame=False, isSave=True, needSpecitile=True):
        """
        结算并结束游戏
        """
        log(u'[on balance]room[%s] curGameCount[%s] gameTotalCount[%s] isDrawn[%s] isEndGame[%s] isSave[%s].' \
            % (self.roomId, self.curGameCount, self.gameTotalCount, isDrawn, isEndGame, isSave), LOG_LEVEL_RELEASE)
        self.doBeforeBalance(isEndGame)
        if not self.setEndTime:
            self.setEndTime = self.server.getTimestamp()
        if not self.gameEndTime:
            self.gameEndTime = self.server.getTimestamp()

        if not self.isUseRoomCards and self.curGameCount == 1 and not self.isDebug and not self.isParty and isSave:
            self.server.useRoomCards(self)

        # 检测局数是否直接结束全部
        if self.curGameCount + 1 > self.gameTotalCount:
            log(u'[on balance]room[%s] curGameCount[%s] > gameTotalCount[%s].' % (
                self.roomId, self.curGameCount, self.gameTotalCount), LOG_LEVEL_RELEASE)
            isEndGame = True

        # 打包小局数据
        resp = mahjong_pb2.S_C_Balance()
        resp.isDrawn = isDrawn
        if needSpecitile and self.specialTile:
            resp.ghostTile = self.specialTile
        if isSave:
            for player in self.getPlayers():
                self.calcBalance(player)

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
        self.sendAll(resp)

        # 每局数据存盘
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
            self.setCounter([self.dealer.chair], self.balanceCounterMs, self.onGameStartTimeout)

    def getActionedTiles(self, resp, side, curPlayerSide):  # 重连暗杠翻牌
        """
        返回玩家已有操作的数据抽象，用于重连刷新
        """
        action2balanceTiels = self.players[side].handleMgr.action2balanceTiels
        getBalanceTiles = self.players[side].handleMgr.getBalanceTiles()

        data = resp.add()
        data.tiles.extend(self.players[side].handleMgr.getDiscardTiles())  # 出过的牌的列表

        tiles2NumList = copy.deepcopy(self.players[side].handleMgr.tiles2NumList)

        data = resp.add()
        chowTiles = copy.deepcopy(action2balanceTiels[CHOW])
        for index, tiles in enumerate(chowTiles):
            chowTiles[index] = tiles + ';%s' % (tiles2NumList[tiles][0])
            tiles2NumList[tiles].remove(tiles2NumList[tiles][0])
        data.tiles.extend(chowTiles)  # 吃过的牌的列表

        data = resp.add()
        pongTiles = copy.deepcopy(action2balanceTiels[PONG])
        for index, tiles in enumerate(pongTiles):
            pongTiles[index] = tiles + ';%s' % (tiles2NumList[tiles][0])
            tiles2NumList[tiles].remove(tiles2NumList[tiles][0])
        data.tiles.extend(pongTiles)  # 碰过的牌的列表

        data = resp.add()
        kongTiles = copy.deepcopy(action2balanceTiels[OTHERS_KONG])
        kongTiles.extend(self.players[side].handleMgr.selfKongSideNTile)
        for index, tiles in enumerate(kongTiles):
            kongTiles[index] = tiles + ';%s' % (tiles2NumList[tiles][0])
            tiles2NumList[tiles].remove(tiles2NumList[tiles][0])
        data.tiles.extend(kongTiles)  # 杠过的牌的列表

        data = resp.add()
        tileList = copy.deepcopy(action2balanceTiels[CONCEALED_KONG])
        for index, tiles in enumerate(tileList):
            tileList[index] = tiles + ';%s' % (tiles2NumList[tiles][0])
            tiles2NumList[tiles].remove(tiles2NumList[tiles][0])

        data.tiles.extend(tileList)  # 暗杠过的牌的列表

        data = resp.add()
        data.tiles.extend(self.players[side].handleMgr.getFlowerTiles())  # 补过的花的列表

        data = resp.add()
        if side != curPlayerSide:
            tiles = [''] * len(self.players[side].handleMgr.getTiles())
        else:
            tiles = copy.deepcopy(self.players[side].handleMgr.getTiles())
            lastTile = self.players[side].handleMgr.lastTile
            if lastTile and lastTile in tiles:
                tiles.remove(lastTile)
                tiles.append(lastTile)
        data.tiles.extend(tiles)  # 手牌列表
        return resp

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

        """ 托管处理 """
        if not self.checkCounter(player):
            return

        log(u'[onProxy] isproxy[%s] Timer %s' % (player.isproxy, player.Timer.__str__()), LOG_LEVEL_RELEASE)

        if player in self.curActioningPlayers:
            if player.isproxy:
                obj_timer = self.timerMgr.getTimer(callback=self.onAutoAction, overTime=getTime_Action_Proxy(),
                                                   params=(player.chair,)
                                                   , note='玩家(%s)设置托管action定时器' % (player.nickname))
                self.timerMgr.add_Timer(obj_timer, 1)
                player.Timer = obj_timer
            else:
                if player.Timer:
                    self.timerMgr.del_timer(player.Timer, 1)
                    player.Timer = None
        else:
            if player.isproxy:
                obj_timer = self.timerMgr.getTimer(callback=self.onAutoDiscardProxy, overTime=getTime_DisCard_Proxy(),
                                                   params=(player.chair,)
                                                   , note='玩家(%s)设置托管自动打牌定时器' % (player.nickname))
                self.timerMgr.add_Timer(obj_timer, 1)
                player.Timer = obj_timer
            else:
                if player.Timer:
                    self.timerMgr.del_timer(player.Timer, 1)
                    player.Timer = None

    def dealDrawTile(self, curPlayer):
        self.curPlayerSide = curPlayer.chair
        self.ActionMS = getTime_DisCard()
        self.ActionStartTime = self.server.getTimestamp()

        if curPlayer.isproxy:
            self.logger(u'[dealDrawTile] 托管打牌[%s]' % (curPlayer.handleMgr.getLastTile()))
            obj_timer = self.timerMgr.getTimer(callback=self.onAutoDiscardProxy, overTime=getTime_DisCard_Proxy(),
                                               params=(curPlayer.chair,), note='玩家(%s)托管打牌' % (curPlayer.nickname))
            self.timerMgr.add_Timer(obj_timer, 1)
            curPlayer.Timer = obj_timer

        obj_timer = self.timerMgr.getTimer(callback=self.onDiscardTimeout, overTime=getTime_DisCard(),
                                           params=(curPlayer.chair,), note='全部(%s)正常打牌' % (curPlayer.nickname))
        self.timerMgr.add_Timer(obj_timer, 0)

    def nextProc(self, curPlayer, isDrawTile=False):
        """
        打牌或摸牌后根据是否存在操作决定下一个流程
        """
        log(u'[next proc] curPlayer[%s] isDrawTile[%s].' % (curPlayer.nickname, isDrawTile), LOG_LEVEL_RELEASE)
        if self.curActioningPlayers:
            self.ActionMS = getTime_Action()
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
                self.drawTile(nexter)

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
        self.onDiscard(player, tile)

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
        self.onDiscard(player, tile)

    def onAutoActionProxy(self, side):
        '''Action超时处理(托管)'''
        player = self.players[side]
        if not player.isproxy or player not in self.curActioningPlayers:
            return
        if HU in self.curActions and player.chair in self.curAction2PlayerNtiles[HU] and \
                self.curAction2PlayerNtiles[HU][player.chair]:
            tile = self.curAction2PlayerNtiles[HU][player.chair][0]
            self.onDoAction(player, HU, tile, self.side2ActionNum[player.chair], Auto=True)
        else:
            self.onDoAction(player, NOT_GET, '', self.side2ActionNum[player.chair], Auto=True)

    def onAutoAction(self, side):
        player = self.players[side]
        if not player.isproxy or player not in self.curActioningPlayers:
            return
        if HU in self.curActions and player.chair in self.curAction2PlayerNtiles[HU] and \
                self.curAction2PlayerNtiles[HU][player.chair]:
            tile = self.curAction2PlayerNtiles[HU][player.chair][0]
            self.onDoAction(player, HU, tile, self.side2ActionNum[player.chair], Auto=True)
        else:
            self.onDoAction(player, NOT_GET, '', self.side2ActionNum[player.chair], Auto=True)

    def onDoActionTimeout(self):
        '''Action超时处理(默认)'''
        self.logger(u'[onDoActionTimeout] countPlayerSides[%s]' % (self.countPlayerSides))
        for side in self.countPlayerSides:
            player = self.players[side]
            if not self.side2ActionNum.has_key(side):
                self.logger(u'[onDoActionTimeout] Error side[%s] not in side2ActionNum[%s]' %
                            (side, self.side2ActionNum), level='error')
                continue
            self.onDoAction(player, NOT_GET, '', self.side2ActionNum[side], Auto=True)

    def doBeforeBalance(self, isEndGame=False):
        if isEndGame:
            return
        pass

    def getBalanceCounterMs(self):
        """
        结算倒计时(毫秒)，需要则重写
        """
        return 15 * 1000

    def onDoAction(self, player, action, actionTiles, num, Auto=False):
        """
        玩家操作(吃碰杠胡)
        """
        if not self.checkStage(GAMING):
            return

        if not self.checkCounter(player):
            return

        if not self.doCurAction(player, action, actionTiles, num, Auto):
            return

    def doHuMoreThanOne(self, ActionPlayers=None):
        pass

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

    def dealPing(self, timestamp):
        '''PING检测连通性'''
        for player in self.getPlayers():
            if timestamp - player.lastPingTimestamp > PING_INTERVAL_TICK:
                player.isOnline = False
            if player.isOnline != player.lastOnlineState:
                resp = mahjong_pb2.S_C_OnlineState()
                resp.changeSide = player.chair
                resp.isOnline = player.isOnline
                self.sendExclude((player,), resp)
                player.lastOnlineState = player.isOnline
                if not player.isOnline and player.chair not in self.exitPlayers:
                    self.onExitGame(player)
