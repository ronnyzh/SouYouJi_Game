module G570 {
    export namespace fl {
        export interface playerTemplateData {
            //data
            account?: string | number;
            coin?: string | number;
            headImgUrl?: string;
            id?: string | number;
            ip?: string;
            isGM?: boolean;
            nickname?: string;
            roomCards?: string | number;
            sex?: number;
            side?: string | number;
            handwall?: fl.HandwallData;

            score;
            isReady;
            online;
            isEmpty;
            isShowHandCount;
            isDouble;
            isLandLord2;
            callLandLord;
            letcard;//让牌
            isTrustee;
            countdown;
            isDealer;
            hidetag;

            alarm?: fairygui.Transition;
            tiles?: any;
            cardsEnabled?: any;
            handCount?: any;
            boomCount?: any;
            boomMultiple?: any;

            getComponent?: Function;
            update?: Function;
            show?: Function;
            hide?: Function;
            reset?: Function;
            getMaxCardId?: Function;
            showAlarm?: Function;
            hideAlarm?: Function;
        }
        //玩家模板- component数据结构
        export interface playerTemplateComponentData {
            //头像部分
            view: fairygui.GComponent;
            tf_nick_name: fairygui.GComponent;
            img_head: fairygui.GComponent;
            tf_score: fairygui.GComponent;
            tag_ready: fairygui.GComponent;

        }
        export class PlayerTemplate extends G560.fl.PlayerTemplate {
            constructor() {
                super();
            }
            static create(component, handwall, roominfo) {
                let base = super.create(component, handwall, roominfo);
                let params: any = base._config;
                //data///////////////////////////////////////////////////////////////////////
                params.data.hidetag = null;
                params.data.isLandLord2 = null;
                params.data.callLandLord = null;
                params.data.letcard = null;
                //component///////////////////////////////////////////////////////////////////////
                params.component['tag'] = component['tag'];
                params.component['tag_landlord_yeslandlord'] = component['tag_landlord_yeslandlord'];
                params.component['tag_landlord_norob'] = component['tag_landlord_norob'];
                params.component['tag_landloed_nolet'] = component['tag_landloed_nolet'];
                params.component['tag_landloed_lettwo'] = component['tag_landloed_lettwo'];
                //watch///////////////////////////////////////////////////////////////////////
                params.watch.boomMultiple = function (newValue) {

                }
                params.watch.hidetag = function (newValue) {
                    let self = <playerTemplateData>this;
                    let tag: fairygui.GComponent = self.getComponent('tag');
                    for (let i = 0; i < tag.numChildren; i++) {
                        tag.getChildAt(i).visible = false;
                    }
                }
                params.watch.isDouble = function (newValue) {
                    // 1 ：不加倍 2：加倍
                    this.hidetge();
                    let self = <playerTemplateData>this;
                    let tagYes = self.getComponent('tag_DoubleYes');
                    let tagNo = self.getComponent('tag_DoubleNo');
                    if (newValue === null) {
                        tagYes.visible = false;
                        tagNo.visible = false;
                    } else {
                        //  console.log(tagYes, tagNo, "=========isDouble");
                        tagYes.visible = newValue == '2';
                        tagNo.visible = newValue == '1';
                    }
                }
                params.watch.isLandLord2 = function (newValue) {
                    // console.log("isLandLord2====", newValue);
                    this.hidetge();
                    let self = <playerTemplateData>this;
                    let tagNo = self.getComponent('tag_landlord_no');
                    let tagYes = self.getComponent('tag_landlord_yeslandlord');
                    if (newValue === null) {
                        tagYes.visible = false;
                        tagNo.visible = false;
                    } else {
                        tagYes.visible = newValue == '1';
                        tagNo.visible = newValue == '0';
                        G560.Sound.playCallDealer(Method.getLocalPos(this.side), newValue)
                    }
                }
                params.watch.letcard = function (newValue) {
                    // console.log(newValue, "=========让牌");
                    this.hidetge();
                    let self = <playerTemplateData>this;
                    let tagnot = self.getComponent('tag_landloed_nolet');
                    let tagtwocard = self.getComponent('tag_landloed_lettwo');
                    if (newValue == null) {
                        tagnot.visible = false;
                        tagtwocard.visible = false;
                    }
                    else {
                        tagnot.visible = newValue == '0';
                        tagtwocard.visible = newValue == '2';
                    }
                }
                params.watch.boomCount = function (newValue) {
                    let self = <playerTemplateData>this;
                    self.getComponent('tfBoom').text = newValue ? 'x' + newValue : 0;
                    self.getComponent('groupBoom').visible = Boolean(newValue);
                }
                //method///////////////////////////////////////////////////////////////////////
                params.method.reset = function (newValue) {
                    //console.log("==========reset======570")
                    let self = <playerTemplateData>this;
                    self.isReady = null;
                    self.online = null;
                    self.isShowHandCount = null;
                    self.isDouble = null;
                    self.isLandLord2 = null;
                    self.letcard = null;
                    self.callLandLord = null;
                    self.isTrustee = null;
                    self.countdown = null;
                    self.cardsEnabled = null;
                    self.boomCount = 0;
                    self.isDealer = null;
                    self.boomMultiple = 0;

                    self.handwall.reset();
                    self.getComponent('tf_ready').visible = false;
                    self.getComponent('icon_handwall').visible = false;
                    self.getComponent('tf_handCount').visible = false;
                }

                params.method.hidetge = function (newValue) {
                    // console.log("======全部隐藏=====");
                    let self = <playerTemplateData>this;
                    let tag = self.getComponent('tag');
                    for (let i = 0; i < tag.numChildren; i++) {
                        tag.getChildAt(i).visible = false;
                    }
                }

                params.method.hidetge = function (newValue) {
                    // console.log("======全部隐藏=====");
                    let self = <playerTemplateData>this;
                    let tag = self.getComponent('tag');
                    for (let i = 0; i < tag.numChildren; i++) {
                        tag.getChildAt(i).visible = false;
                    }
                }

                params.method.setcallLandLord = function (newValue) {
                    //  console.log("==抢地主==", newValue);
                    this.hidetge();
                    let self = <playerTemplateData>this;
                    let tagNo = self.getComponent('tag_landlord_norob');
                    let tagYes = self.getComponent('tag_landlord_yes');
                    if (newValue === null) {
                        tagYes.visible = false;
                        tagNo.visible = false;
                    } else {
                        tagYes.visible = newValue == '1';
                        tagNo.visible = newValue == '0';
                        G560.Sound.playRobLandlord(Method.getLocalPos(this.side), newValue);
                    }
                }

                params.method.discard = function (data, cb) {
                    let self = <playerTemplateData>this;

                    // console.log("-------discard---------", data);
                    this.clearActionTips();
                    let discardList: Array<string> = data['discardList'].concat();
                    if (Method.getLocalPos(this.side) != 0) {
                        for (let i = 0; i < discardList.length; i++)
                            discardList[i] = 'card_backface';
                    }
                    self.handwall.remove(discardList);
                    let outList = data.cp1.getShowCardIdList();
                    self.handwall.out(outList);
                    // console.log(data.isShowEffect, "=============data.isShowEffect");
                    if (data.isShowEffect)
                        this.showCardEffect(data.pos2, data.cp1, data.cp2, cb);
                    else
                        cb();
                    // if(data.isShowEffect)
                    //     this.showCardEffect(data.pos2, data.cp1, data.cp2, cb);
                    // else
                    //     cb();
                    cb()
                }

                return new Vuet(params);
            }
        }
    }
}
