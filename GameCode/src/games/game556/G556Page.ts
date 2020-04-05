class G556Page extends GbpPage {
    constructor(scene = "GS_556") {
        super("G556", scene);
    }
    protected btnOpen: fairygui.GButton = null;

    protected greyScrenn: fairygui.GGraph;

    protected bullStyle = 0;

    public gameID: number = 556;
    public selfPlayer: GbpPlayerFrame;
    protected uiPlayerCount: number = 8;
    protected tableUrl = ResourceMgr.RES_PATH + 'bg/table_bg.jpg';
    protected bgUrl: string = ResourceMgr.RES_PATH + 'bg/bg2.jpg';
    protected PlayerFrames: Array<G556PlayerFrame> = [];
    public poolKey = 'G556Poker';
    protected cardParentIndex: number;

    newPlayerFrame(side) {
        return new G556PlayerFrame({
            side: side,
            seat: this.view.getChild('seat' + side).asCom,
            out_pokers: this.view.getChild('out_pokers_' + side).asList,
            out_nnStr: this.view.getChild('out_nn_' + side).asCom,
            out_QStr: this.view.getChild('QStr' + side).asCom,
            out_BStr: this.view.getChild('BStr' + side).asCom,
            bullStyle: this.bullStyle
        })
    }


    onCreated(data: any = null) {
        var view = this._view;
        var robTheVillageBG = view.getChild('operation').asCom;
        for (var i = 0; i < 5; ++i) {
            var child = robTheVillageBG.getChild('btn_Q' + i);
            var btn = child.asButton;
            if (btn != null) {
                btn.onClick(this, this.onRobTheVillage, [i]);
            }
        }
        var btnOpen = view.getChild('btnOpen').asButton;
        this.btnOpen = btnOpen;
        btnOpen.onClick(this, this.onBtnOpen.bind(this));
        this.greyScrenn = view.getChild('greyScreen').asGraph;
        this.initPool();
        this.cardParentIndex = view.getChildIndex(view.getChild('cardParent'));
        super.onCreated(data);
    }

    initPool() {
        //预先把发牌动画的牌加到池里
        for (let j = 0; j < 4 * this.uiPlayerCount; j++) {
            GObjectPool.inst.removeItemToPool(this.poolKey, fairygui.UIPackage.createObject('G556', 'Poker'));
        }
    }

    onBtnOpen() {
        NetHandlerMgr.netHandler.sendOnHasBullOrNot(2);
        this.btnOpen.visible = false;
        this.getPlayer(0).showOutPokersAction();
    }

    getPlayer(side: number, server: boolean = false): G556PlayerFrame {
        if (server) side = this.getLocalPos(side);
        return this.PlayerFrames[side];
    }

    //  选择抢庄倍数
    onRobTheVillage(ind) {
        NetHandlerMgr.netHandler.sendOnStrive(ind);
        this.setRobTheVillageState(false);
    }

    onSelectRate(value) {
        //var values=[5,10,15,20,25];
        // this.readyRate=value;
        NetHandlerMgr.netHandler.sendBid(value, 1);
        this.setRobTheVillageState(false);
    }

    onEnterRoomSuccess(data) {
        // console.log('onEnterRoomSuccess ok',data);
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

    onRefreshGameData(refreshData) {
    }

    initGame(gameInfo) {
        this.reset();

        this.initGameInfo(gameInfo);

        var roomInfo = gameInfo["roomInfo"];
        this.initRoomInfo(roomInfo);
    }

    reset() {
        super.reset();
        this.gameStateCtl.setSelectedIndex(0);
        GObjectPool.inst.getItemList(this.poolKey).forEach((item) => {
            GObjectPool.inst.removeItemToPool(this.poolKey, item)
        })
    }


    resetGame() {
        super.resetGame();
        this.btnContinue.visible = false;
        this.btnOpen.visible = false;
    }

    initRoomInfo(roomInfo) {
        var playerList = roomInfo["playerList"];
        Tools.inst.each(playerList, (playerInfo) => {
            if (playerInfo != null) {
                var posServer = playerInfo["side"];
                var posLocal = this.getLocalPos(posServer);
                this.getPlayer(posLocal).setSeat(playerInfo);
            }
        }, this);
    }

    initMsgListen() {
        super.initMsgListen();
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_SET_START, this.onSetStart.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_DRAW_TILES, this.onPlayerDraw.bind(this));

        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey556.S_C_READY_GAME_DATA, this.onReadyShow.bind(this));

        NetHandlerMgr.netHandler.addMsgListener(ProtoKey556.S_C_MESSAGE, this.onGetMessage.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey556.S_C_HAS_BULL_OR_NOT, this.onHasBullOrNot.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKey556.S_C_WAIT_TIME, this.onServerCountDown.bind(this));

        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey556.S_C_STRIVE_FOR_DEALER, this.onStriveForDealer.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey556.S_C_GA_DATA, this.receivedGambleChoose.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey556.S_C_GA_CHOOSE, this.receivedGambleWager.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey556.S_C_STRIVE_CHOOSE, this.onStriveChoose.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey556.S_C_STRIVE_RESULT, this.onStriveResult.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey556.S_C_GET_ONE_RESULT, this.onGetOneResult.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey556.S_C_DEAL_TILES_NN, this.onDealTiles.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey556.S_C_FLY, this.onGoldFlightAnimation.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyJDNN.S_C_RESULT_INFO, this.OnResultInfo.bind(this));
    }

    //win_status 3 通赔 4 通杀
    OnResultInfo(msgData, finishedListener) {
        let winStatus = msgData['win_status']
        this.showWinStaus(winStatus, finishedListener);
    }

    // 飞行金币
    onGoldFlightAnimation(msgData, finishedListener) {
        //console.log(msgData)
        this.hideTimeTip();
        var dealer = this.getLocalPos(msgData["dealer"]);
        let others = msgData["others"];

        Tools.inst.each(others, (data, i) => {
            let localSide = this.getLocalPos(data["side"])
            let score = data["score"];
            if (localSide != dealer) {
                if (score < 0) {
                    this.onBettingAnimation(localSide, dealer);
                }
            }
        });
        Tools.inst.setTimeout(() => {
            Tools.inst.each(others, (data, i) => {
                let localSide = this.getLocalPos(data["side"])
                let score = data["score"];
                if (localSide != dealer) {
                    if (score > 0) {
                        this.onBettingAnimation(dealer, localSide);
                    }
                }
            });
            if (finishedListener) finishedListener();
        }, 1000);
    }
    onBettingAnimation(startPos: number, endPos: number) {
        SoundMgrNiu.flyGold();
        let startPlayer = this.getPlayer(startPos);
        let startPosX = startPlayer.getSeatX();
        let startPosY = startPlayer.getSeatY();

        let endPlayer = this.getPlayer(endPos);
        let endPosX = endPlayer.getSeatX();
        let endPosY = endPlayer.getSeatY();

        var randomInt = Tools.inst.randomInt;
        var view = this._view;

        for (var i = 0; i < 20; i++) {
            let gold = fairygui.UIPackage.createObject('G556', 'tb_gold').asImage;
            gold.setScale(0.8, 0.8)
            gold.setXY(startPosX, startPosY);
            view.addChild(gold);
            gold.parent.setChildIndex(gold, gold.parent.numChildren - 2);

            let hd = Handler.create(gold, () => {
                view.removeChild(gold, true);
            });

            let goldX = randomInt(endPosX, endPosX + 100);
            let goldY = randomInt(endPosY, endPosY + 100);

            let tween = Laya.Tween;
            tween.to(gold, { x: goldX, y: goldY }, 500, Laya.Ease.circInOut, hd, i * 10);
        }
    }

    onSetStart(msgData, finishedListener) {
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

    onPlayerJoin(msgData) {
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

    private readyCallback;
    onReadyShow(msgData, finishedListener) {
        var btnReady;
        if (btnReady) {
            btnReady.offClick(this, this.readyCallback);
            this.readyCallback = () => {
                btnReady.visible = false;
                NetHandlerMgr.netHandler.sendReadyGame();
            }
            btnReady.onClick(this, this.readyCallback);
            btnReady.visible = true;
        } else {
            if (this.gameStateCtl && this.gameStateCtl.selectedIndex != 3) {
                NetHandlerMgr.netHandler.sendReadyGame();
            }
        }
        if (finishedListener) finishedListener();
    }

    onGetMessage(msgData) {
        //console.log(msgData);
    }

    onServerCountDown(msgData) {
        //console.log(msgData)
        var wait_time = (msgData['wait_time'] || 3) * 1000;
        switch (msgData['stage']) {
            case 'start':
                this.gameStateCtl.setSelectedIndex(2);
                this.setTimeTip(4, null);
                break;
            case 'strive':
                this.setTimeTip(1, wait_time);
                break;
            case 'wager':
                this.setTimeTip(2, wait_time);
                break;
            case 'draw':
                this.setTimeTip(3, null);
                break;
        }
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

    onDealTiles(msgData, finishedListener) {
        //记录参与游戏玩家
        var sides = msgData['participantSides'].map((d) => { return this.getLocalPos(d) });
        sides.sort();
        var tiles = msgData["tiles"];

        // if (tiles && tiles[0])
        //     this.getPlayer(0).setCards(tiles);
        // //在游戏的玩家显示手牌
        // for (var i = 0; i < sides.length; i++) {
        //     var side = sides[i];
        //     if (side == 0) continue;
        //     this.getPlayer(side).setCards(new Array(tiles.length));
        // }
        // SoundMgrNiuJD.fapai();
        //每轮间隔
        let dealDelta = 100;
        //每张间隔
        let oneCardDelta = 0;
        //单张运动时间
        let duration = 1000;
        //发完牌多久翻牌
        let showCardDelay = 100;
        let cards: Array<fairygui.GComponent> = [];
        {
            let cardIndex: number = 0;
            let startScale = 0.0;
            for (let i = 0; i < tiles.length; i++) {
                Laya.timer.once(oneCardDelta * i * sides.length + dealDelta * i, this, (i) => {
                    sides.sort(function (x, y) {
                        return Math.random() > .5 ? -1 : 1
                    });
                    for (let j = 0; j < sides.length; j++) {
                        Laya.timer.once(oneCardDelta * j, this, (sides, j, i) => {
                            let side = sides[j];
                            let player = this.getPlayer(side);
                            let firstCard = player.out_pokers.getChildAt(0).asCom;
                            let listStartPoi = firstCard.getChildAt(0).localToGlobal(0, 0);
                            let columnGap = (firstCard.width + player.out_pokers.columnGap) * player.out_pokers.scaleX;
                            let card = GObjectPool.inst.getItemFormPool(this.poolKey).asCom;
                            card.getChildAt(0).asLoader.url = player.getPokerUrl('');
                            card.data = '';
                            card.setScale(player.out_pokers.scaleX, player.out_pokers.scaleY);
                            let centerPoi: { x: number, y: number } = {
                                x: this.view.actualWidth / 2 + ((card.pivotX - 0.5) * card.actualWidth),
                                y: this.view.actualHeight / 2 + ((card.pivotY - 0.5) * card.actualHeight)
                            };
                            card.setXY(centerPoi.x, centerPoi.y);
                            this.view.addChild(card);
                            this.view.setChildIndex(card, this.cardParentIndex - 1 + (i * sides.length + j));
                            card.visible = true;
                            cards.push(card);
                            let endPoi = { x: listStartPoi.x + columnGap * i, y: listStartPoi.y };
                            SoundMgrNiuJD.fapai();
                            Tween.from(card, { scaleX: startScale, scaleY: startScale }, duration, laya.utils.Ease.quintOut);
                            Tween.to(card, endPoi, duration, laya.utils.Ease.cubicInOut, Handler.create(this, () => {
                                if (i == tiles.length - 1) {
                                    player.setCards(new Array(tiles.length));
                                    if (j == sides.length - 1) {
                                        for (let k = 0; k < cards.length; k++) {
                                            const card = cards[k];
                                            GObjectPool.inst.removeItemToPool(this.poolKey, card);
                                        }
                                        Laya.timer.once(showCardDelay, this, () => {
                                            this.getPlayer(0).showPokersAni(tiles, () => {
                                                if (finishedListener) finishedListener();
                                            })
                                        })
                                    }
                                }
                            }));
                        }, [sides, j, i])
                    }
                }, [i])
            }
        }
    }

    onStriveForDealer(msgData, finishedListener) {
        // console.log(msgData)

        // this.SetProgressCountdown(msgData['wait_time'] || 3,1);
        var robTheVillageBG = this.robTheVillageBG;
        for (var i = 1; i < 5; ++i) {
            var child = robTheVillageBG.getChild('btn_Q' + i);
            var btn = child.asButton;
            if (btn != null) {
                var idx = msgData['choices'].indexOf(i);
                btn.enabled = (idx != -1);
            }
        }
        this.setRobTheVillageState(true, 0);
        SoundMgrNiu.startQiang();

        if (finishedListener) finishedListener();
    }

    onStriveChoose(msgData, finishedListener) {
        // console.log(msgData)        

        var datas = msgData["data"];
        for (var i = 0; i < datas.length; i++) {
            var ele = datas[i];
            var side = this.getLocalPos(ele['side']);
            var player = this.getPlayer(side);
            player.showQiang(true, ele["choice"]);
            SoundMgrNiu.qiang(ele["choice"], player.sex);
            SoundMgrNiu.actionFinish();
            if (side == 0)
                this.setRobTheVillageState(false);
        }

        if (finishedListener) finishedListener();
    }

    onStriveResult(msgData: { strive_choice: number, dealer: number }, finishedListener) {
        var players = this.PlayerFrames;
        var counts = [];
        var max = 0;
        for (var i = 0; i < players.length; i++) {
            var idx = players[i].getQiangIndex();
            if (idx == msgData.strive_choice) {
                counts.push(this.getServerPos(i));
            }
        }
        let striveNumber = counts.length;
        let duration = striveNumber <= 3 ? 1000 : (striveNumber - 3) * 500 + 1000;
        let frameDelta = 5;
        this.horsRaceLamp(duration, frameDelta, counts, () => {
            var dealer = this.getLocalPos(msgData.dealer);
            var player = this.getPlayer(dealer);
            this.hideTimeTip();
            SoundMgrNiu.dingzhuang();
            player.setLightMark(true);
            Tools.inst.setTimeout(() => {
                player.showQiang(true, msgData.strive_choice);
                player.updateBankerState(true);
                player.setLightMark(false);
                if (finishedListener) finishedListener();
            }, 1000)
        });
    }

    horsRaceLamp(duration: number, frameDelta: number, sides: number[], cb: () => void) {
        if (sides.length > 1) {
            let totalTime: number = 0;
            let currentIndex: number = 0;
            let currentFrame: number = 0;
            this.greyScrenn.visible = true;
            for (let i = 0; i < sides.length; i++) {
                const side = this.getLocalPos(sides[i]);
                let player = this.getPlayer(side);
                player.setLayerTop();
            }
            let update = () => {
                let delta = Laya.timer.delta;
                totalTime += delta;
                currentFrame++;
                if (currentFrame >= frameDelta) {
                    currentFrame = 0;
                    for (let i = 0; i < sides.length; i++) {
                        const side = this.getLocalPos(sides[i]);
                        let player = this.getPlayer(side);
                        if (i == currentIndex) {
                            player.showStriveBankerMask();
                        } else {
                            player.hideStriveBankerMask();
                        }
                    }
                    currentIndex++;
                    if (currentIndex == sides.length) {
                        currentIndex = 0;
                    }
                }
                if (totalTime >= duration) {
                    totalTime = 0;
                    for (let i = 0; i < sides.length; i++) {
                        const side = this.getLocalPos(sides[i]);
                        let player = this.getPlayer(side);
                        player.hideStriveBankerMask();
                    }
                    Laya.timer.clear(this, update);
                    this.greyScrenn.visible = false;
                    for (let i = 0; i < sides.length; i++) {
                        const side = this.getLocalPos(sides[i]);
                        let player = this.getPlayer(side);
                        player.resetLayerIndex();
                    }
                    if (cb != null) {
                        cb();
                    }
                }
            }
            Laya.timer.frameLoop(1, this, update);
        }
        else {
            if (cb != null) {
                cb();
            }
        }
    }

    receivedGambleChoose(msgData, finishedListener) {
        // console.log(msgData)  
        var robTheVillageBG = this.robTheVillageBG;
        for (var i = 0; i < 5; ++i) {
            var child = robTheVillageBG.getChild('btn_C' + i);
            var btn = child.asButton;
            if (btn != null) {
                var num = msgData['canGetGa'][i];
                btn.enabled = (num != undefined);
                if (btn.enabled) {
                    if (ExtendMgr.inst.lan == ExtendMgr.CN) {
                        btn.title = num + '倍';
                    } else {
                        btn.title = 'x' + num;
                    }

                    btn.onClick(this, this.onSelectRate, [num]);
                }
            }
        }
        this.setRobTheVillageState(true, 1);
        SoundMgrNiu.startBidGame();
        if (finishedListener) finishedListener();
    }

    receivedGambleWager(msgData, finishedListener) {
        if (msgData["reason"]) return;
        var wager_infos = msgData["data"];
        for (var i = 0; i < wager_infos.length; i++) {
            var dt = wager_infos[i];
            var posLocal = this.getLocalPos(dt["side"]);
            this.getPlayer(posLocal).setWagerStr(dt["ga"]);
            SoundMgrNiu.xia(dt["ga"])
            SoundMgrNiu.actionFinish();
        }
        if (finishedListener) finishedListener();
    }

    onPlayerDraw(msgData, finishedListener) {
        // console.log(msgData)
        this.setRobTheVillageState(false);
        // console.log('this.posServerSelf :',this.posServerSelf)
        var tiles = (msgData['tiles'][0] || [])['inTiles'] || [];
        var side = msgData['side'];
        if (side == this.posServerSelf) {
            SoundMgrNiuJD.fapai();
            this.btnOpen.visible = true;
        }
        this.getPlayer(side, true).addCards(tiles, true);

        Tools.inst.setTimeout(() => {
            if (finishedListener) finishedListener();
        }, 50);
    }

    onGetOneResult(msgData, finishedListener) {
        var side = this.getLocalPos(msgData['side']);
        var data = msgData["info"][0];

        var bullnum = data['bullnum'];
        var tiles = data["handcards"];
        if (true || bullnum > 0) {
            if (data['tiles4ten'] != null && data['tiles4bull'] != null) {
                tiles = data['tiles4ten'].concat(data['tiles4bull']);
            }
        }

        if (side == 0) this.btnOpen.visible = false;

        var player = this.getPlayer(side);
        if (!player.isBullFinish()) {
            let cb = () => {
                player.showBullStr(bullnum);
                if (finishedListener) finishedListener();
            }
            if (side != 0) {
                player.showPokersAni(tiles, () => {
                    cb();
                })
            } else {
                cb();
                SoundMgrNiu.pokerHit();
            }
        } else {
            if (finishedListener) finishedListener();
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

    onGameEnd(msgData, finishedListener) {
        this.gameStateCtl.setSelectedIndex(3);
        super.onGameEnd(msgData, finishedListener);
    }

    onHasBullOrNot(msgData, finishedListener) {
        if (!msgData['data']) return;
        let scData = msgData['data'][0];
        if (!scData) return;
        let side = this.getLocalPos(scData['side']);
        if (side == 0) this.btnOpen.visible = false;
        let info = scData['info'];
        let bullnum = info['bullnum'];

        if (true || bullnum > 0) {
            let player = this.getPlayer(side);
            if (!player.isBullFinish()) {
                //player.showBullStr(info["bullnum"]);
                let tiles = info["handcards"];
                if (info['tiles4ten'] != null && info['tiles4bull'] != null) {
                    tiles = info['tiles4ten'].concat(info['tiles4bull']);
                }
                let cb = () => {
                    player.showBullStr(bullnum);
                }
                if (side != 0) {
                    player.isBullFinishValue = true;
                    player.showPokersAni(tiles, () => {
                        cb();
                    })
                } else {
                    cb();
                    SoundMgrNiu.pokerHit();
                }
            }
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
        if (finishedListener) finishedListener();
    }

    onExitRoom() {
        this.showRequesting(true);
        super.onExitRoom();
    }

    onGoldExitRoomResult(msgData, finishedListener) {
        this.showRequesting(false);
        super.onGoldExitRoomResult(msgData, finishedListener);
    }

    onDispose() {
        super.onDispose();
        GObjectPool.inst.clearPool();
    }

}