#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    更新脚本
"""
import sys
sys.path.insert(0, './mahjong')
sys.path.insert(0, './server_common')
from web_db_define import *
from datetime import datetime,timedelta,time
import redis
import hashlib
import time

def getInst(dbNum):
    global redisdb
    redisdb = redis.ConnectionPool(host="127.0.0.1", port=6379, db=dbNum, password='')
    #redisdb.connection_read_pool = redis.ConnectionPool(host="192.168.0.99", port=6000, db=dbNum, password='')
    return redis.Redis(connection_pool=redisdb)

redis = getInst(1)

FISH_HALL_2_VERS = {
    "resVersion"            :   '1',
    "minVersion"            :   '1.0.1',
    "iosMinVersion"         :   '1.0.1',
    "downloadURL"           :   "/download/hall/hall.apk",
    "IPAURL"                :   "",
    "apkSize"               :   22307533, #字节
    "apkMD5"                :   "67BD3A586E608AF76075F458AFB8056F",
    "hotUpdateURL"          :   "/download/hall/hall.zip",
    "hotUpdateScriptsURL"   :   "/download/hall/script.zip",
    "updateAndroid"         :   1,
    "updateYYB"             :   1,
    "updateAppStore1"       :   False,
    "updateAppStore2"       :   True,
    'packName'              :   'hall.zip'
}
pipe = redis.pipeline()
#################################################
###  脚本更新
#    1.商城商品按分类索引
#    2.捕鱼热更新初始化
#################################################
# GOODS_TYPE_LIST = "goods:type:%s:list"
# good_ids = redis.lrange(GOODS_LIST,0,-1)
# for good_id in good_ids:
#     print 'set goodId[%s]...'%(good_id)
#     good_type = redis.hget(GOODS_TABLE%(good_id),'type')
#     if not good_type:
#         good_type = 1
#     pipe.lpush(GOODS_TYPE_LIST%(good_type),good_id)
#
# pipe.hmset(FISH_HOTUPDATE_TABLE,FISH_HALL_2_VERS)
# pipe.execute()

###############################################################
### game字段表更新
###  新增两个字段  other_info,game_sort
###   2017-12-28
###############################################################
# update = {'other_info':'','game_sort':0}
# for key in redis.keys(GAME_TABLE%('*')):
#     if 'set' in key or 'desc' in key:
#         continue
#     print 'set game_table[%s]'%(key)
#     pipe.hmset(key,update)
# pipe.execute()

###############################################################
### fish字段表更新
###  新增1个字段  get_rate
###   2018-01-03
###############################################################
# update = {'get_rate':''}
# for key in redis.keys(FISH_ROOM_TABLE%('*')):
#     if 'set' in key or 'desc' in key:
#         continue
#     print 'set fish_table[%s]'%(key)
#     pipe.hmset(key,update)
#
# goods_lists = redis.lrange(FISH_REWARD_ON_SHOP_LIST,0,-1)
# for goods in goods_lists:
#     goods_type = redis.hget(FISH_REWARD_TABLE%(goods),'reward_type')
#     pipe.lpush(FISH_REWARD_ON_SHOP_TYPE_LIST%(goods_type),goods)
#     print 'set goods id index success....[%s]'%(goods_type)
# pipe.execute()

###############################################################
### exchange_table更新
###  新增1个字段  exchange_type
###   2018-01-03
###############################################################
total = redis.llen(FISH_EXCHANGE_LIST)
exchange_ids = redis.lrange(FISH_EXCHANGE_LIST,0,-1)

exchange_id_keys = [FISH_EXCHANGE_TABLE%(exchange_id) for exchange_id in exchange_ids]
exchange_details = [exchange_detail for exchange_detail in redis.mget(exchange_id_keys)]
exchange_info = []
for exchange_detail in exchange_details:
    exchange_detail = eval(exchange_detail)
    exchange_detail['exchange_type'] = redis.hget(FISH_REWARD_TABLE%(exchange_detail['exchange_reward_id']),'reward_type')
    pipe.set(FISH_EXCHANGE_TABLE%(exchange_detail['exchange_id']),exchange_detail)
    print 'id [%s] setType success...'%(exchange_detail['exchange_id'])

pipe.execute()

# pipe.execute()
