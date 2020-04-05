module G562 {
    export class G562classic {
        public sortCardFunc;
        constructor() {
            this.sortCardFunc = this.compareCard.bind(this);
        }
        isJoker(cardId) {
            // console.log(cardId, "============cardId");
            return cardId == twa.CONSTANTS.RED_JOKER_ID || cardId == twa.CONSTANTS.BLACK_JOKER_ID;
        }
        //card2是否大过card1
        greaterThan(card1, card2) {
            return this.getCardNumber(card2) > this.getCardNumber(card1);
        }

        //获得形成牌型后的排序列表
        getPatternIdList(mainList, cardIdList) {
            let patternIdList = [];
            // console.log(mainList.length, "classic--------19");
            mainList.forEach(list => {
                patternIdList = patternIdList.concat(list);
            });

            mainList = this.combineList(mainList);
            //  console.log(cardIdList.length, "classic--------25");
            cardIdList.forEach(cardId => {
                if (mainList.indexOf(cardId) == -1)
                    patternIdList.push(cardId);
            });
            return patternIdList;
        }

        combineList(lists) {
            let ret = [];
            // console.log(lists.length, "classic--------35");
            lists.forEach(list => {
                ret = ret.concat(list);
            });
            return ret;
        }

        transferCardId(id) {
            return id;
        }

        compareCard(id1, id2) {
            let num1 = this.getCardNumber(id1);
            let num2 = this.getCardNumber(id2);
            if (num1 == num2) {
                let type1 = this.getCardType(id1);
                let type2 = this.getCardType(id2);
                return type1 > type2 ? -1 : 1;
            }
            return num1 > num2 ? -1 : 1;
        }

        getCardIdList(str) {
            let list = str.split(",");
            // console.log(list.length, "classic--------60");
            list.forEach((id, i) => {
                list[i] = this.transferCardId(id);
            });
            list.sort(this.sortCardFunc);
            return list;
        }

        getCardNumber(cardId) {
            //console.log(cardId, "==========cardId");
            let num = cardId[0];
            // console.log(num, "==============num");
            return twa.CONSTANTS.cardNumMap[num];
        }

        getCardType(cardId) {
            return cardId.charAt(cardId.length - 1);
        }

        getJokerNum(list) {
            let num = 0;
            //  console.log(list.length, "classic--------81");
            list.forEach(id => {
                if (this.isJoker(id))
                    num++;
            });
            return num;
        }
        getJokerTurnList(num, idNum, idType) {
            let list = [];
            if (num == 0)
                return list;

            for (let i = 0; i < num; i++) {
                list.push(twa.CONSTANTS.valueMap[Array.isArray(idNum) ? idNum[i] : idNum] + idType);
            }

            return list;
        }

        //获得牌型
        getCardPattern(cardIdList, pierNum) {
           // console.log(cardIdList, pierNum, "=============获得牌型");
            let length = cardIdList.length;
            if ((pierNum == 1 && length != 3) || (pierNum != 1 && length != 5)) {
                console.log(".........error cardIdList..........");
                return null;
            }
            // console.log(cardIdList, "===============cardIdList");
            let cardPatternList = cardIdList;
            let jokerNum = this.getJokerNum(cardIdList);
            let jokerTurnList = [];

            if (pierNum == 1 && jokerNum == 2) {
                jokerTurnList = this.getJokerTurnList(jokerNum, this.getCardNumber(cardIdList[length - 1]), "d");
                return twa.CardPatternFactory.getPattern(twa.CARD_TYPE.DOUBLE_GHOST, cardPatternList, pierNum, jokerNum, jokerTurnList);
            }

            //预处理牌数组数据
            let repeatCardLists = [[], [], [], [], []];
            let repeatCardList1 = repeatCardLists[0];
            let repeatCardList2 = repeatCardLists[1];
            let repeatCardList3 = repeatCardLists[2];
            let repeatCardList4 = repeatCardLists[3];
            let repeatCardList5 = repeatCardLists[4];

            let numLast = this.getCardNumber(cardIdList[0]);
            let tmpList = [];
            //  console.log(cardIdList.length, "classic--------127");
            cardIdList.forEach((id, key) => {
                if (this.isJoker(id)) {
                    if (cardIdList[key + 1] != null)
                        numLast = this.getCardNumber(cardIdList[key + 1]);
                }
                else {
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
            });
            if (tmpList.length == 1)
                repeatCardLists[0].push(tmpList[0]);
            else if (tmpList.length > 1)
                repeatCardLists[tmpList.length - 1].push(tmpList);
            // console.log(repeatCardLists, "++++++++++++++++++repeatCardLists");
            //同花顺子处理
            let sameFlower = this.getSameFlower(cardIdList);
            let serialData = this.getSerialData(cardIdList, repeatCardList1, jokerNum);
            //  console.log(sameFlower, "=================sameFlower");
            //  console.log(serialData, "==============serialData");
            //  console.log(jokerNum, "=======jokerNum");
            if ((repeatCardList5.length == 1) || (repeatCardList4.length == 1 && jokerNum == 1) || (repeatCardList3.length == 1 && jokerNum == 2)) {
                if (jokerNum == 1) {
                    cardPatternList = this.getPatternIdList(repeatCardList4, cardIdList);
                    // console.log(cardPatternList, "=======111111111cardPatternList");
                }
                else if (jokerNum == 2) {
                    cardPatternList = this.getPatternIdList(repeatCardList3, cardIdList);
                    // console.log(cardPatternList, "=======2222222222cardPatternList");
                }
                jokerTurnList = this.getJokerTurnList(jokerNum, this.getCardNumber(cardPatternList[0]), "d");
                return twa.CardPatternFactory.getPattern(twa.CARD_TYPE.FIVE_HEADS, cardPatternList, pierNum, jokerNum, jokerTurnList);
            }

            else if (sameFlower != null && serialData != null && pierNum != 1) {
                cardPatternList = serialData.idList;
                //  console.log(cardPatternList, "=======33333333333cardPatternList");
                jokerTurnList = this.getJokerTurnList(jokerNum, serialData.jokerTurnList, sameFlower);
                return twa.CardPatternFactory.getPattern(twa.CARD_TYPE.STRAIGHT_FLUSH, cardPatternList, pierNum, jokerNum, jokerTurnList);
            }

            else if ((repeatCardList4.length == 1) || (repeatCardList3.length == 1 && jokerNum == 1) || (repeatCardList2.length == 1 && jokerNum == 2)) {
                if (jokerNum == 0)
                    cardPatternList = this.getPatternIdList(repeatCardList4, cardIdList);
                else if (jokerNum == 1)
                    cardPatternList = this.getPatternIdList(repeatCardList3, cardIdList);
                else if (jokerNum == 2)
                    cardPatternList = this.getPatternIdList(repeatCardList2, cardIdList);

                // console.log(cardPatternList, "=======4444444444cardPatternList");
                jokerTurnList = this.getJokerTurnList(jokerNum, this.getCardNumber(cardPatternList[0]), "d");
                return twa.CardPatternFactory.getPattern(twa.CARD_TYPE.IRON_BRANCH, cardPatternList, pierNum, jokerNum, jokerTurnList);
            }

            else if ((repeatCardList3.length == 1 && repeatCardList2.length == 1) || (repeatCardList2.length == 2 && jokerNum == 1)) {
                if (jokerNum == 0)
                    cardPatternList = this.getPatternIdList(repeatCardList3, cardIdList);
                else if (jokerNum == 1)
                    cardPatternList = this.getPatternIdList([repeatCardList2[0]], cardIdList);
                // console.log(cardPatternList, "=======555555555cardPatternList");
                jokerTurnList = this.getJokerTurnList(jokerNum, this.getCardNumber(cardPatternList[0]), "d");
                return twa.CardPatternFactory.getPattern(twa.CARD_TYPE.GOURD, cardPatternList, pierNum, jokerNum, jokerTurnList);
            }

            else if (sameFlower != null && pierNum != 1) {
                jokerTurnList = this.getJokerTurnList(jokerNum, twa.CONSTANTS.cardNumMap["A"], sameFlower);
                return twa.CardPatternFactory.getPattern(twa.CARD_TYPE.FLUSH, cardPatternList, pierNum, jokerNum, jokerTurnList);
            }

            else if (serialData != null && pierNum != 1) {
                cardPatternList = serialData.idList;
                //  console.log(cardPatternList, "=======6666666666cardPatternList");
                jokerTurnList = this.getJokerTurnList(jokerNum, serialData.jokerTurnList, "d");
                return twa.CardPatternFactory.getPattern(twa.CARD_TYPE.STRAIGHT, cardPatternList, pierNum, jokerNum, jokerTurnList);
            }
            else if ((repeatCardList3.length == 1) || (repeatCardList2.length == 1 && jokerNum == 1) || (repeatCardList1.length == 3 && jokerNum == 2)) {
                if (jokerNum == 0)
                    cardPatternList = this.getPatternIdList(repeatCardList3, cardIdList);
                else if (jokerNum == 1)
                    cardPatternList = this.getPatternIdList(repeatCardList2, cardIdList);
                else if (jokerNum == 2)
                    cardPatternList = this.getPatternIdList(repeatCardList1, cardIdList);

                // console.log(cardPatternList, "=======777777777cardPatternList");
                jokerTurnList = this.getJokerTurnList(jokerNum, this.getCardNumber(cardPatternList[0]), "d");
                return twa.CardPatternFactory.getPattern(twa.CARD_TYPE.TRIPLET, cardPatternList, pierNum, jokerNum, jokerTurnList);
            }

            else if (repeatCardList2.length == 2) {
                cardPatternList = this.getPatternIdList(repeatCardList2, cardIdList);
                //   console.log(cardPatternList, "=======88888888888cardPatternList");
                return twa.CardPatternFactory.getPattern(twa.CARD_TYPE.TWO_PAIR, cardPatternList, pierNum, jokerNum, jokerTurnList);
            }

            else if ((repeatCardList2.length == 1) || (repeatCardList1.length == (cardIdList.length - 1) && jokerNum == 1)) {
                if (jokerNum == 0)
                    cardPatternList = this.getPatternIdList(repeatCardList2, cardIdList);
                else if (jokerNum == 1)
                    cardPatternList = this.getPatternIdList([repeatCardList1[0]], cardIdList);
                //console.log(cardPatternList, "==============cardPatternList");
                jokerTurnList = this.getJokerTurnList(jokerNum, this.getCardNumber(cardPatternList[0]), "d");
                return twa.CardPatternFactory.getPattern(twa.CARD_TYPE.PAIR, cardPatternList, pierNum, jokerNum, jokerTurnList);
            }

            return twa.CardPatternFactory.getPattern(twa.CARD_TYPE.OOLONG, cardPatternList, pierNum, jokerNum, jokerTurnList);
        }

        getSerialData(cardIdList, lists, jokerNum) {
            let data = { list: null, jokerTurnList: null, idList: null };

            let idList = cardIdList.concat();
            let len = lists.length;

            if (len + jokerNum != 5)
                return null;

            let list = [];
            for (let i = 0; i < len; i++) {
                list.push(parseInt(this.getCardNumber(lists[i])));
            }

            let num1 = list[0];
            let num2 = list[len - 1];
            if (num1 > 14)
                return null;

            if (jokerNum == 0) {
                if ((list.toString() == [14, 5, 4, 3, 2].toString()) || (num1 - num2 == len - 1)) {
                    data.list = list;
                    data.jokerTurnList = [];
                    data.idList = idList;
                    return data;
                }
            }
            else {
                let isOverstep = false;
                let reList = [num2];
                let jokerTurnList = [];
                let key = len - 2;
                let oddJokerNum = jokerNum;
                let oldNum = num2;

                let idKey = cardIdList.length - 2;
                idList = [cardIdList[idKey + 1]];
                for (let n = 1; n < 5; n++) {
                    if (key >= 0 && ((list[key] == oldNum + 1) || (list[key] == 14 && oldNum == 5))) {
                        oldNum = list[key];
                        reList.unshift(oldNum);
                        idList.unshift(cardIdList[idKey]);
                        key--;
                        idKey--;
                    }
                    else if (oddJokerNum != 0) {
                        if (n == 4)
                            oldNum = (oldNum == 5 ? 14 : oldNum + 1);
                        else
                            oldNum = oldNum + 1;

                        if (oldNum == 15) {
                            isOverstep = true;

                            oldNum = 10;
                            jokerTurnList.push(oldNum);
                            reList.push(oldNum);
                            idList.push(cardIdList[oddJokerNum - 1]);
                        }
                        else {
                            jokerTurnList.unshift(oldNum);

                            if (isOverstep) {
                                reList.splice(3, 0, oldNum);
                                idList.splice(3, 0, cardIdList[oddJokerNum - 1]);
                            }
                            else {
                                reList.unshift(oldNum);
                                idList.unshift(cardIdList[oddJokerNum - 1]);
                            }
                        }

                        oddJokerNum--;
                    }
                    else {
                        return null;
                    }
                }

                data.list = reList;
                data.jokerTurnList = jokerTurnList;
                data.idList = idList;
                return data;
            }

            return null;
        }

        isSerial(lists) {
            let len = lists.length;
            let list = [];
            for (let i = 0; i < len; i++) {
                list.push(parseInt(this.getCardNumber(lists[i])));
            }

            let num1 = list[0];
            let num2 = list[len - 1];
            if (num1 > 14)
                return false;

            if (list.toString() == [14, 5, 4, 3, 2].toString())
                return true;

            return num1 - num2 == len - 1;
        }

        getSameFlower(lists) {
            let self = this;
            let sameFlower = self.getCardType(lists[lists.length - 1]);
            // console.log(lists.length, "classic--------353");
            lists.forEach(id => {
                if (!this.isJoker(id)) {
                    let flower = self.getCardType(id);
                    if (sameFlower == null || sameFlower != flower)
                        sameFlower = null;
                }
            });
            return sameFlower;
        }

        isSameFlower(lists) {
            let self = this;
            let sameFlower = self.getCardType(lists[0]);
            // console.log(lists.length, "classic--------367");
            lists.forEach(id => {
                let flower = self.getCardType(id);
                if (sameFlower == null || sameFlower != flower)
                    sameFlower = null;
            });

            return (sameFlower != null);
        }

        /*-------------------------------------------鬼牌变化相关---------------------------------------------------*/
        setJokerTurn(pierNum, idList, cardList) {
            if (this.getJokerNum(idList) == 0)
                return;

            let turnListNum = 0;
         //   console.log(idList.sort(this.sortCardFunc), "==========鬼牌的相关变化")
            let cardPattern = this.getCardPattern(idList.sort(this.sortCardFunc), pierNum);
            let jokerTurnList = cardPattern.getJokerTurnList();
            let cardsIdList = cardPattern.getCardIdList();
            for (let n = 0; n < cardsIdList.length; n++) {
                let card = cardList[n];
                if (this.isJoker(card.getCardId())) {
                    let jokerTurnId = jokerTurnList[turnListNum];
                    card.setJokerCardTurnCard(jokerTurnId);

                    turnListNum++;
                }
            }
        }

        setJokerTurnInMV(idList, cardList) {
            let jokerNum = this.getJokerNum(idList);
            if (jokerNum == 0)
                return;

            let card = null;
            let cardListLength = cardList.length;
            let mostIdNum = this.getMostIdNumInIdList(idList);

            if (mostIdNum == null) {
                for (let n = 0; n < cardListLength; n++) {
                    card = cardList[n];
                    if (this.isJoker(card.getCardId()))
                        card.setJokerCardTurnCard("Ad");
                }
            }
            else {
                for (let m = 0; m < cardListLength; m++) {
                    card = cardList[m];
                    if (this.isJoker(card.getCardId()))
                        card.setJokerCardTurnCard(twa.CONSTANTS.valueMap[mostIdNum] + "d");
                }
            }
        }

        getMostIdNumInIdList(idList) {
            let mostIdNum = null;
            let numLast = null;
            let mostNum = 0;
            let tmpNum = 0;
            // console.log(idList.length, "classic--------428");
            idList.forEach(id => {
                if (!this.isJoker(id) && (id != "")) {
                    let numCard = this.getCardNumber(id);
                    if (numCard != numLast || numLast == null) {
                        numLast = numCard;
                        tmpNum = 1;
                    }
                    else {
                        tmpNum++;
                    }

                    if (tmpNum > mostNum) {
                        mostNum = tmpNum;
                        mostIdNum = numCard;
                    }
                }
            });

            return mostIdNum;
        }
        /*-------------------------------------------鬼牌变化相关---------------------------------------------------*/

        /*-------------------------------------------提示相关---------------------------------------------------*/
        getTipsDataList(cardIdList) {
            // console.log(cardIdList, "=========453========cardIdList")
            let tipsData = {};
            if (cardIdList.length == 0)
                return tipsData;

            for (let n = 1; n <= 10; n++) {
                if (n != 4)
                    tipsData[n] = this.getListByType(n, cardIdList);
            }

            return tipsData;
        }

        getListByType(type, cardIdList) {
            if (type < 1 || type > 10 || type == twa.CARD_TYPE.DOUBLE_GHOST) {
                console.log("-------------------error type-----------------------");
                return null;
            }
            //  console.log(cardIdList, "=========471=====cardIdList");
            // console.log(type, "=============type");
            let tipsObj = twa.TipsUtils.getTipsObj(type, cardIdList);
            // console.log(tipsObj, "===============tipsObj");
            let list = tipsObj.getTipsList();
            // console.log(list, "========gggggggggg====list");
            //console.log("-------------------tips list-----------------------");
            //cc.each(list, function(cardIdList){
            //    console.log("usable:" + cardIdList.join(","));
            //});

            return list;
        }
        /*-------------------------------------------提示相关 end---------------------------------------------------*/

        /*-------------------------------------------自动出牌---------------------------------------------------*/
        getAutoArrangedCardsData(cardIdList, tipsData) {
            let data = twa.AutoArrangedCards.getAutoArrangedCardsData(cardIdList, tipsData);

            //let typeKeyList = data.typeKeyList;
            //cc.each(typeKeyList, function(typeKey)
            //{
            //    console.log("typeKey = " + typeKey);
            //    console.log("arrangedCards1 = " + data.arrangedCardsData[typeKey][0].getCardIdList().toString());
            //    console.log("arrangedCards2 = " + data.arrangedCardsData[typeKey][1].getCardIdList().toString());
            //    console.log("arrangedCards3 = " + data.arrangedCardsData[typeKey][2].getCardIdList().toString());
            //    console.log("");
            //});

            return data;
        }
        /*-------------------------------------------自动出牌 end---------------------------------------------------*/
    }
    export namespace twa {
        export let unitTest = function (list) {
            console.log("twa unit test!");
            list.forEach(strCardIdList => {
                let cardIdList = twa.utils.getCardIdList(strCardIdList);
                let card = this.getCardPattern(cardIdList);
                console.log(card.getCardIdList().join(","), card.toString());
            });
        };

        export let testTipList = function (list, target) {
            let targetIdList = twa.utils.getCardIdList(target);
          
            let targetPattern = twa.utils.getCardPattern.bind(this, targetIdList);
            console.log("--------------------------------------------------");
            console.log("target:" + targetPattern.getCardIdList().join(","), targetPattern.toString());
            list.forEach(strCardIdList => {
                let cardIdList = twa.utils.getCardIdList(strCardIdList);
                console.log("-----------------------usable list---------------------------");
                console.log("target:" + cardIdList.join(","));
              
                let cardPattern = twa.utils.getCardPattern.bind(this, targetIdList);
            });
        }
    }
}