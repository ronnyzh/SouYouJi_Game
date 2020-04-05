/*
* name;
*/
class G564Page extends G445Page {

    newPlayerFrame(data) {
        return new G564PlayerFrame(data);
    }
    public gameID = 564;

    initMsgListen() {
        super.initMsgListen();

        NetHandlerMgr.netHandler.addSequenceMsgListener(G564.S_C_EXCHANGE_FLAG, this.onExchangeFlag.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(G564.S_C_EXCHANGE_THREE, this.onExchangeThree.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(G564.S_C_PLAYER_EXCHANGE_THREE, this.onPlayerExchange3.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(G564.S_C_PLAYER_SET_COLOR, this.onPlayerSetColor.bind(this));
        NetHandlerMgr.netHandler.addSequenceMsgListener(G564.S_C_SET_COLOR, this.onSetColors.bind(this));

        NetHandlerMgr.netHandler.addMsgListener(G564.S_C_EXTRA_MESSAGE, this.onExtraMessage.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(G564.S_C_REFRESH_SCORE, this.onRealTimeCount.bind(this));
        NetHandlerMgr.netHandler.addMsgListener(G564.S_C_HUTILES, this.onShowHuTiles.bind(this));
    }

    pageStyleSetting(data) {
        var view = this._view;

        var txtTitle = view.getChild('txtTitle').asLabel;
        txtTitle.text = ExtendMgr.inst.getText4Language("血流成河");

        var ghost = this._view.getChild('ghost').asCom;
        ghost.visible = false;

        /*** 暂时开放 ***
        var GM = this._view.getChild('GM').asCom;
        GM.visible = true;
        /*******************/

        var changeList = view.getChild('changeList').asList;
        var btnChange3 = view.getChild('btnChange3').asButton;
        btnChange3.onClick(this, function () {
            var changeThrees = this.getPlayer(0).checkChoosed();
            // this.refreshChangeThree(changeThrees);
        }.bind(this));

        var types = ['a', 'b', 'c'];
        for (var i = 0; i < 3; i++) {
            var btn = view.getChild('color' + i).asButton;
            btn.onClick(this, function (type) {
                NetHandlerMgr.netHandler.sendColor(type);
                this.gameStateCtl.setSelectedIndex(7);
            }.bind(this, types[i]));
        }
    }

    firstState() {
        this.gameStateCtl.setSelectedIndex(5);
    }

    showBalance(setData) {
        this.setBalance.showData(setData, SetBalanceStyle.BLOOD);
    }

    onExchangeFlag(msgData, finishedListener = null) {
        //console.log('onExchangeFlag',msgData)
        try {
            this.refreshChangeThree([]);
        } catch (error) {
            console.log(error)
        }
        if (finishedListener) finishedListener();
    }

    onExchangeThree(msgData, finishedListener) {
        //console.log(msgData)
        try {
            var datas = msgData["data"];
            for (var h = 0; h < datas.length; h++) {
                var data = datas[h];
                var localSide = this.getLocalPos(data["side"]);
                var changeTiles = data["tile"];
                var oldChangeTiles = data["temp_tile"];
                this.getPlayer(localSide).add3HandTiles(changeTiles);
            }
        } catch (error) {
            console.log(error)
        }
        this.gameStateCtl.setSelectedIndex(6);

        if (finishedListener) finishedListener();
    }

    // 重连之后的数据
    onExtraMessage(msgData) {
        //console.log(msgData)
        switch (msgData["status"]) {
            case 1://换三张
                this.refreshChangeThree(msgData["changingTiles"]);
                break;
            case 2://定缺
                this.gameStateCtl.setSelectedIndex(6);
                if (msgData["selfColor"]) {
                    this.gameStateCtl.setSelectedIndex(7);
                    this.getPlayer(0).setIgnoreColor(msgData["selfColor"]);
                }
                break;
            case 3://普通            
                var colors = msgData['color'];
                for (var i = 0; i < colors.length; i++) {
                    this.getPlayer(i, true).setIgnoreColor(colors[i]);
                }
            default:
                this.inGameState();
                break;
        }
        var huPlayer = msgData['huPlayer'];
        for (var i = 0; i < huPlayer.length; i++) {
            var localSide = this.getLocalPos(huPlayer[i]['side']);
            if (localSide == 0) {
                this.getPlayer(localSide).LockTile(true);
                // this.sendOnProxy(true);
            }
        }
    }

    sendOnProxy(on = false) {
        if (!on && this.getPlayer(0).isHuState) {
            Alert.show(ExtendMgr.inst.getText4Language("胡了之后手牌不才允许操作")); return;
        }
        super.sendOnProxy(on);
    }

    inGameState() {
        this.gameStateCtl.setSelectedIndex(0);
        this.getPlayer(0).setChangeTileState(false, false);
    }

    refreshChangeThree(list = []) {
        var view = this._view;
        var btnChange3 = view.getChild('btnChange3').asButton;
        btnChange3.visible = (list.length == 0);

        var changeList = view.getChild('changeList').asList;
        MahjongMgr.inst.addTiles(list, changeList);
        this.getPlayer(0).setChangeTileState(true, list.length > 0);

        this.gameStateCtl.setSelectedIndex(5);
    }

    onSetColors(msgData, finishedListener) {
        //console.log(msgData)
        var colors = msgData['color'];
        for (var i = 0; i < colors.length; i++) {
            this.getPlayer(i, true).setIgnoreColor(colors[i]);
        }
        this.inGameState();
        if (finishedListener) finishedListener();
    }

    // 实时算分
    onRealTimeCount(msgData) {
        //console.log(msgData)
        var scoreList = msgData["data"];
        for (var i = 0; i < scoreList.length; i++) {
            var oneData = scoreList[i];
            var side = this.getLocalPos(oneData["side"]);
            var player = this.getPlayer(side);
            player.setScore(oneData["change"], oneData["score"]);
        }
    }

    onPlayerExchange3(msgData, finishedListener) {
        console.log(msgData)
        if (!msgData['result']) {
            Alert.show(ExtendMgr.inst.getText4Language(msgData['reason']) || 'Error');
            if (finishedListener) finishedListener();
            return;
        }
        var side = this.getLocalPos(msgData['side']);
        if (side == 0) {
            this.refreshChangeThree(msgData['tile']);
            this.getPlayer(side).finishChoosed(msgData);
        }
        Tools.inst.setTimeout(function () {
            if (finishedListener) finishedListener();
        }, 500)
    }

    onPlayerSetColor(msgData, finishedListener) {
        console.log(msgData)
        if (!msgData['result']) {
            Alert.show(ExtendMgr.inst.getText4Language(msgData['reason']) || 'Error');
            if (finishedListener) finishedListener();
            return;
        }
        var side = this.getLocalPos(msgData['side']);
        this.getPlayer(side).setIgnoreColor(msgData['color']);
        if (side == 0) {
            this.gameStateCtl.setSelectedIndex(7);
        }
        if (finishedListener) finishedListener();
    }

    onShowHuTiles(msgData) {
        //console.log('onShowHuTiles',msgData)
        var playerData = msgData['HuData'] || [];
        for (var n = 0; n < playerData.length; n++) {
            var tiles = playerData[n]['HuTile'] || [];
            if (tiles.length > 0) {
                this.getPlayer(playerData[n]['side'], true).setHuState(tiles, true);
            }
        }
    }

    onGameEnd(msgData, finishedListener) {
        //console.log(msgData)
        var setData = msgData["setUserDatas"];
        if (setData != null && setData.length > 0) {
            //然后在玩家头像那里计算分数
            /*for(var n = 0; n < setData.length; n ++)
            {
                var oneSetData = setData[n];
                var setDataSide = this.getLocalPos(oneSetData["side"]);
                var player = this.getPlayer(setDataSide);
                player.balanceScore(oneSetData["score"]);
            }*/
        }

        this.resetInEnd();
        SoundMgr.win();

        this.gameStateCtl.setSelectedIndex(3);//msgData["isDrawn"] ? 2 :3
        Tools.inst.setTimeout(function () {
            this.showBalance(setData);
            this.gameStateCtl.setSelectedIndex(4);
        }.bind(this), 1000);

        if (finishedListener) finishedListener();
    }

    onPlayerHu(data, cb) {

        var huPlayer = data["getPlayer"];
        var huTiles = data["list"];
        var passivePlayer = data["passivePlayer"];
        var removeTileID = data["tileData"];

        if (passivePlayer != null) {
            passivePlayer.removeOutTile(removeTileID);
        } else {
            huPlayer.removeHandTiles([removeTileID])
        }
        huPlayer.hu(data, cb);
    }

    onKeyDown(e: Event): void {
        if (TestMgr.IS_REAL_ACCOUNT) return;
        var keyCode: number = e["keyCode"];
        var Keyboard = Laya.Keyboard;
        switch (keyCode) {
            case Keyboard.NUMBER_1:
                NetHandlerMgr.netHandler.gameManage("2:b1b1b2b2b1b2b4b4b4b5b5b4b1", this.onGMResult.bind(this));
                return;
            case Keyboard.NUMBER_2:
                NetHandlerMgr.netHandler.gameManage("1:a2", this.onGMResult.bind(this));
                return;
            case Keyboard.G:
                var txtGM = this.view.getChild('GM').asLabel;
                if (txtGM.text.length) NetHandlerMgr.netHandler.gameManage(txtGM.text, this.onGMResult.bind(this));
                break;
            default:
                console.log(keyCode)
                return;
        }
    }
}