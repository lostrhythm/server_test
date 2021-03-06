# -*- coding:utf-8 -*-
'''
Created on 2017年6月20日

@author: Thinkpad
'''
def Singleton(cls):     # http://blog.csdn.net/linshengchao123/article/details/47775383
    _instance = {}  
    def _singleton(*args, **kargs):  
        if cls not in _instance:  
            _instance[cls] = cls(*args, **kargs)  
        return _instance[cls]  
    return _singleton  