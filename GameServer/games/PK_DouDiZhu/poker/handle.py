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
from ddz_arith import *
from consts import *
import fightTheLandlord_poker_pb2

import copy


class Handel(HandleManger):
    def __init__(self, player):
        super(Handel, self).__init__(player)

    def resetDataPerGame(self):
        super(Handel, self).resetDataPerGame()
        self.count2cards = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
        self.autoDiscard = []

    def doDiscard(self, cardList):
        '''
        进行出牌操作
        '''
        log(u'[doDiscard] cardList[%s]' % (cardList), LOG_LEVEL_RELEASE)
        self.player.logger(u'[doDiscard] cardList[%s]' % (cardList))
        if not cardList:
            log(u'[doDiscard][error] no cardList', LOG_LEVEL_RELEASE)
            return []
        _len = len(cardList)
        cards = cardList[0].split(',')
        for card in cards:
            if card not in self.cards:
                log(u'[doDiscard][error] card[%s] not in cards[%s]' % (card, self.cards), LOG_LEVEL_RELEASE)
                return []
        newCards = cards[:]
        useWildCard = []
        if _len == 2:
            substituteCards = cardList[1].split(',')
            wildCard = self.wildCardList[0]
            log(u'[doDiscard] substituteCards[%s] wildCard[%s]' % (substituteCards, wildCard), LOG_LEVEL_RELEASE)
            self.player.logger(u'[doDiscard] substituteCards[%s] wildCard[%s]' % (substituteCards, wildCard))
            for c in cards:
                if c[0] == wildCard:
                    newCards.remove(c)
                    useWildCard.append(c)
            newCards.extend(substituteCards)
        cardPattern = self.isValidDiscard(newCards[:], useWildCard)
        if cardPattern:
            self.dealDiscardData(cards)
            self.player.lastDiscard = cardList
            if self.isDisRocket(cardPattern):
                self.canAutoDiscard()
            return newCards
        return []

    def dealDiscardData(self, cards):
        super(Handel, self).dealDiscardData(cards)
        self.player.game.addCardList(cards)

    def isValidDiscard(self, cards, useWildCard=[]):
        log(u'[isValidDiscard] cards[%s]' % (cards), LOG_LEVEL_RELEASE)
        self.player.logger(u'[isValidDiscard] cards[%s]' % (cards))
        values = [card2val_map[card[0]] for card in cards]
        cardIdList = []
        # for val in set(values):
        # valCount = values.count(val)
        # tempList = []
        # for i in xrange(valCount):
        # if val in [16,17]:
        # cardId = (val-16)+52
        # else:
        # cardId = (val-3)*4+i
        # tempList.append(cardId)
        # cardIdList.extend(tempList)
        log(u'[isValidDiscard] values[%s] cardIdList[%s]' % (values, cardIdList), LOG_LEVEL_RELEASE)
        self.player.logger(u'[isValidDiscard] values[%s] cardIdList[%s]' % (values, cardIdList))
        # cardPattern = CardsModelFactory(cardIdList)
        cardPattern = CardsModelFactory(values, useWildCard)
        if cardPattern.is_invalid():
            log(u'[isValidDiscard] invalid cardPattern', LOG_LEVEL_RELEASE)
            return False

        # if self.player.game.lastDiscardSide == self.player.chair:
        # self.player.game.lastDiscard = []
        lastDiscard = self.player.game.lastDiscard
        log(u'[isValidDiscard] lastDiscard[%s] lastDiscardSide[%s]' %
            (lastDiscard, self.player.game.lastDiscardSide), LOG_LEVEL_RELEASE)
        self.player.logger(u'[isValidDiscard] lastDiscard[%s] lastDiscardSide[%s]' %
                           (lastDiscard, self.player.game.lastDiscardSide))
        if not lastDiscard or (lastDiscard and cardPattern > lastDiscard):
            self.player.game.lastDiscard = cardPattern
            self.player.game.lastDiscardSide = self.player.chair
            if cardPattern.get_pattern() >= HARD_BOMB_PATTERN:
                self.player.game.dealBombData(self.player)
            log(u'[isValidDiscard] lastDiscard[%s] lastDiscardSide[%s]' %
                (cardPattern.get_pattern(), self.player.game.lastDiscardSide), LOG_LEVEL_RELEASE)
            self.player.logger(u'[isValidDiscard] lastDiscard[%s] lastDiscardSide[%s]' %
                               (cardPattern.get_pattern(), self.player.game.lastDiscardSide))
            return cardPattern
        return False

    def isDisRocket(self, cardPattern):
        log(u'[isDisRocket] cardPattern[%s]' % (cardPattern), LOG_LEVEL_RELEASE)
        self.player.logger(u'[isDisRocket] cardPattern[%s]' % (cardPattern))
        if not cardPattern:
            return False
        return cardPattern.get_pattern() == ROCKET_PATTERN

    def canAutoDiscard(self):
        leftCards = self.cards[:]
        tmpWildCards = self.getWildCards()
        values = [card2val_map[card[0]] for card in leftCards if card not in tmpWildCards]
        log(u'[canAutoDiscard] leftCards[%s] tmpWildCards[%s] values[%s]' %
            (leftCards, tmpWildCards, values), LOG_LEVEL_RELEASE)
        self.player.logger(u'[canAutoDiscard] leftCards[%s] tmpWildCards[%s] values[%s]' %
                           (leftCards, tmpWildCards, values))
        usdWilds = []
        if tmpWildCards:
            wildVal = self.getWildVal()
            tmpWildVals = [wildVal] * len(tmpWildCards)
            usdWildVals = useWildCard(values, tmpWildVals)
            if not usdWildVals:
                return False
            for val in usdWildVals:
                card = val2card_map[val]
                cardStr = card + 'w'
                usdWilds.append(cardStr)
        else:
            cardPattern = CardsModelFactory(values, [])
            log(u'[canAutoDiscard] cardPattern[%s]' % (cardPattern), LOG_LEVEL_RELEASE)
            self.player.logger(u'[canAutoDiscard] cardPattern[%s]' % (cardPattern))

            if cardPattern.is_invalid() or cardPattern.get_pattern() in PATTERN_QUADRUPLE:
                log(u'[canAutoDiscard] invalid cardPattern', LOG_LEVEL_RELEASE)
                return False
        self.dealAutoDiscard(leftCards, usdWilds)
        self.player.isAutoDiscard = True
        return True

    def dealAutoDiscard(self, cards, usdWilds):
        cards = self.sortedCards(cards)
        log(u'[dealAutoDiscard] cards[%s] usdWilds[%s]' % (cards, usdWilds), LOG_LEVEL_RELEASE)
        self.player.logger(u'[dealAutoDiscard] cards[%s] usdWilds[%s]' % (cards, usdWilds))
        cardStr = ','.join(cards)
        self.autoDiscard.append(cardStr)
        if usdWilds:
            wildStr = ','.join(usdWilds)
            self.autoDiscard.append(wildStr)
        log(u'[dealAutoDiscard] autoDiscard[%s]' % (self.autoDiscard), LOG_LEVEL_RELEASE)
        self.player.logger(u'[dealAutoDiscard] autoDiscard[%s]' % (self.autoDiscard))

    def sortedCards(self, cards):
        valStr2Count = {}
        # cards = sorted(cards, key=lambda x:x[1] , reverse = True)
        log(u'[sortedCards] cards[%s]' % (cards), LOG_LEVEL_RELEASE)
        for c in cards:
            valStr = c[0]
            if valStr2Count.has_key(valStr):
                valStr2Count[valStr] += 1
            else:
                valStr2Count[valStr] = 1
        log(u'[sortedCards] valStr2Count[%s]' % (valStr2Count), LOG_LEVEL_RELEASE)
        count2valStr = {1: [], 2: [], 3: [], 4: []}
        for key, val in valStr2Count.items():
            count2valStr[val].append(key)
        valStrSetList = []
        for i in [4, 3, 2, 1]:
            valStrs = count2valStr[i]
            valStrs = sorted(valStrs, key=lambda x: card2val_map[x], reverse=True)
            log(u'[sortedCards] i[%s] valStrs[%s]' % (i, valStrs), LOG_LEVEL_RELEASE)
            valStrSetList.extend(valStrs)
        log(u'[sortedCards] valStrSetList[%s]' % (valStrSetList), LOG_LEVEL_RELEASE)
        newCards = []
        for valStr in valStrSetList:
            valStrCards = [card for card in cards if card[0] == valStr]
            newCards.extend(valStrCards)
        log(u'[sortedCards] newCards[%s]' % (newCards), LOG_LEVEL_RELEASE)
        return newCards

    def getAutoDiscard(self):
        return self.autoDiscard

    def setWildCard(self, cardList):  # 设置万能牌
        cardVal = cardList[0][0]
        self.wildCardList = [cardVal]
        log(u'[setWildCard] wildCardList[%s] cardList[%s]' \
            % (self.wildCardList, cardList), LOG_LEVEL_RELEASE)

    def getWildCards(self):
        wildCards = [c for c in self.cards if c[0] in self.wildCardList]
        log(u'[getWildCards] wildCards[%s]' % (wildCards), LOG_LEVEL_RELEASE)
        return wildCards

    def getWildVal(self):
        wildVal = card2val_map[self.wildCardList[0]]
        log(u'[getWildVal] wildVal[%s]' % (wildVal), LOG_LEVEL_RELEASE)
        return wildVal

    def dealHandCards(self):
        myCards = self.cards[:]
        tmpWildCards = self.getWildCards()
        cardVals = [card2val_map[card[0]] for card in myCards if card not in tmpWildCards]
        cardValsList = list(set(cardVals))
        log(u'[dealHandCards] myCards[%s] cardVals[%s] cardValsList[%s]' % (myCards, cardVals, cardValsList),
            LOG_LEVEL_RELEASE)

        self.count2cards = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
        self.count2cards[0] = cardVals
        self.count2cards[1] = cardValsList
        self.count2cards[5] = tmpWildCards
        for val in set(cardVals):
            _count = cardVals.count(val)
            if _count > 4 or _count <= 0:
                log(u'[dealHandCards] _count[%s]' % (_count), LOG_LEVEL_RELEASE)
                return
            else:
                for i in xrange(2, _count + 1):
                    self.count2cards[i].append(val)
        log(u'[dealHandCards] count2cards[%s]' % (self.count2cards), LOG_LEVEL_RELEASE)

    def isExistBigger(self, lastDiscard):
        log(u'[isExistBigger] lastDiscard[%s]' % (lastDiscard), LOG_LEVEL_RELEASE)
        if not lastDiscard:
            return True

        lastPattern = lastDiscard.get_pattern()
        log(u'[isExistBigger] lastPattern[%s]' % (lastPattern), LOG_LEVEL_RELEASE)
        if lastPattern == ROCKET_PATTERN:
            return False

        self.dealHandCards()

        isHaveRocket = self.haveRocket()
        maxBombTup = self.haveBomb()
        log(u'[isExistBigger] isHaveRocket[%s] maxBombTup[%s]' % (isHaveRocket, maxBombTup), LOG_LEVEL_RELEASE)

        if isHaveRocket:
            return True
        if maxBombTup:
            if maxBombTup == MIX_BOMB_PATTERN:
                return True
            return CardsModelFactory(maxBombTup[0], maxBombTup[1]) > lastDiscard
        isSingle = isinstance(lastDiscard, SingleJoint)
        isPair = isinstance(lastDiscard, PairJoint)
        isTriple = isinstance(lastDiscard, TripleJoint)
        isAerSingle = isinstance(lastDiscard, AerocraftWithSingle)
        isAerPair = isinstance(lastDiscard, AerocraftWithPair)
        log(u'[isExistBigger] isSingle[%s] isPair[%s] isTriple[%s] isAerSingle[%s] isAerPair[%s]' \
            % (isSingle, isPair, isTriple, isAerSingle, isAerPair), LOG_LEVEL_RELEASE)
        if isSingle or isPair or isTriple or isAerSingle or isAerPair:
            jointCount = lastDiscard.get_count()
            jointValue = lastDiscard.get_value()
            isUseWild = lastDiscard.get_use_wild()
            if isSingle:
                return self.checkJoint(1, jointValue, jointCount) or \
                       self.dealUseWild(1, jointValue, jointCount, isUseWild)
            if isPair:
                return self.checkJoint(2, jointValue, jointCount) or \
                       self.dealUseWild(2, jointValue, jointCount, isUseWild)

            isJoint = self.checkJoint(3, jointValue, jointCount) or \
                      self.dealUseWild(3, jointValue, jointCount, isUseWild)
            if isTriple:
                return isJoint
            if isAerSingle:
                lenCards = len(self.cards)
                return isJoint and lenCards >= jointCount * 4
            if isAerPair:
                val2SetList = self.count2cards[2]
                lenPair = len(val2SetList)
                return isJoint and lenPair >= jointCount * 2

    def haveRocket(self):
        valList = self.count2cards[1]
        log(u'[haveRocket] valList[%s]' % (valList), LOG_LEVEL_RELEASE)
        return LITTLE_VAL in valList and BIG_VAL in valList

    def haveBomb(self):
        tmpWildCards = self.count2cards[5]
        _lenWildCards = len(tmpWildCards)
        log(u'[haveBomb0] tmpWildCards[%s] _lenWildCards[%s]' % (tmpWildCards, _lenWildCards), LOG_LEVEL_RELEASE)
        # for i in [4,3,2,1]:
        # valSetList = self.count2cards[i]
        # valCount = _lenWildCards+i
        # log(u'[haveBomb1] valSetList[%s] valCount[%s]'%(valSetList, valCount), LOG_LEVEL_RELEASE)
        # if valSetList and valCount >= 4:
        # maxVals = self.getMaxVals(valSetList, valCount)
        # return (maxVals, tmpWildCards)
        # if _lenWildCards >= 4:
        # log(u'[haveBomb2] MIX_BOMB_PATTERN[%s]'%(MIX_BOMB_PATTERN), LOG_LEVEL_RELEASE)
        # return MIX_BOMB_PATTERN

        val4CardList = self.count2cards[4][:]
        if _lenWildCards == 4:
            wildVal = self.getWildVal()
            val4CardList.append(wildVal)
        if val4CardList:
            maxVals = self.getMaxVals(val4CardList)
            return (maxVals, [])

        val321CardList = []
        for i in [3, 2, 1]:
            valSetList = self.count2cards[i]
            valCount = _lenWildCards + i
            log(u'[haveBomb1] valSetList[%s] valCount[%s]' % (valSetList, valCount), LOG_LEVEL_RELEASE)
            if valSetList and valCount >= 4:
                val321CardList.extend(valSetList)

        if val321CardList:
            maxVals = self.getMaxVals(val321CardList)
            return (maxVals, tmpWildCards)

        return False

    def getMaxVals(self, valList, valCount=4):
        maxVal = max(valList)
        maxCardVals = [maxVal] * (valCount)
        log(u'[getMaxVals] maxCardVals[%s]' % (maxCardVals), LOG_LEVEL_RELEASE)
        return maxCardVals

    def getCurJoint(self, needValList, myValList, type):
        curJoint = []
        for val in needValList:
            vCount = myValList.count(val)
            if vCount >= type:
                curJoint.extend([val] * type)
            else:
                curJoint.extend([val] * vCount)
        lenCurJoint = len(curJoint)
        log(u'[getCurJoint] curJoint[%s] lenCurJoint[%s]' % (curJoint, lenCurJoint), LOG_LEVEL_RELEASE)
        return lenCurJoint

    def checkJoint(self, type, minVal, jointCount):
        cardList = xrange(3, 18)
        # val0CardList = self.count2cards[0]
        # val0List = [card2val_map[card[0]] for card in val0CardList]
        val0List = self.count2cards[0]
        log(u'[checkJoint0] minVal[%s] jointCount[%s] cardList[%s] val0List[%s]' \
            % (minVal, jointCount, cardList, val0List), LOG_LEVEL_RELEASE)
        valList = [c for c in cardList if c > minVal]
        _len = len(valList)
        if _len < jointCount:
            return False
        valList.sort()
        tmpWildCards = self.count2cards[5]
        _lenWildCards = len(tmpWildCards)
        log(u'[checkJoint1] valList[%s] _lenWildCards[%s]' % (valList, _lenWildCards), LOG_LEVEL_RELEASE)
        if jointCount == 1:
            for val in valList:
                if val > 15:
                    _lenWildCards = 0
                lenCurJoint = self.getCurJoint([val], val0List, type)
                if (lenCurJoint + _lenWildCards) >= jointCount * type:
                    if lenCurJoint > 0:
                        return True
                    else:
                        wildVal = self.getWildVal()
                        if wildVal in valList:
                            return True
        else:
            for val in valList:
                curMaxVal = val + jointCount - 1
                log(u'[checkJoint2] curMaxVal[%s]' % (curMaxVal), LOG_LEVEL_RELEASE)
                if curMaxVal > 14:
                    return False
                curValList = xrange(val, curMaxVal + 1)
                lenCurJoint = self.getCurJoint(curValList, val0List, type)
                if (lenCurJoint + _lenWildCards) >= jointCount * type:
                    return True
        return False

    def dealUseWild(self, type, minVal, jointCount, isUseWild):
        if not isUseWild:
            return False
        valCardList = self.count2cards[type]
        maxVal = minVal + jointCount - 1
        cardValList = xrange(minVal, maxVal + 1)
        cardValSet = set(cardValList)
        log(u'[dealUseWild] valCardList[%s] cardValList[%s]' % (valCardList, cardValList), LOG_LEVEL_RELEASE)
        self.player.logger(u'[dealUseWild] valCardList[%s] cardValList[%s]' % (valCardList, cardValList))
        if cardValList:
            return cardValSet & set(valCardList) == cardValSet
        return False

    def mustBeLandLord(self):
        '''
        在没有癞子的情况下，若是有双鬼和4个2，那么就一定叫分，3分
        :return:
        '''
        self.player.logger(u'[mustBeLandLord] cards => %s' % (self.cards))
        cards = set(self.cards)
        targetCards = set(JOKER_LIST)
        targetCardsTwo = set()
        for col in color_set:
            targetCardsTwo.add('2' + col)
        diffCard = set(cards) & set(targetCards)
        diffCardTwo = set(cards) & set(targetCardsTwo)
        if diffCard == set(targetCards) or diffCardTwo == set(targetCardsTwo):
            return True
        return False

    def _addCards(self, cards=None):
        '''
        添加一组牌
        '''
        if not cards:
            cards = []
        newCards = set(cards)
        oldCards = set(self.cards)
        if (newCards & oldCards) == oldCards:
            return
        self.cards.extend(cards)
        log(u'[_addCards] cards[%s] self.cards[%s]' % (cards, self.cards), LOG_LEVEL_RELEASE)
        self.player.logger(u'[_addCards] cards[%s] self.cards[%s]' % (cards, self.cards))

    def doSortMyCards(self):
        self.cards = self.cardSort(self.cards)

    def getSmallestCards(self):
        self.player.logger(u'[getSmallestCards] %s' % self.cards)
        return self.cards[-1]
