/**
 * Created by Administrator on 2018/4/11.
 */
module G559 {
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
    export namespace rf {
        export let roominfo;
        export class Roominfo {
            static init(delegate, component) {
                return rf.roominfo = new Vuet({
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
                    },
                    component: {
                        'tf_room_no': component['tf_room_no'],
                        'tfRoomDesc': component['tfRoomDesc']
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
                            component.text = ExtendMgr.inst.getText4Language("牌局编号：")+'{0}'.format(newValue);
                        },
                    },
                    method: {
                        reset: function () {
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