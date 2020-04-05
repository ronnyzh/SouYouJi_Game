/**
 * Created by Administrator on 2018/4/13.
 */
module G559 {
    export namespace rf {
        export class OperationManagerFace extends Vuet {
            operation: fairygui.GList;
            controller: fairygui.Controller;
          

            show: Function;
            onItem: Function;
            hide: Function;
        }
        export class OperationManager {
            static init(component, Controller) {
                let operation = component['operation'];
                return new Vuet({
                    data: {
                        gameStage: null,
                        isTrustee: null,
                    },
                    component: {
                        'operation': operation,

                    },
                    params: {
                        controller: Controller,
                        pageDict: operation._children.reduce(function (acc, item) {
                            let groupName = item.group && item.group.name;
                            if (groupName) {
                                let list = acc[groupName] || (acc[groupName] = []);
                                list.push(item);
                            }
                            return acc;
                        }, {})
                    },

                    created: function () {
                        //初始化主选项管理器
                        var _obj;
                        var self = <OperationManagerFace>this;
                        Object.keys((_obj = this.pageDict)).forEach(function (key) {
                            _obj[key].forEach(function (btn, idx) {
                                (<fairygui.GButton>btn).onClick(self, self.onItem, [idx, btn]);
                            })
                        });
                    },
                    watch: {
                        gameStage: function (newValue) {
                            var isGameEnd = newValue == Method.GAME_STAGE.GAME_READY;

                            console.log('operation watch gamestage:', newValue, ',isGameEnd:', isGameEnd);

                            let self = (<OperationManagerFace>this);

                            if (isGameEnd) {
                                self.hide();
                            }
                        },

                    },
                    once: {
                        bindPlayer: function (playerSelf) {
                            //绑定自己是否托管
                            playerSelf.watch('isTrustee', function (newValue) {
                                this.isTrustee = newValue;
                            }.bind(this));
                        },
                    },
                    method: {
                        //-----------开放调用

                        show: function (name?, clickCallback?, list?) {
                            let self = (<OperationManagerFace>this);

                            //---如果是加倍，先检测自己是否已经选了
                            if (name == 'jiabei' && rf.playerSelf.isDouble !== null) {
                                return;
                            }

                            //---下面是 打牌操作按钮
                            // 显示界面
                            self.getComponent('operation').visible = true;
                            //没有name则只显示
                            if (!name) return;

                            self.controller.setSelectedPage(name);

                            if (clickCallback) {
                                this._clickCallback = clickCallback;
                            }

                            let items = this.pageDict[name];
                            if (items) {
                                items.forEach(function (item, idx) {
                                    let isShow = !list || (list && list.indexOf(idx) === -1);
                                    item.visible = isShow;
                                })
                            }


                        },
                        hide: function () {
                            let self = (<OperationManagerFace>this);
                            self.getComponent('operation').visible = false;
                        },

                        reset: function () {
                            this.hide();
                            this._clickCallback = null;
                        },
                        //-----------

                        onItem: function (idx, btn) {
                            //console.log('itemClick', idx);
                            var clickCallback = this._clickCallback;
                            if (clickCallback) {
                                clickCallback(idx, btn);
                            }
                            // this._clickCallback = null;
                        },
                    }
                });
            }

        }
    }
}