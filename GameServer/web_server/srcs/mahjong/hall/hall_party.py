#-*- coding:utf-8 -*-
#!/usr/bin/python

from common.log import *
from hall import hall_app
from hall_func import *
from common.utilt import *
from bottle import request, Bottle, abort, redirect, response, template,static_file
from model.partyModel import *
import time
from datetime import *
import json
"""
    大厅竞技场接口
    
"""

"""
    竞技场 & 金币场 & 比赛场 db
"""
"""
    竞技场记录id
    party:game:record:count
"""
PARTY_GAME_RECORD_COUNT_TABLE = "party:game:record:count" #
"""
    竞技场记录信息
    party:game:record:xxx-xxx-xx(年月日):xx(id) 
"""
PARTY_GAME_RECORD_TABLE = "party:game:record:%s:%s"

"""
    玩家竞技场总记录表
    party:game:record:xxx-xxx-xx(年月日):ag:account:list
    胜局记录表
    party:game:record:xxx-xxx-xx(年月日):ag:account:win:list
"""
PARTY_GAME_RECORD_ACCOUNT_TOTAL_LIST = "party:game:record:%s:%s:%s:total:list"
PARTY_GAME_RECORD_ACCOUNT_WIN_LIST = "party:game:record:%s:%s:%s:win:list"

"""
    排行榜----按工会+胜局
    有序集合
    party:game:rank:xxx-xxx-xx(年月日):ag:table
"""
PARTY_GAME_RANK_WITH_AGENT_TABLE = "party:game:rank:%s:%s:table"

"""
    战绩（流水）
    party:game:score:xxx-xxx-xx(年月日):ag:account:list
    当日竞技场钻石成绩
    party:game:roomcard:xxx-xxx-xx(年月日):ag:account
"""
# PARTY_GAME_SCORE_WITH_AGENT_LIST = "party:game:score:%s:%s:%s:list"
PARTY_GAME_ROOM_CRADS_BY_DAY = "party:game:roomcard:%s:%s:%s"

"""
    报名费 
"""
PARTY_GAME_ENTER_ROOM_CRADS = "party:game:enter:roomcard:key"

# 特殊赛场模式编号
PARTY_TYPE_COMPETITION = '1'
PARTY_TYPE_GOLD = '2'
PARTY_TYPE_MATCH = '3'

#  ----------------------------------------------   所有赛场      -----------------------------------------------

@hall_app.get('/party/status')
def onGetPartyStutus(redis,session):
    """
        获取竞技场状态
    """
    response.add_header('Access-Control-Allow-Origin', '*')
    # 用户检查
    sid = request.GET.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    picUrl, gender, groupId, isVolntExitGroup, maxScore, baseScore = \
        redis.hmget(userTable, ('headImgUrl', 'sex', 'parentAg', 'isVolntExitGroup', 'maxScore', 'baseScore'))
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    # 获取赛场类型
    partyType = request.GET.get('partyType','').strip()

    if not partyType :
        return {'code':1, 'msg': '未填写赛场类型'}

    if partyType == PARTY_TYPE_COMPETITION:
        # 竞技场开关检查
        if not is_party_comp_open(redis):
            return {'code': 1, 'msg': '模式暂未开放'}
        # 竞技场开启时间检查
        if not is_party_time(redis):
            return {'code': 1, 'msg': '本赛事还没到开放时间'}
        return {'code': 0, 'msg': '竞技场状态开放'}

    if partyType == PARTY_TYPE_GOLD :
        # 金币场
        return {'code': 0, 'msg': '金币场状态开放'}

    return {'code': 1, 'msg': '未查询到对应场次'}

#  ----------------------------------------------   竞技场      -----------------------------------------------


def get_party_roomcard_by_day(redis,groupid,account):
    """ 
        获取当日钻石成绩或消耗
    """
    today = datetime.now().strftime("%Y-%m-%d")
    count = redis.get(PARTY_GAME_ROOM_CRADS_BY_DAY % (today, groupid, account))
    return int(count)


def get_party_rate_by_day(redis,groupid,account):
    """ 
        获取比赛胜率
    """
    today = datetime.now().strftime("%Y-%m-%d")
    win = redis.llen(PARTY_GAME_RECORD_ACCOUNT_WIN_LIST % (today, groupid, account))
    total = redis.llen(PARTY_GAME_RECORD_ACCOUNT_TOTAL_LIST % (today, groupid, account))
    return win/float(total)


def get_party_score(redis,groupid,account):
    """
        获取玩家本日战绩
    """
    today = datetime.now().strftime("%Y-%m-%d")
    infos = []
    for tableid in redis.lrange(PARTY_GAME_RECORD_ACCOUNT_TOTAL_LIST % (today, groupid, account), 0, -1):
        key = PARTY_GAME_RECORD_TABLE % (today, tableid)
        date, gameid, data = redis.hmget(key,('date', 'gameid', account))
        data = eval(data)
        data['date'] = date
        data['gameid'] = gameid
        infos.append(data)
    return infos


def get_party_rank(redis,groupid,account,sortby,limit):
    """
        获取排行榜        
        日排行
        周排行
        月排行
    """
    if sortby == 'day':
        # 日排行
        pass
    elif sortby == 'week':
        # 周排行
        pass
    elif sortby == 'mouth':
        # 月排行
        pass
    today = datetime.now().strftime("%Y-%m-%d")
    rank_key = PARTY_GAME_RANK_WITH_AGENT_TABLE % (today, groupid)
    res = []
    rank = 0
    for _account, score in redis.zrevrange(rank_key,0,limit-1,True):
        rank += 1
        score = int(score)
        res.append({'rank': rank, 'nickname': _account, 'win_count': score, 'account':_account })
    if account not in [item['account'] for item in res]:
        score = redis.zscore(rank_key,account)
        if score:
            score = int(score)
            res.append({'rank': 999, 'nickname': account, 'win_count': score, 'account': account})
    return res




@hall_app.get('/party/rule')
def onGetPartyRule(redis,session):
    """
        查看竞技场页面信息
        玩法规则
    """
    response.add_header('Access-Control-Allow-Origin', '*')
    sid = request.GET.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    picUrl, gender, groupId, isVolntExitGroup, maxScore, baseScore = \
        redis.hmget(userTable, ('headImgUrl', 'sex', 'parentAg', 'isVolntExitGroup', 'maxScore', 'baseScore'))
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    timeList = get_party_time(redis)
    timeArr = []
    for item in timeList:
        timeArr.append("{0}~{1}".format(item[0][:5],(item[1] or item[0])[:5]))

    info = {
        'time':timeArr,
        'fee':'1个钻石',
    }
    msg = "竞技场开启时间：\n\n{0}\n\n需要：{1}".format('\n'.join(info['time']), info['fee']);
    return {'code':0,'msg':msg}

@hall_app.get('/party/rank')
def onGetPartyRank(redis,session):
    """
        查看竞技场排行榜
    """
    response.add_header('Access-Control-Allow-Origin', '*')
    sid = request.GET.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    picUrl, gender, groupId, isVolntExitGroup, maxScore, baseScore = \
        redis.hmget(userTable, ('headImgUrl', 'sex', 'parentAg', 'isVolntExitGroup', 'maxScore', 'baseScore'))
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    sortby = request.GET.get('sort', 'day').strip()
    limit = request.GET.get('limit', '10').strip()
    limit = int(limit)
    data = get_party_rank(redis,groupId,account,sortby,limit,)

    log_debug('*****************88888888888888888888888 {0}'.format(data))
    return {'code': 0, 'msg': '','data': data}


@hall_app.get('/party/score')
def onGetPartyScore(redis,session):
    """
        查看竞技场页面信息
        本日战绩
    """
    response.add_header('Access-Control-Allow-Origin', '*')
    sid = request.GET.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    picUrl, gender, groupId, isVolntExitGroup, maxScore, baseScore = \
        redis.hmget(userTable, ('headImgUrl', 'sex', 'parentAg', 'isVolntExitGroup', 'maxScore', 'baseScore'))
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    infos = get_party_score(redis,groupId,account)
    rate = get_party_rate_by_day(redis,groupId,account)
    roomcard = get_party_roomcard_by_day(redis,groupId,account)
    data = {
        'content':infos,
        'rate': rate,
        'score': roomcard
    }
    return {'code': 0, 'msg': '', 'data': data}



#  ----------------------------------------------   金币场      -----------------------------------------------

@hall_app.post('/party/gold/gameList')
def getPartyGoldGameList(redis,session):
    """
    获取金币场场次列表
    """
    response.add_header('Access-Control-Allow-Origin', '*')
    sid = request.POST.get('sid', '').strip()

    data = get_GoldGameList(redis)
    return {'code': 0, 'msg': '金币场场次列表获取成功','data':data}



#  ----------------------------------------------   福利系统      -----------------------------------------------

@hall_app.post('/welfare/info')
def getWelfareInfo(redis, session) :
    """获取是否签到、低保"""
    response.add_header('Access-Control-Allow-Origin', '*')
    sid = request.forms.get('sid', '').strip()

    # return
    log_debug('********getPartyGoldInfo sid %s'.format(sid))

    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    coin = get_PlayerWelfareInfo(redis,account)
    res = {'coin': coin,'isSign':False,'isInsurance':True,'mession':[]}
    return {'code': 0 , 'msg' : '金币信息获取成功','data' :res}

@hall_app.post('/welfare/sign')
def doWelfareSign(redis, session):
    """签到"""
    response.add_header('Access-Control-Allow-Origin', '*')
    sid = request.forms.get('sid', '').strip()

    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    res = do_PlayerWelfareSign(redis, uid, account)

    # log_debug('********doWelfareSign sid {0} do_PlayerWelfareSign {1}'.format(sid,res))

    if not res :
        return {'code': 1, 'msg': "今日已签到"}
    else:
        return {'code': 0, 'msg': "签到成功,获得 {0} 金币".format(res)}


@hall_app.post('/welfare/insurance')
def doWelfareInsurancen(redis, session):
    """低保"""
    response.add_header('Access-Control-Allow-Origin', '*')
    sid = request.forms.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    res = do_PlayerWelfareInsurance(redis,uid, account)

    return res

@hall_app.post('/welfare/coin/GMSet')
def checkWelfareIsGM(redis, session):
    """设置该玩家金币 正式环境请删除本函数"""
    response.add_header('Access-Control-Allow-Origin', '*')
    sid = request.forms.get('sid', '').strip()
    coinNum = request.forms.get('coinNum', '').strip()

    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    isNumber = all(c in "0123456789.+-" for c in coinNum)

    if not coinNum or not isNumber:
        return {'code':1,'msg':'输入值错误'}


    res = do_PlayerCoin(redis, 'to', uid, account, coinNum, 'gm设置')
    if not res :
        log_debug('--------------[errror]checkWelfareIsGM account-coinNum :{0}-{1}'.format(account, coinNum))
        return {'code':1,'msg':'设置金币失败'}
    return {'code':0,'msg':'设置金币成功'}




#  ----------------------------------------------   任务      -----------------------------------------------

@hall_app.post('/mession/day/list')
def getMessionDayList(redis, session):
    """每日任务"""
    response.add_header('Access-Control-Allow-Origin', '*')
    sid = request.forms.get('sid', '').strip()
    # return
    log_debug('********getPartyGoldInfo sid %s'.format(sid))


    return {'code':0,'msg':""}

