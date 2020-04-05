module G562 {
    export class G562Balance extends Page {
        constructor() {
            super("G562", "balance", UILayer.GAME)
            // this.addRelation(fairygui.RelationType.Center_Center);
            this.keepCenter();
        }
        private resultsCtl: fairygui.Controller = null;
        private List: fairygui.GList = null;
        private closeBtn: fairygui.GButton = null;
        private setUserDatas: Array<any> = null;
        onCreated(data: any = null) {
            // console.log(data, "===========G562Balance");
            if (!data) return;
            this.setUserDatas = data;
            let view = this._view;
            this.resultsCtl = view.getController("results");
            this.closeBtn = view.getChild("closeBtn").asButton;
            this.closeBtn.onClick(this, this.hide);
            this.List = view.getChild("List").asList;
            view.center();
            this.onShow();
        }
        onShow() {
            this.resultsCtl.selectedIndex = 2;
            for (let i = this.List.numChildren - 1; i >= 0; i--) {
                this.List.removeChildToPoolAt(i);
            }
            for (let i = 0; i < this.setUserDatas.length; i++) {
                let Item = this.List.addItemFromPool().asCom;
                Item.getChild("Loader_Avatar").asCom.getChild("n2").asLoader.url = this.setUserDatas[i]['headImgUrl'];
                if (i == 0)
                    Tools.inst.setNickname(Item.getChild("Loader_Avatar").asCom.getChild("n4").asTextField.text, this.setUserDatas[i]["nickname"]);
                else
                    Tools.inst.setNickname(Item.getChild('Loader_Avatar').asCom.getChild('n4').asTextField.text, Tools.inst.maskUserName(this.setUserDatas[i]["nickname"]));
                //console.log(this.setUserDatas[i]["score"], "===========this.setUserDatas[i]score");
                // console.log(Tools.inst.TableParseFloat(this.setUserDatas[i]["score"]), "=========");

                if (0 == this.setUserDatas["G562page"].getLocalPos(this.setUserDatas[i]["side"])) {
                    this.view.getController("results").selectedIndex = this.setUserDatas[i]["score"] >= 0 ? 0 : 1;
                }
                let score = Tools.inst.TableParseFloat(this.setUserDatas[i]["score"]);
                if (score >= 0) {
                    Item.getChild("Txt_total_score_win").visible = true;
                    Item.getChild("Txt_total_score_lose").visible = false;
                    Item.getChild("Txt_total_score_win").asTextField.text = score.toString();
                }
                else {
                    Item.getChild("Txt_total_score_lose").visible = true;
                    Item.getChild("Txt_total_score_win").visible = false;
                    Item.getChild("Txt_total_score_lose").asTextField.text = score.toString();
                }
                Item.getChild("Txt_qiang").asTextField.text = this.setUserDatas[i]["descs"][1];
                Item.getChild("Txt_zhongqiang").asTextField.text = this.setUserDatas[i]["descs"][2];

                let type = this.setUserDatas[i]["times"];
                let cards: Array<string> = this.setUserDatas[i]['cards'];
                let extend = this.setUserDatas[i]["extend"];
                /*  let horseCardFrame = Item.getChild("ma").asCom.getChild("n0").asCom.getChild("n0").asLoader;
                  if (cgb.config.isHorsePlay) {
                      let name = "card_" + cgb.config.horseCardId.toString()
                      let horseCardImg = twa.UI_CARD[name];
                      horseCardFrame.url = horseCardImg;
                  }
                  else {
                      Item.getChild("ma").asCom.visible = false;
                  }
                  Item.getChild("ma").asCom.visible = false;
                  let isshowMa = false;*/
                if (cards.length == 3) {
                    Item.getController("Type").selectedIndex = 0;
                    for (let s = 0; s < cards.length; s++) {
                        let list = cards[s].split(",");
                        let obj = Item.getChild(s + "_list").asList;
                        Item.getChild(s + "_score").asTextField.text = Tools.inst.TableParseFloat(extend[s]).toString();
                        Item.getChild("Type_" + s).asCom.getController("type").selectedIndex = type[s];
                        if (obj.numChildren > 0) {
                            for (let i = obj.numChildren - 1; i >= 0; i--) {
                                obj.removeChildAt(i);
                            }
                        }
                        for (let j = 0; j < list.length; j++) {
                            let carduiname = "card_" + list[j].toString();
                            let card = obj.addItemFromPool();
                            card.asCom.getChild("n0").asLoader.url = twa.UI_CARD[carduiname];
                            // obj.getChildAt(j).asCom.getChild("n0").asLoader.url = twa.UI_CARD[carduiname];
                            // if (list[j] == cgb.config.horseCardId && isshowMa == false) {
                            // isshowMa = true;
                            // }
                        }
                    }
                }
                else {
                    Item.getController("Type").selectedIndex = 1;
                    let list = cards[0].split(",");
                    let obj = Item.getChild("spiceList").asList;
                    Item.getChild("spice_score").asTextField.text = Tools.inst.TableParseFloat(extend[0]).toString();
                    // Item.getChild(type[0].toString()).asImage.visible = true;
                    Item.getController("spType").selectedIndex = type[0] - 11;
                    if (obj.numChildren > 0) {
                        for (let i = obj.numChildren - 1; i >= 0; i--) {
                            obj.removeChildAt(i);
                        }
                    }
                    for (let j = 0; j < list.length; j++) {
                        let carduiname = "card_" + list[j].toString();
                        let card = obj.addItemFromPool();
                        card.asCom.getChild("n0").asLoader.url = twa.UI_CARD[carduiname];
                        // obj.getChildAt(j).asCom.getChild("n0").asLoader.url = twa.UI_CARD[carduiname];
                        // if (list[j] == cgb.config.horseCardId && isshowMa == false) {
                        //isshowMa = true;
                        //}

                    }
                }
                // Item.getChild("ma").asCom.visible = this.setUserDatas[i]["descs"][0];;
            }
            console.log(this.view, "=============小结");
        }
        hide() {
            super.hide();
            this.setUserDatas["G562page"].onReset();
        }
    }

}
