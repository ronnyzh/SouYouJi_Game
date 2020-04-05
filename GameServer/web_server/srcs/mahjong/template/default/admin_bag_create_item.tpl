<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class='block'>
    %include admin_frame_header
    <div class='content'>
        <form class='form-horizontal group-border-dashed' action="{{ info['submitUrl'] }}" method='POST' id='createConfig'
              onSubmit='return false'>
            <table class='table config-table'>
                <tr>
                    <td width='20%' class='table-title' style="font-size:20px">创建道具</td>
                </tr>
                <tr>
                    <td>
                        <table class="table config-table" border="1">
                            <tr>
                                <td class='table-title'>道具ID<br>
                                </td>
                                <td>
                                    <input type="text" class="form-control" placeholder="填写道具ID" name="item_id">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>道具名称<br>
                                </td>
                                <td>
                                    <input type="text" class="form-control" placeholder="填写道具名称" name="title">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>道具描述<br>
                                </td>
                                <td>
                                    <input type="text" class="form-control" placeholder="填写道具描述" name="des">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>道具价格<br>
                                </td>
                                <td>
                                    <input type="text" class="form-control" placeholder="填写道具价格" name="price">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>道具有效次数<br>
                                </td>
                                <td>
                                    <input type="text" class="form-control" placeholder="填写道具有效次数" name="times">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>道具有效天数<br>
                                </td>
                                <td>
                                    <input type="text" class="form-control" placeholder="填写道具有效天数" name="days">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>道具单位（元）<br>
                                </td>
                                <td>
                                    <input type="text" class="form-control" placeholder="填写道具单位（元）" name="unit">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>是否可兑换<br>
                                </td>
                                <td>
                                    <input type="text" class="form-control" placeholder="是否可兑换" name="can_reward">
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
            <div class="modal-footer" style="text-align:center">
                <button type="submit" class="btn btn-sm btn-primary btn-mobile">创建</button>
                <button type="button" class="btn btn-sm btn-primary" name="backid" id="backid">返回</button>
            </div>
        </form>
    </div>
</div>
</div>
<script>
    $('#backid').click(function(){
        window.location.href="/admin/bag/list";
    });

    $('#createConfig').submit(function(){
          formAjax($(this).attr("action"), $(this).attr("method"), $(this).serialize(),'正在保存...');
    });
</script>
%rebase admin_frame_base


