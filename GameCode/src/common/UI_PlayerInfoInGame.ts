class UI_PlayerInfoInGame extends Widget{
    constructor(){
        super('Basic','UI_PlayerInfoInGame',UILayer.POPUP);
        this.keepCenter();
    }

    onCreated(){
        let btnClose = this._view.getChild('btn_mask').asButton;
        btnClose.onClick(this,()=>{
            this.hide();
        });
    }
}