var Game;
var Control;
var Method;
module G559 {
    export let Gmaster;
    export class GMaster extends GallMaster {
        constructor() {
            super();
            Gmaster = this;
        }
        protected gameid: number = 559;
        getImgUrl(): string[] {
            let needloads = [
                ExtendMgr.inst.uipath + '/G559@atlas0.png',
            ];
            return needloads;
        }
        getResUrl(): { url: string, type: string }[] {
            var path = ResourceMgr.GetGameProtoPath(this.gameid);
            var res = [
                { url: ExtendMgr.inst.uipath + '/G559.fui', type: Loader.BUFFER },
                { url: path + 'private_mahjong.proto', type: Loader.TEXT }
            ];
            Game = G559;
            Control = G559.GControl;
            Method = G559.GMethod;
            return res;
        }
        getUIPackageUrl(): string[] {
            let keys = [ExtendMgr.inst.uipath + '/G559']
            return keys;
        }
        addPage(data): Widget {
            let page = UIMgr.inst.add(G559.GPage, null, { sid: UserMgr.inst.sid }) as G559.GPage;
            return page;
        }
        newNetHandler(): NetHandler {
            let netHandler = new Game.GNetHandler();
            return netHandler;
        }
    }
}