# -*- coding:utf-8 -*-

# Copyright (c) 2017 yu.liu <showmove@qq.com>
# All rights reserved

""" 俱乐部服务


"""
import traceback 
import re
from bottle import request, Bottle, abort, redirect, response, template,static_file
from web_db_define import *
from club_db_define import *
from hall_func import *
from common.log import *
from config.config import *
from model.gameModel import get_game_info
from model.userModel import get_user_open_auth
from model.hallModel import *
from model.protoclModel import sendProtocol2GameService
#wechatApp
from hall import hall_app
import json
from common import web_util
from websocket_client import SendManager, Packer
from websocket import create_connection
import random
import clubOpenRoom_pb2
import time


def remote_disbaled(redis):
    
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR')
    redis.hincrby("access:number:ip:hset", client_ip, 1)
    print(u"远程地址:%s 头部：%s" % (client_ip, request.headers))
    if not client_ip or client_ip == "183.60.133.160":
        return
    number = redis.hget("access:number:ip:hset", client_ip)
    number = int(number) if number else 0
    if number >= 15:
        redis.sadd("remote:disbled:ip:set", client_ip)
        # sendRemoveIpaddr(client_ip)
    return 

def getRoomId(redis):
    " 获取一个新的ROOMID"

    # test
    roomId = redis.spop('gameTestNnm:set')
    if not roomId:
        roomId = redis.spop("gameNnm:set")
    return roomId

def otherCreateRoom(gameid, auto_id, rule, ruleText, ag, club_number, account, redis):
    """ 其他的方式创建房间

    """
    log_debug(u"account=%s" % account)
    if not account:
        return False, u"创建失败，account信息获取失败"
    room_id = getRoomId(redis)
    if not room_id:
        return False, u"创建失败, 没有找到房间ID."
    room_id = "%06d" % int(room_id)
    serverList = redis.lrange("services:game:%s" % gameid, 0, -1)
    gameConnection = []
    log_debug(u"循环服务器地址列表:%s" % serverList)
    for item in serverList:
        port = item.split(":")[-1]
        ip = item.split(":")[-2]
        gameConnection.append({"ip": ip, "port": port})
    if not gameConnection:
        return False, u'失败！没有找到服务器地址'

    server = random.choice(gameConnection)
    ip_addr = server["ip"]
    port = server["port"]
    print(ip_addr, port)
    mahjongConnect = create_connection("ws://%s:%s" % (ip_addr, port))
    senderMgr = SendManager()
    senderMgr.registerCommands(
        (
            Packer(clubOpenRoom_pb2.S_S_CLUBOPENROOM, clubOpenRoom_pb2.S_S_ClubOpenRoom),
        )
    )
    resp = clubOpenRoom_pb2.S_S_ClubOpenRoom()
    resp.timestamp = str(int(time.time()))
    resp.id = int(auto_id)
    resp.rule = rule
    resp.ag = ag
    resp.account = account
    resp.ruleText = ruleText
    resp.clubNumber = club_number
    resp.roomId = room_id
    mahjongConnect.send_binary(senderMgr.pack(resp))
    mahjongConnect.close()
    log_debug(room_id)
    return True, room_id

class ClubOperation(object):
    
    @staticmethod
    def create_club(redis, account, club_number, club_name, ag, club_content=""):
        """ 添加俱乐部

        """
        print(club_number)
        redis.sadd(CLUB_LIST, club_number)
        redis.hmset(
            CLUB_ATTR % club_number, {
                "club_name": club_name,
                "club_user": account,
                "club_max_players": 9999,
                "club_is_vip": 0,
                "club_content": club_content,
                "club_use_create_room": 1, # 是否允许成员自己创建房间！默认允许,
                "club_manager": 'set()',
                "club_agent": ag # 第一次设置的时候加入的公会
            }
        )
        redis.sadd(CLUB_ACCOUNT_LIST%account, club_number)


    @staticmethod
    def add_club(redis, account, club_number):
        """ 添加玩家到俱乐部

        """
        # 检查这个俱乐部是否存在
        if redis.exists(CLUB_ATTR % club_number):
            try:
                redis.sadd(CLUB_PLAYER_TO_CLUB_LIST % account, club_number)
                redis.sadd(CLUB_PLAYER_LIST % club_number, account)
                return True
            except Exception as err:
                return False
        return False
        
    @staticmethod
    def sign_out_club(redis, account, club_number):
        """ 将玩家从俱乐部移除

        """
        log_info("%s-%s" % (account, club_number))
        try:
            redis.srem(CLUB_PLAYER_LIST % club_number, account)
            redis.srem(CLUB_PLAYER_TO_CLUB_LIST % account, club_number)
            return True
        except Exception as err:
            return False

    @staticmethod
    def get_cur_club_list(redis, account):
        """ 获取自己创建的俱乐部列表

        """
        club_list = []

        _rlis = list(redis.smembers(CLUB_ACCOUNT_LIST % account))
        history_club = None
        if redis.exists(CLUB_PLAYER_INTO % account):
            history_club = redis.get(CLUB_PLAYER_INTO % account)
            if history_club in _rlis:
                _rlis.remove(history_club)
                _rlis.insert(0, history_club)

        for item in _rlis:
            # 获取俱乐部名称
            club_name = redis.hget(CLUB_ATTR % item, "club_user")
            # 获取创始人的头像
            userTable = getUserByAccount(redis, club_name)
            #avatar_url = redis.hget(userTable, "headImgUrl")
            avatar_url, nickName = redis.hmget(userTable, "headImgUrl", "nickname")
            # 获取俱乐部当前人数
            club_person_number = len(redis.smembers(CLUB_PLAYER_LIST % item)) + 1
            club_list.append(
                {
                    "club_name": nickName,
                    "club_person_number": club_person_number,
                    "club_number": item,
                    "creator": 1,
                    "isManager": 0,
                    "avatar_url": avatar_url
                }
            )


        return club_list

    @staticmethod
    def get_all_club_list(redis, session, account):
        """ 获取所有人的俱乐部列表

        """
        club_list = []
        _rlis = list(redis.smembers(CLUB_LIST))
        for item in _rlis:
            # 获取俱乐部名称
            club_name = redis.hget(CLUB_ATTR % item, "club_name")
            players = redis.smembers(CLUB_PLAYER_LIST % item)
            club_join = 0
            if account in players:
                club_join = 1
            isManager = 0
            creator = 0
            apply = 0
            if redis.hmget(CLUB_ATTR % item, "club_name") == account:
                creator = 1
            if account in eval(redis.hget(CLUB_ATTR % item, "club_manager")):
                isManager = 1
            #if account in redis.smembers("CLUB_AUDI_LIST"):
            apply_status = -2
            if creator or isManager:
                apply = 2
            else:
                apply_list = redis.smembers(CLUB_AUDI_LIST % item)
                for iter in apply_list:
                    try:
                        apply_account, nickname, avatar_url, status = iter.split("|---|")
                        if apply_account == account:
                            apply_status = status
                    except Exception as err:
                        print(err)
                        redis.srem(iter)
            # 获取俱乐部当前人数
            club_person_number = len(players) + 1
            club_list.append(
                {
                    "club_name": club_name,
                    "club_person_number": club_person_number,
                    "club_number": item,
                    "club_join": club_join,
                    "creator": creator,
                    "isManager": isManager,
                    "apply_status": int(apply_status)
                }
            )
        return club_list

    @staticmethod
    def get_player_club_list(redis, account):
        """ 获取自己加入的俱乐部列表

        """
        club_list = []
        _rlis = list(redis.smembers(CLUB_PLAYER_TO_CLUB_LIST % account))
        history_club = None
        if redis.exists(CLUB_PLAYER_INTO % account):
            history_club = redis.get(CLUB_PLAYER_INTO % account)
            if history_club in _rlis:
                _rlis.remove(history_club)
                _rlis.insert(0, history_club)

        for item in _rlis:
            # 获取俱乐部名称
            club_user, club_name, club_guest = redis.hmget(CLUB_ATTR % item, "club_user", "club_name", "guest")

            # 获取创始人的头像
            userTable = getUserByAccount(redis, club_user)
            avatar_url, nickName = redis.hmget(userTable, "headImgUrl", "nickname")

            club_manager = redis.hget(CLUB_ATTR % item, "club_manager")
            if not club_manager:
                club_manager = set()
            else:
                club_manager = eval(club_manager)

            isManager = 0
            if account in club_manager:
                isManager = 1
            # 获取俱乐部当前人数
            club_person_number = len(redis.smembers(CLUB_PLAYER_LIST % item)) + 1
            club_list.append(
                {
                    "club_user": nickName,
                    "club_name": club_name,
                    "club_person_number": club_person_number,
                    "club_number": item,
                    "isManager": isManager,
                    "creator": 0,
                    "avatar_url": avatar_url,
                }
            )
        return club_list

    @staticmethod
    def get_club_player_list(redis, club_number):
        """ 获取俱乐部的玩家列表

        """
        players = []
        accounts = redis.smembers(CLUB_PLAYER_LIST % club_number)
        members = redis.smembers(ONLINE_ACCOUNTS_TABLE)

        # 添加管理者
        managerAccount = redis.hget(CLUB_ATTR % club_number, "club_user")
        accounts.add(managerAccount)
        for item in accounts:
            userTable = redis.get(FORMAT_ACCOUNT2USER_TABLE % item)
            player = {}
            nickname, headImgUrl, account, last_logout_date = redis.hmget(userTable, 'nickname', 'headImgUrl', 'account', "last_logout_date")
            player["account"] = account
            player["nickname"] = nickname
            player["avatar_url"] = headImgUrl
            player["online"] = 0
            player["user_id"] = int(userTable.split(":")[-1])

            # 查找备注信息
            notes = redis.hget(CLUB_PLAYER_NOTES % club_number, account)
            if not notes:
                notes = ''
            player["notes"] = notes

            if account in members:
                player["online"] = 1
            if not last_logout_date.strip():
                player["time"] = u"未登录过"
            else:
                _time = int(time.mktime(time.strptime(last_logout_date, '%Y-%m-%d %H:%M:%S')))
                curtime = int(time.time())
                seco = (curtime - _time)
                mon  = seco/60
                hour = mon/60
                day  = hour/24
                if day >= 1:
                    player["time"] = u"%s天前"% day
                elif hour >= 1:
                    player["time"] = u"%s小时前"% hour
                elif mon >= 1:
                    player["time"] = u"%s分钟前" % mon
                else:
                    player["time"] = u"%s秒前" % seco

            isManager = 0
            data = eval(redis.hget(CLUB_ATTR % club_number, 'club_manager'))
            if account in data:
                isManager = 1
            player.update(
                {
                    "isManager": isManager
                }
            )
            player["creator"] = 0
            if item == managerAccount:
                player["isManager"] = 1
                player["creator"] = 1
            player["guest"] = 0
            players.append(player)

        players = sorted(players, key=lambda x: (-x["creator"], -x["isManager"]))
        return players

@hall_app.post('/club/create')
@web_util.allow_cross_request
def create_club(redis, session):
    """ 创建俱乐部

    request http://server/club/create
    data  :sid=sid, club_name=俱乐部名称, club_content=俱乐部说明
    returns {"club_number": int(), code: int() }

    :param redis:
    :param session:
    :return:
    """
    try:
        log_info(dict(request.forms).items())
        # 获取参数
        sid = request.forms.get('sid','').strip()
        club_name = request.forms.get('club_name','').strip()
        club_content = request.forms.get('club_name','').strip()
        if not club_name:
            return {"code": 1, "msg": "俱乐部名称不能为空"}

        SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
        if verfiySid and sid != verfiySid:
            # session['member_account'],session['member_id'] = '',''
            return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
        if not redis.exists(SessionTable):
            return {'code': -3, 'msg': 'sid 超时'}

        ag = redis.hgetall(redis.get(FORMAT_ACCOUNT2USER_TABLE % account))
        print(ag)
        ag = ag["parentAg"]
        if not ag:
            return {"code": 1, 'msg': "你没有任何公会，不能创建俱乐部"}

        log_info("%s, %s, %s, %s" % (SessionTable, account, uid, verfiySid))
        if verfiySid and sid != verfiySid:
            # session['member_account'],session['member_id'] = '',''
            return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
        # 做一次硬性判定
        number = redis.hget(CLUB_CREATE_ATTR, "max_club_num") or 10
        if len(redis.smembers(CLUB_ACCOUNT_LIST % account)) >= 10:
            return {"code": 1, "msg": "你已经超出了创建俱乐部的上限"}

        log_info("Create Club...")
        # 检查俱乐部列表取出最大的值加1
        club_list = [int(i) for i in redis.smembers(CLUB_LIST)]

        log_info("Club list: %s" % club_list)
        if not club_list:
            next_id = 2000
        else:
            next_id = max(club_list) + 1

        next_id = str(next_id)
        if '4' in next_id:
            next_id = next_id.replace('4', str(4+1))
        next_id = int(next_id)

        # 添加数据
        ClubOperation.create_club(redis, account, next_id, club_name, ag, club_content)

        return {"code": 0, "msg": "恭喜，创建俱乐部成功，您的俱乐部ID为%s" % next_id, "club_number": next_id}
    except Exception as err:
        traceback.print_exc()
        return {"code": 1, "msg": "创建失败"}

@hall_app.post('/club/disbandment')
@web_util.allow_cross_request
def delete_club(redis, session):
    """ 解散俱乐部

    request http://server/club/disbandment
    args  :sid=sid, club_number=俱乐部ID
    header: Session
    returns {"msg": string, "code": int() }

    :param redis:
    :param session:
    :return:
    """
    try:
        # 获取参数
        sid = request.forms.get('sid','').strip()
        club_number = request.forms.get('club_number','').strip()
        SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
        if verfiySid and sid != verfiySid:
            # session['member_account'],session['member_id'] = '',''
            return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
        if not redis.exists(SessionTable):
            return {'code': -3, 'msg': 'sid 超时'}
        # 检查俱乐部是否存在
        if redis.exists(CLUB_ATTR % club_number):
            # 解散俱乐部逻辑
            club_user = redis.hget(CLUB_ATTR % club_number, 'club_user')
            if club_user != account:
                return {"code": 1, 'msg': '你无法删除这个俱乐部'}

            pipe = redis.pipeline()


            # 删除俱乐部的属性
            pipe.delete(CLUB_ATTR % club_number)
            # 从总举了表中移除
            pipe.srem(CLUB_LIST, club_number)
            # 从创始人中的俱乐部列表中移除
            pipe.srem(CLUB_ACCOUNT_LIST % account, club_number)
           
            # 检查俱乐部的玩家，并将这些玩家从这个俱乐部中踢出
            for player in redis.smembers(CLUB_PLAYER_LIST % club_number):
                pipe.srem(CLUB_PLAYER_TO_CLUB_LIST % player, club_number)
            # 删除俱乐部存储的玩家信息

            pipe.delete(CLUB_PLAYER_LIST % club_number)

            # 删除自动开房信息
            userTable = getUserByAccount(redis, club_user)
            parentAg = redis.hget(userTable, "parentAg")
            agClubNumber = "%s-%s" % (club_number, parentAg)
            for i in range(1, 6):
                pipe.delete(CLUB_EXTENDS_LIST_ATTRIBUTE % agClubNumber)
                pipe.delete(CLUB_EXTENDS_ATTRIBUTE % (agClubNumber, i))

            pipe.execute()
            return {'code': 0, "msg": '删除成功'}
        else:
            return {'code': 1, "msg": '不存在这个俱乐部号'}


    except Exception as err:
        traceback.print_exc()
        return {"code": 1, "msg": "删除失败"}


@hall_app.post('/club/edit')
@web_util.allow_cross_request
def edit_club(redis, session):
    """ 修改俱乐部信息

    :param redis:
    :param session:
    :return:
    """
    sid = request.forms.get('sid', '').strip()
    club_number = request.forms.get("club_number", '').strip()
    club_content = request.forms.get("club_content", '').strip()
    if not club_number:
        return {"code": 1, "msg": "没有俱乐部ID"}
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    if verfiySid and sid != verfiySid:
        # session['member_account'],session['member_id'] = '',''
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}

    # 检查俱乐部是否存在
    if redis.exists(CLUB_ATTR % club_number):
        # 检查是否有操作权限
        data = eval(redis.hget(CLUB_ATTR % club_number, "club_manager"))
        club_user = redis.hget(CLUB_ATTR % club_number, 'club_user')
        if club_user != account and account not in data:
            return {"code": 1, 'msg': '你没有操作这个俱乐部的权限'}

        redis.hset(CLUB_ATTR % club_number, "club_content", club_content)
        return {"code": 0, 'msg': '成功'}
    return {"code": 1, 'msg': '失败'}

@hall_app.get('/club/get_one')
@web_util.allow_cross_request
def get_one(redis, session):
    """ 获取单个俱乐部的信息

    :param redis:
    :param session:
    :return:
    """
    sid = request.params.get('sid', '').strip()
    club_number = request.params.get("club_number", '').strip()
    club_content = request.params.get("club_content", '').strip()
    if not club_number:
        return {"code": 1, "msg": "没有俱乐部ID"}
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if not redis.exists(CLUB_ATTR % club_number):
        return {"code": 1, 'msg': '俱乐部不存在'}
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}

    club_data = redis.hgetall(CLUB_ATTR % club_number)

    club_data["club_manager"] = list(eval(club_data["club_manager"]))
    person_number = len(redis.smembers(CLUB_PLAYER_LIST % club_number))
    club_data["people_number"] = person_number
    print(club_data)
    return {'code': 0, 'msg': '成功', 'data': club_data}


@hall_app.get('/club/user/list')
@web_util.allow_cross_request
@retry_insert_number()
def club_user_list(redis, session):
    """ 获取俱乐部用户列表

    :param redis:
    :param session:
    :return:
    """
    sid = request.params.get('sid', '').strip()
    club_number = request.params.get("club_number", '').strip()
    if not club_number:
        return {"code": 1, "msg": "没有俱乐部ID"}

    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if not redis.exists(CLUB_ATTR % club_number):
        return {"code": 1, 'msg': '俱乐部不存在'}
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}

    return {"code": 0, "list": ClubOperation.get_club_player_list(redis, club_number)}

@hall_app.post('/club/user/set_notes')
@web_util.allow_cross_request
@retry_insert_number()
def set_notes(redis, session):
    """ 设置玩家的备注名称

    :param redis:
    :param session:
    :return:
    """
    sid = request.forms.get('sid', '').strip()
    targetAccount = request.forms.get('account', '').strip()
    notes = request.forms.get("notes", '').strip()
    club_number = request.forms.get('club_number','').strip()

    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}
    if verfiySid and sid != verfiySid:
        # session['member_account'],session['member_id'] = '',''
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
    if not redis.exists(CLUB_ATTR%club_number):
        return {"code": 1, "msg": '俱乐部不存在'}
    data = eval(redis.hget(CLUB_ATTR % club_number, "club_manager"))
    club_user = redis.hget(CLUB_ATTR % club_number, 'club_user')
    if club_user != account and account not in data:
        return {"code": 1, 'msg': '你没有操作这个俱乐部的权限'}

    if len(notes) > 30:
        return {"code": 1, 'msg': "你设置的备注太长了"}

    # 开始设置
    redis.hset(CLUB_PLAYER_NOTES % club_number, targetAccount, notes)
    return {"code": 0, "msg": "成功"}

@hall_app.get('/club/list')
@web_util.allow_cross_request
@retry_insert_number()
def get_club_list(redis, session):
    """ 获取俱乐部列表
    request http://server/club/list
    args: sid=用户的SID
    header: Session
    returns {"list": [], "code": int() }


    :param redis:
    :param session:
    :return:
    """
    log_info(request.params)
    # 获取参数
    sid = request.params.get('sid','').strip()
    # club_number = request.forms.get('club_number','').strip()
    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not redis.exists(SessionTable):
        return {'code':-3, 'msg':'sid 超时'}

    # return {"code": 0, "list": ClubOperation.get_all_club_list(redis, session, account) }
    return {"code": 0, "list": []}

@hall_app.get('/club/owner_list')
@web_util.allow_cross_request
@retry_insert_number()
def get_owner_list(redis, session):
    """ 获取自己的俱乐部列表
    request http://server/club/list
    args  : sid=sid
    header: Session
    returns {"list": [], "code": int() }


    :param redis:
    :param session:
    :return:
    """
    log_info(request.params)
    # 获取参数
    sid = request.params.get('sid','').strip()
    # club_number = request.forms.get('club_number','').strip()
    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not redis.exists(SessionTable):
        return {'code':-3, 'msg':'sid 超时'}
    return {"code": 0, "list": ClubOperation.get_cur_club_list(redis, account)}

@hall_app.get('/club/club_of_list')
@web_util.allow_cross_request
@retry_insert_number()
def club_of_list(redis, session):
    """ 获取自己所有相关的俱乐部列表
    request http://server/club/list
    args  : sid=sid
    header: Session
    returns {"list": [], "code": int() }


    :param redis:
    :param session:
    :return:
    """
    log_info(request.params)
    # 获取参数
    sid = request.params.get('sid','').strip()
    # club_number = request.forms.get('club_number','').strip()
    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}
    if verfiySid and sid != verfiySid:
        # session['member_account'],session['member_id'] = '',''
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
    cur_list = ClubOperation.get_cur_club_list(redis, account)
    cur_list.extend(
        ClubOperation.get_player_club_list(redis, account)
    )
    club_number = redis.get(CLUB_PLAYER_INTO % account)
    if not cur_list:
        return {"code": 0, "list": cur_list}
    if club_number:
        switch_number = 0
        for index, value in enumerate(cur_list):
            if value["club_number"] == club_number:
                switch_number = index
        cur_list[switch_number], cur_list[0] = cur_list[0], cur_list[switch_number]

    return {"code": 0, "list": cur_list}

@hall_app.get('/club/join_club_list')
@web_util.allow_cross_request
@retry_insert_number()
def join_club_list(redis, session):
    """ 获取自己加入的俱乐部列表
    request http://server/club/join_club_list
    args  : sid=sid
    header: Session
    returns {"list": [], "code": int() }


    :param redis:
    :param session:
    :return:
    """
    sid = request.params.get('sid','').strip()
    # club_number = request.forms.get('club_number','').strip()
    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not redis.exists(SessionTable):
        return {'code':-3, 'msg':'sid 超时'}

    return {"code": 0, "list": ClubOperation.get_player_club_list(redis, account)}

@hall_app.post('/club/join_club')
@web_util.allow_cross_request
@retry_insert_number()
def join_club(redis, session):
    """ 加入俱乐部
    request http://server/club/join_club
    args  : sid=sid, club_number = 俱乐部ID
    header: Session
    returns {"msg": 成功, "code": int() }


    :param redis:
    :param session:
    :return:
    """
    log_info(request.forms.items())
    sid = request.forms.get('sid','').strip()
    club_number = request.forms.get('club_number','').strip()
    if not club_number:
        return {"code": 1, 'msg': '不能没有俱乐部ID'}
    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not redis.exists(SessionTable):
        return {'code':-3, 'msg':'sid 超时'}
    if redis.hget(CLUB_ATTR % club_number, 'club_user') == account:
        return {"code": 1, 'msg': '创建人不需要加入自己的俱乐部'}

    result = ClubOperation.add_club(redis, account, club_number)
    if result:
        return {"code": 0, "msg": "成功"}
    return {"code": 1, "msg": "失败"}

@hall_app.post('/club/sign_out_club')
@web_util.allow_cross_request
@retry_insert_number()
def sign_out_club(redis, session):
    """ 退出俱乐部
    request http://server/club/sign_out_club
    args  : sid=sid, club_number = 俱乐部ID
    header: Session
    returns {"msg": 成功, "code": int() }


    :param redis:
    :param session:
    :return:
    """
    sid = request.forms.get('sid','').strip()
    club_number = request.forms.get('club_number','').strip()
    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not redis.exists(SessionTable):
        return {'code':-3, 'msg':'sid 超时'}
    result = ClubOperation.sign_out_club(redis, account, club_number)
    if result:
        return {"code": 0, "msg": "成功"}
    return {"code": 1, "msg": "失败"}

@hall_app.post('/club/force_sign_out_club')
@web_util.allow_cross_request
@retry_insert_number()
def force_sign_out_club(redis, session):
    """ 将玩家踢出俱乐部
    request http://server/club/force_sign_out_club
    args  : builder_sid=创建者的SID, member_account = 被踢出去的人的ID, club_number=俱乐部ID
    header: Session
    returns {"msg": 成功, "code": int() }

    :param redis:
    :param session:
    :return:
    """
    builder_sid = request.forms.get('builder_sid','').strip()
    builderSessionTable,builderaccount,builderuid,builderverfiySid = getInfoBySid(redis, builder_sid)
    if not builderaccount:
        return {"code": 1, "msg": "用户不生效"}
    member_account = request.forms.get('member_account','').strip()
    club_number = request.forms.get('club_number','').strip()
    # 检查俱乐部是否存在
    if redis.exists(CLUB_ATTR % club_number):
        # 检查是否有操作权限
        data = eval(redis.hget(CLUB_ATTR % club_number, "club_manager"))

        club_user = redis.hget(CLUB_ATTR % club_number, 'club_user')
        if club_user != builderaccount and builderaccount not in data:
            return {"code": 1, 'msg': '你没有操作这个俱乐部的权限'}
        if member_account in data:
            return {"code": 1, "msg": "该用户是管理员！无法踢出。"}
        # SessionTable,account,uid,verfiySid = getInfoBySid(redis, member_sid)
        result = ClubOperation.sign_out_club(redis, member_account, club_number)
        if result:
            return {"code": 0, "msg": "成功"}

    return {"code": 1, "msg": "失败"}

@hall_app.post("/club/apply")
@web_util.allow_cross_request
@retry_insert_number()
def apply_club(redis, session):
    """ 申请加入俱乐部
    request http://server/club/apply
    args  : sid=申请者SID, club_number=俱乐部ID
    header: Session
    returns {"msg": 成功, "code": int() }

    :param redis:
    :param session:
    :return:
    """
    
    sid = request.forms.get('sid','').strip()
    club_number = request.forms.get('club_number','').strip()
    if not club_number:
        return {"code": 1, 'msg': '不能没有俱乐部ID'}
    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)

    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if redis.hget(CLUB_ATTR % club_number, 'club_user') == account:
        return {"code": 1, 'msg': '创建人不需要加入自己的俱乐部'}
    # 检查俱乐部是否存在
    if redis.exists(CLUB_ATTR % club_number):

        nickname, headImgUrl, _account = redis.hmget(redis.get(FORMAT_ACCOUNT2USER_TABLE % account), 'nickname', 'headImgUrl', 'account')
        if not _account or _account.strip() == 'None':
            log_info("[apply_club][error] userPath=%s" % (FORMAT_ACCOUNT2USER_TABLE % account))
            return {"code": 1, "msg": "获取信息失败, 请重试。"}
        audiList = redis.smembers(CLUB_AUDI_LIST%club_number)
        audiAccountData = "%s|---|%s|---|%s|---|%s" % (_account, nickname, headImgUrl, 1)
        clubUserList = redis.smembers(CLUB_PLAYER_LIST % club_number)
        if audiAccountData in audiList and account in clubUserList:
            return {"code": 1, "msg": "你已经加入了该俱乐部, 请勿重新申请。"}

        # 增加用户到这个俱乐部申请表中
        auditEntry = "%s|---|%s|---|%s|---|%s" % (_account, nickname, headImgUrl, 0)
        if auditEntry in audiList:
            return {"code": 0, 'msg': '你的申请正在审核中。'}

        redis.sadd(CLUB_AUDI_LIST%club_number, auditEntry)
        redis.incrby(CLUB_AUDI_INTO_NUMBER % club_number, 1)
        return {"code": 0, 'msg': '成功'}
    return {"code": 1, "msg": "该俱乐部ID不存在，请重新输入"}

@hall_app.get("/club/apply/list")
@web_util.allow_cross_request
@retry_insert_number()
def apply_club_list(redis, session):
    """ 俱乐部申请加入列表
    request http://server/club/apply/list
    args  : sid=当前用户SID, club_number=俱乐部ID
    header: Session
    returns {"msg": 成功, "code": int() }

    :param redis:
    :param session:
    :return:
    """
    sid = request.params.get('sid','').strip()
    club_number = request.params.get('club_number','').strip()
    if not club_number:
        return {"code": 1, 'msg': '不能没有俱乐部ID'}
    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not redis.exists(SessionTable):
        return {'code':-3, 'msg':'sid 超时'}

    if redis.exists(CLUB_ATTR % club_number):
        data = eval(redis.hget(CLUB_ATTR % club_number, "club_manager"))

        if redis.hget(CLUB_ATTR % club_number, "club_user") != account and account not in data:
            return {"code": 1, 'msg': "你不能操作这个俱乐部"}
        data = []
        result = redis.smembers(CLUB_AUDI_LIST % club_number)
        for item in result:
            print("审核内容: %s" % item)
            try:
                account, nickname, avatar_url, status = item.split("|---|")
            except Exception as err:
                log_info(err)
                print("item:%s, err:%s" % (item, err))
                continue
            if not account or account.strip() == 'None':
                log_info("[error][club_audit]%s,  %s" % (CLUB_AUDI_LIST % club_number, item))
                redis.srem(CLUB_AUDI_LIST % club_number, item)
                continue

            user_path = redis.get(FORMAT_ACCOUNT2USER_TABLE % account)
            user_id = user_path.split(":")[-1]
            reg_date = redis.hget(user_path, "reg_date")
            status_keys = {0: "申请中", 1: '成功', -1: '拒绝'}
            orders = {
                0: 2,
                1: 1,
                -1: 0
            }

            data.append(
                {
                    "account": account,
                    "nickname": nickname,
                    "avatar_url": avatar_url,
                    "status" : {"code": status, "name": status_keys[int(status)] },
                    "club_number": club_number,
                    "user_id": user_id,
                    "reg_date": reg_date,
                    "order": orders[int(status)]
                }
            )
        data = sorted(data, key=lambda x: -x["order"])
        redis.set(CLUB_AUDI_INTO_NUMBER % club_number, 0)
        return {"code": 0, 'msg': '成功', "list": data}
    return {"code": 1, "msg": "失败"}

@hall_app.post("/club/apply/audit")
@web_util.allow_cross_request
@retry_insert_number()
def apply_club_audit(redis, session):
    """ 审核
    request http://server/club/apply/audit
    args  : sid=当前用户SID, apply_user_account=申请的用户 club_number=俱乐部ID status= 1=允许 -1=拒绝
    header: Session
    returns {"msg": 成功, "code": int() }

    """
    sid = request.forms.get('sid','').strip()
    club_number = request.forms.get('club_number','').strip()
    apply_user_account = request.forms.get("apply_user_account", '').strip()
    status = request.forms.get("status", '').strip()
    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)

    if not club_number:
        return {"code": 1, 'msg': '不能没有俱乐部ID'}
    if not apply_user_account:
        return {"code": 1, 'msg': '不能没有用户信息'}
    if not status or int(status) == 0:
        return {"code": 1, 'msg': '请填写你的申请状态'}
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}

    if redis.exists(CLUB_ATTR % club_number):
        data = eval(redis.hget(CLUB_ATTR % club_number, "club_manager"))
        # 增加用户到这个俱乐部申请表中
        if redis.hget(CLUB_ATTR % club_number, "club_user") != account and account not in data:
            return {"code": 1, 'msg': "你不能操作这个俱乐部"}



    if int(status) == 1:
        apply_list = redis.smembers(CLUB_AUDI_LIST % club_number)
        for item in apply_list:
            account, nickname, avatar_url, state = item.split("|---|")
            if account == apply_user_account and int(state) == 0:
                redis.srem(CLUB_AUDI_LIST % club_number, item)
                redis.sadd(CLUB_AUDI_LIST % club_number, "%s|---|%s|---|%s|---|%s" % (account, nickname, avatar_url, status))
                if ClubOperation.add_club(redis, account, club_number):
                    return {"code": 0, 'msg': '成功'}
    else:
        apply_list = redis.smembers(CLUB_AUDI_LIST % club_number)
        for item in apply_list:
            account, nickname, avatar_url, state = item.split("|---|")
            if account == apply_user_account and int(state) == 0:
                redis.srem(CLUB_AUDI_LIST % club_number, item)
                redis.sadd(CLUB_AUDI_LIST % club_number, "%s|---|%s|---|%s|---|%s" % (account, nickname, avatar_url, status))
                return {"code": 0, 'msg': '成功'}

    return {"code": 1, 'msg': '失败'}


@hall_app.post("/club/add_manager")
@web_util.allow_cross_request
@retry_insert_number()
def add_manager(redis, session):
    """ 添加管理者

    :param redis:
    :param session:
    :return:
    """
    sid = request.forms.get('sid', '').strip()
    club_number = request.forms.get('club_number', '').strip()
    manager_account = request.forms.get("account", '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not redis.exists(SessionTable):
        return {'code':-3, 'msg':'sid 超时'}

    if redis.exists(CLUB_ATTR % club_number):
        # data = eval(redis.hget(CLUB_ATTR % club_number, "club_manager"))
        if redis.hget(CLUB_ATTR % club_number, "club_user") != account:
            return {"code": 1, 'msg': "你不能操作这个俱乐部"}
        data = eval(redis.hget(CLUB_ATTR % club_number, "club_manager"))
        if len(data) >= 3:
            return {"code":1, "msg": "管理员已达上限数量，无法增加更多的管理员"}
        data.add(manager_account)
        redis.hset(CLUB_ATTR % club_number, "club_manager", data)
        return {"code": 0, 'msg': '成功'}
    else:
        return {"code": 1, "msg": "失败"}

@hall_app.post("/club/relieve_manager")
@web_util.allow_cross_request
@retry_insert_number()
def relieve_manager(redis, session):
    """ 解除管理者
    :param redis:
    :param session:
    :return:
    """
    sid = request.forms.get('sid', '').strip()
    club_number = request.forms.get('club_number', '').strip()
    manager_account = request.forms.get("account", '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not redis.exists(SessionTable):
        return {'code':-3, 'msg':'sid 超时'}

    if redis.exists(CLUB_ATTR % club_number):
        if redis.hget(CLUB_ATTR % club_number, "club_user") != account:
            return {"code": 1, 'msg': "你不能操作这个俱乐部"}
        data = eval(redis.hget(CLUB_ATTR % club_number, "club_manager"))
        data.remove(manager_account)
        if not data:
            data = "set()"
        redis.hset(CLUB_ATTR % club_number, "club_manager", data)
        return {"code": 0, 'msg': '成功'}
    else:
        return {"code": 1, "msg": "失败"}

@hall_app.post('/club/createRoom')
@web_util.allow_cross_request
@retry_insert_number()
def do_ClubCreateRoom(redis,session):
    """
    创建房间接口
    """
    # tt = request.forms.get('tt', '').strip()
    # if tt not in ACCEPT_TT:
        # print "try getServer: get faild, code[1]."
        # return {'code' : -1}
    gameId = request.forms.get('gameid','').strip()
    gameId = int(gameId)
    rule = request.forms.get('rule','').strip()
    sid = request.forms.get('sid','').strip()
    # hidden = request.forms.get('hidden','').strip()
    hidden = 1
    club_number = request.forms.get("club_number", '').strip()
    # 检查当前用户是否是这个俱乐部的主人
    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    if not redis.exists(CLUB_ATTR % club_number):
        return {'code':1, 'msg':'俱乐部不存在'}
    if redis.hget(CLUB_ATTR % club_number, "club_user") != account:
        # 检查当前用户是否存在俱乐部
        if club_number not in redis.smembers(CLUB_PLAYER_TO_CLUB_LIST % club_number):
            return {'code':1, 'msg':'你没有加入这个俱乐部！不能创建房间'}
        # 这个俱乐部是否允许俱乐部成员创建房间
        if int(redis.hget(CLUB_ATTR % club_number, "club_use_create_room")) != 1:
            return {'code':1, 'msg':'你不能创建房间！请和俱乐部创始人联系'}

    # 获取俱乐部主人的ACCOUNT
    club_admin_user = redis.hget(CLUB_ATTR % club_number, "club_user")
    
    print 'do_CreateRoom'
    try:
        print '[on createRoom]sid[%s] account[%s] gameId[%s] rule[%s] hidden[%s]'%(sid, account, gameId, rule, hidden)
    except Exception as e:
        print 'print error File', e

    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not redis.exists(SessionTable):
        return {'code':-3, 'msg':'sid 超时'}

    userTable = getUserByAccount(redis, club_admin_user)
    if not redis.exists(userTable):
        return {'code':-5,'msg':'该用户不存在'}
    ag, maxScore,user_open_auth = redis.hmget(userTable, ('parentAg', 'maxScore','open_auth'))
    adminTable = AGENT_TABLE%(ag)
    agValid,agent_open_auth = redis.hmget(adminTable,('valid','open_auth'))
    # 获取是否有权限开房
    open_room = get_user_open_auth(redis,user_open_auth,agent_open_auth)
    if agValid != '1':
       print  '[CraeteRoom][info] agentId[%s] has freezed. valid[%s] '%(ag,agValid)
       return {'code':-7,'msg':'该公会已被冻结,不能创建或加入该公会的房间'}


    id = userTable.split(':')[1]
    roomCards = redis.get(USER4AGENT_CARD%(ag, id))
    if not maxScore:
        maxScore = 1
    params = eval(rule)

    isOther = params[0]
    try:
        isOther = int(isOther)
    except:
        pass
    del params[0]
    print params

    if params[-1] > maxScore:
        params[-1] = maxScore
    needRoomCards = int(params[-2])

    for index, data in enumerate(redis.lrange(USE_ROOM_CARDS_RULE%(gameId), 0, -1)):
        datas = data.split(':')
        name, cards = datas[0], datas[1]
        try:
            playCount = int(datas[2])
        except:
            playCount = 0
        # if int(cards) == needRoomCards:
            # break
        if int(index) == needRoomCards:
            needRoomCards = int(cards)
            params[-2] = needRoomCards
            break
        playCount = -1
    if playCount < 0:
        return {'code':-1,'msg':'房间规则已修改，请重新加载创房页面'}
    params.insert(-2, playCount)

    rule = str(params)

    if int(roomCards) < needRoomCards:
        return {'code':-6,'msg':'钻石不足'}
    print '[do_CreateRoom][info] roomCards[%s] needRoomCards[%s]'%(roomCards, needRoomCards)


    countPlayerLimit = 30
    gameTable = GAME_TABLE%(gameId)
    maxRoomCount = redis.hget(gameTable,'maxRoomCount')
    if maxRoomCount:
        countPlayerLimit = int(maxRoomCount) * 4

    reservedServers = []
    serverList = redis.lrange(FORMAT_GAME_SERVICE_SET%(gameId), 0, -1)
    for serverTable in serverList:
        playerCount = redis.hincrby(serverTable, 'playerCount', 0)
        roomCount = redis.hincrby(serverTable, 'roomCount', 0)
        if not playerCount:
            playerCount = 0
        if not roomCount:
            roomCount = 0
        playerCount = int(playerCount)
        roomCount = int(roomCount)
        countPlayerLimit = int(countPlayerLimit)
        if countPlayerLimit and (playerCount >= countPlayerLimit or roomCount >= countPlayerLimit/4):
            continue
        _, _, _, currency, ipData, portData = serverTable.split(':')
        reservedServers.append((currency, ipData, portData))

    if reservedServers:
        currency, serverIp, serverPort = reservedServers[0]
        ruleText = getRuleText(rule, gameId, redis)
        params = eval(rule)
        params.append(int(hidden))
        rule = str(params)
        protocolStr = HEAD_SERVICE_PROTOCOL_CREATE_OTHER_ROOM%(account, "%s-%s" % (ag, club_number), rule, ruleText)
        redis.rpush(FORMAT_SERVICE_PROTOCOL_TABLE%(gameId, '%s:%s:%s'%(currency, serverIp, serverPort)), protocolStr)
        return {'code':0, 'msg':'房间开启成功', 'ip':'', 'port':''}
    else:
        return {'code':-1, 'msg':'服务器忙碌或维护中'}



@hall_app.post('/club/getRoomList')
@web_util.allow_cross_request
@retry_insert_number()
def doclub_getRoomList(redis, session):
    """
    获取房间列表
    """
    sid  =  request.forms.get('sid','').strip()
    if not sid:
        remote_disbaled(redis)
        return {"code": 1, "msg": "参数错误没有SID"}

    club_number = request.forms.get("club_number", '').strip()
    print 'do_getRoomList'
    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)


    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not redis.exists(SessionTable):
        remote_disbaled(redis)
        return {'code':-3, 'msg':'sid 超时'}

    if redis.exists(CLUB_ATTR%club_number):
        if account not in redis.smembers(CLUB_PLAYER_LIST%club_number):
            if redis.hget(CLUB_ATTR%club_number, 'club_user') != account:
                return {"code": 1, 'msg': "你不能查看这个俱乐部的房间"}
    try:
        print '[on getRoomList]sid[%s] account[%s]'%(sid, account)
    except Exception as e:
        print 'print error File', e

    print 'account'

    uTbles = getUserByAccount(redis, account)
    ag, maxScore, user_open_auth = redis.hmget(uTbles, ('parentAg', 'maxScore', 'open_auth'))
    id = uTbles.split(':')[1]
    userRoomCards = redis.get(USER4AGENT_CARD % (ag, id))


    club_user = redis.hget(CLUB_ATTR % club_number, "club_user")
    userTable = getUserByAccount(redis, club_user)
    if not redis.exists(userTable):
        return {'code':-5,'msg':'该用户不存在'}

    id = userTable.split(':')[1]
    maxScore,userBaseScore = redis.hmget(userTable,('maxScore','baseScore'))
    print maxScore,userBaseScore
    if not userBaseScore:
        userBaseScore = DEFAULT_BASE_SCORE
    groupId = redis.hget(userTable, 'parentAg')
    print maxScore,userBaseScore
    if not maxScore:
        maxScore = 1
    try:
        roomLists = redis.smembers(AG2SERVER%("%s-%s"% (groupId, club_number)))
    except:
        roomLists = []
    roomDatas = []
    ownerAccount = redis.hget(userTable, 'account')
    otherRooms = MY_OTHER_ROOMS % account
    print(otherRooms)
    #try:
    otherRoomsDict = {i.split(":")[-2]: i for i in redis.lrange(otherRooms, 0, -1)}
    #otherRoomsDict = {}
    # for item in otherRooms:
    #     try:
    #         item.split(":")[-2] = item
    #     except Exception as err:
    #         redis.lrem()
    #         continue
    players = redis.smembers(CLUB_PLAYER_LIST % club_number)
    playersNumber = len(players) + 1
    roomlistNumber = 0
    roomActiveNumber = 0
    onlineNumber = 0
    for roomNum in roomLists:

        print '[getRoomList][info] ROOM2SERVER[%s]'%ROOM2SERVER%(roomNum)
        gameName, dealer, playerCount, maxPlayer, gameid, baseScore, ruleText, gameState, room_club_number, curGameCount, maxGameCount = redis.hmget(
            ROOM2SERVER % (roomNum), (
            'gameName', 'dealer', 'playerCount', 'maxPlayer', 'gameid', 'baseScore', 'ruleText', "gameState",
            "club_number", "curGameCount", "maxGameCount"))

        otherInfo = redis.hget(GAME_TABLE % gameid, "other_info")
        try:
            otherInfo = otherInfo.split(",")[2]
        except Exception as err:
            otherInfo = gameName

        if club_number != room_club_number:
            continue

        if not ruleText:
            continue
        if not baseScore:
            baseScore = 1
        print 'baseScore[%s],userBaseScore[%s]'%(baseScore,userBaseScore)
        try:
            hidden = int(redis.hget(ROOM2SERVER%(roomNum), 'hidden'))
        except:
            hidden = 0

        if isinstance(userBaseScore,str):
            userBaseScore = map(int,eval(userBaseScore))

        print userBaseScore
        if int(baseScore)!=1 and int(baseScore) not in userBaseScore:
            continue


        if not gameState:
            if otherRoomsDict.get(roomNum):
                roomTable = otherRoomsDict.get("roomNum")
                try:
                    gameState = int(redis.hget(roomTable, "gameType"))
                except Exception as err:
                    # redis.lrem(otherRooms, roomTable)
                    gameState = 0
        else:
            try:
                if int(gameState) == 1:
                    roomActiveNumber += 1
            except Exception as err:
                gameState = 1
        gameText = ''
        if gameState == 1:
            curGameCount = curGameCount if curGameCount else 0
            maxGameCount = maxGameCount if maxGameCount else 0
            gameText = "（%s/%s）" % (curGameCount, maxGameCount)
        onlineNumber += len(redis.lrange(ROOM2ACCOUNT_LIST % roomNum, 0, -1))
        roomlistNumber += 1
        gameType = CLUB_GAME_ATTRIBUTE_NUMBER.get(int(gameid), 0) or 0#redis.hget(GAME_TABLE % gameid, "gameType") or 0

        # 查看是否自动开房
        auto_id = redis.hget(ROOM2SERVER % (roomNum), 'auto_id')
        if not auto_id:
            auto_id = -1
        auto_id = int(auto_id)

        result = {'gameName': otherInfo, 'dealer': dealer, 'playerCount': playerCount,
                  'maxPlayer': maxPlayer, 'roomNum': roomNum, 'gameid': gameid,
                  'ruleText': ruleText.replace("\n", '|'), 'baseScore': int(baseScore),
                  'gameType': int(gameType), "gameState": gameState, "numberOfInnings": gameText,
                  "curGameCount": curGameCount if curGameCount else 0,
                  "maxGameCount": maxGameCount if maxGameCount else 0,
                  "auto_id": auto_id}
        result["players_list"] = []
        if redis.exists(ROOM2ACCOUNT_LIST % roomNum):
            accountContent = redis.lrange(ROOM2ACCOUNT_LIST % roomNum, 0, -1)
            for item in accountContent:
                playerContent = redis.hgetall(redis.get(FORMAT_ACCOUNT2USER_TABLE % item))
                content = {}
                content["nickname"] = playerContent["nickname"]
                content["avatar_url"] = playerContent["headImgUrl"]
                content["account"] = item
                result["players_list"].append(content)
        roomDatas.append(result)
    # for item in redis.smembers(ONLINE_ACCOUNTS_TABLE):
    #     if item in players:
    #         onlineNumber += 1

    auditNumber = redis.get(CLUB_AUDI_INTO_NUMBER % club_number) or 0
    print '[getRoomList][info] roomDatas[%s]'%roomDatas
    return {'code':0, 'roomData':roomDatas, "data": {"playerNumber": playersNumber, "active": onlineNumber, "roomNumber": roomlistNumber, "roomActiveNumber": roomActiveNumber, "club_number": club_number, "RoomCards": userRoomCards, "auditNumber": auditNumber}}



@hall_app.get('/club/history')
@web_util.allow_cross_request
@retry_insert_number()
def history(redis, session):
    """ 历史赢钱最多的玩家

    :param redis:
    :param session:
    :return:
    """
    sid = request.params.get('sid', '').strip()
    club_number = request.params.get("club_number", '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not club_number:
        return {"code": 1, 'msg': '俱乐部编号没有传递'}
    if not redis.exists(CLUB_ATTR % club_number):
        return {"code": 1, 'msg': '不存在这个俱乐部'}
    # 获取公会ID
    ownner_account = redis.hget(CLUB_ATTR % club_number, "club_user")
    path = redis.get(FORMAT_ACCOUNT2USER_TABLE % ownner_account)
    ag = redis.hget(path, 'parentAg')

    club_agent = "%s-%s" % (ag, club_number)

    playerExtends = {}
    playerDatas = []
    playHisList = []
    player_list = redis.smembers(CLUB_PLAYER_LIST % club_number)
    # player_list.add(ownner_account)
    # # for playerAccount in player_list:
    # #         LEN = 30
    # #         timeRe = 'startTime:[0-9]+'
    # #         roomRe = 'game:\w+'
    # #         playHis = PLAYER_PLAY_ROOM%(playerAccount)
    # #         data = redis.lrange(playHis, 0, LEN)
    # #         playerDatas.extend(data)
    LEN = 30
    timeRe = 'startTime:[0-9]+'
    roomRe = 'game:\w+'
    playerDatas = redis.smembers("club:replay:%s:set" % club_number)
    user_list = {}
    user_list_nick_name = {}
    playerDatas = set(playerDatas)
    win = {}

    dataTableDict = {}
    userScores = {}
    for hisData in playerDatas:

        timeData = re.search(timeRe, hisData)
        timeData = timeData.group()
        time = timeData.split(':')[1]
        roomData = re.search(roomRe, hisData)
        roomData = roomData.group()
        num = roomData.split(':')[1]

        if redis.exists(hisData):
            game2room = GAME2ROOM%(num, time)
            dataTable = PLAY_GAME_DATA%(num, time)
            if redis.exists(dataTable):

                players, gameid, scoreData = redis.hmget(dataTable, ('player', 'gameid', 'score'))
                name = redis.hget(GAME_TABLE % (gameid), 'name')
                players = players.split(':')
                roomId = num
                ownner_nickname = ''
                scores = []
                ownnerAccount = players[0].split(',')[1]
                account2user_table = FORMAT_ACCOUNT2USER_TABLE % (ownnerAccount)
                table = redis.get(account2user_table)
                ownnerNickname = redis.hget(table, 'nickname')


                for gamePlayer in players:
                    if not gamePlayer:
                        continue
                    hisPlayer = gamePlayer.split(',')[1]
                    account2user_table = FORMAT_ACCOUNT2USER_TABLE % (ownnerAccount)
                    table = redis.get(account2user_table)

                    hisPlayerNickName = redis.hget(table, 'nickname')
                    side = int(gamePlayer.split(',')[0])
                    score = int(scoreData.split(':')[side])
                    scores.append({"nickname": hisPlayerNickName, 'account': hisPlayer, 'score': score})
                    # user_list_nick_name[hisPlayer] = hisPlayerNickName

                if not redis.hget(dataTable, 'tag'):
                    win = reduce(lambda x, y: x if x["score"] > y["score"] else y, scores)
                    winScorePlayer = []
                    if win:
                        for item in scores:
                            if item["account"] == win["account"] or win["score"] == item["score"]:
                                winScorePlayer.append(item)

                        winScorePlayerNumber = len(winScorePlayer)
                        if IS_AVG:
                            avg = round(1.0 / winScorePlayerNumber, 2)
                            for item in winScorePlayer:
                                cur_account = item["account"]
                                user_list[cur_account] = user_list.get(cur_account, 0) + avg
                                dataTableDict[cur_account] = dataTableDict.get(cur_account, []) + [dataTable]
                                userScores[cur_account] = userScores.get(cur_account, 0) + item["score"]

                        else:
                            for item in winScorePlayer:
                                cur_account = item["account"]
                                user_list[cur_account] = user_list.get(cur_account, 0) + 1
                                dataTableDict[cur_account] = dataTableDict.get(cur_account, []) + [dataTable]
                                userScores[cur_account] = userScores.get(cur_account, 0) + item["score"]

                tag = 0
                if redis.hget(dataTable, 'tag'):
                    tag = 1
                playHisList.append(
                    {
                        "time": time,
                        "room_id": roomId,
                        "room_master": ownnerNickname,
                        "game_name": name,
                        "game_id": gameid,
                        "data": dataTable,
                        "tag" : tag,
                        "score": score
                     }
                )
        else:
            redis.lrem(playHis, hisData)
            return {"code": 1, 'msg': '没有数据'}


    user_win_data = []
    for item in user_list:
        user_result = {}
        user_result["dataTable"] = dataTableDict[item]
        user_result["number"] = user_list[item]
        user_result["score"] = userScores[item]
        user_result["account"] = item
        user_path = redis.get(FORMAT_ACCOUNT2USER_TABLE % item)
        user_id = user_path.split(":")[-1]
        user_result["nickname"] = redis.hget(user_path, "nickname")
        user_result["user_id"] = user_id
        user_win_data.append(user_result)

    user_win_data = sorted(user_win_data, key=lambda x: -x["number"])
    playHisList = sorted(playHisList, key=lambda x: -int(x["time"]))
    return {"code": 0, "list": playHisList, "win_data": user_win_data}



@hall_app.get('/club/historyBySelfToday')
@web_util.allow_cross_request
@retry_insert_number()
def historyBySelfToday(redis, session):
    """ 历史赢钱最多的玩家

    :param redis:
    :param session:
    :return:
    """
    sid = request.params.get('sid', '').strip()
    club_number = request.params.get("club_number", '').strip()
    datetime = request.params.get("datetime", '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not club_number:
        return {"code": 1, 'msg': '俱乐部编号没有传递'}
    if not redis.exists(CLUB_ATTR % club_number):
        return {"code": 1, 'msg': '不存在这个俱乐部'}
    if not datetime:
        datetime = time.strftime("%Y-%m-%d", time.localtime())

    # try:
    #     timestramp = time.strptime(datetime, "%Y-%m-%d")
    # except Exception as err:
    #     log_debug("[error]%s" % err)
    #     datetime = time.strftime("%Y-%m-%d", time.localtime())

    # 获取公会ID
    ownner_account = redis.hget(CLUB_ATTR % club_number, "club_user")
    path = redis.get(FORMAT_ACCOUNT2USER_TABLE % ownner_account)
    ag = redis.hget(path, 'parentAg')

    club_agent = "%s-%s" % (ag, club_number)

    playerExtends = {}
    playerDatas = []
    playHisList = []
    player_list = redis.smembers(CLUB_PLAYER_LIST % club_number)
    # player_list.add(ownner_account)
    # # for playerAccount in player_list:
    # #         LEN = 30
    # #         timeRe = 'startTime:[0-9]+'
    # #         roomRe = 'game:\w+'
    # #         playHis = PLAYER_PLAY_ROOM%(playerAccount)
    # #         data = redis.lrange(playHis, 0, LEN)
    # #         playerDatas.extend(data)
    LEN = 30
    timeRe = 'startTime:[0-9]+'
    roomRe = 'game:\w+'
    playerDatas = redis.smembers("club:replay:%s:%s:set" % (club_number, datetime))
    user_list = {}
    user_list_nick_name = {}
    playerDatas = set(playerDatas)
    win = {}

    dataTableDict = {}
    userScores = {}
    for hisData in playerDatas:

        timeData = re.search(timeRe, hisData)
        timeData = timeData.group()
        time = timeData.split(':')[1]
        roomData = re.search(roomRe, hisData)
        roomData = roomData.group()
        num = roomData.split(':')[1]

        if redis.exists(hisData):
            game2room = GAME2ROOM%(num, time)
            dataTable = PLAY_GAME_DATA%(num, time)
            if redis.exists(dataTable):

                players, gameid, scoreData = redis.hmget(dataTable, ('player', 'gameid', 'score'))
                name = redis.hget(GAME_TABLE % (gameid), 'name')
                players = players.split(':')
                roomId = num
                ownner_nickname = ''
                scores = []
                ownnerAccount = players[0].split(',')[1]
                account2user_table = FORMAT_ACCOUNT2USER_TABLE % (ownnerAccount)
                table = redis.get(account2user_table)
                ownnerNickname = redis.hget(table, 'nickname')
                accountList = set()

                for gamePlayer in players:
                    if not gamePlayer:
                        continue
                    hisPlayer = gamePlayer.split(',')[1]
                    accountList.add(hisPlayer)
                    account2user_table = FORMAT_ACCOUNT2USER_TABLE % (hisPlayer)
                    table = redis.get(account2user_table)

                    hisPlayerNickName = redis.hget(table, 'nickname')
                    side = int(gamePlayer.split(',')[0])
                    score = int(scoreData.split(':')[side])
                    scores.append({"nickname": hisPlayerNickName, 'account': hisPlayer, 'score': score})
                    # user_list_nick_name[hisPlayer] = hisPlayerNickName
                if account not in accountList:
                    continue

                playHisList.append(
                    {
                        "time": time,
                        "room_id": roomId,
                        "room_master": ownnerNickname,
                        "game_name": name,
                        "game_id": gameid,
                        "data": dataTable,
                        "score": score
                     }
                )
        else:
            redis.lrem(playHis, hisData)
            return {"code": 1, 'msg': '没有数据'}


    user_win_data = []
    playHisList = sorted(playHisList, key=lambda x: -int(x["time"]))
    return {"code": 0, "list": playHisList}



@hall_app.get('/club/historyByDay')
@web_util.allow_cross_request
@retry_insert_number()
def historyByDay(redis, session):
    """ 历史赢钱最多的玩家

    :param redis:
    :param session:
    :return:
    """
    sid = request.params.get('sid', '').strip()
    club_number = request.params.get("club_number", '').strip()
    datetime = request.params.get("datetime", '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not club_number:
        return {"code": 1, 'msg': '俱乐部编号没有传递'}
    if not redis.exists(CLUB_ATTR % club_number):
        return {"code": 1, 'msg': '不存在这个俱乐部'}
    if not datetime:
        datetime = time.strftime("%Y-%m-%d", time.localtime())
    log_debug(datetime)
    # try:
    #     timestramp = time.strptime(datetime, "%Y-%m-%d")
    # except Exception as err:
    #     log_debug("[error]%s" % err)
    #     datetime = time.strftime("%Y-%m-%d", time.localtime())

    # 获取公会ID
    ownner_account = redis.hget(CLUB_ATTR % club_number, "club_user")
    path = redis.get(FORMAT_ACCOUNT2USER_TABLE % ownner_account)
    ag = redis.hget(path, 'parentAg')

    club_agent = "%s-%s" % (ag, club_number)

    playerExtends = {}
    playerDatas = []
    playHisList = []
    player_list = redis.smembers(CLUB_PLAYER_LIST % club_number)
    # player_list.add(ownner_account)
    # # for playerAccount in player_list:
    # #         LEN = 30
    # #         timeRe = 'startTime:[0-9]+'
    # #         roomRe = 'game:\w+'
    # #         playHis = PLAYER_PLAY_ROOM%(playerAccount)
    # #         data = redis.lrange(playHis, 0, LEN)
    # #         playerDatas.extend(data)
    LEN = 30
    timeRe = 'startTime:[0-9]+'
    roomRe = 'game:\w+'
    playerDatas = redis.smembers("club:replay:%s:%s:set" % (club_number, datetime))
    user_list = {}
    user_list_nick_name = {}
    playerDatas = set(playerDatas)
    win = {}

    dataTableDict = {}
    userScores = {}
    for hisData in playerDatas:

        timeData = re.search(timeRe, hisData)
        timeData = timeData.group()
        time = timeData.split(':')[1]
        roomData = re.search(roomRe, hisData)
        roomData = roomData.group()
        num = roomData.split(':')[1]

        if redis.exists(hisData):
            game2room = GAME2ROOM%(num, time)
            dataTable = PLAY_GAME_DATA%(num, time)
            if redis.exists(dataTable):

                players, gameid, scoreData = redis.hmget(dataTable, ('player', 'gameid', 'score'))
                name = redis.hget(GAME_TABLE % (gameid), 'name')
                players = players.split(':')
                roomId = num
                ownner_nickname = ''
                scores = []
                ownnerAccount = players[0].split(',')[1]
                account2user_table = FORMAT_ACCOUNT2USER_TABLE % (ownnerAccount)
                table = redis.get(account2user_table)
                ownnerNickname = redis.hget(table, 'nickname')


                for gamePlayer in players:
                    if not gamePlayer:
                        continue
                    hisPlayer = gamePlayer.split(',')[1]
                    account2user_table = FORMAT_ACCOUNT2USER_TABLE % (hisPlayer)
                    table = redis.get(account2user_table)

                    hisPlayerNickName = redis.hget(table, 'nickname')
                    side = int(gamePlayer.split(',')[0])
                    score = int(scoreData.split(':')[side])
                    scores.append({"nickname": hisPlayerNickName, 'account': hisPlayer, 'score': score})
                    # user_list_nick_name[hisPlayer] = hisPlayerNickName

                if not redis.hget(dataTable, 'tag'):
                    win = reduce(lambda x, y: x if x["score"] > y["score"] else y, scores)
                    winScorePlayer = []
                    if win:
                        for item in scores:
                            if item["account"] == win["account"] or win["score"] == item["score"]:
                                winScorePlayer.append(item)

                        winScorePlayerNumber = len(winScorePlayer)
                        if IS_AVG:
                            avg = round(1.0 / winScorePlayerNumber, 2)
                            for item in winScorePlayer:
                                cur_account = item["account"]
                                user_list[cur_account] = user_list.get(cur_account, 0) + avg
                                dataTableDict[cur_account] = dataTableDict.get(cur_account, []) + [dataTable]
                                userScores[cur_account] = userScores.get(cur_account, 0) + item["score"]

                        else:
                            for item in winScorePlayer:
                                cur_account = item["account"]
                                user_list[cur_account] = user_list.get(cur_account, 0) + 1
                                dataTableDict[cur_account] = dataTableDict.get(cur_account, []) + [dataTable]
                                userScores[cur_account] = userScores.get(cur_account, 0) + item["score"]

                tag = 0
                if redis.hget(dataTable, 'tag'):
                    tag = 1
                playHisList.append(
                    {
                        "time": time,
                        "room_id": roomId,
                        "room_master": ownnerNickname,
                        "game_name": name,
                        "game_id": gameid,
                        "data": dataTable,
                        "tag" : tag,
                        "score": score
                     }
                )
        else:
            redis.lrem(playHis, hisData)
            return {"code": 1, 'msg': '没有数据'}


    user_win_data = []
    for item in user_list:
        user_result = {}
        user_result["dataTable"] = dataTableDict[item]
        user_result["number"] = user_list[item]
        user_result["score"] = userScores[item]
        user_result["account"] = item
        user_path = redis.get(FORMAT_ACCOUNT2USER_TABLE % item)
        user_id = user_path.split(":")[-1]
        user_result["nickname"] = redis.hget(user_path, "nickname")
        user_result["user_id"] = user_id
        user_win_data.append(user_result)

    user_win_data = sorted(user_win_data, key=lambda x: -x["number"])
    playHisList = sorted(playHisList, key=lambda x: -int(x["time"]))
    return {"code": 0, "list": playHisList, "win_data": user_win_data}



@hall_app.post('/club/isManager')
@web_util.allow_cross_request
@retry_insert_number()
def isManager(redis, session):

    sid = request.forms.get('sid', '').strip()
    club_number = request.forms.get("club_number", '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}

    if redis.hget(CLUB_ATTR % club_number, "club_user") == account:
        return {"code": 0, 'msg': "成功", "status": 2}

    elif account in eval(redis.hget(CLUB_ATTR % club_number, 'club_manager')):
        return {"code": 0, 'msg': "成功", "status": 1}
    else:
        return {'code': 0, 'msg': '成功', 'status': -1}

@hall_app.post('/club/history_sign')
@web_util.allow_cross_request
@retry_insert_number()
def history_sign(redis, session):
    """ 标记历史记录， 下次查询的时候不再查询这些已经标记的记录
    :param redis:
    :param session:
    :return:
    """
    sid = request.forms.get('sid', '').strip()
    club_number = request.forms.get("club_number", '').strip()
    path_data = request.forms.get("path_data", '').strip()
    if isinstance(path_data, str):
        try:
            path_data = path_data.split(",")
        except:
            return {"code": 1, 'msg': '数据传输出错'}
    elif isinstance(path_data, list):
        path_data = path_data
    else:
        return {"code": 1, 'msg': '数据传输出错'}

    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not club_number:
        return {"code": 1, 'msg': '俱乐部编号没有传递'}
    if not redis.exists(CLUB_ATTR % club_number):
        return {"code": 1, 'msg': '不存在这个俱乐部'}
    # 获取公会ID
    try:
        ownner_account = redis.hget(CLUB_ATTR % club_number, "club_user")
        manager_list = eval(redis.hget(CLUB_ATTR % club_number, "club_manager"))
        if ownner_account != account and account not in manager_list:
            return {"code": 1, 'msg': '你没有权限进行设置'}
        path = redis.get(FORMAT_ACCOUNT2USER_TABLE % ownner_account)
        ag = redis.hget(path, 'parentAg')
        club_agent = "%s-%s" % (ag, club_number)

        for item in path_data:
            if redis.exists(item):
                redis.hset(item, 'tag', 'True')
        return {"code": 0, 'msg': '成功'}
    except:
        traceback.print_exc()
        return {"code": 1, 'msg': '失败'}

@hall_app.post('/club/club_into')
@web_util.allow_cross_request
@retry_insert_number()
def club_into(redis, session):
    """ 玩家进入俱乐部

    :param redis:
    :param session:
    :return:
    """
    sid = request.forms.get('sid', '').strip()
    club_number = request.forms.get("club_number", '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if not redis.exists(SessionTable):
        return {'code':-3,'msg':'sid 超时'}

    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}

    if not club_number:
        return {"code": 1, 'msg': '俱乐部编号没有传递'}

    if not redis.exists(CLUB_ATTR % club_number):
        return {"code": 1, 'msg': '不存在这个俱乐部'}

    msg = {"status": 0, "content": ""}
    if redis.exists(CLUB_ATTR % club_number):
        if account not in redis.smembers(CLUB_PLAYER_LIST % club_number):
            if redis.hget(CLUB_ATTR % club_number, "club_user") != account:
                return {"code": 1, "msg": '你不属于这个俱乐部不能进入'}
            else:
                # 获取自动开放是否存在消息提示
                allow = redis.hget("club:auto_create:allow", club_number) or 0
                if int(allow) == 1:
                    # 检查钻石是否足够
                    userTable = getUserByAccount(redis, account)
                    ag, maxScore, user_open_auth = redis.hmget(userTable, ('parentAg', 'maxScore', 'open_auth'))
                    id = userTable.split(':')[1]
                    print("club_into: %s" % USER4AGENT_CARD%(ag, id))
                    roomCards = redis.get(USER4AGENT_CARD%(ag, id)) or 0
                    if int(roomCards) < 100:
                        msg = {"status": 1, "content": "你的自动开房钻石将要消耗殆尽，请及时兑换, 避免造成无法自动开房的情况."}
                    elif int(roomCards) < 10:
                        msg = {"status": 1, "content": "你开启了自动开房服务，钻石不足10请及时兑换。"}
                    elif int(roomCards) < 5:
                        msg = {"status": 1, "content": "你的自动开放服务即将停止，请兑换钻石."}

        redis.set(CLUB_PLAYER_INTO % account, club_number)

        players = redis.smembers(CLUB_PLAYER_LIST % club_number)
        playersNumber = len(players) + 1
        onlineNumber = 0

        club_user = redis.hget(CLUB_ATTR % club_number, "club_user")
        userTable = redis.get(FORMAT_ACCOUNT2USER_TABLE % club_user)
        ag, maxScore, user_open_auth, isAgent = redis.hmget(userTable, ('parentAg', 'maxScore', 'open_auth', "isAgent"))
        if not isAgent:
            isAgent = 0
        else:
            isAgent = int(isAgent)
        id = userTable.split(':')[1]
        roomCards = redis.get(USER4AGENT_CARD % (ag, id)) or 0
        DSdiamond = redis.hget('users:%s' % id,'DSdiamond') or 0

        curPlayerTable = redis.get(FORMAT_ACCOUNT2USER_TABLE % account)
        curPlayerAg = redis.hget(curPlayerTable, 'parentAg')
        curPlayerId = curPlayerTable.split(":")[1]
        curPlayerCards = redis.get(USER4AGENT_CARD % (curPlayerAg, curPlayerId)) or 0


        ownerAccount = redis.hget(userTable, 'account')
        otherRooms = MY_OTHER_ROOMS % account
        otherRoomsDict = {i.split(":")[-2]: i for i in redis.lrange(otherRooms, 0, -1)}

        id = userTable.split(':')[1]
        maxScore, userBaseScore = redis.hmget(userTable, ('maxScore', 'baseScore'))
        print maxScore, userBaseScore
        if not userBaseScore:
            userBaseScore = DEFAULT_BASE_SCORE
        groupId = redis.hget(userTable, 'parentAg')
        print maxScore, userBaseScore
        if not maxScore:
            maxScore = 1
        try:
            roomLists = redis.smembers(AG2SERVER % ("%s-%s" % (groupId, club_number)))
        except:
            roomLists = []
        roomlistNumber = 0
        roomActiveNumber = 0
        for roomNum in roomLists:
            # print '[getRoomList][info] ROOM2SERVER[%s]' % ROOM2SERVER % (roomNum)
            gameName, dealer, playerCount, maxPlayer, gameid, baseScore, ruleText, gameState = redis.hmget(
                ROOM2SERVER % (roomNum),
                ('gameName', 'dealer', 'playerCount', 'maxPlayer', 'gameid', 'baseScore', 'ruleText', "gameState"))
            if not ruleText:
                continue
            if not baseScore:
                baseScore = 1
            print 'baseScore[%s],userBaseScore[%s]' % (baseScore, userBaseScore)
            try:
                hidden = int(redis.hget(ROOM2SERVER % (roomNum), 'hidden'))
            except:
                hidden = 0

            if isinstance(userBaseScore, str):
                userBaseScore = map(int, eval(userBaseScore))

            print userBaseScore
            if int(baseScore) != 1 and int(baseScore) not in userBaseScore:
                continue

            if not gameState:
                if otherRoomsDict.get(roomNum):
                    roomTable = otherRoomsDict.get("roomNum")
                    try:
                        gameState = int(redis.hget(roomTable, "gameType"))
                    except Exception as err:
                        # redis.lrem(otherRooms, roomTable)
                        gameState = 0
            else:
                try:
                    if int(gameState) == 1:
                        roomActiveNumber += 1
                except Exception as err:
                    gameState = 1

            onlineNumber += len(redis.lrange(ROOM2ACCOUNT_LIST % roomNum, 0, -1))
            roomlistNumber += 1

        isManager = 0
        if redis.hget(CLUB_ATTR % club_number, "club_user") == account:
            isManager = 2
        elif account in eval(redis.hget(CLUB_ATTR % club_number, 'club_manager')):
            isManager = 1
        else:
            isManager = -1

        return {"code":0, "msg": '成功', "data": {"playerNumber": playersNumber, "active": onlineNumber, "roomNumber": roomlistNumber, "roomActiveNumber": roomActiveNumber, "club_number": club_number}, "prompt": msg, "isManager": isManager, "clubroomCards": roomCards,'DSdiamond':DSdiamond, "curPlayerCards": curPlayerCards}
    return {"code": 1, "msg": '失败， 俱乐部不存在'}


@hall_app.post('/club/getPlayHis')
@web_util.allow_cross_request
@retry_insert_number()
def do_getPlayHis(redis,session):
    """
    获得历史回放
    """
    sid = request.forms.get('sid','').strip()
    getAccount = request.forms.get('account','').strip()

    SessionTable = FORMAT_USER_HALL_SESSION%(sid)
    if not redis.exists(SessionTable):
        return {'code':-3,'msg':'sid 超时'}

    account = redis.hget(SessionTable, 'account')
    if getAccount:
        account = getAccount
    print '[do_getPlayHis] account[%s] getAccount[%s]'%(account, getAccount)

    playHisList = []
    LEN = 30
    timeRe = 'startTime:[0-9]+'
    roomRe = 'game:\w+'
    playHis = PLAYER_PLAY_ROOM%(account)
    data = redis.lrange(playHis, 0, LEN)
    for hisData in data:
        timeData = re.search(timeRe, hisData)
        timeData = timeData.group()
        time = timeData.split(':')[1]
        roomData = re.search(roomRe, hisData)
        roomData = roomData.group()
        num = roomData.split(':')[1]
        if redis.exists(hisData):
            game2room = GAME2ROOM%(num, time)
            dataTable = PLAY_GAME_DATA%(num, time)
            if redis.exists(dataTable):
                players, gameid, scoreData = redis.hmget(dataTable, ('player', 'gameid', 'score'))
                players = players.split(':')
                for gamePlayer in players:
                    if not gamePlayer:
                        continue
                    hisPlayer = gamePlayer.split(',')[1]
                    if hisPlayer == account:
                        side = int(gamePlayer.split(',')[0])
                        score = int(scoreData.split(':')[side])
                        name = redis.hget(GAME_TABLE%(gameid), 'name')
                        ownnerAccount = players[0].split(',')[1]
                        account2user_table = FORMAT_ACCOUNT2USER_TABLE%(ownnerAccount)
                        table = redis.get(account2user_table)
                        ownnerNickname = redis.hget(table, 'nickname')
                        playHisList.append({'side':side, 'time':time, 'gameid':gameid, 'roomId':num, 'score':score,\
                                'name':name, 'ownner':ownnerNickname})
                        break
        else:
            redis.lrem(playHis, hisData)

    if not playHisList:
        return {'code':-1, 'msg':'没有回放数据'}
    else:
        return {'code':0, 'playHis':playHisList}

@hall_app.post('/club/settting_auto_create_allow')
@web_util.allow_cross_request
@retry_insert_number()
def settting_auto_create_allow(redis, session):
    " 是否开启自动创房， 默认拒绝"
    try:
        sid = request.forms.get('sid', '').strip()
        club_number = request.forms.get("club_number", '').strip()
        # allow = int(request.forms.get("allow", '').strip())
    except Exception as err:
        return {"code": 1, 'msg': "参数错误"}
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not club_number:
        return {"code": 1, 'msg': '俱乐部编号没有传递'}
    if not redis.exists(CLUB_ATTR % club_number):
        return {"code": 1, 'msg': '不存在这个俱乐部'}

    ownerAccount = redis.hget(CLUB_ATTR % club_number, "club_user")
    if ownerAccount != account and account not in account in eval(redis.hget(CLUB_ATTR % club_number, 'club_manager')):
        return {"code": 1, 'msg': "失败, 你不能操作"}
    allow = redis.hget("club:auto_create:allow", club_number) or 0
    allow = int(allow)
    if allow == 0:
        settingAllow = 1
    else:
        settingAllow = 0
    if settingAllow == 1:
        # 判断是否能够开启自动开房
        # 检查钻石是否足够
        userTable = getUserByAccount(redis, ownerAccount)
        ag, maxScore, user_open_auth = redis.hmget(userTable, ('parentAg', 'maxScore', 'open_auth'))
        id = userTable.split(':')[1]
        print("settting_auto_create_allow: %s" % USER4AGENT_CARD % (ag, id))
        roomCards = redis.get(USER4AGENT_CARD % (ag, id)) or 0
        if int(roomCards) < 100:
            return {"code": 1, "msg": "俱乐部所属创建人钻石数不足100，请兑换后开启。 "}
    redis.hset("club:auto_create:allow", club_number, settingAllow)
    return {"code": 0, 'msg': "成功", "allow": settingAllow}

@hall_app.post('/club/get_auto_create_allow')
@web_util.allow_cross_request
@retry_insert_number()
def settting_auto_create_allow(redis, session):
    " 是否开启自动创房， 默认拒绝"
    try:
        sid = request.forms.get('sid', '').strip()
        club_number = request.forms.get("club_number", '').strip()
    except Exception as err:
        return {"code": 1, 'msg': "参数错误"}
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not club_number:
        return {"code": 1, 'msg': '俱乐部编号没有传递'}
    if not redis.exists(CLUB_ATTR % club_number):
        return {"code": 1, 'msg': '不存在这个俱乐部'}
    if not id:
        return {"code": 1, 'msg': 'ID不能为空'}
    if redis.hget(CLUB_ATTR % club_number, "club_user") != account and account not in account in eval(redis.hget(CLUB_ATTR % club_number, 'club_manager')):
        return {"code": 1, 'msg': "失败, 你不能操作"}

    allow = redis.hget("club:auto_create:allow", club_number) or 0
    allow = int(allow)
    return {"code": 0, 'msg': "成功", "data": allow}




@hall_app.post('/club/auto_create')
@web_util.allow_cross_request
@retry_insert_number()
def setting_auto_create(redis,session):
    "自动开房设置"

    sid = request.forms.get('sid', '').strip()
    club_number = request.forms.get("club_number", '').strip()
    gameid = request.forms.get("gameid", '').strip()
    rule = request.forms.get("rule", '').strip()
    id = request.forms.get("id", '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    # parentAg = redis.hget(SessionTable, "parentAg")

    club_user = redis.hget(CLUB_ATTR % club_number, "club_user")
    userTable = getUserByAccount(redis, club_user)
    parentAg = redis.hget(userTable, "parentAg")
    agClubNumber = "%s-%s" % (club_number, parentAg)
    log_debug(u"创建出来的规则：%s" % rule)
    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not club_number:
        return {"code": 1, 'msg': '俱乐部编号没有传递'}
    if not redis.exists(CLUB_ATTR % club_number):
        return {"code": 1, 'msg': '不存在这个俱乐部'}
    if not id:
        return {"code": 1, 'msg': 'ID不能为空'}

    if redis.hget(CLUB_ATTR % club_number, "club_user") != account and account not in account in eval(redis.hget(CLUB_ATTR % club_number, 'club_manager')):
        return {"code": 0, 'msg': "失败, 你不能操作"}

    redis.hmset(CLUB_EXTENDS_ATTRIBUTE % (agClubNumber, id), {
        "gameid": gameid,
        "rule": rule,
    })
    return {"code": 0, 'msg': '成功'}

@hall_app.post('/club/clear_auto_create')
@web_util.allow_cross_request
@retry_insert_number()
def clear_auto_create(redis,session):
    "清楚"
    sid = request.forms.get('sid', '').strip()
    club_number = request.forms.get("club_number", '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)


    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not club_number:
        return {"code": 1, 'msg': '俱乐部编号没有传递'}
    if not redis.exists(CLUB_ATTR % club_number):
        return {"code": 1, 'msg': '不存在这个俱乐部'}
    if not id:
        return {"code": 1, 'msg': 'ID不能为空'}
    if redis.hget(CLUB_ATTR % club_number, "club_user") != account and account not in account in eval(redis.hget(CLUB_ATTR % club_number, 'club_manager')):
        return {"code": 0, 'msg': "失败, 你不能操作"}
    club_user = redis.hget(CLUB_ATTR % club_number, "club_user")
    userTable = getUserByAccount(redis, club_user)
    parentAg = redis.hget(userTable, "parentAg")
    agClubNumber = "%s-%s" % (club_number, parentAg)
    for i in range(1, 6):
        if not redis.exists(CLUB_EXTENDS_ATTRIBUTE % (agClubNumber, i)):
            redis.sadd(CLUB_EXTENDS_LIST_ATTRIBUTE%(agClubNumber), CLUB_EXTENDS_ATTRIBUTE % (agClubNumber, i))
            redis.hset(CLUB_EXTENDS_ATTRIBUTE %(agClubNumber, i), 'id', i)
        else:
            redis.hmset(CLUB_EXTENDS_ATTRIBUTE % (agClubNumber, i), {
                "id": i,
                "rule": '',
                "gameid": ''
            })
    return {"code": 0, 'msg': '成功'}

@hall_app.get('/club/auto_create')
@web_util.allow_cross_request
@retry_insert_number()
def get_setting_auto_create(redis,session):
    "自动开房设置"

    sid = request.params.get('sid', '').strip()
    club_number = request.params.get("club_number", '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not club_number:
        return {"code": 1, 'msg': '俱乐部编号没有传递'}
    if not redis.exists(CLUB_ATTR % club_number):
        return {"code": 1, 'msg': '不存在这个俱乐部'}
    if not id:
        return {"code": 1, 'msg': 'ID不能为空'}

    # data = redis.hget(CLUB_ATTR % club_number, 'club_manager')
    # if not data:
    #     data = set()
    # else:
    #     data = eval(data)
    # if redis.hget(CLUB_ATTR % club_number, "club_user") != account and account not in data:
    #     return {"code": 1, 'msg': "失败, 你不能操作"}
    club_user = redis.hget(CLUB_ATTR % club_number, "club_user")
    data = redis.smembers(CLUB_PLAYER_LIST % club_number)
    if account not in data and account != club_user:
        return {"code": 1, 'msg': "你不是这个俱乐部的成员，不能查看该数据。"}

    userTable = getUserByAccount(redis, club_user)
    parentAg = redis.hget(userTable, "parentAg")

    agClubNumber = "%s-%s" % (club_number, parentAg)
    for i in range(1, 6):
        if not redis.exists(CLUB_EXTENDS_ATTRIBUTE % (agClubNumber, i)):
            redis.sadd(CLUB_EXTENDS_LIST_ATTRIBUTE%(agClubNumber), CLUB_EXTENDS_ATTRIBUTE % (agClubNumber, i))
            redis.hset(CLUB_EXTENDS_ATTRIBUTE %(agClubNumber, i), 'id', i)
    apply_data = []
    for i in redis.smembers(CLUB_EXTENDS_LIST_ATTRIBUTE%(agClubNumber)):
        auto_datas = redis.hgetall(i)
        if auto_datas.get("rule") and auto_datas.get("gameid"):
            rule = auto_datas.get("rule")
            gameId = auto_datas.get("gameid")
            params = eval(rule)
            log_debug(u"查看存储的规则:%s" % rule)
            isOther = params[0]
            try:
                isOther = int(isOther)
            except:
                pass
            del params[0]
            print params

            # if params[-1] > maxScore:
            #     params[-1] = maxScore
            needRoomCards = int(params[-2])

            for index, data in enumerate(redis.lrange(USE_ROOM_CARDS_RULE % (gameId), 0, -1)):
                datas = data.split(':')
                name, cards = datas[0], datas[1]
                try:
                    playCount = int(datas[2])
                except:
                    playCount = 0
                    # if int(cards) == needRoomCards:
                    # break
                if int(index) == needRoomCards:
                    needRoomCards = int(cards)
                    params[-2] = needRoomCards
                    break
                playCount = -1
            # if playCount < 0:
            #     return {'code': -1, 'msg': '房间规则已修改，请重新加载创房页面'}
            params.insert(-2, playCount)

            rule = str(params)
            ruleText = getRuleText(rule, gameId, redis)
            log_info(ruleText)
            gameTable = GAME_TABLE % (gameId)
            gameId = int(gameId)
            gameType = CLUB_GAME_ATTRIBUTE_NUMBER.get(gameId, 0) or 0
            gameName, relationOpts, relationAndOpts = redis.hmget(gameTable,
                                                                  ('name', 'dependSetting', 'dependAndSetting'))

            auto_datas["rule_text"] = u"%s" % ruleText.replace("\n", '|')
            auto_datas["game_name"] = u"%s" % gameName
            auto_datas["gameType"]  = gameType
        apply_data.append(auto_datas)
    apply_data = sorted(apply_data, key=lambda x: int(x["id"]))
    return {"code": 0 , 'list': apply_data}


@hall_app.post('/club/getRoomSetting')
@web_util.allow_cross_request
@retry_insert_number()
def do_club_getRoomSetting(redis,session):
    """
    获取创建房间设置信息
    """
    curTime = datetime.now()
    sid = request.forms.get('sid','').strip()
    club_number = request.forms.get("club_number", '').strip()
    if not club_number:
        return {"code": 1, 'msg': "不能没有俱乐部编号"}
    if not redis.exists(CLUB_ATTR%club_number):
        return {"code": 1, 'msg': '俱乐部不存在'}

    #return
    print 'do_getRoomSetting'
    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}
    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not club_number:
        return {"code": 1, 'msg': '俱乐部编号没有传递'}
    if not redis.exists(CLUB_ATTR % club_number):
        return {"code": 1, 'msg': '不存在这个俱乐部'}
    if not id:
        return {"code": 1, 'msg': 'ID不能为空'}

    creator_club_account = redis.hget(CLUB_ATTR%club_number, "club_user")
    if account != creator_club_account:
        if account not in redis.smembers(CLUB_PLAYER_LIST%club_number):
            return {"code": 1, 'msg': "你不是这个俱乐部的玩家"}

    try:
        print '[on getRoomSetting]sid[%s] account[%s]'%(sid, account)
    except Exception as e:
        print 'print error File', e

    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}

    if not redis.exists(SessionTable):
        return {'code':-3, 'msg':'sid 超时'}
    userTable = getUserByAccount(redis, creator_club_account)
    if not redis.exists(userTable):
        return {'code':-5,'msg':'该用户不存在'}

    groupId = redis.hget(userTable, 'parentAg')

    gameIdList = get_game_info(redis,groupId)
    if not gameIdList:
        return {'code':-1}
    gameDatas = []
    gameIdList = [gameid for gameid in gameIdList if gameid[0] not in redis.smembers("isgold:gameid:set")]
    gameDatas = []
    for gameId in gameIdList:

        # print(1222222, gameId)
        gameId = int(gameId[0])
        gameTable = GAME_TABLE%(gameId)
        gameName, relationOpts, relationAndOpts, other_info = redis.hmget(gameTable, (
        'name', 'dependSetting', 'dependAndSetting', 'other_info'))
        try:
            gameRuleUrl = redis.hget(gameTable,'template_url')
            if not gameRuleUrl:
                gameRuleUrl = '/intro/game_0.html'
        except:
            gameRuleUrl = '/intro/game_0.html'

        optionType = 1
        ruleLists = []
        # ruleLists.append({'title': "房费", 'list': ["房主支付", "代开房间"], 'Dependencies': [], 'message': [], 'type': 1, 'row': ""})
        roomCardsDatas = []
        for index, data in enumerate(redis.lrange(USE_ROOM_CARDS_RULE%(gameId), 0, -1)):
            datas = data.split(':')
            name, cards = datas[0], datas[1]
            # roomCardsDatas.append({'name':name, 'cards':int(cards)})
            roomCardsDatas.append({'name':name, 'cards':int(index)})
        rows = 0
        for ruleNum in redis.lrange(GAME2RULE%(gameId), 0, -1):
            ruleTile, ruleType, rule, message,depend= redis.hmget(GAME2RULE_DATA%(gameId, ruleNum), ('title', 'type', 'rule', 'message','depend'))
            try:
                message = message.split(',')
            except:
                message = []
            ruleDataList = rule.split(',')
            ruleData = {'type':int(ruleType), 'title':ruleTile, 'list':ruleDataList,'Dependencies':[], 'message':message,'rows':rows}
            if redis.hexists(GAME2RULE_DATA%(gameId, ruleNum), 'row'):
                ruleData['row'] = redis.hget(GAME2RULE_DATA%(gameId, ruleNum), 'row')
            if depend:
                dependsDatas = redis.hget(GAME2RULE_DATA%(gameId, ruleNum), 'depend').split(';')
                for depend in dependsDatas:
                    if depend == '0':
                        """
                        type:3 为空
                        """
                        ruleData['Dependencies'].append({'type':3,'list':[]})
                    else:
                        subInfo = depend.split('|')
                        ruleData['Dependencies'].append({'type':int(subInfo[0]),'list':subInfo[1].split(',')})
            rows+=1
            ruleLists.append(ruleData)

        if relationOpts:
            #或选项
            relationOpts = eval(relationOpts)
        else:
            relationOpts = {}

        if relationAndOpts:
            #与选项
            relationAndOpts = eval(relationAndOpts)
        else:
            relationAndOpts = {}

        gameDatas.append({'name':gameName,'relationOptsAnd':relationAndOpts,'relationOptsOr':relationOpts,'optionType':optionType, 'gameId':gameId,'ruleUrl':gameRuleUrl,'optionsData':ruleLists, 'cardUseDatas':roomCardsDatas, 'other_info':other_info})

    # print '[getRoomSetting][info] gameId[%s] gameRule[%s]'%(gameIdList,gameDatas)

    return {'code':0,'setting':gameDatas}

@hall_app.post("/club/getRoomListById")
@web_util.allow_cross_request
@retry_insert_number()
def getRoomListById(redis, session):
    """ 获取自动开房的某一个ID房间

    :param redis:
    :param session:
    :return:
    """
    sid = request.forms.get('sid', '').strip()
    if not sid:
        remote_disbaled(redis)
        return {"code": 1, "msg": "参数错误没有SID"}

    club_auto_id = request.forms.get('auto_id', '').strip()
    club_number = request.forms.get("club_number", '').strip()
    if not club_auto_id:
        return {"code": 1, 'msg': "没有开房ID"}
    club_auto_id = int(club_auto_id)
    print 'do_getRoomList'
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if verfiySid and sid != verfiySid:
        # session['member_account'],session['member_id'] = '',''
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
    if not redis.exists(SessionTable):
        remote_disbaled(redis)
        return {'code': -3, 'msg': 'sid 超时'}

    if redis.exists(CLUB_ATTR % club_number):
        if account not in redis.smembers(CLUB_PLAYER_LIST % club_number):
            if redis.hget(CLUB_ATTR % club_number, 'club_user') != account:
                return {"code": 1, 'msg': "你不能查看这个俱乐部的房间"}
    try:
        print '[on getRoomList]sid[%s] account[%s]' % (sid, account)
    except Exception as e:
        print 'print error File', e

    print 'account'

    uTbles = getUserByAccount(redis, account)
    ag, maxScore, user_open_auth = redis.hmget(uTbles, ('parentAg', 'maxScore', 'open_auth'))
    id = uTbles.split(':')[1]
    userRoomCards = redis.get(USER4AGENT_CARD % (ag, id))

    #club_user = redis.hget(CLUB_ATTR % club_number, "club_user")
    #userTable = redis.get(FORMAT_ACCOUNT2USER_TABLE % club_user)
    # ag, maxScore, user_open_auth = redis.hmget(userTable, ('parentAg', 'maxScore', 'open_auth'))
    #id = userTable.split(':')[1]



    club_user = redis.hget(CLUB_ATTR % club_number, "club_user")
    userTable = getUserByAccount(redis, club_user)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}

    id = userTable.split(':')[1]
    maxScore, userBaseScore = redis.hmget(userTable, ('maxScore', 'baseScore'))
    print maxScore, userBaseScore
    if not userBaseScore:
        userBaseScore = DEFAULT_BASE_SCORE
    groupId = redis.hget(userTable, 'parentAg')
    roomCards = redis.get(USER4AGENT_CARD % (groupId, id)) or 0

    print maxScore, userBaseScore
    if not maxScore:
        maxScore = 1
    try:
        roomLists = redis.smembers(AG2SERVER % ("%s-%s" % (groupId, club_number)))
    except:
        roomLists = []
    roomDatas = []
    ownerAccount = redis.hget(userTable, 'account')
    otherRooms = MY_OTHER_ROOMS % account
    print(otherRooms)
    # try:
    otherRoomsDict = {i.split(":")[-2]: i for i in redis.lrange(otherRooms, 0, -1)}
    # otherRoomsDict = {}
    # for item in otherRooms:
    #     try:
    #         item.split(":")[-2] = item
    #     except Exception as err:
    #         redis.lrem()
    #         continue
    players = redis.smembers(CLUB_PLAYER_LIST % club_number)
    playersNumber = len(players) + 1
    roomlistNumber = 0
    roomActiveNumber = 0
    onlineNumber = 0
    for roomNum in roomLists:
        # 查看是否自动开房
        auto_id = redis.hget(ROOM2SERVER % (roomNum), 'auto_id')
        if not auto_id:
            continue
        auto_id = int(auto_id)
        if auto_id != club_auto_id:
            continue

        # print '[getRoomList][info] ROOM2SERVER[%s]' % ROOM2SERVER % (roomNum)
        gameName, dealer, playerCount, maxPlayer, gameid, baseScore, ruleText, gameState, room_club_number, curGameCount, maxGameCount = redis.hmget(
            ROOM2SERVER % (roomNum), (
            'gameName', 'dealer', 'playerCount', 'maxPlayer', 'gameid', 'baseScore', 'ruleText', "gameState",
            "club_number", "curGameCount", "maxGameCount"))
        if club_number != room_club_number:
            continue

        if not ruleText:
            continue
        if not baseScore:
            baseScore = 1
        print 'baseScore[%s],userBaseScore[%s]' % (baseScore, userBaseScore)
        try:
            hidden = int(redis.hget(ROOM2SERVER % (roomNum), 'hidden'))
        except:
            hidden = 0

        if isinstance(userBaseScore, str):
            userBaseScore = map(int, eval(userBaseScore))

        print userBaseScore
        if int(baseScore) != 1 and int(baseScore) not in userBaseScore:
            continue

        if not gameState:
            if otherRoomsDict.get(roomNum):
                roomTable = otherRoomsDict.get("roomNum")
                try:
                    gameState = int(redis.hget(roomTable, "gameType"))
                except Exception as err:
                    # redis.lrem(otherRooms, roomTable)
                    gameState = 0
        else:
            try:
                gameState = int(gameState)
                if gameState == 1:
                    roomActiveNumber += 1
            except Exception as err:
                gameState = 1
        gameText = ''
        if gameState == 1:
            curGameCount = curGameCount if curGameCount else 0
            maxGameCount = maxGameCount if maxGameCount else 0
            gameText = "（%s/%s）" % (curGameCount, maxGameCount)

        onlineNumber += len(redis.lrange(ROOM2ACCOUNT_LIST % roomNum, 0, -1))
        roomlistNumber += 1
        gameType = CLUB_GAME_ATTRIBUTE_NUMBER.get(int(gameid),
                                                  0) or 0  # redis.hget(GAME_TABLE % gameid, "gameType") or 0



        result = {'gameName': gameName, 'dealer': dealer, 'playerCount': playerCount, 'maxPlayer': maxPlayer,
                  'roomNum': roomNum, 'gameid': gameid, 'ruleText': ruleText.replace("\n", '|'),
                  'baseScore': int(baseScore), 'gameType': int(gameType), "gameState": gameState,
                  "curGameCount": curGameCount if curGameCount else 0,
                  "maxGameCount": maxGameCount if maxGameCount else 0,
                  "numberOfInnings": gameText, "auto_id": auto_id}
        result["players_list"] = []
        if redis.exists(ROOM2ACCOUNT_LIST % roomNum):
            accountContent = redis.lrange(ROOM2ACCOUNT_LIST % roomNum, 0, -1)
            for item in accountContent:
                playerContent = redis.hgetall(redis.get(FORMAT_ACCOUNT2USER_TABLE % item))
                content = {}
                content["nickname"] = playerContent["nickname"]
                content["avatar_url"] = playerContent["headImgUrl"]
                content["account"] = item
                result["players_list"].append(content)
        roomDatas.append(result)
    # for item in redis.smembers(ONLINE_ACCOUNTS_TABLE):
    #     if item in players:
    #         onlineNumber += 1


    # print '[getRoomList][info] roomDatas[%s]' % roomDatas
    return {'code': 0, 'roomData': roomDatas,
            "data": {"playerNumber": playersNumber, "active": onlineNumber, "roomNumber": roomlistNumber,
                     "roomActiveNumber": roomActiveNumber, "club_number": club_number, "RoomCards": userRoomCards, "clubRoomCards": roomCards}}


@hall_app.post("/club/createOtherRoom")
@web_util.allow_cross_request
@retry_insert_number(time=2, count=6)
def createOtherRoom(redis, session):
    """ 创建俱乐部房间其他的方法

    :param redis:
    :param session:
    :return:
    """
    #gameId = request.forms.get('gameid', '').strip()
    #gameId = int(gameId)
    #rule = request.forms.get('rule', '').strip()
    sid = request.forms.get('sid', '').strip()
    auto_id = request.forms.get("id", '').strip()
    hidden = 1
    club_number = request.forms.get("club_number", '').strip()
    
    if not sid or not auto_id or not club_number:
        remote_disbaled(redis)

    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if not redis.exists(CLUB_ATTR % club_number):
        return {'code': 1, 'msg': '俱乐部不存在'}
    # 检查当前用户是否是这个俱乐部的主人
    # if redis.hget(CLUB_ATTR % club_number, "club_user") != account:
    #     # 检查当前用户是否存在俱乐部
    #     if club_number not in redis.smembers(CLUB_PLAYER_TO_CLUB_LIST % club_number):
    #         return {'code': 1, 'msg': '你没有加入这个俱乐部！不能创建房间'}
    #     # 这个俱乐部是否允许俱乐部成员创建房间
    #     if int(redis.hget(CLUB_ATTR % club_number, "club_use_create_room")) != 1:
    #         return {'code': 1, 'msg': '你不能创建房间！请和俱乐部创始人联系'}
    # 获取规则
    if verfiySid and sid != verfiySid:
        # session['member_account'],session['member_id'] = '',''
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}

    if not redis.exists(SessionTable):
        remote_disbaled(redis)
        return {'code': -3, 'msg': 'sid 超时'}

    # 获取俱乐部主人的ACCOUNT
    club_admin_user = redis.hget(CLUB_ATTR % club_number, "club_user")
    userTable = getUserByAccount(redis, club_admin_user)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}



    # 检查是否数据该俱乐部的玩家
    if account not in redis.smembers(CLUB_PLAYER_LIST % club_number) and account != club_admin_user:
        return {"code": 1, 'msg': "你不是这个俱乐部的玩家。"}

    # print 'do_CreateRoom'
    # try:
    #     print '[on createRoom]sid[%s] account[%s] gameId[%s] rule[%s] hidden[%s]' % (sid, account, gameId, rule, hidden)
    # except Exception as e:
    #     print 'print error File', e


    ag, maxScore, user_open_auth = redis.hmget(userTable, ('parentAg', 'maxScore', 'open_auth'))
    adminTable = AGENT_TABLE % (ag)
    agValid, agent_open_auth = redis.hmget(adminTable, ('valid', 'open_auth'))
    # 获取是否有权限开房
    open_room = get_user_open_auth(redis, user_open_auth, agent_open_auth)
    if agValid != '1':
        print  '[CraeteRoom][info] agentId[%s] has freezed. valid[%s] ' % (ag, agValid)
        return {'code': -7, 'msg': '该公会已被冻结,不能创建或加入该公会的房间'}

    createRulePath = CLUB_EXTENDS_ATTRIBUTE % ("%s-%s" % (club_number, ag), auto_id)
    rule, gameId = redis.hmget(createRulePath, 'rule', "gameid")
    if not rule or not gameId:
        return {"code": 1, 'msg': "不存在这个规则的RULE"}

    id = userTable.split(':')[1]
    roomCards = redis.get(USER4AGENT_CARD % (ag, id))
    if not maxScore:
        maxScore = 1
    params = eval(rule)

    isOther = params[0]
    try:
        isOther = int(isOther)
    except:
        pass
    del params[0]
    print params

    if params[-1] > maxScore:
        params[-1] = maxScore
    needRoomCards = int(params[-2])

    for index, data in enumerate(redis.lrange(USE_ROOM_CARDS_RULE % (gameId), 0, -1)):
        datas = data.split(':')
        name, cards = datas[0], datas[1]
        try:
            playCount = int(datas[2])
        except:
            playCount = 0
        if int(index) == needRoomCards:
            needRoomCards = int(cards)
            params[-2] = needRoomCards
            break
        playCount = -1
    if playCount < 0:
        return {'code': -1, 'msg': '房间规则已修改，请重新加载创房页面'}
    params.insert(-2, playCount)

    rule = str(params)

    if int(roomCards) < needRoomCards:
        return {'code': -6, 'msg': '钻石不足'}
    print '[do_CreateRoom][info] roomCards[%s] needRoomCards[%s]' % (roomCards, needRoomCards)

    countPlayerLimit = 30
    gameTable = GAME_TABLE % (gameId)
    maxRoomCount = redis.hget(gameTable, 'maxRoomCount')
    if maxRoomCount:
        countPlayerLimit = int(maxRoomCount) * 4
    reservedServers = []
    serverList = redis.lrange(FORMAT_GAME_SERVICE_SET % (gameId), 0, -1)
    for serverTable in serverList:
        playerCount = redis.hincrby(serverTable, 'playerCount', 0)
        roomCount = redis.hincrby(serverTable, 'roomCount', 0)
        if not playerCount:
            playerCount = 0
        if not roomCount:
            roomCount = 0
        playerCount = int(playerCount)
        roomCount = int(roomCount)
        countPlayerLimit = int(countPlayerLimit)
        if countPlayerLimit and (playerCount >= countPlayerLimit or roomCount >= countPlayerLimit / 4):
            continue
        _, _, _, currency, ipData, portData = serverTable.split(':')
        reservedServers.append((currency, ipData, portData))

    if reservedServers:
        ruleText = getRuleText(rule, gameId, redis)
        params = eval(rule)
        params.append(int(hidden))
        rule = str(params)
        result, data = otherCreateRoom(gameId, auto_id, rule, ruleText, ag, club_number, club_admin_user, redis)
        if not result:
            return {"code": 1, "msg": data}
        return {"code": 0, 'room_id': data, "gameid": gameId, "msg": "成功"}
    else:
        return {'code': -1, 'msg': '已经超出服务器的最大负荷房间数！请联系客服.'}

@hall_app.post('/club/dissolveMyRoom')
@web_util.allow_cross_request
@retry_insert_number()
def do_dissolveMyRoomList(redis,session):
    """
    解散俱乐部房间
    """
    sid  =  request.forms.get('sid','').strip()
    roomId = request.forms.get('roomId','').strip()
    print 'do_getRoomList'
    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    club_number = request.forms.get("club_number", '').strip()
    if not club_number:
        return {"code": 1, 'msg': "不能没有俱乐部编号"}
    if not redis.exists(CLUB_ATTR%club_number):
        return {"code": 1, 'msg': '俱乐部不存在'}

    try:
        print '[on dissolveMyRoomList]sid[%s] account[%s] roomId[%s]'%(sid, account, roomId)
    except Exception as e:
        print 'print error File', e

    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not redis.exists(SessionTable):
        return {'code':-3, 'msg':'sid 超时'}
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code':-5,'msg':'该用户不存在'}

    #
    # 判断该用户是否有权限解散
    ownner_account = redis.hget(CLUB_ATTR % club_number, "club_user").strip()
    manager_list = eval(redis.hget(CLUB_ATTR % club_number, "club_manager"))
    print("account:%s, ownner_account:%s" % (account, ownner_account))

    if ownner_account != account and account not in manager_list:
        return {"code": 1, 'msg': '你不能操作'}

    account = redis.hget(SessionTable, 'account')
    roomTable = ROOM2SERVER%(roomId)
    otherRooms = MY_OTHER_ROOMS%ownner_account
    otherRoomList = redis.lrange(otherRooms, 0, -1)
    roomIds = []
    for table in otherRoomList:
        roomIds.append(table.split(':')[-2])
    if roomId not in roomIds:
        return {'code':1,'msg':'无权限的房间'}
    try:
        gameId, playerCount, maxPlayer = redis.hmget(roomTable, ('gameid', 'playerCount', 'maxPlayer'))
        playerCount = int(playerCount)
        maxPlayer = int(maxPlayer)
    except:
        return {'code':1,'msg':'房间已解散或不存在'}
    if int(playerCount) == int(maxPlayer):
        return {'code':1,'msg':'房间内玩家已满，无法解散'}

    ag, maxScore, user_open_auth,DSdiamond = redis.hmget(userTable, ('parentAg', 'maxScore', 'open_auth','DSdiamond'))
    id = userTable.split(':')[1]
    roomCards = redis.get(USER4AGENT_CARD % (ag, id))

    sendProtocol2GameService(redis, gameId,HEAD_SERVICE_PROTOCOL_DISSOLVE_ROOM%(roomId))
    return {'code':0,'msg':'房间解散成功', "roomCards": roomCards,'DSdiamond':DSdiamond}


