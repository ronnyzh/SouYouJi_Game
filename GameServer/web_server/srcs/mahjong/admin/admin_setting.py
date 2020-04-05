#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    系统设置模块
"""
from bottle import request,response,template,default_app
from admin import admin_app
from config.config import STATIC_LAYUI_PATH,STATIC_ADMIN_PATH,BACK_PRE,PARTY_PLAYER_COUNT,RES_VERSION
from common.utilt import *
from common.log import *
from common import convert_util,log_util,web_util
from datetime import datetime
from web_db_define import ORDER2WEIXIN_SWITCH
from model.hallModel import *
import json

#系统配置
conf = default_app().config

@admin_app.get('/setting/system')
@checkLogin
def getSysSetting(redis,session):
    """
    系统设置页面
    """
    curTime = datetime.now()
    lang    = getLang()

    info = {
                'title'                  :           lang.MENU_GAME_PAY_LIST_TXT,
                'settingUrl'             :           BACK_PRE+'/setting/system',
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
    }

    """
    系统设置的参数列表
    [
        {'name':xxxx,'value':xxx,'desc':xxxx},
        {'name':xxxx,'value':xxx,'desc':xxxx},
        {'name':xxxx,'value':xxx,'desc':xxxx},
    ]
    """
    wechatSwitch = redis.get(ORDER2WEIXIN_SWITCH)
    if not wechatSwitch:
        wechatSwitch = 0
    gameServerUrl = redis.get(GAME_SERVER_URL)
    if not gameServerUrl:
        gameServerUrl = ''

    settings = [

         {'name':'wechatSwitch','title':'支付设置','value':wechatSwitch,'desc':'微信支付开关'},
         {'name':'gameServerUrl','title':'游戏服务域名','value':gameServerUrl,'desc':'游戏服务地址'}

    ]

    return template('admin_setting_system',info=info,lang=lang,settings=settings,RES_VERSION=RES_VERSION)

@admin_app.get('/setting/fish/system')
def get_fish_setting(redis,session):
    """
    捕鱼系统参数设置页面
    """
    curTime = datetime.now()
    lang    = getLang()
    get_confg_fields = ('share_coin','exchange_shop','hall_shop','shop_version','exchange_shop_ver','wechat_switch')
    if not redis.exists(FISH_CONSTS_CONFIG):
        #首次加载
        init_date = {
                'share_coin'        :       conf.get('fish.share_coin'),
                'exchange_shop'     :       conf.get('fish.exchange_shop'),
                'hall_shop'         :       conf.get('fish.hall_shop'),
                'shop_version'      :       conf.get('fish.shop_version'),
                'exchange_shop_ver' :       conf.get('fish.exchange_shop_ver'),
                'wechat_switch'     :       conf.get('fish.wechat_switch')
        }
        redis.hmset(FISH_CONSTS_CONFIG,init_date)

    share_coin,exchange_shop,hall_shop,shop_version,exchange_shop_ver,wechat_switch = redis.hmget(FISH_CONSTS_CONFIG,get_confg_fields)
    fish_setting = [
            {'name':'wechat_switch','title':'捕鱼商城微信支付开关','value':wechat_switch,'desc':'0-关闭 1-开启'},
            {'name':'share_coin','title':'每日首次分享获得金币数','value':share_coin,'desc':'用户每日第一次分享游戏可以获得的金币'},
            #{'name':'share_datetime','title':'每日分享截止时间','value':conf.get('fish.exchange_shop')}
            {'name':'exchange_shop','title':'捕鱼兑换商城是否开放','value':exchange_shop,'desc':'0-关闭 1-开启'},
            {'name':'hall_shop','title':'捕鱼商城是否开放','value':hall_shop,'desc':'0-关闭 1-开启'},
            {'name':'shop_version','title':'捕鱼商城版本','value':shop_version,'desc':''},
            {'name':'exchange_shop_ver','title':'捕鱼兑换商城版本','value':exchange_shop_ver,'desc':''}
    ]

    info = {
                'title'                  :           lang.SYSTEM_SETTING_TITLE_TXT,
                'settingUrl'             :           BACK_PRE+'/setting/fish/system',
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
    }

    return template('admin_setting_fish_system',info=info,lang=lang,fish_setting=fish_setting,RES_VERSION=RES_VERSION)

@admin_app.post('/setting/fish/system')
@checkLogin
def do_fish_setting(redis,session):
    """
    捕鱼系统参数设置接口
    """
    curTime = datetime.now()
    lang    = getLang()
    fields = ('share_coin','exchange_shop','hall_shop','shop_version','exchange_shop_ver','wechat_switch')
    for field in fields:
        exec('%s = request.forms.get("%s","")'%(field,field))

    try:
        log_debug('[try do_fish_setting] share_coin[%s] exchange_shop[%s]'%(share_coin,exchange_shop))
    except:
        return {'code':-300,'msg':'接口参数错误!'}

    if not share_coin.isdigit():
        return {'code':1,'msg':'分享金币设置数必须为整数'}

    if exchange_shop not in ['0','1',0,1]:
        return {'code':1,'msg':'兑换商城开关的值只能设置为0或1'}

    if hall_shop not in ['0','1',0,1]:
        return {'code':1,'msg':'捕鱼商城开关的值只能设置为0或1'}

    update_info = {
        'share_coin'           :    convert_util.to_int(share_coin),
        'exchange_shop'        :    convert_util.to_int(exchange_shop),
        'hall_shop'            :    convert_util.to_int(hall_shop),
        'shop_version'         :    convert_util.to_int(shop_version),
        'exchange_shop_ver'    :    convert_util.to_int(exchange_shop_ver),
        'wechat_switch'    :    convert_util.to_int(wechat_switch)
    }
    redis.hmset(FISH_CONSTS_CONFIG,update_info)
    return {'code':1,'msg':'更新成功'}

@admin_app.post('/setting/system')
def do_settingSystem(redis,session):
    """
    系统设置页面
    """
    curTime = datetime.now()

    #微信支付开关
    wechatSwitch = request.forms.get('wechatSwitch','').strip()
    gameServerUrl = request.forms.get('gameServerUrl','').strip()

    #print
    log_debug('[%s][settingSystem][info] wechatSwitch[%s]'%(curTime,wechatSwitch))

    pipe = redis.pipeline()
    try:
        if int(wechatSwitch) not in [0,1]:
            return {'code':1,'msg':'微信支付开关值只能为0或1'}
    except:
        wechatSwitch = 1

    try:
        pipe.set(ORDER2WEIXIN_SWITCH,int(wechatSwitch))
        pipe.set(GAME_SERVER_URL,gameServerUrl)
    except Exception,e:
        log_debug('[%s][settingSystem][error] setting error[%s]'%(curTime,e))
        return {'code':0,'msg':'设置配置失败'}

    pipe.execute()
    return {'code':1,'msg':'保存配置成功'}


@admin_app.get('/setting/hotUpDateSetting')
@admin_app.get('/setting/hotUpDateSetting/<action>')
@checkLogin
def getHotUpDataSetting(redis,session,action=None):
    """
    热更新设置配置
    """
    curTime = datetime.now()
    lang    = getLang()
    sys = request.GET.get('sys','').strip()
    if not sys:
        sys = 'HALL'

    if action:
        """ 获取数据接口 """
        action = action.upper()
        if action == "HALL":
            setting_info = getHotSettingAll(redis)
        else:
            setting_info = get_fish_hall_setting(redis)

        return {'setting_info':setting_info}
    else:
        """ 模板渲染 """
        info = {
                'title'                  :       '热更新配置',
                'submitUrl'              :        BACK_PRE+'/setting/hotUpDateSetting/{}'.format(sys),
                'STATIC_LAYUI_PATH'      :        STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :        STATIC_ADMIN_PATH
        }

        return template('admin_hotUpdate_setting',info=info,action=sys,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/setting/hotUpDateSetting')
@admin_app.post('/setting/hotUpDateSetting/<action>')
@checkLogin
def do_HotUpdate(redis,session,action="HALL"):
    """
    热更新配置
    """
    action = action.upper()
    curTime = datetime.now()
    lang = getLang()
    fields = (
                'resVersion','minVersion','iosMinVersion',\
                'downloadURL','IPAURL','apkSize','apkMD5',\
                'hotUpdateURL','hotUpdateScriptsURL','updateAppStore1',\
                'updateAppStore2','updateAndroid','updateYYB','packName'
    )
    for field in fields:
        exec("%s=request.forms.get('%s','').strip()"%(field,field))

    #log_debug
    log_util.debug('[%s][hotUpDateSetting][info] resVersion[%s] minVersion[%s] iosMinVersion[%s] downloadURL[%s]'\
                    %(curTime,resVersion,minVersion,iosMinVersion,downloadURL))

    checkNullField = [
            {'field':resVersion,'msg':'resVersion不能为空'},
            {'field':minVersion,'msg':'minVersion不能为空'},
            {'field':iosMinVersion,'msg':'iosMinVersion不能为空'},
            {'field':downloadURL,'msg':'downloadURL不能为空'},
            {'field':IPAURL,'msg':'IPAURL不能为空'},
            {'field':hotUpdateURL,'msg':'hotUpdateURL不能为空'},
            {'field':hotUpdateScriptsURL,'msg':'hotUpdateScriptsURL不能为空'}
    ]

    for check in checkNullField:
        if not check['field']:
            return {'code':1,'msg':check['msg']}

    updateHostSettingInfo = {
                'resVersion'        :       resVersion,
                'minVersion'        :       minVersion,
                'iosMinVersion'     :       iosMinVersion,
                'downloadURL'       :       downloadURL,
                'IPAURL'            :       IPAURL,
                'apkSize'           :       apkSize,
                'hotUpdateURL'      :       hotUpdateURL,
                'hotUpdateScriptsURL'   :   hotUpdateScriptsURL,
                'updateAppStore1'    :       updateAppStore1,
                'updateAppStore2'    :       updateAppStore2,
                'updateAndroid'     :       updateAndroid,
                'updateYYB'         :       updateYYB,
                'packName'          :       packName,
                'lastUpTime'        :       curTime.strftime('%Y-%m-%d %H:%M:%S')
    }

    try:
        saveHotUpDateSetting(redis,updateHostSettingInfo,action)
    except:
        log_debug('[%s][hotUpDateSetting][error] hotUpdateError reason[%s]'%(curTime,e))

    return {'code':0,'msg':'保存配置成功','jumpUrl':BACK_PRE+'/setting/hotUpDateSetting?sys={}'.format(action)}
