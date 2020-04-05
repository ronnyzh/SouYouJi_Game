module G666 {
    export namespace soundMgr{
        export let SND_PATH = 'HLniuniu/';

        export function playEffect(path) {
            SoundMgr.playEffect(SND_PATH + path);
        }

        export function getSexPath(sex) {
            return SoundMgr.getSexPath(sex);
        }

        export function playBGM(path?){
            SoundMgr.playMusic(path || 'bgm_hl.ogg');
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

        export function chipClick() {
            this.playEffect("chipClick.ogg");
        }

        export function cards_dealing() {
            this.playEffect("cards_dealing.ogg");
        }
    }
}