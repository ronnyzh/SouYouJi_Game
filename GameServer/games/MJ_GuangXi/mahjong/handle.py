# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: game logic
"""

from common.handle_manger import HandleManger
from common.card_define import *
from common.log import *
from collections import Counter, OrderedDict

import copy


# 是否能过杠再杠
CanKongAfterPass = True


class Handel(HandleManger):

    def __init__(self, player):
        super(Handel, self).__init__(player)
        self.ActiveKongStats = None

        # 杠上开花的标记
        self.KongFlower = False
        self.BeKongFlower = None
        self.NoKongList = []

        # 是否存在过胡不胡导致不能胡
        self.isCanHu = True
        # 是否处于杠后出牌阶段
        self.afterKong = False
        self.afterDiscardTile = None
        # 连杠操作list
        self.alwaysKongs = []
        # 3笔记录
        self.threeBi = []
        # 3笔成立位置
        self.threeBiSide = -1
        # 封胡
        self.fengHu = False

    def isCheckHu(self):
        '''
        确认是否胡，修改胡规则则重写此方法
        '''
        if self.fengHu:
            return False
        if self.isWaitingHu():  # 33332
            return True
        if self.isSevenPair():  # 七对
            return True
        if self.isThirteenOrphans():  # 十三幺
            return True
        return False

    def onPong(self, tiles):
        '''
        进行碰操作
        '''
        result = super(Handel, self).onPong(tiles)
        if result and self.tmpSide >= 0:
            self.threeBi.append(self.tmpSide)
        return result

    def onOthersKong(self, tiles):
        '''
        进行碰操作
        '''
        result = super(Handel, self).onOthersKong(tiles)
        if result and self.tmpSide >= 0:
            self.threeBi.append(self.tmpSide)
        return result

    ###########doOnAction##############
    def doOnAction(self, action, tiles):
        if action in [OTHERS_KONG, SELF_KONG, CONCEALED_KONG]:
            self.ActiveKongStats = action

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
                    self.afterKong = True

                    if action == OTHERS_KONG:
                        self.alwaysKongs.append(self.tmpSide)
                    else:
                        self.alwaysKongs.append(action)

                    if action == OTHERS_KONG:
                        self.BeKongFlower = self.tmpSide

            if action == [PONG, OTHERS_KONG, SELF_KONG, CONCEALED_KONG]:
                self.isCanHu = True
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
        self.player.logger(u'[try getAllowAction] [%s] 过胡不能胡[%s]' % (self.player.__str__(), self.isCanHu))
        for action in allowActions:
            if not self.isCanHu and action == HU:
                self.player.logger(u'[try getAllowAction] [%s] 过胡不能胡' % (self.player.__str__()))
                continue
            tiles = action2callback[action]()

            if self.NoKongList and action == SELF_KONG:  # 过杠不杠（三张牌碰后不能再杠）
                for p in self.NoKongList:
                    if p in tiles:
                        tiles.remove(p)

            if tiles:
                actionNtiles[action] = tiles

                if action == HU:
                    self.player.logger(u'[try getAllowAction] [%s] 过胡不能胡标记设立' % (self.player.__str__()))
                    self.isCanHu = False

        if not CanKongAfterPass and actionNtiles.has_key(PONG) and actionNtiles[PONG] and actionNtiles.has_key(
                OTHERS_KONG) and actionNtiles[OTHERS_KONG]:
            for v in actionNtiles[PONG]:
                if v in actionNtiles[OTHERS_KONG]:
                    self.NoKongList.append(v)

        log(u'[try getAllowAction] allowActions[%s] actionNtiles[%s]' % (allowActions, actionNtiles), LOG_LEVEL_RELEASE)
        return actionNtiles

    def isOneColour(self, **kwargs):
        return super(Handel, self).isOneColour()

    def isSevenPair(self, **kwargs):  # 七对子
        if self.isClean():
            notPairCount = 0
            # print 'tile2num',self.tile2num
            for tile, count in self.tile2num.items():
                isOne = count % 2
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

    def isBigSeverPair(self, **kwargs):
        x = 0
        for _iter in self.tile2num.values():
            if _iter == 4:
                x += 1
        return x >= 1

    def isSuperBigSeverPair(self, **kwargs):
        x = 0
        for _iter in self.tile2num.values():
            if _iter == 4:
                x += 1
        return x >= 2

    def isThirteenOrphans(self, **kwargs):  # 十三幺
        if not self.isClean():
            return False
        ThirteenOrphansList = ['a1', 'a9', 'b1', 'b9', 'c1', 'c9']
        ThirteenOrphansList.extend(HONOR_TILES)
        return set(ThirteenOrphansList) == set(self.tiles)

    def isAllHelpHu(self, **kwargs):
        if len(self.tiles) <= 2 and not self.concealedKongTiles and not self.lastTile:
            return True
        return False

    def isAllPong(self, **kwargs):  # 碰碰胡
        return super(Handel, self).isAllPong()

    def isCleanRoom(self, **kwargs):  # 门清
        if self.pongTiles or self.othersKongTiles or self.selfKongTiles:
            return False
        return True

    def isPingHu(self, **kwargs):
        return True

    def isTianHu(self, **kwargs):
        '''
        天胡
        庄家起手牌直接胡牌称为天胡
        '''
        if self.player == self.player.game.dealer and not self.isDiscard:
            return True
        return False

    def isDiHu(self, **kwargs):
        '''地胡'''
        if self.player != self.player.game.dealer and not self.isDiscard:
            return True
        return False

    def isPeopleHu(self, **kwargs):
        '''
        人胡(64番)
        庄家打出第一张牌后，闲家胡这张牌为人胡
        思路:
        1.胡的牌是庄家第一张打出的牌
        2.胡的玩家是庄家
        3.自己未做任何操作
        '''
        game = self.player.game
        dealer = game.dealer
        if dealer.chair == self.player.chair:
            return False
        if self.isDiscard:
            return False
        if self.tmpSide != dealer.chair:
            return False
        if len(dealer.handleMgr.discardTiles) == 1 and self.tmpTile == dealer.handleMgr.discardTiles[0]:
            return True
        return False

    def isAllHelpPaoHu(self, beHuPlayer, **kwargs):
        '''
        全求炮
        放炮玩家手牌为全求人听牌为全球炮
        '''
        if not self.lastTile and beHuPlayer.handleMgr.isAllHelpHu(beHuPlayer=beHuPlayer, **kwargs):
            return True
        return False

    def isSeaPaoHu(self, **kwargs):
        '''
        海底炮
        玩家摸上最后一张牌后，打出任意牌被其他玩家胡牌为海底炮
        '''
        if not self.lastTile and self.player.game.dealMgr.isDraw():
            return True
        return False

    def isKongDiscardHu(self, beHuPlayer, **kwargs):
        '''
        杠上炮
        杠牌后打出的第一张牌被其他玩家胡牌为杠上炮
        '''
        if not self.lastTile and beHuPlayer.handleMgr.alwaysKongs:
            return True
        return False

    def isQiangKongHu(self, **kwargs):
        return self.player.game.beGrabKongHuPlayer

    def isKongFlowerHu(self, **kwargs):
        return self.KongFlower

    def isSeaHu(self, **kwargs):
        if self.lastTile and self.player.game.dealMgr.isDraw():
            return True
        return False

    def getHuScore(self):
        CleanRoom = u'门清'
        TianHu = u'天胡'
        DiHu = u'地胡'
        PeopleHu = u'人胡'
        AllHelpPaoHu = u'全求炮'
        SeaPaoHu = u'海底炮'
        KongDiscardHu = u'杠上炮'
        QiangKongHu = u'抢杠胡'
        KongFlowerHu = u'杠上开花'
        SeaHu = u'海底捞月'

        PingHu = u'平胡'
        OneColourHu = u'清一色'
        PongHu = u'碰碰胡'
        AllHelpHu = u'全求人'
        SeverPair = u'七小对'
        BigSeverPair = u'七大对'
        SuperBigSeverPair = u'豪华七大对'
        ThirteenOrphans = u'十三幺'

        side, _, _ = self.getHuData()
        if side == self.player.chair:
            beHuPlayer = None
        else:
            beHuPlayer = self.player.game.players[side]

        if beHuPlayer:
            if self.isGrabKongSide == -1:
                # 吃胡
                huType = 0
            else:
                # 抢杠胡
                huType = 2
        else:
            # 自摸
            huType = 1

        DescMap = OrderedDict()
        DescMap[ThirteenOrphans] = {'func': self.isThirteenOrphans, 'fan': [48, 32, 32], 'ignore': [PingHu, CleanRoom]}
        DescMap[SuperBigSeverPair] = {'func': self.isSuperBigSeverPair, 'fan': [48, 32, 32],
                                      'ignore': [BigSeverPair, SeverPair, CleanRoom]}
        DescMap[BigSeverPair] = {'func': self.isBigSeverPair, 'fan': [24, 16, 16], 'ignore': [SeverPair, CleanRoom]}
        DescMap[SeverPair] = {'func': self.isSevenPair, 'fan': [12, 8, 8], 'ignore': [CleanRoom]}
        if huType != 1:
            DescMap[AllHelpHu] = {'func': self.isAllHelpHu, 'fan': [18, 0, 0], 'ignore': [PongHu, PingHu]}
        DescMap[PongHu] = {'func': self.isAllPong, 'fan': [9, 6, 6], 'ignore': [PingHu]}
        DescMap[OneColourHu] = {'func': self.isOneColour, 'fan': [9, 6, 6], 'ignore': [PingHu]}
        DescMap[PingHu] = {'func': self.isPingHu, 'fan': [2, 3, 3], 'ignore': []}

        if huType == 1:
            DescMap[CleanRoom] = {'func': self.isCleanRoom, 'double': 4 / 3}
            DescMap[TianHu] = {'func': self.isTianHu, 'double': 2}
            DescMap[DiHu] = {'func': self.isDiHu, 'double': 2}
            DescMap[KongFlowerHu] = {'func': self.isKongFlowerHu, 'double': 1 + len(self.alwaysKongs)}
            DescMap[SeaHu] = {'func': self.isSeaHu, 'double': 2}
        elif huType == 0:
            if self.player.game.chiHuCountClean:
                DescMap[CleanRoom] = {'func': self.isCleanRoom, 'double': 4 / 3}
            DescMap[PeopleHu] = {'func': self.isPeopleHu, 'double': 2, 'min': 9}
            DescMap[AllHelpPaoHu] = {'func': self.isAllHelpPaoHu, 'double': 2, 'min': 9}
            DescMap[SeaPaoHu] = {'func': self.isSeaPaoHu, 'double': 2, 'min': 9}
            DescMap[KongDiscardHu] = {'func': self.isKongDiscardHu, 'double': 1 + len(beHuPlayer.handleMgr.alwaysKongs),
                                      'min': 9}
        elif huType == 2:
            DescMap[CleanRoom] = {'func': self.isCleanRoom, 'double': 4 / 3}
            DescMap[QiangKongHu] = {'func': self.isQiangKongHu, 'double': len(beHuPlayer.handleMgr.alwaysKongs)}

        kwargs = dict(
            beHuPlayer=beHuPlayer,
        )

        ignoreDesc = []
        descList = []
        totalScore = 0
        minScore = 0
        self.player.logger(u'---------------------------------- [getHuScore] ----------------------------------')
        for _desc, _data in DescMap.items():
            _func = _data['func']
            if _desc in ignoreDesc:
                continue
            if _func(**kwargs):
                self.player.logger(u'[getHuScore] [start] totalScore[%s] minScore[%s]' % (totalScore, minScore))
                self.player.logger(u'[getHuScore] _desc[%s] 通过 %s' % (_desc, _data))
                if 'fan' in _data:
                    totalScore += _data['fan'][huType]
                    # descList.append('%s+%s' % (_desc, _data['fan'][huType]))
                    descList.append('%s' % (_desc))
                if 'double' in _data:
                    if _desc == CleanRoom:
                        totalScore = totalScore * 4 / 3
                        # descList.append('%s*%s' % (_desc, '4/3'))
                        descList.append('%s' % (_desc))
                    else:
                        totalScore *= _data['double']
                        # descList.append('%s*%s' % (_desc, _data['double']))
                        descList.append('%s' % (_desc))
                minScore = max(minScore, _data.get('min', 0))
                # descList.append(_desc)
                ignoreDesc.extend(_data.get('ignore', []))

                self.player.logger(u'[getHuScore] [end] totalScore[%s] minScore[%s]' % (totalScore, minScore))
        if self.alwaysKongs:
            descList.append(u'连杠X%s' % (len(self.alwaysKongs) - 1))
        if beHuPlayer and beHuPlayer.handleMgr.alwaysKongs:
            descList.append(u'连杠X%s' % (len(beHuPlayer.handleMgr.alwaysKongs) - 1))
        return descList, max(totalScore, minScore)
