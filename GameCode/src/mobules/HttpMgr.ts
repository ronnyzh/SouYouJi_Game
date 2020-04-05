/*
* name;
*/
class HttpMgr{
    private static _inst:HttpMgr = null;
    public static get inst():HttpMgr{
        if(HttpMgr._inst == null){
            HttpMgr._inst = new HttpMgr();
        }
        return HttpMgr._inst;
    }

    private addr:string = null;
    private port:number =  null;
    private http:HTTP = null;
    constructor(){

    }

    configure(addr,port)
    {
        this.addr = addr;
        this.port = port;
        this.http = new HTTP(addr+':'+port);
        
        if(TestMgr.IS_ENABLE_PRINT_URL)
        {
            console.log(location.href);
            console.log(addr+":"+port);
        }
    }

    get url(){
        return this.addr + ':' + this.port;
    }

    getSource(){
        return this.http;
    }

    guest(account,cb){
        this.login(account,'ping',cb);
    }

    private _loginData;
    login(account,sign,cb){

        var loginData = this._loginData ={
            account:account, passwd:sign, type : 0
        };
        
        var time = new Date();
        var num = time.valueOf();
        loginData["ttA"] = (num.toString()+Tools.inst.randomInt(126, 198335));
        var tt = md5(loginData["ttA"]);
        var ttB = tt.slice(1,4);
        loginData["ttC"] = md5(loginData["ttA"]+ttB);

        this.http.send('/hall/login','post',loginData,cb);
    }
    
    loginEncryption(sign,cb){
        //console.log(sign);
        //console.log(sign.length);
        this.http.send('/hall/login/h5','post',{encryption:sign},cb);
    }
    
    relogin(cb?){
        let data = this._loginData;
        if(data){
            this.login(data['account'], data['passwd'], function(ret){
                HttpMgr.inst.getSource().sid = ret.sid;
                // HttpMgr.inst.getSource().mid = ret.mid;

                if(cb)cb(true, ret);
            } );
        }else{
            if(cb)cb(false)
        }
    }
    
    getGameID(roomId:string, cb:Function = null)
    {
        this.http.send("/hall/getGameID","POST",{roomid : roomId},cb);
    }

    joinRoom(roomId, cb:Function = null,failcb:Function = null)
    {
        this.http.send("/hall/joinRoom","POST",{roomid : roomId},cb,failcb);
    }
    
    extendSession(cb:Function = null){
        this.http.send('/hall/extendSession','get',{ },cb);
    }
    
    refreshGoldGameListh(cb:Function = null,failcb:Function = null) {
        this.http.send('/hall/party/gold/gameList','POST',{ },cb,failcb);
    }
    
    refreshPlayerData(cb:Function = null) {
        this.http.send('/hall/new_refresh','POST',{ },cb);
    }
    
    refreshPlayerDataReal(cb:Function = null,failcb:Function = null) {
        this.http.send('/hall/getGold','POST',{ },cb);
    }
    
    joinPartyGold(params:any = {},cb:Function = null,failcb:Function = null) {
        this.http.send('/hall/joinGoldRoom','POST',params,cb,failcb);
    }
    
    checkJoinPartyGold(cb:Function = null) {
        this.http.send('/hall/checkJoinGoldRoom','POST',{},cb);
    }
    
    sendGMSet(coinNum, cb:Function = null) {
        this.http.send('/hall/welfare/coin/GMSet','POST',{coinNum : coinNum},cb);
    }
    
    refreshSession(cb:Function = null) {
        this.http.send('/hall/extendSession','GET',{},cb);
    }
    
    getHeaders(cb:Function = null) {
        this.http.send('/hall/getHeaders','GET',{},cb);
    }
    
    setHeaders(hid, cb:Function = null) {
        this.http.send('/hall/setHeaders','POST',{id : hid},cb);
    }
    
    getHistorys(params:any = {}, cb:Function = null) {
        this.http.send('/hall/gameHistory','POST',params,cb);
    }
    
    getBroadcast(cb:Function = null) {
        this.http.send('/hall/getBroadcast','POST',{},cb);
    }
    
    getHallBroad(cb:Function = null) {
        this.http.send('/hall/getHallBroad','POST',{},cb);
    }
    
    presetGold(g:number,cb:Function = null) {
        this.http.send('/hall/gold/preset_gold','POST',{gold:g},cb);
    }

    getBaccaratRoomsList(id:number,cb:Function = null) {
        this.http.send('/hall/getBaccaratroomsList','POST',{playId:id},cb);
    }

    setDeviceInfo(device:string,lan:string,cb:Function = null) {
        this.http.send('/hall/setDeviceInfo','POST',{DeviceType:device,language:lan},cb);
    }
}

//游戏阶段
var GAME_STAGE = {
    WAIT_START : -1, //等待开始
    GAME_READY : 0, //等待下一局
    WAIT_ROLL : 1, //等待roll点
    GAMING : 2 //游戏中
};