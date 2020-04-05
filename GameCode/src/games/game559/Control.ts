/**
 * Created by Administrator on 2018/4/13.
 */



module G559 {
    export namespace rf {
        export let hideSetBalance;
        export let isWildcardMode;
    }

    export namespace GControl {
        //按钮管理器
        let ButtonManager;
        export let buttonMgr;

        //动画
        let Effects;
        export let effect;

        // //牌池管理器
        //     export let Tilepool;

        //房间信息管理器
        let Roominfo;
        export let roominfo;

        //玩家管理器
        let PlayerManager;
        export let isPlayerMgrBuild;
        export let playerMgr;
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
                Roominfo = rf.Roominfo;
                PlayerManager = rf.PlayerManager;
                PlayerTemplate = rf.PlayerTemplate;
                Handwall = rf.Handwall;
                OperationManger = rf.OperationManager;
                ButtonManager = rf.ButtonManager;
                BalanceView = rf.BalanceView;
                Effects = rf.Effects;
                // Tilepool = MahjongMgr;

                //定义变量
                Control.delegate = delegate;
                Control.view = delegate._view;

                Control.balanceView = createBalanceView();
                Control.roominfo = createRoominfo();
                Control.operationMgr = createOperationMgr();
                Control.buttonMgr = createButtonMgr();
                Control.effects = createEffect();
                Control.playerMgr = PlayerManager.init(Control.createPlayer);

                //映射
                Method.getPlayer = rf.getPlayer;
                Method.getPlayerServer = rf.getPlayerServer;
                Method.getLocalPos = rf.getLocalPos;
                Method.getServerPos = rf.getServerPos;

                //初始化设置
                Control.roominfo.gameStage = Method.GAME_STAGE.WAIT_START;


            } catch (e) {
                console.error(e);
            }
            isbuild = true;
        };
        export let destory = function () {
            Control.balanceView.destory();
            Method.clearTimeout();
            Control.isPlayerMgrBuild = null;
            Control.playerMgr && Control.playerMgr.clearCountdown();
        }
        //定义房间信息管理
        export let createRoominfo = function () {
            let view = <fairygui.GComponent>Control.view;
            let component = {
                'tf_room_no': view.getChild('room_no'),
                'tfRoomDesc': view.getChild('tfRoomDesc'),
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
                obj.refreshGameListInGame(559);
            }.bind(this));
            // 玩法：
            var btn_rule = uiExitGame.getChild('btn_rule').asButton;
            btn_rule.onClick(this, function () {
                var rule = UIMgr.inst.popup(UI_Rules) as UI_Rules;
                rule.refreshData('game' + 559);
            });
            //托管
            var btn_proxy = uiExitGame.getChild('btn_proxy').asButton;
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

            let component = {
                'btn_msg': view.getChild('btn_msg'),
                // 'btn_exit': view.getChild('btn_exit'),
                // 'btn_setting': view.getChild('btn_setting'),
                // 'btn_chat': view.getChild('btn_chat'),
                'btn_change': view.getChild('btn_change'),
                'btnReady': view.getChild('btnReady'),
                //右上角按钮
                'operationView': view.getChild('operationExit'),
                'btn_exit': view.getChild('operationExit').asCom.getChild('btn_exit'),
                'btn_setting': view.getChild('operationExit').asCom.getChild('btn_setting'),

                //跑得快按钮
                'btn_last_round': view.getChild('btn_last_round'),
                // 'btn_trusteeship': view.getChild('btn_trusteeship'),
                // 'btn_trusteeship_close': view.getChild('btn_trusteeship_close'),
                'btn_trusteeship': btn_proxy,
                'ctl_autoCont': ctl_autoCont,
            }
            return ButtonManager.init(component, Control.roominfo, delegate);
        };

        //定义创建选项按钮管理器
        export let createOperationMgr = function () {
            let view = <fairygui.GComponent>Control.view;
            let operation = <fairygui.GComponent>view.getChild('operation');
            let controller = operation.getController('c1');

            let component = {
                'operation': operation,
            };
            return OperationManger.init(component, controller);
        };

        //定义创建玩家管理器
        export let createPlayerMgr = function (gameInfo) {
            try {
                Control.isPlayerMgrBuild = true;

                Control.playerMgr.build(gameInfo);
                Control.playerSelf = rf.getPlayer(0);
                Control.playerOther = rf.playerOther;
                Control.posServerSelf = rf.getServerPos(0);

                Control.buttonMgr.bindPlayer(Control.playerSelf);
                Control.operationMgr.bindPlayer(Control.playerSelf)
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
            let component = {
                'view': seat,
                'tf_nick_name': seat.getChild('name'),
                'img_head': seat.getChild('icon'),
                'tf_score': seat.getChild('score'),
                'tf_offline': seat.getChild('tagOffline'),
                'tag_trusteeship': seat.getChild('tagTrusteeship'),

                'tf_ready': view.getChildInGroup('tagReady', con),
                'tf_handCount': view.getChildInGroup('tf_handCount', con),

                'score_balance': seat.getController('balance'),
                'score_balance_txt1': seat.getChild('scoreBalance'),
                'score_balance_txt2': seat.getChild('scoreBalance2'),

                //警告灯
                'tagAlarm': view.getChildInGroup('tagAlarm', con),

                //托管
                'maskHandwallTrustee': view.getChildInGroup('maskHandwallTrustee', con) || null,
                'btnHandwallTrustee': view.getChildInGroup('btnHandwallTrustee', con) || null,

                'icon_handwall': view.getChildInGroup('icon_handwall', con),
                'tag_DoubleYes': view.getChildInGroup('tagDoubleYes', con),
                'tag_DoubleNo': view.getChildInGroup('tagDoubleNo', con),
                'con_countdown': view.getChildInGroup('countdown', con),
                'tf_countdown': view.getChildInGroup('tf_countdown', view.getChildInGroup('countdown', con).asGroup),
            };

            return PlayerTemplate.create(component, handwall, roominfo, setting);
        };

        //定义获取手牌实例方法
        export let createHandwall = function (localSide) {
            var view = <fairygui.GComponent>Control.view;
            var conName = Map_side2playerCon[localSide];
            var con = <fairygui.GGroup>view.getChild(conName);
            let isShowHand = localSide == 0;
            let component = {
                'hand_pokers': view.getChildInGroup('hand_pokers', con),
                'outwall': view.getChildInGroup('out_pokers', con),
                'tag_Pass': view.getChildInGroup('tagPass', con),

            };

            let HandwallInstance = Handwall.create(component, localSide, isShowHand);
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
                'tfDesc': balanceview.getChild('tfDesc'),
                'autoContTimer': balanceview.getChild('autoContTimer'),
            };
            let getPlayerItem = function (localside) {
                let mapSide2Name = {
                    0: 'seat0',
                    1: 'seat1',
                    2: 'seat2',
                };
                let name = mapSide2Name[localside];
                let item = balanceview.getChild(name).asCom;
                return {
                    'con': item,
                    'tfName': item.getChild('tfName559'),
                    'icon': item.getChild('icon'),
                    'tfBaseScore': item.getChild('tfBaseScore'),
                    'tfLastCard': item.getChild('tfLastCard'),
                    'tfBoom': item.getChild('tfBoom'),
                    'tfScore': item.getChild('tfScore'),
                    'tfMultiple': item.getChild('tfMultiple'),
                    'tagWin': item.getChild('tagWin'),
                    'tagSpring': item.getChild('tagSpring'),
                    'tagDouble': item.getChild('tagDouble'),
                    'tgamectl': item.getController('gametype'),
                }
            };
            let params = {
                'player0': getPlayerItem(0),
                'player1': getPlayerItem(1),
                'player2': getPlayerItem(2),
                'controller': balanceview.getController('c1'),
                'onShow': balanceview.getTransition('onShow'),
                "gameTypectl": balanceview.getController('gametype'),
            };
            return BalanceView.create(component, params)

        };

        //动画
        export let createEffect = function () {
            var view = <fairygui.GComponent>Control.view;
            var con = <fairygui.GGroup>view.getChild('effect');
            let component = {
                cardEffect: view.getChildInGroup('cardEffect', con).asCom,
            };
            let params = {
                shunzi: component.cardEffect.getController('shunzi'),
                bomb: component.cardEffect.getController('bomb'),
                liandui: component.cardEffect.getController('liandui'),
                feiji: component.cardEffect.getController('feiji'),
                rocket: component.cardEffect.getController('rocket'),
            };
            let instance = Effects.create(component, params);
            return instance;
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