<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/echarts.common.min.js"></script>
<div class='rows' style='margin-bottom:10px;'>
    <div class='col-md-12'>
        <div class="panel panel-info">
            <div class="panel-heading">
                <h3 class="panel-title">近一周统计数据</h3>
            </div>
            <div class="panel-body">
                <div id="main" style="width:100%;height:400px;"></div>
            </div>
        </div>
    </div>
</div>
<script type="text/javascript">
    // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main'));
        var resizeWorldMapContainer = function () {
            document.getElementById('main').style.width = $('.panel-body').attr('width');
            document.getElementById('main').style.height = $('.panel-body').attr('height');

        };
        resizeWorldMapContainer();
        // 指定图表的配置项和数据
        $.getJSON('/admin/gold/operate/detail',function(data){
            myChart.setOption({
                    tooltip : {
                        trigger: 'axis'
                    },
                    legend: {
                        data:['每日在线玩家数','每日房间数','玩家拥有金币总数']
                    },
                    calculable : true,
                    toolbox: {
                        show : true,
                        feature : {
                            mark : {show: true},
                            dataView : {show: true, readOnly: false},
                            magicType : {show: true, type: ['line', 'bar','tiled']},
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
                    },
                    xAxis : [
                        {
                            type : 'category',
                            boundaryGap : false,
                            data : data.week
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value'
                        }
                    ],
                    series : [
                        {
                            name:'每日在线玩家数',
                            type:'line',                            
                            data:data.reg_list
                        },
                        {
                            name:'每日房间数',
                            type:'line',                            
                            data:data.login_list
                        },
                        {
                            name:'玩家拥有金币总数',
                            type:'line',                            
                            data:data.take_list
                        }
                    ]
                });
        });

        // 使用刚指定的配置项和数据显示图表。
        window.onresize = function () {
            //重置容器高宽
            resizeWorldMapContainer();
            myChart.resize();
        };
</script>
