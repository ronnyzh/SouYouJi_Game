class Scene{
    private _isGameScene = false;
    private _designWidth = -1;
    private _designHeight = -1;

    constructor(designWidth=1334,designHeight=750,isGameScene = false){
    // constructor(designWidth=1600,designHeight=900,isGameScene = false){
        this._designWidth = designWidth;
        this._designHeight = designHeight;
        this._isGameScene = isGameScene;
        
        Laya.timer.loop(60000,this,this.refreshSession);
    }

    refreshSession(){
        // console.log('refreshSession');
        UserMgr.inst.refreshSession();
    }

    public get isGameScene(){
        return this._isGameScene;
    }

    getDesignResolution():Laya.Point{
        if(this._designHeight < 0 || this._designWidth < 0){
            return null;
        }
        return new Laya.Point(this._designWidth,this._designHeight);
    }

    getRes(){

    }
    
    start(){

    }

    update(){
    }

    end(){
        Laya.timer.clearAll(this);
    }
}