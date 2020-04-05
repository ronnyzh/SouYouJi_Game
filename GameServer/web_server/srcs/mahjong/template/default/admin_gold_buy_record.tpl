

<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>

<div class="block">
          <div class="header bordered-bottom bordered-themesecondary" id="crumb">
              %if info.get('title', None):
              <i class="widget-icon fa fa-tags themesecondary"></i>
              <span class="widget-caption themesecondary" style='font-size:16px;font-weight:bold' id="subTitle">{{info['title']}}</span>
              %end
              <!-- 解 绑 规 则 -->
          </div>
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
                showRefresh: true,
                showExport: true,
                exportTypes: ['excel', 'csv', 'pdf', 'json'],
                pageList: [15, 25],
                responseHandler: responseFun,
                queryParams:getSearchP,
         columns: [
                       {
                       field: 'date',
                       title: '时间',
                       align: 'center',
                       valign: 'middle',
                       sortable: true
                       },{
                       field: 'account',
                       title: '微信账号',
                       align: 'center',
                       valign: 'middle',
                       sortable: true
                       },{
                       field: 'gold',
                       title: '金币数',
                       align: 'center',
                       valign: 'middle',
                       sortable: true
                       },{
                       field: 'money',
                       title: '金额',
                       align: 'center',
                       valign: 'middle',
                       sortable: true
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
                      var str = JSON.stringify({id : rowobj['id']});
                      var cStr = str.replace(/\"/g, "@");
                      if(op['url'] == '/admin/niuniu/set_cash_journal')
                          opList.push(String.format("<a href=\"#\" class=\"btn btn-info\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"><i class=\"fa fa-edit\"> {3} </i></a> ", op['url'], op['method'], cStr, op['txt']));
                      else
                          opList.push(String.format("<a href=\"{0}?id="+rowobj['id']+"\" class=\"btn btn-info\" ><i class=\"fa fa-edit\"> {1} </i></a> ", op['url'],op['txt']));
                  }
                  return opList.join('');
              }


    //获得返回的json 数据
    function responseFun(res){
//        count= res.orderCount;
//        totalMoney = res.moneyCount
//        pendingMoney = res.pendingMoney
//        successMoney = res.successMoney
//        //实时刷
//        $('.count').text(count);
//        $('.totalMoney').html("总交易额: "+totalMoney+"&nbsp;  交易成功总额: "+successMoney+"&nbsp;交易挂起总额: "+pendingMoney);
//
//        return {"data": res.data,"total": res.orderCount};
        return {"data": res.data,"total": 0};
    }
 }

  //如果有searchId自动搜索
 $(document).ready(function(){
      initTable();
      var testCount = 10;//尝试10次
      (function () {
          if (--testCount < 0)return;
          var selfFunc = arguments.callee;
          var input = $('[placeholder="搜索"]');
          if (!input) {
              setTimeout(selfFunc, 1000);
              return;
          }
//          input.val(searchId);
          input.keyup()
      })();

      //隐藏搜索日期
     $('.table-toolbar').hide()
 })
</script>
%rebase admin_frame_base