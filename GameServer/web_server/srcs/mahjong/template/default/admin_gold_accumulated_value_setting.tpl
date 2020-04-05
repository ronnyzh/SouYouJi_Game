<div>
    <script>
        var accmulated_list_js = new Array();
        $(
            function()
            {
                % for list_obj in original_info['accmulated_list']:
                    var row_tem = new Array();
                    % for list_obj_obj in list_obj:
                        row_tem.push({{list_obj_obj}});
                    % end
                    accmulated_list_js.push(row_tem);
                % end    
                for (var i=0; i<accmulated_list_js.length; i++)
                {
                    new_accumulated_item(accmulated_list_js[i][0],accmulated_list_js[i][1],accmulated_list_js[i][2]);
                }
            }
        );
    </script>
    <script>
        function validate()
        {
            var is_valid = true;
            $("input").each(function(){
                if(checkEmpty($(this).val())===true)
                {
                    alert("请填入内容");
                    $(this).focus();
                    is_valid = false;
                    return false;                    
                }
                else if(checkNumber($(this).val())===false)
                {
                    alert("请填入数字");
                    $(this).focus();
                    is_valid = false;
                    return false;              
                }                
            });

            return is_valid;
        }
        function trim(str)
        { 

            //删除左右两端的空格
    　　     return str.replace(/(^\s*)|(\s*$)/g, "");
        } 
        //验证字符串是否是数字
        function checkNumber(theObj) 
        {
            var reg = /^(-?\d+)(\.\d+)?$/;
            if (reg.test(theObj)) 
            {
                return true;
            }
            return false;
        }         
        //验证是否为空 返回true表示为空
        function checkEmpty(value)
        {
                if(trim(value)==null || trim(value)=="")
                {
                    return true;   
                }        
                else
                {
                    return false;
                }
        }

    </script>
    <script>
            var accumulated_row_index = 0;
            function delete_row(Obj)
            {
                t_body = Obj.parentNode.parentNode.parentNode;
                tr = Obj.parentNode.parentNode;
                t_body.removeChild(tr);
            }
            function input1_func(value, row, index) {
               var label_name = "accumulated_" + accumulated_row_index.toString() + "_0";
               element = '<input placeholder="输入最小比率" id=' + label_name + ' name= ' + label_name + '></input>';
               return [
                    element                   
               ].join('');
            }
            function input2_func(value, row, index) {
               var label_name = "accumulated_" + accumulated_row_index.toString() + "_1";
               element = '<input placeholder="输入最大比率" id=' + label_name + ' name= ' + label_name + '></input>';
               return [
                   element
               ].join('');
            }
            function input3_func(value, row, index) {
               var label_name = "accumulated_" + accumulated_row_index.toString() + "_2";
               element = '<input placeholder="输入比例" id=' + label_name + ' name= ' + label_name + '></input>';
               return [
                   element
               ].join('');
            }
            function value_delete_func(value, row, index) {
               var btn_name = "delete_btn_" + accumulated_row_index.toString();
               accumulated_row_index +=1
               element = '<button type="button" onclick="delete_row(this);" id=' + btn_name + ' name= ' + btn_name + '>删除</button>'               
               return [
                   element
               ].join('');
            }
            function new_accumulated_item(min_radio,max_radio,input_radio)
            {
                //默认值
                var min_radio = (arguments[0] !== undefined)? arguments[0] : "无数据,请输入";//设置第一个参数的默认值 
                var max_radio = (arguments[1] !== undefined)? arguments[1] : "无数据,请输入";//设置第二个参数的默认值
                var input_radio = (arguments[2] !== undefined) ? arguments[2] : "无数据,请输入";//设置第三个参数的默认值

                var new_row = document.getElementById('value_controller').insertRow(-1);
                var label_name1 = "accumulated_" + accumulated_row_index.toString() + "_0";
                var label_name2 = "accumulated_" + accumulated_row_index.toString() + "_1";
                var label_name3 = "accumulated_" + accumulated_row_index.toString() + "_2";
                var label_name4 = "accumulated_" + accumulated_row_index.toString() + "_3";
                accumulated_row_index +=1
                element1 = '<input placeholder="输入最小比率" id=' + label_name1 + ' value=' + min_radio + ' name= ' + label_name1 + '></input>';
                element2 = '<input placeholder="输入最大比率" id=' + label_name2 + ' value=' + max_radio + ' name= ' + label_name2 + '></input>';
                element3 = '<input placeholder="输入比例" id=' + label_name3 + ' value=' + input_radio + ' name= ' + label_name3 + '></input>';
                element4 = '<button type="button" onclick="delete_row(this);" id=' + label_name4 + ' name= ' + label_name4 + '>删除</button>'               
                var input1=new_row.insertCell(0);
                var input2=new_row.insertCell(1);
                var input3=new_row.insertCell(2);
                var delete_btn=new_row.insertCell(3);
                input1.innerHTML=element1;
                input2.innerHTML=element2;
                input3.innerHTML=element3;
                delete_btn.innerHTML=element4;
            }
    </script>

</div>

<form method="post" onsubmit="return validate();">
    <h1 align = 'center'>累计值调控</h1>

    <div class="panel panel-primary">
            <div class="panel-heading">
                <h3 class="panel-title">
                    B档AI比率
                </h3>
            </div>
            <div class="panel-body">
                        <div class="input-group">
                                <input type="text" class="form-control" value={{original_info["Ai_B_Pct"]}} placeholder="输入比率" id = "level_b_ai_radio" name="level_b_ai_radio" />
                        </div>
            </div>
    </div>    

    <div class="panel panel-primary">
            <div class="panel-heading">
                <h3 class="panel-title">
                    D档AI比率
                </h3>
            </div>
            <div class="panel-body">
                        <div class="input-group">
                                <input type="text" class="form-control" value={{original_info["Ai_D_Pct"]}} placeholder="输入比率" id="level_d_ai_radio"  name="level_d_ai_radio" />
                        </div>
            </div>
    </div>

    <div class="panel panel-primary">
            <div class="panel-heading">
                <h3 class="panel-title">
                    玩家比率
                </h3>
            </div>
            <div class="panel-body">
                        <div class="input-group">
                                <input type="text" class="form-control" value={{original_info["Player_Pct"]}} placeholder="输入比率" id="player_radio" name="player_radio" />
                        </div>
            </div>
    </div>
 
    <div class="panel panel-primary">
            <div class="panel-heading">
                <h3 class="panel-title">
                    初始累计值
                </h3>
            </div>
            <div class="panel-body">
                        <div class="input-group">
                                <input type="text" class="form-control"value={{original_info["Default_Pct"]}}  placeholder="输入比率" id="initial_accumulated_value" name="initial_accumulated_value" />
                        </div>
            </div>
    </div>    

    <div class="panel panel-primary">
            <div class="panel-heading">
                <h3 class="panel-title">
                    累计值调控
                </h3>
            </div>
                    <div class="panel-body">
                        <button type='button' class="btn btn-primary" onclick='new_accumulated_item();'>新建</button>
                        <table id='value_controller' class="table table-bordered table-hover"></table>
                        <script>
                                $('#value_controller').bootstrapTable({ 
                                    columns: 
                                    [
                                        {  
                                            field: 'input1',  
                                            formatter: input1_func
                                        }, 
                                        {  
                                            field: 'input2',  
                                            formatter: input2_func 
                                        },                                         
                                        {  
                                            field: 'input3',  
                                            formatter: input3_func 
                                        },                                         
                                        {  
                                            field: 'value_delete_btn',  
                                            formatter: value_delete_func 
                                        },                                         
                                    ],                                     
                                    formatNoMatches: function(){
                                        return "";
                                    },
                                });
                        </script>
                    </div>
    </div>
    <div align = 'center' >   
        <button id="btn_confirm"  type="submit"   class="btn btn-primary" style="width:220px;height:50px;margin : 10px;"> 确定 </button>
    <div>
</form>
%rebase admin_frame_base