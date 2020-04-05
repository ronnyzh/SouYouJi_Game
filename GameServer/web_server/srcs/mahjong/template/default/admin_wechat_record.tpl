<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/echarts.common.min.js"></script>
<div class="block">
    %include admin_frame_header
    <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
        <div class='col-sm-12' style='margin-left:-1em;'>
            <!-- 查询代理ID -->
            <div style='float:left;margin-left:1em;'>
                <input type="text" class=“form-control” placeholder=" 订单号" id='orderNo' name="orderNo" style="width:270px;height:34px;"/>
            </div>
            <div style='float:left;margin-left:1em;'>
                <input type="text" class=“form-control” placeholder=" 用户编号" id='memberId' name="memberId" style="width:150px;height:34px;"/>
            </div>
            <div style='float:left;margin-left:1em;'>
                <select class="form-control" id="orderType" name="orderType">
                    <option value=""> 订单状态（全部）</option>
                    <option value="successful"> 交易成功</option>
                    <option value="pending"> 交易挂起</option>
                </select>
            </div>
            <div style='float:left;margin-left:1em;' id="payType" id="payType">
                <select class="form-control">
                    <option value=""> 支付类型（全部）</option>
                    <option value="weChatPay"> 微信</option>
                    <option value="alipay"> 支付宝</option>
                    <option value="appStore"> AppStore</option>
                </select>
            </div>
        </div>
    </div>
     <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
        <div class='col-sm-12' style='margin-left:-1em; margin-top:10px'>
        <div style='float:left;margin-left:1em;' class="input-group date datetime col-md-1 col-xs-1"
                 data-min-view="2" data-date-format="yyyy-mm-dd">
                <input class="form-control" size="12" type="text" style='width:140px;height:28px;' id='pick-date-start'
                       name="startdate" value="{{lang.INPUT_LABEL_START_DATE_TXT}}" readonly>
                <span class="input-group-addon btn btn-primary pickdate-btn"><span
                        class="glyphicon pickdate-btn pickdate glyphicon-th"></span>
            </div>

            <div style='float:left;margin-left:1em;' class="input-group date datetime col-md-1 col-xs-1"
                 data-min-view="2" data-date-format="yyyy-mm-dd">
                <input class="form-control" style='width:140px;height:28px;' id='pick-date-end' name="enddate" size="12"
                       type="text" value="{{lang.INPUT_LABEL_END_DATE_TXT}}" readonly>
                <span class="input-group-addon btn btn-primary pickdate-btn"><span
                        class="pickdate glyphicon pickdate-btn glyphicon-th"></span></span>
            </div>
        <div style='float:left;margin-left:1em;'>
                <button id="btn_query" class='btn btn-primary btn-sm'>{{lang.INPUT_LABEL_QUERY}}</button>
                <button id="btn_lastMonth" class='btn btn-sm'>{{lang.INPUT_LABEL_PREV_MONTH}}</button>
                <button id="btn_thisMonth" class='btn btn-sm'>{{lang.INPUT_LABEL_CURR_MONTH}}</button>
                <button id="btn_lastWeek" class='btn btn-sm'>{{lang.INPUT_LABEL_PREV_WEEK}}</button>
                <button id="btn_thisWeek" class='btn btn-sm'>{{lang.INPUT_LABEL_CURR_WEEK}}</button>
                <button id="btn_yesterday" class='btn btn-sm'>{{lang.INPUT_LABEL_PREV_DAY}}</button>
                <button id="btn_today" class='btn btn-sm'>{{lang.INPUT_LABEL_CURR_DAY}}</button>
                <div class='clearfix'></div>
            </div>
        </div>
     </div>
    <table id="dataTable" class="table table-bordered table-hover"></table>
</div>
<div class='rows' style='margin-bottom:10px;'>
        <div class="panel panel-info" style="height:500px">
            <div class="panel-heading">
                <h3 class="panel-title">商城订单统计</h3>
            </div>
            <div class="panel-body" style='margin-top:10px;'>
                <div id="wechat_record" style="width:100%;height:400px;"></div>
            </div>
        </div>
</div>
</div>
<script type="text/javascript">
    var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 6);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));
</script>
<script type="text/javascript">
  function initTable() {
     var startDate = $("#pick-date-start").val();
     var endDate   = $("#pick-date-end").val();
     $("#dataTable").bootstrapTable({
                url: "{{info['tableUrl']}}",
                method: 'get',
                pagination: true,
                pageSize: 15,
                search: true,
                showRefresh: true,
                showColumns: true,
                showToggle: true,
                showExport:true,
                showFooter: true,
                cardView: false,
                striped: true,
                exportDataType: 'all',
                exportTypes:[ 'csv', 'txt', 'sql', 'doc', 'excel', 'xlsx', 'pdf'],
                exportOptions:{
                    fileName: '{{ info["title"] }}',
                },
                pageList: [15, 50,100],
                responseHandler:responseFun,
                queryParams:getSearchP,
                columns: [
                [{
                    "title": "搜索日期："+startDate+" 至 "+endDate,
                    "halign":"center",
                    "align":"center",
                    "colspan": 15
                }],
                [{
                    "halign":"center",
                    "align":"center",
                    "class":'totalMoney',
                    "colspan":15
                }],
                [{
                    field: 'orderNo',
                    title: '订单号',
                    sortable: true,
                    align: 'center',
                    valign: 'middle',
                },{
                    field: 'pay_type',
                    title: '支付类型',
                    align: 'center',
                    valign: 'middle',
                    formatter:pay_type
                },{
                    field: 'order_type',
                    title: '订单状态',
                    align: 'center',
                    valign: 'middle',
                    formatter:status
                },{
                    field: 'memberId',
                    align: 'center',
                    valign: 'middle',
                    title: '玩家编号'
                },{
                    field: 'memberAccount',
                    title: '玩家账号',
                    align: 'center',
                    valign: 'middle',
                },{
                    field: 'memberNickname',
                    title: '玩家昵称',
                    align: 'center',
                    valign: 'middle',
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
                    %if info['action'] == 'FISH':
                        title: '购买金币数',
                    %else:
                        title: '购买数',
                    %end
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                       var count = 0 ;
                       for (var val in values)
                            count+=parseInt(values[val].good_count)

                       return colorFormat(count)
                    }
                },{
                    field: 'order_paytime',
                    title: '订单生成时间',
                    align: 'center',
                    valign: 'middle',
                    sortable: true
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

    function pay_type(value,row,index){
        eval('var rowobj='+JSON.stringify(row))
        var statusstr = '';
        if(rowobj['pay_type'] == 'alipay'){
            statusstr = '<span class="label label-primary">支付宝</span>';
        }else if(rowobj['pay_type'] == 'weChatpay'){
            statusstr = '<span class="label label-success">微信</span>';
        }else{
            statusstr = '<span class="label label-danger">AppStore</span>';
        }

        return [
            statusstr
        ].join('');
    }

    function getSearchP(p){
          var startDate = $("#pick-date-start").val();
          var endDate   = $("#pick-date-end").val();
          var orderNo = $("#orderNo").val();
          var memberId = $("#memberId").val();
          var orderType = $('#orderType option:selected').val();
          var payType = $('#payType option:selected').val();
          sendParameter = p;
          sendParameter['startDate'] = startDate;
          sendParameter['endDate']  = endDate;
          sendParameter['orderNo'] = orderNo;
          sendParameter['memberId'] = memberId;
          sendParameter['orderType'] = orderType;
          sendParameter['payType'] = payType;
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

        top_show_str = String.format("订单总金额：{0}&nbsp; 交易成功金额：{1}&nbsp; 交易挂起金额：{2}",moneyCount,successMoney,pendingMoney);
        $('.totalMoney').html(top_show_str)
        var totalMoney = document.getElementsByClassName('totalMoney')[0];
        totalMoney.style.cssText = "background-color:#d9edf7;height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
        return {"data": res.data,"total": res.orderCount};
    };

    url = String.format('{0}?startDate={1}&endDate={2}',"{{ info['wechatRecordUrl'] }}", startDate, endDate);
    show_graphs('wechat_record', url, startDate, endDate);
 }
</script>
<script type="text/javascript">
    function show_graphs(div, url, startDate, endDate) {
        var myChart = echarts.init(document.getElementById(div));
        var resizeWorldMapContainer = function () {
            document.getElementById(div).style.width = $('.panel-body').attr('width');
            document.getElementById(div).style.height = $('.panel-body').attr('height');
        };

        $.getJSON(url, function (data) {
            myChart.setOption({
                tooltip: {
                    trigger: 'axis',
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '10%',
                    top: '20%',
                    containLabel: true
                },
                legend: {
                    data: data.data.legen
                },
                /*
                title: {
                    text: String.format('{0} ~ {1}', startDate, endDate),
                    subtext: '商城订单统计'
                },
                */
                calculable: true,
                toolbox: {
                    show: true,
                    feature: {
                        mark: {show: true},
                        dataView: {show: true, readOnly: false},
                        magicType: {show: true, type: ['line', 'bar', 'tiled']},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    },
                    orient: 'horizontal',
                    top: '25',
                },
                calculable: true,
                dataZoom: [{
                        show: true,
                        realtime: true,
                        start: 0,
                        end: data.data.dataZoom_start
                    },{
                        type: 'inside',
                        realtime: true,
                        start: 0,
                        end: 10
                }],
                xAxis: [
                    {
                        type: 'category',
                        boundaryGap: false,
                        data: data.data.week,
                        axisLabel: {
                            interval: 0
                        },
                    }
                ],
                yAxis: [
                    {
                        type: 'value'
                    }
                ],
                series: data.data.series
            });
        });

        window.onresize = function () {
            resizeWorldMapContainer();
            myChart.resize();
        };
    }
</script>
%rebase admin_frame_base
