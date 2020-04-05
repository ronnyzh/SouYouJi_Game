class G445Master extends GallMaster {
    protected gameid: number = 445;
    getImgUrl(): string[] {
        let needloads = [
            ExtendMgr.inst.uipath + "/MJ@atlas0.png",
        ];
        return needloads;
    }
    getResUrl(): { url: string, type: string }[] {
        var res = [
            { url: ExtendMgr.inst.uipath + "/MJ.fui", type: Loader.BUFFER },
            { url: ResourceMgr.GetGameProtoPath(this.gameid) + 'gold_additive.proto', type: Loader.TEXT }
        ];
        return res;
    }
    getUIPackageUrl(): string[] {
        let keys = [ExtendMgr.inst.uipath + '/MJ']
        return keys;
    }
    newNetHandler(): NetHandler {
        let netHandler = new G445NetHandler();
        return netHandler;
    }
    addPage(data): Widget {
        let page = UIMgr.inst.add(G445Page, null, data);
        return page;
    }
}