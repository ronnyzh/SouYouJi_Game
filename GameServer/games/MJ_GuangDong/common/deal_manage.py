#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    发牌管理器
"""
from gameobject import GameObject
# from common import consts
from common.log import log, LOG_LEVEL_RELEASE
# from common_player import CommonPlayer

# from common.protocols.mahjong_consts import *
# from common_db_define import *
from card_define import *

# import mahjong_pb2
# import replay4proto_pb2
# from pb_utils import *
# import time
# from datetime import datetime
# import copy
import random
# import redis_instance
import re

GET_TILE = 1
GET_HAND_TILES = 2
GET_DEALER = 3

class DealMgr(GameObject):
    """
    发牌管理器
    """
    def __init__(self, game):
        """
        """
        self.game = game
        self.getDealSetting()
        self.origTiles = self.createTiles()
        self.tiles = self.origTiles[:]
        self.setCtrlTypes()
        # 记录GM命令数据
        self.getTile4GM = {}
        self.getHandTiles4GM = {}
        self.getDealer4GM = -1

    def deal(self):
        """
        打乱牌
        """
        self.shuffleTiles(self.tiles)
        
    def resetTiles(self):
        """
        得到一副牌
        """
        self.tiles = self.origTiles[:]
        log(u'[resetTiles] tiles[%s]'%(self.tiles),LOG_LEVEL_RELEASE)

    def getOrigTileData(self):
        """
        获得一副牌里面一共有哪些不同的牌
        """
        return set(self.origTiles)

    def getTryReadyHandTiles(self):
        """
        一副牌中需要去测试是否听的牌
        """
        tiles = self.getOrigTileData() - set(self.setting['FLOWER_TILES'])
        log(u'[try ready hand] tiles[%s] OrigTile[%s] setting[%s]'%\
            (tiles, self.getOrigTileData(), set(self.setting['FLOWER_TILES'])),LOG_LEVEL_RELEASE)
        return tiles

    def getEachTiles(self):
        """
        获得所有边玩家的手牌
        """
        playerCount = self.game.maxPlayerCount
        eachTiles = [0]*playerCount
        
        if self.getHandTiles4GM:
            for side in self.getHandTiles4GM.keys():
                handTiles = self.dealTiles2PlayerByGM(side)
                eachTiles[side] = handTiles
        for side in xrange(playerCount):
            if not eachTiles[side]:
                eachTiles[side] = self.dealTiles2Player()
            
        return eachTiles

    def hasAnyTiles(self):
        """
        返回剩余牌的张数
        """
        return len(self.tiles)

    def getTotalTiles(self):
        """
        返回牌组的总长度
        """
        return len(self.origTiles)
        
    def setCtrlTypes(self):
        """
        GM类型到相应记录数据方法的映射
        """
        self.ctrlTypes = {
            GET_TILE         :  self.onGetTile4GM,
            GET_HAND_TILES   :  self.onGetHandTiles4GM,
            GET_DEALER       :  self.onGetDealer4GM,
        }
    
    def getDealSetting(self):
        """
        设置发牌器参数
        """
        self.setting = {
             'MAX_TILES_NUM'        :    9,
             'MAX_REPEAT_COUNT'     :    4,
             'HAND_TILES_COUNT'     :    13,
             'INVALID_TILES_COUNT'  :    0,
             #常规牌
             'NORMAL_TILES'         :    [CHARACTER,DOT,BAMBOO],
             #字牌[中发白,东南西北]
             'HONOR_TILES'          :    [RED, WHITE, GREEN, EAST, WEST, SOUTH, NORTH],
             #花牌
             'FLOWER_TILES'         :    [PLUM, ORCHID, BAMBOO1, CHRYSANTHEMUM, SPRING, SUMMER, AUTUMN, WINTER]
        }

    def shuffleTiles(self, tiles):
        """
        洗牌方法
        """
        random.shuffle(tiles)

    def dealTiles2Player(self):
        """
        发一副牌给玩家
        """
        tileNums = self.setting['HAND_TILES_COUNT']
        playerTiles = self.tiles[:tileNums]
        self.tiles = self.tiles[tileNums:]
        return playerTiles

    def dealTiles2PlayerByGM(self, side):
        """
        GM控制发牌
        """
        if self.getHandTiles4GM.has_key(side):
            handTiles = self.getHandTiles4GM[side]
            canUse = True
            for tile in handTiles:
                if self.tiles.count(tile) < handTiles.count(tile):
                    canUse = False
                    break
            if canUse:
                for tile in handTiles:
                    self.tiles.remove(tile)
                del self.getHandTiles4GM[side]
                tileNums = self.setting['HAND_TILES_COUNT']
                setNums = len(handTiles)
                if setNums < tileNums:
                    needCounts = tileNums - setNums
                    needTiles = self.tiles[:needCounts]
                    self.tiles = self.tiles[needCounts:]
                    handTiles.extend(needTiles)
                return handTiles
        return self.dealTiles2Player()
        
    def getDealerByGM(self):
        """
        GM控制dealer
        """
        dealerSide = self.getDealer4GM
        self.getDealer4GM = -1
        return dealerSide
        
    def getTile(self, side = -1):
        """
        摸牌方法
        """
        tile = ''
        # print 'getTile',side,self.getTile4GM,self.tiles
        if self.getTile4GM.has_key(side) and self.getTile4GM[side]:
            tileList = self.getTile4GM[side]
            tile = tileList[0]
            tileList.remove(tile)
        if tile not in self.tiles:
            print 'tile not in tiles',tile
            tile = self.tiles[0]
        self.tiles.remove(tile)
        return tile
        
    def isDraw(self):
        """
        是否流局
        """
        log(u'[is Draw] tiles[%s] INVALID_TILES_COUNT[%s]'%(len(self.tiles), self.setting['INVALID_TILES_COUNT']),LOG_LEVEL_RELEASE)
        return len(self.tiles) <= self.setting['INVALID_TILES_COUNT']

    def createTiles(self):
        """
        生成牌列表
        """
        tiles = []
        if self.setting.has_key('NORMAL_TILES') and self.setting['NORMAL_TILES']:
            for tile in self.setting['NORMAL_TILES']:
                for num in xrange(self.setting['MAX_TILES_NUM']):
                    tiles.append('%s%s'%(tile,num+1))

        if self.setting.has_key('HONOR_TILES') and self.setting['HONOR_TILES']:
            for tile in self.setting['HONOR_TILES']:
                #字牌
                tiles.append('%s'%(tile))

        tiles = tiles * self.setting['MAX_REPEAT_COUNT']

        if self.setting.has_key('FLOWER_TILES') and self.setting['FLOWER_TILES']:
            for tile in self.setting['FLOWER_TILES']:
                tiles.append('%s'%(tile))

        return tiles
        
    def onGetTile4GM(self, side, data):
        data = re.findall('\D\d', data)
        self.getTile4GM[side] = data

    def onGetHandTiles4GM(self, side, data):
        data = re.findall('\D\d', data)
        self.getHandTiles4GM[side] = data

    def onGetDealer4GM(self, side, data):
        self.getDealer4GM = int(data)
        
        
if __name__ == "__main__":
    dealMgr = DealMgr()
    dealMgr.deal()
    dealMgr.getTile4GM[2] = 'a5'
    dealMgr.getHandTiles4GM[2] = ['a1','a1','a1','a1','a2','a2','a2','a2','a3','a3','a3','a3','a4']
    dealMgr.getHandTiles4GM[3] = ['b1','b1','b1','b1','b2','b2','b2','b2','b3','b3','b3','b3','b4']
    dealMgr.getDealer4GM = 1
    print dealMgr.tiles
    print dealMgr.hasAnyTiles()
    print dealMgr.getHandTiles4GM
    print dealMgr.getEachTiles()
    print dealMgr.getHandTiles4GM
    print dealMgr.hasAnyTiles()
    print dealMgr.getTile(2)
    print dealMgr.hasAnyTiles()
    print dealMgr.getEachTiles()
    print dealMgr.hasAnyTiles()
    print dealMgr.getTile()
    print dealMgr.hasAnyTiles()
    print dealMgr.getTile()
    print dealMgr.hasAnyTiles()
    print dealMgr.getDealerByGM()
    print dealMgr.getDealerByGM()
    
 
  
   
    
