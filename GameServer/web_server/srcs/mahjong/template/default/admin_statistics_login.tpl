<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<div class="cl-mcont">
  <div class="block">
            <div class="header">              
              <h3>
                %if info.get('title',None):
                  {{info['title']}}
                %end
              </h3>
            </div>
            <div class="content">
               %include original_search_bar
               <table id="dataTable" class="table table-bordered table-hover"></table>
            </div>
  </div>
</div>
<script type="text/javascript">
  var firstDate=new Date();
  firstDate.setDate(firstDate.getDate()-6);
  $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
  $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));
  
  /**------------------------------------------------
    *  代理操作日志
    *
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
          pageList: [12, 48, 100, 'All'],
          minimumCountColumns: 2,
          clickToSelect: true,
          smartDisplay: true,
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
          {
              field: 'reg_date',
              title: '日期',
              align: 'center',
              valign: 'middle'
          },{
              field: 'reg_count',
              title: '登录人数',
              align: 'center',
              valign: 'middle'
          },{
              field: 'op',
              title: '操作',
              align: 'center',
              valign: 'middle',
              formatter:getOp
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

        function getOp(value,row,index){
            eval('rowobj='+JSON.stringify(row))
            var opList = []
            for (var i = 0; i < rowobj['op'].length; ++i) {
                var op = rowobj['op'][i];
                var str = JSON.stringify({id : rowobj['account']});
                var cStr = str.replace(/\"/g, "@");

                opList.push(String.format("<a href=\"{0}?reg_date="+rowobj['reg_date']+"\" class=\"btn btn-xs btn-primary\" ><i class=\"fa fa-edit\"> {1} </i></a> ", op['url'],op['txt']));
            }
            return opList.join('');
        }

        //获得返回的json 数据
        function responseFun(res){
            data = res
            return data;
        }
}
</script>
%rebase admin_frame_base