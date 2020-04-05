/*
* name;
*/
class G564PlayerFrame extends G445PlayerFrame{
    
    private colorCtl:fairygui.Controller;

    constructor(components:Object){
        super(components);
        
        var component = components['seat'];
        this.colorCtl = component.getController('color');
    }
    
    resetGame(){
        super.resetGame();
        this.isHuState = false;
        this.colorCtl.setSelectedIndex(0);
    }
    
    public playDragDrop(tileComp:fairygui.GComponent,value): void {
        super.playDragDrop(tileComp,value);

        var btn=tileComp.asButton;
        btn.off(fairygui.Events.DRAG_START,this,this.__onDrag);
        btn.on(fairygui.Events.DRAG_START,this,this.__onDrag,[tileComp,value]); 
    }

    private isChangeTile=false;
    public setChangeTileState(state,lock){
        this.isChangeTile = state;
        this.LockTile(lock);
    }

    private __onDrag(tileComp,value):void {
        if(this.isChangeTile)tileComp.stopDrag(); 
    }

    public LockTile(Lock=true){
        if(this.side==0)
            this.hand_tiles.touchable = !Lock;
        // console.log('side:'+this.side,Lock);
    }
    
    getChoosedCount():number{
        var count=0;
        var outList = this.hand_tiles;
        for(var i = 0; i < outList.numChildren; ++i){
            let tileComp = outList.getChildAt(i).asCom;            
            var c = tileComp.getController('button');
            if(c && this.isChoosed(tileComp)){
                count++;
            }
        }
        return count;
    }
    
    onPokerClicked(tileComp:fairygui.GComponent){
        if(this.isChangeTile){
            var c = tileComp.getController('button');
            if(tileComp.y==0 && this.getChoosedCount()>=3)return;
            if(c){
                tileComp.y = (tileComp.y==0 ? this.tileOffsetY : 0);
            }
            tileComp.stopDrag(); 
            return;
        }
        super.onPokerClicked(tileComp);
    }
    
    sendDiscardCheck(value){
        if(value[0]!=this.ignoreColor){
            var outList = this.hand_tiles;
            for(var i = 0; i < outList.numChildren; ++i){
                let tileComp = outList.getChildAt(i).asCom; 
                if(tileComp.data[0] == this.ignoreColor){
                    Alert.show(ExtendMgr.inst.getText4Language('选缺的牌必须先出'));return;
                }
            }
        }
        super.sendDiscardCheck(value);
    }

    checkChoosed(){
        var count=0; var changeThrees=[];
        var outList = this.hand_tiles;
        for(var i = 0; i < outList.numChildren; ++i){
            let tileComp = outList.getChildAt(i).asCom; 
            var c = tileComp.getController('button');
            if(c && this.isChoosed(tileComp)){
                if(count>0 && tileComp.data[0]!=changeThrees[0][0]){
                    Alert.show(ExtendMgr.inst.getText4Language('换三张的牌必须是同一种花色'));return;
                }
                count++; changeThrees.push(tileComp.data);
            }
        }
        if(count<3){
            Alert.show(ExtendMgr.inst.getText4Language('牌数不足三张'));return;
        }
        NetHandlerMgr.netHandler.sendExchangeThree(changeThrees);
        return changeThrees;
    }

    finishChoosed(msgData){
        if(!msgData['result'])return;
        var changeThrees = msgData['tile'];
        if(changeThrees.length>2){
            this.LockTile(true);
            this.removeChoosed();
            this.removeHandTiles(msgData['tile']);
        }
    }
    
    public add3HandTiles(changeTiles){
        if(this.side>0){
            if(this.tilesDataHand.length>=13)return;
        }
        this.addHandTiles(changeTiles);
        if(this.side==0)
            Tools.inst.setTimeout(function(){
                this.sortHandTiles();
            }.bind(this),500);
    }
    
    private ignoreColor="";
    public setIgnoreColor(color){
        try {
            this.colorCtl.setSelectedPage(color);
            this.ignoreColor = color;
        } catch (error) {
            console.log(error)
        }
    }
    
    public isHuState=false;
    public hu(data, cb){
        this.setActionEffect(data['passivePlayer'] ? 3 :4);
        this.setHuState([data["tileData"]],false);

        if(data['passivePlayer']) SoundMgr.hu(this.sex);
        else SoundMgr.hu_origin(this.sex);
        SoundMgr.layTiles();
        
        if(cb)cb();
    }
    
    public addHuTiles(tiles,clear:boolean=false){
        var outList = this.hu_tiles;
        if(clear)outList.removeChildrenToPool();
        this.addTiles(tiles,outList);
    }

    public setHuState(tiles=[],clear=false){
        this.isHuState = true;
        this.LockTile(true);
        this.addHuTiles(tiles,clear);

        if(this.side==0)
            NetHandlerMgr.netHandler.sendOnProxy(1);
    }
}