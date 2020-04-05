<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
  <div class="block">
            %include admin_frame_header
            <div class="content">
               %include original_search_bar
               <table id="dataTable" class="table table-bordered table-hover"></table>
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
          pageList: [15,50,100,'All'],
          clickToSelect: true,
          sortOrder: 'desc',
          sortName: 'date',
          queryParams:getSearchP,
          responseHandler:responseFun,
          showFooter:true, //添加页脚做统计
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
          [{
                    "halign":"center",
                    "align":"center",
                    "class":'total',
                    "colspan":15
          }],
          [{
              field: 'date',
              title: '日期',
              align: 'center',
              valign: 'middle'
          },{
              field: 'id',
              title: '代理ID',
              align: 'center',
              valign: 'middle',
              footerFormatter:function(values){
                 return '总活跃数:'
              }
          },{
              field: 'account',
              title: '代理账号',
              align: 'center',
              valign: 'middle',
          },{
              field: 'members',
              title: '会员总数',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{
              field: 'active',
              title: '会员活跃数',
              align: 'center',
              valign: 'middle',
              sortable:true,
              footerFormatter:function(values){
                 var count = 0;
                 for (var val in values)
                    count+=parseInt(values[val].active);

                 return colorFormat(count);
              }
          },{
              field: 'roomcard',
              title: '消耗钻石数',
              align: 'center',
              valign: 'middle',
              sortable:true,
              footerFormatter:function(values){
                 var count = 0;
                 for (var val in values)
                    count+=parseInt(values[val].roomcard);

                 return colorFormat(count);
              }
          }]],
          onExpandRow: function (index, row, $detail) {
              console.log(index,row,$detail);
              InitSubTable(index, row, $detail);
          }
      });

      //初始化子表格(无线循环)
      function InitSubTable(index, row, $detail) {
              var parentDate = row.date;
              var parentId = row.id;
              var unitPrice = row.unitPrice;
              var cur_table = $detail.html('<table table-bordered table-hover definewidth></table>').find('table');
              $(cur_table).bootstrapTable({
                  url: '{{info["listUrl"]}}',
                  method: 'get',
                  detailView: false,
                  contentType: "application/json",
                  datatype: "json",
                  cache: false,
                  queryParams:getSearchP,
                  sortOrder: 'desc',
                  sortName: 'date',
                  pageSize: 15,
                  pageList: [15, 25],

              columns: [{
                    field: 'date',
                    title: '日期',
                    align: 'center',
                    valign: 'middle'
                },{
                        field: 'id',
                        title: '代理ID',
                        align: 'center',
                        valign: 'middle'
                },{
                        field: 'account',
                        title: '代理账号',
                        align: 'center',
                        valign: 'middle'
                },{
                        field: 'active',
                        title: '会员活跃数',
                        align: 'center',
                        valign: 'middle',
                        sortable:true
                }],
                      //注册加载子表的事件。注意下这里的三个参数！
              });

              //定义列操作
              function getSearchP(p){
                    sendParameter = p;
                    sendParameter['id'] = parentId;
                    startDate = $("#pick-date-start").val();
                    sendParameter['startDate'] = startDate;
                    sendParameter['date'] = parentDate;
                    return sendParameter;
              }
      }

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
            $('.total').text(String.format("当前查询日期：{0} ~ {1}", startDate, endDate));
            var totalTitle = document.getElementsByClassName('total')[0];
            totalTitle.style.cssText = "background-color:#d9edf7; height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            data = res.data
            return data;
        }
}
</script>
%rebase admin_frame_base
