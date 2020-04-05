<div class="table-toolbar" style="float:right;border-radius:5px;width:100%;height:50px;position:relative;">
          <div class='col-sm-12'>
                  <div style='float:right;'>
                      <div style='float:right;margin-left:1em;'>
                          <input type="text" id="searchId"  placeholder="{{info['searchTxt']}}" name="id" value="" style='width:200px;height:30px;'/>
                           <button id="btn_search" v-bind:click="onRefresh()" class='btn btn-primary btn-sm'>{{lang.INPUT_LABEL_QUERY}}</button>
                      </div>
                      %if info.has_key('show_date_search'):
                          <div style='float:right;margin-left:1em;' class="input-group date datetime col-md-1 col-xs-1"  data-min-view="2" data-date-format="yyyy-mm-dd">
                            <input class="form-control" style='width:140px;' id='pick-date-end' name="enddate" size="18" type="text" value="{{lang.INPUT_LABEL_END_DATE_TXT}}" readonly>
                            <span class="input-group-addon btn btn-primary pickdate-btn"><span class="pickdate glyphicon pickdate-btn glyphicon-th"></span></span>
                          </div>
                          <div style='float:right;margin-left:1em;' class="input-group date datetime col-md-1 col-xs-1"data-min-view="2" data-date-format="yyyy-mm-dd">
                            <input class="form-control" size="18" type="text" style='width:140px;' id='pick-date-start' name="startdate" value="{{lang.INPUT_LABEL_START_DATE_TXT}}" readonly>
                            <span class="input-group-addon btn btn-primary pickdate-btn"><span class="glyphicon pickdate-btn pickdate glyphicon-th"></span>
                          </div>
                      %end
                  </div>
          </div>
</div>
<div style='clear:both'></div>
<script type="text/javascript">
    var firstDate=new Date();
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd"));
    $('#pick-date-end').val(firstDate.Format("yyyy-MM-dd"));
</script>
