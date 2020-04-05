class G449Master extends G445Master {
    protected gameid: number = 449;
    getImgUrl(): string[] {
        let needloads = [
            ExtendMgr.inst.uipath + "/MJ@atlas0.png",
        ];
        return needloads;
    }
    getResUrl(): { url: string, type: string }[] {
        var path = ResourceMgr.GetGameProtoPath(this.gameid);
        var res = [
            { url: ExtendMgr.inst.uipath + "/MJ.fui", type: Loader.BUFFER },
            { url: path + 'gold_additive.proto', type: Loader.TEXT },
            { url: path + 'twoPeople_mahjong.proto', type: Loader.TEXT }
        ];
        return res;
    }
    newNetHandler(): NetHandler {
        let netHandler = new G449NetHandler();
        return netHandler;
    }
    addPage(data): Widget {
        let page = UIMgr.inst.add(G449Page, null, data);
        return page;
    }
}