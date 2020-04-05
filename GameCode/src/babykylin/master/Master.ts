class Master{
    public setting:MasterInfo;
    protected agent:NetAgent;
    private main_frame_rate:string;

    enter(params)
    {
        this.main_frame_rate = Laya.stage.frameRate;
        console.log("--------------------------------------------->this.setting.frame_rate",this.setting.frame_rate.toString());
        Laya.stage.frameRate = this.setting.frame_rate;
    }

    update(){}

    exit()
    {
        Laya.stage.frameRate = this.main_frame_rate;
    }

    isPlaying(){
        return null;
    }
}

