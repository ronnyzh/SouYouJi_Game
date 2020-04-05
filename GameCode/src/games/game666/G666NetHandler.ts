module ProtoKey666{
    //欢乐牛牛专属
     //client2server
    export let C_S_BID = 0x00002001; //下注
    export let C_S_GRAB_DEALER_VOTE = 0x00002002; //玩家抢庄结果

    //server2client
    export let S_C_BID = 0x00003001; //下注
    export let S_C_START_GRABDEALER = 0x00003002; //开始抢庄
    export let S_C_GRABDEALER_VOTERESULT = 0x00003003; //抢庄结果
    export let S_C_AFTER_START = 0x00003004; //开始下注
    //export let S_C_MORETHAN_70PER = 0x00003005; //下注盘高亮
    //export let S_C_FULLBIGPLAYER = 0x00003006; //玩家满注
    export let S_C_SENDSIGN = 0x00003007; //发送玩家标记
    export let S_C_BID_END = 0x00003008; //结算
    export let S_C_AFTERREFRESH = 0x00003009; //重连
    export let S_C_END_GRABDEALER = 0x00003011; //结束抢庄
    export let S_C_END_BID = 0x00003010; //结束下注

    //-----------------------poker
    //client2server
    export let C_S_REFRESH_DATA = 0x00020001; //刷新数据
    export let C_S_GAME_START = 0x00020002; //游戏开始
    export let C_S_DO_ACTION = 0x00020003;
    export let C_S_READY_NEXT = 0x00020004; //关闭结算窗口准备好下一局
    export let C_S_GET_OLD_BALANCE = 0x00020005; //获得上局结算信息

    //server2client
    export let S_C_REFRESH_DATA = 0x00031001; //刷新数据
    export let S_C_SET_START = 0x00031002; //小局开始
    export let S_C_DEAL_CARDS = 0x00031003; //发牌
    export let S_C_TURN_ACTION = 0x00031004; //action可选项
    export let S_C_DO_ACTION_RESULT = 0x00031005;
    export let S_C_BALANCE = 0x00031006; //得分数据
    export let S_C_GAME_START_RESULT = 0x00031007; //开始游戏结果
    export let S_C_OLD_BALANCE = 0x00031008; //上局结算数据

    // ---------------------------------baseProto
    //client2server
    export let C_S_CONNECTING = 0x00000001; //登录
    export let C_S_DEBUG_CONNECTING = 0x00000002; //测试模式登录
    export let C_S_EXIT_ROOM = 0x00000003; //退出房间
    export let C_S_PING = 0x00000004;
    export let C_S_TALK = 0x00000005; //发言，发表情
    export let C_S_GM_CONTROL = 0x00000006; //GM控制
    export let C_S_DISSOLVE_ROOM = 0x00000007; //申请解散房间
    export let C_S_DISSOLVE_VOTE = 0x00000008; //解散投票
    export let C_S_DEBUG_PROTO = 0x00000009; //C_S的单个客户端调试多边，包装协议
    export let C_S_GPS = 0x0000000a; //GPS

    //server2client S_C_CONNECTED
    export let S_C_CONNECTED = 0x00010001; //登录结果
    export let S_C_JOIN_ROOM = 0x00010002; //有玩家加入房间
    export let S_C_DISCONNECTED = 0x00010003; //被断开链接
    export let S_C_EXIT_ROOM = 0x00010004; //有玩家退出房间
    export let S_C_REFRESH_ROOM_CARD = 0x00010005; //刷新房卡
    export let S_C_NOTICE = 0x00010006; //消息
    export let S_C_PING = 0x00010007;
    export let S_C_TALK = 0x00010008; //语音，表情
    export let S_C_ONLINE_STATE = 0x00010009; //离开游戏状态
    export let S_C_GM_CONTROL = 0x0001000a; //GM控制
    export let S_C_DISSOLVE_VOTE = 0x0001000b; //有人发起解散
    export let S_C_DISSOLVE_VOTE_RESULT = 0x0001000c; //某人对解散的投票
    export let S_C_DEBUG_PROTO = 0x0001000d; //S_C的单个客户端调试多边，包装协议
    export let S_C_GPS = 0x0001000e; //GPS
    export let S_C_EXIT_ROOM_RESULT = 0x0001000f; //开始游戏前退出房间结果

    //-----------------------------gold_addtitive.proto
    //client2server
    export let C_S_ONPROXY = 0x0000A001; // 玩家选择是否托管
    export let C_S_DOREADYSTART = 0x0000A002;  //发送准备结果
    //server2client
    export let S_C_READY_GAMESTART = 0x0000B001;   //开始倒计时
    export let S_C_CANCEL_READY = 0x0000B002;  //取消倒计时
    export let S_C_GOLDUPDATE = 0x0000B003;    //更新金币数
    export let S_C_NOGOLD = 0x0000B004;    //发送破产协议
    export let S_C_GOLDPAYRESULT = 0x0000B005;     //发送支付结果协议(不启用)
    export let S_C_PROXY = 0x0000B006; // 托管广播
    export let S_C_PLAYERREADYRESULT = 0x0000B007; //广播玩家准备结果
    export let S_C_READY_GAMESTARTHAPPY = 0x0000B008; //准备
}

class G666NetHandler extends PartyNetHandler{   
    getGameProtoDataList()
    {//欢乐牛牛专属
        let niuniuMapList = [ 
            [ProtoKey666.C_S_BID, "C_S_bid"],
            [ProtoKey666.C_S_GRAB_DEALER_VOTE, "C_S_GrabDealer_Vote"],

            [ProtoKey666.S_C_BID, "S_C_bid"],
            [ProtoKey666.S_C_AFTERREFRESH, "S_C_AfterRefresh"],
            [ProtoKey666.S_C_BID_END, "S_C_Bid_End"],
            [ProtoKey666.S_C_AFTER_START, "S_C_After_Start"],
            [ProtoKey666.S_C_GRABDEALER_VOTERESULT, "S_C_GrabDealer_VoteResult"],
            [ProtoKey666.S_C_START_GRABDEALER, "S_C_Start_GrabDealer"],
            //[ProtoKey666.S_C_MORETHAN_70PER, "S_C_MoreThan_70per"],
            //[ProtoKey666.S_C_FULLBIGPLAYER, "S_C_FullBigPlayer"],
            [ProtoKey666.S_C_SENDSIGN, "S_C_SendSign"],
            [ProtoKey666.S_C_END_GRABDEALER, "S_C_End_GrabDealer"],
            [ProtoKey666.S_C_END_BID, "S_C_End_Bid"],
        ];
        let classesMapList1 = [
                // base
                [ProtoKey666.C_S_CONNECTING, "C_S_Connecting"],
                [ProtoKey666.C_S_DEBUG_CONNECTING, "C_S_DebugConnecting"],
                [ProtoKey666.C_S_EXIT_ROOM, "C_S_ExitRoom"],
                [ProtoKey666.C_S_PING, "C_S_Ping"],
                [ProtoKey666.C_S_TALK, "C_S_Talk"],
                [ProtoKey666.C_S_GM_CONTROL, "C_S_GMControl"],
                [ProtoKey666.C_S_DISSOLVE_ROOM, "C_S_DissolveRoom"],
                [ProtoKey666.C_S_DISSOLVE_VOTE, "C_S_DissolveVote"],
                [ProtoKey666.C_S_DEBUG_PROTO, "C_S_DebugProto"],
                [ProtoKey666.C_S_GPS, "C_S_Gps"],


                [ProtoKey666.S_C_CONNECTED, "S_C_Connected"],
                [ProtoKey666.S_C_JOIN_ROOM, "S_C_JoinRoom"],
                [ProtoKey666.S_C_DISCONNECTED, "S_C_Disconnected"],
                [ProtoKey666.S_C_EXIT_ROOM, "S_C_ExitRoom"],
                [ProtoKey666.S_C_REFRESH_ROOM_CARD, "S_C_RefreshRoomCard"],
                [ProtoKey666.S_C_NOTICE, "S_C_Notice"],
                [ProtoKey666.S_C_PING, "S_C_Ping",true],
                [ProtoKey666.S_C_TALK, "S_C_Talk"],
                [ProtoKey666.S_C_ONLINE_STATE, "S_C_OnlineState"],
                [ProtoKey666.S_C_GM_CONTROL, "S_C_GMControl"],
                [ProtoKey666.S_C_DISSOLVE_VOTE, "S_C_DissolveVote"],
                [ProtoKey666.S_C_DISSOLVE_VOTE_RESULT, "S_C_DissolveVoteResult"],
                [ProtoKey666.S_C_DEBUG_PROTO, "S_C_DebugProto"],
                [ProtoKey666.S_C_GPS, "S_C_Gps"],
                [ProtoKey666.S_C_EXIT_ROOM_RESULT, "S_C_ExitRoomResult"],
            ];

            let classesMapList2 = [
                // poker
                [ProtoKey666.C_S_REFRESH_DATA, "C_S_RefreshData"],
                [ProtoKey666.C_S_GAME_START, "C_S_GameStart"],
                [ProtoKey666.C_S_DO_ACTION, "C_S_DoAction"],
                [ProtoKey666.C_S_READY_NEXT, "C_S_ReadyNext"],
                [ProtoKey666.C_S_GET_OLD_BALANCE, "C_S_GetOldBalance"],

                [ProtoKey666.S_C_REFRESH_DATA, "S_C_RefreshData"],
                [ProtoKey666.S_C_SET_START, "S_C_SetStart"],
                [ProtoKey666.S_C_DEAL_CARDS, "S_C_DealCards"],
                [ProtoKey666.S_C_TURN_ACTION, "S_C_TurnAction"],
                [ProtoKey666.S_C_DO_ACTION_RESULT, "S_C_DoActionResult"],
                [ProtoKey666.S_C_BALANCE, "S_C_Balance"],
                [ProtoKey666.S_C_GAME_START_RESULT, "S_C_GameStartResult"],
                [ProtoKey666.S_C_OLD_BALANCE, "S_C_OldBalance"],

            ];

            let classesMapList3 = [
                //gold_additive.proto
                [ProtoKey666.C_S_ONPROXY,'C_S_OnProxy'],
                [ProtoKey666.C_S_DOREADYSTART,'C_S_DoReadyStart'],

                [ProtoKey666.S_C_READY_GAMESTART,'S_C_Ready_GameStart'],
                [ProtoKey666.S_C_CANCEL_READY,'S_C_CanCel_Ready'],
                [ProtoKey666.S_C_GOLDUPDATE,'S_C_GoldUpdate'],
                [ProtoKey666.S_C_NOGOLD,'S_C_NoGold'],
                [ProtoKey666.S_C_GOLDPAYRESULT,'S_C_GoldPayResult'],
                [ProtoKey666.S_C_PROXY,'S_C_Proxy'],
                [ProtoKey666.S_C_PLAYERREADYRESULT,'S_C_PlayerReadyResult'],
                [ProtoKey666.S_C_READY_GAMESTARTHAPPY,'S_C_Ready_GameStartHappy'],
            ];

            
        var protopath = ResourceMgr.GetGameProtoPath(666);
        var protoDataList = [ 
            { pkgName:"huanle_niuniu", path:protopath+'huanle_niuniu.proto' , classesMapList : niuniuMapList},//新改动地方
            { pkgName: "baseProto", path:protopath+'baseProto.proto', classesMapList: classesMapList1 },
            { pkgName: "poker", path:protopath+'poker.proto', classesMapList: classesMapList2 },
            { pkgName: 'gold_additive',path:protopath+'gold_additive.proto', classesMapList: classesMapList3 },
        ];     
        return protoDataList;
    }

    //---------------请求断线重连
    sendRefreshData(){
        this.sendData(ProtoKey666.C_S_REFRESH_DATA);
    }
    
    //抢庄
    sendOnStrive(vote:boolean)
    {
        this.sendData(ProtoKey666.C_S_GRAB_DEALER_VOTE, vote);
    }

    //下注
    sendBid(place,denomination,qty)
    {
        var obj = {
            place : place,//下注的位置
            denomination : denomination, //下注面额
            qty : qty,//下注的数量
        };
        //console.log('玩家下注---',obj);
        this.sendData(ProtoKey666.C_S_BID, obj);
    }

    sendChangeRoom(cb?) {
        this.sendData(ProtoKeyParty.C_S_CHANGE_ROOM);
    }
    //----------------------base、poker

    enterGame(sid, gameid, cb) {
        let obj = { "sid": sid };
        this.sendData(ProtoKey666.C_S_CONNECTING, obj);
        this.createOnceSequenceListener(ProtoKey666.S_C_CONNECTED, cb);
    }

    sendExitRoom(cb?) {
        this.sendData(ProtoKey666.C_S_EXIT_ROOM);
    }

    sendExitRoomConfirm(cb?) {
        this.sendData(ProtoKeyParty.C_S_EXIT_ROOM_CONFIRM);
    }

    refreshData(cb) {
        this.sendData(ProtoKey666.C_S_REFRESH_DATA);
        this.createOnceSequenceListener(ProtoKey666.S_C_REFRESH_DATA, cb);
    }

    sendReadyNextRound()
    {
        this.sendData(ProtoKey666.C_S_READY_NEXT);
    }

    sendTalk(num, voiceId, duration)
    {
        var obj = {
            "emoticons" : num,
            "voice" : voiceId,
            "duration" : duration || 1
        };

        this.sendData(ProtoKey666.C_S_TALK, obj);
    }

    sendPing()
    {
        this.sendData(ProtoKey666.C_S_PING);
    }

    sendAction(type, actionData, actionNum)
    {
        var obj = {
            "action" : type,
            "tiles" : actionData,
            "num" : actionNum
        };
        this.sendData(ProtoKey666.C_S_DO_ACTION, obj);
    }

    gameManage(str, cb)
    {
        var obj = {};
        obj["GMMessage"] = str;
        this.sendData(ProtoKey666.C_S_GM_CONTROL, obj);
        this.createOnceListener(ProtoKey666.S_C_GM_CONTROL, cb);
    }
}