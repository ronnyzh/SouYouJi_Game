#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    数据统计模块
"""
from bottle import *
from admin import admin_app
from config.config import STATIC_LAYUI_PATH,STATIC_ADMIN_PATH,BACK_PRE,RES_VERSION
from common.utilt import *
from common.log import *
from datetime import datetime
from web_db_define import *
from model.orderModel import *
from model.agentModel import *
from model.statisticsModel import *
from model.userModel import *
from common.mysql_util import MysqlInterface
from common import log_util,convert_util,web_util
from db_define.db_define_consts import *
from model.matchModel import *
from db_define.db_define_consts import *
import json
import copy


@admin_app.get('/statistics/buyReport')
@checkAccess
def getBuyReport(redis,session):
    """
    获取代理的订单报表
    """
    lang      = getLang()

    isList = request.GET.get('list','').strip()
    startDate = request.GET.get('startDate','').strip()
    endDate = request.GET.get('endDate','').strip()

    selfAccount,selfUid = session['account'],session['id']

    if not startDate or not endDate:
        #默认显示一周时间
        startDate,endDate = getDaya4Week()

    if isList:
        reports = getBuyCardReport(redis,selfUid,startDate,endDate)
        return json.dumps(reports)
    else:
        info = {
                'title'         :    '[%s]购钻报表'%(selfAccount),
                'searchStr'     :    '',
                'showLogType'   :    '',
                'startDate'     :    startDate,
                'endDate'       :    endDate,
                'listUrl'       :    BACK_PRE+'/statistics/buyReport?list=1',
                'STATIC_LAYUI_PATH'      :   STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :   STATIC_ADMIN_PATH
        }

        return template('admin_report_buy',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/statistics/saleReport')
@checkAccess
def getSaleReport(redis,session):
    """
    获取代理的订单报表
    """
    lang      = getLang()

    isList = request.GET.get('list','').strip()
    startDate = request.GET.get('startDate','').strip()
    endDate = request.GET.get('endDate','').strip()

    selfAccount,selfUid = session['account'],session['id']

    if not startDate or not endDate:
        #默认显示一周时间
        startDate,endDate = getDaya4Week()

    if isList:
        reports = getSaleCardReport(redis,selfUid,startDate,endDate)
        return json.dumps(reports)
    else:
        info = {
                'title'         :    '[%s]售钻报表'%(selfAccount),
                'searchStr'     :    '',
                'showLogType'   :    '',
                'startDate'     :    startDate,
                'endDate'       :    endDate,
                'listUrl'       :    BACK_PRE+'/statistics/saleReport?list=1',
                'STATIC_LAYUI_PATH'      :   STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :   STATIC_ADMIN_PATH
        }

        return template('admin_report_sale',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/statistics/allAgentSaleReport')
@checkAccess
def getAgentSaleReport(redis,session):
    """
    获取下线代理的售钻订单报表
    """
    lang      = getLang()

    isList = request.GET.get('list','').strip()
    startDate = request.GET.get('startDate','').strip()
    endDate = request.GET.get('endDate','').strip()
    group_id = request.GET.get('group_id','').strip()

    selfAccount,selfUid = session['account'],session['id']

    if not startDate or not endDate:
        #默认显示一周时间
        startDate,endDate = getDaya4Week()

    if isList:
        reports = getAgentSaleCardReport(redis,selfUid,startDate,endDate,group_id)
        return json.dumps(reports)
    else:
        info = {
                'title'         :    '[%s]的下线代理售钻报表'%(selfAccount),
                'searchStr'     :    '',
                'showLogType'   :    '',
                'startDate'     :    startDate,
                'endDate'       :    endDate,
                'group_search'  :    True,#开启代理查询
                'listUrl'       :    BACK_PRE+'/statistics/allAgentSaleReport?list=1',
                'STATIC_LAYUI_PATH'      :   STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :   STATIC_ADMIN_PATH
        }

        return template('admin_report_agent_sale',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/statistics/allAgentBuyReport')
@checkAccess
def getAgentBuyReport(redis,session):
    """
    获取下线代理的购钻订单报表
    """
    lang      = getLang()

    isList = request.GET.get('list','').strip()
    startDate = request.GET.get('startDate','').strip()
    endDate = request.GET.get('endDate','').strip()
    group_id = request.GET.get('group_id','').strip()

    selfAccount,selfUid = session['account'],session['id']

    if not startDate or not endDate:
        #默认显示一周时间
        startDate,endDate = getDaya4Week()

    if isList:
        reports = getAgentBuyCardReport(redis,selfUid,startDate,endDate,group_id)
        return json.dumps(reports)
    else:
        info = {
                'title'         :    '[%s]的下线代理购钻报表'%(selfAccount),
                'searchStr'     :    '',
                'showLogType'   :    '',
                'startDate'     :    startDate,
                'endDate'       :    endDate,
                'group_search'  :    True,#开启代理查询
                'listUrl'       :    BACK_PRE+'/statistics/allAgentBuyReport?list=1',
                'STATIC_LAYUI_PATH'      :   STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :   STATIC_ADMIN_PATH
        }

        return template('admin_report_agent_buy',info=info,lang=lang,RES_VERSION=RES_VERSION)



def getTimeList(begin_date,end_date):
    date_list = []
    begin_date = datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += timedelta(days=1)
    return date_list


def get_downline_rate(redis,date,my_downline_agents):
    """
    获取下线抽成的列表(循环查询)
    """
    RateReportList = []
    for agent_id in my_downline_agents:
        agentTable = AGENT_TABLE%(agent_id)
        aType,parentId = redis.hmget(agentTable,('type','parent_id'))
        log_util.debug('agent_id[%s] aType[%s] parentId[%s]'%(agent_id,aType,parentId))
        if aType in ['2','3']:
            agentPerPriceList  =  redis.smembers(AGENT_ROOMCARD_PER_PRICE%(parentId))
        else:
            agentPerPriceList  =  redis.smembers(AGENT_ROOMCARD_PER_PRICE%(agent_id))
        log_util.debug('----------------------------------------agentPerPriceList[%s]'%(agentPerPriceList))
        agentRateList =  redis.smembers(AGENT_RATE_SET%(agent_id))
        log_util.debug('----------------------------------------agentRateList[%s]'%(agentRateList))
        for price in agentPerPriceList:
            for rate in agentRateList:
                agentRateTable = AGENT_RATE_DATE%(agent_id,rate,price,date)
                if redis.exists(agentRateTable):
                    agentRate = redis.hgetall(agentRateTable)
                    agentRate['date'] = date
                    agentRate['id'] = agent_id
                    RateReportList.append(agentRate)

    #log_util.debug('[RateReportList] agentTable[%s] RateReportList[%s]'%(agentTable,RateReportList))
    return RateReportList

def get_downline_rate2(redis,date_list,selfUid,agent_id):
    """
    获取下线抽成的列表(循环查询)
    """
    RateReportList = []

    New_agentRate = {'id': agent_id, 'number': 0.0, 'rateTotal': 0.0, 'superRateTotal': 0.0, 'meAndNextTotal': 0.0}

    agentTable = AGENT_TABLE % (agent_id)
    aType, parentId = redis.hmget(agentTable, ('type', 'parent_id'))
    log_util.debug('agent_id[%s] aType[%s] parentId[%s]' % (agent_id, aType, parentId))
    if aType in ['2', '3']:
        agentPerPriceList = redis.smembers(AGENT_ROOMCARD_PER_PRICE % (parentId))
    else:
        agentPerPriceList = redis.smembers(AGENT_ROOMCARD_PER_PRICE % (agent_id))
    log_util.debug('----------------------------------------agentPerPriceList[%s]' % (agentPerPriceList))
    agentRateList = redis.smembers(AGENT_RATE_SET % (agent_id))
    log_util.debug('----------------------------------------agentRateList[%s]' % (agentRateList))

    for price in agentPerPriceList:
        for rate in agentRateList:
            Tmp_agentRate = copy.deepcopy(New_agentRate)

            Tmp_agentRate['rate'] = rate
            Tmp_agentRate['unitPrice'] = price

            for date in date_list:
                agentRateTable = AGENT_RATE_DATE % (agent_id, rate, price, date)
                if redis.exists(agentRateTable):
                    agentRate = redis.hgetall(agentRateTable)
                    for _key in ['number','meAndNextTotal','rateTotal','superRateTotal']:
                        Tmp_agentRate[_key] += float(agentRate.get(_key,0))

            if Tmp_agentRate.get('number',0):
                if agent_id == selfUid:
                    Tmp_agentRate['superRateTotal'] = ''
                    Tmp_agentRate['rateTotal'] = ''
                    Tmp_agentRate['unitPrice'] = ''
                    Tmp_agentRate['rate'] = ''
                RateReportList.append(Tmp_agentRate)

            print 'agent_id %s Tmp_agentRate %s price %s rate %s'%(agent_id,Tmp_agentRate,price,rate)

    #log_util.debug('[RateReportList] agentTable[%s] RateReportList[%s]'%(agentTable,RateReportList))
    if RateReportList:
        print 'RateReportList',RateReportList
    return RateReportList


def get_rate_reports(redis,selfUid,startDate,endDate,agent_type):
    """
    获取抽成的列表
    """
    date_list = convert_util.to_week_list(startDate,endDate)
    if agent_type == 0:
        my_downline_agents = redis.smembers(AGENT_CHILD_TABLE%(selfUid))
    elif agent_type >0:
        my_downline_agents = getAllChildAgentId(redis,selfUid)
    else:
        my_downline_agents = []

    log_util.debug('my_downline_agents[%s]'%(my_downline_agents))
    RateReportList = []
    for date in date_list:
        downline_reports = get_downline_rate(redis,date,my_downline_agents)
        log_util.debug('[get_rate_reports] date[%s] selfId[%s] downline_reports[%s]'%(date,selfUid,downline_reports))
        if not downline_reports:
            continue
        RateReportList.extend(downline_reports)

    log_util.debug('[agentRateTable1111] selfUid[%s] RateReportList[%s]'%(selfUid,RateReportList))
    return {'date':RateReportList}

def get_rate_reports2(redis,selfUid,startDate,endDate,agent_type):
    """
    获取抽成的列表
    """
    date_list = convert_util.to_week_list(startDate,endDate)
    if agent_type == 0:
        my_downline_agents = redis.smembers(AGENT_CHILD_TABLE%(selfUid))
    elif agent_type >0:
        my_downline_agents = getAllChildAgentId(redis,selfUid)
    else:
        my_downline_agents = []
    if agent_type == 2:
        my_downline_agents.append(selfUid)
    log_util.debug('my_downline_agents[%s]'%(my_downline_agents))
    RateReportList = []

    for _agentid in my_downline_agents:
        downline_reports = get_downline_rate2(redis,date_list,selfUid,_agentid)
        log_util.debug('[get_rate_reports2] _agentid[%s] selfId[%s] date_list[%s]'%(_agentid,selfUid,date_list))
        if not downline_reports:
            continue
        RateReportList.extend(downline_reports)

    log_util.debug('[agentRateTable1111] selfUid[%s] RateReportList[%s]'%(selfUid,RateReportList))
    return {'date':RateReportList}

@admin_app.get('/statistics/rateReport')
@checkAccess
def get_rate_info(redis,session):
    """
    获取代理的利润分成报表
    """
    lang  =  getLang()
    isList = request.GET.get('list','').strip()

    startDate = request.GET.get('startDate','').strip()
    endDate = request.GET.get('endDate','').strip()
    selfUid = request.GET.get('id','').strip()
    date = request.GET.get('date','').strip()
    unitPrice = request.GET.get('unitPrice','').strip()

    log_util.debug('[try get_rate_info] selfUid[%s] date[%s]'%(selfUid,date))

    # if selfUid and date and unitPrice:
    #     reports = getNextRateReportInfo(redis,selfUid,date)
    #     return json.dumps(reports)

    if not selfUid:
        selfUid  =  session['id']

    selfAccount = session['account']
    agent_type  = convert_util.to_int(session['type'])
    agentTable = AGENT_TABLE%(selfUid)
    if isList:
        reports = get_rate_reports(redis,selfUid,startDate,endDate,agent_type)
        return json.dumps(reports)
    else:
        info = {
                    'title'         :       '[%s]销售利润报表'%(selfAccount),
                    'startDate'     :       startDate,
                    'endDate'       :       endDate,
                    'listUrl'       :       BACK_PRE+'/statistics/rateReport?list=1',
                    'STATIC_LAYUI_PATH'  :   STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH'  :   STATIC_ADMIN_PATH,
                    'aType'              :  session['type'],
        }

        return template('admin_report_rate',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/statistics/rateReport2')
@checkAccess
def get_rate_info2(redis,session):
    """
    获取代理的利润分成报表
    """
    lang  =  getLang()
    isList = request.GET.get('list','').strip()

    startDate = request.GET.get('startDate','').strip()
    endDate = request.GET.get('endDate','').strip()
    selfUid = request.GET.get('id','').strip()
    date = request.GET.get('date','').strip()
    unitPrice = request.GET.get('unitPrice','').strip()

    log_util.debug('[try get_rate_info] selfUid[%s] date[%s]'%(selfUid,date))

    # if selfUid and date and unitPrice:
    #     reports = getNextRateReportInfo(redis,selfUid,date)
    #     return json.dumps(reports)

    if not selfUid:
        selfUid  =  session['id']

    selfAccount = session['account']
    agent_type  = convert_util.to_int(session['type'])
    agentTable = AGENT_TABLE%(selfUid)
    if isList:
        reports = get_rate_reports2(redis,selfUid,startDate,endDate,agent_type)
        return json.dumps(reports)
    else:
        info = {
                    'title'         :       '[%s]销售利润报表2'%(selfAccount),
                    'startDate'     :       startDate,
                    'endDate'       :       endDate,
                    'listUrl'       :       BACK_PRE+'/statistics/rateReport2?list=1',
                    'STATIC_LAYUI_PATH'  :   STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH'  :   STATIC_ADMIN_PATH,
                    'aType'              :  session['type'],
        }

        return template('admin_report_rate2',info=info,lang=lang,RES_VERSION=RES_VERSION)

def getRegCountList(redis,startDate,endDate):
    """
    获取某个时间段注册人数列表
    params: [ startDate ] : 开始日期
            [ endDate ]   : 结束日期
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

    res = []
    res_count = 0
    now_time = datetime.now()
    while startDate <= endDate:
        if startDate > now_time:
            startDate += deltaTime
            continue
        reg_roomcard = 0
        money_count = 0
        match_enroll_num = 0
        match_enroll_fee = 0
        regInfo = {}
        dateStr = startDate.strftime('%Y-%m-%d')
        regTable = FORMAT_REG_DATE_TABLE%(dateStr)
        regSet = redis.smembers(regTable)
        regCount = redis.scard(regTable)
        if regCount:
            for account in regSet:
                memberId = redis.get(FORMAT_ACCOUNT2USER_TABLE % account)
                if memberId:
                    memberId = memberId.split(':')[-1]
                    datas = redis.lrange(PLAYER_DAY_USE_CARD % (memberId, dateStr), 0, -1)
                    day_use_card = 0
                    for data in datas:
                        typeInfo = data.split(';')
                        useCards = typeInfo[0]
                        day_use_card += int(useCards)
                    reg_roomcard += day_use_card
            orders = redis.lrange(DAY_ORDER % (dateStr), 0, -1)
            for order in orders:
                order_table = ORDER_TABLE % order
                if not redis.exists(order_table):
                    continue
                orderAccount, money, type = redis.hmget(order_table, ('account', 'money', 'type'))
                if type in 'pending' or orderAccount not in redis.smembers(regTable):
                    continue
                money_count += round(float(money) * 0.01, 2)

            queryStartDate = time.mktime(time.strptime('%s 00:00:00' % dateStr, '%Y-%m-%d %H:%M:%S'))
            queryEndDate = time.mktime(time.strptime('%s 23:59:59' % dateStr, '%Y-%m-%d %H:%M:%S'))
            # 赛事参与人数
            # queryStr = """select user_id from match_player
            # WHERE create_time >= %s and create_time <= %s GROUP BY user_id
            # """ % (queryStartDate, queryEndDate)
            queryStr = """SELECT 
            player.user_id FROM match_player AS player 
            LEFT JOIN match_record AS record ON player.match_number = record.match_number 
            WHERE record.end_time >= %s AND record.end_time <= %s
            GROUP BY player.user_id
            """ % (queryStartDate, queryEndDate)
            results = MysqlInterface.query(sql=queryStr)
            login_data = set([redis.hget(FORMAT_USER_TABLE % i, 'account') for i in results]) if results else set([])
            match_enroll_num = len(set(login_data) & regSet)

            # 赛事报名费用
            fee_enroll_ids = []
            for _account in regSet:
                userTable = redis.get(FORMAT_ACCOUNT2USER_TABLE % _account)
                regUseId = int(userTable.split(':')[-1])
                fee_enroll_ids.append(regUseId)
            fee_enroll_ids = tuple(fee_enroll_ids) if fee_enroll_ids else [0,0]
            fee_enroll_ids = fee_enroll_ids + (0,) if len(fee_enroll_ids) == 1 else fee_enroll_ids
            # queryStr = """select sum(fee) from match_player  WHERE user_id in %s and create_time >= %s and create_time <= %s""" % (fee_enroll_ids, queryStartDate, queryEndDate)
            queryStr = """SELECT 
            sum( player.fee ) 
            FROM match_player AS player LEFT JOIN match_record AS record ON player.match_number = record.match_number 
            WHERE player.user_id in %s AND record.end_time >= %s AND record.end_time <= %s
            """ % (fee_enroll_ids, queryStartDate, queryEndDate)
            fee_results = MysqlInterface.query_one(sql=queryStr)
            match_enroll_fee = float(fee_results[0]) if fee_results[0] else 0

        res_count += regCount
        regInfo['money_count'] = money_count
        regInfo['reg_date'] = dateStr
        regInfo['reg_count'] = regCount
        regInfo['reg_roomcard'] = reg_roomcard
        regInfo['match_enroll_num'] = match_enroll_num
        regInfo['match_enroll_fee'] = match_enroll_fee
        regInfo['op'] = []
        regInfo['op'].append({'url':'/admin/statistics/reg/list','method':'GET','txt':'查看详情'})
        res.append(regInfo)
        startDate += deltaTime

    if res_count:
        for info in res:
            proportion = round((float(info.get('reg_count', 0.0)) / float(res_count)) * 100, 2)
            info['reg_proportion'] = proportion
    res.reverse()
    return res

def getCardCountList(redis,agentId,startDate,endDate):
    """
        获取某个时间段注册人数列表
        params:
            [ startDate ] : 开始日期
            [ endDate ]   : 结束日期

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

    res = []

    while startDate <= endDate:
        regInfo = {}
        dateStr = startDate.strftime('%Y-%m-%d')
        if agentId == '1':
            regTable = DAY_ALL_PLAY_ROOM_CARD%(dateStr)
            regCount = redis.get(regTable)
        else:
            regCount = getAgentRoomByDay(redis,agentId,dateStr)
        if not regCount:
            regCount = 0

        regInfo['reg_date'] = dateStr
        regInfo['reg_count'] = regCount
        res.append(regInfo)

        startDate += deltaTime

    res.reverse()
    return res


@admin_app.get('/statistics/reg')
@checkAccess
def getRegStatistics(redis,session):
    lang    =  getLang()
    curTime =  datetime.now()
    isList  =  request.GET.get('list','').strip()
    startDate = request.GET.get('startDate','').strip()
    endDate   = request.GET.get('endDate','').strip()
    if isList:
        res = getRegCountList(redis,startDate,endDate)
        return json.dumps(res)
    else:
        info = {
                'title'                  :           '注册人数统计',
                'listUrl'                :           BACK_PRE+'/statistics/reg?list=1',
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
                'show_data_url'          :           BACK_PRE + '/statistics/reg/echarts',
        }

        return template('admin_statistics_reg',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/statistics/reg/echarts')
def get_show_regEcharts(redis,session):
    """
    获取注册人数图表统计
    """
    startDate = request.GET.get('startDate', '').strip()
    endData = request.GET.get('endDate', '').strip()
    get_week_date_list = get_week_date_obj(startDate, endData)
    show_obj = {
        'data':  ['每日注册人数'],
        'reg_datas' :   [],
    }
    for week_date in get_week_date_list:
        show_obj['reg_datas'].append(
            convert_util.to_int(redis.scard(FORMAT_REG_DATE_TABLE%(week_date)))
        )
    show_obj['series'] = [
        {'name':'每日注册人数','type':'line','data':show_obj['reg_datas'], 'itemStyle' : { 'normal': {'label' : {'show': 'true'}}}, 'areaStyle': {'normal': {}}},
    ]
    dataZoom_start = 7.0 / len(get_week_date_list) * 100
    return web_util.do_response(1,msg="",jumpUrl="",data={'week':get_week_date_list,'series':show_obj['series'],'legen':show_obj['data'], 'dataZoom_start': dataZoom_start})

@admin_app.get('/statistics/takeCard')
@checkAccess
def getCardStatistics(redis,session):
    lang    =  getLang()
    curTime =  datetime.now()
    isList  =  request.GET.get('list','').strip()
    startDate = request.GET.get('startDate','').strip()
    endDate   = request.GET.get('endDate','').strip()

    if isList:
        res = getCardCountList(redis,session['id'],startDate,endDate)
        return json.dumps(res)
    else:
        info = {
                'title'                  :           '日耗钻统计',
                'listUrl'                :           BACK_PRE+'/statistics/takeCard?list=1',
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
        }

        return template('admin_statistics_card',info=info,lang=lang,RES_VERSION=RES_VERSION)


def getRegListByRegDate(redis,reg_date):
    """
        获取某个时间段注册人数详情
        params:
            [ reg_date ] : 某一天

    """
    print 'reg_date',reg_date
    dateStr = reg_date
    registMemberList =  redis.smembers(FORMAT_REG_DATE_TABLE%(reg_date))
    res = []
    for member in registMemberList:
        memberInfo = {}
        account2user_table = FORMAT_ACCOUNT2USER_TABLE%(member) #从账号获得账号信息，和旧系统一样
        table = redis.get(account2user_table)
        if redis.exists(table):
            userId = table.split(':')[-1]
            nickname,reg_date,regIp,login_out_date,last_login_date,parentAg,headImgUrl= \
            redis.hmget(table,('nickname','regDate','regIp','last_logout_date','last_login_date','parentAg','headImgUrl'))
            memberInfo['nickname'] = nickname
            memberInfo['reg_date'] = reg_date
            memberInfo['regIp'] = regIp
            memberInfo['parentAg'] = regIp
            memberInfo['last_login_date'] = last_login_date if last_login_date else '-'
            memberInfo['login_out_date'] = login_out_date if login_out_date else '-'
            memberInfo['parentAg'] = parentAg if parentAg else '未加入任何公会'
            memberInfo['headImgUrl'] = headImgUrl
            memberInfo['account'] = member
            memberInfo['userId'] = userId
            datas = redis.lrange(PLAYER_DAY_USE_CARD % (userId, dateStr), 0, -1)
            day_use_card = 0
            for data in datas:
                typeInfo = data.split(';')
                useCards = typeInfo[0]
                day_use_card += int(useCards)
            memberInfo['reg_roomcard'] = day_use_card
            res.append(memberInfo)
    return res



@admin_app.get('/statistics/reg/list')
def getRegStatisticsList(redis,session):
    lang    =  getLang()
    curTime =  datetime.now()
    isList  =  request.GET.get('list','').strip()
    reg_date = request.GET.get('reg_date','').strip()

    if isList:
        res = getRegListByRegDate(redis,reg_date)
        return json.dumps(res)
    else:
        info = {
                'title'                  :           '%s 注册列表'%(reg_date),
                'listUrl'                :           BACK_PRE+'/statistics/reg/list?list=1&reg_date=%s'%(reg_date),
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
                'reg_date'               :           reg_date,
        }

        return template('admin_statistics_reg_list',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/statistics/card/list')
def getRegStatisticsList(redis,session):
    lang    =  getLang()
    curTime =  datetime.now()
    isList  =  request.GET.get('list','').strip()
    reg_date = request.GET.get('reg_date','').strip()

    if isList:
        res = getRegListByRegDate(redis,reg_date)
        return json.dumps(res)
    else:
        info = {
                'title'                  :           '%s 注册列表'%(reg_date),
                'listUrl'                :           BACK_PRE+'/statistics/reg/list?list=1&reg_date=%s'%(reg_date),
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
        }

        return template('admin_statistics_reg_list',info=info,lang=lang,RES_VERSION=RES_VERSION)


def getloginCountList(redis,agentId,agentIds,startDate,endDate):
    """
        获取某个时间段注册人数列表
        params:
            [ startDate ] : 开始日期
            [ endDate ]   : 结束日期

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

    res = []

    while startDate <= endDate:
        regInfo = {}
        dateStr = startDate.strftime('%Y-%m-%d')
        if not agentIds and int(agentId) == 1:
            regTable = FORMAT_LOGIN_DATE_TABLE%(dateStr)
            regCount = redis.scard(regTable)
        else:
            if not agentIds:
                agentIds = [agentId]
            regCount = 0
            for _agentId in agentIds:
                count = redis.get(DAY_AG_LOGIN_COUNT%(_agentId,dateStr))
                if not count:
                    count = 0
                regCount+=int(count)

        regInfo['reg_date'] = dateStr
        regInfo['reg_count'] = regCount
        regInfo['op'] = []
        regInfo['op'].append({'url':'/admin/statistics/login/list','method':'GET','txt':'查看详情'})
        res.append(regInfo)

        startDate += deltaTime

    res.reverse()
    return res

@admin_app.get('/statistics/login')
@checkAccess
def getLoginStatistics(redis,session):

    lang    =  getLang()
    curTime =  datetime.now()
    isList  =  request.GET.get('list','').strip()
    startDate = request.GET.get('startDate','').strip()
    endDate   = request.GET.get('endDate','').strip()

    selfUid  = session['id']
    if int(selfUid) == 1:
        agentIds = []
    else:
        agentIds = getAllChildAgentId(redis,selfUid)

    if isList:
        res = getloginCountList(redis,selfUid,agentIds,startDate,endDate)
        return json.dumps(res)
    else:
        info = {
                'title'                  :           '日登录人数统计',
                'listUrl'                :           BACK_PRE+'/statistics/login?list=1',
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
        }


    return template('admin_statistics_login',info=info,lang=lang,RES_VERSION=RES_VERSION)


@admin_app.get('/statistics/login/list')
def getRegStatisticsList(redis,session):
    lang    =  getLang()
    curTime =  datetime.now()
    isList  =  request.GET.get('list','').strip()
    reg_date = request.GET.get('reg_date','').strip()
    selfUid  = session['id']

    if isList:
        res = getLoginListByRegDate(redis,session['id'],reg_date)
        return json.dumps(res)
    else:
        info = {
                'title'                  :           '%s 登录列表'%(reg_date),
                'listUrl'                :           BACK_PRE+'/statistics/login/list?list=1&reg_date=%s'%(reg_date),
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
        }

        return template('admin_statistics_login_list',reg_date=reg_date,info=info,lang=lang,RES_VERSION=RES_VERSION)

# @admin_app.get('/statistics/count')
# def getCountStatics(redis,session):
#     """
#     获取每日的局数统计
#     """
#     lang = getLang()
#     curTime = datetime.now()
#     isList = request.GET.get('list','').strip()
#     startDate = request.GET.get('startDate','').strip()
#     endDate = request.GET.get('endDate','').strip()
#     selfUid = request.GET.get('id','').strip()
#     date    = request.GET.get('date','').strip()

#     if date:
#         endDate = date

#     log_debug('[count] startDate[%s] endDate[%s]'%(startDate,endDate))

#     if not selfUid:
#         selfUid = session['id']

#     agentType = session['type']
#     openList = 'true'
#     if int(agentType) == 2:
#         openList = 'false'
#     if isList:
#         res = getCountTotal(redis,selfUid,startDate,endDate)
#         return json.dumps(res)
#     else:
#         info = {
#                 'title'         :       '局数统计',
#                 'listUrl'                :           BACK_PRE+'/statistics/count?list=1',
#                 'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
#                 'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
#         }

#     return template('admin_statistics_count',openList=openList,info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/statistics/active')
def get_active_page(redis,session):
    """
    活跃人数统计
    """
    curTime = datetime.now()
    lang = getLang()

    isList = request.GET.get('list','').strip()
    start_date = request.GET.get('startDate','').strip()
    end_date = request.GET.get('endDate','').strip()
    selfUid = session['id']
    if isList:
        active_reports = get_active_reports(redis,start_date,end_date,selfUid)
        return json.dumps(active_reports)
    else:
        info = {
                'title'         :       '活跃人数统计',
                'listUrl'                :           BACK_PRE+'/statistics/active?list=1',
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
                'selfUid'                :           selfUid,
                'show_data_url'          :           BACK_PRE + '/statistics/active/echarts'
        }

        return template('admin_statistics_active',PAGE_LIST=PAGE_LIST,info=info,RES_VERSION=RES_VERSION,lang=lang)

@admin_app.get('/statistics/active/echarts')
def get_show_avtiveEcharts(redis,session):
    """
    获取活跃人数图表统计
    """
    startDate = request.GET.get('startDate', '').strip()
    endData = request.GET.get('endDate', '').strip()
    selfUid = session.get('id')
    get_week_date_list = get_week_date_obj(startDate, endData)
    show_obj = {
        'data':  ['钻石活跃人数', '钻石钻石消耗', '钻石局数统计', '比赛场活跃人数', '比赛场报名费用', '钻石赛奖励', '积分赛奖励'],
        'active_datas' : [],
        'card_datas': [],
        'task_count': [],
        'match_active_datas': [],
        'match_fee_datas': [],
        'match_roomcard_datas': [],
        'match_gamepoint_datas': [],
    }
    if int(selfUid) == 1:
        agentIds = []
    else:
        agentIds = getAllChildAgentId(redis,selfUid)

    for week_date in get_week_date_list:
        show_obj['active_datas'].append(get_login_count(redis, selfUid, week_date, agentIds))
        show_obj['card_datas'].append(get_take_count(redis, selfUid, week_date))
        show_obj['task_count'].append(getCountTotal(redis, selfUid, week_date))
        queryStartDate = time.mktime(time.strptime('%s 00:00:00' % week_date, '%Y-%m-%d %H:%M:%S'))
        queryEndDate = time.mktime(time.strptime('%s 23:59:59' % week_date, '%Y-%m-%d %H:%M:%S'))
        results = get_match_record(redis, queryStartDate, queryEndDate)
        match_fee_count = convert_util.to_float(results[1])
        match_roomcard_count = convert_util.to_float(results[9])
        match_gamepoint_count = convert_util.to_float(results[10])
        show_obj['match_active_datas'].append(get_match_player_count(redis, queryStartDate, queryEndDate))
        show_obj['match_fee_datas'].append(match_fee_count)
        show_obj['match_roomcard_datas'].append(match_roomcard_count)
        show_obj['match_gamepoint_datas'].append(match_gamepoint_count)
    show_obj['series'] = [
        {'name': '钻石活跃人数', 'type': 'line', 'data': show_obj['active_datas'],
         'itemStyle': {'normal': {'label': {'show': 'true'}}}, 'areaStyle': {'normal': {}}},
        {'name': '钻石钻石消耗', 'type': 'line', 'data': show_obj['card_datas'],
         'itemStyle': {'normal': {'label': {'show': 'true'}}}, 'areaStyle': {'normal': {}}},
        {'name': '钻石局数统计', 'type': 'line', 'data': show_obj['task_count'],
         'itemStyle': {'normal': {'label': {'show': 'true'}}}, 'areaStyle': {'normal': {}}},
        {'name': '比赛场活跃人数', 'type': 'line', 'data': show_obj['match_active_datas'],
         'itemStyle': {'normal': {'label': {'show': 'true'}}}, 'areaStyle': {'normal': {}}},
        {'name': '比赛场报名费用', 'type': 'line', 'data': show_obj['match_fee_datas'],
         'itemStyle': {'normal': {'label': {'show': 'true'}}}, 'areaStyle': {'normal': {}}},
        {'name': '钻石赛奖励', 'type': 'line', 'data': show_obj['match_roomcard_datas'],
         'itemStyle': {'normal': {'label': {'show': 'true'}}}, 'areaStyle': {'normal': {}}},
        {'name': '积分赛奖励', 'type': 'line', 'data': show_obj['match_gamepoint_datas'],
         'itemStyle': {'normal': {'label': {'show': 'true'}}}, 'areaStyle': {'normal': {}}},
    ]

    dataZoom_start = 7.0 / len(get_week_date_list) * 100
    return web_util.do_response(1,msg="",jumpUrl="",data={
        'week':get_week_date_list,'series':show_obj['series'],
        'legen':show_obj['data'], 'dataZoom_start': dataZoom_start,
    })


@admin_app.get('/statistics/active/showDay')
def get_active_day(redis,session):
    """
    活跃人数统计
    """
    curTime = datetime.now()
    lang = getLang()

    isList = request.GET.get('list','').strip()
    date = request.GET.get('day','').strip()
    selfUid = session['id']
    if isList:
        active_reports = get_login_list(redis,session['id'],date)
        return json.dumps(active_reports)
    else:
        info = {
                'title'                  :          '[%s] 统计列表'%(date),
                'listUrl'                :           BACK_PRE+'/statistics/active/showDay?list=1&day=%s'%(date),
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
                'active_date'            :           date,
        }

        return template('admin_statistics_login_list',PAGE_LIST=PAGE_LIST,date=date,info=info,RES_VERSION=RES_VERSION,lang=lang)


@admin_app.get('/statistics/daily')
def get_active_daily(redis,session):
    """
    每日数据统计
    """
    curTime = datetime.now()
    lang = getLang()

    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    isList = request.GET.get('list','').strip()

    if isList:

        daily_reports = get_daily_list(redis, session, startDate, endDate)
        return json.dumps(daily_reports)
    else:
        info = {
                'title'                  :           lang.MENU_STATISTICS_DAILY_TXT,
                'listUrl'                :           BACK_PRE + '/statistics/daily?list=1',
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
        }

        return template('admin_statistics_daily_list', info=info,RES_VERSION=RES_VERSION,lang=lang)

@admin_app.get('/statistics/user/save')
def get_active_user_save(redis,session):
    """
    用户留存率
    """
    curTime = datetime.now()
    lang = getLang()

    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    isList = request.GET.get('list','').strip()
    model = request.GET.get('model', '').strip()
    selfAccount, selfUid, selfType = session['account'], session['id'], session['type']
    if isList:
        usersave_reports = get_usersave_list(redis, session, startDate, endDate, model=model)
        return json.dumps(usersave_reports)
    else:
        info = {
                'title'                  :           lang.MENU_STATISTICS_USER_SAVE_TXT,
                'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
                'selfType': selfType,
                'listUrl'                :           BACK_PRE + '/statistics/user/save?list=1&model=reg',
                'login_listUrl'          :           BACK_PRE + '/statistics/user/save?list=1&model=login',
                'match_listUrl'          :           BACK_PRE + '/statistics/user/save?list=1&model=matchReg',
                'match_login_listUrl'    :           BACK_PRE + '/statistics/user/save?list=1&model=matchLogin',
                'regEchartUrl'           :           BACK_PRE + '/statistics/user/save/regEchart',
        }

        return template('admin_statistics_user_save_list', info=info,RES_VERSION=RES_VERSION,lang=lang)

@admin_app.get('/statistics/user/save/regEchart')
def get_All_useSaveregEchart(redis,session):
    """
    获取游戏注册统计图表统计
    """
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    type = request.GET.get('type', '').strip()
    title_lists = get_week_date_obj(startDate, endDate)
    x_date_lists = ['1 日后', '2 日后', '3 日后', '4 日后', '5 日后', '6 日后', '7 日后', '15 日后', '30 日后'] # 横坐数据
    # 获取生成对象类型
    show_obj = {
        'data': title_lists
    }
    for _title in title_lists:
        show_obj[_title] = []

    for week in x_date_lists:
        for _title in title_lists:
            if type == '0':
                reg_data = redis.smembers(FORMAT_REG_DATE_TABLE % (_title))
            else:
                reg_data = redis.smembers(FORMAT_LOGIN_DATE_TABLE % (_title))
            day = week.split(' ')[0]
            save_data = saveDate(redis, session, 'reg', reg_data, _title, int(day))
            show_obj[_title].append(convert_util.to_int(save_data.split(' ')[0] if save_data else 0))

    show_obj['series'] = [ {'name': _title, 'type': 'line', 'data': show_obj[_title], 'itemStyle' : { 'normal': {'label' : {'show': 'true'}}}, 'areaStyle': {'normal': {}}} for _title in title_lists ]

    dataZoom_start = 7.0 / len(x_date_lists) * 100
    return web_util.do_response(1,msg="",jumpUrl="",data={
        'week':x_date_lists,'series':show_obj['series'],
        'legen':show_obj['data'], 'dataZoom_start': dataZoom_start,
    })

@admin_app.get('/statistics/game/play')
@checkAccess
def get_active_game_play(redis, session):
    """
    游戏耗钻数统计
    """
    curTime = datetime.now()
    lang = getLang()

    isList = request.GET.get('list', '').strip()
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()

    if isList:
        get_week_date_list = get_week_date_obj(startDate, endDate)[::-1]
        res = []
        for gameId in redis.lrange(GAME_LIST, 0, -1):
            if int(gameId)  in MatchGameIds:
                continue
            info = {'gameName': redis.hget(GAME_TABLE % gameId, 'name'), 'gameId': gameId}
            for week in get_week_date_list:
                roomcard = redis.get('game:roomCards:%s:%s:total' % (gameId, week))
                info[week] = roomcard if roomcard else 0
            res.append(info)
        data ={'data': res, 'count': len(res)}
        return json.dumps(data)
    else:
        info = {
            'title': '[房间模式] %s' % lang.MENU_STATISTICS_GAME_PLAY_TXT,
            'listUrl': BACK_PRE + '/statistics/game/play?list=1',
            'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
            'AllPlayGameurl': BACK_PRE + '/statistics/all/game/echarts',
            'EveryPlayGameurl': BACK_PRE + '/statistics/every/game/echarts',
            'columnsArrayUrl': BACK_PRE + '/statistics/columnsArrayUrl'
        }
    return template('admin_statistics_game_play_list', info=info, RES_VERSION=RES_VERSION, lang=lang)

@admin_app.get('/statistics/all/game/echarts')
def get_All_gameplayEcharts(redis,session):
    """
    获取游戏统计图表统计
    """
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    selfUid = session.get('id')
    week_date_lists = get_week_date_obj(startDate, endDate)
    week_date_lists = sorted(week_date_lists, reverse=True)
    # 获取生成对象类型
    show_obj = {
        'data': [u'当日游戏耗钻总数'],
        'roomcards_day': [],
        'roomcards_all': [],
    }

    game_ids = redis.lrange(GAME_LIST, 0, -1)
    allGame_total = 0
    for date in week_date_lists:
        roomcards_day = 0
        for each in game_ids:
            roomcard_day = redis.get('game:roomCards:%s:%s:total' % (each, date))
            if roomcard_day:
                roomcards_day += int(roomcard_day)
        allGame_total += roomcards_day
        show_obj['roomcards_day'].append(convert_util.to_int(roomcards_day))

    show_obj['series'] = [
        {'name': u'当日游戏耗钻总数', 'type': 'line', 'itemStyle' : { 'normal': {'label' : {'show': 'true'}}}, 'data': show_obj['roomcards_day'],'areaStyle': {'normal': {}}},
    ]

    dataZoom_start = 7.0 / len(week_date_lists) * 100
    return web_util.do_response(1,msg="",jumpUrl="",data={
        'week':week_date_lists,'series':show_obj['series'],
        'legen':show_obj['data'], 'dataZoom_start': dataZoom_start,
    })

@admin_app.get('/statistics/every/game/echarts')
def get_Every_gameplayEcharts(redis,session):
    """
    获取游戏统计图表统计
    """
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    selfUid = session.get('id')
    week_date_lists = get_week_date_obj(startDate, endDate)
    week_date_lists = sorted(week_date_lists, reverse=True)
    # 获取生成对象类型
    game_ids = []
    for gameid in redis.lrange(GAME_LIST, 0, -1):
        if int(gameid) not in MatchGameIds:
            game_ids.append(gameid)
    game_set = ['%s(%s)' % (each, redis.hget(GAME_TABLE % (each), 'name')) for each in game_ids]

    show_obj = {
        'data': game_set,
    }

    for date in week_date_lists:
        for each in game_ids:
            roomcard_day = redis.get('game:roomCards:%s:%s:total' % (each, date))
            if not roomcard_day:
                roomcard_day = 0

            show_obj.setdefault(each, []).append(convert_util.to_int(roomcard_day))

    for item in game_set:
        show_obj.setdefault('series', []).append(
            {'name': item, 'type': 'line', 'data': show_obj[item.split('(')[0]], 'itemStyle' : { 'normal': {'label' : {'show': 'true'}}},'areaStyle': {'normal': {}}}
        )

    dataZoom_start = 7.0 / len(week_date_lists) * 100
    return web_util.do_response(1,msg="",jumpUrl="",data={
        'week':week_date_lists,'series':show_obj['series'],
        'legen':show_obj['data'], 'dataZoom_start': dataZoom_start,
    })

@admin_app.get('/statistics/columnsArrayUrl')
def get_active_columnsArrayUrl(redis, session):
    """
    游戏耗钻数统计日期
    """
    curTime = datetime.now()
    lang = getLang()
    startDate = request.GET.get("startDate", "").strip()
    endDate = request.GET.get("endDate", "").strip()

    get_week_date_list = get_week_date_obj(startDate, endDate)
    get_week_date_list = sorted(get_week_date_list, reverse=True)
    res = []
    for week in get_week_date_list:
        res.append({week: 0})
    data = {'data': res, 'count': len(res)}
    return json.dumps(data)

@admin_app.get('/statistics/game/play/match')
def get_active_game_play_match(redis, session):
    """
    游戏耗钻数统计
    """
    curTime = datetime.now()
    lang = getLang()

    isList = request.GET.get('list', '').strip()
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()

    if isList:
        res = []
        queryStartDate = time.mktime(time.strptime('%s 00:00:00' % startDate, '%Y-%m-%d %H:%M:%S'))
        queryEndDate = time.mktime(time.strptime('%s 23:59:59' % endDate, '%Y-%m-%d %H:%M:%S'))
        results = get_match_record_game(redis, queryStartDate, queryEndDate)
        if results:
            num_id = 0
            for _result in results:
                info = {}
                info['game_id'] = convert_util.to_int(_result[0])
                info['total_fee'] = convert_util.to_float(_result[1])
                info['total_num'] = convert_util.to_float(_result[2])
                info['roomcard_game_count'] = convert_util.to_float(_result[3])
                info['point_game_count'] = convert_util.to_float(_result[4])
                info['total_enroll_num'] = convert_util.to_float(_result[5])
                info['total_roomcard_num'] = convert_util.to_float(_result[6])
                info['total_point_num'] = convert_util.to_float(_result[7])
                info['total_roomcard_fee'] = convert_util.to_float(_result[8])
                info['total_point_fee'] = convert_util.to_float(_result[9])
                info['total_roomcard_award'] = convert_util.to_float(_result[10])
                info['total_point_award'] = convert_util.to_float(_result[11])
                gameTable = GAME_TABLE % (info['game_id'])
                info['game_name'] = redis.hget(gameTable, 'name')
                num_id += 1
                info['num_id'] = num_id
                res.append(info)
        data ={'data': res, 'count': len(res)}
        return json.dumps(data)
    else:
        info = {
            'title': '[比赛场模式] %s' % lang.MENU_STATISTICS_GAME_PLAY_TXT,
            'listUrl': BACK_PRE + '/statistics/game/play/match?list=1',
            'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        }
    return template('admin_statistics_game_play_match_list', info=info, RES_VERSION=RES_VERSION, lang=lang)

@admin_app.get('/statistics/overall/data')
@checkAccess
def get_active_overall_data(redis, session):
    """
    游戏耗钻数统计
    """
    curTime = datetime.now()
    lang = getLang()

    # 当日数据
    today = curTime.strftime('%Y-%m-%d')
    month = curTime.strftime('%Y-%m')
    uid = session.get('id')

    dayData = today_count(redis, session, uid, today)
    monthData = tomonth_count(redis, session, uid, month)
    totalData= tototal_count(redis, session, uid)
    phone_proportion = phone_Proportion(redis, session, uid, today)
    info = {
        'title': lang.MENU_STATISTICS_OVERALL_DATA_TXT,
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'today': today,
        'month': month,
    }
    return template('admin_statistics_overall_data_list', phone_proportion=phone_proportion,dayData=dayData, monthData=monthData, totalData=totalData, info=info, RES_VERSION=RES_VERSION, lang=lang)

@admin_app.get('/statistics/temp')
def get_temp(redis, session):
    """获取总体数据饼形图"""
    curTime = datetime.now()
    date = curTime.strftime("%Y-%m-%d")

    # 当前终端系统占比
    login_data = FORMAT_LOGIN_DATE_TABLE % date
    clientKind_info = {'0': 'Web_Browser', '1': 'Android', '2': 'IOS', '3': 'Unknown'}
    phone_info = {'Web_Browser': 0, 'Android': 0, 'IOS': 0, 'Unknown': 0}
    for account in redis.smembers(login_data):
        user_table = redis.get(FORMAT_ACCOUNT2USER_TABLE % account)
        if redis.exists(user_table):
            clientKind = redis.hget(user_table, 'lastLoginClientType')
            if clientKind:
                clientKind_type = clientKind_info.get(clientKind, '3')
                phone_info[clientKind_type] += 1
            else:
                phone_info['Unknown'] += 1
    phone_series = [{'value': '%s' % _value , 'name': '%s' % _key } for _key, _value in phone_info.items()]

    # 当前游戏占比
    game_series = []
    game_legend = []
    for gameId in redis.lrange(GAME_LIST, 0, -1):
        if int(gameId) in MatchGameIds:
            continue
        game_table = GAME_TABLE % gameId
        if redis.exists(game_table):
            name = redis.hget(GAME_TABLE % gameId, 'name')
            value = redis.get('game:roomCards:%s:%s:total' % (gameId, date))
            game_legend.append(name)
            game_series.append({'value': value if value else 0, 'name': name})

    # 当前登录人数占比
    user_weixin_set = redis.scard(ACCOUNT4WEIXIN_SET)
    user_login_set = redis.scard(FORMAT_LOGIN_DATE_TABLE % date)
    user_login_legend = ['当天登录数', '当天非登录数']
    user_login_series = [{'value': user_login_set, 'name': '当天登录数'}, {'value': user_weixin_set - user_login_set, 'name': '当天非登录数'}]
    return {
        'phone_info': {
            'legend': phone_info.keys(),
            'series': phone_series
        },
        'game_info': {
            'legend': game_legend,
            'series': game_series
        },
        'user_login_info': {
            'legend': user_login_legend,
            'series': user_login_series
        }
    }

@admin_app.get('/statistics/match')
@checkAccess
def get_tatistics_match_data(redis, session):
    """
    赛事数据统计
    """
    curTime = datetime.now()
    lang = getLang()

    isList = request.GET.get('list', '').strip()
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    gameId = request.GET.get('gameId', '').strip()
    playId = request.GET.get('playId', '').strip()
    matchId = request.GET.get('matchId', '').strip()
    matchType = request.GET.get('matchType', '').strip()
    matchState = request.GET.get('matchState', '').strip()
    pageSize = request.GET.get('pageSize', '').strip()
    pageNumber = request.GET.get('pageNumber', '').strip()
    sortName = request.GET.get('sortName', '').strip()
    sortOrder = request.GET.get('sortOrder', '').strip()
    if isList:
        startDate = time.mktime(time.strptime('%s 00:00:00' % startDate, '%Y-%m-%d %H:%M:%S'))
        endDate = time.mktime(time.strptime('%s 23:59:59' % endDate, '%Y-%m-%d %H:%M:%S'))
        if not pageNumber:
            pageNumber = 0
        else:
            pageNumber = convert_util.to_int(pageNumber)
            pageNumber = (pageNumber - 1) * int(pageSize)
        condition = {
            'start_time': startDate,
            'end_time': endDate,
            'game_id': gameId,
            'match_id': playId,
            'match_number': matchId,
            'total_award_type': matchType,
            'pageNumber': pageNumber,
            'pageSize': pageSize,
            'matchState': matchState,
            'sortName': sortName if sortName else 'end_time',
            'sortOrder': sortOrder if sortOrder else 'desc',
        }
        match_reports = get_match_reports(redis, condition)
        return json.dumps(match_reports)
    else:
        info = {
            'title': lang.MENU_STATISTICS_MATCH_TXT,
            'listUrl': BACK_PRE + '/statistics/match?list=1',
            'player_listUrl': BACK_PRE + '/statistics/matchPlayer?list=1',
            'total_listUrl': BACK_PRE + '/statistics/match/total?list=1',
            'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
            'show_data_url': BACK_PRE + '/statistics/match/echarts',
        }

        return template('admin_statistics_match', PAGE_LIST=PAGE_LIST, info=info, RES_VERSION=RES_VERSION, lang=lang)

@admin_app.get('/statistics/matchPlayer')
def get_tatistics_matchPlayer(redis, session):
    """
    赛事玩家数据统计
    """
    curTime = datetime.now()
    lang = getLang()

    isList = request.GET.get('list', '').strip()
    match_number = request.GET.get('match_number', '').strip()
    res = []
    if isList:
        queryStr = """
        SELECT user_id, game_id, match_id, fee_type, fee, score, `rank`, reward_type, reward_fee FROM match_player WHERE match_number='%s'""" % (match_number)
        results = MysqlInterface.query(sql=queryStr)
        if results:
            for result in results:
                info = {}
                info['user_id'] = result[0]
                userTable = FORMAT_USER_TABLE % result[0]
                nickname, account = redis.hmget(userTable, ('nickname', 'account'))
                info['user_nickanme'] = nickname
                info['user_account'] = account
                info['fee'] = result[4]
                info['score'] = result[5]
                info['rank'] = result[6]
                info['reward_type'] = result[7]
                info['reward_fee'] = result[8]
                res.append(info)
        data =  {"count": res, "data": res}
        return json.dumps(data)
    else:
        return json.dumps({})

@admin_app.get('/statistics/match/total')
def get_tatistics_match_total(redis, session):
    """
    赛事数据统计
    """
    curTime = datetime.now()
    lang = getLang()

    isList = request.GET.get('list', '').strip()
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    gameId = request.GET.get('gameId', '').strip()
    playId = request.GET.get('playId', '').strip()
    matchId = request.GET.get('matchId', '').strip()
    matchType = request.GET.get('matchType', '').strip()
    matchState = request.GET.get('matchState', '').strip()
    pageSize = request.GET.get('pageSize', '').strip()
    pageNumber = request.GET.get('pageNumber', '').strip()
    if isList:
        startDate = time.mktime(time.strptime('%s 00:00:00' % startDate, '%Y-%m-%d %H:%M:%S'))
        endDate = time.mktime(time.strptime('%s 23:59:59' % endDate, '%Y-%m-%d %H:%M:%S'))
        condition = {
            'start_time': startDate,
            'end_time': endDate,
            'game_id': gameId,
            'match_id': playId,
            'match_number': matchId,
            'total_award_type': matchType,
            'matchState': matchState,
        }
        info = {}
        conditionStr = "game_id={game_id} and match_id={match_id} and match_number='{match_number}' and total_award_type={total_award_type} and matchState={matchState}  order by start_time desc".format(
            **condition)
        whereStr = 'and'.join([i for i in conditionStr.split('and') if ('= ') not in i and "=''" not in i])
        # queryStr = """select count(1) as '总条数', sum(total_fee) as '总报名费用', sum(total_num) as '总报名人数', count( IF (total_award_type = 1 ,1, null)) '钻石场总数',count( IF (total_award_type = 3 ,1, null)) '积分场总数', sum( IF (( total_award_type = 1 ), total_num, 0 ) ) as '钻石场报名人数', sum( IF (( total_award_type = 3 ), total_num, 0 ) ) as  '积分场报名人数', sum( IF (( total_award_type = 1), total_award_num, 0 ) ) as '钻石奖励总数', sum( IF (( total_award_type = 3), total_award_num, 0 ) ) as '积分奖励总数' from match_record  where %s""" % (whereStr)
        results = get_match_record(redis, condition['start_time'], condition['end_time'], condition=whereStr)
        active_resultes = get_match_active_data(redis, condition['start_time'], condition['end_time'], whereStr)
        # results = MysqlInterface.query_one(queryStr)
        info['game_count'] = convert_util.to_float(results[0])
        info['total_fee'] = convert_util.to_float(results[1])
        info['total_num'] = convert_util.to_float(results[2])
        info['total_roomcard'] = convert_util.to_float(results[3])
        info['total_gamepoint'] = convert_util.to_float(results[4])
        info['total_roomcard_fee'] = convert_util.to_float(results[5])
        info['total_gamepoint_fee'] = convert_util.to_float(results[6])
        info['total_roomcard_player'] = convert_util.to_float(results[7])
        info['total_gamepoint_player'] = convert_util.to_float(results[8])
        info['total_roomcard_reward'] = convert_util.to_float(results[9])
        info['total_gamepoint_reward'] = convert_util.to_float(results[10])
        info['total_active'] = convert_util.to_float(active_resultes[0])
        info['total_active_roomcard'] = convert_util.to_float(active_resultes[1])
        info['total_active_gamepoint'] = convert_util.to_float(active_resultes[2])
        data =  {"count": 1, "data": [info]}
        return json.dumps(data)
    else:
        return json.dumps({})

@admin_app.get('/statistics/match/echarts')
def get_show_matchEcharts(redis,session):
    """
    获取活跃人数图表统计
    """
    startDate = request.GET.get('startDate', '').strip()
    endData = request.GET.get('endDate', '').strip()
    get_week_date_list = get_week_date_obj(startDate, endData)
    show_obj = {
        'data':  ['赛事总数', '赛事报名数', '赛事报名费用', '钻石赛奖励', '积分赛奖励'],
        'matchCount_datas': [],
        'matchNum_datas' :   [],
        'matchFee_datas': [],
        'matchRoomCard_datas': [],
        'matchGamePoint_datas': [],
    }

    for week_date in get_week_date_list:
        queryStartDate = time.mktime(time.strptime('%s 00:00:00' % week_date, '%Y-%m-%d %H:%M:%S'))
        queryEndDate = time.mktime(time.strptime('%s 23:59:59' % week_date, '%Y-%m-%d %H:%M:%S'))
        results = get_match_record(redis, queryStartDate, queryEndDate)
        show_obj['matchCount_datas'].append(convert_util.to_float(results[0]))
        show_obj['matchFee_datas'].append(convert_util.to_float(results[1]))
        show_obj['matchNum_datas'].append(convert_util.to_float(results[2]))
        show_obj['matchRoomCard_datas'].append(convert_util.to_float(results[9]))
        show_obj['matchGamePoint_datas'].append(convert_util.to_float(results[10]))

    show_obj['series'] = [
        {'name': '赛事总数', 'type': 'line', 'data': show_obj['matchCount_datas'],
         'itemStyle': {'normal': {'label': {'show': 'true'}}}, 'areaStyle': {'normal': {}}},
        {'name':'赛事报名数','type':'line','data':show_obj['matchNum_datas'], 'itemStyle' : { 'normal': {'label' : {'show': 'true'}}}, 'areaStyle': {'normal': {}}},
        {'name': '赛事报名费用', 'type': 'line', 'data': show_obj['matchFee_datas'],'itemStyle': {'normal': {'label': {'show': 'true'}}}, 'areaStyle': {'normal': {}}},
        {'name': '钻石赛奖励', 'type': 'line', 'data': show_obj['matchRoomCard_datas'],'itemStyle': {'normal': {'label': {'show': 'true'}}}, 'areaStyle': {'normal': {}}},
        {'name': '积分赛奖励', 'type': 'line', 'data': show_obj['matchGamePoint_datas'],
         'itemStyle': {'normal': {'label': {'show': 'true'}}}, 'areaStyle': {'normal': {}}},
    ]

    dataZoom_start = 7.0 / len(get_week_date_list) * 100
    return web_util.do_response(1,msg="",jumpUrl="",data={
        'week':get_week_date_list,'series':show_obj['series'],
        'legen':show_obj['data'], 'dataZoom_start': dataZoom_start,
    })


@admin_app.get('/statistics/match/player')
@checkAccess
def get_statistics_player_data(redis, session):
    """
    赛事数据统计
    """
    curTime = datetime.now()
    lang = getLang()

    isList = request.GET.get('list', '').strip()
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    userId = request.GET.get('userId', '').strip()
    gameId = request.GET.get('gameId', '').strip()
    playId = request.GET.get('playId', '').strip()
    matchId = request.GET.get('matchId', '').strip()
    matchType = request.GET.get('matchType', '').strip()
    matchRank = request.GET.get('matchRank', '').strip()
    pageSize = request.GET.get('pageSize', '').strip()
    pageNumber = request.GET.get('pageNumber', '').strip()
    sortName = request.GET.get('sortName', '').strip()
    sortOrder = request.GET.get('sortOrder', '').strip()
    if isList:
        startDate = time.mktime(time.strptime('%s 00:00:00' % startDate, '%Y-%m-%d %H:%M:%S'))
        endDate = time.mktime(time.strptime('%s 23:59:59' % endDate, '%Y-%m-%d %H:%M:%S'))
        if not pageNumber:
            pageNumber = 0
        else:
            pageNumber = convert_util.to_int(pageNumber)
            pageNumber = (pageNumber - 1) * int(pageSize)
        if sortName in ['total_award_type', 'game_id', 'match_id', 'match_number', 'end_time']:
            sortName = 'record.%s' % sortName
        if sortName in ['fee', 'rank', 'score', 'reward_fee']:
            sortName = 'player.%s' % sortName
        condition = {
            'start_time': startDate,
            'end_time': endDate,
            'user_id': userId,
            'game_id': gameId,
            'match_id': playId,
            'match_number': matchId,
            'reward_type': matchType,
            'rank': matchRank,
            'pageNumber': pageNumber,
            'pageSize': pageSize,
            'sortName': sortName if sortName  else 'end_time',
            'sortOrder': sortOrder if sortOrder else 'desc',
        }
        match_reports = get_match_player_reports(redis, condition)
        return json.dumps(match_reports)
    else:
        info = {
            'title': lang.MENU_STATISTICS_MATCH_PLAYER_TXT,
            'listUrl': BACK_PRE + '/statistics/match/player?list=1',
            'record_listUrl': BACK_PRE + '/statistics/matchRecord?list=1',
            'total_listUrl': BACK_PRE + '/statistics/match/player/total?list=1',
            'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        }

        return template('admin_statistics_match_player', PAGE_LIST=PAGE_LIST, info=info, RES_VERSION=RES_VERSION, lang=lang)

@admin_app.get('/statistics/matchRecord')
def get_statistics_matchRecord(redis, session):
    """
        玩家赛事数据统计
    """
    curTime = datetime.now()
    lang = getLang()
    isList = request.GET.get('list', '').strip()
    match_number = request.GET.get('match_number', '').strip()
    res = []
    if isList:
        queryStr = """
            SELECT total_num, user_ids, total_fee, total_award_type, total_award_num FROM match_record
            WHERE match_number='%s'""" % (match_number)
        results = MysqlInterface.query(sql=queryStr)
        if results:
            for result in results:
                info = {}
                info['total_num'] = result[0]
                info['user_ids'] = result[1]
                info['total_fee'] = result[2]
                info['total_award_type'] = result[3]
                info['total_award_num'] = result[4]
                res.append(info)
        data = {"count": res, "data": res}
        return json.dumps(data)
    else:
        return json.dumps({})

@admin_app.get('/statistics/match/player/total')
def get_statistics_player_total(redis, session):
    """
        赛事数据统计
        """
    curTime = datetime.now()
    lang = getLang()
    isList = request.GET.get('list', '').strip()
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    userId = request.GET.get('userId', '').strip()
    gameId = request.GET.get('gameId', '').strip()
    playId = request.GET.get('playId', '').strip()
    matchId = request.GET.get('matchId', '').strip()
    matchType = request.GET.get('matchType', '').strip()
    matchRank = request.GET.get('matchRank', '').strip()
    pageSize = request.GET.get('pageSize', '').strip()
    pageNumber = request.GET.get('pageNumber', '').strip()
    if isList:
        startDate = time.mktime(time.strptime('%s 00:00:00' % startDate, '%Y-%m-%d %H:%M:%S'))
        endDate = time.mktime(time.strptime('%s 23:59:59' % endDate, '%Y-%m-%d %H:%M:%S'))
        if not pageNumber:
            pageNumber = 0
        else:
            pageNumber = convert_util.to_int(pageNumber)
            pageNumber = (pageNumber - 1) * int(pageSize)
        condition = {
            'start_time': startDate,
            'end_time': endDate,
            'user_id': userId,
            'game_id': gameId,
            'match_id': playId,
            'match_number': matchId,
            'reward_type': matchType,
            'rank': matchRank,
            'pageNumber': pageNumber,
            'pageSize': pageSize,
        }
        info = {}
        # conditionStr = "user_id={user_id} and game_id={game_id} and match_id={match_id} and match_number='{match_number}' and reward_type={reward_type} and rank={rank} and create_time>={start_time} and create_time<={end_time}".format(**condition)
        conditionStr = "player.user_id={user_id} and player.game_id={game_id} and player.match_id={match_id} and player.match_number='{match_number}' and record.total_award_type={reward_type} and player.rank={rank} and record.end_time>={start_time} and record.end_time<={end_time}".format(**condition)

        whereStr = 'and'.join([i for i in conditionStr.split('and') if ('= ') not in i and "=''" not in i])
        queryStr = """SELECT sum( player.fee ) AS '总报名费用',
        count(distinct record.match_number) AS '总场数',
        sum( IF (( record.total_award_type = 1 ), player.fee, 0 )) '钻石场报名费用',
        sum( IF (( record.total_award_type = 3 ), player.fee, 0 )) '积分场报名总费用',
        count( IF ( record.total_award_type = 1, 1, NULL )) '钻石场报名总数',
        count( IF ( record.total_award_type = 3, 1, NULL )) '积分场报名总数', 
        sum( IF (( record.total_award_type = 1 ), player.reward_fee, 0 )) '钻石奖励总数',
        sum( IF (( record.total_award_type = 3 ), player.reward_fee, 0 )) '积分奖励总数' 
        FROM match_player as player LEFT JOIN match_record AS record ON player.match_number = record.match_number 
        WHERE %s
        """ % (whereStr)
        results = MysqlInterface.query_one(queryStr)
        active_resultes = get_match_active_data(redis, startDate, endDate, whereStr)
        info['fee'] = convert_util.to_float(results[0])
        info['match_num'] = convert_util.to_float(results[1])
        info['roomcard_fee'] = convert_util.to_float(results[2])
        info['gamePoint_fee'] = convert_util.to_float(results[3])
        info['roomcard_num'] = convert_util.to_float(results[4])
        info['gamePoint_num'] = convert_util.to_float(results[5])
        info['reward_roomcard_fee'] = convert_util.to_float(results[6])
        info['gamePoint_roomcard_fee'] = convert_util.to_float(results[7])
        info['total_active'] = convert_util.to_float(active_resultes[0])
        info['total_enroll'] = info['roomcard_num'] + info['gamePoint_num']
        info['total_active_roomcard'] = convert_util.to_float(active_resultes[1])
        info['total_active_gamepoint'] = convert_util.to_float(active_resultes[2])
        data = {"count": 0, "data": [info]}
        return json.dumps(data)
    else:
        return json.dumps({})

@admin_app.get('/statistics/match/info')
def get_statistics_info_data(redis, session):
    """
    赛事详情
    """
    curTime = datetime.now()
    lang = getLang()
    match_number = request.GET.get('match_number', '').strip()
    queryStr = """select match_info from match_record where match_number='%s'""" % (match_number)
    results = MysqlInterface.query_one(sql=queryStr)
    if results:
        for _result in results:
            matchInfo = json.loads(_result)
            rewardList = json.loads(matchInfo.get('rewardList', '[]'))
    else:
        return
    info = {
        "title": '赛事详情 [%s]' % match_number,
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        "feetypeList": FeeTypeList,
        "matchType": MatchTypeList,
        "rewardList": rewardList
    }
    return template('admin_statistics_match_info', info=info,  matchInfo=matchInfo, RES_VERSION=RES_VERSION, lang=lang)
