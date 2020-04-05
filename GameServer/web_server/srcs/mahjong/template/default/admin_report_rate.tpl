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
          pageList: [15,50,100, 'All'],
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
          clickToSelect: true,
          sortOrder: 'desc',
          sortName: 'date',
          queryParams:getSearchP,
          responseHandler:responseFun,
          showExport:true,
          showFooter:true,
          columns: [
            {
              field: 'date',
              title: '日期',
              align: 'center',
              valign: 'middle',
            },{
              field: 'id',
              title: 'ID',
              align: 'center',
              valign: 'middle',
              sortable:true,
              footerFormatter:function(values){
                  return '销售总计'
              }
          },{
              field: 'number',
              title: '销售个数',
              align: 'center',
              valign: 'middle',
              footerFormatter:function(values){
                  var count = 0;
                  for (var val in values)
                      count+=parseInt(values[val].number)

                  return '销售总数:'+colorFormat(count);
              }
          },{
            field: 'unitPrice',
            title: '销售单价(元)',
            align: 'center',
            valign: 'middle',
            formatter:getColor,
         },{
            field: 'rate',
            title: '该代理占额/个(元)',
            align: 'center',
            valign: 'middle',
            formatter:getColor,
        },{
              field: 'rateTotal',
              title: '该代理占额(元)',
              align: 'center',
              valign: 'middle',
              formatter:getColor,
              footerFormatter:function(values){
                  var count = 0;
                  for (var val in values)
                      if ("rateTotal" in values[val])
                          count+=parseFloat(values[val].rateTotal);

                  return '下线代理总占额:'+colorFormat(count.toFixed(2));
              }
          },{
                  field: 'superRateTotal',
                  title: '我的占额(元)',
                  align: 'center',
                  valign: 'middle',
                  formatter:getColor,
                  footerFormatter:function(values){
                      var count = 0;
                      for (var val in values)
                          if ("superRateTotal" in values[val])
                              count+=parseFloat(values[val].superRateTotal);

                      return '我的总占额:'+colorFormat(count.toFixed(2));
                  }
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
