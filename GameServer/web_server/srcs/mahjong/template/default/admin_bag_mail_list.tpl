<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<link rel="stylesheet" href="{{info['STATIC_ADMIN_PATH']}}/layer/mobile/need/layer.css" media="all">
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/layerMobile/layer.js?{{RES_VERSION}}"></script>
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
                <input type="text" class=“form-control” placeholder=" 邮件ID" id='eid' name="eid" style="width:270px;height:34px;"/>
            </div>
            <div style='float:left;margin-left:1em;'>
                <input type="text" class=“form-control” placeholder=" 用户ID" id='userId' name="userId" style="width:100px;height:34px;"/>
            </div>
            <div style='float:left;margin-left:1em;' id="enclosureType" id="enclosureType">
                <select class="form-control">
                    <option value=""> 附件类型（全部）</option>
                    <option value="3"> 积分</option>
                    <option value="1"> 钻石</option>
                    <option value="0"> 空</option>
                </select>
            </div>
            <div style='float:left;margin-left:1em;' id="isRead" id="isRead">
                <select class="form-control">
                    <option value=""> 是否已读（全部）</option>
                    <option value="1"> 已读</option>
                    <option value="0"> 未读</option>
                </select>
            </div>
            <div style='float:left;margin-left:1em;' id="isGet" id="isGet">
                <select class="form-control">
                    <option value=""> 附件是否领取（全部）</option>
                    <option value="1"> 是</option>
                    <option value="0"> 否</option>
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
            sortOrder: 'desc',
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
                field: 'send_time',
                title: '发送时间',
                align: 'center',
                valign: 'middle',
                sortable: true
            },{
                field: 'eid',
                title: '邮件ID',
                sortable: true,
                align: 'center',
                valign: 'middle',
            },{
                field: 'title',
                title: '邮件标题',
                sortable: true,
                align: 'center',
                valign: 'middle',
            }, {
                field: 'body',
                title: '邮件内容',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'awardStr',
                title: '邮件附件',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: function (value) {
                    if (value) {
                        return value
                    } else {
                        return '空'
                    }
                },
            }, {
                field: 'enclosureNum',
                title: '附件数量',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: function (value) {
                    if (value) {
                        return value
                    } else {
                        return '空'
                    }
                },
            }, {
                field: 'user',
                title: '收件人ID / 昵称 / 账号',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'read',
                title: '是否已读',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: read,
            }, {
                field: 'is_get',
                title: '附件领取时间',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: function (value) {
                    if (value == '空') {
                        return value
                    } else if (value == '尚未领取') {
                        return '<span class="label label-danger">' + value +'</span>'
                    } else {
                        return '<span class="label label-success">' + value +'</span>'
                    }
                },
            }, {
                field: 'read_time',
                title: '邮件已读时间',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'valid_time',
                title: '邮件有效期<br>（用户邮件列表到期自动删除）',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: function (value) {
                    if (value) {
                        return '<span class="label label-danger">' + value +'</span>'
                    } else {
                        return '<span class="label label-danger">永久</span>'
                    }
                },
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
            var eid = $("#eid").val();
            var userId = $("#userId").val();
            var enclosureType = $('#enclosureType option:selected').val();
            var isRead = $('#isRead option:selected').val();
            var isGet = $('#isGet option:selected').val();
            sendParameter = p;
            sendParameter['startDate'] = startDate;
            sendParameter['endDate'] = endDate;
            sendParameter['eid'] = eid;
            sendParameter['userId'] = userId;
            sendParameter['enclosureType'] = enclosureType;
            sendParameter['isRead'] = isRead;
            sendParameter['isGet'] = isGet;
            return sendParameter;
        }

        function getOp(value, row, index) {
            eval('rowobj=' + JSON.stringify(row))
            var opList = []
            for (var i = 0; i < rowobj['op'].length; ++i) {
                var op = rowobj['op'][i];
                var str = JSON.stringify({eid: rowobj["eid"], send_time: rowobj["send_time"], user: rowobj['user']});
                var cStr = str.replace(/\"/g, "@");
                if (op['txt'] == '删除'){
                    opList.push(String.format("<a href=\"javascript:;\" class=\"btn btn-danger btn-sm\" onclick=\"comfirmDialog(\'{0}\',\'{1}\',\'{2}\')\"> {3} </a> ", op['url'], op['method'], cStr, op['txt']));
                }else{
                     opList.push(String.format("<a href=\"{0}?eid={1}&userId={2}\" class=\"btn btn-primary btn-sm\">{3}</a> ", op['url'], rowobj['eid'], rowobj['user'], op['txt']));
                }
            }
            return opList.join('');
        }

        //获得返回的json 数据
        function responseFun(res) {
            var count = res.length;
            $('.totalTitle').html("邮件总数： " + count)
            var totalTitle = document.getElementsByClassName('totalTitle')[0];
            totalTitle.style.cssText = "background-color:#d9edf7; height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            return res
        }

    }
</script>
%rebase admin_frame_base