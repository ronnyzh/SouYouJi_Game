module G565 {
    export class G565Page extends Page {

        private playerFrames: Array<G565PlayerFrame> = [];
        private gameInfoText: fairygui.GLabel;
        private aniChangeBanker: fairygui.Transition;
        private winImg: fairygui.GImage;
        private winAni: fairygui.Transition;
        private bankerTag: fairygui.GObject;
        private aniStartGame: fairygui.GComponent;
        private cardTypeCom: fairygui.GComponent;
        private btnContinue: fairygui.GButton;
        private timeTip: fairygui.GLabel;
        private fillView: G565BidSlider;
        private deskCard: G565DeskCard;
        private totalPoolText: fairygui.GTextField;
        private poolTexts: Array<ChipText>;
        private chipItemMgr: ChipItemMgr;
        // private sequenceCTL: SequenceCTL;
        private baseScore: number;
        private actionIndex: number;
        private roomName: string;
        private bankerSide: number;
        private totalPoolValue: number;
        private netHandler: G565NetHandler;
        private btnMgr: BtnsMgr;
        private TimerEvt: (player: G565.G565PlayerFrame) => void;
        private TimerMaxEvt: (player: G565.G565PlayerFrame) => void;
        private chipPoi: { x: number, y: number };

        protected autoContTimer: fairygui.GObject;
        protected ctl_autoCont: fairygui.Controller;
        protected autoContTime: number = 3000;


        constructor(scene = 'GameScene') {
            super('G565', scene, UILayer.GAME);
        }

        onDispose() {
            if (this.btnMgr != null) {
                this.btnMgr.onDispose()
            };
            Laya.timer.clearAll(this);
            this.playerFrames.forEach((player) => {
                player.onDispose();
            })
            Laya.stage.off(Laya.Event.KEY_DOWN, this, this.onKeyDown);
        }

        onCreated(data: any = null) {
            if (!data) return;

            let view = this.view;
            for (let i = 0; i < 9; i++) {
                this.playerFrames.push(new G565PlayerFrame({
                    side: i,
                    seat: view.getChild('seat' + i).asCom,
                    seatText: view.getChild('seatText' + i).asCom,
                    parent: this.view,
                }));
            }
            this.gameInfoText = view.getChild('gameInfoText').asLabel;
            this.aniStartGame = view.getChild('aniStartGame').asCom;
            this.bankerTag = view.getChild('floatBankerTag');
            this.aniChangeBanker = view.getTransition('changeBanker');
            this.cardTypeCom = view.getChild('showCardType').asCom;
            this.timeTip = view.getChild('timeTip').asLabel;
            this.btnContinue = view.getChild('btnContinue').asButton;
            this.winImg = view.getChild('winImg').asImage;
            this.winAni = view.getTransition('winAni');
            this.btnMgr = new BtnsMgr(view.getChild('btns').asCom);
            this.fillView = new G565BidSlider(view.getChild('fillView').asCom);
            let chipPoiView = this.view.getChild('chipPoi');
            this.chipPoi = { x: chipPoiView.x, y: chipPoiView.y };
            this.poolTexts = [];
            let poolTextsName = 'pool';
            for (let i = 0; i < 8; i++) {
                this.poolTexts[i] = new ChipText(view.getChild(poolTextsName + i).asLabel);
            }
            this.totalPoolText = this.view.getChild('totalPool').asTextField;
            this.deskCard = new G565DeskCard(view);
            this.chipItemMgr = new ChipItemMgr(view);
            // this.sequenceCTL = new SequenceCTL();

            this.TimerEvt = (player: G565.G565PlayerFrame) => {
                player.TimerValue -= Laya.timer.delta;
                if (player.TimerValue > 0) {
                    Laya.timer.frameOnce(1, this, this.TimerEvt, [player]);
                }
            }

            this.TimerMaxEvt = (player: G565.G565PlayerFrame) => {
                player.TimerMax -= Laya.timer.delta;
                if (player.TimerMax > 0) {
                    Laya.timer.frameOnce(1, this, this.TimerMaxEvt, [player]);
                }
            }


            let lPos = this.bankerTag.localToGlobal(0, 0);
            this.originalBankerPos = fairygui.GRoot.inst.globalToLocal(lPos.x, lPos.y);

            /**继续按钮点击事件 */
            this.btnContinue.onClick(this, this.onExchangeRoom.bind(this));

            /*弃牌按钮点击事件*/
            this.btnMgr.foldBtn.onClick(this, () => {
                this.netHandler.sendNewAction(1, this.actionIndex);
                SoundMgrDeZhou.button();
            });
            /*让牌按钮点击事件*/
            this.btnMgr.yieldBtn.onClick(this, () => {
                this.netHandler.sendNewAction(4, this.actionIndex);
                SoundMgrDeZhou.button();
            });
            /*加注按钮点击事件*/
            this.btnMgr.fillBtn.onClick(this, () => {
                //显示加注进度条
                if (this.fillView.visible) {
                    //if (this.fillView.getAddGoldValue() == this.fillView.addGoldMax)
                    if (this.fillView.getAddGoldValue() == this.fillView.allinNumber) {
                        this.netHandler.sendNewAction(5, this.actionIndex);
                    }
                    else {
                        this.netHandler.sendNewAction(3, this.actionIndex, this.fillView.getAddGoldValue())
                    }
                }
                else {
                    this.fillView.visible = true;
                }
                this.btnMgr.setIsAdd(this.fillView.visible);
                SoundMgrDeZhou.button();
            });
            /*跟按钮点击事件*/
            this.btnMgr.callBtn.onClick(this, () => {
                this.netHandler.sendNewAction(2, this.actionIndex);
                SoundMgrDeZhou.button();
            });
            /*全下按钮点击事件*/
            this.btnMgr.allinBtn.onClick(this, () => {
                this.netHandler.sendNewAction(5, this.actionIndex);
                SoundMgrDeZhou.button();
            });
            /*测试 全下按钮点击事件*/
            this.btnMgr.allinBtn2.onClick(this, () => {
                this.netHandler.sendNewAction(5, this.actionIndex);
                SoundMgrDeZhou.button();
            });

            //游戏按钮
            {
                let uiExitGame = view.getChild('uiExitGame').asCom;
                uiExitGame.getController('gametype').selectedIndex = 1;
                let btn_exit = uiExitGame.getChild('btn_exit').asButton;
                btn_exit.onClick(this, this.onExitRoom.bind(this));
                let btn_setting = uiExitGame.getChild('btn_setting').asButton;
                btn_setting.onClick(this, () => {
                    UIMgr.inst.popup(UI_Setting);
                    SoundMgrDeZhou.button();
                });
                let btn_history = uiExitGame.getChild('btn_history').asButton;
                btn_history.onClick(this, () => {
                    let obj = UIMgr.inst.popup(UI_History) as UI_History;
                    obj.refreshGameListInGame(565);
                    SoundMgrDeZhou.button();
                });
                let btn_rule = uiExitGame.getChild('btn_rule').asButton;
                btn_rule.onClick(this, () => {
                    let rule = UIMgr.inst.popup(UI_Rules) as UI_Rules;
                    rule.refreshData('game565');
                    SoundMgrDeZhou.button();
                });
                // btn_rule.visible = false;
                let btn_proxy = uiExitGame.getChild('btn_proxy').asButton;
                btn_proxy.visible = false;

                //自动继续 判断ui是否有自动继续按钮和倒计时
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
                //
            }

            SoundMgrDeZhou.playBGM();
            this.reset();
            this.setSelfSeat();
            //this.onEnterRoomSuccess(data);

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
        //

        reset() {
            this.posServerSelf = null;
            this.aniStartGame.visible = false;
            this.btnContinue.visible = false;
            this.fillView.visible = false;
            this.btnMgr.setIsAdd(this.fillView.visible);
            this.btnMgr.lastCallNumber = 0;
            this.btnMgr.selectedIndex = 0;
            this.hideCardTypeCom();
            this.hideWinImg();
            this.hideTimeTip();
            this.deskCard.hide();
            // this.sequenceCTL.reset();
            this.setPlayerMask(false, true);
            this.setTotalPoolText(0);
            this.poolTexts.forEach((pool) => {
                pool.Value = 0;
            })
            Tools.inst.each(this.playerFrames, (node: G565PlayerFrame) => {
                node.clear();
            }, this);
        }

        setSelfSeat() {
            let data = {};
            data['nickname'] = UserMgr.inst._info.name;
            data['headImgUrl'] = UserMgr.inst._info.imgUrl;
            data['coin'] = '';
            let selfPlayer = this.getPlayer(0);
            if (selfPlayer.isInit == false) {
                selfPlayer.setSeat(data);
            }
        }

        onNetIntoGame(data) {
            this.netHandler = NetHandlerMgr.netHandler as G565NetHandler;
            this.onEnterRoomSuccess(data);
            Laya.stage.on(Laya.Event.KEY_DOWN, this, this.onKeyDown);
            this.setTimeTip(4, null);
        }


        onEnterRoomSuccess(data) {
            let gameInfo = data['myInfo'];
            //断线重连，请求当前游戏数据
            if (gameInfo['isRefresh'])
                this.refreshInfo();
            else
                this.initGame(gameInfo);
        }

        /**请求断线重连 */
        refreshInfo() {
            this.netHandler.refreshData((data) => {
                if (data['result']) {
                    // WaitingView.hide();
                    let refreshData = data['data'];
                    let gameInfo = refreshData['gameInfo'];
                    //是否已经初始化过
                    if (this.posServerSelf == null)
                        this.initGame(gameInfo, true);
                    else
                        this.initRoomInfo(gameInfo['roomInfo'], true);
                    this.onRefreshGameData();
                    if (refreshData['stage'] == 0 || refreshData['stage'] == -1) {
                        this.setTimeTip(4, null);
                    }
                }
                else {
                    //退出房间
                    UserMgr.inst.returnToLobby();
                }
            });
        }

        initGame(gameInfo, isrefresh = false) {
            this.reset();
            this.initGameInfo(gameInfo);

            let roomInfo = gameInfo['roomInfo'];
            this.initRoomInfo(roomInfo, isrefresh);
        }


        initGameInfo(gameInfo) {
            let roomInfo = gameInfo['roomInfo'];
            let selfInfo = gameInfo['selfInfo'];
            this.posServerSelf = selfInfo['side'];
            let playerCount = roomInfo['playerCount'];
            this.transferServerPos(this.posServerSelf, playerCount);
            this.initMsgListen();

        }

        initRoomInfo(roomInfo, isrefresh = false) {
            // let roomId = roomInfo['roomId'];
            // let roomSetting = roomInfo['roomSetting'];
            this.roomName = ExtendMgr.inst.getText4Language(roomInfo["roomName"]);
            let playerList = roomInfo['playerList'];
            Tools.inst.each(playerList, (playerInfo, key) => {
                if (playerInfo != null) {
                    let side = this.getLocalPos(playerInfo['side']);
                    let player = this.getPlayer(side);
                    player.setSeat(playerInfo, isrefresh ? '0' : '');
                }
            }, this);
        }
        getPlayer(side: number, server: boolean = false) {
            if (server) side = this.getLocalPos(side);
            return side == null ? null : this.playerFrames[side];
        }

        onRefreshGameData() {
        }

        initMsgListen() {
            // // //重写已有接口，先检查是否存在
            // // if (typeof S_C_READY_GAME_DATA != 'undefined') {
            // //     this.netHandler.removeMsgListener(S_C_READY_GAME_DATA);
            // //     this.netHandler.addMsgListener(S_C_READY_GAME_DATA, this.onReadyShow.bind(this));
            // // }


            //------------基本消息
            //串行消息处理
            this.netHandler.addSequenceMsgListener(S_C_SET_START, this.onSetStart.bind(this));
            this.netHandler.addSequenceMsgListener(S_C_BALANCE, this.onBalance.bind(this));

            //正常消息处理
            this.netHandler.addMsgListener(S_C_JOIN_ROOM, this.onPlayerJoin.bind(this));
            this.netHandler.addMsgListener(S_C_EXIT_ROOM, this.onPlayerExit.bind(this));
            //this.netHandler.addMsgListener(S_C_CONNECTED, this.onEnterRoomSuccess.bind(this));

            //this.netHandler.addMsgListener(S_C_ONLINE_STATE, this.onUpdateOnlineState.bind(this));
            //this.netHandler.addMsgListener(S_C_NOTICE, this.onNotice.bind(this));
            //this.netHandler.addMsgListener(S_C_GAME_START_RESULT, this.onGameStartResult.bind(this));

            //------------金币场特有
            //串行消息处理
            this.netHandler.addSequenceMsgListener(ProtoKeyParty.S_C_GOLD_MESSAGE, this.onGoldMessage.bind(this));
            this.netHandler.addSequenceMsgListener(S_C_EXIT_ROOM_RESULT, this.onGoldExitRoomResult.bind(this));
            this.netHandler.addSequenceMsgListener(ProtoKeyParty.S_C_IS_GOLD, this.onGoldInfo.bind(this));
            this.netHandler.addMsgListener(S_C_READY_GAMESTART, this.onReadyGameStart.bind(this));



            //正常消息处理
            // this.netHandler.addMsgListener(ProtoKeyParty.S_C_PAY, this.onGoldPay.bind(this));
            this.netHandler.addMsgListener(ProtoKeyParty.S_C_PLAYER_INFO, this.onPlayerGoldInfo.bind(this));

            // //----------德州
            this.netHandler.addMsgListener(S_C_CANDOACTIONS, this.onCanDoActions.bind(this));
            this.netHandler.addSequenceMsgListener(S_C_CANDOACTIONS, this.onCanDoActions2.bind(this));
            this.netHandler.addSequenceMsgListener(S_C_SENDRANDOMTILE, this.onGetRandomTile.bind(this));
            this.netHandler.addSequenceMsgListener(S_C_DEAL_CARDS, this.onDealCards.bind(this));
            this.netHandler.addSequenceMsgListener(S_C_NEWDOACTION, this.onNewDoAction.bind(this));
            this.netHandler.addSequenceMsgListener(S_C_SHOWPUBLICTIOLES, this.onShowPublicTiles.bind(this));
            this.netHandler.addSequenceMsgListener(S_C_SHOWTILES, this.onShowTiles.bind(this));
            this.netHandler.addSequenceMsgListener(S_C_PAYBASEBETS, this.onPayBaseBets.bind(this));
            this.netHandler.addSequenceMsgListener(S_C_NEWREFRESHDATAS, this.onNewRefreshDatas.bind(this));
            this.netHandler.addSequenceMsgListener(S_C_SENDEACHPOOLS, this.onSendEachPools.bind(this));
            this.netHandler.addMsgListener(S_C_GOLDUPDATE, this.updateGold.bind(this));

        }

        ///////////游戏流程相关/////////////////////////////////////////////////////////////////////////////////////////


        /**额外的断线重连数据 */
        onNewRefreshDatas(msgData, finishedListener) {
            // this.sequenceCTL.push(msgData, (msgData: { state: number, totalBid?: number, dealSide?: number, tilesDatas: { player: Array<{ side: number, type: number, tiles: Array<string>, rank: number, selfTiles: Array<string> }> }, playerDatas: Array<{ side: number, lastState?: number, TotalBid?: number, curBid?: number, winGold?: number, beforeGold?: number, lastGold?: number }> }, finishedListener: Function) => {
            //庄家
            if (msgData.dealSide != null) {
                this.setBanker(msgData.dealSide, false);
            }
            //总池分数
            if (msgData.totalBid != null && msgData.state == 1) {
                this.setTotalPoolText(msgData.totalBid);
            }
            let selfPlayer = this.getPlayer(0);
            //恢复手牌和名堂
            {
                //获得亮牌下标的方法
                let getMaskArray = (tiles: Array<string>, handCardIds: Array<string>, deskCardIds: Array<string>) => {
                    let showHandCardIndexs: Array<boolean> = [];
                    let showDeskCardIndexs: Array<boolean> = [];
                    for (let i = 0; i < tiles.length; i++) {
                        let isBreak = false;
                        let tile = tiles[i];
                        for (let j = 0; j < 2; j++) {
                            let cardId = handCardIds[j];
                            if (cardId == tile) {
                                showHandCardIndexs[j] = true;
                                isBreak = true;
                                break;
                            }
                        }
                        for (let j = 0; j < deskCardIds.length; j++) {
                            if (isBreak) { break; }
                            let cardId = deskCardIds[j];
                            if (cardId == tile) {
                                showDeskCardIndexs[j] = true;
                                break;
                            }
                        }
                    }
                    return { showHandCardIndexs, showDeskCardIndexs };
                };
                //恢复所有玩家默认手牌
                this.playerFrames.forEach((player, side) => {
                    if (player.visible == true) {
                        let handCard0 = player.getHandCardIdList()[0];
                        if (handCard0 == '' || handCard0 == null) {
                            player.setMiniHandCard(['', '']);
                        }
                    }
                });
                if (msgData.tilesDatas != null) {
                    //恢复有数据的手牌 恢复名堂
                    let deskCardIds = this.deskCard.getCardIdList();
                    let winType: number = null;
                    let playerDeskCardIndexs = [false, false, false, false, false];
                    msgData.tilesDatas.player.forEach((data, index) => {
                        let handCardIds: Array<string> = data.selfTiles;
                        if (handCardIds[0] != null && handCardIds[0] != '') {
                            let side = this.getLocalPos(data.side);
                            let rank = data.rank;
                            let player = this.getPlayer(side);
                            let isWin = false;
                            let showType = data.type;
                            let playerHandCardIndexs = [false, false];
                            player.hideMiniHandCard();
                            player.setHandCard(handCardIds);
                            if (msgData.tilesDatas.player.length > 1 && rank == 1 || msgData.tilesDatas.player.length == 1) {
                                let { showHandCardIndexs, showDeskCardIndexs } = getMaskArray(data.tiles, handCardIds, deskCardIds);
                                playerHandCardIndexs = showHandCardIndexs;
                                playerDeskCardIndexs = showDeskCardIndexs;
                                winType = data.type;
                                isWin = true;
                            }
                            if (msgData.tilesDatas.player.length > 1) {
                                player.win(isWin);
                                if (side == 0 && isWin == true) {
                                    this.showWinAni(false);
                                }
                            }
                            if (msgData.tilesDatas.player.length == 1 && (data.selfTiles == null || data.type == null)) {
                                let num1 = handCardIds[0].substring(0, 1);
                                let num2 = handCardIds[1].substring(0, 1);
                                if (num1 == num2) {
                                    selfPlayer.setHandCardMask([true, true], 9);
                                }
                                else {
                                    let temp = G565CardItem.compareCard(handCardIds[0], handCardIds[1]);
                                    selfPlayer.setHandCardMask(temp ? [false, true] : [true, false], 10);
                                }
                            } else {
                                player.setHandCardMask(playerHandCardIndexs, showType);
                            }
                        }
                    });
                    this.deskCard.setMask(playerDeskCardIndexs.slice(0, deskCardIds.length), true);
                    if (winType == 1 || winType == 2 || winType == 3 || winType == 4) {
                        this.showCardTypeCom(winType, false);
                    }
                }
            }
            if (msgData.state == 1) {
                //恢复玩家下注和状态
                if (msgData.playerDatas != null && msgData.playerDatas.length > 0) {
                    msgData.playerDatas.forEach((data, index) => {
                        let side = this.getLocalPos(data.side);
                        let curBid = data.curBid;
                        let TotalBid = data.TotalBid;
                        let lastState = data.lastState;
                        let player = this.getPlayer(side);
                        if (curBid != 0) {
                            player.bid(curBid);
                        }
                        player.AllCallNumber = TotalBid;
                        this.btnMgr.lastCallNumber = this.btnMgr.lastCallNumber < player.bidNumber ? player.bidNumber : this.btnMgr.lastCallNumber;
                        player.State = lastState;
                        if (player.State == 5) {
                            this.setPlayerAllinMask(side);
                        } else if (player.State == 1) {
                            this.setPlayerFold(side);
                        }
                    });
                    this.btnMgr.CallNumber = this.btnMgr.lastCallNumber - selfPlayer.bidNumber;
                    if (this.btnMgr.State != 1 && selfPlayer.State != 1 && selfPlayer.State != 5) {
                        this.btnMgr.State = 2;
                    }
                }
            }

            if (finishedListener) { finishedListener() };
            // });
        }

        /**结算 */
        onBalance(msgData, finishedListener) {
            // this.sequenceCTL.push(msgData, (msgData: { setUserDatas: Array<{ side: number, isWin: boolean, score: number }> }, finishedListener: Function) => {
            this.hideTimeTip();
            let cb = () => {
                let addScoreSideList = [];
                let addScoreList = [];
                let allMoveOverEvt = () => {
                    this.btnMgr.State = 0;
                    this.btnContinue.visible = true;
                    this.showAutoContTimer();
                    if (finishedListener) { finishedListener(); }
                }
                this.setPlayerMask(false, true);
                for (let i = 0; i < msgData.setUserDatas.length; i++) {
                    let data = msgData.setUserDatas[i];
                    let side = this.getLocalPos(data.side);
                    let score = data.score;
                    let player = this.getPlayer(side);
                    player.State = 0;
                    player.hideBid();
                    if (score > 0) {
                        addScoreSideList.push(side);
                        addScoreList[side] = score;
                    }
                    player.changeScore(score);
                }
                this.poolTexts.forEach((pool) => {
                    pool.Value = 0;
                })
                this.setTotalPoolText(0);
                let moveGold = () => {
                    SoundMgrDeZhou.gold();
                    if (addScoreSideList.length > 0) {
                        for (let i = 0; i < addScoreSideList.length; i++) {
                            let side = addScoreSideList[i];
                            let player = this.getPlayer(side);
                            this.distributionChip(this.chipPoi, player.getChipPoi(), addScoreList[side], 0.75, (isOver: Boolean) => {
                                if (isOver) {
                                    allMoveOverEvt()
                                }
                            }, i == addScoreSideList.length - 1);
                        }
                        SoundMgrDeZhou.chipfly();
                    }
                    else {
                        allMoveOverEvt();
                    }
                }
                if (this.getPlayer(0).getWinValue() == true) {
                    this.showWinAni(true, moveGold);
                } else {
                    moveGold();
                }
            }
            this.centralizeChip(cb);
            // });
            if (finishedListener) { finishedListener(); }
        }

        /**显示每个玩家的手牌和牌型 */
        onShowTiles(msgData, finishedListener) {
            // this.sequenceCTL.push(msgData, (msgData: { player: Array<{ side: number, type: number, tiles: Array<string>, rank: number, selfTiles: Array<string>, fiveTiles: Array<string>, isShow: boolean }> }, finishedListener: Function) => {
            if (msgData.player.length > 1) {
                this.deskCard.setMask([false, false, false, false, false]);
                this.getPlayer(0).setHandCardMask([false, false], 0);
            }
            let showHandCardPlayerNum = 0;
            let deskCardIds = this.deskCard.getCardIdList();
            let openCardOverEvt = (cardIndex: number, showHandCardIndexs: { [key: number]: Array<boolean> }, showDeskCardIndexs: { [key: number]: Array<boolean> }, type: number, winSide: { [key: number]: boolean }, winType: number) => {
                if (cardIndex == 1) {
                    showHandCardPlayerNum++;
                    if (showHandCardPlayerNum == msgData.player.length - 1) {
                        /**开牌完 */
                        for (let k = 0; k < msgData.player.length; k++) {
                            let data = msgData.player[k];
                            let side = this.getLocalPos(data.side);
                            let player = this.getPlayer(side);
                            if (winSide[side] == true) {
                                player.win(true);
                                this.deskCard.setMask(showDeskCardIndexs[side].slice(0, deskCardIds.length), true);
                            }
                            player.setHandCardMask(showHandCardIndexs[side], type[side]);
                            if ((winType == 1 || winType == 2 || winType == 3 || winType == 4) && k == msgData.player.length - 1) {
                                this.showCardTypeCom(winType, true, Handler.create(this, () => {
                                    if (finishedListener && k == msgData.player.length - 1) { finishedListener(); }
                                }));
                            } else if (k == msgData.player.length - 1) {
                                if (finishedListener && k == msgData.player.length - 1) { finishedListener(); }
                            }
                        }
                    }
                }
            }

            let winSide: { [key: number]: boolean } = {};
            let showHandCardIndexs: { [key: number]: Array<boolean> } = {};
            let showDeskCardIndexs: { [key: number]: Array<boolean> } = {};
            let showType: { [key: number]: number } = {};
            let winType: number = null;
            for (let i = 0; i < msgData.player.length; i++) {
                let data = msgData.player[i];
                let side = this.getLocalPos(data.side);
                let player = this.getPlayer(side);
                let handCardIds: Array<string> = ['', ''];
                showType[side] = data.type;
                showHandCardIndexs[side] = [false, false];
                showDeskCardIndexs[side] = [false, false, false, false, false];
                winSide[side] = false;

                if (msgData.player.length > 1 && data.isShow == true || msgData.player.length == 1) {

                    if (msgData.player.length == 1 || side == 0) {
                        handCardIds = player.getHandCardIdList();
                    }
                    if (handCardIds[0] == '') {
                        handCardIds = data.selfTiles;
                    }

                    for (let i = 0; i < data.fiveTiles.length; i++) {
                        let isBreak = false;
                        let tile = data.fiveTiles[i];
                        for (let j = 0; j < 2; j++) {
                            let cardId = handCardIds[j];
                            if (cardId == tile) {
                                showHandCardIndexs[side][j] = true;
                                isBreak = true;
                                break;
                            }
                        }
                        for (let j = 0; j < deskCardIds.length; j++) {
                            if (isBreak) { break; }
                            let cardId = deskCardIds[j];
                            if (cardId == tile) {
                                showDeskCardIndexs[side][j] = true;
                                break;
                            }
                        }
                    }
                    winSide[side] = true;
                    winType = showType[side];
                }

                if (msgData.player.length > 1) {
                    player.win(false);
                    if (side != 0) {
                        let handCardIds = data.selfTiles;
                        for (let j = 0; j < 2; j++) {
                            player.showHandCard(j, handCardIds[j], openCardOverEvt, [j, showHandCardIndexs, showDeskCardIndexs, showType, winSide, winType]);
                        }
                    }
                }
                else {
                    let handCard0 = player.getHandCardIdList()[0];
                    if (handCard0 == '' || handCard0 == null) {
                        player.setHandCard(handCardIds);
                    }
                    player.setHandCardMask(showHandCardIndexs[side], showType[side]);
                    this.deskCard.setMask(showDeskCardIndexs[side].slice(0, deskCardIds.length), true);
                    if (finishedListener) { finishedListener(); }
                }
            }
            // });
        }

        /**发桌面上的公共牌*/
        onShowPublicTiles(msgData, finishedListener) {
            // this.sequenceCTL.push(msgData, (msgData: { len: number, tiles: Array<string>, addTiles: Array<string> }, finishedListener: Function) => {
            this.btnMgr.lastCallNumber = 0;
            if (msgData.addTiles.length == 0) {
                this.deskCard.setDeskCard(msgData.tiles);
                if (finishedListener) { finishedListener(); }
            }
            else {
                //发牌方法
                let currentIndex = msgData.len - msgData.addTiles.length;
                for (let i = 0; i < msgData.addTiles.length; i++) {
                    Laya.timer.frameOnce(6 * i, this, (deskCardIndex) => {
                        this.deskCard.showDeskCard(currentIndex + deskCardIndex, msgData.addTiles[deskCardIndex], Handler.create(this, (isOver: boolean) => {
                            if (isOver) {
                                this.playerFrames.forEach((player, index, array) => {
                                    if (player.State != 5 && player.State != 1) {
                                        player.State = 0;
                                    }

                                });
                                if (finishedListener) {
                                    finishedListener();
                                }
                            }
                        }, [deskCardIndex == msgData.addTiles.length - 1]));
                        SoundMgrDeZhou.fapai();
                    }, [i]);
                }
            }
            // });
        }

        /**主边池 */
        onSendEachPools(msgData, finishedListener) {
            // this.sequenceCTL.push(msgData, (msgData: { PoolDatas: Array<{ poolId: number, goldTotal: number, chairs: Array<number> }> }, finishedListener: Function) => {
            let cb = () => {
                let lineNumber: number = msgData.PoolDatas.length > 5 ? 5 : msgData.PoolDatas.length;
                let poolIds: Array<number> = [];
                for (let i = 0; i < msgData.PoolDatas.length; i++) {
                    const data = msgData.PoolDatas[i];
                    poolIds.push(data.poolId);
                }
                for (let i = 0; i < this.poolTexts.length; i++) {
                    let pool = this.poolTexts[i];
                    if (poolIds.indexOf(i) != -1) {
                        pool.Value = msgData.PoolDatas[i].goldTotal;
                        if (i < 5) {
                            pool.view.x = this.chipPoi.x - pool.view.actualWidth * (lineNumber / 2 - i);
                        }
                    }
                    else {
                        pool.Value = 0;
                    }
                }
                if (finishedListener != null) {
                    finishedListener();
                }
            }
            this.centralizeChip(cb);
            // });
        }

        /**@做了啥 action 1 弃牌; 2 跟注; 3 加注; 4 过牌; 5 全压; number 下注金额(跟注|加注|全压)*/
        onNewDoAction(msgData, finishedListener) {
            // this.sequenceCTL.push(msgData, (msgData: { side: number, action: number, datas: Array<string>, number: number }, finishedListener: Function) => {
            let side = this.getLocalPos(msgData.side);
            let player = this.getPlayer(side);
            if (side == 0) {
                this.fillView.visible = false;
                this.btnMgr.setIsAdd(this.fillView.visible);
            }

            //切换单选按钮
            if (side == 0 && player.State != 5 && player.State != 1) {
                this.btnMgr.State = 2;
                this.btnMgr.subState = 0;
            }

            //显示头像上的状态
            player.State = msgData.action;
            if (player.State == 5) {
                this.setPlayerAllinMask(side);
                SoundMgrDeZhou.allin_effect();
            } else if (player.State == 1) {
                this.setPlayerFold(side);
                SoundMgrDeZhou.foldpai();
            }
            //去掉头像红圈
            this.setPlayerMask(false, false);

            //下注筹码动画
            if (msgData.action == 2 || msgData.action == 3 || msgData.action == 5) {
                this.bid(side, msgData.number, msgData.action == 3 || msgData.action == 5, () => {
                    if (finishedListener) { finishedListener(); }
                });
            }
            else {
                if (finishedListener) { finishedListener(); }
            }
            // });
        }

        /**发手牌 */
        onDealCards(msgData, finishedListener) {
            // this.sequenceCTL.push(msgData, (msgData: { cards: string, isReDeal?: boolean }, finishedListener: Function) => {
            let dealCardSides = [];
            this.playerFrames.forEach((player, index, Array) => {
                if (player.visible) {
                    dealCardSides.push(index);
                }
            });
            let selfHandCardIds = msgData.cards.split(',')
            this.dealCard(0, dealCardSides, selfHandCardIds, () => {
                if (finishedListener) { finishedListener() };
            }, 0.3);
            // });
        }

        /**决定庄家 */
        onGetRandomTile(msgData, finishedListener) {
            // this.sequenceCTL.push(msgData, (msgData: { tiles: string, side?: number }, finishedListener: Function) => {
            if (msgData.side != null) {

                let side = this.getLocalPos(msgData.side);
                this.setBanker(side, true, () => {
                    if (finishedListener) { finishedListener() }
                });
            }
            else {
                //console.log('onGetRandomTile msgData.side is null');
                if (finishedListener) { finishedListener() }
            }
            // });
        }

        onCanDoActions(msgData) {
            let side = this.getLocalPos(msgData.side);
            let player = this.getPlayer(side);
            player.TimerMax = msgData.leftMs;
            Laya.timer.frameOnce(1, this, this.TimerMaxEvt, [player]);

        }

        /**可以做啥 actions action 1 弃牌; 2 跟注; 3 加注; 4 让牌; 5 全压 */
        onCanDoActions2(msgData, finishedListener) {

            // this.sequenceCTL.push(msgData, (msgData: { side: number, leftMs?: number, num?: number, actions: Array<{ action: number, datas: Array<number> }> }, finishedListener: Function) => {
            let side = this.getLocalPos(msgData.side);
            let player = this.getPlayer(side);
            //player.TimerMax = msgData.leftMs;
            this.setPlayerMask(true, false, side);
            player.State = 0;
            this.actionIndex = msgData.num;
            let isCanPass: boolean = false;
            let isCanCall: boolean = false;
            let isCanAdd: boolean = false;
            let isCanAllin: boolean = false;

            let callNumber: number = 0;
            let addMin: number;
            let addMax: number;
            let allinNumber: number;

            for (let i = 0; i < msgData.actions.length; i++) {
                let data = msgData.actions[i];
                if (data.action == 2) {
                    isCanCall = true;
                    callNumber = data.datas[0];
                } else if (data.action == 3) {
                    isCanAdd = true;
                    addMin = data.datas[0];
                    addMax = data.datas[1];
                }
                else if (data.action == 4) {
                    isCanPass = true;
                }
                else if (data.action == 5) {
                    isCanAllin = true;
                    allinNumber = data.datas[0];
                }
            }

            if (side == 0) {
                if (isCanAdd) {
                    this.fillView.addGoldMin = addMin;
                    this.fillView.addGoldMax = addMax;
                }
                if (isCanAllin) {
                    this.fillView.allinNumber = allinNumber;
                }
                else {
                    this.fillView.allinNumber = -1;
                }
                if (isCanPass) {
                    this.btnMgr.subState = 0;
                }
                else if (isCanAllin && !isCanAdd && !isCanCall) {
                    this.btnMgr.subState = 2;
                }
                else if (isCanCall && !isCanAdd) {
                    this.btnMgr.subState = 3;
                } else if (isCanCall) {
                    this.btnMgr.subState = 1;
                }


                if (this.btnMgr.CallNumber != callNumber) {
                    this.btnMgr.CallNumber = callNumber;
                }

                this.btnMgr.State = 1;
                //根据单选按钮自动操作
                switch (this.btnMgr.selectedIndex) {
                    case 1:
                        if (isCanPass)
                            this.netHandler.sendNewAction(4, this.actionIndex);
                        else
                            this.netHandler.sendNewAction(1, this.actionIndex);
                        break;
                    case 2:
                        this.netHandler.sendNewAction(2, this.actionIndex);
                        break;
                    case 3:
                        if (isCanPass)
                            this.netHandler.sendNewAction(4, this.actionIndex);
                        else if (isCanCall) {
                            this.netHandler.sendNewAction(2, this.actionIndex);
                        } else if (isCanAllin) {
                            this.netHandler.sendNewAction(5, this.actionIndex);
                        }

                        break;
                    case 4:
                        if (isCanPass)
                            this.netHandler.sendNewAction(4, this.actionIndex);
                        break;
                    case 5:
                        this.netHandler.sendNewAction(5, this.actionIndex);
                        break;
                    default:
                        break;
                }
                this.btnMgr.selectedIndex = 0;
            }
            else {
                if (this.btnMgr.lastCallNumber != 0) {
                    if (this.btnMgr.CallNumber != this.btnMgr.lastCallNumber - this.getPlayer(0).bidNumber) {
                        this.btnMgr.CallNumber = this.btnMgr.lastCallNumber - this.getPlayer(0).bidNumber;
                    }
                    let selfPlayer = this.getPlayer(0);
                    if (selfPlayer.State != 1 && selfPlayer.State != 5) {
                        this.btnMgr.State = 2;
                    }
                }
            }
            if (finishedListener) { finishedListener(); }
            // });
        }

        /**决定大小盲注*/
        onPayBaseBets(msgData, finishedListener) {
            // this.sequenceCTL.push(msgData, (msgData: { Ptype: number, chair: number, money: number }, finishedListener: Function) => {
            let side = this.getLocalPos(msgData.chair);
            let player = this.getPlayer(side);
            let selfPlayer = this.getPlayer(0);
            if (msgData.Ptype == 1) {
                player.State = 10;
            }
            else if (msgData.Ptype == 2) {
                player.State = 11;
            }
            player.bid(msgData.money);
            this.btnMgr.lastCallNumber = this.btnMgr.lastCallNumber < player.bidNumber ? player.bidNumber : this.btnMgr.lastCallNumber;
            this.setTotalPoolText(this.totalPoolValue + msgData.money)
            this.btnMgr.CallNumber = msgData.money - player.bidNumber;

            if (side != 0) {
                if (selfPlayer.getScore() - selfPlayer.AllCallNumber <= this.btnMgr.lastCallNumber) {
                    this.btnMgr.subState = 2;
                } else {
                    this.btnMgr.subState = 1;
                }
            } else {
                this.btnMgr.subState = 0;
            }
            this.btnMgr.State = 2;

            if (finishedListener) { finishedListener(); }
            // });
        }

        /**更新分数 */
        updateGold(msgData) {
            //console.log('updateGold', msgData);
            let playerinfo = msgData['playerinfo'];
            playerinfo.forEach((oneData) => {
                let player = this.getPlayer(oneData['side'], true);//Method.getPlayerServer(oneData['side']);
                if (player)
                    player.setScoreString(oneData['score']);
            })
        }

        /**开始游戏 */
        onSetStart(msgData, finishedListener) {
            // this.sequenceCTL.push(msgData, (msgData: { player: Array<{ side: number, type: number, tiles: Array<string>, rank: number }> }, finishedListener: Function) => {
            this.playGameStartAni(Handler.create(this, () => {
                this.aniStartGame.visible = false;
                if (finishedListener) finishedListener();
            }));
            this.hideTimeTip();
        }

        /**即将开始游戏 */
        onReadyGameStart(msgData: { leftMS: number }) {
            this.setTimeTip(0, msgData.leftMS);
        }

        distributionChip(startPoi: { x: number, y: number }, endPoi: { x: number, y: number }, score: number, duration?: number, cb?: (...params: any[]) => void, ...params: any[]) {
            if (score == 0) {
                if (cb != null) {
                    cb(...params);
                }
            } else {
                let gold = Tools.inst.changeMoneyToGold(Tools.inst.changeGoldToMoney(score))
                let distributor = this.chipItemMgr.distributor(gold);
                let num: number = 0;
                for (let key in distributor) {
                    if (distributor.hasOwnProperty(key) && key != 'total') {
                        var value = distributor[key];
                        for (let i = 0; i < value; i++) {
                            Laya.timer.frameOnce(i + 1, this, () => {
                                num++;
                                let chip = this.chipItemMgr.getChip();
                                chip.Color = ChipItemMgr.colorMap[key];
                                chip.move(
                                    { x: startPoi.x, y: startPoi.y },
                                    { x: endPoi.x, y: endPoi.y },
                                    duration,
                                    Handler.create(this, (chip: ChipItem, isOver: boolean) => {
                                        this.chipItemMgr.hideChip(chip);
                                        if (isOver && cb != null) {
                                            cb(...params);
                                        }
                                    }, [chip, num == distributor.total])
                                );
                            })
                        }
                    }
                }
            }
        }

        setTotalPoolText(value: number) {
            this.totalPoolValue = value;
            this.totalPoolText.setVar("value", value != 0 ? Tools.inst.changeGoldToMoney(value) : '').flushVars()
            this.totalPoolText.visible = value != 0 ? true : false;
            //G565.AutoTextSize(this.totalPoolText.asTextField);
        }

        /**开始游戏动画*/
        playGameStartAni(onComplete?: laya.utils.Handler, times?: number, delay?: number) {
            this.aniStartGame.visible = true;
            this.aniStartGame.getTransitionAt(0).play(onComplete, times, delay);
        }

        showWinAni(isPlay: boolean = true, onComplete?: () => void, times?: number, delay?: number) {
            this.winImg.visible = true
            if (isPlay == true) {
                this.winAni.play(Handler.create(this, () => {
                    if (onComplete != null) {
                        onComplete();
                    }
                }), times, delay)
            }
            else {
                if (onComplete != null) {
                    onComplete();
                }
            }
        }

        hideWinImg() {
            this.winImg.visible = false;
        }


        private originalBankerPos: { x: number, y: number } = null;

        /**设置庄家动画*/
        setBanker(side, isPlayAni: boolean = false, onComplete?: () => void, times?: number, delay?: number) {
            if (isPlayAni == true) {
                this.bankerTag.visible = true;
                let lastBankerPlayer = this.getPlayer(this.bankerSide);
                let currentPos: { x: number, y: number };
                // if (lastBankerPlayer != null && lastBankerPlayer.visible == true) {
                //     currentPos = lastBankerPlayer.getBankerTagPoi();
                //     lastBankerPlayer.updateBankerState(false);
                // }
                // else {
                currentPos = this.originalBankerPos;
                // }
                this.aniChangeBanker.setValue('startPos', currentPos.x, currentPos.y);
                let endPos = this.getPlayer(side).getBankerTagPoi();
                this.aniChangeBanker.setValue('endPos', endPos.x, endPos.y);
                this.aniChangeBanker.play(Handler.create(this, () => {
                    this.bankerTag.visible = false;
                    this.getPlayer(side).updateBankerState(true);
                    if (onComplete) {
                        onComplete();
                    }
                }), times, delay);
            } else {
                this.getPlayer(side).updateBankerState(true);
                if (onComplete) {
                    onComplete();
                }
            }
            this.bankerSide = side;
        }

        /**当前是谁的回合的红框框*/
        setPlayerMask(value: boolean, allhide: boolean = true, side?: number) {
            for (let i = 0; i < this.playerFrames.length; i++) {
                let player = this.playerFrames[i];
                player.TimerValue = 0
                if (value == true && i == side) {
                    player.setMask(1);
                }
                else if (allhide == true) {
                    player.setMask(0);
                }
                else if (player.State != 1 && player.State != 5) {
                    player.setMask(0);
                }
            }

            // Laya.timer.clear(this, this.TimerEvt);
            Laya.timer.clear(this, this.TimerMaxEvt);
            if (side != null) {
                let player = this.playerFrames[side];
                player.TimerValue = player.TimerMax;
                Laya.timer.frameOnce(1, this, this.TimerEvt, [player]);
            }
        }

        setPlayerAllinMask(side: number) {
            this.getPlayer(side).setMask(2);
            if (side == 0) {
                this.btnMgr.State = 0;
            }
        }

        setPlayerFold(side: number) {
            this.getPlayer(side).setMask(4);
            if (side == 0) {
                this.btnMgr.State = 0;
            }
        }

        /**
         * 发牌动画
         * @param startDealCardSide 第一个发牌的玩家座位号
         * @param dealCardSides 参与发牌的玩家的座位号列表
         * @param selfCardIds 自己的手牌id数组
         */
        dealCard(startDealCardSide: number, dealCardSides: Array<number>, selfCardIds: Array<string>, onComplete?: () => void, delay: number = 0) {
            dealCardSides.sort((a, b) => {
                let i1 = this.dealCardList.indexOf(a);
                let i2 = this.dealCardList.indexOf(b);
                return i1 <= i2 ? -1 : 1;
            });
            let num = 0;
            let cardNum = 2;
            let cardIndex = 0;
            let currentIndex = dealCardSides.indexOf(startDealCardSide);
            let getNextSide = (currentIndex: number) => {
                let nextIndex = currentIndex + 1;
                if (nextIndex >= dealCardSides.length) {
                    nextIndex -= dealCardSides.length;
                }
                return nextIndex;
            }
            let dealCardDelay = 100;
            for (let i = 0; i < dealCardSides.length * selfCardIds.length; i++) {
                Laya.timer.once(dealCardDelay * i, this, (currentIndex, cardIndex, i) => {
                    let player = this.getPlayer(dealCardSides[currentIndex]);
                    player.playShowMiniHandCard(cardIndex, currentIndex == 0 ? selfCardIds[cardIndex] : null, (currentIndex, cardIndex, i) => {
                        if (currentIndex == 0 && cardIndex == cardNum - 1) {
                            let num1 = selfCardIds[0].substring(0, 1);
                            let num2 = selfCardIds[1].substring(0, 1);
                            if (num1 == num2) {
                                this.getPlayer(0).setHandCardMask([true, true], 9);
                            }
                            else {
                                let temp = G565CardItem.compareCard(selfCardIds[0], selfCardIds[1]);
                                this.getPlayer(0).setHandCardMask(temp ? [false, true] : [true, false], 10);
                            }
                        }
                        if (i == dealCardSides.length * selfCardIds.length - 1) {
                            if (onComplete != null) {
                                if (delay > 0) {
                                    Laya.timer.once(delay, this, onComplete);
                                }
                                else {
                                    onComplete();
                                }
                            }
                        }
                    }, null, null, currentIndex, cardIndex, i)
                }, [currentIndex, cardIndex, i]);
                currentIndex = getNextSide(currentIndex);
                num++;
                if (num >= dealCardSides.length) {
                    num = 0;
                    cardIndex++;
                }
            }

            // let showMiniHandCardOnComplete = null;
            // let cb = () => {
            //     if (cardIndex >= cardNum) {
            //         let num1 = selfCardIds[0].substring(0, 1);
            //         let num2 = selfCardIds[1].substring(0, 1);
            //         if (num1 == num2) {
            //             this.getPlayer(0).setHandCardMask([true, true], 9);
            //         }
            //         else {
            //             let temp = G565CardItem.compareCard(selfCardIds[0], selfCardIds[1]);
            //             this.getPlayer(0).setHandCardMask(temp ? [false, true] : [true, false], 10);
            //         }
            //         if (onComplete != null) {
            //             if (delay > 0) {
            //                 Laya.timer.once(delay, this, onComplete);
            //                 return;
            //             }
            //             else {
            //                 onComplete();
            //                 return;
            //             }
            //         }
            //         else {
            //             return;
            //         }
            //     }
            //     this.getPlayer(dealCardSides[currentIndex]).playShowMiniHandCard(cardIndex, currentIndex == 0 ? selfCardIds[cardIndex] : null, showMiniHandCardOnComplete);
            //     SoundMgrDeZhou.fapai();
            //     currentIndex = getNextSide(currentIndex);
            //     num++;
            //     if (num >= dealCardSides.length) {
            //         num = 0;
            //         cardIndex++;
            //     }
            // }
            // showMiniHandCardOnComplete = cb;
            // cb();
        }

        /**把各个玩家的筹码集中到总池 */
        centralizeChip(cb: () => void) {
            let bidPlayerList: Array<G565PlayerFrame> = [];
            let bidNumbers: Array<number> = [];
            this.playerFrames.forEach((player, index, array) => {
                if (player.bidNumber != 0) {
                    bidPlayerList.push(player);
                    bidNumbers[index] = player.bidNumber;
                    player.hideBid();
                }
            });
            if (bidPlayerList.length > 0) {
                for (let i = 0; i < bidPlayerList.length; i++) {
                    let player = bidPlayerList[i];
                    let onComplete = (playerIndex: number) => {
                        //所有筹码集中后 发牌
                        if (playerIndex == bidPlayerList.length - 1) {
                            cb();
                        }
                    }
                    let startPos = player.getChipTagPoi();
                    let endPos = this.chipPoi;
                    this.distributionChip(startPos, endPos, bidNumbers[player.side], 0.75, onComplete, i);
                }
                SoundMgrDeZhou.chipfly();
            }
            else {
                cb();
            }
        }

        /**下注筹码动画和头像上显示数量*/
        bid(side: number, value: number, isAddGold: boolean, onComplete?: () => void, score?: number) {
            let player = this.getPlayer(side);
            this.setTotalPoolText(this.totalPoolValue + value)
            let selfPlayer = this.getPlayer(0);
            let moveOverEvt = () => {
                player.bid(value);
                this.btnMgr.lastCallNumber = this.btnMgr.lastCallNumber < player.bidNumber ? player.bidNumber : this.btnMgr.lastCallNumber;
                if (this.btnMgr.CallNumber != this.btnMgr.lastCallNumber - selfPlayer.bidNumber) {
                    this.btnMgr.CallNumber = this.btnMgr.lastCallNumber - selfPlayer.bidNumber
                    if (side != 0 && selfPlayer.State != 1 && selfPlayer.State != 5) {
                        if (selfPlayer.getScore() - selfPlayer.AllCallNumber <= this.btnMgr.lastCallNumber) {
                            this.btnMgr.subState = 2;
                        } else {
                            this.btnMgr.subState = 1;
                        }
                    }
                }
                if (score != null) { player.setScoreString(score); }
                if (onComplete) { onComplete(); }
            }
            this.distributionChip(player.getChipPoi(), player.getChipTagPoi(), value, 0.3, moveOverEvt);
        }

        /**
         * @param type 0：游戏即将开始 1：开始抢庄 2：开始下注 3：请亮牌 4：正在匹配 5：开始比牌 6：开始要牌 7：正在开牌
         * @param timer 倒计时时间 null时显示‘...’
         */
        setTimeTip(type: number, time: number) {
            let timeLabel = this.timeTip.getChild('title');
            this.timeTip.getController('state').selectedIndex = type;
            Laya.timer.clearAll(this.timeTip);
            this.timeTip.visible = true;
            let cb: () => void = null;
            if (time == null) {
                let num = 1;
                let str = ' .';
                timeLabel.text = str;
                cb = () => {
                    num++;
                    if (num > 6) {
                        num = 1
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
            Laya.timer.loop(250, this.timeTip, cb);
        }

        hideTimeTip() {
            Laya.timer.clearAll(this.timeTip);
            this.timeTip.visible = false;
        }

        /**隐藏大牌图标 */
        hideCardTypeCom() {
            this.cardTypeCom.visible = false;
        }

        /**显示大牌图标 */
        showCardTypeCom(type: number, isTransition: boolean, onComplete?: laya.utils.Handler, times?: number, delay?: number) {
            let map: { [key: number]: number } = {
                4: 0,
                3: 1,
                2: 2,
                1: 3,
            };
            this.cardTypeCom.getControllerAt(0).selectedIndex = map[type];
            this.cardTypeCom.visible = true;
            this.cardTypeCom.getTransitionAt(0).play(onComplete, times, delay);

            SoundMgrDeZhou.cardtype(map[type]);
        }
        ////////////////////////////////////////////////////////////////////////////////////////////////////////        

        onGoldInfo(msgData, finishedListener) {
            let difen = Tools.inst.changeGoldToMoney(msgData['gold']);    //底分
            let xiaomangzhu = Tools.inst.changeGoldToMoney(msgData['gold'] / 2);    //小盲注
            this.baseScore = msgData['gold'];
            this.fillView.baseScore = this.baseScore;
            let info = ExtendMgr.inst.getText4Language(msgData['info']);     //场次信息
            let partyType = msgData['party_type']; //2:金币场 3：竞技场
            let gamenumber = msgData['gamenumber'] || 'no data';     //牌局编号
            this.gameInfoText.text = `${ExtendMgr.inst.getText4Language('牌局编号：')}${gamenumber}\n${info}     ${ExtendMgr.inst.getText4Language('盲注：')}${xiaomangzhu}/${difen}`
            if (finishedListener) finishedListener();
        }


        onPlayerJoin(msgData) {
            let data = msgData['info'];
            let posServer = data['side'];
            let posLocal = this.getLocalPos(posServer);
            this.getPlayer(posLocal).setSeat(data);

            SoundMgrDeZhou.sit();
        }

        onPlayerExit(msgData) {
            let playerInfo = msgData['info'];
            let posServer = playerInfo['side'];
            let posLocal = this.getLocalPos(posServer);
            this.getPlayer(posLocal).clear();
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
            if (finishedListener) { finishedListener(); }
        }

        onPlayerGoldInfo(msgData) {
            let playerInfo = msgData['playerInfo'];
            for (let i = 0; i < playerInfo.length; i++) {
                let oneData = playerInfo[i];
                let side = this.getLocalPos(oneData["side"]);
                let player = this.getPlayer(side);
                player.setScoreString(oneData["possessionOfProperty"]);
            }
        }

        onExitRoom() {
            if (this.netHandler != null && this.netHandler.sendExitRoom != null && this.netHandler.valid()) {
                this.netHandler.sendExitRoom();
            }
            else {
                UserMgr.inst.returnToLobby();
            }
            SoundMgrDeZhou.button();
        }


        onExchangeRoom() {
            if (this.netHandler != null && this.netHandler.sendExitRoom != null && this.netHandler.valid()) {
                this.showRequesting(true);
                this.netHandler.sendChangeRoom((msgData) => {
                    this.showRequesting(false);
                    if (msgData['result']) {
                        if (this.netHandler != null) {
                            this.netHandler.disconnect();
                        }
                        this.reset();
                        let params = NetHandlerMgr.lastConnectParams;
                        this.netHandler.connect(params, this.reconnectResult.bind(this));
                    }
                });
                SoundMgrDeZhou.button();
            }
        }

        onGoldExitRoomResult(msgData, finishedListener) {
            // this.sequenceCTL.push(msgData, (msgData, finishedListener: Function) => {
            if (msgData['result']) {
                UserMgr.inst.returnToLobby();
            } else {
                this.netHandler.sendData(ProtoKeyParty.C_S_EXIT_ROOM_CONFIRM);
            }
            if (finishedListener) { finishedListener(); }
            // });
            if (finishedListener) finishedListener();
        }

        reconnectResult(connected) {
            if (!connected) return;
            let sid = UserMgr.inst.sid;
            this.netHandler.enterGame(sid, 565, this.onEnterRoomSuccess.bind(this));
            NetHandlerMgr.inst.initPingListen(G565.S_C_PING);
        }

        /**********setSeat******************/
        private posServerSelf: number = null;
        private localPosList: Array<number> = null;
        private local2serverPos: Array<number> = [];
        private server2localPos: Array<number> = [];
        public playerCount: number = 0;
        /**发牌顺序列表 */
        public dealCardList: Array<number> = [];

        transferServerPos(posServerSelf: number, playerCount: number) {
            this.playerCount = playerCount;
            //////顺时针////////
            for (let i = 0; i < this.playerCount; i++) {
                let temp = (i + posServerSelf) % this.playerCount;
                //tempNetworkseat = tempNetworkseat >= this.playerCount ? tempNetworkseat - this.playerCount : tempNetworkseat;
                this.server2localPos[i] = temp;
                this.local2serverPos[temp] = i;
                this.dealCardList.push(i);
            }
            ///////////////////////
        }
        /**获取本地座位号 */
        getLocalPos(network_seat) {
            return this.local2serverPos[network_seat]
        }
        /**获取网络座位号 */
        getServerPos(local_seat) {
            return this.server2localPos[local_seat]
        }

        /*********************************/

        private onKeyDown(e: Event): void {
            var keyCode: number = e["keyCode"];
            var Keyboard = Laya.Keyboard;
            switch (keyCode) {
                case Keyboard.NUMBER_0:
                    MasterMgr.inst.switch('relogin');
                    break;
                default:
                    break;
            }
        }
    }

    class BtnsMgr {
        private item: fairygui.GComponent;
        private stateCtl: fairygui.Controller;
        private clickBtnCtl: fairygui.Controller;
        private optionBtnSelectedCtl: fairygui.Controller;
        private optionBtnCtl: fairygui.Controller;
        private isAddCtl: fairygui.Controller;
        public lastCallNumber: number;
        private callNumber: number;

        /**弃牌按钮*/
        public foldBtn: fairygui.GButton;
        /**跟按钮*/
        public callBtn: fairygui.GButton;
        /**全下按钮*/
        public allinBtn: fairygui.GButton;
        /**加注按钮*/
        public fillBtn: fairygui.GButton;
        /**让牌按钮 */
        public yieldBtn: fairygui.GButton;

        /**让或弃选项*/
        private passOption: fairygui.GButton;
        /**跟当前注选项*/
        private callOption: fairygui.GButton;
        /**跟任何注选项*/
        private callAnyOption: fairygui.GButton;
        /**自动让牌选项 */
        private autoPassOption: fairygui.GButton;
        /**全下选项 */
        private allinOption: fairygui.GButton;

        /**加注界面还没做的全下按钮*/
        public allinBtn2: fairygui.GButton;

        private optionOff: () => void;

        constructor(item: fairygui.GComponent) {
            this.item = item;
            this.foldBtn = item.getChild('btnFold').asButton;
            this.callBtn = item.getChild('btnCall').asButton;
            this.allinBtn = item.getChild('btnAllIn').asButton;
            this.allinBtn2 = item.getChild('btnAllIn2').asButton;
            this.fillBtn = item.getChild('btnFill').asButton;
            this.yieldBtn = item.getChild('btnYield').asButton;

            this.passOption = item.getChild('btnPass').asButton;
            this.callOption = item.getChild('btnCallCurrent').asButton;
            this.callAnyOption = item.getChild('btnCallAny').asButton;
            this.autoPassOption = item.getChild('btnAutoPass').asButton;
            this.allinOption = item.getChild('btnAllinOption').asButton;

            this.stateCtl = item.getController('btnsCtl');
            this.clickBtnCtl = item.getController('btns1Ctl');
            this.optionBtnSelectedCtl = item.getController('btns2Selected');
            this.optionBtnCtl = item.getController('btns2Ctl');
            this.isAddCtl = item.getController('isAdd');

            let options = [this.passOption, this.callOption, this.callAnyOption, this.autoPassOption, this.allinOption];
            let optionEvt = (index) => {
                this.selectedIndex = this.selectedIndex == index ? 0 : index;
                SoundMgrDeZhou.button();
            };

            for (let i = 0; i < options.length; i++) {
                let v = options[i];
                v.onClick(this, optionEvt, [i + 1]);
            }

            this.optionOff = () => {
                for (let i = 0; i < options.length; i++) {
                    let v = options[i];
                    v.offClick(this, optionEvt)
                }
            }
            this.State = 0;

        }

        onDispose() {
            this.fillBtn.mode = -1;
            this.callBtn.mode = -1;
            this.allinBtn.mode = -1;
            this.allinBtn2.mode = -1;
            this.fillBtn.mode = -1;

            this.passOption.mode = -1;
            this.callOption.mode = -1;
            this.callAnyOption.mode = -1;

            if (this.optionOff != null) {
                this.optionOff();
            }
        }

        /**@param value 0隐藏 1单击按钮模式 2单选按钮模式*/
        set State(value: number) {
            if (value != this.stateCtl.selectedIndex) {
                this.stateCtl.selectedIndex = value;
                let anis: fairygui.Transition[] = [];
                anis[1] = this.item.getTransition('btns1');
                anis[2] = this.item.getTransition('btns2');
                anis[1].stop(true);
                anis[2].stop(true);
                if (value != 0) {
                    anis[value].play();
                }
            }
        }
        /**0隐藏 1单击按钮模式 2单选按钮模式 */
        get State() {
            return this.stateCtl.selectedIndex;
        }

        /**@param value 0让牌 1跟 2全下 3跟and全下*/
        set subState(value: number) {
            this.clickBtnCtl.selectedIndex = value;
            this.optionBtnCtl.selectedIndex = value;
        }

        setIsAdd(value: boolean) {
            let addAni = this.item.getTransition('');
            this.isAddCtl.selectedPage = value == true ? 'true' : 'false';
        }

        /**0让牌 1跟 2全下 3跟and全下*/
        get subState() {
            return this.clickBtnCtl.selectedIndex;
        }

        /**0无 1让或弃 2跟 3跟任何注 4自动让牌 5全下*/
        get selectedIndex() {
            return this.optionBtnSelectedCtl.selectedIndex;
        }
        /**@param value 0无 1让或弃 2跟 3跟任何注 4自动让牌 5全下*/
        set selectedIndex(value: number) {
            this.optionBtnSelectedCtl.selectedIndex = value;
            let options = [this.passOption, this.callOption, this.callAnyOption, this.autoPassOption, this.allinOption];
            for (let i = 0; i < options.length; i++) {
                let btn = options[i];
                btn.getController('selected').selectedIndex = 0;
            }
            if (value > 0) {
                let btn = options[value - 1];
                btn.getController('selected').selectedIndex = 1;
            }
        }

        /**跟牌数值*/
        set CallNumber(value: number) {
            if ((this.selectedIndex == 2 && value != this.callNumber) || (this.selectedIndex == 4 && value != 0)) {
                this.selectedIndex = 0;
            }
            this.callNumber = value;
            this.callBtn.title = '跟' + Tools.inst.changeGoldToMoney(value);
            this.callOption.title = '跟' + Tools.inst.changeGoldToMoney(value);

            G565.AutoTextSize(this.callBtn.getChild('title').asTextField);
            G565.AutoTextSize(this.callOption.getChild('title').asTextField);
        }

        get CallNumber() {
            return this.callNumber;
        }

    }

    class ChipText {
        public view: fairygui.GLabel;
        private value: number;
        constructor(bg: fairygui.GLabel) {
            this.view = bg;
            this.Value = 0;
        }

        get visible() {
            return this.view.visible;
        }

        set visible(value: boolean) {
            this.view.visible = value;
        }

        get Value() {
            return this.value;
        }

        set Value(value: number) {
            this.value = value;
            this.view.title = value != 0 ? Tools.inst.changeGoldToMoney(value) : '';
            this.visible = value != 0 ? true : false;
            //G565.AutoTextSize(this.view.getChild('title').asTextField);
        }

        get chipPoi() {
            let poi = this.view.getChild('chipPoi');
            return this.view.localToGlobal(poi.x, poi.y);
        }
    }

    export class ChipItemMgr {
        private parent: fairygui.GComponent;
        private chipPool: Array<ChipItem> = [];
        private chipList: Array<ChipItem> = [];
        public static colorMap = {
            '_1000': 9,
            '_500': 8,
            '_250': 2,
            '_200': 1,
            '_100': 3,
            '_50': 0,
            '_10': 4,
            '_5': 6,
            '_1': 7,
            '_0': 5,
        }

        constructor(parent: fairygui.GComponent) {
            this.parent = parent;
        }

        distributor(num: number): { total: number, _0?: number, _1?: number, _5?: number, _10?: number, _50?: number, _100?: number, _200?: number, _250?: number, _500?: number, _1000?: number } {
            let obj: { total: number, _0?: number, _1?: number, _5?: number, _10?: number, _50?: number, _100?: number, _200?: number, _250?: number, _500?: number, _1000?: number } = { total: 0 };
            obj._1000 = Math.floor(num / 1000);
            if (obj._1000 > 7) {
                obj._1000 = 7;
            }
            num %= 1000;
            obj._500 = Math.floor(num / 500);
            num %= 500;
            obj._250 = Math.floor(num / 250);
            num %= 250;
            obj._200 = Math.floor(num / 200);
            num %= 200;
            obj._100 = Math.floor(num / 100);
            num %= 100;
            obj._50 = Math.floor(num / 50);
            num %= 50;
            obj._10 = Math.floor(num / 10);
            num %= 10;
            obj._5 = Math.floor(num / 5);
            num %= 5;
            obj._1 = Math.floor(num / 1);
            num %= 1;
            obj._0 = num != 0 ? 1 : 0;
            obj.total = obj._1000 + obj._500 + obj._250 + obj._200 + obj._100 + obj._50 + obj._10 + obj._5 + obj._1 + obj._0;
            return obj;
        }


        private addChip() {
            let chip: ChipItem = new ChipItem(fairygui.UIPackage.createObject('G565', 'ChipSmall').asCom);
            this.parent.addChild(chip.item);
            this.chipList.push(chip);
            chip.item.setXY(0, 0);
            return chip;
        }

        getChip() {
            let chip: ChipItem;
            if (this.chipPool.length > 0) {
                chip = this.chipPool.shift()
                this.chipList.push(chip);
            }
            else {
                chip = this.addChip();
            }
            chip.item.removeFromParent()
            this.parent.addChild(chip.item);
            chip.item.setXY(0, 0);
            chip.item.visible = true;
            return chip
        }

        hideChip(chip: ChipItem) {
            let index = this.chipList.indexOf(chip)
            if (index != -1) {
                let chip = this.chipList.splice(index, 1)[0];
                chip.item.visible = false;
                this.chipPool.push(chip);
            }
        }

        clearChip() {
            for (let i = 0; i < this.chipList.length; i++) {
                let chip = this.chipList.shift();
                chip.item.removeFromParent();
                chip.item.dispose();
            }
            for (let i = 0; i < this.chipPool.length; i++) {
                let chip = this.chipPool.shift();
                chip.item.removeFromParent();
                chip.item.dispose();
            }
        }
        get ChipPool() {
            return this.chipPool;
        }

        get ChipList() {
            return this.chipList;
        }
    }

    class ChipItem {
        public item: fairygui.GComponent;
        private colorIndex: number;
        private colorCtl: fairygui.Controller;
        private moveAni: fairygui.Transition;

        constructor(item: fairygui.GComponent) {
            this.item = item;
            this.colorCtl = this.item.getController('color');
            this.moveAni = this.item.getTransition('move');
        }

        move(startPos: { x: number, y: number }, endPos: { x: number, y: number }, duration?: number, onComplete?: laya.utils.Handler, times?: number, delay?: number) {
            this.moveAni.setValue('startPos', startPos.x, startPos.y);
            this.moveAni.setValue('endPos', endPos.x, endPos.y);
            if (duration != null) {
                this.moveAni.setDuration('startPos', duration);
            }
            this.moveAni.play(onComplete, times, delay);
        }

        hide() {
            this.item.visible = false;
        }

        get Color() {
            return this.colorIndex;
        }

        /** @param value 0,橙,1,粉,2,红,3,黄,4,蓝,5,绿,6,浅蓝,7,青绿,8,浅紫,9,紫*/
        set Color(value: number) {
            this.colorIndex = value;
            this.colorCtl.selectedIndex = value;
        }
    }

    //写着玩的
    /*     class SequenceCTL {
            private actionDataList: Array<{ listener: (msgData: any, finishedListener: () => void) => void, data: any }> = null;
            private acting: boolean;
            private peek: () => void;
            constructor() {
                this.actionDataList = [];
                this.acting = false;
                let cb: () => void = null;
                this.peek = () => {
                    if (this.acting || this.actionDataList.length == 0)
                        return;
    
                    this.acting = true;
                    let actionData = this.actionDataList.shift();
                    //console.log('SequenceCTL', actionData.data.className, actionData.data);
                    actionData.listener(actionData.data, () => {
                        this.acting = false;
                        cb();
                    })
                }
                cb = this.peek;
            }
    
            push(data: any, listener: (msgData: any, finishedListener: () => void) => void) {
                this.actionDataList.push({ listener, data });
                this.peek();
            }
    
            reset() {
                this.acting = false;
                this.actionDataList.splice(0, this.actionDataList.length);
            }
    
            dispose() {
    
            }
        } */

    export let AutoTextSize = (label: fairygui.GTextField) => {
        let tf: Laya.Text = new Laya.Text();
        tf.fontSize = label.fontSize;
        tf.text = label.text;
        for (let i = 0; i < tf.textWidth; i++) {
            if (tf.textWidth > label.width) {
                tf.fontSize--;
            } else {
                break;
            }
        }
        label.fontSize = tf.fontSize;
    }
}
