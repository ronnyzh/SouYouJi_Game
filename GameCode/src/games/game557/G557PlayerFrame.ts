/*
* name;
*/
class G557PlayerFrame extends GbpPlayerFrame {
    private complete: fairygui.GComponent;
    private completeCt1: fairygui.Controller;

    constructor(components: Object) {
        super(components);
        var component = components['seat'];
        this.complete = components['complete'];
        this.completeCt1 = this.complete.getController('c1');
    }

    showComplete(num: number) {
        this.completeCt1.setSelectedIndex(num);
        this.complete.visible = true;
    }

    hideComplete() {
        this.complete.visible = false;
    }

    resetGame() {
        this.out_pokers.visible = false;
        this.out_nnStr.visible = false;
        this.out_BStr.visible = false;
        this.complete.visible = false;
        this.tfScore.visible = false;
        this.lightkMark.visible = false;
        this.updateBankerState(false);
    }

    setCards(tiles, effectFunc?: (outPokers: fairygui.GList, ...param) => any, ...param) {
        var outPokers = this.out_pokers;
        let action = effectFunc ? effectFunc(outPokers, ...param) : false;
        for (let i = outPokers.numChildren - 1; i >= 0; i--) {
            this.setPoker(outPokers.getChildAt(i).asCom.getChildAt(0), null)
            outPokers.removeChildAt(i);
        }
        this.addCards(tiles, action);
        outPokers.visible = true;
    }

    showBullStr(bullnum: number) {
        SoundMgrPoint.playPointEffect(bullnum, this.sex);
        super.showBullStr(bullnum);
    }

    /**获得当前牌的点数 */
    getHandCardNum() {
        let outPokers = this.out_pokers;
        let num = 0;
        let oneNum = 0;
        let cb = (value) => {
            if (value > 21 && oneNum > 0) {
                value -= 10;
                oneNum--;
                return cb(value);
            } else {
                return value;
            }
        }
        for (let index = 0; index < outPokers.numChildren; index++) {
            let cardId = outPokers.getChildAt(index).data as string;
            if (cardId != '') {
                let temp = cardId.substr(1);
                let tempNum = parseInt(temp) > 10 ? 10 : parseInt(temp);
                if (tempNum != null) {
                    if (tempNum == 1) {
                        num += 11;
                        oneNum++;
                    }
                    else {
                        num += tempNum;
                    }
                    num = cb(num);
                }
            }
        }
        return num;
    }

    setOtherCards() {
        var otherPokers = this.out_pokers;
        // otherPokers.removeChildrenToPool();
        for (let i = otherPokers.numChildren - 1; i >= 0; i--) {
            this.setPoker(otherPokers.getChildAt(i).asCom.getChildAt(0), null)
            otherPokers.removeChildAt(i);
        }
        var pokerComp = otherPokers.addItemFromPool().asCom;
        var poker = pokerComp.getChildAt(0);
        this.setPoker(poker.asLoader, null);
        pokerComp.visible = true;
        otherPokers.visible = true;
    }

    setDrawCard(tiles, action = false) {
        this.addCards(tiles, action);
    }

    public getShowCardNum() {
        let outPokers = this.out_pokers;
        return outPokers.numChildren;
    }

}