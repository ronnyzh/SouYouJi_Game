<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
  <div class="block">
            %include admin_frame_header
            <div class="content">
               <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
          <div class='col-sm-12' style='margin-left:1em;'>
                  <div style='float:left;margin-left:1em;' class="input-group date datetime col-md-1 col-xs-1"data-min-view="2" data-date-format="yyyy-mm-dd">
                    <input class="form-control" size="12" type="text" style='width:140px;height:28px;' id='pick-date-start' name="startdate" value="{{lang.INPUT_LABEL_START_DATE_TXT}}" readonly>
                    <span class="input-group-addon btn btn-primary pickdate-btn"><span class="glyphicon pickdate-btn pickdate glyphicon-th"></span>
                  </div>

                  <div style='float:left;margin-left:1em;' class="input-group date datetime col-md-1 col-xs-1"  data-min-view="2" data-date-format="yyyy-mm-dd">
                    <input class="form-control" style='width:140px;height:28px;' id='pick-date-end' name="enddate" size="12" type="text" value="{{lang.INPUT_LABEL_END_DATE_TXT}}" readonly>
                    <span class="input-group-addon btn btn-primary pickdate-btn"><span class="pickdate glyphicon pickdate-btn glyphicon-th"></span></span>
                  </div>
                  <div style='float:left;margin-left:1em;'>
                          <button id="btn_query" class='btn btn-primary btn-sm btn-xs'><i class='fa fa-search'></i>{{lang.INPUT_LABEL_QUERY}}</button>
                          <button id="btn_lastMonth" class='btn btn-sm btn-xs'>{{lang.INPUT_LABEL_PREV_MONTH}}</button>
                          <button id="btn_thisMonth" class='btn btn-sm btn-xs '>{{lang.INPUT_LABEL_CURR_MONTH}}</button>
                          <button id="btn_lastWeek" class='btn btn-sm btn-xs '>{{lang.INPUT_LABEL_PREV_WEEK}}</button>
                          <button id="btn_thisWeek" class='btn btn-sm btn-xs'>{{lang.INPUT_LABEL_CURR_WEEK}}</button>
                          <button id="btn_yesterday" class='btn btn-sm btn-xs'>{{lang.INPUT_LABEL_PREV_DAY}}</button>
                          <button id="btn_today" class='btn btn-sm btn-xs'>{{lang.INPUT_LABEL_CURR_DAY}}</button>
                          <button id="btn_z" class='btn btn-primary btn-sm btn-xs'><i class='fa fa-search'></i>元宝总表</button>
                         <div class='clearfix'></div>
                  </div>
          </div>
</div>
<!-- 初始化搜索栏的日期 -->
<script type="text/javascript">
var firstDate=new Date();
    firstDate.setDate(firstDate.getDate()-6);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));
    $('#btn_z').click(function(){
        window.location.href = "/admin/bag/vcoin/sum"
    })
</script>

               <table id="dataTable" class="table table-bordered table-hover"></table>
            </div>
  </div>
<script type="text/javascript">

  function initTable() {
    $('#dataTable').bootstrapTable({
          method: 'get',
          url: '{{info["listUrl"]}}',
          contentType: "application/json",
          datatype: "json",
          cache: false,
          checkboxHeader: true,
          striped: true,
          pagination: true,
          pageSize: 15,
          showExport: true,
          exportTypes:['excel', 'csv', 'pdf', 'json'],
          pageList: [15,50,100,'All'],
          search: true,
          clickToSelect: true,
          //sidePagination : "server",
          sortOrder: 'desc',
          sortName: 'date',
          queryParams:getSearchP,
          responseHandler:responseFun,
          showFooter:true, //添加页脚做统计
          //onLoadError:responseError,
          showExport:true,
          exportTypes:['excel', 'csv', 'pdf', 'json'],
          // exportOptions:{fileName: "{{info['title']}}"+"_"+ new Date().Format("yyyy-MM-dd")},
          columns: [
          {
              field: 'date',
              title: '日期',
              align: 'center',
              valign: 'middle'
          },{
              field: 'day_join_num',
              title: '当天参与人数',
              align: 'center',
              valign: 'middle',
              sortable:true,
          },{
              field: 'day_round',
              title: '当天局数',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{
              field: 'day_send_redbag',
              title: '当天发放红包',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{
              field: 'day_send_vcoin',
              title: '当天发放元宝',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{
              field: 'day_present_redbag',
              title: '当天赠送元宝数量',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{
              field: 'day_room_fee',
              title: '当天房费',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{
              field: 'b_robot_change',
              title: 'B档机器人元宝变化',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{
              field: 'd_robot_change',
              title: 'D档机器人元宝变化',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{
              field: 'diamond_to_vcoin_num',
              title: '钻石转元宝数',
              align: 'center',
              valign: 'middle',
              sortable:true
          },{
              field: 'player_claim_redbag_cash',
              title: '玩家兑换红包价值',
              align: 'center',
              valign: 'middle',
              sortable:true
          }],
          onExpandRow: function (index, row, $detail) {
              console.log(index,row,$detail);
              InitSubTable(index, row, $detail);
          }
      });



        //定义列操作
        function getSearchP(p){
          startDate = $("#pick-date-start").val();
          endDate   = $("#pick-date-end").val();

          sendParameter = p;

          sendParameter['startDate'] = startDate;
          sendParameter['endDate']  = endDate;

          return sendParameter;
        }


        //获得返回的json 数据

        function responseFun(res){

            data = res.data
            return data;
        }
}
</script>




<div class='content'>
      <form class='form-horizontal group-border-dashed' action="{{info['submitUrl']}}" method='POST' id='selfModify'>
       <div class="form-group">
            <label class="col-sm-5 col-xs-10 control-label">玩家持有元宝最小值</label>
            <div class="col-sm-6 col-xs-12">
                  <input type='text' style='width:100%;float:left' name='min_possess_value' value="{{min_possess_value}}" data-rules="{required:true}" class="form-control">
            </div>
       </div>

       <div class="form-group">
            <label class="col-sm-5 col-xs-10 control-label">玩家持有元宝最大值</label>
            <div class="col-sm-6 col-xs-12">
                  <input type='text' style='width:100%;float:left' name='max_possess_value'  value="{{max_possess_value}}" data-rules="{required:true}" class="form-control">
            </div>
       </div>

       <div class="form-group">
            <label class="col-sm-5 col-xs-10 control-label">当天进行游戏局数上限</label>
            <div class="col-sm-6 col-xs-12">
                  <input type='text' style='width:100%;float:left' name='max_round_value'  value="{{max_round_value}}" data-rules="{required:true}" class="form-control">
            </div>
       </div>

       <div class="form-group">
            <label class="col-sm-5 col-xs-10 control-label">触发好牌机率</label>
            <div class="col-sm-6 col-xs-12">
                  <input type='text' style='width:100%;float:left' name='good_hand_per'  value="{{good_hand_per}}" data-rules="{required:true}" class="form-control">
            </div>
       </div>

       <div class="modal-footer" style="text-align:center">
           <button type="submit" class="btn btn-sm btn-xs btn-primary btn-mobile">确认</button>
       </div>


</form>
</div>
%rebase admin_frame_base
