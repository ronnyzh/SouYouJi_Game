module G562 {
    export class G562ChooseCard extends Page {
        // export class G562ChooseCard {
        constructor() {
            super("G562", "choosecard", UILayer.GAME);
            // console.log("=========G562====G56ChooseCard======");
            // this.keepCenter();

        }

        private chooseClt: fairygui.Controller = null;
        private Card_Btn: Array<fairygui.GButton> = [];

        private Txt_Time_1: fairygui.GTextField = null;
        private Txt_Time_2: fairygui.GTextField = null;
        private DeleteBtn: { [key: string]: fairygui.GButton } = {};
        private letfBtn: fairygui.GButton = null;
        private rightBtn: fairygui.GButton = null;
        private BtnList: fairygui.GList = null;
        private chupaiBtn: fairygui.GButton = null;
        private specialBtn: fairygui.GButton = null;
        private richardBtn: fairygui.GButton = null;
        private TypeList: fairygui.GList = null;
        private cardlist: fairygui.GList = null;
        private Tip: fairygui.GComponent = null;
        private hardCard_scope: Array<laya.maths.Rectangle> = [];
        //   private maCard: fairygui.GComponent = null;
        private daoshuiimg: fairygui.GImage = null;
        private Cards_scope: Array<laya.maths.Rectangle> = [];
        private Cards_pos: Array<laya.maths.Point> = [];

        private data: any = null;
        private typeKeyList: Array<string> = [];
        private arrangedCardsData: Array<Array<twa.BaseCard>> = [];
        private selectedCardsData: Array<twa.BaseCard> = null;
        private pierCardsIdList: Array<Array<string>> = [];
        private cardIdList: Array<any> = null;
        private nowCardIdList: Array<any> = null;
        private tipsType: any = null;
        private tipsDataNum: any = null;
        private tips13DataList: any = null;
        private tipsDataList: any = null;
        private specialType = null;
        private typeScore = null;
        private isFull = false;
        private hardcardStartIndex: number = null;
        private hardcardEndIndex: number = null;



        onCreated(data: any = null) {
            //  constructor(data: any = null) {
            // console.log(data, "===G562====onCreatea======");
            if (!data) return;
            this.data = data;

            this.typeKeyList = this.data["typesList"]["typeKeyList"];
            this.arrangedCardsData = this.data["typesList"]["arrangedCardsData"];
            // console.log(this.typeKeyList, "======================this.typeKeyList");
            //console.log(this.arrangedCardsData, "=================this.arrangedCardsData");
            this.cardIdList = this.data["cardIdList"];
            this.nowCardIdList = this.cardIdList.concat();
            //  console.log(this.nowCardIdList, "==2222222222this.nowCardIdList");
            this.specialType = this.data["specialType"];
            this.typeScore = this.data["typeScore"];
            this.tips13DataList = this.data["tipsDataList"];
            //  console.log(this.tips13DataList, "==============this.tips13DataList")

            let view = this._view;

            view.center();
            this.Tip = view.getChild("tip").asCom;
            this.chooseClt = view.getController("choose");
            this.Txt_Time_1 = view.getChild("Txt_Time_1").asTextField;
            this.Txt_Time_2 = view.getChild("Txt_Time_2").asTextField;
            this.DeleteBtn = {
                "tou": view.getChild("delecrBtn_tou").asButton,
                "zhong": view.getChild("delecrBtn_zhong").asButton,
                "wei": view.getChild("delecrBtn_wei").asButton
            };
            this.DeleteBtn["tou"].onClick(this, this.OnClearBtn, [1]);
            this.DeleteBtn["zhong"].onClick(this, this.OnClearBtn, [2]);
            this.DeleteBtn["wei"].onClick(this, this.OnClearBtn, [3]);
            // this.letfBtn = view.getChild("leftBtn").asButton;
            //  this.rightBtn = view.getChild("rightBtn").asButton;
            this.BtnList = view.getChild("BtnList").asList;
            this.chupaiBtn = view.getChild("chupaiBtn").asButton;
            // this.chupaiBtn.onClick(this, this.outAutoCards);
            this.chupaiBtn.onClick(this, this.outManualCards);
            this.specialBtn = view.getChild("specialBtn").asButton;
            this.richardBtn = view.getChild("richardBtn").asButton;
            this.TypeList = view.getChild("TypeList").asList;
            this.cardlist = view.getChild("cardlist").asList;
            this.daoshuiimg = view.getChild("daoshuiImg").asImage;
            // this.maCard = view.getChild("ma").asCom;

            let bounds: fairygui.GObject = this.view.getChild("n2");
            let rect = new laya.maths.Rectangle(bounds.x, bounds.y, bounds.actualWidth, bounds.actualHeight);
            //console.log(rect, "=============rect");
            this.richardBtn.onClick(this, this.Richard)
            if (this.Card_Btn == null || this.Card_Btn.length == 0) {
                for (let i = 0; i < 13; i++) {
                    // this.oldCard_btn[i] = this.view.getChild(i.toString()).asButton;
                    this.Card_Btn[i] = this.view.getChild(i.toString()).asButton;
                    this.Cards_scope[i] = this.getCardscope(this.Card_Btn[i]);
                    this.Cards_pos[i] = new laya.maths.Point(this.Card_Btn[i].x, this.Card_Btn[i].y);
                    // this.Card_Btn[i].draggable = true;
                    this.Card_Btn[i].dragBounds = rect;
                    //牌的拖动
                    this.Card_Btn[i].on(fairygui.Events.DRAG_END, this, this.onDragEnd, [this.Card_Btn[i]])

                }

            }
            // this.showma();

            this.showTypesList(this.typeKeyList);
            this.initCardFramesAuto();
            this.The_countdown(this.data["time"]);
            if (parseInt(this.specialType) == -1) {
                this.specialBtn.visible = false;
            }
            else {
                this.specialBtn.visible = true;
                this.specialBtn.getController("type").selectedIndex = parseInt(this.specialType) - 11;
                this.specialBtn.onClick(this, this.showSpecialTips);
                this.showSpecialTip(parseInt(this.specialType));
            }

        }
        moveOneCard(card, pos1, pos2) {
            if (!this.isFull)
                return;
            // console.log(card, pos1, pos2, "============换位");
            let startpos = FairyguiTools.rootToLocal(card, { x: pos2.x, y: pos2.y });
            let endpos = FairyguiTools.rootToLocal(card, { x: pos1.x, y: pos1.y });
            let trans = card.getTransition("Ani");
            trans.setValue("startpos", startpos.x, startpos.y);
            trans.setValue("endpos", endpos.x, endpos.y);
            let cb1 = () => {
                card.getChild('carsloader').setXY(0, 0);
                card.setXY(pos1.x, pos1.y);

            };
            trans.play(Handler.create(this, cb1, [], true));

        }
        onDragEnd(CardBtn: fairygui.GButton) {
            if (!this.isFull)
                return;

            var mousePos = this.getMousePos()
            var endcard: fairygui.GButton = null;
            let startindex = this.Card_Btn.indexOf(CardBtn);
            let endindex;

            for (var i = 0; i < this.Cards_scope.length; i++) {
                if (this.Cards_scope[i].contains(mousePos.x, mousePos.y)) {
                    // console.log('MouseEndPos contains ', i);
                    if (endcard != null) {
                        endcard = null;
                        break;
                    }
                    endcard = this.Card_Btn[i];
                    endindex = i;
                }
            }
            if (endcard != null) {
                // let CardBtn_Cards_scope = this.Cards_scope[startindex];
                //  let endcard_Cards_scope = this.Cards_scope[endindex];
                //把点击的牌层级设置到最高
                this.view.setChildIndex(CardBtn, this.view.numChildren - 1);
                //   let name_1 = CardBtn.name;
                // let name_2 = endcard.name;
                let startpos1 = FairyguiTools.rootToLocal(CardBtn, { x: this.Cards_pos[startindex].x, y: this.Cards_pos[startindex].y })
                let endpos1 = FairyguiTools.rootToLocal(CardBtn, { x: this.Cards_pos[endindex].x, y: this.Cards_pos[endindex].y })

                let startpos2 = FairyguiTools.rootToLocal(endcard, { x: this.Cards_pos[endindex].x, y: this.Cards_pos[endindex].y })
                let endpos2 = FairyguiTools.rootToLocal(endcard, { x: this.Cards_pos[startindex].x, y: this.Cards_pos[startindex].y })

                let trans_1 = CardBtn.getTransition("Ani");
                let trans_2 = endcard.getTransition("Ani");

                trans_1.setValue("startpos", startpos1.x, startpos1.y);
                trans_1.setValue("endpos", endpos1.x, endpos1.y);
                trans_2.setValue("startpos", startpos2.x, startpos2.y);
                trans_2.setValue("endpos", endpos2.x, endpos2.y);
                let cb1 = () => {
                    CardBtn.getChild('carsloader').setXY(0, 0);
                    CardBtn.setXY(this.Cards_pos[endindex].x, this.Cards_pos[endindex].y);
                };
                let cb2 = () => {
                    endcard.getChild('carsloader').setXY(0, 0);
                    endcard.setXY(this.Cards_pos[startindex].x, this.Cards_pos[startindex].y);
                };
                trans_1.play(Handler.create(this, cb1, [], true));
                trans_2.play(Handler.create(this, cb2, [], true));
                this.Card_Btn[startindex] = endcard;
                this.Card_Btn[endindex] = CardBtn;
                // CardBtn.name = name_2;
                //  endcard.name = name_1;
                //   console.log(CardBtn.x, CardBtn.y, "=========被拖拽的物体");
                //  console.log(endcard.x, endcard.y, "=========拖拽到的位置");
                //换完牌之后的算法
                this.changeCard(startindex, endindex);
            }
            else {
                CardBtn.setXY(this.Cards_pos[startindex].x, this.Cards_pos[startindex].y);
            }

        }
        changeCard(startindex: number, endindex: number) {
            //  console.log(this.pierCardsIdList, "this.pierCardsIdList");
            let List = this.pierCardsIdList[0].concat(this.pierCardsIdList[1]).concat(this.pierCardsIdList[2]);
            // console.log(List, "===============list");
            let startCardId = List[startindex];
            List[startindex] = List[endindex];
            List[endindex] = startCardId;
            for (let i = 0; i < 3; i++) {
                this.pierCardsIdList[0][i] = List[i];
            }
            for (let i = 0; i < 5; i++) {
                this.pierCardsIdList[1][i] = List[i + 3];
                this.pierCardsIdList[2][i] = List[i + 8];
            }
            //  console.log(this.pierCardsIdList, "==========拖拽完之后 的牌列表");
        }

        //自动选牌按钮列表
        showTypesList(list: Array<string>) {
            for (var i = this.BtnList.numChildren; i > 0; i--) {
                this.BtnList.removeChildToPoolAt(i - 1);
            }
            for (var i = 0; i < list.length; i++) {
                var _typeKey = list[i];
                var _typesList = _typeKey.split("-");
                var ItemBtn = this.BtnList.addItemFromPool();
                ItemBtn.asButton.getChild("title_1").asCom.getController("type").selectedIndex = parseInt(_typesList[0]);
                ItemBtn.asButton.getChild("title_2").asCom.getController("type").selectedIndex = parseInt(_typesList[1]);
                ItemBtn.asButton.getChild("title_3").asCom.getController("type").selectedIndex = parseInt(_typesList[2]);
                ItemBtn.onClick(this, this.OnItemBtn, [_typeKey, i]);
            }
        }

        OnItemBtn(_typeKey: string, index: number) {
            SoundMgrShiSanShui.click();
            this.selectedCardsData = this.arrangedCardsData[_typeKey];
            for (let i = 0; i < this.BtnList.numChildren; i++) {
                if (i == index)
                    this.BtnList.getChildAt(i).asButton.getController("isshow").selectedIndex = 1;
                else
                    this.BtnList.getChildAt(i).asButton.getController("isshow").selectedIndex = 0;
            }
            if (this.isFull) {
                let List = this.arrangedCardsData[_typeKey];
                let cardList_0 = List[0].getCardIdList();
                let cardList_1 = List[1].getCardIdList();
                let cardList_2 = List[2].getCardIdList();
                let idList = cardList_0.concat(cardList_1).concat(cardList_2);

                let contrastIdList: Array<any> = this.pierCardsIdList[0].concat(this.pierCardsIdList[1]).concat(this.pierCardsIdList[2]);
                //  console.log(contrastIdList, "==============要排序的列表");
                // console.log(idList, "==============要变成的表");
                let removebtn = [];
                let removeindex = [];
                for (let i = 0; i < idList.length; i++) {
                    let id = idList[i];

                    let contrastIdx = contrastIdList.indexOf(id);
                    //  console.log(contrastIdx, "=====contrastIdx");
                    if (contrastIdx != -1) {
                        contrastIdList[contrastIdx] = 0;
                        removebtn.push(this.Card_Btn[contrastIdx]);
                        removeindex.push(contrastIdx);
                        // console.log(contrastIdx, i, "============");

                        this.moveOneCard(this.Card_Btn[contrastIdx], this.Cards_pos[i], this.Cards_pos[contrastIdx]);
                    }
                    // this.Card_Btn[contrastIdx] = this.Card_Btn[i];
                }
                // console.log(removebtn, "===========removebtn");
                // console.log(removeindex, "==========removeindex");
                for (let i = 0; i < removebtn.length; i++) {
                    this.Card_Btn[i] = removebtn[i];
                }
                // console.log(this.Card_Btn, "=============牌列表");
                this.pierCardsIdList[0] = cardList_0;
                this.pierCardsIdList[1] = cardList_1;
                this.pierCardsIdList[2] = cardList_2;
                // console.log(this.pierCardsIdList[0], this.pierCardsIdList[1], this.pierCardsIdList[2], "==========当前出牌列表");
            }
            else {
                this.OnItemBtnInit(_typeKey, index);
            }

        }
        OnItemBtnInit(_typeKey: string, index: number) {
            for (let num = 0; num < this.Card_Btn.length; num++) {
                this.Card_Btn[num].getChild("carsloader").asLoader.url = null;
            }
            this.selectedCardsData = this.arrangedCardsData[_typeKey];
            // console.log(index, "============index");
            for (let i = 0; i < this.BtnList.numChildren; i++) {
                if (i == index)
                    this.BtnList.getChildAt(index).asButton.getController("isshow").selectedIndex = 1;
                else
                    this.BtnList.getChildAt(i).asButton.getController("isshow").selectedIndex = 0;
            }
            let List = this.arrangedCardsData[_typeKey]
            let cardList_1 = List[0].getCardIdList()
            let cardList_2 = List[1].getCardIdList()
            let cardList_3 = List[2].getCardIdList()
            for (let i = 0; i < 3; i++) {
                this.pierCardsIdList[0][i] = cardList_1[i];
                let carduiname = "card_" + cardList_1[i].toString();
                this.Card_Btn[i].getChild("carsloader").asLoader.url = twa.UI_CARD[carduiname];
                this.Card_Btn[i].draggable = true;
            }
            for (let j = 0; j < 5; j++) {
                this.pierCardsIdList[1][j] = cardList_2[j];
                this.pierCardsIdList[2][j] = cardList_3[j];
                let carduiname_1 = "card_" + cardList_2[j].toString();
                let carduiname_2 = "card_" + cardList_3[j].toString();
                this.Card_Btn[3 + j].getChild("carsloader").asLoader.url = twa.UI_CARD[carduiname_1];
                this.Card_Btn[8 + j].getChild("carsloader").asLoader.url = twa.UI_CARD[carduiname_2];
                this.Card_Btn[3 + j].draggable = true;
                this.Card_Btn[8 + j].draggable = true;
            }
            // console.log(this.pierCardsIdList[0], this.pierCardsIdList[1], this.pierCardsIdList[2], "=======初始化===当前出牌列表");
            this.isFull = true;
        }
        //初始化牌阵
        initCardFramesAuto() {
            this.pierCardsIdList[0] = [];
            this.pierCardsIdList[1] = [];
            this.pierCardsIdList[2] = [];
            this.chooseClt.selectedIndex = 0;
            this.selectedCardsData = null;
            this.richardBtn.getController("type").selectedIndex = 1;
            //取第一个
            this.OnItemBtnInit(this.typeKeyList[0], 0);
        }
        showSpecialTips() {
            NetHandlerMgr.netHandler.sendArrangedCards([], [this.specialType]);
            this.hide();
        }
        //切换
        Richard() {
            // console.log(this.chooseClt.selectedIndex, "==============选择控制器");
            if (this.chooseClt.selectedIndex == 0) {
                this.chooseClt.selectedIndex = 1;
                this.richardBtn.getController("type").selectedIndex = 0;
                this.initCardFramesManual();
                this.chupaiBtn.visible = false;
            }
            else if (this.chooseClt.selectedIndex == 1) {
                this.chooseClt.selectedIndex = 0;
                this.richardBtn.getController("type").selectedIndex = 1;
                this.initCardFramesAuto();
                this.chupaiBtn.visible = true;

            }
        }
        //倒计时
        The_countdown(time: number) {
            // console.log("==========倒计时==========")
            var num = 10;
            if (time != null)
                num = time;
            // num = num - 1;//先暂时这样改
            let CountDown = () => {
                // this.Txt_Time.text = (num - 1).toString()
                if (num / 10 == 0) {
                    this.Txt_Time_2.text = num.toString();
                    this.Txt_Time_1.text = null;
                }
                else {
                    this.Txt_Time_1.text = Math.floor((num / 10)).toString();
                    this.Txt_Time_2.text = Math.floor(num % 10).toString();
                }
                // SoundMgrShiSanShui.time();
                if (num == 0) {
                    {
                        Laya.timer.clear(this, CountDown)
                        //  console.log("----222222-----关闭理牌面板");
                        this.hide();
                    }

                }
                num = num - 1;
            }
            CountDown();
            Laya.timer.loop(1000, this, CountDown);
        }
        OnClearBtn(type: number) {
            //  console.log(type, this.pierCardsIdList, "=======清空按钮=======");
            if (type == 1) {
                for (let i = 0; i < 3; i++) {
                    this.Card_Btn[i].getChild("carsloader").asLoader.url = null;
                }
            }
            else if (type == 2) {
                for (let i = 0; i < 5; i++) {
                    this.Card_Btn[i + 3].getChild("carsloader").asLoader.url = null;
                }
            }
            else if (type == 3) {
                for (let i = 0; i < 5; i++) {
                    this.Card_Btn[i + 8].getChild("carsloader").asLoader.url = null;
                }
            }
            if (this.pierCardsIdList[type - 1] != null && this.pierCardsIdList[type - 1].length > 0) {
                for (let i = 0; i < this.pierCardsIdList[type - 1].length; i++) {
                    this.nowCardIdList.push(this.pierCardsIdList[type - 1][i]);
                }
                this.pierCardsIdList[type - 1] = [];
                this.refreshCard();
            }
        }

        getCardscope(card) {
            return card.localToGlobalRect(0, 0, card.actualWidth, card.actualHeight);
        }
        getMousePos() {
            //屏幕坐标
            let pos = new laya.maths.Point();
            pos.x = laya.events.MouseManager.instance.mouseX;
            pos.y = laya.events.MouseManager.instance.mouseY;
            return pos;
        }
        dealCard(type: number) {
            let addCardList: Array<any> = [];
            for (let i = this.cardlist.numChildren - 1; i >= 0; i--) {
                let card = this.cardlist.getChildAt(i).asCom;
                if (card.getController("button").selectedIndex == 1) {
                    addCardList.push(card.name)
                    //  this.cardlist.removeChildToPoolAt(i);
                }
            }
            if (addCardList.length == 0 || addCardList == null)
                return;
            // console.log(addCardList, "+++++++++++++addCardList");
            let Maxnum = 0;
            let isPour = false;
            // console.log(type, "==============type");
            if (type == 0) {
                if (addCardList.length <= 3) {
                    this.Removehardcard(addCardList);
                    Maxnum = 3;
                    isPour = true;
                }
            }
            else if (type == 1) {
                if (addCardList.length <= 5) {
                    this.Removehardcard(addCardList);
                    Maxnum = 5
                    isPour = true;
                }
            }
            else {
                if (addCardList.length <= 5) {
                    this.Removehardcard(addCardList);
                    Maxnum = 5
                    isPour = true;
                }
            }
            if (isPour) {
                if (this.pierCardsIdList[type].length >= 0) {
                    if (Maxnum - this.pierCardsIdList[type].length >= addCardList.length) {
                        for (let i = 0; i < addCardList.length; i++) {
                            this.pierCardsIdList[type].push(addCardList[i]);
                        }
                    }
                    else {
                        for (let i = 0; i < this.pierCardsIdList[type].length; i++) {
                            this.nowCardIdList.push(this.pierCardsIdList[type][i]);
                        }
                        this.pierCardsIdList[type] = [];
                        for (let i = 0; i < addCardList.length; i++) {
                            this.pierCardsIdList[type][i] = addCardList[i];
                        }
                    }
                }
                else {
                    for (let i = 0; i < addCardList.length; i++) {
                        this.pierCardsIdList[type][i] = addCardList[i];
                    }
                }

                this.pierCardsIdList[type].sort(twa.utils.sortCardFunc);
                //  console.log(type, this.pierCardsIdList[type], "==============");
                for (let i = 0; i < this.pierCardsIdList[type].length; i++) {
                    let cardname = "card_" + this.pierCardsIdList[type][i];
                    // console.log(cardname, "+++++++++++++++++++");
                    if (type == 0) {
                        this.Card_Btn[i].getChild("carsloader").asLoader.url = twa.UI_CARD[cardname];
                    }
                    else if (type == 1) {
                        this.Card_Btn[i + 3].getChild("carsloader").asLoader.url = twa.UI_CARD[cardname];
                    } else if (type == 2) {
                        this.Card_Btn[i + 8].getChild("carsloader").asLoader.url = twa.UI_CARD[cardname];
                    }
                }
                if (this.pierCardsIdList[0].length == 0 && this.pierCardsIdList[1].length == 5 && this.pierCardsIdList[2].length == 5)
                    this.addCardsToPier();
                this.refreshCard();
            }

        }
        Removehardcard(addCardList: Array<any>) {
            //  console.log(this.nowCardIdList, "====11111111 this.nowCardIdList");
            let num_cards = this.nowCardIdList.length;
            let isbreak = false;
            for (let i = 0; i < addCardList.length; i++) {
                for (let n = this.nowCardIdList.length - 1; n >= 0; n--) {
                    if (this.nowCardIdList[n] == addCardList[i]) {
                        this.nowCardIdList.splice(n, 1);
                        if (i == addCardList.length - 1 || num_cards == this.nowCardIdList.length - addCardList.length)
                            isbreak = true;
                    }
                }
                if (isbreak) {

                    return;
                }

            }
        }
        refreshCard() {
            //排序
            this.nowCardIdList.sort(twa.utils.sortCardFunc);
            // console.log(this.nowCardIdList, "===============this.nowCardIdList");
            //  console.log(this.cardlist.numChildren, "==================this.cardlist.numChildren");
            if (this.nowCardIdList.length > this.cardlist.numChildren) {
                for (let i = this.cardlist.numChildren; i <= this.nowCardIdList.length - 1; i++) {
                    this.cardlist.addItemFromPool();
                }
            }
            else if (this.nowCardIdList.length < this.cardlist.numChildren) {
                for (let i = this.cardlist.numChildren - 1; i >= this.nowCardIdList.length; i--) {
                    this.cardlist.removeChildToPoolAt(i);
                }
            }
            // console.log(this.cardlist.numChildren, "========111111111==========this.cardlist.numChildren");
            for (let i = 0; i < this.cardlist.numChildren; i++) {
                let card = this.cardlist.getChildAt(i);
                let carduiname = "card_" + this.nowCardIdList[i].toString();
                card.asCom.getChild("n0").asLoader.url = twa.UI_CARD[carduiname];
                card.name = this.nowCardIdList[i];
                // card.on(Laya.Event., this, this.Up, [card]);
                card.asCom.getController("button").selectedIndex = 0;
            }
            this.updateTips();
        }
        /* Up(card: fairygui.GComponent) {
             console.log("==========up");
             let ctl = card.asCom.getController("button").selectedIndex;
             if (ctl == 1) {
                 ctl = 0;
             } else if (ctl == 0) {
                 ctl = 1;
             }
             // console.log(ctl, "此时牌的状态");
         }*/

        OnMouseMove(Card: fairygui.GComponent) {
            // console.log(Card.name, "------OnCardMove-------");
            if (Card.getController("color").selectedIndex == 0 && this.hardcardStartIndex != null)
                Card.getController("color").selectedIndex = 1;
            if (this.hardcardStartIndex != null) {
                this.hardcardEndIndex = this.cardlist.getChildIndex(Card);
            }
        }
        onMouseDown(Card: fairygui.GComponent) {
            //  console.log(Card.name, "------onCardDown-------");
            if (this.hardcardStartIndex == null) {
                this.hardcardStartIndex = this.cardlist.getChildIndex(Card);
            }
        }
        onMousedUp(Card: fairygui.GComponent) {
            //  console.log(Card.name, "-----onCardUp------");
            this.hardcardEndIndex = this.cardlist.getChildIndex(Card);
            // console.log(this.hardcardEndIndex, "============this.hardcardEndIndex");
            //console.log(this.hardcardStartIndex, "===========this.hardcardStartIndex");
            this.oncardsUPorDown();
        }
        oncardsUPorDown() {
            if (this.hardcardEndIndex != null && this.hardcardStartIndex != null) {
                if (this.hardcardEndIndex > this.hardcardStartIndex) {
                    for (let i = this.hardcardStartIndex; i <= this.hardcardEndIndex; i++) {
                        let ItemCard = this.cardlist.getChildAt(i).asCom;
                        if (ItemCard.getController("button").selectedIndex == 0)
                            ItemCard.getController("button").selectedIndex = 1;
                        else
                            ItemCard.getController("button").selectedIndex = 0;
                        //ItemCard.getController("color").selectedIndex = 1;
                    }
                }
                else if (this.hardcardEndIndex < this.hardcardStartIndex) {
                    for (let i = this.hardcardStartIndex; i >= this.hardcardEndIndex; i--) {
                        let ItemCard = this.cardlist.getChildAt(i).asCom;
                        if (ItemCard.getController("button").selectedIndex == 0)
                            ItemCard.getController("button").selectedIndex = 1;
                        else
                            ItemCard.getController("button").selectedIndex = 0;
                        // ItemCard.getController("color").selectedIndex = 1;
                    }
                }
                else if (this.hardcardEndIndex == this.hardcardStartIndex) {
                    let ctl = this.cardlist.getChildAt(this.hardcardEndIndex).asCom.getController("button").selectedIndex;
                    if (ctl == 1) {
                        ctl = 0;
                    } else if (ctl == 0) {
                        ctl = 1;
                    }
                }
                for (let i = 0; i < this.cardlist.numChildren; i++) {
                    let ItemCard = this.cardlist.getChildAt(i).asButton;
                    ItemCard.getController("color").selectedIndex = 0;
                }
            }
            this.hardcardStartIndex = null;
            this.hardcardEndIndex = null;
        }
        state_moveUp() {
            //console.log("鼠标up事件");
            this.oncardsUPorDown();
        }
        initHardCardsScope() {
            //  this.cardlist.on(Laya.Event.MOUSE_DOWN, this, this.OnListDrag)
            this.hardcardStartIndex = null;
            this.hardcardEndIndex = null;
            this.hardCard_scope = [];
            for (let i = 0; i < this.cardlist.numChildren; i++) {
                let card = this.cardlist.getChildAt(i);
                this.hardCard_scope[i] = this.getCardscope(card);
                card.on(Laya.Event.MOUSE_MOVE, this, this.OnMouseMove, [card]);
                card.on(Laya.Event.MOUSE_DOWN, this, this.onMouseDown, [card]);
                card.on(Laya.Event.MOUSE_UP, this, this.onMousedUp, [card]);
            }
            Laya.stage.on(Laya.Event.MOUSE_UP, this, this.state_moveUp);
        }
        initCardFramesManual() {
            this.chooseClt.selectedIndex = 1;
            this.pierCardsIdList[0] = [];
            this.pierCardsIdList[1] = [];
            this.pierCardsIdList[2] = [];
            this.cardlist.removeChildrenToPool();


            for (let i = 0; i < this.Card_Btn.length; i++)
                this.Card_Btn[i].draggable = false;

            for (let n = 0; n < 13; n++) {
                let type;
                if (n < 3) {
                    type = 0;
                }
                else if (n >= 3 && n < 8) {
                    type = 1;
                }
                else
                    type = 2;
                this.Card_Btn[n].onClick(this, this.dealCard, [type]);
            }
            for (let num = 0; num < this.Card_Btn.length; num++) {
                this.Card_Btn[num].getChild("carsloader").asLoader.url = null;
            }
            // console.log(this.cardIdList, "===============牌");
            for (let i = 0; i < this.cardIdList.length; i++) {
                var card = this.cardlist.addItemFromPool();
                let carduiname = "card_" + this.cardIdList[i].toString();
                card.asCom.getChild("n0").asLoader.url = twa.UI_CARD[carduiname];
                card.name = this.cardIdList[i];
                card.asButton.getController("button").selectedIndex = 0;
                // card.onClick(this, this.Up, [card]);
            }
            this.selectedCardsData = null;
            this.initTips();
            this.initHardCardsScope();
        }
        initTips() {
            this.tipsType = 0;
            this.tipsDataNum = 0;
            this.tipsDataList = this.tips13DataList;
            let num = this.TypeList.numChildren;
            let typeNumList = [1, 2, 3, 5, 6, 7, 8, 9, 10];
            for (let i = 0; i < num; i++) {
                var type = typeNumList[i];
                var tipsData = this.tipsDataList[type];
                var btn = this.TypeList.getChildAt(i);
                if (tipsData == null || tipsData.length == 0) {
                    btn.enabled = false;
                }
                else {
                    btn.enabled = true;
                    btn.onClick(this, this.onTip, [type]);
                }
            }
        }
        onTip(type) {
            this.cardDown();
            var tipsData = this.tipsDataList[type];
            // console.log(tipsData, "==============tipsData");
            if (this.tipsType != type) {
                this.tipsType = type;
                this.tipsDataNum = 0;
            }
            else {
                this.tipsDataNum++;
            }
            if (this.tipsDataNum >= tipsData.length)
                this.tipsDataNum = 0;
            var tipCards = tipsData[this.tipsDataNum].concat();
            var isbreak = false;
            let num = 0;
            // console.log(tipCards, "=========tipCards");
            let index = null;
            for (let i = 0; i < tipCards.length; i++) {
                for (let j = 0; j < this.cardlist.numChildren; j++) {
                    // console.log(index, "=======index")
                    if (this.cardlist.getChildAt(j).name == tipCards[i] && this.cardlist.getChildAt(j).asCom.getController("button").selectedIndex == 0) {
                        //index = i;
                        this.cardlist.getChildAt(j).asCom.getController("button").selectedIndex = 1;
                        // num++;
                        // tipCards.splice(i, 1);
                        //if (i == 0 || num == tipCards.length - 1) {
                        //    isbreak = true;
                        //}
                        break;
                    }
                    //if (isbreak) {
                    //break;
                    // }
                }
            }
        }

        updateTips() {
            this.tipsDataNum = 0;
            if (this.nowCardIdList.length == 13) {
                this.tipsDataList = this.tips13DataList;
            }
            else if (this.nowCardIdList.length == 0) {
                this.tipsDataList = {};
            }
            else {
                this.tipsDataList = twa.utils.getTipsDataList(this.nowCardIdList);
            }
            let typeNumList = [1, 2, 3, 5, 6, 7, 8, 9, 10];
            // let isTipnull = true;
            for (let i = 0; i < 9; i++) {
                var type = typeNumList[i];
                var tipsData = this.tipsDataList[type];
                var btn = this.TypeList.getChildAt(i);
                if (tipsData == null || tipsData.length == 0) {
                    btn.enabled = false;
                }
                else {
                    //  isTipnull = false;
                    btn.enabled = true;
                    btn.onClick(this, this.onTip, [type]);
                }
            }
            if (this.pierCardsIdList[0].length == 3 && this.pierCardsIdList[1].length == 5 && this.pierCardsIdList[2].length == 5) {
                this.isFull = true;
                for (let i = 0; i < this.Card_Btn.length; i++)
                    this.Card_Btn[i].draggable = true;
            }
            else {
                this.isFull = false;
                for (let i = 0; i < this.Card_Btn.length; i++)
                    this.Card_Btn[i].draggable = false;
                // if (isTipnull) {
                //自动加牌
                //  this.addCardsToPier();
                // }
            }
            if (this.isFull) {
                this.chupaiBtn.visible = true;
            }
            else {
                this.chupaiBtn.visible = false;
            }
        }
        addCardsToPier() {
            this.nowCardIdList.sort(twa.utils.sortCardFunc)
            for (let i = 0; i < this.nowCardIdList.length; i++) {
                this.pierCardsIdList[0].push(this.nowCardIdList[i]);
                let cardname = "card_" + this.nowCardIdList[i].toString();
                this.Card_Btn[i].getChild("carsloader").asLoader.url = twa.UI_CARD[cardname];
            }
            this.nowCardIdList = [];
        }
        cardDown() {
            for (let i = 0; i < this.cardlist.numChildren; i++) {
                this.cardlist.getChildAt(i).asCom.getController("button").selectedIndex = 0;
            }
        }
        showSpecialTip(Type: number) {
            this.Tip.visible = true;
            let index = this.view.getChildIndex(this.Tip);
            this.Tip.getController("type").selectedIndex = Type - 11;
            this.view.setChildIndex(this.Tip, this.view.numChildren - 1)
            this.Tip.getChild("no").asButton.onClick(this, function () {
                this.view.setChildIndex(this.Tip, index);
                this.Tip.visible = false;
            });
            this.Tip.getChild("yes").asButton.onClick(this, function () {
                this.view.setChildIndex(this.Tip, index);
                this.Tip.visible = false;
                this.showSpecialTips();
            });
        }

        /* outAutoCards() {
             //console.log("222222222发送出牌事件");
             if (this.chooseClt.selectedIndex == 1)
                 return;
             if (this.selectedCardsData == null)
                 return;
             console.log("------------outAutoCards---------");
             let isPour = !(this.selectedCardsData[2].greaterThan(this.selectedCardsData[1]) && this.selectedCardsData[1].greaterThan(this.selectedCardsData[0]));
             if (isPour) {
                 //倒水动画
                 console.log("2222222222显示倒水动画");
                 this.daoshuiimg.visible = true;
                 let index = this.view.getChildIndex(this.daoshuiimg);
                 this.view.setChildIndex(this.daoshuiimg, this.view.numChildren - 1)
                 this.view.getTransition("daoshui").play(new Handler(this, function () {
                     this.daoshuiimg.visible = false;
                     this.view.setChildIndex(this.daoshuiimg, index)
                 }))
                 return;
             }
             let cardList = [
                 this.selectedCardsData[0].getCardIdList().join(","),
                 this.selectedCardsData[1].getCardIdList().join(","),
                 this.selectedCardsData[2].getCardIdList().join(",")
             ];
             var typeList = [this.selectedCardsData[0].getType(), this.selectedCardsData[1].getType(), this.selectedCardsData[2].getType()];
             NetHandlerMgr.netHandler.sendArrangedCards(cardList, typeList);
             this.hide();
         }*/
        outManualCards() {
            //console.log("1111111111发送出牌事件");
            // if (this.chooseClt.selectedIndex == 0)
            //  return;
            if (!this.isFull)
                return;
            // console.log("---------outManualCards-------");
            var selectedCardsPattern1 = twa.utils.getCardPattern(this.pierCardsIdList[0].sort(twa.utils.sortCardFunc), 1);
            var selectedCardsPattern2 = twa.utils.getCardPattern(this.pierCardsIdList[1].sort(twa.utils.sortCardFunc), 2);
            var selectedCardsPattern3 = twa.utils.getCardPattern(this.pierCardsIdList[2].sort(twa.utils.sortCardFunc), 3);
            //console.log(this.pierCardsIdList[0], this.pierCardsIdList[1], this.pierCardsIdList[2], "========发送给服务器的牌");
            var isPour = !(selectedCardsPattern3.greaterThan(selectedCardsPattern2) && selectedCardsPattern2.greaterThan(selectedCardsPattern1));
            if (isPour) {
                //倒水动画
                //console.log("1111111111显示倒水动画");
                this.daoshuiimg.visible = true;
                let index = this.view.getChildIndex(this.daoshuiimg);
                this.view.setChildIndex(this.daoshuiimg, this.view.numChildren - 1)
                this.view.getTransition("daoshui").play(new Handler(this, function () {
                    this.daoshuiimg.visible = false;
                    this.view.setChildIndex(this.daoshuiimg, index)
                }))

                return;
            }
            var cardList = [
                selectedCardsPattern1.getCardIdList().join(","),
                selectedCardsPattern2.getCardIdList().join(","),
                selectedCardsPattern3.getCardIdList().join(",")
            ];
            var typeList = [
                selectedCardsPattern1.getType(),
                selectedCardsPattern2.getType(),
                selectedCardsPattern3.getType()
            ];
            //  console.log(cardList, "===========cardList");
            //  console.log(typeList, "=============typeList");
            NetHandlerMgr.netHandler.sendArrangedCards(cardList, typeList);
            this.hide();
        }
        hide() {

            for (let i = 0; i < this.Card_Btn.length; i++) {
                this.Card_Btn[i].mode = -1;
            }
            Laya.timer.clearAll(this);
            super.hide();
        }
    }
}