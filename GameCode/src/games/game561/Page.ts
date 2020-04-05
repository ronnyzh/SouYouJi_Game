/*
 * name;
 */
module G561 {
    import OperationManager = G561.fl.OperationManager;
    import roominfo = G560.fl.roominfo;
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
        private gameTimer: fairygui.GComponent;


        constructor() {
            super("G561", "GameScene", UILayer.GAME);
            Laya.stage.on(Laya.Event.KEY_DOWN, this, this.onKeyDown);
            page = this;
        }
        onCreated(data: any = null) {
            Sound.playBGM();
            Control.build(this);
            Control.playerMgr.clear();
            Control.playerMgr.setSelfSeat();
            this.gameTimer = this.view.getChild('timer').asCom;
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
            this.setTimeTip(4, null);
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
            NetHandlerMgr.netHandler.refreshData((data, finishedListener) => {
                try {
                    //console.log('refreshInfo', data);
                    if (data["result"]) {
                        // WaitingView.hide();
                        var refreshData = data['data'];
                        //基本游戏信息，只需要基本poker协议的refreshData的data里的gameInfo
                        var gameInfo = refreshData["gameInfo"];
                        //游戏房间信息，只需要基本协议的roomInfo
                        var roomInfo = gameInfo["roomInfo"];

                        //是否已经初始化过
                        try {
                            if (!Control.isPlayerMgrBuild)
                                this.initGame(gameInfo);
                            else
                                this.initRoomInfo(gameInfo["roomInfo"]);

                            this.onRefreshGameData(data);
                        } catch (e) {
                            console.error(e);
                        }
                        if (refreshData['stage'] == 0 || refreshData['stage'] == -1) {
                            this.setTimeTip(4, null);
                        }
                    }
                    else {
                        //退出房间
                    }
                    if (typeof finishedListener == 'function') finishedListener();
                } catch (e) {
                    //console.log(e)
                }

            });
        }

        onRefreshGameData(data) {
            this.reset();

            //已有数据部分
            let refreshData = data['data'];
            let gameInfo = refreshData['gameInfo'];
            let roomInfo = gameInfo['roomInfo'];
            let playerList = roomInfo['playerList'];
            let playerDataList = refreshData["playerDatas"];
            let selfInfo = gameInfo['selfInfo'];
            let baseRefreshData = data["data"];
            var stage = baseRefreshData["stage"];

            //更改房间状态
            Control.roominfo.gameStage = stage;
            Control.roominfo.defaultCountdown = parseFloat(gameInfo['Countdown']);

            //钩子函数触发
            Method.checkRefreshGameData(data);

            Control.playerMgr.clearOther();
            //尝试恢复玩家数据
            //玩家在线数据
            jx.each(playerDataList, function (playerData) {
                let player = Method.getPlayerServer(playerData["side"]);
                if (player) {
                    player.onine = playerData["isOnline"];
                }
            }, this);

            //尝试恢复玩家数据-个人信息
            //console.log('尝试恢复玩家数据-个人信息', playerList);
            if (playerList) {
                playerList.forEach(function (oneData) {
                    let player = Method.getPlayerServer(oneData['side']);
                    let useData = oneData['side'] == selfInfo['side'] ? selfInfo : oneData;
                    if (player) {
                        player.update(useData);
                    }
                })
            }

            //检查是否要发送准备

            // if (stage == Method.GAME_STAGE.WAIT_START || stage == Method.GAME_STAGE.GAME_READY) {
            if (stage == Method.GAME_STAGE.WAIT_START) {
                this.doSelfReady(true);
            } else if (stage != Method.GAME_STAGE.WAIT_START && stage != Method.GAME_STAGE.GAME_READY) {

                //游戏中

                //不响应准备消息
                Method.ignoreReady();

                //为了游戏结束的时候玩家不要消失
                Method.cleanPlayerExit();

                //显示操作盘
                let transition = this._view.getTransition('showOperation');
                transition.play();
                Control.operationMgr.show('normal');

                //每人发三张牌
                playerList.forEach(function (oneData) {
                    let player = Control.playerMgr.getPlayerServer(oneData['side']);
                    player.handwall.resetHand();
                    player.handwall.deal3();
                });

            }


            //倒计时
            var posCurrentServer = baseRefreshData["currentSide"];
            var posCurrentLocal = Method.getLocalPos(posCurrentServer);
            Control.playerMgr.setCountdown(posCurrentLocal);
            if (Control.playerMgr.playerList.length > 1) {
                Control.playerMgr.setTurnAnimate(posCurrentLocal);
            }

        }

        initGame(gameInfo) {
            var roomInfo = gameInfo["roomInfo"];
            //拼接数据-extend是打牌规则，服务器不发的话默认用这个
            roomInfo['extend'] = roomInfo['extend'] || "0,0,3,False,False";

            this.initGameInfo(gameInfo);

            Control.createPlayerMgr(gameInfo);

            this.initRoomInfo(roomInfo);

            let selfInfo = gameInfo['selfInfo'];


        }

        initGameInfo(gameInfo) {
            var roomInfo = gameInfo["roomInfo"];
            var playerList = roomInfo["playerList"];
            var roomId = roomInfo["roomId"];
            var roomSetting = roomInfo["roomSetting"];
            var roomName = ExtendMgr.inst.getText4Language(roomInfo["roomName"]);

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
            this.clearChip();
            this.hideTimeTip();
            this.lastCardPattern = null;
            this._resetPlayerData = null;
            this.posLastDiscardServer = null;
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

        pass(msgData, finishedListener) {
            //console.log(msgData, arguments);
            if (typeof finishedListener == 'function') return finishedListener();
        }

        //--------------调试部分结束
        initMsgListen() {

            //------------基本消息
            //串行消息处理
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_SET_START, this.onSetStart.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_BALANCE, this.onGameEnd.bind(this));

            //正常消息处理
            NetHandlerMgr.netHandler.addMsgListener(S_C_JOIN_ROOM, this.onPlayerJoin.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_EXIT_ROOM, this.onPlayerExit.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_ONLINE_STATE, this.onUpdateOnlineState.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_NOTICE, this.onNotice.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_GAME_START_RESULT, this.onGameStartResult.bind(this));
            //------------金币场特有
            //串行消息处理
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyParty.S_C_GOLD_MESSAGE, this.onGoldMessage.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_EXIT_ROOM_RESULT, Method.exitRoomHandler.bind(Method));
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyParty.S_C_IS_GOLD, this.onGoldRoomInfo.bind(this));
            //正常消息处理
            NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_PAY, this.onGoldPay.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_PLAYER_INFO, this.onPlayerGoldInfo.bind(this));
            //------------炸金花
            //串行消息处理
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_SENDRANDOMTILE, this.onRollDice.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_CANDOACTIONS, this.onCanDoAction.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_NEWDOACTION, this.onPlayerAction.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_SHOWTILES, this.onShowTiles.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_DEAL_CARDS, this.onDealCards.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_NEW_REFRESH_DATA, this.try(this.onRefreshNewData.bind(this)));


            //正常消息处理
            NetHandlerMgr.netHandler.addMsgListener(S_C_READY_GAMESTART, this.onServerCountDown.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_CANCEL_READY, this.clearServerCountDown.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_GOLDUPDATE, this.updateGold.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_NOGOLD, this.doNoGold.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_GOLDPAYRESULT, this.onChargeResult.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_PROXY, this.onProxyResult.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_PLAYERREADYRESULT, this.onReadyResult.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_BOTTOMCASTING, this.onBaseBitResult.bind(this));

            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_FIGHTOTHERRESULT, this.onFightResult.bind(this));

        }

        //--------------公共部分
        onPlayerJoin(msgData) {
            //console.log('onPlayerJoin', msgData);
            Control.playerMgr.addPlayer(msgData['info']);
        }

        onUpdateOnlineState(msgData) {
            let player = Method.getPlayerServer(msgData['chageSide']);
            if (player)
                player.online = msgData['isOnline'];
        }

        onSetStart(msgData, finishedListener) {

            //console.log('-onSetStart-', msgData);
            try {
                this.isStartGame = true;
                this.reset();
                // if(this.imgRuleTray != null)
                //     this.imgRuleTray.setVisible(false);
                //为了游戏结束的时候玩家不要消失
                Method.cleanPlayerExit();

                //开始游戏局数归零
                Control.roominfo.roundEmmit(null, 1);
                Control.roominfo.gameStage = Method.GAME_STAGE.GAMING;

                Control.playerMgr.playerList.forEach(function (player) {
                    player.isReady = false;
                });

                Sound.stopOperation();

                //忽略准备消息
                Method.ignoreReady();

                Control.playerMgr.playerList
                    .reduce(function (acc, cur) {
                        return cur.isEmpty ? acc : acc.concat(cur);
                    }, [])
                    .forEach(function (player) {
                        // let player = Method.getPlayerServer(serverSide);
                        player.handwall.resetHand();
                        player.handwall.deal3();
                    });


                //播放按鈕出現動畫

                let transition = this._view.getTransition('showOperation');
                transition.play();
                Control.operationMgr.show('normal');

            } catch (e) {
                console.error(e);
            }


            // fl.hideSetBalance();
            // fl.sound.setPlayerDataList(this.playerInfoMgr.getPlayerDataList());

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
                // if (result) {
                //     Laya.timer.clear(this, sendReady);
                //     this.doSelfReady();
                // }

            });



            if (setData != null && setData.length > 0) {

                //插入补充数据加倍信息
                this.lastBalanceData = msgData;

                //显示结算分数
                setData.forEach(oneData => {
                    let player = Method.getPlayerServer(oneData['side']);
                    if (!player) return;
                    if (oneData['side'] == Control.posServerSelf && parseFloat(oneData['score']) > 0) {
                        Sound.win();
                    }
                    player.scoreBalance = parseFloat(oneData['score']);
                    let tiles = oneData['tiles'] && oneData['tiles'][0] && oneData['tiles'][0].split(',');
                    if (player && tiles)
                        player.handwall.out(tiles);
                });


                //定义显示小结函数
                var doBalance = function () {
                    //3秒后无反应自动准备
                    Laya.timer.once(3000, this, sendReady);

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
                }.bind(this);
                // 显示结算分数后再显示结算
                Laya.timer.once(1000, this, doBalance);
            } else if (hasGameData) {
                sendReady();
            } else if (isGameEndTimeOut) {
                sendReady();
            }
        }

        //小结补充数据
        private _getBalanceAddition;

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
                data['gameCommonDatas'][0]["datas"] = (_d = msgData) && _d['datas']; laya
                return data
            })
        }

        onGameEnd(msgData, finishedListener) {
            Control.operationMgr.hide();
            this.hideTimeTip();
            //单局结算数据
            var setData = msgData["setUserDatas"];
            var self = this;

            //补充数据
            if (this._getBalanceAddition) {
                this._getBalanceAddition(msgData);
            }
            //-----函数定义

            //小结
            var showView = function (msgData) {
                Control.roominfo.gameStage = Method.GAME_STAGE.GAME_READY;
                Control.roominfo.gameStage = Method.GAME_STAGE.GAMEEND;
                Control.playerMgr.clearReadyPlayer();
                self.showBalance(msgData);
                if (finishedListener != null)
                    finishedListener();
            }.bind(this, msgData);

            //筹码飞向赢家
            var flyChip = function (callback) {
                Sound.chip2win();
                let arr = msgData["setUserDatas"]
                let i = arr.length;
                var winnerSide = null;
                while (i--) {
                    let item = arr[i];
                    let score = item['score'];
                    if (score != null) {
                        if (parseFloat(score) > 0) {
                            winnerSide = item['side'];
                            break;
                        }
                    }
                }
                if (winnerSide != null) {
                    let view = Method.getPlayerServer(winnerSide).getComponent('view');
                    let doList = this._chip_list;
                    var count = 0;
                    callback = callback && jx.once(this, callback);

                    if (doList.length) {
                        var emmit = function () {
                            if (count++ >= doList.length - 1) {
                                if (callback) callback();
                            }
                        }
                        doList.forEach((item) => {
                            Laya.Tween.to(
                                item,
                                { x: view.x, y: view.y },
                                1170,
                                Laya.Ease.expoOut,
                                new Laya.Handler(this, function () {
                                    item.visible = false;
                                    emmit();
                                }));
                        })
                    } else {
                        if (callback) callback();
                    }

                }
            }.bind(this)

            flyChip(showView);
        }

        onPlayerExit(msgData) {
            //console.log('onPlayerExit', msgData);
            let serverSide = msgData['info'] && msgData['info']['side'];
            let player = Method.getPlayerServer(serverSide);
            Control.playerMgr.removeReadyPlayer(serverSide);
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
        onPlayerGoldInfo(msgData) {
            //console.log('+++++++++++ onPlayerGoldInfo', msgData)
            var playerInfo = msgData['playerInfo'];

            playerInfo.forEach(function (oneData) {
                let player = Method.getPlayerServer(oneData["side"]);
                player.score = parseFloat(oneData["possessionOfProperty"]);
            });
        }

        onGoldRoomInfo(msgData) {
            if (msgData['gamenumber'])
                Control.roominfo.roomId = msgData['gamenumber'];
            if (msgData['gold'] != null)
                Control.roominfo.baseScore = msgData['gold'];
            Control.roominfo.roomSetting = ExtendMgr.inst.getText4Language(msgData['info']) + "  " + ExtendMgr.inst.getText4Language("底分：") + Tools.inst.changeGoldToMoney(msgData['gold']);
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        onGoldPay(msgData) {
            //console.log('onGoldPay', msgData);
            var sides = msgData['sides'];
            var cost = msgData['coin'];

            var tips = '本场游戏每一局需要扣除 {0} 金币'.format(cost);
            this.showTableTips(tips);

            sides.forEach(function (side) {
                let player = Method.getPlayerServer(side);
                player.score -= cost;
            })
        }

        doSelfReady(isDoNow) {
            if (isDoNow) {
                NetHandlerMgr.netHandler.sendReadyGame();
                Control.playerMgr.readyPlayer(Control.posServerSelf);
            }
            //Control.playerSelf.isReady = true;
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
                    NetHandlerMgr.netHandler.removeSequenceMsgListener(S_C_EXIT_ROOM_RESULT);
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

        //-----------炸金花
        onServerCountDown(msgData) {
            // let num = msgData['leftMS'] / 1000;
            // Control.playerMgr.setCountdown(Control.posLocalSelf, num);
            this.setTimeTip(0, msgData.leftMS);

            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        clearServerCountDown() {
            Control.playerMgr.clearCountdown();
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        updateGold(msgData) {
            //console.log('updateGold', msgData);
            let playerinfo = msgData['playerinfo'];

            playerinfo.forEach(function (oneData) {
                //总分
                if (parseFloat(oneData['change']) < 0) {
                    Control.roominfo.zongzhu -= parseFloat(oneData['change']);
                }

                let player = Method.getPlayerServer(oneData['side']);
                if (player)
                    player.score = oneData['score']
            })

            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        doNoGold() {
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        onChargeResult() {
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        onProxyResult(msgData) {

            let data = msgData['data'];
            data.forEach(function (oneData) {
                let isproxy = oneData['isproxy'];
                let player = Method.getPlayerServer(oneData['side']);
                player.isTrustee = isproxy;
                if (oneData['side'] == Control.posServerSelf) {
                    Control.buttonMgr.isTrustee = isproxy;
                }
            })
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        onReadyResult(msgData) {
            //console.log('onReadyResult', msgData);
            //@example:
            // {
            //     "PlayerResult": [{
            //     "side": 0,
            //     "result": false
            // }],
            //     "className": "S_C_PlayerReadyResult",
            //     "type": 45063,
            //     "receiveTime": 1526872262004
            // }
            try {
                msgData['PlayerResult'].forEach((oneData) => {
                    let player = Method.getPlayerServer(oneData['side']);
                    if (player) {
                        player.isReady = oneData['result'];
                        if (oneData['result'])
                            Control.playerMgr.readyPlayer(oneData['side']);
                    }
                });
            } catch (e) { console.error(e) }


            // return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        //所有玩家下底注
        onBaseBitResult(msgData) {
            // var example = {
            //         "number": 400,
            //         "className": "S_C_BottomCasting",
            //         "type": 12290,
            //         "receiveTime": 1526980869134
            // }

            Control.roominfo.baseScore = msgData['number'];
            //console.log('onBaseBitResult', msgData);

            Control.playerMgr.getPlayerList().forEach(function (player) {
                player.putChip(msgData['number']);
                if (!player.isEmpty) {
                    this.putChip(player.side, msgData['number'], true);
                }
            }, this);
            // return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        onCanDoAction(msgData, finishedListener) {
            //console.log('onCanDoAction', msgData);
            Control.roominfo.roundEmmit(msgData['side']);

            //倒计时
            if (msgData['leftMs']) {
                Control.playerMgr.setCountdown(Method.getLocalPos(msgData['side']), msgData['leftMs'] / 1000);
                Control.playerMgr.setTurnAnimate(Method.getLocalPos(msgData['side']));
            }
            //轮到自己操作
            if (msgData['side'] == Control.posServerSelf) {
                var actions = msgData['actions'];



                //数据处理
                var jiazhuList = null; //加注列表
                var fightList = null; //比牌玩家列表
                var fallowMulit = 1;//跟住数值
                let i = actions.length;

                while (i--) {
                    switch (true) {
                        case (actions[i]['action'] == ACTION.ADDGOLD):
                            jiazhuList = actions[i]['datas'].map(item => { return parseInt(item) });
                            break;
                        case (actions[i]['action'] == ACTION.FIGHTOTHER):
                            fightList = actions[i]['datas'].map(item => { return parseInt(item) });
                            break;
                        case (actions[i]['action'] == ACTION.FOLLOWGOLD):
                            fallowMulit = actions[i]['datas'];
                            break;
                    }
                }

                //获取操作对应按钮的映射
                let mapAction2btnName = {
                    [ACTION.GIVEUP]: 'btnPass',
                    [ACTION.LOOKTILE]: 'btnWatch',
                    [ACTION.FIGHTOTHER]: 'btnContrast',
                    [ACTION.ALL_IN]: 'btnAll',
                    [ACTION.ADDGOLD]: 'btnAdd',
                    [ACTION.FOLLOWGOLD]: 'btnFallow',
                    [ACTION.SINGLE]: 'btnSingle',
                };
                let actionList = msgData['actions'].reduce(function (acc, oneData) {
                    return acc.concat(mapAction2btnName[oneData['action']])
                }, []);

                //操作函数-结束
                var actionEnd = function () {
                    Control.operationMgr.disabledBtn();
                    actionReset();
                }

                //操作函数-还原
                var actionReset = function () {
                    //比牌
                    Control.operationMgr.clearSelectListPK();
                    //跟注
                    if (isShowing)
                        hideJiazhu();

                    Control.operationMgr.disabledBtn();
                }

                //操作函数-显示比牌
                var pkHandller = function (serverSide) {
                    //console.log('pkHandller', serverSide);
                    if (fightList.indexOf(serverSide) != -1) {
                        actionEnd();

                        Method.getPlayerServer(serverSide)
                            .showBipaiEffect(new Laya.Handler(this, function () {
                                send(ACTION.FIGHTOTHER, '', serverSide);
                            }));
                    } else {
                        this.showTileTips('不能选择该玩家');
                    }
                };
                var togglePK = function () {
                    if (fightList.length == 1) {
                        pkHandller(fightList[0]);
                    } else {
                        Control.operationMgr.toggleSelectListPK(fightList, pkHandller);
                    }

                };



                //操作函数-显示加注面板
                var hideJiazhu = function () {
                    //调整加注面板层级
                    Method.resetOperationIndex();
                    Control.operationMgr.hideJiazhu();
                };
                var handllerJiazhu = function () {
                    //调整加注面板层级
                    Method.topShowOperationIndex();
                    Control.operationMgr.showJiazhu(jiazhuList, function (idx, multiple) {
                        try {
                        } catch (e) {
                            console.error(e)
                        }

                        send(ACTION.ADDGOLD, '', multiple);
                        actionEnd();
                    })
                };

                var isShowing = Control.operationMgr.isShowJiazhu;
                var toggleJiazhu = function () {
                    if (!jiazhuList) return;
                    if (isShowing) {
                        isShowing = false;

                        hideJiazhu();
                    } else {
                        isShowing = true;
                        handllerJiazhu();
                    }
                };


                //操作函数-发送
                var send = function (action, datas?, number?) {
                    NetHandlerMgr.netHandler.sendAction(action, datas, msgData['num'], number);
                };

                //操作控制器
                let actionHandler = function (idx, btn) {
                    switch (btn.name) {
                        case ('btnPass'):
                            send(ACTION.GIVEUP);
                            return actionEnd();
                        case ('btnWatch'):
                            break;
                        case ('btnContrast'):
                            togglePK();
                            break;
                        case ('btnAll'):
                            send(ACTION.ALL_IN);
                            actionEnd();
                            break;
                        case ('btnAdd'):
                            toggleJiazhu();
                            break;
                        case ('btnFallow'):
                            send(ACTION.FOLLOWGOLD);
                            actionEnd();
                        case ('btnSingle'):
                            send(ACTION.SINGLE);
                            actionEnd();
                            break;
                    }
                };

                Control.operationMgr.showAction(actionList);
                Control.operationMgr.setClickCallback(actionHandler);
                // Control.operationMgr.textFallow = '跟' + Tools.inst.changeGoldToMoney(fallowMulit * Control.roominfo.baseScore);
                if (ExtendMgr.inst.lan == ExtendMgr.CN) {
                    if (fallowMulit[0]) Control.operationMgr.textFallow = '跟' + Tools.inst.changeGoldToMoney(fallowMulit[0]);
                    if (fallowMulit[0]) Control.operationMgr.textFight = '比' + Tools.inst.changeGoldToMoney(fallowMulit[0]);
                } else {
                    if (fallowMulit[0]) Control.operationMgr.textFallow = Tools.inst.changeGoldToMoney(fallowMulit[0]);
                    if (fallowMulit[0]) Control.operationMgr.textFight = Tools.inst.changeGoldToMoney(fallowMulit[0]);
                }

            }

            if (finishedListener) finishedListener();
        }

        onPlayerAction(msgData, finishedListener) {
            // var example = {
            //     "side": 0,
            //     "action": 1,
            //     "datas": [],
            //     "number": null,
            //     "multiple": null,
            //     "className": "S_C_NewDoAction",
            //     "type": 12292,
            //     "receiveTime": 1527038625283
            // }
            //console.log('onPlayerAction', msgData);
            if (msgData['side'] == Control.posServerSelf) {
                Control.operationMgr.resetExtend();
                Method.resetOperationIndex();
            }


            Control.playerMgr.talkAction(msgData['side'], msgData['action']);
            // if(msgData['action']==ACTION.GIVEUP || msgData['action']==ACTION.FIGHTLOSE){
            //     Control.Roominfo.onPlayerGameover(msgData['side']);
            // }

            let multiple = msgData['multiple'];
            let total = msgData['number'];
            let isSelf = msgData['side'] == Control.posServerSelf;
            switch (true) {
                case (msgData['action'] == ACTION.GIVEUP):
                    if (isSelf) {
                        Control.operationMgr.onGiviup();
                    }
                    break;
                case (msgData['action'] == ACTION.LOOKTILE):
                    break;
                case (msgData['action'] == ACTION.FIGHTLOSE):
                    break;
                case (isSelf):
                    Control.operationMgr.disabledBtn();
                case (msgData['action'] == ACTION.ALL_IN):
                case (msgData['action'] == ACTION.SINGLE):
                    this.putChip(msgData['side'], msgData['number'], true);
                    Method.getPlayerServer(msgData['side']).putChip(total);
                    break;
                case (msgData['action'] == ACTION.ADDGOLD):
                case (msgData['action'] == ACTION.FOLLOWGOLD):
                    this.putChip(msgData['side'], msgData['multiple']);
                    Method.getPlayerServer(msgData['side']).putChip(total);
                    break;
                case (msgData['action'] == ACTION.FIGHTOTHER):
                    this.putChip(msgData['side'], msgData['multiple']);
                    Method.getPlayerServer(msgData['side']).putChip(total);
                    break;
            }

            if (finishedListener) finishedListener();
            // return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        onFightResult(msgData, finishedListener) {
            //console.log('onFightResult', msgData);
            var _p1, _p2;
            var losePos;
            this.showPK(
                (_p1 = msgData['Player']['side']),
                (_p2 = msgData['bePlayer']['side']),
                (losePos = msgData['isWin'] ? _p2 : _p1),
                function () {

                    Control.playerMgr.talkAction(losePos, ACTION.FIGHTLOSE);
                    if (losePos == Control.posServerSelf)
                        Control.operationMgr.disabledAll();
                    if (finishedListener) finishedListener();
                }
            );


        }

        onShowTiles(msgData, finishedListener) {
            // var msgData = {
            //     "player": [
            //          {"side": 0, "tiles": ["9a", "6d", "5d"], "type": 6},
            //          {"side": 1,"tiles": ["Qb", "8a", "4a"],"type": 6
            //     }], "WinSide": null, "className": "S_C_ShowTiles", "type": 12294, "receiveTime": 1527154499232
            // }
            //console.log('onShowTiles', msgData);

            var dataCount = msgData.player.length;
            var isShowEffect = dataCount == 1;
            //修改數據
            msgData.player.forEach(function (oneData) {
                if (oneData['side'] == Control.posServerSelf) {
                    Control.operationMgr.WATCHED = true;
                }

                //伪造数据调用playerAction 播放玩家动作
                if (isShowEffect) {
                    var data = {
                        "side": oneData['side'],
                        "action": ACTION.LOOKTILE,
                    };
                    this.onPlayerAction(data, function () {
                        if (oneData['side'] == Control.posServerSelf) {
                            Control.playerSelf.handwall.showTileType(oneData['type']);
                        }
                    }.bind(this));
                }


                //写入数据
                Method.getPlayerServer(oneData['side']).handwall.dataList = oneData['tiles'].sort(Method.sortCardFunc);

            }, this);

            //判断当前阶段
            var finished = jx.once(this, function () {
                if (finishedListener) finishedListener();
            });

            if (isShowEffect) {
                finished();
            } else {
                Control.playerMgr.setCountdown(Control.posLocalSelf, 1, function () {
                    finished();
                });
            }


            // return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }


        //动效之类
        //------炸金花
        public _chip_pool = [];
        public _chip_list = [];
        putChip(serverSide, number, isAll?) {
            Sound.chip();
            var chip = this._chip_pool.shift();
            if (!chip) {
                chip = fairygui.UIPackage.createObject('G561', 'ChipMini');
                this._view.getChild('chipLayout').asGraph.addBeforeMe(chip);
                // this._view.getChild('chipGroup').asGroup
            }
            this._chip_list.push(chip);
            chip.setScale(1, 1);
            //外观-可见
            chip.visible = true;
            // //旋转
            // chip.rotate = Math
            //外观-文字
            var baseScore = Control.roominfo.baseScore;
            var score = isAll ? number : number * baseScore;
            let label = chip.asCom.getChild('title');
            label.text = jx.goldFormat(score);
            let tf: Laya.Text = new Laya.Text();
            tf.fontSize = label.fontSize;
            tf.text = label.text;
            while (tf.textWidth > label.width) {
                tf.fontSize--;
            }
            label.fontSize = tf.fontSize;
            //外观-颜色
            Control.operationMgr.changeChipBackground(chip, score, true, true);
            let poi0 = this.view.getChild('chipPoi0');
            let poi1 = this.view.getChild('chipPoi1');
            let width = poi1.x - poi0.x;
            let height = poi1.y - poi0.y;
            let x = poi0.x + width * Math.random();
            let y = poi0.y + height * Math.random();

            if (serverSide == null) {
                chip.x = x;
                chip.y = y;
            } else {
                //玩家头像位置
                var view = Method.getPlayerServer(serverSide).getComponent('view');
                chip.x = view.x;
                chip.y = view.y;
                Laya.Tween.to(chip, { x: x, y: y }, 200, Laya.Ease.expoOut);
            }



        }
        clearChip() {
            var arr = this._chip_list;
            var i = arr.length;
            while (i--) {
                let chip = arr.shift();
                chip.visible = false;
                this._chip_pool.push(chip);
            }
        }

        onDealCards(msgData, finishedListener) {
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

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

        showPK(serverSide1, serverSide2, loseSide, callback?) {
            let con = this._view.getChild('conPK').asGroup;
            let seat0 = this._view.getChildInGroup('seat0', con).asCom;
            let seat1 = this._view.getChildInGroup('seat1', con).asCom;
            let boom = this._view.getChildInGroup('boom', con);


            var resetBoomSite = function () {
                let LoseSeat = (loseSide == serverSide1) ? seat0 : seat1;
                let position = { x: LoseSeat.x + LoseSeat.width / 2 - boom.width / 2, y: LoseSeat.y + LoseSeat.height / 2 - boom.height / 2 };
                boom.x = position.x;
                boom.y = position.y;
                return position;
            };


            var initplayer = function (side, seat) {
                let player = Method.getPlayerServer(side);
                let seatItem = seat.getChild('seatItem').asCom;
                seatItem.getChild('icon').asLoader.url = 'ui://la8oslyoosvmbg';
                var headImgUrl = player.headImgUrl;
                try {
                    if (headImgUrl)
                        Tools.inst.changeHeadIcon(headImgUrl, seatItem.getChild('icon').asLoader);
                    else if (side == 0)
                        Tools.inst.changeHeadIcon(UserMgr.inst.imgUrl, seatItem.getChild('icon').asLoader);
                } catch (error) {
                    console.log(error)
                }
                seatItem.getChild('name').asTextField.text = player.nickname;
                seatItem.getChild('score').asTextField.text = Tools.inst.changeGoldToMoney(player.coin);
                seat.getChild('tfChip').asTextField.text = Tools.inst.changeGoldToMoney(player.chipNum);
            };

            initplayer(serverSide1, seat0);
            initplayer(serverSide2, seat1);

            var _c;
            (_c = this._view.getTransition('showPK'));

            _c.setHook('BoomStart', Laya.Handler.create(this, function () {
                // console.warn('BoomStart hook:',arguments)
                resetBoomSite();
                // _c.setValue('BoomStart', _p.x,_p.y);
            }));
            _c.play(new Laya.Handler(this, function () {
                Sound.pkLose();
                con.visible = false;
                if (callback) callback();
            }));

        }

        onRefreshNewData(msgData, finishedListener) {

            Control.roominfo.zongzhu = msgData['TotalGold'];
            Control.roominfo.roundEmmit(msgData['dealSide'], msgData['round']);
            Control.roominfo.totalRound = msgData['totalRound'];


            //已经转成元了，所以要转换显示
            msgData['BetsList'] && msgData['BetsList'].forEach(num => {
                this.putChip(null, num, true);
            });

            msgData['MultipleList'] && msgData['MultipleList'].forEach(num => {
                this.putChip(null, num);
            });

            msgData['AllInList'] && msgData['AllInList'].forEach(num => {
                this.putChip(null, num, true);
            });

            //这里的玩家数据保证是游戏中的玩家
            msgData['PlayerData'] && msgData['PlayerData'].forEach((oneData) => {
                //底注
                if (Method.isPlayingGame()) {
                    //console.log('恢复每个玩家底注');
                    this.putChip(null, Control.roominfo.baseScore, true);
                }

                let player = Method.getPlayerServer(oneData['side']);
                // //发三张牌
                // if(Method.isPlayingGame()){
                //     player.handwall.resetHand();
                //     player.handwall.deal3();
                // }
                //检查是否看牌，跳过自己
                if (oneData['isLook'] == 1 && oneData['side'] != Control.posServerSelf)
                    Control.playerMgr.talkAction(oneData['side'], ACTION.LOOKTILE);

                //加入游戏中的玩家队列
                Control.playerMgr.readyPlayer(oneData['side']);
                if (player) {
                    player.chipNum = oneData['PTotalGold'];
                    switch (oneData['state']) {
                        case 1:
                            //弃牌
                            if (oneData['side'] == Control.posServerSelf)
                                Control.operationMgr.onGiviup();
                            Control.playerMgr.talkAction(oneData['side'], ACTION.GIVEUP);
                            break;
                        case 2:
                            // 比牌失败
                            Control.playerMgr.talkAction(oneData['side'], ACTION.FIGHTLOSE);
                            break;
                        case 3:
                            //全压
                            Sound.allin_ef();
                            Control.playerMgr.talkAction(oneData['side'], ACTION.ALL_IN);
                            break;
                    }
                }

            }, this);
            if (finishedListener) finishedListener();
            return this.pass.apply(this, Array.prototype.slice.apply(arguments));
        }

        //------牛牛特有
        onStriveForDealer(msgData) {
            // var choiceRace = msgData['choices'];
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

        onRollDice(msgData, finishedListener) {
            Control.roominfo.roundEmmit(msgData['side'], 1);
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
            Laya.timer.clearAll(this.gameTimer);
            Method.clearTimeout();
            Laya.stage.off(Laya.Event.KEY_DOWN, this, this.onKeyDown);
        }


        private onKeyDown(e: Event): void {
            var keyCode: number = e["keyCode"];
            var Keyboard = Laya.Keyboard;
            switch (keyCode) {
                case Keyboard.NUMBER_0:
                    //console.log(UserMgr.inst.sid)
                    // if(NetHandlerMgr.netHandler)NetHandlerMgr.netHandler.disconnect();
                    // Game.Gmaster.reconnectNetHandler();
                    MasterMgr.inst.switch('relogin');
                    break;
                case Keyboard.X:
                    //this.putChip(null, 100 * Math.random(), true);
                    break;
                default:
                    //console.log(keyCode)
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
    }
}