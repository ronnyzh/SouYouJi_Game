/*
* name;
*/
module G9999 {
    export class G9999Master extends Master {

        constructor() {
            super()
        }

        enter(params) {
            let path = ResourceMgr.GetGameProtoPath(9999);
            let res = [
                { url: path + 'baccarat.proto', type: Loader.TEXT },
                { url: path + 'chets.proto', type: Loader.TEXT },
                { url: path + 'zhajinhua_poker.proto', type: Loader.TEXT },
                { url: path + 'gold_additive.proto', type: Loader.TEXT },
                { url: path + 'poker.proto', type: Loader.TEXT },
                { url: path + 'baseProto.proto', type: Loader.TEXT },
                { url: ExtendMgr.inst.uipath+'/G9999.fui', type: Loader.BUFFER },
                { url: ExtendMgr.inst.uipath+'/G9999@atlas0.png', type: Loader.IMAGE },
                { url: ExtendMgr.inst.uipath+'/G9999@z5p1b5.ogg', type: Loader.SOUND}
            ];
            Laya.loader.load(res, Handler.create(this, this.initNetHandler.bind(this, params)));
        }

        newNetHandler() {
            return new G9999NetHandler();
        }

        initNetHandler(params) {
            let pkg = fairygui.UIPackage.addPackage(ExtendMgr.inst.uipath+'/G9999');
            let netHandler = this.newNetHandler();
            NetHandlerMgr.inst.setMGNetHandler(netHandler);
            NetHandlerMgr.inst.setLastConnectData(params);
            netHandler.connect(params, this.onConnectResult.bind(this));
        }

        onConnectResult(connected) {
            if (!connected) {
                Alert.show(ExtendMgr.inst.OnConnectError).onYes(function () {
                    MasterMgr.inst.switch('lobby');
                });
                return;
            }
            let sid = UserMgr.inst.sid;
            NetHandlerMgr.netHandler.enterGame(sid, 9999,this.onEnterResult.bind(this));
            NetHandlerMgr.inst.initPingListen(G9999.S_C_PING);
        }

        onEnterResult(data) {
            this.addPage(data);
        }

        addPage(data) {
            UIMgr.inst.add(G9999Page, null, data);
        }

        exit() {
            if(NetHandlerMgr.inst.valid())
            {
                NetHandlerMgr.netHandler.disconnect();
            }
        }
    }
}