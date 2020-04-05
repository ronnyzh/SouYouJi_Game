/*
* name;
*/
class SequenceController{
    private actionDataList:Array<any>=null;
    private acting:boolean;
    public actionFinishedListener:Function;
    private executeAction:Function;
    constructor(){
        this.actionDataList = [];
        this.acting = false;
        this.actionFinishedListener = this.onActionFinished.bind(this);
    }

    push(data)
    {
        this.actionDataList.push(data);
        this.peek();
    }

    onActionFinished()
    {
        this.acting = false;
        this.peek();
    }

    reset()
    {
        this.acting = false;
        this.actionDataList = [];
    }

    peek()
    {
        if(this.acting || this.actionDataList.length == 0)
            return;

        this.acting = true;
        var actionData = this.actionDataList.shift();
        this.executeAction(actionData);
    }

    setExecutor(executor)
    {
        this.executeAction = executor;
    }
    
    dispose()
    {

    }
}