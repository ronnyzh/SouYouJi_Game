# -*- coding:utf-8 -*-
# !/usr/bin/python

"""
     比赛场模型
"""

"""
    单项配置
    id 该项标识
    type 赛事类型 0 人满即开
    title 标题
    openStart 开放日期
    openEnd 结束日期
    timeStart 开始时间
    timeEnd 结束时间
    waitTime 倒计时 秒数
    status 0 未开始 1 倒计时 2 已经开始 3 结束
    timeSpacing 场间间隔 秒数
    general 概况
    rewardList 奖品列表
    rule 规则
    num 当前人数
    fee 报名费
    feetype 报名方式 
    gameid 游戏ID
    play_num 玩家基数
    baseScore 底分
 """
DetailConfig = {
    "id": "5",
    "type": 0,
    "title": "100钻石赛",
    "openStart": "2017-07-30",
    "openEnd": "2018-07-30",
    "timeStart": "10:00",
    "timeEnd": "19:00",
    "waitTime": 60 * 3,
    "status": 0,
    "timeSpacing": 60 * 5,
    "feetype": "gold",
    "fee": 1000,
    "play_num": 4,
    "general": [
        {"field": "赛事名称", "value": "100钻石赛"},
        {"field": "玩家基数", "value": 4},
        {"field": "游戏id", "value": 600},
        {"field": "游戏名", "value": "明牌牛牛"},
        {"field": "开启周期", "value": "10:00-19:00"},
        {"field": "报名费用", "value": "5个钻石"},
        {"field": "赛事玩法", "value": "牛七*2,牛八*3"},
    ],
    "rewardList": [
        {"ids": [1, ], "field": "冠军", "value": 2, "type": "redpacket"},
        {"ids": [2, ], "field": "亚军", "value": 10000, "type": "gold"},
        {"ids": [3, ], "field": "季军", "value": 8000, "type": "gold"},
        {"ids": [4, ], "field": "第4名", "value": 6000, "type": "gold"},
        {"ids": [5, 8], "field": "第5-8名", "value": 4000, "type": "gold"},
        {"ids": [9, 16], "field": "第9-16名", "value": 2000, "type": "gold"},
        {"ids": [17, 32], "field": "第17-32名", "value": 1000, "type": "gold"},
    ],
    "rule": "",
    "num": 0,
    "gameid": 600,
    "baseScore": 50,
}

"""
    后台增加比赛场配置
    比赛名称 title
    比赛类型 type 0 --- 即开 1 定时 默认即开
    比赛玩法 gameid 600 - 二人牛牛 450 - 二人麻将
    报名条件 feetype : gold , roomCard, yuanbao 金币 、钻石、 元宝
            fee : 值
    比赛人数: play_num 8 16 32 64 128 512
    比赛赛制 rule_type: 0 淘汰制
    规则: rule 
    奖励 
    rewardList
        第1名：XXX
        第2名：XXX、
        ...
        第5-8名：XXX
"""

"""
    list ----- DetailConfig 作为元素
"""

DATA = [
        {"rule_type": 0,
         "fee": 12,
         "feetype": "yuanbao",
         "need": [12],
         "num": 0,
         "title": "跑得快红包场",
         "gameName": "跑得快红包赛",
         "rule": """游戏介绍：
            跑得快是一款传统的纸牌游戏，多人游玩，趣味十足。


            基本规则：
            *【 人  数 】：3人；
            *【 模  式 】：经典玩法，16张玩法；
            *【 牌  数 】：经典游戏，牌数为每人16张；
            *【牌内容】：经典玩法为一副牌去掉大小王，1张A,3张2，剩余共48张；
             【 出  牌 】：每局持有方块3者先出（首出牌可不含3），各为一家，每人独立算分，没有搭档，上家打完下家跟着出牌（逆时针）；
            【 胜  利 】：每位游戏者都要想方设法将自己手中的牌尽快打出去。谁先打完所有的牌，即为胜方；
            【 报  单 】：当下家报单时，如果选择出单张，必须为手牌中最大的牌，其他牌不可打，最大牌有多张时，可任选其中之一张打出；
            【有打必打】：打得起时必须打，不能选择过；
            【对应打牌】：例如三带一不能打三带二，三带二不能打三带一。即对方打出的牌型，只能用相应的牌型打它。


            基本牌型：

            【 单  张 】：即单牌，2>A>K>Q>J>10>9>8>7>6>5>4>3；
            【 对  子 】：两张点数一样的牌组成的牌型；
            【 连  对 】：两对或两对以上点数相连的牌组成的牌型；
            【 顺  子 】：五张或更多的连续单牌，可以从3连到A。如：910JQKA（2不能出现在顺子）。
            【 三带二 】：点数相同的3张牌 + 1对子/2张不同的单牌；
            【 三带一 】：点数相同的3张牌 + 1张单牌，但只能在最后剩4张的时候出；
            【 三  张 】：点数相同的3张牌，但只能在最后剩3张的时候出；
            【 飞  机 】：两套或多套连续相邻点数的三带二（或三带一）即为飞机，牌不够时可为连续点数相同的三张；
            【 炸  弹 】：四张点数一样的牌组成的牌型，炸弹可以打任何牌，只有比他点数大的炸弹才能打炸弹。牌局中每出一次炸弹最后的结算分数翻一次番。


            牌型的大小：

            本游戏的牌点由大到小排列为： 2、A、K、Q、J、10、9、8、7、6、5、4、3，不分花色；
            炸弹比其他牌大。都是炸弹时按牌的分值比大小；
            对牌、三张牌都按分值比大小；
            顺牌按最大的一张牌的分值来比大小；
            飞机带翅膀和四带三按其中的三顺和四张部分来比，带的牌不影响大小。


            胜负判定：

            任意一家出完牌后结束游戏，先出完牌者胜，其他两家负。
            """,
         "rewardList": [
             {"ids": [1, ], "field": "每三场必得红包", "value": '', "type": "redpacket"},
         ],
         "gameid": 1008,
         "baseScore": 50,
         "play_num": 3,
         "general": [
             {"field": "场次名称", "value": "三局红包赛"},
             {"field": "每局房费", "value": '1元宝'},
             {"field": "入场门槛", "value": '12元宝'},
         ],
         "type": 2,
         "id": "999999",
         "name": "红包场",
         },
    ]

MatchConfig = [
    {"type": 0, "name": "坐满即玩", "list": [], "online_num": 0},
    {"type": 1, "name": "定时赛场", "list": [], "online_num": 0},
    {"type": 2, "name": "红包场", "list": DATA, "online_num": 0},

]

EnclosureList = {
    '0': 'roomCard',
    '1': 'gamePoint',
}

FeeTypeList = {
    'roomCard': '钻石',
    'gamePoint': '积分',
}

MatchTypeList = {
    '0': '即时开启'
}

"""
    比赛配置
"""
MATCH_SETTING = "match:id:%s:setting:key"

"""
    配置自增值
"""
MATCH_COUNT = "match:ids:count"

"""
    比赛场集合
"""
MATCH_SET = "match:game:ids:set"


""" 报名玩家并进入房间集合
    通过该key来判断玩家是否在房间中
    如果是在房间中大退重进大厅后，弹窗提示玩家进入房间
"""
MATCH_ENTER_ROOM_PLAYER_SET = "match:id:%s:enter:room:account:set"

""" 
    比赛场名次
    match:rank:matchid:timestamp:zset
"""
MATCH_RANK_BY_MATCHID = "match:rank:%s:zset"

"""
    比赛场游戏ID集合
"""
MATCH_GAMEID_SET = "ismatch:gameid:set"

"""
等待加入比赛场集合
'match:wait:accounts:id:%s:set'
"""
MATCH_WAITTING_PLAYER_SET = 'match:wait:accounts:id:%s:set'

"""
    已经加入比赛场集合
    已经在游戏中的玩家集合
"""
MATCH_ENTER_PLAYER_SET = "match:enter:accounts:id:%s:set"

"""
    同一个match不能场次不能进同一个game进程
    当前已经游戏进行中不能开放给玩家的游戏服务集合
"""
MATCH_GAMING_GAME_SERVICE_SET = "match:gaming:game:%s:set"

"""
    处于等待中的游戏服务
"""
MATCH_WAITING_GAME_SERVIVE_KEY = "match:waiting:game:%s:key"

"""
    比赛场在线集合
"""
MATCH_ONLINE_ACCOUNTS_BY_TYPE_SET = "match:online:accounts:type:%s:set"


"""
    玩家在比赛场免费次数
    按天
    match:free:times:比赛ID:account:date
"""

MATCH_ACCOUNT_FREE_TIMES = "match:free:times:%s:%s:%s"

MATCH_FIELDS = [
    "match_reward_rank1 = request.forms.get('match_reward_rank1', '').strip()",
    "match_reward_appellation1 = request.forms.get('match_reward_appellation1', '').strip()",
    "match_reward_type1 = request.forms.get('match_reward_type1', '').strip()",
    "match_reward_fee1 = request.forms.get('match_reward_fee1', '').strip()",

    "match_reward_rank2 = request.forms.get('match_reward_rank2', '').strip()",
    "match_reward_appellation2 = request.forms.get('match_reward_appellation2', '').strip()",
    "match_reward_type2 = request.forms.get('match_reward_type2', '').strip()",
    "match_reward_fee2 = request.forms.get('match_reward_fee2', '').strip()",

    "match_reward_rank3 = request.forms.get('match_reward_rank3', '').strip()",
    "match_reward_appellation3 = request.forms.get('match_reward_appellation3', '').strip()",
    "match_reward_type3 = request.forms.get('match_reward_type3', '').strip()",
    "match_reward_fee3 = request.forms.get('match_reward_fee3', '').strip()",

    "match_reward_rank4 = request.forms.get('match_reward_rank4', '').strip()",
    "match_reward_appellation4 = request.forms.get('match_reward_appellation4', '').strip()",
    "match_reward_type4 = request.forms.get('match_reward_type4', '').strip()",
    "match_reward_fee4 = request.forms.get('match_reward_fee4', '').strip()",
]

def get_match_list(redis):
    """
        获取比赛场列表
    """
    res = []

    match_set = sorted(redis.smembers(MATCH_SET),key=lambda x:int(x.split(':')[2]))

    for key in match_set:
        matchid = key.split(":")[2]
        info = get_match_info(redis, matchid)
        if not info:
            continue
        ret = {
            "type": info["type"],
            "title": info["title"],
            "id": info["id"],
            "gameid": info["gameid"],
            "timeStart":info.get("timeStart",''),
            "play_num":info["play_num"],
            "play_num_lower":info.get("play_num_lower",'无'),
        }
        ret['op'] = [
            {'url':'/admin/match/modify', 'txt':'修改', 'method':'POST'},
            {'url':'/admin/match/del', 'txt':'删除', 'method':'POST'},
        ]
        res.append(ret)

    return res


import json
from datetime import datetime
import calendar

def get_match_info(redis, matchid):
    """ 
        获取比赛配置信息
    """
    key = MATCH_SETTING % matchid
    if not redis.sismember(MATCH_SET, key):
        return
    if not redis.exists(key):
        return
    return json.loads(redis.get(key))

from bottle_mysql import get_mysql

def get_2MJ_log_list(redis,startDate,endDate,gameid):
    reward_dict = {'reward_gold':'金币', 'reward_roomCard':'钻石', 'reward_yuanbao':'元宝', 'reward_redpacket':'红包'}
    total_dict = {'total_gold':'金币', 'total_roomCard':'钻石', 'total_yuanbao':'元宝', 'total_redpacket':'红包'}

    sql = get_mysql()
    if startDate and endDate:
        startDate = datetime.strptime(startDate, "%Y-%m-%d")
        year,mon,day = [int(s) for s in endDate.split('-')]
        if int(day) != calendar.monthrange(year,mon):
            day += 1
        else:
            mon += 1
            day = 1
        endDate = '%s-%s-%s'%(year,mon,day)
        endDate = datetime.strptime(endDate, "%Y-%m-%d")
        sql_str = 'select * from MatchLog where StartTime >= "%s" and EndTime <= "%s"' % (startDate, endDate)
        if gameid:
            sql_str += ' and GameId = "%s"'%(gameid)
        result, answers = sql.select_data_bywhere(sql_str)
    else:
        if gameid:
            pass
            result, answers = sql.select_data('MatchLog', '*', {'gameid':gameid})
        else:
            pass
            result, answers = sql.select_data('MatchLog', '*')
    sql.close_connect()
    if result and answers:
        answers.reverse()
        for _answer in answers:
            _answer['total_reward'] = []
            _answer['total_Rankings'] = []
            _answer['total_all'] = []
            for _key,_value in reward_dict.iteritems():
                if _answer[_key]:
                    _answer['total_reward'].append('%sX%s\n'%(_value,_answer[_key]))
            for _val in _answer['Rankings'].split('|'):
                _answer['total_Rankings'].append(_val)
            for _key,_value in total_dict.iteritems():
                if _answer[_key] or True:
                    _answer['total_all'].append('%sX%s\n'%(_value,_answer[_key]))
        return answers
    return []


