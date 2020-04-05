


module G560{

    //client2server
    export let C_S_READY_GAME = 0x00002004;


    //export let C_S_TOTAL_BALANCE_DATA = 0x00002007;
    export let C_S_DOUBLE = 0x00002008;
    export let C_S_PREACTIONEDDATA = 0x00002009;
    export let C_S_TRUSTEE = 0x00002010;
    export let C_S_DO_ACTION2 = 0x000020011;


    export let C_S_ROBLANDLORD = 0x000020012;


    //server2client


    // export let S_C_GET_RESULT = 0x000030003;      // 结果返回
    // export let S_C_TOTAL_REPORT = 0x000030004;    // 大局结算


    export let S_C_READY_GAME = 0x00003000d;
    export let S_C_READY_GAME_DATA = 0x00003000e;

    export let S_C_DEAL_CARDS = 0x000030010;
    export let S_C_TURN_ACTION = 0x000030011;
    export let S_C_DO_ACTION_RESULT = 0x000030012;
    export let S_C_ADDL_GAME_INFO = 0x000030013;


    export let S_C_DOUBLE = 0x000030015;
    export let S_C_DOUBLE_RESULT = 0x000030016;
    export let S_C_PREACTIONEDDATA = 0x000030017;
    export let S_C_TRUSTEE = 0x000030018;

    export let S_C_ROBLANDLORD = 0x000030019;
    export let S_C_ROBLANDLORDRESULT = 0x000030020;
    export let S_C_SCOREDATA = 0x000030021;

    export let S_C_WAIT_TIME = 0x000030090;
    // export let S_C_SWAP_DEALER = 0x000030091;//换位
    export let S_C_TOTAL_BALANCE_DATA = 0x000030092; // 总战绩
    export let S_C_MESSAGE = 0x000030093; // 消息
    export let S_C_ADDL_REPORT_CUR_GAME = 0x000030094;  //赣州单局结算报表需要的数据
    export let S_C_OLD_ADDL_REPORT_CUR_GAME = 0x000030095;  //赣州上一局单局结算报表需要的数据
    
    export class GNetHandler extends PartyNetHandler{

        getGameProtoDataList()
        {
            var classesMapList = [
                [G560.C_S_READY_GAME, "C_S_ReadyGame"],


                [G560.C_S_DOUBLE, "C_S_Double"],
                [G560.C_S_PREACTIONEDDATA, "C_S_PreActionedData"],
                [G560.C_S_TRUSTEE, "C_S_Trustee"],
                [G560.C_S_DO_ACTION2, "C_S_DoAction2"],
                [G560.C_S_ROBLANDLORD, "C_S_RobLandlord"],
                

                // [G560.S_C_GET_RESULT, "C_S_OnGa"],
                // [G560.S_C_TOTAL_REPORT, "C_S_OnGa"],
                [G560.S_C_READY_GAME, "S_C_ReadyGame"],
                [G560.S_C_READY_GAME_DATA, "S_C_ReadyGameData"],
                [G560.S_C_DEAL_CARDS, "S_C_DealCards"],
                [G560.S_C_TURN_ACTION, "S_C_TurnAction"],
                [G560.S_C_DO_ACTION_RESULT, "S_C_DoActionResult"],
                [G560.S_C_ADDL_GAME_INFO, "S_C_AddlGameInfo"],

                [G560.S_C_DOUBLE, "S_C_Double"],
                [G560.S_C_DOUBLE_RESULT, "S_C_DoubleResult"],
                [G560.S_C_PREACTIONEDDATA, "S_C_PreActionedData"],
                [G560.S_C_TRUSTEE, "S_C_Trustee"],

                [G560.S_C_ROBLANDLORD, "S_C_RobLandlord"],
                [G560.S_C_ROBLANDLORDRESULT, "S_C_RobLandlordResult"],
                [G560.S_C_SCOREDATA, "S_C_ScoreData"],

                [G560.S_C_WAIT_TIME, "S_C_WaitTime"],
                // [G560.S_C_SWAP_DEALER, "C_S_OnGa"],
                [G560.S_C_TOTAL_BALANCE_DATA, "S_C_TotalBalanceData"],
                [G560.S_C_MESSAGE, "S_C_Message"],
                [G560.S_C_ADDL_REPORT_CUR_GAME, "S_C_AddlReportCurGame"],
                [G560.S_C_OLD_ADDL_REPORT_CUR_GAME, "S_C_OldAddlReportCurGame"],

            ];

            var path=ResourceMgr.GetGameProtoPath(560);
            var protoDataList = [
                { pkgName:"private_mahjong", path:path+'private_mahjong.proto' , classesMapList : classesMapList}
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

        sendRob(type, operate)
        {
            //0:叫地主，1:叫分，2:抢地主
            // required CALL_TYPE choseType = 1;

            //如果是叫地主，0是不叫，1是叫
            //如果是叫分，0是不叫，1是叫1分，2是叫2分，3是叫3分
            //如果是抢地主，0是不抢，1是抢

            // required fixed32 operate = 2;
            var obj = {};
            obj["choseType"] = type;
            obj["operate"] = operate;
            this.sendData(C_S_ROBLANDLORD, obj);
        }
        


    }
}
