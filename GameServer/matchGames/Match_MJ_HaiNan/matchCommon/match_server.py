# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/1
Revision: 1.0.0
Description: Description
"""
import time
import traceback
from datetime import datetime
import uuid

from common.log import log, LOG_LEVEL_RELEASE
from common import net_resolver_pb
from common.peer import Peer
from match_game import MatchGame
from match_player import MatchPlayer
from publicCommon.public_server import PublicServer
from publicCommon import logger_mgr
from match_mysql_twisted import mysql_twisted
from match_mgr import *
import match_pb2
from configs import CONFIGS

isMahjong = False
try:
    from common import mahjong_pb2
except:
    from common import baseProto_pb2, poker_pb2
else:
    baseProto_pb2 = mahjong_pb2
    poker_pb2 = mahjong_pb2
    isMahjong = True

s_logger = logger_mgr.s_logger


class MatchServer(PublicServer):
    protocol = MatchPlayer

    def __init__(self, *args, **kwargs):
        super(MatchServer, self).__init__(*args, **kwargs)
        self.matchMgrMap = {}
        self.waitCloseTime = 0
        self.waitCloseMoreTime = 1000 * 60  # 关服多等时间
        self.mysql_twisted = mysql_twisted(**CONFIGS['mysql'])
        self.Match_ServerInfo_Key = Key_Match_ServerInfo % (self.getGameID(), self.ip, self.port)

    def registerServiceProtocols(self):
        super(MatchServer, self).registerServiceProtocols()
        self.serviceProtoCalls.update({
            "createMatch": self.createMatch,
            "dismissMatch": self.dismissMatch,
        })

    def registerProtocolResolver(self):
        unpacker = net_resolver_pb.Unpacker
        self.recverMgr.registerCommands((
            unpacker(match_pb2.C_S_MATCHINFO, match_pb2.C_S_MatchInfo, self.C_S_MatchInfo),
            unpacker(match_pb2.C_S_NEED_TO_REFRESH, match_pb2.C_S_Need_To_Refresh, self.C_S_Need_To_Refresh),
            unpacker(match_pb2.C_S_RANKINFO, match_pb2.C_S_RankInfo, self.C_S_RankInfo),
            unpacker(match_pb2.C_S_ROTATIONDATAS, match_pb2.C_S_RotationDatas, self.C_S_RotationDatas),
            unpacker(match_pb2.C_S_GETREWARDLIST, match_pb2.C_S_getRewardList, self.C_S_getRewardList),
        ))

        packer = net_resolver_pb.Packer
        self.senderMgr.registerCommands((
            packer(match_pb2.S_C_MATCHINFO, match_pb2.S_C_MatchInfo),
            packer(match_pb2.S_C_NEED_TO_REFRESH, match_pb2.S_C_Need_To_Refresh),
            packer(match_pb2.S_C_NOTICEMSG, match_pb2.S_C_NoticeMsg),
            packer(match_pb2.S_C_RANKINFO, match_pb2.S_C_RankInfo),
            packer(match_pb2.S_C_ROTATIONDATAS, match_pb2.S_C_RotationDatas),
            packer(match_pb2.S_C_CURROUNDROOMDATAS, match_pb2.S_C_curRoundRoomDatas),
            packer(match_pb2.S_C_ROUNDBALANCE, match_pb2.S_C_RoundBalance),
            packer(match_pb2.S_C_GETREWARDLIST, match_pb2.S_C_getRewardList),
        ))

        super(MatchServer, self).registerProtocolResolver()

    def onServiceGameClose(self, timestamp):
        if self.matchMgrMap:
            self.waitCloseTime = timestamp + self.waitCloseMoreTime
        super(MatchServer, self).onServiceGameClose(timestamp)
        for matchMgr in self.matchMgrMap.itervalues():
            matchMgr.dismiss(reason=u'关服维护')

    def closeServer(self):
        timestatmp = int(time.time() * 1000)
        if timestatmp < self.waitCloseTime and self.matchMgrMap:
            return
        super(MatchServer, self).closeServer()

    def C_S_MatchInfo(self, player, req):
        if not player.game:
            log(u'[C_S_MatchInfo][error] nickname[%s] is not in game.' % (player.nickname), LOG_LEVEL_RELEASE)
            return
        log(u'[C_S_MatchInfo] room[%s] nickname[%s]' % (player.game.roomId, player.nickname), LOG_LEVEL_RELEASE)
        player.game.sendMatchInfo(player)

    def C_S_Need_To_Refresh(self, player, req):
        resp = match_pb2.S_C_Need_To_Refresh()
        if not player.game:
            log(u'[C_S_Need_To_Refresh][error] nickname[%s] is not in game.' % (player.nickname), LOG_LEVEL_RELEASE)
            resp.refreshType = 3
        else:
            log(u'[C_S_Need_To_Refresh] room[%s] nickname[%s]' % (player.game.roomId, player.nickname),
                LOG_LEVEL_RELEASE)
            resp.refreshType = 2
        self.sendOne(player, resp)

    def C_S_RankInfo(self, player, req):
        if not player.game:
            log(u'[C_S_RankInfo][error] nickname[%s] is not in game.' % (player.nickname), LOG_LEVEL_RELEASE)
            return
        log(u'[C_S_RankInfo] room[%s] nickname[%s]' % (player.game.roomId, player.nickname), LOG_LEVEL_RELEASE)
        player.game.sendRankInfo(
            getRoomRanks=req.getRoomRanks,
            getMatchRanks=req.getMatchRanks,
            sendPlayer=player
        )

    def C_S_RotationDatas(self, player, req):
        player.game.sendRotationDatas(sendPlayer=player)

    def C_S_getRewardList(self, player, req):
        player.game.getRewardList(sendPlayer=player)

    def getGameModule(self, *args, **kwargs):
        return MatchGame(*args, **kwargs)

    def createMatch(self, timestamp, matchNumber, uidsList, *args):
        uidsList = list(eval(uidsList))
        self.logger(u'[createMatch] [%s] %s' % (matchNumber, uidsList))
        _, matchId, _ = matchNumber.split('-')
        matchId = int(matchId)
        Match_Game_MatchInfo_Hesh_Key = Key_Match_Game_MatchInfo_Hesh % (self.ID, matchId)
        redis = self.getPublicRedis()
        matchInfo = redis.hgetall(Match_Game_MatchInfo_Hesh_Key)
        if self.gameCloseTimestamp:
            s_logger.error(u'[Error] [createMatch] [%s] 服务器正在关服 创建失败 matchInfo=> %s' % (matchNumber, matchInfo))
            self.createMatchFail(matchNumber=matchNumber, uidsList=uidsList, reason=u'服务器正在关服 创建失败',
                                 matchInfo=matchInfo)
            return
        if not matchInfo:
            s_logger.error(u'[Error] [createMatch] [%s] 赛事不存在' % (matchNumber))
            self.createMatchFail(matchNumber=matchNumber, uidsList=uidsList, reason=u'赛事不存在')
            return
        if len(uidsList) != int(matchInfo['play_num']):
            s_logger.error(u'[Error] [createMatch] [%s] 人数不足 创建失败 matchInfo=> %s' % (matchNumber, matchInfo))
            self.createMatchFail(matchNumber=matchNumber, uidsList=uidsList, reason=u'人数不足 创建失败', matchInfo=matchInfo)
            return
        try:
            matchMgr = MatchMgr(server=self, matchNumber=matchNumber, uidsList=uidsList, gameId=self.ID,
                                matchId=matchId, matchInfo=matchInfo)
            self.logger(u'[createMatch] %s' % matchMgr)
        except Exception as err:
            traceback.print_exc()
            for tb in traceback.format_exc().splitlines():
                self.logger(u'[createMatch] [%s] %s' % (matchNumber, tb))
            self.createMatchFail(matchNumber=matchNumber, uidsList=uidsList, reason=u'赛事创建失败', errMsg=u'%s' % err,
                                 matchInfo=matchInfo)
        else:
            self.matchMgrMap[matchNumber] = matchMgr
            matchMgr.readyStart()

    def createMatchFail(self, matchNumber, uidsList, reason=u'未知', matchInfo=None, errMsg=u''):
        if not matchInfo:
            matchInfo = {}
        self.logger(u'[createMatchFail] %s %s 原因[%s] err => %s' % (matchNumber, uidsList, reason, errMsg))
        redis = self.getPublicRedis()
        for uid in uidsList:
            Match_UserEnroll_Key = Key_Match_UserEnroll % uid
            redis.delete(Match_UserEnroll_Key)
        self.matchFailReturnFee(**dict(
            userIds=uidsList,
            matchNumber=matchNumber,
            feeType=int(matchInfo.get('feetype', 0)),
            fee=int(matchInfo.get('fee', 0)),
            dismissReason=reason
        ))

    def matchFailReturnFee(self, userIds, matchNumber, feeType=0, fee=0, dismissReason=u'未知'):
        self.send_mail(**dict(
            uids_list=userIds,
            title=u'比赛临时取消通知',
            body=u'十分抱歉，因%s的缘故，您正在参与的比赛已经取消，报名费用已通过本邮件返还。\n%s' % (dismissReason, matchNumber),
            enclosure_id=feeType,
            enclosure_num=fee,
            emailType=Email_Type.returnEnrollFee,
        ))

    def dismissMatch(self, timestamp, matchNumber, *args, **kwargs):
        self.logger(u'[dismissMatch] %s' % matchNumber)
        if matchNumber not in self.matchMgrMap:
            return
        matchMgr = self.matchMgrMap[matchNumber]
        matchMgr.dismiss(reason=u'举办方主动关闭')

    def getMatchNumber(self, matchId):
        return '%s-%s-%s' % (self.ID, matchId, int(time.time() * 1000))

    def oncreateNewMatchRoom(self, timestamp=0, **kwargs):
        redis = self.getPublicRedis()
        rule = str(self.getMatchRoomRule())
        _game = self.getGameModule(self, rule, **kwargs)
        bind_result = self.globalCtrl.addGame(_game, self.ID)
        _game.setGameNumber()
        if not bind_result:
            return

        # 保存房间信息
        pipe = redis.pipeline()
        pipe.hmset(ROOM2SERVER % _game.roomId, {
            'ip': self.ip,
            'port': self.port,
            'gameid': self.ID,
            'hidden': True,
            'playerCount': 0,
            'maxPlayer': _game.maxPlayerCount,
            'gameName': _game.roomName,
            'baseScore': _game.baseScore,
            'ruleText': _game.ruleDescs,
        })
        redis.sadd(SERVER2ROOM % (self.serviceTag), _game.roomId)
        pipe.hincrby(self.table, 'roomCount', 1)
        pipe.execute()
        log(u'[oncreateNewMatchRoom] create game succeedroom[%s].' % _game.roomId, LOG_LEVEL_RELEASE)
        return _game

    def createNewPlayerInGame(self, game, uid, matchMgr):
        userTable = FORMAT_USER_TABLE % uid

        player = game.getRobot()
        player.loadDB(userTable)
        player.userRecordMgr = matchMgr.getUserRecordMgr(uid)

        regResp = baseProto_pb2.S_C_Connected()
        regResp.result = True
        regResp.myInfo.result = True
        regResp.myInfo.isRefresh = True
        game.onJoinGame(player, regResp, False)
        game.onExitGame(player, sendMessage=False)

        if player.account in self.account2players:
            onlinePlayer = self.account2players[player.account]
            return onlinePlayer

    def getMatchRoomRule(self):
        """
        娱乐模式规则
        """
        return [2, 0, 1]

    def onGameStart(self, player, req):
        return

    def onDissolveRoom(self, player, req):
        return

    def onDissolveVote(self, player, req):
        return

    def onRefresh(self, timestamp):
        super(MatchServer, self).onRefresh(timestamp)
        serverInfoData = {
            'curPlayerNum': 0,  # 当前仍在比赛的玩家数,不算淘汰,算离线
            'curMatchNum': 0,  # 当前进行的赛事数量
        }
        for matchMgr in self.matchMgrMap.values():
            try:
                matchMgr.onTick(timestamp)
                serverInfoData['curPlayerNum'] += matchMgr.curPlayerNum
                serverInfoData['curMatchNum'] += 1
            except:
                traceback.print_exc()

        try:
            redis = self.getPublicRedis()
            redis.hmset(self.Match_ServerInfo_Key, serverInfoData)
            redis.expire(self.Match_ServerInfo_Key, 60 * 10)
        except:
            traceback.print_exc()

    def doAfterRefresh(self, player):
        try:
            player.game.sendMatchInfo(player)
            player.game.sendRankInfo(getRoomRanks=True, getMatchRanks=True, sendPlayer=player)
            player.game.sendRoomDatas(player)
            player.game.sendRotationDatas(player)
        except:
            traceback.print_exc()
        super(MatchServer, self).doAfterRefresh(player)

    def sendOne(self, peer, protocol_obj):
        assert isinstance(peer, Peer)
        try:
            self.sendData(peer, self.senderMgr.pack(protocol_obj))
        except:
            traceback.print_exc()

    def send(self, peers, protocol_obj, excludes=()):
        data = self.senderMgr.pack(protocol_obj)
        for peer in peers:
            if peer not in excludes:
                try:
                    self.sendData(peer, data)
                except:
                    traceback.print_exc()

    def onPing(self, player, game):
        if not player.game:
            player.notGamePingCount += 1
        if player.notGamePingCount >= 10:
            messsageStr = u'长时间未开始游戏，房间已自动解散'
            player.drop(reason=messsageStr, type=2)
        else:
            super(MatchServer, self).onPing(player, game)

    def onExitGame(self, player, req=None, sendMessage=True):
        if not player.game:
            log(u'[try exit game][error]nickname[%s] is not in game.' % (player.nickname), LOG_LEVEL_RELEASE)
            resp = baseProto_pb2.S_C_ExitRoomResult()
            resp.result = True
            self.sendOne(player, resp)
            return

        byPlayer = False
        if req != None:
            log(u'[try exit game]exit by player.', LOG_LEVEL_RELEASE)
            byPlayer = True

        log(u'[try exit game]nickname[%s] room[%s].' % (player.nickname, player.game.roomId), LOG_LEVEL_RELEASE)
        if not byPlayer:
            player.game.onExitGame(player, sendMessage, byPlayer)
        else:
            log(u'[try exit game][error]room[%s] is start.' % (player.game.roomId), LOG_LEVEL_RELEASE)
            resp = baseProto_pb2.S_C_ExitRoomResult()
            resp.result = False
            self.sendOne(player, resp)

    def send_mail(self, uids_list, title, body, enclosure_id=0, enclosure_num=0, emailType=Email_Type.none):
        '''
        发送邮件接口
        :param uid: 用户,多个可用逗号分隔
        :param title: 标题
        :param body: 内容
        :param enclosure_id: 附件id
        :param enclosure_num: 附件数量
        :return: None
        '''
        USER_EMAIL_SET = "user:uid:%s:email:set"
        USER_EMAIL_DATE_SET = "user:email:date:%s:set"
        EMAIL_HASH = "email:id:%s:hash"

        redis = self.getPublicRedis()
        curTime = datetime.now()
        date = curTime.strftime("%Y-%m-%d")

        awards = ''
        if enclosure_id and enclosure_num:
            awards = '%s,%s' % (enclosure_id, enclosure_num)

        if isinstance(uids_list, (int, str)):
            uids_list = [uids_list]
        for uid in uids_list:
            email_id = uuid.uuid4().hex
            redis.sadd(USER_EMAIL_DATE_SET % date, email_id)
            redis.sadd(USER_EMAIL_SET % uid, email_id)
            redis.hmset(EMAIL_HASH % email_id, {
                "title": title,
                "body": body,
                "awards": awards,
                "send_time": curTime.strftime('%Y-%m-%d %H:%M:%S'),
                "read": 0,
                "timestamp": int(time.time() * 1000),
                'email_type': '',
                'userId': uid,
                'emailType': emailType,

            })

    def getMaxPlayerCount(self):
        return 4

    def tryRmExitPlayerData(self, player, game):
        redis = self.getPublicRedis()
        pipe = redis.pipeline()

        gameNumber = redis.hget(Key_Match_PlayingUser, player.uid)
        game.logger(u'[tryRmExitPlayerData]  uid[%s] => [%s]' % (player.uid, gameNumber))
        if gameNumber == game.gameNumber:
            redis.hdel(Key_Match_PlayingUser, player.uid)

        self.removeExitPlayer(pipe, player, game)
        pipe.lrem(ROOM2ACCOUNT_LIST % (game.roomId), player.account)
        pipe.execute()
        self.removePlayerGameData(player)
        # 关闭服务器标识
        if self.isEnding:
            player.endType = 'waitEnd'
