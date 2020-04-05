module G559{
    export namespace rfaw {
        export class BaseCardPattern extends rfa.BaseCard {
            public wcValueList;
            public showCardIdList;
            public cardIdList;

            constructor(type, data, keyValue?, wcValueList?, showCardIdList?) {
                super(type, data, keyValue);
                this.wcValueList = wcValueList;
                this.showCardIdList = showCardIdList;
            }

            isWildcard(cardId) {
                return rfaw.utils.isWildcard(cardId);
            }

            getShowCardIdList() {
                return (this.showCardIdList || this.cardIdList).concat();
            }

            getActionData() {
                var data = [this.cardIdList.join(",")];
                if (this.wcValueList != null) {
                    jx.each(this.wcValueList, function (cardId, i) {
                        this.wcValueList[i] = rfa.utils.transferWildCardTo(cardId);
                    }, this);
                    data.push(this.wcValueList.join(","));
                }
                return data;
            }

            isAllWildcardPattern() {
                return !this.isWildcardPattern() && this.isWildcard(this.getShowCardIdList()[0]);
            }

            // isWildcardPattern()
            // {
            //     if(this.isWCP != null)
            //         return this.isWCP;
            //
            //     this.isWCP = false;
            //     var showIdList = this.getShowCardIdList();
            //     for(var i = 0; i < showIdList.length; ++i)
            //     {
            //         var cardId = showIdList[i];
            //         if(cardId[1] == "w" && !rfaw.utils.isWildcard(cardId))
            //         {
            //             this.isWCP = true;
            //             break;
            //         }
            //     }
            //     return this.isWCP;
            // }

            // greaterThan(card)
            // {
            //     var isWcSelf = this.isWildcardPattern();
            //     var isWcCard = card.isWildcardPattern();
            //
            //     if( isWcSelf == isWcCard ||
            //         rfaw.classicUtils.getCardNumber(card.getKeyValue()) != rfaw.classicUtils.getCardNumber(this.getKeyValue()))
            //     {
            //         return this._super(card);
            //     }
            //
            //     return !isWcSelf
            // }

            // getKeyValue()
            // {
            //
            // }
        }

        export class Bomb extends BaseCardPattern {
            constructor(cardIdList, wcValueList, showCardIdList) {
                super(rfa.CARD_TYPE.BOMB, cardIdList, cardIdList[3], wcValueList, showCardIdList)
            }

            // setData:function(cardIdList, keyValue)
            // {
            //     this._super(cardIdList, keyValue);
            //     if(this.isWildcard(cardIdList[0]) && !this.isWildcard(cardIdList[3]))
            //     {
            //         this.keyValue = cardIdList[3];
            //         this.isWildcardBomb = true;
            //     }
            //     else if(cardIdList[0].charAt(1) == "w")
            //     {
            //         this.isWildcardBomb = true;
            //     }
            //     this.isWildcardBomb = this.isWildcardPattern();
            // },

            greaterThan(card) {
                if (card.getType() != rfa.CARD_TYPE.BOMB)
                    return true;

                var priority = 0;
                if (this.isAllWildcardPattern())
                    priority = 2;
                else if (!this.isWildcardPattern())
                    priority = 1;

                var CardPriority = 0;
                if (card.isAllWildcardPattern())
                    CardPriority = 2;
                else if (!card.isWildcardPattern())
                    CardPriority = 1;

                if (priority > CardPriority)
                    return true;
                else if (priority == CardPriority && rfaw.classicUtils.getCardNumber(this.getKeyValue()) > rfaw.classicUtils.getCardNumber(card.getKeyValue()))
                    return true;

                return false;
            }
        }
    }

}