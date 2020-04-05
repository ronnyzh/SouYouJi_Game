/**
 * Created by Administrator on 2018/4/12.
 */
module G561 {
    export namespace fl {
        export interface playerTemplateData extends Vuet {
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
            scoreBalance;
            isReady;
            online;
            isEmpty;
            isTrustee;
            countdown;
            isDealer;
            canSelectPK;
            gameover;
            giveup;



            alarm?: fairygui.Transition;
            tiles?: any;

            update?: Function;
            show?: Function;
            hide?: Function;
            reset?: Function;

            talkAction: playerTemplateData;
            clearTalk: void;

            putChip;
            chipNum;
            _chipPool;

            turnController: fairygui.Controller;
            ImageController: fairygui.Controller;
            TalkController: fairygui.Controller;


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

            static create(component, params, roominfo) {

                var handwall = params['handwall'];
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
                        isTrustee: null,
                        countdown: null,
                        gameover: null,
                        giveup: null,

                        chipNum: null,
                        canSelectPK: null,


                        //游戏流程
                        gameStage: 0,
                    },


                    params: {
                        handwall: params['handwall'],
                        turnController: params['turnController'],
                        ImageController: params['ImageController'],
                        TalkController: params['TalkController'],
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
                        'tfScore': component['tfScore'],
                        // 'score_balance': component['score_balance'],
                        // 'score_balance_txt1': component['score_balance_txt1'],
                        // 'score_balance_txt2': component['score_balance_txt2'],


                        //倒计时
                        'con_countdown': component['con_countdown'],
                        'tf_countdown': component['tf_countdown'],

                        //炸金花
                        'operationTalk': component['operationTalk'],
                        'tfChip': component['tfChip'],
                        'tagBipai': component['tagBipai'],
                        'group': component['group'],


                    }),

                    created: function () {
                        this.handwall.setTileData(this.tiles);

                        roominfo.watch('gameStage', function (newValue) {
                            this.gameStage = newValue;
                        });
                        handwall.watch('handCount', function (newValue) {
                            this.handCount = newValue;
                        }.bind(this));

                        this.boomCount = 0;
                        this.chipNum = 0;
                    },

                    watch: {
                        nickname: function (newValue) {
                            let self = <Vuet>this;
                            var component = self.getComponent('tf_nick_name');
                            //component.text = Tools.inst.abbreviateNickname(newValue, component.width + 20, component.fontSize);
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
                            let sss = parseFloat(newValue) || 0;
                            let score = Tools.inst.changeGoldToMoney(sss);
                            let scoreNum = newValue < 0 ? ("" + score) : ("+" + score)
                            self.getComponent('tfScore').visible = true;
                            var scoreC = self.getComponent('tfScore').getController("c1");
                            var selectedIdx = newValue < 0 ? 1 : 2;
                            scoreC.setSelectedIndex(selectedIdx);
                            let tfScore1 = self.getComponent('tfScore').getChild('title' + selectedIdx).asLabel;
                            // tfScore1.text = scoreNum;
                            var trant = self.getComponent('tfScore').getTransition('tfScoreActon' + selectedIdx);
                            trant.play();
                            this.numRun(tfScore1, sss);
                            // var handler = laya.utils.Handler.create(this, function () {
                            //     self.getComponent('tfScore').visible = false;
                            //     scoreC.setSelectedIndex(0);
                            // }.bind(this));
                            // trant.setHook("tfScoreActionEnd", handler);
                        },

                        coin: function (newValue) {
                            let self = <playerTemplateData>this;
                            self.score = newValue;
                            var component = self.getComponent('tf_score');
                            component.text = Tools.inst.changeGoldToMoney(newValue);

                        },

                        isReady: function (newValue) {
                            let self = <Vuet>this;
                            // var component = self.getComponent('tf_ready');
                            // if(newValue && !Method.isPlayingGame()){
                            //     component.visible = true;
                            // }else{
                            //     component.visible = false;
                            // }
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



                        isDealer: function (newValue) {
                            let self = <playerTemplateData>this;
                            let isNull = newValue == null;
                            let b = Boolean(newValue);
                            self.getComponent('tagDealer').visible = b && !isNull;
                            self.getComponent('tagBanker').visible = !b && !isNull;
                        },


                        isTrustee: function (newValue) {
                            let self = <playerTemplateData>this;

                            self.getComponent('tag_trusteeship').visible = Boolean(newValue);
                        },

                        countdown: function (newValue) {
                            let self = <playerTemplateData>this;

                            let isShow = Boolean(newValue);
                            self.getComponent('con_countdown').visible = isShow;
                            var str = parseInt(newValue).toString();
                            //移除小数点
                            str = str.replace(/(\.[\s\S]+)/g, function (match, target) { return match.replace(target, ''); })
                            self.getComponent('tf_countdown').text = str || 0;
                        },

                        chipNum: function (newValue) {
                            let self = <playerTemplateData>this;
                            let num = newValue || 0;
                            self.getComponent('tfChip').text = jx.goldFormat(num);
                        },

                        canSelectPK: function (newValue) {
                            let self = <playerTemplateData>this;
                            let component = self.getComponent('tagBipai');
                            if (component)
                                component.visible = newValue;
                        },
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

                        numRun: function (numBox, maxNum, endFunc?: (...params) => void, ...params) {
                            let num = 0;
                            let delta = Math.abs(maxNum / 39);
                            if (maxNum >= 0) {
                                let cb = () => {
                                    num += delta;
                                    if (num >= maxNum) {
                                        let str = '+' + Tools.inst.changeGoldToMoney(maxNum);
                                        let index = str.lastIndexOf('.');
                                        if (index == -1) {
                                            str = str + '.00';
                                        } else if ((str.length - index) == 2) {
                                            str = str + '0';
                                        }
                                        numBox.text = str
                                        if (endFunc != null) {
                                            endFunc(...params);
                                        }
                                    } else {
                                        let str = '+' + Tools.inst.changeGoldToMoney(num);
                                        let index = str.lastIndexOf('.');
                                        if (index == -1) {
                                            str = str + '.00';
                                        } else if ((str.length - index) == 2) {
                                            str = str + '0';
                                        }
                                        numBox.text = str;
                                        Laya.timer.once(50, this, cb);
                                    }
                                }
                                cb();
                            }
                            else {
                                let cb = () => {
                                    num -= delta;
                                    if (num <= maxNum) {
                                        let str = Tools.inst.changeGoldToMoney(maxNum);
                                        let index = str.lastIndexOf('.');
                                        if (index == -1) {
                                            str = str + '.00';
                                        } else if ((str.length - index) == 2) {
                                            str = str + '0';
                                        }
                                        numBox.text = str;
                                        if (endFunc != null) {
                                            endFunc(...params);
                                        }
                                    } else {
                                        let str = Tools.inst.changeGoldToMoney(num);
                                        let index = str.lastIndexOf('.');
                                        if (index == -1) {
                                            str = str + '.00';
                                        } else if ((str.length - index) == 2) {
                                            str = str + '0';
                                        }
                                        numBox.text = str;
                                        Laya.timer.once(50, this, cb);
                                    }
                                }
                                cb();
                            }
                        },

                        hide: function () {
                            let self = <playerTemplateData>this;

                            self.getComponent('view').visible = false;
                        },

                        show: function () {
                            let self = <playerTemplateData>this;

                            self.getComponent('view').visible = true;
                            self.turnController.setSelectedPage('off');
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
                            self.isTrustee = null;
                            self.countdown = null;
                            self.isDealer = null;
                            self.chipNum = null;
                            self.scoreBalance = 0;
                            self.gameover = false;
                            self.giveup = false;


                            self.handwall.reset();
                            self.getComponent('tf_ready').visible = false;
                            this.getComponent('tfScore').visible = false;
                            self.turnController.setSelectedPage('off');
                            self.ImageController.setSelectedPage('normal');
                            self.TalkController.setSelectedPage('hide');

                            //炸金花
                            this.clearTalk();
                        },

                        setContent: function (data) {
                            //console.log('setContent', data);
                            let self = <playerTemplateData>this;

                        },

                        //炸金花
                        talkAction: function (action) {
                            let self = <playerTemplateData>this;
                            let mapAction2Msg = {
                                [ACTION.GIVEUP]: '弃牌',
                                [ACTION.LOOKTILE]: '看牌',
                                [ACTION.FIGHTOTHER]: '比牌',
                                [ACTION.ALL_IN]: '全压',
                                [ACTION.ADDGOLD]: '加注',
                                [ACTION.FOLLOWGOLD]: '跟注',
                                [ACTION.FIGHTLOSE]: '失败',
                                [ACTION.SINGLE]: '孤注一掷',
                            };
                            var mapAction2Sound = {
                                [ACTION.GIVEUP]: Sound.giveup.bind(Sound, self.side),
                                [ACTION.LOOKTILE]: Sound.watchCard.bind(Sound, self.side),
                                [ACTION.FIGHTOTHER]: Sound.dopk.bind(Sound, self.side),
                                [ACTION.ALL_IN]: Sound.allin.bind(Sound, self.side),
                                [ACTION.ADDGOLD]: Sound.jiazhu.bind(Sound, self.side),
                                [ACTION.FOLLOWGOLD]: Sound.fallow.bind(Sound, self.side),
                            };

                            //弃牌/比牌失败 ，头像灰掉
                            if (action == ACTION.GIVEUP || action == ACTION.FIGHTLOSE) {
                                self.gameover = true;
                                if (action == ACTION.GIVEUP) {
                                    self.giveup = true
                                }
                                self.ImageController.setSelectedPage('disabled');

                            }

                            //操作对话框
                            (function () {
                                var sound = mapAction2Sound[action];
                                if (sound) sound();
                                //定义类型对应切换的控制器pageName
                                let mapAction2Page = {
                                    [ACTION.FOLLOWGOLD]: 'genzhu',
                                    [ACTION.ADDGOLD]: 'jiazhu',
                                    [ACTION.GIVEUP]: 'qipai',
                                    [ACTION.ALL_IN]: 'quanxia',
                                };
                                let pageName = mapAction2Page[action];
                                let pageMsg = mapAction2Msg[action];

                                this.visible = Boolean(pageName || pageMsg);

                                //优先显示控制器
                                if (pageName) {
                                    self.TalkController.setSelectedPage(pageName);
                                }

                                // 没有控制器则显示文字
                                // else if(pageMsg){
                                //     self.TalkController.setSelectedPage('normal');
                                //     this.getChild('tfTalk').text =  mapAction2Msg[action] || '';
                                // }

                                //如果是弃牌或者比牌失败则不隐藏
                                if (action == ACTION.GIVEUP || action == ACTION.FIGHTLOSE)
                                    return;

                                // 如果显示消息，那么2s后隐藏
                                if (pageMsg || pageName) {
                                    Method.setTimeout(function () {
                                        self.TalkController.setSelectedPage('hide');
                                    }, 2000);
                                } else {
                                    //没有显示消息，马上隐藏
                                    self.TalkController.setSelectedPage('hide');
                                }

                                // this.visible = true;
                                // this.getChild('tfTalk').text =  mapAction2Msg[action] || '';
                                //
                                // this.getTransition('show')
                                //     .play(new Laya.Handler(this, function(){
                                //         if(action == ACTION.GIVEUP)return;
                                //         this.visible = false;
                                //     }))
                            }).call(self.getComponent('operationTalk'));
                            return self;
                        },

                        showBipaiEffect: function (handler?: Laya.Handler) {
                            let self = <playerTemplateData>this;
                            self.getComponent('view').asCom
                                .getTransition('bipai')
                                .play(handler);
                        },

                        clearTalk: function () {
                            let self = <playerTemplateData>this;
                            (function () {
                                this.getChild('tfTalk').text = '';
                                this.visible = false;
                            }).call(self.getComponent('operationTalk'));
                        },

                        putChip: function (num) {
                            this.chipNum += num;
                            // Control.roominfo.zongzhu =( Control.roominfo.zongzhu || 0) + num;
                        },

                        setClickCallback: function (callback) {
                            let self = <playerTemplateData>this;
                            let component = self.getComponent('tagBipai');
                            this._clickMethod = callback;
                            component.onClick(this, callback, [this]);
                        },
                        clearClickCallback: function () {
                            let self = <playerTemplateData>this;
                            let component = self.getComponent('tagBipai');
                            var _clickMethod = this._clickMethod;
                            this._clickMethod = null;
                            if (_clickMethod)
                                component.offClick(this, _clickMethod);
                        },



                    }
                })
            }
        }
    }
}