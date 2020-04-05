module SetBalanceStyle {
    export let NORMAL = 0;
    export let HORSE = 1;
    export let HORSE_WIN = 2;
    export let BLOOD = 3;
}

class SetBalance {
    private layer: fairygui.GComponent;
    private cBalance: fairygui.GComponent;
    private itemList = [];
    private playercountctl: fairygui.Controller;
    private t_itemList = [];

    constructor(layer: fairygui.GComponent) {
        this.layer = layer;
        //layer.visible=false;

        var cBalance = layer.getChild('cBalance').asCom;
        this.cBalance = cBalance;
        this.playercountctl = cBalance.getController('playercount');
        var btnClose = cBalance.getChild('btnClose');
        btnClose.onClick(this, function () {
            layer.visible = false;
            if (this.closeCB) this.closeCB();
        }.bind(this));
        for (let j = 0; j < 2; j++) {
            this.t_itemList.push(cBalance.getChild('Item' + j));
        }
        for (var i = 0; i < 4; i++) {
            this.itemList.push(cBalance.getChild("cItem" + i));
        }

        this.setStyle(0);

        var btnReady = cBalance.getChild('btnReady');
        btnReady.onClick(this, function () {
            layer.visible = false;
            // NetHandlerMgr.netHandler.sendReadyGame();
            if (this.closeCB2) this.closeCB2();
        }.bind(this));
    }

    private closeCB: Function = null;
    setCloseCallback(cb = null) {
        this.closeCB = cb;
    }

    private closeCB2: Function = null;
    setCloseCallback2(cb = null) {
        this.closeCB2 = cb;
    }

    setStyle(style) {
        var styleCtl = this.cBalance.getControllerAt(0);
        styleCtl.setSelectedIndex(style);
    }

    private horseTile = '';
    showData(data, style = 0, playercount = 4, roomNumStr = '') {

        var dataList = data;
        var length = dataList.length;
        this.horseTile = '';
        if (playercount == 4) {
            this.playercountctl.selectedIndex = 0;
            for (var i = 0; i < 4; i++) {
                this.itemList[i].visible = false;
            }
            for (var i = 0; i < length; i++) {
                var itemData = dataList[i];
                var item = this.itemList[i];
                this.setItem(itemData, item, style, i);
            }
        }
        else if (playercount == 2) {
            this.playercountctl.selectedIndex = 1;
            for (let i = 0; i < 2; i++) {
                this.t_itemList[i].visible = false;
            }
            //console.log(dataList, "===========结算数据");
            for (let i = 0; i < length; i++) {
                let itemData = dataList[i];
                let item = this.t_itemList[i];
                this.setItem(itemData, item, style, i, playercount)

            }
        }
        this.cBalance.getChild('room_nuber').text = roomNumStr;
        if (this.horseTile != "") {
            var outList = this.cBalance.getChild("horseTile");
            this.addTiles(this.horseTile.split(","), outList);
        }

        this.layer.visible = true;
    }

    setItem(itemData, item, style, side, playercount = 4) {

        //昵称显示
        var nickname = itemData["nickname"];
        var tfName = item.getChild("tfName").asLabel;
        // tfName.text = nickname.substring(0,6);
        tfName.text = nickname;
        // if (side == 0)
        //     Tools.inst.setNickname(tfName, nickname);
        // else
        //     Tools.inst.setNickname(tfName, Tools.inst.abbreviateNickname(nickname));

        //得分显示
        var score = parseFloat(itemData["score"]);
        var tfScore1 = item.getChild("tfScore1").asLabel;
        var tfScore2 = item.getChild("tfScore2").asLabel;
        var scoreStr = Tools.inst.changeGoldToMoney(score);
        tfScore1.text = tfScore2.text = (score > 0 ? '+' + scoreStr : scoreStr);
        var horseTiles = '', flowerTiles = '', wallTiles = '';
        var tileList = Tools.inst.cloneObject(itemData["tiles"]);
        //判断是否显示庄家标识
        var isDealer = itemData["isDealer"];
        var imgBanker = item.getChild("imgBanker");
        imgBanker.visible = isDealer;

        //判断是否显示胡牌标识
        var isHu = itemData["isHu"];
        // var imgHued = item.getChild("imgHued");
        // imgHued.visible = isHu;
        var styleCtl = item.getControllerAt(0);
        styleCtl.setSelectedIndex(isHu ? 1 : 0);
        //玩家本局信息
        if (playercount == 4) {
            var descs = itemData["descs"];
            var tfHued = item.getChild("tfHued").asLabel;
            //  tfHued.text = (descs + " ");
            let text = "";
            for (let i = 0; i < descs.length; i++) {
                let txt = descs[i];
                txt = txt.split('*');
                if (text == "") {
                    if (txt.length > 1)
                        text = ExtendMgr.inst.getText4Language(txt[0]) + "*" + txt[1];
                    else {
                        txt = txt[0].split('X');
                        if (txt.length > 1) {
                            text = ExtendMgr.inst.getText4Language(txt[0].replace(/\s/g, "")) + "X" + txt[1].replace(/\s/g, "");
                        }
                        else
                            text = ExtendMgr.inst.getText4Language(txt[0]);
                    }

                }
                else {
                    if (txt.length > 1)
                        text = text + "  " + ExtendMgr.inst.getText4Language(txt[0]) + "*" + txt[1];
                    else {
                        txt = txt[0].split('X');
                        if (txt.length > 1) {
                            txt
                            text = text + "  " + ExtendMgr.inst.getText4Language(txt[0].replace(/\s/g, "")) + "X" + txt[1].replace(/\s/g, "");
                        }
                        else
                            text = text + " " + ExtendMgr.inst.getText4Language(txt[0]);
                    }

                }

            }
            tfHued.text = text;
            switch (style) {
                case SetBalanceStyle.HORSE_WIN:
                    horseTiles = tileList.pop();
                    var winHorseTiles = tileList.pop();
                    flowerTiles = tileList.pop();
                    wallTiles = tileList.pop();
                    break;
                case SetBalanceStyle.BLOOD:
                    tileList.pop();
                    wallTiles = tileList.pop();
                    break;
                case SetBalanceStyle.HORSE:
                default:
                    horseTiles = tileList.pop();
                    flowerTiles = tileList.pop();
                    wallTiles = tileList.pop() || '';
                    break;
            }
        }
        else if (playercount == 2) {
            var descs = itemData["descs"];
            var tfHued = item.getChild("tfHued").asLabel;
            tfHued.text = "";
            let ttype = item.getChild('ttype');
            let text = "";
            for (let i = 0; i < descs.length; i++) {
                let txt = descs[i];
                txt = txt.split('+');
                if (text == "") {
                    text = ExtendMgr.inst.getText4Language(txt[0]) + '+' + txt[1];
                }
                else {
                    text = text + "  " + ExtendMgr.inst.getText4Language(txt[0]) + '+' + txt[1];
                }

            }
            ttype.text = text;

            flowerTiles = tileList.pop();
            wallTiles = tileList.pop() || '';
            // horseTiles = tileList.pop();
        }
        if (horseTiles != "") {
            this.horseTile = horseTiles;
        }



        var outList = item.getChild("out_tiles");
        //  wallTileslist.sort(G445PlayerFrame.sortTileData)
        this.addTiles(wallTiles.split(','), outList);

        var meldtiles = item.getChild("tileList");
        this.addMeldTiles(tileList, meldtiles);

        outList.x = meldtiles.x + 160 * tileList.length;

        item.visible = true;
    }

    private addTiles(tiles, outList) {
        // console.log(tiles, "============tiles");
        outList.removeChildrenToPool();
        for (let i = 0; i < tiles.length; ++i) {
            var value = tiles[i];
            //if(!value)continue;
            var tileComp = outList.addItemFromPool().asCom;
            MahjongMgr.inst.setWholeTile(tileComp, value);
        }
    }

    public addMeldTiles(dataList, outList) {
        outList.removeChildrenToPool();
        for (let n = 0; n < dataList.length; n++) {
            var meldComp = outList.addItemFromPool().asCom;
            var tilesStr = dataList[n].split(';')[1] || '';
            var tiles = tilesStr.split(',') || [];
            tiles = tiles.sort(G445PlayerFrame.sortTileData);
            var tile4 = meldComp.getChildAt(3).asCom;
            tile4.visible = tiles.length > 3;
            for (let i = 0; i < tiles.length; ++i) {
                var value = tiles[i];
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
            }
        }
    }
}