<link href="{{info['STATIC_ADMIN_PATH']}}/css/select2.min.css" rel="stylesheet" />
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script src="{{info['STATIC_ADMIN_PATH']}}/js/select2.min.js"></script>
<div class="block">
    %include admin_frame_header
    <div class="content">
    <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
            <div class='col-sm-12'>
                <div style='float:left;'>
                     <div style='float:left;margin-left:0em;' class="input-group date datetime col-md-1 col-xs-1"
                         data-min-view="2" data-date-format="yyyy-mm-dd">
                        <input class="form-control" size="18" type="text" style='width:140px;height:28px;' id='pick-date-start'
                               name="startdate" value="{{lang.INPUT_LABEL_START_DATE_TXT}}" readonly>
                        <span class="input-group-addon btn btn-primary pickdate-btn"><span
                                class="glyphicon pickdate-btn pickdate glyphicon-th"></span>
                    </div>
                    <div style='float:left;margin-left:1em;' class="input-group date datetime col-md-1 col-xs-1"
                         data-min-view="2" data-date-format="yyyy-mm-dd">
                        <input class="form-control" style='width:140px;height:28px;' id='pick-date-end' name="enddate" size="18"
                               type="text" value="{{lang.INPUT_LABEL_END_DATE_TXT}}" readonly>
                        <span class="input-group-addon btn btn-primary pickdate-btn"><span
                                class="pickdate glyphicon pickdate-btn glyphicon-th"></span></span>
                    </div>
                     <div style='float:left;margin-left:1em;'>
                        <select class="form-control"  id="searchId" multiple="multiple" style='width:150px;height:30px;'>
                                    </select>
                        <button id="btn_lastMonth" class='btn btn-sm'>{{lang.INPUT_LABEL_PREV_MONTH}}</button>
                        <button id="btn_thisMonth" class='btn btn-sm'>{{lang.INPUT_LABEL_CURR_MONTH}}</button>
                        <button id="btn_lastWeek" class='btn btn-sm'>{{lang.INPUT_LABEL_PREV_WEEK}}</button>
                        <button id="btn_thisWeek" class='btn btn-sm'>{{lang.INPUT_LABEL_CURR_WEEK}}</button>
                        <button id="btn_yesterday" class='btn btn-sm'>{{lang.INPUT_LABEL_PREV_DAY}}</button>
                        <button id="btn_today" class='btn btn-sm'>{{lang.INPUT_LABEL_CURR_DAY}}</button>
                        <button id="btn_search" v-bind:click="onRefresh()" class='btn btn-primary btn-sm'>
                            {{lang.INPUT_LABEL_QUERY}}
                        </button>
                    </div>
                </div>
            </div>
            </div>
        <table id="dataTable" class="table table-bordered table-hover"></table>
    </div>
</div>
<script type="text/javascript">
    var firstDate = new Date();
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(firstDate.Format("yyyy-MM-dd"));
</script>
<script type="text/javascript">
    $('#btn_search').click(function () {
        $('#dataTable').bootstrapTable('refresh', {"url": '{{info["listUrl"]}}'});
    });

    var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 6);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-start').val(new Date().Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));
    function initTable() {
        $('#dataTable').bootstrapTable({
        method: 'get',
        url: '{{info["listUrl"]}}',
        contentType: "application/json",
        datatype: "json",
        detailView: true,//父子表
        cache: false,
        striped: true,
        toolbar: '#toolbar',
        pagination: true,
        pageSize: 15,
        pageList: '{{PAGE_LIST}}',
        responseHandler: responseFun,
        queryParams: getSearchP,
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
                    halign: "center",
                    align: "left",
                    size: '50',
                    class: 'info',
                    colspan: 9
                }
            ], [{
                field: 'date',
                title: '日期',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'userId',
                title: '用户ID',
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
                field: 'parentAg',
                title: '公会号',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'roomId',
                title: '房间号',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'totalCards',
                title: '总钻石数',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'useCards',
                title: '钻石变更',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: getColorCredit,
                footerFormatter:function(values){
                    var count = 0;
                    for (var val in values)
                        count+=parseInt(values[val].useCards);
                    return colorFormat(count);
              }
            }, {
                field: 'useType',
                title: '钻石变更说明',
                align: 'center',
                valign: 'middle',
                sortable: true
            }]],
                onExpandRow: function (index, row, $detail) {
                console.log(index,row,$detail);
                InitSubTable(index, row, $detail);
            }
    });

    function InitSubTable(index, row, $detail) {
        var roomId = row.roomId;
        var account = row.account;
        var date = row.date;
        var parentAg = row.parentAg;
        var cur_table = $detail.html('<table class="table-bordered table-hover definewidth" style="background-color:#428bca4d;border-color: #428bca4d;border-width: 2px 2px 2px 2px;"></table>').find('table');
        $(cur_table).bootstrapTable({
                url: '{{ info['room_listUrl'] }}',
                method: 'get',
                contentType: "application/json",
                datatype: "json",
                cache: false,
                sortOrder: 'desc',
                sortName: 'regDate',
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
                    field: 'gameid',
                    title: '游戏ID',
                    align: 'center',
                    valign: 'middle'
                },{
                    field: 'gamename',
                    title: '游戏名称',
                    align: 'center',
                    valign: 'middle'
                },{
                    field: 'ownner',
                    title: '房主',
                    align: 'center',
                    valign: 'middle'
                },{
                    field: 'player',
                    title: '玩家',
                    align: 'center',
                    valign: 'middle',
                    formatter: function (values) {
                        playStr = ''
                        for (var val in values){
                            valStr = String.format('{0} ：{1}<br>', val, values[val])
                            playStr = playStr += valStr
                        }
                        return playStr;
                    }
                },{
                    field: 'score',
                    title: '分数',
                    align: 'center',
                    valign: 'middle',
                    formatter: function (values) {
                        playStr = ''
                        for (var val in values){
                            valStr = String.format('{0} ：{1}<br>', val, values[val])
                            playStr = playStr += valStr
                        }
                        return playStr;
                    }
                },{
                    field: 'roomSettings',
                    title: '房间设置',
                    align: 'center',
                    valign: 'middle',
                    formatter: function (values) {
                        playStr = ''
                        for (var val in values){
                            valStr = String.format('{0} ：{1}<br>', val, values[val])
                            playStr = playStr += valStr
                        }
                        return playStr;
                    }
                },{
                    field: 'descs',
                    title: '牌局描述',
                    align: 'center',
                    valign: 'middle',
                    formatter: function (values) {
                        playStr = ''
                        for (var val in values){
                            valStr = String.format('{0} ：{1}<br>', val, values[val])
                            playStr = playStr += valStr
                        }
                        return playStr;
                    }
                },{
                    field: 'startTime',
                    title: '开始时间',
                    align: 'center',
                    valign: 'middle'
                },{
                    field: 'endTime',
                    title: '结束时间',
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
              sendParameter['account'] = account;
              sendParameter['parentAg'] = parentAg;
              sendParameter['date'] = date;
              sendParameter['roomId'] = roomId;
              return sendParameter;
        }
    }

    function getColorCredit(value, row, index) {
        if (parseInt(value) > 0)
            infoStr = String.format("<span style=\"color:red;\">+{0}</span>", value);
        else
            infoStr = String.format("<span style=\"color:green;\">{0}</span>", value);
        return [
            infoStr
        ].join('');
    }

    function getOp(value, row, index) {
        var comfirmUrls = [
            '/admin/member/kick',
            '/admin/member/freeze'
        ];
        eval('rowobj=' + JSON.stringify(row))
        var opList = []
        for (var i = 0; i < rowobj['op'].length; ++i) {
            var op = rowobj['op'][i];
            var str = JSON.stringify({id: rowobj['id']});
            var cStr = str.replace(/\"/g, "@");
            if (comfirmUrls.indexOf(op['url']) >= 0)
                opList.push(String.format("<a href=\"#\" class=\"btn btn-primary btn-xs\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"><i class=\"fa fa-edit\"> {3} </i></a> ", op['url'], op['method'], cStr, op['txt']));
            else
                opList.push(String.format("<a href=\"{0}?id=" + rowobj['id'] + "\" class=\"btn btn-primary btn-xs\" ><i class=\"fa fa-edit\"> {1} </i></a> ", op['url'], op['txt']));
        }
        return opList.join('');
    }


    function getColor(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        statusstr = '<span style="color:#6600FF">' + value + '</span>';

        return [statusstr].join('');
    }

    //定义列操作
    function getSearchP(p) {
        searchId = $("#searchId").val();
        startDate = $("#pick-date-start").val();
        endDate = $("#pick-date-end").val();

        sendParameter = p;

        sendParameter['searchId'] = searchId;
        sendParameter['startDate'] = startDate;
        sendParameter['endDate'] = endDate;

        return sendParameter;
    }

    //获得返回的json 数据
    function responseFun(res) {
        var startDate = $('#pick-date-start').val();
        var endDate = $('#pick-date-end').val();
        var searchId = $("#searchId").val();
        count = res.count;
        img = res.headImgUrl;
        if (searchId){
            $('.info').html("玩家名称：" + name + "&nbsp;  玩家头像：<img src='" + img + "' width='30' height='30' />");
        }else{
            $('.info').html("玩家耗钻数据");
        };
        var totalMoney = document.getElementsByClassName('info')[0];
        totalMoney.style.cssText = "height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
        return res.data
    }
}
</script>
<script>
    $("#searchId").select2({
        allowClear: true,
        closeOnSelect: false,
        language: "zh-CN",
        placeholder: " 请选择用户ID",
        minimumInputLength: 0,
        multiple: false,
        ajax:{
            url: "{{ info['searchUrl'] }}",
            dataType:"json",
            delay:250,
            data:function(params){
                return {
                    name: params.term,
                    page: params.page || 1,
                };
            },
            cache: true,
            processResults: function (res, params) {
                var users = res["data"]["users"];
                var options = [];
                for(var i= 0, len=users.length;i<len;i++){
                    var option = {"id":users[i]["id"], "text":users[i]["name"]};
                    options.push(option);
                }
                return {
                    results: options,
                    pagination: {
                        more:res["data"]["more"]
                    }
                };
            },
            escapeMarkup: function (markup) { return markup; },
        }
    });
</script>
%rebase admin_frame_base

