<div class='col-md-3'>
    <button style='width:100%;height:45px;padding:5px;'>
        <strong>{{lang.LABEL_MEMBER_TOTAL}}</strong><br>
        <span>{{info['member_total']}}</span>
    </button>
</div>

%if session['id'] == '1':
<div class='col-md-3'>
    <button style='width:100%;height:45px;padding:5px;'>
        <strong>{{lang.LABEL_REGIST_DAY}}</strong><br>
        <span>{{info['regist_per_day']}}</span>
    </button>
</div>
%end

<div class='col-md-3'>
    <button style='width:100%;height:45px;padding:5px;'>
        <strong>{{lang.LABEL_LOGIN_DAY}}</strong><br>
        <span>{{info['login_per_day']}}</span>
    </button>
</div>

%if sys == 'HALL':
<div class='col-md-3'>
    <button style='width:100%;height:45px;padding:5px;'>
        <strong>{{lang.LABEL_PLAYROOM_DAY}}</strong><br>
        <span>{{info['play_room_per_day']}}</span>
    </button>
</div>
%end

%if sys == 'FISH':
<div class='col-md-3'>
    <button style='width:100%;height:45px;padding:5px;'>
        <strong>{{lang.LABEL_RECHARGE_DAY}}</strong><br>
        <span>{{info['recharge_total']}}</span>
    </button>
</div>
%end

%rebase component_panel title='欢迎使用搜集游棋牌后台管理系统',panel_color='info'
