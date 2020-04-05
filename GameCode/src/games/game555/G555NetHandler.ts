
module ProtoKeyJDNN {
    //server2client
    export let C_S_ON_GA = 0x00002001; //下注
    export let C_S_GET_RESULT = 0x00002002;  // 客户端获取结果
    export let C_S_ON_STRIVE = 0x00002003; // 抢庄
    export let C_S_READY_GAME = 0x00002004; // 准备帧
    export let C_S_HAS_BULL_OR_NOT = 0x00002005; // 发送请求有牛没
    export let C_S_SET_START = 0x00002006; // 抢庄完之后发送请求
    export let C_S_TOTAL_BALANCE_DATA = 0x00002007; // 请求当前总战绩




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
    export let S_C_BASE_SCORE = 0x000030010; 
    export let S_C_MESSAGE = 0x000030011; // 消息
    export let S_C_TIMEOUT = 0x000030012; // 倒计时
    export let S_C_STAGE = 0x000030013;
    export let S_C_TOTAL_BALANCE_DATA = 0x000030014; // 总战绩
    export let S_C_WAIT_TIME = 0x000030015; // 
    
}



class G555NetHandler extends PartyNetHandler{
    
    getGameProtoDataList()
    {
        var classesMapList = [
            [ProtoKeyJDNN.C_S_ON_GA, "C_S_OnGa"],
            [ProtoKeyJDNN.C_S_GET_RESULT, "C_S_GetResult"],
            [ProtoKeyJDNN.C_S_ON_STRIVE, "C_S_OnStrive"],
            [ProtoKeyJDNN.C_S_READY_GAME, "C_S_ReadyGame"],
            [ProtoKeyJDNN.C_S_HAS_BULL_OR_NOT, "C_S_HasBullOrNot"],
            [ProtoKeyJDNN.C_S_SET_START, "C_S_SetStart"],
            [ProtoKeyJDNN.C_S_TOTAL_BALANCE_DATA, "C_S_TotalBalanceData"],

            [ProtoKeyJDNN.S_C_GA_DATA, "S_C_GaData"],
            [ProtoKeyJDNN.S_C_GA_CHOOSE, "S_C_Ga_Choose"],
            [ProtoKeyJDNN.S_C_GET_RESULT, "S_C_GetResult"],
            [ProtoKeyJDNN.S_C_TOTAL_REPORT, "S_C_TotalReport"],
            [ProtoKeyJDNN.S_C_DEAL_TILES_NN, "S_C_DealCards"],
            [ProtoKeyJDNN.S_C_GET_ONE_RESULT, "S_C_GetOneResult"],
            [ProtoKeyJDNN.S_C_RESULT_INFO, "S_C_ResultInfo"],
            [ProtoKeyJDNN.S_C_FLY, "S_C_Fly"],
            [ProtoKeyJDNN.S_C_STRIVE_FOR_DEALER, "S_C_StriveForDealer"],
            [ProtoKeyJDNN.S_C_STRIVE_FOR_DEALER_TIMEOUT, "S_C_StriveForDealerTimeout"],
            [ProtoKeyJDNN.S_C_STRIVE_CHOOSE, "S_C_Strive_Choose"],
            [ProtoKeyJDNN.S_C_STRIVE_RESULT, "S_C_Strive_Result"],
            [ProtoKeyJDNN.S_C_READY_GAME, "S_C_ReadyGame"],
            [ProtoKeyJDNN.S_C_READY_GAME_DATA, "S_C_ReadyGameData"],
            [ProtoKeyJDNN.S_C_HAS_BULL_OR_NOT, "S_C_HasBullOrNot"],
            [ProtoKeyJDNN.S_C_BASE_SCORE, "S_C_BaseScore"],
            [ProtoKeyJDNN.S_C_MESSAGE, "S_C_Message"],
            [ProtoKeyJDNN.S_C_TIMEOUT, "S_C_Timeout"],
            [ProtoKeyJDNN.S_C_STAGE, "S_C_Stage"],
            [ProtoKeyJDNN.S_C_TOTAL_BALANCE_DATA, "S_C_TotalBalanceData"],
            [ProtoKeyJDNN.S_C_WAIT_TIME, "S_C_WaitTime"],
            
        ];
        
        var path=ResourceMgr.GetGameProtoPath(555);
        var protoDataList = [
            { pkgName:"private_mahjong", path:path+'private_mahjong.proto' , classesMapList : classesMapList}
        ];
        
        return protoDataList;
    }
    
    sendBid(readyRate,hand)
    {
        var obj = {
            ga : readyRate,
            handnum : hand
        };
        this.sendData(ProtoKeyJDNN.C_S_ON_GA, obj);
    }

    sendGetHistory(gamenum)
    {
        var obj = {
            gamenum : gamenum
        };
        this.sendData(ProtoKeyJDNN.C_S_GET_RESULT, obj);
    }
    
    sendOnStrive(choice)
    {
        var obj = {
            choice : choice
        };
        this.sendData(ProtoKeyJDNN.C_S_ON_STRIVE, obj);
    }

    sendReadyGame()
    {
        this.sendData(ProtoKeyJDNN.C_S_READY_GAME);
    }

    sendOnHasBullOrNot(data)
    {
        var obj = {
            data : data
        };
        this.sendData(ProtoKeyJDNN.C_S_HAS_BULL_OR_NOT, obj);
    }

    sendSetStart()
    {
        this.sendData(ProtoKeyJDNN.C_S_SET_START);
    }

    sendTotalBalanceData(cb)
    {
        this.sendData(ProtoKeyJDNN.C_S_TOTAL_BALANCE_DATA);
        this.createOnceSequenceListener(ProtoKeyJDNN.S_C_TOTAL_BALANCE_DATA,cb);
    }
}