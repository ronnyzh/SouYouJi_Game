/*
* name;
*/

class Alert extends Page{
    public static get BTN_OK(){ return 0x1};
    public static get BTN_CANCEL(){ return 0x2};

    public static show(content:string,needCancel:boolean = false){
        var alert = UIMgr.inst.add(UIMgr.alertClass) as Alert;
        alert.setContext(content,needCancel);
        return alert;
    }

    private content:fairygui.GTextField;
    private needCancel:boolean;

    private okHandler:Function;
    private cancelHandler:Function;
    private handler:Function;

    constructor(pkg:string,comp:string,layer:number){
        super(pkg,comp,layer);
    }
    
    onCreated(){
        this.content = this._view.getChild('content').asTextField;

        var btnOK = this._view.getChild('btn_ok').asButton;
        var self = this;
        btnOK.onClick(this,function(){
            self.hide();
            if(self.okHandler){
                self.okHandler(Alert.BTN_OK);
            }
            if(self.handler){
                self.handler(Alert.BTN_OK);
            }
        }.bind(this));

        var btnCancel = this._view.getChild('btn_cancel').asButton;
        btnCancel.onClick(this,function(){
            self.hide();
            if(self.cancelHandler){
                self.cancelHandler(Alert.BTN_CANCEL);
            }
            if(self.handler){
                self.handler(Alert.BTN_CANCEL);
            }
        }.bind(this));
    }

    setContext(content:string,needCancel:boolean)
    {
        //account not exist
        this.content.text = content;
        this.needCancel = needCancel;
        var btnCancel = this._view.getChild('btn_cancel').asButton;
        var btnOK = this._view.getChild('btn_ok').asButton;
        btnCancel.visible = this.needCancel;

        if(this.needCancel){
            btnOK.x = this._view.width / 2 - btnOK.width/2 - 150;
            btnCancel.x = this._view.width / 2 - btnCancel.width/2 + 150;    
        }
        else{
            btnOK.x = this._view.width / 2 - btnOK.width/2;
        }
    }

    on(fn:Function):Alert{
        this.handler = fn;
        return this;
    }

    onYes(fn:Function):Alert{
        this.okHandler = fn;
        return this;
    }

    onNO(fn:Function):Alert{
        this.cancelHandler = fn;
        return this;
    }
}