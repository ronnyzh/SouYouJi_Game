module G9999 {
    export namespace SoundMgrBaccarat{
        export let SND_PATH = 'baccarat/';

        export function playEffect(path) {
            SoundMgr.playEffect(SND_PATH + path);
        }

        export function getSexPath(sex) {
            return SoundMgr.getSexPath(sex);
        }

        export function playBGM(path?){
            SoundMgr.playMusic(path || 'bgm_bjl.ogg');
        }

        export function stopBGM(){
            SoundMgr.stopMusic();
        }

        export function bets() {
            this.playEffect("bets.ogg");
        }

        export function chipFly() {
            this.playEffect("chipfly.ogg");
        }

        export function window_open() {
            this.playEffect("window_open.ogg");
        }

        export function cards_dealing() {
            this.playEffect("cards_dealing.ogg");
        }
    }
}
