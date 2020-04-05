<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
      <div class="block">
                %include admin_frame_header

                <div class="panel panel-default" style="width:40%;float: left;">
                    <div class="panel-heading">
                        <button id='refresh_yuanbao_gold_value_button'>点击显示当前数据</button>
                    </div>
                    <div class="panel-body" >
                        <table id='current_yuanbao_gold_value_table' class="table table-bordered table-hover;"></table>
                        <br/>
                        <br/>
                        <h4 align='center'>全服金币排行<h4>
                        <table id='user_gold_rank_table' class="table table-bordered table-hover;"></table>
                        <br/>
                        <br/>
                        <h4 align='center'>全服元宝排行<h4>
                        <table id='user_yuanbao_rank_table' class="table table-bordered table-hover;"></table>                        
                    </div>
                </div>

                <div class="content">
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
</div>

<script type="text/javascript">

var firstDate=new Date();

function initTable()
{
    
    startDate = $("#pick-date-start").val();
    endDate   = $("#pick-date-end").val();
    var pageNumber;
   $('#dataTable').bootstrapTable
     ({
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
                field: 'value_of_gold_that_players_own',
                title: '玩家当天拥有金币价值',
                align: 'center',
                valign: 'middle'
            }, 
          {
                field: 'value_of_yuanbao_that_players_own',
                title: '玩家当天拥有元宝价值',
                align: 'center',
                valign: 'middle'
            },             
          {
                field: 'total_population_golden_house',
                title: '参与金币场总人数',
                align: 'center',
                valign: 'middle'
            },  
          {
                field: 'total_population_match_house',
                title: '参与比赛场总人数',
                align: 'center',
                valign: 'middle'
            },  
          {
                field: 'total_qty_of_games_in_golden_house',
                title: '金币场总局数',
                align: 'center',
                valign: 'middle'
            },
          {
                field: 'total_qty_of_games_in_match_house',
                title: '比赛场总局数',
                align: 'center',
                valign: 'middle'
            },                
          {
                field: 'volatility_of_gold_coin',
                title: '玩家波动金额',
                align: 'center',
                valign: 'middle'
            },
          {
                field: 'total_value_of_active_in_gold_and_compete',
                title: '金币场比赛场活跃人数总金币',
                align: 'center',
                valign: 'middle'
            },
          {
                field: 'total_wave_value_of_active_in_gold_and_compete',
                title: '金币场比赛场活跃人数金币波动',
                align: 'center',
                valign: 'middle'
            },
          {
                field: 'value_of_reward_that_player_redeem',
                title: '玩家兑换奖励价值总额',
                align: 'center',
                valign: 'middle'
            },            
          {
                field: 'amount_of_recharge_gold_coin',
                title: '充值金币数',
                align: 'center',
                valign: 'middle'
            },
          {
                field: 'amount_of_recharge_yuan_bao',
                title: '充值元宝数',
                align: 'center',
                valign: 'middle'
            },

          {
                field: 'total_cash_value_of_recharge',
                title: '充值总价值金额',
                align: 'center',
                valign: 'middle'
            }, 
          {
                field: 'income_value_of_player_change',
                title: '玩家转换货币的收入价值',
                align: 'center',
                valign: 'middle'
            },
            {
                field: 'income_value_of_tool_that_activity_cost',
                title: '活动（抽奖）消耗货币道具价值',
                align: 'center',
                valign: 'middle'                 
            },
            
            {
                field: 'income_value_of_tool_that_purchase',
                title: '道具购买收入价值',
                align: 'center',
                valign: 'middle'                 
            },            
  
 
          {
                field: 'income_total_value_from_golden_house_fee',
                title: '金币场房费收入价值',
                align: 'center',
                valign: 'middle'
            },
          {
                field: 'income_total_value_from_competition_house_fee_yuanbao',
                title: '比赛场房费收入价值(元宝)',
                align: 'center',
                valign: 'middle'
          },
//          {
//                field: 'total_value_from_competition_house_fee_gold',
//                title: '比赛场房费收入价值(金币)',
//                align: 'center',
//                valign: 'middle'
//           },
//          {
//                field: 'total_value_from_competition_house_fee_roomCard',
//                title: '比赛场房费收入价值(钻石)',
//                align: 'center',
//                valign: 'middle'
//           },           
//         {
//               field: 'total_value_from_competition_house_fee_redpacket',
//                title: '比赛场房费收入价值(红包)',
//                align: 'center',
//                valign: 'middle'
//           },           
          {
                field: 'income_total_value_from_competition_house_register_fee_roomCard',
                title: '比赛场报名费收入价值(钻石)',
                align: 'center',
                valign: 'middle'
           },

          {
                field: 'income_total_value_from_competition_house_register_fee_gold',
                title: '比赛场报名费收入价值(金币)',
                align: 'center',
                valign: 'middle'
           },
          {
                field: 'income_total_value_from_competition_house_register_fee_yuanbao',
                title: '比赛场报名费收入价值(元宝)',
                align: 'center',
                valign: 'middle'
           },
          {
                field: 'income_from_insurance_box',
                title: '保险箱收入手续费',
                align: 'center',
                valign: 'middle'
           },
//          {
//                field: 'total_value_from_competition_house_register_fee_redpacket',
//                title: '比赛场报名费收入价值(红包)',
//                align: 'center',
//                valign: 'middle'
//           },
          {
                field: 'fee_value_back_to_creator_of_club',
                title: '返利俱乐部创建人（10%）',
                align: 'center',
                valign: 'middle'
           },           
          {
                field: 'fee_value_back_to_agent_level_1',
                title: '返利一级代理（10%）',
                align: 'center',
                valign: 'middle'
           },            
          {
                field: 'fee_value_back_to_relaship_between_updown',
                title: '返利上下级绑定关系',
                align: 'center',
                valign: 'middle'
           },            
            {
                field: 'fee_value_that_pay_commission_to_platform',
                title: '支付平台手续费用',
                align: 'center',
                valign: 'middle'
            },
           {
                field: 'fee_total_welfare_expenditure_gold',
                title: '福利支出(金币)',
                align: 'center',
                valign: 'middle'
           },          
          {
                field: 'fee_total_welfare_expenditure_vcoin',
                title: '福利支出(元宝)',
                align: 'center',
                valign: 'middle'
           },
          {
                field: 'fee_total_welfare_expenditure_bag',
                title: '福利支出(背包)',
                align: 'center',
                valign: 'middle'
           },
           {
                field: 'fee_total_reward_expenditure_gold',
                title: '奖励支出(金币)',
                align: 'center',
                valign: 'middle'
           },          
          {
                field: 'fee_total_reward_expenditure_yuanbao',
                title: '奖励支出(元宝)',
                align: 'center',
                valign: 'middle'
           },
          {
                field: 'fee_total_reward_expenditure_redpacket',
                title: '奖励支出(红包)',
                align: 'center',
                valign: 'middle'
           },
          {
                field: 'fee_total_reward_expenditure_roomCard',
                title: '奖励支出(钻石)',
                align: 'center',
                valign: 'middle'
           },
          {
                field: 'fee_special_fee',
                title: '特殊支出(元)',
                align: 'center',
                valign: 'middle',
                formatter:get_special_fee,
           },
          {
                field: 'income_value_of_AI_fluctuating_gold_coin',
                title: 'AI波动金币价值（赢-输的价值）',
                align: 'center',
                valign: 'middle'
           },
          {
                field: 'income_value_of_AI_fluctuating_gold_coin_levelA_baoji',
                title: 'A档（AI）波动金币价值（暴击场)',
                align: 'center',
                valign: 'middle'
           },
          {
                field: 'profit_of_today',
                title: '当天盈利值（收入总值-支出总值）',
                align: 'center',
                valign: 'middle'
           },
           {
                field: 'profit_of_journal',
                title: '当天流水盈利值',
                align: 'center',
                valign: 'middle'
           },
           {
                field: 'the_tax_rate',
                title: '税率',
                align: 'center',
                valign: 'middle'
           }           

           ]
     });

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
}

    function on_update_special_fee(row,row_date)
    {
        var input_value = row.parentNode.childNodes[0].value;
        var input_obj = row.parentNode.childNodes[0];
        //table_type 0 表示运营表 1 表示活跃玩家运营表
        var href_str = "/admin/gold/update_special_value?update_s_v=1&data_date=" + row_date + "&value=" + input_value +"&table_type=0";
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

    var gold_yuanbao_dic = {
            method: 'get',
            sortable:false,
            columns:[
        {
            field: 'gold',
            title: '总金币数',
            align: 'center',
            valign: 'middle',
            sortable: true,
        },{

            field: 'yuanbao',
            sortable: true,
            title: '总元宝数',
            align: 'center',
            valign: 'middle',
            sortable: true,
        },              
     
        ],
        data: 
        [
               {}
        ]            
            
        }

     $("#current_yuanbao_gold_value_table").bootstrapTable(gold_yuanbao_dic);

    var user_rank_dic = 
    {
            method: 'get',
            sortable:false,
            columns:[
                {
                    field: 'user_id',
                    title: '用户id',
                    align: 'center',
                    valign: 'middle',
                    sortable: false,
                },
                {
                    field: 'user_gold',
                    title: '用户金币数',
                    align: 'center',
                    valign: 'middle',
                    sortable: false,
                },
                {
                    field: 'user_yuanbao',
                    title: '用户元宝数',
                    align: 'center',
                    valign: 'middle',
                    sortable: false,
                },
            ],
            data:
            [
                {}
            ]
    } 
    $("#user_gold_rank_table").bootstrapTable(user_rank_dic);
    $("#user_yuanbao_rank_table").bootstrapTable(user_rank_dic);


$("#refresh_yuanbao_gold_value_button").click(function (){
    var opt = {
        url: "/admin/gold/get_yuanbao_gold_value",
    };

    $("#current_yuanbao_gold_value_table").bootstrapTable('refresh', opt);

    var opt_gold_rank = 
    {
        url: "/admin/gold/get_user_gold_rank_whole_server",
    };
    $("#user_gold_rank_table").bootstrapTable('refresh', opt_gold_rank);    

    var opt_yuanbao_rank = 
    {
        url: "/admin/gold/get_user_yuanbao_rank_whole_server",
    };
    $("#user_yuanbao_rank_table").bootstrapTable('refresh', opt_yuanbao_rank);    
});     

</script>
%rebase admin_frame_base