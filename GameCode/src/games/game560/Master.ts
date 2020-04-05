var Game;
var Control;
var Method;
module G560 {
    export let Gmaster;
    export class GMaster extends GallMaster {
        protected gameid: number = 560;
        constructor() {
            super();
            Gmaster = this;
        }
        getImgUrl(): string[] {
            let needloads = [
                ExtendMgr.inst.uipath + "/G560@atlas0.png",
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
                { url: path + 'private_mahjong.proto', type: Loader.TEXT },
                { url: ExtendMgr.inst.uipath + "/G560.fui", type: Loader.BUFFER },
                { url: ExtendMgr.inst.uipath + "/Effect.fui", type: Loader.BUFFER },
            ];
            Game = G560;
            Control = G560.GControl;
            Method = G560.GMethod;
            return res;
        }
        getUIPackageUrl(): string[] {
            let keys = [ExtendMgr.inst.uipath + '/Effect', ExtendMgr.inst.uipath + '/G560'];
            return keys;
        }
        addPage(data): Widget {
            let page = UIMgr.inst.add(G560.GPage, null, data) as G560.GPage;
            return page;
        }
        newNetHandler(): NetHandler {
            let netHandler = new Game.GNetHandler();
            return netHandler;
        }
    }
}