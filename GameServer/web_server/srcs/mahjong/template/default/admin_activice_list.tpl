<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<div class="cl-mcont">
  <div class="block">
            <div class="header bordered-bottom bordered-themesecondary" id="crumb">
                %if info.get('title', None):
                <i class="widget-icon fa fa-tags themesecondary"></i>
                <span class="widget-caption themesecondary" id="subTitle">{{info['title']}}</span>
                %end
                <!-- 解 绑 规 则 -->
            </div>
            <div class="content">
            <div class="table-toolbar" style="float:left">
                <a id="add" href='{{info["createUrl"]}}' class="btn btn-primary">
                    <i class="btn-label fa fa-plus"></i>{{info['addTitle']}}
                </a>
            </div>
                <table id="dataTable" class="table table-bordered table-hover"></table>
            </div>
  </div>
</div>

<script type="text/javascript">

    startDate = $("#pick-date-start").val();
    endDate   = $("#pick-date-end").val();
    $('#dataTable').bootstrapTable({
          method: 'get',
          url: '{{info["tableUrl"]}}',
          contentType: "application/json",
          datatype: "json",
          cache: true,
          checkboxHeader: true,
          striped: true,
          pagination: true,
          pageSize: 24,
          pageList: [24, 48, 100,'All'],
          // queryParamsType:'',
          // sidePagination:"server",
          showColumns: true,
          minimumCountColumns: 2,
          clickToSelect: true,
          search:true,
          //smartDisplay: true,
          responseHandler:responseFun,
          //onLoadError:responseError,
          queryParams:getSearchP,
          //sortOrder: 'asc',
          //sortable: true,                     //是否启用排序
          showExport:true,
          exportTypes:['excel', 'csv', 'pdf', 'json'],
          // exportOptions:{fileName: "{{info['title']}}"+"_"+ new Date().Format("yyyy-MM-dd")},
          columns: [
          {
              field: 'startdate',
              title: '开始时间',
              align: 'center',
              valign: 'middle'
          },{
              field: 'enddate',
              title: '结束时间',
              align: 'center',
              valign: 'middle'
          },{
              field: 'title',
              title: '活动标题',
              align: 'center',
              valign: 'middle'
          },{
              field: 'type',
              title: '活动类型',
              align: 'center',
              valign: 'middle',
              formatter:getTemplate
          },{
              field: 'agentid',
              title: '工会号',
              align: 'center',
              valign: 'middle'
          },{
              field: 'status',
              title: '状态',
              align: 'center',
              valign: 'middle',
              formatter:getStatusCredit
          },{
              field: 'op',
              title: '操作',
              align: 'center',
              valign: 'middle',
              formatter:getOp
          }]
    });

        function getStatusCredit(value,row,index) {
            if( parseInt(value) == 0)
                infoStr = String.format("<span style=\"color:blue;\">未提交</span>", value);
            else if (parseInt(value) == 1)
                infoStr = String.format("<span style=\"color:red;\">审核中</span>", value);
            else if (parseInt(value) == 2)
                infoStr = String.format("<span style=\"color:green;\">已通过</span>", value);
            else if (parseInt(value) == 3)
                infoStr = String.format("<span style=\"color:red;\">未通过</span>", value);
            else if (parseInt(value) == 4)
                infoStr = String.format("<span style=\"color:green;\">预开启</span>", value);
             else if (parseInt(value) == 5)
                infoStr = String.format("<span style=\"color:green;\">进行中</span>", value);
            else
                infoStr = String.format("<span style=\"color:green;\">已结束</span>", value);
            return [
                infoStr
            ].join('');
        }

        function getColorCredit(value,row,index) {
            if( parseInt(value) > 0)
                infoStr = String.format("<span style=\"color:red;\">+{0}</span>", value);
            else
                infoStr = String.format("<span style=\"color:green;\">{0}</span>", value);
            return [
                infoStr
            ].join('');
        }

        function getColorWithDraw(value,row,index) {
            infoStr = String.format("<span style=\"color: #6600FF;\">{0}</span>", value);
            return [
                infoStr
            ].join('');
        }

        function getTemplate(value,row,index){
            eval('var rowobj='+JSON.stringify(row))
            var statusstr = '';
            if(rowobj['type'] == '0'){
                statusstr = '<span class="label label-danger">红包雨</span>';
            }else if(rowobj['type'] == 'turnlate'){
                statusstr = '<span class="label label-success">风车</span>';
            }else{
                statusstr = '<span class="label label-success">转盘</span>';
            }
            return [
                statusstr
            ].join('');
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
                            "<a href=\"#\" class=\"btn btn-danger btn-sm \" " +
                              "onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\">" +
                              "<i class=\"glyphicon glyphicon-trash\"> {3} </i>" +
                            "</a> ",
                            op['url'], op['method'], cStr, op['txt'])
                        );
                  else if (op['txt'] == '关闭'){
                      opList.push(String.format(
                          "<a href=\"#\" class=\"btn btn-primary btn-sm \" " +
                            "onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\">" +
                            "<i class=\"glyphicon glyphicon-trash\"> {3} </i>" +
                          "</a> ",
                          op['url'], op['method'], cStr, op['txt'])
                      );
                  }
                  else
                      opList.push(String.format("<a href=\"{0}?id={1}\" class=\"btn btn-primary btn-sm\"><i class=\"glyphicon glyphicon-edit\"> {2}</i></a> ", op['url'], param, op['txt']));
              }
              return opList.join('');
        }


          //前台查询参数

        function getSearchP(p){
            // account = $("#account").val();
            // member_level = $('#member_level').val();
            // member_status = $("#member_status").val();
            // userId = $("#userId").val();
            startDate = $("#pick-date-start").val();
            endDate   = $("#pick-date-end").val();

            sendParameter = p;
            sendParameter['startDate'] = startDate;
            sendParameter['endDate']  = endDate;

            return sendParameter;
          }

        //获得返回的json 数据
        function responseFun(res){

            data = res.data;
            count= res.count;
            //实时刷
            return data;
        }

        function responseError(status) {
            location.reload();
        }
</script>
%rebase admin_frame_base

