module G570 {
    import OperationManager = G560.fl.OperationManager;
    import cleanPlayerExit = G560.GMethod.cleanPlayerExit;
    import playerMgr = GControl.playerMgr;
    export let page: GPage;
    export class GPage extends G560.GPage {
        public rangPaicardnum: number = 0;
        public multiple: number = 1;
        private poolKey = 'G570Poker';
        constructor() {
            super("G560", "GS570", UILayer.GAME);
            page = this;
        }
        onCreated(data: any = null) {
            //加载真正的背景
            //   var url = ResourceMgr.RES_PATH + 'bg/bg2.jpg';
            //  Tools.inst.changeBackground(url, this._view.getChild('bg').asLoader);
            G560.Sound.playBGM();
            Control.build(this);
            Control.playerMgr.clear();
            Control.playerMgr.setSelfSeat();
            //预先把发牌动画的牌加到池里
            for (let j = 0; j < 34; j++) {
                GObjectPool.inst.removeItemToPool(this.poolKey, fairygui.UIPackage.createObject('G560', 'Poker3'));
            }
            Laya.stage.on(Laya.Event.KEY_DOWN, this, this.onKeyDown);
        }
        initGame(gameInfo) {
            var roomInfo = gameInfo["roomInfo"];
            //拼接数据-extend是打牌规则，服务器不发的话默认用这个
            roomInfo['extend'] = roomInfo['extend'] || "0,0,3,False,False";
            this.initGameInfo(gameInfo);
            Control.createPlayerMgr(gameInfo);
            this.initRoomInfo(roomInfo);
            let selfInfo = gameInfo['selfInfo'];
            this.initRule(roomInfo["extend"]);
            Control.playerSelf.handwall.MoveUpTip = this.onHandWallTipList.bind(this);
            //NetHandlerMgr.netHandler.gameManage("1:", this.onGMResult.bind(this));
        }
        onKeyDown(e: Event): void {
            if (TestMgr.IS_REAL_ACCOUNT) return;
            var keyCode: number = e["keyCode"];
            var Keyboard = Laya.Keyboard;
            switch (keyCode) {
                case Keyboard.A:
                    NetHandlerMgr.netHandler.gameManage("2:Lj2d2c2bAdAbQdTb9a8b7d6b5d5c5b5a", this.onGMResult.bind(this));
                    break;
                case Keyboard.B:
                    break;
                case Keyboard.G:
                    break;
                case Keyboard.M:
                    break;
                default:
                    console.log(keyCode)
                    break;
            }
        }
        initMsgListen() {
            super.initMsgListen();
            //串行消息处理
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_RANG_PAI, this.onRangPai.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_RANG_PAI_RESULT, this.onRangPaiResult.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_WAGER, this.onWager.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_WAGER_RESULT, this.onWagerResult.bind(this));
        }
        onSetStart(msgData, finishedListener) {
            //console.log('-onSetStart-', msgData);
            try {
                this.isStartGame = true;
                this.reset();
                Control.operationMgr.hide();
                Control.balanceView.hide();
                //为了游戏结束的时候玩家不要消失
                Method.cleanPlayerExit();
                // if(this.imgRuleTray != null)
                //     this.imgRuleTray.setVisible(false);

                //开始游戏局数加一
                Control.roominfo.currentRound++;
                Control.roominfo.gameStage = Method.GAME_STAGE.GAMING;
                Control.playerMgr.playerList.forEach(function (player) {
                    player.isReady = false;
                });
            } catch (e) { console.error(e); }
            finishedListener();
        }
        reset() {
            // console.log("--------pag-----reset");
            Control.playerMgr.reset();
            Control.operationMgr.reset();
            Control.roominfo.reset();
            Control.buttonMgr.reset();
            Control.balanceView.hide();

            this.lastCardPattern = null;
            this._resetPlayerData = null;
            this.posLastDiscardServer = null;
            this.Turnside = null;
            this.rangPaicardnum = 0;
            this.multiple = 1;

        }
        refreshInfo() {
            NetHandlerMgr.netHandler.refreshData(function (data, finishedListener) {
                try {
                    //console.log('refreshInfo', data);
                    if (data["result"]) {
                        // WaitingView.hide();
                        var originData = {
                            //缺失数据部分
                            landlordData: null,
                            lastActionedData: [],
                            playerBombData: [{ side: 0, bombCount: 0 }],
                            reason: null,
                            result: true,
                            robLandlord: null,
                            //已有数据部分
                            refreshData: data
                        };
                        var refreshData = originData['refreshData']['data'];
                        //基本游戏信息，只需要基本poker协议的refreshData的data里的gameInfo
                        var gameInfo = refreshData["gameInfo"];
                        //游戏房间信息，只需要基本协议的roomInfo
                        var roomInfo = gameInfo["roomInfo"];
                        //是否已经初始化过
                        try {
                            if (!Control.isPlayerMgrBuild) {
                                this.reset();
                                this.initGame(gameInfo);
                            } else
                                this.initRoomInfo(gameInfo["roomInfo"]);
                            //Control.roominfo.multiple = 0;
                            [0, 1].forEach(function (side) {
                                let player = Method.getPlayerServer(side);
                                player.scoreBalance = null;
                            })
                            this.onRefreshGameData(originData);
                        } catch (e) { console.error(e); }
                    }
                    else {
                        //退出房间
                    }
                    if (typeof finishedListener == 'function') finishedListener();
                } catch (e) { console.log(e) };
            }.bind(this));
            // WaitingView.show(gb.getText("refresh_roomInfo_tips"));
        }
        onGMResult(data) {
            var result = data["result"];
            var reason = data["reason"];
            if (result) {
                console.log("++++++++++++Set GM Success+++++++++++");
            } else {
                console.log("GM码设置失败");
            }
        }
        getDealCardList(card, side, list) {
            //自己是双，别人是单
            let hideDealList = [];
            let showDealList = [];
            let otherList = [];
            let length = list.length * 2
            // console.log(side, Control.playerSelf.side, "=========side");
            if (side == Control.playerSelf.side) {
                for (let i = 0; i < length; i++) {
                    if (i % 2 == 0) {
                        showDealList.push(list[i / 2]);
                        if (list[i / 2] == card) {
                            // console.log(card, "==============card");
                            hideDealList.push(card);
                        }
                        else
                            hideDealList.push('card_backface');
                    }
                    else {
                        showDealList.push('card_backface');
                        hideDealList.push('card_backface');
                        otherList.push('card_backface');
                    }
                }
            }
            else {
                let randcardside = Math.floor(Math.random() * (list.length - 1));
                //  console.log(randcardside, "===========randcardside");
                for (let i = 0; i < length; i++) {
                    if (i % 2 == 0) {
                        showDealList.push(list[i / 2]);
                        hideDealList.push('card_backface');
                    } else {
                        if (Math.floor(i / 2) == randcardside) {
                            showDealList.push(card);
                            otherList.push(card);
                            hideDealList.push(card);
                        }
                        else {
                            otherList.push('card_backface');
                            showDealList.push("card_backface");
                            hideDealList.push("card_backface");
                        }
                    }
                }
            }
            let data = {
                'hideDealList': hideDealList,
                "showDealList": showDealList,
                'selfList': list,
                'otherList': otherList,
            }
            // console.log(data, otherList.concat(), "============发牌数据")
            return data;
        }
        //发牌
        onDealCards(msgData, finishedListener) {
            Control.roominfo.gameStage = Method.GAME_STAGE.GIVE_TILE;
            try {
                let dealcard = () => {
                    let list = msgData['cards'];
                    let card = msgData['card'];//随机翻出的牌
                    let randomside = msgData['side'];//随机牌的位置
                    list = list.split(',');
                    list.sort(G560.fla.utils.sortCardFunc);
                    let data = this.getDealCardList(card, randomside, list);
                    let startScale = 0.6;
                    let dealTilespacing = 25;
                    // let during = G570.fl.Handwall.SHOW_EFFECT_DURING;
                    Control.playerSelf.handwall.update(list, Method.getLocalPos(Control.playerSelf.side), true, function () {
                        //if (typeof finishedListener == 'function') finishedListener();
                    });
                    Control.playerOther.handwall.update(data.otherList, Method.getLocalPos(Control.playerOther.side), true, function () {
                        //if (typeof finishedListener == 'function') finishedListener();
                    });
                    let during = G570.fl.Handwall.DEAL_CARDS_DURING;

                    let hideDealList = data['hideDealList'];
                    let CardList = [];
                    for (let i = 0; i < hideDealList.length; i++) {
                        let card = GObjectPool.inst.getItemFormPool(this.poolKey).asCom;
                        card.getChild('card').asCom.getChildAt(0).asLoader.url = G560.fl.Handwall.getCardPath(hideDealList[hideDealList.length - 1 - i]);
                        card.setScale(1, 1);
                        card.getChild('card').setScale(startScale, startScale);
                        card.getChild('card').setXY(0, 0);
                        let Ani = card.getTransition('moveAni');
                        Ani.setValue('startscale', startScale, startScale);
                        Ani.setValue('startpos', 0, 0);

                        let startPos = {
                            x: this.view.actualWidth / 2 + ((card.pivotX - 0.5) * card.actualWidth) - (dealTilespacing * (hideDealList.length - 1) / 2 + card.actualWidth) + dealTilespacing * i,
                            y: this._view.actualHeight / 2 + ((card.pivotY - 0.5) * card.actualHeight),
                        };
                        card.setXY(startPos.x, startPos.y);
                        this._view.addChild(card);
                        card.visible = false;
                        CardList.push(card);
                    }
                    let deletemoveCard = () => {
                        //console.log("========清除动画========");
                        for (let i = CardList.length - 1; i >= 0; i--) {
                            GObjectPool.inst.removeItemToPool(this.poolKey, CardList[i]);
                        }
                        Control.playerSelf.handwall.showCard();
                        Control.playerOther.handwall.showCard();
                        if (typeof finishedListener == 'function')
                            finishedListener();
                    }
                    //发牌动画
                    let DealCardAni = () => {
                        let showDealList = data['showDealList'];
                        let otherList = data['otherList'];
                        let dealTileDelta = 100;
                        //   let dealTileDuration = 500
                        let intervalX = 25;
                        let intervalY = 20;
                        let middleindex = Math.floor(list.length / 2);
                        let selfmiddlepos = Control.playerSelf.handwall.getHandCardpos(middleindex);
                        let othermiddlepos = Control.playerOther.handwall.getHandCardpos(middleindex);
                        for (let i = 0; i < showDealList.length; i++) {
                            Laya.timer.once(dealTileDelta * i, this, (i) => {
                                let card: fairygui.GComponent = CardList[showDealList.length - 1 - i];
                                card.getChild('card').asCom.getChildAt(0).asLoader.url = G560.fl.Handwall.getCardPath(showDealList[i]);
                                let moveCardnum = showDealList.length / 2 - Math.floor((showDealList.length - 1 - i) / 2) - 1;
                                let player;
                                let enddata;
                                let moveAni = card.getTransition('moveAni');
                                let pos;
                                if (i % 2 == 0) {
                                    player = Control.playerSelf;
                                    enddata = selfmiddlepos;
                                    pos = card.globalToLocal(enddata.pos.x, enddata.pos.y);
                                    //card.getChild('card').asCom.getChildAt(0).asLoader.url = G560.fl.Handwall.getCardPath(list[moveCardnum]);
                                    // moveAni.setValue('endpos', pos.x + i  * intervalX, pos.y - intervalY);
                                    let index = i / 2;
                                    // if (index < middleindex)
                                    //     moveAni.setValue('endpos', pos.x, pos.y - intervalY);
                                    // else
                                    moveAni.setValue('endpos', pos.x + (index) * intervalX, pos.y - intervalY);
                                }
                                else {
                                    player = Control.playerOther;
                                    enddata = othermiddlepos;
                                    pos = card.globalToLocal(enddata.pos.x, enddata.pos.y);
                                    // card.getChild('card').asCom.getChildAt(0).asLoader.url = G560.fl.Handwall.getCardPath(otherList[moveCardnum]);
                                    //  moveAni.setValue('endpos', pos.x + i * intervalX, pos.y + intervalY);
                                    let index = i / 2;
                                    // if (index < middleindex)
                                    //     moveAni.setValue('endpos', pos.x, pos.y + intervalY);
                                    // else
                                    moveAni.setValue('endpos', pos.x + (index) * intervalX, pos.y + intervalY);
                                }
                                moveAni.setValue('startpos', 0, 0);

                                moveAni.setValue('startscale', startScale, startScale);
                                moveAni.setValue('endscale', enddata.scale, enddata.scale);
                                G560.Sound.playDealCard();
                                let carddata = player.handwall.getHandCardpos(moveCardnum);
                                let cardendpos = card.globalToLocal(carddata.pos.x, carddata.pos.y);
                                //console.log(cardendpos, "============cardendpos");
                                card.asCom.parent.setChildIndex(card, card.parent.numChildren - 1);
                                moveAni.play(
                                    new Handler(this, (i, enddata, pos, cardendpos, moveAni, card) => {

                                        let lineAni = card.getTransition('lineAni');
                                        if (i % 2 == 0) {
                                            let index = i / 2;
                                            // if (index < middleindex)
                                            //     lineAni.setValue('startpos', pos.x, pos.y - intervalY)
                                            // else
                                            lineAni.setValue('startpos', pos.x + (index) * intervalX, pos.y - intervalY);
                                        } else {
                                            let index = i / 2;
                                            // if (index < middleindex)
                                            //     lineAni.setValue('startpos', pos.x, pos.y + intervalY);
                                            // else
                                            lineAni.setValue('startpos', pos.x + (index) * intervalX, pos.y + intervalY);

                                        }
                                        //    lineAni.setValue('startpos', pos.x + (i - list.length) * intervalX, pos.y - intervalY);
                                        lineAni.setValue('endpos', cardendpos.x, cardendpos.y);
                                        lineAni.play(
                                            new Handler(this, (i) => {
                                                // console.log(i,"============i=")
                                                if (i == showDealList.length - 1) {
                                                    deletemoveCard();
                                                }
                                            }, [i])
                                        )
                                    }, [i, enddata, pos, cardendpos, moveAni, card])

                                )

                            }, [i]);

                        }
                    }

                    CardList.forEach((card, index) => {
                        Method.setTimeout(function () {
                            card.visible = true;
                            if (index == CardList.length - 1) {
                                //Anicard();
                                DealCardAni();
                            }
                            G560.Sound.playDealCard();
                        }, during * index);

                    })

                    //是否显示手牌计数
                    Control.playerSelf.isShowHandCount = false;
                    Control.playerOther.isShowHandCount = true;
                };
                this.reset();
                if (msgData["isReDeal"]) {
                    Control.effects.playRedeal(this, dealcard);//重新发牌
                    Control.roominfo.setfilpcards = false;
                } else {
                    dealcard();
                }

            } catch (e) {
                console.error(e);
            }
        }
        onPlayerAction(msgData, finishedListener) {
            // console.log('onPlayerAction', msgData);
            Control.roominfo.gameStage = Method.GAME_STAGE.GAMING;
            Control.operationMgr.hide();
            Control.playerMgr.clearCountdown();
            let isShowEffect = !msgData['instant'];
            let action = msgData["action"];
            var posServer = msgData["side"];
            var posLocal = Method.getLocalPos(posServer);
            let player = Method.getPlayerServer(posServer);
            player.handwall.resetOut();
            player.handwall.resetDisabled();
            if (G560.ACTION_TYPE.NO_DISCARD == action) {
                player.handwall.pass();
                if (isShowEffect)
                    G560.Sound.playPassSound(posLocal);
                if (typeof finishedListener == 'function') finishedListener();
            }
            else if (G560.ACTION_TYPE.DISCARD) {
                let cardDataList = msgData["datas"];
                let cardIdList = cardDataList[0].split(",");
                let wvValueList = null;
                if (cardDataList.length > 1)
                    wvValueList = cardDataList[1].split(",");
                // console.log("receive:" + cardIdList + "--" + wvValueList);
                //这里排序会影响癞子玩法
                cardIdList = cardIdList.concat().sort(G560.fla.utils.compareCard.bind(G560.fla.utils));
                var cardPattern = G560.fla.utils.getCardPattern(cardIdList, true, wvValueList);
                var data = {
                    cp1: cardPattern,
                    cp2: this.lastCardPattern,
                    pos1: posLocal,
                    pos2: Method.getLocalPos(this.posLastDiscardServer),
                    isShowEffect: isShowEffect,
                    discardList: cardIdList
                };
                player.discard(data, function () {
                    var handCardCount = player.handCount;
                    if (handCardCount == 1 || handCardCount == 2) {
                        if (isShowEffect) {
                            setTimeout(function () {
                                G560.Sound.playLeftCardSound(posLocal, handCardCount);
                            }, 400);
                        }
                        player.showAlarm();
                    }
                    if (finishedListener != null)
                        finishedListener();
                });
                this.lastCardPattern = cardPattern;
                this.posLastDiscardServer = posServer;
            }
        }
        onPlayerTurn(msgData, finishedListener?) {
            try {
                //console.log('onPlayerTurn', msgData);
                Control.roominfo.gameStage = Method.GAME_STAGE.GAMING;
                let posServer = msgData['side'];
                let posLocal = Method.getLocalPos(posServer);
                let player = Method.getPlayer(posLocal);
                player.handwall.resetOut();
                Control.playerMgr.clearCountdown();
                this.Turnside = posServer;
                if (Control.posServerSelf == posServer) {
                    this.myTurnNum = msgData["num"];
                    //开始计算应该显示哪些按钮
                    this.showPlayButton(msgData);
                } else {
                    Control.operationMgr.hide();
                    Control.playerMgr.setCountdown(Method.getLocalPos(msgData['side']), 15);
                }
                if (typeof finishedListener == 'function') return finishedListener();
            } catch (e) { console.error(e); }
        }
        //-----------金币场
        onGoldRoomInfo(msgData) {
            if (msgData['gamenumber'])
                Control.roominfo.roomId = msgData['gamenumber'];
            Control.roominfo.roomSetting = ExtendMgr.inst.getText4Language(msgData['info']) + " " + ExtendMgr.inst.getText4Language("底分：") + Tools.inst.changeGoldToMoney(msgData['gold']);
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }
        onRefreshGameData(data) {
            //  console.log('onRefreshGameData', data);
            //已有数据部分
            let refreshData = data['refreshData']['data'];
            var playerDataList = refreshData["playerDatas"];
            let baseRefreshData = data["refreshData"]["data"];
            var stage = baseRefreshData["stage"];
            //更改房间状态
            Control.roominfo.gameStage = stage;
            // console.log(Control.roominfo.gameStage, "=========断线后的游戏状态");
            //钩子函数触发
            var hookActive = jx.once(this, function () {
                //钩子函数触发点-重连
                Method.checkRefreshGameData(data);
            });
            //尝试恢复玩家数据-在线
            jx.each(playerDataList, function (playerData) {
                let posServer = playerData["side"];
                let isOnline = playerData["isOnline"];
                let player = Method.getPlayerServer(posServer);
                if (player)
                    player.onine = isOnline;
            }, this);
            //尝试恢复玩家数据-个人信息
            var _d;
            var playerList = (_d = baseRefreshData['gameInfo']) && (_d = _d['roomInfo']) && (_d['playerList']);
            //console.log('尝试恢复玩家数据-个人信息', playerList);
            if (playerList) {
                playerList.forEach(function (oneData) {
                    let player = Method.getPlayerServer(oneData['side']);
                    if (player) {
                        player.update(oneData);
                    }

                })
            }
            //检查是否要发送准备
            //避免重连时发准备
            // if(stage == Method.GAME_STAGE.WAIT_START || stage == Method.GAME_STAGE.GAME_READY){
            if (stage == Method.GAME_STAGE.WAIT_START) {
                this.doSelfReady(true);
            }
            //玩家数据恢复因为要等另一条协议，所以暂时不执行
            this._resetPlayerData = jx.once(this, function (extendData) {
                // console.log("-玩家数据恢复-异步后数据", data, extendData);
                let refreshData = data['refreshData']['data'];
                //-------恢复数据结构
                data['landlordData'] = extendData['landlordData'];
                data['lastActionedData'] = extendData['lastActionedData'];
                data['num'] = extendData['num'];
                data['playerBombData'] = extendData['playerBombData'];
                data['playerRestoreData'] = extendData['playerRestoreData'];
                data['robLandlord'] = extendData['robLandlord'];
                //--------修改重连数据
                // Control.playerOther.forEach(player => {
                //     player.isShowHandCount = true;
                // })
                Control.playerOther.isShowHandCount = true;
                //玩家手牌数据
                refreshData.playerDatas.forEach(function (oneData, idx) {
                    //手牌数据
                    let _c;
                    oneData['cardDatas'] = (_c = extendData.playerRestoreData) && _c[idx]['cardDatas'];

                });
                //出牌数据
                refreshData['lastActionedData'] = extendData.lastActionedData;
                //重构 allowAction 数据
                if (extendData['num'] === null) {
                    refreshData['allowAction'] = null;
                } else {
                    refreshData['allowAction'] = {
                        action: [],
                        num: extendData['num'],
                        side: extendData['actionSide']
                    }
                }
                //--------开始恢复数据
                //console.log('开始恢复数据', data);
                var baseRefreshData = data["refreshData"]["data"];
                var gameRefreshData = data["landlordData"];
                var stage = baseRefreshData["stage"];
                //钩子函数触发
                hookActive();
                Control.operationMgr.hide();
                if (stage == Method.GAME_STAGE.WAIT_START) {
                    if (!Control.roominfo.isGameStart()) {
                        this.checkAutoStart();
                    }
                    return;
                }
                //入场或者重连先发一次下一局
                if (stage == Method.GAME_STAGE.GAME_READY) {
                    // fl.netHandler.sendReadyNextRound();
                    return;
                }
                //倒计时
                var posCurrentServer = baseRefreshData["currentSide"];
                var posCurrentLocal = Method.getLocalPos(posCurrentServer);
                Control.playerMgr.setCountdown(posCurrentLocal);
                //炸弹数
                var bombDataList = data["playerBombData"];
                jx.each(bombDataList, function (bombData) {
                    let player = Method.getPlayerServer(bombData["side"]);
                    player.boomCount = bombData["bombCount"];
                }, this);
                var robLandlord = data["robLandlord"];
                if (robLandlord != null) {
                    this.onPlayerRobLandlord(robLandlord);
                }
                var playerContentList = [{}, {}, {}];
                var lastActionedData = data["lastActionedData"];
                jx.each(lastActionedData, function (actionData, i) {
                    var isRobLandlord = actionData["isRobLandlord"];
                    var posLocal = Method.getLocalPos(actionData["side"]);
                    var content = playerContentList[posLocal];
                    if (gameRefreshData == null) {
                        //抢叫地主流程恢复
                        var callType = actionData["callType"];
                        var callData = actionData["callData"];
                        var actionTipsId = null;
                        switch (callType) {
                            //叫地主
                            case 0:
                                actionTipsId = callData == 0 ? Method.Player.TIPS_ID_NO_CALL : Method.Player.TIPS_ID_CALL;
                                break;
                            //叫分
                            case 1:
                                if (callData == 0)
                                    actionTipsId = Method.Player.TIPS_ID_NO_CALL;
                                else
                                    actionTipsId = callData;
                                break;
                            //抢地主
                            case 2:
                                actionTipsId = callData == 0 ? Method.Player.TIPS_ID_NO_ROB : Method.Player.TIPS_ID_ROB;
                                break;
                        }
                        content["tips"] = actionTipsId;
                    }
                    if (actionData["cards"] != null) {
                        var outCards = actionData["cards"]
                            && actionData["cards"][0];
                        switch (outCards) {
                            case 'pass':
                                content["tips"] = Method.Player.TIPS_ID_NO_DISCARD;
                                break;
                            case "never":
                                break;
                            case "":
                                break;
                            default:
                                content["out"] = outCards.split(',');
                                var wvValueList = actionData["usedWildCards"];
                                if (wvValueList != null)
                                    content["wildcard"] = wvValueList.split(",");
                                break;
                        }
                    }
                });
                if (gameRefreshData != null) {
                    //显示地主拿到的三张牌
                    var cardIdList = gameRefreshData["holeCards"] && gameRefreshData["holeCards"].split(",");
                    if (cardIdList != null && cardIdList != '')
                        Control.roominfo.holeCards = cardIdList
                    if (fl.isWildcardMode) {
                        var wildcardId = G560.fla.utils.transferWildCardTo(gameRefreshData["wildCard"][0]);
                        G560.fla.utils.setWildcard(wildcardId);
                        // this.setWildcard(wildcardId);
                    }
                    this.multiple = gameRefreshData["multiple"];
                    this.rangPaicardnum = gameRefreshData['rangPaiCnt'];
                    Control.roominfo.multiple = gameRefreshData["multiple"];
                    Control.roominfo.information = gameRefreshData['rangPaiCnt'];
                    //显示庄家手牌标识
                    if (gameRefreshData['landlordSide'] == Control.posServerSelf) {
                        Control.playerSelf.handwall.isDealer = true;
                    }
                    var dealerLocal = Method.getLocalPos(gameRefreshData["landlordSide"]);
                    var playerCount = Control.playerMgr.playerList.length;
                    for (var posLocal = 0; posLocal < playerCount; ++posLocal) {
                        var isDealer = dealerLocal == posLocal;
                        let player = Method.getPlayer(posLocal);
                        player.isDealer = isDealer;
                        player.clearActionTips();
                    }
                    this.lastCardPattern = null;
                    this.posLastDiscardServer = null;
                    var posTurnLocal = Method.getLocalPos(baseRefreshData["currentSide"]);
                    this.Turnside = baseRefreshData["currentSide"];
                    for (var i = 1; i < playerCount; ++i) {
                        var posLocal = (posTurnLocal - i + playerCount) % playerCount;
                        var content = playerContentList[posLocal];
                        var outCards = content["out"];
                        if (outCards != null) {
                            this.lastCardPattern = G560.fla.utils.getCardPattern(outCards, content["wildcard"]);
                            this.posLastDiscardServer = Method.getServerPos(posLocal);
                            break;
                        }
                    }
                }
                //console.log('最终组装的玩家重连数据', playerContentList);
                jx.each(playerDataList, function (playerData, i) {
                    try {
                        var posServer = playerData["side"];
                        var posLocal = Method.getLocalPos(posServer);
                        var content = playerContentList[posLocal];
                        content["hand"] = playerData["cardDatas"][0].split(",");
                        if (posLocal != 0) {
                            for (var j = 0; j < content['hand'].length; j++) {
                                if (content['hand'][j] == '') {
                                    content['hand'][j] = 'card_backface';
                                }
                            }
                        }
                        Method.getPlayer(posLocal).setContent(content);
                    } catch (e) {
                        console.error(e);
                    }
                }, this);
                var turnAction = baseRefreshData["allowAction"];
                if (turnAction != null && robLandlord == null)
                    this.onPlayerTurn(turnAction);
                Control.playerSelf.handwall.cardsEnabled = true;
            })
            //如果0.1s后没有收到补充数据，那么用现有数据调用一次
            Laya.timer.once(0.1, this, function () {
                //钩子函数触发
                hookActive();
            })
        }
        updatePlayerBoomMultiple(msgData) {

            //  setTimeout(function () {
            if (msgData['multiple']) {
                Control.playerMgr.playerList.forEach(player => {
                    //player.boomMultiple = msgData['multiple'];
                    this.multiple = msgData['multiple'];
                    Control.roominfo.multiple = this.multiple;
                    // console.log(this.multiple, "=============炸弹");
                })
            }
            let bombInfo = msgData['playerBombData'];
            if (bombInfo) {
                let player = Method.getPlayerServer[bombInfo['side']];
                if (player)
                    player.boomCount = bombInfo['bombCount'] != null ? bombInfo['bombCount'] : player.boomCount;
            }
            //}.bind(this))

            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }
        showServerCountDown(msgData) {
            let sides = msgData['sides'];
            let waitTime = msgData['wait_time'];
            let side = sides.length > 1 ? 0 : (sides[0] || 0);
            let stage = msgData['stage'];
            Control.playerMgr.setCountdown(Method.getLocalPos(side), waitTime);
            //console.log(stage, "=============stage");
            if (stage == 'call_landlord')//叫地主
            {

            } else if (stage == 'rob_landlord') {//抢地主

            } else if (stage == "rang_pai") {//让牌
                // let isSelfTurn = Control.playerSelf.side == side;
                // let choice = [0, 2, 3, 4];
                // if (isSelfTurn) {
                //     let operationName = Control.operationMgr.show('letcard', function (idx, btn) {
                //         Control.operationMgr.hide();
                //         NetHandlerMgr.netHandler.sendRANGPAI(choice[idx]);
                //     });
                // }
            } else if (stage == 'wager') {
                //加倍

            }

            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }
        // //0:叫地主，1:叫分， 2:抢地主
        onPlayerRobLandlord(msgData, finishedListener?) {
            //console.log('onPlayerRobLandlord', msgData);
            // console.log(Control.roominfo.gameStage, "=========游戏状态");
            try {
                let isSelfTurn = Control.playerSelf.side == msgData['side'];
                let _c;
                // console.log(Control.playerSelf.isLandlord, _c, "========== Control.playerSelf.isLandlord");
                let canShow = (_c = Control.playerSelf.isLandlord) == null || _c === 0;
                let countTime = 15;
                Control.playerMgr.setCountdown(Method.getLocalPos(msgData['side']), countTime);
                var type = msgData['choseType'];
                let operate = msgData['operate'];
                let player = Method.getPlayer(Method.getLocalPos(msgData['side']));
                player.hidetge();
                //中间三张牌
                Control.roominfo.setfilpcards = true;
                player.hidetge();
                if (isSelfTurn) {
                    if (canShow) {
                        var canChooseScore = msgData['canChooseScore'];
                        let operationName;
                        if (type == 0) {
                            operationName = Control.operationMgr.show('landlord2', function (idx, btn) {
                                Control.operationMgr.hide();
                                // console.log(type, idx, "==========发送sendRob");
                                NetHandlerMgr.netHandler.sendRob(type, idx);
                            });
                        }
                        else if (type == 2) {
                            operationName = Control.operationMgr.show('callLandLord', function (idx, btn) {
                                Control.operationMgr.hide();
                                //console.log(type, idx, "==========发送sendRob");
                                NetHandlerMgr.netHandler.sendRob(type, idx);
                            });

                        }
                    }
                } else {
                    this.showTableTips(ExtendMgr.inst.getText4Language("请等待其他玩家抢地主"));
                }
            } catch (e) {
                console.error(e);
            }
            if (typeof finishedListener == 'function') finishedListener();
        }
        //叫地主/叫分/抢地主 操作的结果
        onPlayerRobResult(msgData, finishedListener) {
            // console.log('S_C_RobLandlordResult', msgData);
            if (Control.roominfo.gameStage == Method.GAME_STAGE.GIVE_TILE || Control.roominfo.gameStage == Method.GAME_STAGE.GAMING) {
                Control.operationMgr.hide();
                var isShowEffect = !msgData.instant;
                let player = Method.getPlayerServer(msgData['side']);
                let type = msgData["choseType"];
                let operate = msgData["operate"];
                player.hidetge();
                this.rangPaicardnum = msgData['rangPaiCnt'];
                if (this.rangPaicardnum > 0) {
                    this.multiple = Math.pow(2, this.rangPaicardnum);
                    Control.roominfo.multiple = this.multiple;
                    Control.roominfo.information = this.rangPaicardnum;
                }
                //确定地主
                let isConfirmLandlord = msgData['isConfirmLandlord'];
                //显示标识
                if (!isConfirmLandlord) {
                    switch (type) {
                        case G560.CALL_TYPE.CALL_LANDLORD:
                            let isLandLord2 = operate;
                            player.isLandLord2 = isLandLord2;
                            break;
                        case G560.CALL_TYPE.ROB_LANDLORD:
                            let callLandLord = operate;;
                            // console.log(player, callLandLord, "==========callLandLord");
                            player.setcallLandLord(callLandLord);
                            break;
                    }
                }
                if (isConfirmLandlord) {
                    //禁用手牌
                    Control.playerSelf.handwall.cardsEnabled = false;
                    let landlordData = msgData["landlordData"];
                    var serverSide = landlordData['landlordSide'];
                    var dealerLocal = Method.getLocalPos(serverSide);
                    let gameData = msgData['landlordData'];
                    let holeCards = gameData["holeCards"] && gameData["holeCards"].split(",");
                    this.rangPaicardnum = landlordData['rangPaiCnt'];
                    this.multiple = landlordData['multiple'];
                    Control.roominfo.multiple = landlordData['multiple'];
                    Control.roominfo.information = this.rangPaicardnum;
                    //底分
                    Control.roominfo.baseScore = landlordData['baseScore'];

                    //地主牌数变更
                    var dealerPlayer = Method.getPlayer(dealerLocal);
                    dealerPlayer.handCount = parseInt(dealerPlayer.handCount) + 3
                    //地主牌
                    Control.roominfo.holeCards = holeCards;
                    if (holeCards != null && holeCards.length > 0) {
                        holeCards.sort(G560.fla.utils.sortCardFunc);
                        let filpcards = this._view.getChild('filpcards').asCom;
                        Control.roominfo.setfilpcards = true;
                        let filpAni = filpcards.getTransition('filpAni');
                        let startposlist = [];
                        let scale = filpcards.getChildAt(0).asCom.scaleX;
                        filpAni.setHook('showcard', Handler.create(this, () => {
                            for (let i = 0; i < holeCards.length; i++) {
                                let card = filpcards.getChildAt(i).asCom;
                                card.getChild("n0").asLoader.url = G560.fl.Handwall.getCardPath(holeCards[i]);
                                startposlist.push([card.x, card.y]);
                            }
                        }, [], true));
                        let temp = player.handwall.getAddCardPos(holeCards);
                        let poslist: Array<{ x: number, y: number }> = temp.posList;
                        let indexs: Array<number> = temp.addCardsIndex;
                        let card_posAni = filpcards.getTransition('card_posAni');
                        let endscale = player.handwall.gethandpokerscale();
                        if (dealerLocal != Control.posLocalSelf) {
                            card_posAni.setHook('showcard_backface', Handler.create(this, () => {
                                Control.roominfo.setfilpcards = true;
                            }, [], true))
                        }
                        filpAni.play(new Handler(this, function () {
                            player.hidetge();
                            for (let i = 0; i < holeCards.length; i++) {
                                let card = filpcards.getChildAt(i).asCom;
                                let name = 'card' + i + "_endpos";
                                let scalename = 'card' + i + '_scale';
                                let pos = filpcards.globalToLocal(poslist[i].x, poslist[i].y);
                                card_posAni.setValue(name, pos.x, pos.y);
                                card_posAni.setValue(scalename, endscale, endscale);
                            }
                            // player.handwall.HandpokeMovePos(holeCards);
                            player.handwall.RobMoveHandCards(indexs);
                            card_posAni.play(new Handler(this, function () {
                                //复原
                                player.handwall.HandPokerRecoverypos();
                                for (let i = 0; i < holeCards.length; i++) {
                                    let card = filpcards.getChildAt(i).asCom;
                                    card.x = startposlist[i][0];
                                    card.y = startposlist[i][1];
                                    card.scaleX = scale;
                                    card.scaleY = scale;
                                }
                                Control.roominfo.setfilpcards = false;
                                if (dealerLocal == Control.posLocalSelf) {
                                    //如果自己事地主，把牌加进入手牌
                                    Control.playerSelf.handwall.addCard(holeCards);
                                    //让牌竖起
                                    Control.playerSelf.handwall.setCardsActive(holeCards);
                                }
                                else {
                                    let cardbacklist = []
                                    for (let i = 0; i < holeCards.length; i++) {
                                        cardbacklist.push("card_backface");
                                    }
                                    player.handwall.addCard(cardbacklist)
                                }
                                let otherplayerLsit = [];
                                for (let i = 0; i < Control.playerOther.handCount; i++) {
                                    otherplayerLsit.push('card_backface');
                                }
                                Control.playerOther.handwall.update(otherplayerLsit)
                            }))
                        }));
                    }
                    // console.log(holeCards, "========地主牌")
                    if (dealerLocal == Control.posLocalSelf) {
                        Control.playerSelf.handwall.resetSelected();
                        //如果自己事地主，显示标识
                        Control.playerSelf.handwall.isDealer = true;
                    }
                    //地主标识
                    Control.playerMgr.playerList.forEach(function (player) {
                        let isDealer = player.side == serverSide;
                        player.isDealer = isDealer;
                        if (!isDealer) {
                            player.isLandLord = null;
                        }
                    });

                }
            }
            if (finishedListener != null)
                finishedListener();
        }
        //让牌的选择 choice [0, 2, 3, 4] 0：为不让牌
        onRangPai(msgData, finishedListener) {

            let rangPaiInfo = msgData['rangPaiInfo'];
            for (let i = 0; i < rangPaiInfo.length; i++) {
                let isSelfTurn = Control.playerSelf.side == rangPaiInfo[i]['side'];
                let choice = rangPaiInfo[i]['choice'];
                // console.log(msgData, "=====onRangPai======");
                if (isSelfTurn) {
                    //  console.log("======onRangPai======");
                    let operationName = Control.operationMgr.show('letcard', function (idx, btn) {
                        Control.operationMgr.hide();
                        // console.log(choice[idx], "==========发送sendRANGPAI");
                        NetHandlerMgr.netHandler.sendRANGPAI(choice[idx]);
                    });
                }
            }
            if (finishedListener != null)
                finishedListener();
        }
        //加倍选择 choice 1：不加倍 2：加倍
        onWager(msgData, finishedListener) {
            let wagerInfo = msgData['wagerInfo'];
            for (let i = 0; i < wagerInfo.length; i++) {
                let choice = wagerInfo[i]['choice'];
                if (Control.playerSelf.side == wagerInfo[i]['side']) {
                    // console.log("=====onWager========")
                    let operationName = Control.operationMgr.show('jiabei', function (idx, btn) {
                        Control.operationMgr.hide();
                        // console.log(choice[idx], "==========发送sendWager");
                        NetHandlerMgr.netHandler.sendWager(choice[idx]);
                    });
                }
            }
            Control.playerSelf.handwall.resetSelected();
            if (finishedListener != null)
                finishedListener();
        }
        //让牌结果
        onRangPaiResult(msgData, finishedListener) {
            let rangPaiInfo = msgData['rangPaiInfo'];
            for (let i = 0; i < rangPaiInfo.length; i++) {
                let choice = rangPaiInfo[i]['choice'];
                let player = Method.getPlayerServer(rangPaiInfo[i]['side']);
                player.letcard = choice;
                this.rangPaicardnum += parseInt(choice);
                Control.roominfo.information = this.rangPaicardnum;
                if (choice == 2) {
                    this.multiple = this.multiple * 4;
                    Control.roominfo.multiple = this.multiple;
                }
                if (Control.playerSelf.side == rangPaiInfo[i]['side']) {
                    //对方的牌变灰
                    //  Laya.timer.frameOnce(2, this, () => {
                    Control.playerOther.handwall.grayHandPoker(this.rangPaicardnum);
                    // });、、
                    Control.playerSelf.handwall.resetSelected();
                }
            }

            if (finishedListener != null)
                finishedListener();
        }
        //加倍结果
        onWagerResult(msgData, finishedListener) {
            let wagerInfo = msgData['wagerInfo'];
            for (let i = 0; i < wagerInfo.length; i++) {
                let choice = wagerInfo[i]['choice'];
                let player = Method.getPlayerServer(wagerInfo[i]['side']);
                player.isDouble = choice;
                if (choice == 2) {
                    // console.log(this.multiple, "=========this.multiple");
                    this.multiple = this.multiple * 2;
                    Control.roominfo.multiple = this.multiple;
                }
                Laya.timer.once(5000, this, function () {
                    player.hidetge();
                })
            }
            Control.playerSelf.handwall.resetSelected();

            if (finishedListener != null)
                finishedListener();
        }
        onPlayerDiscard() {
            let cardIdList = Control.playerSelf.handwall.getSelectedData();
            //没有选择牌
            if (cardIdList.length == 0) {
                return this.showTileTips(G560.getText('discard_error_tips1'));
            }
            //------函数定义
            //隐藏选项
            Control.operationMgr.hide();
            //------开始判断流程
            //检查牌是否符合规则
            cardIdList = cardIdList.sort(G560.fla.utils.sortCardFunc);
            var cpList = this.getAvailableCpList(cardIdList);
            //console.log('playerDiscard', cardIdList, cpList);
            if (cpList == null || cpList.length == 0) {
                //不符合规则
                this.showTileTips(G560.getText("discard_error_tips2"));
                // console.log("=======onPlayerDiscard===========");
                Control.operationMgr.show();
            }
            else if (cpList.length == 1) {
                NetHandlerMgr.netHandler.sendAction(G560.ACTION_TYPE.DISCARD, cpList[0].getActionData(), this.myTurnNum);
            }
            else {
                //console.log('因为有癞子，所以有多种组合，暂未完成界面', cpList);
            }
        }
        saveBalanceAddition(msgData) {
            // console.log('小结补充数据', msgData);
            this._getBalanceAddition = jx.once(this, function (data) {
                var _d;
                data['gameCommonDatas'] = [];
                data['gameCommonDatas'][0] = {};
                data['gameCommonDatas'][0]["extendData"] = (_d = msgData) && _d['extendData'];
                data['gameCommonDatas'][0]["datas"] = ExtendMgr.inst.getText4Language((_d = msgData) && _d['datas']);
                data['leftCards'] = (_d = msgData) && _d['leftCards'];
                // console.log(data['leftCards'], "===========data['leftCards'] ");
                return data
            })
        }

        onGameEnd(msgData, finishedListener) {
            //console.log('onGameEnd', msgData);
            //单局结算数据
            var setData = msgData["setUserDatas"];
            var self = this;
            //补充数据
            //console.log(this._getBalanceAddition, "==========_getBalanceAddition");
            if (this._getBalanceAddition) {
                this._getBalanceAddition(msgData);
            }
            //没有数据，说明服务器踢人
            // if(
            //     msgData['setUserDatas']
            //     && msgData['setUserDatas'].length == 0
            //     && msgData['gameUserDatas']
            //     && msgData['gameUserDatas'].length == 0
            // )this.onExitRoom(true);
            //-----函数定义
            //小结
            var showView = function (msgData) {
                // Control.roominfo.gameStage = Method.GAME_STAGE.GAME_READY;
                //清除桌面資源
                self.reset();
                //8秒后再显示小结
                self.showBalance(msgData);
                if (finishedListener != null)
                    finishedListener();
            }.bind(this, msgData);
            //展示手牌
            var showOtherHand = function () {
                // console.log("========showOtherHand======");
                //清空手牌 和出牌
                Control.playerSelf.handwall.resetHand();
                Control.playerOther.handwall.resetHand();
                Control.playerSelf.handwall.resetOut();
                Control.playerOther.handwall.resetOut();
                msgData['setUserDatas'] && msgData['setUserDatas'].forEach(oneData => {
                    let player = Method.getPlayerServer(oneData['side']);
                    //console.log(player);
                    //结算分动画
                    player.scoreBalance = parseFloat(oneData['score']);
                    //计算玩家分数
                    player.score = parseFloat(player.score) + parseFloat(oneData['score']);
                    let tiles = oneData['tiles'] && oneData['tiles'][0] && oneData['tiles'][0].split(',');
                    if (player && tiles) {
                        tiles.sort(G560.fla.utils.sortCardFunc);
                        if (oneData['side'] == Control.playerSelf.side) {
                            //  console.log(tiles, "==========1111111111")
                            player.handwall.out(tiles);
                        }
                        else {
                            // console.log(tiles, "==========222222222")
                            Control.playerOther.handwall.update(tiles, 1);
                        }
                    }
                });

                let leftCardsList = msgData['leftCards'];
                // console.log(leftCardsList, "===========leftCardsList");
                if (leftCardsList != null) {
                    //  console.log(leftCardsList, "=================leftCardsList");
                    leftCardsList.sort(G560.fla.utils.sortCardFunc)
                    // Control.playerOther.handwall.update(leftCardsList, 1);
                    //最后九张放在中间
                    Control.playerOther.handwall.out(leftCardsList);
                }
            }.bind(this);
            //先展示手牌，再到小结
            let showResult = function () {
                let delayTime = 4;
                // showOtherHand();
                Laya.timer.once(1000, this, showOtherHand);
                Control.playerMgr.setCountdown(Control.posLocalSelf, delayTime, showView)
            }.bind(this);
            if (msgData["instant"]) {
                //  showOtherHand();
                Laya.timer.once(1000, this, showOtherHand);
                showView();/**/
            } else {
                //有动画
                //春天表现
                var springData = null;
                var gameCommonDatas = msgData["gameCommonDatas"];
                if (gameCommonDatas != null && gameCommonDatas.length > 0)
                    springData = gameCommonDatas[0]["extendData"];
                if (springData != null && springData.length > 0) {
                    if (springData[0] == 1)//春天
                    {
                        // console.log(this.multiple, "==========春天");
                        this.multiple = this.multiple * 2;
                        Control.roominfo.multiple = this.multiple;
                        this.showSpring(showResult);
                    }
                    else if (springData[0] == 2)//反春
                    {
                        //   console.log(this.multiple, "==========反春天");
                        this.multiple = this.multiple * 2;
                        Control.roominfo.multiple = this.multiple;
                        this.showAntiSpring(showResult);
                    }
                    else
                        showResult();
                }
                else
                    showResult();
            }
            // this.reset();
            // return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }
        onDispose() {
            GObjectPool.inst.clearPool();
            this.stopPoll();
            Control.destory();
            Laya.stage.off(Laya.Event.KEY_DOWN, this, this.onKeyDown);
            if (NetHandlerMgr.netHandler != null && NetHandlerMgr.netHandler.valid()) {
                NetHandlerMgr.netHandler.disconnect();
            }
            Laya.timer.clearAll(this);
        }
        //得到顺子
        onHandWallTipList(cardlist: Array<string>) {
            //console.log(cardlist, this.Turnside, Control.posServerSelf, this.posLastDiscardServer, "=========得到顺子");
            if (cardlist == null || cardlist.length < 2)
                return false;
            //如果没有出牌人的数据或者上一个出牌人是自己，说明允许出所有牌
            if (this.posLastDiscardServer == null || this.posLastDiscardServer == Control.posServerSelf) {
                if (this.Turnside == Control.posServerSelf) {
                    let list = G560.fla.utils.getSequence(cardlist);
                    if (list != null && list.length > 0) {
                        Control.playerSelf.handwall.setCardsActive(list);
                        return true;
                    }
                    else
                        return false;
                }
                else
                    return false;
            }
            else {
                //通过算法计算是否有可以出的牌
                var tipsObjList = G560.fla.utils.getGreaterList(this.lastCardPattern, Control.playerSelf.handwall.getDataList());
                if (tipsObjList == null || tipsObjList.length == 0) {
                    // return false;
                    //若有顺子，提示顺子
                    let list = G560.fla.utils.getSequence(cardlist);
                    if (list != null && list.length > 0) {
                        Control.playerSelf.handwall.setCardsActive(list);
                        return true;
                    }
                    else
                        return false;
                } else {
                    //return tipsObjList;
                    // console.log(tipsObjList, '=======提示内容')
                    let cardIdList = cardlist.concat();
                    for (let i = 0; i < tipsObjList.length; i++) {
                        let tiplist = tipsObjList[i];
                        let isup = false;
                        for (let j = 0; j < tiplist.length; j++) {
                            let indexOf = cardIdList.indexOf(tiplist[j]);
                            if (indexOf == -1) {
                                isup = false;
                                break;
                            }
                            else {
                                isup = true;
                                cardIdList.splice(indexOf, 1);
                            }
                        }
                        if (isup) {
                            if (!tiplist.isSorted) {
                                tiplist.sort(G560.fla.utils.sortCardFunc);
                                tiplist.isSorted = true;
                            }
                            //  console.log(tiplist, "========升起的牌");
                            Control.playerSelf.handwall.setCardsActive(tiplist);
                            return true;
                        }
                    }
                }
            }
        }

    }

}