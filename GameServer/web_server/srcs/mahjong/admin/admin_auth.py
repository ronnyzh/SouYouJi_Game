#-*- coding:utf-8 -*-
#!/usr/bin/env python

"""
Author : $Author$
Date   : $Date$
Revision:$Revision$

Description:
    后台用户验证模块
"""
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from bottle import request,abort,template,response,redirect
from admin import admin_app
#from common.log import *
from config.config import *
from common.utilt import *
from common.validcode import create_validate_code
from common import encrypt_util
from datetime import datetime
from web_db_define import *
from model.agentModel import *

@admin_app.get('/login')
def getLoginPage(redis,session):
    """
        后台管理验证模块
    """
    lang = getLang()

    info = {
                    'vcodeUrl'               :           BACK_PRE+'/vcode',
                    'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
                    'submitUrl'              :           BACK_PRE+'/login',
                    'account'                :       '',
                    'passwd'                 :       '',
    }
    return template('admin_login',info=info,lang=lang,message='',RES_VERSION=RES_VERSION)

@admin_app.post('/login')
def do_login(redis,session):
    lang = getLang()
    account = request.forms.get('userName','').strip()
    passwd  = request.forms.get('password','').strip()
    vcode   = request.forms.get('code','').strip()

    info = {
            'title'                  :           '管理员登录',
            'submitUrl'              :           BACK_PRE+'/login',
            'account'                :           account,
            'passwd'                 :           passwd,
            'vcodeUrl'               :           BACK_PRE+'/vcode',
            'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
    }

    if not account or not passwd:
        return template('admin_login',message='请填写账号和密码',info=info,lang=lang,RES_VERSION=RES_VERSION)

    try:
        if vcode.upper() != session['maj_vcode'].upper():
            return template('admin_login',message='验证码无效',info=info,lang=lang,RES_VERSION=RES_VERSION)
    except:
        return template('admin_login',message='验证码过期,请重新登录',info=info,lang=lang,RES_VERSION=RES_VERSION)

    agentId = getAgentId(redis,account)
    adminTable = AGENT_TABLE%(agentId)

    # log_debug('[Try login] account[%s] password[%s] adminTable[%s]'%(account,passwd,adminTable))
    if not redis.hgetall(adminTable):
        return template('admin_login',message='无效的账号或密码',info=info,lang=lang,RES_VERSION=RES_VERSION)

    adminPasswd,valid,agent_type = redis.hmget(adminTable,('passwd','valid','type'))

    if  adminPasswd != encrypt_util.to_sha256(passwd):
        #记录登录日志
        agentOpLog(redis,account,2,request.remote_addr)
        return template('admin_login',message='无效的账号或密码',info=info,lang=lang,RES_VERSION=RES_VERSION)

    if valid != '1':
        return template('admin_login',message='账号已被冻结',info=info,lang=lang,RES_VERSION=RES_VERSION)

    #同一账号不能同时登录
    # global ACCOUNT_SESSION
    # if account in ACCOUNT_SESSION:
    #     sessionKey  = ACCOUNT_SESSION[account]
    #     if redis.exists(sessionKey):
    #         redis.delete(sessionKey)
    #     ACCOUNT_SESSION[account] = session.session_hash
    # else:
    #     ACCOUNT_SESSION[account] = session.session_hash
    if agent_type == '1':
        redis.sadd(AGENT2ACCESS%(agentId),'/admin/agent/open_auth')

    #更新登录IP和登陆日期
    session['lastLoginIp'], session['lastLoginDate'],session['type'] = \
        redis.hmget(adminTable, ('lastLoginIp', 'lastLoginDate','type'))

    curTime = datetime.now()
    redis.hmset(adminTable, {
        'lastLoginIp'     :   request.remote_addr,
        'lastLoginDate'   :   curTime.strftime("%Y-%m-%d %H:%M:%S")
    })

    #记录session信息
    session['account'] = account
    session['id'] = agentId
    #重新生成权限
    getNewAccess(redis,agentId)
    session['access'] = str(redis.smembers(AGENT2ACCESS%(agentId)))
    #记录登录日志
    agentOpLog(redis,account,1,request.remote_addr)

    return redirect('/admin')

@admin_app.get('/vcode')
def changeVerfiyCode(session):
    # if checkServiceOutDate(redis):
    #     return ''
    img, vcode = create_validate_code()
    session['maj_vcode'] = vcode.upper()

    mstream = StringIO()
    img.save(mstream, "GIF")
    response.set_header('Content-Type', 'image/gif')
    return mstream.getvalue()
