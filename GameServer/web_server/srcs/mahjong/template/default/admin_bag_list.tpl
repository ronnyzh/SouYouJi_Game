<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<div class='block'>
    %include admin_frame_header
    <div class='content'>
        <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
            <a id="add" href="{{info["createUrl"]}}" style='color:#FFF;text-decoration:none;'>
                <button id="btn_add" type="button" class="btn btn-sm btn-primary">
                    <i class="glyphicon glyphicon-plus"> {{info['addTitle']}} </i>
                </button>
            </a>
        </div>
        <table id='dataTable' class="table table-bordered table-hover table-striped"></table>
    </div>
</div>
<script type="text/javascript">

    $('#dataTable').bootstrapTable({
          method: 'get',
          url: '{{info["listUrl"]}}',
          contentType: "application/json",
          datatype: "json",
          cache: false,
          striped: true,
          search:true,
          toolbar:'#toolbar',
          pagination: true,
          pageSize: 15,
          pageList: [15, 50, 100],
          search: true,
          showRefresh: true,
          minimumCountColumns: 2,
          clickToSelect: true,
          showExport: true,
          exportTypes: ['excel', 'csv', 'pdf', 'json'],
          columns: [
          [{
              field: 'item_id',
              title: '道具ID',
              align: 'center',
              valign: 'middle',
              sortable: true
          },{
              field: 'title',
              title: '道具名称',
              align: 'center',
              valign: 'middle'
          },{
              field: 'icon',
              title: '道具图标',
              align: 'center',
              valign: 'middle',
              formatter:getIcon,
          },{
              field: 'des',
              title: '道具描述',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'price',
              title: '道具价格',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'times',
              title: '道具有效次数',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'days',
              title: '道具有效天数',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'is_delete',
              title: '状态',
              align: 'center',
              valign: 'middle',
              sortable: true,
              formatter:is_valid
          },{
              field: 'is_goods',
              title: '商城可否购买',
              align: 'center',
              valign: 'middle',
              sortable: true,
              formatter:can_buy
          },{
              field: 'can_use',
              title: '可否使用',
              align: 'center',
              valign: 'middle',
              sortable: true,
              formatter:can_used
          },{
              field: 'bag_show',
              title: '是否显示在背包中',
              align: 'center',
              valign: 'middle',
              sortable: true,
              formatter:bag_show
          },{
              field: 'unit',
              title: '单位',
              align: 'center',
              valign: 'middle',
              sortable: true,
              formatter:show_unit
          },{
              field: 'can_reward',
              title: '是否可兑奖',
              align: 'center',
              valign: 'middle',
              sortable: true,
              formatter:show_reward
          },{
              field: 'op',
              title: '操作',
              align: 'left',
              valign: 'middle',
              formatter:getOp
          }]]
    });


      function getIcon(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          statusstr = '<img src="'+row['icon']+'" width="30" height="30" />';
          return [statusstr].join('');
       }


      function is_valid(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          var statusstr = '';
          if(rowobj['is_delete'] == '0'){
              statusstr = '<span class="label label-success">正常</span>';
          }else if(rowobj['is_delete'] == '1'){
              statusstr = '<span class="label label-danger">删除</span>';
          }
          return [
              statusstr
          ].join('');
      }

      function can_buy(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          var statusstr = '';
          if(rowobj['is_goods'] == '0'){
              statusstr = '<span class="label label-danger">不可购买</span>';
          }else if(rowobj['is_goods'] == '1'){
              statusstr = '<span class="label label-success">可购买</span>';
          }
          return [
              statusstr
          ].join('');
      }

      function show_unit(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          var statusstr = '';
          if(rowobj['unit'] == '0'){
              statusstr = '<span class="label label-danger">个</span>';
          }else if(rowobj['unit'] == '1'){
              statusstr = '<span class="label label-success">元</span>';
          }
          return [
              statusstr
          ].join('');
      }

      function show_reward(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          var statusstr = '';
          if(rowobj['can_reward'] == '0'){
              statusstr = '<span class="label label-danger">不可兑奖</span>';
          }else if(rowobj['can_reward'] == '1'){
              statusstr = '<span class="label label-success">可兑奖</span>';
          }
          return [
              statusstr
          ].join('');
      }

      function can_used(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          var statusstr = '';
          if(rowobj['can_use'] == '0'){
              statusstr = '<span class="label label-danger">不可使用</span>';
          }else if(rowobj['can_use'] == '1'){
              statusstr = '<span class="label label-success">可以使用</span>';
          }
          return [
              statusstr
          ].join('');
      }

      function bag_show(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          var statusstr = '';
          if(rowobj['bag_show'] == '0'){
              statusstr = '<span class="label label-danger">不显示</span>';
          }else if(rowobj['bag_show'] == '1'){
              statusstr = '<span class="label label-success">显示</span>';
          }
          return [
              statusstr
          ].join('');
      }

      function getOp(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          var a2,a3,a4,a5;
          if(rowobj['is_delete']=='0'){
             a2 = "<a class='btn btn-primary' href='/admin/bag/item/changeI?item_id="+rowobj['item_id']+"&ci=1'>删除</a>"
          }else{
             a2 = "<a class='btn btn-primary' href='/admin/bag/item/changeI?item_id="+rowobj['item_id']+"&ci=0'>恢复</a>"
          }

          if(rowobj['is_goods']=='0'){
             a3 = "<a class='btn btn-primary' href='/admin/bag/item/isgoods?item_id="+rowobj['item_id']+"&ig=1'>允许购买</a>"
          }else{
             a3 = "<a class='btn btn-primary' href='/admin/bag/item/isgoods?item_id="+rowobj['item_id']+"&ig=0'>禁止购买</a>"
          }

          if(rowobj['can_use']=='0'){
             a4 = "<a class='btn btn-primary' href='/admin/bag/item/can_use?item_id="+rowobj['item_id']+"&cu=1'>允许使用</a>"
          }else{
             a4 = "<a class='btn btn-primary' href='/admin/bag/item/can_use?item_id="+rowobj['item_id']+"&cu=0'>禁止使用</a>"
          }

          if(rowobj['bag_show']=='0'){
             a5 = "<a class='btn btn-primary' href='/admin/bag/item/bag_show?item_id="+rowobj['item_id']+"&bs=1'>设置显示</a>"
          }else{
             a5 = "<a class='btn btn-primary' href='/admin/bag/item/bag_show?item_id="+rowobj['item_id']+"&bs=0'>设置不显示</a>"
          }

          res = "<a href='/admin/bag/item/modify?item_id="+rowobj['item_id']+"' class='btn btn-primary'>修改</a>"+a2+a3+a4+a5
          return [
            res
          ].join('');
      }

</script>
%rebase admin_frame_base