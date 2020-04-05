# coding=utf-8

"""
    某游戏ID下可加入荣誉场房间列表
    gold:canjoin:room:$gameid:$playid:hash
    {
    roomid:playcount
    }
"""
HONOR_CAN_JOIN_ROOM_HASH = "honor:canjoin:room:%s:%s:hash"

HONOR_ROOM_THRESHOLD = 'honor:setting:threshold:%s'
HONOR_ROOM_INFOS = 'honor:setting:infos:%s'

HONOR_ROOMS_SET = 'honor:gameList:set'
GOLD_ACCOUNT_WAIT_JOIN_TABLE = 'honor:account:%s:wait:join:table'
Honor_ACCOUNT_WAIT_JOIN_TABLE = 'honor:account:%s:wait:join:table'


"""
    某游戏ID下可加入金币场房间列表
    gold:canjoin:room:$gameid:$playid:set
"""
GOLD_CAN_JOIN_ROOM_SET = "gold:canjoin:room:%s:%s:set"