% setdefault('setting',{})
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
        <div class="content ">
            <div class="col-sm-8">
                <form class='form-horizontal group-border-dashed' enctype="application/json"
                      action="{{info.get('submitUrl','')}}" method='post' id='broadcastForm' onSubmit='return false'>
                    <table class='table config-table' id="config-table">
                        <tr>
                            <td class="table-title min_base_txt">
                                活动标题
                            </td>
                            <td>
                                <div class="col-sm-4">
                                    %if setting.get('readOnly'):
                                        {{setting.get('data',{}).get('title','')}}
                                    %else:
                                        <input type="text" class="form-control" name="title" placeholder="请填写标题"
                                           value="{{setting.get('data',{}).get('title','')}}">
                                    %end

                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td class="table-title min_base_txt">
                                起止时间
                            </td>
                            <td>
                                %if setting.get('readOnly'):
                                    <div class="col-sm-2">
                                        {{setting.get('data',{}).get('startdate','')}}
                                    </div>
                                %else:
                                <div style='float:left;margin-left:1em;' class="input-group date datetime col-md-1 col-xs-1"
                                     data-min-view="2" data-date-format="yyyy-mm-dd">
                                    <input class="form-control" style='width:140px;' id='pick-date-start' name="startdate"
                                           size="18"
                                           type="text" placeholder="{{lang.INPUT_LABEL_START_DATE_TXT}}" readonly
                                           value="{{setting.get('data',{}).get('startdate','')}}"
                                    >
                                    <span class="input-group-addon btn btn-primary pickdate-btn"><span
                                            class="pickdate glyphicon pickdate-btn glyphicon-th"></span></span>
                                </div>
                                %end
                                <div class="col-sm-1 text-center">
                                    到
                                </div>
                                %if setting.get('readOnly'):
                                    <div class="col-sm-2">
                                        {{setting.get('data',{}).get('enddate','')}}
                                    </div>
                                %else:
                                <div style='float:left;margin-left:1em;' class="input-group date datetime col-md-1 col-xs-1"
                                     data-min-view="2" data-date-format="yyyy-mm-dd">

                                        <input class="form-control" style='width:140px;' id='pick-date-end' name="enddate"
                                               size="18"
                                               type="text" placeholder="{{lang.INPUT_LABEL_END_DATE_TXT}}" readonly
                                               value="{{setting.get('data',{}).get('enddate','')}}"
                                        >
                                    <span class="input-group-addon btn btn-primary pickdate-btn"><span
                                            class="pickdate glyphicon pickdate-btn glyphicon-th"></span></span>
                                </div>
                                %end
                            </td>
                        </tr>
                        %if bool(info.get('isAdmin','')):
                        <tr>
                            <td class="table-title min_base_txt">
                                限定工会
                            </td>
                            <td>
                                <div class="col-sm-12" id="authListCon" style="max-height: 250px;overflow: auto;">

                                </div>
                            </td>
                        </tr>
                        %end
                        <tr>
                            <td class='table-title min_base_txt'>
                                活动类型:<br/>
                                <span class="text-muted">更换活动类型会重置下面的资料</span>
                            </td>
                            <td>
                                %for item in setting['typeList'] :
                                <div class="col-sm-2 text-center">
                                    %if item['status'] == 0 :
                                    <img src="{{item['imgUrl']}}" alt="{{item['title']}}"
                                         class="img-thumbnail  alert-danger" style="height: 80px;opacity: .4"
                                         data-toggle="tooltip" title="{{item['title']}}:不可选"
                                    >

                                    %else :
                                    <input type="radio" name="type" value="{{item['field']}}" class="hide">
                                    <img src="{{item['imgUrl']}}" alt="{{item['title']}}" class="img-thumbnail "
                                         % #如果readOnly == True 不可点击
                                         % if not setting.get("readOnly",False):
                                            onclick="changeType(this)"
                                         %end
                                         style="height: 80px"
                                         data-toggle="tooltip" title="{{item['title']}}:点击生成对应配置表"
                                    >
                                    %end

                                    <span style="position:absolute;width: 100%;bottom:0;left:0;
                                                        padding: 0 10; background: rgba(255, 255, 255, .6);
                                                        font-size: 1.2em;text-align: center;">
                                                        {{item['title']}}
                                                    </span>
                                </div>
                                %end
                            </td>
                        </tr>
                    </table>

                    <div class="modal-footer" style="text-align:center">
                        % if setting.get('readOnly')  :
                            %if setting.get('isConfirm'):
                            <a href="#" class="btn btn-sm  btn-primary btn-mobile"
                            onclick="comfirmDialog(
                                '{{info.get('submitUrl','#')}}',
                                'get',
                                '{}',
                                '{{info.get('submitText','提交')}}'
                            )">
                                {{info.get("submitText","提交")}}
                            </a>
                            <a href="#" class="btn btn-sm  btn-primary btn-mobile"
                            onclick="comfirmDialog(
                                '{{info.get('refuseUrl','#')}}',
                                'get',
                                '{}',
                                '{{info.get('refuseText','拒绝')}}'
                            )">
                                {{info.get("refuseText","拒绝")}}
                            </a>
                            %end
                        % else:
                        <button type="submit" class="btn btn-sm btn-primary btn-mobile">
                            {{info.get("submitText","提交")}}
                        </button>
                        %end
                        <button type="button" class="btn btn-sm btn-primary btn-mobile" name="backid"
                                id="backid">
                            返回
                        </button>
                    </div>
                </form>
            </div>
            %if not setting.get("readOnly",False):
            <div class="col-sm-4" id="rewardList" >
                %include search
                <table id="agentTable" class="table table-bordered table-hover" ></table>
            </div>
            %end
        </div>

    </div>
</div>


<script src="https://cdn.bootcss.com/bootstrap/3.2.0/js/tooltip.min.js"></script>
<script type="text/javascript">
    $('#backid').click(function(){
        window.location.href="{{info['backUrl']}}";
   });

    //初始化日期组件，如果是readOnly 则不初始化
    %if not setting.get('readOnly',""):
        var myDate = new Date();
        $(".datetime").datetimepicker({
                   autoclose   : true,
                   language    : 'zh-CN',
                   startDate   : myDate.toLocaleDateString()
               });
    %end

    //页面初始化执行
    $(document).ready(function () {
        //提示元素赋值
        $("[data-toggle]").tooltip();

        //如果有活动类型默认值
        %if setting.get('data',{}).get('type',''):
            var img = $("input[name='type'][value='{{setting['data']['type']}}']").next();
            if(img.length > 0 ){
                var div = document.createElement('div');
                div.innerHTML = "{{setting.get('dataString')}}";
                div.innerHTML = div.innerHTML.replace(/[\s]u[\']/g,"'");
                div.innerHTML = div.innerHTML.replace(/[\{]u[\']/g,"{'");
                var readData = JSON.parse(div.innerHTML);

                changeType(img.get(0),readData)

            };
        %end

        //限定工会
        showAgentChildren(
            $("#authListCon"),
            typeof readData === "undefined" ? '' : readData
        );
    });
    /*
    *
    * 变量定义
    *
    *
    * */
    var FIELD_REWARD_ID     = "id",
        FIELD_REWARD_TITLE  = "title",
        FIELD_REWARD_PRICETOTAL  = "priceTotal",
        FIELD_REWARD_NOTE   = "note",
        FIELD_REWARD_URL    = "imgUrl",
        FIELD_ADD_TYPE      = "type",
        FIELD_ADD_REWARD_ID = "rewardId",
        FIELD_ADD_REWARD_URL = "imgUrl",
        FIELD_ADD_REWARD_PUT = "rewardPut",
        FIELD_ADD_REWARD_BASE_REWARD_COUNT = "baseRewardCount",
        FIELD_ADD_REWARD_RATE = "rewardRate",
        FIELD_ADD_REWARD_SIDE = "rewardSide",
        FIELD_ADD_REWARD_SPECIALONLY = "specialOnly",
        FIELD_ADD_INVITE_NUM = "inviteNum",
        FIELD_ADD_GAME_ID   = "gameId",
        FIELD_ADD_GAME_NUM   = "gameNum",
        FIELD_ADD_PROP_ID   = "propId",
        FIELD_ADD_PROP_NUM  = "propNum",
        FIELD_ADD_PLAN_REWARD_ID  = "planRewardId",
        FIELD_ADD_PLAN_REWARD_RATE= "planRewardRate",
        FIELD_ADD_PLAN_NEED_TYPE  = "planNeedType",
        FIELD_ADD_PLAN_NEED_NUM  = "planNeedNum",
        FIELD_ADD_PLAN_LEVEL  = "planNeedLevel",
        FIELD_ADD_ALLOW_AGENT_ID  = "allowAgentId",
        FIELD_ADD_ALLOW_AGENT_NAME  = "allowAgentName",
        FIELD_ADD_ALLOW_AGENT_TYPE  = "allowAgentType"

    ;
    var SELECT_SOURCE = {
        //游戏列表
        [FIELD_ADD_GAME_ID]: [
            %for item in setting['gameList']:
                {value: "{{item['id']}}", text: "{{item['name']}}"},
            %end
        ],
        //消耗品列表
        [FIELD_ADD_PROP_ID]: [
            {value: "001", text: "消耗品1"},
            {value: "002", text: "消耗品2"},
        ],
        //概率方案需求类型
        [FIELD_ADD_PLAN_NEED_TYPE]: [
            {value: "equal", text: "相等"},
            {value: "multiple", text: "倍数"}
        ]
    };
    /*
    *
    * 表单提交
    *
    *
    * */
    $('#broadcastForm').submit(function () {
        var data = template().getFormData(this);
        if(!data){return ; }
        jsonAjax($(this).attr("action"), $(this).attr("method"), JSON.stringify(data), '正在提交...');
    });
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

    /*
    *
    * 点击图片切换表格
    *
    *
    * */
    //活动类型图片点击触发
    var selectedCon = $("<i class='glyphicon glyphicon-ok text-success' style='position:absolute;left:0'></i>");
    function changeType(self,readData) {
        var $self = $(self);

        $self.parent().siblings().each(function(ind,ele){
            $(ele).find("img").removeClass("alert-success");
        });
        $self.parent().append(selectedCon);
        $self.addClass("alert-success");

        var radio = $self.parent().find("input[type='radio']");
        radio.attr("checked",true);
        template(radio.val(),readData);
    };
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

    //定义表单
    transTable = cla.extend({
        ctor: function (tableType) {
            this.tableType = tableType;
            this.tableCon = [];
            this.tableIndex = 0;
            this.target = $("#config-table");
            this.clearStart = this.target.find("tr:last");
            this.dataIndex = 0;
            this.data=[];

            this.readOnly = {{ 'true' if setting.get('readOnly') else 'false'}};
            return this;
        },

        //重置
        reset: function(){
            //构建表单初始化
            this.tableCon = [];
            this.tableIndex = 0;
            //清空原表单数据
            this.clearStart.nextAll().remove();
            //清除原活动类型标识
            this.tmp_type = "";
            //数据自增初始化
            this.dataIndex = -1;
            this.data=[];
            //钩子函数初始化
            this.updateState= function(){};
            this.befordAdd = function (param, ind, data) {};
            this.resetAfter();
            this.resetAfter = function(){};
            //提取数据函数还原
            this.getFormData = function(form){
                return false;
            };
        },

        //钩子函数：重置之后执行，并且会在执行一次后还原成空函数
        resetAfter : function(){

        },

        /*
        *
        * 逻辑函数
        *
        * */

        //提取表单数据
        //每个活动类型表单数据不一样，请单独重写
        getFormData : function(form){
            return false
        },

        //钩子函数：添加奖品前
        befordAdd: function (param, ind, data) {
            //如果需要在添加前判断并阻止添加 请return false
        },

        //添加奖品
        addReward: function (id, imgUrl, title, priceTotal,baseRewardCount,addition) {
            var afterAdd = afterAdd || function(){};
            //获取数据
            var param = {
                id: id,
                imgUrl: imgUrl,
                title: title || "",
                priceTotal: priceTotal || "",
                baseRewardCount: baseRewardCount || "",
                $el: []
            };
            //如果存在补充数据
            if(addition){
                param = $.extend(true,addition,param);
            }

            //判断是否允许插入数据
            var dataIndex = this.dataIndex + 1;

            var beforeRes = this.befordAdd(param,dataIndex,this.data);
            if ( beforeRes === false){return;}
            //允许插入，更新数据序号
            this.data[dataIndex] = $.extend(true, {}, param);
            this.dataIndex = dataIndex;

            //根据表格配置更新表格
            this.tableCon.forEach(function(item, tableIndex){
                this.tableUpdate(tableIndex, dataIndex);
            },this);

            this.updateState();
        },

        removeReward : function(dataIndex){
            var item = this.data[dataIndex]
            if(item){
                item["$el"].forEach(function (ele) {
                    $(ele).remove();
                });
                delete this.data[dataIndex];
                this.updateState();
            }
        },

        //钩子函数：每次增加删除奖品都会调用
        updateState:function(){

        },


        //切换模板
        tmp : function (tableType,readData) {
            var constor = this["tmp_"+tableType];

            if(constor && this.tmp_type!== tableType){
                //重置
                this.reset();
                this.tmp_type = tableType;
                constor.call(this,readData).forEach(function(ele){
                    this.target.append(ele);
                },this);
            }
        },

        //构造dom函数
        createTr: function (options) {
            var options = $.extend({}, {
                title: "",
                content: [],
            },options);
            var tr = $(String.format(
                "<tr>" +
                "<td class='table-title min_base_txt'>{0}</td>" +
                "<td></td>" +
                "</tr>",
                options.title || ""
            ));
            if (options.content instanceof Array) {
                var td = tr.find("td:last");
                options.content.forEach(function (ele) {
                    td.append(ele);
                });
            }
            return tr;
        },
        createDiv: function (css, content) {
            var div = $(String.format(
                "<div class='{0}'>{1}</div>",
                css, typeof content === "string" ? content : ""
            ));
            if (content instanceof Array) {
                content.forEach(function (ele) {
                    div.append(append(ele));
                });
            } else if (typeof content === "object") {
                div.append(content);
            }
            return div;
        },
        createTable: function (css, param, afterAdd,isUpdate) {
            var table = $(String.format(
                "<table class='{0}' ></table>",
                css || ""
            ));
            var tableIndex = this.tableIndex++;

            var tableItem = this.tableCon[tableIndex] = {
                $el : table,
                config : $.extend(true, {}, param),
                afterAdd : afterAdd || function(){}
            } ;

            //更新表格数据
            if(isUpdate){
                this.data.forEach(function(dataItem, ind){
                    this.tableUpdate(tableIndex, ind);
                },this);
                this.updateState();
            }
            return table;
        },
        tableUpdate: function(tableIndex, dataIndex){
            var item = this.tableCon[tableIndex];
            var table = item.$el;
            var config = item.config;
            var afterAdd = item.afterAdd;
            var thead = $("<tr></tr>");
            var tbody = $("<tr></tr>");
            var param = this.data[dataIndex];
            Object.keys(config).forEach(function (key,ind,arr) {
                var option = config[key];
                var con = option["con"];
                var th = option["th"];
                var tdStyle = option['tdStyle'] || "";

                thead.append($(String.format(
                    "<th>{0}</th>", th || ""
                )));
                tbody.append($(
                    "<td style='" + tdStyle + "'>" +
                    String.format(
                        con, param[key] || ""
                    ) +
                    "</td>"
                ));

                if(ind === arr.length-1){
                    afterAdd.call(this, thead, tbody, dataIndex, tableIndex);
                }
            }, this);

            this.data[dataIndex].$el.push(tbody.get(0));
            table.append(
                table.find("th").length === 0 ? thead : "",
                tbody
            );
        },
        delTable : function(element){

            for(var i = 0 ,count = 0, len = this.tableCon.length; i < len ; i++ ,count++){
                var ele = this.tableCon[count];
                if(ele.$el.get(0).isSameNode(element)){
                   ele.$el.remove();
                   this.tableCon.splice(count,count+1);
                   count--;
                }
            }
            return;
        },

        //活动类型-游戏任务

        tmp_mission: function () {
            var constor = [];

            //游戏局数
            var gameSelect = $("<select name='"+FIELD_ADD_GAME_ID+"' class='form-control'></select>");
            constor.push(this.createTr({
                    title: "游戏局数",
                    content: [
                        this.createDiv("col-sm-3", gameSelect),
                        this.createDiv("col-sm-1 text-center", "×"),
                        this.createDiv("col-sm-3", "<input name='"+FIELD_ADD_GAME_NUM+"' class='form-control'>")
                    ]
                }));

            //游戏列表
            var url = typeof SELECT_SOURCE[FIELD_ADD_GAME_ID] === "string" ? SELECT_SOURCE[FIELD_ADD_GAME_ID] : null;
            var data = typeof SELECT_SOURCE[FIELD_ADD_GAME_ID] === "object" ? SELECT_SOURCE[FIELD_ADD_GAME_ID] : null;
            gameSelect.combobox({
                url: url,
                param: null,
                data: data,
                valueField: 'value',
                textField: 'text',
                placeholder: "任意游戏",
                onBuild: null,
                onBeforeLoad: function (param) {},
                onLoadSuccess: function () {},
                onChange: function () {}
            });

            //奖品
            var table = this.createTable(
                "table table-bordered table-condensed",
                {
                    "id": {
                        "th": "奖品id",
                        "tdStyle": "width:80px;",
                        "con": "<input name ='" + FIELD_ADD_REWARD_ID + "' class='form-control' value='{0}' readonly >"
                    },
                    "imgUrl": {
                        "th": "奖品图片",
                        "tdStyle": "width:80px;",
                        "con": "<img src='{0}' style='height:60px;'>"
                    },
                    "title": {
                        "th": "奖品标题",
                        "con": "{0}"
                    },
                    "priceTotal": {
                        "th": "奖品价值",
                        "con": "<span class='priceTotal'>{0}</span>"
                    },
                    "count": {
                        "th": "投放数量",
                        "con": "<input name='" + FIELD_ADD_REWARD_PUT + "' class='form-control' type='number'>"
                    },
                },
                function (thead, tbody, dataIndex, tableIndex) {

                    //删除按钮
                    thead.append($(String.format(
                        "<th>{0}</th>", "操作"
                    )));
                    tbody.append($(
                        "<td >" +
                        "<button type='button' class='btn btn-sm btn-danger' " +
                        "onclick=\"template().removeReward('" + dataIndex + "')\" >删除</button>" +
                        "</td>"
                    ));
                }
            )
            constor.push(
                this.createTr({
                    title: "奖品列表",
                    content: [
                        this.createDiv(
                            "col-sm-12",
                            table
                        ),
                    ]
                }));
            //表格提示语
            var msg = $(
                "<span class='text-muted'>点击右侧插入</span>" +
                "<span class='text-danger'>" +
                "<i class='glyphicon glyphicon-exclamation-sign'></i>该活动类型只能选择一个奖品" +
                "</span>"
            );
            table.before(msg);

            //限制只能选择一个奖品
            this.befordAdd= function (param, ind, data) {
                if($.grep(data,function(n){return n;}).length > 1){
                    return false;
                }
            };
            return constor;
        },

        //活动类型-邀请

        tmp_invite: function () {
            var constor = [];

            //游戏局数
            constor.push(this.createTr({
                title: "邀请人数",
                content: [
                    this.createDiv("col-sm-3", "<input name='" + FIELD_ADD_INVITE_NUM + "' class='form-control' type='number'>"),
                ]
            }))

            //奖品
            var table = this.createTable(
                "table table-bordered table-condensed",
                {
                    "id": {
                        "th": "奖品id",
                        "tdStyle": "width:80px;",
                        "con": "<input name ='" + FIELD_ADD_REWARD_ID + "' class='form-control' value='{0}' readonly >"
                    },
                    "imgUrl": {
                        "th": "奖品图片",
                        "tdStyle": "width:80px;",
                        "con": "<img src='{0}' style='height:60px;'>"
                    },
                    "title": {
                        "th": "奖品标题",
                        "con": "{0}"
                    },
                    "count": {
                        "th": "投放数量",
                        "con": "<input name='" + FIELD_ADD_REWARD_PUT + "' class='form-control' type='number'>"
                    }
                },
                function (thead, tbody, dataIndex) {
                    //删除按钮
                    thead.append($(String.format(
                        "<th>{0}</th>", "操作"
                    )));
                    tbody.append($(
                        "<td >" +
                        "<button type='button' class='btn btn-sm btn-danger' " +
                        "onclick=\"template().removeReward('" + dataIndex + "')\" >删除</button>" +
                        "</td>"
                    ));
                }
            );
            constor.push(this.createTr({
                title: "奖品列表",
                content: [
                    this.createDiv(
                        "col-sm-12",
                        table
                    ),
                ]
            }));
            var msg = $(
                "<span class='text-muted'>点击右侧插入</span>"
            );
            table.before(msg);

            return constor;
        },

        //活动类型-风车

        tmp_turnlate: function (readData) {
            var constor = [];

//            //消耗品选择
//            var propSelect = $("<select name='" + FIELD_ADD_PROP_ID + "' class='form-control'></select>");
//            constor.push(this.createTr({
//                title: "选择消耗品",
//                content: [
//                    this.createDiv("col-sm-3", propSelect),
//                    this.createDiv("col-sm-1 text-center", "×"),
//                    this.createDiv("col-sm-3", "<input name='" + FIELD_ADD_PROP_NUM + "' class='form-control' type='number' placeholder='(单位个，例：1)'>")
//                ]
//            }));
            //任务列表
            (function(){
                var panel = $("<div class='panel panel-default col-sm-10'><div class='panel-body'><table class='table table-bordered table-condensed'></table></div></div>");
                var panelTable = panel.find(">.panel-body >table");
                var addBtn = $("<button type='button' class='btn btn-primary'>增加任务</button>");
                addBtn.on("click",addpart.bind(this));
                constor.push(this.createTr({
                    title: "任务列表",
                    content: [
                        panel,
                        this.createDiv("col-sm-2",this.readOnly ? "" : addBtn)
                    ]
                }));

                function addpart(params){
                    var constorArr =[];
                    //游戏列表
                    var select = $("<select name='"+FIELD_ADD_GAME_ID+"' class='form-control'></select>");
                    var url = typeof SELECT_SOURCE[FIELD_ADD_GAME_ID] === "string" ? SELECT_SOURCE[FIELD_ADD_GAME_ID] : null;
                    var data = typeof SELECT_SOURCE[FIELD_ADD_GAME_ID] === "object" ? SELECT_SOURCE[FIELD_ADD_GAME_ID] : null;

                    select.combobox({
                        url: url,
                        param: null,
                        data: data,
                        valueField: 'value',
                        textField: 'text',
                        placeholder: "任意游戏",
                        onBuild: null,
                        onBeforeLoad: function (param) {},
                        onLoadSuccess: function () {
                            //游戏列表-如果有数据则读取数据
                            if(params && params[FIELD_ADD_GAME_ID]){
                                this.val(params[FIELD_ADD_GAME_ID]);
                            }
                        },
                        onChange: function () {}
                    });
                    if(this.readOnly){
                        select.attr("disabled","disabled");
                    }

                    //删除按钮
                    var delBtn = $("<button class='btn btn-danger btn-sm'>删除</button>");
                    delBtn.on("click",function(){
                        $(this).parents("tr:first").remove();
                    })
                    constorArr.push(this.createTr({
                        title:"任务",
                        content:[
                            this.createDiv("col-sm-3", select),
                            this.createDiv("col-sm-2 text-center", "局数："),
                            this.createDiv(
                                "col-sm-3",
                                String.format(
                                    this.readOnly
                                    ? "{0}"
                                    : "<input name='" + FIELD_ADD_GAME_NUM + "' class='form-control' type='number' placeholder='(单位次，例：10)' value = '{0}'>",
                                    params && params[FIELD_ADD_GAME_NUM] ? params[FIELD_ADD_GAME_NUM] : ""
                                )
                            ),
                            this.createDiv("col-sm-1",this.readOnly ? "" : delBtn)
                        ]
                    }));
                    constorArr.forEach(function(ele){
                        panelTable.append(ele);

                        //局数过滤，不能为空 或小于1
                        var gameNum =ele.find("input[name="+FIELD_ADD_GAME_NUM+"]");
                        checkGameNum = function(){
                            var val = gameNum.val();
                            if(!val || isNaN(val) || Number(val) < 1 ){
                                gameNum.val(1);
                            }
                        };
                        gameNum.on("focusout",checkGameNum);
                        checkGameNum();
                    });
                }

                if(readData && readData['missionList']){
                    try {
                        eval("var itemData = "+readData['missionList'].trim("\""));
                        itemData.forEach(function(data){
                            addpart.call(this,data)
                        },this)
                    }catch(e){
                        console.log(e)
                    }
                }
                //addpark()End
            }).call(this);

            //奖品
            var table = this.createTable(
                "table table-bordered table-condensed",
                {
                    "id": {
                        "th": "奖品id",
                        "tdStyle": "width:80px;",
                        "con": "<input name ='" + FIELD_ADD_REWARD_ID + "' class='form-control' value='{0}' readonly >"
                    },
                    "imgUrl": {
                        "th": "奖品图片",
                        "tdStyle": "width:80px;",
                        "con": "<input name ='" + FIELD_ADD_REWARD_URL + "' class='form-control hide' value='{0}' readonly >" +
                            "<img src='{0}' style='height:60px;'>"
                    },
                    "title": {
                        "th": "奖品标题",
                        "con": "{0}"
                    },
                    "priceTotal": {
                        "th": "奖品价值",
                        "con": "<span class='priceTotal'>{0}</span>"
                    },
//                    [FIELD_ADD_REWARD_BASE_REWARD_COUNT]: {
//                        "th": "基础奖品发放数量",
//                        "con": "<input type='text' name='"+FIELD_ADD_REWARD_BASE_REWARD_COUNT+"' value='{0}'  class='hide'>" +
//                        "<span >{0}</span>"
//                    },
                    [FIELD_ADD_REWARD_PUT]: {
                        "th": "投放数量",
                        "con": "<input name='" + FIELD_ADD_REWARD_PUT + "' class='form-control' type='number' placeholder='' " +
                        "value='{0}' ><label>无限 <input type='checkbox' class='put' ></label>"
                    },
                    [FIELD_ADD_REWARD_RATE]: {
                        "th": "设置概率",
                        "con": "<input name='" + FIELD_ADD_REWARD_RATE + "' class='form-control' type='text' placeholder='(单位%，例：20)' " +
                        "value='{0}' " + (this.readOnly?"readonly":"") +">"                    },
                    [FIELD_ADD_REWARD_SIDE]: {
                        "th": "奖品位置",
                        "con": "<input name='" + FIELD_ADD_REWARD_SIDE + "' class='form-control' type='text' readonly>"
                    },
                    "curl_total": {
                        "th": "物品总价值（估算）",
                        "con": "<span class='curl_total'></span>"
                    },
//                    "baserate": {
//                        "th": "基础概率（估算）",
//                        "con": ""
//                    },
                    "drawCount": {
                        "th": "预计抽取次数（估算）",
                        "con": ""
                    }
                },
                function (thead, tbody, dataIndex, tableIndex) {
                    //概率过滤
                    function rateFilter() {
                        var str = $(this).val();
                        if (isNaN(str) || str === "") {
                            $(this).val(0);
                            return;
                        }
                        str = isNaN(str) ? 0 : str;
                        str = str.replace(/[^0-9\.]/g, "");
                        str = parseFloat(str).toFixed(2);
                        $(this).val(str);
                    }
                    tbody.find("input[name='"+FIELD_ADD_REWARD_RATE+"']").on("focusout",rateFilter);
                    rateFilter.call(tbody.find("input[name='"+FIELD_ADD_REWARD_RATE+"']"));

                    //概率限制100
                    tbody.find("input[name='"+FIELD_ADD_REWARD_RATE+"']").on("focusout",function(){
                        try{
                            var $this = $(this);
                            var $parent = $this.parents("table").first();
                            var $rates = $parent.find("input[name='" + FIELD_ADD_REWARD_RATE + "']");
                            var total = 0;
                            $rates.each(function (ind, ele) {
                                var num = Number(ele.value);
                                if(num)
                                    total += num;
                            });
                            if(total != 100)
                                setTooltip(this,"本列概率之和应该等于100",2000);
                        }catch(e){
                            console.log("//概率限制100出错",e);
                            setTooltip(this,"本列概率之和应该等于100",2000);
                        }

                    });


                    //无限按钮功能赋值
                    (function(){
                        var put = tbody.find("input.put");
                        var putTarget = tbody.find("input[name=" + FIELD_ADD_REWARD_PUT + "]");
                        var tr = tbody;
                        var turnFunc = function (isChecked) {
                            tr.find("span.curl_total").text("");
                            if(typeof isChecked !== "boolean"){
                                var isChecked = put.get(0).checked
                            }else{
                                put.get(0).checked = isChecked;
                            }
                            if (isChecked) {
                                putTarget.attr({"readonly": true, "placeholder": "无限"});
                                putTarget.val("");
                            } else {
                                putTarget.removeAttr("readonly");
                                putTarget.attr({"placeholder": "请输入数量"});
                                putTarget.val("1");
                            }
                        };
                        put.on("click",turnFunc );

                        if(!putTarget.val()) {
                            turnFunc(true);
                        }
                    })();

                    //投放数量过滤
                    tbody.find("input[name=" + FIELD_ADD_REWARD_PUT + "]").on("focusout", function () {
                        var val = this.value.replace(/[^0-9\.\-]/g,"");
                        switch (true){
                            case val === "":
                                break;
                            case isNaN(val):
                                this.value = 1;
                                break;
                            case (!isNaN(val) && Number(val) <= 0 ):
                                this.value = 1;
                                break;
                            default:
                                this.value = val;
                        }
                    });

                    //估算物品总价值
                    var priceTotal = tbody.find("span.priceTotal").text();
                    tbody.find("input[name=" + FIELD_ADD_REWARD_PUT + "]").on("input propertychange ", function () {
                        try {

                            var curl_total = parseInt(priceTotal * this.value);
                            tbody.find("span.curl_total").text(curl_total);
                        } catch (e) {
                            console.log("error:curl_total [priceTotal,value]", priceTotal, this.value)
                        }
                    });
                    if(! this.readOnly){
                        //删除按钮
                        thead.append($(String.format(
                            "<th>{0}</th>", "操作"
                        )));
                        tbody.append($(
                            "<td >" +
                            "<button type='button' class='btn btn-sm btn-danger' " +
                            "onclick=\"template().removeReward('" + dataIndex + "')\" >删除</button>" +
                            "</td>"
                        ));
                    }
                }
            );
            //奖品位置排序
            this.updateState = function(){
                this.tableCon.map(function(item,tableIndex){
                    var input = item.$el.find("[name="+FIELD_ADD_REWARD_SIDE+"]");
                    input.map(function(ind,ele){
                        ele[ele.localName === "input"? "value" : "innerHTML" ] = ind;
                    });
                });
            };
            //奖品列表
            constor.push(this.createTr({
                title: "奖品列表<br/>" +
                "<a href='/assest/activice/admin/turnlate_note.jpg' target='_blank'>" +
                "<img src='/assest/activice/admin/turnlate_note.jpg' alt='' width='210px'>" +
                "</a>",
                content: [
                    this.createDiv(
                        "col-sm-12",
                        table
                    )
                ]
            }));
            //阻止多于七个奖品
            var msg = $(
                "<span class='text-muted'>点击右侧插入</span>" +
                "<span class='text-danger'>" +
                "<i class='glyphicon glyphicon-exclamation-sign'></i>该活动类型只能选择7个奖品" +
                "</span>"
            );
            table.before(msg);
            this.befordAdd = function (param, ind, data) {
                if ($.grep(data,function(n){return n;}).length >= 7) {
                    return false;
                }
            };


            //读取数据
            try {
                var readwardReadData = eval(readData['rewardList'].trim('"'));
                if(readwardReadData){
                    var rewardDataList = [];
                    var self = this;

                    readwardReadData.sort(function(a, b){return a['rewardSide'] - b['rewardSide']})

                    readwardReadData.forEach(function(ele,ind){
                        (function(){
                            var eleData = ele;
                            var index = ind ;
                            //根据奖品id获取奖品信息
                            var postdata = {searchId:eleData[FIELD_ADD_REWARD_ID]}
                            $.ajax({
                                url:"{{info['listUrl']}}",
                                data:postdata,
                                type:"GET",
                                success:function(res){
                                    var res = JSON.parse(res);
                                    if(res.code == 0){
                                        rewardDataList[index] = res['data'][0];
                                    }
                                },
                                complete:function(){
                                    rewardDataList[index] = rewardDataList[index] || [];
                                    rewardDataList[index] =$.extend(true,rewardDataList[index],{id:eleData[FIELD_ADD_REWARD_ID]},eleData);
                                    //满足奖品数
                                    if($.grep(rewardDataList,function(eleData){return eleData;}).length === readwardReadData.length){
                                        rewardDataList.forEach(function(eleData){
                                            self.addReward(
                                                eleData[FIELD_REWARD_ID],
                                                eleData[FIELD_REWARD_URL],
                                                eleData[FIELD_REWARD_TITLE],
                                                eleData[FIELD_REWARD_PRICETOTAL],
                                                eleData[FIELD_ADD_REWARD_BASE_REWARD_COUNT],
                                                eleData
                                            )
                                        })

                                    }
                                }
                            })
                        })()

                    },this);
                }
            }catch(e){
                console.log(e)
            }


            //概率方案

            var panel = $(
                "<div class='panel panel-default'>" +
                "<div class='panel-body'>" +
                "<table class='table table-condensed table-bordered table-hover'></table>" +
                "</div>" +
                "</div>");
            var panelBody = panel.find("> .panel-body > table");
            var addBtn = $("<button type='button'class='btn btn-sm btn-primary'>增加方案</button>");
            addBtn.on("click",addPlan.bind(this));
            constor.push(
                this.createTr({
                    title: "特殊方案配置",
                    content: [
                        this.createDiv(
                            "col-sm-10",
                            panel
                        ),
                        this.createDiv(
                            "col-sm-2",
                            this.readOnly
                                ? ""
                                : addBtn
                        )
                    ]
                })
            );

            function addPlan(params){
                var arr = [];
                //特殊方案触发条件
                var needSelect = $("<select name='" + FIELD_ADD_PLAN_NEED_TYPE + "' class='form-control'" +
                    (this.readOnly?"disabled":"")+"></select>");
                var delBtn = $("<button type='button' class='btn btn-danger btn-sm'>删除方案</button>")
                delBtn.on("click",function(btn){
                    //寻找数据中的table
                    arr.forEach(function(ele){
                        this.delTable($(ele).find("table").get(0));
                    },this);

                    //逐条删除
                    arr.forEach(function(ele){
                        $(ele).remove();
                    });
                }.bind(this,delBtn));
                arr.push(this.createTr({
                    title: "触发条件：",
                    content: [
                        this.createDiv("col-sm-3", needSelect),
                        this.createDiv(
                            "col-sm-3", String.format(
                                this.readOnly
                                ? "{0}"
                                : "<input name='" + FIELD_ADD_PLAN_NEED_NUM + "' class='form-control' type='number' value ='{0}'>",
                                params && params[FIELD_ADD_PLAN_NEED_NUM] ? params[FIELD_ADD_PLAN_NEED_NUM]:""
                            )
                        ),
                        this.createDiv(
                            "col-sm-3 col-sm-offset-3 text-right",
                            this.readOnly?"":delBtn
                        )
                    ]
                }));
                //特殊方案列表
                var url = typeof SELECT_SOURCE[FIELD_ADD_PLAN_NEED_TYPE] === "string" ? SELECT_SOURCE[FIELD_ADD_PLAN_NEED_TYPE] : null;
                var data = typeof SELECT_SOURCE[FIELD_ADD_PLAN_NEED_TYPE] === "object" ? SELECT_SOURCE[FIELD_ADD_PLAN_NEED_TYPE] : null;
                needSelect.combobox({
                    url: url,
                    param: null,
                    data: data,
                    valueField: 'value',
                    textField: 'text',
                    placeholder: null,
                    onBuild: null,
                    onBeforeLoad: function (param) {},
                    onLoadSuccess: function () {},
                    onChange: function () {}
                });
                if(params && params[FIELD_ADD_PLAN_NEED_TYPE]){
                    needSelect.val(params[FIELD_ADD_PLAN_NEED_TYPE]);
                }
                //特殊方案优先级
                arr.push(this.createTr({
                    title: "优先级：",
                    content: [
                        this.createDiv(
                            "col-sm-3",
                            String.format(
                                this.readOnly
                                    ? "{0}"
                                    : "<input name='" + FIELD_ADD_PLAN_LEVEL + "' class='form-control' type='number' placeholder='越大优先级越高' value = '{0}'> ",
                                    params && params[FIELD_ADD_PLAN_LEVEL] ? params[FIELD_ADD_PLAN_LEVEL] : ""
                            )
                        )
                    ]
                }));

                //特殊方案配置
                var table = this.createTable(
                    "table table-bordered table-condensed",
                    {
                        "id": {
                            "th": "奖品id",
                            "tdStyle": "width:80px;",
                            "con": "<input name ='" + FIELD_ADD_PLAN_REWARD_ID + "' class='form-control' value='{0}' readonly >"
                        },
                        "imgUrl": {
                            "th": "奖品图片",
                            "tdStyle": "width:80px;",
                            "con": "<img src='{0}' style='height:60px;'>"
                        },
                        "title": {
                            "th": "奖品标题",
                            "con": "{0}"
                        },
                        "site": {
                            "th": "奖品位置",
                            "con": "<span name='"+FIELD_ADD_REWARD_SIDE+"'>{0}</span>"
                        },
                        "priceTotal": {
                            "th": "奖品价值",
                            "con": "{0}"
                        },
                        [FIELD_ADD_PLAN_REWARD_RATE]: {
                            "th": "修改概率",
                            "con": "<input name='" + FIELD_ADD_PLAN_REWARD_RATE + "' class='form-control' type='text' placeholder='(单位%，例：0)'" +
                            "value='{0}' "+(this.readOnly ? "readonly" : "")+">"
                        }
                    },
                    function(thead, tbody, dataIndex, tableIndex){
                        //如果有数据则写入默认数据
                        if(params && params['specialRate'] ){
                            var data = params['specialRate'][dataIndex][FIELD_ADD_PLAN_REWARD_RATE];
                            if(data){
                                tbody.find("[name="+FIELD_ADD_PLAN_REWARD_RATE+"]").val(data )
                            }
                        }

                        //特殊方案概率过滤
                        function rateFilter() {
                            var str = $(this).val();
                            if (isNaN(str) || str === "") {
                                $(this).val(0);
                                return;
                            }
                            str = isNaN(str) ? 0 : str;
                            str = str.replace(/[^0-9\.]/g, "");
                            str = parseFloat(str).toFixed(2);
                            $(this).val(str);
                        }

                        tbody.find("input[name='" + FIELD_ADD_PLAN_REWARD_RATE + "']").on("focusout", rateFilter);
                        rateFilter.call(tbody.find("input[name='" + FIELD_ADD_PLAN_REWARD_RATE+"']"));


                        //特殊方案概率限制100
                        tbody.find("input[name='" + FIELD_ADD_PLAN_REWARD_RATE + "']").on("focusout", function () {
                            try {
                                var $this = $(this);
                                var $parent = $this.parents("table").first();
                                var $rates = $parent.find("input[name='" + FIELD_ADD_PLAN_REWARD_RATE + "']");
                                var total = 0;
                                $rates.each(function (ind, ele) {
                                    var num = Number(ele.value);
                                    if (num)
                                        total += num;
                                });
                                if (total != 100)
                                    setTooltip(this, "本列概率之和应该等于100", 2000);
                            } catch (e) {
                                console.log("//特殊方案概率限制100出错", e);
                                setTooltip(this, "本列概率之和应该等于100", 2000);
                            }

                        });



                        //概率
                        tbody.find("[name=" + FIELD_ADD_PLAN_REWARD_RATE + "]").val(data)
                    },
                    true
                );

                arr.push(this.createTr({
                    title: "概率配置：",
                    content: [
                        table
                    ],
                }));

                arr.forEach(function(ele){
                    panelBody.append(ele)
                });

                //优先级不可以为空
                var planLevelInput = panelBody.find("input[name="+FIELD_ADD_PLAN_LEVEL+"]");
                var checkPanelLevel = function (){
                    var $this = $(this);
                    var val = $this.val();
                    if(!val || isNaN(val) ){
                        $this.val(1);
                    }
                };
                planLevelInput.unbind("focusout");
                planLevelInput.on("focusout",checkPanelLevel);
                checkPanelLevel.call(planLevelInput);
            }


            //如果有概率方案的数据
            if(readData && readData['specialPlan']){
                try{
                    var planReadData = eval(readData['specialPlan'].trim('"'));
                    planReadData.forEach(function(params){
                        addPlan.call(this,params);
                    },this)
                }catch(e){
                    console.log(e);
                }

            }

            //修改数据提取方式
            this.getFormData = function (form) {
//                var data = serializeDeal({
//                    data: $(form).serializeArray(),
//                    special: {
//                        singleData: ["singleId", "singlePrice", "minCount", "maxCount"]
//                    }
//                });
                var data = serializeDeal({
                    data: $(form).serializeArray(),
                    theList:["rewardList","allowAgent"],
                    special: {
                        missionList: [FIELD_ADD_GAME_ID, FIELD_ADD_GAME_NUM],
                        rewardList: [
                            FIELD_ADD_REWARD_ID,
                            FIELD_ADD_REWARD_PUT,
                            FIELD_ADD_REWARD_RATE,
                            FIELD_ADD_REWARD_SIDE,
                            FIELD_ADD_REWARD_SPECIALONLY,
                            FIELD_ADD_REWARD_BASE_REWARD_COUNT,
                            FIELD_ADD_REWARD_URL
                        ],
                        specialPlan: [
                            FIELD_ADD_PLAN_NEED_TYPE,
                            FIELD_ADD_PLAN_NEED_NUM,
                            FIELD_ADD_PLAN_LEVEL],
                        specialRate: [
                            FIELD_ADD_PLAN_REWARD_ID,
                            FIELD_ADD_PLAN_REWARD_RATE
                        ],
                    }
                });
                if(data["specialRate"]){
                    var i = 0;
                    var plan = data["specialPlan"];
                    var reward = data["rewardList"];
                    data["specialRate"].forEach(function(item, ind, arr){
                        if(! plan[i]["specialRate"]){
                            plan[i]["specialRate"] = [];
                        }
                        plan[i]["specialRate"].push(item);

                        if(plan[i]["specialRate"].length >= reward.length ) {
                            i = i+1 < plan.length ? i+1 : plan.length-1;
                        }
                    });
                    delete data["specialRate"];
                }

                if(data["allowAgent"]){
                    data["allowAgent"] = data["allowAgent"].map(function(item,ind){
                        var obj = {};
                        item.split(";").map(function(d){
                            var key = d.split(",").shift();
                            var val = d.split(",").pop();
                            obj[key] = val;
                        });
                        return obj;
                    });
                }
                console.log(data);
                return data;
            };

            return constor;
        },

    });

    var temp = null;
    function template(tableType,readData) {
        if (!temp){
            temp = new transTable();
        }
        if(tableType){
            temp.tmp(tableType,readData);
        }
        return temp;
    }
    /*
    * 初始化限定工会列表
    * */
    (function(){
        var page = 1;
        function getAgentChildren($target,readData) {
            if (!$target)return;
            console.log("readData",readData);
            var param_ids = [];
            try{
                var param = eval(readData['allowAgent'].trim('"'));
                param_ids = param.map(function(d){return d.allowAgentId});
            }catch(e){
                console.log(e)
            }

            var selfFunc = arguments.callee;
            var url = "{{info.get('agentListUrl')}}";

            function sendData(data,callback) {
                $.ajax({
                    type: "get",
                    url: url,
                    data: data || {list: page},
                    success: callback || function () {
                    }
                })
            }

            function createItemOne(d) {


                var item = $(String.format(
                    "<div class='col-sm-6'>" +
                    "<label class='form-control'>" +
                    '<input type="checkbox" name="allowAgent" ' +
                    'value="{3},{0};{4},{1};{5},{2}" ' +
                    (param_ids.includes(d.parentId) ? "checked " : "" )+
                    ("{{setting.get('readOnly','')}}" === "True" ? "disabled ":"")+
                    '>' +
                    '工会id：{2}' +
//                    '[{0}]代理账号:{1}, 工会id：{2}' +
                    '</label>' +
                    "</div>",
                    d.agentType, d.parentAg, d.parentId,
                    FIELD_ADD_ALLOW_AGENT_TYPE,FIELD_ADD_ALLOW_AGENT_NAME,FIELD_ADD_ALLOW_AGENT_ID
                ));

                return item;
            }

            function createItemTwo(res) {

            }

            sendData("",function (res) {
                var res = typeof res === "string" ? JSON.parse(res) : res;

                if (res['data']) {
                    res['data'].forEach(function (d, ind) {
                        var item = createItemOne(d);
                        $target.append(item);
                    });
                }
            });
        }
        showAgentChildren = getAgentChildren;
    })();

    /*
    *   在当前元素添加提示
    * */
    function setTooltip(target,text,time){
        var $self = $(target);
        $self.tooltip({
            title: text,
        });
        $self.on("show.bs.tooltip", function () {
            setTimeout(function () {
                $self.tooltip('destroy');
            }, time|| 2000);
        });
        $self.tooltip("show");
    }

    /*
    * 初始化选择奖品区域
    * */
    $('#btn_search').click(function () {
        $('#agentTable').bootstrapTable('refresh');
    });
    $("#agentTable").bootstrapTable({
        url: '{{info["listUrl"]}}',
        method: 'get',
        detailView: eval("{{info['showPlus']}}"),//父子表
        //sidePagination: "server",
        pagination: true,
        pageSize: 48,
        sortOrder: 'desc',
        sortName: 'regDate',
        sorttable: true,
        responseHandler: responseFunc,
        queryParams: getSearchP,
        showExport: true,
        exportTypes: ['excel', 'csv', 'pdf', 'json'],
        pageList: [48, 100],
        columns: [
            {
                field: 'op',
                title: '操作',
                align: 'center',
                valign: 'middle',
                formatter: getOp
            },
            {
                field: 'id',
                title: 'ID',
                align: 'center',
                valign: 'middle',
                width:'100',
                sortable: true,
            }, {
                field: 'imgUrl',
                title: '图片',
                width:'100',
                align: 'center',
                valign: 'middle',
                sortable: true,
                formatter: createImg
            }, {
                field: 'title',
                title: '标题',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'priceTotal',
                title: '总价值',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'desc',
                title: '描述',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'note',
                title: '备注',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }],

        //注册加载子表的事件。注意下这里的三个参数！
        onExpandRow: function (index, row, $detail) {
            console.log(index, row, $detail);
            InitSubTable(index, row, $detail);
        }
    });
    //定义列操作
    function getSearchP(p){
      searchId = $("#searchId").val();

      sendParameter = p;

      sendParameter['searchId'] = searchId;

      return sendParameter;
    }


    function responseFunc(res){
        data = res.data;
        count= res.count;
        //实时刷
        $('.count').text(count);

        return data;
    }
    function getOp(value, row, index) {
        var rowobj = row;
        var opList = [];
        var btn = $(String.format(
            "<button class='btn btn-small btn-primary' " +
            "onclick='rewardInsert(this,\"{0}\")'>" +
            "<i class='glyphicon glyphicon-arrow-left'></i>插入" +
            "</button>",
            [
                row[FIELD_REWARD_ID],
                rowobj[FIELD_REWARD_URL],
                rowobj[FIELD_REWARD_TITLE],
                rowobj[FIELD_REWARD_PRICETOTAL],
                rowobj[FIELD_ADD_REWARD_BASE_REWARD_COUNT]
            ].join(",")
            ));
        opList.push(btn.get(0).outerHTML);
        return opList.join("");
    }
    function rewardInsert(self, paramString){
        var $self = $(self);
        var con = template().tableCon;
        var tip = function(text){
            $self.tooltip({
                title: text,
            });
            $self.on("show.bs.tooltip", function () {
                setTimeout(function () {
                    $self.tooltip('destroy');
                }, 1000);
            });
            $self.tooltip("show");
        };

        if(!con || con.length===0){
            tip("未选择活动类型 或 不支持插入奖品");
            return;
        }

        //判断是否已插入
//        var isInsert = Boolean(-1 !== Array.prototype.slice.apply(con.find("[name='"+FIELD_ADD_REWARD_ID+"']").map(function (ind, ele) {
//                return ele.value.toString();
//            })).indexOf(id.toString()));
//        if(isInsert){
//            tip("已经有该奖品了");
//            return
//        }
        template().addReward.apply(
            template(),
            paramString.split(",")
        );
    }
    //创建表格中创建图片
    function createImg(value, row, index) {
        if(!value){return ;}
        var rowobj = JSON.parse(JSON.stringify(row));
        var img = document.createElement("img");
        img.src = value;
        img.height = "100";
        img.alt = rowobj["title"];
        return img.outerHTML;
    }

    /*动态加载选项框组件*/
    $.fn.combobox = function (options, param) {
        if ($(this).get(0).iscombox)
            return;
        else
            $(this).get(0).iscombox = true;

        if (typeof options == "string")
            return $.fn.combobox.methods[options](this, param);
        //合并默认值
        options = $.extend({}, $.fn.combobox.defaults, options || {});

        //清空目标
        var target = $(this);
        target.attr('valuefield', options.valueField);
        target.attr('textfield', options.textField);
        target.empty();

        //添加默认项
        if (options["placeholder"] !== null && options["placeholder"] !== false) {
            var option = $('<option></option>');
            option.attr('value', "");
            option.text(options["placeholder"]);
            target.append(option);
        }

        //判断data参数是否有数据，没有则请求
        if (options.data) {
            init(target, options.data);
        } else {
            options.onBeforeLoad.call(target, options.param);
            if (!options.url) return;
            $.getJSON(options.url, options.param, function (data) {
                init(target, data);
            });
        }
        //
        function init(target, data) {
            if (options.onBuild) {
                //已经执行构建函数，不在执行下面的else
                options.onBuild(target, data, options);
            } else {
                $.each(data, function (i, item) {
                    var option = $('<option></option>');
                    option.attr('value', item[options.valueField]);
                    option.text(item[options.textField]);
                    target.append(option);
                });
            }

            options.onLoadSuccess.call(target);
        }

        target.unbind("change");
        target.on("change", function (e) {
            if (options.onChange)
                return options.onChange(target.val());
        });

    }

    $.fn.combobox.methods = {
        load: function () {

        }
    }
    //默认参数
    $.fn.combobox.defaults = {
        url: null,
        param: null,
        data: null,
        valueField: 'value',
        textField: 'text',
        placeholder: '请选择',
        onBuild: null || function (target, data, options) {
        },
        onBeforeLoad: function (param) {
        },
        onLoadSuccess: function () {
        },
        onChange: function (param) {
        }
    }


</script>
%rebase admin_frame_base