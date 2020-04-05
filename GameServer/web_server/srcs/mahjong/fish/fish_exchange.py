#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    捕鱼邀请接口相关
"""
from bottle import request,response,default_app
from fish import fish_app
from datetime import datetime
from model.hallModel import get_fish_hall_setting,check_session_verfiy
from model.goodsModel import *
from model.userModel import *
from common.utilt import allow_cross,getInfoBySid
from common import log_util,web_util
from fish_config import consts

@fish_app.post('/getRewardInfo')
@allow_cross
def get_fish_goods_info(redis,session):
    '''
    捕鱼获取商城商品接口
    :params sid 用户登录session
    :params ver 当前商城的ver
    :return  rewardInfo:[{},{}],addressInfo:{}
    '''
    fields = ('sid','rewardType','ver')
    onshop_fields = ('reward_name','reward_per_stock','reward_img_path','reward_need_ticket','reward_pos','reward_type')
    for field in fields:
        exec(consts.FORMAT_PARAMS_POST_STR%(field,field))

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/getRewardInfo/',SessionTable,account,sid,verfiySid)
    log_util.debug('[try do_refresh] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    user_addr_table = FORMAT_USER_ADDRESS_TABLE%(uid)
    if not redis.exists(user_addr_table):
        address_info = {}
    else:
        address_info = redis.hgetall(user_addr_table)
    #获取奖品列表
    reward_type_info,reward_goods_info = get_reward_shop_api_data(redis,onshop_fields)
    log_util.debug('[try get_fish_goods_info]  sid[%s] goodsInfo[%s] address_info[%s] '%(sid,reward_goods_info,address_info))
    return {'code':0,'typeInfo':reward_type_info,'rewardInfo':reward_goods_info,'addressInfo':address_info}

@fish_app.post('/getExchangeRecord')
@allow_cross
def get_user_reward_record(redis,session):
    """
    玩家兑换记录接口
    """
    fields = ('sid','pageNum')
    exchange_fields = ( # 兑换记录需要的字段
        'exchange_reward_name',
        'exchange_card_no',
        'exchange_card_pwd',
        'exchange_date',
        'exchange_reward_status'
    )
    for field in fields:
        exec(consts.FORMAT_PARAMS_POST_STR%(field,field))

    try:
        log_util.debug('[try get_user_reward_record] get params sid[%s] pageNum[%s]'%(sid,pageNum))
        if not pageNum:
            pageNum = 1
    except:
        return {'code':-300,'msg':'接口参数错误'}
    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/getRewardInfo/',SessionTable,account,sid,verfiySid)
    log_util.debug('[try do_refresh] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    pageNum = convert_util.to_int(pageNum)

    user_exchange_list,user_total_record = get_user_exchange_list(redis,uid,exchange_fields,pageNum,consts.NUMS_PER_PAGE)
    log_util.debug('[try get_user_reward_record]  sid[%s] user_exchange_list[%s]'%(sid,user_exchange_list))
    return {'code':0,'userExchangeInfo':user_exchange_list,'totalRecords':user_total_record}

@fish_app.post('/doExchange')
@allow_cross
def do_reward_exchange(redis,session):
    '''
    玩家兑换奖品协议
    @params:
            sid : 玩家sesion
            rewardId : 奖品ID
    '''
    curTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dateStr = datetime.now().strftime('%Y-%m-%d')
    fields = ('sid','rewardId','needTicket')
    for field in fields:
        exec(consts.FORMAT_PARAMS_POST_STR%(field,field))

    try:
        log_util.debug('[try do_reward_exchange] get params ticket[%s] sid[%s] rewardId[%s]'%(needTicket,sid,rewardId))
    except:
        return {'code':-300,'msg':'接口参数错误.'}

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/doExchange/',SessionTable,account,sid,verfiySid)
    log_util.debug('[try do_refresh] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    if not redis.exists(FISH_REWARD_TABLE%(rewardId)):
        return {'code':-4001,'msg':'兑换商品不存在或已过期'}

    reward_table    = FISH_REWARD_TABLE%(rewardId)
    user_addr_table = FORMAT_USER_ADDRESS_TABLE%(uid)
    if not redis.exists(user_addr_table):
        return {'code':-4004,'msg':'请先设置奖品收货地址信息'}

    user_exchange_ticket = convert_util.to_int(redis.hget(user_table,'exchange_ticket'))
    needTicket = convert_util.to_int(needTicket)
    #获取奖品对应信息
    reward_need_ticket,reward_name,reward_per_stock,reward_img_path,reward_card_no,reward_card_pwd,reward_type,reward_coin,reward_status= \
                redis.hmget(reward_table,('reward_need_ticket','reward_name','reward_per_stock','reward_img_path','reward_card_no','reward_card_pwd','reward_type','reward_coin','reward_status'))

    reward_need_ticket = convert_util.to_int(reward_need_ticket)
    reward_coin = convert_util.to_int(reward_coin)
    reward_type = convert_util.to_int(reward_type)
    reward_status = convert_util.to_int(reward_status)
    reward_per_stock = convert_util.to_int(reward_per_stock)

    if reward_status == consts.REWARD_OFFLINE:
        return {'code':-4005,'msg':'该奖品未上架'}

    if reward_per_stock <= 0:
        #根正数据错误
        redis.hset(reward_table,'reward_per_stock',0)
        return {'code':0,'msg':'库存不足','type':3,'userTicket':user_exchange_ticket,'needTicket':reward_need_ticket,'rewardStock':0}

    if needTicket != reward_need_ticket:
        reward_per_stock = convert_util.to_int(redis.hget(reward_table,'reward_per_stock'))
        return {'code':0,'msg':'使用兑换卷和所需兑换卷不一致','type':3,'userTicket':user_exchange_ticket,'needTicket':reward_need_ticket,'rewardStock':reward_per_stock}

    if user_exchange_ticket < needTicket:
        reward_per_stock = convert_util.to_int(redis.hget(reward_table,'reward_per_stock'))
        log_util.debug('[try do_reward_exchange] needTicke[%s] user_exchange_ticket[%s]'%(needTicket,user_exchange_ticket))
        return {'code':0,'msg':'兑换卷不足','type':3,'userTicket':user_exchange_ticket,'needTicket':reward_need_ticket,'rewardStock':reward_per_stock}

    #写入相应的兑换记录表
    #减去玩家相应的兑换卷
    #减去兑换奖品库存
    user_addr_info = redis.hgetall(user_addr_table)
    exchange_info = {
            'user_id'                   :   uid,
            'exchange_date'             :   curTime,
            'exchange_reward_id'        :   rewardId,
            'exchange_reward_name'      :   reward_name,
            'exchange_use_ticket'       :   needTicket,
            'exchange_type'             :   reward_type,
            'exchange_leave_ticket'     :   user_exchange_ticket-needTicket,
            'exchange_reward_img_path'  :   reward_img_path,
            'exchange_need_ticket'      :   reward_need_ticket,
            'exchange_card_no'          :   reward_card_no if reward_card_no else '',
            'exchange_card_pwd'         :   reward_card_pwd if reward_card_pwd else '',
            'exchange_reward_status'    :   '0',
            'exchange_user_name'        :   user_addr_info['name'],
            'exchange_user_phone'       :   user_addr_info['phone'],
            'exchange_user_addr'        :   user_addr_info['city']+user_addr_info['address']
    }
    pipe = redis.pipeline()
    try:
        ori_exchange_id = redis.get(FISH_EXCHANGE_ID_COUNT)
        exchange_id = redis.incr(FISH_EXCHANGE_ID_COUNT)
        exchange_info['exchange_id'] = exchange_id
        pipe.hincrby(user_table,'exchange_ticket',-int(needTicket))
        pipe.hincrby(reward_table,'reward_per_stock',-1)
        #设置兑换表
        pipe.set(FISH_EXCHANGE_TABLE%(exchange_id),exchange_info)
        #写入兑换记录列表
        pipe.lpush(FISH_EXCHANGE_LIST,exchange_id)
        #写入用户兑换记录表
        pipe.lpush(FISH_USER_EXCHANGE_LIST%(uid),exchange_id)
        #写入兑换记日期索引表
        pipe.lpush(FISH_USER_EXCHANGE_DATE%(dateStr),exchange_id)
        #写入状态索
        pipe.lpush(FISH_USER_EXCHANGE_STATUS_LIST%(0),exchange_id)
    except Exception,e:
        redis.set(FISH_EXCHANGE_ID_COUNT,ori_exchange_id)
        reward_per_stock = convert_util.to_int(redis.hget(reward_table,'reward_per_stock'))
        log_util.debug('[try do_reward_exchange] exchange error reason[%s]'%(e))
        return {'code':-4004,'msg':'数据错误','needTicket':reward_need_ticket,'rewardStock':reward_per_stock}

    log_util.debug('[try do_reward_exchange] return userTicket[%s] reward_per_stock[%s]'%(exchange_info['exchange_leave_ticket'],reward_per_stock))
    # if reward_type == consts.COIN_EXCHANGE: #金币兑换
    #     pipe.hincrby(user_table,'coin',reward_coin)
    #     exchange_info['exchange_reward_status'] = 1
    #     pipe.set(FISH_EXCHANGE_TABLE%(exchange_id),exchange_info)
    #     pipe.execute()
    #     #领取后的库存
    #     reward_per_stock = convert_util.to_int(redis.hget(reward_table,'reward_per_stock'))
    #     return {'code':0,'msg':'兑换成功,获得{}个金币'.format(reward_coin),'type':reward_type,'coin':reward_coin,'userTicket':exchange_info['exchange_leave_ticket'],'needTicket':reward_need_ticket,'rewardStock':reward_per_stock}

    if reward_type == consts.CARD_EXCHANGE: #卡密兑换
        exchange_info['exchange_reward_status'] = 1
        pipe.set(FISH_EXCHANGE_TABLE%(exchange_id),exchange_info)
        pipe.execute()
        #领取后的库存
        reward_per_stock = convert_util.to_int(redis.hget(reward_table,'reward_per_stock'))
        return {'code':0,'msg':'兑换成功','cardNo':reward_card_no,'type':consts.CARD_EXCHANGE,'cardPwd':reward_card_pwd,'userTicket':exchange_info['exchange_leave_ticket'],'needTicket':reward_need_ticket,'rewardStock':reward_per_stock}

    elif reward_type in [consts.REAL_EXCHANGE,consts.GOODS_EXCHANGE,consts.PHONE_EXCHANGE,consts.COIN_EXCHANGE]:
        pipe.execute()
        #领取后的库存
        reward_per_stock = convert_util.to_int(redis.hget(reward_table,'reward_per_stock'))
        return {'code':0,'msg':'兑换成功,奖品将在3-5个工作日内发出,请注意查收','type':consts.REAL_EXCHANGE,'userTicket':exchange_info['exchange_leave_ticket'],'needTicket':reward_need_ticket,'rewardStock':reward_per_stock}

    else:
        #领取后的库存
        reward_per_stock = convert_util.to_int(redis.hget(reward_table,'reward_per_stock'))
        return {'code':0,'msg':'兑换失败','type':3,'userTicket':exchange_info['exchange_leave_ticket'],'needTicket':reward_need_ticket,'rewardStock':reward_per_stock}

@fish_app.post('/doAddress')
@allow_cross
def do_address(redis,session):
    '''
    玩家操作收获地址接口
    @params:
        sid
        phone
        province
        city
        address
        name
    '''
    fields = ('sid','name','phone','city','address','action')
    for field in fields:
        exec(consts.FORMAT_PARAMS_POST_STR%(field,field))

    try:
        log_util.debug('[try do_address] get parasm sid[%s] name[%s]  phone[%s] city[%s] addr[%s]'%(sid,name,phone,city,address))
    except:
        return {'code':-300,'msg':'接口参数错误'}

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/getRewardInfo/',SessionTable,account,sid,verfiySid)
    log_util.debug('[try do_refresh] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    if action not in ['add','modify','delete']:
        return {'code':-2001,'msg':'不被允许的操作,请重试.'}

    address_info = {
            'name'      :       name,
            'phone'     :       phone,
            'city'      :       city,
            'address'   :       address
    }
    action_2_fun = {
        'add'       :   do_user_modify_addr,
        'modify'    :   do_user_modify_addr,
        'delete'    :   do_user_del_addr
    }
    op_result = action_2_fun[action](redis,uid,address_info)
    log_util.debug('[try do_address] sid[%s] action[%s] op_result[%s]'%(sid,action,op_result))
    return {'code':0,'msg':'操作成功'}

@fish_app.post('/getRewardBaseInfo')
@allow_cross
def refresh_reward_stock(redis,session):
    """
    刷新所有商品的库存接口
    :params  sid  返回最新库存的ID和库存
    """
    onshop_fields = ('reward_per_stock',)
    fields = ('sid',)
    for field in fields:
        exec('%s = request.forms.get("%s","").strip()'%(field,field))

    try:
        log_util.debug('[try refresh_reward_stock] sid[%s]'%(sid))
    except:
        return {'code':-300,'msg':'接口参数请求错误!'}

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/getRewardInfo/',SessionTable,account,sid,verfiySid)
    log_util.debug('[try do_refresh] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    reward_info = get_reward_shop_data(redis,onshop_fields)
    log_util.debug('[try refresh_reward_stock]  sid[%s] goodsInfo[%s] '%(sid,reward_info))
    return {'code':0,'rewardInfo':reward_info}

@fish_app.post('/doGainExchangeTicket')
@allow_cross
def do_gain_exchange_ticket(redis,session):
    """
    获取捕鱼奖品兑换卷接口
    """
    fields = ('sid','tickets')
    for field in fields:
        exec(consts.FORMAT_PARAMS_POST_STR%(field,field))

    try:
        log_util.debug('[try do_gain_exchange_ticket] sid[%s] tickets[%s]'%(sid,tickets))
    except:
        return {'code':-300,'msg':'接口请求参数错误'}

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/getRewardInfo/',SessionTable,account,sid,verfiySid)
    log_util.debug('[try do_refresh] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    if int(tickets) < 0:
        return {'code':-5001,'msg':'奖券数据错误'}
    #测试
    exchange_ticket = redis.hincrby(user_table,'exchange_ticket',int(tickets))
    return {'code':0,'userTickets':exchange_ticket}
