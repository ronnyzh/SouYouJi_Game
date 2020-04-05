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
    /**
     *表格数据
     */
    var editId;        //定义全局操作数据变量
    var isEdit;
    var startDate;
    var endDate;
    $('#loadDataTable').bootstrapTable({
        method: 'get',
        url: "{{info['tableUrl']}}",
        contentType: "application/json",
        datatype: "json",
        detailView: true,//父子表
        cache: false,
        detailView: true,
        checkboxHeader: true,
        striped: true,
        pagination: true,
        pageSize: 10,
        pageList: [10, 15, 25, 50, 100, 'All'],
        minimumCountColumns: 2,
        clickToSelect: true,
        smartDisplay: true,
        sortOrder: 'asc',
        sortName: 'gameid',
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
                    "halign":"center",
                    "align":"center",
                    "class":'total',
                    "colspan":13
            }],
            [{
                field: 'gameid',
                title: '游戏ID',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'id',
                title: '比赛ID',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'gamename',
                title: '游戏名称',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'title',
                title: '比赛名称',
                align: 'center',
                valign: 'middle',
                sortable: true,
/*
            }, {
                field: 'type',
                title: '比赛类型',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: function (value) {
                    if (value == '1') {
                        return '定时开赛'
                    } else {
                        return '人满即开'
                    }
                },
*/
            }, {
                field: 'matchtype',
                title: '场次类型',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: function (value) {
                    if (value == 'roomCard'){
                        return '钻石'
                    }else if (value == 'gamePoint'){
                        return '积分'
                    }else {
                        return ''
                    }
                },
            }, {
                field: 'fee',
                title: '报名费用',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: function (value) {
                    if (value == '0') {
                        return '免费'
                    } else {
                        return value
                    }
                },
            }, {
                field: 'play_num',
                title: '比赛人数',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'enrollNum',
                title: '报名人数',
                align: 'center',
                valign: 'middle',
                sortable: true,
/*
            }, {
                field: 'rule',
                title: '说明',
                align: 'center',
                valign: 'middle',
                sortable: true,
*/
            }, {
                field: 'display',
                title: '可见状态',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: is_display
            }, {
                field: 'enroll_status',
                title: '报名状态',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: is_status
            }, {
                field: 'createTime',
                title: '创建时间',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'server',
                title: '游戏服务器',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'op',
                title: '操作',
                align: 'left',
                valign: 'middle',
                formatter: getOp
            }]],

            onExpandRow: function (index, row, $detail) {
              console.log(index,row,$detail);
              InitSubTable(index, row, $detail);
           }
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
            var str = JSON.stringify({id: rowobj['id'], gameid: rowobj['gameid']});
            var cStr = str.replace(/\"/g, "@");
            if (['修改', '比赛规则'].indexOf(op['txt']) >= 0 ){
                opList.push(String.format("<a href=\"{0}?id=" + rowobj['id'] + "&gameId="  + rowobj['gameid'] + "\" class=\"btn btn-primary btn-sm btn-xs\" > {1}</a> ", op['url'], op['txt']));
            }else{
                if (op['txt'] == '删除'){
                    var btn_type = 'danger';
                }else{
                    var btn_type = 'primary';
                }
                opList.push(String.format("<a href=\"javascript:;\" class=\"btn btn-{4} btn-sm btn-xs\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"> {3} </a> ", op['url'], op['method'], cStr, op['txt'], btn_type));
            }
        }
        return opList.join('');
    }

    function responseFunc(res) {
        var count = res.length;
        top_show_str = String.format("比赛场总数：{0}", count);
        $('.total').html(top_show_str)
        var total = document.getElementsByClassName('total')[0];
        total.style.cssText = "background-color:#d9edf7;height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
        return res;
    }

    function responseError(status) {
        location.reload();
    }

    function is_display(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          var statusstr = '';
          if(rowobj['display'] == '1'){
              statusstr = '<span class="label label-success">可见</span>';
          }else if(rowobj['display'] == '0'){
              statusstr = '<span class="label label-danger">不可见</span>';
          }
          return [statusstr].join('');
      }

    function is_status(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          var statusstr = '';
          if(rowobj['enroll_status'] == '1'){
              statusstr = '<span class="label label-success">开启</span>';
          }else if(rowobj['enroll_status'] == '0'){
              statusstr = '<span class="label label-danger">关闭</span>';
          }

          return [
              statusstr
          ].join('');
      }
</script>
<script>
function InitSubTable(index, row, $detail) {
        var playId = row.id;
        var gameId = row.gameid;
        var cur_table = $detail.html('<table class="table-bordered table-hover definewidth" style="background-color:#428bca4d;border-color: #428bca4d;border-width: 2px 2px 2px 2px;"></table>').find('table');
        $(cur_table).bootstrapTable({
                url: '{{info["enrollUserUrl"]}}',
                method: 'get',
                contentType: "application/json",
                datatype: "json",
                cache: false,
                sortOrder: 'desc',
                sortName: 'regDate',
                striped: true,
                checkboxHeader: true,
                pagination: true,
                pageSize: 10,
                pageList: [10, 15, 25, 50, 100, 'All'],
                strictSearch: true,
                minimumCountColumns: 5,
                clickToSelect: true,
                smartDisplay: true,
                queryParams:getSearchP,
                columns: [{
                    field: 'userId',
                    title: '用户ID',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                },{
                    field: 'account',
                    title: '用户账号',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                },{
                    field: 'nickname',
                    title: '用户昵称',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                }],

                onExpandRow: function (index, row, $detail) {
                    console.log(index,row,$detail);
                    InitSubTable(index, row, $detail);
                }

        });

        function getSearchP(p){
              sendParameter = p;
              sendParameter['playId'] = playId;
              sendParameter['gameId'] = gameId;
              return sendParameter;
        }
}
</script>
%rebase admin_frame_base
