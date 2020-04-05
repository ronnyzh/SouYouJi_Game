<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<div class="block">
          %include admin_frame_header
          <div class="content">
            <span id='total' style='position:relative;left:20px;font-size:14px;margin-right:20px'></span>
             %include original_search_bar
             <table id="dataTable" class="table table-bordered table-hover"></table>
          </div>
</div>
<script type="text/javascript">
  /**------------------------------------------------
    *  代理操作日志
    -------------------------------------------------
  */
  function initTable() {
    startDate = $("#pick-date-start").val();
    endDate   = $("#pick-date-end").val();
    $('#dataTable').bootstrapTable({
          method: 'get',
          url: '{{info["listUrl"]}}',
          contentType: "application/json",
          datatype: "json",
          cache: false,
          checkboxHeader: true,
          striped: true,
          pagination: true,
          pageSize: 24,
          pageList: [24, 48, 100, 'All'],
          search: true,
          clickToSelect: true,
          sortOrder: 'desc',
          sortName: 'datetime',
          queryParams:getSearchP,
          responseHandler:responseFun,
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
                halign: "center",
                font: 15,
                align: "left",
                class: "total",
                colspan: 17
            }],
            [{
              field: 'date',
              title: '日期',
              align: 'center',
              valign: 'middle',
              footerFormatter:function(values){
                       return '总计:'
              }
          },{
              field: 'cardNums',
              title: '当日售钻数',
              align: 'center',
              valign: 'middle',
              sortable: true,
              footerFormatter:function(values){
                    var count = 0;
                    for (var val in values)
                        count+=parseInt(values[val].cardNums);

                    return colorFormat(count);
              }
          },{
              field: 'totalNums',
              title: '历史售钻数',
              align: 'center',
              valign: 'middle',
              sortable: true,
              footerFormatter:function(values){
                    var count = 0;
                    for (var val in values)
                        count+=parseInt(values[val].totalNums);

                    return colorFormat(count);
              }
          }]]
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
            $('.total').text(String.format("当前查询日期：{0} ~ {1}", startDate, endDate));
            var totalTitle = document.getElementsByClassName('total')[0];
            totalTitle.style.cssText = "background-color:#d9edf7;height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            data = res.result
            return data;
      }
}
</script>
%rebase admin_frame_base
