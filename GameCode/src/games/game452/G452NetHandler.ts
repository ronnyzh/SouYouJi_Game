
class G452NetHandler extends G445NetHandler{
    
    getGameProtoDataList()
    {
        var classesMapList = [
            [ProtoKeyMJG.C_S_ONPROXY, "C_S_OnProxy"],
            [ProtoKeyMJG.S_C_PROXY, "S_C_Proxy"],
            [ProtoKeyMJG.S_C_GOLDUPDATE, "S_C_GoldUpdate"],

            [ProtoKeyMJG.C_S_DOREADYSTART, "C_S_DoReadyStart"],
            [ProtoKeyMJG.S_C_PLAYERREADYRESULT, "S_C_PlayerReadyResult"],
            [ProtoKeyMJG.S_C_READY_GAMESTART, "S_C_Ready_GameStart"]
        ];
        var classesMapList2 = [
            [ProtoKeyMJG.S_C_RUNHORSE, "S_C_RunHorse"]
        ];
        
        var path=ResourceMgr.GetGameProtoPath(452);
        var protoDataList = [
            { pkgName:"gold_additive", path:path+'gold_additive.proto' , classesMapList : classesMapList},
            { pkgName:"jidahu_mahjong", path:path+'jidahu_mahjong.proto' , classesMapList : classesMapList2}
        ];
        
        return protoDataList;
    }
}