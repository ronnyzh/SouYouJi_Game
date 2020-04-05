<div class="table-toolbar" style="float:left;width:100%;position:relative;top:3.2em">
          <div class='col-sm-12' style='margin-left:1em;'>
                  %if info.has_key('group_search'):
                  <!-- 查询代理ID -->
                  <div style='float:left;margin-left:1em;'>
                      <input type="text" placeholder="请输入代理ID" id='group_id' name="group_id" style="width:100px;height:28px;"/>
                  </div>
                  %end

                  %if info.has_key('user_search'):
                    <!-- 是否增加查询房间 -->
                    <!-- 查询代理ID -->
                    <div style='float:left;margin-left:1em;'>
                        <input type="text" placeholder="请输入玩家ID" id='user_id' name="user_id" style="width:100px;height:28px;"/>
                    </div>
                  %end

                  %if info.has_key('room_search'):
                    <!-- 是否增加查询房间 -->
                    <div style='float:left;margin-left:1em;'>
                        <select name='room_name' id='room_name' style='height:28px;'>
                              <option value="">所有房间</option>
                              %for room in info['rooms']:
                                  <option value="{{room['room_id']}}">{{room['room_name']}}</option>
                              %end
                        </select>
                    </div>
                  %end
                  <div style='float:left;margin-left:-1em;' class="input-group date datetime col-md-1 col-xs-1"data-min-view="2" data-date-format="yyyy-mm-dd">
                    <input class="form-control" size="12" type="text" style='width:140px;height:28px;' id='pick-date-start' name="startdate" value="{{lang.INPUT_LABEL_START_DATE_TXT}}" readonly>
                    <span class="input-group-addon btn btn-primary pickdate-btn"><span class="glyphicon pickdate-btn pickdate glyphicon-th"></span>
                  </div>

                  <div style='float:left;margin-left:1em;' class="input-group date datetime col-md-1 col-xs-1"  data-min-view="2" data-date-format="yyyy-mm-dd">
                    <input class="form-control" style='width:140px;height:28px;' id='pick-date-end' name="enddate" size="12" type="text" value="{{lang.INPUT_LABEL_END_DATE_TXT}}" readonly>
                    <span class="input-group-addon btn btn-primary pickdate-btn"><span class="pickdate glyphicon pickdate-btn glyphicon-th"></span></span>
                  </div>
                  <div style='float:left;margin-left:1em;'>
                          <button id="btn_query" class='btn btn-primary btn-sm'>{{lang.INPUT_LABEL_QUERY}}</button>
                          <button id="btn_lastMonth" class='btn btn-sm'>{{lang.INPUT_LABEL_PREV_MONTH}}</button>
                          <button id="btn_thisMonth" class='btn btn-sm'>{{lang.INPUT_LABEL_CURR_MONTH}}</button>
                          <button id="btn_lastWeek" class='btn btn-sm'>{{lang.INPUT_LABEL_PREV_WEEK}}</button>
                          <button id="btn_thisWeek" class='btn btn-sm'>{{lang.INPUT_LABEL_CURR_WEEK}}</button>
                          <button id="btn_yesterday" class='btn btn-sm'>{{lang.INPUT_LABEL_PREV_DAY}}</button>
                          <button id="btn_today" class='btn btn-sm'>{{lang.INPUT_LABEL_CURR_DAY}}</button>
                         <div class='clearfix'></div>
                  </div>
          </div>
</div>
<!-- 初始化搜索栏的日期 -->
<script type="text/javascript">
var firstDate=new Date();
    firstDate.setDate(firstDate.getDate()-6);
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(new Date().Format("yyyy-MM-dd"));
</script>
