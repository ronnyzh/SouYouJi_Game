/**
 * Created by Administrator on 2018/5/4.
 */
module G559{
    export namespace Sound{

        export function playBGM(path?){
            SoundMgr.playMusic(path || 'bgm_run.mp3');
        }

        export function stopBGM(){
            SoundMgr.stopMusic();
        }

        export function play(path, caller?, callback?) {
            SoundMgr.playSoundABS(SoundMgr.ROOT_PATH +path,caller,callback);
        }

        export function alarm(){
            play("sound/doudizhu/normal/alarm.mp3");
        }


        export function playResult(isWin) {
            play("sound/doudizhu/normal/{0}.mp3".format(isWin ? "win" : "lost"));
        }

        export function bgm() {
            this.playMusic("sound/doudizhu/normal/bgm.mp3");
        }

        /*
         pos1 出牌玩家
         pos2 上一次出牌玩家
         cp1 出牌牌型
         cp2 上一次出牌牌型
         */
        export function playCardEffect(pos1, pos2, cp1, cp2) {
            var sexType = this.getSexType(pos1);
            var cardType1 = cp1.getType();

            var path;
            switch (cardType1) {
                case rfa.CARD_TYPE.BOMB:
                    path = "sound/doudizhu/player/bomb_{0}.mp3".format(sexType);
                    play(path);
                    path = "sound/doudizhu/player/bomb.mp3";
                    play(path);
                    break;

                case rfa.CARD_TYPE.ROCKET:
                    path = "sound/doudizhu/player/rocket_{0}.mp3".format(sexType);
                    play(path);
                    path = "sound/doudizhu/player/bomb.mp3";
                    play(path);
                    break;

                default:
                    //大小王固定音效
                    if (rfa.CARD_TYPE.SINGLE_CARD) {
                        var cardId = cp1.getKeyValue();
                        if (cardId == rfa.CONSTANTS.BLACK_JOKER_ID || cardId == rfa.CONSTANTS.RED_JOKER_ID) {
                            var path = this.getPathByCardPattern(cp1, sexType);
                            play(path);
                            return;
                        }
                    }

                    if (pos2 == null || pos1 == pos2) {
                        var path = this.getPathByCardPattern(cp1, sexType);
                        play(path);
                    }
                    else {
                        //打队友
                        if (this.isTeammate(pos1, pos2)) {
                            this.playNormalBiggerSound(cp1, sexType);
                        }
                        else {
                            if (this.isBiggest(cp1)) {
                                this.playBiggerSound(3, sexType);
                            }
                            else {
                                var cardNum1 = rfa.utils.getCardNumber(cp1.getKeyValue());
                                var cardNum2 = rfa.utils.getCardNumber(cp2.getKeyValue());
                                if (cardNum1 - cardNum2 == 1) {
                                    this.playBiggerSound(2, sexType);
                                }
                                else {
                                    this.playNormalBiggerSound(cp1, sexType);
                                }
                            }
                        }
                    }
                    break;
            }

        }

        export function playNormalBiggerSound(cp, sexType) {
            if (Math.random() > 0.7)
                this.playBiggerSound(1, sexType);
            else {
                var path = this.getPathByCardPattern(cp, sexType);
                play(path);
            }
        }

        export function playBiggerSound(biggerType, sexType) {
            var path = "sound/doudizhu/player/bigger{0}_{1}.mp3".format(biggerType, sexType);
            play(path);
        }

        export function isBiggest(cp) {
            var type = cp.getType();
            var num = rfa.utils.getCardNumber(cp.getKeyValue());
            switch (type) {
                case rfa.CARD_TYPE.SINGLE_CARD:
                case rfa.CARD_TYPE.PAIR:
                    return num == 15;

                default:
                    return num == 14;

            }
        }

        export function getPathByCardPattern(cp, sexType) {
            var path = null;
            switch (cp.getType()) {
                case rfa.CARD_TYPE.SINGLE_CARD:
                    path = "sound/doudizhu/player/single/{0}_{1}.mp3".format(cp.getKeyValue().charAt(0), sexType);
                    break;

                case rfa.CARD_TYPE.PAIR:
                    path = "sound/doudizhu/player/double/{0}_{1}.mp3".format(cp.getKeyValue().charAt(0), sexType);
                    break;

                case rfa.CARD_TYPE.TRIPLET:
                    path = "sound/doudizhu/player/triplet_{0}.mp3".format(sexType);
                    break;

                case rfa.CARD_TYPE.TRIPLET_WITH_ONE:
                    path = "sound/doudizhu/player/triplet1_{0}.mp3".format(sexType);
                    break;

                case rfa.CARD_TYPE.TRIPLET_WITH_TWO:
                    path = "sound/doudizhu/player/triplet2_{0}.mp3".format(sexType);
                    break;

                case rfa.CARD_TYPE.SEQUENCE:
                    path = "sound/doudizhu/player/sequence_{0}.mp3".format(sexType);
                    break;

                case rfa.CARD_TYPE.SEQUENCE_OF_PAIRS:
                    path = "sound/doudizhu/player/sequence2_{0}.mp3".format(sexType);
                    break;

                case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS:
                case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_ONE:
                case rfa.CARD_TYPE.SEQUENCE_OF_TRIPLETS_WITH_TWO:
                    path = "sound/doudizhu/player/plane_{0}.mp3".format(sexType);
                    break;

                case rfa.CARD_TYPE.QUADPLEX_SET_WITH_ONE:
                    path = "sound/doudizhu/player/quadplex21_{0}.mp3".format(sexType);
                    break;

                case rfa.CARD_TYPE.QUADPLEX_SET_WITH_TWO:
                    path = "sound/doudizhu/player/quadplex22_{0}.mp3".format(sexType);
                    break;

                case rfa.CARD_TYPE.BOMB:
                    path = "sound/doudizhu/player/bomb_{0}.mp3".format(sexType);
                    break;

                case rfa.CARD_TYPE.ROCKET:
                    path = "sound/doudizhu/player/rocket_{0}.mp3".format(sexType);
                    break;

            }

            return path;
        }

        export function getSexType(pos) {
            return Method.getPlayer(pos)["sex"] == 2 ? "w" : "m";
        }

        export function isTeammate(pos1, pos2) {
            return Method.getPlayer(pos1).isDealer == Method.getPlayer(pos2).isDealer;
        }


        export function playPassSound(pos) {
            var sexType = this.getSexType(pos);
            var random = Math.random() > 0.5 ? 1 : 2;
            var path = "sound/doudizhu/player/pass{0}_{1}.mp3".format(random, sexType);
            play(path);
        }

        export function playLeftCardSound(pos, type) {
            var sexType = this.getSexType(pos);
            var path = "sound/doudizhu/player/last{0}_{1}.mp3".format(type, sexType);
            play(path);
        }

        export function playCDSound() {
            // var path = "sound/doudizhu/normal/countdown.mp3";
            // play(path);
            play("sound/mahjong/timer_normal.mp3");
        }

        export function playCallDealer(pos, operate) {
            var sexType = this.getSexType(pos);
            var call = operate == 1 ? "call" : "no_call";
            var path = "sound/doudizhu/player/rob/{0}_{1}.mp3".format(call, sexType);
            play(path);
        }

        export function playCallScore(pos, score) {
            var sexType = this.getSexType(pos);
            var path = "sound/doudizhu/player/rob/score{0}_{1}.mp3".format(score, sexType);
            play(path);
        }

        export function playRobLandlord(pos, operate) {
            var sexType = this.getSexType(pos);
            var rob = operate == 1 ? "rob" : "no_rob";
            var path = "sound/doudizhu/player/rob/{0}_{1}.mp3".format(rob, sexType);
            play(path);
        }

        export function clickCard() {
            var path = "sound/doudizhu/normal/click_card.mp3";
            play(path);
        }

        export function playRocket(pos) {
            var sexType = this.getSexType(pos);
            var path = "sound/doudizhu/player/rocket_{0}.mp3".format(sexType);
            play(path);
        }

        export function playBomb() {
            var path = "sound/doudizhu/player/bomb.mp3";
            play(path);
        }

        export function playVoiceBomb(pos) {
            var sexType = this.getSexType(pos);
            let path = "sound/doudizhu/player/bomb_{0}.mp3".format(sexType);
            play(path);
        }

        export function playPlaneEngine() {
            var path = "sound/doudizhu/player/plane_engine.mp3";
            play(path);
        }

        export function playInvalidSet() {
            var path = "sound/doudizhu/normal/invalid_set.mp3";
            play(path);
        }

        export function playDealCard() {
            var path = "sound/doudizhu/normal/fapai.mp3";
            play(path);
        }

    }
}