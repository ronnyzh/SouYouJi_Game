<header class="layout-header" id="header">
            <!-- <span class="header-logo">{{session['account']}}</span> -->


            %if datas.has_key('show_card_bar'):
                <span class="header-logo" style='margin-left:20px;font-size:1em'>{{lang.LABEL_ROOMCARD_TITLE}}:&nbsp;<span class='badge badge-card'>{{datas['room_card']}}</span></span>
            %end

            <span class="header-logo"><a href="javascript:;" class='label label-small label-primary' onclick="logout();">{{lang.LABEL_LOGOUT_TXT}}</a></span>
            <!--
            %if datas['agent_type'] in ['0']:
                <span class="header-logo"><a href="{{datas['link_fish_url']}}" class='label label-small label-primary'>{{datas['link_fish_txt']}}</a></span>
            %end
            -->
            <a class="header-menu-btn" href="javascript:;"><i class="icon-font">&#xe600;</i></a>
            <ul class="header-bar">
                <li class="header-bar-role"><a href="javascript:;">{{lang.LABEL_AGENTROLE_TXT}}:{{TYPE2TXT[datas['agent_type']]}}</a></li>
                <li class="header-bar-role"><a href="javascript:;">{{lang.LABEL_AGENTID_TXT}}:{{datas['agent_id']}}</a></li>
                <li class="header-bar-role"><a href="javascript:;">{{lang.LABEL_LASTLOIN_TIME_TXT}}:{{session['lastLoginDate']}}</a></li>
                <li class="header-bar-role"><a href="javascript:;">{{lang.LABEL_LASTLOIN_IP_TXT}}:{{session['lastLoginIp']}}</a></li>
<!--                 <li class="header-bar-nav"></li> -->
<!--                 <li class="header-bar-nav">
                    <a href="javascript:;" title="换肤"><i class="icon-font">&#xe608;</i></a>
                    <ul class="header-dropdown-menu right dropdown-skin">
                        <li><a href="javascript:;" data-val="qingxin" title="清新">清新</a></li>
                        <li><a href="javascript:;" data-val="blue" title="蓝色">蓝色</a></li>
                        <li><a href="javascript:;" data-val="molv" title="墨绿">墨绿</a></li>

                    </ul>
                </li> -->
            </ul>
</header>
