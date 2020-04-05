<link rel="stylesheet" href="{{info['STATIC_ADMIN_PATH']}}/layer/mobile/need/layer.css" media="all">
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/layerMobile/layer.js?{{RES_VERSION}}"></script>
<div class="block">
    %include admin_frame_header
    <div class="content" style="float:left;width:100%;position:relative;top:2.6em">
        <div style='clear:both'></div>
        <table id="agentTable" class="table table-bordered table-hover"></table>
    </div>
</div>
<script type="text/javascript">
    $("#agentTable").bootstrapTable({
        url: '{{ info.get("listUrl") }}',
        method: 'get',
        contentType: "application/json",
        datatype: "json",
        cache: true,
        checkboxHeader: true,
        striped: true,
        pagination: true,
        pageSize: 15,
        pageList: [15, 50, 100, 'All'],
        sortOrder: "desc",
        sortName: 'status',
        minimumCountColumns: 2,
        clickToSelect: true,
        responseHandler: responseFunc,
        queryParams: getSearchP,                     //是否启用排序
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
                class: "totalTitle",
                colspan: 17
            }],
            [{
                field: 'txt',
                title: '权限名称',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'agentType',
                title: '权限说明',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'isOpen',
                title: '是否开启',
                align: 'center',
                valign: 'middle',
                formatter: isOpen
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

    function isOpen(value, row, index) {
        eval('var rowobj=' + JSON.stringify(row))
        var isOpenStr = '';
        if (rowobj['isOpen'] == true) {
            isOpenStr = "<label for='reward_name' class='hitLabel' style='float:center;line-height:30px;font-weight:bold'>√</label>";
        } else if (rowobj['isOpen'] == false) {
            isOpenStr = "<label for='reward_name' class='hitLabel' style='float:center;line-height:30px;font-weight:bold''>☓</label>";
        }

        return [isOpenStr].join('');
    }

    function getOp(value,row,index){
      eval('rowobj='+JSON.stringify(row))
      var opList = []
      for (var i = 0; i < rowobj['op'].length; ++i) {
          var op = rowobj['op'][i];
          var str = JSON.stringify({url : rowobj['url'], isOpen : rowobj['isOpen'], account : "{{ info['account'] }}"});
          var cStr = str.replace(/\"/g, "@");
          if(op['txt'] == '关闭'){
            btn = 'danger'
          }else{
            btn = 'primary'
          }
          if(op['url'] == '/admin/agent/role/modify'){
             opList.push(String.format("<a href=\"#\" class=\"btn btn-{4} btn-sm btn-xs\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"><i class=\"glyphicon glyphicon-edit\"> {3} </i></a> ", op['url'], op['method'], cStr, op['txt'], btn));
          }
      }
      return opList.join('');
    }

    function responseFunc(res) {
        var data = res.data;
        var account = res.account;
        var role = res.role;
        //实时刷
        totalStr = String.format("代理 ：{0} ，角色 ：{1}", account, role)
        $('.totalTitle').html(totalStr);
        var totalClass = document.getElementsByClassName('totalTitle')[0];
        totalClass.style.cssText = "background-color:#d9edf7;height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
        return data;
    }

    //定义列操作
    function getSearchP(p) {
        sendParameter = p;
        return sendParameter;
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
%rebase admin_frame_base
