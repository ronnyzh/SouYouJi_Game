<div class="block">
        %include admin_frame_header
        <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
            <div class='col-sm-12'>
                <div style='float:left;'>
                     <div style='float:left;margin-left:-0.3em;'>
                        <a id="add" href="{{info['addGMUrl']}}" style='color:#FFF;text-decoration:none;'>
                            <button id="btn_add" type="button" class="btn btn-sm btn-primary">
                                <i class="glyphicon glyphicon-plus"> 添加GM</i>
                            </button>
                        </a>
                    </div>
                    <div style='float:left;margin-left:0.3em;'>
                        <a id="add" href="javascript:;" style='color:#FFF;text-decoration:none;'>
                            <button id="btn_add" type="button" onclick="_settingBatchGm()" class="btn btn-sm btn-primary">
                                <i class="glyphicon glyphicon-plus"> 批量解除GM </i>
                            </button>
                        </a>
                    </div>
                     <div style='float:right;margin-left:1em;'>
                          <input type="text" id="searchId"  placeholder=" {{info['searchTxt']}}" name="id" value="" style='width:200px;height:30px;'/>
                           <button id="btn_search" v-bind:click="onRefresh()" class='btn btn-primary btn-sm'>{{lang.INPUT_LABEL_QUERY}}</button>
                      </div>
                </div>
            </div>
        </div>
        <div style='clear:both'></div>
          <table id="dataTable" class="table table-bordered table-hover table-striped"></table>
        </div>
</div>
<script type="text/javascript">
    $('#btn_search').click(function(){
            $('#dataTable').bootstrapTable('refresh');
    });

    startDate = $("#pick-date-start").val();
    endDate   = $("#pick-date-end").val();
    $('#dataTable').bootstrapTable({
          method: 'get',
          url: '{{info["listUrl"]}}',
          contentType: "application/json",
          datatype: "json",
          cache: true,
          checkboxHeader: true,
          pagination: true,
          pageSize: 15,
          pageList: "{{PAGE_LIST}}",
          queryParamsType:'',
          sidePagination:"server",
          toolbar:'#toolbar',
          clickToSelect: true,
          responseHandler:responseFun,
          queryParams:getSearchP,
          sortOrder: 'asc',
          sortable: true,                     //是否启用排序
          sortName:'id',
          striped: true,
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
          [
                {
                    "align":"center",
                    "hlign":"center",
                    "class":"count",
                    "colspan": 15
                }
          ],
          [{
              checkbox: true
          },{
              field: 'id',
              title: '用户编号',
              align: 'center',
              valign: 'middle',
              sortable: true
          },{
              field: 'name',
              title: '用户名称',
              align: 'center',
              valign: 'middle',
              sortable: true
          },{
              field: 'account',
              title: '账号',
              align: 'center',
              valign: 'middle',
              sortable: true
          },{
              field: 'op',
              title: '操作',
              align: 'center',
              valign: 'middle',
              formatter:getOp
          }]]
    });


        function getOp(value,row,index){
            var confirmDiologUrls = [   //需要弹框确认的url
              '/admin/member/gm/kick'
            ];
            var showHisUrls  =  [  // 需要弹窗显示的数据
              '/admin/member/gm/showHis'
            ];
            eval('rowobj='+JSON.stringify(row))
            var opList = []
            for (var i = 0; i < rowobj['op'].length; ++i) {
                var op = rowobj['op'][i];
                var str = JSON.stringify({id : rowobj['account']});
                var cStr = str.replace(/\"/g, "@");
                if(confirmDiologUrls.indexOf(op['url'])>=0){
                    btn_type = 'primary';
                    if (op['url'].substring(op['url'].length-4)=='kick')
                        btn_type = 'danger';
                    opList.push(String.format("<a href=\"#\" class=\"btn btn-{4} btn-sm\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\">{3}</a> ", op['url'], op['method'], cStr, op['txt'],btn_type));
                }else if(showHisUrls.indexOf(op['url'])>=0){
                    opList.push(String.format("<a href=\"#\" class=\"btn btn-primary btn-sm\" onclick=\"showGmHisDialog(\'{0}\', \'{1}\', \'{2}\')\">{3}</a> ", op['url'], op['method'], rowobj['id'], op['txt']));
                }else{
                    opList.push(String.format("<a href=\"{0}?id="+rowobj['id']+"\" class=\"btn btn-primary btn-sm\" >{1}</a> ", op['url'],op['txt']));
                }
            }
            return opList.join('');
        }


          //前台查询参数

        function getSearchP(p){
            // account = $("#account").val();
            // member_level = $('#member_level').val();
            // member_status = $("#member_status").val();
            // userId = $("#userId").val();
            searchId = $("#searchId").val();

            sendParameter = p;
            sendParameter['searchId']  = searchId;

            return sendParameter;
          }

        //获得返回的json 数据
        function responseFun(res){
            $('.count').text(String.format("GM总数：{0}", res.total));
            var totalTitle = document.getElementsByClassName('count')[0];
            totalTitle.style.cssText = "background-color:#d9edf7; height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
            return {"rows": res.result,
                "total": res.total};
        }

        function responseError(status) {
            location.reload();
        }

        function _settingBatchGm(){
          var userIds = $.map($('#dataTable').bootstrapTable('getSelections'),function(row){
              return row.account;
          });

          if (!userIds.length){    //如果没选择直接return
              console.log('---------------had not selected.. return');
              return;
          }

          var remoteUrl = "{{info['removeUrl']}}",
              method    = "GET",
              jsonStr   = {'id':userIds.join(',')}

          console.log('----------------select gameIds['+userIds+']');
          formAjax(remoteUrl,method,jsonStr,'正在设置...,');
        }
</script>
%rebase admin_frame_base
