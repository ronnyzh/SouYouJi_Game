/**
 * Created by Administrator on 2018/5/4.
 */
module G561 {
    export namespace Sound {

        export function playBGM(path?){
            try {
                path = path || SoundMgr.MUSIC_PATH+'bgm_zjh.mp3';
                Laya.SoundManager.stopMusic();
                Laya.SoundManager.playMusic(path, 0);
            }catch(e){}
        }
        export function play(path, caller?, callback?) {
             SoundMgr.playSoundABS(ResourceMgr.RES_PATH+path,caller,callback);
        }

        export function alarm() {
            play("sound/doudizhu/normal/alarm.mp3");
        }
        
        export function chip2win(){
            play("sound/zhajinhua/af_flychip.mp3");
        }
        
        export function chip(){
            play("sound/zhajinhua/jh_chip.mp3");
        }

        export function win(){
            play("sound/zhajinhua/af_jhwin.mp3");
        }

        /** 操作 **/
        export function stopOperation(){
            play("sound/zhajinhua/didi.mp3");
        }

        export function pkLose(){
            play("sound/zhajinhua/af_pk_loss.mp3");
        }

        export function allin_ef(){
            play("sound/zhajinhua/af_allin.mp3");
        }

        export function allin(side){
            var sex = Control.playerMgr.getSexServer(side);
            var file = sex==2 ? "jh_w_allin1.mp3" : "jh_m_allin.mp3";
            play("sound/zhajinhua/"+file);
        }

        export function fallow(side){
            var sex = Control.playerMgr.getSexServer(side);
            var file = sex==2 ? "jh_w_gen1.mp3" : "jh_m_gen1.mp3";
            play("sound/zhajinhua/"+file);
        }

        export function jiazhu(side){
            var sex = Control.playerMgr.getSexServer(side);
            var file = sex==2 ? "jh_w_jia.mp3" : "jh_m_jia.mp3";
            play("sound/zhajinhua/"+file);
        }

        export function watchCard(side){
            var sex = Control.playerMgr.getSexServer(side);
            var file = sex==2 ? "jh_w_kan.mp3" : "jh_m_kan.mp3";
            play("sound/zhajinhua/"+file);
        }
        export function dopk(side){
            var sex = Control.playerMgr.getSexServer(side);
            var file = sex==2 ? "jh_w_pk1.mp3" : "jh_m_pk.mp3";
            play("sound/zhajinhua/"+file);
        }
        export function giveup(side){
            var sex = Control.playerMgr.getSexServer(side);
            var file = sex==2 ? "jh_w_qipai1.mp3" : "jh_m_qipai1.mp3";
            play("sound/zhajinhua/"+file);
        }
    }
}