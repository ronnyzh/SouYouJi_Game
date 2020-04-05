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
    <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
        <div class='col-sm-12' style='margin-left:-1em;'>
            <div style='float:left;margin-left:1em;'>
                        %if info['atype'] in ['0']:
                        <select class="form-control"  id="searchId" multiple="multiple" style='width:150px;height:34px;'>
                                    </select>
                        %else:
                        <input type="text" id="searchId" placeholder=" {{info['searchTxt']}}" name="id" value=""
                               style='width:200px;height:34px;'/>
                        %end
                    </div>
                    <div style='float:left;margin-left:1em;' id="shopMail" id="shopMail">
                        <select class="form-control" style='width:150px;height:34px;'>
                            <option value=""> 商城类型（全部）</option>
                            <option value="cocogc"> 椰云</option>
                            <option value="cygse"> 创盈</option>
                        </select>
                    </div>
                    <div style='float:left;margin-left:1em;' id="exchangeType" id="exchangeType">
                        <select class="form-control" style='width:150px;height:34px;'>
                            <option value=""> 兑换状态（全部）</option>
                            <option value="successful"> 兑换成功</option>
                            <option value="failed"> 兑换失败</option>
                        </select>
                    </div>
        </div>
    </div>
        <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
            <div class='col-sm-12' style='margin-left:-1em; margin-top:10px'>
                <div style='float:left;margin-left:1em;' class="input-group date datetime col-md-1 col-xs-1"
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
                        <button id="btn_lastMonth" class='btn btn-sm'>{{lang.INPUT_LABEL_PREV_MONTH}}</button>
                        <button id="btn_thisMonth" class='btn btn-sm'>{{lang.INPUT_LABEL_CURR_MONTH}}</button>
                        <button id="btn_lastWeek" class='btn btn-sm'>{{lang.INPUT_LABEL_PREV_WEEK}}</button>
                        <button id="btn_thisWeek" class='btn btn-sm'>{{lang.INPUT_LABEL_CURR_WEEK}}</button>
                        <button id="btn_yesterday" class='btn btn-sm'>{{lang.INPUT_LABEL_PREV_DAY}}</button>
                        <button id="btn_today" class='btn btn-sm'>{{lang.INPUT_LABEL_CURR_DAY}}</button>
                        <button id="btn_search" v-bind:click="onRefresh()" class='btn btn-primary btn-sm'>
                            {{lang.INPUT_LABEL_QUERY}}
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <table id="dataTable" class="table table-bordered table-hover"></table>
</div>
<script type="text/javascript">
    $('#btn_search').click(function () {
        $('#dataTable').bootstrapTable('refresh', {"url": '{{info["listUrl"]}}'});
    });

    var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 6);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-start').val(new Date().Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));
    function initTable() {
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
        pageList: [15,50,100,'All'],
        clickToSelect: true,
        sortOrder: 'desc',
        sortName: 'date',
        queryParams:getSearchP,
        responseHandler:responseFun,
        showFooter:true, //添加页脚做统计
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
                align: "left",
                size: '50',
                class: 'info',
                colspan: 15
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
                field: 'account',
                title: '用户账号',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'nickname',
                title: '用户昵称',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'beforePoint',
                title: '兑换前积分',
                align: 'center',
                valign: 'middle',
                sortable: true,
                footerFormatter:function(values){
                  return '兑换总数';
               }
            }, {
                field: 'pointNum',
                title: '兑换积分',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: function (value) {
                    return '<span class="label label-primary">' +  value  + '</span>'
                },
                footerFormatter:function(values){
                  var count = 0;
                  for (var val in values)
                      count+=parseInt(values[val].pointNum)
                  return colorFormat(count);
               }
            }, {
                field: 'afterPoint',
                title: '兑换后积分',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'shopMail',
                title: '商城',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: function (value) {
                    if (value == 'cocogc') {
                        return '<span class="label label-primary">椰云</span>'
                    } else {
                        return '<span class="label label-info">创盈</span>'
                    }
                }
            }, {
                field: 'type',
                title: '兑换状态',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: function (value) {
                    if (value == 'successful') {
                        return '<span class="label label-success">兑换成功</span>'
                    } else {
                        return '<span class="label label-danger">兑换失败</span>'
                    }
                }
            }, {
                field: 'startTime',
                title: '兑换操作时间',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'endTime',
                title: '兑换完成时间',
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

    function colorFormat(value,color){  //颜色格式化
            fontColor = color || '#1E9FFF'; //#1E9FFF
            statusstr = String.format('<span style="color:{0}">{1}</span>',fontColor,value);

            return [statusstr].join('');
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
        var searchId = $("#searchId").val();
        var startDate = $("#pick-date-start").val();
        var endDate = $("#pick-date-end").val();
        var exchangeType = $('#exchangeType option:selected').val();
        var shopMail = $('#shopMail option:selected').val();
        sendParameter = p;

        sendParameter['searchId'] = searchId;
        sendParameter['startDate'] = startDate;
        sendParameter['endDate'] = endDate;
        sendParameter['exchangeType'] = exchangeType;
        sendParameter['shopMail'] = shopMail;
        return sendParameter;
    }

    //获得返回的json 数据
    function responseFun(res) {
        var startDate = $('#pick-date-start').val();
        var endDate = $('#pick-date-end').val();
        var searchId = $("#searchId").val();
        var data = res.data
        var count = res.total;
        var img = res.headImgUrl;
        var name = res.name || '<font color="red">请输入要查询的玩家编号</font>';
        if (searchId){
            $('.info').html("玩家名称：" + name + "&nbsp;  玩家头像：<img src='" + img + "' width='30' height='30' />");
        }else{
            $('.info').html("玩家数据");
        }
        var totalMoney = document.getElementsByClassName('info')[0];
        totalMoney.style.cssText = "height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
        return data
    }
}
</script>
<script>
    $("#searchId").select2({
        allowClear: true,
        closeOnSelect: false,
        language: "zh-CN",
        placeholder: " 请选择用户ID",
        minimumInputLength: 0,
        multiple: false,
        ajax:{
            url: "{{ info['searchUrl'] }}",
            dataType:"json",
            delay:250,
            data:function(params){
                return {
                    name: params.term,
                    page: params.page || 1,
                };
            },
            cache: true,
            processResults: function (res, params) {
                var users = res["data"]["users"];
                var options = [];
                for(var i= 0, len=users.length;i<len;i++){
                    var option = {"id":users[i]["id"], "text":users[i]["name"]};
                    options.push(option);
                }
                return {
                    results: options,
                    pagination: {
                        more:res["data"]["more"]
                    }
                };
            },
            escapeMarkup: function (markup) { return markup; },
        }
    });
</script>
%rebase admin_frame_base

