<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
          %include admin_frame_header
          <div class="content" style="float:left;width:100%;position:relative;top:2.6em">
              <table id="dataTable" class="table table-bordered table-hover"></table>
          </div>
</div>
<script type="text/javascript">

    var startDate = "{{ info['reg_date'] }}";
    var endDate   = $("#pick-date-end").val();
    $('#dataTable').bootstrapTable({
          method: 'get',
          url: '{{info["listUrl"]}}',
          contentType: "application/json",
          datatype: "json",
          cache: true,
          checkboxHeader: true,
          striped: true,
          pagination: true,
          pageSize: 15,
          pageList: [15, 50, 100,'All'],
          minimumCountColumns: 2,
          clickToSelect: true,
          responseHandler:responseFun,
          queryParams:getSearchP,
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
                          "halign":"left",
                          "align":"left",
                          "class": 'count',
                          "colspan": 11
          }],
          [{
              field: 'userId',
              title: '用户ID',
              align: 'center',
              valign: 'middle',
              sortable: true
          },{
              field: 'account',
              title: '用户账号',
              align: 'center',
              valign: 'middle',
              sortable: true
          },{
              field: 'nickname',
              title: '用户昵称',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'headImgUrl',
              title: '用户头像',
              align: 'center',
              valign: 'middle',
              sortable: true,
              formatter:getAvatorImg,
          },{
              field: 'parentAg',
              title: '所属公会',
              align: 'center',
              valign: 'middle',
              sortable: true,
          }, {
              field: 'reg_roomcard',
              title: '耗钻数',
              align: 'center',
              sortable: true,
              valign: 'middle',
              formatter: function(values){
                    return '<span style="color:red">'+ values + '</span>'
              },
              footerFormatter:function(values){
                    var count = 0;
                    for (var val in values)
                        count+=values[val].reg_roomcard
                    statusstr = String.format('<span style="color:red">{0}</span>',count);
                    return [statusstr].join('');
              }
          },{
              field: 'last_login_date',
              title: '上次登录时间',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'login_out_date',
              title: '上次登出时间',
              align: 'center',
              valign: 'middle',
              sortable: true,
          }]]
    });



      //前台查询参数
      function getSearchP(p){
          var startDate = $("#pick-date-start").val();
          var endDate   = $("#pick-date-end").val();

          sendParameter = p;
          sendParameter['startDate'] = startDate;
          sendParameter['endDate']  = endDate;

          return sendParameter;
        }

      //获得返回的json 数据
      function responseFun(res){
        $('.count').text(String.format("当前查询注册日期：{0}", startDate));
        var totalTitle = document.getElementsByClassName('count')[0];
        totalTitle.style.cssText = "background-color:#d9edf7; height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
        return res;
      }

      function responseError(status) {
          location.reload();
      }
</script>
%rebase admin_frame_base

