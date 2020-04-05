/**
 * Created by Administrator on 2018/4/25.
 */
module G559 {
    export namespace rf {
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
            tfBaseScore: fairygui.GTextField;
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
        export class BalanceView extends G560.fl.BalanceView {
            constructor() {
                super();
            }
            static create(component, params) {
                let base = super.create(component, params);
                let vuetparams: any = base._config;

                vuetparams.method.show = function (data, callback) {
                    var self = (<i_BalanceView>this);
                    self.setCloseCallback(callback);

                    let con = self.getComponent('con');
                    con.visible = true;
                    self.getComponent('btnContinue').visible = true;

                    let dataList = data['setUserDatas'];
                    let dataDict = dataList.reduce(function (acc, one) {
                        let localside = rf.getLocalPos(one['side']);
                        acc[localside] = one;
                        return acc;
                    }, {});
                    let posWinners = [];

                    //下方描述
                    let _p;
                    _p = (_p = data['gameCommonDatas']) && (_p = _p[0]) && (_p = _p['datas']);
                    let descList = [];
                    // console.log(_p, "=============_p");
                    if (_p != null) {
                        for (let i = 0; i < _p.length; i++) {
                            let desc = _p[i];
                            let tempList = desc.split(':');
                            if (tempList[0] == '底分') {
                                tempList[1] = Tools.inst.changeGoldToMoney(tempList[1]);
                            }
                            descList.push(ExtendMgr.inst.getText4Language(tempList[0]) + ":" + tempList[1])
                        }
                    }

                    let desc = descList.join(' ');
                    var tfDesc = self.getComponent('tfDesc')
                    tfDesc.visible = Boolean(desc);
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
                            if (localside != 0)
                                nickname = player.tfName.text = Tools.inst.maskUserName(itemData["nickname"]);
                            else
                                nickname = player.tfName.text = Tools.inst.abbreviateNickname(itemData["nickname"], component.width + 10, component.fontSize);
                            player.tgamectl.selectedIndex = 0;
                            let score = player.tfScore.text = (itemData["score"].toString().replace(/[0-9\.]+/, function (match) {
                                return jx.goldFormat(parseFloat(match));
                            }));
                            // console.log(itemData, "===============itemData");
                            let isWin = player.tagWin.visible = Boolean(itemData["isHu"]);
                            let desc = itemData["descs"];
                            let isBird = (desc[0] == "True");
                            let lastCard = player.tfLastCard.text = desc[1];
                            let boomCount = player.tfBoom.text = desc[2];
                            let isSpring = player.tagSpring.visible = (desc[4] == "True");
                            let isDouble = player.tagDouble.visible = Boolean(itemData["isDouble"]);
                            let imgHead = player.icon.url = itemData["headImgUrl"];
                            let tfBaseScore = player.tfBaseScore.text = desc[5];

                            //高亮自己
                            player.con.getController('role').setSelectedPage(Control.posServerSelf == itemData['side'] ? 'self' : 'normal');

                            if (isWin)
                                posWinners.push(localside);

                        }
                    });

                    this.setTitle(posWinners);
                }
                vuetparams.method.setTitle = function (posWinners) {
                    var self = (<i_BalanceView>this);
                    self.gameTypectl.setSelectedPage('559');

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
                }
                return new Vuet(vuetparams);
            }
        }
    }
}