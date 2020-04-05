# -*- coding:utf-8 -*-
# !/usr/bin/python

"""
        比赛场模块
"""

from bottle import *
from admin import admin_app
from config.config import STATIC_LAYUI_PATH, STATIC_ADMIN_PATH, BACK_PRE, RES_VERSION
from common.utilt import *
from common.log import *
from datetime import datetime
from web_db_define import *
from model.protoclModel import *
from model.gameModel import getGameServersById
from model.goldModel import *
from common.mysql_util import MysqlInterface
from access_module import *
from common import encrypt_util, convert_util, json_util, web_util
from model.matchModel import *
import hashlib
import json
import traceback
import requests
from db_define.db_define_consts import *
from db_define.db_define_redis_key import *


@admin_app.get('/match/list')
def getMatchList(redis, session):
    """
        比赛场列表
    """
    lang = getLang()
    isList = request.GET.get('isList', '').strip()
    if isList:
        res = []
        match_set = redis.smembers(MATCH_SET)
        for gameId in match_set:
            gameId_res = []
            match_game_set = MATCH_GAME_SET % gameId
            for matchId in redis.smembers(match_game_set):
                match_game_TABLE = MATCH_GAME_ID_TABLE % (gameId, matchId)
                match_game_info = redis.hgetall(match_game_TABLE)
                gameservers = (getGameServersById(redis, gameId))
                match_game_info['server'] = '<br>'.join(server.get('serverUrl', '') for server in gameservers)
                match_game_info['fee'] = '%s' % (match_game_info['fee'])
                match_game_info['op'] = [
                    {'url': BACK_PRE + '/match/introSetting', 'txt': '比赛规则', 'method': 'GET'},
                    {'url': BACK_PRE + '/match/modify', 'txt': '修改', 'method': 'POST'},
                    {'url': BACK_PRE + '/match/delete', 'txt': '删除', 'method': 'POST'},
                    {'url': BACK_PRE + '/match/display', 'txt': '关闭可见' if match_game_info['display'] == '1' else '开启可见',
                     'method': 'POST'},
                    {'url': BACK_PRE + '/match/enroll_status',
                     'txt': '关闭报名' if match_game_info['enroll_status'] == '1' else '开启报名', 'method': 'POST'},
                ]
                if int(match_game_info['enrollNum']) > 0:
                    match_game_info['op'].append(
                        {'url': BACK_PRE + '/match/enrollUsers_delete', 'txt': '取消该赛事报名', 'method': 'POST'})
                match_game_info['matchtype'] = Define_Currency.getCurrencyName(match_game_info['matchtype'])
                match_game_info['feetype'] = Define_Currency.getCurrencyName(match_game_info['feetype'])
                gameId_res.append(match_game_info)
            gameId_res = sorted(gameId_res, key=lambda x: x['id'])
            res.extend(gameId_res)
        # res = get_match_list(redis)
        return json.dumps(res)
    else:
        info = {
            'title': "比赛场列表",
            'addTitle': "创建新比赛",
            'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
            'tableUrl': BACK_PRE + '/match/list?isList=1',
            'createUrl': BACK_PRE + '/match/create',
            'enrollUserUrl': BACK_PRE + '/match/enroll/user',
        }
        return template('admin_match_list', info=info, lang=lang, RES_VERSION=RES_VERSION)


@admin_app.get('/match/create')
def getMatchCreate(redis, session):
    """
        创建比赛场
    """
    lang = getLang()

    game_ids = redis.lrange(GAME_LIST, 0, -1)

    gameList = {}
    for gameId in game_ids:
        if int(gameId) not in MatchGameIds:
            continue
        if redis.exists(GAME_TABLE % gameId):
            gameList[gameId] = redis.hget(GAME_TABLE % gameId, 'name')

    info = {
        "title": lang.MENU_MATCH_SETTING,
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        "submitUrl": BACK_PRE + "/match/create",
        'backUrl': BACK_PRE + '/match/list',
        "feetypeList": FeeTypeList,
        "gameList": gameList,
        "matchType": MatchTypeList,
    }
    return template('admin_match_create', info=info, lang=lang, RES_VERSION=RES_VERSION)


@admin_app.post('/match/create')
def postMatchCreate(redis, session):
    """
        创建比赛场
    """
    lang = getLang()
    curTime = datetime.now()
    match_title = request.forms.get('match_title', '').strip()  # 比赛名称
    match_type = request.forms.get('match_type', '').strip()  # 比赛类型
    match_gameid = request.forms.get('match_gameid', '').strip()  # 比赛游戏
    match_gamename = request.forms.get('match_gamename', '').strip() # 游戏名称
    match_feetype = request.forms.get('match_feetype', '').strip()  # 比赛费用类型
    party_type = request.forms.get('party_type', '').strip()  # 场次类型
    match_fee = request.forms.get('match_fee', '').strip()  # 比赛费用
    match_num = request.forms.get('match_num', '').strip()  # 比赛人数
    match_rule = request.forms.get('match_rule', '').strip()  # 比赛说明
    match_display = request.forms.get('match_display', '').strip()  # 比赛显示
    match_enroll = request.forms.get('match_enroll', '').strip()  # 比赛状态
    roundNums = request.forms.get('roundNums', '').strip()
    roundPlayers = request.forms.get('roundPlayers', '').strip()

    rewardList = []
    for num in range(1, 9):
        match_reward_rank = request.forms.get('match_reward_rank%s' % num, '').strip()
        match_reward_appellation = request.forms.get('match_reward_appellation%s' % num, '').strip()
        match_reward_type = request.forms.get('match_reward_type%s' % num, '').strip()
        match_reward_fee = request.forms.get('match_reward_fee%s' % num, '').strip()
        if any([match_reward_rank, match_reward_appellation, match_reward_type, match_reward_fee]):
            if all([match_reward_rank, match_reward_appellation, match_reward_type, match_reward_fee]):
                try:
                    assert int(match_reward_fee) >= 0
                    rewardList.append({
                        'rank': int(match_reward_rank),
                        'currency_count': int(match_reward_fee if match_reward_fee else 0),
                        'field': match_reward_appellation.decode('utf-8'),
                        'currency_type': Define_Currency.getCurrencyId(match_reward_type),
                        'id': num
                    })
                except Exception as err:
                    return {'code': 1, 'msg': '请输入正确的比赛奖励参数'}
            else:
                return {'code': 1, 'msg': '请输入正确的比赛奖励参数'}

    checkNullFields = [
        {'field': match_title, 'msg': '请输入比赛名称'},
        {'field': match_type, 'msg': '请选择比赛类型'},
        {'field': party_type, 'msg': '请选择场次类型'},
        {'field': match_gameid, 'msg': '请选择比赛游戏'},
        {'field': match_gamename, 'msg': '请填写游戏名称'},
        {'field': match_feetype, 'msg': '请选择比赛费用类型'},
        {'field': match_fee, 'msg': '请输入报名费用'},
        {'field': match_num, 'msg': '请输入比赛人数'},
        {'field': roundNums, 'msg': '请输入淘汰计划的触发轮数'},
        {'field': roundPlayers, 'msg': '请输入淘汰计划的淘汰人数'},
        {'field': match_display, 'msg': '请选择比赛是否前端显示'},
        {'field': match_enroll, 'msg': '请选择是否可报名'},
    ]

    for check in checkNullFields:
        if not check['field']:
            return {'code': 1, 'msg': check['msg']}

    try:
        roundNums = roundNums.split(',')
        roundNums = map(int, roundNums)
        assert roundNums == sorted(roundNums)
        assert len(roundNums) == len(list(set(roundNums)))
    except:
        traceback.print_exc()
        return {'code': 1, 'msg': '淘汰计划的触发轮数,请检查'}

    try:
        roundPlayers = roundPlayers.split(',')
        roundPlayers = map(int, roundPlayers)
        assert roundPlayers == sorted(roundPlayers, reverse=True)
        assert roundPlayers[-1] == 0
        assert len(roundNums) == len(roundPlayers)
        party_player_count = int(redis.hget(GAME_TABLE % match_gameid, 'party_player_count') or 4)
        assert not filter(lambda x: x % party_player_count != 0, roundPlayers)
        assert roundPlayers[0] < int(match_num)

    except:
        traceback.print_exc()
        return {'code': 1, 'msg': '淘汰计划的淘汰人数错误,请检查'}

    try:
        assert int(match_fee) >= 0
        assert int(match_num) > 0
    except Exception as err:
        return {'code': 1, 'msg': '报名费用或比赛人数，参数错误'}

    if not rewardList:
        return {'code': 1, 'msg': '请输入至少一个比赛奖励'}

    if party_type not in Define_Currency.CurrencyNameList:
        return {'code': 1, 'msg': '场次货币类型错误'}

    if match_feetype not in Define_Currency.CurrencyNameList:
        return {'code': 1, 'msg': '报名费用货币类型错误'}

    info = {'createTime': curTime.strftime("%Y-%m-%d %H:%M:%S"),  # 创建时间
            'title': match_title.decode('utf-8'),  # 比赛名称
            'type': match_type,  # 比赛类型
            'gameid': match_gameid,  # 比赛游戏ID
            'gamename': match_gamename.decode('utf-8'),  # 游戏名称
            'matchtype': Define_Currency.getCurrencyId(party_type),  # 场次类型
            'feetype': Define_Currency.getCurrencyId(match_feetype),  # 比赛费用类型
            'fee': match_fee,  # 比赛费用
            'play_num': match_num,  # 比赛人数
            'rule': match_rule.decode('utf-8'),  # 比赛规则说明
            'display': match_display,  # 比赛是否可见
            'enroll_status': match_enroll,  # 比赛是否可报名
            'rewardList': json.dumps(rewardList),  # 比赛奖品
            'enrollNum': 0,  # 当前报名人数
            'roundNums': ','.join(list(map(str, roundNums))),
            'roundPlayers': ','.join(list(map(str, roundPlayers))),
            }

    pipe = redis.pipeline()
    count = redis.incrby(MATCH_GAME_COUNT % (match_gameid))
    match_game_table = MATCH_GAME_ID_TABLE % (match_gameid, count)
    info['id'] = count
    pipe.hmset(match_game_table, info)
    pipe.sadd(MATCH_GAME_SET % match_gameid, count)
    if not redis.sismember(MATCH_SET, match_gameid):
        pipe.sadd(MATCH_SET, match_gameid)
    pipe.execute()
    return {'code': 0, 'msg': '创建比赛场成功', 'jumpUrl': BACK_PRE + '/match/list'}


@admin_app.get('/match/modify')
def getMatchModify(redis, session):
    """
        修改比赛场
    """
    lang = getLang()
    curTime = datetime.now()
    gameId = request.GET.get('gameId', '').strip()
    matchId = request.GET.get('id', '').strip()

    match_game_table = MATCH_GAME_ID_TABLE % (gameId, matchId)
    if not redis.exists(match_game_table):
        return {'code': 1, 'msg': '比赛场不存在'}

    matchInfo = redis.hgetall(match_game_table)
    matchInfo['match_gameplay'] = redis.hget(GAME_TABLE % matchInfo['gameid'], ('name'))
    try:
        rewardList = json.loads(matchInfo.get('rewardList', '[]'))
    except Exception as err:
        rewardList = eval(matchInfo.get('rewardList', '[]'))
    info = {
        "title": lang.MENU_MATCH_SETTING,
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        "submitUrl": BACK_PRE + "/match/modify",
        'backUrl': BACK_PRE + '/match/list',
        "feetypeList": FeeTypeList,
        "matchType": MatchTypeList,
        "rewardList": rewardList
    }
    return template('admin_match_modify', info=info, matchInfo=matchInfo, lang=lang, RES_VERSION=RES_VERSION)


@admin_app.post('/match/modify')
def postMatchModify(redis, session):
    """
        修改比赛场
    """
    lang = getLang()
    curTime = datetime.now()
    match_title = request.forms.get('match_title', '').strip()  # 比赛名称
    match_type = request.forms.get('match_type', '').strip()  # 比赛类型
    gameId = request.forms.get('match_gameid', '').strip()  # 游戏ID
    matchId = request.forms.get('match_matchId', '').strip()  # 比赛场ID
    gameName = request.forms.get('match_gamename', '').strip() # 比赛名称
    match_feetype = request.forms.get('match_feetype', '').strip()  # 比赛费用类型
    party_type = request.forms.get('party_type', '').strip()  # 场次类型
    match_fee = request.forms.get('match_fee', '').strip()  # 比赛费用
    match_num = request.forms.get('match_num', '').strip()  # 比赛人数
    match_rule = request.forms.get('match_rule', '').strip()  # 比赛说明
    roundNums = request.forms.get('roundNums', '').strip()
    roundPlayers = request.forms.get('roundPlayers', '').strip()

    rewardList = []
    for num in range(1, 9):
        match_reward_rank = request.forms.get('match_reward_rank%s' % num, '').strip()
        match_reward_appellation = request.forms.get('match_reward_appellation%s' % num, '').strip()
        match_reward_type = request.forms.get('match_reward_type%s' % num, '').strip()
        match_reward_fee = request.forms.get('match_reward_fee%s' % num, '').strip()
        if any([match_reward_rank, match_reward_appellation, match_reward_type, match_reward_fee]):
            if all([match_reward_rank, match_reward_appellation, match_reward_type, match_reward_fee]):
                try:
                    assert int(match_reward_fee) >= 0
                    rewardList.append({
                        'rank': int(match_reward_rank),
                        'currency_count': int(match_reward_fee if match_reward_fee else 0),
                        'field': match_reward_appellation.decode('utf-8'),
                        'currency_type': Define_Currency.getCurrencyId(match_reward_type), 'id': num
                    })
                except Exception as err:
                    return {'code': 1, 'msg': '请输入正确的比赛奖励参数'}
            else:
                return {'code': 1, 'msg': '请输入正确的比赛奖励参数'}

    checkNullFields = [
        {'field': match_title, 'msg': '请输入比赛名称'},
        {'field': match_type, 'msg': '请选择比赛类型'},
        {'field': party_type, 'msg': '请选择场次类型'},
        {'field': gameName, 'msg': '请填写游戏名称'},
        {'field': match_feetype, 'msg': '请选择比赛费用类型'},
        {'field': roundNums, 'msg': '请输入淘汰计划的触发轮数'},
        {'field': roundPlayers, 'msg': '请输入淘汰计划的淘汰人数'},
        {'field': match_fee, 'msg': '请输入报名费用'},
        {'field': match_num, 'msg': '请输入比赛人数'},
    ]

    for check in checkNullFields:
        if not check['field']:
            return {'code': 1, 'msg': check['msg']}

    try:
        roundNums = roundNums.split(',')
        roundNums = map(int, roundNums)
        assert roundNums == sorted(roundNums)
        assert len(roundNums) == len(list(set(roundNums)))
    except:
        traceback.print_exc()
        return {'code': 1, 'msg': '淘汰计划的触发轮数,请检查'}

    try:
        roundPlayers = roundPlayers.split(',')
        roundPlayers = map(int, roundPlayers)
        assert len(roundPlayers) == len(list(set(roundPlayers)))
        assert roundPlayers == sorted(roundPlayers, reverse=True)
        assert roundPlayers[-1] == 0
        assert len(roundNums) == len(roundPlayers)
        party_player_count = int(redis.hget(GAME_TABLE % gameId, 'party_player_count') or 4)
        assert not filter(lambda x: x % party_player_count != 0, roundPlayers)
        assert roundPlayers[0] < int(match_num)

    except:
        traceback.print_exc()
        return {'code': 1, 'msg': '淘汰计划的淘汰人数错误,请检查'}

    try:
        assert int(match_fee) >= 0
        assert int(match_num) > 0
    except Exception as err:
        return {'code': 1, 'msg': '报名费用或比赛人数，参数错误'}

    if not rewardList:
        return {'code': 1, 'msg': '请输入至少一个比赛奖励'}

    match_game_table = MATCH_GAME_ID_TABLE % (gameId, matchId)
    if not redis.exists(match_game_table):
        return {'code': 1, 'msg': '比赛场不存在'}

    if party_type not in Define_Currency.CurrencyNameList:
        return {'code': 1, 'msg': '场次类型货币类型错误'}

    if match_feetype not in Define_Currency.CurrencyNameList:
        return {'code': 1, 'msg': '报名费用货币类型错误'}

    info = {'title': match_title.decode('utf-8'),  # 比赛名称
            'type': match_type,  # 比赛类型
            'gamename': gameName,
            'matchtype': Define_Currency.getCurrencyId(party_type),  # 场次类型
            'feetype': Define_Currency.getCurrencyId(match_feetype),  # 比赛费用类型
            'fee': match_fee,  # 比赛费用
            'play_num': match_num,  # 比赛人数
            'rule': match_rule.decode('utf-8'),  # 比赛规则说明
            'rewardList': json.dumps(rewardList),  # 比赛奖品
            'roundNums': ','.join(list(map(str, roundNums))),
            'roundPlayers': ','.join(list(map(str, roundPlayers))),
            }

    pipe = redis.pipeline()
    pipe.hmset(match_game_table, info)
    pipe.execute()
    return {'code': 0, 'msg': '修改比赛场成功', 'jumpUrl': BACK_PRE + '/match/list'}


@admin_app.post('/match/enroll_status')
def doMatchStatus(redis, session):
    """
        关闭比赛场赛事
    """
    lang = getLang()
    curTime = datetime.now()
    gameId = request.forms.get('gameid', '').strip()
    matchId = request.forms.get('id', '').strip()

    if not gameId or not matchId:
        return {'code': 1, 'msg': '该比赛场不存在'}

    match_game_table = MATCH_GAME_ID_TABLE % (gameId, matchId)
    enroll_status = redis.hget(match_game_table, 'enroll_status')
    if enroll_status == '1':
        redis.hmset(match_game_table, {'enroll_status': '0'})
    else:
        redis.hmset(match_game_table, {'enroll_status': '1'})
    return {'code': 0, 'msg': '修改成功', 'jumpUrl': ''}


@admin_app.post('/match/display')
def doMatchDsiplay(redis, session):
    """
        关闭比赛场赛事
    """
    lang = getLang()
    curTime = datetime.now()
    gameId = request.forms.get('gameid', '').strip()
    matchId = request.forms.get('id', '').strip()

    if not gameId or not matchId:
        return {'code': 1, 'msg': '该比赛场不存在'}

    match_game_table = MATCH_GAME_ID_TABLE % (gameId, matchId)
    status = redis.hget(match_game_table, 'display')
    if status == '1':
        redis.hmset(match_game_table, {'display': '0'})
    else:
        redis.hmset(match_game_table, {'display': '1'})
    return {'code': 0, 'msg': '修改成功', 'jumpUrl': ''}


@admin_app.post('/match/delete')
def doMatchDelete(redis, session):
    """
    删除比赛场赛事
    """
    lang = getLang()
    curTime = datetime.now()
    gameId = request.forms.get('gameid', '').strip()
    matchId = request.forms.get('id', '').strip()

    if not gameId or not matchId:
        return {'code': 1, 'msg': '该比赛场不存在'}

    '''删除只移除遍历队列,不完全删除'''
    matchInfo = redis.hgetall(MATCH_GAME_ID_TABLE % (gameId, matchId))
    enrollNum = int(matchInfo.get('enrollNum', 0))
    if enrollNum > 0:
        return {'code': 1, 'msg': '当前存在报名玩家,不能删除'}

    # redis.delete(MATCH_GAME_ID_TABLE % (gameId, matchId))
    redis.srem(MATCH_GAME_SET % gameId, matchId)
    if not redis.exists(MATCH_GAME_SET % gameId):
        redis.srem(MATCH_SET, gameId)
    return {'code': 0, 'msg': '删除成功', 'jumpUrl': ''}


@admin_app.post('/match/enrollUsers_delete')
def do_enrollUsers_delete(redis, session):
    """
    取消该比赛场的报名
    """
    lang = getLang()
    gameId = request.forms.get('gameid', '').strip()
    matchId = request.forms.get('id', '').strip()
    data = {}
    for serverTag in list(redis.smembers(Key_Server_Set)):
        url = 'http://%s' % serverTag
        r = requests.post('%s/ping' % url)
        if r.status_code == 200:
            print('[do_enrollUsers_delete] [%s] OK' % url)
            r = requests.delete('%s/admin/match/enrollUsers' % (url), data={'gameId': gameId, 'matchId': matchId})
            if r.status_code == 200:
                print(r)
                print(r.text)
                data = r.json()
            else:
                data = r.text
            break
    if not gameId or not matchId:
        return {'code': 1, 'msg': '该比赛场不存在'}
    return {'code': 0, 'msg': '成功', 'jumpUrl': '', 'data': data}

@admin_app.get('/match/enroll/user')
def getMatchEnrollUser(redis, session):
    """
    获取比赛场已报名人员信息
    """
    curTime = datetime.now()
    gameId = request.GET.get('gameId', '').strip()
    playId = request.GET.get('playId', '').strip()
    if not gameId or not playId:
        return

    enrollUsers_Table = 'match:game:%s:%s:enroll:users:zset' % (gameId, playId)
    res = []
    if redis.exists(enrollUsers_Table):
        for _userId in redis.zrange(enrollUsers_Table, 0, -1):
            info = {}
            info['userId'] = _userId
            nickname, account = redis.hmget(FORMAT_USER_TABLE % _userId, ('nickname', 'account'))
            info['nickname'] = nickname
            info['account'] = account
            res.append(info)
    return json.dumps(res)


@admin_app.get('/match/run/list')
def getMatchRunList(redis, session):
    """
    赛事列表
    """
    lang = getLang()
    curTime = datetime.now()
    toDay = curTime.strftime("%Y-%m-%d")
    isList = request.GET.get('isList', '').strip()
    if isList:
        res = []
        startDate = time.mktime(time.strptime('%s 00:00:00' % toDay, '%Y-%m-%d %H:%M:%S'))
        endDate = time.mktime(time.strptime('%s 23:59:59' % toDay, '%Y-%m-%d %H:%M:%S'))
        queryStr = """SELECT * FROM match_record
        WHERE matchState not in (10,12) and create_time >=%s and create_time <=%s
        """ % (startDate, endDate)
        results = MysqlInterface.query(sql=queryStr)
        num = 1
        for result in results:
            info = {}
            info['num'] = num
            info['game_id'] = result[1]
            info['match_id'] = result[2]
            info['match_number'] = result[3]
            gameTable = GAME_TABLE % (result[1])
            info['game_name'] = redis.hget(gameTable, 'name')
            info['match_type'] = result[9]
            info['total_fee'] = result[7]
            info['total_num'] = result[8]
            info['match_state'] = result[15]
            info['match_dismissReason'] = result[16]
            info['start_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(result[13])))
            num += 1
            res.append(info)
        data = { 'count': len(res),'data': res }
        return json.dumps(data)
    else:
        info = {
            'title': "赛事列表",
            'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
            'tableUrl': BACK_PRE + '/match/run/list?isList=1',
            'user_tableUrl': BACK_PRE + '/match/runUser/list?isList=1',
        }
        return template('admin_match_run_list', info=info, lang=lang, RES_VERSION=RES_VERSION)


@admin_app.get('/match/runUser/list')
def getMatchRunUserList(redis, session):
    """
    赛事用户列表
    """
    lang = getLang()
    curTime = datetime.now()
    toDay = curTime.strftime("%Y-%m-%d")
    isList = request.GET.get('isList', '').strip()
    game_id = request.GET.get('game_id', '').strip()
    match_id = request.GET.get('match_id', '').strip()
    match_number = request.GET.get('match_number', '').strip()
    res = []
    if isList:
        matchNumber_table = 'match:matchNumber:%s:hesh' % match_number
        if redis.exists(matchNumber_table):
            userIds = redis.hget(matchNumber_table, 'curUserIds')
            userIds = userIds.split(',')
            for userId in userIds:
                info = {}
                info['user_id'] = userId
                user_table = FORMAT_USER_TABLE % (userId)
                account, nickname, gamePoint, clientKind = redis.hmget(user_table, ('account','nickname', 'gamePoint', 'lastLoginClientType'))
                online_table = FORMAT_CUR_USER_GAME_ONLINE % (account)
                date, roomTag, serviceTag, ip = redis.hmget(online_table, ('date', 'game', 'serviceTag', 'ip'))
                info['date'] = date
                info['account'] = account
                info['nickname'] = nickname
                info['roomTag'] = roomTag
                info['serverTag'] = serviceTag
                info['clientKind'] = lang.CLINET_KIND_TXTS[clientKind] if clientKind else '未知设备',
                info['login_ip'] = ip
                res.append(info)
    data = {'count': len(res), 'data': res}
    return data




@admin_app.get('/match/introSetting')
def get_editDesc(redis,session):
    """
    编辑游戏规则
    生成游戏静态页面
    """
    curTime = datetime.now()
    lang = getLang()
    matchId = request.GET.get('id', '').strip()
    gameId = request.GET.get('gameId', '').strip()

    gameDescTable = MATCH_GAME_ID_DESC % (gameId, matchId)
    gameDesc =  redis.get(gameDescTable)
    gameTable = MATCH_GAME_ID_TABLE % (gameId, matchId)
    gameName = redis.hget(gameTable,'gamename')

    info = {
          'title'                 :       lang.GAME_EDIT_DESC % (gameName),
          'gameId'                :       gameId,
          'matchId'               :       matchId,
          'gameDesc'              :       gameDesc if gameDesc else '',
          'backUrl'               :       BACK_PRE+'/match/list',
          'submitUrl'             :       BACK_PRE+'/match/introSetting',
          'back_pre'              :       BACK_PRE,
          'STATIC_LAYUI_PATH'     :       STATIC_LAYUI_PATH,
          'STATIC_ADMIN_PATH'     :       STATIC_ADMIN_PATH,
    }

    return template('admin_match_introsetting', info=info, lang=lang, RES_VERSION=RES_VERSION)

@admin_app.post('/match/introSetting')
def get_editDesc(redis,session):
    """
    编辑游戏规则
    生成游戏静态页面
    """
    curTime = datetime.now()
    lang = getLang()
    gameId = request.forms.get('gameId', '').strip()
    matchId = request.forms.get('matchId', '').strip()
    content = request.forms.get('content', '').strip()

    gameDescTable = MATCH_GAME_ID_DESC % (gameId, matchId)
    gameTable = MATCH_GAME_ID_TABLE % (gameId, matchId)

    if not redis.exists(gameTable):
        return {'code': -1, 'msg': '该比赛场不存在'}

    if not content:
        return {'code': -1, 'msg': '规则不能为空'}
    redis.set(gameDescTable, content)
    return {'code': 0, 'msg': '编辑规则成功', 'jumpUrl': ''}


# @admin_app.get('/match/setting')
# @admin_app.post('/match/setting')
# def set_matchSetting(redis, session):
#     """
#     比赛场设置
#     """
#     lang = getLang()
#     submitData = request.json
#     if submitData:
#         # log_debug("set_matchSetting ********** %s" % request.json)
#         count = redis.incrby(MATCH_COUNT)
#         info = copy.deepcopy(request.json)
#         key = MATCH_SETTING % count
#         info["id"] = str(count)
#         info["type"] = int(info["type"]) if info["type"] else 0
#         info["gameid"] = int(info["gameid"])
#         info["baseScore"] = int(info["baseScore"])
#         redis.set(key, json.dumps(info))
#         redis.sadd(MATCH_SET, key)
#
#         return {'code': 0, 'msg': '提交成功', 'jumpUrl': BACK_PRE + "/match/setting"}
#
#     game_ids = redis.lrange(GAME_LIST, 0, -1)
#     gameList = {}
#     for gameId in game_ids:
#         if redis.exists(GAME_TABLE % gameId):
#             gameList[gameId] = redis.hget(GAME_TABLE % gameId, 'name')
#
#     feetypeList = {'0': '钻石'}
#     rewardTypeList = json.dumps({'0': '钻石'})
#     matchType = {'0': '即时开启', '1': '定时开启'}
#
#     info = {
#         "title": lang.MENU_MATCH_SETTING,
#         "submitUrl": BACK_PRE + "/match/setting",
#         'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
#         'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
#         'resourceUrl': BACK_PRE + "/activice/resource?list=1",
#         'agentListUrl': BACK_PRE + '/agent/list',
#         'backUrl': BACK_PRE + '/match/list'
#     }
#     setting = {
#         "feetypeList": feetypeList,
#         "rewardTypeList": rewardTypeList,
#         "gameList": gameList,
#         "matchType": matchType,
#         "readonly": False,
#         "tableUrl": False,
#     }
#
#     return template('admin_match_setting', info=info, setting=setting, lang=lang, RES_VERSION=RES_VERSION)
#
#
# @admin_app.get('/match/modify')
# @admin_app.post('/match/modify')
# def set_matchModify(redis, session):
#     """
#     修改比赛场设置
#     """
#     lang = getLang()
#     # 修改
#     if request.json:
#         matchid = request.json.get('id', '').strip()
#         if matchid:
#             info = copy.deepcopy(request.json)
#             key = MATCH_SETTING % matchid
#             info["type"] = int(info["type"]) if info["type"] else 0
#             info["gameid"] = int(info["gameid"])
#             info["baseScore"] = int(info["baseScore"])
#             redis.set(key, json.dumps(info))
#             redis.sadd(MATCH_SET, key)
#             return {'code': 0, 'msg': '修改成功', 'jumpUrl': BACK_PRE + '/match/list'}
#     # 获取数据
#     matchid = request.GET.get('id', '').strip()
#     isJson = request.GET.get('isJson', '').strip()
#     log_debug('比赛场数据接收 {0} -'.format(isJson))
#
#     if isJson and matchid:
#         data = get_match_info(redis, matchid)
#         return {'code': 0, 'msg': '获取成功', 'data': data}
#
#     # 展示页面
#     feetypeList = json.dumps({
#         'gold': '金币',
#         'roomCard': '钻石',
#         'yuanbao': '元宝',
#         'prop': '道具'
#     })
#
#     rewardTypeList = json.dumps({
#         'gold': '金币',
#         'roomCard': '钻石',
#         'yuanbao': '元宝',
#         'redpacket': '红包',
#         'prop': '道具'
#     })
#
#     info = {
#         "title": lang.MENU_MATCH_MODIFY,
#         "submitUrl": BACK_PRE + "/match/modify",
#         'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
#         'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
#     }
#     setting = {
#         "feetypeList": feetypeList,
#         "rewardTypeList": rewardTypeList,
#         "readonly": False,
#         "tableMethod": 'get',
#         "tableUrl": BACK_PRE + '/match/modify?id=%s&isJson=1' % matchid,
#     }
#
#     return template('admin_match_setting.tpl', info=info, setting=setting, lang=lang, RES_VERSION=RES_VERSION)
#
#
# @admin_app.get('/match/del')
# @admin_app.post('/match/del')
# def set_matchDel(redis, session):
#     """
#         删除比赛场
#     """
#     matchid = request.forms.get('id', '').strip()
#     checkNullFields = [
#         {'field': matchid, 'msg': '比赛ID不存在'},
#     ]
#
#     for check in checkNullFields:
#         if not check['field']:
#             return {'code': 1, 'msg': check['msg']}
#
#     key = MATCH_SETTING % matchid
#     if not redis.sismember(MATCH_SET, key):
#         return {'code': 1, 'msg': '比赛ID不存在'}
#
#     pipe = redis.pipeline()
#     try:
#         pipe.delete(key)
#         pipe.srem(MATCH_SET, key)
#         pipe.execute()
#     except Exception, e:
#         return {'code': 1, 'msg': '删除失败'}
#
#     return {'code': 0, 'msg': '删除成功', 'jumpUrl': BACK_PRE + '/match/list'}
#
#
# class CJsonEncoder(json.JSONEncoder):
#     def default(self, obj):
#         # if isinstance(obj, datetime):
#         # return obj.strftime('%Y-%m-%d %H:%M:%S')
#         if isinstance(obj, datetime):
#             return obj.strftime('%Y-%m-%d %H:%M:%S')
#         else:
#             return json.JSONEncoder.default(self, obj)
#
#
# @admin_app.get('/match/2renmajiang')
# def getMatchList(redis, session):
#     """
#         比赛场列表
#     """
#     lang = getLang()
#     isList = request.GET.get('isList', '').strip()
#     startDate = request.GET.get('startDate', '').strip()
#     endDate = request.GET.get('endDate', '').strip()
#     gameid = request.GET.get('gameid', '').strip()
#     if isList:
#         res = get_2MJ_log_list(redis, startDate, endDate, gameid)
#         return json.dumps(res, cls=CJsonEncoder)
#     else:
#         info = {
#             'title': "二人麻将统计表",
#             'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
#             'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
#             'listUrl': BACK_PRE + '/match/2renmajiang?isList=1&gameid=451'
#         }
#         return template('admin_match_2mj_log.tpl', info=info, lang=lang, RES_VERSION=RES_VERSION)
#
#
# @admin_app.get('/match/paodekuai')
# def getMatchList(redis, session):
#     """
#         比赛场列表
#     """
#     lang = getLang()
#     isList = request.GET.get('isList', '').strip()
#     startDate = request.GET.get('startDate', '').strip()
#     endDate = request.GET.get('endDate', '').strip()
#     gameid = request.GET.get('gameid', '').strip()
#     if isList:
#         res = get_2MJ_log_list(redis, startDate, endDate, gameid)
#         return json.dumps(res, cls=CJsonEncoder)
#     else:
#         info = {
#             'title': "跑得快统计表",
#             'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
#             'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
#             'listUrl': BACK_PRE + '/match/paodekuai?isList=1&gameid=460'
#         }
#         return template('admin_match_2mj_log.tpl', info=info, lang=lang, RES_VERSION=RES_VERSION)
