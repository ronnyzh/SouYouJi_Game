/*
* name;
*/
class Widget{
    private static _pool:Array<Widget> = new Array<Widget>();
    private _relations:Array<number> = new Array<number>();
    private _component:string = null;
    private _package:string = null;
    private _timer:number = -1;
    
    protected _view:fairygui.GComponent = null;
    protected _layer:number = 0;

    /**
     * 
     * @param pkg   FairyGUI包名
     * @param comp  FairyGUI组件名
     * @param layer UI层级
     */
    constructor(pkg,comp,layer){
        this._package = pkg;
        this._component = comp;
        
        Widget._pool.push(this);
    }

    public static clearPool(){
        while(Widget._pool.length){
            let w = Widget._pool[0];
            w.hide();
        }
    }

    public hide()
    {
        var root = this._view;
        if(!root || !root.parent)
        {
            return;
        }
        //如果是MASK，则需要移除
        if(root.parent.data){
            root = root.parent;
        }

        if(root.parent)
        {
            root.removeFromParent();
        }

        if(root)
        {
            for(var i = 0; i<root.numChildren; i++)
            {
                var com = root.getChildAt(i).asCom;
                var btn = com.asButton;
                if(btn)
                {
                    btn.mode = -1;
                }

                if(com.numChildren > 0)
                {
                    for(var j = 0; j<com.numChildren; j++)
                    {
                        var btn2 = com.getChildAt(j).asButton;
                        if(btn2)
                        {
                            btn2.mode = -1;
                        }
                    }
                }
            }
            //root.dispose();
            root.visible = false;
        }

        var idx = Widget._pool.indexOf(this);
        Widget._pool.splice(idx,1);
        this.onDispose();
        clearInterval(this._timer);

        Laya.stage.off(Laya.Event.RESIZE,this,this.onResize);
        Laya.timer.once(1500,this,function()
        {
            root.dispose();
        });
    }

    get package():string{
        return this._package;
    }
    get component():string{
        return this._component;
    }

    get view(){
        return this._view;
    }

    get layer(){
        return this._layer;
    }

    protected keepSize(){
        this.addRelation(fairygui.RelationType.Size);
        Laya.stage.on(Laya.Event.RESIZE,this,this.onResize);
    }

    protected keepCenter(){
        this.addRelation(fairygui.RelationType.Center_Center);
        this.addRelation(fairygui.RelationType.Middle_Middle);
    }

    protected addRelation(relationType:number){
        this._relations.push(relationType);
    }
    
    create(parent:fairygui.GComponent,data:any = null){
         //console.log('create:',this._package,this._component)
        try 
        {
            let obj = fairygui.UIPackage.createObject(this._package,this._component);
            let view = obj.asCom;
            if(!view)return;
            this._view = view;
            this.resize(parent,obj);
            /*
            for(let i = 0; i < this._relations.length; ++i){
                let rt = this._relations[i];
                this._view.addRelation(parent,rt);
                if(rt == fairygui.RelationType.Size){
                    this._view.setSize(parent.width,parent.height);
                }
                else if(rt == fairygui.RelationType.Center_Center){
                    var y = parent.height/2 -  obj.height/2;
                    obj.y = y;
                }
                else if(rt == fairygui.RelationType.Middle_Middle){
                    var x = parent.width/2 -  obj.width/2;
                    obj.x = x;
                }
            }
            */
            parent.addChild(this._view);
            this.onCreated(data);
        } catch (error) {
            console.log('create error: ',error)
        }
    }

    private resize(parent:fairygui.GComponent,obj:fairygui.GObject)
    {
            for(let i = 0; i < this._relations.length; ++i){
                let rt = this._relations[i];
                this._view.addRelation(parent,rt);
                if(rt == fairygui.RelationType.Size){
                    this._view.setSize(parent.width,parent.height);
                }
                else if(rt == fairygui.RelationType.Center_Center){
                    var y = parent.height/2 -  obj.height/2;
                    obj.y = y;
                }
                else if(rt == fairygui.RelationType.Middle_Middle){
                    var x = parent.width/2 -  obj.width/2;
                    obj.x = x;
                }
            }
    }

    onResize()
    {
        if(this._view.parent)
        {
            let parent = this._view.parent;

            //this.hide();

            //let obj = fairygui.UIPackage.createObject(this._package,this._component);
            //let view = obj.asCom;
            //if(!view)return;
            //this._view = view;

            this.resize(parent,this._view);

            //parent.addChild(this._view);
            //this.onCreated(null);
            ////////////////////////////////////////////////////////////////
            //window.location.reload(true);
        }
    }

    protected listenButtons(btnList,handler:Function){
        for(let i = 0; i < btnList.length;++i){
            let btnName = btnList[i];
            this._view.getChild(btnName).asButton.onClick(this,handler,[btnName]);
        }
    }

    //开启界面更新。 （由于不是每一个界面都需要更新。所以，界面更新需要由子界面自己开启。)
    protected startUpdate(interval){
        if(this._timer){
            clearInterval(this._timer);
        }
        var self = this;
        this._timer = setInterval(function(){
            self.onUpdate();
        },interval);
    }

    onCreated(data:any = null){}
    onDispose(){}
    onUpdate(){}
}