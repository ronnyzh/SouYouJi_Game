# -*- coding:utf-8 -*-
# !/usr/bin/python

"""
    金币场 db 
"""

PARTY_TYPE_COMPETITION = '1'
PARTY_TYPE_GOLD = '2'
PARTY_TYPE_MATCH = '3'
PARTY_TYPE_RE = '4'
PARTY_TYPE_HONOR = '2'

"""
    金币场统计数据私人数据库Gameid
"""
MASTER_GAMEID = '555'

"""
    判断金币场匹配是否完成
'IsGoldRoomMatchFinished:%s:str'
"""
IS_GOLD_ROOM_MATCH_FINISHED = 'IsGoldRoomMatchFinished:%s:str'

"""
    等待加入金币场列表
'WaitJoinGoldRoomPlayers:场次编号:gameID:rule:list'
"""
WAIT_JOIN_GOLD_ROOM_PLAYERS = 'WaitJoinGoldRoomPlayers:%s:%s:%s:list'

"""
    账号到所在等待加入各种场表名的映射 ---- 暂时只用金币场
'Account2waitJoinGoldRoomTable:account:str'
"""
ACCOUNT2WAIT_JOIN_GOLD_ROOM_TABLE = 'Account2waitJoinGoldRoomTable:%s:str'

"""
    已经进入金币场游戏中玩家列表
'GameInGoldRoomPlayers:场次编号:gameID:rule:ip:port:list'
"""
ALREADY_IN_GOLD_ROOM_PLAYERS = 'GameInGoldRoomPlayers:%s:%s:%s:%s:%s:list'

"""
    账号到所在已经加入各种场表名的映射
'Account2GameInGoldRoomTable:account:str'
"""
ACCOUNT2ALREADY_IN_JOIN_GOLD_ROOM_TABLE = 'Account2GameInGoldRoomTable:%s:str'

"""
    金币场服务协议
"""
FORMAT_GOLD_SERVICE_PROTOCOL_TABLE = "goldservice:protocols"
FORMAT_GOLD_SERVICE_STATUS = "goldservice:status"

"""
    协议结果返回 
    goldservice:result:uuid
"""
RESULT_GOLD_SERVICE_PROTOCOL = "goldservice:result:%s"

"""
金币增加记录
user:$userID:list:[
{'source':'金币来源','date':'%Y-%m-%d %H:%M:%S','account':'','coinChange':'','coinTotal':''}
]
"""
RECORD4USER_COIN = "welfare:coin:record:user:%s:list"
"""
签到
welfare:sign:user:[account]:[date]:key
"""
WELFARE_USER_SIGN = "welfare:sign:user:%s:%s:key"

"""
补签
welfare:patch:sign:user:[account]:[month]:key
"""
WELFARE_USER_PATCH_SIGN = "welfare:patch:sign:user:%s:%s:set"

"""
低保
welfare:insurance:user:[account]:[date]:list
"""
WELFARE_USER_INSURANCE = "welfare:insurance:user:%s:%s:list"

"""
登陆获取门票
welfare:ticket:user:[account]:[date]:key
"""
WELFARE_USER_TICKET = "welfare:ticket:user:%s:%s:key"

"""
        金币场场次排序
"""
PARTY_GOLD_GAME_LIST_SORT = [
    # "555",
    # "556",
    # "666",
    "444",
    # "557",
    "445",
    # "446",
    # "447",
    # "448",
    "559",
]
"""
        金币场场次配置
"""
PARTY_GOLD_GAME_LIST = {
    'default': [
        {'id': 0, 'title': '新手场', 'need': [1000, 50000], 'baseScore': 400, 'cost': 150, 'maxMultiples': '2048倍'},
        {'id': 1, 'title': '普通场', 'need': [2500, 150000], 'baseScore': 800, 'cost': 280, 'maxMultiples': '2048倍'},
        {'id': 2, 'title': '中级场', 'need': [5000, 500000], 'baseScore': 2000, 'cost': 480, 'maxMultiples': '2048倍'},
        {'id': 3, 'title': '高级场', 'need': [10000], 'baseScore': 4000, 'cost': 800, 'maxMultiples': '2048倍'},
        {'id': 4, 'title': '土豪场', 'need': [20000], 'baseScore': 8000, 'cost': 2400, 'maxMultiples': '2048倍'},
        {'id': 5, 'title': '至尊场', 'need': [40000], 'baseScore': 15000, 'cost': 5000, 'maxMultiples': '2048倍'}
    ],
    '556': [
        {'id': 0, 'title': '新手场', 'need': [1000, 50000], 'baseScore': 25, 'cost': 160, 'maxMultiples': '2048倍'},
        {'id': 1, 'title': '普通场', 'need': [1500, 150000], 'baseScore': 50, 'cost': 240, 'maxMultiples': '2048倍'},
        {'id': 2, 'title': '中级场', 'need': [2500, 500000], 'baseScore': 100, 'cost': 360, 'maxMultiples': '2048倍'},
        {'id': 3, 'title': '高级场', 'need': [5000], 'baseScore': 300, 'cost': 900, 'maxMultiples': '2048倍'},
        {'id': 4, 'title': '土豪场', 'need': [25000], 'baseScore': 1000, 'cost': 2400, 'maxMultiples': '2048倍'},
        {'id': 5, 'title': '至尊场', 'need': [125000], 'baseScore': 5000, 'cost': 10000, 'maxMultiples': '2048倍'}
    ],
    '666': [
        {'id': 0, 'title': '新手场', 'need': [1000, 50000], 'baseScore': 10, 'cost': 100, 'maxMultiples': '2048倍'},
        {'id': 1, 'title': '普通场', 'need': [10000, 150000], 'baseScore': 100, 'cost': 1000, 'maxMultiples': '2048倍'},
        {'id': 2, 'title': '中级场', 'need': [20000, 500000], 'baseScore': 200, 'cost': 2000, 'maxMultiples': '2048倍'},
        {'id': 3, 'title': '高级场', 'need': [50000], 'baseScore': 1000, 'cost': 5000, 'maxMultiples': '2048倍'},
        {'id': 4, 'title': '土豪场', 'need': [100000], 'baseScore': 5000, 'cost': 10000, 'maxMultiples': '2048倍'},
        {'id': 5, 'title': '至尊场', 'need': [150000], 'baseScore': 10000, 'cost': 15000, 'maxMultiples': '2048倍'}
    ],
    '444': [
        {'id': 0, 'title': '新手场', 'need': [2000, 150000], 'baseScore': 500, 'cost': 100, 'maxMultiples': '2048倍'},
        {'id': 1, 'title': '普通场', 'need': [20000, 750000], 'baseScore': 1500, 'cost': 300, 'maxMultiples': '2048倍'},
        {'id': 2, 'title': '中级场', 'need': [30000, 1800000], 'baseScore': 3000, 'cost': 600, 'maxMultiples': '2048倍'},
        {'id': 3, 'title': '高级场', 'need': [80000], 'baseScore': 10000, 'cost': 3000, 'maxMultiples': '2048倍'},
        {'id': 4, 'title': '土豪场', 'need': [200000], 'baseScore': 20000, 'cost': 7000, 'maxMultiples': '2048倍'},
        {'id': 5, 'title': '至尊场', 'need': [600000], 'baseScore': 72000, 'cost': 14400, 'maxMultiples': '2048倍'}
    ],
    '445': [
        {'id': 0, 'title': '新手场', 'need': [2000, 150000], 'baseScore': 500, 'cost': 100, 'maxMultiples': '2048倍'},
        {'id': 1, 'title': '普通场', 'need': [20000, 750000], 'baseScore': 1500, 'cost': 300, 'maxMultiples': '2048倍'},
        {'id': 2, 'title': '中级场', 'need': [30000, 1800000], 'baseScore': 3000, 'cost': 600, 'maxMultiples': '2048倍'},
        {'id': 3, 'title': '高级场', 'need': [80000], 'baseScore': 10000, 'cost': 3000, 'maxMultiples': '2048倍'},
        {'id': 4, 'title': '土豪场', 'need': [200000], 'baseScore': 20000, 'cost': 7000, 'maxMultiples': '2048倍'},
        {'id': 5, 'title': '至尊场', 'need': [600000], 'baseScore': 72000, 'cost': 14400, 'maxMultiples': '2048倍'}
    ],
    '557': [
        {'id': 0, 'title': '新手场', 'need': [1000], 'baseScore': 50, 'cost': 150, 'maxMultiples': '2048倍'},
        {'id': 1, 'title': '普通场', 'need': [10000], 'baseScore': 200, 'cost': 500, 'maxMultiples': '2048倍'},
        {'id': 2, 'title': '中级场', 'need': [100000], 'baseScore': 1000, 'cost': 2000, 'maxMultiples': '2048倍'},
        {'id': 3, 'title': '高级场', 'need': [1000000], 'baseScore': 2500, 'cost': 8000, 'maxMultiples': '2048倍'},
        {'id': 4, 'title': '土豪场', 'need': [3000000], 'baseScore': 5000, 'cost': 20000, 'maxMultiples': '2048倍'},
    ],
    # 跑得快
    '559': [
        {'id': 0, 'title': '新手场', 'need': [1000, 250000], 'baseScore': 50, 'cost': 200, 'maxMultiples': '2048倍'},
        {'id': 1, 'title': '普通场', 'need': [30000, 1000000], 'baseScore': 250, 'cost': 1000, 'maxMultiples': '2048倍'},
        {'id': 2, 'title': '中级场', 'need': [50000, 3000000], 'baseScore': 500, 'cost': 2000, 'maxMultiples': '2048倍'},
        {'id': 3, 'title': '高级场', 'need': [70000], 'baseScore': 1000, 'cost': 4000, 'maxMultiples': '2048倍'},
        {'id': 4, 'title': '土豪场', 'need': [120000], 'baseScore': 2000, 'cost': 8000, 'maxMultiples': '2048倍'},
    ],
    # 斗地主
    '560': [
        {'id': 0, 'title': '新手场', 'need': [1000, 100000], 'baseScore': 200, 'cost': 50, 'maxMultiples': '2048倍'},
        {'id': 1, 'title': '初级场', 'need': [2000, 300000], 'baseScore': 500, 'cost': 150, 'maxMultiples': '2048倍'},
        {'id': 2, 'title': '中级场', 'need': [5000, 1500000], 'baseScore': 1200, 'cost': 300, 'maxMultiples': '2048倍'},
        {'id': 3, 'title': '高级场', 'need': [20000], 'baseScore': 3000, 'cost': 1000, 'maxMultiples': '2048倍'},
        {'id': 4, 'title': '土豪场', 'need': [50000], 'baseScore': 8000, 'cost': 2000, 'maxMultiples': '2048倍'},
        {'id': 5, 'title': '王者场', 'need': [100000], 'baseScore': 20000, 'cost': 5000, 'maxMultiples': '2048倍'}
    ],
    # 余干
    '446': [
        {'id': 0, 'title': '新手场', 'need': [2000, 150000], 'baseScore': 200, 'cost': 600, 'maxMultiples': '2048倍'},
        {'id': 1, 'title': '普通场', 'need': [20000, 750000], 'baseScore': 600, 'cost': 1500, 'maxMultiples': '2048倍'},
        {'id': 2, 'title': '中级场', 'need': [30000], 'baseScore': 1200, 'cost': 4000, 'maxMultiples': '2048倍'},
        {'id': 3, 'title': '高级场', 'need': [80000], 'baseScore': 4000, 'cost': 8000, 'maxMultiples': '2048倍'},
        {'id': 4, 'title': '土豪场', 'need': [200000], 'baseScore': 8000, 'cost': 16000, 'maxMultiples': '2048倍'},
        {'id': 5, 'title': '至尊场', 'need': [600000], 'baseScore': 20000, 'cost': 30000, 'maxMultiples': '2048倍'}
    ],
    # 南昌
    '447': [
        {'id': 0, 'title': '新手场', 'need': [2000, 150000], 'baseScore': 100, 'cost': 500, 'maxMultiples': '2048倍'},
        {'id': 1, 'title': '普通场', 'need': [20000, 750000], 'baseScore': 300, 'cost': 1500, 'maxMultiples': '2048倍'},
        {'id': 2, 'title': '中级场', 'need': [30000], 'baseScore': 600, 'cost': 4000, 'maxMultiples': '2048倍'},
        {'id': 3, 'title': '高级场', 'need': [80000], 'baseScore': 1800, 'cost': 8000, 'maxMultiples': '2048倍'},
        {'id': 4, 'title': '土豪场', 'need': [200000], 'baseScore': 3600, 'cost': 16000, 'maxMultiples': '2048倍'},
        {'id': 5, 'title': '至尊场', 'need': [600000], 'baseScore': 12000, 'cost': 30000, 'maxMultiples': '2048倍'}
    ],
    # 抚州
    '448': [
        {'id': 0, 'title': '新手场', 'need': [2000, 150000], 'baseScore': 500, 'cost': 250, 'maxMultiples': '2048倍'},
        {'id': 1, 'title': '普通场', 'need': [20000, 750000], 'baseScore': 1500, 'cost': 750, 'maxMultiples': '2048倍'},
        {'id': 2, 'title': '中级场', 'need': [30000], 'baseScore': 3000, 'cost': 1500, 'maxMultiples': '2048倍'},
        {'id': 3, 'title': '高级场', 'need': [80000], 'baseScore': 10000, 'cost': 5000, 'maxMultiples': '2048倍'},
        {'id': 4, 'title': '土豪场', 'need': [200000], 'baseScore': 20000, 'cost': 10000, 'maxMultiples': '2048倍'},
        {'id': 5, 'title': '至尊场', 'need': [600000], 'baseScore': 72000, 'cost': 30000, 'maxMultiples': '2048倍'}
    ],
    #二人麻将
    '449': [
        {'id': 0, 'title': '新手场', 'need': [2000, 120000], 'baseScore': 120, 'cost': 200, 'maxMultiples': '2048倍'},
        {'id': 1, 'title': '普通场', 'need': [5000, 320000], 'baseScore': 350, 'cost': 500, 'maxMultiples': '2048倍'},
        {'id': 2, 'title': '中级场', 'need': [15000, 1800000], 'baseScore': 800, 'cost': 1000, 'maxMultiples': '2048倍'},
        {'id': 3, 'title': '高级场', 'need': [50000], 'baseScore': 2200, 'cost': 2000, 'maxMultiples': '2048倍'},
        {'id': 4, 'title': '土豪场', 'need': [100000], 'baseScore': 6600, 'cost': 5000, 'maxMultiples': '2048倍'},
        # {'id': 5, 'title': '至尊场', 'need': [500000], 'baseScore': 25000, 'cost': 25000, 'maxMultiples': '2048倍'}
        {'id': 5, 'title': '荣誉场', 'need': [500000], 'baseScore': 25000, 'cost': 25000, 'maxMultiples': '2048倍'}
    ],
    #鸡大胡麻将
    '452': [
        {'id': 0, 'title': '新手场', 'need': [2000, 80000], 'baseScore': 120, 'cost': 300, 'maxMultiples': '2048倍'},
        {'id': 1, 'title': '普通场', 'need': [5000, 160000], 'baseScore': 350, 'cost': 800, 'maxMultiples': '2048倍'},
        {'id': 2, 'title': '中级场', 'need': [15000], 'baseScore': 800, 'cost': 1300, 'maxMultiples': '2048倍'},
        {'id': 3, 'title': '高级场', 'need': [50000], 'baseScore': 2200, 'cost': 5000, 'maxMultiples': '2048倍'},
        {'id': 4, 'title': '土豪场', 'need': [100000], 'baseScore': 6600, 'cost': 10000, 'maxMultiples': '2048倍'},
        {'id': 5, 'title': '至尊场', 'need': [250000], 'baseScore': 25000, 'cost': 30000, 'maxMultiples': '2048倍'}
    ],
}

"""
    某游戏ID下在线金币场房间列表
    gold:online:room:$gameid:set
"""
GOLD_ONLINE_ROOM_SET = "gold:online:room:%s:set"

GOLD_ONLINE_PLAYID_ROOM_SET = "gold:online:playid:room:%s:%s:set"

"""
    总当前在线房间数
"""
GOLD_ONLINE_ROOM_SET_TOTAL = "gold:online:room:set:total"

"""
    在线集合 gameid
"""
GOLD_ONLINE_ACCOUNT_SET = 'gold:online:account:%s:set'

GOLD_ONLINE_PLAYID_ACCOUNT_SET = 'gold:online:playid:account:%s:%s:set'


"""
    在线集合
"""
GOLD_ONLINE_ACCOUNT_SET_TOTAL = 'gold:online:account:set:total'

""" 
    在线人数峰值时刻 gameid:date
    {'count:' xx, 'date': }
"""
GOLD_ONLINE_MAX_ACCOUNT_TABLE = 'gold:online:account:time:%s:%s:table'

"""
    某游戏ID下可加入金币场房间列表
    gold:canjoin:room:$gameid:$playid:set
"""
GOLD_CAN_JOIN_ROOM_SET = "gold:canjoin:room:%s:%s:set"

"""
金币场房间信息
{
       roomid        :     房间号,
       name          :     房间名称,
       playid          :     场次编号,
       minNum        :     最小人数,
       maxNum        :     最大人数,
       time          :     时间戳,
       rule          :     规则字符串,
}
gold:room:data:$gameid:$roomid:hesh
服务器关服时不需要清除
"""
GOLD_ROOM_DATA = 'gold:room:data:%s:%s:hesh'


"""
玩家所在对应金币场房间信息
gold:room:account:[account]:key
"""
GOLD_ROOM_ACCOUNT_KEY = 'gold:room:account:%s:key'

"""
    所有房间hesh key

"""
GOLD_ROOM_TOTAL_LIST = 'gold:room:total:list'

""" 
    玩家房间列表记录
"""
GOLD_ROOM_ACCOUNT_LIST = 'gold:room:account:%s:list'

"""
    属于金币场的gameid
"""
GOLD_GAMEID_SET = 'isgold:gameid:set'


"""
    属于红包赛的gameid
"""
RED_ENVELOPE_GAMEID_SET = 'isre:gameid:set'


"""
    用户待匹配信息
    {
        'playid':
        'gameid':
    }
"""
GOLD_ACCOUNT_WAIT_JOIN_TABLE = 'gold:account:%s:wait:join:table'


#  -----------  统计数据 私人数据库

""" 
    用户总数据
    'uid',
    'account',
    'nickname',
    'phone_num',
    'agent',
    'agent_wealth_rank',
    'gold_win_rate',
    'agent_win_rank',
    'cur_diamond_num',
    'buy_diamond_num',
    'buy_diamond_stream',
    'store_buy_record',
    'cur_gold_num',
    'buy_gold_num',
    'buy_gold_stream',
    'join_gold_game_sum',
    'gold_record_stream',
    'first_log_date',
    'last_log_date',

    gold:account:[account]:data
"""
GOLD_USER_TABLE = "gold:account:%s:data:table"

""" 
    'online_count': 总当前在线人数,
    'online_room': 总当前房间数
    'gold_total': 玩家当前拥有金币总数

    运营总表
    {
    'date': 日期,
    'player_count': 总参与玩家数,
    'room_count': 游戏房间总数
    'game_count': 金币场局数,
    'fee_total': 收取房费总额,
    'new_count': 新增用户数,
    'online_user_max': 在线人数峰值,
    'buy_gold_count': 购买金币人数
    'buy_gold_total': 购买金币数
    'buy_money': 购买总额
     }
    gold:operate:[gameid]:[xxx-xxx-xx(年月日)]:table
"""
GOLD_OPERATE = "gold:operate:%s:%s:table"

"""
    参与集合 gameid 按天
"""
GOLD_ACCOUNT_SET = 'gold:account:%s:%s:set'


"""
    新增用户 gameid 按天 
"""
GOLD_ACCOUNT_ADD_SET = 'gold:add:account:%s:%s:set'

"""
    参与总人数
"""
GOLD_ACCOUNT_SET_TOTAL = 'gold:account:set:total'

"""
    某游戏参与总人数
    gold:account:$gameid:set
"""
GOLD_ACCOUNT_GAMEID_SET = 'gold:account:%s:set'


"""
    工会胜局排行榜
    gold:win:rank:ag:zset
"""
GOLD_WIN_RANK_WITH_AGENT_ZSET = "gold:win:rank:%s:zset"

"""
    工会胜局排行榜 -- 按天
    gold:win:rank:ag:zset:byday
"""
GOLD_WIN_RANK_WITH_AGENT_ZSET_BYDAY = "gold:win:rank:%s:%s:zset"

"""
    工会财富排行榜
    gold:money:rank:ag:zset
"""
GOLD_MONEY_RANK_WITH_AGENT_ZSET = "gold:money:rank:%s:zset"



"""
    金币场记录保存时间
    1个月
"""
GOLD_ROOM_MAX_TIME = 30 * 24 * 60 * 60

"""
    金币场小局记录id
    gold:record:$gameid:count
"""
GOLD_RECORD_COUNT_TABLE = "gold:record:%s:count"


"""
    记录表
    gold:record:$gameid:xxx-xxx-xx(年月日):xx(tableid):table
    {
            'start_time': 开始时间,
            'end_time': 结束时间,
            'score': 分数|分数|||,
            'descs': 描述|描述|,
            'tiles': 牌|牌|,
            'roomid': 房间号,
            'accounts': 账号列表,
            'bull_info': 11|11| 
    }
    小局结算时更新牛牛记录表
"""
GOLD_RECORD_TABLE = "gold:record:%s:%s:%s:table"

"""
    金币场记录列表
    gold:record:$gameid:xxx-xxx-xx(年月日):list
"""
GOLD_RECORD_LIST = "gold:record:%s:%s:list"

"""
    金币场总记录列表
    gold:record:$gameid:list:total
"""
GOLD_RECORD_LIST_TOTAL = "gold:record:%s:list:total"


"""
    金币场玩家记录列表
    gold:record:account:total:$account:list
"""
GOLD_RECORD_ACCOUNT_TOTAL_LIST = "gold:record:account:total:%s:list"


"""
    金币场玩家胜局列表
    gold:record:account:win:$account:list
"""
GOLD_RECORD_ACCOUNT_WIN_LIST = "gold:record:account:win:%s:list"

"""
    金币场金币购买记录id
    gold:buy:record:count
"""
GOLD_BUY_RECORD_COUNT_TABLE = "gold:buy:record:count"


"""
    金币场总记录列表
    gold:buy:record:account:%s:list
"""
GOLD_BUY_RECORD_ACCOUNT_LIST = "gold:buy:record:account:%s:list"


"""
    金币场总记录列表
    gold:buy:record:list:total
"""
GOLD_BUY_RECORD_LIST_TOTAL = "gold:buy:record:list:total"

"""
    购买金币记录表
    gold:buy:record:tableid:table
    {
            'date': 时间,
            'gold': 金币数,
            'money': 金额,
            'account': 账号
    }
"""
GOLD_BUY_RECORD_TABLE = "gold:buy:record:%s:table"


GOLD_BUY_RECORD_ACCOUNT_GOLD_SUM = "gold:buy:record:account:%s:gold:sum"
GOLD_BUY_RECORD_ACCOUNT_MOENY_SUM = "gold:buy:record:account:%s:money:sum"


"""
    参与AI数---按天
"""
GOLD_AI_ACCOUNT_SET_BYDAY = "gold:ai:account:%s:set"

"""
    AI参与房间数---按天
"""
GOLD_AI_ROOM_SET_BYDAY = "gold:ai:room:%s:set"

"""
    AI参与金币场流水记录---按天
"""
GOLD_AI_RECORD_LIST_BYDAY = "gold:ai:record:%s:list"



# ------------------------  福利 & 任务 ------------------

"""
    任务状态
"""
MESSION_STATUS_NO = "0" #未完成
MESSION_STATUS_OK = "1" #已完成未领取
MESSION_STATUS_OVER = "2" #已完成已领取
MESSION_STATUS_NOT_YET = "3" #未满足领取条件

"""
    任务所属模块
"""
CHECK_PARTY_COMPETITION = "1"    #竞技场
CHECK_PARTY_GOLD = "2"           #金币场
CHECK_PARTY_MATCH = "3"          #比赛场
CHECK_CREATE_ROOM = "4"          #创房界面
CHECK_ACTIVICE = "5"             #活动界面
CHECK_MALL = "6"                 #商城
CHECK_SHARE = "7"                #分享


"""
    福利系统配置
    {
        'date' : 当前日期,
        'issigned': 今天是否签到,
        'signed': 已签到,
        'unsinged': 未签到,
        'patched': 补签,
        'defaultGold': '2000',
        'specialGold':{'4000': [1, 2, 3],....}
        'rewardlist': 奖励列表, 
        'messionlist': 任务列表,
        'sign_url': 签到地址
        'patchsign_url': 补签地址,
    }
    
"""






"""
    新手礼包
    {'account': 'status'}
"""
GOLD_REWARD_NEW_PRESENT_HASH = "gold:reward:new:present:hash"

"""
    每日首充奖励
    {'account': 'status'}
"""
GOLD_REWARD_DAY_BUY_GOLD_HASH = "gold:reward:buy:gold:%s:hash"

SIGN_MAX = 3  # 破产每日领取次数
SIGN_LINE = 1000  # 破产低保线
SIGN_COINNUM = 2000  # 破产每次赠送金币数

PATCH_SIGN_MAX = 5 # 每月补签次数
# PATCH_SIGN_FEE = 2 # 补签消耗钻石
PATCH_SIGN_FEE = 3000 # 补签消耗金币


"""
    七天奖励
    gold:welfare:sign:7days:[月份01-12]:hash
"""
GOLD_WELFARE_SIGN_7DAYS = "gold:welfare:sign:7days:%s:hash"

"""
    十五天奖励
"""
GOLD_WELFARE_SIGN_15DAYS = "gold:welfare:sign:15days:%s:hash"

"""
    月奖励
"""
GOLD_WELFARE_SIGN_MONTH = "gold:welfare:sign:month:%s:hash"

"""
    每日分享
    gold:welfare:share:@account:key : (%Y-%m-%d)
"""
GOLD_WELFARE_SHARE = "gold:welfare:share:%s:key"

"""
    福利界面配置，需要放在其他福利界面配置数据下面
    iconImg: icon_gold 金币图标,  icon_card 钻石图标
"""
WELFARE_REWARD_GOLD = {'id': 0, 'title': '金币', 'iconImg': 'icon_gold'}
WELFARE_REWARD_ROOMCARD = {'id': 1, 'title': '钻石', 'iconImg': 'icon_card'}
WELFARE_REWARD_YUANBAO = {'id': 2, 'title': '元宝', 'iconImg': 'icon_yuanbao'}
WELFARE_CONFIG = {
    'defaultGold': 2000,
    'specialGold': {
    },
    # need:满足奖励得签到天数，如果为负数，前端就会取 last_date 这个值
    'rewardlist': [
        {
            'id': 0,
            'title': '七天奖励',
            'status': 0,
            'need': 7,
            'jumpUrl': '/hall/welfare/get_reward',
            'params': {'id': 0},
            'itemList': [
                {'reward':WELFARE_REWARD_GOLD, 'baseRewardCount': 10000},
            ]
        },
        {
            'id': 1,
            'title': '十五天奖励',
            'status': 0,
            'need': 15,
            'jumpUrl': '/hall/welfare/get_reward',
            'params': {'id': 1},
            'itemList': [
                {'reward':WELFARE_REWARD_GOLD, 'baseRewardCount': 30000},
            ]
        },
        {
            'id': 2,
            'title': '月奖励',
            'status': 0,
            'need': -1,
            'jumpUrl': '/hall/welfare/get_reward',
            'params': {'id': 2},
            'itemList': [
                {'reward':WELFARE_REWARD_GOLD, 'baseRewardCount': 90000},
            ]
        },
    ],
    'sign_url': '/hall/welfare/sign',
    'patchsign_url': '/hall/welfare/patch_sign',
    'patchsign_cost': PATCH_SIGN_FEE,
    'patchsign_max': PATCH_SIGN_MAX,
    'patchsign_times': 0,
    'messionlist':[
        # {
        #     'id': 0,
        #     'title': "每日首冲奖励",
        #     'desc': '金币0',
        #     'jumpUrl': '/hall/welfare/get_welfare',
        #     'method': 'post',
        #     'params': {'id': 0},
        #     'status': "0",
        #     #  'routeData': {'gameid': 1},
        # },
        {
            'id': 1,
            'title': "新手礼包",
            'desc': '金币20000',
            'jumpUrl': '/hall/welfare/get_welfare',
            'method': 'post',
            'params': {'id': 1},
            'status': "0",
        }, {
            'id': 2,
            'title': "破产补助",
            'desc': '金币2000',
            'jumpUrl': '/hall/welfare/get_welfare',
            'baseLine': '1000',
            'isOver' : MESSION_STATUS_NO,
            'method': 'post',
            'params': {'id': 2},
            'status': "0",
        }, {
            'id': 3,
            'title': "分享有奖",
            'desc': '金币2000',
            'status': "0",
            'parent_mode': CHECK_SHARE,
            'routeData': {'jumpUrl': '/hall/welfare/share'},
        }, {
            'id': 4,
            'title': "精彩活动",
            'desc': '',
            'status': "0",
            'parent_mode': CHECK_ACTIVICE,
        }, 
        # {
            # 'id': 5,
            # 'title': "无限领金币",
            # 'desc': '每次20000',
            # 'jumpUrl': '/hall/welfare/get_welfare',
            # 'method': 'post',
            # 'params': {'id': 5},
            # 'status': "0",
        # },
        # {
            # 'id': 6,
            # 'title': "登陆领取门票",
            # 'desc': '门票2张',
            # 'method': 'post',
            # 'jumpUrl': '/hall/welfare/get_welfare',            
            # 'status': "0",
            # 'params': {'id': 6},
            # 'isOver' : MESSION_STATUS_NO,
        # },
    ],
}
"""
根据配置整理出特殊签到日期下，日期对应金币的映射
"""
WELFARE_CONFIG_SPECIAL_DATE2GOLD ={}
for gold, dateList in WELFARE_CONFIG['specialGold'].items():
    for date in dateList:
        WELFARE_CONFIG_SPECIAL_DATE2GOLD[date] = gold


"""
        金币场场次人数配置
"""
PARTY_GOLD_GAME_ONLINE_NUM_LIST = {
    '555': {
        '00': {'0': [50, 70], '1': [60, 80], '2': [20, 30]},
        '01': {'0': [30, 50], '1': [40, 60], '2': [10, 20]},
        '02': {'0': [10, 30], '1': [20, 40], '2': [5, 10]},
        '03': {'0': [10, 20], '1': [10, 30], '2': [5, 10]},
        '04': {'0': [2, 10], '1': [2, 10], '2': [2, 10]},
        '05': {'0': [2, 10], '1': [2, 10], '2': [2, 10]},
        '06': {'0': [2, 10], '1': [2, 10], '2': [2, 10]},
        '07': {'0': [2, 10], '1': [2, 10], '2': [2, 10]},
        '08': {'0': [10, 20], '1': [10, 30], '2': [5, 10]},
        '09': {'0': [10, 30], '1': [20, 40], '2': [5, 10]},
        '10': {'0': [30, 50], '1': [40, 60], '2': [10, 20]},
        '11': {'0': [50, 70], '1': [60, 80], '2': [20, 30]},
        '12': {'0': [60, 80], '1': [80, 110], '2': [30, 50]},
        '13': {'0': [60, 80], '1': [80, 110], '2': [30, 50]},
        '14': {'0': [60, 80], '1': [80, 110], '2': [30, 50]},
        '15': {'0': [70, 90], '1': [90, 120], '2': [40, 60]},
        '16': {'0': [60, 80], '1': [80, 110], '2': [30, 50]},
        '17': {'0': [50, 70], '1': [60, 80], '2': [20, 30]},
        '18': {'0': [50, 70], '1': [60, 80], '2': [20, 30]},
        '19': {'0': [60, 80], '1': [80, 110], '2': [30, 50]},
        '20': {'0': [80, 100], '1': [100, 200], '2': [50, 80]},
        '21': {'0': [120, 150], '1': [150, 200], '2': [80, 120]},
        '22': {'0': [120, 150], '1': [150, 200], '2': [80, 120]},
        '23': {'0': [80, 100], '1': [100, 200], '2': [50, 80]},
    },

    '556': {
        '00': {'0': [120, 150], '1': [150, 200], '2': [80, 100]},
        '01': {'0': [80, 120], '1': [90, 150], '2': [50, 80]},
        '02': {'0': [20, 80], '1': [40, 90], '2': [10, 50]},
        '03': {'0': [20, 30], '1': [20, 40], '2': [10, 20]},
        '04': {'0': [10, 20], '1': [10, 20], '2': [5, 10]},
        '05': {'0': [10, 15], '1': [10, 20], '2': [5, 10]},
        '06': {'0': [10, 15], '1': [10, 20], '2': [5, 10]},
        '07': {'0': [10, 15], '1': [10, 20], '2': [5, 10]},
        '08': {'0': [20, 30], '1': [20, 40], '2': [10, 20]},
        '09': {'0': [20, 80], '1': [40, 90], '2': [10, 50]},
        '10': {'0': [80, 120], '1': [90, 150], '2': [50, 80]},
        '11': {'0': [120, 150], '1': [150, 200], '2': [80, 100]},
        '12': {'0': [140, 180], '1': [160, 220], '2': [100, 130]},
        '13': {'0': [140, 180], '1': [160, 220], '2': [100, 130]},
        '14': {'0': [140, 180], '1': [160, 220], '2': [100, 130]},
        '15': {'0': [150, 190], '1': [170, 230], '2': [110, 140]},
        '16': {'0': [140, 180], '1': [160, 220], '2': [100, 130]},
        '17': {'0': [120, 150], '1': [150, 200], '2': [80, 100]},
        '18': {'0': [120, 150], '1': [150, 200], '2': [80, 100]},
        '19': {'0': [140, 180], '1': [160, 220], '2': [100, 130]},
        '20': {'0': [150, 200], '1': [180, 240], '2': [100, 150]},
        '21': {'0': [180, 220], '1': [200, 280], '2': [120, 160]},
        '22': {'0': [180, 220], '1': [200, 280], '2': [120, 160]},
        '23': {'0': [150, 200], '1': [180, 240], '2': [100, 150]},
    },
    '666': {
        '00': {'0': [20, 30], '1': [30, 50], '2': [10, 20]},
        '01': {'0': [15, 20], '1': [20, 30], '2': [8, 15]},
        '02': {'0': [8, 15], '1': [10, 20], '2': [5, 10]},
        '03': {'0': [5, 10], '1': [5, 10], '2': [5, 10]},
        '04': {'0': [2, 8], '1': [2, 8], '2': [2, 8]},
        '05': {'0': [2, 8], '1': [2, 8], '2': [2, 8]},
        '06': {'0': [2, 8], '1': [2, 8], '2': [2, 8]},
        '07': {'0': [2, 8], '1': [2, 8], '2': [2, 8]},
        '08': {'0': [5, 10], '1': [5, 10], '2': [5, 10]},
        '09': {'0': [8, 15], '1': [10, 20], '2': [5, 10]},
        '10': {'0': [15, 20], '1': [20, 30], '2': [8, 15]},
        '11': {'0': [20, 30], '1': [30, 50], '2': [10, 20]},
        '12': {'0': [30, 50], '1': [40, 60], '2': [15, 30]},
        '13': {'0': [30, 50], '1': [40, 60], '2': [15, 30]},
        '14': {'0': [30, 50], '1': [40, 60], '2': [15, 30]},
        '15': {'0': [40, 60], '1': [50, 80], '2': [20, 40]},
        '16': {'0': [30, 50], '1': [40, 60], '2': [15, 30]},
        '17': {'0': [20, 30], '1': [30, 50], '2': [10, 20]},
        '18': {'0': [20, 30], '1': [30, 50], '2': [10, 20]},
        '19': {'0': [30, 50], '1': [40, 60], '2': [15, 30]},
        '20': {'0': [40, 60], '1': [50, 80], '2': [20, 40]},
        '21': {'0': [50, 70], '1': [60, 100], '2': [30, 50]},
        '22': {'0': [50, 70], '1': [60, 100], '2': [30, 50]},
        '23': {'0': [40, 60], '1': [50, 80], '2': [20, 40]},
    },
}

GOLD_ONLINE_NUM_CACHE_KEY = "gold:online:num:cache:%s:%s:key"
GOLD_ONLINE_NUM_CACHE_VALUE = "gold:online:num:cache:%s:%s:value"

# welfare_daily_total_fee_日期_币种_类型
WELFARE_DAILY_FEE = 'welfare:daily:total_fee_%s_%s_%s'

# 特殊支出，记录平台发生故障时，平台活动成本
# gold:special_fee_%s 日期
SPECIAL_FEE = 'gold:special_fee_%s'


# 金币场的游戏列表
# 红中二人 444, 红中四人 445,跑得快 559,二人麻将449,斗地主 556
GOLD_GAME_LIST = [444,445,559,449,560]


"""
    机器人转为C、D档的概率，  robot:switch:{gameId}  该表为hash值，键为：档次，值为概率（0-100）
"""
ROBOT_SWITCH = 'robot:switch:%s'

"""
    设置机器人获取到好牌的规则 robot:goodhand:{gameId}:{robotlevel} robotlevel为B、C、D ，该表为hash值，键为：牌形，值为牌形概率值，如跑得快的话， AAA:20 2:15 AA:30
"""
ROBOT_GOOD_HAND_RULE = 'robot:goodhand:%s:%s'

