/*
* name;
*/
class UI_History extends Widget{
    constructor(){
        super('Basic','History',UILayer.POPUP);
        this.keepCenter();
    }
    
    public PageUp:fairygui.GButton = null;
    public PageDown:fairygui.GButton = null;
    public outList:fairygui.GList;
    private stateCrl:fairygui.Controller;

    onCreated(){
        var view = this._view;        
        //view.center();
        //this._view.displayObject.cacheAs = "normal";
        let btn_close = view.getChild('btn_close').asButton;
        btn_close.onClick(this,()=>{
            this.onBack();
        });
        
        this.outList = view.getChild('list').asList;
        this.stateCrl = view.getControllerAt(0);

        this.PageUp = view.getChild('PageUp').asButton;
        this.PageUp.onClick(this,()=>{
            this.refreshList(this.page_now-1);
        });
        this.PageDown = view.getChild('PageDown').asButton;
        this.PageDown.onClick(this,()=>{
            this.refreshList(this.page_now+1);
        });
    }

    private page_now=1;
    private gameID_now=null;
    refreshList(page=1,count=50){
        this.outList.removeChildrenToPool();
        var params:any = {index : page};
        if(this.gameID_now){
            params['game_id']=this.gameID_now;
            params['count']=count;
        }
        HttpMgr.inst.getHistorys(params,function(data){
            this.refreshData(data,page);
        }.bind(this));
    }

    refreshGameList(gameID,page?,count?){
        this.gameID_now=gameID;
        this.stateCrl.selectedIndex=(gameID ? 1 :0);
        this.refreshList(page,count);
    }

    refreshGameListInGame(gameID){
        this.PageUp.visible = false; this.PageDown.visible = false;
        this.refreshGameList(gameID,1,10);
    }

    refreshData(datas,page){
        //console.log(datas);
        this.page_now=page;
        this.PageUp.enabled = page>1;
        this.PageDown.enabled = datas['next']==1;
        
        var gameID = this.gameID_now;
        // this.stateCrl.selectedIndex=(gameID ? 1 :0);

        var outList = this.outList;
        var list = datas['data'];
        if(list == null || list.map == null)
        {
            return;
        }
        
        var count=1;
        list.map(item=>{
            // console.log(item);
            var component = outList.addItemFromPool().asCom;
            component.getChild('id').asLabel.text = ''+count;//item['id'];
            count++;

            var play_name = gameID?item['play_name']:item['gameName'];
            component.getChild('play_name').asLabel.text = ExtendMgr.inst.getText4Language(play_name);

            component.getChild('game_number').asLabel.text = item['game_number'];
            component.getChild('create_time').asLabel.text = item['create_time'];
            component.getChild('balance').asLabel.text = item['balance'];
            component.getControllerAt(0).selectedIndex=(Tools.inst.changeMoneyToGold(item['balance'])>0 ? 0 :1);
        })
    }
    
    onBack() {
        this.hide();
    }
}