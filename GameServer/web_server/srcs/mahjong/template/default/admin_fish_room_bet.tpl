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

  $('#room_name').change(function(e){
        refreshUrl = '{{info["tableUrl"]}}';
        console.log('-----------refresh url:'+refreshUrl);
        $("#dataTable").bootstrapTable('refresh',{'url':refreshUrl});
  });
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
                contentType: "application/json",
                datatype: "json",
                cache:false,
                pagination: true,
                pageSize: 15,
                pageList: '{{PAGE_LIST}}',
                queryParamsType:'',
                sidePagination:"server",
                showRefresh: true,
                showExport: true,
                exportTypes:['excel', 'csv', 'pdf', 'json'],
                responseHandler:responseFun,
                queryParams:getSearchP,
                showFooter:true,
                onSort:getSortByClick,
                columns: [
                [{
                    "title": "搜索日期:"+startDate+"至"+endDate,
                    "halign":"center",
                    "align":"center",
                    "colspan": 11
                }],
                [{
                    "halign":"center",
                    "align":"center",
                    "colspan":7
                },{
                    "title":"产生总奖券",
                    "halign":"center",
                    "align":"center",
                    "class":'ticketTotal',
                    "colspan":1
                },{
                    "title":"消耗总金币",
                    "halign":"center",
                    "align":"center",
                    "class":'betTotalMoney',
                    "colspan":1
                },{
                    "title":"收益总金币",
                    "halign":"center",
                    "align":"center",
                    "class":'WinLoseMoney',
                    "colspan":1
                },{
                    "title":"胜负比例",
                    "halign":"center",
                    "align":"center",
                    "class":'winLoseRate',
                    "colspan":1
                }],
                [{
                    field: 'login_time',
                    align: 'center',
                    valign: 'middle',
                    title: '入房时间',
                    sortable: true
                },{
                    field: 'datetime',
                    title: '开始时间',
                    align: 'center',
                    valign: 'middle',
                    sortable: true
                },{
                    field: 'bet_id',
                    align: 'center',
                    valign: 'middle',
                    title: '入房ID'
                },{
                    field: 'uid',
                    title: '玩家编号',
                    align: 'center',
                    valign: 'middle',
                },{
                    field: 'room_id',
                    align: 'center',
                    valign: 'middle',
                    title: '房间名称',
                    footerFormatter:function(values){
                        return '总计:'
                    }
                },{
                    field: 'init_coin',
                    align: 'center',
                    valign: 'middle',
                    title: '入房金币',
                    formatter:getColor
                },{
                    field: 'add_coin',
                    align: 'center',
                    valign: 'middle',
                    title: '充值金币',
                    formatter:getColor
                },{
                    field: 'bet',
                    align: 'center',
                    valign: 'middle',
                    title: '消耗金币',
                    sortable: true,
                    formatter:getColor
                },{
                    field: 'profit',
                    sortable: true,
                    align: 'center',
                    valign: 'middle',
                    title: '最终结果',
                    sortable: true,
                    formatter:getFuncColor
                },{
                    field: 'add_ticket',
                    sortable: true,
                    align: 'center',
                    valign: 'middle',
                    title: '下注产生奖票',
                    sortable: true,
                    formatter:getFuncColor
                },{
                    field: 'op',
                    title: '操作',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter:getOp
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

    function getSortByClick(name,sort){ //列排序
          console.log(String.format('------getSortByClick name[{0}] sort[{1}]',name,sort));
          $('#dataTable').bootstrapTable('refresh',{'url':String.format('{0}&sort_name={1}&sort_method={2}','{{info["tableUrl"]}}',name,sort)});
    }

    function getSearchP(p){
          startDate = $("#pick-date-start").val();
          endDate   = $("#pick-date-end").val();
          room_id   = $("#room_name").val();
          user_id   = $("#user_id").val();

          sendParameter = p;

          sendParameter['startDate'] = startDate;
          sendParameter['endDate']  = endDate;
          sendParameter['room_id']  = room_id;
          sendParameter['user_id']  = user_id;

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
        totalMoney = res.betTotal;
        winLostTotal = res.winLostTotal;
        winLostRate = res.winLostRate;
        ticketTotal = res.ticketTotal;
        //实时刷
        $('.betTotalMoney').html(String.format("消耗金币总额:<font color='#6600FF'>{0}</font>",totalMoney));

        if (parseInt(winLostTotal)>0){
            showStr = "结果统计:<font color='red'>+{0}</font>";;
        }else{
            showStr = "结果统计:<font color='green'>{0}</font>";
            showWinStr = "百分比:<font color='green'>{0}%</font>";
        }

        if (parseInt(winLostRate)>0){
            showWinStr = "百分比:<font color='red'>{0}%</font>"
        }else {
            showWinStr = "百分比:<font color='green'>{0}%</font>";
        }

        $('.WinLoseMoney').html(String.format(showStr,winLostTotal));
        $('.winLoseRate').html(String.format(showWinStr,winLostRate));
        $('.ticketTotal').html(String.format("产生总奖券:<font color='#6600FF'>{0}</font>",ticketTotal));

        return {"rows": res.result,"total": res.count};
    }
 }
</script>
%rebase admin_frame_base
