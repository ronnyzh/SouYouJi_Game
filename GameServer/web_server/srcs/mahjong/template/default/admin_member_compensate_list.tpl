<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/echarts.common.min.js"></script>
<div class="block">
    %include admin_frame_header
    <div class="content">
        %include original_search_bar
        <table id="dataTable" class="table table-bordered table-hover"></table>
        <table id="dataTable_1" class="table table-bordered table-hover"></table>
    </div>
</div>
<script type="text/javascript">
    var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 6);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-start').val(new Date().Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));
</script>
<script type="text/javascript">
    function initTable() {
    $("#dataTable").bootstrapTable({
        url: '{{info["listUrl"]}}',
        method: 'get',
        //sidePagination: "server",
        pagination: true,
        pageSize: 15,
        toolbar: '#toolbar',
        sortOrder: 'desc',
        striped: true,
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
            fileName: '会员增减钻石记录',
        },
        sortName: 'regDate',
        sorttable: true,
        responseHandler: responseFunc,
        queryParams: getSearchP,
        pageList: '[10, 15, 25, 50, 100, all]',
        columns:[
        [{
            halign: "center",
            font: 15,
            align: "left",
            class: "totalTitle",
            colspan: 17
        }],
        [{
            field: 'time',
            title: '时间',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'userId',
            title: '用户编号',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'account',
            title: '用户账号',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'nickname',
            title: '用户昵称',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'agentId',
            title: '公会',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'roomcard',
            title: '增减前钻石数',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'card',
            title: '增减钻石数',
            align: 'center',
            valign: 'middle',
            sortable: true,
            formatter: card
        }, {
            field: 'type',
            title: '增减类型',
            align: 'center',
            valign: 'middle',
            sortable: true,
            formatter: card_type
        }, {
            field: 'after_card',
            title: '增减后钻石数',
            align: 'center',
            valign: 'middle',
            sortable: true,
            formatter: after_card
        }, {
            field: 'note',
            title: '备注信息',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'dateTime',
            title: '操作时间',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }]],
        //注册加载子表的事件。注意下这里的三个参数！
        onExpandRow: function (index, row, $detail) {
            console.log(index, row, $detail);
            InitSubTable(index, row, $detail);
        }
    });

    function responseFunc(res) {
        var data = res.data;
        var count = res.count;
        $('.totalTitle').html("会员增减钻石记录总数 ：" + count)
        var totalTitle = document.getElementsByClassName('totalTitle')[0];
        totalTitle.style.cssText = "background-color:#d9edf7;height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
        return data;
    }

    //定义列操作
    function getSearchP(p) {
          startDate = $("#pick-date-start").val();
          endDate   = $("#pick-date-end").val();
          sendParameter = p;
          sendParameter['startDate'] = startDate;
          sendParameter['endDate']  = endDate;
          return sendParameter;
    }

    function card_type(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (rowobj['card'].indexOf('-') == '0') {
            statusstr = '<span class="label label-danger">减少</span>';
        }else{
            statusstr = '<span class="label label-success">增加</span>';
        }

        return [statusstr].join('');
    }

    function card(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (rowobj['card'].indexOf('-') == '-1') {
            statusstr = String.format("<span style=\"color:green;\">+{0}</span>", value);
        }else{
            statusstr = String.format("<span style=\"color:red;\">{0}</span>", value);
        }

        return [statusstr].join('');
    }

    function after_card(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (rowobj['card'].indexOf('-') == '-1') {
            statusstr = String.format("<span style=\"color:green;\">{0}</span>", value);
        }else{
            statusstr = String.format("<span style=\"color:red;\">{0}</span>", value);
        }

        return [statusstr].join('');
    }
    }
</script>
<script type="text/javascript">
    function initTable_1() {
    $("#dataTable_1").bootstrapTable({
        url: '{{info["maillistUrl"]}}',
        method: 'get',
        pagination: true,
        pageSize: 15,
        toolbar: '#toolbar',
        sortOrder: 'desc',
        striped: true,
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
            fileName: '会员增减积分记录',
        },
        sortName: 'regDate',
        sorttable: true,
        responseHandler: responseFun_1,
        queryParams: getSearchP,
        pageList: '[10, 15, 25, 50, 100, all]',
        columns:[
        [{
            halign: "center",
            font: 15,
            align: "left",
            class: "totalTitle_1",
            colspan: 17
        }],
        [{
            field: 'time',
            title: '时间',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'userId',
            title: '用户编号',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'account',
            title: '用户账号',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'nickname',
            title: '用户昵称',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'agentId',
            title: '公会',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'roomcard',
            title: '增减前积分数',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'card',
            title: '增减积分数',
            align: 'center',
            valign: 'middle',
            sortable: true,
            formatter: card
        }, {
            field: 'type',
            title: '补偿类型',
            align: 'center',
            valign: 'middle',
            sortable: true,
            formatter: card_type
        }, {
            field: 'after_card',
            title: '增减后积分数',
            align: 'center',
            valign: 'middle',
            sortable: true,
            formatter: after_card
        }, {
            field: 'note',
            title: '备注信息',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'dateTime',
            title: '操作时间',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }]],
        //注册加载子表的事件。注意下这里的三个参数！
        onExpandRow: function (index, row, $detail) {
            console.log(index, row, $detail);
            InitSubTable(index, row, $detail);
        }
    });
    function responseFun_1(res) {
        data = res.data;
        count = res.count;
        //实时刷
        $('.totalTitle_1').html("会员增减积分记录总数 ：" + count)
        var totalTitle = document.getElementsByClassName('totalTitle_1')[0];
        totalTitle.style.cssText = "background-color:#d9edf7;height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
        return data;
    }

    //定义列操作
    function getSearchP(p) {
          startDate = $("#pick-date-start").val();
          endDate   = $("#pick-date-end").val();
          sendParameter = p;
          sendParameter['startDate'] = startDate;
          sendParameter['endDate']  = endDate;
          return sendParameter;
    }

    function card_type(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (rowobj['card'].indexOf('-') == '0') {
            statusstr = '<span class="label label-danger">减少</span>';
        }else{
            statusstr = '<span class="label label-success">增加</span>';
        }

        return [statusstr].join('');
    }

    function enclosure_type(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (rowobj['enclosure_type'] == '积分') {
            statusstr = '<span class="label label-danger">' + rowobj['enclosure_type'] +'</span>';
        }else{
            statusstr = '<span class="label label-success">' + rowobj['enclosure_type'] + '</span>';
        }

        return [statusstr].join('');
    }

    function card(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (rowobj['card'].indexOf('-') == '-1') {
            statusstr = String.format("<span style=\"color:green;\">+{0}</span>", value);
        }else{
            statusstr = String.format("<span style=\"color:red;\">{0}</span>", value);
        }

        return [statusstr].join('');
    }

    function after_card(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (rowobj['card'].indexOf('-') == '-1') {
            statusstr = String.format("<span style=\"color:green;\">{0}</span>", value);
        }else{
            statusstr = String.format("<span style=\"color:red;\">{0}</span>", value);
        }

        return [statusstr].join('');
    }
    }
</script>
<script>
    String.format = function () {
        if (arguments.length == 0) {
            return null;
        }
        var str = arguments[0];
        for (var i = 1; i < arguments.length; i++) {
            var re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
            str = str.replace(re, arguments[i]);
        }
        return str;
    }
</script>
<script>
    $().ready(function () {
        if (initTable && typeof(eval(initTable)) == "function") {
            initTable();
            initTable_1()
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
                loadTable = true;
            }
            else {
                $("#dataTable").bootstrapTable('destroy');
                // $("#dataTable").bootstrapTable('refresh');
                initTable();
            }
        });

        function refresh(startDate, endDate) {
            $('#pick-date-start').val(startDate.Format("yyyy-MM-dd"));
            $('#pick-date-end').val(endDate.Format("yyyy-MM-dd"));
            if (!loadTable) {
                initTable();
                initTable_1();
                loadTable = true;
            }
            else {
                $("#dataTable").bootstrapTable('destroy');
                initTable();
                $("#dataTable_1").bootstrapTable('destroy');
                initTable_1();
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
%rebase admin_frame_base
