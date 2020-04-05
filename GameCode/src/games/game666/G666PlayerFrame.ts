/*
* name;
*/
class G666PlayerFrame{
    public score : number;//存放服务器发过来的金币数(未转汇率前)
    public side: number;
    private seat:fairygui.GComponent;//座位组件
    private nameText:fairygui.GLabel;//玩家姓名
    private scoreText:fairygui.GLabel;//玩家金币
    private imgHead:fairygui.GLoader;//玩家头像
    private lightkMark : fairygui.GMovieClip;//lightkMark scoreBalance
    private c_zhuang : fairygui.Controller = null;
    private c_balance : fairygui.Controller = null;
    private scoreBalance : fairygui.GLabel;
    private scoreBalance2 : fairygui.GLabel;
    private tfScoreActon1 : fairygui.Transition;
    private tfScoreActon2 : fairygui.Transition;
    private tfScore : fairygui.GComponent;
    private run : fairygui.Transition;


    constructor(components:Object){
        this.seat = components['seat'];
        this.side = this.seat['side'];
        this.run = this.seat.getTransition('run');
        let tempSeatCom = this.seat.getChild('seat').asCom;
        this.nameText = tempSeatCom.getChild('name').asLabel;
        this.scoreText = tempSeatCom.getChild('score').asLabel;
        this.imgHead = tempSeatCom.getChild('icon').asLoader;
        this.lightkMark = tempSeatCom.getChild('light').asMovieClip;
        this.c_zhuang = tempSeatCom.getController('c1');
        this.tfScore = tempSeatCom.getChild('tfScore').asCom;
        this.c_balance = this.tfScore.getController('c1');
        this.scoreBalance = this.tfScore.getChild('title1').asLabel;//减
        this.scoreBalance2 = this.tfScore.getChild('title2').asLabel;//加
        this.tfScoreActon1 = this.tfScore.getTransition('tfScoreActon1');
        this.tfScoreActon2 = this.tfScore.getTransition('tfScoreActon2');
    }
    //初始化座位
    setSeat(data,localSide)
    {
        if(!data)return;
        this.seat.visible = true;
        let nickname = data['nickname'];
        let nick:string = this.formatNickname(nickname,localSide);
        this.nameText.text = nick;
        let coin = parseFloat(data['coin'] || 0);
        let score = Tools.inst.changeGoldToMoney(data['coin']);
        if(this.score!=null)
        {
            let gold = Tools.inst.changeGoldToMoney(this.score);
            this.scoreText.text = gold;
        }
        else
        {
            this.scoreText.text = score;
        }
        
        this.imgHead.url = 'ui://la8oslyoosvmbg';
        var headImgUrl = data['headImgUrl'];
        try {
            if (headImgUrl)
                Tools.inst.changeHeadIcon(headImgUrl, this.imgHead);
            else if (this.side == 0)
                Tools.inst.changeHeadIcon(UserMgr.inst.imgUrl, this.imgHead);
        } catch (error) {
            console.log(error)
        }
    }
//----设置名称格式
        formatNickname(nickname:string,localSide:number):string{
            let nickArray_1 = nickname.split('');
            let nickArray_2 : Array<any>=[];
            let nick : string = '';
            let index = nickArray_1.length - 8;
            if(nickArray_1.length<8){
                nick = nickname;
            }else{
                for(let i = index; i < nickArray_1.length; ++i){
                    nickArray_2.push(nickArray_1[i]);
                }
                if(localSide == 0){
                    for(let i = 0; i < nickArray_2.length; ++i){
                        nick+=nickArray_2[i];
                    }
                }else{
                    for(let i = 0; i < nickArray_2.length; ++i){
                        if(i<5){
                            nick+='*';
                        }else{
                            nick+=nickArray_2[i];
                        }
                    }
                }
            }
            return nick;
        }

    scoreBalanceAni(score:number,winpoint_str:string){
        //console.log('000----',typeof(score),typeof(winpoint_str));
        //console.log('111----',score,winpoint_str);
        this.tfScore.visible = true;
        if(score > 0){
            let str_score = '+'+winpoint_str;
            this.scoreBalance2.text = str_score;
            this.scoreBalance.text = '';
            this.c_balance.selectedIndex = 2;
            this.tfScoreActon2.play();
        }else if(score < 0){
            this.scoreBalance2.text = '';
            this.scoreBalance.text = winpoint_str;
            this.c_balance.selectedIndex = 1;
            this.tfScoreActon1.play();
        }
    }
    //-----跑马灯
    horseRun(){
        this.run.play();
    }
    //-----头像动 左1 3 5 右2 4 6
    playerBet(chair){
        if(chair==7&&this.seat==null)return;
        //this.seat.getTransition('playerBet').play();
        let leftBet = this.seat.getTransition('leftBet');
        let rightBet = this.seat.getTransition('rightBet');
        let rightUpperBet = this.seat.getTransition('rightUpperBet');//---JiaTao2018-11-22-16:03 右上角抖动
        if(chair==1||chair==3||chair==5){
            leftBet.play();
        }else if(chair==2||chair==4||chair==6){
            rightBet.play();
        }else if(chair==7&&this.seat.y>600){//---换位到seat0位置 rightUpperBet
            rightUpperBet.play();
        }else if(chair==7&&this.seat.x<666){//----换位到左边三个座位中一个
            leftBet.play();
        }else if(chair==7&&this.seat.x>666){//----换位到右边三个座位中一个
            rightBet.play();
        }else{
            //
        }
    }

    //----抢庄成功后的闪光
    setLightMark(){
        this.lightkMark.visible=true;
        this.lightkMark.playing = true;
        this.lightkMark.setPlaySettings(0,-1,1,-1,Handler.create(this,function(){
            this.lightkMark.visible = false;
            this.lightkMark.playing = false;
        }));
    }

    setScore(score,isChange?:boolean){
        let gold:string;
        if(isChange == true){
            gold = score;
        }else{
            gold = Tools.inst.changeGoldToMoney(score);
        }
        this.scoreText.text = gold;
    }
    //---设置this.score函数
    setScoreNumber(possessionOfProperty){
        this.score = possessionOfProperty;
    }
    //JiaTao 2019-1-8 分数递减函数
    updatePlayerScore(money){
        this.score = this.score - parseFloat(money);
        if(this.score<0){
            this.score = 0;
        }
        this.scoreText.text = Tools.inst.changeGoldToMoney(this.score);
    }

    updateBankerState(index){
        this.c_zhuang.selectedIndex = index;
    }
    //清除座位
    clear(){
        this.seat.visible = false;
    }

    resetGame(){
        this.tfScore.visible = false;
        this.lightkMark.visible = false;
        this.lightkMark.playing = false;
        this.c_zhuang.selectedIndex = 0;
        this.c_balance.selectedIndex = 0;
        this.scoreBalance.text = '';
        this.scoreBalance2.text = '';
    }
}