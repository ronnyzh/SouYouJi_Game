# -*- coding:utf-8 -*-
# !/usr/bin/python

"""
     消消乐模块
"""

from hall import hall_app
from hall_func import getUserByAccount
from common.utilt import *
from bottle import request, response, template, static_file
from common import web_util
from model.xiaoxiaoleModel import *
import ast
import traceback
import json
import copy
import urllib

ODDS = {
    1: {
        3: 1, 4: 2, 5: 3, 6: 4,
        7: 5, 6: 8, 7: 9,
        'default': 11,
    },
    2: {
        3: 2, 4: 3, 5: 4, 6: 5,
        7: 6, 8: 7, 9: 8,
        'default': 12,
    },
    3: {
        3: 3, 4: 4, 5: 5, 6: 6,
        7: 7, 8: 8, 9: 9,
        'default': 13,
    },
    4: {
        3: 4, 4: 5, 5: 6, 6: 7,
        7: 8, 8: 9, 9: 10,
        'default': 14,
    },
    5: {
        3: 5, 4: 6, 5: 7, 6: 8,
        7: 9, 8: 10, 9: 11,
        'default': 15,
    },
}
# 比例
Proportion = 1


@hall_app.get('/xiaoxiaole/setting')
@web_util.allow_cross_request
def xiaoxiaole_setting(redis, session):
    uid = request.GET.get('uid', '').strip()
    sid = request.GET.get('sid', '').strip()
    if not uid:
        if not sid:
            return {'code': -5, 'msg': '该用户不存在'}
        SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
        userTable = getUserByAccount(redis, account)
        uid = userTable.split(':')[-1]
    else:
        userTable = 'users:%s' % (uid)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    gold = int(redis.hget('users:%s' % (uid), 'gold') or 0)
    return {'code': 0, 'gameinfo': ODDS, 'max': int(gold / Proportion), 'money': 'gold'}


@hall_app.get('/xiaoxiaole/run')
@web_util.allow_cross_request
def xiaoxiaole_run(redis, session):
    uid = request.GET.get('uid', '').strip()
    sid = request.GET.get('sid', '').strip()
    if not uid:
        if not sid:
            return {'code': -5, 'msg': '该用户不存在'}
        SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
        userTable = getUserByAccount(redis, account)
        uid = userTable.split(':')[-1]
    else:
        userTable = 'users:%s' % (uid)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    bets = ast.literal_eval(request.GET.get('bets', '{}').strip())
    print '/xiaoxiaole/run',uid, bets
    try:
        bets = urllib.unquote(bets)
    except:
        traceback.print_exc()

    if not isinstance(bets, dict):
        return {'code': -1, 'msg': u'参数错误'}

    nickname, gold = redis.hmget(userTable, ('nickname', 'gold'))
    print u'开始金币', gold

    totalPayGold = sum(bets.values())
    print 'totalPayGold', totalPayGold
    print u'扣除金币', totalPayGold

    if not gold or int(totalPayGold) > int(gold):
        return {'code': -1, 'msg': u'金币不足'}

    redis.hincrby(userTable, 'gold', -totalPayGold)
    Mgr = xiaoxiaoleMgr()
    results = Mgr.run()

    datas = []
    winScore = 0
    for _result in results:
        numtype = int(_result["type"])
        numlen = int(_result["len"])
        rep = {
            'score': (bets.get(numtype, 0) or bets.get(str(numtype), 0)) * getOdds(numtype, numlen),
            'len': numlen,
            'coordinates': _result["coordinates"],
            'type': numtype,
        }
        winScore += rep["score"]
        print rep
        datas.append(rep)
    matrix = Mgr.getCanvas().tolist()

    redis.hincrby(userTable, 'gold', winScore)
    print u'增加金币', winScore
    print datas
    gold = redis.hget(userTable, 'gold')
    print u'剩余金币', gold
    return {'code': 0, 'msg': u'成功', 'winScore': winScore, 'matrix': matrix, 'datas': datas, 'money': 'gold', 'gold_coin': gold}


def getOdds(type, count):
    type = int(type)
    count = int(count)
    if count not in ODDS[type]:
        return ODDS[type]['default']
    else:
        return ODDS[type][count]
