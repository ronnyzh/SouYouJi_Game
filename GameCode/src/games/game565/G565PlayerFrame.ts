module G565 {
    export class G565PlayerFrame {
        public side: number;
        public sex: number;
        public bidNumber: number = 0;
        public isInit: boolean = false;
        private score: number;
        private state: number;
        private timerMax: number = 0;
        private timerValue: number = 0;
        private seat: fairygui.GComponent;
        private seatText: fairygui.GComponent;
        private nameText: fairygui.GLabel;
        private scoreText: fairygui.GLabel;
        private chipText: fairygui.GLabel;
        private scoreChangeText: fairygui.GComponent;
        private imgHead: fairygui.GLoader;
        private miniHandCard: MiniHandCard;
        private handCard: HandCard;
        private timer: fairygui.GProgressBar;
        private allCallNumberText: fairygui.GLabel;
        private timerMask: laya.display.Sprite;
        private timerSprite: laya.display.Sprite;
        private allCallNumber: number;

        set AllCallNumber(value: number) {
            this.allCallNumber = value;
            this.allCallNumberText.text = ''/* value == 0 ? '' : Tools.inst.changeGoldToMoney(value) */;
        }

        get AllCallNumber() {
            return this.allCallNumber;
        }

        private static stateMap: { [key: number]: number } = {
            //隐藏
            0: 0,
            //弃牌
            1: 5,
            //跟注
            2: 1,
            //加注
            3: 2,
            //过牌
            4: 4,
            //全压
            5: 3,
            //小盲注
            10: 6,
            //大盲注
            11: 7,
        }

        private static handCardTypeMap: { [key: number]: number } = {
            //0,无,1,皇家同花顺,2,同花顺3,金刚,4,葫芦,5,同花,6,顺子,7,三条,8,两对,9,一对,10,高牌*/
            //隐藏
            0: 0,
            //皇家同花顺
            1: 10,
            // 同花顺
            2: 9,
            // 金刚
            3: 8,
            // 葫芦        
            4: 7,
            // 同花
            5: 6,
            // 顺子
            6: 5,
            // 三条
            7: 4,
            // 两对 
            8: 3,
            // 一对
            9: 2,
            // 高牌 
            10: 1,
        }

        onDispose() {
            this.miniHandCard.onDispose();
        }

        constructor(data: {
            side: number,
            seat: fairygui.GComponent,
            seatText: fairygui.GComponent,
            parent: fairygui.GComponent,
        }) {
            this.side = data.side;
            this.seat = data.seat;
            this.seatText = data.seatText
            this.nameText = this.seatText.getChild('nameText').asLabel;
            this.scoreText = this.seatText.getChild('scoreText').asLabel;
            this.chipText = this.seatText.getChild('chipText').asLabel;
            this.imgHead = this.seat.getChild('icon').asLoader;
            this.scoreChangeText = this.seat.getChild('txtChangeScore').asCom;
            this.timer = this.seat.getChild('mask').asProgress;
            if (this.side == 0) {
                this.handCard = new HandCard(data.parent.getChild('selfHandCard').asCom, this.side);
                this.seat.getController('showHandCard').selectedPage = 'false';
            } else {
                this.handCard = new HandCard(this.seat.getChild('handCard').asCom, this.side);
                this.seat.getController('showHandCard').selectedPage = 'true';
            }
            this.miniHandCard = new MiniHandCard(data.parent, this.side);

            this.allCallNumberText = this.seatText.getChild('allCallNumberText').asLabel;


            this.timerSprite = this.timer.getChild('bar').displayObject;
            this.timerMask = new laya.display.Sprite();
            this.timerSprite.mask = this.timerMask
        }

        setSeat(data, scoreDef: string = '') {
            if (!data) return;
            if (this.side != 0)
                this.nameText.text = Tools.inst.maskUserName(data['nickname']);
            else
                Tools.inst.SetNickNameAfter(this.nameText, data['nickname']);
            this.sex = parseInt(data['sex'] || 0);
            this.setScoreString(parseFloat(data['coin'] || 0), scoreDef);
            this.imgHead.url = 'ui://la8oslyoosvmbg';
            var headImgUrl = data['headImgUrl'];
            try {
                if (headImgUrl)
                    Tools.inst.changeHeadIcon(headImgUrl, this.imgHead);
                else if (this.side == 0)
                    Tools.inst.changeHeadIcon(UserMgr.inst.imgUrl, this.imgHead);
            } catch (error) {
                console.log(error)
            }
            this.seatText.visible = true;
            this.seat.visible = true;
            this.isInit = true;
        }

        private setScoreText(def: string = '0') {
            this.scoreText.text = Tools.inst.changeGoldToMoney(this.score, def);
        }

        updateBankerState(dealer: boolean) {
            this.seat.getController('banker').setSelectedIndex(dealer ? 1 : 0);
        }

        changeScore(num) {
            num = parseFloat(num) || 0;
            // this.score += (num);
            // this.setScoreText();
            let addScore: string = Tools.inst.changeGoldToMoney(num);
            let scoreCtl = this.scoreChangeText.getController("c1");
            let selectedIdx = num < 0 ? 1 : 2
            scoreCtl.selectedIndex = selectedIdx;
            this.scoreChangeText.visible = true;
            let scoreText = this.scoreChangeText.getChild('title' + selectedIdx).asLabel;
            scoreText.text = num >= 0 ? '+' + addScore : addScore;
            this.scoreChangeText.getTransition('tfScoreActon' + selectedIdx).play();
        }

        setScoreString(score, def: string = '0') {
            this.score = score;
            this.setScoreText(def);
        }

        clear() {
            this.AllCallNumber = 0;
            this.seat.visible = false;
            this.seatText.visible = false;
            this.updateBankerState(false);
            this.scoreChangeText.visible = false;
            this.State = 0;
            this.setMask(0);
            this.win(false);
            this.hideBid();
            this.handCard.hide();
            this.miniHandCard.hide();
            this.isInit = false;
        }

        bid(value: number) {
            if (value != null) {
                this.seat.getController('bid').selectedIndex = 0;
                this.seatText.getController('bid').selectedIndex = 0;
                this.bidNumber += value;
                this.AllCallNumber += value;
                this.chipText.text = Tools.inst.changeGoldToMoney(this.bidNumber);
                this.setChipColor(Tools.inst.changeMoneyToGold(Tools.inst.changeGoldToMoney(this.bidNumber)));
            }
        }

        setChipColor(value: number) {
            let chip = this.seat.getChild('chip').asCom;
            let colorCtl = chip.getController('color');
            if (value >= 1000) {
                colorCtl.selectedIndex = ChipItemMgr.colorMap._1000;
            } else if (value >= 500) {
                colorCtl.selectedIndex = ChipItemMgr.colorMap._500;
            } else if (value >= 250) {
                colorCtl.selectedIndex = ChipItemMgr.colorMap._250;
            } else if (value >= 200) {
                colorCtl.selectedIndex = ChipItemMgr.colorMap._200;
            } else if (value >= 100) {
                colorCtl.selectedIndex = ChipItemMgr.colorMap._100;
            } else if (value >= 50) {
                colorCtl.selectedIndex = ChipItemMgr.colorMap._50;
            } else if (value >= 10) {
                colorCtl.selectedIndex = ChipItemMgr.colorMap._10;
            } else if (value >= 5) {
                colorCtl.selectedIndex = ChipItemMgr.colorMap._5;
            } else if (value >= 1) {
                colorCtl.selectedIndex = ChipItemMgr.colorMap._1;
            } else {
                colorCtl.selectedIndex = ChipItemMgr.colorMap._0;
            }
        }

        /**stateIndex 0隐藏 1 弃牌; 2 跟注; 3 加注; 4 过牌; 5 全压; 10 小盲注; 11 大盲注;
         * @param stateIndex 0隐藏 1 弃牌; 2 跟注; 3 加注; 4 过牌; 5 全压; 10 小盲注; 11 大盲注;
         * */
        set State(stateIndex: number) {
            if (stateIndex == null) {
                stateIndex = 0;
            }
            this.state = stateIndex;
            this.seat.getController('state').selectedIndex = G565PlayerFrame.stateMap[stateIndex];
            if (this.seat.getController('state').selectedIndex != 0) {
                this.seat.getTransitionAt(0).play();
            }
            if (stateIndex != 0 && stateIndex != null && stateIndex != 10 && stateIndex != 11) {
                SoundMgrDeZhou.action(G565PlayerFrame.stateMap[stateIndex], this.sex);
            }
        }

        get State() {
            return this.state;
        }


        /**number 0,无,1,红,2,黄,3,绿,4,灰头像
         * @param number 0,无,1,红,2,黄,3,绿,4,灰头像
         * */
        setMask(number: number) {
            this.timerMask.graphics.clear();
            this.timer.getController('mask').selectedIndex = number;
        }

        getMask() {
            return this.timer.getController('mask').selectedIndex;
        }

        set TimerMax(max: number) {
            this.timerMax = max;
        }

        get TimerMax() {
            return this.timerMax;
        }

        set TimerValue(value: number) {
            this.timerValue = value;
            this.updataTimer();
        }

        get TimerValue() {
            return this.timerValue;
        }

        updataTimer() {
            this.timerMask.graphics.clear();
            if (this.TimerValue / this.TimerMax >= 0.66) {
                this.setMask(3);
            } else if (this.TimerValue / this.TimerMax >= 0.33) {
                this.setMask(2);
            } else {
                this.setMask(1);
            }
            this.timerMask.graphics.drawPie(this.timerSprite.width / 2, this.timerSprite.height / 2, 78, (-90 + (1 - (this.TimerValue / this.TimerMax)) * 360), 270, '#ffffff');
        }

        win(value: boolean) {
            this.seat.getController('win').selectedIndex = value ? 1 : 0;
        }

        getWinValue() {
            return this.seat.getController('win').selectedIndex == 1;
        }

        hideBid() {
            this.seat.getController('bid').selectedIndex = 1;
            this.seatText.getController('bid').selectedIndex = 1;
            this.bidNumber = 0;
            this.chipText.text = '';
        }

        getBidVisible() {
            return this.seat.getController('bid').selectedIndex == 0;
        }

        getBankerTagPoi() {
            let bankerTag = this.seat.getChild('imgBankerTag').asCom;
            return this.seat.localToGlobal(bankerTag.x, bankerTag.y);
        }

        getChipTagPoi() {
            let chipTag = this.seat.getChild('chip');
            return this.seat.localToGlobal(chipTag.x, chipTag.y);
        }

        getChipPoi() {
            let chipPoi = this.seat.getChild('chipPoi').asCom;
            return this.seat.localToGlobal(chipPoi.x, chipPoi.y);
        }

        getScore() {
            return this.score;
        }

        playShowMiniHandCard(index: number, cardId?: string, onComplete?: (...params) => void, times?: number, delay?: number, ...params) {
            let handler: Handler;
            if (cardId == null) {
                handler = Handler.create(this, () => {
                    if (onComplete != null) {
                        onComplete(...params)
                    }
                }, [], true)
            }
            else {
                handler = Handler.create(this, () => {
                    this.miniHandCard.playShowHandCard(index, cardId, () => {
                        this.handCard.cards[index].visible = true;
                        this.handCard.cards[index].setCardId(cardId);
                    });
                    if (onComplete != null) {
                        onComplete(...params)
                    }
                })
            }
            this.miniHandCard.playShowMiniCard(index, handler, times, delay);
        }

        setMiniHandCard(ids: Array<string>) {
            this.miniHandCard.show(ids);
        }

        hideMiniHandCard() {
            this.miniHandCard.hide();
        }

        playHideMiniHandCard(onComplete?: laya.utils.Handler, times?: number, delay?: number) {
            this.miniHandCard.playHideMiniCard(onComplete, times, delay);
        }

        showHandCard(index: number, cardid: string, onComplete?: Function, params?: Array<any>, times?: number, delay?: number) {
            this.miniHandCard.playShowHandCard(index, cardid, () => {
                this.handCard.cards[index].visible = true;
                this.handCard.cards[index].setCardId(cardid);
                if (onComplete != null) {
                    onComplete(...params)
                }
            }, times, delay);
        }

        setHandCard(ids: Array<string>) {
            for (let i = 0; i < 2; i++) {
                let id = ids[i];
                this.handCard.cards[i].visible = true;
                this.handCard.cards[i].setCardId(id);
            }
        }

        /**@param resultIndex 0,无,1,皇家同花顺,2,同花顺3,金刚,4,葫芦,5,同花,6,顺子,7,三条,8,两对,9,一对,10,高牌*/
        setHandCardMask(showCards: Array<boolean>, resultIndex: number) {
            if (showCards != null) {
                this.handCard.setMask(showCards[0], showCards[1], true);
            }
            if (resultIndex != null) {
                this.handCard.setResult(G565PlayerFrame.handCardTypeMap[resultIndex]);
            }

        }

        getHandCardIdList() {
            return this.handCard.getCardIdList();
        }

        get visible() {
            return this.seat.visible;
        }
    }

    class MiniHandCard {
        private cards: Array<G565CardItem> = [];
        private showMiniCardAnis: Array<fairygui.Transition> = [];
        private hideMiniCardAni: fairygui.Transition;
        private showHandAnis: Array<fairygui.Transition> = [];
        constructor(parent: fairygui.GComponent, side: number) {
            let miniHandCardName = 'miniHandCard';
            let showMiniHandCardName = 'showMiniHandCard';
            let hideMiniHandCardName = 'hideMiniHandCard';
            let showHandCardName = 'showHandCard';
            let postfix = ['_0', '_1'];
            for (let i = 0; i < 2; i++) {
                this.cards[i] = new G565CardItem(parent.getChild(miniHandCardName + side + postfix[i]).asCom);
                this.showMiniCardAnis[i] = parent.getTransition(showMiniHandCardName + side + postfix[i]);
                this.showHandAnis[i] = parent.getTransition(showHandCardName + side + postfix[i]);
            }
            this.hideMiniCardAni = parent.getTransition(hideMiniHandCardName + side);
        }

        playShowMiniCard(index: number, onComplete?: laya.utils.Handler, times?: number, delay?: number) {
            this.cards[index].visible = true;
            this.cards[index].setScale(0.45, 0.45)
            this.cards[index].setCardId('');
            this.showMiniCardAnis[index].play(onComplete, times, delay);
        }

        playHideMiniCard(onComplete?: laya.utils.Handler, times?: number, delay?: number) {
            this.hideMiniCardAni.play(onComplete, times, delay);
        }

        playShowHandCard(index: number, cardid: string, onComplete?: () => void, times?: number, delay?: number) {
            this.cards[index].setCardId('');
            this.showHandAnis[index].setHook('showCard', Handler.create(this, () => {
                this.cards[index].setCardId(cardid);
            }));
            this.showHandAnis[index].play(Handler.create(this, () => {
                Laya.timer.frameOnce(10, this, () => {
                    this.cards[index].visible = false;
                })
                if (onComplete != null) {
                    onComplete();
                }
            }), times, delay);
        }

        show(ids: Array<string>) {
            for (let index = 0; index < 2; index++) {
                this.cards[index].visible = true;
                this.cards[index].setCardId(ids[index] == null ? '' : ids[index]);
                this.showMiniCardAnis[index].play();
                this.showMiniCardAnis[index].stop(true);
            }
        }

        hide() {
            for (let i = 0; i < this.cards.length; i++) {
                this.cards[i].visible = false;
            }
        }

        onDispose() {
            Laya.timer.clearAll(this);
        }
    }

    class HandCard {
        public cards: Array<G565CardItem> = [];
        private cardMask: fairygui.GComponent;

        constructor(parent: fairygui.GComponent, side: number) {
            this.cards[0] = new G565CardItem(parent.getChild('card0').asCom);
            this.cards[1] = new G565CardItem(parent.getChild('card1').asCom);
            this.cardMask = parent;
        }

        setMask(showCard0: boolean, showCard1: boolean, isShadow: boolean = false) {
            let showCtl = this.cardMask.getController('showCard');
            let shadowCtl = this.cardMask.getController('shadow');
            // showCtl.selectedPage = (showCard0 ? '1' : '0') + (showCard1 ? '1' : '0');
            if (isShadow) {
                shadowCtl.selectedPage = (showCard0 ? '0' : '1') + (showCard1 ? '0' : '1');
            } else {
                shadowCtl.selectedPage = '00';
            }
        }

        /** @param resultIndex 0,无,1,高牌,2,一对,3,两对,4,三条,5,顺子,6,同花,7,葫芦,8,金刚,9,同花顺,10,皇家同花顺*/
        setResult(resultIndex: number) {
            this.cardMask.getController('result').selectedIndex = resultIndex;
        }

        hide() {
            for (let i = 0; i < this.cards.length; i++) {
                this.cards[i].visible = false;
                this.cards[i].setCardId('');
            }
            this.setResult(0);
            this.setMask(false, false);
        }

        getCardIdList() {
            return [this.cards[0].ID, this.cards[1].ID];
        }
    }

    export class G565DeskCard {
        private deskCards: Array<G565CardItem> = [];
        private deskCardMasks: Array<fairygui.GComponent> = [];
        private showDeskCardAnis: Array<fairygui.Transition> = [];
        constructor(parent: fairygui.GComponent) {
            let deskCardName = 'deskCard';
            let deskCardMaskName = 'deskCardMask';
            let showDeskCardName = 'showDeskCard';
            for (let i = 0; i < 5; i++) {
                this.deskCards.push(new G565CardItem(parent.getChild(deskCardName + i).asCom));
                this.deskCardMasks.push(parent.getChild(deskCardMaskName + i).asCom);
                this.showDeskCardAnis.push(parent.getTransition(showDeskCardName + i));
            }
        }

        setMask(indexs: Array<boolean>, isShadow: boolean = false) {
            for (let i = 0; i < this.deskCardMasks.length; i++) {
                if (i < indexs.length) {
                    if (indexs[i] == true) {
                        //this.deskCardMasks[i].getController('mask').selectedIndex = 1;
                        this.deskCardMasks[i].getController('mask').selectedIndex = 0;
                    }
                    else {
                        if (isShadow == false) {
                            this.deskCardMasks[i].getController('mask').selectedIndex = 0;
                        } else {
                            this.deskCardMasks[i].getController('mask').selectedIndex = 2;
                        }
                    }
                } else {
                    this.deskCardMasks[i].getController('mask').selectedIndex = 0;
                }

            }
        }

        showDeskCard(index: number, id: string, onComplete?: laya.utils.Handler, times?: number, delay?: number) {
            this.deskCards[index].visible = true;
            this.deskCards[index].setCardId('')
            this.showDeskCardAnis[index].setHook('showCard', Handler.create(this, () => {
                this.deskCards[index].setCardId(id)
            }));
            this.showDeskCardAnis[index].play(onComplete, times, delay);
        }

        setDeskCard(ids: Array<string>) {
            for (let i = 0; i < ids.length; i++) {
                this.deskCards[i].visible = true;
                this.deskCards[i].setCardId(ids[i]);
            }
        }

        hide() {
            for (let i = 0; i < this.deskCards.length; i++) {
                this.deskCards[i].setCardId('');
                this.deskCards[i].visible = false;
                this.deskCardMasks[i].getController('mask').selectedIndex = 0;
            }
        }

        getCardIdList() {
            let idList = [];
            for (var i = 0; i < this.deskCards.length; i++) {
                var card = this.deskCards[i];
                if (card.ID != '') {
                    idList.push(card.ID);
                }
            }
            return idList;
        }
    }
    export class G565CardItem {
        private item: fairygui.GComponent;
        private id: string;
        constructor(item: fairygui.GComponent) {
            this.item = item;
            this.setCardId('');
        }
        setCardId(id: string) {
            this.id = id;
            if (id == '') { id = 'Back' }
            this.item.getController('id').selectedPage = id;
        }
        setScale(sx: number, sy: number) {
            this.item.setScale(sx, sy);
        }
        get visible() {
            return this.item.visible;
        }
        set visible(value: boolean) {
            this.item.visible = value;
        }

        get ID() {
            return this.id;
        }

        public static compareCard(id1: string, id2: string) {
            let numList = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'];
            let typeList = ['a', 'b', 'c', 'd'];
            let num1 = numList.indexOf(id1.substring(0, 1));
            let num2 = numList.indexOf(id2.substring(0, 1));
            if (num1 == num2) {
                let type1 = typeList.indexOf(id1.substring(1));
                let type2 = typeList.indexOf(id2.substring(1));
                return type1 < type2;
            }
            return num1 < num2;
        }
    }
}