class G566NetHandler extends G563NetHandler {

    getGameProtoDataList() {
        var path = ResourceMgr.GetGameProtoPath(566);
        var classesMapList = this.getClassesMapList();
        var protoDataList = [
            { pkgName: "private_mahjong", path: path + 'private_mahjong.proto', classesMapList: classesMapList }
        ];
        return protoDataList;
    }
}