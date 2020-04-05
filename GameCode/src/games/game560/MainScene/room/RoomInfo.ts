/**
 * Created by Administrator on 2018/4/11.
 */
module G560 {
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
                        currentRound: "",
                        playerCount: "",
                        tileCount: "",

                        gameStage: null,

                        multiple: 0,
                        holeCards: null,
                        baseScore: null,
                        boomLimit: 0,
                    },
                    component: {
                        'tf_room_no': component['tf_room_no'],
                        'tfRoomDesc': component['tfRoomDesc'],

                        //斗地主信息
                        'conLandlordInfo': component['conLandlordInfo'],
                        // 'tfBoomCount': component['tfBoomCount'],
                        // 'tfMultiple': component['tfMultiple'],
                        'conHoldcard': component['conHoldcard'],
                        'conHoldCardBG': component['conHoldCardBG'],
                    },
                    created: function () {
                        this.multiple = null;
                        this.boomLimit = null;
                    },
                    watch: {
                        roomSetting: function (newValue) {
                            let value = newValue.split('：');
                        
                            // let score = parseInt(value[1]);
                            let score = value[1];

                            newValue = value[0] + "：" + score;
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

                        multiple: function (newValue) {
                            if (Control.playerMgr)
                                Control.playerMgr.playerList.forEach(player => {
                                    player.boomMultiple = newValue;
                                })
                            // let component = this.getComponent('tfMultiple');
                            // newValue = newValue == null ? '-': 'x'+ newValue;
                            // component.text = newValue;
                        },

                        boomLimit: function (newValue) {
                            // let component = this.getComponent('tfBoomCount');
                            // newValue = newValue == null ? '-': 'x'+ newValue;
                            // component.text = newValue;
                        },

                        holeCards: function (newValue) {
                            let isShow = Boolean(newValue);
                            let conList = this.getComponent('conHoldcard').asList;
                            conList.visible = isShow;
                            conList.removeChildrenToPool();
                            if (newValue) {
                                newValue.forEach(function (cardNum, idx) {
                                    var tile = conList.addItemFromPool().asCom;
                                    let img = tile.getChildAt(0).asLoader;
                                    img.url = fl.Handwall.getCardPath(cardNum);
                                })
                            }
                        },

                        gameStage: function (newValue) {
                            this.getComponent('conHoldCardBG').visible = Method.isPlayingGame();
                            this.getComponent('conHoldcard').visible = Method.isPlayingGame();
                        },
                    },
                    method: {
                        reset: function () {
                            //this.multiple= null;
                            this.holeCards = null;
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
                    }
                })
            }
        }
    }
}