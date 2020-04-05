class G557Page extends GbpPage {
    constructor() {
        super("G557", "GameScene");
    }
    public gameID: number = 557;
    public selfPlayer: G557PlayerFrame;
    protected uiPlayerCount: number = 5;
    protected poolKey: string = 'G557';
    protected tableUrl: string;
    protected bgUrl: string = ResourceMgr.RES_PATH + 'bg/bg4.jpg';
    protected PlayerFrames: Array<G557PlayerFrame> = [];
    private gameStage: number = 0;
    private btnHaveGroup: fairygui.GGroup;
    private isShowNiuBtn: boolean = false;
    private gameRefreshStage: boolean = false;
    private isBalance: Boolean = false;
    private goldList: Array<fairygui.GImage> = [];
    private selfNumberTip: fairygui.GLabel;

    newPlayerFrame(side) {
        return new G557PlayerFrame({
            side: side,
            seat: this.view.getChild('seat' + side).asCom,
            out_pokers: this.view.getChild('out_pokers_' + side).asList,
            out_nnStr: this.view.getChild('out_nn_' + side).asCom,
            out_QStr: this.view.getChild('QStr' + side).asCom,
            out_BStr: this.view.getChild('BStr' + side).asCom,
            complete: this.view.getChild('complete' + side).asCom,
        })
    }
    onCreated(data: any = null) {
        var view = this.view;
        this.selfNumberTip = view.getChild('selfNumberTip').asLabel;
        this.btnHaveGroup = this._view.getChild("btnHaveGroup").asGroup;
        this.btnHaveGroup.visible = false;
        this.initBtnHave();
        super.onCreated(data);
    }


    // 重连进来的数据
    onRefreshGameData(data) {
        this.resetGame();
        let stage = data["stage"];
        this.gameStage = stage;
    }

    reset() {
        super.reset();
        this.isBalance = false;
    }

    initMsgListen() {
        super.initMsgListen();
        // 串行消息处理
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyHLPD.S_C_DEAL_CARDS, this.onDealTiles.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_DRAW_TILES, this.onPlayerDraw.bind(this));
        // //正常消息处理

        //重写已有接口，先检查是否存在
        if (typeof ProtoKeyHLPD.S_C_READY_GAME_DATA != 'undefined') {
            NetHandlerMgr.netHandler.removeMsgListener(ProtoKeyHLPD.S_C_READY_GAME_DATA);
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyHLPD.S_C_READY_GAME_DATA, this.onReadyShow.bind(this));
        }
        //游戏
        NetHandlerMgr.netHandler.addMsgListener(ProtoKeyHLPD.S_C_HAS_BULL_OR_NOT, this.onHasBullOrNot.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_GAME_START_RESULT, this.onGameStartResult.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKeyHLPD.S_C_WAIT_TIME, this.onRefreshTimeOut.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKeyHLPD.S_C_DRAW_TILE, this.onDrawTile.bind(this));


        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyHLPD.S_C_STRIVE_FOR_DEALER, this.onStriveForDealer.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyHLPD.S_C_GA_DATA, this.receivedGambleChoose.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyHLPD.S_C_GA_CHOOSE, this.receivedGambleWager.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyHLPD.S_C_GET_ONE_RESULT, this.onGetOneResult.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyHLPD.S_C_STRIVE_CHOOSE, this.onStriveChoose.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyHLPD.S_C_STRIVE_RESULT, this.onStriveResult.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyHLPD.S_C_FLY, this.onGoldFlightAnimation.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyHLPD.S_C_GET_RESULT, this.receivedGambleOneResult.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyJDNN.S_C_RESULT_INFO, this.OnResultInfo.bind(this));
    }

    //win_status 3 通赔 4 通杀
    OnResultInfo(msgData, finishedListener) {
        let winStatus = msgData['win_status']
        this.showWinStaus(winStatus, finishedListener);
    }

    initBtnHave() {
        let btnHave0 = this._view.getChild("btnHave0").asButton;
        let btnHave1 = this._view.getChild("btnHave1").asButton;
        btnHave0.onClick(this, this.onBtnHave0);
        btnHave1.onClick(this, this.onBtnHave1);
    }

    onBtnHave0() {
        SoundMgr.clickButton();
        NetHandlerMgr.netHandler.sendDrawTile(true);

    }

    onBtnHave1() {
        SoundMgr.clickButton();
        NetHandlerMgr.netHandler.sendDrawTile(false);
    }

    // 游戏开始返回结果
    onGameStartResult(data, finishedListener) {
        if (!data["result"]) {

        }
        else {
            this.resetGame();
            SoundMgrNiu.gameStart();
            this.gameStateCtl.setSelectedIndex(1);
            let startAni = this.view.getChild('startAni').asCom;
            startAni.visible = true;
            startAni.getTransitionAt(0).play(Handler.create(this, () => {
                this.gameStateCtl.setSelectedIndex(2);
                startAni.visible = false;
                if (finishedListener != null) {
                    finishedListener();
                }
            }));
        }
    }

    onReadyShow(msgData, finishedListener) {
        if (!this.isBalance) {
            // this.btnReady.visible = true; 
            NetHandlerMgr.netHandler.sendReadyGame();
        }
        if (finishedListener) {
            finishedListener();
        }
    }

    onRefreshTimeOut(msgData) {
        var wait_time = msgData["wait_time"] * 1000;
        let stage = msgData['stage'];
        if (stage == GbpPage.GAMEPD_TIMER.start) {
            this.setTimeTip(4, null);
        } else if (stage == GbpPage.GAMEPD_TIMER.strive) {
            this.setTimeTip(1, wait_time);
        } else if (stage == GbpPage.GAMEPD_TIMER.wager) {
            this.setTimeTip(2, wait_time);
        } else if (stage == GbpPage.GAMEPD_TIMER.draw) {
            this.setTimeTip(6, wait_time);
        }
    }

    getPlayer(side: number) {
        return this.PlayerFrames[side];
    }

    // 要不要牌
    onDrawTile(msgData) {
        let drawTileInfo = msgData["drawTileInfo"];
        jx.each(drawTileInfo, (info, i) => {
            let localSide = this.getLocalPos(info["side"]);
            let drawTile = info["drawTile"];
            let several = this.getPlayer(localSide).getShowCardNum();
            if (localSide == 0) {
                this.btnHaveGroup.visible = drawTile;
                if (!drawTile) this.isShowNiuBtn = false;
            }
            if (several >= 2) {
                var isDrawTile = drawTile == true ? 1 : 0;
                this.getPlayer(localSide).showComplete(isDrawTile);
            }
        });
    }

    // 摸牌    
    onPlayerDraw(msgData, finishedListener) {
        let posDrawServer = msgData["side"];
        var localPos = this.getLocalPos(posDrawServer);
        var inTiles = (msgData['tiles'][0] || [])['inTiles'] || [];
        this.getPlayer(localPos).setDrawCard(inTiles, true);
        SoundMgrNiuJD.fapai();

        let selfCardNum = this.getPlayer(0).getHandCardNum();
        let tip = this.selfNumberTip;
        Tools.inst.setTimeout(() => {
            tip.getControllerAt(0).selectedIndex = selfCardNum > 21 ? 22 : selfCardNum;
            tip.visible = true;
            if (finishedListener) finishedListener();
        }, 50);
    }

    // 发牌
    onDealTiles(msgData, finishedListener) {
        let sides = msgData["participantSides"];
        let tiles = msgData["tiles"];
        let othersDealCardInfo = msgData["othersDealCardInfo"];
        this.getPlayer(0).setCards(tiles, () => true);
        SoundMgrNiuJD.fapai();
        if (othersDealCardInfo.length > 0) {
            if (tiles.length > 1) {
                this.btnHaveGroup.visible = true;
            }
            for (var i = 0; i < othersDealCardInfo.length; i++) {
                let side = othersDealCardInfo[i]["side"];
                let tiles = othersDealCardInfo[i]["tiles"];
                let localSide = this.getLocalPos(side);
                if (localSide != 0) {
                    this.getPlayer(localSide).setCards(tiles, () => true);
                }
            }
        }
        else {
            if (othersDealCardInfo.length > 0) {
                for (var i = 0; i < othersDealCardInfo.length; i++) {
                    let otherData = othersDealCardInfo[i];
                    let serverSide = otherData['side'];
                    let otherCard = otherData['tiles'];
                    let side = this.getLocalPos(serverSide);
                    this.getPlayer(side).setCards(otherCard, () => true);
                }
            } else {
                for (var i = 0; i < sides.length; i++) {
                    let side = this.getLocalPos(sides[i]);
                    if (side != 0) {
                        this.getPlayer(side).setOtherCards();
                    }
                }
            }
        }

        let selfCardNum = this.getPlayer(0).getHandCardNum();
        let tip = this.selfNumberTip;

        Tools.inst.setTimeout(() => {
            if (tiles.length > 1) {
                tip.getControllerAt(0).selectedIndex = selfCardNum > 21 ? 22 : selfCardNum;
                tip.visible = true;
            }
            if (finishedListener) finishedListener();
        }, 50);
    }
    // 显示抢庄
    onStriveForDealer(msgData, finishedListener) {
        var choices = msgData["choices"];
        SoundMgrNiu.startQiang();

        var robTheVillageBG = this.robTheVillageBG;
        for (var i = 0; i < 5; ++i) {
            var child = robTheVillageBG.getChild('btn_Q' + i);
            var btn = child.asButton;
            if (btn != null) {
                var num = msgData['choices'][i];
                btn.onClick(this, this.onRobTheVillage, [i]);
                btn.enabled = (num != undefined);
            }
        }

        this.setRobTheVillageState(true, 0);

        if (finishedListener) finishedListener();
    }

    // 抢庄确认
    onStriveChoose(msgData, finishedListener) {

        var datas = msgData["data"];
        for (var i = 0; i < datas.length; i++) {
            var ele = datas[i];
            var side = this.getLocalPos(ele['side']);
            var player = this.getPlayer(side);
            let isQiang = ele["choice"];

            if (side == 0) {
                this.setRobTheVillageState(false);
            }
            SoundMgrNiu.actionFinish();
            player.showQiang(true, ele["choice"]);
            SoundMgrNiu.qiang(ele["choice"]);
        }

        if (finishedListener) finishedListener();
    }

    //  选择抢庄倍数
    onRobTheVillage(ind) {
        SoundMgr.clickButton();
        NetHandlerMgr.netHandler.sendOnStrive(ind);
        this.setRobTheVillageState(false);
    }

    // 返回谁是庄
    onStriveResult(msgData, finishedListener) {

        var dealer = msgData["dealer"];
        var player = this.getPlayer(dealer);
        SoundMgrNiu.dingzhuang();
        player.setLightMark(true);

        Tools.inst.setTimeout(() => {
            var players = this.PlayerFrames;
            for (var i = 0; i < players.length; i++) {
                if (i == this.getLocalPos(dealer)) {
                    players[i].showQiang(true, msgData['strive_choice']);
                }
                players[i].updateBankerState(i == this.getLocalPos(dealer));
            }
            player.setLightMark(false);
            if (finishedListener) finishedListener();
        }, 1000)
    }

    // 显示下注
    receivedGambleChoose(msgData, finishedListener) {

        SoundMgrNiu.startBidGame();

        var robTheVillageBG = this.robTheVillageBG;
        for (var i = 0; i < 5; ++i) {
            var child = robTheVillageBG.getChild('btn_C' + i);
            var btn = child.asButton;
            if (btn != null) {
                var num = msgData['canGetGa'][i];
                btn.onClick(this, this.onSelectRate, [num]);
                // if (num == null) {
                //     btn.visible = false;
                // }
                btn.enabled = (num != undefined);
            }
        }
        this.setRobTheVillageState(true, 1);

        if (finishedListener) finishedListener();
    }

    // 不知道什么结果的返回
    receivedGambleOneResult(msgData, finishedListener) {
        this.selfNumberTip.visible = false;
        if (finishedListener) {
            finishedListener();
        }
    }

    // 下注的结果
    receivedGambleWager(msgData, finishedListener) {
        if (msgData["reason"]) return;
        var wager_infos = msgData["data"];
        for (var i = 0; i < wager_infos.length; i++) {
            var dt = wager_infos[i];
            var posLocal = this.getLocalPos(dt["side"]);
            this.getPlayer(posLocal).setWagerStr(dt["ga"]);
            // SoundMgrNiu.xia(dt["ga"]);
            if (posLocal == 0) {
                this.setRobTheVillageState(false);
            }
            SoundMgrNiu.actionFinish();
        }
        if (finishedListener) finishedListener();
    }

    // 一个个翻牌
    onGetOneResult(msgData, finishedListener) {
        this.resetBtnHaveGroup();
        this.hideComplete();
        var time = 0;
        var side = this.getLocalPos(msgData['side']);
        var data = msgData["info"][0];
        var tiles = data["handcards"];
        var player = this.getPlayer(side);
        if (!player.isBullFinish()) {
            player.setCards(tiles);
            player.showBullStr(data["bullnum"]);
            time = 500;
        }
        if (side == 0) {
            this.selfNumberTip.visible = false;
        }
        Laya.timer.once(time, this, () => {
            if (finishedListener) finishedListener();
        })
        if (side == 0) {
            SoundMgrNiu.pokerHit();
        }

        let isAllPlayerShowCard = true;
        this.PlayerFrames.forEach(player => {
            if (player.isInit == true && player.isBullFinish() == false) {
                isAllPlayerShowCard = false;
            }
        });
        if (isAllPlayerShowCard) {
            this.hideTimeTip();
        }
    }

    // 隐藏要不要牌
    hideComplete() {
        for (var i = 0; i < 5; i++) {
            this.getPlayer(i).hideComplete();
        }
    }

    // 状态
    onStage(msgData) {
        let stage = msgData["stage"];
        this.gameStage = stage;
    }

    // 飞行金币
    onGoldFlightAnimation(msgData, finishedListener) {
        var dealer = this.getLocalPos(msgData["dealer"]);
        let others = msgData["others"];

        jx.each(others, (data, i) => {
            let localSide = this.getLocalPos(data["side"])
            let score = data["score"];
            if (localSide != dealer) {
                if (score < 0) {
                    this.onBettingAnimation(localSide, dealer);
                }
            }
        });

        Tools.inst.setTimeout(() => {
            jx.each(others, (data, i) => {
                let localSide = this.getLocalPos(data["side"])
                let score = data["score"];
                if (localSide != dealer) {
                    if (score > 0) {
                        this.onBettingAnimation(dealer, localSide);
                    }
                }
            });

        }, 1000)

        //this.onScoreShow(msgData);
        if (finishedListener) {
            finishedListener();
        }
        this.resetBtnHaveGroup()
        this.gameRefreshStage = false;
    }

    // // 弹出分数
    // onScoreShow(msgData) {
    //     let others = msgData["others"];
    //     jx.each(others, (data, i) => {
    //         let localSide = this.getLocalPos(data["side"])
    //         let score = data["score"];

    //         let player = this.getPlayer(localSide);
    //         player.setScoreAction(score);

    //     });
    // }

    //金币飞行动画相关的东西/
    random4(n: number, m: number) {
        let random = Math.floor(Math.random() * (m - n + 1) + n);
        return random;
    }

    onBettingAnimation(startPos: number, endPos: number) {
        SoundMgrNiu.flyGold();
        let startPlayer = this.getPlayer(startPos);
        let startPosX = startPlayer.getSeatX();
        let startPosY = startPlayer.getSeatY();

        let endPlayer = this.getPlayer(endPos);
        let endPosX = endPlayer.getSeatX();
        let endPosY = endPlayer.getSeatY();

        for (var i = 0; i < 20; i++) {
            let gold = fairygui.UIPackage.createObject('G557', 'tb_gold').asImage;
            // gold.displayObject.loadImage("tb_gold.png");
            gold.setScale(0.8, 0.8)
            gold.setXY(startPosX, startPosY);
            this._view.addChild(gold);
            this.goldList.push(gold);

            let hd = Handler.create(gold, () => {
                gold.visible = false;
                this._view.removeChild(gold);
            });

            let goldX = this.random4(endPosX, endPosX + 100);
            let goldY = this.random4(endPosY, endPosY + 100);

            let tween = Laya.Tween;
            tween.to(gold, { x: goldX, y: goldY }, 500, Laya.Ease.circInOut, hd, i * 10);
        }


    }


    // 游戏结束
    onGameEnd(msgData, finishedListener) {
        super.onGameEnd(msgData, finishedListener);
        this.isBalance = true;
        NetHandlerMgr.netHandler.sendReadyNextRound();
    }

    // 接收是否有牛
    onHasBullOrNot(msgData) {
        if (!msgData['data']) return;
        var scData = msgData['data'][0];
        if (!scData) return;
        var side = this.getLocalPos(scData['side']);
        var info = scData['info'];
        var bullnum = info['bullnum'];
        if (bullnum > 0) {
            var tiles = info['tiles4bull'].concat(info['tiles4ten']);
            var player = this.getPlayer(side);
            if (side > 0) player.setCards(tiles);
            player.showBullStr(info["bullnum"]);
        }
        if (side == 0) {
            SoundMgrNiu.pokerHit();
        }
        let isAllPlayerShowCard = true;
        this.PlayerFrames.forEach(player => {
            if (player.isInit == true && player.isBullFinish() == false) {
                isAllPlayerShowCard = false;
            }
        });
        if (isAllPlayerShowCard) {
            this.hideTimeTip();
        }
    }

    // 初始化一些状态
    resetBtnHaveGroup() {
        this.btnHaveGroup.visible = false;
    }
}