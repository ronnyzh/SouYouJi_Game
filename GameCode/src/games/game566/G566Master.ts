class G566Master extends G556Master {
    protected gameid: number = 566;
    newNetHandler() {
        return new G566NetHandler();
    }
    addPage(data) {
        return UIMgr.inst.add(G566Page, null, data) as G566Page;
    }
}