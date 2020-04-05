<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<div class="block">
    %include admin_frame_header
    <div class="content">
        <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
            <div class='col-sm-12' style='margin-left:1em;'>
                %if info.has_key('group_search'):
                <!-- 查询代理ID -->
                <div style='float:left;margin-left:-1em;'>
                    <input type="text" id="group_id"  placeholder=" 请输入代理ID" name="group_id" value="" style='width:150px;height:30px;'/>
                </div>
                %end
                <div style='float:left;margin-left:1em;' class="input-group date datetime col-md-1 col-xs-1"
                     data-min-view="2" data-date-format="yyyy-mm-dd">
                    <input class="form-control" size="12" type="text" style='width:140px;height:28px;'
                           id='pick-date-start' name="startdate" value="{{lang.INPUT_LABEL_START_DATE_TXT}}" readonly>
                    <span class="input-group-addon btn btn-primary pickdate-btn"><span
                            class="glyphicon pickdate-btn pickdate glyphicon-th"></span>
                </div>

                <div style='float:left;margin-left:1em;' class="input-group date datetime col-md-1 col-xs-1"
                     data-min-view="2" data-date-format="yyyy-mm-dd">
                    <input class="form-control" style='width:140px;height:28px;' id='pick-date-end' name="enddate"
                           size="12" type="text" value="{{lang.INPUT_LABEL_END_DATE_TXT}}" readonly>
                    <span class="input-group-addon btn btn-primary pickdate-btn"><span
                            class="pickdate glyphicon pickdate-btn glyphicon-th"></span></span>
                </div>
                <div style='float:left;margin-left:1em;'>
                    <button id="btn_query" class='btn btn-primary btn-sm'>{{lang.INPUT_LABEL_QUERY}}</button>
                    <button id="btn_lastMonth" class='btn btn-sm'>{{lang.INPUT_LABEL_PREV_MONTH}}</button>
                    <button id="btn_thisMonth" class='btn btn-sm'>{{lang.INPUT_LABEL_CURR_MONTH}}</button>
                    <button id="btn_lastWeek" class='btn btn-sm'>{{lang.INPUT_LABEL_PREV_WEEK}}</button>
                    <button id="btn_thisWeek" class='btn btn-sm'>{{lang.INPUT_LABEL_CURR_WEEK}}</button>
                    <button id="btn_yesterday" class='btn btn-sm'>{{lang.INPUT_LABEL_PREV_DAY}}</button>
                    <button id="btn_today" class='btn btn-sm'>{{lang.INPUT_LABEL_CURR_DAY}}</button>
                    <div class='clearfix'></div>
                </div>
            </div>
        </div>
        <table id="dataTable" class="table table-bordered table-hover"></table>
    </div>
</div>
<script type="text/javascript">
    var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 6);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));
</script>
<script type="text/javascript">

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
            pageSize: 15,
            pageList: [15, 50, 100, 'All'],
            clickToSelect: true,
            sortOrder: 'desc',
            sortName: 'date',
            queryParams: getSearchP,
            responseHandler: responseFun,
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
            columns: [
                [{
                    halign: "center",
                    font: 15,
                    align: "left",
                    class: "count",
                    colspan: 17
                }],
                [{
                    field: 'date',
                    title: '日期',
                    align: 'center',
                    valign: 'middle'
                }, {
                    field: 'account',
                    title: '代理账号',
                    align: 'center',
                    valign: 'middle'
                }, {
                    field: 'aId',
                    title: '代理ID',
                    align: 'center',
                    sortable: true,
                    valign: 'middle',
                    footerFormatter: function (values) {
                        return "总计:"
                    }
                }, {
                    field: 'cards',
                    title: '当日购钻数',
                    align: 'center',
                    sortable: true,
                    valign: 'middle',
                    footerFormatter: function (values) {
                        var count = 0;
                        for (var val in values)
                            count += parseInt(values[val].cards);

                        return colorFormat(count);
                    }
                }, {
                    field: 'cardNumsTotal',
                    title: '总购钻数',
                    align: 'center',
                    sortable: true,
                    valign: 'middle',
                    footerFormatter: function (values) {
                        var count = 0;
                        for (var val in values)
                            count += parseInt(values[val].cardNumsTotal);

                        return colorFormat(count)
                    }
                }]]
        });

        //定义列操作
        function getSearchP(p) {
            startDate = $("#pick-date-start").val();
            endDate = $("#pick-date-end").val();
            group_id = $("#group_id").val();

            sendParameter = p;

            sendParameter['startDate'] = startDate;
            sendParameter['endDate'] = endDate;
            sendParameter['group_id'] = group_id;

            return sendParameter;
        }

        //获得返回的json 数据
        function responseFun(res) {
            $('.count').text(String.format("当前查询日期：{0} ~ {1}", startDate, endDate));
            var totalTitle = document.getElementsByClassName('count')[0];
            totalTitle.style.cssText = "background-color:#d9edf7; height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            data = res.result
            return data;
        }
    }
</script>
%rebase admin_frame_base
