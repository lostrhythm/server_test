# -*- coding:utf-8 -*-
'''
Created on 2017年6月19日

@author: Thinkpad
'''
import json
from collections import Counter
from utils.decorators import Singleton
from time import time
from log.log import get_logger
logger = get_logger('status')
 
 
 
@Singleton 
class MachineStatus():
    
    def __init__(self, user = 'test_vps_ip'): 
        self._user = user 
        self._MachineStatusCollector_dict = {} 
        
    def machine_status_collector(self):
        return self._MachineStatusCollector_dict
    
    def get_user(self):
        return self._user
    
    def get_json(self): 
        MachineStatusJson = json.dumps(self._MachineStatusCollector_dict, 'utf-8')
        return MachineStatusJson
    


        
    
class StrategyStatus():
    
    def __init__(self, MachineStatusIns, StrategyID = 'TEST'):
        self.start_collector()
        
        self._StrategyID = StrategyID
        self._MachineStatusCollector_dict = MachineStatusIns.machine_status_collector()
        
        if not self._MachineStatusCollector_dict.has_key(self._StrategyID): 
            self._MachineStatusCollector_dict[self._StrategyID] = self._StrategyStatusCollector_counter
            
            
        else:
            logger.warn('_MachineStatusCollector_dict has already contain the strategy name: %s'%self._StrategyID)
            raise KeyError

    def start_collector(self): 
        self._StrategyStatusCollector_counter = Counter()
        
        self._StrategyStatusCollector_counter['RT_c'] = 0 
        self._StrategyStatusCollector_counter['ST_c'] = 0 
        self._StrategyStatusCollector_counter['FT_c'] = 0 
        self._StrategyStatusCollector_counter['GT_c'] = 0 
        self._StrategyStatusCollector_counter['TR_c'] = 0 
        self._StrategyStatusCollector_counter['SR_c'] = 0 
        self._StrategyStatusCollector_counter['FR_c'] = 0 
        
        
    def strategy_status_collector(self):
        return self._StrategyStatusCollector_counter
    
    
    def get_json(self):
        
        StrategyStatusJson = json.dumps(self._StrategyStatusCollector_counter, encoding = 'utf-8')
        return StrategyStatusJson
    

    def task_cnt_inc(self):
        self._StrategyStatusCollector_counter['RT_c'] += 1
        return self._StrategyStatusCollector_counter['RT_c']
        
    def task_success_inc(self):
        self._StrategyStatusCollector_counter['ST_c'] += 1
        return self._StrategyStatusCollector_counter['ST_c']
    
    def task_failed_inc(self):
        self._StrategyStatusCollector_counter['FT_c'] += 1
        return self._StrategyStatusCollector_counter['FT_c']
    
    def task_generated_inc(self):
        self._StrategyStatusCollector_counter['GT_c'] += 1
        return self._StrategyStatusCollector_counter['GT_c']
            
    def req_cnt_inc(self):
        self._StrategyStatusCollector_counter['TR_c'] += 1
        return self._StrategyStatusCollector_counter['TR_c']

    def req_success_inc(self):
        self._StrategyStatusCollector_counter['SR_c'] += 1
        return self._StrategyStatusCollector_counter['SR_c']
        
    def req_failed_inc(self): 
        self._StrategyStatusCollector_counter['FR_c'] += 1
        return self._StrategyStatusCollector_counter['FR_c']
        
        
        
        
class TaskStatus():
    
    def __init__(self, StrategyID = 'TEST'):
        self.start_collector()
        self._StrategyID = StrategyID

        

    def start_collector(self): 
        self._TaskStatusCollector_counter = Counter()
        
        self._TaskStatusCollector_counter['TR_c'] = 0
        self._TaskStatusCollector_counter['SR_c'] = 0
        self._TaskStatusCollector_counter['FR_c'] = 0
        
        
    def task_status_collector(self):
        return self._TaskStatusCollector_counter 
    
    
    def get_json(self):
        TaskStatusJson = json.dumps(self._TaskStatusCollector_counter, encoding = 'utf-8')
        return TaskStatusJson
    
            
    def req_cnt_inc(self):
        self._TaskStatusCollector_counter['TR_c'] += 1
        return self._TaskStatusCollector_counter['TR_c']

    def req_success_inc(self):
        self._TaskStatusCollector_counter['SR_c'] += 1
        return self._TaskStatusCollector_counter['SR_c']
        
    def req_failed_inc(self): 
        self._TaskStatusCollector_counter['FR_c'] += 1
        return self._TaskStatusCollector_counter['FR_c']
        
        

        
        
if __name__ == '__main__':
    MachineStatusIns_0 = MachineStatus()
    StrategyStatusIns_1 = StrategyStatus(MachineStatusIns_0, 'TEST_1')
     
    MachineStatusIns_1 = MachineStatus()
    StrategyStatusIns_2 = StrategyStatus(MachineStatusIns_1, 'TEST_2')
     
    StrategyStatusIns_1.task_cnt_inc()
    StrategyStatusIns_1.task_cnt_inc()
    StrategyStatusIns_1.task_cnt_inc()
     
    StrategyStatusIns_2.req_cnt_inc()
    StrategyStatusIns_2.req_cnt_inc()
     
    print StrategyStatusIns_1.get_json()
    print StrategyStatusIns_2.get_json()
     
    print MachineStatusIns_0.get_json()
    print MachineStatusIns_1.get_json()
    
    TaskStatusIns = TaskStatus('TEST_1')
    print TaskStatusIns.get_json()
