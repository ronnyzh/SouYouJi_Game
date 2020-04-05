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
from model.partyModel import *
from access_module import *
import hashlib
import json
import traceback
import copy
#
# 页面输出
#


@admin_app.get('/party/index')
@admin_app.get('/party/setting')
def getPartyCompetitionList(redis,session):
    """
    竞技场开启设置
    """
    lang = getLang()

    # 权限
    agentId = session['id']
    creatAgUrl = BACK_PRE + '/activice/resource_add'
    if creatAgUrl in redis.smembers(AGENT2ACCESSBAN % (agentId)):
        createAg = '0'
    else:
        createAg = '1'
    #
    # 读取竞技场状态
    status = is_party_comp_open(redis)
    # 读取竞技场开启时间
    time = get_party_time(redis)

    info = {
        "title"                 :   lang.PARTY_COMPETITION_SETTING,
        "submitUrl"             :   BACK_PRE+"/party/timeModify",
        'STATIC_LAYUI_PATH'     :   STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'     :   STATIC_ADMIN_PATH,
        'back_pre'              :   BACK_PRE,
        'competitionState'      :   status, #竞技场状态，0关闭  1开启
        'competitionTime'       :   time,   #竞技场开启时间列表
        'backUrl'               :   BACK_PRE+"/party/index",
        'createAccess'          :   createAg,
        'openUrl'               :   BACK_PRE+"/party/open",
        'closeUrl'               :   BACK_PRE+"/party/close",
    }
    return template('admin_party_setting_create',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/party/open')
def setPartyCompetitionOpen(redis,session):
    #  0 关 1 开
    # switch =  0 关 1 开
    lang = getLang()
    switch = 1
    if set_party_comp(redis, switch):
        return {'code': 0, 'msg': lang.PARTY_COMPETITION_OPEN_SUCCESS}
    return {'code': 1, 'msg': lang.PARTY_COMPETITION_OPEN_ERROR}

@admin_app.post('/party/close')
def setPartyCompetitionClose(redis,session):
    # switch =  0 关 1 开
    lang = getLang()
    switch = 0
    if set_party_comp(redis,switch) :
        return {'code':0,'msg':lang.PARTY_COMPETITION_CLOSE_SUCCESS}
    return {'code':1,'msg':lang.PARTY_COMPETITION_CLOSE_ERROR}

@admin_app.post('/party/timeModify')
def setPartyCompetitionTimeModify(redis,session):
    """
    设置竞技场开启时间
    request.json格式：
    [
        [开始时间,终止时间]，
        [开始时间,终止时间]，
    ]
    """
    lang = getLang()
    timeList = copy.deepcopy(request.json)
    jumpUrl = BACK_PRE+"/party/index"
    if timeList:
        res = modify_party_time(redis,timeList)
        log_debug("****************设置竞技场开启时间{0}-{1}".format(type(timeList),timeList))
        if res:
            return {'code': 0, 'msg': lang.PARTY_COMPETITION_SETTING_SUCCESS, 'jumpUrl': jumpUrl}

    return {'code':1,'msg':lang.PARTY_COMPETITION_SETTING_ERROR,'jumpUrl':jumpUrl}

