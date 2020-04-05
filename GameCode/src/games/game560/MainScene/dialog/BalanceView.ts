/**
 * Created by Administrator on 2018/4/25.
 */
module G560 {
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
            tagDealer: fairygui.GImage;
            tgamectl: fairygui.Controller;
        }
        interface i_BalanceView extends Vuet {

            playerDataList: any;
            playerList: Array<BalanceViewItemPlayer>;
            player0: BalanceViewItemPlayer;
            player1: BalanceViewItemPlayer;
            player2: BalanceViewItemPlayer;


            controller: fairygui.Controller;
            gameTypectl: fairygui.Controller;
            onShow: fairygui.Transition;
            _closecallback: Function;

            show: Function;
            hide: Function;
            setCloseCallback: Function;

        }
        export class BalanceView {
            static create(component, params) {

                return new Vuet({
                    data: {
                        playerDataList: [],
                    },
                    params: {
                        playerList: [],

                        player0: params['player0'],
                        player1: params['player1'],
                        player2: params['player2'],

                        controller: params['controller'],
                        onShow: params['onShow'],
                        gameTypectl: params['gameTypectl'],
                    },
                    component: {
                        'con': component['con'],
                        'onShow': component['onShow'],
                        'btnExit': component['btnExit'],
                        'btnContinue': component['btnContinue'],
                        'btnChange': component['btnChange'],
                        'tfDesc': component['tfDesc'],
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

                            //下方描述
                            let _p;
                            _p = (_p = data['gameCommonDatas']) && (_p = _p[0]) && (_p = _p['datas']);
                            let descList = [];
                            for (let i = 0; i < _p.length; i++) {
                                let desc = _p[i];
                                let tempList = desc.split(':');
                                if (tempList[0] == '底分') {
                                    tempList[1] = Tools.inst.changeGoldToMoney(tempList[1]);
                                }
                                descList.push(ExtendMgr.inst.getText4Language(tempList[0]) + ":" + tempList[1])
                            }
                            let desc = descList.join(' ');
                            // var _p;
                            // var desc = (_p = data['gameCommonDatas']) && (_p = _p[0]) && (_p = _p['datas']) && (_p = _p.reduce(function (acc, cur) {
                            //     let rgx = /([\d\.]+)/;
                            //     console.log(rgx, cur, "============rgx");
                            //     if (rgx.test(cur)) {
                            //         cur = ExtendMgr.inst.getText4Language("底分：") + cur.replace(rgx, function (str, match) {
                            //             var result = match;
                            //             try {
                            //                 result = str.replace(match, Tools.inst.changeGoldToMoney(parseFloat(match)));
                            //             } catch (e) { };
                            //             return result;
                            //         });
                            //     }
                            //     return acc.concat(cur);
                            // }, []).join(' '));

                            // console.log(_p, "------------_p");
                            var tfDesc = self.getComponent('tfDesc')
                            tfDesc.visible = Boolean(desc);
                            //  console.log(desc, "=========desc");
                            if (desc) tfDesc.text = desc;

                            self.playerList.forEach(function (player, idx) {
                                let localside = idx;
                                let itemData = dataDict[localside];

                                if (!itemData) {
                                    //没有数据
                                    player.con.visible = false;
                                    return;
                                } else {
                                    let nickname;
                                    //console.log(itemData["nickname"],"=========名字");
                                    if (localside != 0)
                                        nickname = player.tfName.text = Tools.inst.maskUserName(itemData["nickname"]);
                                    else
                                        nickname = player.tfName.text = itemData["nickname"];
                                    player.tgamectl.selectedIndex = 1;
                                    let score = player.tfScore.text = (itemData["score"].toString().replace(/[0-9\.]+/, function (match) {
                                        return Tools.inst.changeGoldToMoney(parseFloat(match))
                                    }));
                                    let isWin = player.tagWin.visible = Boolean(itemData["isHu"]);
                                    let desc = itemData["descs"];
                                    let lastCard = player.tfLastCard.text = desc[0];
                                    let boomCount = player.tfBoom.text = desc[1];
                                    player.tagSpring.visible = false;
                                    player.tagDouble.visible = false;
                                    // let isSpring = player.tagSpring.visible = (desc[4] == "True");
                                    // let isDouble = player.tagDouble.visible = Boolean(itemData["isDouble"]);
                                    let isDouble = player.tagDouble.visible = false;
                                    let imgHead = player.icon.url = itemData["headImgUrl"];
                                    //地主
                                    player.tagDealer.visible = Boolean(itemData['isDealer']);
                                    //高亮自己
                                    player.con.getController('role').setSelectedPage(Control.posServerSelf == itemData['side'] ? 'self' : 'normal');

                                    if (isWin)
                                        posWinners.push(localside);

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
                            Laya.timer.once(autoContTime, this, this.onChangeRoom);
                            self.getComponent('autoContTimer').visible = true;

                            let time = Math.floor(autoContTime / 1000);
                            let cb = (time: number) => {
                                self.getComponent('autoContTimer').text = time.toString();
                                if (time > 0) {
                                    Laya.timer.once(1000, this, cb, [time - 1]);
                                } else {
                                    self.getComponent('autoContTimer').visible = false;
                                    this.hide();
                                }
                            }
                            cb(time);
                        },

                        hideAutoContTimer: function () {
                            var self = (<i_BalanceView>this);
                            Laya.timer.clear(this, Method.changeRoom);
                            self.getComponent('autoContTimer').visible = false;
                        },
                        destory: function () {
                            var self = (<i_BalanceView>this);
                            self.getComponent('btnExit').mode = -1;
                            self.getComponent('btnContinue').mode = -1;
                            //self.getComponent('btnChange').mode = -1;
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

                        setTitle: function (posWinners) {
                            var self = (<i_BalanceView>this);
                            self.gameTypectl.setSelectedPage('560');
                            if (posWinners.length == 0) {
                                self.controller.setSelectedPage('empty')
                            }
                            else if (posWinners.indexOf(0) != -1) {
                                self.controller.setSelectedPage('win')
                            }
                            else {
                                self.controller.setSelectedPage('lose')
                            }
                            self.onShow.play();
                        },
                    }
                })
            }
        }
    }
}