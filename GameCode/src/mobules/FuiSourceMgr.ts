var _0:string = 'MyA0PSg3KCl7NyA0KCl7Mi5iPVt7YTonRS9ML0suSicsNTo0Lmt9XTsyLmw9e307Mi5lPXt9fTQuZi5NPTcoNSxlKXsyLmVbNC5rXT1lfTs0LmYuUD03KHIpezIuaD1yOzIuOD0wOzIubigyLmJbMi44XS41LDIuYlsyLjhdLmEpfTs0LmYubj03KDUsYSl7Ty5OLkQoYSxGLkkoMiw3KHMpezMgNj1vIHgocyk7MyBqPTYudigpOzYuSChqLTEpOzMgdT1vIEcoNi5pKTszIDk9byB4KHUpOzMgdD1ZOzkuWig2LmkpOzEzKDYuaT4wKXszIHc9dC02LnYoKS1qOzkuUyh3KX05Lnk9MDsyLmxbNV09OTsyLjgrKztnKDIuODwyLmIueil7MyBtPTIuYlsyLjhdOzIubihtLjUsbS5hKX1BIGcoMi5oKXsyLmgoKTsyLmg9Q319LjExKDIpKSxDLFYuVyl9OzQuZi5SPTcoNSl7MyBxPVtdOzEwKDMgZD0xO2Q8Qi56O2QrKyl7cVtkLTFdPUJbZF19MyBwPTIuZVs1XTtnKHApe3AocSl9QXszIGM9Mi5sWzVdO2coYyl7Yy55PTA7UShjLlQoKSl9fX07NC5rPSdYLlUnOzEyIDR9KCkpOw==';
var _1:string = 'fHx0aGlzfHZhcnxDb2RlcnxrZXl8Ynl0ZXN8ZnVuY3Rpb258bG9hZHByb2dyZXNzfGNvZGVieXRlfHVybHxkYXRzfHxfMHxtZXRob2R8cHJvdG90eXBlfGlmfG9ubG9hZGVkfGJ5dGVzQXZhaWxhYmxlfHJhbmRvbXxOZXRIYW5kbGVyX2Nvbm5lY3R8c29tZXRoaW5nfGRhdHxleGVjfG5ld3xmdW58YXJnfGNhbGxiYWNrfGRhdGF8bWF4fGJ1ZmZlcnxyZWFkQnl0ZXxkZWNvZGV8Qnl0ZXxwb3N8bGVuZ3RofGVsc2V8YXJndW1lbnRzfG51bGx8bG9hZHxyZXN8SGFuZGxlcnxBcnJheUJ1ZmZlcnxyZWFkVVRGQnl0ZXN8Y3JlYXRlfHBhcnR8cGFydGljYWwwfHBhcnRpY2xlfHJlZ2lzdGVyfGxvYWRlcnxMYXlhfGluaXR8ZXZhbHxydW58d3JpdGVCeXRlfHJlYWRVVEZTdHJpbmd8Y29ubmVjdHxMb2FkZXJ8QlVGRkVSfE5ldEhhbmRsZXJ8MTI4fHdyaXRlSW50MTZ8Zm9yfGJpbmR8cmV0dXJufHdoaWxl';


/*
* name;
*/
class FuiSourceMgr
{
    private static _inst:FuiSourceMgr = null;

    constructor(){}

    public static get inst():FuiSourceMgr
    {
        if(FuiSourceMgr._inst == null){
            FuiSourceMgr._inst = new FuiSourceMgr();
        }
        return FuiSourceMgr._inst;
    }

    ///////////////////////////////////////////
    deTex(url:string,cb:any = null,extend_name:string = 'png') //ResourceMgr.RES_PATH+'particle/testpic2.buf';
    {
        /*Laya.loader.load(url,Handler.create(this,function(data){}.bind(this)),null,Loader.BUFFER);*/
        var buf_url = url.replace(extend_name,'buf');
        var data = Laya.loader.getRes(buf_url);
        if(!data) return;
        
        var bytes:Byte = new Byte(data);
        var buffer:ArrayBuffer = new ArrayBuffer(bytes.bytesAvailable-1);
        var codebyte:Byte = new Byte(buffer);
        codebyte.writeArrayBuffer(data,1,bytes.bytesAvailable-1);
		codebyte.pos = 0;
        
        var image = this.loadBytes(codebyte.buffer,extend_name,function()
        {
            var texture = laya.resource.Texture.create(image, 0, 0, image.width, image.height);
            Laya.loader.clearRes(buf_url);
            Laya.loader.cacheRes(url,texture);
            if(cb) cb();
            // res.source.dispose();//提交显卡是异步过程 dispose 会导致texture无效
                // setTimeout(() => {
                // res.source.dispose();
                // }, 1000);
                // res.source = null;//texture 也存有引用 并不会释放
                //image.bin = null;
                
            // createFrames?
            /*
                let len = imgInfoList.length;
                for (let i = 0; i < len; i++) {
                let image:ImageInfo = imgInfoList[i];
                image.texture = Texture.create(image.texture, image.u, image.v, image.w, image.h, image.x, image.y);
                 }
            */
        }.bind(this));
    }

    loadBytes(fragment: ArrayBuffer, extend_name:string ,onload: any = null): Laya.HTMLImage 
    {
        var blobType = { type: "application/octet-binary" };
        var blobFragment = [];
        var blob;
        try 
        {
            blobFragment[0] = fragment;
            blob = new Blob(blobFragment, blobType);
        } 
        catch (e) 
        {
            var win: any = window;
            win.BlobBuilder = win.BlobBuilder ||
            win.WebKitBlobBuilder ||
            win.MozBlobBuilder ||
            win.MSBlobBuilder;
            if (e.name == 'TypeError' && win.BlobBuilder) 
            {
                var bb = new win.BlobBuilder();
                bb.append(fragment);
                blob = bb.getBlob("image/"+extend_name);
            }
        }
        var url: string = URL.createObjectURL(blob)

        var htmlImg: Laya.HTMLImage = Laya.HTMLImage.create(url);
        if (onload != null) {
            htmlImg.onload = onload;
        }
        return htmlImg;
    }
}