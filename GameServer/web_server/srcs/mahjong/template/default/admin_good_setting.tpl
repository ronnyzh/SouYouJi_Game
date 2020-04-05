<style type="text/css">
    .config-table td{text-align:center;font-size:13px;vertical-align:middle}
    .config-table td .input{border:none;text-align:center;}
</style>
<div class="block">
          %include admin_frame_header
          <div class="content">
            <form class="form-horizontal" id='createConfig' onSubmit="return false;" action="{{info['createUrl']}}" method="POST" style="border-radius: 0px;">
                <table class='table config-table'>
                    <tr>
                      <td align='center'>配置名称</td>
                      <td align='center'>配置值</td>
                      <td align='center'>配置说明</td>
                      <td align='center'>操作</td>
                    </tr>
                    <tr>
                      <td align='center'>
                          <input type='text' name='config_name' id='config_name' value="钻石单价" style='width:250px;height:30px;' class='input' readonly="" /></td>
                      <td align='center'>
                          <input type='text' name='goodsPrice' id='goodsPrice' value="{{goodsPrice}}" style='width:250px;height:30px;' class='input'/></td>
                      <td align='center'>
                          <input type='text' name='config_note' id='config_note' value="商城钻石当家配置" style='width:250px;height:30px;' class='input'/></td>
                      <td align='center'>
                           <button type="submit" class="btn btn-primary">保存更改</button>
                      </td>
                    </tr>
                </table>
              </form>
          </div>
</div>
<script type="text/javascript">
    $('#createConfig').submit(function(){
          formAjax($(this).attr("action"), $(this).attr("method"), $(this).serialize(),'正在保存...');
    });

    $('#backid').click(function(){
        window.location.href="{{info['backUrl']}}";
   });
</script>
%rebase admin_frame_base
