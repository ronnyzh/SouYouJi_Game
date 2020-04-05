module G549 {
    export class G549Page extends G548.G548Page {
        //----------------JiaTao 路单百家乐专有属性
        private showWait : fairygui.GComponent;//2018-12-21JiaTao
        //-----------------end
        playerFrames: Array<G549PlayerFrame> = [];

        constructor(scene = 'GameScene') {
            super('G548', scene, UILayer.GAME);
        }

        onDispose() {
            super.onDispose();
            Laya.timer.clear(this,this.randomJettonLight);
        }

        onCreated(data: any = null) {
            //data['typeoflayout'] = 2;//界面选择
            this.layout = 2;
            this.gameId = 549;
            super.onCreated(data,G549PlayerFrame);
            this.c_GameType.selectedIndex = 1;
            this.showWait = this._view.getChild('showWait').asCom;//2018-12-21JiaTao
            let txt_msg = this.showWait.getChild('txt_msg').asLabel;
            let info = ExtendMgr.inst.getText4Language(txt_msg.text);
            txt_msg.text = info;
            this.initDrawcall();
        }

        //-------JiaTao Drawcall优化
        initDrawcall(){
            super.initDrawcall();
            //路单
            let waybillCom = this._view.getChild('waybillCom').asCom;
            waybillCom.displayObject.cacheAs = this.cashAsMode;
        }
        //----重置下注区数据
        resetAreaCom(){
            super.resetAreaCom();
            this.showWait.visible = this.destoryRoom;
            this.isViewer = false;//2018-12-22 用来重置观察者身份
            this.jetton_Layout.removeChildren();
            //----隐藏飘分 2018-12-20 16:00
            for(let i = 0; i < 9; ++i){
                this.getPlayer(i).hideScore();
            }
        }

        getPlayer(side: number, server: boolean = false): G549PlayerFrame {
            if (server) side = this.getLocalPos(side);
            return this.playerFrames[side];
        }

        initMsgListen() {
            super.initMsgListen();
            //NetHandlerMgr.netHandler.addMsgListener(G548.S_C_AFTERREFRESh_BCR, this.onAfterRefresh.bind(this));
            //路单
            NetHandlerMgr.netHandler.addMsgListener(S_C_SEND_LUDAN, this.setdLudan.bind(this));
            //观察者
            NetHandlerMgr.netHandler.addMsgListener(S_C_SEND_VIEWER_DATA, this.initViewer.bind(this));
            //踢人
            NetHandlerMgr.netHandler.addMsgListener(S_C_SEND_NOBID_COUNT, this.nobidCount.bind(this));
        }
        //踢人
        private kick : boolean = false;
        nobidCount(msgData){
            let count = msgData['count'];
            if(count == 3){
                this.xianH.getChild('msg').text = ExtendMgr.inst.getText4Language('第5局后将自动退出房间');
                this.xianH.getTransition('xianH').play();
            }else if(count == 5){
                this.kick = true;
            }
        }
        //观察者
        initViewer(msgData){//(0:结算阶段,1:抢庄阶段,2:下注阶段,3:倒计时阶段)//仿写断线重连
            //console.log('观察者数据',msgData);
            this.showWait.visible = true;
            //------------------分割--------------------//
            let left_MS = msgData['leftMS'];
            let stage = parseFloat(msgData['stage']);
            let voteresult = msgData['voteresult'];
            this.bidValue = msgData['bidValue'];
            switch(stage){
                case 0:
                    this.showBetArea(true);
                    this.onAfterBidNew(msgData);
                    break;
                case 1:
                    this.isViewer = true;
                    break;
                case 2:
                    this.showBetArea(true);
                    this.isViewer = true;
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
                    player.setSeat(playerInfo,side);
                }
            }, this);
            //--显示庄家标识
            if(stage==2||stage==0){
                //--显示庄家标识
                let side = voteresult[0]['side'];
                
                let bankerSide = this.getLocalPos(side);
                let player = this.getPlayer(bankerSide);
                player.updateBankerState(true);
                this.bankerSide = bankerSide;
                this.swapSeat(this.bankerSide);
                //--初始化按钮面额 和 筹码颜色选择有关，不可删除
                let bidValue = msgData['bidValue'];
                for(let i = 0,len = bidValue.length; i < len; ++i){
                    let jetton = this._view.getChild('jetton'+i).asCom;
                    let score = jetton.getChild('title').asLabel;
                    score.text = Tools.inst.changeGoldToMoney(bidValue[i]);
                }
            }
            this.clearTimer();
            if(stage!=0){
                let leftMS = parseFloat(msgData['leftMS']) / 1000;//Jia stage 1:抢庄阶段,2:下注阶段
                this.clearTimer();
                this.setTimer(parseInt(leftMS.toString()),stage);//0 即将开始 1抢庄 2开始下注 3请亮牌 4匹配 5开始比牌 6开始要牌 7正在开牌
            }
            //桌面数据恢复
            let onbidlist = msgData['onbidlist'];
            for(let i = 0,len = onbidlist.length; i < len; ++i){
                let value = onbidlist[i];
                let place = value['place'];
                let side = this.getLocalPos(value['chair']);
                let denomination = value['denomination'];
                let qty = value['qty'];//下注位置 面额 数量 玩家位置
                let subtotalmoney = value['subtotalmoney'];
                let totalplacemoney = value['totalplacemoney'];
                this.flyJetton(place,Tools.inst.changeGoldToMoney(denomination),qty,side);//,subtotalmoney,totalplacemoney
                //--------------更新下注区分数---------------------//
                let areaCom = this.AreaCom.getChild('area_'+place).asCom;
                let txtSelfChip = areaCom.getChild('txtSelfChip').asLabel;
                let txtTotalChip = areaCom.getChild('txtTotalChip').asLabel;
                txtTotalChip.text = Tools.inst.changeGoldToMoney(totalplacemoney);
                if(side==0){
                    txtSelfChip.text = Tools.inst.changeGoldToMoney(subtotalmoney);
                }
                //-------------------end---------------------//
            }
        }
        //路单
        private destoryRoom : boolean = false;
        private isCut : boolean = false;//防止‘房间即将关闭’显示的过早
        setdLudan(msgData){
            //console.log('房间路单信息',msgData);
            let waybillCom = this._view.getChild('waybillCom').asCom;
            let startPoint = waybillCom.getChild('startPoint').asImage;
            let subBoxLayout = waybillCom.getChild('subBoxLayout').asCom
            let subBoxList = waybillCom.getChild('subBoxList').asList;//----------
            //subBoxList.removeChildrenToPool();
            subBoxList.numItems = 120;//----------
            let ludan = msgData['ludan'];
            let gamecount = msgData['gamecount'];
            gamecount = this.isCut?(gamecount-1):gamecount;
            if(gamecount==70){//-----用来判断是否是最后一局  
                let txt_msg = this.showWait.getChild('txt_msg').asLabel;
                txt_msg.text = ExtendMgr.inst.getText4Language('房间即将关闭');
                this.showWait.visible = true;
                this.destoryRoom = true;
            }

            if(this.isCut)
                this.isCut = false;
            else if(gamecount==69)
                this.destoryRoom = true;
            
            let len = ludan.length;
            if(len==0)return;
            let firstLineNum = ludan[0]['ludan_row'].length;
            let endLineNum = ludan[len-1]['ludan_row'].length;
            let maxLineNum = firstLineNum > endLineNum ? firstLineNum : endLineNum;
            for(let i = 0; i < len; ++i){
                let value = ludan[i]['ludan_row'].length;
                if(value>maxLineNum){
                    maxLineNum = value;
                }
            }
            let hideIndex = 0;
            if(maxLineNum>20){
                hideIndex = maxLineNum - 20;
            }
            //subBoxLayout.removeChildren();
            subBoxList.removeChildrenToPool();
            for(let i = 0; i < 120; ++i){
                //subBoxList.addItemFromPool();
                let box = subBoxList.addItemFromPool().asCom;
                box.getController('c_win').selectedIndex = 0;
                box.getController('c_he').selectedIndex = 0;
                box.getController('c_point').selectedIndex = 0;
            }
            //subBoxList.numItems=120;
            for(let i = 0,len1 = ludan.length; i < len1; ++i)
            {
                for(let j = 0,len2 = ludan[i]['ludan_row'].length; j < len2; ++j)
                {
                    if(j < hideIndex) continue;
                    let index = (j-hideIndex)+20*i;//----------
                    let box = subBoxList.getChildAt(index).asCom;
                    //let box = subBoxList.addItemFromPool().asCom;//subBoxList.getChildAt(index).asCom;//----------
                    let value = ludan[i]['ludan_row'][j];
                    //let index = (j-hideIndex)+20*i;//----------
                    //let box = subBoxList.addItemFromPool().asCom;//subBoxList.getChildAt(index).asCom;//----------
                    let winType = 0;
                    let heType = 0;
                    let pointType = 0;//默认设置控制器索引为10,不显示任何点数.
                    if(value!='-')
                    {
                        let str = value.split('');
                        if(str[0]=='0'){//---开局第一局或前几局都是和
                            heType = 1;//2019-1-9
                            winType = 3;//c_win 3 表示和赢 显示绿圈
                        }else{
                            winType = parseInt(str[0]);
                            let point = parseInt(str[1]);//----------
                            pointType = point==0 ? 10 : point;//----------
                        }
                    }
                    let c_win = box.getController('c_win');
                    let c_he = box.getController('c_he');
                    let c_point = box.getController('c_point');
                    c_he.selectedIndex = heType;
                    c_point.selectedIndex = pointType;
                    c_win.selectedIndex = winType;//和显示绿圈
                }
            }
        }

        gameReady(msgData){
            // console.log('游戏即将开始',msgData);
            this.resetAreaCom();//-------------重置上一局信息
            if(this.destoryRoom) return;
            super.gameReady(msgData);
        }
        //开始抢庄
        onStartGrabDealer(msgData) {
            super.onStartGrabDealer(msgData);
            this.showWait.visible = this.isViewer;
            this.c_bar.selectedIndex = 2;
            if(this.isViewer) return;
            this.c_bar.selectedIndex = 3;//显示抢庄条
        }

        //换回庄家到原来的位置
        resetSeat(bankerSide:number){
            super.resetSeat(bankerSide);
            this.getPlayer(bankerSide).updateBankerState(false);
        }

        randomJettonLight(){ 
            if(this._view==null) return;
            super.randomJettonLight();
        }
        initBetBtn(){
            let jetton = ['jetton0','jetton1','jetton2','jetton3'];//,'jetton20','jetton50'
            for(let i = 0; i < jetton.length; ++i){
                let cb = function(){
                    //console.log('选中按钮');
                    G548.SoundMgrBaccarat.chipClick();
                    let chose = this._view.getChild(jetton[i]).asCom.getChild('title').asLabel.text;
                    chose = parseInt(chose);//以后如果要显示小数的话,需要改动.
                    if(chose != 0){
                        this.denomination = chose;
                    }
                    else{
                        this.denomination = 1;
                    }
                }
                let btn_jetton = this._view.getChild(jetton[i]).asButton;
                btn_jetton.onClick(this,cb.bind(this),[]);
            }
            if(this.isViewer)return;
            Laya.timer.loop(2000,this,this.randomJettonLight,[],false);//开启扫光 ,[],false
        }

        startBid(msgData){
            super.startBid(msgData);//这里面有开启btnExitEnd按钮
            this.btnExitEnd(false);
            this.showWait.visible = this.isViewer;
        }
        //-----------结算阶段断线重连调用函数
        onAfterBidNew(msgData){
            let setUserDatas = msgData['balance'][0]['setUserDatas'];
            this.jetton_Layout.removeChildren();
            let cardresStr = setUserDatas[0]['cardres'];
            let cardres = JSON.parse(cardresStr);
            this.initCardValue(cardres);
            let xianFen = cardres['x'][1];
            let zhuangFen = cardres['z'][1];
            //console.log('新版结算断线重连',xianFen,zhuangFen,'牌值',this.cardValue);
            this.showCard(xianFen,zhuangFen,this.cardValue);
            Laya.timer.once(500,this,this.showScore,[setUserDatas],false);
        }
        //结算阶段断线重连 显示牌
        showCard(xianFen,zhuangFen,cardValue){
            //---牌
            let showCardCom = this.AreaCom.getChild('showCard').asCom;
            let X_Score = showCardCom.getChild('X_Score').asLabel;
            let Z_Score = showCardCom.getChild('Z_Score').asLabel;
            X_Score.text = xianFen.toString();
            Z_Score.text = zhuangFen.toString();
            let c_bg = showCardCom.getController('c_bg');
            let c_score = showCardCom.getController('c_score');
            c_bg.selectedIndex = 1;
            c_score.selectedIndex = 1;
            for(let i = 0; i < 6; ++i){
                let Card = showCardCom.getChild('card_'+i).asCom;
                let value = cardValue[i];
                if(value=='') continue;
                Card.visible = true;
                Card.icon = G549Page.getCardPath(value);
            }
            this.showResult(xianFen,zhuangFen);
        }
        //结算阶段断线重连 显示输赢结果
        showResult(xianFen,zhuangFen){
            //---结果
            let resultCom = this.AreaCom.getChild('resultCom').asCom;
            let c_result = resultCom.getController('c_result');
            let z_bei = resultCom.getChild('z_bei').asLabel;
            let x_bei = resultCom.getChild('x_bei').asLabel;
            if(xianFen>zhuangFen){//闲赢 2
                c_result.selectedIndex = 2;
                x_bei.text = xianFen.toString();
            }else if(xianFen < zhuangFen){//庄赢 1
                c_result.selectedIndex = 1;
                switch(zhuangFen){
                    case 6 : 
                        zhuangFen.text = '3';
                    break;
                    default : 
                        zhuangFen.text = zhuangFen.toString();
                    break
                }
            }else if(xianFen == zhuangFen){//和 3
                c_result.selectedIndex = 3;
            }
        }
        //结算阶段断线重连 显示飘分结果
        showScore(setUserDatas){
            //console.log('断线重连飘分',setUserDatas);
            this.showWait.visible = true;
            let playerDatas = setUserDatas;
            for(let i = 0,len = playerDatas.length; i < len; ++i)
            {
                let value = playerDatas[i];
                let side = this.getLocalPos(value['side']);
                let player = this.getPlayer(side);
                let changegold = value['changegold'];
                let gold = value['gold'];
                // console.log('飘分数据',changegold,gold,side);
                player.changeScore(changegold);
                player.setScoreString(gold);
            }
        }

        jettonRecycle(){
            super.jettonRecycle();
            if(this.destoryRoom){//-----用来判断是否是最后一局  
                let txt_msg = this.showWait.getChild('txt_msg').asLabel;
                txt_msg.text = ExtendMgr.inst.getText4Language('房间即将关闭');
            }
            this.showWait.visible = true;
        }

        static getCardPath(cardId: string) {
            return super.getCardPath(cardId);
        }
        //-----贝塞尔结束
        //断线重连

        // //-------JiaTao
        onAfterRefreshBid(msgData) {//(0:结算阶段,1:抢庄阶段,2:下注阶段,3:倒计时阶段)
            //console.log('断线重连6666666666',msgData);
            let left_MS = msgData['leftMS'];
            let stage = parseFloat(msgData['stage']);
            let voteresult = msgData['voteresult'];
            this.bidValue = msgData['bidValue'];
            switch(stage){
                case 0:
                    this.showBetArea(true);
                    this.onAfterBidNew(msgData);
                break;
                case 1:
                    this.c_bar.selectedIndex = 3;
                break;
                case 2:
                    this.isCut = true;
                    this.showBetArea(true);
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
                    player.setSeat(playerInfo,side);
                }
            }, this);
            //--显示庄家标识
            if(stage==2||stage==0){
                let side = voteresult[0]['side'];
                let bankerSide = this.getLocalPos(side);
                let player = this.getPlayer(bankerSide);
                player.updateBankerState(true);
                this.bankerSide = bankerSide;
                this.swapSeat(this.bankerSide);
                //--初始化按钮面额 和 筹码颜色选择有关，不可删除
                let bidValue = msgData['bidValue'];
                for(let i = 0,len = bidValue.length; i < len; ++i){
                    let jetton = this._view.getChild('jetton'+i).asCom;
                    let score = jetton.getChild('title').asLabel;
                    score.text = Tools.inst.changeGoldToMoney(bidValue[i]);
                }
            }
            //-------如果不是庄的话开启下注功能
            if(this.bankerSide != 0&&stage==2){
                //console.log('开启按钮');
                this.c_seat.selectedIndex = 1;
                this.showJetton();
                this.initBetBtn();
                this.initPlace();
            }
            //----------end
            this.clearTimer();
            if(stage!=0){
                let leftMS = parseFloat(msgData['leftMS']) / 1000;//Jia stage 1:抢庄阶段,2:下注阶段
                this.clearTimer();
                this.setTimer(parseInt(leftMS.toString()),stage);//0即将开始 1抢庄 2开始下注 3请亮牌 4匹配 5开始比牌6开始要牌 7正在开牌
            }
            
            let onbidlist = msgData['onbidlist'];
            for(let i = 0,len = onbidlist.length; i < len; ++i){
                let value = onbidlist[i];
                let place = value['place'];
                let side = this.getLocalPos(value['chair']);
                let denomination = value['denomination'];
                let qty = value['qty'];//下注位置 面额 数量 玩家位置
                let subtotalmoney = value['subtotalmoney'];
                let totalplacemoney = value['totalplacemoney'];
                this.flyJetton(place,Tools.inst.changeGoldToMoney(denomination),qty,side);
                //--------------更新下注区分数---------------------//
                let areaCom = this.AreaCom.getChild('area_'+place).asCom;
                let txtSelfChip = areaCom.getChild('txtSelfChip').asLabel;
                let txtTotalChip = areaCom.getChild('txtTotalChip').asLabel;
                txtTotalChip.text = Tools.inst.changeGoldToMoney(totalplacemoney);
                if(side==0){
                    txtSelfChip.text = Tools.inst.changeGoldToMoney(subtotalmoney);
                }
                //------------------end--------------------------//
            }
        }

        
        onGoldExitRoomResult(msgData) {
            if(this.isCloseExitRoomResult) return;
            //console.log('G549退房',msgData);
            if(msgData['result'])
            {
                let callback = ()=> 
                {
                    this.destoryAllBtn();
                    this.clearTimer();
                    UserMgr.inst.returnToLobby();
                }

                if(this.kick)
                    Alert.show(ExtendMgr.inst.getText4Language('连续5局没有下注退出房间')).onYes(callback);
                else
                    callback();
            }
            else
            {
                NetHandlerMgr.netHandler.sendData(ProtoKeyParty.C_S_EXIT_ROOM_CONFIRM);
            }
            /*
            let result = msgData['result'];
            if(result&&this.kick){
                Alert.show(ExtendMgr.inst.getText4Language('连续5局没有下注退出房间')).onYes(()=> {
                    this.destoryAllBtn();
                    this.clearTimer();
                    UserMgr.inst.returnToLobby();
                });
            }
            else if (result) {
                this.destoryAllBtn();
                this.clearTimer();
                UserMgr.inst.returnToLobby();
            } else {
                NetHandlerMgr.netHandler.sendData(ProtoKeyParty.C_S_EXIT_ROOM_CONFIRM);
            }
            */
        }

        reconnectResult(connected) {
            if (!connected) return;
            let sid = UserMgr.inst.sid;
            NetHandlerMgr.netHandler.enterGame(sid, this.gameId, this.onEnterRoomSuccess.bind(this));
            NetHandlerMgr.inst.initPingListen(G548.S_C_PING);
        }
    }
} 