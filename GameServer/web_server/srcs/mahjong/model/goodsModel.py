#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    商品模型
"""
from web_db_define import *
from common.log import *
from operator import itemgetter
from common import log_util,web_util,convert_util
from common.utilt import getLang
import agentModel
import copy

FISH_REWARD_LIST_OP = [
        #{'url':'/admin/goods/reward/status','txt':'上架','method':'POST'},
        {'url':'/admin/goods/reward/modify','txt':'编辑','method':'POST'},
        #{'url':'/admin/goods/reward/auto_charge','txt':'自动续期','method':'POST'},
        {'url':'/admin/goods/reward/delete','txt':'删除','method':'POST'},
]

FISH_EXCHANGE_LIST_OP = [
        {'url':'/admin/goods/reward/exchange/status','txt':'发货','method':'POST'},
]

def do_create_goods(redis,goodsInfo):
    """
    创建商品方法
    """
    goods_id  =  redis.incr(GOODS_COUNT)
    goodsInfo['id'] = goods_id
    goodsTable = GOODS_TABLE%(goods_id)

    pipe = redis.pipeline()
    pipe.hmset(goodsTable,goodsInfo)
    pipe.lpush(GOODS_LIST,goods_id)
    pipe.lpush(GOODS_TYPE_LIST%(goodsInfo['type']),goods_id)
    #更新版本号
    pipe.hincrby(FISH_CONSTS_CONFIG,'shop_version',1)
    return pipe.execute()

def getGoodsMoney(redis,groupId,cardNums):
    """
    获取每个玩家所在公会的价格
    """
    companyId = agentModel.getTopAgentId(redis,groupId)
    log_debug('[getGoodsMoney] groupId[%s] cardNums[%s] companyId[%s]'%(groupId,cardNums,companyId))
    unitPrice = redis.hget(AGENT_TABLE%(companyId),'unitPrice')

    return int(cardNums)*round(float(unitPrice),2)

def get_goods_list(redis,goods_type,action):
    """
    获取商品列表
    """
    goods_ids = redis.lrange(GOODS_TYPE_LIST%(goods_type),0,-1)
    if goods_type == '0':
        goods_ids.extend(redis.lrange(GOODS_TYPE_LIST % '2', 0, -1))
        goods_ids.extend(redis.lrange(GOODS_TYPE_LIST % '4', 0, -1))
    log_util.debug('goods_ids[%s]'%(goods_ids))
    goodsList = []

    type2name = {
            '0'     :       '游戏钻石',
            '1'     :       '游戏金币',
            '2'     :       '金币场金币',
            '4'     :       '其他',
    }

    for goods_id in goods_ids:
        if not redis.exists(GOODS_TABLE % goods_id):
            continue
        goodInfo = redis.hgetall(GOODS_TABLE%(goods_id))
        _type = goodInfo.get('type', '0')
        goodInfo['goods_type'] = type2name[_type]
        goodInfo['op'] = [
                        {'url':'/admin/goods/modify/{}'.format(action),'txt':'修改','method':'POST'},
                        {'url':'/admin/goods/del/{}'.format(action),'txt':'删除','method':'POST'},
        ]
        goodsList.append(goodInfo)

    return goodsList


def getHallGoodsList(redis, _type):
    """
        获取商城商品列表
    """
    goodids = redis.lrange(GOODS_LIST, 0, -1)
    res = []
    for goodid in goodids:
        info = redis.hgetall(GOODS_TABLE % goodid)
        if not info.has_key('type'):
            continue
        if info['type'] != _type:
            continue
        res.append(info)
    return res

def get_dia_goods_list(redis,groupId):
    """
    获取钻石商品列表
    """
    goods_ids = redis.lrange(GOODS_TYPE_LIST%('0'),0,-1)
    goodsList = []
    for good_id in goods_ids:
        goodInfo = redis.hgetall(GOODS_TABLE%(good_id))
        # goodInfo['price'] = getGoodsMoney(redis,groupId,goodInfo['cards'])
        goodsList.append(goodInfo)

    return goodsList

def get_coin_goods_list(redis):
    """
    获取金币商品列表
    """
    goods_ids = redis.lrange(GOODS_TYPE_LIST%('1'),0,-1)
    goodsList = []
    for goods_id in goods_ids:
        goodInfo = redis.hgetall(GOODS_TABLE%(goods_id))
        if not goodInfo:
            continue
        goodsList.append(goodInfo)

    return goodsList

def do_goods_modify(redis,goodsId,goodsInfo):
    """
    商品模块修改
    """
    pipe = redis.pipeline()
    pipe.hmset(GOODS_TABLE%(goodsId),goodsInfo)
    #更新版本号
    pipe.hincrby(FISH_CONSTS_CONFIG,'shop_version',1)
    return pipe.execute()

def get_goods_info(redis,goodsId):
    """
    获取商品信息
    """
    return redis.hgetall(GOODS_TABLE%(goodsId))

def get_reward_info(redis,reward_id):
    '''
    获取奖品信息
    '''
    return redis.hgetall(FISH_REWARD_TABLE%(reward_id))


def setGoodsPrice(redis,price):
    """
    设置钻石单价
    """
    return redis.lpush(GOODS_ROOMCARD_PRICE,price)

def getGoodsPrice(redis):
    """
    获取最新钻石单价
    """
    return redis.lrange(GOODS_ROOMCARD_PRICE,0,1)[0]

def do_create_reward(redis,reward_info):
    '''
    创建奖品列表
    '''
    pipe = redis.pipeline()
    try:
        pipe.lpush(FISH_REWARD_LIST,reward_info['reward_id'])
        pipe.hmset(FISH_REWARD_TABLE%(reward_info['reward_id']),reward_info)
        pipe.sadd(FISH_REWARD_ID_SET,reward_info['reward_id'])
    except Exception,e:
        log_debug('[try do_create_reward] create error[%s]'%(e))
        return

    pipe.execute()

def do_modify_reward(redis,reward_info):
    '''
    修改奖品信息
    '''
    pipe = redis.pipeline()
    pipe.hmset(FISH_REWARD_TABLE%(reward_info['reward_id']),reward_info)
    #修改商品信息后,商品需要重新上架
    pipe.lrem(FISH_REWARD_ON_SHOP_LIST,reward_info['reward_id'])
    #增加版本号
    pipe.hincrby(FISH_CONSTS_CONFIG,'exchange_shop_ver',1)
    pipe.execute()

def do_reward_delete(redis,reward_id):
    """
    删除奖品接口
    :params redis
    :params reward_id 奖品ID
    """
    reward_table = FISH_REWARD_TABLE%(reward_id)
    pipe = redis.pipeline()
    try:
        pipe.delete(reward_table)
        pipe.lrem(FISH_REWARD_LIST,reward_id)
        pipe.srem(FISH_REWARD_ID_SET,reward_id)
        pipe.srem(FISH_REWARD_AUTO_CHARGE,reward_id)
    except Exception,e:
        log_uti.error('[do_reward_delete] error . reason[%s]'%(e))
        return
    pipe.execute()

def get_fish_reward_list(redis,get_op=True):
    '''
    获取奖品列表
    '''
    reward_ids = redis.lrange(FISH_REWARD_LIST,0,-1)
    reward_lists = []
    for reward_id in reward_ids:
        reward_info = redis.hgetall(FISH_REWARD_TABLE%(reward_id))
        if get_op:
            tempOp = []
            tempOp = copy.copy(FISH_REWARD_LIST_OP)
            tempOp.append({'url':'/admin/goods/reward/status','txt':'下架' if reward_info['reward_status'] == '1' else '上架','method':'POST'})
            tempOp.append({'url':'/admin/goods/reward/auto_charge','txt':'取消自动续期' if reward_info['reward_auto_charge'] =='1' else '自动续期','method':'POST'})
            reward_info['op'] = tempOp
        reward_lists.append(reward_info)

    return reward_lists

def get_reward_shop_api_data(redis,on_shop_field):
    """
    获取商城数据（大厅接口1）
    """
    lang = getLang()
    def index2dic(des_type):
        return lang.REWARD_TYPE_2_DESC[des_type]

    on_shop_lists = get_reward_shop_data(redis,on_shop_field)
    on_shop_dic = {0:[],1:[],2:[],3:[],4:[]}
    on_shop_type = on_shop_dic.keys()
    for on_shop in on_shop_lists:
        on_shop['reward_type'] = lang.REWARD_TYPE_2_DESC[convert_util.to_int(on_shop['reward_type'])]

    log_util.debug('[try get_reward_shop_api_data] on_shop[%s]'%(on_shop_lists))
    return map(index2dic,[0,1,2,3,4]),on_shop_lists

def get_reward_shop_data(redis,on_shop_fields):
    """
    获取商城数据
    :params redis 数据库实例
    :params on_shop_fields 获取的字段值
    """
    reward_onshop_ids = redis.lrange(FISH_REWARD_ON_SHOP_LIST,0,-1)
    shop_lists = []
    #onshop_fields = ('reward_name','reward_id','reward_stock','reward_img_path','reward_need_ticket')
    for onshop_id in reward_onshop_ids:
        shop_info = {}
        for on_shop_field in on_shop_fields:
            shop_info[on_shop_field] = redis.hget(FISH_REWARD_TABLE%(onshop_id),on_shop_field)
        shop_info['reward_id'] = int(onshop_id)
        shop_lists.append(shop_info)

    return shop_lists

def get_exchange_infos(redis,start_date,end_date,user_id,sort_name,sort_method,pageSize,pageNumber):
    '''
    获取玩家兑换信息列表
    '''
    if user_id:
        total = redis.llen(FISH_USER_EXCHANGE_LIST%(user_id))
        exchange_ids = redis.lrange(FISH_USER_EXCHANGE_LIST%(user_id),0,-1)
    else:
        total = redis.llen(FISH_EXCHANGE_LIST)
        exchange_ids = redis.lrange(FISH_EXCHANGE_LIST,0,-1)

    exchange_id_keys = [FISH_EXCHANGE_TABLE%(exchange_id) for exchange_id in exchange_ids]
    exchange_details = [exchange_detail for exchange_detail in redis.mget(exchange_id_keys)]
    exchange_info = []
    for exchange_detail in exchange_details:
        exchange_detail = eval(exchange_detail)
        if int(exchange_detail['exchange_reward_status']) == 1:
            exchange_detail['op'] = []
        else:
            exchange_detail['op'] = FISH_EXCHANGE_LIST_OP
        exchange_info.append(exchange_detail)
    exchange_info = sorted(exchange_info, key=itemgetter(sort_name),reverse=sort_method)
    #分页渲染
    exchange_info = web_util.get_server_pagination(exchange_info,pageSize,pageNumber)
    #exchange_info = sorted(exchange_info, key=itemgetter(sort_name),reverse=True)
    return {'data':exchange_info,'count':convert_util.to_int(total)}
