<link rel="stylesheet" href="{{info['STATIC_ADMIN_PATH']}}/layer/mobile/need/layer.css" media="all">
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/layerMobile/layer.js?{{RES_VERSION}}"></script>
<script src="{{info['STATIC_ADMIN_PATH']}}/layer/layer.js"></script>
<div class="block">
    %include admin_frame_header
    <div class="content" style="float:left;width:100%;position:relative;top:2.6em">
        <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
            <div class='col-sm-12' style='margin-left:-1em;'>
                <div style='float:left;margin-left:1em;'>
                <div class='clearfix'></div>
            </div>
            </div>
        </div>
        <!--
        <div class="table-toolbar" style="float:right;border-radius:5px;width:100%;height:50px;position:relative;">
            <div class='col-sm-12'>
                <div style='float:left;'>
                    <div style='float:left;margin-left:0em;'>
                        <input type="text" id="searchId" placeholder=" 权限查找" name="id" value=""
                               style='width:200px;height:30px;'/>
                        <button id="btn_search" v-bind:click="onRefresh()" class='btn btn-primary btn-sm'>
                            {{lang.INPUT_LABEL_QUERY}}
                        </button>
                    </div>
                </div>
            </div>
        </div>
        -->
        <div style='clear:both'></div>
        <table id="agentTable" class="table table-bordered table-hover"></table>
    </div>
</div>
<script type="text/javascript">
    $("#agentTable").bootstrapTable({
        url: '{{ info.get("listUrl") }}',
        method: 'get',
        detailView: false, //父子表
        pagination: true,
        pageSize: 15,
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
            fileName: '{{ info["title"] }}',
        },
        toolbar: '#toolbar',
        sortOrder: 'desc',
        sortName: 'regDate',
        checkboxHeader: true,
        sorttable: true,
        responseHandler: responseFunc,
        queryParams: getSearchP,
        pageList: '[10, 15, 20, 25, 50, 100]',
        columns: [
        [{
            halign: "center",
            font: 15,
            align: "left",
            class: "totalTitle",
            colspan: 17
        }],
        [{
            field: 'agentId',
            title: 'ID',
            align: 'center',
            valign: 'middle',
            sortable: true,
        },{
            field: 'account',
            title: '账号',
            align: 'center',
            valign: 'middle',
            sortable: true,
        },{
            field: 'agentRole',
            title: '所属角色',
            align: 'center',
            valign: 'middle',
            sortable: true,
        },{
            field: 'op',
            title:'操作',
            align: 'center',
            valign: 'middle',
            formatter: getOp
        }
    ]],

    //注册加载子表的事件。注意下这里的三个参数！
    onExpandRow: function (index, row, $detail) {
        console.log(index, row, $detail);
        InitSubTable(index, row, $detail);
    }});

    function getOp(value, row, index) {
        var comfirmList = [       //需要dialog确认打开的url
            '/admin/agent/freeze',
        ];
        eval('rowobj=' + JSON.stringify(row))
        var opList = []
        for (var i = 0; i < rowobj['op'].length; ++i) {
            var op = rowobj['op'][i];
            var str = JSON.stringify({account: rowobj['account'], role: rowobj['agentRole']});
            var cStr = str.replace(/\"/g, "@");
            btn_type = 'primary';
            txt = '查看';
            opList.push(String.format("<a href=\"javascript:;\" class=\"btn btn-{5} btn-sm btn-xs\" onclick=\"showAccessDialog(\'{0}\', \'{1}\', \'{2}\', \'{3}\')\"><i class=\"glyphicon glyphicon-edit\"> {4} </i></a> ", op['url'], op['method'], rowobj['account'], rowobj['agentRole'], txt, btn_type));
        }
        return opList.join('');
    }


    function responseFunc(res) {
        data = res.data;
        count = res.count;
        //实时刷

        $('.totalTitle').html("角色总数： " + count)
        var root = document.getElementsByClassName('totalTitle')[0];
        root.style.cssText = "background-color:#d9edf7;height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
        return data;
    }

    //定义列操作
    function getSearchP(p) {
        sendParameter = p;

        return sendParameter;
    }

    function status(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (rowobj['valid'] == '0') {
            statusstr = '<span class="label label-danger">冻结</span>';
        } else if (rowobj['valid'] == '1') {
            statusstr = '<span class="label label-success">有效</span>';
        }

        return [
            statusstr
        ].join('');
    }

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

    function showAccessDialog(url, method, account, role) {
        layer.open({
            type: 2,
            title: '权限查看',
            shadeClose: true,
            shade: 0.5,
            area: ['70%', '70%'],
            content: String.format('{0}?account={1}&role={2}', url, account, role),
        });
    }

</script>
%rebase admin_frame_base
