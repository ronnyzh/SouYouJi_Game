/*
* name;
*/
//红中麻将
class G445Page extends Page {
    constructor() {
        super("MJ", "GameScene", UILayer.GAME);
        // super("MJ", "MJ445", UILayer.GAME);
    }
    public gameID = 445;

    public isReadyHandFancy = true;

    private PlayerFrames: Array<any> = [];
    private txtLeftTileCount: fairygui.GLabel;
    protected tileTotal: number;
    private tileCount: number;
    protected game_seconds: number = 0;
    protected operatorArea: OperateArea;

    protected playerCount = 4;
    private cbCenter: fairygui.GComponent;
    private timer: fairygui.GComponent;
    private gameTimerStr: fairygui.GLabel = null;
    protected gameSideCtl: fairygui.Controller = null;
    public gameStateCtl: fairygui.Controller = null;
    public gamePayStr: fairygui.GLabel = null;
    private gameInfoStr: fairygui.GLabel = null;
    protected tfTips: fairygui.GLabel = null;
    private roomNumberStr: fairygui.GLabel = null;
    public setBalance: SetBalance = null;
    public btnReady: fairygui.GButton = null;
    protected isTingAction: boolean;
    protected isClickTing: boolean;
    protected tingBtn: fairygui.GButton = null;
    protected tingpanel: fairygui.GComponent = null;
    public tingAutoBtn: fairygui.GButton = null;
    public tingAutoBtnCtl: fairygui.Controller = null;
    public isTingAuto: boolean = false;
    protected tingdatas: Array<string> = [];
    private cardTypenum = 4;
    protected roomNumstr: string = null;
    private Cbalance: fairygui.GComponent = null;
    public handCardsnum: number = 14;
    // protected Readytingdatas: Array<any> = [];
    protected huAl: HuAlgorithm;

    protected ctl_autoCont: fairygui.Controller;
    protected autoContTimer: fairygui.GComponent;
    protected autoContTime: number = 3000;
    newPlayerFrame(data) {
        return new G445PlayerFrame(data);
    }


    onCreated(data: any = null) {
        if (!data) return;
        //加载真正的背景
        var view = this._view;
        // var view = this._view.getChild('basicScene').asCom;
        //  var url = this.Createbgurl();
        // Tools.inst.changeBackground(url, view.getChild('bg').asLoader);
        this.huAl = HuAlgorithm.createHuAlgorithm();
        for (let i = 0; i < 4; i++) {
            this.PlayerFrames.push(this.newPlayerFrame({
                side: i,
                seat: view.getChild('seat' + i).asCom,
                hand_tiles: view.getChild('hand_tiles_' + i).asList,
                out_tiles: view.getChild('out_tiles_' + i).asList,
                meld_tiles: view.getChild('out_meld_' + i).asList,
                actions: view.getChild('actions_' + i).asList,
                hu_tiles: view.getChild('hu_tiles_' + i).asList,
                pin: view.getChild('pin_' + 0).asCom,
                okMark: view.getChild('okMark' + i).asCom,
                hand_tiles_url: fairygui.UIPackage.getItemURL("MJ", "tile" + i),
            }));
        }
        this.playerSelf = this.PlayerFrames[0];

        // var btn_setting = view.getChild('btn_setting').asButton;
        // btn_setting.onClick(this,function(){
        //     NetHandlerMgr.netHandler.sendChangeRoom(function(msgData){
        //         if(msgData['result']){
        //             this.changeRoom();
        //         }
        //     }.bind(this));
        // });

        // var btn_exit = view.getChild('btn_exit').asButton;
        // btn_exit.onClick(this,this.onExitRoom.bind(this));
        this.tingpanel = view.getChild('tingpanel').asCom;
        this.tingpanel.visible = false;
        this.tingBtn = view.getChild('tingbtn').asButton;
        this.tingBtn.visible = false;
        this.tingBtn.onClick(this, this.refreshTingpanel.bind(this), [true]);
        this.tingAutoBtn = view.getChild('tingAutoBtn').asButton;

        this.tingAutoBtnCtl = this.tingAutoBtn.getController('btn');
        this.restTingAuto();
        this.tingAutoBtn.onClick(this, this.TingAuto.bind(this));

        var btnProxy = view.getChild('btnProxy').asButton;
        btnProxy.onClick(this, () => {
            this.sendOnProxy(false);
        });
        // var btn_trusteeship = view.getChild('btn_trusteeship').asButton;
        // btn_trusteeship.onClick(this,function(){
        //      this.sendOnProxy(true);
        // }.bind(this));

        this.txtLeftTileCount = view.getChild('txtLeftTileCount').asLabel;
        this.operatorArea = new OperateArea({
            operatorArea: view.getChild('operatorArea').asList,
            operatorAreaChoice: view.getChild('operatorAreaChoice').asCom
        });

        this.gameStateCtl = view.getController('state');

        this.timer = view.getChild('timer').asCom;
        this.cbCenter = view.getChild('center').asCom;
        this.gameTimerStr = this.cbCenter.getChild('txtLeftTime').asLabel;
        this.gameSideCtl = this.cbCenter.getChild('center').asCom.getController('side');

        this.gamePayStr = view.getChild('txtPay').asLabel;
        this.gameInfoStr = view.getChild('txtInfo').asLabel;
        this.tfTips = this._view.getChild('tfTips').asLabel;
        this.roomNumberStr = view.getChild('room_nuber').asLabel;

        this.Cbalance = view.getChild('cBalance').asCom;
        this.setBalance = new SetBalance(this.Cbalance);
        this.setBalance.setCloseCallback(this.onExitRoom.bind(this));
        this.setBalance.setCloseCallback2(() => {
            this.showRequesting(true);
            NetHandlerMgr.netHandler.sendChangeRoom((msgData) => {
                this.showRequesting(false);
                if (msgData['result']) {
                    this.changeRoom();
                }
            });
        })

        var btnReady = this._view.getChild('btnReady').asButton;
        btnReady.onClick(this, () => {
            btnReady.visible = false;
            NetHandlerMgr.netHandler.sendReadyGame();
        });
        this.btnReady = btnReady;
        this.tingdatas = [];
        // this.showtingpanel();
        /*********************************/
        this.initGameMenu(view);
        /*********************************/

        this.reset();
        this.pageStyleSetting(data);
        this.setSelfseat();
        // this.onEnterRoomSuccess(data);

        // Laya.timer.loop(1000, this, this.updateTimer);
        //  Laya.stage.on(Laya.Event.KEY_DOWN, this, this.onKeyDown);

        // NetHandlerMgr.netHandler.sendIsGold();
    }

    onNetIntoGame(data) {
        this.onEnterRoomSuccess(data);
        // Laya.timer.loop(1000, this, this.updateTimer);
        // Laya.stage.on(Laya.Event.KEY_DOWN, this, this.onKeyDown);

        NetHandlerMgr.netHandler.sendIsGold();
    }
    setSelfseat() {
        let data = {}
        data['nickname'] = UserMgr.inst._info.name;
        data['headImgUrl'] = UserMgr.inst._info.imgUrl;
        data['coin'] = '';
        this.playerSelf.setSeat(data);


    }

    Createbgurl() {
        return ResourceMgr.RES_PATH + 'bg/main_bg0.jpg';
    }
    initGameMenu(view) {
        var uiExitGame = view.getChild('uiExitGame').asCom;
        uiExitGame.getController('gametype').selectedIndex = 1;
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
        btn_proxy.onClick(this, () => {
            this.sendOnProxy(true);
        });
        //自动继续 判断ui是否有自动继续按钮和倒计时
        this.ctl_autoCont = uiExitGame.getController('AutoCont');
        this.autoContTimer = this.Cbalance.getChild("cBalance").asCom.getChild('autoContTimer').asCom;
        if (this.ctl_autoCont != null && this.autoContTimer != null) {
            let btn_autoCont = uiExitGame.getChild('btn_autoCont').asButton;
            btn_autoCont.onClick(this, () => {
                if (this.ctl_autoCont.selectedIndex == 1) {
                    Laya.timer.clear(this, this.onExchangeRoom);

                    // this.showRequesting(true);
                    // NetHandlerMgr.netHandler.sendChangeRoom((msgData) => {
                    //     this.showRequesting(false);
                    //     if (msgData['result']) {
                    //         this.changeRoom();
                    //     }
                    // });
                    this.autoContTimer.visible = false;

                }
                else if (this.gameStateCtl.selectedIndex == 4) {

                    this.onExchangeRoom();
                }
                this.ctl_autoCont.selectedIndex = this.ctl_autoCont.selectedIndex == 0 ? 1 : 0;
            })
        }
    }
    onExchangeRoom() {
        if (NetHandlerMgr.netHandler != null && NetHandlerMgr.netHandler.sendExitRoom != null && NetHandlerMgr.netHandler.valid()) {
            this.showRequesting(true);
            NetHandlerMgr.netHandler.sendChangeRoom((msgData) => {
                this.showRequesting(false);
                if (msgData['result']) {
                    this.firstState();
                    this.changeRoom();
                }
            });
        }
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
    pageStyleSetting(data) {
        //console.log('pageStyleSetting 445')
    }

    sendOnProxy(on = false) {
        NetHandlerMgr.netHandler.sendOnProxy(on ? 1 : 0);
    }

    setGhostTile(tileID: string) {
        MahjongMgr.inst.setGhostTile(tileID);
        var ghost = this._view.getChild('ghost').asCom;
        if (tileID)
            MahjongMgr.inst.setWholeTile(ghost, tileID);
        ghost.visible = !!tileID;

        /**预听牌设置鬼牌 */
        if (tileID != null && tileID != '') {
            let ghostList = tileID.split(',');
            this.huAl.setGhostList(ghostList);
        } else {
            this.huAl.setGhostList([]);
        }
    }

    updatePlayerTurn(posServer, time = 15) {
        var posLocal = this.getLocalPos(posServer);
        // this.turnIndicator.indicate(posLocal, time);
        // this.tileTouch.setDiscardable(posLocal == 0);
        // this.playerInfoHandler.updatePlayerTurnBySide(posLocal);

        let num = posLocal - this.getLocalPos(this.posDealerServer);
        if (num < 0)
            num += 4;
        else if (num >= 4)
            num -= 4;
        if (posLocal == 0) {
            this.getPlayer(0).setselfDrag();  //手牌可拖拽
        }
        else {
            this.getPlayer(0).setselfNotDrag();
        }
        this.gameSideCtl.setSelectedIndex(num);
        MahjongMgr.inst.refreshPlayerTurn(posLocal);

        this.game_seconds = time;
        this.setTimer(this.game_seconds);
    }

    setgamestateTimer(stateindex, time: number = null) {
        Laya.timer.clear(this, this.UpdatePoint);
        this.timer.visible = true;
        let stage = this.timer.getController('state');
        stage.selectedIndex = stateindex;
        let text = this.timer.getChild('title');
        if (time == null) {
            text.text = "";
            this.numpoint = 0;
            Laya.timer.loop(250, this, this.UpdatePoint);
        }
        else {
            //Laya.timer.clear(this, Pointcb);
            let num = Tools.inst.timeinteger(time)
            text.text = " " + num.toString();
            let cb = () => {
                num--;
                text.text = " " + num.toString();
                if (num <= 0) {
                    Laya.timer.clear(this, cb);
                    this.timer.visible = false;
                }
            }
            Laya.timer.loop(1000, this, cb);
        }
    }
    private numpoint = 0;
    UpdatePoint() {
        this.numpoint++;
        let text = this.timer.getChild('title');
        text.text = text.text + " .";
        if (this.numpoint > 3) {
            text.text = "";
            this.numpoint = 0;
        }
    }
    setTimer(seconds: number) {
        Laya.timer.clear(this, this.updateTimer);
        if (!seconds) return;
        this.game_seconds = seconds;
        this.gameTimerStr.visible = seconds > 0;
        this.gameTimerStr.text = seconds.toString();
        Laya.timer.loop(1000, this, this.updateTimer);
    }
    updateTimer() {

        this.gameTimerStr.visible = this.game_seconds > 0;
        this.gameTimerStr.text = this.game_seconds.toString();
        if (this.game_seconds < 0) {
            // Laya.timer.clear(this, this.updateTimer);
            this.clearTimer();
        }
        this.game_seconds--;
    }
    clearTimer() {
        this.gameTimerStr.visible = false;
        Laya.timer.clear(this, this.updateTimer);
    }

    changeRoom() {
        if (NetHandlerMgr.netHandler != null) {
            NetHandlerMgr.netHandler.disconnect();
        }
        this.reset();
        var params = NetHandlerMgr.lastConnectParams;
        NetHandlerMgr.netHandler.connect(params, this.reconnectResult.bind(this));
    }

    reconnectResult(connected) {
        if (!connected) return;
        var sid = UserMgr.inst.sid;
        NetHandlerMgr.netHandler.enterGame(sid, this.gameID, this.onEnterRoomSuccess.bind(this));
        NetHandlerMgr.inst.initPingListen();
    }

    getPlayer(side: number, server: boolean = false) {
        if (server) side = this.getLocalPos(side);
        return this.PlayerFrames[side];
    }

    onEnterRoomSuccess(data) {
        //console.log('onEnterRoomSuccess ok',data);
        var gameInfo = data["myInfo"];
        //断线重连，请求当前游戏数据
        if (gameInfo["isRefresh"])
            this.refreshInfo();
        else
            this.initGame(gameInfo);
    }

    refreshInfo() {
        NetHandlerMgr.netHandler.refreshData((data) => {
            if (data["result"]) {
                // WaitingView.hide();
                var refreshData = data["data"];
                var gameInfo = refreshData["gameInfo"];
                //是否已经初始化过
                if (this.posServerSelf == null)
                    this.initGame(gameInfo);
                else
                    this.initRoomInfo(gameInfo["roomInfo"]);

                this.onRefreshGameData(refreshData);
            }
            else {
                //退出房间
            }
        });
        // WaitingView.show(gb.getText("refresh_roomInfo_tips"));
    }

    onRefreshGameData(msgData) {

        var stage = msgData["stage"];

        this.setReadyEvent(stage <= 0);

        if (stage == GAME_STAGE.WAIT_START)
            return;

        switch (stage) {
            case GAME_STAGE.GAME_READY:
                this.refreshInGameEnd(msgData);
                break;

            case GAME_STAGE.WAIT_ROLL:
                this.refreshInWaitRoll(msgData);
                break;

            case GAME_STAGE.GAMING:
                this.refreshInGame(msgData);
                break;
        }
    }

    refreshLeftTileCount(num, reduce: boolean = false) {
        if (reduce) {
            num = this.tileCount - parseInt(num || 1);
        }
        this.tileCount = parseInt(num);
        this.txtLeftTileCount.text = this.tileCount + '';
    }

    //在回合间段刷新回来
    refreshInGameEnd(data) {
        //暂时没有需要恢复的数据
        // this.refreshInWaitRoll(data);
        // var currentSide = data["currentSide"];
        // //判断是否已出牌
        // var outTile = data["lastDiscard"]
        // //设置各边玩家数据
        // for (var i = 0; i < this.playerCount; i++) {
        //     var onePlayerData = data["playerDatas"][i];
        //     var playerSide = onePlayerData["side"];

        //     if (playerSide == currentSide) {
        //         onePlayerData["outTile"] = outTile;
        //         onePlayerData["turn"] = (outTile == "");
        //     }
        //     else {
        //         onePlayerData["outTile"] = "";
        //         onePlayerData["turn"] = false;
        //     }
        //  this.refreshPlayerArea(onePlayerData);
        //显示玩家在线状态
        // var isOnline = onePlayerData["isOnline"];
        // var posLocal = this.getLocalPos(playerSide);
        //this.playerInfoHandler.updateOnlineStateBySide(posLocal, {"isOnline" : isOnline});
        //}
    }

    //在摇色阶段刷新回来
    refreshInWaitRoll(data) {
        //剩余牌张数显示
        this.refreshLeftTileCount(data["leftTileCount"]);

        //设置庄家显示
        this.posDealerServer = data["dealerSide"];
        this.rollCircle(this.getLocalPos(data["dealerSide"]));
        // this.playerInfoHandler.showBankerBySide(mb.getLocalPos(data["dealerSide"]), data["dealerCount"]);        
        this.getPlayer(this.posDealerServer, true).updateBankerState(true);
    }

    rollCircle(bankerSide) {
        //  var imgCircle: fairygui.GComponent = this.cbCenter.getChild('imgCircle').asCom;
        // imgCircle.rotation = (1 - bankerSide) * 90;
        this.cbCenter.getChild('center').rotation = (4 - bankerSide) * 90;
    }

    //在游戏段刷新回来
    refreshInGame(data) {
        this.refreshInWaitRoll(data);

        var currentSide = data["currentSide"];
        this.lastDrawPlayer = this.getPlayer(currentSide, true);
        let num = parseInt((data["Countdown"] / 1000).toString());
        this.updatePlayerTurn(currentSide, num);

        this.setGhostTile(data["ghost"]);

        //判断是否已出牌
        var outTile = data["lastDiscard"];

        //玩家吃碰杠胡按钮显示
        var allowActionsData = data["allowAction"];
        if (allowActionsData != null) {
            //玩家有吃碰杠选择时不能出牌
            // this.tileTouch.setDiscardable(false);

            this.onShowActionOption(allowActionsData);
        }

        //设置各边玩家数据
        for (var i = 0; i < this.playerCount; i++) {
            var onePlayerData = data["playerDatas"][i];
            var playerSide = onePlayerData["side"];

            if (playerSide == currentSide) {
                onePlayerData["outTile"] = outTile;
                onePlayerData["turn"] = (outTile == "");
            }
            else {
                onePlayerData["outTile"] = "";
                onePlayerData["turn"] = false;
            }

            this.refreshPlayerArea(onePlayerData);

            //显示玩家在线状态
            var isOnline = onePlayerData["isOnline"];
            var posLocal = this.getLocalPos(playerSide);
            //this.playerInfoHandler.updateOnlineStateBySide(posLocal, {"isOnline" : isOnline});
        }
    }

    refreshPlayerArea(data) {
        var side = data["side"];
        var actionedTiles = data["actionedTiles"];

        var meldData = [];
        var chowTiles = actionedTiles[1]["tiles"];
        var pongTiles = actionedTiles[2]["tiles"];
        var kongTiles = actionedTiles[3]["tiles"];
        var concealedKongTiles = actionedTiles[4]["tiles"];
        var meldTiles = pongTiles.concat(kongTiles, concealedKongTiles);
        for (var i = 0; i < meldTiles.length; i++) {
            var oneMeldStrings = meldTiles[i].split(";");
            var oneMeldSide = parseInt(oneMeldStrings[0]);
            var oneMeldTiles = oneMeldStrings[1];
            var serialNumber = parseInt(oneMeldStrings[2]);
            var oneMeldData = {
                "list": (oneMeldTiles.split(",").sort()),
                "isShowEffect": false,
                "from": this.getLocalPos(oneMeldSide)
            };
            //meldData[serialNumber] = oneMeldData;
            meldData.push(oneMeldData);
        }
        let chowData = [];
        for (let i = 0; i < chowTiles.length; i++) {
            let oneChowStrings = chowTiles[i].split(';');
            let oneChowSide = parseInt(oneChowStrings[0]);
            let oneChowTiles = oneChowStrings[1];
            let serialNumber = parseInt(oneChowStrings[2]);
            let oneChowData = {
                "list": (oneChowTiles.split(",").sort()),
                "isShowEffect": false,
                "from": this.getLocalPos(oneChowSide)
            };
            chowData.push(oneChowData);
        }

        var areaData = {
            "outTile": (data["outTile"]),
            "discardTiles": (actionedTiles[0]["tiles"]),
            "handTiles": (actionedTiles[6]["tiles"]),
            "turn": data["turn"],
            "meldData": meldData,
            "exhitbitTiles": (actionedTiles[5]["tiles"]),
            'chowData': chowData
        };

        var player = this.getPlayer(side, true);
        try {
            player.setContent(areaData);
        } catch (e) {
            console.log(e)
        }
        /**预听牌  start*/
        if (side == 0 && data["turn"]) {
            let handCardIds = actionedTiles[6]["tiles"].concat();
            this.ready_hand_fancy(handCardIds);
        }
        /**预听牌  end*/

    }

    ready_hand_fancy(handCardIds?: string[]) {
        //预听牌
        if (this.isReadyHandFancy) {
            let selfPlayer = this.getPlayer(0);
            if (handCardIds == null) {
                handCardIds = selfPlayer.tilesDataHand.concat();
            }
            let tingKeyList: string[] = [];
            let ReadyHandFancyMap = {};
            for (let value of handCardIds) {
                if (ReadyHandFancyMap[value] == null) {
                    let tingList = this.huAl.getReadyHandTiles(value, handCardIds);
                    if (tingList != null && tingList.length > 0) {
                        ReadyHandFancyMap[value] = tingList;
                        tingKeyList.push(value);
                    }
                }
            }
            this.tingBtn.visible = false;
            if (tingKeyList.length > 0) {
                Laya.timer.frameOnce(1, this, () => {
                    this.tryMarkTiles(tingKeyList.join(','), true);
                });
                this.showtingpanel(tingKeyList, true);
                if (selfPlayer.pitchUpCard != null) {
                    let selfPitchUpId = selfPlayer.pitchUpCard.data.toString();
                    if (ReadyHandFancyMap[selfPitchUpId] != null) {
                        this.showtingpanel(ReadyHandFancyMap[selfPitchUpId]);
                    }
                }
                selfPlayer.ReadyHandFancyEvt = (value: string, state: boolean) => {
                    if (state == true) {
                        if (ReadyHandFancyMap[value] != null) {
                            this.showtingpanel(ReadyHandFancyMap[value]);
                        }
                        else {
                            this.tingpanel.visible = false;
                            this.tingBtn.visible = false;
                        }
                    }
                };
            } else {
                this.tingpanel.visible = false;
            }
        }
    }


    initGame(gameInfo) {
        this.initGameInfo(gameInfo);

        var roomInfo = gameInfo["roomInfo"];
        this.initRoomInfo(roomInfo);
        this.isTingAction = false;
        this.isClickTing = false;
        //  this.markTiles = [];
    }
    posServerSelf = null;
    posLocalList = [0, 1, 2, 3];
    getLocalPos(posServer): number {
        return MahjongMgr.inst.getLocalPos(posServer);
    }
    initGameInfo(gameInfo) {
        var roomInfo = gameInfo["roomInfo"];
        var playerList = roomInfo["playerList"];
        var roomId = roomInfo["roomId"];
        var roomSetting = roomInfo["roomSetting"];
        var roomName = roomInfo["roomName"];

        this.playerCount = roomInfo["playerCount"] || 4;

        var selfInfo = gameInfo["selfInfo"];
        this.posServerSelf = selfInfo["side"];

        MahjongMgr.inst.transferServerPos(this.posServerSelf);

        //剩余牌张数显示
        this.tileTotal = roomInfo["tileCount"];
        this.refreshLeftTileCount(this.tileTotal);

        this.initMsgListen();
    }

    reset() {
        this.posServerSelf = null;
        this.isTingAction = false;
        this.isClickTing = false;
        Tools.inst.each(this.PlayerFrames, (node) => {
            node.clear();
        }, this);

        var ghost = this._view.getChild('ghost').asCom;
        ghost.visible = false;

        this.huAl.clearMap();
        this.resetGame();
        this.clearTimer();
    }

    resetGame() {
        this.operatorArea.reset();

        Tools.inst.each(this.PlayerFrames, (node) => {
            node.resetGame();
        }, this);
        this.huAl.clearMap();
        var stateCtl = this._view.getController('proxy');
        stateCtl.setSelectedIndex(0);

        this.btnReady.visible = false;
        this.tingdatas = [];
        this.tingpanel.visible = false;
        this.tingBtn.visible = false;
        this.tfTips.visible = false;
        this.tingAutoBtn.visible = false;
        this.tingAutoBtn.enabled = true;
        this.isTingAuto = false;
        this.tingAutoBtnCtl.selectedIndex = 0;
        this.timer.visible = false;
    }

    initRoomInfo(roomInfo) {
        //console.log('initRoomInfo',roomInfo)

        var playerList = roomInfo["playerList"];
        this.reset();
        if (playerList.length < this.playerCount)
            this.setgamestateTimer(4);
        Tools.inst.each(playerList, (playerInfo) => {
            if (playerInfo != null) {
                var posServer = playerInfo["side"];
                var posLocal = this.getLocalPos(posServer);
                this.getPlayer(posLocal).setSeat(playerInfo);
            }
        }, this);
    }

    initMsgListen() {
        // 串行消息处理
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_SET_START, this.onSetStart.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_BALANCE, this.onGameEnd.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_DEAL_TILES, this.onDealTiles.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_DRAW_TILES, this.onPlayerDraw.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_ROLL_DICE, this.onRollDice.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_DISCARD, this.onPlayerDiscard.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_DO_ACTION, this.onPlayerAction.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_ALLOW_ACTION, this.onShowActionOption.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_READY_HAND, this.onReadyHand.bind(this));

        // //正常消息处理
        NetHandlerMgr.netHandler.addMsgListener(ProtoKey.S_C_JOIN_ROOM, this.onPlayerJoin.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKey.S_C_EXIT_ROOM, this.onPlayerExit.bind(this));
        // NetHandlerMgr.netHandler.addMsgListener(S_C_ONLINE_STATE, this.onUpdateOnlineState.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKey.S_C_NOTICE, this.onNotice.bind(this));

        //金币场特有
        // NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_PAY, this.onPay.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_WATCHER_INFO, this.onWatcherInfo.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_GOLD_MESSAGE, this.onGoldMssage.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_IS_GOLD, this.onGoldInfo.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_PLAYER_INFO, this.onPlayerGoldInfo.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_EXIT_ROOM_RESULT, this.onGoldExitRoomResult.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKeyMJG.S_C_PROXY, this.onProxy.bind(this));

        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyMJG.S_C_PLAYERREADYRESULT, this.onPlayerReadyResult.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyMJG.S_C_READY_GAMESTART, this.onShowMsg.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyMJG.S_C_CANCEL_READY, this.onHideMsg.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKeyMJG.S_C_GOLDUPDATE, this.onGoldUpdate.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKeyMJG.S_C_NOGOLD, this.onNoGold.bind(this));

    }

    onShowMsg(msgData, finishedListener) {
        //console.log(msgData); 
        this.setgamestateTimer(0, msgData['leftMS']);
        if (finishedListener)
            finishedListener();
    }
    onHideMsg(msgData, finishedListener) {
        this.timer.visible = false;
        this.setgamestateTimer(4)
        if (finishedListener)
            finishedListener();
    }
    isAutoReady = true;
    setReadyEvent(show) {
        if (this.isAutoReady) {
            if (show) {
                NetHandlerMgr.netHandler.sendReadyGame();
            }
        }
        else {
            this.btnReady.visible = show;
        }
    }

    onPlayerReadyResult(msgData, finishedListener) {
        var PlayerResult = msgData['PlayerResult'];
        for (var i = 0; i < PlayerResult.length; i++) {
            var data = PlayerResult[i];
            this.getPlayer(data['side'], true).setOkMark(data['result']);
            if (this.getLocalPos(data['side']) == 0) {
                this.setReadyEvent(!data['result']);
            }
        }
        if (finishedListener) finishedListener();
    }

    onProxy(msgData) {
        var data = msgData["data"];
        var stateCtl = this._view.getController('proxy');
        for (var i = 0; i < data.length; i++) {
            var side = this.getLocalPos(data[i]["side"]);
            if (side != 0) continue;
            var isproxy = data[i]["isproxy"];
            stateCtl.setSelectedIndex(isproxy ? 1 : 0);
            if (isproxy && this.tingAutoBtn.visible) {
                this.isTingAuto = false;
                this.tingAutoBtnCtl.selectedIndex = 0;
                this.tingAutoBtn.enabled = false;
            }
            else if (!isproxy && this.tingAutoBtn.visible) {
                this.isTingAuto = false;
                this.tingAutoBtn.enabled = true;
            }
        }
    }

    posDealerServer = null;
    onSetStart(msgData, finishedListener) {
        //console.log(msgData)

        this.resetGame();

        //显示牌的剩余数量
        this.refreshLeftTileCount(this.tileTotal);

        this.gameStateCtl.setSelectedIndex(1);
        this._view.getChild('gamestart').asCom.getTransitionAt(0).play();

        this.posDealerServer = msgData["dealer"];
        this.rollCircle(this.getLocalPos(this.posDealerServer));

        SoundMgr.rollDice();
        this.timer.visible = false;

        Tools.inst.setTimeout(() => {
            if (finishedListener) finishedListener();
            this.getPlayer(this.posDealerServer, true).updateBankerState(true);
            this.firstState();
        }, 1000);
    }

    firstState() {
        this.gameStateCtl.setSelectedIndex(0);
    }

    onPlayerJoin(msgData) {
        //console.log(msgData)
        var data = msgData["info"];
        var posServer = data["side"];
        var posLocal = this.getLocalPos(posServer);
        this.getPlayer(posLocal).setSeat(data);
    }

    onPlayerExit(msgData) {
        //console.log(msgData)
        var playerInfo = msgData["info"];
        var posServer = playerInfo["side"];
        var posLocal = this.getLocalPos(posServer);
        this.getPlayer(posLocal).clear();
    }

    onUpdateOnlineState(msgData) {
        //console.log(msgData)
    }

    onNotice(msgData) {
        //console.log(msgData)        
        /*var addData = {
            "content": msgData["txt"],
            "repeatTimes": msgData["repeatTimes"],
            "repeatInterval": msgData["repeatInterval"]
        };
        NoticeView.addNotices([addData]);*/
        NoticeView.show(ExtendMgr.inst.getText4Language(msgData["txt"]));
    }

    onPay(msgData) {
        //console.log(msgData)

        var cost = msgData['coin'];
        this.gamePayStr.text = '本场游戏每一局需要扣除 ' + cost + ' 金币';
        this.gamePayStr.visible = true;
        Tools.inst.setTimeout(() => {
            this.gamePayStr.visible = false;
        }, 1000);

        var setData = msgData['sides'];
        for (var n = 0; n < setData.length; n++) {
            var side = setData[n];
            var player = this.getPlayer(side, true);
            player.balanceScore(-cost);
        }
    }
    onWatcherInfo(msgData) {
        //console.log(msgData)
    }

    onGoldMssage(msgData) {
        let type = msgData['msg_type'];
        let msg = msgData['msg'];
        let self = this;
        switch (true) {

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
            //代表金币不够 取消换房 退出房间
            case (type == 1):
            //关服
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

    onGoldInfo(msgData) {
        //console.log(msgData)                        
        var difen = msgData['gold'];    //底分
        var info = ExtendMgr.inst.getText4Language(msgData['info']);     //场次信息
        var partyType = msgData['party_type']; //2:金币场 3：竞技场
        var gamenumber = msgData['gamenumber'] || "no data";     //牌局编号

        this.gameInfoStr.text = info + " " + ExtendMgr.inst.getText4Language("底分：") + Tools.inst.changeGoldToMoney(difen);
        this.roomNumberStr.text = ExtendMgr.inst.getText4Language("牌局编号：") + gamenumber + "\n" + info + ' ' + ExtendMgr.inst.getText4Language("底分：") + Tools.inst.changeGoldToMoney(difen);
        this.roomNumstr = ExtendMgr.inst.getText4Language("牌局编号：") + gamenumber;
    }
    onGetMessage(msgData) {
        //console.log(msgData)
    }
    onShowReadyOk(msgData) {
        //console.log(msgData)
    }

    onDealTiles(msgData, finishedListener) {
        // console.log(msgData)
        var tileIdList = msgData["tiles"];
        this.setGhostTile(msgData["specialTile"]);

        var playerTileDataList = [];
        for (var posServer = 0; posServer < this.playerCount; ++posServer) {
            if (0 == this.getLocalPos(posServer))
                playerTileDataList[posServer] = tileIdList;
            else
                playerTileDataList[posServer] = new Array(tileIdList.length);
            // console.log('onDealTiles : ',playerTileDataList[posServer])
            this.getPlayer(posServer, true).addHandTiles(playerTileDataList[posServer], true);
            this.refreshLeftTileCount(tileIdList.length, true);
        }
        if (finishedListener) finishedListener();
    }

    protected isFirstDraw = true;
    onPlayerDraw(msgData, finishedListener) {
        // console.log(msgData, "===========S_C_DRAW_TILES");

        var drawDataList = msgData["tiles"];
        var posDrawServer = msgData["side"];
        var player = this.getPlayer(posDrawServer, true);
        this.lastDrawPlayer = player;
        var drawData = drawDataList.shift();
        var inIDList = drawData["inTiles"] || [];
        var outIDList = drawData["outTiles"] || [];
        var inList = [];
        Tools.inst.each(inIDList, (id) => {
            inList.push(id);
        }, this);
        this.refreshLeftTileCount(inList.length, true);

        player.drawHandTile(inList);
        SoundMgr.drawTile();
        this.updatePlayerTurn(posDrawServer);

        if (this.isFirstDraw && this.getLocalPos(posDrawServer) == 0) {
            this.tfTips.text = ExtendMgr.inst.getText4Language("双击或者拖动即可出牌");
            this.tfTips.visible = this.isFirstDraw;

            // console.log('this.isFirstDraw',this.isFirstDraw)
        }
        //预听牌
        if (this.getLocalPos(posDrawServer) == 0) {
            this.ready_hand_fancy();            //预听牌
            //是否自动出牌
            if (this.tingAutoBtn.visible && this.tingAutoBtnCtl.selectedIndex == 1)
                this.AutoSendcardCheck(180);
        }
        if (finishedListener) finishedListener();
    }

    onRollDice(msgData, finishedListener) {
        //console.log(msgData)
        // SoundMgr.rollDice();
        if (finishedListener) finishedListener();
    }

    onPlayerDiscard(msgData, finishedListener) {
        //出牌取消预听牌事件
        this.playerSelf.ReadyHandFancyEvt = null;
        //隐藏预听牌面板
        this.tingpanel.visible = false;
        Laya.timer.frameOnce(1, this, () => {
            //手牌颜色恢复
            this.playerSelf.resetcardcolor();
        });
        if (msgData["tile"]) {
            var serverSide = msgData["side"];
            var player = this.getPlayer(serverSide, true);
            var tileData = (msgData["tile"]);
            player.discard(tileData);
            if (this.isFirstDraw && this.getLocalPos(serverSide) == 0) {
                this.isFirstDraw = false;
                this.tfTips.text = ExtendMgr.inst.getText4Language("双击或者拖动即可出牌");
                this.tfTips.visible = this.isFirstDraw;
                // console.log('this.isFirstDraw',this.isFirstDraw)
            }
            if (this.getLocalPos(serverSide) == 0)
                this.getPlayer(0).setselfNotDrag();
            //刷新
            this.refreshTingpanel();
            //获得听牌列表
            //  NetHandlerMgr.netHandler.sendGetReadyHand();
        }
        if (finishedListener) finishedListener();
    }
    onPlayerAction(msgData: { side: number, action: { action: number, tiles: string[], beActionSide?: number }[] }, finishedListener) {
        this.operatorArea.hide();

        var actionData = msgData["action"][0];
        var type = actionData["action"];
        var doSide = msgData["side"];
        var passiveSide = actionData["beActionSide"];
        var meldTileList = actionData["tiles"];

        this.updatePlayerTurn(doSide);

        var player = this.getPlayer(doSide, true);
        var passivePlayer = (passiveSide == null ? null : this.getPlayer(passiveSide, true));

        var actData = {
            "type": type,
            "getPlayer": player,
            "passivePlayer": passivePlayer,
            "tileData": (meldTileList[meldTileList.length - 1]),
            "originalList": (meldTileList),
            "list": meldTileList,
            "isShowEffect": (!msgData["instant"]),
            "from": this.getLocalPos(passiveSide),
            "container": this
        };
        // console.log('onPlayerAction:',actData);
        if (this.tingAutoBtn.visible) {
            this.tingAutoBtn.enabled = true;
        }
        var doActionCB = () => {
            if (type == ACTION_OPTION.CHOW || type == ACTION_OPTION.PONG) {
                this.updatePlayerTurn(doSide);
            }
            this.lastDrawPlayer = null;

            if (this.getLocalPos(doSide) == 0) {
                //吃碰之后移除听牌显示（会影响听的牌）

                /**吃碰杠后显示预听牌 */
                if (type == ACTION_OPTION.CHOW || type == ACTION_OPTION.PONG || ACTION_OPTION.OTHERS_KONG || ACTION_OPTION.SELF_KONG || ACTION_OPTION.CONCEALED_KONG) {
                    this.ready_hand_fancy()
                }

                /** */
            }

            if (finishedListener != null)
                finishedListener();
        };

        try {
            var removeTileID = actData["tileData"];
            switch (type) {
                case ACTION_OPTION.CHOW:
                    passivePlayer.removeOutTile(removeTileID);
                    player.chow(actData, doActionCB);
                    this.refreshTingpanel();
                    return;
                case ACTION_OPTION.PONG:
                    passivePlayer.removeOutTile(removeTileID);
                    player.pong(actData, doActionCB);
                    this.refreshTingpanel();
                    return;
                case ACTION_OPTION.OTHERS_KONG:
                    passivePlayer.removeOutTile(removeTileID);
                    player.kong(actData, doActionCB);
                    this.refreshTingpanel();
                    return;
                case ACTION_OPTION.SELF_KONG:
                    player.addToKong(actData, doActionCB);
                    this.refreshTingpanel();
                    return;
                case ACTION_OPTION.CONCEALED_KONG:
                    player.concealedKong(actData, doActionCB);
                    this.refreshTingpanel();
                    return;
                case ACTION_OPTION.HU:
                    this.onPlayerHu(actData, finishedListener);
                    return;
                case ACTION_OPTION.TING:
                    this.doTingAction(type, actData, msgData, finishedListener);
                    break;
                default:
                    this.doSpecialAction(type, actData, msgData, finishedListener);
                    return;
            }
        } catch (error) {
            console.log(error)
        }
        if (finishedListener) finishedListener();
    }
    // 点听按钮的动作
    doTingAction(type, actData, msgData, finishedListener) {
        // this.tileTouch.setDiscardable(true);
        if (finishedListener != null)
            finishedListener();
    }
    //收到玩家是否听牌协议
    onReadyHand(msgData, finishedListener) {
        // this.getPlayer(0).getTilesDataMeld();
        let readyHandTiles = msgData["tile"];
        let myFancyTiles = msgData["myTiles"];
        myFancyTiles.sort();
        let listLength = readyHandTiles.length;
        if (listLength == 0) {
            // console.log(this, "=============");
            this.tingdatas.splice(0, this.tingdatas.length);
            //this.operatorArea.hideReadyHand();
            this.tingBtn.visible = false;
            this.tingpanel.visible = false;
            this.restTingAuto();
        }
        else {
            // console.log(msgData, "==============听牌");
            this.tingdatas.splice(0, this.tingdatas.length);
            for (let i = 0; i < readyHandTiles.length; i++) {
                // let cardid = readyHandTiles[i].split(':')[0];
                let cardid = readyHandTiles[i];
                this.tingdatas.push(cardid);
            }
            this.refreshTingpanel();
            this.tingBtn.visible = true;
            this.tingpanel.visible = true;
            this.tingAutoBtn.visible = true;
            var stateCtl = this._view.getController('proxy')
            if (stateCtl.selectedIndex == 1) {
                this.tingAutoBtn.enabled = false;
                this.tingAutoBtnCtl.selectedIndex = 0;
                this.isTingAuto = false;
            }
        }
        if (finishedListener != null)
            finishedListener();
    }
    refreshTingpanel(isclick = false) {
        //刷新
        if (isclick) {
            if (this.tingdatas != null && this.tingdatas.length > 0) {
                this.tingpanel.visible = !this.tingpanel.visible;
                if (this.tingpanel.visible) {
                    this.showtingpanel();
                }

            }
            else {
                this.tingBtn.visible = false;
                this.tingpanel.visible = false;
                this.restTingAuto();

            }
        }
        else {
            if (this.tingdatas != null && this.tingdatas.length > 0)
                this.showtingpanel();
            else {
                this.tingBtn.visible = false;
                this.tingpanel.visible = false;
                this.restTingAuto();

            }
        }

    }
    //听牌后自动出牌
    TingAuto() {
        if (this.tingAutoBtnCtl.selectedIndex == 1) {
            //默认不勾选
            this.tingAutoBtnCtl.selectedIndex = 0;
            this.isTingAuto = false;
        }
        else {
            //勾选
            this.tingAutoBtnCtl.selectedIndex = 1;
            this.isTingAuto = true;
            this.AutoSendcardCheck(300);
        }

    }
    restTingAuto() {
        this.tingAutoBtn.visible = false;
        this.tingAutoBtnCtl.selectedIndex = 0;
        this.isTingAuto = false;
    }
    //自动出牌  

    AutoSendcardCheck(delay: number) {
        let player = this.getPlayer(0);
        let length = player.hand_tiles.numChildren;

        if (this.isTingAuto && length > 0) {
            let time = 0;
            let cb = () => {

                if (time < delay) {
                    time += Laya.timer.delta;
                    Laya.timer.frameOnce(1, this, cb);
                } else {
                    let num = player.hand_tiles.numChildren + player.meld_tiles.numChildren * 3
                    // console.log(num, "=============手牌数");
                    if (num == this.handCardsnum) {
                        player.sendDiscardCheck(player.hand_tiles.getChildAt(player.hand_tiles.numChildren - 1).data);
                    }
                }
            }

            cb();
        }
    }

    showtingpanel(tingdatas = this.tingdatas, isNotShowNum: boolean = false) {
        this.tingpanel.visible = true;
        let tinglist = this.tingpanel.getChild('tinglist').asList;
        tinglist.removeChildrenToPool();
        let cardActualWidth: number;
        let cardActualHeight: number;
        for (let i = 0; i < tingdatas.length; i++) {
            let card = tinglist.addItemFromPool().asCom;
            let icon = card.getChild('icon');
            MahjongMgr.inst.setTile(icon.asLoader, tingdatas[i]);
            let txt = card.getChild('numtxt').asTextField;
            if (isNotShowNum == true) {
                txt.visible = false;
                card.getChild('n10').visible = false;
                card.getChild('n11').visible = false;
            }
            else {
                let num = this.getcardremainnum(tingdatas[i]);
                // console.log(num, "===========牌数");
                let ctl = card.getController('numtype');
                if (num > 0) {
                    ctl.selectedIndex = 0;
                } else {
                    ctl.selectedIndex = 1;
                }
                txt.text = num.toString();
                txt.visible = true;
                card.getChild('n10').visible = true;
                card.getChild('n11').visible = true;
            }
            if (cardActualWidth == null) {
                cardActualWidth = card.actualWidth;
                cardActualHeight = card.actualHeight;
            }
        }
        let bg = this.tingpanel.getChild('bg');
        let cardNum = tinglist.numChildren;
        let tinglistColumnGap = tinglist.columnGap;
        if (cardNum > 0 && cardNum <= 7) {
            this.tingpanel.x = this.view.actualWidth / 2 - ((cardNum - 1) * (cardActualWidth + tinglistColumnGap) / 2) * this.tingpanel.scaleX;
            this.tingpanel.y = this.view.actualHeight / 2 - cardActualHeight / 2;
            bg.width = cardNum * (cardActualWidth + tinglistColumnGap) - tinglistColumnGap / 3;
            bg.height = cardActualHeight * 1 + tinglist.lineGap;
        }
        else if (cardNum > 7) {

            let multiple = Math.floor((cardNum - 1) / 7);

            this.tingpanel.x = this.view.actualWidth / 2 - (6 * (cardActualWidth + tinglistColumnGap) / 2) * this.tingpanel.scaleX;
            this.tingpanel.y = this.view.actualHeight / 2 - cardActualHeight * multiple / 2;
            bg.width = 7 * (cardActualWidth + tinglistColumnGap) - tinglistColumnGap / 3;

            bg.height = (cardActualHeight + tinglist.lineGap) * (multiple + 1);
        }
    }

    getcardremainnum(id) {
        let num = 0
        for (let i = 0; i < this.playerCount; i++) {
            let side = this.getLocalPos(i);
            let player = this.getPlayer(side);
            num = num + player.getTilesDataMeld(id) + player.gethandcardnum(id) + player.getoutcardnum(id);
        }
        num = this.cardTypenum - num;
        return num;
    }
    onPlayerHu(data, cb) {

        var huPlayer = data["getPlayer"];
        var huTiles = data["list"];
        var passivePlayer = data["passivePlayer"];
        var removeTileID = data["tileData"];

        //关掉指示器,手牌不让操作
        // this.turnIndicator.stopCountdown();
        // this.tileTouch.setDiscardable(false);

        //摊牌
        var handWallTiles = [];
        var lastTilePos = null;
        if (passivePlayer != null) {
            huPlayer.addHandTiles([removeTileID]);
            //出牌人的牌拿走
            passivePlayer.removeOutTile(removeTileID);
        }
        //隐藏听牌面板
        this.tingpanel.visible = false;
        this.tingBtn.visible = false;
        this.restTingAuto();
        this.tingdatas.splice(0, this.tingdatas.length);
        huPlayer.hu(data, cb);
        this.getPlayer(0).resetcardcolor();
    }

    doSpecialAction(type, actData, msgData, finishedListener) {
        // this.isTingAction = false;
        this.isClickTing = false;
        if (finishedListener) finishedListener();
    }

    lastDrawPlayer = null;
    playerSelf = null;

    onShowActionOption(msgData, finishedListener = null) {
        // console.log(msgData, "=========吃碰杠");

        // this.turnIndicator.indicate(0);
        // this.tileTouch.setDiscardable(false);

        var actionData = msgData["actions"];
        var actionNum = msgData["num"] || 0;
        var data = [];
        var tileId2Action = {};
        var kongTiles = [];
        for (var i = 0; i < actionData.length; i++) {
            var oneActionData = actionData[i];
            var oneActionType = oneActionData["action"];
            var oneActionTiles = oneActionData["tiles"];
            var isOriginHu = false;

            if ((this.lastDrawPlayer == this.playerSelf) && (oneActionType == ACTION_OPTION.HU))
                isOriginHu = true;

            if ((oneActionType == ACTION_OPTION.SELF_KONG) || (oneActionType == ACTION_OPTION.CONCEALED_KONG)) {
                kongTiles = kongTiles.concat(oneActionTiles);

                Tools.inst.each(oneActionTiles, (value, key) => {
                    tileId2Action[value] = oneActionType;
                }, this);
                continue;
            }

            var oneData = {
                "type": oneActionType,
                "choiceList": oneActionTiles,
                "isOriginHu": isOriginHu
            };
            if (oneActionType == 7) {
                // this.isTingAction = true;
                oneData.choiceList = [oneActionTiles.join(',')];
            }
            data.push(oneData);
        }

        if (kongTiles.length != 0) {
            var kongData = {
                "type": ACTION_OPTION.SELF_KONG,
                "choiceList": kongTiles.sort(),
                "isOriginHu": false
            };
            data.push(kongData);
        }
        if (this.tingAutoBtn.visible) {
            this.isTingAuto = false;
            this.tingAutoBtnCtl.selectedIndex = 0;
            this.tingAutoBtn.enabled = false;
        }

        var cb = this.getActionCB(tileId2Action, actionNum);

        //show之前先隐藏一次
        this.operatorArea.hide();
        this.operatorArea.show(data, cb);

        if (finishedListener) finishedListener();
    }

    getActionCB(tileId2Action, actionNum) {
        //console.log(tileId2Action, actionNum, "=========11111111getActionCB");
        return (type, meldList) => {
            // console.log(type, meldList, "============getActionCB");
            if (type == ACTION_OPTION.TING) {
                this.isClickTing = true;
                // console.log(meldList, "==========meldList")
                this.tryMarkTiles(meldList);

                //this.tileTouch.setDiscardable(true);
                this.playerSelf.senTypeData = {
                    sendType: type,
                    meldList: meldList,
                    actionNum: actionNum
                };
                //显示过
                let actions = {
                    "action": 0,
                    "tiles": [""]
                }
                let msgdata = {
                    "actions": actions,
                    'num': actionNum
                }
                this.onShowActionOption(msgdata);
                // this.operatorArea.hide();
                return;
            }
            var sendType = type;
            if (sendType == ACTION_OPTION.SELF_KONG)
                sendType = tileId2Action[meldList];
            //过
            if (this.isClickTing && sendType != ACTION_OPTION.TING) {
                this.playerSelf.resetcardcolor();
                this.isClickTing = false;
            }


            NetHandlerMgr.netHandler.sendAction(sendType, meldList, actionNum);

            this.operatorArea.hide();

            if (this.lastDrawPlayer == this.playerSelf)
                this.updatePlayerTurn(MahjongMgr.inst.getServerPos(0));

            //自动打牌相关
            // if (type == 0){
            //     this.operatorArea.cancelAutoDiscard();
            // }
        };
    }
    //手牌变黄
    tryMarkTiles(meldList, isCantouch = false) {
        let hand_tiles: fairygui.GList = this.playerSelf.getHandcards();
        let chooseList = meldList.concat();
        chooseList = chooseList.split(',');
        for (let i = 0; i < hand_tiles.numChildren; i++) {
            hand_tiles.getChildAt(i).asCom.touchable = isCantouch;
        }
        for (let i = 0; i < hand_tiles.numChildren; i++) {
            for (let j = 0; j < chooseList.length; j++) {
                let card = hand_tiles.getChildAt(i).asCom;
                if (chooseList[j] == card.data) {
                    this.playerSelf.setCardcolor(i);
                }
            }
        }
    }

    // 更新金币数量
    onGoldUpdate(msgData) {
        //console.log(msgData)
        var scoreList = msgData["playerinfo"];
        for (var i = 0; i < scoreList.length; i++) {
            var oneData = scoreList[i];
            var side = this.getLocalPos(oneData["side"]);
            var player = this.getPlayer(side);
            player.setScore(oneData["change"], oneData["score"]);
        }
    }
    //破产
    onNoGold(msgData) {
        let side = this.getLocalPos(msgData['side']);
        this.getPlayer(side).SetNoGold();
    }

    onGameEnd(msgData, finishedListener) {
        NetHandlerMgr.netHandler.removeAllMsgListener(ProtoKey.S_C_EXIT_ROOM);

        this.resetInEnd();

        var setData = msgData["setUserDatas"];
        if (setData != null && setData.length > 0) {
            //然后在玩家头像那里计算分数
            // for(var n = 0; n < setData.length; n ++)
            // {
            //     var oneSetData = setData[n];
            //     var setDataSide = this.getLocalPos(oneSetData["side"]);
            //     var player = this.getPlayer(setDataSide);
            //     player.balanceScore(oneSetData["score"]);
            // }
        }
        // console.log(setData, "-------------结算");
        if (msgData["isDrawn"]) {
            this.gameStateCtl.setSelectedIndex(2);
            Tools.inst.setTimeout(() => {
                this.showBalance(setData);
                this.gameStateCtl.setSelectedIndex(4);
            }, 500)
            SoundMgr.drawn();
        }
        else {
            SoundMgr.win();
            this.gameStateCtl.setSelectedIndex(3);
            Tools.inst.setTimeout(() => {
                this.showBalance(setData);
                this.showAutoContTimer();
                this.gameStateCtl.setSelectedIndex(4);
            }, 500)
        }

        //发送可以开始下一局准备
        //NetHandlerMgr.netHandler.sendReadyNextRound();

        if (finishedListener) finishedListener();
    }

    resetInEnd() {
        var stateCtl = this._view.getController('proxy');
        stateCtl.setSelectedIndex(0);
    }

    showBalance(setData) {
        this.setBalance.showData(setData, 0, this.playerCount, this.roomNumstr);
    }

    onDispose() {
        Laya.timer.clearAll(this);
        Laya.stage.off(Laya.Event.KEY_DOWN, this, this.onKeyDown);
        this.tingBtn.mode = -1;
        this.huAl = null;
    }

    onKeyDown(e: Event): void {
        if (TestMgr.IS_REAL_ACCOUNT) return;
        var keyCode: number = e["keyCode"];
        var Keyboard = Laya.Keyboard;
        switch (keyCode) {
            case Keyboard.A:
                NetHandlerMgr.netHandler.gameManage("2:a1a1a5a5a6a6a2a2", this.onGMResult.bind(this));
                // NetHandlerMgr.netHandler.gameManage("2:b1b1b2b2b1b2b4b4b4b5b5b4b1",this.onGMResult.bind(this));
                // console.log("==============发送GM");
                // NetHandlerMgr.netHandler.gameManage("2:e1e1e1a2a2a2a2d5d5d5",this.onGMResult.bind(this));
                // this.getPlayer(1).layHandTile(0);                
                // this.getPlayer(2).setScore(-666, 5598);
                break;
            case Keyboard.B:
                NetHandlerMgr.netHandler.gameManage("1:a2", this.onGMResult.bind(this));
                // this.getPlayer(0).removeOutTile("");
                // for(var i=0;i<4;i++)
                // this.getPlayer(i).layHandTile(1,['a1','a4']);
                // this.getPlayer(0).refreshOutPinPos();
                break;
            case Keyboard.G:
                NetHandlerMgr.netHandler.gameManage("1:a1", this.onGMResult.bind(this));
                // var txtGM = this.view.getChild('GM').asLabel;
                // NetHandlerMgr.netHandler.gameManage(txtGM.text,this.onGMResult.bind(this));
                break;
            case Keyboard.M:
                NetHandlerMgr.netHandler.gameManage("1:a5", this.onGMResult.bind(this));
                //NetHandlerMgr.netHandler.gameManage('2:d1d1d1d1a1a1a1a1a2a2a2a2', this.onGMResult.bind(this));
                //NetHandlerMgr.netHandler.gameManage('1:b2', this.onGMResult.bind(this));
                break;
            default:
                console.log(keyCode)
                break;
        }
    }

    onGMResult(data) {
        var result = data["result"];
        var reason = data["reason"];
        if (result) {
            Alert.show("Set GM Success");
        } else {
            Alert.show(ExtendMgr.inst.getText4Language(reason));
        }
    }

    onExitRoom() {
        this.showRequesting(true);
        if (NetHandlerMgr.netHandler != null && NetHandlerMgr.netHandler.sendExitRoom != null && NetHandlerMgr.netHandler.valid()) {
            NetHandlerMgr.netHandler.sendExitRoom();
        }
        else {
            UserMgr.inst.returnToLobby();
        }
    }

    onGoldExitRoomResult(msgData, finishedListener) {
        //console.log(msgData)        
        this.showRequesting(false);
        if (msgData['result']) {
            UserMgr.inst.returnToLobby();
            this.Cbalance.getChild("cBalance").asCom.getChild("btnReady").asButton.mode = -1;
            this.Cbalance.getChild("cBalance").asCom.getChild("btnClose").asButton.mode = -1;
        } else {
            NetHandlerMgr.netHandler.sendData(ProtoKeyParty.C_S_EXIT_ROOM_CONFIRM);
        }
        if (finishedListener) finishedListener();
    }
}