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

GRAPHITE_PARAMS = {
                   'host': '192.168.31.181',
                   'port': '2003',
                   'upload_timeinterval': 5,
                   'upload_max_batchsize': 1000,
                   
                   'machine_key': 'M.%s', 
                   'strategy_key': 'S.%s', 
                   
                   'strategies_aggregated_key':'SA', 
                   'machines_aggregated_key':'MA', 
                   
                   'total_key': 'T'
                   }

UPLOAD_STATUS_TIMEINTERVAL = 5
