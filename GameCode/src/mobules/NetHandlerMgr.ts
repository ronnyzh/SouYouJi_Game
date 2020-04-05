/*
* name;
*/
class NetHandlerMgr
{
    private static _inst:NetHandlerMgr = null;
    public static get inst():NetHandlerMgr{
        if(NetHandlerMgr._inst == null){
            NetHandlerMgr._inst = new NetHandlerMgr();
        }
        return NetHandlerMgr._inst;
    }

    public static removeSelf(){
        if(NetHandlerMgr._inst){
            // delete NetHandlerMgr._inst;
            NetHandlerMgr._inst = null;
        }
    }

    private _netHandler:any = null;
    public setMGNetHandler(netHandler:any){
        this._netHandler = netHandler;
    }
    public static get netHandler():any{
        return NetHandlerMgr.inst._netHandler;
    }



    constructor(){ /*bk.registerUpdater(this,this.update);*/ }
    
    private _lastConnectData:any = null;
    public setLastConnectData(params:any){
        this._lastConnectData = params;
    }
    public static get lastConnectParams():any{
        //console.log('lastConnectParams:',NetHandlerMgr.inst._lastConnectData)
        return NetHandlerMgr.inst._lastConnectData;
    }

    update (dt) { }

    public static ON_RECEIVED_PING:string = 'on_received_ping';

    private PING_INTERVAL:number = 7000;
    private PING_LIMIT:number = 8000;
    private ping_limit:number;    
    private pingReferenceTime:number;    
    private receivePingTime:number;    
    private sendPingTime:number;    
    private pollSendId:number;     

    private S_C_PING:number;

    private relogin_ing:boolean = false;

    initPingListen(key?)
    {
        this.S_C_PING = key || ProtoKey.S_C_PING;
        this.ping_limit = this.PING_INTERVAL + this.PING_LIMIT;
        this._netHandler.addMsgListener(this.S_C_PING, this.onReceivePing.bind(this));
        this.resetPingListen();
    }
    
    resetPingListen()
    {
        this.pingReferenceTime = 0;
        this.receivePingTime = Date.now();
        this.sendPingTime = Date.now();
        
        clearInterval(this.pollSendId);
        this.pollSendId = setInterval(this.onSendPing.bind(this), this.PING_INTERVAL);
        clearInterval(this.pollCheckPing);
        this.pollCheckPing = setInterval(this.checkPing.bind(this), 500);
    }

    clearPingListen()
    {
        clearInterval(this.pollSendId);
        clearInterval(this.pollCheckPing);
    }

    valid(){
        return (this._netHandler && this._netHandler.valid());
    }

    private pollCheckPing:number;   
    checkPing()
    {
        if(!this.valid())return;
        var time_diff = Date.now() - this.receivePingTime;
        if(time_diff > this.ping_limit)
        {
            console.log("checkPing -> relogin?! " +  time_diff + " " + this.receivePingTime);
            this.receivePingTime = Date.now();
            try 
            {
                if(this.alertView)
                {
                    this.alertView.hide(); 
                    this.alertView=null;
                }
                
                if(!this.relogin_ing)
                {
                    Laya.stage.on(NetHandlerMgr.ON_RECEIVED_PING,this,this.onRecvPingWhenRelogin.bind(this));

                    this.alertView = Alert.show(ExtendMgr.inst.NetCheckPingAlert).onYes(function()
                    {
                        this.relogin_ing = false;
                        MasterMgr.inst.switch('relogin');
                    }.bind(this));
                }
            } 
            catch (error) 
            {
                console.log(error);
            }

            this.relogin_ing = true;
        }
    }

    private alertView;

    onSendPing()
    {
        if(this.valid())
        {
            this.sendPingTime = Date.now();
            this._netHandler.sendPing();
            console.log("this.sendPing----------",this.sendPingTime);
        }
    }

    onReceivePing()
    {
        this.receivePingTime = Date.now();
        this.pingReferenceTime = (this.pingReferenceTime + this.receivePingTime - this.sendPingTime) / 2;
        this.ping_limit = this.PING_INTERVAL + this.PING_LIMIT + this.pingReferenceTime;
    }

    onReceiveMsg()
    {
        //this.receivePingTime = Date.now();
        Laya.stage.event(NetHandlerMgr.ON_RECEIVED_PING);
    }

    onRecvPingWhenRelogin()
    {
        this.relogin_ing = false;
        Laya.stage.off(NetHandlerMgr.ON_RECEIVED_PING,this,this.onRecvPingWhenRelogin.bind(this));
        if(this.alertView)
        {
            this.alertView.hide();
            this.alertView=null;
        }
    }
}