# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: game logic
"""

# from common.gameobject import GameObject
from common.handle_manger import HandleManger
from common.card_define import *
from common.log import *
from common.common_game import CommonGame
import copy
import collections
from Hutype import *
from collections import Counter


class Handel(HandleManger):
    def __init__(self, player):
        super(Handel, self).__init__(player)

        # 杠上开花的标记
        self.KongFlower = False
        self.BeKongFlower = None
        self.NoKongList = []

    def setGhost(self, tile):  # 设置鬼牌
        if isinstance(tile, str):
            self.ghost = tile
            self.onRefreshTileData()
        elif isinstance(tile, list):
            self.ghostList.extend(tile)
            self.onRefreshTileData()
        else:
            return False

    ###########doOnAction##############
    def doOnAction(self, action, tiles):
        action2callback = {
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
                tilesData = '%s;%s' % (side, tileData)
                self.action2balanceTiels[action].append(tilesData)
                if action == SELF_KONG:
                    tilesData = '%s;%s' % (self.pongTile2Side[tiles[0]], tileData)
                    self.selfKongSideNTile.append(tilesData)
                else:
                    self.myTileCount -= TRIPLET_NUM
                self.actionNum += 1
                if tilesData not in self.tiles2NumList:
                    self.tiles2NumList[tilesData] = []
                self.tiles2NumList[tilesData].append(self.actionNum)

                if action in [SELF_KONG, CONCEALED_KONG, OTHERS_KONG]:  # 杠上开花的标记
                    self.KongFlower = True

                if action == OTHERS_KONG and self.player.game.isBaoKongHu:
                    self.BeKongFlower = self.tmpSide

            action2callback[action](tiles)

    def discard(self, tile):
        '''
        出牌
        '''
        self.KongFlower = False  # 初始化杠上开花的标记
        self.BeKongFlower = None  # 初始化明杠爆的标记
        super(Handel, self).discard(tile)

    def getAllowActionNTiles(self, allowActions=()):
        '''
        获得允许进行的action
        '''
        action2callback = {
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

            if self.NoKongList and action == SELF_KONG:  # 过杠不杠（三张牌碰后不能再杠）
                for p in self.NoKongList:
                    if p in tiles:
                        tiles.remove(p)

            if tiles:
                actionNtiles[action] = tiles

        if actionNtiles.has_key(PONG) and actionNtiles[PONG] and actionNtiles.has_key(OTHERS_KONG) and actionNtiles[
            OTHERS_KONG]:
            for v in actionNtiles[PONG]:
                if v in actionNtiles[OTHERS_KONG]:
                    self.NoKongList.append(v)

        log(u'[try getAllowAction] allowActions[%s] actionNtiles[%s]' % (allowActions, actionNtiles), LOG_LEVEL_RELEASE)
        return actionNtiles

    def removeGhost(self, testTiles):  # 移除牌中的鬼牌
        if self.ghostList:
            for __ghost in self.ghostList:
                while 1:
                    if __ghost in testTiles:
                        testTiles.remove(__ghost)
                    else:
                        break
        if self.ghost:
            while 1:
                if self.ghost in testTiles:
                    testTiles.remove(self.ghost)
                else:
                    break
        return testTiles

    def getGhostCount(self):  # 获取鬼牌数量
        tmpghostcount = 0
        if self.ghostList:
            for _ghost in self.ghostList:
                tmpghostcount += self.tiles.count(_ghost)
        elif self.ghost:
            tmpghostcount = self.tiles.count(self.ghost)
        return tmpghostcount

    def getHuScore(self):
        DescMap = collections.OrderedDict()
        DescMap[BigFourHu] = {'func': self.isBigFour, 'fan': 88, 'ignore': [PongHu, PingHu]}
        DescMap[BigThreeHu] = {'func': self.isBigThree, 'fan': 88, 'ignore': [PongHu, PingHu]}
        DescMap[ThirteenOrphans] = {'func': self.isThirteenOrphans, 'fan': 88, 'ignore': [PingHu]}

        DescMap[TianHu] = {'func': self.isTianHu, 'fan': 64}
        DescMap[DiHu] = {'func': self.isDiHu, 'fan': 64}
        DescMap[CleanYaoNine] = {'func': self.isCleanYaoNine, 'fan': 64, 'ignore': [PongHu, MixYaoNine, PingHu]}
        DescMap[ZiColourHu] = {'func': self.isZiColourHu, 'fan': 64, 'ignore': [PongHu, PingHu]}

        DescMap[SmallFourHu] = {'func': self.isSmallFour, 'fan': 48, 'ignore': [PingHu]}
        DescMap[SmallThreeHu] = {'func': self.isSmallThree, 'fan': 48, 'ignore': [PingHu]}

        DescMap[MixYaoNine] = {'func': self.isMixYaoNine, 'fan': 32, 'ignore': [PongHu, PingHu]}
        DescMap[SuperSevenPairHu] = {'func': self.isSuperSevenPair, 'ignore': [SevenPairHu, PongHu, PingHu], 'fan': 32}

        DescMap[SevenPairHu] = {'func': self.isSevenPair, 'fan': 16, 'ignore': [PongHu, PingHu]}
        DescMap[OneColourHu] = {'func': self.isOneColour, 'fan': 16, 'ignore': [PingHu]}

        DescMap[MixColourHu] = {'func': self.isMixColour, 'fan': 8, 'ignore': [PingHu]}
        DescMap[PongHu] = {'func': self.isPongHu, 'fan': 8, 'ignore': [PingHu]}
        DescMap[SeeMoon] = {'func': self.isSeeMoon, 'fan': 8}
        DescMap[KongHu] = {'func': self.isKongHu, 'fan': 8}
        DescMap[BeGrabKongHu] = {'func': self.isBeGrabKongHu, 'fan': 8}
        DescMap[PingHu] = {'func': self.isPingHu, 'fan': 2}

        ignoreDesc = []
        desclist = []
        fanNum = 0
        for _desc, _data in DescMap.items():
            _func = _data['func']
            _ignore = _data.get('ignore', [])
            _fan = _data.get('fan', 0)
            if _desc in ignoreDesc:
                continue
            if _func():
                desclist.append(_desc)
                ignoreDesc.extend(_ignore)
                fanNum += _fan
        self.player.huDescs.extend(desclist)
        return fanNum

    def isPingHu(self):
        return True

    def isBeGrabKongHu(self):
        '''抢杠胡'''
        return self.player.game.beGrabKongHuPlayer

    def isKongHu(self):
        '''杠上开花'''
        if self.KongFlower:
            return True
        return False

    def isSeeMoon(self):
        '''海底捞月'''
        return not self.player.game.dealMgr.tiles

    def isTianHu(self):
        '''天胡'''
        if self.player.game.isTianDiHu:
            if self.player == self.player.game.dealer and not self.concealedKongTiles:
                return True
        return False

    def isDiHu(self):
        '''地胡'''
        if self.player.game.isTianDiHu:
            if self.player != self.player.game.dealer:
                return True
            elif self.concealedKongTiles:
                return True
        return False

    def isThirteenOrphans(self):
        '''十三幺'''
        if not self.player.game.huType_ThirteenOrphans:
            return False
        return super(Handel, self).isThirteenOrphans()

    def isBigFour(self):
        '''大四喜'''
        if not self.player.game.huType_BigFourHu:
            return False
        testTiles = copy.deepcopy(self.tiles)
        testTiles.extend(self.pongTiles * 3)
        testTiles.extend(self.kongTiles * 4)
        testTiles.extend(self.concealedKongTiles * 4)
        _dict = Counter(testTiles)
        if _dict[EAST] >= 3 and _dict[NORTH] >= 3 and _dict[SOUTH] >= 3 and _dict[WEST] >= 3:
            return True
        return False

    def isBigThree(self):
        '''大三元'''
        if not self.player.game.huType_BigThreeHu:
            return False
        testTiles = copy.deepcopy(self.tiles)
        testTiles.extend(self.pongTiles * 3)
        testTiles.extend(self.kongTiles * 4)
        testTiles.extend(self.concealedKongTiles * 4)
        _dict = Counter(testTiles)
        if _dict[RED] >= 3 and _dict[GREEN] >= 3 and _dict[WHITE] >= 3:
            return True
        return False

    def isSmallFour(self):
        '''小四喜'''
        if not self.player.game.huType_SmallFourHu:
            return False
        testTiles = copy.deepcopy(self.tiles)
        testTiles.extend(self.pongTiles * 3)
        testTiles.extend(self.kongTiles * 4)
        testTiles.extend(self.concealedKongTiles * 4)
        _dict = Counter(testTiles)
        if _dict[EAST] == 3 and _dict[NORTH] == 3 and _dict[SOUTH] == 3 and _dict[WEST] == 2:
            return True
        if _dict[EAST] == 3 and _dict[NORTH] == 3 and _dict[SOUTH] == 2 and _dict[WEST] == 3:
            return True
        if _dict[EAST] == 3 and _dict[NORTH] == 2 and _dict[SOUTH] == 3 and _dict[WEST] == 3:
            return True
        if _dict[EAST] == 2 and _dict[NORTH] == 3 and _dict[SOUTH] == 3 and _dict[WEST] == 3:
            return True
        return False

    def isSmallThree(self):
        '''小三元'''
        if not self.player.game.huType_SmallThreeHu:
            return False
        testTiles = copy.deepcopy(self.tiles)
        testTiles.extend(self.pongTiles * 3)
        testTiles.extend(self.kongTiles * 4)
        testTiles.extend(self.concealedKongTiles * 4)
        _dict = Counter(testTiles)
        zhong = _dict[RED]
        fa = _dict[GREEN]
        bai = _dict[WHITE]
        if zhong == 2 and fa >= 3 and bai >= 3:
            return True
        if fa == 2 and zhong >= 3 and bai >= 3:
            return True
        if bai == 2 and fa >= 3 and zhong >= 3:
            return True
        return False

    def isCleanYaoNine(self):
        '''清幺九'''
        if not self.isPongHu():  # 是否碰碰胡
            return False
        testTiles = copy.deepcopy(self.tiles)
        testTiles.extend(self.pongTiles)
        testTiles.extend(self.kongTiles)
        testTiles.extend(self.concealedKongTiles)
        testTiles = self.removeGhost(testTiles)
        ###是否有除1.9外点数的牌（字牌也不行）
        for t in testTiles:
            type = getTileType(t)
            number = getTilePoints(t)
            if type in HONOR_TYPE_LIST or (number != 1 and number != 9):
                return False
        return True

    def isMixYaoNine(self):
        '''混幺九'''
        if not self.isPongHu():  # 是否碰碰胡
            return False
        testTiles = copy.deepcopy(self.tiles)
        testTiles.extend(self.pongTiles)
        testTiles.extend(self.kongTiles)
        testTiles.extend(self.concealedKongTiles)
        testTiles = self.removeGhost(testTiles)
        ###是否有除1.9外点数的牌（字牌也不行）
        isHasZi = False  # 是否有字牌
        isHasOneNine = False  # 是否有1,9牌(避免是全字牌)
        for t in testTiles:
            type = getTileType(t)
            number = getTilePoints(t)
            if type in HONOR_TYPE_LIST:
                isHasZi = True
                continue
            elif number == 1 or number == 9:
                isHasOneNine = True
                continue
            else:
                return False
        if isHasOneNine and isHasZi:
            return True
        return False

    def isZiColourHu(self):
        '''字一色'''
        if not self.isPongHu():
            return False
        tmptiles = copy.deepcopy(self.tiles)
        tmptiles.extend(self.pongTiles)
        tmptiles.extend(self.kongTiles)
        tmptiles.extend(self.concealedKongTiles)
        tmptiles = self.removeGhost(tmptiles)
        for t in tmptiles:
            type = getTileType(t)
            if type not in HONOR_TYPE_LIST:
                return False
        return True

    def isSevenPair(self):
        '''七对子'''
        if self.isClean():
            notPairCount = 0
            for tile, count in self.tile2num.items():
                isOne = count % 2
                if isOne:
                    notPairCount += 1
            ghostCount = self.ghostCount
            for count in self.useGhost.values():
                ghostCount += count
            if notPairCount <= ghostCount:
                return True
        return False


    def isSuperSevenPair(self):
        '''豪华七对'''
        if not self.player.game.huType_SuperSevenPairHu:
            return False
        if self.isSevenPair():
            count = 0
            for k, v in self.tile2num.iteritems():
                if v == MAX_REPEAT_COUNT and v != self.ghost:
                    count += 1
            if count > 0:
                return count
        return False

    def isOneColour(self):
        '''清一色'''
        useType = None
        testTiles = copy.deepcopy(self.tiles)
        testTiles.extend(self.pongTiles)
        testTiles.extend(self.kongTiles)
        testTiles.extend(self.concealedKongTiles)
        testTiles = self.removeGhost(testTiles)
        for tile in testTiles:
            type = getTileType(tile)
            if not useType:
                useType = type
            if type != useType:
                return False
        if useType in HONOR_TILES_SET or useType in FLOWER_TILES_SET:
            return False
        return True

    def isMixColour(self):
        '''混一色'''
        useType = None
        hasFlowerTile = False
        testTiles = copy.deepcopy(self.tiles)
        testTiles.extend(self.pongTiles)
        testTiles.extend(self.kongTiles)
        testTiles.extend(self.concealedKongTiles)
        testTiles = self.removeGhost(testTiles)
        for tile in testTiles:
            if tile in HONOR_TILES_SET:
                hasFlowerTile = True
            type = getTileType(tile)
            if not useType and type not in HONOR_TILES_SET and type not in FLOWER_TILES_SET:
                useType = type
                continue
            if type != useType and tile not in HONOR_TILES_SET and tile not in FLOWER_TILES_SET:
                return False
        return hasFlowerTile

    def isPongHu(self):
        '''碰碰胡'''
        if not self.tile2num:
            return True
        nocount = 0
        tmpghostcount = self.getGhostCount()
        onecount = self.tile2num.values().count(MIN_REPEAT_COUNT)
        twocount = self.tile2num.values().count(EYE_NUM)

        if twocount >= 1:
            nocount += (twocount - 1)  # 补2张（2-》3）
            nocount += 2 * onecount  # 补单张（1-》3）
        else:
            nocount += 2 * (onecount - 1)  # 补单张 （1-》3）
            nocount += 1  # 补眼 （1-》2）

        if tmpghostcount >= nocount:
            return True
        return False

    def isPingHu(self):
        if self.isWaitingHu():
            return True
        return False

    def getTilesOne(self, isdrop=True):
        '''获取所有牌（已去重）'''
        testTiles = copy.deepcopy(self.tiles)
        testTiles.extend(self.pongTiles)
        testTiles.extend(self.kongTiles)
        testTiles.extend(self.concealedKongTiles)
        if isdrop:
            tmptiles = list(set(testTiles))  # 去重
            return tmptiles
        return testTiles
