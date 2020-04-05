<div class="cl-mcont">
    <div class='block'>
         <div class='header'>
             <h3>
             %if info.get('title',None):
               {{info['title']}}
             %end
           </h3>
         </div>

<div class='content'>
         <h4><span class="label label-default">消耗类型和获取类型请填写道具id
</span></h4>
      <form class='form-horizontal group-border-dashed' action="{{info['submitUrl']}}" method='POST' id='selfModify'>
       <div class="form-group">
            <label class="col-sm-5 control-label">套餐id</label>
            <div class="col-sm-6">
                  <input type='text' style='width:100%;float:left' name='cid' class="form-control" value='{{cid}}' readonly='readonly'>
            </div>
       </div>

       <div class="form-group">
            <label class="col-sm-5 col-xs-10 control-label">套餐名称</label>
            <div class="col-sm-6 col-xs-12">
                  <input type='text' style='width:100%;float:left' name='name'  data-rules="{required:true}" class="form-control" value='{{name}}'>
            </div>
       </div>

       <div class="form-group">
            <label class="col-sm-5 col-xs-10 control-label">消耗类型</label>
            <div class="col-sm-6 col-xs-12">
                  <input type='text' style='width:100%;float:left' name='cost_type'  data-rules="{required:true}" class="form-control" value='{{cost_type}}'>
            </div>
       </div>


       <div class="form-group">
            <label class="col-sm-5 col-xs-10 control-label">消耗数量</label>
            <div class="col-sm-6 col-xs-12">
                  <input type='text' style='width:100%;float:left' name='cost'  data-rules="{required:true}" class="form-control" value='{{cost}}'>
            </div>
       </div>

       <div class="form-group">
            <label class="col-sm-5 col-xs-10 control-label">获取类型</label>
            <div class="col-sm-6 col-xs-12">
                  <input type='text' style='width:100%;float:left' name='gain_type'  data-rules="{required:true}" class="form-control" value='{{gain_type}}'>
            </div>
       </div>

       <div class="form-group">
            <label class="col-sm-5 col-xs-10 control-label">获取数量</label>
            <div class="col-sm-6 col-xs-12">
                  <input type='text' style='width:100%;float:left' name='gain'  data-rules="{required:true}" class="form-control" value='{{gain}}'>
            </div>
       </div>

       <div class="form-group">
            <label class="col-sm-5 col-xs-10 control-label">获取类型名称</label>
            <div class="col-sm-6 col-xs-12">
                  <input type='text' style='width:100%;float:left' name='gain_title'  data-rules="{required:true}" value="{{gain_title}}" class="form-control">
            </div>
       </div>

       <div class="form-group">
            <label class="col-sm-5 col-xs-10 control-label">消耗类型名称</label>
            <div class="col-sm-6 col-xs-12">
                  <input type='text' style='width:100%;float:left' name='cost_title'  data-rules="{required:true}" value="{{cost_title}}" class="form-control">
            </div>
       </div>

       <div class="form-group">
            <label class="col-sm-5 col-xs-10 control-label">大类id</label>
            <div class="col-sm-6 col-xs-12">
                  <input type='text' style='width:100%;float:left' name='big_type_id'  data-rules="{required:true}"  class="form-control">
            </div>
       </div>

       <div class="form-group">
            <label class="col-sm-5 col-xs-10 control-label">大类名称</label>
            <div class="col-sm-6 col-xs-12">
                  <input type='text' style='width:100%;float:left' name='big_type_title'  data-rules="{required:true}"  class="form-control">
            </div>
       </div>

       <div class="modal-footer" style="text-align:center">
           <button type="submit" class="btn btn-sm btn-xs btn-primary btn-mobile">修改</button>
       </div>


</form>
</div>
</div>
</div>
%rebase admin_frame_base

<script>
    if("{{post_res}}"=="1"){
        alert("创建成功！")
    }else if("{{post_res}}"=="2"){
        alert("创建失败！")
    }else if("{{post_res}}"=="3"){
        alert("创建失败!套餐id已存在！")
    }
</script>