<!DOCTYPE html>
<html>
    <head>
        <title>{{title}}</title>
        <style type="text/css">
            *{margin:0;padding:0;}
            html,body{
                height: 100%;
                width: 100%;
                position: absolute;
            }
            #wrap{
                width:100%;
                height:100%;
                overflow-y: auto;

                /*背景*/
                background-size:100% 100%;
                background:url("/intro/notice_beijin.png");
                background-repeat: no-repeat;
                background-size:100% 100%;
                /**/

                /*描边阴影*/
                box-shadow: #001020 0px 0px 18px inset;
                /**/

                /*默认字体*/
                color: #f3f6ff ;
                font-size: 24px;    /*如果不支持vw，则用这个*/
                font-size: 3.3vw;   /*字体大小按屏幕宽度 3.3% 显示*/
                /**/
            }
            .wrap-content{
                    padding:8px;
            }
        </style>
    </head>
    <body>
        <div id='wrap'>
             <div class="wrap-content">
                 {{!content}}
             </div>
        </div>
    </body>
</html>