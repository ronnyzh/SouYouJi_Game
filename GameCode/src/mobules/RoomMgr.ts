class RoomMgr{
    private static _inst:RoomMgr = null;
    public static get inst():RoomMgr{
        if(RoomMgr._inst == null){
            RoomMgr._inst = new RoomMgr();
        }
        return RoomMgr._inst;
    }

    public roomId:number = null;
    public maxNumOfGames:number = 0;
    public numOfGames:number = 0;
    public seatIndex:number = -1;
    public seats:any = null;
    public testSeat = null;
    public isOver:boolean = false;
    public conf = null;
    public dissoveData = null;
    public costConfs = null;
    public gameMode:string = null;
    public gameType:string = null;
    public localIndexList:any = [];
    public unlimitedMaxChair = null
    constructor(){
        this.init();
    }

    init () {
        this.reset();
        var agent = new NetAgent('roommgr',true);
        bk.net.addAgent(agent);
        agent.addTarget(this);

        EventMgr.on("scene_switched",this,function(){
            bk.on("room_dissolve_notice", this,this.showDissolveNotice);

            bk.on('disconnect',this,function(){
                RoomMgr.inst.dissoveData = null;
            });

            if (RoomMgr.inst.dissoveData) {
                this.showDissolveNotice();
            }
        });
    }

    reset() {
        this.roomId = null;
        this.maxNumOfGames = 0;
        this.numOfGames = 0;
        this.seatIndex = -1;
        this.seats = null;
        this.testSeat = null;
        this.isOver = false;
        this.conf = null;
        this.dissoveData = null;
    }

    /**
     * 根据游戏类型 获取花费
     * @param  {Number} maxChair    最大人数
     * @param  {Number} turns       最大局数
     * @param  {Number} isAA        是否AA制
     * @param  {Number} gameType    游戏类型 （游戏编号）
     * @param  {Number} gameMode    游戏模式 （金币、钻石等）
     * @return {Number}             具体花费
     */
    calcCost (maxChair, turns, isAA, gameType, gameMode) {
        var config = this.costConfs;
        if(!config||config==undefined)
        {
            return 0;
        }
        for (var i = 0; i < config.length; i++) {
            var tConfig = config[i];
            if (!tConfig) {
                continue;
            }
            if ((tConfig.game_mode === gameMode) && (tConfig.game_type === gameType)) {
                config = tConfig.cost_conf;
                break;
            }
        }

        if (!config) {
            return 0;
        }

        var t = config[maxChair];
        if (!t) {
            return 0;
        }

        var total = t[turns];
        if (total > 0) {
            if (isAA) {
                return total / maxChair;
            }
            return total;
        }

        return 0;
    }

    // 设定每个座位的信息
    setSeatInfo(seatIdx, data) {
        var seat = {
            userId: data.userid,
            ip: data.ip,
            score: data.score,
            name: data.name,
            online: data.online,
            ready: data.ready,
            seatIndex: data.seatindex
        };
        this.getSeats()[seatIdx] = seat;
        return seat;
    }

    getSeats():any {
        return this.seats;
    }


    showDissolveNotice(){
        if(!SceneMgr.inst.currentScene.isGameScene){
            return;
        }
        UIMgr.inst.popup(UI_DissolveNotice);
    }

    onLogin(data) {
        this.roomId = data.roomid;
        this.gameType = data.gametype;
        this.gameMode = data.gamemode;
        console.log("roomid and game type mode", data);
        this.conf = data.conf;
        this.maxNumOfGames = data.conf.numOfGames;
        this.numOfGames = data.numofgames;
        this.seats = [];
        for (var i = 0; i < data.seats.length; ++i) {
            this.setSeatInfo(i, data.seats[i]);
            if (UserMgr.inst.userId == data.seats[i].userid) {
                this.seatIndex = i;
            }
        }
        this.isOver = false;
    }

    //自己是否为房主
    isOwner () {
        this.getSeats();
        return UserMgr.inst.userId == this.conf.creator;
    }

    //通过角色ID获取房间座位号码
    getSeatIndexByID (userId) {
        for (var i = 0; i < this.getSeats().length; ++i) {
            var s = this.getSeats()[i];
            if (s.userId == userId) {
                return i;
            }
        }
        return -1;
    }

    //通过角色ID获取座位信息
    getSeatByID (userId) {
        var tIdx = this.getSeatIndexByID(userId);
        var seat = this.getSeats()[tIdx];
        return seat;
    }

    // 通过服务器座位号索引获取seatInfo
    getSeatByIdx (idx) {
        return this.getSeats()[idx];
    }

    //通过服务器座位号索引获取本地座位号索引
    getLocalIndex (index) {
        this.getSeats();
        var tMaxChair = this.getMaxPlayerNum();

        var tLocalIndexList = this.getLocalIndexList();
        if (!tLocalIndexList) {
            var ret = (index - this.seatIndex + tMaxChair) % tMaxChair;
            return ret;
        }
        else {
            var tSelfIdx = -1;
            var tTargetIdx = -1;
            for (var i = 0; i < tLocalIndexList.length; i++) {
                if (tLocalIndexList[i] === this.seatIndex) {
                    tSelfIdx = i;
                }
                if (tLocalIndexList[i] === index) {
                    tTargetIdx = i;
                }
            }
            if (tSelfIdx === -1 || tTargetIdx === -1) {
                return -1;
            }
            else {
                return (tSelfIdx > tTargetIdx) ? (tMaxChair - (tSelfIdx - tTargetIdx)) : (tTargetIdx - tSelfIdx);
            }
        }
    }

    // 通过本地座位号索引获取seatInfo
    getSeatInfoByLocalIndex (localIdx) {
        var tMaxChair = this.getMaxPlayerNum();
        var tIdx = (localIdx + this.seatIndex) % tMaxChair;
        var tLocalIndexList = this.getLocalIndexList();
        var tSeatList;

        if (!tLocalIndexList) {
            tSeatList = this.getSeats();
            return tSeatList[tIdx];
        }
        else {
            for (var i = 0; i < tLocalIndexList.length; i++) {
                if (tIdx === tLocalIndexList[i]) {
                    break;
                }
            }

            if (i === tLocalIndexList.length) {
                return null;
            }
            else {
                tSeatList = this.getSeats();
                return tSeatList[tLocalIndexList[i]];
            }
        }

    }

    /** 是否人数不限 */
    setIsUnlimitedMaxChair (isUnlimited) {
        //this.unlimitedMaxChair = isUnlimited;
    }

    /** 一圈座位的转法 [0,5,4,1,3,2] */
    setLocalIndexList (list) {
        this.localIndexList = list;
    }

    /** 一圈座位的转法 */
    getLocalIndexList () {
        return this.localIndexList;
    }

    // 获取最大玩家数量
    getMaxPlayerNum () {
        if(this.conf.type == "niuniu_1"){
            return 8;
        }
        if (this.unlimitedMaxChair) {
            var tMaxChair = this.getSeats().length;
            for (tMaxChair; tMaxChair > 0; tMaxChair--) {
                if (this.getSeats()[tMaxChair - 1].userId) {
                    break;
                }
            }
            return tMaxChair;
        }

        if ("numPeople" in this.conf) {
            return this.conf.numPeople;
        }
        return this.conf.maxChair;
    }

    //获取自己的座位信息
    getSelfData () {
        return this.getSeats()[this.seatIndex];
    }

    //通过房间座位号码获取玩家名字
    getName (index) {
        return this.getSeats()[index].name;
    }

    //通过userID获取玩家名字
    getNameByUserID (userID) {
        var tRoomMgr = this;
        var tSeatInfo = tRoomMgr.getSeatByID(userID);
        return tSeatInfo.name;
    }

    //通过userID获取玩家IP
    getIPByUserID (userID) {
        var ip;
        var tSeatInfo;
        var tRoomMgr = this;
        if (userID === UserMgr.inst.userId) {
            ip = UserMgr.inst.ip;
        }
        else if (tSeatInfo = tRoomMgr.getSeatByID(userID)) {
            ip = tSeatInfo.ip;
        }

        if (!ip) {
            return "掉线";
        }

        if (ip.indexOf("::ffff:") != -1) {
            ip = ip.substr(7);
        }

        return ip;
    }

    clearReady () {
        for (var i = 0; i < this.getSeats().length; ++i) {
            this.getSeats()[i].ready = false;
        }
    }

    //准备
    ownReady () {
        if (bk.online) {
            bk.net.send('ready');
        }
        else {                  //非联网状态直接设定所有人为准备状态
            var tSeats = this.getSeats();
            for (var i = 0; i < tSeats.length; i++) {
                tSeats[i].ready = true;
            }

            bk.emit("room_user_state_changed");
        }
    }

    sendRoomDispress () {
        if (bk.online) {
            bk.net.send("dispress");
        }
    }

    sendRoomExit () {
        if (bk.online) {
            bk.net.send("exit");
        }
    }

    sendRoomDissolveRequest () {
        if (bk.online) {
            bk.net.send("dissolve_request");
        }
    }

    wantQuitRoom () {
        var tRoomMgr = this;
        if (!bk.online) {
            tRoomMgr.reset();
            bk.emit("back_sub_halls");
            return;
        }

        if (tRoomMgr.numOfGames != 0) {
            Alert.show(ExtendMgr.inst.getText4Language('是否要发起协商解散请求？'),true).onYes(function(){
                tRoomMgr.sendRoomDissolveRequest();
            });
            return;
        }

        var isCreator = tRoomMgr.isOwner();
        if (isCreator) {
            Alert.show(ExtendMgr.inst.getText4Language('解散未开始的房间不扣房卡，是否要解散？'),true).onYes(function(){
                tRoomMgr.sendRoomDispress();
            });
        }
        else {
            Alert.show(ExtendMgr.inst.getText4Language('确定要退出吗？'),true).onYes(function(){
                tRoomMgr.sendRoomExit();
            });
        }
    }

    //同意解散房间
    sendRoomDissolveAgree () {
        if (!bk.online) {
            bk.emit("back_sub_halls");
        }
        else {
            bk.net.send("dissolve_agree");
        }
    }

    // 拒绝解散房间
    sendRoomDissolveReject () {
        if (!bk.online) {
        }
        else {
            bk.net.send("dissolve_reject");
        }
    }

    //===========网络消息相关处理函数================
    onnet_dissolve_notice_push (data) {
        this.dissoveData = data;
        bk.emit("room_dissolve_notice", data);
    }

    onnet_dissolve_cancel_push (data) {
        this.dissoveData = null;
        bk.emit("room_dissolve_cancel", data);
    }

    onnet_exit_result (data) {
        this.isOver = true;
        this.reset();
        var entry = MasterMgr.current.setting.entry_scene; 
        if(entry){
            SceneMgr.inst.replace(entry);
        }
        else{
            MasterMgr.inst.switch('lobby');
        }
    }

    onnet_dispress_push (data) {
        this.reset();
        this.isOver = true;
        var entry = MasterMgr.current.setting.entry_scene; 
        if(entry){
            SceneMgr.inst.replace(entry);
        }
        else{
            MasterMgr.inst.switch('lobby');
        }
    }

    onnet_exit_notify_push (data) {
        var userId = data;
        var s = this.getSeatByID(userId);
        if (s != null) {
            s.userId = 0;
            s.name = "";
            bk.emit("room_user_state_changed", s);
        }
    }

    onnet_new_user_comes_push (data) {
        //GameLogic.updateData("new_user_comes_push", data);
        // console.log(data);
        var seatIndex = data.seatindex;
        var curSeat = this.getSeats()[seatIndex];
        if (curSeat.userId > 0) {
            curSeat.online = true;
        }
        else {
            data.online = true;
            curSeat = this.setSeatInfo(seatIndex, data);
        }

        bk.emit('room_new_user', curSeat);
    }

    //Gps获取位置事件监听 
    onnet_location_push (data) {
        if (data) {
            bk.emit("check_location", data);
        }
    }

    onnet_user_state_push (data) {
        //console.log(data);
        var userId = data.userid;
        var seat = this.getSeatByID(userId);
        seat.online = data.online;
        bk.emit('room_user_state_changed', seat);
    }

    onnet_room_user_ready_push (data) {
        //console.log(data);
        var userId = data.userid;
        var seat = this.getSeatByID(userId);
        seat.ready = data.ready;
        bk.emit('room_user_ready', seat);
        bk.emit("room_user_state_changed", seat);
    }

    onnet_game_num_push (data) {
        this.numOfGames = data;
        bk.emit('room_game_num', data);
    }

    onnet_room_close_push (data) {
        this.isOver = true;
        this.dissoveData = data;
        bk.emit('room_close', data);
    }

    onnet_room_seats_changed_push (data) {
        var seats = this.getSeats();
        this.seats = [];
        for (var i = 0; i < data.length; ++i) {
            var userId = data[i];
            for (var k in seats) {
                var s = seats[k];
                if (s.userId == userId) {
                    this.seats[i] = s;
                    s.seatIndex = i;
                    break;
                }
            }
            if (userId == UserMgr.inst.userId) {
                this.seatIndex = i;
            }
        }
        bk.emit('room_user_state_changed', null);
    }
}
