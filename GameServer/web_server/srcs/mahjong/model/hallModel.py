#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    大厅Model
"""

from web_db_define import *
from datetime import datetime,timedelta
from wechat.wechatData import *
from admin  import access_module
from config.config import *
from datetime import datetime
from mahjong.model.agentModel import getTopAgentId
from common import log_util
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from hashlib import sha256
import hmac
import urllib
import json
import random
import time
import rsa
import base64
import mahjong_pb2
import poker_pb2
import replay4proto_pb2
import requests

def onReg(redis, account, passwd, type, ip): #传入参数：账号，密码，类型；返回参数：成功返回账号和密码，失败返回None, None

    curTime = datetime.now()

    #print
    log_util.debug('[try onReg] account[%s] passwd[%s] type[%s]'%(account,passwd,type))

    if type == 1: #微信code登录
        tokenMessage = checkWeixinCode(account)
        print '====================================='
        print 'account'
        print account
        print 'tokenMessage'
        print tokenMessage
        print '====================================='
        if tokenMessage:
            password = account
            accessToken = tokenMessage["access_token"]
            refreshToken = tokenMessage["refresh_token"]
            openID = tokenMessage["openid"]
            userData = getWeixinData(openID, accessToken)
            unionid = userData['unionid']
            if redis.exists(WEIXIN2ACCOUNT%(unionid)):
                realAccount = redis.get(WEIXIN2ACCOUNT%(unionid))
                account2user_table = FORMAT_ACCOUNT2USER_TABLE%(realAccount)
                table = redis.get(account2user_table)
                redis.hmset(table, {'accessToken':accessToken, 'refreshToken':refreshToken, 'password':md5.new(password).hexdigest()})
            else:
                setOpenid2account(openID, accessToken, refreshToken, ip, redis, account)
            redis.srem(FORMAT_LOGIN_POOL_SET,account)
            return unionid, password
        # 第二种appid
        else:
            tokenMessage = checkWeixinCode_2(account)
            if tokenMessage:
                password = account
                accessToken = tokenMessage["access_token"]
                refreshToken = tokenMessage["refresh_token"]
                openID = tokenMessage["openid"]
                userData = getWeixinData(openID, accessToken)
                print '---------------------------------'
                print '---------------------------------'
                print 'userData'
                print userData
                print '---------------------------------'
                print '---------------------------------'
                unionid = userData['unionid']
                if redis.exists(WEIXIN2ACCOUNT%(unionid)):
                    realAccount = redis.get(WEIXIN2ACCOUNT%(unionid))
                    account2user_table = FORMAT_ACCOUNT2USER_TABLE%(realAccount)
                    table = redis.get(account2user_table)
                    redis.hmset(table, {'accessToken':accessToken, 'refreshToken':refreshToken, 'password':md5.new(password).hexdigest()})
                else:
                    setOpenid2account(openID, accessToken, refreshToken, ip, redis, account)
                redis.srem(FORMAT_LOGIN_POOL_SET,account)
                return unionid, password

        redis.srem(FORMAT_LOGIN_POOL_SET,account)
    elif type == 2:
        if redis.exists(WEIXIN2ACCOUNT%(account)):
            realAccount = redis.get(WEIXIN2ACCOUNT%(account))
            account2user_table = FORMAT_ACCOUNT2USER_TABLE%(realAccount)
            table = redis.get(account2user_table)
            truePassword, openID, accessToken = redis.hmget(table, ('password', 'openid', 'accessToken'))
            log_util.debug('type 2:passwd[%s] md5[%s] truePassword[%s]'%(md5.new(passwd).hexdigest(), passwd, truePassword))
            if truePassword == md5.new(passwd).hexdigest():
                userData = getWeixinData(openID, accessToken)
                log_util.debug('onReg for type 2, userData:%s'%(userData))
                if userData:
                    redis.hmset(table,
                        {
                            'nickname'      :   userData['nickname'],
                            'sex'           :   userData['sex'],
                            'headImgUrl'    :   userData['headimgurl']
                        }
                    )
                redis.srem(FORMAT_LOGIN_POOL_SET,account)
                return account, passwd
        redis.srem(FORMAT_LOGIN_POOL_SET,account)
    elif type == 3: #微信WEBcode登录
        tokenMessage = checkWeixinCodeWEB(account)
        if tokenMessage:
            password = account
            accessToken = tokenMessage["access_token"]
            refreshToken = tokenMessage["refresh_token"]
            openID = tokenMessage["openid"]
            userData = getWeixinData(openID, accessToken)
            unionid = userData['unionid']
            if redis.exists(WEIXIN2ACCOUNT%(unionid)):
                realAccount = redis.get(WEIXIN2ACCOUNT%(unionid))
                account2user_table = FORMAT_ACCOUNT2USER_TABLE%(realAccount)
                table = redis.get(account2user_table)
                redis.hmset(table, {'accessToken':accessToken, 'refreshToken':refreshToken, 'password':md5.new(password).hexdigest()})
            else:
                setOpenid2account(openID, accessToken, refreshToken, ip, redis, account)
            redis.srem(FORMAT_LOGIN_POOL_SET,account)
            return unionid, password
        redis.srem(FORMAT_LOGIN_POOL_SET,account)
    elif type == 4: #微信WEBcode登录
        tokenMessage = checkWeixinCodeWEB(account)
        if tokenMessage:
            password = account
            accessToken = tokenMessage["access_token"]
            refreshToken = tokenMessage["refresh_token"]
            openID = tokenMessage["openid"]
            userData = getWeixinData(openID, accessToken)
            unionid = userData['unionid']
            if redis.exists(WEIXIN2ACCOUNT%(unionid)):
                realAccount = redis.get(WEIXIN2ACCOUNT%(unionid))
                account2user_table = FORMAT_ACCOUNT2USER_TABLE%(realAccount)
                table = redis.get(account2user_table)
                redis.hmset(table, {'accessToken':accessToken, 'refreshToken':refreshToken, 'password':md5.new(password).hexdigest()})
            else:
                setOpenid2account(openID, accessToken, refreshToken, ip, redis, account)
            redis.srem(FORMAT_LOGIN_POOL_SET,account)
            return unionid, password
        redis.srem(FORMAT_LOGIN_POOL_SET,account)
    elif type == 5: #微信小程序登录
        tokenMessage = checkWeixinCodeMINI(account)
        if tokenMessage:
            password = account
            accessToken = tokenMessage["access_token"]
            refreshToken = tokenMessage["refresh_token"]
            openID = tokenMessage["openid"]
            userData = getWeixinData(openID, accessToken)
            unionid = userData['unionid']
            if redis.exists(WEIXIN2ACCOUNT%(unionid)):
                realAccount = redis.get(WEIXIN2ACCOUNT%(unionid))
                account2user_table = FORMAT_ACCOUNT2USER_TABLE%(realAccount)
                table = redis.get(account2user_table)
                redis.hmset(table, {'accessToken':accessToken, 'refreshToken':refreshToken, 'password':md5.new(password).hexdigest()})
            else:
                setOpenid2account(openID, accessToken, refreshToken, ip, redis, account)
            redis.srem(FORMAT_LOGIN_POOL_SET,account)
            return unionid, password
    elif type == 0:
        account2user_table = FORMAT_ACCOUNT2USER_TABLE%(account)
        if redis.exists(account2user_table):
            table = redis.get(account2user_table)
            truePassword = redis.hget(table, 'password')
            if truePassword == md5.new(passwd).hexdigest():
                return account, passwd
    elif type == 6: # 手机号码
        account2user_phone_table = USERS_ACCOUNT_PHONE_TABLE % account
        if redis.exists(account2user_phone_table):
            phoneVcode_table = USERS_LOGIN_PHONE_VCODE_TABLE % account
            if redis.exists(phoneVcode_table):
                if passwd == redis.get(phoneVcode_table):
                    userTable = redis.get(account2user_phone_table)
                    account, passwd = redis.hmget(userTable, ('account', 'password'))
                    redis.sadd(FORMAT_LOGIN_POOL_SET, account)
                    return account, account

    redis.srem(FORMAT_LOGIN_POOL_SET,account)
    return None, None

def onRegFish(redis, account, passwd, type, ip): #传入参数：账号，密码，类型；返回参数：成功返回账号和密码，失败返回None, None

    curTime = datetime.now()

    #print
    log_util.debug('[try onReg] account[%s] passwd[%s] type[%s]'%(account,passwd,type))

    if type == 1: #微信code登录
        tokenMessage = checkWeixinCode4fish(account)
        if tokenMessage:
            password = account
            accessToken = tokenMessage["access_token"]
            refreshToken = tokenMessage["refresh_token"]
            openID = tokenMessage["openid"]
            userData = getWeixinData(openID, accessToken)
            unionid = userData['unionid']
            if redis.exists(WEIXIN2ACCOUNT4FISH%(unionid)):# or redis.exists(WEIXIN2ACCOUNT%(unionid)):
                realAccount = redis.get(WEIXIN2ACCOUNT4FISH%(unionid))
                if not realAccount:
                    realAccount = redis.get(WEIXIN2ACCOUNT%(unionid))
                account2user_table = FORMAT_ACCOUNT2USER_TABLE%(realAccount)
                table = redis.get(account2user_table)
                redis.hmset(table, {'accessToken':accessToken, 'refreshToken':refreshToken, 'password':md5.new(password).hexdigest()})
            else:
                setOpenid2account4fish(openID, accessToken, refreshToken, ip, redis, account)
            redis.srem(FORMAT_LOGIN_POOL_SET,account)
            return unionid, password
        redis.srem(FORMAT_LOGIN_POOL_SET,account)
    elif type == 2:
        if redis.exists(WEIXIN2ACCOUNT4FISH%(account)):#  or redis.exists(WEIXIN2ACCOUNT%(account)):
            realAccount = redis.get(WEIXIN2ACCOUNT4FISH%(account))
            if not realAccount:
                realAccount = redis.get(WEIXIN2ACCOUNT%(account))
            account2user_table = FORMAT_ACCOUNT2USER_TABLE%(realAccount)
            table = redis.get(account2user_table)
            truePassword, openID, accessToken = redis.hmget(table, ('password', 'openid', 'accessToken'))
            log_util.debug('type 2:passwd[%s] md5[%s] truePassword[%s]'%(md5.new(passwd).hexdigest(), passwd, truePassword))
            if truePassword == md5.new(passwd).hexdigest():
                userData = getWeixinData(openID, accessToken)
                log_util.debug('onReg for type 2, userData:%s'%(userData))
                if userData:
                    redis.hmset(table,
                        {
                            'nickname'      :   userData['nickname'],
                            'sex'           :   userData['sex'],
                            'headImgUrl'    :   userData['headimgurl']
                        }
                    )
                redis.srem(FORMAT_LOGIN_POOL_SET,account)
                return account, passwd
        redis.srem(FORMAT_LOGIN_POOL_SET,account)
    elif type == 3: #微信WEBcode登录
        tokenMessage = checkWeixinCodeWEB(account)
        if tokenMessage:
            password = account
            accessToken = tokenMessage["access_token"]
            refreshToken = tokenMessage["refresh_token"]
            openID = tokenMessage["openid"]
            userData = getWeixinData(openID, accessToken)
            unionid = userData['unionid']
            if redis.exists(WEIXIN2ACCOUNT4FISH%(unionid)):#  or redis.exists(WEIXIN2ACCOUNT%(unionid)):
                realAccount = redis.get(WEIXIN2ACCOUNT4FISH%(unionid))
                if not realAccount:
                    realAccount = redis.get(WEIXIN2ACCOUNT%(unionid))
                account2user_table = FORMAT_ACCOUNT2USER_TABLE%(realAccount)
                table = redis.get(account2user_table)
                redis.hmset(table, {'accessToken':accessToken, 'refreshToken':refreshToken, 'password':md5.new(password).hexdigest()})
            else:
                setOpenid2account4fish(openID, accessToken, refreshToken, ip, redis, account)
            redis.srem(FORMAT_LOGIN_POOL_SET,account)
            return unionid, password
        redis.srem(FORMAT_LOGIN_POOL_SET,account)
    elif type == 4: #微信WEBcode登录
        tokenMessage = checkWeixinCodeWEB(account)
        if tokenMessage:
            password = account
            accessToken = tokenMessage["access_token"]
            refreshToken = tokenMessage["refresh_token"]
            openID = tokenMessage["openid"]
            userData = getWeixinData(openID, accessToken)
            unionid = userData['unionid']
            if redis.exists(WEIXIN2ACCOUNT4FISH%(unionid)):#  or redis.exists(WEIXIN2ACCOUNT%(unionid)):
                realAccount = redis.get(WEIXIN2ACCOUNT4FISH%(unionid))
                if not realAccount:
                    realAccount = redis.get(WEIXIN2ACCOUNT%(unionid))
                account2user_table = FORMAT_ACCOUNT2USER_TABLE%(realAccount)
                table = redis.get(account2user_table)
                redis.hmset(table, {'accessToken':accessToken, 'refreshToken':refreshToken, 'password':md5.new(password).hexdigest()})
            else:
                setOpenid2account4fish(openID, accessToken, refreshToken, ip, redis, account)
            redis.srem(FORMAT_LOGIN_POOL_SET,account)
            return unionid, password
        redis.srem(FORMAT_LOGIN_POOL_SET,account)
    elif type == 0:
        account2user_table = FORMAT_ACCOUNT2USER_TABLE%(account)
        if redis.exists(account2user_table):
            table = redis.get(account2user_table)
            truePassword = redis.hget(table, 'password')
            if truePassword == md5.new(passwd).hexdigest():
                return account, passwd
    redis.srem(FORMAT_LOGIN_POOL_SET,account)
    return None, None

def saveHotUpDateSetting(redis,settingInfo,sys="HALL"):
    """
    保存热更新配置
    """
    if sys == 'HALL':
        hot_table = HOTUPDATE_TABLE
    else:
        hot_table = FISH_HOTUPDATE_TABLE

    return redis.hmset(hot_table,settingInfo)

def getHotSettingField(redis,field):
    """
    获取单个配置信息
    """
    return redis.hget(HOTUPDATE_TABLE,field)

def getHotSettingAll(redis):
    return redis.hgetall(HOTUPDATE_TABLE)

def get_fish_hall_setting(redis):
    return redis.hgetall(FISH_HOTUPDATE_TABLE)

def getUserByAccount(redis, account):
    """
    通过account获取玩家数据
    """
    account2user_table = FORMAT_ACCOUNT2USER_TABLE%(account)
    userTable = redis.get(account2user_table)
    return userTable

def do_sessionExpire(redis,session,SessionTable,SESSION_TTL):
    """
    刷新session
    """
    #refresh session
    redis.expire(session['session_key'],60*60)
    redis.expire(SessionTable,60*10)
    session.expire()

def check_session_verfiy(redis,api_name,SessionTable,account,sid,verfiySid):
    '''
    验证session是否合法
    return code,msg
    '''
    log_util.debug('[on refresh] account[%s] sid[%s]'%(account, sid))

    if verfiySid and sid != verfiySid:
        #session['member_account'],session['member_id'] = '',''
        return -4,'账号已在其他地方登录',False

    if not redis.exists(SessionTable):
        return -3,'sid 超时',False

    user_table = getUserByAccount(redis, account)
    if not redis.exists(user_table):
        return -5,'该用户不存在',False

    return 0,True,user_table

def packPrivaTeData4Game(chair, data, resp, proto):
    privateResp = proto()
    privateResp.ParseFromString(resp.privateData)
    for data in privateResp.data.gameInfo.roomInfo.playerList:
        if int(data.side) == int(chair):
            print 'replay side get,side:%s nickname:%s'%(data.side, data.nickname)
            privateResp.data.gameInfo.selfInfo.side = data.side
            privateResp.data.gameInfo.selfInfo.nickname = data.nickname
            privateResp.data.gameInfo.selfInfo.coin = data.coin
            privateResp.data.gameInfo.selfInfo.ip = data.ip
            privateResp.data.gameInfo.selfInfo.sex = data.sex
            privateResp.data.gameInfo.selfInfo.headImgUrl = data.headImgUrl
            privateResp.data.gameInfo.selfInfo.roomCards = 0
    resp.privateData = privateResp.SerializeToString()
    replayStr = resp.SerializeToString()
    return replayStr

def packPrivaTeData(chair, data):
    resp = replay4proto_pb2.ReplayData()
    resp.ParseFromString(data)
    refreshDataNameProtos = [mahjong_pb2.S_C_RefreshData, poker_pb2.S_C_RefreshData]
    for proto in refreshDataNameProtos:
        try:
            replayStr = packPrivaTeData4Game(chair, data, resp, proto)
            break
        except Exception as e:
            print 'packPrivaTeData error', e
    return replayStr

def getRuleText(rule, gameId, redis):
    ruleList = eval(rule)
    ruleText = '底分: %s\n'%(max(int(ruleList[-1]), 1))
    gameTable = GAME_TABLE%(gameId)

    for data in redis.lrange(USE_ROOM_CARDS_RULE%(gameId), 0, -1):
        datas = data.split(':')
        name, cards = datas[0], datas[1]
        try:
            playCount = int(datas[2])
        except:
            playCount = name
        if int(cards) == ruleList[-2]:
            ruleText += '局数: %s\n'%(playCount)

    num = 0
    for ruleNum in redis.lrange(GAME2RULE%(gameId), 0, -1):
        ruleTile, ruleType, rule = redis.hmget(GAME2RULE_DATA%(gameId, ruleNum), ('title', 'type', 'rule'))
        ruleDataList = rule.split(',')
        if int(ruleType) == 1:
            print '[on getRuleText]get ruleList[%s] num[%s]'%(ruleList, num)
            try:
                ruleText += '%s: %s\n'%(ruleTile, ruleDataList[int(ruleList[num])])
            except:
                ruleText += '%s: %s\n'%(ruleTile, ruleDataList[int(ruleList[num][0])])
        else:
            text = '%s: '%(ruleTile)
            textList = []
            for ruleData in ruleList[num]:
                textList.append(ruleDataList[ruleData])
            textData = ','.join(textList)
            text += textData
            ruleText =ruleText + text + '\n'
        num += 1
    ruleText = ruleText.decode('utf-8')
    return ruleText

def tryExitGroup(redis, userTable, account, id, groupId):
    pipe = redis.pipeline()
    key = redis.get(ACCOUNT2WAIT_JOIN_PARTY_TABLE%account)
    # for key in redis.keys(WAIT_JOIN_PARTY_ROOM_PLAYERS%('*', '*', '*')): #在等待匹配娱乐模式的话则离开列表
    if key:
        waitJoinList = redis.lrange(key, 0, -1)
        if account in waitJoinList:
            pipe.lrem(key, account)
    pipe.srem(FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE%(groupId), id) #上线代理需要获得
    pipe.hmset(userTable, {'parentAg':'000000', 'isVolntExitGroup':1,'lastGroup':groupId})
    #记录到省级公会的钻石
    topAgId = getTopAgentId(redis,groupId)
    roomcard = redis.get(USER4AGENT_CARD%(groupId,id))
    if not roomcard:
        roomcard = 0
    print '[try exitGroup] topAgId[%s] roomCards[%s]'%(topAgId,roomcard)
    pipe.set(USER4AGENT_CARD%(topAgId,id),int(roomcard))
    pipe.execute()

def getGroupIds(redis,groupId):
    """
    获取所有上级代理ID
    """
    Ids = []
    if redis.exists(AGENT_TABLE%(groupId)):
        parentId = redis.get(AGENT2PARENT%(groupId))
        if parentId:
            if int(parentId) == 1:
                return ['1']
            Ids.extend(getGroupIds(redis,parentId))
        else:
            Ids.append(parentId)

    return Ids

def getBroadcasts(redis,groupId,isNew=''):
    """
    获取广播列表
    """
    bIds = redis.lrange(HALL_BROADCAST_LIST,0,-1)
    broadInfos = []
    groupIds = getGroupIds(redis,groupId)
    groupIds.append(groupId)
    log_util.debug('[groupIds][%s] bids[%s]'%(groupIds,bIds))
    for bid in bIds:
        if redis.exists(FORMAT_BROADCAST_TABLE%(bid)):
            bInfos = redis.hgetall(FORMAT_BROADCAST_TABLE%(bid))
            if bInfos['ag'] in groupIds:
                broadInfos.append(bInfos)
        else:
            redis.lrem(FORMAT_BROADCAST_LIST_TABLE,'1',bid)

    broadcasts = {'broadcasts':broadInfos}

    if isNew:
        broadcasts['isNew'] = isNew

    return broadcasts

def getHallBroadInfo(redis,group_id,broad_table,broad_belone):
    """
    获取大厅广播列表
    """
    from bag.bag_func import put_marquee_into_broad,check_marquee_have
    marquee_have = check_marquee_have()
    m = int(str(datetime.strftime(datetime.now(),'%M')))
    broad_list = []
    #if  m % 3 == 0 or not marquee_have:
    play_set = redis.smembers(HALL_BRO_PLAY_SET)
    broads = redis.lrange(broad_table % (1), 0, -1)
    for broad in broads:
        if broad in play_set:
            broadDetail = {}
            broadInfo = redis.hgetall(HALL_BRO_TABLE % (broad))
            broadDetail['content'] = broadInfo['content']
            broadDetail['repeatInterval'] = int(broadInfo['per_sec'])
            broad_list.append(broadDetail)

    broads = redis.lrange(broad_table % (0), 0, -1)
    for broad in broads:
        if broad in play_set:
            broadDetail = {}
            broadInfo = redis.hgetall(HALL_BRO_TABLE % (broad))
            broadDetail['content'] = broadInfo['content']
            broadDetail['repeatInterval'] = int(broadInfo['per_sec'])
            broad_list.append(broadDetail)

    if broad_belone == 'HALL':
        broads = redis.lrange(HALL_BRO_CONTAIN_AG_LIST % (2, group_id), 0, -1)
        for broad in broads:
            if broad in play_set:
                broadDetail = {}
                broadInfo = redis.hgetall(HALL_BRO_TABLE % (broad))
                broadDetail['content'] = broadInfo['content']
                broadDetail['repeatInterval'] = int(broadInfo['per_sec'])
                broad_list.append(broadDetail)

        broads = redis.lrange(HALL_BRO_CONTAIN_AG_LIST % (3, group_id), 0, -1)
        for broad in broads:
            if broad in play_set:
                broadDetail = {}
                broadInfo = redis.hgetall(HALL_BRO_TABLE % (broad))
                broadDetail['content'] = broadInfo['content']
                broadDetail['repeatInterval'] = int(broadInfo['per_sec'])
                broad_list.append(broadDetail)

    broad_list = put_marquee_into_broad(broad_list)

    return broad_list

def extendSession(redis,session,SessionTable):
    """
    延长session有效时间
    """
    redis.expire(session['session_key'],60*60)
    redis.expire(SessionTable,60*40)

def getPhoneVcode(redis, session, mobile, msg=''):
    """
    获取短信验证码
    """
    vcode = random.randint(000000, 999999) # 验证码随机六位数
    smsid = ''
    try:
        tpl_value = JUHE_TPL_VALUE % vcode  # 短信模板变量,根据实际情况修改
        params = JUHE_PARAMS % (JUHE_APPKEY, mobile, JUHE_TPL_ID, urllib.quote(tpl_value))  # 组合参数
        wp = urllib.urlopen(JUHE_TPL_SEND_URL + "?" + params)
        content = wp.read()  # 获取接口返回内容
        result = json.loads(content)
        if result:
            error_code = result['error_code']
            if error_code == 0:
                # 发送成功
                smsid = vcode
                print "[vcode: %s] mobile[%s] vcode request sendsms success, smsid[%s]" % (msg, mobile, result['result']['sid'])
                log_util.debug('[vcode: %s] mobile[%s] vcode is vsuccess]' % (msg, mobile))
            else:
                print "[vcode: %s] mobile[%s] vcode request sendsms error, code[%s] reason[%s]" % (msg, mobile, error_code, result['reason'])
                log_util.debug('[vcode: %s] mobile[%s] is verification code acquisition failure]' % (msg, mobile))
        else:
            # 请求失败
            print("[vcode: %s] mobile[%s] vcode request sendsms faild" % (msg, mobile))
            log_util.debug('[vcode: %s] mobile[%s] vcode is verification code acquisition failure]' % (msg, mobile))
    except Exception as err:
        log_util.debug('[vcode: %s] mobile[%s] vcode is verification code acquisition failure]' % (msg, mobile))
    return smsid

def get_ordered_data(data):
    """
    获取URL参数值, 进行排序
    """
    complex_keys = []
    for key, value in data.items():
        if isinstance(value, dict):
            complex_keys.append(key)
    for key in complex_keys:
        data[key] = json.dumps(data[key], separators=(',', ':'))
    return sorted([(k, v) for k, v in data.items()])

def get_args_join(data):
    """
    将URL参数值进行拼接
    """
    return "&".join("{0}={1}".format(k, v) for k, v in data)

def get_sign(unsigned_string):
    """
    支付宝计算签名
    """
    private_key = ALIPAY_APPLICATION_PRIVATE_KEY
    rsaKey = RSA.importKey(base64.b64decode(private_key))
    signer = PKCS1_v1_5 .new(rsaKey)
    digest = SHA256.new()
    digest.update(unsigned_string.encode('utf8'))
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)
    return signature

def checkAlipaySign(params):
    """
    支付宝回调验签
    """
    sign = params['sign']
    if params.has_key('sign'):
        params.pop('sign')
    if params.has_key('sign_type'):
        params.pop('sign_type')
    public_key = "-----BEGIN PUBLIC KEY-----\n%s\n-----END PUBLIC KEY-----" % ALIPAY_PUBLIC_KEY
    sign = base64.b64decode(sign)
    orderData = get_ordered_data(params)
    unsigned_string = get_args_join(orderData)
    try:
        status = rsa.verify(unsigned_string, sign, rsa.PublicKey.load_pkcs1_openssl_pem(public_key))
    except Exception as err:
        return False
    return True

def alipay_VerfiyRcvDatas(redis, params):
    """
    支付宝校验支付数据， 成功（回调）后进行订单完成操作
    """
    curTime = datetime.now()
    orderTable = ORDER_TABLE % (params['out_trade_no'])
    if not redis.exists(orderTable):
        log_util.debug('[%s][alipay][error] orderNo[%s] is not exists.' % (curTime, params['out_trade_no']))
        return False

    endTime = params['gmt_payment']
    endTime = time.mktime(time.strptime(endTime, "%Y-%m-%d %H:%M:%S"))
    updateInfo = {
        'money': float(params['total_amount']) * 100,
        'endTime': endTime,
        'currency': 'CNY',
        'orderNum': params['out_trade_no'],
        'type': 'successful',
    }

    pipe = redis.pipeline()
    try:
        log_util.debug('[%s][alipay][info] update orderInfo[%s] success.'  % (curTime, updateInfo))
        pipe.hmset(orderTable, updateInfo)
        pipe.srem(PENDING_ORDER, orderTable)
        pipe.sadd(SUCCEED_ORDER, orderTable)
        pipe.persist(orderTable)
    except Exception as err:
        log_util.debug('[%s][alipay][error] update orderInfo[%s] error.' % (curTime, updateInfo))
        return False
    pipe.execute()
    return True

def get_shopmail_resultData(url, args, shapmail='cocogc'):
    """
    获取商城接口数据
    """
    curTime = datetime.now()
    headers = {'Content-type': 'application/json'}
    orderData = get_ordered_data(args)
    message = get_args_join(orderData)
    if shapmail == 'cocogc':
        message += '&secretKey=%s' % COCOGC_PRIVATE_KEY
        sign = hmac.new(bytes(COCOGC_PRIVATE_KEY.encode('utf-8')), bytes(message.encode('utf-8')),
                        digestmod=hashlib.sha256).hexdigest().upper()
    else:
        message += '&secret_key=%s' % CYGSE_PRIVATE_KEY
        sha256 = hashlib.sha256()
        sha256.update(message.encode())
        sign = sha256.hexdigest().upper()
    args['sign'] = sign
    data = json.dumps(args)
    try:
        res = requests.post(url=url, data=data, headers=headers, timeout=10)
        if res.status_code == 200:
            log_util.debug('[%s][on%s]Aapi]  url[%s] is request success.' % (curTime, shapmail, url))
            return res.json() if res.json() else False
        log_util.debug('[%s][on%s][Api]  url[%s] is request faild.' % (curTime, shapmail, url))
        return False
    except Exception as err:
        log_util.debug('[%s][on%s][Api]  url[%s] is request faild.' % (curTime, shapmail, url))
        return False

def get_cocogc_binduser(redis, uid, phone):
    """
    椰子用户绑定
    """
    curTime = datetime.now()
    userTable = FORMAT_USER_TABLE % (uid)
    args = {
        "merchantId": COCOGC_MERCHANTID,
        "uniqueUserId": uid,
        "reqTime": int(time.time()),
        "mobile": phone if phone else '',
    }
    resultData = get_shopmail_resultData(url=COCOGC_BINDUSER, args=args)
    if not resultData or resultData.get('resultCode') != 0:
        log_util.debug('[%s][onCocogc][binduser] uid[%s] is bind error.' % (curTime, uid))
        return False

    res = resultData.get('data')
    yyUid = res.get('userId')
    redis.hmset(userTable, {'yyUid': yyUid})
    log_util.debug('[%s][onCocogc][binduser] uid[%s] is bind success.' % (curTime, uid))
    return True


def get_cocogc_token(redis, uid, yyuid):
    """
    椰子用户登录
    """
    curTime = datetime.now()
    args = {
        "merchantId": COCOGC_MERCHANTID,
        "uniqueUserId": uid,
        "reqTime": int(time.time()),
        "yyUid": yyuid,
    }
    res = get_shopmail_resultData(url=COCOGC_GETTOKEN, args=args)
    if not res or res.get('resultCode') != 0:
        log_util.debug('[%s][onCocogc][gettoken] uid[%s] is token faild.' % (curTime, uid))
        return False
    log_util.debug('[%s][onCocogc][gettoken] uid[%s] is bind success.' % (curTime, uid))
    return res


def get_cocogc_getuserInfo(redis, uid):
    """
    椰子用户积分查询
    """
    curTime = datetime.now()
    args = {
        "merchantId": COCOGC_MERCHANTID,
        "uniqueUserId": uid,
        "reqTime": int(time.time()),
    }
    res = get_shopmail_resultData(url=COCOGC_GETUSERINFO, args=args)
    if not res or res.get('resultCode') != 0:
        log_util.debug('[%s][onUserInfo][userInfo] uid[%s] is faild.' % (curTime, uid))
        return False
    log_util.debug('[%s][onUserInfo][userInfo] uid[%s] is success.' % (curTime, uid))
    return res

def get_cocogc_pointIncome(redis, uid, pointNum):
    """
    椰子用户积分接口
    """
    curTime = datetime.now()
    args = {
        "tradeNo": int(time.time()),
        "merchantId": COCOGC_MERCHANTID,
        "pointNum": pointNum,
        "reqTime": int(time.time()),
        "uniqueUserId": uid,
    }
    res = get_shopmail_resultData(url=COCOGC_POINTINCOME, args=args)
    if not res or res.get('resultCode') != 0:
        log_util.debug('[%s][onCocogc][pointIncome] uid[%s] is exchange faild.' % (curTime, uid))
        return False
    return True

def get_cocogc_searchOrders(redis, uid, startTime, endTime, pageNumber, pageSize):
    """
    椰子用户积分明细查询接口
    """
    curTime = datetime.now()
    userTable = FORMAT_USER_TABLE % (uid)
    args = {
        "uniqueUserId": uid,
        "merchantId": COCOGC_MERCHANTID,
        "dateFrom": startTime,
        "dateTo": endTime,
        "pageIndex": pageNumber,
        "pageSize": pageSize,
        "reqTime": int(time.time()),
    }
    res = get_shopmail_resultData(url=COCOGC_SEARCHORDERS, args=args)
    if not res or res.get('resultCode') != 0:
        log_util.debug('[%s][onCocogc][searchOrders] uid[%s] is search faild.' % (curTime, uid))
        return False

    log_util.debug('[%s][onCocogc][searchOrders] uid[%s] is search success.' % (curTime, uid))
    return res

def get_cocogc_order(redis, session0):
    """
    获取椰云积分兑换订单号
    """
    curTime = datetime.now()
    orderIndex = redis.incr(COCOGC_ORDER_KEY)
    if orderIndex >= 10000000000:
        redis.set(COCOGC_ORDER_KEY, 0)
        orderIndex = redis.incr(COCOGC_ORDER_KEY)
    outTradeNo = curTime.strftime("%Y%m%d%H%M%S")
    outTradeNo += "001"
    outTradeNo += "%010d" % (int(orderIndex))
    for count in xrange(32 - len(outTradeNo)):
        outTradeNo += str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    return outTradeNo

def get_cygse_order(redis, session0):
    """
    获取创盈积分兑换订单号
    """
    curTime = datetime.now()
    orderIndex = redis.incr(CYGSE_ORDER_KEY)
    if orderIndex >= 10000000000:
        redis.set(CYGSE_ORDER_KEY, 0)
        orderIndex = redis.incr(CYGSE_ORDER_KEY)
    outTradeNo = curTime.strftime("%Y%m%d%H%M%S")
    outTradeNo += "002"
    outTradeNo += "%010d" % (int(orderIndex))
    for count in xrange(32 - len(outTradeNo)):
        outTradeNo += str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    return outTradeNo

def get_cygse_binduser(redis, uid, phone, nickname, headImgUrl):
    """
    创盈用户绑定
    """
    curTime = datetime.now()
    userTable = FORMAT_USER_TABLE % (uid)
    args = {
        "merchant_id": CYGSE_MERCHANTID,
        "user_id": uid,
        "nickname": nickname,
        "phone": phone if phone else '',
        "head_img_url": headImgUrl if headImgUrl else '',
    }
    resultData = get_shopmail_resultData(url=CYGSE_BINDUSER, args=args, shapmail='cygse')
    if not resultData or resultData.get('status') != 200:
        log_util.debug('[%s][onCygse][binduser] uid[%s] is bind error.' % (curTime, uid))
        return False
    res = resultData.get('data')
    cyUid = res.get('uid')
    redis.hmset(userTable, {'cyUid': cyUid})
    log_util.debug('[%s][onCygse][binduser] uid[%s] is bind success.' % (curTime, uid))
    return True

def get_cygse_token(redis, uid, cyUid):
    """
    创盈用户登录， 获取token
    """
    curTime = datetime.now()
    args = {
        "merchant_id": CYGSE_MERCHANTID,
        "user_id": uid,
        "uid": cyUid,
    }
    res = get_shopmail_resultData(url=CYGSE_GETTOKEN, args=args, shapmail='cygse')
    if not res or res.get('status') != 200:
        log_util.debug('[%s][onCygse][gettoken] uid[%s] is token faild.' % (curTime, uid))
        return False
    log_util.debug('[%s][onCygse][gettoken] uid[%s] is bind success.' % (curTime, uid))
    return res

def get_cygse_getuserInfo(redis, uid, cyUid):
    """
    创盈用户积分查询
    """
    curTime = datetime.now()
    args = {
        "merchant_id": CYGSE_MERCHANTID,
        "user_id": uid,
        "uid": cyUid,
    }
    res = get_shopmail_resultData(url=CYGSE_GETPOINT, args=args, shapmail='cygse')
    if not res or res.get('status') != 200:
        log_util.debug('[%s][onUserInfo][userInfo] uid[%s] is faild.' % (curTime, uid))
        return False
    log_util.debug('[%s][onUserInfo][userInfo] uid[%s] is success.' % (curTime, uid))
    return res

def get_cygse_pointIncome(redis, uid, coin_num, trade_no):
    """
    创盈用户积分接口
    """
    curTime = datetime.now()
    args = {
        "merchant_id": CYGSE_MERCHANTID,
        "user_id": uid,
        "trade_no": trade_no,
        "coin_num": str(coin_num),
        "req_time": str(time.time()),
    }
    res = get_shopmail_resultData(url=CYGSE_POINTINCOME, args=args, shapmail='cygse')
    if not res or res.get('status') != 200:
        log_util.debug('[%s][onCocogc][pointIncome] uid[%s] is exchange faild.' % (curTime, uid))
        return False
    return True