/**
 *  表格工具对象
 *  @name formUtils
 *  @param  val: row: index:
 *  @author:david
 +---------------------------------------------------------
*/

function toMoney(value){
    value = parseFloat(value)
    value = value.toFixed(2);
    value = value.toLocaleString();
    return value;//返回的是字符串23,245.12保留2位小数
}

function colorFormat(value,color){  //颜色格式化
    fontColor = color || '#1E9FFF'; //#1E9FFF
    statusstr = String.format('<span style="color:{0}">{1}</span>',fontColor,value);

    return [statusstr].join('');
}

function getColor(value,row,index){
    if (!value)
        value = '0.00'
    value = toMoney(value)
    eval('var rowobj='+JSON.stringify(row))
    statusstr = '<span style="color:#6600FF">'+value+'</span>';

    return [statusstr].join('');
}

function getImg(value,row,index){
    statusstr = ""
    if (!value)
        return statusstr
    console.log("--------------getImg value:"+value);
    fish_imgs = value;
    eval('var rowobj='+JSON.stringify(row))
    for (var idx = 0; idx<fish_imgs.length;idx++){
        statusstr+=String.format('<img src="/assest/default/image/fish_images/fish_{0}.png" widht="40" height="40"/>',fish_imgs[idx]);
    }

    return [statusstr].join('');
}

function getAvatorImg(value,row,index){
      eval('var rowobj='+JSON.stringify(row))
      statusstr = '<img src="'+row['headImgUrl']+'" width="30" height="30" />';

      return [statusstr].join('');
}

function getRewardImg(value,row,index){
      eval('var rowobj='+JSON.stringify(row))
      statusstr = '<img src="'+row['reward_img_path']+'" width="100" height="100" />';

      return [statusstr].join('');
}

function getFuncColor(value,row,index){
    if (!value)
        value = '0.00'
    value = toMoney(value)
    eval('var rowobj='+JSON.stringify(row));

    console.log(String.format("---------check value[{0}]",value))
    if (parseInt(value) > 0)
        statusstr = '<span style="color:red"> +'+value+'</span>';
    else
        statusstr = '<span style="color:green">'+value+'</span>';

    return [statusstr].join('');
}

function getDate(value,row,index){
    var time = new Date(value).toLocaleString();
    return time;
}
