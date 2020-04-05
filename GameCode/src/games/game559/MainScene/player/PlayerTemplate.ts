/**
 * Created by Administrator on 2018/4/12.
 */
module G559 {
    export namespace rf {
        export interface playerTemplateData {
            //data
            account?: string | number;
            coin?: string | number;
            headImgUrl?: string;
            id?: string | number;
            ip?: string;
            isGM?: boolean;
            nickname?: string;
            roomCards?: string | number;
            sex?: number;
            side?: string | number;
            handwall?: HandwallData;
            isDealer: any;

            score;

            alarm?: fairygui.Transition;
            tiles?: any;
            cardsEnabled?: any;
            handCount?: any;

            getComponent?: Function;
            update?: Function;
            show?: Function;
            hide?: Function;
            reset?: Function;
            getMaxCardId?: Function;
            haveSequenceThree?: Function;
            showAlarm?: Function;
            hideAlarm?: Function;
        }
        //玩家模板- component数据结构
        export interface playerTemplateComponentData {
            //头像部分
            view: fairygui.GComponent;
            tf_nick_name: fairygui.GComponent;
            img_head: fairygui.GComponent;
            tf_score: fairygui.GComponent;
            tag_ready: fairygui.GComponent;

        }
        export class PlayerTemplate {

            constructor() {

            }

            static create(component, handwall, roominfo) {


                return new Vuet({
                    data: {
                        //个人信息
                        account: 0,
                        coin: 0,
                        headImgUrl: '',
                        id: 0,
                        ip: '',
                        isGM: false,
                        nickname: '',
                        roomCards: 0,
                        sex: 0,
                        side: 0,
                        isDealer: false,

                        score: 0,
                        scoreBalance: null,
                        //游戏其他数据
                        tiles: null,
                        isReady: null,
                        online: null,
                        isEmpty: true,
                        isShowHandCount: null,
                        isDouble: null,
                        handCount: null,
                        isTrustee: null,
                        countdown: null,
                        cardsEnabled: null,


                        //游戏流程
                        gameStage: 0,
                    },


                    params: {
                        handwall: handwall,
                    },

                    component: ({
                        'view': component['view'],
                        'tf_nick_name': component['tf_nick_name'],
                        'img_head': component['img_head'],
                        'tf_score': component['tf_score'],
                        'tf_offline': component['tf_offline'],
                        'tagAlarm': component['tagAlarm'],
                        'tf_ready': component['tf_ready'],
                        'tag_trusteeship': component['tag_trusteeship'],
                        'tf_handCount': component['tf_handCount'],
                        'icon_handwall': component['icon_handwall'],
                        'tag_DoubleYes': component['tag_DoubleYes'],
                        'tag_DoubleNo': component['tag_DoubleNo'],
                        'con_countdown': component['con_countdown'],
                        'tf_countdown': component['tf_countdown'],

                        'score_balance': component['score_balance'],
                        'score_balance_txt1': component['score_balance_txt1'],
                        'score_balance_txt2': component['score_balance_txt2'],

                        'maskHandwallTrustee': component['maskHandwallTrustee'],
                        'btnHandwallTrustee': component['btnHandwallTrustee'],
                    }),

                    created: function () {
                        this.handwall.setTileData(this.tiles);

                        roominfo.watch('gameStage', this.updateGameStage);
                        handwall.watch('handCount', function (newValue) {
                            this.handCount = newValue;
                        }.bind(this))
                    },

                    watch: {
                        nickname: function (newValue) {
                            let self = <Vuet>this;
                            var component = self.getComponent('tf_nick_name');
                            if (Method.getLocalPos(this.side) != 0)
                                //component.text = Tools.inst.abbreviateNickname(Tools.inst.maskUserName(newValue), component.width, component.fontSize);
                                component.text = Tools.inst.maskUserName(newValue);
                            else
                                //  component.text = Tools.inst.abbreviateNickname(newValue, component.width, component.fontSize);
                                Tools.inst.SetNickNameAfter(component, newValue);
                        },

                        headImgUrl: function (newValue) {
                            let self = <Vuet>this;
                            var component = self.getComponent('img_head');
                            component.url = 'ui://la8oslyoosvmbg';
                            var headImgUrl = newValue;
                            try {
                                if (headImgUrl)
                                    Tools.inst.changeHeadIcon(headImgUrl, component);
                                else if (this.side == 0)
                                    Tools.inst.changeHeadIcon(UserMgr.inst.imgUrl, component);
                            } catch (error) {
                                console.log(error)
                            }
                        },

                        score: function (newValue) {
                            this.coin = newValue;
                        },
                        coin: function (newValue) {
                            let self = <playerTemplateData>this;
                            self.score = newValue;
                            var component = self.getComponent('tf_score');
                            component.text = Tools.inst.changeGoldToMoney(newValue, '');
                        },

                        scoreBalance: function (newValue) {
                            let self = <Vuet>this;
                            var component = self.getComponent('score_balance');
                            var score_balance_txt1 = self.getComponent('score_balance_txt1');
                            var score_balance_txt2 = self.getComponent('score_balance_txt2');
                            if (newValue != null) {
                                var num = parseFloat(newValue);
                                var str = Tools.inst.changeGoldToMoney(newValue);
                                score_balance_txt1.text = (num < 0 ? "" : '+' + str);
                                score_balance_txt2.text = (num < 0 ? '' + str : '');
                                component.setSelectedIndex(num < 0 ? 2 : 1);
                            } else {
                                score_balance_txt1.text = '';
                                score_balance_txt2.text = '';
                                component.setSelectedIndex(0);
                            }
                        },

                        isReady: function (newValue) {
                            let self = <Vuet>this;
                            var component = self.getComponent('tf_ready');
                            if (newValue && !Method.isPlayingGame()) {
                                // component.visible = true;
                            } else {
                                component.visible = false;
                            }
                        },

                        gameStage: function (newValue) {
                            let self = <playerTemplateData>this;
                            var isGaming = Method.checkGameStage(newValue);
                            //console.log('player watch gamestage:', newValue, ',isGaming:', isGaming);


                            if (isGaming)
                                self.getComponent('tf_ready').visible = false;

                        },

                        online: function (newValue) {
                            let self = <playerTemplateData>this;
                            let showOffLine = newValue === false;
                            self.getComponent('tf_offline').visible = showOffLine;
                        },

                        isShowHandCount: function (newValue) {
                            let self = <Vuet>this;
                            self.getComponent('tf_handCount').visible = Boolean(newValue);
                            self.getComponent('icon_handwall').visible = Boolean(newValue);
                        },

                        handCount: function (newValue) {
                            let self = <playerTemplateData>this;
                            self.handwall.handCount = newValue;
                            // self.getComponent('icon_handwall').visible = true;
                            self.getComponent('tf_handCount').text = newValue;
                        },

                        isDouble: function (newValue) {
                            // 1 ：不加倍 2：加倍
                            let self = <playerTemplateData>this;

                            let tagYes = self.getComponent('tag_DoubleYes');
                            let tagNo = self.getComponent('tag_DoubleNo');
                            if (newValue === null) {
                                tagYes.visible = false;
                                tagNo.visible = false;
                            } else {
                                tagYes.visible = newValue == 2;
                                tagNo.visible = newValue == 1;
                            }
                        },

                        isTrustee: function (newValue) {
                            let self = <playerTemplateData>this;

                            self.getComponent('tag_trusteeship').visible = Boolean(newValue);
                            var handwallMask = self.getComponent('maskHandwallTrustee');
                            var btn = self.getComponent('btnHandwallTrustee');
                            if (handwallMask) {
                                handwallMask.visible = Boolean(newValue);
                                btn.visible = Boolean(newValue);
                                btn.onClick(this, function () {
                                    console.log('1');
                                    Control.buttonMgr.cancelTrustee();
                                })
                            }
                        },

                        countdown: function (newValue) {
                            let self = <playerTemplateData>this;

                            let isShow = Boolean(newValue);
                            self.getComponent('con_countdown').visible = isShow;
                            if (newValue != null)
                                newValue = newValue.toString();
                            self.getComponent('tf_countdown').text = newValue || 0;
                        },

                        cardsEnabled: function (newValue) {
                            let self = <playerTemplateData>this;
                            self.handwall.cardsEnabled = newValue;
                        }


                    },

                    method: {
                        //------------------开放调用

                        update: function (data) {
                            this.show();
                            this.isEmpty = false;
                            for (let key in data) {
                                this[key] = data[key];
                            }
                        },

                        hide: function () {
                            let self = <playerTemplateData>this;

                            self.getComponent('view').visible = false;
                        },

                        show: function () {
                            let self = <playerTemplateData>this;

                            self.getComponent('view').visible = true;
                        },

                        pass: function () {
                            let self = <playerTemplateData>this;
                            self.handwall.pass();
                        },

                        clear: function () {
                            this.reset();

                            this.account = 0;
                            this.coin = 0;
                            this.headImgUrl = '';
                            this.id = 0;
                            this.ip = '';
                            this.isGM = false;
                            this.nickname = '';
                            this.roomCards = 0;
                            this.sex = 0;
                            this.side = 0;
                            this.isEmpty = true;


                            this.score = 0;

                            let self = <playerTemplateData>this;
                            self.getComponent('view').visible = false;

                        },

                        reset: function () {
                            let self = <playerTemplateData>this;

                            this.isReady = null;
                            this.online = null;
                            this.isShowHandCount = null;
                            // this.isDouble = null;
                            this.isTrustee = null;
                            this.countdown = null;
                            this.cardsEnabled = null;


                            self.handwall.reset();
                            self.getComponent('tf_ready').visible = false;
                            self.getComponent('icon_handwall').visible = false;
                            self.getComponent('tf_handCount').visible = false;
                        },

                        showAlarm: function () {
                            //console.log('showAlarm');
                            let self = <playerTemplateData>this;

                            Sound.alarm();

                            let controller = self.getComponent('tagAlarm').getController('c1');
                            controller.setSelectedPage('shank');
                            Laya.timer.once(2000, Game.page, function () {
                                self.hideAlarm();
                            })
                        },

                        hideAlarm: function () {
                            let self = <playerTemplateData>this;
                            let controller = self.getComponent('tagAlarm').getController('c1');
                            controller.setSelectedPage('hide');
                        },

                        setContent: function (data) {
                            let self = <playerTemplateData>this;

                            var handList = data["hand"];
                            var outList = data["out"];
                            var actionTipsId = data["tips"];

                            self.handwall.update(handList);
                            if (handList.length <= 2)
                                this.showAlarm();

                            if (outList != null) {
                                outList.sort(rfa.utils.sortCardFunc);
                                var outCp = <rfa.BaseCard>rfa.utils.getCardPattern(outList, true, data["wildcard"]);
                                outList = outCp.getShowCardIdList();

                                self.handwall.out(outList);
                            }

                            if (actionTipsId != null)
                                this.showActionTips(actionTipsId);
                        },

                        showActionTips: function (tipsId) {
                            let self = <playerTemplateData>this;

                            self.handwall.out();
                            if (tipsId == Control.playerMgr.TIPS_ID_NO_DISCARD) {
                                self.handwall.pass();
                            }
                        },

                        clearActionTips: function () {
                            let self = <playerTemplateData>this;

                            self.hideAlarm();
                        },

                        discard: function (data, cb) {
                            let self = <playerTemplateData>this;

                            //console.log("-discard-", data);
                            this.clearActionTips();
                            self.handwall.remove(data['discardList']);

                            let outList = data.cp1.getShowCardIdList();
                            self.handwall.out(outList);

                            if (data.isShowEffect)
                                this.showCardEffect(data.pos2, data.cp1, data.cp2, cb);
                            else
                                cb();

                            // if(data.isShowEffect)
                            //     this.showCardEffect(data.pos2, data.cp1, data.cp2, cb);
                            // else
                            //     cb();

                        },

                        showCardEffect: function (posOpponent, cp, cpOpponent, cb) {
                            let localPos = Method.getLocalPos(this.side);
                            Sound.playCardEffect(localPos, posOpponent, cp, cpOpponent);
                            switch (cp.getType()) {
                                case rfa.CARD_TYPE.BOMB:
                                    // Control.effects.playBomb(this.ptOut, this.pos, cb);
                                    Control.effects.playBomb(localPos, this, cb);

                                    break;

                                case rfa.CARD_TYPE.ROCKET:
                                    // Control.effects.playRocket(this.ptOut, this.pos, cb);
                                    Control.effects.playRocket(localPos, this, cb);

                                    break;

                                case rfa.CARD_TYPE.SEQUENCE:
                                    // Control.effects.playSequence(this.ptOut, this.pos, posOpponent, cp, cpOpponent, cb);
                                    Control.effects.playSequence(localPos, this, cb);

                                    break;

                                case rfa.CARD_TYPE.SEQUENCE_OF_PAIRS:
                                    // Control.effects.playSequence2(this.ptOut, this.pos, posOpponent, cp, cpOpponent, cb);
                                    Control.effects.playSequence2(localPos, this, cb);

                                    break;

                                case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS:
                                case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_ONE:
                                case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_TWO:
                                    // Control.effects.playSequence3(this.ptOut, this.pos, posOpponent, cp, cpOpponent, cb);
                                    Control.effects.playSequence3(localPos, this, cb);
                                    break;

                                default:
                                    try {
                                        Sound.playCardEffect(localPos, posOpponent, cp, cpOpponent);
                                    } catch (e) {
                                        console.log("最后打出去的是一手牌时，出现问题")
                                    }
                                    if (cb != null)
                                        setTimeout(cb, 100);
                                    break;
                            }
                        },

                        getMaxCardId: function () {
                            let self = <playerTemplateData>this;
                            return self.handwall.getMaxCardId();
                        },

                        haveSequenceThree: function () {
                            let self = <playerTemplateData>this;
                            let list = self.handwall.dataList;
                            let haveSequenceThree = false;
                            if (list) {
                                haveSequenceThree = list.indexOf(rfa.CONSTANTS.SEQUENCE_THREE) != -1;
                            }
                            return haveSequenceThree;
                        },

                        //--------------------------

                        updateGameStage: function (newValue) {
                            this.gameStage = newValue;
                        },

                    }
                })
            }
        }
    }
}