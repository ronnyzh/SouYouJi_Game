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
                  action="{{info['submitUrl']}}" method='post' id='broadcastForm'
                  onSubmit='return false'
            >
            <div class="col-md-2 col-sm-12 text-center">
                <div class="panel panel-default">
                    <div class="panel-body">
                        <button type="button" class="btn btn-primary " id="btn-edit" >编辑</button>
                    </div>
                </div>

                <div class="panel panel-default" id="matchState0"
                     style="{{'' if info.get('competitionState','0') == 0 else 'display : none'}}"
                >
                    <div class="panel-body">
                        <div class="text-muted">
                            竞技场已 <span class="text-danger">关闭</span> 。
                        </div>
                        <button type="button" class="btn btn-success " id="btn-open">开启</button>
                    </div>
                </div>
                <div class="panel panel-default" id="matchState1"
                     style="{{'display : none' if info.get('competitionState','0') == 0 else ''}}"
                >
                    <div class="panel-body">
                        <div class="text-muted">
                            竞技场已 <span class="text-success">开启</span> 。
                        </div>
                        <button type="button" class="btn btn-danger " id="btn-close">关闭</button>
                    </div>
                </div>

            </div>
            <div class="col-md-10 col-sm-12">
                <div class="col-md-12" id="form-body">
                    <div class="panel panel-default">
                        <div class="panel-body">
                            <div class="col-md-2">开启时间：</div>
                            <div class="col-md-2">
                                <div class="input-group date datetime col-md-12 col-xs-12"
                                     data-date-format="hh:ii:00">
                                    <input class="form-control" name="starTime"
                                           type="text" readonly
                                           value=""
                                    >
                                    <span class="input-group-addon btn btn-primary pickdate-btn">
                                        <span class="pickdate glyphicon pickdate-btn glyphicon-th"></span>
                                    </span>
                                </div>
                            </div>
                            <div class="col-md-1 text-center">~</div>
                            <div class="col-md-2">
                                <div class="input-group date datetime col-md-12 col-xs-12"
                                     data-date-format="hh:ii:00">
                                    <input class="form-control" name="endTime"
                                           type="text" readonly
                                           value=""
                                    >
                                    <span class="input-group-addon btn btn-primary pickdate-btn">
                                        <span class="pickdate glyphicon pickdate-btn glyphicon-th"></span>
                                    </span>
                                </div>
                            </div>
                            <div class="col-md-1">
                                <button type="button"  class="btn btn-danger btn-small del" >
                                    删除
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-12 text-center">
                    <button type="button" class="btn btn-primary " id="btn-add">增加</button>
                    <button type="submit"  class="btn btn-primary " id="btn-save"  cb-data="listSave">保存</button>
                </div>
            </div>
            </form>
        </div>
    </div>
</div>
<script type="text/javascript">
    $('#backid').click(function(){
        window.location.href="{{info['backUrl']}}";
   });
    //timepicker
    var timepickerSetting = {
        startDate : "",
        autoclose: true,
        language: 'zh-CN',
        startView : 1,
        maxView : 1,
        minuteStep : 10,
    }

    $(document).ready(function(){
        //按钮赋值
        var btnAgentNew =new btnAgent();
        %if info.get('competitionTime',""):
            %for list in info['competitionTime']:
                btnAgentNew.dataPush(["{{list[0]}}","{{list[1]}}"]);
            %end
        %end
        //提交数据
        $('#broadcastForm').submit(function () {
                if( !btnAgentNew || !btnAgentNew.check()){return ;}
                var data = $(this).serializeArray().reduce(function(sum,obj,ind){
                                        ind % 2 === 0 ?  sum.push(obj.value) : sum.push([sum.pop(),obj.value]) ;
                                        return sum;
                                        },[]);
                if (!data) {
                    return;
                }
                jsonAjax($(this).attr("action"), $(this).attr("method"), JSON.stringify(data), '正在提交...');
            });
    });
    //实现一个垃圾的类-只包含extend功能
        var cla = function(){};
        cla.extend = function (param) {
            var prototype = cla.prototype;
            Object.keys(param).forEach(function(key){
                prototype[key] = param[key]
            });
            prototype.extend = arguments.callee;
            var cl = param["ctor"] || function () {};
            cl.prototype = prototype;
            return cl;
        };

        //按钮代理
        var btnAgent = cla.extend({
            ctor : function(){
                this.$container = $("#form-body");
                this.isEditing = false;

                //获得第一份表单的拷贝
                var fpanel = $("#form-body > .panel").first();
                this.$formGroup = fpanel.clone();
                fpanel.remove();

                //按钮可视初始化
                this.btnEdit = $("#btn-edit");
                this.btnEdit.click(this.listEdit.bind(this));

                this.btnOpen = $("#btn-open");
                this.btnOpen.click(this.matchOpen.bind(this));

                this.btnClose = $("#btn-close");
                this.btnClose.click(this.matchClose.bind(this));

                this.btnAdd = $("#btn-add");
                this.btnAdd.hide();
                this.btnAdd.click(this.listAdd.bind(this));

                this.btnSave = $("#btn-save");
                this.btnSave.hide();

                var self = this;
                this.$container.delegate("button.del","click",function(){
                    self.listDel.call(self, this);
                });

            },
            listEdit : function(){
                this.isEditing = true;

                this.$container.find("> .panel").each(function(ind,ele){
                    this.listItemInit($(ele));
                }.bind(this));

                this.btnEdit.hide();
                this.btnAdd.show();
                this.btnSave.show();
            },
            listAdd : function(){
                var item = this.$formGroup.clone();
                this.listItemInit(item);
                this.$container.append(item);
                return item;
            },
            listDel : function(btn){
                $(btn).parents(".panel").first().remove();
            },

            matchOpen : function(){
                this.sendMatchOpen(function(res){
                    var res = typeof res === "string"? JSON.parse(res) : res;
                    if (res.code == 0) {
                        this.btnOpen.parents(".panel").first().hide();
                        this.btnClose.parents(".panel").first().show();
                    }

                }.bind(this));
            },
            matchClose : function(){
                this.sendMatchClose(function(res){
                    var res = typeof res === "string"? JSON.parse(res) : res;
                    if(res.code == 0) {
                        this.btnOpen.parents(".panel").first().show();
                        this.btnClose.parents(".panel").first().hide();
                    }

                }.bind(this));
            },

            /*操作*/
            sendMatchOpen : function(callback){
                var data = {};
                var url = "{{info['openUrl']}}";
                $.ajax({
                    type: "post",
                    data: data,
                    url: url,
                    success: callback || function(){}
                });
            },
            sendMatchClose : function(callback){
                var data = {};
                var url = "{{info['closeUrl']}}";
                $.ajax({
                    type: "post",
                    data: data,
                    url: url,
                    success: callback || function(){}
                });
            },
            dataPush : function(arr){
                if(arr){
                    var item = this.listAdd();
                    item.find("input[name='starTime']").val(arr[0])
                    item.find("input[name='endTime']").val(arr[1])
                }
            },
            /***/
            listItemInit : function($formGroupClone){
                var datetimepicker = $formGroupClone.find(".datetime");
                var btnDel = $formGroupClone.find("button.del");

                if(this.isEditing){
                    //初始化timepicker
                    datetimepicker.each(function(ind,ele){
                        $(ele).one("click",function () {
                            $(ele).find("input").val("");
                            $(ele).datetimepicker(timepickerSetting);
                        })
                    });

                    btnDel.show();
                }else{
                    datetimepicker.unbind("click");
                    datetimepicker.datetimepicker('remove');
                    btnDel.hide();
                }

            }/***/,
            check : function(){
                var inputs = this.$container.find("input[name]");
                var ispass = inputs.length > 0 ;
                inputs.each(function(ind,ele){
                    var $ele = $(ele),
                        value = $ele.val();
                    if(!value){
                        ispass = false;
                        var def = $ele.css("borderColor");
                        $ele.css("borderColor","red");
                        setTimeout(function(){
                            $ele.css("borderColor",def);
                        },2000)
                    }
                });
                return ispass
            }
        })


    function serializeDeal(options) {
            var options = this.options = $.extend(true, options, serializeDeal.DEFAULT_OPTIONS);

            var res = {};

            //处理特殊列表
            this.getSpecialName = function (keyName) {
                var name = false,
                    special = this.options.special;
                Object.keys(special).map(function (ruleName) {
                    if (special[ruleName].indexOf(keyName) !== -1) {
                        name = ruleName;
                    }
                });
                return name;
            };
            //数据赋值
            this.key2Value = function (obj, key, val) {
                if (key in obj) {
                    obj[key] = obj[key] instanceof Array
                        ? obj[key].concat(val)
                        : [obj[key]].concat(val);
                } else {
                    obj[key] = options.theList.indexOf(key) === -1 ? val: [val];
                }
                return obj
            };
            //寻找特殊数据
            this.insertSpecialData = function (specialName, dataName, dataValue) {
                var specialData = res[specialName] = res[specialName] || [];
                //先判断该字段最后出现的ind
                var specialInd = specialData.concat().pop()
                    ? dataName in specialData.concat().pop()
                        ? specialData.length
                        : specialData.length - 1
                    : 0
                ;
                var specialObj = specialData[specialInd] = specialData[specialInd] || {};
                this.key2Value(specialObj, dataName, dataValue);
            };

            Object.keys(this.options.data).forEach(function (ind) {
                var dataObj = this.options.data[ind],
                    dataName = dataObj["name"],
                    dataValue = dataObj["value"];

                var specialName = this.getSpecialName(dataName);
                if (specialName) {
                    this.insertSpecialData(specialName, dataName, dataValue);
                } else {
                    this.key2Value(res, dataName, dataValue);
                }
            }, this);

            return res;
        };
        serializeDeal.DEFAULT_OPTIONS = {
            data: [],
            theList:[],//强制使用数组的字段
            special: {},
        };
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