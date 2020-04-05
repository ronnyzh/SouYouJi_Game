<style type="text/css">.config-table td.table-title {
    text-align: center;
    font-size: 13px;
    vertical-align: middle
}</style>
<div class="block">
    %include admin_frame_header
    <div class="content" id='good_app' style="float:left;width:100%;position:relative;top:2.6em">
        <form class="form-horizontal group-border-dashed" id='gameForm' v-on:submit="onSubmit"
              action="{{info['submitUrl']}}" method="post" style="border-radius: 0px;" enctype="multipart/form-data">
            <input type="hidden" name="goodsId" v-bind:value="goodId"/>
            <input type="hidden" name="goods_type" v-bind:value="goodsInfo.type"/>
            <table class='table config-table'>
                <tr>
                    <td width='20%' class='table-title' style="background-color:#d9edf7;font-size:17px">编辑商品</td>
                </tr>
                <tr>
                    <td>
                        <table class='table config-table' border='1'>
                            <tr>
                                <td class='table-title'>商品名称</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' v-model="goodsInfo.name"
                                           v-bind:value="goodsInfo.name" id="name" name="name" class="form-control"
                                           placeholder="商品名称（必填）">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>商品介绍</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' v-model="goodsInfo.note"
                                           v-bind:value="goodsInfo.note" id="note" name="note" class="form-control"
                                           placeholder="商品介绍">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title'>商品类型</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' v-model="goodsInfo.goodsType"
                                           v-bind:value="goodsInfo.goodsType" id="goodsType" name="goodsType"
                                           class="form-control" readonly>
                                </td>
                            </tr>
                            %if info['type'] in ['0', '2']:
                            <tr>
                                <td class='table-title' v-if="system == 'HALL'">游戏钻石数</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' v-bind:value="goodsInfo.cards"
                                           id="cards" name="cards" class="form-control" placeholder="游戏钻石数（必填）">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title' v-if="system=='HALL'">{{lang.GOODS_CARD_PRESENT_TXT}}</td>
                                <td>
                                    <input type="text" style='width:100%;float:left'
                                           v-bind:value="goodsInfo.present_cards" id="present_cards"
                                           name="present_cards" class="form-control" placeholder="赠送钻石数">
                                </td>
                            </tr>
                            %else:
                            <tr>
                                <td class='table-title' v-if="system=='HALL'">商品属性</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' v-bind:value="goodsInfo.attribute"
                                           id="attribute" name="attribute" class="form-control" placeholder="商品属性">
                                </td>
                            </tr>
                            <tr>
                                <td class='table-title' v-if="system == 'HALL'">游戏商品数</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' v-bind:value="goodsInfo.cards"
                                           id="cards" name="cards" class="form-control" placeholder="游戏商品数（必填）">
                                </td>
                            </tr>
                            %end
                            <tr>
                                <td class='table-title'>商品价格（单位：元）</td>
                                <td>
                                    <input type="text" style='width:100%;float:left' v-bind:value="goodsInfo.price"
                                           id="price" name="price" class="form-control" placeholder="商品价格（单位：元）（必填）">
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div style="text-align:center;padding: 10px 10px 10px;">
                            <button type="submit" class="btn btn-primary btn-sm"><i class="glyphicon"> {{lang.BTN_SUBMIT_TXT}} </i></button>
                            <button type="button" class="btn btn-primary btn-sm" v-on:click="onClick"><i class="glyphicon"> {{lang.BTN_BACK_TXT}} </i> </button>
                        </div>
                    </td>
                </tr>
            </table>
        </form>
    </div>
</div>

<script type="text/javascript">
    function initPage(results) {  //渲染页面
        var good_app = new Vue({
            el: '#good_app'
            , data: {
                goodsInfo: results.goods_info,
                goodId: '',
                action: '',
                system: ''
            }, mounted: function () {
                var self = this;
                self.$data.goodsInfo = results.goods_info;
                self.$data.goodId = "{{goodsId}}";
                self.$data.action = "{{info['submitUrl']}}";
                self.$data.system = "{{system}}";

            }, methods: {
                onSubmit: function (e) {
                    e.preventDefault();
                    formAjax($('#gameForm').attr("action"), $('#gameForm').attr("method"), $('#gameForm').serialize(), '正在修改...');
                },
                onClick: function (e) {
                    e.preventDefault();
                    window.location.href = "{{info['backUrl']}}";
                }
            }, delimiters: ['${', '}']

        });

    }

    $(function () {  //获取数据接口
        var api = String.format("/admin/goods/info/{0}", {{ goodsId }});
        $.getJSON(api, function (results) {
            initPage(results);
        });
    });


</script>
%rebase admin_frame_base
