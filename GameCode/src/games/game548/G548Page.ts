module G548 {
    export class G548Page extends Page {
        public isStartGame: boolean;

        protected playerFrames: Array<G548PlayerFrame> = [];
        protected gameTimer: fairygui.GComponent;
        protected gameTimerText: fairygui.GLabel;
        protected gameInfoText: fairygui.GLabel;
        protected exitBtn: fairygui.GButton;
        protected changeRoomBtn: fairygui.GButton;
        protected aniStartGame: fairygui.GComponent;
        protected tipText: fairygui.GLabel;

        protected seconds: number = 0;

        protected isChangeRoom: boolean = false;
        protected roomName: string;
        protected bankerSide: number;
        protected balanceData;

        //----------------JiaTao
        protected btn_bar: fairygui.GComponent;//2018.8.7-------JiaTao
        protected btnList: fairygui.GComponent;
        protected xianH: fairygui.GComponent;
        protected c_bar: fairygui.Controller = null;
        protected c_jetton: fairygui.Controller = null;
        protected c_seat: fairygui.Controller = null;
        //-----------------end
        //private btn_test : fairygui.GButton;
        protected AreaCom: fairygui.GComponent;
        protected jetton_Layout: fairygui.GComponent;
        protected c_jettonBtn: fairygui.Controller = null;

        protected playerSelf: G548PlayerFrame;

        //2019-1-5
        protected c_GameType: fairygui.Controller = null;
        //2019-1-5
        protected gameId: number = 548;
        protected layout: number = 0;
        protected isViewer: boolean = false;
        //-----属性位置规范 2019-1-7
        protected connectToServer: boolean = false;
        protected cashAsMode: 'bitmap';
        protected buttonMode: number = 1;//按钮屏蔽
        protected isRefreshData: boolean = false;
        protected isSwapSeat: boolean = false;
        protected initialX: number = null;
        protected initialY: number = null;
        protected place: number;//下注位置
        protected denomination: number;//下注面额
        protected quantity: number = 1;//下注数量
        protected isInitPlace: boolean = false;
        //用来存储 闲、庄 牌数来判断是否天牌
        protected x_cardNum: number = 0;
        protected z_cardNum: number = 0;
        protected cardList: Array<fairygui.GComponent> = [];
        protected cardValue: Array<string> = [];
        protected xResult: any;
        protected zResult: any;
        protected xianPoint: number;
        protected zhuangPoint: number;
        protected xScore: Array<number> = [];
        protected zScore: Array<number> = [];
        protected xScoreCount: number;
        protected zScoreCount: number;
        protected balanceScore: any;//存放输赢数据
        protected _playerList: any;
        protected _selfInfo: any;
        protected isCloseExitRoomResult: boolean = false;
        protected pointCount: number = 0;//正在匹配点的统计
        protected bidValue: any;


        constructor(G = 'G548', scene = 'GameScene', layer = UILayer.GAME) {
            super('G548', scene, UILayer.GAME);
        }

        clearView() {
            Laya.timer.clearAll(this);
            Laya.Tween.clearAll(this);
            if (this._view != null) {
                this._view.removeChildren();
            }
        }

        onDispose() {
            //console.log('清除缓动');
            this.clearAutoExit();
            this._view.dispose();
            SoundMgrBaccarat.stopBGM();
        }

        onCreated(data: any = null, palyerFrame: any = G548PlayerFrame) {
            //Laya.Stat.show(0,0);
            if (!data) return;
            //this.pageStyleSetting(data);
            //开启背景音乐
            SoundMgrBaccarat.playBGM();

            let view = this.view;
            for (let i = 0; i < 9; i++) {
                this.playerFrames.push(new palyerFrame({
                    side: i,
                    seat: view.getChild('seat' + i).asCom,
                }));
            }

            /*------------------------end------------------------*/
            this.initFairygui();
            this.initDrawcall();
            this.reset();
            //let selfInfo = data['myInfo']['selfInfo'];
            //this.playerFrames[0].setSeat(selfInfo,0);
            //this.onEnterRoomSuccess(data);
            this.playerSelf = this.playerFrames[0];
            this.setSelfseat();
        }

        initFairygui() {
            let view = this.view;

            let url = ResourceMgr.RES_PATH + 'bg/bg6.jpg';
            Tools.inst.changeBackground(url, view.getChild('bg').asLoader);

            this.c_GameType = view.getController('c_GameType');
            this.gameInfoText = view.getChild('gameInfo').asLabel;
            this.changeRoomBtn = view.getChild('btnChangeRoom').asButton;
            this.changeRoomBtn.onClick(this, this.onExchangeRoom.bind(this));
            this.aniStartGame = view.getChild('aniStartGame').asCom;
            this.tipText = view.getChild('txtTip').asLabel;
            /*------------------------JiaTao------------------------*/
            this.btn_bar = view.getChild('btn_bar').asCom;
            this.btnList = view.getChild('btnList').asCom;
            this.xianH = view.getChild('xianH').asCom;
            this.c_bar = view.getController('c_bar');
            this.c_jetton = view.getController('c_jetton');
            this.c_seat = view.getController('c_seat');
            this.AreaCom = view.getChild('comChipRect').asCom;
            this.jetton_Layout = this.AreaCom.getChild('jetton_Layout').asCom;
            this.c_jettonBtn = view.getController('jetton');
            //---新版倒计时
            this.gameTimer = this.AreaCom.getChild('comTimer').asCom;
            this.gameTimerText = this.gameTimer.getChild('title').asLabel;
            this.gameTimer.visible = false;
            //----------------------new
            let c_btnList = this.btnList.getController('c1');
            this.btnList.getChild('open').onClick(this, () => {
                c_btnList.selectedIndex = 1;
            });
            this.btnList.getChild('close').onClick(this, () => {
                c_btnList.selectedIndex = 0;
            });
            this.btnList.getChild('btn_exit').onClick(this, this.onExitRoom.bind(this));
            this.btnList.getChild('btn_setting').onClick(this, () => {
                UIMgr.inst.popup(UI_Setting);
            });
            //----------------------------gameId
            this.btnList.getChild('btn_history').onClick(this, () => {
                let obj = UIMgr.inst.popup(UI_History) as UI_History;
                obj.refreshGameListInGame(this.gameId);
            });

            this.btnList.getChild('btn_rule').onClick(this, () => {
                var rule = UIMgr.inst.popup(UI_Rules) as UI_Rules;
                rule.refreshData('game' + this.gameId);
            });

            this.btnList.getChild('btn_exit_end').onClick(this, () => {
                //let msg = ExtendMgr.inst.language['cn']['tips_exit'];
                let msg = ExtendMgr.inst.getText4Language('游戏过程中不能退出游戏哦,请您先打完这局!');
                Alert.show(msg);
            });

            function strivebtnOnClick(btnName) {
                this.c_bar.selectedIndex = this.layout;
                NetHandlerMgr.netHandler.sendGrabDealerVote(btnName == 'strive');
            }
            this.btn_bar.getChild('strive').onClick(this, strivebtnOnClick, ['strive']);
            this.btn_bar.getChild('strive_no').onClick(this, strivebtnOnClick, ['strive_no']);
        }

        onNetIntoGame(data) {
            this.onEnterRoomSuccess(data);
        }

        setSelfseat() {
            let data = {}
            data['nickname'] = UserMgr.inst._info.name;
            data['headImgUrl'] = UserMgr.inst._info.imgUrl;
            data['coin'] = '';
            this.playerSelf.setSeat(data, 0);
        }

        //------JiaTao
        showTip(type: number, handler?: Handler) {
            this.tipText.visible = true;
            let c_show = this.tipText.getController('c_show');
            let c1 = this.tipText.getController('c1');
            c1.selectedIndex = 1;
            c_show.selectedIndex = type;
            switch (type) {
                case 0:
                    SoundMgrBaccarat.startBidGame();
                    this.c_seat.selectedIndex = 1;
                    this.showBetArea(true);
                    if (!this.isViewer) {
                        this.showJetton();//-----------开启下注按钮
                    }
                    break;
                case 1:
                    this.c_seat.selectedIndex = 0;
                    this.showBetArea(true);
                    break;
                case 2:
                    SoundMgrNiu.gameStart();
                    this.clearTimer();
                    break;
                default:
                    break;
            }
            this.tipText.getTransitionAt(0).play(handler);
        }

        //-------JiaTao Drawcall优化
        initDrawcall() {
            //this.AreaCom.displayObject.cacheAs = this.cashAsMode;
            let name = ['area_1', 'area_2', 'area_4'];
            for (let i = 0; i < 3; ++i) {
                let area = this.AreaCom.getChild(name[i]).asCom;
                area.displayObject.cacheAs = this.cashAsMode;
            }
            for (let i = 0; i < 9; ++i) {
                let seat = this._view.getChild('seat' + i).asCom;
                seat.displayObject.cacheAs = this.cashAsMode;
            }
            this.btnList.displayObject.cacheAs = this.cashAsMode;
            this.btn_bar.displayObject.cacheAs = this.cashAsMode;
            let resultCom = this.AreaCom.getChild('resultCom').asCom;
            resultCom.displayObject.cacheAs = this.cashAsMode;
            let comTimer = this.AreaCom.getChild('comTimer').asCom;
            comTimer.displayObject.cacheAs = this.cashAsMode;
        }
        //-------------JiaTao 按钮屏蔽
        destoryAllBtn() {
            let open = this.btnList.getChild('open').asButton;
            let close = this.btnList.getChild('close').asButton;
            let btn_exit = this.btnList.getChild('btn_exit').asButton;
            let btn_setting = this.btnList.getChild('btn_setting').asButton;
            let btn_rule = this.btnList.getChild('btn_rule').asButton;
            let btn_history = this.btnList.getChild('btn_history').asButton;
            let btnArray = [open, close, btn_exit, btn_setting, btn_rule, btn_history, this.changeRoomBtn];
            for (let i = 0, len = btnArray.length; i < len; ++i) {
                btnArray[i].mode = this.buttonMode;
            }
        }

        showJetton() {//isShowAll = false
            //JiaTao 2019-1-5
            let GameType = this.c_GameType.selectedIndex;
            if (GameType == 0)
                this.c_jetton.selectedIndex = 1;
            else
                this.c_jetton.selectedIndex = 3;
        }
        //-----显示/关闭下注区
        showBetArea(isShow: boolean = false) {
            let index = [1, 2, 4];
            for (let i = 0, len = index.length; i < len; ++i) {
                let ind = index[i];
                let area = this.AreaCom.getChild('area_' + ind).asCom;
                if (!area) continue;
                area.visible = isShow;
            }
        }

        reset() {
            this.posServerSelf = null;
            this.balanceData = null;
            Tools.inst.each(this.playerFrames, (node) => {
                node.clear();
            }, this);
            this.resetGame();
        }

        resetGame() {
            Tools.inst.each(this.playerFrames, (node) => {
                node.resetGame();
            }, this);
        }

        //卸载clickRect下注区绑定事件
        offBtnHandler() {
            this.isInitPlace = false;
            let name = ['area_1', 'area_2', 'area_4'];
            for (let i = 0; i < 3; ++i) {
                let area = this.AreaCom.getChild(name[i]).asCom;//clickRect
                if (area == null) continue;
                let clickRect = area.getChild('clickRect').asCom;
                clickRect.enabled = false;
                clickRect.offClick(this, this.handlerBet);
            }
        }
        //----重置下注区数据
        resetAreaCom() {
            if (this._view == null || this.AreaCom == null) return;
            if (this.isSwapSeat) {
                this.resetSeat(this.bankerSide);
            }
            this.offBtnHandler();
            this.cardList = [];//JiaTao
            this.cardValue = [];//JiaTao
            this.xResult = null;
            this.zResult = null;
            this.xianPoint = null;
            this.zhuangPoint = null;
            this.x_cardNum = null;
            this.z_cardNum = null;
            let resultCom = this.AreaCom.getChild('resultCom').asCom;
            resultCom.getController('c_result').selectedIndex = 0;
            this.AreaCom.getChild('cardLayout').asCom.removeChildren();
            let showCard = this.AreaCom.getChild('showCard').asCom;
            let c_score = showCard.getController('c_score');
            c_score.selectedIndex = 0;
            let c_bg = showCard.getController('c_bg');
            c_bg.selectedIndex = 0;
            for (let i = 0; i < 6; ++i) {
                let Card = showCard.getChild('card_' + i).asCom;
                Card.visible = false;
                Card.icon = G548Page.getCardPath('backface');
            }
            this.showBetArea(false);
            for (let i = 1; i <= 5; ++i) {
                let area = this.AreaCom.getChild('area_' + i).asCom;
                let txtSelfChip = area.getChild('txtSelfChip').asLabel;
                let txtTotalChip = area.getChild('txtTotalChip').asLabel;
                txtSelfChip.text = '0';
                txtTotalChip.text = '0';
                let blink = area.getChild('blink').asCom;
                blink.alpha = 0;
            }
        }

        onEnterRoomSuccess(data) {
            //console.log('进入房间成功---s_c_Connected',data);
            let gameInfo = data['myInfo'];
            //开启匹配动效
            this.clearTimer();
            this.startMatch();
            //断线重连，请求当前游戏数据
            if (gameInfo['isRefresh'])
                this.refreshInfo();
            else
                this.initGame(gameInfo);
        }

        refreshInfo() {
            NetHandlerMgr.netHandler.refreshData((data) => {
                this.isRefreshData = true;
                if (data['result']) {
                    let refreshData = data['data'];
                    let gameInfo = refreshData['gameInfo'];
                    //是否已经初始化过
                    if (this.posServerSelf == null)
                        this.initGame(gameInfo);
                    else
                        this.initRoomInfo(gameInfo['roomInfo']);
                    this.onRefreshGameData();
                }
                else {
                    //退出房间
                }
            });
        }

        initGame(gameInfo) {
            //console.log('initGame',gameInfo);
            this.reset();
            this.initGameInfo(gameInfo);
            let roomInfo = gameInfo['roomInfo'];
            this.initRoomInfo(roomInfo);
        }

        initRoomInfo(roomInfo) {
            let playerList = roomInfo['playerList'];
            Tools.inst.each(playerList, (playerInfo, key) => {
                if (playerInfo != null) {
                    let side = this.getLocalPos(playerInfo['side']);
                    let player = this.getPlayer(side);
                    player.setSeat(playerInfo, side);
                }
            }, this);
            /*                 开始游戏                      */
            this.changeRoomBtn.visible = false;
            NetHandlerMgr.netHandler.sendGameStart();
        }
        getPlayer(side: number, server: boolean = false): G548PlayerFrame {
            if (server) side = this.getLocalPos(side);
            return this.playerFrames[side];
        }

        onRefreshGameData() {
        }

        initMsgListen() {
            //正常消息处理
            NetHandlerMgr.netHandler.addMsgListener(S_C_JOIN_ROOM, this.onPlayerJoin.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_EXIT_ROOM, this.onPlayerExit.bind(this));
            //------------金币场特有
            //串行消息处理
            NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_GOLD_MESSAGE, this.onGoldMessage.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_EXIT_ROOM_RESULT, this.onGoldExitRoomResult.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_IS_GOLD, this.onGoldInfo.bind(this));


            //正常消息处理
            NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_PLAYER_INFO, this.onPlayerGoldInfo.bind(this));

            //----------百家乐 S_C_AFTER_START_BCR
            NetHandlerMgr.netHandler.addMsgListener(S_C_BID_BCR, this.onBid.bind(this));//下注结果
            NetHandlerMgr.netHandler.addMsgListener(S_C_START_GRABDEALER_BCR, this.onStartGrabDealer.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_GRABDEALER_VOTERESULT_BCR, this.onGrabDealer.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_SWAPDEALER_BCR, this.onSwapDealer.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_BALANCEBACCARAT_BCR, this.onBalance.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_AFTERBID_BCR, this.onAfterBid.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_AFTERREFRESh_BCR, this.onAfterRefreshBid.bind(this));
            //---------------JiaTao
            NetHandlerMgr.netHandler.addMsgListener(S_C_SENDSIGN_BCR, this.showSign.bind(this));
            //---------滚动消息
            NetHandlerMgr.netHandler.addMsgListener(S_C_NOTICE, this.notice.bind(this));
            //------开始下注 新加协议 筹码面额和限红
            NetHandlerMgr.netHandler.addMsgListener(S_C_STARTBID, this.startBid.bind(this));//开始下注
            //-------JiaTao
            NetHandlerMgr.netHandler.addMsgListener(S_C_READY_GAMESTART, this.gameReady.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_CANCEL_READY, this.cancleReady.bind(this));
        }

        gameReady(msgData) {
            let leftMS = msgData['leftMS'];
            let str_MS: string = leftMS.toString();
            let temp = str_MS.split('');
            leftMS /= 1000;
            leftMS = parseInt(leftMS.toString());
            if (parseInt(temp[1]) >= 5) {
                leftMS += 1;
            }
            this.clearTimer();
            this.setTimer(leftMS, 0);//0 游戏即将开始
        }

        cancleReady(msgData) {
            this.clearTimer();
            this.startMatch();//开启匹配动效
        }
        //-----是否开启假退出按钮
        btnExitEnd(isOpen: boolean) {
            //----JiaTao 假按钮
            let btn_exit_end = this.btnList.getChild('btn_exit_end').asButton;
            btn_exit_end.visible = isOpen;
            btn_exit_end.enabled = isOpen;
            //----end
        }
        /*//公告广播
        message S_C_Notice {
            required string txt = 1;
            optional fixed32 repeatTimes = 2;
            optional fixed32 repeatInterval = 3;
            required fixed32 id = 4;
        }*/
        notice(msgData) {
            //console.log('关服协议',msgData);
            //let info = msgData['txt'];
            //Alert.show(info);
        }

        onGoldInfo(msgData) {
            //console.log('onGoldInfo',msgData);
            this.connectToServer = true;
            let difen = msgData['gold'];
            difen = Tools.inst.changeGoldToMoney(difen);//----JiaTao 2018-12-6
            let info = msgData['info'];
            let partyType = msgData['party_type'];
            let gamenumber = msgData['gamenumber'] || 'no data';
            let gameInfo_score = this._view.getChild('gameInfo_score').asLabel;

            this.gameInfoText.text = ExtendMgr.inst.getText4Language('牌局编号：') + ExtendMgr.inst.getText4Language(gamenumber);

            gameInfo_score.text = ExtendMgr.inst.getText4Language(info) + ExtendMgr.inst.getText4Language('底分') + ' ' + difen;//' 底分  '
        }

        initGameInfo(gameInfo) {
            //console.log('初始化房间信息',gameInfo);
            //------Jia
            this._playerList = gameInfo['roomInfo']['playerList'];
            this._selfInfo = gameInfo['selfInfo'];
            //-----end
            let roomInfo = gameInfo['roomInfo'];
            let roomId = roomInfo['roomId'];
            let roomSetting = roomInfo['roomSetting'];
            this.roomName = roomInfo['roomName'];

            let selfInfo = gameInfo['selfInfo'];
            this.posServerSelf = selfInfo['side'];
            this.transferServerPos(this.posServerSelf, roomInfo['playerCount']);
            this.initMsgListen();
        }

        onPlayerJoin(msgData) {
            let data = msgData['info'];
            let posServer = data['side'];
            let posLocal = this.getLocalPos(posServer);
            this.getPlayer(posLocal).setSeat(data, posLocal);
        }

        onPlayerExit(msgData) {
            let playerInfo = msgData['info'];
            let posServer = playerInfo['side'];
            let posLocal = this.getLocalPos(posServer);
            this.getPlayer(posLocal).clear();
        }
        //开始抢庄
        onStartGrabDealer(msgData) {
            this.changeRoomBtn.visible = false;
            this.c_seat.selectedIndex = 2;//调整头像位置
            this.c_bar.selectedIndex = 1;//显示抢庄条
            let waitTime: { high: number, low: number, unsigned: boolean } = {
                high: msgData['waitTime']['high'],
                low: msgData['waitTime']['low'],
                unsigned: msgData['waitTime']['unsigned'],
            }
            this.clearTimer();
            this.setTimer(waitTime.low / 1000, 1);////0即将开始 1抢庄 2开始下注 3请亮牌 4匹配 5开始比牌6开始要牌 7正在开牌
            this.aniStartGame.visible = true;
            this.aniStartGame.getTransitionAt(0).play();
            SoundMgrNiu.gameStart();
            SoundMgrNiu.startQiang();
        }

        //服务器广播玩家标记----JiaTao
        showSign(msgData) {
            let PlayerInfo = msgData['PlayerInfo'];
            for (let i = 0, len = PlayerInfo.length; i < len; ++i) {
                let localSide = this.getLocalPos(PlayerInfo[i]['side']);
                if (localSide == 0) {
                    //2019-1-7
                    this.c_bar.selectedIndex = this.layout;
                }
                let player = this.getPlayer(localSide);
                let sign = PlayerInfo[i]['sign'];
                let sex = msgData['PlayerInfo'][i]['sex'];
                let c_showSign = this._view.getChild('sign_' + localSide).asCom.getController('c1');
                switch (sign) {
                    case 1:
                        Laya.timer.frameOnce(i * 5, this, function () {
                            SoundMgrNiu.qiang('', sex);//第一个参数什么都不传，为"抢庄"。strive
                            c_showSign.selectedIndex = 1;
                        }.bind(this), null, false);
                        break;
                    case 2:
                        Laya.timer.frameOnce(i * 5, this, function () {
                            SoundMgrNiu.qiang(0, sex);
                            c_showSign.selectedIndex = 2;
                        }.bind(this), null, false);
                        break;
                    default:
                        Laya.timer.frameOnce(i * 5, this, function () {
                            c_showSign.selectedIndex = sign;
                        }.bind(this), null, false);
                        break;
                }
            }
        }
        //新版换位
        swapSeat(bankerSide: number) {
            if (this.isSwapSeat) return;
            //获取fairygui中bankerside坐标
            this.isSwapSeat = true;
            let bankerCom = this._view.getChild('BankerSide').asCom;
            let x = bankerCom.x;
            let y = bankerCom.y;
            let banker = this._view.getChild('seat' + bankerSide).asCom;
            this.initialX = banker.x;
            this.initialY = banker.y;
            banker.setXY(x, y);
        }
        //换回庄家到原来的位置
        resetSeat(bankerSide: number) {
            if (!this.isSwapSeat) return;
            this.isSwapSeat = false;
            let banker = this._view.getChild('seat' + bankerSide).asCom;
            banker.setXY(this.initialX, this.initialY);
        }
        //抢庄结果
        onGrabDealer(msgData) {
            //2019-1-7
            this.c_bar.selectedIndex = this.layout;
            for (let i = 0; i < 9; ++i) {
                let c_sign = this._view.getChild('sign_' + i).asCom.getController('c1');
                c_sign.selectedIndex = 0;
            }
            //闪光特效
            let localSide = this.getLocalPos(msgData['side']);
            this.bankerSide = localSide;
            let player = this.getPlayer(localSide);
            player.updateBankerState(true);
            player.setLightMark(true);
            SoundMgrNiu.dingzhuang();
            this.initBetBtn();
            this.initPlace();
            //----JiaTao新版换位
            this.swapSeat(this.bankerSide);
        }

        randomJettonLight() {
            let jetton = ['jetton0', 'jetton1', 'jetton2', 'jetton3'];
            let index = parseInt((Math.random() * 4).toString());
            let jettonLight = this._view.getChild(jetton[index]).asCom.getChild('goldLight').asMovieClip;
            jettonLight.playing = true;
            jettonLight.asMovieClip.setPlaySettings(0, -1, 1, -1, Handler.create(this, function () {
                jettonLight.playing = false;
            }.bind(this)));
        }

        initBetBtn() {
            Laya.timer.loop(2000, this, this.randomJettonLight, [], false);//开启扫光 ,[],false
            let jetton = ['jetton0', 'jetton1', 'jetton2', 'jetton3'];//,'jetton20','jetton50'
            for (let i = 0, len = jetton.length; i < len; ++i) {
                let cb = function () {
                    SoundMgrBaccarat.chipClick();
                    let chose = this._view.getChild(jetton[i]).asCom.getChild('title').asLabel.text;
                    chose = parseInt(chose);//以后如果要显示小数的话,需要改动.
                    if (chose != 0) {
                        this.denomination = chose;
                    }
                    else {
                        this.denomination = 1;
                    }
                }
                let btn_jetton = this._view.getChild(jetton[i]).asButton;
                btn_jetton.onClick(this, cb.bind(this), []);
            }
        }

        initPlace() {
            let name = ['area_1', 'area_2', 'area_4'];
            for (let i = 0; i < 3; ++i) {
                let area = this.AreaCom.getChild(name[i]).asCom;//clickRect
                if (area == null) continue;
                let clickRect = area.getChild('clickRect').asCom;
                clickRect.enabled = true;
                if (!this.isInitPlace) {
                    // clickRect.onClick(this,this.handlerBet.bind(this),[i]);
                    clickRect.onClick(this, this.handlerBet, [i]);
                    if (i == 2) {
                        this.isInitPlace = true;
                    }
                }
            }
        }

        handlerBet(index) {
            let place = [1, 2, 4];
            this.place = place[index];
            this.quantity = 1;
            let ind = this.c_jettonBtn.selectedIndex - 1;
            this.denomination = ind >= 0 ? this.bidValue[ind] : null;
            if (!this.place || !this.denomination || !this.quantity) return;
            NetHandlerMgr.netHandler.sendBid(this.place, this.denomination, this.quantity);//位置 面额 数量
        }

        //换位--里面有开始下注的信息 如下注按钮面额的初始化
        onSwapDealer(msgData) { }

        startBid(msgData) {
            this.btnExitEnd(true);
            this.bidValue = msgData['bidValue'];
            let bidTime = msgData['bidTime'];

            for (let i = 0, len = this.bidValue.length; i < len; ++i) {
                let jetton = this._view.getChild('jetton' + i).asCom;
                let score = jetton.getChild('title').asLabel;
                score.text = Tools.inst.changeGoldToMoney(this.bidValue[i]);
            }
            let cb = () => {
                //
            }
            this.showTip(this.bankerSide != 0 ? 0 : 1, Handler.create(this, cb, [], true));
            this.clearTimer();
            bidTime /= 1000;
            bidTime = parseInt(bidTime.toString());
            this.setTimer(bidTime, 2);//0即将开始 1抢庄 2开始下注 3请亮牌 4匹配 5开始比牌6开始要牌 7正在开牌
        }

        ////下注结果
        onBid(msgData) {
            let place = msgData['place'];
            let side = this.getLocalPos(msgData['chair']);
            let denomination = msgData['denomination'];
            let qty = msgData['qty'];//--数量
            let totalplacemoney = msgData['totalplacemoney'];
            let subtotalmoney = msgData['subtotalmoney'];
            let player = this.getPlayer(side);
            this.upPlayerGold(msgData['chair'], denomination);//JiaTao------时时更新玩家分数
            this.flyJetton(place, Tools.inst.changeGoldToMoney(denomination), qty, side);//--下注位置 面额 数量 玩家位置,subtotalmoney,totalplacemoney
            //-----更新下注区分
            let area = this.AreaCom.getChild('area_' + place).asCom;
            let txtSelfChip = area.getChild('txtSelfChip').asLabel;
            let txtTotalChip = area.getChild('txtTotalChip').asLabel;
            txtTotalChip.text = Tools.inst.changeGoldToMoney(totalplacemoney);
            if (side == 0) {
                txtSelfChip.text = Tools.inst.changeGoldToMoney(subtotalmoney);
            } else {
                player.betEffect(side);//头像抖动-动效
            }
        }

        flyJetton(place, denomination, quantity, seat/*,subtotalmoney,totalplacemoney*/) {//下注位置 面额 数量 玩家位置 自己下注额  总下注额
            SoundMgrBaccarat.bets();
            let beginPos: laya.maths.Point;
            let index = 0;//----用来标记用哪一种颜色筹码
            for (let i = 0; i < 4; ++i) {
                let score_str = this._view.getChild('jetton' + i).asCom.getChild('title').asLabel.text;
                //let score = parseInt(score_str);
                if (denomination == score_str) {
                    index = i;
                }
            }
            if (seat == 0) {
                //-----自己下注筹码动
                let jetton = this._view.getChild('jetton' + index).asCom;//--目前denomination是个定值，后面要改.
                let screenPos = this._view.localToGlobal(jetton.x, jetton.y);
                beginPos = this.jetton_Layout.globalToLocal(screenPos.x, screenPos.y);
                let t_bet = jetton.getTransition('t_bet');
                t_bet.play();
            } else {
                let player = this._view.getChild('seat' + seat);
                let screenPos = this._view.localToGlobal(player.x, player.y);
                beginPos = this.jetton_Layout.globalToLocal(screenPos.x, screenPos.y);
            }
            for (let j = 0; j < quantity; ++j) {
                let jetton = fairygui.UIPackage.createObject('G548', 'JettonItem').asCom;
                jetton.displayObject.cacheAs = this.cashAsMode;
                //-----选择筹码颜色
                let c_jetton = jetton.getController('value');
                c_jetton.selectedIndex = index;
                //-----初始化筹码面额
                let title = jetton.getChild('title').asLabel;
                title.text = denomination;
                //c_jetton.selectedPage = denomination.toString();
                jetton.setPivot(0.5, 0.5, true);
                jetton.setXY(beginPos.x, beginPos.y);
                //jetton.setScale(0.7,0.7);
                this.jetton_Layout.addChild(jetton);
                let areaRect = this.AreaCom.getChild('area_' + place).asCom;
                let area = areaRect.getChild('area').asCom;
                let rect: { width: number, height: number } = { width: 41, height: 41 }
                let x = (area.actualWidth - rect.width * 2) < 0 ? area.actualWidth / 2 : (area.actualWidth - rect.width * 2) * Math.random() + rect.width;
                let y = (area.actualWidth - rect.height * 2) < 0 ? area.actualHeight / 2 : (area.actualHeight - rect.height * 2) * Math.random() + rect.height;
                let screenPos = area.localToGlobal(x, y);
                let target = this.jetton_Layout.globalToLocal(screenPos.x, screenPos.y);
                let delay_time = 200 * j;
                Laya.Tween.to(jetton, { x: target.x, y: target.y }, 500, Laya.Ease.strongOut, null, delay_time, false);
            }
        }

        //下注过后的信息 cardrescode 1庄赢2闲赢3和
        onAfterBid(msgData) {
            //this.autoExit();//开启自动退房
            Laya.timer.clear(this, this.randomJettonLight);
            this.clearTimer();
            this.jetton_Layout.displayObject.cacheAs = this.cashAsMode;
            for (let i = 1; i <= 5; ++i) {
                let area = this.AreaCom.getChild('area_' + i).asCom;//clickRect
                if (area == null) continue;
                let clickRect = area.getChild('clickRect').asCom;
                clickRect.enabled = false;
            }
            let cardresStr: string = msgData['cardres'];
            let cardres = JSON.parse(cardresStr);
            let cb = () => {
                this.clearTimer();
                this.setTimer(7, 5);//0即将开始 1抢庄 2开始下注 3请亮牌 4匹配 5开始比牌6开始要牌 7正在开牌
                this.pushCards();
            }
            this.initCardList();
            this.initCardValue(cardres);
            this.showTip(2, Handler.create(this, cb, [], true));
        }

        initCardList() {
            let showCard = this.AreaCom.getChild('showCard').asCom;
            for (let i = 0; i < 6; ++i) {
                let Card = showCard.getChild('card_' + i).asCom;
                this.cardList.push(Card);
            }
        }

        initCardValue(cardres) {
            this.xianPoint = cardres['x'][1];
            this.zhuangPoint = cardres['z'][1];
            let xian = cardres['x'][0];
            let zhuang = cardres['z'][0];
            this.x_cardNum = xian.length;
            this.z_cardNum = zhuang.length;
            this.xResult = cardres['x'][1];
            this.zResult = cardres['z'][1];
            this.initXZscore(xian, zhuang);
            for (let i = 0; i < 3; ++i) {
                let x = xian[i];
                if (!x) {
                    this.cardValue.push('');
                } else {
                    this.cardValue.push(x);
                }
                let z = zhuang[i];
                if (!z) {
                    this.cardValue.push('');
                } else {
                    this.cardValue.push(z);
                }
            }
        }
        //获取闲庄每一张牌所代表的分数 private cardValue : Array<string> = [];
        initXZscore(x_Cards: Array<string>, z_Cards: Array<string>) {
            this.xScore = [];
            this.zScore = [];
            for (let i = 0, len = x_Cards.length; i < len; ++i) {
                let temp1 = x_Cards[i].split('');//用来存储后台发过来的牌值数据，字母数字的组合字符串；
                let temp2 = temp1[0];//取字符串的第一个字符
                let temp3: number = 0;//用来存放最终转换的值
                if (temp2 == 'A') {
                    temp3 = 1;
                } else if (temp2 == 'T' || temp2 == 'J' || temp2 == 'Q' || temp2 == 'K') {
                    temp3 = 0;
                } else {
                    temp3 = parseInt(temp2);
                }
                this.xScore.push(temp3);
            }
            for (let i = 0, len = z_Cards.length; i < len; ++i) {
                let temp1 = z_Cards[i].split('');
                let temp2 = temp1[0];//取字符串的第一个字符
                let temp3: number = 0;//用来存放最终转换的值
                if (temp2 == 'A') {
                    temp3 = 1;
                } else if (temp2 == 'T' || temp2 == 'J' || temp2 == 'Q' || temp2 == 'K') {
                    temp3 = 0;
                } else {
                    temp3 = parseInt(temp2);
                }
                this.zScore.push(temp3);
            }
            // console.log('测试---',x_Cards,z_Cards,this.xScore,this.zScore);
        }
        //重置
        resetXZfen() {
            this.xScoreCount = 0;
            this.zScoreCount = 0;
        }
        //设置闲庄的点数
        setXZscore(index: number, X_Score: fairygui.GLabel, Z_Score: fairygui.GLabel) {
            if (index == 0 || index == 2 || index == 4) {
                let score = parseInt(X_Score.text) + this.xScore[this.xScoreCount++];
                if (score >= 10) {
                    score -= 10;
                } else if (score >= 20) {
                    score -= 20;
                }
                X_Score.text = score.toString();
            } else {
                let score = parseInt(Z_Score.text) + this.zScore[this.zScoreCount++];
                if (score >= 10) {
                    score -= 10;
                } else if (score >= 20) {
                    score -= 20;
                }
                Z_Score.text = score.toString();
            }
        }
        pushCards() {
            this.resetXZfen();
            let cardLayout = this.AreaCom.getChild('cardLayout').asCom;
            let showCard = this.AreaCom.getChild('showCard').asCom;
            let X_Score = showCard.getChild('X_Score').asLabel;
            let Z_Score = showCard.getChild('Z_Score').asLabel;
            let c_bg = showCard.getController('c_bg');
            let c_score = showCard.getController('c_score');
            X_Score.text = '0';
            Z_Score.text = '0';
            c_score.selectedIndex = 1;
            c_bg.selectedIndex = 1;
            let cardIndex = 0;
            let func: () => void;
            let tempFunc = () => {
                if (cardIndex < this.cardList.length) {
                    if (this.cardValue[cardIndex] == '') {
                        cardIndex++;
                        func();
                        return;
                    } else {
                        let poker = fairygui.UIPackage.createObject('G548', 'poker').asCom;
                        poker.setXY(840, 220);//扑克牌出发位置poker.setXY(826,236);
                        poker.setScale(0, 0);
                        cardLayout.addChild(poker);
                        let handler = Handler.create(this, function (poker, ind) {
                            cardLayout.removeChild(poker);
                            SoundMgrBaccarat.cards_dealing();
                            //---JiaTao
                            let Card = showCard.getChild('card_' + cardIndex).asCom;
                            Card.visible = true;
                            let aniReversal = Card.getTransition('reversal');
                            aniReversal.play(Laya.Handler.create(this, func, [], true), 1, 0.1);
                            aniReversal.setHook('center', Handler.create(this, () => {
                                //sound
                                // SoundMgrBaccarat.cards_dealing();
                                this.setXZscore(cardIndex, X_Score, Z_Score);
                                Card.icon = G548Page.getCardPath(this.cardValue[cardIndex++]);
                            }, [], true));
                        }.bind(this), [poker, cardIndex]);
                        //----音效层
                        let soundName = ['xianjia', 'zhuangjia', 'xianjia', 'zhuangjia', 'xian_zhui', 'zhuang_zhui'];
                        SoundMgrBaccarat.playAIsound(soundName[cardIndex]);
                        //----end
                        let endPos = this.cardList[cardIndex];
                        let rotate = 720;
                        if (cardIndex == 4 || cardIndex == 5) {
                            rotate = 630;
                        }
                        let flyTime = [500, 400, 500, 400, 500, 400];
                        let delayTime = [0, 0, 0, 0, 800, 800];
                        SoundMgrBaccarat.pushCard();//发牌声音
                        Laya.Tween.to(poker, { x: endPos.x, y: endPos.y, skewX: 1, skewY: 1, rotation: rotate }, flyTime[cardIndex], Laya.Ease.strongOut, handler, delayTime[cardIndex], false);
                    }//内层

                } else if (cardIndex == this.cardList.length) {
                    let resultCom = this.AreaCom.getChild('resultCom').asCom;
                    let showCard = this.AreaCom.getChild('showCard').asCom;
                    showCard.displayObject.cacheAs = this.cashAsMode;
                    let c_result = resultCom.getController('c_result');
                    //let t_result = resultCom.getTransition('t_result');
                    let t_result: fairygui.Transition;
                    let z_bei = resultCom.getChild('z_bei').asLabel;
                    let x_bei = resultCom.getChild('x_bei').asLabel;
                    let blinkLight: fairygui.Transition;
                    let selectedIndex: number = 0;
                    if (this.zResult > this.xResult) {//庄赢
                        t_result = resultCom.getTransition('t_result');
                        selectedIndex = 1;
                        if (this.zResult == 6) {
                            z_bei.text = '3';
                        } else {
                            z_bei.text = this.zResult.toString();
                        }
                        blinkLight = this.AreaCom.getChild('area_2').asCom.getTransition('blinkLight');
                    } else if (this.zResult < this.xResult) {//闲赢
                        t_result = resultCom.getTransition('t_resultXian');
                        selectedIndex = 2;
                        x_bei.text = this.xResult.toString();
                        blinkLight = this.AreaCom.getChild('area_1').asCom.getTransition('blinkLight');
                    } else if (this.zResult == this.xResult) {//和
                        t_result = resultCom.getTransition('t_resultHe');
                        selectedIndex = 3;
                        blinkLight = this.AreaCom.getChild('area_4').asCom.getTransition('blinkLight');
                    }
                    let handler = Handler.create(this, () => {
                        this.jettonRecycle();
                        this.clearTimer();
                        //this.setTimer(3,7);//0即将开始 1抢庄 2开始下注 3请亮牌 4匹配 5开始比牌6开始要牌 7正在开牌
                    }, []);
                    let onComplete = Handler.create(this, () => {
                        blinkLight.play(handler, 1);//先闪光后回收
                        //-------AI广播结果 
                        let soundName = ['', 'win_zhuang', 'win_xian', 'win_he'];
                        let ind = c_result.selectedIndex;
                        SoundMgrBaccarat.playAIsound(soundName[ind]);
                        //------JiaTao 让扑克和阴影部分消失
                        c_bg.selectedIndex = 0;
                        c_result.selectedIndex = 0;
                        for (let i = 0; i < 6; ++i) {
                            let card = showCard.getChild('card_' + i).asCom;
                            card.visible = false;
                        }
                        //-----end
                    }, []);
                    this.soundAI(t_result, onComplete, c_result, selectedIndex);//JiaTao
                }
            }
            func = tempFunc;
            func();
        }

        //-----声音处理
        //音效->播放时长映射
        protected soundMap = {
            p0: 600, p1: 600, p2: 600, p3: 600, p4: 600,//点
            p5: 600, p6: 600, p7: 600, p8: 600, p9: 600,//点
            win_he: 300, win_xian: 600, win_zhuang: 600,//闲/庄/和赢
            xianjia: 600, zhuangjia: 600,//庄/闲家
            xian_zhui: 1200, zhuang_zhui: 1200,//追加牌
            tian_xian: 1200, tian_zhuang: 1200,//天牌
        }
        soundAI(t_result: fairygui.Transition, onComplete: Handler, c_result: fairygui.Controller, selectedIndex: number) {
            let resultHandler = () => {
                c_result.selectedIndex = selectedIndex;
                t_result.play(onComplete);
            };
            //-------AI广播结果  
            let name: string[];
            if (this.xianPoint >= 8 && this.zhuangPoint >= 8 && this.x_cardNum == 2 && this.z_cardNum == 2) {//庄闲都是天牌
                let x_tian = 'tian_xian';
                let z_tian = 'tian_zhuang';
                let x_soundName = 'p' + this.xianPoint;
                let z_soundName = 'p' + this.zhuangPoint;
                name = [x_tian, x_soundName, z_tian, z_soundName];
            } else if (this.xianPoint >= 8 && this.x_cardNum == 2) {//闲家天牌
                let x_tian = 'tian_xian';
                let x_soundName = 'p' + this.xianPoint;
                let z_soundName = 'p' + this.zhuangPoint;
                name = [x_tian, x_soundName, 'zhuangjia', z_soundName];
            } else if (this.zhuangPoint >= 8 && this.z_cardNum == 2) {//庄家天牌
                let z_tian = 'tian_zhuang';
                let x_soundName = 'p' + this.xianPoint;
                let z_soundName = 'p' + this.zhuangPoint;
                name = ['xianjia', x_soundName, z_tian, z_soundName];
            } else {//庄闲都不是天牌
                let x_soundName = 'p' + this.xianPoint;
                let z_soundName = 'p' + this.zhuangPoint;
                name = ['xianjia', x_soundName, 'zhuangjia', z_soundName];
            }
            let countIndex = 0;
            let tempComplete: () => void;
            let complete = () => {
                countIndex++;
                let len = name.length - 1;
                if (countIndex == len) {
                    let tempName = name[countIndex];
                    SoundMgrBaccarat.playAIsound(tempName);
                    Laya.timer.once(this.soundMap[tempName], this, resultHandler.bind(this));
                } else {
                    let tempName = name[countIndex];
                    SoundMgrBaccarat.playAIsound(tempName);
                    Laya.timer.once(this.soundMap[tempName], this, tempComplete.bind(this));
                }
            };
            tempComplete = complete;
            let tempName = name[countIndex];
            SoundMgrBaccarat.playAIsound(tempName);
            Laya.timer.once(this.soundMap[tempName], this, tempComplete.bind(this));
        }

        //---------JiaTao花色处理
        static treatMentsColor(value: string): string {
            let val = value.split('');
            if (val.length != 2) return value;
            let color = val[1];
            switch (color) {
                case 'a': color = 'd'; break;
                case 'b': color = 'c'; break;
                case 'c': color = 'b'; break;
                case 'd': color = 'a'; break;
                default: color = val[1]; break;
            }
            let pokerValue = val[0] + color;
            return pokerValue;
        }

        static getCardPath(cardId: string) {
            let itemName = 'card_' + cardId;
            let url = fairygui.UIPackage.getItemURL('G548pokers', itemName);
            return url;
        }

        drawCurves_poker(obj, endX, endY) {
            if (this._view.getChild('seat' + this.bankerSide) == null) return;
            let bankerSeat = this._view.getChild('seat' + this.bankerSide).asCom;
            let screenPos = this._view.localToGlobal(bankerSeat.x, bankerSeat.y);
            let endPos = this.jetton_Layout.globalToLocal(screenPos.x, screenPos.y);
            let p1 = new Laya.Point(obj.x, obj.y);
            let p2 = new Laya.Point(obj.x, endY);
            let p3 = new Laya.Point(endX, endY);
            let count = 0;
            let curvePoint = this.CreateBezierPoints([p1, p2, p3], 50);
            let fn = function (sp, point, ind) {
                sp.setXY(point.x, point.y);
                if (ind == 49) {
                    sp.removeFromParent();
                }
            }
            let len = curvePoint.length;
            for (let i = 0; i < len; ++i) {
                Laya.timer.once(20 * i, this, fn, [obj, curvePoint[i], i], false);
            }
        }

        //输赢数据
        onBalance(msgData) {
            //this.c_jetton.selectedIndex = 0;//JiaTao关闭下注按钮
            //JiaTao 2019-1-5
            let GameType = this.c_GameType.selectedIndex;
            if (GameType == 0)
                this.c_jetton.selectedIndex = 0;
            else
                this.c_jetton.selectedIndex = 2;
            this.balanceData = msgData;
            this.balanceScore = msgData;
        }

        jettonToPlayer() {//playerlist
            this.jetton_Layout.removeChildren();
            this.changeRoomBtn.visible = true;
            let isOpen = false;
            let openOnce = false;
            let cb = () => {
                if (this.balanceScore == null) {
                    Laya.timer.once(500, this, cb.bind(this));
                } else {
                    let playerDatas = this.balanceScore['setUserDatas'];
                    for (let i = 0, len = playerDatas.length; i < len; ++i) {
                        let value = playerDatas[i];
                        let side = this.getLocalPos(value['side']);
                        let player = this.getPlayer(side);
                        let score: boolean = value['score'] == 1;//0输了 1赢了
                        let changegold = value['changegold'];
                        let gold = value['gold'];
                        let isDealer = value['isDealer'];
                        player.changeScore(changegold);
                        player.setScoreString(gold);
                        isOpen = this.flyJettonToPlayer(isDealer, score, changegold, side);
                        if (isOpen && !openOnce) {
                            SoundMgrBaccarat.chipFly();
                            openOnce = true;
                        }
                    }
                }//--else结尾
            }//--cb结尾
            cb();
        }

        flyJettonToPlayer(isDealer, score, changegold, side): boolean {
            let isOpen: boolean = false;
            let change = parseFloat(changegold);
            if (!isDealer && score) {//重连时候isDealer为null是为false,!isDealer为true
                if (change <= 0) return;
                isOpen = true;
                if (this._view == null || this._view.getChild('seat' + this.bankerSide) == null) return;
                let bankerSeat = this._view.getChild('seat' + this.bankerSide).asCom;
                let seat = this._view.getChild('seat' + side).asCom;
                if (bankerSeat == null || seat == null) {
                    console.log('error44444', bankerSeat, seat, this.bankerSide);
                    return;//-----白色弹窗
                }
                for (let j = 0; j < 6; ++j) {
                    let jetton = fairygui.UIPackage.createObject('G548', 'JettonItem').asCom;
                    if (jetton == null) continue;
                    jetton.displayObject.cacheAs = this.cashAsMode;
                    let c_jetton = jetton.getController('value');
                    c_jetton.selectedIndex = 0;
                    jetton.setPivot(0.5, 0.5, true);
                    this.jetton_Layout.addChild(jetton);
                    let screenPos_1 = this._view.localToGlobal(bankerSeat.x, bankerSeat.y);
                    let pox = this.jetton_Layout.globalToLocal(screenPos_1.x, screenPos_1.y);
                    jetton.setXY(pox.x, pox.y);
                    let screenPos = this._view.localToGlobal(seat.x, seat.y);
                    let endPos = this.jetton_Layout.globalToLocal(screenPos.x, screenPos.y);
                    let delay_time = 20 * j;
                    Laya.Tween.to(jetton, { x: endPos.x, y: endPos.y }, 800, Laya.Ease.strongOut, Handler.create(this, function (jetton) {
                        this.jetton_Layout.removeChild(jetton);
                    }, [jetton]), delay_time, false);
                }
            }
            return isOpen;
        }

        jettonRecycle() {
            this.btnExitEnd(false);
            if (this._view == null || this._view.numChildren == 0) return;
            let bankerSeat = this._view.getChild('seat' + this.bankerSide).asCom;
            let screenPos = this._view.localToGlobal(bankerSeat.x, bankerSeat.y);
            let endPos = this.jetton_Layout.globalToLocal(screenPos.x, screenPos.y);
            let childNum = this.jetton_Layout.numChildren;
            if (childNum > 0) {
                SoundMgrBaccarat.chipFly();
            } else {
                this.changeRoomBtn.visible = true;
            }
            for (let i = 0; i < childNum; ++i) {
                let jetton = this.jetton_Layout.getChildAt(i);
                let delay_time = Math.random() * 500;
                Laya.timer.once(delay_time, this, this.drawCurves.bind(this), [jetton], false);
                if (i == childNum - 1) {
                    Laya.timer.once(1000, this, this.jettonToPlayer.bind(this), [], false);
                }
            }
        }

        drawCurves(obj) {
            if (this._view.getChild('seat' + this.bankerSide) == null) return;
            let bankerSeat = this._view.getChild('seat' + this.bankerSide).asCom;
            let screenPos = this._view.localToGlobal(bankerSeat.x, bankerSeat.y);
            let endPos = this.jetton_Layout.globalToLocal(screenPos.x, screenPos.y);
            let p1 = new Laya.Point(obj.x, obj.y);
            let p2 = new Laya.Point(460, 380);
            let p3 = new Laya.Point(endPos.x, endPos.y);
            let count = 0;
            let curvePoint = this.CreateBezierPoints([p1, p2, p3], 50);
            let fn = function (sp, point, ind) {
                sp.setXY(point.x, point.y);
                if (ind == 49) {
                    sp.removeFromParent();
                }
            }
            let len = curvePoint.length;
            for (let i = 0; i < len; ++i) {
                Laya.timer.once(10 * i, this, fn, [obj, curvePoint[i], i], false);
            }
        }
        //anchorpoints：贝塞尔基点
        //pointsAmount：生成的点数
        //return 路径点的Array
        CreateBezierPoints(anchorpoints, pointsAmount) {
            //console.log('CreateBezierPoints',anchorpoints,pointsAmount);
            var points = [];
            for (var i = 0; i < pointsAmount; i++) {
                var point = this.MultiPointBezier(anchorpoints, i / pointsAmount);
                points.push(point);
            }
            return points;
        }

        MultiPointBezier(points, t) {
            var len = points.length;
            var x = 0, y = 0;
            var erxiangshi = function (start, end) {
                var cs = 1, bcs = 1;
                while (end > 0) {
                    cs *= start;
                    bcs *= end;
                    start--;
                    end--;
                }
                return (cs / bcs);
            };
            for (var i = 0; i < len; i++) {
                var point = points[i];
                x += point.x * Math.pow((1 - t), (len - 1 - i)) * Math.pow(t, i) * (erxiangshi(len - 1, i));
                y += point.y * Math.pow((1 - t), (len - 1 - i)) * Math.pow(t, i) * (erxiangshi(len - 1, i));
            }
            return { x: x, y: y };
        }
        //-----贝塞尔结束
        //断线重连
        //-------JiaTao
        onAfterRefreshBid(msgData) {//(0:结算阶段,1:抢庄阶段,2:下注阶段,3:倒计时阶段)
            this.btnExitEnd(true);
            let left_MS = msgData['leftMS'];
            let stage = parseFloat(msgData['stage']);
            let voteresult = msgData['voteresult'];
            this.bidValue = msgData['bidValue'];
            switch (stage) {
                case 0:
                    this.showBetArea(true);
                    this.balanceData = msgData['balance'][0];
                    let msg = msgData['balance'][0]['setUserDatas'][0];
                    this.balanceScore = msgData['balance'][0];
                    this.onAfterBid(msg);
                    break;
                case 1:
                    this.c_bar.selectedIndex = 1;
                    break;
                case 2:
                    this.showBetArea(true);;
                    break;
                case 3:
                    this.changeRoomBtn.visible = true;
                    break;
                default:
                    break;
            }
            //--------重连初始化玩家座位
            let myside = this._selfInfo['side'];
            let playerList = this._playerList;
            this.transferServerPos(myside, this.playerCount);
            this.playerFrames.forEach(element => {
                element.resetGame();
                element.clear();
            });
            Tools.inst.each(playerList, (playerInfo, key) => {
                if (playerInfo != null) {
                    let side = this.getLocalPos(playerInfo['side']);
                    let player = this.getPlayer(side);
                    player.setSeat(playerInfo, side);
                }
            }, this);
            //--显示庄家标识
            if (stage == 0 || stage == 2) {
                let side = voteresult[0]['side'];
                let bankerSide = this.getLocalPos(side);
                let player = this.getPlayer(bankerSide);
                player.updateBankerState(true);
                this.bankerSide = bankerSide;
                this.swapSeat(this.bankerSide);
                /*按钮值初始化*/
                let bidValue = msgData['bidValue'];
                for (let i = 0, len = bidValue.length; i < len; ++i) {
                    let jetton = this._view.getChild('jetton' + i).asCom;
                    let score = jetton.getChild('title').asLabel;
                    score.text = Tools.inst.changeGoldToMoney(bidValue[i]);
                }
            }
            //-------如果不是庄的话开启下注功能
            if (this.bankerSide != 0 && stage == 2) {
                this.c_seat.selectedIndex = 1;
                this.showJetton();
                this.initBetBtn();
                this.initPlace();
            }
            this.clearTimer();
            if (stage != 0) {
                let leftMS = parseFloat(msgData['leftMS']) / 1000;//Jia stage 1:抢庄阶段,2:下注阶段
                this.clearTimer();
                this.setTimer(parseInt(leftMS.toString()), stage);//0即将开始 1抢庄 2开始下注 3请亮牌 4匹配 5开始比牌6开始要牌 7正在开牌
            }

            let onbidlist = msgData['onbidlist'];
            for (let i = 0, len = onbidlist.length; i < len; ++i) {
                let value = onbidlist[i];
                let place = value['place'];
                let side = this.getLocalPos(value['chair']);
                let denomination = value['denomination'];
                let qty = value['qty'];//下注位置 面额 数量 玩家位置
                let subtotalmoney = value['subtotalmoney'];
                let totalplacemoney = value['totalplacemoney'];
                this.flyJetton(place, Tools.inst.changeGoldToMoney(denomination), qty, side);
                //--------------更新下注区分数---------------------//
                let areaCom = this.AreaCom.getChild('area_' + place).asCom;
                let txtSelfChip = areaCom.getChild('txtSelfChip').asLabel;
                let txtTotalChip = areaCom.getChild('txtTotalChip').asLabel;
                txtTotalChip.text = Tools.inst.changeGoldToMoney(totalplacemoney);
                if (side == 0) {
                    txtSelfChip.text = Tools.inst.changeGoldToMoney(subtotalmoney);
                }
                //------------------end--------------------------//
            }
        }

        onGoldMessage(msgData) {
            let type = msgData['msg_type'];
            let msg: string = msgData['msg'];

            if (msg) {
                var spindex: number = msg.indexOf('红');
                var str = msg.substring(0, spindex + 1);
                var number = msg.substring(spindex + 1);
                this.xianH.getChild('msg').text = ExtendMgr.inst.getText4Language(str) + number;
            }
            else
                this.xianH.getChild('msg').text = '';

            let self = this;

            if (type == 1 || type == 1002) {
                this.isCloseExitRoomResult = true;
            }
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

        onPlayerGoldInfo(msgData) {
            var playerInfo = msgData['playerInfo'];
            for (var i = 0, len = playerInfo.length; i < len; i++) {
                var oneData = playerInfo[i];
                var side = this.getLocalPos(oneData["side"]);
                var player = this.getPlayer(side);
                player.setScoreString(oneData["possessionOfProperty"]);
            }
        }

        //-----------JiaTao
        upPlayerGold(chair, money) {
            let side = this.getLocalPos(chair);
            let player = this.getPlayer(side);
            player.updateScoreString(money);
        }

        onExitRoom() {
            this.isChangeRoom = false;
            if (this.connectToServer) {
                NetHandlerMgr.netHandler.sendExitRoom();
            } else {
                NoticeView.hide();
                Tools.inst.clearAllTimeout();
                MasterMgr.inst.switch('lobby');
            }
        }

        onExchangeRoom() {
            this.isChangeRoom = true;
            NetHandlerMgr.netHandler.sendChangeRoom((msgData) => { });
        }

        onGoldExitRoomResult(msgData) {
            //console.log('退房回应---',msgData);
            if (this.isCloseExitRoomResult) return;
            if (this.isChangeRoom == true) {
                this.clearAutoExit();
                this.c_jetton.selectedIndex = 0;//JiaTao
                this.c_seat.selectedIndex = 0;//JiaTao
                if (msgData['result']) {
                    this.changeRoomBtn.visible = false;
                    NetHandlerMgr.netHandler.disconnect();
                    this.reset();
                    this.resetAreaCom();
                    var params = NetHandlerMgr.lastConnectParams;
                    NetHandlerMgr.netHandler.connect(params, this.reconnectResult.bind(this));
                }
            }
            else {
                if (msgData['result']) {
                    this.destoryAllBtn();
                    this.clearTimer();
                    UserMgr.inst.returnToLobby();
                } else {
                    NetHandlerMgr.netHandler.sendData(ProtoKeyParty.C_S_EXIT_ROOM_CONFIRM);
                }
            }

        }

        reconnectResult(connected) {
            if (!connected) return;
            let sid = UserMgr.inst.sid;
            NetHandlerMgr.netHandler.enterGame(sid, this.gameId, this.onEnterRoomSuccess.bind(this));
            NetHandlerMgr.inst.initPingListen(G548.S_C_PING);
        }

        startMatch() {
            this.gameTimer.visible = true;
            Laya.timer.clear(this, this.updateTimer);
            let c_timer = this.gameTimer.getController('state');
            c_timer.selectedIndex = 4;
            this.gameTimerText.text = '';
            Laya.timer.loop(500, this, this.updateMatch);
        }

        updateMatch() {
            if (this.pointCount == 3) {
                this.pointCount = 0;
            } else {
                this.pointCount++;
            }
            let point = ['.', '. .', '. . .', ''];
            this.gameTimerText.text = point[this.pointCount];
        }

        setTimer(seconds: number, type: number) {//0即将开始 1抢庄 2开始下注 3请亮牌 4匹配 5开始比牌6开始要牌 7正在开牌
            Laya.timer.clear(this, this.updateMatch);
            Laya.timer.clear(this, this.updateTimer);
            if (!seconds) return;
            let c_timer = this.gameTimer.getController('state');
            c_timer.selectedIndex = type;
            this.seconds = seconds;
            this.gameTimer.visible = seconds >= 0;
            let tempText = ' ' + seconds.toString();
            this.gameTimerText.text = tempText;
            Laya.timer.loop(1000, this, this.updateTimer, [type]);
        }

        updateTimer(type: number) {
            this.seconds--;
            this.gameTimer.visible = this.seconds > 0;
            let tempText = ' ' + this.seconds.toString();
            this.gameTimerText.text = tempText;
            //----添加 3 2 1 音效
            if (type == 1 || type == 2 || type == 0) {
                if (this.seconds >= 1 && this.seconds <= 3) {
                    SoundMgrBaccarat.clockRing();
                }
            }
            if (this.seconds < 0) {
                Laya.timer.clear(this, this.updateTimer);
            }
        }

        clearTimer() {
            let c_timer = this.gameTimer.getController('state');
            c_timer.selectedIndex = 0;
            this.gameTimer.visible = false;
            Laya.timer.clear(this, this.updateTimer);
        }

        autoExit() {
            Laya.timer.once(30000, this, this.onExitRoom.bind(this));
        }
        clearAutoExit() {
            Laya.timer.clear(this, this.onExitRoom);
        }

        /**********setSeat******************/
        protected posServerSelf: number = null;
        protected localPosList: Array<number> = null;
        protected local2serverPos: Array<number> = [];
        protected server2localPos: Array<number> = [];
        public playerCount: number = 0;
        transferServerPos(posServerSelf: number, playerCount: number) {
            this.playerCount = playerCount;
            for (let i = 0; i < this.playerCount; i++) {
                let temp = (i + posServerSelf) % this.playerCount;
                //tempNetworkseat = tempNetworkseat >= this.playerCount ? tempNetworkseat - this.playerCount : tempNetworkseat;
                this.server2localPos[i] = temp;
                this.local2serverPos[temp] = i;
            }
            //console.log('座位测试----',this.server2localPos,this.local2serverPos);
        }
        //-获取本地座位号
        getLocalPos(network_seat) {
            return this.local2serverPos[network_seat]
        }
        //-获取网络座位号
        getServerPos(local_seat) {
            return this.server2localPos[local_seat]
        }
        /*************************** */
    }
} 