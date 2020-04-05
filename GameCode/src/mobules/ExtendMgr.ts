class ExtendMgr {
    private static _inst: ExtendMgr = null;

    public static LastSelectGameIdKey: string = 'last_select_gameId';
    public static OnMinGameLoadingProgress = 'OnMinGameLoadingProgress';

    public static CN: string = 'cn';
    public static EN: string = 'en';


    public multiLanguageTextMap: JSON;
    public lan: string = ExtendMgr.CN;
    public uipath: string = '';

    //
    public VersionStr: string = '版本';
    public PreloadingPageLoadingString: string = '玩命加载中... ';
    public PreloadingUnzipString: string = '整理中...';

    public NetCheckPingAlert: string = "网络状态不稳定或长时间没通信";
    public OnConnectError: string = '游戏网络连接失败，请稍后再进';
    public OnNetWorkError: string = '网络异常，请检查您的网络是否畅顺?';
    public DisconnectAlert: string = '网络连接断开,是否重新连接';
    public DissolveNoticeMin: string = '分';
    public DissolveNoticeSec: string = '秒后房间将自动解散';
    public NotEnoughMoney: string = '您携带的金额不足以进入本场次游戏，请充值后进入。';
    public NotGameData: string = '没有匹配场次数据';
    public SwitchGameFail1: string = '你正在其他游戏场次中,是否立刻进入游戏？';
    public SwitchGameFail2: string = '无法加入场次';

    public PresetGoldNotEnough: string = '携带金额不能大于总额';

    public OnChangeLanguageFail: string = '当前语言己经是';
    public OnChangeLanguage: string = '是否把当前语言切换为';
    //

    //moudles name
    public MN_Lobby: string = '平台大厅';
    public MN_HongZhong: string = '红中麻将';
    public MN_ErRenMaJiang: string = '二人麻将';
    public MN_GuangDongJiDaHu: string = '广东麻将';
    public MN_MingPaiNiu: string = '明牌牛牛';
    public MN_QiangZhuangNiu: string = '抢庄牛牛';
    public MN_TongBiNiu: string = '通比牛牛';
    public MN_PaoDeKuai: string = '跑得快';
    public MN_DouDiZhu: string = '斗地主';
    public MN_XueLiu: string = '血流成河';

    public MN_SanGong: string = '三公';
    public MN_TongBiSanGong: string = '通比三公';
    public MN_21Dian: string = '决战21点';
    public MN_ZhaJinHua: string = '炸金花';
    public MN_ShiSanShui: string = '十三水';
    public MN_DeZhou: string = '德州扑克';
    public MN_ErRenDouDiZhu: string = '二人斗地主';
    public MN_HuanLeNiu: string = '欢乐牛牛';
    public MN_BaoDian: string = '爆点百家乐';
    public MN_BaiJiaLe: string = '百家乐';
    //

    public static get inst(): ExtendMgr {
        if (ExtendMgr._inst == null) {
            ExtendMgr._inst = new ExtendMgr();
        }
        return ExtendMgr._inst;
    }

    public isShowProtoCmd: boolean = false;
    public oldAnimaEffect: boolean = true;

    public map: { [key: string]: string; } = {}

    ///////////////////////////////////////////////////////////////////
    public player_switch_on: boolean;
    public players: Array<HTMLAudioElement>;
    public audios: { [key: string]: HTMLAudioElement; } = {}
    public player_src: string;
    public player_mark: string;
    public player_cache_size: number;
    public player_playmode: boolean;
    public player_reload_sounds: HTMLScriptElement;
    public player_cache_gameid: number = 0;
    public player_cache_gameid_table: { [key: number]: Array<number>; } = {}

    private runCardsTemp: Array<string> = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K'];
    private mahjongActionsTemp: Array<string> = ['tile_draw', 'tile_fall', 'tile_impact', 'tile_out', 'tile_show', 'tile_up', 'roll_dice', 'win', 'lose',
        'boy/chow', 'boy/pong', 'boy/kong', 'boy/hu', 'boy/hu_origin', 'boy/flower'];
    private mahjongTilesTemp: Array<string> = ['boy/tile_a1', 'boy/tile_a2', 'boy/tile_a3', 'boy/tile_a4', 'boy/tile_a5', 'boy/tile_a6', 'boy/tile_a7', 'boy/tile_a8', 'boy/tile_a9',
        'boy/tile_b1', 'boy/tile_b2', 'boy/tile_b3', 'boy/tile_b4', 'boy/tile_b5', 'boy/tile_b6', 'boy/tile_b7', 'boy/tile_b8', 'boy/tile_b9',
        'boy/tile_c1', 'boy/tile_c2', 'boy/tile_c3', 'boy/tile_c4', 'boy/tile_c5', 'boy/tile_c6', 'boy/tile_c7', 'boy/tile_c8', 'boy/tile_c9',
        'boy/tile_d1', 'boy/tile_d5', 'boy/tile_d9', 'boy/tile_e1', 'boy/tile_e4', 'boy/tile_e6', 'boy/tile_e9'];
    ///////////////////////////////////////////////////////////////////
    /**原本的外部资源目录名对应fairygui的包名 */
    public tile_map =
        {
            555: ['pokers'],
            556: ['pokers'],
            557: ['pokers', 'pokerscards'],
            558: ['pokers'],
            559: ['pokersFTLpoker'],
            560: ['pokersFTLpoker'],
            561: ['pokersstyle1'],
            562: ['pokers'],
            563: ['pokers'],
            566: ['pokers'],
            445: ['MJtiles'],
            449: ['MJtiles'],
            452: ['MJtiles'],
            564: ['MJtiles'],
            570: ['pokersFTLpoker'],
            666: ['G666pokers'],
            548: ['G548pokers'],
            549: ['G548pokers']
        }

    public background_map =
        {
            555: 'bg1.jpg',
            556: 'bg2.jpg',
            557: 'bg4.jpg',
            558: 'bg2.jpg',
            559: 'bg4.jpg',
            560: 'bg2.jpg',
            561: 'table2.jpg',
            562: 'shisanshuibg.jpg',
            563: 'table3.jpg',
            566: 'table3.jpg',
            445: 'main_bg0.jpg',
            449: 'main_bg1.jpg',
            452: 'main_bg0.jpg',
            564: 'main_bg0.jpg',
            570: 'bg2.jpg',
            666: 'bg7.jpg',
            548: 'bg6.jpg',
            549: 'bg6.jpg',
            565: 'bg5.jpg'
        }
    ///////////////////////////////////////////////////////////////////
    public fui: { [key: string]: fairygui.UIPackage; } = {}

    private preloadingBar: fairygui.GComponent;
    private preloadingBarInCycle: fairygui.GObject;
    private preloadingBarOutCycle: fairygui.GObject;
    private preloadingRotaTargetValue: number;

    private initConched: Boolean = false;
    private conch = null;
    private contex = null;
    private animation = null;

    //-----------------------------------------------------
    private onCheckPartySuccess;

    //-----------------------------------------------------

    private iosVersion;
    private iosDevice = 0;
    private igonelist;

    //testsound---
    private testsoundlist;
    private testindex = 0;

    /////////////////////////////////////////////////////////////
    public getScreenFullSize() {
        var ratio = Laya.stage.width / Laya.stage.height;
        var real_ratio = Laya.Browser.width > Laya.Browser.height ? Laya.Browser.width / Laya.Browser.height : Laya.Browser.height / Laya.Browser.width;
        var real_less = ratio > real_ratio;
        var real_w = real_less ? Laya.stage.width : Laya.stage.height * real_ratio;
        var real_h = real_less ? Laya.stage.width / real_ratio : Laya.stage.height;
        return [real_w, real_h];
    }

    public setBackgroundfull(name, url, bg, cb?) {
        var vec2 = this.getScreenFullSize();
        bg.name = name;
        bg.loadImage(url, 0, 0, vec2[0], vec2[1], cb);
    }

    /////////////////////////////////////////////////////
    public setLanguage(lan: string): void {
        var res_root = ResourceMgr.RES_PATH;
        switch (lan) {
            case 'cn':
            case 'CN':
                this.lan = 'cn';
                SoundMgr.SOUND_PATH = res_root + 'sound/';
                break;

            case 'en':
            case 'EN':
                this.lan = 'en';
                SoundMgr.SOUND_PATH = res_root + 'sound_en/';
                break;

            default:
                this.lan = ExtendMgr.CN;
                SoundMgr.SOUND_PATH = res_root + 'sound/';
                break;
        }

        if (this.lan != ExtendMgr.CN) {
            this.VersionStr = this.getText4Language(this.VersionStr);
            this.PreloadingUnzipString = this.getText4Language(this.PreloadingUnzipString);
            this.PreloadingPageLoadingString = this.getText4Language(this.PreloadingPageLoadingString);
            this.NetCheckPingAlert = this.getText4Language(this.NetCheckPingAlert);
            this.OnConnectError = this.getText4Language(this.OnConnectError);
            this.OnNetWorkError = this.getText4Language(this.OnNetWorkError);
            this.DisconnectAlert = this.getText4Language(this.DisconnectAlert);
            this.DissolveNoticeMin = this.getText4Language(this.DissolveNoticeMin);
            this.DissolveNoticeSec = this.getText4Language(this.DissolveNoticeSec);
            this.NotEnoughMoney = this.getText4Language(this.NotEnoughMoney);
            this.NotGameData = this.getText4Language(this.NotGameData);
            this.SwitchGameFail1 = this.getText4Language(this.SwitchGameFail1);
            this.SwitchGameFail2 = this.getText4Language(this.SwitchGameFail2);
            this.PresetGoldNotEnough = this.getText4Language(this.PresetGoldNotEnough);
            this.OnChangeLanguageFail = this.getText4Language(this.OnChangeLanguageFail);
            this.OnChangeLanguage = this.getText4Language(this.OnChangeLanguage);
            //
            //moudles name
            this.MN_Lobby = this.getText4Language(this.MN_Lobby);
            this.MN_HongZhong = this.getText4Language(this.MN_HongZhong);
            this.MN_ErRenMaJiang = this.getText4Language(this.MN_ErRenMaJiang);
            this.MN_GuangDongJiDaHu = this.getText4Language(this.MN_GuangDongJiDaHu);
            this.MN_MingPaiNiu = this.getText4Language(this.MN_MingPaiNiu);
            this.MN_QiangZhuangNiu = this.getText4Language(this.MN_QiangZhuangNiu);
            this.MN_PaoDeKuai = this.getText4Language(this.MN_PaoDeKuai);
            this.MN_DouDiZhu = this.getText4Language(this.MN_DouDiZhu);
            this.MN_XueLiu = this.getText4Language(this.MN_XueLiu);
            this.MN_SanGong = this.getText4Language(this.MN_SanGong);
            this.MN_21Dian = this.getText4Language(this.MN_21Dian);
            this.MN_ZhaJinHua = this.getText4Language(this.MN_ZhaJinHua);
            this.MN_ShiSanShui = this.getText4Language(this.MN_ShiSanShui);
            this.MN_DeZhou = this.getText4Language(this.MN_DeZhou);
            this.MN_ErRenDouDiZhu = this.getText4Language(this.MN_ErRenDouDiZhu);
            this.MN_HuanLeNiu = this.getText4Language(this.MN_HuanLeNiu);
            this.MN_BaoDian = this.getText4Language(this.MN_BaoDian);
            this.MN_BaiJiaLe = this.getText4Language(this.MN_BaiJiaLe);
        }
    }

    getText4Language(content): string {
        if (this.lan == ExtendMgr.CN)
            return content;

        return this.multiLanguageTextMap[content] || content;
    }

    /////////////////////////////////////////////////////
    checkIOSVersionAndDevice(callback) {
        var agent = navigator.userAgent;
        if ((agent.match(/iPhone/i) || agent.match(/iPod/i))) {
            for (var i = 4; i <= 11; i++) {
                var key = "iPhone OS " + i + "_";
                if (agent.indexOf(key) >= 0) {
                    this.iosVersion = i;
                }
            }
        }
        else {
            this.iosVersion = -1;
        }

        //fairy gui///////////////////////////
        if (this.iosVersion > 0 && this.iosVersion < 9) {
            fairygui.UIConfig.buttonSoundVolumeScale = 0;
        }
        /////////////////////////////

        if (screen.height == 812 && screen.width == 375) {
            this.iosDevice = 10;
        } else if (screen.height == 736 && screen.width == 414) {
            //console.log("iPhone7P - iPhone8P - iPhone6");
            this.iosDevice = 7;
        } else if (screen.height == 667 && screen.width == 375) {
            //console.log("iPhone7 - iPhone8 - iPhone6");
            this.iosDevice = 6;
        } else if (screen.height == 568 && screen.width == 320) {
            //console.log("iPhone5");
            this.iosDevice = 5;
        } else {
            //console.log("iPhone4");
            this.iosDevice = 4;
        }
    }

    getIOSVersion() {
        return this.iosVersion;
    }

    getIPhoneModel() {
        return this.iosDevice;
    }

    getDevice() {
        var device = "UNkNOWN";
        if (laya.utils.Browser.onAndriod) {
            device = "Android";
        }
        else if (laya.utils.Browser.onIPhone) {
            device = "IPhone";
        }
        else if (laya.utils.Browser.onIPad) {
            device = "IPad";
        }
        else if (laya.utils.Browser.onPC) {
            device = "PC";
        }
        else if (laya.utils.Browser.onMac) {
            device = "Mac";
        }

        var browser = "UNkNOWN";
        if (laya.utils.Browser.onIE) {
            browser = "ie";
        }
        else if (laya.utils.Browser.onEdge) {
            browser = "edge";
        }
        else if (laya.utils.Browser.onSafari) {
            browser = "safari";
        }
        else if (laya.utils.Browser.onFirefox) {
            browser = "firefox";
        }
        else if (laya.utils.Browser.onMQQBrowser) {
            browser = "MQQBrowser";
        }

        return device + ',' + browser;
    }

    //////////////////////////////////////////////////////////////////
    setDesignResolution() {
        if (ExtendMgr.inst.getIOSVersion() == 10)
            bk.setDesignResolution(2436, 1125);
        else
            bk.setDesignResolution(1334, 750);
    }

    //////////////////////////////////////////////////////////////////

    isCanPlayMusicAndSound(src = '') {
        /*
        var iversion = this.getIOSVersion();

        if(iversion<0) return true;

        var can = !(iversion>0 && iversion<9);

        if(can && src.length>0) 
        {
            if(this.getIPhoneModel() > 5)
            {
                var has = this.igonelist.indexOf(src)>=0;
                can = !has;
            }
        }
        
        return can;
        */
        return true;
    }

    ////////////////////////////////////////////////////////////////////
    preloadResources(callback) {
        this.preloadLoaded(callback);
    }

    preloadLoaded(callback) {
        fairygui.UIPackage.addPackage(this.uipath + '/GALL');
        fairygui.UIPackage.addPackage(this.uipath + '/GBP');
        fairygui.UIPackage.addPackage(this.uipath + '/Effect');
        fairygui.UIPackage.addPackage(this.uipath + '/Test');
        callback();
    }

    //load image and decode
    liad(urls: any, cb: any, onProgress: any = null) {
        var extend_name: string = 'png';
        var buf_name: string = 'buf';
        var _t: string = TestMgr.IS_DECODE ? Loader.BUFFER : Loader.IMAGE;
        var res = [];
        var count: number = urls.length;

        if (_t == Loader.BUFFER) {
            for (var i: number = 0; i < count; i++) {
                var _url: string = urls[i].replace(extend_name, buf_name);
                res.push({ url: _url, type: _t });
            }
        }
        else {
            for (var i: number = 0; i < count; i++) {
                res.push({ url: urls[i], type: _t });
            }
        }

        var decode = function (curr: number): void {
            if (onProgress) {
                onProgress.caller.onProgress(curr / urls.length * 100, ExtendMgr.inst.PreloadingUnzipString);
            }

            if (curr < urls.length) {
                FuiSourceMgr.inst.deTex(urls[curr], function () {
                    decode(curr + 1);
                }.bind(this), extend_name);
            }
            else
                cb();
        }

        Laya.loader.load(res, Handler.create(this, function () {
            if (_t == Loader.BUFFER)
                decode(0);
            else if (cb)
                cb();
        }.bind(this)), onProgress);
    }

    /////////////////////////////////////////////////////////////////////
    loadTileRes(gameid: number, cb: () => void, uipath = 'ui') {
        let map = this.tile_map;
        if (map[gameid]) {
            let resMap = [];
            let imgMap = [];
            let len = 0;
            for (let i = 0; i < map[gameid].length; i++) {
                const pkgName = map[gameid][i];
                resMap[pkgName] = [{ url: ResourceMgr.RES_PATH + uipath + '/' + pkgName + '.fui', type: Loader.BUFFER }];
                imgMap.push(ResourceMgr.RES_PATH + uipath + '/' + pkgName + '@atlas0.png');
                len++;
            }

            let index = 0;
            if (len > 0) {
                this.liad(imgMap, () => {
                    for (const pkgName in resMap) {
                        if (resMap.hasOwnProperty(pkgName)) {
                            const res = resMap[pkgName];

                            Laya.loader.load(res, Handler.create(this, (pkgName) => {
                                this.fui[pkgName] = fairygui.UIPackage.addPackage(ResourceMgr.RES_PATH + uipath + '/' + pkgName);
                                index++;
                                //console.log('index, len', index, len);
                                if (index == len) {
                                    cb();
                                }
                            }, [pkgName]));
                        }
                    }
                });
            }
            else {
                cb();
            }
        }
        else {
            console.log('map没有这个gameid', gameid);
            cb();
        }
    }

    showMinGameSourcePreload() {
        if (!this.preloadingBar) {
            //super('Basic','PreLoading',UILayer.GAME);
            this.preloadingBar = fairygui.UIPackage.createObject('Basic', 'PreLoading').asCom;
            this.preloadingBarInCycle = this.preloadingBar.getChild('n20');
            this.preloadingBarOutCycle = this.preloadingBar.getChild('n19');
            //this.preloadingBar.getChild('bg').asLoader.url = "ui://Basic/mini2";
            this.preloadingBar.getChild('bg').visible = false;
            //ui://la8oslyom01xlc en
            //ui://la8oslyory34lj cn
            var vec2 = this.getScreenFullSize();
            this.preloadingBar.width = vec2[0];
            this.preloadingBar.height = vec2[1];
        }
        this.preloadingBar.center();
        fairygui.GRoot.inst.addChild(this.preloadingBar);
    }

    updateMinGameSourcePreload(value: number) {
        if (this.preloadingBarInCycle) {
            this.preloadingRotaTargetValue = value * 360;
            var v = (this.preloadingRotaTargetValue - this.preloadingBarInCycle.rotation) * 0.6;
            this.preloadingBarInCycle.rotation += v;
            this.preloadingBarOutCycle.rotation -= v;
        }
    }

    updateMinGameSourcePreload2() {
        if (this.preloadingBarInCycle) {
            this.preloadingBarInCycle.rotation += 1;
            this.preloadingBarOutCycle.rotation -= 1;
        }
    }

    hideMinGameSourcePreload() {
        setTimeout(function () {
            fairygui.GRoot.inst.removeChild(this.preloadingBar);
            this.preloadingBar = null;
            this.preloadingBarInCycle = null;
            this.preloadingBarOutCycle = null;
        }.bind(this), 200);
    }

    /////////////////////////////////////////////////////////////////////
    createUserIconMasker(gcom: fairygui.GComponent, maskComName: string, localx, localy) {
        var masker: UserIconMasker = new UserIconMasker();
        masker.setGCom(gcom, maskComName, localx, localy);
        return masker;
    }

    //////////////////////////////////////////////////////////////////////
    private hot_rota_anima_temp_index = -1;
    startHotAnima(list) {
        if (this.hot_rota_anima_temp_index != -1) {
            return;
        }
        Laya.timer.loop(2200, this, this.startHotGameIcon, [list]);
    }

    startHotGameIcon(...arg) {
        var list: fairygui.GList = arg[0];
        if (this.hot_rota_anima_temp_index != -1) {
            this.stopHotGameIcon(list);
        }
        this.hot_rota_anima_temp_index = Tools.inst.randomInt(0, 2);
        var childindex = list.itemIndexToChildIndex(this.hot_rota_anima_temp_index);
        list.getChildAt(childindex).asCom.getTransition('t0').play();
    }

    stopHotGameIcon(list) {
        if (this.hot_rota_anima_temp_index != -1) {
            var childindex = list.itemIndexToChildIndex(this.hot_rota_anima_temp_index);
            list.getChildAt(childindex).asCom.getTransition('t0').stop();
        }
        this.hot_rota_anima_temp_index = -1;
    }

    stopHotAnima(list) {
        Laya.timer.clearAll(this);
        this.stopHotGameIcon(list);
    }

    //////////////////////////////////////////////////////////////////////
    private spark_temp_index = -1;
    startflashGamesublist(list) {
        if (this.spark_temp_index != -1) {
            return;
        }
        Laya.timer.loop(3000, this, this.startSparkSubGameIcon, [list]);
    }

    startSparkSubGameIcon(...arg) {
        var list = arg[0];
        if (this.spark_temp_index != -1) {
            this.stopSparkSubGameIcon(list);
        }
        this.spark_temp_index = Tools.inst.randomInt(0, list.numChildren - 1);
        var mc: fairygui.GMovieClip = list.getChildAt(this.spark_temp_index).getChild("Ani_flash").asMovieClip;
        mc.playing = true;
        Laya.timer.frameOnce(14, this, function () {
            if (mc != null) {
                mc.playing = false;
                mc.frame = 13;
            }
        });
    }

    stopSparkSubGameIcon(list) {
        var mc: fairygui.GMovieClip = list.getChildAt(this.spark_temp_index).getChild("Ani_flash").asMovieClip;
        mc.playing = false;
        mc.frame = 13;
    }

    stopFlashGamesublist(list) {
        Laya.timer.clearAll(this);
        //Laya.timer.clear(this,this.startSparkSubGameIcon);
        if (this.spark_temp_index == -1) {
            return;
        }
        var mc: fairygui.GMovieClip = list.getChildAt(this.spark_temp_index).getChild("Ani_flash").asMovieClip;
        if (mc != null) {
            mc.playing = false;
            mc.frame = 13;
        }
        this.spark_temp_index = -1;
    }

    //////////////////////////////////////////////////////////////////////
    createParticle2Fairygui(id = "0", src = "particle.part", x = 0, y = 0, parent = null, callback = null) {
        /*
        if(!laya.particle.Particle2D) return null;

        let par: laya.particle.Particle2D = new laya.particle.Particle2D(null);
        function onAssetsLoaded(settings: laya.particle.ParticleSetting): void 
        {
            par.setParticleSetting(settings);
            par.emitter.start();
            par.emitter.emissionRate = 30;
            par.emitter.minEmissionTime = 0.5;
            par.play();

            if (parent == null)
                Laya.stage.addChild(par);
            else {
                var fairy_parent: fairygui.GComponent = parent;
                fairy_parent.displayObject.addChild(par);
            }

            //par.parent.setChildIndex(par,0);
            par.x = x;
            par.y = y;

            par.name = "Particle" + id;

            if (callback != null) {
                callback();
            }
        }
        Laya.loader.load(ResourceMgr.RES_PATH+"particle/" + src, Handler.create(this, onAssetsLoaded), null, Loader.JSON);
        */
        var par: nullParticle = new nullParticle();
        return par;
    }

    clearParticle(id = "0", parent = null) {
        /*
        let par: laya.particle.Particle2D = null;
        if (parent == null)
            par = Laya.stage.getChildByName("Particle" + id) as laya.particle.Particle2D;
        else {
            var fairy_parent: fairygui.GComponent = parent;
            if (fairy_parent != null)
                par = fairy_parent.displayObject.getChildByName("Particle" + id) as laya.particle.Particle2D;
            else
                par = parent.getChildByName("Particle" + id) as laya.particle.Particle2D;
        }

        if (par != null) {
            par.stop();
            par.parent.removeChild(par);
        }
        */
    }

    /////////////////////////////////////////////////////////////////////////////////////////////
    initConch() {
        if (this.initConched) return;

        this.conch = Laya.Browser.window.conch
        this.conch && this.conch.showAssistantTouch(false);
        this.contex = document.createElement('canvas').getContext('2d');

        if (this.conch && this.conch.setOnBackPressedFunction) {
            var hallpage = this;
            this.conch.setOnBackPressedFunction(() => {
                var anima = hallpage.animation;
                //恢复声音
                if (anima != null) {
                    SoundMgr.playMusic('bg.ogg');
                    window.cancelAnimationFrame(anima)
                    //Laya.Browser.window.conch.closeExternalLink();
                }
                else {
                    //Laya.Browser.window.conch.exit();
                }
            });

            this.initConched = true;
        }
    }

    loadExtendGame(gameid, ldmask) {
        if (!this.initConched) return;

        var ctx = this.contex;
        function render() {
            ctx.fillStyle = '#99d9ea';
            ctx.fillRect(0, 0, window.innerWidth, window.innerHeight);
            this.animation = window.requestAnimationFrame(render);
        }
        this.animation = window.requestAnimationFrame(render);

        if (this.conch) {
            var url: string = ExtendMgr.inst.map[gameid];
            if (url != null) {
                //var loadingmask = this.loadingC
                ldmask.setSelectedPage('show');

                Tools.inst.setTimeout(function () {
                    ldmask.setSelectedIndex(0);
                }, 3000);

                //暂停声音
                SoundMgr.stopMusic();

                //Laya.timer.loop(500, this, this.checkCanvasRender);

                //this.conch.setExternalLinkEx(url,0,0,window.innerWidth,window.innerHeight,false); //在按返回键时闪退
                this.conch.setExternalLinkEx(url, 0, 0, window.innerWidth, window.innerHeight, true);
            }
        }
    }

    checkStartGame(gameid, ldmask): boolean {
        switch (gameid) {
            case (gameid == 'w0000'):
            case (gameid == 'w0001'):
            case (gameid == 'w0002'):
            case (gameid == 'w0003'):
            case (gameid == 'w0004'):
            case (gameid == 'w0005'):
            case (gameid == 'w0006'):
            case (gameid == 'w0007'):
            case (gameid == 'w0008'):
                this.initConch();
                this.loadExtendGame(gameid, ldmask);
                return true;
        }
        return false;
    }

    ////////
    isShowPicHot(name) {
        return isHotGame(name); //(name == 'game449' || name == 'game555' || name == 'game556');
    }

    refreshGameListMembersNum(gameList, gameid2Data, serverStates): void {
        //var gameList = this._view.getChild('sub_game_list').asList;
        if (gameList != null && serverStates) {
            for (var i = 0; i < gameList.numChildren; ++i) {
                var child = gameList.getChildAt(i);
                var key_str = child.name;
                var key = key_str.substring(4, key_str.length);

                var openServer = serverStates[key];
                if (openServer) {
                    child.getChild('Pic_hot').visible = ExtendMgr.inst.isShowPicHot(child.name);
                    child.getChild('n6').visible = true;
                    child.getChild('Txt_online').visible = true;
                    child.getChild('Pic_lock').visible = false;
                    //child.getChild('icon').asLoader.color = '#ffffff';
                    child.getChild('icon').filters = null;
                    //child.getChild('icon').grayed = false;
                    child.touchable = true;

                    var arr = gameid2Data[key];

                    if (arr == null) {
                        continue;
                    }
                    var len = arr.length;
                    var total = 0;
                    for (var j = 0; j < len; ++j) {
                        total += arr[j].online;
                    }

                    var online = child.getChild('Txt_online').asLabel;
                    online.text = total.toString();
                }
                else {
                    child.getChild('Pic_hot').visible = false;
                    child.getChild('n6').visible = false;
                    child.getChild('Txt_online').visible = false;
                    child.getChild('Pic_lock').visible = true;

                    //child.grayed = true;
                    child.touchable = false;
                    //child.filters=[new laya.filters.ColorFilter([0.3086,0.6094,0.082,0,0,0.3086,0.6094,0.082,0,0,0.3086,0.6094,0.082,0,0,0,0,0,1,0])];
                    child.getChild('icon').filters = [new laya.filters.ColorFilter([0.2086, 0.2094, 0.082, 0, 0,
                        0.2086, 0.2094, 0.082, 0, 0,
                        0.2086, 0.2094, 0.082, 0, 0,
                        0, 0, 0, 1, 0])];
                }
            }
        }
    }

    ///////////////////////////////////////////
    initHowler(soundMgr, callback) {

    }

    ///////////////////////////////////////////
    initSoundPlayers() {

    }

    reloadPlaySound(path) {

    }

    stopSound() {

    }

    playSound(path) {

    }

    reloadSounds(gameid = 0) {

    }

    addBackgroundMusicEvent() {
        Laya.SoundManager.useAudioMusic = false;
        //Laya.SoundManager.autoStopMusic = true;
        //Laya.SoundManager.autoReleaseSound = true;
        Laya.stage.on(laya.events.Event.VISIBILITY_CHANGE, this, onHideWindow);
        function onHideWindow() {
            if (Laya.stage.isVisibility) {
                SoundMgr.rePlayMusic();
            }
            else {
                //console.log("hide");
                //SoundMgr.stopMusic();
                //Laya.SoundManager.stopAllSound();
            }
        }

        Laya.stage.on(laya.events.Event.FOCUS, this, onFocusWindow);
        function onFocusWindow() {
            //console.log("focus");
            //SoundMgr.rePlayMusic();
        }

        Laya.stage.on(laya.events.Event.BLUR, this, onBlurWindow);
        function onBlurWindow() {
            //console.log("blur");
            //SoundMgr.rePlayMusic();
        }
    }

    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    intoGameRoom(data0, cb) {
        //断线重联
        if (data0.gameName == null) {
            cb(data0);
            return;
        }
        HttpMgr.inst.joinPartyGold(data0, function (data) {
            if (data.code == 0) {
                laya.net.LocalStorage.setItem('last_gold_setting', data);
                this.checkJoinParty(cb);
            }
            else
                this.switchGameFail(data);
        }.bind(this), this.onHallHttpFail);
    }

    checkJoinParty(cb) {
        this.onCheckPartySuccess = cb;
        //var selfFunc = arguments.callee.bind(this);
        HttpMgr.inst.checkJoinPartyGold(function (data) {
            if (data.code == 0) {
                if (data["gameid"] != null) {
                    var gameData = {
                        id: data["gameid"],
                        sid: UserMgr.inst.sid,
                        ip: data["ip"],
                        port: data["port"],
                        isParty: data["isParty"],
                    };

                    if (this.onCheckPartySuccess) {
                        this.onCheckPartySuccess(gameData);
                        this.onCheckPartySuccess = null;
                    }
                }
                else {
                    Tools.inst.setTimeout(this.checkJoinParty.bind(this, cb), 1000);
                }
            }
            else
                this.switchGameFail(data);
        }.bind(this));
    }

    switchGameFail(data) {
        if (data.code == -7 || data.code == -4 || data.code == -3 || data.code == -1) {
            Alert.show(ExtendMgr.inst.getText4Language(data.msg)).onYes(function () {
                switch (data.code) {
                    case -1:
                    case -7:
                        MasterMgr.inst.switch('lobby');
                        break;
                    case -3:
                    case -4:
                        MasterMgr.inst.switch('login');
                        break;
                }
            });
        }
        else if (data.code == 100405) {
            //this.SwitchGameFail1
            Alert.show(ExtendMgr.inst.getText4Language(data.msg), true).onYes(function () {
                var lastData = data['data'];
                var gameData = {
                    id: lastData["gameid"],
                    sid: UserMgr.inst.sid,
                    ip: lastData["ip"],
                    port: lastData["port"],
                    isParty: true
                };
                //this.switchGame('game'+gameData.id,gameData);
                MasterMgr.inst.switch('game' + gameData.id, false, lastData);
            }.bind(this));
        }
        else {
            Alert.show(ExtendMgr.inst.getText4Language(data.msg), true).onYes(function () {
                MasterMgr.inst.switch('login');
            });
        }
    }

    onHallHttpFail(reason) {
        MasterMgr.inst.switch('lobby');
    }
}

class UserIconMasker {
    private graphics: laya.display.Graphics;
    public localx: number;
    public localy: number;
    public radius: number;
    public starAngle: number;
    public endAngle: number;

    setGCom(gcom: fairygui.GComponent, maskComName: string, localx, localy) {
        this.graphics = gcom.getChild(maskComName).displayObject.graphics;
        this.localx = localx;
        this.localy = localy;
    }

    updateMaskPieAngle(starAngle, endAngle) {
        this.graphics.clear();
        this.graphics.drawPie(this.localx, this.localy, this.radius, starAngle, endAngle, 0xffffff00, 0xffffffff, 0.1);
    }

    updateMaskPieAll(starAngle, endAngle, localx, localy, radius) {
        this.graphics.clear();
        this.graphics.drawPie(localx, localy, radius, starAngle, endAngle, 0xffffff00, 0xffffffff, 0.1);
        this.radius = radius;
        this.localx = localx;
        this.localy = localy;
    }

    dispose() {
        this.graphics = null;
    }
}

class nullEmitter {
    start() { }
    stop() { }
}

class nullParticle {
    public emitter: nullEmitter;
    constructor() {
        this.emitter = new nullEmitter();
    }
    destroy() { };
}