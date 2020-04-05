import Handler = laya.utils.Handler;
import Loader = laya.net.Loader;
import Socket = Laya.Socket;
import Byte = Laya.Byte;
import ResourceVersion = Laya.ResourceVersion;
import Tween = Laya.Tween;
import Ease = Laya.Ease;
import WebGL = Laya.WebGL;

module TestMgr {
    export let LANGUAGE = 'CN';
    export let IS_SHOW_TAKE_MONEY = false;

    export let IS_REAL_ACCOUNT = true;
    export let IS_ENABLE_SELECT_SERVER = true;
    export let SELECT_SERVER_COUNT = 5;
    export let IS_ENABLE_PRINT_URL = true;
    export let IS_DECODE = true;
    //这是用来控制快捷按键的开关
    export let IS_DEBUG = false;
    export let IS_PUBLIC = false;
}

module ResourceMgr {
    export let RES_PATH = 'res/';
    export let TEXT_RES_PATH = 'res/';
    // export let MUSIC_PATH = 'res/music/';
    export let PROTO_PATH = RES_PATH + 'proto/';
    // export let PROTO_PATH = 'res/proto_bak/';
    export let GAMERES_PATH = RES_PATH + 'games/';

    export function GetGameProtoPath(gameID) {
        return GAMERES_PATH + 'game' + gameID + '/proto/';
    }
}

class MyAppSettings extends AppSettings {
    constructor() {
        super();
        var settings = this;
        settings.designWidth = 1334;
        settings.designHeight = 750;
        settings.scaleMode = Laya.Stage.SCALE_SHOWALL;
        settings.screenMode = Laya.Stage.SCREEN_HORIZONTAL;
        settings.showStats = true;
        settings.statsX = 0;
        settings.statsY = 500;
        settings.frameRate = Laya.Stage.FRAME_FAST; //Laya.Stage.FRAME_MOUSE;//
        settings.maxUILayer = UILayer.MAX_NUM;
        settings.alertWidget = GameAlert;
        settings.wcWidget = GameWC;
    }
}

ds64(_0);
ds64(_1);

var location_search_account = "";
var location_random_account = 0;
var location_random_index = -1;
var location_return_url = null;
var wait_of_loading_mark = 'ui_for_wait_of_loading';
var minigame_background_mark = 'ui_for_background_of_minigame';

// console.log=function(){}
//if (TestMgr.IS_PUBLIC) console.log = function () { }

// app entry.
class app {
    constructor() {
        //TestMgr.IS_PUBLIC = true;
        //ExtendMgr.inst.lan = ExtendMgr.inst.lan.toLowerCase(); //非调试环境 出现 toLowerCase is not a function

        this.init_params();
        TestMgr.IS_DECODE = false;
        var protocol = "https:"; // location.protocol == "https:" ? location.protocol : "http:";
        var port = getNetworkPort(protocol);
        var address = "//" + getDefaultDns(port);
        var url = protocol + address;

        if (TestMgr.IS_ENABLE_SELECT_SERVER) {
            dnsSeverSelectorInit(protocol, 2, "test", "-", port, protocol + address);

            selectDnsSever(function (success) {
                if (success) {
                    var serverURL = getDnsSever();
                    if (serverURL) {
                        url = serverURL;
                        //success
                    }
                    //url = protocol+address;
                }
                else {
                    //fail
                }
                HttpMgr.inst.configure(url, port);
            });
        }
        else {
            HttpMgr.inst.configure(url, port);
        }

        //Laya.alertGlobalError = !TestMgr.IS_PUBLIC; 

        //加载版本信息文件
        var configUrl: string = "manifest.json?" + Math.random();
        ResourceVersion.enable(configUrl, Handler.create(this, this.beginLoad), ResourceVersion.FOLDER_VERSION);
    }

    private init_params() {
        var lan = Laya.LocalStorage.getItem(KEY_LANGUAGE);
        if (lan) {
            TestMgr.LANGUAGE = lan;
        }
        else {
            var lan = getQueryString('language');
            if (lan) {
                TestMgr.LANGUAGE = lan;
            }
        }

        var res_root = getQueryString('resource_url');
        if (res_root) {
            ResourceMgr.RES_PATH = res_root;
        }
        else {
            res_root = getResRoot();
            if (res_root) {
                ResourceMgr.RES_PATH = res_root;
            }
        }

        ResourceMgr.TEXT_RES_PATH = getTextResRoot();

        //add ui for wait of loading ///////////
        var ape = Laya.stage.addChild(new laya.ui.Image()) as laya.ui.Image;
        ExtendMgr.inst.setBackgroundfull(wait_of_loading_mark, ResourceMgr.RES_PATH + "bg/lodingBg.jpg", ape);
        /////////////////////////////////////////

        var account = getQueryString('params');
        if (account && account.toString().length > 1) {
            location_search_account = account;
        }
        else {
            var test = getQueryString('test');
            if (test && test.toString().length > 1) {
                location_random_account = parseInt(test);
            }
        }

        var usebuf = getQueryString('usebuf');
        if (usebuf) {
            TestMgr.IS_DECODE = (usebuf == 'true' || usebuf == 'TRUE');
        }

        var show_other_wallet = getQueryString('singleWallet');
        if (show_other_wallet) {
            TestMgr.IS_SHOW_TAKE_MONEY = (show_other_wallet == 'true' || show_other_wallet == 'TRUE');
        }

        location_return_url = getQueryString('returnURL');
        if (location_return_url && TestMgr.IS_ENABLE_PRINT_URL) {
            console.log("return_url: " + location_return_url);
        }

        var default_game = getQueryString('gameId');
        if (default_game) {
            Laya.LocalStorage.setItem(ExtendMgr.LastSelectGameIdKey, '' + parseInt(default_game));
        }
        else {
            if (Laya.LocalStorage.getItem(ExtendMgr.LastSelectGameIdKey)) {
                Laya.LocalStorage.removeItem(ExtendMgr.LastSelectGameIdKey)
            }
        }
    }

    private beginLoad() {
        //initialize
        SoundMgr.initResPath();
        ExtendMgr.inst.addBackgroundMusicEvent();

        var is_ios_ver_10: boolean = ExtendMgr.inst.getIOSVersion() == 10;
        var settings = new MyAppSettings();
        settings.designWidth = is_ios_ver_10 ? 2436 : 1334;
        settings.designHeight = is_ios_ver_10 ? 1125 : 750;

        let url = ResourceMgr.TEXT_RES_PATH + 'language/c2e.json';
        Laya.loader.load(url, Handler.create(this, (data: JSON) => {
            ExtendMgr.inst.multiLanguageTextMap = data;
            ExtendMgr.inst.setLanguage(TestMgr.LANGUAGE);
            getCodeAdapter().init(function () {
                bk.configure(settings);
                bk.start('preloading');
            }.bind(this));
        }), null, Loader.JSON);
        //StressTestMgr.inst.decodeTex();
    }
}

function initgame(mode = 0) {
    TestMgr.IS_PUBLIC = isPublicVersion();
    TestMgr.IS_ENABLE_SELECT_SERVER = getSelectServerSwitchState(); //
    TestMgr.IS_ENABLE_PRINT_URL = isPrintURL();//  showurl;
    //TestMgr.SELECT_SERVER_COUNT = server_count;
    TestMgr.LANGUAGE = getLanguage(); //lan;
    TestMgr.IS_SHOW_TAKE_MONEY = getShowOtherWallet();//show_take_money;

    ExtendMgr.inst.isShowProtoCmd = isPrintProtoCmd();

    function initLaya() {
        ExtendMgr.inst.checkIOSVersionAndDevice(null);
        ExtendMgr.inst.setDesignResolution();
    }

    initLaya();
    new app();
}   