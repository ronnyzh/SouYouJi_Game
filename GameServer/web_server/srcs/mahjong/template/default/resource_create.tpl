<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/agent_create.js"></script>
<style type="text/css">
    .config-table td.table-title{text-align:center;width:20%;font-size:13px;vertical-align:middle}
</style>
<div class="cl-mcont">
    <div class="block">
        <div class="header bordered-bottom bordered-themesecondary" id="crumb">
            %if info.get('title', None):
            <i class="widget-icon fa fa-tags themesecondary"></i>
            <span class="widget-caption themesecondary" style='font-size:16px;font-weight:bold' id="subTitle">{{info['title']}}</span>
            %end
        </div>
        <div class="content">
            <form class='form-horizontal group-border-dashed' enctype="multipart/form-data"
                  action="{{info['submitUrl']}}" method='post' id='fileCreate' >
                <table class='table config-table'>
                    <td class='table-title'>
                        基本信息<br/>
                        %if defined('setting') and setting.get("title"):
                        <img src="{{setting['url']}}" alt="{{setting['title']}}" style="height: 100px">
                        %end
                    </td>
                    <td>
                        <table class='table config-table'>
                            <tr class="hide">
                                <td class='table-title min_base_txt'>ID:</td>
                                <td>
                                    <div class="col-sm-12">
                                        %if defined('setting') and setting.get("id"):
                                            <input type='text' style='width:100%;float:left' name='id'
                                            value = "{{setting['id']}}" class="form-control">
                                        %end
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title min_base_txt'>标题:</td>
                                <td>
                                    <div class="col-sm-12">
                                        <input type='text' style='width:100%;float:left' name='title'
                                       %if defined('setting') and setting.get("title"):
                                        value = "{{setting['title']}}"
                                        %end
                                        class="form-control">
                                    </div>
                                </td>
                            </tr>
                            <!--<tr>
                                <td class='table-title min_base_txt'>发放类型:</td>
                                <td>
                                    <div class="col-sm-12">

                                            %if defined('setting') and setting.get("typeList"):
                                                %for item in setting['typeList']:
                                                <div class="col-sm-2">
                                                    <label  class="form-control">
                                                        <input type='radio' name='type'
                                                               value = "{{item['value']}}"
                                                               {{ "checked" if setting.get('type') and item['value'] == setting['type'] else "" }}
                                                        >{{item['name']}}
                                                    </label>
                                                </div>
                                                %end
                                            %end



                                    </div>
                                </td>
                            </tr>-->
                            <tr>
                                <td class='table-title min_base_txt'>备注:</td>
                                <td>
                                    <div class="col-sm-12">
                                        <input type='text' style='width:100%;float:left' name='note'
                                               %if defined('setting') and setting.get("note"):
                                        value="{{setting['note']}}"
                                        %end
                                        class="form-control">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title min_base_txt'>上传图片:</td>
                                <td>
                                    <div class="col-sm-12">
                                        <label>
                                            <input type='file' name='file'>
                                        </label>

                                    </div>
                                </td>
                            </tr>
                        </table>
                    </td>
                </table>

                <div class="modal-footer" style="text-align:center">
                    <button type="submit" class="btn btn-sm btn-xs btn-primary btn-mobile">
                        %if info.get("submitText"):
                        {{info["submitText"]}}
                        %else :
                        提交
                        %end
                    </button>
                    <button type="button" class="btn btn-sm btn-xs btn-primary btn-mobile" name="backid" id="backid">
                        返回
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
<script type="text/javascript">
    $('#backid').click(function(){
        window.location.href="{{info['backUrl']}}";
   });
//    $("#agentCreate").bootstrapValidator({
//        feedbackIcons:{
//            valid: 'glyphicon glyphicon-ok',
//            invalid: 'glyphicon glyphicon-remove',
//            validating: 'glyphicon glyphicon-refresh'
//        },
//        message:'不能为空',
//        fields:{
//            title:{
//                validators: {
//                    notEmpty: {}
//                }
//            },
//            file:{
//                validators: {
//                    notEmpty: {}
//                }
//            },
//        }
//    }).on('success.form.bv', function(e) {
//        // 阻止默认事件提交
//        e.preventDefault();
//    });
//
//
//    $("#sub").on("click", function (e) {
//        document.preventDefault();
//        //获取表单对象
//        var bootstrapValidator = $("#agentCreate").data('bootstrapValidator');
//
//        //手动触发验证
//        $("#agentCreate").on('success.form.bv', function(e) {
//                // 阻止默认事件提交
//                e.preventDefault();
//            });
//        bootstrapValidator.validate();
//        if (bootstrapValidator.isValid()) {
//            console.log("bootstrapValidator", arguments);
//            //表单提交的方法、比如ajax提交
//
//
//        }
//    })



</script>
%rebase admin_frame_base