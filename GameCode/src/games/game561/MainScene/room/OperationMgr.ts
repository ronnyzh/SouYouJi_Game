/**
 * Created by Administrator on 2018/4/13.
 */
module G561 {
    export namespace fl {
        export class OperationManagerFace extends Vuet {
            operation: fairygui.GList;
            controller: fairygui.Controller;
            pageDict: any;
            btnList: any;
            btnFallow: any;
            textFallow: any;
            btnFight: any;
            defaultFallow: any;
            textFight: any;
            defaultFight: any;
            DEFAULT_DISABLED: any;
            WATCHED_BTN: any;
            DEFAULT_BTN: any;
            disabledList: any;
            AUTO_BAND_LIST: any;
            GIVEUP_BANDlIST: any;

            SORT_DATA: any;


            showAction: OperationManagerFace;
            setClickCallback: OperationManagerFace;
            changeChipBackground: Function;

            show: OperationManagerFace;
            after: OperationManagerFace;
            onItem: Function;
            hide: Function;
            isAuto: any;
            updateBtns: any;
        }
        export class OperationManager {
            static init(component, Controller, buttonMgr) {
                let operation = component['operation'];
                return new Vuet({
                    data: {
                        gameStage: null,
                        isShowPaixing: false,

                        defaultFallow: '跟注',
                        textFallow: '跟注',
                        defaultFight: '比牌',
                        textFight: '比牌',
                        isAuto: null,
                        isShowJiazhu: null,
                        isSelectPK: null,
                        WATCHED: false,
                        WATCHED_BTN: 'btnWatch',

                        //排序先后
                        SORT_DATA: {
                            LIST: ["btnPass", 'btnAdd', 'btnContrast', 'btnFallow', 'btnAuto', 'btnSingle'],
                            SPACING: 30,
                            CENTER_RIGHT_OFFSET: 450,
                            RIGHT_OFFSET: 250,
                            MAX_WIDTH_PRE: 0.8
                        },
                        //开始不会屏蔽的列表
                        DEFAULT_BTN: ['btnBrandType', 'btnAuto', 'btnWatch'],
                        //开始自动屏蔽列表
                        DEFAULT_DISABLED: [
                            "btnPass",
                            "btnAll",
                            "btnContrast",
                            "btnFallow",
                            "btnAdd",
                            "btnSingle"
                        ],
                        //弃牌的禁用列表-用来屏蔽所有按钮
                        GIVEUP_BANDlIST: ["btnPass", 'btnWatch', 'btnAll', 'btnContrast', 'btnAdd', 'btnFallow', 'btnAuto', 'btnSingle'],
                        //自动跟的禁用列表
                        AUTO_BAND_LIST: ["btnPass", 'btnWatch', 'btnAll', 'btnContrast', 'btnAdd', 'btnFallow', 'btnSingle'],
                        disabledList: [],
                        lastActionList: [],
                    },
                    component: {
                        'operation': component['operation'],
                        'jiazhu': component['jiazhu'],
                        'pkMask': component['pkMask'],

                    },
                    params: {
                        controller: Controller,
                        pageDict: operation._children.reduce(function (acc, item) {
                            let groupName = item.group && item.group.name;
                            let list = acc[groupName] || (acc[groupName] = []);
                            list.push(item);
                            return acc;
                        }, {}),
                        btnFallow: operation._children.reduce(function (acc, item) {
                            return item.name == 'btnFallow' ? item : acc;
                        }, null),
                        btnFight: operation._children.reduce(function (acc, item) {
                            return item.name == 'btnContrast' ? item : acc;
                        }, null),
                        btnList: operation._children.reduce(function (acc, item) {
                            let groupName = item.group && item.group.name;
                            if ((groupName == 'left' || groupName == 'right' || groupName == 'container') && item.visible) {
                                acc.push(item);

                            }
                            return acc;
                        }.bind(this), []),
                    },

                    created: function () {
                        //初始化主选项管理器

                        var self = <OperationManagerFace>this;
                        // //以page的方式绑定按钮
                        // var _obj;
                        // Object.keys((_obj = this.pageDict)).forEach(function(key){
                        //     _obj[key].forEach(function (btn, idx) {
                        //         (<fairygui.GButton>btn).onClick(self, self.onItem,[idx, btn]);
                        //     })
                        // })

                        //以btnList的方式绑定
                        this.btnList.forEach(function (btn, idx) {
                            (<fairygui.GButton>btn).onClick(self, self.onItem, [idx, btn]);
                            btn.setEnabled = function (b) {
                                this.enabled = b;
                                this.getController('status').setSelectedPage(b ? 'normal' : 'disabled');
                                this.visible = b;
                            }
                        }, this);

                        //比牌蒙版绑定事件
                        this.getComponent('pkMask').onClick(this, this.clearSelectListPK);


                        buttonMgr.watch('isTrustee', function (newValue) {
                            this.isAuto = newValue;
                        }.bind(this))
                    },
                    watch: {
                        gameStage: function (newValue) {
                            var isGameEnd = newValue == Method.GAME_STAGE.GAME_READY;

                            //console.log('operation watch gamestage:', newValue, ',isGameEnd:', isGameEnd);

                            let self = (<OperationManagerFace>this);

                            if (isGameEnd) {
                                self.hide();
                            }
                        },

                        isShowPaixing: function (newValue) {
                            let self = (<OperationManagerFace>this);
                            if (newValue === null) return;
                            let transition = self.getComponent('operation').getTransition('showPaixing');
                            if (newValue)
                                transition.play();
                            else
                                transition.playReverse();
                        },

                        isAuto: function (newValue) {
                            let self = (<OperationManagerFace>this);
                            (function () {
                                // this.enabled = !newValue;

                                if (ExtendMgr.inst.lan == ExtendMgr.CN) {
                                    this.title = newValue ? '取消' : '自动跟注';
                                } else {
                                    this.getController('auto').selectedPage = newValue ? '取消' : '自动跟注';
                                }
                            }).call(self.getComponent('operation').getChild('btnAuto'));
                            self.updateBtns();
                        },

                        isShowJiazhu: function (newValue) {
                            let self = (<OperationManagerFace>this);
                            var con = self.getComponent('jiazhu');
                            if (newValue === null) {
                                con.visible = false;
                                return
                            }

                            let transition = self.getComponent('operation').getTransition('showJiazhu');
                            if (Boolean(newValue)) {
                                transition.play();
                            } else {
                                transition.playReverse();
                            }
                        },

                        textFallow: function (newValue) {
                            let self = (<OperationManagerFace>this);
                            // self.btnFallow.text = newValue;
                            self.btnFallow.getChild('title').text = newValue || self.defaultFallow;
                        },
                        textFight: function (newValue) {
                            let self = (<OperationManagerFace>this);
                            // self.btnFallow.text = newValue;
                            self.btnFight.getChild('title').text = newValue || self.defaultFight;
                        },

                        WATCHED: function (newValue) {
                            let self = (<OperationManagerFace>this);
                            let method = function (method, list, item) {
                                let idx = list.indexOf(item);

                                switch (method) {
                                    case 'remove':
                                        if (idx != -1)
                                            list.splice(idx, 1);
                                        break;
                                    case 'add':
                                        if (idx == -1)
                                            list.push(item);
                                        break;
                                }
                            };
                            if (newValue) {
                                method('add', self.DEFAULT_DISABLED, self.WATCHED_BTN);
                                method('add', self.disabledList, self.WATCHED_BTN);
                                self.updateBtns();

                            } else {
                                method('remove', self.DEFAULT_DISABLED, self.WATCHED_BTN);
                                method('remove', self.disabledList, self.WATCHED_BTN);

                            }

                        },

                    },
                    method: {
                        //-----------开放调用
                        show: function (name?, clickCallback?, nameList?): OperationManagerFace {
                            let self = (<OperationManagerFace>this);
                            this._name = name;

                            //---下面是 打牌操作按钮
                            // 显示界面
                            self.getComponent('operation').visible = true;

                            //没有name则只显示
                            if (!name) return;

                            self.controller.setSelectedPage(name);

                            if (clickCallback) {
                                this._clickCallback = clickCallback;
                            }
                            this.setClickCallback(clickCallback);
                            this.showAction(nameList);
                            return self;
                        },

                        setClickCallback: function (clickCallback) {

                            if (clickCallback) {
                                this._clickCallback = clickCallback;
                            }
                            return self;
                        },

                        showAction: function (nameList) {
                            let self = (<OperationManagerFace>this);
                            let items = self.DEFAULT_DISABLED;
                            let result = self.DEFAULT_DISABLED.concat();
                            if (items) {
                                items.forEach(function (item, idx) {
                                    let isShow = (nameList && nameList.indexOf(item) !== -1);
                                    if (isShow) {
                                        let idx = result.indexOf(item);
                                        if (idx != -1)
                                            result.splice(idx, 1);
                                    }
                                })
                            }
                            self.disabledList = result;
                            this.updateBtns();
                            return self;
                        },

                        disabledBtn: function () {
                            let self = (<OperationManagerFace>this);
                            self.disabledList = self.DEFAULT_DISABLED;
                            this.updateBtns();
                            self.textFallow = self.defaultFallow;
                            self.textFight = self.defaultFight;
                            // self.getComponent('operation')
                            //     .getController('c1')
                            //     .setSelectedPage('disabled');
                        },

                        disabledAll: function () {
                            let self = (<OperationManagerFace>this);
                            self.disabledList = self.GIVEUP_BANDlIST;
                            self.updateBtns();
                        },

                        updateBtns: function () {
                            let self = (<OperationManagerFace>this);

                            //console.log('updateBtns', self.disabledList);
                            var showList = [];
                            self.btnList.forEach(function (btn) {
                                let isShow = self.disabledList.indexOf(btn.name) == -1
                                    && (self.isAuto ? self.AUTO_BAND_LIST.indexOf(btn.name) == -1 : true);
                                btn.setEnabled(isShow);
                                isShow && showList.push(btn);
                            })

                            if (showList.length != 0) {
                                //排序
                                var parent = showList[0].parent;
                                var spacing = self.SORT_DATA.SPACING;
                                var sortList = self.SORT_DATA.LIST;
                                var rightOffset = self.SORT_DATA.RIGHT_OFFSET;

                                //检查长度
                                var maxWidth = Laya.stage.width * self.SORT_DATA.MAX_WIDTH_PRE;
                                var curWidth = showList.reduce(function (acc, item: fairygui.GComponent) {
                                    item.scaleX = 1;
                                    item.scaleY = 1;
                                    return acc + item.width + spacing;
                                }, 0);
                                var scale = 1;
                                if (curWidth > maxWidth) {
                                    scale = maxWidth / curWidth;
                                }
                                //console.log('curWidth', curWidth, 'maxWidth', maxWidth, 'scale', scale)

                                var lastW = 0;
                                showList.sort(function (a, b) {
                                    let sA = sortList.indexOf(a.name);
                                    let sB = sortList.indexOf(b.name);
                                    return (sA != null && sB != null) ? sB - sA : 1;
                                });
                                showList.forEach(function (item, idx) {
                                    item.anchorX = 0.5;
                                    item.anchorY = 0.5;
                                    item.scaleX = scale;
                                    item.scaleY = scale;
                                    item.x = Laya.stage.width - rightOffset - item.width * scale / 2 - lastW;
                                    lastW += (item.width * scale + spacing);
                                }, this);
                            }
                        },

                        changeChipBackground: function (chip, number?, enabled?, isTable?) {
                            let sCon = chip.getController('status');
                            let cCon = chip.getController('c1');


                            let list = [
                                1 * Control.roominfo.baseScore,
                                2 * Control.roominfo.baseScore,
                                3 * Control.roominfo.baseScore,
                                4 * Control.roominfo.baseScore,
                                5 * Control.roominfo.baseScore,
                                6 * Control.roominfo.baseScore,
                            ];

                            //设置背景
                            let idx = 0;
                            if (number != null) {
                                //如果是丢到筹码区，那么三位数的话会变成金砖
                                var isBrick = isTable && parseInt(number).toString().length >= 3;
                                if (isBrick) {
                                    //直接等于金砖
                                    idx = 5;
                                } else {
                                    //根据背景列表筛选
                                    let arr = list;
                                    let i = arr.length;
                                    while (i--) {
                                        if (parseInt(number) >= list[i]) {
                                            idx = i;
                                            break;
                                        }
                                    }
                                }

                                cCon.setSelectedIndex(idx);
                            }
                            //设置禁用
                            sCon.setSelectedPage(enabled == null || enabled ? 'normal' : 'disabled');

                        },

                        showJiazhu: function (list, callback) {
                            let self = (<OperationManagerFace>this);
                            this.isShowJiazhu = true;
                            var conList = self.getComponent('operation')
                                .getChildInGroup('chipList', self.getComponent('jiazhu')).asList;
                            conList.removeChildrenToPool();

                            list.forEach((num, idx) => {
                                let item = conList.addItemFromPool().asCom;
                                let cost = num * Control.roominfo.baseScore;
                                self.changeChipBackground(item, cost);
                                item.getChild('title').text = jx.goldFormat(cost);
                                item.onClick(this, function () {
                                    this.hideJiazhu();
                                    callback(idx, num);
                                })
                            })
                        },

                        hideJiazhu: function () {
                            this.isShowJiazhu = false;
                        },

                        toggleSelectListPK: function (fightList, callback) {
                            if (this.isSelectPK) {
                                this.clearSelectListPK();
                            } else {
                                if (fightList) {
                                    this.setSelectListPK(fightList, callback)
                                }
                            }
                        },

                        setSelectListPK: function (newValue, callback) {
                            this.isSelectPK = true;
                            let self = (<OperationManagerFace>this);
                            let pkMask = self.getComponent('pkMask');
                            if (!newValue) {
                                pkMask.visible = false;
                            } else {
                                pkMask.visible = true;
                                Control.playerMgr.showSelectPK(newValue, callback)
                            }
                        },

                        clearSelectListPK: function () {
                            this.isSelectPK = false;
                            let self = (<OperationManagerFace>this);
                            self.getComponent('pkMask').visible = false;
                            Control.playerMgr.clearSelectPK();
                        },
                        /**
                         * @params: method(btns);
                         * */
                        after: function (caller, method, args?): OperationManagerFace {
                            args = typeof args == 'undefined' ? [] : args;
                            let self = (<OperationManagerFace>this);
                            // let btns = self.pageDict[this._name].concat();
                            let btns = self.btnList;
                            method.apply(caller, [].concat(args, [btns]));
                            return self;
                        },

                        hide: function () {
                            let self = (<OperationManagerFace>this);
                            self.getComponent('operation').visible = false;
                            return this;
                        },

                        resetExtend: function () {
                            this.clearSelectListPK();
                            this.isShowJiazhu = null;
                        },

                        reset: function () {
                            this.hide();
                            this.resetExtend();
                            this.disabledList = [];
                            this.WATCHED = null;
                            this.isShowPaixing = null;
                            this._clickCallback = null;
                            return this;
                        },

                        togglePaixing: function () {
                            this.isShowPaixing = !this.isShowPaixing;
                            return this;
                        },

                        toggleProxy: function () {
                            let self = (<OperationManagerFace>this);
                            let current = self.isAuto = !self.isAuto;
                            NetHandlerMgr.netHandler.sendTrustee(current);
                        },

                        giveup: function () {
                            NetHandlerMgr.netHandler.sendAction(ACTION.GIVEUP);
                        },

                        onGiviup: function () {
                            this.disabledAll();
                        },

                        sendWatch: function () {
                            Control.operationMgr.textFallow = '跟' + Tools.inst.changeGoldToMoney(2 * Control.roominfo.baseScore).replace(',', '');
                            Control.operationMgr.textFight = '比' + Tools.inst.changeGoldToMoney(2 * Control.roominfo.baseScore).replace(',', '');

                            NetHandlerMgr.netHandler.sendWatch();
                            // Control.playerMgr.talkAction(Control.posServerSelf, ACTION.LOOKTILE);

                        },

                        //-----------

                        onItem: function (idx, btn) {
                            //console.log('itemClick', idx);
                            if (btn.name == 'btnBrandType') this.togglePaixing();
                            if (btn.name == 'btnAuto') this.toggleProxy();
                            // if(btn.name == 'btnPass')this.giveup();
                            if (btn.name == 'btnWatch') this.sendWatch();

                            var clickCallback = this._clickCallback;
                            if (clickCallback) {
                                clickCallback(idx, btn);
                            }
                            // this._clickCallback = null;
                        },
                    }
                });
            }

        }
    }
}