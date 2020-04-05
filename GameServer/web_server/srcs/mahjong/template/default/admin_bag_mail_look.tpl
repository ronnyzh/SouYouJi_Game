<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="cl-mcont">
    <div class='block'>
        <div class='content'>
            <form class='form-horizontal group-border-dashed' action="" method='GET'>
                <table class='table config-table'>
                    <tr>
                        <td width='20%' class='table-title' style="background-color:#d9edf7;font-size:20px">邮件查看</td>
                    </tr>
                    %if not mailInfo:
                    <tr>
                        <td>
                            <table class='table config-table' border='1'>
                                <tr>
                                    <td class='table-title'>该邮件已被删除</td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    %else:
                    <tr>
                        <td>
                            <table class='table config-table' border='1'>
                                <tr>
                                    <td class='table-title'>邮件标题</td>
                                    <td>
                                        <input type='text' style='width:100%;float:left' name='title' id="title"
                                               class="form-control" value="{{ mailInfo.get('title') }}" readonly="" >
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title'>发件人</td>
                                    <td>
                                        <input type='text' style='width:100%;float:left' name='sender' id="sender"
                                               class="form-control" value="系统" readonly="" >
                                    </td>
                                </tr>
                                 <tr>
                                    <td class='table-title'>收件人ID</td>
                                    <td>
                                        <input type='text' style='width:100%;float:left' name='userId' id="userId"
                                               class="form-control" value="{{ mailInfo.get('userId') }}" readonly="" >
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title'>收件人账号</td>
                                    <td>
                                        <input type='text' style='width:100%;float:left' name='account' id="account"
                                               class="form-control" value="{{ mailInfo.get('account') }}" readonly="" >
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title'>收件人昵称</td>
                                    <td>
                                        <input type='text' style='width:100%;float:left' name='nickname' id="nickname"
                                               class="form-control" value="{{ mailInfo.get('nickname') }}" readonly="" >
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title'>发件时间</td>
                                    <td>
                                        <input type='text' style='width:100%;float:left' name='send_time' id="send_time"
                                               class="form-control" value="{{ mailInfo.get('send_time') }}" readonly="" >
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title'>邮件内容</td>
                                    <td>
                                        <input type='text' style='width:100%;float:left' name='body' id="body"
                                               class="form-control" value="{{ mailInfo.get('body') }}" readonly="" >
                                    </td>
                                </tr>
                                %if mailInfo.get('awards'):
                                <tr>
                                    <td class='table-title'>邮件附件</td>
                                    <td>
                                        <input type='text' style='width:100%;float:left' name='awards' id="awards"
                                               class="form-control" value="{{ mailInfo.get('awards') }}" readonly="" >
                                    </td>
                                </tr>
                                %end
                                <tr>
                                    <td class='table-title'>是否已读</td>
                                    <td>
                                        %if mailInfo.get('read') == '1':
                                        <span class="label label-primary">是</span>
                                        %else:
                                        <span class="label label-danger">否</span>
                                        %end
                                    </td>
                                </tr>
                                %if mailInfo.get('read') == '1':
                                <tr>
                                    <td class='table-title'>已读时间</td>
                                    <td>
                                         <input type='text' style='width:100%;float:left' name='read_time' id="read_time"
                                               class="form-control" value="{{ mailInfo.get('read_time') }}" readonly="" >
                                    </td>
                                </tr>
                                %end
                                %if mailInfo.get('awards'):
                                <tr>
                                    <td class='table-title'>附件是否领取</td>
                                    <td>
                                        %if mailInfo.get('is_get') == '1':
                                        <span class="label label-primary">是</span>
                                        %else:
                                        <span class="label label-danger">否</span>
                                        %end
                                    </td>
                                </tr>
                                %end
                                %if mailInfo.get('award_time') == '1':
                                <tr>
                                    <td class='table-title'>附件领取时间</td>
                                    <td>
                                         <input type='text' style='width:100%;float:left' name='award_time' id="award_time"
                                               class="form-control" value="{{ mailInfo.get('award_time') }}" readonly="" >
                                    </td>
                                </tr>
                                %end
                            </table>
                            <div class="modal-footer" style="text-align:center">
                              <button type="button" class="btn btn-primary btn-sm" name="backid" id="backid">返回</button>
                          </div>
                        </td>
                    </tr>
                    %end
                </table>
            </form>
        </div>
    </div>
</div>
<script>
    $('#backid').click(function(){
        window.location.href="{{info['backUrl']}}";
   });
</script>
%rebase admin_frame_base
