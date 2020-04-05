<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
  <div class="block">
            %include admin_frame_header
            <table class="table table-bordered table-hover" style="width:20%;float: left;">
            <thead>
                <tr>
                <th>总当前AI人数</th>
                <th>总当前有AI房间数</th>
                    <th>当天AI金币总数</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                <td>{{info['online_ai_sum']}}</td>
                <td>{{info['online_ai_room_num']}}</td>
                <td>{{info['cur_ai_gold_sum']}} </td>
                </tr>
                
            </tbody>
            </table>
            <div style='margin-left: 5%;float: left;margin-top: 20px;'>
                <button id='B' type="button" class="btn btn-primary">B档</button>
                <button id='D' type="button" class="btn btn-primary">D档</button>
            </div>
            
            <div class="content">
               %include original_search_bar
               <table id="dataTable" class="table table-bordered table-hover"></table>
            </div>
  </div>
<script type="text/javascript">
  
    $('#B').click(function(){
        window.location.href = '/admin/gold/ai?grade=b'    
    });

    $('#D').click(function(){
        window.location.href = '/admin/gold/ai?grade=d'    
    });


    
    var bootstrap_dic = {
            url: '{{info["listUrl"]}}',
            method: 'get',
            pagination: true,
            pageSize: 15,
            sortOrder: 'desc',
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
                field: 'join_ai_sum',
                title: '总参与AI数',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{

                field: 'ai_room_sum',
                sortable: true,
                title: 'AI参与房间总数',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{

                field: 'ai_gold_sum',
                title: 'AI参与金币场总局数',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{

                field: 'cur_ai_gold_num',
                title: '当天AI携带金币总数',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }]],
            //注册加载子表的事件。注意下这里的三个参数！
            onExpandRow: function (index, row, $detail) {
                console.log(index,row,$detail);
                InitSubTable(index, row, $detail);
            }
    }

    function initTable(){
        if('{{info["grade"]}}'=='d'){
            bootstrap_dic['url'] = '{{info["listUrl"]}}&grade=d'
            }else{
            bootstrap_dic['url'] = '{{info["listUrl"]}}&grade=b'
        }
        $("#dataTable").bootstrapTable(bootstrap_dic);
    }
    initTable()    

    

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

function responseFunc(res){
    data = res.data;
    count= res.count;
    //实时刷

    // $('.totalTitle').html("下线代理总数: "+count)

    return data;
}


function getSearchP(p){
      startDate = $("#pick-date-start").val();
      endDate   = $("#pick-date-end").val();

      sendParameter = p;

      sendParameter['startDate'] = startDate;
      sendParameter['endDate']  = endDate;

      return sendParameter;
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


</script>
%rebase admin_frame_base
