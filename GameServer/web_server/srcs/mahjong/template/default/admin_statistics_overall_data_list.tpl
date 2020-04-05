<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/echarts.common.min.js"></script>
<div class="block">
    %include admin_frame_header
    <div class="content" style="float:left;width:100%;position:relative;top:2.1em">
        <div class="col-lg-4">
            <div class="ibox float-e-margins">
                <div class="ibox-title">
                    <h4><strong> 当日数据 [ {{ info['today'] }} ] </strong></h4>
                </div>
                <div class="ibox-content">
                    <ul class="list-group clear-list m-t">
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ dayData['reg_count'] }}
                            </span>
                            <span class="label label-success">1</span> 新增玩家数量
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ dayData['active_count'] }}
                            </span>
                            <span class="label label-primary">2</span> 活跃玩家数量
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ dayData['take_count'] }}
                            </span>
                            <span class="label label-danger">3</span> 钻石耗钻
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ dayData['room_count'] }}
                            </span>
                            <span class="label label-info">4</span> 局数统计
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ dayData['money_count'] }}
                            </span>
                            <span class="label label-warning">5</span> 玩家充值金额
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ dayData['sale_report_count'] }}
                            </span>
                            <span class="label label-info">6</span> 我的售钻数
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ dayData['sub_sale_reprot_count'] }}
                            </span>
                            <span class="label label-danger">7</span> 下线代理售钻数
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ dayData['sub_buy_reprot_count'] }}
                            </span>
                            <span class="label label-warning">8</span> 下线代理购钻数
                        </li>
                        <!--
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ dayData['rate_report_count'] }}
                            </span>
                            <span class="label label-primary">9</span> 我的利润总占额
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ dayData['rate_report_agent_count'] }}
                            </span>
                            <span class="label label-success">10</span> 下线代理总占额
                        </li>
                        -->
                    </ul>
                </div>
            </div>
        </div>
        <div class="col-lg-4">
            <div class="ibox float-e-margins">
                <div class="ibox-title">
                    <h4><strong> 当月数据 [ {{ info['month'] }} ] </strong></h4>
                </div>
                <div class="ibox-content">
                    <ul class="list-group clear-list m-t">
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ monthData['reg_count'] }}
                            </span>
                            <span class="label label-success">1</span> 新增玩家数量
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ monthData['active_count'] }}
                            </span>
                            <span class="label label-primary">2</span> 活跃玩家数量
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ monthData['take_count'] }}
                            </span>
                            <span class="label label-danger">3</span> 钻石耗钻
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ monthData['room_count'] }}
                            </span>
                            <span class="label label-info">4</span> 局数统计
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ monthData['money_count'] }}
                            </span>
                            <span class="label label-warning">5</span> 玩家充值金额
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ monthData['sale_report_count'] }}
                            </span>
                            <span class="label label-info">6</span> 我的售钻数
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ monthData['sub_sale_reprot_count'] }}
                            </span>
                            <span class="label label-danger">7</span> 下线代理售钻数
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ monthData['sub_buy_reprot_count'] }}
                            </span>
                            <span class="label label-warning">8</span> 下线代理购钻数
                        </li>
                        <!--
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ monthData['rate_report_count'] }}
                            </span>
                            <span class="label label-primary">9</span> 我的利润总占额
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ monthData['rate_report_agent_count'] }}
                            </span>
                            <span class="label label-success">10</span> 下线代理总占额
                        </li>
                        -->
                    </ul>
                </div>
            </div>
        </div>
        <div class="col-lg-4">
            <div class="ibox float-e-margins">
                <div class="ibox-title">
                    <h4><strong> 总计数据 </strong></h4>
                </div>
                <div class="ibox-content">
                    <ul class="list-group clear-list m-t">
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ totalData['reg_count'] }}
                            </span>
                            <span class="label label-success">1</span> 新增玩家数量
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ totalData['active_count'] }}
                            </span>
                            <span class="label label-primary">2</span> 活跃玩家数量
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ totalData['take_count'] }}
                            </span>
                            <span class="label label-danger">3</span> 钻石耗钻
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ totalData['room_count'] }}
                            </span>
                            <span class="label label-info">4</span> 局数统计
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ totalData['money_count'] }}
                            </span>
                            <span class="label label-warning">5</span> 玩家充值金额
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ totalData['sale_report_count'] }}
                            </span>
                            <span class="label label-info">6</span> 我的售钻数
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ totalData['sub_sale_reprot_count'] }}
                            </span>
                            <span class="label label-danger">7</span> 下线代理售钻数
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ totalData['sub_buy_reprot_count'] }}
                            </span>
                            <span class="label label-warning">8</span> 下线代理购钻数
                        </li>
                        <!--
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ totalData['rate_report_count'] }}
                            </span>
                            <span class="label label-primary">9</span> 我的利润总占额
                        </li>
                        <li class="list-group-item">
                            <span class="pull-right">
                                {{ totalData['rate_report_agent_count'] }}
                            </span>
                            <span class="label label-success">10</span> 下线代理总占额
                        </li>
                        -->
                    </ul>
                </div>
            </div>
        </div>
    </div>
    <div class="content" style="float:left;width:100%;position:relative;top:2.1em">
        <div class="col-lg-4">
            <div class="ibox float-e-margins">
                <div class="ibox-title">
                    <h4><strong> 当天终端系统占比 </strong></h4>
                </div>
                <div class="ibox-content">
                     <div>
                        <div id="phone_pie" style="width:100%;height:400px;"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-lg-4">
            <div class="ibox float-e-margins">
                <div class="ibox-title">
                    <h4><strong> 当天钻石游戏耗钻占比 </strong></h4>
                </div>
                <div class="ibox-content">
                    <div>
                        <div id="game_pie" style="width:100%;height:400px;"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-lg-4">
            <div class="ibox float-e-margins">
                <div class="ibox-title">
                    <h4><strong> 当天登录人数占比 </strong></h4>
                </div>
                <div class="ibox-content">
                    <div>
                        <div id="user_login_pie" style="width:100%;height:400px;"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<script type="text/javascript">
    function show_graphs(div, data) {
        var myChart = echarts.init(document.getElementById(div));
        var resizeWorldMapContainer = function () {
            document.getElementById(div).style.width = $('.panel-body').attr('width');
            document.getElementById(div).style.height = $('.panel-body').attr('height');
        };

        myChart.setOption({
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                data:  data.legend,
            },
            series : [
                {
                    name: '访问来源',
                    type: 'pie',
                    radius : '55%',
                    center: ['50%', '55%'],
                    data: data.series,
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        });

        window.onresize = function () {
            resizeWorldMapContainer();
            myChart.resize();
        };
    }
</script>
<script type="text/javascript">
    $(document).ready(function () {
        $.getJSON('/admin/statistics/temp', function (data) {
            show_graphs('phone_pie', data.phone_info);
            show_graphs('game_pie', data.game_info);
            show_graphs('user_login_pie', data.user_login_info);
        });
    });
</script>
%rebase admin_frame_base