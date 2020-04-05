/**
 * Created by Administrator on 2018/4/13.
 */


module G561 {
    export namespace fl {
        export let hideSetBalance;
        export let isWildcardMode;
    }
    export namespace GControl {

        //按钮管理器
        let ButtonManager;
        export let buttonMgr;

        //房间信息管理器
        let Roominfo;
        export let roominfo;

        // //牌池管理器
        // export let Tilepool;

        //动画
        let Effects;
        export let effect;

        //玩家管理器
        let PlayerManager;
        export let isPlayerMgrBuild;
        export let playerMgr: playerManagerData;
        export let playerSelf;
        export let playerOther;
        export let posServerSelf;
        export let posLocalSelf = 0;

        //玩家模板
        let PlayerTemplate;

        //手牌模板
        let Handwall;

        //操作按钮
        let OperationManger;
        export let operationMgr;

        //小结界面
        let BalanceView;
        export let balanceView;

        //控制器初始化
        export let delegate;
        export let view;
        export let isbuild = false;
        export let build = function (delegate) {
            try {
                //定义使用对象
                Roominfo = fl.Roominfo;
                PlayerManager = fl.PlayerManager;
                PlayerTemplate = fl.PlayerTemplate;
                Handwall = fl.Handwall;
                OperationManger = fl.OperationManager;
                ButtonManager = fl.ButtonManager;
                BalanceView = fl.BalanceView;
                Effects = fl.Effects;
                // Tilepool = MahjongMgr;

                //定义变量
                Control.delegate = delegate;
                Control.view = delegate._view;

                Control.roominfo = createRoominfo();
                Control.balanceView = createBalanceView();
                Control.buttonMgr = createButtonMgr();
                Control.operationMgr = createOperationMgr();
                Control.playerMgr = PlayerManager.init(Control.createPlayer);

                //映射
                Method.getPlayer = fl.getPlayer;
                Method.getPlayerServer = fl.getPlayerServer;
                Method.getLocalPos = fl.getLocalPos;
                Method.getServerPos = fl.getServerPos;

                //初始化设置
                Control.roominfo.gameStage = Method.GAME_STAGE.WAIT_START;


            } catch (e) {
                console.error(e);
            }
            isbuild = true;
        };

        export let destory = function () {
            Control.isPlayerMgrBuild = null;
            Control.playerMgr && Control.playerMgr.clearCountdown();
            Control.isPlayerMgrBuild = false;
        }
        //定义房间信息管理
        export let createRoominfo = function () {
            let view = <fairygui.GComponent>Control.view;
            let component = {
                'tf_room_no': view.getChild('room_no'),
                'tfRoomDesc': view.getChild('tfRoomDesc'),
                //炸金花
                'tfDanzhu': view.getChild('tfDanzhu0'),
                'tfZongzhu': view.getChild('tfDanzhu1'),
                'tfLunshu': view.getChild('tfDanzhu2'),
            };
            return Roominfo.init(delegate, component);
        };

        //定义按钮管理器
        export let createButtonMgr = function () {
            let view = <fairygui.GComponent>Control.view;


            var uiExitGame = view.getChild('operationExit').asCom;
            // 游戏内的战绩：
            var btn_history = uiExitGame.getChild('btn_history').asButton;
            btn_history.onClick(this, function () {
                var obj = UIMgr.inst.popup(UI_History) as UI_History;
                obj.refreshGameListInGame(561);
            }.bind(this));
            // 玩法：
            var btn_rule = uiExitGame.getChild('btn_rule').asButton;
            btn_rule.onClick(this, function () {
                var rule = UIMgr.inst.popup(UI_Rules) as UI_Rules;
                rule.refreshData('game' + 561);
            });
            // 设置：
            var btn_rule = uiExitGame.getChild('btn_setting').asButton;
            btn_rule.onClick(this, function () {
                UIMgr.inst.popup(UI_Setting);
            });
            //托管
            var btn_proxy = uiExitGame.getChild('btn_proxy').asButton;
            btn_proxy.visible = false;

            //自动继续 判断ui是否有自动继续按钮和倒计时
            let ctl_autoCont = uiExitGame.getController('AutoCont');
            let autoContTimer = Control.balanceView.getComponent('autoContTimer');
            if (ctl_autoCont != null && autoContTimer != null) {
                let btn_autoCont = uiExitGame.getChild('btn_autoCont').asButton;
                btn_autoCont.onClick(this, function () {
                    if (ctl_autoCont.selectedIndex == 1) {
                        Control.balanceView.hideAutoContTimer();
                    }
                    else if (Control.balanceView.getComponent('btnContinue').visible == true) {
                        Method.changeRoom();
                    }
                    ctl_autoCont.selectedIndex = ctl_autoCont.selectedIndex == 0 ? 1 : 0;
                })
            }
            //


            let component = {
                'btn_msg': view.getChild('btn_msg'),
                // 'btn_exit': view.getChild('btn_exit'),
                // 'btn_setting': view.getChild('btn_setting'),
                'btn_chat': view.getChild('btn_chat'),
                'btn_change': view.getChild('btn_change'),
                'btnReady': view.getChild('btnReady'),
                //右上角按钮
                'operationView': view.getChild('operationExit'),
                'btn_exit': view.getChild('operationExit').asCom.getChild('btn_exit'),
                'btn_setting': view.getChild('operationExit').asCom.getChild('btn_setting'),

                //炸金花按钮
                'btn_trusteeship': view.getChild('btn_trusteeship'),
                'btn_trusteeship_close': view.getChild('btn_trusteeship_close'),
                'ctl_autoCont':ctl_autoCont,
            };
            return ButtonManager.init(component, Control.roominfo, delegate);
        };

        //定义创建选项按钮管理器
        export let createOperationMgr = function () {
            let view = <fairygui.GComponent>Control.view;
            let operation = <fairygui.GComponent>view.getChild('operation');
            let controller = operation.getController('c1');
            let component = {
                'operation': operation,
                'jiazhu': operation.getChild('jiazhu'),
                'pkMask': view.getChild('pkMask0')
            };
            return OperationManger.init(component, controller, Control.buttonMgr);
        };

        //定义创建玩家管理器
        export let createPlayerMgr = function (gameInfo) {
            try {
                Control.isPlayerMgrBuild = true;

                Control.playerMgr.build(gameInfo);
                Control.playerSelf = fl.getPlayer(0);
                Control.playerOther = fl.playerOther;
                Control.posServerSelf = fl.getServerPos(0);

                Control.buttonMgr.bindPlayer(Control.playerSelf);

            } catch (e) { console.error(e) }
        };

        //定义获取玩家实例方法
        let Map_side2playerCon = {
            0: 'playerCon0',
            1: 'playerCon1',
            2: 'playerCon2',
            3: 'playerCon3',
            4: 'playerCon4',
        };
        export let createPlayer = function (localSide) {
            var view = <fairygui.GComponent>Control.view;
            var conName = Map_side2playerCon[localSide];
            var con = <fairygui.GGroup>view.getChild(conName);
            var seat = <fairygui.GComponent>view.getChildInGroup('seat', con);

            let setting = {};
            let handwall = Control.createHandwall(localSide);
            let seatItem = seat.getChild('seatItem').asCom;
            let component = {
                'view': seat,
                'tf_nick_name': seatItem.getChild('name'),
                'img_head': seatItem.getChild('icon'),
                'tf_score': seatItem.getChild('score'),
                'tf_offline': seat.getChild('tagOffline'),
                'tag_trusteeship': seat.getChild('tagTrusteeship'),

                'tf_ready': view.getChildInGroup('tagReady', con),
                'tf_handCount': view.getChildInGroup('tf_handCount', con),
                'icon_handwall': view.getChildInGroup('icon_handwall', con),

                'tfScore': seatItem.getChild('tfScore').asCom,

                //倒计时
                'con_countdown': view.getChildInGroup('countdown', con),
                'tf_countdown': view.getChildInGroup('tf_countdown', view.getChildInGroup('countdown', con).asGroup),

                //炸金花
                'operationTalk': view.getChildInGroup('operationTalk', con),
                'tfChip': seat.getChild('tfChip'),
                'tagBipai': view.getChild('tagBipai' + localSide) || null,
                'group': con,
            };

            let params = {
                handwall: handwall,
                turnController: seat.getController('turn'),
                ImageController: seat.getController('Image'),
                TalkController: (component['operationTalk'] as fairygui.GComponent).getController('TalkController'),
            };
            return PlayerTemplate.create(component, params, roominfo, setting);
        };

        //定义获取手牌实例方法
        export let createHandwall = function (localSide) {
            var view = <fairygui.GComponent>Control.view;
            var conName = Map_side2playerCon[localSide];
            var con = <fairygui.GGroup>view.getChild(conName);
            let isShowHand = true;
            let isSelf = localSide == Control.posLocalSelf;
            let handwall;
            let component = {
                'hand_pokers': (handwall = isSelf ? view.getChild('playerHandwall0') : view.getChildInGroup('hand_pokers', con)),
                'clickLayer': handwall.getChild('clickLayer'),
                'outwall': view.getChildInGroup('out_pokers', con),
                'tag_Pass': view.getChildInGroup('tagPass', con),

            };
            let params = {
                'hand_position': { x: (component['hand_pokers'] as fairygui.GList).x, y: (component['hand_pokers'] as fairygui.GList).y },
            }
            let HandwallInstance = Handwall.create(component, localSide, isShowHand, params);
            if (localSide == Control.posLocalSelf) {
                HandwallInstance.enabledTouch();
            }
            return HandwallInstance;
        };

        //小结页面
        export let createBalanceView = function () {
            var view = <fairygui.GComponent>Control.view;
            var balanceview = view.getChild('balanceView').asCom;
            let component = {
                'con': balanceview,
                'btnExit': balanceview.getChild('btnExit'),
                'btnContinue': balanceview.getChild('btnContinue'),
                'btnChange': balanceview.getChild('btnChange'),
                'autoContTimer': balanceview.getChild('autoContTimer'),
            };
            let params = {
                'conPlayerList': balanceview.getChild('playerList'),
                'controller': balanceview.getController('c1'),
            };
            return BalanceView.create(component, params)

        };

        //呼叫机器人
        export let callRobot = function () {
            let result = laya.net.LocalStorage.getJSON('last_gold_setting');
            let params = {};
            params['r'] = roominfo.roomId;
            params['g'] = result['id'];
            // params['c'] = playerMgr.
        }
    }
}
