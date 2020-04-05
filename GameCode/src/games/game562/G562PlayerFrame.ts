/*
* name;
*/
module G562 {
    export class G562PlayerFrame {

        private seat: fairygui.GComponent;
        private nameText: fairygui.GLabel;
        private score: number;
        private imgHead: fairygui.GLoader;
        private dealerCtl: fairygui.Controller;
        private tfScore: fairygui.GComponent;
        //  private tfScore: fairygui.GTextField;
        private headgoldtxt: fairygui.GTextField;
        private sex: any;

        private hand_cards: fairygui.GComponent;
        private qiang: fairygui.GComponent;
        private imgType: fairygui.GComponent;
        private special: fairygui.GComponent;
        private ok: fairygui.GComponent;
        private dongList: Array<any> = [];
        private scaleCtl: fairygui.Controller;

        private shui: fairygui.GTextField;
        private Txt_total_score: fairygui.GTextField;
        private Txt_total_score_bule: fairygui.GTextField;
        private gun_0_txt: fairygui.GTextField;
        private gun_1_txt: fairygui.GTextField;
        constructor(components: Object) {
            let component = components['seat'];
            //  let component_txt = components['seat_txt'];
            this.seat = component;
            // this.seattxt = component_txt;
            let player = component.getChild('player').asCom;
            this.nameText = player.getChild('name').asLabel;
            this.tfScore = player.getChild('tfScore').asCom;
            // this.scoreText = component_txt.getChild('score').asLabel;
            this.imgHead = player.getChild('icon').asLoader;
            this.dealerCtl = component.getController('c1');
            this.headgoldtxt = player.getChild('score');
            // this.tfScore = component_txt.getChild('score');
            this.shui = component.getChild('shuitxt');
            this.hand_cards = components['hand_cards'];
            this.hand_cards.visible = false;
            this.ok = components["ok"];
            this.qiang = components["qiang"];
            this.imgType = components["imgType"];
            this.special = components["special"];

            this.Txt_total_score = components["Txt_total_score"];
            this.Txt_total_score_bule = components["Txt_total_score_bule"];
            this.gun_0_txt = components["gun_0_txt"];
            this.gun_1_txt = components["gun_1_txt"];
            this.scaleCtl = components["scaleCtl"];

            if (!laya.renders.Render.isWebGL)
                this.setcacheAs();

        }
        setcacheAs() {
            this.seat.displayObject.cacheAs = "bitmap";
            this.headgoldtxt.displayObject.cacheAs = "bitmap";
            this.ok.displayObject.cacheAs = "bitmap";
            this.shui.displayObject.cacheAs = "bitmap";
            this.Txt_total_score.displayObject.cacheAs = "bitmap";
            this.Txt_total_score_bule.displayObject.cacheAs = "bitmap";
            this.gun_0_txt.displayObject.cacheAs = "bitmap";
            this.gun_1_txt.displayObject.cacheAs = "bitmap";
        }
        setSeat(data, side) {
            if (!data) return;
            if (side != 0)
                this.nameText.text = Tools.inst.maskUserName(data['nickname']);
            else
                Tools.inst.SetNickNameAfter(this.nameText, data['nickname']);
            //this.score = parseInt(data['coin'] || 0);
            this.score = parseFloat(data['coin'] || 0);
            this.headgoldtxt.visible = true;
            this.headgoldtxt.text = '' + Tools.inst.changeGoldToMoney(this.score, '');
            //this.headgoldtxt.text = '' + Tools.inst.TableParseFloat(this.score);
            this.sex = parseInt(data['sex'] || 0);
            this.shui.visible = true;
            this.shui.text = parseFloat(data["w_num"] || 0).toString();

            this.imgHead.url = 'ui://la8oslyoosvmbg';
            var headImgUrl = data['headImgUrl'];
            try {
                if (headImgUrl)
                    Tools.inst.changeHeadIcon(headImgUrl, this.imgHead);
                else if (side == 0)
                    Tools.inst.changeHeadIcon(UserMgr.inst.imgUrl, this.imgHead);
            } catch (error) {
                console.log(error)
            }
            this.seat.visible = true;
        }

        updateBankerState(dealer) {
            // this.dealerCtl.setSelectedIndex(dealer ? 1 : 0);

        }
        balanceScore(num) {
            // this.score += parseInt(num);
            this.score += parseFloat(num);
            //  this.scoreText.text = '' + Tools.inst.TableParseFloat(this.score);
            this.headgoldtxt.visible = true;
            this.headgoldtxt.text = '' + Tools.inst.changeGoldToMoney(this.score);

        }
        showshuiScore(num) {
            this.shui.text = num.toString();
        }
        getSeatX() {
            return this.seat.x
        }

        getSeatY() {
            return this.seat.y
        }
        getHardCardX() {
            return this.hand_cards.x;
        }
        getHardCardY() {
            return this.hand_cards.y;
        }
        getsex() {
            return this.sex;
        }
        clear() {
            //  console.log("-----clear-----");
            this.seat.visible = false;
            this.hand_cards.visible = false;
            this.ok.visible = false;
            this.shui.visible = false;

            this.qiang.visible = false;
            this.imgType.visible = false;
            this.special.visible = false;
            this.headgoldtxt.visible = false;
            this.Txt_total_score.visible = false;
            this.Txt_total_score_bule.visible = false;
            this.tfScore.visible = false;
            this.gun_0_txt.visible = false;
            this.gun_1_txt.visible = false;
            this.iserror = 0;
            Laya.timer.clearAll(this);
        }

        resetGame(side) {
            // console.log("-----resetGame----");
            this.hand_cards.visible = false;
            this.scaleCtl.selectedIndex = 0;
            this.ok.visible = false;
            this.iserror = 0;

            this.special.visible = false;
            this.imgType.visible = false;
            this.qiang.visible = false;
            this.Txt_total_score.visible = false;
            this.Txt_total_score_bule.visible = false;
            this.tfScore.visible = false;
            this.gun_0_txt.visible = false;
            this.gun_1_txt.visible = false;
            if (this.dongList != null && this.dongList.length > 0) {
                for (let i = this.dongList.length - 1; i >= 0; i--) {
                    let img = this.dongList.shift();
                    img.dispose();
                }
            }
            // for (let i = 0; i < this.hand_cards.numChildren - 1; i++) {
            this.hand_cards.setChildIndex(this.hand_cards.getChild("lipai"), this.hand_cards.numChildren - 1);
            // }
        }
        //0代表打枪的人，1代表洞
        showshoot(type: number, rotating, score) {

            if (type == 0) {
                SoundMgrShiSanShui.shoot();

                this.qiang.visible = true;
                this.qiang.getTransition("Ani").play();
                //  console.log(rotating, "=========rotating");
                this.qiang.rotation = rotating;
                if (rotating >= 90 || rotating <= -90)
                    this.qiang.scaleY = -1;
                else
                    this.qiang.scaleY = 1;
                //console.log(qiang.rotation, "=========qiang.rotation");
            }
            else if (type == 1) {
                for (let i = 0; i < (Math.random() + 1) * 5; i++) {
                    let img = fairygui.UIPackage.createObject('G562', 'dong').asCom;
                    this.dongList.push(img);
                    let dong = this.hand_cards.addChild(img);
                    dong.visible = true;
                    dong.x = (Math.random() * this.hand_cards.width / 2) + this.hand_cards.width / 5;
                    dong.y = (Math.random() * this.hand_cards.height / 2) + this.hand_cards.height / 5;
                }

            }
        }
        hideshoot() {
            this.qiang.visible = false;
            if (this.dongList != null && this.dongList.length > 0) {
                for (let i = this.dongList.length - 1; i >= 0; i--) {
                    let img = this.dongList.shift();
                    img.dispose();
                }
            }
        }
        private iserror: number = 0;//发牌异常
        setfapai(showcallback) {
            this.setScaleCtl(0);

            for (let i = 0; i < 13; i++) {
                let loader = this.hand_cards.getChildAt(i).asCom.getChild("n0").asLoader;
                if (loader != null) {
                    loader.url = twa.UI_CARD["card_back"];
                }
                else {
                    //可能会为空加载不出
                    this.iserror += 1;
                    //console.log(this.iserror, "=======this.iserror");
                    if (this.iserror > 1) {
                        // Alert.show('-------发牌异常-------');
                    }
                    else if (this.iserror == 1) {
                        Laya.timer.once(30, this, this.setfapai, [showcallback]);
                    }
                }
            }
            this.hand_cards.getTransition("fapaiAni").play(new Handler(this, function () {
                this.hand_cards.getController("state").selectedIndex = 1;
                if (showcallback != null)
                    showcallback()
            }));
        }
        settotal_score(score) {
            // if (score < 0) {
            //     this.Txt_total_score.visible = false;
            //     this.Txt_total_score_bule.visible = true;
            //     // console.log(score, "==============score");
            //     this.Txt_total_score_bule.text = parseFloat(Tools.inst.changeGoldToMoney(score)).toString();
            // }
            // else {
            //     this.Txt_total_score.visible = true;
            //     this.Txt_total_score_bule.visible = false;
            //     this.Txt_total_score.text = "+" + parseFloat(Tools.inst.changeGoldToMoney(score)).toString();
            // }
            // this.Txt_total_score.text = "+" + "10000,00000000";
            score = parseFloat(score) || 0;
            let addScore: string = Tools.inst.changeGoldToMoney(score);
            let scoreCtl = this.tfScore.getController("c1");
            let selectedIdx = score < 0 ? 1 : 2
            scoreCtl.selectedIndex = selectedIdx;
            this.tfScore.visible = true;
            let scoreText = this.tfScore.getChild('title' + selectedIdx).asLabel;
            scoreText.text = score >= 0 ? '+' + addScore.toString() : addScore.toString();
            this.tfScore.getTransition('tfScoreActon' + selectedIdx).play();

        }
        setqiang(gun0, gun1) {
          //  console.log(gun0, gun1, "============打枪中枪");
            if (gun0.length == 0) {
                if (gun1.length > 0) {
                    this.gun_0_txt.visible = true;
                    gun1 = gun1.split("x");
                    if (gun1.length > 1)
                        this.gun_0_txt.text = ExtendMgr.inst.getText4Language(gun1[0]) + "x" + gun1[1];
                    else
                        this.gun_0_txt.text = ExtendMgr.inst.getText4Language(gun1[0]);
                }

            }
            else {
                this.gun_0_txt.visible = true;
                gun0 = gun0.split("x");
                if (gun0.length > 1)
                    this.gun_0_txt.text = ExtendMgr.inst.getText4Language(gun0[0]) + "x" + gun0[1];
                else
                    this.gun_0_txt.text = ExtendMgr.inst.getText4Language(gun0[0])

                if (gun1.length > 0) {
                    this.gun_1_txt.visible = true;
                    gun1 = gun1.split("x");
                    if (gun1.length > 1)
                        this.gun_1_txt.text = ExtendMgr.inst.getText4Language(gun1[0]) + "x" + gun1[1];
                    else
                        this.gun_1_txt.text = ExtendMgr.inst.getText4Language(gun1[0])
                }
            }
        }
        setScaleCtl(statenum: number) {
            this.hand_cards.visible = true;
            this.ok.visible = false;
            if (statenum == this.scaleCtl.selectedIndex)
                return;
            this.hand_cards.getTransition('cardsAni').stop();
            this.scaleCtl.selectedIndex = statenum;

        }
        setHandCard(statenum: number, tiles) {
            // console.log("========setHandCard=======");
            this.setScaleCtl(1);
            this.hand_cards.getController("state").selectedIndex = 0;
            if (statenum == 0) {
                this.setbackface();
            }
            else if (statenum == 1 && tiles != null) {
            }
            else if (tiles == null) {
                this.setbackface();
            }
            // console.log(this.hand_cards, "========this.hand_cards");
        }
        setReady() {
            this.ok.visible = true;
        }
        setSpecial(cardList: Array<string>, cardType = null) {
            this.setScaleCtl(0);
            this.hand_cards.getController("state").selectedIndex = 0;
            for (let i = 0; i < cardList.length; i++) {
                let card = this.hand_cards.getChildAt(i);
                let carduiname = "card_" + cardList[i].toString();
                card.asCom.getChild("n0").asLoader.url = twa.UI_CARD[carduiname];
            }
            //声音
            if (cardType != null) {
                this.special.visible = true;
                SoundMgrShiSanShui.Type(cardType, this.sex);
                this.special.getController("type").selectedIndex = cardType - 11;
                this.hand_cards.getTransition("special").play(new Handler(this, function () {
                    this.special.visible = false;
                }));
            }

        }
        setNormalcard(cardList: Array<string>) {
            this.setScaleCtl(1);
            this.hand_cards.getController('state').selectedIndex = 0;
            for (let i = 0; i < cardList.length; i++) {
                let indexList = cardList[i].split(',');
                for (let j = 0; j < indexList.length; j++) {
                    let carduiname = "card_" + indexList[j].toString();
                    let card;
                    if (i == 0) {
                        card = this.hand_cards.getChildAt(j).asCom;
                    }
                    else if (i == 1) {
                        card = this.hand_cards.getChildAt(3 + j).asCom;
                    }
                    else if (i == 2) {
                        card = this.hand_cards.getChildAt(8 + j).asCom;
                    }

                    card.visible = true;
                    card.getChild("n0").asLoader.url = twa.UI_CARD[carduiname];
                }
            }
        }
        setCompareCard(index: number, cardList: Array<string>, cardType: number, localCtl) {
            // this.seat.visible = false;
            this.setScaleCtl(1);
            this.hand_cards.getController('state').selectedIndex = 0;
            let Type;
            // let num;
            if (index == 0) {
                Type = "tou";
                // num = 0;
            }
            else if (index == 1) {
                Type = "zhong";
                // num = 3;
            }
            else if (index == 2) {
                Type = "wei";
                // num = 8;
            }
            //let obj = this.hand_cards.getChild(Type).asCom;
            let cardComList = [];
            let carduinameList = [];
            for (let i = 0; i < cardList.length; i++) {
                let carduiname = "card_" + cardList[i].toString();
                let card = this.hand_cards.getChildAt(i).asCom;
                card.visible = true;
                cardComList.push(card);
                carduinameList.push(carduiname);
            }
            for (let i = 0; i < cardComList.length; i++) {
                let card = cardComList[i];
                this.hand_cards.setChildIndex(card, this.hand_cards.numChildren - 1);
            }
            localCtl.selectedIndex = index;
            this.imgType.visible = true;
            this.imgType.getController("type").selectedIndex = cardType;
            //声音
            SoundMgrShiSanShui.Type(cardType, this.sex);
            this.hand_cards.getTransition(Type + "Ani").setHook('showCard', Handler.create(this, () => {
                for (let i = 0; i < cardComList.length; i++) {
                    let card = cardComList[i];
                    card.getChild("n0").asLoader.url = twa.UI_CARD[carduinameList[i]];
                }
            }, [], true));
            this.hand_cards.getTransition(Type + "Ani").play(Handler.create(this, () => {
                for (let i = 0; i < cardComList.length; i++) {
                    let card = cardComList[i];
                    // this.hand_cards.setChildIndex(card, i + num);
                }
            }, [], true));
            // this.hand_cards.getChild(Type).asCom.invalidateBatchingEveryFrame = true;
            this.imgType.getTransition("imgAni").play(
                Handler.create(this, function () {
                    this.imgType.visible = false;
                    // this.hand_cards.setChildIndex(obj, childindex);
                }, [], true)
            )
        }
        setbackface() {
            for (let i = 0; i < 13; i++) {
                var card = this.hand_cards.getChildAt(i).asCom.getChild("n0").asLoader;
                card.visible = true;
                card.url = twa.UI_CARD["card_back"];
            }
        }
        getHardcardstage() {
            return this.hand_cards.getController("state").selectedIndex;
        }
        setCards(tiles) {

        }
        setOtherCards() {

        }
        arrangedCards() {

        }
        getOutPokerX() {

        }
        getOutPokerY() {

        }

        private static _pokerCache = {};
        public setPoker(pokerComp, value) {
            let cache = G562PlayerFrame._pokerCache[value];
            if (cache) {
                pokerComp.onExternalLoadSuccess(cache);
                return;
            }
            let url = this.getPokerUrl(value);
            Laya.loader.load(url, Handler.create(this, function (v, tex) {
                pokerComp.onExternalLoadSuccess(tex);
                G562PlayerFrame._pokerCache[v] = tex;
            }, [value]));
        }
        public getPokerUrl(value) {
            let url = ResourceMgr.RES_PATH + 'pokers/cards/';
            if (value)
                url += 'card_' + value + '.png';
            else
                url += 'card_backface.png';
            return url;
        }

        showBullStr(bullnum: number) {

        }
    }
}