/*
* name;
*/
class G445PlayerFrame {

    public side: number;
    private seat: fairygui.GComponent;
    private nameText: fairygui.GLabel;
    private scoreText: fairygui.GLabel;
    private score: number;
    public sex: number;
    private imgHead: fairygui.GLoader;
    private dealerCtl: fairygui.Controller;
    private scoreCtl: fairygui.Controller;
    public OnGoldCtl: fairygui.Controller;
    // private scoreBalanceText:fairygui.GLabel;
    private scoreBalanceText1: fairygui.GLabel;
    private scoreBalanceText2: fairygui.GLabel;

    public out_tiles: fairygui.GList;
    public hand_tiles: fairygui.GList;
    public meld_tiles: fairygui.GList;
    public hu_tiles: fairygui.GList;
    public actions: fairygui.GComponent;
    private actionsCrl: fairygui.Controller;
    public out_pin: fairygui.GComponent;
    private okMark: fairygui.GComponent;
    protected hand_tiles_url: string;
    public senTypeData: {
        sendType: any,
        meldList: any,
        actionNum: number
    };
    protected isTingAction: boolean;//收到听牌的消息
    protected isBaoTing: boolean;//点击听，手牌变黄

    //当前玩家所出的牌
    private selfoutcard: fairygui.GComponent;
    public outListX = 0;

    /**点击牌时的预听牌事件*/
    public ReadyHandFancyEvt = null;
    /**上浮的牌 */
    public pitchUpCard: fairygui.GComponent = null;


    constructor(components: Object) {
        this.side = components['side'];
        var component = components['seat'];
        this.seat = component;
        this.nameText = component.getChild('name').asLabel;
        this.scoreText = component.getChild('score').asLabel;
        this.imgHead = component.getChild('icon').asLoader;
        this.dealerCtl = component.getController('c1');
        this.scoreCtl = component.getController('balance');
        this.OnGoldCtl = component.getController('Nocold');
        this.OnGoldCtl.selectedIndex = 0;
        // this.scoreBalanceText = component.getChild('scoreBalance').asLabel;
        this.scoreBalanceText1 = component.getChild('scoreBalance1').asLabel;
        this.scoreBalanceText2 = component.getChild('scoreBalance2').asLabel;

        this.out_tiles = components['out_tiles'];
        this.out_pin = components['pin'];
        this.hand_tiles = components['hand_tiles'];
        this.meld_tiles = components['meld_tiles'];
        this.hu_tiles = components['hu_tiles'];
        this.actions = components['actions'];
        this.actionsCrl = this.actions.getControllerAt(0);

        this.okMark = components['okMark'];
        this.hand_tiles_url = components['hand_tiles_url'];

        this.outListX = this.hand_tiles.x;
        this.hand_tiles.defaultItem = this.hand_tiles_url;
        this.isTingAction = false;
        this.isBaoTing = false;
        this.selfoutcard = null;

    }

    setSeat(data) {
        if (!data) return;
        // this.nameText.visible=false;
        // this.nameText.text = data['nickname'].substring(0,6);
        // this.nameText.text = 'ID:'+data["id"];
        if (this.side != 0)
            this.nameText.text = Tools.inst.maskUserName(data['nickname']);
        else
            // Tools.inst.setNickname(this.nameText, data['nickname']);
            Tools.inst.SetNickNameAfter(this.nameText, data['nickname']);
        this.sex = parseInt(data['sex'] || 0);
        this.score = parseFloat(data['coin']);//*0.01
        this.setScoreText();

        this.imgHead.url = 'ui://la8oslyoosvmbg';
        var headImgUrl = data['headImgUrl'];
        try {
            if (headImgUrl)
                Tools.inst.changeHeadIcon(headImgUrl, this.imgHead);
            else if (this.side == 0)
                Tools.inst.changeHeadIcon(UserMgr.inst.imgUrl, this.imgHead);
        } catch (error) {
            console.log(error)
        }
        this.seat.visible = true;
    }


    setScoreText() {
        // this.scoreText.text = jx.goldFormat(this.score);
        this.scoreText.text = Tools.inst.changeGoldToMoney(this.score, '');
    }

    setOkMark(show = false) {
        // this.okMark.visible=show;
    }

    updateBankerState(dealer) {
        this.dealerCtl.setSelectedIndex(dealer ? 1 : 0);
    }

    balanceScore(num) {
        num = parseFloat(num);
        this.score += (num);
        this.setScore(num, this.score);
    }

    setScore(num, score) {
        this.score = parseFloat(score);
        this.setScoreText();

        num = parseFloat(num);
        //var scoreStr = Tools.inst.changeGoldToMoney(num);
        // this.scoreBalanceText.text = (num<0 ? scoreStr : '+'+scoreStr);

        var scoreStr = Tools.inst.changeGoldToMoney(num);
        this.scoreBalanceText1.text = (num < 0 ? "" : '+' + scoreStr);
        this.scoreBalanceText2.text = (num < 0 ? '' + scoreStr : '');

        this.scoreCtl.setSelectedIndex(num < 0 ? 2 : 1);
        Tools.inst.setTimeout(function () {
            try {
                // this.scoreBalanceText.text='';
                this.scoreCtl.setSelectedIndex(0);
                this.clearScore();
            } catch (error) {
                console.log(error)
            }
        }.bind(this), 1000);
    }

    clearScore() {
        this.scoreBalanceText1.text = '';
        this.scoreBalanceText2.text = '';
        this.scoreCtl.setSelectedIndex(0);
    }

    setScoreString(score) {
        this.score = parseFloat(score);
        this.setScoreText();
    }

    clear() {
        this.ReadyHandFancyEvt = null;
        this.setOkMark(false);
        this.seat.visible = false;
        this.clearScore();
    }

    resetGame() {
        this.layHandTile(0);

        this.hand_tiles.removeChildrenToPool();
        this.out_tiles.removeChildrenToPool();
        this.meld_tiles.removeChildrenToPool();
        this.hu_tiles.removeChildrenToPool();

        this.hand_tiles.x = this.outListX;

        this.tilesDataHand = [];
        this.tilesDataOut = [];
        this.tilesDataMeld = {};
        this.senTypeData = null;
        this.tileschipenggang = [];

        this.updateBankerState(false);
        this.setOkMark(false);

        this.actions.visible = false;
        this.out_pin.visible = false;
        this.isTingAction = false;
        this.OnGoldCtl.selectedIndex = 0;

    }

    public setTileIcon(tileComp, value) {
        var icon = tileComp.getChild('icon');
        if (icon) {
            var id = value;
            if ((typeof value == 'object') && value.getId)
                id = value.getId();
            if (typeof id == 'string')
                MahjongMgr.inst.setWholeTile(tileComp, id);

            var c = tileComp.getController('button');
            if (c && this.side == 0) {
                tileComp.x = 0; tileComp.y = 0;
                tileComp.data = value;
                this.playDragDrop(tileComp, value);
            }
        }
    }

    public addTiles(tiles, outList) {
        for (let i = 0; i < tiles.length; ++i) {
            var value = tiles[i];
            //if(!value)continue;
            // console.log(outList.defaultItem, "=========defaultItem");
            var tileComp = outList.addItemFromPool().asCom;
            tileComp.x = 0;
            this.setTileIcon(tileComp, value);
        }
    }

    removeChoosed(separate = false) {
        var outList = this.hand_tiles;
        for (var i = 0; i < outList.numChildren; ++i) {
            let tileComp = outList.getChildAt(i).asCom;

            if (this.side == 0) {
                tileComp.stopDrag();
                tileComp.y = 0;
                //重置位置和缩放
                if (separate) {
                    tileComp.getTransition('Ani').stop();
                    for (let i = 0; i < tileComp.numChildren; i++) {
                        tileComp.getChildAt(i).scaleX = 1;
                        tileComp.getChildAt(i).scaleY = 1;
                    }
                    tileComp.getChild("bg").x = 0;
                    tileComp.getChild("bg").y = 0;
                }

            }

            if (separate) {
                //console.log(tileComp.data, "========removeChoosed")
                this.separateTile(tileComp);
            }

        }
    }

    private lastTouchX = 0;
    private touchTile(tileComp: fairygui.GComponent, value) {
        this.lastTouchX = tileComp.x;
        //console.log('touchTile',value,this.lastTouchX)
    }

    public playDragDrop(tileComp: fairygui.GComponent, value): void {
        // console.log(MahjongMgr.inst.isMyTurn(), "===========playDragDrop");
        try {
            //  tileComp.draggable = MahjongMgr.inst.isMyTurn();
            var btn = tileComp.asButton;
            btn.off(fairygui.Events.DRAG_END, this, this.__onDrop);
            btn.on(fairygui.Events.DRAG_END, this, this.__onDrop, [tileComp, value]);

            btn.off(Laya.Event.MOUSE_DOWN, this, this.onPokerClicked);
            btn.on(Laya.Event.MOUSE_DOWN, this, this.onPokerClicked, [tileComp, value]);
        } catch (error) {
            console.log(error)
        }
    }
    private __onDrop(tileComp, value): void {
        //console.log('send tile :'+value)

        try {
            var c = tileComp.getController('button');
            if (!c) {
                return;
            }
            // if (tileComp.getController('color').selectedIndex == 0 && this.isBaoTing)
            //     return;
            tileComp.stopDrag();
            if (MahjongMgr.inst.isMyTurn() && tileComp.y < -150) {
                this.selfoutcard = tileComp;
                this.sendDiscardCheck(value);
            }
            tileComp.x = this.lastTouchX;
            this.removeChoosed()

            this.pitchUpCard = null;
        } catch (error) {
            console.log(error)
        }
    }

    public tileOffsetY = -30;
    onPokerClicked(pokerComp: fairygui.GComponent) {
        if (!pokerComp) return;
        try {
            var value = pokerComp.data;
            var c = pokerComp.getController('button');
            if (!c) return;
            // if (pokerComp.getController('color').selectedIndex == 0 && this.isBaoTing)
            //     return;

            this.lastTouchX = pokerComp.x;
            if (pokerComp.y == this.tileOffsetY) {
                pokerComp.stopDrag();
                pokerComp.y = 0;
                this.selfoutcard = pokerComp;
                this.sendDiscardCheck(value);

                if (this.ReadyHandFancyEvt != null) {
                    this.ReadyHandFancyEvt(value.toString(), false);
                }
                this.pitchUpCard = null;
                return;
            }
            this.removeChoosed();
            SoundMgr.clickcard();
            pokerComp.y = this.tileOffsetY;

            if (this.ReadyHandFancyEvt != null) {
                this.ReadyHandFancyEvt(value.toString(), true);
            }
            this.pitchUpCard = pokerComp;
        } catch (error) {
            console.log(error)
        }
    }

    isChoosed(tileComp) {
        return tileComp.y == this.tileOffsetY;
    }

    public sendDiscardCheck(value) {
        if (!MahjongMgr.inst.isMyTurn()) return;
        // console.log(this.senTypeData, "=========this.senTypeData");
        if (this.senTypeData != null) {
            NetHandlerMgr.netHandler.sendAction(this.senTypeData.sendType, this.senTypeData.meldList, this.senTypeData.actionNum);
        }

        NetHandlerMgr.netHandler.sendDiscard(value);

        this.resetcardcolor();
    }

    public setTiles(tiles, outList, clear: boolean = false) {
        if (clear) outList.removeChildrenToPool();
        this.addTiles(tiles, outList);
    }

    public static sortTileData(data1, data2, reversed = false) {
        var type1 = data1.charAt(0);
        var type2 = data2.charAt(0);
        var v1 = -1, v2 = 1; if (reversed) v1 = 1, v2 = -1;

        var ghostTileId = MahjongMgr.inst.ghostTileId();
        if (ghostTileId) {
            if (ghostTileId == data1) return v1;
            if (ghostTileId == data2) return v2;
        }

        if (type1 == type2) {
            if (type1 == "d") {
                var dvalue = { 1: 1, 5: 3, 9: 2 };
                return dvalue[data1.charAt(1)] < dvalue[data2.charAt(1)] ? v1 : v2;
            }
            return data1.charAt(1) < data2.charAt(1) ? v1 : v2;
        }
        return type1 < type2 ? v1 : v2;
    }
    public getHandcards() {
        return this.hand_tiles;
    }
    public setCardcolor(index) {
        let card = this.hand_tiles.getChildAt(index).asCom;
        card.getController('color').selectedIndex = 1;
        card.touchable = true;
    }
    public resetcardcolor() {
        if (this.side == 0) {
            for (let i = 0; i < this.hand_tiles.numChildren; i++) {
                let card = this.hand_tiles.getChildAt(i).asCom;
                card.getController('color').selectedIndex = 0;
                card.touchable = true;
            }
        }
    }
    public setselfNotDrag() {
        if (this.side == 0) {
            // console.log("不能拖拽");
            for (let i = 0; i < this.hand_tiles.numChildren; i++) {
                let card = this.hand_tiles.getChildAt(i).asCom;
                card.draggable = false;
            }
        }
    }
    public setselfDrag() {
        if (this.side == 0) {
            // console.log("可以拖拽");
            for (let i = 0; i < this.hand_tiles.numChildren; i++) {
                let card = this.hand_tiles.getChildAt(i).asCom;
                card.draggable = true;
            }
        }
    }
    public tilesDataHand: Array<string> = [];
    public addHandTiles(tiles, clear: boolean = false, isselfmobile: boolean = false, isrefresh = false, actionnum: number = 0) {
        var outList = this.hand_tiles;
        tiles.sort(G445PlayerFrame.sortTileData);
        if (clear) {
            this.tilesDataHand = tiles;
        } else {
            this.tilesDataHand = this.tilesDataHand.concat(tiles);
        }
        this.setTiles(tiles, outList, clear);
        this.refreshHandPos(isselfmobile, isrefresh, actionnum);
    }

    public drawHandTile(tiles) {
        //console.log(tiles, this.side, "=========摸牌位置");
        this.addHandTiles(tiles);
        this.separateLastTile();
    }
    public separateLastTile() {
        var outList = this.hand_tiles;
        var length = outList.numChildren;
        if (length == 0) return;
        var index = 0;
        if (this.side == 0 || this.side == 3) index = length - 1;
        let tileComp = outList.getChildAt(index).asCom;
        this.separateTile(tileComp, true);
    }

    public separateTile(tileComp, sp = false) {
        var c = tileComp.getController('separate');
        if (c) c.setSelectedIndex(sp ? 1 : 0);
        else {
            var tileBG = tileComp.getChild('bg');
            if (tileBG) tileBG.x = sp ? 50 : 0;
        }
    }

    public sortHandTiles() {
        this.tilesDataHand.sort(G445PlayerFrame.sortTileData);
        this.setTiles(this.tilesDataHand, this.hand_tiles, true);
        this.refreshHandPos();
    }

    public refreshHandPos(isselfmobile = false, isrefresh = false, actionnum: number = 0) {
        if (this.side > 0) return;
        var outList = this.hand_tiles;
        let meldList = this.meld_tiles;
        //  console.log(this.side, isselfmobile, "=============刷新手牌位置");
        // if (this.side == 2)
        //     outList.x = this.outListX - (outList.numChildren + meldList.numChildren) * outList._rawWidth;
        // else if (this.side == 1 || this.side == 4)
        //     outList.x = this.outListX - outList.numChildren * outList._rawWidth;
        if (this.side == 0 && isselfmobile) {
            if (isrefresh)
                outList.x = this.outListX + actionnum * 3 * outList._rawWidth * outList.scaleX;
            else {
                outList.x = this.outListX + meldList.numChildren * 3 * outList._rawWidth * outList.scaleX;
            }
        }
    }

    public removeHandTiles(list = [], isselfmobile = false) {
        // console.log(list, "=============要移除的手牌");
        var tiles = this.tilesDataHand;
        var outList = this.hand_tiles;
        var isShow = tiles[0];
        this.removeChoosed(true);
        // console.log(this.tilesDataHand, tiles, isShow, list, this.side, "=======出牌位置");
        Tools.inst.each(list, function (tileId) {
            if (isShow) {
                Tools.inst.removeElement(tiles, tileId);
            } else {
                tiles.pop();
                outList.removeChildAt(0);
            }
        }.bind(this));
        if (isShow) {
            tiles.sort(G445PlayerFrame.sortTileData)
            this.setTiles(tiles, outList, true);
        }
        this.refreshHandPos(isselfmobile);
    }

    public tilesDataOut: Array<string> = [];
    public getoutcardnum(id) {
        let num = 0;
        for (let i = 0; i < this.tilesDataOut.length; i++) {
            if (id == this.tilesDataOut[i])
                num++;
        }
        return num;
    }
    public getHandcardsId() {
        return this.tilesDataHand;
    }
    public gethandcardnum(id) {
        let num = 0;
        for (let i = 0; i < this.tilesDataHand.length; i++) {
            if (id == this.tilesDataHand[i])
                num++;
        }
        return num;
    }
    public addOutTiles(tiles, clear: boolean = false) {
        var outList = this.out_tiles;
        if (clear) {
            this.tilesDataOut = tiles;
        } else {
            this.tilesDataOut = this.tilesDataOut.concat(tiles);
        }
        this.setTiles(tiles, outList, clear);

        this.refreshOutPinPos();
    }

    public removeOutTile(tileID) {
        var outList = this.out_tiles;
        var tiles = this.tilesDataOut;
        if (tiles.length < 1) return;
        if (tileID && tiles[tiles.length - 1] == tileID) {
            outList.removeChildAt(tiles.length - 1);
            tiles.pop();
        }
        // console.log('removeOutTile :',tiles[tiles.length-1],tileID)
    }

    refreshOutPinPos() {
        var outList = this.out_tiles;
        var length = outList.numChildren;
        this.out_pin.visible = false;
        if (length < 1) return;
        var index = length - 1;
        // let tileComp = outList.getChildAt(index).asCom;   
        var columnCount = outList.columnCount;
        var row = Math.floor((length - 1) / columnCount)
        var rol = (length - 1) % columnCount;
        switch (this.side) {
            case 0:
                this.out_pin.setXY(outList.x + rol * 50 - 12, outList.y - row * 72);
                break;
            case 2:
                this.out_pin.setXY(outList.x - rol * 50 - 15, outList.y + row * 65 - 10);
                break;
            case 1:
                this.out_pin.setXY(outList.x - row * 65, outList.y - rol * 44 - 80);
                break;
            case 3:
                this.out_pin.setXY(outList.x + row * 65, outList.y + rol * 44 - 74);
                break;
            default:
                this.out_pin.setXY(outList.x - 12, outList.y);
                return;
        }
        this.out_pin.visible = true;
    }

    public tilesDataMeld = {};
    public tileschipenggang = [];
    public getTilesDataMeld(id) {
        let num = 0;
        for (let i = 0; i < this.tileschipenggang.length; i++) {
            if (this.tileschipenggang[i] == id)
                num++;
        }
        return num;
    }
    public addMeldTiles(dataList, clear: boolean = false, discolorid: string = '') {
        var outList = this.meld_tiles;
        if (clear) outList.removeChildrenToPool();
        for (let n = 0; n < dataList.length; n++) {
            var meldComp = outList.addItemFromPool().asCom;
            var tiles = dataList[n]['list'] || [];
            let tileData = dataList[n]['tileData'];
            // tiles = ['','',''];
            var tile4 = meldComp.getChildAt(3).asCom;
            tile4.visible = tiles.length > 3;
            for (let i = 0; i < tiles.length; ++i) {
                var value = tiles[i];
                if (value == "")
                    this.tileschipenggang.push(tileData)
                else
                    this.tileschipenggang.push(value);

                var tile = meldComp.getChildAt(i).asCom;
                var ctrl = tile.getControllerAt(0);
                if (!value && ctrl) {
                    ctrl.setSelectedIndex(1);
                    continue;
                }
                var icon = tile.getChild('icon');
                if (icon) {
                    MahjongMgr.inst.setWholeTile(tile, value);
                    if (ctrl) ctrl.setSelectedIndex(0);
                }
                //吃牌变黄
                let colorctl = tile.getController('color');
                if (colorctl) {
                    if (discolorid != '' && discolorid == value)
                        colorctl.selectedIndex = 1;
                    else
                        colorctl.selectedIndex = 0;
                }
            }
            var tileID = tiles[0];//dataList[n]['tileData'];
            this.tilesDataMeld[tileID] = tile4;
        }
    }

    public setContent(data) {
        var tiles = data["handTiles"];
        let melddata = data["meldData"];
        let chowdata = data['chowData']

        if (tiles) {
            //断线重连   手牌位置是否需要移动
            let isselfmobile = false;
            let actionNum = 0;
            if (this.side == 0 && ((melddata != null && melddata.length > 0) || (chowdata != null && chowdata.length > 0))) {
                isselfmobile = true;
                actionNum = melddata.length + chowdata.length;
            }
            this.addHandTiles(tiles, true, isselfmobile, true, actionNum);
        }
        var tiles = data["discardTiles"];
        if (tiles) {
            this.addOutTiles(tiles, true);
        }
        if (melddata)
            this.addMeldTiles(melddata);

        if (chowdata) {
            for (let i = 0; i < chowdata.length; i++) {
                let colorid = chowdata[i]['list'][2];
                this.addMeldTiles([chowdata[i]], false, colorid);
            }
        }

    }

    public discard(data) {
        var tiles = this.tilesDataHand;

        // console.log(data, "=======discard");
        if (this.side == 0) {
            //托管
            if (this.selfoutcard == null || this.isTingAction)
                this.selfoutcard = this.hand_tiles.getChildAt(this.hand_tiles.numChildren - 1).asCom;

            // console.log(this.selfoutcard, "===========this.selfoutcard");
            if (this.selfoutcard != null && this.selfoutcard.data == data) {
                let trans = this.selfoutcard.getTransition('Ani');
                let pos = this.getouttilescardpos(this.selfoutcard);
                trans.setValue('endpos', pos.x, pos.y);
                trans.play(Handler.create(this, function () {
                    for (let i = 0; i < this.selfoutcard.numChildren; i++) {
                        this.selfoutcard.getChildAt(i).scaleX = 1;
                        this.selfoutcard.getChildAt(i).scaleY = 1;
                    }
                    this.selfoutcard.getChild("bg").x = 0;
                    this.selfoutcard.getChild("bg").y = 0;
                    this.selfoutcard = null;
                    this.removeHandTiles([data]);
                    this.addOutTiles([data], false);
                    this.removeChoosed(true);
                }));
            }
            else {
                this.addOutTiles([data], false);

                this.removeHandTiles([data]);
            }
        }
        else {
            this.addOutTiles([data], false);

            this.removeHandTiles([data]);
        }
        SoundMgr.discardTile(data, this.sex);
    }
    private getouttilescardpos(card: fairygui.GComponent) {
        if (this.side != 0)
            return;
        let num = this.out_tiles.numChildren;
        let out_list_pos = this.out_tiles.localToGlobal(0, 0);
        let pos = card.getChild('bg').globalToLocal(out_list_pos.x, out_list_pos.y);
        let Children;
        if (num != 0) {
            Children = this.out_tiles.getChildAt(num - 1).asCom;
            pos.x += num % 10 * Children.actualWidth;
            pos.y -= Math.floor(num / 10) * Children.actualHeight;
        }
        //  let pos = { x, y };
        //console.log(pos, "=============位置");
        return pos;
    }

    public setActionEffect(index) {
        this.actionsCrl.setSelectedIndex(index);
        var eff = this.actions.getTransitionAt(0);
        eff.play();
        this.actions.visible = true;
        Tools.inst.setTimeout(function () {
            this.actions.visible = false;
        }.bind(this), 1000);

        this.out_pin.visible = false;
    }
    public SetNoGold() {
        this.actionsCrl.setSelectedIndex(5);
        var eff = this.actions.getTransitionAt(0);
        eff.play();
        this.actions.visible = true;
        Tools.inst.setTimeout(function () {
            this.actions.visible = false;
            this.OnGoldCtl.selectedIndex = 1;
        }.bind(this), 1000);

    }
    /**碰 */
    public pong(data, cb) {
        var tileData = data['tileData'];
        let isselfmobile = this.side == 0 ? true : false;

        this.addMeldTiles([data]);
        this.removeHandTiles([tileData, tileData], isselfmobile);
        this.setActionEffect(1);
        this.separateLastTile()
        SoundMgr.pong(this.sex);
        SoundMgr.li_pai();
        if (cb) cb();
    }
    /**吃 */
    public chow(data, cb) {
        var list = data["list"];
        let isselfmobile = this.side == 0 ? true : false;
        let deletelist = list.concat();
        let colorcardid = deletelist[2];
        list.sort(G445PlayerFrame.sortTileData);
        this.addMeldTiles([data], false, colorcardid);
        this.removeHandTiles([deletelist[0], deletelist[1]], isselfmobile);
        this.setActionEffect(0);
        this.separateLastTile()
        SoundMgr.chow(this.sex);
        SoundMgr.li_pai();
        if (cb) cb();
    }
    /**杠 */
    public kong(data, cb) {
        var tileData = data['tileData'];
        let isselfmobile = this.side == 0 ? true : false;
        this.addMeldTiles([data]);
        this.removeHandTiles([tileData, tileData, tileData], isselfmobile);
        this.setActionEffect(2);
        SoundMgr.kong(this.sex);
        SoundMgr.li_pai();
        if (cb) cb();
    }
    /**暗杠 */
    public concealedKong(data, cb) {
        var tileData = data['tileData'];
        var list = Tools.inst.cloneObject(data["list"]);
        for (var i = 0; i < list.length; i++) {
            list[i] = tileData;
        }
        let isselfmobile = this.side == 0 ? true : false;
        this.addMeldTiles([data]);
        this.removeHandTiles(list, isselfmobile);
        this.setActionEffect(2);
        SoundMgr.kong(this.sex);
        SoundMgr.li_pai();
        if (cb) cb();
    }
    /**补杠 */
    public addToKong(data, cb) {
        var tileData = data['tileData'];
        let isselfmobile = this.side == 0 ? true : false;
        this.removeHandTiles([tileData], isselfmobile);
        var tile = this.tilesDataMeld[tileData];
        if (tile) {
            var icon = tile.getChild('icon');
            if (icon) {
                MahjongMgr.inst.setWholeTile(tile, tileData);
                tile.visible = true;
            }
        }
        this.setActionEffect(2);
        SoundMgr.kong(this.sex);
        SoundMgr.li_pai();
        this.tileschipenggang.push(tileData);

        // console.log(this.tileschipenggang, "======addToKong");
        if (cb) cb();
    }
    /**胡 */
    public hu(data, cb) {
        var tiles = data["list"];
        this.layHandTile(1, tiles);
        this.setActionEffect(data['passivePlayer'] ? 3 : 4);

        if (data['passivePlayer']) SoundMgr.hu(this.sex);
        else SoundMgr.hu_origin(this.sex);
        SoundMgr.layTiles();

        Tools.inst.setTimeout(function () {
            if (cb) cb();
        }, 100)
    }

    public layHandTile(state, tiles = []) {
        var outList = this.hand_tiles;
        if (tiles.length) tiles.sort(G445PlayerFrame.sortTileData);
        for (var i = 0; i < outList.numChildren; ++i) {
            let tileComp = outList.getChildAt(i).asCom;
            var c1 = tileComp.getController('state');
            var c2 = tileComp.getController('lay');
            if (c1) c1.setSelectedIndex(state);
            else if (c2) {
                let outComp = tileComp.getChild('out').asCom;
                if (tiles[i] && outComp) {
                    this.setTileIcon(outComp, tiles[i]);
                }
                c2.setSelectedIndex(state);
            }
        }
    }
}