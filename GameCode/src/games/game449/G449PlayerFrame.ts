class G449PlayerFrame extends G445PlayerFrame {
    constructor(components: Object) {
        super(components);
        this.baoting_url = [];
    }
    private baoting_url: Array<string>;
    //摊牌
    public setOtherBaotingshow(tileData) {
        if (this.side == 0)
            return;
        this.isTingAction = true;
        let itemCard;
        this.baoting_url[0] = null
        if (this.side == 1) {
            itemCard = fairygui.UIPackage.getItemURL('MJ', 'out1');
            this.baoting_url[1] = itemCard;
        }
        else if (this.side == 2) {
            itemCard = fairygui.UIPackage.getItemURL('MJ', 'otherout');
            this.baoting_url[2] = itemCard;
        }
        else if (this.side == 3) {
            itemCard = fairygui.UIPackage.getItemURL('MJ', 'out3');
            this.baoting_url[3] = itemCard;
        }
       // console.log(this.side, itemCard, "=============itemCard");
        // this.hand_tiles.removeChildrenToPool();
        this.addHandTiles(tileData, true);
        //  this.hand_tiles.defaultItem=
    }
    public drawHandTile(tiles) {
        //console.log(tiles, this.side, "=========摸牌位置");
        this.addHandTiles(tiles, false, false, false, 0, true);
        this.separateLastTile();
    }
    public addHandTiles(tiles, clear: boolean = false, isselfmobile: boolean = false, isrefresh = false, actionnum: number = 0, isdrawtile = false) {
        //  console.log(itemCard, "===========itemCard");
        if (this.isTingAction && this.side != 0) {
            this.hand_tiles.defaultItem = this.baoting_url[this.side];
            //console.log(tiles, "=======addHandTiles========");
        }
        else
            this.hand_tiles.defaultItem = this.hand_tiles_url;
        var outList = this.hand_tiles;
        tiles.sort(G445PlayerFrame.sortTileData);

        if (clear) {
            this.tilesDataHand = tiles;
        } else {
            this.tilesDataHand = this.tilesDataHand.concat(tiles);
        }

        this.setTiles(tiles, outList, clear, true, isdrawtile);
        this.refreshHandPos(isselfmobile, isrefresh, actionnum);
    }
    public setTiles(tiles, outList, clear: boolean = false, ishandtile = false, isdrawtile = false) {
        if (clear) outList.removeChildrenToPool();
        if (this.isTingAction && this.side != 0 && ishandtile && tiles.length > 0 && isdrawtile) {
            this.otherplayeraddTiles(tiles, outList);
        }
        else
            this.addTiles(tiles, outList, clear);
    }
    public addTiles(tiles, outList, clear: boolean = false) {
        for (let i = 0; i < tiles.length; ++i) {
            var value = tiles[i];
            //if(!value)continue;
            // console.log(outList.defaultItem, "=========defaultItem");
            var tileComp = outList.addItemFromPool().asCom;
            if (this.side != 0 && this.isTingAction && clear) {
                // console.log(tiles, "==========addTiles======")
                tileComp.getController('separate').selectedIndex = 0;
            }
            else
                tileComp.x = 0;
            this.setTileIcon(tileComp, value);
        }
    }
    public otherplayeraddTiles(tiles, outList) {

        let list = this.tilesDataHand.concat();
        list.sort(G445PlayerFrame.sortTileData);
        let index = list.indexOf(tiles[0]);
        if (index != -1) {
            list.splice(index, 1);
        }
        list.unshift(...tiles);
        // console.log(tiles, list, "=========手牌");
        for (let i = 0; i < list.length; i++) {
            var value = list[i];
            if (!value)
                continue;
            if (i > outList.numChildren - 1) {
                var tileComp = outList.addItemFromPool().asCom;
                tileComp.x = 0;
            }
            else {
                var tileComp = outList.getChildAt(i).asCom;
            }
            this.setTileIcon(tileComp, value);

        }
        //     for (let i = 0; i < tiles.length; ++i)
        //         var value = tiles[i];
        //     //if(!value)continue;
        //     // console.log(outList.defaultItem, "=========defaultItem");
        //     var tileComp = outList.addItemFromPool().asCom;
        //     tileComp.x = 0;
        //     this.setTileIcon(tileComp, value);
    }

    // public separateLastTile() {
    //     var outList = this.hand_tiles;
    //     var length = outList.numChildren;
    //     if (length == 0) return;
    //     var index = 0;
    //     if (this.side == 2 && this.isTingAction) {
    //         index = length - 1;
    //     }
    //     else {
    //         index = 0;
    //         if (this.side == 0 || this.side == 3) index = length - 1;
    //     }
    //     let tileComp = outList.getChildAt(index).asCom;
    //     this.separateTile(tileComp, true);
    // }

    public hu(data, cb, isbaoting = false) {
        var tiles = data["list"];
        if (isbaoting == false)
            this.layHandTile(1, tiles);
        this.setActionEffect(data['passivePlayer'] ? 3 : 4);

        if (data['passivePlayer']) SoundMgr.hu(this.sex);
        else SoundMgr.hu_origin(this.sex);
        SoundMgr.layTiles();

        Tools.inst.setTimeout(function () {
            if (cb) cb();
        }, 100)
    }

    public setCardcolor(index) {
        this.isBaoTing = true;
        let card = this.hand_tiles.getChildAt(index).asCom;
        card.getController('color').selectedIndex = 1;
        card.touchable = true;
    }
    public resetcardcolor() {
        if (this.side == 0) {
            this.isBaoTing = false;
            for (let i = 0; i < this.hand_tiles.numChildren; i++) {
                let card = this.hand_tiles.getChildAt(i).asCom;
                card.getController('color').selectedIndex = 0;
                card.touchable = true;
            }
        }
    }
}