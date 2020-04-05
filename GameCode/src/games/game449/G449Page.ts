class G449Page extends G445Page {
    newPlayerFrame(data) {
        return new G449PlayerFrame(data);
    }
    public gameID = 449;

    public isReadyHandFancy = false;
    //private playerCount = 2;

    pageStyleSetting(data) {
        let view = this._view;
        var txtTitle = view.getChild('txtTitle').asLabel;
        txtTitle.text = ExtendMgr.inst.getText4Language("二人麻将");
    }
    Createbgurl() {

        return ResourceMgr.RES_PATH + 'bg/main_bg1.jpg';
    }
    posLocalList = [0, 2];
    initGameInfo(gameInfo) {
        //console.log('gameInfo',gameInfo)

        var roomInfo = gameInfo["roomInfo"];
        var playerList = roomInfo["playerList"];
        var roomId = roomInfo["roomId"];
        var roomSetting = roomInfo["roomSetting"];
        var roomName = roomInfo["roomName"];

        this.playerCount = roomInfo["playerCount"] || 4;

        var selfInfo = gameInfo["selfInfo"];
        this.posServerSelf = selfInfo["side"];

        MahjongMgr.inst.transferServerPos(this.posServerSelf, this.posLocalList);

        //剩余牌张数显示
        this.tileTotal = roomInfo["tileCount"];
        this.refreshLeftTileCount(this.tileTotal);

        this.initMsgListen();
    }
    initMsgListen() {
        super.initMsgListen();
        NetHandlerMgr.netHandler.addSequenceMsgListener(G449.S_C_BAOTINGRESULT, this.onBaoTingResult.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(G449.S_C_DONOTGETAFTERTING, this.onNotGetAfterTing.bind(this));

    }
    updatePlayerTurn(posServer, time = 15) {
        var posLocal = this.getLocalPos(posServer);
        let dealerside = this.getLocalPos(this.posDealerServer);
        let num = posLocal;
        if (posLocal == dealerside)
            num = 0;
        else
            num = 2;

        //  console.log(num, posLocal, "===========出牌位置");
        if (posLocal == 0) {
            this.getPlayer(0).setselfDrag();  //手牌可拖拽
        }
        else {
            this.getPlayer(0).setselfNotDrag();
        }
        this.gameSideCtl.setSelectedIndex(num);
        MahjongMgr.inst.refreshPlayerTurn(posLocal);

        this.game_seconds = time;
        this.setTimer(this.game_seconds);
    }
    onBaoTingResult(msgData, finishedListener) {
        // console.log("=====this.isTingAction======", this.isTingAction)
        var otherData = msgData["OtherData"];
        var playerData = msgData['playerData'];
        Tools.inst.each(playerData, function (item) {
            var selfside = this.getLocalPos(item["side"]);
            if (selfside == 0)
                this.isTingAction = true;
        }, this);
        Tools.inst.each(otherData, function (item) {
            var side = this.getLocalPos(item["side"]);
            // console.log(side, "=============报听翻牌位置");
            var handTiles = item["handTiles"];
            var lastTile = item["lastTile"];
            if (lastTile != null)
                handTiles.push(lastTile);
            //  console.log(handTiles, "=========handTiles");
            this.getPlayer(side).setOtherBaotingshow(handTiles)

        }, this);


        //获得听牌列表
        //NetHandlerMgr.netHandler.sendGetReadyHand();
        if (finishedListener != null)
            finishedListener();
    }
    onNotGetAfterTing() {
        //过取消
        this.playerSelf.ReadyHandFancyEvt = null;
        this.playerSelf.resetcardcolor();
        this.tingpanel.visible = false;
        this.getPlayer(0).setselfDrag();
    }
    onProxy(msgData) {
        var data = msgData["data"];
        var stateCtl = this._view.getController('proxy');
        for (var i = 0; i < data.length; i++) {
            var side = this.getLocalPos(data[i]["side"]);
            if (side != 0) continue;
            var isproxy = data[i]["isproxy"];
            stateCtl.setSelectedIndex(isproxy ? 1 : 0);
        }
    }
    //收到玩家是否听牌协议
    onReadyHand(msgData, finishedListener) {
        //console.log(msgData, "=====2人=========听牌");
        // this.getPlayer(0).getTilesDataMeld();
        let readyHandTiles = msgData["tile"];
        let myFancyTiles = msgData["myTiles"];
        myFancyTiles.sort();
        let listLength = readyHandTiles.length;
        if (listLength == 0) {
            // mb.readyHandTiles = [];
            // console.log(this, "=============");
            this.tingdatas.splice(0, this.tingdatas.length);
            //this.operatorArea.hideReadyHand();
            this.tingBtn.visible = false;
            this.tingpanel.visible = false;
            this.tingAutoBtn.visible = false;
            this.isTingAuto = false;
        }
        else {
            this.tingdatas.splice(0, this.tingdatas.length);
            for (let i = 0; i < readyHandTiles.length; i++) {
                // let cardid = readyHandTiles[i].split(':')[0];
                let cardid = readyHandTiles[i];
                this.tingdatas.push(cardid);
            }
            //console.log(this.isTingAction, "================this.isTingAction");
            if (this.isTingAction) {
                this.refreshTingpanel();
                this.tingBtn.visible = true;
                this.tingpanel.visible = true;
                this.tingAutoBtn.visible = true;
                this.tingAutoBtnCtl.selectedIndex = 1;
                this.tingAutoBtn.enabled = false;
            }
            else {
                this.tingBtn.visible = false;
                this.tingpanel.visible = false;
                this.tingAutoBtn.visible = false;
            }

        }
        if (finishedListener != null)
            finishedListener();
    }
    onShowActionOption(msgData, finishedListener = null) {
        // console.log(msgData, "=========吃碰杠");
        // this.turnIndicator.indicate(0);
        // this.tileTouch.setDiscardable(false);
        var actionData = msgData["actions"];
        var actionNum = msgData["num"] || 0;
        var data = [];
        var tileId2Action = {};
        var kongTiles = [];
        for (var i = 0; i < actionData.length; i++) {
            var oneActionData = actionData[i];
            var oneActionType = oneActionData["action"];
            var oneActionTiles = oneActionData["tiles"];
            var isOriginHu = false;

            if ((this.lastDrawPlayer == this.playerSelf) && (oneActionType == ACTION_OPTION.HU))
                isOriginHu = true;

            if ((oneActionType == ACTION_OPTION.SELF_KONG) || (oneActionType == ACTION_OPTION.CONCEALED_KONG)) {
                kongTiles = kongTiles.concat(oneActionTiles);

                Tools.inst.each(oneActionTiles, function (value, key) {
                    tileId2Action[value] = oneActionType;
                }, this);
                continue;
            }

            var oneData = {
                "type": oneActionType,
                "choiceList": oneActionTiles,
                "isOriginHu": isOriginHu
            };
            if (oneActionType == 7) {
                this.getPlayer(0).setselfNotDrag();
                oneData.choiceList = [oneActionTiles.join(',')];
            }
            data.push(oneData);
        }

        if (kongTiles.length != 0) {
            var kongData = {
                "type": ACTION_OPTION.SELF_KONG,
                "choiceList": kongTiles.sort(),
                "isOriginHu": false
            };
            data.push(kongData);
        }

        var cb = this.getActionCB(tileId2Action, actionNum);

        //show之前先隐藏一次
        this.operatorArea.hide();
        this.operatorArea.show(data, cb);

        if (finishedListener) finishedListener();
    }
    onPlayerAction(msgData: { side: number, action: { action: number, tiles: string[], beActionSide?: number }[] }, finishedListener) {
        this.operatorArea.hide();

        var actionData = msgData["action"][0];
        var type = actionData["action"];
        var doSide = msgData["side"];
        var passiveSide = actionData["beActionSide"];
        var meldTileList = actionData["tiles"];

        this.updatePlayerTurn(doSide);

        var player = this.getPlayer(doSide, true);
        var passivePlayer = (passiveSide == null ? null : this.getPlayer(passiveSide, true));

        var actData = {
            "type": type,
            "getPlayer": player,
            "passivePlayer": passivePlayer,
            "tileData": (meldTileList[meldTileList.length - 1]),
            "originalList": (meldTileList),
            "list": meldTileList,
            "isShowEffect": (!msgData["instant"]),
            "from": this.getLocalPos(passiveSide),
            "container": this
        };
        // console.log('onPlayerAction:',actData);

        var doActionCB = () => {
            if (type == ACTION_OPTION.CHOW || type == ACTION_OPTION.PONG) {
                this.updatePlayerTurn(doSide);
            }
            this.lastDrawPlayer = null;

            if (this.getLocalPos(doSide) == 0) {
                /**吃碰杠后显示预听牌 */
                if (type == ACTION_OPTION.CHOW || type == ACTION_OPTION.PONG || ACTION_OPTION.OTHERS_KONG || ACTION_OPTION.SELF_KONG || ACTION_OPTION.CONCEALED_KONG) {
                    this.ready_hand_fancy()
                }
            }

            if (finishedListener != null)
                finishedListener();
        };
        try {
            var removeTileID = actData["tileData"];
            switch (type) {
                case ACTION_OPTION.CHOW:
                    passivePlayer.removeOutTile(removeTileID);
                    player.chow(actData, doActionCB);
                    this.refreshTingpanel();
                    return;
                case ACTION_OPTION.PONG:
                    passivePlayer.removeOutTile(removeTileID);
                    player.pong(actData, doActionCB);
                    this.refreshTingpanel();
                    return;
                case ACTION_OPTION.OTHERS_KONG:
                    passivePlayer.removeOutTile(removeTileID);
                    player.kong(actData, doActionCB);
                    this.refreshTingpanel();
                    return;
                case ACTION_OPTION.SELF_KONG:
                    player.addToKong(actData, doActionCB);
                    this.refreshTingpanel();
                    return;
                case ACTION_OPTION.CONCEALED_KONG:
                    player.concealedKong(actData, doActionCB);
                    this.refreshTingpanel();
                    return;
                case ACTION_OPTION.HU:
                    this.onPlayerHu(actData, finishedListener);
                    return;
                case ACTION_OPTION.TING:
                    this.doTingAction(type, actData, msgData, finishedListener);
                    break;
                default:
                    this.doSpecialAction(type, actData, msgData, finishedListener);

                    return;
            }
        } catch (error) {
            console.log(error)
        }
        if (finishedListener) finishedListener();
    }
    onPlayerDraw(msgData, finishedListener) {
        var drawDataList = msgData["tiles"];
        var posDrawServer = msgData["side"];
        var player = this.getPlayer(posDrawServer, true);
        this.lastDrawPlayer = player;

        var drawData = drawDataList.shift();
        var inIDList = drawData["inTiles"] || [];
        var outIDList = drawData["outTiles"] || [];
        // console.log(inIDList, "============inIDList");
        var inList = [];
        Tools.inst.each(inIDList, function (id) {
            inList.push(id);
        }, this);
        this.refreshLeftTileCount(inList.length, true);
        player.drawHandTile(inList);
        SoundMgr.drawTile();

        this.updatePlayerTurn(posDrawServer);

        if (this.isFirstDraw && this.getLocalPos(posDrawServer) == 0) {
            this.tfTips.visible = this.isFirstDraw;
            // console.log('this.isFirstDraw',this.isFirstDraw)
        }
        if (finishedListener) finishedListener();
    }

    onPlayerHu(data, cb) {
        var huPlayer = data["getPlayer"];
        var huTiles = data["list"];
        var passivePlayer = data["passivePlayer"];
        var removeTileID = data["tileData"];

        //关掉指示器,手牌不让操作
        // this.turnIndicator.stopCountdown();
        // this.tileTouch.setDiscardable(false);

        //摊牌
        var handWallTiles = [];
        var lastTilePos = null;
        if (passivePlayer != null) {
            huPlayer.addHandTiles([removeTileID]);
            //出牌人的牌拿走
            passivePlayer.removeOutTile(removeTileID);
        }

        huPlayer.hu(data, cb, this.doTingAction);
    }
    refreshTingpanel(isclick = false) {
        //刷新
        // console.log(isclick, "=============refreshTingpanel");
        if (isclick) {
            if (this.isTingAction && this.tingdatas != null && this.tingdatas.length > 0) {
                this.tingpanel.visible = !this.tingpanel.visible;
                if (this.tingpanel.visible) {
                    this.showtingpanel();
                }
            }
            else {
                this.tingBtn.visible = false;
                this.tingpanel.visible = false;
                this.tingAutoBtn.visible = false;
            }
        }
        else {
            if (this.isTingAction && this.tingdatas != null && this.tingdatas.length > 0)
                this.showtingpanel();
            else {
                this.tingBtn.visible = false;
                this.tingpanel.visible = false;
                this.tingAutoBtn.visible = false;
            }
        }
    }
    showtingpanel(tingdatas = this.tingdatas) {
        this.tingpanel.visible = true;
        //console.log(this.tingdatas, "===============需要显示时的听牌数据");
        let tinglist = this.tingpanel.getChild('tinglist').asList;
        for (let i = tinglist.numChildren - 1; i >= 0; i--) {
            tinglist.removeChildrenToPool();
        }
        for (let i = 0; i < tingdatas.length; i++) {
            let card = tinglist.addItemFromPool().asCom;
            var icon = card.getChild('icon');
            let onetinglist = tingdatas[i].split(':')
            MahjongMgr.inst.setTile(icon.asLoader, onetinglist[0]);
            let num = this.getcardremainnum(onetinglist[0]);
            var txt = card.getChild('numtxt').asTextField;
            let ctl = card.getController('numtype');
            if (num > 0) {
                ctl.selectedIndex = 0;
            } else {
                ctl.selectedIndex = 1;
            }
            let fantxt = card.getChild('fantxt').asTextField;
            if (onetinglist[1] != null) {
                fantxt.visible = true;
                fantxt.text = onetinglist[1].toString() + ExtendMgr.inst.getText4Language("番");
            }
            else
                fantxt.visible = false;
            txt.text = num.toString();
        }
        //  tinglist.resizeToFit();
        let bg = this.tingpanel.getChild('bg');
        let cardNum = tinglist.numChildren;
        if (cardNum > 0 && cardNum <= 7) {
            let card = tinglist.getChildAt(0).asCom;
            this.tingpanel.x = this._view.actualWidth / 2 - ((cardNum - 1) * (card.actualWidth + tinglist.columnGap) / 2) * this.tingpanel.scaleX;
            this.tingpanel.y = this.view.actualHeight / 2 - card.actualHeight / 2;
            bg.width = cardNum * (card.actualWidth + tinglist.columnGap) - tinglist.columnGap / 3;
            bg.height = tinglist.getChildAt(0).asCom.actualHeight * 1 + tinglist.lineGap;
        }
        else if (cardNum > 7) {
            let multiple = Math.floor((cardNum - 1) / 7);
            let card = tinglist.getChildAt(0).asCom;
            this.tingpanel.y = this.view.actualHeight / 2 - card.actualHeight * multiple / 2;
            this.tingpanel.x = this._view.actualWidth / 2 - (6 * (card.actualWidth + tinglist.columnGap) / 2) * this.tingpanel.scaleX;
            bg.width = 7 * (card.actualWidth + tinglist.columnGap) - tinglist.columnGap / 3;
            bg.height = (tinglist.getChildAt(0).asCom.actualHeight + tinglist.lineGap) * (multiple + 1);
        }

    }

    showBalance(setData) {
        this.setBalance.showData(setData, 0, this.playerCount, this.roomNumstr);
    }

    getActionCB(tileId2Action, actionNum) {
        //console.log(tileId2Action, actionNum, "=========11111111getActionCB");
        return (type, meldList) => {
            // console.log(type, meldList, "============getActionCB");
            if (type == ACTION_OPTION.TING) {
                this.isClickTing = true;
                // console.log(meldList, "==========meldList")
                this.tryMarkTiles(meldList);
                let chooseList = meldList.concat();
                chooseList = chooseList.split(',');
                this.tingClick(chooseList, this.getPlayer(0).tilesDataHand);
                //this.tileTouch.setDiscardable(true);
                this.playerSelf.senTypeData = {
                    sendType: type,
                    meldList: meldList,
                    actionNum: actionNum
                };
                //显示过
                let actions = {
                    "action": 0,
                    "tiles": [""]
                }
                let msgdata = {
                    "actions": actions,
                    'num': actionNum
                }
                this.onShowActionOption(msgdata);
                // this.operatorArea.hide();
                return;
            }
            var sendType = type;
            if (sendType == ACTION_OPTION.SELF_KONG)
                sendType = tileId2Action[meldList];
            //过
            if (this.isClickTing && sendType != ACTION_OPTION.TING) {
                this.playerSelf.resetcardcolor();
                this.isClickTing = false;
            }


            NetHandlerMgr.netHandler.sendAction(sendType, meldList, actionNum);

            this.operatorArea.hide();

            if (this.lastDrawPlayer == this.playerSelf)
                this.updatePlayerTurn(MahjongMgr.inst.getServerPos(0));

            //自动打牌相关
            // if (type == 0){
            //     this.operatorArea.cancelAutoDiscard();
            // }
        };
    }

    tingClick(CardcolorList, handCardIds) {
        let ReadyHandFancyMap = {};
        for (let value of CardcolorList) {
            if (ReadyHandFancyMap[value] == null) {
                let tingList = this.huAl.getReadyHandTiles(value, handCardIds);
                if (tingList != null && tingList.length > 0) {
                    ReadyHandFancyMap[value] = tingList;
                }
            }
        }
        this.getPlayer(0).ReadyHandFancyEvt = (value: string, state: boolean) => {
            if (state == true) {
                if (ReadyHandFancyMap[value] != null) {
                    this.showtingpanel(ReadyHandFancyMap[value]);
                }
                else {
                    this.tingpanel.visible = false;
                    this.tingBtn.visible = false;
                }
            }
        };
    }
}