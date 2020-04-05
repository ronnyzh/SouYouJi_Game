<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
    %include admin_frame_header
    <div class="content" id="goods_create_app" style="float:left;width:100%;position:relative;top:2.6em">
        <form class='form-horizontal group-border-dashed' action="{{ info['subUrl'] }}" method='POST' id='broadcastForm'
              onSubmit='return false'>
            <input type='hidden' name='gameId' value="{{ info['defaultGameId'] }}"/>
            <input type='hidden' name='broad_belone' value="{{ info['broad_belone'] }}"/>
            <table class='table config-table'>
                <tr>
                    <td width='20%' class='table-title' style="font-size:20px;background-color:#d9edf7;">创建广播</td>
                </tr>
                <tr>
                    <td>
                        <table class='table config-table' border='1'>
                            <tr>
                                <td class='table-title'>广播类型</td>
                                <td>
                                    %if info['agent_type'] in ['0']:
                                    <input type="radio" checked='checked' name="broad_type" value='0'
                                           class="broad_type"/>&nbsp;全服维护广播&nbsp;&nbsp;
                                    <input type="radio" name="broad_type" value='1' class="broad_type"/>&nbsp;全服循环广播&nbsp;&nbsp;
                                    %elif info['agent_type'] in ['1']:
                                    <input type="radio" checked='checked' name="broad_type" value='2'
                                           class="broad_type"/>&nbsp;地区维护广播&nbsp;&nbsp;
                                    <input type="radio" name="broad_type" value='3' class="broad_type"/>&nbsp;地区循环广播&nbsp;&nbsp;
                                    %end
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>开始时间</td>
                                <td>
                                    <div class="input-group date timeStamp col-sm-1" data-min-view="0"
                                         data-date-format="yyyy-mm-dd hh:ii">
                                        <input class="form-control" style='width:180px;' id='pick-date-end'
                                               name="start_date" size="18" type="text"
                                               value="{{lang.INPUT_LABEL_END_DATE_TXT}}" readonly>
                                        <span class="input-group-addon btn btn-primary pickdate-btn1"><span
                                                class="pickdate1 glyphicon pickdate-btn1 glyphicon-th"></span></span>
                                    </div>
                                </td>
                            </tr>
                            <tr class="endDateDiv" style='display:none;'>
                                <td class='table-title'>结束时间</td>
                                <td>
                                    <div class="input-group date timeStamp col-sm-1" data-min-view="0"
                                         data-date-format="yyyy-mm-dd hh:ii">
                                        <input class="form-control" size="18" type="text" style='width:180px;'
                                               id='pick-date-start' name="end_date"
                                               value="{{lang.INPUT_LABEL_START_DATE_TXT}}" readonly>
                                        <span class="input-group-addon btn btn-primary pickdate-btn1"><span
                                                class="pickdate1 glyphicon pickdate-btn1 glyphicon-th"></span></span>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>广播内容</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' id="content" name="content"
                                           class="form-control" placeholder="必填">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>广播间隔（秒）</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' id="per_sec" name="per_sec"
                                           class="form-control" placeholder="必填">
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div style="text-align:center;padding: 10px 10px 10px;">
                            <button type="submit" class="btn btn-primary btn-sm"><i class="glyphicon"> {{lang.BTN_SUBMIT_TXT}} </i></button>
                            <button type="button" class="btn btn-primary btn-sm" id="backid"><i class="glyphicon"> {{lang.BTN_BACK_TXT}} </i></button>
                        </div>
                    </td>
                </tr>
            </table>
        </form>
    </div>
</div>
</div>
<script type="text/javascript">

    $('.broad_type').click(function () {
        var choosVal = $(this).val()
        console.log('--------------chose value' + choosVal);
        if (['0', '2'].indexOf(choosVal) >= 0) {
            $('.endDateDiv').css({'display': 'none'});
        } else {
            $('.endDateDiv').css({'display': 'table-row'});
        }
    });
    var firstDate = new Date();
    $('#pick-date-start').val(firstDate.Format("yyyy-MM-dd hh:mm"));
    $('#pick-date-end').val(firstDate.Format("yyyy-MM-dd hh:mm"));

    $('#broadcastForm').submit(function () {
        formAjax($(this).attr("action"), $(this).attr("method"), $(this).serialize(), '正在提交...');
    });

    $('#backid').click(function () {
        window.location.href = "{{info['backUrl']}}";
    });

</script>
%rebase admin_frame_base
