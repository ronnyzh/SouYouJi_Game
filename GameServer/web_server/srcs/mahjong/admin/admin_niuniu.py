#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    活动设置模块
"""
from bottle import *
from admin import admin_app
from config.config import STATIC_LAYUI_PATH,STATIC_ADMIN_PATH,BACK_PRE,RES_VERSION
from common.utilt import *
from common.log import *
from datetime import datetime
from web_db_define import *
from model.niuniuModel import *
from urlparse import urlparse
from access_module import *
import hashlib
import json
import traceback
import copy
import time
import redis
#
# 页面输出
#


"""
    经典牛牛GAMEID
"""
NIUNIU_GAMEID_1 = '5'

def select_report(request):
    """根据url判断牛牛类型"""
    lang = getLang()
    # report  1:经典牛牛  2：明牌牛牛
    o = urlparse(request.url)
    report = "1" if o.path.find("_op1") != -1 else "2"
    report = request.GET.get("report", report)
    title = lang.MENU_NIUNIU_ONE_TXT if report == "1" else lang.MENU_NIUNIU_TWO_TXT

    return report,title


def getPrivateRedisInst(redisdb, gameid):
    """
        获取redis连接实例
    """
    try:
        if not redisdb.exists(GAME2REDIS % gameid):
            return None
        info = redisdb.hgetall(GAME2REDIS % gameid)
        ip = info['ip']
        passwd = info['passwd']
        port = int(info['port'])
        dbnum = int(info['num'])
        redisdb = redis.ConnectionPool(host=ip, port=port, db=dbnum, password=passwd)
        return redis.Redis(connection_pool=redisdb)
    except:
        traceback.print_exc()
        return None


@admin_app.get('/niuniu/kefu')
def getKefuIndex(redis,session):
    """
    牛牛客服
    """
    lang = getLang()

    # 权限
    agentId = session['id']
    creatAgUrl = BACK_PRE + '/niuniu/reward_journal'
    if creatAgUrl in redis.smembers(AGENT2ACCESSBAN % (agentId)):
        createAg = '0'
    else:
        createAg = '1'

    # report  1:经典牛牛  2：明牌牛牛
    report, title = select_report(request)
    gotoTitle = "跳转明牌牛牛" if report == 1 else "跳转经典牛牛"
    gotoReport = 2 if report == 1 else 1

    info = {
        "gotoTitle" : gotoTitle,
        "gotoUrl": BACK_PRE + "/niuniu/kefu?report=%s" % gotoReport,
        "title": title + lang.MENU_NIUNIU_KEFU,
        "tableUrl": BACK_PRE + "/niuniu/kefu?report=%s&list=%s" % (report, 1),
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'searchTxt': 'uid',
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + "/niuniu/index?report=" + report,
        'createAccess': createAg,
    }
    return template('admin_niuniu_kefu', info=info, lang=lang, RES_VERSION=RES_VERSION)







def getNiuniuOperateList(redis, start_date, end_date):
    """
        获取某个时间段牛牛运营报表

    """
    try:
        startDate = datetime.strptime(start_date, '%Y-%m-%d')
        endDate = datetime.strptime(end_date, '%Y-%m-%d')
    except:
        weekDelTime = timedelta(7)
        weekBefore = datetime.now() - weekDelTime
        startDate = weekBefore
        endDate = datetime.now()

    deltaTime = timedelta(1)
    res = []
    while startDate <= endDate:
        dateStr = startDate.strftime('%Y-%m-%d')
        if redis.exists(NIUNIU_GAME_OPERATE_BY_DAY_TABLE % dateStr):
            info = redis.hgetall(NIUNIU_GAME_OPERATE_BY_DAY_TABLE % dateStr)
            info['date'] = dateStr
            info['op'] = []
            info['op'].append({'url': '/admin/niuniu/tile_type_op1?list=1', 'method': 'GET', 'txt': '查看牌型统计表'})
            res.append(info)
        startDate += deltaTime
    res.reverse()
    return res


@admin_app.get('/niuniu/index')
@admin_app.get('/niuniu/operate')
@admin_app.get('/niuniu/operate_op1')
@admin_app.get('/niuniu/operate_op2')
def getNiuniuOperate(redis,session):
    """
        牛牛运营表
    """
    # report  1:经典牛牛  2：明牌牛牛
    report, title = select_report(request)
    lang = getLang()
    isList = request.GET.get('list','').strip()
    start_date = request.GET.get('startDate','').strip()
    end_date = request.GET.get('endDate','').strip()
    if isList:
        res = []
        redis = getPrivateRedisInst(redis,NIUNIU_GAMEID_1)
        if redis:
            res = getNiuniuOperateList(redis, start_date, end_date)
        return {'code': 0, 'data': res}
    agentId = session['id']
    creatAgUrl = BACK_PRE + '/niuniu/operate'
    if creatAgUrl in redis.smembers(AGENT2ACCESSBAN % agentId):
        createAg = '0'
    else:
        createAg = '1'
    info = {
        "title"                 :   title + lang.MENU_NIUNIU_OPERATE,
        "tableUrl"              :    BACK_PRE+"/niuniu/operate?report=%s&list=%s" % (report, 1),
        'STATIC_LAYUI_PATH'     :   STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'     :   STATIC_ADMIN_PATH,
        'back_pre'              :   BACK_PRE,
        'backUrl'               :   BACK_PRE+"/niuniu/index?report=" + report,
        'createAccess'          :   createAg,
    }
    return template('admin_niuniu_operate',info=info,lang=lang,RES_VERSION=RES_VERSION)


def getNiuniuTileTypeList(redis, start_date, end_date):
    """
        获取某个时间段牛牛牌型统计表
    """
    try:
        startDate = datetime.strptime(start_date, '%Y-%m-%d')
        endDate = datetime.strptime(end_date, '%Y-%m-%d')
    except:
        weekDelTime = timedelta(7)
        weekBefore = datetime.now() - weekDelTime
        startDate = weekBefore
        endDate = datetime.now()

    deltaTime = timedelta(1)
    res = []
    while startDate <= endDate:
        dateStr = startDate.strftime('%Y-%m-%d')
        if redis.exists(NIUNIU_GAME_OPERATE_BY_DAY_TABLE % dateStr):
            info = redis.hgetall(NIUNIU_GAME_OPERATE_BY_DAY_TABLE % dateStr)
            info['date'] = dateStr
            info['op'] = []
            total = 0
            for k,v in info.iteritems():
                if k[:5] == 'bull_':
                    total += int(v)
            info['total'] = total
            res.append(info)
        startDate += deltaTime
    res.reverse()
    return res


@admin_app.get('/niuniu/tile_type')
@admin_app.get('/niuniu/tile_type_op1')
@admin_app.get('/niuniu/tile_type_op2')
def getNiuniuTileType(redis,session):
    """
    牛牛牌型统计表
    """
    # report  1:经典牛牛  2：明牌牛牛
    report, title = select_report(request)
    lang = getLang()
    isList = request.GET.get('list','').strip()
    start_date = request.GET.get('startDate','').strip()
    end_date = request.GET.get('endDate','').strip()
    if isList:
        res = []
        redis = getPrivateRedisInst(redis,NIUNIU_GAMEID_1)
        if redis:
            res = getNiuniuTileTypeList(redis, start_date, end_date)
        return {'code': 0, 'data': res}
    agentId = session['id']
    creatAgUrl = BACK_PRE + '/niuniu/tile_type'
    if creatAgUrl in redis.smembers(AGENT2ACCESSBAN % agentId):
        createAg = '0'
    else:
        createAg = '1'
    info = {
        "title": title + lang.MENU_NIUNIU_TILE_TYPE,
        "tableUrl": BACK_PRE + "/niuniu/tile_type?report=%s&list=%s" % (report, 1),
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + "/niuniu/index?report=" + report,
        'createAccess': createAg,
    }
    return template('admin_niuniu_tile_type', info=info, lang=lang, RES_VERSION=RES_VERSION)


def getNiuniuJournalList(redis, start_date, end_date):
    """
        获取某个时间段数据流水
    """
    try:
        startDate = datetime.strptime(start_date, '%Y-%m-%d')
        endDate = datetime.strptime(end_date, '%Y-%m-%d')
    except:
        weekDelTime = timedelta(7)
        weekBefore = datetime.now() - weekDelTime
        startDate = weekBefore
        endDate = datetime.now()

    deltaTime = timedelta(1)
    res = []
    try:
        while startDate <= endDate:
            dateStr = startDate.strftime('%Y-%m-%d')
            for key in redis.keys(NIUNIU_GAME_RECORD_TABLE % (dateStr, '*')):
                info = redis.hgetall(key)
                if not info.get('start_time', '0'):
                    continue
                info['recordId'] = key.split(':')[4]
                info['op'] = []
                info['start_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(info['start_time'])/1000))
                info['end_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(info['end_time'])/1000))
                res.append(info)
            startDate += deltaTime
        res = sorted(res, key=lambda s: int(s.get('recordId', '0')),reverse=True)
    except:
        traceback.print_exc()
    return res


@admin_app.get('/niuniu/journal')
@admin_app.get('/niuniu/journal_op1')
@admin_app.get('/niuniu/journal_op2')
def getNiuniuJournal(redis,session):
    """
        牛牛游戏数据流水
    """
    report, title = select_report(request)
    lang = getLang()
    isList = request.GET.get('list','').strip()
    start_date = request.GET.get('startDate','').strip()
    end_date = request.GET.get('endDate','').strip()
    if isList:
        res = []
        redis = getPrivateRedisInst(redis,NIUNIU_GAMEID_1)
        if redis:
            res = getNiuniuJournalList(redis, start_date, end_date)
        return {'code': 0, 'data': res}
    agentId = session['id']
    creatAgUrl = BACK_PRE + '/niuniu/journal'
    if creatAgUrl in redis.smembers(AGENT2ACCESSBAN % agentId):
        createAg = '0'
    else:
        createAg = '1'
    info = {
        "title": title + lang.MENU_NIUNIU_JOURNAL,
        "tableUrl": BACK_PRE + "/niuniu/journal?report=%s&list=%s" % (report, 1),
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + "/niuniu/index?report=" + report,
        'createAccess': createAg,
    }
    return template('admin_niuniu_journal', info=info, lang=lang, RES_VERSION=RES_VERSION)



def getNiuniuStatisList(redis, account):
    """
        获取牛牛账号统计数据
    """
    res = []
    if account:
        info = redis.hgetall(NIUNIU_ACCOUNT_STACTICS_TABLE % account)
        if info:
            info['op'] = []
            res.append(info)
        return {'total': len(res), 'result': res}
    for account in redis.smembers(NIUNIU_ACCOUNT_SET_TOTAL):
        info = redis.hgetall(NIUNIU_ACCOUNT_STACTICS_TABLE % account)
        if info:
            info['op'] = []
            info['op'].append({'url': '/admin/niuniu/reward_journal_op1?list=1', 'method': 'GET', 'txt': '奖励记录'})
            info['op'].append({'url': '/admin/niuniu/get_cash_journal_op1?list=1', 'method': 'GET', 'txt': '提现记录'})
            info['op'].append({'url': '/admin/niuniu/set_cash_journal_op1', 'method': 'GET', 'txt': '清零'})
            res.append(info)
    return {'total': len(res), 'result': res}


@admin_app.get('/niuniu/draw_statis')
@admin_app.get('/niuniu/draw_statis_op1')
@admin_app.get('/niuniu/draw_statis_op2')
def getNiuniuStatis(redis,session):
    """
        牛牛活动客服查询表
    """
    report, title = select_report(request)
    lang = getLang()
    isList = request.GET.get('list','').strip()
    search_account = request.GET.get('searchText','').strip()
    if isList:
        res = {'total': 0, 'result': []}
        redis = getPrivateRedisInst(redis,NIUNIU_GAMEID_1)
        if redis:
            res = getNiuniuStatisList(redis, search_account)
        return json.dumps(res)
    agentId = session['id']
    creatAgUrl = BACK_PRE + '/niuniu/draw_statis'
    if creatAgUrl in redis.smembers(AGENT2ACCESSBAN % agentId):
        createAg = '0'
    else:
        createAg = '1'

    info = {
        "title": title + lang.MENU_NIUNIU_DRAW_STATIS,
        "listUrl": BACK_PRE + "/niuniu/draw_statis?report=%s&list=%s" % (report, 1),
        'searchTxt': 'uid',
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + "/niuniu/index?report=" + report,
        'createAccess': createAg,
    }
    return template('admin_niuniu_draw_statis', info=info, lang=lang, RES_VERSION=RES_VERSION)


def getNiuniuRewardStatisList(redis, start_date, end_date):
    """
        获取某个时间段牛牛奖励统计数据
    """
    try:
        startDate = datetime.strptime(start_date, '%Y-%m-%d')
        endDate = datetime.strptime(end_date, '%Y-%m-%d')
    except:
        weekDelTime = timedelta(7)
        weekBefore = datetime.now() - weekDelTime
        startDate = weekBefore
        endDate = datetime.now()
    deltaTime = timedelta(1)
    res = []
    while startDate <= endDate:
        dateStr = startDate.strftime('%Y-%m-%d')
        if redis.exists(NIUNIU_GAME_OPERATE_BY_DAY_TABLE % dateStr):
            info = redis.hgetall(NIUNIU_GAME_OPERATE_BY_DAY_TABLE % dateStr)
            info['date'] = dateStr
            info['op'] = []
            res.append(info)
        startDate += deltaTime
    res.reverse()
    return res


@admin_app.get('/niuniu/reward_statis')
@admin_app.get('/niuniu/reward_statis_op1')
@admin_app.get('/niuniu/reward_statis_op2')
def getNiuniuRewardStatisJournal(redis,session):
    """
        牛牛奖励统计表
    """
    report, title = select_report(request)
    lang = getLang()
    isList = request.GET.get('list','').strip()
    start_date = request.GET.get('startDate','').strip()
    end_date = request.GET.get('endDate','').strip()
    if isList:
        res = []
        redis = getPrivateRedisInst(redis,NIUNIU_GAMEID_1)
        if redis:
            res = getNiuniuRewardStatisList(redis, start_date, end_date)
        return {'code': 0, 'data': res}
    agentId = session['id']
    creatAgUrl = BACK_PRE + '/niuniu/reward_statis'
    if creatAgUrl in redis.smembers(AGENT2ACCESSBAN % agentId):
        createAg = '0'
    else:
        createAg = '1'

    info = {
        "title": title + lang.MENU_NIUNIU_REWARD_STATIS,
        "tableUrl": BACK_PRE + "/niuniu/reward_statis?report=%s&list=%s" % (report, 1),
        'searchTxt': 'uid',
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + "/niuniu/index?report=" + report,
        'createAccess': createAg,
    }
    return template('admin_niuniu_reward_statis', info=info, lang=lang, RES_VERSION=RES_VERSION)

@admin_app.get('/niuniu/get_cash_journal')
@admin_app.get('/niuniu/get_cash_journal_op1')
@admin_app.get('/niuniu/get_cash_journal_op2')
def getNiuniuJournal(redis,session):
    """
    牛牛提现记录表
    """
    lang = getLang()

    # 权限
    agentId = session['id']
    creatAgUrl = BACK_PRE + '/niuniu/get_cash_journal'
    if creatAgUrl in redis.smembers(AGENT2ACCESSBAN % (agentId)):
        createAg = '0'
    else:
        createAg = '1'

    # report  1:经典牛牛  2：明牌牛牛
    report, title = select_report(request)

    info = {
        "title": title + lang.MENU_NIUNIU_GET_CASH_JOURNAL,
        "tableUrl": BACK_PRE + "/niuniu/get_cash_journal?report=%s&list=%s" % (report, 1),
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + "/niuniu/index?report=" + report,
        'createAccess': createAg,
    }
    return template('admin_niuniu_get_cash_journal.tpl', info=info, lang=lang, RES_VERSION=RES_VERSION)

@admin_app.get('/niuniu/reward_journal')
@admin_app.get('/niuniu/reward_journal_op1')
@admin_app.get('/niuniu/reward_journal_op2')
def getNiuniuJournal(redis,session):
    """
        牛牛奖励流水表
    """
    lang = getLang()

    # 权限
    agentId = session['id']
    creatAgUrl = BACK_PRE + '/niuniu/reward_journal'
    if creatAgUrl in redis.smembers(AGENT2ACCESSBAN % (agentId)):
        createAg = '0'
    else:
        createAg = '1'

    # report  1:经典牛牛  2：明牌牛牛
    report, title = select_report(request)

    info = {
        "title": title + lang.MENU_NIUNIU_REWARD_JOURNAL,
        "tableUrl": BACK_PRE + "/niuniu/reward_journal?report=%s&list=%s" % (report, 1),
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'searchTxt': 'uid',
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + "/niuniu/index?report=" + report,
        'createAccess': createAg,
    }
    return template('admin_niuniu_reward_journal', info=info, lang=lang, RES_VERSION=RES_VERSION)
