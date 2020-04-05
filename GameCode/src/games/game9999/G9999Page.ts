module G9999 {
    export class G9999Page extends Page {
        private playerFrames: Array<G9999PlayerFrame> = [];
        private gameTimer: fairygui.GComponent;
        private gameTimerText: fairygui.GLabel;
        private gameInfoText: fairygui.GLabel;
        private exitBtn: fairygui.GButton;
        private changeRoomBtn: fairygui.GButton;
        private aniStartGame: fairygui.GComponent;
        private tipText: fairygui.GLabel;


        private detailedList: G9999DetailedList;
        private chipRect: G9999ChipFrame;
        private headinfo: G9999HeadInfo;

        private showCardView: G9999ShowCard;

        private seconds: number = 0;
        public isStartGame: boolean;
        private isChangeRoom: boolean = false;
        private roomName: string;
        private bankerSide: number;
        private chipPosData: ChipPosData;
        private balanceData;
        //----------------JiaTao
        private btn_bar : fairygui.GComponent;//2018.8.7-------JiaTao
        private matching : fairygui.GComponent;//2018.8.25-----JiaTao
        private btnList : fairygui.GComponent;
        private xianH : fairygui.GComponent;
        private c_bar : fairygui.Controller = null;
        private c_jetton : fairygui.Controller = null;
        private c_seat : fairygui.Controller = null;
        //-----------------end
        //private btn_test : fairygui.GButton;

        constructor(scene = 'GameScene') {
            super('G9999', scene, UILayer.GAME);
        }

        onDispose() {
            SoundMgrBaccarat.stopBGM();
            this.showCardView.hide();
            this.clearAutoExit();
            this.chipRect.chipItemMgr.clearChip();
        }

        onCreated(data: any = null) {
            // Laya.Stat.show(0,0);
            if (!data) return;
            //this.pageStyleSetting(data);
            //开启背景音乐
            SoundMgrBaccarat.playBGM();

            let view = this.view;
            for (let i = 0; i < 5; i++) {
                this.playerFrames.push(new G9999PlayerFrame({
                    side: i,
                    seat: view.getChild('seat' + i).asCom,
                }));
            }
            this.gameTimer = view.getChild('comTimer').asCom;
            this.gameTimerText = this.gameTimer.getChild('Txt_count_down').asLabel;
            this.gameTimer.visible = false;
            this.gameInfoText = view.getChild('gameInfo'
            ).asLabel;
            this.changeRoomBtn = view.getChild('btnChangeRoom').asButton;
            this.changeRoomBtn.onClick(this, this.onExchangeRoom.bind(this));
            this.aniStartGame = view.getChild('aniStartGame').asCom;
            this.tipText = view.getChild('txtTip').asLabel;
            this.detailedList = new G9999DetailedList(view.getChild('comDetailedList').asCom);
            this.chipRect = new G9999ChipFrame(view);
            this.headinfo = new G9999HeadInfo(view);
            this.chipPosData = new ChipPosData();
            /*------------------------JiaTao------------------------*/
            this.matching = view.getChild('matching').asCom;
            this.btn_bar = view.getChild('btn_bar').asCom;
            this.btnList = view.getChild('btnList').asCom;
            this.xianH = view.getChild('xianH').asCom;
            this.c_bar = view.getController('c_bar');
            this.c_jetton = view.getController('c_jetton');
            this.c_seat = view.getController('c_seat');
            //----------------------new
            let c_btnList = this.btnList.getController('c1');
            this.btnList.getChild('open').onClick(this,()=>{
                c_btnList.selectedIndex = 1;
            }); 
            this.btnList.getChild('close').onClick(this,()=>{
                c_btnList.selectedIndex = 0;
            });
            this.btnList.getChild('btn_exit').onClick(this,this.onExitRoom.bind(this));
            this.btnList.getChild('btn_setting').onClick(this,()=>{
                UIMgr.inst.popup(UI_Setting);
            });
            this.btnList.getChild('btn_history').onClick(this,()=>{
                let obj = UIMgr.inst.popup(UI_History) as UI_History;
                obj.refreshGameListInGame(9999);
            });

            this.btnList.getChild('btn_rule').onClick(this,()=>{
                var rule = UIMgr.inst.popup(UI_Rules) as UI_Rules;
                rule.refreshData('game'+9999);
            });

            //----------------------end

            this.btn_bar.getChild('strive').asButton.onClick(this,()=>{
                this.c_bar.selectedIndex = 0;
                NetHandlerMgr.netHandler.sendGrabDealerVote(true);
            });
            this.btn_bar.getChild('strive_no').asButton.onClick(this,()=>{
                this.c_bar.selectedIndex = 0;
                NetHandlerMgr.netHandler.sendGrabDealerVote(false);
            });
            /*------------------------end------------------------*/
            for (let chipRectItemKey in this.chipRect.ChipRectItems) {
                if (this.chipRect.ChipRectItems.hasOwnProperty(chipRectItemKey)) {
                    let cb = (index) => {
                        let chipRectItemClickCallBack = (poi: laya.maths.Point) => {
                            if (G9999ChipFrame.isCanChip && this.chipRect.ChipChoose != 0) {
                                this.chipPosData.addPoi(this.chipRect.ChipRectItems[index].Place, this.chipRect.ChipChoose, poi);
                                NetHandlerMgr.netHandler.sendBid(this.chipRect.ChipRectItems[index].Place, this.chipRect.ChipChoose, 1);
                            }
                        }
                        this.chipRect.ChipRectItems[index].ClickCallBack = chipRectItemClickCallBack;
                    }
                    cb(chipRectItemKey);
                }
            }
            this.showCardView = UIMgr.inst.add(G9999ShowCard, null) as G9999ShowCard;
            this.reset();
            this.onEnterRoomSuccess(data);
            this.initDrawcall();
        }

        // showTip(text: string, handler?: Handler) {
        //     this.tipText.text = "[color=#FF6600,#FFFFFF]" + text + "[/color]";
        //     this.tipText.visible = true;
        //     this.tipText.getTransitionAt(0).play(handler);
        //     SoundMgrNiu.startBidGame();
        // }
        //------JiaTao
        showTip(text: string, handler?: Handler) {
            // this.tipText.text = "[color=#FF6600,#FFFFFF]" + text + "[/color]";
            this.tipText.text = text;//JiaTao
            this.tipText.visible = true;
            let c_show = this.tipText.getController('c_show');
            if(text == '开始下注'){//JiaTao
                c_show.selectedIndex = 0;
                SoundMgrNiu.startBidGame();
                this.c_seat.selectedIndex = 1;
                this.showJetton();//-----------开启下注按钮
            }else if(text == '等待下注'){
                c_show.selectedIndex = 1;
                this.c_seat.selectedIndex = 0;
            }else if(text == '停止下注'){
                c_show.selectedIndex = 2;
            }
            this.tipText.getTransitionAt(0).play(handler);
        }

        //-------JiaTao Drawcall优化
        private cashAsMode : 'bitmap';
        initDrawcall(){
            let comChipRect = this._view.getChild('comChipRect').asCom;
            for(let i = 0; i < this.playerFrames.length; ++i){
                this.playerFrames[i]['seat'].displayObject.cacheAs = this.cashAsMode;
            }
            this.btnList.displayObject.cacheAs = this.cashAsMode;
            comChipRect.displayObject.cacheAs = this.cashAsMode;
        }
        //-------------JiaTao 按钮屏蔽
        private buttonMode : number = 1;//按钮屏蔽
        destoryAllBtn(){
            let open = this.btnList.getChild('open').asButton;
            let close = this.btnList.getChild('close').asButton;
            let btn_exit = this.btnList.getChild('btn_exit').asButton;
            let btn_setting = this.btnList.getChild('btn_setting').asButton;
            let btn_rule = this.btnList.getChild('btn_rule').asButton;
            let btn_history = this.btnList.getChild('btn_history').asButton;
            let btnArray = [open,close,btn_exit,btn_setting,btn_rule,btn_history,this.changeRoomBtn];
            for(let i = 0; i < btnArray.length; ++i){
                btnArray[i].mode = this.buttonMode;
            }
        }

        //--------JiaTao 下注按钮动画 this.c_jetton
        showJettonHandler(index){
            SoundMgrBaccarat.window_open();
            this.c_jetton.selectedIndex = index;
            if(index == 6){
                Laya.timer.clear(this,this.showJettonHandler);
            }
        }

        showJetton(isShowAll = false){
            let index = [1,2,3,4,5,6];
            let delayTime = [0,200,400,600,800,1000];
            if(isShowAll){
                SoundMgrBaccarat.window_open();
                this.c_jetton.selectedIndex = 6;
            }
            else{
                for(let i = 0; i < index.length; ++i){
                    Laya.timer.once(delayTime[i],this,this.showJettonHandler.bind(this),[index[i]],false);
                }
            }
        }
        

        reset() {
            G9999ChipFrame.isCanChip = false;
            this.posServerSelf = null;
            this.balanceData = null;
            this.chipPosData.clearPoi();
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

        onEnterRoomSuccess(data) {
            //console.log('进入房间成功---s_c_Connected',data);
            let gameInfo = data['myInfo'];
            //开启匹配动效
            if(!gameInfo['isRefresh']){
                this.matching.visible = true;
                Laya.timer.loop(1750,this,this.showMatch.bind(this),null,false);
            }
            //断线重连，请求当前游戏数据
            if (gameInfo['isRefresh'])
                this.refreshInfo();
            else
                this.initGame(gameInfo);
        }
        private isRefreshData  : boolean = false;
        refreshInfo() {
            NetHandlerMgr.netHandler.refreshData((data) => {
                this.isRefreshData = true;
                if (data['result']) {
                    // WaitingView.hide();
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
                    player.setSeat(playerInfo);
                    // if (key == 0) {
                    //     player.updateBankerState(true);
                    //     this.bankerSide = side;
                    // }
                }
            }, this);
            /*                 开始游戏                      */
            this.changeRoomBtn.visible = false;
            NetHandlerMgr.netHandler.sendGameStart();
            //NetHandlerMgr.netHandler.sendGrabDealerVote(true);//JiaTao
        }
        getPlayer(side: number, server: boolean = false): G9999PlayerFrame {
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
            NetHandlerMgr.netHandler.addSequenceMsgListener(ProtoKeyParty.S_C_IS_GOLD, this.onGoldInfo.bind(this));


            //正常消息处理
            NetHandlerMgr.netHandler.addMsgListener(ProtoKeyParty.S_C_PLAYER_INFO, this.onPlayerGoldInfo.bind(this));

            //----------百家乐
            NetHandlerMgr.netHandler.addMsgListener(S_C_BID_BCR, this.onBid.bind(this));//下注结果
            NetHandlerMgr.netHandler.addMsgListener(S_C_START_GRABDEALER_BCR, this.onStartGrabDealer.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_GRABDEALER_VOTERESULT_BCR, this.onGrabDealer.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_SWAPDEALER_BCR, this.onSwapDealer.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_BALANCEBACCARAT_BCR, this.onBalance.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_AFTERBID_BCR, this.onAfterBid.bind(this));
            NetHandlerMgr.netHandler.addMsgListener(S_C_AFTERREFRESh_BCR, this.onAfterRefreshBid.bind(this));
            //---------------JiaTao
            NetHandlerMgr.netHandler.addMsgListener(S_C_SENDSIGN_BCR, this.showSign.bind(this));
        }
        
        onGoldInfo(msgData, finishedListener) {
            //console.log('onGoldInfo',msgData);
            let difen = msgData['gold'];    //底分
            let info = msgData['info'];     //场次信息
            let partyType = msgData['party_type']; //2:金币场 3：竞技场
            let gamenumber = msgData['gamenumber'] || 'no data';     //牌局编号 '\n' + 
            //this.gameInfoText.text = '牌局编号：' + gamenumber + '\n' + this.roomName + '     ' + info + '     底分：' + difen;
            //-----JiaTao
            this.gameInfoText.text = '牌局编号：' + gamenumber + '   ' +this.roomName + '     ' + info + '     底分：' + difen;
            if (finishedListener) finishedListener();
        }

        showMatch(){
            this.matching.getTransition('matching').play();
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
            this.getPlayer(posLocal).setSeat(data);
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
            this.matching.visible = false;//Jia
            Laya.timer.clear(this,this.showMatch);
            this.matching.getTransition('matching').stop();//Jia 关闭动效

            this.c_bar.selectedIndex = 1;
            let waitTime: { high: number, low: number, unsigned: boolean } = {
                high: msgData['waitTime']['high'],
                low: msgData['waitTime']['low'],
                unsigned: msgData['waitTime']['unsigned'],
            }
            this.setTimer(waitTime.low / 1000);
            this.aniStartGame.visible = true;
            this.aniStartGame.getTransitionAt(0).play();
            SoundMgrNiu.gameStart();
            Laya.timer.once(500,this,function(){
                SoundMgrNiu.startQiang();
            })
        }

        //服务器广播玩家标记----JiaTao
        //let side = this.getLocalPos(chair);
            //let player = this.getPlayer(side);
            //player.updateScoreString(money);
        showSign(msgData){ 
            let PlayerInfo = msgData['PlayerInfo'];
            for(let i = 0; i < PlayerInfo.length; ++i){
                let localSide = this.getLocalPos(PlayerInfo[i]['side']);
                let player = this.getPlayer(localSide);
                let sign = PlayerInfo[i]['sign'];
                let sex = msgData['PlayerInfo'][i]['sex'];
                let c_showSign = this._view.getChild('sign_'+localSide).asCom.getController('c1');
                //this._view.getChild('sign_'+localSide).asCom.getController('c1').selectedIndex = sign;
                if(sign == 1){//抢庄
                Laya.timer.frameOnce(i*5,this,function(){
                    SoundMgrNiu.qiang('',sex);//第一个参数什么都不传，为"抢庄"。strive
                    c_showSign.selectedIndex = 1;
                }.bind(this),null,false);
                }
                else if(sign == 2){//不抢庄
                    Laya.timer.frameOnce(i*5,this,function(){
                        SoundMgrNiu.qiang(0,sex);
                        c_showSign.selectedIndex = 2;
                    }.bind(this),null,false);
                }
                else{//3-满注 4-弃牌 5-观看
                    Laya.timer.frameOnce(i*5,this,function(){
                        c_showSign.selectedIndex = sign;
                    }.bind(this),null,false);
                }
            }
        }
        //抢庄结果
        onGrabDealer(msgData) {
            //------------JiaTao 消除标记
            this.c_bar.selectedIndex = 0;
            for(let i = 0; i < 5; ++i){
                this._view.getChild('sign_'+i).asCom.getController('c1').selectedIndex = 0;
            }
            //闪光特效
            //--------------end
            let localSide = this.getLocalPos(msgData['side']);
            this.bankerSide = localSide;
            let player = this.getPlayer(localSide);
            
            let cb = () => {
                // let player = this.getPlayer(localSide);
                //player.updateBankerState(true);//JiaTao 显示两个庄，抢庄结果时候不显示庄图标.
                if (localSide != 0)
                    G9999.G9999ChipFrame.isCanChip = true;
            }
            this.showTip(localSide != 0 ? "开始下注" : "等待下注", Handler.create(this, cb, [], true));
            this.setTimer(15);
        }

         //换位--里面有开始下注的信息 如下注按钮面额的初始化
        onSwapDealer(msgData) {
            SoundMgrNiu.dingzhuang();
            let myside = msgData['myside'];
            let playerList = msgData['playerList']
            this.transferServerPos(myside, this.playerCount);
            this.playerFrames.forEach(element => {
                element.resetGame();
                element.clear();
            });
            Tools.inst.each(playerList, (playerInfo, key) => {
                if (playerInfo != null) {
                    let side = this.getLocalPos(playerInfo['side']);
                    let player = this.getPlayer(side);
                    player.setSeat(playerInfo);
                    if (key == 0) {
                        player.setLightMark(true);
                        player.updateBankerState(true);
                        this.bankerSide = side;
                    }
                }
            }, this);

        }
        ////下注结果
        onBid(msgData) {
            //console.log('onBid---',msgData);
            let place = msgData['place'];
            let side = this.getLocalPos(msgData['chair']);
            let denomination = msgData['denomination'];
            let qty = msgData['qty'];
            let totalplacemoney = msgData['totalplacemoney'];
            let subtotalmoney = msgData['subtotalmoney'];
            let player = this.getPlayer(side);
            player.betEffect(side);//头像抖动-动效
            this.upPlayerGold(msgData['chair'],denomination);//JiaTao------时时更新玩家分数
            //console.log('玩家座位',side,'下注金额',denomination,'下注位置',place);
            SoundMgrBaccarat.bets();
            let chipRectItem = this.chipRect.getChipRectItem(place);
            chipRectItem.TotalChipData = totalplacemoney;
            if (side == 0) {
                chipRectItem.SelfChipData = subtotalmoney;
                for (let i = 0; i < qty; i++) {
                    let startPoi = this.playerFrames[side].getSeatRandomPoi();
                    let endPoi = this.chipPosData.getPoi(place, denomination) || chipRectItem.getRandomPoi();
                    let chip = this.chipRect.chipItemMgr.getChip(denomination);
                    chip.play({ x: startPoi.x, y: startPoi.y }, { x: endPoi.x, y: endPoi.y }, Handler.create(this, () => {
                        FairyguiTools.changeParentNotMove(chipRectItem.clickRect, chip.item)
                    }, [], true))
                }
            }
            else {
                for (let i = 0; i < qty; i++) {
                    let startPoi = this.playerFrames[side].getSeatRandomPoi();
                    let endPoi = chipRectItem.getRandomPoi();
                    let chip = this.chipRect.chipItemMgr.getChip(denomination);
                    chip.play({ x: startPoi.x, y: startPoi.y }, { x: endPoi.x, y: endPoi.y }, Handler.create(this, () => {
                        FairyguiTools.changeParentNotMove(chipRectItem.clickRect, chip.item)
                    }, [], true))
                }
            }
        }
        
       
        //下注过后的信息
        onAfterBid(msgData) {
            this.clearTimer();
            G9999ChipFrame.isCanChip = false;
            let cardresStr: string = msgData['cardres'];
            let cardres = JSON.parse(cardresStr);
            let xianIDs: { id0: string, id1: string, id2: string } = { id0: cardres['x'][0][0], id1: cardres['x'][0][1], id2: cardres['x'][0][2] };
            let xianFinValue: number = cardres['x'][1];
            let zhuangIDs: { id0: string, id1: string, id2: string } = { id0: cardres['z'][0][0], id1: cardres['z'][0][1], id2: cardres['z'][0][2] };
            let zhuangFinValue: number = cardres['z'][1];
            let result: number = msgData['cardrescode'];
            let xzdui: number = msgData['xzdui'];
            let onComplete: Handler = Handler.create(this, () => {
                this.showCardView.visible = false;
                this.addBead(result, xzdui);//result 输赢结果
            }, [], true);
            let cb = () => {
                this.showCardView.show(xianIDs, xianFinValue, zhuangIDs, zhuangFinValue, result, onComplete, 1, 1);
            }
            this.showTip('停止下注', Handler.create(this, cb, [], true));
        }
        //断线重连
        //-------JiaTao
        private _playerList : any;
        private _selfInfo : any;
        onAfterRefreshBid(msgData) {
            //console.log('断线重连----',msgData);
            //----------JiaTao //(0:结算阶段,1:抢庄阶段,2:下注阶段,3:倒计时阶段)
            // if(this.isRefreshData && msgData['stage'] == 0 && msgData['leftMS'] == 0) {
            //     this.changeRoomBtn.visible = true;
            //     this.isRefreshData = false;
            //     return;
            // }
            this.c_seat.selectedIndex = 1;
            let left_MS = msgData['leftMS'];
            let stage = parseFloat(msgData['stage']);
            /*onBalance(msgData) {
            console.log('结算---',msgData);
            this.c_jetton.selectedIndex = 0;//JiaTao关闭下注按钮
            this.balanceData = msgData;
        }*/
            if(stage == 0){
                this.balanceData = msgData['balance'][0];
                let msg = msgData['balance'][0]['setUserDatas'][0];
                this.onAfterBid(msg);
                this.clearTimer();
            }
            else if(stage == 1){
                this.c_bar.selectedIndex = 1;
            }
            else if(stage == 2){
                this.showJetton(true);
            }
            else if(stage == 3){
                this.changeRoomBtn.visible = true;
            }
            else{
                Alert.show('对局已结束,请重新进入！').onYes(function(){});
            }

            //--------重连上来后换位，显示正确的庄家头像标记。
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
                    player.setSeat(playerInfo);
                    if (key == 0) {
                        player.updateBankerState(true);
                        this.bankerSide = side;
                    }
                }
            }, this);
            //-------如果不是庄的话开启下注功能
            if(myside != 0){
                G9999ChipFrame.isCanChip = true;
            }

            //----------end
            this.clearTimer();
            // this.setTimer(parseFloat(msgData['leftMS']) / 1000);
            let leftMS = parseFloat(msgData['leftMS']) / 1000;//Jia
            this.setTimer(parseInt(leftMS.toString()));//Jia
            
            this.bankerSide = this.getLocalPos(0);
            for (let key in msgData['onbidlist']) {
                if (msgData['onbidlist'].hasOwnProperty(key)) {
                    let value = msgData['onbidlist'][key];
                    let place = value['place'];
                    let side = this.getLocalPos(value['chair']);
                    let denomination = value['denomination'];
                    let qty = value['qty'];
                    let totalplacemoney = value['totalplacemoney'];
                    let subtotalmoney = value['subtotalmoney'];
                    //let playertotalmoney = value['playertotalmoney'];
                    //let selflimit = value['selflimit'];
                    //let totallimit = value['totallimit'];
                    let chipRectItem = this.chipRect.getChipRectItem(place);
                    chipRectItem.TotalChipData = totalplacemoney;
                    for (let i = 0; i < qty; i++) {
                        let startPoi = this.playerFrames[side].getSeatRandomPoi();
                        let endPoi = chipRectItem.getRandomPoi();
                        let chip = this.chipRect.chipItemMgr.getChip(denomination);
                        chip.play({ x: startPoi.x, y: startPoi.y }, { x: endPoi.x, y: endPoi.y }, Handler.create(this, () => {
                            FairyguiTools.changeParentNotMove(chipRectItem.clickRect, chip.item)
                        }, [], true))
                    }
                    if (side == 0) {
                        chipRectItem.SelfChipData = subtotalmoney;
                    }

                }
            }
        }
        //输赢数据
        onBalance(msgData) {
            //console.log('结算---',msgData);
            this.c_jetton.selectedIndex = 0;//JiaTao关闭下注按钮
            this.balanceData = msgData;
        }

        onGoldMessage(msgData) {
            let type = msgData['msg_type'];
            let msg = msgData['msg'];
            let self = this;
            this.xianH.getChild('msg').text = msg;

            switch (true) {
                // 代表金币不够退出房间
                case (type == 1):
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
    
                case (type == 20483):
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

        onPlayerGoldInfo(msgData) {
            var playerInfo = msgData['playerInfo'];
            for (var i = 0; i < playerInfo.length; i++) {
                var oneData = playerInfo[i];
                var side = this.getLocalPos(oneData["side"]);
                var player = this.getPlayer(side);
                player.setScoreString(oneData["possessionOfProperty"]);
            }
        }

        //-----------JiaTao
        upPlayerGold(chair,money){
            let side = this.getLocalPos(chair);
            let player = this.getPlayer(side);
            player.updateScoreString(money);
        }

        onExitRoom() {
            this.isChangeRoom = false;
            NetHandlerMgr.netHandler.sendExitRoom();
        }

        onExchangeRoom() {
            this.isChangeRoom = true;
            NetHandlerMgr.netHandler.sendChangeRoom((msgData) => { });
        }

        onGoldExitRoomResult(msgData, finishedListener) {
            if (this.isChangeRoom == true) {
                this.clearAutoExit();
                this.c_jetton.selectedIndex = 0;//JiaTao
                this.c_seat.selectedIndex = 0;//JiaTao
                if (msgData['result']) {
                    this.changeRoomBtn.visible = false;
                    NetHandlerMgr.netHandler.disconnect();
                    this.reset();
                    var params = NetHandlerMgr.lastConnectParams;
                    NetHandlerMgr.netHandler.connect(params, this.reconnectResult.bind(this));
                }
            }
            else {
                if (msgData['result']) {
                    this.chipRect.reset();//---重置chipFrame类里面的单例
                    this.destoryAllBtn();
                    UserMgr.inst.returnToLobby();
                } else {
                    NetHandlerMgr.netHandler.sendData(ProtoKeyParty.C_S_EXIT_ROOM_CONFIRM);
                }
                if (finishedListener) finishedListener();
            }

        }

        reconnectResult(connected) {
            if (!connected) return;
            let sid = UserMgr.inst.sid;
            NetHandlerMgr.netHandler.enterGame(sid, 9999,this.onEnterRoomSuccess.bind(this));
            NetHandlerMgr.inst.initPingListen(G9999.S_C_PING);
        }

        setTimer(seconds: number) {
            Laya.timer.clear(this, this.updateTimer);
            if (!seconds) return;
            this.seconds = seconds;
            this.gameTimer.visible = seconds > 0;
            this.gameTimerText.text = seconds.toString();
            Laya.timer.loop(1000, this, this.updateTimer);
        }

        updateTimer() {
            this.seconds--;
            this.gameTimer.visible = this.seconds > 0;
            this.gameTimerText.text = this.seconds.toString();
            if (this.seconds < 0) {
                Laya.timer.clear(this, this.updateTimer);
            }
        }

        clearTimer() {
            this.gameTimer.visible = false;
            Laya.timer.clear(this, this.updateTimer);
        }

        addBead(result: number, xzdui: number) {
            this.detailedList.addBead(result, true, Handler.create(this, () => {
                switch (xzdui.toString()) {
                    case '1':
                        //闲对        
                        this.detailedList.XianDui++;
                        break;
                    case '0':
                        //庄对        
                        this.detailedList.ZhuangDui++;
                        break;
                }
                this.recycleChip(result, xzdui, this.distributionChip());
            }, [], true))
        }

        recycleChip(result: number, xzdui: number, handler?: () => void) {
            let cb = () => {
                let chipNum = 0;
                let chipTotal = this.chipRect.chipItemMgr.ChipList.length;
                if (this.chipRect.chipItemMgr.ChipList.length > 0) {
                    SoundMgrBaccarat.chipFly();//金币往庄家飞
                    this.chipRect.chipItemMgr.ChipList.forEach((chipItem, index) => {
                        let endPos = this.playerFrames[this.bankerSide].getSeatRandomPoi();
                        chipItem.recycle(endPos, Handler.create(this, () => {
                            this.chipRect.chipItemMgr.hideChip(chipItem);
                            chipNum++;
                            if (chipNum == chipTotal) {
                                this.chipRect.resetRectData();
                                if (handler != null) {
                                    handler();
                                }
                            }
                        }));
                    })
                }
                else {
                    if (handler != null) {
                        handler();
                    }
                }
            }
            let tempHandler = Handler.create(this, cb, [], true);
            //------JiaTao
            let tempFunc = ()=>{
                this.chipRect.ChipRectItems[3].twinkle();
                this.chipRect.ChipRectItems[5].twinkle();
                
            }
            switch (xzdui.toString()) {
                case '1,':
                    //闲对    
                    this.chipRect.ChipRectItems[3].twinkle();
                    break;
                case '0':
                    //庄对    
                    this.chipRect.ChipRectItems[5].twinkle();
                    break;
                case '1,0':
                    //闲庄对一起出现    
                    tempFunc();
                    break;
            }
            switch (result.toString()) {

                case '2':
                    //闲    
                    this.chipRect.ChipRectItems[1].twinkle(tempHandler);
                    break;
                case '0':
                    //和
                    this.chipRect.ChipRectItems[4].twinkle(tempHandler);
                    break;
                case '1':
                    //庄    
                    this.chipRect.ChipRectItems[2].twinkle(tempHandler);
                    break;
            }
        }

        distributionChip() {
            let cb = () => {
                if (this.balanceData == null) {
                    Laya.timer.once(500, this, cb);
                }
                else {
                    this.changeRoomBtn.visible = true;
                    this.autoExit()
                    let data = this.balanceData;
                    let playerDatas = data['setUserDatas'];
                    // let cardrescode = data['setUserDatas'][0]['cardrescode'];
                    // let xzdui = data['setUserDatas'][0]['xzdui'];
                    Tools.inst.each(playerDatas, (value, key) => {
                        let side = this.getLocalPos(value['side']);
                        let player = this.getPlayer(side);
                        let score: boolean = value['score'] == 1;
                        let changegold = value['changegold'];
                        let gold = value['gold'];
                        let isDealer = value['isDealer'];
                        player.changeScore(changegold);
                        player.setScoreString(gold);
                        if (!isDealer && score) {
                            let distributor = this.chipRect.chipItemMgr.distributor(changegold);
                            for (let key in distributor) {
                                if (distributor.hasOwnProperty(key)) {
                                    var value = distributor[key];
                                    let denomination: number = ChipValue[key];
                                    for (let i = 0; i < value; i++) {//---------筹码往闲家飞
                                        let startPoi = this.playerFrames[this.bankerSide].getSeatRandomPoi();
                                        let endPoi = this.playerFrames[side].getSeatRandomPoi_new();
                                        let chip = this.chipRect.chipItemMgr.getChip(denomination);
                                        //SoundMgrBaccarat.chipFly();
                                        //console.log('111111111');
                                        chip.play(
                                            { x: startPoi.x, y: startPoi.y},
                                            { x: endPoi.x, y: endPoi.y },
                                            Handler.create(this, () => {
                                                this.chipRect.chipItemMgr.hideChip(chip);
                                            }, [], true)
                                        )
                                    }
                                }
                            }
                        }
                    })
                }
            }
            return cb;
        }

        private autoExit() {
            //自动退出
            Laya.timer.once(30000, this, this.onExitRoom);
        }
        private clearAutoExit() {
            Laya.timer.clear(this, this.onExitRoom);
        }


        pageStyleSetting(data) {
            //加载真正的背景
            let url = ResourceMgr.RES_PATH+'bg/bg1.jpg';
            Tools.inst.changeBackground(url, this._view.getChild('bg').asLoader);
        }

        /**********setSeat******************/
        private posServerSelf: number = null;
        private localPosList: Array<number> = null;
        private local2serverPos: Array<number> = [];
        private server2localPos: Array<number> = [];
        public playerCount: number = 0;
        transferServerPos(posServerSelf: number, playerCount: number) {
            this.playerCount = playerCount;
            for (let i = 0; i < this.playerCount; i++) {
                let temp = (i + posServerSelf) % this.playerCount;
                //tempNetworkseat = tempNetworkseat >= this.playerCount ? tempNetworkseat - this.playerCount : tempNetworkseat;
                this.server2localPos[i] = temp;
                this.local2serverPos[temp] = i;
            }
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

    export class G9999HeadInfo {
        private xianHongData: string;
        private xianHongText: fairygui.GLabel;
        private xiaXianData: string;
        private xiaXianText: fairygui.GLabel;
        private shangXianData: string;
        private shangXianText: fairygui.GLabel;
        constructor(parent: fairygui.GComponent) {
            this.xianHongText = parent.getChild('txtXianHongValue').asLabel;
            this.xiaXianText = parent.getChild('txtXiaXianValue').asLabel;
            this.shangXianText = parent.getChild('txtShangXianValue').asLabel;
        }

        set XianHong(value: string) {
            this.xianHongText.text = value;
        }
        get XianHong() {
            return this.xianHongText.text
        }

        set XiaXian(value: string) {
            this.xiaXianText.text = value;
        }
        get XiaXian() {
            return this.xiaXianText.text
        }

        set ShangXian(value: string) {
            this.shangXianText.text = value;
        }
        get ShangXian() {
            return this.shangXianText.text
        }
    }

    class ChipPosData {
        private data: Array<Array<Array<{ x?: number, y?: number }>>>;
        private place: Array<number>;
        private denomination: Array<number>;
        constructor() {
            this.place = [3, 4, 5, 1, 2];//下注区
            //this.denomination = [100, 500, 1000, 2000, 5000, 10000];
            this.denomination = [1, 2, 5, 10, 20, 50];//------JiaTao
            this.data = [];
            for (var i = 0; i < this.place.length; i++) {
                var v1 = this.place[i];
                this.data[v1] = [];
                for (var j = 0; j < this.denomination.length; j++) {
                    var v2 = this.denomination[j];
                    this.data[v1][v2] = [];
                }
            }
        }

        getPoi(place: number, denomination: number) {
            if (place == null || denomination == null) {
                return null;
            }
            if (this.data[place] != null) {
                if (this.data[place][denomination] != null) {
                    return this.data[place][denomination].shift();
                }
            }
            return null;
        }

        addPoi(place: number, denomination: number, poi: { x?: number, y?: number }) {
            if (place == null || denomination == null || poi == null) {
                return;
            }
            if (this.data[place] != null) {
                if (this.data[place][denomination] != null) {
                    this.data[place][denomination].push(poi);
                }
            }
        }

        clearPoi() {
            this.place = [3, 4, 5, 1, 2];
            //this.denomination = [100, 500, 1000, 2000, 5000, 10000];
            this.denomination = [1, 2, 5, 10, 20, 50];//------JiaTao

            for (var i = 0; i < this.place.length; i++) {
                var v1 = this.place[i];
                for (var j = 0; j < this.denomination.length; j++) {
                    var v2 = this.denomination[j];
                    this.data[v1][v2].splice(0, this.data[v1][v2].length);
                }
            }
        }
    }


} 