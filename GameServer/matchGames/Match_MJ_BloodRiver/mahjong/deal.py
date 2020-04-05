#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    发牌管理器
"""
from common.deal_manage import DealMgr
from common.card_define import *

import random
import re


class DealManager(DealMgr):
    """
    发牌管理器
    """
    def __init__(self, game=None):
        """
        """
        super(DealManager, self).__init__(game)


    def getDealSetting(self):
        """
        设置发牌器参数
        """
        self.setting = {
             'MAX_TILES_NUM'        :    9,
             'MAX_REPEAT_COUNT'     :    4,
             'PLAYER_COUNT'         :    4,
             'HAND_TILES_COUNT'     :    13,
             'INVALID_TILES_COUNT'  :    0,
             #常规牌
             'NORMAL_TILES'         :    [CHARACTER, DOT, BAMBOO],
             #字牌[中发白,东南西北]
             'HONOR_TILES'          :    [],
             #花牌
             'FLOWER_TILES'         :    []
        }

