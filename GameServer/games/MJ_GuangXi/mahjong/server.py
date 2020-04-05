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
from publicCommon.public_server import PublicServer

from player import Player
from game import Game

from db_define import *

import guangxi_mahjong_pb2
import copy


class MahjongServer(PublicServer):
    protocol = Player

    def __init__(self, *args, **kwargs):
        super(MahjongServer, self).__init__(*args, **kwargs)

    def getGameID(self):
        return MY_GAMEID

    def getGameModule(self, *initData):
        return Game(*initData)

    def registerProtocolResolver(self):
        packer = net_resolver_pb.Packer
        self.senderMgr.registerCommands((
            packer(guangxi_mahjong_pb2.S_C_RUNHORSE, guangxi_mahjong_pb2.S_C_RunHorse),
        ))

        super(MahjongServer, self).registerProtocolResolver()
