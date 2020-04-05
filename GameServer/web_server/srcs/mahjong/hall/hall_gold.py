#-*- coding:utf-8 -*-
#!/usr/bin/python

"""
     金币场模块
"""
from hall import hall_app
from hall_func import getUserByAccount
from common.utilt import *
from bottle import request, response, template, static_file
from model.goldModel import *
from model.red_envelope_db_define import RED_ENVELOPE_GAMEID_SET
from model.protoclModel import sendProtocol2GameService
from common import  web_util,convert_util
from common.record_player_info import record_player_balance_change
from bag.bag_func import check_vcoin_baselive

@hall_app.post('/party/gold/getThreshold')
@web_util.allow_cross_request
def getGoldThreshold(redis, session):
    """
        获取该玩家进入二人麻将的门槛
    """
    sid = request.forms.get('sid', '').strip()
    gameid = request.forms.get('gameid', '').strip()

    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    DSbonus, bindGuild = redis.hmget(userTable,'DSbonus','bind_guild')
    try:
        DSbonus = int(DSbonus)
    except:
        DSbonus = 0
    CheckThreshold = True
    CanJoinRoom = False
    if DSbonus > 25000:
        CheckThreshold = False
    if bindGuild:
        CanJoinRoom = True
    return {'code':0,'CheckThreshold':CheckThreshold,'CanJoinRoom':CanJoinRoom,'DSbonus':DSbonus}

@hall_app.post('/party/gold/gameList')
@web_util.allow_cross_request
def getPartyGoldGameList(redis,session):
    """
    获取金币场场次列表
    """
    sid = request.POST.get('sid', '').strip()
    if not sid:
        return
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    groupId = redis.hget(userTable, 'parentAg')
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    data = get_GoldGameList(redis)
    sort = PARTY_GOLD_GAME_LIST_SORT[:]

    """ 只有这个公会有余干金币场 抚州金币场 """
    #if groupId == '213482':
    #sort.append('446')
    #sort.append('448')
    #sort.append('447')
    sort.append('449')  # 二人麻将
    #sort.append('452')  # 鸡大胡麻将
    sort.append('555')  # 经典牛牛
    sort.append('556')  # 明牌牛牛
    sort.append('557')  # 欢乐拼点
    #sort.append('560')  # 斗地主
    #sort.append('562')  # 十三水
    sort.append('666')  # 欢乐牛牛
    #sort.append('570')  # 测试

    return {'code': 0, 'msg': '金币场场次列表获取成功','data':data,'sort':sort}


@hall_app.post('/notJoinGoldRoom')
@web_util.allow_cross_request
def do_NotJoinGoldRoom(redis, session):
    """
        取消加入金币场
    """
    sid = request.forms.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    try:
        print '[on notJoinPartyRoom]sid[%s] account[%s]' % (sid, account)
    except Exception as e:
        print 'print error File', e

    if verfiySid and sid != verfiySid:
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    return {'code': 0}


@hall_app.post('/joinGoldRoom')
@web_util.allow_cross_request
def do_JoinGoldRoom(redis, session):
    """
        加入金币场
    """
    log_debug('do_joinGoldRoom  *********** ')
    gameid = request.forms.get('gameid', '').strip()
    playid = request.forms.get('id', '').strip()
    sid = request.forms.get('sid', '').strip()
    need = request.forms.get('need', '').strip()  # 参与条件
    cost = request.forms.get('cost', '').strip()  # 报名费
    cost = int(cost)
    base_score = request.forms.get('baseScore', '').strip()  # 底分
    base_score = int(base_score)

    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    if verfiySid and sid != verfiySid:
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}

    groupId = redis.hget(userTable, 'parentAg')
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    gameTable = GAME_TABLE % gameid
    if not redis.exists(gameTable):
        return {'code': -1, 'msg': 'gameId 不存在'}

    serverList = redis.lrange(FORMAT_GAME_SERVICE_SET % gameid, 0, -1)
    if not serverList:
        return {'code': -1, 'msg': '服务器忙碌或维护中'}

    myroom_key = redis.get(GOLD_ROOM_ACCOUNT_KEY % account)
    if myroom_key:
        roomid, myplayid = redis.hmget(myroom_key, 'roomid', 'playid')
        ip, port, _gameid = redis.hmget(ROOM2SERVER % roomid, ('ip', 'port', 'gameid'))
        if ip and port and _gameid:
            if playid != myplayid or _gameid != gameid:
                return {'code': -1, 'msg': '您正在别的场次游戏中'}
            else:
                return {'code': 0, 'msg': '已经在金币场中'}
        else:
            redis.delete(GOLD_ROOM_ACCOUNT_KEY % account)

    if not redis.sismember(RED_ENVELOPE_GAMEID_SET, gameid):
        coin, DSbonus = redis.hmget(FORMAT_USER_TABLE % userTable.split(':')[1], 'gold', 'DSbonus')
        if DSbonus:
            DSbonus = int(DSbonus)
        else:
            DSbonus = 0
        if not coin:
            coin = 0
        coin = int(coin)
        need = need.split(',')
        min_need = need[0]
        if not min_need:
            min_need = 0
        min_need = int(min_need)
        if len(need) == 1:
            max_need = 9999999999
        else:
            max_need = need[1]
        max_need = int(max_need)
        if DSbonus and DSbonus > 25000:
            min_need = cost
            max_need = 9999999999
        if coin < min_need:
            return {'code': -2, 'msg': u'您携带的金币数不足以进入本场次游戏，请充值后进入。'}
        if coin > max_need:
            return {'code': -1, 'msg': u'您携带的金币数超出本场次上限，请进入更高一级的场次游戏。'}
    elif str(gameid) in ["1008"]:
        # 元宝领低保
        # 默认12
        threshold = 12
        res = check_vcoin_baselive(uid,threshold)
        if res == 1:
            return {'code': -2, 'msg': u'您携带的元宝数不足以进入本场次游戏，请充值后进入。'}
        elif res == 2:
            calculateTotalWelfareFee(redis,12,7,1)
            from bag.bag_config import bag_redis
            uid = userTable.split(':')[1]
            yuanbao_final = bag_redis.hget(PLAYER_ITEM_HASH%uid,'3')
            yuanbao_final = int(yuanbao_final) if yuanbao_final else 0
            record_player_balance_change(bag_redis,userTable,3,threshold,yuanbao_final,7)
            return {'code': 3, 'msg': u'您携带的元宝数不足以进入本场次游戏，系统为您免费补足12元宝。'}

    _uuid = get_uuid()
    serverTable = random.choice(serverList)
    sendProtocol2GameService(redis, gameid, "joinGoldRoom|%s|%s|%s" % (account, playid, _uuid), serverTable)
    redis.hmset(GOLD_ACCOUNT_WAIT_JOIN_TABLE % account, {'playid': playid, 'gameid': gameid})
    redis.expire(GOLD_ACCOUNT_WAIT_JOIN_TABLE % account, 5)
    return {'code': 0, 'msg': '加入金币场成功'}


@hall_app.post('/checkJoinGoldRoom')
@web_util.allow_cross_request
def do_CheckJoinGoldRoom(redis, session):
    """
        确认加入金币场结果
    """
    sid = request.forms.get('sid', '').strip()
    print 'do_CheckJoinPartyRoom'
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if verfiySid and sid != verfiySid:
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}

    myroom_key = redis.get(GOLD_ROOM_ACCOUNT_KEY % account)
    if myroom_key:
        roomid = redis.hget(myroom_key, 'roomid')
        ip, port, gameid = redis.hmget(ROOM2SERVER % roomid, ('ip', 'port', 'gameid'))
        if gameid and redis.sismember(RED_ENVELOPE_GAMEID_SET, gameid):
            return {'code': 0, 'ip': ip, 'port': port, 'gameid': gameid,
                'isParty': PARTY_TYPE_RE} 
        return {'code': 0, 'ip': ip, 'port': port, 'gameid': gameid,
                'isParty': PARTY_TYPE_GOLD}

    if not redis.exists(GOLD_ACCOUNT_WAIT_JOIN_TABLE % account):
        return {'code': -1, 'msg': u'匹配超时'}

    playid, gameid = redis.hmget(GOLD_ACCOUNT_WAIT_JOIN_TABLE % account, 'playid', 'gameid')
    roomids = redis.smembers(GOLD_CAN_JOIN_ROOM_SET % (gameid, playid))
    if not roomids:
        return {'code': 0, 'maxPlayers': 5, 'waitPlayers': 1}
    _f = [item.split(':')[4] for item in redis.lrange(GOLD_ROOM_ACCOUNT_LIST % account, 0, 1) if item]
    _roomids = [roomid for roomid in list(roomids) if roomid not in _f]
    if not _roomids:
        return {'code': 0, 'maxPlayers': 5, 'waitPlayers': 1}
    log_debug(u'可以加入的房间 {0}'.format(_roomids))

    choice_roomids = []
    for roomid in _roomids:
        playerCount = redis.hget(ROOM2SERVER % roomid, 'playerCount')
        playerCount = int(playerCount) if playerCount else 0
        if not playerCount:
            continue
        choice_roomids.append(roomid)
    if not choice_roomids:
        roomid = random.choice(_roomids)
    else:
        roomid = random.choice(choice_roomids)
    redis.hmset(SessionTable, {'roomid': roomid, 'action': 0})
    ip, port, gameid = redis.hmget(ROOM2SERVER % roomid, ('ip', 'port', 'gameid'))
    if not ip or not port or not gameid:
        redis.srem(GOLD_CAN_JOIN_ROOM_SET % (gameid, playid), roomid)

    if gameid and redis.sismember(RED_ENVELOPE_GAMEID_SET, gameid):
        return {'code': 0, 'ip': ip, 'port': port, 'gameid': gameid,
                'isParty': PARTY_TYPE_RE}        
    return {'code': 0, 'ip': ip, 'port': port, 'gameid': gameid,
            'isParty': PARTY_TYPE_GOLD}


@hall_app.get('/gold/rank')
@web_util.allow_cross_request
def onGetRank(redis, session):
    """
        获取排行榜数据
    """
    sid = request.GET.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if verfiySid and sid != verfiySid:
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
    userTable = getUserByAccount(redis, account)

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}

    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    picUrl, gender, groupId, isVolntExitGroup, maxScore, baseScore = \
        redis.hmget(userTable, ('headImgUrl', 'sex', 'parentAg', 'isVolntExitGroup', 'maxScore', 'baseScore'))
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}
    data = get_gold_rank(redis, groupId, account)
    return {'code': 0, 'data': data}


@hall_app.post('/welfare')
@web_util.allow_cross_request
def getWelfare(redis, session):
    """ 
        福利系统
    """
    sid = request.forms.get('sid', '').strip()

    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if verfiySid and sid != verfiySid:
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
    userTable = getUserByAccount(redis, account)

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}

    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    picUrl, gender, groupId, isVolntExitGroup, maxScore, baseScore = \
        redis.hmget(userTable, ('headImgUrl', 'sex', 'parentAg', 'isVolntExitGroup', 'maxScore', 'baseScore'))
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    res = get_welfare_info(redis, account)

    return {'code': 0, 'data': res}


@hall_app.post('/welfare/sign')
@web_util.allow_cross_request
def doWelfareSign(redis, session):
    """ 
        签到
    """
    sid = request.forms.get('sid', '').strip()

    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if verfiySid and sid != verfiySid:
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
    userTable = getUserByAccount(redis, account)

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}

    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    picUrl, gender, groupId, isVolntExitGroup, maxScore, baseScore = \
        redis.hmget(userTable, ('headImgUrl', 'sex', 'parentAg', 'isVolntExitGroup', 'maxScore', 'baseScore'))
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    res = do_PlayerWelfareSign(redis, account)

    if not res:
        return {'code': 1, 'msg': "今日已签到"}
    else:
        calculateTotalWelfareFee(redis,int(res),0,0)
        from bag.bag_config import bag_redis
        uid = userTable.split(':')[1]
        gold_final = redis.hget(userTable, 'gold')
        gold_final = int(gold_final) if gold_final else 0
        record_player_balance_change(bag_redis,userTable,2,int(res),gold_final,0)
        return {'code': 0, 'msg': "签到成功,获得 {0} 金币".format(res)}


@hall_app.post('/welfare/patch_sign')
@web_util.allow_cross_request
def doWelfarePatchSign(redis, session):
    """ 
        补签
    """
    sid = request.forms.get('sid', '').strip()

    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if verfiySid and sid != verfiySid:
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
    userTable = getUserByAccount(redis, account)

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}

    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    picUrl, gender, groupId, isVolntExitGroup, maxScore, baseScore = \
        redis.hmget(userTable, ('headImgUrl', 'sex', 'parentAg', 'isVolntExitGroup', 'maxScore', 'baseScore'))
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    id = userTable.split(':')[1]

    return doPatchSign(redis, account, groupId, id, userTable)

@hall_app.post('/welfare/share')
@web_util.allow_cross_request
def doWelfareShare(redis, session):
    """
        分享
    """
    sid = request.forms.get('sid', '').strip()

    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if verfiySid and sid != verfiySid:
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
    userTable = getUserByAccount(redis, account)

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}

    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    picUrl, gender, groupId, isVolntExitGroup, maxScore, baseScore = \
        redis.hmget(userTable, ('headImgUrl', 'sex', 'parentAg', 'isVolntExitGroup', 'maxScore', 'baseScore'))
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    res = do_PlayerWelfareShare(redis, account)
    if res['code'] == 0:
        calculateTotalWelfareFee(redis,res['gold'],1,0)
        from bag.bag_config import bag_redis
        uid = userTable.split(':')[1]
        gold_final = redis.hget(userTable, 'gold')
        gold_final = int(gold_final) if gold_final else 0
        record_player_balance_change(bag_redis,userTable,2,res['gold'],gold_final,1)
    return res


@hall_app.post('/welfare/coin/GMSet')
@web_util.allow_cross_request
def checkWelfareIsGM(redis, session):
    """
        设置该玩家金币 
    """
    sid = request.forms.get('sid', '').strip()
    coinNum = request.forms.get('coinNum', '').strip()
    isNumber = all(c in "0123456789.+-" for c in coinNum)
    if not coinNum or not isNumber:
        return {'code': 1, 'msg': '输入值错误'}
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if player_set_gold(redis, account, coinNum):
        return {'code': 0, 'msg': '设置金币成功'}
    return {'code': -1, 'msg': '设置金币失败'}


@hall_app.post('/welfare/insurance')
@web_util.allow_cross_request
def doWelfareInsurancen(redis, session):
    """ 
        低保
    """
    sid = request.forms.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    res = doWelfareById(redis, uid, account, '2')
    return res


@hall_app.post('/welfare/get_welfare')
@web_util.allow_cross_request
def do_get_welfare(redis, session):
    """ 
        获取福利
    """
    sid = request.forms.get('sid', '').strip()
    id = request.forms.get('id', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if verfiySid and sid != verfiySid:
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
    userTable = getUserByAccount(redis, account)

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}

    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    picUrl, gender, groupId, isVolntExitGroup, maxScore, baseScore = \
        redis.hmget(userTable, ('headImgUrl', 'sex', 'parentAg', 'isVolntExitGroup', 'maxScore', 'baseScore'))
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    res = doWelfareById(redis, uid, account, id) 
    # 将获取福利的记录存入数据库
    record_welfare_info_into_db(redis,res,userTable)
    return res

def record_welfare_info_into_db(redis,res,userTable):
    """
        将获取福利的记录存入数据库
    """
    from bag.bag_config import bag_redis
    uid = userTable.split(':')[1]
    gold_final = redis.hget(userTable, 'gold')
    gold_final = int(gold_final) if gold_final else 0
    if res['code'] == 0 and res['id'] == '1':
        calculateTotalWelfareFee(redis,res['gold'],3,0)    
        record_player_balance_change(bag_redis,userTable,2,res['gold'],gold_final,3)  

    if res['code'] == 0 and res['id'] == '2':
        calculateTotalWelfareFee(redis,res['gold'],2,0)
        record_player_balance_change(bag_redis,userTable,2,res['gold'],gold_final,2)

    if res['code'] == 0 and res['id'] == '6':
        player_item =  'player:item:uid:%s:hash' % uid
        ticket_num = bag_redis.hget(player_item,'15')
        ticket_num = int(ticket_num) if ticket_num else 0
        record_player_balance_change(bag_redis,userTable,15,res['ticket'],ticket_num,36)         

@hall_app.post('/welfare/get_reward')
@web_util.allow_cross_request
def do_get_reward(redis, session):
    """ 
        获取奖励
    """
    sid = request.forms.get('sid', '').strip()
    id = request.forms.get('id', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if verfiySid and sid != verfiySid:
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
    userTable = getUserByAccount(redis, account)

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}

    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    picUrl, gender, groupId, isVolntExitGroup, maxScore, baseScore = \
        redis.hmget(userTable, ('headImgUrl', 'sex', 'parentAg', 'isVolntExitGroup', 'maxScore', 'baseScore'))
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    res = doSignRewardById(redis, uid, account, id)

    if res['code'] == 0:
        id_str_map = {'0':4,'1':5,'2':6}
        calculateTotalWelfareFee(redis,res['gold'],id_str_map[id],0)

        from bag.bag_config import bag_redis
        uid = userTable.split(':')[1]
        gold_final = redis.hget(userTable, 'gold')
        gold_final = int(gold_final) if gold_final else 0
        record_player_balance_change(bag_redis,userTable,2,res['gold'],gold_final,id_str_map[id])
    return res


@hall_app.post('/gold/personal_info')
@web_util.allow_cross_request
def do_get_personal_info(redis, session):
    """ 
        获取个人信息
    """
    sid = request.forms.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if verfiySid and sid != verfiySid:
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}
    userTable = getUserByAccount(redis, account)

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}

    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    picUrl, gender, groupId, isVolntExitGroup, maxScore, baseScore = \
        redis.hmget(userTable, ('headImgUrl', 'sex', 'parentAg', 'isVolntExitGroup', 'maxScore', 'baseScore'))
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    return get_personal_info(redis, account)
