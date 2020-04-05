/*
* name;
*/

class WC extends Page{
    public static cur:WC = null;
    private content:fairygui.GLabel = null;
    constructor(pkg:string,comp:string,layer:number){
        super(pkg,comp,layer);
    }

    public static show(content:string){
        let wc = UIMgr.inst.add(UIMgr.wcClass) as WC;
        wc.setContext(content);
    }

    public static hide(){
        if(WC.cur){
            WC.cur.hide();
            WC.cur = null;
        }
    }
    
    onCreated(){
        if(WC.cur){
            WC.cur.hide();
        }
        WC.cur = this;
        this.content = this._view.getChild('txt').asLabel;
    }

    setContext(content:string){
        this.content.text = content;
    }
}