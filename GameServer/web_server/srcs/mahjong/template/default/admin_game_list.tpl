<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
 <div class='block'>
       %include admin_frame_header
       <div class='content'>
          <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
                <a href="{{info['createUrl']}}" style='color:#FFF;text-decoration:none;'>
                   <button id="btn_add" type="button" class="btn btn-sm btn-primary">
                        <i class="glyphicon glyphicon-plus"> {{info['addTitle']}} </i>
                    </button>
                </a>
                <a href="javascript:;" style='color:#FFF;text-decoration:none;'>
                    <button id="btn_add" onclick="_settingDefaultGame();" type="button" class="btn btn-sm btn-primary">
                        <i class="glyphicon glyphicon-plus"> {{info['setTitle']}} </i>
                    </button>
                </a>
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
          toolbar:'#toolbar',
          striped: true,
          checkboxHeader: true,
          detailView: true,//父子表
          pagination: true,
          pageSize: 15,
          pageList: '{{PAGE_LIST}}',
          search: true,
          showRefresh: true,
          showColumns: true,
          showToggle: true,
          showExport:true,
          showFooter: true,
          cardView: false,
          strictSearch: true,
          minimumCountColumns: 5,
          clickToSelect: true,
          smartDisplay: true,
          sortOrder: 'desc',
          sortName: 'datetime',
          queryParams:getSearchP,
          responseHandler:responseFunc,
          exportDataType: 'all',
          exportTypes:[ 'csv', 'txt', 'sql', 'doc', 'excel', 'xlsx', 'pdf'],
          exportOptions:{
          fileName: '{{ info["title"] }}',
          },

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

              field: 'version',
              title: '游戏版本号',
              align: 'center',
              valign: 'middle'
          },{

              field: 'pack_name',
              title: '游戏包路径',
              align: 'center',
              valign: 'middle'
          },{

              field: 'default',
              title: '默认绑定',
              align: 'center',
              valign: 'middle',
              formatter:status
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
            $('.totalTitle').html('游戏总数： '+count+" 今日新增：0");
            var totalTitle = document.getElementsByClassName('totalTitle')[0];
            totalTitle.style.cssText = "background-color:#d9edf7; height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
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
        var cur_table = $detail.html('<table class="table-bordered table-hover definewidth" style="background-color:#428bca4d;border-color: #428bca4d;border-width: 2px 2px 2px 2px;"></table>').find('table');
        $(cur_table).bootstrapTable({
                url: '{{info["serversUrl"]}}',
                method: 'get',
                contentType: "application/json",
                datatype: "json",
                cache: false,
                sortOrder: 'desc',
                sortName: 'regDate',
                striped: true,
                checkboxHeader: true,
                pagination: true,
                pageSize: 15,
                pageList: '{{PAGE_LIST}}',
                strictSearch: true,
                minimumCountColumns: 5,
                clickToSelect: true,
                smartDisplay: true,
                queryParams:getSearchP,
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
                opList.push(String.format("<a href=\"#\" class=\"btn btn-primary btn-sm\" onclick=\"comfirmServer(\'{0}\', \'{1}\', \'{2}\')\"> {3} </a> ", op['url'], op['method'], cStr, op['txt']));

            }
            return opList.join('');
        }
}
</script>
%rebase admin_frame_base
