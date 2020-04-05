module ProtoKey556{
    //server2client
    export let C_S_ON_GA = 0x00002001; //下注
    export let C_S_GET_RESULT = 0x00002002;  // 客户端获取结果
    export let C_S_ON_STRIVE = 0x00002003; // 抢庄
    export let C_S_READY_GAME = 0x00002004; // 准备帧
    export let C_S_HAS_BULL_OR_NOT = 0x00002005; // 发送请求有牛没
    export let C_S_TOTAL_BALANCE_DATA = 0x00002007;

    //server2client
    export let S_C_GA_DATA = 0x00003001;          // 下注返回数据
    export let S_C_GA_CHOOSE  =  0x000030002;     //
    export let S_C_GET_RESULT = 0x000030003;      // 结果返回
    export let S_C_TOTAL_REPORT = 0x000030004;    // 大局结算
    export let S_C_DEAL_TILES_NN = 0x000030005; // 手牌
    export let S_C_GET_ONE_RESULT = 0x000030006; // 单个玩家返回
    export let S_C_RESULT_INFO = 0x000030007; // 输赢结果 
    export let S_C_FLY = 0x000030008;
    export let S_C_STRIVE_FOR_DEALER = 0x000030009; // 抢庄
    export let S_C_STRIVE_FOR_DEALER_TIMEOUT = 0x00003000a; // 抢庄等待时间
    export let S_C_STRIVE_CHOOSE = 0x00003000b; // 抢庄确认帧
    export let S_C_STRIVE_RESULT = 0x00003000c; // 抢庄结果
    export let S_C_READY_GAME = 0x00003000d; // 准备数据
    export let S_C_READY_GAME_DATA = 0x00003000e; // 准备按钮
    export let S_C_HAS_BULL_OR_NOT = 0x00003000f;
    export let S_C_MESSAGE = 0x000030093; // 消息
    export let S_C_TOTAL_BALANCE_DATA = 0x000030092; // 总战绩
    export let S_C_ADDL_REPORT_CUR_GAME = 0x000030094;  //赣州单局结算报表需要的数据
    export let S_C_OLD_ADDL_REPORT_CUR_GAME = 0x000030095;  //赣州上一局单局结算报表需要的数据
    // export let S_C_BASE_SCORE = 0x000030010;

    export let S_C_WAIT_TIME = 0x000030090;
    export let S_C_SWAP_DEALER = 0x000030091;//换位
}

class G556NetHandler extends PartyNetHandler{

    getClassesMapList(){
        var classesMapList = [
            [ProtoKey556.C_S_ON_GA, "C_S_OnGa"],
            [ProtoKey556.C_S_GET_RESULT, "C_S_GetResult"],
            [ProtoKey556.C_S_ON_STRIVE, "C_S_OnStrive"],
            [ProtoKey556.C_S_READY_GAME, "C_S_ReadyGame"],
            [ProtoKey556.C_S_HAS_BULL_OR_NOT, "C_S_HasBullOrNot"],
            [ProtoKey556.C_S_TOTAL_BALANCE_DATA, "C_S_TotalBalanceData"],

            [ProtoKey556.S_C_GA_DATA, "S_C_GaData"],
            [ProtoKey556.S_C_GA_CHOOSE, "S_C_Ga_Choose"],
            [ProtoKey556.S_C_GET_RESULT, "S_C_GetResult"],
            [ProtoKey556.S_C_TOTAL_REPORT, "S_C_TotalReport"],
            [ProtoKey556.S_C_DEAL_TILES_NN, "S_C_DealCards"],
            [ProtoKey556.S_C_GET_ONE_RESULT, "S_C_GetOneResult"],
            [ProtoKey556.S_C_RESULT_INFO, "S_C_ResultInfo"],
            [ProtoKey556.S_C_FLY, "S_C_Fly"],
            [ProtoKey556.S_C_STRIVE_FOR_DEALER, "S_C_StriveForDealer"],
            [ProtoKey556.S_C_STRIVE_FOR_DEALER_TIMEOUT, "S_C_StriveForDealerTimeout"],
            [ProtoKey556.S_C_STRIVE_CHOOSE, "S_C_Strive_Choose"],
            [ProtoKey556.S_C_STRIVE_RESULT, "S_C_Strive_Result"],
            [ProtoKey556.S_C_READY_GAME, "S_C_ReadyGame"],
            [ProtoKey556.S_C_READY_GAME_DATA, "S_C_ReadyGameData"],
            [ProtoKey556.S_C_HAS_BULL_OR_NOT, "S_C_HasBullOrNot"],

            [ProtoKey556.S_C_SWAP_DEALER, "S_C_SwapDealer"],
            [ProtoKey556.S_C_WAIT_TIME, "S_C_WaitTime"],
            [ProtoKey556.S_C_TOTAL_BALANCE_DATA, "S_C_TotalBalanceData"],
            [ProtoKey556.S_C_MESSAGE, "S_C_Message"],
            [ProtoKey556.S_C_ADDL_REPORT_CUR_GAME, "S_C_AddlReportCurGame"],
            [ProtoKey556.S_C_OLD_ADDL_REPORT_CUR_GAME, "S_C_OldAddlReportCurGame"],
            // [ProtoKey556.S_C_BASE_SCORE, "S_C_BaseScore"],
        ];
        return classesMapList;
    }
    
    getGameProtoDataList()
    {
        var path=ResourceMgr.GetGameProtoPath(556);
        var classesMapList=this.getClassesMapList();
        var protoDataList = [
            { pkgName:"private_mahjong", path:path+'private_mahjong.proto' , classesMapList : classesMapList}
        ];
        
        return protoDataList;
    }
    
    sendReadyGame()
    {
        this.sendData(ProtoKey556.C_S_READY_GAME);
    }
    
    sendBid(readyRate,hand)
    {
        var obj = {
            ga : readyRate,
            handnum : hand
        };
        this.sendData(ProtoKey556.C_S_ON_GA, obj);
    }
    
    sendOnHasBullOrNot(data)
    {
        var obj = {
            data : data
        };
        this.sendData(ProtoKey556.C_S_HAS_BULL_OR_NOT, obj);
    }
    
    sendOnStrive(choice)
    {
        var obj = {
            choice : choice
        };
        this.sendData(ProtoKey556.C_S_ON_STRIVE, obj);
    }
}