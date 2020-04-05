class GallPlayerFrame {
    public side: number
    public sex: number;
    public isInit: boolean = false;

    protected score: number;
    protected seat: fairygui.GComponent;
    protected nameText: fairygui.GLabel;
    protected scoreText: fairygui.GLabel;
    protected imgHead: fairygui.GLoader;

    constructor(components: Object) {
        this.side = components['side'];
        let component = components['seat'];
        this.seat = component;
        this.nameText = component.getChild('name').asLabel;
        this.scoreText = component.getChild('score').asLabel;
        this.imgHead = component.getChild('icon').asLoader;
    }

    setSeat(data, scoreDef: string = '') {
        if (!data) return;
        if (this.side != 0)
            this.nameText.text = Tools.inst.maskUserName(data['nickname']);
        else
            Tools.inst.SetNickNameAfter(this.nameText, data['nickname']);
        this.sex = parseInt(data['sex'] || 0);
        this.setScoreString(parseFloat(data['coin'] || 0), scoreDef);
        this.imgHead.url = 'ui://la8oslyoosvmbg';
        let headImgUrl = data['headImgUrl'];
        try {
            if (headImgUrl)
                Tools.inst.changeHeadIcon(headImgUrl, this.imgHead);
            else if (this.side == 0)
                Tools.inst.changeHeadIcon(UserMgr.inst.imgUrl, this.imgHead);
        } catch (error) {
            console.log(error)
        }
        this.seat.visible = true;
        this.isInit = true;
    }

    setScoreString(score, def: string = '0') {
        this.score = score;
        this.setScoreText(def);
    }

    protected setScoreText(def: string = '0') {
        this.scoreText.text = Tools.inst.changeGoldToMoney(this.score, def);
    }


}