/*
* name;
*/
//
class G666Page extends Page {
    //GUI组件属性
    private roomID: fairygui.GLabel;
    private btn_ready: fairygui.GButton;
    private showTime: fairygui.GComponent;//倒计时组件
    private show_strive: fairygui.GComponent;//抢庄组件
    private show_bid: fairygui.GComponent;//下注组件
    private Gold_Layout: fairygui.GComponent;//金币容器组件
    private Poker_Layout: fairygui.GComponent;//扑克容器组件
    private c_bar: fairygui.Controller = null;//下注条控制
    private showBar_Q: fairygui.Transition;//动效
    private showBar_X: fairygui.Transition;//动效
    private matching: fairygui.GComponent;//匹配动效
    //--------优化
    private btnList: fairygui.GComponent;
    private AreaCom: fairygui.GComponent;
    private c_showArea: fairygui.Controller = null;//四个下注区显示控制
    private start_ani: fairygui.GComponent;
    private msg: fairygui.GComponent;
    //正常属性
    private static seconds_time: number = 8;//倒计时

    private PlayerFrames: Array<G666PlayerFrame> = [];
    private isZhuang: boolean = false;
    private selfInfo: any;//存放玩家自己信息
    private cashAsMode: string = 'bitmap';//cashAs模式
    private buttonMode: number = 1;//按钮屏蔽
    private isChangeRoom: boolean = false;
    private resetSelectedIndex: number = 0;//重置房间是用
    //2019-1-15属性规范整理
    private serverPlayerList: any;//存放服务器玩家列表
    private isAfterRefresh: boolean = false;//记录玩家是否断线重连上来
    private isCloseExitRoomResult: boolean = false;//是否屏蔽退房监听函数
    private bankerSide: number;//庄家在本地座位号
    private selfSide: number;//玩家自己再本地座位号
    private place = 1;//下注位置
    private denomination = 1;//下注面额
    private quantity = 1;//下注数量
    private bei: any;//用来记录每个下注按钮的额度
    private isInitPlace: boolean = false;//记录下注区是否已经绑定回调函数 防止重复绑定
    private niuIndex = [];//存放欢乐顶出来两张扑克牌的下标
    private show_4_tiles: Array<string> = [];//先亮的四张牌
    private show_5_tiles: Array<string> = [];//最后亮的那张牌
    private AllPokers: Array<any> = [];//服务器发过来所有牌值
    private stageOneTiles = [];
    private count: number = 0;//控制最后一张牌亮牌顺序


    constructor() {
        super("G666", "GameScene", UILayer.GAME);
    }

    clearView() {
        Laya.timer.clearAll(this);
        Laya.Tween.clearAll(this);
        if (this._view != null) {
            this._view.removeChildren();
        }
    }
    onDispose() {
        this._view.dispose();
        G666.soundMgr.stopBGM();
    }
    onCreated(data: any = null) {
        if (!data) return;
        let url = ResourceMgr.RES_PATH + 'bg/bg7.jpg';
        Tools.inst.changeBackground(url, this._view.getChild('bg').asLoader);
        G666.soundMgr.playBGM();
        var view = this._view;
        for (let i = 0; i < 8; i++) {
            this.PlayerFrames.push(new G666PlayerFrame({
                seat: view.getChild('seat' + i).asCom,
            }));
        }
        //初始化GUI按钮和组件属性
        this.roomID = view.getChild('roomId').asLabel;
        this.btn_ready = view.getChild('btn_ready').asButton;
        this.showTime = view.getChild('showTime').asCom;
        this.show_strive = view.getChild('show_strive').asCom;
        this.show_bid = view.getChild('show_bid').asCom;
        this.matching = view.getChild('matching').asCom;
        this.start_ani = view.getChild('start_ani').asCom;
        this.c_bar = view.getController('c_bar');
        this.showBar_Q = view.getTransition('showBar_Q');
        this.showBar_X = view.getTransition('showBar_X');
        //-------------下注区域优化
        this.AreaCom = view.getChild('AreaCom').asCom;
        this.msg = this.AreaCom.getChild('msg').asCom;
        this.c_showArea = this.AreaCom.getController('c_showArea');

        this.Gold_Layout = this.AreaCom.getChild('Gold_Layout').asCom;
        this.Poker_Layout = this.AreaCom.getChild('Poker_Layout').asCom;

        this.btnList = view.getChild('btnList').asCom;
        let c_btnList = this.btnList.getController('c1');
        let open = this.btnList.getChild('open').asButton;
        let close = this.btnList.getChild('close').asButton;
        let btn_setting = this.btnList.getChild('btn_setting').asButton;
        let btn_exit = this.btnList.getChild('btn_exit').asButton;
        let btn_history = this.btnList.getChild('btn_history').asButton;
        let btn_rule = this.btnList.getChild('btn_rule').asButton;

        open.onClick(this, function () {
            c_btnList.selectedIndex = 1;
        });
        close.onClick(this, function () {
            c_btnList.selectedIndex = 0;
        });
        btn_setting.onClick(this, function () {
            UIMgr.inst.popup(UI_Setting);
        });
        btn_exit.onClick(this, this.onExitRoom);
        btn_history.onClick(this, function () {
            let obj = UIMgr.inst.popup(UI_History) as UI_History;
            obj.refreshGameListInGame(666);
        });
        btn_rule.onClick(this, function () {
            let rule = UIMgr.inst.popup(UI_Rules) as UI_Rules;
            rule.refreshData('game' + 666);
        });
        //------优化end
        this.btn_ready.onClick(this, this.onExchangeRoom.bind(this));
        this.reset();//清除座位信息
        //this.onEnterRoomSuccess(data);   
    }//onCreate结束括号

    onNetIntoGame(data) {
        this.onEnterRoomSuccess(data);
    }

    onExchangeRoom() {
        this.isChangeRoom = true;
        NetHandlerMgr.netHandler.sendChangeRoom((msgData) => { });//(msgData) => { }
    }

    releaseRes() {
        Laya.timer.clearAll(this);
        Laya.Tween.clearAll(this);
        G666Page._pokerCache = {};
        this.show_4_tiles = [];
        this.show_5_tiles = [];
        this.niuIndex = [];
        this.stageOneTiles = [];
    }

    //卸载clickRect下注区绑定事件
    offBtnHandler() {
        this.isInitPlace = false;
        let name = ['area_1', 'area_2', 'area_3', 'area_4'];
        for (let i = 0; i < 4; ++i) {
            let area = this.AreaCom.getChild(name[i]).asCom;//clickRect
            if (area == null) continue;
            let clickRect = area.getChild('place').asCom;
            clickRect.enabled = false;
            clickRect.offClick(this, this.handerBid);
        }
    }

    resetRoom() {
        this.offBtnHandler();
        this.clearSign();
        this.isAfterRefresh = false;
        if (this.isChangeRoom && this.bankerSide >= 0 && this.bankerSide <= 6) {
            this.swapSeat();
        }
        let c_chose = this.show_bid.getController('c_chose');
        c_chose.selectedIndex = 0;
        this.isCloseExitRoomResult = false;
        this.isChangeRoom = false;
        this.Gold_Layout.removeChildren();
        this.Poker_Layout.removeChildren();
        this.btn_ready.visible = false;
        this.isZhuang = false;
        this.matching.visible = false;
        this.c_bar.setSelectedIndex(this.resetSelectedIndex);
        this.c_showArea.setSelectedIndex(this.resetSelectedIndex);
        for (let i = 0; i < 5; ++i) {
            //-------消除扑克牌
            let pokersCom = this.AreaCom.getChild('pokers_' + i).asCom;
            pokersCom.getController('c_show').selectedIndex = 0;
            let name = ['n0', 'n1', 'n2', 'n3', 'n4'];
            for (let j = 0, len = name.length; j < len; ++j) {
                let pkCom = pokersCom.getChild(name[j]).asCom
                let c1 = pkCom.getController('c1');
                c1.selectedIndex = 0;
            }
            //------
            let showNN_Com = this.AreaCom.getChild('showNN_' + i).asCom;
            showNN_Com.getController('c_showNN').setSelectedIndex(this.resetSelectedIndex);
            if (i == 0) continue;
            let scoreCom = this.AreaCom.getChild('score_' + i).asCom;
            scoreCom.getChild('totalScore').text = '0';
            scoreCom.getChild('selfScore').text = '0';
        }
        for (let i = 1; i < 5; ++i) {
            let area = this.AreaCom.getChild('area_' + i).asCom;
            area.getChild('place').offClick(this, this.handerBid);
            let name = 't' + i;
            this.AreaCom.getChild(name).text = '';
        }
        this.releaseRes();
    }

    //按钮屏蔽
    destoryAllBtn() {
        let open = this.btnList.getChild('open').asButton;
        let close = this.btnList.getChild('close').asButton;
        let btn_setting = this.btnList.getChild('btn_setting').asButton;
        let btn_exit = this.btnList.getChild('btn_exit').asButton;
        let btn_history = this.btnList.getChild('btn_history').asButton;
        let btn_rule = this.btnList.getChild('btn_rule').asButton;
        let btn_ready = this.btn_ready;
        let btnArray = [open, close, btn_setting, btn_exit, btn_history, btn_rule, btn_ready];
        for (let i = 0, len = btnArray.length; i < len; ++i) {
            btnArray[i].mode = this.buttonMode;
        }
    }
    //cashAs优化
    initBitmap() {
        for (let i = 0; i < 8; ++i) {
            let seat = this._view.getChild('seat' + i).asCom;
            seat.displayObject.cacheAs = this.cashAsMode;
        }
        for (let i = 0; i < 5; ++i) {
            let pokerCom = this.AreaCom.getChild('pokers_' + i).asCom;
            pokerCom.displayObject.cacheAs = this.cashAsMode;
            let showNN = this.AreaCom.getChild('showNN_' + i).asCom;
            showNN.displayObject.cacheAs = this.cashAsMode;
            if (i == 0) continue;
            let area = this.AreaCom.getChild('area_' + i).asCom;
            area.displayObject.cacheAs = this.cashAsMode;
        }
        let bg = this.AreaCom.getChild('bg').asCom;
        bg.displayObject.cacheAs = this.cashAsMode;
        this.show_strive.displayObject.cacheAs = this.cashAsMode;
        this.show_bid.displayObject.cacheAs = this.cashAsMode;
        this.btnList.displayObject.cacheAs = this.cashAsMode;
        this.msg.displayObject.cacheAs = this.cashAsMode;
    }

    //倒计时
    cutDownTime(time, index) {
        Laya.timer.clear(this, this.cutTime);
        G666Page.seconds_time = parseInt((parseInt(time) / 1000).toString());
        Laya.timer.loop(1000, this, this.cutTime, [index]);
    }
    //倒计时递减
    cutTime(index) {
        let c_showTime = this.showTime.getController('c_showTime');
        c_showTime.selectedIndex = index;
        if (G666Page.seconds_time < 0) {
            c_showTime.selectedIndex = 0;
        }
        this.showTime.getChild('time').asLabel.text = (G666Page.seconds_time--).toString();
    }
    onExitRoom() {
        NetHandlerMgr.netHandler.sendExitRoom();
    }

    //链接结果
    reconnectResult(connected) {
        if (!connected) return;
        let sid = UserMgr.inst.sid;
        NetHandlerMgr.netHandler.enterGame(sid, 666, this.onEnterRoomSuccess.bind(this));
        NetHandlerMgr.inst.initPingListen(ProtoKey666.S_C_PING);
    }

    //获取玩家座位
    getPlayer(side: number): G666PlayerFrame {
        return this.PlayerFrames[side];
    }

    showMatch() {
        this.matching.getTransition('matching').play();
    }

    isOpenMatching(isShow: boolean = false) {
        this.matching.visible = isShow;
        if (isShow) {
            Laya.timer.loop(1750, this, this.showMatch.bind(this), null, false);
        } else {
            Laya.timer.clear(this, this.showMatch);
            this.matching.getTransition('matching').stop();
        }
    }

    //进入房间成功
    onEnterRoomSuccess(data) {
        let myInfo = data["myInfo"];
        //开启匹配
        this.isOpenMatching(true);
        //断线重连，请求当前游戏数据
        if (myInfo["isRefresh"]) {
            this.refreshInfo();//如果断线重连则请求刷新界面信息
        }
        else {
            this.initGame(myInfo);//否则认为是第一次进入房间,初始化房间信息.
        }
    }

    //断线重连刷新界面信息
    refreshInfo() {
        NetHandlerMgr.netHandler.refreshData(function (msg) {
            if (msg["result"]) {
                let refreshData = msg["data"];
                let gameInfo = refreshData["gameInfo"];
                let roomInfo = gameInfo["roomInfo"];
                //是否已经初始化过
                if (this.posServerSelf == null)
                    this.initGame(gameInfo);
                else
                    this.initRoomInfo(roomInfo);
            }
            else {
                //退出房间
                this.onExitRoom();
            }
        }.bind(this));
    }
    //初始化游戏信息
    initGame(msg) {
        let roomInfo = msg['roomInfo'];
        if (!msg['result']) {
            let reason = msg['reason'].toString();
            reason = ExtendMgr.inst.getText4Language(reason);
            Alert.show(reason).onYes(function () { });
        }
        else {
            this.serverPlayerList = roomInfo['playerList'];
            this.selfInfo = msg['selfInfo'];
            this.initGameInfo(msg);
            this.initRoomInfo(roomInfo);
            this.selfSide = this.getLocalPos(this.selfInfo['side']);
        }
    }


    /*******************************服务器位置与客户端位置处理******************************/
    private posServerSelf: number = null;
    private localPosList: Array<number> = null;
    private local2serverPos: Array<number> = [];
    private server2localPos: Array<number> = [];
    public playerCount: number = 0;
    transferServerPos(posServerSelf: number, playerCount: number) {
        this.playerCount = playerCount;
        for (let i = 0; i < this.playerCount; i++) {
            let temp = (i + posServerSelf) % this.playerCount;
            this.server2localPos[i] = temp;
            this.local2serverPos[temp] = i;
        }
    }
    //-获取本地座位号
    getLocalPos(network_seat) {
        return this.local2serverPos[network_seat]
    }
    //-获取网络座位号
    getServerPos(local_seat) {
        return this.server2localPos[local_seat]
    }
    /*******************************服务器位置与客户端位置处理******************************/

    //重置游戏房间
    reset() {
        this.posServerSelf = null;
        //遍历清除每一个座位信息 1.要迭代的对象2.迭代函数
        Tools.inst.each(this.PlayerFrames, function (node) {
            node.clear();
        }, this);
        this.resetGame();
    }
    //清楚座位上UI显示
    resetGame() {
        Tools.inst.each(this.PlayerFrames, function (node) {
            node.resetGame();
        }, this);
    }


    initGameInfo(msg) {
        let selfInfo = msg['selfInfo'];
        this.selfInfo = selfInfo;
        this.posServerSelf = selfInfo["side"];
        this.transferServerPos(this.posServerSelf, msg['roomInfo']['playerCount']);
        this.initMsgListen();
    }

    initRoomInfo(roomInfo) {
        this.initBitmap();
        this._view.setXY(0, 0);
        this.Gold_Layout.setXY(0, 0);
        this.Poker_Layout.setXY(0, 0);
        this._view.getController('c_bar').selectedIndex = 0;
        this.reset();
        let playerList = roomInfo['playerList'];
        Tools.inst.each(playerList, (playerInfo) => {
            if (playerInfo != null) {
                let side = this.getLocalPos(playerInfo['side']);
                let player = this.getPlayer(side);
                player.setSeat(playerInfo, side);
            }
        }, this);
    }


    /************************************************************我是华丽的分割线*************************************************************/
    initMsgListen() {
        //监听协议
        let proto = [ProtoKey666.S_C_JOIN_ROOM, ProtoKey666.S_C_EXIT_ROOM, ProtoKey666.S_C_START_GRABDEALER, ProtoKey666.S_C_GRABDEALER_VOTERESULT, ProtoKey666.S_C_AFTER_START,
        ProtoKey666.S_C_BID, ProtoKey666.S_C_BID_END, ProtoKey666.S_C_AFTERREFRESH, ProtoKey666.S_C_SENDSIGN, ProtoKeyParty.S_C_GOLD_MESSAGE, ProtoKeyParty.S_C_PLAYER_INFO,
        ProtoKey666.S_C_EXIT_ROOM_RESULT, ProtoKeyParty.S_C_IS_GOLD, ProtoKey.S_C_NOTICE, ProtoKey666.S_C_END_GRABDEALER, ProtoKey666.S_C_END_BID, ProtoKey666.S_C_READY_GAMESTART,
        ProtoKey666.S_C_CANCEL_READY,];
        //监听回调函数
        let monitor = [this.onPlayerJoin, this.onPlayerExit, this.startGrabDealer, this.voteResult, this.bet, this.betResult, this.bidEnd, this.afterRefresh, this.sendSign,
        this.onGoldMssage, this.initPlayerGold, this.exitRoomResult, this.initRoomID, this.Notice, this.endGrab, this.endBid, this.gameReady, this.cancleReady];

        for (let i = 0, len = proto.length; i < len; ++i) {
            NetHandlerMgr.netHandler.addMsgListener(proto[i], monitor[i].bind(this));
        }
    }

    gameReady(msgData) {
        this.isOpenMatching(false);
        let leftMS = msgData['leftMS'];
        if (leftMS > 2500 && leftMS < 3000) {
            leftMS = 3000;
        }
        this.cutDownTime(leftMS, 6);
    }

    cancleReady(msgData) {
        let c_showTime = this.showTime.getController('c_showTime');
        c_showTime.selectedIndex = 0;
        Laya.timer.clear(this, this.cutTime);
        this.isOpenMatching(true);
    }

    endGrab(msgData) {
        //-----重置扑克组件
        let name = ['n0', 'n1', 'n2', 'n3', 'n4'];
        for (let i = 0; i < 5; ++i) {
            let pokerCom = this.AreaCom.getChild('pokers_' + i).asCom;
            for (let j = 0, len = name.length; j < len; ++j) {
                let pkCom = pokerCom.getChild(name[j]).asCom;
                let poker = pkCom.getChildAt(0).asLoader;
                this.setPoker(poker, '0000');
            }
        }
    }

    showBetMsg(select) {//0开始下注 1等待下注 2停止下注
        this.clearSign();
        SoundMgrNiu.gameStart();
        let stopBetCom = this._view.getChild('stopBet').asCom;
        let c_betMsg = stopBetCom.getController('c_betMsg');
        let stopBet = stopBetCom.getTransition('stopBet');
        stopBetCom.visible = true;
        c_betMsg.selectedIndex = select;
        stopBet.play();
    }

    endBid(msgData) {//0开始下注 1等待下注 2停止下注
        Laya.timer.clear(this, this.randomJettonLight);
        this.showBetMsg(2);
    }

    Notice(msgData) {
        // let id = msgData['id'];
        // let msg = msgData['txt'];
        // Alert.show(msg).onYes(function () {});
    }

    afterRefresh(msgData) {//(1:抢庄阶段,2:下注阶段,3:结算阶段)
        let leftMS = msgData['leftMS'];
        let stage = msgData['stage'];
        this.isAfterRefresh = true;
        switch (stage) {
            case 1:
                this.cutDownTime(leftMS, 2);
                break;
            case 2:
                this.cutDownTime(leftMS, 3);
                break;
            case 3:
                this.c_showArea.selectedIndex = 1;
                let bidend = msgData['bidend'];
                Laya.timer.once(500, this, this.bidEnd, [bidend], false);
                break;
            default:
                break;
        }

        this.isOpenMatching(false);

        let myside = this.selfInfo['side'];
        this.transferServerPos(myside, this.playerCount);
        this.PlayerFrames.forEach(element => {
            element.resetGame();
            element.clear();
        });

        Tools.inst.each(this.serverPlayerList, (playerInfo) => {
            if (playerInfo != null) {
                let side = this.getLocalPos(playerInfo['side']);
                let player = this.getPlayer(side);
                player.setSeat(playerInfo, side);
            }
        }, this);

        let dealerSide = msgData['dealerSide'];
        if (dealerSide != null && dealerSide >= 0) {
            let localPos = this.getLocalPos(dealerSide);
            let player = this.getPlayer(localPos);
            player.updateBankerState(1);
            this.bankerSide = localPos;
            if (dealerSide == this.selfInfo['side']) {
                this.isZhuang = true;
            }
            if (this.bankerSide != 7) {
                this.swapSeat();
            }
        }

        let BidTransList = msgData['BidTransList'];
        if (stage != 3) {
            for (let i = 0, len = BidTransList.length; i < len; ++i) {
                let value = BidTransList[i];
                let chair = value['chair'];
                let place = value['place'];
                let qty = value['qty'];
                let denomination = value['denomination'];
                let denomination_place = value['denomination_place'];
                let denomination_money = value['denomination_money'];
                denomination = Tools.inst.changeGoldToMoney(denomination);
                denomination_money = Tools.inst.changeGoldToMoney(denomination_money);
                chair = this.getLocalPos(chair);
                if (denomination != '0') {
                    this.flyJetton(place, denomination, qty, chair, denomination_place, denomination_money);//位置 面额 数量 座位
                }
            }
        }

        let bidlist = msgData['bidlist'];
        for (let i = 0, len = bidlist.length; i < len; ++i) {
            let value = bidlist[i];
            let index = i + 1;
            let scoreCom = this.AreaCom.getChild('score_' + index).asCom;
            let playertotalmoney = value['playerTotal'];
            let totalplacemoney = value['placeTotalBid_money'];
            let subtotalmoney = value['subTotal_money'];
            totalplacemoney = Tools.inst.changeGoldToMoney(totalplacemoney);
            subtotalmoney = Tools.inst.changeGoldToMoney(subtotalmoney);
            scoreCom.getChild('totalScore').text = totalplacemoney;
            scoreCom.getChild('selfScore').text = subtotalmoney;
        }
    }
    //-----------初始化玩家金币
    initPlayerGold(msgData) {
        let playerInfo = msgData['playerInfo'];
        for (let i = 0, len = playerInfo.length; i < len; ++i) {
            let info = msgData['playerInfo'][i];
            let side = info['side'];
            let score = info['possessionOfProperty'];
            let localSide = this.getLocalPos(side);
            let player = this.getPlayer(localSide);
            let gold = Tools.inst.changeGoldToMoney(score);
            player.setScore(gold, true);
            player.setScoreNumber(score);
        }
    }

    exitRoomResult(msgData) {
        if (this.isCloseExitRoomResult) return;
        let result: boolean = msgData['result'];
        if (this.isChangeRoom && result) {
            this.resetRoom();
            NetHandlerMgr.netHandler.disconnect();
            this.reset();
            let params = NetHandlerMgr.lastConnectParams;
            NetHandlerMgr.netHandler.connect(params, this.reconnectResult.bind(this));
        } else if (result) {
            this.releaseRes();
            this.destoryAllBtn();
            UserMgr.inst.returnToLobby();
        } else {
            NetHandlerMgr.netHandler.sendData(ProtoKeyParty.C_S_EXIT_ROOM_CONFIRM);
        }
    }

    initRoomID(msgData) {
        let gamenumber: string = msgData['gamenumber'];
        let info = msgData['info'];
        let gold = msgData['gold'];
        this.roomID.text = ExtendMgr.inst.getText4Language("牌局编号：") + gamenumber;
        let roomInfo = this._view.getChild('roomInfo').asLabel;
        gold = Tools.inst.changeGoldToMoney(gold);//----JiaTao 2018-12-6
        let str = ExtendMgr.inst.getText4Language(info) + ' ' + ExtendMgr.inst.getText4Language('底分') + '   ' + gold;
        roomInfo.text = str;
    }

    //游戏期间服务器广播的消息
    onGoldMssage(msgData) {
        let type = msgData['msg_type'];
        let msg = ExtendMgr.inst.getText4Language(msgData['msg']);
        let self = this;
        self.msg.getChild('msg').text = msg;
        if (type == 1 || type == 1002) {
            this.isCloseExitRoomResult = true;
        }
        switch (true) {
            // 代表金币不够退出房间
            case (type == 1002):
                Alert.show(ExtendMgr.inst.getText4Language(msg)).onYes(() => {
                    UserMgr.inst.returnToLobby();
                    //self.onExitRoom();
                });
                break;
            // 当前正在游戏中，是否要退出房间
            case (type == 2):
                Alert.show(ExtendMgr.inst.getText4Language(msg)).onYes(() => {
                    NetHandlerMgr.netHandler.sendExitRoomConfirm();
                });
                break;

            case (type == 1):
            case (type == 5001):
                NetHandlerMgr.netHandler.removeSequenceMsgListener(ProtoKey666.S_C_EXIT_ROOM_RESULT);
                Alert.show(ExtendMgr.inst.getText4Language(msg)).onYes(() => {
                    UserMgr.inst.returnToLobby();
                    //self.onExitRoom();
                });
                break;
            default:
                Alert.show(ExtendMgr.inst.getText4Language(msg)).onYes(() => {
                });
                break;
        }
    }

    //------------------------开始抢庄
    startGrabDealer(msgData) {
        this.isOpenMatching(false);
        if (msgData['isGrab']) return;
        SoundMgrNiu.gameStart();
        this.start_ani.visible = true;
        this.start_ani.getTransitionAt(0).play();
        let waitTime = msgData['waitTime'] - 2000;
        this.cutDownTime(waitTime, 2);//开启抢庄倒计时
        function cb() {
            this.c_bar.selectedIndex = 1;
            SoundMgrNiu.startQiang();
            this.showBar_Q.play();
        }
        Laya.timer.once(400, this, cb.bind(this));
        function sendStrive(btnName: string) {
            NetHandlerMgr.netHandler.sendOnStrive('btn_strive' == btnName);
        }
        this.show_strive.getChild('btn_strive').onClick(this, sendStrive.bind(this), ['btn_strive']);
        this.show_strive.getChild('btn_no_strive').onClick(this, sendStrive.bind(this), ['btn_no_strive']);
    }

    //----------------------抢庄结果
    voteResult(msgData) {
        this.clearSign();
        this.c_bar.selectedIndex = 0;
        //------跑马灯
        let BeDealer = msgData['BeDealer'];
        this.bankerSide = this.getLocalPos(msgData['side']);
        let bankerPlayer = this.getPlayer(this.bankerSide);

        let runResult = function (bankerPlayer, self) {
            bankerPlayer.updateBankerState(1);
            bankerPlayer.setLightMark();
            if (self.bankerSide != 7) {
                self.swapSeat();
            }
        }
        let self = this;
        let run = function (player, k) {
            player.horseRun();
            let len = BeDealer.length - 1;
            if (k == len) {
                runResult(bankerPlayer, self);
            }
        }

        for (let i = 0, len = BeDealer.length; i < len; ++i) {
            let localPos = this.getLocalPos(BeDealer[i]);
            let player = this.getPlayer(localPos);
            Laya.timer.once(300 * i, this, run.bind(this), [player, i], false);
        }

        if (this.selfInfo['side'] == msgData['side']) this.isZhuang = true;

    }

    //庄家换位
    swapSeat() {
        if (this.bankerSide > 7 || this.bankerSide < 0) return;
        let playerSeat = this._view.getChild('seat' + this.bankerSide).asCom;//抢庄成功玩家座位
        if (playerSeat == null) {
            console.log('error11111', playerSeat, this.bankerSide);
            return;//-----白色弹窗
        }
        let x1 = playerSeat.x;
        let y1 = playerSeat.y;
        let bankerSeat = this._view.getChild('seat7').asCom;//庄家座位
        let x2 = bankerSeat.x;
        let y2 = bankerSeat.y;
        let cb = Handler.create(this, function () {
            Laya.Tween.to(bankerSeat, { x: x1, y: y1 }, 500, Laya.Ease.strongInOut, null, null, false);
        });
        Laya.Tween.to(playerSeat, { x: x2, y: y2 }, 500, Laya.Ease.strongInOut, cb, null, false);
    }

    //标记清除
    clearSign() {//c_showSign
        for (let i = 0; i < 8; ++i) {
            let showSignCom = this._view.getChild('showSign_' + i).asCom;
            let c_showSign = showSignCom.getController('c_showSign');
            c_showSign.selectedIndex = this.resetSelectedIndex;
        }
    }
    //----------------------开始下注
    bet(msgData) {
        this.c_showArea.selectedIndex = 1;
        this.bei = msgData['BidQty_money'];
        let leftMS = msgData['leftMS'] - 1000;
        this.cutDownTime(leftMS, 3);//开启下注倒计时
        this.place = 1;
        this.denomination = 1;
        this.quantity = 1;
        if (this.isZhuang) {//庄家不可以下注
            this.showBetMsg(1);
        }
        else {
            SoundMgrNiu.startBidGame();
            this.showBetMsg(0);
            this.c_bar.selectedIndex = 3;
            this.showBar_X.play();
            this.initPlace();
            this.initBetBtn();
        }
    }

    randomJettonLight() {
        let jetton = ['bei_1', 'bei_2', 'bei_3', 'bei_4', 'bei_5'];
        let index = parseInt((Math.random() * 5).toString());
        let jettonLight = this.show_bid.getChild(jetton[index]).asCom.getChild('light').asMovieClip;
        jettonLight.playing = true;
        jettonLight.asMovieClip.setPlaySettings(0, -1, 1, -1, Handler.create(this, function () {
            jettonLight.playing = false;
        }.bind(this)));
    }
    //----------------JiaTao
    initBetBtn() {
        if (this.bei.length == 5) {
            Laya.timer.loop(2000, this, this.randomJettonLight.bind(this), [], false);
            for (let i = 1; i < 6; ++i) {
                let btn_bei = this.show_bid.getChild('bei_' + i).asButton;
                let title_gold = Tools.inst.changeGoldToMoney(this.bei[i - 1]);

                btn_bei.asCom.getChild('title').asLabel.text = title_gold;

                let c_chose = this.show_bid.getController('c_chose');

                let cb = function () {
                    G666.soundMgr.chipClick();
                    let chose = c_chose.selectedIndex;
                    if (chose != 0) {
                        this.denomination = chose;
                    }
                    else {
                        this.denomination = 1;
                    }
                }
                btn_bei.onClick(this, cb.bind(this));
            }
        }
    }

    initPlace() {
        for (let i = 1; i < 5; ++i) {
            let area = this.AreaCom.getChild('area_' + i).asCom;
            if (area == null) continue;
            let place = area.getChild('place').asCom;
            place.enabled = true;
            if (!this.isInitPlace) {
                place.onClick(this, this.handerBid, [i]);
                if (i == 4) {
                    this.isInitPlace = true;
                }
            }
        }
    }

    handerBid(index) {
        let place = [1, 2, 3, 4, 5];
        this.place = place[index - 1];
        NetHandlerMgr.netHandler.sendBid(this.place, this.denomination, this.quantity);//位置 面额 数量
    }


    //金币飞行动作
    flyJetton(place, denomination, quantity, seat, denomination_place, denomination_money) {//位置 面额 数量 座位 颜色 金额
        G666.soundMgr.bets();
        let beginPos: laya.maths.Point;
        if (seat == this.selfSide) {
            let btn = this.show_bid.getChild('bei_' + denomination_place).asButton;
            let screenPos = this.show_bid.localToGlobal(btn.x, btn.y);
            beginPos = this.AreaCom.globalToLocal(screenPos.x, screenPos.y);
            btn.getTransition('t0').play();
        } else {
            //-------头像跳动 左1 3 5 右2 4 6
            let player = this.getPlayer(seat);
            player.playerBet(seat);
            let _seat = this._view.getChild('seat' + seat).asCom;
            let screenPos = this._view.localToGlobal(_seat.x, _seat.y);
            beginPos = this.AreaCom.globalToLocal(screenPos.x, screenPos.y);
        }

        let jetton = fairygui.UIPackage.createObject('G666', 'jetton').asCom;
        jetton.displayObject.cacheAs = this.cashAsMode;//-----JiaTao
        jetton.getChild('title').asLabel.text = denomination_money;
        let c_jetton = jetton.getController('c_jetton');
        c_jetton.selectedIndex = denomination_place;
        jetton.setPivot(0.5, 0.5, true);
        jetton.setXY(beginPos.x, beginPos.y);
        this.Gold_Layout.addChild(jetton);

        let area = this.AreaCom.getChild('area_' + place).asCom;
        let temp = area.actualWidth - jetton.actualWidth * 2;
        let rand_x = Math.random() * temp;
        let rand_y = Math.random() * 80;
        let target_x = area.x + rand_x;
        let target_y = area.y - rand_y;
        Laya.Tween.to(jetton, { x: target_x, y: target_y, rotation: 1080 }, 500, Laya.Ease.strongOut, null, null, false);
    }

    //---------------------下注结果 5 flyJetton(place,denomination,quantity,seat){//位置 面额 数量 座位
    betResult(msgData) {
        let chair = msgData['chair'];
        chair = this.getLocalPos(chair);
        let denomination = msgData['denomination_money'];
        denomination = Tools.inst.changeGoldToMoney(denomination);
        let place = msgData['place'];
        let qty = msgData['qty'];
        let denomination_place = msgData['denomination_place'];
        let denomination_money = msgData['denomination_money'];
        this.getPlayer(chair).updatePlayerScore(denomination_money);//JiaTao 2019-1-8 18:36
        denomination_money = Tools.inst.changeGoldToMoney(denomination_money);
        if (this.isZhuang) {
            this.c_bar.selectedIndex = 0;
        }
        if (denomination != 0 || denomination != '0') {
            this.flyJetton(place, denomination, qty, chair, denomination_place, denomination_money);//位置 面额 数量 座位 颜色
        }
        let totalplacemoney = msgData['placeTotalBid_money'];
        let subtotalmoney = msgData['subTotal_money'];
        totalplacemoney = Tools.inst.changeGoldToMoney(totalplacemoney);//--二进制数据转换
        subtotalmoney = Tools.inst.changeGoldToMoney(subtotalmoney);//---二进制数据转换
        let scoreCom = this.AreaCom.getChild('score_' + place).asCom;
        scoreCom.getChild('totalScore').text = totalplacemoney;
        let selfLocSide = this.getLocalPos(this.selfInfo['side']);
        if (selfLocSide == chair) {
            scoreCom.getChild('selfScore').text = subtotalmoney;
        }
    }

    /**********扑克牌操作开始*************/
    public static _pokerCache = {};
    getPokerUrl(value) {
        let itemName = '';
        if (value == '0000') {//自定义 '0000' 表示背面
            itemName = 'card_backface';
        } else if (value) {
            itemName = 'card_' + value;
        } else {
            itemName = 'card_backface';
        }
        let url = fairygui.UIPackage.getItemURL('G666pokers', itemName);
        return url;
    }
    setCards(tiles) {
        for (let i = 0; i < 5; i++) {
            let pokerCom = this.AreaCom.getChild('pokers_' + i).asCom;
            if (pokerCom == null) continue;
            let outPokers = pokerCom.getChild('pokers').asList;
            outPokers.removeChildrenToPool();
        }
        this.addCards(tiles);
    }
    addCards(tiles) {
        if (tiles == null) return;
        let j = 0;
        for (let i = 0; i < tiles.length; ++i) {
            let value = tiles[i];
            if (i == 5 || i == 10 || i == 15 || i == 20)++j;
            let outPokers = this.AreaCom.getChild('pokers_' + j).asCom.getChild('pokers').asList;
            let pokerComp = outPokers.addItemFromPool().asCom;
            let poker = pokerComp.getChildAt(0);
            this.setPoker(poker.asLoader, value);
            pokerComp.visible = true;
        }
    }

    setPoker(pokerComp, value) {
        let cache = G666Page._pokerCache[value];
        if (cache) return;
        let url = this.getPokerUrl(value);
        if (this.isAfterRefresh) {
            console.log('url', url, 'value', value);
        }
        pokerComp.asLoader.url = url;
    }
    //----------翻转
    addLastPoker(value, place) {
        let pokerCom = this.AreaCom.getChild('pokers_' + place).asCom;
        let poker = pokerCom.getChildAt(4).asCom.getChild('n1').asLoader;
        this.setPoker(poker.asLoader, value);
    }
    //-------------JiaTao
    addCardStageOne(tiles, ind) {
        if (tiles == null || ind == null) return;
        for (let i = 0, len = tiles.length; i < len; ++i) {
            let value = tiles[i];
            let pokerCom = this.AreaCom.getChild('pokers_' + ind).asCom;
            let name = ['n0', 'n1', 'n2', 'n3', 'n4'];
            let poker = pokerCom.getChild(name[i]).asCom.getChildAt(0).asLoader;
            this.setPoker(poker.asLoader, value);
        }
    }

    //主要用来解析结算时后台发过来的 有符号整数 
    analyzeSfixed64(data): any {
        if (data['low'] || data['low'] == '0')
            return data['low'];
        else
            return data;
    }
    //--------------------JiaTao新发牌动作
    push(beginPos, ind, AreaCom) {
        G666.soundMgr.cards_dealing();
        for (let j = 0; j < 5; ++j) {
            let poker = fairygui.UIPackage.createObject('G666', 'poker').asImage;
            if (poker == null || this.Poker_Layout == null) continue;
            poker.setPivot(0.5, 0.5, true);
            this.Poker_Layout.addChild(poker);
            poker.setXY(beginPos.x, beginPos.y);
            let pokersCom = AreaCom.getChild('pokers_' + ind).asCom;
            let screenPos = AreaCom.localToGlobal(pokersCom.x + 30 * j, pokersCom.y);
            let endPos = this.Poker_Layout.globalToLocal(screenPos.x, screenPos.y);
            let delay_time = 40 * j;
            Laya.Tween.to(poker, { x: endPos.x, y: endPos.y }, 300, Laya.Ease.strongOut, null, delay_time, false);
        }
    }
    pushCard() {
        this._view.setXY(0, 0);
        this.Gold_Layout.setXY(0, 0);
        this.Poker_Layout.setXY(0, 0);
        let ani_xp = this._view.getChild('ani_xp').asCom;
        let screenPos_ani = this._view.localToGlobal(ani_xp.x, ani_xp.y);
        let beginPos = this.Poker_Layout.globalToLocal(screenPos_ani.x, screenPos_ani.y);
        for (let i = 0; i < 5; ++i) {
            Laya.timer.once(500 * i, this, this.push.bind(this), [beginPos, i, this.AreaCom], false);
        }
    }
    //--------------------end
    getNiuIndex(placelist) {
        if (placelist == null) return;
        let str = '1,2,3';
        str.split(',');
        let tiles_niu = [];
        for (let i = 0, len = placelist.length; i < len; ++i) {
            tiles_niu[i] = new Array();
            let value = placelist[i];
            let showtiles = value['showtiles'];
            let threetiles = value['threetiles'];
            let tiles_5 = showtiles.split(',');
            let tiles_3 = threetiles.split(',');
            if (threetiles == '') {
                tiles_niu[i].push('00');
                tiles_niu[i].push('00');
            } else {
                for (let j = 0; j < tiles_5.length; ++j) {
                    let tile = tiles_5[j];
                    let isInTile3 = false;
                    for (let z = 0; z < tiles_3.length; ++z) {
                        if (tile == tiles_3[z]) {
                            isInTile3 = true;
                        }
                    }
                    if (!isInTile3) {
                        tiles_niu[i].push(tile);
                    }
                }
            }
        }
        for (let i = 0; i < 5; ++i) {
            this.niuIndex[i] = new Array();
        }
        for (let i = 0; i < placelist.length; ++i) {
            let showtiles = placelist[i]['showtiles'];
            let tiles_5 = showtiles.split(',');
            for (let j = 0; j < tiles_niu[i].length; ++j) {
                let tile = tiles_niu[i][j];
                let isExpect = false;
                if (tile == '00') {
                    //this.niuIndex[i].push(1000);
                } else {
                    for (let z = 0; z < tiles_5.length; ++z) {
                        if (tile == tiles_5[z]) {
                            isExpect = true;
                        }
                        if (isExpect) {
                            isExpect = false;
                            this.niuIndex[i].push(z);
                        }
                    }
                }

            }
        }
    }

    getAllTiles(placelist) {
        if (placelist == null) return;
        let poker = [];
        for (let i = 0, len = placelist.length; i < len; ++i) {
            let tile = placelist[i]['showtiles'].split(',');
            poker = poker.concat(tile);
        }
        return poker;
    }

    getFourTiles(pokers) {
        if (pokers == null) return;
        for (let i = 0, len = pokers.length; i < len; ++i) {
            let value = pokers[i];
            if (i == 4 || i == 9 || i == 14 || i == 19 || i == 24) {
                let temp = '0000';
                this.show_4_tiles.push(temp);
                this.show_5_tiles.push(value);
            }
            else {
                this.show_4_tiles.push(value);
            }
        }
    }
    //------------------------结算
    bidEnd(msgData) {

        let Gold_Layout = this.AreaCom.getChild('Gold_Layout').asCom;
        Gold_Layout.displayObject.cacheAs = this.cashAsMode;

        this.c_bar.selectedIndex = 0;
        let placelist = msgData['placelist'];
        let playerlist = msgData['playerlist'];
        if (placelist == null || playerlist == null) return;
        let pokers = this.getAllTiles(placelist);
        this.AllPokers = pokers;
        this.getFourTiles(pokers);
        this.getstageOneTiles(this.show_4_tiles);
        if (this.isAfterRefresh) {
            console.log('pokers', pokers, 'this.show_4_tiles', this.show_4_tiles, 'this.show_5_tiles', this.show_5_tiles);
        }
        for (let i = 1; i <= 4; ++i) {
            let area = this.AreaCom.getChild('area_' + i).asCom;
            area.getChild('place').enabled = false;
        }

        let cb_3 = function (side) {
            let index: number;
            for (let i = 0, len = playerlist.length; i < len; ++i) {
                if (playerlist[i]['chair'] == side) {
                    let playerbid = playerlist[i];
                    let temp = ['1', '2', '3', '4'];
                    for (let i = 0, len1 = temp.length; i < len1; ++i) {
                        let str_name = 'point' + temp[i] + '_money';
                        let point = playerbid[str_name];
                        point = Tools.inst.changeGoldToMoney(point);
                        let name_child = 't' + temp[i];
                        this.AreaCom.getChild(name_child).text = point;
                    }
                }
            }
        }
        this.getNiuIndex(placelist);
        if (this.isAfterRefresh) {
            let PokersFive = this.getFiveTiles(this.AllPokers);
            //显示牌值
            for (let i = 0, len = PokersFive.length; i < len; ++i) {
                let pokersCom = this.AreaCom.getChild('pokers_' + i).asCom;
                let c_show = pokersCom.getController('c_show');
                c_show.selectedIndex = 1;
                this.addCardStageOne(PokersFive[i], i);
            }
            //显示牛牛字样
            for (let i = 0, len = placelist.length; i < len; ++i) {
                let value = placelist[i];
                let place = value['place'];
                let type = value['bull_type'];
                let point = value['showpoint'];
                this.showNN(place, type, point);
            }
            //顶牛
            for (let i = 0, len1 = this.niuIndex.length; i < len1; ++i) {
                for (let j = 0, len2 = this.niuIndex[i].length; j < len2; ++j) {
                    let index = this.niuIndex[i][j];
                    let pokerCom = this.AreaCom.getChild('pokers_' + i).asCom;
                    if (!pokerCom) continue;
                    let poker = pokerCom.getChildAt(index).asCom;
                    let c1 = poker.getController('c1');
                    c1.selectedIndex = 1;
                }
            }
            this.btn_ready.visible = true;
            //飘分
            for (let i = 0, len = playerlist.length; i < len; ++i) {
                let value = playerlist[i];
                //头像飘分
                let winpoint = value['winpoint_money'];
                let winpoint_str = Tools.inst.changeGoldToMoney(winpoint);
                let index = value['chair'];
                index = this.getLocalPos(index);
                let player = this.getPlayer(index);
                player.scoreBalanceAni(winpoint, winpoint_str);
                //更新玩家分数
                let totalScore = value['totalScore'];
                totalScore = Tools.inst.changeGoldToMoney(totalScore);
                let seat = this._view.getChild('seat' + index).asCom.getChild('seat').asCom;
                let score_label = seat.getChild('score').asLabel;
                score_label.text = totalScore;
            }
        } else {
            Laya.timer.once(800, this, this.pushCard.bind(this), null, false);
            Laya.timer.once(3300, this, this.stageAni.bind(this), [placelist], false);//显示四张牌
            Laya.timer.once(8800, this, this.jettonToPlayer.bind(this), [playerlist], false);
            Laya.timer.once(9500, this, this.updateScore.bind(this), [playerlist], false);
        }
    }

    getstageOneTiles(show_4_tiles) {
        let count = 0;
        for (let i = 0, len = show_4_tiles.length; i < len; ++i) {
            if (i == 0 || i == 5 || i == 10 || i == 15 || i == 20) {
                if (i == 5 || i == 10 || i == 15 || i == 20)++count;
                this.stageOneTiles[count] = new Array();
            }
            this.stageOneTiles[count].push(show_4_tiles[i]);
        }
    }
    stageAni(placelist) {
        this.Poker_Layout.removeChildren();//-----移除Poker_Layout里面的所有扑克
        for (let i = 0; i < 5; ++i) {
            let pokersCom = this.AreaCom.getChild('pokers_' + i).asCom;
            if (pokersCom == null) continue;
            let c_show = pokersCom.getController('c_show');
            c_show.selectedIndex = 1;
            let t_poker = pokersCom.getTransition('t0');
            if (i == 4) {//-------JiaTao
                t_poker.play(Handler.create(this, function (placelist) {
                    if (this.isAfterRefresh) {
                        console.log('end---placelist----', placelist);
                    }
                    this.orderShowAni(placelist);//----翻第一张牌，不要有延迟.
                    this.orderShow(placelist);//---从第二张牌开始做延迟
                }.bind(this), [placelist]));
            } else {
                t_poker.play();
            }
            t_poker.setHook('center', Handler.create(this, function (stageOneTiles, ind) {
                if (this.isAfterRefresh) {
                    console.log('center-----', stageOneTiles, ind);
                }
                this.addCardStageOne(stageOneTiles, ind);
            }.bind(this), [this.stageOneTiles[i], i]));
        }
    }

    orderShowAni(placelist) {
        if (this.isAfterRefresh) {
            console.log('orderShowAni--', placelist);
        }
        this.Poker_Layout.removeChildren();
        let index = [1, 2, 3, 4, 0];
        let ind = index[this.count];
        let name = 'pokers_' + index[this.count].toString();
        let plValue = placelist[ind];
        let type = plValue['bull_type'];
        let point = plValue['showpoint'];
        let ani = this.AreaCom.getChild(name).asCom.getChildAt(4).asCom.getTransition('t0');
        ani.play(Handler.create(this, function () {
            this.showNN(ind, type, point);
            for (let j = 0; j < this.niuIndex[ind].length; ++j) {
                let index = this.niuIndex[ind][j];
                let c1 = this.AreaCom.getChild('pokers_' + ind).asCom.getChildAt(index).asCom.getController('c1');
                c1.selectedIndex = 1;
            }
        }, [ind, type, point]));
        ani.setHook('center', Handler.create(this, function (value, place) {
            this.addLastPoker(value, place);
        }.bind(this), [this.show_5_tiles[ind], ind.toString()]));
        this.count++;
        if (this.count == 5) {
            Laya.timer.clear(this, this.orderShowAni);
            this.count = 0;
            Laya.timer.once(500, this, this.jettonRecycle.bind(this), [], false);//---JiaTao
        }
    }

    orderShow(placelist) {
        if (this.isAfterRefresh) {
            console.log('orderShow---', placelist);
        }
        Laya.timer.loop(750, this, this.orderShowAni, [placelist], false);
    }
    //----------------
    //anchorpoints：贝塞尔基点
    //pointsAmount：生成的点数
    //return 路径点的Array
    CreateBezierPoints(anchorpoints, pointsAmount) {
        let points = [];
        for (let i = 0; i < pointsAmount; i++) {
            let point = this.MultiPointBezier(anchorpoints, i / pointsAmount);
            points.push(point);
        }
        return points;
    }

    MultiPointBezier(points, t) {
        let len = points.length;
        let x = 0, y = 0;
        let erxiangshi = function (start, end) {
            let cs = 1, bcs = 1;
            while (end > 0) {
                cs *= start;
                bcs *= end;
                start--;
                end--;
            }
            return (cs / bcs);
        };
        for (let i = 0; i < len; i++) {
            let point = points[i];
            x += point.x * Math.pow((1 - t), (len - 1 - i)) * Math.pow(t, i) * (erxiangshi(len - 1, i));
            y += point.y * Math.pow((1 - t), (len - 1 - i)) * Math.pow(t, i) * (erxiangshi(len - 1, i));
        }
        return { x: x, y: y };
    }
    //---------JiaTao
    drawCurves(obj) {
        let bankerSeat = this._view.getChild('seat' + this.bankerSide).asCom;
        if (bankerSeat == null) {
            console.log('error222222', bankerSeat, this.bankerSide);
            return;//----白色弹窗
        }
        let screenPos = this._view.localToGlobal(bankerSeat.x, bankerSeat.y);
        let endPos = this.Gold_Layout.globalToLocal(screenPos.x, screenPos.y);
        let p1 = new Laya.Point(obj.x, obj.y);
        let p2 = new Laya.Point(460, 380);
        let p3 = new Laya.Point(endPos.x, endPos.y);
        let count = 0;
        let curvePoint = this.CreateBezierPoints([p1, p2, p3], 50);
        let fn = function (sp, point, ind) {
            sp.setXY(point.x, point.y);
            if (ind == 49) {
                sp.removeFromParent();
            }
        }
        let len = curvePoint.length;
        for (let i = 0; i < curvePoint.length; ++i) {
            Laya.timer.once(10 * i, this, fn.bind(this), [obj, curvePoint[i], i], false);
        }
    }

    getFiveTiles(pokers): any {//Array<string> = [];
        let Pokers = [];
        for (let i = 0; i < 5; ++i) {
            Pokers[i] = new Array();
        }
        if (pokers == null) return;
        let count = 0;
        for (let i = 0; i < pokers.length; ++i) {
            if (i == 4 || i == 9 || i == 14 || i == 19 || i == 24) {
                Pokers[count].push(pokers[i]);
                count++;
            } else {
                Pokers[count].push(pokers[i]);
            }
        }
        return Pokers;
    }
    GRootClick() {//终极保护措施 一旦断线重连出现扑克牌有未翻转过来情况 轻触屏幕任何位置 再次初始化扑克牌
        console.log('9999999999999');
        let PokersFive = this.getFiveTiles(this.AllPokers);
        for (let i = 0, len = PokersFive.length; i < len; ++i) {
            this.addCardStageOne(PokersFive[i], i);
        }
        fairygui.GRoot.inst.offClick(this, this.GRootClick);
    }

    jettonRecycle() {
        /*************触摸保护************/
        if (this.isAfterRefresh) {
            fairygui.GRoot.inst.onClick(this, this.GRootClick);
        }
        //-----------------------------------------
        this.Poker_Layout.removeChildren();
        let bankerSeat = this._view.getChild('seat' + this.bankerSide).asCom;
        if (bankerSeat == null) {
            console.log('error333333', bankerSeat, this.bankerSide);
            return;
        }
        let screenPos = this._view.localToGlobal(bankerSeat.x, bankerSeat.y);
        let endPos = this.Gold_Layout.globalToLocal(screenPos.x, screenPos.y);
        let childNum = this.Gold_Layout.numChildren;
        if (childNum > 0) {
            G666.soundMgr.chipFly();
        }
        for (let i = 0; i < childNum; ++i) {
            let jetton = this.Gold_Layout.getChildAt(i);
            let delay_time = Math.random() * 500;
            Laya.timer.once(delay_time, this, this.drawCurves.bind(this), [jetton], false);
        }
    }
    //---------JiaTao 筹码往其他玩家飞
    jettonToPlayer(playerlist) {
        this.Poker_Layout.removeChildren();
        let isOpen = false;
        for (let i = 0; i < playerlist.length; ++i) {
            let winpoint = playerlist[i]['winpoint_money'];
            let chair = playerlist[i]['chair'];
            chair = this.getLocalPos(chair);
            if (parseFloat(winpoint) > 0 && chair != this.bankerSide) {
                isOpen = true;
                let bankerSeat = this._view.getChild('seat' + this.bankerSide).asCom;
                let seat = this._view.getChild('seat' + chair).asCom;
                if (bankerSeat == null || seat == null) {
                    console.log('error44444', bankerSeat, seat, this.bankerSide);
                    return;//-----白色弹窗
                }

                for (let i = 0; i < 6; ++i) {
                    let jetton = fairygui.UIPackage.createObject('G666', 'jetton').asCom;
                    if (jetton == null) continue;
                    jetton.displayObject.cacheAs = this.cashAsMode;//---JiaTao
                    let c_jetton = jetton.getController('c_jetton');
                    c_jetton.selectedIndex = 1;
                    jetton.setPivot(0.5, 0.5, true);
                    this.Gold_Layout.addChild(jetton);
                    let screenPos_1 = this._view.localToGlobal(bankerSeat.x, bankerSeat.y);
                    let pox = this.Gold_Layout.globalToLocal(screenPos_1.x, screenPos_1.y);
                    jetton.setXY(pox.x, pox.y);
                    let screenPos = this._view.localToGlobal(seat.x, seat.y);
                    let endPos = this.Gold_Layout.globalToLocal(screenPos.x, screenPos.y);
                    let delay_time = 20 * i;
                    Laya.Tween.to(jetton, { x: endPos.x, y: endPos.y }, 800, Laya.Ease.strongOut, Handler.create(this, function (jetton) {
                        this.Gold_Layout.removeChild(jetton);
                    }, [jetton]), delay_time, false);
                }
            }
        }
        if (isOpen) {
            G666.soundMgr.chipFly();
        }
    }

    //更新玩家分数 playerList[i]['winpoint']
    updateScore(playerList) {
        this.Poker_Layout.removeChildren();
        //----JiaTao
        this.AreaCom.displayObject.cacheAs = this.cashAsMode;
        //------
        for (let i = 0, len = playerList.length; i < len; ++i) {
            let value = playerList[i];
            //头像飘分
            let winpoint = value['winpoint_money'];
            let winpoint_str = Tools.inst.changeGoldToMoney(winpoint);
            let index = value['chair'];
            index = this.getLocalPos(index);
            let player = this.getPlayer(index);
            player.scoreBalanceAni(winpoint, winpoint_str);
            //更新玩家分数
            let totalScore = value['totalScore'];
            totalScore = Tools.inst.changeGoldToMoney(totalScore);
            let seat = this._view.getChild('seat' + index).asCom.getChild('seat').asCom;
            let score_label = seat.getChild('score').asLabel;
            score_label.text = totalScore;
        }

        let cb = function () {
            this.showTime.getController('c_showTime').selectedIndex = 0;
            this.btn_ready.visible = true;
        }
        Laya.timer.once(1000, this, cb.bind(this), null, false);

    }

    //显示牛牛或五牛字样 
    private showNN_mingtang_info = [[11, 0, ''], null, null, null, [10, 10, ''], [12, 11, ''], [14, 12, ''], [13, 13, '']];
    showNN(place, type, point) {
        let c_showNN = this.AreaCom.getChild('showNN_' + place).asCom.getController('c_showNN');
        if (type >= 1 && type <= 3) {
            this.showNN_mingtang_info[1] = this.showNN_mingtang_info[2] = this.showNN_mingtang_info[3] = [point, point, ''];
        }
        else if (type < 0 || type > this.showNN_mingtang_info.length) {
            return;
        }
        let info = this.showNN_mingtang_info[type];
        c_showNN.selectedIndex = info[0] as number;//无牛
        SoundMgrNiu.playNiuEffect(info[1], info[2]);
    }

    /**********扑克牌操作结束*************/
    //发送玩家标记
    sendSign(msgData) {
        let PlayerInfo = msgData['PlayerInfo'];
        for (let i = 0, len = PlayerInfo.length; i < len; i++) {
            let value = PlayerInfo[i];
            let sign = value['sign'];
            let account = value['nickname'];
            let sex = value['sex'];
            let pos = value['side'];
            pos = this.getLocalPos(pos);
            if (pos == 0) {
                this.c_bar.selectedIndex = 0;
            }
            let c_showSign = this._view.getChild('showSign_' + pos).asCom.getController('c_showSign');
            if (sign == 1) {//抢庄
                Laya.timer.frameOnce(i * 5, this, function () {
                    SoundMgrNiu.qiang('', sex);//第一个参数什么都不传，为"抢庄"。
                    c_showSign.selectedIndex = 1;
                    if (account == this.selfInfo['account']) {
                        this.showBar_Q.playReverse();
                    }
                }.bind(this));
            }
            else if (sign == 2) {//不抢庄
                Laya.timer.frameOnce(i * 5, this, function () {
                    SoundMgrNiu.qiang(0, sex);
                    c_showSign.selectedIndex = 2;
                    if (account == this.selfInfo['account']) {
                        this.showBar_Q.playReverse();
                    }
                }.bind(this));
            }
            else {//3-满注 4-弃牌 5-观看
                Laya.timer.frameOnce(i * 5, this, function () {
                    c_showSign.selectedIndex = sign;
                }.bind(this));
            }
        }
    }

    //-------------------玩家加入
    onPlayerJoin(msgData) {
        var data = msgData["info"];
        var posServer = data["side"];
        let posLocal = this.getLocalPos(posServer);
        this.getPlayer(posLocal).setSeat(data, posLocal);
        let isHave = false;
        for (let i = 0, len = this.serverPlayerList.length; i < len; ++i) {
            let value = this.serverPlayerList[i];
            let side = value['side'];
            if (posServer == side) {
                isHave = true;
            }
        }
        if (!isHave) {
            this.serverPlayerList.push(data);
        }
    }
    //---------数组移除指定元素
    removeIndex(array, index) {
        let temp = [];
        for (let i = 0, len = array.length; i < len; ++i) {
            if (i == index) continue;
            temp.push(array[i]);
        }
        return temp;
    }
    //------------------玩家退出
    onPlayerExit(msgData) {
        var playerInfo = msgData["info"];
        var posServer = playerInfo["side"];
        let posLocal = this.getLocalPos(posServer);
        this.getPlayer(posLocal).clear();//设置玩家座位不可见
        for (let i = 0, len = this.serverPlayerList.length; i < len; ++i) {
            let side = this.serverPlayerList[i]['side'];
            if (posServer == side) {
                this.serverPlayerList = this.removeIndex(this.serverPlayerList, i);
            }
        }
    }
}