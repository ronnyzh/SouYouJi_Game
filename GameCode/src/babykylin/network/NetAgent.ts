
class NetAgent{
    private static idbase:number = 0;
    private name:string = null;
    private id:number = null;
    private _reserved:boolean = false;
    private handlers = {};
    constructor(name:string,reserved = false){
        this.name = name;
        this.id = NetAgent.idbase++;
        this._reserved = reserved;
        console.log('NetAgent',this.name,':',this.id,'has been created.');
    }

    public get reserved():boolean{
        return this._reserved;
    }

    addTarget(target,prefix = null){
        if (!target) {
            return;
        }
        if(!prefix){
            prefix = 'onnet_';
        }

        for (var k in target) {
            if (k.search(prefix) == 0) {
                var event = k.substr(prefix.length);
                var fn = target[k];
                var tFunc = fn.bind(target);
                this.addHandler(event, tFunc);
            }
        }
    }

    addHandler(msgType,func){
        this.handlers[msgType] = func;
    }

    //网络消息
    onMessage(msgType,data){
        var func = this.handlers[msgType];
        if(func){
            func(data);
        }
    }
}

