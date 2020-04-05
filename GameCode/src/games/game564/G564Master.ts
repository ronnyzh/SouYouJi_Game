class G564Master extends G445Master {

    protected gameid: number = 564;
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
            { url: path + 'BloodRiver_mahjong.proto', type: Loader.TEXT }
        ];
        return res;
    }
    newNetHandler() {
        return new G564NetHandler();
    }
    addPage(data) {
        return UIMgr.inst.add(G564Page, null, data);
    }
}