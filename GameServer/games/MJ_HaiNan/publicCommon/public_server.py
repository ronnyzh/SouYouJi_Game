# coding=utf-8

from common.log import log, LOG_LEVEL_RELEASE
from common import net_resolver_pb
from common.protocols.mahjong_consts import *
from common.common_server import CommonServer
from public_game import PublicGame
from public_player import PublicPlayer
from publicCommon import logger_mgr
import common_pb2
from configs import *
from common.pb_utils import *

import copy
from datetime import datetime

s_logger = logger_mgr.s_logger
e_logger = logger_mgr.e_logger


class PublicServer(CommonServer):
    protocol = PublicPlayer

    def logger(self, str, level='info'):
        try:
            if level == 'info':
                s_logger.info(u'%s' % (str))
            elif level == 'error':
                e_logger.info(u'%s' % (str))
            else:
                print(u'%s' % (str))
        except:
            s_logger.print_exc()
            print(u'%s' % (str))

    def registerProtocolResolver(self):
        unpacker = net_resolver_pb.Unpacker
        self.recverMgr.registerCommands((
            unpacker(common_pb2.C_S_DOREADYSTART, common_pb2.C_S_DoReadyStart, self.DoReadyStart),
            unpacker(common_pb2.C_S_ONPROXY, common_pb2.C_S_OnProxy, self.onProxy),
        ))

        packer = net_resolver_pb.Packer
        self.senderMgr.registerCommands((
            packer(common_pb2.S_C_PLAYERREADYRESULT, common_pb2.S_C_PlayerReadyResult),
            packer(common_pb2.S_C_PROXY, common_pb2.S_C_Proxy),
        ))

        super(PublicServer, self).registerProtocolResolver()

    def getGameModule(self, *initData):
        return PublicGame(*initData)

    def DoReadyStart(self, player, req):
        if not player.game:
            log(u'[DoReadyStart][error] account[%s] not in game.' % (player.account), LOG_LEVEL_RELEASE)
            return
        log(u'[DoReadyStart]account[%s] req[%s].' % (player.account, req), LOG_LEVEL_RELEASE)
        result = True
        if req.result == False:
            result = False
        player.game.DoReadyStart(player, result)

    def doAfterRefresh(self, player):
        super(PublicServer, self).doAfterRefresh(player)
        game = player.game
        if game.stage == WAIT_START and isOpenReadyStart:
            game.sendAllPlayerReadyResult(sendPlayer=player)

        if game.isEnding:
            if game.oldBalanceData and player.chair not in game.ready2NextGameSides:
                log(u'[doAfterRefresh] player[%s] 已结算重弹结算' % (player), LOG_LEVEL_RELEASE)
                newResp = copy.deepcopy(game.oldBalanceData)
                self.sendOne(player, newResp)

        """ 发送托管状态 """
        game.sendProxyBro(player)

    def tryRefresh(self, game, player, resp):
        super(PublicServer, self).tryRefresh(game, player, resp)
        resp.data.Countdown = game.getCountdownTime(player)

    def onProxy(self, player, req):
        if not player.game:
            return
        if req.choice not in [0, 1]:
            return
        player.game.onProxy(player, req.choice)

    def useRoomCards(self, game):
        super(PublicServer, self).useRoomCards(game)
        GAME_ROOMCARDS_DAY_TOTAL = "game:roomCards:%s:%s:total"
        GAME_ROOMCARDS_ALL_TOTAL = "game:roomCards:%s:total"
        ymd = datetime.now().strftime("%Y-%m-%d")
        redis = self.getPublicRedis()
        pipe = redis.pipeline()
        pipe.incrby(GAME_ROOMCARDS_DAY_TOTAL % (self.ID, ymd), game.needRoomCards)
        pipe.incrby(GAME_ROOMCARDS_ALL_TOTAL % (self.ID), game.needRoomCards)
        pipe.execute()
