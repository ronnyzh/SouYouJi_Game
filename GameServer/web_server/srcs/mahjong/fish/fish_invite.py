#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    捕鱼邀请接口相关
"""
from bottle import request,response,template,default_app
from fish import fish_app
from datetime import datetime
from model.hallModel import get_fish_hall_setting
from common.utilt import allow_cross,getInfoBySid
from common import log_util,web_util
from fish_config import consts


@fish_app.get('/invite')
@allow_cross
def get_invite_page(redis,session):
    """
    捕鱼邀请页面链接
    """
    ip = web_util.get_ip()
    rid = request.GET.get('rid','').strip()

    HALL2VERS = get_fish_hall_setting(redis)
    log_util.debug('[try get_fish_invite_path] requestIp[%s] rid[%s] versionInfo[%s]'%(ip,rid,HALL2VERS))

    info = {
            'entry_title'           :           '搜集游棋牌捕鱼',
            'scheme_ios'            :           consts.FISH_INVITE_LINKS['scheme_ios'],
            'scheme_android'        :           consts.FISH_INVITE_LINKS['scheme_android'],
            'ios_download'          :           consts.FISH_INVITE_LINKS['download_android'],
            'android_download'      :           consts.FISH_INVITE_LINKS['download_android'],
            'btn_open_res'          :           consts.FISH_INVITE_LINKS['btn_open_res'],
            'btn_down_res'          :           consts.FISH_INVITE_LINKS['btn_down_res'],
            'invite_bg_res'         :           consts.FISH_INVITE_LINKS['invite_bg_res'],
            'ifr_src'               :           '',
            'timeout'               :           1000,
    }

    response.add_header("Expires", 0);
    response.add_header( "Cache-Control", "no-cache" );
    response.add_header( "Cache-Control", "no-store" );
    response.add_header( "Cache-Control", "must-revalidate" );
    #是否限制IP
    return template('invite',info=info)
