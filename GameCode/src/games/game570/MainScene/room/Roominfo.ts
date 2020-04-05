module G570 {
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
        information?: string;
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
                        information: '',
                        setfilpcards: Boolean,
                        LastcardList: "",

                        gameStage: null,

                        multiple: 1,
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
                        'doubleNumtxt': component['doubleNumtxt'],
                        'informationTxt': component['informationTxt'],
                        "difenTxt": component['difenTxt'],
                        'filpcards': component['filpcards'],
                    },
                    created: function () {
                        this.multiple = null;
                        this.boomLimit = null;
                    },
                    watch: {
                        roomSetting: function (newValue) {
                            //console.log("======roomSetting======");
                            let value = newValue.split('：');
                            // let score = parseInt(value[1]);
                            let score = value[1];
                            newValue = ExtendMgr.inst.getText4Language(value[0]) + "：" + score;
                            var component = this.getComponent('difenTxt');
                            if (newValue) {
                                component.visible = true;
                                component.text = newValue;
                                this.getComponent('conHoldCardBG').visible = true;
                                this.getComponent('conHoldcard').visible = true;
                                this.getComponent('difenTxt').visible = true;
                                this.getComponent('doubleNumtxt').visible = true;
                                this.getComponent('informationTxt').visible = true;
                                this.getComponent('doubleNumtxt').text = "X1";
                                this.getComponent('informationTxt').text = ExtendMgr.inst.getText4Language('地主让0张');
                            } else {
                                // component.visible = false;
                            }
                        },
                        roomId: function (newValue) {
                            var component = this.getComponent('tf_room_no');
                            //component.text = '牌局编号：\n{0}'.format(newValue);
                            component.text = newValue;
                        },
                        multiple: function (newValue) {
                            //  console.log(newValue, "==========multiple");
                            let component = this.getComponent('doubleNumtxt');
                            component.visible = true;
                            newValue = newValue == null ? '' : 'X' + newValue.toString();
                            component.text = newValue;
                        },
                        //让牌数  
                        information: function (newValue) {
                            //  console.log(newValue, "========information");
                            let component = this.getComponent('informationTxt');
                            component.visible = true;
                            newValue = newValue == null ? '' : ExtendMgr.inst.getText4Language("地主让") + newValue.toString() + ExtendMgr.inst.getText4Language('张');
                            component.text = newValue;
                        },
                        boomLimit: function (newValue) {
                            // let component = this.getComponent('tfBoomCount');
                            // newValue = newValue == null ? '-': 'x'+ newValue;
                            // component.text = newValue;
                        },
                        setfilpcards(newValue: boolean) {
                            let filpcards = this.getComponent('filpcards');
                            filpcards.visible = newValue;
                            if (!newValue)
                                return;
                            for (let i = 0; i < filpcards.numChildren; i++) {
                                let card = filpcards.getChildAt(i).asCom;
                                card.getChildAt(0).asLoader.url = G560.fl.Handwall.getCardPath('card_backface');
                            }
                        },
                        holeCards: function (newValue) {
                            let isShow = Boolean(newValue);
                            let conList = this.getComponent('conHoldcard').asList;
                            if (newValue) {
                                for (let i = 0; i < conList.numChildren; i++) {
                                    let card = conList.getChildAt(i).asCom;
                                    card.getChildAt(0).asLoader.url = fl.Handwall.getCardPath(newValue[i]);
                                }
                            }
                            else {
                                for (let i = 0; i < conList.numChildren; i++) {
                                    let card = conList.getChildAt(i).asCom;
                                    card.getChildAt(0).asLoader.url = G560.fl.Handwall.getCardPath('card_backface');
                                }
                            }
                        },
                        gameStage: function (newValue) {
                            // this.getComponent('conHoldCardBG').visible = Method.isPlayingGame();
                            // this.getComponent('conHoldcard').visible = Method.isPlayingGame();
                            // let doubleNumtxt = this.getComponent('doubleNumtxt').visible = Method.isPlayingGame();
                            // let informationTxt = this.getComponent('informationTxt').visible = Method.isPlayingGame();
                            // let difenTxt = this.getComponent('difenTxt').visible = Method.isPlayingGame();
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
                            //this.gameStage = Method.GAME_STAGE.GAME_READY;
                            this.getComponent('doubleNumtxt').text = "X1";
                            this.getComponent('informationTxt').text = ExtendMgr.inst.getText4Language('地主让0张');
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