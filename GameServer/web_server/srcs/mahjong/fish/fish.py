#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    捕鱼大厅接口
"""

from bottle import request, Bottle, redirect, response,default_app
from web_db_define import *
import mahjong_pb2
import poker_pb2
import replay4proto_pb2
from talk_data import sendTalkData
from wechat.wechatData import *
from common.install_plugin import install_redis_plugin,install_session_plugin
from common.log import *
from common.utilt import allow_cross,getInfoBySid
from fish_util.fish_func import *
#from config.config import *
from fish_config import consts
from datetime import datetime, date, timedelta
from model.goodsModel import *
from model.userModel import do_user_modify_addr,do_user_del_addr,get_user_exchange_list
from model.hallModel import *
from model.protoclModel import sendProtocol2GameService
from model.mailModel import *
from model.fishModel import get_room_list
from common import web_util,log_util,convert_util
import time
import urllib2
import json
import random
import md5
import re
import pdb
from urlparse import urlparse
#from pyinapp import *
ACCEPT_NUM_BASE = 198326
ACCEPT_TT = [md5.new(str(ACCEPT_NUM_BASE+i)).hexdigest() for i in xrange(10)]
SESSION_TTL = 60*60

#生成捕鱼APP
fish_app = Bottle()
#获取配置
conf = default_app().config
#安装插件
install_redis_plugin(fish_app)
install_session_plugin(fish_app)

import fish_broad
import fish_invite
import fish_pay
import fish_exchange

FORMAT_PARAMS_POST_STR = "%s = request.forms.get('%s','').strip()"
FORMAT_PARAMS_GET_STR  = "%s = request.GET.get('%s','').strip()"
#用户信息
USER_INFO = ('headImgUrl', 'sex', 'isVolntExitGroup','coin','exchange_ticket')

@fish_app.post('/login')
@allow_cross
def do_login(redis,session):
    """
    大厅登录接口

    """
    tt = request.forms.get('tt', '').strip()
    curTime = datetime.now()
    ip = web_util.get_ip()
    getIp = request['REMOTE_ADDR']
    _account = request.forms.get('account', '').strip()
    clientType = request.forms.get('clientType', '').strip()
    if not clientType:
        clientType = 0
    passwd = request.forms.get('passwd', '').strip()
    login_type = request.forms.get('type', '').strip() #登录类型
    login_type = int(login_type)
    sid=0
    try:
        log_util.debug('[on login]account[%s] clientType[%s] passwd[%s] type[%s]'%(_account, clientType, passwd, login_type))
    except Exception as e:
        print 'print error File', e

    login_pools = redis.smembers(FORMAT_LOGIN_POOL_SET)
    log_util.debug('[try do_login] account[%s] login_pools[%s]'%(_account,login_pools))

    if _account in login_pools:
        log_util.debug('[try do_login] account[%s] is already login.'%(_account))
        return {'code':0}

    redis.sadd(FORMAT_LOGIN_POOL_SET,_account)
    log_util.debug('[try do_login] account[%s] login_pools[%s]'%(_account,login_pools))
    reAccount, rePasswd = onRegFish(redis, _account, passwd, login_type, ip)

    if reAccount:
        if login_type:
            realAccount = redis.get(WEIXIN2ACCOUNT4FISH%(reAccount))
            # if not realAccount:
                # realAccount = redis.get(WEIXIN2ACCOUNT%(reAccount))
                # redis.set(WEIXIN2ACCOUNT4FISH%(reAccount), realAccount)
        else:
            realAccount = reAccount
        #读取昵称和group_id
        account2user_table = FORMAT_ACCOUNT2USER_TABLE%(realAccount)
        userTable = redis.get(account2user_table)
        id = userTable.split(':')[1]
        if not redis.sismember(ACCOUNT4WEIXIN_SET4FISH, realAccount): #初次登录
            redis.sadd(ACCOUNT4WEIXIN_SET4FISH, realAccount)
            redis.sadd(FORMAT_REG_DATE_TABLE4FISH%(curTime.strftime("%Y-%m-%d")), realAccount)
            redis.hset(userTable, 'coin', consts.GIVE_COIN_FIRST_LOGIN)
        if redis.exists(UNIONID2GROUP%reAccount):
            unionId = reAccount
            needJoinGroup = redis.get(UNIONID2GROUP%unionId)
            adminTable = AGENT_TABLE%(needJoinGroup)
            if redis.exists(adminTable):
                agValid, auto_check, groupType = redis.hmget(adminTable, ('valid', 'auto_check', 'type'))
                if agValid == '1' and groupType != '1':
                    if not auto_check:
                        auto_check = CHECK_SUCCESS
                    pipe = redis.pipeline()
                    if auto_check == CHECK_SUCCESS:
                        pipe.hset(FORMAT_USER_TABLE%(id), 'parentAg', needJoinGroup)
                        pipe.sadd(FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE%(needJoinGroup), id)
                    pipe.lpush(JOIN_GROUP_LIST%(needJoinGroup), id)
                    pipe.set(JOIN_GROUP_RESULT%(id), '%s:%s:%s'%(needJoinGroup, auto_check, curTime.strftime('%Y-%m-%d %H:%M:%S')))
                    pipe.execute()
        account, name, groupId,loginIp, loginDate, picUrl, gender,valid, lockCount = \
                redis.hmget(userTable, ('account', 'nickname', 'parentAg', 'lastLoginIp',\
                'lastLoginDate', 'picUrl', 'gender','valid', 'lockCount'))
        if not lockCount:
            lockCount = 0
        else:
            lockCount = int(lockCount)
        agentTable = AGENT_TABLE%(groupId)
        isTrail,shop = redis.hmget(agentTable,('isTrail','recharge'))
        if not isTrail:
            isTrail = 0

        #默认开放上次
        shop = 1

        shop = int(shop)
        if int(valid) == 0:
            #冻结后不能登录
            redis.srem(FORMAT_LOGIN_POOL_SET,_account)
            return {'code':105,'msg':'该帐号被冻结,请与客服联系'}

        #会话信息
        type2Sid = {
            True     :  sid,
            False    :  md5.new(str(id)+str(time.time())).hexdigest()
        }
        sid = type2Sid[login_type == 3]
        SessionTable = FORMAT_USER_HALL_SESSION%(sid)
        if redis.exists(SessionTable):
            log_util.debug("[try do_login] account[%s] sid[%s] is existed."%(curTime,realAccount,sid))
            redis.srem(FORMAT_LOGIN_POOL_SET,account)
            return {'code':-1, 'msg':'链接超时'}

        #同一账号不能同时登录
        loginMsg = ''
        if type==3:##网页登录不更新session
            pass
        else:
            redis.set(FORMAT_USER_PLATFORM_SESSION%(id),sid)

        #更新登录IP和登陆日期
            redis.hmset(userTable, {'lastLoginIp':request.remote_addr, 'lastLoginDate':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
                    'lastLoginClientType':clientType})

            #记录session信息
            session['member_id'] = id
            session['member_account'] = account
            session['member_lastIp'] = loginIp
            session['member_lastDate'] = loginDate
            session['session_key']  = sid
            pipe = redis.pipeline()
            pipe.hmset(SessionTable, {'account':account,'uid':id,'sid':sid,'loginIp':ip})
            pipe.expire(SessionTable, 60*40)
            pipe.execute()
            if (not loginDate) or loginDate.split(' ')[0] != datetime.now().strftime("%Y-%m-%d"): #当日没登录过，即第一次登录
                redis.hincrby(userTable, 'coin', consts.GIVE_COIN_DAY_LOGIN)
                loginMsg = '恭喜您获得内测每天奖励%s金币'%(consts.GIVE_COIN_DAY_LOGIN)
                if lockCount < consts.GIVE_LOCK_COUNT_DAY_LOGIN_MAX:
                    addLockCount = min(consts.GIVE_LOCK_COUNT_DAY_LOGIN_MAX - lockCount, consts.GIVE_LOCK_COUNT_DAY_LOGIN)
                    redis.hincrby(userTable, 'lockCount', addLockCount)
        urlRes = urlparse(request.url)
        serverIp = ''
        serverPort = 0
        gameid = 0
        # exitPlayerData = EXIT_PLAYER%(realAccount)
        # print '[hall][login]exitPlayerData[%s]'%(exitPlayerData)
        # if redis.exists(exitPlayerData):
            # serverIp, serverPort, game = redis.hmget(exitPlayerData, ('ip', 'port', 'game'))
            # print '[hall][login]exitPlayerData get succed, ip[%s], serverPort[%s], game[%s]'%(serverIp, serverPort, game)
            # serverIp = urlRes.netloc.split(':')[0]
            # gameid = redis.hget(ROOM2SERVER%(game), 'gameid')
            # try:
                # int(gameid)
            # except:
                # serverIp = ''
                # serverPort = 0
                # gameid = 0
                # redis.delete(exitPlayerData)
                # print '[hall][login][delete] exitPlayerData[%s]'%(exitPlayerData)
        if redis.sismember(ONLINE_ACCOUNTS_TABLE4FISH, realAccount):
            key = FORMAT_CUR_USER_GAME_ONLINE%(realAccount)
            if key:
                gameNum = redis.hget(key, 'game')
                if gameNum:
                    # gameId = redis.hget(ROOM2SERVER%(gameNum), 'gameid')
                    playerSid = redis.get(FORMAT_USER_PLATFORM_SESSION%(id))
                    sendProtocol2GameService(redis, gameNum, HEAD_SERVICE_PROTOCOL_KICK_MEMBER4REPEAT%(realAccount, playerSid))

        userInfo = {'name':name,'isTrail':int(isTrail),'shop':int(shop),'group_id':groupId,'account':reAccount, 'passwd':rePasswd}
        joinNum = ''
        id = userTable.split(':')[1]
        joinMessage = redis.get(JOIN_GROUP_RESULT%(id))
        if joinMessage:
            joinMessage = joinMessage.split(':')
            joinNum = int(joinMessage[0])
            joinResult = int(joinMessage[1])
            userInfo['applyId'] = joinNum
            if joinResult == 1:
                redis.delete(JOIN_GROUP_RESULT%(id))

        key = redis.get(ACCOUNT2WAIT_JOIN_PARTY_TABLE%account)
        # for key in redis.keys(WAIT_JOIN_PARTY_ROOM_PLAYERS%('*', '*', '*')):
        if key:
            if account in redis.lrange(key, 0, -1):
                try:
                    gameId, serviceTag = redis.get('account:%s:wantServer'%account).split(',')
                    message = HEAD_SERVICE_PROTOCOL_NOT_JOIN_PARTY_ROOM%(account, ag)
                    redis.lpush(FORMAT_SERVICE_PROTOCOL_TABLE%(gameId, serviceTag), message)
                except:
                    print '[account wantServer][%s]'%(redis.get('account:%s:wantServer'%account))
                redis.lrem(key, account)
        if serverIp:
            urlRes = urlparse(request.url)
            domain = urlRes.netloc.split(':')[0]
            gameInfo = {'ip':domain, 'port':int(serverPort), 'gameid':gameid}

            gameState = {}
            gameTable = GAME_TABLE%(gameid)
            if redis.exists(gameTable):
                name, webTag, version,packName = redis.hmget(gameTable, ('name', 'web_tag', 'version','pack_name'))
                gameState[gameid] = {
                    'id'                :           gameid,
                    'name'              :           name,
                    'web_tag'           :           webTag,
                    'version'           :           version,
                    'downloadUrl'       :           packName
                }

            if joinNum:
                redis.srem(FORMAT_LOGIN_POOL_SET,_account)
                return {'code':0, 'sid':sid, 'userInfo':userInfo,\
                    'gameInfo':gameInfo, 'joinResult':joinResult, 'gameState':gameState}
            redis.srem(FORMAT_LOGIN_POOL_SET,_account)
            return {'code':0, 'sid':sid, 'userInfo':userInfo, 'gameInfo':gameInfo, 'gameState':gameState}
        else:
            if joinNum:
                redis.srem(FORMAT_LOGIN_POOL_SET,_account)
                return {'code':0, 'sid':sid, 'userInfo':userInfo, 'joinResult':joinResult, 'loginMsg':loginMsg}
            redis.srem(FORMAT_LOGIN_POOL_SET,account)
            return {'code':0, 'sid':sid, 'userInfo':userInfo, 'loginMsg':loginMsg}
    else: #失败
        redis.srem(FORMAT_LOGIN_POOL_SET,_account)
        return {'code':101, 'msg':'账号或密码错误或者微信授权失败'}

@fish_app.post('/refresh')
@allow_cross
def do_refresh(redis,session):
    """
    Refresh接口
    """
    ip = web_util.get_ip()
    curTime = datetime.now()
    fields = ('sid',)
    for field in fields:
        exec(FORMAT_PARAMS_POST_STR%(field,field))

    try:
        log_util.debug('[try do_refresh] get params sid[%s]'%(sid))
    except:
        return {'code':-300,'msg':'接口参数请求失败'}

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/refresh/',SessionTable,account,sid,verfiySid)
    log_util.debug('[try do_refresh] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    #refresh session
    do_sessionExpire(redis,session,SessionTable,SESSION_TTL)
    #获取用户信息
    head_url, gender, isVolntExitGroup,coin,exchange_ticket = redis.hmget(user_table,USER_INFO)
    log_util.debug('[try do_refresh] userId[%s] gender[%s] coin[%s]'%(uid,gender,coin))
    #group_table = AGENT_TABLE%(groupId)
    #isTrail = redis.hget(group_table,'isTrail')
    #isTrail = convert_util.to_int(isTrail)
    exchange_ticket = convert_util.to_int(exchange_ticket)

    #hasBroad = False
    # if redis.exists(FORMAT_BROADCAST_LIST_TABLE):
    #     #有广播内容
    #     hasBroad = True

    #判断是否能领取奖励
    if redis.sismember(FISH_SHARE_NOT_TAKE_SETS,uid):
        is_take_reward = 1
    elif redis.sismember(FISH_SHARE_TAKE_SETS,uid):
        is_take_reward = 2
    else: #未分享
        is_take_reward = 0

    share_coin,exchange_shop,hall_shop,shop_version,exchange_shop_ver = \
                    redis.hmget(FISH_CONSTS_CONFIG,('share_coin','exchange_shop','hall_shop','shop_version','exchange_shop_ver'))

    userInfo = {  #用户数据
            'id'                :       uid,
            'ip'                :       ip,
            'picUrl'            :       head_url,
            'exchangeTicket'    :       exchange_ticket,                         #兑换券
            'isTakeReward'      :       is_take_reward,                          # 0-为分享 1-未领取 2-已领取
            'shareCoin'         :       convert_util.to_int(share_coin),             #分享赠送金币金额
            'gender'            :       gender,
            'isTrail'           :       0,
            'shop'              :       convert_util.to_int(hall_shop),             #大厅商城是否开放
            'exchangeShop'      :       convert_util.to_int(exchange_shop),         #兑换商城是否开放
            'coin'              :       convert_util.to_int(coin)
    }

    lobbyInfo = get_fish_hall_setting(redis)
    #获取roomInfo
    roomInfo  = get_room_list(redis,False,False)
    lobbyInfo['hotUpdateURL'] = lobbyInfo['hotUpdateURL']+"/"+lobbyInfo['packName']
    log_util.info('[try do_refresh] roomInfo[%s] userInfo[%s] lobbyInfo[%s]'%(roomInfo,userInfo,lobbyInfo))
    return {
                'code':0,
                'lobbyInfo':lobbyInfo,
                'hasBroad':False,
                'shopVerison':convert_util.to_int(shop_version),
                'exchangeShopVersion':convert_util.to_int(exchange_shop_ver),
                'roomInfo':roomInfo,
                'userInfo':userInfo
     }

@fish_app.post('/getShopInfo')
@allow_cross
def get_fish_goods_info(redis,session):
    '''
    捕鱼获取商城商品接口
    '''
    fields = ('sid',)
    for field in fields:
        exec(FORMAT_PARAMS_POST_STR%(field,field))

    try:
        log_util.debug('[try get_fish_goods_info] get params sid[%s]'%(sid))
    except:
        return {'code':-300,'msg':'接口参数请求错误'}

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/getShopInfo/',SessionTable,account,sid,verfiySid)

    log_util.debug('[try do_refresh] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    goods_info = get_coin_goods_list(redis)
    log_util.debug('[try get_fish_goods_info]  sid[%s] goodsInfo[%s]'%(sid,goods_info))
    return {'code':0,'goodsInfo':goods_info}

@fish_app.post('/onGetShareReward')
@allow_cross
def get_fish_share_reward(redis,session):
    """
    金币分享获取金币接口
      分享游戏成功后回调获取分享金币
    """
    fields = ('sid',)
    for field in fields:
        exec(FORMAT_PARAMS_POST_STR%(field,field))

    try:
        log_util.debug('[try get_fish_share_reward] get params sid[%s]'%(sid))
    except:
        return {'code':-300,'msg':'接口请求参数错误'}

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/getRewardInfo/',SessionTable,account,sid,verfiySid)
    log_util.debug('[try do_refresh] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    has_share_users = uid in redis.smembers(FISH_FIRST_SHARE_PER_DAY_SET)
    is_ready_share    = uid in redis.smembers(FISH_SHARE_NOT_TAKE_SETS)
    is_take_share    = uid in redis.smembers(FISH_SHARE_TAKE_SETS)

    # if not has_share_users:
    #     return {'code':-3000,'msg':'你今天还未分享过游戏,赶快去分享吧!'}
    #
    if is_take_share:
        return {'code':-3002,'msg':'你今天已经领取过奖励!'}

    share_coin = redis.hget(FISH_CONSTS_CONFIG,'share_coin')
    if not share_coin:
        return {'code':-3001,'msg':'error in get share_coin,try again.'}
    pipe = redis.pipeline()
    try:
        pipe.srem(FISH_SHARE_NOT_TAKE_SETS,uid)
        pipe.sadd(FISH_SHARE_TAKE_SETS,uid)
        pipe.hincrby(user_table,'coin',share_coin)
    except:
        return {'code':-3003,'msg':'数据错误'}

    pipe.execute()
    coin = convert_util.to_int(redis.hget(user_table,'coin'))
    log_util.debug('[try get_fish_share_reward] sid[%s] get shareCoin[%s] after user coin[%s]'%(sid,share_coin,coin))
    return {'code':0,'coin':coin}

@fish_app.post('/onShareCallback')
@allow_cross
def on_shareCallback(redis,session):
    """
    用户分享回调接口
    :params  sid 用户sid
    :return code 0 成功  -1<均视为失败
    """
    fields = ('sid',)
    for field in fields:
        exec(FORMAT_PARAMS_POST_STR%(field,field))

    try:
        log_util.debug('[try on_shareCallback] get params sid[%s]'%(sid))
    except:
        return {'code':-300,'msg':'接口请求参数错误'}

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/onShareCallback',SessionTable,account,sid,verfiySid)
    log_util.debug('[try do_refresh] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    if uid in redis.smembers(FISH_FIRST_SHARE_PER_DAY_SET):
        return {'code':-4001,'msg':'uid[%s] already share.'%(uid)}

    pipe = redis.pipeline()
    try:
        pipe.sadd(FISH_FIRST_SHARE_PER_DAY_SET,uid)
        pipe.sadd(FISH_SHARE_NOT_TAKE_SETS,uid)
        pipe.incr(FISH_SHARE_TOTAL,1)
    except:
        log_util.error('[try on_shareCallback] add to set error. sid[%s] reason[%s]'%(sid,e))
        return {'code':-4000,'msg':'data error. retry please!'}

    pipe.execute()
    return {'code':0}

@fish_app.get('/getHallVersion')
@allow_cross
def getHallVersion(redis,session):
    """
    获取捕鱼更新包接口
    """
    HALL2VERS = get_fish_hall_setting(redis)
    HALL2VERS['hotUpdateURL'] = HALL2VERS['hotUpdateURL']+"/"+HALL2VERS['packName']
    return HALL2VERS

@fish_app.get('/extendSession')
@allow_cross
def do_extendSession(redis,session):
    """
    游戏中延长session有效时间接口
    """
    ip = web_util.get_ip()
    api_path = request.path
    log_util.debug('user ip[%s] remote_ip[%s] path[%s]'%(ip,request['REMOTE_ADDR'],request.path))
    sid = request.GET.get('sid','').strip()

    SessionTable = FORMAT_USER_HALL_SESSION%(sid)
    if not redis.exists(SessionTable):
        return {'code':1}

    extendSession(redis,session,SessionTable)
    return {'code':0}

@fish_app.post('/joinRoom')
@allow_cross
def do_joinRoom(redis,session):
    """
    加入房间接口
    """
    fields = ('sid','gameid')
    for field in fields:
        exec('%s = request.forms.get("%s",'').strip()'%(field,field))

    try:
        log_util.debug('[try do_joinRoom] get params sid[%s] gameid[%s]'%(sid,gameid))
        gameId = int(gameid)
    except:
        return {'code':-300,'msg':'接口参数错误'}

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/getRewardInfo/',SessionTable,account,sid,verfiySid)
    log_util.debug('[try do_refresh] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    ag = redis.hget(user_table, 'parentAg')
    adminTable = AGENT_TABLE%(ag)
    agValid = redis.hget(adminTable,'valid')
    # if agValid != '1':
        # print  '[CraeteRoom][info] agentId[%s] has freezed. valid[%s] '%(ag,agValid)
        # return {'code':-7,'msg':'该公会已被冻结,不能创建或加入该公会的房间'}

    countPlayerLimit = 0
    gameTable = GAME_TABLE%(gameId)
    maxRoomCount = redis.hget(gameTable,'maxRoomCount')
    if not maxRoomCount:
        maxRoomCount = 0
    maxPlayerCount = redis.hget(FISH_ROOM_TABLE%(gameId), 'max_player_count')
    if maxRoomCount and maxPlayerCount:
        countPlayerLimit = int(maxRoomCount) * maxPlayerCount

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
        if countPlayerLimit and (playerCount >= countPlayerLimit or roomCount >= maxRoomCount):
            continue
        _, _, _, currency, ipData, portData = serverTable.split(':')
        reservedServers.append((currency, ipData, portData))

    if reservedServers:
        currency, serverIp, serverPort = reservedServers[0]
        # ruleText = getRuleText(rule, gameId, redis)
        # if isOther:
            # params = eval(rule)
            # params.append(int(hidden))
            # rule = str(params)
            # protocolStr = HEAD_SERVICE_PROTOCOL_CREATE_OTHER_ROOM%(account, ag, rule, ruleText)
            # redis.rpush(FORMAT_SERVICE_PROTOCOL_TABLE%(gameId, '%s:%s:%s'%(currency, serverIp, serverPort)), protocolStr)
            # return {'code':0, 'msg':'房间开启成功', 'ip':'', 'port':''}

        # redis.hmset(SessionTable,
            # {
                # 'action'   :   1,
                # 'rule'     :   rule,
                # 'ruleText' :   ruleText,
                # 'hidden'   :   hidden,
            # }
        # )
        urlRes = urlparse(request.url)
        domain = urlRes.netloc.split(':')[0]
        return {'code' : 0, 'ip' : domain, 'port' : serverPort}
    else:
        return {'code':-1, 'msg':'服务器忙碌或维护中'}

@fish_app.post('/getRank')
@allow_cross
def do_getRank(redis,session):
    """
    加入房间接口
    """
    fields = ('sid',)
    for field in fields:
        exec('%s = request.forms.get("%s",'').strip()'%(field,field))

    try:
        log_util.debug('[try do_getRank] get params sid[%s]'%(sid))
    except:
        return {'code':-300,'msg':'接口参数错误'}

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/getRank/',SessionTable,account,sid,verfiySid)
    log_util.debug('[try do_refresh] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    today = date.today()
    yesterday = today - timedelta(days=1)
    rankInfo = {'rankForCoin':[], 'rankForProfit':[]}

    #获取盈利排行
    lastRank = RANK_COUNT-1
    lastPlayers = redis.zrevrange(TMP_FORMAT_USER_COINDELTA_TABLE, lastRank, lastRank, True, int)
    if lastPlayers:
        lastPlayers = redis.zrevrangebyscore(TMP_FORMAT_USER_COINDELTA_TABLE, lastPlayers[0][1], lastPlayers[0][1], score_cast_func = int)
        lastRank = redis.zrevrank(TMP_FORMAT_USER_COINDELTA_TABLE, lastPlayers[0]) + len(lastPlayers) - 1
    players = redis.zrevrange(TMP_FORMAT_USER_COINDELTA_TABLE, 0, lastRank, True, int)
    #更低排名玩家的还存不存在，不存在则屏蔽盈利0分玩家
    zeroPlayers = redis.zrevrangebyscore(TMP_FORMAT_USER_COINDELTA_TABLE, 0, 0, score_cast_func = int)
    if zeroPlayers:
        less0Rank = redis.zrevrank(TMP_FORMAT_USER_COINDELTA_TABLE, zeroPlayers[-1])
        less0RankPlayers = redis.zrevrange(TMP_FORMAT_USER_COINDELTA_TABLE, less0Rank+1, less0Rank+1, False, int)
    else:
        less0RankPlayers = None
    rank = prevRank = 1
    sameCount = 0
    prevCoinDelta = players[0][1] if players else 0
    selfRank = 0
    selfTicketDelta = 0
    for player in players:
        if player[1] >= prevCoinDelta:
            rank = prevRank
            sameCount += 1
        else:
            rank = prevRank + sameCount
            sameCount = 1
        prevRank = rank
        prevCoinDelta = player[1]
        playerAccount = player[0]
        if prevCoinDelta <= 0:
            continue
        playerTable = redis.get(FORMAT_ACCOUNT2USER_TABLE%(playerAccount))
        nickname, headImgUrl = redis.hmget(playerTable, ('nickname', 'headImgUrl'))
        if playerAccount == account:
            selfRank = rank
            selfTicketDelta = player[1]
            pbAppendRank(rankInfo['rankForProfit'], rank, nickname, headImgUrl, player[1])
        else:
            if player[1] or less0RankPlayers:
                pbAppendRank(rankInfo['rankForProfit'], rank, nickname, headImgUrl, player[1])
    if not selfRank:
        selfTicketDelta = redis.zscore(TMP_FORMAT_USER_COINDELTA_TABLE, account)
        if not selfTicketDelta:
            selfRank = NOT_RANK_USE_NUM
            selfTicketDelta = 0
        else:
            selfTicketDelta = int(selfTicketDelta)
            selfRankPlayers = redis.zrevrangebyscore(TMP_FORMAT_USER_COINDELTA_TABLE, selfTicketDelta, selfTicketDelta, score_cast_func = int)
            if selfRankPlayers:
                selfRank = redis.zrevrank(TMP_FORMAT_USER_COINDELTA_TABLE, selfRankPlayers[0]) + 1
            else:
                selfRank = rank + 1
    if selfRank > MY_MAX_RANK:
        selfRank = NOT_RANK_USE_NUM
    nickname, headImgUrl = redis.hmget(user_table, ('nickname', 'headImgUrl'))
    pbAppendRank(rankInfo['rankForProfit'], selfRank, nickname, headImgUrl, selfTicketDelta)

    #获取金币排行
    lastRank = RANK_COUNT-1
    lastPlayers = redis.zrevrange(FORMAT_USER_COIN_TABLE%(yesterday), lastRank, lastRank, True, int)
    if lastPlayers:
        lastPlayers = redis.zrevrangebyscore(FORMAT_USER_COIN_TABLE%(yesterday), lastPlayers[0][1], lastPlayers[0][1], score_cast_func = int)
        lastRank = redis.zrevrank(FORMAT_USER_COIN_TABLE%(yesterday), lastPlayers[0]) + len(lastPlayers) - 1
    players = redis.zrevrange(FORMAT_USER_COIN_TABLE%(yesterday), 0, lastRank, True, int)
    #更低排名玩家的还存不存在，不存在则屏蔽盈利0分玩家
    zeroPlayers = redis.zrevrangebyscore(FORMAT_USER_COIN_TABLE%(yesterday), 0, 0, score_cast_func = int)
    if zeroPlayers:
        less0Rank = redis.zrevrank(FORMAT_USER_COIN_TABLE%(yesterday), zeroPlayers[-1])
        less0RankPlayers = redis.zrevrange(FORMAT_USER_COIN_TABLE%(yesterday), less0Rank+1, less0Rank+1, False, int)
    else:
        less0RankPlayers = None
    rank = prevRank = 1
    sameCount = 0
    prevCoinDelta = players[0][1] if players else 0
    selfRank = 0
    selfTicketDelta = 0
    for player in players:
        if player[1] >= prevCoinDelta:
            rank = prevRank
            sameCount += 1
        else:
            rank = prevRank + sameCount
            sameCount = 1
        prevRank = rank
        prevCoinDelta = player[1]
        playerAccount = player[0]
        playerTable = redis.get(FORMAT_ACCOUNT2USER_TABLE%(playerAccount))
        nickname, headImgUrl = redis.hmget(playerTable, ('nickname', 'headImgUrl'))
        if playerAccount == account:
            selfRank = rank
            selfTicketDelta = player[1]
            pbAppendRank(rankInfo['rankForCoin'], rank, nickname, headImgUrl, player[1])
        else:
            if player[1] or less0RankPlayers:
                pbAppendRank(rankInfo['rankForCoin'], rank, nickname, headImgUrl, player[1])
    if not selfRank:
        selfTicketDelta = redis.zscore(FORMAT_USER_COIN_TABLE%(yesterday), account)
        if not selfTicketDelta:
            selfRank = NOT_RANK_USE_NUM
            selfTicketDelta = 0
        else:
            selfTicketDelta = int(selfTicketDelta)
            selfRankPlayers = redis.zrevrangebyscore(FORMAT_USER_COIN_TABLE%(yesterday), selfTicketDelta, selfTicketDelta, score_cast_func = int)
            if selfRankPlayers:
                selfRank = redis.zrevrank(FORMAT_USER_COIN_TABLE%(yesterday), selfRankPlayers[0]) + 1
            else:
                selfRank = rank + 1
    if selfRank > MY_MAX_RANK:
        selfRank = NOT_RANK_USE_NUM
    nickname, headImgUrl = redis.hmget(user_table, ('nickname', 'headImgUrl'))
    pbAppendRank(rankInfo['rankForCoin'], selfRank, nickname, headImgUrl, selfTicketDelta)

    return {'code' : 0, 'rankInfo' : rankInfo}
