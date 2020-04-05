<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<div class="block">
        %include admin_frame_header
        <div class="content">
           %include original_search_bar
           <table id="dataTable" class="table table-bordered table-hover" >

           </table>
        </div>
</div>
<script type="text/javascript">

  function initTable() {
    $('#dataTable').bootstrapTable({
          method: 'get',
          url: '{{info["listUrl"]}}',
          contentType: "application/json",
          datatype: "json",
          cache: false,
          checkboxHeader: true,
          striped: true,
          pagination: true,
          pageSize: 15,
          showExport: true,
          exportTypes:['excel', 'csv', 'pdf', 'json'],
          pageList: [15,50,100, 'All'],
          search: true,
          clickToSelect: true,
          sortOrder: 'desc',
          sortName: 'date',
          queryParams:getSearchP,
          // responseHandler:responseFun,
          showExport:true,
          showRefresh:true,
          exportTypes:['excel', 'csv', 'pdf', 'json'],
          // exportOptions:{fileName: "{{info['title']}}"+"_"+ new Date().Format("yyyy-MM-dd")},
          columns: [
            {
              field: 'Id',
              title: '主键ID',
              align: 'center',
              valign: 'middle',
              sortable:true,
            },{
              field: 'GameName',
              title: '比赛名称',
              align: 'center',
              valign: 'middle',
              sortable:true,
            },{
              field: 'StartTime',
              title: '开始时间',
              align: 'center',
              valign: 'middle',
              sortable:true,
          },{
              field: 'EndTime',
              title: '结束时间',
              align: 'center',
              valign: 'middle',
              sortable:true,
          },{
              field: 'PlayerCount',
              title: '玩家人数',
              align: 'center',
              valign: 'middle',
              sortable:true,
         },{
              field: 'Accounts',
              title: '玩家ID列表',
              align: 'center',
              valign: 'middle',
              sortable:true,
         },{
              field: 'playerGolds',
              title: '玩家总计',
              align: 'center',
              valign: 'middle',
              sortable:true,
         },{
              field: 'total_reward',
              title: '奖励统计',
              align: 'center',
              valign: 'middle',
              formatter:function (value) {
                var str = ''
                console.log(value)
                for(var i=0;i<value.length;i++){
                    str += '<p>'+value[i]+'</p>'
                }
                return str
              },
         },{
              field: 'total_Rankings',
              title: '名次统计',
              align: 'center',
              formatter:function (value) {
                var str = ''
                console.log(value)
                for(var i=0;i<value.length;i++){
                    str += '<p>'+value[i]+'</p>'
                }
                return str
              },
         },{
              field: 'total_roomCard',
              title: '比赛总结(钻石)',
              align: 'center',
              valign: 'middle',
              sortable:true,
         },{
              field: 'total_gold',
              title: '比赛总结(金币)',
              align: 'center',
              valign: 'middle',
              sortable:true,
         },{
              field: 'total_yuanbao',
              title: '比赛总结(元宝)',
              align: 'center',
              valign: 'middle',
              sortable:true,
         },{
              field: 'total_redpacket',
              title: '比赛总结(红包)',
              align: 'center',
              valign: 'middle',
              sortable:true,
         }]
      });
        //定义列操作
        function getSearchP(p){
          startDate = $("#pick-date-start").val();
          endDate   = $("#pick-date-end").val();

          sendParameter = p;

          sendParameter['startDate'] = startDate;
          sendParameter['endDate']  = endDate;

          return sendParameter;
        }
        //获得返回的json 数据

        function responseFun(res){
            data = res.date
            return data;
        }
}
</script>
%rebase admin_frame_base
