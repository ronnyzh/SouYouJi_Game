<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/fileInput/js/fileinput.min.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/fileInput/js/locales/zh.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/fileInput/ds_file_upload.js"></script>
<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
          %include admin_frame_header
          <div class="content">
             <form class="form-horizontal group-border-dashed" id='gameForm' onSubmit="return false;" action="{{info['submitUrl']}}" method="post" style="border-radius: 0px;" enctype="multipart/form-data">
               <input type="hidden" value="{{info['token']}}" id='token' />
               <input type='hidden' name='adId' value="{{ ad_info['ad_id'] }}"/>
               <table class='table config-table'>
                <tr>
                    <td width='20%' class='table-title' style="font-size:20px;background-color:#d9edf7;">编辑广告</td>
                </tr>
                <tr>
                    <td>
                        <table class='table config-table'>
                            <tr>
                                <td class='table-title'>广告名称</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' id="title" name="title"
                                           class="form-control" placeholder="广告名称" value="{{ ad_info['title'] }}">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>广告图片</td>
                                 <td>
                                     <img src="{{ad_info['img_path']}}" style='margin:10px;' id='' width='50' height='50' />
                                  </td>
                            </tr>
                            <tr>
                                <td class='table-title'>重新上传</td>
                                 <td>
                                     <input type="file" name="files" id="txt_file" multiple class="file-loading" />
                                     <input type="hidden" name="img_path" id="img_path" value=""/>
                                  </td>
                            </tr>
                            <tr>
                                <td class='table-title'>播放顺序</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' id="order" name="order"
                                           class="form-control" placeholder="播放顺序" value="{{ ad_info['order'] }}">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>备注信息</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' id="note" name="note"
                                           class="form-control" placeholder="备注信息" value="{{ ad_info['note'] }}">
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div style="text-align:center;padding: 10px 10px 10px;">
                             <button type="submit" class="btn btn-sm btn-primary">{{lang.BTN_SUBMIT_TXT}}</button>
                             <button type="button" class="btn btn-sm btn-primary" id='backid'>{{lang.BTN_BACK_TXT}}</button>
                        </div>
                    </td>
                </tr>
            </table>
            </form>
          </div>
</div>
</div>
<script type="text/javascript">
    $('#gameForm').submit(function(){
          formAjax($(this).attr("action"), $(this).attr("method"), $(this).serialize(),'正在创建...');
    });

    $('#backid').click(function(){
        window.location.href="{{info['backUrl']}}";
    });
    //0.初始化fileinput
    var oFileInput = new FileInput();
    oFileInput.Init("txt_file", "{{info['upload_url']}}");
</script>
%rebase admin_frame_base
