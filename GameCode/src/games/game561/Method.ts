/**
 * Created by Administrator on 2018/4/13.
 */
module G561 {
    export let ACTION_REFRESH = {
        GIVEUP: 1, //弃牌
        FIGHTLOSE: 2, //比牌失败
        ALL_IN: 3, //全压
    }
    export let ACTION = {
        GIVEUP: 1, //弃牌
        LOOKTILE: 2, //看牌
        FIGHTOTHER: 3, //比牌
        ALL_IN: 4, //全压
        ADDGOLD: 5, //加注
        FOLLOWGOLD: 6, //跟注
        SINGLE: 7, //孤注一掷
        FIGHTLOSE: 100, //比牌失败
    };
    export let ACTION_TILE = {
        NOTHING: 0, //无牌型
        BAOZI: 1,  //豹子
        SHUNJIN: 2,//顺金
        JINHUA: 3, //金花
        SHUNZI: 4, //顺子
        PAIR: 5,   //对子
        SINGLE: 6, //单牌

    }
    export namespace GMethod {
        //-------------方便调用方法
        export let getPlayer;
        export let getPlayerServer;
        export let getLocalPos;
        export let getServerPos;

        //-------------游戏状态
        export let GAME_STAGE = {
            WAIT_START: '-1', //等待开始
            GAME_READY: 0, //等待下一局
            WAIT_ROLL: 1, //等待roll点
            GAMING: 2, //游戏中
            GIVE_TILE: 3, //发牌
            WAIT_STRIVE: 4, // 抢庄
            AFTER_STRIVE: 5, // 抢庄完成做动画阶段
            PREPARE_GAME: 6, // 准备游戏阶段
            PAUSE: 7, // 游戏暂停阶段
            GAMEEND: 808, //游戏结束
        };

        //------------玩家操作
        export let Player;
        Player = {};
        Player.TIPS_ID_CALL = 4;
        Player.TIPS_ID_ROB = 5;
        Player.TIPS_ID_NO_CALL = 6;
        Player.TIPS_ID_NO_ROB = 7;
        Player.TIPS_ID_NO_DISCARD = 8;
        Player.TIPS_ID_NO_SCORE1 = 1;
        Player.TIPS_ID_NO_SCORE2 = 2;
        Player.TIPS_ID_NO_SCORE3 = 3;

        //-------------扑克牌
        interface i_CONSTANTS {
            RED_JOKER_ID: any;
            BLACK_JOKER_ID: any;
            cardNumMap: any;
            valueMap: any;
        }
        export let CONSTANTS = <i_CONSTANTS>{
            RED_JOKER_ID: "Bj",
            BLACK_JOKER_ID: "Lj",
        };

        CONSTANTS.cardNumMap = {};
        CONSTANTS.valueMap = {};

        (function () {
            var map = CONSTANTS.cardNumMap;
            for (var i = 2; i < 10; ++i) {
                map[i.toString()] = i;
            }
            map["T"] = 10;
            map["J"] = 11;
            map["Q"] = 12;
            map["K"] = 13;
            map["A"] = 14;
            //map["2"] = 15;
            map["L"] = 16;
            map["B"] = 17;

            jx.each(map, function (v, k) {
                CONSTANTS.valueMap[v] = k;
            });
        })();
        export function sortCardFunc(card1, card2) {
            // return this.compareCard(card1, card2) == 1;
            return getCardNumber(card2) > getCardNumber(card1);
        }
        export function getCardNumber(cardId) {
            var num = cardId[0];//.substring(0, cardId.length - 1);
            return CONSTANTS.cardNumMap[num];
        }
        export function getCardType(cardId) {
            return cardId.charAt(cardId.length - 1);
        }
        export function compareCard(id1, id2) {
            var num1 = getCardNumber(id1);
            var num2 = getCardNumber(id2);
            if (num1 == num2) {
                var type1 = this.getCardType(id1);
                var type2 = this.getCardType(id2);
                return type1 > type2 ? -1 : 1;
            }

            return num1 > num2 ? -1 : 1;
        }

        //格式化金币
        export let goldFormat = function (num) {
            // if (typeof num === 'string' || typeof num === 'number') {
            //     num = num.toString();
            //     num = num.replace(/([0-9]+\.?[0-9]+)/, function (match) {
            //         var match_int = parseInt(match).toString();
            //         switch (true) {
            //             case match_int.length > 8:
            //                 var num = match / Math.pow(10, 8);
            //                 return jx.floor2Fixed(num, 1) + "亿";
            //             case match_int.length > 7:
            //                 var num = match / Math.pow(10, 7);
            //                 return jx.floor2Fixed(num, 1) + "千万";
            //             case match_int.length > 4:
            //                 var num = match / Math.pow(10, 4);
            //                 return jx.floor2Fixed(num, 1) + "万";
            //             default:
            //                 return match;
            //         }
            //     });
            // }
            return jx.goldFormat(num);
        };

        //调整operationView层级
        var _operationIndexData = null;
        export let initOperationIndex = function () {
            if (_operationIndexData) return _operationIndexData;

            var view = page.view;
            var targetPanel = Control.playerSelf.handwall.getComponent('hand_pokers');
            var thePanel = Control.operationMgr.getComponent('operation');

            var targetIndex = view.getChildIndex(targetPanel);
            var theIndex = view.getChildIndex(thePanel);

            return _operationIndexData = {
                view: view,
                targetPanel: targetPanel,
                targetIndex: targetIndex,
                thePanel: thePanel,
                theIndex: theIndex
            }
        }
        //置顶到手牌之上
        export let topShowOperationIndex = function () {
            var data = initOperationIndex();
            var view = data.view;
            view.setChildIndex(data.thePanel, data.targetIndex + 1);
        };
        //还原位置
        export let resetOperationIndex = function () {
            var data = initOperationIndex();
            var view = data.view;
            view.setChildIndex(data.thePanel, data.theIndex);
            _operationIndexData = null;
        };

        //游戏开始后，不接收准备监听
        export let ignoreReady = function () {
            Control.roominfo.isGameStarted = true;
            NetHandlerMgr.netHandler.removeAllMsgListener(S_C_PLAYERREADYRESULT);
        }

        //计时工具
        export function setTimeout(callback, during) {
            Laya.timer.once(during, this, function () {
                if (callback) callback();
            })
        }
        export function clearTimeout() {
            Laya.timer.clearAll(this);
        }


        //判断游戏流程
        export let isPlayingGame = function () {
            return Method.checkGameStage(Control.roominfo.gameStage);
        }

        export let checkGameStage = function (stage) {
            var gamingStage = [
                GAME_STAGE.WAIT_START,
                GAME_STAGE.GAME_READY,
                GAME_STAGE.PREPARE_GAME,
            ];
            for (var i = 0; i < gamingStage.length; i++) {
                if (stage == gamingStage[i]) {
                    return false;
                }
            }
            return true;
        };

        //断开游戏链接
        export function disconnect() {
            //console.log('断开游戏链接')
            Gmaster.stopPoll();
            if (NetHandlerMgr.netHandler != null) {
                NetHandlerMgr.netHandler.disconnect();
            }
        }

        //开局清除退房协议
        export let cleanPlayerExit = function () {
            NetHandlerMgr.netHandler.removeAllMsgListener(ProtoKey.S_C_EXIT_ROOM);
            // NetHandlerMgr.netHandler.removeAllMsgListener(ProtoKey.S_C_JOIN_ROOM);
        };

        //---------游戏流程钩子函数
        //刷新
        var _onRefreshGameData;
        export function clearRefreshGameData() {
            _onRefreshGameData = null;
        }
        export function checkRefreshGameData(data): boolean {
            let _e = _onRefreshGameData;
            _onRefreshGameData = null;
            return _e ? _e(data) : true;
        }
        export function setRefreshGameData(caller, method, args = []) {
            _onRefreshGameData = jx.once(caller, method, args);
        }

        //游戏结束
        var _onGameEnd;

        export function clearGameEnd() {
            _onGameEnd = null;
        }

        export function checkGameEnd(): boolean {
            let _e = _onGameEnd;
            _onGameEnd = null;
            let result = _e ? _e() : true;
            //console.log('checkGameEnd', _onGameEnd, result);
            return result;
        }

        //设置游戏结束执行函数， 如果继续，一定要返回true
        export function setGameEnd(caller, method, args = []) {
            _onGameEnd = jx.once(caller, method, args);
        }


        //---------进出房操作
        export function clearOnExitRoom() {
            Laya.LocalStorage.removeItem('g560-onExitRoom-method');
        }

        /**
         * 设置收到退房时的操作，换房/退房
         * @param: methodStringify：
         * */
        // var KEY_ON_EXIT = 'g561-onExitRoom-method';
        // var ON_EXIT_TYPE = {
        //     EXIT: 10,
        //     EXIT_SUCCESS: 11,
        //     CHANGE: 20,
        //     CHANGE_SUCCESS: 21,
        // };
        // var ON_EXIT_METHOD = {};
        // ON_EXIT_METHOD[ON_EXIT_TYPE.EXIT] = _exitRoomOnExit;
        // ON_EXIT_METHOD[ON_EXIT_TYPE.EXIT_SUCCESS] = _exitRoomSuccess;
        // ON_EXIT_METHOD[ON_EXIT_TYPE.CHANGE] = _changeRoomOnExit;
        // ON_EXIT_METHOD[ON_EXIT_TYPE.CHANGE_SUCCESS] = _changeGoldRoom;
        //
        // export function setOnExitRoom(methodStringify){
        //     Laya.LocalStorage.setItem(KEY_ON_EXIT, methodStringify);
        // }
        export function exitRoomHandler(msgData, finishedListener) {
            //console.log('onGoldExitRoomResult', msgData)
            if (msgData['result']) {
                UserMgr.inst.returnToLobby();
            } else {
                NetHandlerMgr.netHandler.sendData(ProtoKeyParty.C_S_EXIT_ROOM_CONFIRM);
            }
            if (finishedListener) finishedListener();
            // //console.log('exitRoomHandler',msgData)
            // try{
            //     let exitRoomMethodString = Laya.LocalStorage.getItem(KEY_ON_EXIT);
            //     //console.log('exitRoomHandler',arguments, exitRoomMethodString);
            //
            //     if(typeof finishenListener =='function')finishenListener();
            //
            //     let success = msgData['result'];
            //     let msg = msgData['reason'];
            //     if(exitRoomMethodString){
            //         let method = jx.once(this, function(){
            //             let func = ON_EXIT_METHOD[exitRoomMethodString];
            //             func.call(this, success, msg);
            //             clearOnExitRoom();
            //         });
            //         method();
            //     }else{
            //         //如果没有设置onExitRoom，则当做服务器踢人处理
            //         if(success){
            //             msg ? Alert.show(msg|| '您已退出房间').onYes(exitToLobby) : exitToLobby();
            //         }
            //     }
            // }catch(e){console.error(e);}

        }
        //
        // //真正的换房函数
        // function _changeGoldRoom(){
        //     Laya.LocalStorage.removeItem(KEY_ON_EXIT);
        //
        //     Control.isPlayerMgrBuild = false;
        //     Control.playerMgr.clearOther();
        //     Control.playerSelf.reset();
        //     //重连后清除金币场操作
        //     setRefreshGameData(this, function(data){
        //         //console.log('重连后清除金币场操作',arguments);
        //         clearGameEnd();
        //         // clearOnExitRoom();
        //         Control.buttonMgr.isGoldOperatin = false;
        //
        //         //重连后开放准备响应
        //         Control.roominfo.isGameStarted = false;
        //     });
        //
        //     NetHandlerMgr.netHandler.disconnect();
        //     Game.Gmaster.reconnectNetHandler();
        //     // Game.page.refreshInfo();
        // }
        //换房封装流程
        export function changeRoom() {
            if (NetHandlerMgr.netHandler != null && NetHandlerMgr.netHandler.sendExitRoom != null && NetHandlerMgr.netHandler.valid()) {
                NetHandlerMgr.netHandler.sendChangeRoom(function (msgData) {
                    if (msgData['result']) {
                        setRefreshGameData(this, function (data) {
                            clearGameEnd();
                            Control.buttonMgr.isGoldOperatin = false;
                        });
                        Control.isPlayerMgrBuild = false;
                        Control.playerMgr.clearOther();
                        Control.playerSelf.reset();
                        if (NetHandlerMgr.netHandler != null) {
                            NetHandlerMgr.netHandler.disconnect();
                        }
                        Game.Gmaster.reconnectNetHandler();
                    }
                }.bind(this));
            }
            // if(NetHandlerMgr.netHandler.valid()){
            //     setOnExitRoom(ON_EXIT_TYPE.CHANGE);
            //     Gmaster.startPoll();
            //     NetHandlerMgr.netHandler.sendChangeRoom();
            // }else{
            //     Alert.show('网络已断开无法切换房间');
            // }
        }
        // export function _changeRoomOnExit(success, msg){
        //     if(success){
        //         _changeGoldRoom();
        //     }else{
        //         Alert.show(msg || '游戏中无法切换房间，是否结束后切换', true)
        //             .onYes(function(){
        //                 //游戏结束后，不发准备
        //                 setGameEnd(this, function(){
        //                     return false;
        //                 });
        //                 //防止收到退房被踢出，马上换房
        //                 setOnExitRoom(ON_EXIT_TYPE.CHANGE_SUCCESS);
        //                 //发送确认换房协议
        //                 NetHandlerMgr.netHandler.sendChangeRoomConfirm();
        //             }.bind(this));
        //     }
        // }

        //退房
        export function exitToLobby() {
            UserMgr.inst.returnToLobby();
            // Laya.LocalStorage.removeItem(KEY_ON_EXIT);
            // setTimeout(function(){
            //     Game.page.onDispose();
            //     MasterMgr.inst.switch('lobby',false);
            // },30)
        }
        export function exitRoom(isDoNow = false) {
            if (isDoNow) {
                exitToLobby();
            }
            else {
                if (NetHandlerMgr.netHandler != null && NetHandlerMgr.netHandler.valid() && NetHandlerMgr.netHandler.sendExitRoom != null) {
                    NetHandlerMgr.netHandler.sendExitRoom();
                }
                else {
                    UserMgr.inst.returnToLobby();
                }
            }

            // let exit = this.exitToLobby;
            //
            // if(isDoNow){
            //     return exit();
            // }
            //
            // if(NetHandlerMgr.netHandler.valid()){
            //     Alert.show('是否确认退出房间', true)
            //         .onYes(function(){
            //             setOnExitRoom(ON_EXIT_TYPE.EXIT);
            //             NetHandlerMgr.netHandler.sendExitRoom();
            //         });
            //
            // }else {
            //     exit();
            // }
        }

        // export function _exitRoomOnExit(success, msg){
        //     var exit = this.exitToLobby;
        //     if(success){
        //         exit();
        //     } else{
        //         //游戏结束后，不发准备
        //         setGameEnd(this, function(){
        //             return false;
        //         });
        //         setOnExitRoom(ON_EXIT_TYPE.EXIT_SUCCESS);
        //
        //         //发送确认退房协议
        //         NetHandlerMgr.netHandler.sendExitRoomConfirm();
        //     }
        // }
        //
        // export function _exitRoomSuccess (){
        //     //保证发送确认退房后，马上退房
        //     this.exitToLobby();
        // }


    }
}