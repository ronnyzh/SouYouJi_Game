/*
* JiaTao 2018-12-8 15:06;路单
*/
class WaybillPage
{
    private roomListInfo : any;
    private view : fairygui.GComponent;
    private roomList : fairygui.GComponent;
    private chooseCom : fairygui.GComponent;
    private dataCache:any;

    public onClickEnterGame : any;

    onCreate(view:fairygui.GComponent,data:any)
    {
        if(view==null||data==null)return;
        
        this.view = view;
        this.roomListInfo = data;
        this.roomList = view.getChild('roomList').asCom;
        this.chooseCom = view.getChild('chooseCom').asCom
        this.refreshLeftRoomList(this.roomListInfo);
        this.OpenRefresh(true);
    }

    initRightWaybillInfo(msg)
    {
        let data = msg['data'];

        if(this.roomList==null||!data||!data.length)return;
        this.dataCache = data;

        let roomList = this.roomList.getChild('roomList').asList;
        roomList.removeChildrenToPool();
        //roomList.numItems = data.length;
        for(let i = 0;i<data.length; ++i)
        {
            roomList.addItemFromPool().asCom;
        }

        for(let i = 0; i < data.length; ++i)
        {
            let dat = data[i];
            let listItem = roomList.getChildAt(i).asCom;
            //-------初始化房间信息 playerCount
            let playId = parseInt(dat['playId']);
            let level = ['X','P','Z','G','T'];
            let txt_roomInfo = listItem.getChild('txt_roomInfo').asLabel;
            let roomInfo = level[playId] + data[i]['roomId'];
            txt_roomInfo.text = roomInfo;
            let playerCount = dat['playerCount'];

            //-------下面是路单小方格初始化 
            let ludanList = data[i]['ludanList'];
            if(ludanList.length>0)
            {
                this.initSubBox(ludanList,listItem);
            }
            else
            {
                let subBoxList = listItem.getChild('subBoxList').asList;
                //subBoxList.numItems = 150;
                subBoxList.removeChildrenToPool();
                for(let i = 0;i<150; ++i)
                {
                    let box = subBoxList.addItemFromPool().asCom;
                    box.getController('c_win').selectedIndex = 0;
                    box.getController('c_he').selectedIndex = 0;
                    box.getController('c_point').selectedIndex =0;
                }
            }
            //-------在这里绑定进入游戏按钮
            //let btn_enterGame = listItem.getChild('btn_enterGame').asButton;
            if(playerCount=='9'||playerCount==9)
            {
                listItem.offClick(this,this.onClick1)
                listItem.onClick(this,this.onClick1);
            }
            else
            {
                listItem.offClick(this,this.onClick2);
                listItem.onClick(this,this.onClick2,[data,i]);
            }
        }
    }

    private onClick1()
    {
        Alert.show(ExtendMgr.inst.getText4Language('房间人数已满'));
    }

    private onClick2(data,i)
    {
        let level = this.chooseCom.getController('choose').selectedIndex;
        let roomId = data[i]['roomId'];
        //console.log('进入游戏按钮被点击',data,level,roomId);
        if(this.onClickEnterGame)
        {
            this.onClickEnterGame(level,roomId);
        }
    }

    initSubBox(ludanList,listItem:fairygui.GComponent)
    {
            let titleBg = listItem.getChild('titleBg').asImage;
            let subBoxList = listItem.getChild('subBoxList').asList;//----------
            //subBoxList.numItems = 150;
            subBoxList.removeChildrenToPool();
            for(let i = 0;i<150; ++i)
            {
                let box = subBoxList.addItemFromPool().asCom;//----------
                box.getController('c_win').selectedIndex = 0;
                box.getController('c_he').selectedIndex = 0;
                box.getController('c_point').selectedIndex =0;
            }

            //let firstLineNum = ludanList[0].length;//subBoxList
            let maxLineNum = ludanList[0].length;
            for(let i = 0,len = ludanList.length; i < len; ++i){
                let lineNum = ludanList[i].length;
                maxLineNum = maxLineNum > lineNum ? maxLineNum:lineNum;
            }
            let hideIndex = 0;
            if(maxLineNum>25){
                hideIndex = maxLineNum-25;
            }
            
            for(let i = 0,len1 = ludanList.length; i < len1; ++i)
            {
                for(let j = 0,len2 = ludanList[i].length; j < len2; ++j)
                {
                    if(j < hideIndex) continue;
                    let index = (j-hideIndex)+25*i;//----------
                    let box = subBoxList.getChildAt(index).asCom;//----------
                    let value = ludanList[i][j];
                    let winType = 0;
                    let heType = 0;
                    let pointType = 0;//默认设置控制器索引为10,不显示任何点数.
                    if(value!='-')
                    {
                        let str = value.split('');
                        if(str[0]=='0'){//---开局第一局或前几局都是和
                            heType = 1;//2019-1-9
                            winType = 3;//c_win 3 表示和赢 显示绿圈
                        }else{
                            winType = parseInt(str[0]);
                            let point = parseInt(str[1]);//----------
                            pointType = point==0 ? 10 : point;//----------
                        }
                    }
                    let c_win = box.getController('c_win');
                    let c_he = box.getController('c_he');
                    let c_point = box.getController('c_point');
                    c_he.selectedIndex = heType;
                    c_point.selectedIndex = pointType;
                    c_win.selectedIndex = winType;//和显示绿圈
                }
            } 
    }


    //初始化左半边数据信息
    refreshLeftRoomList(data)
    {
        if(!data) return;
            for(let i = 1; i < 5; ++i)
            {
                let name = 'btn_choose_s' + i;
                let chooseCom = this.chooseCom.getChild(name).asCom;
                let txt_online_lan = chooseCom.getChild('txt_online_lan').asLabel;
                let txt_limitScore_lan = chooseCom.getChild('txt_limitScore_lan').asLabel;
                let txt_baseScore_lan = chooseCom.getChild('txt_baseScore_lan').asLabel;
                let txt_online_bai = chooseCom.getChild('txt_online_bai').asLabel;
                let txt_limitScore_bai = chooseCom.getChild('txt_limitScore_bai').asLabel;
                let txt_baseScore_bai = chooseCom.getChild('txt_baseScore_bai').asLabel;
                let info = data[i];
                /*
                txt_online_lan.text = (info['online'] as number).toString();
                txt_limitScore_lan.text = (info['need'][0] as number).toString();
                txt_baseScore_lan.text = info['baseScore'];
                txt_online_bai.text = (info['online'] as number).toString();
                txt_limitScore_bai.text = (info['need'][0] as number).toString();
                txt_baseScore_bai.text = info['baseScore'];
                */

                txt_online_lan.text = txt_online_bai.text = (info['online'] as number).toString();
                txt_limitScore_lan.text = txt_limitScore_bai.text = Tools.inst.changeGoldToMoney(info['need'][0]);
                txt_baseScore_lan.text = txt_baseScore_bai.text = Tools.inst.changeGoldToMoney(info['baseScore']);

                //------给左边场次按钮绑定回调函数
                let btn_choose = this.chooseCom.getChild(name).asButton;
                btn_choose.onClick(this,()=>{
                    //console.log('请求服务器接口');
                    HttpMgr.inst.getBaccaratRoomsList(i,this.initRightWaybillInfo.bind(this));
                });
            }
        //----------请求右边房间路单信息;
        Laya.timer.once(400,this,function():void
        {
            HttpMgr.inst.getBaccaratRoomsList(this.chooseCom.getController('choose').selectedIndex,this.initRightWaybillInfo.bind(this));
        });
        
        this.OpenRefresh(true);
    }

    OpenRefresh(isOpen:boolean)
    {
        Laya.timer.clear(this,this.refresh);
        
        if(!isOpen)   return;
        
        Laya.timer.loop(5000,this,this.refresh);//5秒刷新一次路单信息
    }

    refresh()
    {
        let rank = this.chooseCom.getController('choose').selectedIndex;
        HttpMgr.inst.getBaccaratRoomsList(rank,this.initRightWaybillInfo.bind(this));
    }

    //退出清理函数
    destroy()
    {
        this.OpenRefresh(false);
        //if(this.view!=null)
            //this.view.removeFromParent();
    }
}