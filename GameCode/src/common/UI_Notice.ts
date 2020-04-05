
class NoticeView extends Page{

    public static cur:NoticeView = null;
    private content:fairygui.GLabel = null;
    private rollBar:fairygui.GComponent = null;
    constructor(){
        super('Basic','NoticeView2',UILayer.NOTICE);
    }

    public static show(content:string){
        let view = UIMgr.inst.add(NoticeView) as NoticeView;
        view.setContext(content);
        view.run();
    }

    public static hide(){
        let view = NoticeView.cur;
        if(view){
            view.reset(); view.hide(); 
        }
        NoticeView.cur = null;
    }
    
    onCreated(){
        if(NoticeView.cur){
            NoticeView.cur.hide();
        }
        NoticeView.cur = this;
        this.rollBar = this._view.getChild('rollStr').asCom;
        this.content = this.rollBar.getChild('txt').asLabel;
    }

    setContext(content:string){
        this.content.text = content;
    }
    
    run(cb?){
        let content = this.content;
        if(!content)return;
        try {
            let complete = cb || Handler.create(this,function(){
                if(NoticeView.cur)NoticeView.cur.run();
            }.bind(this));
            var width = this.rollBar.width
            content.x = width;
            var duration = Math.min(15000,(width+content.width)*6);
            Laya.Tween.clearAll(content);
            Laya.Tween.to(content, {x: -content.width}, duration, null, complete);
        } catch (error) {
            console.log(error)
        }
    }

    private readyStringList = [];
    reset(){
        this.readyStringList = [];
        this.content.text = '';
        Laya.Tween.clearAll(this.content);
    }

    getNotice(){
        let readyList = this.readyStringList || [];
        if(readyList.length==0){
            return this.hide();
        }

        let oneData = readyList.shift();
        // let repeatInterval = oneData['repeatInterval'];
        this.content.text = oneData['content'];
        this.run(Handler.create(this,function(){
            if(NoticeView.cur)NoticeView.cur.getNotice();
        }.bind(this)));

        readyList.push(oneData);
    }
    
    public static addNotices(strList=[],clear=true){
        if(NoticeView.cur){
            NoticeView.cur.readyStringList =  strList;
            return;
        }
        let view = UIMgr.inst.add(NoticeView) as NoticeView;
        if(clear)view.reset();
        view.readyStringList =  strList;
        view.getNotice();
    }
}