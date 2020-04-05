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

import copy


class Handel(HandleManger):
    def __init__(self, player):
        super(Handel, self).__init__(player)
        self.specialTileList = []  # 摸到的花牌
        self.isPlayTile = False  # 是否已出牌
        self.isFirstDiscard = None
        self.HuList = []  # 已经胡的牌

    def onHu(self, tiles):
        super(Handel, self).onHu(tiles)
        self.player.isFreeze = True
        if self.player.chair not in self.player.game.huChairs:
            self.player.game.huPlayerCount += 1
            self.player.game.huChairs.append(self.player.chair)
        self.player.game.refreshScore(self.player)
        huTile = self.getHuData()[1]
        self.HuList.append(huTile)
        self._rmTile(huTile)

    def isHaiDi(self):
        '''海底'''
        tmp = len(self.player.game.dealMgr.tiles)
        return False if tmp else True

    def rootCount(self):
        '''根'''
        count = (len(self.kongTiles) + len(self.concealedKongTiles))
        count += len(self.getConcealedKongList())
        return count

    def isJinGou(self):
        '''金钩胡'''
        testTiles = copy.deepcopy(self.tiles)
        if len(testTiles) == 2:
            return True
        return False

    def checkRate(self):
        '''查最大番数'''
        desc = []
        game = self.player.game
        rc = self.rootCount()
        if self.isEighteenGod():
            if self.isOneColour():
                desc.append('清十八罗汉'.decode('utf-8'))
                rate = 8
            else:
                desc.append('十八罗汉'.decode('utf-8'))
                rate = 6
            rc -= 4
        elif game.isCanHu_qinglongqidui and self.isOneColour() and self.isSuperSevenPair():
            # desc.append('清一色豪华七对子'.decode('utf-8'))
            desc.append('清龙七对'.decode('utf-8'))
            rate = 5
            rc -= 1
        elif game.isCanHu_jiangqidui and self.isJiangQiDui():
            desc.append('将七对'.decode('utf-8'))
            rate = 4
        elif game.isCanHu_qingqidui and self.isOneColour() and self.isSevenPair():
            # desc.append('清一色七对子'.decode('utf-8'))
            desc.append('清七对'.decode('utf-8'))
            rate = 4
        elif self.isOneColour() and self.isJinGou():
            desc.append('清金钩钓'.decode('utf-8'))
            rate = 4
        elif game.isCanHu_qingpeng and self.isOneColour() and self.isAllPong():
            # desc.append('清一色碰碰碰胡'.decode('utf-8'))
            desc.append('清碰'.decode('utf-8'))
            rate = 3
        elif game.isCanHu_jiangdui and self.player.game.j19 and self.isJiangDui():
            desc.append('将对'.decode('utf-8'))
            rate = 3
        elif game.isCanHu_quanyaojiu and self.player.game.j19 and self.isQuanYaojiu():
            desc.append('全幺九'.decode('utf-8'))
            rate = 3
        elif game.isCanHu_longqidui and self.isSuperSevenPair():
            # desc.append('豪华七对子'.decode('utf-8'))
            desc.append('龙七对'.decode('utf-8'))
            rate = 3
            rc -= 1
        elif game.isCanHu_qingyise and self.isOneColour():
            desc.append('清一色'.decode('utf-8'))
            rate = 2
        elif game.isCanHu_qidui and self.isSevenPair():
            desc.append('七对'.decode('utf-8'))
            rate = 1
        elif game.isCanHu_penghu and self.isAllPong():
            '''金钩'''
            if self.isJinGou():
                desc.append('金钩钓'.decode('utf-8'))
                rate = 2
            else:
                desc.append('碰碰胡'.decode('utf-8'))
                rate = 1
        elif game.isCanHu_menqing and self.player.game.mqzz and self.isClean():
            desc.append('门清'.decode('utf-8'))
            rate = 1
        elif game.isCanHu_zhongzhang and self.player.game.mqzz and self.isMiddleTiles():
            desc.append('中张'.decode('utf-8'))
            rate = 1
        else:
            desc.append('平胡'.decode('utf-8'))
            rate = 0
        if rc > 0:
            gen = '根*{}'.format(rc).decode('utf-8')
            desc.append(gen)
            rate += rc
        return desc, rate

    def checkColor(self):
        '''查花色'''
        if self.isOneColour():
            return 1
        typeList = []
        testTiles = copy.deepcopy(self.tiles)
        testTiles.extend(self.pongTiles)
        testTiles.extend(self.kongTiles)
        testTiles.extend(self.concealedKongTiles)
        for tile in testTiles:
            type = getTileType(tile)
            if type not in typeList:
                typeList.append(type)
        return len(typeList)

    def isPig(self):
        '''查花猪'''
        return self.checkColor() == 3

    def isMiddleTiles(self):
        '''中张'''
        testTiles = copy.deepcopy(self.tiles)
        testTiles.extend(self.pongTiles)
        testTiles.extend(self.kongTiles)
        testTiles.extend(self.concealedKongTiles)
        for i in testTiles:
            num = getTilePoints(i)
            if num == 1 or num == 9:
                return False
        return True

    def isJiangDui(self):
        '''将对'''
        if self.isAllPong():
            testTiles = copy.deepcopy(self.tiles)
            testTiles.extend(self.pongTiles)
            testTiles.extend(self.kongTiles)
            testTiles.extend(self.concealedKongTiles)
            for i in testTiles:
                num = getTilePoints(i)
                if num in [1, 3, 4, 6, 7, 9]:
                    return False
            return True
        return False

    def isQuanYaojiu(self):
        '''全幺九'''
        if self.isSevenPair():
            return False
        for i in self.pongTiles:
            num = getTilePoints(i)
            if num not in [1, 9]:
                return False
        for i in self.kongTiles:
            num = getTilePoints(i)
            if num not in [1, 9]:
                return False
        for i in self.concealedKongTiles:
            num = getTilePoints(i)
            if num not in [1, 9]:
                return False
        for i in self.tripleTiles:
            for j in i:
                num = int(j[1])
                flag = False
                if num in [1, 9]:
                    flag = True
                if not flag:
                    return False
        if self.eye and int(self.eye[1]) not in [1, 9]:
            return False
        return True

    def isJiangQiDui(self):
        '''将七对'''
        if self.isSuperSevenPair():
            testTiles = copy.deepcopy(self.tiles)
            testTiles.extend(self.pongTiles)
            testTiles.extend(self.kongTiles)
            testTiles.extend(self.concealedKongTiles)
            for i in testTiles:
                num = getTilePoints(i)
                if num in [1, 3, 4, 6, 7, 9]:
                    return False
            return True
        return False

    def isEighteenGod(self):
        '''十八罗汉'''
        testTiles = copy.deepcopy(self.tiles)
        if len(testTiles) != 2:
            return False
        if len(self.concealedKongTiles) + len(self.kongTiles) != 4:
            return False
        return True

    def discard(self, tile):
        '''
        出牌
        '''
        super(Handel, self).discard(tile)
        if self.isFirstDiscard == None:
            self.isFirstDiscard = True
        elif self.isFirstDiscard == True:
            self.isFirstDiscard = False

    def isCheckHu(self):
        '''是否能胡'''
        testTiles = copy.deepcopy(self.tiles)
        testTiles.extend(self.pongTiles)
        testTiles.extend(self.kongTiles)
        testTiles.extend(self.concealedKongTiles)
        for tile in testTiles:
            type = getTileType(tile)
            if type == self.player.colorSet:
                return False
        if self.checkColor() > 2:
            return False
        if self.isWaitingHu():  # 33332
            return True
        if self.isSevenPair():  # 七对
            return True
        return False

    def getAllowActionNTiles(self, allowActions=()):
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
            if tiles:
                actionNtiles[action] = tiles
        log(u'[try getAllowAction] allowActions[%s] actionNtiles[%s]' % (allowActions, actionNtiles), LOG_LEVEL_RELEASE)
        return actionNtiles

    def getPongList(self):
        if self.player.isFreeze:
            return []
        if getTileType(self.tmpTile) == self.player.colorSet:
            return []
        if self.tmpTile == self.ghost or self.tmpTile in self.ghostList:
            return []
        if self.tmpTile and self.tiles.count(self.tmpTile) >= EYE_NUM:
            return [self.tmpTile]
        return []

    def checkAfterDoingReadyHands(self, rmTiles, msg='未知'):
        self.player.logger(u'[checkAfterDoingReadyHands] tiles=>%s kongTiles=>%s concealedKongTiles=>%s' %
                           (self.tiles, self.kongTiles, self.concealedKongTiles))
        if self.lastTile:
            self._rmTile(self.lastTile)
            l_ReadyHands = self.player.getReadyHands(self.player.game.dealMgr.getTryReadyHandTiles())
            self._addTiles([self.lastTile])
        else:
            l_ReadyHands = self.player.getReadyHands(self.player.game.dealMgr.getTryReadyHandTiles())
        self._rmTiles(rmTiles)
        tile = rmTiles[0]
        if len(rmTiles) == TRIPLET_NUM:  # 接杠
            self.othersKongTiles.append([self.tmpSide, tile])
            self.kongTiles.append(tile)
        elif len(rmTiles) == MAX_REPEAT_COUNT:  # 暗杠
            self.concealedKongTiles.append(tile)
        else:  # 碰杠
            self.kongTiles.append(tile)

        self.readyHandList = []
        r_ReadyHands = self.player.getReadyHands(self.player.game.dealMgr.getTryReadyHandTiles())

        self._addTiles(rmTiles)
        if len(rmTiles) == TRIPLET_NUM:  # 接杠
            self.othersKongTiles.remove([self.tmpSide, tile])
            self.kongTiles.remove(tile)
        elif len(rmTiles) == MAX_REPEAT_COUNT:  # 暗杠
            self.concealedKongTiles.remove(tile)
        else:  # 碰杠
            self.kongTiles.remove(tile)

        self.readyHandList = []
        self.player.logger(u'[checkAfterDoingReadyHands] msg=>[%s] rmTiles=> %s' % (msg, rmTiles))
        self.player.logger(u'[checkAfterDoingReadyHands] l_R=> %s r_R=> %s' % (l_ReadyHands, r_ReadyHands))
        return l_ReadyHands and r_ReadyHands and l_ReadyHands == r_ReadyHands

    def getOthersKongList(self):
        if getTileType(self.tmpTile) == self.player.colorSet:
            return []
        if self.tmpTile == self.ghost or self.tmpTile in self.ghostList:
            return []
        if self.tmpTile and self.tiles.count(self.tmpTile) >= TRIPLET_NUM:
            if not self.player.isFreeze:
                return [self.tmpTile]
            if self.checkAfterDoingReadyHands([self.tmpTile] * TRIPLET_NUM, msg='getOthersKongList'):
                return [self.tmpTile]
        return []

    def getSelfKongList(self):
        kongList = []
        for tile in self.tiles:
            if tile in self.pongTiles and getTileType(tile) != self.player.colorSet:
                if self.player.isFreeze:
                    if not self.checkAfterDoingReadyHands([tile], msg='getSelfKongList'):
                        continue
                kongList.append(tile)
        return kongList

    def getConcealedKongList(self):
        if self.lastTile:
            concealedKongList = []
            for tile, num in self.tile2num.iteritems():
                if num >= MAX_REPEAT_COUNT and getTileType(tile) != self.player.colorSet:
                    if self.player.isFreeze:
                        if not self.checkAfterDoingReadyHands([tile] * MAX_REPEAT_COUNT, msg='getConcealedKongList'):
                            continue
                    concealedKongList.append(tile)
            return concealedKongList
        return []
