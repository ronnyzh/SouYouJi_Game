module G562 {
    export class G562Master extends GallMaster {
        protected gameid: number = 562;
        protected pingKey: number = G562.S_C_PING;
        getImgUrl(): string[] {
            let needloads = [
                ExtendMgr.inst.uipath + "/G562@atlas0.png",
                ExtendMgr.inst.uipath + "/pokers@atlas0.png",
            ];
            return needloads;
        }
        getResUrl(): { url: string, type: string }[] {
            var path = ResourceMgr.GetGameProtoPath(this.gameid);
            let res = [
                { url: path + 'baseProto.proto', type: Loader.TEXT },
                { url: path + 'poker.proto', type: Loader.TEXT },
                { url: path + 'replay4proto.proto', type: Loader.TEXT },
                { url: path + 'thirteenWater_poker.proto', type: Loader.TEXT },
                { url: ExtendMgr.inst.uipath + "/G562.fui", type: Loader.BUFFER },
                { url: ExtendMgr.inst.uipath + "/pokers.fui", type: Loader.BUFFER },
            ];
            return res;
        }
        getUIPackageUrl(): string[] {
            let keys = [ExtendMgr.inst.uipath + '/G562', ExtendMgr.inst.uipath + '/pokers'];
            return keys;
        }
        addPage(data): Widget {
            G562.twa.initUICard();
            let page = UIMgr.inst.add(G562Page, null, { sid: UserMgr.inst.sid }) as G562Page;
            return page;
        }
        newNetHandler(): NetHandler {
            let netHandler = new G562NetHandler();
            return netHandler;
        }
    }
}