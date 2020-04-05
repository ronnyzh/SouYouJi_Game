/*
* name;
*/
class PreloadingPage extends Page{
    constructor(){
        super("Preloading","Preloading",UILayer.GAME);
    }
    
    private loadingString:fairygui.GTextField = null;
    private loadingBar:fairygui.GProgressBar = null;

    onCreated(){
        var view = this._view;
        var logoanima = view.getChild('logoanima');
        if(logoanima) view.getChild('logoanima').center();
        this.loadingString = view.getChild('loadingTxt').asTextField;
        this.loadingBar = view.getChild('loadingBar').asProgress;
        this.setProgress(0);
        
        var url = ResourceMgr.RES_PATH+'bg/lodingBg.jpg';
        Tools.inst.changeBackground(url,this._view.getChild('bg').asLoader);
    }

    setProgress(value:number,descriptiion:string = '')
    {
        var progress = Math.floor(value*100);
        this.loadingString.text = (descriptiion.length>0?descriptiion+progress:ExtendMgr.inst.PreloadingPageLoadingString + progress + '%');
        this.loadingBar.update(progress);
    }
}