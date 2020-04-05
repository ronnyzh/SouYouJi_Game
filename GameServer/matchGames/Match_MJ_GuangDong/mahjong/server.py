# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: Server factory
"""

from common import net_resolver_pb
from player import Player
from game import Game
from db_define import *
import guangdong_mahjong_pb2
from publicCommon.public_server import PublicServer
from matchCommon.match_server import MatchServer


class MahjongServer(MatchServer):
    protocol = Player

    def getGameID(self):
        return MY_GAMEID

    def getGameModule(self, *args, **kwargs):
        return Game(*args, **kwargs)

    def registerProtocolResolver(self):
        packer = net_resolver_pb.Packer
        self.senderMgr.registerCommands((
            packer(guangdong_mahjong_pb2.S_C_RUNHORSE, guangdong_mahjong_pb2.S_C_RunHorse),
        ))

        super(MahjongServer, self).registerProtocolResolver()

    def getMatchRoomRule(self):
        return [[0, []], 0, 2, 0, 1]
