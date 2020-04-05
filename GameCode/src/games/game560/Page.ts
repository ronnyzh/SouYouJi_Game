/*
 * name;
 */
module G560 {
    import OperationManager = G560.fl.OperationManager;
    import cleanPlayerExit = G560.GMethod.cleanPlayerExit;
    import playerMgr = G560.GControl.playerMgr;
    export let page: GPage;
    export class GPage extends Page {
        public isStartGame;
        public buttonsHandler;
        public currentRound;
        public lastCardPattern;
        public _resetPlayerData;
        public posLastDiscardServer;
        public myTurnNum;
        public lastBalanceData;

        public Turnside;//出牌位置  服务器位置
        constructor(pkg = "G560", comp = "GS560", layer = UILayer.GAME) {
            super(pkg, comp, layer);
            page = this;
        }
        onCreated(data: any = null) {
            //加载真正的背景
            // var url = ResourceMgr.RES_PATH + 'bg/bg2.jpg';
            // Tools.inst.changeBackground(url, this._view.getChild('bg').asLoader);
            Sound.playBGM();
            Control.build(this);
            Control.playerMgr.clear();
            Control.playerMgr.setSelfSeat();


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
                            Control.roominfo.multiple = 0;
                            [0, 1, 2].forEach(function (side) {
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
        onRefreshGameData(data) {
            //console.log('onRefreshGameData', data);
            //已有数据部分
            let refreshData = data['refreshData']['data'];
            var playerDataList = refreshData["playerDatas"];
            let baseRefreshData = data["refreshData"]["data"];
            var stage = baseRefreshData["stage"];
            //更改房间状态
            Control.roominfo.gameStage = stage;
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
                    if (player)
                        player.update(oneData);
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
                //console.log("-玩家数据恢复-异步后数据", data, extendData);
                let refreshData = data['refreshData']['data'];
                //-------恢复数据结构
                data['landlordData'] = extendData['landlordData'];
                data['lastActionedData'] = extendData['lastActionedData'];
                data['num'] = extendData['num'];
                data['playerBombData'] = extendData['playerBombData'];
                data['playerRestoreData'] = extendData['playerRestoreData'];
                data['robLandlord'] = extendData['robLandlord'];
                //--------修改重连数据
                Control.playerOther.forEach(player => {
                    player.isShowHandCount = true;
                })
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
                        var wildcardId = fla.utils.transferWildCardTo(gameRefreshData["wildCard"][0]);
                        fla.utils.setWildcard(wildcardId);
                        // this.setWildcard(wildcardId);
                    }
                    Control.roominfo.multiple = gameRefreshData["multiple"];
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
                            this.lastCardPattern = fla.utils.getCardPattern(outCards, content["wildcard"]);
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
            this.Turnside = null;
        }
        //--------------调试
        checkAutoStart() {
            return;
        }
        //--------------调试部分结束
        initMsgListen() {
            //------------基本消息
            //串行消息处理
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_ROLL_DICE, this.onRollDice.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_SET_START, this.onSetStart.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_BALANCE, this.onGameEnd.bind(this));
            //正常消息处理
            NetHandlerMgr.netHandler.addMsgListener(ProtoKey.S_C_JOIN_ROOM, this.onPlayerJoin.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(ProtoKey.S_C_EXIT_ROOM, this.onPlayerExit.bind(this));
            // NetHandlerMgr.netHandler.addMsgListener(ProtoKey.S_C_ONLINE_STATE, this.onUpdateOnlineState.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(ProtoKey.S_C_NOTICE, this.onNotice.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(ProtoKey.S_C_GAME_START_RESULT, this.onGameStartResult.bind(this));
            //------------金币场特有
            //串行消息处理
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyParty.S_C_GOLD_MESSAGE, this.onGoldMessage.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKey.S_C_EXIT_ROOM_RESULT, Method.exitRoomHandler.bind(Method));
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyParty.S_C_PLAYER_INFO, this.onPlayerGoldInfo.bind(this));
            //正常消息处理
            NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_PAY, this.onGoldPay.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_IS_GOLD, this.onGoldRoomInfo.bind(this));
            //------------斗地主
            //串行消息处理
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_DEAL_CARDS, this.onDealCards.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_ROBLANDLORD, this.onPlayerRobLandlord.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_ROBLANDLORDRESULT, this.onPlayerRobResult.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_TURN_ACTION, this.onPlayerTurn.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_DO_ACTION_RESULT, this.try(this.onPlayerAction.bind(this)));
            //正常消息处理
            //------------强行补充数据消息
            //串行消息处理
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_ADDL_GAME_INFO, this.afterRefreshInfo.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_TRUSTEE, this.onTrusteeResult.bind(this));
            //正常消息处理
            // NetHandlerMgr.netHandler.addMsgListener(S_C_READY_GAME_DATA, this.doSelfReady.bind(this));
            // NetHandlerMgr.netHandler.addMsgListener(S_C_TOTAL_BALANCE_DATA, this.pass('S_C_TOTAL_BALANCE_DATA'));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_READY_GAME, this.onPlayerReady.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_WAIT_TIME, this.showServerCountDown.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_MESSAGE, this.onServerMessage.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_ADDL_REPORT_CUR_GAME, this.saveBalanceAddition.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_OLD_ADDL_REPORT_CUR_GAME, this.saveOldBalanceAddition.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_SCOREDATA, this.updatePlayerBoomMultiple.bind(this));
            //癞子
            // NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_WILD_CARD, this.onWildCard.bind(this));
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
        showBalance(msgData) {
            //console.log('showBalance', msgData)
            //补充数据
            if (this._getBalanceAddition) {
                this._getBalanceAddition(msgData);
            }
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
                // //计算玩家分数
                // setData.forEach(function(oneData){
                //     let player = Method.getPlayerServer(oneData['side']);
                //     player.score =parseFloat(player.score)+ parseFloat(oneData['score']);
                // })
            } else if (hasGameData) {
                // console.log('没有局数据，只有总的数据', gameData);
                // this.onTimeOutExitRoom();
                sendReady();
            } else if (isGameEndTimeOut) {
                // this.onTimeOutExitRoom();
                sendReady();
            }
        }
        //小结补充数据
        public _getBalanceAddition;
        saveOldBalanceAddition(msgData) {
            this.saveBalanceAddition(msgData['addlReportCurGame']);
        }
        saveBalanceAddition(msgData) {
            //console.log('小结补充数据', msgData);
            this._getBalanceAddition = jx.once(this, function (data) {
                var _d;
                data['gameCommonDatas'] = [];
                data['gameCommonDatas'][0] = {};
                data['gameCommonDatas'][0]["extendData"] = (_d = msgData) && _d['extendData'];
                data['gameCommonDatas'][0]["datas"] = ExtendMgr.inst.getText4Language((_d = msgData) && _d['datas']);

                return data
            })
        }
        onGameEnd(msgData, finishedListener) {
            //console.log('onGameEnd', msgData);
            //单局结算数据
            var setData = msgData["setUserDatas"];
            var self = this;
            //补充数据
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
                msgData['setUserDatas'] && msgData['setUserDatas'].forEach(oneData => {
                    let player = Method.getPlayerServer(oneData['side']);
                    console.log(player);
                    //结算分动画
                    player.scoreBalance = parseFloat(oneData['score']);
                    //计算玩家分数
                    player.score = parseFloat(player.score) + parseFloat(oneData['score']);
                    let tiles = oneData['tiles'] && oneData['tiles'][0] && oneData['tiles'][0].split(',');
                    if (player && tiles) {
                        tiles.sort(fla.utils.sortCardFunc);
                        player.handwall.out(tiles);
                    }
                });
                //清空自己手牌
                Control.playerSelf.handwall.resetHand();
            }.bind(this);
            //先展示手牌，再到小结
            let showResult = function () {
                let delayTime = 4;
                showOtherHand();
                Control.playerMgr.setCountdown(Control.posLocalSelf, delayTime, showView)
            }.bind(this);
            if (msgData["instant"]) {
                showOtherHand();
                showView();
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
            //console.log('onPlayerExit', msgData);
            let serverSide = msgData['info'] && msgData['info']['side'];
            let player = Method.getPlayerServer(serverSide);
            if (player)
                player.clear();
        }
        onExitRoom(isDoNow = false) {
            Method.exitRoom(isDoNow);
        }
        onTimeOutExitRoom() {
            this.stopPoll();
            if (NetHandlerMgr.netHandler != null) {
                NetHandlerMgr.netHandler.disconnect();
            }
            Alert
                .show('无操作时间过长，请重新进入游戏', true)
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
        onGoldPay(msgData, finishedListener) {
            //console.log('onGoldPay', msgData);
            var sides = msgData['sides'];
            var cost = msgData['coin'];

            var tips = ExtendMgr.inst.getText4Language('本场游戏每一局需要扣除 {0} 金币').format(cost);
            this.showTableTips(tips);

            sides.forEach(function (side) {
                let player = Method.getPlayerServer(side);
                player.score = parseFloat(player.score) - parseFloat(cost);
            });
            if (finishedListener) finishedListener();
        }
        onPlayerGoldInfo(msgData, finishedListener) {
            //console.log('+++++++++++ onPlayerGoldInfo', msgData)
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
            //console.log('onPlayerReady', msgData);
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
            //console.log('onGoldMessage', msgData);
            if (typeof finishedListener == 'function') finishedListener();
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
        onDealCards(msgData, finishedListener) {
            Control.roominfo.gameStage = Method.GAME_STAGE.GIVE_TILE;
            //console.log('onDealCards', msgData);
            try {
                let dealcard = function () {
                    let cards = msgData['cards'];
                    cards = cards.split(',');
                    Control.playerSelf.handwall.update(cards, true, function () {
                        if (typeof finishedListener == 'function') finishedListener();
                    }, true);
                    Control.playerOther.forEach(function (player) {
                        player.handCount = cards.length;
                    });
                    //是否显示手牌计数
                    Control.playerSelf.isShowHandCount = false;
                    Control.playerOther.forEach(function (player) {
                        player.isShowHandCount = cgb.config.showHandCardsCount;
                    });
                };
                this.reset();
                if (msgData["isReDeal"]) {
                    Control.effects.playRedeal(this, dealcard);
                } else {
                    dealcard();
                }

            } catch (e) {
                console.error(e);
            }
        }
        initRule(rule) {
            //注意这里用了假数据
            // rule = "0,0,0,1,0,True,False";
            var ruleList = rule.split(",");
            //炸弹上限
            Control.roominfo.boomLimit = ruleList[2];
            fla.utils = new fla.ClassicUtils();
            cgb.config.showHandCardsCount = true; //是否显示手牌
            // //癞子玩法
            // fl.isWildcardMode = rule[3] == "True";
            // cgb.config.firstThree = ruleList[3] == "0";
            // cgb.config.showHandCardsCount = ruleList[4] == "0";
            // cgb.config.canNoDiscard = ruleList[5] == "False";
            //
            // fla.utils = new fla.ClassicUtils();
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
            if (this._resetPlayerData) {
                try {
                    this._resetPlayerData(msgData);
                } catch (e) { console.error(e); }
            }
            if (typeof finishedListener == 'function') return finishedListener();
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
        onPlayerDiscard() {
            let cardIdList = Control.playerSelf.handwall.getSelectedData();
            //没有选择牌
            if (cardIdList.length == 0) {
                return this.showTileTips(Game.getText('discard_error_tips1'));
            }
            //------函数定义
            //隐藏选项
            Control.operationMgr.hide();
            //------开始判断流程
            //检查牌是否符合规则
            cardIdList = cardIdList.sort(fla.utils.sortCardFunc);
            var cpList = this.getAvailableCpList(cardIdList);
            //console.log('playerDiscard', cardIdList, cpList);
            if (cpList == null || cpList.length == 0) {
                //不符合规则
                this.showTileTips(Game.getText("discard_error_tips2"));
                Control.operationMgr.show();
            }
            else if (cpList.length == 1) {
                NetHandlerMgr.netHandler.sendAction(ACTION_TYPE.DISCARD, cpList[0].getActionData(), this.myTurnNum);
            }
            else {
                //console.log('因为有癞子，所以有多种组合，暂未完成界面', cpList);
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
                    case (btnName == 'btnPass'):
                        NetHandlerMgr.netHandler.sendAction(ACTION_TYPE.NO_DISCARD, [], myTurnNum);
                        break;
                    case (btnName == 'btnTips'):
                        var cardIdList = tipsObjList[idxTips];
                        if (!cardIdList.isSorted) {
                            cardIdList.sort(fla.utils.sortCardFunc);
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
                Control.playerMgr.setCountdown(Method.getLocalPos(msgData['side']), 15);
                Control.playerSelf.cardsEnabled = false;
                Control.operationMgr.show('pass', function (idx, btn) {
                    if (btn.name == 'btnPass') {
                        Control.playerSelf.handwall.resetSelected();
                        NetHandlerMgr.netHandler.sendAction(ACTION_TYPE.NO_DISCARD, [], myTurnNum);
                    }
                });
            }.bind(this);
            //允许出牌且提示
            var allowEnabled = function () {
                Control.playerMgr.setCountdown(Method.getLocalPos(msgData['side']), 15);
                Control.playerSelf.cardsEnabled = true;
                Control.operationMgr.show('chupai_tips_pass', function (idx, btn) {
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
                var tipsObjList = fla.utils.getGreaterList(this.lastCardPattern, Control.playerSelf.handwall.getDataList());
                //下家报单要过滤牌
                if (tipsObjList == null || tipsObjList.length == 0) {
                    pass();
                } else {
                    allowEnabled();

                }
            }
        }
        //得到顺子
        onHandWallTipList(cardlist: Array<string>) {
            if (cardlist == null || cardlist.length < 2)
                return false;
            //如果没有出牌人的数据或者上一个出牌人是自己，说明允许出所有牌
            if (this.posLastDiscardServer == null || this.posLastDiscardServer == Control.posServerSelf) {
                if (this.posLastDiscardServer == null && this.Turnside == Control.posServerSelf) {
                    let list = fla.utils.getSequence(cardlist);
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
                var tipsObjList = fla.utils.getGreaterList(this.lastCardPattern, Control.playerSelf.handwall.getDataList());
                if (tipsObjList == null || tipsObjList.length == 0) {
                    // return false;
                    //若有顺子，提示顺子
                    let list = fla.utils.getSequence(cardlist);
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
                                tiplist.sort(fla.utils.sortCardFunc);
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
            if (ACTION_TYPE.NO_DISCARD == action) {
                player.handwall.pass();
                if (isShowEffect)
                    Sound.playPassSound(posLocal);
                if (typeof finishedListener == 'function') finishedListener();
            }
            else if (ACTION_TYPE.DISCARD) {
                let cardDataList = msgData["datas"];
                let cardIdList = cardDataList[0].split(",");
                let wvValueList = null;
                if (cardDataList.length > 1)
                    wvValueList = cardDataList[1].split(",");
                // console.log("receive:" + cardIdList + "--" + wvValueList);
                //这里排序会影响癞子玩法
                cardIdList = cardIdList.concat().sort(fla.utils.compareCard.bind(fla.utils));
                var cardPattern = fla.utils.getCardPattern(cardIdList, true, wvValueList);
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
            // console.log('onTrusteeResult', msgData);
            let infos = msgData['trusteeInfo'];
            infos.forEach(function (info) {
                let player = Method.getPlayerServer(info['side']);
                player.isTrustee = info['isTruster'];
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
        updatePlayerBoomMultiple(msgData) {

            setTimeout(function () {
                if (msgData['multiple']) {
                    Control.playerMgr.playerList.forEach(player => {
                        player.boomMultiple = msgData['multiple'];
                    })
                }
                let bombInfo = msgData['playerBombData'];
                if (bombInfo) {
                    let player = Method.getPlayerServer[bombInfo['side']];
                    if (player)
                        player.boomCount = bombInfo['bombCount'] != null ? bombInfo['bombCount'] : player.boomCount;
                }
            }.bind(this))
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }
        //判断下下家是否报单
        nextPlayerIsAlarm() {
            let nextPlayer = <fl.playerTemplateData>Method.getPlayer(1);
            return nextPlayer.handCount == 1;
        }
        getAvailableCpList(cardIdList) {
            var cpList = fla.utils.getCardPattern(cardIdList);
            if (cpList == null)
                return null;
            if (!jx.isArray(cpList)) {
                if (cpList.getType() == fla.CARD_TYPE.INVALID)
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
        onPlayerRobLandlord(msgData, finishedListener?) {
            //console.log('onPlayerRobLandlord', msgData);
            try {
                let isSelfTurn = Control.playerSelf.side == msgData['side'];
                let _c;
                let canShow = (_c = Control.playerSelf.isLandlord) == null || _c === 0;
                let countTime = 15;
                Control.playerMgr.setCountdown(Method.getLocalPos(msgData['side']), countTime);
                var type = msgData['choseType'];
                if (isSelfTurn) {
                    if (canShow) {
                        var canChooseScore = msgData['canChooseScore'];
                        let operationName =
                            Control.operationMgr.show('landlord', function (idx, btn) {
                                Control.operationMgr.hide();
                                NetHandlerMgr.netHandler.sendRob(type, idx);
                            }).after(this, function (btns: Array<fairygui.GButton>) {
                                let count = 0;
                                btns.forEach(function (btn, idx) {
                                    //第一个一定显示
                                    let isShow = idx == 0 || canChooseScore.indexOf(idx) !== -1;
                                    btn.visible = Boolean(isShow);
                                    if (isShow) {
                                        count++;
                                        let len = canChooseScore.length + 1;//第一个一定显示，所以+1
                                        let width = btn.parent.width;
                                        btn.x = ((count) / (len + 1) * width) - btn.width / 2;
                                    }
                                })
                            });
                    }
                } else {
                    this.showTableTips(ExtendMgr.inst.getText4Language("请等待其他玩家抢地主"));
                }
            } catch (e) { console.error(e); }
            if (typeof finishedListener == 'function') finishedListener();
        }
        onPlayerRobResult(msgData, finishedListener) {
            // console.log('S_C_RobLandlordResult', msgData);
            Control.operationMgr.hide();
            var isShowEffect = !msgData.instant;
            let player = Method.getPlayerServer(msgData['side']);
            let type = msgData["choseType"];
            let operate = msgData["operate"];
            let isLandLord;
            //显示标识
            switch (type) {
                case CALL_TYPE.CALL_LANDLORD:
                    isLandLord = operate == 1 ? 'yes' : operate;
                    player.isLandLord = isLandLord;
                    break;
                case CALL_TYPE.CALL_SCORE:
                    isLandLord = operate;
                    player.isLandLord = isLandLord;
                    if (isShowEffect)
                        Sound.playCallScore(msgData['side'], operate);
                    break;
                case CALL_TYPE.ROB_LANDLORD:
                    isLandLord = operate;
                    player.isLandLord = isLandLord;
                    break;
            }
            //确定地主
            let isConfirmLandlord = msgData['isConfirmLandlord'];
            if (isConfirmLandlord) {
                //禁用手牌
                Control.playerSelf.handwall.cardsEnabled = false;
                let landlordData = msgData["landlordData"];
                var serverSide = landlordData['landlordSide'];
                var dealerLocal = Method.getLocalPos(serverSide);
                let gameData = msgData['landlordData'];
                let holeCards = gameData["holeCards"] && gameData["holeCards"].split(",");
                //底分
                Control.roominfo.baseScore = landlordData['baseScore'];
                //地主标识
                Control.playerMgr.playerList.forEach(function (player) {
                    let isDealer = player.side == serverSide;
                    player.isDealer = isDealer;
                    if (!isDealer) {
                        player.isLandLord = null;
                    }
                });
                //地主牌数变更
                //if (dealerLocal != 0) {
                var dealerPlayer = Method.getPlayer(dealerLocal);
                dealerPlayer.handCount = parseInt(dealerPlayer.handCount) + 3
                // }
                //倍数
                Control.roominfo.multiple = gameData["multiple"];
                //地主牌
                Control.roominfo.holeCards = holeCards;
                if (dealerLocal == Control.posLocalSelf) {
                    Control.playerSelf.handwall.resetSelected();
                }
                if (dealerLocal == Control.posLocalSelf) {
                    //如果自己事地主，把牌加进入手牌
                    Control.playerSelf.handwall.addCard(holeCards);
                    //如果自己事地主，显示标识
                    Control.playerSelf.handwall.isDealer = true;
                }
            }
            if (finishedListener != null)
                finishedListener();
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
        showTableTips(str, callback?) {
            let view = this._view;
            let container = view.getChild('tableTips').asGroup;
            container.visible = true;
            let font = view.getChildInGroup('tf_tlt_text', container);
            font.text = str == null ? '' : str;
            let transition = view.getTransition('showTableTips');
            transition.play(new Handler(this, function () {
                container.visible = false;
                if (callback) callback();
            }));
        }
        showSpring(showResult) {
            Control.effects.playSpring(this, showResult);
        }
        showAntiSpring(showResult) {
            Control.effects.playAntiSpring(this, showResult);
        }
        try(callback) {
            return function (msgData, finishedListener) {
                try {
                    callback.call(this, msgData, finishedListener)
                } catch (e) { console.error(e) }
            }
        }
        pass(msgData, finishedListener) {
            // console.log(msgData, arguments);
            if (typeof finishedListener == 'function') return finishedListener();
        }
        onNotice() {
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }
        onStage() {
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }
        onServerMessage() {
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
            this.stopPoll();
            Control.destory();
            if (NetHandlerMgr.netHandler != null && NetHandlerMgr.netHandler.valid()) {
                NetHandlerMgr.netHandler.disconnect();
            }
            Laya.timer.clearAll(this);
        }
    }
}