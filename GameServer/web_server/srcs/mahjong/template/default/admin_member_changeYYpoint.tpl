<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class='block'>
    %include admin_frame_header
    <div class='content' id="recharge_app">
        <form class='form-horizontal group-border-dashed' @submit="onSubmit" action="{{info['submitUrl']}}"
              method='POST' id='removeCard' onSubmit='return false'>
            <input type='hidden' name='agentId' value="{{info['agentId']}}"/>
            <input type='hidden' name='memberId' value="{{info['memberId']}}"/>
            <table class='table config-table'>
                <tr>
                    <td width='20%' class='table-title' style="background-color:#d9edf7;font-size:20px">增减积分</td>
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
                                    <input type='text' value="{{info['name']}}" readonly=''
                                           style='width:100%;float:left' name='name' data-rules="{required:true}"
                                           class="form-control">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>会员公会</td>
                                <td>
                                    <input type='text' value="{{info['agentId']}}" readonly=''
                                           style='width:100%;float:left' name='agentId' data-rules="{required:true}"
                                           class="form-control">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>当前会员积分数</td>
                                <td>
                                    <input type='text' value="{{info['yyPoint']}}" readonly=''
                                           style='width:100%;float:left' name='yyPoint' data-rules="{required:true}"
                                           class="form-control">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>增减类型<br></td>
                                <td>
                                    <table class='table config-table' border='1'>
                                        <tr>
                                            <td>
                                                <label class="well col-sm-6" style="">
                                                    <input type="radio" name="changeType" value="add" checked='checked'> <span style="color:#428bca">增加</span>
                                                </label>
                                                <label class="well col-sm-6">
                                                    <input type="radio" name="changeType" value="remove"> <span style="color:#d9534f">移除</span>
                                                </label>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>增减积分数</td>
                                <td>
                                    <input type='text' style='width:100%;float:left' name='changePoint'
                                           data-rules="{required:true}" class="form-control">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>备注信息</td>
                                <td>
                                    <input type='text' style='width:100%;float:left' name='note'
                                           data-rules="{required:true}" class="form-control">
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div style="text-align:center;padding: 10px 10px 10px;">
                            <button type="submit" class="btn btn-sm btn-primary btn-mobile">确定</button>
                            <button type="button" class="btn btn-sm btn-primary btn-mobile" name="backid"
                                    @click="onBack">返回
                            </button>
                        </div>
                    </td>
                </tr>
            </table>
        </form>
    </div>
</div>
<script type="text/javascript">
    $(function () {
        var recharge_app = new Vue({
            el: '#recharge_app',
            data: {
                'page': ''
            }, mounted: function () {
                this.$data.page = "{{page}}";
            }, methods: {
                onSubmit: function (e) {
                    e.preventDefault();
                    formAjax($('#removeCard').attr("action"), $('#removeCard').attr("method"), $('#removeCard').serialize(), '正在移除...');
                },
                onBack: function (e) {
                    e.preventDefault();
                    window.location.href = "{{info['backUrl']}}";
                }
            }
        });
    });
</script>

%rebase admin_frame_base
