  <div class='block'>
       %include admin_frame_header
       <div class='content'>
          <div id="toolbar" class="btn-group">
               <button id="btn_add" type="button" class="btn btn-sm btn-primary">
                  <span class="glyphicon glyphicon-plus">
                      <a href="{{info['createUrl']}}" style='color:#FFF;text-decoration:none;'>{{info['addTitle']}}</a>
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
          pageSize: 16,
          toolbar:'#toolbar',
          pageList: [24, 48, 100,'All'],
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
              checkbox: true
          },{
              field: 'room_id',
              title: '房间ID',
              align: 'center',
              valign: 'middle'
          },{

              field: 'room_name',
              title: '房间名称',
              align: 'center',
              valign: 'middle'
          },{

              field: 'base_coin',
              title: '入房下限',
              align: 'center',
              valign: 'middle'
          },{

              field: 'max_base_coin',
              title: '入房上限',
              align: 'center',
              valign: 'middle'
          },{
              field: 'max_player_count',
              title: '房间最大人数',
              align: 'center',
              valign: 'middle'
          },{
              field: 'need_coin',
              title: '基本金币',
              align: 'center',
              valign: 'middle'
          },{
              field: 'coin_value',
              title: '金币价值',
              align: 'center',
              valign: 'middle'
          },{
              field: 'op',
              title: '操作',
              align: 'center',
              valign: 'middle',
              formatter:getOp
          }]],

         //注册加载子表的事件。注意下这里的三个参数！
          onExpandRow: function (index, row, $detail) {
              console.log(index,row,$detail);
              InitSubTable(index, row, $detail);
          }
      });

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
            var comfirmUrls = [
                '/admin/fish/room/delete'
            ];
            eval('rowobj='+JSON.stringify(row))
            var opList = []
            for (var i = 0; i < rowobj['op'].length; ++i) {
                var op = rowobj['op'][i];
                var str = JSON.stringify({room_id : rowobj['room_id']});
                var cStr = str.replace(/\"/g, "@");
                if(comfirmUrls.indexOf(op['url'])>=0)
                    opList.push(String.format("<a href=\"#\" class=\"btn btn-primary btn-sm \" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"><i class=\"fa fa-edit\"> {3} </i></a> ", op['url'], op['method'], cStr, op['txt']));
                else
                    opList.push(String.format("<a href=\"{0}?room_id="+rowobj['room_id']+"\" class=\"btn btn-primary btn-sm\" ><i class=\"fa fa-edit\"> {1} </i></a> ", op['url'],op['txt']));
            }
            return opList.join('');
        }

        function responseFunc(res){
            console.log("-------------------------data:"+res.data);
            data = res.data;
            count = res.count;
            $('.totalTitle').html('房间总数: '+count+" 今日新增: 0");
            return data;
        }

        function responseError(status) {
            location.reload();
        }

        function status(value,row,index){
            eval('var rowobj='+JSON.stringify(row))
            var statusstr = '';
            if(value == '0'){
                statusstr = '<span class="label label-warning">关闭</span>';
            }else if(value == '1'){
                statusstr = '<span class="label label-success">正在运行</span>';
            }

            return [
                statusstr
            ].join('');
        }

 //初始化子表格(无线循环)
function InitSubTable(index, row, $detail) {
        var parentAg = row.room_id;
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
</script>
%rebase admin_frame_base
