# -*- coding:utf-8 -*-
#!/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: Player peer
"""

from common.log import log, LOG_LEVEL_RELEASE
from common.peer import Peer
from common import consts
from handle_manger import HandleManger
from mahjong_pb2 import S_C_Disconnected
from common_db_define import *
from common.protocols.mahjong_consts import *
import redis_instance

import time
from datetime import datetime
import copy

SESSION_TIMEOUT_TICK = 300000
GAME_KICK_OUT_TICK = 30 * 1000

DROP_REASON_CODE2TXT = {
    consts.DROP_REASON_INVALID      :   "与服务器的连接中断。".decode(LANG_CODE),
    consts.DROP_REASON_TIMEOUT      :   "你因长时间未做操作，被断开连接，请重新登录。".decode(LANG_CODE),
    consts.DROP_REASON_FREEZE       :   "你的账号已被管理员冻结，请咨询客服了解详请。".decode(LANG_CODE),
    consts.DROP_REASON_CLOSE_SERVER :   "系统因进行维护暂已关闭，请稍后再进。".decode(LANG_CODE),
    consts.DROP_REASON_REPEAT_LOGIN :   "你的账号已从其它位置登录，请咨询客服了解详情。".decode(LANG_CODE),
}

class CommonPlayer(Peer):
    def __init__(self):
        super(CommonPlayer, self).__init__()

        self.game = None
        self.endType = None
        self.chair = consts.SIDE_UNKNOWN
        self.isControlByOne = False

        self.uid = 0
        self.account = ""
        self.passwd = ""
        self.nickname = ""
        self.money = 0
        self.coin = 0
        self.parentAg = ''
        self.sex = 0
        self.roomCards = 0
        self.headImgUrl = ''
        self.region = ''
        self.valid = '1'
        self.isGM = False
        # 总分数
        self.totalGameScore = 0
        self.maxScore = 1

        #微信
        self.openID = None
        self.refreshToken = None
        self.accessToken = None
        self.unionID = None

        self.table = ''

        #用户sessionId
        self.operatorSessionId = ""
        #本次登录session
        self.sessionId = ""
        self.cacheTable = ''

        self.lastSessionTimestamp = int(time.time()*1000)
        self.lastGetRankTimestamp = 0
        self.gameLastPacketTimestamp = 0
        self.lastGetReadyHandTimestamp = 0

        # 玩家在线状态相关参数
        self.lastPingTimestamp = int(time.time()*1000)
        self.lastOnlineState = False
        self.isOnline = True

        self.totalGameScore = 0
        self.totalKongCount = 0
        self.totalConcealedKongCount = 0
        self.totalGiveHuCount = 0
        self.totalOtherHuCount = 0
        self.totalSelfHuCount = 0
        self.totalBeKongCount = 0

        self.resetPerGame()

    def OnRefresh(self):
        """ 设置SID的超时时间

        :return:
        """
        print(u"开始设置超时时间:%s" % self.nickname)
        privateRedis = redis_instance.getInst(8)
        publicRedis  = redis_instance.getInst(PUBLIC_DB)

        sid = self.operatorSessionId
        up_time = privateRedis.get("session:%s:timeout" % sid)
        if up_time:
            up_time = int(up_time)
            curTime = int(time.time())
            if (curTime - up_time) < 300:
                print(u"还没有到达超时时间:%s" % self.nickname)
                return
        SessionTable = FORMAT_USER_HALL_SESSION % (sid)
        print(u"设置超时时间的SESSIONTABLE=%s" % SessionTable)
        if publicRedis.exists(SessionTable):
            print(u"增加超时时间:%s" % self.nickname)
            publicRedis.expire(SessionTable, 60 * 40)
            privateRedis.set("session:%s:timeout" % sid, int(time.time()))
        print(u"设置超时时间结束:%s" % self.nickname)

    def resetPerGame(self):
        """
        每局需要重置的数据
        """
        self.handleMgr = self.getHandleMgr()

        self.curGameScore = 0

    def doAction(self, action, actionTiles):
        self.handleMgr.doOnAction(action, actionTiles)

    def getHandleMgr(self):
        return HandleManger(self)

    def setHandleTiles(self, tiles):
        '''
        设置手牌
        '''
        self.handleMgr.doAddTiles(tiles, draw = False)
        self.handleMgr.setMyTileCount(len(tiles))

    def getReadyHands(self, tiles):
        '''
        获得听牌列表
        '''
        return self.handleMgr.getReadyHands(tiles)

    def loadDB(self, playerTable, isInit=True, account = None):
        #配置信息
        redis = redis_instance.getInst(PUBLIC_DB)

        if isInit:
            self.table = playerTable
            self.uid = self.table.split(':')[-1]
            self.account, self.passwd, self.nickname, self.money,\
                    self.parentAg, self.currency, self.valid, self.sex, self.headImgUrl, self.maxScore = redis.hmget(playerTable, 
                        ('account', 'password', 'nickname', 'money', 'parentAg', 'currency', 'valid', 'sex', 'headImgUrl', 'maxScore'))

            self.coin, self.money = int(self.coin), round(float(self.money), 2)
            self.sex = int(self.sex) if self.sex else 0
            self.maxScore = int(self.maxScore) if self.maxScore and int(self.maxScore) >= 1 else 1
            self.headImgUrl = self.headImgUrl if self.headImgUrl else ''
            self.isGM = bool(int(redis.sismember(GM_SET, self.account)))

            roomCards = redis.get(USER4AGENT_CARD%(self.parentAg, self.uid))
            if roomCards and int(roomCards) > 0:
                self.roomCards = int(roomCards)
            else:
                self.roomCards = 0
            try:
                self.nickname = self.nickname.decode('utf-8')
            except:
                pass
        else:
            self.passwd, self.money, self.valid, self.sex, self.headImgUrl = redis.hmget(playerTable, ('password', 'money', 'valid', 'sex', 'headImgUrl'))

            self.money = round(float(self.money), 2)

            self.sex = int(self.sex) if self.sex else 0
            self.headImgUrl = self.headImgUrl if self.headImgUrl else ''

            roomCards = redis.get(USER4AGENT_CARD%(self.parentAg, self.uid))
            if roomCards and int(roomCards) > 0:
                self.roomCards = int(roomCards)
            else:
                self.roomCards = 0

    def isSessionTimeout(self, timestamp):
        return timestamp - self.lastSessionTimestamp > SESSION_TIMEOUT_TICK

    def isGameTimeout(self, timestamp):
        return timestamp - self.gameLastPacketTimestamp > GAME_KICK_OUT_TICK

    def onCheck(self, timestamp):
        if not super(CommonPlayer, self).onCheck(timestamp):
            return False
        # if self.isSessionTimeout(timestamp):

        # if self.game and self.chair == self.game.playPlayer.chair and self.isGameTimeout(timestamp) and\
                # self.game.getEmptyChair() == consts.SIDE_UNKNOWN and self.game.isInGame[self.chair]:
            # self.game.onLeaveGame(self.chair)
            # self.game.isInGame[self.chair] = False
        return True

    def drop(self, reason, reasonCode = None, type = 3):
        resp = S_C_Disconnected()
        resp.actionType = type
        if reasonCode in DROP_REASON_CODE2TXT:
            resp.reason = DROP_REASON_CODE2TXT[reasonCode]
        else:
            resp.reason = reason
        if type != 4:
            try:
                self.factory.sendOne(self, resp)
            except:
                pass
        super(CommonPlayer, self).drop(reason, reasonCode)

    def onMessage(self, payload, isBinary):
        super(CommonPlayer, self).onMessage(payload, isBinary)
        self.lastPacketTimestamp = self.factory.getTimestamp()
        self.gameLastPacketTimestamp = self.factory.getTimestamp()
        # if self.game and self.chair != consts.SIDE_UNKNOWN:
            # self.game.notLeaveGame(self.chair)
            # self.game.isInGame[self.chair] = True
            # self.game.lastPacketTimestamp = self.game.getTimestamp()
            # for gamePlayer in self.game.players:
                # if gamePlayer and self.game.isInGame[gamePlayer.chair] == True and gamePlayer != self:
                    # gamePlayer.gameLastPacketTimestamp = self.game.getTimestamp()

    def upTotalUserData(self):
        '''
        更新总得分数据
        '''
        self.totalGameScore += self.curGameScore
        self.totalKongCount += len(self.handleMgr.getKongTiles())
        self.totalConcealedKongCount += len(self.handleMgr.getConcealedKongTiles())
        self.totalBeKongCount += len(self.handleMgr.getBeKongTiles())
        huSide = self.handleMgr.getHuData()[0]
        if huSide >=0:
            if huSide == self.chair:
                self.totalSelfHuCount += 1
            else:
                self.totalOtherHuCount += 1
                self.game.players[huSide].totalGiveHuCount += 1

