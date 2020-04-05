#-*- coding:utf-8 -*-
#!/usr/bin/python

import traceback
from bottle import *
from admin import admin_app
from config.config import STATIC_LAYUI_PATH,STATIC_ADMIN_PATH,BACK_PRE,RES_VERSION
from common.utilt import *
from model.activeModel import *
from access_module import *

@admin_app.get('/activice/check')
def getActiviceIndex(redis,session):
    """
        提交审核
    """
    tableid = request.GET.get('id', '').strip()
    if not tableid:
        return
    try:
        status = getActiviceStatus(redis,tableid)
        if status == STATUS_NON_CHECKED or status == STATUS_FAIL:
            setActiviceStatus(redis,tableid,STATUS_CHECKING)
    except Exception,ex:
        traceback.print_exc()
        return
    return redirect(BACK_PRE + '/activice/list')


@admin_app.get('/activice/confirm')
def getActiviceIndex(redis,session):
    """
        确认通过或不通过
    """
    tableid = request.GET.get('id', '').strip()
    result = request.GET.get('result', '').strip()
    log_debug('55555555555555555555555555555 %s' % tableid )
    if not tableid:
        return {"code":1,"msg":"没有tableid权限"}
    if int(session['id']) != systemId:
        return {"code":1,"msg":"不是系统管理员"}
    try:
        status = getActiviceStatus(redis, tableid)
        if status == STATUS_CHECKING:
            if result == '0':
                setActiviceStatus(redis, tableid, STATUS_FAIL)
            elif result == '1':
                setActiviceStatus(redis, tableid, STATUS_PASS)

        log_debug('55555555555555555555555555555 %s' % status)
    except Exception,ex:
        traceback.print_exc()
        return {"code":1,"msg":"查询出错"}
    return {"code":0,"msg":"审核通过","jumpUrl":BACK_PRE + '/activice/list'}

@admin_app.get('/activice/ready')
def getActiviceIndex(redis,session):
    """
        提交审核
    """
    tableid = request.GET.get('id', '').strip()
    if not tableid:
        return
    try:
        status = getActiviceStatus(redis,tableid)
        if status == STATUS_PASS:
            setActiviceStatus(redis,tableid,STATUS_READY)
    except Exception,ex:
        traceback.print_exc()
        return
    return redirect(BACK_PRE + '/activice/list')

@admin_app.get('/activice/close')
def getActiviceIndex(redis,session):
    """
        关闭活动
    """
    tableid = request.GET.get('id', '').strip()
    if not tableid:
        return
    try:
        status = getActiviceStatus(redis,tableid)
        if status in STATUS_READY:
            setActiviceStatus(redis,tableid,STATUS_CLOSE)
        elif status in STATUS_STARTING:
            agentid = getActiciveAgentid(redis,tableid)
            if agentid and redis.exists(ONLINE_ACTIVICE_LIST % agentid):
                rm_online_activice(redis,agentid,tableid)
    except Exception,ex:
        traceback.print_exc()
        return {"code": 0, "msg": "关闭失败", "jumpUrl": BACK_PRE + '/activice/list'}
    return {"code": 0, "msg": "关闭成功", "jumpUrl": BACK_PRE + '/activice/list'}