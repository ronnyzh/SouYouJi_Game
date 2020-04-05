/**
  * 弹出层确认框
  * @author:ldw
  -----------------------------------------------
*/
function comfirmDialog(url,method,jsonStr,text){
    var comfirmTxt = text || '是否确定此操作';

      layer.open({
          title: [
             '搜集游棋牌后台提醒你',
             'background-color:#204077; color:#fff;'
          ]
          ,anim: 'up'
          ,content:comfirmTxt
          ,btn: ['确认', '取消']
          ,fixed:true
          ,style: 'top:25%;'
          ,yes:function(index){
            normalAjaxStrData(url,method,jsonStr);
            layer.close(index);
          }
      });
}

/**
  * 弹出层确认框
  * @author:ldw
  -----------------------------------------------
*/
function comfirmServer(url,method,jsonStr){
    var comfirmTxt = '是否确定关闭服务器';

      layer.open({
          title: [
             '搜集游棋牌后台提醒你',
             'background-color:#204077; color:#fff;'
          ]
          ,anim: 'up'
          ,content:comfirmTxt
          ,btn: ['确认', '取消']
          ,style: 'top:25%;'
          ,yes:function(index){
            normalAjaxStrData(url,method,jsonStr,'正在关闭服务器');
            layer.close(index);
          }
      });
}

/**
  * 订单确认弹出层
  * @author:ldw
  -----------------------------------------------
*/
function comfirmOrderDialog(url,method,jsonStr){
   var str = JSON.parse(jsonStr.replace(/\@/g, "\"")),
       orderUrl = '/admin/order/info';

   $.ajax({
        url : orderUrl,
        type : 'GET',
        data : {'isAjax':1,'orderNo':str['orderNo']},
        dataType: "json",//(可以不写,默认)

        success : function(data, statue) {
              var title = "订单号:"+data.orderNo+""
              var orderTxt = '  <p>充值钻石数       : '+data.cardNums+' </p>\
                                <p>申请充值账号     : '+data.rechargeAccount+'</p>\
                                <p>申请时间         : '+data.applyDate+'</p>\
                                <p>备注             : '+data.note+'</p>';

              layer.open({
                  title: [
                     title,
                    'background-color:#204077; color:#fff;'
                  ]
                  ,anim: 'up'
                  ,content : orderTxt
                  ,btn: ['确认', '取消']
                  ,style: 'position:fixed;left:0;top:0;'
                  ,yes:function(index){
                    formAjax(url,method,{'orderNo':data.orderNo,'token':data.token});
                    layer.close(index);
                  }
            });
        }
    });
}

/**
  * 订单取消弹出层
  * @author:ldw
  -----------------------------------------------
*/
function cancelOrderDialog(url,method,jsonStr){
   var str = JSON.parse(jsonStr.replace(/\@/g, "\"")),
       orderUrl = '/admin/order/info';

   $.ajax({
        url : orderUrl,
        type : 'GET',
        data : {'isAjax':1,'orderNo':str['orderNo']},
        dataType: "json",//(可以不写,默认)

        success : function(data, statue) {
              var title = "订单号:"+data.orderNo+""
              var orderTxt = '  <p>充值钻石数     : '+data.cardNums+' </p>\
                                <p>申请充值账号   : '+data.rechargeAccount+'</p>\
                                <p>申请时间       : '+data.applyDate+'</p>\
                                <p>备注           : '+data.note+'</p>';

              layer.open({
                  title: [
                     title,
                    'background-color:#204077; color:#fff;'
                  ]
                  ,anim: 'up'
                  ,content : orderTxt
                  ,btn: ['确认取消', '取消']
                  ,yes:function(index){
                    formAjax(url,method,str);
                    layer.close(index);
                  }
            });
        }
    });
}

/**
  * 后台首页消息提示框
  * @author:ldw
  -----------------------------------------------
*/
function tipsDialog(nums){

    var content = '<p style="font-size:14px;text-align:center;margin-top:8px">\
                   有<a href="/admin/order/saleOrderPending"><b>&nbsp;'+nums+'</b>&nbsp;</a>条待处理钻石订单</p>';

    layer.open({
          title: [
            '待处理订单消息',
            'background-color:#204077; color:#fff;'
          ]
          ,style: 'position:fixed;left:0;top:0px;'
          ,anim: 'up'
          ,content: content
    });
}

/**
  * 悬空提示操作框
  * @author:ldw
  -----------------------------------------------
*/
function timeTipsDialog(url,time,message){

    layer.open({
          title: [
             '系统提示',
            'background-color:#204077; color:#fff;'
          ]
          ,anim: 'up'
          ,content:message
          ,btn: ['确认', '取消']
          ,style: 'position:fixed;left:0;top:0px;'
          ,yes:function(index){
            location.href = url;
            layer.close(index);
          }
    });
}


function cancelDialog(url,orderNo){

      layer.open({
            content: '是否删除该订单'
            ,btn: ['删除', '取消']
            ,skin: 'footer'
            ,yes: function(index){
              $.ajax({
                  type  :   'POST',
                  url   :   url,//提交的URL
                  data  :   {'orderNo':orderNo}, // 要提交的表单,必须使用name属性
                  dataType:'JSON',

                  success: function (data,statue) {
                      reCode = parseInt(data.code);
                      switch(reCode){
                          case 0:
                              //信息框
                              layer.open({
                                  content: data.msg
                                  ,btn: '确认'
                                  ,style: 'position:fixed;left:0;top:0px;'
                                  ,yes:function(index){
                                       location.href=data.jumpUrl;
                                       layer.close(index);
                                  }
                              });
                              break;

                          default: //错误信息提示,不刷新页面
                              layer.open({
                                content: data.msg
                                ,skin: 'msg'
                                ,style: 'position:fixed;left:0;top:0px;'
                                ,time: 2 //2秒后自动关闭
                              });
                      }
                  }
            });
       }
  });
}

/**
  * 显示回放的详细记录
  *
  +-------------------------------------------
*/
function showFishReplay(url,method,replay_id){

    console.log(String.format("---------showFishReplay params url[{0}] method[{1} replay_id[{2}]]",url,method,replay_id));

    var pageii = layer.open({
        type: 1
        ,content: String.format("<iframe src='/admin/fish/bet/replay?replay_id={0}' width='100%' height='500px'></iframe>",replay_id)
        ,anim: 'up'
        ,success: function(elem){
            $(".layui-m-layercont").css({"text-align":"left", "padding-top":"20px", "overflow":"auto"});
            $('.layui-m-layerchild').append('<div class="closePage">x</div>');
        }
        ,style: 'position:fixed; left:0; top:0; width:100%; border: none; -webkit-animation-duration: .5s; animation-duration: .5s;'
    });

}


/**
  * 显示回放的详细记录
  *
  +-------------------------------------------
*/
function showGmHisDialog(url,method,userId){

    console.log(String.format("---------showGmHisDialog params url[{0}] method[{1} replay_id[{2}]]",url,method,userId));

    var pageii = layer.open({
        type: 1
        ,content: String.format("<iframe src='/admin/member/gm/showHis?userId={0}' width='100%' height='500px'></iframe>",userId)
        ,anim: 'up'
        ,success: function(elem){
            $(".layui-m-layercont").css({"text-align":"left", "padding-top":"20px", "overflow":"auto"});
            $('.layui-m-layerchild').append('<div class="closePage">x</div>');
        }
        ,style: 'position:fixed; left:0; top:0; width:100%; border: none; -webkit-animation-duration: .5s; animation-duration: .5s;'
    });

}

/**
  * 显示回放的详细记录
  *
  +-------------------------------------------
*/
function showActiveDialog(url,method,reg_date){

    console.log(String.format("---------showActiveDialog params url[{0}] method[{1} replay_id[{2}]]",url,method,reg_date));

    var pageii = layer.open({
        type: 1
        ,content: String.format("<iframe src='/admin/statistics/active/showDay?day={0}' width='100%' height='500px'></iframe>",reg_date)
        ,anim: 'up'
        ,success: function(elem){
            $(".layui-m-layercont").css({"text-align":"left", "padding-top":"20px", "overflow":"auto"});
            $('.layui-m-layerchild').append('<div class="closePage">x</div>');
        }
        ,style: 'position:fixed; left:0; top:0; width:100%; border: none; -webkit-animation-duration: .5s; animation-duration: .5s;'
    });

}

function logout(message){
	var message = message || '正在登出..';

  //询问框
  layer.open({
    content: '是否退出系统'
    ,btn: ['确定', '取消']
    ,yes: function(index){
      location.href="/admin/logout";
      layer.close(index);
    }
  });
}
