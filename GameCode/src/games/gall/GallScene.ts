class GallScene extends Scene 
{
        start() 
        {
            ExtendMgr.inst.showMinGameSourcePreload();
            EventMgr.on(ExtendMgr.OnMinGameLoadingProgress,this,this.updateProgress.bind(this));
        }

        end()
        {
            EventMgr.off(ExtendMgr.OnMinGameLoadingProgress,this,this.updateProgress);
            super.end();
        }

        updateProgress(data)
        {
            if(!data)return;
            if(data >= 1)
                ExtendMgr.inst.hideMinGameSourcePreload();
            else
                ExtendMgr.inst.updateMinGameSourcePreload2();
        }
}
