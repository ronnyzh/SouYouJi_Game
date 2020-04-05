<div class='block'>
    %include admin_frame_header
    <div class='content'>
        <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
            <a id="add" href="{{info["createUrl"]}}" style='color:#FFF;text-decoration:none;'>
                <button id="btn_add" type="button" class="btn btn-sm btn-primary">
                    <i class="glyphicon glyphicon-plus"> {{info['addTitle']}} </i>
                </button>
            </a>
        </div>
        <table id='loadDataTable' class="table table-bordered table-hover table-striped"></table>
    </div>
</div>
<script type="text/javascript">
    var editId;
    var isEdit;
    var startDate;
    var endDate;
    $('#loadDataTable').bootstrapTable({
        method: 'get',
        url: "{{info['tableUrl']}}",
        contentType: "application/json",
        datatype: "json",
        cache: false,
        checkboxHeader: true,
        striped: true,
        pagination: true,
        pageSize: 24,
        pageList: [24, 48, 100, 'All'],
        minimumCountColumns: 2,
        clickToSelect: true,
        smartDisplay: true,
        sortOrder: 'asc',
        sortName: 'order',
        queryParams: getSearchP,
        responseHandler: responseFunc,
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
                font: 15,
                align: "left",
                class: "totalTitle",
                colspan: 17
            }],
            [{
                field: 'ad_id',
                title: '广告ID',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{
                field: 'title',
                title: '广告名称',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{
                field: 'img_path',
                title: '广告图片',
                align: 'center',
                valign: 'middle',
                formatter: getRewardImg,
            },{
                field: 'order',
                title: '排序',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: order,
            },{
                field: 'note',
                title: '备注',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{
                field: 'create_time',
                title: '创建时间',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'op',
                title: '操作',
                align: 'center',
                valign: 'middle',
                formatter: getOp
            }]]
    });

    //定义列操作
    function getSearchP(p) {
        sendParameter = p;

        sendParameter['startDate'] = startDate;
        sendParameter['endDate'] = endDate;

        startDate = $("#data-pick-start").val();
        endDate = $("data-pick-end").val();

        return sendParameter;
    }

    function getOp(value, row, index) {
        eval('rowobj=' + JSON.stringify(row))
        var opList = []
        for (var i = 0; i < rowobj['op'].length; ++i) {
            var op = rowobj['op'][i];
            var str = JSON.stringify({id: rowobj['ad_id']});
            var cStr = str.replace(/\"/g, "@");
            if (op['txt'] == '删除')
                opList.push(String.format("<a href=\"javascript:;\" class=\"btn btn-danger btn-sm btn-xs\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"><i class=\"glyphicon glyphicon-trash\"> {3} </i></a> ", op['url'], op['method'], cStr, op['txt']));
            else
                opList.push(String.format("<a href=\"{0}?adId=" + rowobj['ad_id'] + "\" class=\"btn btn-primary btn-sm btn-xs\" > <i class=\"glyphicon glyphicon-edit\"> {1} </i></a> ", op['url'], op['txt']));
        }
        return opList.join('');
    }

    function getRewardImg(value,row,index){
        eval('var rowobj='+JSON.stringify(row))
        statusstr = '<img src="'+row['img_path']+'" width="100" height="100" />';
        return [statusstr].join('');
    }

    function order(value,row,index){
        eval('var rowobj='+JSON.stringify(row))
        statusstr = '<span class="label label-primary">' + row['order'] + '</span>';
        return [statusstr].join('');
    }

    function responseFunc(res) {
        var count = res.length;
        $('.totalTitle').html("广告总数 ：" + count);
        var totalTitle = document.getElementsByClassName('totalTitle')[0];
        totalTitle.style.cssText = "background-color:#d9edf7;height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
        return res;
    }

    function responseError(status) {
        location.reload();
    }
</script>
%rebase admin_frame_base
