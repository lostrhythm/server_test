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

# objects instantiate by server_t1
NEW_TASK_DUPEFILTER_KEY = 'new_task_dupefilter' # redis_ops.new_task_dupefilter
NEW_TASK_SSET = 'new_task_sset' # server_methods_t1
PROCESSED_TASK_LIST = 'processed_task_list' # server_methods_t1
STATUS_LIST = 'status_list' # server_methods_t1