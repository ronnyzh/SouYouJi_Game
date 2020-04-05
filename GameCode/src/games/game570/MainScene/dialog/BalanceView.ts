module G570 {
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
        export class BalanceView extends G560.fl.BalanceView {
            constructor() {
                super();
            }
            static create(component, params) {
                let base = super.create(component, params);
                let vuetparams: any = base._config;
                vuetparams.create = function () {
                    this.playerList = [
                        this.player0,
                        this.player1,]
                }
                vuetparams.method.show = function (data, callback) {
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
                        descList.push(ExtendMgr.inst.getText4Language(tempList[0]) + ":" + tempList[1])
                    }
                    let desc = descList.join(' ');

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
                }
                return new Vuet(vuetparams);
            }
        }
    }
}