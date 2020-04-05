<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class='block'>
          %include admin_frame_header
          <div class="content" id="game_create_app" style="float:left;width:100%;position:relative;top:2.6em">
             <form class="form-horizontal group-border-dashed" id='gameForm' @submit="onSubmit" action="{{info['submitUrl']}}" method="post" style="border-radius: 0px;" enctype="multipart/form-data">
              <table class='table config-table'>
                    <tr>
                        <td width='20%' class='table-title' style="font-size:20px;background-color:#d9edf7;">创建比赛</td>
                    </tr>
                    <tr>
                        <td>
                            <table class='table config-table' border='1'>
                                <tr>
                                    <td class='table-title' style="width:200px">比赛名称<br>
                                    </td>
                                    <td>
                                        <input type="text" class="form-control" placeholder="填写比赛的名称" name="match_title">
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">比赛类型<br>
                                    </td>
                                    <td>
                                        %for typeId, typeName in sorted(info['matchType'].items()):
                                        <label class="well col-sm-6">
                                            <input type="radio" name="match_type" value="{{ typeId }}"  {{ "checked" if typeId == '0' else "" }}> {{ typeName }}
                                            %if typeId == '0':
                                                <span class="help-block">报名人数满之后直接开始比赛</span>
                                            %else:
                                                <span class="help-block">定于某个时间点开始比赛</span>
                                            %end
                                        </label>
                                        %end
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">比赛玩法<br>
                                    </td>
                                    <td>
                                        <select name='match_gameid' id='match_gameid' class="form-control">
                                            <option value="">下拉选择游戏</option>
                                            %for gameid, gamename in info['gameList'].items():
                                                <option value="{{ gameid }}">{{ gamename }}</option>
                                            %end
                                        </select>
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">游戏名称<br>
                                    </td>
                                    <td>
                                        <input type="text" class="form-control" placeholder="填写游戏的名称" name="match_gamename">
                                    </td>
                                </tr>
                                <tr id="rewardList">
                                    <td class='table-title' style="width:200px">场次类型<br>
                                    </td>
                                    <td>
                                        <table class='table config-table' border='1'>
                                            <tr>
                                                <td>
                                                    %for feeId, feeName in sorted(info['feetypeList'].items()):
                                                    <label class="well col-sm-6">
                                                        <input type="radio" name="party_type"  value="{{ feeId }}"  {{"checked" if feeId == 'roomCard' else ""}} onclick="checkradio('{{ feeId }}')">&nbsp;{{ feeName }}
                                                    </label>
                                                    %end
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                <tr id="rewardList">
                                    <td class='table-title' style="width:200px">报名费用<br>
                                    </td>
                                    <td>
                                        <table class='table config-table' border='1'>
                                            <tr>
                                                <td>
                                                    <label class="well col-sm-12">
                                                        <input type="radio" name="match_feetype" value="roomCard"  checked='checked'>&nbsp;钻石
                                                    </label>
                                                    <input type="text" class="form-control" name="match_fee" placeholder="报名费用（费用为0则免费）">
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">比赛人数<br>
                                    </td>
                                    <td>
                                        <input type="text" class="form-control" placeholder="填写比赛人数" name="match_num">
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">淘汰轮数计划<br>
                                    </td>
                                    <td>
                                        <input type="text" class="form-control" placeholder="填写淘汰轮数计划,如:3,6,9,12" name="roundNums">
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">淘汰人数计划<br>
                                    </td>
                                    <td>
                                        <input type="text" class="form-control" placeholder="填写淘汰人数计划,如:32,16,8,0" name="roundPlayers">
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">比赛奖励<br><span class="help-block">填写比赛的名次跟奖励，将会显示在前端</span>
                                        <span><a href="javascript:;" @click="onAdd" class='btn btn-small btn-xs btn-primary'>增加</a></span>
                                        <span><a href="javascript:;" @click="onDel" class='btn btn-small btn-xs btn-danger'>删除</a></span>
                                    </td>
                                    <td id="rewardList">
                                        <table class="table config-table table1 table-bordered table-hover" style="margin-top:5px">
                                            <tr>
                                                <td class="table-title">名次</td>
                                                <td>
                                                    <input type="text" name="match_reward_rank1" style="width:120px;float:left" class="form-control" value="1" readonly>
                                                </td>
                                                <td class="table-title">称谓</td>
                                                <td>
                                                    <input type="text"  name="match_reward_appellation1" style="width:120px;float:left" class="form-control" value="第一名">
                                                </td>
                                                <td class="table-title">类型</td>
                                                <td>
                                                    <select name='match_reward_type1' readonly id='match_reward_type1' class="form-control" style="width:120px;float:left">
                                                        <option value="roomCard" selected >钻石</option>
                                                    </select>
                                                </td>
                                                <td class="table-title">数值</td>
                                                <td>
                                                    <input type="text" name='match_reward_fee1' style="width:120px;float:left" class="form-control" value="0">
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">比赛说明<br>
                                    </td>
                                    <td>
                                        <textarea name="match_rule" cols="30" rows="10" class="form-control"></textarea>
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">可显示<br>
                                    </td>
                                    <td>
                                        <label class="well col-sm-6">
                                            <input type="radio" name="match_display" value="1" checked> 是
                                                <span class="help-block">会在游戏前端比赛场显示</span>
                                        </label>
                                        <label class="well col-sm-6">
                                            <input type="radio" name="match_display" value="0"> 否
                                                <span class="help-block">不在游戏前端比赛场显示</span>
                                        </label>
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">可报名<br>
                                    </td>
                                    <td>
                                        <label class="well col-sm-6">
                                            <input type="radio" name="match_enroll" value="1" checked> 开启
                                                <span class="help-block">可以进行报名</span>
                                        </label>
                                        <label class="well col-sm-6">
                                            <input type="radio" name="match_enroll" value="0"> 关闭
                                                <span class="help-block">不可以进行报名</span>
                                        </label>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
              </table>
              <div class="modal-footer" style="text-align:center">
                   <button type="submit" class="btn btn-sm btn-primary">{{lang.BTN_SUBMIT_TXT}}</button>
                  <button type="button" class="btn btn-sm btn-primary" @click="onBack">{{lang.BTN_BACK_TXT}}</button>
              </div>
            </form>
    </div>
</div>
<script type="text/javascript">
    $(function(){   //前端页面配置及渲染
        var game_create_app = new Vue({
               el : '#game_create_app',
               data:{

               },mounted:function(){

               },methods:{
                   onSubmit : function(e){
                       e.preventDefault();
                       formAjax($('#gameForm').attr("action"), $('#gameForm').attr("method"), $('#gameForm').serialize(),'正在创建...');
                   },

                   onBack : function(e){
                       e.preventDefault();
                       window.location.href="{{info['backUrl']}}";
                   },

                   onAdd : function(e){
                       e.preventDefault();
                       var configTable = $('.table1');
                       var num = parseInt(configTable.find('tr').length);
                       if (num == 8){
                            //信息框
                            layer.open({
                              content   : '只允许创建8个名次'
                              ,btn      : '关闭'
                            });
                       }else{
                            feeStr = ''
                            var party_type = $('input:radio[name="party_type"]:checked').val()
                            var feeName = {'roomCard': '钻石', 'gamePoint': '积分'};
                            feeStr += String.format('<option value="{0}">{1}</option>', party_type, feeName[party_type])
                            var rankName = {'1': '第一名', '2': '第二名', '3': '第三名', '4': '第四名', '5': '第五名', '6': '第六名', '7': '第七名', '8': '第八名', '9': '第九名', '10': '第十名'}
                            str = '<tr num="'+(num+1)+'">\
                                    <td class="table-title">名次</td>\
                                    <td><input type="text" name="match_reward_rank'+(num+1)+'" style="width:120px;float:left" class="form-control" value="'+(num+1)+'" readonly>\
                                    <td class="table-title">称谓</td>\
                                    <td><input type="text" name="match_reward_appellation'+(num+1)+'" style="width:120px;float:left" class="form-control" value="'+(rankName[num+1])+'">\
                                    <td class="table-title">类型</td>\
                                    <td><select name="match_reward_type'+(num+1)+'" id="match_reward_type'+(num+1)+'"  class="form-control" style="width:120px;float:left" readonly>' + feeStr + '</select></td>\
                                    <td class="table-title">数值</td>\
                                    <td><input type="text" name="match_reward_fee'+(num+1)+'" style="width:120px;float:left" class="form-control" value="0"></td>\
                                  </tr>';

                            //添加到子节点
                            configTable.append(str);
                       }
                   },

                   onDel : function(e){
                       e.preventDefault();
                       var configTable = $('.table1');
                       var num = parseInt(configTable.find('tr').length);
                       if (num == 1){
                            //信息框
                            layer.open({
                              content   : '至少需要一个比赛奖励名次'
                              ,btn      : '关闭'
                            });
                       }else{
                            $('.table1 tr:last').remove();
                       }
                   },
               }
        });
    })
</script>
<script>
function checkradio(x){
    for (var i = 1; i < 9; i++){
        var selectId = String.format("#match_reward_type{0}", i);
        var sl=$(selectId);
        var ops=sl.find("option");
        if(x == 'roomCard'){
            ops.eq(0).val("roomCard").text("钻石").prop("selected",true);
        }
        if(x == 'gamePoint'){
            ops.eq(0).val("gamePoint").text("积分").prop("selected",true);
        }
        $(selectId).attr("readonly","readonly");
    }
}
</script>
%rebase admin_frame_base
