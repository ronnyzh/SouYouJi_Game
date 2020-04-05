var selectServerHandler = (function (){
    return {
        PING_TIMEOUT : 1000,
        PING_COUNT  : 1,
        selectServerUrl : "",
        selectedDns: "",
        serverPingData:{},
        httpUrl: "/hall/extendSession",
        isSelectServer : false,

        protocol:"http:",
        defautAddress:"",
        serverDnsList:[],
        subDnsCount:0,
        subDns:"",
        mainDns:"",
        port:9798,

        select : function(cb)
        {
            if(!this.isSelectServer)
            {
                this.isSelectServer = true;
                this.serverPingData = {};
                this._testServerList(cb);
            }
            else
                console.log("is selectServering" );
        },

        selectFail:function(errorInfo)
        {
			/*
            jx.alert(errorInfo, jx.AlertButtonType.OK, function(confirm){
                if(confirm)
                {
                    jx.utils.exitGame();
                }
            });
			*/
			console.log(errorInfo);
        },

        getServer : function()
        {
          return  this.selectServerUrl;
        },

        _generateServeList:function(serverList)
        {
            this.serverDnsList = [];

            if(this.port %2==0) //selectServerHandler.protocol == 'http:'
            {
                this.serverDnsList = [];
                this.serverDnsList.push("test1");
                serverList.push("http://test1-lb.365cards.net");
                this.serverDnsList.push("test2");
                serverList.push("http://test2-lb.365cards.net");
            }
            else
            {
                this.serverDnsList = [];
                this.serverDnsList.push("test1");
                serverList.push("https://test1-lb.365cards.net");
                this.serverDnsList.push("test2");
                serverList.push("https://test2-lb.365cards.net");
            }
            
        },

        _testServerList : function(cb)
        {
            var serverList = [];
            this._generateServeList(serverList);

            var onTested = function()
            {
                var isSuccess = this._select(serverList);
                cb(isSuccess);
                this.isSelectServer = false;
            };

            //console.log("loop start:" + Date.now());
            var obj = {isEnd:false};
            //console.log("serverList:" + serverList.length);
            for(var i = 0; i < serverList.length; ++i)
            {
                var url = serverList[i];
                this._testServer(url, onTested.bind(this), obj);
            }
            //console.log("loop end:" + Date.now());
        },

        _testServer:function(url,cb, obj)
        {
            var pingOverCount = 0;
            for(var i = 0; i < this.PING_COUNT; ++i)
            {
                this._pingServer(url, function(interval){
                    if(!obj.isEnd)
                    {
                        if(!this.serverPingData.hasOwnProperty(url))
                            this.serverPingData[url] = [];
                        
                        this.serverPingData[url].push(interval);
                        ++pingOverCount;
                        if(pingOverCount == this.PING_COUNT)
                        {
                            obj.isEnd = true;
                            cb();
                        }
                    }

                }.bind(this),this.PING_TIMEOUT, i);
            }
        },

        _select:function(serverList)
        {
            //jx.utils.dumpObject(this.serverPingData);
            var interval = this.PING_TIMEOUT;
            var serverIdx = -1;
            for(var i = 0; i < serverList.length; ++i)
            {
                var url = serverList[i];
                if(this.serverPingData.hasOwnProperty(url) && this.serverPingData[url].length > 0)
                {
                    //var tmp = this.serverPingData[url];
                    var tmp = 0;
                    for(var j = 0; j < this.serverPingData[url].length; ++j)
                        tmp += this.serverPingData[url][j];

                    tmp = Math.ceil(tmp / this.serverPingData[url].length);
                    console.log(interval+"  "+tmp);
                    if(interval > tmp)
                    {
                        interval = tmp;
                        serverIdx = i;
                    }
                }
            }
            //console.log("----------------------------------------------------");
            //console.log(interval+"  "+this.PING_TIMEOUT);

            if(interval == this.PING_TIMEOUT){
                this.selectServerUrl = this.defautAddress;
            }else{
                this.selectServerUrl = serverList[serverIdx];
                this.selectedDns = this.serverDnsList[serverIdx];
            }

            //console.log("select server:" + this.selectServerUrl);
            return true;
        },

        _pingServer:function(url, cb, timeOut, Num)
        {
            timeOut = timeOut || 0;
            var timer;
            var start = 0;
            var isPong = false;

            var pingCheck = function() {
                if(isPong)
                    return;
                
                if (timer) { clearTimeout(timer); }
                var pong = Date.now() - start;
                isPong = true;
                if (typeof cb === "function") {
                    //console.log(pong);
                    cb(pong);
                }
            }.bind(this);

            start = Date.now();

            if (timeOut > 0) { timer = setTimeout(pingCheck, timeOut); }

            url = url +":"+this.port+ this.httpUrl;

            var hr = new Laya.HttpRequest();
            
            hr.once(Laya.Event.COMPLETE, null, function(e)
            {
                var jsonobj = JSON.parse(e);
                if(jsonobj.code == 1)
                {
                    pingCheck();
                }
            });

            hr.once(Laya.Event.ERROR, null, function (e)
            {
                if(isPong)
                    return;
                    
                if (timer) 
                { 
                    clearTimeout(timer); 
                }

                var pong = 9999999999;
                isPong = true;

                if (typeof cb === "function")
                {
                    cb(pong);
                }
            });

            hr.send(url, null, 'get', 'text');
        }
    };
})();

function dnsSeverSelectorInit(protocol,subDnsCount,subDns,mainDns,port,defautAddress)
{
    selectServerHandler.protocol = protocol;
    selectServerHandler.defautAddress = defautAddress;
    selectServerHandler.subDnsCount = subDnsCount;
    selectServerHandler.subDns = subDns;
    selectServerHandler.mainDns = mainDns;
    selectServerHandler.port = port;
}

function selectDnsSever(cb)
{
    selectServerHandler.select(cb);
}

function getDnsSever()
{
    return selectServerHandler.getServer();
}

function getSelectDns()
{
    return selectServerHandler.selectedDns;
}

function getDefaultDns(port)
{
    return (port %2==0)? 'tss449.365gaming.cc':'tss449.365gaming.cc';
}

function getNetworkPort(protocol)
{
    return ("http:" == protocol)? 80:443;
}