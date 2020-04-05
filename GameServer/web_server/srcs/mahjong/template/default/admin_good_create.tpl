<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
    %include admin_frame_header
    <div class="content" id="goods_create_app" style="float:left;width:100%;position:relative;top:2.6em">
        <form class='form-horizontal group-border-dashed' action="{{ info['submitUrl'] }}" method='POST' id='gameForm'
              onSubmit='return false'>
               <span v-if="system == 'FISH'">
                         <input type='hidden' name="goods_type" :value='goodsType'/>
               </span>
            <table class='table config-table'>
                <tr>
                    <td width='20%' class='table-title' style="background-color:#d9edf7;font-size:20px">创建新商品</td>
                </tr>
                <tr>
                    <td>
                        <table class='table config-table'>
                            <tr>
                                <td class='table-title'>{{lang.GOODS_NAME_TXT}}</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' id="name" name="name"
                                           class="form-control" placeholder="商品名称（必填）">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>{{lang.GOODS_NOTE_TXT}}</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' id="note" name="note"
                                           class="form-control" placeholder="商品介绍">
                                </td>
                            </tr>
                            <tr v-if="system == 'HALL'">
                                <td class='table-title'>商品类型</td>
                                <td>
                                    <input id="goods_type" class="goods_type" type="radio" name="goods_type" value='0'
                                           checked='checked'/> 游戏钻石
                                    &nbsp;
                                    <!--
                                    <input id="goods_type" class="goods_type" type="radio" name="goods_type" value='2'/>
                                    金币场金币
                                    &nbsp;
                                    <input id="goods_type" class="goods_type" type="radio" name="goods_type" value='4'/>
                                    其他
                                    -->
                                </td>
                            </tr>
                            <!--
                            <tr class="attribute" style='display:none;'>
                                <td class='table-title'>商品属性</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' id="attribute" name="attribute"
                                           class="form-control" placeholder="商品属性">
                                </td>
                            </tr>
                            -->
                            <tr class="gamecards">
                                <td class='table-title' v-if="system == 'HALL'">游戏钻石数</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' id="cards" name="cards"
                                           class="form-control" placeholder="游戏钻石数（必填）">
                                </td>
                            </tr>
                            <tr class="gamegoods" style="display:none">
                                <td class='table-title' v-if="system == 'HALL'">商品数</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' id="goods" name="goods"
                                           class="form-control" placeholder="商品数（必填）">
                                </td>
                            </tr>
                            <tr class="present">
                                <td class='table-title' v-if="system=='HALL'">{{lang.GOODS_CARD_PRESENT_TXT}}</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' id="present_cards"
                                           name="present_cards" class="form-control" placeholder="赠送钻石数">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>商品价格（单位：元）</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' id="price" name="price"
                                           class="form-control" placeholder="商品价格（单位：元）（必填）">
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div style="text-align:center;padding: 10px 10px 10px;">
                            <button type="submit" class="btn btn-sm btn-primary "><i class="glyphicon">{{lang.BTN_SUBMIT_TXT}}</i></button>
                            <button type="button" class="btn btn-sm  btn-primary" id="backid"><i class="glyphicon">{{lang.BTN_BACK_TXT}}</i></button>
                        </div>
                    </td>
                </tr>
            </table>
        </form>
    </div>
</div>
</div>
<script type="text/javascript">

    $('.goods_type').click(function () {
        var choosVal = $(this).val()
        if (['0', '2', '4'].indexOf(choosVal) >= 2) {
            $('.attribute').css({'display': 'table-row'});
            $('.present').css({'display': 'none'});
            $('.gamegoods').css({'display': 'table-row'});
            $('.gamecards').css({'display': 'none'});
        } else {
            $('.attribute').css({'display': 'none'});
            $('.present').css({'display': 'table-row'});
        }
    });

    $('#gameForm').submit(function () {
        formAjax($(this).attr("action"), $(this).attr("method"), $(this).serialize(), '正在提交...');
    });

    $('#backid').click(function () {
        window.location.href = "{{info['backUrl']}}";
    });


</script>
%rebase admin_frame_base

<!--
<style type="text/css">.config-table td.table-title{text-align:center;font-size:13px;vertical-align:middle}</style>
<div class="block">
          %include admin_frame_header
          <div class="content" id="goods_create_app">
             <form class="form-horizontal group-border-dashed" id='gameForm' @submit.prevent="onSubmit" method="post" style="border-radius: 0px;" enctype="multipart/form-data">
               <span v-if="system == 'FISH'">
                         <input type='hidden' name="goods_type" :value='goodsType' />
               </span>
               <table class='table config-table'>
                        <tr>
                          <td width='20%' class='table-title' style="font-size:17px">创建新商品</td>
                        </tr>
                        <tr>
                              <td>
                                <table class='table config-table' border='1'>
                                    <tr>
                                         <td class='table-title'>{{lang.GOODS_NAME_TXT}}</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="name" name="name" class="form-control" placeholder="必填">
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>{{lang.GOODS_NOTE_TXT}}</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="note" name="note" class="form-control" >
                                         </td>
                                    </tr>
                                    <tr class="attribute" style="display:none" >
                                         <td class='table-title'>商品属性</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="attribute" name="attribute" class="form-control" >
                                         </td>
                                    </tr>
                                    <tr  v-if="system == 'HALL'">
                                        <td class='table-title'>商品类型</td>
                                         <td>
                                                <input id="goods_type" class="goods_type" type="radio" name="goods_type" value='0' checked='checked' /> 游戏钻石
                                                &nbsp;
                                                <input id="goods_type" class="goods_type" type="radio" name="goods_type" value='2' /> 金币场金币
                                                &nbsp;
                                                <input id="goods_type" class="goods_type" type="radio" name="goods_type" value='4' /> 其他
                                         </td>
                                    </tr>
                                    <tr>
                                        <td class='table-title' v-if="system == 'HALL'">{{lang.GOODS_CARD_TXT}}</td>
                                        <td class='table-title' v-if="system == 'FISH'">{{lang.GOODS_COIN_TXT}}</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="cards" name="cards" class="form-control" placeholder="必填">
                                         </td>
                                    </tr>
                                     <tr>
                                         <td class='table-title' v-if="system=='HALL'">{{lang.GOODS_CARD_PRESENT_TXT}}</td>
                                         <td class='table-title' v-if="system=='FISH'">{{lang.GOODS_COIN_PRESENT_TXT}}</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="present_cards" name="present_cards" class="form-control">
                                         </td>
                                    </tr>
                                    <tr>
                                         <td class='table-title'>商品价格（单位：元）</td>
                                         <td>
                                             <input type="text" style='width:100%;float:left' id="price" name="price" class="form-control" placeholder="必填">
                                         </td>
                                    </tr>
                        </tr>
              </table>
              <div class="modal-footer" style="text-align:center">
                   <button type="submit" class="btn btn-primary btn-sm">{{lang.BTN_SUBMIT_TXT}}</button>
                  <button type="button" class="btn btn-primary btn-sm" @click.prevent="onBack">{{lang.BTN_BACK_TXT}}</button>
              </div>
            </form>
          </div>
</div>
</div>
<script type="text/javascript">

    $('.goods_type').click(function(){
        var choosVal = $(this).val()
        if (['0','2', '4'].indexOf(choosVal)>=0){
            $('.endDateDiv').css({'display':'none'});
        }else{
            $('.endDateDiv').css({'display':'table-row'});
        }
    });

    var goods_create_app = new Vue({
                'el': '#goods_create_app',
                'data': {
                        'system': '',
                        'goodsType': '',
                },mounted: function(){
                    this.$data.system = '{{system}}',
                    this.$data.goodsType = '{{goods_type}}'
                },methods: {
                    onSubmit:function(){
                          formAjax($('#gameForm').attr("action"), $('#gameForm').attr("method"), $('#gameForm').serialize(),'正在创建...');
                    },
                    onBack: function(){
                        window.location.href="{{info['backUrl']}}";
                    }
                }
    });

</script>
%rebase admin_frame_base
-->