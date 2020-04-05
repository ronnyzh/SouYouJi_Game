<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/checkEvent.js?{{RES_VERSION}}"></script>
<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
        %include admin_frame_header
        <div class="table-toolbar" style="float:left;width:100%;position:relative;top:2.6em">
            <table id="memberOLtable" class="table table-bordered table-hover"></table>
        </div>
</div>
<script type="text/javascript">
    /**
      * 服务端刷新表格
      --------------------------------------------
    */
    $(function () {
        $('#memberOLtable').bootstrapTable({
            method:'get',
            url   :'{{info["tableUrl"]}}',
            smartDisplay: true,
            pagination: true,
            pageSize: 15,
            pageList: [15,50,100],
            detailView: true,
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
            responseHandler:responseFunc,
            columns: [
                      [{
                          "halign":"left",
                          "align":"left",
                          "class": 'count',
                          "colspan": 11
                      }],
                      [{
                          field: 'num',
                          title: '序号',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'game_id',
                          title: '游戏ID',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'match_id',
                          title: '比赛场次',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'game_name',
                          title: '游戏名称',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'match_number',
                          title: '比赛编号',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'total_fee',
                          title: '报名费用',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'total_num',
                          title: '报名人数',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'start_time',
                          title: '开始时间',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'match_state',
                          title: '状态',
                          align: 'center',
                          valign: 'middle',
                          sortable: true,
                          formatter: function (value) {
                               return '<span class="label label-danger">进行中</span>'
                          },
                      },{
                          field: 'match_dismissReason',
                          title: '状态说明',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                }]],
                    onExpandRow: function (index, row, $detail) {
                    console.log(index,row,$detail);
                    InitSubTable(index, row, $detail);
              }
        });

        function responseFunc(res){
            var data = res.data;
            var count= res.count;
            $('.count').text(String.format("当前赛事：{0}",count));
            var totalTitle = document.getElementsByClassName('count')[0];
            totalTitle.style.cssText = "background-color:#d9edf7;height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            return data;
        }

    function InitSubTable(index, row, $detail) {
        var match_number = row.match_number;
        var game_id = row.game_id;
        var match_id = row.match_id;
        var cur_table = $detail.html('<table class="table-bordered table-hover definewidth" style="background-color:#428bca4d;border-color: #428bca4d;border-width: 2px 2px 2px 2px;"></table>').find('table');
        $(cur_table).bootstrapTable({
                url: '{{ info['user_tableUrl'] }}',
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
                    field: 'user_id',
                    title: '用户ID',
                    align: 'center',
                    valign: 'middle'
                },{
                    field: 'account',
                    title: '用户账号',
                    align: 'center',
                    valign: 'middle'
                },{
                          field: 'roomTag',
                          title: '房间号',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'clientKind',
                          title: '客户端类型',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'date',
                          title: '进入房间时间',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'login_ip',
                          title: '登录IP',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'serverTag',
                          title: '服务器标识',
                          align: 'center',
                          valign: 'middle',
                          sortable: false
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
              sendParameter['game_id'] = game_id;
              sendParameter['match_id'] = match_id;
              sendParameter['match_number'] = match_number;
              return sendParameter;
        }
}

    });
</script>
%rebase admin_frame_base
