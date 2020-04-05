module G564{
    export let C_S_SET_COLOR = 0x00002001;    // 定缺
    export let C_S_EXCHANGE_THREE = 0x00002002;    // 换三张

    // server2client
    export let S_C_EXCHANGE_FLAG = 0x00003001;     // 换三张标志
    export let S_C_EXCHANGE_THREE = 0x00003002;    // 置换后的牌
    export let S_C_SET_COLOR = 0x00003003;
    export let S_C_EXTRA_MESSAGE = 0x00003004;     // 额外信息
    export let S_C_REFRESH_SCORE = 0x00003005;     // 分数变动
    export let S_C_HUTILES = 0x00003006;   // 胡牌列表
    
    export let S_C_PLAYER_EXCHANGE_THREE = 0x00003007; //换三张结果
    export let S_C_PLAYER_SET_COLOR = 0x00003008;  //选缺结果
}

class G564NetHandler extends G445NetHandler{    
    
    getGameProtoDataList()
    {
        var classesMapList = [
            [ProtoKeyMJG.C_S_ONPROXY, "C_S_OnProxy"],
            [ProtoKeyMJG.S_C_PROXY, "S_C_Proxy"],

            [ProtoKeyMJG.C_S_DOREADYSTART, "C_S_DoReadyStart"],
            [ProtoKeyMJG.S_C_PLAYERREADYRESULT, "S_C_PlayerReadyResult"],
            [ProtoKeyMJG.S_C_READY_GAMESTART, "S_C_Ready_GameStart"]
        ];
        
        var classesMapList2 = [
            [G564.C_S_SET_COLOR, "C_S_SetColor"],
            [G564.C_S_EXCHANGE_THREE, "C_S_ExchangeThree"],
            
            [G564.S_C_EXCHANGE_FLAG, "S_C_ExchangeFlag"],
            [G564.S_C_EXCHANGE_THREE, "S_C_ExchangeThree"],
            [G564.S_C_SET_COLOR, "S_C_SetColor"],
            [G564.S_C_EXTRA_MESSAGE, "S_C_ExtraMessage"],
            [G564.S_C_REFRESH_SCORE, "S_C_RefreshScore"],
            [G564.S_C_HUTILES, "S_C_HuTiles"],

            [G564.S_C_PLAYER_EXCHANGE_THREE, "S_C_PlayerExchangeThree"],
            [G564.S_C_PLAYER_SET_COLOR, "S_C_PlayerSetColor"]
        ];
        
        var path=ResourceMgr.GetGameProtoPath(564);
        var protoDataList = [
            { pkgName:"BloodRiver_mahjong", path:path+'BloodRiver_mahjong.proto' , classesMapList : classesMapList2},
            { pkgName:"gold_additive", path:path+'gold_additive.proto' , classesMapList : classesMapList}
        ];
        
        return protoDataList;
    }

    sendColor(color) 
    {
        this.sendData(G564.C_S_SET_COLOR, color);
    }
    
    sendExchangeThree(tile)
    {
        this.sendData(G564.C_S_EXCHANGE_THREE, tile);
    }
}