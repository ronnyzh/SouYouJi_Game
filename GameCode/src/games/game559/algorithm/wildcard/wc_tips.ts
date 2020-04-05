module G559{
    export namespace rfaw {
        export let TipsUtils = {
            getTipsObj: function (opponent, cardIdList) {
                var obj = null;
                switch (opponent.getType()) {
                    case rfa.CARD_TYPE.SEQUENCE:
                        obj = new rfaw.SequenceTips(opponent, cardIdList);
                        break;

                    case rfa.CARD_TYPE.SINGLE_CARD:
                        obj = new rfaw.SingleCardTips(opponent, cardIdList);
                        break;

                    case rfa.CARD_TYPE.PAIR:
                        obj = new rfaw.PairTips(opponent, cardIdList);
                        break;

                    case rfa.CARD_TYPE.TRIPLET:
                    case rfa.CARD_TYPE.TRIPLET_WITH_ONE:
                    case rfa.CARD_TYPE.TRIPLET_WITH_TWO:
                        obj = new rfaw.TripletTips(opponent, cardIdList);
                        break;

                    case rfa.CARD_TYPE.BOMB:
                        obj = new rfaw.BombTips(opponent, cardIdList);
                        break;

                    case rfa.CARD_TYPE.QUADPLEX_SET_WITH_ONE:
                    case rfa.CARD_TYPE.QUADPLEX_SET_WITH_TWO:
                        obj = new rfaw.QuadplexSetTips(opponent, cardIdList);
                        break;

                    case rfa.CARD_TYPE.SEQUENCE_OF_PAIRS:
                        obj = new rfaw.PairSequenceTips(opponent, cardIdList);
                        break;

                    case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS:
                    case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_ONE:
                    case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_TWO:
                        obj = new rfaw.TripletSequenceTips(opponent, cardIdList);
                        break;

                }

                return obj;
            }
        };

        export class TipsObj extends rfa.TipsObj {
            public wcCount;
            constructor(opponent, cardIdList) {
                super(opponent, cardIdList)
            }

            addBomb(list) {
                super.addBomb(list);
                if (this.wcCount > 0) {
                    for (var count = 3; count > 0; --count) {
                        if ((count + this.wcCount) < 4)
                            break;

                        var repeatCardList = this.getRepeatList(count);
                        if (repeatCardList.length == 0)
                            continue;

                        var wcList = this.getWcListForCount(4 - count);
                        for (var i = repeatCardList.length - 1; i >= 0; --i) {
                            if (count == 1 && rfaw.classicUtils.isJoker(repeatCardList[i]))
                                continue;

                            var bombList = wcList.concat(repeatCardList[i]);
                            list.push(bombList);
                        }
                    }
                }
                if (this.wcCount == 4) {
                    list.push(this.getWcListForCount(4));
                }
            }

            isWildcardPattern(list) {

            }

            getWcListForCount(count) {
                return this.cardIdList.slice(0, count);
            }

            analyse() {
                this.wcCount = rfaw.utils.getWildcardCount(this.cardIdList);
                var normalList = this.cardIdList.slice(this.wcCount);
                //预处理牌数组数据
                this.repeatCardLists = rfaw.utils.analyseRepeatList(normalList);
            }

            getWildcardId() {
                return rfaw.utils.getWildcardId();
            }

            getWildcardIdList(count) {
                var wcId = this.getWildcardId();
                var list = [];
                while (count-- > 0)
                    list.push(wcId);

                return list;
            }

            handleWildcard(list) {
                // return list;
                var repeatMap = {};
                // var wcId = this.getWildcardId();
                var finalList = [];
                jx.each(list, function (cardIdList, i) {
                    var count = 0;
                    var finalCardIdList = [];
                    jx.each(cardIdList, function (cardId) {
                        if (rfaw.utils.isWildcard(cardId))
                            ++count;
                        else
                            finalCardIdList.push(cardId);
                    }, this);

                    if (count > this.wcCount) {
                        console.error("error wildcard count:" + count, "wildcard count is only:" + this.wcCount);
                        return;
                    }

                    if (count > 0)
                        finalCardIdList = this.getWcListForCount(count).concat(finalCardIdList);
                    finalCardIdList.sort(rfaw.utils.sortCardFunc);

                    var key = finalCardIdList.join(",");
                    if (repeatMap[key] == null) {
                        // list[i] = finalCardIdList;
                        finalList.push(finalCardIdList);
                        repeatMap[key] = 1;
                    }
                }, this);

                return finalList;
            }

            isIntersect(list1, list2) {
                for (var i = 0; i < list1.length; ++i) {
                    var id1 = list1[i];
                    for (var j = 0; j < list2.length; ++j) {
                        var id2 = list2[j];
                        if (id1 == id2)
                            return true;
                    }
                }
                return false;
            }

            getNumCardList(count, excludeList){
                if (this.cardIdList.length - excludeList.length < count)
                    return null;

                var excludeNumList = this.getNumList(excludeList);

                var list = [];
                //var id2Num = {};
                for (var i = this.cardIdList.length - 1; i >= 0; --i) {
                    var id = this.cardIdList[i];
                    if (excludeNumList.indexOf(this.getCardNumber(id)) == -1)
                        list.push(id);

                    // if(id2Num.hasOwnProperty(id))
                    //     id2Num[id] += 1;
                    // else
                    //     id2Num[id] = 1;
                    //
                    // if(id2Num[id] == 4)
                    //     excludeNumList.push(id);

                    if (list.length == count)
                        break;
                }

                if (list.length < count) {
                    var usedWcCount = 0;
                    jx.each(excludeList, function (cardId) {
                        if (rfaw.utils.isWildcard(cardId))
                            ++usedWcCount;
                    });

                    if (usedWcCount == excludeList.length)
                        return null;

                    if (usedWcCount == 3) {
                        excludeList.sort(rfaw.classicUtils.compareCard);
                        if (this.getCardNumber(excludeList[0]) - this.getCardNumber(excludeList[excludeList.length - 1]) == excludeList.length / 3) {
                            var isValid = false;
                            var id2Num = {};
                            jx.each(excludeList, function (cardId) {
                                var id = this.getCardNumber(cardId);
                                if (id2Num.hasOwnProperty(id))
                                    id2Num[id] += 1;
                                else
                                    id2Num[id] = 1;
                            }, this);

                            for (var key in id2Num) {
                                if (id2Num[key] != 3) {
                                    isValid = true;
                                    break;
                                }
                            }

                            if (!isValid)
                                return null;
                        }
                    }

                    var wcId = this.getWildcardId();
                    var needCount = count - list.length;
                    if (needCount <= this.wcCount - usedWcCount) {
                        while (needCount > 0) {
                            list.push(wcId);
                            --needCount;
                        }
                    }
                }

                if (list.length >= count)
                    list.reverse();
                else
                    list = null;

                return list;
            }

            getSingleCardList(count, excludeList) {
                if (this.cardIdList.length - excludeList.length < count)
                    return null;

                var excludeNumList = this.getNumList(excludeList);

                var list = null;
                var r1List = this.getRepeatList(1);
                if (r1List.length >= count && !this.isIntersect(excludeList, r1List))
                    list = r1List.slice(r1List.length - count);
                else {
                    list = [];
                    for (var i = this.cardIdList.length - 1; i >= 0; --i) {
                        var id = this.cardIdList[i];
                        if (excludeNumList.indexOf(this.getCardNumber(id)) == -1)
                            list.push(id);

                        if (list.length == count)
                            break;
                    }
                }

                if (list.length > count)
                    list.reverse();
                else {
                    //检测癞子当单牌的情况
                    var usedWcCount = 0;
                    jx.each(excludeList, function (cardId) {
                        if (rfaw.utils.isWildcard(cardId))
                            ++usedWcCount;
                    });

                    var wcId = this.getWildcardId();
                    var needCount = count - list.length;
                    var leftCount = this.wcCount - usedWcCount;
                    if (leftCount >= needCount) {
                        while (needCount > 0) {
                            list.push(wcId);
                            --needCount;
                        }
                    }
                }

                return list;
            }

            getPairList(count, excludeList) {
                if (this.cardIdList.length - excludeList.length < 2 * count)
                    return null;

                var excludeNumList = this.getNumList(excludeList);
                var list = [];
                for (var i = 2; i <= 3; ++i) {
                    var repeatList = this.getRepeatList(i);
                    if (repeatList.length > 0) {
                        for (var j = repeatList.length - 1; j >= 0; --j) {
                            var tmp = repeatList[j];
                            if (excludeNumList.indexOf(this.getCardNumber(tmp[0])) != -1)
                                continue;

                            list.push(tmp.slice(i - 2));
                            if (list.length == count)
                                return list;

                            //炸弹可以拆两对
                            if (i == 4) {
                                list.push(tmp.slice(0, 2));
                                if (list.length == count)
                                    return list;
                            }
                        }
                    }
                }

                var repeatList = this.getRepeatList(4);
                if (repeatList.length > 0) {
                    for (var j = repeatList.length - 1; j >= 0; --j) {
                        var tmp = repeatList[j];
                        if (excludeNumList.indexOf(this.getCardNumber(tmp[0])) != -1)
                            continue;

                        list.push(tmp.slice(i - 2));
                        list.push(tmp.slice(0, 2));

                        if (list.length >= count) {
                            //有可能取炸弹做两对比只取炸弹其中一对更好，比如12a,12b,8a,8b,8c,8d，从牌值来说，此时留对12比对8好
                            list.sort(this.repeatListSortFunc);
                            list = list.slice(list.length - count);
                            return list;
                        }
                    }
                }

                //检测癞子凑对子的情况
                var usedWcCount = 0;
                jx.each(excludeList, function (cardId) {
                    if (rfaw.utils.isWildcard(cardId))
                        ++usedWcCount;
                });
                var wcId = this.getWildcardId();
                var needCount = count - list.length;
                var leftWcCount = this.wcCount - usedWcCount;
                if (needCount <= leftWcCount) {
                    var repeatList = this.getRepeatList(1);
                    for (var i = repeatList.length - 1; i >= 0; --i) {
                        var cardId = repeatList[i];
                        if (excludeNumList.indexOf(this.getCardNumber(cardId)) != -1)
                            continue;

                        list.push([wcId, cardId]);
                        if (list.length == count)
                            return list;

                        --leftWcCount;
                        if (leftWcCount <= 0)
                            break;
                    }

                    var repeatList = this.getRepeatList(3);
                    for (var i = repeatList.length - 1; i >= 0; --i) {
                        var cardId = repeatList[j][0];
                        if (excludeNumList.indexOf(this.getCardNumber(cardId)) != -1)
                            continue;

                        list.push([wcId, cardId]);
                        if (list.length == count)
                            return list;

                        --leftWcCount;
                        if (leftWcCount <= 0)
                            break;
                    }
                }

                return null;
            }

            getAvailableSequence(itemCount, lenSequence?) {
                var availableList = [];
                var lenOpponent = this.opponent.getCardIdList().length;
                if (this.cardIdList.length >= lenOpponent) {
                    var keyValue = this.kvOpponent;
                    if (lenSequence == null)
                        lenSequence = lenOpponent / itemCount;
                    var keyNum = this.getCardNumber(keyValue) - lenSequence + 1;

                    var testItemList = [];
                    for (var count = 1; count <= 4; ++count) {
                        var repeatList = this.getRepeatList(count);
                        for (var i = 0; i < repeatList.length; ++i) {
                            var testItem = repeatList[i];
                            if (count == 1)
                                testItem = [testItem];
                            if (count < itemCount)
                                testItem = testItem.concat();
                            else
                                testItem = testItem.slice(count - itemCount);

                            var numCard = this.getCardNumber(testItem[0]);
                            if (numCard > 14)
                                continue;

                            if (numCard <= keyNum)
                                break;

                            testItemList.push(testItem);
                        }
                    }

                    if (testItemList.length > 0) {
                        testItemList.sort(rfaw.utils.repeatListSortFunc);

                        var numCardMin = Math.max(this.getCardNumber(testItemList[testItemList.length - 1][0]) - this.wcCount, keyNum);
                        var numCardMax = 14 - lenSequence + 1;
                        for (var numMinTest = numCardMin; numMinTest <= numCardMax; ++numMinTest) {
                            var wcCount = this.wcCount;
                            var testList = [];
                            var numCurrent = numMinTest;
                            var numMaxTest = numMinTest + lenSequence - 1;
                            for (var i = testItemList.length - 1; i >= 0; --i) {
                                var testItem = testItemList[i].concat();
                                var numCard = this.getCardNumber(testItem[0]);
                                if (numCard < numMinTest)
                                    continue;

                                if (numCard == numCurrent) {
                                    var needCount = itemCount - testItem.length;
                                    if (needCount > 0) {
                                        if (wcCount < needCount)
                                            break;

                                        testItem = this.getWildcardIdList(needCount).concat(testItem);
                                        wcCount -= needCount;
                                    }
                                    testList.unshift(testItem);
                                    ++numCurrent;
                                }
                                else {
                                    while (numCurrent < numCard && numCurrent <= numMaxTest) {
                                        testList.unshift(this.getWildcardIdList(itemCount));
                                        ++numCurrent;
                                        wcCount -= itemCount;

                                        if (wcCount < 0)
                                            break;
                                    }

                                    if (wcCount < 0)
                                        break;

                                    if (testList.length < lenSequence) {
                                        var needCount = itemCount - testItem.length;
                                        if (needCount > 0) {
                                            if (wcCount < needCount)
                                                break;

                                            testItem = this.getWildcardIdList(needCount).concat(testItem);
                                            wcCount -= needCount;
                                        }

                                        testList.unshift(testItem);
                                        ++numCurrent;
                                    }
                                }

                                if (testList.length == lenSequence) {
                                    availableList.push(this.combineList(testList));
                                    break;
                                }
                            }

                            if (testList.length < lenSequence) {
                                while (numCurrent <= numMaxTest) {
                                    testList.unshift(this.getWildcardIdList(itemCount));
                                    ++numCurrent;
                                    wcCount -= itemCount;

                                    if (wcCount < 0)
                                        break;
                                }
                                if (wcCount >= 0 && testList.length == lenSequence) {
                                    availableList.push(this.combineList(testList));
                                    break;
                                }
                            }
                        }
                    }
                }
                return availableList;
            }

            getAvailableItemList(itemCount) {
                var availableList = [];
                this.iterRepeatList(itemCount, 4, function (count, list) {
                    if (rfa.utils.greaterThan(this.kvOpponent, list[0]))
                    //if(this.getCardNumber(list[0]) >= this.getCardNumber(this.kvOpponent))
                        availableList.push(list.slice(count - itemCount));
                }.bind(this));

                for (var i = itemCount - 1; i > 0; --i) {
                    var needCount = itemCount - i;
                    if (this.wcCount >= needCount) {
                        var repeatList = this.getRepeatList(i);
                        for (var j = repeatList.length - 1; j >= 0; --j) {
                            var list = repeatList[j];
                            if (!jx.isArray(list))
                                list = [list];

                            if (!rfaw.classicUtils.isJoker(list[0]) && rfa.utils.greaterThan(this.kvOpponent, list[0]))
                                availableList.push(this.getWildcardIdList(needCount).concat(list));
                        }
                    }
                }

                var wcId = this.getWildcardId();
                if (this.wcCount >= itemCount && rfa.utils.greaterThan(this.kvOpponent, wcId)) {
                    availableList.push(this.getWcListForCount(itemCount));
                }
                return availableList;
            }
        }

        export class SequenceTips extends rfaw.TipsObj {
            getTipsList() {
                var tipsList = this.getAvailableSequence(1);
                this.addBomb(tipsList);
                tipsList = this.handleWildcard(tipsList);

                return tipsList;
            }
        }

        export class SingleCardTips extends rfaw.TipsObj {
            getTipsList() {
                var tipsList = [];
                var r1List = this.getRepeatList(1);
                for (var i = r1List.length - 1; i >= 0; --i) {
                    var id = r1List[i];
                    if (rfa.utils.greaterThan(this.kvOpponent, id))
                        tipsList.push([id]);
                }

                this.iterRepeatList(2, 4, function (count, list) {
                    if (rfa.utils.greaterThan(this.kvOpponent, list[0]))
                        tipsList.push(list.slice(count - 1));
                }.bind(this));

                if (this.wcCount > 0) {
                    if (rfa.utils.greaterThan(this.kvOpponent, this.cardIdList[0]))
                        tipsList.push(this.getWcListForCount(1));
                }

                this.addBomb(tipsList);
                return tipsList;
            }
        }

        export class PairTips extends rfaw.TipsObj {
            getTipsList() {
                var tipsList = this.getAvailableItemList(2);
                this.addBomb(tipsList);
                tipsList = this.handleWildcard(tipsList);
                return tipsList;
            }
        }


        export class TripletTips extends rfaw.TipsObj {
            getTipsList() {
                var testList = this.getAvailableItemList(3);
                var tipsList = [];
                switch (this.opponent.getType()) {
                    case rfa.CARD_TYPE.TRIPLET:
                        tipsList = tipsList.concat(testList);
                        break;

                    case rfa.CARD_TYPE.TRIPLET_WITH_ONE:
                        for (var i = 0; i < testList.length; ++i) {
                            var testItem = testList[i];
                            var tmp = this.getSingleCardList(1, testItem);
                            if (tmp != null && tmp.length > 0)
                                tipsList.push(testItem.concat(tmp));
                        }
                        break;

                    case rfa.CARD_TYPE.TRIPLET_WITH_TWO:
                        for (var i = 0; i < testList.length; ++i) {
                            var testItem = testList[i];
                            let tmp: any[] = this.getNumCardList(2, testItem);
                            if (tmp != null && tmp.length > 0)
                                tipsList.push(testItem.concat(tmp));
                        }
                        break;
                }

                this.addBomb(tipsList);
                tipsList = this.handleWildcard(tipsList);
                return tipsList;
            }
        }

        export class PairSequenceTips extends rfaw.TipsObj {
            getTipsList() {
                var tipsList = this.getAvailableSequence(2);
                this.addBomb(tipsList);
                tipsList = this.handleWildcard(tipsList);

                return tipsList;
            }
        }

        export class TripletSequenceTips extends rfaw.TipsObj {
            getTipsList() {
                var lenOpponent = this.opponent.getCardIdList().length;
                var lenOpponentTriplet = this.opponent.getSequenceNum();
                var lastCardNum = lenOpponent - lenOpponentTriplet * 3;
                var tipsList = [];
                switch (this.opponent.getType()) {
                    case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS:
                        var testList = this.getAvailableSequence(3, lenOpponentTriplet);
                        for (var i = 0; i < testList.length; ++i) {
                            var tripletList = testList[i];
                            var tmp = this.getNumCardList(lastCardNum, tripletList);
                            if (tmp != null && tmp.length > 0)
                                tipsList.push(tripletList.concat(tmp));
                        }
                        break;

                    // case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_ONE:
                    //     var lenSequence = lenOpponent / 4;
                    //     var testList = this.getAvailableSequence(3, lenSequence);
                    //     for(var i = 0; i < testList.length; ++i)
                    //     {
                    //         var tripletList = testList[i];
                    //         var tmp = this.getSingleCardList(lenSequence, tripletList);
                    //         if(tmp != null && tmp.length > 0)
                    //             tipsList.push(tripletList.concat(tmp));
                    //     }
                    //     break;
                    //
                    // case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_TWO:
                    //     var lenSequence = lenOpponent / 5;
                    //     var testList = this.getAvailableSequence(3, lenSequence);
                    //     for(var i = 0; i < testList.length; ++i)
                    //     {
                    //         var tripletList = testList[i];
                    //         var tmp = this.getPairList(lenSequence, tripletList);
                    //         if(tmp != null && tmp.length > 0)
                    //             tipsList.push(tripletList.concat(this.combineList(tmp)));
                    //     }
                    //     break;

                }
                this.addBomb(tipsList);
                tipsList = this.handleWildcard(tipsList);

                return tipsList;
            }
        }

        export class BombTips extends rfaw.TipsObj {
            getTipsList() {
                var bombList = [];
                this.addBomb(bombList);
                var tipsList = [];
                var isOpponentWcPattern = this.opponent.isWildcardPattern();
                var isAllWc = this.opponent.isAllWildcardPattern();
                jx.each(bombList, function (bomb) {
                    //是否癞子炸弹
                    var isWcBomb = bomb[0][0] != bomb[3][0];
                    var isAllWcBomb = !isWcBomb && rfaw.utils.isWildcard(bomb[0]);

                    if (isAllWc) {
                        if (isAllWcBomb && rfa.utils.greaterThan(this.kvOpponent, bomb[0]))
                            tipsList.push(bomb);
                    }
                    else if (isOpponentWcPattern) {
                        if (!isWcBomb || isAllWcBomb || rfa.utils.greaterThan(this.kvOpponent, bomb[3]))
                            tipsList.push(bomb);
                    }
                    else {
                        if (isAllWcBomb || (!isWcBomb && rfa.utils.greaterThan(this.kvOpponent, bomb[0])))
                            tipsList.push(bomb);
                    }
                    // if(isWcBomb)
                    // {
                    //     if(isOpponentWcPattern && rfa.utils.greaterThan(this.kvOpponent, bomb[3]))
                    //         tipsList.push(bomb);
                    // }
                    // else
                    // {
                    //     if(isOpponentWcPattern || rfa.utils.greaterThan(this.kvOpponent, bomb[0]))
                    //         tipsList.push(bomb);
                    // }
                }, this);

                tipsList = this.handleWildcard(tipsList);
                return tipsList;
            }
        }

        export class QuadplexSetTips extends rfaw.TipsObj {
            getTipsList() {
                var testList = this.getAvailableItemList(4);
                var tipsList = [];
                switch (this.opponent.getType()) {
                    case rfa.CARD_TYPE.BOMB:
                        tipsList = tipsList.concat(testList);
                        break;

                    case rfa.CARD_TYPE.QUADPLEX_SET_WITH_ONE:
                        for (var i = 0; i < testList.length; ++i) {
                            var testItem = testList[i];
                            var tmp = this.getSingleCardList(2, testItem);
                            if (tmp != null && tmp.length > 0)
                                tipsList.push(testItem.concat(tmp));
                        }
                        break;

                    case rfa.CARD_TYPE.QUADPLEX_SET_WITH_TWO:
                        for (var i = 0; i < testList.length; ++i) {
                            var testItem = testList[i];
                            let tmp:any[] = this.getPairList(2, testItem);
                            if (tmp != null && tmp.length > 0)
                                tipsList.push(testItem.concat(this.combineList(tmp)));
                        }
                        break;
                }

                this.addBomb(tipsList);
                tipsList = this.handleWildcard(tipsList);
                return tipsList;
            }
        }
    }
}