# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: game logic
"""

from common.card_define import *
from common.log import *
from common.protocols.mahjong_consts import *
from player import Player
from deal import DealManager
import BloodRiver_mahjong_pb2
import copy
from common import mahjong_pb2
from publicCommon import timer
import random
from publicCommon.public_game import PublicGame
from publicCommon.time_config import *
from collections import Counter


class Game(PublicGame):

    def __init__(self, server, ruleParams, needInit=True, roomId=0):
        super(Game, self).__init__(server, ruleParams, needInit=needInit, roomId=0)
        self.huPlayerCount = 0
        self.huChairs = []
        self.checkLock = False
        self.setColorList = [i for i in range(self.maxPlayerCount)]
        self.colorSet = [''] * self.maxPlayerCount
        self.privateStatus = -1
        self.ds = -1
        self.multi_flag = False
        self.single_lock = False

    def resetSetData(self):
        '''每局数据初始化'''
        super(Game, self).resetSetData()
        self.huPlayerCount = 0
        self.huChairs = []
        self.checkLock = False
        self.setColorList = [i for i in range(self.maxPlayerCount)]
        self.colorSet = [''] * self.maxPlayerCount
        self.multi_flag = False
        self.single_lock = False
        self.privateStatus = -1

        # 呼叫转移记录
        self.callChangeKong = []

    def initByRuleParams(self, ruleParams):
        params = eval(ruleParams)

        self.fans = 0
        self.bt = None
        self.bt2 = None

        fans = params[0]  # 番
        if fans == 0:
            self.fans = 3
            self.ruleDescs.append("封顶3番")
        elif fans == 1:
            self.fans = 4
            self.ruleDescs.append("封顶4番")
        elif fans == 2:
            self.fans = 5
            self.ruleDescs.append("封顶5番")
        else:
            self.fans = 666
            self.ruleDescs.append("不封顶")

        bt = params[1]
        if bt == 1:
            self.bt = 0
            self.ruleDescs.append("自摸加底")
        else:
            self.bt = 1
            self.ruleDescs.append("自摸加番")

        bt2 = params[2]
        if bt2 == 0:
            self.bt2 = 0
            self.ruleDescs.append("点杠开(点炮)")
        else:
            self.bt2 = 1
            self.ruleDescs.append("点杠开(自摸)")

        checkbox = params[3]
        self.exchangeThree = False
        self.j19 = False
        self.mqzz = False
        self.tdHU = False
        if 0 in checkbox:
            self.exchangeThree = True
            self.ruleDescs.append("换三张")
        # if 1 in checkbox:
        #     self.j19 = True
        #     self.ruleDescs.append("幺九将对")
        # if 2 in checkbox:
        #     self.mqzz = True
        #     self.ruleDescs.append("门清中张")
        if 1 in checkbox:
            self.tdHU = True
            self.ruleDescs.append("天地胡")

        # huTypeBox = params[4]
        huTypeBox = range(0, 12)

        self.isCanHu_menqing = False
        if 0 in huTypeBox:
            # self.ruleDescs.append("门清")
            self.mqzz = True
            self.isCanHu_menqing = True

        self.isCanHu_zhongzhang = False
        if 1 in huTypeBox:
            # self.ruleDescs.append("中张")
            self.mqzz = True
            self.isCanHu_zhongzhang = True

        self.isCanHu_penghu = False
        if 2 in huTypeBox:
            # self.ruleDescs.append("碰碰胡")
            self.isCanHu_penghu = True

        self.isCanHu_qidui = False
        if 3 in huTypeBox:
            # self.ruleDescs.append("七对")
            self.isCanHu_qidui = True

        self.isCanHu_qingyise = False
        if 4 in huTypeBox:
            # self.ruleDescs.append("清一色")
            self.isCanHu_qingyise = True

        self.isCanHu_longqidui = False
        if 5 in huTypeBox:
            # self.ruleDescs.append("龙七对")
            self.isCanHu_longqidui = True

        self.isCanHu_quanyaojiu = False
        if 6 in huTypeBox:
            # self.ruleDescs.append("全幺九")
            self.j19 = True
            self.isCanHu_quanyaojiu = True

        self.isCanHu_jiangdui = False
        if 7 in huTypeBox:
            # self.ruleDescs.append("将对")
            self.j19 = True
            self.isCanHu_jiangdui = True

        self.isCanHu_qingpeng = False
        if 8 in huTypeBox:
            # self.ruleDescs.append("清碰")
            self.isCanHu_qingpeng = True

        self.isCanHu_qingqidui = False
        if 9 in huTypeBox:
            # self.ruleDescs.append("清七对")
            self.isCanHu_qingqidui = True

        self.isCanHu_jiangqidui = False
        if 10 in huTypeBox:
            # self.ruleDescs.append("将七对")
            self.isCanHu_jiangqidui = True

        self.isCanHu_qinglongqidui = False
        if 11 in huTypeBox:
            # self.ruleDescs.append("清龙七对")
            self.isCanHu_qinglongqidui = True

        super(Game, self).initByRuleParams(ruleParams)

    def getMaxPlayerCount(self):
        return 4

    def doAfterDeal(self):
        '''发牌后操作'''
        '''换三张'''
        self.logger('after deal')
        resp = BloodRiver_mahjong_pb2.S_C_ExchangeFlag()
        if self.exchangeThree:
            resp.flag = 1
            self.changeList = [i for i in range(self.maxPlayerCount)]
            self.changDict = {}
            self.privateStatus = 1
            obj_timer = timer.Timer(callback=self.AutoExchangeThree, overTime=getTime_AutoExchangeThree(),
                                    note='全局自动换三张')
            self.timerMgr.add_Timer(obj_timer, 0)
        else:
            resp.flag = 0
            self.privateStatus = 2
            obj_timer = timer.Timer(callback=self.AutoSetColor, overTime=getTime_AutoSetColor(), note='全局自动选缺')
            self.timerMgr.add_Timer(obj_timer, 0)
        self.sendAll(resp)

    def AutoExchangeThree(self):
        if self.privateStatus != 1:
            return
        for _player in self.getPlayers():
            if _player.chair in self.changeList:
                type_tiles = {}
                type_nums = {}
                for _tile in _player.handleMgr.tiles:
                    _type = getTileType(_tile)
                    type_tiles.setdefault(_type, [])
                    type_tiles[_type].append(_tile)
                for _type, _tiles in type_tiles.iteritems():
                    _len = len(_tiles)
                    if _len >= 3:
                        type_nums.setdefault(_len, [])
                        type_nums[_len].append(_type)
                nums_keys = type_nums.keys()
                nums_keys.sort()
                self.logger(u'[AutoExchangeThree] 玩家 nickname[%s] type_tiles[%s] type_nums[%s]' %
                            (_player.nickname, type_tiles, type_nums))
                type_key = random.choice(type_nums[nums_keys[0]])
                self.onExchangeThree(_player, random.sample(type_tiles[type_key], 3))

    def onExchangeThree(self, player, tiles):
        '''执行换3张操作'''
        self.logger(u'[onExchangeThree] nickname[%s] tiles[%s] tiles[%s]' %
                    (player.nickname, player.handleMgr.tiles, tiles))

        resp = BloodRiver_mahjong_pb2.S_C_PlayerExchangeThree()
        type_list = [_tile[0] for _tile in tiles]

        resp.side = player.chair
        resp.result = True
        if player.chair not in self.changeList:
            resp.result = False
            resp.reason = u'玩家已完成换3张操作,请勿重复操作'
            self.sendOne(player, resp)
            return
        elif len(set(type_list)) != 1:
            resp.result = False
            resp.reason = u'换3张的牌必须是同一种花色'
            self.sendOne(player, resp)
            return
        elif len(tiles) != 3:
            resp.result = False
            resp.reason = u'选择长度错误,请选择3张牌'
            self.sendOne(player, resp)
            return
        else:
            self.sendExclude((player,), resp)
            resp.tile.extend(tiles)
            self.sendOne(player, resp)
            player.handleMgr._rmTiles(tiles)
            player.changingTiles.extend(tiles)
            self.changeList.remove(player.chair)
            self.changDict[player.chair] = tiles
            if not self.changeList:
                self.logger(u'before change tiles {}'.format(self.changDict))
                self.changeTiles()

    def changeTiles(self):
        clock = 0
        resp = BloodRiver_mahjong_pb2.S_C_ExchangeThree()
        for _player in self.players:
            clock += 1
            tmp = self.changDict.keys()
            self.logger('change dict.keys in {} is {}'.format(_player.nickname, tmp))
            if _player.chair in tmp:
                tmp.remove(_player.chair)
            if clock == (self.maxPlayerCount - 1) and clock in tmp:
                _t = clock
            else:
                _t = random.choice(tmp)
            t = self.changDict.pop(_t)
            _player.handleMgr._addTiles(t)
            self.logger('player {} received exchanged tiles {}'.format(_player.nickname, t))
            data = resp.data.add()
            data.side = _player.chair
            data.tile.extend(t)
            data.temp_tile.extend(_player.changingTiles)
            del _player.changingTiles[:]
        self.sendAll(resp)
        self.privateStatus = 2

        obj_timer = timer.Timer(callback=self.AutoSetColor, overTime=getTime_AutoSetColor(), note='全局自动选缺')
        self.timerMgr.add_Timer(obj_timer, 0)

    def AutoSetColor(self):
        if self.privateStatus != 2:
            return
        for _player in self.getPlayers():
            if _player.chair in self.setColorList:
                type_tiles = {}
                type_nums = {}
                for _tile in _player.handleMgr.tiles:
                    _type = getTileType(_tile)
                    type_tiles.setdefault(_type, [])
                    type_tiles[_type].append(_tile)
                for _type, _tiles in type_tiles.iteritems():
                    _len = len(_tiles)
                    type_nums.setdefault(_len, [])
                    type_nums[_len].append(_type)

                type_keys = type_tiles.keys()
                self.logger(u'[AutoSetColor] nickname[%s] type_tiles[%s] type_nums[%s]' %
                            (_player.nickname, type_tiles, type_nums))
                if len(type_tiles) != 3:
                    for _type in ['a', 'b', 'c']:
                        if _type not in type_keys:
                            self.onSetColor(_player, _type)
                else:
                    nums_keys = type_nums.keys()
                    nums_keys.sort()
                    type_key = random.choice(type_nums[nums_keys[0]])
                    self.onSetColor(_player, type_key)

    def onSetColor(self, player, color):
        self.logger(u'[onSetColor] player[%s] color[%s]' % (player.nickname, color))
        resp = BloodRiver_mahjong_pb2.S_C_PlayerSetColor()
        resp.side = player.chair
        resp.result = True
        if player.chair not in self.setColorList:
            resp.color = ''
            resp.result = False
            resp.reason = u'玩家已完成选缺操作,请勿重复操作'
            self.sendOne(player, resp)
            return
        else:
            resp.color = color
            self.sendAll(resp)
            player.colorSet = color
            self.setColorList.remove(player.chair)
            self.colorSet[player.chair] = color
            if not self.setColorList:
                resp = BloodRiver_mahjong_pb2.S_C_SetColor()
                resp.color.extend(self.colorSet)
                self.sendAll(resp)
                self.logger(u'set color completed and the resp is {}'.format(resp))
                self.privateStatus = 3
                self.drawTile(self.dealer)

    def fillExtraMessage(self, player):
        resp = BloodRiver_mahjong_pb2.S_C_ExtraMessage()
        resp.status = self.privateStatus
        if self.colorSet[player.chair]:
            resp.selfColor = self.colorSet[player.chair]
        resp.color.extend(self.colorSet)
        if player.changingTiles:
            resp.changingTiles.extend(player.changingTiles)
        tmp = [0] * 4
        for _player in self.getPlayers():
            tmp[_player.chair] = _player.totalGameScore or 0
            # if _player.isFreeze:
            #     huData = resp.huPlayer.add()
            #     huData.side = _player.chair
            #     huData.tile.extend(_player.handleMgr.tiles)
            #     huData.huTile = _player.handleMgr.getHuData()[1]
        resp.score.extend(tmp)
        if player.handleMgr.lastTile:
            resp.lastTile = player.handleMgr.lastTile
        self.sendOne(player, resp)
        self.logger('send extra message to {} is {}'.format(player.nickname, resp))

    def getSaveSendAllProtoList(self):
        '''回放数据保存'''
        return ['S_C_SetColor', 'S_C_RefreshScore', 'S_C_ExchangeThree', 'S_C_HuTiles', 'S_C_PlayerExchangeThree',
                'S_C_PlayerSetColor']

    def dealHu(self, action, player):
        if self.multi_flag:
            self.ds = self.players[player.handleMgr.getHuData()[0]].chair
            self.logger(u'deal hu and multi flag and now ds is {}'.format(self.ds))
            self.multi_flag = False
            self.single_lock = True
        elif not self.single_lock:
            self.ds = player.chair
            self.single_lock = True
        # if self.huPlayerCount >= (self.maxPlayerCount - 1):
        #     self.balance()
        #     return
        self.nextProc(player)

    def refreshScore(self, player):
        self.logger('{} in refresh score'.format(player.nickname))

        '''名堂计算以及胡分结算'''
        beenHuPlayer, rate = player.getHuData()
        if beenHuPlayer:
            self.logger('hu player is {} and been hu player is {}'.format(player.nickname, beenHuPlayer.nickname))
            resp = BloodRiver_mahjong_pb2.S_C_RefreshScore()
            # all the rate calculus in player method get hu data
            score = self.baseScore * (2 ** rate)
            self.logger('player {} rate is {} and score is {}'.format(player.nickname, rate, score))
            if player.isSelfHU:
                '''自摸'''
                if self.bt == 0:
                    '''自摸加底'''
                    score += self.baseScore
                tmp = 0
                for other in self.getPlayers((player,)):
                    # if not other.isFreeze:
                    other.curGameScore -= score
                    player.curGameScore += score
                    other.totalGameScore -= score
                    player.totalGameScore += score
                    tmp += score

                    data = resp.data.add()
                    data.side = other.chair
                    data.change = -score
                    data.score = other.totalGameScore

                    self.logger('{} win {} from {} by self hu'.format(player.nickname, score, other.nickname))
                data = resp.data.add()
                data.side = player.chair
                data.change = tmp
                data.huType = 1
                data.score = player.totalGameScore

            elif player.isOtherHu:
                '''抢杠/点炮 一对一结算'''

                player.curGameScore += score
                beenHuPlayer.curGameScore -= score
                player.totalGameScore += score
                beenHuPlayer.totalGameScore -= score

                data = resp.data.add()
                data.side = beenHuPlayer.chair
                data.change = -score
                data.score = beenHuPlayer.totalGameScore

                data = resp.data.add()
                data.side = player.chair
                data.change = score
                data.huType = 2
                data.score = player.totalGameScore
                self.logger('[%s] win [%s] from [%s] by get hu or catch kong' %
                            (player.nickname, score, beenHuPlayer.nickname))

                if beenHuPlayer != self.beGrabKongHuPlayer:
                    '''呼叫转移'''
                    changeScore = 0
                    if beenHuPlayer.trueLastAction == CONCEALED_KONG:
                        changeScore = self.baseScore * 2 * 3
                    elif beenHuPlayer.trueLastAction == SELF_KONG:
                        changeScore = self.baseScore * 1 * 3
                    elif beenHuPlayer.trueLastAction == OTHERS_KONG:
                        changeScore = self.baseScore * 2 * 1

                    if changeScore:
                        self.callChangeKong.append([player.chair, beenHuPlayer.chair, changeScore])
                        self.logger('预计呼叫转移 [%s] pay [%s] to [%s]' %
                                    (beenHuPlayer.nickname, changeScore, player.nickname))

            self.sendAll(resp)

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
            log(u'[try do curAction][error]side[%s] not in curAction2PlayerNtiles[%s].' %
                (side, self.curAction2PlayerNtiles[action]), LOG_LEVEL_RELEASE)
            return False

        if side not in self.side2ActionNum or num != self.side2ActionNum[side]:
            log(u'[try do curAction][error]error num[%s] for side[%s] player[%s], side2ActionNum[%s].' %
                (num, side, player.nickname, self.side2ActionNum), LOG_LEVEL_RELEASE)
            return False

        allowActionTiles = self.curAction2PlayerNtiles[action][side]

        # 判断操作的麻将是否在允许集合中
        if action and actionTiles not in allowActionTiles:
            log(u'[try do curAction][error]actionTiles[%s] not in allowActionTiles[%s].' %
                (actionTiles, allowActionTiles), LOG_LEVEL_RELEASE)
            return False

        if not Auto and player.isproxy:
            self.onProxy(player, 0)

        for _action in self.curAction2PlayerNtiles:
            if side in self.curAction2PlayerNtiles[_action]:
                del self.curAction2PlayerNtiles[_action][side]
                if _action in self.curActions:
                    self.curActions.remove(_action)
        log(u'[doCurAction]curAction2PlayerNtiles[%s] curActions[%s] num[%s].' %
            (self.curAction2PlayerNtiles, self.curActions, num), LOG_LEVEL_RELEASE)
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
            tmp = [i for i in self.curActionedPlayerDatas]
            flag = self.players[tmp[0]].handleMgr.huData[0]
            tmp2 = {}
            tmp3 = []
            for i in tmp:
                p = self._getPriority4Side(flag, i)
                tmp2[p] = i
                tmp3.append(p)
            tmp3.sort()
            tmp3.reverse()
            flow = [tmp2[i] for i in tmp3]
            self.logger('curActionedPlayerDatas is {}'.format(self.curActionedPlayerDatas))
            self.logger('flag is {}'.format(flag))
            self.logger('tmp is {}'.format(tmp))
            self.logger('tmp2 is {}'.format(tmp2))
            self.logger('tmp3 is {}'.format(tmp3))
            for chair in flow:
                actionNtiles = self.curActionedPlayerDatas[chair]
                _action, tiles = actionNtiles
                if self.curHighestAction == _action:
                    if not _action:
                        resp = mahjong_pb2.S_C_DoAction()
                        resp.side = chair
                        actionObj = resp.action.add()
                        actionObj.action = NOT_GET
                        if doActionPlayer.handleMgr.tmpSide >= 0:
                            actionObj.beActionSide = doActionPlayer.handleMgr.tmpSide
                        self.sendOne(doActionPlayer, resp)
                        continue
                    curHighestAction = _action
                    doActionPlayer = self.players[chair]
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
                            actionObj.action = 99
                            actionObj.beActionSide = self.beGrabKongHuPlayer.chair
                        handTiles = self.getHuTileList(doActionPlayer, tileList)
                        actionObj.tiles.extend(handTiles)
                        actionObj.tiles.extend(tileList)
                        self.sendOne(doActionPlayer, resp)

                        copyHuResp = copy.deepcopy(resp)
                        copyActionObj = copyHuResp.action[0]
                        handTilesLen = len(handTiles)
                        copyActionObj.tiles[0:handTilesLen] = [''] * handTilesLen
                        self.sendExclude((doActionPlayer,), copyHuResp)

                    elif _action == CONCEALED_KONG:
                        actionObj.tiles.extend(tileList)
                        self.sendOne(doActionPlayer, resp)
                        tileList = self.getTileList(doActionPlayer, tileList[-1])
                        actionObj2 = copyResp.action.add()
                        actionObj2.action = _action
                        actionObj2.tiles.extend(tileList)
                        self.sendExclude((doActionPlayer,), copyResp)
                    else:
                        actionObj.tiles.extend(tileList)
                        self.sendAll(resp)
                    log(u'[try do cur action]room[%s] player[%s] action[%s] handle[%s].'
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

    def doHuMoreThanOne(self, ActionPlayers=None):
        self.multi_flag = True
        self.logger('set multi flag True')
        self.logger(u"[doHuMoreThanOn] lastDiiscardSide [%s] ActionPlayers %s" % (self.lastDiscardSide, ActionPlayers))

    # def dealSelfKong(self, action, player):
    #     if self.canGrabKongHu():
    #         log(u'[dealSelfKong] try grabkongHu.', LOG_LEVEL_RELEASE)
    #         if not player.handleMgr.kongTiles:
    #             return
    #         tile = player.handleMgr.kongTiles[-1]
    #         existCanHu = False
    #         self.resetCurAction()
    #         for _player in self.getPlayers((player,)):
    #             _player.handleMgr.setTmpTile(tile, _player.chair)
    #             actionNtiles = _player.handleMgr.getGrabKongHu()
    #             _player.handleMgr.setTmpTile(None)
    #             self.addCurAction(_player, actionNtiles)
    #             if actionNtiles:
    #                 existCanHu = True
    #         if existCanHu:
    #             self.lastOperateSide = player.chair
    #             self.beGrabKongHuPlayer = self.players[player.chair]
    #             self.nextProc(player)
    #             return
    #     resp = BloodRiver_mahjong_pb2.S_C_RefreshScore()
    #     tmp = 0
    #     for other in self.getPlayers((player,)):
    #         self.logger('{} in calculus self kong'.format(player.nickname))
    #         if not other.isFreeze:
    #             player.totalGameScore += self.baseScore
    #             other.totalGameScore -= self.baseScore
    #             player.curGameScore += self.baseScore
    #             other.curGameScore -= self.baseScore
    #             tmp += self.baseScore
    #             data = resp.data.add()
    #             data.side = other.chair
    #             data.change = -self.baseScore
    #             data.score = other.totalGameScore
    #     data = resp.data.add()
    #     data.side = player.chair
    #     data.change = tmp
    #     data.score = player.totalGameScore
    #     self.sendAll(resp)
    #     self.drawTile(player)

    # def dealOthersKong(self, action, player):
    #     side = player.handleMgr.action2balanceTiels[action][-1].split(';')[0]
    #     boy = self.players[int(side)]
    #     self.logger('{} in calculus others kong by {}'.format(player.nickname, boy.nickname))
    #     boy.totalGameScore -= self.baseScore * 2
    #     player.totalGameScore += self.baseScore * 2
    #     boy.curGameScore -= self.baseScore * 2
    #     player.curGameScore += self.baseScore * 2
    #     resp = BloodRiver_mahjong_pb2.S_C_RefreshScore()
    #
    #     data = resp.data.add()
    #     data.side = boy.chair
    #     data.change = -(self.baseScore * 2)
    #     data.score = boy.totalGameScore
    #
    #     data = resp.data.add()
    #     data.side = player.chair
    #     data.change = self.baseScore * 2
    #     data.score = player.totalGameScore
    #
    #     self.sendAll(resp)
    #     self.drawTile(player)

    # def dealConcealedKong(self, action, player):
    #     self.logger('{} in calculus ck kong'.format(player.nickname))
    #     resp = BloodRiver_mahjong_pb2.S_C_RefreshScore()
    #     tmp = 0
    #     for other in self.getPlayers((player,)):
    #         if not other.isFreeze:
    #             player.totalGameScore += self.baseScore * 2
    #             other.totalGameScore -= self.baseScore * 2
    #             player.curGameScore += self.baseScore * 2
    #             other.curGameScore -= self.baseScore * 2
    #             player.ckScore += self.baseScore * 2
    #             tmp += self.baseScore * 2
    #             data = resp.data.add()
    #             data.side = other.chair
    #             data.change = -(self.baseScore * 2)
    #             data.score = other.totalGameScore
    #     data = resp.data.add()
    #     data.side = player.chair
    #     data.change = tmp
    #     data.score = player.totalGameScore
    #     self.sendAll(resp)
    #     self.drawTile(player)

    def canHuMoreThanOne(self):
        return True

    def canGrabKongHu(self):
        return True

    def doAfterDiscard(self, discardPlayer, tile):
        discardPlayer.lastAction = -1
        discardPlayer.actionBefore = -1
        super(Game, self).doAfterDiscard(discardPlayer, tile)
        # self.resetCurAction()
        # for player in self.getPlayers((discardPlayer,)):
        #     if player.isFreeze: continue
        #     player.handleMgr.setTmpTile(tile, discardPlayer.chair)
        #     actionNtiles = player.handleMgr.getAllowActionNTiles(self.getAllowActions4Discard(discardPlayer, player))
        #     player.handleMgr.setTmpTile(None)
        #     self.addCurAction(player, actionNtiles)
        # self.lastOperateSide = discardPlayer.chair
        #
        # self.onReadyHand(discardPlayer)
        #
        # self.nextProc(discardPlayer)

    def setPlayerCopy(self, robot, player):
        '''掉线备份'''
        super(Game, self).setPlayerCopy(robot, player)
        robot.lastAction = player.lastAction
        robot.actionBefore = player.actionBefore
        robot.changingTiles = player.changingTiles
        robot.colorSet = player.colorSet
        robot.trueLastAction = player.trueLastAction
        robot.isFreeze = player.isFreeze
        robot.ckScore = player.ckScore
        robot.isSelfHU = player.isSelfHU
        robot.isOtherHu = player.isOtherHu

    def getAllowActions4Draw(self):
        '''摸牌后允许动作'''
        actions = [SELF_KONG, CONCEALED_KONG, HU]
        # 无牌可摸的情况下，可能需要将杠排除到允许actions之外
        if self.dealMgr.isDraw():
            if not self.canKong4NotTile():
                actions.remove(SELF_KONG)
                actions.remove(CONCEALED_KONG)
        return actions

    def getAllowActions4Discard(self, curPlayer, player):
        '''出牌時允許的操作'''
        actions = [PONG, OTHERS_KONG, HU]
        # 无牌可摸的情况下，可能需要将杠排除到允许actions之外
        if self.dealMgr.isDraw():
            if not self.canKong4NotTile():
                actions.remove(OTHERS_KONG)
        return actions

    def getDealer(self, dicePoints=None):
        '''获取庄家座位'''
        if self.curGameCount == 1:
            return OWNNER_SIDE
        elif self.ds >= 0:
            return self.ds
        return OWNNER_SIDE

    def getDealManager(self):
        """
        返回发牌器
        """
        _obj = DealManager(self)
        return _obj

    def getRobot(self):
        """
        获得使用的玩家类，用于设置掉线后放置玩家的拷贝
        """
        return Player()

    def doBeforeBalance(self, isEndGame=False):
        if isEndGame:
            return
        self.logger('[doBeforeBalance] roomId[%s]' % (self.roomId))
        for _player in self.getPlayers():
            New_huDesc = Counter(_player.huDescs)
            _player.huDescs = map(lambda x, y: ('%sX%s' % (x, y) if y > 1 else '%s' % x), New_huDesc.keys(),
                                  New_huDesc.values())
        if self.checkLock:
            return
        self.checkLock = True
        noReadyHands = []

        resp = BloodRiver_mahjong_pb2.S_C_RefreshScore()

        for _player in self.getPlayers():
            if _player.isFreeze:
                flag = True
            else:
                flag = _player.getReadyHands(self.dealMgr.getTryReadyHandTiles())
            if not flag:
                noReadyHands.append(_player)
                if not _player.handleMgr.isPig():
                    continue
                _player.huDescs.append('花猪'.decode('utf-8'))
                score = self.baseScore * (2 ** 4)
                for _other in self.getPlayers(excludePlayers=(_player,)):
                    _player.curGameScore -= score
                    _other.curGameScore += score
                    _player.totalGameScore -= score
                    _other.totalGameScore += score
                    self.logger('查花猪 {} pay {} to {} by flower pig'.format(_player.nickname, score, _other.nickname))

                    data = resp.data.add()
                    data.side = _player.chair
                    data.change = -score
                    data.score = _player.totalGameScore
                    data.msg = u'查花猪'

                    data = resp.data.add()
                    data.side = _other.chair
                    data.change = score
                    data.score = _other.totalGameScore
                    data.msg = u'[%s]查花猪' % (_player.nickname)
            else:
                '''小局杠信息'''
                if _player.handleMgr.selfKongTiles:
                    desc = "碰杠X{}".format(len(_player.handleMgr.selfKongTiles)).decode('utf-8')
                    _player.huDescs.append(desc)
                if _player.handleMgr.othersKongTiles:
                    desc = "接杠X{}".format(len(_player.handleMgr.othersKongTiles)).decode('utf-8')
                    _player.huDescs.append(desc)
                # if _player.handleMgr.beKongTiles:
                #     desc = "放杠*{}".format(len(_player.handleMgr.beKongTiles)).decode('utf-8')
                #     _player.huDescs.append(desc)
                if _player.handleMgr.concealedKongTiles:
                    desc = "暗杠X{}".format(len(_player.handleMgr.concealedKongTiles)).decode('utf-8')
                    _player.huDescs.append(desc)

                score = len(_player.handleMgr.selfKongTiles) * 1 + len(_player.handleMgr.concealedKongTiles) * 2
                if score > 0:
                    for other in self.getPlayers((_player,)):
                        _player.curGameScore += score
                        other.curGameScore -= score
                        _player.totalGameScore += score
                        other.totalGameScore -= score

                        data = resp.data.add()
                        data.side = other.chair
                        data.change = -score
                        data.score = other.totalGameScore
                        data.msg = u'[%s]暗杠和碰杠' % (_player.nickname)

                        data = resp.data.add()
                        data.side = _player.chair
                        data.change = score
                        data.score = _player.totalGameScore
                        data.msg = u'暗杠和碰杠'

                for BeKonger in _player.handleMgr.othersKongTiles:
                    other = self.players[BeKonger[0]]
                    score = 2
                    _player.curGameScore += score
                    other.curGameScore -= score
                    _player.totalGameScore += score
                    other.totalGameScore -= score

                    other.huDescs.append("放杠".decode('utf-8'))

                    data = resp.data.add()
                    data.side = other.chair
                    data.change = -score
                    data.score = other.totalGameScore
                    data.msg = u'放杠给[%s]' % (_player.nickname)

                    data = resp.data.add()
                    data.side = _player.chair
                    data.change = score
                    data.score = _player.totalGameScore
                    data.msg = u'接杠[%s]' % (other.nickname)

        for callData in self.callChangeKong:
            callChair, beCallChair, callScore = callData
            callPlayer = self.players[callChair]
            beCallPlayer = self.players[beCallChair]
            self.logger(
                '呼叫转移 {} pay {} to {} by flower pig'.format(callPlayer.nickname, callScore, beCallPlayer.nickname))
            if beCallPlayer in noReadyHands:
                self.logger('呼叫转移 没听牌,没算杠,忽略')
                continue
            callPlayer.curGameScore += callScore
            beCallPlayer.curGameScore -= callScore
            callPlayer.totalGameScore += callScore
            beCallPlayer.totalGameScore -= callScore

            data = resp.data.add()
            data.side = beCallPlayer.chair
            data.change = -callScore
            data.score = beCallPlayer.totalGameScore
            data.msg = u'呼叫转移给[%s]' % (callPlayer.nickname)

            data = resp.data.add()
            data.side = callPlayer.chair
            data.change = callScore
            data.score = callPlayer.totalGameScore
            data.msg = u'[%s]呼叫转移给我' % (beCallPlayer.nickname)

        self.sendAll(resp)

    def fillBalanceData(self, player, balanceData):
        '''小局结算'''
        beHuPlayer, _, _ = player.handleMgr.getHuData()
        balanceData.descs.extend(player.getBalanceDescs())
        balanceData.score = player.curGameScore
        balanceData.tiles.extend(player.handleMgr.getBalanceTiles())
        self.logger('{} hand tiles {}'.format(player.nickname, balanceData.tiles))
        balanceData.isHu = False
        if beHuPlayer >= 0:
            balanceData.isHu = True

    def drawTile(self, player):
        """
        某玩家摸牌
        """
        # 无牌可摸了，应该结算流局
        self.logger(' ')
        self.logger('[drawTile] player[%s] lastDiscardSide[%s]' %
                    (player.nickname, self.lastDiscardSide))

        for _player in self.getPlayers():
            self.logger('[drawTile] player[%s] trueLastAction[%s] lastDiscardSide[%s]' %
                        (_player.nickname, _player.trueLastAction, self.lastDiscardSide))

        if self.lastDiscardSide >= 0 and self.lastDiscardSide != player.chair:
            self.players[self.lastDiscardSide].trueLastAction = None

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
        self.onDrawTile(player, resp.tiles)
        self.curPlayerSide = player.chair

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

    def fillTotalBalanceData(self, player, balanceData):
        '''大局结算'''
        balanceData.score = player.totalGameScore
        self.logger('total data is {}'.format(player.packTotalBalanceDatas()))
        balanceData.descs.extend(player.packTotalBalanceDatas())

    def discard(self, discardPlayer, tile):
        if discardPlayer.isFreeze:
            lastTile = discardPlayer.handleMgr.getLastTile()
            if lastTile and tile != lastTile:
                log(u'[try play tile] [error] 已胡 所出牌[%s]不是最后摸的牌[%s] ' % (tile, lastTile), LOG_LEVEL_RELEASE)
                return
        super(Game, self).discard(discardPlayer, tile)

    def getPlayersName(self, players):
        return ','.join([p.nickname for p in players])

    def CountdownCallbackFunc(self):
        return [self.AutoExchangeThree, self.AutoSetColor, self.onDiscardTimeout, self.onDoActionTimeout]

    def dealDrawTile(self, curPlayer):
        self.curPlayerSide = curPlayer.chair
        self.ActionMS = getTime_DisCard()
        self.ActionStartTime = self.server.getTimestamp()

        if curPlayer.handleMgr.HuList:
            log(u'roomId[%s] 玩家[%s][%s]胡牌激活后自动打牌[%s]' %
                (self.roomId, curPlayer.nickname, curPlayer.chair, curPlayer.handleMgr.getLastTile()),
                LOG_LEVEL_RELEASE)
            obj_timer = self.timerMgr.getTimer(callback=self.onAutoDiscardProxy, overTime=getTime_DisCard_Proxy(),
                                               params=(curPlayer.chair,), note='玩家(%s)胡牌激活后自动打牌' % (curPlayer.nickname))
            self.timerMgr.add_Timer(obj_timer, 1)
            curPlayer.Timer = obj_timer
        elif curPlayer.isproxy:
            log(u'[dealDrawTile] 托管打牌[%s]' % (curPlayer.handleMgr.getLastTile()), LOG_LEVEL_RELEASE)
            obj_timer = self.timerMgr.getTimer(callback=self.onAutoDiscardProxy, overTime=getTime_DisCard_Proxy(),
                                               params=(curPlayer.chair,), note='玩家(%s)托管打牌' % (curPlayer.nickname))
            self.timerMgr.add_Timer(obj_timer, 1)
            curPlayer.Timer = obj_timer

        obj_timer = self.timerMgr.getTimer(callback=self.onDiscardTimeout, overTime=getTime_DisCard(),
                                           params=(curPlayer.chair,), note='全部(%s)正常打牌' % (curPlayer.nickname))
        self.timerMgr.add_Timer(obj_timer, 0)

    def onAutoDiscardProxy(self, chair):
        player = self.players[chair]
        if not player.isproxy and not player.handleMgr.HuList:
            return
        ColorSetTiles = player.getMyColorSetTiles()
        if ColorSetTiles:
            tile = ColorSetTiles[0]
        else:
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
        ColorSetTiles = player.getMyColorSetTiles()
        if ColorSetTiles:
            tile = ColorSetTiles[0]
        else:
            tile = player.handleMgr.getLastTile()
            if not tile:
                tile = player.handleMgr.tiles[-1]
        self.onDiscard(player, tile)

    def getBalanceCounterMs(self):
        """
        结算倒计时(毫秒)，需要则重写
        """
        return 15 * 1000
