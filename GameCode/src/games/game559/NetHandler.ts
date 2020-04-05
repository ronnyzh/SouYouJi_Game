


module G559{

    //server2client
    export let C_S_ON_GA = 0x00002001; //下注
    export let C_S_GET_RESULT = 0x00002002;  // 客户端获取结果
    export let C_S_ON_STRIVE = 0x00002003; // 抢庄
    export let C_S_READY_GAME = 0x00002004;
    export let C_S_HAS_BULL_OR_NOT = 0x00002005;
    export let C_S_TOTAL_BALANCE_DATA = 0x00002007;
    export let C_S_DO_ACTION2 = 0x000030014;

    export let C_S_DOUBLE = 0x00002008;
    export let C_S_PREACTIONEDDATA = 0x00002009;
    export let C_S_TRUSTEE = 0x00002010;


//server2client
    export let S_C_GA_DATA = 0x00003001;          // 下注返回数据
    export let S_C_GA_CHOOSE  =  0x000030002;     //
    export let S_C_GET_RESULT = 0x000030003;      // 结果返回
    export let S_C_TOTAL_REPORT = 0x000030004;    // 大局结算
// export let S_C_DEAL_CARDS = 0x000030005; // 手牌
    export let S_C_GET_ONE_RESULT = 0x000030006; // 单个玩家返回
    export let S_C_RESULT_INFO = 0x000030007; // 输赢结果
    export let S_C_FLY = 0x000030008;
    export let S_C_STRIVE_FOR_DEALER = 0x000030009; // 抢庄
    export let S_C_STRIVE_FOR_DEALER_TIMEOUT = 0x00003000a; // 抢庄等待时间
    export let S_C_STRIVE_CHOOSE = 0x00003000b; // 抢庄确认帧
    export let S_C_STRIVE_RESULT = 0x00003000c; // 抢庄结果
    export let S_C_READY_GAME = 0x00003000d;
    export let S_C_READY_GAME_DATA = 0x00003000e;
    export let S_C_HAS_BULL_OR_NOT = 0x00003000f;
    export let S_C_DEAL_CARDS = 0x000030010;  // 手牌 - 重写
    export let S_C_TURN_ACTION = 0x000030011;
    export let S_C_DO_ACTION_RESULT = 0x000030012;
    export let S_C_ADDL_GAME_INFO = 0x000030013; // 刷新的补充数据

    export let S_C_DOUBLE = 0x000030015;
    export let S_C_DOUBLE_RESULT = 0x000030016;
    export let S_C_PREACTIONEDDATA = 0x000030017;
    export let S_C_TRUSTEE = 0x000030018;

    export let S_C_WAIT_TIME = 0x000030090;
    export let S_C_SWAP_DEALER = 0x000030091;//换位
    export let S_C_TOTAL_BALANCE_DATA = 0x000030092; // 总战绩
    export let S_C_MESSAGE = 0x000030093; // 消息
    export let S_C_ADDL_REPORT_CUR_GAME = 0x000030094;  //赣州单局结算报表需要的数据
    export let S_C_OLD_ADDL_REPORT_CUR_GAME = 0x000030095;  //赣州上一局单局结算报表需要的数据
    
    export class GNetHandler extends PartyNetHandler{

        getGameProtoDataList()
        {
            var classesMapList = [
                [G559.C_S_ON_GA, "C_S_OnGa"],
                [G559.C_S_GET_RESULT, "C_S_GetResult"],
                [G559.C_S_ON_STRIVE, "C_S_OnStrive"],
                [G559.C_S_READY_GAME, "C_S_ReadyGame"],
                [G559.C_S_HAS_BULL_OR_NOT, "C_S_HasBullOrNot"],
                [G559.C_S_TOTAL_BALANCE_DATA, "C_S_TotalBalanceData"],
                [G559.C_S_DO_ACTION2, "C_S_DoAction2"],
                [G559.C_S_DOUBLE, "C_S_Double"],
                [G559.C_S_PREACTIONEDDATA, "C_S_PreActionedData"],
                [G559.C_S_TRUSTEE, "C_S_Trustee"],

                [G559.S_C_GA_DATA, "S_C_GaData"],
                [G559.S_C_GA_CHOOSE, "S_C_Ga_Choose"],
                [G559.S_C_GET_RESULT, "S_C_GetResult"],
                [G559.S_C_TOTAL_REPORT, "S_C_TotalReport"],
                [G559.S_C_GET_ONE_RESULT, "S_C_GetOneResult"],
                [G559.S_C_RESULT_INFO, "S_C_ResultInfo"],
                [G559.S_C_FLY, "S_C_Fly"],
                [G559.S_C_STRIVE_FOR_DEALER, "S_C_StriveForDealer"],
                [G559.S_C_STRIVE_FOR_DEALER_TIMEOUT, "S_C_StriveForDealerTimeout"],
                [G559.S_C_STRIVE_CHOOSE, "S_C_Strive_Choose"],
                [G559.S_C_STRIVE_RESULT, "S_C_Strive_Result"],
                [G559.S_C_READY_GAME, "S_C_ReadyGame"],
                [G559.S_C_READY_GAME_DATA, "S_C_ReadyGameData"],
                [G559.S_C_HAS_BULL_OR_NOT, "S_C_HasBullOrNot"],

                [G559.S_C_DEAL_CARDS, "S_C_DealCards"],
                [G559.S_C_TURN_ACTION, "S_C_TurnAction"],
                [G559.S_C_DO_ACTION_RESULT, "S_C_DoActionResult"],
                [G559.S_C_ADDL_GAME_INFO, "S_C_AddlGameInfo"],

                [G559.S_C_DOUBLE, "S_C_Double"],
                [G559.S_C_DOUBLE_RESULT, "S_C_DoubleResult"],
                [G559.S_C_PREACTIONEDDATA, "S_C_PreActionedData"],
                [G559.S_C_TRUSTEE, "S_C_Trustee"],

                [G559.S_C_WAIT_TIME, "S_C_WaitTime"],
                [G559.S_C_SWAP_DEALER, "S_C_SwapDealer"],
                [G559.S_C_ADDL_REPORT_CUR_GAME, "S_C_AddlReportCurGame"],
                [G559.S_C_OLD_ADDL_REPORT_CUR_GAME, "S_C_OldAddlReportCurGame"],

                [G559.S_C_TOTAL_BALANCE_DATA, "S_C_TotalBalanceData"],
                [G559.S_C_MESSAGE, "S_C_Message"],
            ];

            var path=ResourceMgr.GetGameProtoPath(559);
            var protoDataList = [
                { pkgName:"hainan_mahjong", path:path+'private_mahjong.proto' , classesMapList : classesMapList}
            ];

            return protoDataList;
        }

        sendTrustee(isOpen){
            let obj = {
                isTruster : isOpen
            };
            this.sendData(C_S_TRUSTEE, obj);
        }

        sendReadyGame()
        {
            this.sendData(C_S_READY_GAME);
        }

        sendDouble(choice)
        {
            var obj = {
                choice : choice,
            };
            this.sendData(C_S_DOUBLE, obj);
        }

        sendAction(type, datas, num)
        {
            var obj = {
                "action" : type,
                "tiles" : datas,
                "num" : num
            };
            //console.log("-C_S_DO_ACTION-",obj);
            this.sendData(C_S_DO_ACTION2, obj);
        }

    }
}
