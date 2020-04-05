
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
      <div class="block">
                %include admin_frame_header
                <div class="content">
                    %include search
                    <table id="dataTable" class="table table-bordered table-hover"></table>
                </div>
</div>
<script type="text/javascript">
    var pageNumber;
    $('#btn_search').click(function(){
          $('#dataTable').bootstrapTable('refresh');
    });

    function get_bds(value,row,index){
        href = row['buy_diamond_stream']
        value = value || 0;
        return "<a href='"+href+"'>" + value + "</a>"
    }

    function get_bgs(value,row,index){
        href = row['buy_gold_stream']
        value = value || 0;
        return "<a href='"+href+"'>" + value + "</a>"
    }

    function get_grs(value,row,index){
        href = row['gold_record_stream']
        return "<a href='"+href+"'>跳转</a>"
    }

    function get_sbr(value,row,index){
        href = row['store_buy_record']
        return "<a href='"+href+"'>跳转购买流水</a>"
    }

    $('#dataTable').bootstrapTable({
          method: 'get',
          url: '{{info["listUrl"]}}',
          contentType: "application/json",
          datatype: "json",
          cache: false,
          striped: true,
          toolbar:'#toolbar',
          pagination: true,
          pageSize: 15,
          pageNumber:parseInt("{{info['cur_page']}}"),
          pageList: [15, 50, 100],
          queryParamsType:'',
          sidePagination:"server",
          minimumCountColumns: 2,
          clickToSelect: true,
          //smartDisplay: true,
          responseHandler:responseFun,
          queryParams:getSearchP,
          onSort:getCellSortByClick,
          //sortOrder: 'asc',
          //sortable: true,                     //是否启用排序
          // exportOptions:{fileName: "{{info['title']}}"+"_"+ new Date().Format("yyyy-MM-dd")},
          columns: [

          {
                field: 'uid',
                title: 'UID',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{

                field: 'account',
                sortable: true,
                title: '微信账号',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{

                field: 'nickname',
                title: '昵称',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{

                field: 'phone_num',
                title: '手机号',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{

                field: 'agent',
                sortable: true,
                title: '所属公会',
                align: 'center',
                valign: 'middle',
            },{

                field: 'agent_wealth_rank',
                sortable: true,
                title: '公会财富排名',
                align: 'center',
                valign: 'middle',
            },{

                field: 'gold_win_rate',
                title: '金币场胜率',
                valign: 'middle',
                align: 'center',
                valign:'middle',
                sortable: true,
            },{

                field: 'agent_win_rank',
                title: '公会胜局榜排名',
                align: 'center',
                valign: 'middle',
                sortable: true,
                valign:'middle'
            },{

                field: 'cur_diamond_num',
                title: '当前钻石数',
                valign: 'middle',
                align: 'center',
                valign:'middle',
                sortable: true,
            },{

                field: 'buy_diamond_num',
                title: '购买钻石金额',
                valign: 'middle',
                align: 'center',
                sortable: true,
                formatter:get_bds,
            },{

                field: 'sbr',
                title: '商城购买记录',
                align: 'center',
                valign: 'middle',
                formatter:get_sbr
            },{

                field: 'cur_gold_num',
                title: '当前金币数',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{

                field: 'buy_gold_num',
                title: '购买金币金额',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter:get_bgs,
            },{

                field: 'join_gold_game_sum',
                title: '参与金币场游戏总局数',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{

                field: 'grs',
                title: '金币战绩流水',
                align: 'center',
                valign: 'middle',
                formatter:get_grs
            },{

                field: 'first_log_date',
                title: '首次登陆时间',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{

                field: 'last_log_date',
                title: '最后登录时间',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }]
    });

      function status(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          var statusstr = '';
          if(rowobj['open_auth'] == '1'){
              statusstr = '<span class="label label-success">是</span>';
          }else if(rowobj['open_auth'] == '0'){
              statusstr = '<span class="label label-danger">否</span>';
          }

          return [
              statusstr
          ].join('');
      }

      function is_valid(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          var statusstr = '';
          if(rowobj['valid'] == '1'){
              statusstr = '<span class="label label-success">正常</span>';
          }else if(rowobj['valid'] == '0'){
              statusstr = '<span class="label label-danger">冻结</span>';
          }

          return [
              statusstr
          ].join('');
      }

      function getCellSortByClick(name,sort){ //用于服务端排序重写

          console.log(String.format('------getCellSortByClick name[{0}] sort[{1}]',name,sort));
          $('#dataTable').bootstrapTable('refresh',{'url':String.format('{0}&sort_name={1}&sort_method={2}','{{info["listUrl"]}}',name,sort)});
      }


      //定义列操作
      function getSearchP(p){
        var searchId = $("#searchId").val();
        console.log(p);
        sendParameter = p;
        sendParameter['searchId'] = searchId;

        return sendParameter;
      }

      function responseFun(res){
          count= res.total;
          //实时刷
          //$('.count').text(String.format("会员总人数:{0}",count));
          pageNumber = parseInt(res.pageNumber);
          return {"rows": res.result,
                  "total": res.total
          };
      }

      function responseError(status) {
          location.reload();
      }
</script>
%rebase admin_frame_base


