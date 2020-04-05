<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/echarts.common.min.js"></script>
<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
    %include admin_frame_header
    <div class="content">
        <a  href="/admin/statistics/game/play" style='color:#FFF;text-decoration:none;'>
            <button id="btn_add" type="button" class="btn btn-sm btn-primary">房间模式</button>
        </a>
        <a  href="/admin/statistics/game/play/match">
            <button id="btn_add" type="button" class="btn btn-sm btn-danger">比赛场模式</button>
        </a>
        %include original_search_bar
        <table id="dataTable" class="table table-bordered table-hover"></table>
    </div>
</div>
<div class='rows' style='margin-bottom:10px;'>
        <div class="panel panel-info" style="height:500px">
            <div class="panel-heading">
                <h3 class="panel-title">游戏玩法统计</h3>
            </div>
            <div class="panel-body" style='margin-top:10px;'>
                <div id="gamePlay" style="width:100%;height:400px;"></div>
            </div>
        </div>
</div>
<div class='rows' style='margin-bottom:10px;'>
        <div class="panel panel-info" style="height:50px">
            <div class="panel-heading">
                <h3 class="panel-title">各游戏玩法统计</h3>
            </div>
            <div class="panel-body" style='margin-top:10px;'>
                <div id="everyGamePlay" style="width:100%;height:400px;"></div>
            </div>
        </div>
</div>

<!-- 初始化搜索栏的日期 -->
<script type="text/javascript">
    var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 6);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));
</script>

<script type="text/javascript">
    function initTable() {
        var startDate = $("#pick-date-start").val();
        var endDate = $("#pick-date-end").val();
        $("#dataTable").bootstrapTable({
            ajax: function (request) {
                $.ajax({
                    type: "GET",
                    url: '{{ info['columnsArrayUrl'] }}' + '?startDate=' + startDate + '&endDate=' + endDate,
                    contentType: "application/json;charset=utf-8",
                    dataType: "json",
                    json: 'callback',
                    success: function (json) {
                        var oneColumnsArray = [];
                        oneColumnsArray.push(
                            {
                                field: 'gameId',
                                title: '游戏ID',
                                valign: "middle",
                                align: "center",
                            });
                        oneColumnsArray.push(
                            {
                                field: 'gameName',
                                title: '游戏名称',
                                valign: "middle",
                                align: "center",
                            });
                        for (var i = 0; i < (Object.keys(json.data)).length; i++) {
                            var property = (Object.keys(json.data[i]));
                            oneColumnsArray.push({
                                title: String.format("<span>{0}</span>", property),
                                field: property,
                                align: 'center',
                                valign: 'middle',
                                sortable: true,
                            });
                        };
                        oneColumnsArray.push({
                            title: "操作",
                            field: "op",
                            align: 'center',
                            valign: 'middle',
                        });
                        $('#dataTable').bootstrapTable('destroy').bootstrapTable({
                            url: '{{ info['listUrl'] }}',
                            toolbar: '#toolbar',
                            singleSelect: true,
                            clickToSelect: true,
                            pageSize: 15,
                            pageNumber: 1,
                            pageList: "[10, 25, 50, 100, All]",
                            pagination: true,
                            queryParams: getSearchP,
                            responseHandler: responseFun,
                            columns: oneColumnsArray,
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
                            onExpandRow: function (index, row, $detail) {
                                InitSubTable(index, row, $detail);
                            }
                        });

                        function getOp(value, row, index) {
                            eval('rowobj=' + JSON.stringify(row))
                            var opList = []
                            for (var i = 0; i < rowobj['op'].length; ++i) {
                                var op = rowobj['op'][i];
                                var str = JSON.stringify({hour: rowobj["hour"]});
                                var cStr = str.replace(/\"/g, "@");
                                var contentUrl = op['url'];
                                if (contentUrl.match("graphs")) {
                                    opList.push(String.format("<a href=\"javascript:;\" class=\"btn btn-primary btn-sm\" onclick=\"showGraps(\'{0}\',\'{1}\',\'{2}\')\"> {3}</a> ", contentUrl, op['method'], cStr, op['txt']));
                                }
                                else {
                                    opList.push(String.format("<a href=\"javascript:;\" class=\"btn btn-success btn-sm\" onclick=\"showGraps(\'{0}\',\'{1}\',\'{2}\')\"> {3}</a> ", contentUrl, op['method'], cStr, op['txt']));
                                }
                            }
                            return opList.join('');
                        }

                        function getSearchP(p) {
                            var startDate = $("#pick-date-start").val();
                            var endDate = $("#pick-date-end").val();
                            sendParameter = p;
                            sendParameter['startDate'] = startDate;
                            sendParameter['endDate'] = endDate;
                            return sendParameter;
                        }

                        function responseFun(res) {
                            var data = res;
                            return data;
                        }
                    },
                });
            }
        });
        url = String.format('{0}?startDate={1}&endDate={2}',"{{ info['AllPlayGameurl'] }}", startDate, endDate);
        show_graphs('gamePlay', url, startDate, endDate);

        url = String.format('{0}?startDate={1}&endDate={2}',"{{ info['EveryPlayGameurl'] }}", startDate, endDate);
        show_graphs('everyGamePlay', url, startDate, endDate);
    };
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
                    subtext: '游戏统计'
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
