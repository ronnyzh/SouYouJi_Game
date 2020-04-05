/**
 * Created by Administrator on 2018/4/12.
 */
module G560 {
    export namespace fl {
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

            score;
            isReady;
            online;
            isEmpty;
            isShowHandCount;
            isDouble;
            isLandLord;
            isTrustee;
            countdown;
            isDealer;

            alarm?: fairygui.Transition;
            tiles?: any;
            cardsEnabled?: any;
            handCount?: any;
            boomCount?: any;
            boomMultiple?: any;

            getComponent?: Function;
            update?: Function;
            show?: Function;
            hide?: Function;
            reset?: Function;
            getMaxCardId?: Function;
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
                        isDealer: null,

                        score: 0,
                        scoreBalance: 0,
                        //游戏其他数据
                        tiles: null,
                        isReady: null,
                        online: null,
                        isEmpty: true,
                        isShowHandCount: null,
                        isDouble: null,
                        isLandLord: null,
                        handCount: null,
                        isTrustee: null,
                        countdown: null,
                        cardsEnabled: null,
                        boomCount: null,

                        boomMultiple: 0,

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
                        'tf_ready': component['tf_ready'],
                        'tag_trusteeship': component['tag_trusteeship'],
                        'tf_handCount': component['tf_handCount'],
                        'icon_handwall': component['icon_handwall'],
                        'score_balance': component['score_balance'],
                        'score_balance_txt1': component['score_balance_txt1'],
                        'score_balance_txt2': component['score_balance_txt2'],

                        //警告灯
                        'tagAlarm': component['tagAlarm'],

                        //加倍
                        'tag_DoubleYes': component['tag_DoubleYes'],
                        'tag_DoubleNo': component['tag_DoubleNo'],

                        'tfMultiple': component['tfMultiple'],
                        'groupMultiple': component['groupMultiple'],

                        'maskHandwallTrustee': component['maskHandwallTrustee'],
                        'btnHandwallTrustee': component['btnHandwallTrustee'],

                        //倒计时
                        'con_countdown': component['con_countdown'],
                        'tf_countdown': component['tf_countdown'],

                        //地主
                        'tagDealer': component['tagDealer'],
                        'tagBanker': component['tagBanker'],
                        'groupBoom': component['groupBoom'],
                        'tfBoom': component['tfBoom'],

                        //抢地主
                        'tag_landlord_1': component['tag_landlord_1'],
                        'tag_landlord_2': component['tag_landlord_2'],
                        'tag_landlord_3': component['tag_landlord_3'],
                        'tag_landlord_no': component['tag_landlord_no'],
                        'tag_landlord_yes': component['tag_landlord_yes'],
                    }),

                    created: function () {
                        let self = <Vuet>this;
                        this.handwall.setTileData(this.tiles);

                        roominfo.watch('gameStage', this.updateGameStage);
                        handwall.watch('handCount', function (newValue) {
                            this.handCount = newValue;
                        }.bind(this));
                        self.getComponent('groupMultiple').visible = false;
                        this.boomCount = 0;

                    },

                    watch: {

                        boomMultiple: function (newValue) {
                            let self = <Vuet>this;

                            if (newValue) {
                                self.getComponent('groupMultiple').visible = true;
                                self.getComponent('tfMultiple').text = '× ' + newValue;
                            } else {
                                self.getComponent('groupMultiple').visible = false;
                            }
                        },

                        nickname: function (newValue) {
                            let self = <Vuet>this;
                            var component = self.getComponent('tf_nick_name');
                            if (Method.getLocalPos(this.side) != 0)
                                //component.text = Tools.inst.abbreviateNickname(Tools.inst.maskUserName(newValue), component.width, component.fontSize);
                                component.text = Tools.inst.maskUserName(newValue);
                            else
                                // component.text = Tools.inst.abbreviateNickname(newValue, component.width, component.fontSize);
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

                        coin: function (newValue) {
                            let self = <playerTemplateData>this;
                            self.score = newValue;
                            var component = self.getComponent('tf_score');
                            component.text = Tools.inst.changeGoldToMoney(newValue,'');
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

                            //self.getComponent('groupMultiple').visible = Boolean(isGaming);
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

                        isLandLord: function (newValue) {
                            let self = <playerTemplateData>this;
                            let tagList = {
                                0: 'tag_landlord_no',
                                1: 'tag_landlord_1',
                                2: 'tag_landlord_2',
                                3: 'tag_landlord_3',
                                'yes': 'tag_landlord_yes',
                            };

                            jx.each(tagList, function (name, key) {
                                let isShow = newValue == key;
                                self.getComponent(name).visible = isShow;
                            });
                        },

                        isDealer: function (newValue) {
                            let self = <playerTemplateData>this;
                            let isNull = newValue == null;
                            let b = Boolean(newValue);
                            self.getComponent('tagDealer').visible = b && !isNull;
                            // self.getComponent('tagBanker').visible = !b && !isNull;
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
                        },

                        boomCount: function (newValue) {
                            let self = <playerTemplateData>this;

                            self.getComponent('tfBoom').text = newValue ? 'x' + newValue : 0;
                            self.getComponent('groupBoom').visible = Boolean(newValue);
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
                            let self = <playerTemplateData>this;
                            this.reset();

                            self.account = 0;
                            self.coin = 0;
                            self.headImgUrl = '';
                            self.id = 0;
                            self.ip = '';
                            self.isGM = false;
                            self.nickname = '';
                            self.roomCards = 0;
                            self.sex = 0;
                            self.side = 0;
                            self.isEmpty = true;


                            self.score = 0;

                            self.getComponent('view').visible = false;

                        },

                        reset: function () {
                            let self = <playerTemplateData>this;

                            self.isReady = null;
                            self.online = null;
                            self.isShowHandCount = null;
                            self.isDouble = null;
                            self.isLandLord = null;
                            self.isTrustee = null;
                            self.countdown = null;
                            self.cardsEnabled = null;
                            self.boomCount = 0;
                            self.isDealer = null;
                            self.boomMultiple = 0;


                            self.handwall.reset();
                            self.getComponent('tf_ready').visible = false;
                            self.getComponent('icon_handwall').visible = false;
                            self.getComponent('tf_handCount').visible = false;
                        },

                        showAlarm: function () {
                            let self = <playerTemplateData>this;

                            Sound.alarm();

                            let controller = self.getComponent('tagAlarm').getController('c1');
                            controller.setSelectedPage('shank');
                            Laya.timer.once(2000, this, function () {
                                self.hideAlarm();
                            })
                        },

                        hideAlarm: function () {
                            let self = <playerTemplateData>this;
                            let controller = self.getComponent('tagAlarm').getController('c1');
                            controller.setSelectedPage('hide');
                        },

                        setContent: function (data) {
                            console.log('setContent', data);
                            let self = <playerTemplateData>this;

                            var handList = data["hand"];
                            var outList = data["out"];
                            var actionTipsId = data["tips"];

                            self.handwall.update(handList);
                            if (handList.length <= 2)
                                this.showAlarm();

                            if (outList != null) {
                                outList.sort(fla.utils.sortCardFunc);
                                var outCp = <fla.BaseCard>fla.utils.getCardPattern(outList, true, data["wildcard"]);
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

                            cb()
                        },

                        showCardEffect: function (posOpponent, cp, cpOpponent, cb) {
                            let localPos = Method.getLocalPos(this.side);
                            Sound.playCardEffect(localPos, posOpponent, cp, cpOpponent);
                            switch (cp.getType()) {
                                case fla.CARD_TYPE.BOMB:
                                    Control.effects.playBomb(localPos, this, cb);
                                    break;

                                case fla.CARD_TYPE.ROCKET:
                                    Control.effects.playRocket(localPos, this, cb);
                                    break;

                                case fla.CARD_TYPE.SEQUENCE:
                                    Control.effects.playSequence(localPos, this, cb);
                                    break;

                                case fla.CARD_TYPE.SEQUENCE_OF_PAIRS:
                                    Control.effects.playSequence2(localPos, this, cb);
                                    break;

                                case fla.CARD_TYPE.SEQUENCE_OF_TRIPLETS:
                                case fla.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_ONE:
                                case fla.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_TWO:
                                    Control.effects.playSequence3(localPos, this, cb);
                                    break;

                                default:
                                    Sound.playCardEffect(localPos, posOpponent, cp, cpOpponent);
                                    if (cb != null)
                                        setTimeout(cb, 100);
                                    break;
                            }
                        },

                        getMaxCardId: function () {
                            let self = <playerTemplateData>this;
                            return self.handwall.getMaxCardId();
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