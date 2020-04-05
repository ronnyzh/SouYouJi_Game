module G548 {
    export class G548PlayerFrame {

        public side: number;
        protected seat: fairygui.GComponent;
        protected nameText: fairygui.GLabel;
        protected scoreText: fairygui.GLabel;
        //private scoreChangeText: fairygui.GLabel;
        protected score: number;
        public sex: number;
        protected imgHead: fairygui.GLoader;
        protected dealerCtl: fairygui.Controller;
        protected lightkMark : fairygui.GComponent;//庄家闪光
        protected case : fairygui.GComponent;
        //JiaTao
        //private changeScoreCom : fairygui.GComponent;
        protected c_balance : fairygui.Controller = null;
        protected scoreBalance : fairygui.GLabel;
        protected scoreBalance2 : fairygui.GLabel;
        protected tfScore : fairygui.GComponent;
        protected tfScoreActon1 : fairygui.Transition;
        protected tfScoreActon2 : fairygui.Transition;

        constructor(components: { side: number, seat: fairygui.GComponent }) {
            this.side = components['side'];
            let component = components['seat'];
            this.seat = component;

            let tempSeatCom = this.seat.getChild('seat').asCom;

            this.nameText = tempSeatCom.getChild('name').asLabel;
            this.scoreText = tempSeatCom.getChild('score').asLabel;
            this.imgHead = tempSeatCom.getChild('icon').asLoader;
            this.dealerCtl = tempSeatCom.getController('c1');
            this.lightkMark = tempSeatCom.getChild('light').asCom;
            this.tfScore = tempSeatCom.getChild('tfScore').asCom;

            this.c_balance = this.tfScore.getController('c1');
            this.scoreBalance = this.tfScore.getChild('title1').asLabel;
            this.scoreBalance2 = this.tfScore.getChild('title2').asLabel;
            this.tfScoreActon1 = this.tfScore.getTransition('tfScoreActon1');
            this.tfScoreActon2 = this.tfScore.getTransition('tfScoreActon2');
        }

        setSeat(data,localSide) {
            //console.log('setSeat---',data);
            if (!data) return;
            let nickname = this.formatNickname(data['nickname'],localSide);//side值用来标记是不是自己
            this.nameText.text = nickname;
            this.score = parseFloat(data['coin'] || 0);
            let score = Tools.inst.changeGoldToMoney(this.score,'');
            if(score != '' || score != null)//jia
                this.scoreText.text = score;//jia
            this.imgHead.url = 'ui://la8oslyoosvmbg';//ui://la8oslyoosvmbg
            var headImgUrl = data['headImgUrl'];
            if (headImgUrl && headImgUrl.indexOf('172.18.176.189') == -1){
                this.imgHead.url = data['headImgUrl'];
            }
            this.seat.visible = true;
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
        //JiaTao
        setLightMark(show = false,time = 500){
            this.lightkMark.visible=show;
            if(show){
                Laya.timer.once(time,this,function(){
                    this.lightkMark.visible = false;
                },null,false);
            }
        }
        //JiaTao

        betEffect(localSide:number){
            //console.log('-----',localSide);
            let leftBet = this.seat.getTransition('leftBet');
            let rightBet = this.seat.getTransition('rightBet');
            let selfBet = this.seat.getTransition('selfBet');
            if(localSide==0){
                selfBet.play();
            }else if(localSide==1||localSide==3||localSide==5||localSide==7){
                rightBet.play();
            }else if(localSide==2||localSide==4||localSide==6||localSide==8){
                leftBet.play();
            }else{
                //console.log('error aaaaaa---',localSide);
            }
        }
    
        getSeatX() {
            return this.seat.x
        }
        getSeatY() {
            return this.seat.y
        }
        getSeatWidth() {
            return this.seat.actualWidth;
        }
        getSeatHeight() {
            return this.seat.actualHeight;
        }

        getSeatRandomPoi(rect: { width: number, height: number } = { width: 0, height: 0 }) {
            //let x = (this.seat.actualWidth - rect.width * 2) < 0 ? this.seat.actualWidth / 2 : (this.seat.actualWidth - rect.width * 2) * Math.random() + rect.width;
            //let y = (this.seat.actualWidth - rect.height * 2) < 0 ? this.seat.actualHeight / 2 : (this.seat.actualHeight - rect.height * 2) * Math.random() + rect.height;
            let x = this.seat.actualWidth / 2;
            let y = this.seat.actualHeight / 2 ;
            let screenPos = this.seat.localToGlobal(x, y);
            return fairygui.GRoot.inst.globalToLocal(screenPos.x, screenPos.y);
        }
        //---JiaTao   只用来在结算时候金币往闲家飞的时候获取随机位置用
        getSeatRandomPoi_new(rect: { width: number, height: number } = { width: 0, height: 0 }) {
            let x = (this.seat.actualWidth - rect.width * 2) < 0 ? this.seat.actualWidth / 2 : (this.seat.actualWidth - rect.width * 2) * Math.random() + rect.width;
            let y = (this.seat.actualWidth - rect.height * 2) < 0 ? this.seat.actualHeight / 2 : (this.seat.actualHeight - rect.height * 2) * Math.random() + rect.height;
            //let x = this.seat.actualWidth / 2;
            //let y = this.seat.actualHeight / 2 ;
            let screenPos = this.seat.localToGlobal(x, y);
            return fairygui.GRoot.inst.globalToLocal(screenPos.x, screenPos.y);
        }

        setScoreText() {
            let score = Tools.inst.changeGoldToMoney(this.score);
            if(score != '' || score != null){
                this.scoreText.text = score;//jia
            }  
        }

        updateBankerState(dealer) {
            this.dealerCtl.setSelectedIndex(dealer ? 1 : 0);
        }

        changeScore(num) {
            //console.log('score-num---',typeof(num),num);
            //num string
            num = parseFloat(num);
            this.score += (num);//---里面存放的是总分
            //console.log('999----',this.score);
            this.setScoreText();
            
            if(num > 0){
                this.tfScore.visible = true;
                let str_score = '+'+num;
                this.scoreBalance2.text = str_score;
                this.scoreBalance.text = '';
                this.c_balance.selectedIndex = 2;
                this.tfScoreActon2.play();
            }else if(num < 0){
                this.tfScore.visible = true;
                let str_score = num.toString();
                this.scoreBalance2.text = '';
                this.scoreBalance.text = str_score;
                this.c_balance.selectedIndex = 1;
                this.tfScoreActon1.play();
            }
        }

        setScoreString(score) {
            //score string
            score = parseFloat(score.toString());
            this.score = score;//JiaTao
            this.setScoreText();
        }
        //JiaTao999999
        updateScoreString(money){
            //money number
            this.score = this.score - parseFloat(money.toString());
            this.score = this.score<0?0:this.score;
            this.setScoreText();
        }

        clear() {
            this.seat.visible = false;
        }

        resetGame() {
            this.lightkMark.visible = false;
            //this.lightkMark.playing = false;
            this.tfScore.visible = false;
            this.c_balance.selectedIndex = 0;
            this.scoreBalance.text = '';
            this.scoreBalance2.text = '';
            this.updateBankerState(false);
            this.lightkMark.visible = false;
        }
    }
}
