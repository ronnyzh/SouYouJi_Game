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

from db_define import *

import hainan_mahjong_pb2

from publicCommon.public_server import PublicServer


class MahjongServer(PublicServer):
    protocol = Player

    def __init__(self, *args, **kwargs):
        super(MahjongServer, self).__init__(*args, **kwargs)

    def getGameID(self):
        return MY_GAMEID

    def getGameModule(self, *initData):
        return Game(*initData)

    def registerProtocolResolver(self):
        unpacker = net_resolver_pb.Unpacker
        self.recverMgr.registerCommands((
            unpacker(hainan_mahjong_pb2.C_S_ON_GA, hainan_mahjong_pb2.C_S_OnGa, self.onGa),
        ))
        packer = net_resolver_pb.Packer
        self.senderMgr.registerCommands((
            packer(hainan_mahjong_pb2.S_C_GA_DATA, hainan_mahjong_pb2.S_C_GaData),
            packer(hainan_mahjong_pb2.S_C_FLOWER_HU, hainan_mahjong_pb2.S_C_Flower_Hu),
            packer(hainan_mahjong_pb2.S_C_GA_CHOOSE, hainan_mahjong_pb2.S_C_Ga_Choose),
            packer(hainan_mahjong_pb2.S_C_BE_HANDLE_TILES, hainan_mahjong_pb2.S_C_Be_Handle_Tiles),
            packer(hainan_mahjong_pb2.S_C_BE_KONG, hainan_mahjong_pb2.S_C_Be_Kong),
            packer(hainan_mahjong_pb2.S_C_BE_FOLLOW, hainan_mahjong_pb2.S_C_Be_Follow),
            packer(hainan_mahjong_pb2.S_C_BE_SURROUND, hainan_mahjong_pb2.S_C_Be_Surround),
            packer(hainan_mahjong_pb2.S_C_ORDER, hainan_mahjong_pb2.S_C_Order),
        ))

        super(MahjongServer, self).registerProtocolResolver()

    def onGa(self, player, req):
        if not player.game:
            log(u'[try set ga][error]account[%s] not in game.' % (player.account), LOG_LEVEL_RELEASE)
            return

        log(u'[try set ga]account[%s] ga[%s].' % (player.account, req.ga), LOG_LEVEL_RELEASE)
        player.game.onGa(player, req.ga)

    def doAfterRefresh(self, player):
        '''
        刷新数据结束后操作
        '''
        super(MahjongServer, self).doAfterRefresh(player)

        if int(player.game.stage) != WAIT_START:
            if int(player.ga) == -1:
                # 如果玩家没选,掉线则重新发送
                if player.game.isUpGa or player.game.isFreeUpGa:
                    sendResp = hainan_mahjong_pb2.S_C_GaData()
                    gaData = player.game.getAllowGa(player.gaHisList[-1] if player.gaHisList else -1)
                    sendResp.canGetGa.extend(gaData)
                    player.game.sendOne(player, sendResp)
                # 广播所有选噶玩家
                player.game.sendAllGaBrocast()

            else:
                player.game.sendAllGaBrocast()
            if player.game.isOrder and player.game.orderNum >= 0:
                resp = hainan_mahjong_pb2.S_C_Order()
                resp.orderNum = player.game.orderNum
                self.sendAll(resp)
