# from scrapy-redis
import mysql.connector
import defaults
from log.log import get_logger

logger = get_logger('connection')

def get_redis(**kwargs):        
    redis_cls = defaults.REDIS_CLS
    url = kwargs.get('url')
    if url:
        return redis_cls.from_url(url, **kwargs)
    else:
        return redis_cls(**kwargs)
    
    

def get_redis_from_default():
    params = defaults.REDIS_PARAMS.copy()
    RedisIns = get_redis(**params)
        
    return RedisIns
    
    
def get_myconn_from_default():
    params = defaults.MYSQL_PARAMS.copy()
    MySqlConn = mysql.connector.connect(**params)
    return MySqlConn

    
    
if __name__ == '__main__':
    RedisIns = get_redis_from_default()
    print RedisIns.keys()
    
