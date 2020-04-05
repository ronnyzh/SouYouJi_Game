/*
* name;
*/
class UI_Rules extends Widget
{
    constructor()
    {
        super('Basic','Rules',UILayer.POPUP);
        this.keepCenter();
    }
    
    private content_image:fairygui.GLoader;
    private subList:fairygui.GList;

    onCreated()
    {
        var view = this._view;
        this._view.displayObject.cacheAs = "bitmap";
        this.subList = view.getChild('list').asList;
        var child = this.subList.getChildAt(0).asCom;
        
        if(this.content_image)
            this.content_image.visible=false;
        
        let btn_close = view.getChild('btn_close').asButton;
        btn_close.onClick(this,()=>{
            this.onBack();
        });
    }

    refreshData(gameID)
    {
        var url = ResourceMgr.TEXT_RES_PATH+'rule/'+gameID;
        switch(ExtendMgr.inst.lan)
        {
            case ExtendMgr.EN:
                url = ResourceMgr.TEXT_RES_PATH+'rule_en/'+gameID;
            break;
            case ExtendMgr.CN:
                url = ResourceMgr.TEXT_RES_PATH+'rule/'+gameID;
            break;
        }

        Laya.loader.load(url,Handler.create(this,function()
        {
            let itemUrl = 'ui://la8oslyogjn8kf';
            new Rule(this.subList,url,itemUrl);
        }.bind(this)),null,Loader.JSON);
    }
    
    resetList(list:fairygui.GList)
    {
        if(list)
        {
            list.numItems = 0;
            list.numChildren = 0;
        }

        if(Rule.RenderHandler)
        {
            Rule.RenderHandler.recover();
            Rule.LHIndex = 0;
        }
    }

    onBack() 
    {
        this.resetList(this.subList);
        this.subList.removeChildren();
        this.hide();
    }
}


class Rule
{
    public static LHIndex : number = 0;
    public static RenderHandler : Handler;

    private _view: fairygui.GComponent;
    private _list:fairygui.GList;

    private _LineHeight :  Array<any> = [];   
    
    private detail : any;
    public constructor(List:fairygui.GList,jsonUrl:string,itemUrl:string) {

        if(List.numItems>0){
            Rule.LHIndex = 0;
        }

        let url = List.defaultItem;
        //fairygui.UIObjectFactory.setPackageItemExtension(itemUrl, richText);//itemUrl tichText类
        //---------JiaTao
        let jsonUBB = Laya.loader.getRes(jsonUrl);
        //console.log('jsonUBB===',jsonUBB);
        let detail = jsonUBB['detail'];
        this.detail = detail;//JiaTao
        // let totalLine = detail[0]['totalLine'];
        let totalColumn = detail[0]['totalColumn'];
        let totalLine = (detail.length-1)/totalColumn;
        //console.log('寒山寺',totalLine);
        let totalItem = totalLine*totalColumn;
        this.initItemHeight(detail);
        //console.log('行数',totalLine,'列数',totalColumn,'itme数',totalItem);
        this._list = List;
        this._list.columnCount = totalColumn;//设置列数
        //this._list.lineCount = totalLine;//设置行数
        this._list.lineGap = 5;//设置行距
        this._list.columnGap = -35;//设置列距
        Rule.RenderHandler = Handler.create(this, this.renderListItemRich, null, false);
        this._list.itemRenderer = Rule.RenderHandler;//指定列表渲染函数
        this._list.numItems = totalItem;//设置item数 列表为横向流动，所以，只设置列数和item总数，行数不用设置.
    }
    //获取表格item格式 即每个单元格的宽 高
    initItemHeight(obj){
        let detail = obj;
        for(let i = 1; i < detail.length; ++i){
            let line = detail[i]['line'];
            line = parseInt(line);
            this._LineHeight.push(line);
            let itemStyle = detail[i]['itemStyle'];
            this._itemStyle.push(itemStyle);
        }
    }
    private _itemStyle : Array<any> = [];
    private static  _RICount: number = 0;
    private renderListItemRich(index:number, obj:fairygui.GObject):void {
        //这里obj是richText
        let height = 25*this._LineHeight[Rule.LHIndex];
        obj.height = height;
        let width = 40*this._itemStyle[Rule.LHIndex];
        obj.width = width;
        Rule.LHIndex++;
        this.initContent(index,this.detail,obj.asCom.getChildAt(0).asRichTextField);
    }

   public initContent(index:number,detail,title:fairygui.GRichTextField)
    {
        let ind = index + 1;
        let type = detail[ind]['type'];//item渲染类型 1大标题2小标题3段落4表格5图片(暂未开发)
        let ubb_itemWidth = detail[ind]['itemWidth'];//item宽度
        let ubb_itemHeight = detail[ind]['itemHeight'];//item高度
        let ubb_fontSize = detail[ind]['fontSize'];//字体大小
        let ubb_content = detail[ind]['content'];//item文本内容
        if(type==1){//大标题
            let format_content = '<font style="fontSize:22" color = "#FFD800">'+ubb_content+'</font>';
            if(ubb_fontSize){
                format_content = '<font style="fontSize:'+ubb_fontSize+'" color = "#FFD800">'+ubb_content+'</font>';
            }
            title.text = format_content;
            title.width = 200;//---默认item宽度
        }else if(type==2){//小标题 标签
            let format_content = '<font style="fontSize:20" color = "#00EAFF">'+ubb_content+'</font>';
            if(ubb_fontSize){
                format_content = '<font style="fontSize:'+ubb_fontSize+'" color = "#00EAFF">'+ubb_content+'</font>';
            }
            title.text = format_content;
            title.width = 90;//---默认item宽度
        }else if(type==3){//段落
            let format_content = '<font style="fontSize:20" color = "#FFFFFF">'+ubb_content+'</font>';
            if(ubb_fontSize){
                format_content = '<font style="fontSize:'+ubb_fontSize+'" color = "#FFFFFF">'+ubb_content+'</font>';
            }
            title.text = format_content;
            title.width = 500;//---默认item宽度
        }else if(type==4){//表格
            let isTitle = detail[ind]['isTitle'];
            let format_content = '';
            if(isTitle){
                format_content = '<font style="fontSize:20" color = "#00EAFF">'+ubb_content+'</font>';
                if(ubb_fontSize){
                    format_content = '<font style="fontSize:'+ubb_fontSize+'" color = "#00EAFF">'+ubb_content+'</font>';
                }
            }else{
                format_content = '<font style="fontSize:20" color = "#FFFFFF">'+ubb_content+'</font>';
                if(ubb_fontSize){
                    format_content = '<font style="fontSize:'+ubb_fontSize+'" color = "#FFFFFF">'+ubb_content+'</font>';
                }
            }
            title.text = format_content;
            title.width = 260;//-----默认item宽度
        }//type==4结尾
        if(ubb_itemWidth){
            title.width = ubb_itemWidth;
        }
        if(ubb_itemHeight){
            title.height = ubb_itemHeight;
        }
    }

    dispose(){
        
    }
}


