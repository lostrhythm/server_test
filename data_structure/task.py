# -*- coding:utf-8 -*-
'''
Created on 2017年6月19日

@author: Thinkpad
'''

import json
import copy

from log.log import get_logger
logger = get_logger('Task')

class Task():
    def __init__(self, TaskID = 0, StrategyID = 'TEST', ParentID = -1, TaskType = 0, TaskContent = '', TaskStatus = 0, AdditionParams = {}, Encoding = None, Processor = '', Priority = 1):
        self.TaskID = TaskID 
        self.StrategyID = StrategyID
        self.ParentID = ParentID 
        self.TaskType = TaskType 
        self.TaskContent = TaskContent
        self.TaskStatus = TaskStatus 
        self.AdditionParams = AdditionParams
        self.Encoding = Encoding
        self.Processor = Processor
        self.Priority = Priority

    @classmethod
    def load_task(cls, TaskJson):
        LocalEncoding = 'utf-8'
        TaskDict = json.loads(TaskJson, encoding = LocalEncoding) 
        
        TaskID = TaskDict['TaskID']
        StrategyID = TaskDict['StrategyID']
        ParentID = TaskDict['ParentID']
        TaskType = TaskDict['TaskType']
        TaskStatus = TaskDict['TaskStatus']
        
        TaskContent = TaskDict.get('TaskContent') or ''
        AdditionParams = json.loads(TaskDict.get('AdditionParams') or '{}', encoding = LocalEncoding)
        Encoding = TaskDict.get('Encoding') 
        Processor = TaskDict.get('Processor') or ''
        Priority = TaskDict.get('Priority') or 1
        
        TaskIns = cls(TaskID, StrategyID, ParentID, TaskType, TaskContent, TaskStatus, AdditionParams, Encoding, Processor, Priority)
        return TaskIns



    @classmethod
    def load_task_from_sqlresult(cls, SGTaskDict):
        LocalEncoding = 'utf-8'
        
        TaskID = SGTaskDict['TaskID']
        StrategyID = SGTaskDict['StrategyID']
        ParentID = SGTaskDict['ParentID']
        TaskType = SGTaskDict['TaskType']
        TaskStatus = SGTaskDict['TaskStatus'] 
        
        TaskContent = SGTaskDict.get('TaskContent') or ''
        AdditionParams = json.loads(SGTaskDict.get('AdditionParams') or '{}', encoding = LocalEncoding)
        Encoding = SGTaskDict.get('Encoding') 
        Processor = SGTaskDict.get('Processor') or ''
        Priority = SGTaskDict.get('Priority') or 1
        
        TaskIns = cls(TaskID, StrategyID, ParentID, TaskType, TaskContent, TaskStatus, AdditionParams, Encoding, Processor, Priority)
        return TaskIns
    
    

    def get_json(self):
        LocalEncoding = 'utf-8'
        
        TaskDict = copy.deepcopy(self.__dict__)
        [TaskDict.pop(key) for key in self.__dict__ if key[0] == '_']
        TaskDict['AdditionParams'] = json.dumps(self.__dict__['AdditionParams'], encoding = LocalEncoding)
        
        TaskJson = json.dumps(TaskDict, encoding = LocalEncoding) 
        return TaskJson
    
    
    def get_sgdict(self):
        LocalEncoding = 'utf-8'
        
        SGTaskDict = {}
        SGTaskDict['TaskID'] = self.TaskID
        SGTaskDict['StrategyID'] = self.StrategyID
        SGTaskDict['ParentID'] = self.ParentID
        SGTaskDict['TaskType'] = self.TaskType
        SGTaskDict['TaskStatus'] = self.TaskStatus
        SGTaskDict['TaskContent'] = self.TaskContent
        SGTaskDict['Encoding'] = self.Encoding
        SGTaskDict['AdditionParams'] = json.dumps(self.AdditionParams or {}, encoding = LocalEncoding) 
        SGTaskDict['Processor'] = self.Processor
        SGTaskDict['Priority'] = self.Priority
        
        return SGTaskDict
    

if __name__ == '__main__':
    t_0 = Task()
    t_1 = Task(TaskType = 3)
    t_2 = Task(TaskStatus = 3)
     
    print repr(t_0.get_json())
    print repr(t_1.get_json())
    print t_1.TaskType
    print t_2.TaskStatus
    
    
    TaskJson_3 = '{"Processor": "user", "Encoding": null, "TaskStatus": 0, "ParentID": -1, "TaskID": 0, "TaskType": 0, "StrategyID": "TEST", "AdditionParams": "{\\"a\\":2}", "TaskContent": ""}'
    t_3 = Task.load_task(TaskJson_3)
    t_3_json = t_3.get_json()
    print t_3.__dict__
    print repr(t_3_json)
    
    print t_3.get_sgdict()
     
