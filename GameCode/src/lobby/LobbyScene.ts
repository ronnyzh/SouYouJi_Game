/*
* name;
*/
class LobbyScene extends Scene{
    getRes(){
        var protoPath = ResourceMgr.PROTO_PATH;
        return [
            { url: "res/ui/Lobby.fui", type: Loader.BUFFER },
            { url: protoPath+"mahjong.proto", type :Loader.TEXT},
            { url: protoPath+"gold.proto", type :Loader.TEXT}
        ]
    }

    start(){
        fairygui.UIPackage.addPackage('res/ui/Lobby');
        UIMgr.inst.add(LobbyPage);        
    }

    update(){

    }

    end(){
        super.end();
    }
}