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
              field: 'round_sum',
              title: '总局数',
              align: 'center',
              valign: 'middle'
          },{
              field: 'join_people_sum',
              title: '总参人数',
              align: 'center',
              valign: 'middle',
              sortable:true,
          },{
              field: 'send_redbag_sum',
              title: '总共发放红包',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{
              field: 'send_vcoin_sum',
              title: '总共发放元宝',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{
              field: 'present_redbag_sum',
              title: '赠送元宝数量总数',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{
              field: 'room_fee_sum',
              title: '总房费',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{
              field: 'b_robot_change_sum',
              title: 'B档机器人元宝变化',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{
              field: 'd_robot_change_sum',
              title: 'D档机器人元宝变化',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{
              field: 'gold_to_vcoin_sum',
              title: '金币转元宝数',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{
              field: 'player_claim_redbag_cash_sum',
              title: '玩家兑换红包价值',
              align: 'center',
              valign: 'middle',
              sortable:true
          }]]
    });




</script>
%rebase admin_frame_base