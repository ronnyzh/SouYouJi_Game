<div class="cl-mcont">
  <div class="block">
            <div class="header bordered-bottom bordered-themesecondary" id="crumb">
                %if info.get('title', None):
                <i class="widget-icon fa fa-tags themesecondary"></i>
                <span class="widget-caption themesecondary" style='font-size:16px;font-weight:bold' id="subTitle">{{info['title']}}</span>
                %end
            </div>
            <div class="content">
                %include search
                <table id="agentTable" class="table table-bordered table-hover"></table>
            </div>
  </div>
</div>
<script>
//    "dateTime":"2017年9月20日21:18:25",
//                "uid":"1",
//                "playerName":"test21",
//                "rewardName":"钻石*3",
//                "rewardId":"1",
//                "rewardCount":"3"
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
                field: 'date',
                title: '获得时间',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'id',
                title: '玩家ID',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'name',
                title: '玩家昵称',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'rewardTitle',
                title: '奖品名称',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'rewardId',
                title: '奖品ID',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'rewardNum',
                title: '获得数量',
                align: 'center',
                valign: 'middle',
                sortable: true,
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
    //创建图片
    function createImg(value, row, index) {
        if(!value){return ;}
        var rowobj = JSON.parse(JSON.stringify(row));
        var img = document.createElement("img");
        img.src = value;
        img.height = "100";
        img.alt = rowobj["title"];
        return img.outerHTML;
    }
    //创建奖品列表
    function rewardInclude(value, row, index) {
        console.log("rewardInclude",arguments);
        if(!value) return;
        var parentAg = row["id"]
        var cur_table = $('<table table-bordered definewidth ></table>');

        $(cur_table).bootstrapTable({
            data: value,
            contentType: "application/json",
            datatype: "json",
            cache: false,
            search: true,
            sorttable: true,
            queryParams: getSearchP,
            sortOrder: 'desc',
            sortName: 'regDate',
            pageSize: 15,
            pageList: [15, 25],
            columns: [
                {
                    field: 'id',
                    title: 'ID',
                    align: 'center',
                    valign: 'middle',
                    width: '100',
                    sortable: true,
                }, {
                    field: 'imgUrl',
                    title: '图片',
                    width: '80',
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
                }
            ],
            //注册加载子表的事件。注意下这里的三个参数！
            onExpandRow: function (index, row, $detail) {
                console.log(index, row, $detail);
                InitSubTable(index, row, $detail);
            }
        });

        //定义列操作
        function getSearchP(p) {
            sendParameter = p;
            sendParameter['id'] = parentAg;
            return sendParameter;
        }
        return cur_table.get(0).outerHTML;
    }

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
                    columns: [
                        {
                            field: 'id',
                            title: 'ID',
                            align: 'center',
                            valign: 'middle',
                            width: '100',
                            sortable: true,
                        }, {
                            field: 'imgUrl',
                            title: '图片',
                            width: '100',
                            align: 'center',
                            valign: 'middle',
                            sortable: true,
                            formatter: createImg
                        }, {
                            field: 'title',
                            title: '标题',
                            width: '100',
                            align: 'center',
                            valign: 'middle',
                            sortable: true,
                        }
                    ],
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
</script>
%rebase admin_frame_base