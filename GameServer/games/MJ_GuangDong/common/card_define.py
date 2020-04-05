# -*- coding:utf-8 -*-
#!/bin/python

CHARACTER = 'a' #万
DOT = 'b' #桶
BAMBOO = 'c' #条
DRAGON = 'd' #箭牌
WIND = 'e' #风牌
FLOWER = 'f' #花朵牌
SEASON = 'g' #季节牌
MAHJONG_TYPE_LIST =[CHARACTER, DOT, BAMBOO]
HONOR_TYPE_LIST =[DRAGON, WIND] #字牌
SPECIAL_TYPE_LIST = [FLOWER, SEASON] #花牌
ALL_TYPE_LIST = [CHARACTER, DOT, BAMBOO, DRAGON, WIND, FLOWER, SEASON]

RED = 'd1' #中
WHITE = 'd5' #白
GREEN = 'd9' #发

EAST = 'e1' #东
SOUTH = 'e4' #南
WEST = 'e6' #西
NORTH = 'e9' #北

PLUM = 'f1' #梅
ORCHID = 'f4' #兰
CHRYSANTHEMUM = 'f6' #菊
BAMBOO1 = 'f9' #竹

SPRING = 'g1' #春
SUMMER = 'g4' #夏
AUTUMN = 'g6' #秋
WINTER = 'g9' #冬

HONOR_TILES = [RED, WHITE, GREEN, EAST, WEST, SOUTH, NORTH]
WIND_TILES = [EAST, SOUTH, WEST, NORTH]
FLOWER_TILES = [PLUM, ORCHID, BAMBOO1, CHRYSANTHEMUM, SPRING, SUMMER, AUTUMN, WINTER]
FLOWER_SEASON_TILES = [SPRING,SUMMER,AUTUMN,WINTER]
FLOWER_FLOWER_TILES = [PLUM,ORCHID,CHRYSANTHEMUM,BAMBOO1]
FLOWER_SEASON_TILES_SET = set(FLOWER_SEASON_TILES)
FLOWER_FLOWER_TILES_SET = set(FLOWER_FLOWER_TILES)
FLOWER_TILES_SET = set(FLOWER_TILES)
HONOR_TILES_SET = set(HONOR_TILES)
SPECIAL_TILES = FLOWER_TILES_SET | HONOR_TILES_SET
DRAGON_TILES = [RED, WHITE, GREEN]

#碰杠牌编号
NOT_GET = 0 #不要牌
CHOW = 1 #吃
PONG = 2 #碰
OTHERS_KONG = 3 #其他人打出来的杠
SELF_KONG = 4 #自己摸到的杠
CONCEALED_KONG = 5 #暗杠
HU = 6 #胡

MAX_MAHJONG_NUM = 9 #每个类型的种类数
MAX_REPEAT_COUNT = 4 #最大重复张数
MIN_REPEAT_COUNT = 1 #最小重复张数
TRIPLET_NUM = 3 #刻子张数
EYE_NUM = 2 #眼张数
PRIVAET_MAHJONG_NUM = 13 #初始手牌数
MAHJONG_TYPE_COUNT = 3 #麻将类型数

def _getMahjongList():
    mahjongList = []
    for mahjongCount in xrange(MAX_REPEAT_COUNT):
        for type in MAHJONG_TYPE_LIST:
            for num in xrange(MAX_MAHJONG_NUM):
                mahjongList.append('%s%s'%(type, num+1))
    return mahjongList

MAHJONG_LIST = _getMahjongList() #牌列表（万桶条），每种四张

def _getAllTiles():
    mahjongList = []
    for type in MAHJONG_TYPE_LIST:
        for num in xrange(MAX_MAHJONG_NUM):
            mahjongList.append('%s%s'%(type, num+1))
    return mahjongList

ALL_TILES = _getAllTiles() #所有的牌（万桶条），每种一张

def getTileType(tile):
    '''
    获得牌类型
    '''
    try:
        type = tile[0]
    except:
        return ''
    if type in ALL_TYPE_LIST:
        return type
    return ''

def getTilePoints(tile):
    '''
    获得牌点数
    '''
    try:
        points = int(tile[1])
    except:
        return 0
    type = getTileType(tile)
    if type in MAHJONG_TYPE_LIST:
        return points
    return 0

def packTile4TypeNPoints(type, points):
    '''
    由牌类型和点数获得对应的牌
    '''
    return type + str(points)

def getTripeleList(tiles, type, tripeleList = []): #返回成牌列表
    if not tiles:
        return tripeleList

    firstTile = tiles[0]
    firstTilePoints = getTilePoints(firstTile)
    if tiles.count(firstTile) >= TRIPLET_NUM: #刻子
        tripeleList.append([firstTile, firstTile, firstTile])
        return getTripeleList(tiles[3:], type, tripeleList)
    elif type in MAHJONG_TYPE_LIST:
        secondTile = packTile4TypeNPoints(type, firstTilePoints + 1)
        thirdTile = packTile4TypeNPoints(type, firstTilePoints + 2)
        if set([firstTile, secondTile, thirdTile]).issubset(set(tiles)):  #顺子
            testTiles = tiles[1:]
            testTiles.remove(secondTile)
            testTiles.remove(thirdTile)
            tripeleList.append([firstTile, secondTile, thirdTile])
            return getTripeleList(testTiles, type, tripeleList)
    return []

def getTripleListNEye4Type(tiles, type): #某类型的牌的成牌列表
    if not tiles:
        return tiles, None

    tiles.sort()
    tilesLen = len(tiles)
    overTileCount = tilesLen % TRIPLET_NUM
    if overTileCount == EYE_NUM:
        needEye = True
    else:
        needEye = False

    if needEye:
        canBeEyeList = []
        tileSet = set(tiles)
        for tile in tileSet:
            if tiles.count(tile) >= EYE_NUM:
                canBeEyeList.append(tile)
        for eye in canBeEyeList:
            testTiles = tiles[:]
            for i in xrange(EYE_NUM):
                testTiles.remove(eye)
            if not testTiles:
                return [], eye
            tripeleList = getTripeleList(testTiles, type)
            if tripeleList:
                return tripeleList, eye
        return [], None
    else:
        return getTripeleList(tiles, type), None

def getTripleListNEye(type2tilesDict): #胡牌后调用，可获得成牌列表和眼
    tripleTiles = []
    eye = None
    for type, tiles in type2tilesDict.iteritems():
        tripleTiles4Type, getEye = getTripleListNEye4Type(tiles, type)
        tripleTiles.extend(tripleTiles4Type)
        if getEye:
            eye = getEye
    return tripleTiles, eye

