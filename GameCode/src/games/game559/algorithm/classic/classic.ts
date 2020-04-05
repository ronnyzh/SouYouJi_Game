/**
 * Created by Administrator on 2018/4/17.
 */
module G559 {
    export namespace rfa {
        export let utils;
        export let initUtils = function () {
            rfa.utils = new rfa.ClassicUtils();
        };

        export class ClassicUtils {
            public sortCardFunc;

            constructor() {
                this.sortCardFunc = this.compareCard.bind(this);
            }

            isJoker(cardId) {
                return cardId == rfa.CONSTANTS.RED_JOKER_ID || cardId == rfa.CONSTANTS.BLACK_JOKER_ID;
            }

            //card2是否大过card1
            greaterThan(card1, card2) {
                // return this.compareCard(card1, card2) == 1;
                return this.getCardNumber(card2) > this.getCardNumber(card1);
            }

            //获得形成牌型后的排序列表
            getPatternIdList(mainList?, cardIdList?) {
                let patternIdList = [];
                jx.each(mainList, function (list) {
                    patternIdList = patternIdList.concat(list);
                });

                mainList = this.combineList(mainList);
                jx.each(cardIdList, function (cardId) {
                    if (mainList.indexOf(cardId) == -1)
                        patternIdList.push(cardId);
                });

                return patternIdList;
            }

            getTripletsPatternIdList(mainList, cardIdList, tripletNum) {
                let patternIdList = [];
                var tripletsList = [];
                for (var i = 0; i < mainList.length - 1; ++i) {
                    var num1 = this.getCardNumber(mainList[i][0]);
                    if (i + tripletNum - 1 < mainList.length) {
                        var num2 = this.getCardNumber(mainList[i + tripletNum - 1][0]);
                        if (num1 - num2 == tripletNum - 1) {
                            for (var j = i; j < i + tripletNum; ++j) {
                                patternIdList = patternIdList.concat(mainList[j]);
                                tripletsList = tripletsList.concat(mainList[j]);
                            }

                            break;
                        }
                    }
                }

                jx.each(cardIdList, function (cardId) {
                    if (tripletsList.indexOf(cardId) == -1)
                        patternIdList.push(cardId);
                });

                return patternIdList;
            }

            combineList(lists) {
                var ret = [];
                jx.each(lists, function (list) {
                    ret = ret.concat(list);
                });

                return ret;
            }

            transferCardId(id) {
                return id;
            }

            compareCard(id1, id2) {
                var num1 = this.getCardNumber(id1);
                var num2 = this.getCardNumber(id2);
                if (num1 == num2) {
                    var type1 = this.getCardType(id1);
                    var type2 = this.getCardType(id2);
                    return type1 > type2 ? -1 : 1;
                }

                return num1 > num2 ? -1 : 1;
            }

            getCardIdList(str) {
                var list = str.split(",");
                jx.each(list, function (id, i) {
                    list[i] = this.transferCardId(id);
                },
                    this
                )
                    ;
                list.sort(this.sortCardFunc);
                return list;
            }

            getCardNumber(cardId) {
                var num = cardId[0];//.substring(0, cardId.length - 1);
                return rfa.CONSTANTS.cardNumMap[num];
            }

            getCardType(cardId) {
                return cardId.charAt(cardId.length - 1);
            }

            //isAll表示是否是所有牌
            getCardPattern(cardIdList?, isAll?) {
                var lenCards = cardIdList.length;
                //单牌
                if (lenCards == 1)
                    return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.SINGLE_CARD, cardIdList, 1);

                //对子
                else if (lenCards == 2) {
                    var id1 = cardIdList[0];
                    var id2 = cardIdList[1];
                    // if(id1 == rfa.CONSTANTS.RED_JOKER_ID && id2 == rfa.CONSTANTS.BLACK_JOKER_ID)
                    //     return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.ROCKET);
                    if (this.getCardNumber(id1) == this.getCardNumber(id2))
                        return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.PAIR, cardIdList, 1);
                }

                //三条
                else if (lenCards == 3 && isAll) {
                    var id1 = cardIdList[0];
                    var id2 = cardIdList[2];

                    if (this.getCardNumber(id1) == this.getCardNumber(id2)) {
                        return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.TRIPLET, cardIdList, 1);
                    }
                }
                else {
                    //预处理牌数组数据
                    var repeatCardLists = [[], [], [], []];
                    var repeatCardList1 = repeatCardLists[0];
                    var repeatCardList2 = repeatCardLists[1];
                    var repeatCardList3 = repeatCardLists[2];
                    var repeatCardList4 = repeatCardLists[3];
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

                    },
                        this
                    )
                        ;

                    if (tmpList.length == 1)
                        repeatCardLists[0].push(tmpList[0]);
                    else if (tmpList.length > 1)
                        repeatCardLists[tmpList.length - 1].push(tmpList);

                    //console.warn('repeatCardLists',repeatCardLists);
                    //四带一，四带二，炸弹
                    if (repeatCardList4.length == 1) {
                        // if(lenCards == 6)
                        //     return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.QUADPLEX_SET_WITH_ONE, this.getPatternIdList(repeatCardList4, cardIdList));
                        // else if(lenCards == 8 && repeatCardList2.length == 2)
                        //     return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.QUADPLEX_SET_WITH_TWO, this.getPatternIdList(repeatCardList4, cardIdList));
                        if (lenCards == 4)
                            return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.BOMB, cardIdList, 1);
                        //四带一
                        if (lenCards == 5 && rfa.QUADPLEX_COVERT_TO_TRIPLET_WITH_ONE)
                            return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.TRIPLET_WITH_TWO, this.getPatternIdList(repeatCardList3, cardIdList), 1);
                    }

                    //三带一，三带二
                    if (repeatCardList3.length == 1) {
                        if (lenCards == 4 && isAll)
                            return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.TRIPLET_WITH_ONE, this.getPatternIdList(repeatCardList3, cardIdList), 1);
                        else if (lenCards == 5)
                            return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.TRIPLET_WITH_TWO, this.getPatternIdList(repeatCardList3, cardIdList), 1);
                    }
                    //飞机
                    else if (repeatCardList3.length > 1) {
                        var len = rfa.utils.tripletIsSerial(repeatCardList3);
                        if (len > 1) {
                            if (lenCards == 3 * len && isAll)
                                return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS, cardIdList, len);
                            else if (lenCards == 5 * len)
                                return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS, this.getTripletsPatternIdList(repeatCardList3, cardIdList, len), len);

                            else if (lenCards < 5 * len) {
                                for (var i = len - 1; i > 1; --i) {
                                    if (lenCards == 5 * i)
                                        return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS, this.getTripletsPatternIdList(repeatCardList3, cardIdList, len), i);
                                }

                                if (isAll)
                                    return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS, this.getTripletsPatternIdList(repeatCardList3, cardIdList, len), len);
                            }
                        }
                        // if(lenCards == 3 * repeatCardList3.length)
                        // {
                        //     return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS, cardIdList);
                        // }
                        // else if(lenCards == 4 * repeatCardList3.length)
                        //     return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_ONE, this.getPatternIdList(repeatCardList3, cardIdList));
                        // else if(lenCards == 5 * repeatCardList3.length &&
                        //     (repeatCardList4.length * 2 + repeatCardList2.length == repeatCardList3.length))//4张拆成2对
                        //     return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_TWO, this.getPatternIdList(repeatCardList3, cardIdList));
                    }

                    //双顺子
                    if (repeatCardList2.length > 1 && repeatCardList2.length * 2 == lenCards && rfa.utils.isSerial(repeatCardList2))
                        return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.SEQUENCE_OF_PAIRS, cardIdList, repeatCardList2.length);

                    //单顺子
                    if (repeatCardList1.length == lenCards && repeatCardList1.length >= 5) {
                        var num1 = this.getCardNumber(repeatCardList1[0]);
                        if (num1 <= 14) {
                            var num2 = this.getCardNumber(repeatCardList1[lenCards - 1]);
                            if (num1 - num2 == lenCards - 1)
                                return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.SEQUENCE, cardIdList, repeatCardList1.length);
                        }
                    }
                }

                return rfa.CardPatternFactory.getPattern(rfa.CARD_TYPE.INVALID, cardIdList, 0);
            }

            patternIsValid(pattern, handCardListNum) {
                if (pattern.getType() == rfa.CARD_TYPE.INVALID)
                    return false;

                // //对3条 3带1 飞机根据手牌数做进一步判断
                // if(pattern.getType() == rfa.CARD_TYPE.TRIPLET && handCardListNum != 3)
                //     return false;
                //
                // else if(pattern.getType() == rfa.CARD_TYPE.TRIPLET_WITH_ONE && handCardListNum != 4)
                //     return false;
                //
                // else if(pattern.getType() == rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS)
                // {
                //     var length = pattern.getCardIdList().length;
                //     if(length != pattern.getSequenceNum() * 5 && length != handCardListNum)
                //         return false;
                // }

                return true;
            }

            tripletIsSerial(lists) {
                var len = lists.length;
                for (var j = 0; j < len - 1; ++j) {
                    var num1 = this.getCardNumber(lists[j][0]);
                    if (num1 > 14)
                        continue;

                    for (var i = len; i > j + 1; --i) {
                        var num2 = this.getCardNumber(lists[i - 1][0]);
                        if (num1 - num2 == i - j - 1)
                            return i - j;
                    }
                }

                return 1;
            }

            isSerial(lists) {
                var num1 = this.getCardNumber(lists[0][0]);
                if (num1 > 14)
                    return false;

                var len = lists.length;
                var num2 = this.getCardNumber(lists[len - 1][0]);

                return num1 - num2 == len - 1;
            }

            /*-------------------------------------------提示相关---------------------------------------------------*/
            hasRocket(cardIdList) {
                return cardIdList.indexOf(rfa.CONSTANTS.RED_JOKER_ID) != -1 && cardIdList.indexOf(rfa.CONSTANTS.BLACK_JOKER_ID) != -1;
            }
            //得到最大顺子
            getSequence(cardIdList: string[]) {
                cardIdList.sort(rfa.utils.sortCardFunc);
                let tmp: Array<Array<string>> = [];
                let lastNumCard = null;
                //获得所有顺子
                for (let i = 0; i < cardIdList.length; i++) {
                    let cardId = cardIdList[i];
                    let numCard = rfa.utils.getCardNumber(cardId);
                    if (lastNumCard != null) {
                        if (lastNumCard == numCard) {
                            tmp[tmp.length - 1][tmp[tmp.length - 1].length - 1] = cardId;
                        } else if (lastNumCard != numCard + 1) {
                            lastNumCard = null;
                        }
                        else {
                            lastNumCard = numCard;
                            tmp[tmp.length - 1].push(cardId);
                        }
                    }
                    if (lastNumCard == null) {
                        lastNumCard = numCard;
                        tmp.push([cardId]);
                    }
                }
                //获得最长顺子
                let SequenceList: Array<string> = [];
                for (let i = 0; i < tmp.length; i++) {
                    const list = tmp[i];
                    if (list.length >= 5 && SequenceList.length <= list.length) {
                        SequenceList = list;
                    }
                }
                // console.log(SequenceList, "==========得到的最大顺子");
                return SequenceList;
            }
            getGreaterList(cardPattern, availableList) {
                // var cardPattern = this.getCardPattern(target);
                var targetType = cardPattern.getType();

                var list = null;
                switch (targetType) {
                    case rfa.CARD_TYPE.ROCKET:
                        return null;

                    case rfa.CARD_TYPE.INVALID:
                        return null;

                    default:
                        var tipsObj = rfa.TipsUtils.getTipsObj(cardPattern, availableList);
                        list = tipsObj.getTipsList();
                        break;
                }

                list = list || [];
                if (this.hasRocket(availableList))
                    list.push([rfa.CONSTANTS.RED_JOKER_ID, rfa.CONSTANTS.BLACK_JOKER_ID]);
                /*
            console.log("-------------------tips list-----------------------");
            jx.each(list, function (cardIdList) {
                console.log("usable:" + cardIdList.join(","));
            });
            */
                return list;
            }

            getDisableList(tipsObjList, availableList) {
                var tempList = [];
                jx.each(tipsObjList, function (tips) {
                    tempList = tempList.concat(tips);
                });

                //先去重
                var enableList = [];
                jx.each(tempList, function (value) {
                    var num = this.getCardNumber(value);
                    if (enableList.indexOf(num) == -1)
                        enableList.push(num);
                },
                    this
                )
                    ;

                //再求不能用的牌
                var disableList = [];
                jx.each(availableList, function (value) {
                    var num = this.getCardNumber(value);
                    if (enableList.indexOf(num) == -1 && disableList.indexOf(num) == -1)
                        disableList.push(num);
                },
                    this
                )
                    ;

                return disableList;
            }

            /*-------------------------------------------提示相关 end---------------------------------------------------*/

            /*------------------------------------------- 智能判断 end---------------------------------------------------*/
            getSingleCardSmartTips(allList, selectedIdx, cpOpponent) {
                var selectedCardId = allList[selectedIdx];
                if (this.compareCard(selectedCardId, cpOpponent.getKeyValue()) == 1)
                    return null;

                var selectedCardNum = this.getCardNumber(selectedCardId);

                var sameNumIdxList = [];
                jx.each(allList, function (cardId, i) {
                    if (this.getCardNumber(cardId) == selectedCardNum)
                        sameNumIdxList.push(i);
                },
                    this
                )
                    ;

                var getLastIdxList = function (idx, list, count) {
                    var lenList = list.length;
                    if (lenList < count)
                        return null;

                    if (lenList == count)
                        return list;

                    var hitList = [];
                    for (var i = idx; i < lenList && count > 0; ++i, --count) {
                        hitList.push(list[i]);
                    }

                    if (count > 0) {
                        for (i = 0; i < count; ++i) {
                            hitList.unshift(list[idx - 1 - i]);
                        }
                    }

                    return hitList;
                };

                var idxList = null;
                var idxTest = sameNumIdxList.indexOf(selectedIdx);
                switch (cpOpponent.getType()) {
                    case rfa.CARD_TYPE.PAIR:
                        idxList = getLastIdxList(idxTest, sameNumIdxList, 2);
                        break;

                    case rfa.CARD_TYPE.TRIPLET:
                        idxList = getLastIdxList(idxTest, sameNumIdxList, 3);
                        break;

                    case rfa.CARD_TYPE.BOMB:
                        idxList = getLastIdxList(idxTest, sameNumIdxList, 4);
                        break;

                }
                return idxList;
            }

            getSmartTips(allList, selectedIdxList, cpOpponent) {
                if (cpOpponent) {
                    if (selectedIdxList.length == 1)
                        return this.getSingleCardSmartTips(allList, selectedIdxList[0], cpOpponent);

                    var selectedCardIdList = [];
                    jx.each(selectedIdxList, function (idx) {
                        selectedCardIdList.push(allList[idx]);
                    });
                    var list = this.getGreaterList(cpOpponent, selectedCardIdList);
                    if (list != null && list.length > 0) {
                        var cardIdList = list[0];
                        var idxList = [];
                        jx.each(cardIdList, function (cardId) {
                            idxList.push(allList.indexOf(cardId))
                        });
                        return idxList;
                    }
                }
                return null;
            }

            /*------------------------------------------- 智能判断 ===---------------------------------------------------*/

        }

        export let unitTest = function (list) {
            console.log("rfa unit test!");

            jx.each(list, function (strCardIdList) {
                var cardIdList = rfa.utils.getCardIdList(strCardIdList);
                var card = rfa.utils.getCardPattern(cardIdList);
                console.log(card.getCardIdList().join(","), card.toString());
            });
        }

        export let testTipList = function (list, target) {
            var targetIdList = rfa.utils.getCardIdList(target);
            var targetPattern = rfa.utils.getCardPattern(targetIdList);
            console.log("--------------------------------------------------");
            console.log("target:" + targetPattern.getCardIdList().join(","), targetPattern.toString());


            jx.each(list, function (strCardIdList) {
                var cardIdList = rfa.utils.getCardIdList(strCardIdList);
                console.log("-----------------------usable list---------------------------");
                console.log("target:" + cardIdList.join(","));
                // rfa.utils.getSequenceList(cardIdList, targetPattern)
                var cardPattern = rfa.utils.getCardPattern(targetIdList);
                var usalbeList = rfa.utils.getGreaterList(cardPattern, cardIdList);
                // jx.each(usalbeList, function(cardIdList){
                //     console.log("usable:" + cardIdList.join(","));
                // });
            });
        }
    }
}
