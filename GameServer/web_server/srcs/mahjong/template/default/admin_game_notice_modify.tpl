<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="cl-mcont">
    <div class="block">
        %include admin_frame_header
        <div class="content" id="goods_create_app" style="float:left;width:100%;position:relative;top:2.6em">
            <form class='form-horizontal group-border-dashed' action="{{info['submitUrl']}}" method='POST'
                  id='noticeForm' onSubmit='return false'>
                <input type="hidden" name="noticeId" value="{{info['noticeId']}}"/>
                <table class='table config-table'>
                    <tr>
                        <td width='20%' class='table-title' style="font-size:20px;background-color:#d9edf7;">修改公告</td>
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
                                               class="form-control" placeholder="必填" value="{{noticInfo['title']}}">
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title'>有效天数<br>
                                        <small style="color:#d95454">（该天数后自动删除）</small>
                                    </td>
                                    <td>
                                        %if noticInfo['validDate'] == '0':
                                        <label class="well col-sm-4">
                                            <input type="radio" name="validDate" value='0' checked='checked'
                                               style='line-height:50px;'/> 永久 &nbsp;&nbsp;&nbsp;
                                        </label>
                                        <label class="well col-sm-4">
                                            <input type="radio" name="validDate" value='7' style='line-height:50px;'/> 一周 &nbsp;&nbsp;&nbsp;
                                        </label>
                                        <label class="well col-sm-4">
                                            <input type="radio" name="validDate" value='30' style='line-height:50px;'/> 一月 &nbsp;&nbsp;&nbsp;
                                        </label>
                                        %elif noticInfo['validDate'] == '30':
                                        <label class="well col-sm-4">
                                            <input type="radio" name="validDate" value='0' style='line-height:50px;'/> 永久 &nbsp;&nbsp;&nbsp;
                                        </label>
                                        <label class="well col-sm-4">
                                            <input type="radio" name="validDate" value='7' checked='checked'
                                               style='line-height:50px;'/> 一周 &nbsp;&nbsp;&nbsp;
                                        </label>
                                        <label class="well col-sm-4">
                                            <input type="radio" name="validDate" value='30' style='line-height:50px;'/> 一月 &nbsp;&nbsp;&nbsp;
                                        </label>
                                        %else:
                                        <label class="well col-sm-4">
                                            <input type="radio" name="validDate" value='0' style='line-height:50px;'/> 永久 &nbsp;&nbsp;&nbsp;
                                        </label>
                                        <label class="well col-sm-4">
                                            <input type="radio" name="validDate" value='7' style='line-height:50px;'/> 一周 &nbsp;&nbsp;&nbsp;
                                        </label>
                                        <label class="well col-sm-4">
                                            <input type="radio" name="validDate" value='30' checked='checked'
                                               style='line-height:50px;'/> 一月 &nbsp;&nbsp;&nbsp;
                                        </label>
                                        %end
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title'>消息类型<br>
                                        <small style="color:#d95454">（公告类型）</small>
                                    </td>
                                    <td>
                                        <input type="text" style='width:100%;float:left;color:#428bca'
                                               value=" {{MSGTYPE2DESC[noticInfo['messageType']]}}" id="messageType"
                                               name="messageType" class="form-control" readonly>
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title'>消息内容<br>
                                        <small style="color:#d95454">（推送给用户）</small>
                                    </td>
                                    <td>
                                        <textarea
                                                style="width:{{MAIL_SETTING_INFO['mailTextWidth']}};height:{{MAIL_SETTING_INFO['mailTextHeight']}};float:left"
                                                name='content'
                                                class="form-control xheditor">{{!noticInfo['content']}}</textarea>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div style="text-align:center;padding: 10px 10px 10px;">
                                <button type="submit" class="btn btn-sm btn-primary">{{lang.BTN_SUBMIT_TXT}}</button>
                                <button type="button" class="btn btn-sm btn-primary" name="backid" id="backid">
                                    {{lang.BTN_BACK_TXT}}
                                </button>
                            </div>
                        </td>
                    </tr>
                </table>
            </form>
        </div>
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