# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: 金币场时间配置
"""
'''
    如果需要改写请写在mahjong目录下文件名为Inherit_time_config
'''

# common类
# 引用库

def getTime_Action():
    '''Action倒计时时间'''
    return 15 * 1000


def getTime_Action_Proxy():
    '''托管Action倒计时时间'''
    return 2 * 1000


try:
    from poker.Inherit_time_config import *
except:
    pass
