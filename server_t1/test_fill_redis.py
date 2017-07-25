# -*- coding:utf-8 -*-
'''
Created on 2017年7月13日

@author: Thinkpad
'''

from threading import Thread
from log.log import get_logger
import json
import time
import connection

RI = connection.get_redis_from_default()
logger = get_logger('test_fill_redis')


BASIC_KEY_COMMAND_MAP = {
                          'new_task_dupefilter' : ['sadd', 'new_task_dupefilter', 'placeholder'],
                          'processed_task_list' : ['lpush', 'processed_task_list', 'placeholder'], 
                          'new_task_sset' : ['zadd', 'new_task_sset', 0, 'placeholder'], 
                          'status_list' : ['lpush', 'status_list', 'placeholder'], 
                          'user_tasks:test_vps_ip' : ['lpush', 'user_tasks:test_vps_ip', 'placeholder'],
                          'strategies' : ['set', 'strategies', 'placeholder'], 
                          'task_list:TEST_0' : ['lpush', 'task_list:TEST_0', 'placeholder'], 
                          'user:test_vps_ip' : ['hset', 'user:test_vps_ip', 'password', '123'], 
                          'user_strategies:test_vps_ip' : ['set', 'user_strategies:test_vps_ip', 'placeholder'] 
                          } 



def initialize_default_keys(RedisIns):
    
    keys_e = RedisIns.execute_command('keys', '*') 
    for k in BASIC_KEY_COMMAND_MAP:
        if k in keys_e:
            logger.info('key %s exists'%str(k))
        else:
            command = BASIC_KEY_COMMAND_MAP[k]
            print command
            RedisIns.execute_command(command[0], *command[1:])
            logger.info('key %s instantiated'%str(k))
            
            

def load_strategies_4_user(RedisIns):
    
    LoadedStrategiesJson = json.dumps(['TEST_0', 'TEST_1', 'TEST_2'], 'utf-8')
    RedisIns.set('user_strategies:test_vps_ip', LoadedStrategiesJson)



def StrategyGenerator():
    
    TEST_1_1_json = '{"RetryTime": 2, "WaitTime": 1, "CookieUse":false, "StrategyID": "TEST_1", "AdditionParams": "{\\"rules\\":[\\"rule_1\\", \\"rule_2\\"]}", "Timeout": 3, "Encoding": "utf-8", "FragmentalUpload": false, "FragmentalAmount":5, "ContentException":[]}'
    TEST_2_1_json = '{"RetryTime": 2, "WaitTime": 1, "CookieUse":false, "StrategyID": "TEST_2", "AdditionParams": "{\\"rules\\":[\\"rule_1\\", \\"rule_2\\"]}", "Timeout": 3, "Encoding": "utf-8", "FragmentalUpload": false, "FragmentalAmount":5, "ContentException":[]}'
    StrategyGroup_1_dict = {'TEST_1' : TEST_1_1_json, 'TEST_2' : TEST_2_1_json}
    StrategyGroupJson_1 = json.dumps(StrategyGroup_1_dict)  
    
    TEST_1_2_json = '{"RetryTime": 3, "WaitTime": 1, "CookieUse":false, "StrategyID": "TEST_1", "AdditionParams": "{\\"rules\\":[\\"rule_1\\", \\"rule_2\\"]}", "Timeout": 3, "Encoding": "utf-8", "FragmentalUpload": false, "FragmentalAmount":5, "ContentException":[]}'
    TEST_2_2_json = '{"RetryTime": 3, "WaitTime": 1, "CookieUse":false, "StrategyID": "TEST_2", "AdditionParams": "{\\"rules\\":[\\"rule_1\\", \\"rule_2\\"]}", "Timeout": 3, "Encoding": "utf-8", "FragmentalUpload": false, "FragmentalAmount":5, "ContentException":[]}'
    StrategyGroup_2_dict = {'TEST_1' : TEST_1_2_json, 'TEST_2' : TEST_2_2_json}
    StrategyGroupJson_2 = json.dumps(StrategyGroup_2_dict)    
    
    looplist = [StrategyGroupJson_1, StrategyGroupJson_2]
    
    while True:
        for StrategyGroupJson in looplist:
            yield StrategyGroupJson
            
def TaskGenerator():
    Task_1_json = '{"Priority": 1, "Encoding": "utf-8", "TaskStatus": 0, "ParentID": -1, "TaskID": 1, "TaskType": 0, "StrategyID": "TEST_1", "AdditionParams": "{\\"a\\": 2}", "Processor": null, "TaskContent": "data+science"}'
    Task_2_json = '{"Priority": 1, "Encoding": "utf-8", "TaskStatus": 0, "ParentID": -1, "TaskID": 2, "TaskType": 0, "StrategyID": "TEST_1", "AdditionParams": "{\\"a\\": 2}", "Processor": null, "TaskContent": "computer+science"}'
    Task_3_json = '{"Priority": 1, "Encoding": "utf-8", "TaskStatus": 0, "ParentID": -1, "TaskID": 3, "TaskType": 0, "StrategyID": "TEST_1", "AdditionParams": "{\\"a\\": 2}", "Processor": null, "TaskContent": "spider"}'
    Task_4_json = '{"Priority": 1, "Encoding": "utf-8", "TaskStatus": 0, "ParentID": -1, "TaskID": 4, "TaskType": 0, "StrategyID": "TEST_1", "AdditionParams": "{\\"a\\": 2}", "Processor": null, "TaskContent": "queue"}'
    Task_5_json = '{"Priority": 1, "Encoding": "utf-8", "TaskStatus": 0, "ParentID": -1, "TaskID": 5, "TaskType": 0, "StrategyID": "TEST_2", "AdditionParams": "{\\"a\\": 2}", "Processor": null, "TaskContent": "python"}'
    Task_6_json = '{"Priority": 1, "Encoding": "utf-8", "TaskStatus": 0, "ParentID": -1, "TaskID": 6, "TaskType": 0, "StrategyID": "TEST_2", "AdditionParams": "{\\"a\\": 2}", "Processor": null, "TaskContent": "shell"}'
    Task_7_json = '{"Priority": 1, "Encoding": "utf-8", "TaskStatus": 0, "ParentID": -1, "TaskID": 7, "TaskType": 0, "StrategyID": "TEST_2", "AdditionParams": "{\\"a\\": 2}", "Processor": null, "TaskContent": "c++"}'
    Task_8_json = '{"Priority": 1, "Encoding": "utf-8", "TaskStatus": 0, "ParentID": -1, "TaskID": 8, "TaskType": 0, "StrategyID": "TEST_2", "AdditionParams": "{\\"a\\": 2}", "Processor": null, "TaskContent": "play+station"}'

    looplist = [Task_1_json, Task_2_json, Task_3_json, Task_4_json, Task_5_json, Task_6_json, Task_7_json, Task_8_json]
    
    while True:
        for TaskJson in looplist:
            yield TaskJson
   
   
def _inc(inc, x):
    return inc + x         
            
def TaskIDGenerator(n):
    from functools import partial
    basiclist = [1,2,3,4,5,6,7,8,9,10]
    TaskIDList = map(partial(_inc, n * len(basiclist)), basiclist)
    while True:
        for TaskID in TaskIDList:
            yield TaskID
            
            
def lpush_strategies(RedisIns):
    StrategyGenerator_Ins = StrategyGenerator()
    while True:
        StrategyGroupJson = StrategyGenerator_Ins.next()
        RedisIns.set('strategies', StrategyGroupJson) 
        logger.info('filled strategygroup')
        time.sleep(10)
            
def lpush_task_list(RedisIns):
    TaskGenerator_Ins = TaskGenerator()
    while True:
        TaskJson = TaskGenerator_Ins.next()
        strategy = json.loads(TaskJson).get('StrategyID') 
        RedisIns.lpush('task_list:%s'%str(strategy or 'TEST_0'), TaskJson) 
        logger.info('filled one taskgroup')
        time.sleep(1)
        
def lpush_user_tasks(RedisIns):
    TaskIDGeneratorIns_1 = TaskIDGenerator(0)
    TaskIDGeneratorIns_2 = TaskIDGenerator(1)
    while True:
        TaskIDList = []
        TaskID_1 = TaskIDGeneratorIns_1.next()
        TaskIDList.append(TaskID_1)
        RedisIns.lpush('user_tasks:test_vps_ip', TaskID_1)
        
        TaskID_2 = TaskIDGeneratorIns_2.next()
        TaskIDList.append(TaskID_2)
        RedisIns.lpush('user_tasks:test_vps_ip2', TaskID_2)
        
        logger.info('filled taskID: %s'%str(TaskIDList))
        time.sleep(1)
        
        
def lpush_processed_task_list(RedisIns):
    TaskJsonList = ['{"Priority": 2, "Encoding": null, "ParentID": -1, "TaskStatus": -1, "TaskID": 3, "TaskType": 0, "TaskContent": "k3", "StrategyID": "TEST_2", "AdditionParams": "{}", "Processor": "test_vps_ip"}' , \
                    '{"Priority": 2, "Encoding": null, "ParentID": -1, "TaskStatus": -1, "TaskID": 6, "TaskType": 0, "TaskContent": "k3", "StrategyID": "TEST_2", "AdditionParams": "{}", "Processor": "test_vps_ip"}' , \
                    '{"Priority": 2, "Encoding": null, "ParentID": -1, "TaskStatus": -1, "TaskID": 2, "TaskType": 0, "TaskContent": "k2", "StrategyID": "TEST_1", "AdditionParams": "{}", "Processor": "test_vps_ip"}' , \
                    '{"Priority": 2, "Encoding": null, "ParentID": -1, "TaskStatus": -1, "TaskID": 5, "TaskType": 0, "TaskContent": "k2", "StrategyID": "TEST_1", "AdditionParams": "{}", "Processor": "test_vps_ip"}' , \
                    '{"Priority": 2, "Encoding": null, "ParentID": -1, "TaskStatus": -1, "TaskID": 1, "TaskType": 0, "TaskContent": "k1", "StrategyID": "TEST_0", "AdditionParams": "{}", "Processor": "test_vps_ip"}' , \
                    '{"Priority": 2, "Encoding": null, "ParentID": -1, "TaskStatus": -1, "TaskID": 4, "TaskType": 0, "TaskContent": "k1", "StrategyID": "TEST_0", "AdditionParams": "{}", "Processor": "test_vps_ip"}']
    
    for TaskJson in TaskJsonList:
        RedisIns.lpush('processed_task_list', TaskJson)

def lpush_tasktimelimit(RedisIns):
    TaskIDList = [1,2,3,4,5,6]
    TimeLimitList = [str(time.time() + 10)] * len(TaskIDList) 
    data = zip(TaskIDList, TimeLimitList)
    for t in data:
        RedisIns.hset('task_timelimit', t[0], t[1])
        
        
def zadd_newtask_sset(RedisIns):
    TaskJsonList = ['{"Priority": 3, "Encoding": null, "ParentID": 1, "TaskStatus": -1, "TaskID": -1, "TaskType": 0, "TaskContent": "k1", "StrategyID": "TEST_2", "AdditionParams": "{}", "Processor": null}' , \
                    '{"Priority": 3, "Encoding": null, "ParentID": 1, "TaskStatus": -1, "TaskID": -1, "TaskType": 0, "TaskContent": "k2", "StrategyID": "TEST_2", "AdditionParams": "{}", "Processor": null}' , \
                    '{"Priority": 3, "Encoding": null, "ParentID": 2, "TaskStatus": -1, "TaskID": -1, "TaskType": 0, "TaskContent": "k3", "StrategyID": "TEST_1", "AdditionParams": "{}", "Processor": null}' , \
                    '{"Priority": 3, "Encoding": null, "ParentID": 3, "TaskStatus": -1, "TaskID": -1, "TaskType": 0, "TaskContent": "k4", "StrategyID": "TEST_1", "AdditionParams": "{}", "Processor": null}' , \
                    '{"Priority": 3, "Encoding": null, "ParentID": 7, "TaskStatus": -1, "TaskID": -1, "TaskType": 0, "TaskContent": "k5", "StrategyID": "TEST_0", "AdditionParams": "{}", "Processor": null}' , \
                    '{"Priority": 3, "Encoding": null, "ParentID": 9, "TaskStatus": -1, "TaskID": -1, "TaskType": 0, "TaskContent": "k6", "StrategyID": "TEST_0", "AdditionParams": "{}", "Processor": null}']
    
    for TaskJson in TaskJsonList:
        RedisIns.zadd('new_task_sset', 1, TaskJson)
        
        
def do_fill():
    initialize_default_keys(RI)
    load_strategies_4_user(RI)
    lpush_processed_task_list(RI)
    lpush_tasktimelimit(RI)
    zadd_newtask_sset(RI)
    t1 = Thread(target= lpush_strategies, args = (RI,))
    t2 = Thread(target= lpush_task_list, args = (RI,))
    t3 = Thread(target= lpush_user_tasks, args = (RI,))
    t1.start()
    t2.start()
    t3.start()

    
    
    
if __name__ == '__main__':
    do_fill()

    