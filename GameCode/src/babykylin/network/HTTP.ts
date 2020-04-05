/*
* name;
*/

class HttpConnect{
    public url:string = null;
    public params:string = null;
    public type:string = null;
    public timeout:number = 0;
    public responseType:string = null;
    private complete:Function = null;
    private progress:Function = null;
    private error:Function = null;

    constructor(fn:Function){
        this.complete = fn;
    }

    send(){
        let xhr = new Laya.HttpRequest();
        xhr.http.timeout = this.timeout;
        xhr.once(Laya.Event.COMPLETE, this, this.handleComplete);
        xhr.once(Laya.Event.ERROR, this, this.handleError);
        xhr.on(Laya.Event.PROGRESS, this, this.handleProcess);
        xhr.send(this.url, this.params , this.type,this.responseType);
    }

    public onComplete(handler:Function){
        this.complete = handler;
        return this;
    }

    public onError(handler:Function){
        this.error = handler;
        return this;
    }

    public onProgress(handler:Function){
        this.progress = handler;
        return this;
    }

    private handleComplete(data){
        if(this.complete && data){
            data = JSON.parse(data);

            if(TestMgr.IS_ENABLE_PRINT_URL)
            {
                var str:string = data.msg;
                if(str && str.indexOf('account')>=0 && str.indexOf('not')>=0 && str.indexOf('exist')>=0)
                {
                    console.log('===================================Alert.log===================================');
                    console.log('url:'+ this.url);
                    console.log('code:'+ data.code);
                    console.log('msg:'+ data.msg);

                    if(location_search_account)
                        console.log('account:\n'+ location_search_account);
                    else if(location_random_index>=0 && location_random_index<TestAccounts.length)
                        console.log('account:\n'+ TestAccounts[location_random_index]);
                    console.log('===============================================================================');
                }
            }

            if(data.code == -3 || data.code == -5)
            {
                EventMgr.emit('onAccountError');
                Alert.show(ExtendMgr.inst.getText4Language(data.msg)).onYes(function()
                {
                    window.location.reload(true);
                }.bind(this))
            }
            else if(data.code == -4)
            {
                EventMgr.emit('onAccountError');
                this.onOtherDeviceLogin(data.msg);
            }
            else
            {
                this.complete(data);
            }
        }
        //console.log('handleComplete:',data);
    }

    private onOtherDeviceLogin(msg)
    {
        Alert.show(ExtendMgr.inst.getText4Language(msg)).onYes(function()
        {
             this.onOtherDeviceLogin(msg);
        }.bind(this))
    }
    
    private handleError(data)
    {
        //console.log(data);
        if(this.error){
            this.error(data);
        }
        else
        {
            /*setTimeout(function() {
                this.send();
            }.bind(this), 3000);*/
            Alert.show(ExtendMgr.inst.OnNetWorkError).onYes(function(){
                //MasterMgr.inst.switch('relogin');
                 window.location.reload(true);
            }.bind(this))
        }
    }
    
    private handleProcess(data){
        if(this.progress){
            this.progress(data);
        }
    }
}

class HTTP{
    private url:string = null;
    private timeout:number = 0;
    private responseType:string = null;
    public mid:number = 0;
    public sid:string = null;
    constructor(url:string,responseType:string='text',timeout:number = 3000){
        this.url = url;
        this.timeout = timeout;
        this.responseType = responseType;
    }

    make(path:string,type:string,data:any={},completeHandler:Function = null,errorHandler:Function = null):HttpConnect{

        /*if(this.mid){
            this.mid++; data.mid = this.mid;
        }*/

        if(this.sid){
            data['sid'] = this.sid;
        }

        let sendtext = '';
        for (let k in data) {
            if (sendtext != "") {
                sendtext += "&";
            }
            sendtext += (k + "=" + data[k]);
        }
        //console.log("sendtext:"+sendtext)

        var item = new HttpConnect(completeHandler);
        item.url = this.url + path;
        item.type = type;
        item.params = encodeURI(sendtext);
        item.timeout = this.timeout;
        item.onError(errorHandler);
        item.responseType = this.responseType;
        return item;
    }

    send(path:string,type:string,data:any,completeHandler:Function = null,errorHandler:Function = null){
        var conn = this.make(path,type,data,completeHandler,errorHandler);
        conn.send();
    }
    
}