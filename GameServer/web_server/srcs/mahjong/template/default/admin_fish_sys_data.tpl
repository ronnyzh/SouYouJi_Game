<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<div class="block">
          %include admin_frame_header
          <div class="content">
              %include original_search_bar
              <table id="dataTable" class="table table-bordered table-hover"></table>
          </div>
</div>
<script type="text/javascript">
  /**
    * 服务端刷新表格
    --------------------------------------------
  */
  function initTable() {
      startDate = $("#pick-date-start").val();
      endDate   = $("#pick-date-end").val();
      $('#dataTable').bootstrapTable({
          method:'get',
          url   :'{{info["listUrl"]}}',
          contentType: "application/json",
          smartDisplay: true,
          pagination: true,
          pageSize: 15,
          showRefresh: true,
          showExport: true,
          pageList: [15, 50, 100, 'All'],
          queryParams:getSearchP,
          showFooter:true,
          responseHandler:responseFunc,
          columns: [
              [{
                    "title": "基本数据统计",
                    "halign":"center",
                    "align":"center",
                    "colspan": 12
              }],
              [{
                    "title": "总人数: "+{{total_member}},
                    "halign":"center",
                    "align":"center",
                    "colspan": 1,
                    "bgcolor":"#000"
              },{
                    "title": "每日注册: "+{{reg_per_day}},
                    "halign":"center",
                    "align":"center",
                    "colspan": 1
              },{
                    "title": "每日活跃: "+{{log_per_day}},
                    "halign":"center",
                    "align":"center",
                    "colspan": 1
              },{
                    "title": "日均活跃: "+{{login_per_rate}},
                    "halign":"center",
                    "align":"center",
                    "colspan": 1
              },{
                    "title": "日均充值: "+{{recharge_per_rate}},
                    "halign":"center",
                    "align":"center",
                    "colspan": 1
              },{
                    "title": "总分享次数: "+{{total_share}}+" <br/>每日分享次数: "+{{share_per_day}},
                    "align":"center",
                    "colspan": 1
              }],
                    [{
                          "title": "搜索日期:"+startDate+"至"+endDate,
                          "halign":"center",
                          "align":"center",
                          "colspan": 12
                    }],
                    [{
                        field: 'today',
                        title: '日期',
                        align: 'center',
                        valign: 'middle',
                        sortable: true,
                        footerFormatter:function(values){
                            return '详细统计:'
                        }
                    },{
                        field: 'today_reg',
                        title: '当日注册',
                        align: 'center',
                        valign: 'middle',
                        sortable: true,
                        footerFormatter:function(values){
                            var count = 0;
                            for (var val in values){
                                count+=parseInt(values[val].today_reg);
                            }

                            return colorFormat(count)
                        }
                    },{
                        field: 'today_active',
                        title: '当日活跃',
                        align: 'center',
                        valign: 'middle',
                        sortable: true,
                        footerFormatter:function(values){
                            var count = 0;
                            for (var val in values){
                                count+=parseInt(values[val].today_active);
                            }

                            return colorFormat(count);
                        }
                    },{
                        field: 'today_sys_user_total',
                        title: '当日充值人数',
                        align: 'center',
                        valign: 'middle',
                        sortable: true,
                        footerFormatter:function(values){
                            var count = 0;
                            for (var val in values){
                                count+=parseInt(values[val].today_sys_user_total);
                            }

                            return colorFormat(count);
                        }
                    },{
                        field: 'today_sys_coin_total',
                        title: '当日总充值金额(元s)',
                        align: 'center',
                        valign: 'middle',
                        sortable: true,
                        formatter:getColor,
                        footerFormatter:function(values){
                            var count = 0;
                            for (var val in values){
                                count+=parseInt(values[val].today_sys_coin_total);
                            }

                            return colorFormat(count);
                        }
                    },{
                        field: 'average_val',
                        title: '平均价值',
                        align: 'center',
                        valign: 'middle',
                        sortable: true,
                        formatter:getColor,
                        footerFormatter:function(values){
                            for(var val in values){
                                var money_total = values[val].money_total;
                                break;
                            }

                            return '历史总充值:'+colorFormat(money_total);
                        }
                    }]]
      });

          function getSearchP(p){
                startDate = $("#pick-date-start").val();
                endDate   = $("#pick-date-end").val();
                sendParameter = p;
                sendParameter['start_date'] = startDate;
                sendParameter['end_date']   = endDate;
                return sendParameter;
          }

          function responseFunc(res){
              data = res.data;

              return data;
          }
    }
</script>
%rebase admin_frame_base
