class G558Page extends G556Page {
    public gameID = 558;
    protected uiPlayerCount: number = 6;
    private myTitle: Array<string> = [];
    constructor(comp) {
        super("GS_558");
    }

    onSetStart(msgData, finishedListener) {
        //console.log(msgData)
        this.resetGame();
        this.hideTimeTip();
        this.gameStateCtl.selectedIndex = 1;
        SoundMgrNiu.gameStart();
        Tools.inst.setTimeout(() => {
            if (finishedListener) finishedListener();
            this.gameStateCtl.selectedIndex = 0;
        }, 1000);
    }


    receivedGambleWager(msgData, finishedListener) {
        if (msgData["reason"]) return;
        var wager_infos = msgData["data"];
        for (var i = 0; i < wager_infos.length; i++) {
            var dt = wager_infos[i];
            var posLocal = this.getLocalPos(dt["side"]);
            let player = this.getPlayer(posLocal);
            player.setWagerStr(dt["ga"]);
            SoundMgrNiu.xia(dt["ga"])
            SoundMgrNiu.actionFinish();
            if (posLocal == 0) {
                this.robTheVillageBG.visible = false;
                break;
            }
        }
        if (finishedListener) finishedListener();
    }

    onBtnOpen() {
        this.getPlayer(0).setCards(this.myTitle);
        this.btnOpen.visible = false;
        this.getPlayer(0).showOutPokersAction();
        NetHandlerMgr.netHandler.sendOnHasBullOrNot(2);
    }

    onDealTiles(msgData, finishedListener) {
        let sides = msgData["participantSides"];
        let tiles = msgData["tiles"];
        sides = sides.map((value, index, array) => {
            return this.getLocalPos(value);
        })
        sides.sort();
        this.myTitle = tiles;
        for (var i = 0; i < sides.length; i++) {
            let side = sides[i];
            let player = this.getPlayer(side);
            if (side == 0) {
                SoundMgrNiuJD.fapai();
            }
            if (side != 0) {
                player.setCards(new Array(tiles.length));
            } else {
                player.setCards(tiles);
                this.btnOpen.visible = true;
            }
        }
        this.gameStateCtl.selectedIndex = 2;
        if (finishedListener) finishedListener();
    }
}