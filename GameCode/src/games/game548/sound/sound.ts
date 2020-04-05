module G548 {
    export namespace SoundMgrBaccarat{
        export let SND_PATH = 'baccarat_bd/';

        export function playEffect(path) {
            SoundMgr.playEffect(SND_PATH + path);
        }

        export function getSexPath(sex) {
            return SoundMgr.getSexPath(sex);
        }

        export function playBGM(path?){
            SoundMgr.playMusic(path || 'bgm_bdBjl.mp3');
        }

        export function stopBGM(){
            SoundMgr.stopMusic();
        }
        //下注时飞筹码声音
        export function bets() {
            this.playEffect("bets.mp3");
        }
        //飞筹码
        export function chipFly() {
            this.playEffect("chipfly.mp3");
        }
        //筹码出现时声音
        export function window_open() {
            this.playEffect("window_open.mp3");
        }
        //筹码选中
        export function chipClick() {
            this.playEffect("chipClick.mp3");
        }
        //翻牌
        export function cards_dealing() {
            this.playEffect("cards_dealing.mp3");
        }
        //发牌
        export function pushCard() {
            this.playEffect("pushcard.mp3");
        }

        export function startBidGame() {
            this.playEffect("startBid.mp3");
        }

        export function clockRing() {
            this.playEffect("clockring.mp3");
        }

        //播放结算时,点数和输赢结果音效. Laya.SoundManager.playSound(SOUND_PATH + n);
        export function playAIsound(soundName:string){
            let name = soundName + '.mp3';
            this.playEffect(name);
        }
    }
}
