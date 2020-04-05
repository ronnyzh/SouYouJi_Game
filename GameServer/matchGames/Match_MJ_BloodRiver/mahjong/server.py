# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: Server factory
"""

from common.common_server import CommonServer
from common.log import log, LOG_LEVEL_RELEASE, LOG_LEVEL_ERROR
from common import net_resolver_pb
from common.protocols.mahjong_consts import *

from player import Player
from game import Game
from publicCommon.public_server import PublicServer
from db_define import *

import BloodRiver_mahjong_pb2
from matchCommon.match_server import MatchServer


class MahjongServer(MatchServer):
    protocol = Player

    def __init__(self, *args, **kwargs):
        super(MahjongServer, self).__init__(*args, **kwargs)

    def getGameID(self):
        return MY_GAMEID

    def getGameModule(self, *args, **kwargs):
        return Game(*args, **kwargs)

    def registerProtocolResolver(self):
        unpacker = net_resolver_pb.Unpacker
        self.recverMgr.registerCommands((
            unpacker(BloodRiver_mahjong_pb2.C_S_SET_COLOR, BloodRiver_mahjong_pb2.C_S_SetColor, self.onSetColor),
            unpacker(BloodRiver_mahjong_pb2.C_S_EXCHANGE_THREE, BloodRiver_mahjong_pb2.C_S_ExchangeThree,
                     self.onExchangeThree),
        ))

        packer = net_resolver_pb.Packer
        self.senderMgr.registerCommands((
            packer(BloodRiver_mahjong_pb2.S_C_EXCHANGE_FLAG, BloodRiver_mahjong_pb2.S_C_ExchangeFlag),
            packer(BloodRiver_mahjong_pb2.S_C_EXCHANGE_THREE, BloodRiver_mahjong_pb2.S_C_ExchangeThree),
            packer(BloodRiver_mahjong_pb2.S_C_SET_COLOR, BloodRiver_mahjong_pb2.S_C_SetColor),
            packer(BloodRiver_mahjong_pb2.S_C_EXTRA_MESSAGE, BloodRiver_mahjong_pb2.S_C_ExtraMessage),
            packer(BloodRiver_mahjong_pb2.S_C_REFRESH_SCORE, BloodRiver_mahjong_pb2.S_C_RefreshScore),
            packer(BloodRiver_mahjong_pb2.S_C_HUTILES, BloodRiver_mahjong_pb2.S_C_HuTiles),
            packer(BloodRiver_mahjong_pb2.S_C_PLAYER_EXCHANGE_THREE, BloodRiver_mahjong_pb2.S_C_PlayerExchangeThree),
            packer(BloodRiver_mahjong_pb2.S_C_PLAYER_SET_COLOR, BloodRiver_mahjong_pb2.S_C_PlayerSetColor),
        ))

        super(MahjongServer, self).registerProtocolResolver()

    def onSetColor(self, player, req):
        if not player.game:
            log(u'[try set color][error]account[%s] not in game.' % (player.account), LOG_LEVEL_RELEASE)
            return
        log(u'[try set color]account[%s] color[%s].' % (player.account, req.color), LOG_LEVEL_RELEASE)
        player.game.onSetColor(player, req.color)

    def onExchangeThree(self, player, req):
        if not player.game:
            log(u'[try exchange three][error]account[%s] not in game.' % (player.account), LOG_LEVEL_RELEASE)
            return
        log(u'[try exchange three]account{} tiles {}.'.format(player.account, req.tile), LOG_LEVEL_RELEASE)
        player.game.onExchangeThree(player, req.tile)

    def doAfterRefresh(self, player):
        super(MahjongServer, self).doAfterRefresh(player)

        if player.game.stage == GAMING:
            resp = BloodRiver_mahjong_pb2.S_C_HuTiles()
            for _player in player.game.getPlayers():
                if not _player.handleMgr.HuList:
                    continue
                HuData = resp.HuData.add()
                HuData.side = _player.chair
                HuData.HuTile.extend(_player.handleMgr.HuList)
            player.game.sendOne(player, resp)

            player.game.fillExtraMessage(player)

    def getMatchRoomRule(self):
        """
        娱乐模式规则
        """
        return [3, 1, 1, [0, 1], 2, 0, 1]
