<div>
    <script>
     var original_arguments_dic = new Array();
  
  %for key, value in original_arguments.iteritems():
        original_arguments_dic['{{key}}'] = '{{value}}';
  % end
    </script>
    <script>
        var column_name_map = {0:'min',1:'max',2:'min_change'};
        var column = 0;
        function input_func(value, row, index)
        {
            var id_name = "ai_config_" + index.toString() + "_" + (column % 3).toString();
            var original_arguments_key = index.toString()+"_"+(column % 3).toString();
            if(original_arguments_dic.hasOwnProperty(original_arguments_key))
            {
                var original_value = original_arguments_dic[original_arguments_key];
            }
            else
            {
                var original_value = '"数据没有值，请提交"';
            }

            column = column + 1;

            var input_str = '<input placeholder="输入数量" class="form-control" ' + ' value=' + original_value + ' name = ' + id_name + ' id = '+ id_name +'></input>';
            return [
                   //'<input placeholder="输入数量" name = id_name></input>'
                   input_str
               ].join('');                
        }
        function on_cancel()
        {
            window.location.href= "{{info['url_pre']}}";
        }
    </script>    

    <h1 align = 'center'>二人麻将D档AI基础配置</h1>

    
<form id='config_form' onsubmit="return sb();" method="post">



<div class="form-group">
    <table id = 'config_table' class="table table-bordered table-hover"> <table>
    <input hidden readonly="readonly" value={{game_id}}  name="game_id"></input>
</div>
    <div align = 'center'>       
        <button id="btn_confirm" type="submit" class="btn btn-primary" style="width:220px;height:50px;margin : 10px;"> 确定 </button>
        <button id="btn_cancel" type="button" class="btn btn-primary" style="width:220px;height:50px;margin : 10px;" onclick="on_cancel()"> 取消 </button>
    </div>    
</form>
            <script>
                    $('#config_table').bootstrapTable({ 
                        columns: 
                        [
                            {
                                field: 'round_info',
                                title: '场次信息',
                            },
                            {  
                                field: 'input1',  
                                title: '携带金币（MIN）',
                                formatter: input_func 
                            },                                         
                            {  
                                field: 'input2',  
                                title: '携带金币（MAX）',
                                formatter: input_func 
                            },                                         
                            {  
                                field: 'input3',  
                                title: '最小变化值',
                                formatter: input_func
                            }, 
                        ],
                        data: [
                                        {
                                            round_info:'新手场'
                                        },
                                        {
                                            round_info:'普通场'
                                        },
                                        {
                                            round_info:'中级场'
                                        },
                                        {
                                            round_info:'高级场'
                                        },
                                        {
                                            round_info:'土豪场'
                                        },
                                        {
                                            round_info:'至尊场'
                                        },
                                        //{
                                        //    round_info:'暴击场'
                                        //},
                              ]                        
                    })
            </script>

</div>

<script>

    function sb()
    {
        var row = 6;
        var column = 3;
        for (var _row=0;_row<row;_row++)
        {
            for (var _column=0;_column<column;_column++)  
            {
                var field_id = "ai_config_" + _row.toString() + "_" + _column.toString();
                var field_content = document.getElementById(field_id);

                if(trim(field_content.value)==null || trim(field_content.value)=="")
                {
                    alert("请填入内容");
                    field_content.focus();
                    return false;
                }                
                if(checkNumber(field_content.value) == false)
                {
                    alert("请输入数字");
                    field_content.focus();
                    return false;
                }
            }          
        }        

        return true;        
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
</script>

<script type="text/javascript">
function valid1()
{
    $('#config_form').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            ai_config_0_0: {
                message: 'The username is not valid',
                validators: {
                    notEmpty: {
                        message: 'The username is required and can\'t be empty'
                    },

 
                }
            },
            ai_config_0_1: {
                message: 'The username is not valid',
                validators: {
                    notEmpty: {
                        message: 'The username is required and can\'t be empty'
                    },

 
                }
            },            
        }
    });
}
</script>

%rebase admin_frame_base