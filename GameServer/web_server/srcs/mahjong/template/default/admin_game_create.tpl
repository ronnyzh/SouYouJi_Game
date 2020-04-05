<style type="text/css">.config-table td.table-title{text-align:center;font-size:13px;vertical-align:middle}</style>
<div class='block'>
          %include admin_frame_header
          <div class="content" id="game_create_app">
             <form class="form-horizontal group-border-dashed" id='gameForm' @submit="onSubmit" action="{{info['submitUrl']}}" method="post" style="border-radius: 0px;" enctype="multipart/form-data">
               <table class='table config-table'>
                        <tr>
                          <td width='20%' class='table-title'>游戏创建</td>
                        </tr>
                        <tr>
                              <td class='table-title'>`</td>
                              <td>
                                <table class='table config-table' border='1'>
                                    <tr>
                                         <td class='table-title'>游戏ID</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="id" name="id" class="form-control">
                                             <label for='id' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>游戏名称</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="name" name="name" class="form-control">
                                             <label for='name' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>游戏版本号</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="version" name="version" class="form-control">
                                             <label for='version' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>排序值<br/>
                                                <small>用于客户端排序,降序排序，值越小越靠前</small>
                                         </td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="game_sort" name="game_sort" class="form-control">
                                             <label for='game_sort' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>其他信息</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="other_info" name="other_info" class="form-control">
                                             <label for='other_info' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                </table>
                              </td>
                        </tr>
                        <tr>
                              <td class='table-title'>
                                      更新下载配置<br/>
                                      <small>用于接口提示更新,非专业人员勿动此配置</small>
                              </td>
                              <td>
                                <table class='table config-table' border='1'>
                                    <tr>
                                         <td class='table-title'>
                                                   更新包路径<br/>
                                                  <small>更新的小游戏包路径,入http://xxxx/xxx.zip</small>
                                         </td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="pack_name" name="pack_name" class="form-control">
                                         </td>
                                    </tr>
                                </table>
                              </td>
                        </tr>
                        <tr>
                              <td class='table-title'>
                                    游戏房间选项
                                    <span><a href="javascript:;" @click="onAdd" class='btn btn-small btn-xs btn-primary'>新增</a></span>
                              </td>
                              <td>
                                <table class='table config-table table1' border='1'>
                                    %include game_setting
                                </table>
                              </td>
                        </tr>
                        <tr>
                            <td class='table-title'>
                                  游戏配置
                            </td>
                            <td>
                                <table class='table config-table' border='1'>
                                   <tr>
                                         <td class='table-title'>
                                                选项配置<br/>
                                                <small>或操作选项</small>
                                         </td>
                                         <td>
                                              <input type="text" style='width:100%;float:left' id="dependSettingStr" name="dependSettingStr" class="form-control">
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>
                                                选项配置<br/>
                                                <small>且操作选项</small>
                                         </td>
                                         <td>
                                              <input type="text" style='width:100%;float:left' id="dependAndSettingStr" name="dependAndSettingStr" class="form-control">
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>
                                                钻石配置<br/>
                                                <small>格式如下:描述1:钻石1:局数1,描述2:钻石2:局数2</small>
                                         </td>
                                         <td>
                                                <input type="text" style='width:100%;float:left' id="cardSetting" name="cardSetting" class="form-control">
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>
                                                娱乐模式人数设置<br/>
                                                <small>必须大于1小于等于{{info['partyPlayerMax']}}</small>
                                         </td>
                                         <td>
                                                <input type="text" style='width:100%;margin-right:10px;float:left' id="partyPlayerCount" name="partyPlayerCount" class="form-control">
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>
                                                游戏最大房间数<br/>
                                                <small>每个游戏最大可开房间数</small>
                                         </td>
                                         <td>
                                                <input type="text" style='width:100%;margin-right:10px;float:left' id="maxRoomCount" name="maxRoomCount" class="form-control">
                                         </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
              </table>
              <div class="modal-footer" style="text-align:center">
                   <button type="submit" class="btn btn-primary">{{lang.BTN_SUBMIT_TXT}}</button>
                  <button type="button" class="btn btn-primary" @click="onBack">{{lang.BTN_BACK_TXT}}</button>
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

                   onBack : function(e){
                       e.preventDefault();
                       window.location.href="{{info['backUrl']}}";
                   },

                   onAdd : function(e){
                       e.preventDefault();
                       var configTable = $('.table1');
                       var num = parseInt(configTable.find('tr').length);
                       if (num == 8){
                            //信息框
                            layer.open({
                              content   : '只允许创建8条规则'
                              ,btn      : '关闭'
                            });
                       }else{
                            str = '<tr num="'+(num+1)+'"><td>选项类型<br><small>游戏房间标题是否可选</small><br>\
                                     <input type="radio" name="radio'+(num+1)+'" value="1">单选<input type="radio" name="radio'+(num+1)+'" value="0">多选</td><td>选项标题<br/><small>选项标题</small><br/><input type="text" name="title'+(num+1)+'" class="form-control" style="width:100%;float:left" /></td><td>可选项<br/><small>文字加逗号隔开,例如3局,4局</small><br/><input type="text" name="content'+(num+1)+'" class="form-control" style="width:100%;float:left" /></td><td>依赖项<br/><small>类型|1:选项1,选项2;类型|选项1,选项2,;</small><br/><input type="text" name="depend'+(num+1)+'" class="form-control" style="width:100%;float:left" /></td><td>最多显示/条<br/><small>客户端最多显示的选择条数</small><br/><input type="text" name="number'+(num+1)+'" class="form-control" style="width:250px;float:left" /></td>\
                                    </tr>';

                            //添加到子节点
                            configTable.append(str);
                       }
                   }
               }
        });
    })
</script>
%rebase admin_frame_base
