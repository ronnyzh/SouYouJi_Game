<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
  <div class="block">
            %include admin_frame_header
            <table class="table table-bordered table-hover" style="width:20%;float: left;">
            <thead>
                <tr>
                <th>总当前在线人数</th>
                <th>总当前房间数</th>
                <th>玩家当前拥有金币总数</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                <td>{{info['online_people_sum']}}</td>
                <td>{{info['online_room_num']}}</td>
                <td>{{info['user_current_gold_sum']}}</td>
                </tr>
                
            </tbody>
            </table>
            <div style='margin-left: 5%;float: left;margin-top: 20px;'>
                <button id='classic' type="button" class="btn btn-primary">经典牛牛</button>
                <button id='open_hand' type="button" class="btn btn-primary">明牌牛牛</button>
                <button id='joy' type="button" class="btn btn-primary">欢乐牛牛</button>
                <button id='game4' type="button" class="btn btn-primary">红中二人</button>
                <button id='game5' type="button" class="btn btn-primary">红中四人</button>
                <button id='game6' type="button" class="btn btn-primary">欢乐拼点</button>
                <button id='game7' type="button" class="btn btn-primary">跑得快</button>
                <button id='game8' type="button" class="btn btn-primary">余干</button>
                <button id='game9' type="button" class="btn btn-primary">抚州</button>
                <button id='game10' type="button" class="btn btn-primary">南昌</button>
                <button id='game11' type="button" class="btn btn-primary">二人麻将</button>
                <button id='game12' type="button" class="btn btn-primary">斗地主</button>
            </div>
            
            <div class="content">
               %include original_search_bar
               <table id="dataTable" class="table table-bordered table-hover"></table>
            </div>
            <div style='clear:both'></div>
            <!-- %if session['type'] in ['0']: -->
                <!-- 数据统计表模块 -->
                %include admin_gold_operate_show.tpl
            <!-- %end -->
            <div style='clear:both'></div>
  </div>
<script type="text/javascript">

    function responseFunc(res){
        data = res.data;
        count= res.count;
        //实时刷

        // $('.totalTitle').html("下线代理总数: "+count)

        return data;
    }

    var bootstrap_dic = {
        url: '{{info["listUrl"]}}',
        method: 'get',
        pagination: true,
        pageSize: 15,
        sortOrder: 'desc',
        // search:true,
        sortName: 'regDate',
        sorttable:true,
        responseHandler:responseFunc,
        queryParams:getSearchP,
        showExport:true,
        exportTypes:['excel', 'csv', 'pdf', 'json'],
        pageList: '{{PAGE_LIST}}',
        columns:[
        [{
                halign    : "center",
                font      :  15,
                align     :  "left",
                class     :  "totalTitle",
                colspan   :  19, 
        }],
        [
        {
            field: 'date',
            title: '日期',
            align: 'center',
            valign: 'middle',
            sortable: true,
        },{

            field: 'player_count',
            sortable: true,
            title: '总参与玩家数',
            align: 'center',
            valign: 'middle',
            sortable: true,
        },{

            field: 'room_count',
            title: '有人房间总数',
            align: 'center',
            valign: 'middle',
            sortable: true,
        },{

            field: 'game_count',
            title: '金币场局数',
            align: 'center',
            valign: 'middle',
            sortable: true,
        },{

            field: 'fee_total',
            sortable: true,
            title: '收取房费总额',
            align: 'center',
            valign: 'middle',
        },{

            field: 'new_count',
            sortable: true,
            title: '新增用户数',
            align: 'center',
            valign: 'middle',
        },{

            field: 'online_user',
            title: '当前在线人数',
            align: 'center',
            valign:'middle',
            sortable: true,
        },{

            field: 'online_user_max',
            title: '在线人数峰值及时间',
            align: 'center',
            valign:'middle',
            sortable: true,
        },{

            field: 'buy_gold_count',
            title: '购买金币人数',
            valign: 'middle',
            align: 'center',
            formatter:get_bgpn
        },{

            field: 'buy_gold_total',
            title: '购买金币数',
            valign: 'middle',
            align: 'center',
            sortable: true,
        },{

            field: 'buy_money',
            title: '购买总额(元)',
            valign: 'middle',
            align: 'center',
            sortable: true,
        }]],
        //注册加载子表的事件。注意下这里的三个参数！
        onExpandRow: function (index, row, $detail) {
            console.log(index,row,$detail);
            InitSubTable(index, row, $detail);
        }
    }
  
    $('#classic').click(function(){
        window.location.href = '/admin/gold/operate?niuniu_type=555'
    });

    $('#open_hand').click(function(){
        window.location.href = '/admin/gold/operate?niuniu_type=556'
    });

    $('#joy').click(function(){
        window.location.href = '/admin/gold/operate?niuniu_type=666'
    });

    $('#game4').click(function(){
        window.location.href = '/admin/gold/operate?niuniu_type=444'
    });

    $('#game5').click(function(){
        window.location.href = '/admin/gold/operate?niuniu_type=445'
    });

    $('#game6').click(function(){
        window.location.href = '/admin/gold/operate?niuniu_type=557'
    });

    $('#game7').click(function(){
        window.location.href = '/admin/gold/operate?niuniu_type=559'
    });

    $('#game8').click(function(){
        window.location.href = '/admin/gold/operate?niuniu_type=446'
    });

    $('#game9').click(function(){
        window.location.href = '/admin/gold/operate?niuniu_type=448'
    });

    $('#game10').click(function(){
        window.location.href = '/admin/gold/operate?niuniu_type=447'
    });

    $('#game11').click(function(){
        window.location.href = '/admin/gold/operate?niuniu_type=449'
    });

    $('#game12').click(function(){
        window.location.href = '/admin/gold/operate?niuniu_type=560'
    });


    function get_bgpn(value,row,index){
        href = row['buy_gold_people_num']
        return "<a href='"+href+"'>" + row['buy_gold_count'] + "</a>"
    }

function fresh_table(niuniu_type){

    if(niuniu_type){
        bootstrap_dic['url'] = '{{info["listUrl"]}}'
    }

    $("#dataTable").bootstrapTable(bootstrap_dic);

    //初始化子表格
    function InitSubTable(index, row, $detail) {
            var parentAg = row.parentId;
            var cur_table = $detail.html('<table table-bordered table-hover definewidth style="margin-left:55px;background:#EEEEE0"></table>').find('table');
            $(cur_table).bootstrapTable(bootstrap_dic);



            function responseFunc(res){
                data = res.data;
                count= res.count;
                //实时刷

                return data;
            }

    }




    String.format = function() {
        if( arguments.length == 0 ) {
        return null;
        }
        var str = arguments[0];
        for(var i=1;i<arguments.length;i++) {
        var re = new RegExp('\\{' + (i-1) + '\\}','gm');
        str = str.replace(re, arguments[i]);
        }
        return str;
    }

}

function getSearchP(p){
      startDate = $("#pick-date-start").val();
      endDate   = $("#pick-date-end").val();

      sendParameter = p;

      sendParameter['startDate'] = startDate;
      sendParameter['endDate']  = endDate;

      return sendParameter;
}

function initTable(){
    fresh_table(555)
}

initTable()


</script>
%rebase admin_frame_base
