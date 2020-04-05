<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<div class="cl-mcont">
  <div class="block">
            <div class="header">              
              <h3>
                %if info.get('title',None):
                  {{info['title']}}
                %end
              </h3>
            </div>
            <div class="content">
              <span id='numberTotal' style='position:relative;left:20px;font-size:14px;margin-right:20px'></span>
              <span id='rateTotal' style='position:relative;left:20px;font-size:14px;margin-right:20px'></span>
              <span id='superTotal' style='position:relative;left:20px;font-size:14px;margin-right:20px'></span>
               %include original_search_bar
               <table id="dataTable" class="table table-bordered table-hover"></table>
            </div>
  </div>
</div>
<script type="text/javascript">
  var firstDate=new Date();
  firstDate.setDate(firstDate.getDate()-6);
  $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
  $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));
  

  function initTable() {
    $('#dataTable').bootstrapTable({
          method: 'get',
          url: '{{info["listUrl"]}}',
          contentType: "application/json",
          datatype: "json",
          cache: false,
          detailView: {{openList}},
          checkboxHeader: true,
          striped: true,
          pagination: true,
          pageSize: 24,
          showExport: true,
          exportTypes:['excel', 'csv', 'pdf', 'json'],
          pageList: [24, 48, 100, 'All'],
          search: true,
          clickToSelect: true,
          //sidePagination : "server",
          //sortOrder: 'desc',
          //sortName: 'date',
          queryParams:getSearchP,
          responseHandler:responseFun,
          //onLoadError:responseError,
          showExport:true,
          exportTypes:['excel', 'csv', 'pdf', 'json'],
          // exportOptions:{fileName: "{{info['title']}}"+"_"+ new Date().Format("yyyy-MM-dd")},
          columns: [
          {
              field: 'date',
              title: '日期',
              align: 'center',
              valign: 'middle'
          },{
              field: 'id',
              title: '代理ID',
              align: 'center',
              valign: 'middle'
          },{
              field: 'account',
              title: '代理账号',
              align: 'center',
              valign: 'middle'
          },{
              field: 'count',
              title: '游戏总局数',
              align: 'center',
              valign: 'middle',
              sortable:true
          }],
          onExpandRow: function (index, row, $detail) {
              console.log(index,row,$detail);
              InitSubTable(index, row, $detail);
          }
      });

//初始化子表格(无线循环)
function InitSubTable(index, row, $detail) {
        var parentDate = row.date;
        var parentId = row.id;
        var unitPrice = row.unitPrice;
        var cur_table = $detail.html('<table table-bordered table-hover definewidth></table>').find('table');
        $(cur_table).bootstrapTable({
            url: '{{info["listUrl"]}}',
            method: 'get',
            detailView: false,
            contentType: "application/json",
            datatype: "json",
            cache: false,
            queryParams:getSearchP,
            sortOrder: 'desc',
            sortName: 'date',
            pageSize: 15,
            pageList: [15, 25],

        columns: [{
              field: 'date',
              title: '日期',
              align: 'center',
              valign: 'middle'
          },{
                  field: 'id',
                  title: '代理ID',
                  align: 'center',
                  valign: 'middle'
          },{
                  field: 'account',
                  title: '代理账号',
                  align: 'center',
                  valign: 'middle'
          },{
                  field: 'count',
                  title: '游戏总局数',
                  align: 'center',
                  valign: 'middle',
          }],
                //注册加载子表的事件。注意下这里的三个参数！
        });

        //定义列操作
        function getSearchP(p){
              sendParameter = p;
              sendParameter['id'] = parentId;
              startDate = $("#pick-date-start").val();
              sendParameter['startDate'] = startDate;
              sendParameter['date'] = parentDate;
              return sendParameter;
        }
}

        //定义列操作
        function getSearchP(p){
          startDate = $("#pick-date-start").val();
          endDate   = $("#pick-date-end").val();

          sendParameter = p;

          sendParameter['startDate'] = startDate;
          sendParameter['endDate']  = endDate;

          return sendParameter;
        }


        //获得返回的json 数据

        function responseFun(res){
            // $('#numberTotal').html(' 销售总个数: <strong style="color:#6600FF">'+res.numberTotal+'</strong>');
            // $('#rateTotal').html('我的总占额: <strong style="color:#6600FF">'+res.rateTotal+'</strong>');
            // $('#superTotal').html('上线总占额: <strong style="color:#6600FF">'+res.superTotal+'</strong>');
            data = res.data
            return data;
        }
}
</script>
%rebase admin_frame_base
