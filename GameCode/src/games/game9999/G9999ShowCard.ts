module G9999 {
    export class G9999ShowCard extends Page {

        private resultCtl: fairygui.Controller;
        private resultAni: fairygui.Transition;
        private resultLoader: fairygui.GLoader;
        private comXian: { card0: Card, card1: Card, card2: Card, score: fairygui.GLabel };
        private comZhuang: { card0: Card, card1: Card, card2: Card, score: fairygui.GLabel };

        constructor() {
            super('G9999', 'ShowCard', UILayer.GAME);
            this.keepCenter();
        }

        onCreated(data: any = null) {
            let view = this.view;
            this.resultCtl = view.getControllerAt(0);
            this.resultAni = view.getTransitionAt(0);
            this.comXian = {
                card0: new Card(view.getChild('xianCard0').asCom),
                card1: new Card(view.getChild('xianCard1').asCom),
                card2: new Card(view.getChild('xianCard2').asCom),
                score: view.getChild('txtXianScore').asLabel,
            };
            this.comZhuang = {
                card0: new Card(view.getChild('zhuangCard0').asCom),
                card1: new Card(view.getChild('zhuangCard1').asCom),
                card2: new Card(view.getChild('zhuangCard2').asCom),
                score: view.getChild('txtZhuangScore').asLabel,
            };
            this.resultLoader = view.getChild('result').asLoader;
            view.visible = false;
        }

        get visible() {
            return this.view.visible;
        }

        set visible(value: boolean) {
            this.view.visible = value;
        }

        onDispose() {

        }

        show(xianIDs: { id0: string, id1: string, id2: string }, xianFinValue: number, zhuangIDs: { id0: string, id1: string, id2: string }, zhuangFinValue: number, result: number, onComplete?: Handler, times?: number, delay?: number) {
            
            this.reset();
            this.visible = true;
            let cardList = [this.comXian.card0, this.comZhuang.card0, this.comXian.card1, this.comZhuang.card1, this.comXian.card2, this.comZhuang.card2];
            let ids = [xianIDs.id0, zhuangIDs.id0, xianIDs.id1, zhuangIDs.id1, xianIDs.id2, zhuangIDs.id2];
            let cardIndex = 0;
            let xianValue = 0;
            let zhuangValue = 0;
            let func: () => void;
            let tempfunc = () => {
                if (cardIndex < cardList.length) {
                    cardList[cardIndex].playReversalAni(ids[cardIndex], Handler.create(this, func, [], true), 1, 0.1);
                }
                else if (cardIndex == cardList.length) {
                    this.comXian.score.text = xianFinValue.toString();
                    this.comZhuang.score.text = zhuangFinValue.toString();
                    this.resultAni.setHook('start', Handler.create(this, () => {
                        switch (result.toString()) {
                            case '2':
                                this.resultCtl.selectedPage = '闲赢';
                                break;
                            case '1':
                                this.resultCtl.selectedPage = '庄赢';
                                break;
                            case '0':
                                this.resultCtl.selectedPage = '和';
                                break;
                            default:
                                this.resultCtl.selectedPage = '无';
                                //console.log('error result is:', result);
                                break;
                        }
                    }, [], true));
                    this.resultAni.play(onComplete, times, delay);
                }
                if (cardIndex > 0) {
                    let lastCardValue = Card.getCardValue(ids[cardIndex - 1]);
                    if ((cardIndex - 1) % 2 == 0) {
                        xianValue += lastCardValue;
                        this.comXian.score.text = (xianValue % 10).toString();
                    }
                    else {
                        zhuangValue += lastCardValue;
                        this.comZhuang.score.text = (zhuangValue % 10).toString();
                    }
                }
                cardIndex++;
            }
            func = tempfunc;
            func();
        }

        reset() {
            this.resultCtl.selectedPage = '无';
            this.comXian.card0.visible = false;
            this.comXian.card1.visible = false;
            this.comXian.card2.visible = false;
            this.comXian.score.text = '0';
            this.comZhuang.card0.visible = false;
            this.comZhuang.card1.visible = false;
            this.comZhuang.card2.visible = false;
            this.comZhuang.score.text = '0';
            this.resultLoader.visible = false;
        }
    }

    class Card {
        public item: fairygui.GComponent;
        private aniReversal: fairygui.Transition;
        constructor(item: fairygui.GComponent) {
            this.item = item;
            this.aniReversal = this.item.getTransitionAt(0);
            let cardMap = Card.CardMap;
        }

        set visible(value: boolean) {
            this.item.visible = value;
        }

        get visible() {
            return this.item.visible;
        }

        playReversalAni(cardid: string, onComplete?: Handler, times?: number, delay?: number) {
            if ((cardid != null) && (cardid != '')) {
                this.item.icon = Card.getCardPath('');
                this.visible = true;
                this.aniReversal.play(onComplete, times, delay);
                this.aniReversal.setHook('center', Handler.create(this, () => {
                    //sound
                    SoundMgrBaccarat.cards_dealing();
                    this.item.icon = Card.getCardPath(cardid);
                }, [], true))
            }
            else if (onComplete != null) {
                this.item.icon = '';
                this.aniReversal.play(onComplete, times, delay);
                Laya.timer.once(100, this, () => {
                    this.aniReversal.stop(true, true);
                })
            }
        }

        private static get CardMap() {
            if (Card.cardMap == null) {
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
                Card.cardMap = numList.reduce((acc, num) => {
                    suitList.forEach(suit => {
                        if (suit == 'w') return;
                        var realSuit = mapSuit[suit] || suit;
                        var realNum = mapNum[num] || num;
                        acc[num + suit] = 'card_' + realSuit + realNum;
                    });
                    return acc;
                }, {})
                Card.cardMap[''] = 'card_backface';
            }
            return Card.cardMap;
        }
        private static cardMap;
        static getCardPath(cardId: string) {
            let cardMap = Card.cardMap;
            let name = cardMap[cardId];
            let path = ResourceMgr.RES_PATH+'pokers/FTLpoker/' + name + '.png';
            return path;
        }
        private static cardValueMap;
        private static get CardValueMap() {
            if (Card.cardValueMap == null) {
                Card.cardValueMap = {
                    ['A']: 1,
                    ['2']: 2,
                    ['3']: 3,
                    ['4']: 4,
                    ['5']: 5,
                    ['6']: 6,
                    ['7']: 7,
                    ['8']: 8,
                    ['9']: 9,
                }
            }
            return Card.cardValueMap;
        }
        static getCardValue(cardId: string): number {
            let value = 0;
            if (cardId == null) { cardId = ''; }
            if (Card.CardValueMap[cardId[0]] != null) {
                value = parseInt(Card.CardValueMap[cardId[0]]);
            }
            return value;
        }

    }
}