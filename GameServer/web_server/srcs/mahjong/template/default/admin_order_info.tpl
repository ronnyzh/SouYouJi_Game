<div class="definewidth" role="form">
    <div class='header definewidth'>
        <h3>
            %if info.get('title',None):
                {{info['title']}}
            %end
        </h3>
    </div>
</div>
<form class='form-horizontal group-border-dashed definewidth m10' >
       <div class="form-group">
            <label class="col-sm-5 control-label">订单号</label>
            <div class="col-sm-6">
                  <span class='input'>{{info['orderNo']}}</span>
            </div>
       </div>  

       <div class="form-group">
            <label class="col-sm-5 control-label">充值卡数:</label>
            <div class="col-sm-6">
                    <span style='margin-top:5px'>{{info['cardNums']}}</span>
            </div>
       </div>           

       <div class="form-group">
            <label class="col-sm-5 control-label">充值代理/会员账号</label>
            <div class="col-sm-6">
                  <span style='margin-top:5px'>{{info['rechargeAccount']}}</span>
            </div>
       </div>       

       <div class="form-group">
            <label class="col-sm-5 control-label">订单状态</label>
            <div class="col-sm-6">
                  <span style='margin-top:5px'>{{info['status']}}</span>
            </div>
       </div>       

       <div class="form-group">
            <label class="col-sm-5 control-label">申请购买时间</label>
            <div class="col-sm-6">
                  <span style='margin-top:5px'>{{info['apply_date']}}</span>
            </div>
       </div>       

       <div class="form-group">
            <label class="col-sm-5 control-label">系统确认时间</label>
            <div class="col-sm-6">
                  <span style='margin-top:5px'>{{info['finish_date']}}</span>
            </div>
       </div>       

      <div class="form-group">
            <label class="col-sm-5 control-label">备注</label>
            <div class="col-sm-6">
                  <span style='margin-top:5px'>{{info['note']}}</span>
            </div>
      </div>      
      <div class="form-group">
            <label class="col-sm-5 control-label"></label>
            <div class="col-sm-6">
                   <button type="button" class="btn btn-sm btn-primary" name="backid" id="backid">返回</button>
            </div>
      </div>
</form>
<script type="text/javascript">
  $(function(){
        $('#backid').click(function(){
                window.location.href="{{info['backUrl']}}";
        });
  });
</script>
%rebase admin_frame_base