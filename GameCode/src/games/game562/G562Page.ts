// /*
// * name;
// */
// //游戏阶段
module G562 {
    export let GAME562_STAGE = {
        WAIT_START: -1, // 创建房间后的第一个状态 ， 第一小局还没开始
        GAME_READY: 0, // 每一小局结束后进入该状态
        PREPARE_GAME: 6, // 准备游戏阶段
        WAIT_STRIVE: 4, // 抢庄
        AFTER_STRIVE: 5, // 抢庄完成做动画阶段
        WAIT_ROLL: 1, // 下注阶段
        GIVE_TILE: 3, // 发牌
        GAMING: 2, //游戏中
        PAUSE: 7 //游戏暂停阶段
    };

    export class G562Page extends Page {
        constructor() {

            super("G562", "GameScene", UILayer.GAME);
            //   super("G562", "handcard", UILayer.GAME);
            // super("G562", "test", UILayer.GAME);

        }
        private PlayerFrames: Array<G562PlayerFrame> = [];
        private robTheVillageBG: fairygui.GComponent;
        private robTheVillageCtl: fairygui.Controller = null;
        private btnContinue: fairygui.GButton;
        protected autoContTimer: fairygui.GObject;
        protected ctl_autoCont: fairygui.Controller;
        protected autoContTime: number = 3000;

        private gameStateCtl: fairygui.Controller = null;
        private Txt_score: { [key: string]: fairygui.GTextField } = {};//Array<fairygui.GTextField>=[];
        //  private CardMa: fairygui.GComponent;
        private Room_no: fairygui.GTextField;
        private centerpos: fairygui.GComponent;
        private timer: fairygui.GComponent;

        // private btnCList: Array<fairygui.GButton> = [];
        private centreSize: number = 0;
        private timerBG: fairygui.GComponent;
        private gameStage: number = 0;
        private playerSide: Array<number> = [];//所有玩家的位置号（服务器位置）
        private compare: Array<any> = [];
        private setUserDatas: Array<any> = [];
        private isshowAni = false;//比牌动画是否播放完毕
        private roomName: string = null;
        private ischoose: any = null
        private choosedata: any = null;
        private isinitChoose = false;//是否已经执行onshowChooseManual

        // private chooseView: fairygui.GComponent;
        //  private chooseBg: fairygui.GComponent;

        private btn_exit: fairygui.GButton;
        private isexit = true;



        //  private arrangedView = null;

        onCreated(data: any = null) {
            // console.log(data, "=====G562Page=========s");
            if (!data) return;
            //加载真正的背景
            //修改声音路径
            //  let url = ResourceMgr.RES_PATH + 'bg/shisanshuibg.jpg';
            //  Laya.loader.load(url, Handler.create(this, function (tex) {
            //  this._view.getChild('bg').asLoader.onExternalLoadSuccess(tex);
            //  }));

            let view = this._view;
            for (let i = 0; i < 5; i++) {
                this.PlayerFrames.push(new G562PlayerFrame({
                    seat: view.getChild('seat' + i).asCom,
                    hand_cards: view.getChild('hand_cards_' + i).asCom,
                    ok: view.getChild("ok_" + i).asCom,
                    qiang: view.getChild("qiang_" + i).asCom,
                    imgType: view.getChild("img_" + i).asCom,
                    special: view.getChild("special_" + i).asCom,
                    // shui: view.getChild("gold_" + i).asCom,
                    Txt_total_score: view.getChild("Txt_total_score_" + i).asCom,
                    Txt_total_score_bule: view.getChild("Txt_total_score_bule_" + i).asCom,
                    gun_0_txt: view.getChild("gun_0_txt_" + i).asCom,
                    gun_1_txt: view.getChild("gun_1_txt_" + i).asCom,
                    scaleCtl: view.getController("scale_" + i)
                }));
            }
            this.centerpos = view.getChild("centerpos").asCom;
            this.PlayerFrames[0]
            this.Txt_score = {
                // "total_socre": view.getChild("Txt_total_score").asTextField,
                "tou_score": view.getChild("Txt_tou_score").asTextField,
                "zhong_score": view.getChild("Txt_zhong_score").asTextField,
                "wei_score": view.getChild("Txt_wei_score").asTextField
            };
            // console.log(this.exitBtn.icon, "===========this.exitBtn");
            this.Room_no = view.getChild("room_no").asTextField;
            this.btnContinue = view.getChild("btn_continue").asButton;
            this.btnContinue.onClick(this, this.onExchangeRoom.bind(this));
            this.btnContinue.visible = false;
            this.timer = view.getChild('timer').asCom;
            this.timer.visible = false;

            var uiExitGame = view.getChild('uiExitGame').asCom;
            this.btn_exit = uiExitGame.getChild('btn_exit').asButton;
            this.btn_exit.onClick(this, this.onExitRoom.bind(this));
            var btn_setting = uiExitGame.getChild('btn_setting').asButton;
            btn_setting.onClick(this, function () {
                UIMgr.inst.popup(UI_Setting);
            });
            var btn_history = uiExitGame.getChild('btn_history').asButton;
            btn_history.onClick(this, function () {
                var obj = UIMgr.inst.popup(UI_History) as UI_History;
                obj.refreshGameListInGame(562);
            }.bind(this));
            var btn_rule = uiExitGame.getChild('btn_rule').asButton;
            btn_rule.onClick(this, function () {
                var rule = UIMgr.inst.popup(UI_Rules) as UI_Rules;
                rule.refreshData('game562');
            });
            // btn_rule.visible = false;
            var btn_proxy = uiExitGame.getChild('btn_proxy').asButton;
            btn_proxy.visible = false;
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
            // this.CardMa = view.getChild("macard").asCom
            //  this.CardMa.visible = false;
            //  let btn_setting = view.getChild('btn_setting').asButton;
            /*  btn_setting.onClick(this, function () {
                  NetHandlerMgr.netHandler.sendChangeRoom(function (msgData) {
                      //console.log('-sendChangeRoom-',msgData);                
                      if (msgData['result']) {
                          NetHandlerMgr.netHandler.disconnect();
                          this.reset();
                          let params = NetHandlerMgr.lastConnectParams;
                          NetHandlerMgr.netHandler.connect(params, this.reconnectResult.bind(this));
                      }
                  }.bind(this));
              });
              btn_setting.visible = false;*/

            // this.chooseView = view.getChild('choosecard').asCom;
            // this.chooseView.visible = false;
            // this.chooseBg = view.getChild('choosebg').asCom;
            // this.chooseBg.visible = false;
            this.playerSide = [];

            this.gameStateCtl = view.getController('State');

            this.reset(false);
            // this.onEnterRoomSuccess(data);
            SoundMgr.playMusic("bgm_sss.mp3")
            this.timerBG = this._view.getChild("updateTimer").asCom;
            this.initBetting();
            // if (!laya.renders.Render.isWebGL)
            //     this.setcacheAs();
            this.setSelfseat();

        }
        // newchooseCard(data) {
        //     // return new G562ChooseCard(data, this.chooseView);
        //     return new G562ChooseCard(data, this.chooseView);

        // }
        // setcacheAs() {
        //     this.view.getChild("bg").displayObject.cacheAs = "bitmap";
        //     this.view.getChild("n128").displayObject.cacheAs = "bitmap";
        //     this.view.getChild("nimg").displayObject.cacheAs = "bitmap";
        //     this.Txt_score["tou_score"].displayObject.cacheAs = "bitmap";
        //     this.Txt_score["zhong_score"].displayObject.cacheAs = "bitmap";
        //     this.Txt_score["wei_score"].displayObject.cacheAs = "bitmap";
        //     this.view.getChild("Txt_time").displayObject.cacheAs = "bitmap";
        //     this.view.getChild("tfGameInfo").displayObject.cacheAs = "bitmap";
        // }
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
        reconnectResult(connected) {
            if (!connected) return;
            let sid = UserMgr.inst.sid;
            NetHandlerMgr.netHandler.enterGame(sid, 562, this.onEnterRoomSuccess.bind(this));
            NetHandlerMgr.inst.initPingListen(G562.S_C_PING);
        }

        getPlayer(side: number) {
            return this.PlayerFrames[side];
        }

        setRobTheVillageState(show: boolean, state: number = 0) {
            this.robTheVillageCtl.setSelectedIndex(state);
            this.robTheVillageBG.visible = show;
        }
        onEnterRoomSuccess(data) {
            // console.log('onEnterRoomSuccess ok', data);
            let gameInfo = data["myInfo"];
            //断线重连，请求当前游戏数据
            if (gameInfo["isRefresh"])
                this.refreshInfo();
            else
                this.initGame(gameInfo);
        }
        onNetIntoGame(data) {
            this.onEnterRoomSuccess(data);
        }
        setSelfseat() {
            let data = {};
            data['nickname'] = UserMgr.inst._info.name;
            data['headImgUrl'] = UserMgr.inst._info.imgUrl;
            data['coin'] = '';
            this.getPlayer(0).setSeat(data, 0);
        }
        refreshInfo() {
            NetHandlerMgr.netHandler.refreshData((data) => {
                //  console.log(data, "=============刷新");

                if (data["result"]) {
                    // WaitingView.hide();
                    let refreshData = data["refreshData"]["data"];
                    let gameInfo = refreshData["gameInfo"];
                    //是否已经初始化过

                    //  console.log(this.posServerSelf, "============this.posServerSelf");
                    if (this.posServerSelf == null)
                        this.initGame(gameInfo);
                    else
                        this.initRoomInfo(gameInfo["roomInfo"]);

                    let waitCompareSides = data["waitCompareSides"];
                    this.onRefreshGameData(refreshData, waitCompareSides);
                    let isselfshowCard = true;
                    for (let i = 0; i < waitCompareSides.length; i++) {
                        if (this.getLocalPos(waitCompareSides[i]) == 0) {
                            isselfshowCard = false;
                            break;
                        }
                    }
                    if (refreshData["showCardTimeOut"] > 0 && !isselfshowCard) {
                        let cardIdList = data["cards"].split(",");
                        // console.log(cardIdList, "=============cardIdList");
                        let tipsDataList = twa.utils.getTipsDataList(cardIdList);
                        //console.log(tipsDataList, "============tipsDataList");
                        let typesList = twa.utils.getAutoArrangedCardsData(cardIdList, tipsDataList);
                        var choosedata =
                        {
                            "cardIdList": cardIdList,
                            "tipsDataList": tipsDataList,
                            "typesList": typesList,
                            "specialType": data["specialType"],
                            "typeScore": data["typeScore"],
                            "time": refreshData["showCardTimeOut"]
                        };
                        this.choosedata = choosedata;
                        if (!this.isinitChoose) {
                            this.onshowChooseManual();
                        }
                    }
                    let balanceData = data['balanceData'];
                    if (balanceData != null) {
                        this.setUserDatas = balanceData['setUserDatas'];
                        this.showBalancedatas(true);
                    }
                }
                else {
                    //退出房间
                }
                // if (data["gameStage"] == 4 || data["gameStage"] == 0) {
                //     this.onReset();
                // }
                if (data["gameStage"] == 0) {
                    this.onReset();
                }
                else if (data["gameStage"] == 4) {
                    // this.onReset(true);
                    this.btnContinue.visible = true;
                    this.showAutoContTimer();
                }

            });
            // WaitingView.show(gb.getText("refresh_roomInfo_tips"));
        }
        // 重连进来的数据
        onRefreshGameData(data, playerState: Array<any>) {
            // console.log("onRefreshGameData: ", data);
            //this.resetGame();
            let stage = data["stage"];
            this.gameStage = stage;

            if (stage == GAME562_STAGE.GAME_READY) {
                //  NetHandlerMgr.netHandler.sendReadyGame();
            }

            if (stage == GAME562_STAGE.WAIT_START) {
                return;
            }

            switch (stage) {
                case GAME562_STAGE.WAIT_ROLL:
                case GAME562_STAGE.GIVE_TILE:
                case GAME562_STAGE.GAMING:
                    this.refershInGame(data);
                    this.gameStateCtl.setSelectedIndex(0);
                    let playSide = this.playerSide.concat();
                    // console.log(playerState, "===========理牌中");
                    for (let i = 0; i < playerState.length; i++) {
                        let side = this.getLocalPos(playerState[i]);
                        // console.log(side, "================发牌");
                        this.getPlayer(side).setfapai(null)
                        let index = playSide.indexOf(playerState[i])
                        playSide.splice(index, 1);
                    }
                    //  console.log(playSide, "=================理牌完成");
                    for (let i = 0; i < playSide.length; i++) {
                        let side = this.getLocalPos(playSide[i]);
                        this.getPlayer(side).setHandCard(1, null);
                    }
                    break;
                case GAME562_STAGE.GAME_READY:
                    this.refreshInGameEnd(data);
                    break;
                default:
                    break;
            }
        }
        // 在游戏中重连回来
        refershInGame(msgData) {
            // console.log(msgData, "============refershInGame")
            let localSide = this.getLocalPos(msgData["dealerSide"]);
            let player = this.getPlayer(localSide);
            // console.log(player, "====refershInGame====");
            player.updateBankerState(true);
        }

        refreshInGameEnd(msgData) {
            //  this.gameStateCtl.setSelectedIndex(2);
            this.gameStateCtl.setSelectedIndex(0);
        }

        initGame(gameInfo) {
            // console.log(gameInfo, "---------initGame----------");
            this.reset(false);
            this.initGameInfo(gameInfo);

            let roomInfo = gameInfo["roomInfo"];
            this.initRoomInfo(roomInfo);
            let playlist = roomInfo["playerList"]
            for (let i = 0; i < playlist.length; i++) {
                this.playerSide.push(playlist[i]['side']);
            }
            this.initRule(roomInfo["extend"]);
        }
        initRule(rule) {
            let ruleList = rule.split(",");
            //  console.log(ruleList, "=============ruleList")
            cgb.config.isJokerPlay = ruleList[2] == "True";
            cgb.config.isHorsePlay = ruleList[3] == "True";
            cgb.config.isShotAddOne = ruleList[4] == "True";
            cgb.config.isDealerPlay = ruleList[6] == "True";

            if (cgb.config.isHorsePlay) {
                let horseCardIdList = ["Aa", "5a", "Ta"];
                cgb.config.horseCardId = horseCardIdList[ruleList[7]];
                // this.showHorseCard();
            }

            //新建算法
            twa.utils = new G562classic();
        }
        posServerSelf = null;
        // posLocalList=[0,2,6,3,5,1,7,4];
        posLocalList = [0, 1, 2, 3, 4, 5, 6];
        /*************************** Temp*/
        local2serverPos = {};
        server2localPos = {};

        transferServerPos = function (posServerSelf, posLocalList) {
            let playerCount = posLocalList.length;
            this.localPosList = posLocalList;
            //创建服务位置列表,不含自己
            let serverPosList = posLocalList.reduce(function (acc, posLocal, i) {
                let posServer = (i + posServerSelf) % playerCount;
                if (posServer != posServerSelf) acc.push(posServer);
                return acc;
            }, []);
            serverPosList.sort();
            //推入自己
            serverPosList = [posServerSelf].concat(serverPosList);
            //根据本地位置依次推入服务器位置        
            Tools.inst.each(posLocalList, function (posLocal, i) {
                let posServer = serverPosList[i];

                this.local2serverPos[posLocal] = posServer;
                this.server2localPos[posServer] = posLocal;
            }, this);
            // console.log('local2serverPos', this.local2serverPos)
            // console.log('server2localPos', this.server2localPos)
        }
        getServerPos(posLocal) {
            return this.local2serverPos[posLocal];
        }
        getLocalPos(posServer) {
            return this.server2localPos[posServer];
        }
        /*************************** */

        initGameInfo(gameInfo) {
            //  console.log('gameInfo', gameInfo)
            // console.log("=========initGameInfo==========");
            let roomInfo = gameInfo["roomInfo"];
            let playerList = roomInfo["playerList"];
            let roomId = roomInfo["roomId"];
            let roomSetting = roomInfo["roomSetting"];
            //let roomName = roomInfo["roomName"];
            this.roomName = roomInfo['roomName'];
            let selfInfo = gameInfo["selfInfo"];
            this.posServerSelf = selfInfo["side"];

            this.transferServerPos(this.posServerSelf, this.posLocalList);

            this.initMsgListen();
        }

        reset(isselfshow) {
            this.posServerSelf = null;
            this.choosedata = null;
            this.ischoose = null;
            this.isinitChoose = false;
            this.playerSide = [];
            this.Txt_score["tou_score"].visible = false;
            this.Txt_score["zhong_score"].visible = false;
            this.Txt_score["wei_score"].visible = false;
            //  this.view.getChild("total_img").visible = false;
            this.timer.visible = false;
            if (!isselfshow) {
                Tools.inst.each(this.PlayerFrames, function (node) {
                    node.clear();
                }, this);
            }
            Laya.timer.clearAll(this);
            this.resetGame();
            if (this.autoContTimer != null) {
                this.autoContTimer.visible = false;
            }

        }

        resetGame() {
            Tools.inst.each(this.PlayerFrames, function (node, side) {
                node.resetGame(side);
            }, this);
        }
        onExchangeRoom() {
            // console.log("====onExchangeRoom===");
            NetHandlerMgr.netHandler.sendChangeRoom(function (msgData) {
                // console.log(msgData, "====继续游戏的返回====");
                if (msgData['result']) {
                    this.btnContinue.visible = false;
                    if (NetHandlerMgr.netHandler != null) {
                        NetHandlerMgr.netHandler.disconnect();
                    }
                    this.reset(false);
                    var params = NetHandlerMgr.lastConnectParams;
                    NetHandlerMgr.netHandler.connect(params, this.reconnectResult.bind(this));
                }
            }.bind(this));
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

        initRoomInfo(roomInfo) {
            //  console.log('initRoomInfo', roomInfo)
            // NetHandlerMgr.netHandler.gameManage("1:4b5c6bTaJcQbKaAa4c5b6c7c8b", this.onGMResult.bind(this));//三顺子
            //  NetHandlerMgr.netHandler.gameManage("1:AcAaKbJcTc8b8a7c7b7a4c2c2a", this.onGMResult.bind(this));
            //  NetHandlerMgr.netHandler.gameManage("1:BjAbKaJd9d7b6c5d5a5b4c2c3c", this.onGMResult.bind(this));
            // NetHandlerMgr.netHandler.gameManage("1:BjAcKbTc8c8b7d6d3d3d3c2a", this.onGMResult.bind(this));
            let playerList = roomInfo["playerList"];
            // console.log(playerList, "============playerList");
            Tools.inst.each(playerList, function (playerInfo) {
                if (playerInfo != null) {
                    let posServer = playerInfo["side"];
                    let posLocal = this.getLocalPos(posServer);
                    this.getPlayer(posLocal).setSeat(playerInfo, posLocal);
                    this.getPlayer(posLocal).setReady();
                }
            }, this);
        }
        setgamestateTimer(stateindex, time: number = null, isshowText = true) {
            Laya.timer.clear(this, this.UpdatePoint);
            this.timer.visible = true;
            let stage = this.timer.getController('state');
            stage.selectedIndex = stateindex;
            let text = this.timer.getChild('title');
            text.visible = isshowText;
            if (isshowText) {
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
            else {
                let cb = () => {
                    this.timer.visible = false
                }
                Laya.timer.once(500, this, cb);
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
        initMsgListen() {
            //console.log("----串行消息处理----");
            // 串行消息处理
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_SET_START, this.onSetStart.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_BALANCE, this.onGameEnd.bind(this));

            // //正常消息处理
            NetHandlerMgr.netHandler.addMsgListener(S_C_JOIN_ROOM, this.onPlayerJoin.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_EXIT_ROOM, this.onPlayerExit.bind(this));
            // NetHandlerMgr.netHandler.addMsgListener(S_C_ONLINE_STATE, this.onUpdateOnlineState.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_NOTICE, this.onNotice.bind(this));

            //重写已有接口，先检查是否存在
            // if(typeof S_C_READY_GAME_DATA != 'undefined'){
            //     NetHandlerMgr.netHandler.removeMsgListener(S_C_READY_GAME_DATA);
            //     NetHandlerMgr.netHandler.addMsgListener(S_C_READY_GAME_DATA, this.onReadyShow.bind(this));
            // }

            //金币场特有
            NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_PAY, this.onPay.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_WATCHER_INFO, this.onWatcherInfo.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_GOLD_MESSAGE, this.onGoldMssage.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyParty.S_C_IS_GOLD, this.onGoldInfo.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_EXIT_ROOM_RESULT, this.onGoldExitRoomResult.bind(this));

            //游戏
            NetHandlerMgr.netHandler.addMsgListener(S_C_REFRESH_DATAS, this.onRefreshData.bind(this));
            //NetHandlerMgr.netHandler.addMsgListener(S_C_REFRESH_DATA, this.onRefreshData.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_NEW_DEAL_CARDS, this.onHasBullOrNot.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_SEND_OK_DATA, this.onShowReadyOk.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_GAME_START_RESULT, this.onGameStartResult.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_COMPARE, this.onCompare.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_SET_MULTIPLE, this.onRefreshTimeOut.bind(this));
            // NetHandlerMgr.netHandler.addMsgListener(S_C_MULTIPLE_RESULT, this.onBaseScore.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_ARRANGED_CARDS, this.onStage.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_WAIT_TIME, this.onwaitTime.bind(this));

            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_READY_GAMESTART, this.onShowMsg.bind(this));
            NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_CANCEL_READY, this.onHideMsg.bind(this));

            // NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_MY_ARRANGED_CARDS, this.onStriveForDealer.bind(this));
            // NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_GA_DATA, this.receivedGambleChoose.bind(this));
            // NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_GA_CHOOSE, this.receivedGambleWager.bind(this));
            // NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_GET_ONE_RESULT, this.onGetOneResult.bind(this));
            // NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_STRIVE_CHOOSE, this.onStriveChoose.bind(this));
            // NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_STRIVE_FOR_DEALER_TIMEOUT, this.onStriveForDealerTimeout.bind(this));
            // NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_STRIVE_RESULT, this.onStriveResult.bind(this));
            // NetHandlerMgr.netHandler.addSequenceMsgListener(S_C_FLY, this.onGoldFlightAnimation.bind(this));

        }
        onShowMsg(msgData, finishedListener) {
            this.setgamestateTimer(0, msgData['wait_time']);
            if (finishedListener)
                finishedListener();
        }
        onHideMsg(finishedListener) {
            this.timer.visible = false;
            if (finishedListener)
                finishedListener();
        }
        onwaitTime(msgdata) {
            // console.log(msgdata, "========onwaitTime");
            let time = msgdata["wait_time"];
            let type = msgdata["types"];
            if (type == "1") {
                this.setgamestateTimer(4);
            }
            else if (type == "2") {
                if (this.choosedata != null) {
                    this.choosedata["time"] = time;
                }
            }

        }
        // 一局游戏开始
        onSetStart(msgData, finishedListener) {
            // console.log(msgData, "---onSetStart---");
            SoundMgrShiSanShui.gameStart();
            let start = this.view.getChild("aniStartGame").asCom;
            start.visible = true;
            start.getTransitionAt(0).play(new Handler(this, function () {
                // start.visible = false;
                if (!this.isinitChoose) {
                    this.onshowChooseManual();
                }
                if (finishedListener) finishedListener();
            }));

        }
        onshowChooseManual() {

            this.isinitChoose = true;
            SoundMgrShiSanShui.gameStart();
            let cb = () => {
                this.view.getChild("aniStartGame").visible = false;
                for (let i = 0; i < this.playerSide.length; i++) {
                    if (this.playerSide[i] != null) {
                        let side = this.getLocalPos(this.playerSide[i]);
                        this.getPlayer(side).setfapai(
                            () => {
                                if (this.choosedata != null && this.ischoose == null) {
                                    this.ischoose = UIMgr.inst.add(G562ChooseCard, null, this.choosedata);
                                    // this.ischoose = this.newchooseCard(this.choosedata);
                                    // this.chooseView.visible = true;
                                    // this.chooseBg.visible = true;

                                }
                            }
                        );
                    }
                }
                Laya.timer.clear(this, cb);
            }
            Laya.timer.loop(800, this, cb);
        }
        // 游戏开始返回结果
        onGameStartResult(data) {
            //  console.log("onGameStartResult: ", data);
            if (!data["result"]) {
            } else {
                this.resetGame();
                // console.log("进来了游戏开始动画")
                //  this.gameStateCtl.setSelectedIndex(1);
                setTimeout(function () {
                    // if(finishedListener)finishedListener();
                    // this.gameStateCtl.setSelectedIndex(2);
                    this.gameStateCtl.setSelectedIndex(0);
                }.bind(this), 1000);
            }
        }
        onPlayerJoin(msgData) {
            //console.log(msgData, "=========onPlayerJoin");
            let data = msgData["info"];
            let posServer = data["side"];
            this.playerSide.push(posServer);
            let posLocal = this.getLocalPos(posServer);
            this.getPlayer(posLocal).setSeat(data, posLocal);
            this.getPlayer(posLocal).setReady();
            SoundMgrShiSanShui.playenter();

        }

        onPlayerExit(msgData) {
            // console.log(msgData);
            let playerInfo = msgData["info"];
            let posServer = playerInfo["side"];
            let posLocal = this.getLocalPos(posServer);
            let index = this.playerSide.indexOf(posServer);
            if (index != -1)
                this.playerSide.splice(index, 1);
            this.getPlayer(posLocal).clear();
            SoundMgrShiSanShui.playout();
        }
        onExitRoom() {
            if (!this.isexit) {
                //  亮牌动画没播放之前不能退出房间
                Alert.show(ExtendMgr.inst.getText4Language("游戏过程中不能退出游戏哦,请您先打完这局")).onYes(function () {
                    //MasterMgr.inst.switch('lobby');
                });
                return;
            }
            if (NetHandlerMgr.netHandler != null && NetHandlerMgr.netHandler.sendExitRoom != null && NetHandlerMgr.netHandler.valid()) {
                NetHandlerMgr.netHandler.sendExitRoom();
            }
            else {
                UserMgr.inst.returnToLobby();
            }
        }
        onUpdateOnlineState(msgData) {
            // console.log(msgData)
        }

        onNotice(msgData) {
            //  console.log(msgData)
        }
        // 显示准备按钮
        //onReadyShow(msgData) {
        // console.log(msgData);        
        //  NetHandlerMgr.netHandler.sendReadyGame();
        // }
        onPay(msgData) {
            // console.log(msgData);
        }

        onWatcherInfo(msgData) {
            // console.log(msgData);
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
        getspecialseat() {
            // let arrayside = [];
            /*for (let i = 0; i < this.compare["cardDatas"].length; i++) {
                let side = this.getLocalPos(i);
                if (this.getspeScore(side) != null) {
                    arrayside.push(side);
                }
            }
            for (let i = 1; i < arrayside.length; i++) {
                let get = this.getcardTypes(arrayside[i])[0];
                let index = arrayside[i];
                let j = i;
                let typenum = this.getcardTypes(arrayside[j - 1])[0];
                while (j > 0 && typenum > get) {
                    arrayside[j] = arrayside[j - 1];
                    --j;
                }
                arrayside[j] = index;
            }*/
            let arrayside = this.compare["specialDatas"];
            return arrayside;
        }
        //0 头  1中  2尾
        getActionseat(type: number) {
            //let arrayside = [];
            /* let cardDatas = this.compare["cardDatas"].concat();
             for (let i = 0; i < cardDatas.length; i++) {
                 let side = this.getLocalPos(cardDatas[i]["side"]);
                 if (this.getspeScore(side) == null) {
                     arrayside.push(side);
                 }
             }
             for (let i = 1; i < arrayside.length; i++) {
                 let get = this.getcardTypes(arrayside[i])[type];
                 let index = arrayside[i];
                 let j = i;
                 let typenum = this.getcardTypes(arrayside[j - 1])[type];
                 // if (this.getcardTypes(j - 1).length == 1) {
                 // typenum = this.getcardTypes(j - 1)[0];
                 // }
                 while (j > 0 && typenum > get) {
                     arrayside[j] = arrayside[j - 1];
                     --j;
                 }
                 arrayside[j] = index;
             }*/
            let arrayside;
            if (this.compare["normalDatas"] == null || this.compare["normalDatas"].length == 0)
                arrayside = null;
            else
                arrayside = this.compare["normalDatas"][type].split(",");
            // console.log(arrayside, "=========排序完之后的座位号");
            return arrayside;
        }
        getcardDatasIndex(side: number) {
            let cardDatas = this.compare["cardDatas"];
            for (let i = 0; i < cardDatas.length; i++) {
                if (cardDatas[i]['side'] == side) {
                    return i;
                }
            }
        }
        //服务器位置
        getCardIdList(side: number) {
            // console.log(side, "============位置号");
            let index = this.getcardDatasIndex(side);
            return this.compare["cardDatas"][index]["cards"];

        }
        getcardTypes(side: number) {
            let index = this.getcardDatasIndex(side);
            return this.compare["cardDatas"][index]["cardTypes"];
        }
        getscoreDatas(side: number) {
            let index = this.getcardDatasIndex(side);
            return this.compare["cardDatas"][index]["scoreDatas"];
        }
        getspeScore(side: number) {
            if (this.compare["cardDatas"] != null) {
                let index = this.getcardDatasIndex(side);
                return this.compare["cardDatas"][index]["speScore"];
            }
            else
                return null;
        }
        getscore(side: number) {
            if (this.setUserDatas != null && this.setUserDatas.length > 0) {
                let index = this.getcardDatasIndex(side);
                return this.setUserDatas[index]["score"];
            }
        }
        getplayertotal(side: number) {
            let speScore = this.getspeScore(side);
            if (speScore == null && this.setUserDatas != null && this.setUserDatas.length > 0) {
                let score = this.getscore(side);
                //   console.log(score, side, "=========正常牌分数");
                return score;
            } else {
                let scoreDatas = this.getscoreDatas(side);
                //let scoreList = scoreDatas.split(";");
                let score = scoreDatas[3];
                // for (let i = 0; i < scoreDatas.length; i++) {
                //     score = score + Tools.inst.TableParseFloat(parseInt(scoreDatas[i].split(",")[0]));
                // }
                //  console.log(score, "=========特殊牌分数");
                return score;
            }

        }
        getrotation(startside, endside) {

            let startPosX = this.getPlayer(startside).getHardCardX();
            let startPosY = this.getPlayer(startside).getHardCardY();
            let endPosX = this.getPlayer(endside).getHardCardX();
            let endPosY = this.getPlayer(endside).getHardCardY();
            let dis = startPosX - endPosX;
            let xy = Math.sqrt((startPosY - endPosY) * (startPosY - endPosY) + (startPosX - endPosX) * (startPosX - endPosX));
            let cos = dis / xy;
            let rot = Math.acos(cos) * 180 / Math.PI;
            //  console.log(rot, cos, startside, endside, "==========旋转角度");
            rot = rot - 180;
            if (rot < 0 && startside != 0)
                rot = -rot;
            return rot;

        }
        //打枪
        onShoot() {
            let shootData = this.compare["shootDatas"];
            if (shootData != null && shootData.length > 0) {
                let num = 0
                let cb = () => {
                    let data = shootData[num].split(",");
                    if (data[1] == 100) {
                        let shootside = this.getLocalPos(data[0]);
                        SoundMgrShiSanShui.Type(101, this.getPlayer(shootside).getsex());
                        let quanleida = this.view.getChild("quanleida").asCom;
                        quanleida.visible = true;
                        quanleida.getTransition("Ani").play(new Handler(this, function () {
                            quanleida.visible = false;
                        }));
                    }
                    else {
                        let shootside = this.getLocalPos(data[0]);
                        let dongside = this.getLocalPos(data[1]);
                        let score = data[2];
                        let rot = this.getrotation(shootside, dongside);
                        this.getPlayer(shootside).showshoot(0, rot, null);
                        this.getPlayer(dongside).showshoot(1, null, score);
                    }

                    if (num == shootData.length - 1) {
                        Laya.timer.clear(this, cb);
                        Laya.timer.once(500, this, showBetting);
                    }
                    num++;
                }
                let showBetting = () => {
                    this.showBetting();
                    for (let i = 0; i < this.playerSide.length; i++) {
                        if (this.playerSide[i] != null) {
                            let side = this.getLocalPos(this.playerSide[i])
                            this.getPlayer(side).hideshoot();
                        }

                    }
                }
                Laya.timer.loop(1000, this, cb);
            }
            else {
                this.showBetting();
            }

        }
        showBetting() {
            //播放金币动画
            // let centerpos = new laya.maths.Point(this.view.actualWidth / 2, this.view.actualHeight / 2);
            let nb = () => {
                for (let i = 0; i < this.playerSide.length; i++) {
                    if (this.playerSide[i] != null) {
                        let side = this.getLocalPos(this.playerSide[i]);
                        let score = this.getplayertotal(this.playerSide[i]);
                        if (score < 0) {
                            let startPlayer = this.getPlayer(side);
                            let startPosX = startPlayer.getSeatX();
                            let startPosY = startPlayer.getSeatY();
                            let pos = FairyguiTools.rootToLocal(this.centerpos, { x: startPosX, y: startPosY })
                            // console.log(localSide, pos, "金币飞入");
                            this.onBettingAnimation(pos.x, pos.y, 0, 0);
                        }
                    }
                    // let localSide = this.getLocalPos(i)
                }
                Laya.timer.clear(this, nb);
                Laya.timer.loop(500, this, cb);
            }
            Laya.timer.loop(500, this, nb);
            //金币动画
            let cb = () => {
                for (let i = 0; i < this.playerSide.length; i++) {
                    // let localSide = this.getLocalPos(i)
                    if (this.playerSide[i] != null) {
                        let side = this.getLocalPos(this.playerSide[i]);
                        let score = this.getplayertotal(this.playerSide[i]);
                        if (score > 0) {
                            let startPlayer = this.getPlayer(side);
                            let startPosX = startPlayer.getSeatX();
                            let startPosY = startPlayer.getSeatY();
                            let pos = FairyguiTools.rootToLocal(this.centerpos, { x: startPosX, y: startPosY })
                            // console.log(localSide, pos, "金币飞出");
                            this.onBettingAnimation(0, 0, pos.x, pos.y);
                        }
                    }
                }
                Laya.timer.clear(this, cb);
                this.showBalancedatas();
                // this.onTimebalance();
                this.btnContinue.visible = true;
                this.showAutoContTimer();
                this.isexit = true;
            }
        }
        private goldPool: Array<fairygui.GComponent> = [];
        private goldList: Array<fairygui.GComponent> = [];

        private addgold() {
            let gold = (fairygui.UIPackage.createObject('G562', 'gold').asCom);
            Tools.inst.changeBackground(ResourceMgr.RES_PATH + "ui/tb_gold.png", gold.getChild('icon').asLoader);
            this.centerpos.addChild(gold);
            this.goldList.push(gold);
            gold.visible = false;

            return gold;
        }
        getgold() {
            let gold;
            if (this.goldPool.length > 0) {
                gold = this.goldPool.shift()
                this.goldList.push(gold);

            }
            else {
                gold = this.addgold();
            }
            gold.removeFromParent()
            this.centerpos.addChild(gold);
            gold.visible = true;
            return gold
        }
        hidegold(gold) {
            let index = this.goldList.indexOf(gold)
            if (index != -1) {
                let gold = this.goldList.splice(index, 1)[0];
                gold.visible = false;
                this.goldPool.push(gold);
            }
        }
        cleargold() {
            for (let i = 0; i < this.goldList.length; i++) {
                let gold = this.goldList.shift();
                gold.removeFromParent();
                gold.dispose();
            }
            for (let i = 0; i < this.goldPool.length; i++) {
                let gold = this.goldPool.shift();
                gold.removeFromParent();
                gold.dispose();
            }
        }

        initBetting() {
            for (var i = 0; i < 15; i++) {
                this.addgold();
            }

        }
        //金币飞行动画
        onBettingAnimation(startPosX, startPosY, endPosX, endPosY) {
            SoundMgrShiSanShui.flyGold();
            // console.log(this.centerpos, "=============this.centerpos");
            for (var i = 0; i < 15; i++) {
                let gold = this.getgold();
                gold.setScale(0.8, 0.8)
                gold.setXY(startPosX, startPosY);
                this.centerpos.addChild(gold);

                let hd = Handler.create(gold, function () {
                    //  gold.visible = false;
                    this.hidegold(gold);
                    //  this.centerpos.removeChild(gold);

                }.bind(this));

                let goldX = this.random4(endPosX, endPosX + 100);
                let goldY = this.random4(endPosY, endPosY + 100);


                let tween = Laya.Tween;
                tween.to(gold, { x: goldX, y: goldY }, 500, Laya.Ease.circInOut, hd, i * 10);
            }
        }
        random4(n: number, m: number) {
            let random = Math.floor(Math.random() * (m - n + 1) + n);
            return random;
        }
        //倒计时进入结算
        // onTimebalance() {
        //     var num = 3;
        //     this.view.getChild("nimg").visible = true;
        //     this.view.getChild("ntxt").visible = true
        //     let txt = this.view.getChild("Txt_time_balance").asTextField;
        //     txt.visible = true
        //     let cb = () => {
        //         txt.text = num.toString();
        //         num = num - 1;
        //         if (num < 0) {
        //             this.view.getChild("nimg").visible = false;
        //             this.view.getChild("ntxt").visible = false;
        //             txt.visible = false;
        //             Laya.timer.clear(this, cb);
        //             if (this.setUserDatas != null && this.setUserDatas.length > 0) {
        //                 // UIMgr.inst.add(G562Balance, null, this.setUserDatas);
        //             }
        //         }
        //     }
        //     cb();
        //     Laya.timer.loop(1000, this, cb);
        // }
        onshowspecial() {
            let arrayside = this.getspecialseat()
            if (arrayside == null || arrayside.length == 0) {
                this.isshowAni = true;
                //播放打枪动画
                this.onShoot();
                return;
            }

            let sideIndex = 0;
            let cb = () => {
                let side = arrayside[sideIndex];
                let cardList = this.getCardIdList(side)[0].split(",");
                let Type = this.getcardTypes(side)[0];
                this.getPlayer(this.getLocalPos(side)).setSpecial(cardList, Type);
                sideIndex++;
                if (sideIndex == arrayside.length) {

                    this.isshowAni = true;
                    //播放打枪动画
                    this.onShoot();
                    Laya.timer.clear(this, cb);
                }

            }
            Laya.timer.loop(1000, this, cb);
        }
        oncardLoop_wei() {
            let sideIndex = 0;
            let indexType_wei = 2;
            let arrayside = this.getActionseat(indexType_wei);

            let cb_wei = () => {
                let side = arrayside[sideIndex];
                let speScore = this.getspeScore(side);
                if (speScore == null) {
                    let cardList = this.getCardIdList(side)[indexType_wei].split(",");
                    let Type = this.getcardTypes(side)[indexType_wei];

                    this.getPlayer(this.getLocalPos(side)).setCompareCard(indexType_wei, cardList, Type, this.view.getController("location"));
                }
                if (sideIndex == arrayside.length - 1) {
                    if (this.getspeScore(this.getServerPos(0)) == null) {
                        let scoreDatas_0 = this.getscoreDatas(this.getServerPos(0))[indexType_wei];
                        let score = Tools.inst.TableParseFloat(scoreDatas_0.split(",")[0]) + Tools.inst.TableParseFloat(scoreDatas_0.split(",")[1]);
                        this.Txt_score["wei_score"].visible = true;
                        this.Txt_score["wei_score"].text = score > 0 ? "+" + score.toString() : score.toString();
                        //this.getPlayer(0).settotal_score(Tools.inst.TableParseFloat(this.getscoreDatas(0)[3]));
                    }
                    else {
                        let scoreDatas_0 = this.getscoreDatas(this.getServerPos(0));
                        // let scoreList = scoreDatas_0.split(";");
                        let score = scoreDatas_0[3];
                    }

                    // this.view.getChild("total_img").visible = true;
                }
                sideIndex++;
                if (sideIndex == arrayside.length) {
                    Laya.timer.clear(this, cb_wei);
                    sideIndex = 0;
                    this.onshowspecial();
                }
            }
            Laya.timer.loop(750, this, cb_wei);
        }
        oncardLoop_zhong() {
            let sideIndex = 0;
            let indexType_zhong = 1;
            let arrayside = this.getActionseat(indexType_zhong);

            let cb_zhong = () => {
                let side = arrayside[sideIndex];
                let speScore = this.getspeScore(side);
                if (speScore == null) {
                    let cardList = this.getCardIdList(side)[indexType_zhong].split(",");
                    let Type = this.getcardTypes(side)[indexType_zhong];
                    let scoreDatas = this.getscoreDatas(side)[indexType_zhong];
                    this.getPlayer(this.getLocalPos(side)).setCompareCard(indexType_zhong, cardList, Type, this.view.getController("location"));
                }
                if (sideIndex == arrayside.length - 1) {
                    if (this.getspeScore(this.getServerPos(0)) == null) {
                        let scoreDatas_0 = this.getscoreDatas(this.getServerPos(0))[indexType_zhong];
                        let score = Tools.inst.TableParseFloat(scoreDatas_0.split(",")[0]) + Tools.inst.TableParseFloat(scoreDatas_0.split(",")[1]);
                        this.Txt_score["zhong_score"].visible = true;
                        this.Txt_score["zhong_score"].text = score > 0 ? "+" + score.toString() : score.toString();
                    }
                }
                sideIndex++;
                if (sideIndex == arrayside.length) {
                    Laya.timer.clear(this, cb_zhong);
                    this.oncardLoop_wei();
                }
            }
            Laya.timer.loop(750, this, cb_zhong);
        }
        oncardLoop_tou() {
            let sideIndex = 0;
            let indexType = 0;//头道
            let arrayside = this.getActionseat(indexType);
            if (arrayside == null || arrayside.length == 0) {
                this.onshowspecial();
                return;
            }
            let cb = () => {
                let side = arrayside[sideIndex];
                //  console.log(this.getCardIdList(side), "========this.getCardIdList(side)");
                let Type = this.getcardTypes(side)[indexType];
                let scoreDatas = this.getscoreDatas(side)[indexType];
                let scoreDatas_0 = this.getscoreDatas(this.getServerPos(0))[indexType];
                let speScore = this.getspeScore(side);
                let cardList = this.getCardIdList(side)[indexType].split(",");
                if (sideIndex == arrayside.length - 1) {
                    if (this.getspeScore(this.getServerPos(0)) == null) {
                        let score = Tools.inst.TableParseFloat(scoreDatas_0.split(",")[0]) + Tools.inst.TableParseFloat(scoreDatas_0.split(",")[1]);
                        this.Txt_score["tou_score"].visible = true;
                        this.Txt_score["tou_score"].text = score > 0 ? "+" + score.toString() : score.toString();
                    }
                }
                if (speScore == null)
                    this.getPlayer(this.getLocalPos(side)).setCompareCard(indexType, cardList, Type, this.view.getController("location"));


                sideIndex++;
                if (sideIndex == arrayside.length) {
                    Laya.timer.clear(this, cb);
                    //side = 0;
                    this.oncardLoop_zhong()
                }
            }
            Laya.timer.loop(750, this, cb);
            /* let cb_play = () => {
                 Laya.timer.loop(1000, this, cb);
                 indexType++;
                 if (indexType == 2) {
                     Laya.timer.clear(this, cb_play);
                 }
             }
             Laya.timer.loop(1000 * this.playerCount, this, cb_play);*/
        }
        //比牌数据
        onCompare(msgData) {
            // let side=
            // console.log(msgData, "============开始比牌");
            this.isexit = false;
            // let lipaiimg = this.view.getChild("bipaiimg");
            // lipaiimg.visible = true;
            // lipaiimg.asCom.getTransition("t1").play(new Handler(this, function () {
            //     lipaiimg.visible = false;
            // })
            // )
            this.setgamestateTimer(5, null, false);
            SoundMgrShiSanShui.compare();
            this.compare = msgData;
            this.oncardLoop_tou();
        }
        showBalancedatas(isRefresh = false) {
            //  console.log(this.setUserDatas, "111111111111111");
            if (this.setUserDatas != null && this.setUserDatas.length > 0) {
                //然后在玩家头像那里计算分数
                //console.log('000000000000');
                for (let n = 0; n < this.setUserDatas.length; n++) {
                    let oneSetData = this.setUserDatas[n];
                    let setDataSide = this.getLocalPos(oneSetData["side"]);
                    let player = this.getPlayer(setDataSide);
                    player.balanceScore(oneSetData["score"]);
                    player.showshuiScore(oneSetData['w_num']);
                    //if (setDataSide != 0)
                    player.settotal_score(oneSetData["score"]);
                    player.setqiang(oneSetData["descs"][1], oneSetData["descs"][2]);
                    if (isRefresh) {
                        let cardslist = oneSetData['cards'];
                        if (cardslist.length == 1) {
                            player.setSpecial(cardslist[0].split(','));
                        }
                        else {
                            player.setNormalcard(cardslist);
                        }
                        if (setDataSide == 0) {
                            let extend = oneSetData['extend'];
                            if (extend != null && extend.length == 3) {
                                this.Txt_score["tou_score"].visible = true;
                                this.Txt_score["zhong_score"].visible = true;
                                this.Txt_score["wei_score"].visible = true;
                                this.Txt_score["tou_score"].text = extend[0] > 0 ? "+" + extend[0].toString() : extend[0].toString();
                                this.Txt_score["zhong_score"].text = extend[1] > 0 ? "+" + extend[1].toString() : extend[1].toString();
                                this.Txt_score["wei_score"].text = extend[2] > 0 ? "+" + extend[2].toString() : extend[2].toString();
                            }
                        }
                    }
                    // player.setScoreAction(oneSetData["score"]);
                }
            }
        }
        // 倒计时协议
        onRefreshTimeOut(msgData) {
            // console.log("onRefreshTimeOut: ", msgData);

            let waitTime = msgData["wait_time"];

            this.updateTimer(waitTime);
        }

        // 倒计时
        updateTimer(waitTime, cbFunc?) {
            // console.log("进来了倒计时：");

            if (this.gameStateCtl.selectedIndex != 2) {
                //this.gameStateCtl.setSelectedIndex(2);
                this.gameStateCtl.setSelectedIndex(0);
            }

            Laya.timer.clearAll(this.timerBG);

            let timer = this._view.getChild("updateTimer").asCom;
            timer.visible = true;
            let tile = timer.getChild("title").asLabel;
            tile.text = waitTime;

            Laya.timer.loop(1000, this.timerBG, function () {
                waitTime--;
                tile.text = waitTime;
                if (waitTime <= 0) {
                    Laya.timer.clearAll(this.timerBG);
                    timer.visible = false;

                    if (cbFunc) {
                        cbFunc();
                    }
                }
            });
        }

        // 倒计时是否显示
        setTimerBGVisible(show) {
            let timer = this._view.getChild("updateTimer").asCom;
            timer.visible = show;
            Laya.timer.clearAll(this)
        }

        onGoldInfo(msgData, finishedListener) {
            // console.log(msgData, "========onGoldInfo");
            let difen = Tools.inst.changeGoldToMoney(msgData['gold']);    //底分
            let info = ExtendMgr.inst.getText4Language(msgData['info']);     //场次信息
            let partyType = msgData['party_type']; //2:金币场 3：竞技场
            let gamenumber = msgData['gamenumber'] || 'no data';     //牌局编号
            let tfGameInfo = this._view.getChild("tfGameInfo").asLabel;
            tfGameInfo.text = info + "  " + ExtendMgr.inst.getText4Language("底分：") + difen;
            this.Room_no.text = ExtendMgr.inst.getText4Language("牌局编号：") + gamenumber;
            // return this.pass.apply(this, Array.prototype.slice.apply(arguments));
            if (finishedListener) finishedListener();
        }
        /*  pass(msgData, finishedListener) {
              console.log(msgData, arguments);
              if (typeof finishedListener == 'function') return finishedListener();
          }*/

        onGoldExitRoomResult(msgData, finishedListener) {
            //  console.log(msgData, "========562=========S_C_EXIT_ROOM_RESULT");

            this.showRequesting(false);
            if (msgData['result']) {
                UserMgr.inst.returnToLobby();
            } else {
                NetHandlerMgr.netHandler.sendData(ProtoKeyParty.C_S_EXIT_ROOM_CONFIRM);
            }
            if (finishedListener) finishedListener();
        }

        // 获取显示不能参加游戏消息
        onGetMessage(msgData) {
            console.log(msgData);
        }

        // 显示准备手势
        onShowReadyOk(msgData) {
            //  console.log(msgData, "显示准备手势");
        }
        //十三水发牌
        onHasBullOrNot(msgData, finishedListener) {
            // console.log(msgData, "--------发牌----------")

            let cardIdList = msgData["cards"].split(",");
            // console.log(cardIdList, "=============cardIdList");
            let tipsDataList = twa.utils.getTipsDataList(cardIdList);
            //console.log(tipsDataList, "============tipsDataList");
            let typesList = twa.utils.getAutoArrangedCardsData(cardIdList, tipsDataList);
            var data =
            {
                // "time": time,
                "cardIdList": cardIdList,
                "tipsDataList": tipsDataList,
                "typesList": typesList,
                "specialType": msgData["specialType"],
                "typeScore": msgData["typeScore"]
            };
            this.choosedata = data;
            if (!this.isinitChoose) {
                this.onshowChooseManual();
            }
            if (finishedListener) finishedListener();
        }
        //   onServerCountDown(msgData) {
        // console.log(msgData)
        /*Laya.timer.loop(1000,this,function(){
        })*/
        // }
        onStage(msgData) {
            let side = this.getLocalPos(msgData["side"]);
            this.getPlayer(side).setHandCard(1, null);
            let issend_GetArrangedCards = true;
            SoundMgrShiSanShui.ready();
            for (let i = 0; i < this.playerSide.length; i++) {
                if (this.playerSide[i] != null) {
                    let side = this.getLocalPos(this.playerSide[i]);
                    if (this.getPlayer(side).getHardcardstage() != 1) {
                        issend_GetArrangedCards = false;
                        break;
                    }
                }

            }
            if (issend_GetArrangedCards) {
                NetHandlerMgr.netHandler.sendGetArrangedCards()
            }
            if (0 == side) {
                if (this.ischoose != null) {
                    //  console.log("----1111111-----关闭理牌面板");
                    this.ischoose.hide()
                    // this.chooseView.visible = false;
                    // this.chooseBg.visible = false;
                    this.ischoose = null;
                    this.choosedata = null;
                }
            }

        }
        // 重连获得的数据
        onRefreshData(msgData, finishedListener) {
            // console.log("onRefreshData: ", msgData);
            if (finishedListener) finishedListener();
        }
        // 游戏结束
        onGameEnd(msgData, finishedListener) {
            let setData = msgData["setUserDatas"];
            setData["G562page"] = this;
            // if (this.isshowAni && this.setUserDatas.length == 0) {
            // UIMgr.inst.add(G562Balance, null, setData);
            // }
            this.setUserDatas = setData;
            //发送可以开始下一局准备
            NetHandlerMgr.netHandler.sendReadyNextRound();
            if (finishedListener) finishedListener();
        }
        onReset() {
            //  console.log("========重置=========");

            this.reset(true);
            this.Txt_score["tou_score"].visible = false;
            this.Txt_score["zhong_score"].visible = false;
            this.Txt_score["wei_score"].visible = false;


            this.btnContinue.visible = true;
            this.showAutoContTimer();
        }
        onDispose() {
            this.cleargold();
            Laya.timer.clearAll(this);
        }
    }
}