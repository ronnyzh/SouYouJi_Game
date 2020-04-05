# -*- coding:utf-8 -*-
# !/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    DB初始化
"""

import sys
import hashlib

sys.path.insert(0, '../server_common')
sys.path.insert(0, '../mahjong')
sys.path.insert(0, '..')
from server_common.web_db_define import *
from mahjong.admin import access_module
from redis_instance import getInst

redis = getInst(1)
pipe = redis.pipeline()
sysid = 1

'''-----配置区(开始)-----'''
agentDict = {
    'id': sysid,
    'account': 'sysadmin',
    'passwd': hashlib.sha256('sysadmin').hexdigest(),
    'name': 'winslen',
    'shareRate': 0.5,
    'valid': 1,
    'roomcard_id': 0,
    'parent_id': 0,
    'roomcard': 0,
    'regIp': '127.0.0.1',
    'regDate': 1,
    'lastLoginIP': 1,
    'lastLoginDate': 1,
    'isCreate': 1,
    'type': 0
}
'''-----配置区(结束)-----'''


def do():
    accessTable = AGENT2ACCESS % (sysid)
    for accessObj in access_module.ACCESS_SADMIN_MODULES:
        pipe.sadd(accessTable, accessObj.url)
    adminTable = AGENT_TABLE % (sysid)
    admimtoIdTalbel = AGENT_ACCOUNT_TO_ID % ('sysadmin')
    print pipe.hmset(adminTable, agentDict)
    pipe.set(admimtoIdTalbel, sysid)
    print 'create sysadmin[%s] success.' % (adminTable)
    pipe.execute()
    print 'creare Done.........'


if __name__ == '__main__':
    do()
