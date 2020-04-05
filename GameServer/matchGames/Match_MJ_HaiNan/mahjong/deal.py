# -*- coding:utf-8 -*-
# !/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    发牌管理器
"""
from common.deal_manage import DealMgr
import random

class DealMange(DealMgr):
    """
    发牌管理器
    """

    def __init__(self, game=None):
        """
        """
        super(DealMange, self).__init__(game)

    def getDealSetting(self):
        super(DealMange, self).getDealSetting()
        self.setting['INVALID_TILES_COUNT'] = 15
