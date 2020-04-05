<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/fileInput/js/fileinput.min.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/fileInput/js/locales/zh.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/fileInput/ds_file_upload.js"></script>
<style type="text/css">
    .config-table td.table-title{text-align:center;font-size:13px;width:20%;vertical-align:middle}
</style>
<div class="block">
          %include admin_frame_header
          <div class="content">
             <form class="form-horizontal group-border-dashed" id='gameForm' onSubmit="return false;" action="{{info['submitUrl']}}" method="post" style="border-radius: 0px;" enctype="multipart/form-data">
               <input type="hidden" value="{{info['token']}}" id='token' />
               <table class='table config-table'>
                        <tr>
                          <td width='20%' class='table-title'>{{lang.GOODS_CREATE_TXT}}</td>
                        </tr>
                        <tr>
                              <td class='table-title'>
                                      奖品兑换设置<br/>
                                      <small>捕鱼礼品兑换编辑</small>
                              </td>
                              <td>
                                <table class='table config-table' border='1'>
                                    <tr>
                                         <td class='table-title'>奖品名称</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="reward_name" name="reward_name" class="form-control">
                                             <label for='reward_name' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>奖品类型</td>
                                         <td>
                                             <input type="radio"  id="reward_type" name="reward_type" checked="checked" value="0" /> 手机
                                             <input type="radio"  id="reward_type" name="reward_type" value="1" /> 话费
                                             <input type="radio"  id="reward_type" name="reward_type" value="2" /> 家用电器
                                             <input type="radio"  id="reward_type" name="reward_type" value="3" /> 生活用品
                                             <input type="radio"  id="reward_type" name="reward_type" value="4" /> 电子产品
                                             <label for='reward_type' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>卡密<br/>
                                                <small>仅奖品类型为卡密生效,卡密将以短信形式发送给玩家</small>
                                         </td>
                                         <td>
                                              卡号:<input type="text"  id="reward_card_no" name="reward_card_no" class="form-control" />
                                              密码:<input type="text"  id="reward_card_pwd" name="reward_card_pwd" class="form-control" />
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>奖品金币<br/>
                                                <small>仅奖品类型为金币生效,金币将直接进入用户金币数</small>
                                         </td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="reward_coin" name="reward_coin" class="form-control">
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>奖品总期数</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="reward_nums" name="reward_nums" class="form-control">
                                             <label for='reward_nums' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>当前期数</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="reward_now_nums" name="reward_now_nums" class="form-control">
                                             <label for='reward_now_nums' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>奖品位置</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="reward_pos" name="reward_pos" class="form-control">
                                             <label for='reward_pos' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>奖品成本</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="reward_cost" name="reward_cost" class="form-control">
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>奖品略缩图</td>
                                         <td>
                                             <input type="file" name="files" id="txt_file" multiple class="file-loading" />
                                             <input type="hidden" name="img_path" id="img_path" value=""/>
                                         </td>
                                    </tr>
                                     <tr>
                                         <td class='table-title'>
                                                 每期奖品库存<br/>
                                                 <small>用于每期库存刷新,如果不自动续期则会同步减少库存</small>
                                         </td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="reward_stock" name="reward_stock" class="form-control">
                                             <label for='reward_stock' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                     <tr>
                                         <td class='table-title'>每期剩余库存</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="reward_per_stock" name="reward_per_stock" class="form-control">
                                             <label for='reward_per_stock' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>所需兑换券</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="reward_need_ticket" name="reward_need_ticket" class="form-control">
                                             <label for='reward_need_ticket' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
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
    //0.初始化fileinput
    var oFileInput = new FileInput();
    oFileInput.Init("txt_file", "{{info['upload_url']}}");
</script>
%rebase admin_frame_base
