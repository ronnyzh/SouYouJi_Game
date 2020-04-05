# -*- coding: utf-8 -*-
# ----------------------------------------- (接口)

###########################    # ·与本模块通信, 请先阅读本接口。
# CLIENT INTERFACE        #    # ·服务器与客户端的通信协议
###########################    #   请尽量遵守本约定。


## 一、约定: ID MAPPING
## (ID 号与纸牌花色的关系)

# UPGRADE WARNING: 牌与 ID 的映射可能会发生改变
#

## 约定的具体内容
# *** 1) 3-10 为 3-10 的数字牌
# *** 2) 11、12、13 分别为 J、Q、K
# *** 3) 14 为 A; 15 为 2
# *** 4) 16 为小王; 17 为大王

# 这里没有采用 "宏" 定义的方法来维护 ID 与纸牌大小的映射。
# 在这个程序的复杂度中 "宏" 显得毫无意义, 是一种无谓封装。
# 首先这是一个资源内敛的模块, 不准备与其他程序发生复杂的联系。
# 而在玩法升级中, 整个程序不可避免地会被大量修改
# 同样 ID 映射也会受到毁灭性的修改。
# 在这种变动中, 本来显得稳定的 ID 宏映射将变成一种负担
# -- 起码, 维护的东西越多, 我们将更容易发生错误。
# 这里, 我们将使用注释和约定来维护这个映射。


## 二、本模块的调用接口
## (使用方法请见最后单元测试部分)
#
## CardsModelFactory 函数

# 用例:
# >>> cards_model1 = CardsModelFactory( [0,4,8,12,16] ) # 顺子
# >>> cards_model2 = CardsModelFactory( [52,53] )     # 火箭
# >>> print cards_model2 > cards_model1
# 结果为(True)
# >>> cards_model = CardsModelFactory( [2] )
# 得到异常(SIG_WRONGCARD) 注: 3-17 为取值范围
# >>> cards_model = CardsModelFactory( [3, 9] )
# 得到异常(SIG_RULECONFLICT)


## 三、信号定义
## (及相关工具函数)
class SIG_WRONGCARD   : pass # 无效牌
class SIG_RULECONFLICT: pass # 与规则冲突

# ----------------------------------------- (牌型)

LITTLE_JOKER_CARD_NUM = 52
PEFECT_CARD_BASE_NUM = 54


chars = ("J".decode('utf-8'),"Q".decode('utf-8'),"K".decode('utf-8'), \
    "A".decode('utf-8'),"2".decode('utf-8'),"小王".decode('utf-8'), "大王".decode('utf-8'))
def get_card_string_from_number(num):
    if num <= 10:
        return str(num)
    else:
        return chars[num-11]

def useWildCard(cards, wildCards):
    if not wildCards:
        print 'no wildCards'
        return cards

    lenWild = len(wildCards)
    if not cards and wildCards:
        wild2Card = wildCards[0]
        print '1wild2Card, lenWild', wild2Card, lenWild
        return [wild2Card]*lenWild

    lenCard = len(cards)
    cardSet = set(cards)
    lenCardSet = len(cardSet)
    lenTotalCard = lenWild + lenCard
    if lenCardSet == 1 and lenTotalCard <= 4:
        wild2Card = cards[0]
        print '2wild2Card, lenWild', wild2Card, lenWild
        return [wild2Card]*lenWild

    count2Card = {1:[], 2:[], 3:[], 4:[]}
    for val in cardSet:
        valCount = cards.count(val)
        if valCount+lenWild >= 4:
            print 'have bomb'
            return []
        count2Card[valCount].append(val)

    l1 = count2Card[1]
    l2 = count2Card[2]
    lenL1 = len(l1)
    lenL2 = len(l2)
    l1.sort()
    l2.sort()
    if lenTotalCard in [4, 5]:
        if (lenL2 == lenL1 == 1) or (lenL2+lenL1 == lenL2 == 2):
            wild2Card = l2[-1]
            print '3wild2Card, lenWild', wild2Card, lenWild
            return [wild2Card]*lenWild
        if lenL1+lenL2 == lenL1 == 2:
            wild2Card = l1[-1]
            print '4wild2Card, lenWild', wild2Card, lenWild
            return [wild2Card]*lenWild

    if l2 and lenTotalCard >= 6 and lenTotalCard%2==0 and lenL1 == 1:
        jointList = l1[:]
        jointList.extend(l2)
        jointList.sort()
        isJoint = is_joint(jointList)
        if isJoint:
            wild2Card = l1[-1]
            print '5wild2Card, lenWild', wild2Card, lenWild
            return [wild2Card]*lenWild

    if not l2 and lenTotalCard >= 5 and lenTotalCard <= 12:
        maxL1 = max(l1)
        if maxL1 > 14:
            print 'val[%s] out of range'%(maxL1)
            return []
        minCard = min(l1)
        maxCard = minCard + lenTotalCard -1
        overstepVal = maxCard - 14
        if overstepVal > 0:
            minCard -= overstepVal
            maxCard = 14
        jointList = xrange(minCard, maxCard+1)
        if not (set(l1) <= set(jointList)):
            print 'val out of range'
            return []
        useWildList = []
        for val in jointList:
            if val not in l1:
                wild2Card = val
                useWildList.append(wild2Card)
        print 'useWildList', useWildList
        return useWildList
    return []

def joint_end_idx(cards):
    # cards has been sorted
    assert cards, "%s is empty"%cards
    _len = len(cards)
    if _len == 1:
        return (0, 1)
    _first = 0
    _tmp_first = 0
    _tmp_len = 1
    _real_len = 1
    for i in xrange(_len - 1):
        if cards[i]+1 > 14:
            break
        if cards[i]+1 != cards[i+1]:
            if _real_len > _tmp_len:
                _tmp_len = _real_len
                _tmp_first = _first
            _first = i + 1
            _real_len = 1
        else:
            _real_len += 1
    if _real_len > _tmp_len:
        _tmp_len = _real_len
        _tmp_first = _first
    return (_tmp_first, _tmp_len)

def is_joint(cards):
    # cards has been sorted
    if not cards:
        return False
    if len(cards) == 1:
        return True
    if cards[-1] > 14:
        return False
    return cards[0] + len(cards) - 1 == cards[-1]

# 牌型工厂
def CardsModelFactory(cards, useWildCard = [], deck = 1):
    """
    cards:牌值列表
    useWildCard:使用的万能牌
    deck:多少副牌
    """
    if not cards:
        return CardsInvalid()
    # tmp = [get_number_from_card_id(card) for card in cards]
    tmp = cards
    tmp.sort()
    _len = len(tmp)
    # print 'aaaaaa2',tmp

    # 判断牌号是否合法
    # UPGRADE WARNING: 新玩法可能会修改牌值范围
    # 3-17 为合法范围, 否则返回无效牌型
    if tmp[0] < 3 or tmp[-1] > 17:
        return CardsInvalid()

    if 16 in tmp and 17 in tmp:
        if _len == deck*2 and tmp.count(16) == tmp.count(17) == deck:
            return Rocket()

    if len(useWildCard) == _len >= 4:
        # return MixBomb(tmp[0], _len)
        return HardBomb(tmp[0])

    if _len == 1: return SingleJoint(tmp[0])

    skipstep = 0
    """
    l1-l5,分别统计1-4，及大于4张以上牌的牌ID
    """
    l5 = []
    l4 = []
    l3 = []
    l2 = []
    l1 = []

    for i in xrange(_len):
        if skipstep > 0:
            skipstep -= 1
            continue
        _count = tmp.count(tmp[i])
        if _count > 4:
            l5.append((tmp[i], _count))
        elif _count == 4:
            l4.append(tmp[i])
        elif _count == 3:
            l3.append(tmp[i])
        elif _count == 2:
            l2.append(tmp[i])
        else:
            l1.append(tmp[i])
        skipstep = _count - 1

    # print 'lllll',l1,l2,l3,l4,l5
    if l5:
        if len(l5) == 1 and not l4 and not l3 and not l2 and not l1:
            card = l5[0][0]; _num = l5[0][1]
            if deck > 1 and not useWildCard:
                return HardBomb(card, _num)
            # if useWildCard:
                # return SoftBomb(card, _num)
        return CardsInvalid()

    if l4:
        if len(l4) == 1:
            if not l3 and not l2 and not l1:
                if not useWildCard:
                    return HardBomb(l4[0])
                else:
                    return SoftBomb(l4[0])
            # if not l3 and not l1 and len(l2)==2:
            #     return QuadrupleWithPair(l4[0])
            if not l3 and (len(l1) + (len(l2)<<1))==2:
                return QuadrupleWithSingle(l4[0])
        # if len(l4) == 2 and not l3 and not l2 and not l1:
        #     return QuadrupleWithPair(l4[-1])
        # return CardsInvalid()

    if l3:
        if l4:
            l2.extend(l4*2)
        l3_len = len(l3)
        l1_len = len(l1); l2_len = len(l2)
        _is_joint = is_joint(l3)
        
        print '_is_joint:',_is_joint
        print 'l3_len:',l3_len
        print 'l2_len:',l2_len
        print 'l1_len:',l1_len
        
        if _is_joint and not l1_len and not l2_len:
            return TripleJoint(l3[0], l3_len, useWildCard)
        
        if _is_joint and not l1_len and l2_len == l3_len:
            return AerocraftWithPair(l3[0], l3_len, useWildCard)
        if deck > 1:
            return CardsInvalid()

        if l4:
            l2 = [i for i in l2 if i not in l4]
            l3.extend(l4)
            l1.extend(l4)
            l3.sort()
            l3_len = len(l3)
            l1_len = len(l1); l2_len = len(l2)
        (_joint_begin, _joint_len) = joint_end_idx(l3)
        print 'joint_end_idx:',joint_end_idx(l3)
        while _joint_len > 0:
            reduce = l3_len - _joint_len
            print 'reduce:',reduce
            if (l1_len + (l2_len*2) + reduce*3) == _joint_len:
                return AerocraftWithSingle(l3[0], _joint_len, useWildCard)
            _joint_len -= 1
        return CardsInvalid()

    if l4:
        return CardsInvalid()

    if l2:
        l2_len = len(l2)
        if not l1 and (l2_len == 1 or l2_len > 2) and is_joint(l2):
            return PairJoint(l2[0], l2_len, useWildCard)

        return CardsInvalid()

    l1_len = len(l1)
    if is_joint(l1) and l1_len >= 5:
        return SingleJoint(l1[0], l1_len, useWildCard)

    return CardsInvalid()

INVALID_PATTERN             =   0
SINGLE_PATTERN              =   1
SINGLE_JOINT_PATTERN            =   2
PAIR_PATTERN                =   3
PAIR_JOINT_PATTERN          =   4
TRIPLE_PATTERN              =   5
TRIPLE_JOINT_PATTERN            =   6
TRIPLE_WITH_SINGLE_PATTERN      =   7
TRIPLE_WITH_SINGLE_JOINT_PATTERN    =   8
TRIPLE_WITH_PAIR_PATTERN        =   9
TRIPLE_WITH_PAIR_JOINT_PATTERN      =   10
QUADRUPLE_WITH_SINGLE_PATTERN       =   11
QUADRUPLE_WITH_PAIR_PATTERN     =   12
HARD_BOMB_PATTERN           =   13
SOFT_BOMB_PATTERN           =   14
MIX_BOMB_PATTERN            =   15
ROCKET_PATTERN              =   16

PATTERN_BOMB = ( HARD_BOMB_PATTERN, SOFT_BOMB_PATTERN, MIX_BOMB_PATTERN )
PATTERN_JOINT = (SINGLE_JOINT_PATTERN, \
    PAIR_JOINT_PATTERN, TRIPLE_JOINT_PATTERN, \
    QUADRUPLE_WITH_PAIR_PATTERN, QUADRUPLE_WITH_SINGLE_PATTERN )

PATTERN_AEROCRAFT = (TRIPLE_WITH_SINGLE_JOINT_PATTERN, TRIPLE_WITH_PAIR_JOINT_PATTERN, )
PATTERN_QUADRUPLE = (QUADRUPLE_WITH_SINGLE_PATTERN, QUADRUPLE_WITH_PAIR_PATTERN )

pattern_texts = { \
    INVALID_PATTERN             :   "无效牌".decode('utf-8'), \
    SINGLE_PATTERN              :   "单牌".decode('utf-8'), \
    SINGLE_JOINT_PATTERN            :   "单顺".decode('utf-8'), \
    PAIR_PATTERN                :   "对子".decode('utf-8'), \
    PAIR_JOINT_PATTERN          :   "双顺".decode('utf-8'), \
    TRIPLE_PATTERN              :   "三张".decode('utf-8'), \
    TRIPLE_JOINT_PATTERN            :   "三顺".decode('utf-8'), \
    TRIPLE_WITH_SINGLE_PATTERN      :   "三带一".decode('utf-8'), \
    TRIPLE_WITH_SINGLE_JOINT_PATTERN    :   "三顺带单".decode('utf-8'), \
    TRIPLE_WITH_PAIR_PATTERN        :   "三带二".decode('utf-8'), \
    TRIPLE_WITH_PAIR_JOINT_PATTERN      :   "飞机（三顺带二）".decode('utf-8'), \
    QUADRUPLE_WITH_SINGLE_PATTERN       :   "四带二".decode('utf-8'), \
    QUADRUPLE_WITH_PAIR_PATTERN     :   "四带二对".decode('utf-8'), \
    HARD_BOMB_PATTERN           :   "炸弹".decode('utf-8'), \
    SOFT_BOMB_PATTERN           :   "软炸弹".decode('utf-8'), \
    MIX_BOMB_PATTERN            :   "混炸弹".decode('utf-8'), \
    ROCKET_PATTERN              :   "火箭".decode('utf-8'), \
}

# 牌型基类 (Also MixIn)
# 生成 __lt__ "<" 和 __eq__ "==" 的操作
# 注意 "==" 在游戏逻辑中是毫无意义的(包括升级逻辑中), 永远返回 False。
# 子类需要定义 __gt__ ">" 操作
# 注意 "==" 及 "<" 比较的实现是相当耗费程序效率的!
class CardsModel:
    ## ">"
    #def __gt__(self, m): pass

    # "=="
    def __eq__(self, m): return False
    # "<"
    def __lt__(self, m): return not self.__gt__(m)
    def __repr__(self):
        return pattern_texts[self.get_pattern()] + ('%s'%(get_card_string_from_number(self.c)) if hasattr(self, 'c') else '')
    __str__ = __repr__
    def get_pattern(self):
        raise "abstract interface"

    def is_invalid(self):
        return self.get_pattern() == INVALID_PATTERN

    def is_big(self):
        return True

    def is_bomb(self):
        return self.get_pattern() in PATTERN_BOMB

    def is_joint(self):
        return self.get_pattern() in PATTERN_JOINT

    def is_rocket(self):
        return self.get_pattern() == ROCKET_PATTERN
        
    def is_aerocraft(self):
        return self.get_pattern() in PATTERN_AEROCRAFT


class CardsInvalid(CardsModel):
    def __gt__(self, m):
        return False
    def is_big(self):
        return False
    def get_pattern(self):
        return INVALID_PATTERN

class Rocket(CardsModel):
    def __gt__(self, m):
        return not isinstance(m, Rocket)
    def get_pattern(self):
        return ROCKET_PATTERN

class MixBomb(CardsModel):
    def __init__(self, c, n = 4):
        self.c = c
        self.n = n
    def __gt__(self, m):
        return not isinstance(m, Rocket) and \
            not (isinstance(m, MixBomb) and self.n < m.n) and \
            not (isinstance(m, SoftBomb) and self.n < m.n)
    def get_pattern(self):
        return MIX_BOMB_PATTERN
    def get_value(self):
        return self.c

class HardBomb(CardsModel):
    def __init__(self, c, n = 4):
        self.c = c
        self.n = n
    def __gt__(self, m):
        return not isinstance(m, Rocket) and \
            not (isinstance(m, MixBomb) and self.n <= m.n) and \
            not (isinstance(m, HardBomb) and (self.n < m.n or (self.n == m.n and self.c < m.c))) and \
            not (isinstance(m, SoftBomb) and self.n < m.n)

    def get_pattern(self):
        return HARD_BOMB_PATTERN
    def get_value(self):
        return self.c

class SoftBomb(CardsModel):
    def __init__(self, c, n = 4):
        self.c = c
        self.n = n

    def __gt__(self, m):
        return not isinstance(m, Rocket) and \
            not (isinstance(m, MixBomb) and self.n <= m.n) and \
            not (isinstance(m, HardBomb) and self.n <= m.n) and \
            not (isinstance(m, SoftBomb) and (self.n < m.n or (self.n == m.n and self.c < m.c)))

    def get_pattern(self):
        return SOFT_BOMB_PATTERN
    def get_value(self):
        return self.c
    def get_count(self):
        return self.n

# 炸弹 (Bomb)
# 注意: 火箭 (Rocket) 被认为是 c 值为 '\x11' (17 大王的 ID ) 的炸弹

# 顺子 (SingelJoint)
# 注意: 单牌 (Singel) 被认为是 n 为 1 的顺子
class SingleJoint(CardsModel):
    def __init__(self, c, n=1, useWild=False):
        self.c = c
        self.n = n
        self.useWild = useWild
    def __gt__(self, m):
        return isinstance(m, SingleJoint) and self.n == m.n and \
                 (self.c > m.c or (self.n > 1 and self.c == m.c and not self.useWild and m.useWild))
    def is_big(self):
        if self.n == 1:
            return self.c == 17
        else:
            return self.c + self.n == 15
    def get_pattern(self):
        if self.n == 1:
            return SINGLE_PATTERN
        return SINGLE_JOINT_PATTERN
    def get_value(self):
        return self.c
    def get_count(self):
        return self.n
    def get_use_wild(self):
        return self.useWild
# 连对 (PairJoint)
# 注意: 对牌 (Pair) 被认为是 n 为 1 的顺子
class PairJoint(CardsModel):
    def __init__(self, c, n=1, useWild=False):
        self.c = c
        self.n = n
        self.useWild = useWild
    def __gt__(self, m):
        return isinstance(m, PairJoint) and self.n == m.n and \
                (self.c > m.c or (self.c == m.c and not self.useWild and m.useWild))
    def is_big(self):
        if self.n == 1:
            return self.c > 14
        return True
    def get_pattern(self):
        if self.n == 1:
            return PAIR_PATTERN
        return PAIR_JOINT_PATTERN
    def get_value(self):
        return self.c
    def get_count(self):
        return self.n
    def get_use_wild(self):
        return self.useWild
# 三顺 (TripleJoint)
# 注意: 三张牌 (Triple) 被认为是 n 为 1 的顺子
class TripleJoint(CardsModel):
    def __init__(self, c, n=1, useWild=False):
        self.c = c
        self.n = n
        self.useWild = useWild
    def __gt__(self, m):
        return isinstance(m, TripleJoint) and self.n == m.n and \
                (self.c > m.c or (self.c == m.c and not self.useWild))
    def is_big(self):
        if self.n == 1:
            return self.c > 13
        return True
    def get_pattern(self):
        if self.n == 1:
            return TRIPLE_PATTERN
        return TRIPLE_JOINT_PATTERN
    def get_value(self):
        return self.c
    def get_count(self):
        return self.n
    def get_use_wild(self):
        return self.useWild

# 飞机带翅膀 (单牌) (AerocraftWithSingle)
# 对玩家的善意提醒:
#  在三顺中带单牌, 包含了两个单数形态,
#  在美学上是相当不对称、不稳定的。
#  而双数的对称美给人带来平和与宁静。
#  长期玩斗地主, 这条规则, 其带来的视觉
#  效果将会给玩家带来生理上的不适 (不可自控)。
#  造成精神紧张, 审美能力下降, 神经衰弱
#  及心理阴影和性格扭曲。请玩家慎重, 切切。
# 注意: 三带一 (单牌) 是飞机带翅膀的一种 (n = 1)。
class AerocraftWithSingle(CardsModel):
    def __init__(self, c, n=1, useWild=False):
        self.c = c
        self.n = n
        self.useWild = useWild
    def __gt__(self, m):
        return isinstance(m, AerocraftWithSingle) and self.n == m.n and \
                (self.c > m.c or (self.c == m.c and not self.useWild))
    def is_big(self):
        if self.n == 1:
            return self.c > 13
        return True
    def get_pattern(self):
        if self.n == 1:
            return TRIPLE_WITH_SINGLE_PATTERN
        return TRIPLE_WITH_SINGLE_JOINT_PATTERN
    def get_value(self):
        return self.c
    def get_count(self):
        return self.n
    def get_use_wild(self):
        return self.useWild
# 飞机带翅膀 (对子) (AerocraftWithPair)
# 注意: 三带一 (对子) 是愚蠢的飞机带翅膀, 其中一种 (n = 1)。
class AerocraftWithPair(CardsModel):
    def __init__(self, c, n=1, useWild=False):
        self.c = c
        self.n = n
        self.useWild = useWild
    def __gt__(self, m):
        return isinstance(m, AerocraftWithPair) and self.n == m.n and \
                (self.c > m.c or (self.c == m.c and not self.useWild))
    def is_big(self):
        if self.n == 1:
            return self.c > 13
        return True
    def get_pattern(self):
        if self.n == 1:
            return TRIPLE_WITH_PAIR_PATTERN
        return TRIPLE_WITH_PAIR_JOINT_PATTERN
    def get_value(self):
        return self.c
    def get_count(self):
        return self.n
    def get_use_wild(self):
        return self.useWild
# 四带二 (单牌) (QuadrupleWithSingle)
class QuadrupleWithSingle(CardsModel):
    def __init__(self, c): self.c = c
    def __gt__(self, m):
        return isinstance(m, QuadrupleWithSingle) and self.c > m.c
    def get_pattern(self):
        return QUADRUPLE_WITH_SINGLE_PATTERN
    def get_value(self):
        return self.c
# 四带二 (对子) (QuadrupleWithPair)
class QuadrupleWithPair(CardsModel):
    def __init__(self, c): self.c = c
    def __gt__(self, m):
        return isinstance(m, QuadrupleWithPair) and self.c > m.c
    def get_pattern(self):
        return QUADRUPLE_WITH_PAIR_PATTERN
    def get_value(self):
        return self.c








# ----------------------------------------- (测试)
if __name__ == '__main__':
    # 编码系统改动
    import sys
    oldencoding = sys.getdefaultencoding()
    encoding = sys.getfilesystemencoding()
    if oldencoding != encoding:
        print 'Modify encoding : ', oldencoding, ' --> ', encoding
        reload(sys)
        sys.setdefaultencoding(encoding)
        print u'配置成功'


    # 这里使用轻量级的测试方案
    print u"LordSiege 模块单元测试"

    print u"取值判断, 取值区域为 [3-17]"
    for i in xrange(20):
        try:
            print "CardsModelFactory([%d]):" %i, CardsModelFactory([i])
        except SIG_WRONGCARD, e:
            print "SIG_WRONGCARD"
    # print

    # print u"单牌、顺子"
    # try:
        # print "CardsModelFactory([0,4,8,12,16]):", CardsModelFactory([0,4,8,12,16])
    # except SIG_RULECONFLICT, e:
        # print "SIG_RULECONFLICT"
    # try:
        # print "CardsModelFactory([0,4,8,8,16]):", CardsModelFactory([0,4,8,8,16])
    # except SIG_RULECONFLICT, e:
        # print "SIG_RULECONFLICT"
    # print "CardsModelFactory([4,8,12,16,20]) > CardsModelFactory([0,4,8,12,16]):",
    # print CardsModelFactory([4,8,12,16,20]) > CardsModelFactory([0,4,8,12,16])
    # print "CardsModelFactory([4,8,12,16,20,24]) > CardsModelFactory([0,4,8,12,16]):",
    # print CardsModelFactory([4,8,12,16,20,24]) > CardsModelFactory([0,4,8,12,16])
    # print "CardsModelFactory([0,4,8,12,16]) > CardsModelFactory([4,8,12,16,20]):",
    # print CardsModelFactory([0,4,8,12,16]) > CardsModelFactory([4,8,12,16,20])
    print CardsModelFactory([3,4,5,6,7])
    print CardsModelFactory([3,3,3,6,6])
    print CardsModelFactory([3,3,3,6])
    print CardsModelFactory([3,3,3])
    print CardsModelFactory([3,4,5,6,3,3,4,4])
    print CardsModelFactory([3,4,5,6,3,3,4,4,5])
    print CardsModelFactory([15,15])
    print CardsModelFactory([15,15,15])
    print CardsModelFactory([3,3,3,4,4,4,5,5,5,6,6,6])
    print CardsModelFactory([3,4,5])
    print CardsModelFactory([8,8,8,8]) > CardsModelFactory([3,4,5,6,7])
    print CardsModelFactory([3,4,5,6,7]) > CardsModelFactory([8,8,8,8])
    # print CardsModelFactory([6,6,5,6,5]) > CardsModelFactory([4,4,4,6])
    
    # print CardsModelFactory([15,15,3])
    # print CardsModelFactory([15,15]) > CardsModelFactory([10,10])

    print useWildCard([3,4,4], ['w'])
    print useWildCard([3,3,4,4], ['w'])
    print useWildCard([3,4], ['w','w'])
    print useWildCard([3,4], ['w','w','w'])
    print useWildCard([3,4,7], ['w','w'])
    print useWildCard([10,11,12,13], ['w','w'])
    print useWildCard([10,11], ['w','w','w','w'])
    print useWildCard([], ['3a','3b','3c'])
    print useWildCard([12,13,14,15], ['3a','3b'])
    # print useWildCard([10,10,11,11,12,12,13], ['w'])


    # 待完成