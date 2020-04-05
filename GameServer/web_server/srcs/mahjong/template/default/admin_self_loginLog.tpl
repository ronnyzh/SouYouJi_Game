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
     *
     -------------------------------------------------
     */
    function initTable() {
        startDate = $("#pick-date-start").val();
        endDate = $("#pick-date-end").val();
        $('#dataTable').bootstrapTable({
            method: 'get',
            url: '{{info["listUrl"]}}',
            contentType: "application/json",
            datatype: "json",
            cache: false,
            checkboxHeader: true,
            striped: true,
            pagination: true,
            pageSize: 24,
            pageList: [24, 48, 100, 'All'],
            clickToSelect: true,
            sortOrder: 'desc',
            sortName: 'datetime',
            queryParams: getSearchP,
            responseHandler: responseFun,
            search: true,
            showRefresh: true,
            showColumns: true,
            showToggle: true,
            showExport:true,
            showFooter: true,
            cardView: false,
            exportTypes:[ 'csv', 'txt', 'sql', 'doc', 'excel', 'xlsx', 'pdf'],
            columns: [
                [{
                    halign: "center",
                    font: 15,
                    align: "left",
                    class: "total",
                    colspan: 17
                }],
                [{
                    field: 'account',
                    title: '登录账号',
                    align: 'center',
                    valign: 'middle'
                }, {
                    field: 'type',
                    title: '登录状态',
                    align: 'center',
                    valign: 'middle',
                    formatter: status,
                }, {
                    field: 'datetime',
                    title: '登录时间',
                    align: 'center',
                    valign: 'middle'
                }, {
                    field: 'ip',
                    title: '登录IP',
                    align: 'center',
                    valign: 'middle',
                }]]
        });

        function status(value, row, index) {
            if (parseInt(value) == 1)
                infoStr = String.format("<span class=\"label label-success\">{0}</span>", '成功');
            else if (parseInt(value) == 2)
                infoStr = String.format("<span class=\"label label-danger\">{0}</span>", '密码错误');
            else
                infoStr = String.format("<span class=\"label label-danger\">{0}</span>", '未知错误');
            return [
                infoStr
            ].join('');
        }

        //定义列操作
        function getSearchP(p) {
            startDate = $("#pick-date-start").val();
            endDate = $("#pick-date-end").val();

            sendParameter = p;

            sendParameter['startDate'] = startDate;
            sendParameter['endDate'] = endDate;

            return sendParameter;
        }

        //获得返回的json 数据
        function responseFun(res) {
            $('.total').text(String.format("当前查询日期：{0} ~ {1}", startDate, endDate));
            var totalTitle = document.getElementsByClassName('total')[0];
            totalTitle.style.cssText = "background-color:#d9edf7;height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            return res;
        }
    }
</script>
%rebase admin_frame_base
