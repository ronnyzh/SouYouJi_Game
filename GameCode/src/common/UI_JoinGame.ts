class UI_JoinGame extends Widget{
    private idArr:Array<fairygui.GLabel> = [];
    private inputPos:number = 0;
    constructor(){
        super('Basic','UI_JoinGame',UILayer.POPUP);
        this.keepCenter();

        var Event = Laya.Event;
        Laya.stage.on(Event.KEY_DOWN, this, this.onKeyDown);
    }

    private onKeyDown(e: Event): void {
        var keyCode: number = e["keyCode"];
	    var Keyboard = Laya.Keyboard;
        if(keyCode>=Keyboard.NUMPAD_0 && keyCode<=Keyboard.NUMPAD_9){
            this.onKeybord(keyCode-Keyboard.NUMPAD_0)
        }
    }

    onCreated(){
        let btnClose = this._view.getChild('win_frame').asCom.getChild('btn_close').asButton;
        btnClose.onClick(this,()=>{
            this.hide();
        });

        for(let i = 0; i < 6; ++i){
            this.idArr[i] = this._view.getChild('id' + i).asLabel;
            this.idArr[i].text = '';
        }

        for(let i = 0; i <= 9; ++i){
            let btn = this._view.getChild('input_' + i).asButton;
            btn.onClick(this,this.onKeybord,[i]);
        }

        let btn = this._view.getChild('input_cs').asButton;
        btn.onClick(this,this.onKeybord,['cs']);

        btn = this._view.getChild('input_sc').asButton;
        btn.onClick(this,this.onKeybord,['sc']);
    }

    reset(){
        for(let i = 0; i < this.idArr.length; ++i){
            this.idArr[i].text = '';
        }
        this.inputPos = 0;
    }

    onKeybord(key){
        if(key == 'cs'){
            this.reset();
        }
        else if(key == 'sc'){
            if(this.inputPos > 0){
                this.inputPos--;
                this.idArr[this.inputPos].text = '';
            }
        }
        else{
            if(this.inputPos < this.idArr.length){
                this.idArr[this.inputPos].text = key.toString();
                this.inputPos++;
                if(this.inputPos == this.idArr.length){
                    this.enterRoom();
                }
            }
        }
    }

    enterRoom(){
        let id = '';
        for(let i = 0; i < this.idArr.length; ++i){
            id += this.idArr[i].text;
        }
        this.onInputFinished(id);
    }

    onInputFinished(roomId){
        var onEnterRoom = function (data) {
            WC.hide();
            console.log("enterRoom ok",data)            
            if(data.ip){
            }
        }.bind(this); 

        WC.show('请求进入房间...');
        UserMgr.inst.enterRoom(roomId,onEnterRoom);
    }
}

/*

    */