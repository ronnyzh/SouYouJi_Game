module G559 {
    interface playerManagerData {

        reset: Function;
    }


    export namespace rf {
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
                return rf.playerManager = new Vuet({
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
                        isbuild: null,
                        _map_playercount2side: {
                            5: [0, 1, 2, 3, 4]
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
                            //console.log('playerManager watch gamestage:', newValue,',isGameEnd:', isGameEnd);


                            if (isGameEnd) {
                                self.reset();
                            }
                        }
                    },

                    created: function () {
                        rf.getPlayer = this.getPlayer;
                        rf.getPlayerServer = this.getPlayerServer;
                        rf.getLocalPos = this.getLocalSide;
                        rf.getServerPos = this.getServerSide;

                        //初始化玩家列表
                        let list = this.playerList;
                        for (let index = 0; index < 3; index++) {
                            let player = this.createPlayer(index);
                            player.reset();
                            list[index] = player;
                        }
                        //特殊映射
                        rf.playerSelf = list[0];
                        let oterlist = list.concat();
                        oterlist.splice(0, 1);
                        rf.playerOther = this.otherList = oterlist;

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

                            rf.roominfo.watch('gameStage', function (newValue) {
                                this.gameStae = newValue;
                            }.bind(this))
                        },

                        getServerSide(localside) {
                            var result = this.local_server[localside];
                            return result == null ? null : result;
                        },

                        getLocalSide(serverside) {
                            var result = this.server_local[serverside];
                            return result == null ? null : result;
                        },

                        getPlayer(localside) {
                            return this.playerList[localside] || null;
                        },

                        getPlayerServer(serverSide) {
                            var localside = this.getLocalSide(serverSide);
                            return this.playerList[localside] || null;
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
                            console.log('update', arguments);
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


                        setCountdown(localside, time?, callback?) {
                            let player = this.getPlayer(localside);

                            let count = time || 15;
                            this.clearCountdown();
                            if (typeof callback == 'function')
                                var timeCB = jx.once(this, callback);

                            if (player) player.countdown = count;
                            Laya.timer.loop(1000, this, function () {
                                --count;
                                if (player) player.countdown = count;
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

                        //--------------------------

                        createPlayer: function (localSide) {
                            return MethodCreatePlayer(localSide);
                        },

                        //----------------初始化玩家
                        initPlayer: function (playerCount, datas) {
                            //console.log('initPlayer', arguments);
                            var list = this.playerList;
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
                            localSideMap.forEach(function (localSide) {
                                //获取玩家对象
                                let player = this.getPlayer(localSide);
                                if (player == null) {
                                    player = this.createPlayer(localSide);
                                    player.reset();
                                    list[localSide] = player;
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

                            }, this);

                            //特殊映射
                            rf.playerSelf = list[0];
                            let oterlist = list.concat();
                            oterlist.splice(0, 1);
                            rf.playerOther = this.otherList = oterlist;
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
                            for (let i = 0; i < playerCount; i++) {
                                map_server2local[currentSide] = i;
                                map_local2server[i] = currentSide;

                                currentSide = ++currentSide >= playerCount ? 0 : currentSide;
                            }

                            this.server_local = map_server2local;
                            this.local_server = map_local2server;
                            this.local_self = 0;
                            this.server_self = selfServer;
                        },


                    }
                })
            }
        }
    }
}