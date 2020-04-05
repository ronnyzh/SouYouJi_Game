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
sys.path.insert(0, 'server_common')
sys.path.insert(0, 'mahjong')
from web_db_define import *
from datetime import datetime,time
from admin import access_module
from config.config import *
import redis
import hashlib


serverList = [
        'http://192.168.0.99:9797',
        'http://192.168.0.18:9797',
        'http://192.168.0.155:9797'
]

def getInst(dbNum):
    global redisdb
    redisdb = redis.ConnectionPool(host="192.168.0.99", port=6379, db='1', password='')
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
agentDict = {
        'id'                    :           sysid,
        'account'               :           'sysadmin',
        'passwd'                :           hashlib.sha256('sysadmin').hexdigest(),
        'name'                  :           'dawei',
        'shareRate'             :           0.5,
        'valid'                 :            1,
        'roomcard_id'           :           0,
        'parent_id'             :           0,
        'roomcard'              :           0,
        'regIp'                 :           '127.0.0.1',
        'regDate'               :           1,
        'lastLoginIP'           :           1,
        'lastLoginDate'         :           1,
        'isCreate'              :           1,
        'type'                  :           0
}

# accessTable = AGENT2ACCESS%(sysid)
# for accessObj in access_module.ACCESS_SADMIN_MODULES:
#     pipe.sadd(accessTable, accessObj.url)

adminTable = AGENT_TABLE%(sysid)
admimtoIdTalbel = AGENT_ACCOUNT_TO_ID%('sysadmin')
print pipe.hmset(adminTable,agentDict)
pipe.set(admimtoIdTalbel,sysid)
print 'create sysadmin[%s] success.'%(adminTable)

pipe.hmset(HOTUPDATE_TABLE,HALL2VERS)
pipe.execute()
print 'creare Done.........'

# if redis.exists(FORMAT_HALL_SERVICE_SET):
#     redis.delete(FORMAT_HALL_SERVICE_SET)

# for server in serverList:
#     pipe.sadd(FORMAT_HALL_SERVICE_SET,server)

# pipe.execute()
# print redis.smembers(FORMAT_HALL_SERVICE_SET)

# redis.delete(FORMAT_GAMEHALL_NOTIC_LIST_TABLE)
# redis.delete(FORMAT_GAMEHALL_NOTIC_COUNT_TABLE)
# for key in redis.keys(FORMAT_GAMEHALL_NOTIC_TABLE%('*')):
#     print key
#     redis.delete(key)

# for key in redis.keys(FORMAT_MGR_SEND_MESSAGE_LIST%('*')):
#     print key
#     redis.delete(key)

# for key in redis.keys(FORMAT_USER_MESSAGE_LIST%('*')):
#     print key
#     redis.delete(key)

# for key in redis.keys(FORMAT_USER_UNREAD_MESSAGE%('*')):
#     print key
#     redis.delete(key)

# for key in redis.keys(FORMAT_MGR_SEND_MESSAGE_LIST%('*')):
#     print key
#     redis.delete(key)

# for key in redis.keys(FORMAT_MSG_READ_SET%('*')):
#     print key
#     redis.delete(key)

# for key in redis.keys(FORMAT_GAMEHALL_NOTIC_TABLE%('*')):
#     print key
#     redis.delete(key)

# for key in redis.keys(FORMAT_USER_MESSAGE_LIST%('*')):
#     print key
#     redis.delete(key)

删除公告脚本
listss = redis.lrange(FORMAT_GAMEHALL_NOTIC_LIST_TABLE,0,-1)
for lists in listss:
    ahInfo = redis.hgetall(FORMAT_GAMEHALL_NOTIC_TABLE%(lists))
    if ahInfo['status'] == '0':
        print 'delete.......[%s]'%(lists)
        redis.lrem(FORMAT_GAMEHALL_NOTIC_LIST_TABLE,lists)


