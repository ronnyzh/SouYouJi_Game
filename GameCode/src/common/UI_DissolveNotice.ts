class UI_DissolveNotice extends Widget{
    private _endTime:number = -1;
    private _info:fairygui.GLabel = null;
    constructor(){
        super('Basic','UI_DissolveNotice',UILayer.POPUP);
        this.startUpdate(200);
        this.keepCenter();
    }

    onCreated(){
        this._info = this._view.getChild('info').asLabel;
        var data = RoomMgr.inst.dissoveData;
        if (!data) {
            return;
        }

        let btnList = ['btn_reject','btn_agree'];
        super.listenButtons(btnList,this.onBtnClicked);

        var list = this._view.getChild('list').asList;
        for(var i = 0; i < list.numChildren; ++i){
            let item = list.getChildAt(i).asCom;
            item.getControllerAt(0).setSelectedIndex(1);
        }

        this._endTime = Date.now() / 1000 + data.time;
        var agrees = "";
        var disagrees = "";
        for (var i = 0; i < data.states.length; ++i) {
            var b = data.states[i];
            var seat = RoomMgr.inst.seats[i];
            if (!seat) {
                break;
            }
            if(seat.userId){
                let item = list.getChildAt(i).asCom
                item.getControllerAt(0).setSelectedIndex(0);
                item.getChild('info').text = seat.name + '  ID:' + seat.userId;
                item.getChild('confirm_flag').visible = b;
            }
        }

        this._info.text = this.getInfoStr();

        var hasAgree = data.states[RoomMgr.inst.seatIndex];
        if(hasAgree){
            this._view.getControllerAt(0).setSelectedIndex(1);
        }
        else{
            this._view.getControllerAt(0).setSelectedIndex(0);
        }
    }

    onBtnClicked(btnName){
        if(btnName == 'btn_reject'){
            RoomMgr.inst.sendRoomDissolveReject();
        }
        else if(btnName == 'btn_agree'){
            RoomMgr.inst.sendRoomDissolveAgree();
        }
        this.hide();
    }

    getInfoStr(){
        if (this._endTime > 0) {
            var lastTime = this._endTime - Date.now() / 1000;
            if (lastTime < 0) {
                lastTime = 0;
                this._endTime = -1;
            }

            var m = Math.floor(lastTime / 60);
            var s = Math.ceil(lastTime - m * 60);

            var str = "";
            if (m > 0) {
                str += m + ExtendMgr.inst.DissolveNoticeMin;
            }

            return str + s + ExtendMgr.inst.DissolveNoticeSec;
        }
        return '';
    }

    onUpdate(){
        this._info.text = this.getInfoStr();

        if (!RoomMgr.inst.dissoveData) {
            this.hide();
        }
    }
}