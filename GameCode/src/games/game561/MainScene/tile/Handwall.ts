/**
 * Created by Administrator on 2018/4/12.
 */
module G561 {
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
            dataList?: any;
            tileList?: any;
            selectList?: any;
            handCount?: any;
            cardsEnabled?: any;
            disabledList?: any;
            isShowHand?: any;
            isEnabled?: any;
            overList?: any;

            currnetAction?: any;
            isDealing3?: any;

            WATCHED?: any;

            reset?: Function;
            getSelectedData?: Function;
            resetHand?: Function;
            getUrlByData?: Function;
            setTileByData?: Function;
            resetSelected?: Function;
            resetDisabled?: Function;
            _enabledTouch?: Function;
            pass?: Function;
            update?: Function;
            remove?: Function;
            setDisabled?: Function;
            revertTile?: Function;
            setTileStage?: Function;
            resetTileStage?: Function;
            refreshTile?: Function;
            initDrop?: Function;
            getTileStage?: Function;
            setTileActive?: Function;
            initTileByData?: Function;
            clearSelectedList?: Function;

            showAction: HandwallData;
            showTileType: HandwallData;

            hand_position: any;
        }
        interface HandwallComponentData {
            hand_pokers: fairygui.GComponent;
        }


        export class Handwall {
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
                return Handwall._rfCardMap;
            }

            static getCardPath(card) {
                let cardMap = Handwall.rfCardMap();
                let name = cardMap[card];
                let path = UIMgr.getTileUrl('pokersstyle1', name);
                return path;
            }

            static create(component, localSide, isShowHand, params) {
                jx.extend(params)
                return new Vuet({
                    data: {
                        dataList: [],
                        overList: [],
                        handCount: null,
                        cardsEnabled: null,
                        selectList: [],
                        disabledList: [],
                        WATCHED: null,
                    },
                    params: {
                        playerTileList: null,
                        tileList: null,
                        localSide: localSide,
                        isShowHand: isShowHand,
                        isEnabled: isShowHand,
                        currnetAction: null,

                        _touching: false,

                        hand_position: params['hand_position'],
                        isDealing3: false,

                    },
                    watch: {
                        dataList: function (newList) {
                            //console.log('watch dataList', newList);
                            var self = (<HandwallData>this);
                            // self.resetHand();
                            self.getComponent('hand_pokers').visible = self.isShowHand;
                            self.setTileByData(self.tileList, newList, self.getComponent('hand_pokers'));
                            // //初始化拖动
                            // self.initDrop();
                        },


                        selectList: function (newList) {
                            var self = (<HandwallData>this);
                            // //console.log('watch select list', newList);
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

                        WATCHED: function (newValue) {
                            var self = (<HandwallData>this);
                            self.getComponent('clickLayer').touchable = !newValue;
                            if (newValue == null) return;

                            if (Method.isPlayingGame()) {
                                if (!newValue) {
                                    self.getComponent('hand_pokers')
                                        .getController('c1')
                                        .setSelectedPage('doWatch');
                                } else {
                                    if (self.currnetAction != 'lose' && self.currnetAction != 'giveup') {
                                        self.getComponent('hand_pokers')
                                            .getController('c1')
                                            .setSelectedPage('normal');
                                    }

                                }
                            }

                        }

                    },
                    created: function () {

                        //获取牌实例列表
                        this.tileList = this.getComponent('hand_pokers')._children.reduce(function (acc, item) {
                            return (item.group && item.group.name) == 'tileGroup'
                                ? acc.concat(item)
                                : acc;
                        }, []);
                        //是否显示手牌
                        this.getComponent('hand_pokers').visible = this.isShowHand;
                        this.resetHand();

                        //绑定看牌按钮
                        var self = (this as HandwallData);
                        if (localSide == 0) {
                            var clickLayer = self.getComponent('clickLayer').asGraph;
                            clickLayer.touchable = true;
                            clickLayer.onClick(this, function () {
                                Control.operationMgr.sendWatch();
                            });
                            Control.operationMgr.watch('WATCHED', (newValue) => {
                                self.WATCHED = newValue
                            });
                            self.WATCHED = Control.operationMgr.WATCHED;
                        } else {

                        }
                        for (let j = 0; j < 3; j++) {
                            GObjectPool.inst.removeItemToPool('G561Poker', fairygui.UIPackage.createObject('G561', 'Card'));
                        }
                    },
                    component: {
                        'hand_pokers': component['hand_pokers'],
                        'tag_Pass': component['tag_Pass'],
                        'clickLayer': component['clickLayer']
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


                        //------出牌区操作


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
                            // let self = (<HandwallData>this);
                            // this.resetSelected();
                            // var tileList = self.tileList;
                            // let list = idList.map(function(tileId){
                            //     for(let i = 0, len = tileList.length; i < len; i++){
                            //         let tile = tileList[i];
                            //         if(tile.data == tileId){
                            //             return tile;
                            //         }
                            //     }
                            //     console.error('setCardsActive error ', tileId, 'not in ', self.dataList);
                            // });
                            // self.selectList = list;
                        },

                        //根据牌设置选取状态
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

                            self.currnetAction = null;
                            self.isDealing3 = null;
                            self.resetHand();
                            GObjectPool.inst.getItemList('G561Poker').forEach((item) => {
                                GObjectPool.inst.removeItemToPool('G561Poker', item)
                            })
                        },

                        resetHand: function () {
                            let self = (<HandwallData>this);

                            self.getComponent('hand_pokers').visible = false;
                            self.isEnabled = true;


                            //切换会普通状态
                            self.getComponent('hand_pokers')
                                .getController('c1')
                                .setSelectedPage(localSide == 0 && !self.WATCHED ? 'doWatch' : 'normal');
                            self.WATCHED = null;

                            self.tileList.forEach(function (tile) {
                                tile.getController('c1').setSelectedPage('cover');
                            });


                            // self.overList = [];
                            // self.resetSelected();
                            // self.resetDisabled();
                            self.each(self.tileList, function (tile) {
                                tile.visible = false;
                                tile.data = null;
                            })
                        },


                        //------
                        //------牌墙批量操作
                        remove: function (newList) {
                            // let self = (<HandwallData>this);
                            // this.resetSelected();
                            // // 减少牌
                            // this.handCount -= newList.length;
                            // //console.log('handCount reduce', this.handCount, newList.length);
                            // // 移除牌
                            // if(!self.isShowHand) return;
                            // let dataList = this.dataList;
                            // //console.log('handwall remove ', newList, 'in', dataList);
                            // let conList = self.getComponent('hand_pokers');
                            //
                            // newList.forEach(function(rank){
                            //     let idx , list;
                            //     (idx = (list = dataList).indexOf(rank)) != -1 ? list.splice(idx, 1):'';
                            //     conList.removeChildToPoolAt(idx);
                            //     self.tileList = conList._children;
                            // })

                            // (function(list){
                            //     let selfFunc = arguments.callee;
                            //     if(!list || list.length == 0) return;
                            //     let tile = list.shift();
                            //     let idx = dataList.indexOf(tile);
                            //     if(idx !== -1){
                            //         dataList.splice(idx, 1);
                            //     }else{
                            //         //console.log('移除牌id不存在',tile, idx, dataList , this.dataList);
                            //     }
                            //     selfFunc(list);
                            // }).call(this, newList.concat());
                            //
                            // this.dataList = dataList;

                        },

                        //保留现有的牌，新增
                        addCard: function (addList) {
                            this.dataList = this.dataList
                                .concat(addList)
                                .sort(this.sortCardListFunc);
                        },

                        //移除现有的牌，更新
                        update: function (tileList) {
                            // if(!tileList)return;
                            tileList = tileList.sort(this.sortCardListFunc);
                            this.handCount = tileList.length;

                            if (tileList.toString() == this.dataList.toString()) {
                                return;
                            }
                            this.dataList = tileList;

                        },

                        //批量设置牌面
                        setTileByData: function (tileList, dataList, conList) {
                            var self = (<HandwallData>this);

                            let len = Math.max(tileList.length, dataList.length);
                            let removeList = [];
                            for (let i = 0; i < len; i++) {
                                let tile = tileList[i];
                                let currentData = dataList[i];
                                if (currentData != null) {
                                    // //有数据，说明要新增或者更改牌信息
                                    // if(!tile ){
                                    //     tile = conList.addItemFromPool().asCom;
                                    // }
                                    // tileList[i] = tile;
                                    self.initTileByData(tile, currentData);
                                } else {
                                    // //没有数据，说明要移除牌
                                    // if(tile){
                                    //     conList.removeChildToPool(tile);
                                    //     removeList.push(tile);
                                    // }
                                }
                            }
                            // //执行移除
                            // (function(list){
                            //     var selfFunc = arguments.callee;
                            //     if(list.length){
                            //         let tile = list.shift();
                            //         let idx = tileList.indexOf(tile);
                            //         tileList.splice(idx, 1);
                            //         selfFunc(list);
                            //     }
                            // })(removeList);

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
                                    case (self.disabledList.indexOf(Method.getCardNumber(tile.data)) !== -1):
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
                            return Method.compareCard(card1, card2);
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

                            switch (type) {
                                case (TILE_STAGE.NORMAL):
                                case (TILE_STAGE.ACTIVE):
                                case (TILE_STAGE.DISABLED):
                                    tile._type_last = tile._type_current || TILE_STAGE.NORMAL;
                                    tile._type_current = type;
                                    controller.setSelectedPage(type);
                                    break;
                                case (TILE_STAGE.MOUSE_OVER):
                                    tile.getTransition('disabled').play();
                                    break;
                                case (TILE_STAGE.MOUSE_OUT):
                                    tile.getTransition('enabled').play();
                                    break;
                            }
                        },
                        resetTileStage: function (tile) {
                            tile = (<fairygui.GComponent>tile);
                            // let type = TILE_STAGE.NORMAL;
                            // if (tile._type_last == type)return;
                            //
                            // tile._type_last = type;
                            // tile._type_current = type;
                            // tile.getController('c1').setSelectedPage(type);
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
                        initTileByData: function (tile, rank) {
                            var self = (<HandwallData>this);
                            if (rank == '') rank = '-';
                            tile.data = rank;
                            var img = tile.getChild('icon').asLoader;
                            // var cache = Control.Tilepool.tileCache['G561-'+rank];
                            var url = rank ? self.getUrlByData(rank) : '';
                            //var cache = Laya.loader.getRes(url);
                            let initTile = function () {
                                self.resetTileStage(tile);
                                tile.visible = true;
                            };
                            let setTile = function (instance) {
                                //img.onExternalLoadSuccess(instance);
                                img.url = instance;
                                initTile();
                                tile.getController('c1').setSelectedPage('stand');
                            };
                            // if (cache) {
                            //     setTile(cache);
                            //     return;
                            // }
                            if (rank == '-') {
                                //显示牌底
                                initTile();
                            } else {
                                setTile(url);
                                // Laya.loader.load(url, Handler.create(this, function (v, tex) {
                                //     setTile(tex);
                                //     // Control.Tilepool.tileCache['G561-' + v] = tex;
                                // }, [rank]));
                            }

                        },

                        //根据花色获取牌图片地址
                        getUrlByData: function (card) {
                            return Handwall.getCardPath(card);
                        },

                        //------

                        //------炸金花
                        showAction: function (action) {
                            let self = <HandwallData>this;
                            let mapAction2Name = {
                                [ACTION.GIVEUP]: 'giveup',
                                [ACTION.LOOKTILE]: 'watch',
                                [ACTION.FIGHTLOSE]: 'lose',
                            };
                            let name = mapAction2Name[action];

                            //如果是失败或者弃牌，禁止点击
                            if (name == 'giveup' || name == 'lose')
                                self.getComponent('clickLayer').touchable = false;

                            //如果放弃或者比牌失败再点看牌，要终止
                            if (name == 'watch' && (self.currnetAction == 'giveup' || self.currnetAction == 'lose'))
                                return;

                            if (name) {
                                self.currnetAction = name;
                                self.getComponent('hand_pokers')
                                    .getController('c1')
                                    .setSelectedPage(name);
                            }
                            return self;
                        },

                        showTileType: function (action) {
                            let self = <HandwallData>this;
                            let mapAction2Name = {
                                [ACTION_TILE.BAOZI]: 'baozi',
                                [ACTION_TILE.SHUNJIN]: 'shunjin',
                                [ACTION_TILE.JINHUA]: 'jinhua',
                                [ACTION_TILE.SHUNZI]: 'shunzi',
                                [ACTION_TILE.PAIR]: 'duizi',
                                [ACTION_TILE.SINGLE]: 'danpai',
                            };
                            let name = mapAction2Name[action];
                            //如果放弃或者比牌失败再点看牌，要终止
                            if (self.currnetAction == 'giveup' || self.currnetAction == 'lose')
                                return;
                            if (name)
                                self.getComponent('hand_pokers')
                                    .getController('c1')
                                    .setSelectedPage(name);

                            return self;
                        },

                        deal3: function (list?) {
                            let self = (<HandwallData>this);
                            if (self.isDealing3) return;
                            self.isDealing3 = true;
                            // this.dataList = list || ['-', '-', '-'];
                            // let wall = self.getComponent('hand_pokers');
                            // let target = { x: wall.x, y: wall.y };
                            // wall.x = Laya.stage.width / 2;
                            // wall.y = Laya.stage.height / 2;
                            // Laya.Tween.to(wall, target, 500, Laya.Ease.expoOut, Laya.Handler.create(this, function () {
                            //     self.isDealing3 = false;
                            // }));
                            //初始缩放
                            let startScale = 0.0;
                            //每轮间隔
                            let dealDelta = 100;
                            //单张运动时间
                            let duration = 1000;
                            let cards: Array<fairygui.GComponent> = [];
                            for (let i = 0; i < 3; i++) {
                                Tools.inst.setTimeout((i) => {
                                    let card = GObjectPool.inst.getItemFormPool('G561Poker').asCom;
                                    card.getChildAt(0).asLoader.url = self.getUrlByData('-');
                                    card.data = '-';
                                    card.setScale(this.tileList[i].scaleX, this.tileList[i].scaleY);
                                    let centerPoi: { x: number, y: number } = {
                                        x: Laya.stage.width / 2 - card.actualWidth * 0.5,
                                        y: Laya.stage.height / 2 - card.actualHeight * 0.5,
                                    };
                                    card.setXY(centerPoi.x, centerPoi.y);
                                    G561.page.view.getChild('chipLayout').asGraph.addBeforeMe(card);
                                    card.visible = true;
                                    cards.push(card);
                                    let Pos = FairyguiTools.getOtherLocalPos(this.tileList[i], card);
                                    let endPoi = { x: Pos.x, y: Pos.y };
                                    if (localSide == 0) {
                                        endPoi = {
                                            x: Pos.x - card.width * (card.scaleX - 1) * 0.5,
                                            y: Pos.y - card.height * (card.scaleX - 1) * 1,
                                        }
                                    }
                                    Tween.from(card, { scaleX: startScale, scaleY: startScale }, duration, laya.utils.Ease.quintOut);
                                    Tween.to(card, endPoi, duration, laya.utils.Ease.cubicInOut, Handler.create(this, () => {
                                        //this.view.setChildIndex(card, this.cardParentIndex - 1 + (i * sides.length + j));
                                        if (i == 2) {
                                            this.dataList = list || ['-', '-', '-'];
                                            self.isDealing3 = false;
                                            for (let k = 0; k < 3; k++) {
                                                const card = cards[k];
                                                GObjectPool.inst.removeItemToPool('G561Poker', card);
                                            }
                                        }
                                    }));
                                }, dealDelta * i, i);
                            }
                        },

                        //触摸事件
                        /**
                         * 鼠标响应事件处理
                         */
                        _enabledTouch: function () {
                            let self = (<HandwallData>this);
                            let handwall = self.getComponent('hand_pokers');
                            // //拖动选牌
                            // handwall.on(Event.MOUSE_DOWN, this, this.mouseHandler);
                            // handwall.on(Event.MOUSE_UP, this, this.mouseHandler);
                            // handwall.on(Event.MOUSE_OUT, this, this.mouseHandler);
                            // handwall.on(Event.MOUSE_MOVE, this, this.mouseHandler);

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
                        _checkLine: function () {
                            let self = (<HandwallData>this);
                            let _startX;
                            _startX = this._line_start_x = (_startX = this._line_start_x) == null ? Laya.stage.mouseX : _startX;
                            let mouseX = Laya.stage.mouseX;
                            let mouseY = Laya.stage.mouseY;
                            let mouseXMin = Math.min(_startX, mouseX);
                            let mouseXMax = Math.max(_startX, mouseX);
                            // //console.log(mouseXMin, mouseXMax, mouseY);

                            //碰撞检测倒序检测
                            let tileList = self.tileList.concat();
                            let overListNew = [];
                            for (let i = 0, len = tileList.length; i < len; i++) {

                                //牌在鼠标划过的路径
                                let tile = tileList[i];
                                let tileNext = (function () {
                                    let idx = self.tileList.indexOf(tile);
                                    return self.tileList[idx + 1];
                                })();
                                let img = tile.getChildAt(0);
                                let width = tileNext ? (tileNext.x - tile.x) : tile.width;
                                let rect = tile.localToGlobalRect(0, img.y, width, tile.height);
                                if (rect.x > mouseXMax) break;

                                let onLine = (
                                    (rect.x <= mouseXMin && mouseXMin <= (rect.x + rect.width))
                                    || (rect.x <= mouseXMax && mouseXMax <= (rect.x + rect.width))
                                    || (mouseXMin <= rect.x && (rect.x + rect.width) <= mouseXMax)
                                )
                                    && (rect.y <= mouseY && mouseY <= rect.y + rect.height);
                                // //console.log(rect.x , rect.y, rect.width, rect.height, onLine);

                                if (onLine) {
                                    let idx = overListNew.indexOf(tile);
                                    if (idx === -1) {
                                        overListNew.push(tile)

                                    }
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
                            this._checkLine();
                        },

                        onMouseMove: function (e: Event) {
                            if (!this._touching) return;
                            this._checkLine();
                        },
                        onMouseUp: function (e: Event) {
                            let self = (<HandwallData>this);
                            let overList = self.overList;

                            if (overList) {
                                overList.forEach(function (tile) {
                                    let stage = self.getTileStage(tile);

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
                            //console.log('onDropItem', arguments);
                        },

                        onDropMove: function (evt: laya.events.Event) {
                            let self = (<HandwallData>this);
                            var hand = self.getComponent('hand_pokers');
                            //console.log('onDropMove', Laya.stage.mouseX, evt.currentTarget.x, Laya.stage.mouseY, evt.currentTarget.y);
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