<style type="text/css">.config-table td.table-title{text-align:center;font-size:13px;vertical-align:middle}</style>
<div class='block'>
          %include admin_frame_header
          <div class="content" id="game_create_app">
             <form class="form-horizontal group-border-dashed" id='gameForm' @submit="onSubmit" action="" method="post" style="border-radius: 0px;" enctype="multipart/form-data">
              <input type="text" class="form-control" placeholder="游戏ID" name="match_gameid" value="{{ matchInfo['gameid'] }}" style="display:none;">
                            <input type="text" class="form-control" placeholder="比赛场ID" name="match_matchId" value="{{ matchInfo['id'] }}" style="display:none;">
              <table class='table config-table'>
                    <tr>
                        <td width='20%' class='table-title' style="font-size:20px; background-color:#d9edf7">赛事详情</td>
                    </tr>
                    <tr>
                        <td>
                            <table class='table config-table' border='1'>
                                <tr>
                                    <td class='table-title' style="width:200px">比赛名称<br>
                                    </td>
                                    <td>
                                        <input type="text" class="form-control" readonly placeholder="填写比赛的名称" name="match_title" value="{{ matchInfo['title'] }}">
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">比赛类型<br>
                                    </td>
                                    <td>
                                        <label class="well col-sm-12">
                                                <input type="radio" name="match_type" value="0"  checked="checked" readonly}}>即时开始
                                                <span class="help-block">报名人数满之后直接开始比赛</span>
                                        </label>
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">比赛玩法<br>
                                    </td>
                                    <td>
                                        <input type="text" class="form-control" readonly name="match_game" value="{{ matchInfo['gamename'] }}">
                                    </td>
                                </tr>
                                <tr id="rewardList">
                                    <td class='table-title' style="width:200px">场次类型<br>
                                    </td>
                                    <td>
                                        <table class='table config-table' border='1'>
                                            <tr>
                                                <td>
                                                    %if matchInfo.get('matchtype') == '1':
                                                    <label class="well col-sm-12">
                                                        <input type="radio" name="party_type" value="roomCard"  readonly checked='checked'> 钻石
                                                    </label>
                                                    %else:
                                                    <label class="well col-sm-12">
                                                        <input type="radio" name="party_type" value="gamePoint"  readonly checked='checked'> 积分
                                                    %end
                                                    </label>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr id="rewardList">
                                    <td class='table-title' style="width:200px">报名费用<br>
                                    </td>
                                    <td>
                                        <table class='table config-table' border='1'>
                                            <tr>
                                                <td>
                                                    <label class="well col-sm-12">
                                                        <input type="radio" name="match_feetype" value="roomCard" readonly checked='checked'> 钻石
                                                    </label>
                                                     <input type="text" class="form-control" name="match_fee" readonly placeholder="报名费用（费用为0则免费）" value="{{ matchInfo['fee'] }}">
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">比赛人数<br>
                                    </td>
                                    <td>
                                        <input type="text" class="form-control" readonly placeholder="填写比赛人数" name="match_num" value="{{ matchInfo['play_num'] }}">
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">淘汰轮数计划<br>
                                    </td>
                                    <td>
                                        <input type="text" class="form-control" readonly placeholder="填写淘汰轮数计划,如:3,6,9,12" name="roundNums" value="{{ matchInfo.get('roundNums','') }}">
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">淘汰人数计划<br>
                                    </td>
                                    <td>
                                        <input type="text" class="form-control" readonly placeholder="填写淘汰人数计划,如:32,16,8,0" name="roundPlayers" value="{{ matchInfo.get('roundPlayers','') }}">
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">比赛奖励
                                    </td>
                                    <td id="rewardList">
                                        <table class="table config-table table1 table-bordered table-hover" style="margin-top:5px">
                                            %if not info['rewardList']:
                                            <tr>
                                                <td class="table-title">名次</td>
                                                <td>
                                                    <input type="text" readonly name="match_reward_rank1" style="width:120px;float:left" class="form-control" value="1" readonly>
                                                </td>
                                                <td class="table-title">称谓</td>
                                                <td>
                                                    <input type="text"  readonly name="match_reward_appellation1" style="width:120px;float:left" class="form-control" value="第一名">
                                                </td>
                                                <td class="table-title">类型</td>
                                                <td>
                                                    <select readonly name='match_reward_type1' id='match_reward_type1' class="form-control" style="width:120px;float:left">
                                                        %for feetype, feename in info['feetypeList'].items():
                                                            <option value="{{ feetype }}">{{ feename }}</option>
                                                        %end
                                                    </select>
                                                </td>
                                                <td class="table-title">数值</td>
                                                <td>
                                                    <input readonly type="text" name='match_reward_fee1' style="width:120px;float:left" class="form-control">
                                                </td>
                                            </tr>
                                            %end
                                            %for reward in info['rewardList']:
                                            <tr>
                                                <td class="table-title">名次</td>
                                                <td>
                                                    <input type="text" readonly name="match_reward_rank{{ reward['id'] }}" style="width:120px;float:left" class="form-control" value="{{ reward.get('rank', '1') }}" readonly>
                                                </td>
                                                <td class="table-title">称谓</td>
                                                <td>
                                                    <input type="text"  readonly name="match_reward_appellation{{ reward['id'] }}" style="width:120px;float:left" class="form-control" value="{{ reward['field'] }}">
                                                </td>
                                                <td class="table-title">类型</td>
                                                <td>
                                                    <select readonly name='match_reward_type{{ reward['id'] }}' id='match_reward_type{{ reward['id'] }}' class="form-control" style="width:120px;float:left">
                                                        %if reward.get('type') == 'roomCard':
                                                            <option readonly value="roomCard" checked="chedked">钻石</option>
                                                            <option readonly value="gamePoint">积分</option>
                                                        %else:
                                                            <option readonly value="gamePoint" checked="chedked">积分</option>
                                                            <option readonly value="roomCard">钻石</option>
                                                        %end
                                                    </select>
                                                </td>
                                                <td class="table-title">数值</td>
                                                <td>
                                                    <input type="text" readonly name='match_reward_fee{{ reward['id'] }}' style="width:120px;float:left" class="form-control" value="{{ reward.get('currency_count', '0') }}">
                                                </td>
                                            </tr>
                                           %end
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">比赛说明<br>
                                    </td>
                                    <td>
                                        <textarea name="match_rule" readonly cols="30" rows="10" class="form-control">{{ matchInfo['rule'] }}</textarea>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
              </table>
            </form>
    </div>
</div>
%rebase admin_frame_base
