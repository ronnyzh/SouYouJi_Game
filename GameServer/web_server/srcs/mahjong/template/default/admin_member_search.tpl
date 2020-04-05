<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
          %include admin_frame_header
          <div class="content" id="member_search_app" style="float:left;width:100%;position:relative;top:2.6em">
          <form class='form-horizontal group-border-dashed' action="{{info['searchUrl']}}" method='POST' id='searchForm'
              onSubmit='return false'>
              <table class="table config-table">
                <tr>
                    <td width='20%' class='table-title' style="font-size:20px">{{info['title']}}</td>
                </tr>
                <tr>
                    <td>
                        <table class='table config-table'>
                            <tr>
                                <td class='table-title'>玩家编号</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' id="memberId" name="memberId"
                                           class="form-control" placeholder="请输入玩家编号">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>钻石数</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' id="cardNums" name="cardNums"
                                           class="form-control" placeholder="请输入玩家编号">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>代理密码</td>
                                <td>
                                    <input type="password" style='width:100%;float:left' id="passwd" name="passwd"
                                           class="form-control" placeholder="请输入自身密码">
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div style="text-align:center;padding: 10px 10px 10px;">
                            <button type="submit" id="btnRechange" class="btn btn-sm btn-primary "><i class="glyphicon">充值</i></button>
                        </div>
                    </td>
                </tr>
              </table>
          </form>
          </div>
  </div>
<script>
    $('#searchForm').submit(function () {
        document.getElementById("btnRechange").setAttribute("disabled", true); //设置不可点击
        formAjax($(this).attr("action"), $(this).attr("method"), $(this).serialize(), '正在提交...');
    });
</script>
%rebase admin_frame_base