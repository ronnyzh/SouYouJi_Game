/*
* name;
*/
module G548 
{
    export class G548Master extends GallMaster 
    {
        protected gameid: number = 548;
        protected pingKey: number = G548.S_C_PING;
        
        getImgUrl(): string[] {
            return [ExtendMgr.inst.uipath+"/G548@atlas0.png"];
        }

        getResUrl(): { url: string, type: string }[] 
        {
            let path = ResourceMgr.GetGameProtoPath(548);
            let res = [
                    { url: path + 'baccarat.proto', type: Loader.TEXT },
                    { url: path + 'chets.proto', type: Loader.TEXT },
                    { url: path + 'zhajinhua_poker.proto', type: Loader.TEXT },
                    { url: path + 'gold_additive.proto', type: Loader.TEXT },
                    { url: path + 'poker.proto', type: Loader.TEXT },
                    { url: path + 'baseProto.proto', type: Loader.TEXT },
                    { url: ExtendMgr.inst.uipath+'/G548.fui', type: Loader.BUFFER }
                ];
            return res;
        }

        getUIPackageUrl(): string[] {
            return [ExtendMgr.inst.uipath+'/G548'];
        }

        newNetHandler(): NetHandler {
            return new G548NetHandler();
        }

        addPage(data): Widget {
            return UIMgr.inst.add(G445Page, null, data);
        }
        
        exit() 
        {
            this._page.clearView();
            super.exit();
            NoticeView.hide();
            Tools.inst.clearAllTimeout();
            if(NetHandlerMgr.inst.valid())
            {
                NetHandlerMgr.netHandler.disconnect();
            }
        }
    }
}