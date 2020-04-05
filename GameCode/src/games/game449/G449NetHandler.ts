module G449 {
    //server2client
    export let C_S_BAOTING = 0x00002001;    //发送报听选择
    export let C_S_GUESTTILES = 0x00002003; //选择猜牌

    export let S_C_BAOTING = 0x00003001;    //发起报听选择
    export let S_C_BAOTINGRESULT = 0x00003002;    //报听结果
    export let S_C_GUESTTILES = 0x00003004;    //开始猜牌
    export let S_C_GUESTRESULT = 0x00003005;
    export let S_C_DONOTGETAFTERTING = 0x00003006; //过听牌

    // // 金币场
    // export let C_S_ONPROXY = 0x0000A001; // 玩家选择是否托管
    // export let C_S_DOREADYSTART = 0x0000A002;  //发送准备结果
    // export let S_C_READY_GAMESTART = 0x0000B001;   //开始倒计时
    // export let S_C_CANCEL_READY = 0x0000B002;  //取消倒计时
    // export let S_C_GOLDUPDATE = 0x0000B003;    //更新金币数
    // export let S_C_NOGOLD = 0x0000B004;    //发送破产协议
    // export let S_C_GOLDPAYRESULT = 0x0000B005;     //发送支付结果协议(不启用)
    // export let S_C_PROXY = 0x0000B006; // 托管广播
    // export let S_C_PLAYERREADYRESULT = 0x0000B007; //广播玩家准备结果

    //吃碰杠胡
    export let ACTION_OPTION = {
        NOT_GET: 0, //不要牌
        CHOW: 1, //吃
        PONG: 2, //碰
        OTHERS_KONG: 3, //其他人打出来的杠
        SELF_KONG: 4, //自己摸到的杠
        CONCEALED_KONG: 5,//暗杠
        HU: 6, //胡
        TING: 7 // 听
    };
}

class G449NetHandler extends G445NetHandler {
    getGameProtoDataList() {
        var classesMapList = [
            [ProtoKeyMJG.C_S_ONPROXY, "C_S_OnProxy"],
            [ProtoKeyMJG.S_C_PROXY, "S_C_Proxy"],
            [ProtoKeyMJG.S_C_GOLDUPDATE, "S_C_GoldUpdate"],

            [ProtoKeyMJG.C_S_DOREADYSTART, "C_S_DoReadyStart"],
            [ProtoKeyMJG.S_C_PLAYERREADYRESULT, "S_C_PlayerReadyResult"],
            [ProtoKeyMJG.S_C_READY_GAMESTART, "S_C_Ready_GameStart"],
            [ProtoKeyMJG.S_C_CANCEL_READY, 'S_C_CanCel_Ready']
        ];

        var classesMapList1 = [
            [G449.C_S_BAOTING, "C_S_BaoTing"],
            [G449.C_S_GUESTTILES, "C_S_GuestTiles"],

            [G449.S_C_BAOTING, "S_C_BaoTing"],
            [G449.S_C_BAOTINGRESULT, "S_C_BaoTing_Result"],
            [G449.S_C_GUESTTILES, "S_C_GuestTiles"],

            [G449.S_C_GUESTRESULT, "S_C_GuestResult"],
            [G449.S_C_DONOTGETAFTERTING,"S_C_DoNotGetAfterTing"],


        ];

        var protoDataList = [
            { pkgName: "twoPeople_mahjong", path: ResourceMgr.GetGameProtoPath(449) + 'twoPeople_mahjong.proto', classesMapList: classesMapList1 },
            { pkgName: "gold_additive", path: ResourceMgr.GetGameProtoPath(449) + 'gold_additive.proto', classesMapList: classesMapList }
        ];

        return protoDataList;
    }
    sendBaoTing(tiles, result) {
        var obj = {
            "tiles": tiles,
            "result": result
        };

        this.sendData(G449.C_S_BAOTING, obj);
    }
    // sendOnProxy(choice) {
    //     var obj = {
    //         "choice": choice
    //     };

    //     this.sendData(G449.C_S_ONPROXY, obj);
    // }
    sendGuestTiles(side) {
        var obj = {
            "side": side
        };

        this.sendData(G449.C_S_GUESTTILES, obj);
    }

    // sendDoReadyStart(result) {
    //     var obj = {
    //         "result": result
    //     };

    //     this.sendData(G449.C_S_DOREADYSTART, obj);
    // }
}