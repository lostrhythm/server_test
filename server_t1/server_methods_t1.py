# -*- coding:utf-8 -*-
'''
Created on 2017年7月12日

@author: Thinkpad
'''
from log.log import get_logger
from utils.data_operations import flatten_list, eliminate_none_items, eliminate_placeholders, strip_list
from new_task_dupefilter import New_Task_DupeFilter
from data_structure.task import Task
import connection
import defaults
import json
import os
import base64
import time
import traceback



class Server_Methods(object):
    def __init__(self, RedisIns, logger = None):
        self.logger = logger or get_logger('Server_Methods_t1')
        self.server = RedisIns
        self.New_Task_DupeFilte_Ins = New_Task_DupeFilter(RedisIns, logger)
    
    
    
    @classmethod
    def from_default(cls, logger = None):
        RedisIns = connection.get_redis_from_default()
        return cls(RedisIns, logger)
    
    
    
    def get_captcha_t1(self, *args, **kw):
        '''pending'''
        pass
    
    def get_proxy_t1(self, *args, **kw):
        '''pending'''
        pass
    
    
    
    def do_register_t1(self, UserInfoJson):
        UserInfo_dict = json.loads(UserInfoJson) 
        
        user = UserInfo_dict['user']
        password = UserInfo_dict['password'] 
                                             
        password_r = None
        
        try:
            password_r = self.server.hget('user:%s'%user, 'password') 
                                                                     
        except Exception as e:
            self.logger.warn(traceback.format_exc(e))

            
        if password == password_r:
            ComfirmInfo = 'Success in registering: %s'%str(user)
        else:
            ComfirmInfo = 'Failed in registering: %s'%str(user)
            
        self.logger.debug('user: %s, ComfirmInfo:%s'%(user, ComfirmInfo))
        
        return ComfirmInfo
            
        
            
    def get_strategy_t1(self):
        
        StrategyGroupJson = ''
        try:
            StrategyGroupJson = self.server.get('strategies') 
        except Exception as e:
            self.logger.warn(traceback.format_exc(e))
            
        if StrategyGroupJson == None:
            StrategyGroupJson = ''
            
        self.logger.info('get strategy: %s'%StrategyGroupJson) 
        return StrategyGroupJson
    
    
    
    def get_task_t1(self, TaskRequestJson):
        
        TaskRequest_dict = json.loads(TaskRequestJson)
        
        StrategyID = TaskRequest_dict.get('strategy_id')
        TasksBatchSize = TaskRequest_dict.get('tasks_batchsize') 
        User = TaskRequest_dict.get('user')
        
        TaskGroupList = []
        pipe = self.server.pipeline()
        
        
        try:
            UserStrategiesJson = self.server.get('user_strategies:%s'%User) or '[]'
            UserStrategies_List = strip_list( json.loads(UserStrategiesJson) ) 
            if StrategyID in UserStrategies_List:
                self.logger.info('Strategy %s is loaded to user %s'%(StrategyID, User))
                StrategyLoaded = True
            else:
                self.logger.info('Strategy %s is not loaded to user %s'%(StrategyID, User))
                StrategyLoaded = False
                
        except Exception as e:
            self.logger.warn(traceback.format_exc(e))
            StrategyLoaded = False
        
        
        if StrategyLoaded:
            
            
            try:
                pipe.multi()
                for _ in xrange(TasksBatchSize):
                    pipe.rpop('task_list:%s'%StrategyID) 
                TaskGroupList = eliminate_placeholders(eliminate_none_items( pipe.execute() )) 
            except Exception as e:
                self.logger.warn(traceback.format_exc(e))
            
            
            try:
                pipe.multi()
                for TaskJson in TaskGroupList:
                    TaskIns = Task.load_task(TaskJson)
                    pipe.lpush('user_tasks:%s'%User, TaskIns.TaskID) 
                pipe.execute()
            except Exception as e:
                self.logger.warn(traceback.format_exc(e))
            
            
            if TaskGroupList:
                TaskGroupJson = json.dumps(TaskGroupList)
            else:
                TaskGroupJson = ''
                
        else:
            TaskGroupJson = '' 
                
            
        self.logger.info('get %s tasks: %s'%(str(len(TaskGroupList)), TaskGroupJson)) 
        return TaskGroupJson 
    
    
    
    def _store_file(self, TaskID, ResultPack_zip):
        
        try:
            if not os.path.isdir('./results'):
                os.mkdir('./results')
                
            zipfilename = './results/' + str(TaskID) + '_' + str(int(time.time())) + '.zip'
            with open(zipfilename, 'wb') as zf:
                zf.write(ResultPack_zip)
                
        except Exception as e:
            self.logger.warn(traceback.format_exc(e))
               
                         
    def _upload_tasks(self, TaskJsonList):
        
        pipe = self.server.pipeline()
        try:
            pipe.multi()
            
            for TaskJson in TaskJsonList:
                pipe.lpush(defaults.PROCESSED_TASK_LIST, TaskJson) 
                
            pipe.execute()
            
        except Exception as e:
            self.logger.warn(traceback.format_exc(e))


    def _upload_new_tasks(self, NewTaskJsonListList):
        NewTaskJsonList = flatten_list(NewTaskJsonListList) 
        pipe = self.server.pipeline()
        try:
            pipe.multi()
            
            for NewTaskJson in NewTaskJsonList:
                if self.New_Task_DupeFilte_Ins.task_seen(NewTaskJson) == False:
                    
                    pipe.execute_command('ZADD', defaults.NEW_TASK_SSET, 'NX', time.time(), NewTaskJson) 
                else:
                    self.logger.info('new_task was seen: %s'%NewTaskJson)
                    
            cnt_list = map(int, pipe.execute()) 
            self.logger.info('new_task added: %s'%str(sum(cnt_list)))
            
        except Exception as e:
            self.logger.warn(traceback.format_exc(e))
            
            
    def upload_result_t1(self, UploadPackJson):

        UploadPack = json.loads(UploadPackJson)
        self.logger.debug(repr(UploadPack))
        
        TaskJsonList = [] 
        NewTaskJsonListList = [] 
        
        for TaskID in UploadPack:
            TaskJson, ResultPack_zip_b64, NewTaskJsonList = UploadPack[TaskID]
            ResultPack_zip = base64.b64decode(ResultPack_zip_b64)
            self._store_file(TaskID, ResultPack_zip) 

            TaskJsonList.append(TaskJson)
            NewTaskJsonListList.append(NewTaskJsonList)
            
        self._upload_tasks(TaskJsonList) 
        self._upload_new_tasks(NewTaskJsonListList) 
        
            
        ComfirmInfo = 'upload_server received TaskID: %s'%str(UploadPack.keys())
        self.logger.info(ComfirmInfo)
        
        return ComfirmInfo



    def upload_status_t1(self, UserCollectorMapJson):
        try:
            self.server.lpush(defaults.STATUS_LIST, UserCollectorMapJson) 
        except Exception as e:
            self.logger.warn(traceback.format_exc(e))
        
        ComfirmInfo = 'monitor_server received: %s'%UserCollectorMapJson
        self.logger.info(ComfirmInfo)
        
        return ComfirmInfo

    
if __name__ == '__main__':
    ServerMethodsIns = Server_Methods.from_default()
    
    UploadPackJson = '{"2": ["{\\"Processor\\":\\"\\",\\"Encoding\\": \\"utf-8\\", \\"TaskStatus\\": 0, \\"ParentID\\": -1, \\"TaskID\\": 2, \\"TaskType\\": 0, \\"StrategyID\\": \\"TEST\\", \\"AdditionParams\\": \\"{\\\\\\"a\\\\\\": 2}\\", \\"TaskContent\\": \\"\\"}", "UEsDBBQAAAAIACqy7UqpMMX+CQAAAAcAAAAOAAAAMi9maWxlbmFtZS5qcGdLzs8rSc0rAQBQSwMEFAAAAAgAKrLtStLMnsUUAAAAEgAAAA4AAAAyL25ld3Rhc2suaHRtbMtLLVcoSSzO9swrVsgqzs9TKAYAUEsBAhQAFAAAAAgAKrLtSqkwxf4JAAAABwAAAA4AAAAAAAAAAAAAALaBAAAAADIvZmlsZW5hbWUuanBnUEsBAhQAFAAAAAgAKrLtStLMnsUUAAAAEgAAAA4AAAAAAAAAAAAAALaBNQAAADIvbmV3dGFzay5odG1sUEsFBgAAAAACAAIAeAAAAHUAAAAAAA==", ["NewTaskJson_1", "NewTaskJson_2"]]}'
    ServerMethodsIns.upload_result_t1(UploadPackJson)
    
    ServerMethodsIns.get_strategy_t1()
    
    TaskRequestJson = json.dumps({'strategy_id' : 'TEST_1', 'tasks_batchsize' : 5, 'user' : 'test_vps_ip'})
    ServerMethodsIns.get_task_t1(TaskRequestJson)
    
    UserCollectorMapJson = UploadedStatus_Json = '["test_vps_ip", {"TEST_2": {"req_failed": 0, "task_generated": 0, "task_failed": 0, "task_cnt": 0, "req_cnt": 0, "req_success": 0, "task_success": 0}, "TEST_1": {"req_failed": 0, "task_generated": 0, "task_failed": 0, "task_cnt": 0, "req_cnt": 0, "req_success": 0, "task_success": 0}}]'
    ServerMethodsIns.upload_status_t1(UserCollectorMapJson)
    
    UserInfoJson = json.dumps({'user' : 'test_vps_ip', 'password' : '123'})
    ServerMethodsIns.do_register_t1(UserInfoJson)