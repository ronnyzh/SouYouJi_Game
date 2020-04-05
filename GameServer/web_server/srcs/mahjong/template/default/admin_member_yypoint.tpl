<link href="{{info['STATIC_ADMIN_PATH']}}/css/select2.min.css" rel="stylesheet" />
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script src="{{info['STATIC_ADMIN_PATH']}}/js/select2.min.js"></script>
<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
    %include admin_frame_header
    <div class="content">
        <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
            <div class='col-sm-12'>
                <div style='float:left;'>
                    <div style='float:left;margin-left:0em;' class="input-group date datetime col-md-1 col-xs-1"
                         data-min-view="2" data-date-format="yyyy-mm-dd">
                        <input class="form-control" size="18" type="text" style='width:140px;height:28px;'
                               id='pick-date-start'
                               name="startdate" value="{{lang.INPUT_LABEL_START_DATE_TXT}}" readonly>
                        <span class="input-group-addon btn btn-primary pickdate-btn"><span
                                class="glyphicon pickdate-btn pickdate glyphicon-th"></span>
                    </div>
                    <div style='float:left;margin-left:1em;' class="input-group date datetime col-md-1 col-xs-1"
                         data-min-view="2" data-date-format="yyyy-mm-dd">
                        <input class="form-control" style='width:140px;height:28px;' id='pick-date-end' name="enddate"
                               size="18"
                               type="text" value="{{lang.INPUT_LABEL_END_DATE_TXT}}" readonly>
                        <span class="input-group-addon btn btn-primary pickdate-btn"><span
                                class="pickdate glyphicon pickdate-btn glyphicon-th"></span></span>
                    </div>
                    <div style='float:left;margin-left:1em;'>
                        <input type="text" id="searchId" placeholder=" {{info['searchTxt']}}" name="id" value=""
                               style='width:200px;height:30px;'/>
                        <button id="btn_search" v-bind:click="onRefresh()" class='btn btn-primary btn-sm'>
                            {{lang.INPUT_LABEL_QUERY}}
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <table id="dataTable" class="table table-bordered table-hover"></table>
    </div>
</div>
<script type="text/javascript">
    var firstDate = new Date();
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(firstDate.Format("yyyy-MM-dd"));
</script>
<script type="text/javascript">
    $('#btn_search').click(function () {

        $('#dataTable').bootstrapTable('refresh', {"url": '{{info["listUrl"]}}'});
    });

    var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 6);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));

    $('#dataTable').bootstrapTable({

        method: 'get',
        url: '{{info["listUrl"]}}',
        contentType: "application/json",
        datatype: "json",
        cache: false,
        striped: true,
        toolbar: '#toolbar',
        pagination: true,
        pageSize: 15,
        pageNumber: parseInt("{{info['cur_page']}}"),
        pageList: [15, 50, 100],
        queryParamsType: '',
        sidePagination: "server",
        minimumCountColumns: 2,
        clickToSelect: true,
        responseHandler: responseFun,
        queryParams: getSearchP,
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
                align: "left",
                size: '50',
                class: 'info',
                colspan: 9
                }
            ], [{
                field: 'date',
                title: '日期',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'userId',
                title: '用户ID',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'type',
                title: '类型',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'desc',
                title: '说明',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'value',
                title: '数值',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: function (value) {
                    value = parseFloat(value);
                    if (value > 0) {
                        return '<span class="label label-primary">+' + value +'</span>'
                    } else {
                        return '<span class="label label-danger">' + value +'</span>'
                    }
                }
            }, {
                field: 'total',
                title: '余额',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }]]
    });


    function getColorCredit(value, row, index) {
        if (parseInt(value) > 0)
            infoStr = String.format("<span style=\"color:red;\">+{0}</span>", value);
        else
            infoStr = String.format("<span style=\"color:green;\">{0}</span>", value);
        return [
            infoStr
        ].join('');
    }

    function getOp(value, row, index) {
        var comfirmUrls = [
            '/admin/member/kick',
            '/admin/member/freeze'
        ];
        eval('rowobj=' + JSON.stringify(row))
        var opList = []
        for (var i = 0; i < rowobj['op'].length; ++i) {
            var op = rowobj['op'][i];
            var str = JSON.stringify({id: rowobj['id']});
            var cStr = str.replace(/\"/g, "@");
            if (comfirmUrls.indexOf(op['url']) >= 0)
                opList.push(String.format("<a href=\"#\" class=\"btn btn-primary btn-xs\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"><i class=\"fa fa-edit\"> {3} </i></a> ", op['url'], op['method'], cStr, op['txt']));
            else
                opList.push(String.format("<a href=\"{0}?id=" + rowobj['id'] + "\" class=\"btn btn-primary btn-xs\" ><i class=\"fa fa-edit\"> {1} </i></a> ", op['url'], op['txt']));
        }
        return opList.join('');
    }


    function getColor(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        statusstr = '<span style="color:#6600FF">' + value + '</span>';

        return [statusstr].join('');
    }

    //定义列操作
    function getSearchP(p) {
        searchId = $("#searchId").val();
        startDate = $("#pick-date-start").val();
        endDate = $("#pick-date-end").val();

        sendParameter = p;

        sendParameter['searchId'] = searchId;
        sendParameter['startDate'] = startDate;
        sendParameter['endDate'] = endDate;

        return sendParameter;
    }

    //获得返回的json 数据
    function responseFun(res) {
        startDate = $('#pick-date-start').val();
        endDate = $('#pick-date-end').val();
        count = res.total;
        img = res.headImgUrl;
        name = res.name || '<font color="red">请输入要查询的玩家编号</font>';
        $('.info').html("玩家名称：" + name + "&nbsp;  玩家头像：<img src='" + img + "' width='30' height='30' />");
        var totalMoney = document.getElementsByClassName('info')[0];
        totalMoney.style.cssText = "height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
        return {
            "rows": res.data,
            "total": res.total
        };
    }
</script>
%rebase admin_frame_base

