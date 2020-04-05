<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
    %include admin_frame_header
    <div class="content">
        %include original_search_bar
        <table id="dataTable" class="table table-bordered table-hover"></table>
    </div>
</div>
<script type="text/javascript">
    var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 6);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));

    /**------------------------------------------------
     *  代理操作日志
     -------------------------------------------------
     */
    function initTable() {
        startDate = $("#pick-date-start").val();
        endDate = $("#pick-date-end").val();
        $("#dataTable").bootstrapTable({
            url: "{{info['tableUrl']}}",
            method: 'get',
            pagination: true,
            pageSize: 15,
            search: true,
            showRefresh: true,
            showColumns: true,
            showToggle: true,
            showExport:true,
            showFooter: true,
            cardView: false,
            exportDataType: 'all',
            exportTypes:[ 'csv', 'txt', 'sql', 'doc', 'excel', 'xlsx', 'pdf'],
            exportOptions:{
                fileName: '{{ info["title"] }}',
            },
            pageList: [15, 25],
            responseHandler: responseFun,
            queryParams: getSearchP,
            columns: [
            [{
                    "halign":"center",
                    "align":"center",
                    "class":'totalMoney',
                    "colspan":15
            }],
            [{
                field: 'cardNums',
                sortable: true,
                align: 'center',
                valign: 'middle',
                title: '售钻数(张)',
                footerFormatter:function(values){
                       return '订单总计:'
                    }
            }, {
                field: 'applyAccount',
                align: 'center',
                valign: 'middle',
                title: '买钻方',
                footerFormatter:function(values){
                       var count = 0 ;
                       for (var val in values)
                            count+=parseFloat(values[val].cardNums)

                       return colorFormat(count.toFixed(2))
                }
            }, {
                field: 'saleAccount',
                align: 'center',
                valign: 'middle',
                title: '卖钻方'
            }, {
                field: 'status',
                title: '订单状态',
                align: 'center',
                valign: 'middle',
                formatter: status
            }, {
                field: 'finish_date',
                align: 'center',
                valign: 'middle',
                sortable: true,
                title: '系统确认时间'
            }, {
                field: 'op',
                title: '操作',
                align: 'center',
                valign: 'middle',
                formatter: getOp
            }]],

            //注册加载子表的事件。注意下这里的三个参数！
            onExpandRow: function (index, row, $detail) {
                console.log(index, row, $detail);
                InitSubTable(index, row, $detail);
            }
        });

        function status(value, row, index) {
            eval('var rowobj=' + JSON.stringify(row))
            var statusstr = '';
            if (rowobj['status'] == '0') {
                statusstr = '<span class="label label-danger">卖钻方未确认</span>';
            } else if (rowobj['status'] == '1') {
                statusstr = '<span class="label label-success">卖钻方已确认</span>';
            }

            return [
                statusstr
            ].join('');
        }

        function colorFormat(value,color){  //颜色格式化
            fontColor = color || '#1E9FFF'; //#1E9FFF
            statusstr = String.format('<span style="color:{0}">{1}</span>',fontColor,value);

            return [statusstr].join('');
        }

        function getSearchP(p) {
            startDate = $("#pick-date-start").val();
            endDate = $("#pick-date-end").val();

            sendParameter = p;

            sendParameter['startDate'] = startDate;
            sendParameter['endDate'] = endDate;

            return sendParameter;
        }

        function getOp(value, row, index) {
            eval('rowobj=' + JSON.stringify(row))
            var opList = []
            for (var i = 0; i < rowobj['op'].length; ++i) {
                var op = rowobj['op'][i];
                var str = JSON.stringify({orderNo: rowobj["orderNo"]});
                var cStr = str.replace(/\"/g, "@");
                if (rowobj['status'] == '1')
                    continue;
                var contentUrl = op['url'];
                opList.push(String.format("<a href=\"#\" class=\"btn btn-primary btn-sm\" onclick=\"comfirmOrderDialog(\'{0}\',\'{1}\',\'{2}\')\"><i class=\"glyphicon glyphicon-edit\"> {3} </i></a> ", contentUrl, op['method'], cStr, op['txt']));
            }
            return opList.join('');
        }

        //获得返回的json 数据
        function responseFun(res) {
            top_show_str = String.format("搜索日期：{0} 至 {1}", startDate, endDate);
            $('.totalMoney').html(top_show_str)
            var totalMoney = document.getElementsByClassName('totalMoney')[0];
            totalMoney.style.cssText = "background-color:#d9edf7;height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            return res
        }
    }
</script>
%rebase admin_frame_base