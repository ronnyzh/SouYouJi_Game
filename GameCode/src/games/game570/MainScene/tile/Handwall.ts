module G570 {
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
            tileoutList?: Array<any>;//批量显示牌面

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

            fapaiside?: number;
        }
        interface HandwallComponentData {
            hand_pokers: fairygui.GComponent;
        }


        export class Handwall extends G560.fl.Handwall {

            //static SHOW_EFFECT_DURING = 130; //动画持续时间,ms
            static DEAL_CARDS_DURING =1;//发牌时间间隔
            constructor() {
                super();
            }
            static create(component, localSide, isShowHand) {
                let base = super.create(component, localSide, isShowHand);
                let params: any = base._config;
                params.method.reset = function () {
                    let self = (<HandwallData>this);
                    self.resetHand();
                    self.resetOut();

                    self.showEffect = false;
                    self.updateCallback = null;
                    self.fapaiside = -1;
                    self.tileoutList = null;
                    // this.dataList = [];
                    // this.tileList = [];
                    // this.outTileList = [];
                    // this.handCount = 0;
                }
                params.method.resetHand = function () {
                    let self = (<HandwallData>this);
                    let conList = self.getComponent('hand_pokers');
                    conList.visible = false;
                    //  conList.removeChildToPool();
                    self.isEnabled = true;

                    self.overList = [];
                    self.resetSelected();
                    self.resetDisabled();
                    self.each(self.tileList, function (tile) {
                        tile.visible = false;
                        tile.getController('gray').selectedIndex = 0;
                        tile.data = null;
                    })
                    self.isDealer = false;
                    // this.dataList = [];
                }
                params.method.resetOut = function () {
                    let self = (<HandwallData>this);
                    let outwall = self.getComponent('outwall');
                    outwall.visible = true;
                    self.each(self.outTileList, function (item) {
                        item.visible = false;
                    });
                    self.getComponent('tag_Pass').visible = false;
                }
                params.method.remove = function (newList) {
                    let self = (<HandwallData>this);
                    this.resetSelected();
                    // 减少牌
                    this.handCount -= newList.length;
                    //console.log('handCount reduce', this.handCount, newList.length);
                    // 移除牌
                    if (!self.isShowHand) return;
                    let dataList = this.dataList;
                    //console.log('handwall remove ', newList, 'in', dataList);
                    let conList: fairygui.GList = self.getComponent('hand_pokers');
                    newList.forEach(function (rank) {
                        let idx, list;
                        (idx = (list = dataList).lastIndexOf(rank)) != -1 ? list.splice(idx, 1) : '';
                        let card = conList.getChildAt(idx);
                        card.asCom.getController('gray').selectedIndex = 0;
                        conList.removeChildToPool(card);
                        self.tileList = conList._children;
                        // console.log(self.tileList, "===============self.tileList");
                    })

                }
                params.method.grayHandPoker = function (num: number) {
                    var self = (<HandwallData>this);
                    let hand_pokers: fairygui.GList = self.getComponent('hand_pokers');
                    // console.log(num, hand_pokers.numChildren, "===========num");
                    for (let i = 0; i < num; i++) {
                        let card = hand_pokers.getChildAt(i).asCom;
                        let GrayControl = card.getController('gray');
                        // console.log(GrayControl, "===========手牌变灰的数量");
                        GrayControl.selectedIndex = 1;
                    }
                }
                params.method.HandPokerRecoverypos = function () {
                    var self = (<HandwallData>this);
                    let hand_pokers: fairygui.GList = self.getComponent('hand_pokers');
                    hand_pokers.touchable = true;
                    for (let i = 0; i < hand_pokers.numChildren; i++) {
                        let card = hand_pokers.getChildAt(i).asCom.getChild('card').asGroup;
                        card.x = 0;
                        card.y = 0;
                    }
                }
                params.method.HandpokeMovePos = function (addList) {
                    var self = (<HandwallData>this);
                    let newList: Array<string> = this.dataList.concat(addList).sort(this.sortCardListFunc);
                    let hand_pokers: fairygui.GList = self.getComponent('hand_pokers');
                    //  let posList: Array<{ x: number, y: number }> = [];
                    let card = hand_pokers.getChildAt(0).asCom;
                    //  let startX = card.getChild('card').asGroup.x;
                    let columnGap = (card.actualWidth + hand_pokers.columnGap) * hand_pokers.scaleX;
                    columnGap = Math.ceil(columnGap);
                    //console.log(columnGap, "======columnGap")
                    let posy = card.getChild('card').asGroup.y;
                    if (self.localSide == 0) {
                        for (let i = 0; i < this.dataList.length; i++) {
                            let index = newList.indexOf(this.dataList[i]);
                            let card = hand_pokers.getChildAt(i).asCom;
                            let posx = (columnGap * index) - card.x;
                            //posList.push()
                            //console.log(posx, index, "========index");
                            let cardAni = card.getTransition('move');
                            cardAni.setValue('endpos', posx, posy);
                            cardAni.play();
                            // posList.push({ x: posx, y: posy });
                        }
                    }
                    else {
                        for (let i = 0; i < this.dataList.length; i++) {
                            let posx = columnGap * i;
                            // posList.push({ x: posx, y: posy });
                            let cardAni = hand_pokers.getChildAt(i).asCom.getTransition('move');
                            cardAni.setValue('endpos', posx, posy);
                            cardAni.play();
                        }
                    }
                    // return posList;
                }
                params.method.getHandCardpos = function (index) {
                    // console.log(this.localSide, index, "=========手牌对象");
                    var self = (<HandwallData>this);
                    let hand_pokers: fairygui.GList = self.getComponent('hand_pokers');

                    let pos: { x: number, y: number } = { x: 0, y: 0 };
                    let scale = hand_pokers.scaleX;
                    if (index < hand_pokers.numChildren) {
                        let card = hand_pokers.getChildAt(index).asCom;
                        pos.x = card.getChildAt(0).localToGlobal(0, 0).x;
                        pos.y = card.getChildAt(0).localToGlobal(0, 0).y;
                        // let sp = new Laya.Sprite();
                        // Laya.stage.addChild(sp);
                        // //  let pos = { x: 0, y: 0 };
                        // sp.graphics.drawCircle(pos.x, pos.y, 3, '#ff0000', 2);
                    }
                    let data = {
                        'pos': pos,
                        'scale': scale,
                    }
                    // console.log(data,"===========data");
                    return data;
                }
                params.method.showCard = function (index) {
                    var self = (<HandwallData>this);
                    let hand_pokers: fairygui.GList = self.getComponent('hand_pokers');
                    // if (index < hand_pokers.numChildren)
                    //     hand_pokers.getChildAt(index).asCom.visible = true;
                    for (let i = 0; i < hand_pokers.numChildren; i++) {
                        let item = hand_pokers.getChildAt(i);
                        item.visible = true;
                        item.touchable = true;
                    }
                }
                params.method.getAddCardPos = function (addList) {
                    var self = (<HandwallData>this);
                    let newList: Array<string> = this.dataList.concat(addList).sort(this.sortCardListFunc);
                    let posList: Array<{ x: number, y: number }> = [];
                    let hand_pokers: fairygui.GList = self.getComponent('hand_pokers');
                    let card = hand_pokers.getChildAt(0).asCom;
                    let columnGap = (card.width + hand_pokers.columnGap) * hand_pokers.scaleX;
                    let startX = card.getChildAt(0).localToGlobal(0, 0).x;
                    let posy;
                    if (this.localSide == 0)
                        posy = card.getChildAt(0).localToGlobal(0, 0).y + card.getChildAt(0).height / 4 * hand_pokers.scaleY;
                    else {
                        posy = card.getChildAt(0).localToGlobal(0, 0).y + card.getChildAt(0).height / 2 * hand_pokers.scaleY;
                        columnGap = Math.ceil(columnGap);
                    }
                    let addCardsIndex = [];
                    if (self.localSide == 0) {
                        for (let i = 0; i < addList.length; i++) {
                            let index = newList.indexOf(addList[i]);
                            if (index != -1 && hand_pokers.numChildren > 0) {
                                let posx = startX + columnGap * index;
                                posList.push({ x: posx, y: posy });
                                addCardsIndex.push(index - addCardsIndex.length);
                            }
                        }
                    }
                    else {
                        let index = hand_pokers.numChildren - 1;
                        for (let i = 0; i < addList.length; i++) {
                            index += 1;
                            let posx = startX + columnGap * index;
                            posList.push({ x: posx, y: posy });
                            addCardsIndex.push(index - addCardsIndex.length);
                        }
                    }
                    return { posList, addCardsIndex };
                }
                params.method.RobMoveHandCards = function (addCardsIndex: Array<number>) {
                    // console.log('addCardsIndex', addCardsIndex);
                    var self = (<HandwallData>this);
                    this.resetSelected();
                    let hand_pokers: fairygui.GList = self.getComponent('hand_pokers');
                    hand_pokers.touchable = false
                    let firstCard = hand_pokers.getChildAt(0).asCom;
                    let columnGap = (firstCard.width + hand_pokers.columnGap) * hand_pokers.scaleX;
                    columnGap = Math.ceil(columnGap);
                    let originalHandPokerX = firstCard.x;
                    let startX = Math.ceil(originalHandPokerX - 1.5 * columnGap);
                    let addnum = 0;
                    for (let i = 0; i < hand_pokers.numChildren; i++) {
                        let card = hand_pokers.getChildAt(i).asCom;
                        let cardAni = card.getTransition('move');
                        let originalX = originalHandPokerX + i * columnGap;
                        let index = addCardsIndex.indexOf(i)
                        if (index != -1) {
                            let temp = 0;
                            do {
                                addnum++;
                                temp++;
                            } while (index + temp < addCardsIndex.length && addCardsIndex[index + temp - 1] == addCardsIndex[index + temp]);
                        }
                        let endX = startX + (i + addnum) * columnGap;
                        let posX = endX - originalX;
                        cardAni.setValue('endpos', posX, 0);
                        cardAni.play();
                    }
                }
                params.method.gethandpokerscale = function () {
                    var self = (<HandwallData>this);
                    let hand_pokers: fairygui.GList = self.getComponent('hand_pokers');
                    return hand_pokers.scaleX;
                }
                params.method.update = function (tileList, fapaiside = -1, isShowEffect?, callback?) {
                    // if (fapaiside != -1)
                    //     console.log(fapaiside, this.dataList, tileList, "===========update");
                    var self = (<HandwallData>this);
                    self.fapaiside = fapaiside;
                    self.showEffect = isShowEffect;
                    self.updateCallback = function () {
                        self.updateCallback = null;
                        self.showEffect = false;
                        if (callback) callback();
                    };
                    if (fapaiside != 1) {
                        // console.log(tileList, "==========排序");
                        tileList = tileList.sort(this.sortCardListFunc);
                    }

                    this.handCount = tileList.length;
                    //console.log(fapaiside, tileList, "=========tileList")
                    if (tileList.toString() == this.dataList.toString() && fapaiside == -1) {
                        //  if (tileList.toString() == this.dataList.toString()) {
                        return;
                    }
                    this.dataList = tileList;
                }
                params.method.setTileByData = function (tileList, dataList, conList, listtype, localSide) {
                    var self = (<HandwallData>this);
                    var isOneLine;
                    var isMoveTile;
                    var onLoaded;
                    var setLoaded;

                    //避免因为没有子集导致计算错误
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
                    // console.log(len, self.fapaiside, "=======设置牌面");
                    for (let i = 0; i < len; i++) {
                        let tile = tileList[i];
                        let currentData = dataList[i];
                        if (currentData) {
                            //有数据，说明要新增或者更改牌信息
                            var hasInstance = Boolean(tile);
                            if (!tile) {
                                tile = conList.addItemFromPool().asCom;
                                //tile.getController('gray').selectedIndex = 0;
                            }
                            tileList[i] = tile;
                            tile.visible = (!(hasInstance || self.showEffect));
                            // console.warn(dataList.length, tile.visible, 'self.showEffect', self.showEffect, '_isLoaded', _isLoaded);
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
                    //  console.log(self.showEffect, "==============self.showEffect");
                    if (!self.showEffect) {
                        if (typeof self.updateCallback == "function") self.updateCallback();
                    } else {
                        var during = Handwall.SHOW_EFFECT_DURING;
                        var animate = function () {
                            //console.log(dataList, "=====animate======")
                            if (listtype == 0 && self.fapaiside != -1) {
                                conList._children.forEach((item, index, array) => {
                                    if (index >= array.length - 1 && index != 0 && isOneLine) return;
                                    item.visible = false;
                                    item.touchable = false;
                                    item.getController('gray').selectedIndex = 0;
                                })
                                self.fapaiside = -1;
                                if (typeof self.updateCallback == "function") self.updateCallback();
                            }
                            else {
                                Method.setTimeout(function () {
                                    //做垃圾动画
                                    conList._children.forEach((item, index, array) => {
                                        if (index >= array.length - 1 && index != 0 && isOneLine) return;
                                        item.visible = false;
                                        Method.setTimeout(function () {
                                            item.visible = true;

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
                                            lastTile.visible = true;
                                            let list = [];
                                            for (let i = 0; i < array.length; i++)
                                                list.push(array[i].data);
                                            var copy = lastTile.getChildAt(0);
                                            // var x = copy.x;
                                            var x = 0;
                                            // copy.x = 0;
                                            //  copy.x = firstTile.x - lastTile.x;
                                            if (lastTile.x != 0)
                                                copy.x = - lastTile.x;
                                            else
                                                copy.x = conList.scaleX * spacing * (array.length - 1);
                                            //  console.log(list, x, copy.x, firstTile.x, lastTile.x, "=========array");
                                            //  if (array != self.tileoutList) {
                                            //  copy.x -= (lastTile.x - firstTile.x);

                                            // self.tileoutList = array;
                                            //  }
                                            Laya.Tween.to(copy, { x: x }, during * (array.length - 1), Laya.Ease.linearNone, Laya.Handler.create(this, function () {
                                                if (typeof self.updateCallback == "function") self.updateCallback();
                                            }));
                                        }
                                        else {
                                            if (typeof self.updateCallback == "function") self.updateCallback();
                                        }
                                    } else {
                                        Method.setTimeout(function () {
                                            if (typeof self.updateCallback == "function") self.updateCallback();
                                        }, during * (array.length - 1));
                                    }
                                }.bind(this), 30)
                            }
                        }.bind(this);
                        onLoaded(animate);
                        conList.visible = true;
                    }
                }
                return new Vuet(params);
            }
        }
    }
}