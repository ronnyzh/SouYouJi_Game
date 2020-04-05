<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
        %include admin_frame_header
        <div class="content" style="float:left;width:100%;position:relative;top:2.6em">
            <div style='clear:both'></div>
            <table id="dataTable" class="table table-bordered table-hover"></table>
        </div>
</div>

<script type="text/javascript">
    var startDate = $("#pick-date-start").val();
    var endDate   = $("#pick-date-end").val();
    $('#dataTable').bootstrapTable({
          method: 'get',
          url: '{{info["listUrl"]}}',
          contentType: "application/json",
          datatype: "json",
          cache: true,
          checkboxHeader: true,
          striped: true,
          pagination: true,
          pageSize: 15,
          pageList: [15, 50, 100,'All'],
          showColumns: true,
          minimumCountColumns: 2,
          clickToSelect: true,
          responseHandler:responseFunc,
          queryParams:getSearchP,
          search: true,
          showRefresh: true,
          showColumns: true,
          showToggle: true,
          showExport:true,
          showFooter: true,
          cardView: false,
          exportDataType: 'all',
          exportTypes:[ 'csv', 'txt', 'sql', 'doc', 'excel', 'xlsx', 'pdf'],
          exportOptions:{
            fileName: '{{ info["title"] }}',
            },
          columns: [
          [
                {
                    "align":"center",
                    "hlign":"center",
                    "class":"total_room",
                    "colspan": 9
                }
          ],
          [{
              field: 'id',
              title: '房间ID',
              align: 'center',
              valign: 'middle',
              sortable: true
          },{
              field: 'game_id',
              title: '游戏ID',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'game_name',
              title: '游戏名称',
              align: 'center',
              valign: 'middle',
              sortable: true
          },{
              field: 'dealer',
              title: '房主',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'player_count',
              title: '玩家数',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'op',
              title: '操作',
              align: 'center',
              valign: 'middle',
              formatter:getOp
          }]]
    });

        function getOp(value,row,index){
            eval('rowobj='+JSON.stringify(row))
            var opList = []
            for (var i = 0; i < rowobj['op'].length; ++i) {
                var op = rowobj['op'][i];
                var str = JSON.stringify({id : rowobj['id']});
                var cStr = str.replace(/\"/g, "@");
                if(op['url'] == '/admin/agent/room/kick')
                    opList.push(String.format("<a href=\"javascript:;\" class=\"btn btn-primary btn-sm\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"> {3}</a> ", op['url'], op['method'], cStr, op['txt']));
                else if(op['url'] == '/admin/agent/room/kick2')
                    opList.push(String.format("<a href=\"javascript:;\" class=\"btn btn-primary btn-sm\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"> {3}</a> ", op['url'], op['method'], cStr, op['txt']));
                else
                    opList.push(String.format("<a href=\"{0}?id="+rowobj['id']+"\" class=\"btn btn-primary btn-sm\" >{1}</a> ", op['url'],op['txt']));
            }
            return opList.join('');
        }


          //前台查询参数

        function getSearchP(p){
            // account = $("#account").val();
            // member_level = $('#member_level').val();
            // member_status = $("#member_status").val();
            // userId = $("#userId").val();
            startDate = $("#pick-date-start").val();
            endDate   = $("#pick-date-end").val();

            sendParameter = p;
            sendParameter['startDate'] = startDate;
            sendParameter['endDate']  = endDate;

            return sendParameter;
          }

        //获得返回的json 数据
        function responseFunc(res){
            data = res.data;
            count= res.count;
            //实时刷
            $('.total_room').html("当前房间总数："+count);
            var totalClass = document.getElementsByClassName('total_room')[0];
            totalClass.style.cssText = "background-color:#d9edf7;height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            return data;
        }
        function responseError(status) {
            location.reload();
        }
</script>
%rebase admin_frame_base
