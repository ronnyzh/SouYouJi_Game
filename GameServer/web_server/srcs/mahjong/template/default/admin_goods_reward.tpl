<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<div class='block'>
     %include admin_frame_header
     <div class='content'>
      <div class="table-toolbar" style="float:left">
          <a id="add" href='{{info["createUrl"]}}' class="btn btn-primary">
              <i class="btn-label fa fa-plus"></i>{{info['addTitle']}}
          </a>
      </div>
      <table id='loadDataTable' class="table table-bordered table-hover table-striped" data-use-row-attr-func="true" data-reorderable-rows="true" ></table>
     </div>
</div>
<script type="text/javascript">
/**
  *表格数据
*/
var editId;        //定义全局操作数据变量
var isEdit;
var startDate;
var endDate;
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
      //sidePagination : "server",
      sortOrder: 'desc',
      sortName: 'datetime',
      responseHandler:responseFunc,
      //onLoadError:responseError,
      showExport:true,
      exportTypes:['excel', 'csv', 'pdf', 'json'],
      //exportOptions:{fileName: "{{info['title']}}"+"_"+ new Date().Format("yyyy-MM-dd")},
      columns: [
      {
            checkbox:true
      },
      {
          field: 'reward_id',
          title: '奖品ID',
          align: 'center',
          valign: 'middle'
      },{
          field: 'reward_pos',
          title: '奖品位置',
          align: 'center',
          valign: 'middle'
      },{

          field: 'reward_name',
          title: '奖品名称',
          align: 'center',
          valign: 'middle'
      },{

          field: 'reward_img_path',
          title: '商品图片',
          align: 'center',
          valign: 'middle',
          formatter:getRewardImg
      },{

          field: 'reward_nums',
          title: '奖品总期数',
          align: 'center',
          valign: 'middle'
      },{

          field: 'reward_now_nums',
          title: '奖品当前期数',
          align: 'center',
          valign: 'middle'
      },{

          field: 'reward_type',
          title: '奖品类型',
          align: 'center',
          valign: 'middle',
          formatter:reward_type
      },{

          field: 'reward_per_stock',
          title: '本期奖品剩余库存',
          align: 'center',
          valign: 'middle',
          sortable:true
      },{

          field: 'reward_stock',
          title: '每期奖品库存',
          align: 'center',
          valign: 'middle'
      },{

          field: 'reward_need_ticket',
          title: '所需兑换卷',
          align: 'center',
          valign: 'middle',
          sortable:true,
      },{

          field: 'reward_cost',
          title: '奖品成本',
          align: 'center',
          valign: 'middle'
      },{

          field: 'reward_auto_charge',
          title: '是否自动续期',
          align: 'center',
          valign: 'middle',
          formatter:auto_charge
      },{

          field: 'reward_status',
          title: '奖品状态',
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
                '/admin/goods/reward/auto_charge',
                '/admin/goods/reward/status',
                '/admin/goods/reward/delete'
        ]
        var opList = []
        for (var i = 0; i < rowobj['op'].length; ++i) {
            var op = rowobj['op'][i];
            var str = JSON.stringify({reward_id : rowobj['reward_id']});
            var cStr = str.replace(/\"/g, "@");
            if(comfirmUrls.indexOf(op['url']) !=-1){
                opList.push(String.format("<a href=\"#\" class=\"btn btn-primary\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"> {3}</a> ", op['url'], op['method'], cStr, op['txt']));
            }else{
                opList.push(String.format("<a href=\"{0}?reward_id="+rowobj['reward_id']+"\" class=\"btn btn-primary\" >{1}</a> ", op['url'],op['txt']));
            }
        }
        return opList.join('');
    }

    function status(value,row,index){
        eval('var rowobj='+JSON.stringify(row))
        var statusstr = '';
        if(parseInt(rowobj['reward_status']) == 0){
            statusstr = '<span class="label label-danger">下架</span>';
        }else if(parseInt(rowobj['reward_status']) == 1){
            statusstr = '<span class="label label-success">上架</span>';
        }

        return [
            statusstr
        ].join('');
    }

    function reward_type(value,row,index){
        eval('var rowobj='+JSON.stringify(row))
        reward_types = {
                0    :  '手机',
                1    :  '话费',
                2    :  '家用电器',
                3    :  '生活用品',
                4    :  '电子产品',
        }
        var statusstr = reward_types[rowobj['reward_type']];

        return [statusstr].join('');
    }

    function auto_charge(value,row,index){
        eval('var rowobj='+JSON.stringify(row))
        var statusstr = '';
        if(rowobj['reward_auto_charge'] == 0){
            statusstr = '<span class="label label-danger">否</span>';
        }else if(rowobj['reward_auto_charge'] == 1){
            statusstr = '<span class="label label-success">是</span>';
        }

        return [
            statusstr
        ].join('');
    }

    function responseFunc(res){

        return res;
    }

    function responseError(status) {
        location.reload();
    }
</script>
%rebase admin_frame_base
