class ReLoginMaster extends Master{
}

class ReLoginScene extends Scene{
    constructor(){
        super();
    }

    getRes(){
        return [
            { url: ExtendMgr.inst.uipath+"/Login.fui", type: Loader.BUFFER },
            { url: ExtendMgr.inst.uipath+"/Login@atlas0.png", type: Loader.IMAGE },
        ];
    }

    start(){
        fairygui.UIPackage.addPackage(ExtendMgr.inst.uipath+'/Login');
        UIMgr.inst.add(ReLoginPage);
    }
}

class ReLoginPage extends Page{
    constructor(){
        super('Login','PageLogin',UILayer.GAME);
    }
    
    onCreated(data:any=null)
    {
        var url = ResourceMgr.RES_PATH+'bg/lodingBg.jpg';
        Tools.inst.changeBackground(url,this._view.getChild('bg').asLoader);

        NetHandlerMgr.inst.setMGNetHandler(null);
        
        var gamePageC = this._view.getController('c1');
        gamePageC.selectedIndex = 3;        
        UserMgr.inst.relogin();
    }
}