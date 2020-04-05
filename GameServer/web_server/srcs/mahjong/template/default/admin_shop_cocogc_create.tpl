<style type="text/css">.config-table td.table-title{text-align:center;font-size:13px;vertical-align:middle}</style>
<div class='block'>
          %include admin_frame_header
          <div class="content" id="game_create_app">
             <form class="form-horizontal group-border-dashed" id='gameForm' @submit="onSubmit" action="{{info['submitUrl']}}" method="post" style="border-radius: 0px;" enctype="multipart/form-data">
              <input type="text" class="form-control" placeholder="游戏ID" name="match_gameid" value="{{ matchInfo['gameid'] }}" style="display:none;">
                            <input type="text" class="form-control" placeholder="比赛场ID" name="match_matchId" value="{{ matchInfo['id'] }}" style="display:none;">
              <table class='table config-table'>
                    <tr>
                        <td width='20%' class='table-title' style="font-size:20px; background-color:#d9edf7">修改比赛</td>
                    </tr>
                    <tr>
                        <td>
                            <table class='table config-table' border='1'>
                                <tr>
                                    <td class='table-title' style="width:200px">比赛名称<br>
                                    </td>
                                    <td>
                                        <input type="text" class="form-control" placeholder="填写比赛的名称" name="match_title" value="{{ matchInfo['title'] }}">
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">比赛奖励<br><span class="help-block">填写比赛的名次跟奖励，将会显示在前端</span>
                                        <span><a href="javascript:;" @click="onAdd" class='btn btn-small btn-xs btn-primary'>增加</a></span>
                                        <span><a href="javascript:;" @click="onDel" class='btn btn-small btn-xs btn-danger'>删除</a></span>
                                    </td>
                                    <td id="rewardList">
                                        <table class="table config-table table1 table-bordered table-hover" style="margin-top:5px">
                                            %if not info['rewardList']:
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
                                                    <select name='match_reward_type1' id='match_reward_type1' class="form-control" style="width:120px;float:left">
                                                        %for feetype, feename in info['feetypeList'].items():
                                                            <option value="{{ feetype }}">{{ feename }}</option>
                                                        %end
                                                    </select>
                                                </td>
                                                <td class="table-title">数值</td>
                                                <td>
                                                    <input type="text" name='match_reward_fee1' style="width:120px;float:left" class="form-control">
                                                </td>
                                            </tr>
                                            %end
                                            %for reward in info['rewardList']:
                                            <tr>
                                                <td class="table-title">名次</td>
                                                <td>
                                                    <input type="text" name="match_reward_rank{{ reward['id'] }}" style="width:120px;float:left" class="form-control" value="{{ reward.get('rank', '1') }}" readonly>
                                                </td>
                                                <td class="table-title">称谓</td>
                                                <td>
                                                    <input type="text"  name="match_reward_appellation{{ reward['id'] }}" style="width:120px;float:left" class="form-control" value="{{ reward['field'] }}">
                                                </td>
                                                <td class="table-title">类型</td>
                                                <td>
                                                    <select name='match_reward_type{{ reward['id'] }}' id='match_reward_type{{ reward['id'] }}' class="form-control" style="width:120px;float:left">
                                                        %if reward.get('type') == 'roomCard':
                                                            <option value="roomCard" checked="chedked">钻石</option>
                                                            <option value="gamePoint">积分</option>
                                                        %else:
                                                            <option value="gamePoint" checked="chedked">积分</option>
                                                            <option value="roomCard">钻石</option>
                                                        %end
                                                    </select>
                                                </td>
                                                <td class="table-title">数值</td>
                                                <td>
                                                    <input type="text" name='match_reward_fee{{ reward['id'] }}' style="width:120px;float:left" class="form-control" value="{{ reward.get('currency_count', '0') }}">
                                                </td>
                                            </tr>
                                           %end
                                        </table>
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
                            %for feeid, feename in info["feetypeList"].items():
                                feeStr += String.format('<option value="{0}">{1}</option>', "{{ feeid }}", "{{ feename }}")
                            %end
                            var rankName = {'1': '第一名', '2': '第二名', '3': '第三名', '4': '第四名', '5': '第五名', '6': '第六名', '7': '第七名', '8': '第八名', '9': '第九名', '10': '第十名'}
                            str = '<tr num="'+(num+1)+'">\
                                    <td class="table-title">名次</td>\
                                    <td><input type="text" name="match_reward_rank'+(num+1)+'" style="width:120px;float:left" class="form-control" value="'+(num+1)+'" readonly>\
                                    <td class="table-title">称谓</td>\
                                    <td><input type="text" name="match_reward_appellation'+(num+1)+'" style="width:120px;float:left" class="form-control" value="'+(rankName[num+1])+'">\
                                    <td class="table-title">类型</td>\
                                    <td><select name="match_reward_type'+(num+1)+'" class="form-control" style="width:120px;float:left">' + feeStr + '</select></td>\
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
%rebase admin_frame_base
