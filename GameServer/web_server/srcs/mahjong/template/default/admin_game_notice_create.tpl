<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
    %include admin_frame_header
    <div class="content" id="goods_create_app" style="float:left;width:100%;position:relative;top:2.6em">
        <form class='form-horizontal group-border-dashed' action="{{info['submitUrl']}}" method='POST' id='noticeForm'
              onSubmit='return false'>
            <input type="hidden" name='action' value="{{info['action']}}"/>
            <table class='table config-table'>
                <tr>
                    <td width='20%' class='table-title' style="font-size:20px;background-color:#d9edf7;">创建新公告</td>
                </tr>
                <tr>
                    <td>
                        <table class='table config-table' border='1'>
                            <tr>
                                <td class='table-title' style="width:200px">消息标题<br>
                                    <small style="color:#d95454">（消息/邮件标题）</small>
                                </td>
                                <td>
                                    <input type="text" style='width:100%;float:left' id="title" name="title"
                                           class="form-control" placeholder="必填">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>有效天数<br>
                                    <small style="color:#d95454">（该天数后自动删除）</small>
                                </td>
                                <td>
                                    <label class="well col-sm-4">
                                        <input type="radio" name="validDate" value='0' style='line-height:50px;'/> 永久 &nbsp;&nbsp;&nbsp;
                                    </label>
                                    <label class="well col-sm-4">
                                        <input type="radio" name="validDate" value='7' style='line-height:50px;'/> 一周 &nbsp;&nbsp;&nbsp;
                                    </label>
                                    <label class="well col-sm-4">
                                        <input type="radio" name="validDate" value='30' style='line-height:50px;'/> 一月 &nbsp;&nbsp;&nbsp;
                                    </label>
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>消息类型<br>
                                    <small style="color:#d95454">（公告类型）</small>
                                </td>
                                <td>
                                    <select id='type' name='messageType' class='form-control'
                                            style="width:{{MAIL_SETTING_INFO['mailTextWidth']}};height:40px;color:#428bca">
                                        %if selfUid == '1':
                                        <option value='0'>{{lang.MSG_TYPE_ONE}}</option>
                                        <option value='1'>{{lang.MSG_TYPE_TWO}}</option>
                                        <option value='2'>{{lang.MSG_TYPE_THREE}}</option>
                                        %else:
                                        <option value='1'>{{lang.MSG_TYPE_TWO}}</option>
                                        <option value='2'>{{lang.MSG_TYPE_THREE}}</option>
                                        %end
                                    </select>
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>消息内容<br>
                                    <small style="color:#d95454">（推送给用户）</small>
                                </td>
                                <td>
                                    <textarea
                                            style="width:{{MAIL_SETTING_INFO['mailTextWidth']}};height:{{MAIL_SETTING_INFO['mailTextHeight']}};float:left"
                                            name='content' class="form-control xheditor" placeholder="必填"></textarea>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div style="text-align:center;padding: 10px 10px 10px;">
                            <button type="submit" class="btn btn-primary btn-sm"><i class="glyphicon">
                                {{lang.BTN_SUBMIT_TXT}} </i></button>
                            <button type="button" class="btn btn-primary btn-sm" id="backid"><i class="glyphicon">
                                {{lang.BTN_BACK_TXT}} </i></button>
                        </div>
                    </td>
                </tr>
            </table>
        </form>
    </div>
</div>

<script type="text/javascript">
    $('#backid').click(function () {
        window.location.href = "{{info['backUrl']}}";
    });

    $('#noticeForm').submit(function () {
        formAjax($(this).attr("action"), $(this).attr("method"), $(this).serialize(), '正在创建...');
    });
</script>
%rebase admin_frame_base
