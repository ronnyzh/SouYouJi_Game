/**
 * Created by Administrator on 2018/4/25.
 */
module G561 {
    export namespace fl {
        interface BalanceViewItemPlayer {
            con: fairygui.GComponent;
            tfName: fairygui.GComponent;
            icon: fairygui.GLoader;
            tfLastCard: fairygui.GComponent;
            tfBoom: fairygui.GComponent;
            tfScore: fairygui.GComponent;
            tagWin: fairygui.GImage;
            tagSpring: fairygui.GImage;
            tagDouble: fairygui.GImage;
        }
        interface i_BalanceView extends Vuet {

            playerDataList: any;
            playerList: Array<BalanceViewItemPlayer>;
            player0: BalanceViewItemPlayer;
            player1: BalanceViewItemPlayer;
            player2: BalanceViewItemPlayer;
            conPlayerList: fairygui.GList;


            controller: fairygui.Controller;
            _closecallback: Function;

            show: Function;
            hide: Function;
            setCloseCallback: Function;
            setTitle: Function;

        }
        export class BalanceView {
            static create(component, params) {

                return new Vuet({
                    data: {
                        playerDataList: [],
                    },
                    params: {
                        playerList: [],

                        conPlayerList: params['conPlayerList'],

                        controller: params['controller'],
                    },
                    component: {
                        'con': component['con'],
                        'btnExit': component['btnExit'],
                        'btnContinue': component['btnContinue'],
                        'btnChange': component['btnChange'],
                        'autoContTimer': component['autoContTimer'],
                    },
                    created: function () {
                        this.playerList = [
                            this.player0,
                            this.player1,
                            this.player2,
                        ];

                        this.getComponent('btnContinue').onClick(this, this.onChangeRoom);
                        this.getComponent('btnExit').onClick(this, this.onExitRoom);
                        this.getComponent('btnChange').onClick(this, this.onChangeRoom);

                        this.hide();
                    },
                    method: {
                        //-----------开放调用
                        show: function (data, callback) {
                            var self = (<i_BalanceView>this);
                            self.setCloseCallback(callback);
                            let con = self.getComponent('con');
                            con.visible = true;
                            self.getComponent('btnContinue').visible = true;

                            let dataList = data['setUserDatas'];
                            let dataDict = dataList.reduce(function (acc, one) {
                                let localside = fl.getLocalPos(one['side']);
                                acc[localside] = one;
                                return acc;
                            }, {});
                            let posWinners = [];

                            let conList = self.conPlayerList;
                            conList.removeChildrenToPool();

                            dataList.forEach(oneData => {
                                var bar = conList.addItemFromPool().asCom;
                                bar.getChild('tagWin').visible = oneData['isWin'];
                                bar.getChild('icon').asLoader.url = oneData['headImgUrl'];
                                bar.getChild('tfName').text = oneData['nickname'];
                                bar.getChild('tfScore').text = Tools.inst.changeGoldToMoney(oneData['score']);
                                if (oneData['side'] == Control.posServerSelf) {
                                    self.setTitle(oneData['isWin'])
                                }
                            });
                            this.setTitle(posWinners);
                        },

                        hide: function () {
                            var self = (<i_BalanceView>this);
                            self.getComponent('con').visible = false;
                            self.getComponent('btnContinue').visible = false;
                            if (self._closecallback) self._closecallback();
                        },

                        showAutoContTimer: function () {
                            var self = (<i_BalanceView>this);
                            let autoContTime = 3000;
                            Laya.timer.once(autoContTime, this, Method.changeRoom);
                            self.getComponent('autoContTimer').visible = true;

                            let time = Math.floor(autoContTime / 1000);
                            let cb = (time: number) => {
                                self.getComponent('autoContTimer').text = time.toString();
                                if (time > 0) {
                                    Laya.timer.once(1000, this, cb, [time - 1]);
                                } else {
                                    self.getComponent('autoContTimer').visible = false;
                                }
                            }
                            cb(time);
                        },

                        hideAutoContTimer: function () {
                            var self = (<i_BalanceView>this);
                            Laya.timer.clear(this, Method.changeRoom);
                            self.getComponent('autoContTimer').visible = false;
                        },

                        onExitRoom: function () {
                            Method.exitRoom();
                        },

                        onChangeRoom: function () {
                            this.hide();
                            Method.changeRoom();
                        },

                        //------------

                        setCloseCallback: function (cb) {
                            this._closecallback = jx.once(this, cb);
                        },

                        setTitle: function (isWin) {
                            var self = (<i_BalanceView>this);

                            if (isWin == null) {
                                self.controller.setSelectedPage('empty')
                            }
                            else if (isWin) {
                                self.controller.setSelectedPage('win')
                            }
                            else {
                                self.controller.setSelectedPage('lose')

                            }
                        },
                    }
                })
            }
        }
    }
}