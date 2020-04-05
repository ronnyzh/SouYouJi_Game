/*
* name;
*/
class G452Page extends G445Page {

    initMsgListen() {
        super.initMsgListen();

        // NetHandlerMgr.netHandler.addMsgListener(ProtoKeyMJG.S_C_GOLDUPDATE, this.onGoldUpdate.bind(this));
    }

    pageStyleSetting(data) {
        var view = this._view;

        var txtTitle = view.getChild('txtTitle').asLabel;
        txtTitle.text = ExtendMgr.inst.getText4Language("广东麻将");

        // this.setGhostTile('d5');
        this.setBalance.setStyle(1);
    }
    public gameID = 452;

    showBalance(setData) {
        this.setBalance.showData(setData, SetBalanceStyle.HORSE_WIN);
    }

    onKeyDown(e: Event): void {
        if (TestMgr.IS_REAL_ACCOUNT) return;
        var keyCode: number = e["keyCode"];
        var Keyboard = Laya.Keyboard;
        switch (keyCode) {
            case Keyboard.NUMBER_1:
                NetHandlerMgr.netHandler.gameManage("1:d5d5d5d5", this.onGMResult.bind(this));
                break;
            case Keyboard.NUMBER_2:
                NetHandlerMgr.netHandler.gameManage("2:a1a1a1a1", this.onGMResult.bind(this));
                break
            default:
                console.log(keyCode)
                break;
        }
    }
}