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
    <div class="panel panel-info" style="height:500px">
        <div class="panel-heading">
            <h3 class="panel-title">活跃人数数据统计</h3>
        </div>
        <div class="panel-body" style='margin-top:10px;'>
            <div id="main" style="width:100%;height:400px;"></div>
        </div>
    </div>
</div>
<script type="text/javascript">

    function initTable() {
        startDate = $("#pick-date-start").val();
        endDate = $("#pick-date-end").val();
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
            pageList: '{{PAGE_LIST}}',
            minimumCountColumns: 2,
            clickToSelect: true,
            smartDisplay: true,
            queryParams: getSearchP,
            responseHandler: responseFun,
            search: true,
            showRefresh: true,
            showColumns: true,
            showToggle: true,
            showExport: true,
            showFooter: true,
            cardView: false,
            exportDataType: 'all',
            exportTypes: ['csv', 'txt', 'sql', 'doc', 'excel', 'xlsx', 'pdf'],
            exportOptions: {
                fileName: '{{ info["title"] }}',
            },
            columns: [
                [{
                    "halign": "left",
                    "align": "left",
                    "class": 'count',
                    "colspan": 20
                }],
                [{
                    field: 'date',
                    title: '日期',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                }, {
                    title: String.format('<span style="color:#d9534f">{0}</span>', "房间模式"),
                    valign: "middle",
                    align: "center",
                    colspan: 7,
                    rowspan: 1,
                }, {
                    title: String.format('<span style="color:#428bca">{0}</span>', "比赛场模式"),
                    valign: "middle",
                    align: "center",
                    colspan: 5,
                    rowspan: 1,
                }, {
                    field: 'op',
                    title: '更多详情',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter:getOp,
                    colspan: 1,
                    rowspan: 2,
                }],
                [{
                    field: 'login_count',
                    title: String.format('<span style="color:#d9534f">{0}</span>', "活跃人数"),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter: function (values) {
                        var count = 0;
                        for (var val in values)
                            count += parseFloat(values[val].login_count)

                        return colorFormat(count);
                    }
                }, {
                    field: 'take_card',
                    title: String.format('<span style="color:#d9534f">{0}</span>', '钻石消耗'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter: function (values) {
                        var count = 0;
                        for (var val in values)
                            count += parseFloat(values[val].take_card)

                        return colorFormat(count);
                    }
                }, {
                    field: 'take_room_count',
                    title: String.format('<span style="color:#d9534f">{0}</span>', '开房统计'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter: function (values) {
                        var count = 0;
                        for (var val in values)
                            count += parseFloat(values[val].take_room_count)
                        return colorFormat(count);
                    }
                }, {
                    field: 'take_count',
                    title: String.format('<span style="color:#d9534f">{0}</span>', '局数统计'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter: function (values) {
                        var count = 0;
                        for (var val in values)
                            count += parseFloat(values[val].take_count)
                        return colorFormat(count);
                    }
                }, {
                    field: 'login_proportion',
                    title: String.format('<span style="color:#d9534f">{0}</span>', '登录人数占比'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: login_proportion,
                    footerFormatter: function (values) {
                        var count = 0;
                        for (var val in values)
                            count += parseFloat(values[val].login_proportion)
                        count = Math.round(count)
                        if (isNaN(count)) {
                            count = 0
                        }
                        return colorFormat(count);
                    }
                }, {
                    field: 'card_proportion',
                    title: String.format('<span style="color:#d9534f">{0}</span>', '钻石占比'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: card_proportion,
                    footerFormatter: function (values) {
                        var count = 0;
                        for (var val in values)
                            count += parseFloat(values[val].card_proportion)
                        count = Math.round(count)
                        if (isNaN(count)) {
                            count = 0
                        }
                        return colorFormat(count);
                    }

                }, {
                    field: 'task_proportion',
                    title: String.format('<span style="color:#d9534f">{0}</span>', '局数占比'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: task_proportion,
                    footerFormatter: function (values) {
                        var count = 0;
                        for (var val in values)
                            count += parseFloat(values[val].task_proportion)
                        count = Math.round(count)
                        if (isNaN(count)) {
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
                    footerFormatter: function (values) {
                        var count = 0;
                        for (var val in values)
                            count += parseFloat(values[val].match_login_count)
                        return colorFormat(count);
                    }
                }, {
                    field: 'match_enroll_count',
                    title: String.format('<span style="color:#428bca">{0}</span>', '报名人数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter: function (values) {
                        var count = 0;
                        for (var val in values)
                            count += parseFloat(values[val].match_enroll_count)
                        return colorFormat(count);
                    }
                }, {
                    field: 'match_fee_count',
                    title: String.format('<span style="color:#428bca">{0}</span>', '报名费用'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter: function (values) {
                        var count = 0;
                        for (var val in values)
                            count += parseFloat(values[val].match_fee_count)

                        return colorFormat(count);
                    }
                }, {
                    field: 'match_roomcard_count',
                    title: String.format('<span style="color:#428bca">{0}</span>', '钻石赛奖励'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter: function (values) {
                        var count = 0;
                        for (var val in values)
                            count += parseFloat(values[val].match_roomcard_count)
                        return colorFormat(count);
                    }
                }, {
                    field: 'match_gamepoint_count',
                    title: String.format('<span style="color:#428bca">{0}</span>', '积分赛奖励'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter: function (values) {
                        var count = 0;
                        for (var val in values)
                            count += parseFloat(values[val].match_gamepoint_count)
                        count = parseInt(count)
                        if (isNaN(count)) {
                            count = 0
                        }
                        return colorFormat(count);
                    }
                }]],
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
            var showDataUrls = [
                '/admin/statistics/active/showDay11'
            ];
            eval('rowobj=' + JSON.stringify(row))
            var opList = []
            for (var i = 0; i < rowobj['op'].length; ++i) {
                var op = rowobj['op'][i];
                var str = JSON.stringify({id: rowobj['account']});
                var cStr = str.replace(/\"/g, "@");
                // if(showDataUrls.indexOf(op['url'])>=0)
                //opList.push(String.format("<a href='javascript:;' onclick=\"showActiveDialog(\'{0}\', \'{1}\', \'{2}\');\" class=\"btn btn-sm btn-primary\" >{3}</a> ", op['url'],op['method'],rowobj['date'],op['txt']));
                //else //不使用弹出窗口打开页面
                opList.push(String.format("<a href=\"{0}?day={1}\" class=\"btn btn-sm btn-primary\">{2}</a>", op['url'], rowobj['date'], op['txt']));
            }
            return opList.join('');
        }

        //获得返回的json 数据
        function responseFun(res) {
            var data = res;
            $('.count').text(String.format("当前查询日期：{0} ~ {1}", startDate, endDate));
            var totalTitle = document.getElementsByClassName('count')[0];
            totalTitle.style.cssText = "background-color:#d9edf7; height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            return data;
        }

        function login_proportion(value, row, index) {
            eval('var rowobj=' + JSON.stringify(row))
            var regStr = '';
            if (rowobj['login_proportion']) {
                regStr = String.format("<span style=\"color:green;\">{0}%</span>", value);
            } else {
                regStr = String.format("<span style=\"color:green;\">{0}%</span>", 0);
            }
            return [regStr].join('');
        }

        function card_proportion(value, row, index) {
            eval('var rowobj=' + JSON.stringify(row))
            var regStr = '';
            if (rowobj['card_proportion']) {
                regStr = String.format("<span style=\"color:green;\">{0}%</span>", value);
            } else {
                regStr = String.format("<span style=\"color:green;\">{0}%</span>", 0);
            }
            return [regStr].join('');
        }

        function task_proportion(value, row, index) {
            eval('var rowobj=' + JSON.stringify(row))
            var regStr = '';
            if (rowobj['task_proportion']) {
                regStr = String.format("<span style=\"color:green;\">{0}%</span>", value);
            } else {
                regStr = String.format("<span style=\"color:green;\">{0}%</span>", 0);
            }
            return [regStr].join('');
        }

        url = String.format('{0}?startDate={1}&endDate={2}', "{{ info['show_data_url'] }}", startDate, endDate);
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
                calculable: true,
                toolbox: {
                    show: true,
                    feature: {
                        mark: {show: true},
                        dataView: {show: true, readOnly: false},
                        magicType: {show: true, type: ['line', 'bar', 'tiled']},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                calculable: true,
                dataZoom: [{
                    show: true,
                    realtime: true,
                    start: 0,
                    end: data.data.dataZoom_start
                }, {
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
