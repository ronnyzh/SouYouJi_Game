/*
 * name;
 */
module G559 {
    import roominfo = G559.rf.roominfo;
    export let page: GPage;
    export class GPage extends Page {
        public isStartGame;
        public buttonsHandler;
        public currentRound;
        public lastCardPattern;
        public _resetPlayerData;
        public _resetPlayerDataAfter;
        public posLastDiscardServer;
        public myTurnNum;
        public lastBalanceData;
        public doubleData: Array<any> = [];
        public Turnside;//出牌位置

        constructor() {
            super("G559", "GameScene", UILayer.GAME);
            page = this;
        }


        onCreated(data: any = null) {
            //加载真正的背景
            // var url = ResourceMgr.RES_PATH + 'bg/bg4.jpg';
            //  Tools.inst.changeBackground(url, this._view.getChild('bg').asLoader);
            //背景音乐
            Sound.playBGM();

            Control.build(this);
            Control.playerMgr.clear();
            Control.playerMgr.setSelfSeat();
            this.doubleData = [];
        }

        onNetIntoGame(data) {
            let result = data['result'];
            if (result) {
                //Control.build(this);
                this.onEnterRoomSuccess(data)
            } else {
                Alert.show(ExtendMgr.inst.getText4Language(data['reason']), false)
                    .onYes(this.onExitRoom.bind(this, true))
            }
        }

        onEnterRoomSuccess(data) {
            var gameInfo = data["myInfo"];
            this.startPoll();
            //断线重连，请求当前游戏数据
            if (gameInfo["isRefresh"])
                this.refreshInfo();
            else {
                this.initGame(gameInfo);
                this.doSelfReady(true);
            }
        }

        refreshInfo() {
            NetHandlerMgr.netHandler.refreshData(function (data, finishedListener) {
                try {
                    //console.log('refreshInfo', data);
                    if (data["result"]) {
                        // WaitingView.hide();

                        var refreshData = data["data"];
                        //基本游戏信息，只需要基本poker协议的refreshData的data里的gameInfo
                        var gameInfo = refreshData["gameInfo"];
                        //游戏房间信息，只需要基本协议的roomInfo
                        var roomInfo = gameInfo["roomInfo"];

                        //是否已经初始化过
                        if (!Control.isPlayerMgrBuild) {
                            this.reset();
                            this.initGame(gameInfo);
                        }
                        else {

                            this.initRoomInfo(gameInfo["roomInfo"]);
                        }
                        [0, 1, 2].forEach(function (side) {
                            let player = Method.getPlayerServer(side);
                            player.scoreBalance = null;
                            player.isDouble = null;
                        })

                        this.try(this.onRefreshGameData(refreshData));
                    }
                    else {
                        //退出房间
                    }
                    if (typeof finishedListener == 'function') finishedListener();
                } catch (e) { console.log(e) };
            }.bind(this));

            // WaitingView.show(gb.getText("refresh_roomInfo_tips"));
        }

        onRefreshGameData(data) {
            //console.log('onRefreshGameData', data);


            var baseRefreshData = data;
            var stage = baseRefreshData["stage"];

            //更改房间状态
            Control.roominfo.gameStage = stage;

            //钩子函数触发点-重连
            Method.checkRefreshGameData(data);
            //尝试恢复玩家数据-在线
            var playerDataList = baseRefreshData["playerDatas"];
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
                    player.update(oneData);
                })
            }



            //防止重连发准备
            // if(stage == Method.GAME_STAGE.WAIT_START || stage ==  Method.GAME_STAGE.GAME_READY){
            if (stage == Method.GAME_STAGE.WAIT_START) {
                //入场或者重连先发一次下一局
                // rf.netHandler.sendReadyNextRound();
                this.doSelfReady(true);
            } else {
                //为了游戏结束的时候玩家不要消失
                Method.cleanPlayerExit();
            }

            if (stage == Method.GAME_STAGE.WAIT_START) {
                if (!Control.roominfo.isGameStart()) {
                    // jx.each(playerDataList, function(playerData)
                    // {
                    //     var posLocal = cgb.getLocalPos(playerData["side"]);
                    //     var isOnline = playerData["isOnline"];
                    //     // this.setPlayerReady(posLocal, isOnline);
                    // }, this);

                    this.checkAutoStart();
                }
                return;
            }

            //入场或者重连先发一次下一局
            if (stage == Method.GAME_STAGE.GAME_READY) {
                // rf.netHandler.sendReadyNextRound();
                return;
            }

            //倒计时
            var posCurrentServer = baseRefreshData["currentSide"];
            var posCurrentLocal = Method.getLocalPos(posCurrentServer);
            Control.playerMgr.setCountdown(posCurrentLocal);

            //玩家数据恢复因为要等另一条协议，所以暂时不执行
            this._resetPlayerDataAfter = function () { };//
            this._resetPlayerData = function (extendData) {
                if (!this._resetPlayerData) return;
                this._resetPlayerData = null;

                //console.log("-玩家数据恢复-异步后数据", extendData);

                //重连游戏已结束
                var isOver = extendData['actionSide'] == 100;

                //其他玩家显示手牌计数
                Control.playerOther.forEach(function (player) {
                    player.isShowHandCount = true;
                });
                //玩家手牌数据
                data.playerDatas.forEach(function (oneData, idx) {
                    //手牌数据
                    oneData['cardDatas'] = extendData.playerRestoreData[idx]['cardDatas'];
                });
                //出牌数据
                data['lastActionedData'] = extendData.lastActionedData;
                //重构 allowAction 数据
                if (extendData['num'] === null) {
                    data['allowAction'] = null;
                } else {
                    data['allowAction'] = {
                        action: [],
                        num: extendData['num'],
                        side: extendData['actionSide']
                    }
                }

                //开始恢复数据
                var playerContentList = [{}, {}, {}];
                var lastActionedData = data["lastActionedData"];

                jx.each(lastActionedData, function (actionData, i) {
                    var posLocal = Method.getLocalPos(actionData["side"]);
                    var content = playerContentList[posLocal];

                    var outCards = actionData["cards"][0];
                    switch (outCards) {
                        case "pass":
                            content["tips"] = Control.playerMgr.TIPS_ID_NO_DISCARD;
                            break;

                        default:
                            var out = outCards.split(",");
                            if (out != "")
                                content["out"] = out;

                            var wvValueList = null;
                            if (actionData["cards"].length > 1)
                                wvValueList = actionData["cards"][1].split(",");
                            if (wvValueList != null)
                                content["wildcard"] = wvValueList;

                            break;
                    }
                });

                //设置癞子
                if (rf.isWildcardMode) {
                    var wildcardId = rfa.utils.transferWildCardTo(data["wildCards"]);
                    rfa.utils.setWildcard(wildcardId);
                    this.setWildcard(wildcardId);
                }

                this.lastCardPattern = null;
                this.posLastDiscardServer = null;
                this.Turnside = null;
                var posTurnLocal = Method.getLocalPos(baseRefreshData["currentSide"]);
                for (var i = 1; i < this.playerCount; ++i) {
                    var posLocal = (posTurnLocal - i + this.playerCount) % this.playerCount;
                    var content = playerContentList[posLocal];
                    var outCards = content["out"];
                    if (outCards != null) {
                        this.lastCardPattern = rfa.utils.getCardPattern(outCards, true, content["wildcard"]);
                        this.posLastDiscardServer = Method.getServerPos(posLocal);
                        break;
                    }
                }

                jx.each(playerDataList, function (playerData, i) {
                    try {
                        //console.log('尝试恢复玩家手牌', playerData);
                        var posServer = playerData["side"];
                        var posLocal = Method.getLocalPos(posServer);

                        var content = playerContentList[posLocal];
                        var cardDatas = playerData["cardDatas"];
                        if (!cardDatas) {
                            return Method.getPlayer(posLocal).handwall.show();
                        }
                        content["hand"] = (playerData["cardDatas"][0] != null ? playerData["cardDatas"][0].split(",") : []);
                        setTimeout(function () {
                            Method.getPlayer(posLocal).setContent(content);
                        }, 0);

                        if (posLocal != 0) {
                            Method.getPlayer(posLocal).handwall.isShowHandCount = cgb.config.showHandCardsCount;
                        }
                    } catch (e) {
                        console.error(e)
                    }
                }, this);


                var turnAction = baseRefreshData["allowAction"];
                if (turnAction != null)
                    this.onPlayerTurn(turnAction);

                var _after = this._resetPlayerDataAfter;
                this._resetPlayerDataAfter = null;
                if (_after) {
                    _after();
                }
            }

        }


        initGame(gameInfo) {

            this.initGameInfo(gameInfo);
            Control.createPlayerMgr(gameInfo);

            var roomInfo = gameInfo["roomInfo"];
            this.initRoomInfo(roomInfo);

            let selfInfo = gameInfo['selfInfo'];

            this.initRule(roomInfo["extend"]);
            Control.playerSelf.handwall.MoveUpTip = this.onHandWallTipList.bind(this);
        }

        initGameInfo(gameInfo) {
            var roomInfo = gameInfo["roomInfo"];
            var playerList = roomInfo["playerList"];
            var roomId = roomInfo["roomId"];
            var roomSetting = roomInfo["roomSetting"];
            var roomName = roomInfo["roomName"];

            //console.log('gameInfo', gameInfo);

            this.initMsgListen();
        }

        initRoomInfo(roomInfo) {
            //console.log('initRoomInfo', roomInfo);
            let playerInfo = roomInfo['playerList'];

            Control.roominfo.update(roomInfo);

            // Control.playerMgr.update(playerInfo);
        }

        reset() {
            Control.playerMgr.reset();
            Control.operationMgr.reset();
            Control.roominfo.reset();
            Control.buttonMgr.reset();
            Control.balanceView.hide();

            this.lastCardPattern = null;
            this._resetPlayerData = null;
            this.posLastDiscardServer = null;
            this.doubleData = [];
            this.Turnside = null;
        }

        //--------------调试
        try(callback) {
            return function () {
                try {
                    callback.apply(this, [].slice.apply(arguments))
                } catch (e) {
                    console.error(e)
                }
            }
        }
        checkAutoStart() {
            return;
        }
        //--------------调试部分结束

        initMsgListen() {
            // //重写已有接口，先检查是否存在
            // if (typeof S_C_READY_GAME_DATA != 'undefined') {
            //     NetHandlerMgr.netHandler.removeMsgListener(S_C_READY_GAME_DATA);
            //     NetHandlerMgr.netHandler.addMsgListener(S_C_READY_GAME_DATA, this.onReadyShow.bind(this));
            // }

            //------------基本消息
            //串行消息处理
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_ROLL_DICE, this.onRollDice.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_SET_START, this.onSetStart.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_BALANCE, this.try(this.onGameEnd.bind(this)));

            //正常消息处理
            NetHandlerMgr.netHandler.addMsgListener(ProtoKey.S_C_JOIN_ROOM, this.onPlayerJoin.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(ProtoKey.S_C_EXIT_ROOM, this.onPlayerExit.bind(this));
            // NetHandlerMgr.netHandler.addMsgListener(ProtoKey.S_C_ONLINE_STATE, this.onUpdateOnlineState.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(ProtoKey.S_C_NOTICE, this.onNotice.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(ProtoKey.S_C_GAME_START_RESULT, this.onGameStartResult.bind(this));
            // NetHandlerMgr.netHandler.addMsgListener(ProtoKey.S_C_EXIT_ROOM_RESULT, this.onGameStartResult.bind(this));
            // NetHandlerMgr.netHandler.addMsgListener(S_C_STAGE, this.onStage.bind(this));
            // NetHandlerMgr.netHandler.addMsgListener(S_C_DISSOLVE_VOTE, mb.showDissolveView);

            //------------金币场特有
            //串行消息处理
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyParty.S_C_GOLD_MESSAGE, this.onGoldMessage.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_EXIT_ROOM_RESULT, Method.exitRoomHandler.bind(Method));
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyParty.S_C_PLAYER_INFO, this.onPlayerGoldInfo.bind(this));


            //正常消息处理
            NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_PAY, this.onGoldPay.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_IS_GOLD, this.onGoldRoomInfo.bind(this));




            //------------跑得快
            //串行消息处理
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_GET_ONE_RESULT, this.onGetOneResult.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_RESULT_INFO, this.onShowWinAnimation.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_FLY, this.onGoldFlightAnimation.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_DEAL_CARDS, this.onDealCards.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_TURN_ACTION, this.onPlayerTurn.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_DO_ACTION_RESULT, this.onPlayerAction.bind(this));

            //正常消息处理
            // NetHandlerMgr.netHandler.addMsgListener(S_C_ONLINE_STATE, this.onUpdateOnlineState.bind(this));
            // NetHandlerMgr.netHandler.addMsgListener(S_C_DISSOLVE_VOTE, rf.showDissolveView);

            //癞子
            // NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_WILD_CARD, this.onWildCard.bind(this));

            //------------跑得快-强行补充数据消息
            //串行消息处理
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_ADDL_GAME_INFO, this.afterRefreshInfo.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_TRUSTEE, this.onTrusteeResult.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_DOUBLE_RESULT, this.onDoubleResult.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_DOUBLE, this.onShowDouble.bind(this));

            //正常消息处理
            // NetHandlerMgr.netHandler.addMsgListener(S_C_READY_GAME_DATA, this.doSelfReady.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_READY_GAME, this.onPlayerReady.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_WAIT_TIME, this.showServerCountDown.bind(this));


        }

        //--------------公共部分
        onPlayerJoin(msgData) {
            //console.log('onPlayerJoin', msgData);
            Control.playerMgr.addPlayer(msgData['info']);
        }

        onUpdateOnlineState(msgData) {
            let player = Method.getPlayerServer(msgData['chageSide']);
            player.online = msgData['isOnline'];
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


                //开始游戏局数加一
                Control.roominfo.currentRound++;
                Control.roominfo.gameStage = Method.GAME_STAGE.GAMING;

                Control.playerMgr.playerList.forEach(function (player) {
                    player.isReady = false;
                });
            } catch (e) { console.error(e); }



            finishedListener();
        }

        showBalance(msgData) {
            //console.log('showBalance', msgData)

            //单局结算数据
            var setData = msgData["setUserDatas"];
            //游戏总数据
            var gameData = msgData["gameUserDatas"];
            var hasGameData = gameData != null && gameData.length > 0;
            //没有数据，说明时间过长踢出
            var isGameEndTimeOut = setData && setData.length === 0 && gameData && gameData.length === 0;

            //发送准备
            var sendReady = jx.once(this, function () {
                //先检查是否继续游戏
                //钩子函数触发点-游戏结束
                let result = Method.checkGameEnd();
                // if(result){
                //     Laya.timer.clear(this, sendReady);
                //     this.doSelfReady();
                // }

            });

            //五秒后无反应自动准备
            Laya.timer.once(5000, this, sendReady);

            if (setData != null && setData.length > 0) {

                //插入补充数据加倍信息
                this.lastBalanceData = msgData;

                //展示小结
                Control.balanceView.show(msgData, function () {
                    sendReady();
                });
                this._view.getChild('operationExit').asCom.getController('c1').selectedIndex = 0;

                let ctl_autoCont = Control.buttonMgr.getComponent('ctl_autoCont');
                let autoContTimer = Control.balanceView.getComponent('autoContTimer');
                if (ctl_autoCont != null && autoContTimer != null) {
                    if (ctl_autoCont.selectedIndex == 1) {
                        Control.balanceView.showAutoContTimer();
                    } else {
                        Control.balanceView.hideAutoContTimer();
                    }
                }
            } else if (hasGameData) {
                // console.log('没有局数据，只有总的数据', gameData);
                // this.onTimeOutExitRoom();
                sendReady();
            } else if (isGameEndTimeOut) {
                // this.onTimeOutExitRoom();
                sendReady();
            }

        }

        playResultSound(data) {
            var dataList = data["setUserDatas"];
            var posWinners = [];
            jx.each(dataList, function (itemData, i) {
                var isWin = itemData["isWin"];
                if (isWin)
                    posWinners.push(itemData["side"]);
            }, this);
            if (posWinners.length > 0)
                Sound.playResult(posWinners.indexOf(Method.posServerSelf) != -1);
        }

        onGameEnd(msgData, finishedListener) {
            // console.log('onGameEnd', msgData);
            //单局结算数据
            var setData = msgData["setUserDatas"];
            var self = this;
            Control.roominfo.gameStage = Method.GAME_STAGE.GAME_READY;
            // if (this.doubleData != null && this.doubleData.length > 0) {
            //     if (setData != null) {
            //         for (let i = 0; i < setData.length; i++) {
            //             for (let j = 0; j < this.doubleData.length; j++) {
            //                 let itemdata = setData[i];
            //                 let itemdoubledata = this.doubleData[j]
            //                 if (itemdata != null && itemdoubledata != null) {
            //                     if (itemdata['side'] != null && itemdoubledata['side'] != null) {
            //                         if (itemdata["side"] == itemdoubledata["side"]) {
            //                             itemdata["double"] = itemdoubledata["choice"];
            //                         }
            //                     }
            //                     else {
            //                         console.log("----setUserDatas side is null-----");
            //                     }
            //                 }
            //                 else {
            //                     console.log("----setUserDatas item is null-----");
            //                 }
            //             }
            //         }
            //     }
            //     else {
            //         console.log("----setUserDatas is null-----");
            //     }
            // }
            // console.log(msgData["setUserDatas"], "========setUserDatas");


            //-----函数定义

            //小结
            var showView = function (msgData) {
                self.playResultSound(msgData);
                self.reset();//清除桌面資源
                self.showBalance(msgData);//8秒后再显示小结

                if (finishedListener != null)
                    finishedListener();
            }.bind(this, msgData);
            //展示手牌
            var showOtherHand = function (setData) {
                jx.each(setData, function (data) {
                    let player = Method.getPlayerServer(data['side']);
                    let cardIdList = data['tiles'][0];

                    if (cardIdList != null && cardIdList != '') {
                        cardIdList = cardIdList.split(",");
                        cardIdList.sort(rfa.utils.compareCard.bind(rfa.utils));
                        player.update(cardIdList);
                    }
                }, this);

                //显示手牌
                setData && setData.forEach(oneData => {
                    let player = Method.getPlayerServer(oneData['side']);
                    //结算动画
                    player.scoreBalance = parseFloat(oneData['score']);
                    //计算玩家分数
                    player.score = parseFloat(player.score) + parseFloat(oneData['score']);

                    let tiles = oneData['tiles'] && oneData['tiles'][0] && oneData['tiles'][0].split(',');
                    if (player && tiles) {
                        tiles.sort(rfa.utils.sortCardFunc);
                        player.handwall.out(tiles);
                    }
                });

                //清空自己手牌
                Control.playerSelf.handwall.resetHand();
            }.bind(this, setData);

            //先展示手牌，再到小结
            let showResult = function () {
                let delayTime = 4;
                showOtherHand();
                Control.playerMgr.setCountdown(Control.posLocalSelf, delayTime, showView)
            }.bind(this);


            if (msgData["instant"]) {
                showOtherHand();
                showView();
            }
            else {
                //有动画

                //春天表现
                var springData = null;
                var gameCommonDatas = msgData["gameCommonDatas"];
                if (gameCommonDatas != null && gameCommonDatas.length > 0)
                    springData = gameCommonDatas[0]["extendData"];

                if (springData != null && springData.length > 0) {
                    if (springData[0] == 1)//春天
                    {
                        this.showSpring(showResult);
                    }
                    else if (springData[0] == 2)//反春
                    {
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

        onPlayerExit(msgData) {
            // console.log('onPlayerExit', msgData);
            let serverSide = msgData['info'] && msgData['info']['side'];
            let player = Method.getPlayerServer(serverSide);
            if (player)
                player.clear();
        }

        onExitRoom(idDoNow = false) {
            Method.exitRoom(idDoNow);
        }

        onTimeOutExitRoom() {
            Method.disconnect();
            Alert
                .show(ExtendMgr.inst.getText4Language('无操作时间过长，请重新进入游戏'), true)
                .onYes(function () {
                    Method.exitToLobby();
                }.bind(this));
        }



        //-----------金币场
        onGoldRoomInfo(msgData) {
            if (msgData['gamenumber'])
                Control.roominfo.roomId = msgData['gamenumber'];
            Control.roominfo.roomSetting = ExtendMgr.inst.getText4Language(msgData['info']) + " " + ExtendMgr.inst.getText4Language("底分：") + Tools.inst.changeGoldToMoney(msgData['gold']);
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        onGoldPay(msgData) {
            // console.log('onGoldPay', msgData);
            var sides = msgData['sides'];
            var cost = msgData['coin'];

            var tips = ExtendMgr.inst.getText4Language('本场游戏每一局需要扣除 {0} 金币').format(cost);
            this.showTableTips(tips);

            sides.forEach(function (side) {
                let player = Method.getPlayerServer(side);
                player = parseFloat(player.score) - parseFloat(cost);
            })
        }

        onPlayerGoldInfo(msgData, finishedListener) {
            // console.log('+++++++++++ onPlayerGoldInfo', msgData)
            var playerInfo = msgData['playerInfo'];

            playerInfo.forEach(function (oneData) {
                let player = Method.getPlayerServer(oneData["side"]);
                player.score = parseFloat(oneData["possessionOfProperty"]);
            });
            if (finishedListener) finishedListener();
        }

        doSelfReady(isDoNow?) {
            if (isDoNow) {
                NetHandlerMgr.netHandler.sendReadyGame();
                Control.playerSelf.isReady = true;
            }

        }

        onPlayerReady(msgData, finishedListener) {

            //  console.log('onPlayerReady', msgData);
            let side = msgData['side'];
            let player = Method.getPlayerServer(side);
            player.isReady = true;

            if (typeof finishedListener == "function") finishedListener();

            // //如果别人准备了，看看自己是否准备
            // if( !Control.playerSelf.isReady){
            //     this.doSelfReady();
            // }
        }

        onGoldMessage(msgData, finishedListener) {
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
            if (typeof finishedListener == 'function') finishedListener();
        }

        //-----------跑得快
        onDealCards(msgData, finishedListener) {
            Control.roominfo.gameStage = Method.GAME_STAGE.GIVE_TILE;

            // console.log('onDealCards', msgData);
            try {
                let cards = msgData['cards'];
                cards = cards.split(',');
                Sound.playDealCard();

                Control.playerSelf.handwall.update(cards, true, function () {
                    if (typeof finishedListener == 'function') finishedListener();
                }, true);
                Control.playerOther.forEach(function (player) {
                    player.handCount = cards.length;
                });

                //是否显示手牌计数
                Control.playerSelf.isShowHandCount = false;
                Control.playerOther.forEach(function (player) {
                    // player.isShowHandCount = cgb.config.showHandCardsCount;
                    player.isShowHandCount = true;
                });
            } catch (e) {
                console.error(e);
            }

            // if (typeof finishedListener == 'function')finishedListener();
        }

        onShowDouble(msgData, finishedListener) {
            //console.log('onShowDouble', arguments);
            var _finished = function () {
                Control.roominfo.gameStage = Method.GAME_STAGE.WAIT_STRIVE;

                Control.operationMgr.show('jiabei', function (idx) {
                    Control.operationMgr.hide();
                    let map_idx2choice = { 0: 1, 1: 2 };
                    let choice = map_idx2choice[idx];
                    //console.log('点击加倍', choice);

                    Sound.clickCard();
                    NetHandlerMgr.netHandler.sendDouble(choice);
                });
            }.bind(this);

            //如果是重连，这在重来后才执行
            if (this._resetPlayerData) {
                this._resetPlayerDataAfter = _finished;
            } else {
                _finished();
            }

            if (typeof finishedListener == 'function') finishedListener();
        }

        onDoubleResult(msgData, finishedListener) {
            //console.log('onDoubleResult', arguments);

            try {
                let infos = msgData['doubleInfo'];
                if (infos.length > 1)
                    this.doubleData = infos;
                else
                    this.doubleData.push(infos[0]);
                infos.forEach(function (info) {
                    let side = info['side'];
                    let choice = info['choice'];
                    let player = Method.getPlayerServer(side);
                    player.isDouble = choice;
                })

                if (infos.length == 1 && infos[0]['side'] == Control.posServerSelf) {
                    Control.operationMgr.hide();
                }
            } catch (e) { console.error(e); }
            if (typeof finishedListener == 'function') finishedListener();
        }

        initRule(rule) {
            //注意这里用了假数据
            rule = "0,0,0,1,0,True,False";

            var ruleList = rule.split(",");
            if (ruleList.length != 7)
                return;

            cgb.config.firstThree = ruleList[3] == "0";
            cgb.config.showHandCardsCount = ruleList[4] == "0";
            cgb.config.canNoDiscard = ruleList[5] == "False";

            rfa.utils = new rfa.ClassicUtils();
        }

        afterRefreshInfo(msgData, finishedListener) {

            let playerRestoreData = msgData['playerRestoreData'];
            let lastActionedData = msgData['lastActionedData'];

            playerRestoreData.forEach(function (oneData) {
                let side = oneData['side'];
                let cardDatas = oneData['cardDatas'];
                if (cardDatas)
                    cardDatas = cardDatas[0].split(',');

                let player = Method.getPlayerServer(side);
                player.handwall.update(cardDatas);
            });

            if (this._resetPlayerData)
                this._resetPlayerData(msgData);

            if (typeof finishedListener == 'function') return finishedListener();
        }

        onPlayerTurn(msgData, finishedListener?) {
            try {
                //console.log('onPlayerTurn', msgData);

                if (Control.roominfo.gameStage == Method.GAME_STAGE.GAME_READY) {
                    if (typeof finishedListener == 'function') return finishedListener();
                    return
                }

                let posServer = msgData['side'];
                let posLocal = Method.getLocalPos(posServer);
                let player = Method.getPlayer(posLocal);
                player.handwall.resetOut();

                Control.playerMgr.clearCountdown();
                this.Turnside = posLocal;
                if (Control.posServerSelf == posServer) {

                    //开始计算应该显示哪些按钮
                    this.showPlayButton(msgData);
                } else {
                    Control.operationMgr.hide();
                    Control.playerMgr.setCountdown(Method.getLocalPos(msgData['side']), 15);
                }

                if (typeof finishedListener == 'function') return finishedListener();
            } catch (e) { console.error(e); }
        }

        onPlayerDiscard() {

            let cardIdList = Control.playerSelf.handwall.getSelectedData();

            // console.log('playerDiscard', cardIdList);
            //没有选择牌
            if (cardIdList.length == 0) {
                return this.showTileTips(Game.getText('discard_error_tips1'));
            }

            //console.log('playerDiscard', cardIdList);
            //------函数定义


            //隐藏选项
            Control.operationMgr.hide();
            //------开始判断流程
            //检查牌是否符合规则
            var isAll = cardIdList.length == Control.playerSelf.handwall.getDataList().length;
            cardIdList = cardIdList.sort(rfa.utils.sortCardFunc);
            var cpList = this.getAvailableCpList(cardIdList, isAll);


            if (cpList == null || cpList.length == 0) {
                //不符合规则
                this.showTileTips(Game.getText("discard_error_tips2"));
                Control.operationMgr.show();
            }
            else {
                //下家报单，自己必须出最大的牌
                if (this.nextPlayerIsAlarm()) {
                    if (cardIdList.length == 1 && rfa.utils.getCardNumber(cardIdList[0]) != Control.playerSelf.getMaxCardId()) {
                        this.showTileTips(Game.getText("discard_error_tips4"));
                        Control.operationMgr.show();
                        return;
                    }
                }

                //首轮必出3判断
                if (cgb.config.firstThree && this.lastCardPattern == null && this.currentRound == 1) {
                    //判断是否有方块3
                    if (Control.playerSelf.haveSequenceThree() && cardIdList.indexOf(rfa.CONSTANTS.SEQUENCE_THREE) == -1) {
                        Control.operationMgr.show();
                        this.showTileTips(Game.getText("discard_error_tips3_1"));
                        Control.operationMgr.show();
                        return;
                    }
                }

                NetHandlerMgr.netHandler.sendAction(Method.ACTION_TYPE.DISCARD, cpList[0].getActionData(), this.myTurnNum);
            }

        }

        showPlayButton(msgData) {
            let myTurnNum = this.myTurnNum = msgData["num"];
            let isNoDiscard = false;
            //--------函数定义
            //出牌函数
            var discard = this.onPlayerDiscard.bind(this);

            //点击按钮事件定义
            var idxTips = 0;
            var btnHandler = function (btnName) {
                switch (true) {
                    case (btnName == 'btnReset'):
                        Control.playerSelf.handwall.resetSelected();
                        break;
                    case (btnName == 'btnDeal'):
                        discard();
                        break;
                    case (btnName == 'btnTips'):
                        var cardIdList = tipsObjList[idxTips];
                        if (!cardIdList.isSorted) {
                            cardIdList.sort(rfa.utils.sortCardFunc);
                            cardIdList.isSorted = true;
                        }
                        Control.playerSelf.handwall.setCardsActive(cardIdList);
                        idxTips = ++idxTips % tipsObjList.length;
                        break;
                }
            }.bind(this);

            //允许出所有牌函数
            var allowAll = function () {
                Control.playerMgr.setCountdown(Method.getLocalPos(msgData['side']), 15);
                Control.playerSelf.cardsEnabled = true;

                this.lastCardPattern = null;
                Control.operationMgr.show('chupai', function (idx, btn) {
                    btnHandler(btn.name);
                }.bind(this));
            }.bind(this);

            //没有可出的牌
            var pass = function () {
                Control.playerMgr.setCountdown(Method.getLocalPos(msgData['side']), 3);
                Control.playerSelf.cardsEnabled = false;
                Control.operationMgr.show('pass', function (idx, btn) {
                    if (btn.name == 'btnPass') {
                        Control.playerSelf.handwall.resetSelected();
                        NetHandlerMgr.netHandler.sendAction(Method.ACTION_TYPE.NO_DISCARD, [], myTurnNum);
                    }
                });


            }.bind(this);

            //允许出部分牌
            var allowEnabled = function () {
                Control.playerMgr.setCountdown(Method.getLocalPos(msgData['side']), 15);
                Control.playerSelf.cardsEnabled = true;

                Control.operationMgr.show('chupai_tips', function (idx, btn) {
                    btnHandler(btn.name);
                })
            }.bind(this);

            //-------开始条件判断
            if (this.posLastDiscardServer == null || this.posLastDiscardServer == Control.posServerSelf) {
                //如果没有出牌人的数据或者上一个出牌人是自己，说明允许出所有牌
                allowAll();
            } else {
                //------获得可以出的牌
                //通过算法计算是否有可以出的牌
                var tipsObjList = rfa.utils.getGreaterList(this.lastCardPattern, Control.playerSelf.handwall.getDataList());

                //下家报单要过滤牌

                if (this.nextPlayerIsAlarm() && this.lastCardPattern.getType() == rfa.CARD_TYPE.SINGLE_CARD) {
                    var maxCardId = Control.playerSelf.getMaxCardId();
                    var temp = [];
                    if (tipsObjList != null) {
                        jx.each(tipsObjList, function (value) {
                            if (value.length != 1 || rfa.utils.getCardNumber(value[0]) == maxCardId)
                                temp.push(value);
                        });
                        tipsObjList = temp;
                    }
                }

                //--------检查候选牌
                if (tipsObjList == null || tipsObjList.length == 0) {
                    //没有可出的牌
                    pass();
                } else {
                    var cardPatternType = this.lastCardPattern.getType();
                    if (cardPatternType != rfa.CARD_TYPE.TRIPLET_WITH_ONE &&
                        cardPatternType != rfa.CARD_TYPE.TRIPLET_WITH_TWO &&
                        cardPatternType != rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS) {
                        //获取禁用牌列表
                        var disableList = rfa.utils.getDisableList(tipsObjList, Control.playerSelf.handwall.getDataList());
                        Control.playerSelf.handwall.setDisabled(disableList);
                    }

                    //跑得快有牌一定要出
                    allowEnabled();
                }
            }
        }
        onHandWallTipList(cardlist: Array<string>) {
            //console.log(cardlist, "=========carlist");
            if (cardlist == null || cardlist.length == 0)
                return false;
            //如果没有出牌人的数据或者上一个出牌人是自己，说明允许出所有牌
            if (this.posLastDiscardServer == null || this.posLastDiscardServer == Control.posServerSelf) {
                if (this.posLastDiscardServer == null && this.Turnside == Control.posServerSelf) {
                    let list = rfa.utils.getSequence(cardlist);
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
                var tipsObjList = rfa.utils.getGreaterList(this.lastCardPattern, Control.playerSelf.handwall.getDataList());
                if (tipsObjList == null || tipsObjList.length == 0) {
                    // return false;
                    //若有顺子，提示顺子
                    let list = rfa.utils.getSequence(cardlist);
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
                                tiplist.sort(rfa.utils.sortCardFunc);
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

        onPlayerAction(msgData, finishedListener) {
            //console.log('onPlayerAction', msgData);
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

            if (Method.ACTION_TYPE.NO_DISCARD == action) {
                if (isShowEffect) Sound.playPassSound(posLocal);
                player.handwall.pass();
                if (typeof finishedListener == 'function') finishedListener();
            }
            else if (Method.ACTION_TYPE.DISCARD) {
                let cardDataList = msgData["datas"];
                let cardIdList = cardDataList[0].split(",");
                let wvValueList = null;
                if (cardDataList.length > 1)
                    wvValueList = cardDataList[1].split(",");

                //console.log("receive:" + cardIdList + "--" + wvValueList);

                //这里排序会影响癞子玩法
                cardIdList = cardIdList.concat().sort(rfa.utils.compareCard.bind(rfa.utils));
                var cardPattern = rfa.utils.getCardPattern(cardIdList, true, wvValueList);
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
                                Sound.playLeftCardSound(posLocal, handCardCount);
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

        onTrusteeResult(msgData) {
            //console.log('onTrusteeResult', msgData);
            let infos = msgData['trusteeInfo'];
            infos.forEach(function (info) {
                let player = Method.getPlayerServer(info['side']);
                player.isTrustee = info['isTruster'];

                // //每次收到托管都拒绝
                // if( info['side'] == Control.posServerSelf && info['isTruster']){
                //     Control.buttonMgr.cancelTrustee();
                // }
            });



            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        showServerCountDown(msgData) {
            let sides = msgData['sides'];
            let waitTime = msgData['wait_time'];
            let side = sides.length > 1 ? 0 : (sides[0] || 0);
            Control.playerMgr.setCountdown(Method.getLocalPos(side), waitTime);

            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }


        //判断下下家是否报单
        nextPlayerIsAlarm() {
            let nextPlayer = <rf.playerTemplateData>Method.getPlayer(1);
            return nextPlayer.handCount == 1;
        }

        getAvailableCpList(cardIdList, isAll) {
            var cpList = rfa.utils.getCardPattern(cardIdList, isAll);
            if (cpList == null)
                return null;

            if (!jx.isArray(cpList)) {
                if (cpList.getType() == rfa.CARD_TYPE.INVALID)
                    return null;

                cpList = [cpList];
            }

            if (this.lastCardPattern == null)
                return cpList;

            var greaterList = [];
            jx.each(cpList, function (cp) {
                if (cp.greaterThan(this.lastCardPattern))
                    greaterList.push(cp);
            }, this);

            return greaterList;
        }



        //动效之类
        //------跑得快
        showTileTips(str) {
            let view = this._view;

            let container = view.getChild('tileTips').asGroup;
            container.visible = true;
            let font = view.getChildInGroup('tf_tlt_text', container);
            font.text = str == null ? '' : str;

            let transition = view.getTransition('showTileTips');
            transition.play(new Handler(this, function () {
                container.visible = false;
            }));
        }
        showTableTips(str) {
            let view = this._view;

            let container = view.getChild('tableTips').asGroup;
            container.visible = true;
            let font = view.getChildInGroup('tf_tlt_text', container);
            font.text = str == null ? '' : str;

            let transition = view.getTransition('showTableTips');
            transition.play(new Handler(this, function () {
                container.visible = false;
            }));
        }
        showSpring(showResult) {
            // let view = this._view;
            // var effectInstance = view.getChild('ef_spring').asCom;
            // effectInstance.visible = true;
            // setTimeout(function(){
            //     let transition = effectInstance.getTransition('enter');
            //     transition.play(new Laya.Handler(this, function(){
            //         effectInstance.visible = false;
            //         if(showResult)showResult();
            //     }))
            // }.bind(this), 0);
            Control.effects.playSpring(this, showResult);
        }
        showAntiSpring(showResult) {
            // let view = this._view;
            // var effectInstance = view.getChild('ef_anti_spring').asCom;
            // effectInstance.visible = true;
            // setTimeout(function(){
            //     let transition = effectInstance.getTransition('enter');
            //     transition.play(new Laya.Handler(this, function(){
            //         effectInstance.visible = false;
            //         if(showResult)showResult();
            //     }))
            // }.bind(this), 0);
            Control.effects.playAntiSpring(this, showResult);

        }

        //------牛牛特有
        onStriveForDealer(msgData) {
            // var choiceRace = msgData['choices'];
        }


        pass(msgData, finishedListener) {
            //console.log(msgData, arguments);
            if (typeof finishedListener == 'function') return finishedListener();
        }

        onGetOneResult() {
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        onShowWinAnimation() {
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        onGoldFlightAnimation() {
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        onNotice() {
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        onStage() {
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }



        onGameStartResult() {
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        onRollDice() {
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }


        startPoll() {
            Gmaster.startPoll();
        }
        stopPoll() {
            Gmaster.stopPoll();
        }

        onDispose() {

            Control.destory();
            Sound.stopBGM();
            Method.disconnect();
            Laya.timer.clearAll(this);
        }
    }
}