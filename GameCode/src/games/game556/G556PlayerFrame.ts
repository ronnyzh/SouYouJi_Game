/*
* name;
*/
class G556PlayerFrame extends GbpPlayerFrame {

    protected bullStyle = 0;

    constructor(components: Object) {
        super(components);
        this.bullStyle = components['bullStyle'];
    }

    showBullStr(bullnum: number) {
        super.showBullStr(bullnum);
        if (this.bullStyle == 1) {
            SoundMgrNiu.playSGEffect(bullnum);
        }
        else {
            SoundMgrNiu.playNiuEffect(bullnum, this.sex);
        }
    }
}