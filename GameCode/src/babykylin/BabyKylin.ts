
/*
* BK is short of Babykylin;
*/
function urlParse() {
    var params = {};
    if (window.location == null) {
        return params;
    }
    var name, value;
    var str = window.location.href; //取得整个地址栏
    var num = str.indexOf("?")
    str = str.substr(num + 1); //取得所有参数   stringvar.substr(start [, length ]

    var arr = str.split("&"); //各个参数放到数组里
    for (var i = 0; i < arr.length; i++) {
        num = arr[i].indexOf("=");
        if (num > 0) {
            name = arr[i].substring(0, num);
            value = arr[i].substr(num + 1);
            params[name] = value;
        }
    }
    return params;
}

class bk{
    public static settings:AppSettings = null;

    //managers
    public static net:NetConnection = null;
    public static online:boolean = true;

    private static _updaters:Array<any> = [];
    private static _eventDispather:Laya.EventDispatcher = new Laya.EventDispatcher();

    private static _args:any = null;
    public static get args():any{
        if(this._args == null){
            this._args = urlParse();
        }
        return this._args;
    }

    public static configure(settings:AppSettings){
        this.settings = settings;
                //design resolutions.
        this.setDesignResolution(settings.designWidth,settings.designHeight);
        //stats panel.
        if(settings.showStats){
            //laya.utils.Stat.show(settings.statsX,settings.statsY);
        }
        Laya.stage.frameRate = settings.frameRate;

        this.initModules();

        Laya.stage.on(Laya.Event.RESIZE,this,()=>{
            //this.adjustScaleMode();
        });

        // Laya.stage.on(laya.events.Event.BLUR, this, function(){console.log('进入后台')})
        // Laya.stage.on(laya.events.Event.FOCUS, this,function(){console.log('回到前台')})
        // Laya.stage.on(laya.events.Event.FOCUS_CHANGE, this,function(){console.log('状态变化 visible:'+ Laya.stage.isVisibility + 'isfocused:'+ Laya.stage.isFocused)})
    }
    private static initModules(){
        UIMgr.inst.configure(this.settings.maxUILayer,this.settings.alertWidget,this.settings.wcWidget);
        bk.net = new NetConnection();
    }

    public static setDesignResolution(dw,dh)
    {
        /**/
        Laya.init(dw,dh,WebGL);
        Laya.stage.width = dw;
        Laya.stage.height = dh;
                //align
        Laya.stage.alignH = Laya.Stage.ALIGN_CENTER;
        Laya.stage.alignV = Laya.Stage.ALIGN_MIDDLE;

        Laya.stage.screenMode = dw > dh?Laya.Stage.SCREEN_HORIZONTAL:Laya.Stage.SCREEN_VERTICAL;
        this.adjustScaleMode();/**/
    }

    protected static adjustScaleMode()
    {
        //这个宽高是真实的宽高。
        var rw = Laya.Browser.width;
        var rh = Laya.Browser.height;

        var dw = Laya.stage.designWidth;
        var dh = Laya.stage.designHeight;
        //
        if(dw > dh)
        {
            if(rh > rw){
                var t = rw;
                rw = rh;
                rh = t;
            }
        }
        else
        {
            if(rh < rw){
                var t = rw;
                rw = rh;
                rh = t;
            }
        }

        //确保不能低于最低高度
        Laya.stage.scaleMode = (rw/rh >= dw/dh)?Laya.Stage.SCALE_FIXED_HEIGHT:Laya.Stage.SCALE_FIXED_WIDTH; 
    }

    public static start(startMaster){
        //keep this in the end line.
        MasterMgr.inst.switch(startMaster);

        var sprite = new Laya.EventDispatcher();

        Time.time = Date.now();
        setInterval(()=>{
            Time.deltaTime = Date.now() - Time.time;
            Time.time = Date.now();
            Time.frameCount++;
            bk.update();
        },1000/30);
    }

    public static registerUpdater(target,fnUpdate){
        bk._updaters.push({
            target:target,
            fn:fnUpdate,
        });
    }

    private static update(){
        for(let k in bk._updaters){
            var up = bk._updaters[k];
            up.fn.apply(up.target);
        }
    }

    public static on(type:string,caller:any,listener:Function,args:any[] = null){
        this._eventDispather.on(type,caller,listener,args);
    }

    public static off(type:string,caller:any,listener:Function,onceOnly:boolean = false){
        this._eventDispather.off(type,caller,listener,onceOnly);
    }

    public static emit(type:string,data:any = null){
        this._eventDispather.event(type,data);
    }

    public static reset(){
        this._eventDispather.offAll();
    }
}