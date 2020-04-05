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
            url   :'{{info["listUrl"]}}',
            smartDisplay: true,
            pagination: true,
            pageSize: 15,
            pageList: [15,50,100],
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
                          "colspan": 14
                      }],
                      [{
                          field: 'id',
                          title: '玩家编号',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'name',
                          title: '玩家名称',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'parentAg',
                          title: '所属公会',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'gameModel',
                          title: '游戏类型',
                          align: 'center',
                          valign: 'middle',
                          sortable: true,
                          formatter: function (value) {
                            if (value == '比赛场') {
                                return '<span class="label label-danger">比赛场</span>'
                            } else {
                                return '<span class="label label-primary">钻石</span>'
                            }
                        }
                      },{
                          field: 'roomCard',
                          title: '钻石余额',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'gamePoint',
                          title: '积分余额',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
                      },{
                          field: 'matchNumber',
                          title: '场次编号',
                          align: 'center',
                          valign: 'middle',
                          sortable: true
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
                          title: '登录时间',
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
                      },{
                          field: 'op',
                          title: '操作',
                          align: 'center',
                          valign: 'middle',
                          sortable: false,
                          formatter:getOp
                }]]
        });

        function getOp(value,row,index){
            eval('rowobj='+JSON.stringify(row))
            var opList = []
            opList.push("<a href='javascript:;' onClick=\"comfirmDialog('/admin/member/kicks?account="+rowobj['account']+"&groupId="+rowobj['parentAg']+"','GET','{}')\" class=\"btn btn-sm btn-primary\" <i class=\"fa fa-edit\"> </i>踢出</a> ");
            return opList.join('');
        }

        function responseFunc(res){
            data = res.data;
            count= res.count;
            //实时刷
            $('.count').text(String.format("当前在线人数：{0}",count));
            var totalTitle = document.getElementsByClassName('count')[0];
            totalTitle.style.cssText = "background-color:#d9edf7;height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            return data;
        }
    });
</script>
<script type="text/javascript">
    checker.refreshMemberOlTable();
</script>
%rebase admin_frame_base
