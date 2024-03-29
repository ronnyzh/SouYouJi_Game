module G559{
    export namespace rfa {
        export let CARD_TYPE = {
            INVALID: 0,
            //单牌
            SINGLE_CARD: 1,
            //对子
            PAIR: 2,
            //三条
            TRIPLET: 3,
            //三带一
            TRIPLET_WITH_ONE: 4,
            //三带二
            TRIPLET_WITH_TWO: 5,
            //单顺子
            SEQUENCE: 6,
            //双顺子
            SEQUENCE_OF_PAIRS: 7,
            //三顺子（飞机不带翅膀）
            SEQUENCE_OF_TRIPLETS: 8,
            //飞机带翅膀（单牌）
            SEQUENCE_OF_TRIPLETS_WITH_ONE: 9,
            //飞机带翅膀（对子）
            SEQUENCE_OF_TRIPLETS_WITH_TWO: 10,
            //炸弹
            BOMB: 11,
            //火箭（大王小王）
            ROCKET: 12,
            //四带二（单牌）
            QUADPLEX_SET_WITH_ONE: 13,
            //四带二（双牌）
            QUADPLEX_SET_WITH_TWO: 14,
        };

        export let QUADPLEX_COVERT_TO_TRIPLET_WITH_ONE = true; //允许四带一看做三带二

        export let PATTERN_NAME_MAP = {};
        jx.each(CARD_TYPE, function (v, k) {
            PATTERN_NAME_MAP[v] = k;
        });

        interface i_CONSTANTS {
            RED_JOKER_ID:any;
            BLACK_JOKER_ID:any;
            BLACK_THREE:any;
            SEQUENCE_THREE:any;
            cardNumMap:any;
            valueMap:any;
        }
        export let CONSTANTS = <i_CONSTANTS>{
            RED_JOKER_ID: "Bj",
            BLACK_JOKER_ID: "Lj",
            BLACK_THREE: "3d",       //黑桃3
            SEQUENCE_THREE: "3a",     //方块3
        };

        CONSTANTS.cardNumMap = {};
        CONSTANTS.valueMap = {};

        (function () {
            var map = rfa.CONSTANTS.cardNumMap;
            for (var i = 3; i < 10; ++i) {
                map[i.toString()] = i;
            }
            map["T"] = 10;
            map["J"] = 11;
            map["Q"] = 12;
            map["K"] = 13;
            map["A"] = 14;
            map["2"] = 15;
            map["L"] = 16;
            map["B"] = 17;

            jx.each(map, function (v, k) {
                rfa.CONSTANTS.valueMap[v] = k;
            });
        })();


        export class BaseCard {
            public type;
            public sequenceNum;
            public keyValue;
            public cardIdList;
            public wcValueList;
            public isWCP;

            constructor(type, data, keyValue?) {
                this.type = type;
                this.setData(data, keyValue);
                this.sequenceNum = 0;     //表明是几连顺
            }

            setSequenceNum(num) {
                this.sequenceNum = num;
            }

            getSequenceNum() {
                return this.sequenceNum;
            }

            greaterThan(card) {
                if (this.getType() != card.getType())
                    return false;

                if (this.getCardIdList().length != card.getCardIdList().length)
                    return false;

                return rfa.utils.greaterThan(card.getKeyValue(), this.getKeyValue());
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
                var str = this.getShowCardIdList().join(",") + ", type:" + rfa.PATTERN_NAME_MAP[this.getType()] + ", key value:" + this.getKeyValue();
                if (this.wcValueList != null)
                    str += ", wildcard value:" + this.wcValueList.join(",");
                return str;
            }

            getActionData() {
                return [this.cardIdList.join(",")];
            }

            isWildcardPattern() {
                if (this.isWCP != null)
                    return this.isWCP;

                this.isWCP = false;
                var showIdList = this.getShowCardIdList();
                for (var i = 0; i < showIdList.length; ++i) {
                    var cardId = showIdList[i];
                    if (cardId[1] == "w" && !rfaw.utils.isWildcard(cardId)) {
                        this.isWCP = true;
                        break;
                    }
                }
                return this.isWCP;
            }
        }

        export class Bomb extends rfa.BaseCard{
            constructor(cardIdList){
                super(rfa.CARD_TYPE.BOMB, cardIdList);

            }

            greaterThan(card)
            {
                if(card.getType() == rfa.CARD_TYPE.ROCKET)
                    return false;
                else if(card.getType() != rfa.CARD_TYPE.BOMB)
                    return true;

                return super.greaterThan(card);
            }
        }

        export class Rocket extends rfa.BaseCard{
            constructor(){
                super(rfa.CARD_TYPE.ROCKET, [rfa.CONSTANTS.BLACK_JOKER_ID, rfa.CONSTANTS.RED_JOKER_ID]);

            }

            greaterThan()
            {
                return true;
            }
        }

        export let CardPatternFactory = {
            getPattern:function(type, cardIdList, sequenceNum)
            {
                var pattern = null;
                switch(type)
                {
                    case rfa.CARD_TYPE.ROCKET:
                        pattern = new rfa.Rocket();
                        break;

                    case rfa.CARD_TYPE.BOMB:
                        pattern = new rfa.Bomb(cardIdList);
                        break;

                    default:
                        pattern = new rfa.BaseCard(type, cardIdList);
                        break;
                }

                (<rfa.BaseCard>pattern).setSequenceNum(sequenceNum);
                return pattern;
            }
        };
    }

}