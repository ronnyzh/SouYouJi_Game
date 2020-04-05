/**
 * Created by Administrator on 2018/4/10.
 */
interface vuetData{
    addComponent?: Function;
    getComponent?: Function;
    clone?: Function;
    each?: Function;
    debug?: Function;
    watch? :Function;
    createOnce? :Function; //获取一次性函数
}
interface vuetParamsData{
    //数据指针等
    data?: any;     //数据        {key: value}        key绑定到[本类this]，可以通过this._data访问
    params?: any;   //参数        {key: value}        key绑定到[本类this]
    computed?: any; //计算属性    {key: Function(){return value;}} key绑定到[本类this]，作用域为本类this,初始化最后调用,然后不应该更改
    component?: any;//包含组件    {key: conponent}    通过this.getComponent(name) 访问
    //操作方法等
    once?:any;      //一次性自定义方法 {key: Function(){}} 只能被执行一次，key绑定到[本类this]，作用域为本类this
    watch?: any;    //监听数据及参数{key: Function(newValue)}
    method?: any;   //自定义方法    {key: Function(){}}  key绑定到[本类this]，作用域为本类this
    //钩子函数
    beforeCreate?: any; //初始化前执行 Function
    created?: any;      //初始化后执行 Function
}
class Vuet implements vuetData{
    static debug = true;
    public _config = {};
    public _data = {};
    public _paceList = {};
    public _componentList = {};
    public _assemble = {};
    constructor(params: vuetParamsData){
        try{
            let _p;
            if(_p = params.beforeCreate)this.debug(_p).call(this);

            if(_p = params.data)this.walkBindData(_p);
            if(_p = params.params)this.walk(_p, this._data);
            if(_p = params.watch)this.watchObj(_p);
            if(_p = params.method)this.customMethod(_p);
            if(_p = params.once)this.onceMethod(_p);
            if(_p = params.component)this.updateComponents(_p);

            //最后初始化
            if(_p = params.computed)this.comput(_p);

            if(_p = params.created)this.debug(_p).call(this);
        }catch (e){console.error('Vuet初始化错误', e, this);}
        this._config = params;
    }

    //写入一次性方法
    private onceMethod(obj){
        var merge = function(value, name){
            this[name] = this.createOnce(value).bind(this);
        }.bind(this);
        this.each(obj, merge)
    }
    

    //写入自定义方法
    private customMethod(obj){
        var merge = function(value, name){
            this[name] = this.debug(value).bind(this);
        }.bind(this);
        this.each(obj, merge)
    }

    //遍历绑定数据
    private walk (obj, bindData?){
        var _data = bindData || {};
        var merge = function(_value, name){
            try{
                _data[name] = _value;
                Object.defineProperty(this, name, {
                    configurable: false,
                    get: function(){return _data[name];},
                    set: function(newValue){
                        // console.log('set:{0}({1}) = {2}'.format(name, _value, newValue));
                        if(newValue === _data[name])return;
                        _data[name] =newValue;
                        this.pace(name, newValue);
                    }.bind(this),
                })
            }catch (e){
                console.error('绑定数据出错',name )
            }
        }.bind(this);
        this.each(obj, merge);
    }
    private walkBindData(obj){
        this.walk(obj, this._data);
    }

    //当数据改变触发监听器
    private pace(name, newValue){
        var listeners = this._paceList[name];
        if(listeners){
            listeners.forEach(listen=>{(listen as Function).call(this, newValue)});
        }
    }
    //绑定数据监听事件
    private watchObj(obj){
        this.each(obj, function(value, name){
            this.watch(name, value);
        }.bind(this))
    }
    public watch (name, callback){
        var paceList = this._paceList;

        let listeners = paceList[name] || (paceList[name] = []);
        let listen = this.debug(callback).bind(this);
        listeners.push(listen);
    }

    //写入计算属性
    private comput(obj){
        var merge = function(func, name){
            this[name] = this.debug(func).call(this)
        }.bind(this);
        this.each(obj, merge);
    }

    //更新包含的ui组件
    private updateComponents(obj){
        this._componentList = obj;
    }

    public addComponent(name, component){
        this._componentList[name] = component;
    }

    getComponent (name: string) {
        return this._componentList[name];
    }




    clone (){
        return new Vuet(this._config);
    }

    each(objOrArr, method){
        if(typeof objOrArr == 'object')
            return objOrArr instanceof Array ? objOrArr.forEach(method) : Object.keys(objOrArr).forEach(function(key, idx){return method(objOrArr[key], key)});
    }

    debug(func){
        return (typeof func == 'function') ? function(){
            try{
                let result = func.apply(this, Array.prototype.slice.apply(arguments));

                return typeof result == 'undefined' ? this : result;
            }catch(e){console.error(e);}
        }:func;
    }

    createOnce(func){
        var _called = false;
        return function(){
            if(_called)return Vuet.debug ? console.warn('方法['+name+']已经被调用', this): undefined;
            _called = true;
            return this.debug(func).apply(this, Array.prototype.slice.apply(arguments));
        };
    }
}