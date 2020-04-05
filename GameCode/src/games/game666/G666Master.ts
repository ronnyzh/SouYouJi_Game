class G666Master extends Master{

    private _page: G666Page;

    constructor(){
        super()
    }

    enter(params)
    {
        super.enter(params);
        var proto_path = ResourceMgr.GetGameProtoPath(666);
        var res = [
            { url: proto_path+'huanle_niuniu.proto', type :Loader.TEXT},//2018.6.28
            { url: proto_path+'poker.proto',type:Loader.TEXT},
            { url: proto_path+'baseProto.proto',type:Loader.TEXT},
            { url: proto_path+'gold_additive.proto',type:Loader.TEXT},
            { url: ExtendMgr.inst.uipath+"/G666.fui", type: Loader.BUFFER },
            //{ url: ExtendMgr.inst.uipath+"/G666@atlas0.png", type: Loader.IMAGE },
            { url: ExtendMgr.inst.uipath+'/G666@rljf9n.ogg',type:Loader.SOUND}
        ];        

        ExtendMgr.inst.liad([ExtendMgr.inst.uipath+"/G666@atlas0.png"],function()
        {
            Laya.loader.load(res, Handler.create(this, this.onloaded.bind(this,params)));
        }.bind(this),Handler.create(this, this.onProgress, null, false));
    }

    onProgress(pro,str='')
    {
        if(str.length == 0)
            EventMgr.emit(ExtendMgr.OnMinGameLoadingProgress,pro);
    }
    
    onloaded(info) {
        var pkg = fairygui.UIPackage.addPackage(ExtendMgr.inst.uipath+'/G666');
        this._page = UIMgr.inst.add(G666Page, null, { sid: UserMgr.inst.sid }) as G666Page;

        ExtendMgr.inst.intoGameRoom(info, this.initNetHandler.bind(this));
    }

    initNetHandler(params){

        var netHandler = new G666NetHandler();
        NetHandlerMgr.inst.setMGNetHandler(netHandler);
        NetHandlerMgr.inst.setLastConnectData(params);
        UIMgr.loadTileRes(666, () => {
            netHandler.connect(params, this.onConnectResult.bind(this));
        });
        //netHandler.connect(params,this.onConnectResult.bind(this));
    }

    onConnectResult(connected){
        if (!connected) {
            Alert.show(ExtendMgr.inst.OnConnectError).onYes(function () {
                MasterMgr.inst.switch('lobby');
            });
            return;
        }
        var sid = UserMgr.inst.sid;
        NetHandlerMgr.netHandler.enterGame(sid, 666,this.onEnterResult.bind(this));  
        NetHandlerMgr.inst.initPingListen(ProtoKey666.S_C_PING);
    }

    onEnterResult(data)
    {
        this._page.onNetIntoGame(data);
    }

    exit()
    {
        var background = Laya.stage.getChildByName(minigame_background_mark) as laya.ui.Image;
        if(background)
        {
            Laya.stage.removeChild(background);
        }

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