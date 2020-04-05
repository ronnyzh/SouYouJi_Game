<div class="block">
    %include admin_frame_header
    <div class="content">
        <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
            <a href="{{info['createUrl']}}" style='color:#FFF;text-decoration:none;'>
                <button id="btn_add" type="button" class="btn btn-sm btn-primary">
                    <i class="glyphicon glyphicon-plus"> {{info['addTitle']}} </i>
                </button>
            </a>
            <a href="javascript:;" style='color:#FFF;text-decoration:none;'>
                <button id="btn_add" onclick="_settingBatchDel();" type="button" class="btn btn-sm btn-danger">
                    <i class="glyphicon glyphicon-plus"> 批量清除 </i>
                </button>
            </a>
        </div>
        <table id="dataTable" class="table table-bordered table-hover"></table>
    </div>
</div>

<script type="text/javascript">

    var startDate = $("#pick-date-start").val();
    var endDate = $("#pick-date-end").val();
    $('#dataTable').bootstrapTable({
        method: 'get',
        url: '{{info["tableUrl"]}}',
        contentType: "application/json",
        datatype: "json",
        cache: true,
        checkboxHeader: true,
        striped: true,
        pagination: true,
        pageSize: 15,
        pageList: '{{PAGE_LIST}}',
        minimumCountColumns: 2,
        clickToSelect: true,
        search: true,
        showHeader: true,
        showFooter: true,
        showRefresh: true,
        showColumns: true,
        showToggle: true,
        showExport:true,
        showFullscreen: true,
        cardView: false,
        responseHandler: responseFun,
        queryParams: getSearchP,
        exportDataType: 'all',
        exportTypes:[ 'csv', 'txt', 'sql', 'doc', 'excel', 'xlsx', 'pdf'],
        exportOptions:{
            fileName: '{{ info["title"] }}',
        },
        columns: [
            [{
                halign: "center",
                font: 15,
                align: "left",
                class: "totalTitle",
                colspan: 17
            }],
            [{
                checkbox: true
            }, {
                field: 'create_date',
                title: '创建时间',
                align: 'center',
                valign: 'middle'
            }, {
                field: 'parent_ag',
                title: '创建公会',
                align: 'center',
                valign: 'middle'
            }, {
                field: 'start_date',
                title: '起始时间',
                align: 'center',
                valign: 'middle'
            }, {
                field: 'end_date',
                title: '结束时间',
                align: 'center',
                valign: 'middle'
            }, {
                field: 'content',
                title: '内容',
                align: 'center',
                valign: 'middle'
            }, {
                field: 'per_sec',
                title: '间隔/s',
                align: 'center',
                valign: 'middle'
            }, {
                field: 'broad_type',
                title: '所属类型',
                align: 'center',
                valign: 'middle',
                formatter: getType
            }, {
                field: 'status',
                title: '当前状态',
                align: 'center',
                valign: 'middle',
                formatter: status
            }, {
                field: 'op',
                title: '操作',
                align: 'center',
                valign: 'middle',
                formatter: getOp
            }]]
    });


    function status(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (rowobj['status'] == '0') {
            statusstr = '<span class="label label-warning">预推送</span>';
        } else if (rowobj['status'] == '1') {
            statusstr = '<span class="label label-success">推送中</span>';
        } else if (rowobj['status'] == '2') {
            statusstr = '<span class="label label-danger">已结束</span>';
        }
        return [
            statusstr
        ].join('');
    }

    function getType(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (rowobj['broad_type'] == '0') {
            statusstr = '<span class="label label-success">全服维护广播</span>';
        } else if (rowobj['broad_type'] == '1') {
            statusstr = '<span class="label label-primary">全服循环广播</span>';
        } else if (rowobj['broad_type'] == '2') {
            statusstr = '<span class="label label-success">地区维护广播</span>';
        } else {
            statusstr = '<span class="label label-success">地区循环广播</span>';
        }
        return [
            statusstr
        ].join('');
    }

    function getOp(value, row, index) {
        var comfirUrl = [
            '/admin/game/broadcast/batch_del'
        ];
        eval('rowobj=' + JSON.stringify(row))
        var opList = []
        for (var i = 0; i < rowobj['op'].length; ++i) {
            var op = rowobj['op'][i];
            var str = JSON.stringify({broadIds: rowobj['broad_id'], broad_belone: "{{info['broad_belone']}}"});
            var cStr = str.replace(/\"/g, "@");
            var param = rowobj['id'];
            if (comfirUrl.indexOf(op['url']) >= 0)
                opList.push(String.format("<a href=\"javascript:;\" class=\"btn btn-danger btn-sm\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\',\'清除后广播将无法还原，是否继续？\')\"><i class=\"glyphicon glyphicon-trash\"> {3} </i></a> ", op['url'], op['method'], cStr, op['txt']));
            else
                opList.push(String.format("<a href=\"{0}?id={1}\" class=\"btn btn-primary btn-sm\"><i class=\"glyphicon glyphicon-edit\"> {2}</i></a> ", op['url'], param, op['txt']));
        }
        return opList.join('');
    }

    //前台查询参数
    function getSearchP(p) {
        // account = $("#account").val();
        // member_level = $('#member_level').val();
        // member_status = $("#member_status").val();
        // userId = $("#userId").val();
        startDate = $("#pick-date-start").val();
        endDate = $("#pick-date-end").val();

        sendParameter = p;
        sendParameter['startDate'] = startDate;
        sendParameter['endDate'] = endDate;

        return sendParameter;
    }

    function _settingBatchDel() {
        var broadIds = $.map($('#dataTable').bootstrapTable('getSelections'), function (row) {
            return row.broad_id;
        });

        if (!broadIds.length) {    //如果没选择直接return
            console.log('---------------had not selected.. return');
            return;
        }

        var remoteUrl = "{{info['batchDelUrl']}}",
            method = "POST",
            jsonStr = {'broadIds': broadIds.join(','), 'broad_belone': "{{info['broad_belone']}}"}

        console.log('----------------select broadIds[' + broadIds + ']');
        formAjax(remoteUrl, method, jsonStr, '正在执行...,');
    }

    //获得返回的json 数据
    function responseFun(res) {

        data = res.data;
        count = res.count;
        //实时刷
        $('.totalTitle').html("公告总数： " + count)
        var totalTitle = document.getElementsByClassName('totalTitle')[0];
        totalTitle.style.cssText = "background-color:#d9edf7; height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
        return data;
    }

    function responseError(status) {
        location.reload();
    }
</script>
%rebase admin_frame_base
