#!/usr/bin/env python
 #-*-coding:utf-8 -*-

"""
    @Author: $Author$
    @Date: $Date$
    @version: $Revision$

    Description:
    捕鱼接口常量配置
"""
from config import config
##################################################
# 数据分页
##################################################
NUMS_PER_PAGE = 30 # 每一页数据数

###########################################################################
# 更新相关
###########################################################################
FISH_HALL_2_VERS = {
    "resVersion"            :   '1',
    "minVersion"            :   '1.0.1',
    "iosMinVersion"         :   '1.0.1',
    "downloadURL"           :   config.API_ROOT+"/download/hall/hall.apk",
    "IPAURL"                :   "",
    "apkSize"               :   22307533, #字节
    "apkMD5"                :   "67BD3A586E608AF76075F458AFB8056F",
    "hotUpdateURL"          :   config.API_ROOT+"/download/hall/hall.zip",
    "hotUpdateScriptsURL"   :   config.API_ROOT+"/download/hall/script.zip",
    "updateAndroid"         :   1,
    "updateYYB"             :   1,
    "updateAppStore1"       :   False,
    "updateAppStore2"       :   True,
    'packName'              :   'hall.zip'
}

###########################################################################
# 邀请相关
###########################################################################

FISH_INVITE_LINKS = {
     'scheme_android'        :       'dsby://com.dsby',
     'scheme_ios'            :       'com.dsby://invite',
     'download_ios'          :        FISH_HALL_2_VERS['IPAURL'],
     'download_android'      :       'https://fir.im/7d41',
     'btn_open_res'          :       "/assest/default/image/invite/fish_entry.png",
     'btn_down_res'          :       "/assest/default/image/invite/fish_down.png",
     'invite_bg_res'         :       "/assest/default/image/invite/bg_fish.png"
}


FORMAT_PARAMS_POST_STR = "%s = request.forms.get('%s','').strip()"
FORMAT_PARAMS_GET_STR  = "%s = request.GET.get('%s','').strip()"

###########################################################################
# 商城常量配置
###########################################################################
REWARD_ONLINE  = 1
REWARD_OFFLINE = 0

REAL_EXCHANGE  = 0   #实物兑换
CARD_EXCHANGE  = 1   #兑换卡密
COIN_EXCHANGE  = 2   #兑换金币
GOODS_EXCHANGE = 3   #兑换卡密
PHONE_EXCHANGE  = 4   #兑换金币

###########################################################################
# 登录道具常量
###########################################################################
GIVE_COIN_FIRST_LOGIN = 1500 #初次登录捕鱼赠送的金币
GIVE_COIN_DAY_LOGIN = 100000 #每日登录赠送金币
GIVE_LOCK_COUNT_DAY_LOGIN = 30 #每天赠送锁定道具个数
GIVE_LOCK_COUNT_DAY_LOGIN_MAX = 99 #每天赠送锁定道具最大个数
