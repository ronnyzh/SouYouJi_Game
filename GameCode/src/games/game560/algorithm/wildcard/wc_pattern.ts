module G560{
    export namespace flaw {
        export class BaseCardPattern extends fla.BaseCard {
            public wcValueList;
            public showCardIdList;
            public cardIdList;

            constructor(type, data, keyValue?, wcValueList?, showCardIdList?) {
                super(type, data, keyValue);
                this.wcValueList = wcValueList;
                this.showCardIdList = showCardIdList;
            }

            isWildcard(cardId) {
                return fla.utils.isWildcard(cardId);
            }

            getShowCardIdList() {
                return (this.showCardIdList || this.cardIdList).concat();
            }

            getActionData() {
                var data = [this.cardIdList.join(",")];
                if (this.wcValueList != null) {
                    jx.each(this.wcValueList, function (cardId, i) {
                        this.wcValueList[i] = fla.utils.transferWildCardTo(cardId);
                    }, this);
                    data.push(this.wcValueList.join(","));
                }
                return data;
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
            //         if(cardId[1] == "w" && !flaw.utils.isWildcard(cardId))
            //         {
            //             this.isWCP = true;
            //             break;
            //         }
            //     }
            //     return this.isWCP;
            // }

            greaterThan(card)
            {
                var isWcSelf = this.isWildcardPattern();
                var isWcCard = card.isWildcardPattern();

                if( isWcSelf == isWcCard ||
                    flaw.classicUtils.getCardNumber(card.getKeyValue()) != flaw.classicUtils.getCardNumber(this.getKeyValue()))
                {
                    return super.greaterThan(card);
                }

                return !isWcSelf
            }

            // getKeyValue()
            // {
            //
            // }
        }

        export class Bomb extends BaseCardPattern {
            constructor(cardIdList, wcValueList, showCardIdList) {
                super(fla.CARD_TYPE.BOMB, cardIdList, cardIdList[3], wcValueList, showCardIdList)
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

            greaterThan(card)
            {
                var isWildcardPattern = this.isWildcardPattern();
                if(card.getType() == fla.CARD_TYPE.ROCKET)
                    return false;

                else if(card.getType() != fla.CARD_TYPE.BOMB)
                    return true;

                if(isWildcardPattern == card.isWildcardPattern())
                    return flaw.classicUtils.getCardNumber(this.getKeyValue()) > flaw.classicUtils.getCardNumber(card.getKeyValue());

                return !isWildcardPattern;
            }
        }
    }

}