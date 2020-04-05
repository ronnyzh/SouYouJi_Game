
class HallScene extends Scene
{
    getRes(){
        var protoPath = ResourceMgr.PROTO_PATH;
        return [
            { url: ExtendMgr.inst.uipath+"/Hall.fui", type: Loader.BUFFER },
            { url: ExtendMgr.inst.uipath+"/Hall@atlas0.png", type: Loader.IMAGE },
            { url: protoPath+"mahjong.proto", type :Loader.TEXT},
            { url: protoPath+"gold.proto", type :Loader.TEXT}
        ];
    }

    start(){
        fairygui.UIPackage.addPackage(ExtendMgr.inst.uipath+'/Hall');
        UIMgr.inst.add(HallPage);

        SoundMgr.playMusic('bg.mp3');
    }
}

class HallPage extends LobbyPage
{
    constructor(){
        super("Hall", "HallPage2",UILayer.GAME);        
        Laya.stage.on(Laya.Event.KEY_DOWN, this, this.onKeyDown);
    }
    
    private gemsText:fairygui.GLabel;
    private moneyText:fairygui.GLabel;
    private moneyMark:fairygui.GLabel;
    private take_moneyText:fairygui.GLabel;
    private take_moneyMark:fairygui.GLabel;
    private loadingC:fairygui.Controller;

    private glabelVersion:fairygui.GLabel;
    private gList:fairygui.GList;
    //private gsubList:fairygui.GList;
    private particles_right:any;
    private particles_left:any;

    lastRequestNoticeTime=0; 
    delayRequestNoticeTime=0;

    onCreated()
    {
        var view = this._view;

        this.glabelVersion = view.getChild('Txt_version').asLabel;
        this.glabelVersion.text = MasterSettings.masters.lobby.name+" "+ExtendMgr.inst.VersionStr+":"+MasterSettings.masters.lobby.version;
        
        this.gemsText = view.getChild('gems').asLabel;
        this.moneyText = view.getChild('money').asLabel;
        this.moneyMark = view.getChild('moneyMark').asLabel;
        
        var headIcon = view.getChild('imgHead').asLoader;
        Tools.inst.changeHeadIcon(UserMgr.inst._info.imgUrl,headIcon);

        var nick_name_max_show = 12;
        var user_nick_name = UserMgr.inst._info.name.length>nick_name_max_show?UserMgr.inst._info.name.substring(UserMgr.inst._info.name.length-nick_name_max_show-1):UserMgr.inst._info.name;
        Tools.inst.SetNickNameAfter(view.getChild('name').asLabel,UserMgr.inst._info.name); //'0_vd012315_demo621'
        
        var setBtn = view.getChild('setHeadBtn').asButton;
        setBtn.onClick(this,function(){
            UIMgr.inst.popup(UI_Portrait);
            //UIMgr.inst.popup(UI_PresetGoldSetter);
        });

        var takeMBtn = view.getChild('btn_takeMoney').asButton;
        var ctrl = view.getController('bringMoney');
        if(ctrl)
        {
            view.getController('bringMoney').selectedIndex = TestMgr.IS_SHOW_TAKE_MONEY?(AllFundVisible()?1:2):0;
        }
        else
        {
            view.getChild('take_money_group').visible = TestMgr.IS_SHOW_TAKE_MONEY;
            takeMBtn.visible = TestMgr.IS_SHOW_TAKE_MONEY;
        }
        this.take_moneyMark = view.getChild('take_moneyMark').asLabel;
        this.take_moneyText = view.getChild('take_money').asLabel;
        if(TestMgr.IS_SHOW_TAKE_MONEY)
        {
            takeMBtn.onClick(this,function(){
                UIMgr.inst.popup(UI_PresetGoldSetter);
            });
        }
        
        var adSpark = view.getChild('game449').asCom; //ad_spark
        adSpark.onClick(this,this.onBtnClicked,[adSpark]);

        if(!laya.renders.Render.isWebGL)
            view.getChild('cacheObject').displayObject.cacheAs = 'bitmap';
        
        EventMgr.on('onAccountError',this,function()
        {
            Laya.timer.clear(this,this.refreshCashes);    
        });

        EventMgr.on("head_changed",this,function(data){
            if(!data)return;
            try {
                var url = ((data['list'] || [])[0] || [])['url'];
                if(!url)return;
                UserMgr.inst._info.imgUrl = url;
                Tools.inst.changeHeadIcon(url,headIcon);
                //headIcon.url = url;
            } catch (error) {
                console.log(error)
            }
        }.bind(this));

        var url = ResourceMgr.RES_PATH+'bg/hallBg.jpg';
        Tools.inst.changeBackground(url,this._view.getChild('bg').asLoader);
        Tools.inst.changeBackground(url,this._view.getChild('bg1').asLoader);
        url = ResourceMgr.RES_PATH+'bg/hallBg2.jpg';
        Tools.inst.changeBackground(url,this._view.getChild('bg2').asLoader);
        //Tools.inst.changeBackground(url,this._view.getChild('bg3').asLoader);
        
        var particle_star = this._view.getChild('Par_star').asLoader;
        var ypos = Laya.stage.height * 0.5;
        //ExtendMgr.inst.createParticle2Fairygui("0","bgstar_bottom.part",Laya.stage.width * 0.5,Laya.stage.height - 20,particle_star);
        this.createParticles(ypos,particle_star);
        /*
        var masker:UserIconMasker = ExtendMgr.inst.createUserIconMasker(this._view.getChild('Pln_AdBoard').asCom,"mask",0,0);
        masker.radius = 200;
        masker.updateMaskPieAngle(50,260);
        */
        this.refreshCashes();
        this.refreshGoldGameListh();

        this.gList = view.getChild('sub_game_list').asList;
        for(var i = 0; i < this.gList.numChildren; ++i)
        {
            var child = this.gList.getChildAt(i);
            var btn = child.asButton;
            if(btn != null)
            {
                if(TestMgr.IS_PUBLIC)
                {
                    if(isPublicLock(btn.name))
                    {
                        btn.visible = false;
                        continue;
                    }
                }
                btn.getChild('Pic_hot').visible = ExtendMgr.inst.isShowPicHot(btn.name);
                btn.onClick(this,this.onBtnClicked,[btn]);
            }
        }

        this._view.getController('pagecodeC').selectedIndex = this.gList.numChildren <= 8?1:0; //1;//

        this.subListPage = view.getChild('game_sub_list').asList;
        let ludan = this.subListPage.getChild('list_ludan');
        if(ludan)
        {
            this.subListLudan = ludan.asList;
        }
            
        for(var i = 0; i < this.subListPage.numChildren; ++i)
        {
            var child = this.subListPage.getChildAt(i);
            var btn = child.asButton;
            if(btn != null)
            {
                btn.onClick(this,this.onBtnClicked2,[btn]);
                if(i == 0)
                {
                    btn.getChild('free').visible = true;
                }
            }
        }
        
        var btn_start = view.getChild('btn_start').asButton;
        btn_start.onClick(this,this.onFastStart);
        
        var gamePageC = this._view.getController('gamePageC');
        var btn_return = view.getChild('btn_return').asButton;
        btn_return.onClick(this,function()
        {
            gamePageC.selectedIndex = 0;
            this.startParticles();
            this._view.getTransition('t1').play();
            ExtendMgr.inst.stopFlashGamesublist(this.subListPage);
            ExtendMgr.inst.startHotAnima(this.gList)

            if(this.waybill) { this.waybill.destroy(); }
            
            this.glabelVersion.text = MasterSettings.masters.lobby.name+" "+ExtendMgr.inst.VersionStr+":"+MasterSettings.masters.lobby.version;
        }.bind(this));
        
        this.loadingC = view.getController('loading');

        var btn_set = view.getChild('btn_set').asButton;
        btn_set.onClick(this,function()
        {
            UIMgr.inst.popup(UI_Setting);
        });
        
        var btn_rule = view.getChild('btn_rule').asButton;
        btn_rule.onClick(this,function()
        {
            var rule = UIMgr.inst.popup(UI_Rules) as UI_Rules;
            rule.refreshData(this._chooseGameIDStr);
        });
        
        var btn_history = view.getChild('btn_history').asButton;
        btn_history.onClick(this,function()
        {
            var obj = UIMgr.inst.popup(UI_History) as UI_History;
            if(gamePageC.selectedIndex == 0)
                obj.refreshList();
            else
                obj.refreshGameList(this._chooseGameID);
        });
        
        var btn_backpage = view.getChild('btn_backpage').asButton;
        btn_backpage.visible = (location_return_url && location_return_url.length>0);
        if(btn_backpage.visible)
        {
            btn_backpage.onClick(this,function()
            {
                Alert.show(ExtendMgr.inst.getText4Language('是否跳转到游戏外部入口？'),true).onYes(function()
                {
                    //Laya.Browser.window.href = location_return_url;
                    //window.location.href = location_return_url;
                    callJsOpenWindow(location_return_url);
                }.bind(this));
            });
        }

        this.moneyMark.text = UserMgr.inst.sourceCurrency+':';
        this.take_moneyMark.text = UserMgr.inst.sourceCurrency+':';

        Laya.stage.on(UI_PresetGoldSetter.ON_SET_PRESET_MONEY,this,this.refreshCashes);

        Laya.timer.loop(5000,this,this.refreshCashes);        

        Laya.timer.once(100,this,function()
        {
            ExtendMgr.inst.startHotAnima(this.gList);
        });  

        var testID = Laya.LocalStorage.getItem(ExtendMgr.LastSelectGameIdKey);
        var gameid2Data = UserMgr.inst.lobbyGameData;
        if(testID && gameid2Data)
        {
            this.gameid2Data = gameid2Data;
            this.showRoomList(parseInt(testID),'game'+testID);
        }
    }

    refreshCashes()
    {
        UserMgr.inst.refreshCashes(function()
        {
            this.gemsText.text = UserMgr.inst.money;
            this.moneyText.text = UserMgr.inst.sourceMoney;//Tools.inst.changeGoldToMoney(UserMgr.inst.sourceMoney);
            this.moneyMark.text = UserMgr.inst.sourceCurrency+':';
            this.take_moneyText.text = UserMgr.inst.presetMoney;
            this.take_moneyMark.text = UserMgr.inst.sourceCurrency+':';
        }.bind(this),function(msg)
        {
            Laya.timer.clearAll(this);
            Alert.show(ExtendMgr.inst.getText4Language(msg)).onYes(function()
            {
                window.location.reload(true);
            });
        });
        
        /**/
        if(Date.now()-this.lastRequestNoticeTime>this.delayRequestNoticeTime)
        {
            this.lastRequestNoticeTime = Date.now();
            HttpMgr.inst.getHallBroad(function(data){
                this.delayRequestNoticeTime = data['requestPerSec']*1000;
                NoticeView.addNotices(data['broadcasts'])
            }.bind(this));

            HttpMgr.inst.refreshGoldGameListh(function(datas)
            {
                if(datas['code']!=0)
                {
                    Alert.show(ExtendMgr.inst.getText4Language(datas['msg'])).onYes(function()
                    {
                        window.location.reload(true);
                    });
                    return;
                }
                        //console.log(datas);
                this.gameid2Data = datas['data'].reduce(function(acc, cur)
                {
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

                UserMgr.inst.setLobbyGameData(this.gameid2Data);

                if(this._view != null)
                {
                    var gamePageC = this._view.getController('gamePageC');
                    if(gamePageC.selectedIndex == 0)
                    {
                        ExtendMgr.inst.refreshGameListMembersNum(this._view.getChild('sub_game_list').asList,this.gameid2Data,this.serverStates);
                    }
                    else
                    {
                        var gameId = this._chooseGameID;
                        var masterObj = MasterSettings.masters['game'+gameId];
                        this.glabelVersion.text = masterObj.name+" "+ExtendMgr.inst.VersionStr+":"+masterObj.version;
                        this.refreshRoomList(this.gameid2Data[gameId],gameId);
                    }
                }
            }.bind(this),this.onHallHttpFail);
        }
    }

    onBtnClicked(sender:fairygui.GObject)
    {
        if(sender.name == "")
            return;
            
        if(ExtendMgr.inst.checkStartGame(sender.name,this.loadingC))
        {
            return;
        }

        ExtendMgr.inst.startflashGamesublist(this.subListPage);
        ExtendMgr.inst.stopHotAnima(this.gList);
        
        this.stopParticles();

        this._view.getTransition('t1').stop();

        var gameid = parseInt(sender.name.replace('game',""));
        this.showRoomList(gameid,sender.name);

        this.glabelVersion.text = MasterSettings.masters[sender.name].name+" "+ExtendMgr.inst.VersionStr+":"+MasterSettings.masters[sender.name].version;
    }

    switchGame(gameID,data)
    {
        this.loadingC.setSelectedPage('show');
        this._view.getChild('bg1').visible = false;
        //this._view.getChild('bg3').visible = false;
        this.destroyParticles();
        this.view.getTransition('t0').stop();
        var gameid = parseInt(gameID.replace('game',""));
        this.addBackground(gameid);
        Laya.timer.frameOnce(20,this,function()//80
        {
            ExtendMgr.inst.reloadSounds(gameid);
            MasterMgr.inst.switch(gameID,false,data);
        }.bind(this));    
    }

    enterGame(data){
        ExtendMgr.inst.stopFlashGamesublist(this.subListPage);
        this.loadingC.setSelectedPage('show');
        this.stopParticles();
        super.enterGame(data);
    }

    switchGameFail(data){
        this.loadingC.setSelectedIndex(0);
        this.subListPage.getController("select").selectedIndex = 0;
        super.switchGameFail(data);
    }

    refreshRoomList(datas=[],gameId = 0)
    {
        var subList = this.subListPage;
        var arr = this.gameid2Data[gameId.toString()];
        for(var i = 0; i < subList.numChildren; ++i)
        {
            var child = subList.getChildAt(i).asButton;
            var data = datas[i];
            if(child != null && child.name.indexOf('btn')>=0)
            {
                child.visible = false;
                if(!data)continue;

                var txtDF = child.getChild('txtDF').asLabel;
                var txtRF = child.getChild('txtRF').asLabel;

                var need = data['need'][0];
                need = Tools.inst.changeGoldToMoney(need);

                if(gameId == 565 )
                {
                    var gold = data['baseScore'];
                    var gold_2: number = parseFloat((parseFloat(gold)/2).toFixed(2));
                    txtDF.text='D'+Tools.inst.changeGoldToMoney(gold_2) +'/'+ Tools.inst.changeGoldToMoney(gold);

                    if(data['cap'])
                    {
                        var cap = Tools.inst.changeGoldToMoney(data['cap']);
                        txtRF.text='V '+arr[i].online+'  R ['+need+']['+cap+']';
                    }
                    else
                        txtRF.text='V '+arr[i].online+'  R '+need;
                }
                else
                {
                    txtDF.text='D'+ Tools.inst.changeGoldToMoney(data['baseScore']);
                    txtRF.text='V '+arr[i].online+'  R '+need;
                }
                
                child.visible = true;
            }
        }
    }

    //Particles//////////////////////////////////////////////////////////////////////////////////////////////
    createParticles(ypos,particle_star)
    {
        this.particles_right = ExtendMgr.inst.createParticle2Fairygui("1","bgstar_r.part",0,ypos,particle_star);
        this.particles_left = ExtendMgr.inst.createParticle2Fairygui("2","bgstar_l.part",Laya.stage.width,ypos,particle_star);
    }

    startParticles()
    {
        if(this.particles_right) this.particles_right.emitter.start();
        if(this.particles_left) this.particles_left.emitter.start();
    }

    stopParticles()
    {
        if(this.particles_right) this.particles_right.emitter.stop();
        if(this.particles_left) this.particles_left.emitter.stop();
    }

    destroyParticles()
    {
        if(this.particles_right) this.particles_right.destroy();
        if(this.particles_left) this.particles_left.destroy();
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////

    onDispose()
    {
        Tween.clearAll(this.view.getChild('n26')); //loading anima
        Tween.clearAll(this.view.getChild('n27')); //loading anima
        Laya.timer.clearAll(this);
        Laya.stage.off(UI_PresetGoldSetter.ON_SET_PRESET_MONEY,this,this.refreshCashes);
        EventMgr.offAll('onAccountError');
        EventMgr.offAll('head_changed');
        NoticeView.hide();
        if(this.waybill) 
        { 
            this.waybill.destroy();
            this.waybill = null; 
        }
        super.onDispose();
    }
}