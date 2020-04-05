    <style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
    <div class='block'>
         %include admin_frame_header
         <div class='content'>
              <form class='form-horizontal group-border-dashed' action="{{info['submitUrl']}}" method='POST' id='J_Form' onSubmit='return false'>
              <table class="table config-table">
                <tr>
                    <td width='20%' class='table-title' style="font-size:20px">{{info['title']}}</td>
                </tr>
                <tr>
                    <td>
                        <table class='table config-table'>
                            <tr>
                                <td class='table-title'>{{lang.CARD_SALER_TXT}}</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' id="parentAccount" name="parentAg" value="{{info['parentAccount']}}" readonly='' class="form-control">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>{{lang.CARD_PACK_CHOOSE_TXT}}</td>
                                <td>
                                    <input type='text' name='cardNums' style='width:100%;float:left' data-rules="{required:true}" class='form-control' />
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>{{lang.CARD_REMARK_TXT}}</td>
                                <td>
                                    <textarea name='note' style='width:100%;height:100px;resize:none' class='form-control'></textarea>
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>{{lang.INPUT_LABEL_PASSWD_TXT}}</td>
                                <td>
                                    <input type='password' name='passwd' style='width:100%;float:left' data-rules="{required:true}" class='form-control' />
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div style="text-align:center;padding: 10px 10px 10px;">
                            <button type="submit" class="btn btn-sm btn-primary">{{lang.CARD_APPLY_RECHARGE_TXT}}</button>
                            <button type="button" class="btn btn-sm btn-primary" name="backid" id="backid">{{lang.BTN_BACK_TXT}}</button>
                        </div>
                    </td>
                </tr>
              </table>
              </form>
         </div>
    </div>
<script type="text/javascript">
    $('#J_Form').submit(function(){
          formAjax($(this).attr("action"), $(this).attr("method"), $(this).serialize(),'正在提交订单...');
    });

    $('#backid').click(function(){
        window.location.href="{{info['backUrl']}}";
   });
</script>
%rebase admin_frame_base