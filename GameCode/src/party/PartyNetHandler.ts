module ProtoKeyParty{
    export let C_S_GET_WATCHER = 0x00004001; //获取观察者
    export let C_S_IS_GOLD = 0x00004002;
    export let C_S_EXIT_ROOM_CONFIRM = 0x00004003;
    export let C_S_CHANGE_ROOM = 0x00004004;
    export let C_S_CHANGE_ROOM_CONFIRM = 0x00004005;


    export let S_C_WATCHER_INFO = 0x00005001; //获取观察者
    export let S_C_PAY = 0x00005002;
    export let S_C_GOLD_MESSAGE = 0x00005003; //消息
    export let S_C_IS_GOLD = 0x00005004;
    export let S_C_PLAYER_INFO = 0x00005005; // 

    //宝箱
    export let C_S_GET_CHETS_STATUS = 0x00002199; // 查看获奖状态
    export let C_S_GET_CHETS_CHANGE = 0x00002197;// 领取奖励

    export let S_C_CHETS_STATUS = 0x00003199; // 发送奖池状态
    export let S_C_CHETS_CHANGE = 0x00003197; // 发送领取结果
    export let S_C_CHETS_SEND_STATUS = 0x00003196; // 发送宝箱
}

class PartyNetHandler extends BaseProtoNetHandler{
    
    getExtendProtoDataList(){
        var GoldMapList = [
            [ProtoKeyParty.C_S_GET_WATCHER, "C_S_GetWatcher"],
            [ProtoKeyParty.C_S_IS_GOLD, "C_S_IsGold"],
            [ProtoKeyParty.C_S_EXIT_ROOM_CONFIRM, "C_S_ExitRoomConfirm"],
            [ProtoKeyParty.C_S_CHANGE_ROOM, "C_S_ChangeRoom"],
            [ProtoKeyParty.C_S_CHANGE_ROOM_CONFIRM, "C_S_ChangeRoomConfirm"],

            [ProtoKeyParty.S_C_WATCHER_INFO, "S_C_WatcherInfo"],
            [ProtoKeyParty.S_C_PAY, "S_C_Pay"],
            [ProtoKeyParty.S_C_GOLD_MESSAGE, "S_C_GoldMessage"],
            [ProtoKeyParty.S_C_IS_GOLD, "S_C_IsGold"],
            [ProtoKeyParty.S_C_PLAYER_INFO, "S_C_PlayerInfo"]
        ];
        
        var protoDataList = [
            { pkgName:"gold_niuniu", path : ResourceMgr.PROTO_PATH+'gold.proto',  classesMapList : GoldMapList}
        ];
        return protoDataList;
    }
    
    sendExitRoomConfirm(cb?){
        this.sendData(ProtoKeyParty.C_S_EXIT_ROOM_CONFIRM);
        if(cb)
            this.createOnceSequenceListener(ProtoKey.S_C_EXIT_ROOM_RESULT,cb)
    }
    
    sendChangeRoom(cb?){
        this.sendData(ProtoKeyParty.C_S_CHANGE_ROOM);
        if(cb)
            this.createOnceSequenceListener(ProtoKey.S_C_EXIT_ROOM_RESULT,cb)
    }

    sendChangeRoomConfirm(cb?){
        this.sendData(ProtoKeyParty.C_S_CHANGE_ROOM_CONFIRM);
        if(cb)
            this.createOnceSequenceListener(ProtoKey.S_C_EXIT_ROOM_RESULT,cb)
    }
    
    sendIsGold(cb:Function=null) {
        this.sendData(ProtoKeyParty.C_S_IS_GOLD);
        if(cb)
            this.createOnceListener(ProtoKeyParty.S_C_IS_GOLD, cb);
    }
}