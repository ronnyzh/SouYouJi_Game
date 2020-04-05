#coding:utf-8
from datetime import datetime

def use_record_log(func):
    def inner(*args,**kwargs):
        func(*args,**kwargs)
    return inner

def log_bag(uid,item_id,num):
    with open('use_item_log','a') as f:
        content = "["+str(datetime.now())+"]"+"[uid:"+uid+"]"+"[item_id:"+item_id+"]"+"[num:"+str(num)+"]\n"
        f.write(content)
