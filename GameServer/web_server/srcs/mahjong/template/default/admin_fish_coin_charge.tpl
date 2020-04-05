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
  /**------------------------------------------------
    *  捕鱼投注明细前端
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
                showRefresh: true,
                showExport: true,
                exportTypes:['excel', 'csv', 'pdf', 'json'],
                pageList: [15, 25],
                responseHandler:responseFun,
                queryParams:getSearchP,
                columns: [
                [{
                    "title": "搜索日期:"+startDate+"至"+endDate,
                    "halign":"center",
                    "align":"center",
                    "colspan": 9
                }],
                [{
                    field: 'recharge_id',
                    sortable: true,
                    align: 'center',
                    valign: 'middle',
                    title: '充值单号'
                },{
                    field: 'recharge_source',
                    sortable: true,
                    align: 'center',
                    valign: 'middle',
                    title: '充值渠道'
                },{
                    field: 'status',
                    sortable: true,
                    align: 'center',
                    valign: 'middle',
                    title: '充值状态'
                },{
                    field: 'user_id',
                    title: '充值玩家',
                    align: 'center',
                    valign: 'middle',
                },{
                    field: 'coin',
                    align: 'center',
                    valign: 'middle',
                    title: '充值金币',
                },{
                    field: 'price',
                    align: 'center',
                    valign: 'middle',
                    title: '价格',
                },{
                    field: 'datetime',
                    align: 'center',
                    valign: 'middle',
                    title: '充值时间'
                }]],

                //注册加载子表的事件。注意下这里的三个参数！
                onExpandRow: function (index, row, $detail) {
                    console.log(index,row,$detail);
                    InitSubTable(index, row, $detail);
                }
      });

    function status(value,row,index){
        eval('var rowobj='+JSON.stringify(row))
        var statusstr = '';
        if(rowobj['order_type'] == 'pending'){
            statusstr = '<span class="label label-danger">交易挂起</span>';
        }else{
            statusstr = '<span class="label label-success">交易成功</span>';
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
              var str = JSON.stringify({orderNo:rowobj["orderNo"]});
              var cStr = str.replace(/\"/g, "@");
             if (rowobj['status'] == '1')
                  continue;
              var contentUrl = op['url'];
              opList.push(String.format("<a href=\"#\" class=\"btn btn-primary btn-sm\" onclick=\"comfirmOrderDialog(\'{0}\',\'{1}\',\'{2}\')\"><i class=\"glyphicon glyphicon-edit\"> {3} </i></a> ",contentUrl,op['method'],cStr,op['txt']));
          }
          return opList.join('');
    }

    //获得返回的json 数据
    function responseFun(res){
        count= res.orderCount;
        return {"data": res.data,"total": res.orderCount};
    }
 }
</script>
%rebase admin_frame_base
