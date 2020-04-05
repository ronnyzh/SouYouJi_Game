<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
      <div class="block">
                <div class="header bordered-bottom bordered-themesecondary" id="crumb">
                    %if info.get('title', None):
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary" style='font-size:16px;font-weight:bold' id="subTitle">{{info['title']}}</span>
                    %end
                    <!-- 解 绑 规 则 -->
                </div>
                <div class="content">
                    %include search
                    <table id="dataTable" class="table table-bordered table-hover"></table>
                </div>
      </div>
<script type="text/javascript">
    $('#btn_search').click(function(){
          
          $('#dataTable').bootstrapTable('refresh');
    });

    var firstDate=new Date();
    firstDate.setDate(firstDate.getDate()-6);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));

    $('#dataTable').bootstrapTable({

          method: 'get',
          url: '{{info["tableUrl"]}}',
          contentType: "application/json",
          datatype: "json",
          cache: false,
          striped: true,
          toolbar:'#toolbar',
          pagination: true,
          pageSize: 16,
          pageList: [16, 24, 100,'All'],
          queryParamsType:'',
          sidePagination:"server",
          minimumCountColumns: 2,
          clickToSelect: true,
          //smartDisplay: true,
          responseHandler:responseFun,
          //onLoadError:responseError,
          queryParams:getSearchP,
          //sortOrder: 'asc',
          //sortable: true,                     //是否启用排序
          // exportOptions:{fileName: "{{info['title']}}"+"_"+ new Date().Format("yyyy-MM-dd")},
          columns:[
          {
              field: 'date',
              title: '日期',
              align: 'center',
              valign: 'middle',
              sortable: true
          },{
              field: 'draw_last_count',
              title: '抽奖资格剩余数',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'no_cash_user',
              title: '未领取现金人数',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'no_cash_total',
              title: '未领取现金金额',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'get_cash_user',
              title: '已领取现金人数',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'get_cash_total',
              title: '已领取现金金额',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'roomcard_total',
              title: '总中奖钻石数',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'draw_used',
              title: '已抽奖次数',
              align: 'center',
              valign: 'middle',
              sortable: true,
          }
        ]
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

        function getOp(value,row,index){
            var comfirmUrls = [
                '/admin/member/kick',
                '/admin/member/freeze'
            ];
            eval('rowobj='+JSON.stringify(row))
            var opList = []
            for (var i = 0; i < rowobj['op'].length; ++i) {
                var op = rowobj['op'][i];
                var str = JSON.stringify({id : rowobj['id']});
                var cStr = str.replace(/\"/g, "@");
                if(comfirmUrls.indexOf(op['url'])>=0)
                    opList.push(String.format("<a href=\"#\" class=\"btn btn-primary btn-xs\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"><i class=\"fa fa-edit\"> {3} </i></a> ", op['url'], op['method'], cStr, op['txt']));
                else
                    opList.push(String.format("<a href=\"{0}?id="+rowobj['id']+"\" class=\"btn btn-primary btn-xs\" ><i class=\"fa fa-edit\"> {1} </i></a> ", op['url'],op['txt']));
            }
            return opList.join('');
        }

        function getImg(value,row,index){
            eval('var rowobj='+JSON.stringify(row))
            statusstr = '<img src="'+row['headImgUrl']+'" width="30" height="30" />';

            return [statusstr].join('');
        }

        function getColor(value,row,index){
            eval('var rowobj='+JSON.stringify(row))
            statusstr = '<span style="color:#6600FF">'+value+'</span>';

            return [statusstr].join('');
        }


          //前台查询参数
        
        //定义列操作
        function getSearchP(p){
          searchId = $("#searchId").val();
          startDate = $("#pick-date-start").val();
          endDate   = $("#pick-date-end").val();

          sendParameter = p;

          sendParameter['searchId'] = searchId;
          sendParameter['startDate'] = startDate;
          sendParameter['endDate'] = endDate;

          return sendParameter;
        }

        //获得返回的json 数据 
        function responseFun(res){
            startDate = $('#pick-date-start').val()
            endDate = $('#pick-date-end').val()
            count= res.count;
            img = res.headImgUrl;
            name = res.name || '<font color="red">请输入要查询的玩家ID</font>';
            $('.info').html("玩家名称: "+name+"&nbsp;  玩家头像:<img src='"+img+"' width='30' height='30' />");
            return {"rows": res.data,
                    "total": res.count
            };
        }

        function responseError(status) {
            location.reload();
        }
</script>
%rebase admin_frame_base

