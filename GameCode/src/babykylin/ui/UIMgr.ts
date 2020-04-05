/*
* name;
*/
class UIMgr {
    private static _inst: UIMgr = null;
    public static get inst(): UIMgr {
        if (UIMgr._inst == null) {
            UIMgr._inst = new UIMgr();
        }
        return UIMgr._inst;
    }

    public static alertClass: any;
    public static wcClass: any;

    private _layers: Array<fairygui.GComponent> = null;
    getLayer(layer: number): fairygui.GComponent {
        if (layer >= 0 && layer < this._layers.length) {
            return this._layers[layer];
        }
        return null;
    }

    configure(maxUILayer: number, alertClass: any, wcClass: any) {
        UIMgr.alertClass = alertClass;
        UIMgr.wcClass = wcClass;

        Laya.stage.addChild(fairygui.GRoot.inst.displayObject);

        //init layers of ui.
        this._layers = new Array<fairygui.GComponent>();
        for (let i = 0; i < maxUILayer; ++i) {
            let uiLayer = new fairygui.GComponent();
            uiLayer.setSize(fairygui.GRoot.inst.width, fairygui.GRoot.inst.height);
            fairygui.GRoot.inst.addChild(uiLayer);
            this._layers.push(uiLayer);
        }

        //handle resize event. keep the size of uilayers as the same as stage.
        Laya.stage.on(Laya.Event.RESIZE, this, () => {
            for (let i = 0; i < this._layers.length; ++i) {
                let uiLayer = this._layers[i];
                uiLayer.setSize(fairygui.GRoot.inst.width, fairygui.GRoot.inst.height);
            }
        });
    }

    setLayerMask(layer: number, packageName: string, compName: string) {
        var uiLayer = this._layers[layer];
        var comp = fairygui.UIPackage.createObject(packageName, compName).asCom;
        comp.addRelation(uiLayer, fairygui.RelationType.Size);
        uiLayer.addChildAt(comp, 0);
    }

    add(classOfWidget: any, parent: Widget = null, data: any = null): Widget {
        var w = new classOfWidget as Widget;
        if (!parent) {
            w.create(this.getLayer(w.layer), data);
        }
        else {
            w.create(parent.view, data);
        }
        return w;
    }

    clear() {
        Widget.clearPool();
    }

    popup(classOfWidget: any, maskAlpha: number = 0.6) {
        let mask: fairygui.GComponent = null;
        if (maskAlpha >= 0) {
            let comp = fairygui.UIPackage.createObject('Basic', 'LayerMask').asCom;
            comp.getChild('mask').asGraph.alpha = maskAlpha;
            mask = comp;
            mask.data = '#LayerMask'
        }
        var w = new classOfWidget as Widget;
        if (!mask) {
            w.create(this.getLayer(w.layer));
        }
        else {
            var uiLayer = this.getLayer(w.layer);
            mask.addRelation(uiLayer, fairygui.RelationType.Size);
            mask.width = uiLayer.width;
            mask.height = uiLayer.height;
            uiLayer.addChild(mask);
            w.create(mask);
        }
        return w;
    }

    
    /**加载牌类资源 */
    static loadTileRes(gameid: number, cb: () => void) 
    {
        ExtendMgr.inst.loadTileRes(gameid,cb);
        /*
        let map = {
            555: [UIMgr.dirnameTopkgNameMap['style0']],
            556: [UIMgr.dirnameTopkgNameMap['style0']],
            557: [UIMgr.dirnameTopkgNameMap['style0'], UIMgr.dirnameTopkgNameMap['cards']],
            559: [UIMgr.dirnameTopkgNameMap['FTLpoker']],
            560: [UIMgr.dirnameTopkgNameMap['FTLpoker']],
            561: [UIMgr.dirnameTopkgNameMap['style1']],
            563: [UIMgr.dirnameTopkgNameMap['style0']],
            445: ['MJtiles'],
            449: ['MJtiles'],
            452: ['MJtiles'],
            564: ['MJtiles'],
            570: [UIMgr.dirnameTopkgNameMap['FTLpoker']],
            666: [UIMgr.dirnameTopkgNameMap['style3']]
        }
        if (map[gameid]) {
            let resMap = [];
            let len = 0;
            for (let i = 0; i < map[gameid].length; i++) {
                const pkgName = map[gameid][i];
                resMap[pkgName] = [
                    { url: ResourceMgr.RES_PATH + uipath + '/' + pkgName + '.fui', type: Loader.BUFFER },
                    { url: ResourceMgr.RES_PATH + uipath + '/' + pkgName + '@atlas0.png', type: Loader.IMAGE }
                ];
                len++;
            }
            let index = 0;
            if (len > 0) {
                for (const pkgName in resMap) {
                    if (resMap.hasOwnProperty(pkgName)) {
                        const res = resMap[pkgName];
                        Laya.loader.load(res, Handler.create(this, (pkgName) => {
                            ExtendMgr.inst.fui[pkgName] = fairygui.UIPackage.addPackage(ResourceMgr.RES_PATH + uipath + '/' + pkgName);
                            index++;
                            //console.log('index, len', index, len);
                            if (index == len) {
                                cb();
                            }
                        }, [pkgName]));
                    }
                }
            } else {
                cb();
            }
        }
        else {
            console.log('map没有这个gameid', gameid);
            cb();
        }
        */
    }

    /**
     * 获得牌的url 需要已经加载过对应的.fui文件和图集
     * @param pkgName fairygui包名
     * @param resName 资源名 和原本读取外部资源时的文件名相同
     */
    static getTileUrl(pkgName: string, resName: string) {
        return fairygui.UIPackage.getItemURL(pkgName, resName);
    }

    /**
     * 给扑克牌的装载器赋值
     * @param loader 扑克牌的装载器
     * @param pkgName fairygui包名
     * @param resName 资源名 和原本读取外部资源时的文件名相同
     */
    static setPoker(loader: fairygui.GLoader, pkgName: string, resName: string) {
        loader.url = UIMgr.getTileUrl(pkgName, resName);
    }

}