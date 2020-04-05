# -*- coding:utf-8 -*-
#!/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: game logic
"""

#from common.gameobject import GameObject
from common.handle_manger import HandleManger
from common.card_define import *
from common.log import *
import hainan_mahjong_pb2

import copy

class Handel(HandleManger):
    def __init__(self, player):
        super(Handel, self).__init__(player)
        self.wind = None #自己的风
        self.flower = None #自己的花
        self.season = None #自己的季节
        self.specialTileList = [] #摸到的花牌
        self.kongNow = False    #杠上开花标志
        self.flowerNow = False  #花上添花标志
        self.isPlayTile = False #是否已出牌
        self.isFirstDiscard = None

    def setWind(self, tile): #设置风
        self.wind = tile

    def setFlower(self, tile): #设置花
        self.flower = tile

    def setSeason(self, tile): #设置季节
        self.season = tile

    def setEye(self,tile):#设置眼
        self.eye = tile

    #是否有番，有番才能胡
    def isAllEat(self): #只吃不碰
        if self.getPongTiles() or self.getKongTiles() or self.getConcealedKongTiles():
            return False
        for tiles in self.tripleTiles:
            if tiles[0] == tiles[1]:
                return False
        return True
        # if self.eye:
            # eyeType = getTileType(self.eye)
            # if eyeType and eyeType != DRAGON and self.eye != self.wind:#白中发自风不可
                # if max(self.tile2num.values()) < TRIPLET_NUM \
                        # and not self.getPongTiles() and not self.getKongTiles() and not self.getConcealedKongTiles():
                    # return True
        # return False

    def haveEye(self): #有眼
        """
        2,5,8万,条,筒 2张
        """
        if self.eye:
            return getTilePoints(self.eye) in [2, 5, 8] and getTileType(self.eye) in MAHJONG_TYPE_LIST
        return False

    def haveDragon(self): #箭刻牌
        for tile, num in self.tile2num.items():
            if num == TRIPLET_NUM and getTileType(tile) == DRAGON:
                return True
        for tile in DRAGON_TILES:
            if tile in self.getKongTiles() or tile in self.getPongTiles() or tile in self.getConcealedKongTiles():
                return True
        return False

    def haveWind(self): #风刻牌

        if not self.wind:
            return False

        if self.wind in self.kongTiles or self.wind in self.pongTiles or self.wind in self.concealedKongTiles:
            return True

        if self.wind in self.tile2num and self.tile2num[self.wind] == TRIPLET_NUM:
            return True

        return False

    def isOrderWind(self):
        if not self.player.game.isOrder:
            return False

        wind = WIND_TILES[self.player.game.orderNum]

        if wind in self.kongTiles or wind in self.pongTiles or wind in self.concealedKongTiles:
            return True

        if wind in self.tile2num and self.tile2num[wind] == TRIPLET_NUM:
            return True

        return False

    def isMySpecialTile(self): #翻花对立
        if self.season in self.getFlowerTiles() or self.flower in self.getFlowerTiles():
            return True
        return False

    def canHu(self): #是否有番

        log(u'[canHu][info] isAllEat[%s] isClean[%s] haveEye[%s] isMySpecialTile[%s] isAllPong[%s]'\
                            %(self.isAllEat(),self.isClean(),self.haveEye(),self.isMySpecialTile(),self.isAllPong()),LOG_LEVEL_RELEASE)

        if self.isAllEat() or self.isClean()    or self.haveEye() \
                           or self.haveDragon() or self.haveWind() or self.isOrderWind() \
                           or self.isMixColour()  or self.isMySpecialTile()\
                           or self.isAllPong() or self.getKongTiles() or self.getConcealedKongTiles():
            return True
        return False

    def isCheckHu(self): #胡牌前置条件：是否有番
        #检查是否花胡
        #self.checkFlowerHu()

        if self.player.game.hasFan and (not self.isDraw() and not self.canHu()):
            log(u'[check Hu][error] not fan.', LOG_LEVEL_RELEASE)
            return False

        if self.isSuperSevenPair():
            return True
        
        huResult = super(Handel, self).isCheckHu()

        log(u'[check Hu] isCanHu[%s] isCheckHu[%s] isDraw[%s]'%(self.canHu(), huResult, self.isDraw()), LOG_LEVEL_RELEASE)

        return huResult

    def isEatKongHu(self): #抢杠胡
        if self.canHu:
            return False
        super(Handel, self).isCheckHu()

    def _rmTile(self, tile):
        super(Handel, self)._rmTile(tile)
        self.kongNow = False
        self.flowerNow = False

    def tryEatSpecialTile(self, tile, isMyTile = False): #补花
        if tile not in FLOWER_TILES:
            return False
        self.specialTileList.append(tile)
        if isMySpecialTile:
            self._rmTile(tile)
        self.kongNow = False
        return True

    def getConcealedKongList(self): # 暗杠列表
        self.flowerNow = False
        return super(Handel, self).getConcealedKongList()

    def onKong(self, tile): #杠
        super(Handel, self).onKong(tile)
        self.flowerNow = False

    def is4FlowerHu(self):
        """
        四花胡 1.春夏秋冬 2.梅兰菊竹
        """
        if set(self.flowerTiles) >= set(FLOWER_SEASON_TILES) \
                        or set(self.flowerTiles) >= set(FLOWER_FLOWER_TILES):
            return True
        return False

    def getGrabKongHu(self):
        '''
        获得可以抢杠胡的牌列表
        '''
        actionNtiles = {}
        if self.tmpTile:
            self._addTiles([self.tmpTile])
            if self.isSuperSevenPair() or self.isWaitingHu() or self.isSevenPair() or self.isThirteenOrphans():
                self._rmTile(self.tmpTile)
                actionNtiles[HU] = [self.tmpTile]
                return actionNtiles
            self._rmTile(self.tmpTile)
        return actionNtiles

    def getBalanceTiles(self):
        balanceTiles = super(Handel, self).getBalanceTiles()
        balanceTiles[-1] = ''
        return balanceTiles

    def getChowList(self):
        '''
        获得可以吃的牌列表
        '''
        if self.player.game.maxPlayerCount in (2,3):
            return []
        return super(Handel, self).getChowList()

# if __name__ == '__main__':
    # handlMgr = Handel()
    # handlMgr.tiles = ['a1','a1','a1','a1','a2','a2','a2','a2','a3','a3','a3','a3','a4']
    #handlMgr.setEye()
    # print 'eye:%s'%(handlMgr.eye)
    # print 'isAllPong:%s'%(handlMgr.isAllPong())
    # print 'canHU:%s'%(handlMgr.canHu())
    # print 'isFlowerHu:%s'%(handlMgr.isFlowerHu())