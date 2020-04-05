class MasterSettings {
    private static _crypto = null;
    private static _masters = null;

    public static get crypto() {
        if (MasterSettings._crypto) {
            return MasterSettings._crypto;
        }

        MasterSettings._crypto = {
            HTTP_AES_KEY: null,//"hTtp^@AES&*kEy";
            GAME_AES_KEY: null,//"GaMe;$AES#!KeY";            
        }
    }

    public static get masters() {
        if (MasterSettings._masters) {
            return MasterSettings._masters;
        }

        MasterSettings._masters = {};

        var masters = MasterSettings._masters;

        //登陆
        masters.preloading = {
            type: 'common', //类别 common:普通 subgame子游戏
            name: '预加载', //拿来看的
            master_script: PreloadingMaster, //主逻辑
            entry_scene: PreloadingScene, //入口场景，如果有，会在切换主逻辑的时候自动加载
            frame_rate: Laya.Stage.FRAME_FAST
        }

        //登陆
        masters.login = {
            type: 'common',
            name: '登陆',
            master_script: LoginMaster,
            entry_scene: LoginScene,
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters.relogin = {
            type: 'common',
            name: '登陆2',
            master_script: ReLoginMaster,
            entry_scene: ReLoginScene,
            frame_rate: Laya.Stage.FRAME_FAST
        }

        //创建角色
        masters.create_role = {
            type: 'common',
            name: '创建角色',
            //master_script:CreateRoleMaster,
            //entry_scene:CreateRoleScene,
            frame_rate: Laya.Stage.FRAME_FAST
        }

        //大厅
        masters.lobby = {
            type: 'common',
            name: ExtendMgr.inst.MN_Lobby,
            master_script: LobbyMaster,
            entry_scene: HallScene,
            version: "1.0.0.5",
            frame_rate: Laya.Stage.FRAME_FAST
        }

        //子游戏
        masters['game445'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_HongZhong,
            master_script: G445Master,
            entry_scene: G445Scene,
            version: "1.0.0.3",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game449'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_ErRenMaJiang,
            master_script: G449Master,
            entry_scene: G445Scene,
            version: "1.0.0.4",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game452'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_GuangDongJiDaHu,
            master_script: G452Master,
            entry_scene: G445Scene,
            version: "1.0.0.3",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game556'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_MingPaiNiu,
            master_script: G556Master,
            entry_scene: G556Scene,
            version: "1.0.0.3",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game555'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_QiangZhuangNiu,
            master_script: G555Master,
            entry_scene: G555Scene,
            version: "1.0.0.3",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game558'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_TongBiNiu,
            master_script: G558Master,
            entry_scene: G558Scene,
            version: "1.0.0.0",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game559'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_PaoDeKuai,
            master_script: G559.GMaster,
            entry_scene: G559.GScene,
            version: "1.0.0.1",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game560'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_DouDiZhu,
            master_script: G560.GMaster,
            entry_scene: G560.GScene,
            version: "1.0.0.1",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game564'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_XueLiu,
            master_script: G564Master,
            entry_scene: G445Scene,
            version: "1.0.0.1",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game563'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_SanGong,
            master_script: G563Master,
            entry_scene: G563Scene,
            version: "1.0.0.1",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game566'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_TongBiSanGong,
            master_script: G566Master,
            entry_scene: G566Scene,
            version: "1.0.0.0",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game557'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_21Dian,
            master_script: G557Master,
            entry_scene: G557Scene,
            version: "1.0.0.2",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game561'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_ZhaJinHua,
            master_script: G561.GMaster,
            entry_scene: G561.GScene,
            version: "1.0.0.3",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game562'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_ShiSanShui,
            master_script: G562.G562Master,
            entry_scene: G562.G562Scene,
            version: "1.0.0.2",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game565'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_DeZhou,
            master_script: G565.G565Master,
            entry_scene: G565.G565Scene,
            version: "1.0.0.6",
            frame_rate: Laya.Stage.FRAME_FAST
        }

        masters['game570'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_ErRenDouDiZhu,
            master_script: G570.GMaster,
            entry_scene: G560.GScene,
            version: "1.0.0.1",
            frame_rate: Laya.Stage.FRAME_FAST
        }

        masters['game666'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_HuanLeNiu,
            master_script: G666Master,
            entry_scene: G666Scene,
            version: "1.0.0.3",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game548'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_BaoDian,
            master_script: G548.G548Master,
            entry_scene: G548.G548Scene,
            version: "1.0.0.1",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game549'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_BaoDian,
            master_script: G549.G549Master,
            entry_scene: G548.G548Scene,
            version: "1.0.0.1",
            frame_rate: Laya.Stage.FRAME_FAST
        }
        masters['game9999'] = {
            enable: true,
            type: 'subgame',
            name: ExtendMgr.inst.MN_BaiJiaLe,
            master_script: G9999.G9999Master,
            entry_scene: G9999.G9999Scene,
            version: "1.0.0.1",
            frame_rate: Laya.Stage.FRAME_FAST
        }

        return masters;
    }
}