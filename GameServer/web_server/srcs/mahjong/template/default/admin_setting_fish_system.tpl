<style type="text/css">
    .config-table td{text-align:center;font-size:13px;vertical-align:middle}
    .config-table td .input{border:none;text-align:center;}
</style>
<div class="block">
          %include admin_frame_header
          <div class="content">
            <form class="form-horizontal" id='createConfig' onSubmit="return false;" action="" method="POST" style="border-radius: 0px;">
                <table class='table config-table'>
                    <tr>
                      <td align='center'>配置名称</td>
                      <td align='center'>配置值</td>
                      <td align='center'>配置说明</td>
                    </tr>
                    %for setting in fish_setting:
                      <tr>
                        <td align='center'>{{setting['title']}}</td>
                        <td align='center'>
                            <input type='text' name='{{setting["name"]}}' id='config_name' value="{{setting['value']}}" style='width:100%;height:30px;' class='input'/>
                        </td>
                        <td>{{setting['desc']}}</td>
                      </tr>
                     %end
                     <tr>
                      <td colspan="3" align='center'><button type="submit" class="btn btn-primary">保存更改</button></td>
                     </tr>
                </table>
              </form>
          </div>
</div>
<script type="text/javascript">
    $('#createConfig').submit(function(){
          formAjax($(this).attr("action"), $(this).attr("method"), $(this).serialize(),'正在保存...');
    });
</script>
%rebase admin_frame_base
