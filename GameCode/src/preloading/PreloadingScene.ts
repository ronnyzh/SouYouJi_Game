/*
* name;
*/
class PreloadingScene extends Scene {
    private pageRoot: PreloadingPage = null;
    private loadingBar: any = null;

    
    private uipath: string = ResourceMgr.RES_PATH+"ui_" + ExtendMgr.CN;

    constructor() { super(); }

    start() 
    {
        if (ExtendMgr.inst.lan == ExtendMgr.CN)
            this.uipath = ResourceMgr.RES_PATH+"ui";
        else
            this.uipath = ResourceMgr.RES_PATH+"ui_" + ExtendMgr.inst.lan;

        ExtendMgr.inst.uipath = this.uipath;

        ExtendMgr.inst.liad([this.uipath + "/Preloading@atlas0.png"],function()
        {
            Laya.loader.load([
                { url: this.uipath + "/Preloading.fui", type: Loader.BUFFER },
                //{ url: this.uipath + "/Preloading@atlas0.png", type: Loader.IMAGE }
            ], Handler.create(this, this.onPreloadingUILoaded));
        }.bind(this));
    }

    update() { }

    end() { super.end(); }

    onPreloadingUILoaded() 
    {
        fairygui.UIPackage.addPackage(this.uipath + '/Preloading');
        this.pageRoot = UIMgr.inst.add(PreloadingPage) as PreloadingPage;
        
        var wait_of_loading_ui = Laya.stage.getChildByName(wait_of_loading_mark) as laya.ui.Image;
        if(wait_of_loading_ui)
        {
            Laya.stage.removeChild(wait_of_loading_ui);
        }
        this.pageRoot.setProgress(0);
        this.startPreloadingQueue();
    }

    startPreloadingQueue() 
    {
        /*
        //加载部分麻将
        var path = 'res/tiles/';
        for(var i=1;i<10;i++){
            res.push({ url: path+'lwgc_tile_a'+i+'.png', type: Loader.IMAGE});
            res.push({ url: path+'lwgc_tile_b'+i+'.png', type: Loader.IMAGE});
            res.push({ url: path+'lwgc_tile_c'+i+'.png', type: Loader.IMAGE});
        }
        //加载扑克
        var addPokers=function(path){
            for(var i=1;i<14;i++){
                res.push({ url: path+'card_a'+i+'.png', type: Loader.IMAGE});
                res.push({ url: path+'card_b'+i+'.png', type: Loader.IMAGE});
                res.push({ url: path+'card_c'+i+'.png', type: Loader.IMAGE});
                res.push({ url: path+'card_d'+i+'.png', type: Loader.IMAGE});
            }
        }
        addPokers('res/pokers/cards/');
        addPokers('res/pokers/style0/');
        */

        //预加载队列
        var protoPath = ResourceMgr.PROTO_PATH;
        var res = [
            { url: protoPath + "mahjong.proto", type: Loader.TEXT },
            { url: protoPath + "gold.proto", type: Loader.TEXT },
            { url: this.uipath + "/Basic.fui", type: Loader.BUFFER },
            { url: this.uipath + "/Login.fui", type: Loader.BUFFER },
            { url: this.uipath + "/BaccaratGrid.fui", type: Loader.BUFFER },
            { url: this.uipath + "/Hall.fui", type: Loader.BUFFER },
            { url: this.uipath + "/GALL.fui", type: Loader.BUFFER },
            { url: this.uipath + "/GBP.fui", type: Loader.BUFFER },
            { url: this.uipath + "/MJ.fui", type: Loader.BUFFER },
            { url: this.uipath + "/Effect.fui", type: Loader.BUFFER },
            { url: this.uipath + "/Test.fui", type: Loader.BUFFER }
        ];

        var needloads = [
        this.uipath + "/Basic@atlas0.png",this.uipath + "/Login@atlas0.png",this.uipath + "/BaccaratGrid@atlas0.png",this.uipath + "/Hall@atlas0.png",
        this.uipath + "/GALL@atlas0.png",this.uipath + "/GBP@atlas0.png",this.uipath + "/MJ@atlas0.png",
        this.uipath + "/Effect@atlas0.png",this.uipath + "/Effect@atlas0_1.png",this.uipath + "/Effect@atlas1.png",
        this.uipath + "/Effect@atlas1_1.png",this.uipath + "/Effect@atlas1_2.png",this.uipath + "/Test@atlas0.png"

        //this.uipath + "/G548@atlas0.png",this.uipath + "/G561@atlas0.png",this.uipath + "/G562@atlas0.png",this.uipath + "/G565@atlas0.png"
        ];

        //加载背景
        needloads.concat([ResourceMgr.RES_PATH+"bg/lodingBg.jpg", ResourceMgr.RES_PATH+"bg/hallBg.jpg", ResourceMgr.RES_PATH+"bg/hallBg2.jpg"]);

        ExtendMgr.inst.liad(needloads,function()
        {
            Laya.loader.load(res, Handler.create(this, this.onLoaded), Handler.create(this, this.onProgress, null, false));
        }.bind(this),Handler.create(this, this.onProgress, null, false));

        UI_Setting.refreshSoundVolume();//音量
    }

    onProgress(pro,str=''): void {
        this.pageRoot.setProgress(pro,str);
    }

    onLoaded(): void {
        fairygui.UIPackage.addPackage(this.uipath + '/Basic');
        fairygui.UIPackage.addPackage(this.uipath + '/BaccaratGrid');

        setTimeout(function () {
            MasterMgr.inst.switch('login');
        }.bind(this), 200);
    }
}