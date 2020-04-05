var Game;
var Control;
var Method;
module G570 {
    export let Gmaster;
    export class GMaster extends G560.GMaster {
        protected gameid: number = 570;
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
            Game = G570;
            Control = G570.GControl;
            Method = G570.GMethod;
            return res;
        }
        addPage(data) {
            return UIMgr.inst.add(G570.GPage, null, data) as G570.GPage;
        }
    }
}