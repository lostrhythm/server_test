# -*- coding:utf-8 -*-
'''
Created on 2017年7月15日

@author: Thinkpad
'''
from threading import Thread,Lock
from log.log import get_logger
from time import sleep, time
from utils.data_operations import vallist_from_dictlist, \
                                    list_to_tuplelist, \
                                    eliminate_none_items, \
                                    eliminate_placeholders, \
                                    safe_remove, \
                                    dictlist_to_tuplelist
                                    
from data_structure.strategy import Strategy
from data_structure.task import Task
import connection
import traceback
import json



class Server_T21():
    def __init__(self, RedisIns, MySqlConn, logger = None):
        self.logger = logger or get_logger('Server_Methods_t21')
        self.server = RedisIns
        self.conn = MySqlConn
        self.cursor = MySqlConn.cursor(dictionary=True)
        self.lock = Lock()
        self.StrategyGroupDict = {}
        
        self.ConfigDict = {}
        self.load_config()
        
        
        
    def execute_sql(self, sqline, data = []):
        sqlresultlist = []
        self.lock.acquire()
        if not data:
            # single sqline
            self.cursor.execute(sqline)
            sqlresultlist = self.cursor.fetchall()
        else:
            # multi sqline s
            if 'SELECT' in sqline or 'select' in sqline:
                for item in data:
                    tempsqline = sqline%item
                    self.cursor.execute(tempsqline)
                    sqlresultlist.extend(self.cursor.fetchall())
                    
            if 'UPDATE' in sqline or 'update' in sqline or 'INSERT' in sqline or 'insert' in sqline:
                if not data[0].__class__ == tuple().__class__:
                    data = list_to_tuplelist(data)
                    
                self.cursor.executemany(sqline, data)

        self.lock.release()
        return sqlresultlist
    
        
    def get_redis_keys(self, RedisPattern, HashKey = None):
        keyslist = []
        PrevRedisCursor = 0
        while True:
            if not HashKey:
                CurRedisCursor_long, subkeyslist = self.server.scan(PrevRedisCursor, RedisPattern, count = 50)
                CurRedisCursor = int(CurRedisCursor_long)
                if CurRedisCursor == 0:
                    keyslist.extend(subkeyslist)
                    break
                else:
                    PrevRedisCursor = CurRedisCursor
                    keyslist.extend(subkeyslist)
                    
            else:
                if HashKey.__class__ == str().__class__:
                    CurRedisCursor_long, subfieldsdict = self.server.hscan(HashKey, PrevRedisCursor, RedisPattern, count = 2)
                    CurRedisCursor = int(CurRedisCursor_long) # scan always return (long_int, list)
                    if CurRedisCursor == 0:
                        keyslist.extend(subfieldsdict.keys())
                        break
                    else:
                        PrevRedisCursor = CurRedisCursor
                        keyslist.extend(subfieldsdict.keys())
                else:
                    self.logger.warn('HashKey must be string type')
                
        return keyslist
        
        
        
    def load_config(self):
        try:
            sqline = "SELECT * FROM Config WHERE AimObject = 'server_t21'"
            sqlresultlist = self.execute_sql(sqline)
            self.ConfigDict = sqlresultlist[0]
            
        except Exception as e:
            self.logger.warn(traceback.format_exc(e))
            
        
        self.logger.info('Config loaded: %s'%str(self.ConfigDict))

            
    def update_config(self):
        while True:
            sleep(self.ConfigDict['UpdateConfigInterval'])
            self.logger.info('---Update config START')
            self.load_config()
            self.logger.info('---Update config END')

 

    
    
    @classmethod
    def from_default(cls, logger = None):
        RedisIns = connection.get_redis_from_default()
        MySqlConn = connection.get_myconn_from_default()
        return cls(RedisIns, MySqlConn, logger)
    
    

    def generate_user_infos(self):
        
        sqline = 'select * from UserInfo'
        PrevUserInfoList = []
        
        while True:
            try:
                CurUserInfoList = self.execute_sql(sqline)
                self.logger.info('UserInfo got:%s'%str(CurUserInfoList))
                
                if CurUserInfoList == PrevUserInfoList:
                    self.logger.info('User Information are not changed')
                else:
                    self.logger.info('User Information changed')
                    PrevUserInfoList = CurUserInfoList # local cache []
                    
                    RedisUserInfoKeyList = self.get_redis_keys('user:*')
                    
                    pipe = self.server.pipeline()
                    pipe.multi()
                    
                    for UserInfoKey in RedisUserInfoKeyList:
                        pipe.delete(UserInfoKey)
                    
                    for UserInfo in CurUserInfoList:
                        pipe.hset('user:%s'%UserInfo['UserID'], 'password', UserInfo['Password'] or '') # Password never be None, at least ''; 'or' here is for the accidently delete of password in db 
                                           
                    pipe.execute()
                    
                    UserIDList = vallist_from_dictlist(CurUserInfoList, 'UserID')
                    self.logger.info( 'User Information setted: %s '%str(UserIDList) )
                    
            except Exception as e:
                self.logger.warn(traceback.format_exc(e))
                   
            sleep(self.ConfigDict['GenerateUserInfoInterval'])
    
    
    
    def generate_user_strategies(self):
        sqline = 'select * from UserStrategies'
        PrevUserStrategiesList = []
        
        while True:
            try:
                
                CurUserStrategiesList = self.execute_sql(sqline)
                self.logger.info('UserStrategies got:%s'%str(CurUserStrategiesList))
                
                if CurUserStrategiesList == PrevUserStrategiesList:
                    self.logger.info('User Strategies are not changed')
                else:
                    self.logger.info('User Strategies changed')
                    PrevUserStrategiesList = CurUserStrategiesList # local cache []
                    
                    UserStrategiesKeyList = self.get_redis_keys('user_strategies:*')
                    
                    pipe = self.server.pipeline()
                    pipe.multi()
                    
                    for UserStrategiesoKey in UserStrategiesKeyList:
                        pipe.delete(UserStrategiesoKey)
                    
                    for UserStrategies in CurUserStrategiesList:
                        UserStrategiesList = UserStrategies['LoadedStrategies'].split(',')
                        UserStrategiesJson = json.dumps(UserStrategiesList, 'utf-8')
                        pipe.set('user_strategies:%s'%UserStrategies['UserID'], UserStrategiesJson) # Password never be None, at least ''; 'or' here is for the accidently delete of password in db 
                                           
                    pipe.execute()
                    
                    UserIDList = vallist_from_dictlist(CurUserStrategiesList, 'UserID')
                    self.logger.info( 'User Strategies setted: %s'%str(UserIDList) )
                    
            except Exception as e:
                self.logger.warn(traceback.format_exc(e))
            
            sleep(self.ConfigDict['GenerateUserStrategiesInterval'])





    
    
    def _delete_fields_of_tasklimit(self, TaskIDList=[]):
        
        try:
            pipe = self.server.pipeline()
            pipe.multi()
            for TaskID in TaskIDList:
                pipe.hdel('task_timelimit', TaskID) # delete the task_list
            pipe.execute()
            
            self.logger.info('delete from task_timelimit taskID: %s'%str(TaskIDList))
        except Exception as e:
            self.logger.warn(traceback.format_exc(e))
    
    
    def _reset_undistributed_tasks_status(self, EliStrategyID):
        
        TaskIDList = []
        sqline = 'update Tasks set Taskstatus = -1 where TaskID = %s;'
        
        try:
            TaskListLen = self.server.llen('task_list:%s'%EliStrategyID)
            
            pipe = self.server.pipeline()
            pipe.multi()
            for _ in xrange(TaskListLen):
                pipe.rpop('task_list:%s'%EliStrategyID)
            TaskJsonList = pipe.execute()
            TaskJsonList = eliminate_placeholders(eliminate_none_items( TaskJsonList ))
            
            for TaskJson in TaskJsonList:
                TaskIns = Task.load_task(TaskJson)
                TaskIDList.append(TaskIns.TaskID)
            
            self._delete_fields_of_tasklimit(TaskIDList)
            
            if TaskIDList:
                self.execute_sql(sqline, TaskIDList)
            
            self.logger.info('reset task status for tasks: %s'%str(TaskIDList))
        except Exception as e:
            self.logger.warn(traceback.format_exc(e))

    
    def _delete_elistrategy_tasklist(self, EliStrategIDList = []): # eliminated strategID s
        try:
            
            pipe = self.server.pipeline()
            pipe.multi()
            for EliStrategyID in EliStrategIDList:
                self._reset_undistributed_tasks_status(EliStrategyID) # reset task status for the elistrategy
                pipe.delete('task_list:%s'%EliStrategyID) # delete the task_list
            pipe.execute()
            
            self.logger.info('delete task list for eliminated strategies:%s'%str(EliStrategIDList))
        except Exception as e:
            self.logger.warn(traceback.format_exc(e))
    
    
    def generate_strategies(self):
        sqline = 'select * from Strategies'

        while True:
            try:
                StrategiesList = self.execute_sql(sqline) # [{},...]
                self.logger.info('Strategies got:%s'%str(StrategiesList))
                
                StrategyGroupDict_cur = {} # ['StrategyID':'StrategyJson', ...]
                
                
                for SGStrategyDict in StrategiesList: # sql get strategy dict
                    
                    StrategyIns = Strategy.load_strategy_from_sqlresult(SGStrategyDict)
                    StrategyJson = StrategyIns.get_json()
                    StrategyGroupDict_cur[StrategyIns.StrategyID] = StrategyJson
                    
                StrategyGroupJson = json.dumps(StrategyGroupDict_cur, 'utf-8')
                self.server.set('strategies', StrategyGroupJson)
                
                StrategyIDList = StrategyGroupDict_cur.keys()
                self.logger.info('Strategies genereated: %s'%str(StrategyIDList))
                
                
                EliStrategIDList = list(self.StrategyGroupDict.viewkeys() - StrategyGroupDict_cur.viewkeys())
                self.StrategyGroupDict = StrategyGroupDict_cur
                
                self._delete_elistrategy_tasklist(EliStrategIDList)
                
                
            except Exception as e:
                self.logger.warn(traceback.format_exc(e))
                
            sleep(self.ConfigDict['GenerateStrategyInterval'])
        


    def _deal_expire_tasks(self):
        sqline_w = 'update Tasks set TaskStatus = -4 where TaskID = %s;'
        
        try:
            # check task timeout
            CurTimeStamp = time()
            ExpiredTaskIDList = []
            GeneratedTaskIDList_orig = self.get_redis_keys('*', 'task_timelimit')
            
            for GeneratedTaskID in GeneratedTaskIDList_orig: 
                TaskTimelimit = self.server.hget('task_timelimit', GeneratedTaskID)
                if CurTimeStamp > float(TaskTimelimit):
                    ExpiredTaskIDList.append(GeneratedTaskID)
                   
            pipe = self.server.pipeline()
            pipe.multi()
            for ExGeneratedTaskID in ExpiredTaskIDList:
                pipe.hdel('task_timelimit', ExGeneratedTaskID)
            pipe.execute()
              
            if ExpiredTaskIDList:
                self.execute_sql(sqline_w, ExpiredTaskIDList)
                
            self.logger.info('Expired Tasks: %s'%str(ExpiredTaskIDList))

        except Exception as e:
            self.logger.warn(traceback.format_exc(e))
                
                


    def generate_tasks(self):
        sqline_r = 'select * from Tasks where TaskStatus = -1 and StrategyID = \'%s\' order by Priority desc limit 0, %s;'
        sqline_w_1 = 'update Tasks set TaskStatus = -2 where TaskID = %s;'
        sqline_w_2 = 'update Tasks set TaskStatus = -3 where TaskID = %s and Processor is not NULL;' # for restore status -3
        sqline_w_3 = 'update Tasks set TaskStatus = -2 where TaskID = %s and Processor is NULL;' # restore status -2
        
        while True:
            try:
                self._deal_expire_tasks() # check and clean task_timelimit
                
                GenerateTaskBatchSize = str(self.ConfigDict['GenerateTaskBatchSize']) # put here due to listening to the change in table Config
                StrategyIDList = self.StrategyGroupDict.keys() # all active strategies
                GenTasksList = []
                
                
                for StrategyID in StrategyIDList:
                    sqline_temp = sqline_r % (StrategyID, GenerateTaskBatchSize)
                    
                    StrategyTaskListLen = self.server.llen('task_list:%s'%StrategyID) # len of task_list:strategy
                    if StrategyTaskListLen < self.ConfigDict['TaskListMinSize']:
                        
                        StrGenTasksList = self.execute_sql(sqline_temp) # strategy generate task, just for one strategy
                        GenTasksList.extend(StrGenTasksList)
                        
                        StrGenTaskIDsList = vallist_from_dictlist(StrGenTasksList, 'TaskID')
                        self.logger.info('Strategy: %s, got Tasks:%s' % (StrategyID, str(StrGenTaskIDsList)) )
                        
                    else:
                        self.logger.info('Too many tasks stock in task_list: %s'%StrategyID)

                

               
                GenTaskIDList = vallist_from_dictlist(GenTasksList, 'TaskID')
                ReTaskIDList = [] # filled with TaskID s that need to be restore status
                
                for SGTaskDict in GenTasksList: # sql get tasks dict
                    TaskIns = Task.load_task_from_sqlresult(SGTaskDict)
                    StrategyID = SGTaskDict['StrategyID']
                    
                    # record timelimit
                    sign = self.server.hsetnx('task_timelimit', TaskIns.TaskID, time() + self.ConfigDict['TaskTimeout']) # 0, field existed, drop the operation
                    
                    if not sign == 0:
                        self.server.lpush('task_list:%s'%StrategyID, TaskIns.get_json())
                    
                    else:
                        GenTaskIDList = safe_remove(GenTaskIDList, TaskIns.TaskID) # remove the -2/-3 taskID s
                        ReTaskIDList.append( TaskIns.TaskID ) # filled with 2/3 taskID s
                        
                        self.logger.warn('NOT GEN, task %s has already been existing in the system (hash task_timelimit), i.e. in status 2/3' % TaskIns.TaskID)


                
                if GenTaskIDList:
                    self.execute_sql(sqline_w_1, GenTaskIDList)
                    
                if ReTaskIDList:
                    self.execute_sql(sqline_w_2, ReTaskIDList) # restore -3
                    self.execute_sql(sqline_w_3, ReTaskIDList) # restore -2
                    
                self.logger.info( '%s Tasks genereated for Strategy: %s' % (str(len(GenTaskIDList)), str(StrategyIDList)) )
                

            except Exception as e:
                self.logger.warn(traceback.format_exc(e))
            
            sleep(self.ConfigDict['GenerateTaskInterval'])

       
            
    def check_tasks_distribution(self):
        sqline = 'update Tasks set TaskStatus = -3, Processor = %s where TaskID = %s;'
        
        while True:
            try:
                AllUserTaskIDTupleList = []
                UserTasksKeyList = self.get_redis_keys('user_tasks:*')
                for UserTasksKey in UserTasksKeyList:
                    
                    TaskIDList = []
                    UserTasksListLen = self.server.llen(UserTasksKey) # O(1)
                    for _ in xrange(UserTasksListLen):
                        TaskID = self.server.rpop(UserTasksKey)
                        TaskIDList.append(TaskID)

                    TaskIDList = eliminate_placeholders( eliminate_none_items(TaskIDList) )
                    User = UserTasksKey.split(':')[1]
                    templist = zip([User]*len(TaskIDList), TaskIDList)
                    
                    AllUserTaskIDTupleList.extend(templist)
                    
                    # TEST
                    print AllUserTaskIDTupleList
                    
                if AllUserTaskIDTupleList:
                    self.execute_sql(sqline, AllUserTaskIDTupleList) # write processor to table Tasks
                    
                self.logger.info('update task status and processor for tasks%s'%str(AllUserTaskIDTupleList))
                
                    
            except Exception as e:
                self.logger.warn(traceback.format_exc(e))
            
            sleep(self.ConfigDict['CheckTaskDistributionInterval'])
            


    def _upload_processed_tasks(self):
        sqline_w_1 = 'insert into TasksProcessed (TaskID, StrategyID, ParentID, TaskType, TaskStatus, TaskContent, Encoding, AdditionParams, Processor, Priority) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        sqline_w_2 = 'update Tasks set TaskStatus = -5 where TaskID = %s;'
        
        try:
            ProcessedTaskDictList = [] # [TaskDict, ...], prepare for upload
            
            pipe = self.server.pipeline()
            pipe.multi()
            for _ in xrange(self.ConfigDict['UploadTaskBatchSize']):
                pipe.rpop('processed_task_list')
            ProcessedTaskJsonList = eliminate_placeholders(eliminate_none_items( pipe.execute() )) # may have None, as BatchSize is 5, but only 2 items left
            
            pipe = self.server.pipeline()
            pipe.multi()
            for ProcessedTaskJson in ProcessedTaskJsonList:
                ProcessedTaskIns = Task.load_task(ProcessedTaskJson)
                
                if self.server.hget('task_timelimit', ProcessedTaskIns.TaskID):
                    ProcessedTaskDictList.append(ProcessedTaskIns.get_sgdict()) # construct TaskDict upload list
                    pipe.hdel('task_timelimit', ProcessedTaskIns.TaskID)
                    
                else:
                    # rec PTask expired
                    self.logger.info('drop a received expired task: %s'%str(ProcessedTaskIns.TaskID))
                    
            pipe.execute()
            
            if ProcessedTaskDictList: # else: all processed tasks are expired
                
                TaskIDList = vallist_from_dictlist(ProcessedTaskDictList, 'TaskID', eli_none= False)
                StrategyIDList = vallist_from_dictlist(ProcessedTaskDictList, 'StrategyID', eli_none= False)
                ParentIDList = vallist_from_dictlist(ProcessedTaskDictList, 'ParentID', eli_none= False)
                TaskTypeList = vallist_from_dictlist(ProcessedTaskDictList, 'TaskType', eli_none= False)
                TaskStatusList = vallist_from_dictlist(ProcessedTaskDictList, 'TaskStatus', eli_none= False)
                TaskContentList = vallist_from_dictlist(ProcessedTaskDictList, 'TaskContent', eli_none= False)
                EncodingList = vallist_from_dictlist(ProcessedTaskDictList, 'Encoding', eli_none= False)
                AdditionParamsList = vallist_from_dictlist(ProcessedTaskDictList, 'AdditionParams', eli_none= False)
                ProcessorList = vallist_from_dictlist(ProcessedTaskDictList, 'Processor', eli_none= False)
                Priority = vallist_from_dictlist(ProcessedTaskDictList, 'Priority', eli_none= False)
                
                data = zip(TaskIDList, StrategyIDList, ParentIDList, TaskTypeList, TaskStatusList, TaskContentList, EncodingList, AdditionParamsList, ProcessorList, Priority)
                self.execute_sql(sqline_w_1, data)

                self.execute_sql(sqline_w_2, TaskIDList)

            self.logger.info('uploaded not expired processed tasks, %s'%str( vallist_from_dictlist(ProcessedTaskDictList, 'TaskID') ))
            
        except Exception as e:
            self.logger.warn(traceback.format_exc(e))
            
            
    def _upload_new_tasks(self):
        sqline_w = 'insert into Tasks (StrategyID, ParentID, TaskType, TaskStatus, TaskContent, Encoding, AdditionParams, Priority) values (%s, %s, %s, -1, %s, %s, %s, %s)'
        
        try:
            # get new tasks
            NewTaskDictList = [] # [TaskDict, ...], prepare for upload
           
            pipe = self.server.pipeline()
            pipe.multi()
            pipe.zrange('new_task_sset', 0, self.ConfigDict['UploadTaskBatchSize'] - 1).zremrangebyrank('new_task_sset', 0, self.ConfigDict['UploadTaskBatchSize'] - 1)
            NewTaskJsonList, _ = pipe.execute()
            NewTaskJsonList = eliminate_placeholders(eliminate_none_items( NewTaskJsonList )) # may have None, as BatchSize is 5, but only 2 items left
    
            # upload new tasks
            pipe = self.server.pipeline()
            pipe.multi()
            for NewTaskJson in NewTaskJsonList:
                NewTaskIns = Task.load_task(NewTaskJson)
                NewTaskDictList.append(NewTaskIns.get_sgdict())
            
            pipe.execute()
            
            if NewTaskDictList:
                # write Tasks
                StrategyIDList = vallist_from_dictlist(NewTaskDictList, 'StrategyID', eli_none= False)
                ParentIDList = vallist_from_dictlist(NewTaskDictList, 'ParentID', eli_none= False)
                TaskTypeList = vallist_from_dictlist(NewTaskDictList, 'TaskType', eli_none= False)
                TaskContentList = vallist_from_dictlist(NewTaskDictList, 'TaskContent', eli_none= False)
                EncodingList = vallist_from_dictlist(NewTaskDictList, 'Encoding', eli_none= False)
                AdditionParamsList = vallist_from_dictlist(NewTaskDictList, 'AdditionParams', eli_none= False)
                Priority = vallist_from_dictlist(NewTaskDictList, 'Priority', eli_none= False)
                
                data = zip(StrategyIDList, ParentIDList, TaskTypeList, TaskContentList, EncodingList, AdditionParamsList, Priority)            
                self.execute_sql(sqline_w, data)
                
            self.logger.info('uploaded new tasks, generated by tasks: %s'%str( vallist_from_dictlist(NewTaskDictList, 'ParentID') ))

        except Exception as e:
            self.logger.warn(traceback.format_exc(e))


    def upload_tasks(self):        
        while True:
            self._deal_expire_tasks()
            self._upload_processed_tasks()
            self._upload_new_tasks()
            
            sleep(self.ConfigDict['UploadTaskInterval'])

    
    
    
    
    def start_update_config_thread(self):
        self.logger.info('---start_update_config_thread---')
        UpdateConfigThread = Thread(target = self.update_config)
        UpdateConfigThread.start()
        
    def start_generate_user_infos_thread(self):
        self.logger.info('---start_generate_user_info_thread---')
        GenerateUserInfosThread = Thread(target = self.generate_user_infos)
        GenerateUserInfosThread.start()
    
    def start_generate_user_strategies_thread(self):
        self.logger.info('---start_generate_user_strategy_thread---')
        GenerateUserStrategiesThread = Thread(target = self.generate_user_strategies)
        GenerateUserStrategiesThread.start()
    
    def start_generate_strategies_thread(self):
        self.logger.info('---start_generate_strategy_thread---')
        GenerateStrategiesThread = Thread(target = self.generate_strategies)
        GenerateStrategiesThread.start()
    
    def start_generate_tasks_thread(self):
        self.logger.info('---start_generate_tasks_thread---')
        GenerateTasksThread = Thread(target = self.generate_tasks)
        GenerateTasksThread.start()
        
    def start_check_tasks_distribution_thread(self):
        self.logger.info('---check_tasks_distribution---')
        CheckTasksDistributionThread = Thread(target = self.check_tasks_distribution)
        CheckTasksDistributionThread.start()
    
    def start_upload_tasks_thread(self):
        self.logger.info('---start_upload_tasks_thread---')
        UploadTasksThread = Thread(target = self.upload_tasks)
        UploadTasksThread.start()
    
    
    
    def start_threads(self):
        self.start_update_config_thread()
        self.start_generate_user_infos_thread()
        self.start_generate_user_strategies_thread() 
     
        self.start_generate_strategies_thread()
        self.start_generate_tasks_thread()
        
        self.start_check_tasks_distribution_thread()
        self.start_upload_tasks_thread()
    
    
    
    
if __name__ == '__main__':
    Server_T21_Ins = Server_T21.from_default()
    Server_T21_Ins.start_threads()

