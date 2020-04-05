/*
* name;
*/
class LayoutSubBtns{
    constructor(comp:fairygui.GComponent){
        var btnList = ['btn_lobby','btn_mall','btn_zhanji','btn_mine'];
        for(let i = 0; i < btnList.length;++i){
            let btnName = btnList[i];
            comp.getChild(btnName).asButton.onClick(this,this.onBtnClicked,[btnName]);
        }

        var btnList = ['btn_guize','btn_kefu','btn_setting'];
        var menu = comp.getChild('menu').asCom;
        for(let i = 0; i < btnList.length;++i){
            let btnName = btnList[i];
            menu.getChild(btnName).asButton.onClick(this,this.onBtnClicked,[btnName]);
        }
    }

    onBtnClicked(sender){
        if(sender == 'btn_lobby'){
            MasterMgr.inst.switch('lobby');
        }
        else if(sender == 'btn_mall'){
            
        }
        else if(sender == 'btn_kefu'){
            
        }
        else if(sender == 'btn_setting'){

        }
        else if(sender == 'btn_mine'){
            
        }
        //转发给子游戏场景处理
        else if(sender == 'btn_zhanji'){
            bk.emit("btn_zhanji_clicked");
        }
        else if(sender == 'btn_guize'){
            bk.emit("btn_guize_clicked");
        }
    }
}