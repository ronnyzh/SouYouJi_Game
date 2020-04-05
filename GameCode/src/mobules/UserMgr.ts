/*
* name;
*/
class User {
    public exp: number;
    public coins: number = 0;
    public sourceMoney: number = 0;
    public sourceCurrency: string = 'RMB';
    public gems: number;
    public lv: number;
    public roomData: number;
    public gender: number = null;
    public ip: string;
    public sid: string;
    public userId: number = null;
    public name: string = null;
    public age: number = null;
    public presetGold: number = 0;
    // public imgUrl: string = 'http://47.106.144.135:9798/header/1.png';
    public imgUrl: string = 'ui://la8oslyoosvmbg';
    public exchangRate: number = null;
}
class UserMgr {
    private static _inst: UserMgr = null;
    public static get inst(): UserMgr {
        if (UserMgr._inst == null) {
            UserMgr._inst = new UserMgr();
        }
        return UserMgr._inst;
    }

    private _account: string = null;
    private _sign: string = null;
    public _token: string = null;
    public _info: User = new User();
    public oldGameMode: string = null;
    public oldGameType: string = null;

    constructor() {

    }

    public get userId():number {
        return this._info.userId;
    }

    public get exchangRate():number {
        return this._info.exchangRate;
    }

    public get name() {
        return this._info.name;
    }

    public get imgUrl() {
        return this._info.imgUrl;
    }

    public get gems() {
        return this._info.gems;
    }

    public get coins() {
        return this._info.coins;
    }

    public get sourceMoney() {
        return this._info.sourceMoney;
    }

    public get presetMoney() {
        return this._info.presetGold;
    }

    public get sourceCurrency() {
        return this._info.sourceCurrency;
    }

    public get money() {
        return Tools.inst.changeGoldToMoney(this._info.coins); 
    }

    public get ip() {
        return this._info.ip;
    }

    public get sid() {
        return this._info.sid;
    }

    public gameid2Data:Array<any> = [];
    public setLobbyGameData(data:any){
        this.gameid2Data = data; 
    }
    public get lobbyGameData() {
        return this.gameid2Data;
    }

    doLoginAsGuest(isTest:boolean=false) {
        var onAuth = function (data) {
            this.onLogin(data);
        }.bind(this);

        if(isTest){
            let index = location_random_account || Tools.inst.randomInt(0,TestAccounts.length-1);
            // console.log('index:'+index)
            let account = TestAccounts[index];
            if(location_search_account)account=location_search_account;
            HttpMgr.inst.loginEncryption(account, onAuth);
            return;
        }

        let account = bk.args['account'];
        if (account == null || account == '') {
            //account = Laya.LocalStorage.getItem('account');
            if (account == null || account == '') {
                account = (isTest ? 'test' : 'ping') + Tools.inst.randomInt(3,10);
                Laya.LocalStorage.setItem('account', account);
            }
        }
        HttpMgr.inst.login(account,(isTest ? 'aaaa8888' : 'ping'), onAuth);
        WC.show(ExtendMgr.inst.getText4Language('正在登陆中...'));
    }
    
    public lastAccount=''
    doLoginAsGuest2(account) {
        /*var onAuth = function (data) {
            this.onLogin(data);
        }.bind(this);*/
        this.lastAccount=account;
        HttpMgr.inst.loginEncryption(account, this.onLogin.bind(this));
    }

    relogin(){
        // MasterMgr.inst.switch('login',false,{relogin:true});
        Laya.timer.once(1500,this,function(){
            this.doLoginAsGuest2(this.lastAccount);
        });
    }

    onLogin(data) {
        HttpMgr.inst.getSource().sid = data.sid;
        // HttpMgr.inst.getSource().mid = data.mid;
        if(data['code']!=0){
            Alert.show(ExtendMgr.inst.getText4Language(data['msg'] || '登陆失败')).onYes(function(){
                window.location.reload(true);
            });
            return;
        }

        ExtendMgr.inst.clearParticle("0");
        ExtendMgr.inst.clearParticle("1");

        UIMgr.inst.add(RequestPage);

        var userData = data.userInfo;

        if (userData !== undefined) 
        {
            if (!userData.uid)
            {
                if (this._account && this._account.indexOf('wx_') == 0) 
                {
                    ExtendMgr.inst.preloadResources(function()
                    {
                        WC.hide();
                        Laya.LocalStorage.removeItem("wx_account");
                        Laya.LocalStorage.removeItem("wx_sign");
                    });
                    return;
                }
            }
            else 
            {
                HttpMgr.inst.setDeviceInfo(ExtendMgr.inst.getDevice(),ExtendMgr.inst.lan);

                Laya.timer.clearAll(this);
                Laya.Tween.clearAll(this);

                this._account = userData.account;
                this._info.userId = userData.uid;
                this._info.name = userData.name;
                this._info.imgUrl = userData['headImgUrl'];
                this._info.sid = data.sid;
                this._info.exchangRate = userData.exchangRate;
                this._info.sourceCurrency = userData.currency;

                //重连进房
                var enterGameInfo = data["gameInfo"];
                if(enterGameInfo != null)
                {
                    var gameId = enterGameInfo["gameid"];
                    var gameData = {
                        id : gameId,
                        sid : data.sid,
                        ip : enterGameInfo["ip"],
                        port : enterGameInfo["port"],
                        isParty: enterGameInfo['isParty']
                    };
                    //this.switchGameWithRes(gameId,gameData);
                    ExtendMgr.inst.preloadResources(this.switchGameWithRes.bind(this,gameId,gameData));
                    return;
                }
                else
                {
                    ExtendMgr.inst.preloadResources(function()
                    {
                        let last_select_gameId = Laya.LocalStorage.getItem(ExtendMgr.LastSelectGameIdKey);

                        if(last_select_gameId)
                        {
                            HttpMgr.inst.refreshGoldGameListh(function(datas)
                            {
                                if(datas['code']!=0)return;
                                
                                let serverStates = datas['data'].reduce(function(acc2, cur2){
                                    var gameid = cur2['gameid'];
                                    var state = cur2['serverState'];
                                    acc2[gameid] = state;
                                    return acc2;
                                } ,{});
                
                                if(!serverStates[last_select_gameId])
                                {
                                   Laya.LocalStorage.removeItem(ExtendMgr.LastSelectGameIdKey);
                                }
                                else
                                {
                                    let gameid2Data = datas['data'].reduce(function(acc, cur){
                                        var gameid = cur['gameid'];
                                        var data = cur['config'];
                                        data.map(function (d) {
                                            d['gameid'] = gameid;
                                        });
                                        acc[gameid] = data;
                                        return acc;
                                    } ,{});
                                    UserMgr.inst.setLobbyGameData(gameid2Data);
                                }
                                
                                MasterMgr.inst.switch('lobby');

                            }.bind(this),function(){
                                MasterMgr.inst.switch('lobby');
                            });
                        }
                        else
                        {
                            MasterMgr.inst.switch('lobby');
                        }
                    });
                }
            }
        }
        else
        {
            if(data['msg'])Alert.show(ExtendMgr.inst.getText4Language(data['msg'])).onYes(function(){
                window.location.reload(true);
            });
        }
    }
    
    switchGameWithRes(gameID,data){        
        var protoPath = ResourceMgr.PROTO_PATH;
        var res = [
            { url: protoPath+"mahjong.proto", type :Loader.TEXT},
            { url: protoPath+"gold.proto", type :Loader.TEXT}
        ];
        Laya.loader.load(res, Handler.create(this, this.switchGames.bind(this,gameID,data)));
    }

    switchGames(gameID,data)
    {
        var gameid = parseInt(gameID);
        this.addBackground(gameid,Handler.create(this,()=>
        {
            MasterMgr.inst.switch('game'+gameID,false,data);
        }));
    }

    addBackground(gameid,cb?):void
    {
        var background = Laya.stage.getChildByName(minigame_background_mark) as laya.ui.Image;
        if(!background)
            background = Laya.stage.addChildAt(new laya.ui.Image(),0) as laya.ui.Image;
        ExtendMgr.inst.setBackgroundfull(minigame_background_mark,ResourceMgr.RES_PATH+"bg/"+ExtendMgr.inst.background_map[gameid],background,cb);
    }

    login(account, sign) {
        this._account = account;
        this._sign = sign;
        HttpMgr.inst.login(account, sign, this.onLogin.bind(this));

        Laya.LocalStorage.setItem('account', account);
        Laya.LocalStorage.setItem('password', sign);
    }
    
    refreshCashes_bak(cb,failcb) {
        HttpMgr.inst.refreshPlayerData(function (datas) 
        {            
            if(datas.code!=0){
                if(datas.msg)failcb(datas.msg);//Alert.show(datas.msg);
                return;
            }
            var data = datas["data"];
            this._info.gems = data['roomCard'];
            this._info.coins = data['gold'];

            if (cb) {
                cb();
            }
        }.bind(this));
    }
    
    refreshCashes(cb,failcb) 
    {        
        if(!TestMgr.IS_REAL_ACCOUNT)
        {
            this.refreshCashes_bak(cb,failcb);
            return;
        }
        HttpMgr.inst.refreshPlayerDataReal(function (datas)
        {
            if(datas.code!=0)
            {
                if(datas.message)failcb(datas.message);
                return;
            }
            
            // this._info.coins = Tools.inst.changeMoneyToGold(datas['balance']);
            this._info.coins = (datas['toBalance'] || 0);
            this._info.sourceMoney = (datas['sourceBalance'] || 0);
            this._info.sourceCurrency = (datas['sourceCurrency'] || '?');
            //this.coinSwitch = (datas['switch'] || null);

            if(datas['preset_gold'])
                this._info.presetGold = datas['preset_gold'];
            else
                this._info.presetGold = 0;

            if (cb)cb();
            
        }.bind(this));
    }

    enterRoom(roomId, callback) {
        var onEnter = function (data) {
            WC.hide();
            if(data.ip){
                if(callback)callback(data);
            }
            else if(data.msg)
                Alert.show(ExtendMgr.inst.getText4Language(data.msg));
        }.bind(this);

        //HttpMgr.inst.joinRoom(roomId, onEnter);
        
        /**/
        HttpMgr.inst.getGameID(roomId,function(data){
            if(data.gameid)
                HttpMgr.inst.joinRoom(roomId,onEnter);
            else if(data.msg){
                WC.hide();
                Alert.show(ExtendMgr.inst.getText4Language(data.msg));
            }
        }.bind(this));/**/
    }

    returnToLobby(){        
        NoticeView.hide();
        Tools.inst.clearAllTimeout();
        if(NetHandlerMgr.netHandler!=null && NetHandlerMgr.netHandler.disconnect!= null)
        {
            NetHandlerMgr.netHandler.disconnect();
        }
        MasterMgr.inst.switch('lobby');
    }
    
    refreshSession(){
        HttpMgr.inst.refreshSession(function(data){
        }.bind(this));
    }
}