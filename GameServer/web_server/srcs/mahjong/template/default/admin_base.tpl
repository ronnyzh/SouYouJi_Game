<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no" />
    <meta name="renderer" content="webkit|ie-comp|ie-stand">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta http-equiv="Cache-Control" content="no-siteapp" />
    <meta name="keywords" content="wy框架">
    <meta name="description" content="wy框架模板">
    <title>{{lang.MAHJONG_TITLE_TXT}}</title>

    <link rel="stylesheet" href="{{datas['STATIC_ADMIN_PATH']}}/css/sccl.css?{{RES_VERSION}}">
    <link rel="stylesheet" href="{{datas['STATIC_ADMIN_PATH']}}/css/bootstrap.css?{{RES_VERSION}}">
    <link rel="stylesheet" type="text/css" href="{{datas['STATIC_ADMIN_PATH']}}/skin/blue/skin.css?{{RES_VERSION}}" id="layout-skin"/>
    <link rel="stylesheet" href="{{datas['STATIC_ADMIN_PATH']}}/js/layerMobile/layer.css?{{RES_VERSION}}">
  </head>

  <body>
    <div class="layout-admin">
        %include admin_header
        <aside class="layout-side">
            <ul class="side-menu"></ul>
        </aside>

        <div class="layout-side-arrow"><div class="layout-side-arrow-icon"><i class="icon-font">&#xe60d;</i></div></div>

        <section class="layout-main">
            <!-- <div class="layout-main-tab"> -->
                <!-- <button class="tab-btn btn-left"><i class="icon-font">&#xe60e;</i></button> -->
                <!-- <nav class="tab-nav"> -->
                    <!-- <div class="tab-nav-content"> -->
                        <!-- <a href="javascript:;" class="content-tab active" data-id="home.html">首页</a> -->
                    <!-- </div> -->
                <!-- </nav> -->
                <!-- <button class="tab-btn btn-right"><i class="icon-font">&#xe60f;</i></button> -->
            <!-- </div> -->
            <div class="layout-main-body">
                <iframe class="body-iframe" name="iframe0" width="100%" height="100%" src="{{datas['ADMIN_DEFAULT_PAGE']}}" frameborder="0" data-id="home.html" seamless></iframe>
            </div>
        </section>
        <div class="layout-footer">{{lang.COPY_RIGHT_TXT}}</div>
    </div>
    <script type="text/javascript" src="{{datas['STATIC_ADMIN_PATH']}}/lib/jquery-1.9.0.min.js?{{RES_VERSION}}"></script>
    <!-- <script type="text/javascript" src="{{datas['STATIC_ADMIN_PATH']}}/lib/vue/dist/vue.min.js?{{RES_VERSION}}"></script> -->
    <script type="text/javascript" src="{{datas['STATIC_ADMIN_PATH']}}/js/layerMobile/layer.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{datas['STATIC_ADMIN_PATH']}}/js/sccl.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{datas['STATIC_ADMIN_PATH']}}/js/sccl-util.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{datas['STATIC_ADMIN_PATH']}}/js/dialog.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{datas['STATIC_ADMIN_PATH']}}/js/checkEvent.js?{{RES_VERSION}}"></script>
    <script type="text/javascript">
        /*
          初始化加载
        */
        $(function(){
            /*获取皮肤*/

            /*菜单json*/
            var menu = [
             %for mainModule in mainModules:
                {"name":"{{mainModule['txt']}}","order":"1","isHeader":"1",
                    "childMenus":[
                    %if mainModule['subModules']:
                         %for subModule in mainModule['subModules']:
                             %if subModule['subsubModules']:
                                    {"id":"{{subModule['txt']}}","name":"{{subModule['txt']}}","url":"","icon":"&#xe602;","order":"1","isHeader":"0",
                                    "childMenus":[
                                     %if subModule['subsubModules']:
                                        %for subsubModule in subModule['subsubModules']:
                                          {"parentId":"{{subModule['txt']}}","name":"{{subsubModule['txt']}}","url":"{{subsubModule['url']}}","icon":"&#xe602;","order":"1","isHeader":"0",
                                            "childMenus":""},
                                        %end
                                    %end
                            ]},
                            %else:
                                            {"id":"{{subModule['txt']}}","name":"{{subModule['txt']}}","url":"{{subModule['url']}}","icon":"&#xe602;","order":"1","isHeader":"0",
                                            "childMenus":[
                                             %if subModule['subsubModules']:
                                                %for subsubModule in subModule['subsubModules']:
                                                  {"parentId":"{{subModule['txt']}}","name":"{{subsubModule['txt']}}","url":"{{subsubModule['url']}}","icon":"&#xe602;","order":"1","isHeader":"0",
                                                    "childMenus":""},
                                                %end
                                            %end
                                    ]},


                            %end

                        %end
                    %end

                ]},
            %end
            ];
            initMenu(menu,$(".side-menu"));
            $(".side-menu > li").addClass("menu-item");
            /*获取菜单icon随机色*/
            //getMathColor();
        });
    </script>
    <script type="text/javascript">
            checker._start(); //开始刷新
    </script>
  </body>
</html>
