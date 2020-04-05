#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    DB初始化
"""

import sys
#sys.path.insert(0, 'mahjong')
sys.path.insert(0, 'server_common')
from web_db_define import *
from datetime import datetime,timedelta,time
#from admin import access_module
#from config.config import *
import redis
import hashlib

AGENT_COMPAY_RATE_DATE ='agent:%s:date:%s'

# 代理占成值集合表
AGENT_RATE_SET = 'agent:%s:rate:set'
# 钻石单价集合表
AGENT_ROOMCARD_PER_PRICE = 'agent:%s:roomcard:per:price'

def getInst(dbNum):
    global redisdb
    redisdb = redis.ConnectionPool(host="192.168.0.99", port=6379, db=dbNum, password='')
    #redisdb.connection_read_pool = redis.ConnectionPool(host="192.168.0.99", port=6000, db=dbNum, password='')
    return redis.Redis(connection_pool=redisdb)

redis = getInst(1)

#初始化管理账号
curTime = datetime.now()
pipe = redis.pipeline()

sysid = 1
# id


"""
    配置代理名称和钻石
    代理名称            ：       钻石数
"""
# print 'clean login pool...............'
# #print redis.srem(FORMAT_LOGIN_POOL_SET,'test38')
# print redis.smembers(FORMAT_LOGIN_POOL_SET)
# #redis.delete(FORMAT_LOGIN_POOL_SET)
# print 'clean success.......'

# """
# 查看捕鱼房间
# """
# print 'fish ids .........................'
# print redis.smembers(FISH_ROOM_ID_SETS)

# # print 'fish table 1'
#print redis.hgetall(FISH_ROOM_TABLE%(1))
# print redis.lrange(FISH_ROOM_LIST,0,-1)
# print redis.delete(FISH_ROOM_TABLE%('1'))
# print redis.delete(FISH_ROOM_ID_SETS)
# print redis.delete(FISH_ROOM_LIST)
# print redis.srem(GAMEID_SET,'5000')

# """
# 捕鱼投注明细
# """

# print redis.keys(ALL_FISH_BET_DATA_DETAIL%('*'))

#print redis.lrange("allFishBetDataDetail:day:2017-10-27:list",0,-1)

#print redis.keys(GM_CONTROL_DATA%('*'))

#print redis.hgetall("agentFishBetDayData:agent:363400:day:2017-11-01:hesh")

#print redis.lrange("GMControlData:uid:351:list",0,-1)



# print redis.delete(HALL_BRO_COUNT)
# print redis.delete(HALL_BRO_TABLE%("*"))
# print redis.delete(HALL_BRO_LIST)
# # print redis.delete(HALL_BRO_AG_LIST%("*"))
# for key in redis.keys(HALL_BRO_AG_LIST%('*')):
#      print redis.delete(key)
# print redis.delete(HALL_BRO_OUT_SET)
# print redis.delete(HALL_BRO_PLAY_SET)
# #print redis.smembers(GAME_DEFAULT_BIND)
# MEMBER_LIST_FIELDS = ('name','parentAg','roomCard','nickname','headImgUrl','last_login_date','last_logout_date','valid','open_auth')
# #pipe  = redis.pipeline()
# #hmset "test"
# redis_batch = redis.pipeline()
# print redis_batch.hmget("users:3075",MEMBER_LIST_FIELDS)

#print keys

#redis_batch.execute()
#AGENT_SALE_CARD_DATE

# for key in redis.keys(AGENT_TABLE%('*')):
#     agent_id = key.split(':')[2]
#     if agent_id in ['1']:
#         continue
#     print 'agentId[%s] is add to set....'%(agent_id)
#     redis.sadd(AGENT_ID_TABLE,agent_id)
#
# startDate = datetime.strptime('2017-05-01','%Y-%m-%d')
# endDate  = datetime.strptime('2017-11-30','%Y-%m-%d')
# deltaTime = timedelta(1)
# agent_ids = [1]
# pipe = redis.pipeline()
# now_time = datetime.now()
# '''
# 批量刷新玩家的总售钻和总购钻记录
# 售钻记录表 ： AGENT_SALE_CARD_DATE
# 购钻记录表 :  AGENT_BUY_CARD_DATE
# '''
# for agent_id in agent_ids:
#     print 'now setting agent_id[%s]'%(agent_id)
#     startCopyDate = startDate
#     totalBuy = 0
#     while startCopyDate <= endDate:
#         if startCopyDate > now_time:
#             startCopyDate+=deltaTime
#             continue
#         dateStr = startCopyDate.strftime('%Y-%m-%d')
#         buyReportTable = AGENT_SALE_CARD_DATE%(agent_id,dateStr)
#         if not redis.exists(buyReportTable):
#             startCopyDate+=deltaTime
#             continue
#         cardNums = redis.hget(buyReportTable,'cardNums')
#         totalBuy+=int(cardNums)
#         redis.hset(buyReportTable,'totalNums',totalBuy)
#         print 'now setting agent_id[%s] table[%s] totalBuy[%s]'%(agent_id,buyReportTable,totalBuy)
#         startCopyDate+=deltaTime
#
#     print 'agent_id[%s] set total[%s]'%(agent_id,totalBuy)
#     redis.set(AGENT_SALE_TOTAL%(agent_id),totalBuy)
#
# '''
# 生成代理日期索引
# 代理ID表 : AGENT_ID_TABLE
# 代理创建日期表 : AGENT_ID_CREATE_DATE
# '''
# AGENT_CREATE_DATE = "agent:create:date:%s"
#
# for agent_id in agent_ids:
#     agent_create_date = redis.hget(AGENT_TABLE%(agent_id),'regDate')
#     agent_create_date = agent_create_date.split(' ')[0]
#     redis.sadd(AGENT_CREATE_DATE%(agent_create_date),agent_id)
#     print 'agent_id[%s] is write to index date[%s].......'%(agent_id,agent_create_date)

FISH_REWARD_ID_COUNT = "fish:reward:id:count"
FISH_REWARD_ID_SET = "fish:reward:id:sets"
FISH_REWARD_LIST   = "fish:reward:id:list"
FISH_REWARD_TABLE  = "fish:reward:%s:info"

"""
捕鱼玩家兑换记录表
{
    'exchange_id'     :   兑换ID
    'exchange_user_id'         :   兑换玩家ID
    'exchange_reward_id'     :   兑换商品ID
    'exchange_reward_name'     :   兑换商品名称
    'exchange_reward_img_path' :   兑换商品图片
    'exchange_time'         :   兑换时间
    'exchange_use_ticket'  : 兑换使用卷
    'exchange_leave_ticket' : 兑换后剩余卷
}
"""
FISH_EXCHANGE_ID_COUNT = "fish:exchange:id:count"
FISH_EXCHANGE_LIST = "fish:exchange:list"
FISH_EXCHANGE_TABLE = "fish:exchange:item:%s:info"
'''
用户兑换索引
'''
FISH_USER_EXCHANGE_LIST = "fish:exchange:user:%s:list"
'''
兑换记录时间索引
'''
FISH_USER_EXCHANGE_DATE = 'fish:exchange:%s:date:list'

# for key in [FISH_REWARD_ID_COUNT,FISH_REWARD_ID_SET,FISH_REWARD_LIST,FISH_EXCHANGE_ID_COUNT,FISH_EXCHANGE_LIST,FISH_REWARD_ON_SHOP_LIST]:
#     print 'delete key[%s]'%(key)
#     redis.delete(key)

# for key in [FISH_REWARD_TABLE,FISH_EXCHANGE_TABLE,FISH_USER_EXCHANGE_LIST,FISH_USER_EXCHANGE_DATE]:
#     for s_key in redis.keys(key%('*')):
#         print 'delete key[%s]'%(s_key)
#         redis.delete(s_key)

# for key in redis.keys(FORMAT_USER_TABLE%('*')):
#     if 'account' in key:
#         continue
#     try:
#         print key
#         redis.hset(key,'recharge_coin_total',0)
#     except:
#         continue

# for key in redis.keys(FISH_SYSTEM_DATE_RECHARGE_TOTAL%('*')):
#     print key
#     redis.delete(key)

#redis.hset(FISH_SYSTEM_DATE_RECHARGE_TOTAL%('2017-12-06'),'recharge_coin_total',2000)



# FISH_FIRST_SHARE_PER_DAY_SET = "fish:first:share:sets"
# '''
# 待领取金币的玩家ID集合
# '''
# FISH_SHARE_NOT_TAKE_SETS = "fish:share:not:take:sets"
# '''
# 已领取金币的玩家ID集合
# '''
# FISH_SHARE_TAKE_SETS = "fish:share:take:sets"

# for key in [FISH_FIRST_SHARE_PER_DAY_SET,FISH_SHARE_NOT_TAKE_SETS,FISH_SHARE_TAKE_SETS]:
#     print key
#     redis.delete(key)



# HALL_BRO_COUNT = "hall:broadcast:count"
# HALL_BRO_TABLE = "hall:broadcast:%s:info"
# HALL_BRO_LIST  = "hall:broadcast:list:all"
# HALL_BRO_AG_LIST = "hall:broadcast:list:ag:%s"

# FISH_BRO_LIST  = "fish:broadcast:list:all"
# """
# 广播列表分类
# hall:broacast:type:%s:list
# $type 0-全服维护广播 1-全服循环广播 2-地区维护广播 3-地区循环广播
# """
# HALL_BRO_CONTAIN_ALL_LIST = "hall:broadcast:type:%s:list"
# FISH_BRO_CONTAIN_ALL_LIST = "fish:broadcast:type:%s:list"

# """
# 代理下的广播分类
# hall:broacast:type:%s:list
# $type 0-全服维护广播 1-全服循环广播 2-地区维护广播 3-地区循环广播
# """
# HALL_BRO_CONTAIN_AG_LIST = "hall:broadcast:type:%s:ag:%s:list"

# """
# 待播放广播队列
# hall:broacast:play:queue
# """
# HALL_BRO_PLAY_QUEUE = "hall:brocast:play:queue"

# """
# 过期的广播集合
# hall:broadcast:out:set
# """
# HALL_BRO_OUT_SET = "hall:bro:out:set"

# """
# 正在播放的广播集合
# hall:broadcast:out:set
# """
# HALL_BRO_PLAY_SET = "hall:bro:play:set"

# for key in redis.keys(HALL_BRO_CONTAIN_AG_LIST%('*','*')):
#     print key
#     print redis.delete(key)