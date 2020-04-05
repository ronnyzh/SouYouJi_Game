#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    通用工具模块
"""
from bottle import request,response,redirect,abort
from i18n.i18n import getLangInst
import inspect
from datetime import datetime,timedelta
from common.install_plugin import *
from config.config import *
from web_db_define import *
from common.log import *
import random
import redis

def allow_cross(fn):
    def _add_cross(*args,**kw):
        #跨域装饰器
        session = session_plugin.getSession()
        r = redis.Redis(connection_pool=session_plugin.connection_pool)
        argNames = inspect.getargspec(fn)[0]
        if redis_plugin.keyword in argNames:
            kw[redis_plugin.keyword] = session.rdb

        if session_plugin.keyword in argNames:
            kw[session_plugin.keyword] = session

        response.add_header('Access-Control-Allow-Origin', '*')

        return fn(*args,**kw)

    return _add_cross

def getInfoBySid(redis,sid):
    """
    通过Sid获取SessionTable, account, uid, verfiySid信息
    """
    SessionTable = FORMAT_USER_HALL_SESSION%(sid)
    account,uid = redis.hmget(SessionTable, ('account','uid'))
    verfiySid   = redis.get(FORMAT_USER_PLATFORM_SESSION%(uid))
    log_debug('[try getInfoById] account[%s] sessionKey[%s] verfiyKey[%s]'%(account,sid,verfiySid))
    return SessionTable, account, uid, verfiySid

def ServerPagination(dates,pageSize,pageNumber):
    """
    服务器端分页函数
    dates：查询到数据集合
    pageSize:每页显示数据数
    pageNumber:页数
    """
    pageSize,pageNumber = int(pageSize),int(pageNumber)
    start  = (pageNumber-1)*pageSize
    end  = pageSize*pageNumber
    dates = list(dates)
    return dates[start:end]

def getLang():
    """
        获取语言包
    """
    return getLangInst(getCurLangByCookie())

def getCurLangByCookie():
    if not request.get_cookie('gglang'):
        return request.get_cookie('gglang','CHN')
    else:
        return request.get_cookie('gglang')

def checkLogin(fn):
    def _check(*args,**kw):
        session = session_plugin.getSession()
        if not session.get('account',None):
            return redirect('/admin/login')

        argNames = inspect.getargspec(fn)[0]
        if redis_plugin.keyword in argNames:
            kw[redis_plugin.keyword] = session.rdb
        if session_plugin.keyword in argNames:
            kw[session_plugin.keyword] = session

        return fn(*args,**kw)

    return _check

def checkAccess(fn):
    '''  验证权限  '''
    def _check(*args,**kw):
        session = session_plugin.getSession()
        r = redis.Redis(connection_pool=session_plugin.connection_pool)
        if not session.get('account',None):
            return redirect(BACK_PRE+'/login')
        elif request.fullpath not in eval(session.get('access', '[]')):
            abort(403)

        agentId = session.get('id',None)
        recharge = r.hget(AGENT_TABLE%(agentId),'recharge')
        log_debug("access[%s] recharge[%s]"%(request.fullpath,recharge))

        argNames = inspect.getargspec(fn)[0]
        if redis_plugin.keyword in argNames:
            kw[redis_plugin.keyword] = session.rdb

        if session_plugin.keyword in argNames:
            kw[session_plugin.keyword] = session

        return fn(*args,**kw)

    return _check

def getDaya4Week():
    """
        返回一个星期时间
    """
    weekDelTime = timedelta(7)
    weekBefore = datetime.now()-weekDelTime
    startDate = weekBefore
    endDate   = datetime.now()

    return startDate.strftime('%Y-%m-%d'),endDate.strftime('%Y-%m-%d')

def get_week_date_list():
    """
    返回一个星期时间
    """
    weekDelTime = timedelta(6)
    one_del_time = timedelta(1)
    weekBefore = datetime.now()-weekDelTime
    startDate = weekBefore
    endDate   = datetime.now()
    date_list = []
    while startDate <= endDate:
        date_list.append(startDate.strftime('%Y-%m-%d'))
        startDate+=one_del_time

    return date_list

def get_week_date_obj(start_date,end_date):
    '''
    返回一段时间的对象列表
    '''
    startDate = datetime.strptime(start_date,'%Y-%m-%d')
    endDate   = datetime.strptime(end_date,'%Y-%m-%d')
    date_list = []
    one_del_time = timedelta(1)
    while startDate<=endDate:
        dateStr = datetime.strftime(startDate,'%Y-%m-%d')
        date_list.append(dateStr)

        startDate+=one_del_time

    return date_list

def getOrderNo(agentId):
    """
        生成订单编号
    """
    curTime = datetime.now()
    dateStr = curTime.strftime('%Y%m%d%H%M%S')
    return dateStr+str(agentId)+str(random.randint(000,999))

def write2HallNotice(redis,bType,broadcasts):
    """
    写入公告
    """
    curTime = datetime.now()
    broadListTable = FORMAT_BROADCAST_LIST_TABLE
    dayBroadTable  = DAY_BROADCAST_LIST%(curTime.strftime('%Y-%m-%d'))
    hallListTable  = HALL_BROADCAST_LIST

    #创建新的代理充钻石记录
    id = redis.incr(FORMAT_BROADCAST_COUNT_TABLE)

    broadTable = FORMAT_BROADCAST_TABLE%(id)
    broadcasts['id'] = id
    broadcasts['type'] = bType
    broadcasts['sendTime'] = curTime.strftime('%Y-%m-%d %H:%M:%S')
    pipe = redis.pipeline()
    pipe.hmset(broadTable,broadcasts)
    pipe.expire(broadTable,60*24)
    pipe.lpush(broadListTable, id)
    if bType in ['1','2']:
        pipe.lpush(HALL_BROADCAST_LIST,id)
    pipe.execute()
    return id

def formatCredit(credit):
    creditStr = '%.2f'%(float(credit))
    l = creditStr.split('.')
    s = ''
    _end = -len(l[0])-1
    for i in xrange(-1, _end, -1):
        char = l[0][i]
        if char.isdigit() and i % 3 == 2 and i != -1:
            s = ',' + s
        s = char + s

    return s + '.' + l[1]
