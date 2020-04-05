var Game;
var Control;
var Method;
module G561 {
    export let Gmaster;
    export class GMaster extends GallMaster {
        protected gameid: number = 561;
        protected pingKey: number = S_C_PING;
        constructor() {
            super();
            Gmaster = this;
        }
        getImgUrl(): string[] {
            let needloads = [
                ExtendMgr.inst.uipath + "/G561@atlas0.png",
                ExtendMgr.inst.uipath + "/Effect@atlas0.png",
                ExtendMgr.inst.uipath + "/Effect@atlas0_1.png",
                ExtendMgr.inst.uipath + "/Effect@atlas1.png",
                ExtendMgr.inst.uipath + "/Effect@atlas1_1.png",
                ExtendMgr.inst.uipath + "/Effect@atlas1_2.png",
            ];
            return needloads;
        }
        getResUrl(): { url: string, type: string }[] {
            var path = ResourceMgr.GetGameProtoPath(this.gameid);
            var res = [
                { url: path + 'gold_additive.proto', type: Loader.TEXT },
                { url: path + 'zhajinhua_poker.proto', type: Loader.TEXT },
                { url: path + 'baseProto.proto', type: Loader.TEXT },
                { url: path + 'poker.proto', type: Loader.TEXT },
                { url: ExtendMgr.inst.uipath + "/G561.fui", type: Loader.BUFFER },
                { url: ExtendMgr.inst.uipath + "/Effect.fui", type: Loader.BUFFER },
            ];
            Game = G561;
            Control = G561.GControl;
            Method = G561.GMethod;
            return res;
        }
        addPage(data) {
            return UIMgr.inst.add(G561.GPage, null, data) as G561.GPage;
        }
        newNetHandler(): NetHandler {
            let netHandler = new Game.GNetHandler();
            return netHandler;
        }
        getUIPackageUrl(): string[] {
            let keys = [ExtendMgr.inst.uipath + '/Effect', ExtendMgr.inst.uipath + '/G561'];
            return keys;
        }
    }
}


