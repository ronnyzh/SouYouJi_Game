<style type="text/css">.config-table td.table-title{text-align:center;font-size:13px;vertical-align:middle}</style>
<div class='block'>
          %include admin_frame_header
          <div class="content" id='fish_room_app'>
             <form class="form-horizontal group-border-dashed" id='gameForm' v-on:submit="onSubmit" action="{{info['submitUrl']}}" method="post" style="border-radius: 0px;" enctype="multipart/form-data">
               <table class='table config-table'>
                        <tr>
                          <td width='20%' class='table-title'>房间修改</td>
                        </tr>
                        <tr>
                              <td class='table-title'>`</td>
                              <td>
                                <table class='table config-table' border='1'>
                                    <tr>
                                         <td class='table-title'>房间ID</td>
                                         <td>
                                             <input type="text" v-bind:value="roomInfo.room_id" readonly="" style='width:100%;float:left' id="room_id" name="room_id" class="form-control">
                                             <label for='id' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>房间名称</td>
                                         <td>
                                             <input type="text" v-bind:value="roomInfo.room_name" style='width:100%;float:left' id="room_name" name="room_name" class="form-control">
                                             <label for='room_name' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                </table>
                              </td>
                        </tr>
                        <tr>
                              <td class='table-title'>
                                   房间基本配置<br/>
                                      <small>房间参数的基本配置</small>
                              </td>
                              <td>
                                <table class='table config-table table1' border='1'>
                                    %include fish_room_setting
                                </table>
                              </td>
                        </tr>
                        <tr>
                              <td class='table-title'>
                                   奖票生成配置<br/>
                              </td>
                              <td>
                                <table class='table config-table table1' border='1'>
                                    %include fish_room_reward_setting
                                </table>
                              </td>
                        </tr>
                        <tr>
                            <td class='table-title'>游玩配置</td>
                            <td>
                                <table class='table config-table' border='1'>
                                    %include fish_room_bet_set
                                </table>
                            </td>
                        </tr>
              </table>
              <div class="modal-footer" style="text-align:center">
                   <button type="submit" class="btn btn-primary">{{lang.BTN_SUBMIT_TXT}}</button>
                  <button type="button" class="btn btn-primary" v-on:click="onBack">{{lang.BTN_BACK_TXT}}</button>
              </div>
            </form>
    </div>
</div>
<script type="text/javascript">
    function initPage(result){
        var fish_room_app = new Vue({
                el : '#fish_room_app',
                data : {
                    roomInfo : "",
                    room_id   : ""

                },mounted:function(){
                    var self = this;
                    self.$data.roomInfo = result.room_info;

                },methods:{

                    onSubmit:function(e){
                         e.preventDefault();
                         formAjax($('#gameForm').attr("action"), $('#gameForm').attr("method"), $('#gameForm').serialize(),'正在修改...');
                    },

                    onBack : function(e){  //返回方法
                         e.preventDefault();
                        window.location.href="{{info['backUrl']}}";
                    }

                },delimiters : ['${','}']
        });

    }

    $(function(){  //获取房间数据接口
        var api = String.format('/admin/fish/room/info/{0}',"{{room_id}}");
        $.getJSON(api,function(result){
            if(result)
                initPage(result);
        });
    });

</script>
%rebase admin_frame_base
