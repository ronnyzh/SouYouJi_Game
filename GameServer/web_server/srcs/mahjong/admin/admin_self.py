#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    个人信息模块
"""
from bottle import *
from admin import admin_app
from config.config import STATIC_LAYUI_PATH,STATIC_ADMIN_PATH,BACK_PRE,RES_VERSION
from common.utilt import *
from datetime import datetime
from model.agentModel import *
import hashlib
import json

@admin_app.get('/self/modifyPasswd')
def getSelfModifyPasswd(redis,session):
    lang = getLang()

    info  =  {

        "title"                  :   '修改密码',
        "submitUrl"              :   BACK_PRE+"/self/modifyPasswd",
        'STATIC_LAYUI_PATH'      :   STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :   STATIC_ADMIN_PATH 
    }

    return template('admin_self_modifyPasswd',lang=lang,info=info,RES_VERSION=RES_VERSION)

@admin_app.post('/self/modifyPasswd')
def do_ModifyPasswd(redis,session):
    """
    修改密码逻辑
    """
    curTime = datetime.now()
    selfAccount,selfUid = session['account'],session['id']
    oldPasswd = request.forms.get('passwd','').strip()
    comfirmPasswd = request.forms.get('comfirmPasswd','').strip()
    comfirmPasswd1 = request.forms.get('comfirmPasswd1','').strip()

    #print
    print '[%s][selfModifyPasswd][info] oldPasswd[%s] comfirmPasswd[%s] comfirmPasswd1[%s]'\
                        %(curTime,oldPasswd,comfirmPasswd,comfirmPasswd1)

    checkNullFields = [
            {'field':oldPasswd,'msg':'请输入你的登录密码(旧密码)'},
            {'field':comfirmPasswd,'msg':'请输入新的登录密码'},
            {'field':comfirmPasswd1,'msg':'请再次输入新的登录密码'}
    ]

    for check in checkNullFields:
        if not check['field']:
            return {'code':1,'msg':check['msg']}

    agentTable = AGENT_TABLE%(selfUid)
    passwd = redis.hget(agentTable,'passwd')

    if passwd != hashlib.sha256(oldPasswd).hexdigest():
        return {'code':1,'msg':'你的登录密码不正确'}

    if comfirmPasswd != comfirmPasswd1:
        return {'code':1, 'msg': '两次密码不一致'}
    else:
        if len(comfirmPasswd) not in range(6, 17):
            return {'code': 1, 'msg': '新密码必须在6-16位之间'}

    pipe = redis.pipeline()
    try:
        pipe.hset(agentTable,'passwd',hashlib.sha256(comfirmPasswd).hexdigest())
    except Exception,e:
        return {'code':1,'msg':'修改密码错误'}

    pipe.execute()
    return {'code':0,'msg':'密码修改成功，请牢记.','jumpUrl':BACK_PRE+'/self/modifyPasswd'}

@admin_app.get('/self/syslog')
def getSysLog(redis,session):
    lang      = getLang()

    isList = request.GET.get('list','').strip()
    startDate = request.GET.get('startDate','').strip()
    endDate = request.GET.get('endDate','').strip()

    selfAccount,selfUid = session['account'],session['id']

    if isList:
        logs = getAgentOpLog(redis,selfUid,startDate,endDate)
        return json.dumps(logs)
    else:
        info = {
                'title'         :    '我的操作日志',
                'searchStr'     :    '',
                'showLogType'   :    '',
                'listUrl'       :    BACK_PRE+'/self/syslog?list=1',
                'STATIC_LAYUI_PATH'      :   STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :   STATIC_ADMIN_PATH 
        }

        return template('admin_self_syslog',info=info,lang=lang,RES_VERSION=RES_VERSION)



def getSysLogByAgent(redis,selfAccount, startDate, endDate, findAccount = ''):
    try:
        startDateTime = datetime.strptime(startDate, '%Y-%m-%d')
        endDateTime = datetime.strptime(endDate, '%Y-%m-%d')
    except ValueError:
        abort(403)

    if startDateTime > endDateTime:
        abort(403)

    deltaTime = timedelta(1)

    totalList = []
    while startDateTime <= endDateTime:
        adminLogDatesetTable = FORMAT_AGENT_OP_LOG_DATESET_TABLE%(startDateTime.strftime('%Y-%m-%d'))
        logIds = redis.lrange(adminLogDatesetTable, 0, -1)
        for logId in logIds:
            logTable = FORMAT_AGENT_OP_LOG_TABLE%(logId)
            logInfo = redis.hgetall(logTable)
            if logInfo['account'] == selfAccount:
                totalList.append(logInfo)

        startDateTime += deltaTime
    return totalList

@admin_app.get('/self/loginLog')
def getLoginLog(redis,session):
    lang  =  getLang()

    isList = request.GET.get('list','').strip()
    startDate = request.GET.get('startDate','').strip()
    endDate   = request.GET.get('endDate','').strip()

    selfAccount,selfUid = session['account'],session['uid']

    if isList:
        logs = getSysLogByAgent(redis,selfAccount,startDate,endDate)
        return json.dumps(logs)
    else:
        info = {
                'title'                  :       '(%s)登录日志查询'%(selfAccount),
                'listUrl'                :       BACK_PRE+'/self/loginLog?list=1',
                'searchStr'              :       '',
                'showLogType'            :       True,
                'STATIC_LAYUI_PATH'      :   STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :   STATIC_ADMIN_PATH 
        }

        return template('admin_self_loginLog',info=info,lang=lang,RES_VERSION=RES_VERSION)