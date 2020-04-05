# -*- coding:utf-8 -*-
#!/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: 
"""


"""
    属于红包赛的gameid
"""
RED_ENVELOPE_GAMEID_SET = 'isre:gameid:set'


# # 用户道具数量表
PLAYER_ITEM_HASH = "player:item:uid:%s:hash"

# PARTY_TYPE_RE = '4' # gold_db_define.py 中已有，这里还是注释掉吧

"""
    设置领取低保的玩家或元宝数量少的玩家，将得到好牌概率
"""
TRIGGER_GOOD_HAND_RULE = 're:trigger:goodhand'

'''
加入过游戏的玩家
'''
RED_ENVELOPE_GAMEID_PLAYER_SET = 're:%s:%s:join:player'  # re:[yyyy-mm-dd]:[gameId]:join:player
RED_ENVELOPE_PLAYER_SET = 're:%s:join:player'  # re:[yyyy-mm-dd]:join:player

RED_ENVELOPE_GOLDINGOT = 're:%s:goldingot'

RED_ENVELOPE_TELEPHONE_FARE = 're:%s:telephonefare'

RED_ENVELOPE_PLAYER_GAMEINFO = 're:%s:join:player:gameInfo'  #键为uid ，值为列表，第一个元素为：当天进行局数 第二个元素：距离上次D档机器人的局数 第三个元素：输赢元宝数



'''
游戏进行的局数
'''
RED_ENVELOPE_GAMEID_ROUND = 're:%s:%s:round'
RED_ENVELOPE_ROUND = 're:%s:round'


'''
记录获取到的红包总额，键为单个红包金额，值为该红包金额的总额
'''
RED_ENVELOPE_GAMEID_MONEY = 're:%s:%s:money'  # re:[yyyy-mm-dd]:[gameId]:money'    用hash hincrby
RED_ENVELOPE_MONEY = 're:%s:money'


'''
房费
'''
RED_ENVELOPE_GAMEID_ROOM_CHARGE = 're:%s:%s:roomcharge'
RED_ENVELOPE_ROOM_CHARGE = 're:%s:roomcharge'


'''
机器人输赢的元宝数（不含房费），键为机器人档次，值为该档次机器人输赢元宝数
'''
RED_ENVELOPE_GAMEID_ROBOT_GOLDINGOT = 're:%s:%s:robot:goldingot'  # 用hash hincrby
RED_ENVELOPE_ROBOT_GOLDINGOT = 're:%s:robot:goldingot'



# '''
# 免费获取到的元宝数
# '''
# RED_ENVELOPE_GAMEID_FREE_GOLDINGOT = 're:%s:%s:free:goldingot' 用下面的 RED_ENVELOPE_BASELIVE_DAY 和 RED_ENVELOPE_BASELIVE_SUM 吧
# RED_ENVELOPE_FREE_GOLDINGOT = 're:%s:free:goldingot'


'''
红包赛日统计信息
playerCount
gameRound
reMoney30
reMoney60
reMoney120
roomCharge
robotB
robotD
baselive_goldingot
baselive_playerCount

金币转元宝数
玩家兑换红包价值
元宝充值数
充值总订单数
'''
RED_ENVELOPE_DAY_INFO = 're:%s:day:statistics' # re:[yyyy-mm-dd]:day:statistics


RED_ENVELOPE_BASELIVE_PLAYER_SET = 'vcoin:baselive:date:%s:set'  #当天赠送低保的玩家uid集合
RED_ENVELOPE_BASELIVE_DAY = 'vcoin:present:date:%s:sum'          #当天赠送低保的元宝总额
RED_ENVELOPE_BASELIVE_SUM = 'vcoin:present:date:sum'             #赠送低保的元宝总额
        # redis.sadd('vcoin:baselive:date:%s:set'%today_str,uid)
        # redis.incrby('vcoin:present:date:%s:sum'%today_str,12)
        # redis.incrby('vcoin:present:sum'%today_str,12)





