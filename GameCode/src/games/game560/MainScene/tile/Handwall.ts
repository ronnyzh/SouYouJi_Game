/**
 * Created by Administrator on 2018/4/12.
 */
module G560 {
    export namespace fl {
        let Event = Laya.Event;
        export let TILE_STAGE = {
            NORMAL: 'normal',
            ACTIVE: 'active',
            DISABLED: 'disabled',
            MOUSE_OVER: 'over',
            MOUSE_OUT: 'out'
        };
        export interface HandwallData extends vuetData {
            imgList?: any;
            dataList?: any;
            tileList?: any;
            outTileList?: any;
            selectList?: any;
            handCount?: any;
            cardsEnabled?: any;
            disabledList?: any;
            isShowHand?: any;
            isEnabled?: any;
            overList?: any;
            isDealer?: any;
            localSide?: any;

            MoveUpTip?: any;//滑动牌事件

            showEffect?: Boolean;
            updateCallback?: Function;

            reset?: Function;
            getSelectedData?: Function;
            resetOut?: Function;
            resetHand?: Function;
            getUrlByData?: Function;
            setTileByData?: Function;
            resetSelected?: Function;
            resetDisabled?: Function;
            _enabledTouch?: Function;
            pass?: Function;
            update?: Function;
            out?: Function;
            remove?: Function;
            getMaxCardId?: Function;
            setDisabled?: Function;
            revertTile?: Function;
            setTileStage?: Function;
            resetTileStage?: Function;
            refreshTile?: Function;
            initDrop?: Function;
            getTileStage?: Function;
            setTileActive?: Function;
            setTileDealer?: Function;
            initTileByData?: Function;
            clearSelectedList?: Function;

            isfapai?: Boolean;
        }
        interface HandwallComponentData {
            hand_pokers: fairygui.GComponent;
        }


        export class Handwall {
            static SHOW_EFFECT_DURING = 130; //动画持续时间,ms
            static _rfCardMap;
            static rfCardMap() {
                if (!Handwall._rfCardMap) {
                    let suitDict = {
                        'a': 'd',
                        'b': 'c',
                        'c': 'b',
                        'd': 'a',
                        'w': 'w', //癞子
                        'j': 'e', //joker
                    };
                    let numDict = {
                        'A': '1',
                        '2': '2',
                        '3': '3',
                        '4': '4',
                        '5': '5',
                        '6': '6',
                        '7': '7',
                        '8': '8',
                        '9': '9',
                        'T': '10',
                        'J': '11',
                        'Q': '12',
                        'K': '13',
                        'L': '2',    //小joker
                        'B': '1',    //大joker
                    };
                    let numList = Object.keys(numDict);
                    let mapNum = numDict;
                    let suitList = Object.keys(suitDict);
                    let mapSuit = suitDict;
                    Handwall._rfCardMap = numList.reduce((acc, num) => {
                        suitList.forEach(suit => {
                            if (suit == 'w') return;
                            var realSuit = mapSuit[suit] || suit;
                            var realNum = mapNum[num] || num;
                            acc[num + suit] = 'card_' + realSuit + realNum;
                        });
                        return acc;
                    }, {})
                }
                Handwall._rfCardMap['card_backface'] = 'card_backface';
                return Handwall._rfCardMap;
            }

            static getCardPath(card) {
                let cardMap = Handwall.rfCardMap();
                let name = cardMap[card];
                let path = UIMgr.getTileUrl('pokersFTLpoker', name);

                return path;
            }

            static create(component, localSide, isShowHand) {

                return new Vuet({
                    data: {
                        dataList: [],
                        outList: [],
                        overList: [],
                        handCount: null,
                        cardsEnabled: null,
                        selectList: [],
                        disabledList: [],

                        isDealer: false,
                        showEffect: false,
                        isfapai: false,
                    },
                    params: {
                        playerTileList: null,
                        tileList: null,
                        outTileList: null,
                        imgList: null,
                        localSide: localSide,
                        isShowHand: isShowHand,
                        isEnabled: isShowHand,

                        _touching: false,

                    },
                    watch: {
                        dataList: function (newList) {
                            //console.log('watch dataList', newList);
                            var self = (<HandwallData>this);
                            self.resetHand();
                            self.getComponent('hand_pokers').visible = self.isShowHand;
                            self.setTileByData(self.tileList, newList, self.getComponent('hand_pokers'), 0, self.localSide);
                            self.tileList.forEach(tile => {
                                //是否显示地主标识
                                self.setTileDealer(tile);
                            });

                            // //初始化拖动
                            // self.initDrop();
                        },

                        // showEffect: function(newValue){
                        //     console.log('showEffect',newValue);
                        //     console.trace();
                        // },

                        outList: function (newList) {
                            //console.log('watch outList', newList);
                            var self = (<HandwallData>this);
                            self.resetOut();
                            self.getComponent('outwall').visible = true;
                            if (!newList) return;
                            self.setTileByData(self.outTileList, newList, self.getComponent('outwall'), 1, self.localSide);
                        },

                        selectList: function (newList) {
                            var self = (<HandwallData>this);
                            // console.log('watch select list', newList);
                            self.refreshTile();
                        },

                        cardsEnabled: function (newValue) {
                            var self = (<HandwallData>this);
                            self.isEnabled = newValue;
                            // self.getComponent('hand_pokers').enabled = newValue;
                        },

                        disabledList: function (newList) {
                            var self = (<HandwallData>this);
                            //console.log('disabledList:', newList);
                            self.refreshTile();
                        },

                        isDealer: function (newValue) {
                            var self = (<HandwallData>this);
                            if (newValue && self.tileList)
                                self.tileList.forEach(tile => {
                                    self.setTileDealer(tile)
                                })
                        }

                    },
                    created: function () {

                        //获取牌实例列表
                        this.tileList = this.getComponent('hand_pokers')._children.concat();
                        //获取出牌实例列表
                        this.outTileList = this.getComponent('outwall')._children.concat();
                        //获取牌的图片列表
                        this.imgList = this.tileList.map(function (item) { return item.getChildAt(0); })
                        //是否显示手牌
                        this.getComponent('hand_pokers').visible = this.isShowHand;
                        this.resetHand();
                    },
                    component: {
                        'hand_pokers': component['hand_pokers'],
                        'outwall': component['outwall'],
                        'tag_Pass': component['tag_Pass']
                    },
                    once: {
                        setTileData(tileList) {
                            this.playerTileList = tileList;
                        },

                        enabledTouch: function () {
                            var self = (<HandwallData>this);
                            self._enabledTouch();

                        },
                    },
                    method: {
                        //---------开放调用
                        show: function () {
                            let self = (<HandwallData>this);
                            self.getComponent('hand_pokers').visible = self.isShowHand;
                        },

                        getDataList: function () {
                            return this.dataList.concat();
                        },

                        getMaxCardId: function () {
                            if (this.dataList == null || this.dataList.length == 0) {
                                console.log("getMaxCardId error");
                                return 0;
                            }

                            var maxCardId = fla.utils.getCardNumber(this.dataList[0]);

                            for (var i = 1; i < this.dataList.length; ++i) {
                                if (fla.utils.getCardNumber(this.dataList[i]) > maxCardId)
                                    maxCardId = fla.utils.getCardNumber(this.dataList[i]);
                            }
                            return maxCardId;
                        },

                        //------出牌区操作

                        //根据数据显示出牌区的牌
                        out: function (tileList) {
                            let self = (<HandwallData>this);

                            self.showEffect = true;
                            self.updateCallback = function () {
                                self.updateCallback = null;
                                self.showEffect = false;
                            };
                            this.outList = tileList;
                        },

                        //出牌区显示不要
                        pass: function () {
                            let self = (<HandwallData>this);
                            self.resetOut();
                            self.getComponent('tag_Pass').visible = true;
                            self.resetSelected();
                        },
                        //------

                        //------选取
                        resetSelected: function () {
                            let self = (<HandwallData>this);
                            self.selectList = [];
                        },
                        clearSelectedList: function () {
                            let self = (<HandwallData>this);
                            (function (list) {
                                list.shift();
                                if (list.length) {
                                    arguments.callee(list);
                                }
                            })(self.selectList)
                        },

                        getSelectedData: function () {
                            let self = (<HandwallData>this);
                            let list = self.selectList.map(function (tile) {
                                return tile.data;
                            });
                            // self.resetSelected();
                            return list;
                        },


                        //根据数据更新选取的牌
                        setCardsActive: function (idList) {
                            let self = (<HandwallData>this);
                            this.resetSelected();
                            var tileList = self.tileList;
                            let list = idList.map(function (tileId) {
                                for (let i = 0, len = tileList.length; i < len; i++) {
                                    let tile = tileList[i];
                                    if (tile.data == tileId) {
                                        return tile;
                                    }
                                }
                                console.error('setCardsActive error ', tileId, 'not in ', self.dataList);
                            });
                            self.selectList = list;
                        },

                        //根据牌设置选取状态
                        setTileDealer: function (tile) {
                            let self = (<HandwallData>this);
                            var isDealer = self.isDealer;
                            if (tile && tile.getController('role')) {
                                var role = tile.getController('role');
                                role.setSelectedPage(isDealer ? 'dealer' : 'normal');
                            }
                        },
                        setTileActive: function (tile, b) {
                            let self = (<HandwallData>this);
                            //更改牌
                            b ? self.setTileStage(tile, TILE_STAGE.ACTIVE) : self.setTileStage(tile, TILE_STAGE.NORMAL);

                            //数据联动
                            let idx = self.selectList.indexOf(tile);
                            let isNotSelected = idx == -1;
                            isNotSelected ? self.selectList.push(tile) : self.selectList.splice(idx, 1);
                        },
                        //------

                        //------禁用
                        resetDisabled: function () {
                            let self = (<HandwallData>this);
                            self.disabledList = [];
                        },

                        setDisabled: function (idList) {
                            if (this.dataList == null || this.dataList.length == 0)
                                return;
                            let self = (<HandwallData>this);
                            //清空已选择牌
                            self.clearSelectedList();
                            //一定要是数组
                            if (!(idList instanceof Array)) idList = [idList];
                            self.disabledList = idList;
                        },
                        //------

                        //------重置
                        reset: function () {
                            let self = (<HandwallData>this);

                            self.resetHand();
                            self.resetOut();


                            self.showEffect = false;
                            self.updateCallback = null;
                        },

                        resetHand: function () {
                            let self = (<HandwallData>this);

                            self.getComponent('hand_pokers').visible = false;
                            self.isEnabled = true;

                            self.overList = [];
                            self.resetSelected();
                            self.resetDisabled();
                            self.each(self.tileList, function (tile) {
                                tile.visible = false;
                                tile.data = null;
                            })
                            self.isDealer = false;
                        },

                        resetOut: function () {
                            let self = (<HandwallData>this);
                            self.getComponent('outwall').visible = true;
                            self.each(self.outTileList, function (item) {
                                item.visible = false;
                            });
                            self.getComponent('tag_Pass').visible = false;
                        },

                        //------
                        //------牌墙批量操作
                        remove: function (newList) {
                            let self = (<HandwallData>this);
                            this.resetSelected();
                            // 减少牌
                            this.handCount -= newList.length;
                            //console.log('handCount reduce', this.handCount, newList.length);
                            // 移除牌
                            if (!self.isShowHand) return;
                            let dataList = this.dataList;
                            //console.log('handwall remove ', newList, 'in', dataList);
                            let conList = self.getComponent('hand_pokers');

                            newList.forEach(function (rank) {
                                let idx, list;
                                (idx = (list = dataList).indexOf(rank)) != -1 ? list.splice(idx, 1) : '';
                                conList.removeChildToPoolAt(idx);
                                self.tileList = conList._children;
                            })

                            // (function(list){
                            //     let selfFunc = arguments.callee;
                            //     if(!list || list.length == 0) return;
                            //     let tile = list.shift();
                            //     let idx = dataList.indexOf(tile);
                            //     if(idx !== -1){
                            //         dataList.splice(idx, 1);
                            //     }else{
                            //         console.log('移除牌id不存在',tile, idx, dataList , this.dataList);
                            //     }
                            //     selfFunc(list);
                            // }).call(this, newList.concat());
                            //
                            // this.dataList = dataList;

                        },
                        //获得排序后牌的位置
                        getAddCardPos(addList) {
                            var self = (<HandwallData>this);

                            let newList: Array<string> = this.dataList.concat(addList).sort(this.sortCardListFunc);
                            let posList: Array<{ x: number, y: number }> = [];
                            let hand_pokers: fairygui.GList = self.getComponent('hand_pokers');
                            let card = hand_pokers.getChildAt(0).asCom;
                            let startX = card.getChildAt(0).localToGlobal(0, 0).x;
                            let posy = card.getChildAt(0).localToGlobal(0, 0).y + card.actualHeight / 2 * hand_pokers.scaleY;
                            // console.log(hand_pokers.columnGap, card.actualWidth, hand_pokers.scaleX, "======hand_pokers.columnGap")
                            let columnGap = (card.actualWidth + hand_pokers.columnGap) * hand_pokers.scaleX;
                            columnGap = Math.ceil(columnGap);
                            if (self.localSide == 0) {
                                for (let i = 0; i < addList.length; i++) {
                                    let index = newList.indexOf(addList[i]);
                                    if (index != -1 && hand_pokers.numChildren > 0) {
                                        let posx = startX + columnGap * index;
                                        posList.push({ x: posx, y: posy });
                                    }
                                }
                            }
                            else {
                                let index = hand_pokers.numChildren - 1;
                                for (let i = 0; i < addList.length; i++) {
                                    index += 1;
                                    let posx = startX + columnGap * index;
                                    posList.push({ x: posx, y: posy });
                                }
                            }
                            return posList;
                        },
                        //得到手牌列表是缩放
                        gethandpokerscale() {
                            var self = (<HandwallData>this);
                            let hand_pokers: fairygui.GList = self.getComponent('hand_pokers');
                            return hand_pokers.scaleX;
                        },
                        //保留现有的牌，新增
                        addCard: function (addList) {
                            this.dataList = this.dataList
                                .concat(addList)
                                .sort(this.sortCardListFunc);
                        },

                        //移除现有的牌，更新
                        update: function (tileList, isShowEffect?, callback?, isfapai = false) {
                            // if(!tileList)return;
                            var self = (<HandwallData>this);
                            self.isfapai = isfapai;
                            self.showEffect = isShowEffect;
                            self.updateCallback = function () {
                                self.updateCallback = null;
                                self.showEffect = false;
                                if (callback) callback();

                            };
                            tileList = tileList.sort(this.sortCardListFunc);
                            this.handCount = tileList.length;

                            if (tileList.toString() == this.dataList.toString()) {
                                return;
                            }
                            this.dataList = tileList;
                        },

                        //批量设置牌面
                        setTileByData: function (tileList, dataList, conList, listtype, localSide) {
                            var self = (<HandwallData>this);

                            //逐张加载
                            // var len;
                            // if(self.showEffect) {
                            //     //一张张做动画
                            //     len = dataList.length;
                            //     //移除所有牌
                            //     conList.removeChildrenToPool();
                            //     var _l = tileList.length;
                            //     while(_l--){
                            //         tileList.shift();
                            //     }
                            //     //一张张添加
                            //     var lastTile:fairygui.GComponent = null;
                            //     var during = Handwall.SHOW_EFFECT_DURING  * 1000;
                            //     var i = 0;
                            //     (function(){
                            //         var selfFunc = arguments.callee;
                            //         var finishedOne = function(tile?){
                            //             lastTile = tile;
                            //             i++;
                            //             selfFunc()
                            //         };
                            //         if(i < len){
                            //             let currentData = dataList[i];
                            //             if(currentData){
                            //                 //有数据，说明要新增或者更改牌信息
                            //                 var tile = conList.addItemFromPool().asCom;
                            //                 if(tileList.indexOf(tile) == -1)
                            //                     tileList.push(tile);
                            //                 //初始化牌
                            //                 self.initTileByData(tile, currentData, function () {
                            //                     // lastTile.getTransition('move').play();
                            //                     // finishedOne();
                            //                 });
                            //                 //计时
                            //                 Method.setTimeout(function () {
                            //                     finishedOne(tile);
                            //                 }, during);
                            //             }else{
                            //                 finishedOne();
                            //             }
                            //         }else{
                            //             if(typeof self.updateCallback=="function")self.updateCallback();
                            //         }
                            //
                            //     })();
                            // }else{
                            //     //不做动画
                            //     let removeList = [];
                            //     len = Math.max(tileList.length, dataList.length );
                            //     for (let i = 0; i < len; i++){
                            //         let tile = tileList[i];
                            //         let currentData = dataList[i];
                            //         if(currentData){
                            //             //有数据，说明要新增或者更改牌信息
                            //             if(!tile ){
                            //                 tile = conList.addItemFromPool().asCom;
                            //             }
                            //             tileList[i] = tile;
                            //             // tile.visible=false;
                            //             //初始化牌
                            //             self.initTileByData(tile, currentData);
                            //         }else{
                            //             //没有数据，说明要移除牌
                            //             if(tile){
                            //                 conList.removeChildToPool(tile);
                            //                 removeList.push(tile);
                            //             }
                            //         }
                            //     }
                            //     //执行移除
                            //     (function(list){
                            //         var selfFunc = arguments.callee;
                            //         if(list.length){
                            //             let tile = list.shift();
                            //             let idx = tileList.indexOf(tile);
                            //             tileList.splice(idx, 1);
                            //             selfFunc(list);
                            //         }
                            //     })(removeList);
                            //     if (typeof self.updateCallback == "function")self.updateCallback();
                            // }
                            var isOneLine;
                            var isMoveTile;
                            var onLoaded;
                            var setLoaded;

                            //避免因为没有子集导致计算错
                            if (conList.getMaxItemWidth() == 0) {
                                var _t = conList.addItemFromPool().asCom;
                                _t.visible = false;
                            }
                            //是否单行
                            isOneLine = dataList.length < Math.floor(conList.width / (conList.getMaxItemWidth() + conList.columnGap));
                            //是否做走牌动画
                            isMoveTile = isOneLine && dataList.length > 1;
                            if (_t) {
                                conList.removeChildToPool(_t);
                            }

                            //最后一张牌加载时触发
                            var _isLoaded = !isMoveTile;
                            var _onLoaded = null;
                            onLoaded = function (callback) {
                                if (_isLoaded)
                                    callback();
                                else
                                    _onLoaded = jx.once(this, callback);
                            }.bind(this);
                            setLoaded = function () {
                                _isLoaded = true;
                                if (_onLoaded) _onLoaded();
                            };


                            let removeList = [];
                            var len = Math.max(tileList.length, dataList.length);
                            for (let i = 0; i < len; i++) {
                                let tile = tileList[i];
                                let currentData = dataList[i];
                                if (currentData) {
                                    //有数据，说明要新增或者更改牌信息
                                    var hasInstance = Boolean(tile);
                                    if (!tile) {
                                        tile = conList.addItemFromPool().asCom;
                                    }
                                    tileList[i] = tile;

                                    tile.visible = (!(hasInstance || self.showEffect));
                                    console.warn(dataList.length, tile.visible, 'self.showEffect', self.showEffect, '_isLoaded', _isLoaded);
                                    if (!self.showEffect && hasInstance) {
                                        Method.setTimeout(function () {
                                            tile.visible = true;
                                        }, 0);
                                    }

                                    //初始化牌
                                    if (isMoveTile && i == dataList.length - 1) {
                                        self.initTileByData(tile, currentData, function () {
                                            setLoaded();
                                        });
                                    } else {
                                        self.initTileByData(tile, currentData);
                                    }

                                } else {
                                    //没有数据，说明要移除牌
                                    if (tile) {
                                        conList.removeChildToPool(tile);
                                        removeList.push(tile);
                                    }
                                }
                            }
                            //执行移除
                            (function (list) {
                                var selfFunc = arguments.callee;
                                if (list.length) {
                                    let tile = list.shift();
                                    let idx = tileList.indexOf(tile);
                                    tileList.splice(idx, 1);
                                    selfFunc(list);
                                }
                            })(removeList);
                           // console.log(self.showEffect, "==============self.showEffect");
                            if (!self.showEffect) {
                                // Method.setTimeout(function(){
                                //     tileList.forEach((item, index, array)=>{
                                //         item.visible= true;
                                //     });
                                //     if (typeof self.updateCallback == "function")self.updateCallback();
                                // }.bind(this),30)
                                if (typeof self.updateCallback == "function") self.updateCallback();
                            } else {
                                var during = Handwall.SHOW_EFFECT_DURING;

                                var animate = function () {

                                    Method.setTimeout(function () {
                                        //做垃圾动画
                                        conList._children.forEach((item, index, array) => {
                                            if (index >= array.length - 1 && index != 0 && isOneLine) return;
                                            item.visible = false;
                                            Method.setTimeout(function () {
                                                item.visible = true
                                                if (localSide == 0 && listtype == 0 && self.isfapai) {
                                                    item.asCom.getTransition('fapai').play();
                                                    Sound.playDealCard();
                                                }
                                            }, during * index)
                                        });

                                        var array = tileList;
                                        if (isOneLine) {
                                            //最后一张
                                            var lastTile: fairygui.GComponent = null;
                                            var firstTile: fairygui.GComponent = null;
                                            if (array.length > 1) {
                                                lastTile = array[array.length - 1];
                                                firstTile = array[0];
                                                var spacing = conList.columnGap;
                                                if (localSide == 0 && listtype == 0 && self.isfapai)
                                                    lastTile.visible = false;
                                                else
                                                    lastTile.visible = true;
                                                var copy = lastTile.getChildAt(0);
                                                var x = copy.x;
                                                copy.x -= (lastTile.x - firstTile.x);
                                                Laya.Tween.to(copy, { x: x }, during * (array.length - 1), Laya.Ease.linearNone, Laya.Handler.create(this, function () {

                                                    if (localSide == 0 && listtype == 0 && self.isfapai) {
                                                        lastTile.getTransition('fapai').play(
                                                            new Laya.Handler(this, function () {
                                                                self.isfapai = false;
                                                                if (typeof self.updateCallback == "function") self.updateCallback();
                                                            })
                                                        );
                                                        lastTile.visible = true;
                                                        Sound.playDealCard();
                                                    }
                                                    else
                                                        if (typeof self.updateCallback == "function") self.updateCallback();
                                                }));

                                            } else {
                                                if (typeof self.updateCallback == "function") self.updateCallback();
                                            }
                                        } else {
                                            Method.setTimeout(function () {
                                                if (typeof self.updateCallback == "function") self.updateCallback();
                                            }, during * (array.length - 1));
                                        }


                                    }.bind(this), 30)
                                }.bind(this);

                                onLoaded(animate);
                                conList.visible = true;
                            }


                            // conList.asList.removeChildrenToPool();
                            // //清空数据
                            // (function(list){
                            //     var selfFunc = arguments.callee;
                            //     if(list.length){
                            //         list.splice(0, 1);
                            //         selfFunc(list);
                            //     }
                            // })(tileList);
                            //
                            //
                            // self.each(dataList, function(rank, idx){
                            //     let tile = conList.addItemFromPool().asCom;
                            //     tile.visible = true;
                            //     tileList[idx] = tile;
                            //     self.initTileByData(tile, rank);
                            //
                            // }.bind(this))
                        },

                        //更新每张牌的状态
                        refreshTile: function () {
                            let self = (<HandwallData>this);

                            self.tileList.forEach(function (tile) {
                                if (!tile.data) {
                                    return;
                                }

                                switch (true) {
                                    case (self.disabledList.indexOf(fla.utils.getCardNumber(tile.data)) !== -1):
                                        self.setTileStage(tile, TILE_STAGE.DISABLED);
                                        break;
                                    case (self.selectList.indexOf(tile) !== -1):
                                        self.setTileStage(tile, TILE_STAGE.ACTIVE);
                                        break;
                                    default:
                                        self.setTileStage(tile, TILE_STAGE.NORMAL);
                                }

                            })
                        },

                        //手牌排序方法
                        sortCardListFunc: function (card1, card2) {
                            return fla.utils.compareCard(card1, card2);
                        },
                        //------

                        //------对单张牌的操作
                        getTileStage: function (tile) {
                            return tile._type_current;
                        },
                        setTileStage: function (tile, type) {
                            let self = (<HandwallData>this);
                            tile = (<fairygui.GComponent>tile);
                            let controller = tile.getController('c1');
                            let Status = tile.getController('status');

                            var setTage = function (target) {
                                tile._type_last = tile._type_current || TILE_STAGE.NORMAL;
                                tile._type_current = target;
                            };
                            //NORMAL,ACTIVE,DISABLED都要设置状态值
                            if ([TILE_STAGE.NORMAL, TILE_STAGE.ACTIVE, TILE_STAGE.DISABLED].indexOf(type) != -1) {
                                setTage(type);
                            }
                            switch (type) {
                                case (TILE_STAGE.NORMAL):
                                case (TILE_STAGE.ACTIVE):
                                    controller.setSelectedPage(type);
                                    Status.setSelectedPage('enabled');
                                    break;
                                case (TILE_STAGE.DISABLED):
                                case (TILE_STAGE.MOUSE_OVER):
                                    Status.setSelectedPage('disabled');
                                    break;
                                case (TILE_STAGE.MOUSE_OUT):
                                    Status.setSelectedPage('enabled');
                                    break;
                            }
                        },
                        resetTileStage: function (tile) {
                            tile = (<fairygui.GComponent>tile);
                            let type = TILE_STAGE.NORMAL;
                            if (tile._type_last == type) return;
                            tile._type_last = type;
                            tile._type_current = type;
                            tile.getController('c1').setSelectedPage(type);
                            tile.getController('status').setSelectedPage('enabled');

                        },
                        revertTile: function (tile) {
                            tile = (<fairygui.GComponent>tile);
                            let type = tile._type_last || TILE_STAGE.NORMAL;
                            tile._type_last = type;
                            tile._type_current = type;

                            tile.getController('c1').setSelectedPage(type);
                        },

                        //获取牌实例
                        getTileById: function (tileId) {
                            var self = (<HandwallData>this);
                            let idx = self.dataList.indexOf(tileId);
                            if (idx != -1) {
                                return self.tileList[idx];
                            } else {
                                console.error('无法找到手牌', tileId, self.dataList)
                            }
                        },

                        //初始化牌
                        initTileByData: function (tile, rank, callback?) {
                            var self = (<HandwallData>this);
                            tile.data = rank;
                            var img = tile.getChildAt(0).asLoader;
                            // tile.visible = false;
                            // var cache = Control.Tilepool.tileCache['G560' + rank];
                            var url = rank ? self.getUrlByData(rank) : '';
                            //var cache = Laya.loader.getRes(url);
                            let setTile = function (instance) {
                                //img.onExternalLoadSuccess(instance);
                                img.url = instance;
                                self.resetTileStage(tile);
                                // tile.visible = typeof tileVisible == null ? true : tileVisible;
                                if (typeof callback == 'function') {
                                    callback();
                                }
                            };
                            setTile(url);
                            // if (cache) {
                            //     setTile(cache);
                            //     return;
                            // }
                            // Laya.loader.load(url, Handler.create(this, function (v, tex) {
                            //     setTile(tex);
                            //     // Control.Tilepool.tileCache['G560' + v] = tex;
                            // }, [rank]));
                        },

                        //根据花色获取牌图片地址
                        getUrlByData: function (card) {
                            return Handwall.getCardPath(card);
                        },

                        //------

                        //触摸事件
                        /**
                         * 鼠标响应事件处理
                         */
                        _enabledTouch: function () {
                            let self = (<HandwallData>this);
                            let handwall = self.getComponent('hand_pokers');
                            //拖动选牌
                            handwall.on(Event.MOUSE_DOWN, this, this.mouseHandler);
                            handwall.on(Event.MOUSE_UP, this, this.mouseHandler);
                            handwall.on(Event.MOUSE_OUT, this, this.mouseHandler);
                            handwall.on(Event.MOUSE_MOVE, this, this.mouseHandler);

                            //点击选牌
                            // handwall.on(Event.CLICK, this, this.mouseHandler);
                        },

                        mouseHandler: function (e: Event): void {
                            let self = (<HandwallData>this);
                            switch (e.type) {
                                case Event.MOUSE_DOWN:
                                    this._touching = true;
                                    self.overList = [];
                                    this.onMouseDown(e);
                                    break;
                                case Event.MOUSE_MOVE:
                                    this.onMouseMove(e);
                                    break;

                                case Event.CLICK:
                                    this.onClick(e);
                                    break;

                                case Event.MOUSE_OUT:
                                case Event.MOUSE_UP:
                                    this._checkLineEnd();
                                    this._touching = false;
                                    this.onMouseUp(e);
                                    self.overList = [];
                                    break;
                            }
                        },

                        //单点检测
                        _checkTest: function () {
                            let self = (<HandwallData>this);
                            let tile = (function () {
                                let mouseX = Laya.stage.mouseX;
                                let mouseY = Laya.stage.mouseY;
                                //碰撞检测倒序检测
                                let tileList = self.tileList.concat();
                                let i = tileList.length;
                                while (i--) {
                                    let tile = tileList[i];
                                    let img = tile.getChildAt(0);
                                    let rect = tile.localToGlobalRect(0, img.y, tile.width, tile.height);
                                    if ((rect.x <= mouseX && mouseX <= rect.x + rect.width) &&
                                        (rect.y <= mouseY && mouseY <= rect.y + rect.height)) {
                                        return tile;
                                    }
                                }
                            })();

                            if (tile) {
                                let idx = self.overList.indexOf(tile);
                                if (idx === -1) {
                                    self.setTileStage(tile, TILE_STAGE.MOUSE_OVER);
                                    self.overList.push(tile);
                                }
                            }
                            return tile;
                        },

                        //终始点检测
                        // _clickTest: function(tile,nextTile){
                        //     let img = tile.getChildAt(0);
                        //     let isUp = this.getTileStage(tile) == TILE_STAGE.ACTIVE;
                        //     let isNext = isUp ? (this.getTileStage(nextTile) == TILE_STAGE.ACTIVE ? nextTile : null) : nextTile;
                        //
                        //     let width = tile.width - (nextTile ? nextTile.x - tile.x : 0);
                        //     let rect = tile.localToGlobalRect(0, img.y, width, tile.height);
                        //     return
                        // },
                        _checkLine: function () {
                            let self = (<HandwallData>this);
                            let _startX;
                            _startX = this._line_start_x = (_startX = this._line_start_x) == null ? Laya.stage.mouseX : _startX;
                            let mouseX = Laya.stage.mouseX;
                            let mouseY = Laya.stage.mouseY;
                            let mouseXMin = Math.min(_startX, mouseX);
                            let mouseXMax = Math.max(_startX, mouseX);
                            let isClick = mouseXMax - mouseXMin < 10;
                            // console.log(mouseXMin, mouseXMax, mouseY);

                            //碰撞检测倒序检测
                            let tileList = self.tileList.concat().reverse();
                            let overListNew = [];
                            for (let i = 0, len = tileList.length; i < len; i++) {

                                //牌在鼠标划过的路径
                                let tile = tileList[i];

                                let tileNext = (function () {
                                    let idx = self.tileList.indexOf(tile);
                                    return self.tileList[idx + 1];
                                })();
                                let img = tile.getChildAt(0);
                                let stage = this.getTileStage(tile);
                                let isUp = stage == TILE_STAGE.ACTIVE;
                                tileNext = isUp ? (tileNext && this.getTileStage(tileNext) == TILE_STAGE.ACTIVE ? tileNext : null) : tileNext;

                                let width = tileNext ? Math.abs(tileNext.x - tile.x) : tile.width;
                                let rect = tile.localToGlobalRect(0, img.y, width, tile.height);
                                rect.y -= (isUp ? 120 : 0);
                                rect.height += (isUp ? 120 : 0);
                                if (rect.x + rect.width < mouseXMin) break;

                                let onLine = (
                                    (rect.x <= mouseXMin && mouseXMin <= (rect.x + rect.width))
                                    || (rect.x <= mouseXMax && mouseXMax <= (rect.x + rect.width))
                                    || (mouseXMin <= rect.x && (rect.x + rect.width) <= mouseXMax)
                                )
                                    && (rect.y <= mouseY && mouseY <= rect.y + rect.height);
                                // console.log(rect.x , rect.y, rect.width, rect.height, onLine);

                                if (onLine) {
                                    let idx = overListNew.indexOf(tile);
                                    if (idx === -1) {
                                        overListNew.push(tile)
                                    }
                                    if (isClick) break;
                                }
                            }

                            //更新牌面状态
                            self.overList.forEach(function (tile) {
                                if (overListNew.indexOf(tile) != -1) {
                                    self.setTileStage(tile, TILE_STAGE.MOUSE_OVER);
                                } else {
                                    self.setTileStage(tile, TILE_STAGE.MOUSE_OUT);
                                }
                            });
                            self.overList = overListNew;

                        },
                        _checkLineEnd: function () {
                            this._line_start_x = null;
                        },

                        onMouseDown: function (e: Event) {
                            Sound.clickCard();
                            this._checkLine();
                        },

                        onMouseMove: function (e: Event) {
                            if (!this._touching) return;
                            this._checkLine();
                        },
                        onMouseUp: function (e: Event) {
                            let self = (<HandwallData>this);
                            let overList = self.overList;
                            //console.log(overList, "========overList");
                            if (overList) {
                                let cardlist = [];
                                //获得当前滑动的牌
                                overList.forEach(card => {
                                    cardlist.push(card.data);
                                });
                                let isup = this.MoveUpTip(cardlist);
                                if (!isup) {
                                    overList.forEach(function (tile) {
                                        let stage = self.getTileStage(tile);
                                        //  console.log(tile, "=========tile");
                                        switch (stage) {
                                            case TILE_STAGE.DISABLED:
                                                return;
                                            case TILE_STAGE.ACTIVE:
                                                self.setTileActive(tile, false);
                                                break;
                                            case TILE_STAGE.NORMAL:
                                                self.setTileActive(tile, true);
                                                break;
                                        }
                                    })

                                }
                                self.refreshTile();
                            }
                        },
                        onClick: function (e: Event) {
                            let self = (<HandwallData>this);
                            let tile = this._checkTest();
                            if (tile) {

                                let isEnabled = tile.getChildAt(0).enabled;
                                if (!isEnabled) return;

                                let idx = self.selectList.indexOf(tile);
                                let isUp = idx == -1;
                                this.setTileActive(tile, isUp);
                            }
                        },

                        /**
                         * drop
                         * */
                        initDrop: function () {
                            try {
                                let self = (<HandwallData>this);
                                let list: Array<fairygui.GComponent> = self.tileList;
                                list.forEach(function (tile) {
                                    tile.draggable = true;


                                    tile.off(fairygui.Events.DRAG_END, this, this.onDropItem);
                                    tile.on(fairygui.Events.DRAG_END, this, this.onDropItem);
                                    tile.off(fairygui.Events.DRAG_MOVE, this, this.onDropMove);
                                    tile.on(fairygui.Events.DRAG_MOVE, this, this.onDropMove);
                                    tile.off(fairygui.Events.DRAG_START, this, this.onDropStart);
                                    tile.on(fairygui.Events.DRAG_START, this, this.onDropStart);
                                }, this)
                            } catch (e) { console.error(e); }

                        },


                        onDropItem: function () {
                            console.log('onDropItem', arguments);
                        },

                        onDropMove: function (evt: laya.events.Event) {
                            let self = (<HandwallData>this);
                            var hand = self.getComponent('hand_pokers');
                            console.log('onDropMove', Laya.stage.mouseX, evt.currentTarget.x, Laya.stage.mouseY, evt.currentTarget.y);
                        },
                        onDropStart: function (evt: laya.events.Event) {
                            var btn: fairygui.GLoader = <fairygui.GLoader>fairygui.GObject.cast(evt.currentTarget);
                            btn.stopDrag();//取消对原目标的拖动，换成一个替代品
                            fairygui.DragDropManager.inst.startDrag(btn, btn.url, btn.icon);
                        }


                    }
                })
            }
        }
    }
}