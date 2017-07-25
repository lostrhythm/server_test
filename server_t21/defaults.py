# from scrapy-redis
import redis

REDIS_CLS = redis.StrictRedis
REDIS_ENCODING = 'utf-8'
REDIS_PARAMS = {
                'socket_timeout': 30,
                'socket_connect_timeout': 30,
                'retry_on_timeout': True,
                'encoding': REDIS_ENCODING,
                'host': '192.168.31.179',
                'port':'6379',
                'encoding': 'utf-8'
                }


MYSQL_PARAMS = {
                'host': '192.168.31.179',
                'user': 'crawlertest_user',
                'password': 'z56123',
                'database': 'crawler_test_db'
                }


