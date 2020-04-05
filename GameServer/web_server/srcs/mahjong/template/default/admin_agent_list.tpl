<link href="{{info['STATIC_ADMIN_PATH']}}/css/select2.min.css" rel="stylesheet" />
<script src="{{info['STATIC_ADMIN_PATH']}}/js/select2.min.js"></script>
<div class="block">
    %include admin_frame_header
    <div class="content">
        <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
            <div class='col-sm-12'>
                <div style='float:right;'>
                    %if info.has_key('show_date_search'):
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
                    %end
                    <div style='float:left;margin-left:1em;'>
                     %if info['atype'] in ['0']:
                     <select class="form-control"  id="searchId" multiple="multiple" style='width:250px;height:30px;'>
                                    </select>
                        <button id="btn_search" v-bind:click="onRefresh()" class='btn btn-primary btn-sm'>
                            {{ lang.INPUT_LABEL_QUERY }}
                     </button>
                     %else:
                        <input type="text" id="searchId" placeholder="{{info['searchTxt']}}" name="id" value=""
                               style='width:200px;height:28px;'/>
                        <button id="btn_search" v-bind:click="onRefresh()" class='btn btn-primary btn-sm'>
                            {{ lang.INPUT_LABEL_QUERY }}
                        </button>
                    %end
                    </div>
                </div>
            </div>
        </div>
        <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
            <div class='col-sm-12' style='margin-left:-0.3em; margin-top:10px'>
                %if info['atype'] == '0':
                 <a href="{{info['createUrl']}}" style='color:#FFF;text-decoration:none;'>
                    <button id="btn_add" type="button" class="btn btn-sm btn-primary">
                        <i class="glyphicon glyphicon-plus"> 添加省级代理 </i>
                    </button>
                </a>
                %elif info['atype'] in ['1']:
                <a href="{{info['createUrl']}}" style='color:#FFF;text-decoration:none;'>
                    <button id="btn_add" type="button" class="btn btn-sm  btn-primary">
                        <i class="glyphicon glyphicon-plus"> 添加直属代理 </i>
                    </button>
                </a>
                %elif info['atype'] in ['2'] and info['create_auth'] == 1:
                <a href="{{info['createUrl']}}" style='color:#FFF;text-decoration:none;'>
                    <button id="btn_add" type="button" class="btn btn-sm btn-primary">
                        <i class="glyphicon glyphicon-plus"> 添加市级代理 </i>
                    </button>
                </a>
                %end
                <!-- 解 绑 规 则 -->
                <a href="javascript:;" style='color:#FFF;text-decoration:none;'>
                    <button id="btn_refresh" type="button" class="btn btn-sm btn-primary">
                        <i class="glyphicon glyphicon-plus"> 显示全部代理 </i>
                    </button>
                </a>
            </div>
        </div>
        <table id="agentTable" class="table table-bordered table-hover"></table>
    </div>
</div>
<script type="text/javascript">
    var firstDate = new Date();
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(firstDate.Format("yyyy-MM-dd"));
</script>
<script type="text/javascript">
    $('#btn_search').click(function () { //刷新代理
        start_date = $('#pick-date-start').val();
        end_date = $('#pick-date-end').val();
        searchId = $('#searchId').val();
        $('#agentTable').bootstrapTable('refresh', {'url': '{{info["listUrl"]}}' + "&searchId=" + searchId + "&start_date=" + start_date + "&end_date=" + end_date});
    });

    $('#btn_refresh').click(function () { //刷新代理
        $('#agentTable').bootstrapTable('refresh', {'url': '{{info["listUrl"]}}'});
    });

    $("#agentTable").bootstrapTable({
        url: '{{info["listUrl"]}}',
        method: 'get',
        detailView: {{ info['showPlus'] }},//父子表
        pagination: true,
        pageSize: 15,
        toolbar: '#toolbar',
        sortOrder: 'desc',
        sortName: 'regDate',
        sorttable: true,
        striped: true,
        responseHandler: responseFunc,
        queryParams: getSearchP,
        pageList: '{{PAGE_LIST}}',
        minimumCountColumns: 2,
        clickToSelect: true,
        smartDisplay: true,
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
        columns:[
        [{
            halign: "center",
            font: 15,
            align: "left",
            class: "totalTitle",
            colspan: 17
        }],
        [{
            field: 'parentId',
            title: '公会ID',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'parentAg',
            title: '代理账号',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'agentType',
            title: '代理类型',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'invite_code',
            title: '邀请码',
            align: 'center',
            valign: 'middle',
            sortable: true,
        /*
        }, {
            field: 'managers',
            title: '管理人员',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'm_num',
            title: '管理总数',
            align: 'center',
            valign: 'middle',
            sortable: true,
        */
        }, {
            field: 'allMembers',
            title: '会员总数',
            align: 'center',
            valign: 'middle',
            sortable: true,
        }, {
            field: 'members',
            sortable: true,
            title: '会员活跃数',
            align: 'center',
            valign: 'middle',
        }, {
            field: 'roomCard',
            sortable: true,
            title: '当日耗钻数',
            align: 'center',
            valign: 'middle',
        }, {
            field: 'leaf_roomcard',
            sortable: true,
            title: '剩余钻石数',
            align: 'center',
            valign: 'middle',
        /*
        }, {
            field: 'isTrail',
            title: '是否试玩',
            valign: 'middle',
            align: 'center',
            formatter: statusTrail,
        */
        }, {
            field: 'valid',
            title: '状态',
            align: 'center',
            valign: 'middle',
            sortable: true,
            formatter: status
        /*
        }, {
            field: 'recharge',
            title: '商城充钻',
            valign: 'middle',
            align: 'center',
            formatter: statusRecharge,
        }, {
            field: 'auto_check',
            title: '是否自动审核',
            valign: 'middle',
            align: 'center',
            formatter: statusCheck,
        },
        %if info['atype'] in ['0']:
        {
            field: 'create_auth',
            title: '市级公会(2)',
            valign: 'middle',
            align: 'center',
            formatter: statusCheck,
        },
        %end
        %if info['atype'] in ['0', '1', '2']:
        {
            field: 'open_auth',
            title: '仅权限者代开房',
            valign: 'middle',
            align: 'center',
            formatter:statusCheck,
        },
        %end
        */
        },{
            field: 'regDate',
            sortable: true,
            title: '创建时间',
            align: 'center',
            valign: 'middle',
        }, {
            field: 'op',
            title: '操作',
            valign: 'middle',
            formatter: getOp
        }]],
        //注册加载子表的事件。注意下这里的三个参数！
        onExpandRow: function (index, row, $detail) {
            console.log(index, row, $detail);
            InitSubTable(index, row, $detail);
        }
    });

    //初始化子表格(无线循环)
    function InitSubTable(index, row, $detail) {
        var parentAg = row.parentId;
        var cur_table = $detail.html('<table class="table-bordered table-hover definewidth" style="background-color:#428bca4d;border-color: #428bca4d;border-width: 2px 2px 2px 2px;"></table>').find('table');
        $(cur_table).bootstrapTable({
            url: '{{info["listUrl"]}}',
            method: 'get',
            detailView: false,//父子表
            contentType: "application/json",
            datatype: "json",
            cache: false,
            sortOrder: 'desc',
            sortName: 'regDate',
            striped: true,
            checkboxHeader: true,
            pagination: true,
            pageSize: 15,
            pageList: [15, 25],
            strictSearch: true,
            minimumCountColumns: 5,
            clickToSelect: true,
            smartDisplay: true,
            queryParams:getSearchP,
            columns:
            [{
                field: 'parentId',
                title: '公会ID',
                valign: 'middle',
                align: 'center',
                sortable: true
            }, {
                field: 'parentAg',
                title: '代理名称',
                align: 'center',
                valign: 'middle'
            }, {
                field: 'agentType',
                title: '代理类型',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'invite_code',
                title: '邀请码',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'managers',
                title: '管理人员',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'm_num',
                title: '管理总数',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'allMembers',
                title: '会员总数',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'members',
                title: '会员活跃数',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'roomCard',
                title: '当日耗钻数',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'leaf_roomcard',
                sortable: true,
                title: '剩余钻石数',
                align: 'center',
                valign: 'middle',
            /*
            }, {
                field: 'isTrail',
                title: '是否试玩',
                valign: 'middle',
                align: 'center',
                formatter: statusTrail,
            */
            }, {
                field: 'valid',
                title: '状态',
                align: 'center',
                valign: 'middle',
                formatter: status
            /*
            }, {
                field: 'recharge',
                title: '商城充钻',
                valign: 'middle',
                align: 'center',
                formatter: statusRecharge,
            }, {
                field: 'auto_check',
                title: '是否自动审核',
                valign: 'middle',
                align: 'center',
                formatter: statusCheck,
            },
            %if info['atype'] in ['0', '1', '2']:
            {
                field: 'open_auth',
                title: '仅权限者代开房',
                valign: 'middle',
                align: 'center',
                formatter: statusCheck,
            },
            %end
            */
            },{
                field: 'regDate',
                title: '创建时间',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'op',
                title: '操作',
                align: 'middle',
                formatter: getOp
            }],

            //注册加载子表的事件。注意下这里的三个参数！
            onExpandRow: function (index, row, $detail) {
                console.log(index, row, $detail);
                InitSubTable(index, row, $detail);
            }
        });

        //定义列操作
        function getSearchP(p) {
            sendParameter = p;
            sendParameter['id'] = parentAg;
            return sendParameter;
        }

        function responseFunc(res) {
            data = res.data;
            count = res.count;
            //实时刷

            return data;
        }
    }

    function getOp(value, row, index) {
        var comfirmList = [       //需要dialog确认打开的url
            '/admin/agent/freeze',
            '/admin/agent/trail',
            '/admin/agent/del',
            '/admin/agent/recharge',
            '/admin/agent/auto_check',
            '/admin/agent/create_auth',
            '/admin/agent/open_auth',
        ];
        eval('rowobj=' + JSON.stringify(row))
        var opList = []
        for (var i = 0; i < rowobj['op'].length; ++i) {
            var op = rowobj['op'][i];
            var str = JSON.stringify({id: rowobj['parentId']});
            var cStr = str.replace(/\"/g, "@");
            var param = rowobj['parentId'];
            if (comfirmList.indexOf(op['url']) >= 0) {
                btn_type = 'primary'
                if (op['url'].substring(op['url'].length - 3) == 'del')
                    btn_type = 'danger'
                //这里是为了一级代理不能解
                if ({{ info["atype"] }} === 1){
                    if (op["txt"] === "解冻") {
                        opList.push(String.format("<a href=\"javascript:;\" disabled='disabled' class=\"btn btn-{4} btn-sm btn-xs\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"><i class=\"glyphicon glyphicon-edit\"> {3} </i></a> ", op['url'], op['method'], cStr, op['txt'], btn_type));
                        continue;
                    }
                }
                opList.push(String.format("<a href=\"javascript:;\" class=\"btn btn-{4} btn-sm btn-xs\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"><i class=\"glyphicon glyphicon-edit\"> {3} </i></a> ", op['url'], op['method'], cStr, op['txt'], btn_type));
            } else {
                opList.push(String.format("<a href=\"{0}/{1}\" class=\"btn btn-primary btn-sm btn-xs\"><i class=\"glyphicon glyphicon-edit\"> {2}</i></a> ", op['url'], param, op['txt']));
            }
        }
        return opList.join('');
    }


    function responseFunc(res) {
        data = res.data;
        count = res.count;
        //实时刷

        $('.totalTitle').html("下线代理总数: " + count)
        var totalTitle = document.getElementsByClassName('totalTitle')[0];
        totalTitle.style.cssText = "background-color:#d9edf7;height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
        return data;
    }

    //定义列操作
    function getSearchP(p) {
        sendParameter = p;
        return sendParameter;
    }

    function status(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (rowobj['valid'] == '0') {
            statusstr = '<span class="label label-danger">冻结</span>';
        } else if (rowobj['valid'] == '1') {
            statusstr = '<span class="label label-success">有效</span>';
        }

        return [statusstr].join('');
    }

    function statusTrail(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (rowobj['isTrail'] == '0') {
            statusstr = '<span class="label label-success">正式公会</span>';
        } else if (rowobj['isTrail'] == '1') {
            statusstr = '<span class="label label-warning">试玩公会</span>';
        }

        return [statusstr].join('');
    }

    function statusRecharge(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (rowobj['recharge'] == '1') {
            statusstr = '<span class="label label-success">开放</span>';
        } else if (rowobj['recharge'] == '0') {
            statusstr = '<span class="label label-warning">未开放</span>';
        }

        return [statusstr].join('');
    }

    function statusCheck(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (value == '1') {
            statusstr = '<span class="label label-success">是</span>';
        } else if (value == '0') {
            statusstr = '<span class="label label-warning">否</span>';
        }

        return [statusstr].join('');
    }

    function statusOpen(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var statusstr = '';
        if (value == '0') {
            statusstr = '<span class="label label-success">是</span>';
        } else if (value == '1') {
            statusstr = '<span class="label label-warning">否</span>';
        }

        return [statusstr].join('');
    }

    String.format = function () {
        if (arguments.length == 0) {
            return null;
        }
        var str = arguments[0];
        for (var i = 1; i < arguments.length; i++) {
            var re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
            str = str.replace(re, arguments[i]);
        }
        return str;
    }

</script>
%if info['atype'] in ['0']:
<script>
    $("#searchId").select2({
        allowClear: true,
        closeOnSelect: false,
        language: "zh-CN",
        placeholder: " 请选择代理ID或手动输入代理ID",
        minimumInputLength: 0,
        multiple: false,
        ajax:{
            url: "/admin/bag/select/agentid",
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
%end
%rebase admin_frame_base
