<div class="cl-mcont">
  <div class="block">
            <div class="header bordered-bottom bordered-themesecondary" id="crumb">
                %if info.get('title', None):
                <i class="widget-icon fa fa-tags themesecondary"></i>
                <span class="widget-caption themesecondary" style='font-size:16px;font-weight:bold' id="subTitle">{{info['title']}}</span>
                %end
                <span style='float:right;margin-right:10px;'>
                    <a href="{{info['createUrl']}}" class='btn btn-sm btn-primary' >
                    <i class='glyphicon glyphicon-plus'></i> 添加资源</a>
                </span>
            </div>
            <div class="content">
                %include search
                <table id="agentTable" class="table table-bordered table-hover"></table>
            </div>
  </div>
</div>
<script>
    $('#btn_search').click(function () {
        $('#agentTable').bootstrapTable('refresh');
    });
    $("#agentTable").bootstrapTable({
        url: '{{info["listUrl"]}}',
        method: 'get',
        detailView: eval("{{info['showPlus']}}"),//父子表
        //sidePagination: "server",
        pagination: true,
        pageSize: 48,
        sortOrder: 'desc',
        sortName: 'regDate',
        sorttable: true,
        responseHandler: responseFunc,
        queryParams: getSearchP,
        showExport: true,
        exportTypes: ['excel', 'csv', 'pdf', 'json'],
        pageList: [48, 100],
        columns: [
            {
                field: 'id',
                title: '图片ID',
                align: 'center',
                valign: 'middle',
                width:'100',
                sortable: true,
            }, {
                field: 'url',
                title: '图片',
                width:'100',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: createImg
            }, {
                field: 'title',
                title: '标题',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'note',
                title: '备注',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'op',
                title: '操作',
                align: 'center',
                valign: 'middle',
                formatter: getOp
            }],

        //注册加载子表的事件。注意下这里的三个参数！
        onExpandRow: function (index, row, $detail) {
            console.log(index, row, $detail);
            InitSubTable(index, row, $detail);
        }
    });
    //定义列操作
    function getSearchP(p){
      searchId = $("#searchId").val();

      sendParameter = p;

      sendParameter['searchId'] = searchId;

      return sendParameter;
    }


    function responseFunc(res){
        data = res.data;
        count= res.count;
        //实时刷
        $('.count').text(count);

        return data;
    }
    function getOp(value,row,index){
          eval('rowobj='+JSON.stringify(row))
          var opList = []
          for (var i = 0; i < rowobj['op'].length; ++i) {
              var op = rowobj['op'][i];
              var str = JSON.stringify({id : rowobj['id']});
              var cStr = str.replace(/\"/g, "@");
              var param = rowobj['id'] ;
              if(op['txt'] == '删除' )
                  opList.push(String.format(
                      "<a href=\"#\" class=\"btn btn-danger btn-sm btn-xs\" " +
                        "onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\">" +
                        "<i class=\"glyphicon glyphicon-trash\"> {3} </i>" +
                      "</a> ",
                      op['url'], op['method'], cStr, op['txt'])
                  );
              else
                  opList.push(String.format(
                      "<a href=\"{0}?id={1}\" class=\"btn btn-primary btn-sm btn-xs\">" +
                          "<i class=\"glyphicon glyphicon-edit\"> {2}</i>" +
                      "</a> ",
                      op['url'], param, op['txt']
                  ));
          }
          return opList.join('');
    }
    function createImg(value, row, index) {
        if(!value){return ;}
        var rowobj = JSON.parse(JSON.stringify(row));
        var img = document.createElement("img");
        img.src = value;
        img.height = "100";
        img.alt = rowobj["title"];
        return img.outerHTML;
    }
</script>
<!--
<script type="text/javascript">
  $('#btn_search').click(function(){

        $('#agentTable').bootstrapTable('refresh');
  });

  $("#agentTable").bootstrapTable({
            url: '{{info["listUrl"]}}',
            method: 'get',
            detailView: {{info['showPlus']}},//父子表
            //sidePagination: "server",
            pagination: true,
            pageSize: 48,
            sortOrder: 'desc',
            sortName: 'regDate',
            sorttable:true,
            responseHandler:responseFunc,
            queryParams:getSearchP,
            showExport:true,
            exportTypes:['excel', 'csv', 'pdf', 'json'],
            pageList: [48, 100],
            columns: [
            {
                field: 'parentAg',
                title: '代理账号',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{
                field: 'parentId',
                title: '公会ID',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{
                field: 'isTrail',
                title: '是否试玩',
                valign: 'middle',
                align: 'center',
                formatter:statusTrail,
            },{
                field: 'allMembers',
                title: '会员总数',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{
                field: 'members',
                sortable: true,
                title: '会员活跃数',
                align: 'center',
                valign: 'middle',
            },{
                field: 'roomCard',
                sortable: true,
                title: '当日耗钻数',
                align: 'center',
                valign: 'middle',
            },{
                field: 'valid',
                title: '状态',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter:status
            },{
                field: 'regDate',
                sortable: true,
                title: '创建时间',
                align: 'center',
                valign: 'middle',
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


//初始化子表格(无线循环)
function InitSubTable(index, row, $detail) {
        var parentAg = row.parentId;
        var cur_table = $detail.html('<table table-bordered table-hover definewidth style="margin-left:55px;background:#EEEEE0"></table>').find('table');
        $(cur_table).bootstrapTable({
                url: '{{info["listUrl"]}}',
                method: 'get',
                contentType: "application/json",
                datatype: "json",
                cache: false,
                search: true,
                sorttable:true,
                queryParams:getSearchP,
                sortOrder: 'desc',
                sortName: 'regDate',
                pageSize: 15,
                pageList: [15, 25],
                columns: [{
                    field: 'parentAg',
                    title: '代理名称',
                    align: 'center',
                    valign: 'middle'
                },{
                    field: 'agentType',
                    title: '代理类型',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
                },{
                    field: 'parentId',
                    title: '公会ID',
                    valign: 'middle',
                    align: 'center',
                    sortable: true
                },{
                    field: 'isTrail',
                    title: '是否试玩',
                    valign: 'middle',
                    align: 'center',
                    formatter:statusTrail,
                },{
                    field: 'allMembers',
                    title: '会员总数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true
                },{
                    field: 'members',
                    title: '活跃会员数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true
                },{
                    field: 'roomCard',
                    title: '当日耗钻数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true
                },{
                    field: 'valid',
                    title: '状态',
                    align: 'center',
                    valign: 'middle',
                    formatter:status
                },{
                    field: 'regDate',
                    title: '创建时间'
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

        //定义列操作
        function getSearchP(p){
              sendParameter = p;
              sendParameter['id'] = parentAg;
              return sendParameter;
        }

        function responseFunc(res){
            data = res.data;
            count= res.count;
            //实时刷

            return data;
        }

}

function getOp(value,row,index){
      eval('rowobj='+JSON.stringify(row))
      var opList = []
      for (var i = 0; i < rowobj['op'].length; ++i) {
          var op = rowobj['op'][i];
          var str = JSON.stringify({id : rowobj['parentId']});
          var cStr = str.replace(/\"/g, "@");
          var param = rowobj['parentId'] ;
          if(op['url'] == '/admin/agent/del' || op ['url'] == '/admin/agent/freeze' || op ['url'] == '/admin/agent/trail')
              opList.push(String.format("<a href=\"#\" class=\"btn btn-primary btn-sm btn-xs\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"><i class=\"glyphicon glyphicon-edit\"> {3} </i></a> ", op['url'], op['method'], cStr, op['txt']));
          else
              opList.push(String.format("<a href=\"{0}?id={1}\" class=\"btn btn-primary btn-sm btn-xs\"><i class=\"glyphicon glyphicon-edit\"> {2}</i></a> ", op['url'], param, op['txt']));
      }
      return opList.join('');
}


function responseFunc(res){
    data = res.data;
    count= res.count;
    //实时刷
    $('.count').text(count);

    return data;
}

//定义列操作
function getSearchP(p){
  searchId = $("#searchId").val();

  sendParameter = p;

  sendParameter['searchId'] = searchId;

  return sendParameter;
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

function statusTrail(value,row,index){
    eval('var rowobj='+JSON.stringify(row))
    var statusstr = '';
    if(rowobj['isTrail'] == '0'){
        statusstr = '<span class="label label-success">正式公会</span>';
    }else if(rowobj['isTrail'] == '1'){
        statusstr = '<span class="label label-warning">试玩公会</span>';
    }

    return [
        statusstr
    ].join('');
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
-->

%rebase admin_frame_base
