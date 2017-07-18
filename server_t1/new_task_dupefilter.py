# from scrapy-redis

from log.log import get_logger
import defaults
import traceback
import hashlib
import connection
# import time



class New_Task_DupeFilter(object):
    
    def __init__(self, RedisIns, logger = None):
        
        self.logger = logger 
        self.server = RedisIns
        
    
    @classmethod
    def from_default(cls, logger = None):
        logger = logger or get_logger('New_Task_DupeFilter')
        RedisIns = connection.get_redis_from_default()
        
        return cls(RedisIns, logger)



    def get_task_fingerprint(self, TaskJson):
        fp = hashlib.sha1()
        fp.update(TaskJson.encode('utf-8'))
        fpd = fp.hexdigest()
        
        return fpd
    
    

    def task_seen(self, TaskJson):
        fp = self.get_task_fingerprint(TaskJson)
        try:
            added = self.server.sadd(defaults.NEW_TASK_DUPEFILTER_KEY, fp)
        except Exception as e:
            self.logger.warn(traceback.format_exc(e))
            
        return added == 0 # if seen return True



    def _clear(self):
        self.server.delete(self.key) 
        
    def close(self, reason=''):
        self._clear()


        
if __name__ == '__main__':
    New_Task_DupeFilter_Ins = New_Task_DupeFilter.from_default()
    print New_Task_DupeFilter_Ins.task_seen('111')
    
    
    
    