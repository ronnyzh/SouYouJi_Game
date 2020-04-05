/**
 * Created by Administrator on 2018/4/19.
 */
module G560 {
    export namespace fl {
        interface i_ButtonManager extends Vuet {
            delegate: any;
            checkShowReady: any;

        }
        export class ButtonManager {
            static init(component, roominfo, delegate) {
                return new Vuet({
                    data: {
                        isTrustee: null, //托管中
                        isGoldOperatin: null, //是否正在执行金币场操作

                        gameStage: null,

                    },
                    params: {
                        playerSelf: null,
                        delegate: delegate
                    },
                    component: {
                        'btn_msg': component['btn_msg'],
                        'btn_exit': component['btn_exit'],
                        'btn_chat': component['btn_chat'],
                        'btn_setting': component['btn_setting'],
                        'btn_change': component['btn_change'],
                        'btnReady': component['btnReady'],
                        'ctl_autoCont': component['ctl_autoCont'],

                        //跑得快按钮
                        // 'btn_last_round': component['btn_last_round'],
                        'btn_trusteeship': component['btn_trusteeship'],
                        // 'btn_trusteeship_close': component['btn_trusteeship_close'],
                    },
                    created: function () {
                        //绑定游戏流程
                        roominfo.watch('gameStage', function (newValue) {
                            this.gameStage = newValue;
                        }.bind(this));

                        //按钮绑定事件
                        [
                            ['btn_trusteeship', this.doTrustee],
                            // ['btn_trusteeship_close',this.cancelTrustee],
                            ['btn_exit', this.onExitRoom],
                            ['btn_setting', this.onSetting],
                            // ['btn_change',this.onChangeRoom],
                            ['btnReady', this.onDoReady],

                        ].forEach(function (one) {
                            let name = one[0];
                            let callback = one[1];
                            this.getComponent(name).onClick(this, callback);
                        }.bind(this));

                        //跑得快
                        // this.getComponent('btn_last_round').enabled = false;
                        this.getComponent('btn_trusteeship').enabled = false;
                        // this.getComponent('btn_trusteeship_close').enabled = false;
                        this.isTrustee = false;
                    },

                    watch: {
                        gameStage: function (newValue) {
                            let self = (<i_ButtonManager>this);
                            let isGaming = Method.isPlayingGame();
                            //console.log('buttomManager watch gamestage:', newValue,',isGaming:', isGaming);

                            // self.getComponent('btn_last_round').enabled = isGaming;
                            self.getComponent('btn_trusteeship').enabled = isGaming;
                            // self.getComponent('btn_trusteeship_close').enabled = isGaming;

                            if (newValue == Method.GAME_STAGE.GAME_READY) {
                                Laya.timer.once(8000, this, function () {
                                    self.checkShowReady();
                                });
                            } else {
                                self.checkShowReady();
                            }
                        },

                        isTrustee: function (newValue) {
                            let self = (<i_ButtonManager>this);
                            newValue = Boolean(newValue);
                            self.getComponent('btn_trusteeship').visible = !newValue;
                            // self.getComponent('btn_trusteeship_close').visible = newValue;
                        },

                        isGoldOperatin: function (newValue) {
                            let self = (<i_ButtonManager>this);
                            let isEnabled = Boolean(!newValue);
                            self.getComponent('btn_exit').enabled = isEnabled;
                            // self.getComponent('btn_change').enabled = isEnabled;
                        }
                    },

                    once: {
                        bindPlayer: function (playerSelf) {
                            let self = (<i_ButtonManager>this);

                            this.playerSelf = playerSelf;
                            //托管绑定到玩家的数据
                            playerSelf.watch('isTrustee', function (newValue) {
                                this.isTrustee = newValue;
                            }.bind(this));

                            playerSelf.watch('isReady', self.checkShowReady.bind(self));
                            self.checkShowReady();

                        }
                    },

                    method: {
                        //----------开放调用
                        reset: function () {
                            this.isGoldOperatin = false;
                        },
                        doTrustee: function () {
                            // console.log("========发送托管");
                            let self = (<i_ButtonManager>this);
                            // self.getComponent('btn_trusteeship').visible = false;
                            Control.playerSelf.isTrustee = true;
                            NetHandlerMgr.netHandler.sendTrustee(true);
                        },

                        cancelTrustee: function () {
                            let self = (<i_ButtonManager>this);
                            Control.playerSelf.isTrustee = false;
                            NetHandlerMgr.netHandler.sendTrustee(false);
                        },

                        onExitRoom: function () {
                            let self = (<i_ButtonManager>this);
                            if (this.isGoldOperatin) return;

                            Method.exitRoom();
                        },

                        onSetting: function () {
                            UIMgr.inst.popup(UI_Setting);
                        },

                        onChangeRoom: function () {

                            if (this.isGoldOperatin) return;
                            this.isGoldOperatin = true;
                            Method.changeRoom();
                        },
                        checkShowReady: function () {
                            // let self = (<i_ButtonManager>this);
                            // if(!Control.playerSelf)return;
                            // var isGaming = Method.isPlayingGame();
                            // var isReady = Control.playerSelf.isReady;
                            // var isStarted = Control.roominfo.isGameStart();
                            // var isShow = !isGaming && !isReady && isStarted;
                            // self.getComponent('btnReady').visible = isShow;
                        },

                        onDoReady: function () {
                            let self = (<i_ButtonManager>this);
                            self.getComponent('btnReady').visible = false;
                            // NetHandlerMgr.netHandler.sendReadyGame();
                            // Control.playerSelf.isReady = true;
                            this.onChangeRoom();
                        },
                    }

                })
            }
        }
    }
}