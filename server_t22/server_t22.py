# -*- coding:utf-8 -*-
'''
Created on 2017年7月24日

@author: Thinkpad
'''
from threading import Thread
from log.log import get_logger
from time import sleep, time    
from utils.data_operations import row_add, column_add                  
import connection
import traceback
import json
import defaults


class Server_T22():
    def __init__(self, RedisIns, SockIns, logger = None):
        self.logger = logger or get_logger('Server_Methods_t22', True)
        self.server = RedisIns
        self.sock = SockIns

    @classmethod
    def from_default(cls, logger = None):
        RedisIns = connection.get_redis_from_default()
        SockIns = connection.get_graphite_socket()
        return cls(RedisIns, SockIns, logger)
    
    
    def _raw_to_matrix_dict(self):
        '''
        [ 'r1',
        123,
        {'c1':{'t1':1, 't2':1}, 'c2':{'t1':2, 't2':2}} ]
        
        [ 'r2',
        123,
        {'c1':{'t1':3, 't2':3}, 'c2':{'t1':4, 't2':4}} ]
        
        -->
        
        matrix_dict = {
               'MACHINE.r1':{'STRATEGY.c1':{'t1':1, 't2':1}, 'STRATEGY.c2':{'t1':2, 't2':2}},
               'MACHINE.r2':{'STRATEGY.c1':{'t1':3, 't2':3}, 'STRATEGY.c2':{'t1':4, 't2':4}}
               
               }
        
        '''
        matrix_dict = {}
        StatusGroupList = [] 
        
        
        for _ in xrange(defaults.GRAPHITE_PARAMS['upload_max_batchsize']):
            
            try:
                StatusJson = self.server.rpop('status_list')
                if StatusJson and StatusJson != 'placeholder':
                    Status_list = json.loads(StatusJson)
                    StatusGroupList.append(Status_list)
                else:
                    break
            
            except Exception as e:
                self.logger.warn(traceback.format_exc(e))
        
        
        
            
            
        
        for Status_list in StatusGroupList:
            User = Status_list[0]
            MachineStatusCollector_dict = Status_list[2]
            
            MachineKey = defaults.GRAPHITE_PARAMS['machine_key']%User 
            
            MachineStatusDict = {} 
            for StrategID in MachineStatusCollector_dict:
                StrategyKey = defaults.GRAPHITE_PARAMS['strategy_key']%StrategID 
                
                MachineStatusDict[StrategyKey] = MachineStatusCollector_dict[StrategID] 
            
            matrix_dict[MachineKey] = MachineStatusDict
        
        return matrix_dict
    
    
    def _do_aggregratet(self):
        
        Detailed_matrix_dict = self._raw_to_matrix_dict()
        Machine_matrix_dict = row_add(Detailed_matrix_dict) 
        Strategy_matrix_dict = column_add(Detailed_matrix_dict)
        Plain_matrix_dict = column_add(Machine_matrix_dict) 
        
        return Detailed_matrix_dict, Machine_matrix_dict, Strategy_matrix_dict, Plain_matrix_dict
    
    def _get_metricgroup(self):
        MetricTemplate_str = "\n%s %s {timestamp}\n"
        Detailed_matrix_dict, Machine_matrix_dict, Strategy_matrix_dict, Plain_matrix_dict = self._do_aggregratet()
        
        MetricGroup_str = ''
        templist = ['','','']
        for MachineKey in Detailed_matrix_dict:
            templist[0] = MachineKey
            MachineStatusCollector_dict = Detailed_matrix_dict[MachineKey]
            
            for StrategyKey in MachineStatusCollector_dict:
                templist[1] = StrategyKey
                StrategyStatusCollector_dict = MachineStatusCollector_dict[StrategyKey]
                
                for CountKey in StrategyStatusCollector_dict:
                    templist[2] = CountKey
                    MetricKeyStr = '.'.join(templist)
                    value = StrategyStatusCollector_dict[CountKey]
    
                    MetricGroup_str += MetricTemplate_str%( MetricKeyStr , str(value) )
        
        templist = ['', defaults.GRAPHITE_PARAMS['strategies_aggregated_key'], '']
        for MachineKey in Machine_matrix_dict:
            templist[0] = MachineKey
            StatusCollector_dict = Machine_matrix_dict[MachineKey] 
            
            for CountKey in StatusCollector_dict:
                templist[2] = CountKey
                MetricKeyStr = '.'.join(templist)
                value = StatusCollector_dict[CountKey]

                MetricGroup_str += MetricTemplate_str%( MetricKeyStr , str(value) )
        
        templist = ['', defaults.GRAPHITE_PARAMS['machines_aggregated_key'], '']
        for StrategyKey in Strategy_matrix_dict:
            templist[0] = StrategyKey
            StatusCollector_dict = Strategy_matrix_dict[StrategyKey] 
            
            for CountKey in StatusCollector_dict:
                templist[2] = CountKey
                MetricKeyStr = '.'.join(templist)
                value = StatusCollector_dict[CountKey]

                MetricGroup_str += MetricTemplate_str%( MetricKeyStr , str(value) )
        
        templist = [defaults.GRAPHITE_PARAMS['total_key'], '']
        for CountKey in Plain_matrix_dict:
            templist[1] = CountKey
            MetricKeyStr = '.'.join(templist)
            value = Plain_matrix_dict[CountKey]

            MetricGroup_str += MetricTemplate_str%( MetricKeyStr , str(value) )
            
        print MetricGroup_str
        
        return MetricGroup_str
    
    
    def upload_status(self):
        
        while True:
            try:
                self.logger.info('upload status START, time interval: %s'%str(defaults.UPLOAD_STATUS_TIMEINTERVAL))
                
                MetricGroup_str =self._get_metricgroup()
                MetricGroup_str = MetricGroup_str.format( timestamp = str(int(time())) ) 
                if MetricGroup_str:
                    self.sock.sendall(MetricGroup_str)
                
                self.logger.info('upload status END: %s'%str(MetricGroup_str[:10]))
                
            except Exception as e:
                self.logger.warn(traceback.format_exc(e))
            
            finally:
                sleep(defaults.UPLOAD_STATUS_TIMEINTERVAL)
                
                
    def start_get_upload_thread(self):
        UploadStatus_thread = Thread(target=self.upload_status)
        UploadStatus_thread.start()


    def start_threads(self):
        self.start_get_upload_thread()
    
    
    
    
    
if __name__ == '__main__':
    Server_T22_Ins = Server_T22.from_default()
    Server_T22_Ins.start_threads()