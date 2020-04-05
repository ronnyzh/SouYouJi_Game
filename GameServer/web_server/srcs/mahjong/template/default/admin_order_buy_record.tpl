<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
    %include admin_frame_header
    <div class="content">
        %include original_search_bar
        <table id="dataTable" class="table table-bordered table-hover"></table>
    </div>
</div>
<script type="text/javascript">
  var firstDate=new Date();
  firstDate.setDate(firstDate.getDate()-6);
  $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
  $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));
  
  /**------------------------------------------------
    *  代理操作日志
    -------------------------------------------------
  */
  function initTable() {
      startDate = $("#pick-date-start").val();
      endDate   = $("#pick-date-end").val();
        $("#dataTable").bootstrapTable({
              url: "{{info['tableUrl']}}",
              method: 'get',
              pagination: true,
              pageSize: 15,
              search: true,
              showExport: true,
              exportTypes:['excel', 'csv', 'pdf', 'json'],
              showRefresh: true,
              pageList: [15, 25],
              responseHandler:responseFun,
              queryParams:getSearchP,
              columns: [{
                  field: 'cardNums',
                  sortable: true,
                  align: 'center',
                  valign: 'middle',
                  title: '购钻数(张)'
              },{
                  field: 'applyAccount',
                  align: 'center',
                  valign: 'middle',
                  title: '买钻方'
              },{
                  field: 'saleAccount',
                  align: 'center',
                  valign: 'middle',
                  title: '卖钻方'
              }, {
                  field: 'status',
                  title: '订单状态',
                  align: 'center',
                  valign: 'middle',
                  formatter:status
              },{
                  field: 'finish_date', 
                  align: 'center',
                  valign: 'middle',
                  sortable: true,
                  title: '系统确认时间'
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

  function status(value,row,index){
      eval('var rowobj='+JSON.stringify(row))
      var statusstr = '';
      if(rowobj['status'] == '0'){
          statusstr = '<span class="label label-danger">卖钻方未确认</span>';
      }else if(rowobj['status'] == '1'){
          statusstr = '<span class="label label-success">卖钻方已确认</span>';
      }

      return [
          statusstr
      ].join('');
  }

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
            var str = JSON.stringify({orderNo : rowobj['orderNo']});
            var cStr = str.replace(/\"/g, "@");
            var param = rowobj['orderNo'] ;
            if(op['url'] == '/admin/order/cancel')
            {     
                  if (rowobj['status'] == '1')
                      continue;
                  var contentUrl = op['url'];
                  opList.push(String.format("<a href=\"#\" class=\"btn btn-primary btn-sm\" onclick=\"cancelOrderDialog(\'{0}\',\'{1}\',\'{2}\')\"><i class=\"glyphicon glyphicon-edit\"> {3} </i></a> ",contentUrl, op['method'],cStr,op['txt']));
            }
        }
        return opList.join('');
  }

  //获得返回的json 数据
  function responseFun(res){
      return res;
  }
}
</script>
%rebase admin_frame_base