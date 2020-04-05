class HuAlgorithm {
    // private static _inst: HuAlgorithm = null;
    // public static get inst(): HuAlgorithm {
    //     if (HuAlgorithm._inst == null) {
    //         HuAlgorithm._inst = new HuAlgorithm();
    //     }
    //     return HuAlgorithm._inst;
    // }

    static createHuAlgorithm() {
        return new HuAlgorithm();
    }

    private tingMap: { [key: string]: string[] };
    private isUseServer: boolean;
    private isUseFancyTile: boolean;
    private ghostList: string[];
    private allId: string[];

    constructor() {
        this.tingMap = {};
        this.isUseServer = false;
        this.isUseFancyTile = false;
        this.ghostList = [];
        this.allId = [];
        this.initIdPool();
    }

    initIdPool() {
        let allId = [];
        if (this.haveWan()) {
            for (let i = 1; i < 10; i++) {
                allId.push("a" + i);
            }
        }
        if (this.haveTong()) {
            for (let i = 1; i < 10; i++) {
                allId.push("b" + i);
            }
        }
        if (this.haveTiao()) {
            for (let i = 1; i < 10; i++) {
                allId.push("c" + i);
            }
        }
        if (this.haveWind()) {
            allId.push("d1");
            allId.push("d5");
            allId.push("d9");
            allId.push("e1");
            allId.push("e4");
            allId.push("e6");
            allId.push("e9");
        }
        allId.sort();
        this.allId = allId;
    }

    haveWind() {
        return true
    }

    haveWan() {
        return true
    }

    haveTong() {
        return true
    }

    haveTiao() {
        return true
    }

    tryMarkTile(testId: string, handWallTileDataList: string[]) {
        let idList = this.getHandTileIdList(testId, handWallTileDataList);
        let value = this.tingMap[idList.join(",")];
        if (value) {//有值，直接显示
            return value;
            //this.delegate.markTile(testId);
        } else if (testId) {
            this.useClientOrServer(testId, handWallTileDataList);
        }
    }

    getReadyHandTiles(testId: string, handTileDataList: string[]) {
        let newHandTileDataList = handTileDataList.concat();
        let idList = this.getHandTileIdList(testId, newHandTileDataList);
        let idStr = idList.join(",");
        let value = this.tingMap[idStr];
        if (value && value.length != 0) {
            return value;
        }
        else {
            let obj = this.useClientOrServer(testId, newHandTileDataList);
            return obj;
        }
    }

    setServer(bool: boolean) {
        this.setIsUseServer(bool);
    }

    setIsUseServer(bool: boolean) {
        this.isUseServer = !!bool;
    }

    setIsUseFancyTile(bool: boolean) {
        this.isUseFancyTile = !!bool;
    }

    /**
     * 有特殊玩法，重写该
     * @returns {boolean}
     */
    isMeetTheSpecialCondition(testIdList, newIdCountList, newTestGhostList) {
        return true;
    }

    /**
     * 有特殊玩法，重写该
     * @returns {boolean}
     */
    isSpecialHu(testIdList, newIdCountList, newTestGhostList) {
        return false;
    }

    isSevenPair(idList: string[], idCountList: { [key: string]: number }, ghostList: string[]) {
        if (idList.length + ghostList.length == 14) {
            let singleCount = 0;
            for (let id in idCountList) {
                let idCount = idCountList[id];
                if (idCount % 2 != 0) {
                    singleCount++;
                }
            }
            return singleCount <= ghostList.length;
        }
        return false;
    }

    isWind(idOrType) {
        return "de".indexOf(idOrType[0]) != -1;
    }

    setGhostList(ghostList: string[]) {
        this.ghostList = ghostList;
    }

    getGhostList() {
        return this.ghostList;
    }

    getTingList(idList: string[], idCountList: { [key: string]: number }, testGhostList: string[]) {
        let allId = this.allId;
        let tingList: string[] = [];
        //将所有麻将丢进来循环一次
        for (let k in allId) {
            let id = allId[k];
            let newIdCountList: { [key: string]: number } = {};
            for (let key in idCountList) {
                newIdCountList[key] = idCountList[key];
            }
            let testIdList = idList.concat();
            let newTestGhostList = testGhostList.concat();
            let ghostList = this.getGhostList();
            if (ghostList.indexOf(id) == -1) {//不是鬼牌
                testIdList.push(id);
                if (!newIdCountList[id]) {
                    newIdCountList[id] = 0;
                }
                newIdCountList[id]++;
            } else {
                newTestGhostList.push(id);
            }
            testIdList.sort();
            if (!this.isMeetTheSpecialCondition(testIdList, newIdCountList, newTestGhostList)) {
            } else if (this.isSpecialHu(testIdList, newIdCountList, newTestGhostList)) {
                tingList.push(id);
            }
            else {
                let pingHuResult = this.isPingHu(testIdList, newIdCountList, newTestGhostList);
                if (pingHuResult[0]) {
                    tingList.push(id);
                }
                else if (this.isSevenPair(testIdList, newIdCountList, newTestGhostList)) {
                    tingList.push(id);
                }
            }
        }
        return tingList;
    }

    getIdList(testId: string, handTileDataList: string[]) {
        let tileDataList = handTileDataList.concat();
        tileDataList.sort();
        let ghostList = this.getGhostList();
        let idList: string[] = [];
        let idCountList: { [key: string]: number } = {};
        let testGhostList: string[] = [];
        tileDataList.forEach((tileData) => {
            if (tileData) {
                let id = tileData;
                if (ghostList.indexOf(id) != -1) {
                    testGhostList.push(id);
                } else {
                    idList.push(id);
                    if (!idCountList[id]) {
                        idCountList[id] = 0;
                    }
                    idCountList[id]++;
                }
            }
        });
        if (idCountList[testId]) {
            let index = idList.indexOf(testId);
            idList.splice(index, 1);
            idCountList[testId]--;
        } else if (testGhostList.indexOf(testId) != -1) {
            let index = testGhostList.indexOf(testId);
            testGhostList.splice(index, 1);
        }
        return { idList, idCountList, testGhostList };
    }

    getHandTileIdList(testId: string, tileDataList: string[]) {
        tileDataList.sort(this.tileCompareFunc);
        let idList: string[] = [];
        tileDataList.forEach((tileData) => {
            if (tileData) {
                let id = tileData;
                idList.push(id);
            }
        });
        if (testId) {
            let index = idList.indexOf(testId);
            idList.splice(index, 1);
        }
        idList.sort();
        return idList;
    }

    isReadyToDiscard() {
        return false;
    }

    /**本地计算或者联网查询 */
    useClientOrServer(testId: string, tileDataList: string[]) {
        if (this.isUseServer) {
            if (testId) {
                if (this.isUseFancyTile) {
                    NetHandlerMgr.netHandler.sendFancyTile(testId);
                }
            } else {
                NetHandlerMgr.netHandler.sendGetReadyHand();
            }
            return null;
        } else {
            let result = this.getIdList(testId, tileDataList);
            let idList = result.idList;
            let idCountList = result.idCountList;
            let testGhostList = result.testGhostList;
            let tingList = this.getTingList(idList, idCountList, testGhostList);
            let handIdList = this.getHandTileIdList(testId, tileDataList);
            this.updateMap(handIdList, tingList);
            return tingList;
        }
    }

    cantHu(testId: string, tileDataList: string[]) {
        let result = this.getIdList(testId, tileDataList);
        let idList = result.idList;
        let idCountList = result.idCountList;
        let testGhostList = result.testGhostList;
        let allId = this.allId;
        //将所有麻将丢进来循环一次
        for (let i = 0; i < allId.length; i++) {
            let id = allId[i];
            let newIdCountList: { [key: string]: number } = {};
            for (let key in idCountList) {
                newIdCountList[key] = idCountList[key];
            }
            let testIdList = idList.concat();
            let newTestGhostList = testGhostList.concat();
            let ghostList = this.getGhostList();
            if (ghostList.indexOf(id) == -1) {//不是鬼牌
                testIdList.push(id);
                if (!newIdCountList[id]) {
                    newIdCountList[id] = 0;
                }
                newIdCountList[id]++;
            } else {
                newTestGhostList.push(id);
            }
            testIdList.sort();

            if (!this.isMeetTheSpecialCondition(testIdList, newIdCountList, newTestGhostList)) {//不符合特定条件
                return false;
            }

            if (this.isSpecialHu(testIdList, newIdCountList, newTestGhostList)) {
                return false;
            }
        }
        return false;
    }

    /**
     * @param myTiles key中的id牌序规则为字符、数字大小比较排序。是考虑到服务器发送idList的不确定性、
     *小游戏麻将排序的不确定性(因为鬼牌、癞根之类的特别排序方法) ，导致比较结果不一致
     *@param readyHandTiles   
     */
    updateMap(myTiles: string[], readyHandTiles: string[]) {
        myTiles.sort()
        let key = myTiles.join(',');
        this.tingMap[key] = readyHandTiles;
    }

    clearMap() {
        this.tingMap = {}
    }

    tileCompareFunc(data1: string, data2: string) {
        let id1 = data1;
        let id2 = data2;
        let type1 = id1.charAt(0);
        let type2 = id2.charAt(0);
        if (type1 == type2) {
            if (type1 == "d") {
                let dvalue = { 1: 1, 5: 3, 9: 2 };
                return dvalue[id1.charAt(1)] < dvalue[id2.charAt(1)] ? -1 : 1;
            }
            return id1.charAt(1) < id2.charAt(1) ? -1 : 1;
        }
        return type1 < type2 ? -1 : 1;
    }

    //================================平胡 START================================
    isPingHu(idList, idCountList, ghostList) {
        let removeElement = (arr: any[], element: any) => {
            let index = arr.indexOf(element);
            arr.splice(index, 1);
        }
        //循环去眼
        let result = [false];
        for (let i in idCountList) {
            let newGhostList = ghostList.concat();
            let newTestIdList = idList.concat();
            if (idCountList[i] >= 2) {
                removeElement(newTestIdList, i);
                removeElement(newTestIdList, i);
                newTestIdList.sort();
                result = this.isTripilet(newTestIdList, newGhostList, []);
                if (result[0]) {
                    break; //return result;
                }
            } else if (idCountList[i] == 1 && newGhostList.length >= 1) {//用一个鬼变
                removeElement(newTestIdList, i);
                newTestIdList.sort();
                newGhostList.shift();
                result = this.isTripilet(newTestIdList, newGhostList, []);
                if (result[0]) {
                    break; // return result;
                }
            } else if (newGhostList.length >= 2) {
                newGhostList.shift();
                newGhostList.shift();
                result = this.isTripilet(newTestIdList, newGhostList, []);
                if (result[0]) {
                    break; // return result;
                }
            }
        }
        return result;
    }

    isTripilet(tiles, testGhostList, tileList) {
        let removeElement = (arr: any[], element: any) => {
            let index = arr.indexOf(element);
            arr.splice(index, 1);
        }
        if (tiles == null || tiles.length == 0) {
            return [true, testGhostList, tileList];
        }
        let testTiles: string[] = tiles.concat();
        let firstTile: string = testTiles[0];
        let type = firstTile.substr(0, 1);
        let num = firstTile.substr(1, 1);

        let firstTileIndex = this.allId.indexOf(firstTile);

        // let secondTile = type + (Number(num) + 1);
        // let thirdTile = type + (Number(num) + 2);
        let secondTile = this.allId[firstTileIndex + 1];
        if (!secondTile || secondTile.substr(0, 1) != type) {
            secondTile = "-1";
        }
        let thirdTile = this.allId[firstTileIndex + 2];
        if (!thirdTile || thirdTile.substr(0, 1) != type) {
            thirdTile = "-1";
        }
        let appendTiles: string[] = null;
        let newTestGhostList: string[] = null;
        let tripleList = null;
        let result = null;
        let newTestTiles = null;
        if (testTiles.length >= 3) {
            if (firstTile == testTiles[2]) {//三个相同
                tripleList = tileList.concat(testTiles.slice(0, 3));
                result = this.isTripilet(testTiles.slice(3), testGhostList, tripleList);
                if (result[0])
                    return result;
            }
            if (testGhostList.length > 0 && firstTile == testTiles[1]) {//有两个相同，并且有鬼牌
                appendTiles = testTiles.slice(0, 2);
                newTestGhostList = testGhostList.concat();
                appendTiles.push(newTestGhostList.shift());
                tripleList = tileList.concat(appendTiles);
                result = this.isTripilet(testTiles.slice(2), newTestGhostList, tripleList);
                if (result[0])
                    return result;
            }
            if (!this.isWind(firstTile)) {//是万筒条
                if (testTiles.indexOf(secondTile) != -1 && testTiles.indexOf(thirdTile) != -1) {//顺子
                    newTestTiles = testTiles.concat();
                    removeElement(newTestTiles, firstTile);
                    removeElement(newTestTiles, secondTile);
                    removeElement(newTestTiles, thirdTile);
                    appendTiles = [firstTile, secondTile, thirdTile];
                    tripleList = tileList.concat(appendTiles);
                    result = this.isTripilet(newTestTiles, testGhostList, tripleList);
                    if (result[0])
                        return result;
                }
                if (testGhostList.length > 0 && (testTiles.indexOf(secondTile) != -1 || testTiles.indexOf(thirdTile) != -1)) {//有鬼，顺子差一张
                    let arr = [secondTile, thirdTile];
                    for (let i in arr) {
                        let tile = arr[i];
                        if (testTiles.indexOf(tile) != -1) {
                            newTestTiles = testTiles.concat();
                            removeElement(newTestTiles, firstTile);
                            removeElement(newTestTiles, tile);
                            newTestGhostList = testGhostList.concat();
                            appendTiles = [firstTile, tile, newTestGhostList.shift()];
                            tripleList = tileList.concat(appendTiles);
                            result = this.isTripilet(newTestTiles, newTestGhostList, tripleList);
                            if (result[0])
                                return result;
                        }
                    }
                }
                if (testGhostList.length >= 2) { //两张鬼牌第1张肯定成牌
                    newTestGhostList = testGhostList.concat();
                    tripleList = tileList.concat([testTiles[0], newTestGhostList.shift(), newTestGhostList.shift()]);
                    return this.isTripilet(testTiles.slice(1), newTestGhostList, tripleList);
                }
            }
        } else if (testGhostList.length && testTiles.length == 2) {
            if (testGhostList > 0) {
                newTestGhostList = testGhostList.concat();
                appendTiles = testTiles.slice(0, 2);
                let shift = newTestGhostList.shift();
                appendTiles.push(shift);
                tripleList = tileList.concat(appendTiles);
                let slice = testTiles.slice(2);
                result = this.isTripilet(slice, newTestGhostList, tripleList);
                if (result[0]) {
                    return result;
                }
            }

            if (!this.isWind(firstTile)) {
                if (testTiles.indexOf(secondTile) != -1 || testTiles.indexOf(thirdTile) != -1) {//顺子差一张
                    let arr = [secondTile, thirdTile];
                    for (let i in arr) {
                        let tile = arr[i];
                        if (testTiles.indexOf(tile) != -1) {
                            newTestTiles = testTiles.concat();
                            removeElement(newTestTiles, firstTile);
                            removeElement(newTestTiles, tile);
                            newTestGhostList = testGhostList.concat();
                            appendTiles = [firstTile, tile, newTestGhostList.shift()];
                            tripleList = tileList.concat(appendTiles);
                            result = this.isTripilet(newTestTiles, newTestGhostList, tripleList);
                            if (result[0])
                                return result;
                        }
                    }
                }
            }
            if (testGhostList >= 2) { //两张鬼牌第1张肯定成牌
                newTestGhostList = testGhostList.concat();
                let ntgl_shift = newTestGhostList.shift();
                let concat_content = [testTiles[0], ntgl_shift, ntgl_shift];
                tripleList = tileList.concat(concat_content);
                return this.isTripilet(testTiles.slice(1), newTestGhostList, tripleList);
            }
        }
        if (testGhostList >= 2) { //两张鬼牌第1张肯定成牌
            newTestGhostList = testGhostList.concat();
            let ntgl_shift = newTestGhostList.shift();
            let concat_content = [testTiles[0], ntgl_shift, ntgl_shift];
            tripleList = tileList.concat(concat_content);
            return this.isTripilet(testTiles.slice(1), newTestGhostList, tripleList);
        }
        return [false, testGhostList, tileList];
    }
    //================================平胡 END================================


}