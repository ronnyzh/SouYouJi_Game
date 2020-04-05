# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/15
Revision: 1.0.0
Description: Description
"""
# 大厅ws服务列表
Key_Server_Set = 'match:hallServer:set'

#  进程类
Key_Server_Order = 'match:hallServer:%s:servicesOrder:list'

# ws服务器状态
Key_Server_Info = 'match:hallServer:%s:info:hesh'

# 比赛场
'''
'match:configs:(游戏ID):(赛事配置ID):list'
'''
Key_Match_Configs_List = 'match:configs:%s:%s:list'
'''
number:比赛所需参数人数
openType:比赛出现类型(1:随时可报名,2:定时开放报名) 
startType:比赛类型(1:人满即开,2:定时开放)
'''
Key_Match_Configs_Info = 'match:configs:%s:%s:hash'

Key_Match_EnrollUsers_Zset = 'match:game:%s:%s:enroll:users:zset'
Key_Match_UserEnroll = 'match:user:%s:enroll:hesh'

Key_Match_GameId_Set = 'match:game:ids:set'  # 比赛游戏ID集合
Key_Match_Game_MatchId_Set = 'match:game:%s:set'  # 比赛游戏ID对应场次ID集合
Key_Match_Game_MatchInfo_Hesh = 'match:game:%s:id:%s'  # 比赛游戏场次信息

Key_Match_GameId_matchNumber_Gameing_Set = 'match:game:%s:gameing:matchNumber:set'  # 某个游戏下,赛事列表
Key_Match_GameId_matchNumber_EndBalance_Set = 'match:game:%s:endBalance:matchNumber:set'  # 某个游戏下,赛事列表
Key_Match_matchNumber_Hesh = 'match:matchNumber:%s:hesh'  # 赛事详情

Key_Match_Mysql_Jobs = 'match:mysql:list'  # 比赛场sql任务
Key_Match_Mysql_Jobs_Error = 'match:mysql:error:list'  # 比赛场sql任务_失败

Key_Match_ServerInfo = 'match:gameServer:%s:%s:%s:hesh'

Key_Match_PlayingUser = 'match:playing:usrs:hesh'  # 比赛场玩家在线情况
