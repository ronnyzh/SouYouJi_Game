
module ProtoKeyHLPD {
    //server2client
    export let C_S_ON_GA = 0x00002001; //下注
    export let C_S_GET_RESULT = 0x00002002;  // 客户端获取结果
    export let C_S_ON_STRIVE = 0x00002003; // 抢庄
    export let C_S_READY_GAME = 0x00002004; // 准备帧
    export let C_S_HAS_BULL_OR_NOT = 0x00002005; // 发送请求有牛没
    export let C_S_TOTAL_BALANCE_DATA = 0x00002007; // 请求当前总战绩
    export let C_S_DRAW_TILE = 0x00002008;  




    //server2client
    export let S_C_GA_DATA = 0x00003001;          // 下注返回数据
    export let S_C_GA_CHOOSE  =  0x000030002;     //  
    export let S_C_GET_RESULT = 0x000030003;      // 结果返回
    export let S_C_TOTAL_REPORT = 0x000030004;    // 大局结算
    export let S_C_DEAL_CARDS = 0x000030005; // 手牌
    export let S_C_GET_ONE_RESULT = 0x000030006; // 单个玩家返回
    export let S_C_RESULT_INFO = 0x000030007; // 输赢结果 
    export let S_C_FLY = 0x000030008; //  飞金币
    export let S_C_STRIVE_FOR_DEALER = 0x000030009; // 抢庄
    export let S_C_STRIVE_FOR_DEALER_TIMEOUT = 0x00003000a; // 抢庄等待时间
    export let S_C_STRIVE_CHOOSE = 0x00003000b; // 抢庄确认帧
    export let S_C_STRIVE_RESULT = 0x00003000c; // 抢庄结果
    export let S_C_READY_GAME = 0x00003000d; // 准备数据
    export let S_C_READY_GAME_DATA = 0x00003000e; // 准备按钮
    export let S_C_HAS_BULL_OR_NOT = 0x00003000f; // 有牛无牛
    export let S_C_MESSAGE = 0x000030011; // 消息
    export let S_C_TOTAL_BALANCE_DATA = 0x000030014; // 总战绩
    export let S_C_WAIT_TIME = 0x000030090; // 倒计时
    export let S_C_SWAP_DEALER = 0x000030091;//换位
    export let S_C_ADDL_REPORT_CUR_GAME = 0x000030094;  //赣州单局结算报表需要的数据
    export let S_C_OLD_ADDL_REPORT_CUR_GAME = 0x000030095;  //赣州上一局单局结算报表需要的数据
    export let S_C_DRAW_TILE = 0x000030096;
}



class G557NetHandler extends PartyNetHandler{
    
    getGameProtoDataList()
    {
        var classesMapList = [
            [ProtoKeyHLPD.C_S_ON_GA, "C_S_OnGa"],
            [ProtoKeyHLPD.C_S_GET_RESULT, "C_S_GetResult"],
            [ProtoKeyHLPD.C_S_ON_STRIVE, "C_S_OnStrive"],
            [ProtoKeyHLPD.C_S_READY_GAME, "C_S_ReadyGame"],
            [ProtoKeyHLPD.C_S_HAS_BULL_OR_NOT, "C_S_HasBullOrNot"],
            [ProtoKeyHLPD.C_S_TOTAL_BALANCE_DATA, "C_S_TotalBalanceData"],
            [ProtoKeyHLPD.C_S_DRAW_TILE, "C_S_DrawTile"],

            [ProtoKeyHLPD.S_C_GA_DATA, "S_C_GaData"],
            [ProtoKeyHLPD.S_C_GA_CHOOSE, "S_C_Ga_Choose"],
            [ProtoKeyHLPD.S_C_GET_RESULT, "S_C_GetResult"],
            [ProtoKeyHLPD.S_C_TOTAL_REPORT, "S_C_TotalReport"],
            [ProtoKeyHLPD.S_C_GET_ONE_RESULT, "S_C_GetOneResult"],
            [ProtoKeyHLPD.S_C_RESULT_INFO, "S_C_ResultInfo"],
            [ProtoKeyHLPD.S_C_FLY, "S_C_Fly"],
            [ProtoKeyHLPD.S_C_STRIVE_FOR_DEALER, "S_C_StriveForDealer"],
            [ProtoKeyHLPD.S_C_STRIVE_FOR_DEALER_TIMEOUT, "S_C_StriveForDealerTimeout"],
            [ProtoKeyHLPD.S_C_STRIVE_CHOOSE, "S_C_Strive_Choose"],
            [ProtoKeyHLPD.S_C_STRIVE_RESULT, "S_C_Strive_Result"],
            [ProtoKeyHLPD.S_C_READY_GAME, "S_C_ReadyGame"],
            [ProtoKeyHLPD.S_C_READY_GAME_DATA, "S_C_ReadyGameData"],
            [ProtoKeyHLPD.S_C_HAS_BULL_OR_NOT, "S_C_HasBullOrNot"],
            [ProtoKeyHLPD.S_C_MESSAGE, "S_C_Message"],
            [ProtoKeyHLPD.S_C_TOTAL_BALANCE_DATA, "S_C_TotalBalanceData"],
            [ProtoKeyHLPD.S_C_DEAL_CARDS, "S_C_DealCards"],
            [ProtoKeyHLPD.S_C_DRAW_TILE, "S_C_DrawTile"],
            [ProtoKeyHLPD.S_C_WAIT_TIME, "S_C_WaitTime"],
        ];
        
        var path=ResourceMgr.GetGameProtoPath(557);
        var protoDataList = [
            { pkgName:"hainan_mahjong", path:path+'private_mahjong.proto' , classesMapList : classesMapList}
        ];
        
        return protoDataList;
    }
    
   sendBid(readyRate,hand)
    {
        var obj = {
            ga : readyRate,
            handnum : hand
        };
        this.sendData(ProtoKeyHLPD.C_S_ON_GA, obj);
    }

    sendGetHistory(gamenum)
    {
        var obj = {
            gamenum : gamenum
        };
        this.sendData(ProtoKeyHLPD.C_S_GET_RESULT, obj);
    }
    
    sendOnStrive(choice)
    {
        var obj = {
            choice : choice
        };
        this.sendData(ProtoKeyHLPD.C_S_ON_STRIVE, obj);
    }

    sendReadyGame()
    {
        this.sendData(ProtoKeyHLPD.C_S_READY_GAME);
    }

    sendOnHasBullOrNot(data)
    {
        var obj = {
            data : data
        };
        this.sendData(ProtoKeyHLPD.C_S_HAS_BULL_OR_NOT, obj);
    }
    
    sendDrawTile(drawTile)
    {
        var obj = {
            drawTile : drawTile
        };
        this.sendData(ProtoKeyHLPD.C_S_DRAW_TILE, obj);
    }

    sendTotalBalanceData(cb)
    {
        this.sendData(ProtoKeyHLPD.C_S_TOTAL_BALANCE_DATA);
        this.createOnceSequenceListener(ProtoKeyHLPD.S_C_TOTAL_BALANCE_DATA,cb);
    }
}