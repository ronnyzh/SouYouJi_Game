# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/11/5
Revision: 1.0.0
Description: Description
"""
from pprint import pformat
import tornado
import tornado.httpclient
import tornado.gen
import tornado.ioloop
from tornado import options
import os

from server.factorys.socketFactory import SocketFactory, Packer, Unpacker
from server.managers.match_manager import MatchMgr
from server.socketHandler.matchSocketHandler import *
from server.focusHandler.matchFocusHandler import *
from public.public_sqlFormat import *
from public import public_func
from define.define_consts import *
from define.define_redis_key import *
from define.define_mysql_key import *
from proto import hall_match_pb2


class MatchResponseMgr(object):
    def response_chat_msg_accept(self, sendMsg, sender=None, msgType=None):
        if not msgType:
            msgType = 'system'
            if sender:
                msgType = 'user'
        sendResp = dict(
            url="/chat/msg_accept",
            code=0,
            data=dict(
                msg=sendMsg,
                type=msgType,
                sendTime=getNowStamp(millisecond=True),
            ),
            msg='接收到聊天消息'
        )
        sendResp['data']['sender'] = dict(nickname=sender.nickname)
        return sendResp


class MatchFactory(SocketFactory):
    def __init__(self, *args, **kwargs):
        super(MatchFactory, self).__init__(*args, **kwargs)
        self.redisMatchInfoMap = {}  # 赛事redis数据
        self.matchMgrMap = {}  # 赛事管理类Map
        self.matchInfoMap = {}  # 赛事redis数据

        self.pushMatchList_lastTime = 0  # 上一次推送时间
        self.pushMatchList_interval = 5 * 1000  # 推送间隔
        self.doingCheckHallServer = False

        self.system = getCurSystem()

        self.add_PeriodicCallback(callback=self.checkHallServer, callback_time=15 * 1000, rightAwayDo=True)
        if options.options.checkDoMysqlJob:
            self.add_PeriodicCallback(callback=self.checkDoMysqlJob, callback_time=30 * 1000, rightAwayDo=True,
                                      jitter=0.1)
        if options.options.zipLogs:
            self.add_PeriodicCallback(callback=self.doZipLogs, callback_time=6 * 3600 * 1000, rightAwayDo=False)

    def doZipLogs(self):
        self.log('[doZipLogs]')
        if self.system == system_Windows:
            os.system('start python3 logs/doZipLogs.py')
        elif self.system == system_Linux:
            os.system('python3 logs/doZipLogs.py &')
        else:
            os.system('python3 logs/doZipLogs.py')

    def resetMatchMgrAndInfo(self):
        self.matchMgrMap = {}  # 赛事管理类Map
        self.matchInfoMap = {}  # 赛事redis数据

    def getMatchMgr(self, gameId: int, matchId: int):
        try:
            return self.matchMgrMap[gameId][matchId]
        except:
            traceback.print_exc()
            for tb in traceback.format_exc().splitlines():
                self.log(u'[ERROR][getMatchMgr] %s' % (tb), level='error')
            return None

    def getMatchInfoMap(self, gameId: int, matchId: int = 0) -> [dict, list]:
        try:
            if not gameId:
                return {}
            if not matchId:
                return self.matchInfoMap[gameId]
            return self.matchInfoMap[gameId][matchId]
        except:
            traceback.print_exc()
            for tb in traceback.format_exc().splitlines():
                self.log(u'[ERROR][getMatchInfoMap] %s' % (tb), level='error')
            return {}

    def doCloseServer(self):
        super(MatchFactory, self).doCloseServer()

    def doBeforeServerStart(self):
        super(MatchFactory, self).doBeforeServerStart()
        self.updateMatchData()

    def onTick(self, timeStamp: int) -> None:
        super(MatchFactory, self).onTick(timeStamp)
        self.log('[onTick] 当前在线 %s' % list(self.uidSocketMgrs.keys()))

        redis = getInst()
        if self.curServerStage == ServerStage.readyClose:
            redis.srem(Key_Server_Set, self.serverTag)
            for uid, socket in self.uidSocketMgrs.items():
                socket.close(code=1000, reason='服务器关闭中')
            return
        redis.sadd(Key_Server_Set, self.serverTag)
        self.updateMatchData()
        for _gameId in self.matchMgrMap:
            _, cbDatas = MatchOperate.getServerList(self=self, gameId=_gameId)
            serverList = cbDatas['serverList']
            if not serverList:
                self.log('[%s]服务器未开启' % _gameId)
                continue
            for matchId, matchMgr in self.matchMgrMap[_gameId].items():
                try:
                    matchMgr.onCheck(serverList, timeStamp)
                except:
                    traceback.print_exc()
                    for tb in traceback.format_exc().splitlines():
                        self.log(u'[ERROR][onTick] %s' % (tb), level='error')
        for uid, socket in self.uidSocketMgrs.items():
            try:
                socket.user_OnTick(timeStamp)
            except:
                traceback.print_exc()
                for tb in traceback.format_exc().splitlines():
                    self.log(u'[ERROR][onTick] %s' % (tb), level='error')
        if not self.pushMatchList_lastTime:
            self.pushMatchList_lastTime = timeStamp
        elif timeStamp - self.pushMatchList_lastTime >= self.pushMatchList_interval:
            self.push_match_infoList()
            self.pushMatchList_lastTime = timeStamp

    def checkHallServer(self):
        if self.curServerStage == ServerStage.readyClose:
            pass
        else:
            tornado.ioloop.IOLoop.current().spawn_callback(self._checkHallServer)

    async def _checkHallServer(self):
        def checkCallBack(serverTag):
            def _checkCallBack(future, *args, **kwargs):
                try:
                    result = future.result()
                    self.log('[checkHallServer] [%s]返回 [%s]' % (serverTag, result))
                    if result.code == 200:
                        return
                except Exception as err:
                    self.log('[checkHallServer][Error] [%s] [%s]' % (serverTag, err))
                redis = getInst()
                redis.srem(Key_Server_Set, serverTag)
                self.log('[checkHallServer] [%s]无法访问,移除' % serverTag)

            return _checkCallBack

        try:
            redis = getInst()
            hallServerSet = redis.smembers(Key_Server_Set)
            self.log('[checkHallServer] %s' % list(hallServerSet))
            http_client = tornado.httpclient.AsyncHTTPClient()
            for serverTag in hallServerSet:
                if serverTag == self.serverTag:
                    continue
                url = 'http://%s/ping' % (serverTag)
                future = http_client.fetch(url, raise_error=False)
                future.add_done_callback(checkCallBack(serverTag))
        except:
            traceback.print_exc()
            for tb in traceback.format_exc().splitlines():
                self.log(u'[ERROR][_checkHallServer] %s' % (tb), level='error')

    def updateMatchData(self):
        redis = getInst()
        newRedisMatchInfoMap = {}
        for _gameId_ in listStrToInt(redis.smembers(Key_Match_GameId_Set), isSorted=True):
            matchIds = listStrToInt(redis.smembers(Key_Match_Game_MatchId_Set % _gameId_), isSorted=True)
            for _matchId in matchIds:
                matchInfo = redis.hgetall(Key_Match_Game_MatchInfo_Hesh % (_gameId_, _matchId))
                newRedisMatchInfoMap.setdefault(_gameId_, {})
                newRedisMatchInfoMap[_gameId_][_matchId] = matchInfo
        if newRedisMatchInfoMap == self.redisMatchInfoMap:
            self.log('[updateMatchData] 一致,不需要更新')
            return
        else:
            self.log('[updateMatchData] 不一致,需要更新')
        self.redisMatchInfoMap = newRedisMatchInfoMap
        self.resetMatchMgrAndInfo()
        for _gameId, _datas in self.redisMatchInfoMap.items():
            for _matchId, _matchInfo in _datas.items():
                try:
                    matchMgr = MatchMgr(self, **_matchInfo)
                    self.matchMgrMap.setdefault(_gameId, {})
                    self.matchInfoMap.setdefault(_gameId, {})
                    self.matchMgrMap[_gameId][_matchId] = matchMgr
                    self.matchInfoMap[_gameId][_matchId] = matchMgr.matchInfo
                except:
                    traceback.print_exc()
                    for tb in traceback.format_exc().splitlines():
                        self.log(u'[ERROR][updateMatchData] %s' % (tb), level='error')
                else:
                    pass
        self.log('[updateMatchData] 完成更新')
        self.log(msg=pformat(self.matchMgrMap))

    def update_redisMatchInfo_enrollNum(self, gameId, matchId, enrollNum):
        redis = getInst()
        Match_Game_MatchInfo_Key = Key_Match_Game_MatchInfo_Hesh % (gameId, matchId)
        redis.hset(Match_Game_MatchInfo_Key, 'enrollNum', enrollNum)
        try:
            self.redisMatchInfoMap[gameId][matchId]['enrollNum'] = str(enrollNum)
        except:
            traceback.print_exc()
            for tb in traceback.format_exc().splitlines():
                self.log(u'[ERROR][update_redisMatchInfo_enrollNum] %s' % (tb), level='error')

    def getPeers(self):
        return self.uidSocketMgrs.values()

    def push_match_infoList(self):
        sendResp = self.getResp_S_C_match_infoList_get()
        sendResp.isPush = True
        if sendResp.code != 0:
            return
        sendResp.msg = '服务器主动更新'
        for peer in self.getPeers():
            if not peer.isNeedAutoPush:
                continue
            tmpSendResp = copy.deepcopy(sendResp)
            _, cb_data = MatchOperate.getUserMatchEnrollInfo(self=self, uid=peer.uid)
            enrollInfo = cb_data.get('enrollInfo', {})
            if enrollInfo:
                self.setKey_enrollInfo(tmpSendResp, enrollInfo)
            self.sendOne(peer, tmpSendResp)

    def createMatch(self, gameId, matchNumber, uidsList, saveData, **kwargs):
        createMatchKey = "createMatch|%s|%s" % (matchNumber, str(uidsList))
        serverTable = '%s:%s' % (saveData['ip'], saveData['port'])
        self.sendProtocol2GameService(gameId, protocolStr=createMatchKey, serviceFind=serverTable)

    def registerProtocolResolver(self):
        unpacker = Unpacker
        self.recverMgr.registerCommands((
            unpacker(hall_match_pb2.header_C_S_Ping, hall_match_pb2.C_S_Ping, self.C_S_Ping),

            unpacker(hall_match_pb2.header_C_S_match_isAutoPush, hall_match_pb2.C_S_match_isAutoPush,
                     self.C_S_match_isAutoPush),
            unpacker(hall_match_pb2.header_C_S_match_infoList_get, hall_match_pb2.C_S_match_infoList_get,
                     self.C_S_match_infoList_get),
            unpacker(hall_match_pb2.header_C_S_match_enroll_get, hall_match_pb2.C_S_match_enroll_get,
                     self.C_S_match_enroll_get),
            unpacker(hall_match_pb2.header_C_S_match_enroll_do, hall_match_pb2.C_S_match_enroll_do,
                     self.C_S_match_enroll_do),
            unpacker(hall_match_pb2.header_C_S_match_enroll_cancel, hall_match_pb2.C_S_match_enroll_cancel,
                     self.C_S_match_enroll_cancel),
            unpacker(hall_match_pb2.header_C_S_match_readyJoin_tips_ignore,
                     hall_match_pb2.C_S_match_readyJoin_tips_ignore, self.C_S_match_readyJoin_tips_ignore),
        ))
        packer = Packer
        self.senderMgr.registerCommands((
            packer(hall_match_pb2.header_S_C_Ping, hall_match_pb2.S_C_Ping),
            packer(hall_match_pb2.header_S_C_Disconnected, hall_match_pb2.S_C_Disconnected),

            packer(hall_match_pb2.header_S_C_match_isAutoPush, hall_match_pb2.S_C_match_isAutoPush),
            packer(hall_match_pb2.header_S_C_match_infoList_get, hall_match_pb2.S_C_match_infoList_get),
            packer(hall_match_pb2.header_S_C_match_enroll_get, hall_match_pb2.S_C_match_enroll_get),
            packer(hall_match_pb2.header_S_C_match_enroll_do, hall_match_pb2.S_C_match_enroll_do),
            packer(hall_match_pb2.header_S_C_match_enroll_cancel, hall_match_pb2.S_C_match_enroll_cancel),
            packer(hall_match_pb2.header_S_C_match_readyJoin_tips_ignore,
                   hall_match_pb2.S_C_match_readyJoin_tips_ignore),
            packer(hall_match_pb2.header_S_C_match_readyJoin_tips, hall_match_pb2.S_C_match_readyJoin_tips),
        ))

    def C_S_Ping(self, peer, resp):
        sendResp = hall_match_pb2.S_C_Ping()
        self.sendOne(peer, sendResp)

    def C_S_match_isAutoPush(self, peer, resp):
        if resp.isAuto in [AutoPushActionType.notAuto, AutoPushActionType.needAuto]:
            peer.isNeedAutoPush = resp.isAuto
        sendResp = hall_match_pb2.S_C_match_isAutoPush()
        sendResp.isAuto = peer.isNeedAutoPush
        self.sendOne(peer, sendResp)

    def C_S_match_enroll_get(self, peer, resp):
        sendResp = hall_match_pb2.S_C_match_enroll_get()
        _, cb_data = MatchOperate.getUserMatchEnrollInfo(self=self, uid=peer.uid)

        enrollInfo = cb_data.get('enrollInfo', {})
        if enrollInfo:
            self.setKey_enrollInfo(sendResp, enrollInfo)
            enroll_gameId = enrollInfo.get('gameId')
            enroll_matchId = enrollInfo.get('matchId')
            matchInfo = self.getMatchInfoMap(enroll_gameId, enroll_matchId)
            self.setKey_matchEnrollNum(sendResp, matchInfo)

        self.sendOne(peer, sendResp)

    def C_S_match_enroll_do(self, peer, resp):
        sendResp = hall_match_pb2.S_C_match_enroll_do()
        sendResp.gameId = gameId = resp.gameId
        sendResp.matchId = matchId = resp.matchId
        flag, cb_data = MatchFocusHandler.enroll_do(self=self, uid=peer.uid, gameId=gameId, matchId=matchId)
        sendResp.code = cb_data.get('code', 0)
        sendResp.msg = cb_data.get('msg', '成功')

        enrollInfo = cb_data.get('data', {}).get('enrollInfo', {})
        changeTrade = cb_data.get('data', {}).get('changeTrade', {})
        if enrollInfo:
            self.setKey_enrollInfo(sendResp, enrollInfo)
            enroll_gameId = enrollInfo.get('gameId')
            enroll_matchId = enrollInfo.get('matchId')
            matchInfo = self.getMatchInfoMap(enroll_gameId, enroll_matchId)
            self.setKey_matchEnrollNum(sendResp, matchInfo)
        if changeTrade:
            self.setKey_changeTrade(sendResp, changeTrade)

        self.sendOne(peer, sendResp)

    def C_S_match_enroll_cancel(self, peer, resp):
        sendResp = hall_match_pb2.S_C_match_enroll_cancel()
        sendResp.gameId = gameId = resp.gameId
        sendResp.matchId = matchId = resp.matchId
        flag, cb_data = MatchFocusHandler.enroll_cancle(self=self, uid=peer.uid, gameId=gameId, matchId=matchId)
        sendResp.code = cb_data.get('code', 0)
        sendResp.msg = cb_data.get('msg', '成功')

        enrollInfo = cb_data.get('data', {}).get('enrollInfo', {})
        changeTrade = cb_data.get('data', {}).get('changeTrade', {})
        if enrollInfo:
            self.setKey_enrollInfo(sendResp, enrollInfo)
            enroll_gameId = enrollInfo.get('gameId')
            enroll_matchId = enrollInfo.get('matchId')
            matchInfo = self.getMatchInfoMap(enroll_gameId, enroll_matchId)
            self.setKey_matchEnrollNum(sendResp, matchInfo)
        else:
            matchInfo = self.getMatchInfoMap(gameId, matchId)
            self.setKey_matchEnrollNum(sendResp, matchInfo)
        if changeTrade:
            self.setKey_changeTrade(sendResp, changeTrade)
        self.sendOne(peer, sendResp)

    def C_S_match_readyJoin_tips_ignore(self, peer, resp):
        ignoreSecond = resp.ignoreSecond
        peer.readyJoinIgnoreTime = getNowStamp(millisecond=True) + ignoreSecond * 1000
        sendResp = hall_match_pb2.S_C_match_readyJoin_tips_ignore()
        sendResp.ignoreSecond = ignoreSecond
        self.sendOne(peer, sendResp)

    def C_S_match_infoList_get(self, peer, resp):
        gameId = resp.gameId
        matchId = resp.matchId
        sendResp = self.getResp_S_C_match_infoList_get(gameId=gameId, matchId=matchId)
        _, cb_data = MatchOperate.getUserMatchEnrollInfo(self=self, uid=peer.uid)
        enrollInfo = cb_data.get('enrollInfo', {})
        if enrollInfo:
            self.setKey_enrollInfo(sendResp, enrollInfo)
        sendResp.msg = sendResp.msg
        self.sendOne(peer, sendResp)

    def getResp_S_C_match_infoList_get(self, gameId=0, matchId=0):
        needShowData = []
        sendResp = hall_match_pb2.S_C_match_infoList_get()
        sendResp.gameId = gameId
        sendResp.matchId = matchId
        if gameId:
            gameIds = [gameId]
            if gameId not in self.matchMgrMap:
                sendResp.msg = u'赛事游戏错误, 无该游戏的相关赛事'
                sendResp.code = -1
            elif matchId and matchId not in self.matchMgrMap[gameId]:
                sendResp.msg = u'赛事Id错误, 该游戏无当前赛事Id的赛事'
                sendResp.code = -1
            if sendResp.code != 0:
                return sendResp
        else:
            gameIds = self.matchInfoMap.keys()
        for _gameId in gameIds:
            if matchId:
                needShowData.append(self.matchInfoMap[_gameId][matchId])
            else:
                for _matchId, _matchInfo in self.matchInfoMap[_gameId].items():
                    needShowData.append(_matchInfo)
        self.setKey_matchList(sendResp, needShowData)
        return sendResp

    def setKey_matchList(self, resp, matchList):
        matchListResp = resp.data.matchList
        matchListResp.gameId = resp.gameId
        matchListResp.matchId = resp.matchId
        for matchInfo in matchList:
            matchDatasResp = matchListResp.matchDatas.add()
            for _key, _value in matchInfo.items():
                if hasattr(matchDatasResp, _key):
                    setattr(matchDatasResp, _key, _value)

    def setKey_enrollInfo(self, resp, enrollInfo):
        self.setKey_Resp(resp=resp, keyName='enrollInfo', dataDicts=enrollInfo)

    def setKey_changeTrade(self, resp, changeTrade):
        changeTradeResp = resp.data.changeTrade.add()
        for _key, _value in changeTrade.items():
            if hasattr(changeTradeResp, _key):
                setattr(changeTradeResp, _key, _value)

    def setKey_matchJoinInfo(self, resp, **matchJoinInfo):
        self.setKey_Resp(resp=resp, keyName='matchJoinInfo', dataDicts=matchJoinInfo)

    def setKey_matchEnrollNum(self, resp, matchInfoLists):
        if not matchInfoLists:
            return
        if isinstance(matchInfoLists, dict):
            newMatchInfoLists = [matchInfoLists]
        else:
            newMatchInfoLists = matchInfoLists
        for _matchInfo in newMatchInfoLists:
            matchEnrollNumResp = resp.data.matchEnrollNum.add()
            for _key, _value in _matchInfo.items():
                if hasattr(matchEnrollNumResp, _key):
                    setattr(matchEnrollNumResp, _key, _value)

    def setKey_Resp(self, resp, keyName, dataDicts):
        if not dataDicts:
            return
        keyResp = getattr(resp.data, keyName, {})
        for _key, _value in dataDicts.items():
            if hasattr(keyResp, _key):
                setattr(keyResp, _key, _value)

    def checkDoMysqlJob(self):
        if self.curServerStage == ServerStage.readyClose:
            pass
        else:
            tornado.ioloop.IOLoop.current().spawn_callback(self.doMysqlJob)

    async def doMysqlJob(self, redisKey=Key_Match_Mysql_Jobs):
        if not redisKey:
            return
        self.log(u'[doMysqlJob] redisKey[%s]' % (redisKey))
        redis = getInst()
        if redis.exists(redisKey):
            tryCount = redis.llen(redisKey)
            tryCount = 10 if tryCount > 10 else tryCount
            mysqlDb = self.getAsyncMysqlDB()
            if not mysqlDb.checkPool():
                return
            while tryCount:
                tryCount -= 1
                sqlStr = ''
                sqlArgs = None
                job = redis.lpop(redisKey)
                if not job:
                    break
                self.log(u'[doMysqlJob] %s' % job)
                try:
                    jobData = json.loads(job)
                    tableName = jobData['tableName']
                    method = jobData['method']
                    data = jobData['data']
                    if tableName == Table_match_record:
                        sqlStr, sqlArgs = self.getSql_match_record(method=method, data=data)
                    elif tableName == Table_match_player:
                        sqlStr, sqlArgs = self.getSql_match_player(method=method, data=data)
                    if sqlStr:
                        self.log(u'[doMysqlJob] sqlStr => %s sqlArgs => %s' % (sqlStr, sqlArgs))
                        assert method in SQL_Method.MethodList
                        if method == SQL_Method.INSERT:
                            result = await mysqlDb.insert(sqlStr, sqlArgs)
                        elif method == SQL_Method.UPDATE:
                            result = await mysqlDb.update(sqlStr, sqlArgs)
                            assert result
                        elif method == SQL_Method.DELETE:
                            result = await mysqlDb.delete(sqlStr, sqlArgs)
                            assert result
                        elif method == SQL_Method.SELECT:
                            result = await mysqlDb.query(sqlStr, sqlArgs)
                        else:
                            result = await mysqlDb.execute(sqlStr, sqlArgs)
                        self.log(u'[doMysqlJob] result => %s' % (result))
                    else:
                        self.log(u'[doMysqlJob] 暂无处理,放回队列')
                        redis.rpush(redisKey, job)
                except:
                    traceback.print_exc()
                    for tb in traceback.format_exc().splitlines():
                        self.log(u'[ERROR][doMysqlJob] %s' % (tb), level='error')
                    redis.rpush(Key_Match_Mysql_Jobs_Error, job)
        if redisKey != Key_Match_Mysql_Jobs_Error and not redis.exists(redisKey):
            await self.doMysqlJob(redisKey=Key_Match_Mysql_Jobs_Error)

    def getSql_match_record(self, method, data):
        datasDict = public_func.dictParseValue(parserObj={
            'game_id': {'type': int},
            'match_id': {'type': int},
            'match_number': {'type': str, 'isMust': True},
            'fee_type': {'type': int},
            'total_fee': {'type': int},
            'total_num': {'type': int},
            'total_award_type': {'type': int},
            'total_award_num': {'type': int},
            'match_Info': {'type': str, 'isMust': method == SQL_Method.INSERT},
            'start_time': {'type': int},
            'end_time': {'type': int},
            'dismissReason': {'type': str},
            'matchState': {'type': int},
        }, onlyParseKey=True, **data)

        if 'start_time' in datasDict:
            datasDict['start_time'] = timeStampTo_Second(datasDict['start_time'])
        if 'end_time' in datasDict:
            datasDict['end_time'] = timeStampTo_Second(datasDict['end_time'])

        if method == SQL_Method.INSERT:
            datasDict['create_time'] = getNowStamp()
            sqlCls = FormatSql_Insert(**dict(
                tableName=Table_match_record,
                datasDict=datasDict,
            ))
            return sqlCls.getSqlStrAndArgs()
        elif method == SQL_Method.UPDATE:
            datasDict['update_time'] = getNowStamp()
            sqlCls = FormatSql_Update(**dict(
                tableName=Table_match_record,
                datasDict=datasDict,
                whereParams={
                    'data': {'match_number': datasDict['match_number']},
                },
            ))
            return sqlCls.getSqlStrAndArgs()

    def getSql_match_player(self, method, data):
        datasDict = public_func.dictParseValue(parserObj={
            'user_id': {'type': int},
            'game_id': {'type': int},
            'match_id': {'type': int},
            'match_number': {'type': str, 'isMust': True},
            'fee_type': {'type': int},
            'fee': {'type': int},
            'score': {'type': int},
            'rank': {'type': int},
            'reward_type': {'type': int},
            'reward_fee': {'type': int},
        }, onlyParseKey=True, **data)

        if method == SQL_Method.INSERT:
            datasDict['create_time'] = getNowStamp()
            sqlCls = FormatSql_Insert(**dict(
                tableName=Table_match_player,
                datasDict=datasDict,
            ))
            return sqlCls.getSqlStrAndArgs()
        elif method == SQL_Method.UPDATE:
            datasDict['update_time'] = getNowStamp()
            sqlCls = FormatSql_Update(**dict(
                tableName=Table_match_player,
                datasDict=datasDict,
                whereParams={
                    'data': {'match_number': datasDict['match_number']},
                },
            ))
            return sqlCls.getSqlStrAndArgs()
