module G562 {
    export namespace cgb {
        export let CONSTANTS = {
            CARD_STATE_SHOW: 0,
            CARD_STATE_COVER: 1,

            BLACK_JOKER_ID: "Lj",
            RED_JOKER_ID: "Bj"
        };
        export let config = {
            playerCount: 7,
            countdown: 60,
            isJokerPlay: null,
            isHorsePlay: null,
            isShotAddOne: null,
            isDealerPlay: null,
            horseCardId: null     //马牌
        };
        export let CARD_TYPES = {
            0: "乌龙",
            1: "对子",
            2: "两对",
            3: "三条",
            4: "双鬼冲头",
            5: "顺子",
            6: "同花",
            7: "葫芦",
            8: "铁支",
            9: "同花顺",
            10: "五同",
            //特殊牌型
            11: "三同花",
            12: "三顺子",
            13: "六对半",
            14: "五对三条",
            15: "四套三条",
            16: "凑一色",
            17: "全小",
            18: "全大",
            19: "六同",
            20: "三分天下",
            21: "三同花顺",
            22: "十二皇族",
            23: "七同",
            24: "一条龙",
            25: "至尊青龙"
        };
        export let CARD_WIDTH = 166;
        export let OUT_LIST_SCALE = 0.4;
        export let OUT_LIST_STRIDE = 32;
        // cgb.OUT_LIST_STRIDE0 = 75;
        export let OUT_LIST_STRIDE_H = 100;
        export let OUT_LIST_LIMIT_COUNT = 10;
    }
}