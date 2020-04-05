<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/echarts.common.min.js"></script>
<div class="block">
    %include admin_frame_header
    <div class="content">
        %include original_search_bar
        <table id="dataTable" class="table table-bordered table-hover"></table>
    </div>
</div>
<script type="text/javascript">
    var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 6);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));

    function initTable() {
        var startDate = $("#pick-date-start").val();
        var endDate = $("#pick-date-end").val();
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
            pageList: [15, 25, 50, 100, 'All'],
            minimumCountColumns: 2,
            clickToSelect: true,
            smartDisplay: true,
            queryParams: getSearchP,
            responseHandler: responseFun,
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
                   "halign":"left",
                   "align":"left",
                   "class": 'count',
                   "colspan": 25
                }],
                [{
                    field: 'date',
                    title: '日期',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                },{
                    field: 'money_count',
                    title: '玩家<br>充值金额',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].money_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                },{
                    field: 'saleRoomcard_count',
                    title: '售出钻石数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].saleRoomcard_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                },{
                    field: 'yyPoint_count',
                    title: '椰云<br>积分兑换数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].yyPoint_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                },{
                    field: 'cyPoint_count',
                    title: '创盈<br>积分兑换数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].cyPoint_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                },{
                    field: 'mailRoomcard_count',
                    title: '后台邮件<br>钻石附件数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].mailRoomcard_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                },{
                    field: 'mailPoint_count',
                    title: '后台邮件<br>积分附件数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].mailPoint_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                },{
                    field: 'compensate_roomcard',
                    title: '增减钻石数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].compensate_roomcard)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                },{
                    field: 'compensate_gamepoint',
                    title: '增减积分数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].compensate_gamepoint)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                },{
                    field: 'shareGame_roomcard',
                    title: '玩家<br>分享钻石数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].shareGame_roomcard)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                }, {
                    field: 'reg_count',
                    title:  '新增玩家',
                    align: 'center',
                    sortable: true,
                    valign: 'middle',
                    colspan: 1,
                    rowspan: 2,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].reg_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                }, {
                    title: String.format('<span style="color:#d9534f">{0}</span>', "房间模式"),
                    valign: "middle",
                    align: "center",
                    colspan: 4,
                    rowspan: 1,
                }, {
                    title: String.format('<span style="color:#428bca">{0}</span>', "比赛场模式"),
                    valign: "middle",
                    align: "center",
                    colspan: 6,
                    rowspan: 1,
                }],
                [{
                    field: 'active_count',
                    title: String.format('<span style="color:#d9534f">{0}</span>', '活跃人数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].active_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                }, {
                    field: 'card_count',
                    title: String.format('<span style="color:#d9534f">{0}</span>', '总耗钻数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].card_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                }, {
                    field: 'take_room_count',
                    title: String.format('<span style="color:#d9534f">{0}</span>', '总开房数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].take_room_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                }, {
                    field: 'room_count',
                    title: String.format('<span style="color:#d9534f">{0}</span>', '总局数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].room_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                }, {
                    field: 'match_login_count',
                    title: String.format('<span style="color:#428bca">{0}</span>', '活跃人数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].match_login_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                }, {
                    field: 'match_enroll_count',
                    title: String.format('<span style="color:#428bca">{0}</span>', '报名人数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].match_enroll_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                }, {
                    field: 'match_count',
                    title: String.format('<span style="color:#428bca">{0}</span>', '赛事总数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].match_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                }, {
                    field: 'match_fee_count',
                    title: String.format('<span style="color:#428bca">{0}</span>', '赛事报名费用'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].match_fee_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                }, {
                    field: 'match_roomcard_count',
                    title: String.format('<span style="color:#428bca">{0}</span>', '钻石赛奖励总数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].match_roomcard_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                }, {
                    field: 'match_gamepoint_count',
                    title: String.format('<span style="color:#428bca">{0}</span>', '积分赛奖励总数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].match_gamepoint_count)
                         if (isNaN(count)){
                            count = 0
                         }
                         return colorFormat(count);
                      }
                }]]
        });

        //定义列操作
        function getSearchP(p) {
            startDate = $("#pick-date-start").val();
            endDate = $("#pick-date-end").val();
            sendParameter = p;

            sendParameter['startDate'] = startDate;
            sendParameter['endDate'] = endDate;
            return sendParameter;
        }

        function getOp(value, row, index) {
            eval('rowobj=' + JSON.stringify(row))
            var opList = []
            for (var i = 0; i < rowobj['op'].length; ++i) {
                var op = rowobj['op'][i];
                var str = JSON.stringify({id: rowobj['account']});
                var cStr = str.replace(/\"/g, "@");

                opList.push(String.format("<a href=\"{0}?reg_date=" + rowobj['reg_date'] + "\" class=\"btn btn-primary btn-sm\" >{1}</a> ", op['url'], op['txt']));
            }
            return opList.join('');
        }

        function reg_status(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          var regStr = '';
          if(rowobj['reg_proportion']){
              regStr = String.format("<span style=\"color:green;\">{0}%</span>", value);
          }else {
              regStr = String.format("<span style=\"color:green;\">{0}%</span>", 0);
          }
          return [regStr].join('');
        }

        //获得返回的json 数据
        function responseFun(res) {
            var data = res;
            $('.count').text(String.format("当前查询日期：{0} ~ {1}", startDate, endDate));
            var totalTitle = document.getElementsByClassName('count')[0];
            totalTitle.style.cssText = "background-color:#d9edf7;height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            return data;
        }

    }
</script>
<script type="text/javascript">
    function show_graphs(div, url, startDate, endDate) {
        var myChart = echarts.init(document.getElementById(div));
        var resizeWorldMapContainer = function () {
            document.getElementById('main').style.width = $('.panel-body').attr('width');
            document.getElementById('main').style.height = $('.panel-body').attr('height');
        };
        resizeWorldMapContainer();
        $.getJSON(url, function(data){
            myChart.setOption({
                    tooltip : {
                        trigger: 'axis'
                    },
                    legend: {
                        data:data.data.legen
                    },
                    title: {
                        text: String.format('{0} ~ {1}', startDate, endDate),
                        subtext: '注册人数'
                    },
                    calculable : true,
                    toolbox: {
                        show : true,
                        feature : {
                            mark : {show: true},
                            dataView : {show: true, readOnly: false},
                            magicType : {show: true, type: ['line', 'bar','tiled']},
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
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
                    xAxis : [
                        {
                            type : 'category',
                            boundaryGap : false,
                            data : data.data.week,
                            axisLabel: {
                                interval: 0
                            },
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value'
                        }
                    ],
                    series : data.data.series
                });
        });

        window.onresize = function () {
            resizeWorldMapContainer();
            myChart.resize();
        };
    }
</script>
%rebase admin_frame_base