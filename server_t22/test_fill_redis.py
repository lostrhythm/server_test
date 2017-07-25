# -*- coding:utf-8 -*-
'''
Created on 2017年7月24日

@author: Thinkpad
'''
from threading import Thread
from log.log import get_logger
import json
import time
import connection
from random import randint,seed

RI = connection.get_redis_from_default()
logger = get_logger('test_fill_redis')

seed(10)

def status_generator():
        
    while True:
        
        status_1 = [
                    "ip_1", 
                    123,
                    {
                    "TEST_2": {"FR_c": randint(1,20), "GT_c": randint(1,20), "FT_c": randint(1,20), "RT_c": randint(1,20), "TR_c": randint(1,20), "SR_c": randint(1,20), "ST_c": randint(1,20)}, 
                    "TEST_1": {"FR_c": randint(1,20), "GT_c": randint(1,20), "FT_c": randint(1,20), "RT_c": randint(1,20), "TR_c": randint(1,20), "SR_c": randint(1,20), "ST_c": randint(1,20)}
                    }]
        
        status_2 = [
                    "ip_2", 
                    123,
                    { 
                    "TEST_2": {"FR_c": randint(1,20), "GT_c": randint(1,20), "FT_c": randint(1,20), "RT_c": randint(1,20), "TR_c": randint(1,20), "SR_c": randint(1,20), "ST_c": randint(1,20)}, 
                    "TEST_1": {"FR_c": randint(1,20), "GT_c": randint(1,20), "FT_c": randint(1,20), "RT_c": randint(1,20), "TR_c": randint(1,20), "SR_c": randint(1,20), "ST_c": randint(1,20)}
                    }]
        
        status_3 = [
                    "ip_3", 
                    123,
                    {
                    "TEST_2": {"FR_c": 1, "GT_c": 1, "FT_c": 1, "RT_c": 1, "TR_c": 1, "SR_c": 1, "ST_c": 1}, 
                    "TEST_1": {"FR_c": 1, "GT_c": 1, "FT_c": 1, "RT_c": 1, "TR_c": 3, "SR_c": 3, "ST_c": 1}
                    }]
        
        looplist = [status_1, status_2, status_3]
        
        for status in looplist:
            yield status
        
        

def lpush_status(RedisIns):
    status_generator_ins = status_generator()
    while True:
        for _ in range(3):
            status = status_generator_ins.next()
            statusjson = json.dumps(status)
            RedisIns.lpush('status_list', statusjson)
            logger.info('lpush status: %s'%statusjson)
        time.sleep(20)


def do_fill():
    t1 = Thread(target= lpush_status, args = (RI,))
    t1.start()



if __name__ == '__main__':
    do_fill()
    
    
    
    
    