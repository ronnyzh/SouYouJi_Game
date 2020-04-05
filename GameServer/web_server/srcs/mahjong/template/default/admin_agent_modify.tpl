<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/agent_create.js"></script>
<style type="text/css">
    .config-table td.table-title{text-align:center;width:20%;font-size:13px;vertical-align:middle}
</style>
<div class="cl-mcont">
  <div class="block">
          %include admin_frame_header
          <div class='content'>
                <form class='form-horizontal group-border-dashed' action="{{info['submitUrl']}}" method='POST' id='agentCreate' onSubmit='return false'>
                      <table class='table config-table'>
                              <td class='table-title'>基本信息</td>
                              <td>
                                 <table class='table config-table'>
                                  <tr>
                                      <td class='table-title min_base_txt'>代理账号:</td>
                                      <td>
                                          <div class="col-sm-12 col-xs-12">
                                            <input type='hidden' name='agentId' value="{{info['agentId']}}" />
                                            <input type='text' style='width:100%;float:left'  value="{{info['account']}}" name='account' class="form-control" >
                                          </div>
                                      </td>
                                  </tr>

                                  <tr>
                                      <td class='table-title min_base_txt'>代理名称:</td>
                                      <td>
                                          <div class="col-sm-12 col-xs-12">
                                            <input type='text' style='width:100%;float:left'  value="{{info['name']}}" name='name' class="form-control" >
                                          </div>
                                      </td>
                                  </tr>

                                 %if  info['aType'] == '0' :
                                 <tr>
                                      <td class='table-title min_base_txt'>钻石单价:</td>
                                      <td>
                                          <div class="col-sm-12 col-xs-12">
                                          <input type='text'  value="{{info['unitPrice']}}"  style='width:100%;float:left' name='unitPrice' data-rules="{required:true}"  class="form-control">
                                          </div>
                                      </td>
                                 </tr>
                                 %end

                                 %if  info['aType'] in ['1','2']:
                                 <tr>
                                      <td class='table-title min_base_txt'>自己的占额(元):</td>
                                      <td>
                                        <div class="col-sm-12 col-xs-12">
                                              <input type='text' value="{{info['shareRate']}}" readonly='' style='width:100%;float:left' name='myRate' data-rules="{required:true}"  class="form-control">
                                        </div>
                                      </td>
                                 </tr>
                                 %end

                                 %if info['aType'] in ['0','1','2']:
                                 <tr>
                                     <td class='table-title min_base_txt'>当前代理占额(元):</td>
                                      <td>
                                          <div class="col-sm-12 col-xs-12">
                                            <input type='text'  value= "{{info['rate']}}" style='width:100%;float:left' name='shareRate' data-rules="{required:true}"  class="form-control">
                                          </div>
                                      </td>
                                 </tr>
                                 %end

                                %if info['aType'] == '0':
                                <tr>
                                    <td class='table-title min_base_txt'>给新用户默认钻石数(个):</td>
                                    <td>
                                       <div class="col-sm-12 col-xs-12">
                                        <input type='text' value= "{{info['defaultRoomCard']}}" style='width:100%;float:left' name='defaultRoomCard' data-rules="{required:true}"  class="form-control">
                                        </div>
                                    </td>
                               </div>
                               %end

                               <tr>
                                  <td  class='table-title min_base_txt'>
                                            勾选游戏:<br/>
                                            <input type="button" value="全选" class="btn btn-sm btn-xs btn-success" id="selectAll">
                                            <input type="button" value="反选" class="btn btn-sm btn-xs btn-success" id="reverser">
                                            <input type="button" value="全不选" class="btn btn-sm btn-xs btn-success" id="unSelect">
                                   </td>
                                    <td>
                                        %for game in info['games']:
                                           <label class="checkbox-inline" id='list'>
                                           %if game['id'] in info['ownGames']:
                                               <input type="checkbox" checked="checked" value="{{game['id']}}" name="game{{game['id']}}" class="icheck"> {{game['name']}}
                                          %else:
                                               <input type="checkbox" value="{{game['id']}}" name="game{{game['id']}}" class="icheck"> {{game['name']}}
                                          %end
                                           </label>
                                        %end
                                    </td>
                                </tr>

                               </table>
                            </td>
                  </table>
                 <table class='table config-table'>
                   <td class='table-title'  >权限选择</td>
                   <td>
                      <table class='table config-table'>
                            %for access in Access:
                            <tr>
                                <td  class='table-title min_base_txt'>{{access['belong']}}</td>
                                <td>
                                       %for sub in access['sub']:
                                           %if sub.url in banAccess:
                                              <label class="checkbox-inline">
                                              <input type="checkbox" value="{{sub.url}}" name="url{{sub.url}}" class="icheck"> {{sub.getTxt(lang)}}
                                              </label>
                                            %else:
                                              <label class="checkbox-inline">
                                              <input type="checkbox" checked="checked" value="{{sub.url}}" name="url{{sub.url}}" class="icheck"> {{sub.getTxt(lang)}}
                                              </label>
                                            %end
                                       %end
                                </td>
                             </tr>
                             %end
                       </table>
                     </td>
                 </table>

                 <div class="modal-footer" style="text-align:center">
                     <button type="submit" class="btn btn-primary btn-mobile">修改</button>
                     <button type="button" class="btn btn-primary btn-mobile" name="backid" id="backid">返回</button>
                 </div>
      </form>
</div>
<script type="text/javascript">
    $('#backid').click(function(){
        window.location.href="{{info['backUrl']}}";
   });

</script>
%rebase admin_frame_base
