
module ProtoKeyMJ {
    export let C_S_ONPROXY = 0x00002007; // 玩家选择是否托管
    export let S_C_PROXY = 0x00002008; // 托管广播
    export let S_C_GOLDUPDATE = 0x00002004;    //更新金币数
}

module ProtoKeyMJG {
    export let C_S_ONPROXY = 0x0000A001; // 玩家选择是否托管
    export let C_S_DOREADYSTART = 0x0000A002;  //发送准备结果
    export let S_C_READY_GAMESTART = 0x0000B001;   //开始倒计时
    export let S_C_CANCEL_READY = 0x0000B002;  //取消倒计时
    export let S_C_GOLDUPDATE = 0x0000B003;    //更新金币数
    export let S_C_NOGOLD = 0x0000B004;    //发送破产协议
    export let S_C_GOLDPAYRESULT = 0x0000B005;     //发送支付结果协议(不启用)
    export let S_C_PROXY = 0x0000B006; // 托管广播
    export let S_C_PLAYERREADYRESULT = 0x0000B007; //广播玩家准备结果
    export let S_C_RUNHORSE = 0x00003001;
}

class TileData {
    private id;
    constructor(id) {
        this.id = id;
    }
    getId() {
        return this.id;
    }
    equals(data: TileData) {
        return this.getId() == data.getId();
    }
}

//各种游戏人数情况下的本地位置配置
var LOCAL_POS_LIST = {
    2: [0, 2],
    3: [0, 1, 3],
    4: [0, 1, 2, 3]
};

class MahjongMgr {
    private static _inst: MahjongMgr = null;
    public static get inst(): MahjongMgr {
        if (MahjongMgr._inst == null) {
            MahjongMgr._inst = new MahjongMgr();
        }
        return MahjongMgr._inst;
    }

    constructor() {
    }

    private static _tileCache = {};
    public static get tileCache() {
        return MahjongMgr._tileCache;
    }

    private getTilerUrl(value) {
        var url = '';
        if (value)
            url = UIMgr.getTileUrl('MJtiles', "lwgc_tile_" + value);
        else
            url = 'ui://ejgb8krjkteu5';
        return url;
    }

    public setWholeTile(tileComp, value) {
        var icon = tileComp.getChild('icon');
        MahjongMgr.inst.setTile(icon.asLoader, value);

        var ghost = tileComp.getChild('ghost');
        if (ghost) {
            ghost.visible = (value && this.ghostTileId() == value);
        }
    }

    public setTile(comp, value) {
        if (!value) {
            comp.url = this.getTilerUrl(value);
            return;
        }
        var url = this.getTilerUrl(value);
        //var cache = MahjongMgr.tileCache[url];
        if (url) {
            comp.visible = true;
            comp.url = url;
            return;
        }
        // Laya.loader.load(url, Handler.create(this, function (v, tex) {
        //     comp.visible = (!!tex);
        //     if (!tex) return;
        //     comp.onExternalLoadSuccess(tex);
        //     MahjongMgr.tileCache[v] = tex;
        // }, [url]));
    }

    public addTiles(tiles, outList) {
        outList.removeChildrenToPool();
        if (!tiles) return;
        for (let i = 0; i < tiles.length; ++i) {
            var value = tiles[i];
            //if(!value)continue;
            var tileComp = outList.addItemFromPool().asCom;
            MahjongMgr.inst.setWholeTile(tileComp, value);
        }
    }

    public addMeldTiles(outList, dataList, clear: boolean = false) {
        if (clear) outList.removeChildrenToPool();
        for (let n = 0; n < dataList.length; n++) {
            var meldComp = outList.addItemFromPool().asCom;
            var tiles = dataList[n]['list'] || [];
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
                    this.setTile(icon.asLoader, value);
                    if (ctrl) ctrl.setSelectedIndex(0);
                }
            }
        }
    }

    createTileData = function (id) {
        if (id == null || id == "")
            return null;
        return new TileData(id);
    }

    createTileDataList = function (list) {
        if (typeof list === 'string')
            list = list.split(",");
        var ret = [];
        Tools.inst.each(list, function (tileId) {
            ret.push(this.createTileData(tileId));
        }, this);
        return ret;
    }

    private local2serverPos = {};
    private server2localPos = {};
    transferServerPos = function (posServerSelf, posLocalList = LOCAL_POS_LIST[4]) {
        this.local2serverPos = {};
        this.server2localPos = {};
        var playerCount = posLocalList.length;
        for (var i = 0; i < playerCount; ++i) {
            var posLocal = posLocalList[i];
            var posServer = (i + posServerSelf) % playerCount;

            this.local2serverPos[posLocal] = posServer;
            this.server2localPos[posServer] = posLocal;
        }
        // console.log('local2serverPos',this.local2serverPos)
        // console.log('server2localPos',this.server2localPos)
    }
    getServerPos(posLocal) {
        return this.local2serverPos[posLocal];
    }
    getLocalPos(posServer) {
        return this.server2localPos[posServer];
    }
    isSelf = function (posServer) {
        return 0 == this.getLocalPos(posServer);
    };

    private touchTile: fairygui.GComponent = null;
    setReadyOutTile(tile: fairygui.GComponent) {
        tile.draggable = true;
        this.touchTile = tile;
    }

    setTouchXY(x, y) {
        // var pos = this.touchTile.localToGlobal(x,y)
        this.touchTile.x = x, this.touchTile.y = y;
    }

    public posLocalTurn;
    refreshPlayerTurn(posLocal) {
        this.posLocalTurn = posLocal;
    }
    isMyTurn() {
        return (this.posLocalTurn == 0);
    }

    private _ghostTile = '';
    public ghostTileId() {
        return this._ghostTile;
    }
    public setGhostTile(id) {
        this._ghostTile = id;
    }
}
