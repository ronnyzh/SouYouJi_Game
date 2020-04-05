# -*- coding:utf-8 -*-
# !/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    清除未正常加入公会的账号
"""

from redis_instance import getInst

redis = getInst()

FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE = "agent:%s:member:children"
USER4AGENT_CARD = 'agent:%s:user:%s:card'

agChildenMap = {}

for _userTable in redis.scan_iter(match='users:[1-9]*'):
    userInfo = redis.hgetall(_userTable)
    uid = _userTable.split(':')[-1]
    parentAg = userInfo.get('parentAg')
    if not parentAg:
        continue
    if parentAg not in agChildenMap:
        agChildenMap[parentAg] = redis.smembers(FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE % parentAg)
    agChildens = agChildenMap[parentAg]
    isClean = False
    msg = []
    if uid not in agChildens:
        isClean = True
        msg.append('不在代理成员列表中')
    cards = redis.get(USER4AGENT_CARD % (parentAg, uid))
    if not cards:
        isClean = True
        msg.append('代理中自己钻石为:None')
    if isClean:
        print(_userTable)
        print(userInfo)
        print('cards', cards)
        print('删除原因:' + ','.join(msg))
        print('$' * 50)
        redis.hdel(_userTable, 'parentAg')
        redis.srem(FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE % parentAg, uid)
        redis.delete(USER4AGENT_CARD % (parentAg, uid))
