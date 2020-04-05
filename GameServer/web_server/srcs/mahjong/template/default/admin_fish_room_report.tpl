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
                pageList: '{{PAGE_LIST}}',
                responseHandler:responseFun,
                showFooter:true,
                queryParams:getSearchP,
                columns: [
                [{
                    "title": "搜索日期:"+startDate+"至"+endDate,
                    "halign":"center",
                    "align":"center",
                    "colspan": 9
                }],      
                [{
                    field: 'agent_account',
                    title: '代理账号',
                    align: 'center',
                    valign: 'middle'
                },{
                    field: 'agent_id',
                    align: 'center',
                    valign: 'middle',
                    title: '代理ID',
                    footerFormatter:function(value){
                        return '总计:'
                    }
                },{
                    field: 'bet',
                    align: 'center',
                    valign: 'middle',
                    title: '投注总金额',
                    sortable: true,
                    formatter:getColor,
                    footerFormatter:function(values){
                          var count = 0 ;
                          for (var value in values)
                            count+=values[value].bet;
                          return getColor(count,{},0);
                    }
                },{
                    field: 'profit',
                    sortable: true,
                    align: 'center',
                    valign: 'middle',
                    title: '输赢总金额',
                    formatter:getFuncColor,
                    footerFormatter:function(values){
                          var count = 0 ;
                          for (var value in values)
                            count+=values[value].profit;
                          return getFuncColor(count,{},0);
                    }
                }]],

                //注册加载子表的事件。注意下这里的三个参数！
                onExpandRow: function (index, row, $detail) {
                    console.log(index,row,$detail);
                    InitSubTable(index, row, $detail);
                }
      });

    function showFootTotal(values){
          var count = 0 ;
          for (var value in values)
            count+=values[value].bet;

          return getColor(count,{},0);
    }

    function getSearchP(p){
          startDate = $("#pick-date-start").val();
          endDate   = $("#pick-date-end").val();
          group_id   = $("#group_id").val();

          sendParameter = p;

          sendParameter['startDate'] = startDate;
          sendParameter['endDate']  = endDate;
          sendParameter['group_id']  = group_id;

          return sendParameter;
    }
    
    function getOp(value,row,index){
          eval('rowobj='+JSON.stringify(row))
          var opList = []
          for (var i = 0; i < rowobj['op'].length; ++i) {
              var op = rowobj['op'][i];
              var str = JSON.stringify({replay_id:rowobj["bet_id"]});
                console.log(String.format("-------------show bet replay replayId[{0}]",rowobj["bet_id"]))
              opList.push(String.format("<a href=\"#\" class=\"btn btn-primary btn-sm\" onclick=\"showFishReplay(\'{0}\',\'{1}\',\'{2}\')\"><i class=\"glyphicon glyphicon-edit\"> {3} </i></a> ",op['url'],op['method'],rowobj['bet_id'],op['txt']));
          }
          return opList.join('');
    }

    //获得返回的json 数据 
    function responseFun(res){
        var count = res.count;
        return res.data;
    }
 }
</script>
%rebase admin_frame_base