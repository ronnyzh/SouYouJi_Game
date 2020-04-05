class G557Master extends GallMaster {
    protected gameid: number = 557;
    getImgUrl(): string[] {
        let needloads = [
            ExtendMgr.inst.uipath + "/G557@atlas0.png",
        ];
        return needloads;
    }
    getResUrl(): { url: string, type: string }[] {
        var path = ResourceMgr.GetGameProtoPath(this.gameid);
        var res = [
            { url: path + 'private_mahjong.proto', type: Loader.TEXT },
            { url: ExtendMgr.inst.uipath + "/G557.fui", type: Loader.BUFFER },
        ];
        return res;
    }
    getUIPackageUrl(): string[] {
        let keys = [ExtendMgr.inst.uipath + '/G557']
        return keys;
    }

    newNetHandler() {
        return new G557NetHandler();
    }
    addPage(data) {
        return UIMgr.inst.add(G557Page, null, data) as G557Page;
    }

}