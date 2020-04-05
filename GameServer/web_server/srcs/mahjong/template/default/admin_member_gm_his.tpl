<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<div class="block">
          %include admin_frame_header
          <div class="content">
             <table id="dataTable" class="table table-bordered table-hover"></table>
          </div>
</div>
<script type="text/javascript">
  $('#dataTable').bootstrapTable({
        method: 'get',
        url: '{{info["dataUrl"]}}',
        contentType: "application/json",
        datatype: "json",
        cache: false,
        pagination: true,
        pageSize: 24,
        showExport: true,
        exportTypes:['excel', 'csv', 'pdf', 'json'],
        pageList: [24, 48, 100, 'All'],
        //sidePagination : "server",
        sortOrder: 'desc',
        responseHandler:responseFun,
        //onLoadError:responseError,
        showExport:true,
        exportTypes:['excel', 'csv', 'pdf', 'json'],
        // exportOptions:{fileName: "{{info['title']}}"+"_"+ new Date().Format("yyyy-MM-dd")},
        columns: [
        {
            field: 'time',
            title: '操作时间',
            align: 'center',
            valign: 'middle',
        },{
            field: 'gamId',
            title: '游戏ID',
            align: 'center',
            valign: 'middle'
        },{
            field: 'roomId',
            title: '房间ID',
            align: 'center',
            valign: 'middle'
        },{
            field: 'message',
            title: '操作指令',
            align: 'center',
            valign: 'middle'
        }]
});

function responseFun(res){
    console.log('-------------------------recive datas:'+res.data);
    return res.data;
}

</script>
%rebase admin_frame_base
