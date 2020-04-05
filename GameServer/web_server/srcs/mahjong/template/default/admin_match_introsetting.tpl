<div class="block">
          <div class="header">                          
            <h3>
                %if info.get('title',None):
                    {{info['title']}}
                %end
            </h3>
          </div>
          <div class="content">
              <form class=" form-horizontal group-border-dashed" id='data_form'>
                  <!-- 操作按钮 -->
                 <div class="form-group">
                     <label class="col-sm-3 control-label">
                        {{lang.GAME_INTRO_TITLE}}<br/>
                        <small>{{lang.GAME_INTRO_TXT}}</small>
                    </label>
                     <div class="btn-group">
                         <button type="button" class="btn btn-primary app_create_biaoti">新增标题</button>
                         <button type="button" class="btn btn-primary app_create_hang">新增行</button>
                         <button type="button" class="btn btn-primary " id="app_copy">复制数据</button>
                         <button type="button" class="btn btn-primary app_create_from_copy">粘贴数据</button>
                         <button type="button" class="btn btn-danger app_clear">清空</button>

                     </div>
                 </div>
                 <!-- End操作按钮 -->
                 <div id="f_content"></div>
              </form>
             <form class="form-horizontal group-border-dashed" id='introForm' onSubmit="return false;" action="{{info['submitUrl']}}" method="post" style="border-radius: 0px;">
              <input type="hidden" name="gameId" value="{{info['gameId']}}" />
              <input type="hidden" name="matchId" value="{{info['matchId']}}" />
             <div class="form-group hide">
               <label class="col-sm-3 control-label">
                    {{lang.GAME_INTRO_TITLE}}<br/>
                    <small>{{lang.GAME_INTRO_TXT}}</small>
                </label>
                <div class="col-sm-8">
                    <textarea style="width:100%;height:650px;float:left"  name='content' class="form-control" id="some-textarea">{{ info.get('gameDesc') }}</textarea>
                </div>
              </div>
              <div class="modal-footer" style="text-align:center">
                   <button type="submit" class="btn btn-sm btn-primary">确认</button>
                   <button type="button" class="btn btn-sm btn-primary" id='backid'>{{lang.BTN_BACK_TXT}}</button>
              </div>
            </form>
          </div>
        <div class="hide">
            <div class="form-group item-group" id="template_biaoti">
                <label class="col-sm-3 control-label">
                        标题
                </label>
                <div class="col-sm-8 input-group">
                    <input name="item_content" type="text"  >
                    <button type="button" class="btn btn-primary app_up" >↑</button>
                    <button type="button" class="btn btn-primary app_down" >↓</button>
                    <button class="btn btn-danger app_remove" >移除</button>
                </div>
            </div>

            <div class="form-group item-group" id="template_hang">
                <label class="col-sm-3 control-label">
                        子规则
                </label>
                <div class="col-sm-8 input-group">
                    <input name="item_content" type="text"  >
                    <button type="button" class="btn btn-primary app_up" >↑</button>
                    <button type="button" class="btn btn-primary app_down" >↓</button>
                    <button type="button" class="btn btn-danger app_remove" >移除</button>
                    <textarea class="form-control" name="item_content" type="text" ></textarea>
                </div>
            </div>
        </div>
</div>
<script type="text/javascript">
  $(function(){

       $('#introForm').submit(function(){
           //数据处理
           var data = app.createJson($('#data_form').serializeArray());
            $('#some-textarea').val(JSON.stringify(data));

            formAjax($(this).attr("action"), $(this).attr("method"), $(this).serialize(),'正在生成规则模板...');
       });

       $('#backid').click(function(){
              window.location.href="{{info['backUrl']}}";
       });
        //-------------------构造app
        var app=(function(){
            var enum_type = {
                title:1,    //标题
                key:2,      //小标题
                content:3,  //内容
            }
            var _app = function(){

            };
            //内置id
            _app.prototype._id = 0;
            _app.prototype.get_insert_id = function(){
                return this._id++;
            }

            //在锚点下插入元素
            var f_content = $("#f_content");
            _app.prototype.insert = function(dom){
                f_content.before(dom);
            };

            //删除当前行
            _app.prototype.removeLine = function(item){
                $(item).parents('.item-group').remove();
            };

            //删除所有行
            var form = $('#data_form');
            _app.prototype.clearLine = function(){
                form.find('.item-group').remove();
            }

            //上移一行
            _app.prototype.pushUp = function(item){
                var p = $(item).parents('.item-group');
                var t = p.prev('.item-group');
                if(t){
                    t.before(p);
                }
            }

            //下移一行
            _app.prototype.pushDown = function(item){
                var p = $(item).parents('.item-group');
                var t = p.next('.item-group');
                if(t){
                    t.after(p);
                }
            }

            //创建包含信息的名字
            _app.prototype.encode_name = function(name, id, type){
                return name + '@' + id + '@' + type;
            }

            //解析名字信息
            _app.prototype.decode_name = function(name){
                var args = name.split('@');
                return {
                    name:args[0],
                    id: args[1],
                    type:args[2]
                }
            }

            //创建一个标题
            var template_biaoti = $("#template_biaoti");
            _app.prototype.create_biaoti = function(data){
                console.log(this);
                var id = this.get_insert_id();
                var res = $(template_biaoti.get(0).outerHTML);
                res.removeAttr('id');

                var com = res.find('[name=item_content]');
                com.prop("name", this.encode_name('item_content', id, enum_type.title));

                if(data){
                    com.prop("value",data[0].content);
                }

                this.insert(res);
                return res;
            };

            //创建行
            var template_hang = $("#template_hang");
            _app.prototype.create_hang = function(data){
                var id = this.get_insert_id();
                var res = $(template_hang.get(0).outerHTML);
                res.removeAttr('id');

                var com = res.find('[name=item_content]');
                com.eq(0).prop("name", this.encode_name('item_content', id, enum_type.key));
                com.eq(1).prop("name", this.encode_name('item_content', id, enum_type.content));

                if(data){
                    com.eq(0).prop("value", data[0].content);
                    com.eq(1).prop("value", data[1].content);
                }
                this.insert(res);
                return res;
            };

            //根据数据恢复dom
            _app.prototype.createDomByData = function(data){
                if(!data)return;
                var json = data;
                json.data.forEach(function(itemArr,index){
                    if(itemArr[0].type == enum_type.title){
                        this.create_biaoti(itemArr);
                    }else{
                        this.create_hang(itemArr)
                    }
                }.bind(this));
            }

            //返回真正的数据
            _app.prototype.createJson = function(dataArr){
                var res = {"data":[]};
                dataArr.forEach(function(item){
                    var name = item.name;
                    var value = item.value;
                    var args = this.decode_name(name);
                    var id = args.id;
                    var type = args.type;
                    switch (true){
                        case(type == enum_type.title):
                            res.data.push([{"type":type, "content":value}]);
                            break;
                        case(type == enum_type.key):
                            res.data[id] = res.data[id] || [];
                            res.data[id][0] = {"type":type, "content":value};
                        case(type == enum_type.content):
                            res.data[id] = res.data[id] || [];
                            res.data[id][1] = {"type":type, "content":value};
                    }
                }.bind(this));
                //稀松数组处理
                var arr = res.data;
                var len = arr.length;
                while(len--){
                    if(typeof arr[len]=='undefined' ){
                        arr.splice(len,1);
                    }
                }
                return res;
            }

            //暴露接口
            var inst = new _app();
            return {
                "inst": inst,
                "createDomByData":inst.createDomByData.bind(inst),
                "createJson": inst.createJson.bind(inst),
                "create_biaoti":inst.create_biaoti.bind(inst),
                "create_hang":inst.create_hang.bind(inst),
                "removeLine":inst.removeLine.bind(inst),
                "clearLine":inst.clearLine.bind(inst),
                "pushUp":inst.pushUp.bind(inst),
                "pushDown":inst.pushDown.bind(inst)
            };
        })();

        //按钮代理
        $('#data_form').undelegate("button","click");
        $('#data_form').delegate("button","click",function(){
            var that = $(this);
              switch(true){
                  case(that.hasClass('app_remove')):
                      app.removeLine(this);
                      break;
                  case(that.hasClass('app_create_biaoti')):
                      app.create_biaoti();
                      break;
                  case(that.hasClass('app_create_hang')):
                      app.create_hang();
                      break;
                  case(that.hasClass('app_clear')):
                      app.clearLine();
                      break;
                  case(that.hasClass('app_up')):
                      app.pushUp(this);
                      break;
                  case(that.hasClass('app_down')):
                      app.pushDown(this);
                      break;
                  case(that.hasClass('app_create_from_copy')):
                      try{
                          var input = prompt('请粘贴已复制的数据');
                          if(input){
                              app.createDomByData(JSON.parse(input));
                          }
                      }catch(e){
                          alert('数据结构不正确')
                      }
                      break;
              }
        })

        //-------------------恢复数据
        try {
            eval("app.createDomByData(JSON.parse('{{ info.get('gameDesc') }}'.replace(/&quot;/g,'\"')))");
        }catch(e){  };

        //-------------------复制粘贴
      (function(){
          var url = 'https://cdn.bootcss.com/clipboard.js/2.0.4/clipboard.min.js';
          var onload = function(){
              (new ClipboardJS('#app_copy',{
                text:function(){
                    return JSON.stringify(app.createJson($('#data_form').serializeArray()));
                }
            })).on('success', function(e) {
                alert('复制成功');
    //            console.info('Action:', e.action);
    //            console.info('Text:', e.text);
    //            console.info('Trigger:', e.trigger);
    //
    //            e.clearSelection();
            });
          }
          if(typeof ClipboardJS != 'undefined')
              onload()
          else{
              var script = document.createElement('script');
              script.src = url;
              script.onload = onload;
              document.body.appendChild(script);
          }

      })()
  });
</script>
%rebase admin_frame_base