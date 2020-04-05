#!/usr/bin/env python
#-*-coding:utf-8 -*-

"""
    @Author: $Author$
    @Date: $Date$
    @version: $Revision$

    Description:
        捕鱼支付函数
"""
from wechat.wechatData import *
#from config.config import *
from fish.fish_config import consts
from datetime import datetime
from common import convert_util,web_util,json_util,wechat_util
import time

def do_pay_record(redis,user_id,user_table,coin,price):
    """
    捕鱼支付统计
    :params redis实例
    :params user_id 用户ID
    :params coin 支付金币
    """
    today  = convert_util.to_dateStr(datetime.now())
    coin = convert_util.to_int(coin)
    pipe = redis.pipeline()
    try:
        pipe.hincrby(user_table,'coin',coin)
        pipe.hincrbyfloat(user_table,'recharge_coin_total',price)
        pipe.incrbyfloat(FISH_SYSTEM_RECHARGE_TOTAL,price)
        pipe.hincrbyfloat(FISH_SYSTEM_DATE_RECHARGE_TOTAL%(today),'recharge_coin_total',price)
        if not redis.sismember(FISH_RECHARGE_USER_DAY_IDS,user_id):
            pipe.hincrby(FISH_SYSTEM_DATE_RECHARGE_TOTAL%(today),'recharge_user_total',1)
            pipe.sadd(FISH_RECHARGE_USER_DAY_IDS,user_id)
    except Exception,e:
        log_util.error('[FUNC do_pay_record] Error userId[%s] coin[%s] reason[%s]'%(user_id,coin,e),True)
        return None

    return pipe.execute()

def do_add_fishcoin_2_members(redis,transNo):
    """
    捕鱼玩家增加金币,收到微信支付成功通知后回调
    :params redis 数据库连接实例
    :params transNo 订单号
    """
    curTime = datetime.now()
    orderTable = ORDER_TABLE4FISH%(transNo)
    if not redis.exists(orderTable):
        log_util.debug('[%s][wechatPay][error] orderNo[%s] is not exists.'%(curTime,params['out_trade_no']))
        return False

    cardNums,present_card = redis.hmget(orderTable,('roomCards','presentCards'))
    cardNums = convert_util.to_int(cardNums)
    present_card = convert_util.to_int(present_card)

    rType,memberAccount,order_money= redis.hmget(orderTable,('num','account','money'))

    #chargeNums = TYPE_2_CARS[rType]
    account2user_table = FORMAT_ACCOUNT2USER_TABLE%(memberAccount) #从账号获得账号信息，和旧系统一样
    userTable = redis.get(account2user_table)
    groupId,ori_coin = redis.hmget(userTable, 'parentAg','coin')
    log_util.debug('[func addCoin2Member4fish] ori_coin[%s] recharge_coin[%s] present_coin[%s] order_money[%s]'%(ori_coin,cardNums,present_card,order_money))
    pipe = redis.pipeline()
    pipe.hincrby(userTable, 'coin', cardNums+present_card)
    #记录今日充值数
    do_pay_record(redis,userTable.split(":")[1],userTable,cardNums,order_money)
    log_util.debug('[%s][wechatPay] recharge roomcards[%s] to account[%s] success'%(curTime,cardNums,memberAccount))
    pipe.execute()
    return

def test_WeChatPay(redis,goodsId,userTable):
    """
    本地模拟微信支付生成订单接口
    """
    curTime = datetime.now()
    ip = web_util.get_ip()

    account  = redis.hget(userTable,'account')
    # goodsId = redis.get(GOODS_NAME2NUM%(goodsName))
    goodsTable = GOODS_TABLE%(goodsId)
    cards,goodsName,present_card, goodsPrice = redis.hmget(goodsTable,('cards','name','present_cards', 'price'))
    #判断金币价格
    # goodsPrice = getGoodsMoney(redis,group_id,cards)
    if not redis.exists(goodsTable):
        log_util.error('[try goods][error] goodId[%s] goods[%s] is not found.'%(goodsId,goodsName))
        return {'code':-1, 'msg':'goods not found'}

    log_util.debug('[try goods] player cards[%s] goodsPrice[%s].'%(cards,goodsPrice))

    goodsId2OrderId = GOODS_NUM4FISH%(goodsId)
    orderIndex = redis.incr(goodsId2OrderId)
    if orderIndex >= 10000000000:
        redis.set(goodsId2OrderId, 0)
        orderIndex = redis.incr(goodsId2OrderId)
    outTradeNo = getOutTradeNo(goodsId, orderIndex)

    #print payment params
    log_util.debug('[try test_WeChatPay] payParams[%s]'%(outTradeNo))

    # signList = packSignDict2List(signDict)
    # sign = getSign(signList)
    timeStamp = int(time.time())
    pipe = redis.pipeline()
    # pipe.set(PENDING4ACCOUNT%(player.account, totalPrice, goodsBody), outTradeNo)
    orderTable = ORDER_TABLE4FISH%(outTradeNo)
    try:
        pipe.hmset(orderTable,
            {
                'time'         :       timeStamp,
                'sign'         :       'wechat_text',
                'nonceStr'     :       'test',
                'prepayID'     :       'test',
                'name'         :       goodsName,
                'body'         :       "123",
                'money'        :       int(float(goodsPrice) * 100),
                'startTime'    :       timeStamp,
                'account'      :       account,
                'num'          :       goodsId,
                'type'         :       'success',
                'roomCards'    :       cards,
                'presentCards' :       present_card
            }
        )
        pipe.sadd(SUCCEED_ORDER4FISH, outTradeNo)
        pipe.lpush(ORDER_NUM_LIST4FISH, outTradeNo)
        pipe.sadd(PLAYER_ORDER4FISH%(account), outTradeNo)

        pipe.lpush(DAY_ORDER4FISH%(curTime.strftime("%Y-%m-%d")),outTradeNo)
        log_util.debug('success [%s]'%(DAY_ORDER4FISH%(curTime.strftime("%Y-%m-%d"))))
        pipe.lpush(DAY_SUCCEED_ORDER4FISH%(curTime.strftime("%Y-%m-%d")), outTradeNo)
        pipe.expire(orderTable, 1 * 60 * 60)
    except Exception,e:
        log_util.debug('[error] reason[%s]'%(e))
        return

    return pipe.execute()

def para_filter(params):
    """
        过滤参数
    """
    return {key: params[key]
            for key in params
            if key.lower() not in {'sign'} and params[key]}

def checkSign(params):
    """
        验证签名
    """
    if 'sign' not in params:
        return False
    wx_sign = params['sign']
    filter_params = para_filter(params)
    sign = wechat_util.gen_sign4fish(filter_params)
    return wx_sign == sign

def verfiyRcvDatas(redis,params):
    """
        校验支付数据
    """
    curTime = datetime.now()
    orderTable = ORDER_TABLE4FISH%(params['out_trade_no'])
    if not redis.exists(orderTable):
        log_util.debug('[%s][wechatPay][error] orderNo[%s] is not exists.'%(curTime,params['out_trade_no']))
        return False

    updateInfo = {
            'money'         :       params['total_fee'],
            'endTime'       :       params['time_end'],
            'currency'      :       params['fee_type'],
            'orderNum'      :       params['transaction_id'],
            'type'          :       'successful',
    }

    pipe = redis.pipeline()
    try:
        log_util.debug('[%s][wechatPay][info] update orderInfo[%s] success.'\
                                    %(curTime,updateInfo))
        pipe.hmset(orderTable,updateInfo)
        pipe.srem(PENDING_ORDER4FISH,orderTable)
        pipe.sadd(SUCCEED_ORDER4FISH,orderTable)
        pipe.persist(orderTable)
        pipe.execute()
    except:
        log_util.debug('[%s][wechatPay][error] update orderInfo[%s] error.'%(curTime,updateInfo))
        return False

    return True
