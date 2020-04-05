String.prototype.format = function (args) {
    let result = this;
    if (arguments.length > 0) {
        if (arguments.length === 1 && typeof (args) === "object") {
            for (let key in args) {
                let reg = new RegExp("({" + key + "})", "g");
                result = result.replace(reg, args[key]);
            }
        }
        else {
            for (let i = 0; i < arguments.length; i++) {
                let reg = new RegExp("({)" + i + "(})", "g");
                result = result.replace(reg, arguments[i]);
            }
        }
    }
    return result;
};

function compreObj(obj1, obj2) {
    let flag = true;

    function compre(obj1, obj2, key) {
        // console.log('[compreObj-0]',key,obj1,obj2);
        if (Object.keys(obj1).length !== Object.keys(obj2).length) {
            flag = false;
            // console.log('[compreObj-1]',obj1,obj2);
        } else {
            for (let x in obj1) {
                if (typeof obj1[x] !== "function") {
                    if (obj2.hasOwnProperty(x)) {
                        if (obj1[x] !== obj2[x]) {
                            compre(obj1[x], obj2[x], x);
                        }
                    } else {
                        // console.log('[compreObj-2]',x,obj1,obj2);
                        flag = false;
                        break;
                    }
                } else {
                    // console.log('[compreObj-4]',x);
                }
            }
        }
        return flag
    }

    return compre(obj1, obj2)
}

function checkIsNone(data) {
    return (!data || data === undefined || JSON.stringify(data) === "{}");
}

function checkValue(val) {
    let args = Array.prototype.slice.call(arguments);
    let oArgs = args.slice(arguments.callee.length, args.length);
    console.log('checkValue');
    console.log(arguments);
    console.log(args);
    console.log(oArgs);
    for (let _type in oArgs) {
        if (val == _type) {
            return false
        }
    }
    return true;
}

checkValue('1', 2, 3, 4);

let $ = layui.jquery;
let element = layui.element; //Tab的切换功能，切换事件监听等，需要依赖element模块
let notice = layui.notice;
let laytpl = layui.laytpl;
let layer = layui.layer;
laytpl.config({
    open: '<%',
    close: '%>'
});
// 初始化配置，同一样式只需要配置一次，非必须初始化，有默认配置
notice.options = {
    closeButton: true,//显示关闭按钮
    debug: false,//启用debug
    showDuration: "300",//显示的时间
    hideDuration: "1000",//消失的时间
    timeOut: "5000",//停留的时间,0则不自动关闭
    extendedTimeOut: "1000",//控制时间
    showEasing: "swing",//显示时的动画缓冲方式
    hideEasing: "linear",//消失时的动画缓冲方式
    iconClass: 'toast-info', // 自定义图标，有内置，如不需要则传空 支持layui内置图标/自定义iconfont类名
    positionClass: "toast-bottom-right",//弹出的位置,
    // - toast-top-center
    // - toast-bottom-center
    // - toast-top-full-width
    // - toast-bottom-full-width
    // - toast-top-left
    // - toast-top-right
    // - toast-bottom-right
    // - toast-bottom-left
    onclick: null // 点击关闭回调
};

// notice.warning("成功");
// notice.info("提示信息：毛都没有...");
// notice.error("大佬，我咋知道怎么肥四！");
// notice.success("大佬，我咋知道怎么肥四！");
let lastShowMsgTime = 0;

let actionMgr = {
    do_send_chat_msg: function (res) {
        let code = res.code || 0;
        console.log('[do_send_chat_msg]');
        console.log(res);
        if (code !== undefined && code !== 0) {
            let reason = res.msg || '出错啦!';
            notice.error('发送信息失败,原因:{0}'.format(reason));
        } else {
            notice.success('发送信息成功');
        }
    },
    do_accept_chat_msg: function (res) {
        let data = res.data;
        console.log('[do_accept_chat_msg]');
        console.log(res);
        notice.info('收到消息,请查看!');
        msg = data.msg;
        sender = data.sender || {};
        sender_nickname = sender.nickname;
        actionMgr.do_show_msg_into_box(actionMgr.getFiterStr_Chat(msg, sender_nickname));
    },

    do_show_msg: function (msg, level) {
        level = level || 'info';
        // console.log('[do_show_msg] level[{0}] {1}'.format(level, msg));
        actionMgr.do_show_msg_into_notice(msg, level);
        actionMgr.do_show_msg_into_box(msg);
    },

    do_show_msg_into_box: function (msg) {
        if (!msg) {
            return
        }
        let timestamp = actionMgr.get_now_timestamp();
        let showMsgHtml = '';
        if ((timestamp - lastShowMsgTime) > 1000 * 60) {
            showMsgHtml = '<p style="text-align: center;color: turquoise">{0}</p>'.format(actionMgr.get_now_date());
            lastShowMsgTime = timestamp;
        }
        showMsgHtml += '<p style="color: white">{0}</p>'.format(msg);
        $('#msg_box_div').append(showMsgHtml).scrollTop($('#msg_box_div').prop("scrollHeight"));
    },

    do_show_msg_into_notice: function (msg, level) {
        switch (level) {
            case 'error':
                notice.error(msg);
                break;
            case 'warning':
                notice.warning(msg);
                break;
            case 'success':
                notice.success(msg);
                break;
            default:
                notice.info(msg);
                break;
        }
    },

    getFiterStr_Sys: function (msg, headTag) {
        headTag = headTag || '系统消息';
        return '<span style="color:#FFB800">{0} : </span>{1}'.format(headTag, msg);
    },
    getFiterStr_Chat: function (msg, headTag) {
        headTag = headTag || '用户信息';
        return '<span style="color:sandybrown">{0} : </span>{1}'.format(headTag, msg);
    },

    get_now_date: function () {
        let myDate = new Date();
        let year = myDate.getFullYear();        //获取当前年
        let month = myDate.getMonth() + 1;   //获取当前月
        let date = myDate.getDate();            //获取当前日
        let hour = myDate.getHours();              //获取当前小时数(0-23)
        let minute = myDate.getMinutes();          //获取当前分钟数(0-59)
        let second = myDate.getSeconds();
        return year + "-" + month + "-" + date + " " + hour + ":" + minute + ":" + second;
    },

    get_now_timestamp: function () {
        return new Date().getTime()
    },

};

class C_S_Handler {
    static C_S_Ping() {
        net.sendData(NetHandler.header_C_S_Ping)
    }

    static C_S_match_infoList_get(gameId, matchId) {
        net.sendData(NetHandler.header_C_S_match_infoList_get, {gameId: gameId, matchId: matchId})
    }

    static C_S_match_enroll_do(gameId, matchId) {
        net.sendData(NetHandler.header_C_S_match_enroll_do, {gameId: gameId, matchId: matchId})
    }

    static C_S_match_enroll_cancel(gameId, matchId) {
        net.sendData(NetHandler.header_C_S_match_enroll_cancel, {gameId: gameId, matchId: matchId})
    }

    static C_S_match_readyJoin_tips_ignore(ignoreSecond) {
        net.sendData(NetHandler.header_C_S_match_readyJoin_tips_ignore, {ignoreSecond: ignoreSecond})
    }
}

class S_C_Handler {
    static S_C_Ping(resp) {
        net.lastRecvPing = actionMgr.get_now_timestamp()
    }

    static S_C_Disconnected(resp) {
        net.do_close_ws(1000, resp.reason)
    }

    static S_C_match_isAutoPush(resp) {

    }

    static S_C_match_infoList_get(resp) {
        let code = resp.code;
        let gameId = verifyMgr.verify_gameId(resp.gameId);
        let matchId = verifyMgr.verify_matchId(resp.matchId);
        // console.log('[S_C_match_infoList_get]:', resp);
        if (verifyMgr.checkSuc(code)) {
            if (resp.data) {
                if (dataView.isInit) {
                    dataView.doKey_matchList(resp.data.matchList);
                    dataView.doKey_enrollInfo(resp.data.enrollInfo);
                    dataView.showView();
                } else {
                    dataView.initData(resp.data.matchList, resp.data.enrollInfo);
                }

            } else {
                notice.info('{0}:刷新成功,但没有数据'.format(gameIdMap[gameId]));
            }
        } else {
            let reason = resp.msg || '出错啦!';
            notice.error('{0}:刷新失败,原因:{1}'.format(gameIdMap[gameId], reason));
        }
    }

    static S_C_match_enroll_get(resp) {
        let code = resp.code;
        // console.log('[S_C_match_enroll_get]:', resp);
        if (verifyMgr.checkSuc(code)) {
            dataView.doKey_enrollInfo(resp.data.enrollInfo);
            dataView.showView();
        } else {
            let reason = resp.msg || '出错啦!';
            notice.error('刷新报名信息失败原因:{0}'.format(reason));
        }
    }

    static S_C_match_enroll_do(resp) {
        let code = resp.code;
        let gameId = resp.gameId;
        let matchId = resp.matchId;
        // console.log('[S_C_match_enroll_do]:', resp);
        if (verifyMgr.checkSuc(code)) {
            notice.success('{0}:成功报名比赛[ID:{1}]'.format(gameIdMap[gameId], matchId));
            dataView.doKey_enrollInfo(resp.data.enrollInfo);
            dataView.showView();
        } else {
            let reason = resp.msg || '出错啦!';
            notice.error('{0}:比赛[ID:{1}]的报名失败了,原因:{2}'.format(gameIdMap[gameId], matchId, reason));
        }
    }

    static S_C_match_enroll_cancel(resp) {
        let code = resp.code;
        let gameId = verifyMgr.verify_gameId(resp.gameId);
        let matchId = verifyMgr.verify_matchId(resp.matchId);
        // console.log('[S_C_match_enroll_cancel]:', resp);
        if (verifyMgr.checkSuc(code)) {
            notice.success('{0}:成功取消比赛[ID:{1}]'.format(gameIdMap[gameId], matchId));
            dataView.doKey_enrollInfo({});
            dataView.showView();
        } else {
            let reason = resp.msg || '出错啦!';
            notice.error('{0}:取消比赛[ID:{1}]的报名失败了,原因:{2}'.format(gameIdMap[gameId], matchId, reason));
        }
    }

    static S_C_match_readyJoin_tips_ignore(resp) {

    }

    static S_C_match_readyJoin_tips(resp) {
        let matchJoinInfo = resp.data.matchJoinInfo;
        let isAutoJoin = matchJoinInfo.isAutoJoin;
        if (!isAutoJoin) {
            layer.open({
                type: 0,
                content: '你报名参加的比赛马上就要开始了？',
                title: false,
                btnAlign: 'c',
                closeBtn: 1,
                offset: 'auto',
                id: 'readyJoinBox',
                btn: ['马上进入', '忽略消息10s', '忽略消息30s'],
                yes: function (index, layero) {
                    layer.msg('已经进入游戏');
                },
                btn2: function (index, layero) {
                    layer.msg('忽略消息10s');
                    C_S_Handler.C_S_match_readyJoin_tips_ignore(10);
                },
                btn3: function (index, layero) {
                    layer.msg('忽略消息30s');
                    C_S_Handler.C_S_match_readyJoin_tips_ignore(30);
                }
            });
        } else {
            layer.msg('已经进入游戏');
        }
    }


}

let sendMgr = {
    send_chat_msg: function (msg) {
        if (!msg) {
            notice.error('发送的消息不能为空');
            return
        }
        if (!socket || socket.readyState !== socket.CONNECTING) {
            notice.error('WebSocket未连接,不能发送');
            return
        }
        socket.send(JSON.stringify({
            url: '/chat/msg_send',
            params: {'sendMsg': msg}
        }));
    },
};

//触发事件
let active = {
    refresh_gameOne: function (_this) {
        console.log('active-refresh_gameOne');
        let gameId = $(_this).data('gameid');
        console.log(gameId);
        C_S_Handler.C_S_match_infoList_get(gameId)
    },
    enroll: function (_this) {
        console.log('active-enroll');
        let matchId = _this.data('matchid');
        let gameId = _this.data('gameid');
        console.log(gameId);
        console.log(matchId);
        C_S_Handler.C_S_match_enroll_do(gameId, matchId)
    },
    del_enroll: function (_this) {
        console.log('active-del_enroll');
        let matchId = _this.data('matchid');
        let gameId = _this.data('gameid');
        // sendMgr.send_match_del_enroll(gameId, matchId);
        C_S_Handler.C_S_match_enroll_cancel(gameId, matchId);
    },
    enrollInfo: function (_this) {
        console.log('active-enrollInfo');
        console.log(_this);
    }
};


let sendMsg = function () {
    msg = $('#readysend_Msg').val();
    console.log('active-sendMsg', msg);
    if (!msg) {
        return
    }
    sendMgr.send_chat_msg(msg);
    msg = $('#readysend_Msg').val('');
};
let clearHistoryMsg = function () {
    lastShowMsgTime = 0;
    $('#msg_box_div').html('');
};


urlApi_callBack = {
    '/chat/msg_send': actionMgr.do_send_chat_msg,
    '/chat/msg_accept': actionMgr.do_accept_chat_msg,
};

