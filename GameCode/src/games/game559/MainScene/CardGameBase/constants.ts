/**
 * Created by Administrator on 2018/4/17.
 */
module G559{
    export namespace cgb{
        export let CONSTANTS = {
            CARD_STATE_SHOW : 0,
            CARD_STATE_COVER : 1,

            BLACK_JOKER_ID : "Lj",
            RED_JOKER_ID : "Bj",
        };

        export let LOCAL_POS_LIST = {
            2 : [0, 1],
            3 : [0, 1, 2]
        };

        interface i_config{
            showHandCardsCount: any;
            playerCount: any;
            countdown: any;
            firstThree: any;
            canNoDiscard: any;
        }
        export let config = <i_config>{
            playerCount : 3,
            countdown : 15,
            firstThree : false,      //是否先出三
            canNoDiscard : false     //是否可以不要
        };

        export let CARD_WIDTH = 166;
        export let OUT_LIST_SCALE = 0.65;
        export let OUT_LIST_STRIDE = 75;
// export let OUT_LIST_STRIDE0 = 75;

        export let OUT_LIST_STRIDE_H = 100;
        export let OUT_LIST_LIMIT_COUNT = 10;

        export let CARD_COUNT = 16;
    }
}