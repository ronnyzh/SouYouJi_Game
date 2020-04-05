#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    web数据表及关系对应
"""

CLUB_CREATE_ATTR = "club:create_attribute:hash"
"""創建俱樂部的屬性
max_club_num  : 最大創建的俱樂部數
max_player_num: 創建俱樂部的最大玩家數量 (預留)
allow_create_room : ["account"]
"""
CLUB_LIST = "club:list:set"
""" 列表

俱乐部编号

"""
# 创始人创建的俱乐部列表
CLUB_ACCOUNT_LIST = "club:account:%s:set"
"""　创始人创建的俱乐部列表
%s = 用户account

俱乐部编号
"""

# 俱乐部所属的玩家列表
CLUB_PLAYER_LIST = "club:players:%s:set"
"""俱乐部所属的玩家列表
%s = 俱乐部id

存储
玩家account
"""
# 玩家所属的俱乐部列表
CLUB_PLAYER_TO_CLUB_LIST= "club:players:accounts:%s:set"
"""玩家所属的俱乐部列表
%s =　玩家ACCOUNT

存储：
俱乐部ＩＤ

"""
CLUB_ATTR = "club:attribute:%s:hash"
"""　
%s = 俱乐部编号
俱乐部属性
存储
club_name : 俱乐部名称
club_user : 俱乐部创建人
club_max_players: 俱乐部最大玩家数量（备用）
club_is_vip: 俱乐部是否是ＶＩＰ俱乐部（备用）
club_manager
club_agent
club_use_create_room
"""
# 用戶加入俱樂部审核列表
CLUB_AUDI_LIST = "club:auditing:%s:set"
"""
%s = 俱樂部ＩＤ
存儲:
account:nickname:avatar_url:status
"""

# 申请加入俱乐部的次数
CLUB_AUDI_INTO_NUMBER = "club:auditing:number:%s"


# 俱乐部基础创建属性
CLUB_GLOBAL_ATTRIBUT = "club:global:attribute:hash"
"""



"""
# 玩家进入俱乐部的临时存储
CLUB_PLAYER_INTO = "club:into:%s"
"""
%s = 玩家ACCOUNT


"""
CLUB_PLAYER_NOTES = "club:player:notes:%s:hash"
"""
俱乐部的玩家备注信息


"""

# 自动房间设置
CLUB_EXTENDS_ATTRIBUTE = "club:auto:create:room:%s:%s:hset"
"""
%s = 俱乐部ID

存储:


"""

# 自动房间设置列表
CLUB_EXTENDS_LIST_ATTRIBUTE = "club:auto:create:room:%s:set"
""" 

"""



CLUB_GAME_ATTRIBUTE_NUMBER = {
    5: 1,
    9991: 1,
    9992: 1,
    1001: 1,
    1000: 1,
    1003: 1,
    1004: 1,
    1007: 1,
    1005: 1,
    1006: 1,
    2000: 1,
    2005: 1,
    3003: 1,
    4001: 1,
    4002: 1,
    9990: 1
}


# 是否平局获取大赢家
IS_AVG = True