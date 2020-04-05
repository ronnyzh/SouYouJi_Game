
class UI_PresetGoldSetter extends Widget{
    
    public static ON_SET_PRESET_MONEY = 'onSetPresetMoney';

    private inputNum:number = -1;

    constructor(){
        super('Basic','PresetGold',UILayer.POPUP);
        this.keepCenter();
    }
    
    onCreated(){
        var view = this._view;

        if(!laya.renders.Render.isWebGL)
            view.displayObject.cacheAs = 'bitmap';
        
        this.inputNum = -1;

        let txtSetGold = view.getChild('txt_setGold').asLabel;

        let btnClose = view.getChild('btn_close').asButton;
        btnClose.onClick(this,()=>{
            this.onBack();
        });
        
        let btnBack = view.getChild('btn_keyBack').asButton;
        btnBack.onClick(this,()=>{
            let pindex = txtSetGold.text.indexOf('.');
            txtSetGold.text = txtSetGold.text.substring(0,txtSetGold.text.length-1);
            if(txtSetGold.text.length>0)
                this.inputNum = parseFloat(txtSetGold.text);
            else
                this.inputNum = 0;
        });

        let btnOK = view.getChild('btn_keyOK').asButton;
        btnOK.onClick(this,()=>{
            let bring = parseFloat(this.inputNum.toFixed(2));
            if(bring > Tools.inst.changeMoneyToGold(UserMgr.inst.sourceMoney))
            {
                Alert.show(ExtendMgr.inst.PresetGoldNotEnough);
                return;
            }
            HttpMgr.inst.presetGold(bring,function(data)
            {
                if(!data || data.code != 0)
                {
                    Alert.show(ExtendMgr.inst.getText4Language(data.msg));
                }
                else
                {
                    Laya.stage.event(UI_PresetGoldSetter.ON_SET_PRESET_MONEY);
                }
            });
            this.onBack();
        });

        let btnPoint = view.getChild('btn_keyPoint').asButton;
        btnPoint.onClick(this,()=>{
            let pindex = txtSetGold.text.indexOf('.');
            if(pindex<0)
                txtSetGold.text += '.';
        });

        var count = 10;
        for(var i = 0; i<count; i++)
        {
            let btnKey = view.getChild('btn_key'+i).asButton;
            btnKey.onClick(this,function()
            {
                let num = parseInt(btnKey.name.substring(7,8));
                if(this.inputNum == -1)
                {
                    this.inputNum = num;
                }
                else
                {
                    let pindex = txtSetGold.text.indexOf('.');
                    if(pindex>0)
                    {
                        let plen = txtSetGold.text.length - pindex;
                        if(plen >= 3)
                        {
                            return;
                        }

                        if(num == 0)
                        {
                            txtSetGold.text += num.toString();
                            return;
                        }
                        else
                        {
                            for(var j = 0; j<plen; j++)
                            {
                                num*=0.1;
                            }
                            this.inputNum += num;
                            if(plen>=2)
                                this.inputNum = parseFloat(this.inputNum.toFixed(2));
                        }
                    }
                    else
                    {
                        this.inputNum *=10;
                        this.inputNum += num;
                    }
                }
                txtSetGold.text = this.inputNum.toString();
            });
        }
    }
    
    onBack() {
        this.hide();
    }
}