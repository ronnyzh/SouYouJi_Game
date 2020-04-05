/**
 * Created by Administrator on 2018/4/11.
 */
module G561 {
    export interface playerManagerData {
        playerList: any;
        MAX_PLAYER_COUNT: number;

        reset: Function;
        talkAction: void;

        checkPlaying: Function;
        getNextPlaying: Function;
        getPlayingList: Function;
        getPlayingSides: Function;
    }


    export namespace fl {
        export let playerManager;
        export let playerSelf;
        export let playerOther;
        export let getPlayer;
        export let getPlayerServer;
        export let getLocalPos;
        export let getServerPos;

        export class PlayerManager {
            constructor() {

            }

            static init(MethodCreatePlayer) {
                return fl.playerManager = new Vuet({
                    data: {
                        count: 0,
                        server_local: [],
                        server_self: 0,

                        local_server: [],
                        local_self: 0,
                        gameStage: null,
                    },

                    params: {
                        otherList: [],
                        playerList: [],
                        gamePlayers: [],
                        isbuild: null,
                        MAX_PLAYER_COUNT: 5,
                        _map_playercount2side: {
                            5: [0, 1, 2, 3, 4],
                            2: [0, 2]
                        },

                        TIPS_ID_CALL: 4,
                        TIPS_ID_ROB: 5,
                        TIPS_ID_NO_CALL: 6,
                        TIPS_ID_NO_ROB: 7,
                        TIPS_ID_NO_DISCARD: 8,
                        TIPS_ID_NO_SCORE1: 1,
                        TIPS_ID_NO_SCORE2: 2,
                        TIPS_ID_NO_SCORE3: 3,
                    },

                    watch: {
                        gameStage: function (newValue) {
                            let self = (<playerManagerData>this);
                            var isGameEnd = newValue == Method.GAME_STAGE.GAME_READY;
                            //console.log('playerManager watch gamestage:', newValue, ',isGameEnd:', isGameEnd);


                            if (isGameEnd) {
                                self.reset();
                            }
                        }
                    },

                    created: function () {
                        fl.getPlayer = this.getPlayer;
                        fl.getPlayerServer = this.getPlayerServer;
                        fl.getLocalPos = this.getLocalSide;
                        fl.getServerPos = this.getServerSide;

                        Control.roominfo.watch('gameStage', function (newValue) {
                            if (Method.GAME_STAGE.GAMEEND == newValue) {
                                this.clearReadyPlayer();
                            }

                        }.bind(this))

                        //初始化玩家列表
                        let list = this.playerList;
                        for (let index = 0; index < 3; index++) {
                            let player = this.createPlayer(index);
                            player.reset();
                            list[index] = player;
                        }
                        //特殊映射
                        fl.playerSelf = list[0];
                        let oterlist = list.concat();
                        oterlist.splice(0, 1);
                        fl.playerOther = this.otherList = oterlist;

                        //初始化假的玩家位置列表 作用：快速进房间后显示的名字不打码
                        this.server_local = { [0]: 0 };
                        this.local_server = { [0]: 0 };
                        this.local_self = 0;
                        this.server_self = 0;

                    },

                    method: {
                        //------------------开放调用
                        build: function (gameInfo) {
                            let roomInfo = gameInfo['roomInfo'];
                            let selfInfo = gameInfo['selfInfo'];

                            if (this.isbuild) {

                                this.initSide(selfInfo['side'], roomInfo['playerCount']);
                                return;
                            }


                            this.count = roomInfo['playerCount'];

                            this.initSide(selfInfo['side'], roomInfo['playerCount']);
                            this.initPlayer(roomInfo['playerCount'], roomInfo['playerList']);

                            this.isbuild = true;

                            fl.roominfo.watch('gameStage', function (newValue) {
                                this.gameStae = newValue;
                            }.bind(this))
                        },

                        getSexServer(serverside) {
                            return this.getPlayerServer(serverside).sex;
                        },

                        getServerSide(localside) {
                            return this.local_server[localside];
                        },

                        getLocalSide(serverside) {
                            return this.server_local[serverside];
                        },

                        getPlayer(localside) {
                            return this.playerList[localside] || null;
                        },

                        getPlayerServer(serverSide) {
                            var localside = this.getLocalSide(serverSide);
                            return this.playerList[localside] || null;
                        },
                        getPlayerList() {
                            return this.playerList.reduce(function (acc, cur) {
                                return cur ? acc.concat(cur) : acc;
                            }, [])
                        },

                        removeReadyPlayer(serverSide) {
                            let idx = this.gamePlayers.indexOf(serverSide);
                            if (idx == -1) {
                                this.gamePlayers.splice(idx, 1);
                            }
                        },

                        readyPlayer(serverSide) {
                            //console.log('readyPlayer', serverSide);
                            let idx = this.gamePlayers.indexOf(serverSide);
                            if (idx == -1) {
                                this.gamePlayers.push(serverSide);
                            }
                            Method.getPlayerServer(serverSide).isReady = true;
                        },
                        clearReadyPlayer() {
                            this.gamePlayers = [];

                        },

                        getReadyList() {
                            return this.gamePlayers;
                        },

                        addPlayer(data) {

                            let player = this.getPlayerServer(data['side']);
                            player.update(data);

                        },

                        clearOther() {
                            this.otherList.forEach(function (player) {
                                player.clear();
                            })
                        },

                        clear() {
                            this.clearCountdown();
                            this.playerList.forEach(function (player) {
                                player.clear();
                            })
                        },

                        update() {
                            //console.log('update', arguments);
                        },

                        reset() {
                            this.clearCountdown();

                            this.playerList.forEach(function (player) {
                                player.reset();
                            })
                        },

                        setSelfSeat() {
                            let data = {};
                            data['nickname'] = UserMgr.inst._info.name;
                            data['headImgUrl'] = UserMgr.inst._info.imgUrl;
                            data['coin'] = '';
                            let selfPlayer = this.getPlayer(0);
                            if (selfPlayer.nickname == null || selfPlayer.nickname == '') {
                                selfPlayer.update(data);
                            }
                        },

                        //头像高光
                        setTurnAnimate: function (localSide) {
                            let serverSide = Method.getServerPos(localSide);



                            if (serverSide == null || localSide == null) return;
                            var doChangePage = function (controller: fairygui.Controller, name) {
                                if (controller.selectedPage != name) {
                                    controller.setSelectedPage(name);
                                }
                            };
                            this.playerList.forEach(function (player) {
                                // //console.log('setTurnAnimate',localSide,serverSide,player.side == serverSide);
                                if (player.side == serverSide) {
                                    doChangePage(player.turnController, 'on');
                                } else {
                                    doChangePage(player.turnController, 'off');
                                }
                            })

                        },

                        //倒计时

                        setCountdown(localside, time?, callback?) {
                            let player = this.getPlayer(localside);
                            let count = time || Control.roominfo.defaultCountdown || 7;
                            this.clearCountdown();
                            if (typeof callback == 'function')
                                var timeCB = jx.once(this, callback);
                            player.countdown = count;
                            Laya.timer.loop(1000, this, function () {
                                player.countdown = --count;
                                if (count <= 0) {
                                    this.clearCountdown();
                                    if (timeCB) timeCB();
                                }

                            })
                        },

                        clearCountdown() {
                            Laya.timer.clearAll(this);
                            this.playerList.forEach(function (player) {
                                player.countdown = null;
                            })
                        },

                        //操作对话框
                        talkAction(serverSide, action) {
                            if (serverSide == null) return;
                            if (serverSide == Control.posServerSelf && action == ACTION.LOOKTILE) {
                                playerSelf.talkAction(action);

                            } else {
                                let player = this.getPlayerServer(serverSide);
                                player.talkAction(action);
                                player.handwall.showAction(action);
                            }
                        },
                        //玩家头像pk按钮
                        showSelectPK(serverSide, callback) {
                            var selected = false;
                            var handller = function (player) {
                                if (selected) return;
                                if (!player.isEmpty && serverSide.indexOf(player.side) !== -1) {
                                    selected = true;
                                    this.clearSelectPK();
                                    callback(player.side);
                                }
                            }.bind(this);
                            this.otherList.forEach(player => {
                                if ((player.isEmpty) || serverSide.indexOf(player.side) == -1) {
                                    player.canSelectPK = false;
                                    player.clearClickCallback();
                                } else {
                                    player.canSelectPK = true;
                                    player.setClickCallback(handller)
                                }
                            })
                        },
                        clearSelectPK() {
                            this.otherList.forEach(player => {
                                player.canSelectPK = false;
                                player.clearClickCallback();
                            })
                        },

                        //--------------------------

                        createPlayer: function (localSide) {
                            return MethodCreatePlayer(localSide);
                        },

                        //----------------初始化玩家
                        initPlayer: function (playerCount, datas) {
                            let self = <playerManagerData>this;
                            //console.log('initPlayer', arguments);
                            var list = self.playerList;
                            //如果有玩家数据则整理数据
                            if (datas) {
                                var _o;
                                var side2Data = Object.keys(_o = datas).reduce(function (acc, key) {
                                    let val = _o[key];
                                    let side = val['side'];
                                    acc[side] = val;
                                    return acc;
                                }, {});
                            }
                            //创建玩家对象
                            var localSideMap = this.getSideListByCount(playerCount);
                            for (let localSide = 0; localSide < self.MAX_PLAYER_COUNT; localSide++) {

                                //获取玩家对象
                                let player = this.getPlayer(localSide);
                                if (player == null) {
                                    player = this.createPlayer(localSide);
                                    player.reset();
                                    list[localSide] = player;
                                }

                                //不在展示列表则跳出
                                if (localSideMap.indexOf(localSide) == -1) {
                                    player.hide();
                                    continue;
                                }

                                //如果有数据则填写数据
                                if (datas) {
                                    var serverSide = this.getServerSide(localSide);
                                    var oneData = side2Data[serverSide];
                                    if (oneData) {
                                        player.update(oneData);
                                    } else {
                                        player.hide();
                                    }
                                }
                            }

                            //特殊映射
                            fl.playerSelf = list[0];
                            let oterlist = list.concat();
                            oterlist.splice(0, 1);
                            fl.playerOther = this.otherList = oterlist;
                        },

                        //------------------

                        //------------------位置部分
                        //获取玩家side对应 localside位置的列表
                        getSideListByCount: function (count) {
                            var list = this['_map_playercount2side'][count];
                            if (!list) {
                                list = [];
                                for (let i = 0; i < count; i++) {
                                    list.push(i);
                                }
                            }
                            return list;
                        },

                        //初始化位置
                        initSide: function (selfServer, playerCount) {
                            let map_server2local = {};
                            let map_local2server = {};
                            var currentSide = selfServer;
                            let playerCountSide = this.getSideListByCount(playerCount);
                            for (let i = 0; i < playerCount; i++) {
                                map_server2local[currentSide] = playerCountSide[i];
                                map_local2server[playerCountSide[i]] = currentSide;

                                currentSide = ++currentSide >= playerCount ? 0 : currentSide;
                            }

                            this.server_local = map_server2local;
                            this.local_server = map_local2server;
                            this.local_self = 0;
                            this.server_self = selfServer;
                        },

                        //玩家是否游戏中
                        checkPlaying: function (serverSide) {
                            let player: playerTemplateData = this.getPlayerServer(serverSide);
                            return Boolean(player && !player.gameover);
                        },

                        getPlayingList: function () {
                            let self = <playerManagerData>this;
                            return self.playerList.reduce(function (acc: Array<playerTemplateData>, cur: playerTemplateData) {
                                return !cur.isEmpty && !cur.gameover ? acc.concat(cur) : acc;
                            }, []);
                        },
                        getPlayingSides: function () {
                            let self = <playerManagerData>this;
                            return self.getPlayingList().map(function (item) { return item.side });
                        },

                        //获取下一个游戏中的玩家
                        getNextPlaying: function (serverSide) {
                            let self = <playerManagerData>this;
                            let player = this.getPlayerServer(serverSide);
                            let inGameList = self.getPlayingList();
                            let idx = this.playerList.indexOf(player);
                            let list = this.playerList.concat();
                            let left = list.splice(0, idx);
                            list.shift();
                            let right = list;
                            let total = [].concat(right, left);
                            for (let item in total) {
                                if (inGameList.indexOf(total[item]) != -1) {
                                    return total[item];
                                }
                            }
                            return null;
                        }

                    }
                })
            }
        }
    }
}