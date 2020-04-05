# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: Server factory
"""

from common.common_server import CommonServer
from common.log import log, LOG_LEVEL_RELEASE
from common import net_resolver_pb, poker_pb2, baseProto_pb2
from publicCommon.public_server import PublicServer
from player import Player
from game import Game
from consts import *
from db_define import *
import fightTheLandlord_poker_pb2
import private_mahjong_pb2
from matchCommon.match_server import MatchServer


class PokerServer(MatchServer):
    protocol = Player

    def __init__(self, *args, **kwargs):
        super(PokerServer, self).__init__(*args, **kwargs)

    def getGameID(self):
        return MY_GAMEID

    def getGameModule(self, *args, **kwargs):
        return Game(*args, **kwargs)

    def registerProtocolResolver(self):
        unpacker = net_resolver_pb.Unpacker
        self.recverMgr.registerCommands((
            unpacker(fightTheLandlord_poker_pb2.C_S_ROB_LANDLORD, fightTheLandlord_poker_pb2.C_S_RobLandlord,
                     self.onRobLandlord),
        ))
        packer = net_resolver_pb.Packer
        self.senderMgr.registerCommands((
            packer(fightTheLandlord_poker_pb2.S_C_ROB_LANDLORD, fightTheLandlord_poker_pb2.S_C_RobLandlord),
            packer(fightTheLandlord_poker_pb2.S_C_ROB_LANDLORD_RESULT,
                   fightTheLandlord_poker_pb2.S_C_RobLandlordResult),
            packer(fightTheLandlord_poker_pb2.S_C_SCORE_DATA, fightTheLandlord_poker_pb2.S_C_ScoreData),
            packer(fightTheLandlord_poker_pb2.S_C_REFRESH_DATAS, fightTheLandlord_poker_pb2.S_C_RefreshDatas),
            packer(private_mahjong_pb2.S_C_BANINTERACTION, private_mahjong_pb2.S_C_BanInteraction),
        ))

        super(PokerServer, self).registerProtocolResolver()

    def onRobLandlord(self, player, req):
        if not player.game:
            log(u'[onRobLandlord][error] account[%s] not in game.' % (player.account), LOG_LEVEL_RELEASE)
            return
        log(u'[onRobLandlord]account[%s] req[%s].' % (player.account, req), LOG_LEVEL_RELEASE)
        player.game.onRobLandlord(player, req.choseType, req.operate)

    def onTryRefresh(self, player, req):
        '''刷新数据'''
        game = player.game

        resp = fightTheLandlord_poker_pb2.S_C_RefreshDatas()
        resp.result = False
        if not game:
            errorStr = '未加入游戏或游戏已结束，刷新失败'.decode('utf-8')
            resp.reason = errorStr
            self.sendOne(player, resp)
            log(u"[try refresh][error]nickname[%s] is not in game." % (player.nickname), LOG_LEVEL_RELEASE)
            return

        log(u"[try refresh]nickname[%s] room[%s]." % (player.nickname, game.roomId), LOG_LEVEL_RELEASE)
        resp.result = True
        self.tryRefresh(game, player, resp)

        self.sendOne(player, resp)

        self.doAfterRefresh(player)

    def tryRefresh(self, game, player, resp):
        if isinstance(resp, poker_pb2.S_C_RefreshData):
            super(PokerServer, self).tryRefresh(game, player, resp)
            return
        super(PokerServer, self).tryRefresh(game, player, resp.refreshData)
        player.logger(u'[tryRefresh] curCallingSide[%s] isAfterLandlord[%s]' %
                      (game.curCallingSide, game.isAfterLandlord))
        if game.curCallingSide == player.chair and game.gameStage != ACTIONING:
            game.fillRobLandlord(resp.robLandlord)
        if game.isAfterLandlord:
            game.fillLandlordData(resp.landlordData)
        for _player in game.getPlayers():
            playerBombData = resp.playerBombData.add()
            playerBombData.side = _player.chair
            playerBombData.bombCount = _player.bombCount
            player.logger(u'[tryRefresh] chair[%s] isCalledLandlord[%s] isRobedLandlord[%s] isActioned[%s]' %
                          (_player.chair, _player.isCalledLandlord, _player.isRobedLandlord, _player.isActioned))
            if _player.chair != game.curPlayerSide:
                lastActionedData = resp.lastActionedData.add()
                lastActionedData.side = _player.chair
                if game.gameStage == ACTIONING:
                    lastDiscardList = _player.lastDiscard
                    if lastDiscardList:
                        lastDiscard = lastDiscardList[0]
                    else:
                        lastDiscard = 'never'
                    lastActionedData.cards = lastDiscard
                    if len(lastDiscardList) == 2:
                        lastActionedData.usedWildCards = lastDiscardList[1]
                elif _player.isRobedLandlord and game.gameStage == ROBING:
                    lastActionedData.callType = ROB_LANDLORD
                    lastActionedData.callData = _player.robData
                if _player.isCalledLandlord and game.gameStage in [CALLING, ROBING] and not _player.isRobedLandlord:
                    lastActionedData.callType = game.callType
                    lastActionedData.callData = _player.callData

    def doAfterRefresh(self, player):
        if player.game.banInteraction:
            resp = private_mahjong_pb2.S_C_BanInteraction()
            resp.result = True
            self.sendOne(player, resp)
        super(PokerServer, self).doAfterRefresh(player)

    def getMatchRoomRule(self):
        return [1, 2, 2, 0, 1]

    def getMaxPlayerCount(self):
        return 3