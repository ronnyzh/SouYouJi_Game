class NetConnection{
    private ip:string = '';
    private sio:any = null;
    private lastRecieveTime:number = null;
    private lastSendTime:number = null;
    private delayMS:number = null;
    private agents:Array<NetAgent> = [];
    private timerPing:number = -1;
    private timerTimeout:number = -1;
    private crypto:EmptyCrypto = null;
    private onEventShowBind:Function = null;
    private http:HTTP = null;
    constructor(crypto:EmptyCrypto = null){
        if(!crypto){
            crypto = new EmptyCrypto();
        }
        this.crypto = crypto;
        this.onEventShowBind = this.onEventShow.bind(this);
    }

    set(addr:string,port:number){
        this.ip = addr + ':' + port;
        var httpheader = '';
        if(addr.indexOf(httpheader) == -1){
            httpheader = 'http://';
        }
        this.http = new HTTP(httpheader + addr + ':' + port,'text');
    }

    addAgent(agent:NetAgent){
        var idx = this.agents.indexOf(agent);
        if(idx != -1){
            return;
        }
        this.agents.push(agent);
    }

    removeAgent(agent){
        var idx = this.agents.indexOf(agent);
        if(idx != -1){
            this.agents.splice(idx,1);
        }
    }

    clearAgent(agent){
        var arr = [];
        for(var i = 0; i < this.agents.length; ++i){
            let agent = this.agents[i];
            if(agent.reserved){
                arr.push(agent);
            }
        }
        this.agents = arr;
    }

    onEventShow(){
        this.ping();
    }

    init(){
        this.ip = '';
        this.sio = null;    
    }

    dispatchEvent(type,data = null){
        for(var k in this.agents){
            var agent = this.agents[k];
            agent.onMessage(type,data);
        }
    }

    gamemsgHandler(param) {
        console.log('[Debug] - gamemsghandler called.');
        var isStr = (typeof param === 'string');
        if (isStr === true) {
            param = JSON.parse(param);
        }

        if (param == null || param.msg == null) {
            console.log('[Error] - param [' + param + '] or msg is null.');
            return;
        }

        var gamemsg = this.crypto.decode(param.msg);
        var msgobj = JSON.parse(gamemsg);
        if (msgobj != null) {
            var event = msgobj.event;
            var data = msgobj.data;

            if (event != "disconnect" && typeof(data) == "string") {
                data = JSON.parse(data);
            }
            console.log(("on net event : [" + event + "]   ["), data, "]");
            this.dispatchEvent(event,data);
        }
    }

    connect(fnConnect, fnError) {
        var timer = setTimeout(function () {
            console.log('connect timeout');
            close();
        }, 10000);

        this.connectInternal(function (data) {
            clearTimeout(timer);
            fnConnect(data);
        }, function (data) {
            clearTimeout(timer);
            fnError(data);
        });
    }

    connectInternal(fnConnect, fnError) {
        var opts = {
            'reconnection': false,
            'force new connection': true,
            'transports': ['websocket', 'polling']
        };

        var self = this;
        self.sio =  Laya.Browser.window.io.connect(self.ip, opts);

        self.sio.on('connect', function (data) {
            if (self.sio) {
                self.sio.connected = true;
                fnConnect(data);
                self.startHearbeat();
            }
        });

        self.sio.on('disconnect', function (data) {
            console.log("disconnect");
            if(self.sio){
                self.sio.connected = false;
                self.close();
            }
        });

        self.sio.on('connect_failed', function () {
            console.log('connect_failed');
        });

        //register game event
        self.sio.on('gamemsg', function(data){
            self.gamemsgHandler(data);
        });
    }

    startHearbeat() {
        clearInterval(this.timerPing);
        clearInterval(this.timerTimeout);
        //cc.game.off(cc.game.EVENT_SHOW,this.onEventShowBind);
        
        var self = this;
        this.sio.on('game_pong', function () {
            console.log('game_pong');
            self.lastRecieveTime = Date.now();
            self.delayMS = self.lastRecieveTime - self.lastSendTime;
            console.log(self.delayMS);
        });

        this.lastRecieveTime = Date.now();
        //cc.game.on(cc.game.EVENT_SHOW,this.onEventShowBind);

        this.timerPing = setInterval(function () {
            self.ping();
        }, 5000);
        this.timerTimeout = setInterval(function () {
            if (Date.now() - self.lastRecieveTime > 10000) {
                self.close();
            }
        }, 500);
    }

    send(event, data:any = null) {
        if(!this.sio || !this.sio.connected){
            return;
        }

        if (data !== null && (typeof (data) == "object")) {
            data = JSON.stringify(data);
            //console.log(data);              
        }
        console.log(("send net event : [" + event + "]   ["), data, "]");

        //加密
        var senddata = {
            event: event,
            data: data,
            mid: ++HttpMgr.inst.getSource().mid,
        };
        var sendstr = JSON.stringify(senddata);
        sendstr = this.crypto.encode(sendstr);
        this.sio.emit('gamemsg', { msg: sendstr });
    }

    ping () {
        if (this.sio) {
            this.lastSendTime = Date.now();
            this.sio.emit('game_ping');
        }
    }

    close() {
        if(!this.sio){
            return;
        }
        console.log('close');
        
        if (this.sio.connected) {
            this.sio.connected = false;
            this.sio.disconnect();
        }

        this.dispatchEvent('disconnect');

        this.sio = null;
        this.delayMS = null;
        clearInterval(this.timerPing);
        clearInterval(this.timerTimeout);
        //cc.game.off(cc.game.EVENT_SHOW,this.onEventShowBind);
    }

    test(fnResult) {
        this.http.make('/hi',null,function(data){
                var isOnline = !data || data.errcode == 0;
                fnResult(isOnline);
            }.bind(this)
        ).send();
    }

    getSio() {
        return this.sio;
    }

    getDelayMS() {
        return this.delayMS;
    }

    getSignalStrength() {
        var delayMS = this.delayMS;
        if (!delayMS || delayMS >= 1000) {
            return 3;
        }
        else if (delayMS >= 500) {
            return 2;
        }
        else if (delayMS >= 200) {
            return 1;
        }
        else if (delayMS >= 0) {
            return 0;
        }
    }
}