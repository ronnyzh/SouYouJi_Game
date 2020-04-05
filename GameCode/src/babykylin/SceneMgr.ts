/*
* name;
*/
class SceneMgr{
    private static _inst:SceneMgr = null;
    public static get inst():SceneMgr{
        if(SceneMgr._inst == null){
            SceneMgr._inst = new SceneMgr();
        }
        return SceneMgr._inst;
    }

    private _currentScene:Scene = null;
    public get currentScene(){ return this._currentScene; }
    constructor(){
        bk.registerUpdater(this,this.update);
    }

    start(typeOfScene:any){
        if(this._currentScene){
            throw new Error('SceneMgr:start can be called only once.');
        }
        this.replace(typeOfScene);
    }

    replace(typeOfScene:any){
        var nextScene = new typeOfScene();
        var size = nextScene.getDesignResolution();
        bk.setDesignResolution(size.x,size.y);
        
        var res = nextScene.getRes();
        if(res && res.length){
            Laya.loader.load(res,Handler.create(this, this.onLoaded,[nextScene]),Handler.create(this,this.onProgress,null,false));
        }
        else{
            this.onLoaded(nextScene);
        }
    }

    onLoaded(nextScene:Scene){
        //重置掉之前注册的事件
        bk.reset();
        if(this._currentScene){
            this._currentScene.end();
            UIMgr.inst.clear();
        }
        this._currentScene = nextScene;
        this._currentScene.start();
        EventMgr.emit('scene_switched');
    }

    onProgress(){

    }

    update(){
        if(this._currentScene){
            this._currentScene.update();
        }
    }
}