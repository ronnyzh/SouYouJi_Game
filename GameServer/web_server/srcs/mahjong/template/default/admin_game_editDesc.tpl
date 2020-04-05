<div class="block">
          <div class="header">                          
            <h3>
                %if info.get('title',None):
                    {{info['title']}}
                %end
            </h3>
          </div>
          <div class="content">
             <form class="form-horizontal group-border-dashed" id='introForm' onSubmit="return false;" action="{{info['submitUrl']}}" method="post" style="border-radius: 0px;">
              <input type="hidden" name="gameId" value="{{info['gameId']}}" />
              <div class="form-group">
                <label class="col-sm-3 control-label">
                    {{lang.GAME_INTRO_TITLE}}<br/>
                    <small>{{lang.GAME_INTRO_TXT}}</small>
                </label>
                <div class="col-sm-8">
                    <textarea style="width:{{GAME_SETTING_INFO['ruleTextWidth']}};height:{{GAME_SETTING_INFO['ruleTextHeight']}};float:left"  name='content' class="form-control xheditor" id="some-textarea">{{info['gameDesc']}}</textarea>
                </div>
              </div>
              <div class="modal-footer" style="text-align:center">
                   <button type="submit" class="btn btn-primary">{{lang.BTN_CREATE_TXT}}</button>
                   <button type="button" class="btn btn-primary" id='backid'>{{lang.BTN_BACK_TXT}}</button>
              </div>
            </form>
          </div>
</div>
<script type="text/javascript">
  $(function(){

       $('#introForm').submit(function(){
            formAjax($(this).attr("action"), $(this).attr("method"), $(this).serialize(),'正在生成规则模板...');
       });

       $('#backid').click(function(){
              window.location.href="{{info['backUrl']}}";
       });

  });
</script>
%rebase admin_frame_base