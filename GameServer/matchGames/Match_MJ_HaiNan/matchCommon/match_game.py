# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/1
Revision: 1.0.0
Description: Description
"""
import copy
import traceback

from common.log import *
from common.pb_utils import *
from publicCommon import logger_mgr
from publicCommon.public_game import PublicGame
import match_pb2

isMahjong = False
try:
    from common.protocols.mahjong_consts import *
    from common import mahjong_pb2
except:
    from common.protocols.poker_consts import *
    from common import baseProto_pb2, poker_pb2
else:
    baseProto_pb2 = mahjong_pb2
    poker_pb2 = mahjong_pb2
    isMahjong = True


class MatchGame(PublicGame):
    def __init__(self, server, ruleParams, needInit=True, roomId=0, curRoundNum=0, matchMgr=None, describe=''):
        assert matchMgr
        self.matchMgr = matchMgr
        self.curRoundNum = curRoundNum
        self.gameNumber = ''
        super(MatchGame, self).__init__(server, ruleParams, needInit=needInit, roomId=roomId)
        self.isUseRoomCards = True
        self.describe = describe or u'第%s轮次比赛' % (self.curRoundNum)

    def setGameNumber(self):
        self.gameNumber = self.getGameNumber()

    def logger(self, str, level='info'):
        try:
            if level == 'info':
                logger_mgr.g_logger.info(u'[%s] %s' % (self.gameNumber, str))
            elif level == 'error':
                logger_mgr.e_logger.info(u'[%s] %s' % (self.gameNumber, str))
            else:
                print(u'[%s] %s' % (self.gameNumber, str))
        except:
            traceback.print_exc()
            print(u'[Room:%s] %s' % (self.gameNumber, str))

    def resetSetData(self):
        super(MatchGame, self).resetSetData()

    def onTick(self, timestamp):
        super(MatchGame, self).onTick(timestamp)

    def setPlayerCopy(self, robot, player):
        super(MatchGame, self).setPlayerCopy(robot, player)
        robot.userRecordMgr = player.userRecordMgr

    def onReady2NextGame(self, player):
        """
        快速关闭结算页面，所有玩家都做了此操作后，马上开始下一小局
        """
        if not self.isEnding:
            log(u'[ready next]room[%s] game is not end.' % (self.roomId), LOG_LEVEL_RELEASE)
            return

        side = player.chair
        if side not in self.ready2NextGameSides:
            self.ready2NextGameSides.append(side)

    def onGameStartTimeout(self):
        """
        """
        pass

    def getGameNumber(self):
        return '%s-%s-%s' % (self.matchMgr.matchNumber, self.curRoundNum, self.roomId)

    def sendMatchInfo(self, player):
        resp = match_pb2.S_C_MatchInfo()
        resp.matchNumber = self.matchMgr.matchNumber
        resp.gameNumber = self.gameNumber
        resp.describe = self.describe
        resp.curRoundNum = self.curRoundNum
        resp.maxRoundNum = self.matchMgr.maxRoundNum
        resp.curPlayerNum = self.matchMgr.curPlayerNum
        resp.maxPlayerNum = self.matchMgr.maxPlayerNum
        resp.curRotation = self.matchMgr.curRotation
        resp.curRotationRoundNum = self.matchMgr.curRotationRoundNum
        self.server.sendOne(player, resp)

    def sendRoomDatas(self, sendPlayer=None):
        resp = self.matchMgr.getCurRoundRoomDatas()
        if not sendPlayer:
            self.sendAll(resp)
        else:
            self.sendOne(sendPlayer, resp)

    def sendRotationDatas(self, sendPlayer=None):
        resp = self.matchMgr.getRotationDatas()
        if not sendPlayer:
            self.sendAll(resp)
        else:
            self.sendOne(sendPlayer, resp)

    def getRoomRanks(self, resp=None):
        if not resp:
            resp = match_pb2.S_C_RankInfo()
        for _player in self.getPlayers():
            roomRankResp = resp.roomRanks.add()
            roomRankResp.side = _player.chair
            roomRankResp.uid = int(_player.uid)
            roomRankResp.nickname = _player.nickname
            roomRankResp.headImgUrl = _player.headImgUrl
            roomRankResp.rank = _player.userRecordMgr.rank
            roomRankResp.integralTotal = _player.userRecordMgr.integralTotal
            roomRankResp.integralHistory.extend(_player.userRecordMgr.integralHistory)
        return resp

    def sendRankInfo(self, getRoomRanks=True, getMatchRanks=True, sendPlayer=None):
        resp = match_pb2.S_C_RankInfo()
        if getRoomRanks:
            self.getRoomRanks(resp=resp)
        if getMatchRanks:
            self.matchMgr.getMatchRanks(resp=resp)
        self.logger(u'[sendRankInfo] sendPlayer[%s] => %s' % (sendPlayer, resp))
        if sendPlayer:
            self.sendOne(sendPlayer, resp)
        else:
            self.sendAll(resp)

    def initByRuleParams(self, ruleParams):
        """
        Abstract interface for parse rule parameters
        """
        params = eval(ruleParams)

        totalCount = int(params[-3])
        if totalCount:
            self.gameTotalCount = totalCount
            self.ruleDescs.append("%s局" % (self.gameTotalCount))

        self.needRoomCards = int(params[-2])
        self.baseScore = max(int(params[-1]), 1)
        self.ruleDescs.append("底分%s" % (self.baseScore))

        self.ruleDescs = "-".join(self.ruleDescs).decode('utf-8')

        log(u'[get gameRules]room[%s] ruleParams[%s] ruleTxt[%s]' % (self.roomId, params, self.ruleDescs),
            LOG_LEVEL_RELEASE)

    def getRewardList(self, sendPlayer=None):
        resp = match_pb2.S_C_getRewardList()
        resp.rewardList = self.matchMgr.rewardList
        if sendPlayer:
            self.sendOne(sendPlayer, resp)
        else:
            self.sendAll(resp)

    def balance(self, *args, **kwargs):
        if isMahjong:
            self.mahjong_balance(*args, **kwargs)
        else:
            self.poker_balance(*args, **kwargs)

    def mahjong_balance(self, isDrawn=False, isEndGame=False, isSave=True, needSpecitile=True):
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
        if isEndGame:
            if self.isSaveGameData:
                # 总数据存盘
                log(u'[on balance]room[%s] save all data.' % (self.roomId), LOG_LEVEL_RELEASE)
                self.server.savePlayerTotalBalanceData(self, resp.gameUserDatas)
            self.removeRoom()
        else:
            self.matchMgr.gameBalanceing(self, isDrawn=isDrawn)
            # 切换下一局
            self.resetSetData()
            self.isEnding = True
            self.stage = GAME_READY
            # self.onSetStart(self.players[OWNNER_SIDE])
            self.setCounter([self.dealer.chair], self.balanceCounterMs, self.onGameStartTimeout)
            self.matchMgr.gameAfterBalance(self)

    def poker_balance(self, isEndGame=False, isSave=True):
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
            self.matchMgr.gameBalanceing(self, isDrawn=False)
            # 切换下一局
            self.resetSetData()
            self.isEnding = True
            self.stage = GAME_READY
            # self.onSetStart(self.players[OWNNER_SIDE])
            self.setCounter([self.dealerSide], self.balanceCounterMs, self.onGameStartTimeout)
            self.matchMgr.gameAfterBalance(self)

    def mahjong_getSaveDatas(self):
        datas = {
            'gameNumber': self.gameNumber,
            'ghostTile': self.specialTile,
            'players': {},
            'startTime': self.setStartTime,
            'endTime': self.setEndTime,
        }
        for player in self.getPlayers():
            beHuPlayer, _, _ = player.handleMgr.getHuData()
            datas['players'][player.chair] = {
                'nickname': player.nickname,
                'account': player.account,
                'chair': player.chair,
                'uid': int(player.uid),
                'descs': ','.join(player.huDescs),
                'tiles': player.handleMgr.tiles,
                'b_tiles': player.handleMgr.getBalanceTiles(),
                'score': player.curGameScore,
                'isDealer': (player == self.dealer),
                'isHu': beHuPlayer >= 0,
            }
        return datas

    def poker_getSaveDatas(self):
        datas = {
            'gameNumber': self.gameNumber,
            'players': {},
            'startTime': self.setStartTime,
            'endTime': self.setEndTime,
            'multiple': self.multiple,
            'holeCards': self.holeCards,
        }
        for player in self.getPlayers():
            isWin = False
            if (self.isLandlordWin and player.isLandlord) or not (self.isLandlordWin or player.isLandlord):
                isWin = True
            datas['players'][player.chair] = {
                'nickname': player.nickname,
                'account': player.account,
                'chair': player.chair,
                'uid': int(player.uid),
                'cards': player.handleMgr.cards,
                'score': player.curGameScore,
                'isWin': isWin,
                'isDealer': player.isLandlord
            }
        return datas
