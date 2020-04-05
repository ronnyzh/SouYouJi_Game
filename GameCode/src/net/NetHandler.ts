/*
* name;
*/
class NetHandler {

    public socket: Socket;
    private output: Byte;
    private sid: string;

    private msgType2listener = {};
    private msgType2Class = {};

    constructor() {
    }

    public init(protoDataList: Array<any>): void {
        var ProtoBuf = dcodeIO["ProtoBuf"];
        var lastBuilder = null;
        for (var i = 0; i < protoDataList.length; ++i) {
            var protoData = protoDataList[i];
            var strProto = Laya.loader.getRes(protoData.path);
            var builder = ProtoBuf.loadProto(strProto, lastBuilder, protoData.path);
            lastBuilder = builder;
            var pkgMsgMap = builder.build(protoData.pkgName);
            if (!pkgMsgMap) continue;

            var list = protoData.classesMapList;
            for (var j = 0; j < list.length; ++j) {
                var data = list[j];
                var msgType = data[0];
                var msgName = data[1];
                var isLog = !data[2];
                var msgClass = pkgMsgMap[msgName];
                if (isLog) {
                    try {
                        msgClass.className = msgName;
                    } catch (e) { console.warn(msgName, e); }
                }

                this.msgType2Class[msgType] = msgClass;
            }
        }
        this.enableSequenceMsg();
    }

    public initProbuf(protoDataList, classesMapList): void {

    }

    valid() {
        return this.socket != null && this.socket.connected;
    }

    private connectCB: Function = null;
    private ip;
    private port;

    connect(data: any, connectCB: Function = null): void {
        this.socket = new Socket();
        this.ip = data["ip"];
        this.port = data["port"];
        getCodeAdapter().run('NetHandler.connect', this.socket, this.ip, this.port);

        this.output = this.socket.output;
        this.connectCB = connectCB;

        var Event = Laya.Event;
        this.socket.on(Event.OPEN, this, this.onSocketOpen);
        this.socket.on(Event.CLOSE, this, this.onSocketClose);
        this.socket.on(Event.MESSAGE, this, this.onMessageReveived);
        this.socket.on(Event.ERROR, this, this.onConnectError);
    }

    private onSocketOpen(): void {
        console.log("Connected 连接成功");
        this.showAlert = true;
        if (this.connectCB) this.connectCB(true);
    }

    private showAlert = true;
    private onSocketClose(): void {
        console.log("Socket closed");
        if (this.showAlert)
            this.showDisconnectAlert();
    }

    showDisconnectAlert() {
        Alert.show(ExtendMgr.inst.DisconnectAlert).onYes(function () {
            MasterMgr.inst.switch('relogin');
        }.bind(this))
    }

    private onMessageReveived(message: any): void {
        //console.log("Message from server:",message);
        if (typeof message == "string") {
            console.log(message);
        }
        else if (message instanceof ArrayBuffer) {
            // try {
            var msg = this._decodeData(message);
            if (!msg) {
                console.log("msg ----- type error!! ");
                return;
            }
            var now = new Date().toString();
            if (msg.className != null && ExtendMgr.inst.isShowProtoCmd)
                console.log(now.split("GMT")[0] + "!!! receive msg type:" + msg.type.toString(16) + ", " + msg.className, msg);

            var listeners = this.msgType2listener[msg.type];
            if (msg.className != "S_C_Ping") {
                //console.log(listeners);
                NetHandlerMgr.inst.onReceiveMsg();
            }

            if (listeners != null && listeners.length != 0) {
                listeners = listeners.concat();
                for (var i = 0; i < listeners.length; ++i)
                    listeners[i](msg);
            }

            // } catch (e) {
            //     console.log(e);
            // }
        }
        this.socket.input.clear();
    }

    private onConnectError(e: Event): void {
        console.log("onConnectError");
        if (this.sequenceController != null)
            this.sequenceController.reset();
        if (this.connectCB) this.connectCB(false);
    }

    public sendData(msgType: number, obj: any): void {
        obj = obj || {};
        var data = this._encodeData(msgType, obj, false, false);
        try {
            this.socket.send(data);
        } catch (error) {
            this.showDisconnectAlert();
        }
    }

    private encodeMessage(msgType, data) {
        var MessageClass = this.msgType2Class[msgType];
        var now = new Date().toString();
        if (MessageClass.className != null && ExtendMgr.inst.isShowProtoCmd)
            console.log(now.split("GMT")[0] + "!!! send msg type:" + msgType.toString(16) + ", " + MessageClass.className, data);
        var msg = new MessageClass(data);
        var msgBuffer = msg.toArrayBuffer();

        return msgBuffer;
    }

    _encodeData(msgType, data, sendtime, compressed) {
        sendtime = !!sendtime;
        compressed = !!compressed;
        var compressedCode = compressed ? 1 : 0;

        var msgBuffer = this.encodeMessage(msgType, data);

        //发送数据的buffer
        var dataBuffer = new ArrayBuffer(4 + msgBuffer.byteLength);

        var tmp: any = new DataView(dataBuffer);
        tmp.setUint32(0, msgType, false);
        tmp = new Uint8Array(dataBuffer);
        tmp.set(new Uint8Array(msgBuffer), 4);

        if (compressed) {
            var gzip = new Zlib["Gzip"](new Uint8Array(dataBuffer));
            var compressData = gzip["compress"]();
            dataBuffer = compressData.buffer.slice(0, compressData.byteLength);
        }

        var ByteBuffer = dcodeIO["ByteBuffer"];
        var extLen = sendtime ? 10 : 2;
        var totalLen = dataBuffer.byteLength + extLen;
        var extData = new ByteBuffer(extLen);
        if (sendtime) {
            extData.writeUInt8(compressedCode);
            extData.writeUInt8(1);
            extData.writeUInt64(new Date().getTime());
        }
        else {
            extData.writeUInt8(compressedCode);
            extData.writeUInt8(0);
        }

        //组装数据
        var extOffset = Math.floor(totalLen / 3);
        var finalData = new Uint8Array(totalLen);
        finalData.set(new Uint8Array(dataBuffer.slice(0, extOffset)), 0);
        finalData.set(new Uint8Array(extData.buffer), extOffset);
        finalData.set(new Uint8Array(dataBuffer.slice(extOffset)), extOffset + extLen);

        return finalData.buffer;
    }

    private _decodeData(data) {
        //var receiveTime = new Date().getTime();

        var totalLen = data.byteLength;
        var extOffset = Math.floor(totalLen / 3);
        var dvTotal = new DataView(data);
        var compressed = dvTotal.getUint8(extOffset) == 1;
        var hasTime = dvTotal.getUint8(extOffset + 1) == 1;
        var extLen = hasTime ? 10 : 2;

        //截取有效数据
        var buffer = new ArrayBuffer(totalLen - extLen);
        var tmp = new Uint8Array(buffer);
        tmp.set(new Uint8Array(data.slice(0, extOffset)), 0);
        tmp.set(new Uint8Array(data.slice(extOffset + extLen)), extOffset);

        if (compressed) {
            var gunzip = new Zlib["Gunzip"](new Uint8Array(buffer));
            buffer = gunzip["decompress"]().buffer;
        }

        var type = new DataView(buffer).getUint32(0, false);
        //console.log("msg type in decode:" + type.toString(16));
        return this.decodeMessage(type, buffer.slice(4, buffer.byteLength));
    }

    private decodeMessage(msgType, data) {
        var receiveTime = new Date().getTime();

        var MessageClass = this.msgType2Class[msgType];
        if (!MessageClass) return console.error('msgType error', msgType);
        var msg = MessageClass.decode(data);
        msg.className = MessageClass.className;
        msg.type = msgType;
        msg.receiveTime = receiveTime;

        return msg;
    }

    public disconnect(): void {
        this.showAlert = false;
        if (this.socket != null) {
            this.socket.close();
        }
        NetHandlerMgr.inst.clearPingListen();
        this.removeAllMsgListener();
    }

    addMsgListener(msgType, listener) {
        var listeners = this.msgType2listener[msgType];
        if (listeners == null) {
            listeners = [];
            this.msgType2listener[msgType] = listeners;
        }
        listeners.push(listener);
    }

    removeElement(arr, ele) {
        var idx = arr.indexOf(ele);
        if (idx == -1) return;
        arr.splice(idx, 1);
    }

    removeMsgListener(msgType, listener) {
        var listeners = this.msgType2listener[msgType];
        if (listeners != null) {
            this.removeElement(listeners, listener);
        }
    }

    removeAllMsgListener(msgType = null) {
        if (msgType)
            this.msgType2listener[msgType] = null;
        else {
            this.msgType2listener = {};
            this.smType2Listener = {};
        }
    }

    createOnceListener(msgType, cb) {
        var listener = function (data) {
            this.removeMsgListener(msgType, listener);
            if (cb != null)
                cb(data);
        }.bind(this);

        this.addMsgListener(msgType, listener)
    }

    createOnceSequenceListener(msgType, cb) {
        this.removeSequenceMsgListener(msgType);

        var listener = function (data, finishedListener) {
            if (cb != null)
                cb(data);
            if (finishedListener != null)
                finishedListener();
        }.bind(this);

        this.addSequenceMsgListener(msgType, listener)
    }

    removeSequenceMsgListener(msgType, listener = null) {
        this.removeMsgListener(msgType, this.smListener);
        this.smType2Listener[msgType] = null;
        //this.msgType2listener[msgType] = null
    }

    private sequenceController: SequenceController;
    private smListener: Function;
    private smType2Listener: Object;

    /*----------------------------------------------- 串行消息处理 ------------------------------------------------------*/
    enableSequenceMsg() {
        this.sequenceController = new SequenceController();
        this.sequenceController.setExecutor(this.dispatchSequenceMsg.bind(this));
        this.smListener = this.onSequenceMMsg.bind(this);
        this.smType2Listener = {};
        // this.smTypeList = msgList;
    }

    addSequenceMsgListener(msgType, listener) {
        if (this.smType2Listener[msgType] != null)
            return;//throw("重复监听串行消息");

        this.addMsgListener(msgType, this.smListener);
        this.smType2Listener[msgType] = listener;
    }

    //分发串行消息,业务层真正响应消息处理在此处
    dispatchSequenceMsg(data) {
        var listener = this.smType2Listener[data.type];

        if (listener != null) {
            listener(data, this.sequenceController.actionFinishedListener);
        }
    }

    //收到服务器的串行消息
    onSequenceMMsg(data) {
        this.sequenceController.push(data);
    }
}