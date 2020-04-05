#-*- coding:utf-8 -*-
#!/usr/bin/python

"""
     比赛场
"""

import json
from hall import hall_app
from hall_func import getUserByAccount
from common.utilt import *
from bottle import request, response, template, static_file
from model.matchModel import *
from model.goldModel import *
from common import web_util, convert_util
import copy
from bag.bag_func import check_vcoin_baselive,cost_player_item,bag_redis,get_player_item
from datetime import datetime
from common.record_player_info import record_player_balance_change
"""
    /hall/match/getInfo  ------ 前端获取比赛场信息接口
"""
Match_Timging_List = 'match:Timing:%s:set'

@hall_app.post('/match/getInfo')
@web_util.allow_cross_request
def getMatchInfo(redis, session):
    """
        获取比赛场信息
    """
    sid = request.POST.get('sid', '').strip()
    if not sid:
        return {'code': -5, 'msg': '该用户不存在'}
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    groupId = redis.hget(userTable, 'parentAg')
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}
    data = copy.deepcopy(MatchConfig)

    # 在线人数
    for item in data:
        item["online_num"] = redis.scard(MATCH_ONLINE_ACCOUNTS_BY_TYPE_SET % item["type"])

    for key in redis.smembers(MATCH_SET):
        if not redis.exists(key):
            continue
        mid = key.split(":")[2]
        info = json.loads(redis.get(key))
        info["num"] = redis.scard(MATCH_WAITTING_PLAYER_SET % mid) + \
            redis.scard(MATCH_ENTER_PLAYER_SET % mid)
        gameid = info["gameid"]
        info["gameName"] = redis.hget(GAME_TABLE % gameid, "name")
        _type = int(info["type"])

        today = datetime.now().strftime("%Y-%m-%d")
        key = MATCH_ACCOUNT_FREE_TIMES % (info["id"], account, today)

        if not redis.exists(key):
            can_times = int(info.get("freeTimes",0))
        else:
            can_times = int(redis.get(key))

        info["currentTimes"] = can_times if can_times > 0 else 0

        if _type == 1:#定时赛
            info["isSignUp"] = False
            info["isCanJoin"] = False
            info["isCanSignUp"] = False
            now_time = datetime.now()
            now_time_tuple = now_time.timetuple()
            now_hour = now_time_tuple.tm_hour
            now_second = now_time_tuple.tm_sec

            timeStart = info["timeStart"]
            today = '%s-%s-%s' % (now_time_tuple.tm_year, now_time_tuple.tm_mon, now_time_tuple.tm_mday)
            timeStart = '%s %s' % (today, timeStart)

            match_startTime = datetime.strptime(timeStart, "%Y-%m-%d %H:%M:%S")
            print 'match_startTime', match_startTime
            match_hour = match_startTime.hour
            match_min = match_startTime.minute

            D_value_minute = (match_startTime - now_time).total_seconds() / 60
            D_value_second = (match_startTime - now_time).total_seconds() % 60
            print '距离比赛还有%s分%s秒钟' % (D_value_minute,D_value_second)
            Match_enrolment = 'match:Timing:%s:%s:%s' % (gameid,info["id"], '%s-%s-%s' % (today, match_hour, match_min))
            print 'Match_enrolment',Match_enrolment

            if D_value_minute > 0:
                if D_value_minute > 1 and redis.scard(Match_enrolment) < int(info["play_num"]):
                    info["isCanSignUp"] = True
                if redis.sismember(Match_enrolment, account):
                    info["isSignUp"] = True
                    if D_value_minute <= 5:
                        info["isCanJoin"] = True
                data[_type]["list"].append(info)
        else:
            data[_type]["list"].append(info)
    # for item in data:
    #     # 人满即开
    #     if item["type"] == 0:
    #         for detail_config in item["list"]:
    #             detail_config["status"] = 2 # 开始状态

    return {'code': 0, 'msg': '', 'data': data}


"""
    /hall/match/enter ------ 报名接口
    params:  id ---- 比赛ID 
"""


@hall_app.post('/match/enter')
@web_util.allow_cross_request
def doMatchEnter(redis, session):
    """
        报名

    """
    log_debug('==============================================')
    log_debug('==================报名============================')
    log_debug('==============================================')

    sid = request.POST.get('sid', '').strip()
    id = request.POST.get('id', '').strip()
    if not sid:
        return {'code': -5, 'msg': '该用户不存在'}
    if not id:
        return {'code': -5, 'msg': '该比赛不存在'}
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    groupId = redis.hget(userTable, 'parentAg')
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    key = MATCH_SETTING % id

    if not redis.sismember(MATCH_SET, key):
        return {'code': -5, 'msg': '该比赛不存在'}

    if not redis.exists(key):
        return {'code': -5, 'msg': '该比赛不存在'}

    detail_config = json.loads(redis.get(key))

    if int(detail_config["type"]) != 0:
        return {"code": 10001, "msg": "当前报名的比赛是定时赛,请刷新重试"}

    now_time = datetime.now().timetuple().tm_hour
    # if  now_time < 11 or now_time >=23:
    #     return {"code": -1, "msg": "比赛场开始时间为11:00~23:00,请在时间内参与"}

    e_num = bag_redis.scard(USER_EMAIL_SET % uid)
    if e_num >= 200:
        return {"code": -1, "msg": "很抱歉，您的邮箱已满，为了避免奖励丢失，请先清理邮箱邮件。"}

    gameid = detail_config["gameid"]
    # 获取可以匹配得服务器端口
    serverTable,serverList,type = get_valuable_game_service(redis, gameid)
    if not serverList:
        return {'code': -1, 'msg': '服务器忙碌或维护中'}
    if not serverTable:
        return {'code': -1, 'msg': '比赛正在进行,请等待比赛结束'}
    _, _, _, _, ip, port = serverTable.split(':')


    fee = int(detail_config["fee"])
    feetype = detail_config["feetype"]

    #门槛
    threshold = int(detail_config["threshold"])
    thresholdType = detail_config["thresholdType"]

    # 判断是否有免费次数
    freeTimes = detail_config.get("freeTimes", None)
    freeTimes = int(freeTimes) if freeTimes else 0

    ###玩家检测#########
    today = datetime.now().strftime("%Y-%m-%d")
    key = MATCH_ACCOUNT_FREE_TIMES % (id, account, today)
    if not redis.exists(key):
        redis.set(key, freeTimes)
        redis.expire(key, 60 * 60 * 24)
    can_times = int(redis.get(key))
    if can_times > freeTimes:
        redis.set(key, freeTimes)
        can_times = freeTimes

    # if fee != 0 and not can_times:
    if fee != 0 and can_times <= 0:
        if feetype == "gold":
            coin = redis.hget(FORMAT_USER_TABLE % userTable.split(':')[1], 'gold')
            if not coin:
                coin = 0
            coin = int(coin)
            if coin < fee:
                return {'code': -1, 'msg': u'您携带的金币数不足支付当前比赛的报名费用(%s)，请充值后进入。'%(fee)}
        elif feetype == "roomCard":
            roomCards = redis.get(USER4AGENT_CARD % (groupId, userTable.split(':')[1]))
            if int(roomCards) < fee:
                return {'code': -1, 'msg': u'您持有的钻石数不足支付当前比赛的报名费用(%s)，请充值后再进入。'%(fee)}

        elif feetype == "yuanbao":
            # 元宝领低保
            res = check_vcoin_baselive(uid,threshold)
            if res == 1:
                return {'code': -2, 'msg': u'您携带的元宝数不足以进入本场次游戏，请充值后进入。'}
            elif res == 2:
                yuanbao_final = bag_redis.hget(PLAYER_ITEM_HASH % uid, '3')
                yuanbao_final = int(yuanbao_final) if yuanbao_final else 0
                record_player_balance_change(bag_redis, userTable, 3, threshold, yuanbao_final, 7)
                return {'code': 3, 'msg': u'您携带的元宝数不足以进入本场次游戏，系统为您免费补足12元宝。'}

    if threshold!= 0:
        if thresholdType == "gold":
            coin = redis.hget(FORMAT_USER_TABLE % userTable.split(':')[1], 'gold')
            if not coin:
                coin = 0
            coin = int(coin)
            if coin < threshold:
                return {'code': -1, 'msg': u'您携带的金币数不满足进入当前比赛所需的最低标准(%s)，请充值后进入。'%(threshold)}
        elif thresholdType == "roomCard":
            roomCards = redis.get(USER4AGENT_CARD % (groupId, userTable.split(':')[1]))
            if int(roomCards) < threshold:
                return {'code': -1, 'msg': u'您持有的钻石数不满足进入当前比赛所需的最低标准(%s)，请充值后再进入。'%(threshold)}
        else:
            pass

    if can_times <= 0:
        # 直接扣取报名费
        log_debug('[%s]扣除报名费'%(account))
        if feetype == "gold":
            player_add_gold(redis, account, -fee)
            gold = redis.hget(userTable,('gold'))
            record_player_balance_change(bag_redis, userTable, 2, -fee, gold, 32, gameid)
        elif feetype == "roomCard":
            player_add_gold(redis, account, 0, -fee)
            parentAg = redis.hget(userTable, ('parentAg'))
            card = redis.get(USER4AGENT_CARD % (parentAg, uid))
            record_player_balance_change(bag_redis, userTable, 1, -fee, card, 32, gameid)
        elif feetype == "yuanbao":
            cost_player_item(3, uid, int(fee))
            new_number = bag_redis.hget(PLAYER_ITEM_HASH%uid,str(3))
            record_player_balance_change(bag_redis, userTable, 3, -fee, new_number, 32, gameid)
        else:
            log_debug('支付红包')
    else:
        log_debug('[%s]扣除免费次数' % (account))
    redis.decr(key)
    return {'code': 0, 'ip': ip, 'port': port, 'gameid': gameid, 'isParty': '3'}

def get_valuable_game_service(redis, gameid):
    serverList = redis.lrange(FORMAT_GAME_SERVICE_SET % gameid, 0, -1)
    print '[get_valuable_game_service] serverList %s'%(serverList)
    if redis.exists(MATCH_WAITING_GAME_SERVIVE_KEY % gameid):
        table = redis.get(MATCH_WAITING_GAME_SERVIVE_KEY % gameid)
        if table in serverList:
            # 已开了比赛场
            return table,serverList,1
        else:
            redis.delete(MATCH_WAITING_GAME_SERVIVE_KEY % gameid)
    for table in serverList:
        match_service_set = redis.sismember(MATCH_GAMING_GAME_SERVICE_SET % gameid, table)
        if match_service_set:
            continue
        # 未开比赛场
        redis.set(MATCH_WAITING_GAME_SERVIVE_KEY % gameid, table)
        return table,serverList,2
    print '[get_valuable_game_service] 当前端口已被消耗完'
    return [],serverList,0

@hall_app.post('/match/enterTiming')
@web_util.allow_cross_request
def doMatchEnterTiming(redis, session):
    """
        报名

    """
    print('==============================================')
    print('==================报名============================')
    print('==============================================')

    sid = request.POST.get('sid', '').strip()
    id = request.POST.get('id', '').strip()
    type = request.POST.get('type', '').strip()

    if not sid:
        return {'code': -5, 'msg': '该用户不存在'}
    if not id:
        return {'code': -5, 'msg': '该比赛不存在'}
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    groupId = redis.hget(userTable, 'parentAg')
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    key = MATCH_SETTING % id

    if not redis.sismember(MATCH_SET, key) or not redis.exists(key):
        return {'code': -5, 'msg': '该比赛不存在'}

    detail_config = json.loads(redis.get(key))

    e_num = bag_redis.scard(USER_EMAIL_SET % uid)
    if e_num >= 200:
        return {"code": -1, "msg": "很抱歉，您的邮箱已满，为了避免奖励丢失，请先清理邮箱邮件。"}

    if int(detail_config["type"] or 0) != 1:
        return {"code": 10001, "msg": "当前报名的比赛不是定时赛,请刷新重试"}

    gameid = detail_config["gameid"]
    # 获取可以匹配得服务器端口
    serverTable,serverList,match_type = get_valuable_game_service(redis, gameid)
    if not serverList:
        return {'code': -1, 'msg': '服务器忙碌或维护中'}
    if not serverTable:
        return {'code': -1, 'msg': '比赛正在进行,请等待比赛结束'}
    _, _, _, _, ip, port = serverTable.split(':')

    now_time = datetime.now()
    now_time_tuple = now_time.timetuple()
    now_hour = now_time_tuple.tm_hour
    now_second = now_time_tuple.tm_sec

    timeStart = detail_config["timeStart"]
    today = '%s-%s-%s'%(now_time_tuple.tm_year,now_time_tuple.tm_mon,now_time_tuple.tm_mday)
    timeStart = '%s %s'%(today,timeStart)

    match_startTime = datetime.strptime(timeStart, "%Y-%m-%d %H:%M:%S")
    print 'match_startTime',match_startTime
    match_hour = match_startTime.hour
    match_min = match_startTime.minute

    D_value_minute = (match_startTime-now_time).total_seconds()/60
    print '距离比赛还有%s分钟'%(D_value_minute)
    Match_enrolment = 'match:Timing:%s:%s:%s' % (gameid,id, '%s-%s-%s' % (today, match_hour, match_min))
    print 'Match_enrolment',Match_enrolment
    #######################该局比赛信息###############
    fee = int(detail_config["fee"])
    feetype = detail_config["feetype"]
    fee_id = int(detail_config.get("fee_id", 0) or 0)
    # 门槛
    threshold = int(detail_config["threshold"])
    thresholdType = detail_config["thresholdType"]

    # 判断是否有免费次数
    freeTimes = detail_config.get("freeTimes", None)
    freeTimes = int(freeTimes) if freeTimes else 0

    ###玩家检测#########
    today = datetime.now().strftime("%Y-%m-%d")
    key = MATCH_ACCOUNT_FREE_TIMES % (id, account, today)
    if not redis.exists(key):
        redis.set(key, freeTimes)
        redis.expire(key, 60 * 60 * 24)
    can_times = int(redis.get(key))
    if can_times > freeTimes:
        redis.set(key, freeTimes)
        can_times = freeTimes

    print '费用类型', feetype
    print '费用', fee
    print '道具id', fee_id
    print '门槛类型', thresholdType
    print '门槛数量', threshold
    print '比赛免费次数', freeTimes
    print '玩家免费次数', can_times
    #######################该局比赛信息###############
    if D_value_minute <= 0:
        return {'code':10000,'msg':u'比赛不存在,请刷新重试'}
    if type == '1':
        if not redis.sismember(Match_enrolment, account):
            if D_value_minute <= 1:
                return {'code': 10005, 'msg': u'您未报名了该比赛,当前比赛已截止报名,请留意下场比赛'}
            else:
                return {'code': 10004, 'msg': u'您未报名了该比赛,请先报名'}
        else:
            if D_value_minute < 5:
                match_players_key = MATCH_WAITTING_PLAYER_SET % id
                players = redis.smembers(match_players_key)
                print u'比赛场内有%s共%s人' % (players, len(players))
                return {'code': 10006, 'msg': u'比赛将要开始,无法取消报名,请进入比赛,等候开始'}
            if can_times < 0:
                print(u'[%s]返还报名费 类型[%s] 道具ID[%s] 数量[%s]' % (account, feetype, fee_id, fee))
                if int(fee) > 0:
                    if feetype == "gold":
                        print(u'返还金币%s个' % (fee))
                        player_add_gold(redis, account, fee)
                        gold = redis.hget(userTable, ('gold'))
                        record_player_balance_change(bag_redis, userTable, 2, fee, gold, 33, gameid)

                    elif feetype == "roomCard":
                        print(u'返还钻石%s个' % (fee))
                        player_add_gold(redis, account, 0, fee)
                        parentAg = redis.hget(userTable, ('parentAg'))
                        card = redis.get(USER4AGENT_CARD % (parentAg, uid))
                        record_player_balance_change(bag_redis, userTable, 1, fee, card, 33, gameid)

                    elif feetype == "yuanbao":
                        print(u'返还元宝%s个' % (fee))
                        cost_player_item(3, uid, -int(fee))
                        new_number = bag_redis.hget(PLAYER_ITEM_HASH % uid, str(3))
                        record_player_balance_change(bag_redis, userTable, 3, fee, new_number, 33, gameid)

                    elif feetype == "prop":
                        # ITEM_ATTRS = "attrs:itemid:%s:hash"
                        # item_attrs = bag_redis.hgetall(ITEM_ATTRS % fee_id)
                        # if item_attrs["unit"] == 1:
                        #     fee *= 100
                        result = cost_player_item(fee_id, uid, -int(fee))
                        if result:
                            print(u'扣除道具(%s)%s个成功' % (fee_id, fee))
                            new_number = bag_redis.hget(PLAYER_ITEM_HASH % uid, str(fee_id))
                            record_player_balance_change(bag_redis, userTable, fee_id, fee, new_number, 33, gameid)
                        else:
                            print(u'扣除道具(%s)%s个失败' % (fee_id, fee))
            else:
                redis.incr(key)
                print(u'返还免费次数 当前还剩%s次' % (can_times+1))
            redis.srem(Match_enrolment, account)
            if not redis.scard(Match_enrolment):
                redis.srem(Match_Timging_List%gameid,Match_enrolment)
                redis.delete(Match_enrolment)
            return {'code': 0, 'msg': u'取消报名成功'}
    elif type == '2':
        if not redis.sismember(Match_enrolment, account):
            if D_value_minute <= 1:
                return {'code': 10008, 'msg': u'您未报名了该比赛,当前比赛已截止报名,请留意下场比赛'}
            else:
                return {'code': 10007, 'msg': u'您未报名了该比赛,请先报名'}
        if D_value_minute >= 5:
            return {'code': 10009, 'msg': u'距离比赛还有%s分钟,现在暂未开放进入'%(int(D_value_minute))}
        else:
            if D_value_minute <= 1:
                if redis.scard(Match_enrolment) < int(detail_config["play_num_lower"]):
                    match_players_key = MATCH_WAITTING_PLAYER_SET%id
                    players = redis.smembers(match_players_key)
                    print u'比赛场内有%s共%s人'%(players,len(players))
                    return {'code':10010,'msg':u'报名人数不足,比赛取消'}
            return {'code': 0, 'ip': ip, 'port': port, 'gameid': gameid, 'isParty': '3'}
    elif type == '0':
        if D_value_minute <= 1:
            return {'code':10003, 'msg': u'报名已关闭,请留意下次比赛时间'}
        if redis.sismember(Match_enrolment,account):
            return {'code':10002, 'msg':u'您已经报名了该比赛,请勿重复报名'}
        if redis.scard(Match_enrolment) >= int(detail_config["play_num"]):
            return {'code': 10011, 'msg': u'报名人数已满'}

        if fee != 0 and can_times <= 0:
            if feetype == "gold":
                coin = redis.hget(FORMAT_USER_TABLE % userTable.split(':')[1], 'gold')
                if not coin:
                    coin = 0
                coin = int(coin)
                if coin < fee:
                    return {'code': -1, 'msg': u'您携带的金币数不足支付当前比赛的报名费用(%s)，请充值后进入。' % (fee)}
            elif feetype == "roomCard":
                roomCards = redis.get(USER4AGENT_CARD % (groupId, userTable.split(':')[1]))
                if int(roomCards) < fee:
                    return {'code': -1, 'msg': u'您持有的钻石数不足支付当前比赛的报名费用(%s)，请充值后再进入。' % (fee)}
            elif feetype == "yuanbao":
                print('-' * 77)
                print('feetype==yuanbao')
                print('-' * 77)
                # 元宝领低保
                res = check_vcoin_baselive(uid,threshold)
                if res == 1:
                    return {'code': -2, 'msg': u'您携带的元宝数不足以进入本场次游戏，请充值后进入。'}
                elif res == 2:
                    yuanbao_final = bag_redis.hget(PLAYER_ITEM_HASH % uid, '3')
                    yuanbao_final = int(yuanbao_final) if yuanbao_final else 0
                    record_player_balance_change(bag_redis, userTable, 3, threshold, yuanbao_final, 7)
                    return {'code': 3, 'msg': u'您携带的元宝数不足以进入本场次游戏，系统为您免费补足12元宝。'}
            elif feetype == "prop":
                cur_num = get_player_item(fee_id,uid)
                if cur_num < fee:
                    return {'code': -1, 'msg': u'您携带的道具不足以进入本场次游戏，请充值或兑换后进入。'}

        if threshold != 0:
            if thresholdType == "gold":
                coin = redis.hget(FORMAT_USER_TABLE % userTable.split(':')[1], 'gold')
                if not coin:
                    coin = 0
                coin = int(coin)
                if coin < threshold:
                    return {'code': -1, 'msg': u'您携带的金币数不满足进入当前比赛所需的最低标准(%s)，请充值后进入。' % (threshold)}
            elif thresholdType == "roomCard":
                roomCards = redis.get(USER4AGENT_CARD % (groupId, userTable.split(':')[1]))
                if int(roomCards) < threshold:
                    return {'code': -1, 'msg': u'您持有的钻石数不满足进入当前比赛所需的最低标准(%s)，请充值后再进入。' % (threshold)}
            else:
                pass

        if can_times <= 0:
            # 直接扣取报名费
            print(u'[%s]扣除报名费 类型[%s] 道具ID[%s] 数量[%s]' % (account,feetype,fee_id,fee))
            if int(fee) > 0:
                if feetype == "gold":
                    player_add_gold(redis, account, -fee)
                    gold = redis.hget(userTable, ('gold'))
                    record_player_balance_change(bag_redis, userTable, 2, -fee, gold, 32, gameid)
                elif feetype == "roomCard":
                    player_add_gold(redis, account, 0, -fee)
                    parentAg = redis.hget(userTable, ('parentAg'))
                    card = redis.get(USER4AGENT_CARD % (parentAg, uid))
                    record_player_balance_change(bag_redis, userTable, 1, -fee, card, 32, gameid)
                elif feetype == "yuanbao":
                    cost_player_item(3, uid, int(fee))
                    new_number = bag_redis.hget(PLAYER_ITEM_HASH%uid,str(3))
                    record_player_balance_change(bag_redis, userTable, 3, -fee, new_number, 32, gameid)
                elif feetype == "prop":
                    # ITEM_ATTRS = "attrs:itemid:%s:hash"
                    # item_attrs = bag_redis.hgetall(ITEM_ATTRS % fee_id)
                    # if item_attrs["unit"] == 1:
                    #     fee_id *= 100
                    result = cost_player_item(fee_id, uid, int(fee))
                    if result:
                        print(u'扣除道具(%s)%s个成功'%(fee_id,fee))
                        new_number = bag_redis.hget(PLAYER_ITEM_HASH % uid, str(fee_id))
                        record_player_balance_change(bag_redis, userTable, fee_id, -fee, new_number, 32, gameid)
                    else:
                        print(u'扣除道具(%s)%s个失败'%(fee_id,fee))
                else:
                    print(u'未知报名费类型')
        else:
            print(u'[%s]扣除免费次数' % (account))
        redis.decr(key)

        if D_value_minute <= 5:
            match_players_key = MATCH_WAITTING_PLAYER_SET % id
            players = redis.smembers(match_players_key)
            print u'比赛场内有%s共%s人' % (players, len(players))
            msg = u'报名成功,当前比赛已开放进入,请提前进入比赛等待'
        else:
            msg = u'报名成功,距离比赛还有%s分钟,请留意时间提前进入比赛等待开始'%(int(D_value_minute))
        redis.sadd(Match_enrolment,account)
        redis.sadd(Match_Timging_List%gameid,Match_enrolment)
        return {'code': 0, 'msg': msg}
    else:
        return {'code':-1, 'msg':u'参数错误'}