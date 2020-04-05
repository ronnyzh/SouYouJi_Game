# -*- coding:utf-8 -*-
# !/usr/bin/python
from web_db_define import *
from admin  import access_module
from config.config import *
from common.log import *
import random
from datetime import datetime
import os
import json
# from niuniu_db_define import *
# from niuniu_active_db_define import *
#from  serviceModle import send_msg_to_service, get_uuid, MSG_NIUNIU_SHARE, get_result_from_service
import redis
import traceback
import functools
"""
    经典牛牛后台数据接口
"""



"""
    牛牛运营表 & 活动统计表
    niuniu:game:operate:xxx-xxx-xx(年月日):table
    {'date': 日期,
            'player_count': 参与总人数,
            'game_count': 游戏总局数,
            'new_count': 新增用户数,
            'online_count': 当前牛牛在线人数,
            'online_user_max': 牛牛在线人数峰值,
            'download_count': 下载经典牛牛数,
            'create_room': 创建房间数,
            'bull_0': 无牛次数, ... 'bull_9': 牛九次数,
            'bull_10': 牛牛次数
            'bull_11': 五花牛次数
            'bull_12': 四炸次数
            'bull_13': 五小牛次数
            'roomcard_total': 消耗钻石数
            'online_room': 在线房间数

            'draw_last_count': 还有多少次抽奖次数,
            'no_cash_user':  未领取奖励人数,
            'no_cash_total': 未领取奖励金额,
            'get_cash_user':  已领取奖励人数,
            'get_cash_total': 已领取奖励金额,
            'roomcard_total': 总中奖钻石数
            'draw_used' : 已抽奖次数
            
     }
     
     点击开始游戏时 更新 [参与总人数  游戏总局数 新增用户数  当前牛牛在线人数 牛牛在线人数峰值 创建房间数]
     结算时更新牛牛次数
     下载时更新下载次数
     游戏结束时更新在线人数
     
"""
NIUNIU_GAME_OPERATE_BY_DAY_TABLE = "niuniu:game:operate:%s:total:table"

"""
    参与牛牛集合 按天
"""
NIUNIU_ACCOUNT_SET = 'niuniu:game:account:%s:set'

"""
    牛牛在线集合 按天
"""
NIUNIU_ONLINE_ACCOUNT_SET = 'niuniu:game:online:account:%s:set'

"""
    牛牛新增用户 按天
"""
NIUNIU_ACCOUNT_ADD_SET = 'niuniu:game:add:account:%s:set'

"""
    牛牛参与总人数
"""
NIUNIU_ACCOUNT_SET_TOTAL = 'niuniu:game:account:set'

"""
    牛牛记录保存时间
"""
NIUNIU_GAME_ROOM_MAX_TIME = 30 * 24 * 60 *60

"""
    牛牛记录id
    每一小局一次记录
    party:game:record:count
"""
NIUNIU_GAME_RECORD_COUNT_TABLE = "niuniu:game:record:count"

"""
    牛牛记录表
    niuniu:game:record:xxx-xxx-xx(年月日):xx(tableid):table
    {
            'start_time': 开始时间,
            'end_time': 结束时间,
            'action_num': 回放码,
            'score': 分数|分数|||,
            'descs': 描述|描述|,
            'tiles': 牌|牌|,
            'roomid': 房间号,
            'accounts': 账号列表,
            'bull_info': 11|11| 
    }
    小局结算时更新牛牛记录表
"""
NIUNIU_GAME_RECORD_TABLE = "niuniu:game:record:%s:%s:table"

"""
    牛牛玩家记录列表
"""
NIUNIU_GAME_ACCOUNT_RECORD_LIST = 'niuniu:game:record:account:%s:list'

"""
    提现记录表
    niuniu:game:getmoney:account:list
    {
        'date':日期,
        'money':金额,
        'nickname': 昵称
        'account': 账号
        'phone': 手机号
    }

"""
NIUNIU_ACCOUNT_GET_MONEY_LIST = "niuniu:game:getmoney:%s:list"
"""
    当天提现次数
"""
NIUNIU_ACCOUNT_GET_MONEY_COUNT_BY_DAY = "niuniu:game:getmoney:%s:byday:count"

"""
    活动客服查询表
    niuniu:game:stactics:account:table
{
    'uid': ,
    'nickname': 昵称
    'account': 账号
    'phone': 手机
    'share_count': 分享次数
    'niuniu_count': 牛牛次数
    'game_count': 总局数
    'score_total': 总积分
    'draw_times': 剩余抽奖次数,
    'cash_total': 总获得现金,
    'roomcard_total': 总获得钻石数
    'draw_count_used': 已抽奖次数
    ‘cash_get' : 可领取现金
}
    结算时更新 牛牛次数 总局数
"""
NIUNIU_ACCOUNT_STACTICS_TABLE = 'niuniu:game:stactics:%s:table'

"""
    niuniu:game:stactics:account:table
    奖励流水表
    {
        'date': 日期
        'uid': uid,
        'nickname': 昵称
        'account': 账号
        'reward_title': 奖品名称
    }
"""

"""
    牛牛奖励记录id
    party:game:reward:count
"""
NIUNIU_GAME_REWARD_COUNT_TABLE = "niuniu:game:reward:count"

"""
    牛牛用户奖励记录表
    niuniu:game:reward:table
"""
NIUNIU_GAME_REWARD_TABLE = "niuniu:game:reward:table"

"""
    牛牛用户奖励记录列表
    niuniu:game:record:account:list
"""
NIUNIU_GAME_REWARD_LIST = "niuniu:game:reward:%s:list"


def get_niuniu_game_op(redis,date,*params):
    """ 
        获取运营数据
    """
    if redis.exists(NIUNIU_GAME_OPERATE_BY_DAY_TABLE % date):
        res = redis.hmget(NIUNIU_GAME_OPERATE_BY_DAY_TABLE % date, params)
        return tuple(map(int, res))
    return tuple([0] * len(params))


def set_niuniu_game_op(redis,date,data):
    """
        更新运营报表
    """
    redis.hmset(NIUNIU_GAME_OPERATE_BY_DAY_TABLE % date, data)

'statistics/login?list=1&order=asc&limit=24&offset=0' \
'&startDate=2017-10-27&endDate=2017-11-02&_=1509612853655'

#----------------------------------------- 活动 -------------------------------------------------------

PATH_NIUNIU_STATIS = STATIC_ACTIVICE_PATH + "/niuniu"
# 奖品类型
REWARD_TYPE_EMPTY       = "0"  #谢谢参与
REWARD_TYPE_ROOMCARD    = "1"  #钻石
REWARD_TYPE_CASH        = "2"  #现金
REWARD_TYPE_GOODS       = "3"  #实物


"""
    牛牛活动配置表
    {
        'start_date': 开始时间,字符串 
         'end_date': 结束时间,
          'status': 状态， 0 未开启 1 进行中 2 已经结束
    }

"""
NIUNIU_ACTIVI_CONFIG_TABLE = "niuniu:activi:config:table"


def is_niuniu_active_openning(redis):
    """ 
        牛牛活动是否进行中
    """
    if not redis.exists(NIUNIU_ACTIVI_CONFIG_TABLE):
        return False
    info = redis.hgetall(NIUNIU_ACTIVI_CONFIG_TABLE)
    if info.get('status', '') == '1':
        return True
    return False


REWARD_LIST = [
    {
        'id':0,
        'pos':0,
        'title':'10颗钻石',
        'imgUrl':PATH_NIUNIU_STATIS + '/reward_0.png',
        'type':REWARD_TYPE_ROOMCARD,
        'baseCount':10, #奖励个数
    },
    {
        'id':1,
        'pos':1,
        'title':'现金20元',
        'imgUrl': PATH_NIUNIU_STATIS + '/reward_1.png',
        'type':REWARD_TYPE_CASH,
        'baseCount':'', #奖励个数
        'cash': 20,

    },
    {
        'id':2,
        'pos':2,
        'title':'Iphone7P',
        'imgUrl': PATH_NIUNIU_STATIS + '/reward_2.png',
        'type':REWARD_TYPE_GOODS,
        'baseCount':'', #奖励个数
    },
    {
        'id':3,
        'pos':3,
        'title':'现金10元',
        'imgUrl': PATH_NIUNIU_STATIS + '/reward_3.png',
        'type':REWARD_TYPE_CASH,
        'baseCount':'', #奖励个数
        'cash': 10,

    },
    {
        'id':4,
        'pos':4,
        'title':'谢谢参与',
        'imgUrl': PATH_NIUNIU_STATIS + '/reward_4.png',
        'type':REWARD_TYPE_EMPTY,
        'baseCount':'', #奖励个数
    },
    {
        'id':5,
        'pos':5,
        'title':'5颗钻石',
        'imgUrl': PATH_NIUNIU_STATIS + '/reward_5.png',
        'type':REWARD_TYPE_ROOMCARD,
        'baseCount':'5', #奖励个数
    },
    {
        'id':6,
        'pos':6,
        'title':'88元现金',
        'imgUrl': PATH_NIUNIU_STATIS + '/reward_6.png',
        'type':REWARD_TYPE_CASH,
        'baseCount':'', #奖励个数
        'cash' : 88,
    },
]
def getActiviceNiuniuInfo(redis):
    """
        牛牛活动前端信息
    """
    # 奖品
    info = {}
    info['rewards'] = REWARD_LIST;

    #中奖纪录
    reco = [{
        'date' : '日期',
        'reward_title' : '中奖产品',
    }]
    info['journal'] = reco

    #抽奖次数
    info['draw_times'] = 1

    #抽奖地址
    info['submitUrl'] = "/hall/activice/draw?type={0}&times=1".format(AC_TYPE_NIUNIU)
    info['submitUrl_10'] = "/hall/activice/draw?type={0}&times=10".format(AC_TYPE_NIUNIU)

    #可领取现金
    info['cash'] = 0
    info['cashUrl'] =  "/hall/activice/niuniu/cash?type={0}".format(AC_TYPE_NIUNIU)



    log_debug("----牛牛活动前端信息{0}".format(info))
    return {'code': 0, 'msg': '获取活动数据成功', 'data': info}
    # return info

def getActiviceNiuniuList(redis, group_id, request):
    """ 
        获取牛牛活动信息
    """
    # if group_id in TRY_PLAY_GROUPS:
    #     return []
    redis = getPrivateRedisInst(redis, NIUNIU_GAMEID)
    if not _check_active_time(redis, 3):
        return []

    # 海报图片地址
    urlParts = request.urlparts
    rootUrl = "{0}://{1}".format(urlParts.scheme, urlParts.netloc)
    res = [{
        'title': '牛牛活动',
        'type': AC_TYPE_NIUNIU,
        'link': "/hall/activice/route?type={0}".format(AC_TYPE_NIUNIU),
        'posterUrl': rootUrl + STATIC_ACTIVICE_PATH + '/niuniu/turnlate_poster.jpg',
        'iconUrl': rootUrl + STATIC_ACTIVICE_PATH + '/niuniu/turnplate-icon.png'
    }]
    return res

def getActiviceNiuniuDraw(redis,times):

    res = {}

    pos = random.randint(0,6)
    cashCount = 0

    #奖品
    res['rewards'] = []
    draw_time = int(times) if times else 1
    isCrash = False
    for i in range(draw_time):
        single_pos = pos if i == draw_time - 1 else random.randint(0,6)

        info = REWARD_LIST[single_pos]
        res['rewards'].append(info)
        #记录获取现金
        if info['type'] ==REWARD_TYPE_CASH:
            isCrash = True
            cashCount = cashCount + int(info['cash'])

    #位置
    res['pos'] = pos

    #客服微信号
    res['contact'] = "客服微信号：xxxx" if isCrash else ""

    #获得现金
    res['cash'] = cashCount
    return {'code': 0, 'msg': '获取活动数据成功', 'data': res}
    # return res

def getPrivateRedisInst(redisdb, gameid):
    """
        获取redis连接实例
    """
    try:
        if not redisdb.exists(GAME2REDIS % gameid):
            return None
        info = redisdb.hgetall(GAME2REDIS % gameid)
        ip = info['ip']
        passwd = info['passwd']
        port = int(info['port'])
        dbnum = int(info['num'])
        redisdb = redis.ConnectionPool(host=ip, port=port, db=dbnum, password=passwd)
        return redis.Redis(connection_pool=redisdb)
    except:
        traceback.print_exc()
        return None

NIUNIU_GAMEID = '5'

def _check_active_time(redis, day=2):
    if not redis.exists(NIUNIU_ACTIVI_CONFIG_TABLE):
        return False
    cur_date = datetime.now()
    nday = functools.partial(_get_next_day, redis.hget(NIUNIU_ACTIVI_CONFIG_TABLE, 'end_date')[:10])
    if cur_date > nday(day):
        return False
    return True
