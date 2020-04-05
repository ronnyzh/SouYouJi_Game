# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/11/5
Revision: 1.0.0
Description: Description
"""
import os

from define.define_web_redis_key import *
from define.define_redis_key import *
from model.model_redis import getInst
from server.factorys.tornadoFactory import TornadoFactory
from server.httpHandler.matchHandler import *
from server.mysqldb import mysqlDB, async_mysqlDb
from server.socketHandler.matchSocketHandler import *


class MatchServer(TornadoFactory):
    def __init__(self, *args, **kwargs):
        super(MatchServer, self).__init__(*args, **kwargs)
        self.mysqldb = self.getMysqlDB()
        self.ServerOrder_Key = Key_Server_Order % self.serverTag

    def getRedis(self, dbNum=1):
        return getInst(dbNum=dbNum)

    def getMysqlDB(self):
        return mysqlDB

    def getAsyncMysqlDB(self):
        return async_mysqlDb

    def getAppRouterHandler(self):
        return [
            (r"/match/infoList_get", MatchHandler_infoList_get),
            (r"/match/enroll", MatchHandler_enroll),
            (r"/match/enroll_get", MatchHandler_enroll_get),
            (r"/match/enroll_post", MatchHandler_enroll_post),
            (r"/match/enroll_delete", MatchHandler_enroll_delete),

            (r"/ping", PingHandler),
            (r"/admin/match/dismiss", MatchHandler_dismiss),
            (r"/admin/match/enrollUsers", MatchHandler_enrollUsers),
            (r"/match/(\w+)", MatchSocketHandler),
            (r"/match/matchList", MatchHandler_matchList),
            (r"/", MatchHandler_matchList),
        ]

    def getApplicationConfigs(self):
        applicationConfigs = super(MatchServer, self).getApplicationConfigs()
        applicationConfigs.update(dict(
            static_path=os.path.join(os.path.dirname(__file__), "..\\..\\static"),
            template_path=os.path.join(os.path.dirname(__file__), "..\\..\\template"),
        ))
        return applicationConfigs

    def initApplication(self):
        app = super(MatchServer, self).initApplication()
        app.mysqldb = self.mysqldb
        return app

    def getOrderServices(self):
        redis = self.getRedis()
        orderServices = redis.lrange(self.ServerOrder_Key, 0, -1)
        return orderServices

    def doOrderJobs_afterSuc(self, job, _orderArgs, _order):
        redis = self.getRedis()
        redis.lrem(self.ServerOrder_Key, 1, _order)

    def sendProtocol2GameService(self, gameId, protocolStr, serviceFind=None):
        """
            发送协议给游戏服务器
        """
        redis = self.getRedis()
        serverList = redis.lrange(FORMAT_GAME_SERVICE_SET % (gameId), 0, -1)
        self.log('[sendProtocol2GameService] serverList=>%s protocolStr=>%s serviceFind[%s]' %
                 (protocolStr, protocolStr, serviceFind))
        for serverTable in serverList:
            if serviceFind and serverTable.find(serviceFind) == -1:
                continue
            _, _, _, currency, ip, port = serverTable.split(':')
            serverTable = FORMAT_SERVICE_PROTOCOL_TABLE % (gameId, '%s:%s:%s' % (currency, ip, port))
            self.log('[sendProtocol2GameService] sendTo [%s] [%s]' % (serverTable, protocolStr))
            redis.rpush(serverTable, protocolStr)
