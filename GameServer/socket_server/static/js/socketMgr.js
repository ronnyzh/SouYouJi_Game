let socket = undefined;
let urlApi_callBack = undefined;

class NetHandler {
    //系统类A0001
    static header_C_S_Ping = 0x000A0001;
    //比赛场类A1001
    static header_C_S_match_isAutoPush = 0x000A1001;
    static header_C_S_match_infoList_get = 0x000A1002;
    static header_C_S_match_enroll_get = 0x000A1003;
    static header_C_S_match_enroll_do = 0x000A1004;
    static header_C_S_match_enroll_cancel = 0x000A1005;
    static header_C_S_match_readyJoin_tips_ignore = 0x000A1006;

    //系统类B0001
    static header_S_C_Ping = 0x000B0001;
    static header_S_C_Disconnected = 0x000B0002;
    //比赛场类B1001
    static header_S_C_match_isAutoPush = 0x000B1001;
    static header_S_C_match_infoList_get = 0x000B1002;
    static header_S_C_match_enroll_get = 0x000B1003;
    static header_S_C_match_enroll_do = 0x000B1004;
    static header_S_C_match_enroll_cancel = 0x000B1005;
    static header_S_C_match_readyJoin_tips_ignore = 0x000B1006;
    static header_S_C_match_readyJoin_tips = 0x000B1007;
    protoDataList = [
        {
            pkgName: "hallMatch",
            path: "/static/proto/hall_match.proto",
            classesMapList: [
                [NetHandler.header_C_S_Ping, 'C_S_Ping'],
                [NetHandler.header_C_S_match_isAutoPush, 'C_S_match_isAutoPush'],
                [NetHandler.header_C_S_match_infoList_get, 'C_S_match_infoList_get'],
                [NetHandler.header_C_S_match_enroll_get, 'C_S_match_enroll_get'],
                [NetHandler.header_C_S_match_enroll_do, 'C_S_match_enroll_do'],
                [NetHandler.header_C_S_match_enroll_cancel, 'C_S_match_enroll_cancel'],
                [NetHandler.header_C_S_match_readyJoin_tips_ignore, 'C_S_match_readyJoin_tips_ignore'],

                [NetHandler.header_S_C_Ping, 'S_C_Ping', S_C_Handler.S_C_Ping],
                [NetHandler.header_S_C_Disconnected, 'S_C_Disconnected', S_C_Handler.S_C_Disconnected],
                [NetHandler.header_S_C_match_isAutoPush, 'S_C_match_isAutoPush', S_C_Handler.S_C_match_isAutoPush],
                [NetHandler.header_S_C_match_infoList_get, 'S_C_match_infoList_get', S_C_Handler.S_C_match_infoList_get],
                [NetHandler.header_S_C_match_enroll_get, 'S_C_match_enroll_get', S_C_Handler.S_C_match_enroll_get],
                [NetHandler.header_S_C_match_enroll_do, 'S_C_match_enroll_do', S_C_Handler.S_C_match_enroll_do],
                [NetHandler.header_S_C_match_enroll_cancel, 'S_C_match_enroll_cancel', S_C_Handler.S_C_match_enroll_cancel],
                [NetHandler.header_S_C_match_readyJoin_tips_ignore, 'S_C_match_readyJoin_tips_ignore', S_C_Handler.S_C_match_readyJoin_tips_ignore],
                [NetHandler.header_S_C_match_readyJoin_tips, 'S_C_match_readyJoin_tips', S_C_Handler.S_C_match_readyJoin_tips],
            ]
        }
    ];

    constructor() {
        this.msgType2listener = {};
        this.msgType2Class = {};
        this.socket = null;
        this.socketCache = [];
        this.init(this.protoDataList);
        this.lastRecvPing = 0;
        this.timers = {};
    }

    ws_onmessage(event) {
        // console.log('socket收到消息', event.data);
        this.onMessageReveived(event.data);

        // try {
        //     data = JSON.parse(event.data);
        //     console.log('socket收到消息', data);
        //     url = data['url'];
        //     callBackFunc = urlApi_callBack[url];
        //     if (callBackFunc) {
        //         callBackFunc(data)
        //     } else {
        //         console.log('未知接口', url)
        //     }
        // } catch (err) {
        //     console.log('socket收到消息,但无法解析', event.data, err);
        // }

    };

    onMessageReveived(message) {
        if (typeof message === "string") {
            console.log(message);
        }
        else if (message instanceof ArrayBuffer) {
            // try {
            let msg = this._decodeData(message);
            if (!msg) {
                console.log("msg ----- type error!! ");
                return;
            }
            let now = new Date().toString();
            if (msg.className != null)
                console.log(now.split("GMT")[0] + "!!! receive msg type:" + msg.type.toString(16) + ", " + msg.className, msg);
            let listeners = this.msgType2listener[msg.type];
            if (msg.className !== "S_C_Ping") {
                //console.log(listeners);
            }
            if (listeners != null && listeners.length !== 0) {
                listeners = listeners.concat();
                for (let i = 0; i < listeners.length; ++i)
                    listeners[i](msg);
            }
            // }
            // catch (e) {
            //     console.log(e);
            // }
        }
    }

    setTimer(tag, timer) {
        this.rmTimer(tag);
        this.timers[tag] = timer;
    }

    rmTimer(tag) {
        let oldTimer = this.timers[tag];
        oldTimer && clearInterval(oldTimer);
        delete this.timers[tag];
    }

    ws_onopen() {
        actionMgr.do_show_msg(actionMgr.getFiterStr_Sys('webSocket已连接'));
        changeReq_type('socket');
        layui.each(this.socketCache, (index, data) => {
            console.log('[ws_onopen] 处理缓存中的待发送消息', data);
            this.socket.send(data)
        });
        this.socket.ping();
        let timer = setInterval(this.socket.ping, 15 * 1000);
        this.setTimer('PING', timer);
    };

    ws_onclose(event) {
        this.rmTimer('PING');
        console.log(event.code, event.reason, event.wasClean);
        let msg = 'webSocket关闭[{0}],原因:{1}'.format(event.code, (event.reason ? event.reason : '未知'));
        actionMgr.do_show_msg(actionMgr.getFiterStr_Sys(msg + ' <a style="color: orangered;cursor:pointer;" onclick=net.do_connect_ws()>点击重新连接</a>'), 'error');
        this.socket = null;
        changeReq_type()
    };

    ws_onerror(event) {
        console.log('socket-onerror');
        console.log(event);
    };

    do_connect_ws() {
        console.log('do_connect_ws');
        if (!this.socket) {
            this.socket = new WebSocket('ws://127.0.0.1:9797/match/{0}'.format(curSid));
            this.socket.binaryType = "arraybuffer";
            this.socket.onopen = this.ws_onopen.bind(this);
            this.socket.onclose = this.ws_onclose.bind(this);
            this.socket.onerror = this.ws_onerror.bind(this);
            this.socket.onmessage = this.ws_onmessage.bind(this);
            this.socket.ping = C_S_Handler.C_S_Ping;
        }
        return this.socket
    }

    do_close_ws(code, reason) {
        console.log('do_close_ws', this.socket);
        this.socket && this.socket.close(code, reason)
    };

    socketIsOpen() {
        return this.socket != null && this.socket.readyState == WebSocket.OPEN;
    }

    sendData(msgType, obj) {
        if (!msgType) {
            return
        }
        obj = obj || {};
        let data = this._encodeData(msgType, obj);
        if (this.socketIsOpen()) {
            this.socket.send(data);
        } else {
            this.socketCache.push(data);
            console.log('[ERROR][sendData] ws未连接 已放入缓存中');
        }
    };

    init(protoDataList) {
        let ProtoBuf = dcodeIO["ProtoBuf"];
        let lastBuilder = null;
        for (let i = 0; i < protoDataList.length; ++i) {
            let protoData = protoDataList[i];
            let builder = ProtoBuf.loadProtoFile(protoData.path);
            lastBuilder = builder;
            let pkgMsgMap = builder.build(protoData.pkgName);
            if (!pkgMsgMap)
                continue;
            let list = protoData.classesMapList;
            for (let j = 0; j < list.length; ++j) {
                let data = list[j];
                let msgType = data[0];
                let msgName = data[1];
                let callFunc = data[2];
                let msgClass = pkgMsgMap[msgName];
                msgClass.className = msgName;
                this.msgType2Class[msgType] = msgClass;
                if (callFunc) {
                    this.msgType2listener[msgType] = [callFunc];
                }

            }
        }
    }

    encodeMessage(msgType, data) {
        let MessageClass = this.msgType2Class[msgType];
        let now = new Date().toString();
        if (MessageClass.className != null)
            console.log(now.split("GMT")[0] + "!!! send msg type:" + msgType.toString(16) + ", " + MessageClass.className, data);
        let msg = new MessageClass(data);
        let msgBuffer = msg.toArrayBuffer();
        return msgBuffer;
    }

    _encodeData(msgType, data) {
        let msgBuffer = this.encodeMessage(msgType, data);
        //发送数据的buffer
        let dataBuffer = new ArrayBuffer(4 + msgBuffer.byteLength);
        let tmp = new DataView(dataBuffer);
        tmp.setUint32(0, msgType, false);
        tmp = new Uint8Array(dataBuffer);
        tmp.set(new Uint8Array(msgBuffer), 4);
        let totalLen = dataBuffer.byteLength;
        //组装数据
        let extOffset = Math.floor(totalLen / 3);
        let finalData = new Uint8Array(totalLen);
        finalData.set(new Uint8Array(dataBuffer.slice(0, extOffset)), 0);
        finalData.set(new Uint8Array(dataBuffer.slice(extOffset)), extOffset);
        return finalData.buffer;
    }

    _decodeData(data) {
        let totalLen = data.byteLength;
        //截取有效数据
        let buffer = new ArrayBuffer(totalLen);
        let tmp = new Uint8Array(buffer);
        tmp.set(new Uint8Array(data), 0);
        let type = new DataView(buffer).getUint32(0, false);
        console.log("[_decodeData]:" + type.toString(16));
        return this.decodeMessage(type, buffer.slice(4, buffer.byteLength));
    }

    decodeMessage(msgType, data) {
        let receiveTime = new Date().getTime();
        let MessageClass = this.msgType2Class[msgType];
        if (!MessageClass)
            return console.error('msgType error', msgType);
        let msg = MessageClass.decode(data);
        msg.className = MessageClass.className;
        msg.type = msgType;
        msg.receiveTime = receiveTime;
        return msg;
    }
}

