/*
* name;
*/
class LoginPage extends Page
{
    constructor(){
        super('Login','PageLogin',UILayer.GAME);
    }
    
    private is_guest=TestMgr.IS_REAL_ACCOUNT;
    private is_auto=TestMgr.IS_REAL_ACCOUNT;
    private is_encryption=TestMgr.IS_REAL_ACCOUNT;

    onCreated(data:any=null)
    {
        var url = ResourceMgr.RES_PATH+'bg/lodingBg.jpg';
        var gamePageC = this._view.getController('c1');

        Tools.inst.changeBackground(url,this._view.getChild('bg').asLoader);
        Tools.inst.changeBackground(url,this._view.getChild('bgadd').asLoader);
        gamePageC.selectedIndex = getLoginType();

        if(gamePageC.selectedIndex == 2)
        {
            var txt_account = this._view.getChild('txt_account').asLabel;
            var txt_pass = this._view.getChild('txt_pass').asLabel;

            txt_account.text = Laya.LocalStorage.getItem('account') || '';
            txt_pass.text = Laya.LocalStorage.getItem('password') || '';
            
            this._view.getChild('btn_login').asButton.onClick(this,()=>{
                UserMgr.inst.login(txt_account.text,txt_pass.text);
            });

            return;
        }

        if(location_search_account){
            UserMgr.inst.doLoginAsGuest2(location_search_account);
            return;
        }
        
        gamePageC.selectedIndex = 1;
        this._view.getChild('btn_guest').asButton.onClick(this,()=>{

            let index = location_random_account || Tools.inst.randomInt(0,TestAccounts.length-1);
            let account = TestAccounts[index];  //index
            location_random_index = index;
            //let account = "qs1kxh3B6PGAScTaY05GMwPZs5UFVTMBE+lpm/MdPw70Q/zkUvAZrNm0ga8ycWe+Y6Cg35FqhPKTPsp6+/h7xHdJsGpcYrKCuMSoLue2YpdW5tpf05sZjqg6MKZUIsMGoOBAMboSuBWEApMT6NmEvcNO18RrxeJ/T7MZVBgkN3IVf96EQRORnPLkXmn6j975rfHjaOeHcosUJkkgmquibuJe0Sb+kkjA";
            UserMgr.inst.doLoginAsGuest2(account);
        });

        var ypos = Laya.stage.height * 0.5;
        ExtendMgr.inst.createParticle2Fairygui("0","poker_star.part",0,ypos);
        ExtendMgr.inst.createParticle2Fairygui("1","poker_star.part",Laya.stage.width,ypos);
    }
  
}