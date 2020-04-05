module G9999 {
    export class G9999DetailedList {

        private parent: fairygui.GComponent;
        private beadListData: Array<number> = []
        private beadList: fairygui.GList;
        private xianData: number;
        private xianText: fairygui.GLabel;
        private zhuangData: number;
        private zhuangText: fairygui.GLabel;
        private heData: number;
        private heText: fairygui.GLabel;
        private xianDuiData: number;
        private xianDuiText: fairygui.GLabel;
        private zhuangDuiData: number;
        private zhuangDuiText: fairygui.GLabel;
        private baDianData: number;
        private baDianText: fairygui.GLabel;
        private jiuDianData: number;
        private jiuDianText: fairygui.GLabel;


        constructor(comDetailedList: fairygui.GComponent) {
            this.parent = comDetailedList;
            this.beadList = this.parent.getChild('beadlist').asList;
            this.xianText = this.parent.getChild('txtXianValue').asLabel;
            this.zhuangText = this.parent.getChild('txtZhuangValue').asLabel;
            this.heText = this.parent.getChild('txtHeValue').asLabel;
            this.xianDuiText = this.parent.getChild('txtXianDuiZiValue').asLabel;
            this.zhuangDuiText = this.parent.getChild('txtZhuangDuiZiValue').asLabel;
            this.baDianText = this.parent.getChild('txt8DianValue').asLabel;
            this.jiuDianText = this.parent.getChild('txt9DianValue').asLabel;
            this.Xian = 0;
            this.Zhuang = 0;
            this.He = 0;
            this.XianDui = 0;
            this.ZhuangDui = 0;
            this.BaDian = 0;
            this.JiuDian = 0;
        }

        setTextData(data: { xian: number, zhuang: number, he: number, xianDui: number, zhuangDui: number, baDian: number, jiuDian: number }) {
            this.Xian = data.xian;
            this.Zhuang = data.zhuang;
            this.He = data.he;
            this.XianDui = data.xianDui;
            this.ZhuangDui = data.zhuangDui;
            this.BaDian = data.baDian;
            this.JiuDian = data.jiuDian;
        }

        set Xian(value: number) {
            this.xianData = value;
            this.xianText.text = value == null ? '' : value.toString();
        }

        get Xian() {
            return this.xianData;
        }

        set Zhuang(value: number) {
            this.zhuangData = value;
            this.zhuangText.text = value == null ? '' : value.toString();
        }

        get Zhuang() {
            return this.zhuangData;
        }

        set He(value: number) {
            this.heData = value;
            this.heText.text = value == null ? '' : value.toString();
        }

        get He() {
            return this.heData;
        }

        set XianDui(value: number) {
            this.xianDuiData = value;
            this.xianDuiText.text = value == null ? '' : value.toString();
        }

        get XianDui() {
            return this.xianDuiData;
        }

        set ZhuangDui(value: number) {
            this.zhuangDuiData = value;
            this.zhuangDuiText.text = value == null ? '' : value.toString();
        }

        get ZhuangDui() {
            return this.zhuangDuiData;
        }

        set BaDian(value: number) {
            this.baDianData = value;
            this.baDianText.text = value == null ? '' : value.toString();
        }

        get BaDian() {
            return this.baDianData
        }

        set JiuDian(value: number) {
            this.jiuDianData = value;
            this.jiuDianText.text = value == null ? '' : value.toString();
        }

        get JiuDian() {
            return this.jiuDianData;
        }

        addBead(value: number, isPlay: boolean = true, onComplete?: laya.utils.Handler, times?: number, delay?: number) {
            this.beadListData.push(value);
            let item = this.beadList.addItemFromPool().asCom;
            let ctl = item.getController('ctl');
            let cb = () => {
                switch (value.toString()) {
                    case '2':
                        ctl.selectedPage = '闲';
                        this.Xian++;
                        break;
                    case '0':
                        ctl.selectedPage = '和';
                        this.He++;
                        break;
                    case '1':
                        ctl.selectedPage = '庄';
                        this.Zhuang++;
                        break;
                    default:
                        ctl.selectedPage = '无';
                        break;
                }
            }
            if (isPlay) {
                item.getTransition('flicker').setHook('start', Handler.create(this, cb, [], true));
                item.getTransition('flicker').play(onComplete, times, delay);
            }
            else {
                cb();
            }
        }

        resetBead() {
            this.beadListData.splice(0, this.beadListData.length);
            this.beadList.removeChildrenToPool();
        }

        refreshBead(data: Array<number>) {
            this.beadListData.splice(0, this.beadListData.length, ...data);
            this.beadList.removeChildrenToPool();
            this.beadListData.forEach(value => {
                this.addBead(value, false)
            });
        }


    }
}
