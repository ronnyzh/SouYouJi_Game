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
            <button id="btn_add" type="button" class="btn btn-sm btn-danger">房间模式</button>
        </a>
        <a  href="/admin/statistics/game/play/match">
            <button id="btn_add" type="button" class="btn btn-sm btn-primary">比赛场模式</button>
        </a>
        %include original_search_bar
        <table id="total_dataTable" class="table table-bordered table-hover"></table>
        <table id="dataTable" class="table table-bordered table-hover"></table>
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
                    "class": 'count',
                    "colspan": 20
                }],
                [{
                    field: 'num_id',
                    title: '序号',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                },{
                    field: 'game_id',
                    title: '游戏ID',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                },{
                    field: 'game_name',
                    title: '游戏名称',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                }, {
                    field: 'total_num',
                    title: '总场数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                    footerFormatter:function(values){
                       var count = 0 ;
                       for (var val in values)
                            count+=parseInt(values[val].total_num)
                       return colorFormat(count)
                    }
                }, {
                    field: 'total_enroll_num',
                    title: '报名总数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                    footerFormatter:function(values){
                       var count = 0 ;
                       for (var val in values)
                            count+=parseInt(values[val].total_enroll_num)
                       return colorFormat(count)
                    }
                }, {
                    field: 'total_fee',
                    title: '报名总费用',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 1,
                    rowspan: 2,
                    footerFormatter:function(values){
                       var count = 0 ;
                       for (var val in values)
                            count+=parseInt(values[val].total_fee)
                       return colorFormat(count)
                    }
                }, {
                    title: String.format('<span style="color:#d9534f">{0}</span>', '钻石赛'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 4,
                    rowspan: 1,
                }, {
                    title:  String.format('<span style="color:#428bca">{0}</span>', '积分赛'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    colspan: 4,
                    rowspan: 1,
                }],
                [{
                    field: 'roomcard_game_count',
                    title: String.format('<span style="color:#d9534f">{0}</span>', '钻石赛总数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                       var count = 0 ;
                       for (var val in values)
                            count+=parseInt(values[val].roomcard_game_count)
                       return colorFormat(count)
                    }
                },{
                    field: 'total_roomcard_num',
                    title: String.format('<span style="color:#d9534f">{0}</span>', '钻石赛报名数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                       var count = 0 ;
                       for (var val in values)
                            count+=parseInt(values[val].total_roomcard_num)
                       return colorFormat(count)
                    }
                },{
                    field: 'total_roomcard_fee',
                    title: String.format('<span style="color:#d9534f">{0}</span>', '钻石赛报名费'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                       var count = 0 ;
                       for (var val in values)
                            count+=parseInt(values[val].total_roomcard_fee)
                       return colorFormat(count)
                    }
                }, {
                    field: 'total_roomcard_award',
                    title: String.format('<span style="color:#d9534f">{0}</span>', '钻石赛奖励数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                       var count = 0 ;
                       for (var val in values)
                            count+=parseInt(values[val].total_roomcard_award)
                       return colorFormat(count)
                    }
                }, {
                    field: 'point_game_count',
                    title: String.format('<span style="color:#428bca">{0}</span>', '积分赛总数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                       var count = 0 ;
                       for (var val in values)
                            count+=parseInt(values[val].point_game_count)
                       return colorFormat(count)
                    }
                }, {
                    field: 'total_point_num',
                    title: String.format('<span style="color:#428bca">{0}</span>', '积分赛报名数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                       var count = 0 ;
                       for (var val in values)
                            count+=parseInt(values[val].total_point_num)
                       return colorFormat(count)
                    }
                },{
                    field: 'total_point_fee',
                    title: String.format('<span style="color:#428bca">{0}</span>', '积分赛报名费'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                       var count = 0 ;
                       for (var val in values)
                            count+=parseInt(values[val].total_point_fee)
                       return colorFormat(count)
                    }
                }, {
                    field: 'total_point_award',
                    title: String.format('<span style="color:#428bca">{0}</span>', '积分赛奖励数'),
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                    footerFormatter:function(values){
                       var count = 0 ;
                       for (var val in values)
                            count+=parseInt(values[val].total_point_award)
                       return colorFormat(count)
                    }
                }]]
        });

        //定义列操作
        function getSearchP(p) {
            var startDate = $("#pick-date-start").val();
            var endDate = $("#pick-date-end").val();
            var gameId = $("#gameId").val();
            var playId = $("#playId").val();
            var matchId = $("#matchId").val();
            var matchType = $('#matchType option:selected').val();
            var matchState = $('#matchState option:selected').val();
            sendParameter = p;
            sendParameter['startDate'] = startDate;
            sendParameter['endDate'] = endDate;
            sendParameter['gameId'] = gameId;
            sendParameter['playId'] = playId;
            sendParameter['matchId'] = matchId;
            sendParameter['matchType'] = matchType;
            sendParameter['matchState'] = matchState;
            return sendParameter;
        }

        function getOp(value, row, index) {
            eval('rowobj=' + JSON.stringify(row))
            var opList = []
            for (var i = 0; i < rowobj['op'].length; ++i) {
                var op = rowobj['op'][i];
                var str = JSON.stringify({match_number: rowobj['match_number']});
                var cStr = str.replace(/\"/g, "@");
                opList.push(String.format("<a href=\"javascript:;\" class=\"btn btn-primary btn-sm btn-xs\" onclick=\"showAccessDialog(\'{0}\', \'{1}\')\"><i class=\"glyphicon glyphicon-edit\"> {2} </i></a> ", op['url'], op['method'], op['txt']));            }
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

%rebase admin_frame_base
