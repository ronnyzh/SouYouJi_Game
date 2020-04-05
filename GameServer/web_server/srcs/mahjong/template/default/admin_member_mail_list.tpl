<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
    %include admin_frame_header
    <div class="content">
        %include original_search_bar
        <table id="dataTable" class="table table-bordered table-hover"></table>
    </div>
</div>
<script type="text/javascript">
    var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 6);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));

    function initTable() {
        startDate = $("#pick-date-start").val();
        endDate = $("#pick-date-end").val();
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
            exportTypes:[ 'csv', 'txt', 'sql', 'doc', 'excel', 'xlsx', 'pdf'],
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
                title: '邮件有效期<br>（到期自动删除）',
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
                //formatter: getOp
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
            startDate = $("#pick-date-start").val();
            endDate = $("#pick-date-end").val();
            sendParameter = p;
            sendParameter['startDate'] = startDate;
            sendParameter['endDate'] = endDate;
            return sendParameter;
        }

        function getOp(value, row, index) {
            eval('rowobj=' + JSON.stringify(row))
            var opList = []
            for (var i = 0; i < rowobj['op'].length; ++i) {
                var op = rowobj['op'][i];
                var str = JSON.stringify({orderNo: rowobj["orderNo"]});
                var cStr = str.replace(/\"/g, "@");
                if (rowobj['status'] == '1')
                    continue;
                var contentUrl = op['url'];
                opList.push(String.format("<a href=\"#\" class=\"btn btn-primary btn-sm\" onclick=\"comfirmOrderDialog(\'{0}\',\'{1}\',\'{2}\')\"><i class=\"glyphicon glyphicon-edit\"> {3} </i></a> ", contentUrl, op['method'], cStr, op['txt']));
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