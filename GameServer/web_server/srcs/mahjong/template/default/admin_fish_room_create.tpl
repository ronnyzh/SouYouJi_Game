<style type="text/css">
    .config-table td.table-title{text-align:center;font-size:13px;vertical-align:middle}
</style>
<div class="cl-mcont">
    <div class='block'>
          %include admin_frame_header
          <div class="content">
             <form class="form-horizontal group-border-dashed" id='gameForm' onSubmit="return false;" action="{{info['submitUrl']}}" method="post" style="border-radius: 0px;" enctype="multipart/form-data">
               <table class='table config-table'>
                        <tr>
                          <td width='20%' class='table-title'>房间创建</td>
                        </tr>
                        <tr>
                              <td class='table-title'>`</td>
                              <td>
                                <table class='table config-table' border='1'>
                                    <tr>
                                         <td class='table-title'>房间ID</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="room_id" name="room_id" class="form-control">
                                             <label for='id' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>房间名称</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="room_name" name="room_name" class="form-control">
                                             <label for='room_name' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                </table>
                              </td>
                        </tr>
                        <tr>
                              <td class='table-title'>
                                   房间基本配置<br/>
                                      <small>房间参数的基本配置</small>
                              </td>
                              <td>
                                <table class='table config-table table1' border='1'>
                                    %include fish_room_setting
                                </table>
                              </td>
                        </tr>
                        <tr>
                              <td class='table-title'>
                                   奖票生成配置<br/>
                              </td>
                              <td>
                                <table class='table config-table table1' border='1'>
                                    %include fish_room_reward_setting
                                </table>
                              </td>
                        </tr>
                        <tr>
                            <td class='table-title'>游玩配置</td>
                            <td>
                                <table class='table config-table' border='1'>
                                    %include fish_room_bet_set
                                </table>
                            </td>
                        </tr>
              </table>
              <div class="modal-footer" style="text-align:center">
                   <button type="submit" class="btn btn-primary">{{lang.BTN_SUBMIT_TXT}}</button>
                  <button type="button" class="btn btn-primary" id='backid'>{{lang.BTN_BACK_TXT}}</button>
              </div>
            </form>
    </div>
  </div>
</div>
<script type="text/javascript">

    $('#gameForm').submit(function(){
          formAjax($(this).attr("action"), $(this).attr("method"), $(this).serialize(),'正在创建...');
    });

    $('#backid').click(function(){
        window.location.href="{{info['backUrl']}}";
   });
</script>
%rebase admin_frame_base
