<div class="block">
             %include admin_frame_header
             <div class="content" id="recharge_app">
                  <div class='user-avator' style='text-align:center;margin-top:30px;'>
                      <img style="border-radius:30px;" src="{{info['headImgUrl']}}" widht='80' height='80' />
                  </div>
                  <form class='form-horizontal group-border-dashed definewidth m10' @submit="onSubmit" action="{{info['submitUrl']}}" method='POST' id='J_Form' onSubmit='return false'>
                         <input type="hidden" value="{{info['submit_token']}}" name="token" />
                         <div class="form-group">
                              <label class="col-sm-5 control-label">会员编号</label>
                              <div class="col-sm-6">
                                      <input type='text' style='width:100%;float:left;' class="form-control"  id='memberId' name='memberId' value="{{info['memberId']}}" readonly="" />
                              </div>
                         </div>
                         <div class="form-group">
                              <label class="col-sm-5 control-label">微信名称:</label>
                              <div class="col-sm-6">
                                      <input type='text' style='width:100%;float:left;' class="form-control"  name='account' value="{{info['name']}}" readonly="" />
                              </div>
                         </div>
                         <div class="form-group">
                              <label class="col-sm-5 control-label" v-if="page=='HALL'">剩余钻石:</label>
                              <label class="col-sm-5 control-label" v-if="page=='FISH'">剩余金币:</label>
                              <div class="col-sm-6">
                                      <input type='text' style='width:100%;float:left;' class="form-control"  name='roomCard' value="{{info['roomCard']}}" readonly="" />
                              </div>
                         </div>
                         <div class="form-group">
                              <label class="col-sm-5 control-label">选择充值套餐:</label>
                              <div class="col-sm-6">
                                    <select name='cardNums' id='cardNums' class="form-control" style='width:100%;height:35px;'>
                                        %for type in info['rechargeTypes']:
                                          <option value="{{type['roomCard']}}">{{type['txt']}}</option>
                                        %end
                                    </select>
                              </div>
                         </div>

                         <div class="form-group">
                              <label class="col-sm-5 control-label">密码:</label>
                              <div class="col-sm-6">
                                    <input type='password' style='width:100%;float:left;' class="form-control" name='passwd' data-rules="{required:true}">
                              </div>
                         </div>

                         <div class="modal-footer" style="text-align:center">
                             <button type="submit" class="btn btn-sm btn-primary">确认充值</button>
                             <button type="button" class="btn btn-sm btn-primary" name="backid" @click="onBack">返回</button>
                         </div>
                  </form>
              </div>
</div>
<script type="text/javascript">
    $(function(){
        var recharge_app = new Vue({
                el : '#recharge_app',
                data:{
                    page : ''
                },mounted:function(){
                    this.$data.page = "{{action}}";
                },methods:{
                    onSubmit:function(e){
                        e.preventDefault();
                        formAjax($('#J_Form').attr("action"),$('#J_Form').attr("method"),$('#J_Form').serialize(),'正在充值...');
                    },
                    onBack:function(e){
                        e.preventDefault();
                        window.location.href="{{info['backUrl']}}";
                    }
                }
        });
    });
</script>
%rebase admin_frame_base
