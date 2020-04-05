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
from common.card_define import *

import random
import re
from collections import Counter

Activedraw = True

GET_TILE = 1
GET_HAND_TILES = 2
GET_DEALER = 3
GET_GHOST = 4


class DealManager(DealMgr):
    """
    发牌管理器
    """

    def __init__(self, game=None):
        """
        初始化
        """
        self.game = game
        self.hc = self.game.HorseCount

        self.getGhost4GM = None
        self.getDealSetting()
        self.origTiles = self.createTiles()
        self.tiles = self.origTiles[:]
        self.setCtrlTypes()
        # 记录GM命令数据
        self.getTile4GM = {}
        self.getHandTiles4GM = {}
        self.getDealer4GM = -1

    def getDealSetting(self):
        """
        设置发牌器参数
        """
        self.setting = {
            'MAX_TILES_NUM': 9,
            'MAX_REPEAT_COUNT': 4,
            'PLAYER_COUNT': 4,
            'HAND_TILES_COUNT': 13,
            'INVALID_TILES_COUNT': self.hc,
            # 常规牌
            'NORMAL_TILES': [CHARACTER, DOT, BAMBOO],
            # 字牌[中发白,东南西北]
            'HONOR_TILES': [RED, WHITE, GREEN, EAST, WEST, SOUTH, NORTH],
            # 花牌
            'FLOWER_TILES': []
        }

    def setCtrlTypes(self):
        """
        GM类型到相应记录数据方法的映射
        """
        self.ctrlTypes = {
            GET_TILE: self.onGetTile4GM,
            GET_HAND_TILES: self.onGetHandTiles4GM,
            GET_DEALER: self.onGetDealer4GM,
            GET_GHOST: self.onGetGhost4GM,
        }

    def onGetGhost4GM(self, side, data):
        data = re.findall('\D\d', data)
        self.getGhost4GM = data
