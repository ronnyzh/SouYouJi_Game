

let KEY_MUSIC_VOLUME = 'MUSIC_VOLUME';
let KEY_SOUND_VOLUME = 'SOUND_VOLUME';
let KEY_LANGUAGE = 'LANGUAGE';

class UI_Setting extends Widget{
    
    constructor(){
        super('Basic','Setting',UILayer.POPUP);
        this.keepCenter();
    }
    
    private sdrMusic:fairygui.GSlider = null;
    private sdrSound:fairygui.GSlider = null;
    
    onCreated(){
        var view = this._view;

        if(!laya.renders.Render.isWebGL)
            view.displayObject.cacheAs = 'bitmap';
        
        let btnClose = view.getChild('btn_close').asButton;
        btnClose.onClick(this,()=>{
            this.onBack();
        });
        
        this.sdrMusic = view.getChild('sdrMusic').asSlider;
        this.sdrSound = view.getChild('sdrSound').asSlider;

        this.sdrMusic.on(fairygui.Events.STATE_CHANGED, this, function(){
            Laya.SoundManager.setMusicVolume(this.sdrMusic.value*0.01);
        }.bind(this));
        this.sdrSound.on(fairygui.Events.STATE_CHANGED, this, function(){
            Laya.SoundManager.setSoundVolume(this.sdrSound.value*0.01);
        }.bind(this));
        
        var lans = view.getChild('list_lan').asList;
        for(var i = 0; i < lans.numChildren; ++i)
        {
            var child = lans.getChildAt(i);
            var btn = child.asButton;
            if(btn != null)
            {
                btn.onClick(this,this.onChangeLanguage,[btn]);
            }
        }

        let volumes = UI_Setting.refreshSoundVolume();
        this.sdrMusic.value=volumes[0];
        this.sdrSound.value=volumes[1];
    }
    
    onBack() 
    {
        Laya.LocalStorage.setItem(KEY_MUSIC_VOLUME, this.sdrMusic.value+'');
        Laya.LocalStorage.setItem(KEY_SOUND_VOLUME, this.sdrSound.value+'');
        let volumes = UI_Setting.refreshSoundVolume();
        this.hide();
    }

    onChangeLanguage(sender:fairygui.GObject)
    {
        UI_Setting.changeLanguage(sender.name,sender.asButton.title);
    }

    public static changeLanguage(lan:string,label:string):void
    {
        if(ExtendMgr.inst.lan == lan)
        {
            Alert.show(ExtendMgr.inst.getText4Language(ExtendMgr.inst.OnChangeLanguageFail)+label);
            return ;
        }
            
        let alert_content:string = ExtendMgr.inst.getText4Language(ExtendMgr.inst.OnChangeLanguage);
        alert_content += label;
        Alert.show(alert_content,true).onYes(function()
        {
            Laya.LocalStorage.setItem(KEY_LANGUAGE,lan);
            let url:string = window.location.href;
            let frist_p:number = url.indexOf('/g365_');

            if(frist_p<0)
            {
                window.location.reload(true);
                return;
            }

            let secon_p:number = url.indexOf('/',frist_p+1);
            if(secon_p<0 || secon_p<frist_p)
            {
                console.log('error url');
                return;
            }
            let new_url:string = url.substring(0,frist_p)+url.substring(secon_p);
            window.location.replace(new_url);
            window.location.reload(true);
        }.bind(this));
    }

    public static refreshSoundVolume(){
        //var MusicVolume=parseInt(Laya.LocalStorage.getItem(KEY_MUSIC_VOLUME) || '100');
        //var SoundVolume=parseInt(Laya.LocalStorage.getItem(KEY_SOUND_VOLUME) || '100'); 
        var MusicVolume=parseInt(Laya.LocalStorage.getItem(KEY_MUSIC_VOLUME) || '50');
        var SoundVolume=parseInt(Laya.LocalStorage.getItem(KEY_SOUND_VOLUME) || '50'); 
        Laya.SoundManager.setMusicVolume(MusicVolume*0.01);
        Laya.SoundManager.setSoundVolume(SoundVolume*0.01);

        fairygui.UIConfig.buttonSoundVolumeScale = SoundVolume*0.01;

        return [MusicVolume,SoundVolume];
    }
}