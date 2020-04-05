module G9999 {
    export class G9999ChipFrame {
        public static isCanChip: boolean = false;
        
        private chipRect: fairygui.GComponent;
        private chipRectItems: Array<ChipRectItem> = [];

        private chipBtns: Array<fairygui.GButton> = [];

        private chipCtl: fairygui.Controller;
        public chipItemMgr: ChipItemMgr;

        private goldLight: fairygui.GMovieClip;
        public static view : fairygui.GComponent;//-----JiaTao
        constructor(view: fairygui.GComponent) {
            G9999ChipFrame.view = view;//-----JiaTao
            this.chipItemMgr = ChipItemMgr.inst;

            this.chipCtl = view.getController('jetton');
            this.chipRect = view.getChild('comChipRect').asCom;//下注区
            // let chipPlace = [3, 4, 5, 1, 2];
            // let RatioList = ['1:11', '1:8', '1:11', '1:1', '1:1'];
            let chipPlace = [0,3, 4, 5, 1, 2];//Jia
            let RatioList = ['0:0','1:11', '1:8', '1:11', '1:1', '1:1'];//Jia
            for (let i = 0; i < this.chipRect.numChildren; i++) {
                let childName =  this.chipRect.getChildAt(i).name;//Jia
                if(childName == 'bg') continue;//Jia
                let element = this.chipRect.getChildAt(i).asCom;
                let chipRectItem = new ChipRectItem(element,view);
                chipRectItem.setRatioData(RatioList[i]);
                chipRectItem.Place = chipPlace[i];
                this.chipRectItems[chipPlace[i]] = chipRectItem;
            }
            // let chipBtnsName: Array<string> = ['jetton100', 'jetton500', 'jetton1000', 'jetton2000', 'jetton5000', 'jetton10000']
            let chipBtnsName: Array<string> = ['jetton1', 'jetton2', 'jetton5', 'jetton10', 'jetton20', 'jetton50']//JiaTao
            chipBtnsName.forEach(name => {
                let btn = view.getChild(name).asCom;
                this.chipBtns[name.slice(6)] = btn;
            });

            Laya.timer.loop(2000,this,this.randomGoldLight.bind(this),[view],false);

        }

        reset(){
            //console.log('9999999999999');
            ChipItemMgr.reset_inst();
            Laya.timer.clearAll(this);
        }
        //JiaTao
        randomGoldLight(view : any){
            let jetton = ['jetton1', 'jetton2', 'jetton5', 'jetton10', 'jetton20', 'jetton50'];
            let index = parseInt((Math.random()*6).toString());
            this.goldLight = view.getChild(jetton[index]).asCom.getChild('goldLight').asMovieClip;
            this.goldLight.playing = true;
            this.goldLight.asMovieClip.setPlaySettings(0,-1,1,-1,Handler.create(this,function(){
                this.goldLight.playing = false;
            }));
        }

        getChipRectItem(place) {
            return this.chipRectItems[place];
        }

        resetRectData() {
            this.chipRectItems.forEach(value => {
                value.TotalChipData = 0;
                value.SelfChipData = 0;
            });
        }

        get ChipRectItems() {
            return this.chipRectItems;
        }

        get ChipChoose(): number {
            return parseInt(this.chipCtl.selectedPage)
        };
    }
    class ChipRectItem {
        public area: fairygui.GComponent;//JiaTao
        public clickRect: fairygui.GComponent;
        private ratioData: string;
        private ratioText: fairygui.GLabel;
        private totalChipData: number;
        private slash : fairygui.GLabel;//Jia
        private totalChipText: fairygui.GLabel;
        private selfChipData: number;
        private aniTwinkle: fairygui.Transition;
        private clickCallBack: (poi: laya.maths.Point) => void;
        private selfChipText: fairygui.GLabel;
        private ctl: fairygui.Controller;
        private place: number;
        private chipLayout : fairygui.GComponent;
        constructor(parent: fairygui.GComponent,view:fairygui.GComponent) {//---JiaTao
            this.chipLayout = view.getChild('chipLayout').asCom;//-----JiaTao
            this.area = parent.getChild('area').asCom;//JiaTao
            this.clickRect = parent.getChild('clickRect').asCom;
            this.ratioText = parent.getChild('title2').asLabel;//ratio比率
            this.totalChipText = parent.getChild('txtTotalChip').asLabel;
            this.slash = parent.getChild('slash').asLabel;//JiaTao
            this.selfChipText = parent.getChild('txtSelfChip').asLabel;
            this.ctl = parent.getController('ctl');
            this.aniTwinkle = parent.getTransitionAt(0);
            this.clickRect.onClick(this, () => {
                let poi: laya.maths.Point = this.getClickPoi()
                this.clickCallBack(poi)
            })
        }

        set Place(value: ChipValue) {
            this.place = value;
        }

        get Place() {
            return this.place
        }

        setRatioData(value: string = '') {
            this.ratioData = value;
            this.ratioText.text = value;
        }

        set ClickCallBack(value: (poi: laya.maths.Point) => void) {
            this.clickCallBack = value;
        }

        set TotalChipData(value: number) {
            if (value != null) {
                this.totalChipData = Math.floor(value);
                this.totalChipText.text = this.totalChipData.toString();
            }
        }
        get TotalChipData() {
            return this.totalChipData
        }

        set SelfChipData(value: number) {
            if (value != null) {
                this.selfChipData = Math.floor(value);
                if (this.selfChipData == 0) {
                    //this.slash.visible = false;//JiaTao
                    //this.selfChipText.visible = false;
                    this.selfChipText.text = this.selfChipData.toString();
                }
                else {
                    //this.slash.visible = true;//JiaTao
                    //this.selfChipText.visible = true;
                    // this.selfChipText.text = '[color=#FFFFFF]下注：[/color]' + this.selfChipData.toString();
                    //-------JiaTao
                    this.selfChipText.text = this.selfChipData.toString();
                }

            }
        }

        get SelfChipData() {
            return this.selfChipData
        }

        twinkle(handler?: Handler) {
            this.aniTwinkle.play(handler);
        }

        getRandomPoi(rect: { width: number, height: number } = { width: 41, height: 41 }) {
            //let x = (this.clickRect.actualWidth - rect.width * 2) < 0 ? this.clickRect.actualWidth / 2 : (this.clickRect.actualWidth - rect.width * 2) * Math.random() + rect.width;
            //let y = (this.clickRect.actualWidth - rect.height * 2) < 0 ? this.clickRect.actualHeight / 2 : (this.clickRect.actualHeight - rect.height * 2) * Math.random() + rect.height;
            // let screenPos = this.clickRect.localToGlobal(x, y);
            //JiaTao
            let x = (this.area.actualWidth - rect.width * 2) < 0 ? this.area.actualWidth / 2 : (this.area.actualWidth - rect.width * 2) * Math.random() + rect.width;
            let y = (this.area.actualWidth - rect.height * 2) < 0 ? this.area.actualHeight / 2 : (this.area.actualHeight - rect.height * 2) * Math.random() + rect.height;
            let screenPos = this.area.localToGlobal(x, y);
            // return fairygui.GRoot.inst.globalToLocal(screenPos.x, screenPos.y);
            //return ChipItemMgr.chipLayout.globalToLocal(screenPos.x, screenPos.y);
            return this.chipLayout.globalToLocal(screenPos.x, screenPos.y);
        }

        getClickPoi(rect: { width: number, height: number } = { width: 41, height: 41 }) {
            //let poi: laya.maths.Point = fairygui.GRoot.inst.globalToLocal(laya.events.MouseManager.instance.mouseX, laya.events.MouseManager.instance.mouseY);
            //let lt = FairyguiTools.localToRoot(this.clickRect, { x: 21, y: 21 });
            //let rb = FairyguiTools.localToRoot(this.clickRect, { x: this.clickRect.actualWidth - 21, y: this.clickRect.actualHeight - 21 });
            //JiaTao
            // let poi: laya.maths.Point = ChipItemMgr.chipLayout.globalToLocal(laya.events.MouseManager.instance.mouseX, laya.events.MouseManager.instance.mouseY);
            let poi: laya.maths.Point = this.chipLayout.globalToLocal(laya.events.MouseManager.instance.mouseX, laya.events.MouseManager.instance.mouseY);
            let lt = FairyguiTools.localToRoot(this.area, { x: 21, y: 21 });
            let rb = FairyguiTools.localToRoot(this.area, { x: this.area.actualWidth - 21, y: this.area.actualHeight - 21 });
            poi.x = poi.x < lt.x ? lt.x : poi.x
            poi.x = poi.x > rb.x ? rb.x : poi.x
            poi.y = poi.y < lt.y ? lt.y : poi.y
            poi.y = poi.y > rb.y ? rb.y : poi.y
            return poi
        }
    }

    class ChipItemMgr {
        private static _inst: ChipItemMgr = null;
        public static get inst(): ChipItemMgr {
            if (ChipItemMgr._inst == null) {
                ChipItemMgr._inst = new ChipItemMgr(G9999ChipFrame.view);
            }
            return ChipItemMgr._inst;
        }
        public static  reset_inst() {
            this._inst = null;
        }
        public static chipLayout : fairygui.GComponent;
        private parent: fairygui.GComponent;// = fairygui.GRoot.inst;
        private chipPool: Array<ChipItem> = [];
        private chipList: Array<ChipItem> = [];
        private constructor(view: fairygui.GComponent) {//view: fairygui.GComponent
            ChipItemMgr.chipLayout = view.getChild('chipLayout').asCom;
            this.parent = view.getChild('chipLayout').asCom;
        }

        private addChip(value: ChipValue) {
            let chip: ChipItem = new ChipItem(fairygui.UIPackage.createObject('G9999', 'JettonItem').asCom, value,this.parent);
            //console.log('BUG测试----——-',this.parent,this.parent.name);
            this.parent.addChild(chip.item);
            //SetChildIndex(元件,0)
            //chip.item.setChildIndex(chip.item,100);
            this.chipList.push(chip);
            chip.item.setXY(0, 0);
            return chip;
        }

        getChip(value: ChipValue) {
            let chip: ChipItem;
            if (this.chipPool.length > 0) {
                chip = this.chipPool.shift()
                this.chipList.push(chip);
                chip.Value = value;
            }
            else {
                chip = this.addChip(value);
            }
            //chip.item._parent.name;
            //console.log('BUG2222----',chip.item._parent.name);
            chip.item.removeFromParent();
            this.parent.addChild(chip.item);
            chip.item.setXY(0, 0);
            chip.item.visible = true;
            return chip
        }

        hideChip(chip: ChipItem) {
            let index = this.chipList.indexOf(chip)
            if (index != -1) {
                let chip = this.chipList.splice(index, 1)[0];
                chip.item.visible = false;
                this.chipPool.push(chip);
            }
        }

        clearChip(){
            for(let i = 0;i < this.chipList.length;i++){
                let chip = this.chipList.shift();
                chip.item.removeFromParent();
                chip.item.dispose();
            }
            for(let i = 0; i < this.chipPool.length;i++){
                let chip = this.chipPool.shift();
                chip.item.removeFromParent();
                chip.item.dispose();
            }
        }
        get ChipPool() {
            return this.chipPool;
        }

        get ChipList() {
            return this.chipList;
        }

        // distributor(num: number): { _100?: number, _500?: number, _1000?: number, _2000?: number, _5000?: number, _10000?: number } {
        //     let obj: { _100?: number, _500?: number, _1000?: number, _2000?: number, _5000?: number, _10000?: number } = {};
        //     obj._10000 = Math.floor(num / 10000);
        //     num %= 10000;
        //     obj._5000 = Math.floor(num / 5000);
        //     num %= 5000;
        //     obj._2000 = Math.floor(num / 2000);
        //     num %= 2000;
        //     obj._1000 = Math.floor(num / 1000);
        //     num %= 1000;
        //     obj._500 = Math.floor(num / 500);
        //     num %= 500;
        //     obj._100 = Math.floor(num / 100);
        //     return obj;
        // }
        //JiaTao
        distributor(num: number): { _1?: number, _2?: number, _5?: number, _10?: number, _20?: number, _50?: number } {
            let obj: { _1?: number, _2?: number, _5?: number, _10?: number, _20?: number, _50?: number } = {};
            obj._50 = Math.floor(num / 50);
            num %= 50;
            obj._20 = Math.floor(num / 20);
            num %= 20;
            obj._10 = Math.floor(num / 10);
            num %= 10;
            obj._5 = Math.floor(num / 5);
            num %= 5;
            obj._2 = Math.floor(num / 2);
            num %= 2;
            obj._1 = Math.floor(num / 1);
            return obj;
        }

    }
    class ChipItem {
        public item: fairygui.GComponent;
        private value: number;
        private startPos: { x: number, y: number };
        private endPos: { x: number, y: number };
        private valueCtl: fairygui.Controller;
        private moveAni: fairygui.Transition;
        private chipLayout : fairygui.GComponent;//--JiaTao
        constructor(item: fairygui.GComponent, value: ChipValue,chipLayout:fairygui.GComponent) {//--JiaTao
            this.chipLayout = chipLayout;
            this.item = item;
            this.valueCtl = item.getController('value');
            this.moveAni = item.getTransition('move');
            this.valueCtl.selectedPage = value.toString();
            this.value = value;
        }
        //筹码往下注区飞和往闲家飞
        play(startPos: { x: number, y: number }, endPos: { x: number, y: number, }, handler?: Handler) {
            this.startPos = startPos;
            this.endPos = endPos;
            this.moveAni.setValue('startpos', this.startPos.x, this.startPos.y);
            this.moveAni.setValue('endpos', this.endPos.x, this.endPos.y);
            this.moveAni.play(handler);
        }
        //筹码往庄家飞
        recycle(endPos: { x: number, y: number, }, handler?: Handler) {
            //SoundMgrBaccarat.bets();
            //FairyguiTools.changeParentNotMove(fairygui.GRoot.inst, this.item);//----因容器所以屏蔽 下同
            // FairyguiTools.changeParentNotMove(ChipItemMgr.chipLayout, this.item);\
            FairyguiTools.changeParentNotMove(this.chipLayout, this.item);
            this.startPos = this.endPos;
            this.endPos = endPos;
            this.moveAni.setValue('startpos', this.startPos.x, this.startPos.y);
            this.moveAni.setValue('endpos', this.endPos.x, this.endPos.y);
            this.moveAni.play(handler);
        }

        get Value() {
            return this.value;
        }
        set Value(value: ChipValue) {
            this.value = value;
            this.valueCtl.selectedPage = value.toString();
        }
    }
    export enum ChipValue {
        //JiaTao
        _1 = 1,
        _2 = 2,
        _5 = 5,
        _10 = 10,
        _20 = 20,
        _50 = 50,
        // _100 = 100,
        // _500 = 500,
        // _1000 = 1000,
        // _2000 = 2000,
        // _5000 = 5000,
        // _10000 = 10000,
    }
}