<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/echarts.common.min.js"></script>
<div class="block">
    %include admin_frame_header
    <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
        <div class='col-sm-12' style='margin-left:-1em;'>
            <div style='float:left;margin-left:1em;'>
                <input type="text" class=“form-control” placeholder=" 游戏ID" id='gameId' name="gameId"
                       style="width:100px;height:34px;"/>
            </div>
            <div style='float:left;margin-left:1em;'>
                <input type="text" class=“form-control” placeholder=" 场次ID" id='playId' name="playId"
                       style="width:100px;height:34px;"/>
            </div>
            <div style='float:left;margin-left:1em;'>
                <input type="text" class=“form-control” placeholder=" 比赛编号" id='matchId' name="matchId"
                       style="width:250px;height:34px;"/>
            </div>
            <div style='float:left;margin-left:1em;'>
                <input type="text" class=“form-control” placeholder=" 用户ID" id='userId' name="userId"
                       style="width:100px;height:34px;"/>
            </div>
            <div style='float:left;margin-left:1em;' id="matchType" id="matchType">
                <select class="form-control">
                    <option value=""> 赛事类型（全部）</option>
                    <option value="3"> 积分</option>
                    <option value="1"> 钻石</option>
                </select>
            </div>
            <div style='float:left;margin-left:1em;' id="matchRank" id="matchRank">
                <select class="form-control">
                    <option value=""> 赛事排名（全部）</option>
                    <option value="1"> 1</option>
                    <option value="2"> 2</option>
                    <option value="3"> 3</option>
                    <option value="4"> 4</option>
                    <option value="5"> 5</option>
                    <option value="6"> 6</option>
                    <option value="7"> 7</option>
                    <option value="8"> 8</option>
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
    <table id="total_dataTable" class="table table-bordered table-hover"></table>
    <table id="dataTable" class="table table-bordered table-hover"></table>
</div>
<script type="text/javascript">
    var firstDate=new Date();
    firstDate.setDate(firstDate.getDate()-6);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));
    function total_initTable() {
        var startDate = $("#pick-date-start").val();
        var endDate = $("#pick-date-end").val();
        $('#total_dataTable').bootstrapTable({
            method: 'get',
            url: '{{ info['total_listUrl'] }}',
            contentType: "application/json",
            datatype: "json",
            cache: false,
            checkboxHeader: true,
            striped: true,
            pagination: true,
            pageSize: 10,
            pageList: [10, 25, 50, 100, 'all'],
            sidePagination: "server",
            minimumCountColumns: 2,
            clickToSelect: true,
            smartDisplay: true,
            queryParamsType: '',
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
                    "class": 'total_count',
                    "colspan": 20
                }],
                [{
                    field: 'match_num',
                    title: '比赛场数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                },{
                    field: 'total_active',
                    title: '活跃人数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                },{
                    field: 'total_enroll',
                    title: '报名人数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                },{
                    field: 'fee',
                    title: '报名费总数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                }, {
                    title: String.format('<span style="color:#d9534f">{0}</span>', "钻石赛"),
                    valign: "middle",
                    align: "center",
                    colspan: 4,
                    rowspan: 1,
                }, {
                    title: String.format('<span style="color:#428bca">{0}</span>', "积分赛"),
                    valign: "middle",
                    align: "center",
                    colspan: 4,
                    rowspan: 1,
                }],
                [{
                    field: 'total_active_roomcard',
                    title: String.format('<span style="color:#d9534f">{0}</span>','钻石赛活跃数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                },{
                    field: 'roomcard_num',
                    title: String.format('<span style="color:#d9534f">{0}</span>','钻石赛报名数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                },{
                    field: 'roomcard_fee',
                    title: String.format('<span style="color:#d9534f">{0}</span>','钻石赛报名费'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                },{
                    field: 'reward_roomcard_fee',
                    title: String.format('<span style="color:#d9534f">{0}</span>','钻石赛奖励数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                },{
                    field: 'total_active_gamepoint',
                    title: String.format('<span style="color:#428bca">{0}</span>', '积分赛活跃人数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                },{
                    field: 'gamePoint_num',
                    title: String.format('<span style="color:#428bca">{0}</span>', '积分赛报名人数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                },{
                    field: 'gamePoint_fee',
                    title: String.format('<span style="color:#428bca">{0}</span>', '积分赛报名费'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                },{
                    field: 'gamePoint_roomcard_fee',
                    title: String.format('<span style="color:#428bca">{0}</span>', '积分赛奖励数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                }]]
        });

        //定义列操作
        function getSearchP(p) {
            var startDate = $("#pick-date-start").val();
            var endDate = $("#pick-date-end").val();
            var gameId = $("#gameId").val();
            var playId = $("#playId").val();
            var matchId = $("#matchId").val();
            var userId = $("#userId").val();
            var matchType = $('#matchType option:selected').val();
            var matchRank = $('#matchRank option:selected').val();
            sendParameter = p;
            sendParameter['startDate'] = startDate;
            sendParameter['endDate'] = endDate;
            sendParameter['gameId'] = gameId;
            sendParameter['playId'] = playId;
            sendParameter['matchId'] = matchId;
            sendParameter['matchType'] = matchType;
            sendParameter['matchRank'] = matchRank;
            sendParameter['userId'] = userId;
            return sendParameter;
        }

        //获得返回的json 数据
        function responseFun(res) {
            $('.total_count').text(String.format("当前查询日期：{0} ~ {1} ，总条数{2}", startDate, endDate, res.count));
            var totalTitle = document.getElementsByClassName('total_count')[0];
            totalTitle.style.cssText = "background-color:#d9edf7; height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            return {
                "rows": res.data,
                "total": res.count
            };
        }
    }
</script>
<script type="text/javascript">
    var firstDate=new Date();
    firstDate.setDate(firstDate.getDate()-6);
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
            detailView: true,//父子表
            cache: false,
            checkboxHeader: true,
            sortOrder: 'desc',
            sortable: true,
            sortName: 'end_time',
            striped: true,
            pagination: true,
            pageSize: 10,
            pageList: [10, 25, 50, 100, 'all'],
            sidePagination: "server",
            minimumCountColumns: 2,
            clickToSelect: true,
            smartDisplay: true,
            queryParamsType: '',
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
                    "colspan": 15
                }],
                [{
                    field: 'num_id',
                    title: '序号',
                    align: 'center',
                    valign: 'middle',
                },{
                    field: 'user_id',
                    title: '用户ID',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                },{
                    field: 'nickname',
                    title: '用户昵称',
                    align: 'center',
                    valign: 'middle',
                },{
                    field: 'account',
                    title: '用户账号',
                    align: 'center',
                    valign: 'middle',
                },{
                    field: 'game_id',
                    title: '游戏ID',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                }, {
                    field: 'match_id',
                    title: '场次ID',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                }, {
                    field: 'match_number',
                    title: '比赛编号',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                }, {
                    field: 'total_award_type',
                    title: '比赛类型',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: function (value) {
                    if (value == '1') {
                        return String.format('<span class="label label-warning">{0}</span>', '钻石')
                    } else {
                        return String.format('<span class="label label-primary">{0}</span>', '积分')
                    }
                },
                }, {
                    field: 'fee',
                    title: '报名费用',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                }, {
                    field: 'rank',
                    title: '比赛排名',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                }, {
                    field: 'score',
                    title: '比赛分数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                }, {
                    field: 'reward_fee',
                    title: '奖励数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                }, {
                    field: 'end_time',
                    title: '时间',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                }]],
                onExpandRow: function (index, row, $detail) {
                console.log(index,row,$detail);
                InitSubTable(index, row, $detail);
                }
        });

        function InitSubTable(index, row, $detail) {
        var match_number = row.match_number;
        var cur_table = $detail.html('<table class="table-bordered table-hover definewidth" style="background-color:#428bca4d;border-color: #428bca4d;border-width: 2px 2px 2px 2px;"></table>').find('table');
        $(cur_table).bootstrapTable({
                url: '{{ info['record_listUrl'] }}',
                method: 'get',
                contentType: "application/json",
                datatype: "json",
                cache: false,
                sortOrder: 'desc',
                sortName: 'rank',
                striped: true,
                checkboxHeader: true,
                pagination: true,
                pageSize: 15,
                pageList: '[10, 15, 25, 50, 100, all]',
                strictSearch: true,
                minimumCountColumns: 5,
                clickToSelect: true,
                smartDisplay: true,
                queryParams:getSearchP,
                columns: [{
                    field: 'total_num',
                    title: '报名总人数',
                    align: 'center',
                    valign: 'middle'
                },{
                    field: 'user_ids',
                    title: '用户ID',
                    align: 'center',
                    valign: 'middle'
                },{
                    field: 'total_fee',
                    title: '报名总费用',
                    align: 'center',
                    valign: 'middle'
                },{
                    field: 'total_award_type',
                    title: '奖励类型',
                    align: 'center',
                    valign: 'middle',
                    formatter: function (value) {
                    if (value == '1') {
                        return String.format('<span class="label label-warning">{0}</span>', '钻石')
                    }else if (value == '3') {
                        return String.format('<span class="label label-primary">{0}</span>', '积分')
                    } else {
                        return '无'
                    }}
                },{
                    field: 'total_award_num',
                    title: '奖励总数',
                    align: 'center',
                    valign: 'middle'
                }],

                //注册加载子表的事件。注意下这里的三个参数！
                onExpandRow: function (index, row, $detail) {
                    console.log(index,row,$detail);
                    InitSubTable(index, row, $detail);
                }

        });
        //定义列操作
        function getSearchP(p){
              sendParameter = p;
              sendParameter['match_number'] = match_number;
              return sendParameter;
        }
    }

        //定义列操作
        function getSearchP(p) {
            var startDate = $("#pick-date-start").val();
            var endDate = $("#pick-date-end").val();
            var gameId = $("#gameId").val();
            var playId = $("#playId").val();
            var matchId = $("#matchId").val();
            var userId = $("#userId").val();
            var matchType = $('#matchType option:selected').val();
            var matchRank = $('#matchRank option:selected').val();
            sendParameter = p;
            sendParameter['startDate'] = startDate;
            sendParameter['endDate'] = endDate;
            sendParameter['gameId'] = gameId;
            sendParameter['playId'] = playId;
            sendParameter['matchId'] = matchId;
            sendParameter['matchType'] = matchType;
            sendParameter['matchRank'] = matchRank;
            sendParameter['userId'] = userId;
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
            $('.count').text(String.format("当前查询日期：{0} ~ {1} ，总条数{2}", startDate, endDate, res.count));
            var totalTitle = document.getElementsByClassName('count')[0];
            totalTitle.style.cssText = "background-color:#d9edf7; height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            return {
                "rows": res.data,
                "total": res.count
            };
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
    }
</script>
<script>
    $().ready(function () {
        if (initTable && typeof(eval(initTable)) == "function") {
            initTable();
            total_initTable();
        }
        var now = new Date();                    //当前日期
        var nowDayOfWeek = now.getDay();         //今天本周的第几天
        if (!nowDayOfWeek)
            nowDayOfWeek = 6
        else
            nowDayOfWeek -= 1
        var nowDay = now.getDate();              //当前日
        var nowMonth = now.getMonth();           //当前月
        var nowYear = now.getFullYear();             //当前年
        var loadTable = true;

        $("#btn_lastMonth").click(function () {
            var firstDate = getLastMonthStartDate();
            var endDate = getLastMonthEndDate();
            refresh(firstDate, endDate);
        });

        $("#btn_thisMonth").click(function () {
            var firstDate = getMonthStartDate();
            var endDate = getMonthEndDate();
            refresh(firstDate, endDate);
        });

        $("#btn_lastWeek").click(function () {
            var firstDate = getLastWeekStartDate();
            var endDate = getLastWeekEndDate();
            refresh(firstDate, endDate);
        });

        $("#btn_thisWeek").click(function () {
            var firstDate = getWeekStartDate();
            var endDate = getWeekEndDate();
            refresh(firstDate, endDate);
        });

        $("#btn_yesterday").click(function () {
            var date = new Date();
            date.setDate(date.getDate() - 1);
            var firstDate = date;
            var endDate = date;
            refresh(firstDate, endDate);
        });

        $("#btn_today").click(function () {
            var firstDate = new Date();
            var endDate = new Date();
            refresh(firstDate, endDate);
        });

        $("#btn_query").click(function () {
            if (!loadTable) {
                initTable();
                total_initTable();
                loadTable = true;
            }
            else {
                $("#dataTable").bootstrapTable('destroy');
                initTable();
                 $("#total_dataTable").bootstrapTable('destroy');
                total_initTable();
            }
        });

        function refresh(startDate, endDate) {
            $('#pick-date-start').val(startDate.Format("yyyy-MM-dd"));
            $('#pick-date-end').val(endDate.Format("yyyy-MM-dd"));
            if (!loadTable) {
                initTable();
                total_initTable();
                loadTable = true;
            }
            else {
                $("#dataTable").bootstrapTable('destroy');
                initTable();
                $("#total_dataTable").bootstrapTable('destroy');
                total_initTable();
            }
        }

        //获得某月的天数
        function getMonthDays(myMonth) {
            var monthStartDate = new Date(nowYear, myMonth, 1);
            var monthEndDate = new Date(nowYear, myMonth + 1, 1);
            var days = (monthEndDate - monthStartDate) / (1000 * 60 * 60 * 24);
            return days;
        }

        //获得本周的开始日期
        function getWeekStartDate() {
            var weekStartDate = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek);
            return weekStartDate;
        }

        //获得本周的结束日期
        function getWeekEndDate() {
            var weekEndDate = new Date(nowYear, nowMonth, nowDay + (6 - nowDayOfWeek));
            return weekEndDate;
        }

        //获得上周的开始日期
        function getLastWeekStartDate() {
            var weekStartDate = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek);
            weekStartDate.setDate(weekStartDate.getDate() - 7);
            return weekStartDate;
        }

        //获得上周的结束日期
        function getLastWeekEndDate() {
            var weekEndDate = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek);
            weekEndDate.setDate(weekEndDate.getDate() - 1);
            return weekEndDate;
        }

        //获得本月的开始日期
        function getMonthStartDate() {
            var monthStartDate = new Date(nowYear, nowMonth, 1);
            return monthStartDate;
        }

        //获得本月的结束日期
        function getMonthEndDate() {
            var monthEndDate = new Date(nowYear, nowMonth, getMonthDays(nowMonth));
            return monthEndDate;
        }

        //获得上月的开始日期
        function getLastMonthStartDate() {
            var monthStartDate = new Date(nowYear, nowMonth - 1, 1);
            return monthStartDate;
        }

        //获得上月的结束日期
        function getLastMonthEndDate() {
            var monthEndDate = new Date(nowYear, nowMonth - 1, getMonthDays(nowMonth - 1));
            return monthEndDate;
        }

    });
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
                legend: {
                    data: data.data.legen
                },
                title: {
                    text: String.format('{0} ~ {1}', startDate, endDate),
                    subtext: '赛事统计'
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
