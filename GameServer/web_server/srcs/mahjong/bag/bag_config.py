import redis
import pymysql

from configs import CONFIGS

bag_redis_config = CONFIGS.get('bag_redis') or dict(host='127.0.0.1', password="", db="1")

bag_redis = redis.Redis(**bag_redis_config)


class Mysql_instance(object):
    def __init__(self, host="172.18.254.133", port=3306, user="root", passwd="root", db="bag_data"):
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
