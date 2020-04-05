#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    统计模型
"""
from web_db_define import *
from config.config import *
from common.log import *
from admin import access_module
import agentModel
from model.userModel import *
from datetime import timedelta,datetime
from operator import itemgetter
from common import convert_util
from common.utilt import get_week_date_obj
from common.mysql_util import MysqlInterface
from decimal import Decimal
import time
#from model.userModel import getAgentAllMemberIds


ACTIVE_OP_LIST = [
        {'url':'/admin/statistics/active/showDay','txt':'查看详细','method':'GET'}
]

def getAllChildAgentId(redis,agentId):
    """
    返回所有下级代理ID
    """
    agentIdList = []
    pipe = redis.pipeline()
    downLines = redis.smembers(AGENT_CHILD_TABLE%(agentId))
    log_debug('[agentModel][Func][getAllChildAgentId] agentId[%s] downlines[%s]'%(agentId,downLines))

    if downLines:
        for downline in downLines:
            agentIdList.append(downline)
            subDownlines = redis.smembers(AGENT_CHILD_TABLE%(downline))
            if subDownlines:
                for subDownline in subDownlines:
                    agentIdList.append(subDownline)

    log_debug('[agentModel][Func][getAllChildAgentId] agentId[%s] allChildIds[%s]'%(agentId,agentIdList))
    return agentIdList

def getDateTotal(redis,agentId,agentIds,endDate,startDate):
    """
    获取某段时间内的总数
    """
    deltaTime = timedelta(1)
    count = 0
    for aid in agentIds:
        nums = redis.get(DAY_ALL_PLAY_COUNT%(endDate,aid))
        if not nums:
            nums = 0
        count+=int(nums)
    #log_debug('[getDateTotal] startDate[%s],endDate[%s] agentIds[%s] count[%s]'%(startDate,endDate,agentIds,count))
    return count

def getCountTotal(redis,agentId,dateStr):
    """
    获取总局数统计数据
    """
    #返回所有下级ID
    parentTable = AGENT_CHILD_TABLE%(agentId)
    agentIds = redis.smembers(parentTable)
    if not agentIds:
        agentIds = [agentId]

    deltaTime = timedelta(1)
    res = []
    totalCount = 0
    for agent_id in agentIds:
        agentDetail = redis.hgetall(AGENT_TABLE%(agent_id))
        count = redis.get(DAY_ALL_PLAY_COUNT%(dateStr,agent_id))
        if not count:
            count = 0
        count = int(count)
        parentTable = AGENT_CHILD_TABLE%(agent_id)
        agent_ids = redis.smembers(parentTable)
        count+=getDateTotal(redis,agent_id,agent_ids,dateStr,dateStr)
        totalCount+=count
        #log_debug('[getAgentActiveReport][FUNC] agentIds[%s] list[%s]'%(agent_id,DAY_AG_LOGIN_COUNT%(agent_id,agentInfo['date'])))

    return int(totalCount)

def get_login_count(redis,selfUid,dateStr,agentIds):
    """
    获取代理当天登录人数统计
    """
    #log_debug('--------------------------[%s][%s]'%(selfUid,dateStr))
    login_count = 0
    if int(selfUid) == 1:
        login_count = redis.scard(FORMAT_LOGIN_DATE_TABLE%(dateStr))
    else:
        for _agentId in agentIds:
            count = redis.get(DAY_AG_LOGIN_COUNT%(_agentId,dateStr))
            if not count:
                count = 0
            login_count+=int(count)
    if not login_count:
        login_count = 0
    #log_debug('[try get_login_count] agentIds[%s] login_count[%s]'%(agentIds,login_count))
    return int(login_count)

def get_take_count(redis,selfUid,dateStr):
    """
    获取代理日消耗钻石统计
    """
    if selfUid == '1':
        regTable = DAY_ALL_PLAY_ROOM_CARD%(dateStr)
        take_count = redis.get(regTable)
    else:
        take_count = agentModel.getAgentRoomByDay(redis,selfUid,dateStr)
    if not take_count:
        take_count = 0
    #log_debug('[try get_take_count] agentIds[%s] take_count[%s]'%(selfUid,take_count))
    return int(take_count)

def get_take_room_count(redis, dateStr, selfUid='1'):
    """
    获取开房数
    """
    take_room_count = 0
    if selfUid == '1':
        loginTable = FORMAT_LOGIN_DATE_TABLE % (dateStr)
        loginSet = redis.smembers(loginTable)
        for loginAccount in loginSet:
            account2user_table = FORMAT_ACCOUNT2USER_TABLE % loginAccount
            userTable = redis.get(account2user_table)
            userId = userTable.split(':')[-1]
            playerDayCard_table = PLAYER_DAY_USE_CARD % (userId, dateStr)
            for playerCard in redis.lrange(playerDayCard_table, 0, -1):
                playerCard = playerCard.split(';')
                if len(playerCard) == 4:
                    if playerCard[1] == '1':
                        take_room_count += 1
    return take_room_count


def get_active_reports(redis,startDate,endDate,selfUid):
    """
    获取活跃人数数据
    """
    try:
        startDate = datetime.strptime(startDate,'%Y-%m-%d')
        endDate   = datetime.strptime(endDate,'%Y-%m-%d')
    except:
        weekDelTime = timedelta(7)
        weekBefore = datetime.now()-weekDelTime
        startDate = weekBefore
        endDate   = datetime.now()

    deltaTime = timedelta(1)
    if int(selfUid) == 1:
        agentIds = []
    else:
        agentIds = getAllChildAgentId(redis,selfUid)

    res = []
    now_time = datetime.now()
    login_proportion = 0
    card_proportion = 0
    take_proportion = 0
    while endDate >= startDate:
        active_info = {}
        if endDate >= now_time:
            endDate -= deltaTime
            continue
        dateStr = endDate.strftime('%Y-%m-%d')
        queryStartDate = time.mktime(time.strptime('%s 00:00:00' % dateStr, '%Y-%m-%d %H:%M:%S'))
        queryEndDate = time.mktime(time.strptime('%s 23:59:59' % dateStr, '%Y-%m-%d %H:%M:%S'))
        login_count = get_login_count(redis,selfUid,dateStr,agentIds)
        take_card  = get_take_count(redis,selfUid,dateStr)
        take_count  = getCountTotal(redis,selfUid,dateStr)
        results = get_match_record(redis, queryStartDate, queryEndDate)
        take_room_count =  get_take_room_count(redis, dateStr)
        match_fee_count = convert_util.to_float(results[1])
        match_enroll_count = convert_util.to_float(results[2])
        match_roomcard_count = convert_util.to_float(results[9])
        match_gamepoint_count = convert_util.to_float(results[10])
        active_info['match_login_count'] = get_match_player_count(redis, queryStartDate, queryEndDate)
        login_proportion += login_count
        card_proportion += take_card
        take_proportion += take_count
        active_info['login_count'] = login_count
        active_info['take_count'] = take_count
        active_info['take_card'] = take_card
        active_info['date'] = dateStr
        active_info['take_room_count'] = take_room_count
        active_info['match_enroll_count'] = match_enroll_count
        active_info['match_fee_count'] = match_fee_count
        active_info['match_roomcard_count'] = match_roomcard_count
        active_info['match_gamepoint_count'] = match_gamepoint_count
        active_info['op'] = ACTIVE_OP_LIST
        res.append(active_info)
        endDate -= deltaTime
    for info in res:
        if login_proportion:
            login_res = round((float(info.get('login_count', 0.0)) / float(login_proportion)) * 100, 2)
            info['login_proportion'] = login_res
        if card_proportion:
            card_res = round((float(info.get('take_card', 0.0)) / float(card_proportion)) * 100, 2)
            info['card_proportion'] = card_res
        if take_proportion:
            task_res = round((float(info.get('take_count', 0.0)) / float(take_proportion)) * 100, 2)
            info['task_proportion'] = task_res
    return {'data':res,'count':len(res)}

def get_login_list(redis,agentId,reg_date):
    """
    获取某个时间段注册人数详情
    params:
        [ reg_date ] : 某一天
    """

    registMemberList =  redis.smembers(FORMAT_LOGIN_DATE_TABLE%(reg_date))

    adminTable = AGENT_TABLE%(agentId)
    agent_type, aId =redis.hmget(adminTable, ('type', 'id'))
    agent_type = convert_util.to_int(agent_type)
    type2getMemberIds = {
            0     :       getSystemMemberIds,
            1     :       getAgentAllMemberIds
    }

    memberIds = None
    if agent_type == 1:
        memberIds = type2getMemberIds[agent_type](redis,agentId)
        if not memberIds:
            return []
    elif agent_type > 1 :
        memberTable = FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE%(agentId)
        memberIds = redis.smembers(memberTable)
        if not memberIds:
            return []

    res = []
    member_id_keys = []
    for member in registMemberList:
        account2user_table = FORMAT_ACCOUNT2USER_TABLE%(member)
        member_id_keys.append(account2user_table)

    #获取会员ID
    member_id_lists = [user_id.split(":")[1] for user_id in redis.mget(member_id_keys)]
    for member_id in member_id_lists:
        if memberIds and (member_id not in memberIds) or (member_id.strip() == 'robot'):
            continue
        use_count = redis.hget(PLAYER_DAY_DATA%(member_id,reg_date),'roomCard')
        use_count = convert_util.to_int(use_count)
        table = FORMAT_USER_TABLE%(member_id) #从账号获得账号信息，和旧系统一样
        account, nickname, headImgUrl, last_logout_date, last_login_date, parentAg = \
            redis.hmget(table, (
            'account', 'nickname', 'headImgUrl', 'last_logout_date', 'last_login_date', 'parentAg'))
        memberInfo = {
                    'userId'        :  member_id,
                    'account'       :  account,
                    'nickname'      :  nickname,
                    'headImgUrl'    :   headImgUrl,
                    'last_logout_date'  : last_logout_date,
                    'last_login_date'   : last_login_date,
                    'parentAg'      :  parentAg,
                    'use_count'     :  use_count
        }
        res.append(memberInfo)
    return res

def get_daily_list(redis, session, startDate, endDate):
    """
    获取每日数据统计
    """
    get_week_date_list = get_week_date_obj(startDate, endDate)
    res = []
    selfUid = session.get('id')
    if selfUid == '-1':
        agentIds = []
    else:
        agentIds = getAllChildAgentId(redis, selfUid)
    for week in get_week_date_list[::-1]:
        info = {}
        info['date'] = week
        info['reg_count'] = redis.scard(FORMAT_REG_DATE_TABLE % (week))
        info['active_count'] = get_login_count(redis, selfUid, week, agentIds)
        info['card_count'] = get_take_count(redis, selfUid, week)
        info['room_count'] = getCountTotal(redis, selfUid, week)
        info['take_room_count'] = get_take_room_count(redis, week)
        # 比赛场数据
        queryStartDate = time.mktime(time.strptime('%s 00:00:00' % week, '%Y-%m-%d %H:%M:%S'))
        queryEndDate = time.mktime(time.strptime('%s 23:59:59' % week, '%Y-%m-%d %H:%M:%S'))
        results = get_match_record(redis, queryStartDate, queryEndDate)
        match_count = convert_util.to_float(results[0])
        match_fee_count = convert_util.to_float(results[1])
        match_enroll_count = convert_util.to_float(results[2])
        match_roomcard_count = convert_util.to_float(results[9])
        match_gamepoint_count = convert_util.to_float(results[10])
        info['match_count'] = match_count
        info['match_enroll_count'] = match_enroll_count
        info['match_fee_count'] = match_fee_count
        info['match_roomcard_count'] = match_roomcard_count
        info['match_gamepoint_count'] = match_gamepoint_count
        info['match_login_count'] = get_match_player_count(redis, queryStartDate, queryEndDate)
        orders = redis.lrange(DAY_ORDER % (week), 0, -1)
        money_count = 0
        saleRoomcard_count = 0
        for order in orders:
            order_table = ORDER_TABLE % order
            if not redis.exists(order_table):
                continue
            money, type, roomCards, presentCards = redis.hmget(order_table, ('money', 'type', 'roomCards', 'presentCards'))
            if type in 'pending':
                continue
            money_count += round(float(money) * 0.01, 2)
            presentCards = presentCards if presentCards else 0
            roomCards = float(roomCards) + float(presentCards)
            saleRoomcard_count += float(roomCards)
        info['money_count'] = money_count
        info['saleRoomcard_count'] = saleRoomcard_count
        yyPoint_count = 0
        cyPoint_count = 0
        # 椰云积分兑换数
        for cocogc_account in redis.smembers(COCOGC_LOGIN_DATE_TABLE % week):
            userTable = redis.get(FORMAT_ACCOUNT2USER_TABLE % cocogc_account)
            userId = userTable.split(':')[-1]
            gamePoint, point = redis.hmget(COCOGC_PLAYER_DAY_DATA % (userId, week), ('gamePoint', 'point'))
            point = gamePoint if gamePoint else 0
            yyPoint_count += int(point)
        info['yyPoint_count'] = yyPoint_count
        # 创盈积分兑换数
        for cocogc_account in redis.smembers(CYGSE_LOGIN_DATE_TABLE % week):
            userTable = redis.get(FORMAT_ACCOUNT2USER_TABLE % cocogc_account)
            userId = userTable.split(':')[-1]
            gamePoint, point = redis.hmget(CYGSE_PLAYER_DAY_DATA % (userId, week), ('gamePoint', 'point'))
            point = gamePoint if gamePoint else 0
            cyPoint_count += int(point)
        info['cyPoint_count'] = cyPoint_count
        compensate_card_table = COMPENSATE_CARD_DAY % week
        # 增加钻石
        compensate_roomcard = 0
        if redis.exists(compensate_card_table):
            for compensate in redis.lrange(COMPENSATE_CARD_DAY % week, 0, -1):
                _, _, _, card, _, _ = compensate.split('|')
                compensate_roomcard += int(card)
        info['compensate_roomcard'] = compensate_roomcard
        compensate_point_table = COMPENSATE_POINT_DAY % week
        # 增加积分
        compensate_gamepoint = 0
        if redis.exists(compensate_point_table):
            for compensate in redis.lrange(compensate_point_table, 0, -1):
                _, _, _, card, _, _ = compensate.split('|')
                compensate_gamepoint += int(card)
        info['compensate_gamepoint'] = compensate_gamepoint
        # 当天后台邮件发送附件
        if redis.exists('email:send:enclosure:%s:hash' % week):
            mailRoomcard_count, mailPoint_count = redis.hmget('email:send:enclosure:%s:hash' % week, ('roomCard', 'gamePoint'))
        else:
            mailRoomcard_count, mailPoint_count = 0, 0
        info['mailRoomcard_count'] = convert_util.to_float(mailRoomcard_count)
        info['mailPoint_count'] = convert_util.to_float(mailPoint_count)
        # 玩家分享钻石数
        shareGame_roomcard = redis.get(SHARE_GAME_DATE_TOTAL_KEY % week)
        shareGame_roomcard if shareGame_roomcard else 0
        info['shareGame_roomcard'] = convert_util.to_float(shareGame_roomcard)
        res.append(info)
    return res


def get_usersave_list(redis, session, startDate, endDate, model):
    get_week_date_list = get_week_date_obj(startDate, endDate)
    res = []
    for week in get_week_date_list:
        info = {}
        info['date'] = week
        if model in ['reg', 'matchReg']:
            reg_data = redis.smembers(FORMAT_REG_DATE_TABLE % (week))
        if model in ['login']:
            reg_data = redis.smembers(FORMAT_LOGIN_DATE_TABLE % week)
        if model in ['matchLogin']:
            queryStartDate = time.mktime(time.strptime('%s 00:00:00' % week, '%Y-%m-%d %H:%M:%S'))
            queryEndDate = time.mktime(time.strptime('%s 23:59:59' % week, '%Y-%m-%d %H:%M:%S'))
            queryStr = """select user_id from match_player  WHERE create_time >= %s and create_time <= %s GROUP BY user_id""" % (
                queryStartDate, queryEndDate)
            results = MysqlInterface.query(sql=queryStr)
            if results:
                login_data = map(lambda x: x[0], results)
                reg_data = set([redis.hget(FORMAT_USER_TABLE % i, 'account') for i in login_data])
            else:
                reg_data = set()
        info['reg_count'] = len(reg_data)
        info['one_save'] = saveDate(redis, session, model, reg_data, week, 1)
        info['two_save'] = saveDate(redis, session, model, reg_data, week, 2)
        info['three_save'] = saveDate(redis, session, model, reg_data, week, 3)
        info['four_save'] = saveDate(redis, session, model, reg_data, week, 4)
        info['five_save'] = saveDate(redis, session, model, reg_data, week, 5)
        info['six_save'] = saveDate(redis, session, model, reg_data, week, 6)
        info['seven_save'] = saveDate(redis, session, model, reg_data, week, 7)
        info['fifteen_save'] = saveDate(redis, session, model, reg_data, week, 15)
        info['thirty_save'] = saveDate(redis, session, model, reg_data, week, 30)
        res.append(info)
    return res

def saveDate(redis, session, model, regDate, week, day):
    """留存占比"""
    import datetime
    curTime = datetime.datetime.now()
    toDay = curTime.strftime("%Y-%m-%d")
    reg_set = regDate
    for i in range(1, day+1):
        next_day = datetime.datetime.strptime(week, '%Y-%m-%d') + datetime.timedelta(days=i)
        next_day = next_day.strftime('%Y-%m-%d')
        if next_day > toDay:
            return ''
        if model in ['matchReg', 'matchLogin']:
            queryStartDate = time.mktime(time.strptime('%s 00:00:00' % next_day, '%Y-%m-%d %H:%M:%S'))
            queryEndDate = time.mktime(time.strptime('%s 23:59:59' % next_day, '%Y-%m-%d %H:%M:%S'))
            if redis.exists('match:login:start:%s:end:%s:key' % (queryStartDate, queryEndDate)):
                login_data = redis.get('match:login:start:%s:end:%s:key' % (queryStartDate, queryEndDate))
                login_data = eval(login_data)
            else:
                queryStr = """select user_id from match_player  WHERE create_time >= %s and create_time <= %s GROUP BY user_id""" % (queryStartDate, queryEndDate)
                results = MysqlInterface.query(sql=queryStr)
                if results:
                    login_data = map(lambda x: x[0], results)
                    login_data = set([ redis.hget(FORMAT_USER_TABLE % i, 'account') for i in login_data])
                else:
                    login_data = set()
                redis.set('match:login:start:%s:end:%s:key' % (queryStartDate, queryEndDate), login_data)
                redis.expire('match:login:start:%s:end:%s:key' % (queryStartDate, queryEndDate), 60)
        else:
            login_data = redis.smembers(FORMAT_LOGIN_DATE_TABLE % (next_day))
        reg_set = login_data & reg_set
        retention = 0
    if reg_set:
        retention = round(float(len(reg_set)) / float(len(regDate)) * 100, 2)
    return '%s %s%%' % (len(reg_set), retention)


def today_count(redis, session, selfUid, dateStr):
    """
    获取当天数据
    """
    # 当天注册人数
    reg_count = redis.scard(FORMAT_REG_DATE_TABLE % (dateStr))
    if not reg_count:
        reg_count = 0

    # 当天活跃人数
    active_count = redis.scard(FORMAT_LOGIN_DATE_TABLE % (dateStr))
    if not active_count:
        active_count = 0

    # 当天钻石耗钻
    take_count = redis.get(DAY_ALL_PLAY_ROOM_CARD % (dateStr))
    if not take_count:
        take_count = 0

    # 玩家充值金额
    orders = redis.lrange(DAY_ORDER % (dateStr), 0, -1)
    money_count = 0
    for order in orders:
        order_table = ORDER_TABLE % order
        if not redis.exists(order_table):
            continue
        money, type = redis.hmget(order_table, ('money', 'type'))
        if type in ['pending']:
            continue
        money_count += round(float(money) * 0.01, 2)

    # 我的售钻数
    agent_sale_card_table = AGENT_SALE_CARD_DATE % (selfUid, dateStr)
    if redis.exists(agent_sale_card_table):
        sale_report_count = redis.hget(agent_sale_card_table, 'totalNums')
    else:
        sale_report_count = 0

    # 下线代理售钻数、下线代理购钻数、局数统计、我的利润总占额、下线代理总占额
    agent_child_set = redis.smembers(AGENT_CHILD_TABLE % selfUid)
    sub_sale_reprot_count = 0
    sub_buy_reprot_count = 0
    room_count = 0
    rate_report_count = 0
    rate_report_agent_count = 0
    for subAgentId in agent_child_set:
        sub_sale_reprot = 0
        sub_buy_reprot = 0
        if redis.exists(AGENT_SALE_CARD_DATE % (subAgentId, dateStr)):
            sub_sale_reprot = redis.hget(AGENT_SALE_CARD_DATE % (subAgentId, dateStr), 'totalNums')
        if redis.exists(AGENT_BUY_CARD_DATE % (subAgentId, dateStr)):
            sub_buy_reprot = redis.hget(AGENT_BUY_CARD_DATE % (subAgentId, dateStr), 'totalNums')
        sub_sale_reprot_count += int(sub_sale_reprot)
        sub_buy_reprot_count += int(sub_buy_reprot)

        count = redis.get(DAY_ALL_PLAY_COUNT % (dateStr, subAgentId))
        if not count:
            count = 0
        count = int(count)
        parentTable = AGENT_CHILD_TABLE % (subAgentId)
        agent_ids = redis.smembers(parentTable)
        count += getDateTotal(redis, subAgentId, agent_ids, dateStr, dateStr)
        room_count += count

        # agent_id = subAgentId
        # agentTable = AGENT_TABLE % (agent_id)
        # aType, parentId = redis.hmget(agentTable, ('type', 'parent_id'))
        # if aType in ['2', '3']:
        #     agentPerPriceList = redis.smembers(AGENT_ROOMCARD_PER_PRICE % (parentId))
        # else:
        #     agentPerPriceList = redis.smembers(AGENT_ROOMCARD_PER_PRICE % (agent_id))
        # agentRateList = redis.smembers(AGENT_RATE_SET % (agent_id))
        # for price in agentPerPriceList:
        #     for rate in agentRateList:
        #         agentRateTable = AGENT_RATE_DATE % (agent_id, rate, price, dateStr)
        #         if redis.exists(agentRateTable):
        #             agentRate = redis.hgetall(agentRateTable)
        #             if agent_id == selfUid and 'superRateTotal' in agentRate and 'rateTotal' in agentRate:
        #                 agentRate['superRateTotal'] = 0
        #                 agentRate['rateTotal'] = 0
        #             rate_report_count += float(agentRate.get("superRateTotal", 0))
        #             rate_report_agent_count += float(agentRate.get("rateTotal", 0))

    return {
        'reg_count': reg_count, 'active_count': active_count, 'take_count': take_count,
        'room_count': room_count, 'money_count': money_count, 'sale_report_count': sale_report_count,
        'sub_sale_reprot_count': sub_sale_reprot_count, 'sub_buy_reprot_count': sub_buy_reprot_count,
        'rate_report_count': 0, 'rate_report_agent_count': 0
    }


def tomonth_count(redis, session, selfUid, monthStr):
    """
    获取当月数据
    """
    # 当天注册人数
    import calendar
    import datetime
    year, month = monthStr.split('-')
    monthRange = calendar.monthrange(int(year), int(month))

    startDate = datetime.datetime(year=int(year), month=int(month), day=1)
    endDate = datetime.datetime(year=int(year), month=int(month), day=int(monthRange[1]))

    reg_count = 0
    active_count = 0
    take_count = 0
    room_count = 0
    money_count = 0
    sale_report_count = 0
    sub_sale_reprot_count = 0
    sub_buy_reprot_count = 0
    rate_report_count = 0
    rate_report_agent_count = 0
    agent_child_set = redis.smembers(AGENT_CHILD_TABLE % selfUid)

    deltaTime = timedelta(1)
    now_time = datetime.datetime.now()
    while startDate <= endDate:
        if startDate > now_time:
            break
        dateStr = startDate.strftime('%Y-%m-%d')

        # 当月注册人数
        reg_total = redis.scard(FORMAT_REG_DATE_TABLE % (dateStr))
        if not reg_total:
            reg_total = 0

        # 当月活跃人数
        active_total = redis.scard(FORMAT_LOGIN_DATE_TABLE % (dateStr))
        if not active_total:
            active_total = 0

        # 当天钻石耗钻
        take_total = redis.get(DAY_ALL_PLAY_ROOM_CARD % (dateStr))
        if not take_total:
            take_total = 0

        # 玩家充值金额
        orders = redis.lrange(DAY_ORDER % (dateStr), 0, -1)
        money_total = 0
        for order in orders:
            order_table = ORDER_TABLE % order
            if not redis.exists(order_table):
                continue
            money = redis.hget(order_table, 'money')
            money_total += round(float(money) * 0.01, 2)

        # 我的售钻数
        agent_sale_card_table = AGENT_SALE_CARD_DATE % (selfUid, dateStr)
        if redis.exists(agent_sale_card_table):
            sale_card_count = redis.hget(agent_sale_card_table, 'totalNums')
        else:
            sale_card_count = 0

        # 下线代理售钻数、下线代理购钻数、局数统计、我的利润总占额、下线代理总占额
        sub_sale_reprot_total = 0
        sub_buy_reprot_total = 0
        room_total = 0
        rate_report_total = 0
        rate_report_agent_total = 0
        for subAgentId in agent_child_set:
            sub_sale_reprot = 0
            sub_buy_reprot = 0
            if redis.exists(AGENT_SALE_CARD_DATE % (subAgentId, dateStr)):
                sub_sale_reprot = redis.hget(AGENT_SALE_CARD_DATE % (subAgentId, dateStr), 'totalNums')
            if redis.exists(AGENT_BUY_CARD_DATE % (subAgentId, dateStr)):
                sub_buy_reprot = redis.hget(AGENT_BUY_CARD_DATE % (subAgentId, dateStr), 'totalNums')
            sub_sale_reprot_total += int(sub_sale_reprot)
            sub_buy_reprot_total += int(sub_buy_reprot)

            count = redis.get(DAY_ALL_PLAY_COUNT % (dateStr, subAgentId))
            if not count:
                count = 0
            count = int(count)
            parentTable = AGENT_CHILD_TABLE % (subAgentId)
            agent_ids = redis.smembers(parentTable)
            count += getDateTotal(redis, subAgentId, agent_ids, dateStr, dateStr)
            room_total += count

            # agent_id = subAgentId
            # agentTable = AGENT_TABLE % (agent_id)
            # aType, parentId = redis.hmget(agentTable, ('type', 'parent_id'))
            # if aType in ['2', '3']:
            #     agentPerPriceList = redis.smembers(AGENT_ROOMCARD_PER_PRICE % (parentId))
            # else:
            #     agentPerPriceList = redis.smembers(AGENT_ROOMCARD_PER_PRICE % (agent_id))
            # agentRateList = redis.smembers(AGENT_RATE_SET % (agent_id))
            # for price in agentPerPriceList:
            #     for rate in agentRateList:
            #         agentRateTable = AGENT_RATE_DATE % (agent_id, rate, price, dateStr)
            #         if redis.exists(agentRateTable):
            #             agentRate = redis.hgetall(agentRateTable)
            #             if agent_id == selfUid and 'superRateTotal' in agentRate and 'rateTotal' in agentRate:
            #                 agentRate['superRateTotal'] = 0
            #                 agentRate['rateTotal'] = 0
            #             rate_report_total += float(agentRate.get("superRateTotal", 0))
            #             rate_report_agent_total += float(agentRate.get("rateTotal", 0))

        reg_count += reg_total
        active_count += active_total
        take_count += int(take_total)
        money_count += money_total
        sale_report_count += int(sale_card_count)
        sub_sale_reprot_count += sub_sale_reprot_total
        sub_buy_reprot_count += sub_buy_reprot_total
        room_count += room_total
        rate_report_count += rate_report_total
        rate_report_agent_count += rate_report_agent_total

        startDate += deltaTime

    return {
        'reg_count': reg_count, 'active_count': active_count, 'take_count': take_count,
        'room_count': room_count, 'money_count': money_count, 'sale_report_count': sale_report_count,
        'sub_sale_reprot_count': sub_sale_reprot_count, 'sub_buy_reprot_count': sub_buy_reprot_count,
        'rate_report_count': 0, 'rate_report_agent_count': 0
    }


def tototal_count(redis, session, selfUid):
    """
    获取总计数据
    """
    def get_AllKeys(key):
        key_list = []
        cursor = 0
        while True:
            next_cursor, keys = redis.scan(cursor, key, 500)
            if keys:
                key_list.extend(keys)
            if next_cursor:
                cursor = next_cursor
            else:
                break
        return key_list

    agent_child_set = redis.smembers(AGENT_CHILD_TABLE % selfUid)
    reg_keys = get_AllKeys(FORMAT_REG_DATE_TABLE % '*')  # 当天注册人数
    active_keys = get_AllKeys(FORMAT_LOGIN_DATE_TABLE % '*')  # 当天活跃人数
    roomcard_keys = get_AllKeys(DAY_ALL_PLAY_ROOM_CARD % '*')  # 当天钻石耗钻
    roomtotal_keys = get_AllKeys(DAY_ALL_PLAY_COUNT % ('*', '*'))  # 局数统计
    order_keys = get_AllKeys(DAY_ORDER % '*')  # 玩家充值金额
    saleCard_keys = get_AllKeys(AGENT_SALE_CARD_DATE % (selfUid, '*'))  # 我的售钻数
    sub_saleCard_keys = []
    sub_buyCard_keys = []
    rate_keys = []
    for subAgentId in agent_child_set:
        sub_saleCard_list = get_AllKeys(AGENT_SALE_CARD_DATE % (subAgentId, '*'))
        sub_saleCard_keys.extend(sub_saleCard_list)

        sub_buyCard_list = get_AllKeys(AGENT_BUY_CARD_DATE % (subAgentId, '*'))
        sub_buyCard_keys.extend(sub_buyCard_list)

        rate_list = get_AllKeys(AGENT_RATE_DATE % (subAgentId, '*', '*', '*'))
        rate_keys.extend(rate_list)

    reg_count = 0
    active_count = 0
    take_count = 0
    room_count = 0
    money_count = 0
    sale_report_count = 0
    sub_sale_reprot_count = 0
    sub_buy_reprot_count = 0
    rate_report_count = 0
    rate_report_agent_count = 0

    for regkey in reg_keys:
        reg_count += redis.scard(regkey)

    for activekey in active_keys:
        active_count += redis.scard(activekey)

    for roomcardkey in roomcard_keys:
        roomcard = redis.get(roomcardkey)
        if not roomcard:
            roomcard = 0
        take_count += int(roomcard)

    for roomtotalkey in roomtotal_keys:
        roomtotal = redis.get(roomtotalkey)
        if not roomtotal:
            roomtotal = 0
        room_count += int(roomtotal)

    for orderkey in order_keys:
        orders = redis.lrange(orderkey, 0, -1)
        count = 0
        for order in orders:
            order_table = ORDER_TABLE % order
            if not redis.exists(order_table):
                continue
            money = redis.hget(order_table, 'money')
            count += round(float(money) * 0.01, 2)
        money_count += count

    for salecardekey in saleCard_keys:
        sale_report = redis.hget(salecardekey, 'totalNums')
        if not sale_report:
            sale_report = 0
        sale_report_count += int(sale_report)

    for subsalecardkey in sub_saleCard_keys:
        sub_sale_reprot = redis.hget(subsalecardkey, 'totalNums')
        if not sub_sale_reprot:
            sub_sale_reprot = 0
        sub_sale_reprot_count += int(sub_sale_reprot)

    for subbuycardkey in sub_buyCard_keys:
        sub_buy_reprot = redis.hget(subbuycardkey, 'totalNums')
        if not sub_buy_reprot:
            sub_buy_reprot = 0
        sub_buy_reprot_count += int(sub_buy_reprot)

    # for ratekey in rate_keys:
    #     agent_id = ratekey.split(':')[1]
    #     agentRate = redis.hgetall(ratekey)
    #     if agent_id == selfUid and 'superRateTotal' in agentRate and 'rateTotal' in agentRate:
    #         superRateTotal= 0
    #         rateTotal = 0
    #     else:
    #         superRateTotal = agentRate.get("superRateTotal", 0)
    #         rateTotal = agentRate.get("rateTotal", 0)
    #     rate_report_count += float(superRateTotal)
    #     rate_report_agent_count += float(rateTotal)

    return {
        'reg_count': reg_count, 'active_count': active_count, 'take_count': take_count,
        'room_count': room_count, 'money_count': money_count, 'sale_report_count': sale_report_count,
        'sub_sale_reprot_count': sub_sale_reprot_count, 'sub_buy_reprot_count': sub_buy_reprot_count,
        'rate_report_count': 0, 'rate_report_agent_count': 0
    }

def phone_Proportion(redis, session, uid, dateStr):
    """
    获取当前用户终端占比
    """
    login_data = redis.smembers(FORMAT_LOGIN_DATE_TABLE % dateStr)

    web_Browser = 0
    android = 0
    ios = 0
    unknown = 0

    for user in login_data:
        userTable = redis.get(FORMAT_ACCOUNT2USER_TABLE % user)
        if userTable:
            clientKind = redis.hget(userTable, 'lastLoginClientType')
            if clientKind == '0':
                web_Browser += 1
                continue
            if clientKind == '1':
                android += 1
                continue
            if clientKind == '2':
                ios += 1
                continue
            else:
                unknown += 1
                continue
    # return [['Web Browser', web_Browser], ['Android', android], ['IOS', ios], ['unknown', unknown]]
    import json
    return {'web_Browser': web_Browser, 'android': android, 'ios': ios, 'unknown': unknown}


def get_match_reports(redis, condition):
    """获取比赛场数据"""
    res = []
    conditionStr = "game_id={game_id} and match_id={match_id} and match_number='{match_number}' and total_award_type={total_award_type} and matchState={matchState} and end_time>={start_time} and end_time<={end_time} order by {sortName} {sortOrder}".format(
        **condition)
    whereStr = 'and'.join([i for i in conditionStr.split('and') if ('= ') not in i and "=''" not in i])
    queryStr = """select * from match_record where %s limit %s,%s""" % (whereStr, condition['pageNumber'], condition['pageSize'])
    totalStr = """select count(1) from match_record where %s""" % whereStr
    count = MysqlInterface.query_one(sql=totalStr)
    if count:
        results = MysqlInterface.query(sql=queryStr)
        nums = condition['pageNumber']
        for _result in results:
            info = dict(zip(('id', 'game_id', 'match_id', 'match_number', 'user_ids','serviceTag','fee_type', 'total_fee', 'total_num', 'total_award_type',
                      'total_award_num', 'balance_datas', 'match_Info', 'start_time', 'end_time', 'matchState', 'dismissReason',
                      'create_time', 'update_time', 'delete_time', 'is_deleted'), _result))
            nums += 1
            info['num_id'] = nums
            info['start_time'] = time.strftime('%Y-%m-%d %H:%M', time.localtime(info['start_time'])) if info.get(
                'start_time', None) else ''
            info['end_time'] = time.strftime('%Y-%m-%d %H:%M', time.localtime(info['end_time'])) if info.get(
                'end_time', None) else ''
            gameTable = GAME_TABLE % (info.get('game_id'))
            info['game_name'] = redis.hget(gameTable, 'name')
            info['op'] = [
                {'url': '/admin/statistics/match/info', 'method': 'POST', 'txt': '赛事详情'},
            ]
            res.append(info)
    else:
        count = [0]
    return {"count": count[0], "data": res}


def get_match_player_reports(redis, condition):
    """比赛场用户数据"""
    res = []
    # conditionStr = "user_id={user_id} and game_id={game_id} and match_id={match_id} and match_number='{match_number}' and reward_type={reward_type} and rank={rank} and create_time>={start_time} and create_time<={end_time} order by create_time desc".format(**condition)
    conditionStr = "player.user_id={user_id} and player.game_id={game_id} and player.match_id={match_id} and player.match_number='{match_number}' and record.total_award_type={reward_type} and player.rank={rank} and record.end_time>={start_time} and record.end_time<={end_time} order by {sortName} {sortOrder}".format(**condition)
    whereStr = 'and'.join([i for i in conditionStr.split('and') if ('= ') not in i and "=''" not in i])
    queryStr = """SELECT
	player.user_id AS '用户ID',
	player.game_id AS '游戏ID',
	player.match_id AS '场次ID',
	player.match_number AS '赛事编号' ,
	record.total_award_type AS '赛事类型',
	player.fee_type AS '报名费类型',
	player.fee AS '报名费用',
	player.score AS '比赛分数',
	player.rank AS '比赛名次',
	player.reward_type AS '奖励类型',
	player.reward_fee AS '奖励数',
	record.end_time AS '赛事时间'
	FROM match_player AS player 
	LEFT JOIN match_record AS record ON player.match_number = record.match_number 
	WHERE %s LIMIT %s, %s
    """ % (whereStr, condition['pageNumber'], condition['pageSize'])
    # queryStr = """select * from match_player where %s limit %s,%s""" % (whereStr, condition['pageNumber'], condition['pageSize'])
    # totalStr = """select count(1) from match_player where %s""" % whereStr
    totalStr = """
    SELECT count( 1 ) 
    FROM match_player AS player 
    LEFT JOIN match_record AS record ON player.match_number = record.match_number 
    WHERE %s 
    """ % whereStr
    count = MysqlInterface.query_one(sql=totalStr)
    if count:
        results = MysqlInterface.query(sql=queryStr)
        nums = condition['pageNumber']
        for _result in results:
            info = dict(zip(('user_id', 'game_id', 'match_id', 'match_number', 'total_award_type', 'fee_type', 'fee', 'score', 'rank',
                      'reward_type', 'reward_fee', 'end_time'), _result))
            nums += 1
            nickname, account = redis.hmget(FORMAT_USER_TABLE % info['user_id'], ('nickname', 'account'))
            info['num_id'] = nums
            info['nickname'] = nickname
            info['account'] = account
            info['end_time'] = time.strftime('%Y-%m-%d %H:%M', time.localtime(info['end_time'])) if info.get('end_time', 0) else ''
            res.append(info)
    else:
        count = [0]
    return {"count": count[0], "data": res}


def get_match_player_count(redis, queryStartDate, queryEndDate):
    """"
    返回比赛场参与人数总和 [总条数]
    """
    # if redis.exists(MATCH_LOGIN_DATE_KEY % (queryStartDate, queryEndDate)):
    #     return redis.get(MATCH_LOGIN_DATE_KEY % (queryStartDate, queryEndDate))
    try:
        # queryStr = """select count(1) from(SELECT count(1)
        # FROM match_player
        # where create_time >= %s and create_time <= %s
        # group by user_id ) player ;""" % (queryStartDate, queryEndDate)
        queryStr = """SELECT
        count( 1 ) FROM (SELECT count( 1 ) FROM match_player AS player
		LEFT JOIN match_record AS record ON player.match_number = record.match_number 
		WHERE record.end_time >= %s AND record.end_time <= %s GROUP BY player.user_id ) A
		""" % (queryStartDate, queryEndDate)
        results = MysqlInterface.query_one(sql=queryStr)
        if results:
            count = convert_util.to_int(results[0])
        else:
            count = 0
        # redis.set(MATCH_LOGIN_DATE_KEY % (queryStartDate, queryEndDate), count)
        # redis.expire(MATCH_LOGIN_DATE_KEY % (queryStartDate, queryEndDate), MATCH_CACHE_TIME)
    except Exception as err:
        count = 0
    return count

def get_match_record(redis, queryStartDate, queryEndDate, condition=None, queryAll=None):
    """
    返回比赛场各总和 [总条数, 总报名费用, 总报名人数, 钻石场报名人数, 积分场报名人数, 钻石奖励总数, 积分奖励总数]
    """
    # if redis.exists(MATCH_RECORD_DATE_SET % (queryStartDate, queryEndDate)):
    #     return eval(redis.get(MATCH_RECORD_DATE_SET % (queryStartDate, queryEndDate)))
    record_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    try:
        queryStr = """select count(1) as '总条数', 
        sum(total_fee) as '总报名费用', 
        sum(total_num) as '总报名人数', 
        count( IF (total_award_type = 1 ,1, null)) '钻石场总数',
        count( IF (total_award_type = 3 ,1, null)) '积分场总数', 
        sum( IF (( total_award_type = 1 ), total_fee, 0 ) ) as '钻石场报名费用', 
        sum( IF (( total_award_type = 3 ), total_fee, 0 ) ) as '积分场报名费用', 
        sum( IF (( total_award_type = 1 ), total_num, 0 ) ) as '钻石场报名人数', 
        sum( IF (( total_award_type = 3 ), total_num, 0 ) ) as  '积分场报名人数', 
        sum( IF (( total_award_type = 1), total_award_num, 0 ) ) as '钻石奖励总数', 
        sum( IF (( total_award_type = 3), total_award_num, 0 ) ) as '积分奖励总数' 
        from match_record where end_time>=%s and end_time<=%s""" % (queryStartDate, queryEndDate)
        if condition:
            queryStr += ('and %s' % condition)
        if queryAll:
            results = MysqlInterface.query(sql=queryStr)
            return results
        else:
            results = MysqlInterface.query_one(sql=queryStr)
        if results:
            record_count = map(int, results)
        # redis.set(MATCH_RECORD_DATE_SET % (queryStartDate, queryEndDate), record_count)
        # redis.expire(MATCH_RECORD_DATE_SET % (queryStartDate, queryEndDate), MATCH_CACHE_TIME)
    except Exception as err:
        pass
    return record_count

def get_match_record_game(redis, queryStartDate, queryEndDate):
    """
    返回比赛场各总和 [总条数, 总报名费用, 总报名人数, 钻石场报名人数, 积分场报名人数, 钻石奖励总数, 积分奖励总数]
    """
    # if redis.exists(MATCH_RECORD_GAME_DATE_SET % (queryStartDate, queryEndDate)):
    #     return eval(redis.get(MATCH_RECORD_GAME_DATE_SET % (queryStartDate, queryEndDate)))
    record_count = []
    try:
        queryStr = """SELECT game_id as '游戏ID',
        sum( total_fee ) as '报名总费用',
        count(IF (total_award_type in (1,3),1 , null)) as '总场数',
        count(IF ( total_award_type = 1, 1, NULL )) AS '钻石赛总数',
        count(IF ( total_award_type = 3, 1, NULL )) AS '积分赛总数',
        sum( total_num ) as '报名总人数',
        sum( IF (( total_award_type = 1 ), total_num, 0 ) ) as '钻石赛报名人总数',
        sum( IF (( total_award_type = 3 ), total_num, 0 ) ) as '积分赛报名人总数',
        sum( IF (( total_award_type = 1 ), total_fee, 0 ) ) as '钻石赛报名费总数',
        sum( IF (( total_award_type = 3 ), total_fee, 0 ) ) as '积分赛报名费总数',
        sum( IF (( total_award_type = 1 ), total_award_num, 0 ) ) as '钻石赛奖励总数',
        sum( IF (( total_award_type = 3 ), total_award_num, 0 ) ) as '积分赛奖励总数'
        FROM match_record  WHERE end_time >= %s AND end_time <= %s
        GROUP BY game_id""" % (queryStartDate, queryEndDate)
        results = MysqlInterface.query(sql=queryStr)
        if results:
            return results
        else:
            return record_count
        # redis.set(MATCH_RECORD_GAME_DATE_SET % (queryStartDate, queryEndDate), results)
        # redis.expire(MATCH_RECORD_GAME_DATE_SET % (queryStartDate, queryEndDate), MATCH_CACHE_TIME)
    except Exception as err:
        pass
    return record_count


def get_match_active_data(redis, queryStartDate, queryEndDate, condition=None):
    """
    获取比赛场活跃人数统计
    """
    active_results = [0, 0, 0]
    try:
        if condition:
            condition += ('and end_time >=%s and end_time <= %s' % (queryStartDate, queryEndDate))
        else:
            condition = 'end_time >=%s and end_time <= %s' % (queryStartDate, queryEndDate)
        queryStr = """SELECT sum(total_num), sum(total_roomcat), sum(total_gamepoint) FROM (SELECT count(distinct player.user_id ) AS 'total_num',count(distinct IF( record.total_award_type = 1, 1, NULL )) AS 'total_roomcat' ,count(distinct IF( record.total_award_type = 3, 1, NULL )) AS 'total_gamepoint' FROM match_player AS player LEFT JOIN match_record AS record ON player.match_number = record.match_number WHERE %s GROUP BY player.user_id ) A""" % (condition)
        results = MysqlInterface.query_one(sql=queryStr)
        if results:
            return results
        else:
            return active_results
    except Exception as err:
        print(err)
    return active_results