/**
 * Created by Administrator on 2018/5/4.
 */
module G561{
    export namespace fl{
        interface i_Effects extends Vuet{

        }
        export class Effects {

            static create (component, params){
                return new Vuet({
                    data:{},
                    watch:{},
                    params:{
                        shunzi:  params['shunzi'],
                        bomb:  params['bomb'],
                        liandui:  params['liandui'],
                        feiji:  params['feiji'],
                        rocket:  params['rocket'],
                        redeal:  params['redeal'],

                    },
                    component:{
                        cardEffect: component['cardEffect'],
                    },
                    method:{
                        setPositionBySide: function(localSide){
                            let self = <i_Effects>this;
                            let player = Method.getPlayer(localSide);
                            let outwall = player.getComponent('outwall');
                            let posGolbal = outwall.localToGlobal();
                            let position = {x: posGolbal.x + outwall.width / 2, y: posGolbal.y + outwall.height / 2};
                            this.setPosition(position);

                        },

                        setPosition: function(position){
                            let self = <i_Effects>this;
                            let component = self.getComponent('cardEffect');
                            component.x = position.x;
                            component.y = position.y;
                            component.visible = true;
                            return position;
                        },

                        playNormalEffect: function(name, caller?, method?){
                            let self = <i_Effects>this;
                            let component = self.getComponent('cardEffect');
                            component.visible = true;
                            component.getController('c1').setSelectedPage(name);
                            let transition = component.getTransition(name);
                            transition.play(new Laya.Handler(this, function(){
                                component.visible = false;
                                if(method)
                                method.call(caller || this);
                            }));
                        },

                        playRocket: function(localSide, caller?, method?){
                            this.setPositionBySide(localSide);
                            this.playNormalEffect( 'rocket', caller, method);
                        },
                        playBomb: function(localSide, caller?, method?){
                            this.setPositionBySide(localSide);
                            this.playNormalEffect( 'bomb', caller, method);
                        },
                        playSequence: function(localSide, caller?, method?){
                            this.setPositionBySide(localSide);
                            this.playNormalEffect( 'shunzi', caller, method);
                        },
                        playSequence2: function(localSide, caller?, method?){
                            this.setPositionBySide(localSide);
                            this.playNormalEffect( 'liandui', caller, method);
                        },
                        playSequence3: function(localSide, caller?, method?){
                            this.setPositionBySide(localSide);
                            this.playNormalEffect( 'feiji', caller, method);
                        },
                        playSpring: function(caller?, method?){
                            this.setPosition(jx.p(Laya.stage.width / 2, Laya.stage.height / 2));
                            this.playNormalEffect( 'spring', caller, method);
                        },
                        playAntiSpring: function( caller?, method?){
                            this.setPosition(jx.p(Laya.stage.width / 2, Laya.stage.height / 2));
                            this.playNormalEffect( 'antispring', caller, method);
                        },

                        playRedeal: function( caller?, method?){
                            let self = <i_Effects>this;
                            this.setPosition(jx.p(Laya.stage.width / 2, Laya.stage.height / 2));
                            this.playNormalEffect( 'redeal', caller, method);
                        }

                    }

                })
            }
        }
    }

}