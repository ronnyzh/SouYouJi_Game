$(function(){

            $(".datetime").datetimepicker({
                            autoclose   : true
            });            

            $(".timeStamp").datetimepicker({
                            autoclose   : true
            });

            $('body').on('click','.pickdate-btn',function(){
                $(".datetime").datetimepicker({
                        autoclose               : true,
                        format                  : 'yyyy-mm-dd',
                        todayHighlight          : true,
                        startView               : 1,
                        language                : 'zh-CN'
                });
            });             

            $('body').on('click','.pickdate-btn',function(){
                $(".datetime").datetimepicker({
                        autoclose               : true,
                        format                  : 'yyyy-mm-dd',
                        todayHighlight          : true,
                        startView               : 1,
                        language                : 'zh-CN'
                });
            });             

                               
            $('body').on('focus','#pick-date-start',function(){
                    $(".datetime").datetimepicker({
                            autoclose   : true
                    });
            });

            $('body').on('focus','.pickdate',function(){
                $(".datetime").datetimepicker({
                        autoclose               : true,
                        format                  : 'yyyy-mm-dd',
                        todayHighlight          : true,
                        startView               : 1,
                        language                : 'zh-CN'
                });
            });              

            $('body').on('click','.pickdate-btn1',function(){
                $(".timeStamp").datetimepicker({
                        autoclose               : true,
                        format                  : 'yyyy-mm-dd hh:ii',
                        todayHighlight          : true,
                        startView               : 0,
                         minView                : 1,
                        language                : 'zh-CN'
                });
            });

            $('body').on('focus','.pickdate1',function(){
                $(".timeStamp").datetimepicker({
                        autoclose               : true,
                        format                  : 'yyyy-mm-dd hh:ii',
                        todayHighlight          : true,
                        startView               : 0,
                         minView                : 1,
                        language                : 'zh-CN'
                });
            });                     

            $('body').on('click','.export',function(){  //导出数据按钮点击事件
                    var cssVal = $('.export-menu').css('display');
                    console.log(cssVal);
                    if (cssVal == 'none'){
                        $('.export-menu').css('display','block');
                    }else{
                        $('.export-menu').css('display','none');
                    }
            });                    

            $('body').on('click','.bet-pagesize',function(){  //页数按钮点击事件
                    var cssVal = $('.page-size-menu').css('display');
                    console.log(cssVal);
                    if (cssVal == 'none'){
                        $('.page-size-menu').css('display','block');
                    }else{
                        $('.page-size-menu').css('display','none');
                    }
            });                    

            //回放关闭按钮
            $('body').on('click','.closePage',function(){
                    layer.closeAll();
            });

             $('#selectAll').click(function(){
                       $("#list :checkbox,#all").prop("checked", true);
             });   

             $('#reverser').click(function(){
                  $("#list :checkbox,#all").each(function () {  
                      $(this).prop("checked", !$(this).prop("checked"));
                      console.log(1);
                  });
             });   

             $('#unSelect').click(function(){
                       $("#list :checkbox,#all").prop("checked", false);
            });

        }); 