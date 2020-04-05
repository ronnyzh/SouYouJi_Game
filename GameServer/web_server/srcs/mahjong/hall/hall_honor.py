# -*- coding:utf-8 -*-
# !/usr/bin/python

"""
     荣誉场模块
"""
from hall import hall_app
from hall_func import getUserByAccount
from common.utilt import *
from bottle import request, response, template, static_file
from model.protoclModel import sendProtocol2GameService
from common import web_util, convert_util
from model.goldModel import *
from model.honorModel import *
from model.userModel import get_user_open_auth
from model.hallModel import getRuleText
from hall_func import *
import random
from urlparse import urlparse
import traceback

HONOR_ROOM_SETTING = 'honor:setting:threshold:%s'
HONOR_ROOMS_SET = 'honor:gameList:set'
GOLD_ACCOUNT_WAIT_JOIN_TABLE = 'honor:account:%s:wait:join:table'
Honor_ACCOUNT_WAIT_JOIN_TABLE = 'honor:account:%s:wait:join:table'


@hall_app.post('/honor/joinHonorRoom')
@web_util.allow_cross_request
def do_JoinGoldRoom(redis, session):
    """
        加入荣誉场
    """
    gameid = request.forms.get('gameid', '').strip()
    sid = request.forms.get('sid', '').strip()
    uid = request.forms.get('uid', '').strip()
    if not uid:
        SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
        if verfiySid and sid != verfiySid:
            return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
        if not redis.exists(SessionTable):
            return {'code': -3, 'msg': 'sid 超时'}
        userTable = getUserByAccount(redis, account)
    else:
        userTable = 'users:%s' % uid
        account = redis.hget(userTable, ('account'))
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}

    groupId = redis.hget(userTable, 'parentAg')
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    gameTable = GAME_TABLE % gameid
    if not redis.exists(gameTable):
        return {'code': -1, 'msg': 'gameId 不存在'}

    if not redis.sismember(HONOR_ROOMS_SET, gameid):
        return {'code': -1, 'msg': '该GameId不是荣誉场'}

    serverList = redis.lrange(FORMAT_GAME_SERVICE_SET % gameid, 0, -1)
    if not serverList:
        return {'code': -1, 'msg': '服务器忙碌或维护中'}

    myroom_key = redis.get(GOLD_ROOM_ACCOUNT_KEY % account)
    if myroom_key:
        roomid, playid = redis.hmget(myroom_key, 'roomid', 'playid')
        ip, port, _gameid = redis.hmget(ROOM2SERVER % roomid, ('ip', 'port', 'gameid'))
        if ip and port and _gameid:
            if _gameid != gameid:
                return {'code': -1, 'msg': '您正在别的场次游戏中'}
            else:
                return {'code': 0, 'msg': '已经在金币场中'}
        else:
            redis.delete(GOLD_ROOM_ACCOUNT_KEY % account)

    # honor = redis.hget(FORMAT_USER_TABLE % userTable.split(':')[1], ('honor'))

    canJoinPlayIdList = getAccountCanJoinPlayId(redis, account, gameid)
    if not canJoinPlayIdList:
        return {'code': -2, 'msg': u'您携带的荣誉值不足以进入本游戏，请前往消消乐小游戏获取'}

    _uuid = get_uuid()
    playid = max(canJoinPlayIdList)
    serverTable = random.choice(serverList)
    sendProtocol2GameService(redis, gameid, "joinHonror|%s|%s|%s" % (account, playid, _uuid), serverTable)
    redis.hmset(Honor_ACCOUNT_WAIT_JOIN_TABLE % account, {'gameid': gameid})
    redis.expire(Honor_ACCOUNT_WAIT_JOIN_TABLE % account, 5)
    print GOLD_ACCOUNT_WAIT_JOIN_TABLE % account
    return {'code': 0, 'msg': '加入荣誉场成功'}


@hall_app.post('/honor/checkJoinHonorRoom')
@web_util.allow_cross_request
def do_checkJoinHonorRoom(redis, session):
    """
        确认加入荣誉场结果
    """
    sid = request.forms.get('sid', '').strip()
    uid = request.forms.get('uid', '').strip()
    if sid:
        SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
        if verfiySid and sid != verfiySid:
            return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}

        if not redis.exists(SessionTable):
            return {'code': -3, 'msg': 'sid 超时'}
    else:
        userTable = 'users:%s' % uid
        account = redis.hget(userTable, 'account')

    myroom_key = redis.get(GOLD_ROOM_ACCOUNT_KEY % account)
    if myroom_key:
        roomid = redis.hget(myroom_key, 'roomid')
        ip, port, gameid = redis.hmget(ROOM2SERVER % roomid, ('ip', 'port', 'gameid'))

        if redis.sismember(HONOR_ROOMS_SET, gameid):
            return {'code': 0, 'ip': ip, 'port': port, 'gameid': gameid, 'isParty': PARTY_TYPE_HONOR}
        else:
            return {'code': 0, 'ip': ip, 'port': port, 'gameid': gameid, 'isParty': PARTY_TYPE_GOLD}

    if not redis.exists(Honor_ACCOUNT_WAIT_JOIN_TABLE % account):
        return {'code': -1, 'msg': u'匹配超时'}

    gameid = redis.hget(Honor_ACCOUNT_WAIT_JOIN_TABLE % account, 'gameid')

    canJoinPlayIdList = getAccountCanJoinPlayId(redis, account, gameid)
    playid = max(canJoinPlayIdList)
    roomids = list(redis.smembers(GOLD_CAN_JOIN_ROOM_SET % (gameid, playid)))
    if not roomids:
        return {'code': 0, 'maxPlayers': 5, 'waitPlayers': 1}
    print roomids
    roomid = random.choice(roomids)
    redis.hmset(SessionTable, {'roomid': roomid, 'action': 7})
    ip, port, gameid = redis.hmget(ROOM2SERVER % roomid, ('ip', 'port', 'gameid'))
    if not ip or not port or not gameid:
        redis.srem(GOLD_CAN_JOIN_ROOM_SET % (gameid, playid), roomid)

    return {'code': 0, 'ip': ip, 'port': port, 'gameid': gameid, 'isParty': PARTY_TYPE_HONOR}


@hall_app.post('/honor/modifyPlayerHonor')
@web_util.allow_cross_request
def do_modifyPlayerHonor(redis, session):
    sid = request.forms.get('sid', '').strip()
    uid = request.forms.get('uid', '').strip()
    isrm = request.forms.get('isrm', '').strip()
    number = request.forms.get('number', '').strip()
    try:
        number = int(number)
        isrm = int(isrm)
    except Exception as error:
        traceback.print_exc()
        return {'code': -1, 'msg': '参数错误'}
    if not uid:
        SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
        if verfiySid and sid != verfiySid:
            return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}

        if not redis.exists(SessionTable):
            return {'code': -3, 'msg': 'sid 超时'}
        userTable = 'users:%s' % uid
    else:
        userTable = 'users:%s' % uid
        account = redis.hget(userTable, 'account')
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    if isrm:
        redis.hset(userTable, 'honor', number)
    else:
        redis.hincrby(userTable, 'honor', number)
    honor = redis.hget(userTable, ('honor'))
    return {'code': 0, 'msg': u'设置成功,玩家当前荣誉值为%s' % (honor)}


@hall_app.post('/honor/addHonorGame')
@web_util.allow_cross_request
def do_addHonorGame(redis, session):
    gameid = request.forms.get('gameid', '').strip()
    if redis.sismember(HONOR_ROOMS_SET, gameid):
        return {'code': -1, 'msg': '该GameId已是荣誉场'}
    redis.sadd(HONOR_ROOMS_SET, gameid)
    return {'code': 0, 'msg': '已成功添加'}


@hall_app.post('/honor/rmHonorGame')
@web_util.allow_cross_request
def do_rmHonorGame(redis, session):
    gameid = request.forms.get('gameid', '').strip()
    if not redis.sismember(HONOR_ROOMS_SET, gameid):
        return {'code': -1, 'msg': '该GameId不是荣誉场'}
    redis.srem(HONOR_ROOMS_SET, gameid)
    return {'code': 0, 'msg': '已成功删除'}


@hall_app.get('/honor/getHonorGame')
@web_util.allow_cross_request
def do_getHonorGame(redis, session):
    games = list(redis.smembers(HONOR_ROOMS_SET))
    return {'code': 0, 'msg': '荣誉场列表获取成功', 'games': games}


@hall_app.post('/honor/setVIP')
@web_util.allow_cross_request
def do_setHonorVIP(redis, session):
    uid = request.forms.get('uid', '').strip()
    type = int(request.forms.get('type', '').strip())
    userTable = 'users:%s' % uid
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    if type:
        redis.hset(userTable, 'isVip', 1)
        return {'code': 0, 'msg': '添加用户VIP标识成功'}
    else:
        redis.hset(userTable, 'isVip', 0)
        return {'code': 0, 'msg': '移除用户VIP标识成功'}


@hall_app.post('/honor/createRoom')
@web_util.allow_cross_request
@retry_insert_number()
def do_honor_CreateRoom(redis, session):
    """
    创建房间接口
    """
    # tt = request.forms.get('tt', '').strip()
    # if tt not in ACCEPT_TT:
    # print "try getServer: get faild, code[1]."
    # return {'code' : -1}
    gameId = request.forms.get('gameid', '').strip()
    rule = request.forms.get('rule', '').strip()
    sid = request.forms.get('sid', '').strip()
    hidden = request.forms.get('hidden', '').strip()

    print '[do_honor_CreateRoom]'
    if not gameId or len(gameId) < 1:
        return
    if not sid or len(sid) < 1:
        remote_disbaled(redis)
        return
    if not rule or len(rule) < 1:
        return
    if not hidden or len(hidden) < 1:
        return
    try:
        gameId = int(gameId)
    except Exception as e:
        print 'gameID error File', e
        return
    if not gameId:
        return
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    try:
        print '[on createRoom]sid[%s] account[%s] gameId[%s] rule[%s] hidden[%s]' % (sid, account, gameId, rule, hidden)
    except Exception as e:
        print 'print error File', e
        return

    if verfiySid and sid != verfiySid:
        # session['member_account'],session['member_id'] = '',''
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
    if not redis.exists(SessionTable):
        remote_disbaled(redis)
        return {'code': -3, 'msg': 'sid 超时'}

    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    ag, user_open_auth = redis.hmget(userTable, ('parentAg', 'open_auth'))
    adminTable = AGENT_TABLE % (ag)
    agValid, agent_open_auth = redis.hmget(adminTable, ('valid', 'open_auth'))
    # 获取是否有权限开房
    open_room = get_user_open_auth(redis, user_open_auth, agent_open_auth)
    if agValid != '1':
        print  '[CraeteRoom][info] agentId[%s] has freezed. valid[%s] ' % (ag, agValid)
        return {'code': -7, 'msg': '该公会已被冻结,不能创建或加入该公会的房间'}

    if not redis.sismember(HONOR_ROOMS_SET, gameId):
        return {'code': -1, 'msg': '该游戏不属于荣誉场,不可创建好友组局'}

    isVip, honor = redis.hmget(userTable, ('isVip', 'honor'))
    honor = int(honor or 0)
    if isVip:
        isVip = True
    else:
        isVip = False
    if not isVip:
        need_honor = getNeedHonorDefault(redis, gameId)
        if honor < need_honor:
            return {'code': -1, 'msg': '荣誉值不足%s,不可创建房间' % (need_honor)}

    id = userTable.split(':')[1]
    roomCards = redis.get(USER4AGENT_CARD % (ag, id))

    params = eval(rule)

    isOther = params[0]
    try:
        isOther = int(isOther)
    except:
        pass
    del params[0]
    print params

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
    if playCount < 0:
        return {'code': -1, 'msg': '房间规则已修改，请重新加载创房页面'}
    params.insert(-2, playCount)

    rule = str(params)

    print '[do_CreateRoom][info] roomCards[%s] needRoomCards[%s]' % (roomCards, needRoomCards)

    if not isOther:

        key = redis.get(ACCOUNT2WAIT_JOIN_PARTY_TABLE % account)
        # for key in redis.keys(WAIT_JOIN_PARTY_ROOM_PLAYERS%('*', '*', '*')):
        if key:
            if account in redis.lrange(key, 0, -1):
                try:
                    game, serviceTag = redis.get('account:%s:wantServer' % account).split(',')
                    message = HEAD_SERVICE_PROTOCOL_NOT_JOIN_PARTY_ROOM % (account, ag)
                    redis.lpush(FORMAT_SERVICE_PROTOCOL_TABLE % (game, serviceTag), message)
                except:
                    print '[account wantServer][%s]' % (redis.get('account:%s:wantServer' % account))
                redis.lrem(key, account)
                # if account in waitJoinPlayers:
                # return {'code':-1, 'msg':'等待加入游戏中'}

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
        currency, serverIp, serverPort = reservedServers[0]
        ruleText = getRuleText(rule, gameId, redis)
        if isOther:
            if open_room == 0:  # 没有代开权限
                return {'code': -1000, 'msg': '没有代开房间权限'}

            params = eval(rule)
            params.append(int(hidden))
            rule = str(params)
            protocolStr = HEAD_SERVICE_PROTOCOL_CREATE_OTHER_ROOM % (account, ag, rule, ruleText)
            redis.rpush(FORMAT_SERVICE_PROTOCOL_TABLE % (gameId, '%s:%s:%s' % (currency, serverIp, serverPort)), protocolStr)
            return {'code': 0, 'msg': '房间开启成功', 'ip': '', 'port': ''}

        redis.hmset(SessionTable,
                    {
                        'action': 1,
                        'rule': rule,
                        'ruleText': ruleText,
                        'hidden': hidden,
                    }
                    )

        urlRes = urlparse(request.url)
        domain = urlRes.netloc.split(':')[0]

        return {'code': 0, 'ip': domain, 'port': serverPort, 'isParty': PARTY_TYPE_HONOR}
    else:
        return {'code': -1, 'msg': '服务器忙碌或维护中'}


@hall_app.post('/honor/joinRoom')
@web_util.allow_cross_request
@retry_insert_number()
def do_honor_joinRoom(redis, session):
    """
    加入房间接口
    """
    roomid = request.forms.get('roomid', '').strip()
    sid = request.forms.get('sid', '').strip()
    print 'do_joinRoom'
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    try:
        print '[on joinRoom]sid[%s] account[%s] roomid[%s]' % (sid, account, roomid)
    except Exception as e:
        print 'print error File', e

    if verfiySid and sid != verfiySid:
        # session['member_account'],session['member_id'] = '',''
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}

    redis.hmset(SessionTable,
                {
                    'action': 0,
                    'roomid': roomid,
                }
                )
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}

    groupId, bind_guild, bind_type = redis.hmget(userTable, ('parentAg', 'bind_guild', 'bind_type'))

    agentTable = AGENT_TABLE % (groupId)
    agValid = redis.hget(agentTable, 'valid')
    if agValid != '1':
        print  '[JoinRoom][info] agentId[%s] has freezed. valid[%s] ' % (groupId, agValid)
        return {'code': -7, 'msg': '该公会已被冻结,不能创建或加入该公会的房间'}

    print '[join game][info] groupId[%s] roomid[%s]' % (groupId, roomid)
    ip, port, ag, gameid, playerCount, maxPlayer, baseScore, club_number = redis.hmget(ROOM2SERVER % (roomid),
                                                                                       ('ip', 'port', 'ag', 'gameid', 'playerCount', 'maxPlayer', 'baseScore', "club_number"))
    print '[join game][info] ip[%s] port[%s] ag[%s] gameid[%s] playerCount[%s] maxPlayer[%s] baseScore[%s]' \
          % (ip, port, ag, gameid, playerCount, maxPlayer, baseScore)
    print '[join game]club_number[%s] gameid[%s]' % (club_number, gameid)

    if not redis.sismember(HONOR_ROOMS_SET, gameid):
        return {'code': -1, 'msg': '该房间游戏不属于荣誉场,不可加入该房间'}

    if not ip:
        return {'code': -2, 'msg': '房间已解散'}

    if redis.exists(GOLD_ROOM_DATA % (gameid, roomid)):
        return {'code': -2, 'msg': '您没有权限进入'}

    try:
        hidden, guildId = redis.hmget(ROOM2SERVER % (roomid), 'hidden', 'guildId')
        hidden = int(hidden)
    except:
        hidden = 1
    key = redis.get(ACCOUNT2WAIT_JOIN_PARTY_TABLE % account)
    if key:
        if account in redis.lrange(key, 0, -1):
            try:
                game, serviceTag = redis.get('account:%s:wantServer' % account).split(',')
                message = HEAD_SERVICE_PROTOCOL_NOT_JOIN_PARTY_ROOM % (account, ag)
                redis.lpush(FORMAT_SERVICE_PROTOCOL_TABLE % (game, serviceTag), message)
            except:
                print '[account wantServer][%s]' % (redis.get('account:%s:wantServer' % account))
            redis.lrem(key, account)

    if int(playerCount) == int(maxPlayer):
        return {'code': -1, 'msg': '房间已满人'}

    if (hidden == 0) and (int(groupId) != int(ag)):
        return {'code': -1, 'msg': '不能进入其它公会的公会房间'}

    isVip, honor = redis.hmget(userTable, ('isVip', 'honor'))
    isVipRoom = redis.hget(ROOM2SERVER % (roomid), 'isVipRoom')
    honor = int(honor or 0)
    isVipRoom = int(isVipRoom or 0)
    if isVip:
        isVip = True
    else:
        isVip = False
    if not isVip and not isVipRoom:
        need_honor = getNeedHonorDefault(redis, gameid)
        if honor < need_honor:
            return {'code': -1, 'msg': '荣誉值不足%s,不可加入该房间' % (need_honor)}

    urlRes = urlparse(request.url)
    domain = urlRes.netloc.split(':')[0]

    return {'code': 0, 'ip': domain, 'port': port, 'gameid': gameid, 'isParty': PARTY_TYPE_HONOR}
