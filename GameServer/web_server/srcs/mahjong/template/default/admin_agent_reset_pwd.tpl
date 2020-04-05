<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="cl-mcont">
    <div class='block'>
        %include admin_frame_header
        <div class='content'>
            <form class='form-horizontal group-border-dashed' action="{{info['submitUrl']}}" method='POST'
                  id='selfModify'>
                  <table class='table config-table'>
                <tr>
                    <td width='20%' class='table-title' style="background-color:#d9edf7;font-size:20px">重置代理密码</td>
                </tr>
                <tr>
                    <td>
                        <table class='table config-table' border='1'>
                            <tr>
                                <td class='table-title'>需要重置的代理ID</td>
                                <td>
                                    <input type='text' style='width:100%;float:left' name='agent_id' id="agent"
                                            class="form-control">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>需要重置的密码</td>
                                <td>
                                    <input type='password' style='width:100%;float:left' name='passwd' id="passwd"
                                            class="form-control" placeholder="重置密码为空，则默认重置为：123456">
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div style="text-align:center;padding: 10px 10px 10px;">
                            <button type="button" id="sub" class="btn btn-sm btn-xs btn-primary btn-mobile">确定重置</button>
                        </div>
                    </td>
                </tr>
            </table>
            </form>
        </div>
    </div>
</div>
%rebase admin_frame_base

<script>
    $("#sub").click(function () {
        var str = JSON.stringify({agent_id : $('#agent').val(), passwd : $('#passwd').val()});
        var cStr = str.replace(/\"/g, "@");
        layer.open({
          title: [
             '搜集游棋牌后台提醒你',
             'background-color:#204077; color:#fff;'
          ]
          ,anim: 'up'
          ,content: '您真的确定要重置吗'
          ,btn: ['确认', '取消']
          ,style: 'top:25%;'
          ,yes:function(index){
            normalAjaxStrData("{{info['submitUrl']}}", "POST", cStr, '正在关闭服务器');
            layer.close(index);
          }
      });
    });

</script>