# from scrapy-redis
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
    
    
    
if __name__ == '__main__':
    RedisIns = get_redis_from_default()
    print RedisIns.keys()
    
