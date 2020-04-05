class UI_ExitGame extends Page{
    constructor(){
        super('Basic','UI_ExitGame',UILayer.GAME);
    }

    onCreated(){
       let btnList = ['btn_setting','btn_exit'];
        for(let i = 0; i < btnList.length;++i){
            let btnName = btnList[i];
            this._view.getChild(btnName).asButton.onClick(this,this.onBtnClicked,[btnName]);
        }
    }

    onBtnClicked(btnName){
        if(btnName == 'btn_setting'){
            UIMgr.inst.popup(UI_Setting);
        }
        else if(btnName == 'btn_exit'){
            // RoomMgr.inst.wantQuitRoom();
        }
        else if(btnName == 'btn_dispress'){
            // RoomMgr.inst.wantQuitRoom();
        }
    }
}