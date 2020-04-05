class G555Page extends GbpPage {
    constructor(pkg = "G555", comp = "GameScene") {
        super(pkg, comp);
    }
    private gameStage: number = 0;
    private isBalance: Boolean = false;
    private btnLiangPai: fairygui.GButton;
    private myTitle: Array<string> = [];
    private isLiangPai: Boolean = false;
    private fanPaiList: Array<string> = [];
    private greyScrenn: fairygui.GGraph;
    public gameID: number = 555;
    public selfPlayer: G555PlayerFrame;
    protected uiPlayerCount: number = 5;
    protected PlayerFrames: Array<G555PlayerFrame> = [];
    public poolKey = 'G555Poker';
    private cardParentIndex: number;

    newPlayerFrame(side) {
        return new G555PlayerFrame({
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
        var view = this._view;
        this.greyScrenn = view.getChild('greyScreen').asGraph;
        var robTheVillageBG = view.getChild('operation').asCom;
        for (var i = 0; i < 2; ++i) {
            var child = robTheVillageBG.getChild('btn_Q' + i);
            var btn = child.asButton;
            if (btn != null) {
                btn.onClick(this, this.onRobTheVillage, [i]);
            }
        }
        this.btnLiangPai = this._view.getChild('btnLiangPai').asButton;
        this.btnLiangPai.onClick(this, this.onBtnLiangPai.bind(this));
        SoundMgr.playMusic("bgm_niu.mp3");
        this.initPool();
        this.cardParentIndex = view.getChildIndex(view.getChild('cardParent'));
        super.onCreated(data);
    }

    initPool() {
        //预先把发牌动画的牌加到池里
        for (let j = 0; j < 5 * this.uiPlayerCount; j++) {
            GObjectPool.inst.removeItemToPool(this.poolKey, fairygui.UIPackage.createObject('G555', 'Poker'));
        }
    }

    onNetIntoGame(data) {
        this.onEnterRoomSuccess(data);
    }

    getPlayer(side: number) {
        return this.PlayerFrames[side];
    }

    // 重连进来的数据
    onRefreshGameData(data) {
        //console.log("onRefreshGameData: " , data);
        this.resetGame();

        let stage = data["stage"];
        this.gameStage = stage;

        if (stage == GbpPage.GAME_STATE.WAIT_START) {
            return;
        }

        switch (stage) {
            case GbpPage.GAME_STATE.WAIT_ROLL:
            case GbpPage.GAME_STATE.GIVE_TILE:
            case GbpPage.GAME_STATE.GAMING:
                this.refershInGame(data);
                this.gameStateCtl.setSelectedIndex(2);
                break;

            case GbpPage.GAME_STATE.GAME_READY:
                this.refreshInGameEnd(data);
                break;

            default:
                break;
        }

    }

    // 在游戏中重连回来
    refershInGame(msgData) {
        let localSide = this.getLocalPos(msgData["dealerSide"]);
        let player = this.getPlayer(localSide);
        player.updateBankerState(true);
    }

    refreshInGameEnd(msgData) {
        this.gameStateCtl.setSelectedIndex(2);
    }

    reset() {
        super.reset();
        if (this.isLiangPai) {
            this.getPlayer(0).resetOutPokersAction();
            this.isLiangPai = false;
        }
        this.isBalance = false;
        this.fanPaiList = [];
        GObjectPool.inst.getItemList(this.poolKey).forEach((item) => {
            GObjectPool.inst.removeItemToPool(this.poolKey, item)
        })
    }

    initMsgListen() {
        super.initMsgListen();
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyJDNN.S_C_DEAL_TILES_NN, this.onDealTiles.bind(this));

        if (typeof ProtoKeyJDNN.S_C_READY_GAME_DATA != 'undefined') {
            NetHandlerMgr.netHandler.removeMsgListener(ProtoKeyJDNN.S_C_READY_GAME_DATA);
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyJDNN.S_C_READY_GAME_DATA, this.onReadyShow.bind(this));
        }

        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyJDNN.S_C_HAS_BULL_OR_NOT, this.onHasBullOrNot.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_GAME_START_RESULT, this.onGameStartResult.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKeyJDNN.S_C_STAGE, this.onStage.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(ProtoKeyJDNN.S_C_WAIT_TIME, this.onWaitTime.bind(this));

        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyJDNN.S_C_STRIVE_FOR_DEALER, this.onStriveForDealer.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyJDNN.S_C_GA_DATA, this.receivedGambleChoose.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyJDNN.S_C_GA_CHOOSE, this.receivedGambleWager.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyJDNN.S_C_GET_ONE_RESULT, this.onGetOneResult.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyJDNN.S_C_STRIVE_CHOOSE, this.onStriveChoose.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyJDNN.S_C_STRIVE_FOR_DEALER_TIMEOUT, this.onStriveForDealerTimeout.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyJDNN.S_C_STRIVE_RESULT, this.onStriveResult.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyJDNN.S_C_FLY, this.onGoldFlightAnimation.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyJDNN.S_C_RESULT_INFO, this.OnResultInfo.bind(this));
    }

    //win_status 3 通赔 4 通杀
    OnResultInfo(msgData, finishedListener) {
        let winStatus = msgData['win_status']
        this.showWinStaus(winStatus, finishedListener);
    }

    // 游戏开始返回结果
    onGameStartResult(data, finishedListener) {
        //console.log("onGameStartResult: ", data);
        if (!data["result"]) {

        }
        else {
            this.resetGame();
            SoundMgrNiu.gameStart();
            this.gameStateCtl.setSelectedIndex(1);
            let startAni = this.view.getChild('startAni').asCom;
            startAni.visible = true;
            console.log(startAni);
            startAni.getTransitionAt(0).play(Handler.create(this, () => {
                this.gameStateCtl.setSelectedIndex(2);
                startAni.visible = false;
                if (finishedListener != null) {
                    finishedListener();
                }
            }));
            // Tools.inst.setTimeout(() => {
            //     this.gameStateCtl.setSelectedIndex(2);
            // }, 1000);
        }

    }

    // 抢庄等待时间
    onStriveForDealerTimeout(msgData, finishedListener) {
        // this.updateTimer(msgData["wait_time"],0); // 封
        if (finishedListener) finishedListener();
    }

    onReadyShow(msgData, finishedListener) {
        if (!this.isBalance) {
            NetHandlerMgr.netHandler.sendReadyGame();
        }
        if (finishedListener) {
            finishedListener();
        }
    }


    onWaitTime(msgData) {
        let wait_time = msgData['wait_time'] * 1000;
        let stage = msgData['stage'];
        if (stage == GbpPage.GAMEPD_TIMER.start) {
            this.setTimeTip(4, null);
        } else if (stage == GbpPage.GAMEPD_TIMER.strive) {
            this.setTimeTip(1, wait_time);
        } else if (stage == GbpPage.GAMEPD_TIMER.wager) {
            this.setTimeTip(2, wait_time);
        } else if (stage == GbpPage.GAMEPD_TIMER.draw) {
            this.setTimeTip(3, null);
        }

    }

    onDealTiles(msgData, finishedListener) {
        let sides = msgData["sides"];
        let tiles = msgData["tiles"];
        sides = sides.map((value, index, array) => {
            return this.getLocalPos(value);
        })
        sides.sort();
        this.myTitle = tiles;
        /*         this.gameStateCtl.setSelectedIndex(3);
                for (var i = 0; i < sides.length; i++) {
                    let side = sides[i];
                    if (side == 0) {
                        SoundMgrNiuJD.fapai();
                    }
                    this.getPlayer(side).setCards(new Array(tiles.length));
                } */
        //每轮间隔
        let dealDelta = 100;
        //每张间隔
        let oneCardDelta = 0;
        //单张运动时间
        let duration = 1000;
        //发完牌多久翻牌
        let showCardDelay = 200;
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
                                                this.btnLiangPai.visible = true;
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

    //  选择抢庄倍数
    onRobTheVillage(ind) {
        SoundMgr.clickButton();
        NetHandlerMgr.netHandler.sendOnStrive(ind);
        this.setRobTheVillageState(false);
    }

    // 显示抢庄
    onStriveForDealer(msgData, finishedListener) {
        SoundMgrNiu.startQiang();
        let choices = msgData["choices"];
        this.setRobTheVillageState(true, 0);
        if (finishedListener) finishedListener();
    }

    // 抢庄确认
    onStriveChoose(msgData, finishedListener) {
        // console.log(msgData)
        var datas = msgData["data"];
        for (var i = 0; i < datas.length; i++) {
            var ele = datas[i];
            var side = this.getLocalPos(ele['side']);
            var player = this.getPlayer(side);

            if (side == 0) {
                this.setRobTheVillageState(false);
            }
            SoundMgrNiuJD.qiang(ele["choice"]);
            SoundMgrNiu.actionFinish();
            player.showQiang(true, ele["choice"]);
        }

        if (finishedListener) finishedListener();
    }

    // 返回谁是庄
    onStriveResult(msgData: { dealer: number, sides: number[] }, finishedListener) {
        let striveNumber = msgData.sides.length;
        let duration = striveNumber <= 3 ? 1000 : (striveNumber - 3) * 500 + 1000;
        let frameDelta = 5;
        this.horsRaceLamp(duration, frameDelta, msgData.sides, () => {
            // console.log(msgData)
            var dealer = msgData["dealer"];
            var player = this.getPlayer(dealer);
            this.hideTimeTip();

            SoundMgrNiu.dingzhuang();
            player.setLightMark(true);
            Tools.inst.setTimeout(() => {
                var players = this.PlayerFrames;
                for (var i = 0; i < players.length; i++) {
                    players[i].updateBankerState(i == this.getLocalPos(dealer));
                }
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

    // 显示下注
    receivedGambleChoose(msgData, finishedListener) {
        //console.log("receivedGambleChoose: ", msgData)
        SoundMgrNiu.startBidGame();
        // this.updateTimer(msgData["wait_time"],1);  封
        if (this.gameStage == GbpPage.GAME_STATE.GAME_READY) {
            return;
        }

        var robTheVillageBG = this.robTheVillageBG;
        for (var i = 0; i < 5; ++i) {
            var child = robTheVillageBG.getChild('btn_C' + i);
            var btn = child.asButton;
            if (btn != null) {
                var num = msgData['canGetGa'][i];
                btn.enabled = num != null;
                if (btn.enabled) {
                    btn.onClick(this, this.onSelectRate, [num]);
                }
            }
        }

        this.setRobTheVillageState(true, 1);

        if (finishedListener) finishedListener();
    }

    // 下注的结果
    receivedGambleWager(msgData, finishedListener) {
        // console.log(msgData)
        if (msgData["reason"]) return;
        if (this.gameStage == GbpPage.GAME_STATE.GAME_READY) {
            return;
        }

        var wager_infos = msgData["data"];
        for (var i = 0; i < wager_infos.length; i++) {
            var dt = wager_infos[i];
            var posLocal = this.getLocalPos(dt["side"]);
            this.getPlayer(posLocal).setWagerStr(dt["ga"]);
            SoundMgrNiuJD.xia(dt["ga"])
            if (posLocal == 0) {
                this.setRobTheVillageState(false);
            }
            SoundMgrNiu.actionFinish();
        }

        if (msgData["wait_time"] > 0) {
            // this.updateTimer(msgData["wait_3time"],1);   // 临时的
        }


        if (finishedListener) finishedListener();
    }

    // 一个个翻牌
    onGetOneResult(msgData, finishedListener) {
        //this.btnHaveGroup.visible = false;
        this.btnLiangPai.visible = false;
        // var time = 0;
        var side = this.getLocalPos(msgData['side']);
        var player = this.getPlayer(side);
        if (!player.isBullFinish()) {
            // time = 500;
            var data = msgData["info"][0];
            var bullnum = data['bullnum'];
            var tiles = data["handcards"];
            if (true || bullnum > 0) {
                if (data['tiles4ten'] != null && data['tiles4bull'] != null) {
                    tiles = data['tiles4ten'].concat(data['tiles4bull']);
                }
            }
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

        // Laya.timer.once(time, this, () => {
        //     if (finishedListener) finishedListener();
        // })

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

    // 状态
    onStage(msgData) {
        let stage = msgData["stage"];
        this.gameStage = stage;
    }

    // 飞行金币
    onGoldFlightAnimation(msgData, finishedListener) {
        this.hideTimeTip();
        var dealer = this.getLocalPos(msgData["dealer"]);
        let others = msgData["others"];

        Tools.inst.setTimeout(() => {
            jx.each(others, (data, i) => {
                let localSide = this.getLocalPos(data["side"])
                let score = data["score"];
                if (localSide != dealer) {
                    if (score < 0) {
                        this.onBettingAnimation(localSide, dealer);
                    }
                }
            });
        }, 1500)

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

        }, 2500)

        if (finishedListener) {
            finishedListener();
        }
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

    onBtnLiangPai() {
        this.btnLiangPai.visible = false;
        this.getPlayer(0).showOutPokersAction();
        this.isLiangPai = true;
        NetHandlerMgr.netHandler.sendOnHasBullOrNot(2);
    }


    /*************************************************金币飞行动画相关的东西**************************************************/
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
            let gold = fairygui.UIPackage.createObject('G555', 'tb_gold').asImage;
            // gold.displayObject.loadImage("tb_gold.png");
            gold.setScale(0.8, 0.8)
            gold.setXY(startPosX, startPosY);
            this._view.addChild(gold);
            gold.parent.setChildIndex(gold, gold.parent.numChildren - 2);

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

    /*************************************************金币飞行动画相关的东西END**************************************************/

    // 游戏结束
    onGameEnd(msgData, finishedListener) {
        super.onGameEnd(msgData, finishedListener);
        this.isBalance = true;
        NetHandlerMgr.netHandler.sendReadyNextRound();
    }

    // 接收是否有牛
    onHasBullOrNot(msgData, finishedListener) {
        var data = msgData["data"][0];
        var side = data['side'];
        this.fanPaiList.push(side);
        var localSide = this.getLocalPos(side);

        var player = this.getPlayer(localSide);
        if (!player.isBullFinish()) {
            let bullInfo = data['info'];
            var bullnum = bullInfo['bullnum'];
            var tiles = data["handcards"];
            if (true || bullnum > 0) {
                var tiles4ten: Array<string> = bullInfo['tiles4ten'];
                var tiles4bull: Array<string> = bullInfo['tiles4bull']
                if (tiles4ten != null && tiles4bull != null) {
                    tiles = tiles4ten.concat(tiles4bull)
                }
            }

            let cb = () => {
                player.showBullStr(bullnum);
            }
            if (localSide != 0) {
                player.isBullFinishValue = true;
                player.showPokersAni(tiles, () => {
                    cb();
                })
            } else {
                cb();
                SoundMgrNiu.pokerHit();
            }
        }
        if (finishedListener) finishedListener();
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


    onDispose() {
        super.onDispose();
        GObjectPool.inst.clearPool();
    }
}