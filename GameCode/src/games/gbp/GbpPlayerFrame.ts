class GbpPlayerFrame extends GallPlayerFrame {
    protected dealerCtl: fairygui.Controller;
    protected tfScore: fairygui.GComponent;

    public out_pokers: fairygui.GList;
    protected out_nnStr: fairygui.GComponent;
    protected out_nnCtl: fairygui.Controller;
    protected out_QStr: fairygui.GComponent;
    protected out_QCtl: fairygui.Controller;
    protected out_BStr: fairygui.GLabel;
    protected out_BCtl: fairygui.Controller;
    protected lightkMark: fairygui.GComponent;

    protected layerIndex: number;
    protected striveBankerMask: fairygui.GImage;

    protected original_out_pokers_y: number;
    protected original_out_pokers_x: number;
    public isBullFinishValue = false;

    constructor(components: Object) {
        super(components);
        let component = this.seat;
        this.dealerCtl = component.getController('c1');
        this.tfScore = component.getChild('tfScore').asLabel;
        this.lightkMark = component.getChild('light').asCom;

        this.out_pokers = components['out_pokers'];
        this.original_out_pokers_y = this.out_pokers.y;
        this.original_out_pokers_x = this.out_pokers.x;

        this.out_nnStr = components['out_nnStr'];
        this.out_nnCtl = this.out_nnStr.getController('c1');

        this.out_BStr = components['out_BStr'];
        this.out_BCtl = this.out_BStr.getController('c1');

        this.out_QStr = components['out_QStr'];
        this.out_QCtl = this.out_QStr.getController('c1');

        this.layerIndex = this.seat.parent.getChildIndex(this.seat);
        this.striveBankerMask = this.seat.getChild('striveBankerMask').asImage;

    }


    setLayerTop() {
        this.seat.parent.setChildIndex(this.seat, this.seat.parent.numChildren - 2);
    }

    resetLayerIndex() {
        this.seat.parent.setChildIndex(this.seat, this.layerIndex);
    }

    shineStriveBankerMask(score: number, cb?: (...params: any[]) => void, ...params: any[]) {
        let num = 0;
        let func = () => {
            if (num < 7) {
                num++;
                if (score > 0) {
                    this.striveBankerMask.visible = !this.striveBankerMask.visible;
                }
                Laya.timer.once(150, this, func);
            }
            else {
                if (cb != null) {
                    cb(...params);
                }
            }
        }
        func();
    }

    showStriveBankerMask() {
        this.striveBankerMask.visible = true;
    }

    hideStriveBankerMask() {
        this.striveBankerMask.visible = false;
    }

    getOutPokerX() {
        return this.out_pokers.x;
    }

    getOutPokerY() {
        return this.out_pokers.y;
    }

    getSeatX() {
        return this.seat.x
    }
    getSeatY() {
        return this.seat.y
    }

    setPlayerSex(sex) {
        this.sex = sex;
    }

    getPlaterSex() {
        return this.sex;
    }

    setLightMark(show = false) {
        this.lightkMark.visible = show;
    }

    updateBankerState(dealer) {
        this.dealerCtl.setSelectedIndex(dealer ? 1 : 0);
        this.out_QStr.visible = dealer;
    }

    balanceScore(num) {
        this.setScoreString(this.score + parseFloat(num));
    }

    setScoreAction(num, cb?: (...params) => void, ...params) {
        let score = parseFloat(num) || 0;
        let tempStr = Tools.inst.changeGoldToMoney(score);
        let finStr = score < 0 ? (tempStr) : ("+" + tempStr)
        let selectedIdx = score < 0 ? 1 : 2;
        let scoreCtl = this.tfScore.getController("c1");
        let scoreLabel = this.tfScore.getChild('title' + selectedIdx).asLabel;
        let scoreAni = this.tfScore.getTransition('tfScoreActon' + selectedIdx);

        scoreCtl.setSelectedIndex(selectedIdx);
        // scoreLabel.text = finStr;
        this.tfScore.visible = true;
        scoreAni.play();
        this.numRun(scoreLabel, score, cb, ...params);
    }

    numRun(numBox, maxNum, endFunc?: (...params) => void, ...params) {
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
    }

    clear() {
        this.seat.visible = false;
        this.isInit = false;
        this.resetOutPokersAction();
    }

    resetGame() {
        this.out_pokers.visible = false;
        this.out_nnStr.visible = false;
        this.out_BStr.visible = false;
        this.tfScore.visible = false;
        this.lightkMark.visible = false;
        this.isBullFinishValue = false;
        this.hideStriveBankerMask();
        this.updateBankerState(false);
    }

    setWagerStr(value) {
        this.out_BCtl.setSelectedIndex(value);
        let ani = this.out_BStr.getTransitionAt(0);
        this.out_BStr.visible = true;
        this.out_QStr.visible = false;
    }

    getBstr() {
        return this.out_BStr;
    }

    showQiang(show: boolean, num: number = 0) {
        this.out_QCtl.setSelectedIndex(num);
        let ani = this.out_QStr.getTransitionAt(0);
        this.out_QStr.visible = show;
    }

    getQiangIndex() {
        if (!this.seat.visible) return -1;
        return this.out_QCtl.selectedIndex;
    }

    setCards(tiles, effectFunc?: (outPokers: fairygui.GList, ...param) => any, ...param) {
        var outPokers = this.out_pokers;
        for (let i = outPokers.numChildren - 1; i >= 0; i--) {
            this.setPoker(outPokers.getChildAt(i).asCom.getChildAt(0), null)
            outPokers.removeChildAt(i);
        }
        this.addCards(tiles);
        outPokers.visible = true;
    }

    addCards(tiles, action = false) {
        var outPokers = this.out_pokers;
        for (let i = 0; i < tiles.length; ++i) {
            var value = tiles[i];
            //if(!value)continue;
            var pokerComp = outPokers.addItemFromPool().asCom;
            pokerComp.data = value;
            var poker = pokerComp.getChildAt(0);
            this.setPoker(poker.asLoader, value);
            pokerComp.y = (outPokers.numChildren > 5 ? 50 : 0);
            pokerComp.visible = true;
            if (action)
                Tween.from(pokerComp, { y: 100 }, 400, Ease.backOut);
        }
    }

    public setPoker(pokerComp, value) {
        let pkgName = 'pokers';
        if (value != null && value != '') {
            UIMgr.setPoker(pokerComp, pkgName, 'card_' + value);
        } else {
            UIMgr.setPoker(pokerComp, pkgName, 'card_backface');
        }
    }

    public getPokerUrl(value) {
        let pkgName = 'pokers';
        if (value != null && value != '')
            return UIMgr.getTileUrl(pkgName, 'card_' + value);
        else
            return UIMgr.getTileUrl(pkgName, 'card_backface');
    }

    showBullStr(bullnum: number) {
        //SoundMgrNiu.playNiuEffect(bullnum, this.sex);
        this.out_nnCtl.setSelectedIndex(bullnum);
        this.out_nnStr.visible = true;
        this.out_nnStr.getTransitionAt(0).play();
    }

    isBullFinish(): boolean {
        return this.out_nnStr.visible || this.isBullFinishValue
    }

    showOutPokersAction() {
        let tween = Laya.Tween;
        let posY = this.out_pokers.y;
        tween.to(this.out_pokers, { y: posY - 35 }, 300, Laya.Ease.expoOut)
    }

    resetOutPokersAction() {
        this.out_pokers.setXY(this.original_out_pokers_x, this.original_out_pokers_y);
    }

    showPokersAni(ids: Array<string>, cb?: () => void) {
        let delta = 30;
        for (let i = 0; i < ids.length; i++) {
            let id = ids[i];
            let delay = i * delta;
            let card = this.out_pokers.getChildAt(i);
            let ani = card.asCom.getTransition('showCard');
            let loader = card.asCom.getChildAt(0).asLoader;
            if (ani == null) {
                loader.url = this.getPokerUrl(id);
                if (i == ids.length - 1) {
                    cb();
                }
            } else {
                ani.setHook('setCardId', Handler.create(this, (i, loader: fairygui.GLoader) => {
                    loader.url = this.getPokerUrl(id);
                }, [i, loader]))
                Laya.timer.once(delay, this, () => {
                    if (i == ids.length - 1) {
                        ani.play(Handler.create(this, () => {
                            cb();
                        }))
                    }
                    else {
                        ani.play();
                    }
                })

            }
        }
    }

    showOnePokerAni(index: number, id: string, cb?: () => void) {
        let card = this.out_pokers.getChildAt(index);
        let ani = card.asCom.getTransition('showCard');
        let loader = card.asCom.getChildAt(0).asLoader;
        if (ani == null) {
            loader.url = this.getPokerUrl(id);
            cb();
        } else {
            ani.setHook('setCardId', Handler.create(this, () => {
                loader.url = this.getPokerUrl(id);
            }));
            ani.play(Handler.create(this, () => {
                cb();
            }));
        }
    }

    onDispose() {
        Laya.timer.clearAll(this);
        Laya.timer.clearAll(this.out_pokers);
    }
}