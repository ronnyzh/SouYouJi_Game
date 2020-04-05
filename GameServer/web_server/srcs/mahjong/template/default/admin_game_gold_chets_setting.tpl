<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>


<div class='block'>
    <div class="row">
        %for _dat in result:
        
        <div class="col-md-4">
        <div class="panel panel-info">
            <!-- Default panel contents -->
            
            <div class="panel-heading"><b>{{ _dat["txt"] }}</b></div>
            <div class="panel-body">
                    <!-- <div class="form-group">
                        <label for="exampleInputEmail1">状态</label>
                        <select class="form-control">
                                            <option value="0">启用</option>
                                            <option value="1">关闭</option>
                        </select>
                    </div> -->
                    <div class="form-inline">
                        <div class="form-group">
                            <div class="col-md-12">
                                <label for="exampleInputEmail1">奖励图标:</label>
                                <select class="form-control chats_type">
                                    <option value="{{_dat['chets_type']['key']}}" > {{_dat['chets_type']['value']}} </option>
                                    <option value="0">铜</option>
                                    <option value="1">银</option>
                                    <option value="2">金</option>
                                </select>
                            </div>

                            
                        </div>
                    </div>
                    <div class="form-inline">
                        <div class="form-group">
                            <div class="col-xs-5">
                                <label for="exampleInputPassword1">对局任务:</label>
                                <!-- <input type="number" class="form-control" id="exampleInputPassword1" placeholder=""> -->
                                <div class="form-inline">
                                <div class="form-group">
                                    <div class="col-md-3">
                                        <select class="form-control chets_resultType1">
                                            <option value="{{ _dat['chets_result'][0]['key'] }}" class="">{{ _dat['chets_result'][0]['txt'] }}</option>
                                            <option value="0">金币</option>
                                            <option value="1">元宝</option>
                                            <option value="2">道具</option>
                                        </select>
                                    </div>
                                    <div class="col-md-3">
                                        <input type="number" class="form-control chets_resultValue1" value="{{ _dat['chets_result'][0]['value'] }}"  placeholder="" >
                                    </div>
                                </div>
                                <div class="form-group">
                                    <div class="col-md-3">
                                        <select class="form-control chets_resultType2">
                                            <option value="{{ _dat['chets_result'][1]['key'] }}" class="">{{ _dat['chets_result'][1]['txt'] }}</option>
                                            <option value="0">金币</option>
                                            <option value="1">元宝</option>
                                            <option value="2">道具</option>
                                        </select>
                                    </div>
                                    <div class="col-md-3">
                                        <input type="number" class="form-control chets_resultValue2" value="{{ _dat['chets_result'][1]['value'] }}"  placeholder="">
                                    </div>
                                </div>
                                <div class="form-group">
                                    <div class="col-md-3">
                                        <select class="form-control chets_resultType3">
                                            <option value="{{ _dat['chets_result'][2]['key'] }}" class="">{{ _dat['chets_result'][2]['txt'] }}</option>
                                            <option value="0">金币</option>
                                            <option value="1">元宝</option>
                                            <option value="2">道具</option>
                                        </select>
                                    </div>
                                    <div class="col-md-4">
                                        <input type="number" class="form-control chets_resultValue3" value="{{ _dat['chets_result'][2]['value'] }}"  placeholder="">
                                    </div>
                                </div>
                                </div>
                            </div>

                             <div class="col-xs-5">
                                 <label for="exampleInputPassword1">胜局任务:</label>
                                <!--<input type="number" class="form-control" id="exampleInputPassword1" placeholder=""> -->
                                <div class="form-inline">
                                <div class="form-group">
                                    <div class="col-md-3">
                                        <select class="form-control chets_win_resultType1">
                                            <option value="{{ _dat['chets_win_result'][0]['key'] }}" >{{ _dat['chets_win_result'][0]['txt'] }}</option>
                                            <option value="0">金币</option>
                                            <option value="1">元宝</option>
                                            <option value="2">道具</option>
                                        </select>
                                    </div>
                                    
                                    <div class="col-md-3">
                                        <input type="number" class="form-control chets_win_resultValue1" value="{{ _dat['chets_win_result'][0]['value'] }}"  placeholder="">
                                    </div>
                                </div>
                                <div class="form-group">
                                    <div class="col-md-3">
                                        <select class="form-control chets_win_resultType2">
                                            <option value="{{ _dat['chets_win_result'][1]['key'] }}">{{ _dat['chets_win_result'][1]['txt'] }}</option>
                                            <option value="0">金币</option>
                                            <option value="1">元宝</option>
                                            <option value="2">道具</option>
                                        </select>
                                    </div>
                                    
                                    <div class="col-md-3">
                                        <input type="number" class="form-control chets_win_resultValue2" value="{{ _dat['chets_win_result'][1]['value'] }}" placeholder="">
                                    </div>
                                </div>
                                <div class="form-group">
                                    <div class="col-md-3">
                                        <select class="form-control chets_win_resultType3">
                                            <option value="{{ _dat['chets_win_result'][2]['key'] }}">{{ _dat['chets_win_result'][2]['txt'] }}</option>
                                            <option value="0">金币</option>
                                            <option value="1">元宝</option>
                                            <option value="2">道具</option>
                                        </select>
                                    </div>
                                    
                                    <div class="col-md-3">
                                        <input type="number" class="form-control chets_win_resultValue3" value="{{ _dat['chets_win_result'][2]['value'] }}"  placeholder="">
                                    </div>
                                </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="form-group">
                        <button class="btn btn-default submit" level="{{_dat['level']}}">修改</button>
                    </div>
                    </div>
            
        </div>
        </div>
        %end
</div>
</div>
<script>
    $('body').delegate(".submit", "click", function(){
        var game_id = {{info["gameId"]}};
        var level = $(this).attr("level")
        btn = $(this);
        panel = btn.parent().parent();
        var chats_type = panel.find(".chats_type").val();
        //var chets_win_type = panel.find(".chets_win_type").val();
        var chets_win_type = chats_type;

        var chets_result1Type1 = panel.find(".chets_resultType1").val();
        var chets_result1Type2 = panel.find(".chets_resultType2").val();
        var chets_result1Type3 = panel.find(".chets_resultType3").val();

        var chets_win_result1Type1 = panel.find(".chets_win_resultType1").val();
        var chets_win_result1Type2 = panel.find(".chets_win_resultType2").val();
        var chets_win_result1Type3 = panel.find(".chets_win_resultType3").val();

        var chets_win_resultValue1 = panel.find(".chets_win_resultValue1").val();
        var chets_win_resultValue2 = panel.find(".chets_win_resultValue2").val();
        var chets_win_resultValue3 = panel.find(".chets_win_resultValue3").val();

        var chets_resultValue1 = panel.find(".chets_resultValue1").val();
        var chets_resultValue2 = panel.find(".chets_resultValue2").val();
        var chets_resultValue3 = panel.find(".chets_resultValue3").val();
        
        var chets_values = [
        {
            "key": chets_result1Type1,
            "value": chets_resultValue1
        },
        {
            "key": chets_result1Type2,
            "value": chets_resultValue2
        },
        {
            "key": chets_result1Type3,
            "value": chets_resultValue3
        },
        ]
        var chets_win_values = [
        {
            "key": chets_win_result1Type1,
            "value": chets_win_resultValue1
        },
        {
            "key": chets_win_result1Type2,
            "value": chets_win_resultValue2
        },
        {
            "key": chets_win_result1Type3,
            "value": chets_win_resultValue3
        },
        ]

        $.ajax({
            type: 'POST',
            url: "/admin/game/setting/chets",
            data: {"game_id": game_id, "level": level, "chets_values": JSON.stringify(chets_values), "chets_win_values": JSON.stringify(chets_win_values), "chets_type": chats_type, "chets_win_type": chets_win_type},
            dataType: "json",
            success: function(res, data){
                layer.msg(res.msg);
                location.reload();
            },
            error: function(res, data){
                console.log(res);
         }, 
            
        });


    });

</script>
%rebase admin_frame_base