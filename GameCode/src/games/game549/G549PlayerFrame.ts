/*
* name;
*/
module G549 {
    export class G549PlayerFrame extends G548.G548PlayerFrame{
        constructor(components: { side: number, seat: fairygui.GComponent }) {
            super(components);
        }
        //子类扩展函数
        hideScore(){
            //console.log('隐藏飘分');
            if(this.tfScore!=null){
                this.tfScore.visible = false;
            }
            
        }
    }
}
