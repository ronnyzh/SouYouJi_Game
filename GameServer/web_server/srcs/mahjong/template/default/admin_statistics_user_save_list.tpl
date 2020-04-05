<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/echarts.common.min.js"></script>
<div class="block">
    %include admin_frame_header
    <div class="content">
        %include original_search_bar
        %if info['selfType'] == '0':
        <table id="dataTable_reg" class="table table-bordered table-hover"></table>
        %end
        <table id="dataTable_match_reg" class="table table-bordered table-hover"></table>
        <table id="dataTable_active" class="table table-bordered table-hover"></table>
        <table id="dataTable_match_active" class="table table-bordered table-hover"></table>
    </div>
    <div class='rows' style='margin-bottom:10px;'>
        <div class="panel panel-info" style="height:500px">
            <div class="panel-heading">
                <h3 class="panel-title">[房间模式] 用户注册留存统计</h3>
            </div>
            <div class="panel-body" style='margin-top:10px;'>
                <div id="reg_echart" style="width:100%;height:400px;"></div>
            </div>
        </div>
    </div>
    <div class='rows' style='margin-bottom:10px;'>
        <div class="panel panel-info" style="height:500px">
            <div class="panel-heading">
                <h3 class="panel-title">[房间模式] 用户活跃留存统计</h3>
            </div>
            <div class="panel-body" style='margin-top:10px;'>
                <div id="active_echart" style="width:100%;height:400px;"></div>
            </div>
        </div>
    </div>
</div>
<script type="text/javascript">
    var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 7);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));

    function initTable_reg() {
        var startDate = $("#pick-date-start").val();
        var endDate = $("#pick-date-end").val();
        $('#dataTable_reg').bootstrapTable({
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
                    "halign": "left",
                    "align": "left",
                    "class": 'count_active',
                    "colspan": 18
                }],
                [{
                    field: 'date',
                    title: '统计日期',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    width: 100,
                }, {
                    field: 'reg_count',
                    title: '注册玩家',
                    align: 'center',
                    sortable: true,
                    valign: 'middle'
                }, {
                    field: 'one_save',
                    title: '一日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: one_save,
                }, {
                    field: 'two_save',
                    title: '二日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: two_save,
                }, {
                    field: 'three_save',
                    title: '三日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: three_save,
                }, {
                    field: 'four_save',
                    title: '四日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: four_save,
                }, {
                    field: 'five_save',
                    title: '五日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: five_save,
                }, {
                    field: 'six_save',
                    title: '六日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: six_save,
                }, {
                    field: 'seven_save',
                    title: '七日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: seven_save,
                }, {
                    field: 'fifteen_save',
                    title: '十五日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: fifteen_save,
                }, {
                    field: 'thirty_save',
                    title: '三十日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: thirty_save,
                }]]
        });

        //获得返回的json 数据
        function responseFun(res) {
            var data = res
            $('.count_active').text(String.format("[房间模式] [注册玩家留存率] 当前查询日期：{0} ~ {1}", startDate, endDate));
            var totalTitle = document.getElementsByClassName('count_active')[0];
            totalTitle.style.cssText = "background-color:#d9edf7; height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            return data;
        }
    }
</script>
<script type="text/javascript">
    var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 7);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));

    function initTable_match_reg() {
        var startDate = $("#pick-date-start").val();
        var endDate = $("#pick-date-end").val();
        $('#dataTable_match_reg').bootstrapTable({
            method: 'get',
            url: '{{info["match_listUrl"]}}',
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
                    "halign": "left",
                    "align": "left",
                    "class": 'count_match_reg',
                    "colspan": 18
                }],
                [{
                    field: 'date',
                    title: '统计日期',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    width: 100,
                }, {
                    field: 'reg_count',
                    title: '注册玩家',
                    align: 'center',
                    sortable: true,
                    valign: 'middle'
                }, {
                    field: 'one_save',
                    title: '一日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: one_save,
                }, {
                    field: 'two_save',
                    title: '二日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: two_save,
                }, {
                    field: 'three_save',
                    title: '三日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: three_save,
                }, {
                    field: 'four_save',
                    title: '四日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: four_save,
                }, {
                    field: 'five_save',
                    title: '五日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: five_save,
                }, {
                    field: 'six_save',
                    title: '六日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: six_save,
                }, {
                    field: 'seven_save',
                    title: '七日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: seven_save,
                }, {
                    field: 'fifteen_save',
                    title: '十五日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: fifteen_save,
                }, {
                    field: 'thirty_save',
                    title: '三十日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: thirty_save,
                }]]
        });

        //获得返回的json 数据
        function responseFun(res) {
            var data = res
            $('.count_match_reg').text(String.format("[比赛场模式] [注册玩家留存率] 当前查询日期：{0} ~ {1}", startDate, endDate));
            var totalTitle = document.getElementsByClassName('count_match_reg')[0];
            totalTitle.style.cssText = "background-color:#d9edf7; height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            return data;
        }
    }
</script>
<script>
    function initTable_active() {
        var startDate = $("#pick-date-start").val();
        var endDate = $("#pick-date-end").val();
        $('#dataTable_active').bootstrapTable({
            method: 'get',
            url: '{{info["login_listUrl"]}}',
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
            responseHandler: responseFun_1,
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
                    "halign": "left",
                    "align": "left",
                    "class": 'count_reg',
                    "colspan": 18
                }],
                [{
                    field: 'date',
                    title: '统计日期',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    width: 100,
                }, {
                    field: 'reg_count',
                    title: '活跃玩家',
                    align: 'center',
                    sortable: true,
                    valign: 'middle'
                }, {
                    field: 'one_save',
                    title: '一日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: one_save,
                }, {
                    field: 'two_save',
                    title: '二日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: two_save,
                }, {
                    field: 'three_save',
                    title: '三日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: three_save,
                }, {
                    field: 'four_save',
                    title: '四日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: four_save,
                }, {
                    field: 'five_save',
                    title: '五日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: five_save,
                }, {
                    field: 'six_save',
                    title: '六日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: six_save,
                }, {
                    field: 'seven_save',
                    title: '七日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: seven_save,
                }, {
                    field: 'fifteen_save',
                    title: '十五日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: fifteen_save,
                }, {
                    field: 'thirty_save',
                    title: '三十日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: thirty_save,
                }]]
        });

        function responseFun_1(res) {
            var data = res
            $('.count_reg').text(String.format("[房间模式] [活跃玩家留存率] 当前查询日期：{0} ~ {1}", startDate, endDate));
            var totalTitle = document.getElementsByClassName('count_reg')[0];
            totalTitle.style.cssText = "background-color:#d9edf7; height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            return data;
        }
    }
</script>
<script>
    function initTable_match_active() {
        var startDate = $("#pick-date-start").val();
        var endDate = $("#pick-date-end").val();
        $('#dataTable_match_active').bootstrapTable({
            method: 'get',
            url: '{{info["match_login_listUrl"]}}',
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
            responseHandler: responseFun_1,
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
                    "halign": "left",
                    "align": "left",
                    "class": 'count_match_active',
                    "colspan": 18
                }],
                [{
                    field: 'date',
                    title: '统计日期',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    width: 100,
                }, {
                    field: 'reg_count',
                    title: '活跃玩家',
                    align: 'center',
                    sortable: true,
                    valign: 'middle'
                }, {
                    field: 'one_save',
                    title: '一日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: one_save,
                }, {
                    field: 'two_save',
                    title: '二日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: two_save,
                }, {
                    field: 'three_save',
                    title: '三日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: three_save,
                }, {
                    field: 'four_save',
                    title: '四日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: four_save,
                }, {
                    field: 'five_save',
                    title: '五日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: five_save,
                }, {
                    field: 'six_save',
                    title: '六日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: six_save,
                }, {
                    field: 'seven_save',
                    title: '七日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: seven_save,
                }, {
                    field: 'fifteen_save',
                    title: '十五日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: fifteen_save,
                }, {
                    field: 'thirty_save',
                    title: '三十日后',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    formatter: thirty_save,
                }]]
        });

        function responseFun_1(res) {
            var data = res
            $('.count_match_active').text(String.format("[比赛场模式] [活跃玩家留存率] 当前查询日期：{0} ~ {1}", startDate, endDate));
            var totalTitle = document.getElementsByClassName('count_match_active')[0];
            totalTitle.style.cssText = "background-color:#d9edf7; height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            return data;
        }
    }
</script>
<script>
    //定义列操作
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

    function getSearchP(p) {
        var startDate = $("#pick-date-start").val();
        var endDate = $("#pick-date-end").val();
        sendParameter = p;
        sendParameter['startDate'] = startDate;
        sendParameter['endDate'] = endDate;
        return sendParameter;
    }

    function reg_status(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var regStr = '';
        if (rowobj['reg_proportion']) {
            regStr = String.format("<span style=\"color:green;\">{0}%</span>", value);
        } else {
            regStr = String.format("<span style=\"color:green;\">{0}%</span>", 0);
        }
        return [regStr].join('');
    }

    function one_save(value, row, index, save) {
        eval('var rowobj=' + JSON.stringify(row))
        var saveStr = '';
        if (rowobj['one_save']) {
            var str = rowobj['one_save'].split(' ');
            reg_num = str[0];
            reg_proportion = str[1];
            saveStr = String.format("{0} (<span style=\"color:green;\">{1}</span>)", reg_num, reg_proportion);
        } else {
            saveStr = String.format("<span style=\"color:green;\"></span>");
        }
        return [saveStr].join('');
    }

    function two_save(value, row, index, save) {
        eval('var rowobj=' + JSON.stringify(row))
        var saveStr = '';
        if (rowobj['two_save']) {
            var str = rowobj['two_save'].split(' ');
            reg_num = str[0];
            reg_proportion = str[1];
            saveStr = String.format("{0} (<span style=\"color:green;\">{1}</span>)", reg_num, reg_proportion);
        } else {
            saveStr = String.format("<span style=\"color:green;\"></span>");
        }
        return [saveStr].join('');
    }

    function three_save(value, row, index, save) {
        eval('var rowobj=' + JSON.stringify(row))
        var saveStr = '';
        if (rowobj['three_save']) {
            var str = rowobj['three_save'].split(' ');
            reg_num = str[0];
            reg_proportion = str[1];
            saveStr = String.format("{0} (<span style=\"color:green;\">{1}</span>)", reg_num, reg_proportion);
        } else {
            saveStr = String.format("<span style=\"color:green;\"></span>");
        }
        return [saveStr].join('');
    }

    function four_save(value, row, index, save) {
        eval('var rowobj=' + JSON.stringify(row))
        var saveStr = '';
        if (rowobj['four_save']) {
            var str = rowobj['four_save'].split(' ');
            reg_num = str[0];
            reg_proportion = str[1];
            saveStr = String.format("{0} (<span style=\"color:green;\">{1}</span>)", reg_num, reg_proportion);
        } else {
            saveStr = String.format("<span style=\"color:green;\"></span>");
        }
        return [saveStr].join('');
    }

    function five_save(value, row, index, save) {
        eval('var rowobj=' + JSON.stringify(row))
        var saveStr = '';
        if (rowobj['five_save']) {
            var str = rowobj['five_save'].split(' ');
            reg_num = str[0];
            reg_proportion = str[1];
            saveStr = String.format("{0} (<span style=\"color:green;\">{1}</span>)", reg_num, reg_proportion);
        } else {
            saveStr = String.format("<span style=\"color:green;\"></span>");
        }
        return [saveStr].join('');
    }

    function six_save(value, row, index, save) {
        eval('var rowobj=' + JSON.stringify(row))
        var saveStr = '';
        if (rowobj['six_save']) {
            var str = rowobj['six_save'].split(' ');
            reg_num = str[0];
            reg_proportion = str[1];
            saveStr = String.format("{0} (<span style=\"color:green;\">{1}</span>)", reg_num, reg_proportion);
        } else {
            saveStr = String.format("<span style=\"color:green;\"></span>");
        }
        return [saveStr].join('');
    }

    function seven_save(value, row, index, save) {
        eval('var rowobj=' + JSON.stringify(row))
        var saveStr = '';
        if (rowobj['seven_save']) {
            var str = rowobj['seven_save'].split(' ');
            reg_num = str[0];
            reg_proportion = str[1];
            saveStr = String.format("{0} (<span style=\"color:green;\">{1}</span>)", reg_num, reg_proportion);
        } else {
            saveStr = String.format("<span style=\"color:green;\"></span>");
        }
        return [saveStr].join('');
    }

    function fifteen_save(value, row, index, save) {
        eval('var rowobj=' + JSON.stringify(row))
        var saveStr = '';
        if (rowobj['fifteen_save']) {
            var str = rowobj['fifteen_save'].split(' ');
            reg_num = str[0];
            reg_proportion = str[1];
            saveStr = String.format("{0} (<span style=\"color:green;\">{1}</span>)", reg_num, reg_proportion);
        } else {
            saveStr = String.format("<span style=\"color:green;\"></span>");
        }
        return [saveStr].join('');
    }

    function thirty_save(value, row, index, save) {
        eval('var rowobj=' + JSON.stringify(row))
        var saveStr = '';
        if (rowobj['thirty_save']) {
            var str = rowobj['thirty_save'].split(' ');
            reg_num = str[0];
            reg_proportion = str[1];
            saveStr = String.format("{0} (<span style=\"color:green;\">{1}</span>)", reg_num, reg_proportion);
        } else {
            saveStr = String.format("<span style=\"color:green;\"></span>");
        }
        return [saveStr].join('');
    }
</script>
<script>
    $().ready(function () {
        var startDate = $("#pick-date-start").val();
        var endDate = $("#pick-date-end").val();
        if (initTable_reg && typeof(eval(initTable_reg)) == "function") {
            initTable_reg();
            initTable_active();
            initTable_match_reg();
            initTable_match_active();
            url = String.format('{0}?startDate={1}&endDate={2}&type={3}',"{{ info['regEchartUrl'] }}", startDate, endDate, '0');
            show_graphs('reg_echart', url, startDate, endDate);
            url = String.format('{0}?startDate={1}&endDate={2}&type={3}',"{{ info['regEchartUrl'] }}", startDate, endDate, '1');
            show_graphs('active_echart', url, startDate, endDate);
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
                initTable_reg();
                initTable_active();
                initTable_match_reg();
                initTable_match_active();
                var startDate = $("#pick-date-start").val();
                var endDate = $("#pick-date-end").val();
                url = String.format('{0}?startDate={1}&endDate={2}&type={3}',"{{ info['regEchartUrl'] }}", startDate, endDate, '0');
                show_graphs('reg_echart', url, startDate, endDate);
                url = String.format('{0}?startDate={1}&endDate={2}&type={3}',"{{ info['regEchartUrl'] }}", startDate, endDate, '1');
                show_graphs('active_echart', url, startDate, endDate);
                loadTable = true;
            }
            else {
                $("#dataTable_reg").bootstrapTable('destroy');
                initTable_reg();
                $("#dataTable_active").bootstrapTable('destroy');
                initTable_active();
                $("#dataTable_match_reg").bootstrapTable('destroy');
                initTable_match_reg();
                $("#dataTable_match_active").bootstrapTable('destroy');
                initTable_match_active();
                var startDate = $("#pick-date-start").val();
                var endDate = $("#pick-date-end").val();
                url = String.format('{0}?startDate={1}&endDate={2}&type={3}',"{{ info['regEchartUrl'] }}", startDate, endDate, '0');
                show_graphs('reg_echart', url, startDate, endDate);
                url = String.format('{0}?startDate={1}&endDate={2}&type={3}',"{{ info['regEchartUrl'] }}", startDate, endDate, '1');
                show_graphs('active_echart', url, startDate, endDate);
            }
        });

        function refresh(startDate, endDate) {
            $('#pick-date-start').val(startDate.Format("yyyy-MM-dd"));
            $('#pick-date-end').val(endDate.Format("yyyy-MM-dd"));
            if (!loadTable) {
                initTable_reg();
                initTable_active();
                initTable_match_reg();
                initTable_match_active();
                var startDate = $("#pick-date-start").val();
                var endDate = $("#pick-date-end").val();
                url = String.format('{0}?startDate={1}&endDate={2}&type={3}',"{{ info['regEchartUrl'] }}", startDate, endDate, '0');
                show_graphs('reg_echart', url, startDate, endDate);
                url = String.format('{0}?startDate={1}&endDate={2}&type={3}',"{{ info['regEchartUrl'] }}", startDate, endDate, '1');
                show_graphs('active_echart', url, startDate, endDate);
                loadTable = true;
            }
            else {
                $("#dataTable_reg").bootstrapTable('destroy');
                initTable_reg();
                $("#dataTable_active").bootstrapTable('destroy');
                initTable_active();
                $("#dataTable_match_reg").bootstrapTable('destroy');
                initTable_match_reg();
                $("#dataTable_match_active").bootstrapTable('destroy');
                initTable_match_active();
                var startDate = $("#pick-date-start").val();
                var endDate = $("#pick-date-end").val();
                url = String.format('{0}?startDate={1}&endDate={2}&type={3}',"{{ info['regEchartUrl'] }}", startDate, endDate, '0');
                show_graphs('reg_echart', url, startDate, endDate);
                url = String.format('{0}?startDate={1}&endDate={2}&type={3}',"{{ info['regEchartUrl'] }}", startDate, endDate, '1');
                show_graphs('active_echart', url, startDate, endDate);
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
        resizeWorldMapContainer();
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