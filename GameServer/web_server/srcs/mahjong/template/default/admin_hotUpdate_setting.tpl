<style type="text/css">
    .config-table td{text-align:center;font-size:13px;vertical-align:middle}
    .config-table td .input{border:none;text-align:center;}
</style>
<div class="block">
          %include admin_frame_header
          <div class="content" id="hot_app">
            <form class="form-horizontal" id='createConfig' v-on:submit="onSubmit" action="{{info['submitUrl']}}" method="POST" style="border-radius: 0px;">
                <table class='table config-table'>
                    <tr>
                      <td align='center'>更新配置名称</td>
                      <td align='center'>更新配置值</td>
                    </tr>
                    <tr>
                      <td align='center'>packName</td>
                      <td align='center'>
                          <input type='text' name='packName' id='packName' v-bind:value="settingInfo.packName" style='width:100%;height:30px;' class='input'/>
                      </td>
                    </tr>

                    <tr>
                      <td align='center'>resVersion</td>
                      <td align='center'>
                          <input type='text' name='resVersion' id='resVersion' v-bind:value="settingInfo.resVersion" style='width:100%;height:30px;' class='input'/>
                      </td>
                    </tr>

                    <tr>
                      <td align='center'>minVersion</td>
                      <td align='center'>
                          <input type='text' name='minVersion' id='minVersion' v-bind:value="settingInfo.minVersion" style='width:100%;height:30px;' class='input'/>
                      </td>
                    </tr>

                    <tr>
                      <td align='center'>iosMinVersion</td>
                      <td align='center'>
                          <input type='text' name='iosMinVersion' id='iosMinVersion' v-bind:value="settingInfo.iosMinVersion" style='width:100%;height:30px;' class='input'/>
                      </td>
                    </tr>

                    <tr>
                      <td align='center'>downloadURL</td>
                      <td align='center'>
                          <input type='text' name='downloadURL' id='downloadURL' v-bind:value="settingInfo.downloadURL" style='width:100%;height:30px;' class='input'/>
                      </td>
                    </tr>

                    <tr>
                      <td align='center'>IPAURL</td>
                      <td align='center'>
                          <input type='text' name='IPAURL' id='IPAURL' v-bind:value="settingInfo.IPAURL" style='width:100%;height:30px;' class='input'/>
                      </td>
                    </tr>

                    <tr>
                      <td align='center'>apkSize</td>
                      <td align='center'>
                          <input type='text' name='apkSize' id='apkSize' v-bind:value="settingInfo.apkSize" style='width:100%;height:30px;' class='input'/>
                      </td>
                    </tr>

                    <tr>
                      <td align='center'>apkMD5</td>
                      <td align='center'>
                          <input type='text' name='apkMD5' id='apkMD5' v-bind:value="settingInfo.apkMD5" style='width:100%;height:30px;' class='input'/>
                      </td>
                    </tr>

                    <tr>
                      <td align='center'>hotUpdateURL</td>
                      <td align='center'>
                          <input type='text' name='hotUpdateURL' id='hotUpdateURL' v-bind:value="settingInfo.hotUpdateURL" style='width:100%;height:30px;' class='input'/>
                      </td>
                    </tr>

                    <tr>
                      <td align='center'>hotUpdateScriptsURL</td>
                      <td align='center'>
                          <input type='text' name='hotUpdateScriptsURL' id='hotUpdateScriptsURL' v-bind:value="settingInfo.hotUpdateScriptsURL" style='width:100%;height:30px;' class='input'/>
                      </td>
                    </tr>

                    <tr>
                      <td align='center'>updateAndroid</td>
                      <td align='center'>
                          <input type='text' name='updateAndroid' id='updateAndroid' v-bind:value="settingInfo.updateAndroid" style='width:100%;height:30px;' class='input'/>
                      </td>
                    </tr>

                    <tr>
                      <td align='center'>updateYYB</td>
                      <td align='center'>
                          <input type='text' name='updateYYB' id='updateYYB' v-bind:value="settingInfo.updateYYB" style='width:100%;height:30px;' class='input'/>
                      </td>
                    </tr>

                    <tr>
                      <td align='center'>updateAppStore1</td>
                      <td align='center'>
                          <input type='text' name='updateAppStore1' id='updateAppStore1' v-bind:value="settingInfo.updateAppStore1"  style='width:100%;height:30px;' class='input'/>
                      </td>
                    </tr>

                    <tr>
                      <td align='center'>updateAppStore2</td>
                      <td align='center'>
                          <input type='text' name='updateAppStore2' id='updateAppStore2' v-bind:value="settingInfo.updateAppStore2"style='width:100%;height:30px;' class='input'/>
                      </td>
                    </tr>

                     <tr>
                              <td colspan="2" align='center'><button type="submit" class="btn btn-primary">保存更改</button></td>
                     </tr>
                </table>
              </form>
          </div>
</div>
<script type="text/javascript">

    function initPage(result){  //渲染页面
        var hot_app = new Vue({
            el : '#hot_app',
            data:{
                settingInfo  : '',
                action       : ''

            },mounted:function(){
                var self = this;
                self.$data.settingInfo=result.setting_info;
                self.$data.action="{{action}}";

            },methods:{
                onSubmit:function(e){
                    e.preventDefault();
                    formAjax($('#createConfig').attr("action"),$('#createConfig').attr("method"), $('#createConfig').serialize(),'正在保存...');
                },

                onBack:function(e){
                    e.preventDefault();
                }
            }
        });
        console.log(hot_app.settingInfo);
    }

    $(function(){   //获取渲染数据
        var api = String.format("/admin/setting/hotUpDateSetting/{0}","{{action}}");
        $.getJSON(api,function(result){
            if (result)
                initPage(result);
        });
    });
</script>
%rebase admin_frame_base
