class G556Master extends GallMaster {
    protected gameid: number = 556;
    getImgUrl(): string[] {
        let needloads = [
            ExtendMgr.inst.uipath + "/G556@atlas0.png",
        ];
        return needloads;
    }
    getResUrl(): { url: string, type: string }[] {
        var path = ResourceMgr.GetGameProtoPath(this.gameid);
        var res = [
            { url: ExtendMgr.inst.uipath + "/G556.fui", type: Loader.BUFFER },
            { url: path + 'private_mahjong.proto', type: Loader.TEXT }
        ];
        return res;
    }
    getUIPackageUrl(): string[] {
        let keys = [ExtendMgr.inst.uipath + '/G556']
        return keys;
    }

    newNetHandler() {
        return new G556NetHandler();
    }

    addPage(data) {
        return UIMgr.inst.add(G556Page, null, data) as G556Page;
    }

}