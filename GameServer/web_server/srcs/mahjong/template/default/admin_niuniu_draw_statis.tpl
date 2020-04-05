<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
      <div class="block">
                <div class="header bordered-bottom bordered-themesecondary" id="crumb">
                    %if info.get('title', None):
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary" id="subTitle">{{info['title']}}</span>
                    %end
                </div>
                <div class="content">
                    <table id="dataTable" class="table table-bordered table-hover"></table>
                </div>
      </div>
<script type="text/javascript">

    startDate = $("#pick-date-start").val();
    endDate   = $("#pick-date-end").val();
    $('#dataTable').bootstrapTable({
          method: 'get',
          url: '{{info["listUrl"]}}',
          contentType: "application/json",
          datatype: "json",
          cache: true,
          checkboxHeader: true,
          striped: true,
          pagination: true,
          pageSize: 24,
          pageList: [24, 48, 100,'All'],
          queryParamsType:'',
          sidePagination:"server",
          search: true,
          showColumns: true,
          minimumCountColumns: 2,
          clickToSelect: true,
          //smartDisplay: true,
          responseHandler:responseFun,
          //onLoadError:responseError,
          queryParams:getSearchP,
          sortOrder: 'asc',
          sortable: false,                     //是否启用排序
          sortName:'id',
          showExport:true,
          exportTypes:['excel', 'csv', 'pdf', 'json'],
          // exportOptions:{fileName: "{{info['title']}}"+"_"+ new Date().Format("yyyy-MM-dd")},
          columns: [
              {
                  field: 'uid',
                  title: '用户ID',
                  align: 'center',
                  valign: 'middle',
                  sortable: true
              },{
              field: 'nickname',
              title: '微信昵称',
              align: 'center',
              valign: 'middle',
              sortable: true
              },{
              field: 'account',
              title: '微信账号',
              align: 'center',
              valign: 'middle',
              sortable: true
              },{
              field: 'phone',
              title: '手机号',
              align: 'center',
              valign: 'middle',
              sortable: true
              },{
              field: 'share_count',
              title: '分享次数',
              align: 'center',
              valign: 'middle',
              sortable: true
              },{
              field: 'niuniu_count',
              title: '牛牛次数',
              align: 'center',
              valign: 'middle',
              sortable: true
              },{
              field: 'game_count',
              title: '对局数总和',
              align: 'center',
              valign: 'middle',
              sortable: true
              },{
              field: 'score_total',
              title: '总积分',
              align: 'center',
              valign: 'middle',
              sortable: true
              },{
              field: 'draw_count_used',
              title: '已抽奖次数',
              align: 'center',
              valign: 'middle',
              sortable: true
              },{
              field: 'draw_times',
              title: '剩余抽奖次数',
              align: 'center',
              valign: 'middle',
              sortable: true
              },{
              field: 'cash_total',
              title: '总获得现金',
              align: 'center',
              valign: 'middle',
              sortable: true
              },{
              field: 'cash_get',
              title: '可领取现金',
              align: 'center',
              valign: 'middle',
              sortable: true
              },{
              field: 'roomcard_total',
              title: '总获得钻石数',
              align: 'center',
              valign: 'middle',
              sortable: true
              },{
              field: 'op',
              title: '操作',
              align: 'center',
              valign: 'middle',
              formatter:getOp
          }]
    });


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

        function getOp(value,row,index){
            eval('rowobj='+JSON.stringify(row))
            var opList = []
            for (var i = 0; i < rowobj['op'].length; ++i) {
                var op = rowobj['op'][i];
                var str = JSON.stringify({id : rowobj['account']});
                var cStr = str.replace(/\"/g, "@");
                if(op['url'] == '/admin/member/gm/kick')
                    opList.push(String.format("<a href=\"#\" class=\"btn btn-info\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"><i class=\"fa fa-edit\"> {3} </i></a> ", op['url'], op['method'], cStr, op['txt']));
                else
                    opList.push(String.format("<a href=\"{0}?id="+rowobj['id']+"\" class=\"btn btn-info\" ><i class=\"fa fa-edit\"> {1} </i></a> ", op['url'],op['txt']));
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
            return {"rows": res.result,
                "total": res.total};
        }

        function responseError(status) {
            location.reload();
        }
</script>
%rebase admin_frame_base

