/*
* name;
*/
class G563Page extends G556Page {
    constructor(scene = "GS_563") {
        super(scene);
    }
    public gameID = 563;
    public bullStyle = 1;
    protected uiPlayerCount: number;
    protected tableUrl = ResourceMgr.RES_PATH + 'bg/zhuozi.jpg';
    protected bgUrl = ResourceMgr.RES_PATH + 'bg/table3.jpg';
    public poolKey = 'G563Poker';

    initPool() {
        //预先把发牌动画的牌加到池里
        for (let j = 0; j < 2 * this.uiPlayerCount; j++) {
            GObjectPool.inst.removeItemToPool(this.poolKey, fairygui.UIPackage.createObject('G556', 'Poker'));
        }
    }

    onGoldInfo(msgData) {
        let difen = Tools.inst.changeGoldToMoney(msgData['gold']);    //底分
        let info = ExtendMgr.inst.getText4Language(msgData['info']);     //场次信息
        let partyType = msgData['party_type']; //2:金币场 3：竞技场 4: 金币好友房
        let gamenumber = msgData['gamenumber'];
        let tfGameInfo = this._view.getChild("tfGameInfo").asLabel;
        tfGameInfo.text = info + "  " + ExtendMgr.inst.getText4Language("底分：") + difen;
        let tfGameNumInfo = this._view.getChild('tfGameNumInfo').asLabel;
        tfGameNumInfo.text = ExtendMgr.inst.getText4Language('牌局编号：') + '\n ' + gamenumber;
    }

    onHasBullOrNot(msgData,finishedListener) {
        if (!msgData['data']) return;
        var scData = msgData['data'][0];
        if (!scData) return;
        var side = this.getLocalPos(scData['side']);
        if (side == 0) this.btnOpen.visible = false;
        var info = scData['info'];
        var bullnum = info['bullnum'];

        if (true || bullnum > 0) {
            var player = this.getPlayer(side);
            if (!player.isBullFinish()) {

                var tiles: string[] = info["handcards"];
                if (info['tiles4ten'] != null && info['tiles4bull'] != null) {
                    tiles = info['tiles4ten'].concat(info['tiles4bull']);
                }
                if (tiles.length > 0) {
                    tiles.sort((a, b) => {
                        let numA = parseInt(a.substr(1));
                        let numB = parseInt(b.substr(1));
                        if (numA != numB) {
                            return numB - numA;
                        } else {
                            let typeA = a.substr(0, 1);
                            let typeB = a.substr(0, 1);
                            let temp = ['e', 'a', 'b', 'c', 'd'];
                            return temp.indexOf(typeA) - temp.indexOf(typeB);
                        }
                    })
                    let cb = () => {
                        player.showBullStr(bullnum);
                    }
                    player.setCards(tiles);
                    cb();
                }
            }
            if (side == 0) {
                SoundMgrNiu.pokerHit();
            }
        }

        let isAllPlayerShowCard = true;
        this.PlayerFrames.forEach(player => {
            if (player.isInit == true && player.isBullFinish() == false) {
                isAllPlayerShowCard = false;
            }
        });
        if (isAllPlayerShowCard) {
            this.hideTimeTip();
        }
        if (finishedListener) finishedListener();
    }


    onGetOneResult(msgData, finishedListener) {
        var side = this.getLocalPos(msgData['side']);
        var data = msgData["info"][0];

        var bullnum = data['bullnum'];
        var tiles = data["handcards"];
        if (true || bullnum > 0) {
            if (data['tiles4ten'] != null && data['tiles4bull'] != null) {
                tiles = data['tiles4ten'].concat(data['tiles4bull']);
            }
        }

        if (side == 0) this.btnOpen.visible = false;

        var time = 0;
        var player = this.getPlayer(side);
        if (!player.isBullFinish()) {
            tiles.sort((a, b) => {
                let numA = parseInt(a.substr(1));
                let numB = parseInt(b.substr(1));
                if (numA != numB) {
                    return numB - numA;
                } else {
                    let typeA = a.substr(0, 1);
                    let typeB = a.substr(0, 1);
                    let temp = ['e', 'a', 'b', 'c', 'd'];
                    return temp.indexOf(typeA) - temp.indexOf(typeB);
                }
            })
            let cb = () => {
                player.showBullStr(bullnum);
                if (finishedListener) finishedListener();
            }
            player.setCards(tiles);
            cb();

            time = 500;
            if (side == 0) {
                SoundMgrNiu.pokerHit();
            }
        } else {
            if (finishedListener) finishedListener();
        }
        let isAllPlayerShowCard = true;
        this.PlayerFrames.forEach(player => {
            if (player.isInit == true && player.isBullFinish() == false) {
                isAllPlayerShowCard = false;
            }
        });
        if (isAllPlayerShowCard) {
            this.hideTimeTip();
        }
    }

}