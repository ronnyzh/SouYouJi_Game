/*
* name;
*/
class LobbyPage extends Page{
    private cashRefresher:number = null;
    constructor(pkg="Lobby",comp="PageLobby",layer){
        super(pkg,comp,UILayer.GAME);
        Laya.stage.on(Laya.Event.KEY_DOWN, this, this.onKeyDown);
    }

    public gameid2Data:Array<any> = [];
    public serverStates:Array<boolean> = [];
    public _useData:Array<any> = [];
    public _chooseGameIDStr:string;
    public _chooseGameID:number;

    public subListPage:fairygui.GComponent;
    public subListLudan:fairygui.GList;
    public layoutTitle:LayoutHallTitle;

    public waybill:WaybillPage;

    onCreated()
    {
        this.layoutTitle = new LayoutHallTitle(this._view.getChild('layout_hall_title').asCom);
        //new LayoutBtns(this._view.getChild('layout_btns').asCom);

        this.refreshCashes();
        this.refreshGoldGameListh();       

        var gameList = this._view.getChild('sub_game_list').asCom;
        for(var i = 0; i < gameList.numChildren; ++i){
            var child = gameList.getChildAt(i);
            var btn = child.asButton;
            if(btn != null)
            {
                btn.onClick(this,this.onBtnClicked,[btn]);
            }
        }
        
        this.subListPage = this._view.getChild('game_sub_list').asCom;
        this.subListLudan = this.subListPage.getChild('list_ludan').asList;
        for(var i = 0; i < this.subListPage.numChildren; ++i){
            var child = this.subListPage.getChildAt(i);
            var btn = child.asButton;
            if(btn != null){
                btn.onClick(this,this.onBtnClicked2,[btn]);
            }
        }
    }

    refreshGoldGameListh(){
        HttpMgr.inst.refreshGoldGameListh(function(datas){
            if(datas['code']!=0)return;
            
            this.gameid2Data = datas['data'].reduce(function(acc, cur){
                var gameid = cur['gameid'];
                var data = cur['config'];
                data.map(function (d) {
                    d['gameid'] = gameid;
                });
                acc[gameid] = data;
                return acc;
            } ,{});

            this.serverStates = datas['data'].reduce(function(acc2, cur2){
                var gameid = cur2['gameid'];
                var state = cur2['serverState'];
                acc2[gameid] = state;
                return acc2;
            } ,{});
            //                data['serverState'] = cur['serverState']; //将serverState 放入 data中

            UserMgr.inst.setLobbyGameData(this.gameid2Data);
            ExtendMgr.inst.refreshGameListMembersNum(this._view.getChild('sub_game_list').asList,this.gameid2Data,this.serverStates);
            // var testID = Laya.LocalStorage.getItem('last_select_gameId');
            // if(testID){
            //     this.showRoomList(testID,'game'+testID);
            // }
        }.bind(this),this.onHallHttpFail);
    }

    onHallHttpFail(reason)
    {
        if(this._view!= null)
        {
            var gamePageC = this._view.getController('gamePageC');
            if(gamePageC != null)
            {
                if(gamePageC.selectedIndex == 2)
                {
                    Alert.show(ExtendMgr.inst.getText4Language(reason));
                    gamePageC.selectedIndex = 1;
                    this._view.getController('loading').selectedIndex = 0;
                    this._view.getChild('bg1').visible = true;
                    this._view.getChild('bg3').visible = true;
                }
            }
        }
    }

    onBtnClicked(sender:fairygui.GObject){
        switch (true){
            case(sender.name == 'game556'):
                this.showRoomList(556,'game556');
                break;
            case(sender.name == 'game445'):
                this.showRoomList(445,'game445');
                break;
            case(sender.name == 'game555'):
                this.showRoomList(555,'game555');
                break;
            case(sender.name == 'game559'):
                this.showRoomList(559,'game559');
                break;
            case(sender.name == 'game560'):
                this.showRoomList(560,'game560');
                break;
            case(sender.name == 'game557'):
                this.showRoomList(557,'game557');
                break;
        }
    }

    onBtnClicked2(sender:fairygui.GObject){
        var gamePageC = this._view.getController('gamePageC');

        if(sender.name == 'btn_return'){
            gamePageC.selectedIndex = 0;
            return;
        }
        
        if(sender.name == 'btn_start'){
            this.onFastStart();
            return;
        }

        for(var i=0;i<6;i++){
            var oneData = this._useData[i];
            if(sender.name == 'btn_s'+i && oneData){
                // UIMgr.inst.popup(UI_JoinGame);
                this.onSelectRoom(oneData)
                return;
            }
        }
    }
    
    showRoomList(gameId:number ,masterID:string) 
    {
        if (!this.gameid2Data || this.gameid2Data.length == 0 || gameId === null )return ;
        var data = this.gameid2Data[gameId];
        if(!data)return Alert.show(ExtendMgr.inst.NotGameData);
        
        this._useData = data;
        this._chooseGameIDStr = masterID;
        this._chooseGameID = gameId;

        var txtGameName = this._view.getChild('txtGameName');
        if(txtGameName)
            txtGameName.asLabel.text = ExtendMgr.inst.getText4Language(MasterSettings.masters['game'+gameId].name);  //data[0]['gameName'] || '';
        
        Laya.LocalStorage.setItem(ExtendMgr.LastSelectGameIdKey, ''+gameId);
        
        this.refreshRoomList(data,gameId);
        
        var gamePageC = this._view.getController('gamePageC');
        gamePageC.selectedIndex = 1;
        
        //lu dan function
        var page = getGameSubPageType(gameId);
        this.subListPage.getController('page').selectedIndex = page;
        
        if(page == 1)
        {
            if(this.waybill == null)
            {
                this.waybill = new WaybillPage();
                this.waybill.onCreate(this.subListLudan,this.gameid2Data[gameId.toString()]);
                this.waybill.onClickEnterGame = function (level,roomId)
                {
                    this._useData[level]['roomId'] = roomId;
                    this.onSelectRoom(this._useData[level]);
                }.bind(this);
            }
            else
            {
                this.waybill.refreshLeftRoomList(this.gameid2Data[gameId.toString()]);
            }
        }

        this._view.getController('showQuickplay').selectedIndex = page;
    }

    refreshRoomList(data,gameId){}

    onFastStart()
    {
        if(this._view.getController('showQuickplay').selectedIndex == 1)
        {
            return;
        }

        var coins = Tools.inst.changeMoneyToGold(UserMgr.inst.sourceMoney);
        var userGold:any = coins;
        if(UserMgr.inst.presetMoney > 0)
        {
            userGold = UserMgr.inst.presetMoney || 0;
            if(UserMgr.inst.presetMoney>coins)
            {
                userGold = coins;
            }
        }

        if(userGold && this._useData)
        {
            var data = this._useData.concat();
            var i = Math.min(5,data.length);
            while(i--)
            {
                var oneData = data[i];
                var need = oneData['need'];
                var min = Tools.inst.changeMoneyToGold(Tools.inst.changeGoldToMoney(need[0]));
                //var max = need[1] ? parseInt(need[1]) : null;
                if(userGold >= min /*&& (!max || max && userGold <= max)*/)
                {
                    this._view.getController('gamePageC').selectedIndex = 2;
                    this.enterGame(oneData);
                    return;
                }
            }
        }
        Alert.show(ExtendMgr.inst.NotGameData);
    }

    onSelectRoom(oneData)
    {
        var need = oneData['need'];
        var coins = Tools.inst.changeMoneyToGold(UserMgr.inst.sourceMoney);
        var gold = coins || 0;
        if(UserMgr.inst.presetMoney > 0)
        {
            gold = UserMgr.inst.presetMoney || 0;

            if(UserMgr.inst.presetMoney>coins)
            {
                gold = coins;
            }
        }

        var need_money = Tools.inst.changeMoneyToGold(Tools.inst.changeGoldToMoney(need[0]));
        if(gold < need_money)
        {
            Alert.show(ExtendMgr.inst.NotEnoughMoney);
            return;
        }

        this._view.getController('gamePageC').selectedIndex = 2;
        this.enterGame(oneData);
    }

    addBackground(gameid,cb?):void
    {
        var background = Laya.stage.getChildByName(minigame_background_mark) as laya.ui.Image;
        if(!background)
            background = Laya.stage.addChildAt(new laya.ui.Image(),0) as laya.ui.Image;
        ExtendMgr.inst.setBackgroundfull(minigame_background_mark,ResourceMgr.RES_PATH+"bg/"+ExtendMgr.inst.background_map[gameid],background,cb);
    }

    enterGame(data0)
    {    
        this.switchGame(this._chooseGameIDStr,data0);
    }

    switchGame(gameID,data)
    {
        var gameid = parseInt(gameID.replace('game',""));
        this.addBackground(gameid,Handler.create(this,()=>
        {
            MasterMgr.inst.switch(gameID,false,data);
        }));
    }

    switchGameFail(data)
    {
        this._view.getController('gamePageC').selectedIndex = 1;
        this._view.getChild('bg1').visible = true;
        this._view.getChild('bg3').visible = true;

        if(data.code==-4){
            Alert.show(ExtendMgr.inst.getText4Language(data.msg)).onYes(function(){
                MasterMgr.inst.switch('login')
            });
        }
        else if(data.code==100405){
            Alert.show(ExtendMgr.inst.SwitchGameFail1,true).onYes(function(){
                var lastData=data['data'];
                var gameData = {
                    id: lastData["gameid"],
                    sid: UserMgr.inst.sid,
                    ip: lastData["ip"],
                    port: lastData["port"],
                    isParty: true
                };
                this.switchGame('game'+gameData.id,gameData);
            }.bind(this));
        }
        else
            Alert.show(ExtendMgr.inst.getText4Language(data.msg) || ExtendMgr.inst.SwitchGameFail2);
    }
    
    checkJoinParty(){
        var selfFunc = arguments.callee.bind(this);
        HttpMgr.inst.checkJoinPartyGold(function(data){
            //console.log('checkJoinParty',data)            
            if(data.code==0)
            {
                if(data["gameid"] != null) 
                {
                    var gameData = {
                        id: data["gameid"],
                        sid: UserMgr.inst.sid,
                        ip: data["ip"],
                        port: data["port"],
                        isParty: data["isParty"],
                    };
                    this.switchGame(this._chooseGameIDStr,gameData);
                }
                else
                {
                    Tools.inst.setTimeout(selfFunc, 1000);
                }
            }
            else
                this.switchGameFail(data);
        }.bind(this));
    }

    refreshCashes(){
        UserMgr.inst.refreshCashes(function(){
            this.layoutTitle.refreshCashes();
        }.bind(this),function(msg)
        {
            Laya.timer.clearAll(this);
            Alert.show(ExtendMgr.inst.getText4Language(msg)).onYes(function()
            {
                window.location.reload(true);
            });
        });
    }

    onDispose()
    {
        Laya.stage.off(Laya.Event.KEY_DOWN, this, this.onKeyDown);
        super.onDispose();
    }

    onKeyDown(e: Event): void {
        if(TestMgr.IS_REAL_ACCOUNT)return;
        var keyCode: number = e["keyCode"];
	    var Keyboard = Laya.Keyboard;
        switch(keyCode){
			case Keyboard.NUMBER_0:
                //console.log(UserMgr.inst.sid)
                // if(this.netHandler)this.netHandler.disconnect();
                break;
			case Keyboard.NUMBER_1:
                /*HttpMgr.inst.sendGMSet(30000,function(){
                    this.refreshCashes();
                }.bind(this));*/
                NoticeView.show('正在XXX?');
                // NoticeView.addNotices([{content:'正在....?'}]);
                break;
			case Keyboard.NUMBER_2:
                NoticeView.hide();
                break;
			case Keyboard.NUMBER_3:
                HttpMgr.inst.getBroadcast(function(data){
                    console.log(data)
                }.bind(this));
                break;
			case Keyboard.NUMBER_4:
                HttpMgr.inst.getHallBroad(function(data){
                    console.log(data)
                }.bind(this));
                break;
            default:
                console.log(keyCode)
                break;
                
        }
    }
}