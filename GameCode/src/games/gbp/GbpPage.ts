class GbpPage extends Page {
    static GAME_STATE = {
        WAIT_START: -1, // 创建房间后的第一个状态 ， 第一小局还没开始
        GAME_READY: 0, // 每一小局结束后进入该状态
        PREPARE_GAME: 6, // 准备游戏阶段
        WAIT_STRIVE: 4, // 抢庄
        AFTER_STRIVE: 5, // 抢庄完成做动画阶段
        WAIT_ROLL: 1, // 下注阶段
        GIVE_TILE: 3, // 发牌
        GAMING: 2, //游戏中
        PAUSE: 7 //游戏暂停阶段
    }
    static GAMEPD_TIMER = {
        start: 'start',//匹配
        strive: 'strive',//抢庄
        wager: 'wager',//加倍（下注）
        draw: 'draw',//开牌
    }

    constructor(pkg, comp) {
        super(pkg, comp, UILayer.GAME);
    }
    public gameID: number;
    public selfPlayer: GbpPlayerFrame;
    protected uiPlayerCount: number;
    protected PlayerFrames: Array<GbpPlayerFrame> = [];
    protected robTheVillageBG: fairygui.GComponent;
    protected robTheVillageCtl: fairygui.Controller = null;
    protected gameStateCtl: fairygui.Controller = null;
    protected gameTimer: fairygui.GComponent = null;
    protected winStaus: fairygui.GComponent = null;

    //自动继续 
    protected btnContinue: fairygui.GButton;
    protected autoContTimer: fairygui.GObject;
    protected ctl_autoCont: fairygui.Controller;
    protected autoContTime: number = 3000;
    //

    onCreated(data: any = null) {
        if (!data) return;
        this.btnContinue = this._view.getChild("btn_continue").asButton;
        this.btnContinue.onClick(this, this.onExchangeRoom);
        this.initGameMenu(this.view);
        for (let i = 0; i < this.uiPlayerCount; i++) {
            this.PlayerFrames.push(this.newPlayerFrame(i));
        }
        this.selfPlayer = this.PlayerFrames[0];
        var robTheVillageBG = this.view.getChild('operation').asCom;
        this.robTheVillageBG = robTheVillageBG;
        this.robTheVillageCtl = robTheVillageBG.getController('c1');

        this.gameStateCtl = this.view.getController('State');

        this.gameTimer = this.view.getChild('timer').asCom;
        this.winStaus = this.view.getChild('winStatus').asCom;

        this.reset();
        this.setSelfSeat();
    }

    setSelfSeat() {
        let data = {};
        data['nickname'] = UserMgr.inst._info.name;
        data['headImgUrl'] = UserMgr.inst._info.imgUrl;
        data['coin'] = '';
        let selfPlayer = this.getPlayer(0);
        if (selfPlayer.isInit == false) {
            selfPlayer.setSeat(data);
        }
    }

    showWinStaus(type: number, cb?: () => void) {
        if (type == 3 || type == 4) {
            if (type == 3) {
                this.winStaus.getControllerAt(0).selectedIndex = 1;
            } else if (type == 4) {
                this.winStaus.getControllerAt(0).selectedIndex = 0;
            }
            this.winStaus.visible = true;
            this.winStaus.getTransitionAt(0).play(Handler.create(this, () => {
                if (cb != null) {
                    cb();
                }
            }));
        }
        else {
            if (cb != null) {
                cb();
            }
        }
    }

    hideWinStaus() {
        this.winStaus.visible = false;
    }

    reset() {
        this.posServerSelf = null;
        this.PlayerFrames.forEach(
            (player) => {
                player.clear();
            }
        )
        this.hideWinStaus();
        this.resetGame();
        this.hideTimeTip();
        if (this.view.getChild('startAni') != null) {
            this.view.getChild('startAni').visible = false;
        }
        //自动继续 reset时隐藏继续游戏按钮
        this.btnContinue.visible = false;
        //
        if (this.autoContTimer != null) {
            this.autoContTimer.visible = false;
        }
    }

    resetGame() {
        this.PlayerFrames.forEach(
            (player) => {
                player.resetGame();
            }
        )
    }

    protected newPlayerFrame(side) {
        return new GbpPlayerFrame({
            side: side,
            seat: this.view.getChild('seat' + side).asCom,
            out_pokers: this.view.getChild('out_pokers_' + side).asList,
            out_nnStr: this.view.getChild('out_nn_' + side).asCom,
            out_QStr: this.view.getChild('QStr' + side).asCom,
            out_BStr: this.view.getChild('BStr' + side).asCom,
        })
    }

    protected initGameMenu(view) {
        var uiExitGame = view.getChild('uiExitGame').asCom;
        var btn_exit = uiExitGame.getChild('btn_exit').asButton;
        btn_exit.onClick(this, this.onExitRoom.bind(this));
        var btn_setting = uiExitGame.getChild('btn_setting').asButton;
        btn_setting.onClick(this, () => {
            UIMgr.inst.popup(UI_Setting);
        });
        var btn_history = uiExitGame.getChild('btn_history').asButton;
        btn_history.onClick(this, () => {
            var obj = UIMgr.inst.popup(UI_History) as UI_History;
            obj.refreshGameListInGame(this.gameID);
        });
        var btn_rule = uiExitGame.getChild('btn_rule').asButton;
        btn_rule.onClick(this, () => {
            var rule = UIMgr.inst.popup(UI_Rules) as UI_Rules;
            rule.refreshData('game' + this.gameID);
        });
        var btn_proxy = uiExitGame.getChild('btn_proxy').asButton;
        btn_proxy.visible = false;

        //自动继续 判断ui是否有自动继续按钮和倒计时
        this.ctl_autoCont = uiExitGame.getController('AutoCont');
        this.autoContTimer = view.getChild('autoContTimer');
        if (this.ctl_autoCont != null && this.autoContTimer != null) {
            let btn_autoCont = uiExitGame.getChild('btn_autoCont').asButton;
            btn_autoCont.onClick(this, () => {
                if (this.ctl_autoCont.selectedIndex == 1) {
                    Laya.timer.clear(this, this.onExchangeRoom);
                    this.autoContTimer.visible = false;
                }
                //如果点击自动继续按钮时 继续游戏按钮已经显示就直接继续游戏 （不同游戏按钮可能不同
                else if (this.btnContinue.visible == true) {
                    this.onExchangeRoom();
                }
                this.ctl_autoCont.selectedIndex = this.ctl_autoCont.selectedIndex == 0 ? 1 : 0;
            })
        }
        //
    }

    //自动继续 显示自动继续的倒计时
    showAutoContTimer() {
        if (this.ctl_autoCont != null && this.autoContTimer != null) {
            if (this.ctl_autoCont.selectedIndex == 1) {
                Laya.timer.once(this.autoContTime, this, this.onExchangeRoom);
                this.autoContTimer.visible = true;

                let time = Math.floor(this.autoContTime / 1000);
                let cb = (time: number) => {
                    this.autoContTimer.text = time.toString();
                    if (time > 0) {
                        Laya.timer.once(1000, this, cb, [time - 1]);
                    } else {
                        this.autoContTimer.visible = false;
                    }
                }
                cb(time);
            }
            else {
                this.autoContTimer.visible = false;
            }
        }
    }
    //

    // 退出房间
    onExitRoom() {
        if (NetHandlerMgr.netHandler != null && NetHandlerMgr.netHandler.sendExitRoom != null && NetHandlerMgr.netHandler.valid()) {
            NetHandlerMgr.netHandler.sendExitRoom();
        }
        else {
            UserMgr.inst.returnToLobby();
        }
    }

    setRobTheVillageState(show: boolean, state: number = 0) {
        this.robTheVillageCtl.setSelectedIndex(state);
        this.robTheVillageBG.visible = show;

    }
    onExchangeRoom() {
        if (NetHandlerMgr.netHandler != null && NetHandlerMgr.netHandler.sendExitRoom != null && NetHandlerMgr.netHandler.valid()) {
            this.showRequesting(true);
            NetHandlerMgr.netHandler.sendChangeRoom((msgData) => {
                this.showRequesting(false);
                if (msgData['result']) {
                    if (NetHandlerMgr.netHandler != null) {
                        NetHandlerMgr.netHandler.disconnect();
                    }
                    this.reset();
                    var params = NetHandlerMgr.lastConnectParams;
                    NetHandlerMgr.netHandler.connect(params, this.reconnectResult.bind(this));
                }
            });
        }
    }

    reconnectResult(connected) {
        if (!connected) return;
        var sid = UserMgr.inst.sid;
        NetHandlerMgr.netHandler.enterGame(sid, this.gameID, this.onEnterRoomSuccess.bind(this));
        NetHandlerMgr.inst.initPingListen();
    }

    onEnterRoomSuccess(data) {
        let gameInfo = data['myInfo'];
        //断线重连，请求当前游戏数据
        if (gameInfo['isRefresh'])
            this.refreshInfo();
        else
            this.initGame(gameInfo);
    }

    // 显示可以下注的倍数
    onSelectRate(value) {
        SoundMgr.clickButton();
        NetHandlerMgr.netHandler.sendBid(value, 1);
        this.setRobTheVillageState(false);
    }

    initGame(gameInfo, isrefresh = false) {
        this.reset();
        this.initGameInfo(gameInfo);
        let roomInfo = gameInfo['roomInfo'];
        this.initRoomInfo(roomInfo, isrefresh);
    }


    initRoomInfo(roomInfo, isrefresh = false) {
        var playerList = roomInfo["playerList"];
        Tools.inst.each(playerList, (playerInfo) => {
            if (playerInfo != null) {
                var posServer = playerInfo["side"];
                var posLocal = this.getLocalPos(posServer);
                this.getPlayer(posLocal).setSeat(playerInfo, isrefresh ? '0' : '');
            }
        }, this);
    }

    initGameInfo(gameInfo) {
        var result = gameInfo["result"];
        var reason1 = gameInfo["reason"];
        if (!result) {
            Alert.show(ExtendMgr.inst.getText4Language(reason1)).onYes(() => {
                UserMgr.inst.returnToLobby();
            });
            return;
        }
        let roomInfo = gameInfo['roomInfo'];
        let selfInfo = gameInfo['selfInfo'];
        this.posServerSelf = selfInfo['side'];
        let playerCount = roomInfo['playerCount'];
        this.transferServerPos(this.posServerSelf, playerCount);
        this.initMsgListen();
    }

    onGoldInfo(msgData) {
        let difen = Tools.inst.changeGoldToMoney(msgData['gold']);    //底分
        let info = ExtendMgr.inst.getText4Language(msgData['info']);     //场次信息
        let partyType = msgData['party_type']; //2:金币场 3：竞技场 4: 金币好友房
        let gamenumber = msgData['gamenumber'];
        let tfGameInfo = this._view.getChild("tfGameInfo").asLabel;
        tfGameInfo.text = info + "  " + ExtendMgr.inst.getText4Language("底分：") + difen;
        let tfGameNumInfo = this._view.getChild('tfGameNumInfo').asLabel;
        tfGameNumInfo.text = ExtendMgr.inst.getText4Language("牌局编号：") + gamenumber;
    }


    /**请求断线重连 */
    refreshInfo() {
        NetHandlerMgr.netHandler.refreshData((data) => {
            if (data['result']) {
                let refreshData = data['data'];
                let gameInfo = refreshData['gameInfo'];
                //是否已经初始化过
                if (this.posServerSelf == null)
                    this.initGame(gameInfo, true);
                else
                    this.initRoomInfo(gameInfo['roomInfo'], true);
                this.onRefreshGameData(refreshData);
            }
            else {
                //退出房间
                UserMgr.inst.returnToLobby();
            }
        });
    }

    initMsgListen() {
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_BALANCE, this.onGameEnd.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKey.S_C_JOIN_ROOM, this.onPlayerJoin.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKey.S_C_EXIT_ROOM, this.onPlayerExit.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_EXIT_ROOM_RESULT, this.onGoldExitRoomResult.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_GOLD_MESSAGE, this.onGoldMssage.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_IS_GOLD, this.onGoldInfo.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_PLAYER_INFO, this.onPlayerGoldInfo.bind(this));
    }

    onPlayerGoldInfo(msgData) {
        //console.log(msgData)
        var playerInfo = msgData['playerInfo'];
        for (var i = 0; i < playerInfo.length; i++) {
            var oneData = playerInfo[i];
            var side = this.getLocalPos(oneData["side"]);
            var player = this.getPlayer(side);
            player.setScoreString(oneData["possessionOfProperty"]);
        }
    }

    onGoldExitRoomResult(msgData, finishedListener) {
        if (msgData['result']) {
            UserMgr.inst.returnToLobby();
        } else {
            NetHandlerMgr.netHandler.sendData(ProtoKeyParty.C_S_EXIT_ROOM_CONFIRM);
        }
        if (finishedListener) finishedListener();
    }

    //好友进房
    onPlayerJoin(msgData) {
        var data = msgData["info"];
        var posServer = data["side"];
        var posLocal = this.getLocalPos(posServer);
        this.getPlayer(posLocal).setSeat(data);
    }

    //好友退房
    onPlayerExit(msgData) {
        var playerInfo = msgData["info"];
        var posServer = playerInfo["side"];
        var posLocal = this.getLocalPos(posServer);
        this.getPlayer(posLocal).clear();
    }

    onGoldMssage(msgData) {
        let type = msgData['msg_type'];
        let msg = msgData['msg'];
        let self = this;
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
                NetHandlerMgr.netHandler.removeSequenceMsgListener(ProtoKey.S_C_EXIT_ROOM_RESULT);
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

    onGameEnd(msgData, finishedListener) {
        NetHandlerMgr.netHandler.removeAllMsgListener(ProtoKey.S_C_EXIT_ROOM);
        var setData = msgData["setUserDatas"];
        if (setData != null && setData.length > 0) {
            //然后在玩家头像那里计算分数
            for (var n = 0; n < setData.length; n++) {
                var oneSetData = setData[n];
                var setDataSide = this.getLocalPos(oneSetData["side"]);
                var player = this.getPlayer(setDataSide);
                player.shineStriveBankerMask(oneSetData["score"], (player, score, self, n) => {
                    player.balanceScore(score);
                    player.setScoreAction(score, (self, n) => {
                        if (n == setData.length - 1) {
                            let cb = () => {
                                //自动继续 游戏结束时显示倒计时和继续游戏按钮
                                self.btnContinue.visible = true;
                                self.showAutoContTimer();
                                self.hideTimeTip();
                                if (finishedListener) finishedListener();
                            }
                            if (this.winStaus.visible == true) {
                                this.winStaus.getTransitionAt(1).play(Handler.create(this, () => {
                                    this.winStaus.visible = false;
                                    cb();
                                }));
                            } else {
                                cb();
                            }

                        }
                    }, self, n);

                }, player, oneSetData["score"], this, n);
            }
        }
        else {
            if (finishedListener) finishedListener();
        }
    }

    onRefreshGameData(data) {

    }

    onNetIntoGame(data) {
        this.onEnterRoomSuccess(data);
    }

    getPlayer(side: number) {
        return this.PlayerFrames[side];
    }

    onDispose() {
        Laya.timer.clearAll(this);
        Laya.timer.clearAll(this.gameTimer);
        this.PlayerFrames.forEach((player) => {
            player.onDispose()
        })
    }

    /**
    * @param type 0：游戏即将开始 1：开始抢庄 2：开始下注 3：请亮牌 4：正在匹配 5：开始比牌 6：开始要牌 7：正在开牌
    * @param timer 倒计时时间 null时显示‘...’
    */
    setTimeTip(type: number, time: number) {
        let timeLabel = this.gameTimer.getChild('title');
        this.gameTimer.getController('state').selectedIndex = type;
        Laya.timer.clearAll(this.gameTimer);
        this.gameTimer.visible = true;
        let cb: () => void = null;
        if (time == null) {
            let num = 0;
            let str = ' .';
            timeLabel.text = '';
            cb = () => {
                num++;
                if (num > 3) {
                    num = 0;
                }
                let tempStr = '';
                for (let i = 0; i < num; i++) {
                    tempStr += str;
                }
                timeLabel.text = tempStr;
            }
        } else {
            let num = Math.floor(time / 1000 + 0.5);
            timeLabel.text = ' ' + num.toString();
            let temp: number = 0;
            cb = () => {
                temp++;
                if (temp >= 4) {
                    temp = 0;
                    num--;
                    timeLabel.text = ' ' + num.toString();
                    if (num <= 0) {
                        this.hideTimeTip();
                    }
                }
            }
        }
        Laya.timer.loop(250, this.gameTimer, cb);
    }

    hideTimeTip() {
        Laya.timer.clearAll(this.gameTimer);
        this.gameTimer.visible = false;
    }

    /**********setSeat******************/
    protected posServerSelf: number = null;
    protected localPosList: Array<number> = null;
    protected local2serverPos: Array<number> = [];
    protected server2localPos: Array<number> = [];
    protected playerCount: number = 0;
    protected dealCardList: Array<number> = [];

    transferServerPos(posServerSelf: number, playerCount: number) {
        this.playerCount = playerCount;
        for (let i = 0; i < this.playerCount; i++) {
            let temp = (i + posServerSelf) % this.playerCount;
            this.server2localPos[i] = temp;
            this.local2serverPos[temp] = i;
            this.dealCardList.push(i);
        }
    }
    /**获取本地座位号 */
    getLocalPos(network_seat) {
        return this.local2serverPos[network_seat]
    }
    /**获取网络座位号 */
    getServerPos(local_seat) {
        return this.server2localPos[local_seat]
    }

    /*********************************/
}