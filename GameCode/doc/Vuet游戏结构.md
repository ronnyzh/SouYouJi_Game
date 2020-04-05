# Vuet游戏结构

## 目前应用游戏
> 这三个游戏都用了Vuet作为基类，并且用了jx工具函数
1. 跑得快(game559)
1. 斗地主(game560)
1. 炸金花(game561)


## 关于这类游戏的运作
* Vuet路径位于：`src/common/Vuet/Vuet.ts`
* jx路径位于: `src/common/utils/utils.ts`
### 游戏结构
1. Game整个结构都包含在Game这个模块中，这个变量在Master.ts中声明
1. Page.ts作为游戏整体流程的控制，与其他游戏结构同步
    * Page.ts类内的函数可以通过Game.page调用
1. Control.ts 应该作为Vuet类集中声明和管理的地方
    * 可以通过Control来调用（e.g: `Control.build()`）
    * `Control.build()`, `Control.destory` 应该在游戏开始，和结束的地方调用，用来统一管理Vuet类
1. Method.ts 应该作为游戏操作封装函数和全局变量声明的地方

### Vuet的配置
```
    data?: any;     //数据        {key: value}        key绑定到[本类this]，可以通过this._data访问
    params?: any;   //参数        {key: value}        key绑定到[本类this]
    computed?: any; //计算属性    {key: Function(){return value;}} key绑定到[本类this]，作用域为本类this,初始化最后调用,然后不应该更改
    component?: any;//包含组件    {key: conponent}    通过this.getComponent(name) 访问
    //操作方法等
    once?:any;      //一次性自定义方法 {key: Function(){}} 只能被执行一次，key绑定到[本类this]，作用域为本类this
    watch?: any;    //监听数据及参数{key: Function(newValue)}
    method?: any;   //自定义方法    {key: Function(){}}  key绑定到[本类this]，作用域为本类this
    //钩子函数
    beforeCreate?: any; //初始化前执行 Function
    created?: any;      //初始化后执行 Function
```

#### 简单应用数据绑定
下面这个例子简单地定义了一个player，并且赋予了这个player一些能力：

* 界面元素tfScore的值和`player.score`绑定，只要socre更新，tfScore也会更新
* `created`定义了初始化完成后执行的操作，这里是把tfScore隐藏了
* 给player定义了一个方法`format()`并且会调用`jx.utils.goldFormat()`来进行格式化
```
    //例子：
    var player = new Vuet({
        data:{
            score:0
        },
        computed: {
            tfScore: this._view.getChild('tfScore');
        },
        watch:{
            score: function(newValue){
                console.log('实时更新score', score);
                var tfScore = this.getComponent('tfScore');
                tfScore.visible = true;
                tfScore.text = this.format(score);
            },
        },
        created: function(){
            this.getComponent('tfScore').visible = false;
        },
        method:{
            format: function(num){
                return jx.utils.goldFormat(score);
            }
        },
    })
```

#### 简单应用外部绑定
下面这个例子简单地定义了一个玩家管理器
* 当玩家分数变化时,管理器会更新`this.total`并打印
* 当所有玩家分数合计大于1000分时，会调用`this.congratulation(newValue)`并且这个函数只能被调用一次
```
    //例子：
    var playerManager = new Vuet({
        data:{
            total:0
        },
        params:{
            players[player1, player2];
        },
        watch: {
            total: function(newValue){
                console.log('玩家总分:', newValue);
                if(newValue > 1000)
                    this.congratulation(newValue);
            },
        },
        once: {
            congratulation: function(value){
                jx.alert('恭喜所有玩家总分达到',value);
            },
        },
        created: function(){
            this.players.forEach(player=>{
                player.watch('score', function(newValue){
                    console.log('玩家分数变化:', newValue);
                    this.total = players.reduce((cur, player)=>{
                        return cur + player.score;
                    },0)
                })
            })

        },

    })
```