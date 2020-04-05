<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<style>
    input
    {
        height: 30px;
    }
    .checkbox {
        padding:0 0 0 10;
    }
</style>
 <div class='block'>
       %include admin_frame_header
       <div class='content'>
          <div id="toolbar" class="btn-group">
               <button id="btn_add" type="button" class="btn btn-sm btn-primary">
                  <span class="glyphicon glyphicon-plus">
                      <a href="{{info['createUrl']}}" style='color:#FFF;text-decoration:none;'>默认奖励设置</a>
                  </span>
              </button>
              <button id="btn_add" type="button" class="btn btn-sm btn-primary">
                  <span class="glyphicon glyphicon-plus">
                      <a href="{{info['createUrl']}}" style='color:#FFF;text-decoration:none;'>启用</a>
                  </span>
              </button>
 
          </div>
          <table id='loadDataTable' class="table table-bordered table-hover " ></table>
       </div>
  </div>

<script type="text/javascript">
    /**
      *表格数据
    */
    var editId;        //定义全局操作数据变量
    var isEdit;
    var startDate;
    var endDate;
    $('#loadDataTable').bootstrapTable({
          method: 'get',
          url: "{{info['tableUrl']}}",
          contentType: "application/json",
          datatype: "json",
          cache: false,
          checkboxHeader: true,
          detailView: true,//父子表
          pagination: true,
          pageSize: 15,
          toolbar:'#toolbar',
          pageList: '{{PAGE_LIST}}',
          search: true,
          showRefresh: true,
          minimumCountColumns: 2,
          clickToSelect: true,
          smartDisplay: true,
          //sidePagination : "server",
          sortOrder: 'desc',
          sortName: 'datetime',
          queryParams:getSearchP,
          responseHandler:responseFunc,
          //onLoadError:responseError,
          showExport:true,
          exportTypes:['excel', 'csv', 'pdf', 'json'],
          //exportOptions:{fileName: "{{info['title']}}"+"_"+ new Date().Format("yyyy-MM-dd")},
          columns: [
          [{
                    halign    : "center",
                    font      :  15,
                    align     :  "left",
                    class     :  "totalTitle",
                    colspan   :  9
          }],
          [{
              field: 'id',
              title: '游戏ID',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{

              field: 'name',
              title: '游戏名称',
              align: 'center',
              valign: 'middle',
              formatter:colorFormat
          },{

              field: 'chets_result',
              title: '游戏场次宝箱规则',
              align: 'center',
              valign: 'middle',
              formatter: chetsGameNumber
          },{

              field: 'op',
              title: '操作',
              align: 'center',
              valign: 'middle',
              formatter: getOp
          }

          ]],

         //注册加载子表的事件。注意下这里的三个参数！
          onExpandRow: function (index, row, $detail) {
              console.log(index,row,$detail);
              InitSubTable(index, row, $detail);
          }
      });
        function chetsGameNumber(value, row, index) {
            var ruleDom = '';
            var queryKeys = {
                "0": '新手场',
                "1": '普通场',
                "2": '中级场',
                "3": '高级场',
                '4': "土豪场",
                '5': '至尊场'
            }

            var chets_status = {
                0: "<button class='btn btn-info'>开启场次</button>",
                1: "<button class='btn btn-danger'>关闭场次</button>"
            }
             

            $.each(value, function(k, v) {
                var chets_win_status = {
                    0: "<button class='btn btn-info closed' level='"+v.gold_level+"' gameId='"+row.id+"' status='1' >开启</button>",
                    1: "<button class='btn btn-danger closed' level='"+v.gold_level+"' gameId='"+row.id+"' status='0'>关闭</button>"
                }
                ruleDom += '<div class="form-inline">'+
                           '<div class="checkbox"><input type="checkbox" level="'+v.gold_level+'" gameId="'+row.id+'"  \>' +
                           "<span style='color:red;'>" +queryKeys[v.gold_level]+ "</span></div>" +
                           ' <div class="form-group"> 对局数: <input type="number" value="' + v.chets_number + '" class="input-number" \>&nbsp;</div>'+
                           ' <div class="form-group"> 对局胜场: <input type="number" value="' + v.chets_win_number + '" class="input-win-number" \>&nbsp; </div>'+
                           '<button class="btn btn-default confirm" level="'+v.gold_level+'" gameId="'+row.id+'">保存</button>'+
                           chets_win_status[v.chets_win_status] +'</div>'
            });
            return ruleDom
        }
        //定义列操作
        function getSearchP(p){
          sendParameter = p;

          sendParameter['startDate'] = startDate;
          sendParameter['endDate']  = endDate;

          startDate = $("#data-pick-start").val();
          endDate   = $("data-pick-end").val();

          return sendParameter;
        }

        function getOp(value,row,index){
            var comfirmUrls = [ //需要弹框操作的接口地址
                '/admin/game/delete',
                '/admin/game/setting/defaultGames'
            ];
            eval('rowobj='+JSON.stringify(row))
            var opList = []
            for (var i = 0; i < rowobj['op'].length; ++i) {
                var op = rowobj['op'][i];
                var str = JSON.stringify({id : rowobj['id']});
                var cStr = str.replace(/\"/g, "@");
                if(comfirmUrls.indexOf(op['url'])>=0){  //删除用红色按钮
                    var btn_type = 'primary';
                    if ( (op['url'].substring(op['url'].length-6)) == 'delete')
                         btn_type = 'danger';
                    opList.push(String.format("<a href=\"#\" class=\"btn btn-{4} btn-sm \" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\">{3}</a> ", op['url'], op['method'], cStr, op['txt'],btn_type));
                }else{
                    opList.push(String.format("<a href=\"{0}?gameId="+rowobj['id']+"\" class=\"btn btn-primary btn-sm\" >{1}</a> ", op['url'],op['txt']));
                }
            }
            return opList.join('');
        }

        function responseFunc(res){
            data = res.data;
            count = res.count;
            $('.totalTitle').html('游戏总数: '+count+" 今日新增: 0");
            return data;
        }

        function responseError(status) {
            location.reload();
        }

        function _settingDefaultGame(){
          var gameIds = $.map($('#loadDataTable').bootstrapTable('getSelections'),function(row){
              return row.id;
          });

          if (!gameIds.length){    //如果没选择直接return
              console.log('---------------had not selected.. return');
              return;
          }

          var remoteUrl = "{{info['setUrls']}}",
              method    = "POST",
              jsonStr   = {'id':gameIds.join(',')}

          console.log('----------------select gameIds['+gameIds+']');
          formAjax(remoteUrl,method,jsonStr,'正在设置...,');
        }

        function status(value,row,index){
            eval('var rowobj='+JSON.stringify(row))
            var statusstr = '';
            if(value == '0'){
                statusstr = '<span class="label label-warning">否</span>';
            }else if(value == '1'){
                statusstr = '<span class="label label-success">是</span>';
            }

            return [
                statusstr
            ].join('');
        }

 //初始化子表格(无线循环)
function InitSubTable(index, row, $detail) {
        var parentAg = row.id;
        var cur_table = $detail.html('<table table-bordered table-hover definewidth></table>').find('table');
        $(cur_table).bootstrapTable({
                url: '{{info["serversUrl"]}}',
                method: 'get',
                contentType: "application/json",
                datatype: "json",
                cache: false,
                queryParams:getSearchP,
                sortOrder: 'desc',
                sortName: 'regDate',
                pageSize: 15,
                pageList: [15, 25],
                columns: [{
                    field: 'serverUrl',
                    title: '游戏服务器',
                    align: 'center',
                    valign: 'middle'
                },{
                    field: 'desc',
                    title: '描述',
                    align: 'center',
                    valign: 'middle'
                },{
                    field: 'op',
                    title: '操作',
                    align: 'center',
                    valign: 'middle',
                    formatter:getOp
                }],

                //注册加载子表的事件。注意下这里的三个参数！
                onExpandRow: function (index, row, $detail) {
                    console.log(index,row,$detail);
                    InitSubTable(index, row, $detail);
                }

        });
        //定义列操作
        function getSearchP(p){
              sendParameter = p;
              sendParameter['id'] = parentAg;
              return sendParameter;
        }

        function getOp(value,row,index){
            eval('rowobj='+JSON.stringify(row))
            var opList = []
            for (var i = 0; i < rowobj['op'].length; ++i) {
                var op = rowobj['op'][i];
                var str = JSON.stringify({gameId : rowobj['id']});
                var cStr = str.replace(/\"/g, "@");
                opList.push(String.format("<a href=\"#\" class=\"btn btn-primary btn-sm btn-xs\" onclick=\"comfirmServer(\'{0}\', \'{1}\', \'{2}\')\"><i class=\"fa fa-edit\"> {3} </i></a> ", op['url'], op['method'], cStr, op['txt']));

            }
            return opList.join('');
        }
    
}

$('body').delegate(".confirm", "click", function(){
    var game_id = $(this).attr("gameid");
    var level = $(this).attr("level");
    confirm = $(this)
    var number = confirm.parent().find(".input-number").val();    
    var win_number = confirm.parent().find(".input-win-number").val();    
    var chets_level = 1; //confirm.parent().find(".input-chets-level").val();    
    var chets_win_level = 1; //confirm.parent().find(".input-chets-win-level").val();    
    
    $.ajax({
            type: 'POST',
            url: "/admin/game/set_game_gold",
            data: {"number": number, "win_number": win_number, "chets_level": chets_level, "chets_win_level": chets_win_level, "game_id": game_id, "level": level},
            dataType: "json",
            success: function(res, data){
                layer.msg(res.msg);
                location.reload();
            },
            error: function(res, data){
                console.log(res);
            }, 
            
    });

});

$('body').delegate(".closed", "click", function(){
    var Btn = $(this);
    var game_id = $(this).attr("gameid");
    var level = $(this).attr("level");
    var status = $(this).attr("status")
    $.ajax({
            type: 'POST',
            url: "/admin/game/chets/close",
            data: {"game_id": game_id, "level": level, "status": status},
            dataType: "json",
            success: function(res, data){
                console.log(res);
                if (res.status == 1) {
                    Btn.removeClass("btn-info");
                    Btn.addClass("btn-danger");
                    Btn.text("关闭");
                    Btn.attr("status", '0')
                } else {
                    Btn.removeClass("btn-danger");
                    Btn.addClass("btn-info");
                    Btn.text("开启");
                    Btn.attr("status", '1')
                }
                layer.msg(res.msg);
            },
            error: function(res, data){
                console.log(res);
            }, 
            
    });

});

</script>
%rebase admin_frame_base