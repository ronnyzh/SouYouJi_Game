#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
批量添加GM用户
'''
'只能通过uid创建,也能通过account创建'

import requests

# 服务器地址

from redis_instance import getInst
from datetime import datetime

redis = getInst(1)

FORMAT_USER_TABLE = "users:%s"
FORMAT_ACCOUNT2USER_TABLE = "users:account:%s"
AGENT_OP_COUNT = 'agent:op:count'
AGENT_OP_LOG_TABLE = 'agent:%s:op:log'
AGENT_OP_LOG_DATESET_TABLE = 'agent:%s:op:log:dateset:%s'

'''-----配置区(开始)-----'''
# 想要赋予GM权限的用户id
TmpUids = []
# 批量区间赋予GM权限
TmpUidsNums = (0, 0)  # (1,101),就是设置1-100的uid
# 想要赋予GM权限的用户account
TmpAccounts = []
'''-----配置区(结束)-----'''


def writeAgentOpLog(redis, agentId, logInfo):
    """
    写操作日志
    @params:
        redis     redis实例
        agentId   操作代理ID
        date      操作日期
        desc      操作记录描述
    """
    dateStr = datetime.now().strftime('%Y-%m-%d')
    logId = redis.incr(AGENT_OP_COUNT)
    logTable = AGENT_OP_LOG_TABLE % (logId)
    agentLogTable = AGENT_OP_LOG_DATESET_TABLE % (agentId, dateStr)
    pipe = redis.pipeline()
    pipe.hmset(logTable, logInfo)
    pipe.lpush(agentLogTable, logId)
    pipe.execute()


def addGM(accountNo, uid='', adminUid=1):
    gmTable = 'GMAccount:set'
    if redis.sismember(gmTable, accountNo):
        print('会员[%s][uid:%s]已经拥有gm权限' % (accountNo, uid))
        return
    redis.sadd(gmTable, accountNo)  # 上线代理需要获得
    logInfo = {
        'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ip': '127.0.0.1',
        'desc': '给玩家[%s]设置gm权限(脚本添加)' % (accountNo)
    }
    writeAgentOpLog(redis, adminUid, logInfo)
    print('给玩家[%s]设置gm权限(脚本添加)' % (accountNo))


def do():
    TmpUids.extend(range(*TmpUidsNums))
    for _uid in TmpUids:
        userTable = FORMAT_USER_TABLE % (_uid)
        if not redis.exists(userTable):
            print('会员id[%s]不存在' % (_uid))
            continue
        account = redis.hget(userTable, 'account')
        addGM(accountNo=account, uid=_uid)
    for _account in TmpAccounts:
        accountTable = FORMAT_ACCOUNT2USER_TABLE % (_account)
        if not redis.exists(accountTable):
            print('会员account[%s]不存在' % (_account))
            continue
        addGM(accountNo=_account)


if __name__ == '__main__':
    do()
