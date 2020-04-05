<div class="block">
        <div class="header bordered-bottom bordered-themesecondary" id="crumb">
            %if info.get('title', None):
            <i class="widget-icon fa fa-tags themesecondary"></i>
            <span class="widget-caption themesecondary" id="subTitle">{{info['title']}}</span>
            %end
        </div>
        <div class="content">
            <table id="applyTable" class="table table-bordered table-hover"></table>
        </div>
</div>

<script type="text/javascript">
  $("#applyTable").bootstrapTable({
            url: '{{info["listUrl"]}}',
            method: 'get',
            //sidePagination: "server",
            pagination: true,
            pageSize: 48,
            sortOrder: 'desc',
            sortName: 'regDate',
            pageList: [48, 100],
            columns: [
            {
                field: 'id',
                title: '玩家编号',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{
                field: 'name',
                title: '玩家名称',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{
                field: 'headImgUrl',
                title: '玩家头像',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter:getImg,
            },{
                field: 'time',
                title: '申请时间',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{
                field: 'op',
                title: '操作',
                align: 'center',
                valign: 'middle',
                formatter:getOp
            }],

            //注册加载子表的事件。注意下这里的三个参数！
            onExpandRow: function (index, row, $detail) {
                console.log(index,row,$detail);
                InitSubTable(index, row, $detail);
            }
  });


function getOp(value,row,index){
      eval('rowobj='+JSON.stringify(row))
      var opList = []
      for (var i = 0; i < rowobj['op'].length; ++i) {
          var op = rowobj['op'][i];
          var str = JSON.stringify({id : rowobj['id']});
          var cStr = str.replace(/\"/g, "@");
          var param = rowobj['parentId'] ;
          opList.push(String.format("<a href=\"#\" class=\"btn btn-primary btn-sm btn-xs\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"><i class=\"glyphicon glyphicon-edit\"> {3} </i></a> ", op['url'], op['method'], cStr, op['txt']));

      }
      return opList.join('');
}


function status(value,row,index){
    eval('var rowobj='+JSON.stringify(row))
    var statusstr = '';
    if(rowobj['valid'] == '0'){
        statusstr = '<span class="label label-danger">冻结</span>';
    }else if(rowobj['valid'] == '1'){
        statusstr = '<span class="label label-success">有效</span>';
    }

    return [
        statusstr
    ].join('');
}

function getImg(value,row,index){
    eval('var rowobj='+JSON.stringify(row))
    statusstr = '<img src="'+row['headImgUrl']+'" width="30" height="30" />';

    return [statusstr].join('');
}

String.format = function() {
    if( arguments.length == 0 ) {
    return null; 
    }
    var str = arguments[0];
    for(var i=1;i<arguments.length;i++) {
    var re = new RegExp('\\{' + (i-1) + '\\}','gm');
    str = str.replace(re, arguments[i]);
    }
    return str;
}

</script>
%rebase admin_frame_base
