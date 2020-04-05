class G558Master extends G556Master {
    protected gameid: number = 558;
    newNetHandler() {
        return new G558NetHandler();
    }
    addPage(data) {
        return UIMgr.inst.add(G558Page, null, data) as G558Page;
    }
}