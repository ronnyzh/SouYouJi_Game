#!/usr/bin/env python
#-*-coding:utf-8 -*-

"""
@Author: $Author$
@Date: $Date$
@version: $Revision$

Description:
捕鱼支付接口模块
"""
from bottle import request,response,error,hook
from fish import fish_app
from wechat.wechatData import *
from web_db_define import *

#from config.config import *
from fish_config import consts
from datetime import datetime
from common import convert_util,web_util,json_util,wechat_util
from common.utilt import allow_cross,getInfoBySid
from model.hallModel import check_session_verfiy
from fish_util import fish_pay_func
from urlparse import urlparse
from hall.hall_func import *

@fish_app.post('/buyCoin')
@allow_cross
def do_buyCoin(redis,session):
    """
    测试购买金币接口
    :params sid  用户sid
    :params cards 购买金币数
    """
    fields = ('sid','cards','price','goodId')
    for field in fields:
        exec('%s = request.forms.get("%s","").strip()'%(field,field))

    try:
        log_util.debug('[try do_buyCoin] sid[%s] cardNums[%s] price[%s]'%(sid,cards,price))
        if not price:
            return {'code':-300,'msg':'接口参数请求错误'}
    except:
        return {'code':-300,'msg':'接口参数请求错误'}

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/buyCoin/',SessionTable,account,sid,verfiySid)

    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    _wechatHandler = fish_pay_func.test_WeChatPay(redis,goodId,user_table)
    if not _wechatHandler:
        return {'code':-6001,'msg':'购买金币失败'}

    #统计金币
    _handler = fish_pay_func.do_pay_record(redis,uid,user_table,cards,price)
    if not _handler:
        return {'code':-6000,'msg':'购买金币失败.'}

    coin = redis.hget(user_table,'coin')
    log_util.debug('[try buyCoin] return coin[%s]'%(coin))
    return {'code':0,'msg':'购买金币成功', 'coin':coin}

@fish_app.post('/notifyServer')
def do_paymentNotifyServer(redis):
    """
    微信支付
    """
    for k,v in request.forms.items():
        xml = k

    xml = xml.split('\n')
    xml = "".join(xml)

    curTime = datetime.now()
    log_util.debug('[%s][wechatPay][info] recive from %s'%(curTime,request.remote_addr))

    #解析xml参数
    params = transXml2Dict(xml)
    log_util.debug('[%s][wxPay][info] rcv params[%s].xml[%s]'%(curTime,params,xml))

    if not fish_pay_func.checkSign(params):
        #签名失败
        log_util.error('[%s][wechatPay][error] sign is not match.'%(curTime))
        return response2Wechat('FAIL','签名校验失败')

    if params['result_code'] != 'SUCCESS':
        log_util.error('[%s][wechatPay][error] result_code[%s] error'%(curTime,params['result_code']))
        return response2Wechat('FAIL','请求失败')

    if not fish_pay_func.verfiyRcvDatas(redis,params):
        log_util.error('[%s][wechatPay][error] data verfiy error.'%(curTime))
        return response2Wechat('FAIL','数据校验失败')

    #想会员增加金币
    fish_pay_func.do_add_fishcoin_2_members(redis,params['out_trade_no'])
    log_util.debug('[%s][wechatPay] payment success!'%(curTime))
    #返回消息给微信
    return response2Wechat('SUCCESS','支付成功')

@fish_app.post('/onAppleStorePay')
@allow_cross
def do_onAppleStorePay(redis, session):
    """
    发起苹果商店支付接口
    """
    curTime = datetime.now()
    orderSwitch = convert_util.to_int(redis.hget(FISH_CONSTS_CONFIG,'wechat_switch'))

    if not orderSwitch:
        return {'code':-1, 'msg':'暂未开放'}

    sid = request.forms.get('sid','').strip()
    databytes = request.forms.get('data','').strip()
    bundle_id = request.forms.get('bundle_id','').strip()
    Sanbox=True

    validator = AppStoreValidator(bundle_id,Sanbox) #确认支付

    try:
        purchases = validator.validate(databytes)

        productid = purchases[0].product_id
        transaction_id = purchases[0].transaction_id
        qty=purchases[0].quantity

        log_util.debug('applePay')
        SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)

        if verfiySid and sid != verfiySid:
            #session['member_account'],session['member_id'] = '',''
            return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
        if not redis.exists(SessionTable):
            return {'code':-3,'msg':'sid 超时'}

        userTable = getUserByAccount(redis, account)
        if not redis.exists(userTable):
            return {'code':-5,'msg':'该用户不存在'}
        groupId = redis.hget(userTable, 'parentAg')
        #会员ID
        id = userTable.split(':')[1]

        try:
            if not redis.exists(APP_PAY_ORDER_ITEM4FISH%(transaction_id)):
                if redis.exists(GOODS_TABLE4FISH%(bundle_id)):
                    cardNums = redis.hget(GOODS_TABLE4FISH%(bundle_id),'cards')
                    # roomCards = redis.incrby(USER4AGENT_CARD%(groupId, id),int(cardNums))
                    roomCards = redis.hincrby(userTable, 'coin', int(cardNums))
                    redis.set(APP_PAY_ORDER_ITEM4FISH%(transaction_id),productid)

                    # pipe = redis.pipeline()
                    # ymd = datetime.now().strftime("%Y-%m-%d")
                    # useDatas = [int(cardNums), 5, roomCards]
                    # useStr = ';'.join(map(str, useDatas))
                    # pipe.lpush(PLAYER_DAY_USE_CARD%(id, ymd), useStr)
                    # pipe.expire(PLAYER_DAY_USE_CARD%(id, ymd), SAVE_PLAYER_DAY_USE_CARD_TIME)
                    # pipe.execute()
            else:
                return {'code':-8,'msg':'交易ID[%s]已存在'%(transaction_id)}
        except:
            return {'code':-1,'msg':'购买失败'}

        # CardMoney = getCardMoney(redis,groupId)
        # countRateOfAgent(redis,groupId,int(cardNums),CardMoney)
        # roomCard = redis.get(USER4AGENT_CARD%(groupId, id))
        roomCard = redis.hget(userTable, 'coin')
        return {'code':0,'msg':'购买成功', 'roomCard':roomCard}

    except InAppValidationError as e:
        return {'code':-1, 'msg':'支付失败:%s'%(e)}

@fish_app.post('/onWeChatPay')
@allow_cross
def do_onWeChatPay(redis, session):
    """
    发起微信支付接口
    """
    curTime = datetime.now()

    orderSwitch = convert_util.to_int(redis.hget(FISH_CONSTS_CONFIG,'wechat_switch'))

    sid = request.forms.get('sid','').strip()
    goodsId   = request.forms.get('id','').strip()
    ip = web_util.get_ip()

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/checkOrder/',SessionTable,account,sid,verfiySid)
    log_util.debug('[try checkOrder] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    group_id  = redis.hget(user_table,'parentAg')

    # goodsId = redis.get(GOODS_NAME2NUM%(goodsName))
    goods_table = GOODS_TABLE%(goodsId)
    cards,goodsName,present_card, goodsPrice = redis.hmget(goods_table,('cards','name','present_cards', 'price'))
    #判断金币价格
    # goodsPrice = getGoodsMoney(redis,group_id,cards)
    if not redis.exists(goods_table):
        log_util.error('[try goods][error] goods[%s] is not found.'%(goodsName))
        return {'code':-1, 'msg':'goods not found'}


    log_util.debug('[try goods] player cards[%s] goodsPrice[%s].'%(cards,goodsPrice))

    goodsId2OrderId = GOODS_NUM4FISH%(goodsId)
    orderIndex = redis.incr(goodsId2OrderId)
    if orderIndex >= 10000000000:
        redis.set(goodsId2OrderId, 0)
        orderIndex = redis.incr(goodsId2OrderId)
    outTradeNo = getOutTradeNo(goodsId, orderIndex)

    # data = (player, goodsBody, totalPrice, outTradeNo, goodsCount, goodsId, goodsName, goodsCards)
    # order2weixin(data) *data
    urlRes = urlparse(request.url)
    serverIp = urlRes.netloc.split(':')[0]

    nonceStr = wechat_util.wechat_order_nonce()
    signDict = {
        'sub_appid'         :       APPID_FISH,
        'mch_id'            :       MCH_ID,
        'nonce_str'         :       nonceStr,
        'body'              :       goodsName,
        'out_trade_no'      :       outTradeNo,
        'total_fee'         :       int(float(goodsPrice) * 100),
        'spbill_create_ip'  :       ip,
        'notify_url'        :       NOTIFY_URL_FISH%(serverIp),
        'trade_type'        :       TRADE_TYPE
    }

    #print payment params
    log_util.debug('[%s][onWechatPay][info] payParams[%s]'%(curTime,signDict))

    # signList = packSignDict2List(signDict)
    # sign = getSign(signList)

    sign = gen_sign(signDict)

    orderStr = packSignDict2XML(signDict, sign)
    url = 'http://api.cmbxm.mbcloud.com/wechat/orders'
    resultDict = wechat_util.get_xml_message(url, orderStr)
    log_util.debug('wxPay url[%s] data[%s] sign[%s] signDict[%s]'%(url, orderStr, sign, signDict))
    log_util.debug('resultDict: %s'%resultDict)

    if not resultDict:
        log_util.error('[%s][onWechatPay][error] resultDict[%s]'%(curTime,resultDict))
        return {'code':-1, 'msg':'微信支付失败'}

    if resultDict['return_code'] != 'SUCCESS':
        try:
            log_util.error('[%s][onWechatPay][error] resultDict[%s]'%(curTime,resultDict['return_msg']))
        except:
            pass
        return {'code':-1, 'msg':'微信支付未开启'}

    prepayID = resultDict['prepay_id']
    package = 'Sign=WXPay'
    timeStamp = int(time.time())
    signList = [
        'appid=%s'%(APPID_FISH),
        'partnerid=%s'%(MCH_ID),
        'prepayid=%s'%(prepayID),
        'package=%s'%(package),
        'noncestr=%s'%(nonceStr),
        'timeStamp=%s'%(timeStamp),
    ]

    sign = getSign(signList)

    pipe = redis.pipeline()
    # pipe.set(PENDING4ACCOUNT%(player.account, totalPrice, goodsBody), outTradeNo)
    orderTable = ORDER_TABLE4FISH%(outTradeNo)
    pipe.hmset(orderTable,
        {
            'time'         :       timeStamp,
            'sign'         :       sign,
            'nonceStr'     :       nonceStr,
            'prepayID'     :       prepayID,
            'name'         :       goodsName,
            'body'         :       "123",
            'money'        :       int(float(goodsPrice) * 100),
            'startTime'    :       timeStamp,
            'account'      :       account,
            'num'          :       goodsId,
            'type'         :       'pending',
            'roomCards'    :       cards,
            'presentCards' :       present_card
        }
    )
    pipe.sadd(PENDING_ORDER4FISH, outTradeNo)
    pipe.lpush(ORDER_NUM_LIST4FISH, outTradeNo)
    pipe.sadd(PLAYER_ORDER4FISH%(account), outTradeNo)

    pipe.lpush(DAY_ORDER4FISH%(curTime.strftime("%Y-%m-%d")), outTradeNo)
    pipe.lpush(DAY_PENDING_ORDER4FISH%(curTime.strftime("%Y-%m-%d")), outTradeNo)
    pipe.expire(orderTable, 1 * 60 * 60)
    pipe.execute()

    #发送成功信息
    app_prepay_info = eval(resultDict['app_prepay_info'])
    data = {'partnerId':app_prepay_info['partnerid'],'prepayID':app_prepay_info['prepayid'], 'nonceStr':app_prepay_info['noncestr'],'sign':app_prepay_info['paySign'], 'outTradeNo':outTradeNo, 'curTime':curTime.strftime("%Y-%m-%d %H:%M:%S"), 'timeStamp':app_prepay_info['timestamp'], 'sub_appid':resultDict['sub_appid'], 'app_prepay_info':resultDict['app_prepay_info']}

    log_util.debug("[try order succeed] data %s"%data)
    log_util.debug("[try order succeed] account[%s] outTradeNo[%s]."%(account, outTradeNo))
    return {'code':0, 'data':data}

@fish_app.post('/onWeChatPay4TX')
@allow_cross
def do_onWeChatPay4TX(redis, session):
    """
    发起微信支付接口
    """
    curTime = datetime.now()
    orderSwitch = convert_util.to_int(redis.hget(FISH_CONSTS_CONFIG,'wechat_switch'))

    sid       = request.forms.get('sid','').strip()
    goodsId   = request.forms.get('id','').strip()
    ip        = web_util.get_ip()

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/checkOrder/',SessionTable,account,sid,verfiySid)
    log_util.debug('[try checkOrder] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    group_id  = redis.hget(user_table,'parentAg')

    # goodsId = redis.get(GOODS_NAME2NUM%(goodsName))
    goods_table = GOODS_TABLE%(goodsId)
    cards,goodsName,present_card, goodsPrice = redis.hmget(goods_table,('cards','name','present_cards', 'price'))
    #判断金币价格
    # goodsPrice = getGoodsMoney(redis,group_id,cards)
    if not redis.exists(goods_table):
        log_util.error('[try goods][error] goods[%s] is not found.'%(goodsName))
        return {'code':-1, 'msg':'goods not found'}


    log_util.debug('[try goods] player cards[%s] goodsPrice[%s].'%(cards,goodsPrice))

    goodsId2OrderId = GOODS_NUM4FISH%(goodsId)
    orderIndex = redis.incr(goodsId2OrderId)
    if orderIndex >= 10000000000:
        redis.set(goodsId2OrderId, 0)
        orderIndex = redis.incr(goodsId2OrderId)
    outTradeNo = getOutTradeNo(goodsId, orderIndex)

    # data = (player, goodsBody, totalPrice, outTradeNo, goodsCount, goodsId, goodsName, goodsCards)
    # order2weixin(data) *data
    urlRes = urlparse(request.url)
    serverIp = urlRes.netloc.split(':')[0]

    nonceStr = wechat_util.tx_wechat_order_nonce()
    signDict = {
        'appid'             :       APPID_FISH,
        'mch_id'            :       MCH_ID_FISH,
        'nonce_str'         :       nonceStr,
        'body'              :       goodsName,
        'out_trade_no'      :       outTradeNo,
        'total_fee'         :       int(float(goodsPrice) * 100),
        'spbill_create_ip'  :       ip,
        'notify_url'        :       NOTIFY_URL_FISH%(serverIp),
        'trade_type'        :       TRADE_TYPE
    }

    #print payment params
    log_util.debug('[%s][onWechatPay][info] payParams[%s]'%(curTime,signDict))

    # signList = packSignDict2List(signDict)
    # sign = getSign4TX(signList)
    sign = wechat_util.gen_sign4fish(signDict)

    orderStr = packSignDict2XML(signDict, sign)
    url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    resultDict = wechat_util.get_xml_message(url, orderStr)
    log_util.debug('wxPay url[%s] data[%s] sign[%s] signDict[%s]'%(url, orderStr, sign, signDict))
    log_util.debug('resultDict: %s'%resultDict)

    if not resultDict:
        log_util.error('[%s][onWechatPay][error] resultDict[%s]'%(curTime,resultDict))
        return {'code':-1, 'msg':'微信支付失败'}

    if resultDict['return_code'] != 'SUCCESS':
        try:
            log_util.debug('[%s][onWechatPay][error] resultDict[%s]'%(curTime,resultDict['return_msg']))
        except:
            pass
        return {'code':-1, 'msg':'微信支付未开启'}

    prepayID = resultDict['prepay_id']
    package = 'Sign=WXPay'
    timeStamp = int(time.time())
    # signList = [
        # 'appid=%s'%(APPID_FISH),
        # 'partnerid=%s'%(MCH_ID_FISH),
        # 'prepayid=%s'%(prepayID),
        # 'package=%s'%(package),
        # 'noncestr=%s'%(nonceStr),
        # 'timeStamp=%s'%(timeStamp),
    # ]
    signList = {'appid':APPID_FISH, 'partnerid':MCH_ID_FISH, 'prepayid':prepayID, 'package':package, 'noncestr':nonceStr, 'timeStamp':timeStamp}
    sign = wechat_util.gen_sign4fish(signList)
    sign = '1'

    pipe = redis.pipeline()
    # pipe.set(PENDING4ACCOUNT%(player.account, totalPrice, goodsBody), outTradeNo)
    orderTable = ORDER_TABLE4FISH%(outTradeNo)
    pipe.hmset(orderTable,
        {
            'time'         :       timeStamp,
            'sign'         :       sign,
            'nonceStr'     :       nonceStr,
            'prepayID'     :       prepayID,
            'name'         :       goodsName,
            'body'         :       "123",
            'money'        :       int(float(goodsPrice) * 100),
            'startTime'    :       timeStamp,
            'account'      :       account,
            'num'          :       goodsId,
            'type'         :       'pending',
            'roomCards'    :       cards,
            'presentCards' :       present_card
        }
    )
    pipe.sadd(PENDING_ORDER4FISH, outTradeNo)
    pipe.lpush(ORDER_NUM_LIST4FISH, outTradeNo)
    pipe.sadd(PLAYER_ORDER4FISH%(account), outTradeNo)

    pipe.lpush(DAY_ORDER4FISH%(curTime.strftime("%Y-%m-%d")), outTradeNo)
    pipe.lpush(DAY_PENDING_ORDER4FISH%(curTime.strftime("%Y-%m-%d")), outTradeNo)
    pipe.expire(orderTable, 1 * 60 * 60)
    pipe.execute()

    #发送成功信息
    app_prepay_info = {'partnerid':MCH_ID_FISH, 'prepayid':prepayID, 'noncestr':nonceStr, 'paySign':sign, 'timestamp':str(timeStamp), 'appid':APPID_FISH, 'package':'Sign=WXPay', }
    data = {'partnerId':str(MCH_ID_FISH),'prepayID':str(prepayID), 'nonceStr':nonceStr,'sign':sign, 'outTradeNo':outTradeNo, 'curTime':curTime.strftime("%Y-%m-%d %H:%M:%S"), 'timeStamp':str(timeStamp), 'sub_appid':APPID_FISH, 'app_prepay_info':app_prepay_info}

    log_util.debug("[try order succeed] data %s"%data)
    log_util.debug("[try order succeed] account[%s] outTradeNo[%s]."%(account, outTradeNo))
    return {'code':0, 'data':data}

@fish_app.post('/checkOrder')
def do_checkOrder(redis, session):
    """
    检查微信支付是否成功接口
    """
    curTime = datetime.now()

    orderSwitch = convert_util.to_int(redis.hget(FISH_CONSTS_CONFIG,'wechat_switch'))

    outTradeNo = request.forms.get('outTradeNo','').strip()
    sid = request.forms.get('sid','').strip()

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/checkOrder/',SessionTable,account,sid,verfiySid)
    log_util.debug('[try checkOrder] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    if not outTradeNo:
        return {'code':-1, 'msg':'outTradeNo不存在'}

    orderTable = ORDER_TABLE4FISH%(outTradeNo)
    if not redis.exists(SUCCEED_ORDER4FISH) or not redis.sismember(SUCCEED_ORDER4FISH, orderTable):
        return {'code':-9}

    if not orderTable:
        return {'code':-1, 'msg':'orderTable不存在'}

    roomCards = redis.hget(orderTable,('roomCards'))
    checkNum = redis.hincrby(orderTable, 'CheckNum', 1)

    groupId = redis.hget(user_table, 'parentAg')
    redis.hset(orderTable,'groupId',groupId)
    # roomCard = redis.get(USER4AGENT_CARD%(groupId, id))
    roomCard = redis.hget(user_table, 'coin')
    return {'code':0,'roomCard':roomCard}
