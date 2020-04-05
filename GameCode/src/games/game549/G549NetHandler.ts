module G549 {
    export let S_C_SEND_LUDAN = 0x00006029; // 发送路单信息
    export let S_C_SEND_VIEWER_DATA = 0x00006030; // 发送观察者需要的数据
    export let S_C_SEND_NOBID_COUNT = 0x00006031; // 连续3，5次没有下注就发送
    
    export class G549NetHandler extends G548.G548NetHandler {

        getGameProtoDataList() {
            let baccaratMapList = [
                [S_C_SEND_LUDAN,'S_C_send_ludan'],
                [S_C_SEND_VIEWER_DATA,'S_C_send_viewer_data'],
                [S_C_SEND_NOBID_COUNT,'S_C_send_nobid_count']
            ];

            let protoDataList = super.getGameProtoDataList();
            let path = ResourceMgr.GetGameProtoPath(549);
            let oldpath = ResourceMgr.GetGameProtoPath(548);

            for(let i = 0; i<oldpath.length; i++)
            {
                if(protoDataList[i]['pkgName'] == 'baccarat.proto')
                {
                    protoDataList[i]['path'] = path + 'baccarat.proto';
                    let maplist = protoDataList[i]['classesMapList'];
                    protoDataList[i]['classesMapList'] = maplist.concat(baccaratMapList);
                    break;
                }
            }

            return protoDataList;
        }
    }
}