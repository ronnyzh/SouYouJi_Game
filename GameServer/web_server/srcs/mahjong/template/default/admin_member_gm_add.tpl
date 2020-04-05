<div class="cl-mcont">
<div class="block">
          <div class="header">
            <h3>
                %if info.get('title',None):
                    {{info['title']}}
                %end
            </h3>
          </div>
          <form class="form-horizontal group-border-dashed"  style='padding: 19px 29px 29px;' action="{{info['addUrl']}}" method="POST" id='addGM' onSubmit='return false'>
            <div class='row'>
                <div class='col-sm-12'>
                    <p align='center'>
                      <span style='font-size:22px;font-weight:600;'>{{info['title']}}</span>
                    </p>
                </div>
                <div class='col-sm-12'>
                    <p align='center'><input type='text' name='memberId' style='width:200px;height:35px;' placeholder="请输入玩家编号"  />&nbsp;</p>
                </div>
                <div class='col-sm-12'>
                     <p align='center'><input type='submit' style='width:200px;height:35px;' value='确定' class='btn btn-sm btn-primary' /></p>
                </div>
                %if message:
                <p align='center'>
                      <span style='color:red'>{{message}}</span>
                </p>
                %end
            </div>
          </form>
  </div>
</div>
<script type="text/javascript">
    $('#addGM').submit(function(){
          var _this = $(this);
          var logTxt   = '正在处理...';
          formAjax(_this.attr("action"),_this.attr("method"),_this.serialize(),logTxt);
    });

</script>
%rebase admin_frame_base