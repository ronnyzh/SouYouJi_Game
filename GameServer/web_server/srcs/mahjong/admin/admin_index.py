#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    this is Description
"""

from bottle import *
from admin import admin_app
from config.config import STATIC_LAYUI_PATH,STATIC_ADMIN_PATH,BACK_PRE,RES_VERSION
import access_module
from model.agentModel import *
from common.utilt import *
from common.log import *
from common import web_util,convert_util,menu_util,log_util
import subprocess
from model.statisticsModel import get_active_reports
#后台首页
import time

@admin_app.get('/')
@admin_app.get('/<action>')
@checkLogin
def get_index_page(redis,session,action='HALL'):
    lang = getLang()
    my_accesses = eval(session['access'])
    datas = {
            'STATIC_ADMIN_PATH'             :   STATIC_ADMIN_PATH,
            'ADMIN_DEFAULT_PAGE'            :   '/admin/home?sys={}'.format(action),
            'agent_id'                      :   session['id'],
            'show_data_url'                 :   BACK_PRE+'/getHomePageData?sys={}'.format(action),
    }
    #初始化后台菜单
    if action == 'HALL':
        """ 棋牌大厅数据生成 """
        hall_fields = ('type','parent_id','roomCard','open_auth')
        agent_type,agent_parentAg,agent_cards,agent_openAuth = redis.hmget(AGENT_TABLE%(session['id']),hall_fields)
        access_modules = access_module.MENU_MODULES
        if int(agent_type) in [SYSTEM_ADMIN]:
            roomcard = '无限制'
        else:
            roomcard = agent_cards
        open_auth = convert_util.to_int(agent_openAuth)
        datas['room_card']  = roomcard
        datas['agent_type'] = agent_type
        datas['open_auth']  =open_auth
        datas['show_card_bar'] = True
        datas['open_auth_text'] =  OPENAUTH_2_TXT[open_auth]
        datas['link_fish_txt']  = '捕鱼系统后台'
        datas['link_fish_url']  = BACK_PRE+'/FISH'

    else:
        info = {
            'title': '您没有权限使用该功能',
            'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        }
        return template('admin_tips',  info=info, RES_VERSION=RES_VERSION, lang=lang, session=session,
                        TYPE2TXT=lang.TYPE_2_ADMINTYPE)
        """ 捕鱼大厅数据生成 """
        fish_fields = ('type','parent_id')
        agent_type,agent_parentAg = redis.hmget(AGENT_TABLE%(session['id']),fish_fields)
        access_modules = access_module.FISH_MENU_MODULES
        #数据绑定
        datas['agent_type']  = agent_type
        datas['link_fish_txt']  = '棋牌系统后台'
        datas['link_fish_url']  = BACK_PRE+'/HALL'

    #生成菜单数据
    menus = menu_util.init_menus(lang,my_accesses,access_modules)
    return template('admin_base',datas=datas,RES_VERSION=RES_VERSION,lang=lang,session=session,TYPE2TXT=lang.TYPE_2_ADMINTYPE,mainModules=menus)

@admin_app.get('/home')
def getSystemInfoPage(redis,session):
    """
    获取系统信息页面
    """
    lang = getLang()
    selfUid = session['id']
    curTime = convert_util.to_dateStr(datetime.now())

    fields = ('sys',)
    for field in fields:
        exec('%s=request.GET.get("%s","").strip()'%(field,field))

    home_info = {
                'title'                  :          '首页',
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
                'show_data_url'          :          '/admin/getHomePageData?sys=%s'%(sys),
    }

    if sys == 'HALL':
        # 当日注册人数
        regist_total =  convert_util.to_int(redis.scard(FORMAT_REG_DATE_TABLE%(curTime)))
        if int(selfUid) == 1:
            member_total = convert_util.to_int(redis.scard(ACCOUNT4WEIXIN_SET))
            login_total = convert_util.to_int(redis.get(DAY_ALL_LOGIN_COUNT%(curTime)))
            play_room_total = convert_util.to_int(redis.get(DAY_ALL_PLAY_ROOM_CARD%(curTime)))

        else:
            member_total = convert_util.to_int(getAgentMemberTotal(redis,session['id']))
            regist_total =  0
            login_total = convert_util.to_int(getAgentMemberLogin(redis,session['id'],curTime))
            play_room_total = convert_util.to_int(getAgentRoomByDay(redis,session['id'],curTime))

        home_info['member_total']  = member_total
        home_info['login_per_day'] = login_total
        home_info['regist_per_day'] = regist_total
        home_info['play_room_per_day'] = play_room_total
    else:
        member_total = convert_util.to_int(redis.scard(ACCOUNT4WEIXIN_SET4FISH))
        regist_total = convert_util.to_int(redis.scard(FORMAT_REG_DATE_TABLE4FISH%(curTime)))
        login_total = convert_util.to_int(redis.scard(FORMAT_LOGIN_DATE_TABLE4FISH%(curTime)))
        recharge_total = convert_util.to_int(redis.hget(FISH_SYSTEM_DATE_RECHARGE_TOTAL%(curTime),'recharge_coin_total'))
        home_info['member_total'] = member_total
        home_info['regist_per_day'] = regist_total
        home_info['login_per_day'] = login_total
        home_info['recharge_total'] = recharge_total

    return template('admin_home',info=home_info,lang=lang,session=session,sys=sys,RES_VERSION=RES_VERSION)

@admin_app.get('/getHomePageData')
def get_show_detail(redis,session):
    """
    获取7日的数据变化
    """
    SYS_HOME_DATA_SETTING = {
            'FISH'   :  {
                                'data':['每日注册','每日活跃数','每日充值数'],
                                'login_datas'       :   [],
                                'recharge_datas'    :   [],
                                'reg_datas'         :   []
            },

            'HALL'   :  {
                                'data':['每日注册','每日活跃数','每日耗钻数'],
                                'login_datas'       :   [],
                                'take_datas'        :   [],
                                'reg_datas'         :   [],
                        }
    }

    fields = ('sys',)
    for field in fields:
        exec('%s=request.GET.get("%s","").strip()'%(field,field))

    #获取生成对象类型
    show_obj = SYS_HOME_DATA_SETTING[sys]
    #获取当前一周日期并格式化为字符串
    week_date_lists = get_week_date_list()
    if sys == 'HALL':
        for week_date in week_date_lists:
            show_obj['reg_datas'].append(
                        convert_util.to_int(redis.scard(FORMAT_REG_DATE_TABLE%(week_date)))
            )
            show_obj['take_datas'].append(
                    convert_util.to_int(redis.get(DAY_ALL_PLAY_ROOM_CARD%(week_date)))
            )
            #show_obj['login_datas'].append(
            #        convert_util.to_int(redis.get(DAY_ALL_LOGIN_COUNT%(week_date)))
            #)
            selfUid = session['id']
            data = get_active_reports(redis,week_date,week_date,selfUid)
            if data["data"]:
                show_obj['login_datas'].append(convert_util.to_int(data["data"][0]["login_count"]))
            else:
                show_obj['login_datas'].append(
                       convert_util.to_int(redis.get(DAY_ALL_LOGIN_COUNT%(week_date)))
                )


        show_obj['series'] = [
                        {'name':'每日注册','type':'line','data':show_obj['reg_datas'], 'itemStyle' : { 'normal': {'label' : {'show': 'true'}}},'areaStyle': {'normal': {}}},
                        {'name':'每日耗钻数','type':'line','data':show_obj['take_datas'], 'itemStyle' : { 'normal': {'label' : {'show': 'true'}}},'areaStyle': {'normal': {}}},
                        {'name':'每日活跃数','type':'line','data':show_obj['login_datas'], 'itemStyle' : { 'normal': {'label' : {'show': 'true'}}},'areaStyle': {'normal': {}}},
        ]
    else:
        for week_date in week_date_lists:
            show_obj['reg_datas'].append(
                        convert_util.to_int(redis.scard(FORMAT_REG_DATE_TABLE4FISH%(week_date)))
            )
            show_obj['recharge_datas'].append(
                    convert_util.to_int(redis.hget(FISH_SYSTEM_DATE_RECHARGE_TOTAL%(week_date),'recharge_coin_total'))
            )
            show_obj['login_datas'].append(
                    convert_util.to_int(redis.scard(FORMAT_LOGIN_DATE_TABLE4FISH%(week_date)))
            )

        show_obj['series']= [
                        {'name':'每日注册','type':'line','data':show_obj['reg_datas']},
                        {'name':'每日充值数','type':'line','data':show_obj['recharge_datas']},
                        {'name':'每日活跃数','type':'line','data':show_obj['login_datas']},
        ]

    return web_util.do_response(1,msg="",jumpUrl="",data={'week':week_date_lists,'series':show_obj['series'],'legen':show_obj['data']})

@admin_app.get('/checkAdminOL')
def checkAdminOl(redis,session):
    """
    检测是否超时
    """
    if session.get('account',None):
        return {'code':1}

    return {'code':0,'msg':'长时间未操作或该账号在其他地方登陆'}

@admin_app.get('/logout')
def get_login_out(redis,session):
    """
    后台管理登出
    """
    curTime = datetime.now()
    agent_account = session['account']
    agent_id      = session['id']
    session['account'],session['id'],session['time_stamp'],session['index_path'] = '','',None,None

    log_util.info('[try get_login_out] time[%s] user[%s] has logout.'%(curTime,agent_account))

    return redirect(BACK_PRE+'/login')
