/**
 * Created by Administrator on 2018/4/11.
 */
module G561 {
    interface roomInfoData {
        roomId?: string | number;
        roomName?: string;
        timestamp?: string;
        playerList?: string;
        roomSetting?: string;
        count?: string;
        ownerSide?: string;
        currentRound?: string;
        playerCount?: string;
        tileCount?: string;
        _u_data?: string;
        gameStage?: string | number | any;
    }
    export namespace fl {
        export let roominfo;
        export class Roominfo {
            static init(delegate, component) {
                return fl.roominfo = new Vuet({
                    data: {
                        roomId: "",
                        roomName: "",
                        timestamp: "",
                        playerList: "",
                        roomSetting: "",
                        count: "",
                        ownerSide: "",

                        sideRoundStart: 0,
                        currentRound: 0,
                        playerCount: "",
                        tileCount: "",

                        gameStage: null,
                        baseScore: 1,
                        defaultCountdown: 15, //默认倒计时
                        isGameStarted: false,
                        //----炸金花
                        // danzhu:0,
                        zongzhu: 0,
                        totalRound: 20,
                    },
                    component: {
                        'tf_room_no': component['tf_room_no'],
                        'tfRoomDesc': component['tfRoomDesc'],

                        //----炸金花
                        'tfDanzhu': component['tfDanzhu'],
                        'tfZongzhu': component['tfZongzhu'],
                        'tfLunshu': component['tfLunshu'],
                    },
                    created: function () {
                        this.zongzhu = 0;
                    },
                    watch: {
                        roomSetting: function (newValue) {
                            var component = this.getComponent('tfRoomDesc');
                            if (newValue) {
                                component.visible = true;
                                component.text = newValue;
                            } else {
                                component.visible = false;
                            }
                        },
                        roomId: function (newValue) {
                            var component = this.getComponent('tf_room_no');
                            component.text = ExtendMgr.inst.getText4Language("牌局编号：") + '{0}'.format(newValue);
                        },

                        //----炸金花
                        currentRound: function (newValue) {
                            var current = newValue == null ? '-' : newValue;
                            var total = this.totalRound;
                            var str = current + (total ? '/' + total : '');
                            let temp = ExtendMgr.inst.lan == ExtendMgr.CN ? '' : '\n';
                            this.getComponent('tfLunshu').text = `[color=#BBBBBB]${ExtendMgr.inst.getText4Language('轮数:')}[/color]${temp}[color=#FFCC00][i]${str}[/i][/color]`;
                        },

                        totalRound: function (newValue) {
                            var current = this.currentRound == null ? '' : this.currentRound;
                            var total = newValue;
                            var str = current + (total ? '/' + total : '');
                            let temp = ExtendMgr.inst.lan == ExtendMgr.CN ? '' : '\n';
                            this.getComponent('tfLunshu').text = `[color=#BBBBBB]${ExtendMgr.inst.getText4Language('轮数:')}[/color]${temp}[color=#FFCC00][i]${str}[/i][/color]`;
                        },

                        baseScore: function (newValue) {
                            let temp = ExtendMgr.inst.lan == ExtendMgr.CN ? '' : '\n';
                            this.getComponent('tfDanzhu').text = `[color=#BBBBBB]${ExtendMgr.inst.getText4Language('单注:')}[/color]${temp}[color=#FFCC00][i]${Tools.inst.changeGoldToMoney(newValue)}[/i][/color]`;
                        },

                        zongzhu: function (newValue) {
                            let temp = ExtendMgr.inst.lan == ExtendMgr.CN ? '' : '\n';
                            this.getComponent('tfZongzhu').text = `[color=#BBBBBB]${ExtendMgr.inst.getText4Language('总注:')}[/color]${temp}[color=#FFCC00][i]${Tools.inst.changeGoldToMoney(newValue)}[/i][/color]`;
                        },




                    },
                    method: {
                        reset: function () {
                            this.multiple = null;
                            this.holeCards = null;

                            this.zongzhu = 0;
                            this.totalRound = 20;
                            this.baseScore = 0;
                            // this.boomLimit= null;
                        },
                        update: function (data) {
                            // this.roomId = data.roomId;
                            this._u_data = data;
                        },

                        setStart: function () {
                            this.gameStage = Method.GAME_STAGE.GAME_READY;
                        },

                        isGameStart: function () {
                            return this.currentRound > 0;
                        },
                        //以此玩家作为每一轮更新的起点

                        onPlayerGameover: function (serverSide) {
                            if (serverSide == this.sideRoundStart) {
                                let nextPlayer = Control.playerMgr.getNextPlaying(this.sideRoundStart);
                                if (nextPlayer) {
                                    this.sideRoundStart = nextPlayer.side;
                                }
                            }
                        },
                        roundEmmit: function (side, setRound?) {
                            if (setRound != null) {
                                if (side != null) {
                                    this.lastSide = side;
                                    this.sideRoundStart = side;
                                }
                                this.currentRound = setRound;
                            } else {
                                //检查初始玩家是否结束游戏
                                let oldSideRound = null;
                                let isSideRoundGameOver = !Control.playerMgr.checkPlaying(this.sideRoundStart);
                                if (isSideRoundGameOver) {
                                    //已经结束游戏换下家
                                    let next = Control.playerMgr.getNextPlaying(this.sideRoundStart);
                                    oldSideRound = this.sideRoundStart;
                                    this.sideRoundStart = next.side;
                                }
                                if (this.sideRoundStart == side && this.lastSide != side && (!isSideRoundGameOver || this.lastSide != oldSideRound)) {
                                    this.currentRound++;
                                }
                                this.lastSide = side;
                            }
                        },
                    }
                })
            }
        }
    }
}