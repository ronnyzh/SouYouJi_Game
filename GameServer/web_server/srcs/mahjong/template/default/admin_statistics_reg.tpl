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
<div class='rows' style='margin-bottom:10px;'>
        <div class="panel panel-info">
            <div class="panel-heading">
                <h3 class="panel-title">注册人数数据统计</h3>
            </div>
            <div class="panel-body">
                <div id="main" style="width:100%;height:400px;"></div>
            </div>
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
            showExport: true,
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
                   "colspan": 11
                }],
                [{
                    field: 'reg_date',
                    title: '日期',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                     return '总计'
                  }
                }, {
                    field: 'reg_count',
                    title: '注册人数',
                    align: 'center',
                    sortable: true,
                    valign: 'middle',
                    footerFormatter:function(values){
                     var count = 0;
                     for (var val in values)
                        count+=parseFloat(values[val].reg_count)

                     return colorFormat(count);
                  }
                }, {
                    field: 'money_count',
                    title: '充值金额',
                    align: 'center',
                    sortable: true,
                    valign: 'middle',
                    formatter: function(values){
                       values = parseFloat(values);
                       return '<span style="color:red">'+ values + '</span>'
                    },
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+= parseFloat(values[val].money_count)
                         statusstr = String.format('<span style="color:red">{0}</span>',count);
                         return [statusstr].join('');
                    }
                }, {
                    field: 'reg_roomcard',
                    title: '钻石耗钻数',
                    align: 'center',
                    sortable: true,
                    valign: 'middle',
                    formatter: function(values){
                       return '<span style="color:red">'+ values + '</span>'
                    },
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].reg_roomcard)
                         statusstr = String.format('<span style="color:red">{0}</span>',count);
                         return [statusstr].join('');
                    }
                }, {
                    field: 'match_enroll_num',
                    title: '赛事活跃人数',
                    align: 'center',
                    sortable: true,
                    valign: 'middle',
                    formatter: function(values){
                       return '<span style="color:red">'+ values + '</span>'
                    },
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].match_enroll_num)
                         statusstr = String.format('<span style="color:red">{0}</span>',count);
                         return [statusstr].join('');
                    }
                }, {
                    field: 'match_enroll_fee',
                    title: '赛事报名费用',
                    align: 'center',
                    sortable: true,
                    valign: 'middle',
                    formatter: function(values){
                       return '<span style="color:red">'+ values + '</span>'
                    },
                    footerFormatter:function(values){
                         var count = 0;
                         for (var val in values)
                            count+=parseFloat(values[val].match_enroll_fee)
                         statusstr = String.format('<span style="color:red">{0}</span>',count);
                         return [statusstr].join('');
                    }
                }, {
                    field: 'reg_proportion',
                    title: '人数占比',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: reg_status,
                    footerFormatter:function(values){
                     var count = 0;
                     for (var val in values)
                        count += parseFloat(values[val].reg_proportion)
                     count = Math.round(count)
                     if (isNaN(count)) {
                        count = 0
                     }
                     return colorFormat(count);
                  }
                }, {
                    field: 'op',
                    title: '操作',
                    align: 'center',
                    valign: 'middle',
                    formatter: getOp
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

        url = String.format('{0}?startDate={1}&endDate={2}',"{{ info['show_data_url'] }}", startDate, endDate);
        show_graphs('main', url, startDate, endDate);
    }
</script>
<script type="text/javascript">
    function show_graphs(div, url, startDate, endDate) {
        var myChart = echarts.init(document.getElementById(div));
        var resizeWorldMapContainer = function () {
            document.getElementById(div).style.width = $('.panel-body').attr('width');
            document.getElementById(div).style.height = $('.panel-body').attr('height');
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