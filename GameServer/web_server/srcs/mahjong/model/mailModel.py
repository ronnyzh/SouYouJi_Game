#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    邮件模型
"""

from web_db_define import *
from datetime import datetime,timedelta
from admin  import access_module
from common.log import *
from config.config import *
from bottle import template
from datetime import datetime
from operator import itemgetter
from model.userModel import getAgentAllMemberIds
from common import log_util,web_util

SYS_TYPE  = '0'
FUN_TYPE  = '1'
MAIL_TYPE = '2'

MSGTYPE2DESC = {
    '0'         :       '系统消息',
    '1'         :       '活动消息',
    '2'         :       '邮件消息'
}

DESC2MSGTYPE = {
    '系统消息'         :       '0',
    '活动消息'         :       '1',
    '邮件消息'         :       '2'
}

FIELDS = [
    #配置  "變量名" = "獲取方式"

    "title              = request.forms.get('title','').strip()",
    "validDate          = request.forms.get('validDate','').strip()",
    "messageType        = request.forms.get('messageType','').strip()",
    "content            = request.forms.get('content','').strip()",
    "noticeId           = request.forms.get('noticeId','').strip()",
]
"""
邮件模块模型的一些基本配置
"""
MAIL_SETTING_INFO = {

        'mailTextWidth'         :   '100%',                         #规则编辑框宽度
        'mailTextHeight'        :   '350px',                        #规则编辑框高度
}

def deleteMsg(redis,msgId,memberId):
    """
    从玩家列表中移除
    """
    userMsgBox = FORMAT_USER_MESSAGE_LIST%(memberId)
    readList   = redis.smembers(FORMAT_MSG_READ_SET%(msgId))
    pipe = redis.pipeline()

    try:
        pipe.lrem(userMsgBox,msgId)
    except Exception,e:
        log_util.error('[try deleteMsg] ERROR msgId[%s] memberId[%s] errReason[%s]'%(msgId,memberId,e))
        return

    log_util.debug('[try deleteMsg] msgId[%s] memberId[%s] '%(msgId,memberId))
    pipe.execute()

def deleteAllMsg(redis,memberId):
    """
    从玩家列表中清楚所有的消息
    """
    log_debug('[FUNC][deleteAllMsg][info] memberId[%s]'%(memberId))
    userMsgBox = FORMAT_USER_MESSAGE_LIST%(memberId)
    pipe = redis.pipeline()
    try:
        pipe.delete(userMsgBox)
    except Exception,e:
        log_debug('[FUNC][deleteMsg][error] msgId[%s] memberId[%s] errReason[%s]'%(msgId,memberId,e))
        return

    pipe.execute()

def push2userMsgTable(redis,agentId,noticId):
    """
    将消息放进玩家的信息列表
    """
    pipe = redis.pipeline()
    #超级管理员发的公告需要塞到所有玩家的信息盒子
    memberIds = getAgentAllMemberIds(redis,agentId)
    noticeTable = FORMAT_GAMEHALL_NOTIC_TABLE%(noticId)
    pipe.hset(noticeTable,'status','1')
    log_debug('[FUNC][push2userMsgTable][info] agentId[%s] memberIds[%s]'%(agentId,memberIds))
    try:
        for memberId in memberIds:
            log_debug('[FUNC][push2userMsgTable][info] agentId[%s] send to memberId[%s] noticId[%s] success'\
                                %(agentId,memberId,noticId))
            pipe.lpush(FORMAT_USER_MESSAGE_LIST%(memberId),noticId)
            #pipe.set(FORMAT_USER_MESSAGE_LIST%(memberId,noticId),noticId)
    except Exception,e:
        log_debug('[FUNC][push2userMsgTable][Error] agentId[%s] reason[%s]'%(agentId,e))
        return

    pipe.execute()

def push_2_fish_users(redis,noticId):
    """
    将消息放进玩家的信息列表
    """
    pipe = redis.pipeline()
    #超级管理员发的公告需要塞到所有玩家的信息盒子
    memberIds = getAgentAllMemberIds(redis,agentId)
    noticeTable = FORMAT_GAMEHALL_NOTIC_TABLE%(noticId)
    pipe.hset(noticeTable,'status','1')
    log_debug('[FUNC][push2userMsgTable][info] agentId[%s] memberIds[%s]'%(agentId,memberIds))
    try:
        for memberId in memberIds:
            log_debug('[FUNC][push2userMsgTable][info] agentId[%s] send to memberId[%s] noticId[%s] success'\
                                %(agentId,memberId,noticId))
            pipe.lpush(FORMAT_USER_MESSAGE_LIST%(memberId),noticId)
            #pipe.set(FORMAT_USER_MESSAGE_LIST%(memberId,noticId),noticId)
    except Exception,e:
        log_debug('[FUNC][push2userMsgTable][Error] agentId[%s] reason[%s]'%(agentId,e))
        return

    pipe.execute()

def createNotice(redis,agentId,messageInfo,create_type='HALL'):
    """
    创建一条新信息
    """

    #创建新的公告记录
    curTime = datetime.now()
    dateStr = curTime.strftime("%Y-%m-%d")
    timeStr = curTime.strftime("%Y-%m-%d %H:%M")

    if create_type == 'HALL':
        noticListTable = FORMAT_GAMEHALL_NOTIC_LIST_TABLE
    else:
        noticListTable = FORMAT_FISHHALL_NOTIC_LIST_TABLE

    noticId = redis.incr(FORMAT_GAMEHALL_NOTIC_COUNT_TABLE)
    #读取的url
    readUrl = '/admin/notice/read?type=%s&id=%s&agentId=%s&action=%s'%(messageInfo['messageType'],noticId,agentId,create_type)
    messageInfo['read'] = '0'
    messageInfo['id'] = noticId
    messageInfo['link'] = readUrl
    messageInfo['groupId'] = agentId
    messageInfo['time'] = timeStr
    messageInfo['status'] = '0'
    pipe = redis.pipeline()
    try:
        noticTable = FORMAT_GAMEHALL_NOTIC_TABLE%(noticId)
        pipe.hmset(noticTable, messageInfo)
        #放进公告列表
        pipe.lpush(noticListTable, noticId)
        #放进代理列表
        agentSendMsgTable = FORMAT_MGR_SEND_MESSAGE_LIST%(agentId)
        pipe.lpush(agentSendMsgTable,noticId)
        #放进代理玩家列表
        #push2userMsgTable(redis,agentId,noticId)
    except Exception,e:
        log_debug('[FUNC][createNotice][error] reason[%s]'%(e))
        return None

    log_debug('[FUNC][createNotice][info] messageInfo[%s]'%(messageInfo))
    return pipe.execute()

def getNoticsList(redis,session,lang,agentId,hall_type='HALL'):
    """
    获取已发送公告列表
    """
    log_util.debug('systemId[%s] agentId[%s] HALL[%s]'%(systemId,agentId,hall_type))
    if int(agentId) == systemId:
        if hall_type == 'HALL':
            notice_ids = redis.lrange(FORMAT_GAMEHALL_NOTIC_LIST_TABLE,0,-1)
        else:
            notice_ids = redis.lrange(FORMAT_FISHHALL_NOTIC_LIST_TABLE,0,-1)
    else:
        notice_ids = redis.lrange(FORMAT_MGR_SEND_MESSAGE_LIST%(agentId),0,-1)

    log_util.debug('[try getNoticsList] agentId[%s] noticIds[%s] hall_type[%s] '%(agentId,notice_ids,hall_type))

    if redis.exists(FORMAT_NOTIC_INOF_TABLE):
        infoId = redis.hget(FORMAT_NOTIC_INOF_TABLE, 'noticId')
        if infoId in notice_ids:
            notice_ids.remove(infoId)

    noticList = []
    for notic_id in notice_ids:
        noticTable = FORMAT_GAMEHALL_NOTIC_TABLE%(notic_id)
        if not noticTable:
            continue
        noticeInfo = redis.hgetall(noticTable)
        noticeInfo['op'] = []
        # sessiob['access']
        for access in access_module.ACCESS_GAME_NOTICE_LIST:
            if access.url in eval(session['access']):
                if access.url[-4:] == 'push':
                    noticeInfo['op'].append({'url':access.url+"/{}".format(hall_type),'txt':'推送' \
                                if noticeInfo['status'] == '0' else '取消推送','method':access.method})
                else:
                    noticeInfo['op'].append({'url':access.url+"/{}".format(hall_type),'method':access.method,'txt':access.getTxt(lang)})
        noticList.append(noticeInfo)

    noticList = sorted(noticList, key=itemgetter('time'),reverse=True)
    return {'data':noticList,'count':len(noticList)}

def pushAgentMsg2User(redis,agentId,memberId):
    """
    将代理下的msg推送到新加入的代理中
    """

    pipe = redis.pipeline()
    #超级管理员发的公告需要塞到所有玩家的信息盒子
    parentAg = redis.hget(AGENT_TABLE%(agentId),'parent_id')
    sysNoticeIds = redis.lrange(FORMAT_MGR_SEND_MESSAGE_LIST%('1'),0,-1)
    noticIds = redis.lrange(FORMAT_MGR_SEND_MESSAGE_LIST%(parentAg),0,-1)
    #log_debug('[FUNC][push2userMsgTable][info] agentId[%s] memberIds[%s]'%(agentId,memberIds))
    try:
        for sysNoticeId in sysNoticeIds:
            noticeTable = FORMAT_GAMEHALL_NOTIC_TABLE%(sysNoticeId)
            status = redis.hget(noticeTable,'status')
            if not status:
                status = 0
            if int(status):
                pipe.lpush(FORMAT_USER_MESSAGE_LIST%(memberId),sysNoticeId)

        for noticId in noticIds:
            noticeTable = FORMAT_GAMEHALL_NOTIC_TABLE%(noticId)
            status = redis.hget(noticeTable,'status')
            if not status:
                status = 0
            if int(status):
                pipe.lpush(FORMAT_USER_MESSAGE_LIST%(memberId),noticId)
            log_debug('[FUNC][push2userMsgTable][info] agentId[%s] send to memberId[%s] noticId[%s] success'\
                                %(agentId,memberId,noticId))
        #删除玩家的已读邮件
        redis.delete(FORMAT_MSG_READ_SET%(memberId))
    except Exception,e:
        log_debug('[FUNC][push2userMsgTable][Error] agentId[%s] reason[%s]'%(agentId,e))
        return

    pipe.execute()
