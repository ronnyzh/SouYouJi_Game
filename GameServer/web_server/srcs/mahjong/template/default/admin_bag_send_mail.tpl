<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<link href="{{info['STATIC_ADMIN_PATH']}}/css/select2.min.css" rel="stylesheet" />
<script src="{{info['STATIC_ADMIN_PATH']}}/js/select2.min.js"></script>
<div class='block'>
    %include admin_frame_header
    <div class='content'>
        <form class='form-horizontal group-border-dashed' action="{{ info['submitUrl'] }}" method='POST' id='createConfig'
              onSubmit='return false'>
            <table class='table config-table'>
                <tr>
                    <td width='20%' class='table-title' style="font-size:20px;background-color:#d9edf7">发送邮件</td>
                </tr>
                <tr>
                    <td>
                        <table class="table config-table" border="1">
                            <tr>
                                <td class='table-title'>邮件标题<br>
                                </td>
                                <td>
                                    <input type="text" class="form-control" placeholder="邮件标题" name="title">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>收件人类型<br>
                                </td>
                                <td>
                                    <label class="well col-sm-6">
                                        <input type="radio" class="recipientType" name="recipientType" id="recipientType" value='0' style='line-height:50px;' checked="checked"/> 单用户/多用户 &nbsp;&nbsp;&nbsp;
                                    </label>
                                    <label class="well col-sm-6">
                                        <input type="radio" class="recipientType" name="recipientType" id="recipientType" value='1' style='line-height:50px;'/> 全部用户 &nbsp;&nbsp;&nbsp;
                                    </label>
                                </td>
                            </tr>
                            <tr class="selectDiv">
                                <td class='table-title'>收件人ID<br>
                                </td>
                                <td>
                                    <select class="form-control"  id="id_select2_demo1" multiple="multiple" >
                                    </select>
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>邮件内容<br>
                                </td>
                                <td>
                                    <input type="text" class="form-control" placeholder="邮件内容" name="body">
                                </td>
                            </tr>
                            <tr>
                                <td class="table-title">邮件附件<br>（附件为空时， 数量可为空）
                                </td>
                                <td>
                                    <select class="form-control chets_win_resultType1" name="enclosure">
                                        <option value="" selected></option>
                                        %for itemId, itemType in items.items():
                                        <option value="{{ itemId }}">{{ itemType }}</option>
                                        %end
                                    </select>
                                    <input type="text" style="margin-top:5px" class="form-control" placeholder="附件数量" name="enclosure_num">
                                </td>
                            </tr>
                        </table>
                    </td>
                <tr>
            </table>
            <div class="modal-footer" style="text-align:center">
                <button type="submit" class="btn btn-sm btn-primary btn-mobile">确认发送</button>
            </div>
        </form>
    </div>
</div>
</div>
<script type="text/javascript">
    $('.recipientType').click(function () {
        var choosVal = $(this).val();
        if (['0', '2'].indexOf(choosVal) >= 0) {
            $('#id_select2_demo1').removeAttr('disabled');
        } else {
            $('#id_select2_demo1').attr({'disabled': 'disabled'});
        }
    });
    $('#createConfig').submit(function(){
        var data = ($(this).serialize());
        var uid = $("#id_select2_demo1").val();
        var serialize = String.format('{0}&uid={1}', data, uid);
        formAjax($(this).attr("action"), $(this).attr("method"), serialize, '正在保存...');
    });
</script>
<script>
    $("#id_select2_demo1").select2({
        allowClear: true,
        closeOnSelect: false,
        language: "zh-CN",
        placeholder: " 请选择一个或多个用户ID 或 手动输入用户ID",
        ajax:{
            url: "/admin/bag/select/userid",
            dataType:"json",
            delay:250,
            data:function(params){
                return {
                    name: params.term,
                    page: params.page || 1,
                };
            },
            cache: true,
            processResults: function (res, params) {
                var users = res["data"]["users"];
                var options = [];
                for(var i= 0, len=users.length;i<len;i++){
                    var option = {"id":users[i]["id"], "text":users[i]["name"]};
                    options.push(option);
                }
                return {
                    results: options,
                    pagination: {
                        more:res["data"]["more"]
                    }
                };
            },
            escapeMarkup: function (markup) { return markup; },
            minimumInputLength: 1
        }
    });
</script>
%rebase admin_frame_base