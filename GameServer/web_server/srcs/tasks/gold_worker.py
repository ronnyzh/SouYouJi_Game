#-*- coding:utf-8 -*-
#!/usr/bin/env python

"""
     gold service 跟 game 之间通讯

"""
import json
import traceback
from threading import Thread, Lock
from tsconfig import *
sys.path.insert(0, '..')
sys.path.insert(0, '../mahjong')
sys.path.insert(0, '../server_common')
from web_db_define import FORMAT_GAME_SERVICE_SET, FORMAT_SERVICE_PROTOCOL_TABLE, GAME_TABLE, EXIT_PLAYER
from model.gold_db_define import *
import robot_pb2
from webSocketConnection import SendManager, Packer
from websocket import create_connection
import time
import random

init_log('gold')

PREFIX_WAIT = WAIT_JOIN_GOLD_ROOM_PLAYERS
PREFIX_ACCOUNT2WAIT = ACCOUNT2WAIT_JOIN_GOLD_ROOM_TABLE
PREFIX_INGAME = ALREADY_IN_GOLD_ROOM_PLAYERS
PREFIX_ACCOUNT2INGAME = ACCOUNT2ALREADY_IN_JOIN_GOLD_ROOM_TABLE
PREFIX_MATCH_FINISH = IS_GOLD_ROOM_MATCH_FINISHED
PROTOCOL_KEY = FORMAT_GOLD_SERVICE_PROTOCOL_TABLE
SERVICE_STATUS_KEY = FORMAT_GOLD_SERVICE_STATUS
PROTOCOL_RESULT = RESULT_GOLD_SERVICE_PROTOCOL

SEND_LABEL = False

def callBackToFunction(tofunc, timeout, *args, **kwargs):
    time.sleep(timeout)
    tofunc(*args, **kwargs)

def sendProtoBuffToServer(num, room, rType = 1, level=1):
    """ 发送添加机器人服务

    """
    global  SEND_LABEL
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
        playid = name_list[1]
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
        '''
        td = Thread(target=callBackToFunction,
                    args=(sendProtoBuffToServer,
                          random.randint(6, 15),
                          player_count,
                          _key.strip(),
                          1,
                          1))
        td.start()
        '''

        # sendProtoBuffToServer(player_count, _key.strip(), 1, 1)
        while _len >= player_count:
            SEND_LABEL = False
            _len -= player_count
            players = waitplayers[:player_count]
            for account in players:
                log_debug('[wait] [popVal]%s' % redis.lpop(_key))
                redis.delete(PREFIX_ACCOUNT2WAIT % account)
                redis.set(PREFIX_MATCH_FINISH % account, player_count)
            log_debug('[succeed] [players]%s,[ag]%s,[gameId]%s,[rule]%s' % (players, playid, gameid, rule))
            sendProtocol2OneGameService(redis, gameid, "joinGoldRoom|%s|%s|%s" % (players, playid, rule))

def onFeedServiceStatus(redis, timeout):
    """
        服务状态监听 喂狗
    """
    redis.set(SERVICE_STATUS_KEY, "")
    redis.expire(SERVICE_STATUS_KEY, timeout)
    return {'code': 0}


def onGoldServiceClose():
    """
        关闭竞技场服务
    """
    redis = get_inst()
    redis.delete(PROTOCOL_KEY)
    redis.delete(SERVICE_STATUS_KEY)
    return {'code': 0}


def onJoinGoldRoom(account, playid, message):
    """
        加入金币场
    """
    redis = get_inst()
    rule = '[0,0,[0],1]'
    message = eval(message)
    gameid = message['gameid']
    player_count = redis.hget(GAME_TABLE % gameid, 'party_player_count')
    maxplayers = int(player_count)
    exit_player_data = EXIT_PLAYER % account
    if redis.exists(exit_player_data):
        return {'code': 0}

    wait_join_list = PREFIX_WAIT % (playid, gameid, rule)
    if redis.exists(wait_join_list) and account in redis.lrange(wait_join_list, 0, -1):
        return {'code': 0}

    pipe = redis.pipeline()
    pipe.rpush(wait_join_list, account)
    pipe.set(PREFIX_ACCOUNT2WAIT % account, wait_join_list)
    pipe.execute()

    return {'code': 0}



def onCancelJoinGoldRoom(account):
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


def onCheckJoinGoldRoom(account):
    """
        确认金币场结果
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

    return {'code': -1, 'msg': '未申请加入金币场'}


def onJoinGoldRoomSuccess(server_table, accountlist, playid, rule):
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
    already_in_list = PREFIX_INGAME % (playid, gameid, rule, ip, port)
    pipe = redis.pipeline()
    for account in accountlist:
        pipe.rpush(already_in_list, account)
        pipe.set(PREFIX_ACCOUNT2INGAME % account, already_in_list)
        pipe.delete(PREFIX_MATCH_FINISH % account)
    pipe.execute()
    return {'code' : 0}


def onGoldRoomLeaveSuccess(server_table, accountlist):
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


def clear_on_gold_room_players():
    """
        清除数据
    """
    redis = get_inst()
    print 'clear_on_gold_room_players'
    key_list = [PREFIX_ACCOUNT2WAIT % '*', 'GameInGoldRoomPlayers:*:list', PREFIX_ACCOUNT2INGAME % '*',
                PREFIX_MATCH_FINISH % '*', 'WaitJoinGoldRoomPlayers:*:list', PROTOCOL_KEY,
                SERVICE_STATUS_KEY, ]
    pipe = redis.pipeline()
    for item in key_list:
        keys = redis.keys(item)
        for key in keys:
            print key
            pipe.delete(key)
    return pipe.execute()


class GoldWorker():
    def __init__(self, thread_num=5):
        self.mutex = Lock()
        self.thread_num = thread_num
        self.serviceProtocolTable = PROTOCOL_KEY
        self.serviceStatus = SERVICE_STATUS_KEY
        self.serviceProtoCalls = []
        self.registerServiceProtocols()

    def run(self):
        log_debug('GoldWorker ***************************')
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
            'close': onGoldServiceClose,
            'joinGoldRoom': onJoinGoldRoom,
            'cancelJoinGoldRoom': onCancelJoinGoldRoom,
            'checkJoinGoldRoom': onCheckJoinGoldRoom,
            'joinGoldRoomSuccess': onJoinGoldRoomSuccess,
            'GoldRoomLeaveSuccess': onGoldRoomLeaveSuccess,
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