/*
* name;
*/
class UI_Portrait extends Widget{
    constructor(){
        super('Basic','Portrait',UILayer.POPUP);
        this.keepCenter();
        
        HttpMgr.inst.getHeaders(function(data){
            this.refreshList(data);
        }.bind(this));
    }
    
    onCreated(){
        var view = this._view;
        
        var subList = view.getChild('list').asList;

        subList.selectedIndex = 0;
        
        let btnSave = view.getChild('btn_save').asButton;
        btnSave.onClick(this,function(){
            // console.log(subList.selectedIndex+1);           
            var idx = subList.selectedIndex;
            var data = this.headData[idx];
            HttpMgr.inst.setHeaders(data['id'],function(res){
                EventMgr.emit('head_changed',res);
                this.onBack();
            }.bind(this));
        }.bind(this));
    }

    public headData=[];

    refreshList(data){
        var view = this._view;        
        var dataList = data['list'];
        this.headData = dataList;
        var subList = view.getChild('list').asList;
        for(var i = 0; i < subList.numChildren; ++i){
            var child = subList.getChildAt(i);
            var btn = child.asButton;
            if(btn != null){
                Tools.inst.changeHeadIcon(dataList[i]['url'],btn.getChild('icon'));
                //btn.icon = dataList[i]['url'];
            }
        }
    }
    
    onBack() {
        this.hide();
    }
}