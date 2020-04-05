/*
* name;
*/
class Page extends Widget{
    constructor(pkg,comp,layer){
        super(pkg,comp,layer);
        this.keepSize();
    }

    private requestPage=null;
    private showing=false;
    showRequesting(show)
    {
        if(show)
        {
            if(!this.showing)
            {
                Laya.stage.on(NetHandlerMgr.ON_RECEIVED_PING,this,this.onHideRequesting);
                this.requestPage = UIMgr.inst.add(RequestPage,this);
                this.showing = show;
            }
        }
        else
        {
            if(this.requestPage && this.showing)
            {
                Laya.stage.off(NetHandlerMgr.ON_RECEIVED_PING,this,this.onHideRequesting);
                this.requestPage.hide();
                this.showing = show;
            }
        }
    }

    private onHideRequesting()
    {
        this.showRequesting(false);
    }
}

class PreloadingGamePage extends Page
{
    private in_cycle:fairygui.GObject;
    private out_cycle:fairygui.GObject;

    constructor(){
        super('Basic','PreLoading',UILayer.GAME);
    }
    onCreated(){
        var url = ResourceMgr.RES_PATH+'bg/hallBg2.jpg';
        Tools.inst.changeBackground(url,this._view.getChild('bg').asLoader);
        this.in_cycle = this.view.getChild('n20');
        this.out_cycle = this.view.getChild('n19');
    }
    
    onDispose()
    {
        console.log('preload onDispose');
        this.view.getTransitionAt(0).stop();
        Laya.Tween.clearAll(this.in_cycle);
        Laya.Tween.clearAll(this.out_cycle);
    }

    public setProgress(value:number)
    {
        var progress = Math.floor(value*100);
        //this.loadingString.text = (descriptiion.length>0?descriptiion:ExtendMgr.inst.PreloadingPageLoadingString) + progress + '%';
        this.in_cycle.rotation = value*360;
        this.out_cycle.rotation = -value*360;
    }
}

class RequestPage extends Page{
    constructor(){
        super('Basic','request',UILayer.GAME);
    }
    onCreated(){
    }
}