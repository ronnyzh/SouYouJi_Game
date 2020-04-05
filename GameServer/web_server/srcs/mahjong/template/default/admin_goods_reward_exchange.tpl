<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<div class='block' id="tools">
     %include admin_frame_header
     <div class='content'>
      %include search
      <button id="btn_add" onclick="_batchSettingStatus();" type="button" class="btn btn-sm btn-primary">
          <span class="glyphicon glyphicon-asterisk">
              <a href="javascript:;" style='color:#FFF;text-decoration:none;'>批量发货</a>
          </span>
      </button>
      <table id='loadDataTable' class="table table-bordered table-hover table-striped" ></table>
     </div>
</div>
<script type="text/javascript">

// $(function(){
//         var tool_app = new Vue({
//             el : '#tools',
//             data:{
//                 batch_btn : '批量发货'
//             },mounted:function(){
//                 this.$data.batch_btn ='批量发货'
//             },methods:{
//                 onRefresh : function(){
//                     $('#loadDataTable').bootstrapTable('refresh',{
//                         'url':"{{info['tableUrl']}}"+"&user_id="+$('#searchId').val()
//                     })
//                 },
//             },delimiter : ['${','}']
//         });
// })

$('#loadDataTable').bootstrapTable({
      method: 'get',
      url: "{{info['tableUrl']}}",
      contentType: "application/json",
      datatype: "json",
      cache: false,
      checkboxHeader: true,
      striped: true,
      pagination: true,
      pageSize: 15,
      pageList: [15, 50, 100,'All'],
      search: true,
      showRefresh: true,
      minimumCountColumns: 2,
      clickToSelect: true,
      smartDisplay: true,
      sidePagination : "server",
      queryParamsType:'',
      responseHandler:responseFunc,
      //onLoadError:responseError,
      showExport:true,
      onSort:getCellSortByClick,
      exportTypes:['excel', 'csv', 'pdf', 'json'],
      //exportOptions:{fileName: "{{info['title']}}"+"_"+ new Date().Format("yyyy-MM-dd")},
      columns: [
      {
        checkbox:true
      },
      {
          field: 'exchange_reward_id',
          title: '奖品ID',
          align: 'center',
          valign: 'middle'
      },{

          field: 'exchange_reward_name',
          title: '奖品名称',
          align: 'center',
          valign: 'middle'
      },{

          field: 'exchange_reward_img_path',
          title: '奖品图片',
          align: 'center',
          valign: 'middle',
          formatter:getReardImages
      },{

          field: 'exchange_need_ticket',
          title: '奖品单价(/券)',
          align: 'center',
          valign: 'middle'
      },{

          field: 'exchange_use_ticket',
          title: '兑换使用券',
          align: 'center',
          valign: 'middle'
      },{

          field: 'exchange_user_phone',
          title: '联系人',
          align: 'center',
          valign: 'middle'
      },{

          field: 'exchange_user_addr',
          title: '收获地址',
          align: 'center',
          valign: 'middle'
      },{

          field: 'exchange_user_name',
          title: '姓名',
          align: 'center',
          valign: 'middle'
      },{

          field: 'exchange_date',
          title: '兑换时间',
          align: 'center',
          sortable:true,
          valign: 'middle'
      },{

          field: 'user_id',
          title: '玩家编号',
          align: 'center',
          valign: 'middle',
      },{

          field: 'exchange_type',
          title: '奖品类型',
          align: 'center',
          valign: 'middle',
      },{

          field: 'exchange_reward_status',
          title: '发货状态',
          align: 'center',
          valign: 'middle',
          sortable:true,
          formatter:status
      },{
          field: 'op',
          title: '操作',
          align: 'center',
          valign: 'middle',
          formatter:getOp
      }]
  });


    function getOp(value,row,index){
        eval('rowobj='+JSON.stringify(row))
        comfirmUrls = [
                '/admin/goods/reward/exchange/status',
                '/admin/goods/reward/exchange/del'
        ]
        var opList = []
        for (var i = 0; i < rowobj['op'].length; ++i) {
            var op = rowobj['op'][i];
            var str = JSON.stringify({exchange_id : rowobj['exchange_id']});
            var cStr = str.replace(/\"/g, "@");
            if(comfirmUrls.indexOf(op['url']) !=-1){
                opList.push(String.format("<a href=\"#\" class=\"btn btn-primary\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"> {3}</a> ", op['url'], op['method'], cStr, op['txt']));
            }else{
                opList.push(String.format("<a href=\"{0}?reward_id="+rowobj['reward_id']+"\" class=\"btn btn-primary\" >{1}</a> ", op['url'],op['txt']));
            }
        }
        if (opList.length == 0)
            return "该商品已发货";
        return opList.join('');
    }

    function getCellSortByClick(name,sort){ //用于服务端排序重写

        console.log(String.format('------getCellSortByClick name[{0}] sort[{1}]',name,sort));
        $('#loadDataTable').bootstrapTable('refresh',{'url':String.format('{0}&sort_name={1}&sort_method={2}&user_id{3}','{{info["tableUrl"]}}',name,sort,$('#searchId').val())});
    }

    function _batchSettingStatus(){
      var exchangeIds = $.map($('#loadDataTable').bootstrapTable('getSelections'),function(row){
          return row.exchange_id;
      });

      if (!exchangeIds.length){    //如果没选择直接return
          console.log('---------------had not selected.. return');
          return;
      }

      var remoteUrl = "{{info['batch_url']}}",
          method    = "POST",
          jsonStr   = {'exchangeIds':exchangeIds.join(',')}

      console.log('----------------select batch_ids['+exchangeIds+']');
      formAjax(remoteUrl,method,jsonStr,'正在设置...,');
    }

    function status(value,row,index){
        eval('var rowobj='+JSON.stringify(row))
        var statusstr = '';
        if(row['exchange_reward_status'] == '0'){
            statusstr = '<span class="label label-danger">未发货</span>';
        }else if(row['exchange_reward_status'] == '1'){
            statusstr = '<span class="label label-success">已发货</span>';
        }
        return [
            statusstr
        ].join('');
    }

    function getReardImages(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          statusstr = '<img src="'+row['exchange_reward_img_path']+'" width="50" height="50" />';

          return [statusstr].join('');
    }


    function responseFunc(res){

        return {"rows": res.data,
                "total": res.count};
    }

    function responseError(status) {
        location.reload();
    }
</script>
%rebase admin_frame_base
