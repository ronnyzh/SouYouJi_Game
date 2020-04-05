<style type="text/css">.config-table td.table-title{text-align:center;font-size:13px;vertical-align:middle}</style>
<div class='block'>
          %include admin_frame_header
          <div class="content" id="game_create_app">
             <form class="form-horizontal group-border-dashed" id='gameForm' @submit="onSubmit" action="{{info['submitUrl']}}" method="post" style="border-radius: 0px;" enctype="multipart/form-data">
               <table class='table config-table'>
                        <tr>
                          <td width='20%' class='table-title'>任务创建</td>
                        </tr>
                        <tr>
                              <td class=''>说明信息：
                               
                              
                              
                              
                              </td>
                              <td>
                                <table class='table config-table' border='1'>
                                    <tr>
                                         <td class='table-title'>任务ID</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="id" name="id" value="系统自动配置" disabled=true class="form-control">
                                             <label for='id' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>任务说明</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="description" name="description" class="form-control">
                                             <label for='name' class='hitLabel' style='float:left;line-height:30px'>*</label>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>任务分类</td>
                                         <td>
                                             <select name="taskType" id="taskType" class="form-control" style='float:left;line-height:30px'>
                                                <option value="1">金币场</option>
                                                <option value="2">比赛场</option>
                                                <option value="3">大厅</option>
                                             </select>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>条件<br/>
                                                <small>每一种条件意义都不相同！请参考文档进行配置</small>
                                         </td>
                                         <td>
                                            <table style='width:100%;float:left' >
                                            <tr>
                                                <td>细分类型</td>
                                                <td colspan=4>
                                                 <select name="whereHead" id="whereHead" class="form-control" style='float:left;line-height:30px'>
                                                    <option value="gold">金币数</option>
                                                    <option value="win">胜局数</option>
                                                    <option value="lost">败局数</option>
                                                    <option value="sports">竞技场</option>
                                                    <option value="other">其他</option>
                                                </select>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>类型(数字)</td>
                                                <td>
                                                <!-- <td><input type="number" style='width:100%;float:left' id="whereType" name="whereType" class="form-control"></td> -->
                                                <select name="whereType" id="whereType" class="form-control" style='float:left;line-height:30px'>
                                                    
                                                </select>
                                                </td>
                                                <td>值</td>
                                                <td><input type="text" style='width:100%;float:left' id="whereValue" name="whereValue" class="form-control"></td>
                                            </tr>
                                             <tr>
                                                <td>排行值(只有需要用到排行时生效):</td>
                                                <td>
                                                <input type="number" style='width:100%;float:left' id="whereSort" name="whereSort" class="form-control">
                                                </td>
                                                <td>指定星期生效(0-6, 0=周末)</td><td>
                                                <!-- <input type="number" style='width:100%;float:left' id="whereWeek" name="whereWeek" class="form-control"> -->
                                                    <select name="whereWeekType" id="whereWeekType" class="form-control" style='float:left;line-height:30px'>
                                                        <option value="">每天</option>
                                                        <option value="0">周日</option>
                                                        <option value="1">周一</option>
                                                        <option value="2">周二</option>
                                                        <option value="3">周三</option>
                                                        <option value="4">周四</option>
                                                        <option value="5">周五</option>
                                                        <option value="6">周六</option>
                                                    </select>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>开始时间（选择填写格式：YYYY-MM-DD）:</td>
                                                <td>
                                                    <input type="text" style='width:100%;float:left' id="whereStartDate" name="whereStartDate" class="form-control">
                                                </td>
                                                <td>结束时间（选择填写格式：YYYY-MM-DD）:</td>
                                                <td>
                                                    <input type="text" style='width:100%;float:left' id="whereEndDate" name="whereEndDate" class="form-control">
                                                </td>
                                            </tr>
                                             </table>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>返回奖励</td>
                                         <td>
                                             <table style='width:100%;float:left' >
                                                <tr>
                                                    <td>金币奖励:</td>
                                                    <td>
                                                        <input type="number" style='width:100%;float:left' id="masonry" name="masonry" class="form-control">
                                                    </td>
                                                    <td>钻石奖励:</td>
                                                    <td>
                                                        <input type="number" style='width:100%;float:left' id="gold" name="gold" class="form-control">
                                                    </td>
                                                </tr>
                                             </table>
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>称号名称</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="title" name="title" class="form-control">
                                         </td>
                                    </tr>

                                </table>
                              </td>
              </table>
              <div class="modal-footer" style="text-align:center">
                   <button type="submit" class="btn btn-primary">{{lang.BTN_SUBMIT_TXT}}</button>
                  <button type="button" class="btn btn-primary" @click="onBack">{{lang.BTN_BACK_TXT}}</button>
              </div>
            </form>
    </div>
</div>
<script type="text/javascript">

    var typeData = {
        gold: [
        {"id": 1, "value": "指定多少天金币最多的"},
        {"id": 2, "value": "当前金币数量"}
        ],
        win: [
        {"id": 1, "value": "普通胜场"},
        {"id": 2, "value": "连续胜场"}
        ],
        lost: [
        {"id": 1, "value": "普通敗场"},
        {"id": 2, "value": "连续敗场"},
        {"id": 3, "value": "特殊失败(连续点炮)"}
        ],
        sports: [
        {"id": 1, "value": "获得竞技场名次奖励"}
        ],
        other: [
        {"id": 1, "value": "俱乐部创建者成员数量"},
        {"id": 2, "value": "分享次数"},
        {"id": 3, "value": "抽奖内容"},
        {"id": 4, "value": "游戏时常"},
        {"id": 5, "value": "连续登录"},
        {"id": 6, "value": "钻石消费"},
        ]
    }



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

        $("#whereHead").change(function() {
            selected = $(this).val()
            dom = ''
            $.each(typeData[selected], function(index, value) {
                dom += "<option value='"+value.id+"'>"+value.value+"</option>"
            });
            $("#whereType").html(dom)
        });
    })
</script>
%rebase admin_frame_base
