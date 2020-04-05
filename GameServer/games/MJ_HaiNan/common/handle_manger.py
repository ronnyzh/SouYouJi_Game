# -*- coding:utf-8 -*-
#!/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: game logic
"""

from gameobject import GameObject
from card_define import *
from log import *
import copy

class HandleManger(GameObject):
    def __init__(self, player):
        self.player = player

        self.tiles = [] #手牌列表
        self.myTileCount = 14

        self.pongTiles = [] #碰的牌列表
        self.kongTiles = [] #杠的牌列表
        self.selfKongTiles = []
        self.othersKongTiles = [] #别人打出来的杠的列表，数据格式为[[放杠的人, 牌], [放杠的人, 牌]]，如：[[1,'a1'], [2',c2']]
        self.beKongTiles = [] #放杠给别人的列表
        self.concealedKongTiles = [] #暗杠的牌列表
        self.chowTiles = [] #吃的牌列表
        self.discardTiles = [] #已经打出的牌列表
        self.flowerTiles = []
        self.specialTileList = []
        # 碰的牌到放碰玩家的边的映射{'a1':2}
        self.pongTile2Side = {}
        self.selfKongSideNTile = []
        self.actionNum = -1
        self.tiles2NumList = {}

        self.lastTile = None #记录刚摸上来的牌（第14张牌），出牌后会设为None
        self.tmpTile = None
        self.tmpSide = -1
        self.firstDiscard = None
        self.lastDiscard = None
        self.isDiscard = False
        self.isGrabKongSide = -1

        self.eye = None #眼

        self.type2tiles = {} #牌类型对应的牌列表
        self.tile2num = {} #每张牌的数量
        self.tripleList = [] #成牌列表，只用于判断是否胡牌
        self.tripleTiles = [] #三张一组

        self.huData = [-1, None, []]
        self.action2balanceTiels = {PONG:[],CHOW:[], OTHERS_KONG:[], SELF_KONG:[], CONCEALED_KONG:[]}

        #鬼牌，可变成任意牌的牌
        #ghost和ghostlist无法同时使用，对于多个鬼牌的时候请使用ghostlist（单个鬼牌时也可使用ghostlist，不过为了兼容旧代码保留了ghost）
        #在game设置specialTile的时候会自动设置ghost，此时ghostlist不会进行处理，如果使用ghostlist时需要自行增加协议与客户端交互
        self.ghost = None
        self.ghostList = []
        self.ghostCount = 0
        self.useGhost = {}
        self.useGhostList = []

        self.readyHandList = []

#++++++++++++++++++++ 胡牌算法 ++++++++++++++++++++

    def _initTileData(self, tiles, type): #是否成牌
        # log(u'[init Tile Data]tiles[%s] type[%s] useGhost[%s] ghostCount[%s] eye[%s]'\
                # %(tiles, type, self.useGhost, self.ghostCount, self.eye), LOG_LEVEL_RELEASE)
        if type in self.tripleList:
            return

        if not tiles:
            self.tripleList.append(type)
            return

        tilesLen = len(tiles)
        overTileCount = tilesLen % TRIPLET_NUM

        #成坎不使用鬼，无将
        if overTileCount == 0:
            result, notUseGhost = self._isTripilet(tiles)
            if result:
                self.tripleList.append(type)
                return
        elif not self.eye and overTileCount == EYE_NUM: #成坎不使用鬼，有将，将不使用鬼
            for tile in tiles:
                self.eye = tile
                if self.tile2num[tile] < EYE_NUM:
                    continue
                testTiles = copy.deepcopy(tiles)
                for count in xrange(EYE_NUM):
                    testTiles.remove(tile)
                result, notUseGhost = self._isTripilet(testTiles)
                if result:
                    self.tripleList.append(type)
                    return
            self.eye = None

        oneTileList = []
        for useGhostCount in xrange(self.ghostCount): #使用鬼数从少到多
            testGhostCount = useGhostCount + 1

            if not self.eye and overTileCount + testGhostCount >= EYE_NUM: #成坎使用鬼，有将
                oneTileList = []

                #成坎使用鬼，有将，将不使用鬼
                for tile in tiles:
                    self.eye = tile
                    if self.tile2num[tile] < EYE_NUM:
                        oneTileList.append(tile)
                        continue
                    testTiles = copy.deepcopy(tiles)
                    for count in xrange(EYE_NUM):
                        testTiles.remove(tile)
                    result, notUseGhost = self._isTripilet(testTiles, testGhostCount)
                    if result:
                        self.tripleList.append(type)
                        self.useGhost[type] = testGhostCount - notUseGhost
                        self.ghostCount = self.ghostCount - (testGhostCount - notUseGhost)
                        return
                self.eye = None

            #成坎使用鬼，无将
            if overTileCount + testGhostCount >= TRIPLET_NUM:
                result, notUseGhost = self._isTripilet(tiles, testGhostCount)
                if result:
                    self.tripleList.append(type)
                    self.useGhost[type] = testGhostCount - notUseGhost
                    self.ghostCount = self.ghostCount - (testGhostCount - notUseGhost)
                    return

            if not self.eye and overTileCount + testGhostCount >= EYE_NUM:
                #成坎不使用鬼，有将，将使用鬼
                # if not oneTileList:
                    # oneTileList = []
                for tile in oneTileList:
                    self.eye = tile
                    testTiles = copy.deepcopy(tiles)
                    testTiles.remove(tile)
                    result, notUseGhost = self._isTripilet(testTiles)
                    if result:
                        self.tripleList.append(type)
                        self.useGhost[type] = EYE_NUM - 1
                        self.ghostCount -= (EYE_NUM - 1)
                        return
                self.eye = None

                #成坎使用鬼，有将，将使用鬼
                if testGhostCount >= 2:
                    # if not oneTileList:
                        # oneTileList = []
                    for tile in oneTileList:
                        self.eye = tile
                        testTiles = copy.deepcopy(tiles)
                        testTiles.remove(tile)
                        result, notUseGhost = self._isTripilet(testTiles, testGhostCount - 1)
                        if result:
                            self.tripleList.append(type)
                            self.useGhost[type] = testGhostCount - notUseGhost
                            self.ghostCount = self.ghostCount - (testGhostCount - notUseGhost)
                            return
                    self.eye = None

    def _isTripilet(self, tiles, ghostCount = 0):
        for num in xrange(ghostCount + 1): #使用鬼数从少到多
            result, count, tileList = self.__isTripilet(tiles, num)
            if result:
                self.tripleTiles.extend(tileList)
                if self.useGhostList:
                    useGhostList = copy.deepcopy(self.useGhostList)
                    for tripleTileData in self.tripleTiles:
                        for index, tile in enumerate(tripleTileData):
                            if tile == None:
                                tripleTileData[index] = useGhostList[0]
                                useGhostList = useGhostList[1:]
                return result, count
        return False, ghostCount

    def __isTripilet(self, tiles, ghostCount = 0, tileList = []):
        testTiles = copy.deepcopy(tiles)
        if not tiles:
            return True, ghostCount, tileList

        firstTile = testTiles[0]
        type = getTileType(firstTile)
        num = getTilePoints(firstTile)
        secondTile = type + str(num+1)
        thirdTile = type + str(num+2)
        if len(testTiles) >= 3:
            if firstTile == testTiles[2]: #三张一样
                tripleList = copy.deepcopy(tileList)
                tripleList.append(testTiles[:TRIPLET_NUM])
                result, count, tripleList = self.__isTripilet(testTiles[TRIPLET_NUM:], ghostCount, tripleList)
                if result:
                    return result, count, tripleList
            if ghostCount and firstTile == testTiles[1]: #有鬼, 两张一样
                tripleList = copy.deepcopy(tileList)
                appendTiles = testTiles[:TRIPLET_NUM-1]
                appendTiles.append(self.ghost)
                tripleList.append(appendTiles)
                result, count, tripleList = self.__isTripilet(testTiles[TRIPLET_NUM-1:], ghostCount - 1, tripleList)
                if result:
                    return result, count, tripleList
            if type in MAHJONG_TYPE_LIST:
                if secondTile in testTiles and thirdTile in testTiles: #顺子
                    newTestTiles = copy.deepcopy(testTiles)
                    newTestTiles.remove(firstTile)
                    newTestTiles.remove(secondTile)
                    newTestTiles.remove(thirdTile)
                    tripleList = copy.deepcopy(tileList)
                    appendTiles = [firstTile, secondTile, thirdTile]
                    tripleList.append(appendTiles)
                    result, count, tripleList = self.__isTripilet(newTestTiles, ghostCount, tripleList)
                    if result:
                        return result, count, tripleList
                if ghostCount and (secondTile in testTiles or thirdTile in testTiles): #有鬼，顺子差一张
                    for tile in [secondTile, thirdTile]:
                        if tile in testTiles:
                            newTestTiles = copy.deepcopy(testTiles)
                            newTestTiles.remove(firstTile)
                            newTestTiles.remove(tile)
                            tripleList = copy.deepcopy(tileList)
                            appendTiles = [firstTile, tile, self.ghost]
                            tripleList.append(appendTiles)
                            result, count, tripleList = self.__isTripilet(newTestTiles, ghostCount - 1, tripleList)
                            if result:
                                return result, count, tripleList
            if ghostCount >=2: #两张鬼牌第单张肯定成牌
                tripleList = copy.deepcopy(tileList)
                appendTiles = testTiles[:TRIPLET_NUM-2]
                appendTiles.extend([self.ghost, self.ghost])
                tripleList.append(appendTiles)
                return self.__isTripilet(testTiles[TRIPLET_NUM-2:], ghostCount - 2, tripleList)
        elif ghostCount and len(testTiles) == 2:
            if firstTile == testTiles[1]: #两张一样
                tripleList = copy.deepcopy(tileList)
                appendTiles = testTiles[:TRIPLET_NUM-1]
                appendTiles.extend([self.ghost])
                tripleList.append(appendTiles)
                result, count, tripleList = self.__isTripilet(testTiles[TRIPLET_NUM-1:], ghostCount - 1, tripleList)
                if result:
                    return result, count, tripleList
            if type in MAHJONG_TYPE_LIST:
                if ghostCount and (secondTile in testTiles or thirdTile in testTiles): #顺子差一张
                    for tile in [secondTile, thirdTile]:
                        if tile in testTiles:
                            newTestTiles = copy.deepcopy(testTiles)
                            newTestTiles.remove(firstTile)
                            newTestTiles.remove(tile)
                            tripleList = copy.deepcopy(tileList)
                            appendTiles = [firstTile, tile]
                            appendTiles.extend([self.ghost])
                            tripleList.append(appendTiles)
                            result, count, tripleList = self.__isTripilet(newTestTiles, ghostCount - 1, tripleList)
                            if result:
                                return result, count, tripleList
            if ghostCount >=2: #两张鬼牌第单张肯定成牌
                tripleList = copy.deepcopy(tileList)
                appendTiles = testTiles[:TRIPLET_NUM-2]
                appendTiles.extend([self.ghost, self.ghost])
                tripleList.append(appendTiles)
                return self.__isTripilet(testTiles[TRIPLET_NUM-2:], ghostCount - 2, tripleList)
        if ghostCount >=2: #两张鬼牌第单张肯定成牌
            tripleList = copy.deepcopy(tileList)
            appendTiles = testTiles[:TRIPLET_NUM-2]
            appendTiles.extend([self.ghost, self.ghost])
            tripleList.append(appendTiles)
            return self.__isTripilet(testTiles[TRIPLET_NUM-2:], ghostCount - 2, tripleList)
        return False, ghostCount, tileList

    def setGhost(self, tile): #设置鬼牌
        self.ghost = tile
        self.onRefreshTileData()

    def addGhostList(self, tile): #鬼牌列表增加牌，不可和setGhost同时使用
        self.ghostList.append(tile)
        self.onRefreshTileData()

    def cleanGhostList(self): #清空鬼牌列表
        self.ghostList = []
        self.onRefreshTileData()

    def isSevenPair(self):#七对子
        if self.isClean():
            notPairCount = 0
            # print 'tile2num',self.tile2num
            for tile, count in self.tile2num.items():
                isOne =count % 2
                if isOne:
                    notPairCount += 1
            ghostCount = self.ghostCount
            for count in self.useGhost.values():
                ghostCount += count
            # log(u'[isSevenPair]notPairCount[%s] ghostCount[%s] useGhost[%s]'\
                    # %(notPairCount, self.ghostCount, self.useGhost), LOG_LEVEL_RELEASE)
            if notPairCount <= ghostCount:
                return True
        return False

    def isThirteenOrphans(self): #十三幺
        if not self.isClean():
            return False
        ThirteenOrphansList = ['a1', 'a9', 'b1', 'b9', 'c1', 'c9']
        ThirteenOrphansList.extend(HONOR_TILES)
        return set(ThirteenOrphansList) == set(self.tiles)

    def isSuperSevenPair(self): #豪华七对
        # log(u'[isSuperSevenPair]isSevenPair[%s] tile2num[%s]'%(self.isSevenPair(), self.tile2num), LOG_LEVEL_RELEASE)
        return self.isSevenPair() and max(self.tile2num.values()) == MAX_REPEAT_COUNT

    def isDraw(self): #自摸
        # log(u'[is draw]lastTile[%s]'%(self.lastTile), LOG_LEVEL_RELEASE)
        if self.lastTile:
            return True
        return False

    def isMixColour(self): #混一色
        useType = None
        testTiles = copy.deepcopy(self.tiles)
        testTiles.extend(self.pongTiles)
        testTiles.extend(self.kongTiles)
        testTiles.extend(self.concealedKongTiles)
        for tile in self.chowTiles:
            testTiles.append(tile[0])
        for tile in testTiles:
            if tile in HONOR_TILES_SET or tile in FLOWER_TILES_SET:
                continue
            type = getTileType(tile)
            if not useType:
                useType = type
            if type != useType:
                return False
        return True

    def isClean(self): #门清
        if self.chowTiles or self.pongTiles or self.kongTiles or self.concealedKongTiles:
            return False
        return True

    def isOneColour(self): #清一色
        useType = None
        testTiles = copy.deepcopy(self.tiles)
        testTiles.extend(self.pongTiles)
        testTiles.extend(self.kongTiles)
        testTiles.extend(self.concealedKongTiles)
        for tile in self.chowTiles:
            testTiles.append(tile[0])
        for tile in testTiles:
            type = getTileType(tile)
            if not useType:
                useType = type
            if type != useType:
                return False
        if useType in HONOR_TILES_SET or useType in FLOWER_TILES_SET:
            return False
        return True

    def isAllPong(self): #碰碰胡
        return self.tile2num.values().count(MIN_REPEAT_COUNT) == 0 and self.tile2num.values().count(EYE_NUM) == 1 and not self.chowTiles

    def isWaitingHu(self): #是否已经成牌
        return len(self.tripleList) == len(self.type2tiles.keys())

    def isCheckHu(self):
        '''
        确认是否胡，修改胡规则则重写此方法
        '''
        # log(u'[isCheckHu][info] tripleList[%s] type2tilesKey[%s]'%(len(self.tripleList),len(self.type2tiles.keys())), LOG_LEVEL_RELEASE)
        if self.isWaitingHu(): #33332
            return True
        if self.isSevenPair(): #七对
            return True
        if self.isThirteenOrphans(): #十三幺
            return True
        return False

    def getReadyHands(self, tiles):
        '''
        获得听牌列表
        '''
        if self.readyHandList:
            return self.readyHandList

        readyHands = []
        lastTile = self.lastTile
        tmpSide = self.tmpSide
        for tile in tiles:
            self._addTiles([tile])
            self.lastTile = tile
            self.tmpSide = -1
            if self.isCheckHu():
                readyHands.append(tile)
            self._rmTile(tile)
        self.lastTile = lastTile
        self.tmpSide = tmpSide
        readyHands.sort()
        self.readyHandList = copy.deepcopy(readyHands)
        return readyHands
    def getReadyHandsFancy(self,tiles,onetile):
        '''
        获得假设听牌列表
        '''
        self._rmTile(onetile)
        readyHands = []
        removingtiles=onetile
        lastTile = self.lastTile
        tmpSide = self.tmpSide
        for tile in tiles:
            self._addTiles([tile])
            self.lastTile = tile
            self.tmpSide = -1
            if self.isCheckHu():
                readyHands.append(tile)
            self._rmTile(tile)
        self.lastTile = lastTile
        self.tmpSide = tmpSide
        readyHands.sort()
        self._addTiles([onetile])
        return readyHands

 #++++++++++++++++++++ 胡牌算法end ++++++++++++++++++++


 #++++++++++++++++++++ action相关 ++++++++++++++++++++


    def getAllowActionNTiles(self, allowActions = ()):
        '''
        获得允许进行的action
        '''
        # print 'test allowActions', allowActions
        # print 'test tmpTile for get allowActions', self.tmpTile
        # print 'test lastTile for get allowActions', self.lastTile
        action2callback ={
            CHOW: self.getChowList,
            PONG: self.getPongList,
            OTHERS_KONG: self.getOthersKongList,
            SELF_KONG: self.getSelfKongList,
            CONCEALED_KONG: self.getConcealedKongList,
            HU: self.getHuList
        }
        actionNtiles = {}
        for action in allowActions:
            tiles = action2callback[action]()
            # log(u'action[%s] Call return[%s]'%(action, tiles), LOG_LEVEL_RELEASE)
            # log(u'[try getAllowAction] tiles[%s]'%(tiles), LOG_LEVEL_RELEASE)
            if tiles:
                actionNtiles[action] = tiles
        # print 'test actionNtiles',actionNtiles
        log(u'[try getAllowAction] allowActions[%s] actionNtiles[%s]'%(allowActions,actionNtiles), LOG_LEVEL_RELEASE)
        return actionNtiles

    def getChowList(self):
        '''
        获得可以吃的牌列表
        '''
        if self.tmpTile:
            if self.tmpTile == self.ghost or self.tmpTile in self.ghostList:
                return []
            chowList = []
            tmpTileType = getTileType(self.tmpTile)
            tmpTilePoint = getTilePoints(self.tmpTile)
            tmpTileNextTiles = [packTile4TypeNPoints(tmpTileType, tmpTilePoint + 1), packTile4TypeNPoints(tmpTileType, tmpTilePoint + 2)]
            tmpTilePreviousTiles = [packTile4TypeNPoints(tmpTileType, tmpTilePoint - 2), packTile4TypeNPoints(tmpTileType, tmpTilePoint - 1)]

            if self.checkTile(tmpTilePreviousTiles[0]) and self.checkTile(tmpTilePreviousTiles[1]) and \
                    self.ghost not in [tmpTilePreviousTiles[0], tmpTilePreviousTiles[1]] and\
                    tmpTilePreviousTiles[0] not in self.ghostList and tmpTilePreviousTiles[1] not in self.ghostList: #前两张牌可吃
                chowList.append('%s,%s,%s'%(self.tmpTile, tmpTilePreviousTiles[0], tmpTilePreviousTiles[1]))
            if self.checkTile(tmpTilePreviousTiles[1]) and self.checkTile(tmpTileNextTiles[0]) and \
                    self.ghost not in [tmpTilePreviousTiles[1], tmpTileNextTiles[0]] and\
                    tmpTilePreviousTiles[1] not in self.ghostList and tmpTileNextTiles[0] not in self.ghostList: #夹中间可吃
                chowList.append('%s,%s,%s'%(self.tmpTile, tmpTilePreviousTiles[1], tmpTileNextTiles[0]))
            if self.checkTile(tmpTileNextTiles[0]) and self.checkTile(tmpTileNextTiles[1]) and \
                    self.ghost not in [tmpTileNextTiles[0], tmpTileNextTiles[1]] and\
                    tmpTileNextTiles[0] not in self.ghostList and tmpTileNextTiles[1] not in self.ghostList: #后两张牌可吃
                chowList.append('%s,%s,%s'%(self.tmpTile, tmpTileNextTiles[0], tmpTileNextTiles[1]))
            return chowList
        return []

    def getPongList(self):
        '''
        获得可以碰的牌列表
        '''
        if self.tmpTile == self.ghost or self.tmpTile in self.ghostList:
            return []
        if self.tmpTile and self.tiles.count(self.tmpTile) >= EYE_NUM:
            return [self.tmpTile]
        return []

    def getOthersKongList(self):
        '''
        获得可以杠的牌列表（其他人出牌）
        '''
        if self.tmpTile == self.ghost or self.tmpTile in self.ghostList:
            return []
        if self.tmpTile and self.tiles.count(self.tmpTile) >= TRIPLET_NUM:
            return [self.tmpTile]
        return []

    def getSelfKongList(self):
        '''
        获得可以杠的牌列表（自己摸到）
        '''
        kongList = []
        for tile in self.tiles:
            if tile in self.pongTiles and (tile != self.ghost and tile not in self.ghostList):
                kongList.append(tile)
        return kongList

    def getConcealedKongList(self):
        '''
        获得可以暗杠的牌列表
        '''
        if self.lastTile:
            concealedKongList = []
            for tile, num in self.tile2num.iteritems():
                if num >= MAX_REPEAT_COUNT and (tile != self.ghost and tile not in self.ghostList):
                    concealedKongList.append(tile)
            return concealedKongList
        return []

    def getHuList(self):
        '''
        获得可以胡的牌列表
        '''
        log(u'[getHuList] tmpTile[%s] lastTile[%s] isCheckHu[%s]'%(self.tmpTile,self.lastTile,self.isCheckHu()),LOG_LEVEL_RELEASE)
        if self.tmpTile:
            self._addTiles([self.tmpTile])
            if self.isCheckHu():
                self._rmTile(self.tmpTile)
                return [self.tmpTile]
            self._rmTile(self.tmpTile)
        elif self.lastTile and self.isCheckHu():
            return [self.lastTile]
        return []

    def getGrabKongHu(self):
        '''
        获得可以抢杠胡的牌列表
        '''
        return self.getAllowActionNTiles([HU])

    def doOnAction(self, action, tiles):
        '''
        执行操作
        会把执行的action存储进self.action2balanceTiels，
        其为字典的格式，是action到side以及tile的映射
        例如：
            吃a1a2a3, side=2的玩家放了a2给吃，则记录：
                self.action2balanceTiels[CHOW].append('2;a2,a1,a3'）
            碰a1a1a1, side=3的玩家放了a1给碰，则记录：
                self.action2balanceTiels[PONG].append('3;a1,a1,a1')
            杠a1a1a1a1, side=3的玩家自己杠铃，则记录：
                self.action2balanceTiels[SELF_KONG].append('3;a1,a1,a1,a1')
        '''
        action2callback ={
            CHOW: self.onChow,
            PONG: self.onPong,
            OTHERS_KONG: self.onOthersKong,
            SELF_KONG: self.onSelfKong,
            CONCEALED_KONG: self.onConcealedKong,
            HU: self.onHu
        }
        self.readyHandList = []
        if action in action2callback:
            if action != HU:
                self.isDiscard = True
                side = self.player.chair
                if self.tmpSide >= 0:
                    side = self.tmpSide
                _tiles = copy.deepcopy(tiles)
                _tiles = self.packActionTiles(action, _tiles)
                tileData = ','.join(_tiles)
                tilesData = '%s;%s'%(side, tileData)
                self.action2balanceTiels[action].append(tilesData)
                if action == SELF_KONG:
                    tilesData = '%s;%s'%(self.pongTile2Side[tiles[0]], tileData)
                    self.selfKongSideNTile.append(tilesData)
                else:
                    self.myTileCount -= TRIPLET_NUM
                self.actionNum += 1
                if tilesData not in self.tiles2NumList:
                    self.tiles2NumList[tilesData] = []
                self.tiles2NumList[tilesData].append(self.actionNum)
            action2callback[action](tiles)

    def onChow(self, tiles):
        '''
        进行吃操作
        '''
        eatTile = tiles[0]
        rmTiles = tiles[1:]
        for tile in rmTiles:
            if tile not in self.tiles:
                return False
        self._rmTiles(rmTiles)
        self.chowTiles.append(tiles)
        if self.tmpSide >= 0:
            self.player.game.players[self.tmpSide].handleMgr.discardTiles.remove(eatTile)
        return True

    def onPong(self, tiles):
        '''
        进行碰操作
        '''
        tile = tiles[0]
        if self.tile2num[tile] < EYE_NUM:
            return False
        self._rmTiles([tile, tile])
        self.pongTiles.append(tile)
        self.pongTile2Side[tile] = self.tmpSide
        if self.tmpSide >= 0:
            self.player.game.players[self.tmpSide].handleMgr.discardTiles.remove(tile)
        return True

    def onOthersKong(self, tiles):
        '''
        进行杠操作（别人打的）
        '''
        tile = tiles[0]

        if self.tile2num[tile] < TRIPLET_NUM:
            return False
        self._rmTiles([tile] * TRIPLET_NUM)
        if self.tmpSide >= 0:
            self.player.game.players[self.tmpSide].handleMgr.discardTiles.remove(tile)
        self.othersKongTiles.append([self.tmpSide, tile])
        self.player.game.players[self.tmpSide].handleMgr.beKongTiles.append(tile)
        self.kongTiles.append(tile)
        return True

    def onSelfKong(self, tiles):
        '''
        进行杠操作（自己摸的）
        '''
        tile = tiles[0]

        if tile not in self.pongTiles:
            return False
        self._rmTile(tile)
        self.pongTiles.remove(tile)
        for data in self.action2balanceTiels[PONG]:
            if tile in data.split(';')[-1].split(','):
                self.action2balanceTiels[PONG].remove(data)
                break
        self.selfKongTiles.append(tile)
        self.kongTiles.append(tile)
        return True

    def onConcealedKong(self, tiles):
        '''
        进行暗杠操作
        '''
        tile = tiles[0]
        if self.tile2num[tile] < MAX_REPEAT_COUNT:
            return False
        self._rmTiles([tile] * MAX_REPEAT_COUNT)
        self.concealedKongTiles.append(tile)
        return True

    def onHu(self, tiles):
        '''
        进行胡操作
        '''
        huSide = self.tmpSide
        huTile = tiles[0]
        huTiles = copy.deepcopy(self.getTiles())
        if self.isGrabKongSide >= 0:
            huSide = self.isGrabKongSide
            self._addTiles([huTile])
        elif self.tmpSide == -1:
            huTiles.remove(huTile)
            huSide = self.player.chair
        else:
            self._addTiles([huTile])
        self.huData = [huSide, huTile, huTiles]


 #++++++++++++++++++++ action相关end ++++++++++++++++++++


 #++++++++++++++++++++ 添加移除牌相关 ++++++++++++++++++++


    def _refreshTileData(self, alterTiles):
        '''
        刷新手牌的统计数据，其中alterTiles为增加或者减少的牌
        '''
        self.tiles.sort()
        self.type2tiles = {}
        self.tripleList = []
        self.tripleTiles = []
        self.useGhostList = []
        self.useGhost = {}
        self.tile2num = {}
        self.eye = None
        for tile in self.tiles:
            if tile == self.ghost or tile in self.ghostList:
                continue
            self.tile2num[tile] = self.tiles.count(tile)
            tileType = getTileType(tile)
            if tileType not in self.type2tiles:
                self.type2tiles[tileType] = []
            self.type2tiles[tileType].append(tile)
            self.useGhost[tileType] = 0
        self.ghostCount = self.tiles.count(self.ghost)
        if self.ghostList:
            self.ghostCount = 0
            for tile in self.ghostList:
                self.ghostCount += self.tiles.count(tile)
        for tile in alterTiles:
            if tile == self.ghost or tile in self.ghostList:
                continue
        for type in self.type2tiles.keys():
            if type in self.type2tiles:
                self.type2tiles[type].sort()
                self._initTileData(self.type2tiles[type], type)

    def onRefreshTileData(self):
        tiles = self.getTiles()
        self._refreshTileData(tiles)

    def _addTiles(self, tiles = []):
        '''
        添加一组牌
        '''
        self.tiles.extend(tiles)
        self._refreshTileData(tiles)

    def _rmTile(self, tile):
        '''
        移除一张牌
        '''
        self.tiles.remove(tile)
        self._refreshTileData([tile])

    def _rmTiles(self, tiles):
        '''
        移除一组牌
        '''
        for tile in tiles:
            self.tiles.remove(tile)
        self._refreshTileData(tiles)

    def setMyTileCount(self, len):
        '''
        设置手牌数
        '''
        self.myTileCount = len + 1

    def getNeedTileCount(self):
        '''
        获得需要补的牌数
        '''
        log(u'[get need tile count]myTileCount[%s] tilesLen[%s]'%(self.myTileCount, len(self.tiles)), LOG_LEVEL_RELEASE)
        needTiles = self.myTileCount - len(self.tiles)
        # if not needTiles:
            # log(u'[get need tile count][error]player[%s] not need tile'%(self.player.nickname), LOG_LEVEL_RELEASE)
        return needTiles

    def setTmpTile(self, tile, side = -1):
        '''
        设置别人出的牌，用于检测别人出牌时的吃碰杠胡
        '''
        self.tmpTile = tile
        if side >= 0:
            self.tmpSide = side

    def doAddTiles(self, tiles = [], draw = True):
        '''
        加入手牌
        '''
        self._addTiles(tiles)
        if draw and tiles:
            self.lastTile = tiles[-1]
            self.tmpSide = -1

    def discard(self, tile):
        '''
        出牌
        '''
        self._rmTile(tile)
        self.discardTiles.append(tile)
        if self.lastTile != tile:
            self.readyHandList = []
        self.lastTile = None
        self.isDiscard = True

    def getFlowerList(self):
        '''
        获得手牌中的花牌的列表，并从手牌移除花牌
        '''
        flowerTiles= []
        for tile in self.tiles:
            if tile in FLOWER_TILES:
                flowerTiles.append(tile)
        if flowerTiles:
            self._rmTiles(flowerTiles)
            self.flowerTiles.extend(flowerTiles)
            log(u'[get flower list]nickname[%s] add[%s] flowerTiles[%s]'\
                    %(self.player.nickname, flowerTiles, self.flowerTiles), LOG_LEVEL_RELEASE)
        return flowerTiles


 #++++++++++++++++++++ 添加移除牌相关end ++++++++++++++++++++


 #++++++++++++++++++++ 通用工具函数 ++++++++++++++++++++


    def packActionTiles(self, action, tileList):
        '''
        打包广播用action数据
        '''
        if action == CHOW:
            lastTile = tileList[-1]
            tileList[-1] = tileList[0]
            tileList[0] = lastTile
        elif action == PONG:
            tileList = tileList * TRIPLET_NUM
        elif action in (OTHERS_KONG, SELF_KONG):
            tileList = tileList * MAX_REPEAT_COUNT
        elif action == CONCEALED_KONG:
            concealedKongTile = tileList[0]
            tileList = [''] * MAX_REPEAT_COUNT
            tileList[-1] = concealedKongTile
        return tileList

    def checkTile(self, tile):
        '''
        检测有无此牌
        '''
        if tile in self.tiles:
            # print 'checkTile',tile,self.tiles
            return True
        return False

    def getDiscardTiles(self):
        '''
        返回出过的牌列表
        '''
        return self.discardTiles

    def getTiles(self):
        '''
        返回手牌列表
        '''
        return self.tiles

    def getChowTiles(self):
        '''
        返回吃过的牌列表
        '''
        return self.chowTiles

    def getPongTiles(self):
        '''
        返回碰过的牌列表
        '''
        return self.pongTiles

    def getKongTiles(self):
        '''
        返回杠过牌列表
        '''
        return self.kongTiles

    def getKongBySelfTiles(self):
        '''
        返回杠过牌列表（自己摸的）
        '''
        return self.selfKongTiles

    def getKongByAnotherTiles(self):
        '''
        返回杠过牌列表（其他人打的）
        '''
        return self.othersKongTiles

    def getBeKongTiles(self):
        '''
        放杠给别人的列表
        '''
        return self.beKongTiles

    def getConcealedKongTiles(self):
        '''
        返回暗杠过牌列表
        '''
        return self.concealedKongTiles

    def getLastTile(self):
        '''
        返回最后摸的牌
        '''
        return self.lastTile

    def getFlowerTiles(self):
        '''
        获得补过的花牌列表
        '''
        return self.flowerTiles

    def getHuData(self):
        '''
        获得胡牌数据，包括胡了哪张牌、放炮位置、胡牌列表
        '''
        return self.huData

    def getBalanceTiles(self):
        '''
        获得结算用牌数据列表
        会先放入self.action2balanceTiels记录的action（没有则不写入）
        然后放入获得手牌数据及胡牌数据
        最后放入花牌列表（没有则固定为空字符串）
        如果有需要添加的数据可在之后再添加
        所有牌字符组合都按逗号分隔，若存在放吃/碰/杠的，使用';'隔开放家side，如:
        ['1;a1,a2,a3', '2;b4,b4,b4,b4', '2;c1,c1,c1', '$手牌(若胡，第一张为胡的牌)', '$花牌',$上层需扩展的牌字串...]
        '''
        balanceTiles = []
        for key, tileDatas in self.action2balanceTiels.iteritems():
            if key == SELF_KONG:
                balanceTiles.extend(self.selfKongSideNTile)
            else:
                balanceTiles.extend(tileDatas)
        huSide, huTile, huTiles = self.getHuData()
        if huSide >= 0:
            tileData = ','.join(huTiles)
            tileData += ',%s'%huTile
        else:
            tileData = ','.join(self.getTiles())
        balanceTiles.append(tileData)

        flowers = ','.join(self.getFlowerTiles())
        if not flowers:
            flowers = ''
        balanceTiles.append(flowers)
        return balanceTiles

    def getTilesNReadyHands(self):
        return self.getTiles(), self.getReadyHands(self.player.game.dealMgr.getTryReadyHandTiles())

 #++++++++++++++++++++ 通用工具函数end ++++++++++++++++++++

