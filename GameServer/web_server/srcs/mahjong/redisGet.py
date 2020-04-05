# -*- coding:utf-8 -*-

# import redis_instance
import datetime
import time
import md5

import sys
reload(sys)
sys.path.insert(0, 'server_common')
import redis
sys.setdefaultencoding('utf-8')
FORMAT_REG_DATE_TABLE = "reg:date:account:%s"
FORMAT_USER_COUNT_TABLE = "users:count"
FORMAT_USER_TABLE = "users:%s"
FORMAT_ACCOUNT2USER_TABLE = "users:account:%s"
ROOM2SERVER = 'room2server:%s:hesh'
AG2SERVER = 'ag2room:ag:%s:set'

redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db='1', password="")
redis = redis.Redis(connection_pool=redis_pool)

def initAccount(account):
    curTime = datetime.datetime.now()
    curRegDateTable = FORMAT_REG_DATE_TABLE%(curTime.strftime("%Y-%m-%d"))
    #创建新的用户数据
    #id = redis.incr(FORMAT_USER_COUNT_TABLE)
    id = account.split('ping')[1]
    table = FORMAT_USER_TABLE%(id)
    pipe = redis.pipeline()
    pipe.hmset(table, 
        {
            'account'       :   account, 
            'password'      :   md5.new('ping').hexdigest(),
            'nickname'      :   account,
            'name'          :   account,
            'currency'      :   'CNY', #国家需要做微信到数据库的变换映射
            'money'         :   0.0,
            'wallet'        :   0.0,
            'vip_level'     :   0,
            'exp'           :   0,
            'level'         :   0,
            'charge'        :   0.0,
            'charge_count'  :   0,
            'game_count'    :   0,
            'coin_delta'    :   0,
            'parentAg'      :   '', #上线代理需要获得
            'email'         :   '',
            'phone'         :   '',
            'valid'         :   1,
            'last_join_ip'  :   '',
            'last_join_date':   '',
            'last_exit_ip'  :   '',
            'last_exit_date':   '',
            'last_login_ip' :   '',
            'last_login_date':  '',
            'last_logout_ip':   '',
            'last_logout_date': '',
            'last_present_date' : '',
            'newcomer_present_date' : '',
            'reg_ip'        :   '192.168.0.1',
            'reg_date'      :   curTime.strftime("%Y-%m-%d %H:%M:%S"),
            'coin'          :   0,
            'accessToken'   :   '', #以下新增
            'refreshToken'  :   '',
            'openid'        :   '',
            'sex'           :   0, #性别
            'headImgUrl'    :   '', #头像
            'unionID'       :   '',
            'province_id'   :   0,
            'playCount'     :   0,
            'like_qty'      :   0
        }
    )
    # pipe.set(WEIXIN2ACCOUNT%(openID), account) #微信ID到账号映射
    # pipe.sadd(ACCOUNT4WEIXIN_SET, account) #微信账号集合
    account2user_table = FORMAT_ACCOUNT2USER_TABLE%(account)
    pipe.set(account2user_table, table)
    # pipe.sadd(FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE%('CHNWX'), id) #上线代理需要获得
    pipe.sadd(curRegDateTable, account)
    pipe.execute()

def getAccount(account):
    account2user_table = FORMAT_ACCOUNT2USER_TABLE%(account)
    table = redis.get(account2user_table)
    print table
    print redis.hgetall(table)

def ag2room():
    num = '123457'
    ag = '113388'
    ip = '192.168.0.1'
    port = '1101'
    gameName = '海南麻将'
    dealer = '房主2号'
    type = 0
    playerCount = 1
    maxPlayer = 4
    redis.hmset(ROOM2SERVER%num, 
        {
            'ip'           :       ip,
            'port'         :       port,
            'ag'           :       ag,
            'type'         :       type,
            'gameName'     :       gameName,
            'dealer'       :       dealer, 
            'playerCount'  :       playerCount, 
            'maxPlayer'    :       maxPlayer,
            'gameid'       :       5,
        }
    )
    redis.sadd(AG2SERVER%(ag), num)

def cleanAg2room():
    for key in redis.keys(AG2SERVER%('*')):
        print key
        print redis.smembers(key)
        redis.delete(key)

#批量创建和查看账号
for num in range(3000,3500):
     account = 'ping' + str(num +1)
     initAccount(account)
     # getAccount(account)
#print getAccount('test89')

#开启的服务器列表
# for key in redis.keys(FORMAT_GAME_SERVICE_SET%('6')):
    # redis.lrem(key, 'service:game:6:CNY:192.168.0.99:10010')
    # redis.lpush(key, 'service:game:6:CNY:192.168.0.99:10010')
    # redis.delete(key)
    # print key
    # print redis.lrange(key, 0, -1)
# redis.lpush(FORMAT_GAME_SERVICE_SET%('7'), 'service:game:7:GUEST:192.168.0.155:9602')
# print redis.lrange(FORMAT_GAME_SERVICE_SET%('6'), 0, -1)

#娱乐模式等待队列
# for key in redis.keys(WAIT_JOIN_PARTY_ROOM_PLAYERS%('*', '*', '*')):
    # print key
    # print redis.lrange(key, 0, -1)
    # redis.delete(key)

#房间列表
# for key in redis.keys(ROOM2SERVER%('211618')):
    # print key
    # print redis.hgetall(key)
    # redis.delete(key)
    # gameid, ag = redis.hmget(key, ('gameid', 'ag'))
    # roomid = key.split(':')[-2]
    # if gameid == '6':
        # if roomid in redis.smembers(AG2SERVER%(ag)):
            # redis.srem(AG2SERVER%(ag), roomid)
            # print roomid
# for key in redis.keys(AG2SERVER%('135415')):
    # print key
    # print redis.smembers(key)
    # redis.delete(key)

# 退出的玩家列表
# for key in redis.keys(EXIT_PLAYER%('*')):
    # print key
    # print redis.hgetall(key)
    # redis.delete(key)

# #在线玩家列表
# print redis.smembers(ONLINE_ACCOUNTS_TABLE)
# redis.sadd(ONLINE_ACCOUNTS_TABLE, 'test32')
# redis.srem(ONLINE_ACCOUNTS_TABLE, 'test14')
# redis.delete(ONLINE_ACCOUNTS_TABLE)

#玩家钻石
# for key in redis.keys(USER4AGENT_CARD%('*','157')):
    # print key
    # print redis.set(key, 100)
    # print redis.get(key)

#游戏消耗钻石数
# for key in redis.keys(USE_ROOM_CARDS_RULE%('6')):
    # print key
    # redis.lrem(key, '8局（钻石*1）:1')
    # redis.lpush(key, '8局（钻石*1）:1')
    # for data in redis.lrange(key, 0, -1):
        # print data.decode('utf-8')

#设置数据库
# redis.hmset(GAME2REDIS%(6), {'ip':'192.168.0.99', 'port':6379, 'num':2, 'passwd':''})
# for key in redis.keys(GAME2REDIS%('*')):
    # print key
    # print redis.hgetall(key)

# print redis.delete('testRunClinetRoomSet')
