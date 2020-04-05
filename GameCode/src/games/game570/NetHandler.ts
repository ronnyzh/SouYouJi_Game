module G570 {
    export let C_S_RANG_PAI = 0x000020013;
    export let C_S_WAGER = 0x000020014;

    // export let S_C_GET_RESULT = 0x000030003;      // 结果返回
    //  export let S_C_TOTAL_REPORT = 0x000030004;    // 大局结算
    export let S_C_RANG_PAI = 0x000030022;
    export let S_C_RANG_PAI_RESULT = 0x000030023;
    export let S_C_WAGER = 0x000030024;
    export let S_C_WAGER_RESULT = 0x000030025;

    export class GNetHandler extends G560.GNetHandler {
        getGameProtoDataList() {
            var classesMapList = [
                [G570.C_S_RANG_PAI, 'C_S_RangPai'],
                [G570.C_S_WAGER, 'C_S_Wager'],

                [G570.S_C_RANG_PAI, 'S_C_RangPai'],
                [G570.S_C_RANG_PAI_RESULT, 'S_C_RangPaiResult'],
                [G570.S_C_WAGER, 'S_C_Wager'],
                [G570.S_C_WAGER_RESULT, 'S_C_WagerResult'],
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
            var path = ResourceMgr.GetGameProtoPath(570);
            var protoDataList = [
                { pkgName: "private_mahjong", path: path + 'private_mahjong.proto', classesMapList: classesMapList }
            ];
            return protoDataList
        }
        sendRANGPAI(PaiCnt) {
            let obj = {
                rangPaiCnt: PaiCnt,
            };
            this.sendData(C_S_RANG_PAI, obj);
        }
        sendWager(wager)  {
            let obj = {
                wager: wager,
            }
            this.sendData(C_S_WAGER, obj);
        }
    }
}