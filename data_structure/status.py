# -*- coding:utf-8 -*-
'''
Created on 2017年6月19日

@author: Thinkpad
'''
import json
from collections import Counter
from utils.decorators import Singleton
from log.log import get_logger
logger = get_logger('status')

 
 
 
@Singleton 
class MachineStatus():
    # MachineStatus is instantiated once for a engine startup
    def __init__(self, user = 'test_vps_ip'): 
        self._user = user # usually IP of vps
        self._MachineStatusCollector_dict = {} # {StrategyID : strategy_status_collector, ...}
        
    def machine_status_collector(self):
        return self._MachineStatusCollector_dict
    
    def get_user(self):
        return self._user
    
    def get_json(self): # when sending pass the _MachineStatusCollector_dict into upload_status directly
        MachineStatusJson = json.dumps(self._MachineStatusCollector_dict, 'utf-8')
        return MachineStatusJson
    

        
    
class StrategyStatus():
    # StrategyStatus instantiated when each spider plugin is instantiated
    def __init__(self, MachineStatusIns, StrategyID = 'TEST'):
        self.start_collector()
        
        self._StrategyID = StrategyID
        self._MachineStatusCollector_dict = MachineStatusIns.machine_status_collector()
        
        if not self._MachineStatusCollector_dict.has_key(self._StrategyID): # automatically load into MachineStatus
            self._MachineStatusCollector_dict[self._StrategyID] = self._StrategyStatusCollector_counter
            # {StrategyID : strategy_status_collector, ...}
            
        else:
            logger.warn('_MachineStatusCollector_dict has already contain the strategy name: %s'%self._StrategyID)
            raise KeyError

    def start_collector(self): # restart
        self._StrategyStatusCollector_counter = Counter()
        
        self._StrategyStatusCollector_counter['task_cnt'] = 0
        self._StrategyStatusCollector_counter['task_success'] = 0
        self._StrategyStatusCollector_counter['task_failed'] = 0
        self._StrategyStatusCollector_counter['task_generated'] = 0
        self._StrategyStatusCollector_counter['req_cnt'] = 0
        self._StrategyStatusCollector_counter['req_success'] = 0
        self._StrategyStatusCollector_counter['req_failed'] = 0
        
        
    def strategy_status_collector(self):
        return self._StrategyStatusCollector_counter
    
    
    def get_json(self):
        StrategyStatusJson = json.dumps(self._StrategyStatusCollector_counter, encoding = 'utf-8')
        return StrategyStatusJson
    

    def task_cnt_inc(self):
        self._StrategyStatusCollector_counter['task_cnt'] += 1
        return self._StrategyStatusCollector_counter['task_cnt']
        
    def task_success_inc(self):
        self._StrategyStatusCollector_counter['task_success'] += 1
        return self._StrategyStatusCollector_counter['task_success']
    
    def task_failed_inc(self):
        self._StrategyStatusCollector_counter['task_failed'] += 1
        return self._StrategyStatusCollector_counter['task_failed']
    
    def task_generated_inc(self):
        self._StrategyStatusCollector_counter['task_generated'] += 1
        return self._StrategyStatusCollector_counter['task_generated']
            
    def req_cnt_inc(self):
        self._StrategyStatusCollector_counter['http_req_cnt'] += 1
        return self._StrategyStatusCollector_counter['http_req_cnt']

    def req_success_inc(self):
        self._StrategyStatusCollector_counter['http_req_success'] += 1
        return self._StrategyStatusCollector_counter['http_req_success']
        
    def req_failed_inc(self): # both http exceptions and content exceptions, count the result of one invoke of spider.http_get ignore the retry
        self._StrategyStatusCollector_counter['http_req_failed'] += 1
        return self._StrategyStatusCollector_counter['http_req_failed']
        
        
        
        
class TaskStatus():
    # TaskStatus instantiate in spider
    # use for deducing the TaskStatus
    # not being upload via monitor
    
    def __init__(self, StrategyID = 'TEST'):
        self.start_collector()
        self._StrategyID = StrategyID

        

    def start_collector(self): # restart
        self._TaskStatusCollector_counter = Counter()
        
        self._TaskStatusCollector_counter['req_cnt'] = 0
        self._TaskStatusCollector_counter['req_success'] = 0
        self._TaskStatusCollector_counter['req_failed'] = 0
        
        
    def task_status_collector(self):
        return self._TaskStatusCollector_counter # {"req_success": 0, "req_failed": 0, "req_cnt": 0}
    
    
    def get_json(self):
        TaskStatusJson = json.dumps(self._TaskStatusCollector_counter, encoding = 'utf-8')
        return TaskStatusJson
    
            
    def req_cnt_inc(self):
        self._TaskStatusCollector_counter['http_req_cnt'] += 1
        return self._TaskStatusCollector_counter['http_req_cnt']

    def req_success_inc(self):
        self._TaskStatusCollector_counter['http_req_success'] += 1
        return self._TaskStatusCollector_counter['http_req_success']
        
    def req_failed_inc(self): # both http exceptions and content exceptions, count the result of one invoke of spider.http_get ignore the retry
        self._TaskStatusCollector_counter['http_req_failed'] += 1
        return self._TaskStatusCollector_counter['http_req_failed']
        
        

        
        
if __name__ == '__main__':
    MachineStatusIns_0 = MachineStatus()
    StrategyStatusIns_1 = StrategyStatus(MachineStatusIns_0, 'TEST_1')
     
    MachineStatusIns_1 = MachineStatus()
    StrategyStatusIns_2 = StrategyStatus(MachineStatusIns_1, 'TEST_2')
     
    StrategyStatusIns_1.task_cnt_inc()
    StrategyStatusIns_1.task_cnt_inc()
    StrategyStatusIns_1.task_cnt_inc()
     
    StrategyStatusIns_2.http_req_cnt_inc()
    StrategyStatusIns_2.http_req_cnt_inc()
     
    print StrategyStatusIns_1.get_json()
    print StrategyStatusIns_2.get_json()
     
    print MachineStatusIns_0.get_json()
    print MachineStatusIns_1.get_json()
    
    TaskStatusIns = TaskStatus('TEST_1')
    print TaskStatusIns.get_json()
