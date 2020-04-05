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
            field: 'timestamp',
            title: '开始时间',
            align: 'center',
            valign: 'middle',
            formatter:getDate
        },{
            field: 'bet',
            title: '炮等级',
            align: 'center',
            valign: 'middle',
            formatter:getColor
        },{
            field: 'profit',
            title: '游玩结果',
            align: 'center',
            valign: 'middle',
            formatter:getFuncColor
        },{
            field: 'fishes',
            title: '击中鱼',
            align: 'center',
            valign: 'middle',
            formatter:getImg
        }]
});

function responseFun(res){
    console.log('-------------------------recive datas:'+res.data);
    return res.data;
}

</script>
%rebase admin_frame_base
