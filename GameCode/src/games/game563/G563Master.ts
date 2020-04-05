class G563Master extends G556Master {
    protected gameid: number = 563;
    newNetHandler() {
        return new G563NetHandler();
    }
    addPage(data) {
        return UIMgr.inst.add(G563Page, null, data) as G563Page;
    }
}