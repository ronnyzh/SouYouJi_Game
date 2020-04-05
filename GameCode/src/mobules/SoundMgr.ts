
module SoundMgr {

    export let ROOT_PATH = 'res/';
    export let MUSIC_PATH = ROOT_PATH+'music/';
    export let SOUND_PATH = ROOT_PATH+'sound/';

    export let MAHJONG_PATH = 'mahjong/';

    export let EXTEND_NAME = ".mp3";
    export let EXTEND_NAME_SOUND = ".mp3"; //.wav

    var current_music:string = "";

    var map: { [key: string]: string; } = {}

    export function initResPath()
    {
        ROOT_PATH =  ResourceMgr.RES_PATH;
        MUSIC_PATH = ROOT_PATH+'music/';
        SOUND_PATH = ROOT_PATH+'sound/';
    }

    export function rePlayMusic()
    {
        if(current_music.length>0)
        {
            //Laya.SoundManager.playSound(SOUND_PATH+"active_sound"+EXTEND_NAME);
            Laya.timer.once(200,this,function()
            {
                Laya.SoundManager.playMusic(current_music);
            });
        }
        else
        {
            playMusic();
        }
    }

    export function playMusic(name = 'bg' + SoundMgr.EXTEND_NAME) {
        var n = name;
        if (map[name] == null) {
            n = name.substring(0, name.lastIndexOf(".")) + EXTEND_NAME;
            map[name] = n;
        }
        else {
            n = map[name];
        }
        current_music = MUSIC_PATH + n;

        if(ExtendMgr.inst.isCanPlayMusicAndSound())
            Laya.SoundManager.playMusic(current_music);
        else
            console.log('play music warning');
    }

    export function playBGM(name) {
        var n = name;
        if (map[name] == null) {
            n = name.substring(0, name.lastIndexOf(".")) + EXTEND_NAME;
            map[name] = n;
        }
        else {
            n = map[name];
        }
        current_music = SOUND_PATH + n;
        if(ExtendMgr.inst.isCanPlayMusicAndSound())
            Laya.SoundManager.playMusic(current_music);
        else
            console.log('play music warning');
    }

    export function playEffect(name) {

        if(Laya.SoundManager.soundVolume == 0)
        {
            //new Laya.Handler(caller, callback).run();
            return;
        }

        var n = name;
        var new_name = name.substring(0, name.lastIndexOf("."));
        if (map[name] == null) {
            n = new_name + EXTEND_NAME_SOUND;
            map[name] = n;
        }
        else {
            n = map[name];
        }
        
        if(ExtendMgr.inst.player_switch_on)
            ExtendMgr.inst.playSound(n);
        else
        {
            var src = SOUND_PATH + n;
            if(ExtendMgr.inst.isCanPlayMusicAndSound(new_name))
                Laya.SoundManager.playSound(src);
            else
                console.log('play effect warning');
        }  
    }

    export function playSoundABS(name, caller?, callback? ,isAdaptLanguage = true) 
    {
        callback = callback || function () { };
        caller = caller || this;
        
        if(Laya.SoundManager.soundVolume == 0)
        {
            //new Laya.Handler(caller, callback).run();
            return;
        }

        var n:string = name;
        if (map[name] == null) {
            n = name.substring(0, name.lastIndexOf(".")) + EXTEND_NAME_SOUND;
            map[name] = n;
        }
        else {
            n = map[name];
        }

        if(ExtendMgr.inst.player_switch_on)
            ExtendMgr.inst.playSound(n);
        else
        {
            var newpath = n;
            var subpath = "/sound/";

            if(isAdaptLanguage)
            {
                switch(ExtendMgr.inst.lan)
                {
                    case ExtendMgr.EN:
                        subpath = "/sound_en/";
                        newpath = n.replace("/sound/",subpath)
                    break;
                    case ExtendMgr.CN:
                        subpath = "/sound/";
                    break;
                }
            }

            var new_name = name.substring(name.lastIndexOf(subpath)+subpath.length, name.lastIndexOf("."));
            if(ExtendMgr.inst.isCanPlayMusicAndSound(new_name))
                Laya.SoundManager.playSound(newpath, 1, new Laya.Handler(caller, callback));
            else
                console.log('play effect warning');
        }
    }

    export function playMusicABS(name, caller?, callback?) {
        var n = name;
        if (map[name] == null) {
            n = name.substring(0, name.lastIndexOf(".")) + EXTEND_NAME;
            map[name] = n;
        }
        else {
            n = map[name];
        }
        current_music = n;
        if(ExtendMgr.inst.isCanPlayMusicAndSound())
            Laya.SoundManager.playMusic(current_music);
        else
            console.log('play music warning');
    }

    export function stopAllEffects() {
        Laya.SoundManager.stopAllSound();
        ExtendMgr.inst.stopSound();
    }

    export function stopMusic() {
        Laya.SoundManager.stopMusic();
    }

    export function getSexPath(sex) 
    {
        if(ExtendMgr.inst.player_switch_on)
            return "boy";
        else
            return sex != 2 ? "boy" : "girl";
    }

    //-----------------------MAHJONG----------------------    
    export function discardTile(tileId, sex = 0) {
        if (!tileId) return;
        this.playSexEffect("/tile_" + tileId + ".mp3", sex);
    }

    export function playSexEffect(name, sex = 0) {
        this.playMJEffect(this.getSexPath(sex) + "/" + name);
    }

    export function playMJEffect(path) {
        try {
            this.playEffect(MAHJONG_PATH + path);
        } catch (error) { console.log(error); }
    }

    export function clickButton() {
        this.playMJEffect("button.mp3");
    }
    export function fallTile() {
        this.playMJEffect("tile_fall.mp3");
    }
    export function layTiles() {
        this.playMJEffect("tile_impact.mp3");
    }
    export function drawTile() {
        this.playMJEffect("tile_draw.mp3");
    }
    export function drawn() {
        this.playMJEffect("drawn.mp3");
    }
    export function win() {
        this.playMJEffect("win.mp3");
    }
    export function lose() {
        this.playMJEffect("lose.mp3");
    }
    export function countdown() {
        this.playMJEffect("timer_normal.mp3");
    }
    export function rollDice() {
        this.playMJEffect("roll_dice.mp3");
    }
    export function clickcard() {
        this.playMJEffect('clickcard.mp3');
    }
    export function li_pai() {
        this.playMJEffect('li_pai.mp3');
    }

    export function pong(sex = 0) {
        this.playSexEffect("pong.mp3", sex);
    }
    export function kong(sex = 0) {
        this.playSexEffect("kong.mp3", sex);
    }
    export function hu_origin(sex = 0) {
        this.playSexEffect("hu_origin.mp3", sex);
    }
    export function hu(sex = 0) {
        this.playSexEffect("hu.mp3", sex);
    }
    export function chow(sex = 0) {
        this.playSexEffect("chow.mp3", sex);
    }
}

module SoundMgrNiu {
    export let SND_PATH = 'niuniu/';

    export function playEffect(path) {
        SoundMgr.playEffect(SND_PATH + path);
    }

    export function getSexPath(sex) {
        return SoundMgr.getSexPath(sex);
    }

    export function playNiuEffect(nType, sex) {
        this.playEffect("niu_{0}_{1}.mp3".format(nType, this.getSexPath(sex)));
    }

    export function playSGEffect(nType) {
        if (parseInt(nType) < 10)
            this.playEffect("sg/point_{0}.mp3".format(nType));
        else
            this.playEffect("sg/gong.mp3");
    }

    export function gameStart() {
        this.playEffect("gamestart.mp3");
    }
    export function startBidGame() {
        this.playEffect("startBid.mp3");
    }
    export function startQiang() {
        this.playEffect("startQiang.mp3");
    }
    export function flyGold() {
        this.playEffect("flyGold.mp3");
    }

    export function dingzhuang() {
        this.playEffect("dingzhuang.mp3");
    }

    export function playSexEffect(name, sex = 0) {
        this.playEffect(this.getSexPath(sex) + "/" + name);
    }

    export function qiang(num, sex = 0) {
        var path = 'qiang{0}.mp3'.format(num);
        this.playSexEffect(path, sex);
    }
    export function xia(num, sex = 0) {
        if (num > 5) return;
        var path = 'xia{0}.mp3'.format(num);
        this.playSexEffect(path, sex);
    }
    export function actionFinish() {
    this.playEffect("au_game_actionFinish.mp3");
    }

    export function pokerHit() {
    this.playEffect("au_poker_hit.mp3");
    }    
}

module SoundMgrNiuJD {
    export let SPD_PATH = 'niuniuJD/';

    export function playEffect(path) {
        SoundMgr.playEffect(SPD_PATH + path);
    }

    export function getSexPath(sex) {
        return SoundMgr.getSexPath(sex);
    }


    export function playSexEffect(name, sex = 0) {
        // console.log(name, "==========name");
        // console.log(sex, "=========sex");
        // console.log(this.getSexPath(sex) + "/" + name, "=========");
        this.playEffect(this.getSexPath(sex) + "/" + name);
    }

    export function qiang(num, sex = 0) {
        var path = 'banker{0}.mp3'.format(num);
        this.playSexEffect(path, sex);
    }
    export function xia(num, sex = 0) {
        var path = 'bei{0}.mp3'.format(num);
        this.playSexEffect(path, sex);
    }

    export function fapai() {
        this.playEffect("fapai.mp3");
    }
}
module SoundMgrShiSanShui {
    export let SPD_PATH = "shisanshui/";
    // export function palyEffect(path) {
    // SoundMgr.playEffect(SPD_PATH + path);
    //  }
    export function getSexPath(sex) {
        return SoundMgr.getSexPath(sex);
    }
    export function playSexEffect(name, sex) {
        SoundMgr.playEffect(SPD_PATH + this.getSexPath(sex) + "/" + name);
    }
    export function Type(num, sex) {
        if (num <= 10) {
            if (num == 4)
                return;
            // this.playEffect(this.getSexPath(sex) + "/" + "common" + num);
            let path = "common{0}.ogg".format(num);
            this.playSexEffect(path, sex);
        } else {
            if (sex == 1 && (num == 19 || num == 23))
                sex = 0;
            let path = "special{0}.ogg".format(num);
            this.playSexEffect(path, sex);
            //this.playEffect(this.getSexPath(sex) + "/" + "special" + num);
        }
    }
    export function compare(sex = 0) {
        this.playSexEffect("start_compare.ogg", sex);
    }
    export function gameStart() {
        SoundMgr.playEffect(SPD_PATH + "gamestart.ogg");
    }
    export function ready() {
        SoundMgr.playEffect(SPD_PATH + "poker_ready.ogg");
    }
    export function click() {
        SoundMgr.playEffect(SPD_PATH + "poker_click.ogg");
    }
    export function time() {
        SoundMgr.playEffect(SPD_PATH + "room_timer.ogg");
    }
    export function playenter() {
        SoundMgr.playEffect(SPD_PATH + "drawer_open_1.ogg");
    }
    export function playout() {
        SoundMgr.playEffect(SPD_PATH + "drawer_open_2.ogg");
    }
    export function flyGold() {
        SoundMgr.playEffect(SPD_PATH + "flyGold.ogg");
    }
      export function shoot() {
        SoundMgr.playEffect(SPD_PATH + "daqiang3.ogg");
    }
}

module SoundMgrPoint {
    export let SND_PATH = 'point/';

    export function playEffect(path) {
        SoundMgr.playEffect(SND_PATH + path);
    }

    export function getSexPath(sex) {
        return SoundMgr.getSexPath(sex);
    }

    export function playPointEffect(pType, sex) {
        this.playEffect("{0}/point_{1}.mp3".format(this.getSexPath(sex), pType));
    }
}

module SoundMgrDeZhou {
    export let SND_PATH = 'dezhou/';

    let CardTypeMap = {
        [0]: 'cardtype_hulu',
        [1]: 'cardtype_jingang',
        [2]: 'cardtype_tonghua',
        [3]: 'cardtype_huangjiatonghua',
    }

    let actionMap = {
        [1]: 'call',
        [2]: 'raise',
        [3]: 'allin',
        [4]: 'check',
        [5]: 'fold',
    }

    export function playEffect(path) {
        console.log('playEffect', SND_PATH + path);
        SoundMgr.playEffect(SND_PATH + path);
    }

    export function getSexPath(sex) {
        return SoundMgr.getSexPath(sex);
    }

    export function playSexEffect(name, sex = 0) {
        this.playEffect(this.getSexPath(sex) + "/" + name);
    }

    export function addchip() {
        this.playEffect("addchip.mp3");
    }

    export function allin_effect() {
        this.playEffect("allin_effect.mp3");
    }

    export function button() {
        this.playEffect("button.mp3");
    }

    export function cardtype(type: number) {
        this.playEffect(CardTypeMap[type]);
    }

    export function action(action: number, sex: number) {
        let path = actionMap[action] + SoundMgr.EXTEND_NAME;
        this.playSexEffect(path, sex);
    }

    export function chip() {
        this.playEffect("chip.mp3");
    }

    export function chipfly() {
        this.playEffect("chipfly.mp3");
    }

    export function fapai() {
        this.playEffect("fapai.mp3");
    }

    export function foldpai() {
        this.playEffect("foldpai.mp3");
    }

    export function gold() {
        this.playEffect("gold.mp3");
    }

    export function half_time() {
        this.playEffect("half_time.mp3");
    }

    export function sit() {
        this.playEffect("sit.mp3");
    }

    export function time() {
        this.playEffect("time.mp3");
    }

    export function playBGM() {
        SoundMgr.playMusic('bgm_dezhou.mp3');
    }
}