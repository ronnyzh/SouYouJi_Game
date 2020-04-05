<link href="{{info['STATIC_ADMIN_PATH']}}/css/select2.min.css" rel="stylesheet" />
<script src="{{info['STATIC_ADMIN_PATH']}}/js/select2.min.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
<div class="block">
    %include admin_frame_header
    <div class="content">
        <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
            <div class='col-sm-12'>
                  <div style='float:left;'>
                      <div style='float:left;margin-left:0em;'>
                        %if info['a_type'] in ['0']:
                        <select class="form-control"  id="searchId" multiple="multiple" style='width:250px;height:30px;'>
                                    </select>
                         <button id="btn_search" v-bind:click="onRefresh()" class='btn btn-primary btn-sm'>{{lang.INPUT_LABEL_QUERY}}</button>
                        %else:
                        <input type="text" id="searchId"  placeholder=" {{info['searchTxt']}}" name="id" value="" style='width:200px;height:30px;'/>
                        <button id="btn_search" v-bind:click="onRefresh()" class='btn btn-primary btn-sm'>{{lang.INPUT_LABEL_QUERY}}</button>
                        %end
                      </div>
                  </div>
            </div>
    </div>
    <div style='clear:both'></div>
        <table id="dataTable" class="table table-bordered table-hover"></table>
     </div>
</div>
<script type="text/javascript">
    var pageNumber;
    $('#btn_search').click(function(){
          $('#dataTable').bootstrapTable('refresh');
    });

    $('#dataTable').bootstrapTable({
          method: 'get',
          url: '{{info["listUrl"]}}',
          contentType: "application/json",
          datatype: "json",
          cache: false,
          striped: true,
          toolbar:'#toolbar',
          pagination: true,
          pageSize: 15,
          pageNumber:parseInt("{{info['cur_page']}}"),
          pageList: [15, 50, 100],
          queryParamsType:'',
          sidePagination:"server",
          minimumCountColumns: 2,
          clickToSelect: true,
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
          responseHandler:responseFun,
          queryParams:getSearchP,
          onSort:getCellSortByClick,
          columns: [
          [{
             "halign":"center",
             "align":"center",
             "class":'totalTitle',
             "colspan": 25
          }],
          [{
              field: 'id',
              title: '用户编号',
              align: 'center',
              valign: 'middle',
              sortable: true
          },{
              field: 'headImgUrl',
              title: '用户头像',
              align: 'center',
              valign: 'middle',
              formatter:getAvatorImg,
          },{
              field: 'name',
              title: '用户账号',
              align: 'center',
              valign: 'middle'
          },{
              field: 'nickname',
              title: '用户昵称',
              align: 'center',
              valign: 'middle'
          },{
              field: 'phone',
              title: '手机号码',
              align: 'center',
              valign: 'middle'
          },{
              field: 'location',
              title: '所在地区',
              align: 'center',
              valign: 'middle'
          },{
              field: 'address',
              title: '收货地址',
              align: 'center',
              valign: 'middle'
          },{
              field: 'parentAg',
              title: '公会号',
              align: 'center',
              valign: 'middle',
              sortable: true
          },{
              field: 'rechargeTotal',
              title: '充值钻石数<br>(当前公会)',
              align: 'center',
              valign: 'middle',
              sortable: true,
          }, {
              field : 'roomcard',
              title : '钻石数',
              align: 'center',
              valign: 'middle',
              sortable: true,
           }, {
              field : 'gamePoint',
              title : '积分数',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'enroll_match_total',
              title: '参与赛事数',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'enroll_fee_total',
              title: '赛事报名耗钻',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'reward_roomcard_total',
              title: '钻石赛奖励',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'reward_gamepoint_total',
              title: '积分赛奖励',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'reg_date',
              title: '注册时间',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'last_login_date',
              title: '最近登录时间',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'last_logout_date',
              title: '最近登出时间',
              align: 'center',
              valign: 'middle',
              sortable: true,
          },{
              field: 'valid',
              title: '状态',
              align: 'center',
              valign: 'middle',
              sortable: true,
              formatter:is_valid
          },{
              field: 'op',
              title: '操作',
              align: 'center',
              align: 'middle',
              formatter:getOp
          }
          ]]
    });

      function status(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          var statusstr = '';
          if(rowobj['open_auth'] == '1'){
              statusstr = '<span class="label label-success">是</span>';
          }else if(rowobj['open_auth'] == '0'){
              statusstr = '<span class="label label-danger">否</span>';
          }

          return [
              statusstr
          ].join('');
      }

      function is_valid(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          var statusstr = '';
          if(rowobj['valid'] == '1'){
              statusstr = '<span class="label label-success">正常</span>';
          }else if(rowobj['valid'] == '0'){
              statusstr = '<span class="label label-danger">冻结</span>';
          }

          return [
              statusstr
          ].join('');
      }

      function getCellSortByClick(name,sort){ //用于服务端排序重写

          console.log(String.format('------getCellSortByClick name[{0}] sort[{1}]',name,sort));
          $('#dataTable').bootstrapTable('refresh',{'url':String.format('{0}&sort_name={1}&sort_method={2}','{{info["listUrl"]}}',name,sort)});
      }

      function getOp(value,row,index){
          var comfirmUrls = [
              '/admin/member/kick',
              '/admin/member/freeze/fish',
              '/admin/member/freeze/hall',
              '/admin/member/open_auth'
          ];

          var notShowOp = [
                '/admin/member/open_auth',
                '/admin/member/modify',
          ];

          eval('rowobj='+JSON.stringify(row))
          var opList = []
          for (var i = 0; i < rowobj['op'].length; ++i) {
              var op = rowobj['op'][i];
              var str = JSON.stringify({id : rowobj['id'],cur_size:"{{info['cur_size']}}",cur_page:pageNumber});
              var cStr = str.replace(/\"/g, "@");
              if(comfirmUrls.indexOf(op['url'])>=0)
                  opList.push(String.format("<a href=\"javascript:;\" class=\"btn btn-primary btn-sm btn-xs\" onclick=\"comfirmDialog(\'{0}\', \'{1}\', \'{2}\')\"><i class=\"glyphicon glyphicon-edit\"> {3} </i></a>", op['url'], op['method'], cStr, op['txt']));
              else
                  opList.push(String.format("<a href=\"{0}/{5}?id={1}&page_size={2}&cur_page={3}\" class=\"btn btn-primary btn-sm btn-xs\" ><i class=\"glyphicon glyphicon-edit\"> {4} </i></a> ", op['url'],rowobj['id'],"{{info['cur_size']}}",pageNumber,op['txt'],"{{info['remove_type']}}"));
          }
          return opList.join('');
      }

      //定义列操作
      function getSearchP(p){
        var searchId = $("#searchId").val();
        console.log(p);
        sendParameter = p;
        sendParameter['searchId'] = searchId;

        return sendParameter;
      }

      function responseFun(res){
          count= res.total;
          //实时刷
          $('.totalTitle').text(String.format("会员总人数：{0}", count));
          var totalTitle = document.getElementsByClassName('totalTitle')[0];
          totalTitle.style.cssText = "background-color:#d9edf7;height: 40px; font-size:15px; text-align:center;padding-bottom: 10px;";
          pageNumber = parseInt(res.pageNumber);
          return {"rows": res.result,
                  "total": res.total
          };
      }

      function responseError(status) {
          location.reload();
      }
</script>
%if info['a_type'] in ['0']:
<script>
    $("#searchId").select2({
        allowClear: true,
        closeOnSelect: false,
        language: "zh-CN",
        placeholder: " 请选择用户ID或手动输入用户ID",
        minimumInputLength: 0,
        multiple: false,
        ajax:{
            url: "/admin/bag/select/userid",
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
