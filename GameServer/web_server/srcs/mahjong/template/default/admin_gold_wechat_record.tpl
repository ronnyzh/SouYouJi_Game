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
    *  微信前端
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
                showFooter:true,
                exportTypes:['excel', 'csv', 'pdf', 'json'],
                pageList: [15, 50,100],
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
                    "halign":"center",
                    "align":"center",
                    "class":'totalMoney',
                    "colspan":8
                }],
                [{
                    field: 'order_paytime',
                    title: '订单生成时间',
                    align: 'center',
                    valign: 'middle',
                    sortable: true
                },{
                    field: 'orderNo',
                    sortable: true,
                    align: 'center',
                    valign: 'middle',
                    title: '订单号'
                },{
                    field: 'order_type',
                    title: '交易状态',
                    align: 'center',
                    valign: 'middle',
                    formatter:status
                },{
                    field: 'memberId',
                    align: 'center',
                    valign: 'middle',
                    title: '玩家编号'
                },{
                    field: 'group_id',
                    align: 'center',
                    valign: 'middle',
                    title: '所属公会'
                },{
                    field: 'good_name',
                    sortable: true,
                    align: 'center',
                    valign: 'middle',
                    title: '商品名称',
                    footerFormatter:function(values){
                       return '订单总计:'
                    }
                },{
                    field: 'good_money',
                    title: '商品价格/元',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                       var count = 0 ;
                       for (var val in values)
                            count+=parseFloat(values[val].good_money)

                       return colorFormat(count.toFixed(2))
                    }
                },{
                    field: 'good_count',
                    title: '购买金币数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                       var count = 0 ;
                       for (var val in values)
                            count+=parseInt(values[val].good_count)

                       return colorFormat(count)
                    }
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
        var count = res.orderCount
            ,moneyCount = res.moneyCount
            ,successMoney = res.successMoney
            ,pendingMoney = res.pendingMoney;

        top_show_str = String.format("订单总金额:{0}&nbsp;交易成功金额:{1}&nbsp;交易挂起金额:{2}",moneyCount,successMoney,pendingMoney);

        $('.totalMoney').html(top_show_str)

        return {"data": res.data,"total": res.orderCount};
    }
 }
</script>
%rebase admin_frame_base
