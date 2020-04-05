#-*- coding:utf-8 -*-
#!/usr/bin/env python

"""
     party service 跟 game 之间通讯

"""

from __future__ import absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import math
import traceback
from threading import Thread, Lock
from tsconfig import *
sys.path.insert(0, '..')
sys.path.insert(0, '../mahjong')
sys.path.insert(0, '../server_common')
from model.partyModel import *
from server_common import robot_pb2
from webSocketConnection import SendManager, Packer
from websocket import create_connection
import time
import random


PREFIX_WAIT = WAIT_JOIN_PARTY_ROOM_PLAYERS
PREFIX_MATCH_PRICE = "partyMatch:price:list"
PREFIX_ACCOUNT2WAIT = ACCOUNT2WAIT_JOIN_PARTY_TABLE
PREFIX_INGAME = ALREADY_IN_PARTY_ROOM_PLAYERS
PREFIX_ACCOUNT2INGAME = ACCOUNT2ALREADY_IN_JOIN_PARTY_ROOM_TABLE
PREFIX_MATCH_FINISH = IS_MATCH_FINISHED
PROTOCOL_KEY = FORMAT_PARTY_SERVICE_PROTOCOL_TABLE
SERVICE_STATUS_KEY = FORMAT_PARTY_SERVICE_STATUS
PROTOCOL_RESULT = RESULT_PARTY_SERVICE_PROTOCOL


SEND_LABEL = False

def callBackToFunction(tofunc, timeout, *args, **kwargs):
    time.sleep(timeout)
    tofunc(*args, **kwargs)

def sendProtoBuffToServer(num, room, rType = 1, level=1):
    """ 发送添加机器人服务

    """
    global SEND_LABEL
    redis = get_inst()
    senderMgr = SendManager()
    senderMgr.registerCommands(
        (
            Packer(robot_pb2.S_S_ROBOTADDR, robot_pb2.S_S_Robotaddr),
        )
    )
    print(room)
    if not room:
        return
    if len(redis.lrange(room, 0, -1)) > 0 and not SEND_LABEL:
        ws = create_connection("ws://localhost:10001")
        resp = robot_pb2.S_S_Robotaddr()
        resp.num = int(num)
        resp.type = int(rType)
        resp.level = int(level)
        resp.roomId = room
        ws.send_binary(senderMgr.pack(resp))
        SEND_LABEL=True

def sendProtocol2OneGameService(redis, gameId, protocolStr):
    """
    发协议给某个服务器
    """
    serverList = redis.lrange(FORMAT_GAME_SERVICE_SET%(gameId), 0, -1)
    print 'sendProtocol2OneGameService11111', gameId,serverList
    if not serverList:
        return
    serverTable = serverList[0]
    _, _, _, currency, ip, port = serverTable.split(':')
    redis.rpush(FORMAT_SERVICE_PROTOCOL_TABLE%(gameId, '%s:%s:%s'%(currency, ip, port)), protocolStr)

def self_check(redis):
    global SEND_LABEL
    wait_join_lists = PREFIX_WAIT % ('*', '*', '*')
    for _key in redis.keys(wait_join_lists):
        waitplayers = redis.lrange(_key, 0, -1)
        name_list = _key.split(':')
        ag = name_list[1]
        gameid = name_list[2]
        rule = name_list[3]
        _len = len(waitplayers)
        player_count = redis.hget(GAME_TABLE % gameid, 'party_player_count')
        if not player_count or int(player_count) <= 0:
            player_count = 4
        player_count = int(player_count)
        log_debug('[wait] [waitList]%s [waitPlayers]%s' % (_key, waitplayers))
        log_debug('[wait] [_len]%s' % _len)
        log_debug('[wait] [playerCount]%s' % player_count)
        # sendProtoBuffToServer(_len, _key.strip(), rType=1, level=1)
        td = Thread(target = callBackToFunction,
                    args = (sendProtoBuffToServer,
                            random.randint(6,15),
                            player_count,
                            _key.strip(),
                            2,
                            1))
        td.start()
        while _len >= player_count:
            SEND_LABEL = False
            _len -= player_count
            players = waitplayers[:player_count]
            for account in players:
                log_debug('[wait] [popVal]%s' % redis.lpop(_key))
                redis.delete(PREFIX_ACCOUNT2WAIT % account)
                redis.set(PREFIX_MATCH_FINISH % account, player_count)
            log_debug('[succeed] [players]%s,[ag]%s,[gameId]%s,[rule]%s' % (players, ag, gameid, rule))
            sendProtocol2OneGameService(redis, gameid, "joinPartyRoom|%s|%s|%s" % (players, ag, rule))

def onFeedServiceStatus(redis, timeout):
    """
        服务状态监听 喂狗
    """
    redis.set(SERVICE_STATUS_KEY, "")
    redis.expire(SERVICE_STATUS_KEY, timeout)
    return {'code': 0}


def onPartyServiceClose():
    """
        关闭竞技场服务
    """
    redis = get_inst()
    redis.delete(PROTOCOL_KEY)
    redis.delete(SERVICE_STATUS_KEY)
    return {'code': 0}

def onJoinPartyRoom(account, ag, gameid):
    """
        加入金币场
    """
    redis = get_inst()
    rule = '[0,0,[0],1]'
    player_count = redis.hget(GAME_TABLE % gameid, 'party_player_count')
    maxplayers = int(player_count)
    exit_player_data = EXIT_PLAYER % account
    if redis.exists(exit_player_data):
        return {'code': 0}

    wait_join_list = PREFIX_WAIT % (ag, gameid, rule)
    if redis.exists(wait_join_list) and account in redis.lrange(wait_join_list, 0, -1):
        return {'code': 0}

    pipe = redis.pipeline()
    pipe.rpush(wait_join_list, account)
    pipe.set(PREFIX_ACCOUNT2WAIT % account, wait_join_list)
    pipe.execute()

    return {'code': 0}



def onCancelJoinPartyRoom(account):
    """
        取消加入竞技场
    """
    redis = get_inst()
    account2wait_table = PREFIX_ACCOUNT2WAIT % account
    if redis.exists(account2wait_table):
        wait_join_key = redis.get(account2wait_table)
        pipe = redis.pipeline()
        pipe.delete(account2wait_table)
        if redis.exists(wait_join_key) and account in redis.lrange(wait_join_key, 0, -1):
            pipe.lrem(wait_join_key, account)
        pipe.execute()
        return {'code': 0}
    return {'code': -1, 'msg': '玩家没有加入金币场'}


def onCheckJoinPartyRoom(account):
    """
        确认竞技场结果
    """
    redis = get_inst()
    account2gamein_table = PREFIX_ACCOUNT2INGAME % account
    is_matched = PREFIX_MATCH_FINISH % account
    if redis.exists(account2gamein_table):
        already_in_key = redis.get(account2gamein_table)
        key_split = already_in_key.split(':')
        gameid, ip, port = key_split[2], key_split[4], key_split[5]
        return {'code': 0, 'ip': ip, 'port': port, 'gameid': gameid}
    else:
        if redis.exists(is_matched):
            maxplayers = int(redis.get(is_matched))
            return {'code': 0, 'maxPlayers': maxplayers, 'waitPlayers': maxplayers}

        account2wait_table = PREFIX_ACCOUNT2WAIT % account
        wait_join_key = redis.get(account2wait_table)
        if wait_join_key:
            gameid = wait_join_key.split(':')[2]
            player_count = redis.hget(GAME_TABLE % gameid, 'party_player_count')
            if not player_count:
                return {'code': -1, 'msg': '相关配置异常，加入失败'}
            maxplayers = int(player_count)
            wait_join_list = redis.lrange(wait_join_key, 0, -1)
            if account in wait_join_list:
                return {'code': 0, 'maxPlayers': maxplayers, 'waitPlayers': len(wait_join_list)}

    return {'code': -1, 'msg': '未申请加入竞技场'}


def onJoinPartyRoomSuccess(server_table, accountlist, ag, rule):
    """
        收到创建金币场房间成功消息
        扣除钻石
        设置状态
    """
    redis = get_inst()
    accountlist = list(eval(accountlist))
    key_split = server_table.split(':')
    gameid = key_split[3]
    ip = key_split[5]
    port = key_split[6]
    already_in_list = PREFIX_INGAME % (ag, gameid, rule, ip, port)
    pipe = redis.pipeline()
    for account in accountlist:
        pipe.rpush(already_in_list, account)
        pipe.set(PREFIX_ACCOUNT2INGAME % account, already_in_list)
        pipe.delete(PREFIX_MATCH_FINISH % account)
    # 报名费
    pipe.set(PARTY_GAME_ENTER_ROOM_CRADS, 1)
    # 更新运营数据
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    if not redis.exists(PARTY_GAME_OPERATE_BY_DAY_TABLE % today):
        player_count, online_count, online_max, party_count = 0, 0, 0, 0
    else:
        player_count, online_count, online_max, party_count = redis.hmget(PARTY_GAME_OPERATE_BY_DAY_TABLE % today,
                                                                         ('player_count','online_count', 'online_max',
                                                                          'party_count'))

    player_count = int(player_count) + len(accountlist)
    online_count = int(online_count) + len(accountlist)
    party_count = int(party_count) + 1
    if online_count > online_max:
        online_max = int(online_max) + online_count
    pipe.hmset(PARTY_GAME_OPERATE_BY_DAY_TABLE % today, {'date': today,
                                                         'player_count': player_count,
                                                         'party_count': party_count,
                                                         'online_count': online_count,
                                                         'online_max': online_max})

    pipe.execute()
    return {'code': 0}


def onPartyRoomLeaveSuccess(server_table, accountlist):
    """

    """
    redis = get_inst()
    accountlist = list(eval(accountlist))
    pipe = redis.pipeline()
    for account in accountlist:
        account2gamein_table = PREFIX_ACCOUNT2INGAME % account
        if redis.exists(account2gamein_table):
            already_in_key = redis.get(account2gamein_table)
            pipe.delete(account2gamein_table)
            if redis.exists(already_in_key) and account in redis.lrange(already_in_key, 0, -1):
                pipe.lrem(already_in_key, account)
    pipe.execute()
    return {'code': 0}


def get_party_game_player_count(gameid):
    """ 
        根据gameid获取参与游戏人数
    """
    redis = get_inst()
    player_count = redis.hget(GAME_TABLE % gameid, 'party_player_count')
    if not player_count or int(player_count) <= 0:
        player_count = 4
    player_count = int(player_count)
    return player_count


def onPartyRoomBalanceSuccess(server_table, data):
    """
        竞技场结算
    """
    redis = get_inst()
    data = eval(data)
    gameid = server_table.split(':')[3]
    account_list = data.keys()
    scores = data.values()
    max_score = max(scores)
    max_list = []
    per_persume = int(redis.get(PARTY_GAME_ENTER_ROOM_CRADS))
    if max_score == 0:
        print u'所有人平局'
    for account, score in data.iteritems():
        if score == max_score:
            max_list.append(account)
    per_count = int(math.ceil((get_party_game_player_count(gameid)-1)/len(max_list)))
    print 'test ************************  {0}'.format(per_count)
    # 竞技场记录
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    table_id = redis.incr(PARTY_GAME_RECORD_COUNT_TABLE)

    record_info = {}
    record_info['id'] = table_id
    record_info['date'] = now.strftime("%Y-%m-%d %H:%M:%S")
    record_info['gameid'] = gameid

    pipe = redis.pipeline()
    for account in account_list:
        if account in max_list:
            result = per_count - per_persume
        else:
            result = 0 - per_persume
        if max_score == 0:
            desc = u'平'
        else:
            if result < 0:
                desc = u'负'
            else:
                desc = u'胜'
        record_info[account] = {'result': result, 'desc':desc, 'win_rate':0}
        # 当日钻石消耗统计
        agentid = redis.hget(getUserByAccount(redis, account), 'parentAg')
        redis.incr(PARTY_GAME_ROOM_CRADS_BY_DAY % (today, agentid, account), result)
        # 胜局排行榜
        if desc == u'胜':
            pipe.zincrby(PARTY_GAME_RANK_WITH_AGENT_TABLE % (today, agentid), account, 1)
            pipe.lpush(PARTY_GAME_RECORD_ACCOUNT_WIN_LIST % (today, agentid, account), table_id)
        pipe.lpush(PARTY_GAME_RECORD_ACCOUNT_TOTAL_LIST % (today, agentid, account), table_id)
    # 单局记录表
    pipe.hmset(PARTY_GAME_RECORD_TABLE % (today, table_id), record_info)
    # 运营表数据
    online_count = redis.hget(PARTY_GAME_OPERATE_BY_DAY_TABLE % today, 'online_count')
    online_count = int(online_count) - len(account_list)
    winner_count, winner_result = get_party_game_winner(redis, today)
    loser_count, loser_result = get_party_game_loser(redis, today)
    pipe.hmset(PARTY_GAME_OPERATE_BY_DAY_TABLE % today, {'online_count': online_count,
                                                         'winner_count': winner_count,
                                                         'winner_result': winner_result,
                                                         'loser_count': loser_count,
                                                         'loser_result': loser_result})
    pipe.execute()
    return {'code': 0}


class SchedulerWorker(object):
    def __init__(self, thread_num=5):
        self.mutex = Lock()
        self.thread_num = thread_num
        self.serviceProtocolTable = PROTOCOL_KEY
        self.serviceStatus = SERVICE_STATUS_KEY
        self.serviceProtoCalls = []
        self.registerServiceProtocols()

    def run(self):
        log_debug('SchedulerWorker ***************************')
        self.spawn_worker()

    def spawn_worker(self):
        t_list = []
        for th_i in range(self.thread_num):
            t_threading = Thread(target=self.spawn_handler, args=())
            t_list.append(t_threading)
        for th_i in t_list:
            th_i.setDaemon(True)
            th_i.start()

    def spawn_handler(self):
        while True:
            if self.mutex.acquire(1):
                self.readPartyServiceProtocol()
                self.mutex.release()
            time.sleep(0.1)

    def registerServiceProtocols(self):
        """
            注册协议
        """
        self.serviceProtoCalls = {
            'close': onPartyServiceClose,
            'joinPartyRoom': onJoinPartyRoom,
            'cancelJoinPartyRoom': onCancelJoinPartyRoom,
            'checkJoinPartyRoom': onCheckJoinPartyRoom,

            'joinPartyRoomSuccess': onJoinPartyRoomSuccess,
            'PartyRoomLeaveSuccess': onPartyRoomLeaveSuccess,
            'PartyRoomBalanceSuccess': onPartyRoomBalanceSuccess,
        }

    def appendServiceProtocols(self, params):
        """ 
            拓展协议
        """
        if not isinstance(params, dict):
            return
        self.serviceProtoCalls.update(params)


    def readPartyServiceProtocol(self):
        """ 
            协议处理
        """
        redis = get_inst()
        if not isPartyServiceOpening(redis):
            return
        protoName = redis.lpop(self.serviceProtocolTable)
        while protoName:
            log_debug('protoName[%s]' % protoName)
            uuid = protoName[-32:]
            protoName = protoName[:-32]
            protoArgs = protoName.split('|')
            if protoArgs:
                protoHead = protoArgs[0]
                if protoHead in self.serviceProtoCalls:
                    try:
                        result = self.serviceProtoCalls[protoHead](*protoArgs[1:])
                        redis.set(PROTOCOL_RESULT % uuid, json.dumps(result))
                        redis.expire(PROTOCOL_RESULT % uuid, 5)
                    except:
                        traceback.print_exc()
            protoName = redis.lpop(self.serviceProtocolTable)