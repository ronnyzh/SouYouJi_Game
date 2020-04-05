%if info['submitUrl'][-6:] == 'create':
<tr>
     <td class='table-title'>
                最低炮等级<br/>
                <small>游戏最低炮等级</small>
         </td>
         <td>
              <input type="text" style='width:100%;float:left' id="base_coin" name="base_coin" class="form-control">
         </td>
    </tr>
    <tr>
         <td class='table-title'>
                最高炮等级<br/>
                <small>游戏最高炮等级</small>
         </td>
         <td>
              <input type="text" style='width:100%;float:left' id="max_base_coin" name="max_base_coin" class="form-control">
         </td>
    </tr>
    <tr>
         <td class='table-title'>
                步长底分<br/>
                <small>游戏中玩家切换的炮分间隔值</small>
         </td>
         <td>
                <input type="text" style='width:100%;float:left' id="step_base_coin" name="step_base_coin" class="form-control">
         </td>
    </tr>
</tr>
%else:
<tr>
     <td class='table-title'>
                最低炮等级<br/>
                <small>游戏最低炮等级</small>
         </td>
         <td>
              <input type="text" style='width:100%;float:left' v-bind:value="roomInfo.base_coin" id="base_coin" name="base_coin" class="form-control">
         </td>
    </tr>
    <tr>
         <td class='table-title'>
                最高炮等级<br/>
                <small>游戏最高炮等级</small>
         </td>
         <td>
              <input type="text" style='width:100%;float:left' v-bind:value="roomInfo.max_base_coin" id="max_base_coin" name="max_base_coin" class="form-control">
         </td>
    </tr>
    <tr>
         <td class='table-title'>
                步长底分<br/>
                <small>游戏中玩家切换的炮分间隔值</small>
         </td>
         <td>
                <input type="text" style='width:100%;float:left' v-bind:value="roomInfo.step_base_coin" id="step_base_coin" name="step_base_coin" class="form-control">
         </td>
    </tr>
</tr>
%end
