module G565 {
    export class G565BidSlider {
        private parent: fairygui.GComponent;
        private slider: fairygui.GSlider;
        private chipList: Array<fairygui.GComponent>;
        private bar: fairygui.GObject;
        private addBtn: fairygui.GButton;
        private addEvt: () => void;
        private subBtn: fairygui.GButton;
        private subEvt: () => void;
        private addGoldValueText: fairygui.GLabel;
        private addGoldValueBg: fairygui.GImage;
        private onChanged: () => void;
        private showAllinAni: () => void;
        private hideAllinAni: () => void;
        public addGoldMin: number;
        public addGoldMax: number;
        public allinNumber: number;
        private addGoldValue: number;
        public baseScore: number;

        constructor(parent: fairygui.GComponent) {
            this.parent = parent;
            this.slider = parent.getChild('item').asSlider;
            let sliderY = this.slider.y;
            //this.slider.changeOnClick = false;
            this.chipList = [];
            let chipName = 'chip';
            let goldY: number;
            for (let i = 0; i < 38; i++) {
                let chip = parent.getChild(chipName + i).asCom;
                this.chipList.push(chip)
                chip.visible = false;
                goldY = chip.y;
            }
            this.bar = this.slider.getChild('bar_v');
            this.addGoldValueText = parent.getChild('txtCallNumber').asLabel;
            let addGoldValueY = this.addGoldValueText.y;
            this.addGoldValueBg = parent.getChild('callNumberBg').asImage;
            this.onChanged = () => {
                this.AddGoldValue = this.addGoldMin + this.value * this.baseScore;
                this.AddGoldValue = this.AddGoldValue > this.addGoldMax ? this.addGoldMax : this.AddGoldValue < this.addGoldMin ? this.addGoldMin : this.AddGoldValue;
                Laya.timer.frameOnce(1, this, () => {
                    this.addGoldValueBg.y = addGoldValueY + this.bar.y;
                    for (let chip of this.chipList) {
                        if (goldY + this.bar.y <= chip.y) {
                            if (chip.visible == false) {
                                chip.visible = true;
                                chip.getTransitionAt(0).play();
                            }
                        } else {
                            chip.visible = false;
                        }
                    }
                })
                if (this.value == this.max) {
                    this.showAllinAni();
                } else {
                    this.hideAllinAni();
                }
            }
            let allinAni = {
                bg: parent.getChild('n7'), text: parent.getChild('n5'), fg: parent.getChild('n6'), ani: parent.getTransitionAt(0),
            };
            this.showAllinAni = () => {
                if (allinAni.text.visible == false) {
                    allinAni.bg.visible = true;
                    allinAni.text.visible = true;
                    allinAni.fg.visible = true;
                    allinAni.ani.play();
                }
            };
            this.hideAllinAni = () => {
                if (allinAni.text.visible == true) {
                    allinAni.bg.visible = false;
                    allinAni.text.visible = false;
                    allinAni.fg.visible = false;
                }
            };
            {
                this.addBtn = parent.getChild('btnAdd').asButton;
                this.subBtn = parent.getChild('btnSub').asButton;
                this.addEvt = () => {
                    if (this.value + 1 <= this.max) {
                        this.value++;
                        this.onChanged();
                    }
                };
                this.subEvt = () => {
                    if (this.value - 1 >= 0) {
                        this.value--;
                        this.onChanged();
                    }
                }
            }
            this.hide();
        }

        private show() {
            this.addBtn.onClick(this, this.addEvt);
            this.subBtn.onClick(this, this.subEvt);
            this.parent.visible = true;
            let number = Math.ceil((this.addGoldMax - this.addGoldMin) / this.baseScore);
            this.max = number;
            this.value = 0;
            this.onChanged();
            this.slider.on(fairygui.Events.STATE_CHANGED, this, this.onChanged);
        }

        getAddGoldValue() {
            return this.AddGoldValue;
        }

        private get AddGoldValue() {
            return this.addGoldValue;
        }

        private set AddGoldValue(value: number) {
            this.addGoldValue = value || 0;
            this.addGoldValueText.text = Tools.inst.changeGoldToMoney(this.addGoldValue);
        }

        private hide() {
            for (let i = 0; i < 38; i++) {
                let chip = this.chipList[i];
                chip.visible = false;
            }
            this.addBtn.mode = -1;
            this.subBtn.mode = -1;
            this.addBtn.offClick(this, this.addEvt);
            this.subBtn.offClick(this, this.subEvt);
            this.hideAllinAni();
            this.parent.visible = false;
            this.slider.off(fairygui.Events.STATE_CHANGED, this, this.onChanged);
            Laya.timer.clearAll(this);
        }

        get visible() {
            return this.parent.visible;
        }

        set visible(value: boolean) {
            if (value) {
                this.show();
            }
            else {
                this.hide();
            }
        }

        private get value() {
            return this.slider.value;
        }
        private set value(value: number) {
            this.slider.value = value;
        }

        private set max(value: number) {
            this.slider.max = value;
        }

        private get max() {
            return this.slider.max;
        }
    }
}