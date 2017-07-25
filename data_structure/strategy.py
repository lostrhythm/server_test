# -*- coding:utf-8 -*-
'''
Created on 2017年6月19日

@author: Thinkpad
'''

import json
import copy
from utils.data_operations import do_split
from log.log import get_logger
logger = get_logger('strategy')


class Strategy():
    def __init__(self, StrategyID = 'TEST', Timeout = 0, WaitTime = 1, RetryTime = 3, AdditionParams = {}, Encoding = 'utf-8', FragmentalUpload = False, FragmentalAmount = 5, ContentException = [], CookieUse = False):
        self.StrategyID = StrategyID
        self.Encoding = Encoding
        self.Timeout = Timeout
        self.WaitTime = WaitTime
        self.RetryTime = RetryTime
        self.AdditionParams = AdditionParams
        self.FragmentalUpload = FragmentalUpload
        self.FragmentalAmount = FragmentalAmount
        self.ContentException = ContentException
        self.CookieUse = CookieUse
        
    @classmethod
    def load_Strategy(cls, StrategyJson):
        LocalEncoding = 'utf-8'
        StrategyDict = json.loads(StrategyJson, encoding = LocalEncoding)
        
        StrategyID = StrategyDict['StrategyID']
        Timeout = StrategyDict['Timeout']
        WaitTime = StrategyDict['WaitTime']
        RetryTime = StrategyDict['RetryTime']
        
        AdditionParams = json.loads(StrategyDict.get('AdditionParams') or '{}', encoding = LocalEncoding) 
        Encoding = StrategyDict.get('Encoding') or LocalEncoding 
        FragmentalUpload = StrategyDict.get('FragmentalUpload') or False
        FragmentalAmount = StrategyDict.get('FragmentalAmount') or 5
        ContentException = StrategyDict.get('ContentException') or []
        CookieUse = StrategyDict.get('CookieUse') or False
        
        
        StrategyIns = cls(StrategyID, Timeout, WaitTime, RetryTime, AdditionParams, Encoding, FragmentalUpload, FragmentalAmount, ContentException, CookieUse)
        return StrategyIns
    
    
    @classmethod
    def load_strategy_from_sqlresult(cls, SGStrategyDict):
        LocalEncoding = 'utf-8'
        
        StrategyID = SGStrategyDict['StrategyID']
        Timeout = SGStrategyDict['Timeout']
        WaitTime = SGStrategyDict['WaitTime']
        RetryTime = SGStrategyDict['RetryTime']

        AdditionParams = json.loads(SGStrategyDict.get('AdditionParams') or '{}', encoding = LocalEncoding) 
        Encoding = SGStrategyDict.get('Encoding') or LocalEncoding
        FragmentalUpload = bool(SGStrategyDict.get('FragmentalUpload') or 0) 
        FragmentalAmount = SGStrategyDict.get('FragmentalAmount') or 5
        ContentException = do_split(SGStrategyDict.get('ContentException')) 
        CookieUse = bool(SGStrategyDict.get('CookieUse') or 0) 
        
        StrategyIns = cls(StrategyID, Timeout, WaitTime, RetryTime, AdditionParams, Encoding, FragmentalUpload, FragmentalAmount, ContentException, CookieUse)
        return StrategyIns
        
        
    def get_json(self):
        LocalEncoding = 'utf-8'
        
        StrategyDict = copy.deepcopy(self.__dict__)
        StrategyDict['AdditionParams'] = json.dumps(self.__dict__['AdditionParams'], encoding = LocalEncoding) 
        StrategyJson = json.dumps(StrategyDict, encoding = LocalEncoding) 
        return StrategyJson
    
    
    
if __name__ == '__main__':
    s_0 = Strategy()
    print repr(s_0.__dict__)
    print repr(s_0.get_json())
    
    
    StrategyJson_1 = '{"RetryTime": 111, "WaitTime": 1, "StrategyID": "TEST_1", "AdditionParams": "{\\"rules\\":[\\"rule_1\\", \\"rule_2\\"]}", "Timeout": 0, "Encoding": "utf-8", "FragmentalUpload": false, "FragmentalAmount":5, "ContentException":[], "CookieUse":false}'
    s_1 = Strategy.load_Strategy(StrategyJson_1)
    s_1_json = s_1.get_json()
    print s_1.__dict__
    print repr(s_1_json)
    
    
