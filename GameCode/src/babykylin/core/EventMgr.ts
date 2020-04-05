/*
* name;
*/
class EventMgr{
    private static _eventDispather:Laya.EventDispatcher = new Laya.EventDispatcher();
    
    public static on(type:string,caller:any,listener:Function,args:any[] = null):Laya.EventDispatcher{
        return this._eventDispather.on(type,caller,listener,args);
    }

    public static once(type:string,caller:any,listener:Function,args:any[] = null):Laya.EventDispatcher{
        return this._eventDispather.once(type,caller,listener,args);
    }

    public static off(type:string,caller:any,listener:Function,onceOnly:boolean = false):Laya.EventDispatcher{
        return this._eventDispather.off(type,caller,listener,onceOnly);
    }

    public static emit(type:string,data:any = null):boolean{
        return this._eventDispather.event(type,data);
    }

    public static offAll(type:string = null){
        this._eventDispather.offAll(type);
    }
}