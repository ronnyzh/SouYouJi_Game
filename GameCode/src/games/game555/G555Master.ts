class G555Master extends GallMaster {
    protected gameid: number = 555;
    getImgUrl(): string[] {
        let needloads = [
            ExtendMgr.inst.uipath + "/G555@atlas0.png",
        ];
        return needloads;
    }
    getResUrl(): { url: string, type: string }[] {
        var path = ResourceMgr.GetGameProtoPath(this.gameid);
        var res = [
            { url: ExtendMgr.inst.uipath + "/G555.fui", type: Loader.BUFFER },
            { url: path + 'private_mahjong.proto', type: Loader.TEXT },
        ];
        return res;
    }
    getUIPackageUrl(): string[] {
        let keys = [ExtendMgr.inst.uipath + '/G555']
        return keys;
    }
    addPage(data): Widget {
        let page = UIMgr.inst.add(G555Page, null, { sid: UserMgr.inst.sid }) as G555Page;
        return page;
    }
    newNetHandler(): NetHandler {
        let netHandler = new G555NetHandler();
        return netHandler;
    }
}