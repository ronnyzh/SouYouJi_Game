#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    后台配置文件
"""
#[resorce version]
RES_VERSION = 4.0

#[role]
SYSTEM_ADMIN = 0
systemId = 1

PROVINCE_AGENT  = 1
#配置文件
CONF_FILE = 'conf_release.json'
#[consts config]
API_ROOT           =           'http://192.168.0.99:9797'
BACK_PRE           =           '/admin'
TEMPLATE_NAME      =           'default'
TEMPLATE_PATH      =           'mahjong/template/%s'%(TEMPLATE_NAME)

#[path config]
DOWNLOAD_PATH             =            'mahjong/static/download/'
STATIC_PATH               =            'mahjong/static/'
STATIC_ADMIN_PATH         =            '/assest/default'
STATIC_LAYUI_PATH         =            '/assest/common/layui'

'''
======================================================== 后台上传/下载参数配置
'''
#允许上传的文件格式
FILES_ALLOW_EXTS = ['.jpg','.png','.gif']
#奖品文件上传路劲
FILES_REWARD_UPLOAD_PATH = 'mahjong/static/assest/default/image/reward'
#[game Pack Address]
GAME_DOWNLOAD_URL = 'http://119.23.203.197:9798/download/games/%s'
'''
======================================================== 后台下载参数配置 结束
'''


HALL_PICK_ROUTES = {
    'CN'        :   ("45.127.184.2",),
    #'CN'        :   ("192.168.0.99","192.168.0.168"),
    'DEFAULT'   :   ("45.127.184.2",),
    'TW'        :   ("45.127.184.2",),
    'HK'        :   ("45.127.184.2",),
    'MY'        :   ("45.127.184.2",),
    'SG'        :   ("45.127.184.2",),
    'ID'        :   ("45.127.184.2",),
    'PH'        :   ("45.127.184.2",),
    'JP'        :   ("45.127.184.2",),
    'KR'        :   ("45.127.184.2",),
    'US'        :   ("45.127.184.2",),
    'RU'        :   ("45.127.184.2",),
}

#[基本分配置]
PLAYER_BASE_SCORE  =  [
    {'name':'score1','score':1},
    {'name':'score2','score':2},
    {'name':'score3','score':3},
    {'name':'score4','score':4},
    {'name':'score5','score':5},
    {'name':'score6','score':6},
    {'name':'score7','score':7},
    {'name':'score8','score':8},
    {'name':'score9','score':9},
    {'name':'score10','score':10},
    {'name':'score11','score':11},
    {'name':'score12','score':12},
    {'name':'score13','score':13},
    {'name':'score14','score':14},
    {'name':'score15','score':15},
    {'name':'score16','score':16},
    {'name':'score17','score':17},
    {'name':'score18','score':18},
    {'name':'score19','score':19},
    {'name':'score2','score':20}
]
DEFAULT_BASE_SCORE = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
#[party roomPlayerSetting]
PARTY_PLAYER_COUNT = 4
#大厅VERSION
HALL2VERS = {
        "resVersion"            :   '1',
        "minVersion"            :   '1.0.1',
        "iosMinVersion"         :   '1.0.1',
        "downloadURL"           :   API_ROOT+"/download/hall/hall.apk",
        "IPAURL"                :   "",
        "apkSize"               :   22307533, #字节
        "apkMD5"                :   "67BD3A586E608AF76075F458AFB8056F",
        "hotUpdateURL"          :   API_ROOT+"/download/hall/hall.zip",
        "hotUpdateScriptsURL"   :   API_ROOT+"/download/hall/script.zip",
        "updateAndroid"         :   1,
        "updateYYB"             :   1,
        "updateAppStore1"       :   False,
        "updateAppStore2"       :   True,
        'packName'              :   'hall.zip'
}
###########################################################################
# 广播常量配置
###########################################################################
BROAD_TYPE_2_TITLE = {
        '0'         :       '【系统广播】',
        '1'         :       '【系统广播】',
        '2'         :       '【地区广播】',
        '3'         :       '【地区广播】'
}

###########################################################################
# 商城常量配置
###########################################################################
REWARD_ONLINE  = 1
REWARD_OFFLINE = 0
'''
======================================================== 前端控制参数配置
'''
#前端分页配置
PAGE_LIST = [15,50,100]
FONT_CONFIG = {
        'PAGE_LIST'         :       [15,50,100], #前端可选分页
        'STR_2_SORT'        :       {'asc':False,'desc':True}, #排序
}
'''
======================================================== 前端控制参数配置s 结束
'''
##################################################################################
### 邮件服务参数 ###
# 邮件服务器
SMTP = 'smtp.qq.com'
# 邮件服务器端口
SMTP_PORT = 465
# email发送账号
EMAIL_USER = '514303208@qq.com'
# email发送密码
EMAIL_PWD = 'cwkahrftixtfbied'
# 系统异常邮件通知地址，多个地址用逗号分隔
EMAIL_LIST = '514303208@qq.com'
# 异常邮件通知标题
# ——由于我们有开发环境、测试环境、预生产环境、生产环境等多个不同的环境，
# ——所以在发送异常通知时如果区分的话，可能就弄不清是那个环境出了问题，
# ——我们可以通过设置邮件标题为：开发、测试、预生产、生产等标签来方便区分是那个环境发送的异常通知
EMAIL_ERR_TITLE = '系统异常通知-ds_admin-系统'
# 活动
STATIC_ACTIVICE_PATH        =   '/assest/activice'
STATIC_ACTIVICE_DOWNLOAD_PATH = STATIC_ACTIVICE_PATH + '/download'
RESOURCE_ALLOW_TYPES = ['image/gif','image/jpg','image/jpeg','image/pjpeg','image/png'] # 允许上传的资源类型
# 活动设置中，活动类型列表
AC_TYPE_TURNLATE = "turnlate"
AC_TYPE_MESSION = "mission"
AC_TYPE_INVITE = "invite"
AC_TYPE_REDPACK = "redpack"
AC_TYPE_NIUNIU = "niuniu"  #牛牛活动

##################################################################################
### 活动模块参数 ###
ACTIVICE_TYPE_LIST =[
            {
                "field": AC_TYPE_TURNLATE,
                "imgUrl": STATIC_ACTIVICE_PATH + "/admin/type_fengche.jpg",
                "title": "风车",
                "status": 1  # 1：允许点击 0：禁止点击
            },
            {
                "field"     : AC_TYPE_MESSION,
                "imgUrl"    : "http://t.cn/RN9rB0V",
                "title"     : "游戏任务",
                "status"    : 0     # 1：允许点击 0：禁止点击
            },
            {
                "field"     : AC_TYPE_INVITE,
                "imgUrl"    : "http://t.cn/RN9pzPZ",
                "title"     : "邀请任务",
                "status"    : 0     # 1：允许点击 0：禁止点击
            },
            {
                "field"     : AC_TYPE_REDPACK,
                "imgUrl"    : "http://t.cn/RN94pCu",
                "title"     : "红包雨",
                "status"    : 0     # 1：允许点击 0：禁止点击
            },
        ]

# 资源设置中，发放类型列表
# value 是 发放类型， type 是需要填写表单的类型
ACTIVICE_RESOURCE_TYPE_LIST =[
            {"name":"金币",   "value":"coin",     "type":"prop"},
            {"name":"钻石",   "value":"diamonds", "type":"prop"},
            {"name":"抽奖券", "value":"lottery",  "type":"prop"},
            {"name":"礼包",   "value":"pack",     "type":"pack"},
            {"name":"实物",   "value":"goods",    "type":"normal"},
            {"name":"不中奖", "value":"empty",    "type":"prop"}
        ]

# 聚合短信平台
JUHE_APPKEY = '015302a31d0b554ec9c3ae8b9c7e78f2'  # 申请的短信服务appkey
JUHE_TPL_ID = '132950'  # 申请的短信模板ID,根据实际情况修改
JUHE_TPL_VALUE = '#code#=%s&#company#=JuheData' # 短信模板变量,根据实际情况修改
JUHE_TPL_SEND_URL = 'http://v.juhe.cn/sms/send'  # 短信发送的URL,无需修改
JUHE_PARAMS = 'key=%s&mobile=%s&tpl_id=%s&tpl_value=%s' # 组合参数
JUHE_VCODE_TIME = 60