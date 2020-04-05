
module ProtoKey {
    // client2server
    export let C_S_CONNECTING = 0x00000001; //登录
    export let C_S_DEBUG_CONNECTING = 0x00000002; //测试模式登录
    export let C_S_EXIT_ROOM = 0x00000003; //退出房间
    export let C_S_REFRESH_DATA = 0x00000004; //刷新数据
    export let C_S_PING = 0x00000005;
    export let C_S_TALK = 0x00000006; //发言，发表情
    export let C_S_GM_CONTROL = 0x00000007; //GM控制
    export let C_S_GAME_START = 0x00000008; //游戏开始
    export let C_S_ROLL_DICE = 0x00000009; //打骰
    export let C_S_DISCARD = 0x0000000a; //出牌
    export let C_S_DO_ACTION = 0x0000000b; //吃碰杠胡牌
    export let C_S_DISSOLVE_ROOM = 0x0000000c; //申请解散房间
    export let C_S_DISSOLVE_VOTE = 0x0000000d; //解散投票
    export let C_S_READY_NEXT = 0x0000000e; //关闭结算窗口准备好下一局
    export let C_S_DEBUG_PROTO = 0x0000000f;
    export let C_S_GPS = 0x00000010; //GPS
    export let C_S_GET_READY_HAND = 0x00000011; //获得听牌列表
    export let C_S_GET_OLD_BALANCE = 0x0000001a; //获得上局结算信息
    // export let C_S_DEBUG_ACTION = 0x0000000f; //单人控制四人模式下C2S协议
    export let C_S_GET_READY_HAND_FANCY = 0x0000001b;

    //server2client
    export let S_C_CONNECTED = 0x00001001; //登录结果
    export let S_C_JOIN_ROOM = 0x00001002; //有玩家加入房间
    export let S_C_DISCONNECTED = 0x00001003; //被断开链接
    export let S_C_EXIT_ROOM = 0x00001004; //有玩家退出房间
    export let S_C_REFRESH_DATA = 0x00001005; //刷新数据
    export let S_C_REFRESH_ROOM_CARD = 0x00001006; //刷新房卡
    export let S_C_NOTICE = 0x00001007; //消息
    export let S_C_PING = 0x00001008;
    export let S_C_TALK = 0x00001009; //语音，表情
    export let S_C_ONLINE_STATE = 0x0000100a; //离开游戏状态
    export let S_C_GM_CONTROL = 0x0000100b; //GM控制
    export let S_C_SET_START = 0x0000100c; //小局开始
    export let S_C_DEAL_TILES = 0x0000100d; //手牌
    export let S_C_DRAW_TILES = 0x0000100e; //摸牌
    export let S_C_DISCARD = 0x0000100f; //出牌
    export let S_C_ALLOW_ACTION = 0x00001010; //吃碰杠胡可选项
    export let S_C_DO_ACTION = 0x00001011; //选择吃碰杠胡
    export let S_C_DISSOLVE_VOTE = 0x00001012; //有人发起解散
    export let S_C_DISSOLVE_VOTE_RESULT = 0x00001013; //某人对解散的投票
    export let S_C_BALANCE = 0x00001014; //得分数据
    export let S_C_ROLL_DICE = 0x00001015; //打色
    export let S_C_DEBUG_PROTO = 0x00001016;
    export let S_C_GPS = 0x00001017; //GPS
    export let S_C_READY_HAND = 0x00001018; //听牌
    export let S_C_EXIT_ROOM_RESULT = 0x00001019; //开始游戏前退出房间结果
    export let S_C_GAME_START_RESULT = 0x0000101a; //开始游戏结果
    export let S_C_OLD_BALANCE = 0x0000101b; //上局结算数据
}

var ZIP_MSG_LIST = [
    ProtoKey.S_C_CONNECTED
];

class BaseProtoNetHandler extends NetHandler {

    public classesMapList = [
        [ProtoKey.C_S_CONNECTING, "C_S_Connecting"],
        [ProtoKey.C_S_DEBUG_CONNECTING, "C_S_DebugConnecting"],
        [ProtoKey.C_S_EXIT_ROOM, "C_S_ExitRoom"],
        [ProtoKey.C_S_REFRESH_DATA, "C_S_RefreshData"],
        [ProtoKey.C_S_PING, "C_S_Ping", true],
        [ProtoKey.C_S_TALK, "C_S_Talk"],
        [ProtoKey.C_S_GM_CONTROL, "C_S_GMControl"],
        [ProtoKey.C_S_GAME_START, "C_S_GameStart"],
        [ProtoKey.C_S_ROLL_DICE, "C_S_RollDice"],
        [ProtoKey.C_S_DISCARD, "C_S_Discard"],
        [ProtoKey.C_S_DO_ACTION, "C_S_DoAction"],
        [ProtoKey.C_S_DISSOLVE_ROOM, "C_S_DissolveRoom"],
        [ProtoKey.C_S_DISSOLVE_VOTE, "C_S_DissolveVote"],
        [ProtoKey.C_S_READY_NEXT, "C_S_ReadyNext"],
        [ProtoKey.C_S_DEBUG_PROTO, "C_S_DebugProto"],
        [ProtoKey.C_S_GPS, "C_S_Gps", true],
        [ProtoKey.C_S_GET_READY_HAND, "C_S_GetReadyHand"],
        [ProtoKey.C_S_GET_OLD_BALANCE, "C_S_GetOldBalance"],
        [ProtoKey.C_S_GET_READY_HAND_FANCY, "C_S_GetReadyHandFancy"],

        [ProtoKey.S_C_CONNECTED, "S_C_Connected"],
        [ProtoKey.S_C_JOIN_ROOM, "S_C_JoinRoom"],
        [ProtoKey.S_C_DISCONNECTED, "S_C_Disconnected"],
        [ProtoKey.S_C_EXIT_ROOM, "S_C_ExitRoom"],
        [ProtoKey.S_C_REFRESH_DATA, "S_C_RefreshData"],
        [ProtoKey.S_C_REFRESH_ROOM_CARD, "S_C_RefreshRoomCard"],
        [ProtoKey.S_C_NOTICE, "S_C_Notice"],
        [ProtoKey.S_C_PING, "S_C_Ping", true],
        [ProtoKey.S_C_TALK, "S_C_Talk"],
        [ProtoKey.S_C_ONLINE_STATE, "S_C_OnlineState"],
        [ProtoKey.S_C_GM_CONTROL, "S_C_GMControl"],
        [ProtoKey.S_C_SET_START, "S_C_SetStart"],
        [ProtoKey.S_C_ROLL_DICE, "S_C_RollDice"],
        [ProtoKey.S_C_DEAL_TILES, "S_C_DealTiles"],
        [ProtoKey.S_C_DRAW_TILES, "S_C_DrawTiles"],
        [ProtoKey.S_C_DISCARD, "S_C_Discard"],
        [ProtoKey.S_C_ALLOW_ACTION, "S_C_AllowAction"],
        [ProtoKey.S_C_DO_ACTION, "S_C_DoAction"],
        [ProtoKey.S_C_DISSOLVE_VOTE, "S_C_DissolveVote"],
        [ProtoKey.S_C_DISSOLVE_VOTE_RESULT, "S_C_DissolveVoteResult"],
        [ProtoKey.S_C_BALANCE, "S_C_Balance"],
        [ProtoKey.S_C_DEBUG_PROTO, "S_C_DebugProto"],
        [ProtoKey.S_C_GPS, "S_C_Gps", true],
        [ProtoKey.S_C_READY_HAND, "S_C_ReadyHand"],
        [ProtoKey.S_C_EXIT_ROOM_RESULT, "S_C_ExitRoomResult"],
        [ProtoKey.S_C_GAME_START_RESULT, "S_C_GameStartResult"],
        [ProtoKey.S_C_OLD_BALANCE, "S_C_OldBalance"]
    ]

    constructor() {
        super();
        var extendList: any = this.getExtendProtoDataList();
        var protoDataList = [{ pkgName: "mahjong", path: ResourceMgr.PROTO_PATH + "mahjong.proto", classesMapList: this.classesMapList }];
        if (extendList != null)
            protoDataList = protoDataList.concat(extendList);
        var extendList: any = this.getGameProtoDataList();
        if (extendList != null)
            protoDataList = protoDataList.concat(extendList);
            
        this.init(protoDataList);
    }

    getExtendProtoDataList() {
    }

    getGameProtoDataList() {
    }

    addServerDisconnectEventListen(gameid)
    {
        //console.log(gameid,GallNetHandle.ProtoKeyDisconnect[gameid]);
        this.addMsgListener(GallNetHandle.ProtoKeyDisconnect[gameid], this.onServerDisconnect.bind(this));
    }

    onServerDisconnect(msgData) 
    {
        Alert.show(ExtendMgr.inst.getText4Language(msgData["reason"] || "")).onYes(function () 
        {
            MasterMgr.inst.switch('lobby');
        });
        this.disconnect();
    }

    public sendData(msgType: number, obj: any = {}): void {
        obj = obj || {};
        var zip = ZIP_MSG_LIST.indexOf(msgType) != -1;
        var data = this._encodeData(msgType, obj, true, zip);
        this.socket.send(data);
        //console.log('sendData 2');
    }

    //------------------------------------------------业务层方法封装--------------------------------------------------

    enterGame(sid,gameid,cb) 
    {
        /*
        let newcb = (data)=>
        {
            console.log("-------------");
            if (data['reason']) 
            {
                Alert.show(ExtendMgr.inst.getText4Language(data['reason'])).onYes(function () 
                {
                    MasterMgr.inst.switch('lobby');
                });
                return;
            }
            this.addServerDisconnectEventListen(gameid);
            cb(data);
        }
        this.createOnceSequenceListener(GallNetHandle.ProtoKeyConnected[gameid], newcb);
        */
        this.addServerDisconnectEventListen(gameid);
        this.createOnceSequenceListener(GallNetHandle.ProtoKeyConnected[gameid],cb); //GallNetHandle.ProtoKeyConnected[gameid]
        var obj = { "sid": sid };
        this.sendData(ProtoKey.C_S_CONNECTING, obj);
    }

    sendExitRoom(cb?) {
        this.sendData(ProtoKey.C_S_EXIT_ROOM);
        if (cb)
            this.createOnceListener(ProtoKey.S_C_EXIT_ROOM_RESULT, cb);
    }

    refreshData(cb) {
        this.sendData(ProtoKey.C_S_REFRESH_DATA);
        this.createOnceSequenceListener(ProtoKey.S_C_REFRESH_DATA, cb);
    }

    sendReadyNextRound() {
        this.sendData(ProtoKey.C_S_READY_NEXT);
    }
    sendGetReadyHand() {
        this.sendData(ProtoKey.C_S_GET_READY_HAND)
    }
    sendFancyTile(id) {
        var obj = {};
        obj["fancytile"] = id;
        this.sendData(ProtoKey.C_S_GET_READY_HAND_FANCY, obj);
    }

    sendTalk(num, voiceId, duration) {
        var obj = {
            "emoticons": num,
            "voice": voiceId,
            "duration": duration || 1
        };

        this.sendData(ProtoKey.C_S_TALK, obj);
    }

    sendPing() {
        this.sendData(ProtoKey.C_S_PING);
    }

    sendDiscard(tileId) {
        var obj = {
            "tile": tileId
        };
        this.sendData(ProtoKey.C_S_DISCARD, obj);
    }

    sendAction(type, actionData, actionNum) {
        var obj = {
            "action": type,
            "tiles": actionData,
            "num": actionNum
        };
        this.sendData(ProtoKey.C_S_DO_ACTION, obj);
    }

    gameManage(str, cb) {
        var obj = {};
        obj["GMMessage"] = str;
        this.sendData(ProtoKey.C_S_GM_CONTROL, obj);
        this.createOnceListener(ProtoKey.S_C_GM_CONTROL, cb);
    }
}