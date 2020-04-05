<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
      <div class="block">
                %include admin_frame_header
                <div class="content">
                    <table id="dataTable" class="table table-bordered table-hover"></table>
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
          columns: [
          [{
              field: 'cid',
              title: 'ID',
              align: 'center',
              valign: 'middle',
              sortable: true
          },{
              field: 'name',
              title: '名称',
              align: 'center',
              valign: 'middle'
          },{
              field: 'cost_type',
              title: '消耗类型',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'cost',
              title: '消耗数量',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'gain_type',
              title: '获取类型',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'gain',
              title: '获取数量',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'gain_title',
              title: '获取类型名称',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'cost_title',
              title: '消耗类型名称',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'big_type_id',
              title: '大类id',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'big_type_title',
              title: '大类名称',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'op',
              title: '操作',
              align: 'center',
              valign: 'middle',
              formatter:getOp
          }]]
    });


      function getOp(value,row,index){
          eval('var rowobj='+JSON.stringify(row))

          res = "<a href='/admin/bag/exchange/del?cid="+rowobj['cid']+"' class='btn btn-primary'>删除</a>"
          res = "<a href='/admin/bag/exchange/del?cid="+rowobj['cid']+"' class='btn btn-primary'>删除</a><a href='/admin/bag/exchange/modify?cid="+rowobj['cid']+"' class='btn btn-primary'>修改</a>"

          return [
            res
          ].join('');
      }

</script>
%rebase admin_frame_base
<script>
    if("{{op_res}}"=="1"){
        alert("修改成功！")
    }else if("{{op_res}}"=="2"){
        alert("修改失败！")
    }
</script>