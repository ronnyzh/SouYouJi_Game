#!/usr/bin/env python
#-*-coding:utf-8 -*-
"""
@Author: $Author$
@Date: $Date$
@version: $Revision$

Description:
 Description
"""
from bottle import request,response,default_app
from model.hallModel import *
from fish import fish_app
from datetime import datetime
from common.utilt import allow_cross,getInfoBySid

@fish_app.post('/mailRefresh')
@allow_cross
def do_mailRefresh(redis,session):
    """
    捕鱼邮件轮询接口
    """
    fields = ('sid',)
    for field in fields:
        exec('%s = request.forms.get("%s","").strip()'%(field,field))
    try:
        log_debug('[try do_getBroadcast] sid[%s]'%(field))
    except:
        return {'code':-300,'msg':'接口参数错误'}

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/getBroadcast/',SessionTable,account,sid,verfiySid)
    log_debug('[try do_refresh] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    userMailList = []
    unReadMailList = []
    userMailTable = FORMAT_USER_MSG_FISH_LIST%(uid)
    mail_ids = redis.lrange(userMailTable,0,-1)
    for mail_id in mail_ids:
        mailTable = FORMAT_GAMEHALL_NOTIC_TABLE%(mail_id)
        if not redis.exists(mailTable) or mail_id == '':
            continue
        readList = redis.smembers(FORMAT_MSG_READ_SET%(mail_id))
        mailInfo = redis.hgetall(mailTable)
        if uid in readList:
            mailInfo['read'] = '1'
        else:
            mailInfo['read'] = '0'

        if mailInfo['read'] == '1':
            userMailList.append(mailInfo)
        else:
            unReadMailList.append(mailInfo)

        log_util.debug('[mailRefresh] mail_id[%s] mailInfo[%s] readList[%s]'%(mail_id,mailInfo,readList))

    #合并消息
    userMailList = unReadMailList + userMailList
    return {'code':0,'mailList':userMailList,'unReadNums':len(unReadMailList)}

@fish_app.post('/getBroadcast')
@allow_cross
def do_getBroadcast(redis,session):
    """
    捕鱼大厅广播
    """
    curTime  =  datetime.now()
    fields = ('sid',)
    for field in fields:
        exec('%s = request.forms.get("%s","").strip()'%(field,field))
    try:
        log_debug('[try do_getBroadcast] sid[%s]'%(field))
    except:
        return {'code':-300,'msg':'接口参数错误'}

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/getBroadcast/',SessionTable,account,sid,verfiySid)
    log_debug('[try do_refresh] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    groupId = redis.hget(user_table, 'parentAg')
    if redis.exists(FORMAT_BROADCAST_LIST_TABLE):
        broadcasts = getBroadcasts(redis,groupId)
    else:
        broadcasts = {'broadcasts':{}}

    return {'code':0,'data':broadcasts}

@fish_app.post('/getHallBroad')
@allow_cross
def get_hall_broad(redis,session):
    """
    获取大厅播放广播
    级别优先级: 全服维护广播>全服循环广播>地区维护广播>地区循环广播
             先播放优先级高的一条
    """
    fields = ('sid',)
    for field in fields:
        exec('%s = request.forms.get("%s","").strip()'%(field,field))

    try:
        log_debug('[try get_hall_broad] sid[%s]'%(sid))
    except:
        return {'code':-300,'msg':'接口参数错误!'}

    SessionTable,account,uid,verfiySid = getInfoBySid(redis,sid)
    check_code,check_msg,user_table = check_session_verfiy(redis,'/fish/getBroadcast/',SessionTable,account,sid,verfiySid)
    log_debug('[try do_refresh] check_code[%s] check_msg[%s]'%(check_code,check_msg))
    if int(check_code)<0:
        if check_code == -4:
            return {'code':check_code,'msg':check_msg,'osid':sid}
        return {'code':check_code,'msg':check_msg}

    broadInfo = getHallBroadInfo(redis,1,FISH_BRO_CONTAIN_ALL_LIST,'FISH')
    if not broadInfo:
        return {'code':0,'broadcasts':[],'requestPerSec':10}

    return {'code':0,'broadcasts':broadInfo,'requestPerSec':10}
