/*
* name;
*/
class Tools {
    private static _inst: Tools = null;
    public static get inst(): Tools {
        if (Tools._inst == null) {
            Tools._inst = new Tools();
        }
        return Tools._inst;
    }

    each(obj, iterator: (value: any, key?: any) => void, context: any = this) {
        if (!obj) return;
        if (obj instanceof Array) {
            for (var i = 0, li = obj.length; i < li; i++) {
                if (iterator.call(context, obj[i], i) === false)
                    return;
            }
        } else {
            for (var key in obj) {
                if (iterator.call(context, obj[key], key) === false)
                    return;
            }
        }
    }

    removeElement(arr, ele) {
        var idx = arr.indexOf(ele);
        if (idx == -1) return;
        arr.splice(idx, 1);
    }

    //随机整数
    randomInt(min, max) {
        return Math.floor(min + Math.random() * (max - min + 1));
    }
    //时间四舍五入
    timeinteger(time: number) {
        let num = time / 1000;
        num = Math.floor(num + 0.5);
        return num;
    }

    //克隆数据，不复制方法属性
    cloneObject(src) {
        var dst = null;
        if (src instanceof Array)
            dst = [];
        else
            dst = {};

        var self = arguments.callee;
        this.each(src, function (v, k) {
            if (v instanceof Function)
                return;
            if (v instanceof Object || v instanceof Array)
                dst[k] = self.call(null, v);
            else
                dst[k] = v;
        });
        return dst;
    }

    //设置昵称缩略
    abbreviateNickname(str, maxWidth = 90, fontSize = 20) {
        var tf: Laya.Text = new Laya.Text();
        tf.fontSize = fontSize; tf.text = str;
        var tfWidth = tf.textWidth;
        if (tfWidth > maxWidth) {
            var length = str.length;
            for (var i = 1; i < length; i++) {
                var newStr = str.slice(0, (length - i)) + "…";
                tf.text = newStr; tfWidth = tf.textWidth;
                if (tfWidth < maxWidth) {
                    return newStr;
                }
            }
        } else {
            return str;
        }
    }
    setNickname(label, nickname) {
        label.text = this.abbreviateNickname(nickname, label.width, label.fontSize);
    }
    //取名字的后八位
    SetNickNameAfter(label, nickname, maxWidth = label.width, fontSize = label.fontSize) {

        let length = nickname.length
        if (length <= 8) {
            label.text = nickname;
        }
        else {
            let str = nickname.slice(length - 8, length);
            label.text = str;
            var tf: Laya.Text = new Laya.Text();
            tf.fontSize = fontSize;
            tf.text = str;
            var tfWidth = tf.textWidth;
            if (tfWidth > maxWidth) {
                for (let i = 0; i < tfWidth; i++) {
                    if (tf.textWidth > label.width) {
                        tf.fontSize--;
                    } else {
                        break;
                    }

                }
                label.fontSize = tf.fontSize;
            }
        }
    }

    private static _timeoutCache = [];
    public static get timeoutCache() {
        return Tools._timeoutCache;
    }
    setTimeout(handler: any, timeout?: any, ...args: any[]): number {
        var id = setTimeout(handler, timeout, ...args);
        Tools.timeoutCache.push(id);
        return id;
    }
    clearAllTimeout() {
        this.each(Tools.timeoutCache, function (v, k) {
            clearTimeout(v);
        });
    }

    changeBackground(url, bg) {
        var tex = Laya.loader.getRes(url);
        if (tex) {
            bg.onExternalLoadSuccess(tex);
        } else
            Laya.loader.load(url, Handler.create(this, function (tex) {
                bg.onExternalLoadSuccess(tex);
            }));
    }

    /**给头像的装载器赋值 在服务器发过来的url无法成功加载时 加载本地的头像图片
     * @param url 服务器发过来的url
     * @param Gloader 装载器
     */
    changeHeadIcon(url: string, Gloader) {
        //如果已经有缓存直接赋值
        let texture = Laya.loader.getRes(url);
        if (texture != null) {
            Gloader.onExternalLoadSuccess(texture);
        } else {
            //如果没有缓存就加载
            Laya.loader.load(url, Handler.create(Gloader, function (texture) {
                //加载成功
                if (texture != null) {
                    this.onExternalLoadSuccess(texture);
                } else {
                    //加载失败 获取本地的头像图片
                    let index1 = url.lastIndexOf('/') + 1;
                    let index2 = url.lastIndexOf('.');
                    let str = url.substring(index1, index2);
                    let newUrl = ResourceMgr.RES_PATH+'portrait/' + str + '.png';
                    Tools.inst.changeBackground(newUrl, Gloader);
                }
            }));
        }
    }

    changeGoldToMoney(gold: any, def: string = '0') {
        if (gold == '') {
            if (def != '0')
                return def;
        }

        var money: number = parseFloat(parseFloat(gold).toFixed(2));
        //console.log("money: "+money);
        if (UserMgr.inst.exchangRate) {
            money *= UserMgr.inst.exchangRate;
            // money *= 0.8519;
        }
        var moneyStr = parseFloat(money.toFixed(2)).toString();
        var rex = /\d{1,3}(?=(\d{3})+$)/g;

        return moneyStr.replace(/^(-?)(\d+)((\.\d+)?)$/, function (s, s1, s2, s3) {
            var result = '' + s1 + s2.replace(rex, '$&,') + s3;
            //console.log("result moneyStr: "+result);
            return result;
        })
    }
    changeMoneyToGold(money: any = '0') {
        var goldStr = (money + '').replaceAll(',', '');
        return parseFloat(goldStr);
    }
    //取小数点后一位
    TableParseFloat(num: number) {
        return Math.floor(num * 10) / 10;
    }

    maskUserName(name: string,count:number = 3): string {
        var result: string = "";
        if (name.length > count) {
            result = "*****" + name.substring(name.length - count, name.length + 1);
        }
        else {
            result = "*****";
        }
        //console.log(name + " / "+ result);
        return result;
    }

    // /*{
    //     let a = [1, 2, 3, 4, 5]
    //     let i = 0;
    //     let is_interval = true;
    //     Tools.inst.interval(1000, 5, this, () => {
    //         if (is_interval) {
    //             console.log(a[i]);
    //             i++;
    //         }
    //     })
    // }*/
    // interval(time: number, num: number, caller: any, func: Function, args: Array<any> = []) {
    //     let index = 0;
    //     let cb = () => {
    //         func(...args);
    //         index++;
    //         if (index >= num) {
    //             Laya.timer.clear(caller, cb);
    //         }
    //     }
    //     Laya.timer.loop(time, caller, cb);
    // }
}

class FairyguiTools {
    /*返回使ui2移动到ui1位置需要的坐标*/
    static getOtherLocalPos(ui1: fairygui.GObject, ui2: fairygui.GObject) {
        let ui1Pos = ui1.parent.localToGlobal(ui1.x, ui1.y);
        return ui2.parent.globalToLocal(ui1Pos.x, ui1Pos.y);
    }

    /*改变父物体 使ui显示在屏幕中的位置不变*/
    static changeParentNotMove(parent: fairygui.GComponent, ui: fairygui.GObject) {
        let uiPos = FairyguiTools.getOtherLocalPos(parent, ui);
        ui.removeFromParent();
        parent.addChild(ui);
        ui.setXY(uiPos.x, uiPos.y);
    }

    /*逻辑屏幕坐标与UI元件坐标之间的转换*/
    static rootToLocal(ui: fairygui.GObject, pos: { x: number, y: number }) {
        let gPos = fairygui.GRoot.inst.localToGlobal(pos.x, pos.y);
        return ui.globalToLocal(gPos.x, gPos.y);
    }
    /*UI元件坐标与逻辑屏幕坐标之间的转换*/
    static localToRoot(ui: fairygui.GObject, pos: { x: number, y: number }) {
        let lPos = ui.localToGlobal(pos.x, pos.y);
        return fairygui.GRoot.inst.globalToLocal(lPos.x, lPos.y);
    }

}

class GObjectPool {
    private static _inst: GObjectPool = null;
    public static get inst(): GObjectPool {
        if (GObjectPool._inst == null) {
            GObjectPool._inst = new GObjectPool();
        }
        return GObjectPool._inst;
    }
    private constructor() {
    }
    private pool: { [key: string]: Array<fairygui.GObject> } = {};
    private map: { [key: string]: Array<fairygui.GObject> } = {};
    private ctorMap: { [key: string]: (...param: Array<any>) => fairygui.GObject } = {};
    clearPool() {
        for (const key in this.pool) {
            if (this.pool[key] != null) {
                for (const item of this.pool[key]) {
                    item.removeFromParent();
                    item.dispose();
                }
                this.pool[key] = null;
            }
        }
        for (const key in this.map) {
            if (this.map[key] != null) {
                for (const item of this.map[key]) {
                    item.removeFromParent();
                    item.dispose();
                }
                this.map[key] = null;
            }
        }
        for (const key in this.ctorMap) {
            if (this.ctorMap[key] != null) {
                this.ctorMap[key] = null;
            }
        }
    }
    getItemList(key: string) {
        return this.map[key];
    }
    getItemPool(key: string) {
        return this.pool[key];
    }
    setItemCtor(key: string, ctor: (...param: Array<any>) => fairygui.GObject) {
        if (this.ctorMap == null) {
            this.ctorMap[key] = ctor;
            this.pool[key] = [];
            this.map[key] = [];
        } else {
            console.warn(`ctorMap[${key}] is not null`);
        }
    }
    private addItem(key: string) {
        let item = this.ctorMap[key]();
        this.map[key].push(item);
        return item;
    }
    getItemFormPool(key: string) {
        if (this.pool[key] == null) {
            console.warn(`pool[${key}] is null `)
            return null;
        }
        let item: fairygui.GObject;
        if (this.pool[key].length > 0) {
            item = this.pool[key].shift();
            this.map[key].push(item);
        } else {
            if (this.ctorMap[key] == null) {
                console.warn(`ctorMap[${key}] is null `)
                return null;
            }
            item = this.addItem(key);
        }
        return item;
    }
    removeItemToPool(key: string, item: fairygui.GObject) {
        if (this.pool[key] == null) {
            this.pool[key] = [];
            this.map[key] = [];
        }
        let index = this.map[key].indexOf(item)
        if (index != -1) {
            this.map[key].splice(index, 1);
        }
        this.pool[key].push(item);
        item.removeFromParent();
        item.visible = false;
    }
}

class DealTilesTool {
    private static _inst: DealTilesTool = null;
    public static get inst(): DealTilesTool {
        if (DealTilesTool._inst == null) {
            DealTilesTool._inst = new DealTilesTool();
        }
        return DealTilesTool._inst;
    }
    private constructor() {
    }
    private playingObjList = [];
    /**
 * 使物体沿二阶贝塞尔曲线运动 同时改变缩放
 * @param obj 要移动的物体
 * @param startPoi 起点 global
 * @param ctrPois 中点 global
 * @param endPoi 终点 global
 * @param startScale 起始缩放
 * @param endScale 最终缩放
 * @param duration 持续时间 单位毫秒
 * @param callBack 回调函数
 * @param param 回调函数参数
 */
    dealTile(obj: fairygui.GObject, startPoi: { x: number, y: number }, ctrPois: { x: number, y: number }, endPoi: { x: number, y: number }, startScale: number, endScale: number, duration: number, delay: number, callBack?: (...param: Array<any>) => void, ...param: Array<any>) {
        {
            // let sp = new Laya.Sprite();
            // Laya.stage.addChild(sp);
            // let pois = [0, 0];
            // pois.push(ctrPois.x - startPoi.x);
            // pois.push(ctrPois.y - startPoi.y);
            // pois.push(endPoi.x - startPoi.x);
            // pois.push(endPoi.y - startPoi.y);
            // sp.graphics.drawCurves(startPoi.x, startPoi.y, pois, '#ff0000', 2);
        }
        let poiData: { p0_x: number, p0_y: number, p1_x: number, p1_y: number, p2_x: number, p2_y: number } = {
            p0_x: startPoi.x, p0_y: startPoi.y,
            p1_x: ctrPois.x, p1_y: ctrPois.y,
            p2_x: endPoi.x, p2_y: endPoi.y,
        };
        obj.setScale(startScale, startScale);
        obj.setXY(poiData.p0_x, poiData.p0_y);
        if (this.playingObjList.indexOf(obj) == -1) {
            this.playingObjList.push(obj);
        }
        this.dealTileUpdate(obj, 0, duration, poiData, startScale, endScale, (obj) => {
            let index = this.playingObjList.indexOf(obj);
            if (index != -1) {
                this.playingObjList.splice(index, 1);
            }
            let time = 0;
            let cb = () => {
                if (time < delay) {
                    time += Laya.timer.delta;
                    Laya.timer.frameOnce(1, this, cb);
                } else {
                    if (callBack != null) {
                        callBack(...param);
                    }
                }
            }
            cb();
        }, obj);
    }

    clear() {
        for (let i = 0; i < this.playingObjList.length; i++) {
            const obj = this.playingObjList[i];
            Laya.timer.clear(obj, this.dealTileUpdate);
            Laya.timer.clear(obj, this.changeScaleUpdate);
        }
        this.playingObjList.splice(0, this.playingObjList.length);
        Laya.timer.clearAll(this);
    }

    private dealTileUpdate = (obj: fairygui.GObject, time: number, duration: number, poiData: { p0_x: number, p0_y: number, p1_x: number, p1_y: number, p2_x: number, p2_y: number }, startScale: number, endScale: number, callBack?: (...param: Array<any>) => void, ...param: Array<any>) => {
        if (time < duration) {
            let t = time / duration;
            let pos = this.getBezierDot(t, poiData);
            obj.setXY(pos.x, pos.y);
            let scale = startScale + (endScale - startScale) * t;
            obj.setScale(scale, scale);
            time += Laya.timer.delta;
            Laya.timer.frameOnce(1, obj, this.dealTileUpdate, [obj, time, duration, poiData, startScale, endScale, callBack, ...param]);
        }
        else {
            obj.setXY(poiData.p2_x, poiData.p2_y);
            obj.setScale(endScale, endScale);
            Laya.timer.clear(obj, this.dealTileUpdate);
            if (callBack != null) {
                callBack(...param);
            }
        }
    }

    private changeScaleUpdate = (obj: fairygui.GObject, time: number, duration: number, startScale: number, endScale: number, callBack?: (...param: Array<any>) => void, ...param: Array<any>) => {
        if (time < duration) {
            let t = time / duration;
            let scale = startScale + (endScale - startScale) * this.easeOutQuad(t);
            obj.scaleX = scale;
            time += Laya.timer.delta;
            Laya.timer.frameOnce(1, obj, this.changeScaleUpdate, [obj, time, duration, startScale, endScale, callBack, ...param])
        }
        else {
            obj.scaleX = endScale;
            if (callBack != null) {
                callBack(...param);
            }
        }
    }

    showCard(obj: fairygui.GLoader, url: string, duration: number, delay: number, callBack?: (...param: Array<any>) => void, ...param: Array<any>) {
        if (this.playingObjList.indexOf(obj) == -1) {
            this.playingObjList.push(obj);
        }
        let startScale = obj.scaleX;
        obj.setPivot(0.5, 0.5);
        this.changeScaleUpdate(obj, 0, duration / 2, startScale, 0, () => {
            obj.url = url;
            this.changeScaleUpdate(obj, 0, duration / 2, 0, startScale, () => {
                let index = this.playingObjList.indexOf(obj);
                if (index != -1) {
                    this.playingObjList.splice(index, 1);
                }
                let time = 0;
                let cb = () => {
                    if (time < delay) {
                        time += Laya.timer.delta;
                        Laya.timer.frameOnce(1, this, cb);
                    } else {
                        if (callBack != null) {
                            callBack(...param);
                        }
                    }
                }
                cb();
            })
        })
    }

    private getBezierDot(t: number, obj: { p0_x: number, p0_y: number, p1_x: number, p1_y: number, p2_x: number, p2_y: number }) {
        let x = (1 - t) * (1 - t) * obj.p0_x + 2 * t * (1 - t) * obj.p1_x + t * t * obj.p2_x;
        let y = (1 - t) * (1 - t) * obj.p0_y + 2 * t * (1 - t) * obj.p1_y + t * t * obj.p2_y;
        return { x, y };
    }

    private easeOutQuad(x) {
        return 1 - (1 - x) * (1 - x)
    }
}