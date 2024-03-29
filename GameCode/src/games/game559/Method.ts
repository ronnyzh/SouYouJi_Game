/**
 * Created by Administrator on 2018/4/13.
 */
module G559 {
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
        };

        //--------------操作类型
        export let ACTION_TYPE = {
            NO_DISCARD: 0,
            DISCARD: 1
        };

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
            console.log('断开游戏链接')
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

        //计时工具
        export function setTimeout(callback, during) {
            Laya.timer.once(during, this, function () {
                if (callback) callback();
            })
        }
        export function clearTimeout() {
            Laya.timer.clearAll(this);
        }

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
        // var KEY_ON_EXIT = 'g559-onExitRoom-method';
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

        // export function setOnExitRoom(methodStringify) {
        //     Laya.LocalStorage.setItem(KEY_ON_EXIT, methodStringify);
        // }

        export function exitRoomHandler(msgData, finishedListener) {
            //console.log('onGoldExitRoomResult' ,msgData)
            if (msgData['result']) {
                UserMgr.inst.returnToLobby();
            } else {
                NetHandlerMgr.netHandler.sendData(ProtoKeyParty.C_S_EXIT_ROOM_CONFIRM);
            }
            if (finishedListener) finishedListener();

            // try {
            //     let exitRoomMethodString = Laya.LocalStorage.getItem(KEY_ON_EXIT);
            //     console.log('exitRoomHandler', arguments, exitRoomMethodString);
            //
            //     if (typeof finishenListener == 'function')finishenListener();
            //
            //     let success = msgData['result'];
            //     let msg = msgData['reason'];
            //     if (exitRoomMethodString) {
            //         let method = jx.once(this, function () {
            //             let func = ON_EXIT_METHOD[exitRoomMethodString];
            //             func.call(this, success, msg);
            //             clearOnExitRoom();
            //         });
            //         method();
            //     } else {
            //         //如果没有设置onExitRoom，则当做服务器踢人处理
            //         if (success) {
            //             msg ? Alert.show(msg || '您已退出房间').onYes(exitToLobby) : exitToLobby();
            //         }
            //     }
            // } catch (e) {
            //     console.error(e);
            // }

        }


        // //真正的换房函数
        // function _changeGoldRoom() {
        //     Laya.LocalStorage.removeItem(KEY_ON_EXIT);
        //
        //     Control.isPlayerMgrBuild = false;
        //     Control.playerMgr.clearOther();
        //     Control.playerSelf.reset();
        //     //重连后清除金币场操作
        //     setRefreshGameData(this, function (data) {
        //         console.log('重连后清除金币场操作', arguments);
        //         clearGameEnd();
        //         // clearOnExitRoom();
        //         Control.buttonMgr.isGoldOperatin = false;
        //     });
        //
        //     NetHandlerMgr.netHandler.disconnect();
        //     Game.Gmaster.reconnectNetHandler();
        //     // Game.page.refreshInfo();
        // }

        //换房封装流程
        export function changeRoom() {
            if (NetHandlerMgr.netHandler != null && NetHandlerMgr.netHandler.sendExitRoom != null && NetHandlerMgr.netHandler.valid())
                NetHandlerMgr.netHandler.sendChangeRoom(function (msgData) {
                    //console.log('-sendChangeRoom-',msgData);
                    if (msgData['result']) {
                        setRefreshGameData(this, function (data) {
                            //console.log('重连后清除金币场操作', arguments);
                            clearGameEnd();
                            // clearOnExitRoom();
                            Control.buttonMgr.isGoldOperatin = false;
                        });

                        Control.isPlayerMgrBuild = false;
                        Control.playerMgr.clearOther();
                        Control.playerSelf.reset();
                        if (NetHandlerMgr.netHandler != null) {
                            NetHandlerMgr.netHandler.disconnect();
                        }
                        Game.Gmaster.reconnectNetHandler();
                        // NetHandlerMgr.netHandler.disconnect();
                        // this.reset();
                        // var params = NetHandlerMgr.lastConnectParams;
                        // NetHandlerMgr.netHandler.connect(params,this.reconnectResult.bind(this));

                    }
                }.bind(this));
            // if (NetHandlerMgr.netHandler.valid()) {
            //     setOnExitRoom(ON_EXIT_TYPE.CHANGE);
            //     NetHandlerMgr.netHandler.sendChangeRoom();
            // } else {
            //     Alert.show('网络已断开无法切换房间');
            // }
        }

        // export function _changeRoomOnExit(success, msg) {
        //     if (success) {
        //         _changeGoldRoom();
        //     } else {
        //         Alert.show(msg || '游戏中无法切换房间，是否结束后切换', true)
        //             .onYes(function () {
        //                 //游戏结束后，不发准备
        //                 setGameEnd(this, function () {
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
            // setTimeout(function () {
            //     Game.page.onDispose();
            //     MasterMgr.inst.switch('lobby', false);
            // }, 30)
        }

        export function exitRoom(isDoNow = false) {
            if (isDoNow)
                exitToLobby();
            else
                if (NetHandlerMgr.netHandler != null && NetHandlerMgr.netHandler.sendExitRoom != null && NetHandlerMgr.netHandler.valid()) {
                    NetHandlerMgr.netHandler.sendExitRoom();
                }
                else {
                    UserMgr.inst.returnToLobby();
                }
            // let exit = this.exitToLobby;
            //
            // if (isDoNow) {
            //     return exit();
            // }
            //
            // if (NetHandlerMgr.netHandler.valid()) {
            //     Alert.show('是否确认退出房间', true)
            //         .onYes(function () {
            //             setOnExitRoom(ON_EXIT_TYPE.EXIT);
            //             NetHandlerMgr.netHandler.sendExitRoom();
            //         });
            //
            // } else {
            //     exit();
            // }
        }

        // export function _exitRoomOnExit(success, msg) {
        //     var exit = this.exitToLobby;
        //     if (success) {
        //         exit();
        //     } else {
        //         //游戏结束后，不发准备
        //         setGameEnd(this, function () {
        //             return false;
        //         });
        //         setOnExitRoom(ON_EXIT_TYPE.EXIT_SUCCESS);
        //
        //         //发送确认退房协议
        //         NetHandlerMgr.netHandler.sendExitRoomConfirm();
        //     }
        // }
        //
        // export function _exitRoomSuccess() {
        //     //保证发送确认退房后，马上退房
        //     this.exitToLobby();
        // }


    }
}