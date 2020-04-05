# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/11/19
Revision: 1.0.0
Description: Description
"""
import random


def getTime_Action_special():
    return 2 * 1000


def getTime_Action_Proxy():
    '''托管Action倒计时时间'''
    return 2 * 1000


def getTime_RobLandlord_Must():
    return random.randint(3000, 5000)


def getTime_RobLandlord():
    return 15 * 1000


def getTime_Action():
    '''Action倒计时时间'''
    return 30 * 1000
