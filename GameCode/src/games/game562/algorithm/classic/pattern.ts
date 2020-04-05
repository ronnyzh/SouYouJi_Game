module G562 {
    export namespace twa {
        export let utils: G562classic;

        export let CARD_TYPE = {
            //.........普通牌型..........
            //乌龙
            OOLONG: 0,
            //对子
            PAIR: 1,
            //两对
            TWO_PAIR: 2,
            //三条
            TRIPLET: 3,
            //双鬼冲头
            DOUBLE_GHOST: 4,
            //顺子
            STRAIGHT: 5,
            //同花
            FLUSH: 6,
            //葫芦
            GOURD: 7,
            //铁支
            IRON_BRANCH: 8,
            //同花顺
            STRAIGHT_FLUSH: 9,
            //五同
            FIVE_HEADS: 10,

            //..........特殊牌型..........
            //三同花
            THREE_FLUSH: 11,
            //三顺子
            THREE_STRAIGHT: 12,
            //六对半
            SIX_PAIRS: 13,
            //五对三条
            FIVE_PAIRS_A_TRIPLET: 14,
            //四套三条
            FOUR_TRIPLET: 15,
            //凑一色
            ONE_COLOR: 16,
            //全小
            ALL_SMALL: 17,
            //全大
            ALL_BIG: 18,
            //六同
            SIX_HEADS: 19,
            //三分天下
            THREE_POINTS: 20,
            //三同花顺
            THREE_STRAIGHT_FLUSH: 21,
            //十二皇族
            TWELVE_ROYALTY: 22,
            //七同
            SEVEN_HEADS: 23,
            //一条龙
            DRAGON: 24,
            //至尊青龙
            SUPREME_QINGLONG: 25
        }

        export let PATTERN_NAME_MAP = {}

        {
            for (let key in twa.CARD_TYPE) {
                twa.PATTERN_NAME_MAP[twa.CARD_TYPE[key]] = key;
            }
        }

        export let CONSTANTS = {
            RED_JOKER_ID: "Bj",
            BLACK_JOKER_ID: "Lj",
            cardNumMap: {},
            valueMap: {}
        }

        {
            let map = twa.CONSTANTS.cardNumMap;
            for (let i = 2; i < 10; ++i) {
                map[i.toString()] = i;
            }
            map["T"] = 10;
            map["J"] = 11;
            map["Q"] = 12;
            map["K"] = 13;
            map["A"] = 14;
            map["L"] = 16;
            map["B"] = 17;
            for (let key in map) {
                twa.CONSTANTS.valueMap[map[key]] = key;
            }
        }

        export let UI_CARD = {}
        export let initUICard = () => {
            UI_CARD = {
                card_Aa: fairygui.UIPackage.getItemURL("pokers", "card_d1"),
                card_2a: fairygui.UIPackage.getItemURL("pokers", "card_d2"),
                card_3a: fairygui.UIPackage.getItemURL("pokers", "card_d3"),
                card_4a: fairygui.UIPackage.getItemURL("pokers", "card_d4"),
                card_5a: fairygui.UIPackage.getItemURL("pokers", "card_d5"),
                card_6a: fairygui.UIPackage.getItemURL("pokers", "card_d6"),
                card_7a: fairygui.UIPackage.getItemURL("pokers", "card_d7"),
                card_8a: fairygui.UIPackage.getItemURL("pokers", "card_d8"),
                card_9a: fairygui.UIPackage.getItemURL("pokers", "card_d9"),
                card_Ta: fairygui.UIPackage.getItemURL("pokers", "card_d10"),
                card_Ja: fairygui.UIPackage.getItemURL("pokers", "card_d11"),
                card_Qa: fairygui.UIPackage.getItemURL("pokers", "card_d12"),
                card_Ka: fairygui.UIPackage.getItemURL("pokers", "card_d13"),

                card_Ab: fairygui.UIPackage.getItemURL("pokers", "card_c1"),
                card_2b: fairygui.UIPackage.getItemURL("pokers", "card_c2"),
                card_3b: fairygui.UIPackage.getItemURL("pokers", "card_c3"),
                card_4b: fairygui.UIPackage.getItemURL("pokers", "card_c4"),
                card_5b: fairygui.UIPackage.getItemURL("pokers", "card_c5"),
                card_6b: fairygui.UIPackage.getItemURL("pokers", "card_c6"),
                card_7b: fairygui.UIPackage.getItemURL("pokers", "card_c7"),
                card_8b: fairygui.UIPackage.getItemURL("pokers", "card_c8"),
                card_9b: fairygui.UIPackage.getItemURL("pokers", "card_c9"),
                card_Tb: fairygui.UIPackage.getItemURL("pokers", "card_c10"),
                card_Jb: fairygui.UIPackage.getItemURL("pokers", "card_c11"),
                card_Qb: fairygui.UIPackage.getItemURL("pokers", "card_c12"),
                card_Kb: fairygui.UIPackage.getItemURL("pokers", "card_c13"),

                card_Ac: fairygui.UIPackage.getItemURL("pokers", "card_b1"),
                card_2c: fairygui.UIPackage.getItemURL("pokers", "card_b2"),
                card_3c: fairygui.UIPackage.getItemURL("pokers", "card_b3"),
                card_4c: fairygui.UIPackage.getItemURL("pokers", "card_b4"),
                card_5c: fairygui.UIPackage.getItemURL("pokers", "card_b5"),
                card_6c: fairygui.UIPackage.getItemURL("pokers", "card_b6"),
                card_7c: fairygui.UIPackage.getItemURL("pokers", "card_b7"),
                card_8c: fairygui.UIPackage.getItemURL("pokers", "card_b8"),
                card_9c: fairygui.UIPackage.getItemURL("pokers", "card_b9"),
                card_Tc: fairygui.UIPackage.getItemURL("pokers", "card_b10"),
                card_Jc: fairygui.UIPackage.getItemURL("pokers", "card_b11"),
                card_Qc: fairygui.UIPackage.getItemURL("pokers", "card_b12"),
                card_Kc: fairygui.UIPackage.getItemURL("pokers", "card_b13"),

                card_Ad: fairygui.UIPackage.getItemURL('pokers', 'card_a1'),
                card_2d: fairygui.UIPackage.getItemURL("pokers", "card_a2"),
                card_3d: fairygui.UIPackage.getItemURL("pokers", "card_a3"),
                card_4d: fairygui.UIPackage.getItemURL("pokers", "card_a4"),
                card_5d: fairygui.UIPackage.getItemURL("pokers", "card_a5"),
                card_6d: fairygui.UIPackage.getItemURL("pokers", "card_a6"),
                card_7d: fairygui.UIPackage.getItemURL("pokers", "card_a7"),
                card_8d: fairygui.UIPackage.getItemURL("pokers", "card_a8"),
                card_9d: fairygui.UIPackage.getItemURL("pokers", "card_a9"),
                card_Td: fairygui.UIPackage.getItemURL("pokers", "card_a10"),
                card_Jd: fairygui.UIPackage.getItemURL("pokers", "card_a11"),
                card_Qd: fairygui.UIPackage.getItemURL("pokers", "card_a12"),
                card_Kd: fairygui.UIPackage.getItemURL("pokers", "card_a13"),

                card_Bj: fairygui.UIPackage.getItemURL("pokers", "card_e1"),
                card_Lj: fairygui.UIPackage.getItemURL("pokers", "card_e2"),

                card_back: fairygui.UIPackage.getItemURL("pokers", "card_backface")
            }
        }
       // console.log(UI_CARD, '---------------------UI_CARD-----------------------------');
        export class BaseCard {
            type;
            pierNum;
            jokerData;
            cardIdList;
            keyValue;
            wcValueList;
            constructor(type, data, keyValue?) {
                this.type = type;
                this.setData(data, keyValue);
                this.pierNum = 0;     //表明是第几墩

                this.jokerData = {};
            }

            setJokerData(jokerNum, jokerTurnList) {
                this.jokerData = {
                    jokerNum: jokerNum,
                    jokerTurnList: jokerTurnList
                };

                //如果有鬼牌，给cardIdList重新排序
                if (jokerNum != 0 && (this.type != twa.CARD_TYPE.STRAIGHT_FLUSH && this.type != twa.CARD_TYPE.STRAIGHT)) {
                    this.sortJokerCardIdList();
                }
            }

            sortJokerCardIdList() {
                let jokerList = [];
                let cardIdList = this.cardIdList.concat();
                //console.log(cardIdList.length, "pattern--------184");
                cardIdList.forEach(cardId => {
                    if (this.isJoker(cardId)) {
                        jokerList.push(cardId);
                        cardIdList.splice(cardIdList.indexOf(cardId), 1);
                    }
                });

                this.cardIdList = jokerList.concat(cardIdList);
            }

            getJokerNum() {
                return this.jokerData.jokerNum;
            }

            getJokerTurnList() {
                return this.jokerData.jokerTurnList;
            }

            setPierNum(num) {
                this.pierNum = num;
            }

            getPierNum() {
                return this.pierNum;
            }

            isJoker(cardId) {
                return cardId == twa.CONSTANTS.RED_JOKER_ID || cardId == twa.CONSTANTS.BLACK_JOKER_ID;
            }
            getCardNumber(cardId) {
                let num = cardId[0];
                return twa.CONSTANTS.cardNumMap[num];
            }

            greaterThan(card) {
                if (this.getType() != card.getType())
                    return card.getType() < this.getType();

                let cardList1 = this.getCardIdList();
                let cardList2 = card.getCardIdList();
                for (let i = 0; i < cardList1.length; i++) {
                    let value1 = cardList1[i];
                    let value2 = cardList2[i];

                    if ((value2 == null) || (this.getCardNumber(value1) == this.getCardNumber(value2)))
                        continue;

                    //鬼牌不用比较
                    if (this.isJoker(value1) || this.isJoker(value2))
                        continue;

                    return this.getCardNumber(value1) > this.getCardNumber(value2);
                }

                return false;
            }

            getKeyValue() {
                return this.keyValue || this.cardIdList[0];
            }

            setData(cardIdList, keyValue) {
                this.cardIdList = cardIdList;
                this.keyValue = keyValue;
            }

            getType() {
                return this.type;
            }

            getCardIdList() {
                return this.cardIdList.concat();
            }

            getShowCardIdList() {
                return this.cardIdList.concat();
            }

            toString() {
                let str = this.getShowCardIdList().join(",") + ", type:" + twa.PATTERN_NAME_MAP[this.getType()] + ", key value:" + this.getKeyValue();
                if (this.wcValueList != null)
                    str += ", wildcard value:" + this.wcValueList.join(",");
                return str;
            }

            getActionData() {
                return [this.cardIdList.join(",")];
            }

            isWildcardPattern() {

            }
        }

        export class Flush extends BaseCard {
            setJokerData(jokerNum, jokerTurnList) {
                super.setJokerData(jokerNum, jokerTurnList);
                if (jokerNum > 0) {
                    let typeData = this.getCardNumTypeData();
                    let turnId = null;
                    for (let i = 0; i < 5; i++) {
                        let value = typeData["keyList"][i];

                        //鬼牌不用比较
                        if (!this.isJoker(value)) {
                            turnId = value;
                            break;
                        }
                    }

                    if (turnId != null) {
                        let newJokerTurnList = [];
                        for (let j = 0; j < jokerNum; j++) {
                            newJokerTurnList.push(turnId)
                        }

                        this.jokerData["jokerTurnList"] = newJokerTurnList;
                    }
                }
            }

            analyse(list) {
                //预处理牌数组数据
                let repeatCardLists = [[], [], [], []];
                let numLast = this.getCardNumber(list[0]);
                let tmpList = [];
                for (let i = 0; i < list.length; ++i) {
                    let id = list[i];
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
                if (tmpList.length == 1)
                    repeatCardLists[0].push(tmpList[0]);
                else if (tmpList.length > 1)
                    repeatCardLists[tmpList.length - 1].push(tmpList);

                return repeatCardLists;
            }

            greaterThan(card) {
                if (this.getType() != card.getType())
                    return card.getType() < this.getType();

                //用于分辨同花里面三条，两对，对子
                let typeData1 = this.getCardNumTypeData();
                let typeData2 = card.getCardNumTypeData();

                if (typeData1["type"] != typeData2["type"])
                    return typeData1["type"] > typeData2["type"];

                for (let i = 0; i < 5; i++) {
                    let value1 = typeData1["keyList"][i];
                    let value2 = typeData2["keyList"][i];

                    if (this.getCardNumber(value1) == this.getCardNumber(value2))
                        continue;

                    //鬼牌不用比较
                    if (this.isJoker(value1) || this.isJoker(value2))
                        continue;

                    return this.getCardNumber(value1) > this.getCardNumber(value2);
                }

                return false;
            }
            getCardNumTypeData() {
                let cardList = this.getCardIdList();
                let repeatCardLists = this.analyse(cardList);
                let jokerNum = this.getJokerNum();

                let type = 0;
                let keyList = cardList;
                if ((jokerNum == 0 && repeatCardLists[2].length == 1)
                    || (jokerNum == 1 && repeatCardLists[1].length == 1)
                    || (jokerNum == 2)) {
                    type = 3;
                }
                else if (jokerNum == 0 && repeatCardLists[1].length == 2) {
                    type = 2;
                }
                else if ((jokerNum == 0 && repeatCardLists[1].length == 1)
                    || (jokerNum == 1)) {
                    type = 1;
                }

                if (repeatCardLists[2].length == 1) {
                    keyList = repeatCardLists[2][0].concat(repeatCardLists[0])
                }
                else if (repeatCardLists[1].length == 2) {
                    keyList = repeatCardLists[1][0].concat(repeatCardLists[1][1]).concat(repeatCardLists[0])
                }
                else if (repeatCardLists[1].length == 1) {
                    keyList = repeatCardLists[1][0].concat(repeatCardLists[0])
                }

                let data =
                    {
                        "type": type,
                        "keyList": keyList
                    };
                return data;
            }
        }

        export class CardPatternFactory {
            static getPattern(type, cardIdList, pierNum, jokerNum, jokerTurnList) {
                let pattern = null;
                switch (type) {
                    case -1:
                        break;

                    case 6:
                        pattern = new twa.Flush(type, cardIdList);
                        break;

                    default:
                        pattern = new twa.BaseCard(type, cardIdList);
                        break;
                }

                pattern.setPierNum(pierNum);
                pattern.setJokerData(jokerNum, jokerTurnList);
                return pattern;
            }
        }
    }
}