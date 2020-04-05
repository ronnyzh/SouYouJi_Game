
//吃碰杠胡
var ACTION_OPTION = {
    NOT_GET: 0, //不要牌
    CHOW: 1, //吃
    PONG: 2, //碰
    OTHERS_KONG: 3, //其他人打出来的杠
    SELF_KONG: 4, //自己摸到的杠
    CONCEALED_KONG: 5,//暗杠
    HU: 6, //胡
    TING: 7//听
};

class OperateArea {

    private showBtnList: fairygui.GList;
    private choiceFrame: fairygui.GComponent;
    private choiceFrameList: fairygui.GList;

    constructor(components: Object) {
        this.showBtnList = components['operatorArea'];
        this.choiceFrame = components['operatorAreaChoice'];
        this.choiceFrameList = this.choiceFrame.getChild('out_meld').asList;
    }

    hide() {
        this.showBtnList.removeChildrenToPool();

        this.choiceFrame.visible = false;
        this.choiceFrameList.removeChildrenToPool();
    }

    show(data, cb: Function = null) {
        // console.log(data, "==========operateAreashow");
        this.showBtnList.removeChildrenToPool();
        var showBtnList = this.showBtnList;
        var onBtnData0 = {
            "type": 0,
            "cb": cb,
            "isNeedChoice": false,
            "choiceList": "",
            "isOriginHu": false
        };
        this.addBtn(onBtnData0);

        var length = data.length;
        for (var i = 0; i < length; i++) {
            var oneData = data[i];
            var choiceList = oneData["choiceList"];
            var isNeedChoice = false;
            if (choiceList.length != 1) {
                isNeedChoice = true;
            }
            var onBtnData = this.createBtnData(oneData, cb);
            var btn = this.addBtn(onBtnData, choiceList);
            // if (isNeedChoice) {
            //     this.addChoiceFrame(choiceList, onBtnData);
            // }
        }

        showBtnList.visible = true;
    }

    addChoiceFrame(data, onBtnData) {
        //console.log('addChoiceFrame==================', data, onBtnData)
        this.choiceFrame.visible = !this.choiceFrame.visible;
        if (this.choiceFrame.visible == false)
            return;
        var cb = onBtnData["cb"];
        var type = onBtnData['type'];
        var choiceFrameList = this.choiceFrameList;
        choiceFrameList.removeChildrenToPool();

        if (type == ACTION_OPTION.SELF_KONG) {
            var dataList = [];
            for (var i = 0; i < data.length; i++) {
                var oneData = data[i];
                dataList.push({ list: ['', '', '', oneData] });
            }
            MahjongMgr.inst.addMeldTiles(choiceFrameList, dataList, true);
            for (var i = 0; i < choiceFrameList.numChildren; ++i) {
                try {
                    let tileComp = choiceFrameList.getChildAt(i).asButton;
                    tileComp.offClick(this, this.clickChoice);
                    tileComp.onClick(this, this.clickChoice, [type, data[i], cb]);
                } catch (error) {
                    console.log(error)
                }
            }
            //  this.choiceFrame.visible = data.length > 0;
            return;
        }
        else if (type == ACTION_OPTION.CHOW) {
            let dataList = [];
            for (let i = 0; i < data.length; i++) {
                let oneData: string = data[i];
                let oneDataList = oneData.split(',');
                oneDataList.sort(G445PlayerFrame.sortTileData);
                dataList.push({ list: oneDataList });
            }
            MahjongMgr.inst.addMeldTiles(choiceFrameList, dataList, true);
            for (var i = 0; i < choiceFrameList.numChildren; ++i) {
                try {
                    let tileComp = choiceFrameList.getChildAt(i).asButton;
                    tileComp.offClick(this, this.clickChoice);
                    tileComp.onClick(this, this.clickChoice, [type, data[i], cb]);
                } catch (error) {
                    console.log(error)
                }
            }
            // this.choiceFrame.visible = data.length > 0;
            return;
        }
        this.clickChoice(type, onBtnData["choiceList"], cb);
    }

    clickChoice(type, value, cb?) {
        if (cb) cb(type, value);
    }

    addBtn(data, choiceList?) {
        //console.log(data, choiceList, "==========添加action按钮");
        var showBtnList = this.showBtnList;
        var comp = showBtnList.addItemFromPool().asCom;

        var types = [0, 1, 2, 3, 3, 3, 4, 6];
        var type = types[data['type']] || 0;
        if (type == 4 && data["isOriginHu"]) type = 5;
        else if (type == 0)
            comp.getTransition('t1').stop();
        comp.getController('Actions').setSelectedIndex(type);
        comp.asButton.offClick(this, this.onBtn);
        comp.asButton.onClick(this, this.onBtn, [data, choiceList]);
    }

    onBtn(data, choiceList) {
        //  console.log(data, choiceList, "=========onBtn");
        var type = data["type"];
        var cb = data["cb"];
        if (type == 7) {
            //console.log(type, data["choiceList"], "==========choiceList");
            cb(type, data["choiceList"]);
            return;
        }
        if (data["isNeedChoice"]) {
            if (data.choiceCTile != null) {
                cb(type, data.choiceCTile.meldList);
            }
            else if (choiceList) {
                this.addChoiceFrame(choiceList, data);
            }
        } else {
            cb(type, data["choiceList"]);
        }
    }

    createBtnData(oneData, cb) {
        var type = oneData["type"];
        var choiceList = oneData["choiceList"];
        var isOriginHu = oneData["isOriginHu"];
        var isNeedChoice = false;
        if (choiceList.length != 1) {
            isNeedChoice = true;
        }

        var onBtnData = {
            "type": type,
            "cb": cb,
            "isNeedChoice": isNeedChoice,
            "choiceList": choiceList[0],
            "isOriginHu": isOriginHu
        };

        return onBtnData;
    }


    reset() {
        this.hide();
    }
}