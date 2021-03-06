module G560{
    export namespace flaw {
        export let classicUtils;
        export let utils;
        export class WildcardUtils extends fla.ClassicUtils {
            public sortCardNumFunc;
            public classicUtils;
            public numWildcard;

            constructor() {
                super();
                this.sortCardNumFunc = fla.ClassicUtils.prototype.compareCard.bind(this);
                flaw.classicUtils = new fla.ClassicUtils();
                flaw.utils = this;
            }

            setWildcard(cardId) {
                if (cardId == null) {
                    this.numWildcard = null;
                    return;
                }
                this.numWildcard = cardId.charAt(0);
            }

            getWildcardId() {
                return this.numWildcard + "w";
            }

            isWildcard(cardId) {
                return cardId.charAt(0) == this.numWildcard;
            }

            transferWildCardTo(cardId) {
                return cardId.substr(0, cardId.length - 1) + "w";
            }

            getWildCardByNum(num) {
                return fla.CONSTANTS.valueMap[num] + "w";
            }

            compareCard(card1, card2) {
                if (this.isWildcard(card1)) {
                    if (!this.isWildcard(card2))
                        return -1;
                }
                else {
                    if (this.isWildcard(card2))
                        return 1;
                }
                return flaw.classicUtils.compareCard(card1, card2);
            }

            getPatternIdList(mainList?, cardIdList?, wcValueList?) {
                if (wcValueList == null)
                    return flaw.classicUtils.getPatternIdList(mainList, cardIdList);

                var patternIdList = [];
                jx.each(mainList, function (list) {
                    patternIdList = patternIdList.concat(list);
                });
                jx.each(cardIdList, function (cardId) {
                    if (patternIdList.indexOf(cardId) == -1)
                        patternIdList.push(cardId);
                });

                return patternIdList;
            }

            getWildcardCount(cardIdList) {
                var count = 0;
                for (var i = 0; i < cardIdList.length; ++i) {
                    if (this.isWildcard(cardIdList[i]))
                        ++count;
                }
                return count;
            }

            hasWildcard(cardIdList) {
                for (var i = 0; i < cardIdList.length; ++i) {
                    if (this.isWildcard(cardIdList[i]))
                        return true;
                }
                return false;
            }

            getRepeatWCValueList(cardId, count) {
                var list = [];
                for (var i = 0; i < count; ++i) {
                    list.push(cardId);
                }
                return list;
            }

            repeatListSortFunc(list1, list2) {
                var num1 = fla.utils.getCardNumber(list1[0]);
                var num2 = fla.utils.getCardNumber(list2[0]);
                var dv = num2 - num1;
                return dv / Math.abs(dv);
            }

            // combineList(lists)
            // {
            //     var ret = [];
            //     jx.each(lists, function(list)
            //     {
            //         ret = ret.concat(list);
            //     });
            //
            //     return ret;
            // }

            analyseRepeatList(cardIdList) {
                var repeatCardLists = [[], [], [], []];
                if (cardIdList.length == 0)
                    return repeatCardLists;

                var numLast = this.getCardNumber(cardIdList[0]);
                var tmpList = [];
                jx.each(cardIdList, function (id) {
                    var numCard = this.getCardNumber(id);
                    if (numCard != numLast) {
                        if (tmpList.length == 1)
                            repeatCardLists[0].push(tmpList[0]);
                        else
                            repeatCardLists[tmpList.length - 1].push(tmpList);
                        numLast = numCard;
                        tmpList = [];
                    }
                    tmpList.push(id);
                }, this);

                if (tmpList.length == 1)
                    repeatCardLists[0].push(tmpList[0]);
                else if (tmpList.length > 1)
                    repeatCardLists[tmpList.length - 1].push(tmpList);

                return repeatCardLists;
            }

            getClassicPattern(cardIdList) {
                // var cp = fla.ClassicUtils.prototype.getCardPattern.call(this, cardIdList);
                var cp = flaw.classicUtils.getCardPattern(cardIdList);
                var type = cp.getType();
                switch(type)
                {
                    case fla.CARD_TYPE.ROCKET:
                        break;

                    case fla.CARD_TYPE.BOMB:
                        cp = flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.BOMB, cp.getCardIdList());
                        break;

                    default:
                        cp = new flaw.BaseCardPattern(type, cp.getCardIdList());//, keyValue, wcValueList, showCardIdList);
                        break;
                }

                return cp;
            }

            getCardPattern(cardIdList?, wcValueList?) {
                cardIdList = cardIdList.concat();
                cardIdList.sort(this.sortCardFunc);

                if (wcValueList != null && wcValueList.length > 0) {
                    wcValueList = wcValueList.concat();
                    jx.each(cardIdList, function (cardId, i) {
                        if (this.isWildcard(cardId))
                            cardIdList[i] = this.transferWildCardTo(wcValueList.shift());
                    }, this);
                    cardIdList.sort(this.sortCardNumFunc);
                    return this.getClassicPattern(cardIdList);
                }

                var wcCount = this.getWildcardCount(cardIdList);
                var lenCards = cardIdList.length;
                if (wcCount == 0 || lenCards == 1 || wcCount == lenCards)
                    return this.getClassicPattern(cardIdList);

                //对子
                if (lenCards == 2) {
                    return this.checkPair(cardIdList, wcCount);
                }
                //三条
                else if (lenCards == 3) {
                    return this.checkTriple(cardIdList, wcCount);
                }
                else {
                    var normalList = cardIdList.slice(wcCount);

                    //预处理牌数组数据
                    var repeatCardLists = this.analyseRepeatList(normalList);

                    var plist = [];
                    if (lenCards == 4) {
                        this.checkBomb(cardIdList, repeatCardLists, wcCount, plist);
                        this.checkTriple1(cardIdList, repeatCardLists, wcCount, plist);
                    }
                    else if (lenCards == 5) {
                        this.checkTriple2(cardIdList, repeatCardLists, wcCount, plist);
                        this.checkSequence(cardIdList, repeatCardLists, wcCount, plist);
                    }
                    else {
                        this.checkSequence(cardIdList, repeatCardLists, wcCount, plist);
                        this.checkSequenceOfPairs(cardIdList, repeatCardLists, wcCount, plist);
                        this.checkSequenceOfTriplets(cardIdList, repeatCardLists, wcCount, plist);
                        this.checkSequenceOfTriplets1(cardIdList, repeatCardLists, wcCount, plist);
                        this.checkSequenceOfTriplets2(cardIdList, repeatCardLists, wcCount, plist);
                        this.checkQuadplexSet1(cardIdList, repeatCardLists, wcCount, plist);
                        //这个版本不允许四带二
                        // this.checkQuadplexSet2(cardIdList, repeatCardLists, wcCount, plist);
                    }
                    if (plist.length > 0)
                        return plist;
                }

                return null;
            }

            checkPair(cardIdList, wcCount) {
                if (this.hasJoker(cardIdList))
                    return null;

                var id2 = cardIdList[1];
                if (wcCount == 1) {
                    var wcValue = this.transferWildCardTo(id2);
                    return [flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.PAIR, cardIdList, id2, [wcValue], [wcValue, id2])];
                }
                else if (wcCount == 2) {
                    var wcId = this.getWildcardId();
                    return [flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.PAIR, cardIdList, wcId, [wcId, wcId], [wcId, wcId])];
                }
                return null;
            }

            checkTriple(cardIdList, wcCount?) {
                if (this.hasJoker(cardIdList))
                    return null;

                var id1 = cardIdList[1];
                var id2 = cardIdList[2];
                if (wcCount > 1 || this.getCardNumber(id1) == this.getCardNumber(id2)) {
                    var showIdList = cardIdList.concat();
                    for (var i = 0; i < wcCount; ++i)
                        showIdList[i] = this.transferWildCardTo(id2);
                    return [flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET, cardIdList, id2, this.getRepeatWCValueList(id2, wcCount), showIdList)];
                }

                return null;
            }

            //三带1
            checkTriple1(cardIdList, repeatCardLists, wcCount, plist) {
                if (cardIdList.length != 4)
                    return;

                var wcId = this.getWildcardId();//cardIdList[0];
                var repeatCardList3 = repeatCardLists[2];
                var repeatCardList2 = repeatCardLists[1];
                var repeatCardList1 = repeatCardLists[0];
                if (wcCount == 1) {
                    if (repeatCardList2.length == 1) {
                        var keyValue = repeatCardList2[0][0];
                        var showIdList = repeatCardList2[0].concat();
                        var wcValue = this.transferWildCardTo(keyValue);
                        showIdList.push(wcValue);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_ONE, cardIdList, keyValue, [wcValue], showIdList));
                    }
                    else if (repeatCardList3.length == 1) {
                        // var keyValue = repeatCardList2[0][0];
                        // showIdList = repeatCardList2[0].concat();
                        // showIdList.push(this.transferWildCardTo(wcId));
                        // cardIdList = cardIdList.slice(1);
                        var showIdList = repeatCardList3[0].concat();
                        showIdList.push(wcId);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_ONE, cardIdList, null, [wcId], showIdList));
                    }
                }
                else if (wcCount == 2) {
                    if (repeatCardList2.length == 1) {
                        var keyValue = repeatCardList2[0][0];
                        var showIdList = repeatCardList2[0].concat();
                        showIdList.unshift(this.transferWildCardTo(keyValue));
                        showIdList.push(wcId);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_ONE, cardIdList, keyValue, [keyValue, wcId], showIdList));
                    }
                    else {
                        var self = this;
                        var func = function (keyValue, single) {
                            if (self.isJoker(keyValue))
                                return;

                            var targetValue = self.transferWildCardTo(keyValue);
                            var showIdList = self.getRepeatWCValueList(targetValue, 2);
                            showIdList.push(keyValue);
                            showIdList.push(single);
                            plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_ONE, cardIdList, keyValue, self.getRepeatWCValueList(keyValue, 2), showIdList));
                        };

                        func(repeatCardList1[0], repeatCardList1[1]);
                        func(repeatCardList1[1], repeatCardList1[0]);
                    }
                }
                else if (wcCount == 3) {
                    let keyValue = wcId;
                    let showIdList = this.getRepeatWCValueList(wcId, 3);
                    showIdList.push(repeatCardList1[0]);
                    plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_ONE, cardIdList, keyValue, this.getRepeatWCValueList(keyValue, 3), showIdList));

                    keyValue = repeatCardList1[0];
                    if (!this.isJoker(keyValue)) {
                        var targetValue = this.transferWildCardTo(keyValue);
                        showIdList = this.getRepeatWCValueList(targetValue, 2);
                        showIdList.push(keyValue);
                        showIdList.push(wcId);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_ONE, cardIdList, keyValue, this.getRepeatWCValueList(keyValue, 3), showIdList));
                    }
                }
            }

            //三带二
            checkTriple2(cardIdList, repeatCardLists, wcCount, plist) {
                if(cardIdList.length != 5)
                    return;

                var repeatCardList1 = repeatCardLists[0];
                if(this.hasJoker(repeatCardList1))
                    return;
                var repeatCardList2 = repeatCardLists[1];
                var repeatCardList3 = repeatCardLists[2];
                var wcId = this.getWildcardId();
                if(wcCount == 1)
                {
                    if(repeatCardList2.length == 2)
                    {
                        var self = this;
                        var func = function(keyPair, normalPair)
                        {
                            var keyValue = keyPair[0];
                            var showIdList = keyPair.concat();
                            showIdList.unshift(self.transferWildCardTo(keyValue));
                            showIdList = showIdList.concat(normalPair);
                            plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_TWO, cardIdList, keyValue, [keyValue], showIdList));
                        };
                        func(repeatCardList2[0], repeatCardList2[1]);
                        func(repeatCardList2[1], repeatCardList2[0]);
                    }
                    else if(repeatCardList3.length == 1)
                    {
                        var showIdList = repeatCardList3[0].concat();
                        var keyValue = showIdList[0];
                        var transValue = repeatCardList1[0];
                        showIdList.push(this.transferWildCardTo(transValue));
                        showIdList.push(transValue);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_TWO, cardIdList, keyValue, [transValue], showIdList));
                    }
                }
                else if(wcCount == 2)
                {
                    if(repeatCardList3.length == 1)
                    {
                        var showIdList = repeatCardList3[0].concat();
                        var keyValue = showIdList[0];
                        showIdList.push(wcId);
                        showIdList.push(wcId);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_TWO, cardIdList, keyValue, [wcId, wcId], showIdList));
                    }
                    else if(repeatCardList2.length == 1)
                    {
                        var showIdList = repeatCardList2[0].concat();
                        var keyValue = showIdList[0];
                        showIdList.unshift(this.transferWildCardTo(keyValue));
                        var transValue = repeatCardList1[0];
                        showIdList.push(this.transferWildCardTo(transValue));
                        showIdList.push(transValue);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_TWO, cardIdList, keyValue, [keyValue, transValue], showIdList));

                        var keyValue = repeatCardList1[0];
                        var targetValue = this.transferWildCardTo(keyValue);
                        showIdList = [targetValue, targetValue, keyValue];
                        showIdList = showIdList.concat(repeatCardList2[0]);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_TWO, cardIdList, keyValue, [keyValue, keyValue], showIdList));
                    }
                }
                else if(wcCount == 3)
                {
                    if(repeatCardList2.length == 1)
                    {
                        showIdList = [wcId, wcId, wcId];
                        keyValue = wcId;
                        showIdList = showIdList.concat(repeatCardList2[0]);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_TWO, cardIdList, keyValue, [wcId, wcId, wcId], showIdList));

                        keyValue = repeatCardList2[0][0];
                        var targetValue = this.transferWildCardTo(keyValue);
                        showIdList = [targetValue].concat(repeatCardList2[0]);
                        showIdList.push(wcId);
                        showIdList.push(wcId);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_TWO, cardIdList, keyValue, [targetValue, wcId, wcId], showIdList));
                    }
                    else
                    {
                        var self = this;
                        var func = function(keyValue, pairValue)
                        {
                            var targetKeyValue = self.transferWildCardTo(keyValue);
                            var targetPairValue = self.transferWildCardTo(pairValue);
                            var showIdList = [targetKeyValue, targetKeyValue, keyValue, targetPairValue, pairValue];
                            plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_TWO, cardIdList, keyValue, [keyValue, keyValue, pairValue], showIdList));
                        };
                        func(repeatCardList1[0], repeatCardList1[1]);
                        func(repeatCardList1[1], repeatCardList1[0]);
                    }
                }
                else if(wcCount == 4)
                {
                    keyValue = wcId;
                    var targetValue = this.transferWildCardTo(repeatCardList1[0]);
                    showIdList = [wcId, wcId, wcId, targetValue, repeatCardList1[0]];
                    showIdList = showIdList.concat(repeatCardList2);
                    plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_TWO, cardIdList, keyValue, [wcId, wcId, wcId, targetValue], showIdList));

                    keyValue = repeatCardList1[0];
                    targetValue = this.transferWildCardTo(keyValue);
                    showIdList = [targetValue, targetValue, keyValue, wcId, wcId];
                    plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_TWO, cardIdList, keyValue, [targetValue, targetValue, wcId, wcId], showIdList));
                }
            }

            //单顺子
            checkSequence(cardIdList, repeatCardLists, wcCount, plist) {
                var repeatCardList1 = repeatCardLists[0];
                if (cardIdList.length < 5 ||
                    cardIdList.length > 12 ||
                    this.getCardNumber(cardIdList[wcCount]) > 14 ||
                    repeatCardList1.length + wcCount != cardIdList.length)
                    return;

                if (repeatCardList1.length + wcCount == cardIdList.length) {
                    var leftWcCount = wcCount;
                    var list = [repeatCardList1[0]];
                    var lastNum = this.getCardNumber(list[0]);
                    var wcValueList = [];
                    for (var i = 1; i < repeatCardList1.length; ++i) {
                        var currentCardId = repeatCardList1[i];
                        var currentNum = this.getCardNumber(currentCardId);

                        var fillCount = lastNum - currentNum - 1;
                        if (fillCount > 0) {
                            if (leftWcCount >= fillCount) {
                                for (var j = 0; j < fillCount; ++j) {
                                    --lastNum;
                                    var targetValue = this.getWildCardByNum(lastNum);
                                    wcValueList.push(targetValue);
                                    list.push(targetValue);
                                }
                                list.push(currentCardId);
                                leftWcCount -= fillCount;
                            }
                            else
                                return;
                        }
                        else
                            list.push(currentCardId);

                        lastNum = currentNum;
                    }
                }

                //处理多余的癞子
                if (leftWcCount > 0) {
                    var maxNum = this.getCardNumber(list[0]);
                    var maxLeftNum = Math.min(14 - maxNum, leftWcCount);

                    for (var biggerCount = maxLeftNum; biggerCount >= 0; --biggerCount) {
                        var showIdList = list.concat();
                        var tmpWcValueList = wcValueList.concat();
                        for (var i = 0; i < biggerCount; ++i) {
                            var num = this.getCardNumber(showIdList[0]) + 1;
                            var targetValue = this.getWildCardByNum(num);
                            showIdList.unshift(targetValue);
                            tmpWcValueList.push(targetValue);
                        }

                        for (j = 0; j < leftWcCount - biggerCount; ++j) {
                            let num = this.getCardNumber(showIdList[showIdList.length - 1]) - 1;
                            if (num < 3)
                                return;

                            var targetValue = this.getWildCardByNum(num);
                            showIdList.push(targetValue);
                            tmpWcValueList.push(targetValue);
                        }
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.SEQUENCE, cardIdList, showIdList[0], tmpWcValueList, showIdList));
                    }
                }
                else
                    plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.SEQUENCE, cardIdList, list[0], wcValueList, list));
            }

            //双顺子
            checkSequenceOfPairs(cardIdList, repeatCardLists, wcCount, plist) {
                var repeatCardList1 = repeatCardLists[0];
                var repeatCardList2 = repeatCardLists[1];
                var repeatCardList3 = repeatCardLists[2];
                var repeatCardList4 = repeatCardLists[3];
                if (cardIdList.length < 6 ||
                    cardIdList.length % 2 == 1 ||
                    repeatCardList1.length > wcCount ||
                    repeatCardList3.length > 0 ||
                    repeatCardList4.length > 0 ||
                    this.getCardNumber(cardIdList[wcCount]) > 14)
                    return;

                var leftWcCount = wcCount;
                var wcValueList = [];
                var srcList = repeatCardList2.concat();
                for (var i = 0; i < repeatCardList1.length; ++i) {
                    if (leftWcCount == 0)
                        return;

                    var cardId = repeatCardList1[i];

                    var wcValue = this.transferWildCardTo(cardId);
                    srcList.push([wcValue, cardId]);
                    wcValueList.push(wcValue);
                    --leftWcCount;
                }

                srcList.sort(this.repeatListSortFunc);
                if (leftWcCount == 0) {
                    if (this.getCardNumber(srcList[0][0]) - this.getCardNumber(srcList[srcList.length - 1][0]) == srcList.length - 1)
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.SEQUENCE_OF_PAIRS, cardIdList, srcList[0][0], wcValueList, this.combineList(srcList)));

                    return;
                }

                var list = [srcList[0]];
                var lastNum = this.getCardNumber(list[0][0]);
                for (var i = 1; i < srcList.length; ++i) {
                    var currentPair = srcList[i];
                    // var currentCardId = currentPair[0];
                    var currentNum = this.getCardNumber(currentPair[0]);

                    var fillCount = lastNum - currentNum - 1;
                    if (fillCount > 0) {
                        if (leftWcCount >= 2 * fillCount) {
                            for (var j = 0; j < fillCount; ++j) {
                                --lastNum;
                                var wcValue = this.getWildCardByNum(lastNum);
                                wcValueList.push(wcValue);
                                wcValueList.push(wcValue);
                                list.push([wcValue, wcValue]);
                            }
                            list.push(currentPair);
                            leftWcCount -= 2 * fillCount;
                        }
                        else
                            return;
                    }
                    else
                        list.push(currentPair);

                    lastNum = currentNum;
                }

                srcList = list;
                if (leftWcCount == 0) {
                    plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.SEQUENCE_OF_PAIRS, cardIdList, srcList[0][0], wcValueList, this.combineList(srcList)));
                }
                else if (leftWcCount % 2 == 0) {
                    var maxNum = this.getCardNumber(srcList[0][0]);
                    var maxLeftNum = Math.min(14 - maxNum, leftWcCount / 2);
                    var totalCount = leftWcCount / 2;
                    for (var biggerCount = maxLeftNum; biggerCount >= 0; --biggerCount) {
                        var pairList = srcList.concat();
                        var tmpWcValueList = wcValueList.concat();
                        for (var i = 0; i < biggerCount; ++i) {
                            var num = this.getCardNumber(pairList[0][0]) + 1;
                            var wcValue = this.getWildCardByNum(num);
                            pairList.unshift([wcValue, wcValue]);
                            tmpWcValueList.push(wcValue);
                            tmpWcValueList.push(wcValue);
                        }

                        for (j = 0; j < totalCount - biggerCount; ++j) {
                            let num = this.getCardNumber(pairList[pairList.length - 1][0]) - 1;
                            if (num < 3)
                                return;

                            var wcValue = this.getWildCardByNum(num);
                            pairList.push([wcValue, wcValue]);
                            tmpWcValueList.push(wcValue);
                            tmpWcValueList.push(wcValue);
                        }
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.SEQUENCE_OF_PAIRS, cardIdList, pairList[0][0], tmpWcValueList, this.combineList(pairList)));
                    }
                }
            }

            //飞机
            checkSequenceOfTriplets(cardIdList, repeatCardLists, wcCount, plist, isAll?) {
                var lenCards = cardIdList.length;
                var repeatCardList4 = repeatCardLists[3];
                if( lenCards % 3 != 0 ||
                    this.getCardNumber(cardIdList[wcCount]) > 14 ||
                    repeatCardList4.length > 0)
                    return;

                var repeatCardList1 = repeatCardLists[0];
                var repeatCardList2 = repeatCardLists[1];

                var tripletsList = [];
                var wcValueList = [];
                for(var i = 0; i < repeatCardList1.length; ++i)
                {
                    if(wcCount < 2)
                        return;

                    var cardId = repeatCardList1[i];
                    var wcValue = this.transferWildCardTo(cardId);
                    var list = [wcValue, wcValue, cardId];
                    wcValueList.push(wcValue, wcValue);
                    wcCount -= 2;

                    tripletsList.push(list);
                }

                for(i = 0; i < repeatCardList2.length; ++i)
                {
                    if(wcCount < 1)
                        return;

                    list = repeatCardList2[i].concat();
                    var wcValue = this.transferWildCardTo(list[0]);
                    list.unshift(wcValue);
                    wcValueList.push(wcValue);
                    --wcCount;

                    tripletsList.push(list);
                }
                var repeatCardList3 = repeatCardLists[2];
                tripletsList = tripletsList.concat(repeatCardList3);
                tripletsList.sort(this.repeatListSortFunc);

                var func = function(tripletsList, wcValueList)
                {
                    var keyValue = tripletsList[0][0];
                    var num1 = this.getCardNumber(keyValue);
                    var offset = tripletsList.length - 1;
                    var num2 = this.getCardNumber(tripletsList[offset][0]);
                    if(num1 - num2 == offset)
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.SEQUENCE_OF_TRIPLETS, cardIdList, keyValue, wcValueList, this.combineList(tripletsList)));
                }.bind(this);

                if(wcCount == 0)
                {
                    func(tripletsList, wcValueList);
                }
                else if(wcCount == 3)
                {
                    var num1 = this.getCardNumber(tripletsList[0][0]);
                    var offset = tripletsList.length - 1;
                    var num2 = this.getCardNumber(tripletsList[offset][0]);
                    if(num1 - num2 == offset)
                    {
                        if(num1 < 14)
                        {
                            var wcValue = this.getWildCardByNum(num1 + 1);
                            var tmpTripletsList = [[wcValue, wcValue, wcValue]].concat(tripletsList);
                            var tmpWcValueList = wcValueList.concat([wcValue, wcValue, wcValue]);
                            func(tmpTripletsList, tmpWcValueList);
                        }
                        if(num2 > 3)
                        {
                            var wcValue = this.getWildCardByNum(num2 - 1);
                            tmpTripletsList = tripletsList.concat([[wcValue, wcValue, wcValue]]);
                            var tmpWcValueList = wcValueList.concat([wcValue, wcValue, wcValue]);
                            func(tmpTripletsList, tmpWcValueList);
                        }
                    }
                    else
                    {
                        var lastNum = this.getCardNumber(tripletsList[0][0]);
                        for(var i = 1; i < tripletsList.length; ++i)
                        {
                            var num = this.getCardNumber(tripletsList[i][0]);
                            var offset = lastNum - num;
                            if(offset > 2)
                                return;
                            else if(offset == 2)
                            {
                                var wcValue = this.getWildCardByNum(num + 1);
                                tmpTripletsList = tripletsList.concat();
                                tmpTripletsList.splice(i, -1, [wcValue, wcValue, wcValue]);
                                var tmpWcValueList = wcValueList.concat([wcValue, wcValue, wcValue]);
                                func(tmpTripletsList, tmpWcValueList);
                            }
                        }
                    }
                }
            }


            //*******************************************3带1飞机判断***********************************************//
            //用癞子牌把list补成三条的数组
            fillRepeatListWithWildCard(list, fillCount, wcValueList) {
                var wcValue = this.transferWildCardTo(list[0]);
                for (var i = 0; i < fillCount; ++i) {
                    list.unshift(wcValue);
                    wcValueList.push(wcValue);
                }
            }

            // list待处理的数组,元素可能是个三条，也可能不是,不是三条的元素使用癞子进行填充,
            checkFillTripletListWitchWildCard(list, wcCount, wcValueList) {
                for (var i = 0; i < list.length; ++i) {
                    var tmpList = list[i].concat();
                    var fillCount = 3 - tmpList.length;
                    if (fillCount > 0) {
                        wcCount -= fillCount;
                        if (wcCount < 0)
                            break;

                        this.fillRepeatListWithWildCard(tmpList, fillCount, wcValueList);
                    }
                    list[i] = tmpList;
                }

                return wcCount;
            }

            //测试是否能生成3带1飞机
            //testList为待测试的连续数组，eg.srcList = [[6a,6b,6c], [5a], [4a,4b]];
            testSequenceOfTriplets1(cardIdList, testList, wcCount, wcValueList, plist) {
                var leftWcCount = this.checkFillTripletListWitchWildCard(testList, wcCount, wcValueList);
                if (leftWcCount < 0)
                    return false;

                //组装除三条外的翅膀数据
                var wingsList = [];
                var num1 = this.getCardNumber(testList[0][0]);
                var num2 = this.getCardNumber(testList[testList.length - 1][0]);
                for (var i = wcCount; i < cardIdList.length; ++i) {
                    var cardId = cardIdList[i];
                    if (this.isWildcard(cardId))
                        continue;
                    var num = this.getCardNumber(cardId);
                    if (num <= num1 && num >= num2)
                        continue;

                    wingsList.push(cardId);
                }

                if (leftWcCount > 0) {
                    var wcId = this.getWildcardId();
                    var repeatWCValueList = this.getRepeatWCValueList(wcId, leftWcCount);
                    wingsList.unshift(repeatWCValueList);
                    wcValueList = wcValueList.concat(repeatWCValueList);
                }
                // wingsList.sort(this.repeatListSortFunc);

                var showIdList = this.combineList(testList).concat(this.combineList(wingsList));
                plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_ONE, cardIdList, showIdList[0], wcValueList, showIdList));

                return true;
            }

            // getList

            //飞机带单翅膀
            checkSequenceOfTriplets1(cardIdList, repeatCardLists, wcCount, plist) {
                var lenCards = cardIdList.length;
                var repeatCardList4 = repeatCardLists[3];
                if (lenCards % 4 != 0 ||
                    repeatCardList4.length > 0)
                    return;

                var tripletCount = lenCards / 4;
                var repeatCardList1 = repeatCardLists[0];
                var repeatCardList2 = repeatCardLists[1];
                var repeatCardList3 = repeatCardLists[2];

                var list = repeatCardList2.concat(repeatCardList3);
                jx.each(repeatCardList1, function (cardId) {
                    list.push([cardId]);
                });
                list.sort(this.repeatListSortFunc);

                var listCount = list.length;

                //检测已存在数组中的第一
                for (var i = 0; i < list.length; ++i) {
                    if (listCount - i < tripletCount)
                        break;

                    var testList = list.slice(i, i + tripletCount);
                    if (this.isSerial(testList)) {
                        var wcValueList = [];
                        this.testSequenceOfTriplets1(cardIdList, testList, wcCount, wcValueList, plist);
                    }
                }

                if (wcCount > 2) {
                    var testTripletCount = tripletCount - 1;
                    for (i = 0; i < list.length; ++i) {
                        if (listCount - i < testTripletCount)
                            break;

                        var num1 = this.getCardNumber(list[i][0]);
                        if (num1 > 14)
                            continue;

                        var idxLastTest = i + testTripletCount - 1;
                        var num2 = this.getCardNumber(list[idxLastTest][0]);
                        var offset = num1 - num2;
                        //连续
                        if (offset == testTripletCount - 1) {
                            if ((i == 0 || (this.getCardNumber(list[i - 1][0]) != num1 + 1)) && num1 < 14) {
                                let wcValue = this.getWildCardByNum(num1 + 1);
                                let wcValueList = [wcValue, wcValue, wcValue];
                                let testList = list.slice(i, i + testTripletCount);
                                testList.unshift(wcValueList);

                                this.testSequenceOfTriplets1(cardIdList, testList, wcCount - 3, wcValueList, plist);
                            }

                            if ((idxLastTest == list.length - 1 || (this.getCardNumber(list[idxLastTest + 1][0]) != num2 - 1) && num2 > 3)) {
                                let wcValue = this.getWildCardByNum(num2 - 1);
                                let wcValueList = [wcValue, wcValue, wcValue];
                                let testList = list.slice(i, i + testTripletCount);
                                testList.push(wcValueList);

                                this.testSequenceOfTriplets1(cardIdList, testList, wcCount - 3, wcValueList, plist);
                            }
                        }
                        else if (offset == tripletCount - 1)//不连续但可以填充
                        {
                            var testList = list.slice(i, i + testTripletCount);
                            var lastNum = this.getCardNumber(testList[0][0]);
                            for (var j = 0; j < testList.length; ++j) {
                                var num = this.getCardNumber(testList[j + 1][0]);
                                if (lastNum - num == 1)
                                    continue;

                                if (lastNum - num == 2) {
                                    var wcValue = this.getWildCardByNum(num + 1);
                                    let wcValueList = [wcValue, wcValue, wcValue];
                                    testList.splice(j + 1, -1, wcValueList.concat());

                                    this.testSequenceOfTriplets1(cardIdList, testList, wcCount - 3, wcValueList, plist);
                                }
                                break;
                            }
                        }
                    }
                }
            }

            //*******************************************3带1飞机判断 end***********************************************//

            //*******************************************3带2飞机判断***********************************************//
            //测试是否能生成3带2飞机
            //testList为待测试的连续数组，eg.srcList = [[6a,6b,6c], [5a], [4a,4b]];
            testSequenceOfTriplets2(cardIdList, testList, wcCount, wcValueList, plist) {
                var leftWcCount = this.checkFillTripletListWitchWildCard(testList, wcCount, wcValueList);
                if (leftWcCount < 0)
                    return false;

                //组装除三条外的翅膀数据
                var leftIdList = [];
                var num1 = this.getCardNumber(testList[0][0]);
                var num2 = this.getCardNumber(testList[testList.length - 1][0]);
                for (var i = wcCount; i < cardIdList.length; ++i) {
                    var cardId = cardIdList[i];
                    if (this.isWildcard(cardId))
                        continue;
                    var num = this.getCardNumber(cardId);
                    if (num <= num1 && num >= num2)
                        continue;

                    leftIdList.push(cardId);
                }

                //预处理牌数组数据
                var repeatCardLists = this.analyseRepeatList(leftIdList);
                var repeatCardList1 = repeatCardLists[0];
                var repeatCardList2 = repeatCardLists[1];
                var repeatCardList3 = repeatCardLists[2];
                var repeatCardList4 = repeatCardLists[3];

                //不足以填充对子
                if (repeatCardList1.length + repeatCardList3.length > leftWcCount)
                    return;

                var pairList = [];
                for (let i = 0; i < repeatCardList1.length; ++i) {
                    if (leftWcCount == 0)
                        return;

                    var cardId = repeatCardList1[i];
                    var wcValue = this.transferWildCardTo(cardId);
                    wcValueList.push(wcValue);
                    pairList.push([wcValue, cardId]);
                    --leftWcCount;
                }

                for (i = 0; i < repeatCardList3.length; ++i) {
                    if (leftWcCount == 0)
                        return;

                    var repeatList = repeatCardList3[i].concat();
                    var cardId = repeatList[0];
                    var wcValue = this.transferWildCardTo(cardId);
                    repeatList.unshift(wcValue);
                    wcValueList.push(wcValue);
                    pairList.push(repeatList);
                    --leftWcCount;
                }

                if (leftWcCount > 0) {
                    if (leftWcCount % 2 != 0)
                        return;

                    var wcId = this.getWildcardId();
                    var repeatWCValueList = this.getRepeatWCValueList(wcId, leftWcCount);
                    pairList.push(repeatWCValueList);
                    wcValueList = wcValueList.concat(repeatWCValueList);
                }
                var wingsList = pairList.concat(repeatCardList2, repeatCardList4);
                wingsList.sort(this.repeatListSortFunc);
                wingsList = this.combineList(wingsList);

                var showIdList = this.combineList(testList).concat(wingsList);
                plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_TWO, cardIdList, showIdList[0], wcValueList, showIdList));
                return true;
            }

            //飞机带双翅膀
            checkSequenceOfTriplets2(cardIdList, repeatCardLists, wcCount, plist) {
                var lenCards = cardIdList.length;
                if (lenCards % 5 != 0)
                    return;

                var repeatCardList1 = repeatCardLists[0];
                if (this.hasJoker(repeatCardList1))
                    return;

                var repeatCardList2 = repeatCardLists[1];
                var repeatCardList3 = repeatCardLists[2];
                var tripletCount = lenCards / 5;
                // var repeatCardList4 = repeatCardLists[3];

                var list = repeatCardList2.concat(repeatCardList3);
                jx.each(repeatCardList1, function (cardId) {
                    list.push([cardId]);
                });
                list.sort(this.repeatListSortFunc);

                var listCount = list.length;

                //检测已存在数组中的第一
                for (var i = 0; i < list.length; ++i) {
                    if (listCount - i < tripletCount)
                        break;

                    var testList = list.slice(i, i + tripletCount);
                    if (this.isSerial(testList)) {
                        var wcValueList = [];
                        this.testSequenceOfTriplets2(cardIdList, testList, wcCount, wcValueList, plist);
                    }
                }

                if (wcCount > 2) {
                    var testTripletCount = tripletCount - 1;
                    for (i = 0; i < list.length; ++i) {
                        if (listCount - i < testTripletCount)
                            break;

                        var num1 = this.getCardNumber(list[i][0]);
                        if (num1 > 14)
                            continue;

                        var idxLastTest = i + testTripletCount - 1;
                        var num2 = this.getCardNumber(list[idxLastTest][0]);
                        var offset = num1 - num2;
                        //连续
                        if (offset == testTripletCount - 1) {
                            if ((i == 0 || (this.getCardNumber(list[i - 1][0]) != num1 + 1)) && num1 < 14) {
                                var wcValue = this.getWildCardByNum(num1 + 1);
                                let wcValueList = [wcValue, wcValue, wcValue];
                                var testList = list.slice(i, i + testTripletCount);
                                testList.unshift(wcValueList);

                                this.testSequenceOfTriplets2(cardIdList, testList, wcCount - 3, wcValueList, plist);
                            }

                            if ((idxLastTest == list.length - 1 || (this.getCardNumber(list[idxLastTest + 1][0]) != num2 - 1) && num2 > 3)) {
                                var wcValue = this.getWildCardByNum(num2 - 1);
                                let wcValueList = [wcValue, wcValue, wcValue];
                                var testList = list.slice(i, i + testTripletCount);
                                testList.push(wcValueList);

                                this.testSequenceOfTriplets2(cardIdList, testList, wcCount - 3, wcValueList, plist);
                            }
                        }
                        else if (offset == tripletCount - 1)//不连续但可以填充
                        {
                            var testList = list.slice(i, i + testTripletCount);
                            var lastNum = this.getCardNumber(testList[0][0]);
                            for (var j = 0; j < testList.length; ++j) {
                                var num = this.getCardNumber(testList[j + 1][0]);
                                if (lastNum - num == 1)
                                    continue;

                                if (lastNum - num == 2) {
                                    var wcValue = this.getWildCardByNum(num + 1);
                                    let wcValueList = [wcValue, wcValue, wcValue];
                                    testList.splice(j + 1, -1, wcValueList.concat());

                                    this.testSequenceOfTriplets2(cardIdList, testList, wcCount - 3, wcValueList, plist);
                                }
                                break;
                            }
                        }
                    }
                }
            }

            //*******************************************3带2飞机判断 end***********************************************//

            //癞子炸弹
            checkBomb(cardIdList, repeatCardLists, wcCount, plist) {
                if (cardIdList.length != 4)
                    return;

                var list = repeatCardLists[4 - wcCount - 1];
                if (list.length == 0)
                    return;

                if (wcCount < 3)
                    list = list[0];
                if (4 - wcCount == list.length) {
                    var keyValue = list[0];
                    if (!this.isJoker(keyValue)) {
                        var showIdList = this.getRepeatWCValueList(this.transferWildCardTo(keyValue), wcCount).concat(list);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.BOMB, cardIdList, keyValue, this.getRepeatWCValueList(keyValue, wcCount), showIdList));
                    }
                }
            }

            //四带二（单牌）
            checkQuadplexSet1(cardIdList, repeatCardLists, wcCount, plist) {
                if (cardIdList.length != 6)
                    return;

                var repeatCardList1 = repeatCardLists[0];
                var repeatCardList2 = repeatCardLists[1];
                var repeatCardList3 = repeatCardLists[2];
                var repeatCardList4 = repeatCardLists[3];
                var wcId = this.getWildcardId();

                var keyValue;
                var showIdList;
                var wcValueList;
                var wcValue;
                var self = this;
                if (repeatCardList4.length == 1) {
                    keyValue = repeatCardList4[0][0];
                    showIdList = repeatCardList4[0].concat();
                    showIdList.push(wcId);
                    wcValueList = [wcId];
                    if (wcCount == 1) {
                        showIdList.push(repeatCardList1[0]);
                    }
                    else {
                        showIdList.push(wcId);
                        wcValueList.push(wcId);
                    }
                    plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_ONE, cardIdList, keyValue, wcValueList, showIdList));
                }
                else if (wcCount == 1) {
                    if (repeatCardList3.length == 1) {
                        showIdList = repeatCardList3[0].concat();
                        keyValue = showIdList[0];
                        wcValue = this.transferWildCardTo(keyValue);
                        showIdList.unshift(wcValue);
                        if (repeatCardList1.length == 2)
                            showIdList = showIdList.concat(repeatCardList1);
                        else
                            showIdList = showIdList.concat(repeatCardList2[0]);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_ONE, cardIdList, keyValue, [keyValue], showIdList));
                    }
                }
                else if (wcCount == 2) {
                    var func = function (keyList, singleList) {
                        let showIdList = keyList.concat();
                        let keyValue = showIdList[0];
                        let wcValue = self.transferWildCardTo(keyValue);
                        showIdList.unshift(wcValue);
                        showIdList.unshift(wcValue);
                        showIdList = showIdList.concat(singleList);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_ONE, cardIdList, keyValue, [keyValue, keyValue], showIdList));
                    };
                    if (repeatCardList2.length == 1) {
                        func(repeatCardList2[0], repeatCardList1);
                    }
                    else if (repeatCardList2.length == 2) {
                        func(repeatCardList2[0], repeatCardList2[1]);
                        func(repeatCardList2[1], repeatCardList2[0]);
                    }
                    else if (repeatCardList3.length == 1) {
                        showIdList = repeatCardList3[0].concat();
                        keyValue = showIdList[0];
                        wcValue = self.transferWildCardTo(keyValue);
                        showIdList.unshift(wcValue);
                        showIdList.push(wcId);
                        showIdList = showIdList.concat(repeatCardList1);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_ONE, cardIdList, keyValue, [keyValue, wcId], showIdList));
                    }
                }
                else if (wcCount == 3) {
                    if (repeatCardList3.length == 1) {
                        showIdList = repeatCardList3[0].concat();
                        keyValue = showIdList[0];
                        showIdList.unshift(this.transferWildCardTo(keyValue));
                        showIdList = showIdList.concat([wcId, wcId]);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_ONE, cardIdList, keyValue, [keyValue, wcId, wcId], showIdList));
                    }
                    else if (repeatCardList2.length == 1) {
                        showIdList = repeatCardList2[0].concat();
                        keyValue = showIdList[0];
                        wcValue = this.transferWildCardTo(keyValue);
                        showIdList.unshift(wcValue);
                        showIdList.unshift(wcValue);
                        showIdList = showIdList.concat([wcId, repeatCardList1[0]]);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_ONE, cardIdList, keyValue, [keyValue, keyValue, wcId], showIdList));

                        keyValue = repeatCardList1[0];
                        if (!this.isJoker(keyValue)) {
                            wcValue = this.transferWildCardTo(keyValue);
                            wcValueList = [wcValue, wcValue, wcValue];
                            let showIdList = [wcValue, wcValue, wcValue, keyValue].concat(repeatCardList2[0]);
                            plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_ONE, cardIdList, keyValue, wcValueList, showIdList));
                        }
                    }
                    else if (repeatCardList1.length == 3) {
                        let func = function (keyValue, single1, single2) {
                            if (self.isJoker(keyValue))
                                return;

                            let wcValue = self.transferWildCardTo(keyValue);
                            let wcValueList = self.getRepeatWCValueList(wcValue, 3);
                            let showIdList = wcValueList.concat([keyValue, single1, single2]);
                            plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_ONE, cardIdList, keyValue, wcValueList, showIdList));
                        };
                        var c1 = repeatCardList1[0];
                        var c2 = repeatCardList1[1];
                        var c3 = repeatCardList1[2];
                        func(c1, c2, c3);
                        func(c2, c1, c3);
                        func(c3, c1, c2);
                    }
                }
                else if (wcCount == 4) {
                    if (repeatCardList1.length == 2) {
                        wcValueList = [wcId, wcId, wcId, wcId];
                        showIdList = wcValueList.concat(repeatCardList1);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_ONE, cardIdList, wcId, wcValueList, showIdList));

                        var func = function (keyValue, single) {
                            let wcValue = self.transferWildCardTo(keyValue);
                            let wcValueList = self.getRepeatWCValueList(wcValue, 3);
                            let showIdList = wcValueList.concat([keyValue, wcId, single]);
                            wcValueList.push(wcId);
                            plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_ONE, cardIdList, keyValue, wcValueList, showIdList));
                        };

                        func(repeatCardList1[0], repeatCardList1[1]);
                        func(repeatCardList1[1], repeatCardList1[0]);
                    }
                    else {
                        let keyList = repeatCardList2[0];
                        keyValue = keyList[0];
                        wcValue = this.transferWildCardTo(keyValue);
                        wcValueList = [wcValue, wcValue, wcId, wcId];
                        showIdList = [wcValue, wcValue, keyList[0], keyList[1], wcId, wcId];
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_ONE, cardIdList, keyValue, wcValueList, showIdList));

                        wcValueList = [wcId, wcId, wcId, wcId];
                        showIdList = wcValueList.concat(repeatCardList2[0]);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_ONE, cardIdList, wcId, wcValueList, showIdList));
                    }
                }

            }

            //四带二（对子）
            checkQuadplexSet2(cardIdList, repeatCardLists, wcCount, plist) {
                if (cardIdList.length != 8)
                    return;

                var repeatCardList1 = repeatCardLists[0];
                if (this.hasJoker(repeatCardList1))
                    return;

                var repeatCardList2 = repeatCardLists[1];
                var repeatCardList3 = repeatCardLists[2];
                var repeatCardList4 = repeatCardLists[3];

                var wcId = this.getWildcardId();
                var wcValue;
                var pairList;
                var showIdList;
                var keyValue;
                var pairs;
                var wcPairValue;
                var wvValueList;
                var wvPairValue;
                var wcValueList;
                var wcValue1;
                var wcValue2;
                var keyList;
                var func;

                var self = this;
                if (wcCount == 1) {
                    if (repeatCardList4.length == 1 && repeatCardList2.length == 1) {
                        wcValue = this.transferWildCardTo(repeatCardList1[0]);
                        pairList = [[wcValue, repeatCardList1[0]], repeatCardList2[0]];
                        pairList.sort(this.repeatListSortFunc);
                        showIdList = repeatCardList4[0].concat(this.combineList(pairList));
                        keyValue = showIdList[0];
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, cardIdList, keyValue, [wcValue], showIdList));
                    }
                    else if (repeatCardList3.length == 1 && repeatCardList2.length == 2) {
                        showIdList = repeatCardList3[0].concat();
                        keyValue = showIdList[0];
                        wcValue = this.transferWildCardTo(keyValue);
                        showIdList.unshift(wcValue);
                        pairs = repeatCardList2[0].concat(repeatCardList2[1]);
                        showIdList = showIdList.concat(pairs);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, cardIdList, keyValue, [wcValue], showIdList));
                    }
                }
                else if (wcCount == 2) {
                    if (repeatCardList4.length == 1) {
                        if (repeatCardList2.length == 1) {
                            pairList = [[wcId, wcId], repeatCardList2[0]];
                            pairList.sort(this.repeatListSortFunc);
                            showIdList = repeatCardList4[0].concat(this.combineList(pairList));
                            keyValue = showIdList[0];
                            plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, cardIdList, keyValue, [wcId, wcId], showIdList));
                        }
                        else if (repeatCardList1.length == 2) {
                            wcValue1 = this.transferWildCardTo(repeatCardList1[0]);
                            wcValue2 = this.transferWildCardTo(repeatCardList1[1]);
                            pairList = [repeatCardList1[0], wcValue1, repeatCardList1[1], wcValue2];
                            showIdList = repeatCardList4[0].concat(pairList);
                            keyValue = showIdList[0];
                            plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, cardIdList, keyValue, [wcValue1, wcValue2], showIdList));
                        }
                    }
                    else if (repeatCardList3.length == 1 && repeatCardList2.length == 1) {
                        showIdList = repeatCardList3[0].concat();
                        keyValue = showIdList[0];
                        showIdList.unshift(this.transferWildCardTo(keyValue));

                        wcPairValue = this.transferWildCardTo(repeatCardList1[0]);
                        pairList = [[wcPairValue, repeatCardList1[0]], repeatCardList2[0]];
                        pairList.sort(this.repeatListSortFunc);

                        showIdList = showIdList.concat(this.combineList(pairList));
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, cardIdList, keyValue, [keyValue, wcPairValue], showIdList));
                    }
                    else if (repeatCardList2.length == 3) {
                        func = function (keyList, pair1, pair2) {
                            let keyValue = keyList[0];
                            let wcValue = self.transferWildCardTo(keyValue);
                            let showIdList = [wcValue, wcValue].concat(keyList).concat(pair1).concat(pair2);
                            plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, cardIdList, keyValue, [keyValue, keyValue], showIdList));
                        };
                        var pair1 = repeatCardList2[0];
                        var pair2 = repeatCardList2[1];
                        var pair3 = repeatCardList2[2];
                        func(pair1, pair2, pair3);
                        func(pair2, pair1, pair3);
                        func(pair3, pair1, pair2);
                    }
                }
                else if (wcCount == 3) {
                    if (repeatCardList4.length == 1) {
                        wvPairValue = this.transferWildCardTo(repeatCardList1[0]);
                        pairList = [[wcId, wcId], [wvPairValue, repeatCardList1[0]]];
                        pairList.sort(this.repeatListSortFunc);
                        showIdList = repeatCardList4[0].concat(this.combineList(pairList));
                        keyValue = showIdList[0];
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, cardIdList, keyValue, [wcId, wcId, wvPairValue], showIdList));
                    }
                    else if (repeatCardList3.length == 1) {
                        if (repeatCardList2.length == 1) {
                            showIdList = repeatCardList3[0].concat();
                            keyValue = showIdList[0];
                            showIdList.unshift(this.transferWildCardTo(keyValue));

                            pairList = [[wcId, wcId], repeatCardList2[0]];
                            pairList.sort(this.repeatListSortFunc);

                            showIdList = showIdList.concat(this.combineList(pairList));
                            plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, cardIdList, keyValue, [wcId, wcId, keyValue], showIdList));
                        }
                        else if (repeatCardList1.length == 2) {
                            showIdList = repeatCardList3[0].concat();
                            keyValue = showIdList[0];
                            showIdList.unshift(this.transferWildCardTo(keyValue));

                            wcValue1 = this.transferWildCardTo(repeatCardList1[0]);
                            wcValue2 = this.transferWildCardTo(repeatCardList1[1]);
                            pairList = [repeatCardList1[0], wcValue1, repeatCardList1[1], wcValue2];

                            showIdList = showIdList.concat(this.combineList(pairList));
                            plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, cardIdList, keyValue, [wcValue1, wcValue2, keyValue], showIdList));
                        }
                    }
                    else if (repeatCardList2.length == 2) {
                        keyValue = repeatCardList1[0];
                        wcValue = this.transferWildCardTo(keyValue);
                        wvValueList = this.getRepeatWCValueList(wcValue, 3);
                        showIdList = wvValueList.concat(keyValue).concat(repeatCardList2[0]).concat(repeatCardList2[1]);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, cardIdList, keyValue, wvValueList, showIdList));

                        func = function (keyList, pair) {
                            let keyValue = keyList[0];
                            let wcValue = self.transferWildCardTo(keyValue);

                            let wcPairValue = self.transferWildCardTo(repeatCardList1[0]);
                            let pairList = [[wcPairValue, repeatCardList1[0]], pair];
                            pairList.sort(self.repeatListSortFunc);
                            let showIdList = [wcValue, wcValue].concat(keyList).concat(self.combineList(pairList));
                            plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, cardIdList, keyValue, [wcValue, wcValue, wcPairValue], showIdList));
                        };

                        func(repeatCardList2[0], repeatCardList2[1]);
                        func(repeatCardList2[1], repeatCardList2[0]);
                    }
                }
                else if (wcCount == 4) {
                    if (repeatCardList3.length == 1) {
                        showIdList = repeatCardList3[0].concat();
                        keyValue = showIdList[0];
                        showIdList.unshift(this.transferWildCardTo(keyValue));

                        wvPairValue = this.transferWildCardTo(repeatCardList1[0]);
                        pairList = [[wcId, wcId], [wvPairValue, repeatCardList1[0]]];
                        pairList.sort(this.repeatListSortFunc);
                        showIdList = showIdList.concat(this.combineList(pairList));

                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, cardIdList, keyValue, [wcId, wcId, keyValue, wvPairValue], showIdList));
                    }
                    else if (repeatCardList2.length == 2) {
                        wcValueList = [wcId, wcId, wcId, wcId];
                        showIdList = wcValueList.concat(repeatCardList2[0]).concat(repeatCardList2[1]);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, cardIdList, wcId, wcValueList, showIdList));

                        func = function (keyPair, pair) {
                            let keyValue = keyPair[0];
                            let wcValue = self.transferWildCardTo(keyValue);
                            let wcValueList = [keyValue, keyValue, wcId, wcId];

                            let pairList = [pair, [wcId, wcId]];
                            pairList.sort(self.repeatListSortFunc);
                            let showIdList = [wcValue, wcValue].concat(keyPair).concat(self.combineList(pairList));
                            plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_ONE, cardIdList, keyValue, wcValueList, showIdList));
                        };

                        func(repeatCardList2[0], repeatCardList2[1]);
                        func(repeatCardList2[1], repeatCardList2[0]);
                    }
                    else if (repeatCardList2.length == 1) {
                        wcValue1 = this.transferWildCardTo(repeatCardList1[0]);
                        wcValue2 = this.transferWildCardTo(repeatCardList1[1]);
                        pairList = [repeatCardList1[0], wcValue1, repeatCardList1[1], wcValue2];

                        keyList = repeatCardList2[0].concat();
                        keyValue = keyList[0];
                        wcValue = this.transferWildCardTo(keyValue);
                        showIdList = [wcValue, wcValue].concat(keyList).concat(pairList);
                        plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, cardIdList, keyValue, [keyValue, keyValue, wcValue1, wcValue2], showIdList));

                        func = function (keyValue, single) {
                            let wcValue = self.transferWildCardTo(keyValue);
                            let wcValueList = self.getRepeatWCValueList(wcValue, 3);

                            let wcPairValue = self.transferWildCardTo(single);
                            let pairList = [repeatCardList2[0], [wcPairValue, single]];
                            pairList.sort(self.repeatListSortFunc);
                            let showIdList = wcValueList.concat(keyValue).concat(self.combineList(pairList));
                            wcValueList.push(wcPairValue);
                            plist.push(flaw.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, cardIdList, keyValue, wcValueList, showIdList));
                        };

                        func(repeatCardList1[0], repeatCardList1[1]);
                        func(repeatCardList1[1], repeatCardList1[0]);
                    }
                }
            }

            getGreaterList(cardPattern, availableList) {
                // var cardPattern = this.getCardPattern(target);
                var targetType = cardPattern.getType();

                var list = null;
                switch (targetType) {
                    case fla.CARD_TYPE.ROCKET:
                        return null;

                    case fla.CARD_TYPE.INVALID:
                        return null;

                    default:
                        var tipsObj = flaw.TipsUtils.getTipsObj(cardPattern, availableList);
                        list = tipsObj.getTipsList();
                        break;
                }

                list = list || [];

                //为原生牌型跟癞子牌型相同关键值时做过滤
                var tmp = [];
                jx.each(list, function(cardIdList){
                    var cpList = this.getCardPattern(cardIdList);
                    if(!jx.isArray(cpList))
                        cpList = [cpList];
                    for(var i = 0; i < cpList.length; ++i)
                    {
                        var cp = cpList[i];
                        if(cp.greaterThan(cardPattern))
                        {
                            tmp.push(cardIdList);
                            return;
                        }
                    }
                }, this);
                list = tmp;

                if(this.hasRocket(availableList))
                    list.push([fla.CONSTANTS.RED_JOKER_ID, fla.CONSTANTS.BLACK_JOKER_ID]);

              //  console.log("-------------------tips list-----------------------");
                jx.each(list, function(cardIdList, i){
                    console.log(i + " usable:" + cardIdList.join(","));
                });

                return list;
            }

            getWCCardPattern(cardIdList, wcValueList) {

            }
        }

        export let CardPatternFactory = {
            getPattern: function (type, cardIdList, keyValue?, wcValueList?, showCardIdList?) {
                var pattern = null;
                switch (type) {
                    case fla.CARD_TYPE.ROCKET:
                        pattern = new fla.Rocket();
                        break;

                    case fla.CARD_TYPE.BOMB:
                        pattern = new flaw.Bomb(cardIdList, wcValueList, showCardIdList);
                        break;

                    default:
                        pattern = new flaw.BaseCardPattern(type, cardIdList);// keyValue, wcValueList, showCardIdList
                        break;
                }

                return pattern;
            }
        };

        export let unitTest = function (list) {
            console.log("fla unit test!");

            jx.each(list, function(strCardIdList)
            {
                var cardIdList = fla.utils.getCardIdList(strCardIdList);
                var plist = fla.utils.getCardPattern(cardIdList);
                console.log(strCardIdList + "--------------------test card list:" );
                jx.each(plist, function(pattern){
                    // console.log(pattern.getCardIdList().join(","), pattern.toString());
                    console.log(pattern.toString());
                });
                console.log("");
            });
        };

        export let testTipList = function (list, target) {
            var targetIdList = flaw.utils.getCardIdList(target);
            var targetPattern = flaw.utils.getCardPattern(targetIdList);
            if(jx.isArray(targetPattern))
                targetPattern = targetPattern[0];
            console.log("--------------------------------------------------");
            console.log("target:" + targetPattern.getCardIdList().join(",") + "----" + targetPattern.toString());

            jx.each(list, function(strCardIdList)
            {
                var cardIdList = fla.utils.getCardIdList(strCardIdList);
                console.log("-----------------------usable list---------------------------");
                console.log("target:" + cardIdList.join(","));
                // fla.utils.getSequenceList(cardIdList, targetPattern)
                var cardPattern = flaw.utils.getCardPattern(targetIdList);
                if(jx.isArray(cardPattern))
                    cardPattern = cardPattern[0];
                var usalbeList = fla.utils.getGreaterList(cardPattern, cardIdList);
                // cc.each(usalbeList, function(cardIdList){
                //     console.log("usable:" + cardIdList.join(","));
                // });
            });
        };

        export let testSort = function (list) {
            jx.each(list, function (cardIdList, i) {
                var cp = flaw.utils.getCardPattern(cardIdList.split(","));
                if (jx.isArray(cp))
                    cp = cp[0];
                list[i] = cp;
            });
            list.sort(function (cp1, cp2) {
                console.log(cp1.toString());
                console.log(cp2.toString());
                console.log("------------------");
                if (cp2.greaterThan(cp1))
                    return 1;

                return -1;
            });

            jx.each(list, function (cp) {
                console.log(cp.getShowCardIdList().join(","));
            });
        };

    }

}