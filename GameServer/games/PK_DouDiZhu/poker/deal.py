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
from common.log import log, LOG_LEVEL_RELEASE

import random
import re

GET_HOLE_CARDS = 2
GET_WILD_CARDS = 3

class DealMange(DealMgr):
    """
    发牌管理器
    """
    def __init__(self, game):
        """
        """
        super(DealMange, self).__init__(game)
        self.getHoleCards4GM = []
        self.getWildCards4GM = []

    def deal(self):
        """
        打乱牌
        """
        if not self.game.noShuffle or not self.game.cardList:
            self.shuffleCards(self.poolCards)
            log(u'[deal] poolCards[%s]'%(self.poolCards),LOG_LEVEL_RELEASE)

    def resetCards(self):
        """
        得到一副牌
        """
        cardList = self.game.cardList
        if self.game.noShuffle and cardList:
            cardPool = cardList[:]
            randomNum = random.randint(0, 53)
            log(u'[resetCards] cardPool[%s] randomNum[%s]'%(cardPool, randomNum),LOG_LEVEL_RELEASE)
            newCardPool = cardPool[randomNum-1:]
            newCardPool.extend(cardPool[:randomNum-1])
            self.poolCards = newCardPool
        else:
            self.poolCards = self.origPoolCards[:]
        log(u'[resetCards] len[%s] poolCards[%s]'%(len(self.poolCards), self.poolCards),LOG_LEVEL_RELEASE)

    def setCtrlTypes(self):
        """
        GM类型到相应记录数据方法的映射
        """
        super(DealMange, self).setCtrlTypes()
        self.ctrlTypes[GET_HOLE_CARDS] = self.onGetHoleCards4GM
        self.ctrlTypes[GET_WILD_CARDS] = self.onGetWildCards4GM

    def getWildCard(self):
        wildCard = ''
        if self.getWildCards4GM:
            wildCard = self.getWildCards4GM[0]
            self.getWildCards4GM = self.getWildCards4GM[1:]
            log(u'[getWildCard] wildCard[%s] origPoolCards[%s]'%(wildCard, self.origPoolCards),LOG_LEVEL_RELEASE)
            return wildCard

        while 1:
            wildCard = random.choice(self.origPoolCards)
            if wildCard not in JOKER_LIST:
                break
        log(u'[getWildCard] wildCard[%s] origPoolCards[%s]'%(wildCard, self.origPoolCards),LOG_LEVEL_RELEASE)
        return wildCard

    def getHoleCards(self):
        if self.getHoleCards4GM:
            self.poolCards.extend(self.getHoleCards4GM)
            self.getHoleCards4GM = []
        holeCards = self.poolCards[-3:]
        log(u'[getHoleCards] holeCards[%s] poolCards[%s]'%(holeCards, self.poolCards),LOG_LEVEL_RELEASE)
        return holeCards

    def dealGMData(self):
        if self.getHoleCards4GM:
            canUse = True
            for card in self.getHoleCards4GM:
                if self.poolCards.count(card) < self.getHoleCards4GM.count(card):
                    canUse = False
                    self.getHoleCards4GM = []
                    break
            if canUse:
                for card in self.getHoleCards4GM:
                    self.poolCards.remove(card)

        super(DealMange, self).dealGMData()

    def onGetHoleCards4GM(self, side, data):
        data = reCards.findall(data)
        self.getHoleCards4GM = data

    def onGetWildCards4GM(self, side, data):
        data = reCards.findall(data)
        self.getWildCards4GM = data


