<style type="text/css">.config-table td.table-title{text-align:center;font-size:13px;vertical-align:middle}</style>
<div class='block'>
          %include admin_frame_header
          <div class="content" id="game_create_app">
             <form class="form-horizontal group-border-dashed" id='gameForm' @submit="onSubmit" action="{{info['submitUrl']}}" method="post" style="border-radius: 0px;" enctype="multipart/form-data">
              <table class='table config-table'>
                    <tr>
                        <td width='20%' class='table-title' style="font-size:20px; background-color:#d9edf7">椰云积分兑换</td>
                    </tr>
                    <tr>
                        <td>
                            <table class='table config-table' border='1'>
                                <tr>
                                    <td class='table-title'>兑换比例</td>
                                    <td>
                                        <input type='text' style='width:100%;float:left' name='proportion' id="proportion"
                                                class="form-control">
                                    </td>
                                </tr>
                                <tr>
                                    <td class='table-title' style="width:200px">兑换积分数<br><br>
                                        <span><a href="javascript:;" @click="onAdd" class='btn btn-small btn-xs btn-primary'>增加</a></span>
                                        <span><a href="javascript:;" @click="onDel" class='btn btn-small btn-xs btn-danger'>删除</a></span>
                                    </td>
                                    <td id="rewardList">
                                        <table class="table config-table table1 table-bordered table-hover" style="margin-top:5px">
                                            <tr>
                                                <td style="display:none;" class="table-title">ID</td>
                                                <td style="display:none;">
                                                    <input  type="text" name="match_reward_rank1" style="width:120px;float:left" class="form-control" value="1" readonly>
                                                </td>
                                                <td class="table-title">椰云积分</td>
                                                <td>
                                                    <input type="text" name='match_reward_fee1' style="width:120px;float:left" class="form-control">
                                                </td>
                                                <td class="table-title">游戏积分</td>
                                                <td>
                                                    <input type="text" name='match_reward_fee1' style="width:120px;float:left" class="form-control">
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>

                            </table>
                        </td>
                    </tr>
              </table>
              <div class="modal-footer" style="text-align:center">
                   <button type="submit" class="btn btn-sm btn-primary">{{lang.BTN_SUBMIT_TXT}}</button>
              </div>
            </form>
    </div>
</div>
<script type="text/javascript">
    $(function(){   //前端页面配置及渲染
        var game_create_app = new Vue({
               el : '#game_create_app',
               data:{

               },mounted:function(){

               },methods:{
                   onSubmit : function(e){
                       e.preventDefault();
                       formAjax($('#gameForm').attr("action"), $('#gameForm').attr("method"), $('#gameForm').serialize(),'正在创建...');
                   },

                   onAdd : function(e){
                       e.preventDefault();
                       var configTable = $('.table1');
                       var num = parseInt(configTable.find('tr').length);
                       if (num == 8){
                            //信息框
                            layer.open({
                              content   : '只允许创建8个名次'
                              ,btn      : '关闭'
                            });
                       }else{
                            str = '<tr num="'+(num+1)+'">\
                                    <td style="display:none;" class="table-title">ID</td>\
                                    <td style="display:none;"><input type="text" name="match_reward_rank'+(num+1)+'" style="width:120px;float:left" class="form-control" value="'+(num+1)+'" readonly>\
                                    <td class="table-title">椰云积分</td>\
                                    <td><input type="text" name="match_reward_fee'+(num+1)+'" style="width:120px;float:left" class="form-control" value="0"></td>\
                                    <td class="table-title">游戏积分</td>\
                                    <td><input type="text" name="match_reward_fee'+(num+1)+'" style="width:120px;float:left" class="form-control" value="0"></td>\
                                  </tr>';

                            //添加到子节点
                            configTable.append(str);
                       }
                   },

                   onDel : function(e){
                       e.preventDefault();
                       var configTable = $('.table1');
                       var num = parseInt(configTable.find('tr').length);
                       if (num == 0){
                            //信息框
                            layer.open({
                              content   : 'DONE DELETE'
                              ,btn      : '关闭'
                            });
                       }else{
                            $('.table1 tr:last').remove();
                       }
                   },
               }
        });
    })
</script>
%rebase admin_frame_base
