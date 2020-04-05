<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
    %include admin_frame_header
    <div class='content'>
        <form class='form-horizontal group-border-dashed' action="{{info['submitUrl']}}" method='POST' id='agentCreate'
              onSubmit='return false'>
            <input type='hidden' name='memberId' value="{{info['memberId']}}"/>
            <table class='table config-table'>
                <tr>
                    <td width='20%' class='table-title' style="background-color:#d9edf7;font-size:20px">信息修改</td>
                </tr>
                <tr>
                    <td>
                        <table class='table config-table' border='1'>
                            <tr>
                                <td class='table-title'>会员头像</td>
                                <td>
                                    <img style="border-radius:30px;" src="{{info['headImgUrl']}}" widht='34'
                                         height='34'/>
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>会员编号</td>
                                <td>
                                    <input type='text' value="{{info['memberId']}}" readonly=''
                                           style='width:100%;float:left' name='memberId' data-rules="{required:true}"
                                           class="form-control">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>会员昵称</td>
                                <td>
                                    <input type='text' value="{{info['nickname']}}" readonly=''
                                           style='width:100%;float:left' name='nickname' data-rules="{required:true}"
                                           class="form-control">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>会员公会</td>
                                <td>
                                    <input type='text' value="{{info['agentId']}}" readonly=''
                                           style='width:100%;float:left'
                                           name='agentId' data-rules="{required:true}" class="form-control">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>maxScore<br>
                                    <small style="color:#d95454">设置玩家可以设置的最大分</small>
                                </td>
                                <td>
                                    <input type='text' readonly="" value="{{info['maxScore']}}"
                                           style='width:100%;float:left' name='maxScore' class="form-control">
                                </td>
                            </tr>
                            <!--
                            <tr>
                                <td class='table-title'>玩家可以选的分</td>
                                <td>
                                    <input type="checkbox" name="score1" style='width:15px;height:15px;'
                                           checked="checked"
                                           onclick="return false" value="1"/>1 &nbsp;
                                    %for score in baseScore:
                                    %if str(score['score']) == '1':
                                    %continue
                                    %end
                                    %if str(score['score']) in info['baseScore']:
                                    <input type="checkbox" name="{{score['name']}}" style='width:15px;height:15px;'
                                           checked="checked" value="{{score['score']}}"/> {{score['score']}} &nbsp;
                                    %else:
                                    <input type="checkbox" name="{{score['name']}}" style='width:15px;height:15px;'
                                           value="{{score['score']}}"/> {{score['score']}} &nbsp;
                                    %end
                                    %end
                                </td>
                            </tr>
                            -->
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div style="text-align:center;padding: 10px 10px 10px;">
                            <button type="submit" class="btn  btn-sm btn-primary btn-mobile">修改</button>
                            <button type="button" class="btn  btn-sm btn-primary btn-mobile" name="backid"
                                    id="backid">返回
                            </button>
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
    $(function () {
        $('#agentCreate').bootstrapValidator({
            message: '无效值',
            fields: {/*验证：规则*/},
        }).on('success.form.bv', function (e) {//点击提交之后
            e.preventDefault();

            var $form = $(e.target);

            var bv = $form.data('bootstrapValidator');

            var logTxt = '正在创建...';
            formAjax($(this).attr("action"), $(this).attr("method"), $(this).serialize(), logTxt);
        });
    });
</script>
%rebase admin_frame_base