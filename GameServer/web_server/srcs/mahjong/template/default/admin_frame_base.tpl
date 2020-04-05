<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no" />
    <meta name="renderer" content="webkit|ie-comp|ie-stand">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta http-equiv="Cache-Control" content="no-siteapp" />
    <meta name="keywords" content="scclui框架">
    <meta name="description" content="scclui为轻量级的网站后台管理系统模版。">
    <title>{{lang.MAHJONG_TITLE_TXT}}</title>

    <link rel="stylesheet" href="{{info['STATIC_ADMIN_PATH']}}/css/style.css?{{RES_VERSION}}">
    <link rel="stylesheet" href="{{info['STATIC_ADMIN_PATH']}}/css/bootstrap.css?{{RES_VERSION}}">
    <link rel="stylesheet" href="{{info['STATIC_ADMIN_PATH']}}/js/table/bootstrap-table.min.css?{{RES_VERSION}}" />
    <link rel="stylesheet" type="text/css" href="{{info['STATIC_ADMIN_PATH']}}/skin/qingxin/skin.css?{{RES_VERSION}}" id="layout-skin"/>
    <link rel="stylesheet" type="text/css" href="{{info['STATIC_ADMIN_PATH']}}/js/bootstrap.datetimepicker/css/bootstrap-datetimepicker.min.css?{{RES_VERSION}}" />
    <link rel="stylesheet" type="text/css" href="{{info['STATIC_ADMIN_PATH']}}/js/validate/css/bootstrapValidator.min.css?{{RES_VERSION}}" />
    <link rel="stylesheet" type="text/css" href="{{info['STATIC_ADMIN_PATH']}}/js/layerMobile/layer.css?{{RES_VERSION}}" />
    <link rel="stylesheet" type="text/css" href="{{info['STATIC_ADMIN_PATH']}}/js/fileInput/css/fileinput.min.css?{{RES_VERSION}}" />
    <link rel="stylesheet" type="text/css" href="{{info['STATIC_ADMIN_PATH']}}/js/fileInput/css/fileinput-rtl.min.css?{{RES_VERSION}}" />
    <!-- 文本编辑器 -->
    <link rel="stylesheet" type="text/css" href="{{info['STATIC_ADMIN_PATH']}}/js/summernote/xheditor.css?{{RES_VERSION}}" />
    <!-- 弹出层组件 -->
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/layerMobile/layer.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/lib/jquery-2.1.4.min.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/sccl.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/sccl-util.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/scroll/iscroll.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/bootstrap.datetimepicker/js/bootstrap-datetimepicker.min.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/bootstrap.datetimepicker/js/bootstrap-datetimepicker.zh-CN.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/validate/js/bootstrapValidator.min.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/ajax.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/summernote/xheditor-1.2.2.min.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/summernote/zh-cn.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/dialog.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/table/bootstrap-table.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/table/bootstrap-table-export.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/table/tableExport.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/table/bootstrap-table-zh-CN.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/admin_frame_init.js?{{RES_VERSION}}"></script>
    <script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/lib/vue/dist/vue.min.js"></script>
    <style type="text/css">
            #scroller {
                position:absolute;
                z-index: -1;
                width:92%;
                height:100%;
                -webkit-tap-highlight-color: rgba(0,0,0,0);
                -webkit-transform: translateZ(0);
                -moz-transform: translateZ(0);
                -ms-transform: translateZ(0);
                -o-transform: translateZ(0);
                transform: translateZ(0);
                -webkit-touch-callout: none;
                -webkit-text-size-adjust: none;
                -moz-text-size-adjust: none;
                -ms-text-size-adjust: none;
                -o-text-size-adjust: none;
                text-size-adjust: none;
                background: #fff;
            }
    </style>
    </head>
    <script type="text/javascript">
        var myScroll;
        function loaded () {   //初始化页面拖动插件
            myScroll = new IScroll('.cl-mcont', { preventDefault: false});
        }

    </script>
    <body onload="loaded();">
        <div class="cl-mcont">
           <div id="scroller">
               %include
            </div>
        </div>
    </body>
</html>
