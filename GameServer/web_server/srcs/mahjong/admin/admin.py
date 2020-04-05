#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    后台APP应用入口
"""

from bottle import Bottle
from common.install_plugin import install_redis_plugin,install_session_plugin

admin_app = Bottle()

install_redis_plugin(admin_app)
install_session_plugin(admin_app)

import admin_index
import admin_auth
#会员模块
import admin_member
# 数据统计模块
import admin_statistics
# 个人信息模块
import admin_self
# 代理模块
import admin_agent
# 用户权限模块
import admin_power
#游戏模块
import admin_game
#订单模块
import admin_order
#商品模块
import admin_goods
#系统设置
import admin_setting
#消息设置
import admin_notic
#捕鱼模块
import admin_fish

# 背包模块
import admin_bag


#任务模块
import admin_task


'''    金币场模块
'''
import admin_gold

""" 比赛场模块 """
import admin_match

""" 荣誉场模块 """
import admin_honor

#活动模块
import admin_activice
