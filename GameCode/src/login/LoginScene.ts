/*
* name;
*/
class LoginScene extends Scene{
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
        UIMgr.inst.add(LoginPage);
    }

    update(){

    }

    end(){
        super.end();
    }
}