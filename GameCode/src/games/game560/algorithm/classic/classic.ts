/**
 * Created by Administrator on 2018/4/17.
 */
module G560 {
    export namespace fla {
        export let utils;
        export let initUtils = function () {
            fla.utils = new fla.ClassicUtils();
        };

        export class ClassicUtils {
            public sortCardFunc;

            constructor() {
                this.sortCardFunc = this.compareCard.bind(this);
            }

            isJoker(cardId) {
                return cardId == fla.CONSTANTS.RED_JOKER_ID || cardId == fla.CONSTANTS.BLACK_JOKER_ID;
            }

            hasJoker(cardIdList) {
                for (var i = 0; i < cardIdList.length; ++i) {
                    if (this.isJoker(cardIdList[i]))
                        return true;
                }
                return false;
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
                return fla.CONSTANTS.cardNumMap[num];
            }

            getCardType(cardId) {
                return cardId.charAt(cardId.length - 1);
            }

            //isAll表示是否是所有牌
            getCardPattern(cardIdList?) {
                var lenCards = cardIdList.length;
                //单牌
                if (lenCards == 1)
                    return fla.CardPatternFactory.getPattern(fla.CARD_TYPE.SINGLE_CARD, cardIdList);

                //对子
                else if (lenCards == 2) {
                    var id1 = cardIdList[0];
                    var id2 = cardIdList[1];
                    if (id1 == fla.CONSTANTS.RED_JOKER_ID && id2 == fla.CONSTANTS.BLACK_JOKER_ID)
                        return fla.CardPatternFactory.getPattern(fla.CARD_TYPE.ROCKET);
                    else if (this.getCardNumber(id1) == this.getCardNumber(id2))
                        return fla.CardPatternFactory.getPattern(fla.CARD_TYPE.PAIR, cardIdList);
                }

                //三条
                else if (lenCards == 3) {
                    var id1 = cardIdList[0];
                    var id2 = cardIdList[2];

                    if (this.getCardNumber(id1) == this.getCardNumber(id2)) {
                        return fla.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET, cardIdList);
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


                    //四带一，四带二，炸弹
                    if (repeatCardList4.length == 1) {
                        if (lenCards == 6)
                            return fla.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_ONE, this.getPatternIdList(repeatCardList4, cardIdList));
                        else if (lenCards == 8 && repeatCardList2.length == 2)
                            return fla.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, this.getPatternIdList(repeatCardList4, cardIdList));
                        else if (lenCards == 4)
                            return fla.CardPatternFactory.getPattern(fla.CARD_TYPE.BOMB, cardIdList);
                    }
                    //四带四当做四带二
                    if (repeatCardList4.length == 2 && lenCards == 8)
                        return fla.CardPatternFactory.getPattern(fla.CARD_TYPE.QUADPLEX_SET_WITH_TWO, this.getPatternIdList(repeatCardList4, cardIdList));

                    //三带一，三带二
                    if (repeatCardList3.length == 1) {
                        if (lenCards == 4)
                            return fla.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_ONE, this.getPatternIdList(repeatCardList3, cardIdList));
                        else if (lenCards == 5 && repeatCardList2.length == 1)
                            return fla.CardPatternFactory.getPattern(fla.CARD_TYPE.TRIPLET_WITH_TWO, this.getPatternIdList(repeatCardList3, cardIdList));
                    }
                    //飞机
                    else if (repeatCardList3.length > 1 && fla.utils.isSerial(repeatCardList3)) {
                        if (lenCards == 3 * repeatCardList3.length) {
                            return fla.CardPatternFactory.getPattern(fla.CARD_TYPE.SEQUENCE_OF_TRIPLETS, cardIdList);
                        }
                        else if (lenCards == 4 * repeatCardList3.length)
                            return fla.CardPatternFactory.getPattern(fla.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_ONE, this.getPatternIdList(repeatCardList3, cardIdList));
                        else if (lenCards == 5 * repeatCardList3.length &&
                            (repeatCardList4.length * 2 + repeatCardList2.length == repeatCardList3.length))//4张拆成2对
                            return fla.CardPatternFactory.getPattern(fla.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_TWO, this.getPatternIdList(repeatCardList3, cardIdList));
                    }

                    // 飞机(有可能带炸弹的算法)
                    if ((repeatCardList4.length > 0 && repeatCardList3.length > 0) || repeatCardList4.length > 2) {
                        var repeatCardList3_4 = [].concat(repeatCardList3, repeatCardList4.map(function (arr) {
                            return arr.concat().splice(0, 3);
                        }));
                        //这个排序为了正确对比是否连号
                        repeatCardList3_4.sort(function (a, b) { return b[0] - a[0] });
                        if (lenCards == 4 * repeatCardList3_4.length && fla.utils.isSerial(repeatCardList3_4)) {
                            return fla.CardPatternFactory.getPattern(
                                fla.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_ONE,
                                this.getPatternIdList(repeatCardList3_4, cardIdList)
                            );
                        }
                    }

                    //双顺子
                    if (repeatCardList2.length >= 3 && repeatCardList2.length * 2 == lenCards && fla.utils.isSerial(repeatCardList2))
                        return fla.CardPatternFactory.getPattern(fla.CARD_TYPE.SEQUENCE_OF_PAIRS, cardIdList);

                    //单顺子
                    if (repeatCardList1.length == lenCards && repeatCardList1.length >= 5) {
                        var num1 = this.getCardNumber(repeatCardList1[0]);
                        if (num1 <= 14) {
                            var num2 = this.getCardNumber(repeatCardList1[lenCards - 1]);
                            if (num1 - num2 == lenCards - 1)
                                return fla.CardPatternFactory.getPattern(fla.CARD_TYPE.SEQUENCE, cardIdList);
                        }
                    }
                }

                return fla.CardPatternFactory.getPattern(fla.CARD_TYPE.INVALID, cardIdList);
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
                return cardIdList.indexOf(fla.CONSTANTS.RED_JOKER_ID) != -1 && cardIdList.indexOf(fla.CONSTANTS.BLACK_JOKER_ID) != -1;
            }
            //得到最大顺子
            getSequence(cardIdList: string[]) {
                cardIdList.sort(fla.utils.sortCardFunc);
                let tmp: Array<Array<string>> = [];
                let lastNumCard = null;
                //获得所有顺子
                for (let i = 0; i < cardIdList.length; i++) {
                    let cardId = cardIdList[i];
                    let numCard = fla.utils.getCardNumber(cardId);
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
                    case fla.CARD_TYPE.ROCKET:
                        return null;

                    case fla.CARD_TYPE.INVALID:
                        return null;

                    default:
                        var tipsObj = fla.TipsUtils.getTipsObj(cardPattern, availableList);
                        list = tipsObj.getTipsList();
                        break;
                }

                list = list || [];
                if (this.hasRocket(availableList))
                    list.push([fla.CONSTANTS.RED_JOKER_ID, fla.CONSTANTS.BLACK_JOKER_ID]);

              //  console.log("-------------------tips list-----------------------");
                jx.each(list, function (cardIdList) {
                    //console.log("usable:" + cardIdList.join(","));
                    cardIdList.join(",");
                });

                return list;
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
                    case fla.CARD_TYPE.PAIR:
                        idxList = getLastIdxList(idxTest, sameNumIdxList, 2);
                        break;

                    case fla.CARD_TYPE.TRIPLET:
                        idxList = getLastIdxList(idxTest, sameNumIdxList, 3);
                        break;

                    case fla.CARD_TYPE.BOMB:
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
            console.log("fla unit test!");

            jx.each(list, function (strCardIdList) {
                var cardIdList = fla.utils.getCardIdList(strCardIdList);
                var card = fla.utils.getCardPattern(cardIdList);
                console.log(card.getCardIdList().join(","), card.toString());
            });
        }

        export let testTipList = function (list, target) {
            var targetIdList = fla.utils.getCardIdList(target);
            var targetPattern = fla.utils.getCardPattern(targetIdList);
            console.log("--------------------------------------------------");
            console.log("target:" + targetPattern.getCardIdList().join(","), targetPattern.toString());


            jx.each(list, function (strCardIdList) {
                var cardIdList = fla.utils.getCardIdList(strCardIdList);
                console.log("-----------------------usable list---------------------------");
                console.log("target:" + cardIdList.join(","));
                // fla.utils.getSequenceList(cardIdList, targetPattern)
                var cardPattern = fla.utils.getCardPattern(targetIdList);
                var usalbeList = fla.utils.getGreaterList(cardPattern, cardIdList);
                // jx.each(usalbeList, function(cardIdList){
                //     console.log("usable:" + cardIdList.join(","));
                // });
            });
        }
    }
}
