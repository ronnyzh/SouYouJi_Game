<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/refreshDateInit.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/common.js"></script>
  <div class="block">
          %include admin_frame_header
          <div class="content">
          <div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
          <div class='col-sm-12' style='margin-left:1em;'>
                   
                    <form class='form-horizontal group-border-dashed' action="{{info['submitUrl']}}" method='POST' id='selfModify1'>
                     <div class="form-group">
                          <span name='game_id' style='display:none' value = "{{info['gameId']}}" > </span>
                          <span name='robot_level' style="display:none" value = "C" > </span>
                          <label class="col-sm-5 col-xs-10 control-label">触发C档机器人概率</label>
                          <div class="col-sm-6 col-xs-12">
                                <input type='text' style='width:30%;float:left' name='switch_per' value="{{info['switch_per']}}" data-rules="{required:true}" class="form-control">
                                <button type="submit" class="btn btn-sm btn-xs btn-primary btn-mobile">确认</button>
                          </div>
                     </div>

                    </form>

          </div>
          </div>

          <table id="dataTable" class="table table-bordered table-hover"></table>
          </div>
  </div>


<script type="text/javascript">
  function initTable() {
    $('#dataTable').bootstrapTable({
          method: 'get',
          url: '{{info["listUrl"]}}',
          contentType: "application/json",
          datatype: "json",
          cache: false,
          //checkboxHeader: true,
          striped: true,
          pagination: true,
          pageSize: 15,
          showExport: true,
          //exportTypes:['excel', 'csv', 'pdf', 'json'],
          pageList: [15,50,100,'All'],
          //search: true,
          clickToSelect: true,
          //sidePagination : "server",
          sortOrder: 'desc',
          sortName: 'date',
          //queryParams:getSearchP,
          responseHandler:responseFun,
          showFooter:true, //添加页脚做统计
          //onLoadError:responseError,
          showExport:true,
          //exportTypes:['excel', 'csv', 'pdf', 'json'],

          columns: [
          [{
              field: 'tile_type',
              title: '',
              align: 'center',
              valign: 'middle',
              formatter: getTileType
          },{
              field: 'tile_type_per',
              title: '',
              align: 'center',
              valign: 'middle',
              sortable: true,
              formatter: getTileTypePer
          },{
              field: 'modify',
              title: '',
              align: 'center',
              valign: 'middle',
              formatter:getModify
          },{
              field: 'delete',
              title: '',
              align: 'center',
              valign: 'middle',
              formatter:getDelete
          }]]
    });

// formTag = "<form class='form-group' action='{{info['modifyUrl']}}&tile_type="+rowobj['tile_type']+"&game_id={{info['gameId']}}&robot_level={{info['robotLevel']}}' method='POST' id='selfModify"+rowobj['tile_type']+"'>"
       function getTileType(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          var tagTip = '<span style="display: none" id="form-row-'+index+'"></span>';
          spanTip = "<div style='width:10%;float:left' >牌型：</div>";
          var oldData = "<input type='text' class='hide' name='old_tile_type' value="+rowobj['tile_type']+" />";
          tileTypeInp = "<input style='width:25%;float:left' type='text' name='new_tile_type' value="+rowobj['tile_type']+" data-rules='{required:true}' class='form-control' onchange='this.setAttribute(\"value\",this.value)'>";
          res = tagTip+spanTip+oldData+tileTypeInp;
          return [res].join('');
       }

      function getTileTypePer(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          spanTip = "<div style='width:10%;float:left' >概率：</div>";
          spanOldTileTypePer = "<span style='display:none' class='label' name='old_tile_type_per'>"+rowobj['tile_type_per']+"</span>";
          var oldData = "<input type='text' class='hide' name='old_tile_type_per' value="+rowobj['tile_type_per']+" />";
          tileTypePerInp = "<input style='width:25%;float:left' type='text' name='new_tile_type_per' value="+rowobj['tile_type_per']+"  data-rules='{required:true}' class='form-control' onchange='this.setAttribute(\"value\",this.value)'>";
          res = spanTip+spanOldTileTypePer+oldData+tileTypePerInp
          return [res].join('');
       }
      function getModify(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          confirmBtn = "<button type='button' class='btn btn-sm btn-xs btn-primary btn-mobile' onclick='doModify("+index+")'>修改</button>";
          formTag = "";
          res = confirmBtn + formTag
          return [res].join('');
      }

      function getDelete(value,row,index){
          eval('var rowobj='+JSON.stringify(row))
          //linkTag = "<a class='btn btn-primary' href='"+ {{info['deleteUrl']}}+"&tile_type="+rowobj['tile_type']+"&game_id="+{{info['gameId']}}+"&robot_level="+{{info['robotLevel']}}+"'></a>";
          linkTag = "<a class='btn btn-primary' href='{{info['deleteUrl']}}&tile_type="+rowobj['tile_type']+"&game_id={{info['gameId']}}&robot_level={{info['robotLevel']}}'>删除</a>";
          return [linkTag].join('');
      }

          //获得返回的json 数据
        function responseFun(res){

            data = res.data
            return data;
        }

        //
       doModify = function(row){
            var td = $("#form-row-"+row);
            var tr = td.parents('tr').get().shift();
            var form = document.createElement('form');
            form.innerHTML = tr.innerHTML;
            var data = $(form).serialize();
            console.log(data);
            $.ajax({
                method:'POST',
                url: "{{info['modifyUrl']}}&"+data,
                success: function () {
                    console.log('修改成功');
                    window.location.reload();
                }
            })
      }
      
}
</script>
%rebase admin_frame_base

<div class='content'>
      <form class='group-border-dashed' action="{{info['addUrl']}}?test=1&op=add&game_id={{info['gameId']}}&robot_level={{info['robotLevel']}}" method='POST' id='selfModify2'>
<!--      <span name='game_id' style="display:none" value = "{{info['gameId']}}" > </span>
      <span name='robot_level' style="display:none" value = "C" > </span>-->
       <div class="form-group">
            <div style='width:5%;float:left'>牌型：</div>
            <!--<div class="col-sm-6 col-xs-12">-->
                  <!--<label class="col-sm-5 col-xs-10 control-label">牌型：</label>-->
          <input type='text' style='width:20%;float:left' name='tile_type' value="" data-rules="{required:true}" class="form-control">
          <div style='width:5%;float:left'>概率：</div>
          <input type='text' style='width:20%;float:left' name='tile_type_per' value="" data-rules="{required:true}" class="form-control">
            <!--</div>-->
       <!--</div>-->
       <!--<div class="form-group">-->
            
            <!--<div class="col-sm-6 col-xs-12">-->
            <!--      <input type='text' style='width:25%;float:left' name='tile_type_per' value="" data-rules="{required:true}" class="form-control">-->
            <!--</div>-->
       </div>
       <div style="text-align:center;width:25%;float:left">
           <button type="submit" class="btn btn-sm btn-xs btn-primary btn-mobile">新增</button>
       </div>
      </form>
</div>

