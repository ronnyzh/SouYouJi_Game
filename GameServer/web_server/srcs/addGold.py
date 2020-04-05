# from mahjong.model.goldModel import get_gold_rank
import redis

def get_redis_ins(host='127.0.0.1', port=6379, password='', db=1):
    r = redis.Redis(host=host, port=port, db=db, password=password)
    return r

#groupId = '000000'
#account = 'ping1'
redis = get_redis_ins()
#data = get_gold_rank(redis, groupId, account)
#print(data)
user = redis.keys('users:[1-9]*')
print(user)
for item in user:
    #print(redis.type(item))
    if redis.type(item) =='hash':
        redis.hmset(item, {"gold": 500000})
