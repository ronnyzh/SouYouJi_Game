/*
* name;
*/
class LayoutBtns{
    constructor(comp:fairygui.GComponent){
        let btnList = [];
        for(let i = 0; i < btnList.length;++i){
            let btnName = btnList[i];
            comp.getChild(btnName).asButton.onClick(this,this.onBtnClicked,[btnName]);
        }
    }

    onBtnClicked(sender){
        if(sender == 'btn_quick_start'){
            UIMgr.inst.popup(UI_JoinGame);
        }
    }
}