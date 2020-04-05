module G559{
    export namespace rfa {
        export class TipsObj {
            public opponent;
            public cardIdList;
            public kvOpponent;
            public repeatCardLists;

            constructor(opponent, cardIdList) {
                this.opponent = opponent;
                this.cardIdList = cardIdList;
                this.kvOpponent = this.opponent.getKeyValue();
                this.analyse();
            }

            getCardNumber(cardId) {
                return rfa.utils.getCardNumber(cardId);
            }

            repeatListSortFunc(list1, list2) {
                var num1 = rfa.utils.getCardNumber(list1[0]);
                var num2 = rfa.utils.getCardNumber(list2[0]);
                var dv = num2 - num1;
                return dv / Math.abs(dv);
            }

            analyse() {
                //预处理牌数组数据
                var repeatCardLists = [[], [], [], []];
                var numLast = this.getCardNumber(this.cardIdList[0]);
                var tmpList = [];
                for (var i = 0; i < this.cardIdList.length; ++i) {
                    var id = this.cardIdList[i];
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

                }
                if (tmpList.length == 1)
                    repeatCardLists[0].push(tmpList[0]);
                else if (tmpList.length > 1)
                    repeatCardLists[tmpList.length - 1].push(tmpList);

                this.repeatCardLists = repeatCardLists;
            }

            getRepeatList(count) {
                return this.repeatCardLists[count - 1].concat();
            }

            getTipsList() {
                return null;
            }

            addBomb(list) {
                var boomList = this.getRepeatList(4);
                if (boomList.length > 0) {
                    for (var i = boomList.length - 1; i >= 0; --i)
                        list.push(boomList[i]);
                }
            }

            getNumList(cardIdList) {
                var excludeNumList = [];
                jx.each(cardIdList, function (id) {
                        var numCard = this.getCardNumber(id);
                        if (excludeNumList.indexOf(numCard) == -1)
                            excludeNumList.push(numCard);
                    },
                    this);

                return excludeNumList;
            }

            getNumCardList(count, excludeList) {
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
                if (r1List.length >= count)
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

                if (list.length >= count)
                    list.reverse();
                else
                    list = null;

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
                return null;
            }

            combineList(lists) {
                var ret = [];
                jx.each(lists, function (list) {
                    ret = ret.concat(list);
                });

                return ret;
            }

            // hasRocket()
            // {
            //     return this.cardIdList.indexOf(rfa.CONSTANTS.RED_JOKER_ID) != -1 && this.cardIdList.indexOf(rfa.CONSTANTS.BLACK_JOKER_ID) != -1;
            // }
            //
            // addRocket(list)
            // {
            //     if(this.hasRocket())
            //         list.push([rfa.CONSTANTS.RED_JOKER_ID, rfa.CONSTANTS.BLACK_JOKER_ID]);
            // }

            iterRepeatList(startCount, endCount, iterator) {
                for (var i = startCount; i <= endCount; ++i) {
                    var repeatList = this.getRepeatList(i);
                    if (repeatList.length > 0) {
                        for (var j = repeatList.length - 1; j >= 0; --j) {
                            var list = repeatList[j];
                            iterator(i, list);
                        }
                    }
                }
            }
        }

        export class SequenceTips extends TipsObj {
            constructor(opponent, cardIdList) {
                super(opponent, cardIdList);
            }

            getTipsList() {
                var opponentCardIdList = this.opponent.getCardIdList();
                var lenOpponent = opponentCardIdList.length;
                var list = [];
                if (this.cardIdList.length >= lenOpponent) {
                    var maxNum = this.getCardNumber(opponentCardIdList[0]);
                    var minNum = this.getCardNumber(opponentCardIdList[lenOpponent - 1]);

                    var tmp = [];
                    var lastNumCard = 0;
                    for (var i = 0; i < this.cardIdList.length; ++i) {
                        var cardId = this.cardIdList[i];
                        var numCard = this.getCardNumber(cardId);
                        //去掉无效顺子牌
                        if (numCard > 14)
                            continue;

                        //不会再出现更大的顺子牌
                        if (tmp.length == 0 && numCard <= maxNum)
                            break;

                        if (numCard <= minNum)
                            break;

                        if (lastNumCard != numCard) {
                            lastNumCard = numCard;
                            tmp.push(cardId);
                        }
                        else//相同牌值时使用花色排序值最低的牌
                        {
                            tmp[tmp.length - 1] = cardId;
                        }
                    }

                    if (tmp.length >= lenOpponent) {
                        for (i = 0; i < tmp.length; ++i) {
                            cardId = tmp[i];
                            if (tmp.length - i < lenOpponent)
                                break;

                            var num1 = this.getCardNumber(cardId);
                            if (this.getCardNumber(cardId) <= maxNum)
                                break;

                            var num2 = this.getCardNumber(tmp[i + lenOpponent - 1]);
                            if (num1 - num2 == lenOpponent - 1) {
                                var usableList = tmp.slice(i, i + lenOpponent);
                                list.push(usableList);
                                // console.log("usableList:" + usableList.join(","));
                            }
                        }
                        if (list.length > 0)
                            list.reverse();
                    }
                }
                this.addBomb(list);
                // this.addRocket(list);

                return list;
            }
        }

        export class SingleCardTips extends TipsObj {
            getTipsList() {
                var tipsList = [];
                var r1List = this.getRepeatList(1);
                for (var i = r1List.length - 1; i >= 0; --i) {
                    var id = r1List[i];
                    if (rfa.utils.greaterThan(this.opponent.getKeyValue(), id))
                        tipsList.push([id]);
                }

                this.iterRepeatList(2, 4, function (count, list) {
                    if (rfa.utils.greaterThan(this.opponent.getKeyValue(), list[0]))
                        tipsList.push(list.slice(count - 1));
                }.bind(this));

                this.addBomb(tipsList);
                return tipsList;
            }
        }

        export class PairTips extends TipsObj {
            getTipsList() {
                var tipsList = [];
                this.iterRepeatList(2, 4, function (count, list) {
                    if (rfa.utils.greaterThan(this.opponent.getKeyValue(), list[0]))
                        tipsList.push(list.slice(count - 2));
                }.bind(this));

                this.addBomb(tipsList);
                return tipsList;
            }
        }

        export class TripletTips extends TipsObj {
            getTipsList() {
                var tipsList = [];
                this.iterRepeatList(3, 4, function (count, list) {
                    if (!rfa.utils.greaterThan(this.opponent.getKeyValue(), list[0]))
                        return;

                    switch (this.opponent.getType()) {
                        case rfa.CARD_TYPE.TRIPLET:
                            tipsList.push(list.slice(count - 3));
                            break;

                        case rfa.CARD_TYPE.TRIPLET_WITH_ONE:
                            var tmp = this.getSingleCardList(1, list);
                            if (tmp != null && tmp.length > 0)
                                tipsList.push(list.slice(count - 3).concat(tmp));
                            break;

                        case rfa.CARD_TYPE.TRIPLET_WITH_TWO:
                            var tmp = this.getNumCardList(2, list);
                            if (tmp != null && tmp.length > 0)
                                tipsList.push(list.slice(count - 3).concat(tmp));
                            break;
                    }
                }.bind(this));

                this.addBomb(tipsList);
                return tipsList;
            }
        }

        export class PairSequenceTips extends TipsObj {
            getTipsList() {
                var pairList = [];
                var opponentList = this.opponent.getCardIdList();
                var minNum = this.getCardNumber(opponentList[opponentList.length - 1]);
                this.iterRepeatList(2, 4, function (count, list) {
                    var numCard = this.getCardNumber(list[0]);
                    if (numCard <= 14 && numCard > minNum)
                        pairList.push(list.slice(count - 2));
                }.bind(this));

                var lenOpponentPair = opponentList.length / 2;
                var tipsList = [];
                if (pairList.length >= lenOpponentPair) {
                    pairList.sort(this.repeatListSortFunc);
                    for (var i = pairList.length - 1; i >= 0; --i) {
                        var pair1 = pairList[i];
                        var idxPair2 = i - lenOpponentPair + 1;
                        if (idxPair2 < 0)
                            break;

                        var pair2 = pairList[idxPair2];
                        if (this.getCardNumber(pair2[0]) - this.getCardNumber(pair1[0]) == lenOpponentPair - 1)
                            tipsList.push(this.combineList(pairList.slice(idxPair2, i + 1)));
                    }
                }
                this.addBomb(tipsList);

                return tipsList;
            }
        }

        export class TripletSequenceTips extends TipsObj {
            getTipsList() {
                var tripletList = [];
                var opponentList = this.opponent.getCardIdList();
                var lenOpponentTriplet = this.opponent.getSequenceNum();
                var lastCardNum = opponentList.length - lenOpponentTriplet * 3;

                //2副牌取最小值要修改  1副牌不可能出现重叠的情况
                var minNum = this.getCardNumber(opponentList[0]);
                this.iterRepeatList(3, 4, function (count, list) {
                    var numCard = this.getCardNumber(list[0]);
                    if (numCard <= 14 && numCard > minNum)
                        tripletList.push(list.slice(count - 3));
                }.bind(this));
                var tipsList = [];
                if (tripletList.length >= lenOpponentTriplet) {
                    tripletList.sort(this.repeatListSortFunc);

                    for (var i = tripletList.length - 1; i >= 0; --i) {
                        var list1 = tripletList[i];
                        var idx2 = i - lenOpponentTriplet + 1;
                        if (idx2 < 0)
                            break;

                        var list2 = tripletList[idx2];
                        if (this.getCardNumber(list2[0]) - this.getCardNumber(list1[0]) == lenOpponentTriplet - 1) {
                            var usableList = tripletList.slice(idx2, i + 1);
                            usableList = this.combineList(usableList);

                            if (lastCardNum > 0) {
                                var tmp = this.getNumCardList(lastCardNum, usableList);
                                if (tmp != null && tmp.length > 0)
                                    tipsList.push(usableList.concat(tmp));
                            }
                            else if (lastCardNum == 0) {
                                tipsList.push(usableList);
                            }
                            // switch(this.opponent.getType())
                            // {
                            //     case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS:
                            //         tipsList.push(usableList);
                            //         break;
                            //
                            //     case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_ONE:
                            //         var tmp = this.getSingleCardList(lenOpponentTriplet, usableList);
                            //         if(tmp != null && tmp.length > 0)
                            //             tipsList.push(usableList.concat(tmp));
                            //         break;
                            //
                            //     case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_TWO:
                            //         var tmp = this.getPairList(lenOpponentTriplet, usableList);
                            //         if(tmp != null && tmp.length > 0)
                            //         {
                            //             jx.each(tmp, function(pair){
                            //                 usableList = usableList.concat(pair);
                            //             });
                            //             tipsList.push(usableList);
                            //         }
                            //         break;
                            //
                            // }
                        }
                    }
                }

                this.addBomb(tipsList);
                return tipsList;
            }
        }

        export class QuadplexSetTips extends TipsObj {
            getTipsList() {
                var tipsList = [];
                this.iterRepeatList(4, 4, function (count, list) {
                    if (!rfa.utils.greaterThan(this.opponent.getKeyValue(), list[0]))
                        return;

                    switch (this.opponent.getType()) {
                        case rfa.CARD_TYPE.BOMB:
                            tipsList.push(list);
                            break;

                        case rfa.CARD_TYPE.QUADPLEX_SET_WITH_ONE:
                            var tmp = this.getSingleCardList(2, list);
                            if (tmp != null && tmp.length > 0)
                                tipsList.push(list.concat(tmp));
                            break;

                        case rfa.CARD_TYPE.QUADPLEX_SET_WITH_TWO:
                            var tmp = this.getPairList(2, list);
                            if (tmp != null && tmp.length > 0)
                                tipsList.push(list.concat(tmp[0]).concat(tmp[1]));
                            break;
                    }
                }.bind(this));
                if (this.opponent.getType() != rfa.CARD_TYPE.BOMB)
                    this.addBomb(tipsList);
                return tipsList;
            }
        }

        export let TipsUtils = {
            getTipsObj(opponent, cardIdList)
            {
                var obj = null;
                switch (opponent.getType()) {
                    case rfa.CARD_TYPE.SEQUENCE:
                        obj = new rfa.SequenceTips(opponent, cardIdList);
                        break;

                    case rfa.CARD_TYPE.SINGLE_CARD:
                        obj = new rfa.SingleCardTips(opponent, cardIdList);
                        break;

                    case rfa.CARD_TYPE.PAIR:
                        obj = new rfa.PairTips(opponent, cardIdList);
                        break;

                    case rfa.CARD_TYPE.TRIPLET:
                    case rfa.CARD_TYPE.TRIPLET_WITH_ONE:
                    case rfa.CARD_TYPE.TRIPLET_WITH_TWO:
                        obj = new rfa.TripletTips(opponent, cardIdList);
                        break;

                    case rfa.CARD_TYPE.BOMB:
                    case rfa.CARD_TYPE.QUADPLEX_SET_WITH_ONE:
                    case rfa.CARD_TYPE.QUADPLEX_SET_WITH_TWO:
                        obj = new rfa.QuadplexSetTips(opponent, cardIdList);
                        break;

                    case rfa.CARD_TYPE.SEQUENCE_OF_PAIRS:
                        obj = new rfa.PairSequenceTips(opponent, cardIdList);
                        break;

                    case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS:
                    case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_ONE:
                    case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_TWO:
                        obj = new rfa.TripletSequenceTips(opponent, cardIdList);
                        break;

                }

                return obj;
            }
        };

    }

}