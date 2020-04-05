/*
* name;
*/
class LayoutHallTitle{
    private gemsText:fairygui.GLabel;
    constructor(component:fairygui.GComponent){
        component.getChild('name').asLabel.text = UserMgr.inst._info.name + ' \nID:' + UserMgr.inst._info.userId;
        var url = UserMgr.inst._info.imgUrl;
        //url = HttpMgr.inst.url + '/image?url=' + encodeURIComponent(url) + '.jpg';
        component.getChild('icon').asLoader.url = url;
        this.gemsText = component.getChild('gems').asLabel;

        // component.getChild('name').asLabel.text = UserMgr.inst._info.name.substring(0,4);
    }

    refreshCashes(){
        this.gemsText.text = UserMgr.inst._info.coins.toString();
    }

    onBtnClicked(sender){
        console.log(sender.name);
    }
}