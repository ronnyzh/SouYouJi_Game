class MasterInfo{
    public static  COMMON:string = 'common';
    public static  SUB_GAME:string = 'subgame';


    public id:number = null;
    public type:string = null; //类别 common:普通 subgame子游戏
    public name:string = null; //名称 拿来看的
    public master_script:Master = null;//主逻辑
    public entry_scene:Scene = null; //入口场景，如果有，会在切换主逻辑的时候自动加载
    public game_scene:Scene = null;
    public extra:any = null;
    public enable:boolean = true;
    public frame_rate:string = bk.settings.frameRate;

    constructor(type,name,master_script,entry_scene,extra,frame_rate = bk.settings.frameRate){
        this.type = type;
        this.name = name;
        this.master_script = master_script;
        this.entry_scene = entry_scene;
        this.extra = extra;
    }
}