<!DOCTYPE html>
<html>
<head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>{{info['entry_title']}}</title>
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        <meta id="MobileViewport" name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1 user-scalable=0" servergenerated="true">
        <script type="text/javascript" src='/assert/default/lib/jquery-2.1.4.min.js'></script>
        <style>
            *{
                padding: 0px;
                margin:0px;
            }
            html{
                height: 100%;
                width: 100%;
                background: #AAA url(/assest/default/image/invite/bg2.jpg) no-repeat;
                background-size: 100% 100%;
            }
            #downdiv a{
                    position:relative;
                    display:block;
                    width:100%;
                    height:100%;
                    z-index:1;
            }

            #downdiv{
                width: 100%;
                top:70%;
                position: absolute;
                text-align: center;
            }
            #downdiv img{
                width: 60%;
            }
            #translayer{
                position:fixed;
                height: 100%;
                width: 100%;
                z-index:999;
                display:none;
            }

            #layertip{
                width: 100%;
                height:100%;
                position:relative;
            }

        </style>
</head>

<body>
    <div id="downdiv">
        <a  href="{{info['downloadUrl']}}" id="download_a">
            <img src="/assest/default/image/invite/dlbtn.png" />
         </a>
    </div>
    
    <div id="translayer">
        <div id="layertip"></div>
    </div>

</body>

<script type="text/javascript">
    $(function(){
        openApp();
    });

    function openApp()
    {   

        var loadTime = +(new Date());
        window.setTimeout( function(){
            var timeOut = +(new Date());
            if( timeOut - loadTime < 5000 )//打开失败
            {   
                    window.parent.location ="{{info['downloadUrl']}}";
                
            } else{
                window.close();
            }

        }, 25);
        
        window.parent.location = "{{info['scheme']}}";

    }
</script>
</html>
