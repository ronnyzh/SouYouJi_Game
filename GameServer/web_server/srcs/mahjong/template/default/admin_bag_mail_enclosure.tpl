<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<link rel="stylesheet" href="{{info['STATIC_ADMIN_PATH']}}/layer/mobile/need/layer.css" media="all">
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/layerMobile/layer.js?{{RES_VERSION}}"></script>
<script src="{{info['STATIC_ADMIN_PATH']}}/layer/layer.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/echarts.common.min.js"></script>
<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
    %include admin_frame_header
    <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
        <div class='col-sm-12' style='margin-left:-1em;'>
            <div style='float:left;margin-left:1em;'>
                <input type="text" class=“form-control” placeholder=" 用户ID" id='userId' name="userId" style="width:150px;height:34px;"/>
            </div>
            <div style='float:left;margin-left:1em;' id="enclosureType" id="enclosureType">
                <select class="form-control">
                    <option value=""> 附件类型（全部）</option>
                    <option value="积分"> 积分</option>
                    <option value="钻石"> 钻石</option>
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
                <h3 class="panel-title">附件领取统计</h3>
            </div>
            <div class="panel-body" style='margin-top:10px;'>
                <div id="enclosure_echart" style="width:100%;height:400px;"></div>
            </div>
        </div>
    </div>
</div>
<script type="text/javascript">
    var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 6);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-start').val(new Date().Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));

    function initTable() {
        var startDate = $("#pick-date-start").val();
        var endDate = $("#pick-date-end").val();
        $("#dataTable").bootstrapTable({
            url: "{{info['tableUrl']}}",
            contentType: "application/json",
            datatype: "json",
            cache: false,
            checkboxHeader: true,
            striped: true,
            pagination: true,
            pageSize: 10,
            pageList: [24, 48, 100, 'All'],
            minimumCountColumns: 2,
            clickToSelect: true,
            smartDisplay: true,
            sortOrder: 'asc',
            sortName: 'send_time',
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
                 "halign":"center",
                 "align":"center",
                 "class":'totalTitle',
                 "colspan": 25
            }],
            [{
                field: 'time',
                title: '时间',
                align: 'center',
                valign: 'middle',
                sortable: true
            },{
                field: 'userId',
                title: '用户编号',
                sortable: true,
                align: 'center',
                valign: 'middle',
            },{
                field: 'account',
                title: '用户账号',
                sortable: true,
                align: 'center',
                valign: 'middle',
            }, {
                field: 'nickname',
                title: '用户昵称',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'agentId',
                title: '公会',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'roomCard',
                title: '领取前余额',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'enclosure_type',
                title: '邮件附件',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: function (value) {
                if (value == '钻石') {
                        return String.format('<span class="label label-warning">{0}</span>', '钻石')
                } else {
                        return String.format('<span class="label label-primary">{0}</span>', '积分')
                }
                },
            }, {
                field: 'enclosure_Num',
                title: '附件数量',
                align: 'center',
                valign: 'middle',
                sortable: true,
                footerFormatter: function (values) {
                        var count = 0;
                        for (var val in values)
                            count += parseInt(values[val].enclosure_Num);

                        return colorFormat(count)
                    }
            }, {
                field: 'after_card',
                title: '领取后余额',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'dateTime',
                title: '领取时间',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'op',
                title: '操作',
                align: 'center',
                valign: 'middle',
                formatter: getOp
            }]],

            //注册加载子表的事件。注意下这里的三个参数！
            onExpandRow: function (index, row, $detail) {
                console.log(index, row, $detail);
                InitSubTable(index, row, $detail);
            }
        });

        function read(value, row, index) {
            eval('var rowobj=' + JSON.stringify(row))
            var statusstr = '';
            if (rowobj['read'] == '0') {
                statusstr = '<span class="label label-danger">未读</span>';
            } else if (rowobj['read'] == '1') {
                statusstr = '<span class="label label-success">已读</span>';
            }

            return [
                statusstr
            ].join('');
        }

        function getSearchP(p) {
            var startDate = $("#pick-date-start").val();
            var endDate = $("#pick-date-end").val();
            var userId = $("#userId").val();
            var enclosureType = $('#enclosureType option:selected').val();
            sendParameter = p;
            sendParameter['startDate'] = startDate;
            sendParameter['endDate'] = endDate;
            sendParameter['userId'] = userId;
            sendParameter['enclosureType'] = enclosureType;
            return sendParameter;
        }

        function getOp(value, row, index) {
            eval('rowobj=' + JSON.stringify(row))
            var opList = []
            for (var i = 0; i < rowobj['op'].length; ++i) {
                var op = rowobj['op'][i];
                var str = JSON.stringify({eid: rowobj['eid'], userId: rowobj['userId']});
                var cStr = str.replace(/\"/g, "@");
                btn_type = 'primary';
                txt = '查看';
                opList.push(String.format("<a href=\"javascript:;\" class=\"btn btn-{5} btn-sm btn-xs\" onclick=\"showAccessDialog(\'{0}\', \'{1}\', \'{2}\', \'{3}\')\"><i class=\"glyphicon glyphicon-edit\"> {4} </i></a> ", op['url'], op['method'], rowobj['eid'], rowobj['userId'], txt, btn_type));
            }
            return opList.join('');
        }

        //获得返回的json 数据
        function responseFun(res) {
            $('.totalTitle').html("邮件总数： " + res.count)
            var totalTitle = document.getElementsByClassName('totalTitle')[0];
            totalTitle.style.cssText = "background-color:#d9edf7; height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            return res
        }

        url = String.format('{0}?startDate={1}&endDate={2}',"{{ info['enclosureEchartUrl'] }}", startDate, endDate);
        show_graphs('enclosure_echart', url, startDate, endDate);
    }
</script>
<script>
    function showAccessDialog(url, method, eid, userId) {
            layer.open({
                type: 2,
                title: '邮件查看',
                shadeClose: true,
                shade: 0.5,
                area: ['70%', '70%'],
                content: String.format('{0}?eid={1}&userId={2}', url, eid, userId),
            });
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
                    subtext: '附件领取统计'
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