/*
* name;
*/
class G558NetHandler extends G556NetHandler {
    constructor() {
        super()
    }

    getGameProtoDataList() {
        var path = ResourceMgr.GetGameProtoPath(558);
        var classesMapList = this.getClassesMapList();
        var protoDataList = [
            { pkgName: "private_mahjong", path: path + 'private_mahjong.proto', classesMapList: classesMapList }
        ];
        return protoDataList;
    }
}