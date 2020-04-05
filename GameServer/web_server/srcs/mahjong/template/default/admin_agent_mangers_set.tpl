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
      <form class='form-horizontal group-border-dashed' action="{{info['submitUrl']}}" method='POST' id='selfModify'>
       <div class="form-group">
            <label class="col-sm-5 control-label">公会id</label>
            <div class="col-sm-6">
                  <input type='text' style='width:100%;float:left' name='agent_id' class="form-control" value="{{agent_id}}" readonly="readonly">
            </div>
       </div>

       <div class="form-group">
            <label class="col-sm-5 control-label">管理人员(uid以逗号分隔，清空则不填)</label>
            <div class="col-sm-6">
                  <input type='text' style='width:100%;float:left' name='managers' class="form-control" value="{{managers}}" >
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
        alert("修改成功！")
    }else if("{{post_res}}"=="2"){
        alert("修改失败!")
    }
</script>