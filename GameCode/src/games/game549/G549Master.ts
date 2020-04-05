/*
* name;
*/
module G549 
{
    export class G549Master extends G548.G548Master
    {
        protected gameid: number = 549;

        getResUrl(): { url: string, type: string }[] 
        {
            let path = ResourceMgr.GetGameProtoPath(549);
            let oldpath = ResourceMgr.GetGameProtoPath(548);
            let res = [
                    { url: path + 'baccarat.proto', type: Loader.TEXT },
                    { url: oldpath + 'chets.proto', type: Loader.TEXT },
                    { url: oldpath + 'zhajinhua_poker.proto', type: Loader.TEXT },
                    { url: oldpath + 'gold_additive.proto', type: Loader.TEXT },
                    { url: oldpath + 'poker.proto', type: Loader.TEXT },
                    { url: oldpath + 'baseProto.proto', type: Loader.TEXT },
                    { url: ExtendMgr.inst.uipath+'/G548.fui', type: Loader.BUFFER }
                ];
            return res;
        }

        newNetHandler(): NetHandler {
            return new G549NetHandler();
        }

        addPage(data): Widget {
            return UIMgr.inst.add(G549Page, null, data);
        }
    }
}