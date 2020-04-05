<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
    %include admin_frame_header
    %if info.get('agentId') == '1':
    <div class="col-lg-12">
        <div class="content" id="notice_create_app" style="float:left;width:100%;position:relative;top:2.1em">
            <form class='form-horizontal group-border-dashed' action="{{ info['gameInfoUrl'] }}" method='POST' id='noticeForm'
                  onSubmit='return false'>
                <table class='table config-table  table-bordered table-hover'>
                    <tr>
                        <td class='table-title'>客服微信</td>
                        <td colspan="5">
                            <input type="text" style='width:100%;float:left' id="server_WeChat" name="server_WeChat"
                                   class="form-control"  value="{{ customerInfo.get('wechat', '') }}"
                                   placeholder="客服微信">
                        </td>
                    </tr>
                    <tr>
                        <td class='table-title'>客服QQ</td>
                        <td colspan="5">
                            <input type="text" style='width:100%;float:left' id="server_QQ" name="server_QQ"
                                   class="form-control"  value="{{ customerInfo.get('qq', '') }}"
                                   placeholder="客服QQ">
                        </td>
                    </tr>
                    <tr>
                        <td class='table-title'>客服邮箱</td>
                        <td colspan="5">
                            <input type="text" style='width:100%;float:left' id="server_Email" name="server_Email"
                                   class="form-control"  value="{{ customerInfo.get('email', '') }}"
                                   placeholder="客服邮箱">
                        </td>
                    </tr>
                    <tr>
                        <td class='table-title'>全国热线</td>
                        <td colspan="5">
                            <input type="text" style='width:100%;float:left' id="server_phone" name="server_phone"
                                   class="form-control"  value="{{ customerInfo.get('phone', '') }}"
                                   placeholder="全国热线">
                        </td>
                    </tr>
                </table>
                <div class="modal-footer" style="text-align:right">
                    <button type="submit" class="btn btn-primary btn-sm">{{lang.BTN_SUBMIT_TXT}}</button>
                </div>
            </form>
        </div>
    </div>
    <div style='clear:both; margin-bottom: 0px;'></div>
    <hr>
    %end
    <div class="col-lg-12">
        <div class="content">
            <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
                <a href="{{info['createUrl']}}" style='color:#FFF;text-decoration:none;'>
                    <button id="btn_add" type="button" class="btn btn-sm btn-primary" style='margin-left: 0em;'>
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
        pageList: [15, 50, 100, 'All'],
        showColumns: true,
        sortOrder: "desc",
        sortName: 'status',
        minimumCountColumns: 2,
        clickToSelect: true,
        search: true,
        showRefresh: true,
        showColumns: true,
        showToggle: true,
        showExport:true,
        showFooter: true,
        cardView: false,
        responseHandler: responseFun,
        queryParams: getSearchP,                     //是否启用排序
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
            },{
                field: 'time',
                title: '发布时间',
                align: 'center',
                valign: 'middle'
            }, {
                field: 'groupId',
                title: '发布人公会号',
                align: 'center',
                valign: 'middle'
            }, {
                field: 'validDate',
                title: '有效天数',
                align: 'center',
                valign: 'middle',
                formatter: validDate
            }, {
                field: 'messageType',
                title: '消息类型',
                align: 'center',
                valign: 'middle',
                formatter: msgType
            }, {
                field: 'title',
                title: '消息标题',
                align: 'center',
                valign: 'middle'
            }, {
                field: 'content',
                title: '消息内容',
                align: 'center',
                valign: 'middle'
            }, {
                field: 'status',
                title: '消息状态',
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

    function validDate(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (rowobj['validDate'] == '0') {
            statusstr = '<span class="label label-primary">永久</span>';
        } else if (rowobj['validDate'] == '7') {
            statusstr = '<span class="label label-success">七天</span>';
        } else if (rowobj['validDate'] == '30') {
            statusstr = '<span class="label label-info">三十天</span>';
        }
        return [statusstr].join('');
    }

    function status(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (rowobj['status'] == '0') {
            statusstr = '<span class="label label-danger">未推送</span>';
        } else if (rowobj['status'] == '1') {
            statusstr = '<span class="label label-success">推送中</span>';
        }
        return [
            statusstr
        ].join('');
    }

    function msgType(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (rowobj['messageType'] == '0') {
            statusstr = '<span class="label label-primary">系统消息</span>';
        } else if (rowobj['messageType'] == '1') {
            statusstr = '<span class="label label-success">活动信息</span>';
        } else {
            statusstr = '<span class="label label-warning">邮件</span>';
        }
        return [
            statusstr
        ].join('');
    }

    function getOp(value, row, index) {
        var showComfirUrl = [
            '/admin/notice/push/HALL',
            '/admin/notice/push/FISH',
            '/admin/notice/del',
        ];
        eval('rowobj=' + JSON.stringify(row));
        var opList = []
        for (var i = 0; i < rowobj['op'].length; ++i) {
            var op = rowobj['op'][i];
            var str = JSON.stringify({id: rowobj['id']});
            var cStr = str.replace(/\"/g, "@");
            var param = rowobj['id'];
            if (showComfirUrl.indexOf(op['url']) > -1) {
                if (op['txt'] == '取消推送'){
                   opList.push(String.format("<a href=\"javascript:;\" class=\"btn btn-danger btn-sm\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"><i class=\"glyphicon glyphicon-hand-up\"> {3}</i></a> ", op['url'], op['method'], cStr, op['txt']));
                }else{
                    opList.push(String.format("<a href=\"javascript:;\" class=\"btn btn-primary btn-sm\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"><i class=\"glyphicon glyphicon-hand-up\"> {3}</i></a> ", op['url'], op['method'], cStr, op['txt']));
                }
            } else {
                opList.push(String.format("<a href=\"{0}?noticeId={1}\" class=\"btn btn-primary btn-sm\"><i class=\"glyphicon glyphicon-edit\"> {2}</i></a> ", op['url'], param, op['txt']));
            }
        }
        return opList.join('');
    }

    //前台查询参数
    function getSearchP(p) {
        startDate = $("#pick-date-start").val();
        endDate = $("#pick-date-end").val();
        sendParameter = p;
        sendParameter['startDate'] = startDate;
        sendParameter['endDate'] = endDate;
        return sendParameter;
    }

    //获得返回的json 数据
    function responseFun(res) {
        var data = res.data;
        var count = res.count;
        //实时刷

        $('.totalTitle').html("公告总数： " + count)
        var totalTitle = document.getElementsByClassName('totalTitle')[0];
        totalTitle.style.cssText = "background-color:#d9edf7; height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
        return data;
    }

    function responseError(status) {
        location.reload();
    }

    function _settingBatchDel() {
        var noticIds = $.map($('#dataTable').bootstrapTable('getSelections'), function (row) {
            return row.id;
        });

        if (!noticIds.length) {    //如果没选择直接return
            return;
        }

        var remoteUrl = "{{info['batchDelUrl']}}",
            method = "POST",
            jsonStr = {'noticIds': noticIds.join(',')}

        formAjax(remoteUrl, method, jsonStr, '正在执行...,');
    }
</script>
<script>
    $('#noticeForm').submit(function(){
          formAjax($(this).attr("action"), $(this).attr("method"), $(this).serialize(),'正在提交...');
    });
</script>
%rebase admin_frame_base
