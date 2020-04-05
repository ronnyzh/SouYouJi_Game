class GameNetMgr{
    private static _inst:GameNetMgr = null;

    private lastSio:any = null;

    public static get inst():GameNetMgr{
        if(GameNetMgr._inst == null){
            GameNetMgr._inst = new GameNetMgr();
        }
        return GameNetMgr._inst;
    }

    constructor(){
        bk.registerUpdater(this,this.update);
        this.start();
    }

    backToHall(){
        //if(bk.masterSettings.entry_scene){
        //    bk.utils.loadScene(bk.masterSettings.entry_scene);
        //}
        //else{
        //    bk.switchMaster('lobby_platform');
        //}
    }

    start() {
        var agent = new NetAgent('gamenetmgr',true);
        bk.net.addAgent(agent);
        var self = this;

        agent.addHandler("disconnect", function (data) {
            bk.emit('disconnect');
            /*
            if (bk.room.roomId === null) {
                // bk.utils.loadScene("hall_" + UserMgr.inst.oldGameType);

                if (bk.room.matchExitCly) {
                    cc.director.loadScene("cfx_test_scenes");
                }
                else {
                    self.backToHall();
                }
            }
            else {
                if (bk.room.isOver === false) {
                    UserMgr.inst.oldRoomId = bk.room.roomId;
                    bk.emit("disconnect");
                }
                else {
                    bk.room.roomId = null;
                }
            }
            */
        });

        agent.addHandler("login_result", function (data) {
            //console.log(data);
            if (data.errcode === 0) {
                var dat = data.data;
                if(dat){
                    RoomMgr.inst.onLogin(dat);
                }
            }
            else {
                console.log(data.errmsg);
                self.backToHall();
            }
        });

        // var data = { user_id: item.userId, rank: (i + 1), total_players: this.totalRooms * 4 };
        // 进入房间
        agent.addHandler("login_finished", function (data) {
            //console.log("login_finished");
            var scene = MasterMgr.current.setting.game_scene;
            if(scene){
                WC.show('正在加载游戏场景...');
                SceneMgr.inst.replace(scene);
                bk.net.ping();
            }
            bk.emit('login_finished');
        });
    }

    connectGameServer(data) {
        RoomMgr.inst.dissoveData = null;
        bk.net.set('http://' + data.ip,data.port);
        //console.log(data.ip,data.port);
        var self = this;

        var onConnectOK = function () {
            RoomMgr.inst.isOver = false;
            //console.log("onConnectOK");
            var sd = {
                token: data.token,
                roomid: data.roomid,
                time: data.time,
                sign: data.sign,
            };
            bk.net.send("login", sd);
        };

        var onConnectFailed = function () {
            //console.log("failed.");
            WC.hide();
        };
        var tips = "正在匹配服务器...";
        if (UserMgr.inst.oldGameMode == 'match') {
            tips = "正在进入比赛";
        }
        WC.show(tips);
        bk.net.connect(onConnectOK, onConnectFailed);
    }

    reset() {
        bk.emit("game_net_re_connect");
    }

    //测试服务器是否可达
    testServerOn () {
        //console.log('testServerOn');
        bk.net.test(function (ret) {
            //console.log('test return - ' + ret);
            if (ret) {
                this.reset();
                this.doReconnect();
            } else {
                setTimeout(this.testServerOn.bind(this), 3000);
            }
        }.bind(this));
    }

    doReconnect(){
        var self = this;
        var roomId = RoomMgr.inst.roomId;
        if (roomId !== null) {
            var gameType;
            var gameMode = UserMgr.inst.oldGameMode;
            let entry_scene = MasterMgr.current.setting.entry_scene;
            let gameType = MasterMgr.current.setting.id;
            UserMgr.inst.enterRoom(roomId, function (ret) {
                if (ret.errcode !== 0) {
                    var showstring = ""
                    if(UserMgr.inst.oldGameMode && UserMgr.inst.oldGameMode == "match"){
                        showstring = "比赛已结束！";
                    }else{
                        showstring = "房间已关闭！"
                    }
                    Alert.show(showstring).onYes(function(){
                        self.backToHall();
                    });
                }
                else{

                }
            }.bind(this));
        }
    }

    //called every frame, uncomment this function to activate update callback
    update (dt) {
        var isNetTurnOff = this.lastSio && !bk.net.getSio();
        if(isNetTurnOff && MasterMgr.current.isPlaying()){
            this.testServerOn();
            WC.show("正在重连");
        }
        
        this.lastSio = bk.net.getSio();
    }
}
