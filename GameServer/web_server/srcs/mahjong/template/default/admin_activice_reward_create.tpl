% setdefault('setting',{})
% setdefault('data',setting.get('data') or {})
% setdefault('readOnly',setting.get('readOnly') or False)
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
            <div class="col-sm-8">
                <form class='form-horizontal group-border-dashed' action="{{info['submitUrl']}}" method='POST'
                      id='broadcastForm' onSubmit='return false' >
                    <table class='table config-table'>
                        <tr>
                            <td class='table-title min_base_txt'>选择图片:</td>
                            <td>
                                <input type="text" class="hide form-control"  name="imgId">
                                <div class="panel panel-default">
                                    <div class="panel-body" id="imgSelector" style="max-height: 150px;overflow:auto;">

                                    </div>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td class='table-title min_base_txt'>标题:</td>
                            <td>
                                <div class="col-sm-12">
                                    %if readOnly :
                                        {{data.get('title','')}}
                                    %else:
                                        <input type='text' style='width:100%;float:left' name='title' class="form-control"
                                            value = "{{data.get('title','')}}">
                                    %end
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td class='table-title min_base_txt'>描述:(客户端中可见)</td>
                            <td>
                                <div class="col-sm-12">
                                    %if readOnly :
                                        {{data.get('desc','')}}
                                    %else:
                                        <input type='text' style='width:100%;float:left' name='desc' class="form-control"
                                        value="{{data.get('desc',' ')}}">
                                    %end
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td class='table-title min_base_txt'>备注:</td>
                            <td>
                                <div class="col-sm-12">
                                    %if readOnly :
                                        {{data.get('note','')}}
                                    %else:
                                        <input type='text' style='width:100%;float:left' name='note' class="form-control"
                                        value="{{data.get('note',' ')}}">
                                    %end
                                </div>
                            </td>
                        </tr>
                        <tr id="priceTotal">
                            <td class='table-title min_base_txt'>总价值:<br/>
                                <span class="text-muted">如果是礼包，开出的奖品价值之和不会大于该值</span>
                            </td>
                            <td>
                                <div class='col-sm-12'>
                                    %if readOnly :
                                        {{data.get('priceTotal','')}}
                                    %else:
                                        <input type='text' style='width:100%;float:left' name='priceTotal' class="form-control"
                                        value="{{data.get('priceTotal',' ')}}">
                                    %end
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td class='table-title min_base_txt'>
                                奖品/道具属性:<br>
                                <span class="text-muted">更改属性，将会重置下面资料</span>
                            </td>
                            <td id="type_message">
                                %if setting.get('typeList'):
                                    %for item in  setting.get('typeList',[]):
                                        <div class="col-sm-2">
                                            <label class="form-control" onclick="initPropAttr('{{item['type']}}')">
                                                <input type='radio' name="type"  value="{{item['value']}}" form-type="{{item['type']}}">
                                                {{item['name']}}
                                            </label>
                                        </div>
                                    %end
                                %end

                            </td>
                        </tr>
                        <tr id="baseRewardCount">
                            <td class='table-title min_base_txt'>基础奖品发放数量:<br/>
                            </td>
                            <td>
                                <div class='col-sm-2'>
                                    %if readOnly :
                                        {{data.get('note','')}}
                                    %else:
                                    <input type='number' style='width:100%;float:left' name='baseRewardCount'
                                        class='form-control' placeholder="(单位个，例：1)" value="{{data.get('baseRewardCount','1')}}">
                                    %end

                                </div>
                            </td>
                        </tr>
                        <tr id="recordCon" style="display:none">
                            <td class='table-title min_base_txt'>是否需要记录获奖人信息:</td>
                            <td id="isRecord_message">

                            </td>
                        </tr>
                        <tr id="packConfig" style="display:none">
                            <td class='table-title min_base_txt'>礼包内奖品配置:</td>
                            <td>
                                <span class='text-muted'>点击右侧插入，添加对应奖品</span>
                                <table class="table table-bordered table-condensed table-hover">
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>图片</th>
                                            <th>奖品名</th>
                                            <th>单品价值</th>
                                            <th>最少发放(个)</th>
                                            <th>最多发放(个)</th>
                                        </tr>
                                    </thead>
                                    <tbody>

                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </table>

                    <div class="modal-footer" style="text-align:center">
                        <button type="submit" class="btn btn-sm btn-xs btn-primary btn-mobile">
                            %if info.get("submitText"):
                            {{info["submitText"]}}
                            %else :
                            提交
                            %end
                        </button>
                        <button type="button" class="btn btn-sm btn-xs btn-primary btn-mobile" name="backid"
                                id="backid">
                            返回
                        </button>
                    </div>
                </form>
            </div>
            <div class="col-sm-4" id="rewardList" style="display:none">
                %include search
                <table id="agentTable" class="table table-bordered table-hover" ></table>
            </div>
        </div>
    </div>
</div>

<script src="https://cdn.bootcss.com/bootstrap/3.2.0/js/tooltip.min.js"></script>
<script type="text/javascript">
    $('#broadcastForm').submit(function(){
        var data = serializeDeal({
                    data:$(this).serializeArray(),
                    special:{
                        singleData:[
                            "singleId",
                            "singleImg",
                            "singleName",
                            "singlePrice",
                            "minCount",
                            "maxCount"]
                    }
                });
        console.log(data);
        jsonAjax($(this).attr("action"), $(this).attr("method"), JSON.stringify(data),'正在提交...');
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

    $('#backid').click(function(){
            window.location.href="{{info['backUrl']}}";
       });
    var FIELD_ADD_IMG_ID    = "imgId",
        FIELD_ADD_BASE_REWARD_COUNT      = "baseRewardCount",
        FIELD_ADD_TYPE      = "type",
        FIELD_ADD_TITLE     = "title",
        FIELD_ADD_DESC      = "desc",
        FIELD_ADD_PRICETOTAL= "priceTotal",
        FIELD_ADD_NOTE      = "note",
        FIELD_ADD_REWARD_ID = "rewardId",
        FIELD_IMG_ID        = "id",
        FIELD_IMG_URL       = "url",
        FIELD_IMG_TITLE     = "title",
        FIELD_IMG_NOTE      = "note",
        FIELD_REWARD_ID     = "id",
        FIELD_REWARD_TITLE     = "title",
        FIELD_REWARD_PRICETOTAL = "priceTotal",
        FIELD_REWARD_NOTE   = "note",
        FIELD_REWARD_URL    = "imgUrl"
        ;

    $(document).ready(function(){
        //尝试获取readdata
        try{
            var div = document.createElement("div");
            div.innerHTML = "{{setting.get('dataString','')}}";
            var propData = JSON.parse(div.innerHTML.replace(/\su\'/g,"'").replace(/{u\'/g,"{'"));
        }catch(e){
            console.log(e)
        }
        //尝试获取图片id
        var imgId = "{{data.get('imgId','')}}";
        init_imgSelector(imgId);

        if(propData){
            //尝试获取道具属性
            var typeValue = "{{data.get('type','')}}";
            if(typeValue){
                var $input = $("input[type='radio'][value='"+typeValue+"']");
                $input.get(0).checked = true;
                initPropAttr($input.attr("form-type"),propData ? propData : "")
            }

            //尝试获取包含单品信息
            try{
                var singleData = eval(propData['singleData'].trim('"'));
                singleData.forEach(function(ele){
                    rewardInsert("",ele);
                })
            }catch (e){
                console.log(e);
            }
        }

    })
    /*
    * 表单验证
    * */
    var formConfig = {
            feedbackIcons:{
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            message:'不能为空',
            excluded:[],
            fields:{
                title:{
                    validators: {
                        notEmpty: {
                            message:"标题不能为空"
                        },
                    },
                },
                imgId:{
                    container:"#imgSelector",
                    validators: {
                        notEmpty: {
                            message:"请选择一张图片"
                        }
                    },
                },
                type:{
                    container:"#type_message",
                    validators: {
                        notEmpty: {
                            message:"请选择是否礼包"
                        }
                    }
                },
                isRecord:{
                    container:"#isRecord_message",
                    validators: {
                        notEmpty: {
                            message:"请选择是否记录获奖人信息"
                        }
                    }
                },
                priceTotal:{
                    validators: {
                        notEmpty: {
                            message:"不能为空"
                        }
                    }
                },
                singleId:{
                    validators: {
                        notEmpty: {
                            message: "不能为空"
                        }
                    }
                },
                singlePrice:{
                    validators: {
                        notEmpty: {
                            message: "不能为空"
                        }
                    }
                },
            }
        };
//    $("#agentCreate").bootstrapValidator($.extend(true,{},formConfig));
    /*
    * 初始化图片选择区域
    * */
    function init_imgSelector(defaultId){

        var selector = $("#imgSelector");
        var url = "{{info['imgListUrl']}}";
        $.get(url,function(ret){
            var ret = typeof ret =="string" ? JSON.parse(ret) : ret;
            var data = ret['data'];
            //URL记录
            $input = $("<input name='imgUrl' value='' class='hide'>");
            selector.append($input);

            for (var i = 0, len = data.length; i < len ; i++){
                //新建图片对象并插入
                var dataObj = data[i];
                var img = $(String.format(
                    "<div class='col-sm-1' style='cursor:pointer;'" +
                        "data-toggle='tooltip' title='{1}:{2}'>"  +
                        "<img src='{0}' alt='{1}:{2}'  " +
                        "class='img-thumbnail' style='height: 60px'/>" +
                    "</div>",
                    dataObj[FIELD_IMG_URL],
                    dataObj[FIELD_IMG_TITLE],
                    dataObj[FIELD_IMG_NOTE]
                ));
                selector.append(img);

                //初始化提示框
                img.tooltip();
                //点击事件
                var selectedCon = $("<i class='glyphicon glyphicon-ok text-success' style='position:absolute;left:0'></i>");
                (function(){
                    var imgId = dataObj[FIELD_IMG_ID];
                    var imgUrl = dataObj[FIELD_IMG_URL];
                    img.on("click",function(){
                        //重置imgId的表单验证
//                        $("#agentCreate").data("bootstrapValidator").updateStatus("imgId",  "NOT_VALIDATED",  null );
                        $("input[name="+FIELD_ADD_IMG_ID+"]").val(imgId);
                        $input.val(imgUrl);
                        $(this).append(selectedCon);
                        imgOnClick.call(this,imgId);
                    })
                    if(defaultId && imgId == defaultId){
                        img.click();
                    }
                })()
            }
        });
    }
    function imgOnClick(){
        var $self = $(this);
        $self.siblings().each(function(ind,ele){
            $(ele).find("img").removeClass("alert-success");
        });
        $self.find("img").addClass("alert-success");
    }
    /*
    * 初始化礼包选择区域
    * */
    function initPropAttr(type, params) {
        params = params || {};
            var con1 = $("#recordCon"),
                con2 = $("#packConfig"),
                input = $("input[name='baseRewardCount']"),
                rewardList = $("#rewardList");

            input.removeAttr("readonly");

            //是实物
            if (type == "normal") {

                rewardList.hide();

                con2.find("> td:last-child tbody").empty();
                con2.hide();

                var str = "<div class='col-sm-2'>" +
                    "<label class='form-control'>" +
                    "<input type='radio' name='isRecord'  value='{0}' {2} {3}>{1}" +
                    "</label></div>";
                var htmlStr =
                    String.format(str, "1", "是",params['isRecord'] == 1 ? "checked" : "") +
                    String.format(str, "0", "否",params['isRecord'] != 1 ? "checked" : "");
                con1.find("> td:last-child").html(htmlStr);
                con1.show();
            }
            //是礼包
            if (type == "pack") {
                //显示右侧奖品列表
                rewardList.show();

                //禁止修改数量  重置发放数量
                input.val(1);
                input.attr("readonly",true);


                //清空不是礼包的时候写的数据
                con1.find("> td:last-child").empty();
                con1.hide();


                //显示是礼包需要填写的数据
                con2.find("> td:last-child tbody").empty();
                con2.show();
            }
            //是金币、钻石、抽奖券、不中奖
            if(type == "prop"){

                rewardList.hide();

                con1.find("> td:last-child").empty();
                con1.hide();

                con2.find("> td:last-child tbody").empty();
                con2.hide();
            }
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
        var param = {
            [FIELD_REWARD_ID]       :   row[FIELD_REWARD_ID],
            [FIELD_REWARD_URL]      :   rowobj[FIELD_REWARD_URL],
            [FIELD_REWARD_TITLE]    :   rowobj[FIELD_REWARD_TITLE],
            [FIELD_REWARD_PRICETOTAL]:  rowobj[FIELD_REWARD_PRICETOTAL],
        };
        param = encodeURI(JSON.stringify(param));
        var btn = $(String.format(
            "<button class='btn btn-small btn-primary' onclick='rewardInsert(this,\"{0}\")'>" +
            "<i class='glyphicon glyphicon-arrow-left'></i>插入" +
            "</button>",
            param
            ));
        opList.push(btn.get(0).outerHTML);
        return opList.join("");
    }
    function rewardInsert(self, param){
//        id, imgUrl, title
        var param = typeof param === "string" ? JSON.parse(decodeURI(param)) : param;
        var id      = param[FIELD_REWARD_ID] || param['singleId'],
            imgUrl  = param[FIELD_REWARD_URL] || param['singleImg'],
            title  = param[FIELD_REWARD_TITLE] || param['singleName'],
            priceTotal  = param[FIELD_REWARD_PRICETOTAL] || param['singlePrice'],
            minCount  = param['minCount'] || "",
            maxCount  = param['maxCount'] || ""
            ;
        //如果不是礼包，则拒绝
        if(!$("input[name='type'][value='pack']").get(0).checked){
            return;
        }

        var con = $("#packConfig > td:last");

        if(self){
            //判断是否已插入
            var isInsert = Boolean(-1 !== Array.prototype.slice.apply(con.find("[name='singleId']").map(function(ind,ele){
                return ele.value.toString();
            })).indexOf(id.toString()));
            if(isInsert){
                var $self = $(self);
                $self.tooltip({
                    title:"已经在奖品列表中",
                });
                $self.on("show.bs.tooltip",function(){
                    setTimeout(function(){
                        $self.tooltip('destroy');
                    },1000);
                });
                $self.tooltip("show");
                return
            }
        }

        //插入一条奖品信息
        /*<tr>
            <th>ID</th>
            <th>图片</th>
            <th>奖品名</th>
            <th>单品价值</th>
            <th>最少发放(个)</th>
            <th>最多发放(个)</th>
        </tr>*/
        var tr = $(String.format(
            "<tr><td style='width: 100px'><div class='col-sm-12'><input type='number' name='singleId' value='{0}' class='form-control' readonly='readonly'></div></td>" +
            "<td><input type='text' class='hide' name='singleImg' value='{1}'><img src='{1}' alt='{0}:{2}' width='60px'></td>" +
            "<td style='width: 60px'><input type='text' name='singleName' class='hide' value='{2}'>{2}</td>" +
            "<td><div class='col-sm-12'><input type='number' name='singlePrice' class='form-control hide' value='{3}' >{3}</div></td>" +
            "<td><div class='col-sm-12'><input type='number' name='minCount' class='form-control' value='{4}'></div></td>" +
            "<td><div class='col-sm-12'><input type='number' name='maxCount' class='form-control' value='{5}'></div></td>" +
            "<td><div class='col-sm-12'><button type='button' class='btn btn-danger del'>删除</button></div></td>" +
            "</tr>",
            id, imgUrl, title, priceTotal, minCount, maxCount
        ));
        tr.find("button.del").on("click",function(){
            tr.remove()
        })
        con.find("tbody").append(tr);
    }
    //创建图片
    function createImg(value, row, index) {
        if(!value){return ;}
        var rowobj = JSON.parse(JSON.stringify(row));
        var img = document.createElement("img");
        img.src = value;
        img.height = "100";
        img.alt = rowobj["title"];
        return img.outerHTML;
    }

</script>
%rebase admin_frame_base