<!DOCTYPE html>
<!-- saved from url=(0054)file:///D:/phpStudy/WWW/qiandaochoujiang/turnlate.html -->
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>{{setting['activice']['title'] if setting.get("activice").get('title') else "" }}</title>
    <link rel="stylesheet" href="{{info['STATIC_ADMIN_PATH']}}/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{info['STATIC_ADMIN_PATH']}}/css/style.css">
    <style>
        html{overflow: hidden;}
        body{overflow: hidden;}
        .bgimg{
            position: absolute;
            z-index: -2;
            width: 100%;
            height: 100%;
            margin:auto;
            top:0;
            bottom:0;
            left:0;
            right:0;
            background-image:url({{info['STATIC_ADMIN_PATH']}}/images/bg.jpg);
            background-repeat:no-repeat;
            background-size:100% 100%;
        }
        .main{width: 100%;height: 100%;top:0;bottom: 0;left: 0;right: 0;}
        .main > *, .pab-mat{position: absolute ;margin: auto;}
        .main > * {z-index: 1;top:0;right:0;bottom:0;left:0;}
        .content {width: 90%;height:90%;top:0;bottom:0;right:0;left:0;}
        .content > * {z-index: 1;}
        .content > .scale9box {z-index:0;top:0;bottom:0;right:0;width: 80%;height:90%;}
        .banner-1 {top:0;bottom:0;left: -6%;}
        .flag {top:-6%;left:25%;width:60%;}
        .turnplate,
        .turnplate > canvas{width:100%;height: 100%;}
        .turnplate > .pointer {top:0;bottom:0;right:0;left:0;height: 35%;width:26.4%}
        .drawCount {top:50%;right:0;left:0;width:16%;height:16%;font-size:1.5vw;color:#fff;text-align: center;}

        .parkbox{font-size: 2.8vw;}
        .parkbox .partitle  {text-align: center;}
        .parbody {overflow: auto}
        .parkbox .prizebox {background:transparent;box-shadow:none;overflow: hidden;margin:0;}
        .prizebox .prizelist {padding:0;}
        .banner-2 {right:0;height: 90%;}
        .banner-2-1 {width:90%;height:40%;top:20%;position: absolute;}
        .banner-2-2 {width:100%;bottom:5%; right0;position: absolute; font-size: 2.3vw;}
        .banner-2-2 .prizelist > div {white-space: nowrap;text-overflow: ellipsis;overflow:hidden;}
        .clearPadding {white-space: nowrap;}
        .content > img.closebtn{ z-index:1;width: 7vw; height:7vw; top:2%;right:-3%;}

        .win-panel{
            padding: 15px 0;
            width: 45vw;
            height:25vw;
            position: fixed;
            z-index: 1001;
            top: 0;
            left: 0;
            bottom:0;
            right: 0;
            margin:auto;
            background: url({{info['STATIC_ADMIN_PATH']}}/images/ditu2.png);
            background-size: 100% 100%;
            display: none;
        }
        .win-panel-head{top:-20%;width:100%;height: 30%;position:absolute;}
        .head-bg{width:120%;top:0;bottom:0;left:-10%;right:-10%;}
        .head-title{width:40%;top:0;bottom:0;left:0;right:0;}
        .reward-bottom{bottom:5%;width:100%;position: absolute;}
        .reward-bottom > * {width:35%}
        .reward-list{position:relative;}
        .reward-desc{padding:0 5%;}
        .reward-div  {
            display: inline-block;
            position: relative;
            background: url({{info['STATIC_ADMIN_PATH']}}/images/wupinkuang.png) no-repeat;
            background-size: 100% 100%;
            width: 8vw;
            height: 8vw;
            text-align:center;
            padding-top:1vw;
            margin: 10% 2% auto 2%;
        }
        .div-img{height:50%;}
        .div-num{height: 25%;}


        #wheelcanvas{
            transform: rotate(0deg);
            -webkit-transform: rotate(0deg);
            -moz-transform: rotate(0deg);
            -ms-transform: rotate(0deg);
            -o-transform: rotate(0deg);
        }
        #turn {
            width:100%;height: 100%;
            transform: rotate(0deg);
            -webkit-transform: rotate(0deg);
            -moz-transform: rotate(0deg);
            -ms-transform: rotate(0deg);
            -o-transform: rotate(0deg);
        }
    </style>
</head>
<body >
<div class="bgimg"></div>
<div class="main pab-mat">
    <div class="content pab-mat">

        <img class="closebtn pab-mat hide" src="{{info['STATIC_ADMIN_PATH']}}/images/tuichu.png" alt=""
       >
        <img class="flag pab-mat" src="{{info['STATIC_ADMIN_PATH']}}/images/zi.png" alt="">
        <div class="pt10lr10 banner-1 pab-mat">
            <div class="turnplate"
                 style="background-image:url({{info['STATIC_ADMIN_PATH']}}/images/turnplate-panbg.png);background-size:100% 100%;padding:10px;">
                <canvas class="item " width="422px" height="422px" id="wheelcanvas"
                        style="transform: rotate(36deg);"></canvas>

                <img class="pointer pab-mat" src="{{info['STATIC_ADMIN_PATH']}}/images/turnplate-pointer.png">
                <div class="pab-mat drawCount">
                    <span style="white-space:nowrap" >剩余次数</span><br>
                    <span id="drawCount" style="color:#E5302F;font-size: 2vw">{{setting.get('drawCount','0')}}</span>
                </div>
                <div class="pointer  pab-mat"></div>
            </div>
            <div class="hide">
                <img src="{{info['STATIC_ADMIN_PATH']}}/images/turshadow1.png" class="img-responsive"
                     style="position:relative;top:-5px;">
            </div>
        </div>
        <div class="pt10lr10 mt20 banner-2 pab-mat">
            <div class="parkbox banner-2-1">
                <div class="partitle" >
                    <img src="{{info['STATIC_ADMIN_PATH']}}/images/zhuanpanhuodong-1.png" alt=""
                         style="width:60%">
                </div>


                <div class="parbody">
                    活动时间：<br>
                    {{setting['activice'].get("startdate","")}} ~ {{setting['activice'].get("enddate","")}}<br>
                    活动时间内完成任务获得奖券
                </div>
                <div class="parbody" style="height: 55%">
                    %for item in setting['user_schedule']:
                    <div class="clearfix pb5">
                        <div class="col-xs-6 clearPadding text-red">{{item['gameName']}}</div>
                        <div class="col-xs-4 clearPadding">{{item['gameFinishNum']}}/{{item['gameNum']}}</div>
                        <div class="col-xs-2 clearPadding">
                            %if item['isFinish'] == 1 :
                            <img src="{{info['STATIC_ADMIN_PATH']}}/images/N-xuanzhong.png" alt="" style="height: 2.5vw">
                            %else :
                            <img src="{{info['STATIC_ADMIN_PATH']}}/images/N-weixuanzhong.png" alt="" style="height: 2.5vw">
                            %end
                        </div>
                    </div>
                    %end
                </div>
            </div>
            <!-->
            <div class="parkbox banner-2-2">
                <div class="partitle">
                    <img src="{{info['STATIC_ADMIN_PATH']}}/images/zhuanpanhuodong-2.png" alt=""
                        style="width: 40%;">
                </div>
                <div class="parbody prizebox" style="height: 3vw">
                    <div class="prizelistwrap" id="demo" style="position:relative;">
                        <div class="prizelist" id="demo1">
                            %for item in setting['awardee']:
                            <div class="clearfix ">
                                <div class="col-xs-3 clearPadding text-red">
                                    {{ item['name']}}
                                </div>
                                <div class="col-xs-3 clearPadding">{{item['rewardTitle']}}</div>
                                <div class="col-xs-3 clearPadding">{{item['date']}}</div>
                            </div>
                            %end
                        </div>
                        <div class="prizelist" id="demo2">
                        </div>
                    </div>
                </div>
            </div>
            <!---->
        </div>
        <div class="scale9box pab-mat" ></div>
    </div>
</div>
<div class="maskbox" ></div>
<div class="win-panel">
    <div class="win-panel-head">
        <img src="{{info['STATIC_ADMIN_PATH']}}/images/caidai.png" alt="" class="pab-mat head-bg">
    </div>

    <div class="text-center reward-list">

    </div>
    <div class="text-center  reward-desc" style="padding-top:8vw">

            </div>
    <div class="text-center reward-bottom">
        <img src="{{info['STATIC_ADMIN_PATH']}}/images/anniu.png" alt="" class="reward-ok">
    </div>
</div>

<!--<div class="qdbox">-->
	<!--<div class="text-center text-green font18 reward-title"><strong>恭喜中奖！</strong></div>-->
	<!--<div class="text-center pt10 reward-desc">-->

    <!--</div>-->
	<!--<div class="text-center ptb15">-->
        <!--<img src="" class="reward-img" style="width:125px;margin-left:20px;">-->
    <!--</div>-->
	<!--<div class="text-center"><button class="btn btn-lottery reward-ok">好的</button></div>-->
<!--</div>-->



<!--<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/jquery-1.10.2.min.js"></script>-->
<!--<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/awardRotate.js"></script>-->
<script src="https://cdn.bootcss.com/zepto/1.2.0/zepto.min.js"></script>
<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/zepto/src/fx.js"></script>

<script type="text/javascript">
    var conX = 16,
        conY = 9,
    	precent_con = conX / conY,
        winX = document.documentElement.clientWidth,
        winY = document.documentElement.clientHeight,
    	precent_win = winX / winY,
        tX = precent_win > precent_con ? winY * precent_con : winX;
    	tY = tX / precent_con
    ;
    $(".main").css({'width':tX,'height':tY});

    var speed = 80;
    var demo = document.getElementById("demo");
    var demo2 = $("#demo2");
    var demo1 = $("#demo1");
    demo2.innerHTML = demo1.innerHTML;
    function demoMove(){
        var selfFunc = arguments.callee;
        demo1.css("transform","translateY(0)");
        demo1.animate(
            {translateY:"-100%" },
            30000,
            "linear",
            selfFunc
        )
    }
    demoMove();
//    function Marquee() {
//        if (demo2.offsetTop - demo.scrollTop <= 0)
//            demo.scrollTop -= demo1.offsetHeight;
//        else {
//            demo.scrollTop++;
//        }
//    }
//    MyMar = setInterval(Marquee, speed)
    var turnplate = {
        restaraunts: [],				//大转盘奖品名称
        colors: [],					//大转盘奖品区块对应背景颜色
        outsideRadius: 192,			//大转盘外圆的半径
        textRadius: 95,				//大转盘奖品位置距离圆心的距离
        insideRadius: 68,			//大转盘内圆的半径
        startAngle: 2 * Math.PI / 180 ,				//开始角度
        bRotate: false				//false:停止;ture:旋转
    };

    function loadimg(arr,funLoading,funOnLoad,funOnError){

        var numLoaded=0,
        numError=0,
        isObject=Object.prototype.toString.call(arr)==="[object Object]" ? true : false;

        var arr=isObject ? arr.get() : arr;
        var imgList = [];
        for(a in arr){
            var src=isObject ? $(arr[a]).attr("data-src") : arr[a];
            preload(src,arr[a],a);
        }

        function preload(src,obj,ind){
            var img=new Image();
            img.onload=function(){
                numLoaded++;
                funLoading && funLoading(numLoaded,arr.length,src,img,ind,imgList);
                funOnLoad && numLoaded==arr.length && funOnLoad(numLoaded,arr.length,imgList);
            };
            img.onerror=function(){
                numLoaded++;
                numError++;
                funOnError && funOnError(numLoaded,arr.length,src,img,ind);
            }
            img.src=src;
            imgList[ind] = img;
        }

    }
    var loadList = [];
    %for ind,item in enumerate(setting['activice']['rewardList']):
    loadList.push("{{item['imgUrl']}}");
    %end

    $(document).ready(function(){
        loadimg(loadList,function(numLoaded,len,src,obj,ind){
//            console.log(arguments);
            obj.id = "rewardImg_"+ind;
            obj.className = "hide";
            document.body.appendChild(obj);
        },init)

    });

    function init() {
        //动态添加大转盘的奖品与奖品区域背景颜色
        turnplate.restaraunts = [];
        turnplate.colors = [];
//        var colors = ["#FFF4D6", "#FFFFFF"];
        %for ind, item in enumerate(setting["activice"]["rewardList"]):
        turnplate.restaraunts.push("{{ item.get('baseRewardCount',item['title']) }}");
//        turnplate.colors.push(colors[ {{ind}} % 2 ]);
        turnplate.colors.push("transparent");
        %end


        var rotateTimeOut = function () {
            $('#turn').rotate({
                angle: 0,
                animateTo: 2160,
                duration: 16000,
                callback: function () {
//                    alert('网络超时，请检查您的网络设置！');
                }
            });
        };

        //旋转转盘 item:奖品位置; txt：提示语;
        var aa=  -124; //偏移修正
        var angles = 0;
        var deviation = 0;
        var rotateFn = function (item, param) {
            angles += 360 - angles % 360; //回归最近的360度

            angles += -deviation;//上次角度补充
            angles +=  (360 - item * (360 / turnplate.restaraunts.length) );
            //本次角度偏移
            deviation = (Math.random()*10 - 5 );
            angles += deviation;

            //多转几圈
            angles += 720 + aa;
//            $('#wheelcanvas').stopRotate();
//            $('#wheelcanvas').rotate({
//                angle: 0,
//                animateTo: angles + 1800 ,
//                duration: 8000,
//                callback: function () {
//                    openWin(param)
//                    turnplate.bRotate = !turnplate.bRotate;
//                }
//            });



//            $('#wheelcanvas').css("-webkit-transform","rotate("+angles+"deg)");
//            $('#wheelcanvas').css("-moz-transform","rotate("+angles+"deg)");
//            $('#wheelcanvas').css("-o-transform","rotate("+angles+"deg)");
//            $('#wheelcanvas').css("transform","rotate("+angles+"deg)");
            var wheel = $('#turn');

            wheel.css({
                        '-webkit-transition': 'all 4s ease-in-out',
                        'transition': 'all 4s ease-in-out',
                        '-webkit-transform': 'rotate(' + angles + 'deg)',
                        'transform': 'rotate(' + angles + 'deg)'
                    });

            setTimeout(function(){
                openWin(param)
                turnplate.bRotate = !turnplate.bRotate;
            }.bind(this),4000);



//            $('#wheelcanvas').animate(
//                {
//                    rotateZ: angles+'deg',
//                },
//                4000,
//                "ease-in-out",
//                function () {
//                    openWin(param)
//                    turnplate.bRotate = !turnplate.bRotate;
//                }
//            );
        };

        $('.pointer').click(function () {
            if (turnplate.bRotate)return;
            turnplate.bRotate = !turnplate.bRotate;
            var drawCount = $('#drawCount').text()
            if (drawCount == '0'){
                openWin("抽奖次数不足");
                return;
            }

            $('#drawCount').text("请求中...");
            var url = "{{info['submitUrl']}}";
            var postdata ={}
            $.ajax({
                url:url,
                type:"get",
                data:postdata,
                success:function (res) {

    //                console.log(res);
    //                alert(res.msg || "看控制台")
//                    var res = typeof res === "string" ?
                    var res = typeof res == "string"? JSON.parse(res):res;
                    if(res.code == 0){
                        //获取随机数(奖品个数范围内)
                        var item = res['data']['pos'];
                        //奖品数量等于10,指针落在对应奖品区域的中心角度[252, 216, 180, 144, 108, 72, 36, 360, 324, 288]
                        var obj = {};
                        res.data.content.forEach(function(d){
                            var key = d.type,
                                o = obj[key] = obj[key] || {},
                                baseRewardCount = parseInt(d.baseRewardCount),
                                imgUrl = d.imgUrl
                            ;
                            o.baseRewardCount = "baseRewardCount" in o
                                ? o.baseRewardCount + baseRewardCount
                                : baseRewardCount ;
                            o.imgUrl = imgUrl;
                            o.jumpUrl = d.jumpUrl || "";
                        });
                        var param = Object.keys(obj).map(function(key){return obj[key];});
                        rotateFn(item, param);
                    }else{
                        openWin(res.msg || "网络异常");
                    }
                    $('#drawCount').text(--drawCount);
                },
                error : function(){
                    $('#drawCount').text(drawCount);
                    turnplate.bRotate = !turnplate.bRotate;
                }
            });
//            return;


            /* switch (item) {
             case 1:
             rotateFn(252, turnplate.restaraunts[0]);
             break;
             case 2:
             rotateFn(216, turnplate.restaraunts[1]);
             break;
             case 3:
             rotateFn(180, turnplate.restaraunts[2]);
             break;
             case 4:
             rotateFn(144, turnplate.restaraunts[3]);
             break;
             case 5:
             rotateFn(108, turnplate.restaraunts[4]);
             break;
             case 6:
             rotateFn(72, turnplate.restaraunts[5]);
             break;
             case 7:
             rotateFn(36, turnplate.restaraunts[6]);
             break;
             case 8:
             rotateFn(360, turnplate.restaraunts[7]);
             break;
             case 9:
             rotateFn(324, turnplate.restaraunts[8]);
             break;
             case 10:
             rotateFn(288, turnplate.restaraunts[9]);
             break;
             } */
//            console.log(item);
        });

        //页面所有元素加载完毕后执行drawRouletteWheel()方法对转盘进行渲染
        drawRouletteWheel();
    }
    function rnd(n, m) {
        var random = Math.floor(Math.random() * (m - n + 1) + n);
        return random;
    }
//    $(document).ready(function () {
//
//    })

    function drawRouletteWheel() {
        var canvas = document.getElementById("wheelcanvas");
        if (canvas.getContext) {
            //根据奖品个数计算圆周角度
            var arc = Math.PI / (turnplate.restaraunts.length / 2);
            var ctx = canvas.getContext("2d");
            //在给定矩形内清空一个矩形
            ctx.clearRect(0, 0, 422, 422);
            //strokeStyle 属性设置或返回用于笔触的颜色、渐变或模式
            ctx.strokeStyle = "#FFBE04";
            //font 属性设置或返回画布上文本内容的当前字体属性
            ctx.font = '16px Microsoft YaHei';
            //加载文字资源
            loadimg(
                ["{{info['STATIC_ADMIN_PATH']}}/images/shuzi.png"],
                function(numLoaded,len,src,img,ind,imgList){
                    var dataList = [];
                    turnplate.restaraunts.forEach(function(text,ind){
                        var text = text.replace(/[0-9]/g,"") === "" ? text : "" ;
                        text = text === "" ? "" : "*" + text;
                        (function(){
                            var index = ind;
                            artNumImgData(img,text,"",function(imgData){
                                dataList[index] = imgData;
                                if(dataList.length === turnplate.restaraunts.length){
                                    drawReward(dataList);
                                }
                            })
                        })()

                    })
                }
            );


            function drawReward(dataList){
                var source_load = [
                        "{{info['STATIC_ADMIN_PATH']}}/images/turnplate-bg.png"
                    ];
                loadimg(
                    source_load.concat(dataList || []),
                    function(){},
                    function(numLoaded,len,imgList){
                    ctx.drawImage(imgList[0],0,0,422,422);
                        for (var i = 0; i < turnplate.restaraunts.length; i++) {
                            var angle = turnplate.startAngle + i * arc;
                            /*ctx.fillStyle = turnplate.colors[i];
                            ctx.beginPath();
                            //arc(x,y,r,起始角,结束角,绘制方向) 方法创建弧/曲线（用于创建圆或部分圆）
                            ctx.arc(211, 211, turnplate.outsideRadius, angle, angle + arc, false);
                            ctx.arc(211, 211, turnplate.insideRadius, angle + arc, angle, true);
                            ctx.stroke();
                            ctx.fill();*/
                            //锁画布(为了保存之前的画布状态)
                            ctx.save();

                            //----绘制奖品开始----
                            ctx.fillStyle = "#E5302F";
                            var text = turnplate.restaraunts[i];
                            var line_height = 17;
                            //translate方法重新映射画布上的 (0,0) 位置
                            ctx.translate(211 + Math.cos(angle + arc / 2) * turnplate.textRadius, 211 + Math.sin(angle + arc / 2) * turnplate.textRadius);

                            //rotate方法旋转当前的绘图
                            ctx.rotate(angle + arc / 2 + Math.PI / 2);

                            /*//添加对应图标
                            function drawIcon(img) {
                                //                    ctx.scale(0.4, 0.4);
                                //                    ctx.beginPath();
                                //                    ctx.arc(0,70,60,0,2*Math.PI);
                                //                    ctx.fill();
                                //                    ctx.globalCompositeOperation="source-in";

                            }*/
                            var img = document.getElementById("rewardImg_" + i);
                            /*img.onload = function () {
                                drawIcon(img);
                            };*/
                            ctx.drawImage(img, -30, -80, 60, 60);

                            //数字
                            var numberImg = imgList.concat().splice(source_load.length)[i];
                            ctx.drawImage(
                                numberImg,
                                -numberImg.naturalWidth * 0.5 * 0.5, -20,
                                numberImg.naturalWidth * 0.5, numberImg.naturalHeight * 0.5
                            );

    //                        /** 下面代码根据奖品类型、奖品名称长度渲染不同效果，如字体、颜色、图片效果。(具体根据实际情况改变) **/
    //                        if (text.indexOf("M") > 0) {//流量包
    //                            var texts = text.split("M");
    //                            for (var j = 0; j < texts.length; j++) {
    //                                ctx.font = j == 0 ? 'bold 20px Microsoft YaHei' : '16px Microsoft YaHei';
    //                                if (j == 0) {
    //                                    ctx.fillText(texts[j] + "M", -ctx.measureText(texts[j] + "M").width / 2, j * line_height);
    //                                } else {
    //                                    ctx.fillText(texts[j], -ctx.measureText(texts[j]).width / 2, j * line_height);
    //                                }
    //                            }
    //                        } else if (text.indexOf("M") == -1 && text.length > 6) {//奖品名称长度超过一定范围
    //                            text = text.substring(0, 6) + "||" + text.substring(6);
    //                            var texts = text.split("||");
    //                            for (var j = 0; j < texts.length; j++) {
    //                                ctx.fillText(texts[j], -ctx.measureText(texts[j]).width / 2, j * line_height);
    //                            }
    //                        } else {
    //                            //在画布上绘制填色的文本。文本的默认颜色是黑色
    //                            //measureText()方法返回包含一个对象，该对象包含以像素计的指定字体宽度
    //                            ctx.fillText(text, -ctx.measureText(text).width / 2, 0);
    //                        }


                            //把当前画布返回（调整）到上一个save()状态之前
                            ctx.restore();
                            //----绘制奖品结束----
                        }
                        var cpimg = document.createElement("img");
                        cpimg.id = "turn";
                        cpimg.src = canvas.toDataURL();
                        cpimg.onload = function(){
                            cpimg.setAttribute("style",canvas.getAttribute("style"));


                            $(canvas).hide();
                            $(canvas).after(cpimg);
                        }
                });
            }


        }
    }

    function openWin(param,jumpUrl,callback){

        var win = $(".win-panel").first().clone();
        var mask = $(".maskbox").first().clone();
        $("body").append(mask,win);

        var desc = typeof param === "string" ? param : "";
        var descCon = win.find(".reward-desc");
        descCon.hide();
        //头部“获得奖品”
        var panelHead = win.find(".win-panel-head");
        panelHead.hide();

        switch (true){
            //是否显示提示语
            case Boolean(desc):
                descCon.show();
                descCon.html(
                    "<span class='' style='font-size: 2.5vw;'>"+desc+"</span>"
                );
                break;
            case (param instanceof  Array):
                panelHead.show()

                //显示中央奖品图片
                var jumpUrl = "";
                win.find(".reward-list").empty();
                    param.forEach(function (d) {
                        var number = d['baseRewardCount'];
                        var imgUrl = d['imgUrl'];
                        jumpUrl = d['jumpUrl'];
                        if (imgUrl) {
                            var con = $("<div class= 'reward-div'></div>");
                            var img = document.createElement("img");
                            con.append(img, $("<br>"));
                            img.src = imgUrl;
                            img.className = "div-img";
                            //插入数字
                            if (number) {
                                loadimg(
                                    ["{{info['STATIC_ADMIN_PATH']}}/images/shuzi.png"],
                                    function (numLoaded, len, src, obj, ind) {
                                        artNumImgData(obj, "*" + number, "", function (imgData) {
                                            var num_img = document.createElement("img");
                                            num_img.className = "div-num"
                                            num_img.src = imgData;
                                            con.append(num_img);
                                        });
                                    }
                                )
                            }
                            win.find(".reward-list").append(con);
                        }
                    });
                break;
        }

        if(jumpUrl){
            descCon.show();
            win.find(".reward-list > .reward-div ").css("marginTop","3%");
            win.css("height",win.height()*1.4);
            descCon.css({"paddingTop":"0"});
            descCon.html(
                "<span class='text-muted' style='font-size: 1.8vw;'>" +
                "奖品将会在近期寄出，请正确填写您的联系方式以方便客服人员核实确认" +
                "</span>" +
                "<div class='col-sm-8 col-sm-offset-2'>"+
                "<input  type='realName' id='realName' placeholder='请填写姓名' class='form-control text-center' style='margin-top:0.5vw'>"+
                "<input  type='number' id='phone' placeholder='请填写手机号' class='form-control text-center' style='margin-top:0.5vw'>"+
                "</div>"
            );
        }
        function hideWin() {
            function end(){
                mask.remove();
                win.remove();
                if(callback)
                    callback();
            }
            if(jumpUrl){
                $.ajax({
                    type:"get",
                    data:{
                        phone:win.find("#phone").val(),
                        realName:win.find("#realName").val()
                    },
                    url:jumpUrl,
                    success:function(res){
                        if(res.code == 0){
                            openWin(res.msg||"提交成功","",end);
                        }else{
                            openWin(res.msg||"网络错误");
                        }
                    },
                    error:function(){
                        openWin("网络错误");
                    }
                })
            }else{
                end();
            }
        }

        var sub = win.find(".reward-ok");
        sub.unbind("click");
        sub.click(hideWin);

        mask.show();
        win.show();
        mask.height($("body").height());
//        mask.click(hideWin)
    }


    /*背景*/
    $(document).ready(function(){
        var plist = [];
        for(var i = 1 ; i <= 9 ; i++){
            plist.push("{{info['STATIC_ADMIN_PATH']}}/images/plist/ditu_0"+i+".png");
        }
        $(".scale9box").scale9init(plist)
    });
    $.fn.scale9init = function(plist){
//        console.log(this);
        var $self = this,
            selfW = parseInt(this.width()),
            selfH = parseInt(this.height()),
            imgW = 0,
            imgH = 0,
            bgColor = "#ffdc96";
        var imgList=[];
        /*每张图片加载时*/
        function preLoaded(numLoaded,len,src,obj,ind){
            imgW+= ind < 3 ? obj.naturalWidth : 0;
            imgH+= ind % 3 === 0 ? obj.naturalHeight : 0;
            obj.className="scale9img scale9-"+ind;
            imgList[ind] = obj;

        }
        /*所有图片完成加载*/
        function allLoaded(){
            var sacleX = selfW / imgW,
                scaleY = selfH / imgH,
                scaleMin = sacleX > scaleY ? scaleY : scaleX;
            imgList.forEach(function(ele,ind,arr){
                $self.append(ele);
//                console.log(ele.naturalWidth,ele.naturalHeight);
                switch (true){
                    case (ind === 1 || ind === 7):
                        var cult = selfW;
                        [0,2].map(function(pos){
                            cult -= arr[pos].naturalWidth * scaleMin;
                        });
                        ele.width = cult;
                        ele.height = ele.naturalHeight * scaleMin;
                        break;
                    case (ind === 3 || ind === 5):
                        var cult = selfH;
                        [0,6].map(function(pos){
                            cult -= arr[pos].naturalHeight * scaleMin;
                        });
                        ele.height = cult;
                        ele.width = ele.naturalWidth * scaleMin;
                        break;
                    case (ind === 4):
                        var cult = selfW;
                        var cult2 = selfH;
                        [0,2].map(function(pos){
                            cult -= arr[pos].naturalWidth * scaleMin;
                        });
                        [0,6].map(function(pos){
                            cult2 -= arr[pos].naturalHeight * scaleMin;
                        });
                        ele.width = cult;
                        ele.height = cult2;
                        break;
                    default:
                        ele.width = ele.naturalWidth * scaleMin;
                        ele.height = ele.naturalHeight * scaleMin;
                }


            })
        }
        loadimg(plist,preLoaded,allLoaded);
        var bgDiv = $("<div></div>");
        bgDiv.addClass("pab-mat");
        bgDiv.css({
            "background":bgColor,
            "width":"97%",
            "height":"95%",
            "borderRadius":"20px",
            "zIndex":"-1",
            "top":"0",
            "bottom":"0",
            "left":"0",
            "right":"0",
        })
        $self.append(bgDiv);
//        $self.css("background",bgColor);
//        $self.css("borderRadius","50px");
    };

    //美术数字
    function artNumImgData(img,num,width,callback){
        list = ["*", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
        var idx = [];
        num.split("").map(function(n){
            var i = list.indexOf(n.toString());
            if(i > -1){
                idx.push(i)
            }
        });
        if(idx.length === 0){
            callback("");
            return ;
        }

        var nH = img.naturalHeight,
            nW = img.naturalWidth,
            pre_nW = nW / list.length,
            precent = ((width || pre_nW) / pre_nW )|| 1,
            tH = nH * precent,
            pre_tW = pre_nW * precent,
            tW = nW * precent,
            d = 0.7
            ;
        var dcanvas = document.createElement("canvas");
        dcanvas.width = pre_tW * idx.length * d;
        dcanvas.height = tH;
        var dtx = dcanvas.getContext('2d');

        var pngList = [];

        idx.forEach(function(i,ind){
            var canvas = document.createElement("canvas");
            canvas.width = pre_tW * d;
            canvas.height = tH;
            var ctx = canvas.getContext('2d');
            ctx.scale(precent,precent);
            ctx.drawImage(img,- i * pre_tW  - pre_tW * d / 4  ,0,tW,tH);


            pngList.push(canvas.toDataURL())
        })

        loadimg(
            pngList,
            function(numLoaded,len,src,img,ind,imgList){
                dtx.drawImage(img, ind * pre_tW * d, 0);
            },
            function(numLoaded,len,imgList){
                if(callback){
                    callback(dcanvas.toDataURL());
                }
            }
        )
    }

    /*所有元素加载完毕，调整*/
    $(document).ready(function(){
        var $main = $(".main"),
            mainH = parseInt($main.height()),
            mainW = parseInt($main.width()),
            long = mainH > mainW ? mainH : mainW,
            sort = mainH > mainW ? mainW : mainH,
            $ban1 = $(".banner-1"),
            $ban2 = $(".banner-2");

//        console.log(sort);
        $ban1.height(0.9 * sort);
        $ban1.width(0.9 * sort);
        $ban2.width ( long * 0.98 - $ban1.width() );
    });
//    function closeWin(){
//        window.opener=null;
//       window.open('', '_self', '');
//       window.close();
//    }
</script>
</body>
</html>