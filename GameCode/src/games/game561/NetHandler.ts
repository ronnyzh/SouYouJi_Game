


module G561{

    // gold_additive
    export let C_S_ONPROXY = 0x0000A001; // 玩家选择是否托管
    export let C_S_DOREADYSTART = 0x0000A002;  //发送准备结果

    export let S_C_READY_GAMESTART = 0x0000B001;   //开始倒计时
    export let S_C_CANCEL_READY = 0x0000B002;  //取消倒计时
    export let S_C_GOLDUPDATE = 0x0000B003;    //更新金币数
    export let S_C_NOGOLD = 0x0000B004;    //发送破产协议
    export let S_C_GOLDPAYRESULT = 0x0000B005;     //发送支付结果协议(不启用)
    export let S_C_PROXY = 0x0000B006; // 托管广播
    export let S_C_PLAYERREADYRESULT = 0x0000B007; //广播玩家准备结果

    //zhajinhua_poker
    export let C_S_NEWDOACTION = 0x00002001;//前端action接口
    export let C_S_SHOWTILES = 0x00002002; //前端看牌接口


    export let S_C_SENDRANDOMTILE = 0x00003001;    //打骰
    export let S_C_BOTTOMCASTING = 0x00003002; //下底注
    export let S_C_CANDOACTIONS = 0x00003003;  //可以做的action
    export let S_C_NEWDOACTION = 0x00003004;   //action操作结果
    export let S_C_FIGHTOTHERRESULT = 0x00003005;   //斗牌结果
    export let S_C_SHOWTILES = 0x00003006;   //展示牌
    export let S_C_NEW_REFRESH_DATA = 0x00003007;


    //baseProto
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
    export let S_C_EXIT_ROOM_RESULT =  0x0001000f; //开始游戏前退出房间结果

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


    export class GNetHandler extends PartyNetHandler {

        getGameProtoDataList() {

            var additiveMapList = [
                [C_S_ONPROXY, 'C_S_OnProxy'],
                [C_S_DOREADYSTART, 'C_S_DoReadyStart'],

                [S_C_READY_GAMESTART, 'S_C_Ready_GameStart'],
                [S_C_CANCEL_READY, 'S_C_CanCel_Ready'],
                [S_C_GOLDUPDATE, 'S_C_GoldUpdate'],
                [S_C_NOGOLD, 'S_C_NoGold'],
                [S_C_GOLDPAYRESULT, 'S_C_GoldPayResult'],
                [S_C_PROXY, 'S_C_Proxy'],
                [S_C_PLAYERREADYRESULT, 'S_C_PlayerReadyResult'],

            ];

            var zhajinhuaMapList = [
                [C_S_NEWDOACTION, 'C_S_NewDoAction'],
                [C_S_SHOWTILES, "C_S_ShowTiles"],


                [S_C_SENDRANDOMTILE, 'S_C_SendRandomTile'],
                [S_C_BOTTOMCASTING, 'S_C_BottomCasting'],
                [S_C_CANDOACTIONS, 'S_C_CanDoActions'],
                [S_C_NEWDOACTION, 'S_C_NewDoAction'],
                [S_C_FIGHTOTHERRESULT, 'S_C_FightOtherResult'],
                [S_C_SHOWTILES, 'S_C_ShowTiles'],
                [S_C_NEW_REFRESH_DATA, 'S_C_New_Refresh_Data'],



            ];

            var baseProtoMapList = [
                [C_S_CONNECTING, 'C_S_Connecting'],
                [C_S_DEBUG_CONNECTING, 'C_S_DebugConnecting'],
                [C_S_EXIT_ROOM, 'C_S_ExitRoom'],
                [C_S_PING, 'C_S_Ping', true],
                [C_S_TALK, 'C_S_Talk'],
                [C_S_GM_CONTROL, 'C_S_GMControl'],
                [C_S_DISSOLVE_ROOM, 'C_S_DissolveRoom'],
                [C_S_DISSOLVE_VOTE, 'C_S_DissolveVote'],
                [C_S_DEBUG_PROTO, 'C_S_DebugProto'],
                [C_S_GPS, 'C_S_Gps', true],

                [S_C_CONNECTED, 'S_C_Connected'],
                [S_C_JOIN_ROOM, 'S_C_JoinRoom'],
                [S_C_DISCONNECTED, 'S_C_Disconnected'],
                [S_C_EXIT_ROOM, 'S_C_ExitRoom'],
                [S_C_REFRESH_ROOM_CARD, 'S_C_RefreshRoomCard'],
                [S_C_NOTICE, 'S_C_Notice'],
                [S_C_PING, 'S_C_Ping', true],
                [S_C_TALK, 'S_C_Talk'],
                [S_C_ONLINE_STATE, 'S_C_OnlineState'],
                [S_C_GM_CONTROL, 'S_C_GMControl'],
                [S_C_DISSOLVE_VOTE, 'S_C_DissolveVote'],
                [S_C_DISSOLVE_VOTE_RESULT, 'S_C_DissolveVoteResult'],
                [S_C_DEBUG_PROTO, 'S_C_DebugProto'],
                [S_C_GPS, 'S_C_Gps', true],
                [S_C_EXIT_ROOM_RESULT, 'S_C_ExitRoomResult'],
            ];

            var pokerMapList = [
                [C_S_REFRESH_DATA, 'C_S_RefreshData'],
                [C_S_GAME_START, 'C_S_GameStart'],
                [C_S_DO_ACTION, 'C_S_DoAction'],
                [C_S_READY_NEXT, 'C_S_ReadyNext'],
                [C_S_GET_OLD_BALANCE, 'C_S_GetOldBalance'],

                [S_C_REFRESH_DATA, 'S_C_RefreshData'],
                [S_C_SET_START, 'S_C_SetStart'],
                [S_C_DEAL_CARDS, 'S_C_DealCards'],
                [S_C_TURN_ACTION, 'S_C_TurnAction'],
                [S_C_DO_ACTION_RESULT, 'S_C_DoActionResult'],
                [S_C_BALANCE, 'S_C_Balance'],
                [S_C_GAME_START_RESULT, 'S_C_GameStartResult'],
                [S_C_OLD_BALANCE, 'S_C_OldBalance'],
            ];

            var path=ResourceMgr.GetGameProtoPath(561); 
            var protoDataList = [
                {
                    pkgName: "gold_additive",
                    path: path+'gold_additive.proto',
                    classesMapList: additiveMapList
                },
                {
                    pkgName: "zhajinhua_poker",
                    path: path+'zhajinhua_poker.proto',
                    classesMapList: zhajinhuaMapList
                },
                {pkgName: "baseProto", path: path+'baseProto.proto', classesMapList: baseProtoMapList},
                {pkgName: "poker", path: path+'poker.proto', classesMapList: pokerMapList},
            ];

            return protoDataList;
        }

        //-----------重写
        //因为baseProto和mahjongProto不同，所以部分接口要重写
        enterGame(sid, gameid, cb) {
            var obj = {"sid": sid};
            this.sendData(C_S_CONNECTING, obj);
            this.createOnceSequenceListener(G561.S_C_CONNECTED, cb);
        }

        //------因为用到的协议不同，所以重写这个退房结果 S_C_EXIT_ROOM_RESULT
        sendChangeRoom(cb?){
            this.sendData(ProtoKeyParty.C_S_CHANGE_ROOM);
            if(cb)
                this.createOnceSequenceListener(S_C_EXIT_ROOM_RESULT,cb)
        }

        sendExitRoomConfirm(cb?){
            this.sendData(ProtoKeyParty.C_S_EXIT_ROOM_CONFIRM);
            if(cb)
                this.createOnceSequenceListener(S_C_EXIT_ROOM_RESULT,cb)
        }

        sendChangeRoomConfirm(cb?){
            this.sendData(ProtoKeyParty.C_S_CHANGE_ROOM_CONFIRM);
            if(cb)
                this.createOnceSequenceListener(S_C_EXIT_ROOM_RESULT,cb)
        }

        //END------因为用到的协议不同，所以重写这个退房结果 S_C_EXIT_ROOM_RESULT

        sendExitRoom(cb?) {
            this.sendData(C_S_EXIT_ROOM);
            if (cb)
                this.createOnceListener(S_C_EXIT_ROOM_RESULT, cb);
        }

        refreshData(cb) {
            this.sendData(C_S_REFRESH_DATA);
            this.createOnceSequenceListener(S_C_REFRESH_DATA, cb);
        }

        sendReadyNextRound() {
            this.sendData(C_S_READY_NEXT);
        }

        sendTalk(num, voiceId, duration) {
            var obj = {
                "emoticons": num,
                "voice": voiceId,
                "duration": duration || 1
            };

            this.sendData(C_S_TALK, obj);
        }

        sendPing() {
            this.sendData(C_S_PING);
        }


        gameManage(str, cb) {
            var obj = {};
            obj["GMMessage"] = str;
            this.sendData(C_S_GM_CONTROL, obj);
            this.createOnceListener(S_C_GM_CONTROL, cb);
        }

        //-----------新增

        sendTrustee(isOpen) {
            //0 取消托管  1 进行托管
            let obj = {
                choice: isOpen ? 1 : 0,
            };
            this.sendData(C_S_ONPROXY, obj);
        }

        sendReadyGame() {
            try {
                let obj = {
                    result: true
                }
                this.sendData(C_S_DOREADYSTART, obj);
            } catch (e) {
                console.error(e);
            }

        }

        sendAction(type, datas?, num?, number?) {
            //     message C_S_NewDoAction{
            //     required fixed32 action = 1;
            //     repeated string datas = 2;
            //     required fixed32 num = 3; //action编号
            //     optional fixed32 number = 4; //在比牌时为对手位置,在加注时为倍数,其他情况不取该值
            // }
            var obj = {
                "action": type,
                "datas": datas,
                "num": num,
                "number": number,
            };
            //console.log("-C_S_NEWDOACTION-", obj);
            this.sendData(C_S_NEWDOACTION, obj);
        }

        sendWatch() {
            this.sendData(C_S_SHOWTILES);
        }

        // sendRob(type, operate)
        // {
        //     //0:叫地主，1:叫分，2:抢地主
        //     // required CALL_TYPE choseType = 1;
        //
        //     //如果是叫地主，0是不叫，1是叫
        //     //如果是叫分，0是不叫，1是叫1分，2是叫2分，3是叫3分
        //     //如果是抢地主，0是不抢，1是抢
        //
        //     // required fixed32 operate = 2;
        //     var obj = {};
        //     obj["choseType"] = type;
        //     obj["operate"] = operate;
        //     this.sendData(C_S_ROBLANDLORD, obj);
        // }
    }
}
