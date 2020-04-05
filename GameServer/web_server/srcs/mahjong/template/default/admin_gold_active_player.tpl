<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<div class="block">
    %include admin_frame_header
    %include original_search_bar
    <script>
        <!-- 初始化搜索栏的日期 -->
        var firstDate=new Date();
        var endDate = new Date();
        firstDate.setDate(firstDate.getDate()-7);
        endDate.setDate(endDate.getDate() - 1);
        $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
        $('#pick-date-end').val(endDate.Format("yyyy-MM-dd"));
     </script>
    <table id="dataTable" class="table table-bordered table-hover"></table>
</div>

<script>
function initTable()
{
   $('#dataTable').bootstrapTable(
       {
           method: 'get',
           url: '{{info["listUrl"]}}',
           showFooter:false,
           striped: true,
           pagination: true,
           pageSize: 15,
           showExport: true,
           queryParams:getSearchP,
           responseHandler:responseFun,
           search: true,
           columns:
           [
               {
                    field: 'date',
                    title: '日期',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
              },               
               {
                    field: 'population_of_players_in_gold',
                    title: '参与金币场总人数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
              }, 
               {
                    field: 'population_of_players_in_match',
                    title: '参与比赛场总人数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
              },     
               {
                    field: 'total_round_in_gold',
                    title: '金币场总局数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
              },  
               {
                    field: 'total_qty_of_games_in_match_house',
                    title: '比赛场总局数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
              }, 
               {
                    field: 'total_value_of_active_in_gold_and_compete',
                    title: '金币场比赛场活跃人数总金币',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
              },
               {
                    field: 'total_wave_value_of_active_in_gold_and_compete',
                    title: '金币场比赛场活跃人数金币波动',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
              },                             
               {
                    field: 'amount_of_recharge_yuan_bao',
                    title: '充值元宝数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
              },      
              {
                    field: 'amount_of_recharge_gold_coin',
                    title: '充值金币数',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,
              }, 
              {
                    field: 'total_cash_value_of_recharge',
                    title: '充值总价值',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,                  
              },
              {
                    field: 'income_total_value_from_golden_house_fee',
                    title: '金币场房费收入价值',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,                   
              },
             {
                    field: 'income_total_value_from_competition_house_fee_yuanbao',
                    title: '比赛场房费收入价值（元宝）',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,                   
              },
              {
                    field: 'income_total_value_from_competition_house_register_fee_roomCard',
                    title: '比赛场报名费收入价值(钻石)',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,                   
              },
              {
                   field: 'income_total_value_from_competition_house_register_fee_gold',
                   title: '比赛场报名费收入价值(金币)',
                   align: 'center',
                   valign: 'middle',
                   sortable: true,                   
              },
              {
                   field: 'income_total_value_from_competition_house_register_fee_yuanbao',
                   title: '比赛场报名费收入价值(元宝)',
                   align: 'center',
                   valign: 'middle',
                   sortable: true,                   
              },              
              {
                   field: 'fee_total_welfare_expenditure_gold',
                   title: '福利支出(金币)',
                   align: 'center',
                   valign: 'middle',
                   sortable: true,                   
              },          
              {
                   field: 'fee_total_welfare_expenditure_vcoin',
                   title: '福利支出(元宝)',
                   align: 'center',
                   valign: 'middle',
                   sortable: true,                   
               },
               {
                   field: 'fee_total_welfare_expenditure_bag',
                   title: '福利支出(背包)',
                   align: 'center',
                   valign: 'middle',
                   sortable: true,                   
               },              
               {
                   field: 'fee_total_reward_expenditure_gold',
                   title: '奖励支出(金币)',
                   align: 'center',
                   valign: 'middle',
                   sortable: true,                   
               },          
               {
                   field: 'fee_total_reward_expenditure_yuanbao',
                   title: '奖励支出(元宝)',
                   align: 'center',
                   valign: 'middle',
                   sortable: true,                   
               },
               {
                   field: 'fee_total_reward_expenditure_redpacket',
                   title: '奖励支出(红包)',
                   align: 'center',
                   valign: 'middle',
                   sortable: true,                   
               },
               {
                   field: 'fee_total_reward_expenditure_roomCard',
                   title: '奖励支出(钻石)',
                   align: 'center',
                   valign: 'middle',
                   sortable: true,                   
              },
              {
                    field: 'fee_special_fee',
                    title: '特殊奖励支出',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,                   
                    formatter:get_special_fee,
              },                           
              {
                    field: 'income_value_of_AI_fluctuating_gold_coin',
                    title: 'AI波动金币价值（赢-输的价值）',
                    align: 'center',
                    valign: 'middle'
              },
              {
                    field: 'profit_of_today',
                    title: '当天盈利',
                    align: 'center',
                    valign: 'middle',
                    sortable: true,                   
              },                              
  
           ]
       }
   );
}
           //定义列操作
        function getSearchP(p){
          //alert('getSerachP')
          startDate = $("#pick-date-start").val();
          endDate   = $("#pick-date-end").val();

          sendParameter = p;

          sendParameter['startDate'] = startDate;
          sendParameter['endDate']  = endDate;

          return sendParameter;
        }
        function responseFun(res){
            var data = res;
            return data;
        }
        function get_special_fee(value,row,index)
        {
            var row_date = row.date;
            return '<div><input placeholder="' + row['fee_special_fee'] + '"></input><button onclick="on_update_special_fee(this,' +"'" + row_date +"');" + '">修改</button></div>'
        }       
        function on_update_special_fee(row,row_date)
        {
            var input_value = row.parentNode.childNodes[0].value;
            var input_obj = row.parentNode.childNodes[0];
            var href_str = "/admin/gold/update_special_value?update_s_v=1&data_date=" + row_date + "&value=" + input_value + '&table_type=1';
            if(trim(input_value)==null || trim(input_value)=="")
            {
                alert("请填入内容");
                input_obj.focus();
                return false;
            }                
            if(checkNumber(input_value) == false)
            {
                alert("请输入数字");
                input_obj.focus();
                return false;
            }
            window.location.href = href_str;
        }         
        function trim(str)
        { 
            //删除左右两端的空格
    　　     return str.replace(/(^\s*)|(\s*$)/g, "");
        } 
        //验证字符串是否是数字
        function checkNumber(theObj) 
        {
        
            var reg = /^(-?\d+)(\.\d+)?$/;
            if (reg.test(theObj)) 
            {
               return true;
            }
            return false;
        } 
</script>

%rebase admin_frame_base