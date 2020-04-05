/**
 * Created by Administrator on 2018/4/11.
 */
module jx {

    /**
     * 合并对象
     * */
    export let extend = function (...arg) {
        var result = {};
        var args = Array.prototype.slice.apply(arguments);
        args.forEach(function (obj) {
            Object.keys(obj).forEach(function (key) {
                result[key] = obj[key];
            });
        });
        return result;
    };

    /**
     * 格式化大额数字
     * */
    export let goldFormat = function (num) {
        /*if (typeof num === 'string' || typeof num === 'number') {
            num = num.toString();
            num = num.replace(/([0-9]+\.?[0-9]+)/, function (match) {
                var match_int = parseInt(match).toString();
                switch (true) {
                    case match_int.length > 8:
                        var num = match / Math.pow(10, 8);
                        return jx.floor2Fixed(num, 1) + "亿";
                    case match_int.length > 7:
                        var num = match / Math.pow(10, 7);
                        return jx.floor2Fixed(num, 1) + "千万";
                    case match_int.length > 4:
                        var num = match/ Math.pow(10, 4);
                        return jx.floor2Fixed(num, 1) + "万";
                    default:
                        return match;
                }
            });
        }*/
        return Tools.inst.changeGoldToMoney(num);
    };

    /**
     * 向下取整保留至小数
     */
    export let floor2Fixed = function (num, len) {
        len = len || 0;
        var arr = num.toString().split(".");
        var num1 = arr[0];
        var num2 = arr[1];
        if (arr.length > 1) {
            var dLen = num2.length;
            var keepLen = len > dLen ? dLen : len;
            num2 = num2.substr(0, keepLen);
            num = num1 + (num2 ? "." + num2 : "");
        }
        return num;
    };

    /**
     *  创建一次性函数
     * */
    export let once = function(caller, method, args:Array<any>=[]){
        var _called = false;
        return function(){
            //console.log('once call ', ',_called:',_called, 'method :', method );
            return _called
                ? function(){}
                : (_called = true && method.apply(caller || this, [].concat(args, [].slice.apply(arguments))));
        }
    }

    /**
     * Helper function that creates a cc.Point.
     * @function
     * @param {Number|cc.Point} x a Number or a size object
     * @param {Number} y
     * @return {cc.Point}
     * @example
     * var point1 = cc.p();
     * var point2 = cc.p(100, 100);
     * var point3 = cc.p(point2);
     * var point4 = cc.p({x: 100, y: 100});
     */
    export let p = function (x, y) {
        // This can actually make use of "hidden classes" in JITs and thus decrease
        // memory usage and overall performance drastically
        // return cc.p(x, y);
        // but this one will instead flood the heap with newly allocated hash maps
        // giving little room for optimization by the JIT,
        // note: we have tested this item on Chrome and firefox, it is faster than cc.p(x, y)
        if (x === undefined)
            return {x: 0, y: 0};
        if (y === undefined)
            return {x: x.x, y: x.y};
        return {x: x, y: y};
    };

    /**
     * Iterate over an object or an array, executing a function for each matched element.
     * @param {object|array} obj
     * @param {function} iterator
     * @param {object} [context]
     */
    export let each = function (obj, iterator?, context?) {
        if (!obj)
            return;
        if (obj instanceof Array) {
            for (var i = 0, li = obj.length; i < li; i++) {
                if (iterator.call(context, obj[i], i) === false)
                    return;
            }
        } else {
            for (var key in obj) {
                if (iterator.call(context, obj[key], key) === false)
                    return;
            }
        }
    };

    /**
     * Check the obj whether is array or not
     * @param {*} obj
     * @returns {boolean}
     */
    export let isArray = function(obj) {
        return Array.isArray(obj) ||
            (typeof obj === 'object' && Object.prototype.toString.call(obj) === '[object Array]');
    };
}