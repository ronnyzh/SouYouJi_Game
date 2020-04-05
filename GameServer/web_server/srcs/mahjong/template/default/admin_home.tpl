<div class="cl-mcont">
        <!-- 欢迎页 -->
            <div class="jumbotron">
                    <h2>{{lang.MAHJONG_TITLE_TXT}} <small>欢迎你,{{session['account']}}</small></h2>
                    <br/>
                    <p></p>
            </div>
            <!-- 基本数据统计模块 -->
            %include admin_home_static
            <div style='clear:both'></div>
            %if session['type'] in ['0']:
                <!-- 数据统计表模块 -->
                %include admin_home_show
            %end
            <div style='clear:both'></div>
</div>
%rebase admin_frame_base
