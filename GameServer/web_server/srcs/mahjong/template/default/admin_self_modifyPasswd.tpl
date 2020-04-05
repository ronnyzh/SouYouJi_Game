<!--
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/agent_create.js"></script>
-->
<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
    %include admin_frame_header
    <div class="content" id="goods_create_app" style="float:left;width:100%;position:relative;top:2.6em">
        <form class='form-horizontal group-border-dashed' action="{{ info['submitUrl'] }}" method='POST' id='modifyPasswdForm' onSubmit='return false'>
            <table class='table config-table'>
                <tr>
                    <td width='20%' class='table-title' style="background-color:#d9edf7;font-size:20px">修改密码</td>
                </tr>
                <tr>
                    <td>
                    <table class="table config-table">
                        <tr>
                            <td class="table-title">{{lang.INPUT_LABEL_OLD_PASSWD_TXT}}</td>
                            <td>
                                <input type="password" style='width:100%;float:left' id="passwd" name="passwd"
                                       class="form-control" placeholder="旧密码">
                            </td>
                        </tr>
                        <tr>
                            <td class="table-title">{{lang.INPUT_LABEL_PASSWD1_TXT}}</td>
                            <td>
                                <input type="password" style='width:100%;float:left' id="comfirmPasswd"
                                       name="comfirmPasswd"
                                       class="form-control" placeholder="新密码">
                            </td>
                        </tr>
                        <tr>
                            <td class="table-title">{{lang.INPUT_LABEL_PASSWD2_TXT}}</td>
                            <td>
                                <input type="password" style='width:100%;float:left' id="comfirmPasswd1"
                                       name="comfirmPasswd1"
                                       class="form-control" placeholder="确认密码">
                            </td>
                        </tr>
                    </table>
                    </td>
                </tr>
                </tr>
            </table>
            <div style="text-align:center;padding: 10px 10px 10px;">
                <button type="submit" class="btn btn-sm btn-primary "><i class="glyphicon">修改</i></button>
            </div>
        </form>
    </div>
</div>
<script type="text/javascript">
    $('#modifyPasswdForm').submit(function () {
        formAjax($(this).attr("action"), $(this).attr("method"), $(this).serialize(), '正在提交...');
    });
</script>
%rebase admin_frame_base