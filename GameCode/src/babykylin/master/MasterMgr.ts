
class MasterMgr{
    private static _inst:MasterMgr = null;
    public static get inst():MasterMgr{
        if(MasterMgr._inst == null){
            MasterMgr._inst = new MasterMgr();
        }
        return MasterMgr._inst;
    }

    private settings:any = null;
    private masterCache:any = {};
    private _current:Master = null;

    constructor(){
        this.settings = MasterSettings.masters;
    }
    
    public static get current(){
        return MasterMgr._inst._current;
    }
        
    switch(id,dontLoadScene=false,params=null){
        var cfg = this.settings[id];

        //console.log('switch ->',id,dontLoadScene,params);

        if(this._current && this._current.setting.id == id){
            console.log('no need switch.');
            return;
        }

        if(!cfg){
            console.log('can not find settings with id:',id);
            return false;
        }
        if(cfg.enable == false){
            return false;
        }

        cfg.id = id;


        if(this._current)
        {
            Tools.inst.clearAllTimeout();
            this._current.exit();
        }

        var MasterClass = cfg.master_script;
        this.masterCache[cfg.master_script] = new MasterClass();

        this._current = this.masterCache[cfg.master_script];
        this._current.setting = cfg;
        this._current.enter(params);
        if(cfg.entry_scene && !dontLoadScene)
        {
            SceneMgr.inst.replace(cfg.entry_scene);
        }

        return true;
    }
}