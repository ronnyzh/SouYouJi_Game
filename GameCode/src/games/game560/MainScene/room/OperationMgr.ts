/**
 * Created by Administrator on 2018/4/13.
 */
module G560{
    export namespace fl{
        export class OperationManagerFace extends Vuet{
            operation: fairygui.GList;
            controller: fairygui.Controller;
            pageDict: any;

            show: Function;
            after: Function;
            onItem: Function;
            hide:Function;
        }
        export class OperationManager{
            static init (component, Controller){
                let operation = component['operation'];
                return new Vuet({
                    data:{
                        gameStage: null,
                    },
                    component:{
                        'operation': operation,

                    },
                    params: {
                        controller: Controller,
                        pageDict : operation._children.reduce(function (acc, item) {
                            let groupName = item.group && item.group.name;
                            if(groupName){
                                let list = acc[groupName] || (acc[groupName]  = []);
                                list.push(item);
                            }
                            return acc;
                        },{})
                    },

                    created: function(){
                        //初始化主选项管理器
                        var _obj;
                        var self = <OperationManagerFace>this;
                        Object.keys((_obj = this.pageDict)).forEach(function(key){
                            _obj[key].forEach(function (btn, idx) {
                                (<fairygui.GButton>btn).onClick(self, self.onItem,[idx, btn]);
                            })
                        })
                    },
                    watch:{
                        gameStage: function(newValue){
                            var isGameEnd = newValue == Method.GAME_STAGE.GAME_READY;

                            console.log('operation watch gamestage:', newValue,',isGameEnd:', isGameEnd);

                            let self = (<OperationManagerFace>this);

                            if(isGameEnd){
                                self.hide();
                            }
                        }
                    },
                    method: {
                        //-----------开放调用
                        show: function(name?, clickCallback?, list?) :OperationManagerFace{
                            let self = (<OperationManagerFace>this);
                            this._name = name;
                            //---如果是isDouble，先检测自己是否已经选了
                            if(name =='isDouble' && fl.playerSelf.isDouble !== null){
                                return;
                            }
                            //---如果是isLandlord，先检测自己是否已经选了
                            if(name =='isLandlord' && fl.playerSelf.isLandlord !== null){
                                return;
                            }

                            //---下面是 打牌操作按钮
                            // 显示界面
                            self.getComponent('operation').visible = true;
                            //没有name则只显示
                            if(!name)return;

                            self.controller.setSelectedPage(name);

                            if(clickCallback){
                                this._clickCallback = clickCallback;
                            }

                            let items = self.pageDict[name];
                            if(items){
                                items.forEach(function(item, idx){
                                    let isShow = !list || (list && list.indexOf(idx) === -1);
                                    item.visible = isShow;
                                })
                            }
                            return self;
                        },

                        /**
                         * @params: method(btns);
                         * */
                        after: function(caller, method, args?):OperationManagerFace{
                            args = typeof args == 'undefined'? []:args;
                            let self = (<OperationManagerFace>this);
                            let btns = self.pageDict[this._name].concat();
                            method.apply(caller, [].concat(args, [btns] ));
                            return self;
                        },

                        hide: function(){
                            let self = (<OperationManagerFace>this);
                            self.getComponent('operation').visible = false;
                        },

                        reset: function(){
                            this.hide();
                            this._clickCallback = null;
                            return this;
                        },
                        //-----------

                        onItem: function(idx, btn){
                            console.log('itemClick',idx);
                            var clickCallback = this._clickCallback;
                            if(clickCallback){
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