class GallMaster extends Master {

    protected _page;
    protected gameid: number;
    protected pingKey: number;

    getResUrl(): { url: string, type: string }[] {
        let res = [];
        return res;
    }

    getImgUrl(): string[] {
        let needloads = [];
        return needloads;
    }

    getUIPackageUrl(): string[] {
        let keys = []
        return keys;
    }

    addPage(data): Widget {
        let page = null;
        return page;
    }

    newNetHandler(): NetHandler {
        let netHandler = null;
        return netHandler;
    }

    //////////////////////////////////////////////

    enter(params) {
        let imgs = this.getImgUrl();
        let res = this.getResUrl();
        Laya.timer.once(15000, this, this.onloadFail); //load ui
        ExtendMgr.inst.liad(imgs, () => {
            Laya.loader.load(res, Handler.create(this, this.onloaded.bind(this, params)));
        }, Handler.create(this, this.onProgress, null, false));

        Laya.timer.loop(0.1, this, this.onProgress);
    }

    onProgress(pro, str = '') {
        if (str.length == 0)
            EventMgr.emit(ExtendMgr.OnMinGameLoadingProgress, pro);
    }

    onloadFail() {
        Laya.timer.clear(this, this.onProgress);
        Alert.show(ExtendMgr.inst.OnConnectError).onYes(function () {
            MasterMgr.inst.switch('lobby');
        });
    }

    onloaded(info) {
        let keys: string[] = this.getUIPackageUrl();
        for (const key of keys) {
            fairygui.UIPackage.addPackage(key);
        }
        this._page = this.addPage({ sid: UserMgr.inst.sid });
        // this._page.view.getChild('bg').visible = false;
        Laya.timer.clear(this, this.onloadFail);
        Laya.timer.clear(this, this.onProgress);
        ExtendMgr.inst.intoGameRoom(info, this.initNetHandler.bind(this));
    }

    initNetHandler(params) {
        let netHandler = this.newNetHandler();
        NetHandlerMgr.inst.setMGNetHandler(netHandler);
        NetHandlerMgr.inst.setLastConnectData(params);
        Laya.timer.once(15000, this, this.onloadFail);//load tile
        UIMgr.loadTileRes(this.gameid, () => {
            netHandler.connect(params, this.onConnectResult.bind(this));
        });
    }

    onConnectResult(connected) {
        Laya.timer.clear(this, this.onloadFail);
        if (!connected) {
            Alert.show(ExtendMgr.inst.OnConnectError).onYes(function () {
                MasterMgr.inst.switch('lobby');
            });
            return;
        }
        var sid = UserMgr.inst.sid;
        NetHandlerMgr.netHandler.enterGame(sid, this.gameid, this.onEnterResult.bind(this));
        NetHandlerMgr.inst.initPingListen(this.pingKey);
    }

    onEnterResult(data) {
        if (data['result']) {
            this._page.onNetIntoGame(data);
        }
        else {
            Alert.show(ExtendMgr.inst.getText4Language(data['reason'])).onYes(() => {
                UserMgr.inst.returnToLobby();
            });
        }

    }

    exit() {
        Laya.timer.clear(this, this.onloadFail);
        Laya.timer.clear(this, this.onProgress);
        if (NetHandlerMgr.netHandler != null) {
            NetHandlerMgr.netHandler.disconnect();
        }
    }

    /////////////////////////////////////////
    reconnectNetHandler() {
        setTimeout(() => {
            NetHandlerMgr.netHandler.connect(NetHandlerMgr.lastConnectParams, (connected) => {
                if (!connected) return;
                var sid = UserMgr.inst.sid;
                NetHandlerMgr.netHandler.enterGame(sid, this.gameid, (data) => {
                    Game.page.onEnterRoomSuccess(data);
                    //Game.page.initMsgListen();
                });
            });
        }, 30);
    }

    startPoll() {
        NetHandlerMgr.netHandler.removeAllMsgListener(ProtoKey.S_C_PING);
        NetHandlerMgr.inst.initPingListen(this.pingKey);
    }
    stopPoll() {
    }
}