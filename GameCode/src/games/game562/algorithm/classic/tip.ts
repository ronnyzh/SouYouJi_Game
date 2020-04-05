module G562 {
    export namespace twa {
        export class TipsObj {
            opponentType;
            cardIdList;
            jokerList;
            repeatCardLists;
            sameFlowerList;
            constructor(type, cardIdList) {
                this.opponentType = type;
                this.cardIdList = cardIdList;
                this.analyse();
            }
            getCardNumber(cardId) {
                return twa.utils.getCardNumber(cardId);
            }

            getCardType(cardId) {
                return twa.utils.getCardType(cardId);
            }

            getCardPattern(cardIdList, pierNum) {
                //console.log(cardIdList, "=========111111111=====getCardPattern")
                return twa.utils.getCardPattern(cardIdList, pierNum);
            }

            isJoker(cardId) {
                return twa.utils.isJoker(cardId);
            }

            isSerial(lists) {
                return twa.utils.isSerial(lists);
            }

            isSameFlower(lists) {
                return twa.utils.isSameFlower(lists);
            }

            analyse() {
                //预处理牌数组数据
                let jokerList = [];
                let repeatCardLists = [[], [], [], [], [], [], [], []];
                let numLast = this.getCardNumber(this.cardIdList[0]);
                let tmpList = [];
                for (let i = 0; i < this.cardIdList.length; ++i) {
                    let id = this.cardIdList[i];
                    if (this.isJoker(id)) {
                        jokerList.push(id);

                        if (this.cardIdList[i + 1] != null)
                            numLast = this.getCardNumber(this.cardIdList[i + 1]);
                    }
                    else {
                        let numCard = this.getCardNumber(id);
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
                }
                if (tmpList.length == 1)
                    repeatCardLists[0].push(tmpList[0]);
                else if (tmpList.length > 1)
                    repeatCardLists[tmpList.length - 1].push(tmpList);

                this.jokerList = jokerList;
               // console.log(this.jokerList, "==============this.jokerList");
                this.repeatCardLists = repeatCardLists;

                //同花色处理
                let sameFlowerList = []// { "a": [], "b": [], "c": [], "d": [] };
                sameFlowerList["a"] = [];
                sameFlowerList["b"] = [];
                sameFlowerList["c"] = [];
                sameFlowerList["d"] = [];

                for (let n = 0; n < this.cardIdList.length; ++n) {
                    let id = this.cardIdList[n];

                    if (id != twa.CONSTANTS.RED_JOKER_ID && id != twa.CONSTANTS.BLACK_JOKER_ID)
                        sameFlowerList[id.slice(-1)].push(id);
                }
                this.sameFlowerList = sameFlowerList;
            }

            getRepeatList(count) {
                return this.repeatCardLists[count - 1].concat();
            }

            getTipsList() {
                return null;
            }

            getNumList(cardIdList) {
                let excludeNumList = [];
                //   console.log(cardIdList.length, "tip-------100");
                cardIdList.forEach(id => {
                    let numCard = this.getCardNumber(id);
                    if (excludeNumList.indexOf(numCard) == -1)
                        excludeNumList.push(numCard);
                });
                return excludeNumList;
            }

            getNumCardList(count, excludeList) {
                if (this.cardIdList.length - excludeList.length < count)
                    return null;

                let excludeNumList = this.getNumList(excludeList);

                let list = [];
                for (let i = this.cardIdList.length - 1; i >= 0; --i) {
                    let id = this.cardIdList[i];
                    if (excludeNumList.indexOf(this.getCardNumber(id)) == -1)
                        list.push(id);

                    if (list.length == count)
                        break;
                }

                if (list.length >= count)
                    list.reverse();
                else
                    list = null;

                return list;
            }

            combineList(lists) {
                let ret = [];
                //  console.log(lists.length, "tip-------135");
                lists.forEach(list => {
                    ret = ret.concat(list);
                });
                return ret;
            }
            iterRepeatList(startCount, endCount, iterator) {
                for (let i = startCount; i <= endCount; ++i) {
                    let repeatList = this.getRepeatList(i);
                    if (repeatList.length > 0) {
                        for (let j = 0; j < repeatList.length; ++j) {
                            let list = repeatList[j];
                            iterator(i, list);
                        }
                    }
                }
            }

            //数组去重,去掉鬼牌
            getDuplicateRemovalData(list) {
                let data = [];
                for (let n = 0; n < list.length; n++) {
                    let id = list[n];
                    if (!this.isJoker(id)) {
                        let num = this.getCardNumber(id);

                        let oneData = data[num];
                        if (oneData == null) {
                            oneData = [id];
                            data[num] = oneData;
                        }
                        else
                            oneData.push(id)
                    }
                }
                return data;
            }

            //从列表按序取出
            getOrderListFromList(num, list) {
                let reList = [];
                let l = list.length;
                if (l < num)
                    return reList;

                for (let n = 0; n <= (l - num); n++) {
                    reList.push(list.slice(n, (n + num)));
                }

                return reList;
            }

            //列举情况
            getCombinationFromList(num, list) {
                let comNum = num;
                let comList = [];

                let fun = function (startNum, list, arr) {
                    let newList = list.concat();
                    let oneCom = arr.concat();
                    let num = startNum + 1;

                    //console.log(num);
                    //console.log("list = " + list.toString());

                    for (let i = 0; i < list.length; i++) {
                        let newArr = oneCom.concat(list[i]);

                        if (num == comNum) {
                            comList.push(newArr);

                            //console.log("comListL = " + comList.length);
                            //console.log("comList = " + comList.toString());
                        }
                        else {
                            newList.shift();

                            if (newList.length != 0)
                                fun(num, newList, newArr);
                        }
                    }
                };
                fun(0, list, []);

                return comList;
            }
        }

        export class FiveHeadsTips extends TipsObj {
            addJokerTips(tipsList) {
                let jokerNum = this.jokerList.length;
                if (jokerNum > 0) {
                    this.iterRepeatList(4, 8, function (count, list) {
                        tipsList.push([this.jokerList[jokerNum - 1]].concat(list.slice(count - 4)));
                    }.bind(this));

                    if (jokerNum == 2) {
                        this.iterRepeatList(3, 8, function (count, list) {
                            tipsList.push(this.jokerList.concat(list.slice(count - 3)));
                        }.bind(this));
                    }
                }
            }

            getTipsList() {
                let tipsList = [];
                this.iterRepeatList(5, 8, function (count, list) {
                    tipsList.push(list.slice(count - 5));
                }.bind(this));

                this.addJokerTips(tipsList);

                return tipsList;
            }
        }

        export class StraightFlushTips extends TipsObj {
            //取出顺子
            getStraightList(list) {
              //  console.log(list, "==取出顺子==list");
                let reList = [];
                let l = list.length;
                let jokerNum = this.jokerList.length;
                if ((l + jokerNum) < 5)
                    return reList;
                //  console.log(this.jokerList, "===========this.jokerList");
              //  console.log(jokerNum, "============jokerNum");
                let duplicateRemovalList = [];
                let duplicateRemovalData = this.getDuplicateRemovalData(list);
                // console.log(duplicateRemovalData.length, "tip--------262");
                duplicateRemovalData.forEach(_list => {
                    duplicateRemovalList.push(_list[0]);
                });
                duplicateRemovalList = duplicateRemovalList.sort(twa.utils.sortCardFunc);
                let orderList0 = this.getOrderListFromList(5, duplicateRemovalList);
                // console.log(orderList0, orderList0.length, "tip--------268");
                Tools.inst.each(orderList0, (_list) => {
                    if (this.getCardNumber(_list[0]) - this.getCardNumber(_list[4]) == 4) {
                        reList.push(_list);
                        // console.log(reList.concat(), "==11111111=============reList");
                    }
                });
                //放一张鬼牌
                if (jokerNum >= 1) {
                    let orderList1 = this.getOrderListFromList(4, duplicateRemovalList);
                    // console.log(orderList1.length, "tip--------278");
                    orderList1.forEach(_list => {
                        let diffNum = this.getCardNumber(_list[0]) - this.getCardNumber(_list[3]);
                        if (diffNum == 4 || diffNum == 3) {
                            reList.push([this.jokerList[jokerNum - 1]].concat(_list));
                            // console.log(reList.concat(), "=======222222222========reList");
                        }
                    });
                }

                //放两张鬼牌
                if (jokerNum == 2) {
                    let orderList2 = this.getOrderListFromList(3, duplicateRemovalList);
                    // console.log(orderList2.length, "tip--------290");
                    orderList2.forEach(_list => {
                        let diffNum = this.getCardNumber(_list[0]) - this.getCardNumber(_list[2]);
                        if (diffNum == 4 || diffNum == 3 || diffNum == 2) {
                            reList.push(this.jokerList.concat(_list));
                            // console.log(reList.concat(), "========33333333333=======reList");
                        }
                    });
                }
               // console.log(reList.concat(), "===============reList");
                return reList;
            }

            getTipsList() {
                let tipsList = [];
                for (let _key in this.sameFlowerList) {
                    if (this.sameFlowerList.hasOwnProperty(_key)) {
                        let _list = this.sameFlowerList[_key];
                        let straightList = this.getStraightList(_list);
                        tipsList = tipsList.concat(straightList);
                    }
                }

                return tipsList;
            }
        }

        export class IronBranchTips extends TipsObj {
            addJokerTips(tipsList) {
                let jokerNum = this.jokerList.length;
                if (jokerNum > 0) {
                    this.iterRepeatList(3, 8, function (count, list) {
                        tipsList.push([this.jokerList[jokerNum - 1]].concat(list.slice(count - 3)));
                    }.bind(this));

                    if (jokerNum == 2) {
                        this.iterRepeatList(2, 8, function (count, list) {
                            tipsList.push(this.jokerList.concat(list.slice(count - 2)));
                        }.bind(this));
                    }
                }
            }

            getTipsList() {
                let tipsList = [];
                this.iterRepeatList(4, 8, function (count, list) {
                    tipsList.push(list.slice(count - 4));
                }.bind(this));

                this.addJokerTips(tipsList);

                return tipsList;
            }
        }

        export class GourdTips extends TipsObj {
            addJokerTips1(tipsList) {
                let jokerNum = this.jokerList.length;
                if (jokerNum == 1) {
                    let tripletList = [];
                    this.iterRepeatList(2, 8, function (count, list) {
                        tripletList.push([this.jokerList[jokerNum - 1]].concat(list.slice(count - 2)));
                    }.bind(this));

                    let pairList = [];
                    this.iterRepeatList(2, 8, function (count, list) {
                        pairList.push(list.slice(count - 2));
                    }.bind(this));

                    for (let i = 0; i < tripletList.length; i++) {
                        let oneTriplet = tripletList[i];
                        for (let j = 0; j < pairList.length; j++) {
                            let onePair = pairList[j];

                            if (this.getCardNumber(oneTriplet[2]) != this.getCardNumber(onePair[1])) {
                                tipsList.push(oneTriplet.concat(onePair));
                            }
                        }
                    }
                }
            }

            addJokerTips2(tipsList) {
                let jokerNum = this.jokerList.length;
                if (jokerNum == 1) {
                    let tripletList = [];
                    this.iterRepeatList(3, 8, function (count, list) {
                        tripletList.push(list.slice(count - 3));
                    }.bind(this));

                    let pairList = [];
                    this.iterRepeatList(1, 8, function (count, list) {
                        pairList.push([this.jokerList[jokerNum - 1]].concat(list.slice(count - 1)));
                    }.bind(this));

                    for (let i = 0; i < tripletList.length; i++) {
                        let oneTriplet = tripletList[i];
                        for (let j = 0; j < pairList.length; j++) {
                            let onePair = pairList[j];

                            if (this.getCardNumber(oneTriplet[2]) != this.getCardNumber(onePair[1])) {
                                tipsList.push(oneTriplet.concat(onePair));
                            }
                        }
                    }
                }
            }

            getTipsList() {
                let tipsList = [];

                let tripletList = [];
                this.iterRepeatList(3, 8, function (count, list) {
                    tripletList.push(list.slice(count - 3));
                }.bind(this));

                let pairList = [];
                this.iterRepeatList(2, 8, function (count, list) {
                    pairList.push(list.slice(count - 2));
                }.bind(this));

                for (let i = 0; i < tripletList.length; i++) {
                    let oneTriplet = tripletList[i];
                    for (let j = 0; j < pairList.length; j++) {
                        let onePair = pairList[j];

                        if (this.getCardNumber(oneTriplet[0]) != this.getCardNumber(onePair[0])) {
                            tipsList.push(oneTriplet.concat(onePair));
                        }
                    }
                }

                this.addJokerTips1(tipsList);
                this.addJokerTips2(tipsList);

                return tipsList;
            }
        }

        export class FlushTips extends TipsObj {
            getTipsList() {
                let tipsList = [];

                let maxLength = 0;
                let flowerList = [];
                // console.log(this.sameFlowerList, "==========this.sameFlowerList")
                for (let key in this.sameFlowerList) {
                    if (this.sameFlowerList.hasOwnProperty(key)) {
                        let list = this.sameFlowerList[key];
                        let listLength = list.length;
                        if (listLength > maxLength) {
                            flowerList.push(key);
                            maxLength = listLength;
                        }
                        else {
                            flowerList.unshift(key);
                        }
                    }
                }

                let jokerNum = this.jokerList.length;
                for (let i = 0; i < 4; i++) {
                    // console.log(flowerList, "==========flowerList")
                    if (flowerList[i] != null) {
                        let list = this.sameFlowerList[flowerList[i]];
                        // console.log(list, "===============list")
                        if (list.length >= 5 - jokerNum)
                            tipsList = tipsList.concat(this.getCombinationFromList(5, this.jokerList.concat(list)));

                    }
                }

                let list1 = [];
                let list2 = [];
                for (let n = 0; n < tipsList.length; n++) {
                    let oneList = tipsList[n];

                    if (!this.isSerial(oneList)) {
                        if (oneList.indexOf(twa.CONSTANTS.RED_JOKER_ID) == -1 && oneList.indexOf(twa.CONSTANTS.BLACK_JOKER_ID) == -1)
                            list1.push(oneList);
                        else
                            list2.push(oneList)
                    }
                }

                return list1.concat(list2);
            }
        }

        export class StraightTips extends TipsObj {
            getTipsList() {
                let list = this.cardIdList.concat();
                let reList = [];
                let l = list.length;
                let jokerNum = this.jokerList.length;
                if ((l + jokerNum) < 5)
                    return reList;

                let lastColor = null;
                let duplicateRemovalList = [];
                let duplicateRemovalData = this.getDuplicateRemovalData(list);
                //  console.log(duplicateRemovalData.length, "tip--------489");

                duplicateRemovalData.forEach(_list => {
                    var listL = _list.length;
                    for (var n = 0; n < listL; n++) {
                        var id = _list[n];
                        var color = this.getCardType(id);
                        if (lastColor == null || lastColor != color || n == (listL - 1)) {
                            lastColor = color;
                            duplicateRemovalList.push(id);
                            break;
                        }
                    }
                });

                duplicateRemovalList = duplicateRemovalList.sort(twa.utils.sortCardFunc);
                let orderList0 = this.getOrderListFromList(5, duplicateRemovalList);
               // console.log(orderList0, orderList0.length, "tip--------506");
                orderList0.forEach(_list => {
                    //  console.log(_list, "============list")
                    if (this.getCardNumber(_list[0]) - this.getCardNumber(_list[4]) == 4) {
                        if (!this.isSameFlower(_list))
                            reList.push(_list);
                    }
                });

                //放一张鬼牌
                if (jokerNum >= 1) {
                    let orderList1 = this.getOrderListFromList(4, duplicateRemovalList);
                    //console.log(orderList1.length, "tip--------518");
                    orderList1.forEach(_list => {
                        let diffNum = this.getCardNumber(_list[0]) - this.getCardNumber(_list[3]);
                        if (diffNum == 4 || diffNum == 3) {
                            if (!this.isSameFlower(_list))
                                reList.push([this.jokerList[jokerNum - 1]].concat(_list));
                        }
                    });
                }

                //放两张鬼牌
                if (jokerNum == 2) {
                    let orderList2 = this.getOrderListFromList(3, duplicateRemovalList);
                    // console.log(orderList2.length, "tip--------531");
                    orderList2.forEach(_list => {
                        let diffNum = this.getCardNumber(_list[0]) - this.getCardNumber(_list[2]);
                        if (diffNum == 4 || diffNum == 3 || diffNum == 2) {
                            if (!this.isSameFlower(_list))
                                reList.push(this.jokerList.concat(_list));
                        }
                    });
                }

                return reList;
            }
        }

        export class TripletTips extends TipsObj {
            addJokerTips(tipsList) {
                let jokerNum = this.jokerList.length;
                if (jokerNum > 1) {
                    this.iterRepeatList(2, 8, function (count, list) {
                        tipsList.push([this.jokerList[jokerNum - 1]].concat(list.slice(count - 2)));
                    }.bind(this));

                    if (jokerNum == 2) {
                        this.iterRepeatList(1, 8, function (count, list) {
                            tipsList.push(this.jokerList.concat(list.slice(count - 1)));
                        }.bind(this));
                    }
                }
            }

            getTipsList() {
                let tipsList = [];
                this.iterRepeatList(3, 8, function (count, list) {
                    tipsList.push(list.slice(count - 3));
                }.bind(this));

                this.addJokerTips(tipsList);

                return tipsList;
            }
        }

        export class TwoPairTips extends TipsObj {
            getTipsList() {
                let tipsList = [];

                let pairList = [];
                this.iterRepeatList(2, 8, function (count, list) {
                    pairList.push(list.slice(count - 2));
                }.bind(this));

                let list = this.getCombinationFromList(2, pairList);
                for (let i = 0; i < list.length; i++) {
                    let oneList = list[i];
                    tipsList.push(oneList);
                }

                return tipsList;
            }
        }

        export class PairTips extends TipsObj {
            addJokerTips(tipsList) {
                let jokerNum = this.jokerList.length;
                if (jokerNum > 1) {
                    this.iterRepeatList(1, 8, function (count, list) {
                        tipsList.push([this.jokerList[jokerNum - 1]].concat(list.slice(count - 1)));
                    }.bind(this));
                }
            }

            getTipsList() {
                let tipsList = [];
                this.iterRepeatList(2, 8, function (count, list) {
                    tipsList.push(list.slice(count - 2));
                }.bind(this));

                this.addJokerTips(tipsList);

                return tipsList;
            }
        }

        export class TipsUtils {
            static getTipsObj(type, cardIdList) {
                let obj = null;
                switch (type) {
                    case twa.CARD_TYPE.FIVE_HEADS:
                        obj = new twa.FiveHeadsTips(type, cardIdList);
                        break;

                    case twa.CARD_TYPE.STRAIGHT_FLUSH:
                        obj = new twa.StraightFlushTips(type, cardIdList);
                        break;

                    case twa.CARD_TYPE.IRON_BRANCH:
                        obj = new twa.IronBranchTips(type, cardIdList);
                        break;

                    case twa.CARD_TYPE.GOURD:
                        obj = new twa.GourdTips(type, cardIdList);
                        break;

                    case twa.CARD_TYPE.FLUSH:
                        obj = new twa.FlushTips(type, cardIdList);
                        break;

                    case twa.CARD_TYPE.STRAIGHT:
                        obj = new twa.StraightTips(type, cardIdList);
                        break;

                    case twa.CARD_TYPE.TRIPLET:
                        obj = new twa.TripletTips(type, cardIdList);
                        break;

                    case twa.CARD_TYPE.TWO_PAIR:
                        obj = new twa.TwoPairTips(type, cardIdList);
                        break;

                    case twa.CARD_TYPE.PAIR:
                        obj = new twa.PairTips(type, cardIdList);
                        break;
                }
                return obj;
            }
        }

        export class AutoArrangedCards {
            static getRemovedList(cusList, sublist) {
                let list = cusList.concat();
                for (let n = 0; n < sublist.length; n++) {
                    let id = sublist[n];
                    list.splice(list.indexOf(id), 1);
                }

                return list;
            }

            static getArrangedCardsList(cardIdList, tipsData) {
                let arrangedCardsList = [];
                let cardIdLists = [["", "", ""], ["", "", "", "", ""], ["", "", "", "", ""]];

                let self = this;
                let fun = function (num, startNum, cards, tipsData, compareCard) {
                    if (num == 0) {
                        let arrangedCards = self.addRemainingCardsInLists(cards, cardIdLists);
                       // console.log(arrangedCards, "==========arrangedCards");
                        arrangedCardsList.push(arrangedCards);

                        return;
                    }

                    for (let n = startNum; n >= 0; n--) {
                        if (n == 0) {
                            let tips0 = [cards[0]];
                            //console.log(tips0, "==================tips0");
                            self.addTipsInLists(tips0, cardIdLists[num - 1]);

                            let remainingCards0 = self.getRemovedList(cards, tips0);
                            let remainingCardsTipsData0 = twa.utils.getTipsDataList(remainingCards0);
                          //  console.log(cardIdLists.concat(), "============111111111===========cardIdList");
                            fun((num - 1), n, remainingCards0, remainingCardsTipsData0, tips0[0]);
                        }
                        else {
                            //首墩类型校验
                            if (num == 1 && (n > 4 || n == 2))
                                continue;

                            let tipsList = tipsData[n];

                            if (tipsList == null)
                                continue;

                            for (let m = 0; m < tipsList.length; m++) {
                                if ((n == 5 || n == 6) && m > 8)
                                    continue;

                                let tips = tipsList[m];
                                if (compareCard != null && n == startNum) {
                                    if (twa.utils.getCardNumber(compareCard) < twa.utils.getCardNumber(tips[0]))
                                        continue;
                                }

                                self.addTipsInLists(tips, cardIdLists[num - 1]);

                                let remainingCards = self.getRemovedList(cards, tips);
                                let remainingCardsTipsData = twa.utils.getTipsDataList(remainingCards);
                              //  console.log(cardIdLists.concat(), "============22222222===========cardIdList");
                                fun((num - 1), n, remainingCards, remainingCardsTipsData, tips[0]);
                            }
                        }

                        //清空
                        cardIdLists[num - 1] = (num == 1 ? ["", "", ""] : ["", "", "", "", ""]);
                    }
                };
               // console.log(cardIdLists.concat(), "===========333333333==========cardIdList");
                fun(3, 10, cardIdList, tipsData, null);

                return arrangedCardsList;
            }

            static addTipsInLists(tips, cardIdList) {
                for (let n = 0; n < tips.length; n++) {
                    cardIdList[n] = tips[n];
                }
            }

            static addRemainingCardsInLists(cards, lists) {
                let cloneLists = [lists[0].concat(), lists[1].concat(), lists[2].concat()];
               // console.log(cloneLists.concat(), "============cloneLists")
                let num = 0;
                for (let n = 0; n < cloneLists.length; n++) {
                    let list = cloneLists[n];
                    for (let m = 0; m < list.length; m++) {
                        let id = list[m];
                        let inId = cards[num];
                        if (id == "") {
                            list[m] = inId;
                            num++;
                        }
                    }
                }
               // console.log(cloneLists.concat(), "=======111111111=====cloneLists")
                return cloneLists;
            }

            static getAutoArrangedCardsData(cardIdList, tipsData) {
                let data = {};
                let typeKeyList = [];

                let arrangedList = this.getArrangedCardsList(cardIdList, tipsData);

                for (let i = 0; i < arrangedList.length; i++) {
                    let oneArrangedList = arrangedList[i];
                    // console.log(oneArrangedList[0].sort(twa.utils.sortCardFunc), "=====4444444444=========getCardPattern");
                    //  console.log(oneArrangedList[1].sort(twa.utils.sortCardFunc), "=====555555555========getCardPattern");
                  //  console.log(oneArrangedList[2], "=====66666666666=========getCardPattern");
                //    console.log(oneArrangedList[2].sort, "===========oneArrangedList[2].sort");
                    let cardPattern1 = this.getCardPattern(oneArrangedList[0].sort(twa.utils.sortCardFunc), 1);
                    let cardPattern2 = this.getCardPattern(oneArrangedList[1].sort(twa.utils.sortCardFunc), 2);
                    let cardPattern3 = this.getCardPattern(oneArrangedList[2].sort(twa.utils.sortCardFunc), 3);
                    let type1 = cardPattern1.getType();
                    let type2 = cardPattern2.getType();
                    let type3 = cardPattern3.getType();

                    if (cardPattern3.greaterThan(cardPattern2) && cardPattern2.greaterThan(cardPattern1)) {
                        let typeKey = type1 + "-" + type2 + "-" + type3;
                        if (data[typeKey] == null)
                            data[typeKey] = [cardPattern1, cardPattern2, cardPattern3];
                        else {
                            let oldCardPatternList = data[typeKey];
                            for (let n = 2; n >= 0; n--) {
                                let oldCardPattern = oldCardPatternList[n];

                                // console.log(oneArrangedList[n].sort(twa.utils.sortCardFunc), "========777777777======getCardPattern");
                                let newCardPattern = this.getCardPattern(oneArrangedList[n].sort(twa.utils.sortCardFunc), n + 1);

                                if (newCardPattern.getKeyValue()[0] == oldCardPattern.getKeyValue()[0])
                                    continue;

                                if (newCardPattern.greaterThan(oldCardPattern))
                                    data[typeKey] = [cardPattern1, cardPattern2, cardPattern3];

                                break;
                            }
                        }

                        if (typeKeyList.indexOf(typeKey) == -1)
                            typeKeyList.push(typeKey);
                    }
                }

                return { typeKeyList: typeKeyList.sort(this.typeKeyListSortFunc), arrangedCardsData: data };
            }

            static typeKeyListSortFunc(type1, type2) {
                let list1 = type1.split("-");
                let list2 = type2.split("-");

                let type11 = parseInt(list1[0]);
                let type12 = parseInt(list1[1]);
                let type13 = parseInt(list1[2]);
                let type21 = parseInt(list2[0]);
                let type22 = parseInt(list2[1]);
                let type23 = parseInt(list2[2]);

                //先用分数排序
                let scoreList1 = [0, 0, 0, 2, 20, 0, 0, 0, 0, 0, 0];
                let scoreList2 = [0, 0, 0, 0, 0, 0, 0, 1, 7, 9, 19];
                let scoreList3 = [0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 9];
                let typeScore1 = scoreList1[type11] + scoreList2[type12] + scoreList3[type13];
                let typeScore2 = scoreList1[type21] + scoreList2[type22] + scoreList3[type23];
                if (typeScore1 != typeScore2)
                    return (typeScore1 > typeScore2 ? -1 : 1);

                //分数一样用牌型排序
                if (type23 != type13)
                    return (type13 > type23 ? -1 : 1);
                else if (type22 != type12)
                    return (type12 > type22 ? -1 : 1);
                else
                    return (type11 > type21 ? -1 : 1);
            }

            static getCardPattern(cardIdList, pierNum) {
                //  console.log(cardIdList,"=============2222222222getCardPattern")
                return twa.utils.getCardPattern(cardIdList, pierNum);
            }
        }
    }
}