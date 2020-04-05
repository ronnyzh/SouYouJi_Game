<div>
    <script>
            function operateFormatter(value, row, index) {
               return [
               '<button type="button" class="change_edit btn btn-primary  btn-sm" style="margin-right:15px;">修改</button>'
               ].join('');
               }

             window.operateEvents = {
            'click .change_edit': function (e, value, row, index) {
                    var game_name = $("table").find("tr").eq(index + 1).find("td").eq(0).text();
                    var game_id = game_id_map[game_name];
                    var url = "{{info['url_pre']}}" + "?game_id=" +  game_id.toString();
                    //alert(url);
                     window.location.href=url; 
                }
             }
    </script> 



    <h1 align='center'>D档机器人基础配置</h1>
    <table id="table" class="table table-bordered table-hover"></table>        
</div>

    <script>
            var game_id_map = {'二人麻将':449,'二人红中':444,'四人红中':445,'跑得快':559}
            $('#table').bootstrapTable({  
                columns: [{  
                    field: 'game',  
                    title: '游戏',
                }, {  
                    field: 'operation',  
                    title: '操作',
                    events: operateEvents,
                    formatter: operateFormatter
                }],  
                data: [{  
                    game: '二人麻将',  
                }, 
                {  
                    game: '二人红中',  
                },
                {  
                    game: '四人红中',  
                },
                {  
                    game: '跑得快',  
                },
                ]  
            });     

    </script> 

%rebase admin_frame_base
