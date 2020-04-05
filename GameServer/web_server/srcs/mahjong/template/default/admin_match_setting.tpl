<div class="cl-mcont">
<div class="block">
          <div class="header">
            <h3>
                %if info.get('title',None):
                    {{info['title']}}
                %end
            </h3>
          </div>
          <form class="form-horizontal group-border-dashed"  style='padding: 19px 29px 29px;' action="{{info.get('submitUrl','')}}" method="POST" id='addMatch' onSubmit='return false'>


            <div class="form-group">
                <label class="col-sm-2 control-label">
                    比赛名称
                </label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" placeholder="填写比赛的名称" name="title" v-model="title" {{"disabled" if setting.get('readonly','') else ""}}>
                </div>
            </div>


              <div class="form-group">
                  <label class="col-sm-2 control-label">比赛类型</label>
                  <div class="col-sm-10">
                      <label class="well">
                          <input type="radio" name="type" value="0"  v-model="type" {{"disabled" if setting.get('readonly','') else ""}}>
                          即开
                          <span class="help-block">报名人数满之后直接开始比赛</span>
                      </label>
                      <label class="well">
                          <input type="radio" name="type" value="1"  v-model="type" {{"disabled" if setting.get('readonly','') else ""}}>
                          定时
                        <span class="help-block">定于某个时间点开始比赛</span>
                      </label>
                  </div>
              </div>


              <div class="form-group" id="matchTime">
                  <label class="col-sm-2 control-label">
                      比赛时间
                      <span class="help-block">只有勾选定时才有效</span>
                  </label>
                  <div class="col-sm-10">
                      <input type="text" class="form-control col-sm-4" name="timeStart" v-model="timeStart" placeholder="第一场比赛的时间 例12:00:00" {{"disabled" if setting.get('readonly','') else ""}}>
                      <input type="text" class="form-control col-sm-4" name="timeEnd" v-model="timeEnd" placeholder="最后一场比赛的时间 例19:00:00" {{"disabled" if setting.get('readonly','') else ""}}>
                      <!--<input type="text" class="form-control col-sm-4" name="timeSpacing" v-model="timeSpacing" placeholder="每场比赛的间隔(s) 例(一小时):3600" {{"disabled" if setting.get('readonly','') else ""}}>-->
                  </div>
              </div>


              <div class="form-group">
                  <label class="col-sm-2 control-label">
                      比赛玩法
                      <span class="help-block">通过选项设置比赛游戏</span>
                  </label>
                  <div class="col-sm-10">
                      <label  class="well col-sm-4">
                          <input type="radio" name="gameid" value="600"  v-model="gameid" {{"disabled" if setting.get('readonly','') else ""}}>
                          二人牛牛
                      </label>
                      <label  class="well col-sm-4">
                          <input type="radio" name="gameid" value="451"  v-model="gameid" {{"disabled" if setting.get('readonly','') else ""}}>
                          二人麻将
                      </label>
                      <label  class="well col-sm-4">
                          <input type="radio" name="gameid" value="460"  v-model="gameid" {{"disabled" if setting.get('readonly','') else ""}}>
                          跑得快
                      </label>
                  </div>
              </div>


              <div class="form-group">
                  <label class="col-sm-2 control-label">
                      报名费用
                      <span class="help-block">选择货币再填写数值</span>
                  </label>
                  <div class="col-sm-5">

                      <label
                          is="item_feetype"
                          v-for="(item, index) in feetypeList"
                          v-bind:field="item.field"
                          v-bind:value="item.value"
                          v-bind:item="item"
                          v-bind:feetype = "feetype"
                      >
                      </label>
                  </div>
                  <div class="col-sm-3">
                      <input type="text"  class="form-control" name="fee" value="" placeholder="数值" v-model="fee" {{"disabled" if setting.get('readonly','') else ""}}>
                                            <p class="help-block">如果留空或者为0，则跳过报名检查</p>

                  </div>
                  <div class="col-sm-2">
                      <input type="text"  class="form-control" name="fee_id" value="" placeholder="道具id" v-model="fee_id" {{"disabled" if setting.get('readonly','') else ""}}>
                      <p class="help-block">如果类型不是道具，麻烦留空</p>
                  </div>

              </div>

              <div class="form-group">
                  <label class="col-sm-2 control-label">
                      入场条件
                  </label>
                  <div class="col-sm-5">

                      <label
                          is="item_threshold_type"
                          v-for="(item, index) in feetypeList"
                          v-bind:field="item.field"
                          v-bind:value="item.value"
                          v-bind:item="item"
                          v-bind:threshold-type = "thresholdType"
                      >
                      </label>
                  </div>
                  <div class="col-sm-3">
                      <input type="text"  class="form-control" name="threshold" value="" placeholder="数值" v-model="threshold" {{"disabled" if setting.get('readonly','') else ""}}>
                      <p class="help-block">如果留空或者为0，则跳过门槛检查</p>
                  </div>

              </div>

              <div class="form-group">
                  <label for="" class="col-sm-2 control-label">
                      免费次数
                      <p class="help-block">每天可以免费参加的次数</p>
                  </label>
                  <div class="col-sm-5">
                      <input type="text" class="form-control" value="" v-model="freeTimes" {{"disabled" if setting.get('readonly','') else ""}}>
                  </div>
              </div>

              <div class="form-group">
                  <label class="col-sm-2 control-label">
                      比赛人数
                      <span class="help-block">选择参赛人数上限</span>
                  </label>
                  <div class="col-sm-10">
                      <label class="well col-sm-2">
                          <input type="radio" name="play_num" value=8  v-model="play_num" {{"disabled" if setting.get('readonly','') else ""}}>
                          8
                      </label>
                      <label class="well col-sm-2">
                          <input type="radio" name="play_num" value=16  v-model="play_num" {{"disabled" if setting.get('readonly','') else ""}}>
                          16
                      </label>
                      <label class="well col-sm-2">
                          <input type="radio" name="play_num" value=32  v-model="play_num" {{"disabled" if setting.get('readonly','') else ""}}>
                          32
                      </label>
                      <label class="well col-sm-2">
                          <input type="radio" name="play_num" value=64  v-model="play_num" {{"disabled" if setting.get('readonly','') else ""}}>
                          64
                      </label>
                      <label class="well col-sm-2">
                          <input type="radio" name="play_num" value=128  v-model="play_num" {{"disabled" if setting.get('readonly','') else ""}}>
                          128
                      </label>
                      <label class="well col-sm-2">
                          <input type="radio" name="play_num" value=256  v-model="play_num" {{"disabled" if setting.get('readonly','') else ""}}>
                          256
                      </label>
                      <label  class="well col-sm-2">
                          <input type="radio" name="play_num" value=512  v-model="play_num" {{"disabled" if setting.get('readonly','') else ""}}>
                          512
                      </label>
                      <label  class="well col-sm-2">
                          <input type="radio" name="play_num" value=9  v-model="play_num" {{"disabled" if setting.get('readonly','') else ""}}>
                          9
                      </label>
                  </div>
              </div>

              <div class="form-group">
                  <label class="col-sm-2 control-label">
                      人数下限
                      <span class="help-block">选择参赛人数下限</span>
                  </label>
                  <div class="col-sm-10">
                      <input type="text" class="form-control"  value="" v-model="play_num_lower" {{"disabled" if setting.get('readonly','') else ""}}>
                  </div>
              </div>

              <div class="form-group">
                  <label class="col-sm-2 control-label">
                      比赛赛制
                      <span class="help-block">设置比赛的模式</span>
                  </label>
                  <div class="col-sm-10">
                      <label class="well col-sm-6">
                          <input type="radio" name="rule_type" value="0" v-model="rule_type" {{"disabled" if setting.get('readonly','') else ""}}>
                          淘汰制
                      </label>
                  </div>
              </div>

              <div class="form-group">
                  <label class="col-sm-2 control-label">
                      赛事底分
                  </label>
                  <div class="col-sm-10">
                      <input type="text" value=0 class="form-control" v-model="baseScore"  {{"disabled" if setting.get('readonly','') else ""}}>
                  </div>
              </div>

              <div class="form-group">
                  <label class="col-sm-2 control-label">
                      详情-比赛奖励
                      <span class="help-block">填写比赛的名次跟奖励,将会显示在前端</span>
                      %if not setting.get('readonly',''):
                      <button type="button" class="btn btn-md btn-primary" v-on:click="addReward()" >增加</button>
                      %end
                  </label>
                  <div class="col-sm-10 well" id="rewardList">

                      <div
                        is="item_reward"
                        v-for="(item, index) in rewardList"
                        v-bind:key = "item.id"
                        v-bind:id = "item.id"
                        v-bind:ids = "item.ids"
                        v-bind:field = "item.field"
                        v-bind:value = "item.value"
                        v-bind:propID = "item.propID"
                        v-bind:type = "item.type"
                        v-bind:locked = "item.locked"
                        v-bind:item = "item"
                        v-bind:reward-type-list = "rewardTypeList"
                        v-on:remove="rewardList.splice(index, 1)"
                      ></div>

                  </div>
              </div>
              <div class="form-group">
                  <label class="col-sm-2 control-label">
                      详情-规则
                      <span class="help-block">将会显示在前端(换行用\n)</span>
                  </label>
                  <div class="col-sm-10" >
                      <textarea name="rule" cols="30" rows="10" class="form-control" v-model="rule" {{"disabled" if setting.get('readonly','') else ""}}></textarea>
                  </div>
              </div>
              <div class="form-group">
                  <label class="col-sm-2 control-label">
                      详情-概况
                      <span class="help-block">将会显示在前端</span>
                      % if not setting.get('readonly',''):
                    <button type="button" class="btn btn-md btn-primary" v-on:click="addGeneral()">增加</button>
                      %end

                  </label>
                  <div class="col-sm-10 well" id="conGeneral" >
                    <div
                        is="item_general"
                          v-for="(item, index) in general"
                          v-bind:key="item.id"
                          v-bind:field="item.field"
                          v-bind:value="item.value"
                          v-bind:item="item"
                          v-on:remove="general.splice(index, 1)">
                  </div>
                      <!--v-on:/click="delReward({{'{{item}}'}})"-->
                  </div>
              <div class='col-sm-12'>
                  % if not setting.get('readonly',''):
                 <p align='center'><input type='button' value='确定' v-on:click="send" class='btn btn-md btn-primary' /></p>
                  %end
            </div>
          </form>

  </div>
</div>
<script type="text/javascript">

    //报名条件货币类型组件
    Vue.component('item_feetype',{
        template:'<label  class=" well col-sm-4">\
                      <input type="radio" name="feetype" :value="item.value"  v-model="feetype" {{"disabled" if setting.get("readonly","") else ""}}>\
                      {{"{{item.field}}"}}\
                  </label>\
                  ',
        props:['field', 'value', 'item', 'feetype'],
        watch: {
            feetype: function(value){
                app.feetype = value;
            },
        }
    });
    //门槛货币类型组件
    Vue.component('item_threshold_type',{
        template:'<label  class=" well col-sm-4">\
                      <input type="radio" name="thresholdType" :value="item.value"  v-model="thresholdType" {{"disabled" if setting.get("readonly","") else ""}}>\
                      {{"{{item.field}}"}}\
                  </label>\
                  ',
        props:['field', 'value', 'item', 'thresholdType'],
        watch: {
            thresholdType: function(value){
                app.thresholdType = value;
            },
        }
    });


    //详情-概况组件
    Vue.component('item_general',{
        template:'<div class="col-sm-12">\
              <label class="col-sm-3">\
                  <input type="text" placeholder="字段" v-model="item.field" name="general-field"\
                         class="form-control" {{"disabled" if setting.get("readonly","") else ""}}>\
              </label>\
              <span class="col-sm-1">:</span>\
              <label class="col-sm-3">\
                  <input type="text" placeholder="值" v-model="item.value" name="general-value"\
                         class="form-control" {{"disabled" if setting.get("readonly","") else ""}}>\
              </label>\
              <span class="col-sm-1">\
                    % if not setting.get("readonly",""):
                  <button type="button" class="btn btn-md btn-danger"  v-on:click="$emit(\'remove\') " >删除</button>\
                    % end
              </span>\
          </div>\
        ',
        props: ['field', 'value', 'item'],
        method: {
            _value:function(){
//                this.item['value'] =
            }
        }
    });
    //比赛奖励组件
    Vue.component('item_reward',{
        template:'<div class="col-sm-12">\
                          <div class="col-sm-2">\
                              <label class="control-label col-sm-3">名次</label>\
                              <div class="col-sm-9">\
                                  <input type="text" class="form-control" :value="item.ids" :disabled = "item.locked" {{"disabled" if setting.get("readonly","") else ""}}>\
                              </div>\
                          </div>\
                          <div class="col-sm-2">\
                              <label class="control-label col-sm-3">称谓</label>\
                              <div class="col-sm-9">\
                                  <input type="text" class="form-control" :value="item.field" {{"disabled" if setting.get("readonly","") else ""}}>\
                              </div>\
                          </div>\
                          <div class="col-sm-2">\
                              <label class="control-label col-sm-3">类型</label>\
                              <div class="col-sm-9">\
                                  <select class = "form-control" v-model = "item.type" {{"disabled" if setting.get("readonly","") else ""}}>\
                                    <option v-for="option in rewardTypeList" v-bind:value = "option.value">\
                                     {{"{{option.field}}"}}\
                                    </option>\
                                  </select>\
                              </div>\
                          </div>\
                          <div class="col-sm-3">\
                              <label class="control-label col-sm-3">数值</label>\
                              <div class="col-sm-9">\
                                  <input type="text" class="form-control" v-model="item.value" {{"disabled" if setting.get("readonly","") else ""}}>\
                              </div>\
                          </div>\
                          \<div class="col-sm-2">\
                              <label class="control-label col-sm-3">道具ID</label>\
                              <div class="col-sm-9">\
                                  <input type="text" class="form-control" v-model="item.propID" {{"disabled" if setting.get("readonly","") else ""}}>\
                              </div>\
                          </div>\
                          <div class="col-sm-1">\
                                % if not setting.get("readonly",""):
                              <button type="button" class="btn btn-md btn-danger" v-if="!item.unDel"  v-on:click="$emit(\'remove\') " >删除</button>\
                                % end
                          </div>\
                      </div>',
        props:['ids', 'field', 'value', 'type', 'locked', 'item', 'rewardTypeList'],
        watch: {
            value: function(newValue){
                    console.log(arguments,this)
            },
          }
    })

    function initApp(data) {
        var haveData = Boolean(data);
        data = data || {
            type: '0', //比赛类型 0即开 1定时
            title: '',
            timeStart: '',
            timeEnd: '',
            timeSpacing: '',
            feetype: 'gold', //报名货币 gold/roomCard/yuanbao
            fee: '',
            fee_id:'', //报名道具id
            limit:'',
            play_num: 8,//参赛人数上限
            play_num_lower: 0,//参赛人数下限
            general: [],
            rewardList: [],
            rule: '',
            gameid: '600',
            rule_type: 0, //比赛制式： 0淘汰制
            freeTimes: 3 , //免费次数
            threshold: 0, //入场门槛
            thresholdType: 'gold', //入场门槛货币类型

            //未显示字段
            openStart: '', //开放日期
            openEnd: '', //结束日期
            waitTime: '',//等待时间
            status: '',//比赛状态
            num: '',
            baseScore: 50,
        };
        //旧版没有字段,没有就加上去
        var extendField = {
            freeTimes: 3 , //免费次数
            threshold: 0 , //入场门槛
            thresholdType: 'gold',
            fee_id: '',
            play_num_lower: 0,
        };
        if(haveData){
            for (var key in extendField){
                if(!(key in data)){
                    data[key] = extendField[key];
                }
            }
        }
        //不提交字段
        var newField = {
            general_index : 0,
            reward_index : 0,
            feetypeList:[],
            rewardTypeList:[],
        };

        if(haveData){
            newField['general_index'] = data['general'].length;
            newField['reward_index'] = data['rewardList'].length;
        }

        data = $.extend(data,newField );

        app = new Vue({
        el : '#addMatch',
        data: data,
        created: function(){
            $("#matchTime").hide();
            //初始化报名货币类型
            var feetypeList = JSON.parse('{{!setting.get("feetypeList","")}}');
            Object.keys(feetypeList).map(function(key){
                var value = feetypeList[key];
                var tem = {'field': value, 'value': key};
                this.feetypeList.push(tem);
            }.bind(this));
            //奖励类型
            var rewardTypeList = JSON.parse('{{!setting.get("rewardTypeList","")}}');
            Object.keys(rewardTypeList).map(function(key){
                var value = rewardTypeList[key];
                var tem = {'field': value, 'value': key};
                this.rewardTypeList.push(tem);
            }.bind(this));

            //没有数据则执行数据初始化
            if(!haveData){
                //初始化general
                var default_general = [
                    {field: '赛事名称', value: ''},
                    {field: '玩家基数', value: ''},
                    {field: '游戏名', value: ''},
                    {field: '开启周期', value: ''},
                    {field: '赛事玩法', value: ''}
                ];
                default_general.forEach(function(item){
                    this.addGeneral(item)
                },this);
                //初始化reward
                 [0, 1, 2].forEach(function () {
                     this.addReward();
                 }, this)
             }

            //有没有数据都执行
             this.checkType();
        },
        watch:{
            type: function () {
                this.checkType();
            },

            general: function(){
//                console.log(arguments);

                $('#conGeneral');
            }
        },
        methods:{
            send: function(){
//                console.log(this._data);
                //不提交字段
                var not_subbmit = ['general_index', 'reward_index'];

                //不为空字段
                var notEmpty = {
                    1: ['title', 'feetype', 'fee', 'play_num', 'gameid', 'rule_type', 'rewardList', 'general'],
                    2: ['field', 'value', 'ids', 'type']
                };

                //资料为空
                function errEmpty(key){
                    alert(String.format('{0} 为空，请填写', key));
                    return false
                }


                //进行检查
                function checkList(obj, level, parent) {
                    var data = {};
                    var parent = parent ? parent+"," : '';
                    var _k = Object.keys(obj);
                    var i = _k.length;
                    while (i--){
                        var key = _k[i];
                        //检查不提交
                        if(level === 1)
                            if (not_subbmit.indexOf(key) !== -1)continue;

                        //检查是否为空
                        var value = obj[key];
                        var currCheck = level; //采用1级notEmpty
                        var emptyRule = notEmpty[currCheck];
                        var isCheck = emptyRule ? emptyRule.indexOf(key) !== -1: false;
                        if( isCheck && (value === '' || value == null) ){
                            return errEmpty(parent + key);
                        }

                        //检查子元素
                        if (value instanceof Array){
                            if(isCheck && !value[0]){
                                return errEmpty(parent + key);
                            }
                            for (var j = 0 ; j < value.length; j++){
                                var child = value[j];
                                if(typeof (child) == 'object'){
                                    var result = checkList(child, currCheck+1, key);
                                    if(!result){
                                        return result;
                                    }
                                }
                            }
                        }
                        data[key] = value;
                    }
                    return data;
                }

                var _d = this._data;
                var currCheck = 1;
                var result = checkList(_d, currCheck);
                console.log('result', result);
                if(result){
                    jsonAjax($('#addMatch').attr("action"), $('#addMatch').attr("method"), JSON.stringify(result),'正在创建...');
                }

            },

            checkType: function(){
                $("#matchTime").toggle(this.type == 1)
            },

            addReward: function(){
                var idx = this.reward_index ++ ;
                var tmpd = [
                    {ids:'[1]', field: '冠军', value: '2', type:'redpacket'},
                    {ids:'[2]', field: '亚军', value: '10000', type:'gold'},
                    {ids:'[3]', field: '季军', value: '8000', type:'gold'},
                    {ids:'[4]', field: '第4名', value: '6000', type:'gold'},
                    {ids:'[5, 8]', field: '第5-8名', value: '4000', type:'gold'},
                    {ids:'[9, 16]', field: '第9-16名', value: '2000', type:'gold'},
                    {ids:'[17, 32]', field: '第17-32名', value: '1000', type:'gold'}
                ];
                var tmpdef = {ids:'[17, 32]', field: '第17-32名', value: '1000', type:'gold'};
                var tmp = tmpd[idx] || tmpdef;
                tmp.id = idx;
                tmp.locked = idx < 4;
                tmp.unDel = idx < 1;
                this.rewardList.push(tmp);
            },


            addGeneral: function(params){
                var tmpd = params || {field: '', value: ''};
                tmpd.id  = this.general_index++;
                this.general.push(tmpd);
            },

        }

    })
    }

    var tableUrl = "{{setting.get('tableUrl','') if setting.get('tableUrl','') else ''}}";
    if(tableUrl ){
        $.ajax({
            url: tableUrl,
            type: "{{setting.get('tableMethod','')}}",
            success: function(res){
                if(res.code == 0){
                    initApp(res.data);
                }else{
                    alert(res.msg);
                }
            }
        })
    }else{
        initApp();
    }
</script>
%rebase admin_frame_base