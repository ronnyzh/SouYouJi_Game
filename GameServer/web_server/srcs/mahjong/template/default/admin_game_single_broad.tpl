<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
          %include admin_frame_header
          <div class="content" id="goods_create_app" style="float:left;width:100%;position:relative;top:2.1em">
             <form class='form-horizontal group-border-dashed' action="{{info['subUrl']}}" method='POST' id='broadcastForm' onSubmit='return false'>
             <input type='hidden' name='gameId' value="{{info['defaultGameId']}}" />

             <table class='table config-table'>
             <tr>
                    <td width='20%' class='table-title' style="font-size:20px">设置广播</td>
             </tr>
             <tr>
                <td>
                    <table class='table config-table'>
                        <tr>
                            <td class='table-title'>广播类型</td>
                                <td>
                                    <input type="radio" checked='checked' name="bType" value='0' id="bType" /> 游戏广播
                            </td>
                        </tr>
                        <tr>
                            <td class='table-title'>广播内容</td>
                                <td>
                                    <input style="width:100%;float:left;" class="form-control" type="text" name="content" id="content">
                            </td>
                        </tr>
                        <tr>
                            <td class='table-title'>广播重复次数</td>
                                <td>
                                    <input style="width:100%;float:left;" class="form-control" type="text" name="repeatTimes" id="repeatTimes" >
                            </td>
                        </tr>
                        <tr>
                            <td class='table-title'>广播间隔（秒）</td>
                                <td>
                                    <input style="width:100%;float:left;" class="form-control" type="text" name="repeatInterval" id="repeatInterval"  value="0">
                            </td>
                        </tr>
                    </table>
                </td>
             </tr>
             <tr>
                    <td>
                        <div style="text-align:center;padding: 10px 10px 10px;">
                            <button type="submit" class="btn btn-sm btn-primary">{{lang.BTN_SUBMIT_TXT}}</button>
                            <button type="button" class="btn btn-sm btn-primary" id="backid">返回</button>
                        </div>
                    </td>
             </tr>
          </table>
            </form>
      </div>
</div>
</div>
<script type="text/javascript">
    $('#broadcastForm').submit(function(){
          formAjax($(this).attr("action"), $(this).attr("method"), $(this).serialize(),'正在提交...');
    });
    $('#backid').click(function(){
        window.location.href="/admin/game/list";
   });
</script>
%rebase admin_frame_base
