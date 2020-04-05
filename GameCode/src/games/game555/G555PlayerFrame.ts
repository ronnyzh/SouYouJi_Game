class G555PlayerFrame extends GbpPlayerFrame {
    showBullStr(bullnum: number) {
        SoundMgrNiu.playNiuEffect(bullnum, this.sex);
        super.showBullStr(bullnum);
    }
    updateBankerState(dealer) {
        this.out_QCtl.setSelectedIndex(1);
        super.updateBankerState(dealer);
    }
    resetGame() {
        super.resetGame();
        this.hideStriveBankerMask();
    }
}