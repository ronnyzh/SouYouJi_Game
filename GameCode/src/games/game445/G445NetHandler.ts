
class G445NetHandler extends PartyNetHandler {

    getGameProtoDataList()  {
        var classesMapList = [
            [ProtoKeyMJG.C_S_ONPROXY, "C_S_OnProxy"],
            [ProtoKeyMJG.S_C_PROXY, "S_C_Proxy"],
            [ProtoKeyMJG.S_C_GOLDUPDATE, "S_C_GoldUpdate"],

            [ProtoKeyMJG.C_S_DOREADYSTART, "C_S_DoReadyStart"],
            [ProtoKeyMJG.S_C_PLAYERREADYRESULT, "S_C_PlayerReadyResult"],
            [ProtoKeyMJG.S_C_READY_GAMESTART, "S_C_Ready_GameStart"],
            [ProtoKeyMJG.S_C_NOGOLD, 'S_C_NoGold'],
            [ProtoKeyMJG.S_C_CANCEL_READY, 'S_C_CanCel_Ready']
        ];

        var protoDataList = [
            { pkgName: "gold_additive", path: ResourceMgr.GetGameProtoPath(445) + 'gold_additive.proto', classesMapList: classesMapList }
        ];

        return protoDataList;
    }

    /*
    主动托管: 0 取消托管  1 进行托管
    */
    sendOnProxy(choice)  {
        var obj = {
            choice: choice
        };
        this.sendData(ProtoKeyMJG.C_S_ONPROXY, obj);
    }

    sendReadyGame()  {
        var obj = {
            result: true
        };
        this.sendData(ProtoKeyMJG.C_S_DOREADYSTART, obj);
    }
}