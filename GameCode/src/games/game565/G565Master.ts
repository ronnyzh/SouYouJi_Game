module G565 {
    export class G565Master extends GallMaster {
        protected gameid: number = 565;
        protected pingKey: number = G565.S_C_PING;
        getImgUrl(): string[] {
            let needloads = [
                ExtendMgr.inst.uipath + '/pokersStyle2@atlas0.png',
                ExtendMgr.inst.uipath + '/G565@atlas0.png',
            ];
            return needloads;
        }
        getResUrl(): { url: string, type: string }[] {
            var path = ResourceMgr.GetGameProtoPath(this.gameid);
            let res = [
                { url: path + 'dezhou_poker.proto', type: Loader.TEXT },
                { url: path + 'gold_additive.proto', type: Loader.TEXT },
                { url: path + 'poker.proto', type: Loader.TEXT },
                { url: path + 'baseProto.proto', type: Loader.TEXT },
                { url: ExtendMgr.inst.uipath + '/pokersStyle2.fui', type: Loader.BUFFER },
                { url: ExtendMgr.inst.uipath + '/G565.fui', type: Loader.BUFFER },
            ];
            return res;
        }
        getUIPackageUrl(): string[] {
            let keys = [ExtendMgr.inst.uipath + '/G565', ExtendMgr.inst.uipath + '/pokersStyle2'];
            return keys;
        }
        newNetHandler() {
            return new G565NetHandler();
        }
        addPage(data) {
            return UIMgr.inst.add(G565Page, null, data) as G565.G565Page;
        }
    }
}