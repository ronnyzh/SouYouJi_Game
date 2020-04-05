#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    商品自动续期脚本
"""
import sys
sys.path.insert(0, './server_common')
sys.path.insert(0, './mahjong')
from web_db_define import FISH_REWARD_AUTO_CHARGE,FISH_REWARD_ON_SHOP_LIST,FISH_REWARD_TABLE
from datetime import datetime
import time
from common import log_util
import redis
import hashlib

def getInst(dbNum):
    global redisdb
    redisdb = redis.ConnectionPool(host="127.0.0.1", port=6379, db='1', password='')
    return redis.Redis(connection_pool=redisdb)


def do_auto_recharge(pipe,reward_id,reward_stock):
    """
    自动续期商品自动续期,如果超过期数则自动下架
    """
    return pipe.hset(FISH_REWARD_TABLE%(reward_id),'reward_per_stock',int(reward_stock))

def _handle_out_of_date(pipe,reward_id):
    """
    过期奖品自动下架
    """
    pipe.hset(FISH_REWARD_TABLE%(reward_id),'reward_status',0)
    pipe.lrem(FISH_REWARD_ON_SHOP_LIST,reward_id)
    return


if __name__ == '__main__':
    redis = getInst(1)
    pipe  = redis.pipeline()
    on_shop_ids = redis.lrange(FISH_REWARD_ON_SHOP_LIST,0,-1)
    auto_recharge_shops = redis.smembers(FISH_REWARD_AUTO_CHARGE)
    for on_shop_id in on_shop_ids:
        reward_per_stock,reward_stock,reward_now_nums,reward_nums = \
                redis.hmget(FISH_REWARD_TABLE%(on_shop_id),('reward_per_stock','reward_stock','reward_now_nums','reward_nums'))

        if int(reward_now_nums) >= int(reward_nums):#时间到,自动下架
            log_util.debug('[reward check] reward_id[%s] is out of date. auto remove....'%(on_shop_id))
            _handle_out_of_date(pipe,on_shop_id)

        if on_shop_id in auto_recharge_shops: #自动续期
            log_util.debug('[reward check] reward_id[%s] auto recharge[%s]->[%s]'%(on_shop_id,reward_per_stock,reward_stock))
            do_auto_recharge(pipe,on_shop_id,reward_stock)
        else:
            if int(reward_per_stock) == 0: #非自动续期的产品到0时候才自动补货
                log_util.debug('[reward check] reward_id[%s] stock is empty. system auto charge[%s]'%(on_shop_id,reward_stock))
                do_auto_recharge(pipe,on_shop_id,reward_stock)
            else:
                continue
        #期数+1
        pipe.hincrby(FISH_REWARD_TABLE%(on_shop_id),'reward_now_nums',1)
        pipe.hincrby(FISH_CONSTS_CONFIG,'exchange_shop_ver',1)
        log_util.debug('[reward check] reward_id[%s] is process complete.'%(on_shop_id))
        pipe.execute()
        print 'done'
