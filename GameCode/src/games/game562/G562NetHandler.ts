
module G562 {
    // replay4proto

    //poker
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

    // baseProto
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

    //server2client
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

    // thirteenWater_poker
    //server2client
    export let C_S_ARRANGED_CARDS = 0x00012001; //整理过的牌
    export let C_S_SET_MULTIPLE = 0x00012002; //设置倍数
    export let C_S_GET_ARRANGED_CARDS = 0x00012003;

    //server2client
    export let S_C_REFRESH_DATAS = 0x00013001; //刷新数据
    export let S_C_NEW_DEAL_CARDS = 0x00013002; //发牌
    export let S_C_ARRANGED_CARDS = 0x00013003;
    export let S_C_COMPARE = 0x00013004; //比牌
    export let S_C_SET_MULTIPLE = 0x00013005; //设置倍数
    export let S_C_MULTIPLE_RESULT = 0x00013006; //倍数结果
    export let S_C_SEND_OK_DATA = 0x00013007;
    export let S_C_MY_ARRANGED_CARDS = 0x00013008;
    export let S_C_WAIT_TIME = 0x0001001f; // 倒计时 
    export let S_C_READY_GAMESTART = 0x00013009; // 开始游戏倒计时
    export let S_C_CANCEL_READY = 0x00013010; // 取消倒计时

    export class G562NetHandler extends PartyNetHandler {

        getGameProtoDataList() {
            let classesMapList = [
                // thirteenWater
                [C_S_ARRANGED_CARDS, "C_S_ArrangedCards"],
                [C_S_SET_MULTIPLE, "C_S_SetMultiple"],
                [C_S_GET_ARRANGED_CARDS, "C_S_GetArrangedCards"],

                [S_C_REFRESH_DATAS, "S_C_RefreshDatas"],
                [S_C_NEW_DEAL_CARDS, "S_C_NewDealCards"],
                [S_C_ARRANGED_CARDS, "S_C_ArrangedCards"],
                [S_C_COMPARE, "S_C_Compare"],
                [S_C_SET_MULTIPLE, "S_C_SetMultiple"],
                [S_C_MULTIPLE_RESULT, "S_C_MultipleResult"],
                [S_C_SEND_OK_DATA, "S_C_SendOkData"],
                [S_C_MY_ARRANGED_CARDS, "S_C_MyArrangedCards"]
            ];

            let classesMapList1 = [
                // base
                [C_S_CONNECTING, "C_S_Connecting"],
                [C_S_DEBUG_CONNECTING, "C_S_DebugConnecting"],
                [C_S_EXIT_ROOM, "C_S_ExitRoom"],
                [C_S_PING, "C_S_Ping"],
                [C_S_TALK, "C_S_Talk"],
                [C_S_GM_CONTROL, "C_S_GMControl"],
                [C_S_DISSOLVE_ROOM, "C_S_DissolveRoom"],
                [C_S_DISSOLVE_VOTE, "C_S_DissolveVote"],
                [C_S_DEBUG_PROTO, "C_S_DebugProto"],
                [C_S_GPS, "C_S_Gps"],

                [S_C_CONNECTED, "S_C_Connected"],
                [S_C_JOIN_ROOM, "S_C_JoinRoom"],
                [S_C_DISCONNECTED, "S_C_Disconnected"],
                [S_C_EXIT_ROOM, "S_C_ExitRoom"],
                [S_C_REFRESH_ROOM_CARD, "S_C_RefreshRoomCard"],
                [S_C_NOTICE, "S_C_Notice"],
                [S_C_PING, "S_C_Ping"],
                [S_C_TALK, "S_C_Talk"],
                [S_C_ONLINE_STATE, "S_C_OnlineState"],
                [S_C_GM_CONTROL, "S_C_GMControl"],
                [S_C_DISSOLVE_VOTE, "S_C_DissolveVote"],
                [S_C_DISSOLVE_VOTE_RESULT, "S_C_DissolveVoteResult"],
                [S_C_DEBUG_PROTO, "S_C_DebugProto"],
                [S_C_GPS, "S_C_Gps"],
                [S_C_EXIT_ROOM_RESULT, "S_C_ExitRoomResult"],
                [S_C_WAIT_TIME, "S_C_WaitTime"],
                [S_C_READY_GAMESTART, 'S_C_ReadyGameStart'],
                [S_C_CANCEL_READY, 'S_C_CancelReady'],
            ];

            let classesMapList2 = [
                // poker
                [C_S_REFRESH_DATA, "C_S_RefreshData"],
                [C_S_GAME_START, "C_S_GameStart"],
                [C_S_DO_ACTION, "C_S_DoAction"],
                [C_S_READY_NEXT, "C_S_ReadyNext"],
                [C_S_GET_OLD_BALANCE, "C_S_GetOldBalance"],

                [S_C_REFRESH_DATA, "S_C_RefreshData"],
                [S_C_SET_START, "S_C_SetStart"],
                [S_C_DEAL_CARDS, "S_C_DealCards"],
                [S_C_TURN_ACTION, "S_C_TurnAction"],
                [S_C_DO_ACTION_RESULT, "S_C_DoActionResult"],
                [S_C_BALANCE, "S_C_Balance"],
                [S_C_GAME_START_RESULT, "S_C_GameStartResult"],
                [S_C_OLD_BALANCE, "S_C_OldBalance"],

            ];

            let path = ResourceMgr.GetGameProtoPath(562);
            let protoDataList = [
                { pkgName: "baseProto", path: path + 'baseProto.proto', classesMapList: classesMapList1 },
                { pkgName: "poker", path: path + 'poker.proto', classesMapList: classesMapList2 },
                { pkgName: "thirteenWater_poker", path: path + 'thirteenWater_poker.proto', classesMapList: classesMapList }
            ];

            return protoDataList;
        }

        /*sendArrangedCards(cards,cardTypes)
        {
            let obj = {
                cards : cards,
                cardTypes : cardTypes
            };
            this.sendData(C_S_ARRANGED_CARDS, obj);
        }
    
        sendGetHistory(multiple)
        {
            let obj = {
                multiple : multiple
            };
            this.sendData(C_S_SET_MULTIPLE, obj);
        }
        
        sendOnStrive()
        {
            let obj = {
            };
            this.sendData(C_S_GET_ARRANGED_CARDS, obj);
        }*/

        sendGetArrangedCards() {
            this.sendData(C_S_GET_ARRANGED_CARDS);
        }
        //------------------------------------------------业务层方法封装--------------------------------------------------
        debugEnterGame(data, cb) {
            // debugMode = data["debugMode"];// || CONNECT_MODE.ACCOUNT_PASSWD;
            let obj = {};
            obj["account"] = data["account"] || "";
            obj["passwd"] = data["pwd"] || "";
            // obj["mode"] = debugMode;
            let settings = {
                //0为加入房间，1为创建房间
                action: data["roomId"] == null ? 1 : 0,
                roomid: data["roomId"] || "",
                rule: data["rule"] || ""
            };
            obj["roomSetting"] = settings;
            this.sendData(C_S_DEBUG_CONNECTING, obj);
            this.createOnceSequenceListener(S_C_CONNECTED, cb);
        }

        enterGame(sid, gameid, cb) {
            let obj = { "sid": sid };
            this.addServerDisconnectEventListen(gameid);
            this.sendData(C_S_CONNECTING, obj);
            this.createOnceSequenceListener(S_C_CONNECTED, cb);
        }

        sendExitRoom(cb) {
            this.sendData(C_S_EXIT_ROOM);
            this.createOnceListener(S_C_EXIT_ROOM_RESULT, cb);
        }

        sendGameStart(cb) {
            this.sendData(C_S_GAME_START);
            this.createOnceListener(S_C_GAME_START_RESULT, cb);
        }

        sendSetMultiple(num) {
            let obj = {
                "multiple": num
            };

            this.sendData(C_S_SET_MULTIPLE, obj);
        }

        sendArrangedCards(cards, cardTypes) {
            let obj = {
                "cards": cards,
                "cardTypes": cardTypes
            };

            this.sendData(C_S_ARRANGED_CARDS, obj);
        }

        sendDissolve() {
            this.sendData(C_S_DISSOLVE_ROOM);
        }

        sendDissolveVote(agree) {
            let obj = {
                "result": agree
            };

            this.sendData(C_S_DISSOLVE_VOTE, obj);
        }

        refreshData(cb) {
            //console.log(cb, "监听了refreshData");
            this.sendData(C_S_REFRESH_DATA);
            this.createOnceSequenceListener(S_C_REFRESH_DATAS, cb);
        }

        sendTalk(num, voiceId, duration) {
            let obj = {
                "emoticons": num,
                "voice": voiceId,
                "duration": duration || 1
            };

            this.sendData(C_S_TALK, obj);
        }

        sendPing() {
            this.sendData(C_S_PING);
        }

        sendReadyNextRound() {
            this.sendData(C_S_READY_NEXT);
        }

        gameManage(str, cb) {
            let obj = {};
            obj["GMMessage"] = str;

            this.sendData(C_S_GM_CONTROL, obj);
            this.createOnceListener(S_C_GM_CONTROL, cb);
        }

        sendGPS(pos) {
            let obj = {};
            obj["gpsValue"] = pos;
            this.sendData(C_S_GPS, obj);
        }

        getOldBalance(cb) {
            this.sendData(C_S_GET_OLD_BALANCE);
            this.createOnceListener(S_C_OLD_BALANCE, cb);
        }

        getArrangedCards(cb) {
            this.sendData(C_S_GET_ARRANGED_CARDS);
            this.createOnceSequenceListener(S_C_MY_ARRANGED_CARDS, cb);
        }

        sendChangeRoom(cb?) {
            // console.log(cb, "======sendChangeRoom====");
            this.sendData(ProtoKeyParty.C_S_CHANGE_ROOM);
            if (cb)
                this.createOnceSequenceListener(S_C_EXIT_ROOM_RESULT, cb)
        }

    }
}