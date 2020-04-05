/*
 * 前端检测事件脚本
    （钻石订单，session过期,刷新金币）
 * @author:ldw
 +-------------------------------------------------------
*/
var CHECK_EVENT = function() {
    var _that = this;
    this.checkOl         = true;
    this.timerOlCheck    = 0;
    this.timerCardCheck  = 0;
    this.timerOrderCheck = 0;
    this.timerMemberOl   = 0;
    this.refreshOlTime   = 30; //每15秒刷新一次

    this.refreshUrls = {  //定时器地址
        'refreshOl'        : '/admin/checkAdminOL?',
        'refreshCard'      : '/admin/agent/cardRefresh?',
        'checkBuy'         : '/admin/agent/checkBuyCard?number=',
        'refreshMember'    : '/admin/agent/member/curOnline?list=1'
    };

    this._start = function(){ //启动定时器
         console.log('____check__init-----------------------');
         _that.timerOlCheck = setTimeout(_that.refreshAdminOL, 1000);
         _that.timerCardCheck  = setTimeout(_that.refreshRoomCard,1000);
         _that.timerOrderCheck = setTimeout(_that.checkBuyCard,1000);
    };

    this.refreshAdminOL = function(){  //检查session时间
        console.log('checkAdminOL1');
        clearTimeout(_that.timerOlCheck);
        $.ajax({
                url:_that.refreshUrls['refreshOl']+new Date().getTime()
                ,method:"GET"
                ,timeout:5000
                ,contentType:"json"
                ,success:function(data,status){
                        // code
                        console.log('--------refreshOlCallback');
                        code = parseInt(data.code)
                        if (_that.checkOl && code == 0){
                            obL = false;
                            layer.open({
                                content: data.msg
                                ,btn: '确认'
                                ,end:function(){
                                    location.href='/admin/login';
                                }
                            });
                       }
                }
               ,complete:function(){
                  console.log('------------------refreshAdminOL complete.');
                  if(_that.checkOl){
                       _that.timerOlCheck = setTimeout(_that.refreshAdminOL, 5000);
                  }
               }
        });
    };

    this.refreshRoomCard = function(){  //刷新用户钻石数
        console.log('refreshRoomCard');
        $.ajax({
                 url:_that.refreshUrls['refreshCard']+new Date().getTime()
                ,method:"GET"
                ,timeout:5000
                ,contentType:"json"
                ,success:function(data,status){
                   console.log('--------refreshCardCallBack');
                   $('.badge-card').html(data.roomCard);
                },complete:function(){
                   console.log('--------refreshCardCallBack complete');
                   _that.timerCardCheck  = setTimeout(_that.refreshRoomCard,5000);
                }
        });
    };

    this.refreshMemberOlTable = function(){   //刷洗女会员在线
        console.log('refreshMemberOlTable time:'+_that.refreshOlTime);
        _that.refreshOlTime -= 1;
        if (_that.refreshOlTime <= 0){
               $('#memberOLtable').bootstrapTable('refresh',{
                        url   : _that.refreshUrls['refreshMember'],
                        query : {ajaxOptions:{async:false,timeout:5000}}}
               );
               _that.refreshOlTime = 30;
        }else{
              this.timerMemberOl   = setTimeout(_that.refreshMemberOlTable,1000);
        }
        console.log("------refreshMemberOlTable callBack");
    }

    this.checkBuyCard = function(){  //刷新订单
        console.log('checkBuyCard');
        clearTimeout(_that.timerOrderCheck);
        num = 0;
        $.ajax({
                 url:_that.refreshUrls['checkBuy']+num+"&_"+new Date().getTime()
                ,method:"GET"
                ,timeout:5000
                ,contentType:"json"
                ,success:function(data,status){
                        console.log('--------refreshCheckCardCallBacl');
                        reCode = parseInt(data.code);
                        switch(reCode){
                            case 0:
                                //信息框
                                number = data.orderNo;
                                layer.open({
                                    title: [
                                       '订单消息',
                                      'background-color:#204077; color:#fff;'
                                    ]
                                    ,anim: 'up'
                                    ,content:data.msg
                                    ,btn: ['查看', '忽略']
                                    ,yes:function(index){
                                      $(".body-iframe").attr('src',data.jumpUrl);
                                      layer.close(index);
                                    }
                                });
                                break;
                            case 2://
                                number = data.orderNo
                                break;
                            case 3:
                                break;
                            default: //错误信息提示,不刷新页面
                                break;
                      }
                },complete:function(){
                    console.log('-----------------checkBuyCard complete.');
                    _that.timerOrderCheck = setTimeout(_that.checkBuyCard,30000);
                }
        });
    };
};

checker = new CHECK_EVENT();
